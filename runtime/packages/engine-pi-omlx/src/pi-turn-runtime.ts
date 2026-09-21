import { createHash, randomUUID } from "node:crypto";
import { realpath } from "node:fs/promises";
import { isAbsolute, relative, resolve, sep, join } from "node:path";
import type { AgentSession, SessionManager, ToolDefinition } from "@earendil-works/pi-coding-agent";
import type { AssistantMessage, Context, Model, SimpleStreamOptions } from "@earendil-works/pi-ai";
import { HarnessError, type AgentEngineRunInput, type UIEvent, type RuntimeToolDefinition, type ContextSuccessorRequest, type PreparedContextSuccessor } from "@chirality/runtime-contracts";
import type { PiTurnRuntimePort } from "./pi-omlx-engine.js";
import { normalizeOmlxBaseUrl } from "./omlx-client.js";
import { createPiReadTool, createBoundPiReadTool } from "./pi-read-tool.js";
import { mapPiEvent } from "./pi-event-mapper.js";
// Keep both SDKs behind Node's native ESM loader. Nonliteral specifiers prevent a
// CommonJS consumer bundle from rewriting their import-only exports to require()
// or bundling a second copy of Pi's provider/model state. Do not inline these.
const codingAgentSpecifier = "@earendil-works/pi-coding-agent";
const piAiSpecifier = "@earendil-works/pi-ai";
async function loadPiSdk() {
  const [agent, ai] = await Promise.all([
    import(codingAgentSpecifier) as Promise<typeof import("@earendil-works/pi-coding-agent")>,
    import(piAiSpecifier) as Promise<typeof import("@earendil-works/pi-ai")>
  ]);
  return { ...agent, ...ai };
}
export interface PiTurnRuntimeOptions {
  baseUrl: string; model: { id: string; contextWindow: number; maxTokens: number }; canonicalRoot: string;
  maxSessions?: number; sessionTtlMs?: number;
  compaction?: { reserveTokens: number; keepRecentTokens: number };
  protectedPaths?: readonly string[]; systemPrompt?: string; turnTimeoutMs?: number; maxOutputBytes?: number; fetchImpl?: typeof fetch;
}
const failure = (message: string) => new HarnessError("PROVIDER_PROTOCOL_FAILURE", 502, message);
const inside = (root: string, path: string) => { const rel = relative(root, path); return rel === "" || (rel !== ".." && !rel.startsWith(`..${sep}`) && !isAbsolute(rel)); };
const object = (value: unknown): Record<string, any> => { if (!value || typeof value !== "object" || Array.isArray(value)) throw failure("Malformed local model response"); return value as Record<string, any>; };
const sameNames = (left: readonly string[], right: readonly string[]) => left.length === right.length && left.every(name => right.includes(name));
const admittedRuntimeTool = (tool: RuntimeToolDefinition) => tool.permission.effect === "allow" && (
  tool.permission.operation === "read" && /^chirality_[a-z0-9_]+$/u.test(tool.name) ||
  tool.permission.operation === "control" && tool.name === "chirality_request_method_change"
);
function createRuntimeTool(tool: RuntimeToolDefinition, signal: AbortSignal): ToolDefinition {
  if (!admittedRuntimeTool(tool)) throw new HarnessError("INVALID_REQUEST", 403, "Pi runtime tools must be admitted Chirality read callbacks or the exact method-change control callback");
  return {
    name: tool.name,
    label: tool.name,
    description: tool.description,
    parameters: tool.inputSchema as never,
    async execute(_id, input, callSignal) {
      const combined = callSignal ? AbortSignal.any([signal, callSignal]) : signal;
      const value = await tool.execute(input, combined);
      return { content: [{ type: "text", text: JSON.stringify(value) }], details: { source: "runtime-method-callback" } };
    }
  };
}
function abortable<T>(pending: Promise<T>, signal: AbortSignal): Promise<T> {
  return new Promise<T>((resolveValue, reject) => {
    const aborted = () => reject(failure("Pi operation aborted"));
    if (signal.aborted) { void pending.catch(() => {}); aborted(); return; }
    signal.addEventListener("abort", aborted, { once: true });
    pending.then(resolveValue, reject).finally(() => signal.removeEventListener("abort", aborted)).catch(() => {});
  });
}
function messages(context: Context, exactSystemPrompt?: string): unknown[] {
  const system = exactSystemPrompt ?? context.systemPrompt;
  const result: unknown[] = system ? [{ role: "system", content: system }] : [];
  const text = (content: unknown): string => {
    if (typeof content === "string") return content;
    if (!Array.isArray(content) || content.some(item => !item || item.type !== "text" || typeof item.text !== "string")) throw failure("Unsupported Pi message content");
    return content.map(item => item.text).join("");
  };
  for (const message of context.messages) {
    if (message.role === "user") result.push({ role: "user", content: text(message.content) });
    else if (message.role === "toolResult") result.push({ role: "tool", tool_call_id: message.toolCallId, content: text(message.content) });
    else {
      const calls = message.content.filter(item => item.type === "toolCall");
      result.push({ role: "assistant", content: message.content.filter(item => item.type === "text").map(item => item.text).join(""), ...(calls.length ? { tool_calls: calls.map(call => ({ id: call.id, type: "function", function: { name: call.name, arguments: JSON.stringify(call.arguments) } })) } : {}) });
    }
  }
  return result;
}
/** Real Pi orchestration with an explicit, bounded OpenAI-compatible local provider transport. */
export interface PiRuntimePort extends PiTurnRuntimePort {
  toolBindings: { bind(sessionId: string, tools: readonly RuntimeToolDefinition[]): Promise<() => Promise<void>> };
  close(): Promise<void>;
}
export function createPiTurnRuntime(inputOptions: PiTurnRuntimeOptions): PiRuntimePort {
  const options = { ...inputOptions, model: { ...inputOptions.model }, protectedPaths: [...(inputOptions.protectedPaths ?? [])] };
  const baseUrl = normalizeOmlxBaseUrl(options.baseUrl), fetchImpl = options.fetchImpl ?? globalThis.fetch.bind(globalThis);
  const timeoutMs = options.turnTimeoutMs ?? 60000, maxBytes = options.maxOutputBytes ?? 1048576;
  if (!options.model.id || ![options.model.contextWindow, options.model.maxTokens, timeoutMs, maxBytes].every(value => Number.isSafeInteger(value) && value > 0) || options.model.maxTokens > options.model.contextWindow || timeoutMs > 600000 || maxBytes > 16777216) throw new HarnessError("INVALID_REQUEST", 400, "Explicit bounded Pi model configuration required");
  const compaction = { enabled: true, reserveTokens: options.compaction?.reserveTokens ?? Math.max(1, Math.min(options.model.maxTokens, Math.floor(options.model.contextWindow / 4))), keepRecentTokens: options.compaction?.keepRecentTokens ?? Math.max(1, Math.floor(options.model.contextWindow / 4)) };
  if (![compaction.reserveTokens, compaction.keepRecentTokens].every(value => Number.isSafeInteger(value) && value > 0 && value < options.model.contextWindow)) throw new HarnessError("INVALID_REQUEST", 400, "Explicit compaction bounds must fit the model context");
  const active = new Map<string, { controller: AbortController; session?: AgentSession; interrupted: boolean }>();
  const maxSessions = options.maxSessions ?? 32, sessionTtlMs = options.sessionTtlMs ?? 1800000;
  if (!Number.isSafeInteger(maxSessions) || maxSessions < 1 || maxSessions > 128 || !Number.isSafeInteger(sessionTtlMs) || sessionTtlMs < 1 || sessionTtlMs > 86400000) throw new HarnessError("INVALID_REQUEST", 400, "Invalid Pi session cache bounds");
  const histories = new Map<string, { manager?: SessionManager; fingerprint: string; lastUsed: number; engineSessionId: string; providerSpanId: string }>();
  const preparations = new Map<string, PreparedContextSuccessor>();
  const retired = new Set<string>();
  const bindings = new Map<string, { id: string; tool: RuntimeToolDefinition }>();
  const releasedBindings = new Set<string>();
  let closed = false;
  const invalidate = (sessionId: string) => { histories.delete(sessionId); retired.add(sessionId); };
  const expire = () => { for (const [id, value] of histories) if (!active.has(id) && Date.now() - value.lastUsed >= sessionTtlMs) invalidate(id); };
  const fingerprint = (input: AgentEngineRunInput, credential: string, bindingId?: string) => createHash("sha256").update(JSON.stringify({
    root: options.canonicalRoot, model: options.model, tools: input.opts.tools, maxTurns: input.opts.maxTurns, agentType: input.session.agentType, childKind: input.session.childKind, orchestrationRunId: input.session.orchestrationRunId, persona: input.opts.persona, mode: input.opts.mode,
    credentialHash: createHash("sha256").update(credential).digest("hex"), bindingId: bindingId ?? null, protectedPaths: options.protectedPaths,
    systemPrompt: options.systemPrompt ?? null, parentSessionId: input.session.parentSessionId, parentInstanceId: input.session.parentInstanceId,
    instructionHash: input.session.instructionHash, briefHash: input.session.briefHash, declaredContext: input.session.declaredContext,
    declaredTools: input.session.declaredTools, allowedWriteTargets: input.session.allowedWriteTargets, approvalRef: input.session.approvalRef,
    bootFingerprint: input.session.bootFingerprint, runtimeFingerprint: input.session.runtimeFingerprint,
    instructionContextSha256: input.instructionContext?.basisPreview.sha256,
    runtimeTools: input.runtimeTools?.map(tool => ({ name: tool.name, permission: tool.permission, inputSchema: tool.inputSchema }))
  })).digest("hex");
  const admittedSuccessor = (input: AgentEngineRunInput, previous?: { engineSessionId: string }) => {
    const successor = input.contextSuccessor;
    const admitted = successor === undefined ? undefined : preparations.get(successor.preparationId);
    return successor !== undefined && admitted !== undefined && JSON.stringify(admitted) === JSON.stringify(successor) && previous?.engineSessionId === successor.predecessorEngineSessionId && successor.adapterId === "pi" && successor.providerId === "omlx" && successor.targetBasisId === input.instructionContext?.basisPreview.id && successor.continuationSha256 === createHash("sha256").update(successor.continuationText).digest("hex");
  };
  async function preflight(input: AgentEngineRunInput, credential: string): Promise<void> {
    if (closed) throw new HarnessError("ENGINE_UNAVAILABLE", 503, "Pi runtime is closed");
    expire();
    if (retired.has(input.session.sessionId) || releasedBindings.has(input.session.sessionId)) throw new HarnessError("INVALID_REQUEST", 409, "Pi context expired or was revoked; create a fresh Runtime session");
    if ((input.session.parentSessionId || input.session.childKind || input.session.orchestrationRunId) && !bindings.has(input.session.sessionId)) throw new HarnessError("INVALID_REQUEST", 403, "Governed Pi child requires its bound Runtime read callback");
    const previous = histories.get(input.session.sessionId);
    if (previous && previous.fingerprint !== fingerprint(input, credential, bindings.get(input.session.sessionId)?.id) && !admittedSuccessor(input, previous)) throw new HarnessError("INVALID_REQUEST", 409, "Pi scope/account context changed without an admitted successor");
    if (!previous && (histories.size >= maxSessions || retired.size >= 1024)) throw new HarnessError("ENGINE_UNAVAILABLE", 503, "Pi session cache capacity reached");
    if (!credential?.trim() || input.session.agentType !== 2 || input.opts.tools.length !== 1 || !["read", "read_file"].includes(input.opts.tools[0]!) || input.runtimeTools?.some(tool => !admittedRuntimeTool(tool)) || input.opts.model !== options.model.id || input.session.projectRoot !== options.canonicalRoot || await realpath(options.canonicalRoot) !== options.canonicalRoot || input.contentBlocks?.length || !Number.isSafeInteger(input.opts.maxTurns) || input.opts.maxTurns < 1 || input.opts.maxTurns > 100) throw new HarnessError("INVALID_REQUEST", 403, "Pi requires explicit Agent2/read-only/model/root pilot binding with only admitted Runtime callbacks");
    if (active.has(input.session.sessionId)) throw new HarnessError("TURN_IN_PROGRESS", 409, "Pi session turn is already running");
  }
  return {
    async prepareContextSuccessor(request: ContextSuccessorRequest) {
      const history = histories.get(request.sessionId);
      if (closed || active.has(request.sessionId) || history === undefined || history.engineSessionId !== request.predecessorEngineSessionId || request.continuationContext.sha256 !== createHash("sha256").update(request.continuationContext.transcript).digest("hex")) throw new HarnessError("INVALID_REQUEST", 409, "Pi predecessor span or continuation evidence is unavailable");
      const prepared: PreparedContextSuccessor = { preparationId: randomUUID(), adapterId: "pi", providerId: "omlx", predecessorEngineSessionId: history.engineSessionId, continuationText: request.continuationContext.transcript, continuationSha256: request.continuationContext.sha256, targetBasisId: request.toBasisPreview.id, targetReference: `${request.toBasisPreview.id}:${request.toBasisPreview.sha256}` };
      preparations.set(prepared.preparationId, prepared);
      return prepared;
    },
    async cancelContextSuccessor(preparationId: string) { preparations.delete(preparationId); },
    toolBindings: {
      async bind(sessionId, tools) {
        if (closed || !sessionId || active.has(sessionId) || histories.has(sessionId) || bindings.has(sessionId) || releasedBindings.has(sessionId) || tools.length !== 1 || bindings.size + releasedBindings.size >= 1024) throw new HarnessError("INVALID_REQUEST", 403, "Pi tool binding requires a fresh bounded session");
        const source = tools[0]!;
        const tool: RuntimeToolDefinition = { name: source.name, description: source.description, inputSchema: structuredClone(source.inputSchema), permission: structuredClone(source.permission), execute: source.execute };
        const entry = { id: randomUUID(), tool };
        // Validate the closed coordinator schema/scope before retaining a callback.
        createBoundPiReadTool({ canonicalRoot: options.canonicalRoot, tool, protectedPaths: options.protectedPaths, isCurrent: () => true, signal: new AbortController().signal });
        bindings.set(sessionId, entry);
        let released = false;
        return async () => { if (released) return; released = true; if (bindings.get(sessionId) === entry) bindings.delete(sessionId); releasedBindings.add(sessionId); invalidate(sessionId); const state = active.get(sessionId); if (state) { state.interrupted = true; state.controller.abort(); await state.session?.abort(); } };
      }
    },
    async close() { closed = true; for (const state of active.values()) { state.interrupted = true; state.controller.abort(); } await Promise.allSettled([...active.values()].map(state => state.session?.abort())); histories.clear(); bindings.clear(); preparations.clear(); },
    preflight,
    async interrupt(sessionId) { const state = active.get(sessionId); if (state) { state.interrupted = true; state.controller.abort(); await state.session?.abort(); } },
    async *startTurn(input, execution) {
      // Retain the admitted request while native SDK loading yields to callers.
      const runtimeTools = input.runtimeTools;
      const cloneableInput = { ...input, runtimeTools: undefined };
      input = { ...structuredClone(cloneableInput), ...(runtimeTools === undefined ? {} : { runtimeTools }) };
      execution = { ...execution };
      await preflight(input, execution.credential);
      if (execution.disableBuiltIns !== true || execution.disableAmbientResources !== true || !isAbsolute(execution.transcriptRoot) || resolve(execution.transcriptRoot) !== execution.transcriptRoot || inside(options.canonicalRoot, execution.transcriptRoot) || inside(execution.transcriptRoot, options.canonicalRoot)) throw new HarnessError("INVALID_REQUEST", 403, "Pi requires disabled ambient resources and external Runtime-owned transcript storage");
      // Recheck mutable admissions synchronously after the awaited filesystem preflight.
      if (closed || retired.has(input.session.sessionId) || releasedBindings.has(input.session.sessionId)) throw new HarnessError("INVALID_REQUEST", 409, "Pi context revoked; create a fresh Runtime session");
      const binding = bindings.get(input.session.sessionId);
      if ((input.session.parentSessionId || input.session.childKind || input.session.orchestrationRunId) && !binding) throw new HarnessError("INVALID_REQUEST", 403, "Governed Pi child requires its bound Runtime read callback");
      if (active.has(input.session.sessionId)) throw new HarnessError("TURN_IN_PROGRESS", 409, "Pi session turn is already running");
      let history = histories.get(input.session.sessionId);
      const successorAdmitted = admittedSuccessor(input, history);
      if (history && history.fingerprint !== fingerprint(input, execution.credential, binding?.id) && !successorAdmitted) throw new HarnessError("INVALID_REQUEST", 409, "Pi scope/account context changed without an admitted successor");
      if (successorAdmitted) { histories.delete(input.session.sessionId); history = undefined; preparations.delete(input.contextSuccessor!.preparationId); }
      if (!history && (histories.size >= maxSessions || retired.size >= 1024)) throw new HarnessError("ENGINE_UNAVAILABLE", 503, "Pi session cache capacity reached");
      if (!history) { history = { fingerprint: fingerprint(input, execution.credential, binding?.id), lastUsed: Date.now(), engineSessionId: `pi-${randomUUID()}`, providerSpanId: randomUUID() }; histories.set(input.session.sessionId, history); }
      const state: { controller: AbortController; session?: AgentSession; interrupted: boolean } = { controller: new AbortController(), interrupted: false };
      if (active.has(input.session.sessionId)) throw new HarnessError("TURN_IN_PROGRESS", 409, "Pi session turn is already running");
      active.set(input.session.sessionId, state);
      const admittedToolNames = [...input.opts.tools, ...(input.runtimeTools ?? []).map(tool => tool.name)];
      let wake: (() => void) | undefined, done = false, problem: unknown, bytes = 0, calls = 0;
      const queue: UIEvent[] = [];
      const enqueue = (event: UIEvent) => { bytes += Buffer.byteLength(JSON.stringify(event)); if (bytes > maxBytes || queue.length >= 4096) throw failure("Pi output budget exceeded"); queue.push(event); wake?.(); };
      const timer = setTimeout(() => { problem = failure("Pi turn deadline exceeded"); state.controller.abort(); void state.session?.abort(); wake?.(); }, timeoutMs);
      let unsubscribe: (() => void) | undefined;
      const run = (async () => {
        try {
          const { createAgentSession, DefaultResourceLoader, ModelRuntime, SessionManager, SettingsManager, createAssistantMessageEventStream, InMemoryCredentialStore, InMemoryModelsStore } = await abortable(loadPiSdk(), state.controller.signal);
          // The reservation counts toward capacity even before the SDK exists.
          const sessionManager = history.manager ??= SessionManager.inMemory(options.canonicalRoot, { id: input.session.sessionId });
          const streamSimple = (model: Model<any>, context: Context, requestOptions?: SimpleStreamOptions) => {
            const stream = createAssistantMessageEventStream();
            const message: AssistantMessage = { role: "assistant", content: [], api: "openai-completions", provider: "omlx", model: options.model.id, usage: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0, totalTokens: 0, cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0, total: 0 } }, stopReason: "stop", timestamp: Date.now() };
            void (async () => {
              try {
                if (++calls > input.opts.maxTurns || model.id !== options.model.id || model.provider !== "omlx" || model.baseUrl !== baseUrl) throw failure("Pi model request escaped its configured bound");
                if (context.tools && !sameNames(context.tools.map(tool => tool.name), admittedToolNames)) throw failure("Pi exposed unexpected tools");
                const signal = requestOptions?.signal ? AbortSignal.any([state.controller.signal, requestOptions.signal]) : state.controller.signal;
                const requestedTokens = requestOptions?.maxTokens ?? options.model.maxTokens;
                if (!Number.isSafeInteger(requestedTokens) || requestedTokens < 1) throw failure("Invalid local model token request");
                const body = JSON.stringify({ model: options.model.id, messages: messages(context, systemPrompt), stream: false, max_tokens: Math.min(options.model.maxTokens, requestedTokens), ...(context.tools?.length ? { tools: context.tools.map(tool => ({ type: "function", function: { name: tool.name, description: tool.description, parameters: tool.parameters } })) } : {}) });
                if (Buffer.byteLength(body) > maxBytes) throw failure("Pi request budget exceeded");
                const response = await abortable(fetchImpl(`${baseUrl}/chat/completions`, { method: "POST", redirect: "manual", headers: { "content-type": "application/json", authorization: `Bearer ${execution.credential}` }, body, signal }), signal);
                if (response.status === 401 || response.status === 403) throw new HarnessError("PROVIDER_AUTH_FAILURE", 401, "Local model credential was rejected");
                if (!response.ok || (response.url && response.url !== `${baseUrl}/chat/completions`) || !response.body) throw failure("Local model request was rejected or redirected");
                const reader = response.body.getReader(); let length = 0; const chunks: Uint8Array[] = [];
                try { for (;;) { const part = await abortable(reader.read(), signal); if (part.done) break; length += part.value.length; if (length > maxBytes) throw failure("Local model response budget exceeded"); chunks.push(part.value); } } finally { void reader.cancel().catch(() => {}); }
                const payload = object(JSON.parse(Buffer.concat(chunks).toString("utf8")));
                if (payload.model !== options.model.id || !Array.isArray(payload.choices) || payload.choices.length !== 1) throw failure("Local model response identity/choice mismatch");
                const choice = object(payload.choices[0]), answer = object(choice.message);
                if (answer.role !== "assistant" || !["stop", "length", "tool_calls"].includes(choice.finish_reason) || (answer.content !== null && typeof answer.content !== "string" && !(answer.content === undefined && choice.finish_reason === "tool_calls" && Array.isArray(answer.tool_calls) && answer.tool_calls.length > 0))) throw failure("Unsupported local model answer");
                stream.push({ type: "start", partial: message });
                if (typeof answer.content === "string" && answer.content) { const index = message.content.length; message.content.push({ type: "text", text: answer.content }); stream.push({ type: "text_start", contentIndex: index, partial: message }); stream.push({ type: "text_delta", contentIndex: index, delta: answer.content, partial: message }); stream.push({ type: "text_end", contentIndex: index, content: answer.content, partial: message }); }
                if (answer.tool_calls !== undefined) {
                  if (!context.tools?.length || !Array.isArray(answer.tool_calls) || answer.tool_calls.length > 8 || choice.finish_reason !== "tool_calls") throw failure("Invalid local model tool calls");
                  const ids = new Set<string>();
                  for (const raw of answer.tool_calls) { const call = object(raw), fn = object(call.function); if (typeof call.id !== "string" || !call.id || ids.has(call.id) || call.type !== "function" || typeof fn.name !== "string" || !admittedToolNames.includes(fn.name) || typeof fn.arguments !== "string") throw failure("Unexpected local model tool call"); ids.add(call.id); const tool = { type: "toolCall" as const, id: call.id, name: fn.name, arguments: object(JSON.parse(fn.arguments)) }; const index = message.content.length; message.content.push(tool); stream.push({ type: "toolcall_start", contentIndex: index, partial: message }); stream.push({ type: "toolcall_end", contentIndex: index, toolCall: tool, partial: message }); }
                }
                if (choice.finish_reason === "tool_calls" && !message.content.some(item => item.type === "toolCall")) throw failure("Missing local model tool calls");
                message.stopReason = choice.finish_reason === "tool_calls" ? "toolUse" : choice.finish_reason === "length" ? "length" : "stop";
                if (payload.usage !== undefined) { const usage = object(payload.usage); if (![usage.prompt_tokens, usage.completion_tokens].every(value => Number.isSafeInteger(value) && value >= 0)) throw failure("Malformed model usage"); message.usage.input = usage.prompt_tokens; message.usage.output = usage.completion_tokens; message.usage.totalTokens = usage.prompt_tokens + usage.completion_tokens; }
                stream.push({ type: "done", reason: message.stopReason, message }); stream.end(message);
              } catch (error) { problem ??= error instanceof HarnessError ? error : failure("Local model protocol request failed"); message.stopReason = state.controller.signal.aborted ? "aborted" : "error"; message.errorMessage = "Local model request failed"; stream.push({ type: "error", reason: message.stopReason, error: message }); stream.end(message); }
            })();
            return stream;
          };
          const modelRuntime = await ModelRuntime.create({ credentials: new InMemoryCredentialStore(), modelsStore: new InMemoryModelsStore(), modelsPath: null, allowModelNetwork: false });
          modelRuntime.registerProvider("omlx", { baseUrl, api: "openai-completions", streamSimple, models: [{ id: options.model.id, name: options.model.id, reasoning: false, input: ["text"], contextWindow: options.model.contextWindow, maxTokens: options.model.maxTokens, cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 } }] });
          await modelRuntime.setRuntimeApiKey("omlx", execution.credential);
          const model = modelRuntime.getModel("omlx", options.model.id); if (!model) throw failure("Explicit local model missing from Pi registry");
          const baseSystemPrompt = options.systemPrompt ?? "You are an Agent 2 specialist. Use only the supplied read tools and, when present, the Chirality method-change control callback inside the authorized project. Do not claim write, shell, network or delegation authority.";
          const instructionPrompt = input.instructionContext === undefined ? baseSystemPrompt : `${baseSystemPrompt}\n\n<chirality-runtime-context schema="v3">\n${JSON.stringify(input.instructionContext.supplied)}\n</chirality-runtime-context>`;
          const systemPrompt = input.contextSuccessor === undefined ? instructionPrompt : `${instructionPrompt}\n\n<chirality-continuation sha256="${input.contextSuccessor.continuationSha256}">\n${input.contextSuccessor.continuationText}\n</chirality-continuation>`;
          const settings = SettingsManager.inMemory({ packages: [], extensions: [], skills: [], prompts: [], themes: [], enableSkillCommands: false, compaction, retry: { enabled: false } }, { projectTrusted: false });
          const resourceLoader = new DefaultResourceLoader({ cwd: options.canonicalRoot, agentDir: join(execution.transcriptRoot, "ambient-disabled"), settingsManager: settings, noExtensions: true, noSkills: true, noPromptTemplates: true, noThemes: true, noContextFiles: true, systemPrompt, appendSystemPrompt: [], extensionsOverride: base => ({ ...base, extensions: [], errors: [] }), skillsOverride: () => ({ skills: [], diagnostics: [] }), promptsOverride: () => ({ prompts: [], diagnostics: [] }), themesOverride: () => ({ themes: [], diagnostics: [] }), agentsFilesOverride: () => ({ agentsFiles: [] }), systemPromptOverride: () => systemPrompt, appendSystemPromptOverride: () => [] });
          await resourceLoader.reload();
          if (state.controller.signal.aborted) throw failure("Pi startup cancelled");
          const methodTools = (input.runtimeTools ?? []).map(tool => createRuntimeTool(tool, state.controller.signal));
          const baseTool = binding ? createBoundPiReadTool({ canonicalRoot: options.canonicalRoot, tool: binding.tool, protectedPaths: [...options.protectedPaths, execution.transcriptRoot], isCurrent: () => bindings.get(input.session.sessionId) === binding && !closed, signal: state.controller.signal }) : createPiReadTool({ canonicalRoot: options.canonicalRoot, name: input.opts.tools[0] as "read" | "read_file", protectedPaths: [...options.protectedPaths, execution.transcriptRoot] });
          const created = await createAgentSession({ cwd: options.canonicalRoot, agentDir: join(execution.transcriptRoot, "ambient-disabled"), modelRuntime, model, resourceLoader, sessionManager, settingsManager: settings, noTools: "all", tools: admittedToolNames, customTools: [baseTool, ...methodTools] });
          state.session = created.session;
          if (created.modelFallbackMessage || !sameNames(created.session.getActiveToolNames(), admittedToolNames)) throw failure("Pi changed the exact model/tool binding");
          unsubscribe = created.session.subscribe(event => { try { for (const projected of mapPiEvent(event, { sessionId: input.session.sessionId, turnId: input.turnId })) enqueue(projected); } catch (error) { problem ??= error; state.controller.abort(); void created.session.abort(); } });
          if (state.controller.signal.aborted) throw failure("Pi startup cancelled");
          await created.session.prompt(input.message, { expandPromptTemplates: false });
          await created.session.waitForIdle();
        } catch (error) { problem ??= error; } finally { done = true; wake?.(); }
      })();
      let cleaned: Promise<void> | undefined;
      const cleanup = () => cleaned ??= (async () => {
        clearTimeout(timer); state.controller.abort(); unsubscribe?.();
        try { await state.session?.abort(); } catch { problem ??= failure("Pi abort cleanup failed"); }
        await run;
        try { state.session?.dispose(); } catch { problem ??= failure("Pi disposal failed"); }
        finally {
          active.delete(input.session.sessionId);
          if (problem || state.interrupted || closed || Buffer.byteLength(JSON.stringify(history.manager?.getEntries() ?? [])) > maxBytes * 4) invalidate(input.session.sessionId);
          else if (histories.get(input.session.sessionId) === history) history.lastUsed = Date.now();
        }
      })();
      try {
        yield { type: "session:init", data: { engineSessionId: history.engineSessionId, providerSpanId: history.providerSpanId, adapterId: "pi", providerId: "omlx", model: options.model.id } };
        while (!done || queue.length) { if (queue.length) yield queue.shift()!; else await new Promise<void>(resolveWake => { wake = resolveWake; }); }
        await cleanup();
        if (state.interrupted) yield { type: "process:exit", data: { exitCode: 0, interrupted: true } };
        else if (problem) { const error = problem instanceof HarnessError ? problem : failure("Pi runtime failed"); yield { type: "turn:error", data: { phase: "mid-stream", errorType: error.type, message: error.message, status: error.status, severity: "error", fatal: true } }; yield { type: "process:exit", data: { exitCode: 1, error: error.message, errorType: error.type, status: error.status, fatal: true, severity: "error" } }; }
        else { yield { type: "session:complete", data: {} }; yield { type: "process:exit", data: { exitCode: 0 } }; }
      } finally { await cleanup(); }
    }
  };
}
