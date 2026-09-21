export type ResizablePaneKey = 'fileTree' | 'toolkit' | 'chat';

export type LayoutStorageState = {
  widths: Record<ResizablePaneKey, number>;
  collapsed: Record<ResizablePaneKey, boolean>;
};

export const LAYOUT_STORAGE_KEY = 'chirality.layout.v1';
export const COLLAPSED_PANE_WIDTH_PX = 56;
export const HANDLE_WIDTH_PX = 12;
export const MAIN_PANE_MIN_WIDTH_PX = 520;
export const MIN_PANE_WIDTH_PX: Record<ResizablePaneKey, number> = {
  fileTree: 220,
  toolkit: 250,
  chat: 280
};
export const DEFAULT_PANE_WIDTH_PX: Record<ResizablePaneKey, number> = {
  fileTree: 280,
  toolkit: 300,
  chat: 320
};

export const APP_SHELL_GRID_TEMPLATE_COLUMNS =
  'minmax(0, 1fr) var(--pane-handle-width) minmax(56px, var(--pane-chat-width)) var(--pane-handle-width) minmax(56px, var(--pane-file-tree-width))';

export const APP_SHELL_GRID_ORDER = [
  'main',
  'chatResizeHandle',
  'chat',
  'workspaceResizeHandle',
  'workspaceSidebar'
] as const;

export const APP_SHELL_DRAG_DIRECTION: Record<ResizablePaneKey, 1 | -1> = {
  fileTree: -1,
  toolkit: -1,
  chat: -1
};

const RESIZABLE_PANES: readonly ResizablePaneKey[] = ['fileTree', 'toolkit', 'chat'];

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null;
}

function clamp(value: number, min: number, max: number): number {
  if (!Number.isFinite(value)) {
    return min;
  }
  if (max < min) {
    return min;
  }
  return Math.max(min, Math.min(max, value));
}

function toSafeNumber(value: unknown, fallback: number): number {
  if (typeof value !== 'number' || !Number.isFinite(value)) {
    return fallback;
  }
  return value;
}

function toSafeBoolean(value: unknown, fallback: boolean): boolean {
  if (typeof value !== 'boolean') {
    return fallback;
  }
  return value;
}

export function createDefaultLayoutState(): LayoutStorageState {
  return {
    widths: {
      fileTree: DEFAULT_PANE_WIDTH_PX.fileTree,
      toolkit: DEFAULT_PANE_WIDTH_PX.toolkit,
      chat: DEFAULT_PANE_WIDTH_PX.chat
    },
    collapsed: {
      fileTree: false,
      toolkit: false,
      chat: false
    }
  };
}

export function readLayoutStateFromStorage(
  storage: Pick<Storage, 'getItem'> | undefined
): LayoutStorageState {
  const fallback = createDefaultLayoutState();
  if (!storage) {
    return fallback;
  }

  try {
    const raw = storage.getItem(LAYOUT_STORAGE_KEY);
    if (!raw) {
      return fallback;
    }

    const parsed = JSON.parse(raw) as unknown;
    if (!isRecord(parsed)) {
      return fallback;
    }

    const widthsInput = isRecord(parsed.widths) ? parsed.widths : {};
    const collapsedInput = isRecord(parsed.collapsed) ? parsed.collapsed : {};

    return {
      widths: {
        fileTree: clamp(
          toSafeNumber(widthsInput.fileTree, fallback.widths.fileTree),
          MIN_PANE_WIDTH_PX.fileTree,
          2000
        ),
        toolkit: clamp(
          toSafeNumber(widthsInput.toolkit, fallback.widths.toolkit),
          MIN_PANE_WIDTH_PX.toolkit,
          2000
        ),
        chat: clamp(
          toSafeNumber(widthsInput.chat, fallback.widths.chat),
          MIN_PANE_WIDTH_PX.chat,
          2000
        )
      },
      collapsed: {
        fileTree: toSafeBoolean(collapsedInput.fileTree, fallback.collapsed.fileTree),
        toolkit: toSafeBoolean(collapsedInput.toolkit, fallback.collapsed.toolkit),
        chat: toSafeBoolean(collapsedInput.chat, fallback.collapsed.chat)
      }
    };
  } catch {
    return fallback;
  }
}

export function writeLayoutStateToStorage(
  storage: Pick<Storage, 'setItem'> | undefined,
  state: LayoutStorageState
): void {
  if (!storage) {
    return;
  }

  try {
    storage.setItem(
      LAYOUT_STORAGE_KEY,
      JSON.stringify({
        widths: state.widths,
        collapsed: state.collapsed
      })
    );
  } catch {
    // Ignore local-storage write failures; layout persistence is convenience state only.
  }
}

export function resolvePaneWidth(
  state: LayoutStorageState,
  pane: ResizablePaneKey,
  toolkitVisible: boolean
): number {
  if (pane === 'toolkit' && !toolkitVisible) {
    return 0;
  }

  if (state.collapsed[pane]) {
    return COLLAPSED_PANE_WIDTH_PX;
  }

  return state.widths[pane];
}

function countActiveHandles(toolkitVisible: boolean): number {
  return toolkitVisible ? 3 : 2;
}

export function clampPaneWidthForLayout(input: {
  pane: ResizablePaneKey;
  requestedWidth: number;
  state: LayoutStorageState;
  layoutWidth: number;
  toolkitVisible: boolean;
}): number {
  const { pane, requestedWidth, state, layoutWidth, toolkitVisible } = input;
  const minimum = MIN_PANE_WIDTH_PX[pane];

  if (!Number.isFinite(layoutWidth) || layoutWidth <= 0) {
    return clamp(requestedWidth, minimum, 2000);
  }

  const activePanes = RESIZABLE_PANES.filter((candidate) =>
    candidate === 'toolkit' ? toolkitVisible : true
  );
  const otherWidthTotal = activePanes
    .filter((candidate) => candidate !== pane)
    .reduce((sum, candidate) => sum + resolvePaneWidth(state, candidate, toolkitVisible), 0);

  const handleWidthTotal = countActiveHandles(toolkitVisible) * HANDLE_WIDTH_PX;
  const maximum = layoutWidth - otherWidthTotal - handleWidthTotal - MAIN_PANE_MIN_WIDTH_PX;

  return clamp(requestedWidth, minimum, maximum);
}

export function resolvePointerDragDelta(pane: ResizablePaneKey, pointerDelta: number): number {
  return pointerDelta * APP_SHELL_DRAG_DIRECTION[pane];
}
