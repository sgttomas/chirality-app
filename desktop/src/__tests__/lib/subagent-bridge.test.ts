import { describe, expect, it } from 'vitest';
import {
  createExecutableAgentDefinition,
  createExecutableSubagentBridge,
  evaluateSubagentPreflight,
  SUBAGENT_BRIDGE_POLICY_VERSION,
  SUBAGENT_BRIDGE_RULING_REF,
  SUBAGENT_EXECUTION_DENIED_REASON
} from '../../lib/harness/subagent-bridge';
import type { ResolvedOpts, SessionRecord } from '@chirality/runtime-contracts/types';

const session: SessionRecord = {
  sessionId: 'sess_bridge',
  projectRoot: '/tmp/project',
  persona: 'WORKING_ITEMS',
  mode: 'direct',
  createdAt: '2026-02-23T00:00:00.000Z',
  updatedAt: '2026-02-23T00:00:00.000Z'
};

const opts: ResolvedOpts = {
  model: 'claude-test',
  tools: ['read'],
  maxTurns: 3,
  persona: 'WORKING_ITEMS',
  mode: 'direct',
  delegatedSubagents: ['TASK'],
  delegatedAgentInstructions: {
    TASK: {
      path: '/instructions/agents/AGENT_TASK.md',
      content: '# TASK actual instruction',
      sha256: 'a'.repeat(64),
      agentType: 2
    }
  }
};

describe('subagent bridge', () => {
  it('creates executable SDK agent definitions without inherited tools', () => {
    const definition = createExecutableAgentDefinition('TASK');

    expect(definition).toMatchObject({
      description: expect.stringContaining('TASK'),
      tools: [],
      maxTurns: 1,
      permissionMode: 'dontAsk'
    });
    expect(definition.prompt).toContain('D-APP-10 Option C');
    expect(definition.disallowedTools).toContain('Agent');
    expect(definition.disallowedTools).toContain('Bash');
    expect(definition.disallowedTools).toContain('Write');
  });

  it('keeps the SDK agents option disabled after managed delegation acceptance', () => {
    const bridge = createExecutableSubagentBridge({ session, opts });
    expect(bridge).toBeUndefined();
    expect(
      createExecutableSubagentBridge({
        session,
        opts: { ...opts, delegatedSubagents: [] }
      })
    ).toBeUndefined();
  });

  it('denies even formerly eligible Agent requests and records retired-bridge metadata', () => {
    const decision = evaluateSubagentPreflight({
      toolInput: {
        agent: 'TASK',
        prompt: 'run this'
      },
      eligibleAgentNames: ['TASK']
    });

    expect(decision).toEqual({
      allowed: false,
      reason: SUBAGENT_EXECUTION_DENIED_REASON,
      safeMetadata: {
        policyVersion: SUBAGENT_BRIDGE_POLICY_VERSION,
        rulingRef: SUBAGENT_BRIDGE_RULING_REF,
        allowClass: undefined,
        denyClass: 'subagent-execution',
        executionPosture: 'hard-denied',
        executableBridge: false,
        requestedAgent: 'TASK',
        eligibleAgentNames: ['TASK'],
        eligibleChildDefinition: false,
        childToolNames: [],
        childCapabilityInheritance: false
      }
    });

    const denied = evaluateSubagentPreflight({
      toolInput: {
        agent: 'UNKNOWN'
      },
      eligibleAgentNames: ['TASK']
    });
    expect(denied).toMatchObject({
      allowed: false,
      reason: SUBAGENT_EXECUTION_DENIED_REASON
    });
    expect(denied.safeMetadata).toMatchObject({
      executionPosture: 'hard-denied',
      requestedAgent: 'UNKNOWN',
      eligibleChildDefinition: false
    });
  });
});
