import { describe, expect, it } from 'vitest';
import {
  AGENT_SUBAGENT_PREREQUISITE_POSTURE,
  CHILD_RUN_EVENT_TYPES,
  childRunRecordToEventData,
  createAdapterObservedChildRunRecord,
  createDelegationChildRunRecord,
  providerNeutralChildRunRecord,
  validateChildRunRecord
} from '../../lib/harness/agent-runtime-contract';
import type { SubagentGovernanceDecision } from '../../lib/harness/subagent-governance';
import type { ResolvedOpts, SessionRecord } from '@chirality/runtime-contracts/types';

const session: SessionRecord = {
  sessionId: 'sess_parent',
  projectRoot: '/tmp/chirality-project',
  persona: 'WORKING_ITEMS',
  mode: 'direct',
  createdAt: '2026-06-15T00:00:00.000Z',
  updatedAt: '2026-06-15T00:00:00.000Z'
};

const opts: ResolvedOpts = {
  model: 'claude-test',
  tools: ['read_file', 'bash'],
  maxTurns: 2,
  persona: 'WORKING_ITEMS',
  mode: 'workspaceWrite'
};

const allowedGovernance: SubagentGovernanceDecision = {
  allowed: true,
  gate: 'ALLOW',
  reason: 'All delegation governance gates passed.',
  evaluationMs: 1,
  allowlistedSubagents: ['TASK'],
  delegatedSubagents: ['TASK'],
  approvalRef: 'approval-1',
  approvedBy: 'human-reviewer'
};

const deniedGovernance: SubagentGovernanceDecision = {
  allowed: false,
  gate: 'ENVIRONMENT',
  reason: 'CHIRALITY_ENABLE_SUBAGENTS is not set to "true".',
  evaluationMs: 1,
  allowlistedSubagents: ['TASK'],
  delegatedSubagents: []
};

describe('agent/subagent runtime contract', () => {
  it('keeps the prerequisite posture contract-only and non-executable', () => {
    expect(AGENT_SUBAGENT_PREREQUISITE_POSTURE).toEqual({
      executableDelegation: 'blocked',
      childDefinitions: 'contract-only',
      patternCorpusRuntime: 'reference-only',
      concreteProviderRouting: 'blocked',
      childCapabilityInheritance: 'blocked'
    });
    expect(CHILD_RUN_EVENT_TYPES).toEqual([
      'subagent.started',
      'subagent.progress',
      'subagent.completed',
      'subagent.failed'
    ]);
  });

  it('creates provider-neutral child-run preflight records from governance decisions', () => {
    const record = createDelegationChildRunRecord({
      session,
      opts,
      agentName: 'TASK',
      parentTurnId: 'turn_1',
      governanceDecision: allowedGovernance,
      requestedToolNames: ['bash', 'read_file', 'bash']
    });

    expect(record).toMatchObject({
      parentSessionId: 'sess_parent',
      parentTurnId: 'turn_1',
      parentPersona: 'WORKING_ITEMS',
      agentName: 'TASK',
      status: 'queued',
      governance: {
        state: 'allowed',
        gate: 'ALLOW',
        approvalRef: 'approval-1'
      },
      capabilityPolicy: {
        inheritParentCapabilities: false,
        requestedToolNames: ['bash', 'read_file'],
        allowedToolNames: [],
        deniedCapabilities: ['read', 'write', 'shell', 'mcp', 'network', 'subagent']
      }
    });
    expect(validateChildRunRecord(record)).toEqual({ passed: true, issues: [] });
    expect(JSON.stringify(providerNeutralChildRunRecord(record))).not.toMatch(
      /sdk|claude|anthropic|pi/i
    );
  });

  it('records denied delegation without queueing execution', () => {
    const record = createDelegationChildRunRecord({
      session,
      opts,
      agentName: 'TASK',
      governanceDecision: deniedGovernance
    });

    expect(record.status).toBe('denied');
    expect(record.governance).toMatchObject({
      state: 'denied',
      gate: 'ENVIRONMENT'
    });
    expect(record.capabilityPolicy.inheritParentCapabilities).toBe(false);
    expect(validateChildRunRecord(record)).toEqual({ passed: true, issues: [] });
  });

  it('keeps adapter-specific child-run identifiers under adapter metadata', () => {
    const record = createAdapterObservedChildRunRecord({
      parentSessionId: 'sess_parent',
      parentPersona: 'WORKING_ITEMS',
      agentName: 'TASK',
      projectRoot: '/tmp/chirality-project',
      mode: 'workspaceWrite',
      status: 'running',
      adapter: {
        adapterName: 'claude-agent-sdk',
        adapterSessionId: 'sdk_1',
        adapterTaskId: 'task_1',
        adapterToolUseId: 'toolu_1'
      }
    });

    expect(validateChildRunRecord(record)).toEqual({ passed: true, issues: [] });
    expect(JSON.stringify(providerNeutralChildRunRecord(record))).not.toMatch(
      /sdk|claude|anthropic|pi/i
    );
    expect(childRunRecordToEventData(record)).toMatchObject({
      childRunId: expect.stringMatching(/^child_/),
      agentName: 'TASK',
      status: 'running',
      adapter: {
        adapterName: 'claude-agent-sdk',
        adapterSessionId: 'sdk_1',
        adapterTaskId: 'task_1',
        adapterToolUseId: 'toolu_1'
      }
    });
  });

  it('flags completed child runs that lack output artifact references', () => {
    const record = createAdapterObservedChildRunRecord({
      parentSessionId: 'sess_parent',
      parentPersona: 'WORKING_ITEMS',
      agentName: 'TASK',
      projectRoot: '/tmp/chirality-project',
      mode: 'workspaceWrite',
      status: 'completed',
      adapter: {
        adapterName: 'claude-agent-sdk'
      }
    });

    expect(validateChildRunRecord(record)).toMatchObject({
      passed: false,
      issues: [
        {
          code: 'COMPLETED_WITHOUT_OUTPUT_ARTIFACT'
        }
      ]
    });
  });
});
