import { randomUUID } from "node:crypto";
import { withRetirementFailure } from "./retirement-failure.js";
import { realpath } from "node:fs/promises";
import {
  HOSTED_MODEL_ID_PATTERN, HOSTED_REASONING_EFFORT_PATTERN,
  RuntimeError, validateHarnessEventV2, validateServerRequestAnswer, policySelectionFromPermissionMode,
  type EventAttributionV2,
  type DelegatedAttachmentInput,
  type DelegatedHarnessProcessSupervisorPort,
  type DelegatedInteractionMode,
  type DelegatedRole,
  type DelegatedTurnRequest,
  type DelegatedTurnResponse,
  type HostedModelCatalog,
  type PolicySelection,
  type WorkerContinuity,
  type WorkerRetirementCoordinatorPort,
  type SupervisorNativePlanPort,
  type NativePlanTransportEvent,
  type NativePlanClarificationPrompt,
  type SupervisorTurnProgressPort,
  type SupervisorRequestPort,
  type SupervisorSteerPort,
  type SessionSteerRequest,
  type SessionSteerResponse,
  type PendingServerRequest,
  type ServerRequestAnswer,
  type DelegatedTurnProgressEvent
} from "@chirality/runtime-contracts";

import { createRolePolicyEvidence, RUNTIME_ROLES, type RolePolicySettings } from "./role-policy.js";

/** One project's delegated composition: the shared supervisor, the retirement journal and attribution. */
export interface DelegatedProjectBinding {
  /** Journal continuity for the retirement records; root-bound, never an account claim. */
  identity: WorkerContinuity;
  supervisor: DelegatedHarnessProcessSupervisorPort;
  retirement: WorkerRetirementCoordinatorPort;
  nativePlanSink?: DelegatedNativePlanSink;
  /** Default attribution for turns that do not choose a model. */
  actual?: EventAttributionV2;
  /** Non-hidden catalog; a requested model or effort outside it is refused before any envelope is sent. */
  catalog?: Readonly<HostedModelCatalog>;
  rolePolicy?: RolePolicySettings;
  /** Controlled fixture evidence must never be upgraded by a request; defaults to provider-observed. */
  evidenceClass?: "controlled-worker" | "provider-observed";
}
export interface DelegatedNativePlanWorkerBinding {
  projectId: string;
  sessionId: string;
  clientTurnId: string;
  workerId: string;
  generation: string;
}
export interface DelegatedNativePlanSink {
  open(binding: DelegatedNativePlanWorkerBinding, bridge: SupervisorNativePlanPort): Promise<void>;
  capture(binding: DelegatedNativePlanWorkerBinding, events: readonly NativePlanTransportEvent[], clarifications: readonly NativePlanClarificationPrompt[]): Promise<void>;
  close(binding: DelegatedNativePlanWorkerBinding): Promise<void>;
}
export interface DelegatedTurnObserver {
  signal?: AbortSignal;
  onProgress(event: DelegatedTurnProgressEvent): void | Promise<void>;
}
export interface DelegatedRuntimeOptions {
  daemonId: string;
  /** Static bindings (tests, single-project compositions). */
  projects?: ReadonlyMap<string, DelegatedProjectBinding>;
  /** Dynamic bindings for projects registered while the service runs. Consulted after `projects`. */
  resolveProject?(projectId: string): Promise<DelegatedProjectBinding | undefined>;
}
/**
 * Turn input accepted by the runtime; developer instructions and additive
 * native role configuration travel to the private supervisor envelope.
 */
export type DelegatedTurnInput = DelegatedTurnRequest;

/** The private broker envelope handed to `supervisor.acquire` as JSON text. */
export interface CodexTurnEnvelope {
  schema: "chirality-codex-turn/v1";
  prompt: string;
  attachments?: readonly DelegatedAttachmentInput[];
  cwd: string;
  developerInstructions?: string;
  /** Additive supported per-thread native role configuration; no feature or depth overrides. */
  nativeRoleConfig?: Readonly<Record<string, string>>;
  /** @deprecated Rejected by the stock supervisor. */
  contextUpdate?: string;
  policy: PolicySelection;
  model?: string;
  reasoningEffort?: string;
  interactionMode: DelegatedInteractionMode;
  requestedRole: DelegatedRole;
  resumeThreadId?: string;
  projectId: string;
  sessionId?: string;
  clientTurnId: string;
}
export function parseCodexTurnEnvelope(input: string): CodexTurnEnvelope {
  let value: unknown;
  try { value = JSON.parse(input); } catch { throw new RuntimeError("INVALID_REQUEST", "Codex worker requires the private broker JSON envelope"); }
  if (!value || typeof value !== "object" || Array.isArray(value)) throw new RuntimeError("INVALID_REQUEST", "Invalid Codex turn envelope");
  const envelope = value as Record<string, unknown>;
  const allowed = ["schema", "prompt", "attachments", "cwd", "developerInstructions", "nativeRoleConfig", "contextUpdate", "policy", "model", "reasoningEffort", "interactionMode", "requestedRole", "resumeThreadId", "projectId", "sessionId", "clientTurnId"];
  if (envelope.schema !== "chirality-codex-turn/v1" || Object.keys(envelope).some(key => !allowed.includes(key)) || typeof envelope.prompt !== "string" || !envelope.prompt.trim()
    || typeof envelope.cwd !== "string" || !envelope.cwd || typeof envelope.clientTurnId !== "string" || typeof envelope.projectId !== "string"
    || !["chat", "native-plan"].includes(String(envelope.interactionMode)) || !RUNTIME_ROLES.includes(envelope.requestedRole as DelegatedRole)
    || !envelope.policy || typeof envelope.policy !== "object") throw new RuntimeError("INVALID_REQUEST", "Invalid Codex turn envelope");
  const policy = envelope.policy as PolicySelection;
  if (!["untrusted", "on-request", "never"].includes(policy.approvalPolicy) || !["read-only", "workspace-write", "danger-full-access"].includes(policy.sandbox)) throw new RuntimeError("INVALID_REQUEST", "Invalid Codex policy selection");
  for (const key of ["developerInstructions", "contextUpdate", "model", "reasoningEffort", "resumeThreadId", "sessionId"]) {
    if (envelope[key] !== undefined && typeof envelope[key] !== "string") throw new RuntimeError("INVALID_REQUEST", "Invalid Codex turn envelope");
  }
  if (envelope.nativeRoleConfig !== undefined) {
    const config = envelope.nativeRoleConfig;
    if (!config || typeof config !== "object" || Array.isArray(config) || Object.entries(config).some(([key, value]) => !/^agents\.(HELP_HUMAN|HELPS_HUMANS|WORKING_ITEMS|TASK)\.(description|config_file)$/.test(key) || typeof value !== "string")) throw new RuntimeError("INVALID_REQUEST", "Invalid native role configuration");
  }
  if (envelope.attachments !== undefined && !Array.isArray(envelope.attachments)) throw new RuntimeError("INVALID_REQUEST", "Invalid Codex attachment envelope");
  return envelope as unknown as CodexTurnEnvelope;
}

const ID_PATTERN = /^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$/u;
const nonempty = (value: unknown): value is string => typeof value === "string" && value.length > 0 && value.length <= 256;
interface LiveTurn { turnId: string; workerId: string; generation: string; sessionId?: string }

/** Runtime-owned broker composition over the stock Codex supervisor. */
export class DelegatedRuntime {
  private readonly active = new Set<string>();
  private readonly turnRetirements = new Map<string, Promise<void>>();
  private readonly interruptedTurns = new Set<string>();
  private readonly liveTurns = new Map<string, LiveTurn>();
  private readonly sessionTurns = new Map<string, string>();
  private closing = false;
  private readonly options: DelegatedRuntimeOptions;
  private readonly inFlight = new Set<Promise<unknown>>();
  constructor(options: DelegatedRuntimeOptions) {
    this.options = { ...options, projects: new Map([...(options.projects ?? [])].map(([key, value]) => [key, Object.freeze({ ...value, ...(value.actual ? { actual: Object.freeze({ ...value.actual }) } : {}), ...(value.rolePolicy ? { rolePolicy: structuredClone(value.rolePolicy) } : {}), identity: Object.freeze({ ...value.identity }) })])) };
  }

  private async binding(projectId: string): Promise<DelegatedProjectBinding> {
    if (this.closing) throw new RuntimeError("ENGINE_UNAVAILABLE", "Delegated runtime is shutting down", 503);
    const binding = this.options.projects?.get(projectId) ?? await this.options.resolveProject?.(projectId);
    if (binding === undefined) throw new RuntimeError("ENGINE_UNAVAILABLE", "No delegated worker is configured for this project", 503);
    return binding;
  }

  /** Per-turn attribution: the requested catalog choice or the admitted default, never a substitute. */
  private resolveTurnAttribution(binding: DelegatedProjectBinding, admitted: EventAttributionV2, request: DelegatedTurnInput): EventAttributionV2 {
    if (request.model === undefined && request.reasoningEffort === undefined) return admitted;
    const pattern = (value: unknown, expected: RegExp) => typeof value === "string" && expected.test(value);
    if ((request.model !== undefined && !pattern(request.model, HOSTED_MODEL_ID_PATTERN)) || (request.reasoningEffort !== undefined && !pattern(request.reasoningEffort, HOSTED_REASONING_EFFORT_PATTERN))) throw new RuntimeError("INVALID_REQUEST", "Invalid model or reasoning effort selection");
    const model = request.model ?? admitted.model;
    if (request.model !== undefined && request.model !== admitted.model && binding.catalog === undefined) {
      throw new RuntimeError("ENGINE_UNAVAILABLE", `Model '${request.model}' is not in the authenticated Codex catalog`, 503, { reason: "MODEL_NOT_IN_CATALOG", model: request.model, available: [admitted.model] });
    }
    const entry = binding.catalog?.models.find(candidate => candidate.model === model);
    if (binding.catalog !== undefined && entry === undefined) {
      throw new RuntimeError("ENGINE_UNAVAILABLE", `Model '${model}' is not in the authenticated Codex catalog`, 503, { reason: "MODEL_NOT_IN_CATALOG", model, available: binding.catalog.models.map(candidate => candidate.model) });
    }
    if (request.reasoningEffort !== undefined) {
      const supported = entry ? [...entry.supportedReasoningEfforts] : admitted.reasoningEffort === undefined ? [] : [admitted.reasoningEffort];
      if (!supported.includes(request.reasoningEffort)) throw new RuntimeError("ENGINE_UNAVAILABLE", `Reasoning effort '${request.reasoningEffort}' is not supported by '${model}'`, 503, { reason: "REASONING_EFFORT_UNSUPPORTED", model, supported });
    }
    const reasoningEffort = request.reasoningEffort ?? (request.model === undefined || request.model === admitted.model ? admitted.reasoningEffort : entry?.defaultReasoningEffort);
    return { ...admitted, model, ...(reasoningEffort === undefined ? {} : { reasoningEffort }) };
  }

  private liveTurn(projectId: string, turnId: string): LiveTurn {
    const live = this.liveTurns.get(`${projectId}\0${turnId}`);
    if (!live) throw new RuntimeError("FORBIDDEN", "Turn is no longer interruptible", 403);
    return live;
  }
  private liveSessionTurn(projectId: string, sessionId: string): LiveTurn | undefined {
    const key = this.sessionTurns.get(`${projectId}\0${sessionId}`);
    return key === undefined ? undefined : this.liveTurns.get(key);
  }
  private requestPort(binding: DelegatedProjectBinding): SupervisorRequestPort | undefined {
    const port = binding.supervisor as DelegatedHarnessProcessSupervisorPort & Partial<SupervisorRequestPort>;
    return typeof port.pendingRequests === "function" && typeof port.answerRequest === "function" ? port as SupervisorRequestPort : undefined;
  }

  async steerTurn(projectId: string, sessionId: string, request: SessionSteerRequest): Promise<SessionSteerResponse> {
    const binding = await this.binding(projectId);
    const live = this.liveSessionTurn(projectId, sessionId);
    const rejected = (message: string): SessionSteerResponse => ({ operationId: request.operationId, turnId: request.expectedTurnId, status: "rejected", message });
    if (!live || live.turnId !== request.expectedTurnId) return rejected("The target turn is no longer active; no input was sent.");
    const port = binding.supervisor as DelegatedHarnessProcessSupervisorPort & Partial<SupervisorSteerPort>;
    if (!port.steerTurn) return rejected("Native steering is unavailable in this composition.");
    return port.steerTurn(live.workerId, live.generation, request);
  }

  /** Unanswered Codex server requests of the session's live turn; empty when no turn is live. */
  async pendingRequests(projectId: string, sessionId: string): Promise<readonly PendingServerRequest[]> {
    const binding = await this.binding(projectId);
    const live = this.liveSessionTurn(projectId, sessionId);
    const port = this.requestPort(binding);
    if (!live || !port) return [];
    try { return await port.pendingRequests(live.workerId, live.generation); }
    catch (error) {
      // The turn can reach its terminal and retire between the live lookup and the read; that is an empty answer, not a failure.
      if (this.liveTurns.get(`${projectId}\0${live.turnId}`) !== live || !(await binding.supervisor.inventory()).some(worker => worker.workerId === live.workerId && worker.generation === live.generation)) return [];
      throw error;
    }
  }

  async answerRequest(projectId: string, sessionId: string, requestId: string, answer: ServerRequestAnswer): Promise<{ sent: true }> {
    const binding = await this.binding(projectId);
    if (!nonempty(requestId)) throw new RuntimeError("INVALID_REQUEST", "A bounded request identity is required");
    validateServerRequestAnswer(answer);
    const live = this.liveSessionTurn(projectId, sessionId);
    if (!live) throw new RuntimeError("NOT_FOUND", "No live turn holds Codex requests for this session", 404);
    const port = this.requestPort(binding);
    if (!port) throw new RuntimeError("ENGINE_UNAVAILABLE", "Supervisor request bridge is unavailable", 503);
    return port.answerRequest(live.workerId, live.generation, requestId, structuredClone(answer));
  }

  /** Answers the approval whose Codex item id (or legacy call id) is the App's tool-use id. */
  async answerApprovalByToolUseId(projectId: string, sessionId: string, toolUseId: string, verdict: "allow" | "deny" | "allowForSession"): Promise<{ sent: true }> {
    if (!nonempty(toolUseId)) throw new RuntimeError("INVALID_REQUEST", "A bounded tool-use identity is required");
    if (!["allow", "deny", "allowForSession"].includes(verdict)) throw new RuntimeError("INVALID_REQUEST", "Unknown approval verdict");
    const pending = await this.pendingRequests(projectId, sessionId);
    const request = pending.find(candidate => candidate.itemId === toolUseId && APPROVAL_METHODS.has(candidate.method));
    if (!request) throw new RuntimeError("NOT_FOUND", "No pending Codex approval carries this tool-use identity", 404);
    return this.answerRequest(projectId, sessionId, request.requestId, { kind: "approval", verdict });
  }

  interruptTurn(projectId: string, request: { turnId: string }) {
    const pending = this.executeInterrupt(projectId, { turnId: request?.turnId });
    this.inFlight.add(pending);
    void pending.finally(() => this.inFlight.delete(pending)).catch(() => undefined);
    return pending;
  }

  private async executeInterrupt(projectId: string, request: { turnId: string }) {
    if (!request || !nonempty(request.turnId)) throw new RuntimeError("INVALID_REQUEST", "A bounded turn identity is required");
    const binding = await this.binding(projectId);
    const live = this.liveTurn(projectId, request.turnId);
    const key = `${projectId}\0${request.turnId}`;
    if (this.interruptedTurns.has(key)) throw new RuntimeError("FORBIDDEN", "Turn is no longer interruptible", 403);
    this.interruptedTurns.add(key);
    // Interruption never retires. A supervisor without a native interrupt takes
    // the retire branch deliberately, joining the turn's own memoized attempt.
    if (binding.supervisor.interrupt) {
      // A rejected interrupt leaves the turn interruptible; only a delivered one latches.
      try { await binding.supervisor.interrupt(live.workerId, live.generation); }
      catch (error) { this.interruptedTurns.delete(key); throw error; }
    }
    else await this.retireWorker(binding, key, live.workerId, live.generation);
    return { interrupted: true as const, turnId: live.turnId, workerGeneration: live.generation };
  }

  private retireWorker(binding: DelegatedProjectBinding, key: string, workerId: string, generation: string): Promise<void> {
    const previous = this.turnRetirements.get(key);
    if (previous) return previous;
    // Install the promise before invoking the supervisor. Interrupt, failure and
    // completion must join the same attempt, including its rejection.
    const retirement = Promise.resolve().then(() => binding.supervisor.retire(workerId, generation));
    this.turnRetirements.set(key, retirement);
    return retirement;
  }

  startGeneration(daemonId?: string): void {
    if (this.inFlight.size !== 0) throw new RuntimeError("ENGINE_UNAVAILABLE", "Previous delegated generation has not drained", 503);
    if (daemonId !== undefined) this.options.daemonId = daemonId;
    this.closing = false;
  }

  /** Interrupts live turns, retires every worker generation and drains in-flight work. */
  async close(): Promise<void> {
    this.closing = true;
    const bindings = new Map<DelegatedHarnessProcessSupervisorPort, DelegatedProjectBinding>();
    for (const binding of this.options.projects?.values() ?? []) bindings.set(binding.supervisor, binding);
    for (const [key, live] of this.liveTurns) {
      const projectId = key.slice(0, key.indexOf("\0"));
      const binding = this.options.projects?.get(projectId) ?? await this.options.resolveProject?.(projectId).catch(() => undefined);
      if (!binding) continue;
      bindings.set(binding.supervisor, binding);
      if (this.interruptedTurns.has(key)) continue;
      this.interruptedTurns.add(key);
      if (binding.supervisor.interrupt) await binding.supervisor.interrupt(live.workerId, live.generation).catch(() => undefined);
      else await this.retireWorker(binding, key, live.workerId, live.generation).catch(() => undefined);
    }
    await Promise.all([...bindings.keys()].map(async (supervisor) => {
      const workers = await supervisor.inventory();
      await Promise.all(workers.map((worker) => supervisor.retire(worker.workerId, worker.generation)));
    }));
    await Promise.allSettled([...this.inFlight]);
  }

  turn(projectId: string, request: DelegatedTurnInput, _runtimeTools: readonly unknown[] = [], observer?: DelegatedTurnObserver): Promise<DelegatedTurnResponse> {
    const pending = this.executeTurn(projectId, structuredClone(request), observer);
    this.inFlight.add(pending);
    void pending.finally(() => this.inFlight.delete(pending)).catch(() => undefined);
    return pending;
  }

  private async executeTurn(projectId: string, request: DelegatedTurnInput, observer?: DelegatedTurnObserver): Promise<DelegatedTurnResponse> {
    if (!request || typeof request !== "object" || typeof request.turnId !== "string") throw new RuntimeError("INVALID_REQUEST", "A scalar turn identity is required");
    if (!nonempty(request.turnId) || !ID_PATTERN.test(request.turnId) || typeof request.prompt !== "string" || Buffer.byteLength(request.prompt) > 65_536) {
      throw new RuntimeError("INVALID_REQUEST", "Invalid bounded turn request");
    }
    const interactionMode = request.interactionMode ?? "chat";
    if (interactionMode !== "chat" && interactionMode !== "native-plan") throw new RuntimeError("INVALID_REQUEST", "Unknown interaction mode");
    if (request.sessionId !== undefined && (!nonempty(request.sessionId) || !ID_PATTERN.test(request.sessionId))) throw new RuntimeError("INVALID_REQUEST", "Invalid runtime session identity");
    if (request.permissionMode !== undefined && !["readOnly", "ask", "workspaceWrite", "bypass"].includes(request.permissionMode)) throw new RuntimeError("INVALID_REQUEST", "Unknown permission mode");
    if (request.developerInstructions !== undefined && (typeof request.developerInstructions !== "string" || Buffer.byteLength(request.developerInstructions) > 1_048_576)) throw new RuntimeError("INVALID_REQUEST", "Invalid developer instructions");
    if (request.contextUpdate !== undefined && (typeof request.contextUpdate !== "string" || Buffer.byteLength(request.contextUpdate) > 1_048_576)) throw new RuntimeError("INVALID_REQUEST", "Invalid context update");
    const requestedRole = request.requestedRole ?? "untyped";
    if (!RUNTIME_ROLES.includes(requestedRole)) throw new RuntimeError("INVALID_REQUEST", "Unknown requested role");
    const binding = await this.binding(projectId);
    const nativePlanPort = binding.supervisor as DelegatedHarnessProcessSupervisorPort & Partial<SupervisorNativePlanPort>;
    if (interactionMode === "native-plan" && (!request.sessionId || !binding.nativePlanSink || !nativePlanPort.drainNativePlanEvents || !nativePlanPort.pendingNativePlanClarifications || !nativePlanPort.replyNativePlanClarification)) throw new RuntimeError("ENGINE_UNAVAILABLE", "Native Plan supervisor and registry composition is unavailable", 503);
    const progressPort = binding.supervisor as DelegatedHarnessProcessSupervisorPort & Partial<SupervisorTurnProgressPort>;
    if (observer && !progressPort.drainTurnProgress) throw new RuntimeError("ENGINE_UNAVAILABLE", "Delegated turn progress bridge is unavailable", 503);
    const retirement = binding.retirement;
    if (!retirement) throw new RuntimeError("ENGINE_UNAVAILABLE", "Turn retirement authority unavailable", 503);
    const identity = binding.identity;
    if (await realpath(identity.canonicalRoot) !== identity.canonicalRoot || identity.cwd !== identity.canonicalRoot) throw new RuntimeError("FORBIDDEN", "Worker root continuity is invalid", 403);
    const admitted: EventAttributionV2 = binding.actual ?? { adapterId: "codex-app-server", providerId: "openai", model: request.model ?? "codex-default" };
    const actual = this.resolveTurnAttribution(binding, admitted, request);
    const policy = policySelectionFromPermissionMode(request.permissionMode);
    const roleEvidence = createRolePolicyEvidence({ role: requestedRole, actual, policy: binding.rolePolicy ?? { allowedTools: [], readRoots: [identity.canonicalRoot], writeRoots: policy.sandbox === "read-only" ? [] : [identity.canonicalRoot], networkPosture: "off", processPolicy: `codex:${policy.approvalPolicy}/${policy.sandbox}`, delegationPolicy: "Codex [agents] configuration; native descent does not assign a role" } });
    const key = `${projectId}\0${request.turnId}`;
    if (this.active.has(key)) throw new RuntimeError("SESSION_TURN_IN_PROGRESS", "Turn is already running", 409);
    this.active.add(key);
    const sessionKey = request.sessionId === undefined ? undefined : `${projectId}\0${request.sessionId}`;
    try {
      if (await retirement.read(request.turnId) !== undefined) throw new RuntimeError("INVALID_REQUEST", "Turn identity already has a durable record; automatic replay is forbidden", 409);
      if (request.previousTurnId !== undefined && (typeof request.previousTurnId !== "string" || !ID_PATTERN.test(request.previousTurnId))) throw new RuntimeError("INVALID_REQUEST", "Invalid previous turn identity");
      const restart = request.previousTurnId === undefined ? { method: "thread/start" as const } : await retirement.restart(request.previousTurnId, identity, roleEvidence.policyDigest);
      await retirement.prepare({ turnId: request.turnId, identity, rolePolicyDigest: roleEvidence.policyDigest, state: "prepared", ...(restart.threadId ? { threadId: restart.threadId } : {}) });
      if (this.closing) throw new RuntimeError("ENGINE_UNAVAILABLE", "Delegated runtime is shutting down", 503);
      const envelope: CodexTurnEnvelope = { schema: "chirality-codex-turn/v1", prompt: request.prompt, cwd: identity.canonicalRoot, policy, interactionMode, requestedRole, projectId, clientTurnId: request.turnId,
        ...(request.attachments?.length ? { attachments: structuredClone(request.attachments) } : {}),
        ...(request.developerInstructions === undefined ? {} : { developerInstructions: request.developerInstructions }),
        ...(request.nativeRoleConfig === undefined ? {} : { nativeRoleConfig: request.nativeRoleConfig }),
        ...(request.contextUpdate === undefined ? {} : { contextUpdate: request.contextUpdate }),
        ...(request.model === undefined ? {} : { model: request.model }), ...(request.reasoningEffort === undefined ? {} : { reasoningEffort: request.reasoningEffort }),
        ...(request.sessionId === undefined ? {} : { sessionId: request.sessionId }), ...(restart.threadId ? { resumeThreadId: restart.threadId } : {}) };
      const worker = await binding.supervisor.acquire(request.turnId, JSON.stringify(envelope), observer?.signal);
      this.liveTurns.set(key, { turnId: request.turnId, workerId: worker.workerId, generation: worker.generation, ...(request.sessionId === undefined ? {} : { sessionId: request.sessionId }) });
      if (sessionKey !== undefined) this.sessionTurns.set(sessionKey, key);
      const nativePlanBinding = interactionMode === "native-plan" ? { projectId, sessionId: request.sessionId!, clientTurnId: request.turnId, workerId: worker.workerId, generation: worker.generation } : undefined;
      let nativePlanOpened = false, nativePlanClosed = false;
      const captureNativePlan = async () => {
        if (!nativePlanBinding || !binding.nativePlanSink) return;
        const [events, clarifications] = await Promise.all([nativePlanPort.drainNativePlanEvents!(worker.workerId, worker.generation), nativePlanPort.pendingNativePlanClarifications!(worker.workerId, worker.generation)]);
        // Empty clarification snapshots clear requests resolved by the supplier.
        await binding.nativePlanSink.capture(nativePlanBinding, events, clarifications);
      };
      const closeNativePlan = async () => {
        if (!nativePlanBinding || !binding.nativePlanSink || !nativePlanOpened || nativePlanClosed) return;
        nativePlanClosed = true; await binding.nativePlanSink.close(nativePlanBinding);
      };
      const captureProgress = async () => {
        if (!observer) return;
        for (const event of await progressPort.drainTurnProgress!(worker.workerId, worker.generation)) await observer.onProgress(event);
      };
      // Polling callbacks can outlive registry cleanup; retain their exact
      // generation's settled attempt rather than recreating it afterward.
      let retirementAttempt: Promise<void> | undefined;
      const retire = () => retirementAttempt ??= this.retireWorker(binding, key, worker.workerId, worker.generation);
      let cancellation: Promise<void> | undefined;
      let cancellationError: unknown;
      const cancel = () => {
        cancellation ??= (async () => {
          this.interruptedTurns.add(key);
          if (binding.supervisor.interrupt) await binding.supervisor.interrupt(worker.workerId, worker.generation);
          else await retire();
        })().catch(error => { cancellationError = error; });
      };
      observer?.signal?.addEventListener("abort", cancel, { once: true });
      if (observer?.signal?.aborted) cancel();
      try {
        if (nativePlanBinding && binding.nativePlanSink) { await binding.nativePlanSink.open(nativePlanBinding, nativePlanPort as SupervisorNativePlanPort); nativePlanOpened = true; }
        let waiting = true;
        const resultPromise = binding.supervisor.wait(worker.workerId, worker.generation);
        void resultPromise.finally(() => { waiting = false; }).catch(() => {});
        const polling = (async () => { while (waiting) {
          await captureNativePlan();
          await captureProgress();
          if (waiting) await new Promise(resolve => setTimeout(resolve, 25));
        } })();
        let pollingError: unknown;
        void polling.catch((error: unknown) => {
          pollingError = error;
          // The Codex turn is still live: interrupt it before releasing its
          // bookkeeping, so the thread is not left with an orphaned turn.
          void (async () => {
            if (binding.supervisor.interrupt) await binding.supervisor.interrupt(worker.workerId, worker.generation).catch(() => {});
            await retire();
          })().catch(() => {});
        });
        const result = await resultPromise;
        await cancellation;
        if (cancellationError !== undefined) throw cancellationError;
        if (pollingError !== undefined) throw pollingError;
        waiting = false; await polling; await captureNativePlan(); await captureProgress();
        if (result.threadId !== undefined) {
          if (retirement.associateThread === undefined) throw new RuntimeError("ENGINE_UNAVAILABLE", "Durable thread association is unavailable", 503);
          await retirement.associateThread(request.turnId, result.threadId);
        }
        // Process reconciliation must succeed before publishing any terminal.
        await retire();
        const interrupted = binding.supervisor.interrupt ? result.exitCode === null && result.signal === "SIGTERM" : this.interruptedTurns.has(key);
        const terminal = await retirement.terminalize({ turnId: request.turnId, workerId: worker.workerId, generation: worker.generation, outcome: interrupted ? "interrupted" : result.exitCode === 0 ? "completed" : "failed", recordedAt: new Date().toISOString() });
        const event = { schemaVersion: 2, eventId: randomUUID(), sequence: 0, timestamp: terminal.recordedAt, projectId, sessionId: request.sessionId ?? request.turnId, turnId: request.turnId, attribution: actual,
          type: terminal.outcome === "completed" ? "turn.completed" : terminal.outcome === "interrupted" ? "turn.interrupted" : "turn.failed",
          data: terminal.outcome === "completed" ? { outcome: "completed" } : terminal.outcome === "interrupted" ? { outcome: "interrupted" } : { code: "WORKER_FAILED", message: result.stderr.trim() ? result.stderr.trim().slice(0, 512) : "Delegated worker did not complete successfully" } };
        if (!validateHarnessEventV2(event)) throw new RuntimeError("INTERNAL_FAILURE", "Invalid canonical v2 terminal projection", 500);
        return { terminal, output: result.stdout, ...(result.threadId ? { providerThreadId: result.threadId } : {}), evidenceClass: binding.evidenceClass ?? "provider-observed", roleEvidence, event };
      } catch (error) {
        // A transport outcome or interruption intent is not retirement evidence.
        // Keep the prepared record unresolved when cleanup cannot be confirmed.
        // The turn's own failure stays the reported error; a retirement
        // diagnostic travels with it as the cause instead of replacing it.
        let retired = false, failure: unknown = error;
        try { await retire(); retired = true; } catch (cleanup) { failure = withRetirementFailure(error, cleanup); }
        if (retired) await retirement.terminalize({ turnId: request.turnId, workerId: worker.workerId, generation: worker.generation, outcome: !binding.supervisor.interrupt && this.interruptedTurns.has(key) ? "interrupted" : "failed", recordedAt: new Date().toISOString() });
        throw failure;
      } finally {
        observer?.signal?.removeEventListener("abort", cancel);
        await cancellation;
        // The settled retirement attempt already reported its outcome above.
        try { await retire().catch(() => {}); }
        finally { await closeNativePlan(); }
      }
    } finally {
      this.turnRetirements.delete(key);
      this.interruptedTurns.delete(key);
      if (sessionKey !== undefined && this.sessionTurns.get(sessionKey) === key) this.sessionTurns.delete(sessionKey);
      this.liveTurns.delete(key);
      this.active.delete(key);
    }
  }
}

const APPROVAL_METHODS = new Set(["item/commandExecution/requestApproval", "item/fileChange/requestApproval", "item/permissions/requestApproval", "execCommandApproval", "applyPatchApproval"]);
