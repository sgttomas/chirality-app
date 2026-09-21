import { describe, expect, it, vi } from 'vitest';
import {
  CHAT_DRAFT_STORAGE_WARNING_CORRUPT,
  CHAT_DRAFT_STORAGE_WARNING_UNAVAILABLE,
  buildChatDraftStorageKey,
  persistChatDraftSnapshotToStorage,
  readChatDraftSnapshotFromStorage,
  sanitizeChatDraftSnapshot
} from '../../lib/harness/chat-draft';

describe('chat draft helpers', () => {
  it('builds a scoped local-storage key', () => {
    expect(
      buildChatDraftStorageKey('/tmp/project', 'WORKING_ITEMS', 'WORKBENCH')
    ).toBe('chirality.chatDraft.v1:/tmp/project:WORKING_ITEMS:WORKBENCH');
  });

  it('sanitizes persisted draft state and attachment records', () => {
    const snapshot = sanitizeChatDraftSnapshot({
      draft: 'continue this turn',
      methods: [],
      attachments: [
        {
          path: '/tmp/example/data.csv',
          displayName: 'data.csv',
          mimeType: 'text/csv',
          clientType: 'csv'
        },
        {
          displayName: 'missing-path'
        }
      ]
    });

    expect(snapshot).toEqual({
      draft: 'continue this turn',
      methods: [],
      attachments: [
        {
          path: '/tmp/example/data.csv',
          displayName: 'data.csv',
          mimeType: 'text/csv',
          clientType: 'csv'
        }
      ]
    });
  });

  it('keeps qualified methods separate from ordinary file attachments', () => {
    expect(sanitizeChatDraftSnapshot({
      draft: 'set up this project',
      attachments: [{ path: '/tmp/example/PROJECT_SETUP.md', displayName: 'PROJECT_SETUP.md', mimeType: 'text/markdown', clientType: 'markdown' }],
      methods: [
        { kind: 'workflow', name: 'project-setup', source: 'bundled', sourceRootId: 'chirality-root' },
        { kind: 'workflow', name: '', source: 'bundled', sourceRootId: 'chirality-root' }
      ]
    })).toEqual({
      draft: 'set up this project',
      attachments: [{ path: '/tmp/example/PROJECT_SETUP.md', displayName: 'PROJECT_SETUP.md', mimeType: 'text/markdown', clientType: 'markdown' }],
      methods: [{ kind: 'workflow', name: 'project-setup', source: 'bundled', sourceRootId: 'chirality-root' }]
    });
  });

  it('reads a valid draft snapshot from local storage', () => {
    const storage = {
      getItem: vi.fn().mockReturnValue(
        JSON.stringify({
          draft: 'resume this turn',
          attachments: [
            {
              path: '/tmp/example/notes.md',
              displayName: 'notes.md',
              mimeType: 'text/markdown',
              clientType: 'markdown'
            }
          ]
        })
      ),
      removeItem: vi.fn()
    };

    const result = readChatDraftSnapshotFromStorage(storage, 'draft-key');

    expect(result).toEqual({
      snapshot: {
        draft: 'resume this turn',
        methods: [],
        attachments: [
          {
            path: '/tmp/example/notes.md',
            displayName: 'notes.md',
            mimeType: 'text/markdown',
            clientType: 'markdown'
          }
        ]
      },
      writable: true,
      warning: null
    });
  });

  it('resets corrupt draft storage payloads and warns once', () => {
    const storage = {
      getItem: vi.fn().mockReturnValue('{not-json'),
      removeItem: vi.fn()
    };

    const result = readChatDraftSnapshotFromStorage(storage, 'draft-key');

    expect(result).toEqual({
      snapshot: {
        draft: '',
        attachments: [],
        methods: []
      },
      writable: true,
      warning: CHAT_DRAFT_STORAGE_WARNING_CORRUPT
    });
    expect(storage.removeItem).toHaveBeenCalledWith('draft-key');
  });

  it('marks storage unavailable when reads throw', () => {
    const storage = {
      getItem: vi.fn(() => {
        throw new Error('localStorage unavailable');
      }),
      removeItem: vi.fn()
    };

    const result = readChatDraftSnapshotFromStorage(storage, 'draft-key');

    expect(result).toEqual({
      snapshot: {
        draft: '',
        attachments: [],
        methods: []
      },
      writable: false,
      warning: CHAT_DRAFT_STORAGE_WARNING_UNAVAILABLE
    });
  });

  it('marks storage unavailable when corrupt payload reset fails', () => {
    const storage = {
      getItem: vi.fn().mockReturnValue('{not-json'),
      removeItem: vi.fn(() => {
        throw new Error('localStorage unavailable');
      })
    };

    const result = readChatDraftSnapshotFromStorage(storage, 'draft-key');

    expect(result).toEqual({
      snapshot: {
        draft: '',
        attachments: [],
        methods: []
      },
      writable: false,
      warning: CHAT_DRAFT_STORAGE_WARNING_UNAVAILABLE
    });
  });

  it('writes non-empty snapshots to local storage', () => {
    const storage = {
      setItem: vi.fn(),
      removeItem: vi.fn()
    };

    const result = persistChatDraftSnapshotToStorage(storage, 'draft-key', {
      draft: 'continue',
      methods: [],
      attachments: [
        {
          path: '/tmp/example/data.csv',
          displayName: 'data.csv',
          mimeType: 'text/csv',
          clientType: 'csv'
        }
      ]
    });

    expect(result).toEqual({
      writable: true,
      warning: null
    });
    expect(storage.setItem).toHaveBeenCalledWith(
      'draft-key',
      JSON.stringify({
        draft: 'continue',
        methods: [],
        attachments: [
          {
            path: '/tmp/example/data.csv',
            displayName: 'data.csv',
            mimeType: 'text/csv',
            clientType: 'csv'
          }
        ]
      })
    );
    expect(storage.removeItem).not.toHaveBeenCalled();
  });

  it('removes empty snapshots from local storage', () => {
    const storage = {
      setItem: vi.fn(),
      removeItem: vi.fn()
    };

    const result = persistChatDraftSnapshotToStorage(storage, 'draft-key', {
      draft: '',
      attachments: [],
      methods: []
    });

    expect(result).toEqual({
      writable: true,
      warning: null
    });
    expect(storage.removeItem).toHaveBeenCalledWith('draft-key');
    expect(storage.setItem).not.toHaveBeenCalled();
  });

  it('round-trips an explicit model/reasoning pair and drops corrupt or partial values', () => {
    const storage = new Map<string, string>();
    const port = {
      getItem: (key: string) => storage.get(key) ?? null,
      setItem: (key: string, value: string) => { storage.set(key, value); },
      removeItem: (key: string) => { storage.delete(key); }
    };
    persistChatDraftSnapshotToStorage(port, 'draft-key', { draft: '', attachments: [], methods: [], model: 'gpt-alt', reasoningEffort: 'low' });
    expect(readChatDraftSnapshotFromStorage(port, 'draft-key').snapshot).toEqual({
      draft: '', attachments: [], methods: [], model: 'gpt-alt', reasoningEffort: 'low'
    });

    expect(sanitizeChatDraftSnapshot({ draft: 'x', model: 'gpt-alt' })).toEqual({ draft: 'x', attachments: [], methods: [] });
    expect(sanitizeChatDraftSnapshot({ draft: 'x', reasoningEffort: 'low' })).toEqual({ draft: 'x', attachments: [], methods: [] });
    expect(sanitizeChatDraftSnapshot({ draft: 'x', model: 'has space', reasoningEffort: 'low' })).toEqual({ draft: 'x', attachments: [], methods: [] });
    expect(sanitizeChatDraftSnapshot({ draft: 'x', model: 'gpt-alt', reasoningEffort: '' })).toEqual({ draft: 'x', attachments: [], methods: [] });
    expect(sanitizeChatDraftSnapshot({ draft: 'x', model: 7, reasoningEffort: 'low' })).toEqual({ draft: 'x', attachments: [], methods: [] });
    expect(sanitizeChatDraftSnapshot({ draft: 'x', model: 'm'.repeat(129), reasoningEffort: 'low' })).toEqual({ draft: 'x', attachments: [], methods: [] });

    // A pair alone is a nonempty snapshot: it is stored, not removed.
    persistChatDraftSnapshotToStorage(port, 'pair-only', { draft: '', attachments: [], methods: [], model: 'gpt-default', reasoningEffort: 'high' });
    expect(storage.has('pair-only')).toBe(true);
    persistChatDraftSnapshotToStorage(port, 'pair-only', { draft: '', attachments: [], methods: [] });
    expect(storage.has('pair-only')).toBe(false);
  });

  it('round-trips unsent per-chat permission and interaction settings and drops unknown values', () => {
    const storage = new Map<string, string>();
    const port = {
      getItem: (key: string) => storage.get(key) ?? null,
      setItem: (key: string, value: string) => { storage.set(key, value); },
      removeItem: (key: string) => { storage.delete(key); }
    };
    persistChatDraftSnapshotToStorage(port, 'session-key', { draft: '', attachments: [], methods: [], permissionMode: 'readOnly', interactionMode: 'native-plan' });
    expect(storage.has('session-key')).toBe(true);
    expect(readChatDraftSnapshotFromStorage(port, 'session-key').snapshot).toEqual({ draft: '', attachments: [], methods: [], permissionMode: 'readOnly', interactionMode: 'native-plan' });
    expect(sanitizeChatDraftSnapshot({ draft: 'x', permissionMode: 'sudo', interactionMode: 'plan' })).toEqual({ draft: 'x', attachments: [], methods: [] });
    expect(sanitizeChatDraftSnapshot({ draft: '', permissionMode: 'ask' })).toEqual({ draft: '', attachments: [], methods: [], permissionMode: 'ask' });
  });

  it('marks storage unavailable when write operations fail', () => {
    const storage = {
      setItem: vi.fn(() => {
        throw new Error('quota exceeded');
      }),
      removeItem: vi.fn()
    };

    const result = persistChatDraftSnapshotToStorage(storage, 'draft-key', {
      draft: 'continue',
      attachments: [],
      methods: []
    });

    expect(result).toEqual({
      writable: false,
      warning: CHAT_DRAFT_STORAGE_WARNING_UNAVAILABLE
    });
  });
});
