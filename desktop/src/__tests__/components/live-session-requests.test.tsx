import React from 'react';
import { act, create, type ReactTestRenderer } from 'react-test-renderer';
import { beforeEach, afterEach, it, expect, vi } from 'vitest';
const api = vi.hoisted(() => ({ list: vi.fn(), answer: vi.fn(), events: [] as unknown[] }));
vi.mock('../../lib/harness/client', () => ({ listHarnessSessionRequests: api.list, answerHarnessSessionRequest: api.answer }));
vi.mock('../../components/workspace/harness-events-provider', () => ({ useHarnessEvents: () => ({ events: api.events }) }));
import { ChatAttentionDialog, useChatAttention } from '../../components/woven-dialogue/chat-attention';
import { LiveSessionRequests } from '../../components/shell/request-card';
const pending = { requestId: 'same', method: 'item/tool/requestUserInput', params: { questions: [{ id: 'q', question: 'Which?', header: 'Choice', options: [{ label: 'One', description: 'Small example' }] }] }, receivedAt: '2026-09-12T00:00:00Z' };
let tree: ReactTestRenderer;
beforeEach(() => { vi.useFakeTimers(); api.events = []; api.list.mockReset(); api.answer.mockReset(); api.answer.mockResolvedValue({ sent: true }); vi.stubGlobal('window', { setInterval, clearInterval, addEventListener() {}, removeEventListener() {} }); });
afterEach(() => { if (tree) act(() => tree.unmount()); vi.useRealTimers(); vi.unstubAllGlobals(); });
it('requires live pending evidence and revalidates after the user finishes a draft', async () => {
  api.list.mockResolvedValueOnce({ requests: [pending] }).mockResolvedValue({ requests: [] });
  await act(async () => { tree = create(<LiveSessionRequests sessionId="s1" />); });
  expect(JSON.stringify(tree.toJSON())).toContain('Small example');
  await act(async () => tree.root.findByProps({ type: 'radio' }).props.onChange());
  await act(async () => tree.root.findByType('form').props.onSubmit({ preventDefault() {} }));
  expect(api.answer).not.toHaveBeenCalled();
  expect(JSON.stringify(tree.toJSON())).toContain('no longer pending');
});
it('answers the owner session even with reused request ids and never enables a historic pending event', async () => {
  api.events = [{ eventId: 'old', sessionId: 's1', type: 'codex.request', data: { requestId: 'same', method: pending.method, request: pending.params } }];
  api.list.mockResolvedValue({ requests: [] });
  await act(async () => { tree = create(<LiveSessionRequests sessionId="s1" />); });
  expect(tree.root.findAllByType('form')).toHaveLength(0);
  api.list.mockResolvedValue({ requests: [pending] });
  await act(async () => tree.update(<LiveSessionRequests sessionId="s2" />));
  await act(async () => tree.root.findByProps({ type: 'radio' }).props.onChange());
  await act(async () => tree.root.findByType('form').props.onSubmit({ preventDefault() {} }));
  expect(api.answer).toHaveBeenCalledWith({ sessionId: 's2', requestId: 'same', answer: { kind: 'userInput', answers: { q: { answers: ['One'] } } } });
  api.list.mockResolvedValue({ requests: [] });
  await act(async () => { await vi.advanceTimersByTimeAsync(2000); });
  expect(tree.root.findAllByType('form')).toHaveLength(0);
});
it('shares one pending poll across badge and inline subscribers', async () => {
  api.list.mockResolvedValue({ requests: [pending] });
  await act(async () => { tree = create(<><LiveSessionRequests sessionId="shared" /><LiveSessionRequests sessionId="shared" showHistory={false} /></>); });
  expect(api.list).toHaveBeenCalledTimes(1);
  await act(async () => { await vi.advanceTimersByTimeAsync(2000); });
  expect(api.list).toHaveBeenCalledTimes(2);
});
it('keeps a late answer failure with its owning session', async () => {
  let reject!: (error: Error) => void;
  api.list.mockResolvedValue({ requests: [pending] });
  api.answer.mockImplementation(() => new Promise((_resolve, failure) => { reject = failure; }));
  await act(async () => { tree = create(<LiveSessionRequests sessionId="old" />); });
  await act(async () => tree.root.findByProps({ type: 'radio' }).props.onChange());
  await act(async () => tree.root.findByType('form').props.onSubmit({ preventDefault() {} }));
  await act(async () => tree.update(<LiveSessionRequests sessionId="new" />));
  await act(async () => reject(new Error('Old session failure')));
  expect(JSON.stringify(tree.toJSON())).not.toContain('Old session failure');
});

function AttentionFixture() {
  const attention = useChatAttention(['legacy-owner']);
  return <>{attention.observers}<ChatAttentionDialog sessionId="legacy-owner" title="Background chat" rows={attention.rows['legacy-owner'] ?? []} onClose={() => {}} /></>;
}
it.each(['execCommandApproval', 'applyPatchApproval'].flatMap(method => ['inline', 'attention'].map(surface => ({ method, surface }))))('renders one actionable legacy $method card in $surface and removes it after resolution', async ({ method, surface }) => {
  vi.stubGlobal('HTMLElement', class {});
  vi.stubGlobal('document', { activeElement: null });
  api.list.mockResolvedValue({ requests: [{ ...pending, method, params: { command: 'Inspect workspace', reason: 'Approval required' } }] });
  api.answer.mockImplementation(async () => { api.list.mockResolvedValue({ requests: [] }); return { sent: true }; });
  await act(async () => { tree = create(surface === 'inline' ? <LiveSessionRequests sessionId="legacy-owner" /> : <AttentionFixture />); });
  const approve = tree.root.findAllByType('button').filter(button => button.children.join('') === 'Approve');
  expect(approve).toHaveLength(1);
  await act(async () => approve[0].props.onClick());
  expect(api.answer).toHaveBeenCalledWith({ sessionId: 'legacy-owner', requestId: 'same', answer: { kind: 'approval', verdict: 'allow' } });
  await act(async () => { await vi.advanceTimersByTimeAsync(2000); });
  expect(tree.root.findAllByType('button').filter(button => ['Approve', 'Deny'].includes(button.children.join('')))).toHaveLength(0);
});
