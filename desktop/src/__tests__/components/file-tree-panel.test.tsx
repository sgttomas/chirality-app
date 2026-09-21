import React from 'react';
import { renderToStaticMarkup } from 'react-dom/server';
import { act, create, type ReactTestRenderer, type ReactTestRendererJSON } from 'react-test-renderer';
import { afterEach, expect, it, vi } from 'vitest';
import { FileTreePanel } from '../../components/shell/file-tree-panel';
const workspace = vi.hoisted(() => ({ projectRoot: '/root' as string | null, chooseProjectRoot: vi.fn(async () => true), hasElectronDirectoryPicker: true, errorMessage: null }));
vi.mock('../../components/workspace/workspace-provider', () => ({ useWorkspace: () => workspace }));
afterEach(() => { vi.unstubAllGlobals(); workspace.projectRoot = '/root'; workspace.hasElectronDirectoryPicker = true; workspace.chooseProjectRoot.mockClear(); });
function deferred<T>() { let resolve!: (value: T) => void; const promise = new Promise<T>(done => { resolve = done; }); return { promise, resolve }; }
it('opens regular files, toggles directories and preserves inert legacy files', async () => {
  vi.stubGlobal('window', { setInterval: vi.fn(), clearInterval: vi.fn(), addEventListener: vi.fn(), removeEventListener: vi.fn() });
  vi.stubGlobal('document', { addEventListener: vi.fn(), removeEventListener: vi.fn() });
  vi.stubGlobal('fetch', vi.fn(async () => ({ ok: true, json: async () => ({ root: { name: 'root', path: '/root', kind: 'directory', children: [{ name: 'spec.md', path: '/root/spec.md', kind: 'file' }] } }) })));
  const onOpenFile = vi.fn(); let tree!: ReactTestRenderer;
  await act(async () => { tree = create(<FileTreePanel onOpenFile={onOpenFile} selectedPath="/root/spec.md" />); });
  const file = tree.root.findAllByType('button').find(x => x.children.includes('spec.md'))!;
  expect(file.props['aria-current']).toBe('true'); act(() => file.props.onClick()); expect(onOpenFile).toHaveBeenCalledWith('/root/spec.md');
  act(() => tree.root.findAllByType('button').find(x => x.children.includes('root'))!.props.onClick());
  expect(tree.root.findAllByType('button').some(x => x.children.includes('spec.md'))).toBe(false);
  act(() => tree.unmount());
  await act(async () => { tree = create(<FileTreePanel />); });
  expect(tree.root.findAllByType('button').some(x => x.children.includes('spec.md'))).toBe(false);
  expect(tree.root.findAllByType('span').some(x => x.children.includes('spec.md'))).toBe(true); act(() => tree.unmount());
});

it('uses the existing folder chooser and supports arrow focus movement between real file buttons', async () => {
  workspace.projectRoot = '/root'; workspace.chooseProjectRoot.mockClear();
  vi.stubGlobal('window', { setInterval: vi.fn(), clearInterval: vi.fn(), addEventListener: vi.fn(), removeEventListener: vi.fn() });
  vi.stubGlobal('document', { addEventListener: vi.fn(), removeEventListener: vi.fn() });
  vi.stubGlobal('fetch', vi.fn(async () => ({ ok: true, json: async () => ({ root: { name: 'root', path: '/root', kind: 'directory', children: [{ name: 'a.txt', path: '/root/a.txt', kind: 'file' }] } }) })));
  let tree!: ReactTestRenderer; await act(async () => { tree = create(<FileTreePanel onOpenFile={vi.fn()} />); });
  await act(async () => tree.root.findAllByType('button').find(x => x.children.includes('Choose folder'))!.props.onClick()); expect(workspace.chooseProjectRoot).toHaveBeenCalledOnce();
  const first = { focus: vi.fn() }, second = { focus: vi.fn() };
  act(() => tree.root.findByProps({ className: 'panel-body' }).props.onKeyDown({ key: 'ArrowDown', target: first, currentTarget: { querySelectorAll: () => [first, second] }, preventDefault: vi.fn() }));
  expect(second.focus).toHaveBeenCalledOnce();
  workspace.projectRoot = null; await act(async () => tree.update(<FileTreePanel onOpenFile={vi.fn()} />));
  expect(tree.root.findAllByType('p').some(x => x.children.includes('Choose a folder to see its files.'))).toBe(true); act(() => tree.unmount()); workspace.projectRoot = '/root';
});


it('keeps the populated file list independent of folder controls across collapse and selection', async () => {
  workspace.projectRoot = '/root'; workspace.chooseProjectRoot.mockClear();
  vi.stubGlobal('window', { setInterval: vi.fn(), clearInterval: vi.fn(), addEventListener: vi.fn(), removeEventListener: vi.fn() });
  vi.stubGlobal('document', { addEventListener: vi.fn(), removeEventListener: vi.fn() });
  vi.stubGlobal('fetch', vi.fn(async () => ({ ok: true, json: async () => ({ root: { name: 'root', path: '/root', kind: 'directory', children: Array.from({ length: 40 }, (_, i) => ({ name: `file-${i}.txt`, path: `/root/file-${i}.txt`, kind: 'file' })) } }) })));
  const open = vi.fn(); let tree!: ReactTestRenderer;
  await act(async () => { tree = create(<FileTreePanel onOpenFile={open} />); });
  const footer = tree.root.findByType('footer');
  const body = tree.root.findByProps({ className: 'panel-body' });
  const folder = () => body.findAllByType('button').find(x => x.children.includes('root'))!;
  expect(body.findAllByType('button').filter(x => x.props.title?.includes('/root/file-'))).toHaveLength(40);
  act(() => folder().props.onClick());
  expect(body.findAllByType('button').some(x => x.children.includes('file-39.txt'))).toBe(false);
  await act(async () => footer.findByType('button').props.onClick());
  expect(workspace.chooseProjectRoot).toHaveBeenCalledOnce(); expect(open).not.toHaveBeenCalled();
  act(() => folder().props.onClick());
  act(() => body.findAllByType('button').find(x => x.children.includes('file-39.txt'))!.props.onClick());
  expect(open).toHaveBeenCalledExactlyOnceWith('/root/file-39.txt');
  expect(tree.root.findByType('footer')).toBe(footer);
  expect(footer.findByType('span').props.title).toBe('/root');
  act(() => tree.unmount());
});


it('matches SSR and the native first client commit before enabling the mounted folder chooser', async () => {
  workspace.projectRoot = null;
  workspace.hasElectronDirectoryPicker = false;
  const serverMarkup = renderToStaticMarkup(<FileTreePanel />);
  expect(serverMarkup).toContain('disabled=""');
  expect(serverMarkup).toContain('Choose a folder using the folder selector above.');

  workspace.hasElectronDirectoryPicker = true;
  // Deliberately create outside act: capture the synchronous first commit before passive effects.
  const tree = create(<FileTreePanel />);
  const initialClientTree = tree.toJSON();
  const toElement = (node: ReactTestRendererJSON | string): React.ReactNode => typeof node === 'string'
    ? node : React.createElement(node.type, node.props, ...(node.children ?? []).map(toElement));
  expect(Array.isArray(initialClientTree)).toBe(false);
  expect(renderToStaticMarkup(toElement(initialClientTree as ReactTestRendererJSON))).toBe(serverMarkup);
  const chooseButton = () => tree.root.findByType('footer').findByType('button');
  expect(chooseButton().props.disabled).toBe(true);

  await act(async () => {});
  expect(chooseButton().props.disabled).toBe(false);
  expect(tree.root.findAllByType('p').some(node => node.children.includes('Choose a folder using the folder selector above.'))).toBe(false);
  workspace.chooseProjectRoot.mockClear();
  await act(async () => chooseButton().props.onClick());
  expect(workspace.chooseProjectRoot).toHaveBeenCalledOnce();
  act(() => tree.unmount());
  // This checks server/initial-client structure and postmount behavior; production hydration is a separate proof.
});

it('retains the folder selector fallback after mounting in a browser without the native picker', async () => {
  workspace.projectRoot = null;
  workspace.hasElectronDirectoryPicker = false;
  let tree!: ReactTestRenderer;
  await act(async () => { tree = create(<FileTreePanel />); });
  expect(tree.root.findByType('footer').findByType('button').props.disabled).toBe(true);
  expect(tree.root.findAllByType('p').some(node => node.children.includes('Choose a folder using the folder selector above.'))).toBe(true);
  expect(workspace.chooseProjectRoot).not.toHaveBeenCalled();
  act(() => tree.unmount());
});

it('publishes a sorted file-only catalog from the tree response and clears it on error', async () => {
  let poll!: () => void;
  vi.stubGlobal('window', { setInterval: vi.fn((callback: () => void) => { poll = callback; return 1; }), clearInterval: vi.fn(), addEventListener: vi.fn(), removeEventListener: vi.fn() });
  vi.stubGlobal('document', { visibilityState: 'visible', addEventListener: vi.fn(), removeEventListener: vi.fn() });
  const fetch = vi.fn()
    .mockResolvedValueOnce({ ok: true, json: async () => ({ root: { name: 'root', path: '/root', kind: 'directory', children: [
      { name: 'dir', path: '/root/dir', kind: 'directory', children: [{ name: 'z.md', path: '/root/dir/z.md', kind: 'file' }] },
      { name: 'link', path: '/root/link', kind: 'symlink' },
      { name: 'a.md', path: '/root/a.md', kind: 'file' }
    ] } }) })
    .mockResolvedValueOnce({ ok: false, json: async () => ({ error: { message: 'tree failed' } }) });
  vi.stubGlobal('fetch', fetch);
  const catalog = vi.fn(); let tree!: ReactTestRenderer;
  await act(async () => { tree = create(<FileTreePanel onFileCatalog={catalog} />); });
  expect(fetch).toHaveBeenCalledTimes(1);
  expect(catalog).toHaveBeenLastCalledWith({ root: '/root', paths: ['/root/a.md', '/root/dir/z.md'] });
  await act(async () => { poll(); });
  expect(fetch).toHaveBeenCalledTimes(2);
  expect(catalog).toHaveBeenLastCalledWith(null);
  act(() => tree.unmount());
  expect(catalog).toHaveBeenLastCalledWith(null);
});

it('retains the conversation catalog when navigation closes the Files panel', async () => {
  vi.stubGlobal('window', { setInterval: vi.fn(), clearInterval: vi.fn(), addEventListener: vi.fn(), removeEventListener: vi.fn() });
  vi.stubGlobal('document', { addEventListener: vi.fn(), removeEventListener: vi.fn() });
  vi.stubGlobal('fetch', vi.fn(async () => ({ ok: true, json: async () => ({ root: { path: '/root', kind: 'directory', children: [{ name: 'README.md', path: '/root/README.md', kind: 'file' }] } }) })));
  const catalog = vi.fn(); let tree!: ReactTestRenderer;
  await act(async () => { tree = create(<FileTreePanel onFileCatalog={catalog} />); });
  catalog.mockClear();
  act(() => tree.unmount());
  expect(catalog).not.toHaveBeenCalled();
});

it('does not erase an existing conversation catalog while a newly opened Files panel is loading', async () => {
  vi.stubGlobal('window', { setInterval: vi.fn(), clearInterval: vi.fn(), addEventListener: vi.fn(), removeEventListener: vi.fn() });
  vi.stubGlobal('document', { addEventListener: vi.fn(), removeEventListener: vi.fn() });
  const pending = deferred<{ ok: boolean; json: () => Promise<unknown> }>();
  vi.stubGlobal('fetch', vi.fn(() => pending.promise));
  const catalog = vi.fn(); let tree!: ReactTestRenderer;
  await act(async () => { tree = create(<FileTreePanel onFileCatalog={catalog} />); });
  act(() => tree.unmount());
  await act(async () => pending.resolve({ ok: true, json: async () => ({ root: { path: '/root', kind: 'directory', children: [] } }) }));
  expect(catalog).not.toHaveBeenCalled();
});

it('clears immediately on root change and ignores a late response from the stale root', async () => {
  const oldRequest = deferred<{ ok: boolean; json: () => Promise<unknown> }>();
  const newRequest = deferred<{ ok: boolean; json: () => Promise<unknown> }>();
  vi.stubGlobal('window', { setInterval: vi.fn(() => 1), clearInterval: vi.fn(), addEventListener: vi.fn(), removeEventListener: vi.fn() });
  vi.stubGlobal('document', { visibilityState: 'visible', addEventListener: vi.fn(), removeEventListener: vi.fn() });
  vi.stubGlobal('fetch', vi.fn().mockReturnValueOnce(oldRequest.promise).mockReturnValueOnce(newRequest.promise));
  const catalog = vi.fn(); let tree!: ReactTestRenderer;
  await act(async () => { tree = create(<FileTreePanel onFileCatalog={catalog} />); });
  workspace.projectRoot = '/next';
  await act(async () => { tree.update(<FileTreePanel onFileCatalog={catalog} />); });
  expect(catalog).toHaveBeenLastCalledWith(null);
  await act(async () => oldRequest.resolve({ ok: true, json: async () => ({ root: { name: 'root', path: '/root', kind: 'directory', children: [{ name: 'old.md', path: '/root/old.md', kind: 'file' }] } }) }));
  expect(catalog).not.toHaveBeenCalledWith({ root: '/root', paths: ['/root/old.md'] });
  await act(async () => newRequest.resolve({ ok: true, json: async () => ({ root: { name: 'next', path: '/next', kind: 'directory', children: [{ name: 'new.md', path: '/next/new.md', kind: 'file' }] } }) }));
  expect(catalog).toHaveBeenLastCalledWith({ root: '/next', paths: ['/next/new.md'] });
  act(() => tree.unmount());
});
