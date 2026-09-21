import React, { useSyncExternalStore } from 'react';
import { act, create, type ReactTestRenderer } from 'react-test-renderer';
import { beforeEach, afterEach, expect, it, vi } from 'vitest';
import { buildChatDraftStorageKey } from '../../lib/harness/chat-draft';
import { HostedBootstrapProvider } from '../../lib/harness/hosted-bootstrap-context';
import type { HostedBootstrapStatusResponse } from '../../lib/harness/hosted-bootstrap-client';
import type { SelectedSessionReplayProjection } from '../../lib/woven-dialogue/contracts';

// Pattern from chat-panel-folder-binding.test.tsx: hermetic ChatPanel with the
// harness client, workspace, and method-selection surfaces stubbed. The hosted
// bootstrap status reaches the panel only through the real provider/context.
const state = vi.hoisted(() => ({ root: '/chosen/subfolder', query: '', listeners: new Set<() => void>(),
  create: vi.fn(), boot: vi.fn(), replay: vi.fn(), stream: vi.fn(), apply: vi.fn(), append: vi.fn(), clear: vi.fn(), hydrate: vi.fn(), streaming: vi.fn(), turnState: vi.fn(), attach: vi.fn(),
  replaceMethods: vi.fn(), resolveContext: vi.fn(),
  nativeCapability: vi.fn(), nativeRevisions: vi.fn(), nativeClarifications: vi.fn(), replyClarification: vi.fn(), exportPlan: vi.fn()
}));
vi.mock('next/navigation', () => ({ usePathname: () => '/chat', useSearchParams: () => new URLSearchParams(state.query), useRouter: () => ({ replace: vi.fn() }) }));
vi.mock('../../components/workspace/workspace-provider', () => ({ useWorkspace: () => ({
  projectRoot: useSyncExternalStore(listener => { state.listeners.add(listener); return () => state.listeners.delete(listener); }, () => state.root),
  applyProjectRoot: state.apply, chooseProjectRoot: vi.fn(async () => false), hasElectronDirectoryPicker: false, errorMessage: null
}) }));
vi.mock('../../components/workspace/toolkit-provider', () => ({ useToolkit: () => ({ optsPayload: undefined }) }));
vi.mock('../../components/workspace/harness-events-provider', () => ({ useHarnessEventActions: () => ({ appendEvent: state.append, clearEvents: state.clear, hydrateEvents: state.hydrate, setStreaming: state.streaming }), useHarnessEvents: () => ({ events: [], streaming: false }) }));
vi.mock('../../components/shell/runtime-connectivity-provider', () => ({ useRuntimeEpoch: () => 0 }));
vi.mock('../../components/shell/persona-picker', () => ({ PersonaPicker: () => <span>Working Items</span> }));
vi.mock('../../components/shell/file-picker', () => ({ FilePicker: () => null }));
vi.mock('../../components/shell/permission-requests', () => ({ PermissionRequests: () => null }));
vi.mock('../../components/shell/chat-markdown', () => ({ ChatMarkdown: (props: { source: string }) => <p>{props.source}</p> }));
vi.mock('../../lib/harness/method-selection-client', async importOriginal => ({
  ...await importOriginal<typeof import('../../lib/harness/method-selection-client')>(),
  replaceSelectedMethods: state.replaceMethods,
  resolveSelectedContext: state.resolveContext,
  getNativePlanCapability: state.nativeCapability,
  listNativePlanRevisions: state.nativeRevisions,
  listNativePlanClarifications: state.nativeClarifications,
  replyNativePlanClarification: state.replyClarification,
  exportNativePlanRevision: state.exportPlan
}));
vi.mock('../../lib/harness/client', async importOriginal => ({ ...await importOriginal<typeof import('../../lib/harness/client')>(), createHarnessSession: state.create, bootHarnessSession: state.boot, replaySessionEvents: state.replay, streamHarnessTurn: state.stream, interruptHarnessSession: vi.fn(), getHarnessTurnState: state.turnState, attachHarnessTurn: state.attach }));
import { ChatPanel } from '../../components/shell/chat-panel';
import { HarnessApiClientError } from '../../lib/harness/client';

const SIGNED_OUT_TITLE = 'Sign in to Codex to choose a model';
const catalog = [
  { model: 'gpt-default', isDefault: true, defaultReasoningEffort: 'high', supportedReasoningEfforts: ['low', 'medium', 'high'] },
  { model: 'gpt-alt', isDefault: false, defaultReasoningEffort: 'medium', supportedReasoningEfforts: ['medium', 'low'] }
] as const;
function snapshot(input: { ceremony?: string; admission?: string; withCatalog?: boolean } = {}): HostedBootstrapStatusResponse {
  const { ceremony = 'signed-in', admission = 'ready', withCatalog = true } = input;
  return { registration: 'registered', projectId: 'project-one', status: {
    schema: 'chirality-hosted-bootstrap-status/v1', projectId: 'project-one',
    ceremony: ceremony as 'signed-in', admission: admission as 'ready', canStartLogin: false,
    ...(withCatalog && ceremony === 'signed-in' && admission === 'ready'
      ? { models: catalog.map(entry => ({ ...entry, supportedReasoningEfforts: [...entry.supportedReasoningEfforts] })), selection: { model: 'gpt-default', reasoningEffort: 'high' } }
      : {})
  } };
}

function reducedSnapshot(): HostedBootstrapStatusResponse {
  const base = snapshot();
  if (base.registration !== 'registered') throw new Error('fixture');
  return { ...base, status: { ...base.status, models: [{ ...catalog[0], supportedReasoningEfforts: [...catalog[0].supportedReasoningEfforts] }], selection: { model: 'gpt-default', reasoningEffort: 'high' } } };
}

let tree: ReactTestRenderer | undefined;
let values: Map<string, string>;
const entryKey = buildChatDraftStorageKey('/chosen/subfolder', 'WORKING_ITEMS', 'CHAT');
async function mount(hosted: HostedBootstrapStatusResponse | null | 'no-provider' = 'no-provider', props: Partial<React.ComponentProps<typeof ChatPanel>> = {}) {
  await act(async () => {
    tree = create(hosted === 'no-provider'
      ? <ChatPanel presentation="woven" {...props} />
      : <HostedBootstrapProvider snapshot={hosted} loading={false}><ChatPanel presentation="woven" {...props} /></HostedBootstrapProvider>);
  });
}
async function update(hosted: HostedBootstrapStatusResponse | null, props: Partial<React.ComponentProps<typeof ChatPanel>> = {}) {
  await act(async () => { tree!.update(<HostedBootstrapProvider snapshot={hosted} loading={false}><ChatPanel presentation="woven" {...props} /></HostedBootstrapProvider>); });
}
const select = (label: 'Model' | 'Reasoning' | 'Interaction mode' | 'Permissions') => tree!.root.findByProps({ 'aria-label': label });
const optionValues = (label: 'Model' | 'Reasoning' | 'Interaction mode'): string[] => select(label).findAllByType('option').map(option => String(option.props.value));
async function choose(label: 'Model' | 'Reasoning' | 'Interaction mode', value: string) { await act(async () => { select(label).props.onChange({ target: { value } }); }); }
async function type(value: string) { await act(async () => { tree!.root.findByProps({ 'aria-label': 'Chat input' }).props.onChange({ target: { value } }); }); }
async function submit() { await act(async () => { tree!.root.findByType('form').props.onSubmit({ preventDefault: vi.fn() }); }); }
function rendered(): string { return JSON.stringify(tree!.toJSON()); }
function resumableProjection(sessionId: string, model?: string, reasoningEffort?: string): SelectedSessionReplayProjection {
  return { selectedSessionId: sessionId, sourceReference: `session:${sessionId}/events`, observedAt: '2026-09-10T00:00:00.000Z', disclosure: 'EMPTY', currency: 'CURRENT',
    transcript: { sessionId, itemCount: 0, items: [] }, instructionHistory: [], instructionBases: [], malformedLineCount: 0, sourceEventCount: 0, renderedItemCount: 0, diagnostics: [],
    session: { projectionId: `operator-session:${sessionId}`, sourceReference: `session:${sessionId}`, sessionId, observedAt: '2026-09-10T00:00:00.000Z', currency: 'CURRENT', runtimeStatus: 'idle', parentage: { state: 'NOT_RECORDED' }, diagnostics: [],
      ...(model ? { model } : {}), ...(reasoningEffort ? { reasoningEffort } : {}),
      continuation: { schemaVersion: 'chirality.session/v3', projectRoot: '/chosen/subfolder', roleId: 'WORKING_ITEMS', mode: 'CHAT', interactionMode: 'chat', permissionMode: 'workspaceWrite', selectedMethods: [], methodSelectionRevision: 1, instructionBasisId: `basis-${sessionId}` } }
  };
}
function bootedRecord(model: string, reasoningEffort?: string) {
  return { session: { schemaVersion: 'chirality.session/v3', sessionId: 'bound', projectRoot: '/chosen/subfolder', engineSelection: { adapterId: 'codex-app-server', providerId: 'openai', model }, ...(reasoningEffort ? { reasoningEffort } : {}),
    selectedMethods: [], methodSelectionRevision: 0, instructionBasisId: 'basis-1' } };
}

beforeEach(() => {
  vi.clearAllMocks(); state.root = '/chosen/subfolder'; state.query = 'agent=WORKING_ITEMS'; state.listeners.clear();
  values = new Map();
  vi.stubGlobal('window', { confirm: vi.fn(() => true), requestAnimationFrame: (callback: () => void) => { callback(); return 1; }, setInterval: globalThis.setInterval, clearInterval: globalThis.clearInterval,
    localStorage: { getItem: (key: string) => values.get(key) ?? null, setItem: (key: string, value: string) => { values.set(key, value); }, removeItem: (key: string) => values.delete(key) },
    chirality: { folders: { registerRecent: vi.fn(async () => ({ ok: true })), pathForFile: vi.fn(() => ''), subscribeOpen: () => () => {} } } });
  state.create.mockResolvedValue({ sessionId: 'bound', engineSelection: { adapterId: 'codex-app-server', providerId: 'openai', model: 'gpt-default' }, reasoningEffort: 'high' });
  state.boot.mockResolvedValue(bootedRecord('gpt-default', 'high'));
  state.replay.mockRejectedValue(new Error('No replay fixture'));
  state.replaceMethods.mockResolvedValue({ schemaVersion: 'chirality.selected-methods/v3', sessionId: 'bound', revision: 1, methods: [], basisPreview: { id: 'basis-1' }, transition: { status: 'unchanged', successorAvailable: false } });
  state.resolveContext.mockResolvedValue({ schemaVersion: 'chirality.selected-context/v3', roleId: 'WORKING_ITEMS', methods: [], documents: [], dispositions: [], supplied: [], basisPreview: {}, compatibilityInputs: [], compatibilityMappings: [] });
  state.nativeCapability.mockResolvedValue({ schemaVersion: 'chirality.native-plan-capability/v3', status: 'unavailable', reason: 'fixture' });
  state.nativeRevisions.mockResolvedValue({ schemaVersion: 'chirality.native-plan-revisions/v3', status: 'unavailable', reason: 'fixture', revisions: [] });
  state.nativeClarifications.mockResolvedValue({ schemaVersion: 'chirality.native-plan-clarifications/v3', status: 'unavailable', reason: 'fixture', clarifications: [] });
  state.apply.mockImplementation(async () => true);
  state.stream.mockResolvedValue(undefined);
  state.turnState.mockResolvedValue({ active: false, lastSeq: 0 });
  state.attach.mockResolvedValue(undefined);
});
afterEach(() => { if (tree) act(() => tree!.unmount()); tree = undefined; vi.unstubAllGlobals(); });

it('disables both selectors with the sign-in title when no hosted status is available or the account is signed out', async () => {
  await mount();
  for (const label of ['Model', 'Reasoning'] as const) {
    expect(select(label).props.disabled).toBe(true);
    expect(select(label).props.title).toBe(SIGNED_OUT_TITLE);
    expect(select(label).props.value).toBe('');
    expect(optionValues(label)).toEqual(['']);
  }
  // Signed out, and signed in without a retained catalog, are both "no catalog",
  // but only the first is a sign-in problem and only it says so.
  await update(snapshot({ ceremony: 'ready-to-start', admission: 'unavailable' }));
  expect(select('Model').props.disabled).toBe(true); expect(select('Model').props.title).toBe(SIGNED_OUT_TITLE);
  await update(snapshot({ withCatalog: false }));
  expect(select('Model').props.disabled).toBe(true); expect(select('Reasoning').props.title).toBe('Codex reported no model catalog for this folder yet.');
  // A session created while signed out carries no modelSelection: nothing is invented.
  await type('hello'); await submit();
  expect(state.create).toHaveBeenCalledTimes(1);
  expect(state.create.mock.calls[0][0]).not.toHaveProperty('modelSelection');
});

it('populates options from the status catalog and defaults to the admitted selection', async () => {
  await mount(snapshot());
  expect(select('Model').props.disabled).toBe(false);
  expect(optionValues('Model')).toEqual(['gpt-default', 'gpt-alt']);
  expect(select('Model').props.value).toBe('gpt-default');
  expect(optionValues('Reasoning')).toEqual(['low', 'medium', 'high']);
  expect(select('Reasoning').props.value).toBe('high');
  // Explanations live in hover/focus help, not inline text.
  expect(select('Model').props.title).toContain('authenticated account catalog');
  expect(select('Reasoning').props.title).toContain('Separate from Plan Mode');
  const contextText = tree!.root.findByProps({ 'aria-label': 'Chat context' }).findAllByType('p').map(node => node.children.join(''));
  expect(contextText.some(text => text.includes('catalog') || text.includes('Reasoning effort'))).toBe(false);
  expect(select('Model').props.className).toBeUndefined();
  expect(select('Model').parent?.props.className).toBe('chat-mode-selector');
});

it('resets the reasoning effort to the chosen model default and persists the explicit pair with the draft', async () => {
  await mount(snapshot());
  await choose('Model', 'gpt-alt');
  expect(select('Model').props.value).toBe('gpt-alt');
  expect(select('Reasoning').props.value).toBe('medium');
  expect(optionValues('Reasoning')).toEqual(['medium', 'low']);
  await choose('Reasoning', 'low');
  expect(select('Reasoning').props.value).toBe('low');
  expect(JSON.parse(values.get(entryKey)!)).toMatchObject({ model: 'gpt-alt', reasoningEffort: 'low' });
  // An effort outside the model's list is ignored, never substituted.
  await choose('Reasoning', 'high');
  expect(select('Reasoning').props.value).toBe('low');
  await choose('Model', 'not-in-catalog');
  expect(select('Model').props.value).toBe('gpt-alt');
  // Changing back resets the effort to that model's default again.
  await choose('Model', 'gpt-default');
  expect(select('Reasoning').props.value).toBe('high');
});

it('drops a stored pair that is not in the current catalog and falls back to the admitted default', async () => {
  values.set(entryKey, JSON.stringify({ draft: 'stored prompt', attachments: [], methods: [], model: 'gone-model', reasoningEffort: 'low' }));
  await mount(snapshot());
  expect(tree!.root.findByProps({ 'aria-label': 'Chat input' }).props.value).toBe('stored prompt');
  expect(select('Model').props.value).toBe('gpt-default');
  expect(select('Reasoning').props.value).toBe('high');
  expect(JSON.parse(values.get(entryKey)!)).not.toHaveProperty('model');
  // A stored effort the model no longer supports is dropped with the pair.
  values.set(entryKey, JSON.stringify({ draft: 'stored prompt', attachments: [], methods: [], model: 'gpt-alt', reasoningEffort: 'high' }));
  await update(null); await update(snapshot());
  expect(select('Model').props.value).toBe('gpt-default');
});

it('creates the session with the displayed modelSelection, sends the pair per turn, and keeps both selectors open between turns', async () => {
  state.create.mockResolvedValue({ sessionId: 'bound', engineSelection: { adapterId: 'codex-app-server', providerId: 'openai', model: 'gpt-alt' }, reasoningEffort: 'low' });
  state.boot.mockResolvedValue(bootedRecord('gpt-alt', 'low'));
  await mount(snapshot());
  await choose('Model', 'gpt-alt'); await choose('Reasoning', 'low');
  await type('Use the alternate model'); await submit();
  expect(state.create).toHaveBeenCalledTimes(1);
  expect(state.create.mock.calls[0][0]).toMatchObject({ modelSelection: { model: 'gpt-alt', reasoningEffort: 'low' } });
  // Boot carries no model; the turn carries the pair as top-level per-turn fields, never inside opts.
  expect(state.boot.mock.calls[0][0]).toEqual({ sessionId: 'bound' });
  expect(state.stream.mock.calls[0][0]).toMatchObject({ model: 'gpt-alt', reasoningEffort: 'low' });
  expect(state.stream.mock.calls[0][0].opts).not.toHaveProperty('model');
  // Between turns the selectors stay open on the recorded pair (D-GOV-43: model is per turn).
  for (const label of ['Model', 'Reasoning'] as const) {
    expect(select(label).props.disabled).toBe(false);
  }
  expect(select('Model').props.value).toBe('gpt-alt'); expect(optionValues('Model')).toEqual(['gpt-default', 'gpt-alt']);
  expect(select('Reasoning').props.value).toBe('low'); expect(optionValues('Reasoning')).toEqual(['medium', 'low']);
  // A different choice is sent with the next turn of the same session.
  await choose('Model', 'gpt-default'); await choose('Reasoning', 'medium');
  await type('Now the default model'); await submit();
  expect(state.create).toHaveBeenCalledTimes(1);
  expect(state.stream.mock.calls[1][0]).toMatchObject({ sessionId: 'bound', model: 'gpt-default', reasoningEffort: 'medium' });
  // When the catalog changes under the session, only published pairs are offered.
  await update(reducedSnapshot());
  expect(select('Model').props.value).toBe('gpt-default'); expect(optionValues('Model')).toEqual(['gpt-default']);
  // The entry draft keeps the pair for the next new chat while the session key holds none.
  expect(JSON.parse(values.get(entryKey)!)).toMatchObject({ draft: '', model: 'gpt-alt', reasoningEffort: 'low' });
});

it('disables the selectors only while a turn is running', async () => {
  let finish!: () => void;
  state.stream.mockImplementation(() => new Promise<void>(resolve => { finish = resolve; }));
  await mount(snapshot());
  await type('hold the turn open'); await submit();
  for (const label of ['Model', 'Reasoning', 'Permissions'] as const) expect(select(label).props.disabled).toBe(true);
  await act(async () => { finish(); await Promise.resolve(); await Promise.resolve(); });
  await act(async () => { await Promise.resolve(); });
  for (const label of ['Model', 'Reasoning', 'Permissions'] as const) expect(select(label).props.disabled).toBe(false);
});

it('sends the admitted default when nothing was chosen and never sends a pair the runtime did not publish', async () => {
  await mount(snapshot());
  await type('Default choice'); await submit();
  expect(state.create.mock.calls[0][0]).toMatchObject({ modelSelection: { model: 'gpt-default', reasoningEffort: 'high' } });
});

it('keeps the Plan Mode interaction select independent of the model and reasoning controls', async () => {
  await mount();
  expect(optionValues('Interaction mode')).toEqual(['chat', 'native-plan']);
  expect(select('Interaction mode').props.disabled).toBe(false);
  expect(select('Interaction mode').props.value).toBe('chat');
  await update(snapshot());
  await choose('Model', 'gpt-alt');
  expect(select('Interaction mode').props.value).toBe('chat');
  expect(optionValues('Interaction mode')).toEqual(['chat', 'native-plan']);
  await choose('Interaction mode', 'native-plan');
  expect(select('Interaction mode').props.value).toBe('native-plan');
  expect(select('Model').props.value).toBe('gpt-alt'); expect(select('Reasoning').props.value).toBe('medium');
  // The permission selector is a fourth, independent control.
  expect(tree!.root.findAllByType('select').map(node => node.props['aria-label'])).toEqual(['Interaction mode', 'Permissions', 'Model', 'Reasoning']);
});

it('shows a resumed conversation\'s recorded model and reasoning as the open starting pair', async () => {
  await mount(snapshot(), { resumeConversation: { requestId: 1, projection: resumableProjection('resumed', 'gpt-alt', 'low') } });
  expect(select('Model').props.value).toBe('gpt-alt'); expect(select('Model').props.disabled).toBe(false);
  expect(select('Reasoning').props.value).toBe('low'); expect(select('Reasoning').props.disabled).toBe(false);
  // A record without the effort field has no recorded pair: the catalog default applies, nothing is invented.
  await update(snapshot(), { newChatRequest: 1 });
  await update(snapshot(), { newChatRequest: 1, resumeConversation: { requestId: 2, projection: resumableProjection('older', 'gpt-default') } });
  expect(select('Model').props.value).toBe('gpt-default');
  expect(select('Reasoning').props.value).toBe('high');
  // A recorded pair outside the current catalog is never offered.
  await update(snapshot(), { newChatRequest: 1 });
  await update(snapshot(), { newChatRequest: 1, resumeConversation: { requestId: 3, projection: resumableProjection('gone', 'gone-model', 'low') } });
  expect(select('Model').props.value).toBe('gpt-default');
});

it('maps MODEL_NOT_IN_CATALOG on session creation to the refresh-and-choose-again message and keeps the selectors open', async () => {
  // A stale renderer catalog snapshot: no chat exists yet, so "this chat used" would mislead.
  state.create.mockRejectedValue(new HarnessApiClientError(400, 'INVALID_REQUEST', "Model 'gpt-alt' is not in the authenticated Codex catalog", { reason: 'MODEL_NOT_IN_CATALOG', model: 'gpt-alt', available: ['gpt-default'] }));
  await mount(snapshot());
  await choose('Model', 'gpt-alt');
  await type('create me'); await submit();
  expect(rendered()).toContain('Model gpt-alt is no longer offered by your Codex account. Refresh your account status and choose again.');
  expect(rendered()).not.toContain('This chat used');
  expect(state.boot).not.toHaveBeenCalled(); expect(state.stream).not.toHaveBeenCalled();
  // No session was bound, so the operator can still choose again.
  expect(select('Model').props.disabled).toBe(false); expect(select('Reasoning').props.disabled).toBe(false);

  // A later failure of the same kind on an existing session is still the session message.
  state.create.mockResolvedValue({ sessionId: 'bound', engineSelection: { adapterId: 'codex-app-server', providerId: 'openai', model: 'gpt-alt' }, reasoningEffort: 'medium' });
  state.boot.mockRejectedValue(new HarnessApiClientError(503, 'ENGINE_UNAVAILABLE', "Model 'gpt-alt' is no longer offered by the authenticated Codex catalog", { reason: 'MODEL_NOT_IN_CATALOG', model: 'gpt-alt', available: ['gpt-default'] }));
  await type('boot me'); await submit();
  expect(rendered()).toContain('This chat used gpt-alt, which your Codex account no longer offers. Start a new chat.');
  expect(rendered()).not.toContain('Refresh your account status');
});

it('maps MODEL_NOT_IN_CATALOG on boot and on the turn stream to the start-a-new-chat message without rewriting anything', async () => {
  state.boot.mockRejectedValue(new HarnessApiClientError(503, 'ENGINE_UNAVAILABLE', "Model 'gpt-alt' is no longer offered by the authenticated Codex catalog", { reason: 'MODEL_NOT_IN_CATALOG', model: 'gpt-alt', available: ['gpt-default'] }));
  await mount(snapshot());
  await type('boot me'); await submit();
  expect(rendered()).toContain('This chat used gpt-alt, which your Codex account no longer offers. Start a new chat.');
  expect(state.stream).not.toHaveBeenCalled();

  // Turn stream: Runtime forwards only runtimeCode and reason; the panel names the session's own model.
  state.boot.mockResolvedValue(bootedRecord('gpt-alt', 'low'));
  state.stream.mockImplementation(async (_request: unknown, onEvent: (event: { event: string; data: unknown }) => void) => {
    onEvent({ event: 'turn:error', data: { phase: 'mid-stream', errorType: 'SDK_FAILURE', message: 'Model is no longer offered', status: 503, severity: 'error', fatal: true, details: { runtimeCode: 'ENGINE_UNAVAILABLE', reason: 'MODEL_NOT_IN_CATALOG' } } });
  });
  await update(snapshot(), { newChatRequest: 1 });
  await type('turn me'); await submit();
  expect(rendered()).toContain('This chat used gpt-alt, which your Codex account no longer offers. Start a new chat.');
  expect(select('Model').props.value).toBe('gpt-alt'); expect(select('Model').props.disabled).toBe(false);
});

it('re-reads hosted status after a fatal engine failure so a fenced account stops reading as ready', async () => {
  state.boot.mockResolvedValue(bootedRecord('gpt-default', 'high'));
  const refresh = vi.fn();
  state.stream.mockImplementation(async (_request: unknown, onEvent: (event: { event: string; data: unknown }) => void) => {
    onEvent({ event: 'turn:error', data: { phase: 'mid-stream', errorType: 'ENGINE_UNAVAILABLE', message: 'Codex request timed out', status: 503, severity: 'error', fatal: true, details: { reason: 'CODEX_PROTOCOL_FAILURE' } } });
  });
  await act(async () => { tree = create(<HostedBootstrapProvider snapshot={snapshot()} loading={false} refresh={refresh}><ChatPanel presentation="woven" /></HostedBootstrapProvider>); });
  await type('turn me'); await submit();
  expect(refresh).toHaveBeenCalledTimes(1);
  expect(rendered()).toContain('Codex request timed out');
});


it('keeps a valid chosen model and reasoning when switching the new chat role', async () => {
  await mount(snapshot());
  await choose('Model', 'gpt-alt'); await choose('Reasoning', 'low');
  state.query = 'agent=HELPS_HUMANS';
  await update(snapshot());
  expect(select('Model').props.value).toBe('gpt-alt');
  expect(select('Reasoning').props.value).toBe('low');
  await update(reducedSnapshot());
  expect(select('Model').props.value).toBe('gpt-default');
});

// Item 14: while a folder is being switched or cannot be bound, the account's
// last reported catalog keeps the selectors usable, and a disabled selector
// names the folder problem rather than demanding sign-in.
it('keeps the account catalog while the selected folder is in conflict and names a folder problem in the disabled title', async () => {
  const registered = snapshot();
  if (registered.registration !== 'registered') throw new Error('fixture');
  const account = registered.status;
  await act(async () => {
    tree = create(<HostedBootstrapProvider snapshot={null} loading={false} account={account} project={{ state: 'conflict', message: 'bound elsewhere' }}><ChatPanel presentation="woven" /></HostedBootstrapProvider>);
  });
  expect(select('Model').props.disabled).toBe(false);
  expect(optionValues('Model')).toEqual(['gpt-default', 'gpt-alt']);

  await act(async () => {
    tree!.update(<HostedBootstrapProvider snapshot={null} loading={false} account={{ ...account, admission: 'establishing', models: undefined, selection: undefined }} project={{ state: 'conflict', message: 'bound elsewhere' }}><ChatPanel presentation="woven" /></HostedBootstrapProvider>);
  });
  expect(select('Model').props.disabled).toBe(true);
  expect(select('Model').props.title).toBe('This folder is not available to Codex yet. Set it up from the account menu to choose a model.');

  await act(async () => {
    tree!.update(<HostedBootstrapProvider snapshot={null} loading={true} account={{ ...account, admission: 'establishing', models: undefined, selection: undefined }} project={{ state: 'checking', message: null }}><ChatPanel presentation="woven" /></HostedBootstrapProvider>);
  });
  expect(select('Model').props.title).toBe('Checking this folder. Models load once it is ready.');

  await act(async () => {
    tree!.update(<HostedBootstrapProvider snapshot={null} loading={false} account={{ ...account, ceremony: 'ready-to-start', admission: 'unavailable', models: undefined, selection: undefined }} project={{ state: 'conflict', message: 'bound elsewhere' }}><ChatPanel presentation="woven" /></HostedBootstrapProvider>);
  });
  expect(select('Model').props.title).toBe(SIGNED_OUT_TITLE);
});
