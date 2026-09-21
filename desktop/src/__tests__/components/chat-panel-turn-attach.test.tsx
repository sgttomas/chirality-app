import React, { useSyncExternalStore } from 'react';
import { act, create, type ReactTestRenderer } from 'react-test-renderer';
import { afterEach, beforeEach, expect, it, vi } from 'vitest';
import type { SelectedSessionReplayProjection } from '../../lib/woven-dialogue/contracts';

/**
 * Runtime owns the turn (D-GOV-43 A2); the panel only observes it. Opening a
 * chat with an active turn replays the persisted log, attaches from seq 0 and
 * deduplicates by eventId; a stream that closes without a terminal frame while
 * the turn is still active shows "Reconnecting" (never Idle) and re-attaches
 * after the last sequence it saw; Stop is an explicit interrupt call, not a
 * disconnect; `turn.interrupted` renders the moment it arrives.
 */
const state = vi.hoisted(() => ({ root: '/chosen/subfolder', listeners: new Set<() => void>(),
  create: vi.fn(), boot: vi.fn(), replay: vi.fn(), stream: vi.fn(), attach: vi.fn(), turnState: vi.fn(), interrupt: vi.fn(), steer: vi.fn(), receipt: vi.fn(),
  append: vi.fn(), clear: vi.fn(), hydrate: vi.fn(), streaming: vi.fn(),
  replaceMethods: vi.fn(), resolveContext: vi.fn(), nativeCapability: vi.fn(), nativeRevisions: vi.fn(), nativeClarifications: vi.fn()
}));
vi.mock('next/navigation', () => ({ usePathname: () => '/chat', useSearchParams: () => new URLSearchParams('agent=WORKING_ITEMS'), useRouter: () => ({ replace: vi.fn() }) }));
vi.mock('../../components/workspace/workspace-provider', () => ({ useWorkspace: () => ({
  projectRoot: useSyncExternalStore(listener => { state.listeners.add(listener); return () => state.listeners.delete(listener); }, () => state.root),
  applyProjectRoot: vi.fn(async () => true), chooseProjectRoot: vi.fn(async () => false), hasElectronDirectoryPicker: false, errorMessage: null
}) }));
vi.mock('../../components/workspace/toolkit-provider', () => ({ useToolkit: () => ({ optsPayload: undefined }) }));
vi.mock('../../components/workspace/harness-events-provider', () => ({
  useHarnessEventActions: () => ({ appendEvent: state.append, clearEvents: state.clear, hydrateEvents: state.hydrate, setStreaming: state.streaming }),
  useHarnessEvents: () => ({ events: [], streaming: false })
}));
vi.mock('../../components/shell/runtime-connectivity-provider', () => ({ useRuntimeEpoch: () => 0 }));
vi.mock('../../components/shell/persona-picker', () => ({ PersonaPicker: () => <span>Working Items</span> }));
vi.mock('../../components/shell/file-picker', () => ({ FilePicker: () => null }));
vi.mock('../../components/shell/permission-requests', () => ({ PermissionRequests: () => null }));
vi.mock('../../components/shell/chat-markdown', () => ({ ChatMarkdown: (props: { source: string }) => <p>{props.source}</p> }));
vi.mock('../../lib/harness/method-selection-client', async importOriginal => ({
  ...await importOriginal<typeof import('../../lib/harness/method-selection-client')>(),
  replaceSelectedMethods: state.replaceMethods, resolveSelectedContext: state.resolveContext,
  getNativePlanCapability: state.nativeCapability, listNativePlanRevisions: state.nativeRevisions, listNativePlanClarifications: state.nativeClarifications,
  replyNativePlanClarification: vi.fn(), exportNativePlanRevision: vi.fn()
}));
vi.mock('../../lib/harness/client', async importOriginal => ({ ...await importOriginal<typeof import('../../lib/harness/client')>(),
  createHarnessSession: state.create, bootHarnessSession: state.boot, replaySessionEvents: state.replay, streamHarnessTurn: state.stream,
  attachHarnessTurn: state.attach, getHarnessTurnState: state.turnState, interruptHarnessSession: state.interrupt, steerHarnessSession: state.steer, checkHarnessSteeringReceipt: state.receipt, listHarnessSessionRequests: vi.fn(async () => ({ requests: [] })) }));
import { ChatPanel } from '../../components/shell/chat-panel';
import { HarnessApiClientError } from '../../lib/harness/client';

type Frame = { event: string; data: unknown; seq?: number };
const harness = (seq: number, eventId: string, type: string, data: Record<string, unknown> = {}) => ({
  event: 'harness:event', seq, data: { schemaVersion: 1, eventId, sessionId: 'resumed', turnId: 'turn-1', timestamp: '2026-09-12T00:00:00.000Z', type, data }
});
const persisted = (eventId: string, type: string, data: Record<string, unknown> = {}) => ({ schemaVersion: 1, eventId, sessionId: 'resumed', turnId: 'turn-1', timestamp: '2026-09-12T00:00:00.000Z', type, data });

function projection(sessionId: string): SelectedSessionReplayProjection {
  return { selectedSessionId: sessionId, sourceReference: `session:${sessionId}/events`, observedAt: '2026-09-10T00:00:00.000Z', disclosure: 'EMPTY', currency: 'CURRENT',
    transcript: { sessionId, itemCount: 0, items: [] }, instructionHistory: [], instructionBases: [], malformedLineCount: 0, sourceEventCount: 0, renderedItemCount: 0, diagnostics: [],
    session: { projectionId: `operator-session:${sessionId}`, sourceReference: `session:${sessionId}`, sessionId, observedAt: '2026-09-10T00:00:00.000Z', currency: 'CURRENT', runtimeStatus: 'running', parentage: { state: 'NOT_RECORDED' }, diagnostics: [],
      continuation: { schemaVersion: 'chirality.session/v3', projectRoot: '/chosen/subfolder', roleId: 'WORKING_ITEMS', mode: 'CHAT', interactionMode: 'chat', permissionMode: 'workspaceWrite', selectedMethods: [], methodSelectionRevision: 1, instructionBasisId: `basis-${sessionId}` } }
  };
}

let tree: ReactTestRenderer | undefined;
const rendered = () => JSON.stringify(tree!.toJSON());
const status = () => tree!.root.findAllByProps({ className: 'chat-runtime-status' }).map(node => node.children.join('')).join('');
const stopButtons = () => tree!.root.findAllByType('button').filter(node => node.children.join('') === 'Stop');
const flush = async () => { await act(async () => { await Promise.resolve(); await Promise.resolve(); await Promise.resolve(); }); };
async function mountResumed() {
  await act(async () => { tree = create(<ChatPanel presentation="woven" resumeConversation={{ requestId: 1, projection: projection('resumed') }} />); });
  await flush();
}

beforeEach(() => {
  vi.clearAllMocks(); state.listeners.clear();
  vi.stubGlobal('window', { confirm: vi.fn(() => true), requestAnimationFrame: (callback: () => void) => { callback(); return 1; }, setInterval: globalThis.setInterval, clearInterval: globalThis.clearInterval,
    localStorage: { getItem: () => null, setItem: () => undefined, removeItem: () => undefined },
    chirality: { folders: { registerRecent: vi.fn(async () => ({ ok: true })), pathForFile: vi.fn(() => ''), subscribeOpen: () => () => {} } } });
  state.replay.mockResolvedValue({ session: { schemaVersion: 'chirality.session/v3', sessionId: 'resumed' }, events: [] });
  state.turnState.mockResolvedValue({ active: false, lastSeq: 0 });
  state.attach.mockResolvedValue(undefined);
  state.stream.mockResolvedValue(undefined);
  state.interrupt.mockResolvedValue({ ok: true });
  state.resolveContext.mockResolvedValue({ schemaVersion: 'chirality.selected-context/v3', roleId: 'WORKING_ITEMS', methods: [], documents: [], dispositions: [], supplied: [], basisPreview: {}, compatibilityInputs: [], compatibilityMappings: [] });
  state.nativeCapability.mockResolvedValue({ schemaVersion: 'chirality.native-plan-capability/v3', status: 'unavailable', reason: 'fixture' });
  state.nativeRevisions.mockResolvedValue({ schemaVersion: 'chirality.native-plan-revisions/v3', status: 'unavailable', reason: 'fixture', revisions: [] });
  state.nativeClarifications.mockResolvedValue({ schemaVersion: 'chirality.native-plan-clarifications/v3', status: 'unavailable', reason: 'fixture', clarifications: [] });
});
afterEach(() => { if (tree) act(() => tree!.unmount()); tree = undefined; vi.unstubAllGlobals(); vi.useRealTimers(); });

it('leaves an idle session alone: turn state is read once and nothing is attached', async () => {
  await mountResumed();
  expect(state.turnState).toHaveBeenCalledWith('resumed');
  expect(state.attach).not.toHaveBeenCalled();
  expect(state.hydrate).not.toHaveBeenCalled();
  expect(stopButtons()).toHaveLength(0);
});

it('replays the log, attaches from seq 0, deduplicates by eventId and streams message.delta text', async () => {
  state.turnState.mockResolvedValue({ active: true, turnId: 'turn-1', lastSeq: 2, startedAt: '2026-09-12T00:00:00.000Z' });
  state.replay.mockResolvedValue({ session: { schemaVersion: 'chirality.session/v3', sessionId: 'resumed' }, events: [persisted('e1', 'turn.accepted'), persisted('e2', 'message.delta', { text: 'Hel' })] });
  let deliver!: (frame: Frame) => void;
  let finish!: () => void;
  state.attach.mockImplementation((_sessionId: string, _after: number, onEvent: (frame: Frame) => void) => new Promise<void>(resolve => { deliver = onEvent; finish = resolve; }));
  await mountResumed();

  expect(state.hydrate).toHaveBeenCalledWith([expect.objectContaining({ eventId: 'e1' }), expect.objectContaining({ eventId: 'e2' })]);
  expect(state.attach).toHaveBeenCalledWith('resumed', 0, expect.any(Function), expect.any(AbortSignal), 'turn-1');
  expect(stopButtons()).toHaveLength(1);
  expect(state.streaming).toHaveBeenLastCalledWith(true);

  // The buffer replays from seq 1: e1 and e2 are already in the log and are not appended twice.
  await act(async () => { deliver(harness(1, 'e1', 'turn.accepted')); deliver(harness(2, 'e2', 'message.delta', { text: 'Hel' })); deliver(harness(3, 'e3', 'message.delta', { text: 'lo' })); });
  expect(state.append.mock.calls.map(call => call[0].eventId)).toEqual(['e3']);
  expect(rendered()).toContain('Hello');

  await act(async () => { deliver(harness(4, 'e4', 'turn.completed')); finish(); });
  await flush();
  expect(stopButtons()).toHaveLength(0);
  expect(state.streaming).toHaveBeenLastCalledWith(false);
  expect(rendered()).toContain('Hello');
});

it('shows Reconnecting, never Idle, when the stream closes on a still-active turn and re-attaches after the last seq', async () => {
  vi.useFakeTimers();
  state.turnState.mockResolvedValue({ active: true, turnId: 'turn-1', lastSeq: 1, startedAt: '2026-09-12T00:00:00.000Z' });
  const attachCalls: Array<{ after: number; deliver: (frame: Frame) => void; finish: () => void }> = [];
  state.attach.mockImplementation((_sessionId: string, after: number, onEvent: (frame: Frame) => void) => new Promise<void>(resolve => { attachCalls.push({ after, deliver: onEvent, finish: resolve }); }));
  await mountResumed();
  expect(attachCalls.map(call => call.after)).toEqual([0]);

  await act(async () => { attachCalls[0].deliver(harness(5, 'e5', 'message.delta', { text: 'partial' })); attachCalls[0].finish(); });
  await flush();
  // The turn is still active according to the Runtime: the panel keeps running and says so.
  expect(status()).toContain('Reconnecting to the running turn');
  expect(stopButtons()).toHaveLength(1);
  expect(attachCalls).toHaveLength(1);

  await act(async () => { await vi.advanceTimersByTimeAsync(1_000); });
  await flush();
  expect(attachCalls.map(call => call.after)).toEqual([0, 5]);

  await act(async () => { attachCalls[1].deliver(harness(6, 'e6', 'message.delta', { text: ' and rest' })); attachCalls[1].deliver(harness(7, 'e7', 'turn.completed')); attachCalls[1].finish(); });
  await flush();
  expect(rendered()).toContain('partial and rest');
  expect(stopButtons()).toHaveLength(0);
  expect(status()).not.toContain('Reconnecting');
});

it('settles from the log when the turn finished while detached, without a reconnect', async () => {
  state.turnState
    .mockResolvedValueOnce({ active: true, turnId: 'turn-1', lastSeq: 1 })
    .mockResolvedValue({ active: false, turnId: 'turn-1', lastSeq: 2, endedAt: '2026-09-12T00:00:05.000Z' });
  state.attach.mockImplementationOnce(async (_s: string, _a: number, onEvent: (frame: Frame) => void) => { onEvent(harness(2, 'e2', 'message.delta', { text: 'done text' })); });
  await mountResumed();
  await flush();
  expect(state.attach).toHaveBeenCalledTimes(1);
  expect(rendered()).toContain('done text');
  expect(status()).not.toContain('Reconnecting');
  expect(stopButtons()).toHaveLength(0);
});

it('treats a 404 TURN_NOT_ACTIVE on re-attach as the turn having ended and reads the outcome from the log', async () => {
  vi.useFakeTimers();
  state.turnState.mockResolvedValue({ active: true, turnId: 'turn-1', lastSeq: 3 });
  state.attach
    .mockImplementationOnce(async (_s: string, _a: number, onEvent: (frame: Frame) => void) => { onEvent(harness(3, 'e3', 'message.delta', { text: 'before drop' })); throw new TypeError('network dropped'); })
    .mockRejectedValueOnce(new HarnessApiClientError(404, 'SESSION_NOT_FOUND', 'No active turn', { reason: 'TURN_NOT_ACTIVE' }));
  state.replay.mockResolvedValue({ session: { schemaVersion: 'chirality.session/v3', sessionId: 'resumed' }, events: [persisted('e3', 'message.delta', { text: 'before drop' }), persisted('e4', 'turn.interrupted')] });
  await mountResumed();
  await flush();
  expect(status()).toContain('Reconnecting to the running turn');
  await act(async () => { await vi.advanceTimersByTimeAsync(1_000); });
  await flush();
  expect(state.attach).toHaveBeenCalledTimes(2);
  expect(state.attach.mock.calls[1][1]).toBe(3);
  expect(rendered()).toContain('before drop');
  expect(rendered()).toContain('"data-turn-outcome":"interrupted"');
  expect(stopButtons()).toHaveLength(0);
});

it('renders turn.interrupted the moment it arrives and Stop calls the interrupt route without closing the stream', async () => {
  state.turnState.mockResolvedValue({ active: true, turnId: 'turn-1', lastSeq: 0 });
  let deliver!: (frame: Frame) => void;
  let finish!: () => void;
  state.attach.mockImplementation((_s: string, _a: number, onEvent: (frame: Frame) => void) => new Promise<void>(resolve => { deliver = onEvent; finish = resolve; }));
  await mountResumed();
  await act(async () => stopButtons()[0].props.onClick());
  expect(state.interrupt).toHaveBeenCalledWith({ sessionId: 'resumed' });
  // Still attached: the interruption is confirmed by the Runtime's own event.
  expect(stopButtons()).toHaveLength(1);
  await act(async () => { deliver(harness(1, 'e1', 'turn.interrupted')); });
  expect(rendered()).toContain('Turn interrupted by operator.');
  await act(async () => { finish(); });
  await flush();
  expect(stopButtons()).toHaveLength(0);
  expect(rendered()).not.toContain('Reconnecting');
});

// Item 15: the phases a live turn passes through are reported to the host, a
// lost connection never reads as completion, and Stop is its own phase until
// the Runtime confirms the interruption.
it('leaves a recovered plan execution running when the attach never opens, instead of settling it as unknown', async () => {
  const key = 'chirality.planExecutions.v1:resumed';
  const writes: string[] = [];
  const running = [{ revision: 1, attempt: 1, startedAt: '2026-09-12T00:00:00.000Z', status: 'running', turnId: 'turn-1' }];
  (globalThis as unknown as { window: { localStorage: Storage } }).window.localStorage = {
    getItem: (name: string) => name === key ? JSON.stringify(running) : null,
    setItem: (name: string, value: string) => { if (name === key) writes.push(value); }, removeItem: () => undefined
  } as unknown as Storage;
  state.turnState.mockResolvedValue({ active: true, turnId: 'turn-1', lastSeq: 1, startedAt: '2026-09-12T00:00:00.000Z' });
  state.attach.mockRejectedValue(new Error('stream refused'));
  await mountResumed();
  await flush();
  const settled = writes.map(value => JSON.parse(value) as Array<{ status: string }>);
  expect(settled.flat().every(record => record.status === 'running')).toBe(true);
  expect(rendered()).not.toContain('Turn outcome unknown');
});

it('reports Reconnecting then Outcome unknown when the connection is lost and the log records no ending, keeping the message', async () => {
  vi.useFakeTimers();
  const phases: string[] = [];
  state.turnState.mockResolvedValue({ active: true, turnId: 'turn-1', lastSeq: 3 });
  state.attach
    .mockImplementationOnce(async (_s: string, _a: number, onEvent: (frame: Frame) => void) => { onEvent(harness(3, 'e3', 'message.delta', { text: 'before drop' })); throw new TypeError('network dropped'); })
    .mockRejectedValueOnce(new HarnessApiClientError(404, 'SESSION_NOT_FOUND', 'No active turn', { reason: 'TURN_NOT_ACTIVE' }));
  state.replay.mockResolvedValue({ session: { schemaVersion: 'chirality.session/v3', sessionId: 'resumed' }, events: [persisted('e3', 'message.delta', { text: 'before drop' })] });
  await act(async () => { tree = create(<ChatPanel presentation="woven" resumeConversation={{ requestId: 1, projection: projection('resumed') }} onTurnPhaseChange={phase => phases.push(phase)} />); });
  await flush();
  expect(phases.at(-1)).toBe('reconnecting');
  expect(tree!.root.findByProps({ className: 'chat-runtime-status' }).props['data-turn-phase']).toBe('reconnecting');
  expect(rendered()).not.toContain('Closing this window keeps it running; quitting Chirality stops it.');
  await act(async () => { await vi.advanceTimersByTimeAsync(1_000); });
  await flush();
  expect(rendered()).toContain('before drop');
  expect(rendered()).toContain('"data-turn-outcome":"unknown"');
  expect(rendered()).toContain('Outcome unknown');
  expect(rendered()).not.toContain('"data-turn-outcome":"completed"');
  expect(rendered()).toContain('Turn outcome unknown');
  expect(rendered()).toContain('Nothing was re-sent.');
  expect(phases.at(-1)).toBe('idle');
  expect(stopButtons()).toHaveLength(0);
});

it('settles a lost connection as Completed only when the log records the ending', async () => {
  vi.useFakeTimers();
  state.turnState.mockResolvedValue({ active: true, turnId: 'turn-1', lastSeq: 3 });
  state.attach
    .mockImplementationOnce(async (_s: string, _a: number, onEvent: (frame: Frame) => void) => { onEvent(harness(3, 'e3', 'message.delta', { text: 'before drop' })); throw new TypeError('network dropped'); })
    .mockRejectedValueOnce(new HarnessApiClientError(404, 'SESSION_NOT_FOUND', 'No active turn', { reason: 'TURN_NOT_ACTIVE' }));
  // The log grows while detached: empty at mount, the full record when the turn is settled.
  state.replay
    .mockResolvedValueOnce({ session: { schemaVersion: 'chirality.session/v3', sessionId: 'resumed' }, events: [] })
    .mockResolvedValue({ session: { schemaVersion: 'chirality.session/v3', sessionId: 'resumed' }, events: [persisted('e3', 'message.delta', { text: 'before drop' }), persisted('e4', 'message.delta', { text: ' and after' }), persisted('e5', 'turn.completed')] });
  await mountResumed();
  await act(async () => { await vi.advanceTimersByTimeAsync(1_000); });
  await flush();
  expect(rendered()).toContain('before drop and after');
  expect(rendered()).toContain('"data-turn-outcome":"completed"');
  expect(rendered()).not.toContain('Outcome unknown');
});

it('moves to Stopping on Stop and to Stopped once the Runtime confirms, reporting each phase to the host', async () => {
  const phases: string[] = [];
  state.turnState.mockResolvedValue({ active: true, turnId: 'turn-1', lastSeq: 0 });
  let deliver!: (frame: Frame) => void;
  let finish!: () => void;
  state.attach.mockImplementation((_s: string, _a: number, onEvent: (frame: Frame) => void) => new Promise<void>(resolve => { deliver = onEvent; finish = resolve; }));
  await act(async () => { tree = create(<ChatPanel presentation="woven" resumeConversation={{ requestId: 1, projection: projection('resumed') }} onTurnPhaseChange={phase => phases.push(phase)} />); });
  await flush();
  expect(phases.at(-1)).toBe('reconnecting');
  await act(async () => { deliver({ event: 'transport:connected', data: {} }); });
  expect(phases.at(-1)).toBe('working');
  await act(async () => stopButtons()[0].props.onClick());
  expect(phases.at(-1)).toBe('stopping');
  expect(status()).toContain('Stopping');
  await act(async () => { deliver(harness(1, 'e1', 'turn.interrupted')); finish(); });
  await flush();
  expect(rendered()).toContain('"data-turn-outcome":"interrupted"');
  expect(rendered()).toContain('Stopped');
  expect(phases.at(-1)).toBe('idle');
});


it('returns to Working on a real reattachment with no new model output and retries an initially failed attach', async () => {
  vi.useFakeTimers();
  state.turnState.mockResolvedValue({ active: true, turnId: 'turn-1', lastSeq: 0 });
  let deliver!: (frame: Frame) => void;
  state.attach.mockRejectedValueOnce(new TypeError('Runtime stalled'))
    .mockImplementation((_s: string, _a: number, onEvent: (frame: Frame) => void) => new Promise<void>(() => { deliver = onEvent; }));
  await mountResumed();
  expect(status()).toContain('Reconnecting');
  expect(stopButtons()).toHaveLength(1);
  await act(async () => { await vi.advanceTimersByTimeAsync(1_000); });
  expect(state.attach).toHaveBeenCalledTimes(2);
  expect(status()).toContain('Reconnecting');
  await act(async () => { deliver({ event: 'transport:connected', data: {} }); });
  expect(tree!.root.findByProps({ className: 'turn-activity-summary' }).children.join('')).toBe('Working');
  await act(async () => { await vi.advanceTimersByTimeAsync(70_000); });
  expect(stopButtons()).toHaveLength(1);
  expect(state.stream).not.toHaveBeenCalled();
  expect(state.interrupt).not.toHaveBeenCalled();
});

it.each([
  ['service-shutdown', 'failed'], ['service-restart', 'unknown'], [undefined, 'interrupted']
])('preserves live interruption cause %s across a generic interrupted exit', async (reason, expected) => {
  state.turnState.mockResolvedValue({ active: true, turnId: 'turn-1', lastSeq: 0 });
  state.attach.mockImplementation(async (_s: string, _a: number, onEvent: (frame: Frame) => void) => {
    onEvent(harness(1, 'e1', 'turn.interrupted', reason ? { reason } : {}));
    onEvent({ event: 'process:exit', seq: 2, data: { exitCode: 130, interrupted: true } });
  });
  await mountResumed();
  expect(rendered()).toContain(`"data-turn-outcome":"${expected}"`);
  expect(rendered()).not.toContain('"data-turn-outcome":"completed"');
  if (reason) expect(rendered()).not.toContain('Turn interrupted by operator.');
  expect(state.stream).not.toHaveBeenCalled();
});

it.each([
  ['service-shutdown', 'failed'], ['service-restart', 'unknown'], [undefined, 'interrupted']
])('preserves replay interruption cause %s', async (reason, expected) => {
  const replay = projection('resumed');
  replay.transcript.items.push({ key: 'terminal', kind: 'terminal', status: 'interrupted', title: 'Turn interrupted', timestamp: '2026-09-12T00:00:00Z', eventId: 'end', eventType: 'turn.interrupted', turnId: 'turn-1', ...(reason ? { terminalReason: reason } : {}) });
  await act(async () => { tree = create(<ChatPanel presentation="woven" resumeConversation={{ requestId: 1, projection: replay }} />); });
  await flush();
  expect(rendered()).toContain(`"data-turn-outcome":"${expected}"`);
  if (reason) expect(rendered()).not.toContain('Turn interrupted by operator.');
  expect(state.stream).not.toHaveBeenCalled();
});

it('sends once, recovers by GET after a dropped stream, and retains a service-loss message without restoring the draft', async () => {
  vi.useFakeTimers();
  await mountResumed();
  state.replay.mockResolvedValue({ session: { schemaVersion: 'chirality.session/v3', sessionId: 'resumed' }, events: [], instructionBases: [], instructionHistory: [] });
  state.turnState.mockResolvedValue({ active: true, turnId: 'turn-1', lastSeq: 1 });
  let submittedTurnId!: string;
  state.stream.mockImplementation(async (input: { turnId: string }, onEvent: (frame: Frame) => void) => {
    submittedTurnId = input.turnId;
    const accepted = harness(1, 'accepted', 'turn.accepted');
    onEvent({ ...accepted, data: { ...accepted.data, turnId: submittedTurnId } });
    throw new TypeError('transport dropped');
  });
  state.attach.mockImplementation(async (_s: string, _a: number, onEvent: (frame: Frame) => void) => {
    onEvent({ event: 'transport:connected', data: {} });
    const ended = harness(2, 'ended', 'turn.interrupted', { reason: 'service-shutdown' });
    onEvent({ ...ended, data: { ...ended.data, turnId: submittedTurnId } });
    onEvent({ event: 'process:exit', seq: 3, data: { exitCode: 130, interrupted: true } });
  });
  await act(async () => { tree!.root.findByProps({ 'aria-label': 'Chat input' }).props.onChange({ target: { value: 'Keep this sent message' } }); });
  await act(async () => { tree!.root.findByProps({ className: 'chat-input-row' }).props.onSubmit({ preventDefault: vi.fn() }); });
  await flush();
  expect(state.stream).toHaveBeenCalledTimes(1);
  expect(status()).toContain('Reconnecting');
  await act(async () => { await vi.advanceTimersByTimeAsync(1_000); });
  await flush();
  expect(state.attach).toHaveBeenCalledWith('resumed', 1, expect.any(Function), expect.any(AbortSignal), submittedTurnId);
  expect(state.stream).toHaveBeenCalledTimes(1);
  expect(rendered()).toContain('Keep this sent message');
  expect(rendered()).toContain('"data-turn-outcome":"failed"');
  expect(tree!.root.findByProps({ 'aria-label': 'Chat input' }).props.value).toBe('');
});

it.each([['service-shutdown', 'failed'], ['service-restart', 'unknown']])('settles a failed first reload attachment from this turn’s recorded %s reason', async (reason, expected) => {
  state.turnState.mockResolvedValue({ active: true, turnId: 'turn-1', lastSeq: 1 });
  state.attach.mockRejectedValue(new HarnessApiClientError(404, 'SESSION_NOT_FOUND', 'No active turn', { reason: 'TURN_NOT_ACTIVE' }));
  state.replay.mockResolvedValue({ session: { schemaVersion: 'chirality.session/v3', sessionId: 'resumed' }, events: [persisted('ended', 'turn.interrupted', { reason })] });
  await mountResumed();
  expect(rendered()).toContain(`"data-turn-outcome":"${expected}"`);
  expect(state.stream).not.toHaveBeenCalled();
});

it('does not borrow an older turn’s completion when reload attachment fails before its first frame', async () => {
  state.turnState.mockResolvedValue({ active: true, turnId: 'turn-1', lastSeq: 1 });
  state.attach.mockRejectedValue(new HarnessApiClientError(404, 'SESSION_NOT_FOUND', 'No active turn', { reason: 'TURN_NOT_ACTIVE' }));
  state.replay.mockResolvedValue({ session: { schemaVersion: 'chirality.session/v3', sessionId: 'resumed' }, events: [{ ...persisted('older', 'turn.completed'), turnId: 'turn-0' }] });
  await mountResumed();
  expect(rendered()).toContain('"data-turn-outcome":"unknown"');
  expect(rendered()).not.toContain('"data-turn-outcome":"completed"');
});

it.each(['retained-old', 'expired-old', 'matching', 'matching-replay'])('correlates a fresh POST whose response is lost before any frame: %s', async scenario => {
  vi.useFakeTimers();
  await mountResumed();
  const older = [persisted('old-text', 'message.delta', { text: 'OLD TURN TEXT' }), persisted('old-end', 'turn.completed')]
    .map(event => ({ ...event, turnId: 'previous-turn' }));
  state.replay.mockResolvedValue({ session: { schemaVersion: 'chirality.session/v3', sessionId: 'resumed' }, events: older, instructionHistory: [], instructionBases: [] });
  state.turnState.mockResolvedValue({ active: false, turnId: 'previous-turn', lastSeq: 2 });
  let submitted!: string;
  state.stream.mockImplementation(async (input: { turnId: string }) => {
    submitted = input.turnId;
    if (scenario === 'matching-replay') {
      const current = [persisted('new-text', 'message.delta', { text: 'NEW TURN TEXT' }), persisted('new-end', 'turn.completed')].map(event => ({ ...event, turnId: submitted }));
      state.replay.mockResolvedValue({ session: { schemaVersion: 'chirality.session/v3', sessionId: 'resumed' }, events: [...older, ...current], instructionHistory: [], instructionBases: [] });
    }
    throw new TypeError('POST response lost');
  });
  state.attach.mockImplementation(async (_s: string, _after: number, deliver: (frame: Frame) => void, _signal: AbortSignal, expectedTurnId?: string) => {
    if (scenario === 'matching') {
      const accepted = harness(1, 'new-accepted', 'turn.accepted');
      const ended = harness(3, 'new-end', 'turn.completed');
      deliver({ ...accepted, data: { ...accepted.data, turnId: submitted } });
      deliver({ event: 'chat:delta', seq: 2, data: { text: 'NEW TURN TEXT' } });
      deliver({ ...ended, data: { ...ended.data, turnId: submitted } });
      return;
    }
    if (scenario === 'expired-old' || expectedTurnId !== undefined) {
      throw new HarnessApiClientError(404, 'SESSION_NOT_FOUND', 'No matching retained turn', { reason: 'TURN_NOT_ACTIVE' });
    }
    // The old behavior (unqualified seq-0 attach) would replay this prior turn.
    deliver({ event: 'chat:delta', seq: 1, data: { text: 'OLD TURN TEXT' } });
    deliver({ event: 'process:exit', seq: 2, data: { exitCode: 0 } });
  });
  await act(async () => { tree!.root.findByProps({ 'aria-label': 'Chat input' }).props.onChange({ target: { value: 'Keep exactly this submitted message' } }); });
  await act(async () => { tree!.root.findByProps({ className: 'chat-input-row' }).props.onSubmit({ preventDefault: vi.fn() }); });
  expect(submitted).toEqual(expect.any(String));
  expect(submitted).not.toBe('previous-turn');
  expect(status()).toContain('Reconnecting');
  await act(async () => { await vi.advanceTimersByTimeAsync(1_000); });
  await flush();
  expect(state.attach).toHaveBeenCalledWith('resumed', 0, expect.any(Function), expect.any(AbortSignal), submitted);
  expect(state.stream).toHaveBeenCalledTimes(1);
  expect(rendered()).toContain('Keep exactly this submitted message');
  expect(tree!.root.findByProps({ 'aria-label': 'Chat input' }).props.value).toBe('');
  expect(rendered()).not.toContain('OLD TURN TEXT');
  expect(state.append.mock.calls.some(([event]) => event.turnId === 'previous-turn')).toBe(false);
  if (scenario === 'matching' || scenario === 'matching-replay') {
    expect(rendered()).toContain('NEW TURN TEXT');
    expect(rendered()).toContain('"data-turn-outcome":"completed"');
  } else {
    expect(rendered()).toContain('"data-turn-outcome":"unknown"');
    expect(rendered()).not.toContain('"data-turn-outcome":"completed"');
  }
  expect(state.interrupt).not.toHaveBeenCalled();
});

it.each(['matching', 'different'])('persists an Execute attempt identity before dispatch and retains it across ambiguous response plus reload: %s', async recovery => {
  vi.useFakeTimers();
  const key = 'chirality.planExecutions.v1:resumed';
  const store = new Map<string, string>();
  Object.assign(window, { localStorage: { getItem: (name: string) => store.get(name) ?? null, setItem: (name: string, value: string) => { store.set(name, value); }, removeItem: (name: string) => { store.delete(name); } } });
  const records = () => JSON.parse(store.get(key) ?? '[]') as Array<{ turnId?: string; status: string; revision: number; attempt: number }>;
  const qualification = { adapterId: 'codex-app-server', providerId: 'openai', qualificationId: 'fixture', admissionSha256: 'a'.repeat(64), evidenceClass: 'native-adapter-qualified' as const };
  const revision = { revision: 1, sourceEvent: { qualificationState: 'qualified' as const, eventId: 'plan-1', occurredAt: '2026-09-12T00:00:00Z', qualification, plan: { id: 'plan-item', type: 'plan', text: 'Perform the planned work.' } } };
  state.nativeCapability.mockResolvedValue({ schemaVersion: 'chirality.native-plan-capability/v3', status: 'qualified', qualification });
  state.nativeRevisions.mockResolvedValue({ schemaVersion: 'chirality.native-plan-revisions/v3', status: 'qualified', qualification, revisions: [revision] });
  state.replay.mockResolvedValue({ session: { schemaVersion: 'chirality.session/v3', sessionId: 'resumed' }, events: [], instructionBases: [], instructionHistory: [] });
  const selected = projection('resumed');
  selected.session!.continuation!.interactionMode = 'native-plan';
  let model: import('../../components/shell/native-plan-panel').NativePlanPanelModel | null = null;
  await act(async () => { tree = create(<ChatPanel presentation="woven" resumeConversation={{ requestId: 1, projection: selected }} onPlanPanelChange={value => { model = value; }} />); });
  await flush();
  await act(async () => { model!.onExecute(revision); });
  let submitted!: string;
  let persistedAtDispatch: ReturnType<typeof records> = [];
  state.stream.mockImplementation(async (input: { turnId: string }) => {
    submitted = input.turnId;
    // Capture at dispatch, before any response, frame, or later effect. Assert
    // outside the handler so the observer cannot swallow an assertion failure.
    persistedAtDispatch = records();
    throw new TypeError('Execute POST response lost');
  });
  await act(async () => { tree!.root.findByProps({ className: 'chat-input-row' }).props.onSubmit({ preventDefault: vi.fn() }); });
  await flush();
  expect(state.stream).toHaveBeenCalledTimes(1);
  expect(status()).toContain('Reconnecting');
  expect(persistedAtDispatch).toEqual([expect.objectContaining({ revision: 1, attempt: 1, status: 'running', turnId: submitted })]);
  expect(records()[0]).toMatchObject({ status: 'running', turnId: submitted });
  // Reload before the observer's first retry/settlement. Keep only persisted state.
  await act(async () => { tree!.unmount(); });
  tree = undefined;
  await flush();
  expect(records()[0]).toMatchObject({ status: 'running', turnId: submitted });
  const observed = recovery === 'matching' ? submitted : 'prior-active-turn';
  state.turnState.mockResolvedValue({ active: true, turnId: observed, lastSeq: 1 });
  state.attach.mockImplementation(async (_s: string, _after: number, deliver: (frame: Frame) => void) => {
    const ended = harness(1, 'reloaded-end', 'turn.completed');
    deliver({ ...ended, data: { ...ended.data, turnId: observed } });
  });
  await mountResumed();
  expect(records()[0]).toMatchObject({ turnId: submitted, status: recovery === 'matching' ? 'completed' : 'unknown' });
  expect(state.stream).toHaveBeenCalledTimes(1);
  expect(tree!.root.findByProps({ 'aria-label': 'Chat input' }).props.value).toBe('');
});

it('never adopts a recovered live turn identity or completion for a legacy idless plan attempt', async () => {
  const key = 'chirality.planExecutions.v1:resumed';
  let saved = JSON.stringify([{ revision: 1, attempt: 1, startedAt: '2026-09-12T00:00:00Z', status: 'running' }]);
  Object.assign(window, { localStorage: { getItem: (name: string) => name === key ? saved : null, setItem: (name: string, value: string) => { if (name === key) saved = value; }, removeItem: () => undefined } });
  state.turnState.mockResolvedValue({ active: true, turnId: 'turn-1', lastSeq: 1 });
  state.attach.mockImplementation(async (_s: string, _after: number, deliver: (frame: Frame) => void) => { deliver(harness(1, 'other-end', 'turn.completed')); });
  await mountResumed();
  expect(JSON.parse(saved)).toEqual([expect.objectContaining({ status: 'unknown' })]);
  expect(JSON.parse(saved)[0].turnId).toBeUndefined();
  expect(state.stream).not.toHaveBeenCalled();
});


it('keeps native commentary and final items separate and replaces their completed snapshots without legacy duplicates', async () => {
  state.turnState.mockResolvedValue({ active: true, turnId: 'turn-1', lastSeq: 0 });
  let deliver!: (frame: Frame) => void;
  state.attach.mockImplementation((_s: string, _a: number, onEvent: (frame: Frame) => void) => { deliver = onEvent; return new Promise(() => {}); });
  await mountResumed();
  const native = (seq: number, id: string, phase: string, text: string) => harness(seq, `n${seq}`, 'codex.notification', {
    method: 'item/completed', params: { threadId: 'primary', turnId: 'native-turn', item: { type: 'agentMessage', id, phase, text } }, codex: { isPrimaryThread: true, providerThreadId: 'primary' }
  });
  await act(async () => {
    deliver(harness(1, 'legacy', 'message.delta', { text: 'joined legacy text' }));
    deliver(native(2, 'comment', 'commentary', 'I will inspect it.'));
    deliver(native(3, 'final', 'final_answer', 'The answer.'));
    deliver(native(4, 'final', 'final_answer', 'The complete answer.'));
    deliver({ event: 'chat:complete', data: { text: 'joined legacy text' } });
  });
  const commentary = tree!.root.findByProps({ 'data-message-phase': 'commentary' });
  const final = tree!.root.findByProps({ 'data-message-phase': 'final_answer' });
  expect(JSON.stringify(commentary.children.map(node => typeof node === 'string' ? node : node.props))).toContain('I will inspect it.');
  expect(rendered()).toContain('The complete answer.');
  expect(rendered()).not.toContain('joined legacy text');
  expect(final.props['data-role']).toBe('assistant');
});

it.each(['accepted', 'rejected', 'unknown'] as const)('steers the owned Runtime turn and preserves unconfirmed drafts: %s', async status => {
  state.turnState.mockResolvedValue({ active: true, turnId: 'turn-1', lastSeq: 0 });
  state.attach.mockImplementation((_sessionId, _after, onEvent) => { onEvent({ event: 'transport:connected', data: {} }); return new Promise(() => {}); });
  state.steer.mockImplementation(async (_sessionId, request) => ({ operationId: request.operationId, turnId: request.expectedTurnId, status }));
  await mountResumed();
  await act(async () => tree!.root.findByProps({ 'aria-label': 'Chat input' }).props.onChange({ target: { value: 'Use the small example.' } }));
  await act(async () => tree!.root.findByType('form').props.onSubmit({ preventDefault() {} }));
  await flush();
  expect(state.steer).toHaveBeenCalledWith('resumed', { operationId: expect.any(String), expectedTurnId: 'turn-1', text: 'Use the small example.' });
  expect(state.stream).not.toHaveBeenCalled();
  expect(state.interrupt).not.toHaveBeenCalled();
  expect(tree!.root.findByProps({ 'aria-label': 'Chat input' }).props.value).toBe(status === 'accepted' ? '' : 'Use the small example.');
  if (status === 'unknown') expect(tree!.root.findByProps({ 'aria-label': 'Update running turn' }).props.disabled).toBe(true);
});

it('keeps background Plan reads quiet and shows busy only for a manual refresh', async () => {
  vi.useFakeTimers();
  state.nativeCapability.mockResolvedValue({ schemaVersion: 'chirality.native-plan-capability/v3', status: 'qualified', qualification: { adapterId: 'fixture', providerId: 'fixture', qualificationId: 'qualified-fixture', admissionSha256: 'a'.repeat(64), evidenceClass: 'native-adapter-qualified' } });
  const projected = projection('resumed');
  projected.session!.continuation!.interactionMode = 'native-plan';
  state.turnState.mockResolvedValue({ active: true, turnId: 'turn-1', lastSeq: 0 });
  state.attach.mockImplementation(() => new Promise(() => {}));
  let model: import('../../components/shell/native-plan-panel').NativePlanPanelModel | null = null;
  await act(async () => { tree = create(<ChatPanel presentation="woven" resumeConversation={{ requestId: 1, projection: projected }} onPlanPanelChange={next => { model = next; }} />); });
  await flush();
  expect(model!.refreshing).toBe(false);
  let complete!: (value: unknown) => void;
  state.nativeRevisions.mockImplementation(() => new Promise(resolve => { complete = resolve; }));
  await act(async () => { await vi.advanceTimersByTimeAsync(1000); });
  expect(model!.refreshing).toBe(false);
  await act(async () => model!.onRefresh());
  expect(model!.refreshing).toBe(true);
  await act(async () => complete({ revisions: [] }));
  expect(model!.refreshing).toBe(false);
});


it('checks a late steering receipt using the original identity without submitting text again', async () => {
  state.turnState.mockResolvedValue({ active: true, turnId: 'turn-1', lastSeq: 0 });
  state.attach.mockImplementation((_s, _after, onEvent) => { onEvent({ event: 'transport:connected', data: {} }); return new Promise(() => {}); });
  state.steer.mockImplementation(async (_s, request) => ({ operationId: request.operationId, turnId: request.expectedTurnId, status: 'unknown' }));
  state.receipt.mockImplementation(async (_s, request) => ({ operationId: request.operationId, turnId: request.expectedTurnId, status: 'accepted', message: 'Confirmed from late native echo.' }));
  await mountResumed();
  await act(async () => tree!.root.findByProps({ 'aria-label': 'Chat input' }).props.onChange({ target: { value: 'Original correction' } }));
  await act(async () => tree!.root.findByType('form').props.onSubmit({ preventDefault() {} }));
  const original = state.steer.mock.calls[0][1];
  await act(async () => tree!.root.findAllByType('button').find(button => button.children.includes('Check delivery'))!.props.onClick());
  await flush();
  expect(state.receipt).toHaveBeenCalledWith('resumed', { operationId: original.operationId, expectedTurnId: original.expectedTurnId });
  expect(state.steer).toHaveBeenCalledTimes(1);
  expect(state.stream).not.toHaveBeenCalled();
  expect(tree!.root.findByProps({ 'aria-label': 'Chat input' }).props.value).toBe('');
  expect(rendered()).toContain('Update received');
});

it('recovers a network-before-intent unknown after reload and checks safely after turn completion', async () => {
  const saved = new Map<string, string>();
  window.localStorage = { getItem: key => saved.get(key) ?? null, setItem: (key, value) => { saved.set(key, value); }, removeItem: key => { saved.delete(key); } } as Storage;
  state.turnState.mockResolvedValue({ active: true, turnId: 'turn-1', lastSeq: 0 });
  state.attach.mockImplementation((_s, _after, onEvent) => { onEvent({ event: 'transport:connected', data: {} }); return new Promise(() => {}); });
  state.steer.mockRejectedValue(new TypeError('Network failed before server intent'));
  state.receipt.mockImplementation(async (_s, request) => ({ operationId: request.operationId, turnId: request.expectedTurnId, status: 'unknown', message: 'No recorded intent. Nothing was sent by this check.' }));
  await mountResumed();
  await act(async () => tree!.root.findByProps({ 'aria-label': 'Chat input' }).props.onChange({ target: { value: 'Locally retained correction' } }));
  await act(async () => tree!.root.findByType('form').props.onSubmit({ preventDefault() {} }));
  const original = state.steer.mock.calls[0][1];
  act(() => tree!.unmount()); tree = undefined;
  state.turnState.mockResolvedValue({ active: false, turnId: 'turn-1', lastSeq: 10 });
  await mountResumed();
  const check = () => tree!.root.findAllByType('button').find(button => button.children.includes('Check delivery'))!;
  await act(async () => check().props.onClick());
  await flush();
  expect(state.receipt).toHaveBeenLastCalledWith('resumed', { operationId: original.operationId, expectedTurnId: 'turn-1' });
  expect(tree!.root.findByProps({ 'aria-label': 'Send' }).props.disabled).toBe(true);
  expect(tree!.root.findByProps({ 'aria-label': 'Chat input' }).props.value).toBe('Locally retained correction');
  expect(rendered()).toContain('No recorded intent');
  // A later explicit check may find durable confirmation, even after the turn ended.
  state.receipt.mockImplementation(async (_s, request) => ({ operationId: request.operationId, turnId: request.expectedTurnId, status: 'accepted' }));
  await act(async () => check().props.onClick());
  await flush();
  expect(tree!.root.findByProps({ 'aria-label': 'Chat input' }).props.value).toBe('');
  expect(state.steer).toHaveBeenCalledTimes(1);
  expect(state.stream).not.toHaveBeenCalled();
});

it('recovers the expected Runtime turn from durable steering evidence without local receipt state', async () => {
  const projected = projection('resumed');
  projected.events = [persisted('steer-original', 'codex.steer', { operationId: 'original-operation', expectedTurnId: 'turn-1', text: 'Original text', status: 'unknown' })] as import('@chirality/runtime-contracts/event-schema').HarnessEvent[];
  state.receipt.mockResolvedValue({ operationId: 'original-operation', turnId: 'turn-1', status: 'unknown' });
  await act(async () => { tree = create(<ChatPanel presentation="woven" resumeConversation={{ requestId: 1, projection: projected }} />); });
  await act(async () => tree!.root.findAllByType('button').find(button => button.children.includes('Check delivery'))!.props.onClick());
  await flush();
  expect(state.receipt).toHaveBeenCalledWith('resumed', { operationId: 'original-operation', expectedTurnId: 'turn-1' });
  expect(state.steer).not.toHaveBeenCalled();
  expect(rendered()).toContain('unconfirmed');
});

it.each(['accepted', 'rejected'] as const)('expires the %s update notice at turn completion while retaining durable history', async receiptStatus => {
  let deliver!: (frame: Frame) => void; let finish!: () => void;
  state.turnState.mockResolvedValue({ active: true, turnId: 'turn-1', lastSeq: 0 });
  state.attach.mockImplementation((_s: string, _after: number, onEvent: (frame: Frame) => void) => new Promise<void>(resolve => { deliver = onEvent; finish = resolve; onEvent({ event: 'transport:connected', data: {} }); }));
  state.steer.mockImplementation(async (_s, request) => {
    deliver(harness(2, 'steer-result', 'codex.steer', { ...request, status: receiptStatus }));
    return { operationId: request.operationId, turnId: request.expectedTurnId, status: receiptStatus };
  });
  await mountResumed();
  await act(async () => tree!.root.findByProps({ 'aria-label': 'Chat input' }).props.onChange({ target: { value: 'Use the small example.' } }));
  await act(async () => tree!.root.findByType('form').props.onSubmit({ preventDefault() {} }));
  expect(tree!.root.findByProps({ 'aria-label': 'Update running turn' }).props.className).toBe('chat-submit-update');
  expect(tree!.root.findByType('form').findAllByProps({ className: 'chat-steer-receipt' })).toHaveLength(1);
  await act(async () => { deliver(harness(3, 'end', 'turn.completed')); finish(); }); await flush();
  expect(tree!.root.findAllByProps({ className: 'chat-steer-receipt' })).toHaveLength(0);
  expect(rendered()).toContain(receiptStatus === 'accepted' ? 'Update received' : 'Update rejected');
  expect(rendered()).toContain('Use the small example.');
});

it.each(['accepted', 'rejected'] as const)('restores %s steering as history without reviving its notice on the next turn', async receiptStatus => {
  const { deriveTranscriptView } = await import('@chirality/runtime-contracts/transcript-replay');
  const projected = projection('resumed');
  projected.events = [persisted('old-update', 'codex.steer', { operationId: 'old-operation', expectedTurnId: 'turn-1', text: 'An earlier update', status: receiptStatus })] as import('@chirality/runtime-contracts/event-schema').HarnessEvent[];
  projected.transcript = deriveTranscriptView(projected.events);
  state.turnState.mockResolvedValue({ active: false, lastSeq: 0 });
  await act(async () => { tree = create(<ChatPanel presentation="woven" resumeConversation={{ requestId: 1, projection: projected }} />); }); await flush();
  expect(rendered()).toContain('An earlier update');
  expect(rendered()).toContain(receiptStatus === 'accepted' ? 'Update received' : 'Update rejected');
  expect(tree!.root.findAllByProps({ className: 'chat-steer-receipt' })).toHaveLength(0);
  await act(async () => tree!.update(<ChatPanel presentation="woven" resumeConversation={{ requestId: 2, projection: projection('other') }} />)); await flush();
  expect(rendered()).not.toContain('An earlier update');
  state.turnState.mockResolvedValue({ active: true, turnId: 'turn-2', lastSeq: 0 });
  state.attach.mockImplementation((_s: string, _after: number, onEvent: (frame: Frame) => void) => { onEvent({ event: 'transport:connected', data: {} }); return new Promise(() => {}); });
  await act(async () => tree!.update(<ChatPanel presentation="woven" resumeConversation={{ requestId: 3, projection: projected }} />)); await flush();
  expect(tree!.root.findByProps({ 'aria-label': 'Update running turn' })).toBeDefined();
  expect(rendered()).toContain('An earlier update');
  expect(tree!.root.findAllByProps({ className: 'chat-steer-receipt' })).toHaveLength(0);
});
