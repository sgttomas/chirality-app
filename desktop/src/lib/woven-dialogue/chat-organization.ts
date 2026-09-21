import type { SessionRecord } from '@chirality/runtime-contracts/types';
import { redactConfiguredApiKeys } from '../harness/run-logger';
import {
  createSelectedSessionReplayLoader,
  type SelectedSessionReplayLoader
} from './selected-session-replay';
import type { WovenWorkspaceAdditions } from './woven-workspace-state';

export const CHAT_TITLE_LIMIT = 60;
export const CHAT_LABEL_LIMIT = 80;
export const CHAT_MESSAGE_SEARCH_LIMIT = 20;

export type ChatSection = {
  id: string;
  label: string;
  kind: 'pinned' | 'group' | 'folder';
  entries: ChatOrganizationEntry[];
  /** Folder sections: the recorded folder path, and whether it is the folder selected for new chats. */
  folderPath?: string;
  current?: boolean;
};

export type ChatOrganizationEntry = {
  session: SessionRecord;
  sessionId: string;
  title: string;
  folderLabel: string;
  updatedAt: string;
  when: string;
};

type ChatOrganizationState = Pick<
  WovenWorkspaceAdditions,
  'chatTitles' | 'chatPins' | 'chatArchived' | 'chatDeleted' | 'chatGroups'
>;

function personaLabel(persona: string | undefined): string | undefined {
  const value = persona?.trim();
  if (!value) return undefined;
  if (value === 'HELP_HUMAN') return 'Assistant';
  return /^[A-Z][A-Z0-9_]*$/.test(value)
    ? value.toLowerCase().split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ')
    : value;
}

export function sanitizeChatLabel(value: string): string | null {
  const label = (redactConfiguredApiKeys(value) ?? '').replace(/[\u0000-\u001f\u007f]/g, ' ').replace(/\s+/g, ' ').trim();
  return label ? label.slice(0, CHAT_LABEL_LIMIT).trim() : null;
}

export function trimChatTitle(value: string, limit = CHAT_TITLE_LIMIT): string {
  const normalized = value.replace(/\s+/g, ' ').trim();
  if (normalized.length <= limit) return normalized;
  const prefix = normalized.slice(0, limit);
  if (/\s/.test(normalized.charAt(limit))) return prefix.trimEnd();
  const boundary = prefix.lastIndexOf(' ');
  return boundary > 0 ? prefix.slice(0, boundary).trimEnd() : prefix.trimEnd();
}

export function deriveChatTitle(input: {
  firstOperatorMessage?: string;
  persona?: string;
  sessionId: string;
}): string {
  const redacted = redactConfiguredApiKeys(input.firstOperatorMessage)?.trim();
  if (redacted) return trimChatTitle(redacted);
  return personaLabel(input.persona) ?? input.sessionId;
}

function validDay(value: string): Date | null {
  if (!/^\d{4}-\d{2}-\d{2}$/.test(value)) return null;
  const date = new Date(`${value}T00:00:00.000Z`);
  return Number.isFinite(date.getTime()) && date.toISOString().slice(0, 10) === value ? date : null;
}

function recordedDate(value: string): Date | null {
  const date = new Date(value);
  return Number.isFinite(date.getTime()) ? date : null;
}

function dayDifference(referenceDay: string, value: string): number | null {
  const reference = validDay(referenceDay);
  const recorded = recordedDate(value);
  if (!reference || !recorded) return null;
  const recordedDay = Date.UTC(recorded.getUTCFullYear(), recorded.getUTCMonth(), recorded.getUTCDate());
  return Math.floor((reference.getTime() - recordedDay) / 86_400_000);
}

export function formatChatWhen(value: string, referenceDay: string): string {
  const date = recordedDate(value);
  if (!date) return '';
  const difference = dayDifference(referenceDay, value);
  if (difference === 0) {
    return `${String(date.getUTCHours()).padStart(2, '0')}:${String(date.getUTCMinutes()).padStart(2, '0')}`;
  }
  if (difference !== null && difference > 0 && difference < 7) {
    return ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'][date.getUTCDay()] ?? '';
  }
  return `${['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'][date.getUTCMonth()]} ${date.getUTCDate()}`;
}

/** Folder key for grouping: the recorded path without a trailing slash; the empty string means no recorded folder. */
export function chatFolderKey(projectRoot: string | undefined): string {
  return typeof projectRoot === 'string' ? projectRoot.replace(/\/+$/, '') : '';
}

/**
 * Short labels for folder sections: the basename, widened with the parent
 * directory when two folders share a basename.
 */
export function folderSectionLabels(paths: readonly string[]): Map<string, string> {
  const labels = new Map<string, string>();
  const byBase = new Map<string, string[]>();
  for (const path of paths) {
    const base = folderBasename(path);
    byBase.set(base, [...(byBase.get(base) ?? []), path]);
  }
  for (const path of paths) {
    if (!path) { labels.set(path, 'No folder'); continue; }
    const base = folderBasename(path);
    if ((byBase.get(base)?.length ?? 0) <= 1) { labels.set(path, base); continue; }
    const parts = path.split('/').filter(Boolean);
    labels.set(path, parts.length >= 2 ? `${parts.at(-2)}/${parts.at(-1)}` : base);
  }
  return labels;
}

function orderSessions(sessions: readonly SessionRecord[]): SessionRecord[] {
  return [...sessions].sort((left, right) => {
    const leftKey = left.updatedAt || left.createdAt || '';
    const rightKey = right.updatedAt || right.createdAt || '';
    return rightKey.localeCompare(leftKey) || left.sessionId.localeCompare(right.sessionId);
  });
}

export function visibleActiveChatSessions(
  sessions: readonly SessionRecord[],
  chatArchived: readonly string[],
  chatDeleted: readonly string[]
): SessionRecord[] {
  const hidden = new Set([...chatArchived, ...chatDeleted]);
  return orderSessions(sessions).filter(session => !hidden.has(session.sessionId));
}

function folderBasename(projectRoot: string | undefined): string {
  const normalized = typeof projectRoot === 'string' ? projectRoot.replace(/\/+$/, '') : '';
  return normalized ? normalized.slice(normalized.lastIndexOf('/') + 1) || normalized : 'No folder';
}

export function projectChatSections(input: {
  sessions: readonly SessionRecord[];
  state: ChatOrganizationState;
  firstOperatorMessages?: Readonly<Record<string, string>>;
  referenceDay: string;
  visibility?: 'active' | 'archived' | 'deleted';
  /** The folder selected for new chats; its section is listed first. */
  currentRoot?: string | null;
  /** Known folders, most recently used first; breaks ties between folder sections. */
  folderOrder?: readonly string[];
}): ChatSection[] {
  const archived = new Set(input.state.chatArchived);
  const deleted = new Set(input.state.chatDeleted);
  const visibility = input.visibility ?? 'active';
  const ordered = orderSessions(input.sessions).filter(session => visibility === 'active'
    ? !archived.has(session.sessionId) && !deleted.has(session.sessionId)
    : visibility === 'archived' ? archived.has(session.sessionId) : deleted.has(session.sessionId));
  const byId = new Map(ordered.map(session => [session.sessionId, session]));
  const entry = (session: SessionRecord): ChatOrganizationEntry => ({
    session,
    sessionId: session.sessionId,
    title: input.state.chatTitles[session.sessionId] ?? deriveChatTitle({
      firstOperatorMessage: input.firstOperatorMessages?.[session.sessionId],
      persona: session.persona,
      sessionId: session.sessionId
    }),
    folderLabel: folderBasename(session.projectRoot),
    updatedAt: session.updatedAt || session.createdAt || '',
    when: formatChatWhen(session.updatedAt || session.createdAt || '', input.referenceDay)
  });
  const assigned = new Set<string>();
  const sections: ChatSection[] = [];

  const pinnedEntries = input.state.chatPins.flatMap(sessionId => {
    const session = byId.get(sessionId);
    if (!session || assigned.has(sessionId)) return [];
    assigned.add(sessionId);
    return [entry(session)];
  });
  if (pinnedEntries.length) sections.push({ id: 'pinned', label: 'Pinned', kind: 'pinned', entries: pinnedEntries });

  for (const group of [...input.state.chatGroups].sort((a, b) => a.name.localeCompare(b.name) || a.id.localeCompare(b.id))) {
    const entries = ordered.flatMap(session => {
      if (assigned.has(session.sessionId) || !group.sessionIds.includes(session.sessionId)) return [];
      assigned.add(session.sessionId);
      return [entry(session)];
    });
    sections.push({ id: group.id, label: group.name, kind: 'group', entries });
  }

  // Everything else sits under its recorded folder: the folder selected for
  // new chats first, then known folders by recency of use, then any other
  // recorded folder by the recency of its newest chat.
  const currentKey = chatFolderKey(input.currentRoot ?? undefined);
  const folderRank = new Map((input.folderOrder ?? []).map((path, index) => [chatFolderKey(path), index]));
  const folderSections = new Map<string, ChatSection>();
  for (const session of ordered) {
    if (assigned.has(session.sessionId)) continue;
    const key = chatFolderKey(session.projectRoot);
    const target = folderSections.get(key) ?? { id: `folder:${key}`, label: '', kind: 'folder' as const, entries: [], folderPath: key, current: key === currentKey && key !== '' };
    target.entries.push(entry(session));
    folderSections.set(key, target);
  }
  const labels = folderSectionLabels([...folderSections.keys()]);
  const ranked = [...folderSections.values()].map((section, index) => ({ section, index }));
  ranked.sort((a, b) => {
    if (a.section.current !== b.section.current) return a.section.current ? -1 : 1;
    const rankA = folderRank.get(a.section.folderPath ?? '') ?? Number.MAX_SAFE_INTEGER;
    const rankB = folderRank.get(b.section.folderPath ?? '') ?? Number.MAX_SAFE_INTEGER;
    if (rankA !== rankB) return rankA - rankB;
    if ((a.section.folderPath === '') !== (b.section.folderPath === '')) return a.section.folderPath === '' ? 1 : -1;
    return a.index - b.index;
  });
  for (const { section } of ranked) {
    section.label = labels.get(section.folderPath ?? '') ?? 'No folder';
    sections.push(section);
  }
  return sections;
}

function projectionCanSupplyText(loader: SelectedSessionReplayLoader): string | null {
  const state = loader.getState();
  if (state.status !== 'READY') return null;
  const projection = state.projection;
  if (projection.disclosure !== 'READY_SNAPSHOT' && projection.disclosure !== 'BOUNDED') return null;
  return projection.transcript.items
    .filter(item => item.kind === 'message')
    .map(item => item.text ?? '')
    .join('\n');
}

export const CHAT_REPLAY_WORKER_LIMIT = 4;
export const COMPLETE_REPLAY_ITEM_LIMIT = Number.MAX_SAFE_INTEGER;

export type ChatReplayReader = {
  loadFirstOperatorMessages(sessions: readonly SessionRecord[], observedAt: string): Promise<Record<string, string>>;
  search(sessions: readonly SessionRecord[], query: string, observedAt: string): Promise<string[]>;
  cancel(): void;
  dispose(): void;
};

type ReplaySlotWaiter = { limit: number; resolve: () => void };
const replaySlots = { occupied: 0, waiters: [] as ReplaySlotWaiter[] };

function acquireReplaySlot(limit: number): Promise<void> {
  if (replaySlots.occupied < limit) { replaySlots.occupied += 1; return Promise.resolve(); }
  return new Promise(resolve => replaySlots.waiters.push({ limit, resolve }));
}

function releaseReplaySlot(): void {
  replaySlots.occupied -= 1;
  const index = replaySlots.waiters.findIndex(waiter => replaySlots.occupied < waiter.limit);
  if (index < 0) return;
  const [waiter] = replaySlots.waiters.splice(index, 1);
  replaySlots.occupied += 1;
  waiter.resolve();
}

export function createChatReplayReader(
  createLoader: () => SelectedSessionReplayLoader = () => createSelectedSessionReplayLoader(),
  workerLimit = CHAT_REPLAY_WORKER_LIMIT
): ChatReplayReader {
  const active = new Set<SelectedSessionReplayLoader>();
  let generation = 0;
  let disposed = false;
  const workers = Number.isFinite(workerLimit) && workerLimit > 0
    ? Math.floor(workerLimit)
    : CHAT_REPLAY_WORKER_LIMIT;

  const cancel = (): void => {
    generation += 1;
    for (const loader of active) { loader.cancel(); loader.dispose(); }
  };

  async function run<T>(sessions: readonly SessionRecord[], observedAt: string, visit: (loader: SelectedSessionReplayLoader, session: SessionRecord) => T | null): Promise<Array<[string, T]>> {
    if (disposed) return [];
    cancel();
    const requestGeneration = generation;
    const availableSessionIds = new Set(sessions.map(session => session.sessionId));
    const output: Array<[string, T]> = [];
    let next = 0;
    await Promise.all(Array.from({ length: Math.min(workers, sessions.length) }, async () => {
      while (!disposed && generation === requestGeneration) {
        const index = next++;
        const session = sessions[index];
        if (!session) return;
        await acquireReplaySlot(workers);
        if (disposed || generation !== requestGeneration) { releaseReplaySlot(); return; }
        const loader = createLoader(); active.add(loader);
        try {
          await loader.load(session.sessionId, { observedAt, availableSessionIds, maxItems: COMPLETE_REPLAY_ITEM_LIMIT });
          if (!disposed && generation === requestGeneration) {
            const value = visit(loader, session);
            if (value !== null) output.push([session.sessionId, value]);
          }
        } finally {
          active.delete(loader); loader.dispose(); releaseReplaySlot();
        }
      }
    }));
    return generation === requestGeneration && !disposed ? output : [];
  }

  return {
    async loadFirstOperatorMessages(sessions, observedAt) {
      const pairs = await run(sessions, observedAt, loader => {
        const state = loader.getState();
        if (state.status !== 'READY' || (state.projection.disclosure !== 'READY_SNAPSHOT' && state.projection.disclosure !== 'BOUNDED')) return null;
        return state.projection.transcript.items.find(item => item.kind === 'message' && item.role === 'user' && Boolean(item.text?.trim()))?.text ?? null;
      });
      return Object.fromEntries(pairs);
    },
    async search(sessions, query, observedAt) {
      const needle = query.trim().toLocaleLowerCase();
      if (!needle) { cancel(); return []; }
      const recent = orderSessions(sessions).slice(0, CHAT_MESSAGE_SEARCH_LIMIT);
      const pairs = await run(recent, observedAt, loader => projectionCanSupplyText(loader)?.toLocaleLowerCase().includes(needle) ? true : null);
      const matches = new Set(pairs.map(([sessionId]) => sessionId));
      return recent.flatMap(session => matches.has(session.sessionId) ? [session.sessionId] : []);
    },
    cancel,
    dispose() { cancel(); disposed = true; }
  };
}

export async function loadRecordedFirstOperatorMessages(input: {
  sessions: readonly SessionRecord[];
  observedAt: string;
  createLoader?: () => SelectedSessionReplayLoader;
}): Promise<Record<string, string>> {
  const reader = createChatReplayReader(input.createLoader);
  try { return await reader.loadFirstOperatorMessages(input.sessions, input.observedAt); }
  finally { reader.dispose(); }
}

export async function searchRecordedSessionMessages(input: {
  sessions: readonly SessionRecord[];
  query: string;
  observedAt: string;
  createLoader?: () => SelectedSessionReplayLoader;
}): Promise<string[]> {
  const reader = createChatReplayReader(input.createLoader);
  try { return await reader.search(input.sessions, input.query, input.observedAt); }
  finally { reader.dispose(); }
}
