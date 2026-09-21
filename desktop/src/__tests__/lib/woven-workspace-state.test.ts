import { describe, expect, it, vi } from 'vitest';
import {
  MAX_SESSION_SURFACE_ATTRIBUTIONS,
  WOVEN_WORKSPACE_SCHEMA,
  WOVEN_WORKSPACE_STORAGE_KEY,
  clearProjectScopedWovenWorkspaceState,
  createDefaultWovenWorkspaceState,
  readWovenWorkspaceStateFromStorage,
  recordWovenSessionSurface,
  toggleWovenNavigatorExpandedSurface,
  writeWovenWorkspaceStateToStorage,
  writeWovenWorkspaceThemeToStorage
} from '../../lib/woven-dialogue/woven-workspace-state';

describe('Woven Dialogue workspace state', () => {
  it('clears project references without changing global layout preferences', () => {
    const state = {
      ...createDefaultWovenWorkspaceState(),
      navigatorWidth: 412,
      coordinationView: 'agents' as const,
      dialogueAnchorId: 'turn-1',
      focusedArtifact: {
        artifactReference: 'project-a/report.md',
        dialogueAnchorId: 'turn-1'
      },
      expandedObjectIds: ['project-a/report.md'],
      selectedReplaySessionId: 'session-a',
      contextReferences: ['project-a/context.md']
    };

    expect(clearProjectScopedWovenWorkspaceState(state)).toMatchObject({
      navigatorWidth: 412,
      coordinationView: 'agents',
      dialogueAnchorId: null,
      focusedArtifact: null,
      expandedObjectIds: [],
      selectedReplaySessionId: null,
      contextReferences: []
    });
  });

  it('creates reference-only defaults for the new versioned schema', () => {
    expect(createDefaultWovenWorkspaceState()).toEqual({
      rightPanelView: 'files', rightPanelWidths: {}, rightPanelExpanded: false,
      preExpandState: null, openDocumentPath: null, chatTitles: {}, chatPins: [],
      chatArchived: [], chatDeleted: [], chatGroups: [], groupsCollapsed: [], knownRoots: [], chatRung: {},
      chatIndex: {}, foldersCollapsed: [], chatDocuments: {}, lastActiveChat: null,
      schema: WOVEN_WORKSPACE_SCHEMA,
      theme: 'light',
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
      navigatorExpandedSurfaces: ['dialogue'],
      migration: {
        sourceKey: null,
        mappedFields: []
      }
    });
  });

  it('migrates only legacy file-tree geometry and leaves the legacy key untouched', () => {
    const legacyRaw = JSON.stringify({
      widths: {
        fileTree: 432,
        toolkit: 901,
        chat: 902
      },
      collapsed: {
        fileTree: true,
        toolkit: true,
        chat: true
      },
      authoritativePlan: {
        status: 'ACCEPTED'
      }
    });
    const setItem = vi.fn();
    const storage = {
      getItem: vi.fn((key: string) =>
        key === 'chirality.layout.v1' ? legacyRaw : null
      ),
      setItem
    };

    const state = readWovenWorkspaceStateFromStorage(storage);

    expect(state.navigatorWidth).toBe(432);
    expect(state.navigatorCollapsed).toBe(true);
    expect(state.coordinationWidth).toBe(360);
    expect(state.coordinationCollapsed).toBe(false);
    expect(state.activityHeight).toBe(220);
    expect(state.activityCollapsed).toBe(true);
    expect(state.migration).toEqual({
      sourceKey: 'chirality.layout.v1',
      mappedFields: ['navigatorWidth', 'navigatorCollapsed']
    });
    expect(state).not.toHaveProperty('authoritativePlan');
    expect(setItem).toHaveBeenCalledTimes(1);
    expect(setItem).toHaveBeenCalledWith(
      WOVEN_WORKSPACE_STORAGE_KEY,
      JSON.stringify(state)
    );
    expect(storage.getItem('chirality.layout.v1')).toBe(legacyRaw);
  });

  it('reads and sanitizes a current workspace state without rerunning migration', () => {
    const current = {
      ...createDefaultWovenWorkspaceState(),
      navigatorWidth: 510,
      coordinationView: 'agents',
      dialogueAnchorId: ' turn-17 ',
      expandedObjectIds: ['artifact-1', 'artifact-1', '', 42],
      contextReferences: [' docs/SPEC.md ', 'docs/SPEC.md'],
      selectedReplaySessionId: ' session-2 '
    };
    const storage = {
      getItem: vi.fn((key: string) =>
        key === WOVEN_WORKSPACE_STORAGE_KEY ? JSON.stringify(current) : null
      ),
      setItem: vi.fn()
    };

    const state = readWovenWorkspaceStateFromStorage(storage);

    expect(state.navigatorWidth).toBe(510);
    expect(state.coordinationView).toBe('agents');
    expect(state.dialogueAnchorId).toBe('turn-17');
    expect(state.expandedObjectIds).toEqual(['artifact-1']);
    expect(state.contextReferences).toEqual(['docs/SPEC.md']);
    expect(state.selectedReplaySessionId).toBe('session-2');
    expect(storage.setItem).not.toHaveBeenCalled();
    expect(storage.getItem).not.toHaveBeenCalledWith('chirality.layout.v1');
  });

  it('recovers from corrupt current and legacy state without throwing', () => {
    const storage = {
      getItem: vi.fn((key: string) =>
        key === WOVEN_WORKSPACE_STORAGE_KEY ? '{bad-current' : key === 'chirality.layout.v1' ? '{bad-legacy' : null
      ),
      setItem: vi.fn()
    };

    expect(readWovenWorkspaceStateFromStorage(storage)).toEqual(
      createDefaultWovenWorkspaceState()
    );
    expect(storage.setItem).not.toHaveBeenCalled();
  });

  it('falls back to memory defaults when storage access fails', () => {
    const storage = {
      getItem: vi.fn(() => {
        throw new Error('storage unavailable');
      }),
      setItem: vi.fn()
    };

    expect(readWovenWorkspaceStateFromStorage(storage)).toEqual(
      createDefaultWovenWorkspaceState()
    );
    expect(storage.setItem).not.toHaveBeenCalled();
  });

  it('writes only the new key and ignores write failures', () => {
    const state = {
      ...createDefaultWovenWorkspaceState(),
      coordinationView: 'agents' as const,
      contextReferences: ['docs/SPEC.md']
    };
    const setItem = vi.fn();

    expect(() =>
      writeWovenWorkspaceStateToStorage({ setItem }, state)
    ).not.toThrow();
    expect(setItem).toHaveBeenCalledWith(
      WOVEN_WORKSPACE_STORAGE_KEY,
      JSON.stringify(state)
    );
    expect(setItem).not.toHaveBeenCalledWith(
      'chirality.layout.v1',
      expect.anything()
    );

    expect(() =>
      writeWovenWorkspaceStateToStorage(
        {
          setItem: () => {
            throw new Error('quota exceeded');
          }
        },
        state
      )
    ).not.toThrow();
  });
  it('defaults the theme to light and keeps stored v1 blobs loadable', () => {
    const legacyBlob = {
      ...createDefaultWovenWorkspaceState(),
      navigatorWidth: 340
    } as Record<string, unknown>;
    delete legacyBlob.theme;

    const storage = {
      getItem: vi.fn((key: string) =>
        key === WOVEN_WORKSPACE_STORAGE_KEY ? JSON.stringify(legacyBlob) : null
      ),
      setItem: vi.fn()
    };

    const state = readWovenWorkspaceStateFromStorage(storage);

    expect(state.theme).toBe('light');
    expect(state.navigatorWidth).toBe(340);
    expect(state.schema).toBe(WOVEN_WORKSPACE_SCHEMA);
  });

  it('falls back to light for an unrecognised stored theme', () => {
    const storage = {
      getItem: vi.fn((key: string) =>
        key === WOVEN_WORKSPACE_STORAGE_KEY
          ? JSON.stringify({ ...createDefaultWovenWorkspaceState(), theme: 'sepia' })
          : null
      ),
      setItem: vi.fn()
    };

    expect(readWovenWorkspaceStateFromStorage(storage).theme).toBe('light');
  });

  it('persists a chosen theme without bumping the schema string', () => {
    const store = new Map<string, string>();
    const storage = {
      getItem: (key: string) => store.get(key) ?? null,
      setItem: (key: string, value: string) => {
        store.set(key, value);
      }
    };

    writeWovenWorkspaceThemeToStorage(storage, 'dark');

    const persisted = JSON.parse(
      store.get(WOVEN_WORKSPACE_STORAGE_KEY) as string
    ) as Record<string, unknown>;
    expect(persisted.theme).toBe('dark');
    expect(persisted.schema).toBe(WOVEN_WORKSPACE_SCHEMA);
    expect(readWovenWorkspaceStateFromStorage(storage).theme).toBe('dark');
  });

  it('keeps stored v1 blobs loadable when the navigator fields are absent', () => {
    const legacyBlob = {
      ...createDefaultWovenWorkspaceState(),
      navigatorWidth: 340
    } as Record<string, unknown>;
    delete legacyBlob.sessionSurfaces;
    delete legacyBlob.navigatorExpandedSurfaces;

    const storage = {
      getItem: vi.fn((key: string) =>
        key === WOVEN_WORKSPACE_STORAGE_KEY ? JSON.stringify(legacyBlob) : null
      ),
      setItem: vi.fn()
    };

    const state = readWovenWorkspaceStateFromStorage(storage);

    expect(state.schema).toBe(WOVEN_WORKSPACE_SCHEMA);
    expect(state.sessionSurfaces).toEqual({});
    expect(state.navigatorExpandedSurfaces).toEqual(['dialogue']);
    expect(state.navigatorWidth).toBe(340);
  });

  it('drops unrecognised session attributions and keeps an empty expansion set', () => {
    const stored = {
      ...createDefaultWovenWorkspaceState(),
      sessionSurfaces: {
        'session-a': 'workbench',
        'session-b': 'document',
        'session-c': 42,
        '   ': 'dialogue'
      },
      navigatorExpandedSurfaces: ['pipeline', 'pipeline', 'document', 7]
    };
    const storage = {
      getItem: vi.fn((key: string) =>
        key === WOVEN_WORKSPACE_STORAGE_KEY ? JSON.stringify(stored) : null
      ),
      setItem: vi.fn()
    };

    const state = readWovenWorkspaceStateFromStorage(storage);

    expect(state.sessionSurfaces).toEqual({ 'session-a': 'workbench' });
    expect(state.navigatorExpandedSurfaces).toEqual(['pipeline']);

    const collapsed = readWovenWorkspaceStateFromStorage({
      getItem: vi.fn((key: string) =>
        key === WOVEN_WORKSPACE_STORAGE_KEY
          ? JSON.stringify({
              ...createDefaultWovenWorkspaceState(),
              navigatorExpandedSurfaces: []
            })
          : null
      ),
      setItem: vi.fn()
    });

    expect(collapsed.navigatorExpandedSurfaces).toEqual([]);
  });

  it('records the first surface a session was observed on and never retags it', () => {
    const state = createDefaultWovenWorkspaceState();

    const tagged = recordWovenSessionSurface(state, ' session-a ', 'pipeline');
    expect(tagged.sessionSurfaces).toEqual({ 'session-a': 'pipeline' });

    const retagged = recordWovenSessionSurface(tagged, 'session-a', 'dialogue');
    expect(retagged).toBe(tagged);

    expect(recordWovenSessionSurface(state, '   ', 'dialogue')).toBe(state);
    expect(recordWovenSessionSurface(state, undefined, 'dialogue')).toBe(state);
  });

  it('evicts the oldest attributions beyond the bounded map size', () => {
    let state = createDefaultWovenWorkspaceState();
    for (let index = 0; index < MAX_SESSION_SURFACE_ATTRIBUTIONS + 3; index += 1) {
      state = recordWovenSessionSurface(state, `session-${index}`, 'dialogue');
    }

    const sessionIds = Object.keys(state.sessionSurfaces);
    expect(sessionIds).toHaveLength(MAX_SESSION_SURFACE_ATTRIBUTIONS);
    expect(sessionIds).not.toContain('session-0');
    expect(sessionIds).not.toContain('session-2');
    expect(sessionIds[0]).toBe('session-3');
    expect(sessionIds[sessionIds.length - 1]).toBe(
      `session-${MAX_SESSION_SURFACE_ATTRIBUTIONS + 2}`
    );
  });

  it('round-trips the navigator fields through storage without a schema bump', () => {
    const store = new Map<string, string>();
    const storage = {
      getItem: (key: string) => store.get(key) ?? null,
      setItem: (key: string, value: string) => {
        store.set(key, value);
      }
    };
    const state = recordWovenSessionSurface(
      {
        ...createDefaultWovenWorkspaceState(),
        navigatorExpandedSurfaces: ['workbench']
      },
      'session-a',
      'workbench'
    );

    writeWovenWorkspaceStateToStorage(storage, state);
    const persisted = JSON.parse(
      store.get(WOVEN_WORKSPACE_STORAGE_KEY) as string
    ) as Record<string, unknown>;

    expect(persisted.schema).toBe(WOVEN_WORKSPACE_SCHEMA);
    expect(persisted.sessionSurfaces).toEqual({ 'session-a': 'workbench' });
    expect(readWovenWorkspaceStateFromStorage(storage)).toEqual(state);
  });

  it('toggles a navigator mode group without disturbing the others', () => {
    const state = createDefaultWovenWorkspaceState();

    const expanded = toggleWovenNavigatorExpandedSurface(state, 'pipeline');
    expect(expanded.navigatorExpandedSurfaces).toEqual(['dialogue', 'pipeline']);

    const collapsed = toggleWovenNavigatorExpandedSurface(expanded, 'dialogue');
    expect(collapsed.navigatorExpandedSurfaces).toEqual(['pipeline']);
  });

  it('keeps session attributions when project-scoped references are cleared', () => {
    const state = recordWovenSessionSurface(
      createDefaultWovenWorkspaceState(),
      'session-a',
      'workbench'
    );

    expect(clearProjectScopedWovenWorkspaceState(state)).toMatchObject({
      sessionSurfaces: { 'session-a': 'workbench' },
      navigatorExpandedSurfaces: ['dialogue'],
      selectedReplaySessionId: null
    });
  });

  it('never lets a stale layout snapshot revert the stored theme', () => {
    const store = new Map<string, string>();
    const storage = {
      getItem: (key: string) => store.get(key) ?? null,
      setItem: (key: string, value: string) => {
        store.set(key, value);
      }
    };
    const staleSnapshot = createDefaultWovenWorkspaceState();

    writeWovenWorkspaceThemeToStorage(storage, 'system');
    writeWovenWorkspaceStateToStorage(storage, {
      ...staleSnapshot,
      navigatorWidth: 300
    });

    const persisted = JSON.parse(
      store.get(WOVEN_WORKSPACE_STORAGE_KEY) as string
    ) as Record<string, unknown>;
    expect(persisted.theme).toBe('system');
    expect(persisted.navigatorWidth).toBe(300);
  });
});


describe('additive shell convenience fields', () => {
  function storageFor(value: Record<string, unknown>, root: string | null = null) {
    const values = new Map<string, string>([[WOVEN_WORKSPACE_STORAGE_KEY, JSON.stringify({ schema: WOVEN_WORKSPACE_SCHEMA, ...value })]]);
    if (root !== null) values.set('chirality.projectRoot', root);
    return {
      values,
      getItem: vi.fn((key: string) => values.get(key) ?? null),
      setItem: vi.fn((key: string, value: string) => { values.set(key, value); })
    };
  }
  const read = (value: Record<string, unknown>) => readWovenWorkspaceStateFromStorage(storageFor(value));

  it('maps an absent view from old v1 and treats invalid-present as an explicit default', () => {
    expect(read({ coordinationView: 'agents' }).rightPanelView).toBe('agents');
    expect(read({ coordinationView: 'agents', rightPanelView: null }).rightPanelView).toBe('files');
    for (const rightPanelView of ['files', 'plan', 'workflows', 'skills', 'agents', 'activity', 'settings']) {
      expect(read({ coordinationView: 'agents', rightPanelView }).rightPanelView).toBe(rightPanelView === 'skills' ? 'workflows' : rightPanelView);
    }
    expect(read({ rightPanelWidths: { files: 0, document: 5000, agents: 320, workflows: 480, activity: -1, session: 320.5, settings: '400', nope: 400 } }).rightPanelWidths)
      .toEqual({ files: 280, document: 2000, agents: 320, workflows: 480, activity: 280, session: 320.5 });
    expect(read({ rightPanelWidths: { files: Infinity, document: NaN } }).rightPanelWidths).toEqual({});
    expect(read({ preExpandState: { rightWidth: 20, leftCollapsed: true } }).preExpandState).toEqual({ rightWidth: 280, leftCollapsed: true });
    expect(read({ preExpandState: { rightWidth: 300 }, rightPanelExpanded: 1 }).preExpandState).toBeNull();
    expect(read({ rightPanelExpanded: 1 }).rightPanelExpanded).toBe(false);
  });

  it('rejects oversized/invalid new identities while leaving legacy trimming and truncation intact', () => {
    const oversized = 'x'.repeat(2049), valid = 'x'.repeat(2048);
    const state = read({ openDocumentPath: ' /a/file.md ', chatPins: [' a ', ' a ', '', oversized, '\u0000', valid],
      dialogueAnchorId: oversized, contextReferences: [' a ', oversized], chatTitles: { ' a ': ' Title ', [oversized]: 'bad' } });
    expect(state.openDocumentPath).toBe(' /a/file.md ');
    expect(state.chatPins).toEqual([' a ', valid]);
    expect(state.chatTitles).toEqual({ ' a ': 'Title' });
    expect(state.dialogueAnchorId).toBe(valid);
    expect(state.contextReferences).toEqual(['a', valid]);
    expect(read({ openDocumentPath: oversized }).openDocumentPath).toBeNull();
  });

  it('roundtrips opaque special map/group/root keys as own data', () => {
    const titles = JSON.parse('{"__proto__":"Title","constructor":"Other"}');
    const rungs = JSON.parse('{"__proto__":{"kind":"workflow","ref":" path "},"constructor":{"kind":"plain","declined":[" x "]}}');
    const storage = storageFor({ chatTitles: titles, chatRung: rungs, chatGroups: [{ id: '__proto__', name: ' Group ', sessionIds: ['constructor'] }],
      knownRoots: [{ path: '__proto__', lastUsedAt: '2026-09-05T00:00:00Z' }] });
    const state = readWovenWorkspaceStateFromStorage(storage);
    expect(Object.hasOwn(state.chatTitles, '__proto__')).toBe(true);
    expect(state.chatTitles.__proto__).toBe('Title');
    expect(state.chatRung.constructor).toEqual({ kind: 'plain', declined: [' x '] });
    expect(Object.getPrototypeOf(state.chatTitles)).toBe(Object.prototype);
    expect(state.chatGroups[0]).toEqual({ id: '__proto__', name: 'Group', sessionIds: ['constructor'] });
    writeWovenWorkspaceStateToStorage(storage, state);
    expect(readWovenWorkspaceStateFromStorage(storage)).toEqual(state);
    expect(({} as Record<string, unknown>).polluted).toBeUndefined();
  });

  it('bounds collections, evicts old map entries, and drops malformed entries', () => {
    const ids = Array.from({ length: 505 }, (_, i) => `s-${i}`);
    const state = read({ chatPins: ids, chatArchived: ids, chatDeleted: ids, groupsCollapsed: ids,
      chatTitles: Object.fromEntries(ids.map(id => [id, id])),
      chatRung: { ...Object.fromEntries(ids.map(id => [id, { kind: 'spec', declined: ids }])), bad: { kind: 'invalid' } },
      chatGroups: [null, { id: '', name: 'bad' }, ...ids.map(id => ({ id, name: id, sessionIds: ids }))] });
    expect(Object.keys(state.chatTitles)).toHaveLength(500);
    expect(Object.hasOwn(state.chatTitles, 's-4')).toBe(false);
    expect(Object.keys(state.chatRung)).toHaveLength(500);
    for (const collection of [state.chatPins, state.chatArchived, state.chatDeleted, state.groupsCollapsed, state.chatGroups, state.chatRung['s-5'].declined, state.chatGroups[0].sessionIds]) expect(collection).toHaveLength(200);
    expect(read({ chatRung: { x: { kind: 'workflow', ref: 'x'.repeat(2049), declined: [null] } }, chatTitles: [], chatGroups: [{ id: 'a', name: ' A ' }, { id: 'a', name: 'B' }] }))
      .toMatchObject({ chatRung: { x: { kind: 'workflow', declined: [] } }, chatTitles: {}, chatGroups: [{ id: 'a', name: 'A', sessionIds: [] }] });
  });

  it('validates ISO root instants, deduplicates newest, sorts and caps roots', () => {
    const roots = Array.from({ length: 52 }, (_, i) => ({ path: `/p/${i}`, lastUsedAt: new Date(Date.UTC(2026, 0, i + 1)).toISOString() }));
    const state = read({ knownRoots: [...roots, { path: '/p/0', lastUsedAt: '2026-09-05T02:00:00+02:00' },
      { path: '/bad', lastUsedAt: '2026-02-30T00:00:00Z' }, { path: '/bad2', lastUsedAt: 'yesterday' }, { path: '/bad3', lastUsedAt: '2026-09-05' }] });
    expect(state.knownRoots).toHaveLength(50);
    expect(state.knownRoots[0]).toEqual({ path: '/p/0', lastUsedAt: '2026-09-05T00:00:00.000Z' });
    expect(state.knownRoots.some(root => root.path.startsWith('/bad'))).toBe(false);
    expect(state.knownRoots.filter(root => root.path === '/p/0')).toHaveLength(1);
  });

  it('seeds only absent roots once, retaining the old key and observation timestamp', () => {
    const storage = storageFor({ theme: 'dark', coordinationView: 'agents' }, ' /old/root ');
    const before = Date.now();
    const state = readWovenWorkspaceStateFromStorage(storage);
    expect(state.knownRoots[0].path).toBe(' /old/root ');
    expect(Date.parse(state.knownRoots[0].lastUsedAt)).toBeGreaterThanOrEqual(before);
    storage.values.set('chirality.projectRoot', '/changed');
    expect(readWovenWorkspaceStateFromStorage(storage)).toEqual(state);
    expect(storage.values.get('chirality.projectRoot')).toBe('/changed');
    expect(storage.getItem.mock.calls.filter(([key]) => key === 'chirality.projectRoot')).toHaveLength(1);
    for (const knownRoots of [[], null, 'bad', [{ path: '/bad' }]]) {
      const explicit = storageFor({ knownRoots }, '/old');
      expect(readWovenWorkspaceStateFromStorage(explicit).knownRoots).toEqual([]);
      expect(explicit.getItem.mock.calls.some(([key]) => key === 'chirality.projectRoot')).toBe(false);
    }
    const noSeed = storageFor({});
    readWovenWorkspaceStateFromStorage(noSeed);
    noSeed.values.set('chirality.projectRoot', '/later');
    expect(readWovenWorkspaceStateFromStorage(noSeed).knownRoots).toEqual([]);
  });

  it('isolates seed and write failures from valid current state', () => {
    const storage = storageFor({ theme: 'dark', navigatorWidth: 500 });
    storage.getItem.mockImplementation(key => { if (key === 'chirality.projectRoot') throw new Error('denied'); return storage.values.get(key) ?? null; });
    storage.setItem.mockImplementation(() => { throw new Error('quota'); });
    expect(readWovenWorkspaceStateFromStorage(storage)).toMatchObject({ theme: 'dark', navigatorWidth: 500, knownRoots: [] });
  });

  it('clears project hints while retaining chat organisation and app state, and excludes activeChatRoot', () => {
    const storage = storageFor({ openDocumentPath: '/doc', chatTitles: { s: 'Title' }, chatPins: ['s'], chatArchived: ['s'], chatDeleted: ['s'], chatRung: { s: { kind: 'plain' } }, chatGroups: [{ id: 'g', name: 'G', sessionIds: ['s'] }], groupsCollapsed: ['g'],
      knownRoots: [{ path: '/root', lastUsedAt: '2026-09-05T00:00:00Z' }], rightPanelView: 'workflows', rightPanelWidths: { workflows: 460 }, rightPanelExpanded: true, preExpandState: { rightWidth: 400, leftCollapsed: true }, theme: 'dark', sessionSurfaces: { s: 'dialogue' }, activeChatRoot: '/authority' });
    const state = readWovenWorkspaceStateFromStorage(storage);
    const cleared = clearProjectScopedWovenWorkspaceState(state);
    expect(cleared).toMatchObject({ openDocumentPath: null, chatTitles: state.chatTitles, chatPins: ['s'], chatArchived: ['s'], chatDeleted: ['s'], chatRung: state.chatRung, chatGroups: state.chatGroups, groupsCollapsed: ['g'], knownRoots: state.knownRoots, rightPanelView: 'workflows', rightPanelWidths: { workflows: 460 }, rightPanelExpanded: true, preExpandState: state.preExpandState, theme: 'dark', sessionSurfaces: { s: 'dialogue' } });
    writeWovenWorkspaceStateToStorage(storage, { ...state, activeChatRoot: '/forbidden' } as typeof state);
    expect(JSON.parse(storage.values.get(WOVEN_WORKSPACE_STORAGE_KEY)!)).not.toHaveProperty('activeChatRoot');
    writeWovenWorkspaceThemeToStorage(storage, 'light');
    expect(readWovenWorkspaceStateFromStorage(storage)).toEqual({ ...state, theme: 'light' });
  });
});


it('does not overwrite an unreadable primary blob when legacy storage remains readable', () => {
  const values = new Map([[WOVEN_WORKSPACE_STORAGE_KEY, '{"schema":"chirality.woven-workspace/v1","theme":"dark"}'], ['chirality.projectRoot', '/old']]);
  const original = values.get(WOVEN_WORKSPACE_STORAGE_KEY);
  const storage = {
    getItem: (key: string) => { if (key === WOVEN_WORKSPACE_STORAGE_KEY) throw new Error('primary unavailable'); return values.get(key) ?? null; },
    setItem: vi.fn((key: string, value: string) => { values.set(key, value); })
  };
  expect(() => readWovenWorkspaceStateFromStorage(storage)).not.toThrow();
  expect(storage.setItem).not.toHaveBeenCalled();
  expect(values.get(WOVEN_WORKSPACE_STORAGE_KEY)).toBe(original);
});


it.each(['{broken-json', '', JSON.stringify({ schema: 'chirality.woven-workspace/v2', theme: 'dark', future: true })])(
  'preserves uninterpretable current bytes during read-time recovery: %s', raw => {
    const values = new Map([[WOVEN_WORKSPACE_STORAGE_KEY, raw], ['chirality.projectRoot', '/legacy']]);
    const storage = { getItem: (key: string) => values.get(key) ?? null,
      setItem: vi.fn((key: string, value: string) => { values.set(key, value); }) };
    expect(readWovenWorkspaceStateFromStorage(storage).knownRoots[0].path).toBe('/legacy');
    expect(storage.setItem).not.toHaveBeenCalled();
    expect(values.get(WOVEN_WORKSPACE_STORAGE_KEY)).toBe(raw);
  }
);


it('persists only the root seed into readable v1 without normalizing or dropping existing own data', () => {
  const original = JSON.parse('{"schema":"chirality.woven-workspace/v1","theme":"future-theme","navigatorWidth":2,"contextReferences":[" padded ",null],"dialogueAnchorId":" anchor ","future":{"nested":[1,true,null]},"__proto__":{"opaque":true},"constructor":"opaque-constructor","activeChatRoot":"/existing-raw-hint"}');
  const values = new Map([[WOVEN_WORKSPACE_STORAGE_KEY, JSON.stringify(original)], ['chirality.projectRoot', ' /seed ']]);
  const storage = { getItem: (key: string) => values.get(key) ?? null,
    setItem: vi.fn((key: string, value: string) => { values.set(key, value); }) };
  const state = readWovenWorkspaceStateFromStorage(storage);
  expect(state).toMatchObject({ theme: 'light', navigatorWidth: 220, contextReferences: ['padded'], dialogueAnchorId: 'anchor' });
  const persisted = JSON.parse(values.get(WOVEN_WORKSPACE_STORAGE_KEY)!);
  expect(persisted.knownRoots).toEqual(state.knownRoots);
  expect(state).not.toHaveProperty('activeChatRoot');
  expect(persisted.activeChatRoot).toBe('/existing-raw-hint');
  delete persisted.knownRoots;
  expect(persisted).toEqual(original);
  expect(Object.hasOwn(persisted, '__proto__')).toBe(true);
  expect(persisted.__proto__).toEqual({ opaque: true });
  expect(Object.getPrototypeOf(persisted)).toBe(Object.prototype);
  expect(storage.setItem).toHaveBeenCalledTimes(1);

  values.set(WOVEN_WORKSPACE_STORAGE_KEY, JSON.stringify(original));
  storage.setItem.mockImplementation(() => { throw new Error('quota'); });
  expect(readWovenWorkspaceStateFromStorage(storage).knownRoots[0].path).toBe(' /seed ');
  expect(JSON.parse(values.get(WOVEN_WORKSPACE_STORAGE_KEY)!)).toEqual(original);
});


it('retains titles and rung/declined hints for sessions in two roots across root switches', () => {
  const storageValues = new Map<string, string>();
  const storage = { getItem: (key: string) => storageValues.get(key) ?? null,
    setItem: (key: string, value: string) => { storageValues.set(key, value); } };
  const state = {
    ...createDefaultWovenWorkspaceState(),
    knownRoots: [
      { path: '/root-a', lastUsedAt: '2026-09-05T00:00:00.000Z' },
      { path: '/root-b', lastUsedAt: '2026-09-04T00:00:00.000Z' }
    ],
    chatTitles: { 'session-in-a': 'A renamed chat', 'session-in-b': 'B renamed chat' },
    chatRung: {
      'session-in-a': { kind: 'workflow' as const, ref: '/root-a/workflow.md', declined: ['proposal-a'] },
      'session-in-b': { kind: 'spec' as const, declined: ['proposal-b'] }
    },
    openDocumentPath: '/root-a/doc.md', chatPins: ['session-in-a'],
    chatArchived: ['session-in-a'], chatDeleted: ['session-in-b'], chatGroups: [{ id: 'group-a', name: 'A', sessionIds: ['session-in-a'] }],
    groupsCollapsed: ['group-a'], dialogueAnchorId: 'turn-a', contextReferences: ['/root-a/context.md']
  };
  const inRootB = clearProjectScopedWovenWorkspaceState(state);
  // Chats from every folder share one navigator, so pins, groups and
  // archive/delete marks (globally unique session ids) survive a root switch.
  expect(inRootB).toMatchObject({ chatTitles: state.chatTitles, chatRung: state.chatRung,
    knownRoots: state.knownRoots, openDocumentPath: null, chatPins: state.chatPins, chatArchived: state.chatArchived, chatDeleted: state.chatDeleted,
    chatGroups: state.chatGroups, groupsCollapsed: state.groupsCollapsed, dialogueAnchorId: null, contextReferences: [] });
  writeWovenWorkspaceStateToStorage(storage, inRootB);
  const backInRootA = clearProjectScopedWovenWorkspaceState(readWovenWorkspaceStateFromStorage(storage));
  expect(backInRootA.chatTitles).toEqual(state.chatTitles);
  expect(backInRootA.chatRung).toEqual(state.chatRung);
});

describe('chat index', () => {
  it('indexes listed chats per folder, drops stale entries for that folder only, and keeps identity when unchanged', async () => {
    const { indexWovenChats, createDefaultWovenWorkspaceState: defaults } = await import('../../lib/woven-dialogue/woven-workspace-state');
    const base = defaults();
    const a1 = indexWovenChats(base, '/root-a', [{ sessionId: 's1', projectRoot: '/root-a', persona: 'TASK', createdAt: '2026-09-01T00:00:00Z', updatedAt: '2026-09-02T00:00:00Z' }]);
    expect(a1.chatIndex).toEqual({ s1: { projectRoot: '/root-a', persona: 'TASK', createdAt: '2026-09-01T00:00:00Z', updatedAt: '2026-09-02T00:00:00Z' } });
    const b1 = indexWovenChats(a1, '/root-b', [{ sessionId: 's2', projectRoot: '/root-b', createdAt: '2026-09-03T00:00:00Z', updatedAt: '2026-09-03T00:00:00Z' }]);
    expect(Object.keys(b1.chatIndex ?? {})).toEqual(['s2', 's1']);
    // Re-listing folder A without s1 removes only s1; s2 (folder B) stays.
    const a2 = indexWovenChats(b1, '/root-a', []);
    expect(a2.chatIndex).toEqual({ s2: b1.chatIndex!.s2 });
    // Same listing again is a no-op with the same reference.
    expect(indexWovenChats(a2, '/root-b', [{ sessionId: 's2', projectRoot: '/root-b', createdAt: '2026-09-03T00:00:00Z', updatedAt: '2026-09-03T00:00:00Z' }])).toBe(a2);
  });

  it('reads and persists the additive chat fields and rejects malformed entries', () => {
    const storageFor = (value: Record<string, unknown>) => {
      const values = new Map<string, string>([[WOVEN_WORKSPACE_STORAGE_KEY, JSON.stringify({ schema: WOVEN_WORKSPACE_SCHEMA, ...value })]]);
      return { getItem: (key: string) => values.get(key) ?? null, setItem: (key: string, item: string) => { values.set(key, item); } };
    };
    const storage = storageFor({ chatIndex: { ok: { projectRoot: '/r', createdAt: 'c', updatedAt: 'u', persona: 'TASK' }, bad: { projectRoot: '' }, worse: 'nope' },
      foldersCollapsed: ['/r', 7], chatDocuments: { ok: 'docs/a.md', bad: 3 }, lastActiveChat: { sessionId: 'ok', projectRoot: '/r' } });
    const state = readWovenWorkspaceStateFromStorage(storage);
    expect(state.chatIndex).toEqual({ ok: { projectRoot: '/r', createdAt: 'c', updatedAt: 'u', persona: 'TASK' } });
    expect(state.foldersCollapsed).toEqual(['/r']);
    expect(state.chatDocuments).toEqual({ ok: 'docs/a.md' });
    expect(state.lastActiveChat).toEqual({ sessionId: 'ok', projectRoot: '/r' });
    expect(readWovenWorkspaceStateFromStorage(storageFor({ lastActiveChat: { sessionId: 'x' } })).lastActiveChat).toBeNull();
  });
});
