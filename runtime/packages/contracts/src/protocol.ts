import type { EngineSelection, HarnessOpts } from "./harness/types.js";
import type {
  HarnessEvent,
  ScaffoldExecutionRootResponse,
  TranscriptView,
  UIEvent
} from "./harness/index.js";
import type { EngineDescriptor } from "./harness/agent-engine-port.js";
import type { RuntimeSessionRecord } from "./session.js";
import type { PendingServerRequest, ServerRequestAnswer } from "./delegated.js";
import { RuntimeError } from "./errors.js";
import type { FrozenInstructionBasisV3, InstructionHistoryRecordV3 } from "./v3.js";
import type { ProjectStatus } from "./project.js";
import type { ResidencyStatus } from "./residency.js";

export const RUNTIME_API_VERSION = "v1" as const;

export const RUNTIME_ROUTES = {
  health: "/v1/health",
  daemonStatus: "/v1/daemon/status",
  projects: "/v1/projects",
  projectRegister: "/v1/projects/register",
  hostedBootstrapProjectRegister: "/v3/hosted-bootstrap/projects/register",
  hostedBootstrapProjectInitialize: "/v3/hosted-bootstrap/projects/initialize",
  projectStatus: (projectId: string) => `/v1/projects/${encodeURIComponent(projectId)}/status`,
  hostedBootstrapStatus: (projectId: string) => `/v3/projects/${encodeURIComponent(projectId)}/hosted-bootstrap/status`,
  hostedBootstrapConsent: (projectId: string) => `/v3/projects/${encodeURIComponent(projectId)}/hosted-bootstrap/provider-network-consent`,
  hostedBootstrapLoginStart: (projectId: string) => `/v3/projects/${encodeURIComponent(projectId)}/hosted-bootstrap/login/start`,
  hostedBootstrapLoginCancel: (projectId: string) => `/v3/projects/${encodeURIComponent(projectId)}/hosted-bootstrap/login/cancel`,
  /** Project-local supplier sign-out; it does not assert account-wide revocation. */
  hostedBootstrapLogout: (projectId: string) => `/v3/projects/${encodeURIComponent(projectId)}/hosted-bootstrap/logout`,
  roles: (projectId: string) => `/v1/projects/${encodeURIComponent(projectId)}/roles`,
  methods: (projectId: string) => `/v1/projects/${encodeURIComponent(projectId)}/methods`,
  method: (projectId: string, qualifiedId: string) =>
    `/v1/projects/${encodeURIComponent(projectId)}/methods/${encodeURIComponent(qualifiedId)}`,
  sessions: (projectId: string) => `/v1/projects/${encodeURIComponent(projectId)}/sessions`,
  session: (projectId: string, sessionId: string) =>
    `/v1/projects/${encodeURIComponent(projectId)}/sessions/${encodeURIComponent(sessionId)}`,
  sessionBoot: (projectId: string, sessionId: string) =>
    `${RUNTIME_ROUTES.session(projectId, sessionId)}/boot`,
  sessionReplay: (projectId: string, sessionId: string) =>
    `${RUNTIME_ROUTES.session(projectId, sessionId)}/replay`,
  sessionTurn: (projectId: string, sessionId: string) =>
    `${RUNTIME_ROUTES.session(projectId, sessionId)}/turn`,
  sessionInterrupt: (projectId: string, sessionId: string) =>
    `${RUNTIME_ROUTES.session(projectId, sessionId)}/interrupt`,
  sessionPermission: (projectId: string, sessionId: string) =>
    `${RUNTIME_ROUTES.session(projectId, sessionId)}/permission`,
  /** Attach to the active (or recently finished) turn owned by the Runtime; SSE. */
  sessionTurnStream: (projectId: string, sessionId: string) =>
    `${RUNTIME_ROUTES.sessionTurn(projectId, sessionId)}/stream`,
  sessionTurnSteer: (projectId: string, sessionId: string) =>
    `${RUNTIME_ROUTES.sessionTurn(projectId, sessionId)}/steer`,
  sessionTurnSteerReceipt: (projectId: string, sessionId: string) =>
    `${RUNTIME_ROUTES.sessionTurnSteer(projectId, sessionId)}/receipt`,
  sessionTurnState: (projectId: string, sessionId: string) =>
    `${RUNTIME_ROUTES.sessionTurn(projectId, sessionId)}/state`,
  sessionRequests: (projectId: string, sessionId: string) =>
    `${RUNTIME_ROUTES.session(projectId, sessionId)}/requests`,
  sessionRequestAnswer: (projectId: string, sessionId: string, requestId: string) =>
    `${RUNTIME_ROUTES.sessionRequests(projectId, sessionId)}/${encodeURIComponent(requestId)}/answer`,
  sessionContextResolve: (projectId: string, sessionId: string) =>
    `${RUNTIME_ROUTES.session(projectId, sessionId)}/context/resolve`,
  sessionMethods: (projectId: string, sessionId: string) =>
    `${RUNTIME_ROUTES.session(projectId, sessionId)}/methods`,
  applicationTools: (projectId: string, sessionId: string) =>
    `${RUNTIME_ROUTES.session(projectId, sessionId)}/application-tools`,
  applicationToolCalls: (projectId: string, sessionId: string) =>
    `${RUNTIME_ROUTES.applicationTools(projectId, sessionId)}/calls`,
  applicationToolResult: (projectId: string, sessionId: string, invocationId: string) =>
    `${RUNTIME_ROUTES.applicationToolCalls(projectId, sessionId)}/${encodeURIComponent(invocationId)}/result`,
  nativePlanCapability: (projectId: string, sessionId: string) =>
    `${RUNTIME_ROUTES.session(projectId, sessionId)}/native-plan/capability`,
  nativePlanRevisions: (projectId: string, sessionId: string) =>
    `${RUNTIME_ROUTES.session(projectId, sessionId)}/native-plan/revisions`,
  nativePlanExport: (projectId: string, sessionId: string) =>
    `${RUNTIME_ROUTES.session(projectId, sessionId)}/native-plan/export`,
  nativePlanClarifications: (projectId: string, sessionId: string) =>
    `${RUNTIME_ROUTES.session(projectId, sessionId)}/native-plan/clarifications`,
  nativePlanClarificationReply: (projectId: string, sessionId: string) =>
    `${RUNTIME_ROUTES.nativePlanClarifications(projectId, sessionId)}/reply`,
  agents: (projectId: string) => `/v1/projects/${encodeURIComponent(projectId)}/agents`,
  scaffold: (projectId: string) => `/v1/projects/${encodeURIComponent(projectId)}/scaffold`,
  runs: (projectId: string) => `/v1/projects/${encodeURIComponent(projectId)}/runs`,
  models: "/v1/models",
  modelActivate: (modelId: string) => `/v1/models/${encodeURIComponent(modelId)}/activate`,
  credentials: (providerId: string) => `/v1/credentials/${encodeURIComponent(providerId)}`
} as const;

export interface ProjectRegistrationRequest {
  manifestPath: string;
  approvedBy: string;
  approvalReference: string;
}
export interface HostedBootstrapProjectRegistrationRequest { manifestPath: string }
export interface HostedBootstrapProjectInitializationRequest { projectRoot: string }

/** Safe renderer-facing binding. Project client credentials remain host-only. */
export interface HostedBootstrapProjectRegistrationResponse {
  projectId: string;
  manifestHash: string;
}

export interface ProjectRegistrationResponse {
  projectId: string;
  clientId: string;
  tokenFile: string;
  manifestHash: string;
}

export interface Agent1RunRequest {
  brief: string;
  localModel?: string;
  agentId?: string;
  approvalReference: string;
  readOnlyTool?: {
    name: "read_file";
    relativePath: string;
  };
}

export interface Agent2DelegationReturn {
  childSessionId: string;
  childRole: "agent2";
  selection: EngineSelection;
  toolName: "read_file";
  sealedBriefHash: string;
  evidence: Readonly<Record<string, unknown>>;
  returnText: string;
  reviewed: boolean;
  acceptance: "accepted" | "rejected";
}

export interface Agent1EngineOutcome {
  managerText: string;
  delegations: readonly Agent2DelegationReturn[];
  managerSession: RuntimeSessionRecord;
}

export interface RuntimeSessionBootRequest {
  expectedSelection?: EngineSelection;
  opts?: HarnessOpts;
}

export interface PermissionDecisionRequest {
  /** Tool-use id of the gated call; for Codex approvals this is the item id carried by `tool.permission`. */
  requestId: string;
  decision: "allow" | "deny";
  reason?: string;
}

/** Runtime-owned turn state for a session (D-GOV-43 disconnection rule). */
export interface SessionTurnState {
  active: boolean;
  turnId?: string;
  /** Sequence of the last frame buffered for the current or retained turn; 0 when none. */
  lastSeq: number;
  startedAt?: string;
  endedAt?: string;
}
/** Input to an existing Runtime turn. operationId is retained across uncertain acknowledgments. */
export interface SessionSteerRequest {
  operationId: string;
  expectedTurnId: string;
  text: string;
}
/** Receipt lookup only: this request can never submit model input. */
export interface SessionSteerReceiptRequest {
  operationId: string;
  expectedTurnId: string;
}
export function validateSessionSteerReceiptRequest(value: unknown): SessionSteerReceiptRequest {
  if (!plainRecord(value) || Object.keys(value).sort().join(",") !== "expectedTurnId,operationId") {
    throw new RuntimeError("INVALID_REQUEST", "Receipt lookup requires exactly operationId and expectedTurnId", 400);
  }
  const valid = validateSessionSteerRequest({ ...value, text: "receipt lookup" });
  return { operationId: valid.operationId, expectedTurnId: valid.expectedTurnId };
}
export interface SessionSteerResponse {
  operationId: string;
  turnId: string;
  status: "accepted" | "rejected" | "unknown";
  message?: string;
  providerTurnId?: string;
}
export function validateSessionSteerRequest(value: unknown): SessionSteerRequest {
  if (!plainRecord(value) || Object.keys(value).sort().join(",") !== "expectedTurnId,operationId,text"
    || typeof value.operationId !== "string" || !/^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$/u.test(value.operationId)
    || typeof value.expectedTurnId !== "string" || !value.expectedTurnId.trim() || value.expectedTurnId.length > 256
    || typeof value.text !== "string" || !value.text.trim() || value.text.length > 128 * 1024) {
    throw new RuntimeError("INVALID_REQUEST", "Steering requires a bounded operationId, expectedTurnId and nonempty text", 400);
  }
  return { operationId: value.operationId, expectedTurnId: value.expectedTurnId, text: value.text };
}

export interface SessionRequestsResponse {
  requests: readonly PendingServerRequest[];
}
export interface AnswerSessionRequestRequest {
  answer: ServerRequestAnswer;
}
export interface AnswerSessionRequestResponse {
  sent: true;
}

function plainRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

/** Shape gate for a server-request answer; the supervisor decides whether the kind fits the request method. */
export function validateServerRequestAnswer(value: unknown): ServerRequestAnswer {
  const invalid = (message: string) => new RuntimeError("INVALID_REQUEST", message, 400, { reason: "SERVER_REQUEST_ANSWER_INVALID" });
  if (!plainRecord(value) || typeof value.kind !== "string") throw invalid("answer must be an object with a kind");
  const keys = Object.keys(value);
  switch (value.kind) {
    case "approval": {
      if (keys.length !== 2 || !["allow", "deny", "allowForSession"].includes(String(value.verdict))) throw invalid("approval answer requires exactly a verdict of allow, deny or allowForSession");
      return { kind: "approval", verdict: value.verdict as "allow" | "deny" | "allowForSession" };
    }
    case "userInput": {
      if (keys.length !== 2 || !plainRecord(value.answers)) throw invalid("userInput answer requires exactly an answers record");
      const answers: Record<string, { answers: string[] }> = {};
      for (const [questionId, entry] of Object.entries(value.answers)) {
        if (questionId.trim() === "" || !plainRecord(entry) || Object.keys(entry).join(",") !== "answers" || !Array.isArray(entry.answers) || !entry.answers.every(item => typeof item === "string")) {
          throw invalid("userInput answers must map question ids to { answers: string[] }");
        }
        answers[questionId] = { answers: [...(entry.answers as string[])] };
      }
      return { kind: "userInput", answers };
    }
    case "elicitation": {
      const allowed = keys.every(key => ["kind", "action", "content"].includes(key));
      if (!allowed || !["accept", "decline", "cancel"].includes(String(value.action))) throw invalid("elicitation answer requires an action of accept, decline or cancel");
      return { kind: "elicitation", action: value.action as "accept" | "decline" | "cancel", ...(Object.hasOwn(value, "content") ? { content: value.content } : {}) };
    }
    default:
      throw invalid("answer kind must be approval, userInput or elicitation");
  }
}

export function validateAnswerSessionRequestRequest(value: unknown): AnswerSessionRequestRequest {
  if (!plainRecord(value) || Object.keys(value).join(",") !== "answer") throw new RuntimeError("INVALID_REQUEST", "Request body must be exactly { answer }", 400, { reason: "SERVER_REQUEST_ANSWER_INVALID" });
  return { answer: validateServerRequestAnswer(value.answer) };
}

export interface AgentDefinitionSummary {
  name: string;
  type?: 0 | 1 | 2;
  class?: string;
}

export type ScaffoldRequest = import("./harness/types.js").ScaffoldExecutionRootRequest;

export interface HealthResponse {
  apiVersion: typeof RUNTIME_API_VERSION;
  status: "ok";
  daemonId: string;
  pid: number;
}

export interface DaemonStatusResponse extends HealthResponse {
  startedAt: string;
  socketPath: string;
  engines: readonly EngineDescriptor[];
}

export interface ProjectsResponse {
  projects: readonly ProjectStatus[];
}

export interface SessionsResponse {
  sessions: readonly RuntimeSessionRecord[];
}

export interface SessionResponse {
  session: RuntimeSessionRecord;
}

export interface SessionDeleteResponse {
  deleted: true;
  sessionId: string;
}

export interface SessionReplayResponse {
  session: RuntimeSessionRecord;
  events: readonly HarnessEvent[];
  malformedLineCount: number;
  summary: HarnessReplaySummary;
  transcript: TranscriptView;
  instructionHistory: readonly InstructionHistoryRecordV3[];
  instructionBases: readonly FrozenInstructionBasisV3[];
}

export interface HarnessReplaySummary {
  eventCount: number;
  malformedLineCount: number;
  eventTypeCounts: Record<string, number>;
  firstTimestamp?: string;
  lastTimestamp?: string;
}

export interface InterruptResponse {
  interrupted: boolean;
  sessionId: string;
}

export interface PermissionDecisionResponse {
  accepted: true;
  requestId: string;
  decision: "allow" | "deny";
}

export interface AgentsResponse {
  agents: readonly AgentDefinitionSummary[];
}

export interface ScaffoldResponse {
  scaffold: ScaffoldExecutionRootResponse;
}

export interface ModelsResponse {
  residency: ResidencyStatus;
}

export interface CredentialStatusResponse {
  providerId: string;
  configured: boolean;
}

export interface CredentialMutationRequest {
  credential: string;
}

export interface CredentialMutationResponse extends CredentialStatusResponse {}

/** One streamed UI event; `seq` is the Runtime-owned frame sequence (`id:` on the wire) when the stream is a turn subscription. */
export type RuntimeSseFrame = UIEvent & { seq?: number };
