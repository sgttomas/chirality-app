import React from 'react';
import renderer, { act } from 'react-test-renderer';
import { afterEach, describe, expect, it, vi } from 'vitest';
import type { SessionRecord } from '@chirality/runtime-contracts/types';
import { Navigator, buildNavigatorSessionGroups } from '../../components/woven-dialogue/navigator';

vi.mock('next/link', () => ({ default: ({ children, ...props }: React.ComponentProps<'a'>) => <a {...props}>{children}</a> }));

const record = (sessionId: string, projectRoot: unknown, persona = 'HELP_HUMAN', updatedAt = '2026-09-06') => ({
  sessionId, projectRoot, persona, mode: 'governed', createdAt: updatedAt, updatedAt
} as SessionRecord);
const trees: renderer.ReactTestRenderer[] = [];
afterEach(() => { act(() => trees.splice(0).forEach(tree => tree.unmount())); vi.unstubAllGlobals(); });
function mount(sessions: SessionRecord[], overrides: Partial<React.ComponentProps<typeof Navigator>> = {}) {
  const props = { activeSurface: 'dialogue' as const, legacyHref: '/?legacy=1', onOpenSurface: vi.fn(), onSelectSession: vi.fn(), onNewChat: vi.fn(), sessions, ...overrides };
  let tree!: renderer.ReactTestRenderer;
  act(() => { tree = renderer.create(<Navigator {...props} />); });
  trees.push(tree);
  return { tree, props };
}
function reveal(tree: renderer.ReactTestRenderer, id: string) {
  return tree.root.findAllByType('button').find(button => button.props['aria-label']?.endsWith(`(${id})`))!;
}
function alerts(tree: renderer.ReactTestRenderer) { return tree.root.findAllByProps({ role: 'alert' }).map(node => node.children.join('')); }
function bridge() {
  const handoff = vi.fn().mockResolvedValue({ ok: true });
  vi.stubGlobal('window', { chirality: { document: { handoff } } });
  return handoff;
}

describe('recorded-chat Reveal', () => {
  it('uses each recorded root across reordered/refetched rows without selecting or opening a surface', async () => {
    const handoff = bridge();
    const a = record('a', '/recorded/a'), b = record('b', '/recorded/b', 'WORKING_ITEMS');
    const { tree, props } = mount([a, b]);
    await act(async () => { reveal(tree, 'a').props.onClick(); });
    expect(handoff).toHaveBeenLastCalledWith({ action: 'reveal-root', projectRoot: '/recorded/a' });
    act(() => { tree.update(<Navigator {...props} sessions={[{ ...b, updatedAt: '2026-09-07' }, { ...a }]} />); });
    await act(async () => { reveal(tree, 'b').props.onClick(); });
    expect(handoff).toHaveBeenLastCalledWith({ action: 'reveal-root', projectRoot: '/recorded/b' });
    expect(props.onSelectSession).not.toHaveBeenCalled();
    expect(props.onNewChat).not.toHaveBeenCalled();
    expect(props.onOpenSurface).not.toHaveBeenCalled();
    expect(a.projectRoot).toBe('/recorded/a');
    expect(b.projectRoot).toBe('/recorded/b');
  });

  it.each([undefined, null, 42, {}, '', '  ', 'relative/path', '/bad\nroot', '/bad\0root'])('explains invalid recorded root %j without calling native actions', async root => {
    const handoff = bridge();
    const { tree } = mount([record('a', root)]);
    await act(async () => { reveal(tree, 'a').props.onClick(); });
    expect(alerts(tree)).toEqual(['This chat has no valid recorded folder to reveal.']);
    expect(handoff).not.toHaveBeenCalled();
  });

  it('explains missing desktop bridge and retries when the bridge becomes available', async () => {
    vi.stubGlobal('window', {});
    const { tree } = mount([record('a', '/recorded/a')]);
    await act(async () => { reveal(tree, 'a').props.onClick(); });
    expect(alerts(tree)).toEqual(['Open the desktop app to use native document actions.']);
    expect(reveal(tree, 'a').props['aria-label']).toContain('Retry revealing');
    const handoff = bridge();
    await act(async () => { reveal(tree, 'a').props.onClick(); });
    expect(handoff).toHaveBeenCalledOnce();
    expect(alerts(tree)).toEqual([]);
  });

  it.each([
    { code: 'FILE_NOT_FOUND', message: 'File or Working Root no longer exists.' },
    { code: 'UNAUTHORIZED_SENDER', message: 'Document action rejected for this sender.' },
    { code: 'REVEAL_FAILED', message: 'Finder unavailable' }
  ])('keeps typed native failure $code visible with a retry', async error => {
    const handoff = bridge(); handoff.mockResolvedValueOnce({ ok: false, error });
    const { tree } = mount([record('a', '/recorded/a')]);
    await act(async () => { reveal(tree, 'a').props.onClick(); });
    expect(alerts(tree)).toEqual([error.message]);
    expect(reveal(tree, 'a').props.disabled).toBe(false);
    await act(async () => { reveal(tree, 'a').props.onClick(); });
    expect(alerts(tree)).toEqual([]);
  });

  it('keeps rejected promises visible', async () => {
    const handoff = bridge(); handoff.mockRejectedValue(new Error('Native bridge disconnected.'));
    const { tree } = mount([record('a', '/recorded/a')]);
    await act(async () => { reveal(tree, 'a').props.onClick(); });
    expect(alerts(tree)).toEqual(['Native bridge disconnected.']);
  });

  it.each(['', '   '])('shows a retryable fallback for blank native failure message %j', async message => {
    const handoff = bridge();
    handoff.mockResolvedValueOnce({ ok: false, error: { code: 'REVEAL_FAILED', message } });
    const { tree } = mount([record('a', '/recorded/a')]);
    await act(async () => { reveal(tree, 'a').props.onClick(); });
    expect(alerts(tree)).toEqual(['Unable to reveal this chat’s folder. Try again.']);
    expect(reveal(tree, 'a').props['aria-label']).toContain('Retry revealing');
    expect(reveal(tree, 'a').props.disabled).toBe(false);
    await act(async () => { reveal(tree, 'a').props.onClick(); });
    expect(handoff).toHaveBeenCalledTimes(2);
    expect(alerts(tree)).toEqual([]);
  });

  it.each([new Error(), new Error('   ')])('shows a retryable fallback for rejected Error with blank message %#', async failure => {
    const handoff = bridge(); handoff.mockRejectedValueOnce(failure);
    const { tree } = mount([record('a', '/recorded/a')]);
    await act(async () => { reveal(tree, 'a').props.onClick(); });
    expect(alerts(tree)).toEqual(['Unable to reveal this chat’s folder. Try again.']);
    expect(reveal(tree, 'a').props['aria-label']).toContain('Retry revealing');
    expect(reveal(tree, 'a').props.disabled).toBe(false);
    await act(async () => { reveal(tree, 'a').props.onClick(); });
    expect(handoff).toHaveBeenCalledTimes(2);
    expect(alerts(tree)).toEqual([]);
  });

  it('deduplicates pending Reveal and never attaches its rejection to a replacement root', async () => {
    const handoff = bridge(); let reject!: (error: Error) => void;
    handoff.mockImplementationOnce(() => new Promise((_, fail) => { reject = fail; }));
    const { tree, props } = mount([record('a', '/old')]);
    act(() => { const click = reveal(tree, 'a').props.onClick; click(); click(); });
    expect(handoff).toHaveBeenCalledOnce();
    expect(reveal(tree, 'a').props.disabled).toBe(true);
    act(() => { tree.update(<Navigator {...props} sessions={[record('a', '/new')]} />); });
    await act(async () => { reveal(tree, 'a').props.onClick(); reject(new Error('Old folder disappeared.')); });
    expect(handoff).toHaveBeenLastCalledWith({ action: 'reveal-root', projectRoot: '/new' });
    expect(alerts(tree)).toEqual([]);
    expect(reveal(tree, 'a').props.disabled).toBe(false);
  });

  it('preserves pending row identity through reorder and refetch', async () => {
    const handoff = bridge(); let resolve!: (result: unknown) => void;
    handoff.mockImplementationOnce(() => new Promise(done => { resolve = done; }));
    const a = record('a', '/a'), b = record('b', '/b');
    const { tree, props } = mount([a, b]);
    act(() => { reveal(tree, 'a').props.onClick(); tree.update(<Navigator {...props} sessions={[{ ...b, updatedAt: '2026-09-07' }, { ...a }]} />); });
    expect(reveal(tree, 'a').props.disabled).toBe(true);
    expect(reveal(tree, 'b').props.disabled).toBe(false);
    await act(async () => { resolve({ ok: false, error: { message: 'A disappeared.' } }); });
    const rowA = tree.root.findByProps({ 'data-session-id': 'a' }).parent!.parent!;
    expect(rowA.findByProps({ role: 'alert' }).children).toEqual(['A disappeared.']);
    expect(reveal(tree, 'b').props['aria-label']).not.toContain('Retry');
  });

  it('remains a separate focusable native action while chat selection and New chat stay guarded', async () => {
    const handoff = bridge();
    const { tree, props } = mount([record('a', '/a')], { selectionDisabled: true });
    const selection = tree.root.findByProps({ 'data-session-id': 'a' });
    const action = reveal(tree, 'a');
    expect(action.type).toBe('button'); expect(action.props.type).toBe('button');
    expect(action.props.tabIndex).not.toBe(-1); expect(action.props.disabled).toBe(false);
    expect(action.parent).toBe(selection.parent); expect(action.props.title).toBe('Reveal in Finder · /a');
    expect(selection.props.disabled).toBe(true);
    act(() => { selection.props.onClick(); });
    await act(async () => { action.props.onClick(); });
    expect(handoff).toHaveBeenCalledOnce();
    expect(props.onSelectSession).not.toHaveBeenCalled(); expect(props.onNewChat).not.toHaveBeenCalled();
  });

  it('renders friendly role copy with exact recorded role in the tooltip and leaves fallback IDs unchanged', () => {
    const sessions = [record('a', '/a'), record('b', '/b', 'WORKING_ITEMS'), record('c', '/c', 'AUDIT_DEP_CLOSURE'), record('RAW_SESSION_ID', '/d', '')];
    const { tree } = mount(sessions);
    expect(buildNavigatorSessionGroups(sessions, {}).all.map(entry => entry.label)).toEqual(['Assistant', 'Working Items', 'Audit Dep Closure', 'RAW_SESSION_ID']);
    expect(tree.root.findByProps({ 'data-session-id': 'a' }).props.title).toContain('HELP_HUMAN');
    expect(tree.root.findByProps({ 'data-session-id': 'b' }).props.title).toContain('WORKING_ITEMS');
    expect(buildNavigatorSessionGroups(sessions, {}).all[0]).toMatchObject({ persona: 'HELP_HUMAN', projectRoot: '/a', sessionId: 'a' });
    expect(tree.root.findAllByType('a')).toHaveLength(0);
  });
});
