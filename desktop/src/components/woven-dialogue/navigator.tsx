'use client';

import React from 'react';
import type { SessionRecord } from '@chirality/runtime-contracts/types';
import { handoffDocument } from '../shell/document-view';
import {
  CHAT_LABEL_LIMIT,
  createChatReplayReader,
  projectChatSections,
  sanitizeChatLabel,
  type ChatOrganizationEntry,
  type ChatSection
} from '../../lib/woven-dialogue/chat-organization';
import type { WovenSessionSurfaceMap, WovenWorkspaceState, WovenWorkspaceSurface } from '../../lib/woven-dialogue/woven-workspace-state';

export type WovenSurface = WovenWorkspaceSurface;
export type NavigatorSessionEntry = { sessionId: string; label: string; persona: string | undefined; projectRoot: string | undefined; when: string; surface: WovenSurface | null };
export type NavigatorSessionGroups = { bySurface: Record<WovenSurface, NavigatorSessionEntry[]>; all: NavigatorSessionEntry[] };
type OrganizationPatch = Pick<WovenWorkspaceState, 'chatTitles' | 'chatPins' | 'chatArchived' | 'chatDeleted' | 'chatGroups' | 'groupsCollapsed' | 'foldersCollapsed'>;
/** A folder whose chats are listed from the local index only, or which could not be opened. */
export type NavigatorFolderNotice = { kind: 'indexed' | 'unavailable'; message: string };

type NavigatorProps = {
  footerSlot?: React.ReactNode; onNewChat?: () => void; activeSurface: WovenSurface; legacyHref: string;
  onOpenSurface: (surface: WovenSurface) => void; sessions?: readonly SessionRecord[]; sessionSurfaces?: WovenSessionSurfaceMap;
  liveSessionId?: string; selectedSessionId?: string; selectionDisabled?: boolean; sessionsLoading?: boolean;
  sessionsError?: string | null; onSelectSession?: (sessionId: string) => void;
  needsAnswerSessionIds?: readonly string[]; onNeedsAnswer?: (sessionId: string) => void;
  expandedSurfaces?: readonly WovenSurface[]; onToggleSurfaceExpanded?: (surface: WovenSurface) => void;
  chatTitles?: Readonly<Record<string, string>>; chatPins?: readonly string[]; chatArchived?: readonly string[];
  chatDeleted?: readonly string[];
  chatGroups?: readonly { id: string; name: string; sessionIds: readonly string[] }[]; groupsCollapsed?: readonly string[];
  firstOperatorMessages?: Readonly<Record<string, string>>; referenceDay?: string; searchEpoch?: string | number;
  focusSearchRequest?: number;
  onModalStateChange?: (open: boolean) => void;
  onOrganizationChange?: (patch: Partial<OrganizationPatch>) => void;
  searchMessages?: (query: string, sessions: readonly SessionRecord[]) => Promise<string[]>;
  /** The folder selected for new chats; its section is listed first. */
  currentRoot?: string | null;
  /** Known folders, most recently used first. */
  folderOrder?: readonly string[];
  foldersCollapsed?: readonly string[];
  folderNotices?: Readonly<Record<string, NavigatorFolderNotice>>;
  /** Recovery for a folder that is missing or inaccessible: choose where it is now. */
  onLocateFolder?: (folderPath: string) => void;
  /** Stop listing a folder that no longer exists; the Runtime records are untouched. */
  onForgetFolder?: (folderPath: string) => void;
};

export const NAVIGATOR_RECENT_SESSION_LIMIT = 4;
const MAX_CHAT_ANNOTATIONS = 500;
const MAX_CHAT_REFERENCES = 200;
const EMPTY_SESSIONS: readonly SessionRecord[] = [];
const EMPTY_SESSION_SURFACES: WovenSessionSurfaceMap = {};
const EMPTY_CHAT_TITLES: Readonly<Record<string, string>> = {};
const EMPTY_CHAT_IDS: readonly string[] = [];
const EMPTY_CHAT_GROUPS: readonly { id: string; name: string; sessionIds: readonly string[] }[] = [];

function legacyPersonaLabel(persona: string | undefined, sessionId: string): string {
  const value = persona?.trim();
  if (!value) return sessionId;
  if (value === 'HELP_HUMAN') return 'Assistant';
  return /^[A-Z][A-Z0-9_]*$/.test(value) ? value.toLowerCase().split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ') : value;
}
function legacyWhen(value: string | undefined): string {
  const match = /^(\d{4})-(\d{2})-(\d{2})/.exec(value ?? '');
  const month = match ? ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'][Number(match[2]) - 1] : undefined;
  return match && month ? `${month} ${Number(match[3])}, ${match[1]}` : '';
}
export function buildNavigatorSessionGroups(sessions: readonly SessionRecord[], sessionSurfaces: WovenSessionSurfaceMap): NavigatorSessionGroups {
  const bySurface: Record<WovenSurface, NavigatorSessionEntry[]> = { dialogue: [], workbench: [], pipeline: [] };
  const all = [...sessions].sort((left, right) => (right.updatedAt || right.createdAt || '').localeCompare(left.updatedAt || left.createdAt || '') || left.sessionId.localeCompare(right.sessionId)).map(session => {
    const entry: NavigatorSessionEntry = { sessionId: session.sessionId, label: legacyPersonaLabel(session.persona, session.sessionId), persona: session.persona, projectRoot: session.projectRoot, when: legacyWhen(session.updatedAt || session.createdAt), surface: sessionSurfaces[session.sessionId] ?? null };
    if (entry.surface) bySurface[entry.surface].push(entry);
    return entry;
  });
  return { bySurface, all };
}

function SessionRow({ entry, live, selected, disabled, onSelectSession, onOpenMenu, controlRef, needsAnswer, onNeedsAnswer }: {
  entry: ChatOrganizationEntry; live: boolean; selected: boolean; disabled: boolean;
  onSelectSession?: (sessionId: string) => void; onOpenMenu: (sessionId: string, trigger: HTMLElement) => void;
  needsAnswer?: boolean; onNeedsAnswer?: (sessionId: string) => void;
  controlRef: (node: HTMLButtonElement | null) => void;
}): JSX.Element {
  const [pending, setPending] = React.useState(false);
  const [error, setError] = React.useState<string | null>(null);
  const active = React.useRef(true); const inFlight = React.useRef(false); const requestGeneration = React.useRef(0); const noticeId = React.useId();
  React.useEffect(() => { active.current = true; return () => { active.current = false; }; }, []);
  React.useEffect(() => { requestGeneration.current += 1; inFlight.current = false; setPending(false); setError(null); }, [entry.session.projectRoot]);
  async function reveal(): Promise<void> {
    if (inFlight.current) return;
    const root = entry.session.projectRoot;
    if (typeof root !== 'string' || !root.startsWith('/') || /[\x00-\x1f\x7f]/.test(root)) { setError('This chat has no valid recorded folder to reveal.'); return; }
    inFlight.current = true; const generation = requestGeneration.current; setPending(true); setError(null);
    try { await handoffDocument({ action: 'reveal-root', projectRoot: root }); }
    catch (failure) { if (active.current && generation === requestGeneration.current) { const message = failure instanceof Error ? failure.message.trim() : ''; setError(message || 'Unable to reveal this chat’s folder. Try again.'); } }
    finally { if (generation === requestGeneration.current) { inFlight.current = false; if (active.current) setPending(false); } }
  }
  return <li draggable tabIndex={-1} onDragStart={event => event.dataTransfer.setData('text/chirality-session-id', entry.sessionId)} onContextMenu={event => { event.preventDefault(); onOpenMenu(entry.sessionId, event.currentTarget); }}>
    <div className="woven-navigator-session-row">
      <button ref={controlRef} type="button" className={`woven-navigator-session${live ? ' woven-navigator-session--live' : ''}`} title={`${entry.title} · ${entry.session.persona ? `${entry.session.persona} · ` : ''}${entry.sessionId}`} data-session-id={entry.sessionId} disabled={disabled || !onSelectSession} aria-pressed={selected} onClick={() => { if (!disabled) onSelectSession?.(entry.sessionId); }}>
        <span className="woven-navigator-session-heading">{live ? <span className="woven-navigator-session-dot" role="img" aria-label="Live session" /> : null}<span className="woven-navigator-session-title">{entry.title}</span><span className="woven-navigator-session-when">{entry.when}</span></span>
        <span className="woven-navigator-session-folder" title={entry.session.projectRoot || 'No folder'}><span aria-hidden="true">⌑</span> {entry.folderLabel}</span>
      </button>
      {needsAnswer ? <button type="button" className="button-muted" aria-label={`Needs answer: ${entry.title}`} onClick={() => onNeedsAnswer?.(entry.sessionId)}>Needs answer</button> : null}
      <button type="button" className="woven-navigator-session-reveal" aria-label={`${pending ? 'Revealing' : error ? 'Retry revealing' : 'Reveal'} folder for ${entry.title} (${entry.sessionId})`} title={`Reveal in Finder · ${entry.session.projectRoot || 'No recorded folder'}`} aria-describedby={error ? noticeId : undefined} aria-busy={pending} disabled={pending} onClick={() => { void reveal(); }}>
        <svg aria-hidden="true" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5"><path d="M3 7V5a1 1 0 0 1 1-1h5l2 3h9a1 1 0 0 1 1 1v11a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V7Z" /><path d="M9 13h6m-3-3 3 3-3 3" /></svg>
      </button>
      <button type="button" className="woven-navigator-session-overflow" aria-label={`Chat actions for ${entry.title}`} aria-haspopup="menu" onClick={event => onOpenMenu(entry.sessionId, event.currentTarget)}>•••</button>
    </div>{error ? <p id={noticeId} className="panel-error" role="alert">{error}</p> : null}
  </li>;
}

const EMPTY_FOLDER_NOTICES: Readonly<Record<string, NavigatorFolderNotice>> = {};

export function Navigator({ activeSurface, footerSlot, onNewChat, legacyHref, onOpenSurface, sessions = EMPTY_SESSIONS, sessionSurfaces = EMPTY_SESSION_SURFACES, liveSessionId, selectedSessionId, selectionDisabled = false, sessionsLoading = false, sessionsError = null, onSelectSession, chatTitles = EMPTY_CHAT_TITLES, chatPins = EMPTY_CHAT_IDS, chatArchived = EMPTY_CHAT_IDS, chatDeleted = EMPTY_CHAT_IDS, chatGroups = EMPTY_CHAT_GROUPS, groupsCollapsed = EMPTY_CHAT_IDS, firstOperatorMessages = EMPTY_CHAT_TITLES, referenceDay = '1970-01-01', searchEpoch = '', focusSearchRequest = 0, onModalStateChange, onOrganizationChange, searchMessages, currentRoot = null, folderOrder = EMPTY_CHAT_IDS, foldersCollapsed = EMPTY_CHAT_IDS, folderNotices = EMPTY_FOLDER_NOTICES, onLocateFolder, onForgetFolder, needsAnswerSessionIds = EMPTY_CHAT_IDS, onNeedsAnswer }: NavigatorProps): JSX.Element {
  void sessionSurfaces;
  void legacyHref;
  const [query, setQuery] = React.useState(''); const [messageMatchIds, setMessageMatchIds] = React.useState<string[]>([]); const [messageSearchPending, setMessageSearchPending] = React.useState(false);
  const [menuSessionId, setMenuSessionId] = React.useState<string | null>(null); const [dialog, setDialog] = React.useState<'rename' | 'new-group' | 'delete' | null>(null); const [dialogValue, setDialogValue] = React.useState('');
  const [visibility, setVisibility] = React.useState<'active' | 'archived' | 'deleted'>('active');
  const searchRef = React.useRef<HTMLInputElement | null>(null); const menuRef = React.useRef<HTMLDivElement | null>(null); const dialogRef = React.useRef<HTMLDivElement | null>(null); const menuTriggerRef = React.useRef<HTMLElement | null>(null);
  const searchReaderRef = React.useRef<ReturnType<typeof createChatReplayReader>>();
  const sessionControlRefs = React.useRef(new Map<string, HTMLButtonElement>()); const groupHeaderRefs = React.useRef(new Map<string, HTMLButtonElement>());
  const normalizedGroups = React.useMemo(() => chatGroups.map(group => ({ ...group, sessionIds: [...group.sessionIds] })), [chatGroups]);
  const organization = React.useMemo(() => ({ chatTitles: { ...chatTitles }, chatPins: [...chatPins], chatArchived: [...chatArchived], chatDeleted: [...chatDeleted], chatGroups: normalizedGroups }), [chatTitles, chatPins, chatArchived, chatDeleted, normalizedGroups]);
  const sections = React.useMemo(() => projectChatSections({ sessions, state: organization, firstOperatorMessages, referenceDay, visibility, currentRoot, folderOrder }), [sessions, organization, firstOperatorMessages, referenceDay, visibility, currentRoot, folderOrder]);
  const entries = React.useMemo(() => sections.flatMap(section => section.entries), [sections]); const entryById = React.useMemo(() => new Map(entries.map(entry => [entry.sessionId, entry])), [entries]);
  const normalizedQuery = query.trim().toLocaleLowerCase(); const titleMatches = normalizedQuery ? entries.filter(entry => entry.title.toLocaleLowerCase().includes(normalizedQuery)) : [];
  const messageMatches = messageMatchIds.flatMap(id => entryById.get(id) ? [entryById.get(id)!] : []);

  React.useEffect(() => {
    const reader = createChatReplayReader(); searchReaderRef.current = reader;
    return () => { if (searchReaderRef.current === reader) searchReaderRef.current = undefined; reader.dispose(); };
  }, []);
  React.useEffect(() => {
    if (!normalizedQuery) { setMessageMatchIds([]); setMessageSearchPending(false); return; }
    let current = true; setMessageSearchPending(true);
    const timeout = globalThis.setTimeout(() => {
      const run = searchMessages ?? ((value: string, visible: readonly SessionRecord[]) => searchReaderRef.current?.search(visible, value, new Date().toISOString()) ?? Promise.resolve([]));
      void run(normalizedQuery, entries.map(entry => entry.session)).then(ids => { if (current) setMessageMatchIds(ids); }).catch(() => { if (current) setMessageMatchIds([]); }).finally(() => { if (current) setMessageSearchPending(false); });
    }, 250);
    return () => { current = false; globalThis.clearTimeout(timeout); searchReaderRef.current?.cancel(); };
  }, [normalizedQuery, entries, searchEpoch, searchMessages]);
  React.useEffect(() => { if (focusSearchRequest > 0) searchRef.current?.focus(); }, [focusSearchRequest]);
  React.useEffect(() => { onModalStateChange?.(Boolean(dialog)); }, [dialog, onModalStateChange]);
  React.useEffect(() => () => onModalStateChange?.(false), [onModalStateChange]);

  function closeMenu(groupId?: string): void { const sessionId = menuSessionId; const trigger = menuTriggerRef.current; setMenuSessionId(null); setDialog(null); setDialogValue(''); if (typeof window !== 'undefined') window.requestAnimationFrame(() => { if (trigger?.isConnected) trigger.focus(); else { const target = sessionControlRefs.current.get(sessionId ?? '') ?? groupHeaderRefs.current.get(groupId ?? '') ?? searchRef.current; target?.focus(); } }); }
  function openMenu(sessionId: string, trigger: HTMLElement): void { menuTriggerRef.current = trigger; setMenuSessionId(sessionId); setDialog(null); setDialogValue(''); }
  React.useEffect(() => {
    if (typeof window === 'undefined' || typeof window.addEventListener !== 'function') return;
    const keydown = (event: KeyboardEvent): void => {
      if (event.key === 'Escape') { if (dialog) setDialog(null); else if (menuSessionId) closeMenu(); else if (query) { setQuery(''); searchRef.current?.focus(); } }
    };
    window.addEventListener('keydown', keydown); return () => window.removeEventListener('keydown', keydown);
  });
  React.useEffect(() => { if (menuSessionId && !dialog) menuRef.current?.querySelector<HTMLButtonElement>('button')?.focus(); }, [menuSessionId, dialog]);
  React.useEffect(() => {
    if (!dialog) return;
    dialogRef.current?.querySelector<HTMLElement>('[data-dialog-initial]')?.focus();
  }, [dialog]);
  React.useEffect(() => {
    if (!menuSessionId || dialog || typeof document === 'undefined') return;
    const dismiss = (event: MouseEvent): void => { if (!menuRef.current?.contains(event.target as Node)) closeMenu(); };
    document.addEventListener('mousedown', dismiss); return () => document.removeEventListener('mousedown', dismiss);
  }, [menuSessionId, dialog]);
  function moveToGroup(sessionId: string, groupId: string): void {
    if (!entryById.has(sessionId) || !normalizedGroups.some(group => group.id === groupId)) return;
    onOrganizationChange?.({ chatPins: chatPins.filter(id => id !== sessionId), chatGroups: normalizedGroups.slice(0, MAX_CHAT_REFERENCES).map(group => ({ ...group, sessionIds: (group.id === groupId ? [sessionId, ...group.sessionIds.filter(id => id !== sessionId)] : group.sessionIds.filter(id => id !== sessionId)).slice(0, MAX_CHAT_REFERENCES) })) }); closeMenu(groupId);
  }
  function menuKeyDown(event: React.KeyboardEvent<HTMLDivElement>): void {
    const items = [...(menuRef.current?.querySelectorAll<HTMLButtonElement>('[role="menuitem"]') ?? [])];
    const index = items.indexOf(document.activeElement as HTMLButtonElement);
    const target = event.key === 'Home' ? 0 : event.key === 'End' ? items.length - 1 : event.key === 'ArrowDown' ? (index + 1) % items.length : event.key === 'ArrowUp' ? (index - 1 + items.length) % items.length : -1;
    if (target >= 0) { event.preventDefault(); items[target]?.focus(); items[target]?.scrollIntoView({ block: 'nearest' }); }
  }
  function trapDialogFocus(event: React.KeyboardEvent<HTMLDivElement>): void {
    if (event.key !== 'Tab') return;
    const items = [...(dialogRef.current?.querySelectorAll<HTMLElement>('input, button') ?? [])];
    if (!items.length) return;
    const index = items.indexOf(document.activeElement as HTMLElement);
    if (event.shiftKey && index <= 0) { event.preventDefault(); items.at(-1)?.focus(); }
    else if (!event.shiftKey && index === items.length - 1) { event.preventDefault(); items[0]?.focus(); }
  }
  function renderRow(entry: ChatOrganizationEntry): JSX.Element { return <SessionRow key={entry.sessionId} entry={entry} needsAnswer={needsAnswerSessionIds.includes(entry.sessionId)} onNeedsAnswer={onNeedsAnswer} live={entry.sessionId === liveSessionId} selected={entry.sessionId === selectedSessionId} disabled={selectionDisabled} onSelectSession={onSelectSession} onOpenMenu={openMenu} controlRef={node => { if (node) sessionControlRefs.current.set(entry.sessionId, node); else sessionControlRefs.current.delete(entry.sessionId); }} />; }
  function renderSection(section: ChatSection): JSX.Element {
    const folderPath = section.folderPath ?? '';
    const notice = section.kind === 'folder' && folderPath ? folderNotices[folderPath] : undefined;
    const collapsed = (section.kind === 'group' && groupsCollapsed.includes(section.id)) || (section.kind === 'folder' && folderPath !== '' && foldersCollapsed.includes(folderPath));
    const heading = section.kind === 'folder'
      ? <button ref={node => { if (node) groupHeaderRefs.current.set(section.id, node); else groupHeaderRefs.current.delete(section.id); }} data-chat-folder={folderPath || undefined} type="button" className={`woven-chat-section-heading woven-chat-section-heading--folder${section.current ? ' is-current' : ''}`} aria-expanded={!collapsed}
          title={folderPath ? `${folderPath}${section.current ? ' · folder for new chats' : ''}` : 'Chats without a recorded folder'}
          onClick={() => { if (!folderPath) return; onOrganizationChange?.({ foldersCollapsed: collapsed ? foldersCollapsed.filter(path => path !== folderPath) : [...foldersCollapsed, folderPath] }); }}>
          <span><span aria-hidden="true">▱ </span>{section.label}{section.current ? <span className="woven-chat-section-current" aria-label="Folder for new chats"> · current</span> : null}</span><span>{section.entries.length}</span>
        </button>
      : section.kind === 'group'
      ? <button ref={node => { if (node) groupHeaderRefs.current.set(section.id, node); else groupHeaderRefs.current.delete(section.id); }} data-chat-group-id={section.id} type="button" className="woven-chat-section-heading" aria-expanded={!collapsed}
          onDragOver={event => event.preventDefault()}
          onDrop={event => { event.preventDefault(); const id = event.dataTransfer.getData('text/chirality-session-id'); if (id) moveToGroup(id, section.id); }}
          onClick={() => onOrganizationChange?.({ groupsCollapsed: collapsed ? groupsCollapsed.filter(id => id !== section.id) : [...groupsCollapsed, section.id] })}>
          <span>{section.label}</span><span>{section.entries.length}</span>
        </button>
      : <h2 className="woven-chat-section-label">{section.label}</h2>;
    return <section className={section.kind === 'folder' ? 'woven-chat-section woven-chat-section--folder' : 'woven-chat-section'} key={section.id} data-folder-notice={notice?.kind}>{heading}
      {notice && !collapsed ? <div className={notice.kind === 'unavailable' ? 'woven-folder-notice woven-folder-notice--unavailable' : 'woven-folder-notice'} role={notice.kind === 'unavailable' ? 'alert' : 'note'}>
        <p>{notice.message}</p>
        {notice.kind === 'unavailable' ? <div className="woven-folder-notice-actions">
          {onLocateFolder ? <button type="button" disabled={selectionDisabled} onClick={() => onLocateFolder(folderPath)}>Locate folder…</button> : null}
          {onForgetFolder ? <button type="button" className="button-muted" onClick={() => onForgetFolder(folderPath)}>Forget folder</button> : null}
        </div> : null}
      </div> : null}
      {!collapsed ? <ul className="woven-navigator-session-list" aria-label={`${section.label} chats`}>{section.entries.map(renderRow)}</ul> : null}</section>;
  }
  const activeEntry = menuSessionId ? entryById.get(menuSessionId) : undefined; const pinned = menuSessionId ? chatPins.includes(menuSessionId) : false;
  return <nav className="woven-navigator" aria-label="Workspace Navigator">
    <header className="woven-navigator-brand">Chirality</header>
    <div className="woven-navigator-sections" aria-label="Workspace chats">
      <div className="woven-chat-search"><input ref={searchRef} type="search" value={query} placeholder="Search chats" aria-label="Search chats" title="Search chat titles and messages" onChange={event => setQuery(event.target.value)} onKeyDown={event => { if (event.key === 'Escape') { event.preventDefault(); setQuery(''); } }} /></div>
      <div className="woven-chat-visibility" aria-label="Chat visibility">
        <button type="button" aria-pressed={visibility === 'active'} onClick={() => setVisibility('active')}>Chats</button>
        <button type="button" aria-pressed={visibility === 'archived'} onClick={() => setVisibility('archived')}>Archived ({chatArchived.length})</button>
        <button type="button" aria-pressed={visibility === 'deleted'} onClick={() => setVisibility('deleted')}>Locally deleted ({chatDeleted.length})</button>
      </div>
      {onNewChat ? <button type="button" className="woven-new-chat" disabled={selectionDisabled} onClick={onNewChat}><span aria-hidden="true">＋</span> New chat</button> : null}
      <button type="button" className="woven-nav-item woven-nav-item--active" aria-current={activeSurface === 'dialogue' ? 'page' : undefined} onClick={() => onOpenSurface('dialogue')}><span>Current chat</span></button>
      <div className="woven-navigator-sessions">{sessionsError ? <p className="panel-error" role="alert">{sessionsError}</p> : null}{sessionsLoading ? <p className="panel-empty">Loading recorded sessions…</p> : null}{selectionDisabled ? <p role="status">Paused while a turn is running.</p> : null}{!sessionsLoading && !sessionsError && entries.length === 0 ? <p className="panel-empty">No recorded sessions.</p> : null}
        {normalizedQuery ? <><section className="woven-chat-section"><h2 className="woven-chat-section-label">Title matches</h2><ul className="woven-navigator-session-list" aria-label="Title matches">{titleMatches.map(renderRow)}</ul>{titleMatches.length === 0 ? <p className="panel-empty">No title matches.</p> : null}</section><section className="woven-chat-section"><h2 className="woven-chat-section-label">Message matches</h2>{messageSearchPending ? <p className="panel-empty" role="status">Searching messages…</p> : <ul className="woven-navigator-session-list" aria-label="Message matches">{messageMatches.map(renderRow)}</ul>}{!messageSearchPending && messageMatches.length === 0 ? <p className="panel-empty">No message matches.</p> : null}</section></> : sections.map(renderSection)}
      </div>
    </div>
    {footerSlot ? <footer className="woven-compatibility">{footerSlot}</footer> : null}
    {activeEntry ? <div className="woven-chat-menu" role="menu" ref={menuRef} aria-label={`Actions for ${activeEntry.title}`} onKeyDown={menuKeyDown}>
      {visibility !== 'active' ? <><button role="menuitem" type="button" onClick={() => { onOrganizationChange?.(visibility === 'archived' ? { chatArchived: chatArchived.filter(id => id !== activeEntry.sessionId) } : { chatDeleted: chatDeleted.filter(id => id !== activeEntry.sessionId) }); closeMenu(); }}>Restore</button><button role="menuitem" type="button" onClick={() => closeMenu()}>Close menu</button></> : <>
      <button role="menuitem" type="button" onClick={() => { setDialogValue(activeEntry.title); setDialog('rename'); }}>Rename</button><button role="menuitem" type="button" onClick={() => { onOrganizationChange?.({ chatPins: (pinned ? chatPins.filter(id => id !== activeEntry.sessionId) : [activeEntry.sessionId, ...chatPins.filter(id => id !== activeEntry.sessionId)]).slice(0, MAX_CHAT_REFERENCES) }); closeMenu(); }}>{pinned ? 'Unpin' : 'Pin'}</button>
      {normalizedGroups.map(group => <button role="menuitem" type="button" key={group.id} onClick={() => moveToGroup(activeEntry.sessionId, group.id)}>Move to {group.name}</button>)}<button role="menuitem" type="button" onClick={() => { setDialogValue(''); setDialog('new-group'); }}>New group…</button><button role="menuitem" type="button" onClick={() => { onOrganizationChange?.({ chatArchived: [...chatArchived.filter(id => id !== activeEntry.sessionId), activeEntry.sessionId].slice(-MAX_CHAT_REFERENCES), chatDeleted: chatDeleted.filter(id => id !== activeEntry.sessionId) }); closeMenu(); }}>Archive</button><hr /><button role="menuitem" type="button" onClick={() => setDialog('delete')}>Delete…</button><button role="menuitem" type="button" onClick={() => closeMenu()}>Close menu</button></>}
    </div> : null}
    {activeEntry && dialog ? <div className="woven-chat-dialog-backdrop"><div ref={dialogRef} className="woven-chat-dialog" role="dialog" aria-modal="true" aria-labelledby="woven-chat-dialog-title" onKeyDown={trapDialogFocus}><h2 id="woven-chat-dialog-title">{dialog === 'rename' ? 'Rename chat' : dialog === 'new-group' ? 'New group' : 'Delete chat locally?'}</h2>{dialog !== 'delete' ? <label>{dialog === 'rename' ? 'Chat title' : 'Group name'}<input data-dialog-initial autoFocus maxLength={CHAT_LABEL_LIMIT} value={dialogValue} onChange={event => setDialogValue(event.target.value)} /></label> : <p>The runtime session record will remain available.</p>}<div className="woven-chat-dialog-actions"><button data-dialog-initial={dialog === 'delete' ? true : undefined} type="button" onClick={() => { setDialog(null); setDialogValue(''); }}>Cancel</button><button type="button" onClick={() => {
      if (dialog === 'delete') { const id = activeEntry.sessionId; onOrganizationChange?.({ chatDeleted: [...chatDeleted.filter(item => item !== id), id].slice(-MAX_CHAT_REFERENCES), chatArchived: chatArchived.filter(item => item !== id) }); closeMenu(); return; }
      const label = sanitizeChatLabel(dialogValue); if (!label) return;
      if (dialog === 'rename') { onOrganizationChange?.({ chatTitles: Object.fromEntries([...Object.entries(chatTitles), [activeEntry.sessionId, label]].slice(-MAX_CHAT_ANNOTATIONS)) }); closeMenu(); }
      else { const id = `group-${Date.now().toString(36)}`; onOrganizationChange?.({ chatPins: chatPins.filter(item => item !== activeEntry.sessionId), chatGroups: [...normalizedGroups.map(group => ({ ...group, sessionIds: group.sessionIds.filter(item => item !== activeEntry.sessionId) })), { id, name: label, sessionIds: [activeEntry.sessionId] }].slice(-MAX_CHAT_REFERENCES) }); closeMenu(); }
    }}>{dialog === 'delete' ? 'Delete locally' : dialog === 'rename' ? 'Save' : 'Create group'}</button></div></div></div> : null}
  </nav>;
}
