import { afterEach, describe, expect, it, vi } from 'vitest';
import type {
  DaemonHarnessPort,
  RunningDaemonHarnessTurn
} from '../../../lib/runtime-client/daemon-harness-port';
import {
  installDaemonHarnessPort,
  resetDaemonHarnessPortForTests
} from '../../../lib/runtime-client/daemon-harness-port';
import * as createRoute from '../../../app/api/harness/session/create/route';
import * as steerReceiptRoute from '../../../app/api/harness/session/[id]/turn/steer/receipt/route';
import * as steerRoute from '../../../app/api/harness/session/[id]/turn/steer/route';
import * as turnRoute from '../../../app/api/harness/turn/route';

function unimplemented(): never {
  throw new Error('Unexpected fake daemon-port method');
}

function daemonPort(
  overrides: Partial<DaemonHarnessPort>
): DaemonHarnessPort {
  return {
    createSession: unimplemented,
    listSessions: unimplemented,
    getSession: unimplemented,
    deleteSession: unimplemented,
    bootSession: unimplemented,
    replaySession: unimplemented,
    turn: unimplemented,
    attachTurn: unimplemented,
    turnState: unimplemented,
    listRequests: unimplemented,
    answerRequest: unimplemented,
    steer: unimplemented,
    steerReceipt: unimplemented,
    interrupt: unimplemented,
    decidePermission: unimplemented,
    listAgents: unimplemented,
    listRoles: unimplemented,
    listMethods: unimplemented,
    inspectMethod: unimplemented,
    resolveSelectedContext: unimplemented,
    replaceSelectedMethods: unimplemented,
    getNativePlanCapability: unimplemented,
    listNativePlanRevisions: unimplemented,
    listNativePlanClarifications: unimplemented,
    replyNativePlanClarification: unimplemented,
    exportNativePlan: unimplemented,
    scaffold: unimplemented,
    ...overrides
  };
}

afterEach(() => {
  resetDaemonHarnessPortForTests();
  vi.unstubAllEnvs();
  vi.restoreAllMocks();
});

describe('Desktop daemon harness proxy boundary', () => {
  it('fails closed when the Desktop composition root has not installed a daemon client', async () => {
    vi.stubEnv('CHIRALITY_RUNTIME_SOCKET_PATH', '');
    vi.stubEnv('CHIRALITY_RUNTIME_TOKEN_FILE', '');
    vi.stubEnv('CHIRALITY_RUNTIME_PROJECT_ID', '');
    vi.stubEnv('CHIRALITY_RUNTIME_PROJECT_ROOT', '');

    const response = await createRoute.POST(
      new Request('http://localhost/api/harness/session/create', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ projectRoot: '/registered/project' })
      })
    );

    expect(response.status).toBe(503);
    await expect(response.json()).resolves.toMatchObject({
      error: {
        type: 'ENGINE_UNAVAILABLE',
        message: 'Chirality runtime daemon client is not configured'
      }
    });
  });

  it('promotes a canonical direct persona to the v3 role while preserving its label', async () => {
    const session = {
      sessionId: 'sess_proxy_1',
      projectRoot: '/registered/project',
      persona: 'WORKING_ITEMS',
      mode: 'direct',
      createdAt: '2026-07-22T00:00:00.000Z',
      updatedAt: '2026-07-22T00:00:00.000Z'
    };
    const createSession = vi.fn(async () => ({ session }));
    installDaemonHarnessPort(daemonPort({ createSession }));
    const abortController = new AbortController();

    const response = await createRoute.POST(
      new Request('http://localhost/api/harness/session/create', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          projectRoot: '/registered/project',
          persona: 'WORKING_ITEMS',
          mode: 'direct'
        }),
        signal: abortController.signal
      })
    );

    expect(response.status).toBe(200);
    await expect(response.json()).resolves.toEqual({ session });
    expect(createSession).toHaveBeenCalledWith(
      {
        projectRoot: '/registered/project',
        persona: 'WORKING_ITEMS',
        mode: 'direct',
        roleId: 'WORKING_ITEMS'
      },
      { signal: expect.any(AbortSignal) }
    );
  });

  it('preserves a retired legacy persona for Runtime compatibility routing', async () => {
    const createSession = vi.fn(async (request) => ({ session: { ...request, sessionId: 'legacy' } }));
    installDaemonHarnessPort(daemonPort({ createSession }));
    const response = await createRoute.POST(new Request('http://localhost/api/harness/session/create', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ projectRoot: '/registered/project', persona: 'PROJECT_SETUP', mode: 'direct' })
    }));
    expect(response.status).toBe(200);
    expect(createSession).toHaveBeenCalledWith({
      projectRoot: '/registered/project', persona: 'PROJECT_SETUP', mode: 'direct'
    }, { signal: expect.any(AbortSignal) });
  });

  it('defaults a new unconfigured conversation to HELP_HUMAN', async () => {
    const createSession = vi.fn(async (request) => ({
      session: {
        sessionId: 'sess_helper',
        projectRoot: request.projectRoot,
        persona: request.persona ?? 'HELP_HUMAN',
        mode: request.mode ?? 'chat',
        createdAt: '2026-09-09T00:00:00.000Z',
        updatedAt: '2026-09-09T00:00:00.000Z'
      }
    }));
    installDaemonHarnessPort(daemonPort({ createSession }));
    const response = await createRoute.POST(new Request('http://localhost/api/harness/session/create', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ projectRoot: '/registered/project' })
    }));
    expect(response.status).toBe(200);
    expect(createSession).toHaveBeenCalledWith(expect.objectContaining({
      roleId: 'HELP_HUMAN',
      persona: 'HELP_HUMAN'
    }), expect.anything());
  });

  it('rejects contradictory v3 role and persona identities before daemon dispatch', async () => {
    const createSession = vi.fn();
    installDaemonHarnessPort(daemonPort({ createSession }));
    const response = await createRoute.POST(new Request('http://localhost/api/harness/session/create', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ projectRoot: '/registered/project', roleId: 'HELP_HUMAN', persona: 'WORKING_ITEMS' })
    }));
    expect(response.status).toBe(400);
    expect(createSession).not.toHaveBeenCalled();
  });

  it('preserves legacy SSE event names and propagates reader cancellation to the daemon turn', async () => {
    let release: (() => void) | undefined;
    const cancelled = vi.fn(async () => {
      release?.();
    });
    const runningTurn: RunningDaemonHarnessTurn = {
      events: (async function* () {
        yield {
          type: 'chat:delta' as const,
          data: { text: 'daemon text' }
        };
        await new Promise<void>((resolve) => {
          release = resolve;
        });
      })(),
      cancel: cancelled
    };
    const turn = vi.fn(async () => runningTurn);
    installDaemonHarnessPort(daemonPort({ turn }));

    const response = await turnRoute.POST(
      new Request('http://localhost/api/harness/turn', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          sessionId: 'sess_proxy_1',
          message: 'hello daemon', turnId: 'submitted-turn'
        })
      })
    );
    const reader = response.body?.getReader();
    const connected = await reader?.read();
    expect(new TextDecoder().decode(connected?.value)).toBe('event: transport:connected\ndata: {}\n\n');
    const first = await reader?.read();

    expect(response.headers.get('content-type')).toContain('text/event-stream');
    expect(new TextDecoder().decode(first?.value)).toBe(
      'event: chat:delta\ndata: {"text":"daemon text"}\n\n'
    );

    await reader?.cancel();
    expect(cancelled).toHaveBeenCalledOnce();
    expect(turn).toHaveBeenCalledWith(
      { sessionId: 'sess_proxy_1', message: 'hello daemon', turnId: 'submitted-turn' },
      { signal: expect.any(AbortSignal) }
    );
  });
});


it('routes steering by the owning session and validates Runtime turn and operation identity', async () => {
  const steer = vi.fn(async (_sessionId, request) => ({ operationId: request.operationId, turnId: request.expectedTurnId, status: 'accepted' as const }));
  installDaemonHarnessPort(daemonPort({ steer }));
  const response = await steerRoute.POST(new Request('http://localhost/api/harness/session/s/turn/steer', { method: 'POST', body: JSON.stringify({ operationId: 'op', expectedTurnId: 'runtime-turn', text: 'Use this correction', providerThreadId: 'untrusted' }) }), { params: Promise.resolve({ id: 's' }) });
  expect(response.status).toBe(200);
  expect(steer).toHaveBeenCalledWith('s', { operationId: 'op', expectedTurnId: 'runtime-turn', text: 'Use this correction' }, expect.any(Object));
  const invalid = await steerRoute.POST(new Request('http://localhost/api/harness/session/s/turn/steer', { method: 'POST', body: JSON.stringify({ operationId: 'op', text: 'Missing turn' }) }), { params: Promise.resolve({ id: 's' }) });
  expect(invalid.status).toBe(400);
  expect(steer).toHaveBeenCalledTimes(1);
});


it('checks a receipt through the non-dispatch port method without forwarding text', async () => {
  const steerReceipt = vi.fn(async (_sessionId, request) => ({ operationId: request.operationId, turnId: request.expectedTurnId, status: 'unknown' as const }));
  const steer = vi.fn(unimplemented);
  installDaemonHarnessPort(daemonPort({ steerReceipt, steer }));
  const response = await steerReceiptRoute.POST(new Request('http://localhost/api/harness/session/s/turn/steer/receipt', { method: 'POST', body: JSON.stringify({ operationId: 'op', expectedTurnId: 'runtime-turn', text: 'Never forward this' }) }), { params: Promise.resolve({ id: 's' }) });
  expect(response.status).toBe(200);
  expect(steerReceipt).toHaveBeenCalledWith('s', { operationId: 'op', expectedTurnId: 'runtime-turn' }, expect.any(Object));
  expect(steer).not.toHaveBeenCalled();
});
