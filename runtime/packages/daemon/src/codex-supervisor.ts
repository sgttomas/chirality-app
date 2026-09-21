import { createHash, randomUUID } from "node:crypto";
import {
  RuntimeError,
  canonicalApplicationJson,
  type ApplicationJson,
  type ApplicationToolBinding,
  type DynamicToolSpec,
  type DelegatedHarnessProcessSupervisorPort,
  type DelegatedTurnProgressEvent,
  type InstructionHistoryInjection,
  type NativePlanClarificationAnswers,
  type NativePlanClarificationPrompt,
  type NativePlanTransportEvent,
  type PendingServerRequest,
  type PolicySelection,
  type ServerRequestAnswer,
  type ServerRequestDecider,
  type ServerRequestOutcome,
  type SupervisorNativePlanPort,
  type SupervisorRequestPort,
  type SupervisorSteerPort,
  type SessionSteerRequest,
  type SessionSteerResponse,
  type SupervisorTurnProgressPort,
  type WorkerHandle,
  type WorkerResult
} from "@chirality/runtime-contracts";
import type { ApplicationToolCall, ApplicationToolRegistry } from "./application-tools.js";
import { parseCodexTurnEnvelope, type CodexTurnEnvelope } from "@chirality/runtime-core";
import { JSON_RPC_METHOD_NOT_FOUND, NOOP_CODEX_LOGGER, type CodexAppServerExit, type CodexAppServerHost, type CodexLogger, type CodexNotification, type CodexServerRequest, type CodexServerRequestOutcome } from "./codex-app-server-client.js";

/**
 * Turn supervisor over one long-lived stock `codex app-server`. One worker
 * generation per turn; `interrupt` sends `turn/interrupt` and never retires;
 * `retire` releases the turn's bookkeeping and is memoized per exact
 * generation. Every notification passes through unchanged; every server
 * request is answered or refused visibly.
 */

export const APPROVAL_REQUEST_METHODS = Object.freeze(new Set(["item/commandExecution/requestApproval", "item/fileChange/requestApproval", "item/permissions/requestApproval", "execCommandApproval", "applyPatchApproval"]));
// Stock thread shutdown allows ten seconds; retain two seconds for scheduling.
export const INSTRUCTION_UNLOAD_TIMEOUT_MS = 12_000;
const USER_INPUT_METHOD = "item/tool/requestUserInput";
const ELICITATION_METHOD = "mcpServer/elicitation/request";
const DYNAMIC_TOOL_METHOD = "item/tool/call";
const UNSUPPORTED_METHODS = Object.freeze(new Set(["account/chatgptAuthTokens/refresh", "attestation/generate"]));

/** Minimal host surface the supervisor needs; `CodexAppServerHost` satisfies it. */
export type CodexSupervisorHost = Pick<CodexAppServerHost, "request" | "onNotification" | "onExit" | "onStart" | "setServerRequestHandler" | "generation">;

export interface CodexSupervisorOptions {
  host: CodexSupervisorHost;
  logger?: CodexLogger;
  maxWorkers?: number;
  /** Bound on queued progress events per turn before the oldest are dropped with a warning. */
  maxQueuedProgress?: number;
  instructionUnloadTimeoutMs?: number;
  applicationTools?: Pick<ApplicationToolRegistry, "prepareTurn" | "call" | "cancelCall" | "finishTurn">;
}

interface PendingRequestEntry {
  request: PendingServerRequest;
  settle(outcome: CodexServerRequestOutcome): void;
}
interface ApplicationOwnership {
  binding: ApplicationToolBinding;
  tools: DynamicToolSpec[];
  envelope: CodexTurnEnvelope;
  hostGeneration: number;
  finished: boolean;
  removeAbortListener?: () => void;
  pending: Map<string, { threadId: string; turnId: string; cancel(): void }>;
  seen: Set<string>;
}
interface Entry {
  application?: ApplicationOwnership;
  handle: WorkerHandle;
  envelope: CodexTurnEnvelope;
  instructionHistoryInjection?: InstructionHistoryInjection;
  threadId: string;
  /** Unknown until the turn/start response; notifications that arrive first are deferred behind the started event. */
  turnId: string | undefined;
  /** Resolves with the turn identity once adopted, or undefined when the turn ends without one. */
  turnIdReady: Promise<string | undefined>;
  adopt(turnId: string | undefined): void;
  deferred: DelegatedTurnProgressEvent[];
  hostGeneration: number;
  progress: DelegatedTurnProgressEvent[];
  nativePlanEvents: NativePlanTransportEvent[];
  pending: Map<string, PendingRequestEntry>;
  text: string;
  emittedByItem: Map<string, number>;
  result: Promise<WorkerResult>;
  settle(result: WorkerResult): void;
  settled: boolean;
}
interface ThreadState { instructionDigest: string; instructionHistoryInjection?: InstructionHistoryInjection; lastPolicy?: PolicySelection; lastMode?: "plan" | "default"; model?: string; hostGeneration: number }

const id = (value: unknown): value is string => typeof value === "string" && /^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$/.test(value);
const unavailable = (message: string, details?: Record<string, unknown>) => new RuntimeError("ENGINE_UNAVAILABLE", message, 503, details);
function record(value: unknown): Record<string, unknown> {
  return value && typeof value === "object" && !Array.isArray(value) ? value as Record<string, unknown> : {};
}
function sandboxPolicy(sandbox: PolicySelection["sandbox"], cwd: string): unknown {
  switch (sandbox) {
    case "read-only": return { type: "readOnly", networkAccess: false };
    case "workspace-write": return { type: "workspaceWrite", writableRoots: [cwd], networkAccess: false, excludeTmpdirEnvVar: false, excludeSlashTmp: false };
    case "danger-full-access": return { type: "dangerFullAccess" };
  }
}
function samePolicy(a: PolicySelection | undefined, b: PolicySelection): boolean {
  return a !== undefined && a.approvalPolicy === b.approvalPolicy && a.sandbox === b.sandbox;
}

export class CodexSupervisor implements DelegatedHarnessProcessSupervisorPort, SupervisorTurnProgressPort, SupervisorRequestPort, SupervisorNativePlanPort, SupervisorSteerPort {
  private readonly entries = new Map<string, Entry>();
  private readonly byThread = new Map<string, Entry>();
  private readonly childThreads = new Map<string, string>();
  private readonly activeChildren = new Set<string>();
  private readonly childTurns = new Map<string, { turnId: string; owner: Entry }>();
  private readonly applicationOwnerships = new Set<ApplicationOwnership>();
  private readonly acquiringThreads = new Set<string>();
  private readonly closedThreads = new Set<string>();
  private readonly pendingUnloads = new Set<string>();
  private readonly closeWaiters = new Map<string, () => void>();
  private readonly threads = new Map<string, ThreadState>();
  private readonly retirements = new Map<string, Promise<void>>();
  private readonly acquiring = new Set<string>();
  private closed = false;
  private providerExitEpoch = 0;
  private readonly logger: CodexLogger;
  private readonly unsubscribe: (() => void)[] = [];
  constructor(private readonly options: CodexSupervisorOptions) {
    this.logger = options.logger ?? NOOP_CODEX_LOGGER;
    options.host.setServerRequestHandler(request => this.handleServerRequest(request));
    this.unsubscribe.push(options.host.onNotification(notification => this.handleNotification(notification)));
    this.unsubscribe.push(options.host.onExit((exit, generation) => this.handleExit(exit, generation)));
  }

  /** Threads known to the current app-server child; after a restart every thread needs `thread/resume`. */
  private threadState(threadId: string): ThreadState | undefined {
    const state = this.threads.get(threadId);
    return state !== undefined && state.hostGeneration === this.options.host.generation ? state : undefined;
  }

  async acquire(workerId: string, input: string, signal?: AbortSignal): Promise<WorkerHandle> {
    if (this.closed) throw unavailable("Codex supervisor is closed");
    signal?.throwIfAborted();
    if (!id(workerId)) throw new RuntimeError("INVALID_REQUEST", "Invalid worker identity");
    if (this.entries.has(workerId) || this.acquiring.has(workerId)) throw unavailable("Codex worker is already acquired");
    if (this.entries.size + this.acquiring.size >= (this.options.maxWorkers ?? 16)) throw unavailable("Codex worker capacity exceeded");
    if (typeof input !== "string" || Buffer.byteLength(input) > 4 * 1024 * 1024) throw new RuntimeError("INVALID_REQUEST", "Invalid Codex turn envelope");
    const envelope = parseCodexTurnEnvelope(input);
    if (envelope.contextUpdate !== undefined) throw new RuntimeError("INVALID_REQUEST", "Persistent guidance must use developerInstructions; contextUpdate is retired");
    if (envelope.resumeThreadId !== undefined) {
      if (this.acquiringThreads.has(envelope.resumeThreadId) || this.byThread.has(envelope.resumeThreadId)) throw unavailable("Codex thread already has a live turn or instruction adoption");
      this.acquiringThreads.add(envelope.resumeThreadId);
    }
    this.acquiring.add(workerId);
    let application: ApplicationOwnership | undefined;
    try {
      const host = this.options.host;
      const hostGeneration = host.generation;
      const providerExitEpoch = this.providerExitEpoch;
      if (this.options.applicationTools && envelope.sessionId) {
        const prepared = await this.options.applicationTools.prepareTurn(envelope.projectId, envelope.sessionId, envelope.clientTurnId);
        if (prepared) {
          application = { ...prepared, envelope, hostGeneration, finished: false, pending: new Map(), seen: new Set() };
          this.applicationOwnerships.add(application);
          if (signal) {
            const owned = application;
            const abort = () => this.finishApplication(owned, "turn acquisition aborted");
            signal.addEventListener("abort", abort, { once: true });
            application.removeAbortListener = () => signal.removeEventListener("abort", abort);
          }
        }
      }
      signal?.throwIfAborted();
      if (this.closed || host.generation !== hostGeneration || providerExitEpoch !== this.providerExitEpoch) throw unavailable("Provider changed during application tool preparation");
      const model = envelope.model;
      const instructionDigest = createHash("sha256").update(JSON.stringify([envelope.developerInstructions ?? null, envelope.nativeRoleConfig ?? null])).digest("hex");
      let threadId: string;
      let threadModel: string | undefined;
      let state = envelope.resumeThreadId === undefined ? undefined : this.threadState(envelope.resumeThreadId);
      if (envelope.resumeThreadId !== undefined && (state === undefined || state.instructionDigest !== instructionDigest || this.pendingUnloads.has(envelope.resumeThreadId))) {
        await this.prepareInstructionResume(envelope.resumeThreadId, hostGeneration, signal);
        state = undefined;
      }
      signal?.throwIfAborted();
      if (envelope.resumeThreadId !== undefined && state === undefined) {
        const resumed = await host.request<{ thread: { id: string; status: { type: string } }; model: string }>("thread/resume", { threadId: envelope.resumeThreadId, cwd: envelope.cwd, developerInstructions: envelope.developerInstructions ?? null, ...(envelope.nativeRoleConfig === undefined ? {} : { config: envelope.nativeRoleConfig }), approvalPolicy: envelope.policy.approvalPolicy, sandbox: envelope.policy.sandbox, ...(model === undefined ? {} : { model }) });
        if (resumed.thread.id !== envelope.resumeThreadId || host.generation !== hostGeneration) throw unavailable("Provider changed during instruction adoption; retry the turn");
        if (resumed.thread.status?.type !== "idle") throw new RuntimeError("INSTRUCTION_ADOPTION_PENDING", "Instruction update pending: resumed thread is not confirmed idle; no developer item or user turn was sent.", 503, { reason: "INSTRUCTION_ADOPTION_PENDING", stage: "resume", threadId: envelope.resumeThreadId });
        threadId = resumed.thread.id; threadModel = resumed.model;
        this.closedThreads.delete(threadId); this.pendingUnloads.delete(threadId);
        // Cold resume restores reference context and history independently of
        // config.developer_instructions in stock 0.154. Explicitly supersede the
        // prior Chirality guidance in developer-level model-visible history.
        const text = "The following is the current Chirality guidance. It supersedes earlier Chirality-provided product, active-role, catalog, and selected-method instructions in this conversation. Earlier versions remain historical context, not current instructions. This update does not replace Codex base instructions or change tools, permissions, applicable project guidance, or conversation history.\n\nCurrent Chirality developer instructions:\n\n" + (envelope.developerInstructions ?? "");
        const instructionHistoryInjection: InstructionHistoryInjection = { method: "thread/inject_items", text, sha256: createHash("sha256").update(text).digest("hex") };
        try {
          signal?.throwIfAborted();
          const acknowledged = await host.request<unknown>("thread/inject_items", { threadId, items: [{ type: "message", role: "developer", content: [{ type: "input_text", text }] }] });
          if (!acknowledged || typeof acknowledged !== "object" || Array.isArray(acknowledged) || Object.keys(acknowledged).length !== 0 || host.generation !== hostGeneration || this.closed) throw unavailable("Developer history injection was not acknowledged");
          signal?.throwIfAborted();
        } catch (error) {
          // A lost acknowledgement may have persisted the item. A retry must
          // re-establish the cold boundary and supersede it again, never infer
          // exactly-once delivery or reuse a config-only accepted digest.
          this.threads.delete(threadId); this.pendingUnloads.add(threadId);
          signal?.throwIfAborted();
          throw new RuntimeError("INSTRUCTION_ADOPTION_PENDING", "Instruction update pending: developer history injection was not confirmed. Retry in this conversation; no new user turn was sent.", 503, { reason: "INSTRUCTION_ADOPTION_PENDING", stage: "developer-history-injection", threadId });
        }
        state = { instructionDigest, instructionHistoryInjection, lastPolicy: { ...envelope.policy }, model: threadModel, hostGeneration };

        this.threads.set(threadId, state);
        this.logger.warn("codex.thread.resumed", { threadId, workerId });
      } else if (state === undefined) {
        const started = await host.request<{ thread: { id: string }; model: string }>("thread/start", { cwd: envelope.cwd, developerInstructions: envelope.developerInstructions ?? null, ...(envelope.nativeRoleConfig === undefined ? {} : { config: envelope.nativeRoleConfig }), approvalPolicy: envelope.policy.approvalPolicy, sandbox: envelope.policy.sandbox, ...(model === undefined ? {} : { model }), ephemeral: false, serviceName: "chirality", ...(application === undefined ? {} : { dynamicTools: application.tools }) });
        threadId = started.thread.id; threadModel = started.model;
        state = { instructionDigest, lastPolicy: { ...envelope.policy }, model: threadModel, hostGeneration };
        this.threads.set(threadId, state);
      } else {
        threadId = envelope.resumeThreadId!;
        threadModel = state.model;
      }
      signal?.throwIfAborted();
      if (this.closed || application?.finished || host.generation !== hostGeneration) throw unavailable("Codex supervisor or application turn is no longer active");
      if (this.byThread.has(threadId)) throw unavailable("Codex thread already has a live turn");
      const requestedMode: "plan" | "default" = envelope.interactionMode === "native-plan" ? "plan" : "default";
      if (state.lastMode !== requestedMode) {
        await host.request("thread/settings/update", { threadId, collaborationMode: { mode: requestedMode, settings: { model: model ?? threadModel ?? state.model ?? null, reasoning_effort: envelope.reasoningEffort ?? null, developer_instructions: null } } });
        state.lastMode = requestedMode;
      }
      signal?.throwIfAborted();
      if (this.closed || application?.finished || host.generation !== hostGeneration || providerExitEpoch !== this.providerExitEpoch) throw unavailable("Provider changed during turn acquisition");
      const policyChanged = !samePolicy(state.lastPolicy, envelope.policy);
      state.lastPolicy = { ...envelope.policy };
      if (model !== undefined) state.model = model;
      const inputItems: unknown[] = [];
      inputItems.push({ type: "text", text: envelope.prompt });
      for (const attachment of envelope.attachments ?? []) {
        if (attachment.type === "text") inputItems.push({ type: "text", text: attachment.text });
        else if (attachment.type === "localImage") inputItems.push({ type: "localImage", path: attachment.path });
      }
      // The entry is live before turn/start goes out: the app-server streams the
      // turn's notifications and requests right behind its response, and the
      // response continuation must not lose them.
      const handle: WorkerHandle = { workerId, generation: randomUUID(), pid: 0, state: "running" };
      let settle!: (result: WorkerResult) => void;
      const result = new Promise<WorkerResult>(resolve => { settle = resolve; });
      let adopt!: (turnId: string | undefined) => void;
      const turnIdReady = new Promise<string | undefined>(resolve => { adopt = resolve; });
      const entry: Entry = { handle, envelope, ...(application === undefined ? {} : { application }), ...(state.instructionHistoryInjection === undefined ? {} : { instructionHistoryInjection: state.instructionHistoryInjection }), threadId, turnId: undefined, turnIdReady, adopt, deferred: [], hostGeneration, progress: [], nativePlanEvents: [], pending: new Map(), text: "", emittedByItem: new Map(), result, settle: value => { if (entry.settled) return; entry.settled = true; this.finishApplication(entry.application, "turn ended"); entry.application = undefined; entry.handle.state = "exited"; entry.adopt(undefined); settle(value); }, settled: false };
      this.entries.set(workerId, entry);
      this.byThread.set(threadId, entry);
      let started: { turn: { id: string; status: string } };
      try {
        started = await host.request<{ turn: { id: string; status: string } }>("turn/start", { threadId, input: inputItems,
          ...(model === undefined ? {} : { model }), ...(envelope.reasoningEffort === undefined ? {} : { effort: envelope.reasoningEffort }),
          ...(policyChanged ? { approvalPolicy: envelope.policy.approvalPolicy, sandboxPolicy: sandboxPolicy(envelope.policy.sandbox, envelope.cwd) } : {}) });
      } catch (error) {
        entry.adopt(undefined);
        this.cancelPending(entry, "failed");
        if (this.entries.get(workerId) === entry) this.entries.delete(workerId);
        if (this.byThread.get(threadId) === entry) this.byThread.delete(threadId);
        throw error;
      }
      this.adoptTurn(entry, started.turn.id);
      return { ...handle };
    } catch (error) {
      this.finishApplication(application, "turn acquisition failed");
      throw error;
    } finally { this.acquiring.delete(workerId); if (envelope.resumeThreadId !== undefined) this.acquiringThreads.delete(envelope.resumeThreadId); }
  }

  /** Codex 0.154 ignores hot resume overrides. Unsubscribe is not proof of unload. */
  private async prepareInstructionResume(threadId: string, hostGeneration: number, signal?: AbortSignal): Promise<void> {
    const pending = (reason: string) => new RuntimeError("INSTRUCTION_ADOPTION_PENDING", `Instruction update pending: ${reason}. Wait for active work or thread unload, then retry. If this persists, restart Chirality after active work finishes and retry in this conversation; no new turn was sent.`, 503, { reason: "INSTRUCTION_ADOPTION_PENDING", threadId });
    // Read the current loaded tree, including descendants that outlived the
    // primary's last turn. Never stop descendants as an instruction refresh.
    try {
      signal?.throwIfAborted();
      let cursor: string | undefined;
      const seen = new Set<string>();
      const loaded = new Map<string, { parent?: string; active: boolean }>();
      do {
        const page = await this.options.host.request<{ data: string[]; nextCursor: string | null }>("thread/loaded/list", { ...(cursor === undefined ? {} : { cursor }) });
        if (!Array.isArray(page.data)) throw pending("loaded-thread evidence is unavailable");
        for (const id of page.data) {
          const result = await this.options.host.request<{ thread: { parentThreadId?: string | null; status: { type: string } } }>("thread/read", { threadId: id, includeTurns: false });
          const status = result.thread.status?.type;
          loaded.set(id, { ...(result.thread.parentThreadId ? { parent: result.thread.parentThreadId } : {}), active: !["idle", "systemError", "notLoaded"].includes(status) });
          if (["idle", "systemError", "notLoaded"].includes(status)) this.activeChildren.delete(id);
        }
        cursor = page.nextCursor ?? undefined;
        if (cursor !== undefined && seen.has(cursor)) throw pending("loaded-thread pagination did not converge");
        if (cursor !== undefined) seen.add(cursor);
      } while (cursor !== undefined);
      const descendant = (id: string): boolean => {
        const visited = new Set<string>();
        let parent = loaded.get(id)?.parent ?? this.childThreads.get(id);
        while (parent && !visited.has(parent)) {
          if (parent === threadId) return true;
          visited.add(parent); parent = loaded.get(parent)?.parent ?? this.childThreads.get(parent);
        }
        return false;
      };
      if (loaded.get(threadId)?.active || [...loaded].some(([id, value]) => value.active && descendant(id)) || [...this.activeChildren].some(descendant)) throw pending("the primary or a native descendant is active");
      signal?.throwIfAborted();
      if (this.options.host.generation !== hostGeneration || this.closed) throw pending("the provider changed");
      if (!loaded.has(threadId)) { this.threads.delete(threadId); return; }
      this.closedThreads.delete(threadId);
      let finish!: () => void;
      const closed = new Promise<void>(resolve => { finish = resolve; });
      this.closeWaiters.set(threadId, finish);
      signal?.addEventListener("abort", finish, { once: true });
      let timer: ReturnType<typeof setTimeout> | undefined;
      try {
        this.pendingUnloads.add(threadId);
        const result = await this.options.host.request<{ status: string }>("thread/unsubscribe", { threadId });
        if (result.status !== "notLoaded") {
          if (!["unsubscribed", "notSubscribed"].includes(result.status)) throw pending("unsubscribe was not accepted");
          await Promise.race([closed, new Promise<void>(resolve => { timer = setTimeout(resolve, this.options.instructionUnloadTimeoutMs ?? INSTRUCTION_UNLOAD_TIMEOUT_MS); })]);
          signal?.throwIfAborted();
          if (!this.closedThreads.has(threadId) && (await this.loadedThreadIds()).has(threadId)) throw pending("Codex has not confirmed thread unload");
        }
        if (this.options.host.generation !== hostGeneration || this.closed) throw pending("the provider changed");
        this.threads.delete(threadId);
      } finally { if (timer) clearTimeout(timer); this.closeWaiters.delete(threadId); signal?.removeEventListener("abort", finish); }
    } catch (error) {
      signal?.throwIfAborted();
      if (error instanceof RuntimeError && error.details?.reason === "INSTRUCTION_ADOPTION_PENDING") throw error;
      throw pending("safe unload could not be verified");
    }
  }

  /** A missed closed notification is recoverable only with complete absence evidence. */
  private async loadedThreadIds(): Promise<Set<string>> {
    const loaded = new Set<string>();
    const seen = new Set<string>();
    let cursor: string | undefined;
    do {
      const page = await this.options.host.request<{ data: string[]; nextCursor: string | null }>("thread/loaded/list", { ...(cursor === undefined ? {} : { cursor }) });
      if (!Array.isArray(page.data) || page.data.some(id => typeof id !== "string") || (page.nextCursor !== null && typeof page.nextCursor !== "string")) throw unavailable("Invalid loaded-thread evidence");
      for (const id of page.data) loaded.add(id);
      cursor = page.nextCursor ?? undefined;
      if (cursor !== undefined && seen.has(cursor)) throw unavailable("Loaded-thread pagination did not converge");
      if (cursor !== undefined) seen.add(cursor);
    } while (cursor !== undefined);
    return loaded;
  }

  async inventory(): Promise<readonly WorkerHandle[]> { return [...this.entries.values()].map(entry => ({ ...entry.handle })); }
  private entry(workerId: string, generation: string): Entry {
    const entry = this.entries.get(workerId);
    if (!entry || entry.handle.generation !== generation) throw unavailable("unknown or stale worker generation", { workerId });
    return entry;
  }
  async reconnect(workerId: string, generation: string): Promise<WorkerHandle> { return { ...this.entry(workerId, generation).handle }; }
  async wait(workerId: string, generation: string): Promise<WorkerResult> { return this.entry(workerId, generation).result; }

  async steerTurn(workerId: string, generation: string, request: SessionSteerRequest): Promise<SessionSteerResponse> {
    const base = { operationId: request.operationId, turnId: request.expectedTurnId };
    const entry = this.entry(workerId, generation);
    const providerTurnId = entry.turnId;
    if (entry.settled || entry.envelope.clientTurnId !== request.expectedTurnId || !providerTurnId
      || entry.hostGeneration !== this.options.host.generation || this.byThread.get(entry.threadId) !== entry) {
      return { ...base, status: "rejected", message: "The target turn is no longer active; no input was sent." };
    }
    try {
      const result = await this.options.host.request<{ turnId: string }>("turn/steer", {
        threadId: entry.threadId, expectedTurnId: providerTurnId,
        clientUserMessageId: request.operationId,
        input: [{ type: "text", text: request.text, text_elements: [] }]
      });
      if (result?.turnId !== providerTurnId) return { ...base, providerTurnId, status: "unknown", message: "Codex did not confirm the expected turn. Input may have been received; it was not resent." };
      return { ...base, providerTurnId, status: "accepted" };
    } catch (error) {
      // Only explicit request/method/parameter rejections establish non-acceptance. A
      // timeout, closed transport or lost response can follow successful input.
      const rejected = error instanceof RuntimeError && [-32600, -32601, -32602].includes(Number(error.details?.jsonRpcCode));
      return { ...base, providerTurnId, status: rejected ? "rejected" : "unknown", message: rejected ? (error as Error).message : "Input delivery is unconfirmed. It may have been received; it was not resent." };
    }
  }

  /** Sends `turn/interrupt` and resolves at the turn's own terminal. Never retires. */
  async interrupt(workerId: string, generation: string): Promise<void> {
    const entry = this.entry(workerId, generation);
    if (entry.settled) return;
    this.finishApplication(entry.application, "turn interrupted");
    entry.application = undefined;
    // Stop during the turn/start round trip waits for the turn identity (the
    // response or the turn/started adoption) instead of sending an empty id.
    const turnId = entry.turnId ?? await entry.turnIdReady;
    if (turnId === undefined || entry.settled) return;
    try { await this.options.host.request("turn/interrupt", { threadId: entry.threadId, turnId }); }
    catch (error) { if (entry.settled) return; throw error; }
    await entry.result;
  }

  /** Releases the turn's bookkeeping; idempotent per exact generation, stale generations reject. */
  retire(workerId: string, generation: string): Promise<void> {
    const key = `${workerId}\0${generation}`;
    const memo = this.retirements.get(key);
    if (memo !== undefined) return memo;
    let entry: Entry;
    try { entry = this.entry(workerId, generation); }
    catch (error) { return Promise.reject(error); }
    const attempt = (async () => {
      this.cancelPending(entry, "cancelled");
      if (!entry.settled) entry.settle(this.failedResult(entry, "turn retired before its terminal"));
      if (this.entries.get(workerId) === entry) this.entries.delete(workerId);
      if (this.byThread.get(entry.threadId) === entry) this.byThread.delete(entry.threadId);
    })();
    this.retirements.set(key, attempt);
    if (this.retirements.size > 1024) { const oldest = this.retirements.keys().next().value; if (oldest !== undefined && oldest !== key) this.retirements.delete(oldest); }
    return attempt;
  }

  async close(): Promise<void> {
    this.closed = true;
    for (const ownership of this.applicationOwnerships) this.finishApplication(ownership, "supervisor closed");
    for (const fn of this.unsubscribe.splice(0)) fn();
    await Promise.all([...this.entries.values()].map(entry => this.retire(entry.handle.workerId, entry.handle.generation).catch(() => undefined)));
  }

  /** Fixes the turn identity, publishes the started event first, then whatever the stream delivered ahead of the response. */
  private adoptTurn(entry: Entry, turnId: string): void {
    if (entry.turnId !== undefined) return;
    entry.turnId = turnId;
    entry.adopt(turnId);
    const deferred = entry.deferred.splice(0);
    this.push(entry, { type: "started", providerThreadId: entry.threadId, providerTurnId: turnId, ...(entry.instructionHistoryInjection === undefined ? {} : { instructionHistoryInjection: entry.instructionHistoryInjection }) });
    for (const event of deferred) this.push(entry, { ...event, providerTurnId: event.providerTurnId || turnId } as DelegatedTurnProgressEvent);
  }

  // Progress and native plan ports.
  async drainTurnProgress(workerId: string, generation: string): Promise<readonly DelegatedTurnProgressEvent[]> {
    const entry = this.entry(workerId, generation);
    return entry.progress.splice(0);
  }
  async drainNativePlanEvents(workerId: string, generation: string): Promise<readonly NativePlanTransportEvent[]> {
    const entry = this.entry(workerId, generation);
    return entry.nativePlanEvents.splice(0);
  }
  async pendingNativePlanClarifications(workerId: string, generation: string): Promise<readonly NativePlanClarificationPrompt[]> {
    const entry = this.entry(workerId, generation);
    if (entry.envelope.interactionMode !== "native-plan" || !entry.envelope.sessionId) return [];
    const prompts: NativePlanClarificationPrompt[] = [];
    for (const { request } of entry.pending.values()) {
      if (request.method !== USER_INPUT_METHOD) continue;
      const params = record(request.params);
      const questions = Array.isArray(params.questions) ? params.questions.map(question => { const q = record(question); return { id: String(q.id ?? ""), header: String(q.header ?? ""), question: String(q.question ?? ""), options: Array.isArray(q.options) ? q.options.map(option => { const o = record(option); return { label: String(o.label ?? ""), description: String(o.description ?? "") }; }) : [], isOther: q.isOther === true, isSecret: q.isSecret === true }; }) : [];
      prompts.push({ projectId: entry.envelope.projectId, sessionId: entry.envelope.sessionId, clientTurnId: entry.envelope.clientTurnId, providerThreadId: entry.threadId, providerTurnId: entry.turnId ?? "", requestId: request.requestId, itemId: request.itemId ?? "", questions, isBlocking: params.isBlocking !== false, autoResolutionMs: typeof params.autoResolutionMs === "number" ? params.autoResolutionMs : null });
    }
    return prompts;
  }
  async replyNativePlanClarification(workerId: string, generation: string, requestId: string | number, answers: NativePlanClarificationAnswers): Promise<{ sent: true }> {
    const mapped: Record<string, { answers: string[] }> = {};
    for (const [question, value] of Object.entries(answers)) mapped[question] = { answers: [...value.answers] };
    return this.answerRequest(workerId, generation, String(requestId), { kind: "userInput", answers: mapped });
  }

  // Request port.
  async pendingRequests(workerId: string, generation: string): Promise<readonly PendingServerRequest[]> {
    const entry = this.entry(workerId, generation);
    return [...entry.pending.values()].map(({ request }) => structuredClone(request));
  }
  async answerRequest(workerId: string, generation: string, requestId: string, answer: ServerRequestAnswer): Promise<{ sent: true }> {
    const entry = this.entry(workerId, generation);
    const pending = entry.pending.get(requestId);
    if (!pending) throw new RuntimeError("NOT_FOUND", "Codex request is no longer pending", 404, { requestId });
    const method = pending.request.method;
    let outcome: CodexServerRequestOutcome;
    if (answer.kind === "approval") {
      if (!APPROVAL_REQUEST_METHODS.has(method)) throw new RuntimeError("INVALID_REQUEST", `Request ${method} does not take an approval verdict`);
      outcome = { result: approvalDecision(method, answer.verdict, pending.request.params) };
    } else if (answer.kind === "userInput") {
      if (method !== USER_INPUT_METHOD) throw new RuntimeError("INVALID_REQUEST", `Request ${method} does not take user input`);
      outcome = { result: { answers: structuredClone(answer.answers) } };
    } else if (answer.kind === "elicitation") {
      if (method !== ELICITATION_METHOD) throw new RuntimeError("INVALID_REQUEST", `Request ${method} does not take an elicitation action`);
      outcome = { result: { action: answer.action, content: answer.action === "accept" ? answer.content ?? null : null, _meta: null } };
    } else throw new RuntimeError("INVALID_REQUEST", "Unknown request answer kind");
    entry.pending.delete(requestId);
    pending.settle(outcome);
    this.push(entry, { type: "request-resolved", providerThreadId: entry.threadId, providerTurnId: entry.turnId ?? "", requestId, method, outcome: "answered", decision: "result" in outcome ? outcome.result : undefined, decidedBy: "user", occurredAt: new Date().toISOString() });
    return { sent: true };
  }

  // Wiring to the host.
  private push(entry: Entry, event: DelegatedTurnProgressEvent): void {
    if (entry.turnId === undefined) { entry.deferred.push(event); return; }
    entry.progress.push(event);
    const limit = this.options.maxQueuedProgress ?? 100_000;
    if (entry.progress.length > limit) { entry.progress.splice(0, entry.progress.length - limit); this.logger.warn("codex.progress.dropped", { workerId: entry.handle.workerId }); }
  }
  private entryForThread(threadId: unknown): Entry | undefined {
    if (typeof threadId !== "string") return undefined;
    let current: string = threadId;
    const visited = new Set<string>();
    while (!visited.has(current)) {
      visited.add(current);
      const entry = this.byThread.get(current);
      if (entry) return entry;
      const parent = this.childThreads.get(current);
      if (!parent) return undefined;
      current = parent;
    }
    return undefined;
  }
  private handleNotification(notification: CodexNotification): void {
    const params = record(notification.params);
    const method = notification.method;
    if (method === "thread/started") {
      const thread = record(params.thread);
      if (typeof thread.parentThreadId === "string" && typeof thread.id === "string") {
        this.childThreads.set(thread.id, thread.parentThreadId);
        if (record(thread.status).type === "active") this.activeChildren.add(thread.id);
      }
    }
    if (typeof params.threadId === "string") {
      if (method === "thread/closed") {
        this.closedThreads.add(params.threadId); this.threads.delete(params.threadId);
        this.activeChildren.delete(params.threadId); this.cancelChildTools(params.threadId); this.childTurns.delete(params.threadId); this.closeWaiters.get(params.threadId)?.();
      }
      if (this.childThreads.has(params.threadId)) {
        if (method === "turn/started" || (method === "thread/status/changed" && record(params.status).type === "active")) this.activeChildren.add(params.threadId);
        if (method === "turn/completed" || (method === "thread/status/changed" && ["idle", "systemError", "notLoaded"].includes(String(record(params.status).type)))) this.activeChildren.delete(params.threadId);
      }
    }
    const entry = this.entryForThread(params.threadId ?? record(params.thread).id ?? record(params.thread).parentThreadId);
    if (entry === undefined) return;
    if (entry.application && !entry.application.finished && this.childThreads.has(String(params.threadId))) {
      const childId = String(params.threadId);
      if (method === "turn/started" && typeof record(params.turn).id === "string" && (this.childTurns.get(childId)?.turnId !== record(params.turn).id || this.childTurns.get(childId)?.owner !== entry)) {
        this.cancelChildTools(childId);
        this.childTurns.set(childId, { turnId: record(params.turn).id as string, owner: entry });
      }
      if ((method === "turn/completed" && this.childTurns.get(childId)?.turnId === record(params.turn).id) || (method === "thread/status/changed" && ["idle", "systemError", "notLoaded"].includes(String(record(params.status).type)))) {
        this.cancelChildTools(childId); this.childTurns.delete(childId);
      }
    }
    const occurredAt = new Date().toISOString();
    this.push(entry, { type: "notification", providerThreadId: entry.threadId, providerTurnId: entry.turnId ?? "", method, params: notification.params, occurredAt });
    if (method === "item/agentMessage/delta" && params.threadId === entry.threadId && typeof params.delta === "string" && params.delta.length > 0) {
      const itemId = String(params.itemId ?? "");
      entry.emittedByItem.set(itemId, (entry.emittedByItem.get(itemId) ?? 0) + params.delta.length);
      entry.text += params.delta;
      this.push(entry, { type: "text", providerThreadId: entry.threadId, providerTurnId: entry.turnId ?? "", text: params.delta });
      return;
    }
    if (method === "item/completed" && params.threadId === entry.threadId) {
      const item = record(params.item);
      if (item.type === "agentMessage" && typeof item.text === "string") {
        const emitted = entry.emittedByItem.get(String(item.id ?? "")) ?? 0;
        if (item.text.length > emitted) {
          const rest = item.text.slice(emitted);
          entry.emittedByItem.set(String(item.id ?? ""), item.text.length);
          entry.text += rest;
          this.push(entry, { type: "text", providerThreadId: entry.threadId, providerTurnId: entry.turnId ?? "", text: rest });
        }
      } else if (item.type === "plan" && entry.envelope.interactionMode === "native-plan" && entry.envelope.sessionId) {
        entry.nativePlanEvents.push({ projectId: entry.envelope.projectId, sessionId: entry.envelope.sessionId, clientTurnId: entry.envelope.clientTurnId, providerThreadId: entry.threadId, providerTurnId: entry.turnId ?? "", eventId: String(item.id ?? randomUUID()), occurredAt, plan: typeof item.text === "string" ? item.text : structuredClone(item) });
      }
      return;
    }
    if (method === "serverRequest/resolved") {
      if (typeof params.requestId === "string" || typeof params.requestId === "number") {
        const call = entry.application?.pending.get(JSON.stringify([typeof params.requestId, params.requestId]));
        if (call && call.threadId === params.threadId) call.cancel();
      }
      const requestId = params.requestId === undefined ? undefined : String(params.requestId);
      const pending = requestId === undefined ? undefined : entry.pending.get(requestId);
      if (pending && requestId !== undefined) {
        entry.pending.delete(requestId);
        pending.settle(cancelOutcome(pending.request.method));
        this.push(entry, { type: "request-resolved", providerThreadId: entry.threadId, providerTurnId: entry.turnId ?? "", requestId, method: pending.request.method, outcome: "cancelled", decidedBy: "runtime", occurredAt });
      }
      return;
    }
    if (method === "turn/started" && params.threadId === entry.threadId && typeof record(params.turn).id === "string") this.adoptTurn(entry, record(params.turn).id as string);
    if (method === "turn/completed" && params.threadId === entry.threadId) {
      const turn = record(params.turn);
      if (typeof turn.id === "string") this.adoptTurn(entry, turn.id);
      if (turn.id !== entry.turnId) return;
      const unobservedChildren = [...this.activeChildren].filter(childId => this.entryForThread(childId) === entry);
      if (unobservedChildren.length) this.push(entry, { type: "notification", providerThreadId: entry.threadId, providerTurnId: entry.turnId ?? "",
        method: "chirality/nativeChildren/observationEnded", params: { threadId: entry.threadId, turnId: entry.turnId,
          agentThreadIds: unobservedChildren, reason: "parentTurnEnded", message: "These children were still active when the primary turn ended. Later child activity is not captured by this turn observer." }, occurredAt });
      this.cancelPending(entry, "cancelled");
      const status = String(turn.status);
      if (status === "completed") entry.settle({ worker: { ...entry.handle, state: "exited" }, exitCode: 0, signal: null, threadId: entry.threadId, stdout: entry.text, stderr: "" });
      else if (status === "interrupted") entry.settle({ worker: { ...entry.handle, state: "exited" }, exitCode: null, signal: "SIGTERM", threadId: entry.threadId, stdout: entry.text, stderr: "" });
      else {
        const error = record(turn.error);
        entry.settle(this.failedResult(entry, typeof error.message === "string" ? error.message : `turn ${status}`));
      }
    }
  }
  private failedResult(entry: Entry, reason: string): WorkerResult {
    return { worker: { ...entry.handle, state: "exited" }, exitCode: 1, signal: null, threadId: entry.threadId, stdout: entry.text, stderr: reason.slice(0, 4096) };
  }
  private cancelPending(entry: Entry, outcome: Extract<ServerRequestOutcome, "cancelled" | "failed">): void {
    for (const [requestId, pending] of entry.pending) {
      entry.pending.delete(requestId);
      pending.settle(cancelOutcome(pending.request.method));
      this.push(entry, { type: "request-resolved", providerThreadId: entry.threadId, providerTurnId: entry.turnId ?? "", requestId, method: pending.request.method, outcome, decidedBy: "runtime", occurredAt: new Date().toISOString() });
    }
  }
  private handleExit(exit: CodexAppServerExit, generation: number): void {
    this.providerExitEpoch += 1;
    for (const ownership of this.applicationOwnerships) if (ownership.hostGeneration === generation) this.finishApplication(ownership, "provider exited");
    this.childTurns.clear();
    this.activeChildren.clear(); this.childThreads.clear(); this.closedThreads.clear(); this.pendingUnloads.clear();
    for (const finish of this.closeWaiters.values()) finish();
    const reason = `codex app-server exited during the turn (code ${exit.code ?? "null"}, signal ${exit.signal ?? "null"})`;
    for (const entry of this.entries.values()) {
      if (entry.hostGeneration !== generation || entry.settled) continue;
      this.cancelPending(entry, "failed");
      this.push(entry, { type: "notification", providerThreadId: entry.threadId, providerTurnId: entry.turnId ?? "", method: "chirality/appServer/exited", params: { code: exit.code, signal: exit.signal }, occurredAt: new Date().toISOString() });
      entry.settle(this.failedResult(entry, reason));
    }
  }
  private finishApplication(ownership: ApplicationOwnership | undefined, reason: string): void {
    if (!ownership || ownership.finished) return;
    ownership.finished = true;
    ownership.removeAbortListener?.();
    this.applicationOwnerships.delete(ownership);
    for (const [threadId, child] of this.childTurns) if (child.owner.application === ownership) this.childTurns.delete(threadId);
    for (const pending of ownership.pending.values()) pending.cancel();
    this.options.applicationTools!.finishTurn(ownership.envelope.projectId, ownership.envelope.sessionId!, ownership.envelope.clientTurnId, reason);
  }
  private cancelChildTools(threadId: string): void {
    for (const ownership of this.applicationOwnerships) {
      for (const pending of ownership.pending.values()) if (pending.threadId === threadId) pending.cancel();
    }
  }
  private async handleApplicationTool(request: CodexServerRequest): Promise<CodexServerRequestOutcome> {
    const params = record(request.params);
    const entry = this.entryForThread(params.threadId);
    const providerThreadId = typeof params.threadId === "string" ? params.threadId : "";
    const providerTurnId = typeof params.turnId === "string" ? params.turnId : "";
    const evidence = { providerThreadId, providerTurnId, requestId: String(request.id), method: request.method };
    if (entry) this.push(entry, { type: "request", ...evidence, params: request.params, occurredAt: new Date().toISOString() });
    const resolved = (result: unknown, outcome: ServerRequestOutcome = "answered") => {
      if (entry) this.push(entry, { type: "request-resolved", ...evidence, outcome, decision: result, decidedBy: "runtime", occurredAt: new Date().toISOString() });
      return { result };
    };
    const failure = (text: string) => ({ success: false, contentItems: [{ type: "inputText", text }] });
    const ownership = entry?.application;
    if (!entry || !ownership || !this.options.applicationTools) return resolved(failure(this.options.applicationTools ? "No active application tool binding" : "Chirality registers no dynamic tools"));
    if ((typeof request.id !== "string" && (typeof request.id !== "number" || !Number.isFinite(request.id))) || !providerThreadId || !providerTurnId || typeof params.callId !== "string" || !params.callId || typeof params.tool !== "string" || !params.tool || (params.namespace !== null && typeof params.namespace !== "string") || !Object.hasOwn(params, "arguments")) return resolved(failure("Malformed application tool request"));
    try { canonicalApplicationJson(params.arguments); } catch { return resolved(failure("Malformed application tool arguments")); }
    const knownTool = ownership.tools.some(spec => spec.type === "function" ? params.namespace === null && spec.name === params.tool : spec.name === params.namespace && spec.tools.some(tool => tool.name === params.tool));
    if (!knownTool) return resolved(failure("Unknown application tool"));
    const key = JSON.stringify([typeof request.id, request.id]);
    const callKey = JSON.stringify([providerThreadId, providerTurnId, params.callId]);
    if (ownership.seen.has(key) || ownership.seen.has(callKey)) return resolved(failure("Duplicate application tool request"));
    ownership.seen.add(key); ownership.seen.add(callKey);
    return new Promise<CodexServerRequestOutcome>(resolve => {
      let done = false;
      const finish = (result: unknown, outcome: ServerRequestOutcome = "answered") => {
        if (done) return;
        done = true; ownership.pending.delete(key); resolve(resolved(result, outcome));
      };
      const callInput: ApplicationToolCall = { bindingId: ownership.binding.bindingId,
        runtimeProjectId: entry.envelope.projectId, runtimeSessionId: entry.envelope.sessionId!, runtimeTurnId: entry.envelope.clientTurnId,
        providerThreadId, providerTurnId, requestId: request.id, callId: params.callId as string,
        namespace: params.namespace as string | null, tool: params.tool as string, arguments: params.arguments as ApplicationJson
      };
      ownership.pending.set(key, { threadId: providerThreadId, turnId: providerTurnId, cancel: () => {
        this.options.applicationTools!.cancelCall(callInput, "provider call cancelled");
        finish(failure("Application tool call cancelled"), "cancelled");
      } });
      // Reserve cancellation ownership before awaiting provider identity: a
      // resolved request or terminal may arrive while turn/start is in flight.
      const dispatch = async () => {
        if (entry.turnId === undefined) await entry.turnIdReady;
        if (done) return;
        const child = this.childTurns.get(providerThreadId);
        const correctTurn = providerThreadId === entry.threadId ? providerTurnId === entry.turnId : child?.owner === entry && child.turnId === providerTurnId;
        if (ownership.finished || entry.settled || entry.application !== ownership || entry.hostGeneration !== this.options.host.generation || !correctTurn) {
          ownership.seen.delete(key); ownership.seen.delete(callKey);
          finish(failure("Foreign or stale application tool request"));
          return;
        }
        finish(await this.options.applicationTools!.call(callInput));
      };
      void dispatch().catch(() => finish(failure("Application tool call failed"), "failed"));
    });
  }
  private async handleServerRequest(request: CodexServerRequest): Promise<CodexServerRequestOutcome> {
    if (request.method === DYNAMIC_TOOL_METHOD) return this.handleApplicationTool(request);
    const params = record(request.params);
    const method = request.method;
    const requestId = String(request.id);
    const entry = this.entryForThread(params.threadId ?? params.conversationId);
    const occurredAt = new Date().toISOString();
    const resolved = (outcome: ServerRequestOutcome, decision: unknown, decidedBy: ServerRequestDecider): void => {
      if (entry) this.push(entry, { type: "request-resolved", providerThreadId: entry.threadId, providerTurnId: entry.turnId ?? "", requestId, method, outcome, ...(decision === undefined ? {} : { decision }), decidedBy, occurredAt: new Date().toISOString() });
    };
    if (entry) this.push(entry, { type: "request", providerThreadId: entry.threadId, providerTurnId: entry.turnId ?? "", requestId, method, params: request.params, occurredAt });
    const answerable = APPROVAL_REQUEST_METHODS.has(method) || method === USER_INPUT_METHOD || method === ELICITATION_METHOD;
    if (!answerable || entry === undefined) {
      if (UNSUPPORTED_METHODS.has(method) || !answerable) this.logger.warn("codex.server-request.unsupported", { method, id: request.id });
      else this.logger.warn("codex.server-request.no_live_turn", { method, id: request.id });
      resolved("unsupported", undefined, "runtime");
      return { error: { code: JSON_RPC_METHOD_NOT_FOUND, message: "unsupported request" } };
    }
    const itemId = typeof params.itemId === "string" ? params.itemId : typeof params.callId === "string" ? params.callId : undefined;
    return new Promise<CodexServerRequestOutcome>(settle => {
      entry.pending.set(requestId, { request: { requestId, method, params: structuredClone(request.params), ...(itemId === undefined ? {} : { itemId }), receivedAt: occurredAt }, settle });
    });
  }
}

function approvalDecision(method: string, verdict: "allow" | "deny" | "allowForSession", params: unknown): unknown {
  if (method === "execCommandApproval" || method === "applyPatchApproval") {
    return { decision: verdict === "allow" ? "approved" : verdict === "allowForSession" ? "approved_for_session" : { denied: { rejection: "Declined by the user in Chirality" } } };
  }
  if (method === "item/permissions/requestApproval") {
    const requested = record(record(params).permissions);
    return verdict === "deny" ? { permissions: {}, scope: "turn" } : { permissions: structuredClone(requested), scope: verdict === "allowForSession" ? "session" : "turn" };
  }
  return { decision: verdict === "allow" ? "accept" : verdict === "allowForSession" ? "acceptForSession" : "decline" };
}
function cancelOutcome(method: string): CodexServerRequestOutcome {
  if (method === "execCommandApproval" || method === "applyPatchApproval") return { result: { decision: "abort" } };
  if (method === "item/permissions/requestApproval") return { result: { permissions: {}, scope: "turn" } };
  if (method === USER_INPUT_METHOD) return { result: { answers: {} } };
  if (method === ELICITATION_METHOD) return { result: { action: "cancel", content: null, _meta: null } };
  return { result: { decision: "cancel" } };
}
