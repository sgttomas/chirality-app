import { afterEach, describe, expect, it, vi } from 'vitest';
import type { DaemonHarnessPort, DaemonTurnFrame, RunningDaemonHarnessTurn } from '../../../lib/runtime-client/daemon-harness-port';
import { installDaemonHarnessPort, resetDaemonHarnessPortForTests } from '../../../lib/runtime-client/daemon-harness-port';
import { HarnessError } from '@chirality/runtime-contracts/errors';
import * as streamRoute from '../../../app/api/harness/session/[id]/turn/stream/route';
import * as stateRoute from '../../../app/api/harness/session/[id]/turn/state/route';
import * as requestsRoute from '../../../app/api/harness/session/[id]/requests/route';
import * as answerRoute from '../../../app/api/harness/session/[id]/requests/[requestId]/answer/route';
import { turnStreamResponse, TURN_STREAM_KEEPALIVE_MS } from '../../../lib/harness/http';
import { requireServerRequestAnswer } from '../../../lib/harness/server-request-answer';
import { createFakeDaemonHarnessPort } from './fake-daemon-harness-port';

/**
 * App routes over the Runtime turn registry (D-GOV-43 A2). The renderer only
 * observes: closing an attach stream unsubscribes and never interrupts, and
 * every frame carries the Runtime sequence as the SSE `id` so a renderer can
 * re-attach with `after=<seq>`.
 */

function port(overrides: Partial<DaemonHarnessPort>): DaemonHarnessPort {
  return { ...createFakeDaemonHarnessPort(), ...overrides };
}

const params = (id: string, requestId = '') => ({ params: Promise.resolve({ id, requestId }) });

afterEach(() => {
  resetDaemonHarnessPortForTests();
  vi.restoreAllMocks();
  vi.useRealTimers();
});

describe('session turn stream route', () => {
  it('replays frames with their sequence ids and unsubscribes on reader cancel without interrupting', async () => {
    let release: (() => void) | undefined;
    const cancel = vi.fn(async () => { release?.(); });
    const interrupt = vi.fn();
    const running: RunningDaemonHarnessTurn = {
      events: (async function* () {
        yield { type: 'harness:event', data: { type: 'message.delta', text: 'hi' }, seq: 7 } as unknown as DaemonTurnFrame;
        await new Promise<void>((resolve) => { release = resolve; });
      })(),
      cancel
    };
    const attachTurn = vi.fn(async () => running);
    installDaemonHarnessPort(port({ attachTurn, interrupt }));

    const response = await streamRoute.GET(
      new Request('http://localhost/api/harness/session/sess-1/turn/stream?after=6&turnId=turn-1'),
      params('sess-1')
    );
    expect(response.status).toBe(200);
    expect(response.headers.get('content-type')).toContain('text/event-stream');
    const reader = response.body!.getReader();
    expect(new TextDecoder().decode((await reader.read()).value)).toBe('event: transport:connected\ndata: {}\n\n');
    const first = await reader.read();
    expect(new TextDecoder().decode(first.value)).toBe('id: 7\nevent: harness:event\ndata: {"type":"message.delta","text":"hi"}\n\n');

    await reader.cancel();
    expect(cancel).toHaveBeenCalledOnce();
    expect(interrupt).not.toHaveBeenCalled();
    expect(attachTurn).toHaveBeenCalledWith('sess-1', 6, { signal: expect.any(AbortSignal), turnId: 'turn-1' });
  });

  it('defaults after to 0 and rejects a malformed value before touching the Runtime', async () => {
    const attachTurn = vi.fn(async () => ({ events: (async function* () {})(), cancel: vi.fn() }));
    installDaemonHarnessPort(port({ attachTurn }));

    const ok = await streamRoute.GET(new Request('http://localhost/api/harness/session/sess-1/turn/stream'), params('sess-1'));
    expect(ok.status).toBe(200);
    expect(attachTurn).toHaveBeenLastCalledWith('sess-1', 0, expect.anything());

    for (const bad of ['-1', 'abc', '1.5']) {
      const response = await streamRoute.GET(new Request(`http://localhost/api/harness/session/sess-1/turn/stream?after=${bad}`), params('sess-1'));
      expect(response.status).toBe(400);
    }
    expect(attachTurn).toHaveBeenCalledTimes(1);
  });

  it('answers 404 when the Runtime retains no turn for the session', async () => {
    installDaemonHarnessPort(port({
      attachTurn: async () => { throw new HarnessError('SESSION_NOT_FOUND', 404, 'No active or retained turn', { reason: 'TURN_NOT_ACTIVE' }); }
    }));
    const response = await streamRoute.GET(new Request('http://localhost/api/harness/session/sess-1/turn/stream?after=3'), params('sess-1'));
    expect(response.status).toBe(404);
    await expect(response.json()).resolves.toEqual(expect.objectContaining({ error: expect.objectContaining({ details: { reason: 'TURN_NOT_ACTIVE' } }) }));
  });
});

describe('session turn state and request routes', () => {
  it('proxies turn state and the pending request list read-only', async () => {
    const turnState = vi.fn(async () => ({ active: true, turnId: 'turn-9', lastSeq: 12, startedAt: '2026-09-12T00:00:00.000Z' }));
    const listRequests = vi.fn(async () => ({ requests: [{ requestId: 'req-1', method: 'item/tool/requestUserInput', kind: 'userInput' as const, request: { questions: [] }, receivedAt: '2026-09-12T00:00:01.000Z' }] })) as unknown as DaemonHarnessPort['listRequests'];
    installDaemonHarnessPort(port({ turnState, listRequests }));

    const state = await stateRoute.GET(new Request('http://localhost/api/harness/session/sess-1/turn/state'), params('sess-1'));
    expect(state.status).toBe(200);
    await expect(state.json()).resolves.toEqual({ active: true, turnId: 'turn-9', lastSeq: 12, startedAt: '2026-09-12T00:00:00.000Z' });
    expect(turnState).toHaveBeenCalledWith('sess-1', { signal: expect.any(AbortSignal) });

    const requests = await requestsRoute.GET(new Request('http://localhost/api/harness/session/sess-1/requests'), params('sess-1'));
    expect(requests.status).toBe(200);
    await expect(requests.json()).resolves.toEqual(expect.objectContaining({ requests: [expect.objectContaining({ requestId: 'req-1' })] }));
    expect(listRequests).toHaveBeenCalledWith('sess-1', { signal: expect.any(AbortSignal) });
  });

  it('validates the answer shape and forwards a well-formed answer verbatim', async () => {
    const answerRequest = vi.fn(async () => ({ accepted: true as const, requestId: 'req-1' })) as unknown as DaemonHarnessPort['answerRequest'];
    installDaemonHarnessPort(port({ answerRequest }));
    const post = (body: unknown) => answerRoute.POST(
      new Request('http://localhost/api/harness/session/sess-1/requests/req-1/answer', {
        method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body)
      }),
      params('sess-1', 'req-1')
    );

    for (const bad of [{}, { answer: 'yes' }, { answer: { kind: 'unknown' } }, { answer: { kind: 'approval', verdict: 'maybe' } },
      { answer: { kind: 'userInput', answers: { q1: { answers: [1] } } } }, { answer: { kind: 'elicitation', action: 'later' } }]) {
      const response = await post(bad);
      expect(response.status).toBe(400);
    }
    expect(answerRequest).not.toHaveBeenCalled();

    const answer = { kind: 'userInput', answers: { q1: { answers: ['blue'] } } };
    const response = await post({ answer });
    expect(response.status).toBe(200);
    await expect(response.json()).resolves.toEqual({ accepted: true, requestId: 'req-1' });
    expect(answerRequest).toHaveBeenCalledWith('sess-1', 'req-1', answer, { signal: expect.any(AbortSignal) });

    const elicitation = await post({ answer: { kind: 'elicitation', action: 'accept', content: { confirm: true } } });
    expect(elicitation.status).toBe(200);
    expect(answerRequest).toHaveBeenLastCalledWith('sess-1', 'req-1', { kind: 'elicitation', action: 'accept', content: { confirm: true } }, expect.anything());
  });

  it('requireServerRequestAnswer accepts every documented kind', () => {
    expect(requireServerRequestAnswer({ kind: 'approval', verdict: 'allowForSession' })).toEqual({ kind: 'approval', verdict: 'allowForSession' });
    expect(requireServerRequestAnswer({ kind: 'elicitation', action: 'decline' })).toEqual({ kind: 'elicitation', action: 'decline' });
    expect(() => requireServerRequestAnswer(null)).toThrow(HarnessError);
  });
});


it('proxy keepalives never replace upstream health or hide a failed Runtime subscription', async () => {
  vi.useFakeTimers();
  let fail!: (error: Error) => void;
  const cancel = vi.fn(async () => undefined);
  const response = turnStreamResponse({ events: (async function* () {
    await new Promise<void>((_resolve, reject) => { fail = reject; });
  })(), cancel });
  const reader = response.body!.getReader();
  const text = async () => new TextDecoder().decode((await reader.read()).value);
  expect(await text()).toContain('event: transport:connected');
  await vi.advanceTimersByTimeAsync(TURN_STREAM_KEEPALIVE_MS);
  expect(await text()).toBe(': keepalive\n\n');
  const pending = reader.read();
  const rejected = expect(pending).rejects.toThrow('Runtime byte deadline');
  fail(new Error('Runtime byte deadline'));
  await rejected;
  expect(vi.getTimerCount()).toBe(0);
  expect(cancel).not.toHaveBeenCalled();
});
