import React, { useSyncExternalStore } from 'react';
import { act, create, type ReactTestRenderer } from 'react-test-renderer';
import { beforeEach, afterEach, expect, it, vi } from 'vitest';
import { buildChatDraftStorageKey } from '../../lib/harness/chat-draft';
import type { QualifiedMethodReference } from '../../lib/harness/method-selection-client';
import type { SelectedSessionReplayProjection } from '../../lib/woven-dialogue/contracts';

const state = vi.hoisted(() => ({ root: '/chosen/subfolder', query: '', listeners: new Set<() => void>(),
  create: vi.fn(), boot: vi.fn(), getSession: vi.fn(), replay: vi.fn(), stream: vi.fn(), apply: vi.fn(), append: vi.fn(), clear: vi.fn(), hydrate: vi.fn(), streaming: vi.fn(),
  replaceMethods: vi.fn(), resolveContext: vi.fn(),
  nativeCapability: vi.fn(), nativeRevisions: vi.fn(), nativeClarifications: vi.fn(), replyClarification: vi.fn(), listRequests: vi.fn(), answerRequest: vi.fn(), exportPlan: vi.fn(),
  markdownProps: [] as Array<{ source: string; projectRoot?: string | null; fileCatalog?: readonly string[]; onOpenFile?: (path: string) => void }>,
  nativeListener: undefined as ((intent: { path?: string; error?: string }) => void) | undefined
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
vi.mock('../../components/shell/file-picker', () => ({ FilePicker: ({ onAddAttachments }: { onAddAttachments: (items: Array<{ path: string; displayName: string; clientType: 'text' }>) => void }) => <button data-add-attachment onClick={() => onAddAttachments([{ path: '/chosen/subfolder/docs/input.txt', displayName: 'input.txt', clientType: 'text' }])}>add fixture attachment</button> }));
vi.mock('../../components/shell/permission-requests', () => ({ PermissionRequests: () => null }));
vi.mock('../../components/shell/chat-markdown', () => ({ ChatMarkdown: (props: { source: string; projectRoot?: string | null; fileCatalog?: readonly string[]; onOpenFile?: (path: string) => void }) => { state.markdownProps.push(props); return <p>{props.source}</p>; } }));
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
vi.mock('../../lib/harness/client', async importOriginal => ({ ...await importOriginal<typeof import('../../lib/harness/client')>(), createHarnessSession: state.create, bootHarnessSession: state.boot, getHarnessSession: state.getSession, replaySessionEvents: state.replay, streamHarnessTurn: state.stream, interruptHarnessSession: vi.fn(), listHarnessSessionRequests: state.listRequests, answerHarnessSessionRequest: state.answerRequest, getHarnessTurnState: vi.fn(async () => ({ active: false, lastSeq: 0 })), attachHarnessTurn: vi.fn(async () => undefined) }));
import { ChatPanel } from '../../components/shell/chat-panel';
import { HarnessApiClientError } from '../../lib/harness/client';

let tree: ReactTestRenderer | undefined;
let values: Map<string, string>;
let writes: [string, string][];
const canonicalKey = buildChatDraftStorageKey('/canonical', 'WORKING_ITEMS', 'CHAT');
const canonicalDraft = JSON.stringify({ draft: 'Unrelated canonical draft', attachments: [] });
function root(value: string) { state.root = value; for (const listener of state.listeners) listener(); }
function deferred<T>() {
  let resolve!: (value: T) => void;
  let reject!: (reason?: unknown) => void;
  const promise = new Promise<T>((done, fail) => { resolve = done; reject = fail; });
  return { promise, resolve, reject };
}
async function mount(props: Partial<React.ComponentProps<typeof ChatPanel>> = {}) { await act(async () => { tree = create(<ChatPanel presentation="woven" {...props} />); }); }
async function type(value: string) { await act(async () => { tree!.root.findByProps({ 'aria-label': 'Chat input' }).props.onChange({ target: { value } }); }); }
async function submit() { await act(async () => { tree!.root.findByType('form').props.onSubmit({ preventDefault: vi.fn() }); }); }
function continueWithProjectAccess() { return tree!.root.findAllByType('button').find(node => node.children.join('') === 'Continue with Write in workspace'); }
function assertCanonicalUntouched() { expect(values.get(canonicalKey)).toBe(canonicalDraft); expect(writes.filter(([key]) => key === canonicalKey)).toEqual([]); }
function resumableProjection(sessionId: string): SelectedSessionReplayProjection {
  return { selectedSessionId: sessionId, sourceReference: `session:${sessionId}/events`, observedAt: '2026-09-09T00:00:00.000Z', disclosure: 'EMPTY', currency: 'CURRENT',
    transcript: { sessionId, itemCount: 0, items: [] }, instructionHistory: [], instructionBases: [], malformedLineCount: 0, sourceEventCount: 0, renderedItemCount: 0, diagnostics: [],
    session: { projectionId: `operator-session:${sessionId}`, sourceReference: `session:${sessionId}`, sessionId, observedAt: '2026-09-09T00:00:00.000Z', currency: 'CURRENT', runtimeStatus: 'idle', parentage: { state: 'NOT_RECORDED' }, diagnostics: [],
      continuation: { schemaVersion: 'chirality.session/v3', projectRoot: '/chosen/subfolder', roleId: 'WORKING_ITEMS', mode: 'CHAT', interactionMode: 'chat', permissionMode: (sessionId === 'legacy-permissions' ? 'dontAsk' : 'ask') as 'ask', selectedMethods: [], methodSelectionRevision: 1, instructionBasisId: `basis-${sessionId}` } }
  };
}
beforeEach(() => {
  vi.clearAllMocks(); state.root = '/chosen/subfolder'; state.query = 'agent=WORKING_ITEMS'; state.listeners.clear(); state.nativeListener = undefined;
  state.markdownProps = [];
  values = new Map([[canonicalKey, canonicalDraft]]); writes = [];
  vi.stubGlobal('window', { confirm: vi.fn(() => true), prompt: vi.fn(() => 'plans/fixture.md'), requestAnimationFrame: (callback: () => void) => { callback(); return 1; }, setInterval: globalThis.setInterval, clearInterval: globalThis.clearInterval, localStorage: { getItem: (key: string) => values.get(key) ?? null, setItem: (key: string, value: string) => { writes.push([key, value]); values.set(key, value); }, removeItem: (key: string) => values.delete(key) }, chirality: { folders: {
    registerRecent: vi.fn(async () => ({ ok: true })), pathForFile: vi.fn(() => ''), subscribeOpen: (listener: typeof state.nativeListener) => { state.nativeListener = listener; return () => { state.nativeListener = undefined; }; }
  } } });
  state.listRequests.mockResolvedValue({ requests: [] });
  state.answerRequest.mockResolvedValue({ sent: true });
  state.create.mockResolvedValue({ sessionId: 'bound' });
  state.boot.mockResolvedValue({ session: { sessionId: 'bound', projectRoot: '/canonical' } });
  state.replay.mockRejectedValue(new Error('No replay fixture'));
  state.getSession.mockImplementation(async () => {
    const replay = await Promise.resolve(state.replay.mock.results.at(-1)?.value).catch(() => undefined);
    const session = replay?.session ?? (await state.boot.mock.results.at(-1)?.value).session;
    return { schemaVersion: 'chirality.session/v3', selectedMethods: [], methodSelectionRevision: 0, instructionBasisId: 'basis-initial', ...session };
  });
  state.replaceMethods.mockImplementation(async (_sessionId: string, methods: QualifiedMethodReference[] | undefined) => ({ schemaVersion: 'chirality.selected-methods/v3', sessionId: 'bound', revision: 1, methods: methods ?? [], basisPreview: { id: 'basis-1' }, transition: { status: 'unchanged', successorAvailable: false } }));
  state.resolveContext.mockResolvedValue({ schemaVersion: 'chirality.selected-context/v3', roleId: 'HELP_HUMAN', methods: [], documents: [], dispositions: [], supplied: [], basisPreview: {}, compatibilityInputs: [], compatibilityMappings: [] });
  state.nativeCapability.mockResolvedValue({ schemaVersion: 'chirality.native-plan-capability/v3', status: 'unavailable', reason: 'fixture' });
  state.nativeRevisions.mockResolvedValue({ schemaVersion: 'chirality.native-plan-revisions/v3', status: 'unavailable', reason: 'fixture', revisions: [] });
  state.nativeClarifications.mockResolvedValue({ schemaVersion: 'chirality.native-plan-clarifications/v3', status: 'unavailable', reason: 'fixture', clarifications: [] });
  state.replyClarification.mockResolvedValue({ schemaVersion: 'chirality.native-plan-clarification-reply/v3', sessionId: 'bound', requestId: 7, sent: true });
  state.exportPlan.mockResolvedValue({ schemaVersion: 'chirality.native-plan-export/v3', sessionId: 'bound', revision: 1, targetRelativePath: 'plans/fixture.md', sha256: 'a'.repeat(64) });
  state.apply.mockImplementation(async (value: string) => { root(value); return true; });
  // A known HTTP rejection before turn acceptance, rather than a lost response.
  state.stream.mockRejectedValue(new HarnessApiClientError(400, 'INVALID_REQUEST', 'Fixture turn failure'));
});
afterEach(() => { if (tree) act(() => tree!.unmount()); tree = undefined; vi.unstubAllGlobals(); });

it('uses the returned canonical root without migrating or overwriting either conversation draft', async () => {
  const pending = deferred<boolean>(); state.stream.mockImplementation(() => pending.promise);
  await mount(); await type('Keep my failed prompt'); await submit();
  expect(state.root).toBe('/canonical'); assertCanonicalUntouched();
  expect(tree!.root.findByProps({ className: 'chat-folder-fixed' }).props.title).toBe('/canonical');
  await act(async () => pending.resolve(false));
  await type('Second prompt'); state.stream.mockRejectedValue(new HarnessApiClientError(400, 'INVALID_REQUEST', 'Failed again')); await submit();
  expect(state.create).toHaveBeenCalledTimes(1); expect(state.boot).toHaveBeenCalledTimes(1);
  expect(tree!.root.findByProps({ 'aria-label': 'Chat input' }).props.value).toBe('Second prompt');
  assertCanonicalUntouched();
});
it('retains the actual binding and failed draft when provider synchronization refuses', async () => {
  state.apply.mockResolvedValue(false); const binding = vi.fn();
  await mount({ onBindingChange: binding }); await type('Keep this prompt'); await submit();
  expect(state.root).toBe('/chosen/subfolder'); expect(binding).toHaveBeenLastCalledWith({ root: '/canonical', locked: true });
  expect(tree!.root.findByProps({ 'aria-label': 'Chat input' }).props.value).toBe('Keep this prompt');
  expect(JSON.stringify(tree!.toJSON())).toContain('file browsing could not switch'); assertCanonicalUntouched();
});
it('rejects a stale boot result after an unrelated folder change without restoring its old draft', async () => {
  const boot = deferred<unknown>(); state.boot.mockReturnValue(boot.promise);
  await mount(); await type('Old context prompt'); await submit();
  await act(async () => root('/other'));
  await act(async () => boot.resolve({ session: { sessionId: 'old', projectRoot: '/canonical' } }));
  expect(state.apply).not.toHaveBeenCalled(); expect(state.stream).not.toHaveBeenCalled();
  expect(tree!.root.findByProps({ 'aria-label': 'Chat input' }).props.value).not.toBe('Old context prompt'); assertCanonicalUntouched();
});
it('rejects a stale synchronization completion after a different folder transition', async () => {
  const applied = deferred<boolean>(); state.apply.mockReturnValue(applied.promise);
  await mount(); await type('Old context prompt'); await submit();
  await act(async () => root('/other'));
  await act(async () => applied.resolve(false));
  expect(state.stream).not.toHaveBeenCalled();
  expect(tree!.root.findByProps({ 'aria-label': 'Chat input' }).props.value).not.toBe('Old context prompt'); assertCanonicalUntouched();
});
it('reports whether a New chat request went ahead, keeping the draft when the confirmation is declined', async () => {
  const settled = vi.fn();
  await mount({ onNewChatSettled: settled }); await type('Unsent words');
  (window.confirm as ReturnType<typeof vi.fn>).mockReturnValueOnce(false);
  await act(async () => tree!.update(<ChatPanel presentation="woven" onNewChatSettled={settled} newChatRequest={1} />));
  expect(settled).toHaveBeenLastCalledWith(false);
  expect(tree!.root.findByProps({ 'aria-label': 'Chat input' }).props.value).toBe('Unsent words');
  await act(async () => tree!.update(<ChatPanel presentation="woven" onNewChatSettled={settled} newChatRequest={2} />));
  expect(settled).toHaveBeenLastCalledWith(true);
  expect(tree!.root.findByProps({ 'aria-label': 'Chat input' }).props.value).toBe('');
});

it('blocks native folder intent while bound or pending and blocks Send during pending selection', async () => {
  await mount({ folderSelectionPending: true }); await type('Pending'); await submit();
  expect(state.create).not.toHaveBeenCalled();
  await act(async () => state.nativeListener?.({ path: '/native-folder' })); expect(state.apply).not.toHaveBeenCalled();
  await act(async () => tree!.update(<ChatPanel presentation="woven" folderSelectionPending={false} />));
  await submit(); const calls = state.apply.mock.calls.length;
  await act(async () => state.nativeListener?.({ path: '/native-folder' })); expect(state.apply).toHaveBeenCalledTimes(calls);
});
it('keeps Enter submission distinct from Shift+Enter and IME composition', async () => {
  await mount(); const submit = vi.fn(); const preventDefault = vi.fn(); const handler = tree!.root.findByType('textarea').props.onKeyDown;
  handler({ key: 'Enter', shiftKey: true, nativeEvent: { isComposing: false }, preventDefault, currentTarget: { form: { requestSubmit: submit } } });
  handler({ key: 'Enter', shiftKey: false, nativeEvent: { isComposing: true }, preventDefault, currentTarget: { form: { requestSubmit: submit } } });
  expect(submit).not.toHaveBeenCalled();
  handler({ key: 'Enter', shiftKey: false, nativeEvent: { isComposing: false }, preventDefault, currentTarget: { form: { requestSubmit: submit } } });
  expect(submit).toHaveBeenCalledTimes(1); expect(preventDefault).toHaveBeenCalledTimes(1);
});

it('captures only the first prompt after a session boots successfully', async () => {
  state.stream.mockResolvedValue(undefined);
  const captured = vi.fn();
  await mount({ onSessionBootedPrompt: captured });
  await type('First prompt'); await submit();
  expect(captured).toHaveBeenCalledWith({ sessionId: 'bound', prompt: 'First prompt', persona: 'WORKING_ITEMS' });
  await type('Second prompt'); await submit();
  expect(captured).toHaveBeenCalledTimes(1);
  expect(state.create).toHaveBeenCalledTimes(1);
  expect(state.boot).toHaveBeenCalledTimes(1);
});

it('merges next-message methods into the active basis without sending turn-time overrides', async () => {
  const method = { kind: 'workflow' as const, name: 'project-setup', source: 'bundled' as const, sourceRootId: 'chirality-root' };
  values.set(buildChatDraftStorageKey('/chosen/subfolder', 'WORKING_ITEMS', 'CHAT'), JSON.stringify({ draft: '', attachments: [], methods: [method] }));
  state.stream.mockResolvedValue(undefined);
  state.nativeCapability.mockResolvedValue({ schemaVersion: 'chirality.native-plan-capability/v3', status: 'qualified', qualification: { adapterId: 'fixture', providerId: 'fixture', qualificationId: 'qualified-fixture', admissionSha256: 'a'.repeat(64), evidenceClass: 'native-adapter-qualified' } });
  function Fixture() {
    const [methods, setMethods] = React.useState<QualifiedMethodReference[]>([method]);
    return <ChatPanel presentation="woven" selectedMethods={methods} onSelectedMethodsChange={setMethods} />;
  }
  await act(async () => { tree = create(<Fixture />); });
  await type('First selected message'); await submit();
  expect(state.stream).toHaveBeenLastCalledWith(expect.objectContaining({ interactionMode: 'chat', permissionMode: 'workspaceWrite' }), expect.any(Function), expect.any(AbortSignal));
  expect(state.stream.mock.calls.at(-1)?.[0]).not.toHaveProperty('methods');
  expect(state.replaceMethods).toHaveBeenLastCalledWith('bound', [method], { boundaryConfirmed: true, selectionMode: 'merge', expectedRevision: 0, expectedBasisId: 'basis-initial' });
  expect(tree!.root.findAllByProps({ 'aria-label': 'Methods for next turn' })).toHaveLength(0);

  await act(async () => tree!.root.findByProps({ 'aria-label': 'Interaction mode' }).props.onChange({ target: { value: 'native-plan' } }));
  await type('Second message'); await submit();
  expect(state.stream).toHaveBeenLastCalledWith(expect.objectContaining({ interactionMode: 'native-plan', permissionMode: 'workspaceWrite' }), expect.any(Function), expect.any(AbortSignal));
  expect(state.stream.mock.calls.at(-1)?.[0]).not.toHaveProperty('methods');
  expect(state.replaceMethods).toHaveBeenCalledTimes(1);
});

it('starts Plan Mode in a new Codex chat and keeps inspect, revise, save, and execute in the conversation', async () => {
  const qualification = { adapterId: 'codex-app-server', providerId: 'openai', qualificationId: 'fixture', admissionSha256: 'a'.repeat(64), evidenceClass: 'native-adapter-qualified' as const };
  const revision = { revision: 2, sourceEvent: { qualificationState: 'qualified' as const, eventId: 'plan-2', occurredAt: '2026-09-09T00:00:00.000Z', qualification, plan: { id: 'native-item', type: 'plan', text: '# Approved plan\n\nKeep the exact scope.' } } };
  state.boot.mockResolvedValue({ session: { schemaVersion: 'chirality.session/v3', sessionId: 'bound', projectRoot: '/chosen/subfolder', selectedMethods: [], methodSelectionRevision: 0, instructionBasisId: 'basis-1' } });
  state.nativeCapability.mockResolvedValue({ schemaVersion: 'chirality.native-plan-capability/v3', status: 'qualified', qualification });
  state.nativeRevisions.mockResolvedValue({ schemaVersion: 'chirality.native-plan-revisions/v3', status: 'qualified', qualification, revisions: [revision] });
  state.stream.mockResolvedValue(undefined);
  await mount();
  const mode = tree!.root.findByProps({ 'aria-label': 'Interaction mode' });
  expect(mode.findByProps({ value: 'native-plan' }).props.disabled).toBe(false);
  await act(async () => mode.props.onChange({ target: { value: 'native-plan' } }));
  await type('Plan this change'); await submit();
  await act(async () => { await Promise.resolve(); });
  expect(JSON.stringify(tree!.toJSON())).toContain('Current plan');
  expect(JSON.stringify(tree!.toJSON())).toContain('Approved plan');

  const refreshCalls = state.nativeRevisions.mock.calls.length;
  await act(async () => tree!.root.findAllByType('button').find(button => button.children.includes('Refresh'))!.props.onClick());
  expect(state.nativeRevisions.mock.calls.length).toBeGreaterThan(refreshCalls);

  await act(async () => tree!.root.findAllByType('button').find(button => button.children.includes('Revise in chat'))!.props.onClick());
  expect(tree!.root.findByProps({ 'aria-label': 'Interaction mode' }).props.value).toBe('native-plan');
  expect(tree!.root.findByProps({ 'aria-label': 'Chat input' }).props.value).toContain('Revise plan revision 2');

  await act(async () => tree!.root.findAllByType('button').find(button => button.children.includes('Execute plan'))!.props.onClick());
  expect(tree!.root.findByProps({ 'aria-label': 'Interaction mode' }).props.value).toBe('chat');
  expect(tree!.root.findByProps({ 'aria-label': 'Chat input' }).props.value).toContain('Execute the accepted native Plan Mode revision 2');
  expect(tree!.root.findByProps({ 'aria-label': 'Chat input' }).props.value).toContain('# Approved plan');

  await act(async () => tree!.root.findAllByType('button').find(button => button.children.includes('Turn into workflow'))!.props.onClick());
  const saveDraft = tree!.root.findByProps({ 'aria-label': 'Chat input' }).props.value;
  expect(tree!.root.findByProps({ 'aria-label': 'Interaction mode' }).props.value).toBe('chat');
  expect(saveDraft).toContain('.chirality/workflow-drafts/<suitable-name>/WORKFLOW.md');
  expect(saveDraft).toContain('# Approved plan');
  expect(saveDraft).not.toContain('native-item');
  expect(JSON.stringify(tree!.toJSON())).not.toContain('No assistant text was returned');
  const chooseExportTarget = vi.fn().mockResolvedValue({ cancelled: true });
  const confirmOverwrite = vi.fn().mockResolvedValue(false);
  window.chirality!.plans = { chooseExportTarget, confirmOverwrite };
  const save = () => tree!.root.findAllByType('button').find(button => button.children.includes('Save plan…'))!.props.onClick();
  await act(async () => { await save(); });
  expect(state.exportPlan).not.toHaveBeenCalled();
  chooseExportTarget.mockResolvedValue({ cancelled: false, targetRelativePath: 'plans/native.md' });
  const { MethodSelectionClientError } = await import('../../lib/harness/method-selection-client');
  state.exportPlan.mockRejectedValueOnce(new MethodSelectionClientError(409, 'exists'));
  await act(async () => { await save(); });
  expect(confirmOverwrite).toHaveBeenCalled();
  expect(state.exportPlan).toHaveBeenCalledTimes(1);
  confirmOverwrite.mockResolvedValue(true);
  state.exportPlan.mockRejectedValueOnce(new MethodSelectionClientError(409, 'exists'));
  await act(async () => { await save(); });
  expect(state.exportPlan).toHaveBeenLastCalledWith({ sessionId: 'bound', revision: 2, targetRelativePath: 'plans/native.md', overwrite: true });
});

it('enables genuine Plan controls for a trial admission and labels its empirical status', async () => {
  const admission = { adapterId: 'codex-app-server', providerId: 'openai', dispositionId: 'human-trial', admissionSha256: 'b'.repeat(64), evidenceClass: 'native-adapter-local-human-trial' as const };
  const revision = { revision: 1, sourceEvent: { qualificationState: 'trial' as const, eventId: 'trial-plan-1', occurredAt: '2026-09-10T00:00:00.000Z', admission, plan: '# Trial plan\n\nInspect before execution.' } };
  state.boot.mockResolvedValue({ session: { schemaVersion: 'chirality.session/v3', sessionId: 'bound', projectRoot: '/chosen/subfolder', selectedMethods: [], methodSelectionRevision: 0, instructionBasisId: 'basis-1' } });
  state.nativeCapability.mockResolvedValue({ schemaVersion: 'chirality.native-plan-capability/v3', status: 'trial', admission });
  state.nativeRevisions.mockResolvedValue({ schemaVersion: 'chirality.native-plan-revisions/v3', status: 'trial', admission, revisions: [revision] });
  state.stream.mockResolvedValue(undefined);
  await mount();
  const mode = tree!.root.findByProps({ 'aria-label': 'Interaction mode' });
  await act(async () => mode.props.onChange({ target: { value: 'native-plan' } }));
  await type('Trial this plan');
  await submit();
  await act(async () => { await Promise.resolve(); await Promise.resolve(); });
  expect(tree!.root.findByProps({ 'aria-label': 'Interaction mode' }).findByProps({ value: 'native-plan' }).props.disabled).toBe(false);
  expect(JSON.stringify(tree!.toJSON())).not.toContain('Human trial');
  expect(JSON.stringify(tree!.toJSON())).toContain('Trial plan');
  expect(tree!.root.findAllByType('button').find(button => button.children.includes('Execute plan'))!.props.disabled).toBe(false);
});

it('answers every native clarification by question id, uses the native session request id, and retains masked input after failure', async () => {
  const qualification = { adapterId: 'codex-app-server', providerId: 'openai', qualificationId: 'fixture', admissionSha256: 'a'.repeat(64), evidenceClass: 'native-adapter-qualified' as const };
  const clarification = { clientTurnId: 'turn-1', providerThreadId: 'thread-1', providerTurnId: 'provider-turn-1', requestId: 7, itemId: 'item-7', isBlocking: true, autoResolutionMs: null,
    questions: [
      { id: 'scope', header: 'Scope', question: 'Which scope?', options: [{ label: 'Current project', description: 'Use this folder.' }], isOther: false, isSecret: false },
      { id: 'token', header: 'Private value', question: 'Enter private value.', options: [], isOther: true, isSecret: true }
    ] };
  state.boot.mockResolvedValue({ session: { schemaVersion: 'chirality.session/v3', sessionId: 'bound', projectRoot: '/chosen/subfolder', selectedMethods: [], methodSelectionRevision: 0, instructionBasisId: 'basis-1' } });
  state.nativeCapability.mockResolvedValue({ schemaVersion: 'chirality.native-plan-capability/v3', status: 'qualified', qualification });
  state.nativeClarifications.mockResolvedValue({ schemaVersion: 'chirality.native-plan-clarifications/v3', status: 'qualified', qualification, clarifications: [clarification] });
  state.listRequests.mockResolvedValue({ requests: [{ requestId: '7', method: 'item/tool/requestUserInput', params: clarification, receivedAt: '2026-09-12T00:00:00Z' }] });
  const running = deferred<void>(); state.stream.mockReturnValue(running.promise);
  await mount();
  await act(async () => tree!.root.findByProps({ 'aria-label': 'Interaction mode' }).props.onChange({ target: { value: 'native-plan' } }));
  await type('Start planning'); await submit();
  await act(async () => { await Promise.resolve(); await Promise.resolve(); });
  const form = tree!.root.findByProps({ className: 'native-plan-clarification' });
  const scope = form.findByProps({ value: 'Current project' });
  const secret = form.findByProps({ type: 'password' });
  expect(scope.props.disabled).toBe(false);
  expect(secret.props.disabled).toBe(false);
  await act(async () => scope.props.onChange());
  await act(async () => secret.props.onChange({ target: { value: 'do-not-render' } }));
  const transcriptText = tree!.root.findByProps({ className: 'panel-body chat-transcript' }).findAllByType('p').flatMap(node => node.children).join(' ');
  expect(transcriptText).not.toContain('do-not-render');

  state.answerRequest.mockRejectedValueOnce(new Error('Reply transport failed'));
  await act(async () => { form.props.onSubmit({ preventDefault: vi.fn() }); await Promise.resolve(); });
  expect(state.answerRequest).toHaveBeenCalledWith({ sessionId: 'bound', requestId: '7', answer: { kind: 'userInput', answers: {
    scope: { answers: ['Current project'] }, token: { answers: ['do-not-render'] }
  } } });
  expect(JSON.stringify(tree!.toJSON())).toContain('Reply transport failed');
  expect(tree!.root.findByProps({ type: 'password' }).props.value).toBe('do-not-render');
  state.answerRequest.mockImplementationOnce(async () => {
    running.resolve();
    return { schemaVersion: 'chirality.native-plan-clarification-reply/v3', sessionId: 'bound', requestId: 7, sent: true };
  });
  await act(async () => { form.props.onSubmit({ preventDefault: vi.fn() }); await Promise.resolve(); await Promise.resolve(); });
  expect(state.answerRequest).toHaveBeenCalledTimes(2);
  expect(tree!.root.findByProps({ 'aria-label': 'Send' }).props.disabled).toBe(true);
});

it('clears native plan actions while a different resumed chat is still loading its plan', async () => {
  const qualification = { adapterId: 'codex-app-server', providerId: 'openai', qualificationId: 'fixture', admissionSha256: 'a'.repeat(64), evidenceClass: 'native-adapter-qualified' as const };
  const capability = { schemaVersion: 'chirality.native-plan-capability/v3' as const, status: 'qualified' as const, qualification };
  const revisionA = { revision: 1, sourceEvent: { qualificationState: 'qualified' as const, eventId: 'plan-a', occurredAt: '2026-09-09T00:00:00.000Z', qualification, plan: '# Plan A\n\nOnly for session A.' } };
  const revisionB = { revision: 2, sourceEvent: { qualificationState: 'qualified' as const, eventId: 'plan-b', occurredAt: '2026-09-09T00:00:01.000Z', qualification, plan: '# Plan B\n\nOnly for session B.' } };
  const capabilityB = deferred<typeof capability>();
  const revisionsB = deferred<{ schemaVersion: 'chirality.native-plan-revisions/v3'; status: 'qualified'; qualification: typeof qualification; revisions: typeof revisionB[] }>();
  const clarificationsB = deferred<{ schemaVersion: 'chirality.native-plan-clarifications/v3'; status: 'qualified'; qualification: typeof qualification; clarifications: [] }>();
  state.nativeCapability.mockImplementation((sessionId: string) => sessionId === 'session-a' ? Promise.resolve(capability) : capabilityB.promise);
  state.nativeRevisions.mockImplementation((sessionId: string) => sessionId === 'session-a'
    ? Promise.resolve({ schemaVersion: 'chirality.native-plan-revisions/v3', status: 'qualified', qualification, revisions: [revisionA] })
    : revisionsB.promise);
  state.nativeClarifications.mockImplementation((sessionId: string) => sessionId === 'session-a'
    ? Promise.resolve({ schemaVersion: 'chirality.native-plan-clarifications/v3', status: 'qualified', qualification, clarifications: [] })
    : clarificationsB.promise);
  const projectionA = resumableProjection('session-a');
  projectionA.session!.continuation!.interactionMode = 'native-plan';
  const projectionB = resumableProjection('session-b');
  projectionB.session!.continuation!.interactionMode = 'native-plan';

  await mount({ resumeConversation: { requestId: 1, projection: projectionA } });
  await act(async () => { await Promise.resolve(); await Promise.resolve(); });
  expect(JSON.stringify(tree!.toJSON())).toContain('Plan A');
  expect(tree!.root.findAllByType('button').some(button => button.children.includes('Execute plan'))).toBe(true);

  await act(async () => tree!.update(<ChatPanel presentation="woven" resumeConversation={{ requestId: 2, projection: projectionB }} />));
  const loadingView = JSON.stringify(tree!.toJSON());
  expect(loadingView).not.toContain('Plan A');
  expect(tree!.root.findAllByType('button').some(button => button.children.includes('Execute plan'))).toBe(false);
  expect(tree!.root.findAllByType('button').some(button => button.children.includes('Turn into workflow'))).toBe(false);

  await act(async () => {
    capabilityB.resolve(capability);
    revisionsB.resolve({ schemaVersion: 'chirality.native-plan-revisions/v3', status: 'qualified', qualification, revisions: [revisionB] });
    clarificationsB.resolve({ schemaVersion: 'chirality.native-plan-clarifications/v3', status: 'qualified', qualification, clarifications: [] });
    await Promise.resolve(); await Promise.resolve();
  });
  expect(JSON.stringify(tree!.toJSON())).toContain('Plan B');
  expect(JSON.stringify(tree!.toJSON())).not.toContain('Plan A');
  expect(tree!.root.findAllByType('button').some(button => button.children.includes('Execute plan'))).toBe(true);
});

it('never makes a historical Plan clarification actionable in an idle resumed chat', async () => {
  const qualification = { adapterId: 'codex-app-server', providerId: 'openai', qualificationId: 'fixture', admissionSha256: 'a'.repeat(64), evidenceClass: 'native-adapter-qualified' as const };
  state.nativeCapability.mockResolvedValue({ schemaVersion: 'chirality.native-plan-capability/v3', status: 'qualified', qualification });
  state.nativeClarifications.mockResolvedValue({ clarifications: [{ requestId: 31, questions: [{ id: 'q', header: 'Old question', question: 'Old pending question?' }] }] });
  const projection = resumableProjection('session-a');
  projection.session!.continuation!.interactionMode = 'native-plan';
  await mount({ resumeConversation: { requestId: 1, projection } });
  expect(tree!.root.findAllByProps({ className: 'native-plan-clarification' })).toHaveLength(0);
  expect(state.answerRequest).not.toHaveBeenCalled();
});

it('preserves an unsupported legacy permission profile until the operator continues with Project access', async () => {
  state.stream.mockResolvedValue(undefined);
  const projection = resumableProjection('legacy-permissions');
  await mount({ resumeConversation: { requestId: 1, projection } });
  await type('Continue this recorded chat');
  // The permission selector offers the four Codex postures; a retired legacy
  // profile on a recorded chat is named and must be replaced before sending.
  // Model and Reasoning are separate catalog controls, not permission postures.
  expect(tree!.root.findAllByType('select').map(node => node.props['aria-label'])).toEqual(['Interaction mode', 'Permissions', 'Model', 'Reasoning']);
  const alert = tree!.root.findByProps({ role: 'alert' });
  expect(alert.type).toBe('p');
  const textOf = (node: { children: unknown[] }): string => node.children.map(child => typeof child === 'string' ? child : textOf(child as { children: unknown[] })).join('');
  expect(textOf(alert)).toBe('This recorded chat used an unknown permission mode (dontAsk). Continue with Write in workspace');
  expect(continueWithProjectAccess()).toBeDefined();
  expect(tree!.root.findByProps({ 'aria-label': 'Send' }).props.disabled).toBe(true);
  await submit();
  expect(state.stream).not.toHaveBeenCalled();

  await act(async () => continueWithProjectAccess()!.props.onClick());
  expect(tree!.root.findAllByProps({ role: 'alert' })).toHaveLength(0);
  expect(tree!.root.findByProps({ 'aria-label': 'Send' }).props.disabled).toBe(false);
  await submit();
  expect(state.stream).toHaveBeenCalledWith(expect.objectContaining({ sessionId: 'legacy-permissions', permissionMode: 'workspaceWrite' }), expect.any(Function), expect.any(AbortSignal));
});

it('resets a new chat to the supported Project access profile', async () => {
  state.stream.mockResolvedValue(undefined);
  await mount({ resumeConversation: { requestId: 1, projection: resumableProjection('legacy-permissions') } });
  expect(continueWithProjectAccess()).toBeDefined();
  await act(async () => tree!.update(<ChatPanel presentation="woven" resumeConversation={{ requestId: 1, projection: resumableProjection('legacy-permissions') }} newChatRequest={1} />));
  expect(continueWithProjectAccess()).toBeUndefined();
  expect(JSON.stringify(tree!.toJSON())).not.toContain('no longer supported');
  await type('Fresh chat'); await submit();
  expect(state.stream).toHaveBeenCalledWith(expect.objectContaining({ permissionMode: 'workspaceWrite' }), expect.any(Function), expect.any(AbortSignal));
});

it('restores method references when the first method-bearing turn fails after boot', async () => {
  const method = { kind: 'workflow' as const, name: 'project-setup', source: 'bundled' as const, sourceRootId: 'chirality-root' };
  state.boot.mockResolvedValue({ session: {
    schemaVersion: 'chirality.session/v3', sessionId: 'bound', projectRoot: '/chosen/subfolder',
    selectedMethods: [method], methodSelectionRevision: 1, instructionBasisId: 'basis-1'
  } });
  let select!: (methods: QualifiedMethodReference[]) => void;
  function Fixture() {
    const [methods, setMethods] = React.useState<QualifiedMethodReference[]>([]);
    select = setMethods;
    return <ChatPanel presentation="woven" selectedMethods={methods} onSelectedMethodsChange={setMethods} />;
  }
  await act(async () => { tree = create(<Fixture />); });
  await act(async () => select([method]));
  await type('Retry this method-bearing turn');
  await submit();
  expect(tree!.root.findByProps({ 'aria-label': 'Chat input' }).props.value).toBe('Retry this method-bearing turn');
  expect(tree!.root.findAllByProps({ 'aria-label': 'Methods for next turn' })).toHaveLength(1);
});

it('uses the replayed active method revision after an agent changes methods during a turn', async () => {
  const agentMethod = { kind: 'skill' as const, name: 'researcher', source: 'bundled' as const, sourceRootId: 'chirality-root' };
  const nextMethod = { kind: 'skill' as const, name: 'review', source: 'project' as const, sourceRootId: 'project-root' };
  state.boot.mockResolvedValue({ session: {
    schemaVersion: 'chirality.session/v3', sessionId: 'bound', projectRoot: '/chosen/subfolder',
    selectedMethods: [], methodSelectionRevision: 2, instructionBasisId: 'basis-2'
  } });
  state.stream.mockResolvedValue(undefined);
  state.replay.mockResolvedValue({
    session: { schemaVersion: 'chirality.session/v3', sessionId: 'bound', projectRoot: '/chosen/subfolder', selectedMethods: [agentMethod], methodSelectionRevision: 5, instructionBasisId: 'basis-5' },
    events: [], transcript: [], instructionHistory: [], instructionBases: []
  });
  let select!: (methods: QualifiedMethodReference[]) => void;
  function Fixture() {
    const [methods, setMethods] = React.useState<QualifiedMethodReference[]>([]);
    select = setMethods;
    return <ChatPanel presentation="woven" selectedMethods={methods} onSelectedMethodsChange={setMethods} />;
  }
  await act(async () => { tree = create(<Fixture />); });
  await type('Agent loads a method'); await submit();
  await act(async () => select([nextMethod]));
  await type('Add another method'); await submit();
  expect(state.replaceMethods).toHaveBeenLastCalledWith('bound', [nextMethod], {
    boundaryConfirmed: true,
    selectionMode: 'merge',
    expectedRevision: 5,
    expectedBasisId: 'basis-5'
  });
});

it('refreshes a post-turn basis when replay was unavailable and retains later CAS rejection', async () => {
  const method = { kind: 'workflow' as const, name: 'create-workflow', source: 'bundled' as const, sourceRootId: 'chirality-root' };
  state.boot.mockResolvedValue({ session: {
    schemaVersion: 'chirality.session/v3', sessionId: 'bound', projectRoot: '/chosen/subfolder',
    selectedMethods: [], methodSelectionRevision: 0, instructionBasisId: 'basis-before-turn'
  } });
  state.stream.mockResolvedValue(undefined);
  state.getSession.mockResolvedValue({
    schemaVersion: 'chirality.session/v3', sessionId: 'bound', projectRoot: '/chosen/subfolder',
    selectedMethods: [], methodSelectionRevision: 0, instructionBasisId: 'basis-accepted-turn'
  });
  let select!: (methods: QualifiedMethodReference[]) => void;
  function Fixture() {
    const [methods, setMethods] = React.useState<QualifiedMethodReference[]>([]);
    select = setMethods;
    return <ChatPanel presentation="woven" selectedMethods={methods} onSelectedMethodsChange={setMethods} />;
  }
  await act(async () => { tree = create(<Fixture />); });
  await type('First message'); await submit();
  await act(async () => select([method]));
  await type('Create a workflow'); await submit();
  expect(state.replaceMethods).toHaveBeenLastCalledWith('bound', [method], {
    boundaryConfirmed: true, selectionMode: 'merge', expectedRevision: 0, expectedBasisId: 'basis-accepted-turn'
  });
  state.replaceMethods.mockRejectedValueOnce(new Error('Method selection revision changed before replacement'));
  await act(async () => select([method]));
  await type('Keep this draft'); await submit();
  expect(state.stream).toHaveBeenCalledTimes(2);
  expect(state.replaceMethods).toHaveBeenCalledTimes(2);
  expect(tree!.root.findByProps({ 'aria-label': 'Chat input' }).props.value).toBe('Keep this draft');
});

it('preserves methods selected for the next message while the current turn finishes', async () => {
  const pending = deferred<void>();
  state.stream.mockImplementation(() => pending.promise);
  const method = { kind: 'workflow' as const, name: 'research-orchestration', source: 'bundled' as const, sourceRootId: 'chirality-root' };
  let select!: (methods: QualifiedMethodReference[]) => void;
  function Fixture() {
    const [methods, setMethods] = React.useState<QualifiedMethodReference[]>([]);
    select = setMethods;
    return <ChatPanel presentation="woven" selectedMethods={methods} onSelectedMethodsChange={setMethods} />;
  }
  await act(async () => { tree = create(<Fixture />); });
  await type('Current turn'); await submit();
  await act(async () => select([method]));
  expect(tree!.root.findAllByProps({ 'aria-label': 'Methods for next turn' })).toHaveLength(1);
  await act(async () => pending.resolve());
  expect(tree!.root.findAllByProps({ 'aria-label': 'Methods for next turn' })).toHaveLength(1);
});

it('preserves an explicit empty next-message selection when a bound turn fails', async () => {
  const method = { kind: 'workflow' as const, name: 'research-orchestration', source: 'bundled' as const, sourceRootId: 'chirality-root' };
  let select!: (methods: QualifiedMethodReference[]) => void;
  function Fixture() {
    const [methods, setMethods] = React.useState<QualifiedMethodReference[]>([]);
    select = setMethods;
    return <ChatPanel presentation="woven" selectedMethods={methods} onSelectedMethodsChange={setMethods} />;
  }
  state.stream.mockResolvedValueOnce(undefined);
  await act(async () => { tree = create(<Fixture />); });
  await type('Bind this chat'); await submit();
  await act(async () => select([method]));
  let rejectTurn!: (error: Error) => void;
  const started = deferred<void>();
  state.stream.mockImplementationOnce(() => new Promise<void>((_resolve, reject) => { rejectTurn = reject; started.resolve(); }));
  await type('This turn will fail');
  await act(async () => {
    const submission = tree!.root.findByType('form').props.onSubmit({ preventDefault: vi.fn() });
    await started.promise;
    select([]);
    rejectTurn(new HarnessApiClientError(400, 'INVALID_REQUEST', 'Fixture turn failure'));
    await submission;
  });
  expect(tree!.root.findAllByProps({ 'aria-label': 'Methods for next turn' })).toHaveLength(0);
  expect(tree!.root.findByProps({ 'aria-label': 'Chat input' }).props.value).toBe('This turn will fail');
});

it('rejects empty and multiple-file drops without invoking folder validation', async () => {
  await mount(); const drop = tree!.root.findByType('form').props.onDrop;
  await act(async () => drop({ preventDefault: vi.fn(), dataTransfer: { files: [] } }));
  await act(async () => drop({ preventDefault: vi.fn(), dataTransfer: { files: [{}, {}] } }));
  await act(async () => drop({ preventDefault: vi.fn(), dataTransfer: { files: [{}] } }));
  expect(state.apply).not.toHaveBeenCalled();
  expect(JSON.stringify(tree!.toJSON())).toContain('Drop a folder');
});

it.each([true, false])('retains conversation binding across an Agent change (provider sync %s), until New chat', async (sync) => {
  state.stream.mockResolvedValue(undefined);
  if (!sync) state.apply.mockResolvedValue(false);
  const binding = vi.fn();
  await mount({ onBindingChange: binding }); await type('First completed turn'); await submit();
  state.query = 'agent=HELPS_HUMANS';
  await act(async () => tree!.update(<ChatPanel presentation="woven" onBindingChange={binding} />));
  expect(JSON.stringify(tree!.toJSON())).toContain('First completed turn');
  expect(binding).toHaveBeenLastCalledWith({ root: '/canonical', locked: true });
  expect(tree!.root.findByProps({ className: 'chat-folder-fixed' }).props.title).toBe('/canonical');
  const calls = state.apply.mock.calls.length;
  await act(async () => state.nativeListener?.({ path: '/native-other' }));
  const bridge = (window as unknown as { chirality: { folders: { pathForFile: ReturnType<typeof vi.fn> } } }).chirality.folders;
  bridge.pathForFile.mockReturnValue('/drop-other');
  await act(async () => tree!.root.findByType('form').props.onDrop({ preventDefault: vi.fn(), dataTransfer: { files: [{}] } }));
  expect(state.apply).toHaveBeenCalledTimes(calls);
  await type('Second agent turn'); await submit();
  expect(state.create).toHaveBeenCalledTimes(1);
  expect(state.replaceMethods).toHaveBeenLastCalledWith('bound', undefined, { roleId: 'HELPS_HUMANS', boundaryConfirmed: true, expectedRevision: 0, expectedBasisId: 'basis-initial' });
  expect(binding).toHaveBeenLastCalledWith({ root: '/canonical', locked: true });
  assertCanonicalUntouched();
  await act(async () => tree!.update(<ChatPanel presentation="woven" onBindingChange={binding} newChatRequest={1} />));
  expect(binding).toHaveBeenLastCalledWith({ root: state.root, locked: false });
  expect(JSON.stringify(tree!.toJSON())).not.toContain('First completed turn');
});
it('changes roles at a confirmed boundary without booting another App session', async () => {
  state.stream.mockResolvedValue(undefined); state.apply.mockResolvedValue(false);
  const binding = vi.fn(); await mount({ onBindingChange: binding }); await type('Original turn'); await submit();
  state.query = 'agent=HELPS_HUMANS';
  await act(async () => tree!.update(<ChatPanel presentation="woven" onBindingChange={binding} />));
  await type('Continue in one chat'); await submit();
  expect(state.stream).toHaveBeenCalledTimes(2);
  expect(state.create).toHaveBeenCalledTimes(1);
  expect(state.boot).toHaveBeenCalledTimes(1);
  expect(state.replaceMethods).toHaveBeenLastCalledWith('bound', undefined, { roleId: 'HELPS_HUMANS', boundaryConfirmed: true, expectedRevision: 0, expectedBasisId: 'basis-initial' });
  expect(binding).toHaveBeenLastCalledWith({ root: '/canonical', locked: true });
  expect(JSON.stringify(tree!.toJSON())).toContain('Original turn');
  assertCanonicalUntouched();
});

it('keeps the unsent draft under the bound conversation when its role changes', async () => {
  state.stream.mockResolvedValue(undefined);
  await mount(); await type('First completed turn'); await submit();
  await type('Unsent next instruction');
  state.query = 'agent=HELPS_HUMANS';
  await act(async () => tree!.update(<ChatPanel presentation="woven" />));
  expect(tree!.root.findByProps({ 'aria-label': 'Chat input' }).props.value).toBe('Unsent next instruction');
});

it('continues a compatible recorded v3 conversation without creating or booting another session', async () => {
  state.stream.mockResolvedValue(undefined);
  const activeMethod = { kind: 'workflow' as const, name: 'project-setup', source: 'bundled' as const, sourceRootId: 'chirality-root' };
  const projection = {
    selectedSessionId: 'recorded-v3', sourceReference: 'session:recorded-v3/events', observedAt: '2026-09-09T00:00:00.000Z',
    disclosure: 'READY_SNAPSHOT', currency: 'CURRENT', malformedLineCount: 0, sourceEventCount: 2, renderedItemCount: 2, diagnostics: [],
    transcript: { sessionId: 'recorded-v3', itemCount: 2, items: [
      { key: 'old-user', kind: 'message', role: 'user', status: 'completed', title: 'You', timestamp: '2026-09-09T00:00:00.000Z', eventId: 'event-1', eventType: 'message.completed', text: 'Earlier question', attachments: ['/chosen/subfolder/red.png'] },
      { key: 'attachment-only', kind: 'message', role: 'user', status: 'accepted', title: 'You', timestamp: '2026-09-09T00:00:00.100Z', eventId: 'attachment-event', eventType: 'turn.accepted', attachments: ['/chosen/subfolder/notes.md'] },
      { key: 'old-answer', kind: 'message', role: 'assistant', status: 'completed', title: 'Assistant', timestamp: '2026-09-09T00:00:01.000Z', eventId: 'event-2', eventType: 'message.completed', turnId: 'turn-old', text: 'Earlier answer' }
    ] }, instructionHistory: [{ schemaVersion: 'chirality.instruction-history/v1', historyId: 'history-old', sessionId: 'recorded-v3', sequence: 1, timestamp: '2026-09-09T00:00:00.500Z', type: 'instruction-basis.resolved', acceptedTurn: { turnId: 'turn-old', eventId: 'event-1' }, basisId: 'basis-old' }], instructionBases: [{
      schemaVersion: 'chirality.instruction-basis/v1', basisId: 'basis-old', sessionId: 'recorded-v3', createdAt: '2026-09-09T00:00:00.500Z', roleId: 'HELP_HUMAN', interactionMode: 'chat', permissionMode: 'ask', selectedMethods: [], compatibilityInputs: [], compatibilityMappings: [], suppliedEntries: [], methodDispositions: []
    }],
    session: { projectionId: 'operator-session:recorded-v3', sourceReference: 'session:recorded-v3', sessionId: 'recorded-v3', observedAt: '2026-09-09T00:00:02.000Z', currency: 'CURRENT', runtimeStatus: 'completed', parentage: { state: 'NOT_RECORDED' }, diagnostics: [], continuation: {
      schemaVersion: 'chirality.session/v3', projectRoot: '/chosen/subfolder', roleId: 'WORKING_ITEMS', mode: 'CHAT', interactionMode: 'chat', permissionMode: 'ask', selectedMethods: [activeMethod], methodSelectionRevision: 2, instructionBasisId: 'basis-2'
    } }
  } satisfies SelectedSessionReplayProjection;
  const resumed = vi.fn();
  await mount({ resumeConversation: { requestId: 1, projection }, onConversationResumed: resumed });
  expect(resumed).toHaveBeenCalledWith('recorded-v3');
  expect(JSON.stringify(tree!.toJSON())).toContain('Earlier question');
  expect(JSON.stringify(tree!.toJSON())).toContain('Earlier answer');
  expect(JSON.stringify(tree!.toJSON())).toContain('red.png');
  expect(JSON.stringify(tree!.toJSON())).toContain('notes.md');
  expect(tree!.root.findAllByProps({ className: 'chat-speaker' }).some(node => node.children.join('') === 'Help Human')).toBe(true);
  // The recorded "ask" posture is a supported Codex posture: no interstitial.
  expect(continueWithProjectAccess()).toBeUndefined();
  expect(tree!.root.findByProps({ 'aria-label': 'Permissions' }).props.value).toBe('ask');
  await type('Continue here'); await submit();
  expect(state.create).not.toHaveBeenCalled();
  expect(state.boot).not.toHaveBeenCalled();
  expect(state.replaceMethods).not.toHaveBeenCalled();
  expect(state.resolveContext).toHaveBeenCalledWith(expect.objectContaining({ sessionId: 'recorded-v3', methods: [activeMethod] }));
  expect(state.stream).toHaveBeenCalledWith(expect.objectContaining({ sessionId: 'recorded-v3', message: 'Continue here', permissionMode: 'ask' }), expect.any(Function), expect.any(AbortSignal));
  expect(state.stream.mock.calls.at(-1)?.[0]).not.toHaveProperty('methods');
});

it('reopens a bound draft under the canonical session root after initial root synchronization', async () => {
  state.stream.mockResolvedValue(undefined);
  await mount(); await type('Create canonical session'); await submit();
  await type('Saved canonical follow-up');
  const canonicalSessionKey = buildChatDraftStorageKey('/canonical', 'session:bound', 'CHAT');
  expect(JSON.parse(values.get(canonicalSessionKey)!).draft).toBe('Saved canonical follow-up');
  act(() => tree!.unmount()); tree = undefined;
  const projection = resumableProjection('bound');
  projection.session!.continuation!.projectRoot = '/canonical';
  await mount({ resumeConversation: { requestId: 1, projection } });
  expect(tree!.root.findByProps({ 'aria-label': 'Chat input' }).props.value).toBe('Saved canonical follow-up');
});

it('keeps unsent drafts isolated between recorded conversations with the same root and role', async () => {
  values.set(buildChatDraftStorageKey('/chosen/subfolder', 'session:recorded-b', 'CHAT'), JSON.stringify({ draft: 'Draft for B', attachments: [], methods: [] }));
  await mount({ resumeConversation: { requestId: 1, projection: resumableProjection('recorded-a') } });
  await type('Draft for A');
  expect(JSON.parse(values.get(buildChatDraftStorageKey('/chosen/subfolder', 'session:recorded-a', 'CHAT'))!).draft).toBe('Draft for A');
  await act(async () => tree!.update(<ChatPanel presentation="woven" resumeConversation={{ requestId: 2, projection: resumableProjection('recorded-b') }} />));
  expect(tree!.root.findByProps({ 'aria-label': 'Chat input' }).props.value).toBe('Draft for B');
  expect(JSON.parse(values.get(buildChatDraftStorageKey('/chosen/subfolder', 'session:recorded-a', 'CHAT'))!).draft).toBe('Draft for A');
});

it('does not resurrect a sent unbound draft when a new chat starts with the same root and role', async () => {
  const entryKey = buildChatDraftStorageKey('/chosen/subfolder', 'WORKING_ITEMS', 'CHAT');
  values.set(entryKey, JSON.stringify({ draft: 'Send this once', attachments: [], methods: [] }));
  state.boot.mockResolvedValue({ session: { sessionId: 'same-root', projectRoot: '/chosen/subfolder' } });
  state.stream.mockResolvedValue(undefined);
  await mount();
  expect(tree!.root.findByProps({ 'aria-label': 'Chat input' }).props.value).toBe('Send this once');
  await submit();
  expect(values.has(entryKey)).toBe(false);
  await act(async () => tree!.update(<ChatPanel presentation="woven" newChatRequest={1} />));
  expect(tree!.root.findByProps({ 'aria-label': 'Chat input' }).props.value).toBe('');
});

it('does not resurrect a consumed unbound method reference in the next chat', async () => {
  const method = { kind: 'workflow' as const, name: 'project-setup', source: 'bundled' as const, sourceRootId: 'chirality-root' };
  const entryKey = buildChatDraftStorageKey('/chosen/subfolder', 'WORKING_ITEMS', 'CHAT');
  values.set(entryKey, JSON.stringify({ draft: 'Use the method once', attachments: [], methods: [method] }));
  state.boot.mockResolvedValue({ session: { schemaVersion: 'chirality.session/v3', sessionId: 'method-session', projectRoot: '/chosen/subfolder', selectedMethods: [method], methodSelectionRevision: 1, instructionBasisId: 'basis-1' } });
  state.stream.mockResolvedValue(undefined);
  function Fixture({ newChatRequest = 0 }: { newChatRequest?: number }) {
    const [methods, setMethods] = React.useState<QualifiedMethodReference[]>([]);
    return <ChatPanel presentation="woven" selectedMethods={methods} onSelectedMethodsChange={setMethods} newChatRequest={newChatRequest} />;
  }
  await act(async () => { tree = create(<Fixture />); });
  expect(tree!.root.findAllByProps({ 'aria-label': 'Methods for next turn' })).toHaveLength(1);
  await submit();
  expect(values.has(entryKey)).toBe(false);
  await act(async () => tree!.update(<Fixture newChatRequest={1} />));
  expect(tree!.root.findAllByProps({ 'aria-label': 'Methods for next turn' })).toHaveLength(0);
});

it('keeps retained assistant speaker labels and titles tied to their originating Agent', async () => {
  state.stream.mockResolvedValue(undefined);
  await mount(); await type('First agent'); await submit();
  const speakers = () => tree!.root.findAllByProps({ className: 'chat-speaker' }).filter(node => node.props.title);
  expect(speakers().map(node => [node.props.title, node.children.join('')])).toEqual([
    ['WORKING_ITEMS', 'Working Items'], ['WORKING_ITEMS', 'Working Items']
  ]);
  state.query = 'agent=HELPS_HUMANS';
  await act(async () => tree!.update(<ChatPanel presentation="woven" />));
  await type('Second agent'); await submit();
  expect(speakers().map(node => [node.props.title, node.children.join('')])).toEqual([
    ['WORKING_ITEMS', 'Working Items'], ['WORKING_ITEMS', 'Working Items'], ['HELPS_HUMANS', 'Helps Humans']
  ]);
});

it('captures first input and paste before parent restoration, and delays restoration during IME', async () => {
  const restored = vi.fn();
  function Fixture() {
    const [expanded, setExpanded] = React.useState(true);
    return <section data-expanded={expanded}><ChatPanel presentation="woven" onDraftCaptured={() => { restored(); setExpanded(false); }} /></section>;
  }
  await act(async () => { tree = create(<Fixture />); });
  const input = tree!.root.findByType('textarea');
  await act(async () => input.props.onChange({ target: { value: 'a' }, nativeEvent: { isComposing: false } }));
  expect(tree!.root.findByType('textarea')).toBe(input);
  expect(input.props.value).toBe('a'); expect(tree!.root.findByType('section').props['data-expanded']).toBe(false);
  await act(async () => input.props.onChange({ target: { value: 'a pasted text' }, nativeEvent: { inputType: 'insertFromPaste', isComposing: false } }));
  expect(input.props.value).toBe('a pasted text');
  const calls = restored.mock.calls.length;
  await act(async () => input.props.onChange({ target: { value: 'あ' }, nativeEvent: { isComposing: true } }));
  expect(input.props.value).toBe('あ'); expect(restored).toHaveBeenCalledTimes(calls);
  await act(async () => input.props.onCompositionEnd({ currentTarget: { value: 'あい' } }));
  expect(input.props.value).toBe('あい'); expect(restored).toHaveBeenCalledTimes(calls + 1);
  expect(tree!.root.findByType('textarea')).toBe(input);
});

it('keeps legacy session creation and draft storage aligned with a changed Working Root', async () => {
  state.stream.mockResolvedValue(undefined);
  state.root = '/root-a';
  state.boot.mockResolvedValue({ session: { sessionId: 'a', projectRoot: '/root-a' } });
  const keyA = buildChatDraftStorageKey('/root-a', 'session:a', 'CHAT');
  const keyB = buildChatDraftStorageKey('/root-b', 'WORKING_ITEMS', 'CHAT');
  values.set(keyB, JSON.stringify({ draft: 'Saved root B prompt', attachments: [] }));
  await mount({ presentation: undefined }); await type('Completed root A turn'); await submit();
  await type('Unsent root A prompt');
  expect(JSON.parse(values.get(keyA)!).draft).toBe('Unsent root A prompt');
  await act(async () => root('/root-b'));
  expect(tree!.root.findByProps({ 'aria-label': 'Chat input' }).props.value).toBe('Saved root B prompt');
  state.boot.mockResolvedValue({ session: { sessionId: 'b', projectRoot: '/root-b' } });
  await submit();
  expect(state.create).toHaveBeenLastCalledWith({ projectRoot: '/root-b', persona: 'WORKING_ITEMS', roleId: 'WORKING_ITEMS', mode: 'CHAT', interactionMode: 'chat', permissionMode: 'workspaceWrite', selectedMethods: [] });
  expect(state.create).toHaveBeenCalledTimes(2);
  expect(JSON.parse(values.get(keyA)!).draft).toBe('Unsent root A prompt');
  expect(values.has(keyB)).toBe(false);
});

it('threads file navigation only to assistant Markdown and preserves attachment payload and failure restoration', async () => {
  const open = vi.fn();
  const catalog = ['/chosen/subfolder/docs/SPEC.md'];
  await mount({ fileCatalog: catalog, onOpenFile: open });
  expect(state.markdownProps.at(-1)).toMatchObject({ source: 'What would you like to work on?', fileCatalog: catalog, onOpenFile: open });
  expect(state.markdownProps.at(-1)?.projectRoot).toBeUndefined();
  await act(async () => tree!.root.findByProps({ 'data-add-attachment': true }).props.onClick());
  await type('Keep attachment');
  await submit();
  expect(state.stream).toHaveBeenCalledWith(expect.objectContaining({
    message: 'Keep attachment',
    attachments: ['/chosen/subfolder/docs/input.txt']
  }), expect.any(Function), expect.any(AbortSignal));
  expect(tree!.root.findByProps({ 'aria-label': 'Chat input' }).props.value).toBe('Keep attachment');
  expect(tree!.root.findAllByProps({ className: 'attachment-chip' }).some(node => node.props.title === '/chosen/subfolder/docs/input.txt')).toBe(true);
  expect(state.markdownProps.every(props => props.fileCatalog === catalog && props.onOpenFile === open)).toBe(true);
});

it('keeps retained assistant Markdown bound to the root that produced it', async () => {
  state.stream.mockImplementation(async (_input, onEvent) => { onEvent({ event: 'chat:complete', data: { text: '[spec](docs/SPEC.md)' } }); });
  state.boot.mockResolvedValue({ session: { sessionId: 'bound', projectRoot: '/chosen/subfolder' } });
  await mount({ fileCatalog: ['/chosen/subfolder/docs/SPEC.md'], onOpenFile: vi.fn() });
  await type('Create a link'); await submit();
  expect(state.markdownProps.at(-1)?.projectRoot).toBe('/chosen/subfolder');
  await act(async () => root('/other'));
  await act(async () => tree!.update(<ChatPanel presentation="woven" fileCatalog={['/other/docs/SPEC.md']} onOpenFile={vi.fn()} />));
  expect(state.markdownProps.at(-1)).toMatchObject({ projectRoot: '/chosen/subfolder', fileCatalog: ['/other/docs/SPEC.md'] });
  act(() => tree!.unmount()); tree = undefined;
  state.markdownProps = [];
  await mount({ fileCatalog: ['/other/docs/SPEC.md'], onOpenFile: vi.fn() });
  expect(state.markdownProps.at(-1)?.projectRoot).toBeUndefined();
});


it('accepts Runtime interrupted exit 130 without a request failure and permits a follow-up turn', async () => {
  state.stream.mockImplementationOnce(async (_input, onEvent) => {
    onEvent({ event: 'harness:event', data: { type: 'turn.interrupted', sessionId: 'bound', turnId: _input.turnId } });
    onEvent({ event: 'process:exit', data: { exitCode: 130, interrupted: true } });
  });
  await mount(); await type('Interrupt this turn'); await submit();
  const output = JSON.stringify(tree!.toJSON());
  expect(output).toContain('Turn interrupted by operator.');
  expect(tree!.root.findAllByProps({ className: 'chat-runtime-error' })).toHaveLength(0);
  expect(output).not.toContain('Harness Request Failed');
  expect(output).not.toContain('Turn failed with exit code');
  expect(tree!.root.findByProps({ 'aria-label': 'Chat input' }).props.value).toBe('');
  state.stream.mockImplementationOnce(async (_input, onEvent) => {
    onEvent({ event: 'chat:complete', data: { text: 'Follow-up completed.' } });
    onEvent({ event: 'process:exit', data: { exitCode: 0 } });
  });
  await type('Continue normally'); await submit();
  expect(JSON.stringify(tree!.toJSON())).toContain('Follow-up completed.');
  expect(state.create).toHaveBeenCalledTimes(1);
});

it.each([{ exitCode: 130 }, { exitCode: 1, interrupted: true }, { exitCode: 1 }])('retains failure handling for unconfirmed or other nonzero exits: %j', async payload => {
  state.stream.mockImplementationOnce(async (_input, onEvent) => {
    onEvent({ event: 'process:exit', data: payload });
  });
  await mount(); await type('Keep this failed draft'); await submit();
  expect(JSON.stringify(tree!.toJSON())).toContain(`Turn failed with exit code ${payload.exitCode}.`);
  expect(tree!.root.findByProps({ 'aria-label': 'Chat input' }).props.value).toBe('Keep this failed draft');
});

it('does not erase an earlier fatal turn error when a later exit is marked interrupted', async () => {
  state.stream.mockImplementationOnce(async (_input, onEvent) => {
    onEvent({ event: 'turn:error', data: { fatal: true, message: 'Underlying fatal failure', errorType: 'SDK_FAILURE' } });
    onEvent({ event: 'process:exit', data: { exitCode: 130, interrupted: true } });
  });
  await mount(); await type('Preserve failure evidence'); await submit();
  expect(JSON.stringify(tree!.toJSON())).toContain('SDK_FAILURE');
  expect(tree!.root.findByProps({ 'aria-label': 'Chat input' }).props.value).toBe('Preserve failure evidence');
});


it('retains a created chat after boot timeout and reconciles without duplicate creation, boot, or prompt', async () => {
  const { HarnessApiClientError } = await import('../../lib/harness/client');
  state.create.mockResolvedValue({ sessionId: 'created-before-timeout', projectRoot: '/chosen/subfolder', engineSelection: { adapterId: 'codex-app-server', providerId: 'openai', model: 'gpt-5.6-terra' }, reasoningEffort: 'high' });
  state.boot.mockRejectedValue(new HarnessApiClientError(504, 'ENGINE_UNAVAILABLE', 'hidden raw cause', { transportReason: 'timeout', operation: 'boot', sessionId: 'created-before-timeout' }));
  await mount(); await type('Send this exactly once'); await submit();
  expect(state.stream).not.toHaveBeenCalled();
  expect(tree!.root.findByProps({ 'aria-label': 'Chat input' }).props.value).toBe('Send this exactly once');
  expect(JSON.stringify(tree!.toJSON())).toContain('Chat took too long to start');
  expect(JSON.stringify(tree!.toJSON())).not.toContain('hidden raw cause');
  expect(tree!.root.findByProps({ 'aria-label': 'Model' }).props).toMatchObject({ disabled: true, value: 'gpt-5.6-terra' });
  expect(tree!.root.findByProps({ 'aria-label': 'Reasoning' }).props).toMatchObject({ disabled: true, value: 'high' });
  state.getSession.mockResolvedValue({ persona: 'WORKING_ITEMS', sessionId: 'created-before-timeout', projectRoot: '/chosen/subfolder', status: 'running' });
  await submit();
  expect(state.create).toHaveBeenCalledTimes(1); expect(state.boot).toHaveBeenCalledTimes(1); expect(state.stream).not.toHaveBeenCalled();
  state.getSession.mockResolvedValue({ persona: 'WORKING_ITEMS', sessionId: 'created-before-timeout', projectRoot: '/chosen/subfolder', status: 'idle', bootedAt: '2026-09-11T00:00:00Z', bootFingerprint: 'fingerprint', engineSessionId: 'native-fixture', engineSelection: { adapterId: 'codex-app-server', providerId: 'openai', model: 'gpt-5.6-terra' }, reasoningEffort: 'high' });
  state.stream.mockResolvedValue(undefined);
  await submit();
  expect(state.getSession).toHaveBeenCalledTimes(2);
  expect(state.create).toHaveBeenCalledTimes(1); expect(state.boot).toHaveBeenCalledTimes(1);
  expect(state.stream).toHaveBeenCalledTimes(1);
  expect(state.stream.mock.calls[0][0]).toMatchObject({ sessionId: 'created-before-timeout', message: 'Send this exactly once' });
});

it('never replaces or reboots an unconfirmed failed chat on another Send', async () => {
  state.create.mockResolvedValue({ sessionId: 'created-failed', projectRoot: '/chosen/subfolder' });
  state.boot.mockRejectedValue(new Error('boot failed'));
  await mount(); await type('Retain this request'); await submit();
  for (const status of ['failed', 'interrupted', 'idle']) {
    state.getSession.mockResolvedValue({ persona: 'WORKING_ITEMS', sessionId: 'created-failed', projectRoot: '/chosen/subfolder', status });
    await submit();
  }
  expect(state.create).toHaveBeenCalledTimes(1); expect(state.boot).toHaveBeenCalledTimes(1); expect(state.stream).not.toHaveBeenCalled();
  expect(tree!.root.findByProps({ 'aria-label': 'Chat input' }).props.value).toBe('Retain this request');
});


it('reconciles known unbooted history sessions before sending and resets for an explicit new chat', async () => {
  const projection = resumableProjection('historic-unbooted');
  projection.session!.bootstrapConfirmed = false;
  projection.session!.continuation!.permissionMode = 'workspaceWrite';
  state.getSession.mockResolvedValue({ persona: 'WORKING_ITEMS', sessionId: 'historic-unbooted', projectRoot: '/chosen/subfolder', status: 'failed' });
  await mount({ resumeConversation: { requestId: 1, projection } });
  await type('Unsatisfied original request'); await submit();
  expect(state.getSession).toHaveBeenCalledWith('historic-unbooted');
  expect(state.stream).not.toHaveBeenCalled(); expect(state.create).not.toHaveBeenCalled(); expect(state.boot).not.toHaveBeenCalled();
  await act(async () => tree!.update(<ChatPanel presentation="woven" newChatRequest={1} />));
  state.create.mockResolvedValue({ sessionId: 'fresh', projectRoot: '/chosen/subfolder' });
  state.boot.mockResolvedValue({ session: { sessionId: 'fresh', projectRoot: '/chosen/subfolder' } });
  state.stream.mockResolvedValue(undefined);
  await type('A deliberately new request'); await submit();
  expect(state.create).toHaveBeenCalledTimes(1); expect(state.boot).toHaveBeenCalledTimes(1);
  expect(state.stream).toHaveBeenCalledWith(expect.objectContaining({ sessionId: 'fresh', message: 'A deliberately new request' }), expect.any(Function), expect.any(AbortSignal));
});


it.each([
  { schemaVersion: 'chirality.session/v3', roleId: 'HELPS_HUMANS', persona: 'WORKING_ITEMS' },
  { schemaVersion: 'chirality.session/v3', persona: 'WORKING_ITEMS' },
  { persona: 'HELPS_HUMANS' },
  {}
])('rejects mismatched or missing canonical reconciliation role before sending: %j', async roleFields => {
  state.create.mockResolvedValue({ sessionId: 'role-check', projectRoot: '/chosen/subfolder', persona: 'WORKING_ITEMS' });
  state.boot.mockRejectedValue(new Error('boot response lost'));
  await mount(); await type('Keep this request with its role'); await submit();
  state.getSession.mockResolvedValue({ sessionId: 'role-check', projectRoot: '/chosen/subfolder', status: 'idle',
    bootedAt: '2026-09-11T00:00:00Z', bootFingerprint: 'confirmed', engineSessionId: 'native', ...roleFields });
  await submit();
  expect(state.stream).not.toHaveBeenCalled();
  expect(state.create).toHaveBeenCalledTimes(1); expect(state.boot).toHaveBeenCalledTimes(1);
  expect(JSON.stringify(tree!.toJSON())).toContain('Chat context changed');
  expect(tree!.root.findByProps({ 'aria-label': 'Chat input' }).props.value).toBe('Keep this request with its role');
});


it('shows a confirmed interruption alongside partial commentary and after reopening', async () => {
  state.stream.mockImplementationOnce(async (_input, onEvent) => {
    onEvent({ event: 'chat:delta', data: { text: 'Starting the requested work.' } });
    onEvent({ event: 'process:exit', data: { exitCode: 130, interrupted: true } });
  });
  await mount(); await type('Begin work'); await submit();
  expect(tree!.root.findByProps({ 'data-turn-outcome': 'interrupted' }).children).toEqual(['Stopped']);
  expect(state.markdownProps.some(props => props.source === 'Starting the requested work.')).toBe(true);
  expect(tree!.root.findAllByProps({ className: 'chat-runtime-error' })).toHaveLength(0);
  const projection = resumableProjection('interrupted-history');
  projection.transcript.items = [
    { key: 'partial', kind: 'message', role: 'assistant', status: 'started', title: 'Assistant', timestamp: '2026-09-09T00:00:01Z', eventId: 'partial', eventType: 'message.delta', turnId: 'cancelled', text: 'Starting the requested work.' },
    { key: 'stop', kind: 'terminal', status: 'interrupted', title: 'Turn interrupted', timestamp: '2026-09-09T00:00:02Z', eventId: 'stop', eventType: 'turn.interrupted', turnId: 'cancelled' }
  ];
  await act(async () => tree!.update(<ChatPanel presentation="woven" resumeConversation={{ requestId: 1, projection }} />));
  expect(tree!.root.findByProps({ 'data-turn-outcome': 'interrupted' }).children).toEqual(['Stopped']);
  expect(state.markdownProps.some(props => props.source === 'Starting the requested work.')).toBe(true);
});

it('hands the Plan tab model to its host, keeps every plan action working from there, and links revisions from the conversation', async () => {
  const { NativePlanPanel } = await import('../../components/shell/native-plan-panel');
  const qualification = { adapterId: 'codex-app-server', providerId: 'openai', qualificationId: 'fixture', admissionSha256: 'a'.repeat(64), evidenceClass: 'native-adapter-qualified' as const };
  const revisions = [1, 2].map(revision => ({ revision, sourceEvent: { qualificationState: 'qualified' as const, eventId: `plan-${revision}`, occurredAt: '2026-09-09T00:00:00.000Z', qualification, plan: { id: `item-${revision}`, type: 'plan', text: `# Plan ${revision}\n\nStep.` } } }));
  state.boot.mockResolvedValue({ session: { schemaVersion: 'chirality.session/v3', sessionId: 'bound', projectRoot: '/chosen/subfolder', selectedMethods: [], methodSelectionRevision: 0, instructionBasisId: 'basis-1' } });
  state.nativeCapability.mockResolvedValue({ schemaVersion: 'chirality.native-plan-capability/v3', status: 'qualified', qualification });
  state.nativeRevisions.mockResolvedValue({ schemaVersion: 'chirality.native-plan-revisions/v3', status: 'qualified', qualification, revisions });
  state.stream.mockResolvedValue(undefined);
  const onOpenPlan = vi.fn();
  function Host(): JSX.Element {
    const [model, setModel] = React.useState<import('../../components/shell/native-plan-panel').NativePlanPanelModel | null>(null);
    return <><ChatPanel presentation="woven" onPlanPanelChange={setModel} onOpenPlan={onOpenPlan} /><aside data-plan-host>{model ? <NativePlanPanel model={model} /> : <p>no plan model</p>}</aside></>;
  }
  await act(async () => { tree = create(<Host />); });
  expect(JSON.stringify(tree!.toJSON())).toContain('no plan model');
  await act(async () => tree!.root.findByProps({ 'aria-label': 'Interaction mode' }).props.onChange({ target: { value: 'native-plan' } }));
  await type('Plan this change'); await submit();
  await act(async () => { await Promise.resolve(); });
  const stage = tree!.root.findByProps({ className: 'chat-conversation-stage' });
  // The large plan block is gone from the conversation; compact links remain.
  expect(stage.findAllByProps({ 'aria-label': 'Plan' })).toHaveLength(0);
  expect(stage.findAllByProps({ className: 'chat-plan-link' }).map(node => node.children.join(''))).toEqual(['Plan · Revision 1', 'Plan · Revision 2']);
  await act(async () => stage.findAllByProps({ className: 'chat-plan-link' })[0].props.onClick());
  expect(onOpenPlan).toHaveBeenCalledWith(1);
  const host = tree!.root.findByProps({ 'data-plan-host': true });
  const textOf = (node: { children: unknown[] }): string => node.children.map(child => typeof child === 'string' ? child : textOf(child as { children: unknown[] })).join('');
  const hostText = () => textOf(tree!.root.findByProps({ 'data-plan-host': true }));
  expect(hostText()).not.toContain('no plan model');
  expect(hostText()).toContain('Plan 2');
  const button = (label: string) => host.findAllByType('button').find(node => node.children.includes(label))!;
  await act(async () => button('Revise in chat').props.onClick());
  expect(tree!.root.findByProps({ 'aria-label': 'Chat input' }).props.value).toContain('Revise plan revision 2');
  await act(async () => button('Execute plan').props.onClick());
  expect(tree!.root.findByProps({ 'aria-label': 'Interaction mode' }).props.value).toBe('chat');
  expect(tree!.root.findByProps({ 'aria-label': 'Chat input' }).props.value).toContain('Execute the accepted native Plan Mode revision 2');
  await act(async () => button('Turn into workflow').props.onClick());
  expect(tree!.root.findByProps({ 'aria-label': 'Chat input' }).props.value).toContain('Do not register it in .chirality/workflows or execute the plan.');
  window.chirality!.plans = { chooseExportTarget: vi.fn().mockResolvedValue({ cancelled: false, targetRelativePath: 'plans/native.md' }), confirmOverwrite: vi.fn().mockResolvedValue(false) };
  await act(async () => { await button('Save plan…').props.onClick(); });
  expect(state.exportPlan).toHaveBeenLastCalledWith({ sessionId: 'bound', revision: 2, targetRelativePath: 'plans/native.md' });
  expect(hostText()).toContain('Plan saved to');
  expect(host.findByProps({ className: 'native-plan-history' })).toBeDefined();
});


it('keeps an ambiguously delivered prompt in history without restoring its draft or sending twice', async () => {
  vi.useFakeTimers();
  try {
    // Fetch failed without a typed HTTP rejection: Runtime may have accepted it.
    state.stream.mockRejectedValueOnce(new TypeError('Failed to fetch'));
    await mount();
    await type('An uncertain delivery');
    await submit();
    expect(state.stream).toHaveBeenCalledTimes(1);
    expect(tree!.root.findByProps({ 'aria-label': 'Chat input' }).props.value).toBe('');
    expect(JSON.stringify(tree!.toJSON())).toContain('Reconnecting');
    await act(async () => { await vi.advanceTimersByTimeAsync(1_000); });
    expect(state.stream).toHaveBeenCalledTimes(1);
    expect(tree!.root.findByProps({ 'aria-label': 'Chat input' }).props.value).toBe('');
    expect(JSON.stringify(tree!.toJSON())).toContain('An uncertain delivery');
    expect(JSON.stringify(tree!.toJSON())).toContain('"data-turn-outcome":"unknown"');
    expect(JSON.stringify(tree!.toJSON())).not.toContain('"data-turn-outcome":"completed"');
    assertCanonicalUntouched();
  } finally { vi.useRealTimers(); }
});

it.each(['context', 'turn'] as const)('keeps a bound normal message for manual retry after a definitive Unknown session rejection: %s', async stage => {
  const projection = resumableProjection('bound-retry');
  const failure = new HarnessApiClientError(404, 'SESSION_NOT_FOUND', 'Unknown session');
  if (stage === 'context') state.resolveContext.mockRejectedValueOnce(failure);
  else state.stream.mockRejectedValueOnce(failure);
  await mount({ resumeConversation: { requestId: 1, projection } });
  await type('Preserve this correction exactly.');
  await submit();
  expect(tree!.root.findByProps({ 'aria-label': 'Chat input' }).props.value).toBe('Preserve this correction exactly.');
  expect(JSON.parse(values.get(buildChatDraftStorageKey('/chosen/subfolder', 'session:bound-retry', 'CHAT'))!).draft).toBe('Preserve this correction exactly.');
  expect(state.stream).toHaveBeenCalledTimes(stage === 'turn' ? 1 : 0);
  expect(state.create).not.toHaveBeenCalled();
});

it('recovers a definitely unsent bound message to its owning draft when context changes before rejection', async () => {
  const check = deferred<never>();
  state.resolveContext.mockReturnValueOnce(check.promise);
  await mount({ resumeConversation: { requestId: 1, projection: resumableProjection('bound-retry') } });
  await type('Keep the original chat correction.');
  await submit();
  await act(async () => root('/other'));
  await act(async () => check.reject(new HarnessApiClientError(404, 'SESSION_NOT_FOUND', 'Unknown session')));
  const key = buildChatDraftStorageKey('/chosen/subfolder', 'session:bound-retry', 'CHAT');
  expect(JSON.parse(values.get(key)!).draft).toBe('Keep the original chat correction.');
  expect(tree!.root.findByProps({ 'aria-label': 'Chat input' }).props.value).not.toBe('Keep the original chat correction.');
  expect(state.stream).not.toHaveBeenCalled();
  expect(JSON.stringify(tree!.toJSON())).toContain('original chat');
});

it('resumes a boot-ready Codex chat after a rejected first attachment and reload before any provider thread exists', async () => {
  const { projectOperatorSession } = await import('../../lib/woven-dialogue/operator-projection');
  const recorded = {
    schemaVersion: 'chirality.session/v3', sessionId: 'pre-thread-attachment', projectRoot: '/chosen/subfolder',
    persona: 'WORKING_ITEMS', roleId: 'WORKING_ITEMS', mode: 'CHAT', status: 'idle',
    bootedAt: '2026-09-13T00:00:00Z', bootFingerprint: 'verified-boot',
    engineSelection: { adapterId: 'codex-app-server', providerId: 'openai', model: 'configured-model' }
  };
  state.create.mockResolvedValue(recorded);
  state.boot.mockResolvedValue({ session: recorded });
  await mount();
  await act(async () => tree!.root.findByProps({ 'data-add-attachment': true }).props.onClick());
  await type('Retry the original attachment'); await submit();
  expect(state.stream).toHaveBeenCalledTimes(1);
  expect(tree!.root.findByProps({ 'aria-label': 'Chat input' }).props.value).toBe('Retry the original attachment');
  await act(async () => tree!.unmount()); tree = undefined;
  const projection = resumableProjection(recorded.sessionId);
  projection.session!.bootstrapConfirmed = projectOperatorSession(recorded as never, new Set([recorded.sessionId]), { observedAt: '2026-09-13' }).bootstrapConfirmed;
  state.getSession.mockResolvedValue(recorded);
  state.stream.mockResolvedValue(undefined);
  await mount({ resumeConversation: { requestId: 1, projection } });
  expect(tree!.root.findByProps({ 'aria-label': 'Chat input' }).props.value).toBe('Retry the original attachment');
  await submit();
  expect(state.stream).toHaveBeenCalledTimes(2);
  expect(state.stream).toHaveBeenLastCalledWith(expect.objectContaining({ sessionId: recorded.sessionId, message: 'Retry the original attachment', attachments: ['/chosen/subfolder/docs/input.txt'] }), expect.any(Function), expect.any(AbortSignal));
  expect(state.create).toHaveBeenCalledTimes(1); expect(state.boot).toHaveBeenCalledTimes(1);
  expect(state.getSession).not.toHaveBeenCalled();
});

it('reconciles a lost Codex boot response from Runtime boot stamps before the first provider thread', async () => {
  state.create.mockResolvedValue({ sessionId: 'codex-boot-response-lost', projectRoot: '/chosen/subfolder' });
  state.boot.mockRejectedValue(new Error('boot response lost'));
  await mount(); await type('Send only after readiness'); await submit();
  state.getSession.mockResolvedValue({ schemaVersion: 'chirality.session/v3', roleId: 'WORKING_ITEMS', sessionId: 'codex-boot-response-lost', projectRoot: '/chosen/subfolder', status: 'idle', bootedAt: '2026-09-13', bootFingerprint: 'verified-boot', engineSelection: { adapterId: 'codex-app-server', providerId: 'openai', model: 'configured-model' } });
  state.stream.mockResolvedValue(undefined);
  await submit();
  expect(state.create).toHaveBeenCalledTimes(1); expect(state.boot).toHaveBeenCalledTimes(1);
  expect(state.stream).toHaveBeenCalledTimes(1);
  expect(state.stream).toHaveBeenCalledWith(expect.objectContaining({ sessionId: 'codex-boot-response-lost', message: 'Send only after readiness' }), expect.any(Function), expect.any(AbortSignal));
});

it.each([{ bootedAt: '2026-09-13' }, { bootFingerprint: 'verified-boot' }, {}])('holds a genuinely incomplete Codex boot: %j', async stamps => {
  const projection = resumableProjection('incomplete-codex');
  projection.session!.bootstrapConfirmed = false;
  state.getSession.mockResolvedValue({ schemaVersion: 'chirality.session/v3', roleId: 'WORKING_ITEMS', sessionId: 'incomplete-codex', projectRoot: '/chosen/subfolder', status: 'idle', engineSelection: { adapterId: 'codex-app-server', providerId: 'openai', model: 'configured-model' }, ...stamps });
  await mount({ resumeConversation: { requestId: 1, projection } });
  await type('Keep this pending'); await submit();
  expect(state.stream).not.toHaveBeenCalled(); expect(state.boot).not.toHaveBeenCalled(); expect(state.create).not.toHaveBeenCalled();
  expect(tree!.root.findByProps({ 'aria-label': 'Chat input' }).props.value).toBe('Keep this pending');
});


it('adds requested workflow feedback to the existing draft without sending or replacing it', async () => {
  await mount(); await type('Keep my unsent notes.');
  const feedback = { sequence: 1, projectRoot: '/chosen/subfolder', name: 'meeting-review', source: 'project' as const };
  await act(async () => tree!.update(<ChatPanel presentation="woven" workflowFeedback={feedback} />));
  const text = tree!.root.findByProps({ 'aria-label': 'Chat input' }).props.value;
  expect(text).toContain('Keep my unsent notes.');
  expect(text).toContain('.chirality/workflow-drafts/meeting-review/WORKFLOW.md');
  expect(text).toContain('do not register it');
  expect(state.stream).not.toHaveBeenCalled();
  await act(async () => tree!.update(<ChatPanel presentation="woven" workflowFeedback={{...feedback, sequence: 2, projectRoot: '/other'}} />));
  expect(tree!.root.findByProps({ 'aria-label': 'Chat input' }).props.value).toBe(text);
});
