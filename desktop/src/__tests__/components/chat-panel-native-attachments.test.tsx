import React, { useSyncExternalStore } from 'react';
import { act, create, type ReactTestRenderer } from 'react-test-renderer';
import { afterEach, beforeEach, expect, it, vi } from 'vitest';

// Owner criterion F: the Attach button prefers the desktop picker when the
// preload bridge exposes it and falls back to the in-app FilePicker otherwise.
const state = vi.hoisted(() => ({ root: '/chosen/subfolder', listeners: new Set<() => void>(), pickerOpen: [] as boolean[],
  create: vi.fn(), boot: vi.fn(), replay: vi.fn(), stream: vi.fn(), apply: vi.fn(),
  replaceMethods: vi.fn(), resolveContext: vi.fn(), nativeCapability: vi.fn(), nativeRevisions: vi.fn(), nativeClarifications: vi.fn() }));
vi.mock('next/navigation', () => ({ usePathname: () => '/chat', useSearchParams: () => new URLSearchParams('agent=WORKING_ITEMS'), useRouter: () => ({ replace: vi.fn() }) }));
vi.mock('../../components/workspace/workspace-provider', () => ({ useWorkspace: () => ({
  projectRoot: useSyncExternalStore(listener => { state.listeners.add(listener); return () => state.listeners.delete(listener); }, () => state.root),
  applyProjectRoot: state.apply, chooseProjectRoot: vi.fn(async () => false), hasElectronDirectoryPicker: false, errorMessage: null
}) }));
vi.mock('../../components/workspace/toolkit-provider', () => ({ useToolkit: () => ({ optsPayload: undefined }) }));
vi.mock('../../components/workspace/harness-events-provider', () => ({ useHarnessEventActions: () => ({ appendEvent: vi.fn(), clearEvents: vi.fn(), hydrateEvents: vi.fn(), setStreaming: vi.fn() }), useHarnessEvents: () => ({ events: [], streaming: false }) }));
vi.mock('../../components/shell/runtime-connectivity-provider', () => ({ useRuntimeEpoch: () => 0 }));
vi.mock('../../components/shell/persona-picker', () => ({ PersonaPicker: () => <span>Working Items</span> }));
vi.mock('../../components/shell/file-picker', () => ({ FilePicker: ({ open }: { open: boolean }) => { state.pickerOpen.push(open); return <div data-file-picker-open={open} />; } }));
vi.mock('../../components/shell/permission-requests', () => ({ PermissionRequests: () => null }));
vi.mock('../../components/shell/chat-markdown', () => ({ ChatMarkdown: (props: { source: string }) => <p>{props.source}</p> }));
vi.mock('../../lib/harness/method-selection-client', async importOriginal => ({
  ...await importOriginal<typeof import('../../lib/harness/method-selection-client')>(),
  replaceSelectedMethods: state.replaceMethods, resolveSelectedContext: state.resolveContext,
  getNativePlanCapability: state.nativeCapability, listNativePlanRevisions: state.nativeRevisions, listNativePlanClarifications: state.nativeClarifications
}));
vi.mock('../../lib/harness/client', async importOriginal => ({ ...await importOriginal<typeof import('../../lib/harness/client')>(), createHarnessSession: state.create, bootHarnessSession: state.boot, replaySessionEvents: state.replay, streamHarnessTurn: state.stream, interruptHarnessSession: vi.fn(), getHarnessTurnState: vi.fn(async () => ({ active: false, lastSeq: 0 })), attachHarnessTurn: vi.fn(async () => undefined) }));
import { HarnessApiClientError } from '../../lib/harness/client';
import { ChatPanel } from '../../components/shell/chat-panel';

let tree: ReactTestRenderer | undefined;
const selectFiles = vi.fn();
function stubWindow(bridge: boolean) {
  vi.stubGlobal('window', { requestAnimationFrame: (callback: () => void) => { callback(); return 1; }, setInterval: globalThis.setInterval, clearInterval: globalThis.clearInterval,
    localStorage: { getItem: () => null, setItem: () => undefined, removeItem: () => undefined },
    chirality: { folders: { registerRecent: vi.fn(async () => ({ ok: true })), pathForFile: vi.fn(() => ''), subscribeOpen: () => () => undefined }, ...(bridge ? { attachments: { selectFiles } } : {}) } });
}
async function mount() { await act(async () => { tree = create(<ChatPanel presentation="woven" />); }); }
const attachButton = () => tree!.root.findByProps({ 'aria-label': 'Attach files' });
const chips = () => tree!.root.findAllByProps({ className: 'attachment-chip' }).map(node => node.props.title);
const pickerOpen = () => tree!.root.findAllByProps({ 'data-file-picker-open': true }).length > 0;

beforeEach(() => {
  vi.clearAllMocks(); state.root = '/chosen/subfolder'; state.listeners.clear(); state.pickerOpen = [];
  state.create.mockResolvedValue({ sessionId: 'bound' });
  state.boot.mockResolvedValue({ session: { sessionId: 'bound', projectRoot: '/chosen/subfolder' } });
  state.replay.mockRejectedValue(new Error('No replay fixture'));
  state.nativeCapability.mockResolvedValue({ schemaVersion: 'chirality.native-plan-capability/v3', status: 'unavailable', reason: 'fixture' });
  state.nativeRevisions.mockResolvedValue({ schemaVersion: 'chirality.native-plan-revisions/v3', status: 'unavailable', reason: 'fixture', revisions: [] });
  state.nativeClarifications.mockResolvedValue({ schemaVersion: 'chirality.native-plan-clarifications/v3', status: 'unavailable', reason: 'fixture', clarifications: [] });
  state.replaceMethods.mockResolvedValue({ schemaVersion: 'chirality.selected-methods/v3', sessionId: 'bound', revision: 1, methods: [], basisPreview: { id: 'basis-1' }, transition: { status: 'unchanged', successorAvailable: false } });
  state.resolveContext.mockResolvedValue({ schemaVersion: 'chirality.selected-context/v3', roleId: 'WORKING_ITEMS', methods: [], documents: [], dispositions: [], supplied: [], basisPreview: {}, compatibilityInputs: [], compatibilityMappings: [] });
  state.stream.mockRejectedValue(new Error('Fixture turn failure'));
});
afterEach(() => { if (tree) act(() => tree!.unmount()); tree = undefined; vi.unstubAllGlobals(); });

it('attaches native picker results scoped to the project root without opening the in-app picker', async () => {
  stubWindow(true);
  selectFiles.mockResolvedValue({ cancelled: false, paths: ['/chosen/subfolder/docs/input.txt', '/chosen/subfolder/image.png'] });
  await mount();
  await act(async () => attachButton().props.onClick());
  expect(selectFiles).toHaveBeenCalledExactlyOnceWith({ projectRoot: '/chosen/subfolder' });
  expect(chips()).toEqual(['/chosen/subfolder/docs/input.txt', '/chosen/subfolder/image.png']);
  expect(pickerOpen()).toBe(false);
  expect(tree!.root.findAllByProps({ role: 'alert' })).toHaveLength(0);
  // A second pick merges by path instead of duplicating.
  selectFiles.mockResolvedValue({ cancelled: false, paths: ['/chosen/subfolder/image.png', '/chosen/subfolder/notes.md'] });
  await act(async () => attachButton().props.onClick());
  expect(chips()).toEqual(['/chosen/subfolder/docs/input.txt', '/chosen/subfolder/image.png', '/chosen/subfolder/notes.md']);
});

it('surfaces a native picker error inline and stays quiet on plain cancellation', async () => {
  stubWindow(true);
  selectFiles.mockResolvedValueOnce({ cancelled: true, error: 'Unsupported attachment type.' });
  await mount();
  await act(async () => attachButton().props.onClick());
  expect(tree!.root.findByProps({ role: 'alert' }).children.join('')).toBe('Unsupported attachment type.');
  expect(chips()).toEqual([]);
  selectFiles.mockResolvedValueOnce({ cancelled: true });
  await act(async () => attachButton().props.onClick());
  expect(tree!.root.findAllByProps({ role: 'alert' })).toHaveLength(0);
  selectFiles.mockRejectedValueOnce(new Error('Picker crashed'));
  await act(async () => attachButton().props.onClick());
  expect(tree!.root.findByProps({ role: 'alert' }).children.join('')).toBe('Picker crashed');
  expect(pickerOpen()).toBe(false);
  expect(attachButton().props.disabled).toBe(false);
});

it('falls back to the in-app FilePicker when the desktop bridge is absent', async () => {
  stubWindow(false);
  await mount();
  expect(pickerOpen()).toBe(false);
  await act(async () => attachButton().props.onClick());
  expect(pickerOpen()).toBe(true);
  expect(selectFiles).not.toHaveBeenCalled();
});


it('keeps the contained selected copy and draft available after a rejected send', async () => {
  stubWindow(true);
  state.stream.mockRejectedValue(new HarnessApiClientError(400, 'INVALID_REQUEST', 'Fixture turn rejection'));
  selectFiles.mockResolvedValue({ cancelled: false, paths: ['/chosen/subfolder/.chirality/attachment-inputs/selection/visitor-desk-brief.txt'] });
  await mount();
  await act(async () => attachButton().props.onClick());
  expect(chips()).toEqual(['/chosen/subfolder/.chirality/attachment-inputs/selection/visitor-desk-brief.txt']);
  await act(async () => tree!.root.findByType('textarea').props.onChange({ target: { value: 'Summarize this brief' } }));
  await act(async () => tree!.root.findByType('form').props.onSubmit({ preventDefault: vi.fn() }));
  expect(state.stream).toHaveBeenCalled();
  expect(state.stream.mock.calls[0][0]).toMatchObject({ message: 'Summarize this brief', attachments: ['/chosen/subfolder/.chirality/attachment-inputs/selection/visitor-desk-brief.txt'] });
  expect(tree!.root.findByType('textarea').props.value).toBe('Summarize this brief');
  expect(chips()).toEqual(['/chosen/subfolder/.chirality/attachment-inputs/selection/visitor-desk-brief.txt']);
});

it.each(['selection', 'cancellation error', 'rejected request'])('discards stale native picker %s after the active folder changes', async (outcome) => {
  stubWindow(true);
  let finish!: (value: unknown) => void;
  let fail!: (error: Error) => void;
  selectFiles.mockImplementationOnce(() => new Promise((resolve, reject) => { finish = resolve; fail = reject; }));
  await mount();
  act(() => { void attachButton().props.onClick(); });
  await act(async () => { state.root = '/other/project'; state.listeners.forEach(listener => listener()); });
  await act(async () => {
    if (outcome === 'rejected request') fail(new Error('Stale picker error'));
    else if (outcome === 'cancellation error') finish({ cancelled: true, error: 'Stale picker error' });
    else finish({ cancelled: false, paths: ['/chosen/subfolder/.chirality/attachment-inputs/selection/visitor-desk-brief.txt'] });
  });
  expect(chips()).toEqual([]);
  expect(JSON.stringify(tree!.toJSON())).not.toContain('Stale picker error');
});
