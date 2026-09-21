import { createHash } from 'node:crypto';
import type { EngineAdapterSubject } from '@chirality/runtime-contracts/agent-engine-port';
import type { HarnessEventType } from '@chirality/runtime-contracts/event-schema';
import type {
  GovernanceGateId,
  SubagentGovernanceDecision
} from './subagent-governance';
import type { ResolvedOpts, SessionRecord } from '@chirality/runtime-contracts/types';

export const AGENT_SUBAGENT_CONTRACT_VERSION = 1 as const;

export const CHILD_RUN_EVENT_TYPES = [
  'subagent.started',
  'subagent.progress',
  'subagent.completed',
  'subagent.failed'
] as const satisfies readonly HarnessEventType[];

export const AGENT_SUBAGENT_PREREQUISITE_POSTURE = {
  executableDelegation: 'blocked',
  childDefinitions: 'contract-only',
  patternCorpusRuntime: 'reference-only',
  concreteProviderRouting: 'blocked',
  childCapabilityInheritance: 'blocked'
} as const;

export type ChildRunStatus =
  | 'queued'
  | 'denied'
  | 'running'
  | 'completed'
  | 'failed'
  | 'cancelled';

export type ChildRunCapability =
  | 'read'
  | 'write'
  | 'shell'
  | 'mcp'
  | 'network'
  | 'subagent';

export type ChildRunCapabilityPolicy = {
  inheritParentCapabilities: false;
  requestedToolNames: string[];
  allowedToolNames: string[];
  deniedCapabilities: ChildRunCapability[];
};

export type ChildRunGovernanceState = 'allowed' | 'denied' | 'adapter-observed';

export type ChildRunGovernance = {
  state: ChildRunGovernanceState;
  gate?: GovernanceGateId;
  reason?: string;
  approvalRef?: string;
  approvedBy?: string;
  allowlistedSubagents: string[];
  delegatedSubagents: string[];
};

export type ChildRunAdapterMetadata = {
  adapterName: EngineAdapterSubject | string;
  adapterSessionId?: string;
  adapterAgentId?: string;
  adapterTaskId?: string;
  adapterToolUseId?: string;
  adapterTranscriptKey?: string;
};

export type ChildRunRecord = {
  contractVersion: typeof AGENT_SUBAGENT_CONTRACT_VERSION;
  childRunId: string;
  parentSessionId: string;
  parentTurnId?: string;
  parentPersona: string;
  agentName: string;
  projectRoot: string;
  mode: string;
  status: ChildRunStatus;
  capabilityPolicy: ChildRunCapabilityPolicy;
  governance: ChildRunGovernance;
  outputArtifactPath?: string;
  adapter?: ChildRunAdapterMetadata;
};

export type ChildRunContractIssueCode =
  | 'MISSING_CHILD_RUN_ID'
  | 'MISSING_PARENT_SESSION_ID'
  | 'MISSING_AGENT_NAME'
  | 'CAPABILITY_INHERITANCE_NOT_BLOCKED'
  | 'QUEUED_WITHOUT_GOVERNANCE_ALLOW'
  | 'DENIED_WITHOUT_GOVERNANCE_DENY'
  | 'COMPLETED_WITHOUT_OUTPUT_ARTIFACT';

export type ChildRunContractIssue = {
  code: ChildRunContractIssueCode;
  message: string;
};

export type ChildRunContractReport = {
  passed: boolean;
  issues: ChildRunContractIssue[];
};

function sortedUnique(values: readonly string[] | undefined): string[] {
  return [...new Set((values ?? []).map((value) => value.trim()).filter(Boolean))].sort();
}

function createStableChildRunId(input: {
  parentSessionId: string;
  parentTurnId?: string;
  agentName: string;
  approvalRef?: string;
}): string {
  const hash = createHash('sha256')
    .update(
      JSON.stringify([
        input.parentSessionId,
        input.parentTurnId ?? '',
        input.agentName,
        input.approvalRef ?? ''
      ])
    )
    .digest('hex')
    .slice(0, 16);

  return `child_${hash}`;
}

function governanceAllowsAgent(
  agentName: string,
  decision: SubagentGovernanceDecision
): boolean {
  return decision.allowed && decision.delegatedSubagents.includes(agentName);
}

export function createDelegationChildRunRecord(input: {
  session: SessionRecord;
  opts: ResolvedOpts;
  agentName: string;
  governanceDecision: SubagentGovernanceDecision;
  parentTurnId?: string;
  requestedToolNames?: string[];
}): ChildRunRecord {
  const allowed = governanceAllowsAgent(input.agentName, input.governanceDecision);
  const governanceState: ChildRunGovernanceState = allowed ? 'allowed' : 'denied';
  const requestedToolNames = sortedUnique(input.requestedToolNames);

  return {
    contractVersion: AGENT_SUBAGENT_CONTRACT_VERSION,
    childRunId: createStableChildRunId({
      parentSessionId: input.session.sessionId,
      parentTurnId: input.parentTurnId,
      agentName: input.agentName,
      approvalRef: input.governanceDecision.approvalRef
    }),
    parentSessionId: input.session.sessionId,
    parentTurnId: input.parentTurnId,
    parentPersona: input.opts.persona,
    agentName: input.agentName,
    projectRoot: input.session.projectRoot,
    mode: input.opts.mode,
    status: allowed ? 'queued' : 'denied',
    capabilityPolicy: {
      inheritParentCapabilities: false,
      requestedToolNames,
      allowedToolNames: [],
      deniedCapabilities: ['read', 'write', 'shell', 'mcp', 'network', 'subagent']
    },
    governance: {
      state: governanceState,
      gate: allowed ? 'ALLOW' : input.governanceDecision.gate,
      reason: allowed
        ? 'Delegation passed governance preflight; executable exposure remains blocked by prerequisite posture.'
        : input.governanceDecision.reason,
      approvalRef: input.governanceDecision.approvalRef,
      approvedBy: input.governanceDecision.approvedBy,
      allowlistedSubagents: [...input.governanceDecision.allowlistedSubagents],
      delegatedSubagents: [...input.governanceDecision.delegatedSubagents]
    }
  };
}

export function createAdapterObservedChildRunRecord(input: {
  parentSessionId: string;
  parentPersona: string;
  agentName: string;
  projectRoot: string;
  mode: string;
  status: ChildRunStatus;
  parentTurnId?: string;
  outputArtifactPath?: string;
  adapter: ChildRunAdapterMetadata;
}): ChildRunRecord {
  return {
    contractVersion: AGENT_SUBAGENT_CONTRACT_VERSION,
    childRunId: createStableChildRunId({
      parentSessionId: input.parentSessionId,
      parentTurnId: input.parentTurnId,
      agentName: input.agentName,
      approvalRef: input.adapter.adapterTaskId ?? input.adapter.adapterToolUseId
    }),
    parentSessionId: input.parentSessionId,
    parentTurnId: input.parentTurnId,
    parentPersona: input.parentPersona,
    agentName: input.agentName,
    projectRoot: input.projectRoot,
    mode: input.mode,
    status: input.status,
    capabilityPolicy: {
      inheritParentCapabilities: false,
      requestedToolNames: [],
      allowedToolNames: [],
      deniedCapabilities: ['read', 'write', 'shell', 'mcp', 'network', 'subagent']
    },
    governance: {
      state: 'adapter-observed',
      reason: 'Adapter child-run evidence observed; Chirality governance is recorded separately.',
      allowlistedSubagents: [],
      delegatedSubagents: []
    },
    outputArtifactPath: input.outputArtifactPath,
    adapter: input.adapter
  };
}

export function providerNeutralChildRunRecord(
  record: ChildRunRecord
): Omit<ChildRunRecord, 'adapter'> {
  const { adapter: _adapter, ...providerNeutral } = record;
  return providerNeutral;
}

export function childRunRecordToEventData(record: ChildRunRecord): Record<string, unknown> {
  return {
    ...providerNeutralChildRunRecord(record),
    ...(record.adapter ? { adapter: record.adapter } : {})
  };
}

export function validateChildRunRecord(record: ChildRunRecord): ChildRunContractReport {
  const issues: ChildRunContractIssue[] = [];

  if (!record.childRunId) {
    issues.push({
      code: 'MISSING_CHILD_RUN_ID',
      message: 'Child run record must include a stable childRunId.'
    });
  }
  if (!record.parentSessionId) {
    issues.push({
      code: 'MISSING_PARENT_SESSION_ID',
      message: 'Child run record must include parentSessionId.'
    });
  }
  if (!record.agentName) {
    issues.push({
      code: 'MISSING_AGENT_NAME',
      message: 'Child run record must name the requested child agent.'
    });
  }
  if (record.capabilityPolicy.inheritParentCapabilities !== false) {
    issues.push({
      code: 'CAPABILITY_INHERITANCE_NOT_BLOCKED',
      message: 'Child runs must not inherit parent capabilities by default.'
    });
  }
  if (record.status === 'queued' && record.governance.state !== 'allowed') {
    issues.push({
      code: 'QUEUED_WITHOUT_GOVERNANCE_ALLOW',
      message: 'Queued child runs require an allowed governance state.'
    });
  }
  if (record.status === 'denied' && record.governance.state !== 'denied') {
    issues.push({
      code: 'DENIED_WITHOUT_GOVERNANCE_DENY',
      message: 'Denied child runs require a denied governance state.'
    });
  }
  if (record.status === 'completed' && !record.outputArtifactPath) {
    issues.push({
      code: 'COMPLETED_WITHOUT_OUTPUT_ARTIFACT',
      message: 'Completed child runs must carry an output artifact reference.'
    });
  }

  return {
    passed: issues.length === 0,
    issues
  };
}
