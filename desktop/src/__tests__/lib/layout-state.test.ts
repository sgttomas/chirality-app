import { describe, expect, it, vi } from 'vitest';
import {
  APP_SHELL_DRAG_DIRECTION,
  APP_SHELL_GRID_ORDER,
  APP_SHELL_GRID_TEMPLATE_COLUMNS,
  COLLAPSED_PANE_WIDTH_PX,
  LAYOUT_STORAGE_KEY,
  clampPaneWidthForLayout,
  createDefaultLayoutState,
  readLayoutStateFromStorage,
  resolvePaneWidth,
  resolvePointerDragDelta
} from '../../lib/shell/layout-state';

describe('shell layout state helpers', () => {
  it('returns defaults when storage is unavailable or empty', () => {
    const defaults = createDefaultLayoutState();
    expect(readLayoutStateFromStorage(undefined)).toEqual(defaults);
    expect(readLayoutStateFromStorage({ getItem: vi.fn().mockReturnValue(null) })).toEqual(defaults);
  });

  it('sanitizes persisted layout payloads', () => {
    const storage = {
      getItem: vi.fn().mockReturnValue(
        JSON.stringify({
          widths: {
            fileTree: 100,
            toolkit: 480,
            chat: 'bad'
          },
          collapsed: {
            fileTree: true,
            toolkit: 'bad',
            chat: false
          }
        })
      )
    };

    const state = readLayoutStateFromStorage(storage);
    expect(storage.getItem).toHaveBeenCalledWith(LAYOUT_STORAGE_KEY);
    expect(state.widths.fileTree).toBe(220);
    expect(state.widths.toolkit).toBe(480);
    expect(state.widths.chat).toBe(320);
    expect(state.collapsed.fileTree).toBe(true);
    expect(state.collapsed.toolkit).toBe(false);
    expect(state.collapsed.chat).toBe(false);
  });

  it('resolves pane widths with collapse and toolkit visibility rules', () => {
    const state = createDefaultLayoutState();
    state.collapsed.fileTree = true;

    expect(resolvePaneWidth(state, 'fileTree', true)).toBe(COLLAPSED_PANE_WIDTH_PX);
    expect(resolvePaneWidth(state, 'toolkit', false)).toBe(0);
    expect(resolvePaneWidth(state, 'chat', true)).toBe(320);
  });

  it('clamps requested pane widths against layout constraints', () => {
    const state = createDefaultLayoutState();

    const enlarged = clampPaneWidthForLayout({
      pane: 'chat',
      requestedWidth: 900,
      state,
      layoutWidth: 1800,
      toolkitVisible: true
    });
    expect(enlarged).toBe(664);

    const constrained = clampPaneWidthForLayout({
      pane: 'toolkit',
      requestedWidth: 200,
      state,
      layoutWidth: 1400,
      toolkitVisible: true
    });
    expect(constrained).toBe(250);
  });

  it('clamps the two-pane (sidebar + chat) geometry the shell now uses (toolkitVisible=false)', () => {
    // After the Tool Kit folded into the sidebar, app-shell always passes
    // toolkitVisible=false, so only two side panes and two handles count.
    const state = createDefaultLayoutState();

    // chat max = layoutWidth - fileTree(280) - 2 handles(24) - MAIN_MIN(520).
    const chatMax = clampPaneWidthForLayout({
      pane: 'chat',
      requestedWidth: 1500,
      state,
      layoutWidth: 1800,
      toolkitVisible: false
    });
    expect(chatMax).toBe(1800 - 280 - 24 - 520);

    // sidebar (fileTree) max = layoutWidth - chat(320) - 2 handles(24) - MAIN_MIN(520).
    const sidebarMax = clampPaneWidthForLayout({
      pane: 'fileTree',
      requestedWidth: 1500,
      state,
      layoutWidth: 1800,
      toolkitVisible: false
    });
    expect(sidebarMax).toBe(1800 - 320 - 24 - 520);

    // The toolkit pane resolves to zero width in this mode and never renders.
    expect(resolvePaneWidth(state, 'toolkit', false)).toBe(0);
  });

  it('guards the AppShell right-sidebar grid order and drag signs', () => {
    expect(APP_SHELL_GRID_ORDER).toEqual([
      'main',
      'chatResizeHandle',
      'chat',
      'workspaceResizeHandle',
      'workspaceSidebar'
    ]);
    expect(APP_SHELL_GRID_TEMPLATE_COLUMNS).toBe(
      'minmax(0, 1fr) var(--pane-handle-width) minmax(56px, var(--pane-chat-width)) var(--pane-handle-width) minmax(56px, var(--pane-file-tree-width))'
    );
    expect(APP_SHELL_DRAG_DIRECTION).toMatchObject({
      fileTree: -1,
      chat: -1
    });
    expect(resolvePointerDragDelta('fileTree', -40)).toBe(40);
    expect(resolvePointerDragDelta('fileTree', 40)).toBe(-40);
    expect(resolvePointerDragDelta('chat', -40)).toBe(40);
  });

  it('falls back to simple min/max clamping when layout width is invalid', () => {
    const state = createDefaultLayoutState();
    const result = clampPaneWidthForLayout({
      pane: 'fileTree',
      requestedWidth: 9000,
      state,
      layoutWidth: 0,
      toolkitVisible: true
    });
    expect(result).toBe(2000);
  });
});
