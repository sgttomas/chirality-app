import React from 'react';
import { act, create, type ReactTestRenderer } from 'react-test-renderer';
import { afterEach, expect, it, vi } from 'vitest';

const workspace = vi.hoisted(() => ({ applyProjectRoot: vi.fn(async () => true), chooseProjectRoot: vi.fn(async () => true), hasElectronDirectoryPicker: true, errorMessage: null as string | null }));
vi.mock('../../components/workspace/workspace-provider', () => ({ useWorkspace: () => workspace }));
import { FolderSelect } from '../../components/shell/folder-select';

let tree: ReactTestRenderer | undefined;
afterEach(() => { if (tree) act(() => tree!.unmount()); tree = undefined; vi.clearAllMocks(); workspace.hasElectronDirectoryPicker = true; workspace.errorMessage = null; });
const text = (node: { children: unknown[] }): string => node.children.map(child => typeof child === 'string' ? child : child && typeof child === 'object' && 'children' in child ? text(child as { children: unknown[] }) : '').join('');

it('leads with the native picker and keeps the typed path behind a disclosure', async () => {
  await act(async () => { tree = create(<FolderSelect locked={false} root={null} disabled={false} />); });
  const menu = tree!.root.findByProps({ className: 'chat-folder-menu' });
  const children = menu.children.filter((child): child is Exclude<typeof child, string> => typeof child !== 'string');
  expect(children[0].type).toBe('button'); expect(text(children[0])).toBe('Choose folder…'); expect(children[0].props.disabled).toBe(false);
  expect(children[0].props.className).toBeUndefined();
  const disclosure = children[1];
  expect(disclosure.type).toBe('details'); expect(disclosure.props.open).toBeUndefined();
  expect(text(disclosure.findByType('summary'))).toBe('Enter a path…');
  expect(disclosure.findByProps({ 'aria-label': 'Folder path' })).toBeDefined();
  const useFolder = disclosure.findAllByType('button').find(node => text(node) === 'Use folder')!;
  expect(useFolder.props.disabled).toBe(true); expect(useFolder.props.className).toBe('button-muted');
  expect(text(menu)).not.toContain('Choose a folder before sending a message.');
  await act(async () => children[0].props.onClick());
  expect(workspace.chooseProjectRoot).toHaveBeenCalledOnce();
  await act(async () => disclosure.findByProps({ 'aria-label': 'Folder path' }).props.onChange({ target: { value: '/typed/root' } }));
  await act(async () => disclosure.findAllByType('button').find(node => text(node) === 'Use folder')!.props.onClick());
  expect(workspace.applyProjectRoot).toHaveBeenCalledExactlyOnceWith('/typed/root');
});

it('explains a disabled native picker on hover and keeps errors as alerts', async () => {
  workspace.hasElectronDirectoryPicker = false; workspace.errorMessage = 'Path is not readable';
  await act(async () => { tree = create(<FolderSelect locked={false} root="/root/project" disabled={false} />); });
  const native = tree!.root.findAllByType('button').find(node => text(node) === 'Choose folder…')!;
  expect(native.props.disabled).toBe(true); expect(native.props.title).toContain('Chirality Desktop');
  expect(tree!.root.findByProps({ role: 'alert' }).children.join('')).toBe('Path is not readable');
});

it('closes after a successful selection, stays open after a failed one, and dismisses on Escape or an outside pointer', async () => {
  class FakeNode { constructor(public readonly name: string) {} }
  const listeners = new Map<string, (event: unknown) => void>();
  const focus = vi.fn();
  vi.stubGlobal('Node', FakeNode);
  vi.stubGlobal('document', { addEventListener: (name: string, handler: (event: unknown) => void) => listeners.set(name, handler), removeEventListener: (name: string) => listeners.delete(name) });
  const inside = new FakeNode('inside'), outside = new FakeNode('outside');
  const menuNode = { contains: (node: unknown) => node === inside, querySelector: () => ({ focus }) };
  try {
    await act(async () => { tree = create(<FolderSelect locked={false} root={null} disabled={false} />, { createNodeMock: element => element.props.className === 'chat-folder-select' ? menuNode : null }); });
    const menu = () => tree!.root.findByProps({ className: 'chat-folder-select' });
    const chooseButton = () => tree!.root.findAllByType('button').find(node => text(node) === 'Choose folder…')!;
    expect(menu().props.open).toBe(false);
    await act(async () => menu().props.onToggle({ currentTarget: { open: true } }));
    expect(menu().props.open).toBe(true);
    // A failed native pick keeps the menu, and its alert, in view.
    workspace.chooseProjectRoot.mockResolvedValueOnce(false);
    await act(async () => chooseButton().props.onClick());
    expect(menu().props.open).toBe(true);
    // Escape closes and returns focus to the summary.
    act(() => listeners.get('keydown')!({ key: 'Escape', preventDefault: vi.fn() }));
    expect(menu().props.open).toBe(false);
    expect(focus).toHaveBeenCalledTimes(1);
    expect(listeners.has('pointerdown')).toBe(false);
    // An inside pointer keeps it open; an outside one closes it.
    await act(async () => menu().props.onToggle({ currentTarget: { open: true } }));
    act(() => listeners.get('pointerdown')!({ target: inside }));
    expect(menu().props.open).toBe(true);
    act(() => listeners.get('pointerdown')!({ target: outside }));
    expect(menu().props.open).toBe(false);
    // A successful pick closes it.
    await act(async () => menu().props.onToggle({ currentTarget: { open: true } }));
    await act(async () => chooseButton().props.onClick());
    expect(menu().props.open).toBe(false);
  } finally { vi.unstubAllGlobals(); }
});
