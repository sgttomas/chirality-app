import { execFile, spawn, type ChildProcess } from 'node:child_process';
import { mkdir, mkdtemp, readFile, realpath, rm, writeFile } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import readline from 'node:readline';
import { promisify } from 'node:util';
import { afterEach, describe, expect, it } from 'vitest';
import { RuntimeClient } from '@chirality/runtime-client';
import type { UIEvent } from '@chirality/runtime-contracts';
import {
  CONTROLLED_CI_APPROVED_BY,
  CONTROLLED_CI_PURPOSE,
  parseControlledCiReadyLine
} from '../../../scripts/controlled-ci-runtime';

const execFileAsync = promisify(execFile);
const roots: string[] = [];
const stops: Array<() => Promise<void>> = [];

async function stopChild(child: ChildProcess): Promise<void> {
  if (child.exitCode !== null) return;
  child.kill('SIGTERM');
  await new Promise<void>((resolve) => child.once('exit', () => resolve()));
}

async function readReadyLine(child: ChildProcess): Promise<string> {
  const stderr: string[] = [];
  child.stderr?.on('data', (chunk: Buffer) => stderr.push(chunk.toString('utf8')));
  return new Promise<string>((resolve, reject) => {
    const lines = readline.createInterface({ input: child.stdout! });
    lines.once('line', (line) => resolve(line));
    child.once('exit', (code) => reject(new Error(`controlled runtime exited with ${code} before its ready line: ${stderr.join('')}`)));
  });
}

afterEach(async () => {
  await Promise.all(stops.splice(0).map((stop) => stop().catch(() => undefined)));
  await Promise.all(roots.splice(0).map((root) => rm(root, { recursive: true, force: true })));
});

async function drain(source: Awaited<ReturnType<RuntimeClient['turnSession']>>): Promise<UIEvent[]> {
  const events: UIEvent[] = [];
  for await (const event of source) events.push(event);
  return events;
}

describe('controlled CI runtime', () => {
  it('builds an isolated graph, registers the manifest itself and serves project turns over the real daemon socket', async () => {
    const frontendRoot = path.resolve(process.cwd());
    const repositoryRoot = path.resolve(frontendRoot, '..', '..', '..');
    await execFileAsync(process.execPath, [path.join(frontendRoot, 'scripts', 'build-controlled-ci-runtime.mjs')], {
      cwd: frontendRoot
    });

    const metadata = JSON.parse(await readFile(path.join(frontendRoot, 'out', 'controlled-ci', 'controlled-runtime.meta.json'), 'utf8')) as {
      inputs: Record<string, unknown>;
    };
    const sources = Object.keys(metadata.inputs).join('\n');
    expect(sources).toContain('scripts/controlled-ci-runtime.ts');
    expect(sources).toContain('packages/daemon/src/runtime-daemon.ts');
    expect(sources).toContain('packages/core/src/project-registry.ts');
    expect(sources).not.toMatch(/electron\/main\.ts|runtime-service-host|engine-pi-omlx|engine-claude|app-owned-composition|hosted-private-|native-admission|codex-|packages\/cli\//u);

    const pkg = JSON.parse(await readFile(path.join(frontendRoot, 'package.json'), 'utf8')) as {
      build: { files: string[]; extraResources: Array<{ from: string }> };
    };
    expect(pkg.build.files.some((item) => !item.startsWith('!') && (item === '**/*' || item.startsWith('out/')))).toBe(false);
    expect(pkg.build.extraResources.some((item) => item.from.includes('out/controlled-ci'))).toBe(false);

    const root = await mkdtemp(path.join(os.tmpdir(), 'chirality-controlled-ci-'));
    roots.push(root);
    const runtimeDirectory = path.join(root, 'runtime');
    const socketPath = path.join(runtimeDirectory, 'control.sock');
    const projectRoot = path.join(root, 'project');
    await mkdir(projectRoot, { recursive: true });
    await writeFile(path.join(projectRoot, 'AGENTS.md'), '# Controlled CI fixture\n');
    const projectId = 'controlled-ci-fixture';
    const manifestPath = path.join(projectRoot, 'chirality.project.json');
    await writeFile(manifestPath, `${JSON.stringify({
      schemaVersion: 'chirality.project/v2',
      projectId,
      displayName: 'Controlled CI fixture',
      workingRoot: '.',
      instructionRoot: { mode: 'runtime' },
      defaultExecutionRoot: '.',
      profiles: { domain: [], capability: [], dataBoundary: [] },
      enabledAdapterIds: ['stub'],
      embeddedUi: { declared: false }
    })}\n`);

    const controlledEntry = path.join(frontendRoot, 'out', 'controlled-ci', 'controlled-runtime.mjs');
    const environment = {
      ...process.env,
      CHIRALITY_RUNTIME_DIRECTORY: runtimeDirectory,
      CHIRALITY_RUNTIME_SOCKET_PATH: socketPath,
      CHIRALITY_INSTRUCTION_ROOT: repositoryRoot,
      CHIRALITY_STUB_CHUNK_DELAY_MS: '0'
    };
    const rejected = await execFileAsync(process.execPath, [controlledEntry, '--manifest', manifestPath], {
      cwd: frontendRoot,
      env: { ...environment, CHIRALITY_CONTROLLED_CI_RUNTIME: 'ordinary-runtime' }
    }).then(() => undefined, (error: unknown) => error);
    expect(String(rejected)).toContain(`CHIRALITY_CONTROLLED_CI_RUNTIME must equal ${CONTROLLED_CI_PURPOSE}`);
    const noManifest = await execFileAsync(process.execPath, [controlledEntry], {
      cwd: frontendRoot,
      env: { ...environment, CHIRALITY_CONTROLLED_CI_RUNTIME: CONTROLLED_CI_PURPOSE }
    }).then(() => undefined, (error: unknown) => error);
    expect(String(noManifest)).toContain('--manifest <absolute path to chirality.project.json>');

    const child = spawn(process.execPath, [controlledEntry, '--manifest', manifestPath], {
      cwd: frontendRoot,
      env: { ...environment, CHIRALITY_CONTROLLED_CI_RUNTIME: CONTROLLED_CI_PURPOSE },
      stdio: ['ignore', 'pipe', 'pipe']
    });
    stops.push(() => stopChild(child));
    const ready = parseControlledCiReadyLine(await readReadyLine(child));
    expect(ready).toMatchObject({ status: 'ready', purpose: CONTROLLED_CI_PURPOSE, socketPath, projectId });
    expect(path.basename(ready.tokenFile)).toMatch(/^project-[A-Za-z0-9_-]+\.token$/u);
    expect(path.dirname(ready.tokenFile)).toBe(path.join(runtimeDirectory, 'auth', 'tokens'));
    expect(ready.projectRoot).toBe(await realpath(projectRoot));

    const registry = JSON.parse(await readFile(path.join(runtimeDirectory, 'projects', 'registry.json'), 'utf8')) as {
      projects: Array<{ projectId: string; approval: { approvedBy: string; approvalReference: string } }>;
    };
    expect(registry.projects.find((item) => item.projectId === projectId)).toMatchObject({
      projectId,
      approval: { approvedBy: CONTROLLED_CI_APPROVED_BY }
    });

    const project = new RuntimeClient({ socketPath, tokenFile: ready.tokenFile });
    expect((await project.listProjects()).map((item) => item.project.projectId)).toContain(projectId);
    const session = await project.createSession(projectId, { projectId });
    const events = await drain(await project.turnSession(projectId, session.sessionId, {
      message: 'CONTROLLED_CI_SOCKET_TURN'
    }));
    expect(events).toContainEqual(expect.objectContaining({
      type: 'session:init',
      data: expect.objectContaining({ adapterId: 'stub', providerId: 'stub', model: 'controlled-ci' })
    }));
    // Frames carry the turn registry's `seq` (SPIKE_DESIGN section 5) next to
    // the UIEvent fields; the fixture asserts the event content only.
    expect(events).toContainEqual(expect.objectContaining({ type: 'chat:complete', data: { text: 'CONTROLLED_CI_SOCKET_TURN' } }));
    expect(events.at(-1)).toEqual(expect.objectContaining({ type: 'process:exit', data: { exitCode: 0 } }));
    expect(events.map((event) => (event as { seq?: number }).seq)).toEqual(events.map((_event, index) => index + 1));
  }, 30_000);
});
