import { mkdtemp, mkdir, rm, writeFile } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { afterEach, beforeEach, describe, expect, it } from 'vitest';
import * as agentsRoute from '../../../app/api/harness/agents/route';
import {
  installDaemonHarnessPort,
  resetDaemonHarnessPortForTests
} from '../../../lib/runtime-client/daemon-harness-port';
import { createFakeDaemonHarnessPort } from './fake-daemon-harness-port';

type RosterEntry = { name: string; type: number | undefined; class: string | undefined };

let tmpRoot = '';
let instructionRoot = '';

async function writeInstructionRootFixture(root: string): Promise<void> {
  const agentsDir = path.join(root, 'agents');
  const docsDir = path.join(root, 'docs');
  await mkdir(agentsDir, { recursive: true });
  await mkdir(docsDir, { recursive: true });

  await writeFile(path.join(root, 'AGENTS.md'), '# agents index\n', 'utf8');
  await writeFile(path.join(root, 'README.md'), '# instruction root\n', 'utf8');
  await writeFile(path.join(docsDir, 'DIRECTIVE.md'), '# directive\n', 'utf8');
  await writeFile(path.join(docsDir, 'CONTRACT.md'), '# contract\n', 'utf8');
  await writeFile(path.join(docsDir, 'SPEC.md'), '# spec\n', 'utf8');
  await writeFile(path.join(docsDir, 'TYPES.md'), '# types\n', 'utf8');
  await writeFile(path.join(docsDir, 'PLAN.md'), '# plan\n', 'utf8');

  await writeFile(
    path.join(agentsDir, 'AGENT_WORKING_ITEMS.md'),
    'AGENT_TYPE: 1\nAGENT_CLASS: PERSONA\n',
    'utf8'
  );
  await writeFile(
    path.join(agentsDir, 'AGENT_HELPS_HUMANS.md'),
    'AGENT_TYPE: 0\nAGENT_CLASS: PERSONA\n',
    'utf8'
  );
  await writeFile(
    path.join(agentsDir, 'AGENT_TASK.md'),
    'AGENT_TYPE: 2\nAGENT_CLASS: TASK\n',
    'utf8'
  );
}

beforeEach(async () => {
  tmpRoot = await mkdtemp(path.join(os.tmpdir(), 'chirality-agents-route-'));
  instructionRoot = path.join(tmpRoot, 'instruction-root');
  await writeInstructionRootFixture(instructionRoot);
  process.env.CHIRALITY_INSTRUCTION_ROOT = instructionRoot;
  installDaemonHarnessPort(createFakeDaemonHarnessPort());
});

afterEach(async () => {
  resetDaemonHarnessPortForTests();
  delete process.env.CHIRALITY_INSTRUCTION_ROOT;
  if (tmpRoot) {
    await rm(tmpRoot, { recursive: true, force: true });
  }
  tmpRoot = '';
  instructionRoot = '';
});

describe('GET /api/harness/agents', () => {
  it('returns the v3 role registry through the legacy shape', async () => {
    const response = await agentsRoute.GET(new Request('http://localhost/api/harness/agents'));
    expect(response.status).toBe(200);

    const body = (await response.json()) as { agents: RosterEntry[] };
    expect(body.agents.map((entry) => entry.name)).toEqual([
      'HELP_HUMAN',
      'HELPS_HUMANS',
      'WORKING_ITEMS',
      'TASK'
    ]);
    expect(body.agents.find((entry) => entry.name === 'TASK')).toEqual({
      name: 'TASK',
      type: 2
    });
  });

  it('restricts to Type-0/Type-1 personas with ?directChat=1 (excludes Type-2)', async () => {
    const response = await agentsRoute.GET(
      new Request('http://localhost/api/harness/agents?directChat=1')
    );
    expect(response.status).toBe(200);

    const body = (await response.json()) as { agents: RosterEntry[] };
    expect(body.agents.map((entry) => entry.name)).toEqual(['HELP_HUMAN', 'HELPS_HUMANS', 'WORKING_ITEMS']);
    expect(body.agents.some((entry) => entry.type === 2)).toBe(false);
  });
});
