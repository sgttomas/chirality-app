import type { EngineSelection, SessionRecord } from "./harness/types.js";
import type { HarnessOpts } from "./harness/types.js";
import type {
  ChiralityRoleName,
  MethodReference,
  QualifiedMethodReference
} from "./v3.js";

export interface RuntimeSessionRecord extends SessionRecord {
  schemaVersion: "chirality.session/v2" | "chirality.session/v3";
  projectId: string;
  projectRoot: string;
  sessionId: string;
  createdAt: string;
  updatedAt: string;
  role: "agent0" | "agent1" | "agent2";
  roleId?: ChiralityRoleName;
  interactionMode?: "chat" | "native-plan";
  permissionMode?: "readOnly" | "ask" | "workspaceWrite" | "bypass";
  selectedMethods?: readonly QualifiedMethodReference[];
  methodSelectionRevision?: number;
  instructionBasisId?: string;
  parentSessionId?: string;
  engineSelection: EngineSelection;
  /** Session-fixed reasoning effort chosen from the authenticated catalog; additive, no schema bump. */
  reasoningEffort?: string;
  /** Model actually used by the most recent turn (a per-turn override does not change `engineSelection`). */
  lastUsedModel?: string;
  /** Reasoning effort actually used by the most recent turn. */
  lastUsedReasoningEffort?: string;
  engineSessionId?: string;
  residencyEpoch?: string;
  status: "idle" | "running" | "completed" | "failed" | "interrupted";
  legacy?: {
    sourcePath: string;
    migratedAt: string;
  };
}

/** Additive v3 reader shape; v2 records remain accepted during migration. */
export interface RuntimeSessionRecordV3 extends Omit<RuntimeSessionRecord, "schemaVersion" | "roleId" | "interactionMode" | "permissionMode" | "selectedMethods" | "methodSelectionRevision" | "instructionBasisId"> {
  schemaVersion: "chirality.session/v3";
  roleId: ChiralityRoleName;
  agentType: 0 | 1 | 2;
  interactionMode: "chat" | "native-plan";
  permissionMode: "readOnly" | "ask" | "workspaceWrite" | "bypass";
  selectedMethods: readonly QualifiedMethodReference[];
  methodSelectionRevision: number;
  instructionBasisId: string;
}

export type ReadableRuntimeSessionRecord = RuntimeSessionRecord | RuntimeSessionRecordV3;

export interface CreateSessionRequest {
  projectId: string;
  role?: RuntimeSessionRecord["role"];
  roleId?: ChiralityRoleName;
  interactionMode?: "chat" | "native-plan";
  permissionMode?: "readOnly" | "ask" | "workspaceWrite" | "bypass";
  selectedMethods?: readonly MethodReference[];
  engineSelection?: EngineSelection;
  /** Catalog choice resolved by the daemon session policy; mutually exclusive with explicit engineSelection. */
  modelSelection?: { model: string; reasoningEffort: string };
  persona?: string;
  mode?: string;
  parentSessionId?: string;
  approvalRef?: string;
  declaredContext?: string[];
  allowedWriteTargets?: string[];
}

export interface SessionTurnRequest {
  message?: string;
  prompt?: string;
  opts?: HarnessOpts;
  attachments?: string[];
  turnId?: string;
  interactionMode?: "chat" | "native-plan";
  permissionMode?: "readOnly" | "ask" | "workspaceWrite" | "bypass";
  /** Per-turn model override; the session's engine selection remains the default. */
  model?: string;
  /** Per-turn reasoning effort override. */
  reasoningEffort?: string;
  methods?: readonly MethodReference[];
  /** Compatibility selector normalized through the legacy method adapter. */
  workflow?: string;
  /** Legacy compatibility selector; accepted only through convertedWorkflowAliases. */
  taskSkill?: string;
}
