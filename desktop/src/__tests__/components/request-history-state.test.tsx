import React from 'react';
import { act, create, type ReactTestRenderer } from 'react-test-renderer';
import { afterEach, expect, it, vi } from 'vitest';
import type { HarnessEvent } from '@chirality/runtime-contracts/event-schema';
import { LiveSessionRequests } from '../../components/shell/request-card';
const state = vi.hoisted(() => ({ events: [] as HarnessEvent[] }));
vi.mock('../../components/workspace/harness-events-provider', () => ({ useHarnessEvents: () => state }));
let tree: ReactTestRenderer | undefined;
afterEach(() => { if (tree) act(() => tree!.unmount()); tree = undefined; });
const event = (id: string, type: string, data: unknown) => ({ eventId: id, sessionId: 's1', type, timestamp: '2026-09-12T00:00:00Z', data } as HarnessEvent);
it('labels answered input as history through next turns and restored sessions without asking again', async () => {
  const history = [event('request', 'codex.request', { requestId: 'q1', method: 'item/tool/requestUserInput', request: { questions: [{ id: 'q', question: 'Which colour?', header: 'Colour' }] } }),
    event('answer', 'codex.request.resolved', { requestId: 'q1', outcome: 'answered', decision: { answers: { q: { answers: ['Blue'] } } } })];
  state.events = history;
  await act(async () => { tree = create(<LiveSessionRequests sessionId="s1" active={false} />); });
  const check = () => { const text = JSON.stringify(tree!.toJSON()); expect(text).toContain('Codex input request'); expect(text).toContain('answered'); expect(text).toContain('Blue'); expect(text).not.toContain('needs your input'); };
  check(); state.events = [];
  await act(async () => tree!.update(<LiveSessionRequests sessionId="s1" active={false} />)); check();
  await act(async () => tree!.update(<LiveSessionRequests sessionId="s2" active={false} />)); expect(JSON.stringify(tree!.toJSON())).not.toContain('Blue');
  state.events = history;
  await act(async () => tree!.update(<LiveSessionRequests sessionId="s1" active={false} />)); check();
});
