import type { CoordinationPanelView } from './contracts';

export const WOVEN_WORKSPACE_STORAGE_KEY = 'chirality.wovenWorkspace.v1';
export const WOVEN_WORKSPACE_SCHEMA = 'chirality.woven-workspace/v1';

const LEGACY_LAYOUT_STORAGE_KEY = 'chirality.layout.v1';
const MIN_NAVIGATOR_WIDTH = 220;
const MAX_PANE_SIZE = 2000;
const MAX_REFERENCE_COUNT = 200;
const MAX_REFERENCE_LENGTH = 2048;

/**
 * Upper bound on the local session→surface attribution map. The map is a
 * projection convenience only (no project truth), so the oldest attributions
 * are evicted rather than growing the stored blob without limit.
 */
export const MAX_SESSION_SURFACE_ATTRIBUTIONS = 500;
/** Upper bound on the local chat index; the oldest entries are evicted. */
export const MAX_CHAT_INDEX_ENTRIES = 500;

type WovenWorkspaceMigrationField = 'navigatorWidth' | 'navigatorCollapsed';

/**
 * Presentation theme. `light` is the product default; `dark` and `system` are
 * explicit human choices. `system` is the only value that consults the
 * operating system, and it does so purely in CSS.
 */
export type WovenWorkspaceTheme = 'light' | 'dark' | 'system';

export const WOVEN_WORKSPACE_THEMES: readonly WovenWorkspaceTheme[] = [
  'light',
  'dark',
  'system'
];

export const DEFAULT_WOVEN_WORKSPACE_THEME: WovenWorkspaceTheme = 'light';

/**
 * Navigator surface. Declared here rather than in the navigator component
 * because the versioned workspace state is the durable home of the
 * client-side session→surface attribution map; `WovenSurface` aliases it.
 */
export type WovenWorkspaceSurface = 'dialogue' | 'workbench' | 'pipeline';

export const WOVEN_WORKSPACE_SURFACES: readonly WovenWorkspaceSurface[] = [
  'dialogue',
  'workbench',
  'pipeline'
];

export const DEFAULT_WOVEN_WORKSPACE_SURFACE: WovenWorkspaceSurface = 'dialogue';

/**
 * Local annotation only: `sessionId → surface active when that session was
 * first observed`. Recorded session records carry no surface field, so this
 * map is a client-side tag-forward convenience and never project truth.
 * Sessions absent from the map stay unattributed and surface only in the
 * navigator's "All sessions" list.
 */
export type WovenSessionSurfaceMap = Readonly<
  Record<string, WovenWorkspaceSurface>
>;

export type WovenRightPanelView = 'files' | 'plan' | 'workflows' | 'skills' | 'agents' | 'activity' | 'settings';
export const RIGHT_PANEL_VIEWS: readonly WovenRightPanelView[] = ['files', 'plan', 'workflows', 'skills', 'agents', 'activity', 'settings'];
/** Future stored views must leave existing content reachable, never blank it. */
export function resolveRightPanelView(view: WovenRightPanelView | undefined): WovenRightPanelView {
  if (view === 'skills') return 'workflows';
  return view !== undefined && RIGHT_PANEL_VIEWS.includes(view) ? view : 'files';
}
export type WovenRightPanelWidthKey = WovenRightPanelView | 'document' | 'session';
export type WovenChatRung = { kind: 'plain' | 'spec' | 'workflow'; ref?: string; declined?: string[] };
/**
 * Local index of every chat this App has listed, keyed by session id, so chats
 * bound to folders other than the one currently selected stay reachable in
 * the navigator. The Runtime record is the truth; this is a pointer to it
 * (folder, role, timestamps) refreshed whenever that folder is listed again.
 */
export type WovenChatIndexEntry = { projectRoot: string; persona?: string; createdAt: string; updatedAt: string };
export type WovenWorkspaceAdditions = {
  rightPanelView: WovenRightPanelView;
  rightPanelWidths: Partial<Record<WovenRightPanelWidthKey, number>>;
  rightPanelExpanded: boolean;
  preExpandState: { rightWidth: number; leftCollapsed: boolean } | null;
  openDocumentPath: string | null;
  chatTitles: Record<string, string>;
  chatPins: string[];
  chatArchived: string[];
  chatDeleted: string[];
  chatGroups: { id: string; name: string; sessionIds: string[] }[];
  groupsCollapsed: string[];
  knownRoots: { path: string; lastUsedAt: string }[];
  chatRung: Record<string, WovenChatRung>;
  chatIndex: Record<string, WovenChatIndexEntry>;
  /** Navigator folder sections the human collapsed (folder paths). */
  foldersCollapsed: string[];
  /** Per-chat document context: the Files tab document open for that session. */
  chatDocuments: Record<string, string>;
  /** The chat open when the window was last used; restored on the next launch. */
  lastActiveChat: { sessionId: string; projectRoot: string } | null;
};

// Older typed callers may omit additions; readers always return every field.
export type NormalizedWovenWorkspaceState = WovenWorkspaceState & WovenWorkspaceAdditions;
export type WovenWorkspaceState = Partial<WovenWorkspaceAdditions> & {
  schema: typeof WOVEN_WORKSPACE_SCHEMA;
  /**
   * Additive field under the unchanged `chirality.woven-workspace/v1` schema
   * string: stored v1 blobs written before the theme control existed still
   * load, falling back to the `light` default.
   */
  theme: WovenWorkspaceTheme;
  navigatorWidth: number;
  coordinationWidth: number;
  activityHeight: number;
  navigatorCollapsed: boolean;
  coordinationCollapsed: boolean;
  activityCollapsed: boolean;
  coordinationView: CoordinationPanelView;
  dialogueAnchorId: string | null;
  focusedArtifact: {
    artifactReference: string;
    dialogueAnchorId: string;
  } | null;
  expandedObjectIds: string[];
  selectedReplaySessionId: string | null;
  contextReferences: string[];
  /**
   * Additive v1 field (no schema-string bump): client-side session→surface
   * attribution for the navigator's mode-scoped history lists.
   */
  sessionSurfaces: WovenSessionSurfaceMap;
  /**
   * Additive v1 field: which navigator mode groups are expanded. An empty
   * array is a real state (the human collapsed everything); a missing field
   * falls back to the default surface.
   */
  navigatorExpandedSurfaces: WovenWorkspaceSurface[];
  migration: {
    sourceKey: typeof LEGACY_LAYOUT_STORAGE_KEY | null;
    mappedFields: WovenWorkspaceMigrationField[];
  };
};

type WovenWorkspaceStorage = Pick<Storage, 'getItem' | 'setItem'>;

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null && !Array.isArray(value);
}

function clampNumber(value: unknown, fallback: number, minimum: number): number {
  if (typeof value !== 'number' || !Number.isFinite(value)) {
    return fallback;
  }
  return Math.max(minimum, Math.min(MAX_PANE_SIZE, value));
}

function readBoolean(value: unknown, fallback: boolean): boolean {
  return typeof value === 'boolean' ? value : fallback;
}

function readReference(value: unknown): string | null {
  if (typeof value !== 'string') {
    return null;
  }
  const reference = value.trim();
  if (!reference) {
    return null;
  }
  return reference.slice(0, MAX_REFERENCE_LENGTH);
}

function readReferenceArray(value: unknown): string[] {
  if (!Array.isArray(value)) {
    return [];
  }

  const references = new Set<string>();
  for (const entry of value) {
    const reference = readReference(entry);
    if (reference) {
      references.add(reference);
    }
    if (references.size >= MAX_REFERENCE_COUNT) {
      break;
    }
  }
  return [...references];
}

// New identities are opaque hints: preserve meaningful bytes and never truncate.
function readIdentity(value: unknown): string | null {
  return typeof value === 'string' && value.trim().length > 0 &&
    value.length <= MAX_REFERENCE_LENGTH && !/[\u0000-\u001f\u007f]/.test(value)
    ? value : null;
}

function readIdentities(value: unknown): string[] {
  if (!Array.isArray(value)) return [];
  const result = new Set<string>();
  for (const entry of value) {
    const identity = readIdentity(entry);
    if (identity !== null) result.add(identity);
    if (result.size === MAX_REFERENCE_COUNT) break;
  }
  return [...result];
}

function readLabel(value: unknown): string | null {
  return readIdentity(value)?.trim() ?? null;
}

function readHintMap<T>(value: unknown, read: (raw: unknown) => T | null): Record<string, T> {
  if (!isRecord(value)) return {};
  const entries: [string, T][] = [];
  for (const [key, raw] of Object.entries(value)) {
    const identity = readIdentity(key);
    const item = read(raw);
    if (identity !== null && item !== null) entries.push([identity, item]);
  }
  // fromEntries creates own data properties even for __proto__ and constructor.
  return Object.fromEntries(entries.slice(-500));
}

function readRung(value: unknown): WovenChatRung | null {
  if (!isRecord(value) || !['plain', 'spec', 'workflow'].includes(value.kind as string)) return null;
  const ref = readIdentity(value.ref);
  return {
    kind: value.kind as WovenChatRung['kind'],
    ...(ref === null ? {} : { ref }),
    ...(Object.hasOwn(value, 'declined') ? { declined: readIdentities(value.declined) } : {})
  };
}

function readKnownRoots(value: unknown): WovenWorkspaceAdditions['knownRoots'] {
  const roots = new Map<string, { path: string; lastUsedAt: string }>();
  if (!Array.isArray(value)) return [];
  for (const entry of value) {
    if (!isRecord(entry)) continue;
    const path = readIdentity(entry.path);
    const stamp = entry.lastUsedAt;
    // Require a real ISO instant, including calendar validity, not Date.parse's
    // permissive date-only or rollover forms. Normalize offsets to UTC.
    if (!path || typeof stamp !== 'string' ||
      !/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,3})?(?:Z|[+-]\d{2}:\d{2})$/.test(stamp)) continue;
    const date = new Date(stamp);
    const calendar = new Date(stamp.slice(0, 10) + 'T00:00:00Z');
    if (!Number.isFinite(date.getTime()) || calendar.toISOString().slice(0, 10) !== stamp.slice(0, 10) ||
      Number(stamp.slice(11, 13)) > 23) continue;
    const lastUsedAt = date.toISOString();
    if (!roots.has(path) || roots.get(path)!.lastUsedAt < lastUsedAt) roots.set(path, { path, lastUsedAt });
  }
  return [...roots.values()].sort((a, b) => b.lastUsedAt.localeCompare(a.lastUsedAt)).slice(0, 50);
}

function readChatIndexEntry(value: unknown): WovenChatIndexEntry | null {
  if (!isRecord(value)) return null;
  const projectRoot = readIdentity(value.projectRoot);
  const createdAt = readIdentity(value.createdAt) ?? '';
  const updatedAt = readIdentity(value.updatedAt) ?? createdAt;
  if (!projectRoot) return null;
  const persona = readIdentity(value.persona);
  return { projectRoot, createdAt, updatedAt, ...(persona ? { persona } : {}) };
}

function readLastActiveChat(value: unknown): WovenWorkspaceAdditions['lastActiveChat'] {
  if (!isRecord(value)) return null;
  const sessionId = readIdentity(value.sessionId);
  const projectRoot = readIdentity(value.projectRoot);
  return sessionId && projectRoot ? { sessionId, projectRoot } : null;
}

/**
 * Merge freshly listed sessions into the index. Entries for sessions the
 * listing of `projectRoot` no longer returns are dropped only for that folder,
 * so an index entry never outlives the record it points to on the folder that
 * owns it. Returns the same reference when nothing changed.
 */
export function indexWovenChats(
  state: WovenWorkspaceState,
  projectRoot: string,
  sessions: readonly { sessionId: string; projectRoot?: string; persona?: string; createdAt?: string; updatedAt?: string }[]
): WovenWorkspaceState {
  const current = state.chatIndex ?? {};
  const next: Record<string, WovenChatIndexEntry> = {};
  let changed = false;
  const dropped = new Set<string>();
  for (const [sessionId, entry] of Object.entries(current)) {
    if (entry.projectRoot === projectRoot) { dropped.add(sessionId); continue; }
    next[sessionId] = entry;
  }
  for (const session of sessions) {
    const root = readIdentity(session.projectRoot) ?? projectRoot;
    const entry: WovenChatIndexEntry = {
      projectRoot: root,
      createdAt: session.createdAt ?? '',
      updatedAt: session.updatedAt ?? session.createdAt ?? '',
      ...(session.persona ? { persona: session.persona } : {})
    };
    const previous = current[session.sessionId];
    if (!previous || previous.projectRoot !== entry.projectRoot || previous.updatedAt !== entry.updatedAt || previous.createdAt !== entry.createdAt || previous.persona !== entry.persona) changed = true;
    dropped.delete(session.sessionId);
    next[session.sessionId] = entry;
  }
  if (!changed && dropped.size === 0) return state;
  const entries = Object.entries(next).sort((a, b) => b[1].updatedAt.localeCompare(a[1].updatedAt)).slice(0, MAX_CHAT_INDEX_ENTRIES);
  return { ...state, chatIndex: Object.fromEntries(entries) };
}

function readAdditions(value: Record<string, unknown>): WovenWorkspaceAdditions {
  const views: readonly WovenRightPanelView[] = RIGHT_PANEL_VIEWS;
  const widths: WovenWorkspaceAdditions['rightPanelWidths'] = {};
  const rawWidths = isRecord(value.rightPanelWidths) ? value.rightPanelWidths : {};
  for (const key of [...views, 'document', 'session'] as WovenRightPanelWidthKey[]) {
    const width = Object.hasOwn(rawWidths, key) ? rawWidths[key] : undefined;
    if (typeof width === 'number' && Number.isFinite(width)) widths[key] = clampNumber(width, 280, 280);
  }
  const groups = new Map<string, WovenWorkspaceAdditions['chatGroups'][number]>();
  if (Array.isArray(value.chatGroups)) {
    for (const entry of value.chatGroups) {
      if (!isRecord(entry)) continue;
      const id = readIdentity(entry.id), name = readLabel(entry.name);
      if (id && name && !groups.has(id)) groups.set(id, { id, name, sessionIds: readIdentities(entry.sessionIds) });
      if (groups.size === MAX_REFERENCE_COUNT) break;
    }
  }
  const pre = value.preExpandState;
  return {
    rightPanelView: Object.hasOwn(value, 'rightPanelView')
      ? resolveRightPanelView(value.rightPanelView as WovenRightPanelView)
      : value.coordinationView === 'agents' ? 'agents' : 'files',
    rightPanelWidths: widths,
    rightPanelExpanded: readBoolean(value.rightPanelExpanded, false),
    preExpandState: isRecord(pre) && typeof pre.rightWidth === 'number' && Number.isFinite(pre.rightWidth) && typeof pre.leftCollapsed === 'boolean'
      ? { rightWidth: clampNumber(pre.rightWidth, 280, 280), leftCollapsed: pre.leftCollapsed } : null,
    openDocumentPath: readIdentity(value.openDocumentPath),
    chatTitles: readHintMap(value.chatTitles, readLabel),
    chatPins: readIdentities(value.chatPins),
    chatArchived: readIdentities(value.chatArchived),
    chatDeleted: readIdentities(value.chatDeleted),
    chatGroups: [...groups.values()],
    groupsCollapsed: readIdentities(value.groupsCollapsed),
    knownRoots: readKnownRoots(value.knownRoots),
    chatRung: readHintMap(value.chatRung, readRung),
    chatIndex: readHintMap(value.chatIndex, readChatIndexEntry),
    foldersCollapsed: readIdentities(value.foldersCollapsed),
    chatDocuments: readHintMap(value.chatDocuments, readIdentity),
    lastActiveChat: readLastActiveChat(value.lastActiveChat)
  };
}

function readCoordinationView(value: unknown): CoordinationPanelView {
  return value === 'agents' ? 'agents' : 'work';
}

export function readWovenWorkspaceTheme(value: unknown): WovenWorkspaceTheme {
  return WOVEN_WORKSPACE_THEMES.includes(value as WovenWorkspaceTheme)
    ? (value as WovenWorkspaceTheme)
    : DEFAULT_WOVEN_WORKSPACE_THEME;
}

export function readWovenWorkspaceSurface(
  value: unknown
): WovenWorkspaceSurface | null {
  return WOVEN_WORKSPACE_SURFACES.includes(value as WovenWorkspaceSurface)
    ? (value as WovenWorkspaceSurface)
    : null;
}

function readSessionSurfaces(value: unknown): WovenSessionSurfaceMap {
  if (!isRecord(value)) {
    return {};
  }

  const entries: Array<[string, WovenWorkspaceSurface]> = [];
  for (const [key, raw] of Object.entries(value)) {
    const sessionId = readReference(key);
    const surface = readWovenWorkspaceSurface(raw);
    if (sessionId && surface) {
      entries.push([sessionId, surface]);
    }
  }
  // Insertion order is oldest-first, so the tail holds the newest attributions.
  return Object.fromEntries(entries.slice(-MAX_SESSION_SURFACE_ATTRIBUTIONS));
}

function readNavigatorExpandedSurfaces(value: unknown): WovenWorkspaceSurface[] {
  if (!Array.isArray(value)) {
    return [DEFAULT_WOVEN_WORKSPACE_SURFACE];
  }

  const surfaces = new Set<WovenWorkspaceSurface>();
  for (const entry of value) {
    const surface = readWovenWorkspaceSurface(entry);
    if (surface) {
      surfaces.add(surface);
    }
  }
  return [...surfaces];
}

/**
 * First attribution wins: a session is tagged with the surface that was active
 * when it was first observed and is never retagged. Returns the same state
 * reference when nothing changes so callers can rely on identity.
 */
export function recordWovenSessionSurface(
  state: NormalizedWovenWorkspaceState,
  sessionId: string | null | undefined,
  surface: WovenWorkspaceSurface
): NormalizedWovenWorkspaceState;
export function recordWovenSessionSurface(
  state: WovenWorkspaceState,
  sessionId: string | null | undefined,
  surface: WovenWorkspaceSurface
): WovenWorkspaceState;
export function recordWovenSessionSurface(
  state: WovenWorkspaceState,
  sessionId: string | null | undefined,
  surface: WovenWorkspaceSurface
): WovenWorkspaceState {
  const normalized = readReference(sessionId);
  if (!normalized || state.sessionSurfaces[normalized]) {
    return state;
  }

  const entries: Array<[string, WovenWorkspaceSurface]> = [
    ...Object.entries(state.sessionSurfaces),
    [normalized, surface]
  ];
  return {
    ...state,
    sessionSurfaces: Object.fromEntries(
      entries.slice(-MAX_SESSION_SURFACE_ATTRIBUTIONS)
    )
  };
}

export function toggleWovenNavigatorExpandedSurface(
  state: NormalizedWovenWorkspaceState,
  surface: WovenWorkspaceSurface
): NormalizedWovenWorkspaceState;
export function toggleWovenNavigatorExpandedSurface(
  state: WovenWorkspaceState,
  surface: WovenWorkspaceSurface
): WovenWorkspaceState;
export function toggleWovenNavigatorExpandedSurface(
  state: WovenWorkspaceState,
  surface: WovenWorkspaceSurface
): WovenWorkspaceState {
  return {
    ...state,
    navigatorExpandedSurfaces: state.navigatorExpandedSurfaces.includes(surface)
      ? state.navigatorExpandedSurfaces.filter((entry) => entry !== surface)
      : [...state.navigatorExpandedSurfaces, surface]
  };
}

function readFocusedArtifact(
  value: unknown
): WovenWorkspaceState['focusedArtifact'] {
  if (!isRecord(value)) {
    return null;
  }
  const artifactReference = readReference(value.artifactReference);
  const dialogueAnchorId = readReference(value.dialogueAnchorId);
  if (!artifactReference || !dialogueAnchorId) {
    return null;
  }
  return {
    artifactReference,
    dialogueAnchorId
  };
}

function readMigration(value: unknown): WovenWorkspaceState['migration'] {
  if (!isRecord(value)) {
    return {
      sourceKey: null,
      mappedFields: []
    };
  }

  const rawFields = Array.isArray(value.mappedFields) ? value.mappedFields : [];
  const mappedFields = rawFields.filter(
    (field): field is WovenWorkspaceMigrationField =>
      field === 'navigatorWidth' || field === 'navigatorCollapsed'
  );

  return {
    sourceKey:
      value.sourceKey === LEGACY_LAYOUT_STORAGE_KEY
        ? LEGACY_LAYOUT_STORAGE_KEY
        : null,
    mappedFields: [...new Set(mappedFields)]
  };
}

export function createDefaultWovenWorkspaceState(): NormalizedWovenWorkspaceState {
  return {
    ...readAdditions({}),
    schema: WOVEN_WORKSPACE_SCHEMA,
    theme: DEFAULT_WOVEN_WORKSPACE_THEME,
    navigatorWidth: 240,
    coordinationWidth: 360,
    activityHeight: 220,
    navigatorCollapsed: false,
    coordinationCollapsed: false,
    activityCollapsed: true,
    coordinationView: 'work',
    dialogueAnchorId: null,
    focusedArtifact: null,
    expandedObjectIds: [],
    selectedReplaySessionId: null,
    contextReferences: [],
    sessionSurfaces: {},
    navigatorExpandedSurfaces: [DEFAULT_WOVEN_WORKSPACE_SURFACE],
    migration: {
      sourceKey: null,
      mappedFields: []
    }
  };
}

/**
 * `sessionSurfaces` is deliberately retained here: session ids are globally
 * unique and the map is only ever consulted for sessions the active Working
 * Root actually enumerates, so returning to a previous root keeps its local
 * grouping instead of silently dropping it. `navigatorExpandedSurfaces` is a
 * layout preference, like the pane widths, and is likewise not project-scoped.
 * Titles and rung/declined hints also follow globally unique session IDs across
 * known folders; switching roots must not lose a rename or declined proposal.
 * Pins, groups, archive and local-delete marks are kept for the same reason:
 * chats from every folder share one navigator, and opening a chat in another
 * folder switches the root as a matter of course.
 */
export function clearProjectScopedWovenWorkspaceState(
  state: WovenWorkspaceState
): WovenWorkspaceState {
  return {
    ...state,
    dialogueAnchorId: null,
    focusedArtifact: null,
    expandedObjectIds: [],
    selectedReplaySessionId: null,
    contextReferences: [],
    openDocumentPath: null
  };
}

function sanitizeWovenWorkspaceState(value: unknown): NormalizedWovenWorkspaceState | null {
  if (!isRecord(value) || value.schema !== WOVEN_WORKSPACE_SCHEMA) {
    return null;
  }

  const fallback = createDefaultWovenWorkspaceState();
  return {
    ...readAdditions(value),
    schema: WOVEN_WORKSPACE_SCHEMA,
    theme: readWovenWorkspaceTheme(value.theme),
    navigatorWidth: clampNumber(
      value.navigatorWidth,
      fallback.navigatorWidth,
      MIN_NAVIGATOR_WIDTH
    ),
    coordinationWidth: clampNumber(
      value.coordinationWidth,
      fallback.coordinationWidth,
      240
    ),
    activityHeight: clampNumber(value.activityHeight, fallback.activityHeight, 120),
    navigatorCollapsed: readBoolean(
      value.navigatorCollapsed,
      fallback.navigatorCollapsed
    ),
    coordinationCollapsed: readBoolean(
      value.coordinationCollapsed,
      fallback.coordinationCollapsed
    ),
    activityCollapsed: readBoolean(
      value.activityCollapsed,
      fallback.activityCollapsed
    ),
    coordinationView: readCoordinationView(value.coordinationView),
    dialogueAnchorId: readReference(value.dialogueAnchorId),
    focusedArtifact: readFocusedArtifact(value.focusedArtifact),
    expandedObjectIds: readReferenceArray(value.expandedObjectIds),
    selectedReplaySessionId: readReference(value.selectedReplaySessionId),
    contextReferences: readReferenceArray(value.contextReferences),
    sessionSurfaces: readSessionSurfaces(value.sessionSurfaces),
    navigatorExpandedSurfaces: readNavigatorExpandedSurfaces(
      value.navigatorExpandedSurfaces
    ),
    migration: readMigration(value.migration)
  };
}

function migrateLegacyLayout(raw: string | null): NormalizedWovenWorkspaceState {
  const state = createDefaultWovenWorkspaceState();
  if (!raw) {
    return state;
  }

  try {
    const parsed = JSON.parse(raw) as unknown;
    if (!isRecord(parsed)) {
      return state;
    }

    const widths = isRecord(parsed.widths) ? parsed.widths : {};
    const collapsed = isRecord(parsed.collapsed) ? parsed.collapsed : {};
    const mappedFields: WovenWorkspaceMigrationField[] = [];

    if (typeof widths.fileTree === 'number' && Number.isFinite(widths.fileTree)) {
      state.navigatorWidth = clampNumber(
        widths.fileTree,
        state.navigatorWidth,
        MIN_NAVIGATOR_WIDTH
      );
      mappedFields.push('navigatorWidth');
    }

    if (typeof collapsed.fileTree === 'boolean') {
      state.navigatorCollapsed = collapsed.fileTree;
      mappedFields.push('navigatorCollapsed');
    }

    if (mappedFields.length > 0) {
      state.migration = {
        sourceKey: LEGACY_LAYOUT_STORAGE_KEY,
        mappedFields
      };
    }
    return state;
  } catch {
    return state;
  }
}

export function readWovenWorkspaceStateFromStorage(
  storage: WovenWorkspaceStorage | undefined
): NormalizedWovenWorkspaceState {
  if (!storage) return createDefaultWovenWorkspaceState();
  let state: NormalizedWovenWorkspaceState | null = null;
  let originalCurrent: Record<string, unknown> | null = null;
  let observedRoots = false;
  let safeToPersistRecovery = false;
  try {
    const raw = storage.getItem(WOVEN_WORKSPACE_STORAGE_KEY);
    const parsed: unknown = raw ? JSON.parse(raw) : null;
    state = sanitizeWovenWorkspaceState(parsed);
    if (state && isRecord(parsed)) originalCurrent = parsed;
    safeToPersistRecovery = raw === null || state !== null;
    observedRoots = state !== null && isRecord(parsed) && Object.hasOwn(parsed, 'knownRoots');
  } catch {
    // Each optional storage source fails independently.
  }
  const recovered = state === null;
  if (!state) {
    let legacy: string | null = null;
    try { legacy = storage.getItem(LEGACY_LAYOUT_STORAGE_KEY); } catch { /* optional */ }
    state = migrateLegacyLayout(legacy);
  }
  if (!observedRoots) {
    try {
      const path = readIdentity(storage.getItem('chirality.projectRoot'));
      if (path) state.knownRoots = [{ path, lastUsedAt: new Date().toISOString() }];
    } catch { /* Retain valid current state even when the seed cannot be read. */ }
    // Presence (including []) records the seed decision; its timestamp is the
    // local observation time. Never remove the legacy key or verify the path.
  }
  // Never replace bytes that this reader could not safely interpret.
  if (safeToPersistRecovery && (recovered || !observedRoots)) {
    if (originalCurrent) {
      // A read-time seed changes only this field. Spreading own JSON data also
      // safely preserves opaque __proto__ keys, unknown additions, and legacy
      // values that the in-memory reader may normalize. Explicit writers retain
      // their separate sanitizing contract.
      try {
        storage.setItem(WOVEN_WORKSPACE_STORAGE_KEY, JSON.stringify({
          ...originalCurrent,
          knownRoots: state.knownRoots
        }));
      } catch { /* The normalized in-memory state remains usable. */ }
    } else {
      writeWovenWorkspaceStateToStorage(storage, state);
    }
  }
  return state;
}

type WovenWorkspaceWriteStorage = Pick<Storage, 'setItem'> &
  Partial<Pick<Storage, 'getItem'>>;

function readStoredTheme(
  storage: WovenWorkspaceWriteStorage
): WovenWorkspaceTheme | null {
  if (typeof storage.getItem !== 'function') {
    return null;
  }

  try {
    const raw = storage.getItem(WOVEN_WORKSPACE_STORAGE_KEY);
    if (!raw) {
      return null;
    }
    const parsed = JSON.parse(raw) as unknown;
    if (!isRecord(parsed) || parsed.schema !== WOVEN_WORKSPACE_SCHEMA) {
      return null;
    }
    return readWovenWorkspaceTheme(parsed.theme);
  } catch {
    return null;
  }
}

export function writeWovenWorkspaceStateToStorage(
  storage: WovenWorkspaceWriteStorage | undefined,
  state: WovenWorkspaceState
): void {
  if (!storage) {
    return;
  }

  const sanitized = sanitizeWovenWorkspaceState(state);
  if (!sanitized) {
    return;
  }

  // `theme` is owned by the theme control, not by the surfaces that persist
  // layout state: a caller holding a snapshot taken before the human changed
  // the theme must never write that stale value back. When the storage is
  // readable, the stored theme wins; `writeWovenWorkspaceThemeToStorage` is
  // the one writer that changes it.
  const storedTheme = readStoredTheme(storage);
  const next = storedTheme ? { ...sanitized, theme: storedTheme } : sanitized;

  try {
    storage.setItem(WOVEN_WORKSPACE_STORAGE_KEY, JSON.stringify(next));
  } catch {
    // Workspace presentation state is optional convenience state.
  }
}

export function writeWovenWorkspaceThemeToStorage(
  storage: Pick<Storage, 'getItem' | 'setItem'> | undefined,
  theme: WovenWorkspaceTheme
): void {
  if (!storage) {
    return;
  }

  const current = readWovenWorkspaceStateFromStorage(storage);
  writeWovenWorkspaceStateToStorage(
    { setItem: (key, value) => storage.setItem(key, value) },
    { ...current, theme }
  );
}
