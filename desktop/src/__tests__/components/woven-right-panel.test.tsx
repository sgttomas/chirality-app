import React from 'react';
import { renderToStaticMarkup } from 'react-dom/server';
import { act, create, type ReactTestRenderer } from 'react-test-renderer';
import type { SelectedSessionReplayState } from '../../lib/woven-dialogue/contracts';
import { afterEach, expect, it, vi } from 'vitest';
import { RightPanel } from '../../components/woven-dialogue/right-panel';
import { createDefaultWovenWorkspaceState } from '../../lib/woven-dialogue/woven-workspace-state';
vi.mock('../../components/woven-dialogue/activity-shelf', () => ({ ActivityView: () => <p>Activity details</p> }));
vi.mock('../../components/woven-dialogue/method-library-view', () => ({ MethodLibraryView: ({ view }: { view: string }) => <p>Library view {view}</p> }));
vi.mock('../../components/workspace/workspace-provider', () => ({ useWorkspace: () => ({ projectRoot: '/root' }) }));
vi.mock('../../components/shell/file-tree-panel', () => ({ FileTreePanel: () => <p>Existing file contents</p> }));
const handoff = vi.hoisted(() => vi.fn(async (_input: unknown) => {}));
vi.mock('../../components/shell/document-view', () => ({ handoffDocument: handoff, DocumentView: ({ target }: { target: string }) => <p>Document {target}</p> }));
const handlers = { onView: vi.fn(), onOpenFile: vi.fn(), onClose: vi.fn(), onExpand: vi.fn(), coordination: <p>Recorded agents and session content</p> };
it('renders the stored Settings view and its breadcrumb without falling back to Files', () => {
  const state = { ...createDefaultWovenWorkspaceState(), rightPanelView: 'settings' as const };
  const html = renderToStaticMarkup(<RightPanel {...handlers} state={state} sessionOpen={false} settingsView={<p>Account and appearance controls</p>} />);
  expect(html).toContain('Account and appearance controls'); expect(html).toContain('Settings breadcrumb');
  expect(html).not.toContain('Existing file contents');
  const unavailable = renderToStaticMarkup(<RightPanel {...handlers} state={state} sessionOpen={false} />);
  expect(unavailable).toContain('Settings are unavailable.');
});
it('shows document breadcrumb and current controls without deferred popout', () => {
  const html = renderToStaticMarkup(<RightPanel {...handlers} state={{ ...createDefaultWovenWorkspaceState(), openDocumentPath: 'pkg/spec.md' }} sessionOpen={false} />);
  expect(html).toContain('Document breadcrumb'); expect(html).toContain('pkg/spec.md'); expect(html).toContain('Close detail'); expect(html).not.toContain('Pop out');
});
it('keeps recorded session content under its breadcrumb', () => {
  const html = renderToStaticMarkup(<RightPanel {...handlers} state={{ ...createDefaultWovenWorkspaceState(), rightPanelView: 'agents' }} sessionOpen />);
  expect(html).toContain('Session breadcrumb'); expect(html).toContain('Recorded agents and session content');
  expect(html).toContain('>Agents</button> › Session'); expect(html).not.toContain('Who is working');
});

afterEach(() => vi.unstubAllGlobals());
function readySession(): Extract<SelectedSessionReplayState, { status: 'READY' }> {
  return { status: 'READY', projection: {
    selectedSessionId: 'child-exact', sourceReference: 'events:child-exact', observedAt: '2026-09-05T10:00:00Z', disclosure: 'READY_SNAPSHOT', currency: 'CURRENT',
    sourceEventCount: 5, renderedItemCount: 3, malformedLineCount: 0, transcript: { itemCount: 0, items: [] }, instructionHistory: [], instructionBases: [], diagnostics: [],
    session: { projectionId: 'session:child-exact', sessionId: 'child-exact', sourceReference: 'record:child-exact', observedAt: '2026-09-05T10:00:00Z', currency: 'CURRENT', persona: 'TASK', parentage: { state: 'RECORDED', parentSessionId: 'parent', parentAvailable: true }, diagnostics: [] }
  } };
}
it('copies exact id and deterministic recorded metadata, exposes clipboard outcome, and opens recorded parent', async () => {
  const writeText = vi.fn(async (_value: string) => {}); vi.stubGlobal('navigator', { clipboard: { writeText } });
  const onOpenParent = vi.fn(); const replayState = readySession(); let tree!: ReactTestRenderer;
  await act(async () => { tree = create(<RightPanel {...handlers} state={{ ...createDefaultWovenWorkspaceState(), rightPanelView: 'agents' }} sessionOpen replayState={replayState} recordedSessionIds={['child-exact', 'parent']} onOpenParent={onOpenParent} />); });
  const button = (label: string) => tree.root.findAllByType('button').find(x => x.children.includes(label))!;
  await act(async () => button('Copy session id').props.onClick()); expect(writeText).toHaveBeenLastCalledWith('child-exact');
  expect(tree.root.findByProps({ role: 'status' }).children).toEqual(['Session id copied.']);
  await act(async () => button('Copy summary').props.onClick());
  const copied = writeText.mock.calls.at(-1)![0];
  expect(copied).toMatch(/^Recorded session metadata \(read-only snapshot\)/);
  expect(JSON.parse(copied.split('\n').slice(1).join('\n'))).toMatchObject({ selectedSessionId: 'child-exact', sourceReference: 'events:child-exact', sourceEventCount: 5, renderedItemCount: 3, recordedAttribution: { persona: 'TASK', parentage: { parentSessionId: 'parent' } } });
  expect(copied).not.toContain('purpose'); expect(copied).not.toContain('result');
  await act(async () => button('Copy summary').props.onClick()); expect(writeText).toHaveBeenLastCalledWith(copied);
  expect(button('Open parent chat').props.disabled).toBe(false); act(() => button('Open parent chat').props.onClick()); expect(onOpenParent).toHaveBeenCalledWith('parent');
  writeText.mockRejectedValue(new Error('Clipboard denied')); await act(async () => button('Copy session id').props.onClick());
  expect(tree.root.findByProps({ role: 'alert' }).children).toEqual(['Unable to copy session id.']); expect(tree.root.findAllByProps({ role: 'status' })).toHaveLength(0);
  act(() => tree.unmount());
});
it.each(['unknown', 'unavailable', 'conflicting', 'missing-roster', 'live-turn'] as const)('explains and disables %s parent without navigating', async reason => {
  const replayState = readySession(); const onOpenParent = vi.fn();
  if (reason === 'unknown') replayState.projection.session!.parentage = { state: 'NOT_RECORDED' };
  if (reason === 'unavailable') replayState.projection.session!.parentage = { state: 'RECORDED', parentSessionId: 'parent', parentAvailable: false };
  if (reason === 'conflicting') replayState.projection.currency = 'CONFLICTING';
  let tree!: ReactTestRenderer; await act(async () => { tree = create(<RightPanel {...handlers} state={{ ...createDefaultWovenWorkspaceState(), rightPanelView: 'agents' }} sessionOpen replayState={replayState} recordedSessionIds={reason === 'missing-roster' ? [] : ['parent']} liveTurnActive={reason === 'live-turn'} onOpenParent={onOpenParent} />); });
  const button = tree.root.findAllByType('button').find(x => x.children.includes('Open parent chat'))!;
  expect(button.props.disabled).toBe(true); expect(button.props['aria-describedby']).toBe('session-parent-explanation');
  expect(tree.root.findByProps({ id: 'session-parent-explanation' }).children.join('')).toMatch(/recorded|Recorded|live turn/);
  act(() => button.props.onClick()); expect(onOpenParent).not.toHaveBeenCalled(); act(() => tree.unmount());
});

it('reveals the root and the selected file through distinct bounded actions', async () => {
  handoff.mockClear(); let tree!: ReactTestRenderer;
  await act(async () => { tree = create(<RightPanel {...handlers} state={createDefaultWovenWorkspaceState()} sessionOpen={false} />); });
  await act(async () => tree.root.findAllByType('button').find(x => x.children.join('') === 'Reveal root in Finder')!.props.onClick());
  expect(handoff).toHaveBeenLastCalledWith({ projectRoot: '/root', action: 'reveal-root' });
  act(() => tree.update(<RightPanel {...handlers} state={{ ...createDefaultWovenWorkspaceState(), openDocumentPath: 'spec.md' }} sessionOpen={false} />));
  await act(async () => tree.root.findAllByType('button').find(x => x.children.join('') === 'Reveal file in Finder')!.props.onClick());
  expect(handoff).toHaveBeenLastCalledWith({ projectRoot: '/root', target: 'spec.md', action: 'reveal' });
  act(() => tree.unmount());
});

it('keeps six-view keyboard navigation and reveals the selected tab after changes', async () => {
  const onView = vi.fn(); const focus = vi.fn(); const scrollIntoView = vi.fn(); const selectors: string[] = [];
  const tabNode = { querySelector: (selector: string) => { selectors.push(selector); return { scrollIntoView }; } };
  let tree!: ReactTestRenderer;
  const props = { ...handlers, onView, sessionOpen: false };
  const state = createDefaultWovenWorkspaceState();
  await act(async () => { tree = create(<RightPanel {...props} state={state} />, { createNodeMock: element => element.props.role === 'tablist' ? tabNode : null }); });
  const key = (value: string) => tree.root.findByProps({ role: 'tablist' }).props.onKeyDown({ key: value, preventDefault: vi.fn(), currentTarget: { querySelector: () => ({ focus }) } });
  expect(tree.root.findAllByProps({ role: 'tab' }).map(tab => tab.props['data-view'])).toEqual(['files', 'plan', 'workflows', 'agents', 'activity']);
  expect(tree.root.findAllByProps({ role: 'tab' }).map(tab => tab.children.join(''))).toEqual(['Files', 'Plan', 'Workflows', 'Agents', 'Activity']);
  act(() => key('ArrowRight')); expect(onView).toHaveBeenLastCalledWith('plan');
  act(() => key('ArrowLeft')); expect(onView).toHaveBeenLastCalledWith('activity');
  act(() => key('End')); expect(onView).toHaveBeenLastCalledWith('activity');
  await act(async () => tree.update(<RightPanel {...props} state={{ ...state, rightPanelView: 'activity' }} />));
  act(() => key('ArrowRight')); expect(onView).toHaveBeenLastCalledWith('files');
  act(() => key('Home')); expect(onView).toHaveBeenLastCalledWith('files');
  expect(focus).toHaveBeenCalledTimes(5); expect(selectors).toEqual(['[aria-selected="true"]', '[aria-selected="true"]']);
  expect(scrollIntoView).toHaveBeenLastCalledWith({ block: 'nearest', inline: 'nearest' });
  act(() => tree.unmount());
});

it('renders the Plan tab from the host-supplied model and redirects a saved Skills view to Workflows', () => {
  const state = createDefaultWovenWorkspaceState();
  const empty = renderToStaticMarkup(<RightPanel {...handlers} state={{ ...state, rightPanelView: 'plan' }} sessionOpen={false} />);
  expect(empty).toContain('No plan in this chat yet');
  const model = { revisions: [{ revision: 1, sourceEvent: { qualificationState: 'qualified' as const, eventId: 'plan-1', occurredAt: '2026-09-12T00:00:00.000Z', qualification: { adapterId: 'codex-app-server', providerId: 'openai', qualificationId: 'fixture', admissionSha256: 'a'.repeat(64), evidenceClass: 'native-adapter-qualified' as const }, plan: '# Plan one\n\nStep.' } }],
    clarifications: [], active: true, refreshing: false, fileCatalog: [], actionsDisabled: false, onRefresh: vi.fn(), onRevise: vi.fn(), onSave: vi.fn(), onExecute: vi.fn(), onSaveAsWorkflow: vi.fn(), onReplyClarification: vi.fn() };
  const plan = renderToStaticMarkup(<RightPanel {...handlers} state={{ ...state, rightPanelView: 'plan' }} sessionOpen={false} planPanel={model} />);
  for (const label of ['Revise in chat', 'Execute plan', 'Turn into workflow', 'Save plan…']) expect(plan).toContain(label);
  expect(plan).toContain('Plan one');
  expect(plan).not.toContain('woven-tab-count');
  const skills = renderToStaticMarkup(<RightPanel {...handlers} state={{ ...state, rightPanelView: 'skills' }} sessionOpen={false} />);
  expect(skills).toContain('Library view workflows');
  expect(skills).not.toContain('right-tab-skills');
  const workflows = renderToStaticMarkup(<RightPanel {...handlers} state={{ ...state, rightPanelView: 'workflows' }} sessionOpen={false} />);
  expect(workflows).toContain('Library view workflows');
});

it('clears viewed Plan badges, counts later revisions, and keeps session read states separate', async () => {
  const revision = (number: number) => ({ revision: number, sourceEvent: { plan: `Plan ${number}` } } as unknown as import('@chirality/runtime-contracts').NativePlanRevision);
  const model: import('../../components/shell/native-plan-panel').NativePlanPanelModel = { sessionId: 'one', revisions: [revision(1)], clarifications: [], active: false, refreshing: false, fileCatalog: [], actionsDisabled: false,
    onRefresh: vi.fn(), onRevise: vi.fn(), onSave: vi.fn(), onExecute: vi.fn(), onSaveAsWorkflow: vi.fn(), onReplyClarification: vi.fn() };
  let tree!: ReactTestRenderer;
  const state = createDefaultWovenWorkspaceState();
  function RetainedPanel({ view = 'files', planPanel = model, collapsed = false }: { view?: 'files' | 'plan'; planPanel?: typeof model; collapsed?: boolean }) {
    const [read, setRead] = React.useState<Record<string, number>>({});
    const mark = React.useCallback((id: string, revision: number) => setRead(current => (current[id] ?? 0) >= revision ? current : { ...current, [id]: revision }), []);
    return collapsed ? null : <RightPanel {...handlers} state={{ ...state, rightPanelView: view }} sessionOpen={false} planPanel={planPanel} readPlanRevisions={read} onPlanRead={mark} />;
  }
  const update = async (view: 'files' | 'plan', planPanel = model) => act(async () => tree.update(<RetainedPanel view={view} planPanel={planPanel} />));
  const badges = () => tree.root.findAllByProps({ className: 'woven-tab-count' });
  await act(async () => { tree = create(<RetainedPanel />); });
  expect(badges()[0].props['aria-label']).toBe('1 unread plan revisions');
  await update('plan'); expect(badges()).toHaveLength(0);
  await update('files'); expect(badges()).toHaveLength(0);
  await act(async () => tree.update(<RetainedPanel collapsed />));
  await update('files'); expect(badges()).toHaveLength(0);
  const next = { ...model, revisions: [revision(1), revision(2)] };
  await update('files', next); expect(badges()[0].children).toEqual(['1']);
  await update('plan', next); await update('files', next); expect(badges()).toHaveLength(0);
  await update('files', { ...model, sessionId: 'two' }); expect(badges()).toHaveLength(1);
  await update('files', next); expect(badges()).toHaveLength(0);
  act(() => tree.unmount());
});
