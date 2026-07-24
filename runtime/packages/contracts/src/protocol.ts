import type { EngineSelection, HarnessOpts } from "./harness/types.js";
import type {
  HarnessEvent,
  ScaffoldExecutionRootResponse,
  TranscriptView,
  UIEvent
} from "./harness/index.js";
import type { EngineDescriptor } from "./harness/agent-engine-port.js";
import type { RuntimeSessionRecord } from "./session.js";
import type { ProjectStatus } from "./project.js";
import type { ResidencyStatus } from "./residency.js";

export const RUNTIME_API_VERSION = "v1" as const;

export const RUNTIME_ROUTES = {
  health: "/v1/health",
  daemonStatus: "/v1/daemon/status",
  projects: "/v1/projects",
  projectRegister: "/v1/projects/register",
  projectStatus: (projectId: string) => `/v1/projects/${encodeURIComponent(projectId)}/status`,
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
  requestId: string;
  decision: "allow" | "deny";
  reason?: string;
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

export type RuntimeSseFrame = UIEvent;
