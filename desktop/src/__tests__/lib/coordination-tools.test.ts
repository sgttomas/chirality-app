import { mkdir, mkdtemp, readFile, rm, writeFile } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import type { SessionRecord, UIEvent } from '@chirality/runtime-contracts/types';
import { launchManagedChild } from '../../lib/harness/mcp/coordination-tools';

const runtimeHolder = vi.hoisted(() => ({ current: undefined as any }));

vi.mock('../../lib/harness/runtime', () => ({
  getHarnessRuntime: () => runtimeHolder.current
}));

let temp = '';
let projectRoot = '';
let instructionRoot = '';

beforeEach(async () => {
  temp = await mkdtemp(path.join(os.tmpdir(), 'coordination-tools-'));
  projectRoot = path.join(temp, 'project');
  instructionRoot = path.join(temp, 'instructions');
  await mkdir(path.join(instructionRoot, 'agents'), { recursive: true });
  await mkdir(path.join(instructionRoot, 'docs'), { recursive: true });
  await mkdir(projectRoot, { recursive: true });
  await writeFile(path.join(instructionRoot, 'README.md'), '# root\n', 'utf8');
  await writeFile(path.join(instructionRoot, 'AGENTS.md'), '# agents\n', 'utf8');
  for (const name of ['DIRECTIVE', 'CONTRACT', 'SPEC', 'TYPES', 'PLAN']) {
    await writeFile(path.join(instructionRoot, 'docs', `${name}.md`), `# ${name}\n`, 'utf8');
  }
  await writeFile(
    path.join(instructionRoot, 'agents/AGENT_HELP_HUMAN.md'),
    '---\ndescription: test\n---\n# HELP_HUMAN\nAGENT_TYPE: 0\n',
    'utf8'
  );
  process.env.CHIRALITY_INSTRUCTION_ROOT = instructionRoot;
});

afterEach(async () => {
  delete process.env.CHIRALITY_INSTRUCTION_ROOT;
  runtimeHolder.current = undefined;
  if (temp) await rm(temp, { recursive: true, force: true });
});

describe('managed child coordination delivery', () => {
  it('injects a live parent update at the next safe turn boundary and requires acknowledgment', async () => {
    const runRoot = path.join(projectRoot, 'execution/_Coordination/AgentRuns/RUN-SAFE');
    const instanceRoot = path.join(runRoot, 'instances/inst_child');
    await mkdir(instanceRoot, { recursive: true });
    await writeFile(path.join(instanceRoot, 'STATUS.json'), '{"status":"RUNNING"}\n', 'utf8');

    const parent: SessionRecord = {
      sessionId: 'sess_parent',
      projectRoot,
      persona: 'HELP_HUMAN',
      mode: 'workspaceWrite',
      executionRoot: 'execution',
      orchestrationRunId: 'RUN-SAFE',
      planVersion: 'v1',
      createdAt: '2026-07-11T00:00:00.000Z',
      updatedAt: '2026-07-11T00:00:00.000Z'
    };
    let child: SessionRecord = {
      sessionId: 'sess_child',
      projectRoot,
      persona: 'WORKING_ITEMS',
      mode: 'workspaceWrite',
      createdAt: '2026-07-11T00:00:00.000Z',
      updatedAt: '2026-07-11T00:00:00.000Z'
    };
    const messages: string[] = [];
    let turnNumber = 0;

    runtimeHolder.current = {
      sessionManager: {
        create: vi.fn(async () => child),
        save: vi.fn(async (_sessionId: string, updates: Partial<SessionRecord>) => {
          child = { ...child, ...updates };
          return child;
        })
      },
      turnEngine: {
        runTurn: vi.fn(async (request: { message: string }) => {
          const activeStatus = JSON.parse(
            await readFile(path.join(instanceRoot, 'STATUS.json'), 'utf8')
          ) as Record<string, unknown>;
          expect(activeStatus.childSessionId).toBe('sess_child');
          messages.push(request.message);
          turnNumber += 1;
          const currentTurn = turnNumber;
          async function* events(): AsyncGenerator<UIEvent> {
            if (currentTurn === 1) {
              await mkdir(path.join(runRoot, 'updates'), { recursive: true });
              await writeFile(
                path.join(runRoot, 'updates/update_1.json'),
                `${JSON.stringify({
                  updateId: 'update_1',
                  childInstanceId: 'inst_child',
                  claimStatus: 'PROVISIONAL',
                  summary: 'Use the revised dependency observation.'
                })}\n`,
                'utf8'
              );
            } else {
              await mkdir(path.join(runRoot, 'acknowledgments'), { recursive: true });
              await writeFile(
                path.join(runRoot, 'acknowledgments/update_1.json'),
                '{"updateId":"update_1","acknowledgment":"INCORPORATED"}\n',
                'utf8'
              );
            }
            yield {
              type: 'chat:complete',
              data: { text: currentTurn === 1 ? '# Return\ninitial' : '# Return\nupdated' }
            };
            yield { type: 'process:exit', data: { exitCode: 0 } };
          }
          return { sessionId: 'sess_child', events: events(), cancel: vi.fn() };
        })
      }
    };

    const result = await launchManagedChild({
      parent,
      childPersona: 'WORKING_ITEMS',
      childKind: 'named',
      childAgentType: 1,
      childInstanceId: 'inst_child',
      runId: 'RUN-SAFE',
      brief: 'Perform the initial package work.',
      declaredContext: [path.join(projectRoot, 'PKG-01')],
      tools: ['read', 'ack_agent_update'],
      writeTargets: [path.join(projectRoot, 'PKG-01')],
      briefHash: 'brief-hash',
      requiredReturnMarkers: ['# Return'],
      approvalRef: 'HUMAN-1',
      executionMode: 'WAIT'
    });

    expect(result.status).toBe('COMPLETED');
    expect(messages).toHaveLength(2);
    expect(messages[1]).toContain('UpdateID update_1');
    expect(messages[1]).toContain('PROVISIONAL');
  });

  it('blocks terminal fan-in when a delivered parent update is not acknowledged', async () => {
    const runRoot = path.join(projectRoot, 'execution/_Coordination/AgentRuns/RUN-BLOCK');
    const instanceRoot = path.join(runRoot, 'instances/inst_blocked');
    await mkdir(instanceRoot, { recursive: true });
    await writeFile(path.join(instanceRoot, 'STATUS.json'), '{"status":"RUNNING"}\n', 'utf8');
    const parent: SessionRecord = {
      sessionId: 'sess_parent',
      projectRoot,
      persona: 'HELP_HUMAN',
      mode: 'workspaceWrite',
      executionRoot: 'execution',
      orchestrationRunId: 'RUN-BLOCK',
      planVersion: 'v1',
      createdAt: '2026-07-11T00:00:00.000Z',
      updatedAt: '2026-07-11T00:00:00.000Z'
    };
    let child: SessionRecord = {
      sessionId: 'sess_blocked',
      projectRoot,
      persona: 'WORKING_ITEMS',
      mode: 'workspaceWrite',
      createdAt: '2026-07-11T00:00:00.000Z',
      updatedAt: '2026-07-11T00:00:00.000Z'
    };
    let turnNumber = 0;
    runtimeHolder.current = {
      sessionManager: {
        create: vi.fn(async () => child),
        save: vi.fn(async (_sessionId: string, updates: Partial<SessionRecord>) => {
          child = { ...child, ...updates };
          return child;
        })
      },
      turnEngine: {
        runTurn: vi.fn(async () => {
          turnNumber += 1;
          const currentTurn = turnNumber;
          async function* events(): AsyncGenerator<UIEvent> {
            if (currentTurn === 1) {
              await mkdir(path.join(runRoot, 'updates'), { recursive: true });
              await writeFile(
                path.join(runRoot, 'updates/update_unacked.json'),
                `${JSON.stringify({
                  updateId: 'update_unacked',
                  childInstanceId: 'inst_blocked',
                  claimStatus: 'VALIDATED',
                  summary: 'Acknowledge this update.'
                })}\n`,
                'utf8'
              );
            }
            yield { type: 'chat:complete', data: { text: '# Return\nresponse' } };
            yield { type: 'process:exit', data: { exitCode: 0 } };
          }
          return { sessionId: 'sess_blocked', events: events(), cancel: vi.fn() };
        })
      }
    };

    const result = await launchManagedChild({
      parent,
      childPersona: 'WORKING_ITEMS',
      childKind: 'named',
      childAgentType: 1,
      childInstanceId: 'inst_blocked',
      runId: 'RUN-BLOCK',
      brief: 'Perform package work.',
      declaredContext: [path.join(projectRoot, 'PKG-01')],
      tools: ['read', 'ack_agent_update'],
      writeTargets: [path.join(projectRoot, 'PKG-01')],
      briefHash: 'brief-hash',
      requiredReturnMarkers: ['# Return'],
      approvalRef: 'HUMAN-1',
      executionMode: 'WAIT'
    });

    expect(result.status).toBe('BLOCKED');
    expect(result.output).toContain('was not acknowledged');
  });
});
