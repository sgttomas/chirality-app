import type { HarnessEvent } from '@chirality/runtime-contracts/event-schema';
import type { TranscriptView } from '@chirality/runtime-contracts/transcript-replay';
import type {
  ChiralityRoleName,
  FrozenInstructionBasisV3,
  InstructionHistoryRecordV3,
  QualifiedMethodReference
} from '@chirality/runtime-contracts/v3';

export type ProjectionCurrency = 'CURRENT' | 'STALE' | 'CONFLICTING' | 'UNKNOWN';

export type CoordinationWorkClass =
  | 'GOVERNED_PROJECT'
  | 'HUMAN_APPROVED_EXECUTION'
  | 'AGENT_WORKING_PROPOSAL'
  | 'RUNTIME_EPHEMERAL';

export type ProjectionDiagnostic = {
  code: string;
  message: string;
  sourceReference?: string;
};

export type CoordinationWorkItem = {
  id: string;
  title: string;
  workClass: CoordinationWorkClass;
  sourceReference: string;
  statusBasis: string;
  currency: ProjectionCurrency;
  statusLabel?: string;
  responsibleReference?: string;
  relatedReferences: string[];
  runtimeStatus?: string;
  lifecycleStatus?: string;
};

export type ParentageProjection =
  | {
      state: 'RECORDED';
      parentSessionId: string;
      parentAvailable: boolean;
    }
  | {
      state: 'NOT_RECORDED';
    };

export type OperatorSessionProjection = {
  projectionId: string;
  sourceReference: string;
  sessionId: string;
  observedAt: string;
  currency: ProjectionCurrency;
  persona?: string;
  role?: 'agent0' | 'agent1' | 'agent2';
  /** Defined by current readers; missing legacy projection keeps compatibility behavior. */
  bootstrapConfirmed?: boolean;
  runtimeStatus?: 'idle' | 'running' | 'completed' | 'failed' | 'interrupted';
  adapterId?: string;
  providerId?: string;
  model?: string;
  /** Session-fixed reasoning effort recorded with the model (Codex catalog sessions). */
  reasoningEffort?: string;
  residencyEpoch?: string;
  parentage: ParentageProjection;
  outputArtifactReference?: string;
  approvalEvidenceReference?: string;
  continuation?: {
    schemaVersion: 'chirality.session/v3';
    projectRoot: string;
    roleId: ChiralityRoleName;
    mode: string;
    interactionMode: 'chat' | 'native-plan';
    permissionMode: 'readOnly' | 'ask' | 'workspaceWrite' | 'bypass';
    selectedMethods: readonly QualifiedMethodReference[];
    methodSelectionRevision: number;
    instructionBasisId: string;
  };
  diagnostics: ProjectionDiagnostic[];
};

export type RecordedAgentHierarchy = {
  roots: OperatorSessionProjection[];
  detached: OperatorSessionProjection[];
  childrenByParentSessionId: Record<string, OperatorSessionProjection[]>;
  unresolvedParentSessionIds: string[];
  diagnostics: ProjectionDiagnostic[];
};

export type ReplayDisclosure =
  | 'READY_SNAPSHOT'
  | 'EMPTY'
  | 'EVIDENCE_ONLY'
  | 'MALFORMED'
  | 'BOUNDED'
  | 'STALE'
  | 'UNAVAILABLE'
  | 'CONFLICTING'
  | 'UNKNOWN';

export type SelectedSessionReplayProjection = {
  selectedSessionId: string;
  sourceReference: string;
  observedAt: string;
  disclosure: ReplayDisclosure;
  currency: ProjectionCurrency;
  session?: OperatorSessionProjection;
  transcript: TranscriptView;
  events?: readonly HarnessEvent[];
  instructionHistory: readonly InstructionHistoryRecordV3[];
  instructionBases: readonly FrozenInstructionBasisV3[];
  malformedLineCount: number;
  sourceEventCount: number;
  renderedItemCount: number;
  bounded?: {
    rendered: number;
    available: number;
  };
  diagnostics: ProjectionDiagnostic[];
};

export type SelectedSessionReplayState =
  | {
      status: 'IDLE';
    }
  | {
      status: 'LOADING';
      selectedSessionId: string;
    }
  | {
      status: 'READY';
      projection: SelectedSessionReplayProjection;
    }
  | {
      status: 'UNAVAILABLE';
      selectedSessionId: string;
      message: string;
    };

export type CoordinationPanelView = 'work' | 'agents';
