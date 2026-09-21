import { mkdtemp, mkdir, readFile, readdir, rm, writeFile } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { afterEach, beforeEach, describe, expect, it } from 'vitest';
import type { SessionRecord } from '@chirality/runtime-contracts/types';
import {
  acknowledgeAgentUpdate,
  ManagedDelegationService,
  reportCoordinationNotice,
  sendAgentUpdate,
  type DelegateAgentInput
} from '../../lib/harness/managed-delegation';

let root = '';
let projectRoot = '';

async function agent(
  name: string,
  type: number,
  frontmatter = '',
  agentClass?: 'PERSONA' | 'TASK'
): Promise<void> {
  await writeFile(
    path.join(root, 'agents', `AGENT_${name}.md`),
    `---\ndescription: test\n${frontmatter}---\n# ${name}\nAGENT_TYPE: ${type}\n${agentClass ? `AGENT_CLASS: ${agentClass}\n` : ''}`,
    'utf8'
  );
}

function parent(persona: string, agentType: 0 | 1 | 2): SessionRecord {
  return {
    sessionId: `sess_${persona}`,
    projectRoot,
    persona,
    agentType,
    mode: 'workspaceWrite',
    createdAt: '2026-07-11T00:00:00.000Z',
    updatedAt: '2026-07-11T00:00:00.000Z'
  };
}

function request(overrides: Partial<DelegateAgentInput> = {}): DelegateAgentInput {
  return {
    executionRoot: 'execution',
    runId: 'RUN-1',
    planVersion: 'v1',
    selectionAuthority: 'AGENT_0',
    posture: 'MIXED',
    acceptedBasis: ['snapshot-1'],
    workGraph: {
      nodes: ['child'],
      edges: [],
      concurrencyEligibility: ['child'],
      expectedReturns: ['# Return'],
      fanInGates: ['valid return'],
      humanDecisionPoints: []
    },
    childKind: 'named',
    agentName: 'WORKING_ITEMS',
    purpose: 'manage package',
    brief: 'Manage PKG-01 and return closure evidence.',
    declaredContext: ['execution/PKG-01'],
    tools: ['read'],
    writeTargets: ['execution/PKG-01'],
    dependencies: [],
    expectedOutput: 'package return',
    acceptanceCriteria: ['valid return'],
    requiredReturnMarkers: ['# Return'],
    contextSealed: true,
    pipelineRunApproved: true,
    approvalRef: 'HUMAN-1',
    ...overrides
  };
}

beforeEach(async () => {
  const temp = await mkdtemp(path.join(os.tmpdir(), 'managed-delegation-'));
  root = path.join(temp, 'instructions');
  projectRoot = path.join(temp, 'project');
  await mkdir(path.join(root, 'agents'), { recursive: true });
  await mkdir(path.join(root, 'docs'), { recursive: true });
  await mkdir(path.join(root, 'docs/governance_harness/_DECISIONS'), { recursive: true });
  await mkdir(projectRoot, { recursive: true });
  await writeFile(path.join(root, 'README.md'), '# root\n', 'utf8');
  await writeFile(path.join(root, 'AGENTS.md'), '# agents\n', 'utf8');
  for (const name of ['DIRECTIVE', 'CONTRACT', 'SPEC', 'TYPES', 'PLAN']) {
    await writeFile(path.join(root, 'docs', `${name}.md`), `# ${name}\n`, 'utf8');
  }
  await agent('HELP_HUMAN', 0, 'subagents: WORKING_ITEMS, MISSING\n');
  await agent('WORKING_ITEMS', 1, 'subagents: TASK, WORKING_ITEMS\nallow_generalist_agent2: true\ntools: [read]\n');
  await agent('TASK', 2, 'tools: [read]\n', 'TASK');
  process.env.CHIRALITY_INSTRUCTION_ROOT = root;
  process.env.CHIRALITY_SESSION_ROOT = path.join(path.dirname(root), 'sessions');
});

afterEach(async () => {
  delete process.env.CHIRALITY_INSTRUCTION_ROOT;
  delete process.env.CHIRALITY_SESSION_ROOT;
  if (root) await rm(path.dirname(root), { recursive: true, force: true });
  root = '';
});

describe('managed delegation', () => {
  it('allows 0→named 1, persists the graph, and records instruction and brief hashes', async () => {
    const service = new ManagedDelegationService(async (launch) => ({
      sessionId: 'sess_child',
      status: 'COMPLETED',
      output: `# Return\n${launch.childPersona}`
    }));
    const result = await service.delegate(
      parent('HELP_HUMAN', 0),
      ['read'],
      request({ selectionAuthority: 'HUMAN', posture: 'TERMINAL_FAN_OUT_IN' })
    );
    expect(result).toMatchObject({ status: 'COMPLETED', sessionId: 'sess_child' });
    expect(result.instructionHash).toMatch(/^[a-f0-9]{64}$/);
    expect(result.briefHash).toMatch(/^[a-f0-9]{64}$/);
    const plan = await readFile(path.join(projectRoot, 'execution/_Coordination/AgentRuns/RUN-1/ORCHESTRATION_PLAN.md'), 'utf8');
    expect(plan).toContain('SelectionAuthority: HUMAN');
    expect(plan).toContain('Posture: TERMINAL_FAN_OUT_IN');
    expect(plan).toContain('ConcurrencyEligibility:');
    expect(plan).toContain('ExpectedReturns:');
    expect(plan).toContain('FanInGates:');
    expect(plan).toContain('HumanDecisionPoints:');
  });

  it('allows configured Agent 0→TASK and keeps unsupported Agent 0/1 routes fail-closed', async () => {
    const service = new ManagedDelegationService(async () => ({
      sessionId: 'sess_child',
      status: 'COMPLETED',
      output: '# Return\ndone'
    }));
    await expect(
      service.delegate(parent('HELP_HUMAN', 0), ['read'], request({ childKind: 'task', agentName: 'TASK' }))
    ).rejects.toThrow('not allowlisted');
    await agent('HELP_HUMAN', 0, 'subagents: WORKING_ITEMS, TASK, MISSING\n');
    const task = await service.delegate(
      parent('HELP_HUMAN', 0),
      ['read'],
      request({
        runId: 'RUN-A0-TASK',
        childKind: 'task',
        agentName: 'TASK'
      })
    );
    expect(task).toMatchObject({ status: 'COMPLETED', sessionId: 'sess_child' });
    await expect(
      service.delegate(
        parent('HELP_HUMAN', 0),
        ['read'],
        request({ runId: 'RUN-A0-NAMED-TASK', childKind: 'named', agentName: 'TASK' })
      )
    ).rejects.toThrow('named Agent 1 roles or the TASK Agent 2');
    await expect(
      service.delegate(parent('WORKING_ITEMS', 1), ['read'], request())
    ).rejects.toThrow('only to Agent 2');
    const result = await service.delegate(
      parent('WORKING_ITEMS', 1),
      ['read_file'],
      request({ runId: 'RUN-2', selectionAuthority: 'AGENT_1', childKind: 'generalist', agentName: undefined })
    );
    expect(result.status).toBe('COMPLETED');
    expect(result.instructionHash).toBeUndefined();
  });

  it('requires canonical TASK class metadata for Agent 0→TASK launches', async () => {
    const service = new ManagedDelegationService(async () => ({
      sessionId: 'sess_task',
      status: 'COMPLETED',
      output: '# Return\ndone'
    }));
    await agent('HELP_HUMAN', 0, 'subagents: WORKING_ITEMS, TASK, MISSING\n');

    await agent('TASK', 2, 'tools: [read]\n');
    await expect(
      service.delegate(
        parent('HELP_HUMAN', 0),
        ['read'],
        request({ runId: 'RUN-A0-TASK-NO-CLASS', childKind: 'task', agentName: 'TASK' })
      )
    ).rejects.toThrow('AGENT_CLASS=TASK');

    await agent('TASK', 2, 'tools: [read]\n', 'PERSONA');
    await expect(
      service.delegate(
        parent('HELP_HUMAN', 0),
        ['read'],
        request({ runId: 'RUN-A0-TASK-WRONG-CLASS', childKind: 'task', agentName: 'TASK' })
      )
    ).rejects.toThrow('AGENT_CLASS=TASK');

    await agent('TASK', 2, 'tools: [read]\n', 'TASK');
    await expect(
      service.delegate(
        parent('HELP_HUMAN', 0),
        ['read'],
        request({ runId: 'RUN-A0-TASK-CANONICAL', childKind: 'task', agentName: 'TASK' })
      )
    ).resolves.toMatchObject({ status: 'COMPLETED', sessionId: 'sess_task' });
  });

  it('allows an Agent 0 ephemeral generalist only with explicit frontmatter opt-in', async () => {
    const service = new ManagedDelegationService(async () => ({
      sessionId: 'sess_generalist',
      status: 'COMPLETED',
      output: '# Return\ndone'
    }));
    await expect(
      service.delegate(
        parent('HELP_HUMAN', 0),
        ['read'],
        request({ runId: 'RUN-A0-GENERALIST-DENIED', childKind: 'generalist', agentName: undefined })
      )
    ).rejects.toThrow('Ephemeral generalist Agent 2 is not allowed');
    await agent(
      'HELP_HUMAN',
      0,
      'subagents: WORKING_ITEMS, TASK, MISSING\nallow_generalist_agent2: true\n'
    );
    const result = await service.delegate(
      parent('HELP_HUMAN', 0),
      ['read'],
      request({ runId: 'RUN-A0-GENERALIST', childKind: 'generalist', agentName: undefined })
    );
    expect(result).toMatchObject({ status: 'COMPLETED', sessionId: 'sess_generalist' });
    expect(result.instructionHash).toBeUndefined();
  });

  it('fails closed for a dedicated Agent 2 whose qualification is not ruled', async () => {
    await agent('CANDIDATE', 2, 'dedicated_agent2_approval: D-GOV-13\ntools: [read]\n');
    await agent('HELP_HUMAN', 0, 'subagents: WORKING_ITEMS, TASK, CANDIDATE\n');
    await agent('WORKING_ITEMS', 1, 'subagents: TASK, WORKING_ITEMS, CANDIDATE\nallow_generalist_agent2: true\ntools: [read]\n');
    await writeFile(
      path.join(root, 'docs/governance_harness/_DECISIONS/D-GOV-13_candidate.md'),
      '# D-GOV-13\n\nStatus: PROPOSED\n\n| Role | Basis |\n|---|---|\n| CANDIDATE | fixture |\n',
      'utf8'
    );
    const service = new ManagedDelegationService(async () => ({
      sessionId: 'sess_candidate',
      status: 'RUNNING',
      output: 'running'
    }));
    await expect(service.delegate(
      parent('HELP_HUMAN', 0),
      ['read'],
      request({
        runId: 'RUN-A0-CANDIDATE',
        childKind: 'named',
        agentName: 'CANDIDATE'
      })
    )).rejects.toThrow('named Agent 1 roles or the TASK Agent 2');
    await expect(service.delegate(
      parent('WORKING_ITEMS', 1),
      ['read'],
      request({
        runId: 'RUN-CANDIDATE',
        selectionAuthority: 'AGENT_1',
        childKind: 'named',
        agentName: 'CANDIDATE'
      })
    )).rejects.toThrow('approval is not RULED');
    await writeFile(
      path.join(root, 'docs/governance_harness/_DECISIONS/D-GOV-13_candidate.md'),
      '# D-GOV-13\n\nStatus: RULED\n\n| Role | Basis |\n|---|---|\n| CANDIDATE | fixture |\n',
      'utf8'
    );
    const approved = await service.delegate(
      parent('WORKING_ITEMS', 1),
      ['read'],
      request({
        runId: 'RUN-CANDIDATE-RULED',
        selectionAuthority: 'AGENT_1',
        childKind: 'named',
        agentName: 'CANDIDATE'
      })
    );
    expect(approved.status).toBe('RUNNING');
  });

  it('allows Agent 1→TASK and denies every delegation attempt from Agent 2', async () => {
    const service = new ManagedDelegationService(async () => ({
      sessionId: 'sess_task',
      status: 'COMPLETED',
      output: '# Return\ntask complete'
    }));
    const task = await service.delegate(
      parent('WORKING_ITEMS', 1),
      ['read'],
      request({
        runId: 'RUN-TASK',
        selectionAuthority: 'AGENT_1',
        childKind: 'task',
        agentName: 'TASK'
      })
    );
    expect(task).toMatchObject({ status: 'COMPLETED', sessionId: 'sess_task' });
    await expect(
      service.delegate(
        parent('TASK', 2),
        ['read'],
        request({ runId: 'RUN-A2', childKind: 'task', agentName: 'TASK' })
      )
    ).rejects.toThrow('Agent 2 may not delegate');
  });

  it('authorizes and attributes only the bounded Pi/oMLX Agent 2 shape', async () => {
    let launchedSelection: DelegateAgentInput['engineSelection'];
    const service = new ManagedDelegationService(async (launch) => {
      launchedSelection = launch.engineSelection;
      return {
        sessionId: 'sess_pi_child',
        status: 'COMPLETED',
        output: '# Return\nlocal child complete'
      };
    });
    const engineSelection = {
      adapterId: 'pi',
      providerId: 'omlx',
      model: 'exact/local-model'
    };
    const result = await service.delegate(
      parent('WORKING_ITEMS', 1),
      ['read'],
      request({
        runId: 'RUN-PI',
        selectionAuthority: 'AGENT_1',
        childKind: 'task',
        agentName: 'TASK',
        engineSelection,
        tools: ['read_file'],
        writeTargets: []
      })
    );
    expect(result.status).toBe('COMPLETED');
    expect(launchedSelection).toEqual(engineSelection);
    const runRoot = path.join(projectRoot, 'execution/_Coordination/AgentRuns/RUN-PI');
    const instance = (await readdir(path.join(runRoot, 'instances')))[0];
    const status = JSON.parse(
      await readFile(path.join(runRoot, 'instances', instance, 'STATUS.json'), 'utf8')
    ) as Record<string, unknown>;
    expect(status.engineSelection).toEqual(engineSelection);
    const brief = await readFile(path.join(runRoot, 'instances', instance, 'LAUNCH_BRIEF.md'), 'utf8');
    expect(brief).toContain('EngineSelection: {"adapterId":"pi","providerId":"omlx","model":"exact/local-model"}');
  });

  it('fails closed on Pi/oMLX scope expansion or unsupported selection', async () => {
    const service = new ManagedDelegationService(async () => ({
      sessionId: 'sess_never',
      status: 'COMPLETED',
      output: '# Return\nnever'
    }));
    const base = {
      adapterId: 'pi',
      providerId: 'omlx',
      model: 'exact/local-model'
    };
    await expect(service.delegate(
      parent('HELP_HUMAN', 0),
      ['read'],
      request({ runId: 'RUN-PI-NOT-A2', engineSelection: base, writeTargets: [] })
    )).rejects.toThrow('only for a managed Agent 2 child');
    await expect(service.delegate(
      parent('WORKING_ITEMS', 1),
      ['read_file'],
      request({
        runId: 'RUN-PI-WRITE',
        selectionAuthority: 'AGENT_1',
        childKind: 'task',
        agentName: 'TASK',
        engineSelection: base,
        tools: ['read_file']
      })
    )).rejects.toThrow('may not declare write targets');
    await expect(service.delegate(
      parent('WORKING_ITEMS', 1),
      ['read_file'],
      request({
        runId: 'RUN-PI-MULTI-TOOL',
        selectionAuthority: 'AGENT_1',
        childKind: 'task',
        agentName: 'TASK',
        engineSelection: base,
        tools: ['read_file', 'read_file'],
        writeTargets: []
      })
    )).rejects.toThrow('exactly one declared read-only tool');
    await expect(service.delegate(
      parent('WORKING_ITEMS', 1),
      ['read_file'],
      request({
        runId: 'RUN-PI-REMOTE',
        selectionAuthority: 'AGENT_1',
        childKind: 'task',
        agentName: 'TASK',
        engineSelection: { ...base, providerId: 'openai' },
        tools: ['read_file'],
        writeTargets: []
      })
    )).rejects.toThrow('only adapterId pi with providerId omlx');
  });

  it('fails closed on missing governance metadata and capability inheritance', async () => {
    const service = new ManagedDelegationService(async () => ({ sessionId: 'x', status: 'COMPLETED', output: '# Return\nx' }));
    await expect(
      service.delegate(parent('HELP_HUMAN', 0), ['read'], request({ contextSealed: false }))
    ).rejects.toThrow('requires seal');
    await expect(
      service.delegate(parent('HELP_HUMAN', 0), ['read'], request({ tools: ['bash'] }))
    ).rejects.toThrow('exceed');
    await expect(
      service.delegate(parent('HELP_HUMAN', 0), ['read'], request({ runId: 'RUN-NO-BRIEF', brief: '' }))
    ).rejects.toThrow('brief must be non-empty');
    await expect(
      service.delegate(
        parent('HELP_HUMAN', 0),
        ['read'],
        request({ runId: 'RUN-NO-INSTRUCTION', agentName: 'MISSING' })
      )
    ).rejects.toThrow();
    await expect(
      service.delegate(
        parent('WORKING_ITEMS', 1),
        ['write'],
        request({
          runId: 'RUN-NO-WRITE-BOUNDARY',
          selectionAuthority: 'AGENT_1',
          childKind: 'generalist',
          agentName: undefined,
          tools: ['write'],
          writeTargets: []
        })
      )
    ).rejects.toThrow('require at least one declared write target');
  });

  it('fails closed on escaped context, escaped writes, and unbounded Bash', async () => {
    const service = new ManagedDelegationService(async () => ({
      sessionId: 'sess_child',
      status: 'COMPLETED',
      output: '# Return\ndone'
    }));
    await expect(
      service.delegate(
        parent('HELP_HUMAN', 0),
        ['read'],
        request({ runId: 'RUN-ESCAPE-READ', declaredContext: ['../outside'] })
      )
    ).rejects.toThrow('escapes the project root');
    await expect(
      service.delegate(
        parent('HELP_HUMAN', 0),
        ['read'],
        request({ runId: 'RUN-ESCAPE-WRITE', writeTargets: ['../outside'] })
      )
    ).rejects.toThrow('escapes the project root');
    await expect(
      service.delegate(
        parent('WORKING_ITEMS', 1),
        ['read', 'bash'],
        request({
          runId: 'RUN-SHELL',
          selectionAuthority: 'AGENT_1',
          childKind: 'generalist',
          agentName: undefined,
          tools: ['bash']
        })
      )
    ).rejects.toThrow('Managed Bash requires declared read and write scope');
  });

  it('rejects active exact and ancestor-overlapping sibling writes', async () => {
    const service = new ManagedDelegationService(async () => ({
      sessionId: 'sess_running',
      status: 'RUNNING',
      output: 'running'
    }));
    await service.delegate(parent('HELP_HUMAN', 0), ['read'], request({ runId: 'RUN-OVERLAP' }));
    await expect(
      service.delegate(
        parent('HELP_HUMAN', 0),
        ['read'],
        request({
          runId: 'RUN-OVERLAP',
          workGraph: undefined,
          writeTargets: ['execution/PKG-01/nested']
        })
      )
    ).rejects.toThrow('Concurrent write overlap');
  });

  it('atomically reserves concurrent sibling write targets', async () => {
    const service = new ManagedDelegationService(async () => ({
      sessionId: `sess_${Math.random()}`,
      status: 'RUNNING',
      output: 'running'
    }));
    await service.delegate(parent('HELP_HUMAN', 0), ['read'], request({ runId: 'RUN-ATOMIC' }));
    const concurrent = await Promise.allSettled([
      service.delegate(parent('HELP_HUMAN', 0), ['read'], request({
        runId: 'RUN-ATOMIC',
        workGraph: undefined,
        declaredContext: ['execution/PKG-02'],
        writeTargets: ['execution/PKG-02']
      })),
      service.delegate(parent('HELP_HUMAN', 0), ['read'], request({
        runId: 'RUN-ATOMIC',
        workGraph: undefined,
        declaredContext: ['execution/PKG-02/nested'],
        writeTargets: ['execution/PKG-02/nested']
      }))
    ]);
    expect(concurrent.filter((result) => result.status === 'fulfilled')).toHaveLength(1);
    expect(concurrent.filter((result) => result.status === 'rejected')).toHaveLength(1);
    expect(String((concurrent.find((result) => result.status === 'rejected') as PromiseRejectedResult).reason)).toContain('Concurrent write overlap');
  });

  it('lets concurrent siblings with genuinely disjoint write targets both succeed', async () => {
    const service = new ManagedDelegationService(async () => ({
      sessionId: `sess_${Math.random()}`,
      status: 'RUNNING',
      output: 'running'
    }));
    await service.delegate(parent('HELP_HUMAN', 0), ['read'], request({ runId: 'RUN-DISJOINT' }));
    const concurrent = await Promise.allSettled([
      service.delegate(parent('HELP_HUMAN', 0), ['read'], request({
        runId: 'RUN-DISJOINT',
        workGraph: undefined,
        declaredContext: ['execution/PKG-02'],
        writeTargets: ['execution/PKG-02']
      })),
      service.delegate(parent('HELP_HUMAN', 0), ['read'], request({
        runId: 'RUN-DISJOINT',
        workGraph: undefined,
        declaredContext: ['execution/PKG-03'],
        writeTargets: ['execution/PKG-03']
      }))
    ]);
    // Disjoint siblings must never be spuriously refused: both reservations succeed,
    // and no rejection may carry the fail-closed "invalid status record" message.
    const rejected = concurrent.filter((result) => result.status === 'rejected');
    expect(rejected).toHaveLength(0);
    expect(concurrent.filter((result) => result.status === 'fulfilled')).toHaveLength(2);
  });

  it('does not bind a parent run until launch validation succeeds', async () => {
    const bound: string[] = [];
    const service = new ManagedDelegationService(
      async () => ({ sessionId: 'sess_child', status: 'RUNNING', output: 'running' }),
      async (candidate) => {
        bound.push(candidate.orchestrationRunId ?? '');
        return candidate;
      }
    );
    await expect(service.delegate(
      parent('HELP_HUMAN', 0),
      ['read'],
      request({ runId: 'RUN-BAD-BIND', contextSealed: false })
    )).rejects.toThrow('requires seal');
    expect(bound).toEqual([]);
    await service.delegate(parent('HELP_HUMAN', 0), ['read'], request({ runId: 'RUN-GOOD-BIND' }));
    expect(bound).toEqual(['RUN-GOOD-BIND']);
  });

  it('keeps disjoint siblings active and reconstructs an existing run with a new service instance', async () => {
    const runningLauncher = async () => ({
      sessionId: 'sess_running',
      status: 'RUNNING' as const,
      output: 'running'
    });
    const firstService = new ManagedDelegationService(runningLauncher);
    await firstService.delegate(parent('HELP_HUMAN', 0), ['read'], request({ runId: 'RUN-RESTART' }));
    await firstService.delegate(
      parent('HELP_HUMAN', 0),
      ['read'],
      request({
        runId: 'RUN-RESTART',
        workGraph: undefined,
        declaredContext: ['execution/PKG-02'],
        writeTargets: ['execution/PKG-02']
      })
    );
    const restartedService = new ManagedDelegationService(runningLauncher);
    const third = await restartedService.delegate(
      parent('HELP_HUMAN', 0),
      ['read'],
      request({
        runId: 'RUN-RESTART',
        workGraph: undefined,
        declaredContext: ['execution/PKG-03'],
        writeTargets: ['execution/PKG-03']
      })
    );
    expect(third.status).toBe('RUNNING');
    const handoff = await readFile(
      path.join(projectRoot, 'execution/_Coordination/AgentRuns/RUN-RESTART/HANDOFF_STATE.md'),
      'utf8'
    );
    expect(handoff.match(/\| RUNNING \|/g)).toHaveLength(3);
  });

  it('isolates a failed node so independent work can continue', async () => {
    const failing = new ManagedDelegationService(async () => {
      throw new Error('child crashed');
    });
    await expect(
      failing.delegate(parent('HELP_HUMAN', 0), ['read'], request({ runId: 'RUN-FAILURE' }))
    ).rejects.toThrow('child crashed');
    const succeeding = new ManagedDelegationService(async () => ({
      sessionId: 'sess_independent',
      status: 'COMPLETED',
      output: '# Return\nindependent complete'
    }));
    const independent = await succeeding.delegate(
      parent('HELP_HUMAN', 0),
      ['read'],
      request({
        runId: 'RUN-FAILURE',
        workGraph: undefined,
        declaredContext: ['execution/PKG-02'],
        writeTargets: ['execution/PKG-02']
      })
    );
    expect(independent.status).toBe('COMPLETED');
  });

  it('rejects schema-invalid terminal returns and records the failed fan-in', async () => {
    const service = new ManagedDelegationService(async () => ({
      sessionId: 'sess_invalid',
      status: 'COMPLETED',
      output: 'missing required structure'
    }));
    await expect(
      service.delegate(parent('HELP_HUMAN', 0), ['read'], request({ runId: 'RUN-INVALID' }))
    ).rejects.toThrow('schema-invalid');
    const handoff = await readFile(
      path.join(projectRoot, 'execution/_Coordination/AgentRuns/RUN-INVALID/HANDOFF_STATE.md'),
      'utf8'
    );
    expect(handoff).toContain('FAILED');
  });

  it('persists child→parent notices and parent→child updates with acknowledgments', async () => {
    const service = new ManagedDelegationService(async () => ({ sessionId: 'sess_child', status: 'RUNNING', output: 'running' }));
    const parentRecord = { ...parent('HELP_HUMAN', 0), orchestrationRunId: 'RUN-3', executionRoot: 'execution', planVersion: 'v1' };
    const delegated = await service.delegate(parentRecord, ['read'], request({ runId: 'RUN-3' }));
    const child: SessionRecord = {
      ...parent('WORKING_ITEMS', 1),
      sessionId: 'sess_child',
      orchestrationRunId: 'RUN-3',
      executionRoot: 'execution',
      agentInstanceId: delegated.instanceId,
      parentSessionId: parentRecord.sessionId
    };
    const notice = await reportCoordinationNotice(child, {
      noticeType: 'DEPENDENCY',
      claimStatus: 'PROVISIONAL',
      summary: 'Sibling may depend on changed contract.',
      evidenceRefs: ['src/a.ts:10'],
      affectedScopes: ['PKG-02'],
      requestedAction: 'relay',
      blocking: false,
      humanDecisionRequired: false,
      acceptedBasisRef: 'snapshot-1'
    });
    await expect(
      reportCoordinationNotice(
        { ...child, sessionId: 'sess_forged_sibling' },
        {
          noticeType: 'DEPENDENCY',
          claimStatus: 'PROVISIONAL',
          summary: 'Attempt to bypass the direct-parent channel.',
          evidenceRefs: [],
          affectedScopes: [],
          requestedAction: 'relay',
          blocking: false,
          humanDecisionRequired: false,
          acceptedBasisRef: 'snapshot-1'
        }
      )
    ).rejects.toThrow('not the recorded direct child');
    await expect(
      sendAgentUpdate(
        { ...parentRecord, sessionId: 'sess_sibling' },
        {
          childInstanceId: delegated.instanceId,
          disposition: 'RELAY',
          summary: 'Attempt direct sibling update.',
          claimStatus: 'PROVISIONAL',
          evidenceRefs: [],
          consequential: false
        }
      )
    ).rejects.toThrow('only to a direct child');
    await expect(
      sendAgentUpdate(parentRecord, {
        childInstanceId: delegated.instanceId,
        disposition: 'RELAY',
        summary: 'Unsourced relay.',
        claimStatus: 'PROVISIONAL',
        evidenceRefs: [],
        consequential: false
      })
    ).rejects.toThrow('RELAY requires noticeId');
    await expect(
      sendAgentUpdate(parentRecord, {
        childInstanceId: delegated.instanceId,
        disposition: 'RECORD',
        summary: 'Unsupported acceptance.',
        claimStatus: 'ACCEPTED',
        evidenceRefs: [],
        consequential: false
      })
    ).rejects.toThrow('requires humanAcceptanceRef');
    await expect(
      sendAgentUpdate(parentRecord, {
        childInstanceId: delegated.instanceId,
        noticeId: notice.noticeId,
        disposition: 'RELAY',
        summary: 'Illegally promote the claim.',
        claimStatus: 'ACCEPTED',
        humanAcceptanceRef: 'HUMAN-ACCEPT-1',
        evidenceRefs: ['src/a.ts:10'],
        consequential: false
      })
    ).rejects.toThrow('must preserve');
    await expect(
      sendAgentUpdate(parentRecord, {
        childInstanceId: delegated.instanceId,
        disposition: 'AMEND',
        summary: 'Consequential change.',
        claimStatus: 'VALIDATED',
        evidenceRefs: [],
        consequential: true,
        amendmentCategories: ['SCOPE'],
        amendmentVersion: 'brief-v2',
        amendment: 'Change the objective.'
      })
    ).rejects.toThrow('requires humanRulingRef');
    const update = await sendAgentUpdate(parentRecord, {
      childInstanceId: delegated.instanceId,
      noticeId: notice.noticeId,
      disposition: 'RELAY',
      summary: 'Preserve provisional status.',
      claimStatus: 'PROVISIONAL',
      evidenceRefs: ['src/a.ts:10'],
      consequential: false
    });
    const acknowledgment = await acknowledgeAgentUpdate(child, {
      updateId: update.updateId,
      acknowledgment: 'INCORPORATED'
    });
    expect(acknowledgment.acknowledgment).toBe('INCORPORATED');
    expect(await readFile(path.join(projectRoot, `execution/_Coordination/AgentRuns/RUN-3/notices/${notice.noticeId}.json`), 'utf8')).toContain('PROVISIONAL');

    await sendAgentUpdate(parentRecord, {
      childInstanceId: delegated.instanceId,
      disposition: 'AMEND',
      summary: 'Add bounded context.',
      claimStatus: 'PROVISIONAL',
      evidenceRefs: ['src/a.ts:10'],
      consequential: false,
      amendmentCategories: ['CONTEXT'],
      amendmentVersion: 'brief-v2',
      amendment: 'Add src/b.ts to the declared read context.'
    });
    expect(await readFile(
      path.join(projectRoot, `execution/_Coordination/AgentRuns/RUN-3/amendments/${delegated.instanceId}/brief-v2.md`),
      'utf8'
    )).toContain('src/b.ts');

    await sendAgentUpdate(parentRecord, {
      childInstanceId: delegated.instanceId,
      disposition: 'REPLAN',
      summary: 'Add a dependency-valid second stage.',
      claimStatus: 'VALIDATED',
      validationRef: 'validation/report-1',
      evidenceRefs: ['src/a.ts:10'],
      consequential: false,
      amendmentCategories: ['SEQUENCING'],
      amendment: 'Use plan v2 for downstream dispatch.',
      planVersion: 'v2',
      selectionAuthority: 'AGENT_0',
      posture: 'MIXED',
      acceptedBasis: ['snapshot-1'],
      workGraph: {
        nodes: ['child', 'downstream'],
        edges: [['child', 'downstream']],
        concurrencyEligibility: ['child'],
        expectedReturns: ['# Return'],
        fanInGates: ['valid return'],
        humanDecisionPoints: []
      }
    });
    const versioned = await readFile(
      path.join(projectRoot, 'execution/_Coordination/AgentRuns/RUN-3/plans/v2/WORK_GRAPH.json'),
      'utf8'
    );
    expect(versioned).toContain('downstream');
  });

  it('releases dependent work only from a valid return explicitly accepted by the manager', async () => {
    const service = new ManagedDelegationService(async () => ({ sessionId: 'sess_child', status: 'COMPLETED', output: '# Return\nvalid return' }));
    const first = await service.delegate(parent('HELP_HUMAN', 0), ['read'], request({ runId: 'RUN-4' }));
    await expect(service.delegate(
      parent('HELP_HUMAN', 0),
      ['read'],
      request({ runId: 'RUN-4', workGraph: undefined, dependencies: [first.instanceId] })
    )).rejects.toThrow('no manager acceptance');
    const second = await service.delegate(
      parent('HELP_HUMAN', 0),
      ['read'],
      request({ runId: 'RUN-4', workGraph: undefined, dependencies: [first.instanceId], acceptedPredecessors: [first.instanceId] })
    );
    expect(second.status).toBe('COMPLETED');
  });
});
