import React, { useEffect } from 'react';
import { act, create, type ReactTestRenderer } from 'react-test-renderer';
import { renderToStaticMarkup } from 'react-dom/server';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { RightPanel } from '../../components/woven-dialogue/right-panel';
import { Navigator } from '../../components/woven-dialogue/navigator';
import { CoordinationPanel } from '../../components/woven-dialogue/coordination-panel';
import { WovenDialogueShell } from '../../components/woven-dialogue/woven-dialogue-shell';

const shellState = vi.hoisted(() => ({
  pathname: '/',
  query: '',
  projectRoot: '/repo/projects/chirality-app-dev' as string | null,
  streaming: false,
  runtimeEpoch: 0,
  extraSessions: [] as string[],
  mounted: 0,
  unmounted: 0,
  replayLoad: vi.fn(),
  replayNotify: undefined as ((state: unknown) => void) | undefined,
  titleLoad: vi.fn(async () => ({} as Record<string, string>)),
  titleCancel: vi.fn(),
  titleDispose: vi.fn(),
  useRealReader: false,
  realReaders: [] as Array<{ dispose: ReturnType<typeof vi.fn>; cancel: ReturnType<typeof vi.fn> }>
  , routerReplace: vi.fn(), resumedSession: undefined as string | undefined,
  applyProjectRoot: vi.fn(async (_path: string) => true), chooseProjectRoot: vi.fn(async () => false), workspaceError: null as string | null,
  initialActiveSession: 'primary' as string | undefined,
  // The mocked chat panel reports a bound chat when set, and honours or declines New chat requests.
  bindingLocked: false, newChatAccepted: true, newChatRequests: 0
}));

vi.mock('next/navigation', () => ({
  usePathname: () => shellState.pathname,
  useSearchParams: () => new URLSearchParams(shellState.query),
  useRouter: () => ({ replace: shellState.routerReplace })
}));
vi.mock('next/link', () => ({
  default: ({ children, ...props }: React.AnchorHTMLAttributes<HTMLAnchorElement>) =>
    React.createElement('a', props, children)
}));

// The node test environment has no `window`/`fetch`; every child that reaches
// for the network, the harness stream, or the shared chrome is mocked so this
// test observes the shell's own composition only.
vi.mock('../../lib/harness/client', () => ({
  listHarnessSessions: vi.fn(async () => ['primary', 'recorded', ...shellState.extraSessions].map(sessionId => ({ sessionId, persona: 'TASK', projectRoot: shellState.projectRoot, mode: 'governed', createdAt: '2026-09-05', updatedAt: '2026-09-05' }))),
  listHarnessSessionRequests: vi.fn(async () => ({ requests: [] })),
  answerHarnessSessionRequest: vi.fn(async () => ({ sent: true })),
  harnessApiErrorMessage: (error: unknown) => String(error),
  replaySessionEvents: vi.fn(async () => ({ events: [] }))
}));
vi.mock('../../lib/woven-dialogue/chat-organization', async importOriginal => {
  const actual = await importOriginal<typeof import('../../lib/woven-dialogue/chat-organization')>();
  return { ...actual, createChatReplayReader: () => {
    if (!shellState.useRealReader) return { loadFirstOperatorMessages: shellState.titleLoad, search: vi.fn(async () => []), cancel: shellState.titleCancel, dispose: shellState.titleDispose };
    const reader = actual.createChatReplayReader();
    const wrapped = { ...reader, cancel: vi.fn(() => reader.cancel()), dispose: vi.fn(() => reader.dispose()) };
    shellState.realReaders.push(wrapped); return wrapped;
  } };
});
vi.mock('../../components/workspace/workspace-provider', () => ({
  useWorkspace: () => ({ projectRoot: shellState.projectRoot, applyProjectRoot: shellState.applyProjectRoot, chooseProjectRoot: shellState.chooseProjectRoot, errorMessage: shellState.workspaceError })
}));
vi.mock('../../components/workspace/harness-events-provider', () => ({
  useHarnessEvents: () => ({ events: [] }),
  useHarnessStreaming: () => shellState.streaming
}));
vi.mock('../../components/shell/shell-frame', () => ({
  ShellFrame: ({ children, title, renderWorkspaceContent, onOpenSettings, legacyHref }: { children?: React.ReactNode; title: string; onOpenSettings?: () => void; legacyHref?: string; renderWorkspaceContent?: (controls: object) => React.ReactNode }) => (
    <div data-shell-frame={title}>{renderWorkspaceContent ? renderWorkspaceContent({ settingsControl: <><button data-account-control="true" onClick={onOpenSettings}>Account settings</button><a href={legacyHref}>Legacy window</a></>, settingsView: <div data-settings-view="true">Settings controls</div> }) : children}</div>
  )
}));
vi.mock('../../components/shell/chat-panel', () => ({
  ChatPanel: ({ onActiveSessionChange, onDraftCaptured, onSessionBootedPrompt, fileCatalog = [], onOpenFile, resumeConversation, onConversationResumed, onBindingChange, onNewChatSettled, newChatRequest = 0 }: { onActiveSessionChange: (id: string | undefined) => void; onDraftCaptured: () => void; onSessionBootedPrompt: (input: { sessionId: string; prompt: string; persona: string }) => void; fileCatalog?: readonly string[]; onOpenFile?: (path: string) => void; resumeConversation?: { projection: { selectedSessionId: string } }; onConversationResumed?: (sessionId: string) => void; onBindingChange?: (binding: { root: string | null; locked: boolean }) => void; onNewChatSettled?: (started: boolean) => void; newChatRequest?: number }) => {
    useEffect(() => { shellState.mounted++; onActiveSessionChange(shellState.initialActiveSession as string); onBindingChange?.({ root: shellState.projectRoot, locked: shellState.bindingLocked }); return () => { shellState.unmounted++; }; }, [onActiveSessionChange, onBindingChange]);
    useEffect(() => {
      if (!newChatRequest) return;
      shellState.newChatRequests++;
      const started = shellState.newChatAccepted;
      if (started) { shellState.bindingLocked = false; onBindingChange?.({ root: shellState.projectRoot, locked: false }); onActiveSessionChange(undefined); }
      onNewChatSettled?.(started);
      // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [newChatRequest]);
    useEffect(() => { if (resumeConversation) { shellState.resumedSession = resumeConversation.projection.selectedSessionId; onActiveSessionChange(resumeConversation.projection.selectedSessionId); onConversationResumed?.(resumeConversation.projection.selectedSessionId); } }, [resumeConversation, onActiveSessionChange, onConversationResumed]);
    return <><input data-chat-panel="mounted" data-chat-input="primary" onChange={onDraftCaptured} /><button data-chat-file={fileCatalog.length} onClick={() => { if (fileCatalog[0]) onOpenFile?.(fileCatalog[0]); }}>open linked file</button><button data-live-title onClick={() => onSessionBootedPrompt({ sessionId: 'primary', prompt: `Review ${process.env.CHIRALITY_ANTHROPIC_API_KEY ?? ''} safely`, persona: 'TASK' })}>capture title</button></>;
  }
}));
vi.mock('../../components/shell/persona-picker', () => ({
  PersonaPicker: () => <div data-persona-picker="mounted" />
}));
vi.mock('../../components/shell/file-tree-panel', () => ({
  FileTreePanel: () => <div data-file-tree="mounted" />
}));
// Mocked defensively: after the Artifacts→Workbench fold, `WorkbenchSurface`
// transitively imports `DocumentView` (react-markdown ESM + fetch).
vi.mock('../../components/shell/document-view', () => ({
  DocumentView: () => <div data-document-view="mounted" />
}));
vi.mock('../../components/workbench/workbench-surface', () => ({
  WorkbenchSurface: () => <div data-workbench-surface="mounted" />
}));
vi.mock('../../components/pipeline/pipeline-surface', () => ({
  PipelineSurface: () => <div data-pipeline-surface="mounted" />
}));
vi.mock('../../components/woven-dialogue/agents-projection', () => ({
  AgentsProjection: () => <div data-agents="mounted" />
}));
vi.mock('../../components/shell/runtime-connectivity-provider', () => ({ useRuntimeEpoch: () => shellState.runtimeEpoch }));
vi.mock('../../lib/woven-dialogue/selected-session-replay', async (importOriginal) => ({
  ...await importOriginal<typeof import('../../lib/woven-dialogue/selected-session-replay')>(),
  createSelectedSessionReplayLoader: () => {
    let current: any = { status: 'IDLE' };
    return {
    getState: () => current,
    subscribe: (notify: (state: unknown) => void) => { shellState.replayNotify = notify; return () => {}; },
    load: async (id: string, options?: { observedAt?: string; maxItems?: number }) => {
      shellState.replayLoad(id);
      if (options?.maxItems) {
        current = { status: 'READY', projection: { selectedSessionId: id, sourceReference: `session:${id}/events`, observedAt: options.observedAt ?? '2026-09-07T00:00:00Z', disclosure: 'READY_SNAPSHOT', currency: 'CURRENT', transcript: { sessionId: id, itemCount: 1, items: [{ key: 'one', kind: 'message', role: 'user', status: 'accepted', title: 'User', timestamp: '2026-09-07T00:00:00Z', eventId: 'event', eventType: 'message.accepted', text: `recorded message ${id}` }] }, malformedLineCount: 0, sourceEventCount: 1, renderedItemCount: 1, diagnostics: [] } };
        return { applied: true, state: current };
      }
      shellState.replayNotify?.({ status: 'LOADING', selectedSessionId: id }); return { applied: true, state: current };
    },
    cancel: () => shellState.replayNotify?.({ status: 'IDLE' }),
    dispose: () => {}
  }; }
}));
vi.mock('../../components/woven-dialogue/activity-shelf', () => ({
  ActivityStrip: ({ onOpenDetails, primarySessionId }: { onOpenDetails: () => void; primarySessionId?: string }) => <button onClick={onOpenDetails} data-primary-session={primarySessionId} data-activity-strip="mounted">Details</button>,
  ActivityView: () => <div data-activity-view="mounted" />
}));
vi.mock('../../components/woven-dialogue/selected-session-replay-lens', () => ({
  SelectedSessionReplayLens: ({ state, onReturnToPrimary, onRetry, onContinue }: { state: any; onReturnToPrimary: () => void; onRetry: () => void; onContinue?: (projection: any) => void }) => <section data-replay-lens={state.status}><button onClick={onReturnToPrimary}>Return to primary dialogue</button><button onClick={onRetry}>Retry</button>{state.status === 'READY' && state.projection.session?.continuation && onContinue ? <button onClick={() => onContinue(state.projection)}>Continue this chat</button> : null}</section>
}));

function navigatorItemCount(html: string): number {
  return (html.match(/class="woven-nav-item/g) ?? []).length;
}

describe('WovenDialogueShell composition', () => {
  afterEach(() => { vi.unstubAllGlobals(); });
  beforeEach(() => {
    shellState.pathname = '/';
    shellState.query = '';
    shellState.projectRoot = '/repo/projects/chirality-app-dev';
    shellState.streaming = false;
    shellState.runtimeEpoch = 0;
    shellState.extraSessions = [];
    shellState.titleLoad.mockReset(); shellState.titleLoad.mockResolvedValue({});
    shellState.titleCancel.mockClear(); shellState.titleDispose.mockClear();
    shellState.useRealReader = false; shellState.realReaders = [];
    shellState.routerReplace.mockClear(); shellState.resumedSession = undefined;
  });

  it.each(['dialogue', 'workbench', 'pipeline'] as const)('only mounts Dialogue even with historical %s surface input', (surface) => {
    const html = renderToStaticMarkup(<WovenDialogueShell defaultSurface={surface} />);
    expect(navigatorItemCount(html)).toBe(1);
    expect(html).toContain('<span>Current chat</span>');
    expect(html).toContain('data-woven-surface="dialogue"');
    expect(html).toContain('data-chat-panel="mounted"');
    expect(html).not.toContain('data-focused-surface');
    expect(html).not.toContain('data-workbench-surface');
    expect(html).not.toContain('data-pipeline-surface');
    expect(html).not.toContain('woven-navigator-chevron');
    expect(html).not.toMatch(/\shidden=/);
  });

  it('preserves controller identity and focusable composer through replay, panel controls, resize, and return', async () => {
    const focus = vi.fn();
    const persist = vi.fn();
    vi.stubGlobal('window', { setInterval: globalThis.setInterval, clearInterval: globalThis.clearInterval, localStorage: { getItem: () => JSON.stringify({ schema: 'chirality.woven-workspace/v1', coordinationView: 'work', rightPanelView: 'agents', sessionSurfaces: { recorded: 'workbench' } }), setItem: persist }, addEventListener: vi.fn(), removeEventListener: vi.fn(), requestAnimationFrame: (callback: () => void) => callback() });
    vi.stubGlobal('document', { querySelector: () => ({ focus }) });
    shellState.mounted = 0; shellState.unmounted = 0; shellState.replayLoad.mockClear();
    let tree!: ReactTestRenderer;
    await act(async () => { tree = create(<WovenDialogueShell defaultSurface="dialogue" />); });
    expect(tree.root.findByType(CoordinationPanel).props.activeView).toBe('agents');
    expect(tree.root.findByType(Navigator).props.sessionSurfaces).toEqual({ recorded: 'workbench', primary: 'dialogue' });
    expect(JSON.parse(persist.mock.calls.at(-1)![1]).sessionSurfaces).toEqual({ recorded: 'workbench', primary: 'dialogue' });
    const input = tree.root.findByProps({ 'data-chat-input': 'primary' });
    const assertPrimary = () => {
      expect(tree.root.findByProps({ 'data-chat-input': 'primary' })).toBe(input);
      let node: typeof input | null = input;
      while (node) { expect(node.props.hidden).not.toBe(true); expect(node.props['aria-hidden']).not.toBe(true); node = node.parent; }
      expect(input.props.disabled).toBeUndefined();
      expect(shellState.mounted).toBe(1); expect(shellState.unmounted).toBe(0);
      expect(tree.root.findAll(node => Boolean(node.props['data-focused-surface']))).toHaveLength(0);
    };
    const click = (label: string) => act(() => { tree.root.findAllByType('button').find(button => (button.props['aria-label'] ?? button.children.join('')) === label)!.props.onClick(); });
    const inspectRecorded = tree.root.findByType(RightPanel).props.onOpenParent;
    act(() => tree.root.findByType(RightPanel).props.onClose());
    act(() => inspectRecorded('recorded'));
    expect(tree.root.findByType(CoordinationPanel).props.activeView).toBe('session');
    expect(tree.root.findByProps({ 'data-replay-lens': 'LOADING' })).toBeTruthy();
    assertPrimary();
    act(() => shellState.replayNotify?.({ status: 'UNAVAILABLE', selectedSessionId: 'recorded', message: 'offline' }));
    assertPrimary();
    click('Retry');
    expect(shellState.replayLoad).toHaveBeenCalledTimes(2);
    act(() => shellState.replayNotify?.({ status: 'READY', projection: { selectedSessionId: 'recorded' } }));
    assertPrimary();
    // The right panel's "Agents" tab or breadcrumb, never the Coordination view toggle (which carries aria-pressed).
    const agentsButton = () => tree.root.findAllByType('button').find(button => button.children.join('') === 'Agents' && button.props['aria-pressed'] === undefined)!;
    const clickAgentsTab = () => act(() => { agentsButton().props.onClick(); });
    expect(agentsButton()).toBeDefined();
    expect(tree.root.findAllByType('button').some(button => button.children.join('') === 'Who is working')).toBe(false);
    clickAgentsTab(); assertPrimary();
    act(() => tree.root.findByType(RightPanel).props.onOpenParent('recorded'));
    expect(tree.root.findByType(CoordinationPanel).props.activeView).toBe('session');
    expect(shellState.replayLoad).toHaveBeenCalledTimes(2); assertPrimary();
    clickAgentsTab(); act(() => tree.root.findByType(Navigator).props.onSelectSession('recorded')); assertPrimary();
    click('Close Navigator'); assertPrimary(); click('Open Navigator'); assertPrimary();
    act(() => tree.root.findByType(RightPanel).props.onView('files'));
    act(() => tree.root.findByType(RightPanel).props.onClose()); assertPrimary(); click('Open Coordination'); assertPrimary();
    for (const label of ['Resize Navigator', 'Resize Coordination Panel']) {
      for (const key of ['Home', 'End', 'ArrowLeft']) {
        act(() => tree.root.findByProps({ 'aria-label': label }).props.onKeyDown({ key, shiftKey: false, preventDefault: vi.fn() }));
        assertPrimary();
      }
    }
    act(() => tree.root.findByType(RightPanel).props.onOpenParent('recorded'));
    click('Return to primary dialogue');
    expect(focus).toHaveBeenCalled(); assertPrimary();
    expect(tree.root.findAll(node => Boolean(node.props['data-replay-lens']))).toHaveLength(0);
    shellState.streaming = true;
    act(() => tree.update(<WovenDialogueShell defaultSurface="dialogue" />));
    act(() => tree.root.findByType(Navigator).props.onSelectSession('recorded'));
    expect(shellState.replayLoad).toHaveBeenCalledTimes(2); assertPrimary();
    act(() => tree.unmount());
    expect(shellState.unmounted).toBe(1);
  });

  it('persists file/document widths and expand return while primary stays mounted', async () => {
    const persist = vi.fn(); const listeners: Record<string, (event: unknown) => void> = {};
    vi.stubGlobal('window', { setInterval: globalThis.setInterval, clearInterval: globalThis.clearInterval, localStorage: { getItem: () => null, setItem: persist },
      addEventListener: (name: string, callback: (event: unknown) => void) => { listeners[name] = callback; }, removeEventListener: vi.fn(), requestAnimationFrame: (cb: () => void) => cb() });
    vi.stubGlobal('document', { querySelector: () => ({ focus: vi.fn() }) });
    let tree!: ReactTestRenderer; await act(async () => { tree = create(<WovenDialogueShell defaultSurface="dialogue" />); });
    const input = tree.root.findByProps({ 'data-chat-input': 'primary' });
    const panel = () => tree.root.findByType(RightPanel);
    const state = () => JSON.parse(persist.mock.calls.at(-1)![1]);
    const resize = () => tree.root.findByProps({ 'aria-label': 'Resize Coordination Panel' });
    expect(panel().props.state.rightPanelView).toBe('files');
    act(() => resize().props.onKeyDown({ key: 'ArrowLeft', shiftKey: false, preventDefault: vi.fn() }));
    expect(state().rightPanelWidths.files).toBe(316);
    act(() => panel().props.onOpenFile(`${shellState.projectRoot}/spec.md`));
    expect(state().openDocumentPath).toBe('spec.md'); expect(resize().props['aria-valuenow']).toBe(480);
    act(() => resize().props.onPointerDown({ button: 0, clientX: 700, clientY: 0, preventDefault: vi.fn() }));
    act(() => listeners.pointermove({ clientX: 620, clientY: 0 })); act(() => listeners.pointerup({}));
    expect(state().rightPanelWidths.document).toBe(560);
    act(() => panel().props.onExpand());
    expect(state()).toMatchObject({ rightPanelExpanded: true, navigatorCollapsed: true, preExpandState: { rightWidth: 560, leftCollapsed: false } });
    act(() => input.props.onChange());
    expect(state()).toMatchObject({ rightPanelExpanded: false, navigatorCollapsed: false, rightPanelWidths: { document: 560 } });
    act(() => panel().props.onView('files'));
    expect(state().openDocumentPath).toBeNull(); expect(resize().props['aria-valuenow']).toBe(316);
    act(() => panel().props.onView('agents')); expect(resize().props['aria-valuenow']).toBe(360);
    expect(tree.root.findByProps({ 'data-chat-input': 'primary' })).toBe(input);
    act(() => tree.unmount());
  });

  it('binds the loaded catalog to the current root and routes chat links through the contained file opener', async () => {
    const persist = vi.fn();
    vi.stubGlobal('window', { setInterval: globalThis.setInterval, clearInterval: globalThis.clearInterval, localStorage: { getItem: () => null, setItem: persist }, addEventListener: vi.fn(), removeEventListener: vi.fn(), requestAnimationFrame: (cb: () => void) => cb() });
    let tree!: ReactTestRenderer;
    await act(async () => { tree = create(<WovenDialogueShell defaultSurface="dialogue" />); });
    const panel = tree.root.findByType(RightPanel);
    const oldCatalogCallback = panel.props.onFileCatalog;
    act(() => oldCatalogCallback({ root: shellState.projectRoot, paths: [`${shellState.projectRoot}/docs/SPEC.md`] }));
    expect(tree.root.findByProps({ 'data-chat-file': 1 })).toBeTruthy();
    act(() => panel.props.onClose());
    expect(tree.root.findByProps({ 'aria-label': 'Open Coordination' })).toBeTruthy();
    expect(tree.root.findAllByType(RightPanel)).toHaveLength(0);
    act(() => tree.root.findByProps({ 'data-chat-file': 1 }).props.onClick());
    expect(tree.root.findAllByProps({ 'aria-label': 'Open Coordination' })).toHaveLength(0);
    expect(tree.root.findByType(RightPanel).props.state.openDocumentPath).toBe('docs/SPEC.md');
    expect(JSON.parse(persist.mock.calls.at(-1)![1])).toMatchObject({ openDocumentPath: 'docs/SPEC.md', rightPanelView: 'files', coordinationCollapsed: false });

    act(() => tree.root.findByType(RightPanel).props.onOpenFile('/repo/projects/chirality-app-dev-other/docs/SPEC.md'));
    expect(JSON.parse(persist.mock.calls.at(-1)![1]).openDocumentPath).toBe('docs/SPEC.md');

    shellState.projectRoot = '/repo/next';
    act(() => tree.update(<WovenDialogueShell defaultSurface="dialogue" />));
    expect(tree.root.findByProps({ 'data-chat-file': 0 })).toBeTruthy();
    act(() => oldCatalogCallback({ root: '/repo/projects/chirality-app-dev', paths: ['/repo/projects/chirality-app-dev/docs/SPEC.md'] }));
    expect(tree.root.findByProps({ 'data-chat-file': 0 })).toBeTruthy();
    act(() => tree.root.findByType(RightPanel).props.onFileCatalog({ root: '/repo/next', paths: ['/repo/next/docs/SPEC.md'] }));
    expect(tree.root.findByProps({ 'data-chat-file': 1 })).toBeTruthy();
    act(() => tree.unmount());
  });

  it('opens a recorded parent through the existing selection guard, preserving live-turn and primary behavior', async () => {
    shellState.extraSessions = ['parent']; shellState.replayLoad.mockClear();
    const focus = vi.fn();
    vi.stubGlobal('window', { setInterval: globalThis.setInterval, clearInterval: globalThis.clearInterval, localStorage: { getItem: () => null, setItem: vi.fn() }, addEventListener: vi.fn(), removeEventListener: vi.fn(), requestAnimationFrame: (cb: () => void) => cb() });
    vi.stubGlobal('document', { querySelector: () => ({ focus }) });
    let tree!: ReactTestRenderer; await act(async () => { tree = create(<WovenDialogueShell defaultSurface="dialogue" />); });
    const input = tree.root.findByProps({ 'data-chat-input': 'primary' });
    act(() => tree.root.findByType(RightPanel).props.onOpenParent('recorded'));
    const projection = (parentSessionId: string) => ({ selectedSessionId: 'recorded', sourceReference: 'events:recorded', observedAt: '2026-09-05', disclosure: 'READY_SNAPSHOT', currency: 'CURRENT', sourceEventCount: 2, renderedItemCount: 1, malformedLineCount: 0, diagnostics: [], session: { sessionId: 'recorded', currency: 'CURRENT', parentage: { state: 'RECORDED', parentSessionId, parentAvailable: true }, diagnostics: [] } });
    act(() => shellState.replayNotify?.({ status: 'READY', projection: projection('parent') }));
    const openParent = () => tree.root.findAllByType('button').find(x => x.children.includes('Open parent chat'))!;
    expect(openParent().props.disabled).toBe(false); act(() => openParent().props.onClick()); expect(shellState.replayLoad).toHaveBeenLastCalledWith('parent');
    act(() => shellState.replayNotify?.({ status: 'READY', projection: projection('parent') }));
    shellState.streaming = true; act(() => tree.update(<WovenDialogueShell defaultSurface="dialogue" />));
    expect(openParent().props.disabled).toBe(true);
    const calls = shellState.replayLoad.mock.calls.length;
    act(() => tree.root.findByType(RightPanel).props.onOpenParent('parent')); expect(shellState.replayLoad).toHaveBeenCalledTimes(calls);
    act(() => shellState.replayNotify?.({ status: 'READY', projection: projection('primary') }));
    expect(openParent().props.disabled).toBe(false); act(() => openParent().props.onClick());
    expect(focus).toHaveBeenCalled(); expect(shellState.replayLoad).toHaveBeenCalledTimes(calls);
    expect(tree.root.findByProps({ 'data-chat-input': 'primary' })).toBe(input);
    act(() => tree.unmount());
  });

  it('continues a compatible v3 replay in the mounted primary dialogue and leaves legacy replay read-only', async () => {
    shellState.query = '';
    vi.stubGlobal('window', { setInterval: globalThis.setInterval, clearInterval: globalThis.clearInterval, localStorage: { getItem: () => null, setItem: vi.fn() }, addEventListener: vi.fn(), removeEventListener: vi.fn(), requestAnimationFrame: (callback: () => void) => callback() });
    vi.stubGlobal('document', { querySelector: () => ({ focus: vi.fn() }) });
    let tree!: ReactTestRenderer;
    await act(async () => { tree = create(<WovenDialogueShell defaultSurface="dialogue" />); });
    act(() => tree.root.findByType(RightPanel).props.onOpenParent('recorded'));
    const projection = { selectedSessionId: 'recorded', sourceReference: 'session:recorded/events', observedAt: '2026-09-09', disclosure: 'READY_SNAPSHOT', currency: 'CURRENT', transcript: { itemCount: 0, items: [] }, instructionHistory: [], instructionBases: [], malformedLineCount: 0, sourceEventCount: 0, renderedItemCount: 0, diagnostics: [], session: { sessionId: 'recorded', parentage: { state: 'NOT_RECORDED' }, diagnostics: [], continuation: { schemaVersion: 'chirality.session/v3', projectRoot: shellState.projectRoot, roleId: 'WORKING_ITEMS', mode: 'CHAT', interactionMode: 'chat', permissionMode: 'ask', selectedMethods: [], methodSelectionRevision: 1, instructionBasisId: 'basis-1' } } };
    await act(async () => shellState.replayNotify?.({ status: 'READY', projection }));
    await act(async () => tree.root.findAllByType('button').find(button => button.children.includes('Continue this chat'))!.props.onClick());
    expect(shellState.routerReplace).toHaveBeenCalledWith('/?agent=WORKING_ITEMS');
    expect(shellState.resumedSession).toBeUndefined();
    shellState.query = 'agent=WORKING_ITEMS';
    await act(async () => tree.update(<WovenDialogueShell defaultSurface="dialogue" />));
    expect(shellState.resumedSession).toBe('recorded');
    expect(tree.root.findAll(node => Boolean(node.props['data-replay-lens']))).toHaveLength(0);
    act(() => tree.unmount());
  });

  it.each(['pointer', 'keyboard'] as const)('announces the constrained panel width, restores its preference, and starts %s resizing from the visible width', async (input) => {
    let measure!: (entries: Array<{ contentRect: { width: number } }>) => void;
    const persist = vi.fn();
    const listeners: Record<string, (event: unknown) => void> = {};
    vi.stubGlobal('ResizeObserver', class { constructor(callback: typeof measure) { measure = callback; } observe() {} disconnect() {} });
    vi.stubGlobal('window', { setInterval: globalThis.setInterval, clearInterval: globalThis.clearInterval,
      localStorage: { getItem: () => JSON.stringify({ schema: 'chirality.woven-workspace/v1', navigatorWidth: 280,
        rightPanelView: 'files', openDocumentPath: 'spec.md', rightPanelWidths: { document: 480, files: 300 } }), setItem: persist },
      addEventListener: (name: string, callback: (event: unknown) => void) => { listeners[name] = callback; }, removeEventListener: vi.fn()
    });
    let tree!: ReactTestRenderer;
    await act(async () => { tree = create(<WovenDialogueShell defaultSurface="dialogue" />, { createNodeMock: element => element.type === 'section' && element.props['data-woven-surface'] ? {} : null }); });
    const resize = () => tree.root.findByProps({ 'aria-label': 'Resize Coordination Panel' });
    const saved = () => JSON.parse(persist.mock.calls.at(-1)![1]);
    const assertWidth = (width: number) => {
      expect(tree.root.findByProps({ 'data-woven-surface': 'dialogue' }).props.style.gridTemplateColumns).toMatch(new RegExp(` ${width}px$`));
      expect(resize().props['aria-valuenow']).toBe(width);
      expect(width).toBeGreaterThanOrEqual(resize().props['aria-valuemin']);
      expect(width).toBeLessThanOrEqual(resize().props['aria-valuemax']);
    };
    act(() => measure([{ contentRect: { width: 1000 } }]));
    assertWidth(280);
    expect(saved().rightPanelWidths.document).toBe(480);
    act(() => measure([{ contentRect: { width: 1440 } }]));
    assertWidth(480);
    act(() => measure([{ contentRect: { width: 1080 } }]));
    assertWidth(356);
    if (input === 'pointer') {
      act(() => resize().props.onPointerDown({ button: 0, clientX: 700, clientY: 0, preventDefault: vi.fn() }));
      act(() => listeners.pointermove({ clientX: 716, clientY: 0 }));
      act(() => listeners.pointerup({}));
    } else {
      act(() => resize().props.onKeyDown({ key: 'ArrowRight', shiftKey: false, preventDefault: vi.fn() }));
    }
    assertWidth(340);
    expect(saved().rightPanelWidths).toMatchObject({ document: 340, files: 300 });
    act(() => measure([{ contentRect: { width: 1440 } }]));
    assertWidth(340);
    // The grid declaration is covered here; actual browser geometry remains the parent's proof.
    act(() => tree.unmount());
  });

  it('responds to measured stacked widths without removing primary, document or activity controls', async () => {
    let measure!: (entries: Array<{ contentRect: { width: number } }>) => void;
    vi.stubGlobal('ResizeObserver', class { constructor(callback: typeof measure) { measure = callback; } observe() {} disconnect() {} });
    vi.stubGlobal('window', { setInterval: globalThis.setInterval, clearInterval: globalThis.clearInterval, localStorage: { getItem: () => null, setItem: vi.fn() }, addEventListener: vi.fn(), removeEventListener: vi.fn(), requestAnimationFrame: (cb: () => void) => cb() });
    let tree!: ReactTestRenderer;
    await act(async () => { tree = create(<WovenDialogueShell defaultSurface="dialogue" />, { createNodeMock: element => element.type === 'section' && element.props['data-woven-surface'] ? {} : null }); });
    const primary = tree.root.findByProps({ 'data-chat-input': 'primary' });
    act(() => tree.root.findByType(RightPanel).props.onOpenFile(`${shellState.projectRoot}/spec.md`));
    for (const width of [1440, 960, 959, 900, 861, 860]) {
      act(() => measure([{ contentRect: { width } }]));
      expect(tree.root.findByProps({ 'data-woven-surface': 'dialogue' }).props.className.includes('is-stacked')).toBe(width < 960);
      expect(tree.root.findByProps({ 'data-chat-input': 'primary' })).toBe(primary);
      expect(tree.root.findByProps({ 'data-document-view': 'mounted' })).toBeTruthy();
      expect(tree.root.findByProps({ 'data-activity-strip': 'mounted' })).toBeTruthy();
    }
    // This tests measured state/identity only; browser scroll geometry is a separate manager-owned proof.
    act(() => tree.unmount());
  });

  it('provides explicit desktop reopen glyphs and full accessible names across responsive states', async () => {
    let measure!: (entries: Array<{ contentRect: { width: number } }>) => void;
    vi.stubGlobal('ResizeObserver', class { constructor(callback: typeof measure) { measure = callback; } observe() {} disconnect() {} });
    vi.stubGlobal('window', { setInterval: globalThis.setInterval, clearInterval: globalThis.clearInterval, localStorage: { getItem: () => null, setItem: vi.fn() }, addEventListener: vi.fn(), removeEventListener: vi.fn(), requestAnimationFrame: (cb: () => void) => cb() });
    let tree!: ReactTestRenderer;
    await act(async () => { tree = create(<WovenDialogueShell defaultSurface="dialogue" />, { createNodeMock: element => element.type === 'section' && element.props['data-woven-surface'] ? {} : null }); });
    act(() => tree.root.findByProps({ 'aria-label': 'Close Navigator' }).props.onClick());
    act(() => tree.root.findByType(RightPanel).props.onClose());
    for (const width of [1440, 960, 959, 860, 1440]) {
      act(() => measure([{ contentRect: { width } }]));
      expect(tree.root.findByProps({ 'aria-label': 'Open Navigator' }).findByProps({ className: 'woven-collapsed-brand' }).children).toEqual(['C']);
      expect(tree.root.findByProps({ 'aria-label': 'Open Coordination' }).children).toEqual(['›']);
    }
    act(() => tree.root.findByProps({ 'aria-label': 'Open Navigator' }).props.onClick());
    act(() => tree.root.findByProps({ 'aria-label': 'Open Coordination' }).props.onClick());
    expect(tree.root.findByType(Navigator)).toBeTruthy();
    expect(tree.root.findByType(RightPanel)).toBeTruthy();
    // Rendered content/state is covered here; actual glyph visibility and geometry need browser proof.
    act(() => tree.unmount());
  });

  it('keeps collapse, detail return and expansion as distinct real controls without remounting primary', async () => {
    const persist = vi.fn();
    vi.stubGlobal('window', { setInterval: globalThis.setInterval, clearInterval: globalThis.clearInterval, localStorage: { getItem: () => null, setItem: persist }, addEventListener: vi.fn(), removeEventListener: vi.fn(), requestAnimationFrame: (cb: () => void) => cb() });
    let tree!: ReactTestRenderer; await act(async () => { tree = create(<WovenDialogueShell defaultSurface="dialogue" />); });
    const primary = tree.root.findByProps({ 'data-chat-input': 'primary' });
    const saved = () => JSON.parse(persist.mock.calls.at(-1)![1]);
    const click = (label: string) => act(() => tree.root.findAllByType('button').find(button => (button.props['aria-label'] ?? button.children.join('')) === label)!.props.onClick());
    const assertPrimary = () => expect(tree.root.findByProps({ 'data-chat-input': 'primary' })).toBe(primary);
    act(() => tree.root.findByType(RightPanel).props.onOpenFile(`${shellState.projectRoot}/spec.md`));
    click('Expand panel'); expect(saved().rightPanelExpanded).toBe(true); assertPrimary();
    click('Return panel'); expect(saved().rightPanelExpanded).toBe(false); expect(saved().openDocumentPath).toBe('spec.md'); assertPrimary();
    click('Close detail'); expect(saved()).toMatchObject({ coordinationCollapsed: false, openDocumentPath: null }); assertPrimary();
    click('Collapse right panel'); expect(saved()).toMatchObject({ coordinationCollapsed: true, openDocumentPath: null });
    expect(tree.root.findAllByType(RightPanel)).toHaveLength(0); assertPrimary();
    click('Close Navigator'); expect(saved().navigatorCollapsed).toBe(true); assertPrimary();
    click('Open Navigator'); expect(saved().navigatorCollapsed).toBe(false); assertPrimary();
    click('Open Coordination'); expect(saved()).toMatchObject({ coordinationCollapsed: false, openDocumentPath: null }); assertPrimary();
    click('Expand panel'); expect(saved().rightPanelExpanded).toBe(true);
    act(() => tree.root.findByProps({ 'aria-label': 'Collapse right panel' }).props.onClick());
    expect(saved()).toMatchObject({ coordinationCollapsed: true, rightPanelExpanded: false, navigatorCollapsed: false }); assertPrimary();
    click('Open Coordination'); expect(saved().rightPanelView).toBe('files'); assertPrimary();
    act(() => tree.unmount());
  });

  it('preserves the legacy compatibility link with the current query string', () => {
    shellState.pathname = '/workbench';
    shellState.query = 'agent=CHANGE';

    const html = renderToStaticMarkup(<WovenDialogueShell defaultSurface="workbench" />);

    expect(html).toContain('href="/workbench?agent=CHANGE&amp;legacy=1"');
  });

  it('persists a redacted live title and rejects an older recorded-title completion', async () => {
    process.env.CHIRALITY_ANTHROPIC_API_KEY = 'configured-secret-value';
    const persist = vi.fn();
    vi.stubGlobal('window', { setInterval: globalThis.setInterval, clearInterval: globalThis.clearInterval, localStorage: { getItem: () => null, setItem: persist }, addEventListener: vi.fn(), removeEventListener: vi.fn(), requestAnimationFrame: (cb: () => void) => cb() });
    let tree!: ReactTestRenderer;
    await act(async () => { tree = create(<WovenDialogueShell defaultSurface="dialogue" />); });
    let finish!: (titles: Record<string, string>) => void;
    shellState.titleLoad.mockImplementation(() => new Promise(resolve => { finish = resolve; }));
    shellState.runtimeEpoch += 1;
    act(() => tree.update(<WovenDialogueShell defaultSurface="dialogue" />));
    await new Promise(resolve => setTimeout(resolve, 0));
    act(() => tree.root.findByProps({ 'data-live-title': true }).props.onClick());
    const live = JSON.parse(persist.mock.calls.at(-1)![1]).chatTitles.primary;
    expect(live).toContain('[REDACTED_API_KEY]');
    expect(live).not.toContain('configured-secret-value');
    await act(async () => finish({ primary: 'older replay title' }));
    expect(JSON.parse(persist.mock.calls.at(-1)![1]).chatTitles.primary).toBe(live);
    act(() => tree.unmount());
    delete process.env.CHIRALITY_ANTHROPIC_API_KEY;
  });

  it('loads recorded titles only for visible active sessions', async () => {
    shellState.extraSessions = ['visible']; shellState.titleLoad.mockClear();
    vi.stubGlobal('window', { setInterval: globalThis.setInterval, clearInterval: globalThis.clearInterval, localStorage: { getItem: () => JSON.stringify({ schema: 'chirality.woven-workspace/v1', chatArchived: ['recorded'], chatDeleted: ['primary'] }), setItem: vi.fn() }, addEventListener: vi.fn(), removeEventListener: vi.fn(), requestAnimationFrame: (cb: () => void) => cb() });
    let tree!: ReactTestRenderer;
    await act(async () => { tree = create(<WovenDialogueShell defaultSurface="dialogue" />); });
    const titleCalls = shellState.titleLoad.mock.calls as unknown as Array<[Array<{ sessionId: string }>]>;
    const loaded = titleCalls.at(-1)![0];
    expect(loaded.map(item => item.sessionId)).toEqual(['visible']);
    act(() => tree.unmount());
  });

  it('exposes collapsed search, guarded new-chat, expand, and account controls', async () => {
    vi.stubGlobal('window', { setInterval: globalThis.setInterval, clearInterval: globalThis.clearInterval, localStorage: { getItem: () => null, setItem: vi.fn() }, addEventListener: vi.fn(), removeEventListener: vi.fn(), requestAnimationFrame: (cb: () => void) => cb() });
    let tree!: ReactTestRenderer;
    await act(async () => { tree = create(<WovenDialogueShell defaultSurface="dialogue" />); });
    act(() => tree.root.findByProps({ 'aria-label': 'Close Navigator' }).props.onClick());
    expect(tree.root.findByProps({ className: 'woven-collapsed-strip' })).toBeTruthy();
    expect(tree.root.findByProps({ 'aria-label': 'New chat' }).props.disabled).toBe(false);
    expect(tree.root.findByProps({ 'data-account-control': 'true' })).toBeTruthy();
    act(() => tree.root.findByProps({ 'aria-label': 'Search chats' }).props.onClick());
    expect(tree.root.findByType(Navigator)).toBeTruthy();
    act(() => tree.unmount());
  });

  it('owns Cmd-K while collapsed and suppresses it behind every Navigator dialog', async () => {
    const listeners: Record<string, Array<(event: any) => void>> = {}; const focus = vi.fn();
    vi.stubGlobal('window', { setInterval: globalThis.setInterval, clearInterval: globalThis.clearInterval, localStorage: { getItem: () => null, setItem: vi.fn() }, addEventListener: (name: string, fn: (event: any) => void) => { (listeners[name] ??= []).push(fn); }, removeEventListener: (name: string, fn: (event: any) => void) => { listeners[name] = (listeners[name] ?? []).filter(item => item !== fn); }, requestAnimationFrame: (cb: () => void) => cb() });
    let tree!: ReactTestRenderer;
    await act(async () => { tree = create(<WovenDialogueShell defaultSurface="dialogue" />, { createNodeMock: element => element.type === 'input' && element.props['aria-label'] === 'Search chats' ? { focus } : null }); });
    act(() => tree.root.findByProps({ 'aria-label': 'Close Navigator' }).props.onClick());
    const shortcut = () => listeners.keydown.forEach(listener => listener({ key: 'k', metaKey: true, ctrlKey: false, preventDefault: vi.fn() }));
    act(shortcut); expect(tree.root.findByType(Navigator)).toBeTruthy(); expect(focus).toHaveBeenCalled();
    for (const action of ['Rename', 'New group…', 'Delete…']) {
      act(() => tree.root.findAllByType('button').find(button => String(button.props['aria-label'] ?? '').startsWith('Chat actions'))!.props.onClick({ currentTarget: { isConnected: true, focus: vi.fn() } }));
      act(() => tree.root.findAllByType('button').find(button => button.children.includes(action))!.props.onClick());
      const before = focus.mock.calls.length; act(shortcut); expect(tree.root.findByProps({ role: 'dialog' })).toBeTruthy(); expect(focus).toHaveBeenCalledTimes(before);
      act(() => tree.root.findByProps({ role: 'dialog' }).findAllByType('button').find(button => button.children.includes('Cancel'))!.props.onClick());
      act(() => tree.root.findByProps({ role: 'menu' }).findAllByType('button').find(button => button.children.includes('Close menu'))!.props.onClick());
    }
    act(() => tree.unmount());
  });

  it('replaces cleaned-up real replay readers across StrictMode effect replay and retains title/search work', async () => {
    shellState.useRealReader = true;
    const persist = vi.fn();
    vi.stubGlobal('window', { setInterval: globalThis.setInterval, clearInterval: globalThis.clearInterval, localStorage: { getItem: () => null, setItem: persist }, addEventListener: vi.fn(), removeEventListener: vi.fn(), requestAnimationFrame: (cb: () => void) => cb() });
    let tree!: ReactTestRenderer;
    await act(async () => { tree = create(<React.StrictMode><WovenDialogueShell defaultSurface="dialogue" /></React.StrictMode>); });
    act(() => tree.update(<React.StrictMode />));
    expect(shellState.realReaders).toHaveLength(2); expect(shellState.realReaders[0].dispose).toHaveBeenCalled(); expect(shellState.realReaders[1].dispose).toHaveBeenCalled();
    await act(async () => { tree.update(<React.StrictMode><WovenDialogueShell defaultSurface="dialogue" /></React.StrictMode>); });
    expect(shellState.realReaders.length).toBeGreaterThanOrEqual(4);
    expect(JSON.parse(persist.mock.calls.at(-1)![1]).chatTitles).toMatchObject({ primary: 'recorded message primary', recorded: 'recorded message recorded' });
    const search = tree.root.findByProps({ 'aria-label': 'Search chats' });
    act(() => search.props.onChange({ target: { value: 'recorded message' } }));
    await act(async () => { await new Promise(resolve => setTimeout(resolve, 260)); });
    expect(tree.root.findByProps({ 'aria-label': 'Message matches' }).findAllByProps({ 'data-session-id': 'recorded' })).toHaveLength(1);
    act(() => tree.unmount());
    expect(shellState.realReaders.at(-1)!.dispose).toHaveBeenCalled();
  });
});

it('opens Settings from the sole footer or collapsed account control without remounting the chat', async () => {
  let tree!: ReactTestRenderer;
  vi.stubGlobal('window', { setInterval: globalThis.setInterval, clearInterval: globalThis.clearInterval, innerWidth: 1440, innerHeight: 900, addEventListener: vi.fn(), removeEventListener: vi.fn(), localStorage: { getItem: () => null, setItem: vi.fn() } });
  await act(async () => { tree = create(<WovenDialogueShell defaultSurface="dialogue" />); });
  const chat = tree.root.findByProps({ 'data-chat-panel': 'mounted' });
  expect(tree.root.findByProps({ 'data-activity-strip': 'mounted' }).props['data-primary-session']).toBe('primary');
  const mounted = shellState.mounted;
  const unmounted = shellState.unmounted;
  expect(tree.root.findAllByProps({ 'data-account-control': 'true' })).toHaveLength(1);
  act(() => tree.root.findByProps({ 'data-account-control': 'true' }).props.onClick());
  expect(tree.root.findAllByProps({ 'data-settings-view': 'true' })).toHaveLength(1);
  expect(tree.root.findByProps({ 'data-chat-panel': 'mounted' })).toBe(chat);
  act(() => tree.root.findByProps({ 'aria-label': 'Close Navigator' }).props.onClick());
  expect(tree.root.findAllByProps({ 'data-account-control': 'true' })).toHaveLength(1);
  act(() => tree.root.findByProps({ 'data-account-control': 'true' }).props.onClick());
  expect(tree.root.findByProps({ 'data-chat-panel': 'mounted' })).toBe(chat);
  expect(shellState.mounted).toBe(mounted); expect(shellState.unmounted).toBe(unmounted);
  expect(tree.root.findByProps({ 'data-activity-strip': 'mounted' }).props['data-primary-session']).toBe('primary');
  act(() => tree.unmount());
  vi.unstubAllGlobals();
});


it('ordinary history selection opens an eligible chat directly and pauses the old composer during loading', async () => {
  shellState.query = 'agent=HELP_HUMAN';
  vi.stubGlobal('window', { setInterval: globalThis.setInterval, clearInterval: globalThis.clearInterval, localStorage: { getItem: () => null, setItem: vi.fn() }, addEventListener: vi.fn(), removeEventListener: vi.fn(), requestAnimationFrame: (cb: () => void) => cb() });
  vi.stubGlobal('document', { querySelector: () => ({ focus: vi.fn() }) });
  let tree!: ReactTestRenderer;
  await act(async () => { tree = create(<WovenDialogueShell defaultSurface="dialogue" />); });
  act(() => tree.root.findByType(RightPanel).props.onOpenFile(`${shellState.projectRoot}/report.md`));
  await act(async () => { tree.root.findByType(Navigator).props.onSelectSession('recorded'); });
  expect(tree.root.findByType(RightPanel).props.state).toMatchObject({ rightPanelView: 'files', openDocumentPath: 'report.md' });
  expect(tree.root.findByType('fieldset').props.disabled).toBe(true);
  await act(async () => { shellState.replayNotify?.({ status: 'READY', projection: { selectedSessionId: 'recorded', disclosure: 'READY_SNAPSHOT', session: { continuation: { roleId: 'HELP_HUMAN', projectRoot: shellState.projectRoot } } } }); });
  expect(shellState.resumedSession).toBe('recorded');
  expect(tree.root.findByType(RightPanel).props.state).toMatchObject({ rightPanelView: 'files', openDocumentPath: 'report.md' });
  expect(tree.root.findByType('fieldset').props.disabled).toBe(false);
  expect(tree.root.findAllByProps({ 'data-replay-lens': 'READY' })).toHaveLength(0);
  act(() => tree.unmount());
});

// Item 13: chats keep their folder. A chat recorded in another folder is
// listed under that folder, opening it re-selects the folder explicitly and
// resumes the chat there, and a folder that cannot be opened is reported with
// a recovery path rather than silently redirected.
describe('WovenDialogueShell per-chat folders', () => {
  const otherRoot = '/repo/projects/other-project';
  const stored = (extra: Record<string, unknown> = {}) => JSON.stringify({ schema: 'chirality.woven-workspace/v1',
    knownRoots: [{ path: '/repo/projects/chirality-app-dev', lastUsedAt: '2026-09-12T00:00:00Z' }, { path: otherRoot, lastUsedAt: '2026-09-11T00:00:00Z' }],
    chatIndex: { elsewhere: { projectRoot: otherRoot, persona: 'TASK', createdAt: '2026-09-11', updatedAt: '2026-09-11' } }, ...extra });
  beforeEach(() => {
    shellState.pathname = '/'; shellState.query = ''; shellState.projectRoot = '/repo/projects/chirality-app-dev'; shellState.streaming = false; shellState.extraSessions = [];
    shellState.replayLoad.mockClear(); shellState.applyProjectRoot.mockReset(); shellState.chooseProjectRoot.mockReset(); shellState.workspaceError = null;
    shellState.titleLoad.mockReset(); shellState.titleLoad.mockResolvedValue({}); shellState.useRealReader = false; shellState.initialActiveSession = 'primary';
    shellState.bindingLocked = false; shellState.newChatAccepted = true; shellState.newChatRequests = 0; shellState.resumedSession = undefined;
  });
  afterEach(() => { vi.unstubAllGlobals(); shellState.initialActiveSession = 'primary'; shellState.bindingLocked = false; });
  const settle = async () => { for (let tick = 0; tick < 6; tick += 1) await act(async () => { await Promise.resolve(); }); };

  it('lists chats from other folders under their folder, opens one by re-selecting its folder, and resumes it there', async () => {
    const persist = vi.fn();
    vi.stubGlobal('window', { setInterval: globalThis.setInterval, clearInterval: globalThis.clearInterval, localStorage: { getItem: () => stored(), setItem: persist }, addEventListener: vi.fn(), removeEventListener: vi.fn(), requestAnimationFrame: (cb: () => void) => cb() });
    vi.stubGlobal('document', { querySelector: () => ({ focus: vi.fn() }) });
    shellState.applyProjectRoot.mockImplementation(async (path: string) => { shellState.projectRoot = path; shellState.extraSessions = ['elsewhere']; return true; });
    let tree!: ReactTestRenderer;
    await act(async () => { tree = create(<WovenDialogueShell defaultSurface="dialogue" />); });
    const navigator = tree.root.findByType(Navigator);
    expect(navigator.props.currentRoot).toBe('/repo/projects/chirality-app-dev');
    expect(navigator.props.sessions.map((session: { sessionId: string; projectRoot: string }) => [session.sessionId, session.projectRoot])).toEqual([
      ['primary', '/repo/projects/chirality-app-dev'], ['recorded', '/repo/projects/chirality-app-dev'], ['elsewhere', otherRoot]
    ]);
    expect(tree.root.findAllByProps({ 'data-chat-folder': otherRoot })).toHaveLength(1);
    // The live listing of the current folder is indexed for later, without touching the other folder's entries.
    const indexed = JSON.parse(persist.mock.calls.at(-1)![1]).chatIndex;
    expect(indexed.elsewhere.projectRoot).toBe(otherRoot);
    expect(indexed.recorded.projectRoot).toBe('/repo/projects/chirality-app-dev');

    await act(async () => { navigator.props.onSelectSession('elsewhere'); });
    expect(shellState.applyProjectRoot).toHaveBeenCalledWith(otherRoot);
    await settle();
    expect(tree.root.findByType(Navigator).props.currentRoot).toBe(otherRoot);
    expect(shellState.replayLoad).toHaveBeenCalledWith('elsewhere');
    expect(tree.root.findByType(Navigator).props.folderNotices).toEqual({});
    act(() => tree.unmount());
  });

  it('closes a bound chat through New chat before switching folders, and only then opens the other folder\'s chat', async () => {
    shellState.bindingLocked = true;
    vi.stubGlobal('window', { setInterval: globalThis.setInterval, clearInterval: globalThis.clearInterval, localStorage: { getItem: () => stored(), setItem: vi.fn() }, addEventListener: vi.fn(), removeEventListener: vi.fn(), requestAnimationFrame: (cb: () => void) => cb() });
    vi.stubGlobal('document', { querySelector: () => ({ focus: vi.fn() }) });
    let applied = false;
    shellState.applyProjectRoot.mockImplementation(async (path: string) => { applied = true; shellState.projectRoot = path; shellState.extraSessions = ['elsewhere']; return true; });
    let tree!: ReactTestRenderer;
    await act(async () => { tree = create(<WovenDialogueShell defaultSurface="dialogue" />); });
    await settle();
    expect(tree.root.findByType(RightPanel).props.folderLocked).toBe(true);
    await act(async () => { tree.root.findByType(Navigator).props.onSelectSession('elsewhere'); });
    // The panel was asked to close its chat first; the folder switch waited for that.
    expect(shellState.newChatRequests).toBe(1);
    expect(applied).toBe(true);
    await settle();
    expect(tree.root.findByType(Navigator).props.currentRoot).toBe(otherRoot);
    expect(tree.root.findByType(RightPanel).props.folderMismatch).toBe(false);
    expect(shellState.replayLoad).toHaveBeenCalledWith('elsewhere');
    expect(tree.root.findByType(Navigator).props.folderNotices).toEqual({});
    act(() => tree.unmount());
  });

  it('leaves everything as it was when closing the current chat is declined', async () => {
    shellState.bindingLocked = true; shellState.newChatAccepted = false;
    vi.stubGlobal('window', { setInterval: globalThis.setInterval, clearInterval: globalThis.clearInterval, localStorage: { getItem: () => stored(), setItem: vi.fn() }, addEventListener: vi.fn(), removeEventListener: vi.fn(), requestAnimationFrame: (cb: () => void) => cb() });
    vi.stubGlobal('document', { querySelector: () => ({ focus: vi.fn() }) });
    let tree!: ReactTestRenderer;
    await act(async () => { tree = create(<WovenDialogueShell defaultSurface="dialogue" />); });
    await settle();
    await act(async () => { tree.root.findByType(Navigator).props.onSelectSession('elsewhere'); });
    await settle();
    expect(shellState.newChatRequests).toBe(1);
    expect(shellState.applyProjectRoot).not.toHaveBeenCalled();
    expect(shellState.replayLoad).not.toHaveBeenCalled();
    expect(tree.root.findByType(Navigator).props.currentRoot).toBe('/repo/projects/chirality-app-dev');
    expect(tree.root.findByType(Navigator).props.folderNotices).toEqual({});
    expect(tree.root.findByType(RightPanel).props.folderLocked).toBe(true);
    act(() => tree.unmount());
  });

  it('reports a chat its folder no longer lists and leaves a clean chat in that folder', async () => {
    shellState.bindingLocked = true;
    vi.stubGlobal('window', { setInterval: globalThis.setInterval, clearInterval: globalThis.clearInterval, localStorage: { getItem: () => stored(), setItem: vi.fn() }, addEventListener: vi.fn(), removeEventListener: vi.fn(), requestAnimationFrame: (cb: () => void) => cb() });
    vi.stubGlobal('document', { querySelector: () => ({ focus: vi.fn() }) });
    // The folder opens, but its listing does not contain the indexed chat.
    shellState.applyProjectRoot.mockImplementation(async (path: string) => { shellState.projectRoot = path; return true; });
    let tree!: ReactTestRenderer;
    await act(async () => { tree = create(<WovenDialogueShell defaultSurface="dialogue" />); });
    await settle();
    await act(async () => { tree.root.findByType(Navigator).props.onSelectSession('elsewhere'); });
    await settle();
    expect(shellState.replayLoad).not.toHaveBeenCalled();
    expect(tree.root.findByType(Navigator).props.currentRoot).toBe(otherRoot);
    expect(tree.root.findByType(Navigator).props.folderNotices[otherRoot]?.kind).toBe('unavailable');
    expect(tree.root.findByType(Navigator).props.folderNotices[otherRoot]?.message).toContain('was not found in');
    expect(tree.root.findByType(RightPanel).props.folderLocked).toBe(false);
    expect(tree.root.findByType(RightPanel).props.folderMismatch).toBe(false);
    act(() => tree.unmount());
  });

  it('reports a folder that cannot be opened with Locate and Forget instead of redirecting, and Forget drops only that folder', async () => {
    const persist = vi.fn();
    vi.stubGlobal('window', { setInterval: globalThis.setInterval, clearInterval: globalThis.clearInterval, localStorage: { getItem: () => stored(), setItem: persist }, addEventListener: vi.fn(), removeEventListener: vi.fn(), requestAnimationFrame: (cb: () => void) => cb() });
    vi.stubGlobal('document', { querySelector: () => ({ focus: vi.fn() }) });
    shellState.applyProjectRoot.mockImplementation(async () => { shellState.workspaceError = 'Working root is not accessible'; return false; });
    let tree!: ReactTestRenderer;
    await act(async () => { tree = create(<WovenDialogueShell defaultSurface="dialogue" />); });
    await act(async () => { tree.root.findByType(Navigator).props.onSelectSession('elsewhere'); });
    await act(async () => { await Promise.resolve(); });
    expect(tree.root.findByType(Navigator).props.currentRoot).toBe('/repo/projects/chirality-app-dev');
    expect(shellState.replayLoad).not.toHaveBeenCalledWith('elsewhere');
    const notice = tree.root.findByProps({ role: 'alert', className: 'woven-folder-notice woven-folder-notice--unavailable' });
    expect(notice.findByType('p').children.join('')).toContain('Working root is not accessible');
    expect(notice.findByType('p').children.join('')).toContain('never moved to another folder');
    const labels = notice.findAllByType('button').map(button => button.children.join(''));
    expect(labels).toEqual(['Locate folder…', 'Forget folder']);
    // The chat is still listed under its recorded folder.
    expect(tree.root.findAllByProps({ 'data-session-id': 'elsewhere' }).length).toBeGreaterThan(0);

    await act(async () => { notice.findAllByType('button')[0].props.onClick(); });
    expect(shellState.chooseProjectRoot).toHaveBeenCalledTimes(1);

    await act(async () => { notice.findAllByType('button')[1].props.onClick(); });
    expect(tree.root.findAllByProps({ 'data-chat-folder': otherRoot })).toHaveLength(0);
    const state = JSON.parse(persist.mock.calls.at(-1)![1]);
    expect(state.knownRoots.map((root: { path: string }) => root.path)).toEqual(['/repo/projects/chirality-app-dev']);
    expect(state.chatIndex.elsewhere).toBeUndefined();
    expect(state.chatIndex.recorded.projectRoot).toBe('/repo/projects/chirality-app-dev');
    act(() => tree.unmount());
  });

  it('restores the last active chat of the current folder on launch and remembers the document each chat had open', async () => {
    // On a fresh launch the chat panel has no session yet; the restore fills it.
    // The recorded role matches the current one, so the resume reaches the panel without a role redirect.
    shellState.initialActiveSession = undefined; shellState.query = 'agent=HELP_HUMAN';
    const persist = vi.fn();
    vi.stubGlobal('window', { setInterval: globalThis.setInterval, clearInterval: globalThis.clearInterval, localStorage: { getItem: () => stored({ lastActiveChat: { sessionId: 'recorded', projectRoot: '/repo/projects/chirality-app-dev' }, chatDocuments: { recorded: 'notes.md' } }), setItem: persist }, addEventListener: vi.fn(), removeEventListener: vi.fn(), requestAnimationFrame: (cb: () => void) => cb() });
    vi.stubGlobal('document', { querySelector: () => ({ focus: vi.fn() }) });
    let tree!: ReactTestRenderer;
    await act(async () => { tree = create(<WovenDialogueShell defaultSurface="dialogue" />); });
    await settle();
    expect(shellState.replayLoad).toHaveBeenCalledWith('recorded');
    await act(async () => { shellState.replayNotify?.({ status: 'READY', projection: { selectedSessionId: 'recorded', disclosure: 'READY_SNAPSHOT', session: { continuation: { roleId: 'HELP_HUMAN', projectRoot: shellState.projectRoot } } } }); });
    expect(shellState.resumedSession).toBe('recorded');
    const persistedState = JSON.parse(persist.mock.calls.at(-1)![1]);
    expect(persistedState.lastActiveChat).toEqual({ sessionId: 'recorded', projectRoot: '/repo/projects/chirality-app-dev' });
    act(() => tree.unmount());
  });

  it('does not hand an open document to a chat that never had one, and records only documents opened in that chat', async () => {
    shellState.query = 'agent=HELP_HUMAN';
    const persist = vi.fn();
    vi.stubGlobal('window', { setInterval: globalThis.setInterval, clearInterval: globalThis.clearInterval, localStorage: { getItem: () => stored(), setItem: persist }, addEventListener: vi.fn(), removeEventListener: vi.fn(), requestAnimationFrame: (cb: () => void) => cb() });
    vi.stubGlobal('document', { querySelector: () => ({ focus: vi.fn() }) });
    let tree!: ReactTestRenderer;
    await act(async () => { tree = create(<WovenDialogueShell defaultSurface="dialogue" />); });
    await settle();
    const documents = () => JSON.parse(persist.mock.calls.at(-1)![1]).chatDocuments ?? {};
    // A chat open before the listing settled is recorded as the last active chat rather than blocking recording.
    expect(JSON.parse(persist.mock.calls.at(-1)![1]).lastActiveChat.sessionId).toBe('primary');
    act(() => tree.root.findByType(RightPanel).props.onOpenFile('/repo/projects/chirality-app-dev/docs/SPEC.md'));
    expect(documents()).toEqual({ primary: 'docs/SPEC.md' });

    // Continuing a chat with no remembered document must not attribute the document still on screen to it.
    shellState.resumedSession = undefined;
    act(() => tree.root.findByType(RightPanel).props.onOpenParent('recorded'));
    expect(shellState.replayLoad).toHaveBeenCalledWith('recorded');
    const projection = { selectedSessionId: 'recorded', sourceReference: 'session:recorded/events', observedAt: '2026-09-09', disclosure: 'READY_SNAPSHOT', currency: 'CURRENT', transcript: { itemCount: 0, items: [] }, instructionHistory: [], instructionBases: [], malformedLineCount: 0, sourceEventCount: 0, renderedItemCount: 0, diagnostics: [], session: { sessionId: 'recorded', parentage: { state: 'NOT_RECORDED' }, diagnostics: [], continuation: { schemaVersion: 'chirality.session/v3', projectRoot: shellState.projectRoot, roleId: 'HELP_HUMAN', mode: 'CHAT', interactionMode: 'chat', permissionMode: 'ask', selectedMethods: [], methodSelectionRevision: 1, instructionBasisId: 'basis-1' } } };
    await act(async () => shellState.replayNotify?.({ status: 'READY', projection }));
    await act(async () => tree.root.findAllByType('button').find(button => button.children.includes('Continue this chat'))!.props.onClick());
    await settle();
    expect(shellState.resumedSession).toBe('recorded');
    expect(JSON.parse(persist.mock.calls.at(-1)![1]).lastActiveChat.sessionId).toBe('recorded');
    expect(documents()).toEqual({ primary: 'docs/SPEC.md' });

    // A document opened while that chat is active is remembered for it alone.
    act(() => tree.root.findByType(RightPanel).props.onOpenFile('/repo/projects/chirality-app-dev/docs/TYPES.md'));
    expect(documents()).toEqual({ primary: 'docs/SPEC.md', recorded: 'docs/TYPES.md' });
    act(() => tree.unmount());
  });

  it('does not attribute a document opened while no chat was active to the chat resumed afterwards', async () => {
    shellState.query = 'agent=HELP_HUMAN';
    const persist = vi.fn();
    vi.stubGlobal('window', { setInterval: globalThis.setInterval, clearInterval: globalThis.clearInterval, localStorage: { getItem: () => stored(), setItem: persist }, addEventListener: vi.fn(), removeEventListener: vi.fn(), requestAnimationFrame: (cb: () => void) => cb() });
    vi.stubGlobal('document', { querySelector: () => ({ focus: vi.fn() }) });
    let tree!: ReactTestRenderer;
    await act(async () => { tree = create(<WovenDialogueShell defaultSurface="dialogue" />); });
    await settle();
    const documents = () => JSON.parse(persist.mock.calls.at(-1)![1]).chatDocuments ?? {};
    act(() => tree.root.findByType(RightPanel).props.onOpenFile('/repo/projects/chirality-app-dev/docs/SPEC.md'));
    expect(documents()).toEqual({ primary: 'docs/SPEC.md' });
    // New chat: no chat is active; a document opened now belongs to no chat.
    await act(async () => { tree.root.findByType(Navigator).props.onNewChat(); });
    expect(shellState.newChatRequests).toBe(1);
    act(() => tree.root.findByType(RightPanel).props.onOpenFile('/repo/projects/chirality-app-dev/docs/TYPES.md'));
    expect(documents()).toEqual({ primary: 'docs/SPEC.md' });
    // Resuming the earlier chat brings back its own document, not the one opened in between.
    act(() => tree.root.findByType(RightPanel).props.onOpenParent('primary'));
    const projection = { selectedSessionId: 'primary', sourceReference: 'session:primary/events', observedAt: '2026-09-09', disclosure: 'READY_SNAPSHOT', currency: 'CURRENT', transcript: { itemCount: 0, items: [] }, instructionHistory: [], instructionBases: [], malformedLineCount: 0, sourceEventCount: 0, renderedItemCount: 0, diagnostics: [], session: { sessionId: 'primary', parentage: { state: 'NOT_RECORDED' }, diagnostics: [], continuation: { schemaVersion: 'chirality.session/v3', projectRoot: shellState.projectRoot, roleId: 'HELP_HUMAN', mode: 'CHAT', interactionMode: 'chat', permissionMode: 'ask', selectedMethods: [], methodSelectionRevision: 1, instructionBasisId: 'basis-1' } } };
    await act(async () => shellState.replayNotify?.({ status: 'READY', projection }));
    await act(async () => tree.root.findAllByType('button').find(button => button.children.includes('Continue this chat'))!.props.onClick());
    await settle();
    expect(shellState.resumedSession).toBe('primary');
    expect(documents()).toEqual({ primary: 'docs/SPEC.md' });
    expect(JSON.parse(persist.mock.calls.at(-1)![1]).openDocumentPath).toBe('docs/SPEC.md');
    // Not even transiently: before the fix the resume render recorded TYPES.md for the chat and the restore overwrote it a render later.
    expect(persist.mock.calls.every(call => (JSON.parse(call[1]).chatDocuments ?? {}).primary !== 'docs/TYPES.md')).toBe(true);
    act(() => tree.unmount());
  });

  it('does not restore a last chat recorded in a different folder, and never while a turn is running', async () => {
    shellState.initialActiveSession = undefined;
    vi.stubGlobal('window', { setInterval: globalThis.setInterval, clearInterval: globalThis.clearInterval, localStorage: { getItem: () => stored({ lastActiveChat: { sessionId: 'elsewhere', projectRoot: otherRoot } }), setItem: vi.fn() }, addEventListener: vi.fn(), removeEventListener: vi.fn(), requestAnimationFrame: (cb: () => void) => cb() });
    vi.stubGlobal('document', { querySelector: () => ({ focus: vi.fn() }) });
    let tree!: ReactTestRenderer;
    await act(async () => { tree = create(<WovenDialogueShell defaultSurface="dialogue" />); });
    await settle();
    expect(shellState.replayLoad).not.toHaveBeenCalled();
    expect(shellState.applyProjectRoot).not.toHaveBeenCalled();
    act(() => tree.unmount());
  });
});


describe('cross-chat attention', () => {
  it('answers a live second-folder request without switching or stopping the running primary, then clears stale attention and cleans up', async () => {
    vi.useFakeTimers();
    const client = await import('../../lib/harness/client');
    const list = vi.mocked(client.listHarnessSessions);
    const priorList = list.getMockImplementation();
    const requests = vi.mocked(client.listHarnessSessionRequests);
    const answer = vi.mocked(client.answerHarnessSessionRequest);
    let pending = true;
    const request = { requestId: 'same-id', method: 'item/tool/requestUserInput', params: { questions: [{ id: 'choice', header: 'Choice', question: 'Which venue?' }] }, receivedAt: '2026-09-13' };
    list.mockImplementation(async root => {
      if (root === '/missing') throw new Error('folder unavailable');
      return [{ sessionId: root === '/second' ? 'second' : 'primary', projectRoot: root, persona: 'TASK', mode: '', createdAt: '', updatedAt: '', status: 'running' }];
    });
    requests.mockImplementation(async id => {
      if (id === 'primary') throw new Error('temporary request lookup failure');
      return { requests: id === 'second' && pending ? [request] : [] } as never;
    });
    answer.mockClear();
    answer.mockImplementation(async () => { pending = false; return { sent: true }; });
    shellState.projectRoot = '/first'; shellState.streaming = true; shellState.initialActiveSession = 'primary'; shellState.mounted = 0; shellState.unmounted = 0; shellState.replayLoad.mockClear();
    vi.stubGlobal('HTMLElement', class {});
    vi.stubGlobal('document', { activeElement: null, querySelector: () => null });
    vi.stubGlobal('window', { setInterval: globalThis.setInterval, clearInterval: globalThis.clearInterval, addEventListener: vi.fn(), removeEventListener: vi.fn(), requestAnimationFrame: (cb: () => void) => cb(), localStorage: { getItem: () => JSON.stringify({ schema: 'chirality.woven-workspace/v1', knownRoots: [{ path: '/second', lastUsedAt: '2026-09-13T00:00:00Z' }, { path: '/missing', lastUsedAt: '2026-09-12T00:00:00Z' }], chatTitles: { second: 'Venue comparison' } }), setItem: vi.fn() } });
    let tree!: ReactTestRenderer;
    try {
      await act(async () => { tree = create(<WovenDialogueShell defaultSurface="dialogue" />); });
      const needsAnswer = () => tree.root.findAllByType('button').find(button => button.props['aria-label'] === 'Needs answer: Venue comparison');
      expect(needsAnswer()).toBeDefined();
      expect(tree.root.findAllByType('button').find(button => button.props['data-session-id'] === 'second')?.props.disabled).toBe(true);
      await act(async () => needsAnswer()!.props.onClick());
      expect(tree.root.findByProps({ role: 'dialog' }).findByType('h2').children).toEqual(['Venue comparison']);
      await act(async () => { await vi.advanceTimersByTimeAsync(5000); });
      expect(needsAnswer()).toBeDefined(); // Missing folder lookup does not erase the second chat.
      const field = tree.root.findByProps({ role: 'dialog' }).findByType('input');
      await act(async () => field.props.onChange({ target: { value: 'Venue B' } }));
      pending = false; // Another renderer resolved it after the last poll.
      await act(async () => tree.root.findByType('form').props.onSubmit({ preventDefault: vi.fn() }));
      expect(answer).not.toHaveBeenCalled();
      expect(JSON.stringify(tree.toJSON())).toContain('This request is no longer pending.');
      pending = true;
      await act(async () => tree.root.findByType('form').props.onSubmit({ preventDefault: vi.fn() }));
      expect(answer).toHaveBeenCalledWith({ sessionId: 'second', requestId: 'same-id', answer: { kind: 'userInput', answers: { choice: { answers: ['Venue B'] } } } });
      expect(shellState.streaming).toBe(true); expect(shellState.mounted).toBe(1); expect(shellState.unmounted).toBe(0); expect(shellState.replayLoad).not.toHaveBeenCalled();
      expect(tree.root.findAllByType('button').some(button => button.children.join('') === 'Stop')).toBe(false);
      await act(async () => { await vi.advanceTimersByTimeAsync(2000); });
      expect(needsAnswer()).toBeUndefined();
      expect(JSON.stringify(tree.toJSON())).toContain('No pending requests for this chat.');
      await act(async () => tree.unmount());
      const calls = requests.mock.calls.length;
      await act(async () => { await vi.advanceTimersByTimeAsync(10000); });
      expect(requests).toHaveBeenCalledTimes(calls);
    } finally {
      if (tree) act(() => tree.unmount());
      list.mockImplementation(priorList!); requests.mockResolvedValue({ requests: [] } as never); answer.mockResolvedValue({ sent: true });
      shellState.streaming = false; vi.useRealTimers(); vi.unstubAllGlobals();
    }
  });
});
