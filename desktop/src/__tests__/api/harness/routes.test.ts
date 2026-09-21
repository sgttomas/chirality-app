import { mkdtemp, mkdir, readFile, rm, writeFile } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { afterAll, afterEach, beforeAll, beforeEach, describe, expect, it, vi } from 'vitest';

type SessionRecord = {
  sessionId: string;
  projectRoot: string;
  persona: string;
  mode: string;
  createdAt: string;
  updatedAt: string;
  engineSelection?: {
    adapterId: string;
    providerId: string;
    model: string;
  };
  engineSessionId?: string;
  adapterSession?: {
    engineSessionId?: string;
    transcriptPath?: string;
    storeKey?: string;
    packageName?: string;
    packageVersion?: string;
  };
  claudeSessionId?: string;
  sdkPackageVersion?: string;
  bootFingerprint?: string;
  runtimeFingerprint?: {
    schemaVersion: string;
    toolRegistryVersion: string;
    sdkPackageVersion: string;
    engineAdapter?: {
      adapterId: string;
      providerId: string;
      model: string;
    };
    mcpServers: Array<{ name: string; version: string; toolNames: string[] }>;
    fingerprintSha256: string;
  };
  bootedAt?: string;
  model?: string;
};

type RouteModules = {
  createRoute: typeof import('../../../app/api/harness/session/create/route');
  listRoute: typeof import('../../../app/api/harness/session/list/route');
  idRoute: typeof import('../../../app/api/harness/session/[id]/route');
  eventsRoute: typeof import('../../../app/api/harness/session/[id]/events/route');
  bootRoute: typeof import('../../../app/api/harness/session/boot/route');
  turnRoute: typeof import('../../../app/api/harness/turn/route');
  interruptRoute: typeof import('../../../app/api/harness/interrupt/route');
  runtimeModule: typeof import('../../../lib/harness/runtime');
  daemonPortModule: typeof import('../../../lib/runtime-client/daemon-harness-port');
};

type TestContext = {
  tmpRoot: string;
  projectRoot: string;
  instructionRoot: string;
};

let context: TestContext;
let cachedRouteModules: RouteModules | undefined;

async function loadRouteModules(): Promise<RouteModules> {
  const createRoute = await import('../../../app/api/harness/session/create/route');
  const listRoute = await import('../../../app/api/harness/session/list/route');
  const idRoute = await import('../../../app/api/harness/session/[id]/route');
  const eventsRoute = await import('../../../app/api/harness/session/[id]/events/route');
  const bootRoute = await import('../../../app/api/harness/session/boot/route');
  const turnRoute = await import('../../../app/api/harness/turn/route');
  const interruptRoute = await import('../../../app/api/harness/interrupt/route');
  const runtimeModule = await import('../../../lib/harness/runtime');
  const daemonPortModule = await import('../../../lib/runtime-client/daemon-harness-port');

  return {
    createRoute,
    listRoute,
    idRoute,
    eventsRoute,
    bootRoute,
    turnRoute,
    interruptRoute,
    runtimeModule,
    daemonPortModule
  };
}

async function importRouteModules(): Promise<RouteModules> {
  if (!cachedRouteModules) {
    throw new Error('Route modules were not loaded before the test started');
  }
  cachedRouteModules.runtimeModule.resetHarnessRuntimeForTests();
  const { createFakeDaemonHarnessPort } = await import('./fake-daemon-harness-port');
  cachedRouteModules.daemonPortModule.installDaemonHarnessPort(
    createFakeDaemonHarnessPort()
  );
  return cachedRouteModules;
}

async function createSession(
  routes: RouteModules,
  projectRoot: string,
  overrides?: {
    persona?: string;
    mode?: string;
  }
): Promise<{ response: Response; body: { session: SessionRecord } }> {
  const response = await routes.createRoute.POST(
    new Request('http://localhost/api/harness/session/create', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        projectRoot,
        persona: overrides?.persona ?? 'WORKING_ITEMS',
        mode: overrides?.mode
      })
    })
  );

  const body = (await response.json()) as { session: SessionRecord };
  return { response, body };
}

function expectOrdered(text: string, fragments: string[]): void {
  let current = -1;
  for (const fragment of fragments) {
    const index = text.indexOf(fragment);
    expect(index).toBeGreaterThan(current);
    current = index;
  }
}

// Preload the route modules once so cold transform/import time is not charged to
// the first route assertion; reset the runtime singleton per test for isolation.
beforeAll(async () => {
  cachedRouteModules = await loadRouteModules();
}, 30000);

beforeEach(async () => {
  const tmpRoot = await mkdtemp(path.join(os.tmpdir(), 'chirality-harness-routes-'));
  const projectRoot = path.join(tmpRoot, 'project-root');
  const instructionRoot = path.join(tmpRoot, 'instruction-root');
  const agentsDir = path.join(instructionRoot, 'agents');
  const docsDir = path.join(instructionRoot, 'docs');

  await mkdir(projectRoot, { recursive: true });
  await mkdir(agentsDir, { recursive: true });
  await mkdir(docsDir, { recursive: true });

  await writeFile(path.join(projectRoot, 'README.md'), '# fixture\n', 'utf8');
  await writeFile(path.join(instructionRoot, 'AGENTS.md'), '# agents index\n', 'utf8');
  await writeFile(path.join(instructionRoot, 'README.md'), '# instruction root\n', 'utf8');
  await writeFile(path.join(agentsDir, 'AGENT_WORKING_ITEMS.md'), '# persona fixture\n', 'utf8');
  await writeFile(path.join(agentsDir, 'AGENT_HELP_HUMAN.md'), '# helper persona fixture\n', 'utf8');
  await writeFile(path.join(docsDir, 'DIRECTIVE.md'), '# directive\n', 'utf8');
  await writeFile(path.join(docsDir, 'CONTRACT.md'), '# contract\n', 'utf8');
  await writeFile(path.join(docsDir, 'SPEC.md'), '# spec\n', 'utf8');
  await writeFile(path.join(docsDir, 'TYPES.md'), '# types\n', 'utf8');
  await writeFile(path.join(docsDir, 'PLAN.md'), '# plan\n', 'utf8');

  process.env.CHIRALITY_SESSION_ROOT = path.join(tmpRoot, '.chirality', 'sessions');
  process.env.CHIRALITY_INSTRUCTION_ROOT = instructionRoot;
  // Keep the provider default deterministic: with the D-APP-18 key-aware default,
  // an ambient Anthropic key would otherwise flip the unset-provider default to
  // agentSdk. Clear provider + key state so these route tests exercise the stub.
  delete process.env.CHIRALITY_HARNESS_PROVIDER;
  delete process.env.ANTHROPIC_API_KEY;
  delete process.env.CHIRALITY_ANTHROPIC_API_KEY;
  delete (globalThis as Record<string, unknown>).__CHIRALITY_UI_API_KEY__;
  // Compress the stub provider's simulated stream pacing: these route tests
  // assert event ordering and payload content, not real-time cadence. Tests
  // that DO depend on cadence (interrupting an un-marked turn mid-stream)
  // restore the production defaults locally.
  process.env.CHIRALITY_STUB_CHUNK_DELAY_MS = '1';
  process.env.CHIRALITY_STUB_POLL_DELAY_MS = '5';
  context = { tmpRoot, projectRoot, instructionRoot };
});

afterEach(async () => {
  vi.restoreAllMocks();
  cachedRouteModules?.runtimeModule.resetHarnessRuntimeForTests();
  cachedRouteModules?.daemonPortModule.resetDaemonHarnessPortForTests();
  delete process.env.CHIRALITY_SESSION_ROOT;
  delete process.env.CHIRALITY_INSTRUCTION_ROOT;
  delete process.env.CHIRALITY_ENABLE_SUBAGENTS;
  delete process.env.CHIRALITY_HARNESS_PROVIDER;
  delete process.env.ANTHROPIC_API_KEY;
  delete process.env.CHIRALITY_ANTHROPIC_API_KEY;
  delete process.env.CHIRALITY_STUB_CHUNK_DELAY_MS;
  delete process.env.CHIRALITY_STUB_POLL_DELAY_MS;
  await rm(context.tmpRoot, { recursive: true, force: true });
});

afterAll(() => {
  cachedRouteModules?.runtimeModule.resetHarnessRuntimeForTests();
  cachedRouteModules?.daemonPortModule.resetDaemonHarnessPortForTests();
});

describe('Harness API baseline routes', () => {
  it('supports session create/list/get/delete happy path', async () => {
    const routes = await importRouteModules();

    const { response: createResponse, body: createBody } = await createSession(
      routes,
      context.projectRoot
    );
    expect(createResponse.status).toBe(200);
    expect(createBody.session.projectRoot).toBe(context.projectRoot);

    const listResponse = await routes.listRoute.GET(
      new Request(
        `http://localhost/api/harness/session/list?projectRoot=${encodeURIComponent(context.projectRoot)}`
      )
    );
    expect(listResponse.status).toBe(200);
    const listBody = (await listResponse.json()) as { sessions: SessionRecord[] };
    expect(listBody.sessions.map((item) => item.sessionId)).toContain(createBody.session.sessionId);

    const getResponse = await routes.idRoute.GET(new Request('http://localhost'), {
      params: Promise.resolve({ id: createBody.session.sessionId })
    });
    expect(getResponse.status).toBe(200);

    const deleteResponse = await routes.idRoute.DELETE(new Request('http://localhost'), {
      params: Promise.resolve({ id: createBody.session.sessionId })
    });
    expect(deleteResponse.status).toBe(200);
    expect(await deleteResponse.json()).toEqual({ ok: true });

    const getAfterDelete = await routes.idRoute.GET(new Request('http://localhost'), {
      params: Promise.resolve({ id: createBody.session.sessionId })
    });
    expect(getAfterDelete.status).toBe(404);
    expect(await getAfterDelete.json()).toMatchObject({
      error: { type: 'SESSION_NOT_FOUND' }
    });
  });

  it('returns typed validation failure for missing projectRoot', async () => {
    const routes = await importRouteModules();

    const response = await routes.createRoute.POST(
      new Request('http://localhost/api/harness/session/create', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({})
      })
    );

    expect(response.status).toBe(400);
    expect(await response.json()).toMatchObject({
      error: {
        type: 'INVALID_REQUEST'
      }
    });
  });

  it('returns typed failure when projectRoot is inaccessible at create time', async () => {
    const routes = await importRouteModules();
    const missingProjectRoot = path.join(context.tmpRoot, 'missing-project-root');

    const response = await routes.createRoute.POST(
      new Request('http://localhost/api/harness/session/create', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ projectRoot: missingProjectRoot })
      })
    );

    expect(response.status).toBe(404);
    expect(await response.json()).toMatchObject({
      error: {
        type: 'WORKING_ROOT_INACCESSIBLE'
      }
    });
  });

  it('rejects projectRoot selections that overlap instruction root', async () => {
    const routes = await importRouteModules();
    const conflictingProjectRoot = path.join(context.instructionRoot, 'execution');
    await mkdir(conflictingProjectRoot, { recursive: true });

    const response = await routes.createRoute.POST(
      new Request('http://localhost/api/harness/session/create', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ projectRoot: conflictingProjectRoot })
      })
    );

    expect(response.status).toBe(409);
    expect(await response.json()).toMatchObject({
      error: {
        type: 'WORKING_ROOT_CONFLICT'
      }
    });
  });

  it('boots sessions and persists boot metadata', async () => {
    const routes = await importRouteModules();
    const runtime = routes.runtimeModule.getHarnessRuntime();
    const { body } = await createSession(routes, context.projectRoot);
    await runtime.sessionManager.save(body.session.sessionId, {
      adapterSession: {
        engineSessionId: 'stub_existing_engine',
        transcriptPath: '/canonical/session/adapter-transcript.jsonl',
        storeKey: 'opaque-adapter-store-key'
      }
    });

    const bootResponse = await routes.bootRoute.POST(
      new Request('http://localhost/api/harness/session/boot', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ sessionId: body.session.sessionId, opts: { model: 'claude-test' } })
      })
    );

    expect(bootResponse.status).toBe(200);
    const bootBody = (await bootResponse.json()) as {
      session: SessionRecord;
      boot: {
        engineSessionId: string;
        adapterId: string;
        providerId: string;
        model: string;
        claudeSessionId?: string;
        bootFingerprint: string;
        runtimeFingerprint: NonNullable<SessionRecord['runtimeFingerprint']>;
        bootedAt: string;
      };
    };

    expect(bootBody.boot).toMatchObject({
      engineSessionId: 'stub_existing_engine',
      adapterId: 'stub',
      providerId: 'stub',
      model: 'claude-test'
    });
    expect(bootBody.boot.claudeSessionId).toBeUndefined();
    expect(bootBody.session.claudeSessionId).toBeUndefined();
    expect(typeof bootBody.boot.bootFingerprint).toBe('string');
    expect(bootBody.boot.bootFingerprint).toMatch(/^[a-f0-9]{64}$/);
    expect(bootBody.boot.bootFingerprint).toBe(
      runtime.personaManager.getBootFingerprint('WORKING_ITEMS', 'direct', context.projectRoot, [
        'read',
        'write',
        'bash'
      ])
    );
    expect(typeof bootBody.boot.bootedAt).toBe('string');
    expect(bootBody.session.bootFingerprint).toBe(bootBody.boot.bootFingerprint);
    expect(bootBody.session.sdkPackageVersion).toBeUndefined();
    expect(bootBody.session.engineSelection).toEqual({
      adapterId: 'stub',
      providerId: 'stub',
      model: expect.any(String)
    });
    expect(bootBody.session.adapterSession).toEqual({
      engineSessionId: 'stub_existing_engine',
      transcriptPath: '/canonical/session/adapter-transcript.jsonl',
      storeKey: 'opaque-adapter-store-key'
    });
    expect(bootBody.session.runtimeFingerprint).toEqual(bootBody.boot.runtimeFingerprint);
    expect(bootBody.boot.runtimeFingerprint).toMatchObject({
      schemaVersion: 'harness-runtime-fingerprint.v5.engine-attribution',
      engineAdapter: {
        adapterId: 'stub',
        providerId: 'stub',
        model: 'claude-test'
      },
      managedDelegationPolicyVersion: 'managed-delegation.v3.atomic-coordination',
      toolRegistryVersion: expect.stringMatching(/^harness-tools\./),
      sdkPackageVersion: '0.3.150',
      mcpServers: [
        expect.objectContaining({
          name: 'chirality',
          version: '2.0.0',
          toolNames: expect.arrayContaining(['status_read', 'deps_read'])
        })
      ],
      fingerprintSha256: expect.stringMatching(/^[a-f0-9]{64}$/)
    });
  });

  it('passes subagentGovernance through boot opts without consuming it in fallback resolution', async () => {
    const routes = await importRouteModules();
    const runtime = routes.runtimeModule.getHarnessRuntime();
    const startTurnSpy = vi.spyOn(runtime.agentSdkManager, 'startTurn');
    const { body } = await createSession(routes, context.projectRoot);
    const governance = {
      contextSealed: true,
      pipelineRunApproved: false,
      approvalRef: 'boot-governance-ref'
    };

    const bootResponse = await routes.bootRoute.POST(
      new Request('http://localhost/api/harness/session/boot', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          sessionId: body.session.sessionId,
          opts: {
            model: 'claude-test',
            subagentGovernance: governance
          }
        })
      })
    );

    expect(bootResponse.status).toBe(200);
    expect(startTurnSpy).toHaveBeenCalled();
    expect(startTurnSpy.mock.calls[0]?.[1]).toBe('bootstrap');
    expect(startTurnSpy.mock.calls[0]?.[2]).toMatchObject({
      subagentGovernance: governance
    });
  });

  it('returns SESSION_NOT_FOUND when booting without prior create', async () => {
    const routes = await importRouteModules();

    const bootMissingSession = await routes.bootRoute.POST(
      new Request('http://localhost/api/harness/session/boot', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ sessionId: 'sess_missing' })
      })
    );

    expect(bootMissingSession.status).toBe(404);
    expect(await bootMissingSession.json()).toMatchObject({
      error: {
        type: 'SESSION_NOT_FOUND'
      }
    });
  });

  it('returns SESSION_NOT_FOUND for a well-formed non-existent session id', async () => {
    const routes = await importRouteModules();
    await createSession(routes, context.projectRoot);

    const bootMissingSession = await routes.bootRoute.POST(
      new Request('http://localhost/api/harness/session/boot', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ sessionId: 'sess_00000000-0000-0000-0000-000000000000' })
      })
    );

    expect(bootMissingSession.status).toBe(404);
    expect(await bootMissingSession.json()).toMatchObject({
      error: {
        type: 'SESSION_NOT_FOUND',
        message: expect.any(String)
      }
    });
  });

  it('returns WORKING_ROOT_INACCESSIBLE when booting a session with missing projectRoot', async () => {
    const routes = await importRouteModules();
    const { body } = await createSession(routes, context.projectRoot);
    await rm(context.projectRoot, { recursive: true, force: true });

    const bootResponse = await routes.bootRoute.POST(
      new Request('http://localhost/api/harness/session/boot', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ sessionId: body.session.sessionId })
      })
    );

    expect(bootResponse.status).toBe(404);
    expect(await bootResponse.json()).toMatchObject({
      error: {
        type: 'WORKING_ROOT_INACCESSIBLE'
      }
    });
  });

  it('returns PERSONA_NOT_FOUND when boot references unknown persona', async () => {
    const routes = await importRouteModules();
    const { body } = await createSession(routes, context.projectRoot, {
      persona: 'NON_EXISTENT_PERSONA'
    });

    const bootResponse = await routes.bootRoute.POST(
      new Request('http://localhost/api/harness/session/boot', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ sessionId: body.session.sessionId })
      })
    );

    expect(bootResponse.status).toBe(404);
    expect(await bootResponse.json()).toMatchObject({
      error: {
        type: 'PERSONA_NOT_FOUND'
      }
    });
  });

  it('returns INSTRUCTION_ROOT_INVALID when required instruction files are missing', async () => {
    const routes = await importRouteModules();
    await rm(path.join(context.instructionRoot, 'docs', 'PLAN.md'));
    const { body } = await createSession(routes, context.projectRoot);

    const bootResponse = await routes.bootRoute.POST(
      new Request('http://localhost/api/harness/session/boot', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ sessionId: body.session.sessionId })
      })
    );

    expect(bootResponse.status).toBe(500);
    expect(await bootResponse.json()).toMatchObject({
      error: {
        type: 'INSTRUCTION_ROOT_INVALID'
      }
    });
  });

  it('preserves INSTRUCTION_ROOT_INVALID taxonomy across boot route bundle boundaries', async () => {
    const routes = await importRouteModules();
    const createRouteBundleA = routes.createRoute;
    const runtimeBundleA = routes.runtimeModule;
    runtimeBundleA.resetHarnessRuntimeForTests();

    const createResponse = await createRouteBundleA.POST(
      new Request('http://localhost/api/harness/session/create', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ projectRoot: context.projectRoot })
      })
    );
    expect(createResponse.status).toBe(200);
    const createBody = (await createResponse.json()) as { session: SessionRecord };
    const runtimeBeforeBundleSplit = runtimeBundleA.getHarnessRuntime();

    await rm(path.join(context.instructionRoot, 'docs', 'PLAN.md'));

    vi.resetModules();
    const [
      bootRouteBundleB,
      runtimeBundleB,
      daemonPortBundleB,
      fakeDaemonPortBundleB
    ] = await Promise.all([
      import('../../../app/api/harness/session/boot/route'),
      import('../../../lib/harness/runtime'),
      import('../../../lib/runtime-client/daemon-harness-port'),
      import('./fake-daemon-harness-port')
    ]);
    daemonPortBundleB.installDaemonHarnessPort(
      fakeDaemonPortBundleB.createFakeDaemonHarnessPort()
    );
    expect(runtimeBundleB.getHarnessRuntime()).toBe(runtimeBeforeBundleSplit);

    const bootResponse = await bootRouteBundleB.POST(
      new Request('http://localhost/api/harness/session/boot', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ sessionId: createBody.session.sessionId })
      })
    );

    expect(bootResponse.status).toBe(500);
    expect(await bootResponse.json()).toMatchObject({
      error: {
        type: 'INSTRUCTION_ROOT_INVALID',
        message: expect.any(String)
      }
    });
  });

  it('returns SDK_FAILURE when bootstrap turn exits non-zero', async () => {
    const routes = await importRouteModules();
    const { body } = await createSession(routes, context.projectRoot);

    const bootResponse = await routes.bootRoute.POST(
      new Request('http://localhost/api/harness/session/boot', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          sessionId: body.session.sessionId,
          opts: { model: '__BOOT_SDK_FAIL__' }
        })
      })
    );

    expect(bootResponse.status).toBe(500);
    expect(await bootResponse.json()).toMatchObject({
      error: {
        type: 'SDK_FAILURE'
      }
    });
  });

  it('returns pre-stream SESSION_NOT_FOUND when turn session is missing', async () => {
    const routes = await importRouteModules();
    const runtime = routes.runtimeModule.getHarnessRuntime();
    const startTurnSpy = vi.spyOn(runtime.agentSdkManager, 'startTurn');
    const missingSessionId = 'sess_00000000-0000-0000-0000-000000000000';

    const turnResponse = await routes.turnRoute.POST(
      new Request('http://localhost/api/harness/turn', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          sessionId: missingSessionId,
          message: 'hello'
        })
      })
    );

    expect(turnResponse.status).toBe(404);
    expect(turnResponse.headers.get('content-type') ?? '').toContain('application/json');
    expect(await turnResponse.json()).toMatchObject({
      error: {
        type: 'SESSION_NOT_FOUND',
        details: {
          sessionId: missingSessionId
        }
      }
    });
    expect(startTurnSpy).not.toHaveBeenCalled();
  });

  it('streams ordered SSE events for turn execution', async () => {
    const routes = await importRouteModules();
    const { body } = await createSession(routes, context.projectRoot);

    const turnResponse = await routes.turnRoute.POST(
      new Request('http://localhost/api/harness/turn', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          sessionId: body.session.sessionId,
          message: 'Hello from route tests',
          opts: { model: 'claude-test' }
        })
      })
    );

    expect(turnResponse.status).toBe(200);
    expect(turnResponse.headers.get('content-type')).toContain('text/event-stream');

    const sseBody = await turnResponse.text();
    expectOrdered(sseBody, [
      'event: session:init',
      'event: chat:delta',
      'event: chat:complete',
      'event: session:complete',
      'event: process:exit'
    ]);
  });

  it('keeps parent turn execution running when governance metadata is invalid', async () => {
    const routes = await importRouteModules();
    process.env.CHIRALITY_ENABLE_SUBAGENTS = 'true';
    await writeFile(
      path.join(context.instructionRoot, 'agents', 'AGENT_WORKING_ITEMS.md'),
      `---
description: persona fixture
subagents: TASK
---
# persona
AGENT_TYPE: 1
`,
      'utf8'
    );
    await writeFile(
      path.join(context.instructionRoot, 'agents', 'AGENT_TASK.md'),
      `---
description: task fixture
---
# task
AGENT_TYPE: 2

| Property | Value |
|---|---|
| **AGENT_CLASS** | TASK |
`,
      'utf8'
    );

    const runtime = routes.runtimeModule.getHarnessRuntime();
    const startTurnSpy = vi.spyOn(runtime.agentSdkManager, 'startTurn');
    const { body } = await createSession(routes, context.projectRoot);

    const turnResponse = await routes.turnRoute.POST(
      new Request('http://localhost/api/harness/turn', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          sessionId: body.session.sessionId,
          message: 'governance deny should stay non-fatal',
          opts: {
            subagentGovernance: {
              contextSealed: false,
              pipelineRunApproved: true,
              approvalRef: 'gate-ref-1'
            }
          }
        })
      })
    );

    expect(turnResponse.status).toBe(200);
    const sseBody = await turnResponse.text();
    expectOrdered(sseBody, [
      'event: session:init',
      'event: chat:delta',
      'event: chat:complete',
      'event: session:complete',
      'event: process:exit'
    ]);
    expect(startTurnSpy).toHaveBeenCalled();
    expect(startTurnSpy.mock.calls[0]?.[2]).toMatchObject({
      delegatedSubagents: []
    });
  });

  it('does not allow opts.subagentGovernance to bypass runtime environment gate', async () => {
    const routes = await importRouteModules();
    await writeFile(
      path.join(context.instructionRoot, 'agents', 'AGENT_WORKING_ITEMS.md'),
      `---
description: persona fixture
subagents: TASK
---
# persona
AGENT_TYPE: 1
`,
      'utf8'
    );
    await writeFile(
      path.join(context.instructionRoot, 'agents', 'AGENT_TASK.md'),
      `---
description: task fixture
---
# task
AGENT_TYPE: 2

| Property | Value |
|---|---|
| **AGENT_CLASS** | TASK |
`,
      'utf8'
    );

    const runtime = routes.runtimeModule.getHarnessRuntime();
    const startTurnSpy = vi.spyOn(runtime.agentSdkManager, 'startTurn');
    const { body } = await createSession(routes, context.projectRoot);

    const turnResponse = await routes.turnRoute.POST(
      new Request('http://localhost/api/harness/turn', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          sessionId: body.session.sessionId,
          message: 'env gate should block delegation',
          opts: {
            subagentGovernance: {
              contextSealed: true,
              pipelineRunApproved: true,
              approvalRef: 'gate-ref-2'
            }
          }
        })
      })
    );

    expect(turnResponse.status).toBe(200);
    expect(startTurnSpy).toHaveBeenCalled();
    expect(startTurnSpy.mock.calls[0]?.[2]).toMatchObject({
      delegatedSubagents: []
    });
  });

  it('does not treat Pipeline TASK selector state as Type 2 governance approval', async () => {
    const routes = await importRouteModules();
    process.env.CHIRALITY_ENABLE_SUBAGENTS = 'true';
    await writeFile(
      path.join(context.instructionRoot, 'agents', 'AGENT_WORKING_ITEMS.md'),
      `---
description: persona fixture
subagents: TASK
---
# persona
AGENT_TYPE: 1
`,
      'utf8'
    );
    await writeFile(
      path.join(context.instructionRoot, 'agents', 'AGENT_TASK.md'),
      `---
description: task fixture
---
# task
AGENT_TYPE: 2

| Property | Value |
|---|---|
| **AGENT_CLASS** | TASK |
`,
      'utf8'
    );

    const runtime = routes.runtimeModule.getHarnessRuntime();
    const startTurnSpy = vi.spyOn(runtime.agentSdkManager, 'startTurn');
    const warnSpy = vi.spyOn(console, 'warn').mockImplementation(() => {});
    const { body } = await createSession(routes, context.projectRoot);

    const turnResponse = await routes.turnRoute.POST(
      new Request('http://localhost/api/harness/turn', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          sessionId: body.session.sessionId,
          message: 'pipeline selector intent is not delegation approval',
          opts: {
            pipelineIntent: {
              category: 'TASK',
              taskAgent: 'TASK',
              taskScopeMode: 'DELIVERABLES',
              scopeKey: 'PKG-08::DEL-08-03'
            }
          }
        })
      })
    );

    expect(turnResponse.status).toBe(200);
    expect(startTurnSpy).toHaveBeenCalled();
    expect(startTurnSpy.mock.calls[0]?.[2]).toMatchObject({
      delegatedSubagents: []
    });
    expect(warnSpy).toHaveBeenCalledWith(
      '[harness/options] Ignoring unknown opts field(s): pipelineIntent'
    );
  });

  it('passes delegated subagents when governance gates are satisfied', async () => {
    const routes = await importRouteModules();
    process.env.CHIRALITY_ENABLE_SUBAGENTS = 'true';
    await writeFile(
      path.join(context.instructionRoot, 'agents', 'AGENT_WORKING_ITEMS.md'),
      `---
description: persona fixture
subagents: TASK
---
# persona
AGENT_TYPE: 1
`,
      'utf8'
    );
    await writeFile(
      path.join(context.instructionRoot, 'agents', 'AGENT_TASK.md'),
      `---
description: task fixture
---
# task
AGENT_TYPE: 2

| Property | Value |
|---|---|
| **AGENT_CLASS** | TASK |
`,
      'utf8'
    );

    const runtime = routes.runtimeModule.getHarnessRuntime();
    const startTurnSpy = vi.spyOn(runtime.agentSdkManager, 'startTurn');
    const { body } = await createSession(routes, context.projectRoot);

    const turnResponse = await routes.turnRoute.POST(
      new Request('http://localhost/api/harness/turn', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          sessionId: body.session.sessionId,
          message: 'governance allow path',
          opts: {
            subagentGovernance: {
              contextSealed: true,
              pipelineRunApproved: true,
              approvalRef: 'gate-ref-3',
              approvedBy: 'human-reviewer'
            }
          }
        })
      })
    );

    expect(turnResponse.status).toBe(200);
    expect(startTurnSpy).toHaveBeenCalled();
    expect(startTurnSpy.mock.calls[0]?.[2]).toMatchObject({
      delegatedSubagents: ['TASK']
    });
  });

  it('emits typed process-exit metadata when runtime turn execution fails', async () => {
    const routes = await importRouteModules();
    const { body } = await createSession(routes, context.projectRoot);

    const turnResponse = await routes.turnRoute.POST(
      new Request('http://localhost/api/harness/turn', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          sessionId: body.session.sessionId,
          message: 'TURN_SDK_FAIL_TEST'
        })
      })
    );

    expect(turnResponse.status).toBe(200);
    const sseBody = await turnResponse.text();
    expectOrdered(sseBody, ['event: turn:error', 'event: process:exit']);
    expect(sseBody).toContain('"phase":"mid-stream"');
    expect(sseBody).toContain('"message":"Turn failed before completion"');
    expect(sseBody).toContain('"severity":"error"');
    expect(sseBody).toContain('"fatal":true');
    expect(sseBody).toContain('"exitCode":1');
    expect(sseBody).toContain('"errorType":"SDK_FAILURE"');
    expect(sseBody).toContain('"error":"Turn failed before completion"');
  });

  it('returns pre-stream MISSING_API_KEY when anthropic provider is selected without API key', async () => {
    process.env.CHIRALITY_HARNESS_PROVIDER = 'anthropic';
    delete process.env.ANTHROPIC_API_KEY;
    delete process.env.CHIRALITY_ANTHROPIC_API_KEY;

    const routes = await importRouteModules();
    const runtime = routes.runtimeModule.getHarnessRuntime();
    const startTurnSpy = vi.spyOn(runtime.agentSdkManager, 'startTurn');
    const { body } = await createSession(routes, context.projectRoot);

    const turnResponse = await routes.turnRoute.POST(
      new Request('http://localhost/api/harness/turn', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          sessionId: body.session.sessionId,
          message: 'hello'
        })
      })
    );

    expect(turnResponse.status).toBe(503);
    expect(turnResponse.headers.get('content-type') ?? '').toContain('application/json');
    expect(await turnResponse.json()).toMatchObject({
      error: {
        type: 'MISSING_API_KEY'
      }
    });
    expect(startTurnSpy).not.toHaveBeenCalled();
  });

  it('rejects attachment-only turns when all attachments fail and no text remains', async () => {
    const routes = await importRouteModules();
    const { body } = await createSession(routes, context.projectRoot);

    const response = await routes.turnRoute.POST(
      new Request('http://localhost/api/harness/turn', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          sessionId: body.session.sessionId,
          message: '   ',
          attachments: ['/does/not/exist.txt']
        })
      })
    );

    expect(response.status).toBe(400);
    expect(await response.json()).toMatchObject({
      error: {
        type: 'ATTACHMENT_FAILURE',
        message: 'Turn requires text content or at least one valid attachment',
        details: {
          category: 'ALL_ATTACHMENTS_FAILED_NO_TEXT',
          rejectedAttachmentCount: 1,
          attachmentErrors: [
            {
              path: '/does/not/exist.txt',
              reason: expect.stringContaining('Attachment file not found')
            }
          ]
        }
      }
    });
  });

  it('prepends attachment warning context when partial attachment resolution succeeds', async () => {
    const routes = await importRouteModules();
    const runtime = routes.runtimeModule.getHarnessRuntime();
    const startTurnSpy = vi.spyOn(runtime.agentSdkManager, 'startTurn');
    const { body } = await createSession(routes, context.projectRoot);
    const validAttachmentPath = path.join(context.projectRoot, 'sample.txt');
    await writeFile(validAttachmentPath, 'attachment fixture', 'utf8');

    const response = await routes.turnRoute.POST(
      new Request('http://localhost/api/harness/turn', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          sessionId: body.session.sessionId,
          message: 'Review attached context',
          attachments: [validAttachmentPath, '/does/not/exist.bin']
        })
      })
    );

    expect(response.status).toBe(200);
    await response.text();

    const contentBlocks = startTurnSpy.mock.calls[0]?.[3] as
      | Array<
          | { type: 'text'; text: string }
          | { type: 'file'; path: string; mimeType: string }
        >
      | undefined;
    expect(contentBlocks).toBeDefined();
    expect(contentBlocks?.[0]).toMatchObject({
      type: 'text'
    });
    if (!contentBlocks || contentBlocks.length === 0 || contentBlocks[0].type !== 'text') {
      throw new Error('Expected a warning text block as the first content block');
    }
    expect(contentBlocks[0].text).toContain(
      'Attachment warning: 1 attachment(s) could not be processed. Continuing with available content.'
    );
    expect(contentBlocks[0].text).toContain('Rejected attachments:');
    expect(contentBlocks[0].text).toContain('- exist.bin: Unsupported attachment extension');
    expect(contentBlocks[1]).toMatchObject({
      type: 'text',
      text: 'Review attached context'
    });
    expect(contentBlocks.some((block) => block.type === 'file' && block.path === validAttachmentPath)).toBe(
      true
    );
  });

  it('uses string prompt mode when no executable attachments are present', async () => {
    const routes = await importRouteModules();
    const runtime = routes.runtimeModule.getHarnessRuntime();
    const startTurnSpy = vi.spyOn(runtime.agentSdkManager, 'startTurn');
    const { body } = await createSession(routes, context.projectRoot);

    const response = await routes.turnRoute.POST(
      new Request('http://localhost/api/harness/turn', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          sessionId: body.session.sessionId,
          message: 'text-only turn'
        })
      })
    );

    expect(response.status).toBe(200);
    await response.text();
    expect(startTurnSpy).toHaveBeenCalled();
    expect(startTurnSpy.mock.calls[0]?.[1]).toBe('text-only turn');
    expect(startTurnSpy.mock.calls[0]?.[3]).toBeUndefined();
  });

  it('falls back to string prompt mode with warning text when all attachments fail but text remains', async () => {
    const routes = await importRouteModules();
    const runtime = routes.runtimeModule.getHarnessRuntime();
    const startTurnSpy = vi.spyOn(runtime.agentSdkManager, 'startTurn');
    const { body } = await createSession(routes, context.projectRoot);
    const missingPath = path.join(context.projectRoot, 'missing.txt');

    const response = await routes.turnRoute.POST(
      new Request('http://localhost/api/harness/turn', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          sessionId: body.session.sessionId,
          message: 'continue without attachments',
          attachments: [missingPath]
        })
      })
    );

    expect(response.status).toBe(200);
    await response.text();
    expect(startTurnSpy).toHaveBeenCalled();
    expect(startTurnSpy.mock.calls[0]?.[3]).toBeUndefined();
    const turnMessage = startTurnSpy.mock.calls[0]?.[1];
    expect(typeof turnMessage).toBe('string');
    expect(turnMessage).toContain(
      'Attachment warning: 1 attachment(s) could not be processed. Continuing with available content.'
    );
    expect(turnMessage).toContain('Rejected attachments:');
    expect(turnMessage).toContain('- missing.txt: Attachment file not found:');
    expect(turnMessage).toContain('continue without attachments');
    expect(turnMessage).toContain(missingPath);
  });

  it('includes omission summary when warning detail entries exceed the configured cap', async () => {
    const routes = await importRouteModules();
    const runtime = routes.runtimeModule.getHarnessRuntime();
    const startTurnSpy = vi.spyOn(runtime.agentSdkManager, 'startTurn');
    const { body } = await createSession(routes, context.projectRoot);

    const response = await routes.turnRoute.POST(
      new Request('http://localhost/api/harness/turn', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          sessionId: body.session.sessionId,
          message: 'keep running with warning summary',
          attachments: [
            '/tmp/a.bin',
            '/tmp/b.bin',
            '/tmp/c.bin',
            '/tmp/d.bin'
          ]
        })
      })
    );

    expect(response.status).toBe(200);
    await response.text();
    expect(startTurnSpy).toHaveBeenCalled();
    expect(startTurnSpy.mock.calls[0]?.[3]).toBeUndefined();
    const turnMessage = startTurnSpy.mock.calls[0]?.[1];
    expect(typeof turnMessage).toBe('string');
    expect(turnMessage).toContain(
      'Attachment warning: 4 attachment(s) could not be processed. Continuing with available content.'
    );
    expect(turnMessage).toContain('Rejected attachments:');
    expect(turnMessage).toContain('- a.bin: Unsupported attachment extension');
    expect(turnMessage).toContain('- b.bin: Unsupported attachment extension');
    expect(turnMessage).toContain('- c.bin: Unsupported attachment extension');
    expect(turnMessage).toContain('- ... 1 additional attachment error(s) omitted');
  });

  it('rejects overlapping turns for the same session and releases lock after completion', async () => {
    const routes = await importRouteModules();
    const { body } = await createSession(routes, context.projectRoot);

    const firstTurnResponse = await routes.turnRoute.POST(
      new Request('http://localhost/api/harness/turn', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          sessionId: body.session.sessionId,
          message: 'INTERRUPT_SIGINT_TEST keep this turn active briefly'
        })
      })
    );
    expect(firstTurnResponse.status).toBe(200);

    const reader = firstTurnResponse.body?.getReader();
    expect(reader).toBeTruthy();
    const firstChunk = await reader!.read();
    expect(firstChunk.done).toBe(false);

    const overlappingTurnResponse = await routes.turnRoute.POST(
      new Request('http://localhost/api/harness/turn', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          sessionId: body.session.sessionId,
          message: 'this should be rejected while another turn is active'
        })
      })
    );
    expect(overlappingTurnResponse.status).toBe(409);
    expect(await overlappingTurnResponse.json()).toMatchObject({
      error: {
        type: 'TURN_IN_PROGRESS'
      }
    });

    const interruptResponse = await routes.interruptRoute.POST(
      new Request('http://localhost/api/harness/interrupt', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ sessionId: body.session.sessionId })
      })
    );
    expect(interruptResponse.status).toBe(200);

    while (true) {
      const chunk = await reader!.read();
      if (chunk.done) {
        break;
      }
    }

    const recoveryTurnResponse = await routes.turnRoute.POST(
      new Request('http://localhost/api/harness/turn', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          sessionId: body.session.sessionId,
          message: 'turn lock should be released after completion'
        })
      })
    );
    expect(recoveryTurnResponse.status).toBe(200);
    await recoveryTurnResponse.text();
  });

  it('interrupt endpoint returns ok and marks active turn as interrupted', async () => {
    // This test interrupts an un-marked turn while it is genuinely mid-stream,
    // so it relies on the production chunk cadence; restore the defaults that
    // the suite-wide beforeEach compresses.
    delete process.env.CHIRALITY_STUB_CHUNK_DELAY_MS;
    delete process.env.CHIRALITY_STUB_POLL_DELAY_MS;
    const routes = await importRouteModules();
    const { body } = await createSession(routes, context.projectRoot);

    const turnResponse = await routes.turnRoute.POST(
      new Request('http://localhost/api/harness/turn', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          sessionId: body.session.sessionId,
          message: 'This turn should be interrupted while streaming.'
        })
      })
    );

    const reader = turnResponse.body?.getReader();
    expect(reader).toBeTruthy();

    const decoder = new TextDecoder();
    let streamText = '';

    const firstChunk = await reader!.read();
    if (firstChunk.value) {
      streamText += decoder.decode(firstChunk.value, { stream: true });
    }

    const interruptResponse = await routes.interruptRoute.POST(
      new Request('http://localhost/api/harness/interrupt', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ sessionId: body.session.sessionId })
      })
    );

    expect(interruptResponse.status).toBe(200);
    expect(await interruptResponse.json()).toEqual({ ok: true });

    while (true) {
      const chunk = await reader!.read();
      if (chunk.done) {
        break;
      }
      if (chunk.value) {
        streamText += decoder.decode(chunk.value, { stream: true });
      }
    }

    expect(streamText).toContain('event: process:exit');
    expect(streamText).toContain('"interrupted":true');
    expect(streamText).toContain('"type":"turn.interrupted"');
  });

  it('persists accepted user text and non-user cancellation when the SSE reader disconnects', async () => {
    const secret = 'sk-route-cancel-secret-fixture';
    process.env.CHIRALITY_HARNESS_PROVIDER = 'stub';
    process.env.ANTHROPIC_API_KEY = secret;
    const routes = await importRouteModules();
    const { body } = await createSession(routes, context.projectRoot);

    const turnResponse = await routes.turnRoute.POST(
      new Request('http://localhost/api/harness/turn', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          sessionId: body.session.sessionId,
          message: `INTERRUPT_SIGINT_TEST recover ${secret}`
        })
      })
    );
    const reader = turnResponse.body?.getReader();
    expect(reader).toBeTruthy();
    expect((await reader!.read()).done).toBe(false);
    await reader!.cancel('client disconnected');

    const eventFile = path.join(
      process.env.CHIRALITY_SESSION_ROOT!,
      body.session.sessionId,
      'events.jsonl'
    );
    await writeFile(eventFile, '{"trailing":', { encoding: 'utf8', flag: 'a' });

    const replayResponse = await routes.eventsRoute.GET(
      new Request(`http://localhost/api/harness/session/${body.session.sessionId}/events`),
      { params: Promise.resolve({ id: body.session.sessionId }) }
    );
    const replay = (await replayResponse.json()) as {
      malformedLineCount: number;
      events: Array<{
        turnId?: string;
        type: string;
        data: { role?: string; text?: string };
      }>;
    };
    const accepted = replay.events.find((event) => event.type === 'message.accepted');
    const cancelled = replay.events.find((event) => event.type === 'turn.cancelled');

    expect(replay.malformedLineCount).toBe(1);
    expect(accepted).toMatchObject({
      type: 'message.accepted',
      data: { role: 'user', text: 'INTERRUPT_SIGINT_TEST recover [REDACTED_API_KEY]' }
    });
    expect(cancelled?.turnId).toBe(accepted?.turnId);
    expect(replay.events.map((event) => event.type)).not.toContain('turn.interrupted');
    expect(replay.events.map((event) => event.type)).not.toContain('interruption.requested');
    expect(await readFile(eventFile, 'utf8')).not.toContain(secret);

    const recovery = await routes.turnRoute.POST(
      new Request('http://localhost/api/harness/turn', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ sessionId: body.session.sessionId, message: 'after disconnect' })
      })
    );
    expect(recovery.status).toBe(200);
    await recovery.body?.cancel();
  });

  it('keeps turn and interrupt routes coherent across module-bundle boundaries', async () => {
    const routes = await importRouteModules();
    const createRouteBundleA = routes.createRoute;
    const turnRouteBundleA = routes.turnRoute;
    const runtimeBundleA = routes.runtimeModule;
    runtimeBundleA.resetHarnessRuntimeForTests();

    const createResponse = await createRouteBundleA.POST(
      new Request('http://localhost/api/harness/session/create', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ projectRoot: context.projectRoot })
      })
    );
    expect(createResponse.status).toBe(200);
    const createBody = (await createResponse.json()) as { session: SessionRecord };
    const runtimeBeforeBundleSplit = runtimeBundleA.getHarnessRuntime();

    const turnResponse = await turnRouteBundleA.POST(
      new Request('http://localhost/api/harness/turn', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          sessionId: createBody.session.sessionId,
          message: 'INTERRUPT_SIGINT_TEST cross-bundle coherence'
        })
      })
    );

    expect(turnResponse.status).toBe(200);
    const reader = turnResponse.body?.getReader();
    expect(reader).toBeTruthy();
    const decoder = new TextDecoder();
    let streamText = '';

    const firstChunk = await reader!.read();
    expect(firstChunk.done).toBe(false);
    if (firstChunk.value) {
      streamText += decoder.decode(firstChunk.value, { stream: true });
    }

    vi.resetModules();
    const [
      interruptRouteBundleB,
      runtimeBundleB,
      daemonPortBundleB,
      fakeDaemonPortBundleB
    ] = await Promise.all([
      import('../../../app/api/harness/interrupt/route'),
      import('../../../lib/harness/runtime'),
      import('../../../lib/runtime-client/daemon-harness-port'),
      import('./fake-daemon-harness-port')
    ]);
    daemonPortBundleB.installDaemonHarnessPort(
      fakeDaemonPortBundleB.createFakeDaemonHarnessPort()
    );
    expect(runtimeBundleB.getHarnessRuntime()).toBe(runtimeBeforeBundleSplit);

    const interruptResponse = await interruptRouteBundleB.POST(
      new Request('http://localhost/api/harness/interrupt', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ sessionId: createBody.session.sessionId })
      })
    );
    expect(interruptResponse.status).toBe(200);
    expect(await interruptResponse.json()).toEqual({ ok: true });

    while (true) {
      const chunk = await reader!.read();
      if (chunk.done) {
        break;
      }
      if (chunk.value) {
        streamText += decoder.decode(chunk.value, { stream: true });
      }
    }

    expect(streamText).toContain('event: process:exit');
    expect(streamText).toContain('"interrupted":true');
    expect(streamText).toContain('"type":"turn.interrupted"');
  });

  it('returns typed failure for interrupt on unknown session', async () => {
    const routes = await importRouteModules();

    const interruptResponse = await routes.interruptRoute.POST(
      new Request('http://localhost/api/harness/interrupt', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ sessionId: 'sess_unknown' })
      })
    );

    expect(interruptResponse.status).toBe(404);
    expect(await interruptResponse.json()).toMatchObject({
      error: {
        type: 'SESSION_NOT_FOUND'
      }
    });
  });
});

describe('direct-chat persona gate (D-APP-24)', () => {
  async function writeTypedAgents(): Promise<void> {
    const agentsDir = path.join(context.instructionRoot, 'agents');
    await writeFile(
      path.join(agentsDir, 'AGENT_WORKING_ITEMS.md'),
      'AGENT_TYPE: 1\nAGENT_CLASS: PERSONA\n',
      'utf8'
    );
    await writeFile(
      path.join(agentsDir, 'AGENT_TASK.md'),
      'AGENT_TYPE: 2\nAGENT_CLASS: TASK\n',
      'utf8'
    );
  }

  it('rejects creating a CHAT-mode session with a Type-2 task persona', async () => {
    const routes = await importRouteModules();
    await writeTypedAgents();

    const response = await routes.createRoute.POST(
      new Request('http://localhost/api/harness/session/create', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          projectRoot: context.projectRoot,
          persona: 'TASK',
          mode: 'CHAT'
        })
      })
    );

    expect(response.status).toBe(400);
    expect(await response.json()).toMatchObject({ error: { type: 'INVALID_REQUEST' } });
  });

  it('allows a CHAT-mode session with a Type-1 persona', async () => {
    const routes = await importRouteModules();
    await writeTypedAgents();

    const { response, body } = await createSession(routes, context.projectRoot, {
      persona: 'WORKING_ITEMS',
      mode: 'CHAT'
    });

    expect(response.status).toBe(200);
    expect(body.session.persona).toBe('WORKING_ITEMS');
    expect(body.session.mode).toBe('CHAT');
  });

  it('allows an explicitly untyped CHAT session without creating an agent role', async () => {
    const routes = await importRouteModules();
    const { response, body } = await createSession(routes, context.projectRoot, {
      persona: 'UNTYPED',
      mode: 'CHAT'
    });

    expect(response.status).toBe(200);
    expect(body.session.persona).toBe('UNTYPED');
  });

  it('does not gate non-CHAT sections (workbench may still create any persona)', async () => {
    const routes = await importRouteModules();
    await writeTypedAgents();

    const { response } = await createSession(routes, context.projectRoot, {
      persona: 'TASK',
      mode: 'WORKBENCH'
    });

    expect(response.status).toBe(200);
  });
});

describe('session events replay (D-APP-22)', () => {
  it('replays persisted events with an honest malformed-line count', async () => {
    const routes = await importRouteModules();
    const { body } = await createSession(routes, context.projectRoot, {
      persona: 'WORKING_ITEMS',
      mode: 'WORKBENCH'
    });
    const sessionId = body.session.sessionId;

    const eventsDir = path.join(process.env.CHIRALITY_SESSION_ROOT as string, sessionId);
    await mkdir(eventsDir, { recursive: true });
    const lines = [
      {
        schemaVersion: 1,
        eventId: 'e1',
        sessionId,
        turnId: 'turn_1',
        timestamp: '2026-06-18T00:00:00.000Z',
        type: 'message.completed',
        data: { role: 'user', text: 'Show the file.' }
      },
      {
        schemaVersion: 1,
        eventId: 'e2',
        sessionId,
        turnId: 'turn_1',
        timestamp: '2026-06-18T00:00:01.000Z',
        type: 'message.completed',
        data: { role: 'assistant', text: 'Here is the file.' }
      },
      {
        schemaVersion: 1,
        eventId: 'e3',
        sessionId,
        turnId: 'turn_1',
        timestamp: '2026-06-18T00:00:02.000Z',
        type: 'tool.completed',
        data: {
          toolUseId: 't1',
          toolName: 'Read',
          resultMetadata: { contentItemCount: 1, resultByteLength: 12 }
        }
      },
      {
        schemaVersion: 1,
        eventId: 'e4',
        sessionId,
        turnId: 'turn_1',
        timestamp: '2026-06-18T00:00:03.000Z',
        type: 'turn.completed',
        data: { stopReason: 'end_turn' }
      }
    ];
    await writeFile(
      path.join(eventsDir, 'events.jsonl'),
      `${JSON.stringify(lines[0])}\n{ broken json\n${lines.slice(1)
        .map((line) => JSON.stringify(line))
        .join('\n')}\n`,
      'utf8'
    );

    const response = await routes.eventsRoute.GET(
      new Request(`http://localhost/api/harness/session/${sessionId}/events`),
      { params: Promise.resolve({ id: sessionId }) }
    );

    expect(response.status).toBe(200);
    const replay = (await response.json()) as {
      events: Array<{ eventId: string }>;
      malformedLineCount: number;
      summary: { eventCount: number };
      session: { sessionId: string };
      transcript: {
        itemCount: number;
        terminalStatus?: string;
        items: Array<{ kind: string; text?: string; toolName?: string }>;
      };
    };
    expect(replay.events.map((entry) => entry.eventId)).toEqual(['e1', 'e2', 'e3', 'e4']);
    expect(replay.malformedLineCount).toBe(1);
    expect(replay.summary.eventCount).toBe(4);
    expect(replay.session.sessionId).toBe(sessionId);
    expect(replay.transcript).toMatchObject({
      itemCount: 4,
      terminalStatus: 'completed',
      items: [
        { kind: 'message', text: 'Show the file.' },
        { kind: 'message', text: 'Here is the file.' },
        { kind: 'tool', toolName: 'Read' },
        { kind: 'terminal' }
      ]
    });
  });

  it('returns an empty replay for a session with no event log', async () => {
    const routes = await importRouteModules();
    const { body } = await createSession(routes, context.projectRoot, {
      persona: 'WORKING_ITEMS',
      mode: 'WORKBENCH'
    });
    const sessionId = body.session.sessionId;

    const response = await routes.eventsRoute.GET(
      new Request(`http://localhost/api/harness/session/${sessionId}/events`),
      { params: Promise.resolve({ id: sessionId }) }
    );

    expect(response.status).toBe(200);
    const replay = (await response.json()) as {
      events: unknown[];
      malformedLineCount: number;
      transcript: { itemCount: number; items: unknown[] };
    };
    expect(replay.events).toEqual([]);
    expect(replay.malformedLineCount).toBe(0);
    expect(replay.transcript).toMatchObject({ itemCount: 0, items: [] });
  });

  it('rejects a session id containing path-traversal characters', async () => {
    const routes = await importRouteModules();

    const response = await routes.eventsRoute.GET(
      new Request('http://localhost/api/harness/session/x/events'),
      { params: Promise.resolve({ id: '../../etc' }) }
    );

    expect(response.status).toBe(400);
    expect(await response.json()).toMatchObject({ error: { type: 'INVALID_REQUEST' } });
  });
});
