import { RuntimeError } from "./errors.js";
import type { HarnessEventV2, EventAttributionV2 } from "./v2-events.js";
/** Additive runtime-owned v2 boundary; not a vendor wire protocol. */
export interface WorkerContinuity {
  canonicalRoot: string;
  accountId: string;
  accountEpoch: number;
  policyDigest: string;
  cwd: string;
}
export interface WorkerHandle {
  workerId: string;
  generation: string;
  pid: number;
  state: "running" | "exited";
}
export interface WorkerResult {
  worker: WorkerHandle;
  exitCode: number | null;
  signal: string | null;
  threadId?: string;
  stdout: string;
  stderr: string;
}
/** Only the broker receives an instance; never expose token or socket to clients. */
export interface DelegatedHarnessProcessSupervisorPort {
  /** Host-only concrete adapter check, never a client-supplied containment assertion. */
  verifyHostedBoundary?(identity: WorkerContinuity): Promise<void>;
  acquire(workerId: string, input: string, signal?: AbortSignal): Promise<WorkerHandle>;
  inventory(): Promise<readonly WorkerHandle[]>;
  reconnect(workerId: string, generation: string): Promise<WorkerHandle>;
  wait(workerId: string, generation: string): Promise<WorkerResult>;
  /** Requests native interruption; resolves after its genuine terminal and retirement. */
  interrupt?(workerId: string, generation: string): Promise<void>;
  retire(workerId: string, generation: string): Promise<void>;
}
export interface WorkerTerminalRecord {
  turnId: string;
  workerId: string;
  generation: string;
  outcome: "completed" | "failed" | "interrupted";
  recordedAt: string;
}
export interface RetirementRecord {
  turnId: string;
  identity: WorkerContinuity;
  threadId?: string;
  rolePolicyDigest?: string;
  state: "prepared" | "committed" | "reconciliation-required";
  terminal?: WorkerTerminalRecord;
}
export interface WorkerRetirementCoordinatorPort {
  prepare(record: RetirementRecord): Promise<void>;
  associateThread?(turnId: string, threadId: string): Promise<void>;
  terminalize(terminal: WorkerTerminalRecord): Promise<WorkerTerminalRecord>;
  read(turnId: string): Promise<RetirementRecord | undefined>;
  reconcile(): Promise<readonly RetirementRecord[]>;
  restart(turnId: string, identity: WorkerContinuity, expectedRolePolicyDigest?: string): Promise<{ method: "thread/resume" | "thread/start"; threadId?: string }>;
}
export type DelegatedRole = "untyped" | "agent0" | "agent1" | "agent2" | "task";
export type DelegatedInteractionMode = "chat" | "native-plan";
export type DelegatedAttachmentInput =
  | { type: "text"; text: string; source: "untrusted-document" }
  | { type: "localImage"; path: string; mimeType: "image/png" | "image/jpeg" | "image/gif" | "image/webp"; source: "untrusted-attachment" };
export interface DelegatedTurnRequest {
  requestedRole?: DelegatedRole;
  /** Runtime session identity is mandatory for native Plan turns. */
  sessionId?: string;
  interactionMode?: DelegatedInteractionMode;
  permissionMode?: "readOnly" | "ask" | "workspaceWrite" | "bypass";
  turnId: string;
  previousTurnId?: string;
  prompt: string;
  /** Resolved user attachments. They remain untrusted user input, never instruction context. */
  attachments?: readonly DelegatedAttachmentInput[];
  /** Session-fixed catalog choice. Absent means the admitted default; never substituted. */
  model?: string;
  reasoningEffort?: string;
  /** Rendered role and method instructions for `thread/start` or `thread/resume` (`developerInstructions`); never a user message. */
  developerInstructions?: string;
  /** Additive supported per-thread native role configuration; no feature or depth overrides. */
  nativeRoleConfig?: Readonly<Record<string, string>>;
  /** @deprecated Rejected by the stock supervisor; send persistent developerInstructions instead. */
  contextUpdate?: string;
}
export interface DelegatedRoleEvidence {
  selectedRole: DelegatedRole;
  offeredRoles: DelegatedRole[];
  enforcementLabel: "role not mechanically enforced";
  evidencePosture: "instruction-asserted";
  policyDigest: string;
  actual: EventAttributionV2;
}
export interface DelegatedTurnResponse {
  roleEvidence: DelegatedRoleEvidence;
  event: HarnessEventV2;
  terminal: WorkerTerminalRecord;
  output: string;
  providerThreadId?: string;
  evidenceClass: "controlled-worker" | "provider-observed";
}

/** One non-hidden entry of the authenticated Codex model catalog (`model/list`). */
export interface HostedModelCatalogEntry {
  model: string;
  isDefault: boolean;
  defaultReasoningEffort: string;
  supportedReasoningEfforts: readonly string[];
}
/** Non-hidden catalog retained for one admission; `default` is its unique default entry. */
export interface HostedModelCatalog {
  models: readonly HostedModelCatalogEntry[];
  default: HostedModelCatalogEntry;
}
export interface HostedModelSelection { model: string; reasoningEffort: string }
export const HOSTED_MODEL_ID_PATTERN = /^[\x21-\x7e]{1,128}$/;
export const HOSTED_REASONING_EFFORT_PATTERN = /^[\x21-\x7e]{1,64}$/;
/** Validates the catalog shape exposed by hosted status: 1..64 entries, exactly one default, each default effort supported. */
export function validateHostedModelCatalogEntries(value: unknown): readonly HostedModelCatalogEntry[] {
  const invalidCatalog = () => new RuntimeError("INVALID_REQUEST", "Invalid hosted model catalog");
  if (!Array.isArray(value) || value.length < 1 || value.length > 64) throw invalidCatalog();
  const seen = new Set<string>();
  const models = value.map((entry: unknown): HostedModelCatalogEntry => {
    const item = hostedRecord(entry, ["model", "isDefault", "defaultReasoningEffort", "supportedReasoningEfforts"]);
    if (typeof item.model !== "string" || !HOSTED_MODEL_ID_PATTERN.test(item.model) || typeof item.isDefault !== "boolean"
      || typeof item.defaultReasoningEffort !== "string" || !HOSTED_REASONING_EFFORT_PATTERN.test(item.defaultReasoningEffort)
      || !Array.isArray(item.supportedReasoningEfforts) || item.supportedReasoningEfforts.length < 1 || item.supportedReasoningEfforts.length > 32
      || !item.supportedReasoningEfforts.every((effort: unknown) => typeof effort === "string" && HOSTED_REASONING_EFFORT_PATTERN.test(effort))
      || new Set(item.supportedReasoningEfforts).size !== item.supportedReasoningEfforts.length
      || !item.supportedReasoningEfforts.includes(item.defaultReasoningEffort) || seen.has(item.model)) throw invalidCatalog();
    seen.add(item.model);
    return Object.freeze({ model: item.model, isDefault: item.isDefault, defaultReasoningEffort: item.defaultReasoningEffort, supportedReasoningEfforts: Object.freeze([...(item.supportedReasoningEfforts as string[])]) });
  });
  if (models.filter(entry => entry.isDefault).length !== 1) throw invalidCatalog();
  return Object.freeze(models);
}
/** Builds a catalog from validated entries; the unique default entry becomes `default`. */
export function hostedModelCatalog(models: readonly HostedModelCatalogEntry[]): HostedModelCatalog {
  const validated = validateHostedModelCatalogEntries(models);
  return Object.freeze({ models: validated, default: validated.find(entry => entry.isDefault)! });
}
/**
 * Single no-substitution validator. An omitted request resolves to the catalog default;
 * anything else must name a catalog model and one of that model's supported efforts.
 */
export function resolveHostedModelSelection(catalog: HostedModelCatalog, requested?: unknown): HostedModelSelection {
  if (requested === undefined) return { model: catalog.default.model, reasoningEffort: catalog.default.defaultReasoningEffort };
  if (!requested || typeof requested !== "object" || Array.isArray(requested) || Object.keys(requested).sort().join(",") !== "model,reasoningEffort") {
    throw new RuntimeError("INVALID_REQUEST", "modelSelection requires exactly model and reasoningEffort", 400, { reason: "MODEL_SELECTION_INVALID" });
  }
  const { model, reasoningEffort } = requested as Record<string, unknown>;
  if (typeof model !== "string" || !HOSTED_MODEL_ID_PATTERN.test(model) || typeof reasoningEffort !== "string" || !HOSTED_REASONING_EFFORT_PATTERN.test(reasoningEffort)) {
    throw new RuntimeError("INVALID_REQUEST", "modelSelection requires exactly model and reasoningEffort", 400, { reason: "MODEL_SELECTION_INVALID" });
  }
  const entry = catalog.models.find(candidate => candidate.model === model);
  if (entry === undefined) {
    throw new RuntimeError("INVALID_REQUEST", `Model '${model}' is not in the authenticated Codex catalog`, 400, { reason: "MODEL_NOT_IN_CATALOG", model, available: catalog.models.map(candidate => candidate.model) });
  }
  if (!entry.supportedReasoningEfforts.includes(reasoningEffort)) {
    throw new RuntimeError("INVALID_REQUEST", `Reasoning effort '${reasoningEffort}' is not supported by '${model}'`, 400, { reason: "REASONING_EFFORT_UNSUPPORTED", model, supported: [...entry.supportedReasoningEfforts] });
  }
  return { model, reasoningEffort };
}
export interface HostedBootstrapStatus {
  schema: "chirality-hosted-bootstrap-status/v1";
  projectId: string;
  ceremony: "ready-to-start" | "pending" | "signed-in" | "failed" | "cancelled";
  admission: "unavailable" | "establishing" | "ready";
  canStartLogin: boolean;
  /** Non-hidden authenticated catalog; present only while `admission === "ready"` and always together with `selection`. */
  models?: readonly HostedModelCatalogEntry[];
  /** Admitted default model and its default reasoning effort. */
  selection?: HostedModelSelection;
}
export interface HostedProviderNetworkConsentRequest { consent: true }
export interface HostedBootstrapLoginStartResponse { loginId: string; authUrl: string }
export function validateHostedBootstrapStatus(value: unknown): HostedBootstrapStatus {
  const status = hostedRecord(value, ["schema", "projectId", "ceremony", "admission", "canStartLogin", "models", "selection"]);
  if (status.schema !== "chirality-hosted-bootstrap-status/v1" || typeof status.projectId !== "string" || !/^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$/.test(status.projectId)
    || !["ready-to-start", "pending", "signed-in", "failed", "cancelled"].includes(String(status.ceremony))
    || !["unavailable", "establishing", "ready"].includes(String(status.admission)) || typeof status.canStartLogin !== "boolean"
    || status.canStartLogin !== ["ready-to-start", "failed", "cancelled"].includes(String(status.ceremony))
    || (status.admission === "ready" && status.ceremony !== "signed-in")) {
    throw new RuntimeError("INVALID_REQUEST", "Invalid hosted bootstrap status");
  }
  const hasModels = Object.hasOwn(status, "models"), hasSelection = Object.hasOwn(status, "selection");
  if (hasModels !== hasSelection || (hasModels && status.admission !== "ready")) throw new RuntimeError("INVALID_REQUEST", "Invalid hosted bootstrap status");
  if (!hasModels) return status as unknown as HostedBootstrapStatus;
  const models = validateHostedModelCatalogEntries(status.models);
  const selection = hostedRecord(status.selection, ["model", "reasoningEffort"]);
  const selected = models.find(entry => entry.model === selection.model);
  if (typeof selection.model !== "string" || typeof selection.reasoningEffort !== "string" || selected === undefined || !selected.supportedReasoningEfforts.includes(selection.reasoningEffort)) {
    throw new RuntimeError("INVALID_REQUEST", "Invalid hosted bootstrap status");
  }
  return { ...(status as unknown as HostedBootstrapStatus), models, selection: { model: selection.model, reasoningEffort: selection.reasoningEffort } };
}
function hostedRecord(value: unknown, allowed: readonly string[]): Record<string, unknown> {
  if (!value || typeof value !== "object" || Array.isArray(value)
    || Object.keys(value).some(key => !allowed.includes(key))) throw new RuntimeError("INVALID_REQUEST", "Invalid hosted status/configuration fields");
  return value as Record<string, unknown>;
}
/** Trusted supervisor projection of an authoritative completed Codex plan item. */
export interface NativePlanTransportEvent {
  projectId: string;
  sessionId: string;
  clientTurnId: string;
  providerThreadId: string;
  providerTurnId: string;
  eventId: string;
  occurredAt: string;
  plan: unknown;
}
export interface NativePlanClarificationQuestion {
  id: string;
  header: string;
  question: string;
  options: readonly { label: string; description: string }[];
  isOther: boolean;
  isSecret: boolean;
}
export interface NativePlanClarificationPrompt {
  projectId: string;
  sessionId: string;
  clientTurnId: string;
  providerThreadId: string;
  providerTurnId: string;
  requestId: string | number;
  itemId: string;
  questions: readonly NativePlanClarificationQuestion[];
  isBlocking: boolean;
  autoResolutionMs: number | null;
}
export type NativePlanClarificationAnswers = Readonly<Record<string, { answers: readonly string[] }>>;
export interface SupervisorNativePlanPort {
  drainNativePlanEvents(workerId: string, generation: string): Promise<readonly NativePlanTransportEvent[]>;
  pendingNativePlanClarifications(workerId: string, generation: string): Promise<readonly NativePlanClarificationPrompt[]>;
  replyNativePlanClarification(workerId: string, generation: string, requestId: string | number, answers: NativePlanClarificationAnswers): Promise<{ sent: true }>;
}

export interface RuntimeToolCallbackDeclaration {
  name: string;
  description: string;
  inputSchema: Readonly<Record<string, unknown>>;
}
export type RuntimeToolCallbackMessage =
  | { kind: "pending" }
  | { kind: "callback"; callId: string; threadId: string; turnId: string; name: string; args: Readonly<Record<string, unknown>>; nativeChild?: Readonly<{ associationId: string; supplierGeneration: string; rootThreadId: string; rootTurnId: string; parentThreadId: string; parentTurnId: string; selectedRole: import("./engine.js").NativeChildSelectedRole; inheritedToolsDigest: string }> };
export interface RuntimeToolCallbackResult {
  success: boolean;
  contentItems: readonly { type: "inputText"; text: string }[];
}
/** Private daemon-to-supervisor bridge. Tool implementations never cross it. */
export interface SupervisorRuntimeToolPort {
  acquireWithRuntimeTools(workerId: string, input: string, tools: readonly RuntimeToolCallbackDeclaration[], inheritableTools?: readonly RuntimeToolCallbackDeclaration[]): Promise<WorkerHandle>;
  nextRuntimeToolCallback(workerId: string, generation: string): Promise<RuntimeToolCallbackMessage>;
  replyRuntimeToolCallback(workerId: string, generation: string, message: Extract<RuntimeToolCallbackMessage, { kind: "callback" }>, result: RuntimeToolCallbackResult): Promise<void>;
}
/**
 * Supervisor-observed progress of one delegated turn. Under D-GOV-43 (A2) the
 * stock Codex App Server's notifications and server requests pass through
 * unchanged: `method` and `params` are the upstream names and payloads.
 */
/** Exact developer history item whose injection was acknowledged by the supplier. */
export interface InstructionHistoryInjection {
  method: "thread/inject_items";
  text: string;
  sha256: string;
}

export type DelegatedTurnProgressEvent =
  | { type: "started"; providerThreadId: string; providerTurnId: string; instructionHistoryInjection?: InstructionHistoryInjection }
  | { type: "text"; providerThreadId: string; providerTurnId: string; text: string }
  | { type: "notification"; providerThreadId: string; providerTurnId?: string; method: string; params: unknown; occurredAt: string }
  | { type: "request"; providerThreadId: string; providerTurnId?: string; requestId: string; method: string; params: unknown; occurredAt: string }
  | {
      type: "request-resolved";
      providerThreadId: string;
      providerTurnId?: string;
      requestId: string;
      method: string;
      outcome: ServerRequestOutcome;
      decision?: unknown;
      decidedBy?: ServerRequestDecider;
      occurredAt: string;
    };
export interface SupervisorTurnProgressPort {
  drainTurnProgress(workerId: string, generation: string): Promise<readonly DelegatedTurnProgressEvent[]>;
}

export type ServerRequestOutcome = "answered" | "cancelled" | "unsupported" | "failed";
export type ServerRequestDecider = "user" | "policy" | "runtime";
/** One unanswered Codex server request held by the supervisor for a live turn. */
export interface PendingServerRequest {
  requestId: string;
  method: string;
  params: unknown;
  /** Codex item id (`itemId` or legacy `callId`) when the request concerns an item. */
  itemId?: string;
  receivedAt: string;
}
export type ServerRequestAnswer =
  | { kind: "approval"; verdict: "allow" | "deny" | "allowForSession" }
  | { kind: "userInput"; answers: Record<string, { answers: string[] }> }
  | { kind: "elicitation"; action: "accept" | "decline" | "cancel"; content?: unknown };
export interface SupervisorRequestPort {
  pendingRequests(workerId: string, generation: string): Promise<readonly PendingServerRequest[]>;
  answerRequest(workerId: string, generation: string, requestId: string, answer: ServerRequestAnswer): Promise<{ sent: true }>;
}

/** The user's chosen Codex approval policy and sandbox mode (TYPES §12 `PolicySelection`). */
/**
 * The sole engine under D-GOV-43. A project manifest's `enabledAdapterIds`
 * remains a compatibility record for other adapters; it never gates Codex.
 */
export const CODEX_ENGINE_ADAPTER_ID = "codex-app-server";
export interface PolicySelection {
  approvalPolicy: "untrusted" | "on-request" | "never";
  sandbox: "read-only" | "workspace-write" | "danger-full-access";
}
export type DelegatedPermissionMode = "readOnly" | "ask" | "workspaceWrite" | "bypass";
/** Fixed mapping from the App's permission mode to the Codex policy; grants nothing by itself. */
export function policySelectionFromPermissionMode(mode: DelegatedPermissionMode | undefined): PolicySelection {
  switch (mode) {
    case "readOnly": return { approvalPolicy: "on-request", sandbox: "read-only" };
    case "workspaceWrite": return { approvalPolicy: "never", sandbox: "workspace-write" };
    case "bypass": return { approvalPolicy: "never", sandbox: "danger-full-access" };
    case "ask":
    case undefined:
      return { approvalPolicy: "on-request", sandbox: "workspace-write" };
  }
}

/** A supervisor can steer only its exact live Runtime worker generation. */
export interface SupervisorSteerPort {
  steerTurn(workerId: string, generation: string, request: import("./protocol.js").SessionSteerRequest): Promise<import("./protocol.js").SessionSteerResponse>;
}
