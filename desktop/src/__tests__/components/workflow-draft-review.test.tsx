import React from 'react';
import { act, create, type ReactTestRenderer } from 'react-test-renderer';
import { afterEach, beforeEach, expect, it, vi } from 'vitest';
const mocks = vi.hoisted(() => ({ list: vi.fn(), register: vi.fn() }));
vi.mock('../../lib/harness/workflow-drafts', () => ({ listWorkflowDrafts: mocks.list, registerWorkflowDraft: mocks.register }));
vi.mock('../../components/shell/runtime-connectivity-provider', () => ({ useRuntimeEpoch: () => 0 }));
vi.mock('../../components/shell/chat-markdown', () => ({ ChatMarkdown: ({ source }: {source: string}) => <pre>{source}</pre> }));
import { WorkflowDraftReview } from '../../components/woven-dialogue/workflow-draft-review';
const draft = { name: 'meeting-review', source: 'project' as const, content: '# Proposed method\nReview the evidence.', description: 'Review meeting evidence', reviewToken: 'a'.repeat(64), files: [{ path: 'WORKFLOW.md', size: 46, sha256: 'a'.repeat(64) }], destinationExists: false };
let tree: ReactTestRenderer;
const registered = vi.fn(); const feedback = vi.fn();
const props = { projectRoot: '/project', refresh: 0, onRegistered: registered, onFeedback: feedback };
const button = (label: string) => tree.root.findAllByType('button').find(item => item.children.includes(label))!;
async function mount() { await act(async () => { tree = create(<WorkflowDraftReview {...props} />); }); }
beforeEach(() => { vi.resetAllMocks(); mocks.list.mockResolvedValue({ drafts: [draft] }); mocks.register.mockResolvedValue({ name: draft.name, source: 'project', path: '.chirality/workflows/meeting-review/WORKFLOW.md' }); });
afterEach(() => { if (tree) act(() => tree.unmount()); });
it('requires visible review before registration and sends the exact review token', async () => {
  await mount(); expect(button('Register workflow')).toBeUndefined();
  await act(async () => button('Review draft').props.onClick());
  expect(JSON.stringify(tree.toJSON())).toContain('Review the evidence.');
  await act(async () => button('Register workflow').props.onClick());
  expect(mocks.register).toHaveBeenCalledWith({ projectRoot: '/project', name: draft.name, source: 'project', reviewToken: draft.reviewToken });
  expect(registered).toHaveBeenCalledOnce();
  expect(JSON.stringify(tree.toJSON())).toContain('meeting-review registered.');
});
it('prepares feedback in chat without registering or losing the draft', async () => {
  await mount(); await act(async () => button('Review draft').props.onClick());
  await act(async () => button('Request changes in chat').props.onClick());
  expect(feedback).toHaveBeenCalledWith({ projectRoot: '/project', name: draft.name, source: 'project' });
  expect(mocks.register).not.toHaveBeenCalled();
  expect(JSON.stringify(tree.toJSON())).toContain('Review the evidence.');
});
it('requires inspecting changed draft bytes again after background refresh', async () => {
  await mount(); await act(async () => button('Review draft').props.onClick());
  const updated = { ...draft, content: '# Revised method', reviewToken: 'b'.repeat(64) };
  mocks.list.mockResolvedValue({ drafts: [updated] });
  await act(async () => tree.update(<WorkflowDraftReview {...props} refresh={1} />));
  expect(button('Register workflow').props.disabled).toBe(true);
  expect(JSON.stringify(tree.toJSON())).toContain('Review the evidence.');
  await act(async () => button('Review latest draft').props.onClick());
  expect(JSON.stringify(tree.toJSON())).toContain('# Revised method');
  await act(async () => button('Register workflow').props.onClick());
  expect(mocks.register.mock.calls[0][0].reviewToken).toBe(updated.reviewToken);
});
it('keeps failed registration reviewable and preserves a conflicting existing name', async () => {
  mocks.register.mockRejectedValue(new Error('Draft changed since review'));
  await mount(); await act(async () => button('Review draft').props.onClick());
  await act(async () => button('Register workflow').props.onClick());
  expect(tree.root.findByProps({ role: 'alert' }).children.join('')).toContain('Draft changed');
  expect(registered).not.toHaveBeenCalled();
  mocks.list.mockResolvedValue({ drafts: [{ ...draft, destinationExists: true }] });
  await act(async () => tree.update(<WorkflowDraftReview {...props} refresh={1} />));
  await act(async () => button('‹ Drafts').props.onClick());
  await act(async () => button('Review draft').props.onClick());
  expect(button('Register workflow').props.disabled).toBe(true);
});
it('does not show already registered identical drafts as awaiting review', async () => {
  mocks.list.mockResolvedValue({ drafts: [{ ...draft, destinationExists: true, registered: true }] });
  await mount(); expect(tree.toJSON()).toBeNull();
});
it('does not apply a late registration return to another project', async () => {
  let resolve!: (value: unknown) => void;
  mocks.register.mockImplementation(() => new Promise(done => { resolve = done; }));
  await mount(); await act(async () => button('Review draft').props.onClick());
  await act(async () => { void button('Register workflow').props.onClick(); });
  mocks.list.mockResolvedValue({ drafts: [] });
  await act(async () => tree.update(<WorkflowDraftReview {...props} projectRoot="/other" />));
  await act(async () => resolve({ name: draft.name }));
  expect(registered).not.toHaveBeenCalled(); expect(tree.toJSON()).toBeNull();
});
