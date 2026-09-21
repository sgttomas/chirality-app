import { afterEach, describe, expect, it, vi } from 'vitest';
import type { SessionRecord } from '@chirality/runtime-contracts/types';
import type { SelectedSessionReplayLoader } from '../../lib/woven-dialogue/selected-session-replay';
import type { ReplayDisclosure, SelectedSessionReplayProjection } from '../../lib/woven-dialogue/contracts';
import {
  CHAT_MESSAGE_SEARCH_LIMIT,
  CHAT_REPLAY_WORKER_LIMIT,
  COMPLETE_REPLAY_ITEM_LIMIT,
  createChatReplayReader,
  deriveChatTitle,
  loadRecordedFirstOperatorMessages,
  projectChatSections,
  sanitizeChatLabel,
  searchRecordedSessionMessages,
  trimChatTitle,
  visibleActiveChatSessions
} from '../../lib/woven-dialogue/chat-organization';
import { WOVEN_WORKSPACE_SCHEMA } from '../../lib/woven-dialogue/woven-workspace-state';

function session(sessionId: string, updatedAt: string, persona = 'TASK', projectRoot = `/roots/${sessionId}`): SessionRecord {
  return { sessionId, projectRoot, persona, mode: 'CHAT', createdAt: updatedAt, updatedAt };
}

function loaderFor(sessionId: string, disclosure: ReplayDisclosure = 'READY_SNAPSHOT', text = `message ${sessionId}`): SelectedSessionReplayLoader {
  const projection: SelectedSessionReplayProjection = { selectedSessionId: sessionId, sourceReference: `session:${sessionId}/events`, observedAt: '2026-09-07T00:00:00Z', disclosure, currency: disclosure === 'CONFLICTING' ? 'CONFLICTING' : 'CURRENT', transcript: { sessionId, itemCount: 1, items: [{ key: 'one', kind: 'message', role: 'user', status: 'accepted', title: 'User', timestamp: '2026-09-07T00:00:00Z', eventId: 'event', eventType: 'message.accepted', text }] }, instructionHistory: [], instructionBases: [], malformedLineCount: disclosure === 'MALFORMED' ? 1 : 0, sourceEventCount: 1, renderedItemCount: 1, diagnostics: [] };
  let state: ReturnType<SelectedSessionReplayLoader['getState']> = { status: 'IDLE' };
  return {
    getState: () => state,
    subscribe: () => () => {},
    load: vi.fn(async () => { state = { status: 'READY', projection }; return { applied: true, state }; }),
    cancel: vi.fn(), dispose: vi.fn()
  };
}

afterEach(() => { delete process.env.CHIRALITY_ANTHROPIC_API_KEY; });

describe('chat title derivation', () => {
  it('redacts configured keys before trimming at a word boundary and uses persona/session fallbacks', () => {
    process.env.CHIRALITY_ANTHROPIC_API_KEY = 'configured-secret-value';
    const title = deriveChatTitle({ firstOperatorMessage: `Review configured-secret-value and ${'carefully '.repeat(12)}`, persona: 'WORKING_ITEMS', sessionId: 'session' });
    expect(title).toContain('[REDACTED_API_KEY]');
    expect(title).not.toContain('configured-secret-value');
    expect(title.length).toBeLessThanOrEqual(60);
    expect(title.endsWith(' ')).toBe(false);
    expect(deriveChatTitle({ persona: 'WORKING_ITEMS', sessionId: 'session' })).toBe('Working Items');
    expect(deriveChatTitle({ persona: ' ', sessionId: 'session' })).toBe('session');
    expect(trimChatTitle('one two three four', 13)).toBe('one two three');
    expect(sanitizeChatLabel('\u0000\n  ')).toBeNull();
  });
});

it('keeps the additive v1 schema string unchanged', () => {
  expect(WOVEN_WORKSPACE_SCHEMA).toBe('chirality.woven-workspace/v1');
});

describe('chat section projection', () => {
  it('applies pin/group/folder precedence, alphabetical groups, and deterministic ordering', () => {
    const sessions = [
      session('today-b', '2026-09-07T09:00:00Z'), session('today-a', '2026-09-07T09:00:00Z'),
      session('yesterday', '2026-09-06T12:00:00Z'), session('week', '2026-09-03T12:00:00Z'),
      session('old', '2026-08-01T12:00:00Z'), session('pinned', '2026-07-01T12:00:00Z')
    ];
    const sections = projectChatSections({ sessions, referenceDay: '2026-09-07', state: {
      chatTitles: {}, chatPins: ['pinned', 'today-b'], chatArchived: ['old'], chatDeleted: [], chatGroups: [
        { id: 'z', name: 'Zulu', sessionIds: ['week', 'today-b'] },
        { id: 'a', name: 'Alpha', sessionIds: ['yesterday', 'week'] }
      ]
    } });
    expect(sections.map(section => section.label)).toEqual(['Pinned', 'Alpha', 'Zulu', 'today-a']);
    expect(sections[0].entries.map(entry => entry.sessionId)).toEqual(['pinned', 'today-b']);
    expect(sections[1].entries.map(entry => entry.sessionId)).toEqual(['yesterday', 'week']);
    expect(sections[2].entries).toEqual([]);
    expect(sections[3]).toMatchObject({ kind: 'folder', folderPath: '/roots/today-a', current: false });
    expect(sections[3].entries.map(entry => entry.sessionId)).toEqual(['today-a']);
    expect(sections.flatMap(section => section.entries).map(entry => entry.sessionId)).toEqual(['pinned', 'today-b', 'yesterday', 'week', 'today-a']);
    expect(sections[3].entries[0]).toMatchObject({ when: '09:00', folderLabel: 'today-a' });
  });

  it('groups chats by recorded folder: the new-chat folder first, then known folders by use, with disambiguated labels', () => {
    const at = (day: number) => `2026-09-0${day}T00:00:00Z`;
    const sessions = [
      { ...session('a1', at(7)), projectRoot: '/work/alpha' }, { ...session('a2', at(1)), projectRoot: '/work/alpha/' },
      { ...session('b1', at(6)), projectRoot: '/other/alpha' }, { ...session('c1', at(5)), projectRoot: '/work/gamma' },
      { ...session('n1', at(4)), projectRoot: '' }
    ];
    const state = { chatTitles: {}, chatPins: [], chatArchived: [], chatDeleted: [], chatGroups: [] };
    const sections = projectChatSections({ sessions, state, referenceDay: '2026-09-07', currentRoot: '/work/gamma', folderOrder: ['/other/alpha', '/work/gamma', '/work/alpha'] });
    expect(sections.map(section => [section.label, section.current, section.entries.map(entry => entry.sessionId)])).toEqual([
      ['gamma', true, ['c1']], ['other/alpha', false, ['b1']], ['work/alpha', false, ['a1', 'a2']], ['No folder', false, ['n1']]
    ]);
    // Without a known order, folders follow the recency of their newest chat; the trailing slash does not split a folder.
    expect(projectChatSections({ sessions, state, referenceDay: '2026-09-07' }).map(section => section.label)).toEqual(['work/alpha', 'other/alpha', 'gamma', 'No folder']);
  });

  it('keeps archived and locally deleted sessions distinct and hides both from active chats', () => {
    const sessions = [session('active', '2026-09-07T00:00:00Z'), session('archived', '2026-09-06T00:00:00Z'), session('deleted', '2026-09-05T00:00:00Z')];
    const state = { chatTitles: {}, chatPins: [], chatArchived: ['archived'], chatDeleted: ['deleted'], chatGroups: [] };
    const ids = (visibility?: 'active' | 'archived' | 'deleted') => projectChatSections({ sessions, state, referenceDay: '2026-09-07', visibility }).flatMap(section => section.entries.map(entry => entry.sessionId));
    expect(ids()).toEqual(['active']);
    expect(ids('archived')).toEqual(['archived']);
    expect(ids('deleted')).toEqual(['deleted']);
  });

  it('orders every visible active session for title derivation without applying the message-search cap', () => {
    const sessions = Array.from({ length: 24 }, (_, index) => session(`s${String(index).padStart(2, '0')}`, `2026-09-${String(index + 1).padStart(2, '0')}T00:00:00Z`));
    const visible = visibleActiveChatSessions(sessions, ['s23'], ['s22']);
    expect(visible).toHaveLength(22);
    expect(visible.map(item => item.sessionId).slice(0, 3)).toEqual(['s21', 's20', 's19']);
    expect(visible.at(-1)?.sessionId).toBe('s00');
  });
});

describe('isolated replay reads', () => {
  it('loads first user text only from admissible identity-checked projections', async () => {
    const created = [loaderFor('good', 'READY_SNAPSHOT', 'first prompt'), loaderFor('bad', 'CONFLICTING', 'foreign'), loaderFor('stale', 'STALE', 'old prompt')];
    const result = await loadRecordedFirstOperatorMessages({ sessions: [session('good', '2026-09-07T00:00:00Z'), session('bad', '2026-09-06T00:00:00Z'), session('stale', '2026-09-05T00:00:00Z')], observedAt: '2026-09-07T00:00:00Z', createLoader: () => created.shift()! });
    expect(result).toEqual({ good: 'first prompt' });
  });

  it('searches only the twenty most recent sessions and excludes malformed, conflicting, and unavailable reads', async () => {
    const sessions = Array.from({ length: 24 }, (_, index) => session(`s${String(index).padStart(2, '0')}`, `2026-09-${String(index + 1).padStart(2, '0')}T00:00:00Z`));
    const loaded: string[] = [];
    const result = await searchRecordedSessionMessages({ sessions, query: 'needle', observedAt: '2026-09-30T00:00:00Z', createLoader: () => {
      const target = sessions.slice().sort((a, b) => b.updatedAt.localeCompare(a.updatedAt))[loaded.length];
      loaded.push(target.sessionId);
      return loaderFor(target.sessionId, target.sessionId === 's22' ? 'MALFORMED' : target.sessionId === 's21' ? 'CONFLICTING' : target.sessionId === 's18' ? 'STALE' : 'READY_SNAPSHOT', target.sessionId === 's20' ? 'a needle here' : target.sessionId === 's19' ? 'another needle' : target.sessionId === 's18' ? 'stale needle' : 'none');
    } });
    expect(loaded).toHaveLength(CHAT_MESSAGE_SEARCH_LIMIT);
    expect(loaded).not.toContain('s00');
    expect(result).toEqual(['s20', 's19']);
  });

  it('uses a finite complete-projection limit and finds content before item 500', async () => {
    const items = Array.from({ length: 601 }, (_, index) => ({ key: String(index), kind: 'message' as const, role: index === 2 ? 'user' as const : 'assistant' as const, status: 'accepted' as const, title: 'Message', timestamp: '2026-09-07T00:00:00Z', eventId: String(index), eventType: 'message.accepted' as const, text: index === 2 ? 'early needle prompt' : `tail ${index}` }));
    const make = () => {
      let state: ReturnType<SelectedSessionReplayLoader['getState']> = { status: 'IDLE' };
      return { getState: () => state, subscribe: () => () => {}, cancel: vi.fn(), dispose: vi.fn(), load: vi.fn(async (sessionId: string, options) => {
        expect(options.maxItems).toBe(COMPLETE_REPLAY_ITEM_LIMIT);
        state = { status: 'READY', projection: { selectedSessionId: sessionId, sourceReference: `session:${sessionId}/events`, observedAt: options.observedAt, disclosure: 'READY_SNAPSHOT', currency: 'CURRENT', transcript: { sessionId, itemCount: items.length, items }, instructionHistory: [], instructionBases: [], malformedLineCount: 0, sourceEventCount: items.length, renderedItemCount: items.length, diagnostics: [] } };
        return { applied: true, state };
      }) } satisfies SelectedSessionReplayLoader;
    };
    const reader = createChatReplayReader(make);
    expect(await reader.loadFirstOperatorMessages([session('long', '2026-09-07T00:00:00Z')], '2026-09-07T00:00:00Z')).toEqual({ long: 'early needle prompt' });
    expect(await reader.search([session('long', '2026-09-07T00:00:00Z')], 'needle', '2026-09-07T00:00:00Z')).toEqual(['long']);
    reader.dispose();
  });

  it('bounds concurrency and cancels and disposes active readers', async () => {
    let active = 0; let maximum = 0;
    const releases: Array<() => void> = [];
    const loaders: SelectedSessionReplayLoader[] = [];
    const reader = createChatReplayReader(() => {
      const loader = loaderFor('unused');
      loader.load = vi.fn(async () => { active += 1; maximum = Math.max(maximum, active); await new Promise<void>(resolve => releases.push(resolve)); active -= 1; return { applied: false, state: { status: 'IDLE' as const } }; });
      loaders.push(loader); return loader;
    });
    const pending = reader.search(Array.from({ length: 9 }, (_, i) => session(`s${i}`, `2026-09-0${i + 1}T00:00:00Z`)), 'x', '2026-09-07T00:00:00Z');
    await vi.waitFor(() => expect(loaders).toHaveLength(CHAT_REPLAY_WORKER_LIMIT));
    expect(maximum).toBe(CHAT_REPLAY_WORKER_LIMIT);
    reader.cancel();
    expect(loaders.every(loader => vi.mocked(loader.cancel).mock.calls.length === 1)).toBe(true);
    releases.splice(0).forEach(resolve => resolve());
    expect(await pending).toEqual([]);
    expect(loaders.every(loader => vi.mocked(loader.dispose).mock.calls.length >= 1)).toBe(true);
    reader.dispose();
  });

  it('does not exceed four outstanding loads across overlapping cancelled generations', async () => {
    let active = 0; let peak = 0;
    const releases: Array<() => void> = [];
    const loaders: SelectedSessionReplayLoader[] = [];
    const reader = createChatReplayReader(() => {
      const loader = loaderFor('pending');
      loader.load = vi.fn(async () => { active += 1; peak = Math.max(peak, active); await new Promise<void>(resolve => releases.push(resolve)); active -= 1; return { applied: false, state: { status: 'IDLE' as const } }; });
      loaders.push(loader); return loader;
    });
    const sessions = Array.from({ length: 8 }, (_, i) => session(`g${i}`, `2026-09-0${i + 1}T00:00:00Z`));
    const obsolete = reader.search(sessions, 'old', '2026-09-07T00:00:00Z');
    await vi.waitFor(() => expect(active).toBe(CHAT_REPLAY_WORKER_LIMIT));
    const replacement = reader.search(sessions, 'new', '2026-09-07T00:00:01Z');
    await Promise.resolve(); expect(loaders).toHaveLength(CHAT_REPLAY_WORKER_LIMIT); expect(peak).toBe(4);
    releases.splice(0, 4).forEach(resolve => resolve());
    await vi.waitFor(() => expect(loaders.length).toBeGreaterThan(4)); expect(peak).toBe(4);
    for (let round = 0; round < 2; round += 1) { await vi.waitFor(() => expect(releases.length).toBeGreaterThan(0)); releases.splice(0).forEach(resolve => resolve()); await Promise.resolve(); }
    expect(await obsolete).toEqual([]); expect(await replacement).toEqual([]); expect(peak).toBe(4);
    reader.dispose();
  });
});
