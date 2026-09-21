import React from 'react';
import renderer, { act } from 'react-test-renderer';
import { describe, expect, it, vi } from 'vitest';

vi.mock('../../components/shell/shell-frame', () => ({
  ShellFrame: ({ children }: { children: React.ReactNode }) => <>{children}</>
}));
vi.mock('../../components/shell/chat-panel', () => ({ ChatPanel: () => <div>chat</div> }));
vi.mock('../../components/shell/workspace-sidebar', () => ({
  WorkspaceSidebar: () => <div>workspace</div>
}));

describe('AppShell resize handles', () => {
  it('exposes keyboard-operable separators that collapse, expand, and resize', async () => {
    Object.assign(globalThis, { React });
    const { AppShell } = await import('../../components/shell/app-shell');
    const tree = renderer.create(
      <AppShell section="PORTAL" title="Portal" subtitle="Workspace">
        <div>main</div>
      </AppShell>
    );
    const handle = tree.root.find(
      (node) => node.props['aria-label'] === 'Resize Workspace'
    );

    expect(handle.props.role).toBe('separator');
    expect(handle.props.tabIndex).toBe(0);
    const initialWidth = handle.props['aria-valuenow'];

    act(() => handle.props.onKeyDown({ key: 'Home', shiftKey: false, preventDefault: vi.fn() }));
    expect(tree.root.find((node) => node.props['aria-label'] === 'Resize Workspace').props['aria-valuenow']).toBe(56);

    act(() => handle.props.onKeyDown({ key: 'End', shiftKey: false, preventDefault: vi.fn() }));
    expect(tree.root.find((node) => node.props['aria-label'] === 'Resize Workspace').props['aria-valuenow']).toBe(initialWidth);

    act(() => handle.props.onKeyDown({ key: 'ArrowRight', shiftKey: false, preventDefault: vi.fn() }));
    expect(tree.root.find((node) => node.props['aria-label'] === 'Resize Workspace').props['aria-valuenow']).toBe(initialWidth + 16);

    act(() => handle.props.onKeyDown({ key: 'ArrowLeft', shiftKey: false, preventDefault: vi.fn() }));
    expect(tree.root.find((node) => node.props['aria-label'] === 'Resize Workspace').props['aria-valuenow']).toBe(initialWidth);
  });
});
