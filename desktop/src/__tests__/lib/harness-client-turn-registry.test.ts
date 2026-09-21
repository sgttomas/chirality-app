import { afterEach, describe, expect, it, vi } from 'vitest';
import {
  answerHarnessSessionRequest,
  attachHarnessTurn,
  getHarnessTurnState,
  listHarnessSessionRequests,
  parseSseFrame,
  streamHarnessTurn
} from '../../lib/harness/client';

afterEach(() => {
  vi.unstubAllGlobals();
});

function sse(body: string, status = 200): Response {
  return new Response(body, { status, headers: { 'Content-Type': 'text/event-stream' } });
}

describe('parseSseFrame', () => {
  it('reads the Runtime sequence from the id line and tolerates CRLF and comment lines', () => {
    expect(parseSseFrame('id: 12\nevent: harness:event\ndata: {"type":"message.delta","text":"a"}')).toEqual({
      event: 'harness:event', data: { type: 'message.delta', text: 'a' }, seq: 12
    });
    expect(parseSseFrame('id: 3\r\nevent: chat:delta\r\ndata: {"text":"b"}\r\n')).toEqual({ event: 'chat:delta', data: { text: 'b' }, seq: 3 });
    expect(parseSseFrame(': keepalive')).toBeNull();
    expect(parseSseFrame('id: x\nevent: chat:delta\ndata: {"text":"no seq"}')).toEqual({ event: 'chat:delta', data: { text: 'no seq' } });
  });
});

describe('turn registry client', () => {
  it('attaches with after=<seq> through GET and delivers every frame with its sequence', async () => {
    const fetchMock = vi.fn().mockResolvedValue(sse(
      'id: 5\nevent: harness:event\ndata: {"type":"message.delta","text":"hello"}\n\n: keepalive\n\nid: 6\nevent: harness:event\ndata: {"type":"turn.completed"}\n\n'
    ));
    vi.stubGlobal('fetch', fetchMock);
    const received: unknown[] = [];
    const controller = new AbortController();
    await attachHarnessTurn('sess/1', 4, (event) => received.push(event), controller.signal, 'turn/1');
    expect(fetchMock).toHaveBeenCalledWith('/api/harness/session/sess%2F1/turn/stream?after=4&turnId=turn%2F1', expect.objectContaining({ method: 'GET', signal: controller.signal }));
    expect(received).toEqual([
      { event: 'harness:event', data: { type: 'message.delta', text: 'hello' }, seq: 5 },
      { event: 'harness:event', data: { type: 'turn.completed' }, seq: 6 }
    ]);
  });

  it('sends the per-turn model pair with the turn request and forwards the signal', async () => {
    const fetchMock = vi.fn().mockResolvedValue(sse('event: chat:complete\ndata: {"text":"done"}\n\n'));
    vi.stubGlobal('fetch', fetchMock);
    const controller = new AbortController();
    await streamHarnessTurn({ sessionId: 's1', message: 'hi', turnId: 'submitted-turn', model: 'gpt-alt', reasoningEffort: 'low' }, () => undefined, controller.signal);
    expect(fetchMock.mock.calls[0][0]).toBe('/api/harness/turn');
    expect(JSON.parse(fetchMock.mock.calls[0][1].body)).toEqual({ sessionId: 's1', message: 'hi', turnId: 'submitted-turn', model: 'gpt-alt', reasoningEffort: 'low' });
    expect(fetchMock.mock.calls[0][1].signal).toBe(controller.signal);
  });

  it('surfaces the TURN_NOT_ACTIVE reason from a 404 attach as a typed client error', async () => {
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue(new Response(JSON.stringify({ error: { type: 'SESSION_NOT_FOUND', message: 'No active turn', details: { reason: 'TURN_NOT_ACTIVE' } } }), { status: 404, headers: { 'Content-Type': 'application/json' } })));
    await expect(attachHarnessTurn('s1', 0, () => undefined)).rejects.toMatchObject({ status: 404, details: { reason: 'TURN_NOT_ACTIVE' } });
  });

  it('reads turn state and requests, and posts an answer under the requestId path', async () => {
    const fetchMock = vi.fn()
      .mockResolvedValueOnce(new Response(JSON.stringify({ active: true, turnId: 't1', lastSeq: 9 }), { status: 200 }))
      .mockResolvedValueOnce(new Response(JSON.stringify({ requests: [] }), { status: 200 }))
      .mockResolvedValueOnce(new Response(JSON.stringify({ accepted: true, requestId: 'req-1' }), { status: 200 }));
    vi.stubGlobal('fetch', fetchMock);

    await expect(getHarnessTurnState('s1')).resolves.toEqual({ active: true, turnId: 't1', lastSeq: 9 });
    await expect(listHarnessSessionRequests('s1')).resolves.toEqual({ requests: [] });
    const answer = { kind: 'elicitation' as const, action: 'accept' as const };
    await answerHarnessSessionRequest({ sessionId: 's1', requestId: 'req 1', answer });
    expect(fetchMock.mock.calls.map((call) => call[0])).toEqual([
      '/api/harness/session/s1/turn/state',
      '/api/harness/session/s1/requests',
      '/api/harness/session/s1/requests/req%201/answer'
    ]);
    expect(fetchMock.mock.calls[2][1]).toEqual(expect.objectContaining({ method: 'POST' }));
    expect(JSON.parse(fetchMock.mock.calls[2][1].body)).toEqual({ answer });
  });
});
