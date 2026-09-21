import { access, mkdir, mkdtemp, readFile, realpath, rm, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { afterEach, describe, expect, it } from 'vitest';
import type { HarnessEvent, OmlxControlPort } from '@chirality/runtime-contracts';
import {
  AuthRegistry,
  EngineRegistry,
  ProjectRegistry,
  ResidencyCoordinator,
  RuntimeService,
  SessionStore,
  TurnCoordinator
} from '@chirality/runtime-core';
import { RuntimeClient } from '@chirality/runtime-client';
import {
  runCli,
  type CliDependencies,
  type CliIo
} from '@chirality/runtime-cli';
import { RuntimeDaemon } from '@chirality/runtime-daemon';
import { RuntimeDaemonHarnessPort } from '../../lib/runtime-client/runtime-daemon-harness-port';
import { buildRecordedAgentHierarchy } from '../../lib/woven-dialogue/recorded-agent-hierarchy';

const activeDaemons: RuntimeDaemon[] = [];
const tempRoots: string[] = [];

afterEach(async () => {
  await Promise.all(
    activeDaemons.splice(0).map(async (daemon) => daemon.stop().catch(() => undefined))
  );
  await Promise.all(
    tempRoots.splice(0).map(async (root) => rm(root, { recursive: true, force: true }))
  );
});

async function createProjectFixture(root: string): Promise<string> {
  await mkdir(join(root, 'agents'), { recursive: true });
  await mkdir(join(root, 'execution'), { recursive: true });
  await mkdir(join(root, 'legacy-sessions'), { recursive: true });
  await writeFile(
    join(root, 'agents', 'AGENT_WORKING_ITEMS.md'),
    '[[DOC:AGENT_INSTRUCTIONS]]\n# WORKING_ITEMS\nAGENT_TYPE: 1\nAGENT_CLASS: WORKING\n',
    'utf8'
  );
  const manifestPath = join(root, 'chirality.project.json');
  await writeFile(
    manifestPath,
    `${JSON.stringify(
      {
        schemaVersion: 'chirality.project/v1',
        projectId: 'chirality-app-dev',
        displayName: 'Chirality App Dev Replay Fixture',
        workingRoot: '.',
        instructionRoot: '.',
        agentsOverlay: 'agents/AGENT_WORKING_ITEMS.md',
        defaultExecutionRoot: 'execution',
        profiles: { domain: [], capability: [], dataBoundary: [] },
        enabledAdapterIds: ['pi'],
        embeddedUi: { declared: false },
        legacySessionRoots: ['legacy-sessions']
      },
      null,
      2
    )}\n`,
    'utf8'
  );
  return manifestPath;
}

function createRuntime(root: string) {
  const runtimeDirectory = join(root, 'runtime');
  const projects = new ProjectRegistry(runtimeDirectory);
  const sessions = new SessionStore(runtimeDirectory, projects);
  const engines = new EngineRegistry();
  const control: OmlxControlPort = {
    async listStatus() {
      return [];
    },
    async load() {},
    async unload() {}
  };
  const residency = new ResidencyCoordinator(control, runtimeDirectory);
  const auth = new AuthRegistry(runtimeDirectory);
  const credentials = {
    async get() {
      return undefined;
    },
    async status() {
      return { configured: false };
    },
    async set() {},
    async remove() {}
  };
  const turns = new TurnCoordinator(projects, sessions, engines, residency);
  const service = new RuntimeService(
    projects,
    sessions,
    engines,
    residency,
    turns,
    auth,
    credentials,
    undefined,
    undefined,
    undefined,
    {
      async resolve() {
        return {
          role: 'agent1' as const,
          engineSelection: { adapterId: 'pi', providerId: 'omlx', model: 'fixture-model' }
        };
      }
    }
  );
  return { runtimeDirectory, service };
}

function event(
  sessionId: string,
  eventId: string,
  timestamp: string,
  type: HarnessEvent['type'],
  data: Record<string, unknown>
): HarnessEvent {
  return {
    schemaVersion: 1,
    eventId,
    sessionId,
    turnId: `${sessionId}-turn`,
    timestamp,
    type,
    data
  };
}

async function replayThroughCli(
  client: RuntimeClient,
  projectId: string,
  sessionId: string,
  root: string
): Promise<Awaited<ReturnType<RuntimeClient['replaySession']>>> {
  const stdout: string[] = [];
  const stderr: string[] = [];
  const io: CliIo = {
    stdout(text) {
      stdout.push(text);
    },
    stderr(text) {
      stderr.push(text);
    },
    async readStdin() {
      return '';
    }
  };
  // The CLI is a client of the App-owned Runtime service (D-GOV-43, A2): no
  // LaunchAgent verbs, no daemon install paths, no conformance measurement.
  const dependencies: CliDependencies = {
    client,
    paths: {
      userData: root,
      runtimeDirectory: join(root, 'runtime'),
      socketPath: join(root, 'runtime', 'control.sock'),
      tokenFile: join(root, 'runtime', 'operator.token')
    },
    readTextFile: (path) => readFile(path, 'utf8')
  };

  const exitCode = await runCli(
    ['session', 'replay', '--project', projectId, '--session', sessionId, '--json'],
    io,
    dependencies
  );

  expect(exitCode).toBe(0);
  expect(stderr).toEqual([]);
  expect(stdout).toHaveLength(1);
  return JSON.parse(stdout[0] ?? '') as Awaited<ReturnType<RuntimeClient['replaySession']>>;
}

async function seedLegacySession(
  projectRoot: string,
  record: Record<string, unknown>,
  events: readonly HarnessEvent[]
): Promise<{ sessionPath: string; eventsPath: string }> {
  const sessionId = String(record.sessionId);
  const directory = join(projectRoot, 'legacy-sessions', sessionId);
  await mkdir(directory, { recursive: true });
  const sessionPath = join(directory, 'session.json');
  const eventsPath = join(directory, 'events.jsonl');
  await writeFile(sessionPath, `${JSON.stringify(record, null, 2)}\n`, 'utf8');
  await writeFile(
    eventsPath,
    `${events.map((candidate) => JSON.stringify(candidate)).join('\n')}\n`,
    'utf8'
  );
  return { sessionPath, eventsPath };
}

describe('canonical replay across Desktop, CLI, and daemon restart', () => {
  it('lazily preserves legacy manager/child records and replays one canonical hierarchy', async () => {
    const root = await mkdtemp(join(tmpdir(), 'chirality-canonical-replay-'));
    tempRoots.push(root);
    const projectRoot = join(root, 'chirality-app-dev');
    const manifestPath = await createProjectFixture(projectRoot);
    const canonicalProjectRoot = await realpath(projectRoot);
    const managerSessionId = 'legacy-manager-session';
    const childSessionId = 'legacy-child-session';
    const engineSelection = {
      adapterId: 'pi',
      providerId: 'omlx',
      model: 'recorded-model'
    };
    const managerSource = await seedLegacySession(
      canonicalProjectRoot,
      {
        sessionId: managerSessionId,
        projectRoot: canonicalProjectRoot,
        persona: 'WORKING_ITEMS',
        mode: 'governed',
        role: 'agent1',
        agentType: 1,
        engineSelection,
        status: 'completed',
        createdAt: '2026-08-16T10:00:00.000Z',
        updatedAt: '2026-08-16T10:02:00.000Z',
        agentInstanceId: 'WI-PKG05-CANONICAL-REPLAY',
        outputArtifact: 'runs/manager/RETURN.md'
      },
      [
        event(
          managerSessionId,
          'manager-event-1',
          '2026-08-16T10:00:01.000Z',
          'turn.accepted',
          { message: 'Coordinate the canonical replay proof.' }
        ),
        event(
          managerSessionId,
          'manager-event-2',
          '2026-08-16T10:02:00.000Z',
          'turn.completed',
          { summary: 'Manager work completed.' }
        )
      ]
    );
    const childSource = await seedLegacySession(
      canonicalProjectRoot,
      {
        sessionId: childSessionId,
        projectRoot: canonicalProjectRoot,
        persona: 'TASK',
        mode: 'readOnly',
        role: 'agent2',
        agentType: 2,
        parentSessionId: managerSessionId,
        parentInstanceId: 'WI-PKG05-CANONICAL-REPLAY',
        engineSelection,
        status: 'completed',
        createdAt: '2026-08-16T10:00:30.000Z',
        updatedAt: '2026-08-16T10:01:30.000Z',
        agentInstanceId: 'A2-PKG05-CANONICAL-REPLAY-IMPLEMENT-01',
        outputArtifact: 'runs/child/RETURN.md'
      },
      [
        event(
          childSessionId,
          'child-event-1',
          '2026-08-16T10:00:31.000Z',
          'turn.accepted',
          { message: 'Implement the bounded replay proof.' }
        ),
        event(
          childSessionId,
          'child-event-2',
          '2026-08-16T10:01:00.000Z',
          'message.completed',
          { role: 'assistant', text: 'The proof is complete.' }
        ),
        event(
          childSessionId,
          'child-event-3',
          '2026-08-16T10:01:30.000Z',
          'turn.completed',
          { summary: 'Child work completed.' }
        )
      ]
    );
    const legacyBytes = new Map(
      await Promise.all(
        [managerSource.sessionPath, managerSource.eventsPath, childSource.sessionPath, childSource.eventsPath].map(
          async (path) => [path, await readFile(path)] as const
        )
      )
    );

    const firstRuntime = createRuntime(root);
    const registration = await firstRuntime.service.registerProject(
      manifestPath,
      'test',
      'D-APP-73'
    );
    const socketPath = join(firstRuntime.runtimeDirectory, 'control.sock');
    const canonicalSessionRoot = join(
      firstRuntime.runtimeDirectory,
      'projects',
      'chirality-app-dev',
      'sessions'
    );
    await expect(access(join(canonicalSessionRoot, managerSessionId, 'session.json'))).rejects.toThrow();
    await expect(access(join(canonicalSessionRoot, childSessionId, 'session.json'))).rejects.toThrow();

    const firstDaemon = new RuntimeDaemon({
      runtimeDirectory: firstRuntime.runtimeDirectory,
      socketPath,
      service: firstRuntime.service
    });
    activeDaemons.push(firstDaemon);
    await firstDaemon.start();
    const desktopClient = new RuntimeClient({
      socketPath,
      tokenFile: registration.tokenFile
    });
    const cliRuntimeClient = new RuntimeClient({
      socketPath,
      tokenFile: registration.tokenFile
    });
    const desktop = new RuntimeDaemonHarnessPort(
      desktopClient,
      'chirality-app-dev',
      canonicalProjectRoot
    );

    const desktopManagerReplay = await desktop.replaySession(managerSessionId);
    const desktopChildReplay = await desktop.replaySession(childSessionId);
    const cliManagerReplay = await replayThroughCli(
      cliRuntimeClient,
      'chirality-app-dev',
      managerSessionId,
      root
    );
    const cliChildReplay = await replayThroughCli(
      cliRuntimeClient,
      'chirality-app-dev',
      childSessionId,
      root
    );

    expect(desktopManagerReplay).toEqual(cliManagerReplay);
    expect(desktopChildReplay).toEqual(cliChildReplay);
    expect(cliManagerReplay.session).toMatchObject({
      sessionId: managerSessionId,
      role: 'agent1',
      agentType: 1,
      engineSelection
    });
    expect(cliChildReplay.session).toMatchObject({
      sessionId: childSessionId,
      role: 'agent2',
      agentType: 2,
      parentSessionId: managerSessionId,
      engineSelection
    });
    expect(cliManagerReplay.events.map(({ eventId }) => eventId)).toEqual([
      'manager-event-1',
      'manager-event-2'
    ]);
    expect(cliChildReplay.events.map(({ eventId }) => eventId)).toEqual([
      'child-event-1',
      'child-event-2',
      'child-event-3'
    ]);
    await expect(access(join(canonicalSessionRoot, managerSessionId, 'session.json'))).resolves.toBeUndefined();
    await expect(access(join(canonicalSessionRoot, childSessionId, 'session.json'))).resolves.toBeUndefined();
    for (const [path, original] of legacyBytes) {
      await expect(readFile(path)).resolves.toEqual(original);
    }

    const firstHierarchy = buildRecordedAgentHierarchy(
      // Deliberately present the child first: hierarchy must come from the
      // recorded role/parentSessionId fields, not replay or display order.
      [cliChildReplay.session, cliManagerReplay.session].map((session) => ({
        ...session,
        sourceReference: `session:${session.sessionId}`,
        observedAt: '2026-08-16T10:03:00.000Z',
        currency: 'CURRENT'
      }))
    );
    expect(firstHierarchy.roots).toEqual([
      expect.objectContaining({ sessionId: managerSessionId, role: 'agent1' })
    ]);
    expect(firstHierarchy.childrenByParentSessionId[managerSessionId]).toEqual([
      expect.objectContaining({
        sessionId: childSessionId,
        role: 'agent2',
        parentage: {
          state: 'RECORDED',
          parentSessionId: managerSessionId,
          parentAvailable: true
        }
      })
    ]);
    expect(firstHierarchy.detached).toEqual([]);
    expect(firstHierarchy.unresolvedParentSessionIds).toEqual([]);

    await firstDaemon.stop();
    const restartedRuntime = createRuntime(root);
    const restartedDaemon = new RuntimeDaemon({
      runtimeDirectory: restartedRuntime.runtimeDirectory,
      socketPath,
      service: restartedRuntime.service
    });
    activeDaemons.push(restartedDaemon);
    await restartedDaemon.start();
    const restartedDesktopClient = new RuntimeClient({
      socketPath,
      tokenFile: registration.tokenFile
    });
    const restartedCliRuntimeClient = new RuntimeClient({
      socketPath,
      tokenFile: registration.tokenFile
    });
    const restartedDesktop = new RuntimeDaemonHarnessPort(
      restartedDesktopClient,
      'chirality-app-dev',
      canonicalProjectRoot
    );
    const restartedDesktopManager = await restartedDesktop.replaySession(managerSessionId);
    const restartedDesktopChild = await restartedDesktop.replaySession(childSessionId);
    const restartedCliManager = await replayThroughCli(
      restartedCliRuntimeClient,
      'chirality-app-dev',
      managerSessionId,
      root
    );
    const restartedCliChild = await replayThroughCli(
      restartedCliRuntimeClient,
      'chirality-app-dev',
      childSessionId,
      root
    );

    expect(restartedDesktopManager).toEqual(cliManagerReplay);
    expect(restartedDesktopChild).toEqual(cliChildReplay);
    expect(restartedCliManager).toEqual(cliManagerReplay);
    expect(restartedCliChild).toEqual(cliChildReplay);
    for (const [path, original] of legacyBytes) {
      await expect(readFile(path)).resolves.toEqual(original);
    }

    const restartedHierarchy = buildRecordedAgentHierarchy(
      [restartedCliManager.session, restartedCliChild.session].map((session) => ({
        ...session,
        sourceReference: `session:${session.sessionId}`,
        observedAt: '2026-08-16T10:04:00.000Z',
        currency: 'CURRENT'
      }))
    );
    expect(restartedHierarchy.childrenByParentSessionId[managerSessionId]).toEqual([
      expect.objectContaining({
        sessionId: childSessionId,
        role: 'agent2',
        parentage: expect.objectContaining({ parentSessionId: managerSessionId })
      })
    ]);
  }, 15_000);
});
