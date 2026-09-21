import React from 'react';
import { act, create, type ReactTestRenderer } from 'react-test-renderer';
import { renderToStaticMarkup } from 'react-dom/server';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import type { SessionRecord } from '@chirality/runtime-contracts/types';
import { Navigator, buildNavigatorSessionGroups } from '../../components/woven-dialogue/navigator';

vi.mock('next/link', () => ({ default: ({ children, ...props }: React.ComponentProps<'a'>) => <a {...props}>{children}</a> }));
vi.mock('../../components/shell/document-view', () => ({ handoffDocument: vi.fn(async () => {}) }));

function session(sessionId: string, updatedAt: string, persona = 'TASK', projectRoot = `/roots/${sessionId}`): SessionRecord {
  return { sessionId, projectRoot, persona, mode: 'CHAT', createdAt: updatedAt, updatedAt };
}
const SESSIONS = [session('today', '2026-09-07T10:15:00Z', 'WORKING_ITEMS', '/one/project'), session('yesterday', '2026-09-06T09:00:00Z', 'RESEARCH', ''), session('week', '2026-09-03T08:00:00Z', 'CHANGE', '/two/folder')];

type State = { chatTitles: Record<string, string>; chatPins: string[]; chatArchived: string[]; chatDeleted: string[]; chatGroups: { id: string; name: string; sessionIds: string[] }[]; groupsCollapsed: string[] };
let tree: ReactTestRenderer | undefined;
let state: State;
function Fixture({ searchMessages = async () => [] }: { searchMessages?: (query: string, sessions: readonly SessionRecord[]) => Promise<string[]> }) {
  const [current, update] = React.useState<State>(state); state = current;
  return <Navigator activeSurface="dialogue" legacyHref="/?legacy=1" onOpenSurface={vi.fn()} sessions={SESSIONS}
    referenceDay="2026-09-07" firstOperatorMessages={{ today: 'First operator request' }} {...current}
    searchMessages={searchMessages} onSelectSession={vi.fn()} onOrganizationChange={patch => update(value => ({ ...value, ...patch }))} />;
}
function buttons(label: string) { return tree!.root.findAllByType('button').filter(button => (button.props['aria-label'] ?? button.children.join('')) === label); }
function click(label: string) { act(() => buttons(label)[0].props.onClick({ currentTarget: { focus: vi.fn() } })); }

beforeEach(() => {
  state = { chatTitles: {}, chatPins: [], chatArchived: [], chatDeleted: [], chatGroups: [{ id: 'client', name: 'Client', sessionIds: [] }], groupsCollapsed: [] };
  vi.stubGlobal('window', { setTimeout: (callback: () => void, delay: number) => globalThis.setTimeout(callback, delay), clearTimeout: (id: ReturnType<typeof setTimeout>) => globalThis.clearTimeout(id), addEventListener: vi.fn(), removeEventListener: vi.fn(), requestAnimationFrame: (callback: () => void) => callback() });
});
afterEach(() => { if (tree) act(() => tree!.unmount()); tree = undefined; vi.unstubAllGlobals(); vi.useRealTimers(); });

describe('Woven Dialogue Navigator', () => {
  it('renders folder sections, derived title/time, folder basename/no-folder, and unchanged live/selected/streaming guards', () => {
    const html = renderToStaticMarkup(<Navigator activeSurface="dialogue" legacyHref="/?legacy=1" onOpenSurface={vi.fn()} sessions={SESSIONS} referenceDay="2026-09-07" firstOperatorMessages={{ today: 'First operator request' }} liveSessionId="today" selectedSessionId="week" selectionDisabled currentRoot="/two/folder" />);
    expect(html).toContain('data-chat-folder="/one/project"'); expect(html).toContain('data-chat-folder="/two/folder"'); expect(html).toContain('No folder chats');
    expect(html.indexOf('data-chat-folder="/two/folder"')).toBeLessThan(html.indexOf('data-chat-folder="/one/project"'));
    expect(html).toContain('Folder for new chats'); expect(html).not.toContain('Today');
    expect(html).toContain('First operator request'); expect(html).toContain('10:15'); expect(html).toContain('project'); expect(html).toContain('No folder');
    expect(html).toContain('title="/one/project"'); expect(html).toContain('aria-label="Live session"'); expect(html).toMatch(/data-session-id="week"[^>]*aria-pressed="true"/);
    expect(html).toContain('Paused while a turn is running.'); expect(html).toContain('Reveal folder for First operator request (today)');
  });

  it('filters titles immediately and debounces message search with stale-result suppression', async () => {
    vi.useFakeTimers();
    const resolvers: ((ids: string[]) => void)[] = []; const search = vi.fn(() => new Promise<string[]>(resolve => resolvers.push(resolve)));
    await act(async () => { tree = create(<Fixture searchMessages={search} />); });
    const input = tree!.root.findByProps({ 'aria-label': 'Search chats' });
    act(() => input.props.onChange({ target: { value: 'first' } }));
    expect(tree!.root.findByProps({ 'aria-label': 'Title matches' }).findAllByProps({ 'data-session-id': 'today' })).toHaveLength(1);
    expect(search).not.toHaveBeenCalled(); await act(async () => { vi.advanceTimersByTime(250); }); expect(search).toHaveBeenCalledTimes(1);
    act(() => input.props.onChange({ target: { value: 'change' } })); await act(async () => { vi.advanceTimersByTime(250); }); expect(search).toHaveBeenCalledTimes(2);
    await act(async () => resolvers[0](['today'])); expect(tree!.root.findAllByProps({ 'data-session-id': 'today' })).toHaveLength(0);
    await act(async () => resolvers[1](['week'])); expect(tree!.root.findByProps({ 'aria-label': 'Message matches' }).findAllByProps({ 'data-session-id': 'week' })).toHaveLength(1);
    act(() => input.props.onKeyDown({ key: 'Escape', preventDefault: vi.fn() })); expect(input.props.value).toBe('');
  });

  it('opens the same accessible menu from overflow and context-click, restores focus, and supports rename/pin/unpin/archive', async () => {
    await act(async () => { tree = create(<Fixture />); });
    click('Chat actions for First operator request');
    expect(tree!.root.findByProps({ role: 'menu' }).props['aria-label']).toContain('First operator request');
    act(() => tree!.root.findAllByType('button').find(button => button.children.includes('Rename'))!.props.onClick());
    const rename = tree!.root.findByProps({ role: 'dialog' }); expect(rename.findByType('input').props.maxLength).toBe(80);
    act(() => rename.findByType('input').props.onChange({ target: { value: '  Renamed chat  ' } }));
    act(() => rename.findAllByType('button').find(button => button.children.includes('Save'))!.props.onClick()); expect(state.chatTitles.today).toBe('Renamed chat');
    click('Chat actions for Renamed chat'); act(() => tree!.root.findAllByType('button').find(button => button.children.includes('Pin'))!.props.onClick()); expect(state.chatPins).toEqual(['today']);
    click('Chat actions for Renamed chat'); act(() => tree!.root.findAllByType('button').find(button => button.children.includes('Unpin'))!.props.onClick()); expect(state.chatPins).toEqual([]);
    const row = tree!.root.findByProps({ 'data-session-id': 'today' }).parent!.parent!;
    act(() => row.props.onContextMenu({ preventDefault: vi.fn(), currentTarget: { focus: vi.fn() } })); expect(tree!.root.findByProps({ role: 'menu' })).toBeTruthy();
    act(() => tree!.root.findAllByType('button').find(button => button.children.includes('Archive'))!.props.onClick()); expect(state.chatArchived).toEqual(['today']);
    expect(tree!.root.findAllByProps({ 'data-session-id': 'today' })).toHaveLength(0);
  });

  it('creates/moves groups, supports drag and collapse, and locally deletes while the original record remains recoverable', async () => {
    state.chatPins = ['today'];
    state.chatGroups[0].sessionIds = ['today'];
    await act(async () => { tree = create(<Fixture />); });
    click('Chat actions for First operator request'); act(() => tree!.root.findAllByType('button').find(button => button.children.includes('New group…'))!.props.onClick());
    const dialog = tree!.root.findByProps({ role: 'dialog' }); act(() => dialog.findByType('input').props.onChange({ target: { value: 'Alpha' } })); act(() => dialog.findAllByType('button').find(button => button.children.includes('Create group'))!.props.onClick());
    expect(state.chatPins).toEqual([]); expect(state.chatGroups.map(group => group.name)).toEqual(['Client', 'Alpha']);
    expect(state.chatGroups.find(group => group.name === 'Client')!.sessionIds).toEqual([]); expect(state.chatGroups.find(group => group.name === 'Alpha')!.sessionIds).toEqual(['today']);
    const client = tree!.root.findAllByProps({ className: 'woven-chat-section-heading' }).find(node => node.findAllByType('span').some(span => span.children.includes('Client')))!;
    act(() => client.props.onDrop({ preventDefault: vi.fn(), dataTransfer: { getData: () => 'week' } })); expect(state.chatGroups.find(group => group.id === 'client')!.sessionIds).toEqual(['week']);
    act(() => client.props.onClick()); expect(state.groupsCollapsed).toEqual(['client']);
    click('Chat actions for First operator request'); act(() => tree!.root.findAllByType('button').find(button => button.children.includes('Delete…'))!.props.onClick());
    act(() => tree!.root.findByProps({ role: 'dialog' }).findAllByType('button').find(button => button.children.includes('Delete locally'))!.props.onClick());
    expect(state).toMatchObject({ chatDeleted: ['today'], chatPins: [] }); expect(SESSIONS.some(item => item.sessionId === 'today')).toBe(true);
    click('Locally deleted (1)');
    click('Chat actions for First operator request');
    act(() => tree!.root.findAllByType('button').find(button => button.children.includes('Restore'))!.props.onClick());
    expect(state.chatDeleted).toEqual([]);
    click('Chats');
    expect(tree!.root.findAllByProps({ 'data-session-id': 'today' })).not.toHaveLength(0);
  });

  it('selects historical and unattributed sessions and exposes loading, error, and empty states', () => {
    const select = vi.fn(); const open = vi.fn();
    act(() => { tree = create(<Navigator activeSurface="dialogue" legacyHref="/?legacy=1" onOpenSurface={open} sessions={[SESSIONS[1]]} onSelectSession={select} />); });
    act(() => tree!.root.findByProps({ 'data-session-id': 'yesterday' }).props.onClick());
    expect(select).toHaveBeenCalledWith('yesterday'); expect(open).not.toHaveBeenCalled();
    act(() => tree!.update(<Navigator activeSurface="dialogue" legacyHref="/?legacy=1" onOpenSurface={open} sessionsLoading />));
    expect(tree!.root.findByType('nav').findAllByType('p').some(node => node.children.includes('Loading recorded sessions…'))).toBe(true);
    act(() => tree!.update(<Navigator activeSurface="dialogue" legacyHref="/?legacy=1" onOpenSurface={open} sessionsError="Unable to list chats" />));
    expect(tree!.root.findByProps({ role: 'alert' }).children).toEqual(['Unable to list chats']);
    act(() => tree!.update(<Navigator activeSurface="dialogue" legacyHref="/?legacy=1" onOpenSurface={open} />));
    expect(tree!.root.findAllByType('p').some(node => node.children.includes('No recorded sessions.'))).toBe(true);
  });

  it('renders invalid dates safely and preserves exact persona in friendly-title tooltips', () => {
    const odd = [session('raw-id', 'invalid', ''), session('helper', '2026-09-07T00:00:00Z', 'HELP_HUMAN')];
    const html = renderToStaticMarkup(<Navigator activeSurface="dialogue" legacyHref="/?legacy=1" onOpenSurface={vi.fn()} sessions={odd} onSelectSession={vi.fn()} />);
    expect(html).toContain('raw-id'); expect(html).not.toContain('Invalid Date');
    expect(html).toMatch(/title="Assistant · HELP_HUMAN · helper"/);
  });

  it('restores real focus targets after Escape, outside dismissal, dialog cancel, and commits from both entry paths', () => {
    const listeners: Record<string, (event: any) => void> = {};
    const documentListeners: Record<string, (event: any) => void> = {};
    const fakeDocument: { activeElement: unknown; addEventListener: (name: string, fn: (event: any) => void) => void; removeEventListener: ReturnType<typeof vi.fn> } = { activeElement: null, addEventListener: (name, fn) => { documentListeners[name] = fn; }, removeEventListener: vi.fn() };
    const focusable = () => { const node = { isConnected: true, focus: () => { fakeDocument.activeElement = node; } }; return node; };
    const overflow = focusable(); const contextRow = focusable(); const menuFirst = focusable(); const dialogFirst = focusable();
    const menuNode = { contains: () => false, querySelector: () => menuFirst, querySelectorAll: () => [menuFirst] };
    const dialogNode = { querySelector: () => dialogFirst, querySelectorAll: () => [dialogFirst] };
    vi.stubGlobal('document', fakeDocument);
    vi.stubGlobal('window', { addEventListener: (name: string, fn: (event: any) => void) => { listeners[name] = fn; }, removeEventListener: vi.fn(), requestAnimationFrame: (fn: () => void) => fn() });
    act(() => { tree = create(<Fixture />, { createNodeMock: element => element.type === 'div' && element.props.role === 'menu' ? menuNode : element.type === 'div' && element.props.role === 'dialog' ? dialogNode : null }); });
    const action = () => tree!.root.findByProps({ 'aria-label': 'Chat actions for First operator request' });
    act(() => action().props.onClick({ currentTarget: overflow })); expect(fakeDocument.activeElement).toBe(menuFirst);
    act(() => listeners.keydown({ key: 'Escape', metaKey: false, ctrlKey: false, preventDefault: vi.fn() })); expect(fakeDocument.activeElement).toBe(overflow);
    const row = tree!.root.findByProps({ 'data-session-id': 'today' }).parent!.parent!;
    act(() => row.props.onContextMenu({ preventDefault: vi.fn(), currentTarget: contextRow }));
    act(() => documentListeners.mousedown({ target: {} })); expect(fakeDocument.activeElement).toBe(contextRow);
    act(() => action().props.onClick({ currentTarget: overflow }));
    act(() => tree!.root.findAllByType('button').find(button => button.children.includes('Rename'))!.props.onClick()); expect(fakeDocument.activeElement).toBe(dialogFirst);
    act(() => tree!.root.findByProps({ role: 'dialog' }).findAllByType('button').find(button => button.children.includes('Cancel'))!.props.onClick()); expect(fakeDocument.activeElement).toBe(menuFirst);
    act(() => tree!.root.findByProps({ role: 'menu' }).findAllByType('button').find(button => button.children.includes('Close menu'))!.props.onClick()); expect(fakeDocument.activeElement).toBe(overflow);
    act(() => row.props.onContextMenu({ preventDefault: vi.fn(), currentTarget: contextRow }));
    act(() => tree!.root.findAllByType('button').find(button => button.children.includes('New group…'))!.props.onClick());
    act(() => tree!.root.findByProps({ role: 'dialog' }).findByType('input').props.onChange({ target: { value: 'Focused' } }));
    act(() => tree!.root.findByProps({ role: 'dialog' }).findAllByType('button').find(button => button.children.includes('Create group'))!.props.onClick()); expect(fakeDocument.activeElement).toBe(contextRow);
  });

  it('keeps all actions reachable at the 200-group cap and scrolls keyboard focus into view', () => {
    state.chatGroups = Array.from({ length: 200 }, (_, index) => ({ id: `g-${index}`, name: `Group ${String(index).padStart(3, '0')}`, sessionIds: [] }));
    const items = Array.from({ length: 206 }, () => ({ focus: vi.fn(), scrollIntoView: vi.fn() }));
    const menuNode = { contains: () => true, querySelector: () => items[0], querySelectorAll: () => items };
    vi.stubGlobal('document', { activeElement: items[0], addEventListener: vi.fn(), removeEventListener: vi.fn() });
    act(() => { tree = create(<Fixture />, { createNodeMock: element => element.type === 'div' && element.props.role === 'menu' ? menuNode : null }); });
    act(() => tree!.root.findByProps({ 'aria-label': 'Chat actions for First operator request' }).props.onClick({ currentTarget: { isConnected: true, focus: vi.fn() } }));
    const menu = tree!.root.findByProps({ role: 'menu' });
    expect(menu.findAllByProps({ role: 'menuitem' })).toHaveLength(206);
    act(() => menu.props.onKeyDown({ key: 'End', preventDefault: vi.fn() }));
    expect(items.at(-1)!.focus).toHaveBeenCalled(); expect(items.at(-1)!.scrollIntoView).toHaveBeenCalledWith({ block: 'nearest' });
  });

  it('resolves replacement-row, group-header, and stable-search focus after invokers detach', () => {
    const frames: Array<() => void> = []; (window as any).requestAnimationFrame = (callback: () => void) => { frames.push(callback); return frames.length; };
    const flushFocus = () => act(() => { frames.splice(0).forEach(callback => callback()); });
    const sessionNodes: Record<string, Array<{ focus: ReturnType<typeof vi.fn> }>> = {}; const groupNodes: Record<string, { focus: ReturnType<typeof vi.fn> }> = {};
    const searchNode = { focus: vi.fn() }; const menuItem = { focus: vi.fn(), scrollIntoView: vi.fn() };
    const nodeFor = (element: any) => {
      if (element.type === 'button' && element.props['data-session-id']) { const node = { focus: vi.fn() }; (sessionNodes[element.props['data-session-id']] ??= []).push(node); return node; }
      if (element.type === 'button' && element.props['data-chat-group-id']) return (groupNodes[element.props['data-chat-group-id']] ??= { focus: vi.fn() });
      if (element.type === 'input' && element.props['aria-label'] === 'Search chats') return searchNode;
      if (element.type === 'div' && element.props.role === 'menu') return { contains: () => true, querySelector: () => menuItem, querySelectorAll: () => [menuItem] };
      return null;
    };
    vi.stubGlobal('document', { activeElement: menuItem, addEventListener: vi.fn(), removeEventListener: vi.fn() });
    act(() => { tree = create(<Fixture />, { createNodeMock: nodeFor }); });
    const action = () => tree!.root.findAllByType('button').find(button => String(button.props['aria-label'] ?? '').startsWith('Chat actions'))!;
    const detachedOverflow = { isConnected: false, focus: vi.fn() };
    act(() => action().props.onClick({ currentTarget: detachedOverflow }));
    act(() => tree!.root.findByProps({ role: 'menu' }).findAllByType('button').find(button => button.children.includes('Pin'))!.props.onClick());
    flushFocus();
    expect(detachedOverflow.focus).not.toHaveBeenCalled(); expect(sessionNodes.today.at(-1)!.focus).toHaveBeenCalled();

    act(() => tree!.root.findAllByProps({ className: 'woven-chat-section-heading' }).find(node => node.findAllByType('span').some(span => span.children.includes('Client')))!.props.onClick());
    const contextRow = tree!.root.findByProps({ 'data-session-id': 'today' }).parent!.parent!; const detachedContext = { isConnected: false, focus: vi.fn() };
    act(() => contextRow.props.onContextMenu({ preventDefault: vi.fn(), currentTarget: detachedContext }));
    act(() => tree!.root.findByProps({ role: 'menu' }).findAllByType('button').find(button => button.children.join('') === 'Move to Client')!.props.onClick());
    flushFocus();
    expect(detachedContext.focus).not.toHaveBeenCalled(); expect(groupNodes.client.focus).toHaveBeenCalled();

    act(() => tree!.root.findByProps({ 'data-chat-group-id': 'client' }).props.onClick());
    act(() => action().props.onClick({ currentTarget: detachedOverflow }));
    act(() => tree!.root.findByProps({ role: 'menu' }).findAllByType('button').find(button => button.children.includes('Archive'))!.props.onClick());
    flushFocus();
    expect(searchNode.focus).toHaveBeenCalled();
    click('Archived (1)'); act(() => action().props.onClick({ currentTarget: detachedOverflow }));
    act(() => tree!.root.findByProps({ role: 'menu' }).findAllByType('button').find(button => button.children.includes('Restore'))!.props.onClick());
    flushFocus();
    expect(searchNode.focus).toHaveBeenCalledTimes(2);
  });
});

describe('legacy session projection compatibility', () => {
  it('retains deterministic recency, surface attribution, and persona fallback for existing callers', () => {
    const projected = buildNavigatorSessionGroups(SESSIONS, { week: 'workbench' });
    expect(projected.all.map(entry => entry.sessionId)).toEqual(['today', 'yesterday', 'week']);
    expect(projected.bySurface.workbench.map(entry => entry.sessionId)).toEqual(['week']);
  });
});

describe('Navigator folder sections', () => {
  it('collapses folder sections through the organisation patch and shows recovery actions for an unavailable folder', () => {
    const locate = vi.fn(); const forget = vi.fn(); const change = vi.fn();
    act(() => { tree = create(<Navigator activeSurface="dialogue" legacyHref="/?legacy=1" onOpenSurface={vi.fn()} sessions={SESSIONS} referenceDay="2026-09-07" onSelectSession={vi.fn()} onOrganizationChange={change}
      folderNotices={{ '/two/folder': { kind: 'unavailable', message: 'This folder is missing or inaccessible.' }, '/one/project': { kind: 'indexed', message: 'Listed from this App’s index.' } }} onLocateFolder={locate} onForgetFolder={forget} foldersCollapsed={['/one/project']} />); });
    const headings = tree!.root.findAll(node => node.type === 'button' && typeof node.props['data-chat-folder'] === 'string');
    expect(headings.map(node => [node.props['data-chat-folder'], node.props['aria-expanded']])).toEqual([['/one/project', false], ['/two/folder', true]]);
    act(() => headings[1].props.onClick());
    expect(change).toHaveBeenCalledWith({ foldersCollapsed: ['/one/project', '/two/folder'] });
    act(() => headings[0].props.onClick());
    expect(change).toHaveBeenCalledWith({ foldersCollapsed: [] });
    const alert = tree!.root.findByProps({ role: 'alert' });
    expect(alert.findByType('p').children.join('')).toContain('missing or inaccessible');
    act(() => alert.findAllByType('button').find(button => button.children.join('') === 'Locate folder…')!.props.onClick());
    act(() => alert.findAllByType('button').find(button => button.children.join('') === 'Forget folder')!.props.onClick());
    expect(locate).toHaveBeenCalledWith('/two/folder'); expect(forget).toHaveBeenCalledWith('/two/folder');
    // A collapsed folder hides its rows and its note.
    expect(tree!.root.findAllByProps({ 'data-session-id': 'today' })).toHaveLength(0);
    expect(tree!.root.findAllByProps({ role: 'note' })).toHaveLength(0);
  });
});
