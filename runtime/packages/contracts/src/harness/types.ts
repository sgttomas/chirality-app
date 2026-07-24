import type { HarnessEvent } from './event-schema.js';

export type HarnessErrorType =
  | 'INVALID_REQUEST'
  | 'TURN_IN_PROGRESS'
  | 'MISSING_API_KEY'
  | 'SESSION_NOT_FOUND'
  | 'PERSONA_NOT_FOUND'
  | 'INSTRUCTION_ROOT_INVALID'
  | 'SDK_FAILURE'
  | 'ENGINE_UNAVAILABLE'
  | 'MODEL_UNAVAILABLE'
  | 'PROVIDER_AUTH_FAILURE'
  | 'PROVIDER_PROTOCOL_FAILURE'
  | 'CONTEXT_EXHAUSTED'
  | 'WORKING_ROOT_INACCESSIBLE'
  | 'WORKING_ROOT_CONFLICT'
  | 'ATTACHMENT_FAILURE';

export interface HarnessErrorResponse {
  error: {
    type: HarnessErrorType;
    message: string;
    details?: unknown;
  };
}

export interface SessionRecord {
  sessionId: string;
  projectRoot: string;
  persona: string;
  mode: string;
  createdAt: string;
  updatedAt: string;
  engineSelection?: EngineSelection;
  adapterSession?: AdapterSessionMetadata;
  engineSessionId?: string;
  claudeSessionId?: string;
  sdkSessionId?: string;
  sdkTranscriptPath?: string;
  sdkSessionStoreKey?: string;
  sdkConfigDir?: string;
  sdkSettingSources?: string[];
  sdkPackageVersion?: string;
  sdkClaudeCodeVersion?: string;
  bootFingerprint?: string;
  runtimeFingerprint?: HarnessRuntimeFingerprint;
  bootedAt?: string;
  model?: string;
  orchestrationRunId?: string;
  executionRoot?: string;
  agentInstanceId?: string;
  parentSessionId?: string;
  parentInstanceId?: string;
  parentAgentType?: 0 | 1;
  agentType?: 0 | 1 | 2;
  childKind?: 'named' | 'task' | 'generalist';
  planVersion?: string;
  approvalRef?: string;
  instructionPath?: string;
  instructionHash?: string;
  briefHash?: string;
  declaredContext?: string[];
  declaredTools?: string[];
  allowedWriteTargets?: string[];
  outputArtifact?: string;
  childRunStatus?: 'LAUNCHED' | 'RUNNING' | 'COMPLETED' | 'FAILED' | 'BLOCKED';
}

export interface EngineSelection {
  adapterId: string;
  providerId: string;
  model: string;
}

export interface AdapterSessionMetadata {
  engineSessionId?: string;
  transcriptPath?: string;
  storeKey?: string;
  configDir?: string;
  packageName?: string;
  packageVersion?: string;
}

export interface SessionCreateRequest {
  projectRoot: string;
  persona?: string;
  mode?: string;
}

export type CoordinationMode = 'SCHEDULE_FIRST' | 'DEPENDENCY_TRACKED' | 'HYBRID';

export interface ScaffoldExecutionRootRequest {
  executionRoot: string;
  decompositionPath: string;
  projectName?: string;
  coordinationMode?: CoordinationMode;
}

export interface ScaffoldLayoutValidationItem {
  id: string;
  path: string;
  valid: boolean;
  missing: string[];
}

export interface ScaffoldLayoutValidation {
  valid: boolean;
  executionRoot: {
    path: string;
    valid: boolean;
    missing: string[];
  };
  packages: ScaffoldLayoutValidationItem[];
  deliverables: ScaffoldLayoutValidationItem[];
}

export interface ScaffoldPreparationCompatibilityItem {
  id: string;
  path: string;
  ready: boolean;
  issues: string[];
}

export interface ScaffoldPreparationCompatibility {
  ready: boolean;
  deliverablesChecked: number;
  issueCount: number;
  deliverables: ScaffoldPreparationCompatibilityItem[];
}

export interface ScaffoldExecutionRootResponse {
  executionRoot: string;
  decompositionPath: string;
  copiedDecompositionPath: string;
  projectName: string;
  coordinationMode: CoordinationMode;
  packageCount: number;
  deliverableCount: number;
  created: {
    directories: string[];
    files: string[];
  };
  layoutValidation: ScaffoldLayoutValidation;
  preparationCompatibility: ScaffoldPreparationCompatibility;
}

export interface SessionBootRequest {
  sessionId: string;
  opts?: HarnessOpts;
}

export interface SessionListResponse {
  sessions: SessionRecord[];
}

export interface BootMetadata {
  engineSessionId: string;
  adapterId: string;
  providerId: string;
  model: string;
  claudeSessionId?: string;
  bootFingerprint: string;
  runtimeFingerprint: HarnessRuntimeFingerprint;
  bootedAt: string;
}

export interface SessionBootResponse {
  session: SessionRecord;
  boot: BootMetadata;
}

export interface HarnessRuntimeFingerprintMcpServer {
  name: string;
  version: string;
  toolNames: string[];
}

export interface HarnessRuntimeFingerprint {
  schemaVersion: string;
  personaComposerVersion: string;
  permissionPolicyVersion: string;
  managedDelegationPolicyVersion: string;
  subagentPolicyVersion: string;
  toolRegistryVersion: string;
  sdkPackageVersion: string;
  engineAdapter?: {
    adapterId: string;
    providerId: string;
    model: string;
    packageName?: string;
    packageVersion?: string;
  };
  mcpServers: HarnessRuntimeFingerprintMcpServer[];
  fingerprintSha256: string;
}

export interface TurnRequest {
  sessionId: string;
  message: string;
  opts?: HarnessOpts;
  attachments?: string[];
}

export interface InterruptRequest {
  sessionId: string;
}

export interface HarnessOpts {
  model?: string;
  tools?: string[];
  maxTurns?: number;
  persona?: string;
  mode?: string;
  subagentGovernance?: unknown;
}

export interface ResolvedOpts {
  model: string;
  tools: string[];
  maxTurns: number;
  persona: string;
  mode: string;
  subagentGovernance?: unknown;
  delegatedSubagents?: string[];
  delegatedAgentInstructions?: Record<string, {
    path: string;
    content: string;
    sha256: string;
    agentType: 1 | 2;
  }>;
}

export type ContentBlock =
  | {
      type: 'text';
      text: string;
    }
  | {
      type: 'file';
      path: string;
      mimeType: string;
    };

export interface AttachmentError {
  path: string;
  reason: string;
}

export interface AttachmentFailureDetails {
  category: 'ALL_ATTACHMENTS_FAILED_NO_TEXT';
  attachmentErrors: AttachmentError[];
  rejectedAttachmentCount: number;
}

export interface ResolvedAttachments {
  contentBlocks: ContentBlock[];
  errors: AttachmentError[];
}

export type TurnErrorSeverity = 'warning' | 'error';

export type UIEvent =
  | {
      type: 'session:init';
      data: {
        engineSessionId: string;
        adapterId: string;
        providerId: string;
        claudeSessionId?: string;
        model: string;
      };
    }
  | {
      type: 'chat:delta';
      data: {
        text: string;
      };
    }
  | {
      type: 'chat:complete';
      data: {
        text: string;
      };
    }
  | {
      type: 'tool:result';
      data: {
        name: string;
        ok: boolean;
        output?: string;
      };
    }
  | {
      type: 'session:complete';
      data: Record<string, never>;
    }
  | {
      type: 'turn:error';
      data: {
        phase: 'mid-stream';
        errorType: HarnessErrorType;
        message: string;
        status: number;
        severity: TurnErrorSeverity;
        fatal: boolean;
        details?: unknown;
      };
    }
  | {
      type: 'process:exit';
      data: {
        exitCode: number;
        interrupted?: boolean;
        error?: string;
        errorType?: string;
        status?: number;
        severity?: TurnErrorSeverity;
        fatal?: boolean;
        errorDetails?: unknown;
      };
    }
  | {
      // Provider-neutral passthrough of a rich, redacted HarnessEvent. Carries the
      // same shape persisted to events.jsonl so the live stream and replay log are
      // identical. The browser may ignore types it does not render. See
      // harness-ui-bridge.ts for which HarnessEvent types are forwarded.
      type: 'harness:event';
      data: HarnessEvent;
    };

export interface ISessionManager {
  create(input: SessionCreateRequest): Promise<SessionRecord>;
  resume(sessionId: string): Promise<SessionRecord>;
  getById(sessionId: string): Promise<SessionRecord>;
  save(sessionId: string, updates: Partial<SessionRecord>): Promise<SessionRecord>;
  list(projectRoot: string): Promise<SessionRecord[]>;
  delete(sessionId: string): Promise<void>;
}

export interface IPersonaManager {
  buildSystemPrompt(
    projectRoot: string,
    persona: string,
    mode: string,
    tools?: readonly string[]
  ): Promise<string>;
  getBootFingerprint(
    persona: string,
    mode: string,
    projectRoot?: string,
    tools?: readonly string[]
  ): string;
}

export interface IAttachmentResolver {
  resolveAttachmentsToContentBlocks(
    message: string,
    attachmentPaths: string[]
  ): Promise<ResolvedAttachments>;
}

/** @deprecated Use AgentEnginePort for new runtime adapters. */
export interface IAgentSdkManager {
  startTurn(
    session: SessionRecord,
    message: string,
    opts: ResolvedOpts,
    contentBlocks?: ContentBlock[]
  ): AsyncIterable<UIEvent>;
  interrupt(sessionId: string): Promise<void>;
}
