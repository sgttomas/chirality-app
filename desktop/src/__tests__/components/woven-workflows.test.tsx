import React from 'react';
import { act, create, type ReactTestRenderer } from 'react-test-renderer';
import { renderToStaticMarkup } from 'react-dom/server';
import { afterEach, expect, it, vi } from 'vitest';
import { WorkflowsView } from '../../components/woven-dialogue/workflows-view';
import { WorkflowDetail } from '../../components/woven-dialogue/workflow-detail';
const file = { name: 'review.md', path: '.chirality/workflows/review.md', size: 20, modifiedAt: '2026-09-06T00:00:00.000Z' };
const response = (body: unknown, ok = true) => ({ ok, json: async () => body });
afterEach(() => vi.unstubAllGlobals());
it('opens the real listed filename and preserves plain unvalidated disclosure', async () => {
  const fetch = vi.fn(async (_url: string) => response({ projectRoot: '/one', files: [file], directoryMissing: false })); vi.stubGlobal('fetch', fetch);
  const onOpen = vi.fn(); let tree!: ReactTestRenderer;
  await act(async () => { tree = create(<WorkflowsView projectRoot="/one" name={null} refresh={0} onOpen={onOpen} />); });
  expect(JSON.stringify(tree.toJSON())).toContain('Plan details cannot be checked yet');
  expect(tree.root.findByType('small').children.join('')).not.toContain('bytes');
  expect(tree.root.findByType('small').children.join('')).toBe(new Date(file.modifiedAt).toLocaleDateString());
  act(() => tree.root.findByType('button').props.onClick()); expect(onOpen).toHaveBeenCalledWith('review.md');
  expect(fetch.mock.calls[0][0]).toContain('projectRoot=%2Fone');
  act(() => tree.unmount());
});
it('discards stale folder results and aborts their requests', async () => {
  let resolve!: (value: unknown) => void; const first = new Promise(r => { resolve = r; });
  const fetch = vi.fn().mockReturnValueOnce(first).mockResolvedValue(response({ projectRoot: '/two', files: [], directoryMissing: true })); vi.stubGlobal('fetch', fetch);
  let tree!: ReactTestRenderer; await act(async () => { tree = create(<WorkflowsView projectRoot="/one" name="old.md" refresh={0} onOpen={() => {}} />); });
  await act(async () => tree.update(<WorkflowsView projectRoot="/two" name={null} refresh={0} onOpen={() => {}} />));
  await act(async () => resolve(response({ projectRoot: '/one', file, content: 'PRIVATE OLD CONTENT', sha256: 'a'.repeat(64) })));
  expect(JSON.stringify(tree.toJSON())).not.toContain('PRIVATE OLD CONTENT'); expect(fetch.mock.calls[0][1].signal.aborted).toBe(true);
  act(() => tree.unmount());
});
it('shows errors and retries after refresh without implying an empty list', async () => {
  vi.stubGlobal('fetch', vi.fn().mockResolvedValueOnce(response({ error: { message: 'Folder changed. Refresh.' } }, false)).mockResolvedValue(response({ projectRoot: '/one', files: [file], directoryMissing: false })));
  let tree!: ReactTestRenderer; await act(async () => { tree = create(<WorkflowsView projectRoot="/one" name={null} refresh={0} onOpen={() => {}} />); });
  expect(tree.root.findByProps({ role: 'alert' }).children.join('')).toContain('Refresh');
  await act(async () => tree.update(<WorkflowsView projectRoot="/one" name={null} refresh={1} onOpen={() => {}} />));
  expect(tree.root.findAllByProps({ role: 'alert' })).toHaveLength(0); act(() => tree.unmount());
});
it('renders readable Markdown with no executable HTML, links or image requests', () => {
  const html = renderToStaticMarkup(<WorkflowDetail preview={{ projectRoot: '/one', file, sha256: 'a'.repeat(64), content: '# Review\n\n1. Gather sources\n2. [gate] Human review\n\n<script>alert(1)</script>\n\n[link](https://external.test) ![image](https://external.test/a.png)' }} />);
  expect(html).toContain('<h1>Review</h1>'); expect(html).toContain('<ol>'); expect(html).not.toContain('<script'); expect(html).not.toContain('href='); expect(html).not.toContain('<img'); expect(html).toContain('[gate]'); expect(html).toContain(file.path);
});
