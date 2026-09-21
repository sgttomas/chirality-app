'use client';

import {
  Suspense,
  useCallback,
  useEffect,
  useMemo,
  useRef,
  useState,
  type CSSProperties,
  type KeyboardEvent,
  type PointerEvent,
  type ReactNode
} from 'react';
import {
  DEFAULT_PANE_WIDTH_PX,
  MIN_PANE_WIDTH_PX,
  APP_SHELL_GRID_ORDER,
  APP_SHELL_GRID_TEMPLATE_COLUMNS,
  clampPaneWidthForLayout,
  createDefaultLayoutState,
  readLayoutStateFromStorage,
  resolvePaneWidth,
  resolvePointerDragDelta,
  writeLayoutStateToStorage,
  type LayoutStorageState,
  type ResizablePaneKey
} from '../../lib/shell/layout-state';
import { ChatPanel } from './chat-panel';
import { ShellFrame, type ShellSection } from './shell-frame';
import { WorkspaceSidebar, type SidebarTabId } from './workspace-sidebar';

type AppShellProps = {
  section: ShellSection;
  title: string;
  subtitle: string;
  children: ReactNode;
};

// Two resizable side panes remain after the Tool Kit folded into the sidebar as
// a tab: `fileTree` is the multi-view workspace sidebar, `chat` is the live loop.
// The `toolkit` entries below are retained only to satisfy the frozen
// `Record<ResizablePaneKey, ...>` type (layout-state.ts is intentionally
// unchanged); no resize handle is ever rendered for the `toolkit` pane.
const PANE_TITLE: Record<ResizablePaneKey, string> = {
  fileTree: 'Workspace',
  toolkit: 'Tool Kit',
  chat: 'Chat Panel'
};

// The dedicated Tool Kit pane is gone (it is now a sidebar tab); the layout
// geometry therefore always computes for the two-pane sidebar + chat shell.
const TOOLKIT_PANE_VISIBLE = false;

type AppShellRenderedPaneKey = Extract<ResizablePaneKey, 'fileTree' | 'chat'>;

const APP_SHELL_RESIZE_HANDLE_SLOT: Record<
  AppShellRenderedPaneKey,
  (typeof APP_SHELL_GRID_ORDER)[number]
> = {
  chat: APP_SHELL_GRID_ORDER[1],
  fileTree: APP_SHELL_GRID_ORDER[3]
};

export function AppShell({ section, title, subtitle, children }: AppShellProps): JSX.Element {
  const [layoutState, setLayoutState] = useState<LayoutStorageState>(() =>
    createDefaultLayoutState()
  );
  const [layoutWidth, setLayoutWidth] = useState(0);
  const [resizingPane, setResizingPane] = useState<ResizablePaneKey | null>(null);
  // Lifted out of WorkspaceSidebar so the chosen tab survives the pane being
  // unmounted while collapsed.
  const [sidebarTab, setSidebarTab] = useState<SidebarTabId>('files');
  const layoutRef = useRef<HTMLElement | null>(null);
  const dragStateRef = useRef<{
    pane: ResizablePaneKey;
    startX: number;
    startWidth: number;
  } | null>(null);

  useEffect(() => {
    if (typeof window === 'undefined') {
      return;
    }
    setLayoutState(readLayoutStateFromStorage(window.localStorage));
  }, []);

  useEffect(() => {
    if (typeof window === 'undefined') {
      return;
    }
    writeLayoutStateToStorage(window.localStorage, layoutState);
  }, [layoutState]);

  useEffect(() => {
    const element = layoutRef.current;
    if (!element) {
      return;
    }

    const updateWidth = (): void => {
      setLayoutWidth(element.clientWidth);
    };

    updateWidth();

    const observer = new ResizeObserver(updateWidth);
    observer.observe(element);

    return () => {
      observer.disconnect();
    };
  }, []);

  const gridStyle = useMemo(
    () =>
      ({
        '--shell-grid-template-columns': APP_SHELL_GRID_TEMPLATE_COLUMNS,
        '--pane-file-tree-width': `${resolvePaneWidth(layoutState, 'fileTree', TOOLKIT_PANE_VISIBLE)}px`,
        '--pane-chat-width': `${resolvePaneWidth(layoutState, 'chat', TOOLKIT_PANE_VISIBLE)}px`
      }) as CSSProperties,
    [layoutState]
  );

  const resizePaneByDelta = useCallback(
    (pane: ResizablePaneKey, delta: number): void => {
      setLayoutState((current) => {
        const requestedWidth = current.widths[pane] + delta;
        const nextWidth = clampPaneWidthForLayout({
          pane,
          requestedWidth,
          state: current,
          layoutWidth,
          toolkitVisible: TOOLKIT_PANE_VISIBLE
        });

        return {
          ...current,
          collapsed: {
            ...current.collapsed,
            [pane]: false
          },
          widths: {
            ...current.widths,
            [pane]: nextWidth
          }
        };
      });
    },
    [layoutWidth]
  );

  const togglePaneCollapse = useCallback((pane: ResizablePaneKey): void => {
    setLayoutState((current) => ({
      ...current,
      collapsed: {
        ...current.collapsed,
        [pane]: !current.collapsed[pane]
      }
    }));
  }, []);

  const handleResizePointerDown = useCallback(
    (event: PointerEvent<HTMLDivElement>, pane: ResizablePaneKey): void => {
      if (event.button !== 0) {
        return;
      }

      event.preventDefault();
      dragStateRef.current = {
        pane,
        startX: event.clientX,
        startWidth: layoutState.widths[pane]
      };
      setResizingPane(pane);
    },
    [layoutState.widths]
  );

  useEffect(() => {
    if (!resizingPane) {
      return;
    }

    const handlePointerMove = (event: globalThis.PointerEvent): void => {
      const dragState = dragStateRef.current;
      if (!dragState) {
        return;
      }

      const delta = resolvePointerDragDelta(
        dragState.pane,
        event.clientX - dragState.startX
      );
      const requestedWidth = dragState.startWidth + delta;

      setLayoutState((current) => {
        const nextWidth = clampPaneWidthForLayout({
          pane: dragState.pane,
          requestedWidth,
          state: current,
          layoutWidth,
          toolkitVisible: TOOLKIT_PANE_VISIBLE
        });

        return {
          ...current,
          collapsed: {
            ...current.collapsed,
            [dragState.pane]: false
          },
          widths: {
            ...current.widths,
            [dragState.pane]: nextWidth
          }
        };
      });
    };

    const stopResizing = (): void => {
      dragStateRef.current = null;
      setResizingPane(null);
    };

    window.addEventListener('pointermove', handlePointerMove);
    window.addEventListener('pointerup', stopResizing);
    window.addEventListener('pointercancel', stopResizing);

    return () => {
      window.removeEventListener('pointermove', handlePointerMove);
      window.removeEventListener('pointerup', stopResizing);
      window.removeEventListener('pointercancel', stopResizing);
    };
  }, [layoutWidth, resizingPane]);

  function handleResizeKeyDown(event: KeyboardEvent<HTMLDivElement>, pane: ResizablePaneKey): void {
    const step = event.shiftKey ? 40 : 16;

    if (event.key === 'ArrowRight') {
      event.preventDefault();
      resizePaneByDelta(pane, step);
      return;
    }

    if (event.key === 'ArrowLeft') {
      event.preventDefault();
      resizePaneByDelta(pane, -step);
      return;
    }

    if (event.key === 'Home') {
      event.preventDefault();
      setLayoutState((current) => ({
        ...current,
        collapsed: {
          ...current.collapsed,
          [pane]: true
        }
      }));
      return;
    }

    if (event.key === 'End') {
      event.preventDefault();
      setLayoutState((current) => {
        const requestedWidth = current.widths[pane] || DEFAULT_PANE_WIDTH_PX[pane];
        const nextWidth = clampPaneWidthForLayout({
          pane,
          requestedWidth,
          state: current,
          layoutWidth,
          toolkitVisible: TOOLKIT_PANE_VISIBLE
        });

        return {
          ...current,
          collapsed: {
            ...current.collapsed,
            [pane]: false
          },
          widths: {
            ...current.widths,
            [pane]: nextWidth
          }
        };
      });
    }
  }

  function renderResizeHandle(pane: AppShellRenderedPaneKey): JSX.Element {
    const widthNow = resolvePaneWidth(layoutState, pane, TOOLKIT_PANE_VISIBLE);
    const isActive = resizingPane === pane;

    return (
      <div
        key={`handle-${pane}`}
        data-shell-slot={APP_SHELL_RESIZE_HANDLE_SLOT[pane]}
        className={isActive ? 'shell-resize-handle shell-resize-handle--active' : 'shell-resize-handle'}
        role="separator"
        aria-label={`Resize ${PANE_TITLE[pane]}`}
        aria-orientation="vertical"
        aria-valuemin={MIN_PANE_WIDTH_PX[pane]}
        aria-valuenow={widthNow}
        tabIndex={0}
        onPointerDown={(event) => {
          handleResizePointerDown(event, pane);
        }}
        onKeyDown={(event) => {
          handleResizeKeyDown(event, pane);
        }}
      />
    );
  }

  return (
    <ShellFrame section={section} title={title} subtitle={subtitle}>
      <section
        ref={layoutRef}
        className="shell-grid shell-grid--resizable"
        style={gridStyle}
      >
        <section className="panel panel--main" data-shell-slot={APP_SHELL_GRID_ORDER[0]}>
          <header className="panel-header">
            <h2>Execution Surface</h2>
          </header>
          <div className="panel-body">{children}</div>
        </section>

        {renderResizeHandle('chat')}

        <div
          data-shell-slot={APP_SHELL_GRID_ORDER[2]}
          className={layoutState.collapsed.chat ? 'shell-pane shell-pane--chat shell-pane--collapsed' : 'shell-pane shell-pane--chat'}
        >
          <button
            type="button"
            className="shell-pane-toggle button-muted"
            onClick={() => {
              togglePaneCollapse('chat');
            }}
          >
            {layoutState.collapsed.chat ? 'Expand' : 'Collapse'}
          </button>
          {layoutState.collapsed.chat ? <span className="shell-pane-collapsed-label">Chat</span> : null}
          <Suspense
            fallback={
              <aside className="panel panel--chat">
                <header className="panel-header">
                  <h2>Chat Panel</h2>
                </header>
                <div className="panel-body chat-transcript">
                  <p className="panel-empty">Loading chat panel...</p>
                </div>
              </aside>
            }
          >
            <ChatPanel />
          </Suspense>
        </div>

        {renderResizeHandle('fileTree')}

        <div
          data-shell-slot={APP_SHELL_GRID_ORDER[4]}
          className={
            layoutState.collapsed.fileTree
              ? 'shell-pane shell-pane--sidebar shell-pane--collapsed'
              : 'shell-pane shell-pane--sidebar'
          }
        >
          <button
            type="button"
            className="shell-pane-toggle button-muted"
            onClick={() => {
              togglePaneCollapse('fileTree');
            }}
          >
            {layoutState.collapsed.fileTree ? 'Expand' : 'Collapse'}
          </button>
          {layoutState.collapsed.fileTree ? (
            <span className="shell-pane-collapsed-label">Workspace</span>
          ) : (
            <WorkspaceSidebar activeTab={sidebarTab} onTabChange={setSidebarTab} />
          )}
        </div>
      </section>
    </ShellFrame>
  );
}
