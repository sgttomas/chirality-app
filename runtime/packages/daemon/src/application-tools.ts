import { createHash, randomUUID } from "node:crypto";
import {
  RuntimeError, applicationToolKey, canonicalApplicationJson,
  validateApplicationToolCatalog, validateApplicationToolCompletion, validateApplicationToolRegistration,
  type ApplicationToolBinding, type ApplicationToolCatalog, type ApplicationToolCompletionRequest,
  type ApplicationToolInvocation, type ApplicationToolRegistrationRequest, type ApplicationToolResult,
  type DynamicToolSpec, type RuntimeSessionRecord
} from "@chirality/runtime-contracts";

export interface ApplicationToolSessions {
  get(projectId: string, sessionId: string): Promise<RuntimeSessionRecord>;
  getApplicationToolCatalog(projectId: string, sessionId: string): Promise<ApplicationToolCatalog | undefined>;
  registerApplicationToolCatalog(projectId: string, sessionId: string, catalog: ApplicationToolCatalog): Promise<ApplicationToolCatalog>;
}
export interface ApplicationToolRegistryOptions { sessions: ApplicationToolSessions; isTurnActive?: (projectId: string, sessionId: string) => boolean }
export type ApplicationToolCall = Pick<ApplicationToolInvocation, "bindingId" | "runtimeProjectId" | "runtimeSessionId" | "runtimeTurnId" | "providerThreadId" | "providerTurnId" | "requestId" | "callId" | "namespace" | "tool" | "arguments">;
interface Pending { invocation: ApplicationToolInvocation; fingerprint: string; promise: Promise<ApplicationToolResult>; resolve: (result: ApplicationToolResult) => void; timer?: ReturnType<typeof setTimeout> }
interface State { binding?: ApplicationToolBinding; catalog?: ApplicationToolCatalog; turnId?: string; calls: Map<string, Pending>; dedupe: Map<string, Pending> }
const clone = <T>(value: T): T => structuredClone(value);
const failure = (message: string): ApplicationToolResult => ({ success: false, contentItems: [{ type: "inputText", text: message }] });
function denied(message: string): never { throw new RuntimeError("INVALID_REQUEST", message, 409); }

/** Application callbacks remain in the authenticated host. No executable paths or URLs are accepted. */
export class ApplicationToolRegistry {
  private readonly states = new Map<string, State>();
  private readonly locks = new Map<string, Promise<unknown>>();
  private closed = false;
  constructor(private readonly options: ApplicationToolRegistryOptions) {}
  private key(p: string, s: string) { return JSON.stringify([p, s]); }
  private state(p: string, s: string): State {
    const key = this.key(p, s); let state = this.states.get(key);
    if (!state) { state = { calls: new Map(), dedupe: new Map() }; this.states.set(key, state); }
    return state;
  }
  private open() { if (this.closed) denied("Application tool registry is closed"); }
  private async serial<T>(p: string, s: string, work: () => Promise<T>): Promise<T> {
    const key = this.key(p, s); const prior = this.locks.get(key) ?? Promise.resolve();
    const next = prior.catch(() => undefined).then(() => { this.open(); return work(); });
    this.locks.set(key, next);
    try { return await next; } finally { if (this.locks.get(key) === next) this.locks.delete(key); }
  }
  private active(p: string, s: string, state: State, record: RuntimeSessionRecord) {
    return state.turnId !== undefined || record.status === "running" || Boolean(this.options.isTurnActive?.(p, s));
  }
  register(p: string, s: string, input: ApplicationToolRegistrationRequest): Promise<ApplicationToolBinding> {
    const req = validateApplicationToolRegistration(input);
    return this.serial(p, s, async () => {
      const state = this.state(p, s); const record = await this.options.sessions.get(p, s); this.open();
      const catalog = validateApplicationToolCatalog({ schemaVersion: 1, applicationId: req.applicationId, workspaceId: req.workspaceId, tools: req.tools });
      const persisted = await this.options.sessions.getApplicationToolCatalog(p, s); this.open();
      if (persisted && canonicalApplicationJson(persisted) !== canonicalApplicationJson(catalog)) denied("Application tool catalog is immutable for this session");
      if (state.binding && state.binding.workspaceGeneration === req.workspaceGeneration && state.binding.timeoutMs === req.timeoutMs && canonicalApplicationJson(state.catalog) === canonicalApplicationJson(catalog)) return clone(state.binding);
      if (this.active(p, s, state, record)) denied("Application handler can only bind while the session is idle");
      const saved = await this.options.sessions.registerApplicationToolCatalog(p, s, catalog); this.open();
      this.cancel(state, "Application handler replaced");
      state.catalog = validateApplicationToolCatalog(saved);
      state.binding = { schemaVersion: 1, bindingId: randomUUID(), applicationId: req.applicationId, workspaceId: req.workspaceId, workspaceGeneration: req.workspaceGeneration, timeoutMs: req.timeoutMs, toolSetHash: createHash("sha256").update(canonicalApplicationJson(state.catalog)).digest("hex") };
      return clone(state.binding);
    });
  }
  async binding(p: string, s: string): Promise<{ catalog?: ApplicationToolCatalog; binding?: ApplicationToolBinding }> {
    return this.serial(p, s, async () => {
      await this.options.sessions.get(p, s); const catalog = await this.options.sessions.getApplicationToolCatalog(p, s); this.open();
      const binding = this.state(p, s).binding;
      return { ...(catalog ? { catalog: clone(catalog) } : {}), ...(binding ? { binding: clone(binding) } : {}) };
    });
  }
  release(p: string, s: string, bindingId: string): Promise<{ released: true }> {
    return this.serial(p, s, async () => {
      await this.options.sessions.get(p, s); this.open(); const state = this.state(p, s);
      if (state.binding?.bindingId !== bindingId) denied("Unknown or stale application tool binding");
      this.cancel(state, "Application handler released"); delete state.binding;
      return { released: true };
    });
  }
  prepareTurn(p: string, s: string, runtimeTurnId: string): Promise<{ binding: ApplicationToolBinding; tools: DynamicToolSpec[] } | undefined> {
    return this.serial(p, s, async () => {
      await this.options.sessions.get(p, s); const state = this.state(p, s);
      if (state.turnId !== undefined && state.turnId !== runtimeTurnId) denied("Application tools already prepared for another turn");
      const catalog = await this.options.sessions.getApplicationToolCatalog(p, s); this.open();
      if (!catalog) return undefined;
      if (!state.binding) denied("Application tool handler is unavailable; explicitly rebind the persisted catalog before continuing");
      if (state.turnId === undefined) { state.calls.clear(); state.dedupe.clear(); }
      state.turnId = runtimeTurnId;
      state.catalog = validateApplicationToolCatalog(catalog);
      return { binding: clone(state.binding), tools: clone(state.catalog.tools) };
    });
  }
  async call(input: ApplicationToolCall): Promise<ApplicationToolResult> {
    if (this.closed) return failure("Application tool registry is closed");
    const state = this.states.get(this.key(input.runtimeProjectId, input.runtimeSessionId));
    const binding = state?.binding;
    if (!state || !binding || binding.bindingId !== input.bindingId || state.turnId !== input.runtimeTurnId) return failure("Unknown, stale or unprepared application tool call");
    let fingerprint: string;
    try { canonicalApplicationJson(input); fingerprint = canonicalApplicationJson({ namespace: input.namespace, tool: input.tool, arguments: input.arguments }); }
    catch { return failure("Invalid or oversized application tool arguments"); }
    const identities = [input.bindingId, input.runtimeProjectId, input.runtimeSessionId, input.runtimeTurnId, input.providerThreadId, input.providerTurnId, input.callId];
    if (identities.some(value => typeof value !== "string" || !value || value.length > 256 || /[\u0000-\u001f]/u.test(value)) ||
      !(typeof input.requestId === "string" && input.requestId.length > 0 && input.requestId.length <= 256 || typeof input.requestId === "number" && Number.isFinite(input.requestId)) ||
      typeof input.tool !== "string" || !/^[a-zA-Z0-9_-]{1,64}$/.test(input.tool) ||
      input.namespace !== null && (typeof input.namespace !== "string" || !/^[a-zA-Z0-9_-]{1,64}$/.test(input.namespace))) return failure("Invalid application tool source identity");
    const dedupeKey = JSON.stringify([input.bindingId, input.providerThreadId, input.providerTurnId, input.callId]);
    const existing = state.dedupe.get(dedupeKey);
    if (existing) return fingerprint === existing.fingerprint ? clone(await existing.promise) : failure("Conflicting duplicate application tool call");
    const registered = state.catalog?.tools.some(spec => spec.type === "function" ? input.namespace === null && spec.name === input.tool : spec.name === input.namespace && spec.tools.some(fn => fn.name === input.tool));
    if (!registered) return failure(`Unregistered application tool ${applicationToolKey(input.namespace, input.tool)}`);
    // Bound memory retained for deduplication through the turn. Never evict and redispatch.
    if (state.calls.size >= 1024) return failure("Application tool call limit reached for this turn");
    const now = Date.now();
    const invocation: ApplicationToolInvocation = { ...clone(input), invocationId: randomUUID(), applicationId: binding.applicationId, workspaceId: binding.workspaceId, workspaceGeneration: binding.workspaceGeneration, status: "pending", createdAt: new Date(now).toISOString(), deadline: new Date(now + binding.timeoutMs).toISOString() };
    let resolve!: Pending["resolve"];
    const promise = new Promise<ApplicationToolResult>(done => { resolve = done; });
    const pending: Pending = { invocation, fingerprint, promise, resolve };
    pending.timer = setTimeout(() => this.settle(pending, "failed", "Application tool handler timed out"), binding.timeoutMs);
    pending.timer.unref?.(); state.calls.set(invocation.invocationId, pending); state.dedupe.set(dedupeKey, pending);
    return clone(await promise);
  }
  cancelCall(input: ApplicationToolCall, reason: string): void {
    const state = this.states.get(this.key(input.runtimeProjectId, input.runtimeSessionId));
    if (!state || state.binding?.bindingId !== input.bindingId || state.turnId !== input.runtimeTurnId) return;
    const key = JSON.stringify([input.bindingId, input.providerThreadId, input.providerTurnId, input.callId]);
    const pending = state.dedupe.get(key);
    if (pending) this.settle(pending, "cancelled", reason);
  }
  listCalls(p: string, s: string, bindingId: string): ApplicationToolInvocation[] {
    this.open(); const state = this.states.get(this.key(p, s));
    // A released binding may still inspect its terminal cancellation records.
    if (!state || state.binding?.bindingId !== bindingId && ![...state.calls.values()].some(call => call.invocation.bindingId === bindingId)) denied("Unknown application tool binding");
    return [...state.calls.values()].filter(call => call.invocation.bindingId === bindingId).map(call => clone(call.invocation));
  }
  complete(p: string, s: string, invocationId: string, input: ApplicationToolCompletionRequest): { state: "completed" | "already-completed" } {
    this.open(); const req = validateApplicationToolCompletion(input); const state = this.states.get(this.key(p, s)); const pending = state?.calls.get(invocationId);
    if (!state || !pending || state.binding?.bindingId !== req.bindingId || pending.invocation.bindingId !== req.bindingId) denied("Unknown, stale or cancelled application tool invocation");
    if (pending.invocation.status === "completed") {
      if (canonicalApplicationJson(pending.invocation.result) !== canonicalApplicationJson(req.result)) denied("Conflicting duplicate application tool result");
      return { state: "already-completed" };
    }
    if (state.turnId !== pending.invocation.runtimeTurnId || pending.invocation.status !== "pending") denied("Application tool invocation is no longer pending");
    if (Date.now() >= Date.parse(pending.invocation.deadline)) { this.settle(pending, "failed", "Application tool handler timed out"); denied("Application tool invocation has expired"); }
    if (pending.timer) clearTimeout(pending.timer); delete pending.timer;
    pending.invocation.status = "completed"; pending.invocation.result = clone(req.result); pending.resolve(clone(req.result));
    return { state: "completed" };
  }
  private settle(pending: Pending, status: "failed" | "cancelled", reason: string) {
    if (pending.invocation.status !== "pending") return;
    if (pending.timer) clearTimeout(pending.timer); delete pending.timer;
    pending.invocation.status = status; pending.invocation.failure = reason; pending.invocation.result = failure(reason); pending.resolve(clone(pending.invocation.result));
  }
  private cancel(state: State, reason: string) { for (const pending of state.calls.values()) this.settle(pending, "cancelled", reason); }
  finishTurn(p: string, s: string, runtimeTurnId: string, reason: string): void {
    const state = this.states.get(this.key(p, s)); if (!state || state.turnId !== runtimeTurnId) return;
    this.cancel(state, reason); delete state.turnId; state.dedupe.clear();
  }
  close(): void { if (this.closed) return; this.closed = true; for (const state of this.states.values()) { this.cancel(state, "Application tool registry closed"); delete state.binding; delete state.turnId; } }
}
