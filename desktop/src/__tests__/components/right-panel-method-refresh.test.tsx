import React from 'react';
import { act, create, type ReactTestRenderer } from 'react-test-renderer';
import { afterEach, expect, it, vi } from 'vitest';
import { createDefaultWovenWorkspaceState } from '../../lib/woven-dialogue/woven-workspace-state';

const mocks = vi.hoisted(() => ({ list: vi.fn() }));
vi.mock('../../lib/harness/method-selection-client', async importOriginal => ({
  ...await importOriginal<typeof import('../../lib/harness/method-selection-client')>(),
  listMethods: mocks.list
}));
vi.mock('../../components/workspace/workspace-provider', () => ({
  useWorkspace: () => ({ projectRoot: '/project' })
}));
vi.mock('../../components/woven-dialogue/activity-shelf', () => ({ ActivityView: () => null }));
vi.mock('../../components/shell/file-tree-panel', () => ({ FileTreePanel: () => null }));

import { RightPanel } from '../../components/woven-dialogue/right-panel';

afterEach(() => { vi.clearAllMocks(); vi.unstubAllGlobals(); });

it('retries an unavailable method catalog through the panel Refresh action', async () => {
  mocks.list.mockRejectedValueOnce(new Error('Daemon was unavailable')).mockResolvedValue({
    schemaVersion: 'chirality.methods/v3', methods: [], malformedPackages: []
  });
  let tree!: ReactTestRenderer;
  await act(async () => {
    tree = create(<RightPanel
      state={{ ...createDefaultWovenWorkspaceState(), rightPanelView: 'workflows' }}
      sessionOpen={false}
      onView={() => {}}
      onOpenFile={() => {}}
      onClose={() => {}}
      onExpand={() => {}}
      coordination={null}
    />);
  });
  await act(async () => { await new Promise(resolve => setTimeout(resolve, 0)); });
  expect(JSON.stringify(tree.toJSON())).toContain('Daemon was unavailable');
  expect(JSON.stringify(tree.toJSON())).toContain('Workflows');
  const refresh = tree.root.findAllByType('button').find(node => node.children.includes('Refresh'))!;
  await act(async () => refresh.props.onClick());
  await act(async () => { await new Promise(resolve => setTimeout(resolve, 0)); });
  expect(mocks.list).toHaveBeenCalledTimes(2);
  act(() => tree.unmount());
});

it('discovers workflows after a turn ends without reopening or flashing existing cards', async () => {
  const method = (name: string) => ({ qualifiedId: `project/workflow/${name}`, sourceRootId: 'project', source: 'project', kind: 'workflow', name, description: name, central: false, compatibility: 'canonical', executionRoleIds: ['TASK'], resources: [] });
  const existing = method('existing-workflow');
  let finish!: (value: unknown) => void;
  mocks.list.mockResolvedValueOnce({ methods: [existing], malformedPackages: [] })
    .mockImplementationOnce(() => new Promise(resolve => { finish = resolve; }));
  const selected = [{ kind: 'workflow' as const, source: 'project' as const, sourceRootId: 'project', name: existing.name }];
  const onSelectedMethodsChange = vi.fn();
  const props = { state: { ...createDefaultWovenWorkspaceState(), rightPanelView: 'workflows' as const }, sessionOpen: false,
    onView: vi.fn(), onOpenFile: vi.fn(), onClose: vi.fn(), onExpand: vi.fn(), coordination: null, selectedMethods: selected, onSelectedMethodsChange };
  let tree!: ReactTestRenderer;
  await act(async () => { tree = create(<RightPanel {...props} liveTurnActive={false} />); });
  await act(async () => { await new Promise(resolve => setTimeout(resolve, 0)); });
  await act(async () => { tree.update(<RightPanel {...props} liveTurnActive />); });
  expect(mocks.list).toHaveBeenCalledTimes(1);
  await act(async () => { tree.update(<RightPanel {...props} liveTurnActive={false} />); });
  await act(async () => { await new Promise(resolve => setTimeout(resolve, 0)); });
  expect(mocks.list).toHaveBeenCalledTimes(2);
  expect(JSON.stringify(tree.toJSON())).toContain('existing-workflow');
  expect(JSON.stringify(tree.toJSON())).not.toContain('Loading…');
  expect(tree.root.findAllByProps({ 'aria-pressed': true }).some(node => node.children.includes('Remove'))).toBe(true);
  await act(async () => finish({ methods: [existing, method('new-workflow')], malformedPackages: [{ name: 'invalid-workflow' }] }));
  expect(JSON.stringify(tree.toJSON())).toContain('new-workflow');
  expect(JSON.stringify(tree.toJSON())).not.toContain('invalid-workflow');
  expect(onSelectedMethodsChange).not.toHaveBeenCalled();
  await act(async () => { tree.update(<RightPanel {...props} liveTurnActive={false} />); });
  expect(mocks.list).toHaveBeenCalledTimes(2);
  act(() => tree.unmount());
});

it('reloads an already open action brief after completed work changes the same file', async () => {
  let content = '# Action brief\n\n| Action | Owner |\n| --- | --- |\n| Book venue | Unassigned |';
  const fetcher = vi.fn(async () => ({ ok: true, json: async () => ({ name: 'action-brief.md', target: 'action-brief.md', kind: 'text', size: content.length, modifiedAt: 'today', content }) }));
  vi.stubGlobal('fetch', fetcher);
  const props = { state: { ...createDefaultWovenWorkspaceState(), rightPanelView: 'files' as const, openDocumentPath: 'action-brief.md' }, sessionOpen: false,
    onView: vi.fn(), onOpenFile: vi.fn(), onClose: vi.fn(), onExpand: vi.fn(), coordination: null };
  let tree!: ReactTestRenderer;
  await act(async () => { tree = create(<RightPanel {...props} liveTurnActive={false} />); });
  expect(JSON.stringify(tree.toJSON())).toContain('Unassigned');
  expect(fetcher).toHaveBeenCalledTimes(1);
  await act(async () => { tree.update(<RightPanel {...props} liveTurnActive />); });
  content = content.replace('Unassigned', 'Morgan');
  // Updating the same open target during work must not poll or disrupt reading.
  await act(async () => { tree.update(<RightPanel {...props} liveTurnActive />); });
  expect(fetcher).toHaveBeenCalledTimes(1);
  await act(async () => { tree.update(<RightPanel {...props} liveTurnActive={false} />); });
  expect(fetcher).toHaveBeenCalledTimes(2);
  expect(fetcher).toHaveBeenLastCalledWith('/api/working-root/file?projectRoot=%2Fproject&target=action-brief.md');
  expect(JSON.stringify(tree.toJSON())).toContain('Morgan');
  expect(JSON.stringify(tree.toJSON())).not.toContain('Unassigned');
  await act(async () => { tree.update(<RightPanel {...props} liveTurnActive={false} />); });
  expect(fetcher).toHaveBeenCalledTimes(2);
  act(() => tree.unmount());
});
