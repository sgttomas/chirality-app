import { afterEach, describe, expect, it, vi } from 'vitest';
import { HarnessError } from '@chirality/runtime-contracts/errors';
import type { UIEvent } from '@chirality/runtime-contracts/types';
import type {
  DaemonHarnessPort,
  RunningDaemonHarnessTurn
} from '../../../lib/runtime-client/daemon-harness-port';
import {
  installDaemonHarnessPort,
  resetDaemonHarnessPortForTests
} from '../../../lib/runtime-client/daemon-harness-port';
import * as turnRoute from '../../../app/api/harness/turn/route';

// Owner criterion 5 (App v3 trial): the App half of the attachment path. The
// chat panel submits `attachments: preservedAttachments.map(item => item.path)`
// through streamHarnessTurn -> POST /api/harness/turn. This proves the route
// hands those paths to the daemon port verbatim (the port's own forwarding to
// RuntimeClient.turnSession is covered by
// src/__tests__/lib/runtime-daemon-harness-port.test.ts, and the fetch body
// serialization by src/__tests__/lib/harness-client.test.ts).

function unimplemented(): never {
  throw new Error('Unexpected fake daemon-port method');
}

function daemonPort(overrides: Partial<DaemonHarnessPort>): DaemonHarnessPort {
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

function runningTurn(events: UIEvent[]): RunningDaemonHarnessTurn {
  return {
    events: (async function* () {
      for (const event of events) yield event;
    })(),
    cancel: vi.fn(async () => undefined)
  };
}

function post(body: unknown): Request {
  return new Request('http://localhost/api/harness/turn', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body)
  });
}

afterEach(() => {
  resetDaemonHarnessPortForTests();
  vi.restoreAllMocks();
});

describe('POST /api/harness/turn attachment forwarding', () => {
  it('forwards the chat-panel attachment path array to the daemon port unchanged, in order, alongside the v3 turn fields', async () => {
    const turn = vi.fn<DaemonHarnessPort['turn']>(async () =>
      runningTurn([
        { type: 'session:init', data: { engineSessionId: 'thread-1', adapterId: 'codex-app-server', providerId: 'openai', model: 'fixture-model' } } as UIEvent,
        { type: 'chat:complete', data: { text: 'received 3 inputs' } } as UIEvent,
        { type: 'process:exit', data: { exitCode: 0 } } as UIEvent
      ])
    );
    installDaemonHarnessPort(daemonPort({ turn }));

    // Exactly what chat-panel.tsx submitDraft sends: message + selected UiAttachment paths.
    const attachments = ['/registered/project/notes.md', '/registered/project/data.txt'];
    const body = {
      sessionId: 'sess_attach_1',
      message: 'Summarize the attached files.',
      attachments,
      interactionMode: 'chat',
      permissionMode: 'workspaceWrite',
      opts: { mode: 'workspaceWrite' }
    };

    const response = await turnRoute.POST(post(body));

    expect(response.status).toBe(200);
    expect(response.headers.get('content-type')).toContain('text/event-stream');
    expect(turn).toHaveBeenCalledTimes(1);
    const [forwarded, options] = turn.mock.calls[0]!;
    expect(forwarded.attachments).toEqual(attachments);
    expect(forwarded).toMatchObject({
      sessionId: 'sess_attach_1',
      message: 'Summarize the attached files.',
      interactionMode: 'chat',
      permissionMode: 'workspaceWrite',
      opts: { mode: 'workspaceWrite' }
    });
    // The route never rewrites, filters, deduplicates, or reorders paths; that is the runtime's job.
    expect(forwarded).toEqual(body);
    expect(options?.signal).toBeInstanceOf(AbortSignal);

    const sse = await response.text();
    expect(sse).toContain('event: session:init');
    expect(sse).toContain('event: chat:complete\ndata: {"text":"received 3 inputs"}');
    expect(sse).toContain('event: process:exit');
  });

  it('supports attachment-only submissions (empty message) without dropping the paths', async () => {
    const turn = vi.fn<DaemonHarnessPort['turn']>(async () => runningTurn([{ type: 'process:exit', data: { exitCode: 0 } } as UIEvent]));
    installDaemonHarnessPort(daemonPort({ turn }));

    const response = await turnRoute.POST(post({ sessionId: 'sess_attach_2', message: '', attachments: ['/registered/project/only.csv'] }));

    expect(response.status).toBe(200);
    expect(turn.mock.calls[0]?.[0]).toMatchObject({ message: '', attachments: ['/registered/project/only.csv'] });
    await response.text();
  });

  it('returns the daemon port rejection for an unsupported attachment as a pre-stream JSON error', async () => {
    const turn = vi.fn<DaemonHarnessPort['turn']>(async () => {
      throw new HarnessError('INVALID_REQUEST', 400, 'Unsupported attachment extension: .bin');
    });
    installDaemonHarnessPort(daemonPort({ turn }));

    const response = await turnRoute.POST(post({ sessionId: 'sess_attach_3', message: 'Inspect.', attachments: ['/registered/project/archive.bin'] }));

    expect(response.status).toBe(400);
    expect(response.headers.get('content-type') ?? '').toContain('application/json');
    await expect(response.json()).resolves.toMatchObject({
      error: { type: 'INVALID_REQUEST', message: 'Unsupported attachment extension: .bin' }
    });
  });
});
