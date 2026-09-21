import React from 'react';
import { act, create, type ReactTestRenderer } from 'react-test-renderer';
import { afterEach, beforeEach, expect, it, vi } from 'vitest';

const api = vi.hoisted(() => ({ get: vi.fn(), initialize: vi.fn(), start: vi.fn(), cancel: vi.fn(), signOut: vi.fn() }));
const openWindow = vi.hoisted(() => vi.fn());
vi.mock('../../lib/harness/hosted-bootstrap-client', () => ({
  hydrateHostedBootstrapProject: (root: string, _onBound: unknown, signal: AbortSignal) => api.get(root, signal),
  getHostedBootstrapStatus: api.get,
  getHostedBootstrapStatusWithRetry: api.get,
  initializeHostedBootstrapProject: api.initialize,
  startHostedBootstrapLogin: api.start,
  cancelHostedBootstrapLogin: api.cancel,
  signOutHostedBootstrapProject: api.signOut
}));
// The controller reads the shared connectivity snapshot to re-read status on a
// reconnect. `null` is the no-bridge case every other test here runs under.
const connectivity = vi.hoisted(() => ({ current: null as null | { state: 'connecting' | 'connected' | 'disconnected'; failedAttempts: number; lastError: string | null; changedAt: string } }));
vi.mock('../../components/shell/runtime-connectivity-provider', () => ({
  useRuntimeConnectivitySnapshot: () => connectivity.current
}));

import { useHostedBootstrapController, type HostedBootstrapController } from '../../components/settings/hosted-bootstrap-controller';
import { HostedBootstrapView, hostedBootstrapSummary } from '../../components/settings/hosted-bootstrap-view';
import { WorkspaceProvider, useWorkspace } from '../../components/workspace/workspace-provider';

const root = '/projects/example';
const status = (ceremony: 'ready-to-start' | 'pending' | 'signed-in' | 'failed' | 'cancelled', admission: 'unavailable' | 'establishing' | 'ready' = 'unavailable') => ({
  schema: 'chirality-hosted-bootstrap-status/v1' as const,
  projectId: 'example', ceremony, admission,
  canStartLogin: ['ready-to-start', 'failed', 'cancelled'].includes(ceremony)
});
const registered = (ceremony: Parameters<typeof status>[0], admission?: Parameters<typeof status>[1]) => ({ registration: 'registered' as const, projectId: 'example', status: status(ceremony, admission) });
const binding = { registration: 'registered' as const, projectId: 'example' };
function deferred<T>() {
  let resolve!: (value: T) => void;
  const promise = new Promise<T>(done => { resolve = done; });
  return { promise, resolve };
}

let tree: ReactTestRenderer;
let latest!: HostedBootstrapController;
function Fixture({ projectRoot = root, refresh = () => {} }: { projectRoot?: string | null; refresh?: () => void }): JSX.Element {
  latest = useHostedBootstrapController(projectRoot, refresh);
  return <HostedBootstrapView controller={latest} />;
}
const text = (): string => JSON.stringify(tree.toJSON());
const button = (label: string) => tree.root.findAllByType('button').find(node => node.children.join('') === label)!;

let workspace!: ReturnType<typeof useWorkspace>;
function WorkspaceFixture({ refresh = () => {} }: { refresh?: () => void }): JSX.Element {
  workspace = useWorkspace();
  latest = useHostedBootstrapController(workspace.projectRoot, refresh);
  return <HostedBootstrapView controller={latest} />;
}
function installWorkspaceHost(stored: string | null): void {
  // WorkspaceProvider relies on the app's JSX runtime; this suite compiles JSX classically.
  vi.stubGlobal('React', React);
  vi.stubGlobal('window', {
    setInterval: (...args: Parameters<typeof globalThis.setInterval>) => globalThis.setInterval(...args),
    clearInterval: (timer: ReturnType<typeof globalThis.setInterval>) => globalThis.clearInterval(timer),
    localStorage: { getItem: () => stored, setItem: () => undefined, removeItem: () => undefined }
  });
  vi.stubGlobal('fetch', vi.fn(async (_url: string, init: RequestInit) => new Response(
    JSON.stringify({ ok: true, projectRoot: JSON.parse(String(init.body)).projectRoot }),
    { status: 200 }
  )));
}
async function settle(): Promise<void> {
  await act(async () => { await Promise.resolve(); await Promise.resolve(); await Promise.resolve(); });
}

beforeEach(() => {
  vi.clearAllMocks();
  vi.stubGlobal('window', { setInterval: (...args: Parameters<typeof globalThis.setInterval>) => globalThis.setInterval(...args), clearInterval: (timer: ReturnType<typeof globalThis.setInterval>) => globalThis.clearInterval(timer), open: openWindow });
  api.get.mockResolvedValue({ registration: 'required' });
});
afterEach(() => { tree?.unmount(); vi.useRealTimers(); vi.unstubAllGlobals(); });

it('requires an explicit project setup and sign-in before exposing the validated provider URL', async () => {
  const refresh = vi.fn();
  await act(async () => { tree = create(<Fixture refresh={refresh} />); });
  await act(async () => { await Promise.resolve(); });
  expect(text()).toContain('Use this folder');
  // The explanation is hover/accessible detail on the action, not a visible paragraph.
  expect(button('Use this folder').props.title).toContain('one minimal');
  expect(tree.root.findAllByType('p').filter(node => node.props.className !== 'api-key-status')).toHaveLength(0);
  expect(tree.root.findAllByType('a')).toHaveLength(0);

  api.initialize.mockResolvedValue(binding);
  api.get.mockResolvedValue(registered('ready-to-start'));
  await act(async () => { button('Use this folder').props.onClick(); await Promise.resolve(); await Promise.resolve(); await Promise.resolve(); });
  expect(refresh).toHaveBeenCalledTimes(1);
  expect(api.initialize).toHaveBeenCalledWith(root, expect.any(AbortSignal));
  expect(api.get).toHaveBeenLastCalledWith(root, expect.any(AbortSignal));
  expect(api.get.mock.invocationCallOrder.at(-1)!).toBeGreaterThan(api.initialize.mock.invocationCallOrder[0]!);
  // No provider-network consent step exists: setup leads straight to sign-in.
  expect(text()).not.toContain('Allow provider network');
  expect(text()).toContain('Sign in');
  api.start.mockResolvedValue({ loginId: 'login-1', authUrl: 'https://auth.openai.example/login-1' });
  api.get.mockResolvedValue(registered('pending', 'establishing'));
  await act(async () => { button('Sign in with your ChatGPT account').props.onClick(); await Promise.resolve(); await Promise.resolve(); });
  // One action: the browser opens on the validated URL as soon as Codex returns it.
  expect(openWindow).toHaveBeenCalledExactlyOnceWith('https://auth.openai.example/login-1', '_blank', 'noopener,noreferrer');
  expect(tree.root.findAllByType('a')).toHaveLength(0);
  expect(text()).toContain('Waiting for sign-in');
  expect(button('Open sign-in page again')).toBeDefined();
  expect(button('Cancel')).toBeDefined();
  expect(tree.root.findByProps({ role: 'status' }).children.join('')).toContain('Finish signing in with your ChatGPT account');
  expect(tree.root.findAllByType('p').filter(node => node.props.className !== 'api-key-status' && node.props.role !== 'status')).toHaveLength(0);
  await act(async () => { button('Open sign-in page again').props.onClick(); });
  expect(openWindow).toHaveBeenCalledTimes(2);

  api.cancel.mockResolvedValue(status('cancelled'));
  await act(async () => { button('Cancel').props.onClick(); await Promise.resolve(); await Promise.resolve(); });
  expect(tree.root.findAllByType('button').some(node => node.children.join('') === 'Open sign-in page again')).toBe(false);
  expect(text()).toContain('previous sign-in was cancelled');
});

it('publishes the verified binding before the status read and never takes status from setup', async () => {
  const refresh = vi.fn();
  const statusRead = deferred<ReturnType<typeof registered>>();
  api.initialize.mockResolvedValue(binding);
  await act(async () => { tree = create(<Fixture refresh={refresh} />); });
  await settle();
  api.get.mockReturnValueOnce(statusRead.promise);
  await act(async () => { button('Use this folder').props.onClick(); await Promise.resolve(); await Promise.resolve(); });
  expect(refresh).toHaveBeenCalledTimes(1);
  expect(button('Setting up…').props.disabled).toBe(true);
  await act(async () => { statusRead.resolve(registered('signed-in', 'ready')); await Promise.resolve(); await Promise.resolve(); });
  expect(text()).toContain('Codex is ready.');
  expect(refresh).toHaveBeenCalledTimes(2);
});

it('surfaces a failed status read after setup and keeps the manual action available', async () => {
  const refresh = vi.fn();
  api.initialize.mockResolvedValue(binding);
  await act(async () => { tree = create(<Fixture refresh={refresh} />); });
  await settle();
  api.get.mockRejectedValueOnce(new Error('Hosted account service is unavailable.'));
  await act(async () => { button('Use this folder').props.onClick(); await Promise.resolve(); await Promise.resolve(); await Promise.resolve(); });
  expect(refresh).toHaveBeenCalledTimes(1);
  expect(text()).toContain('Hosted account service is unavailable.');
  expect(text()).toContain('Use this folder');
  expect(api.initialize).toHaveBeenCalledOnce();
});

it('sets up an explicitly selected folder once and reports a failure without retrying', async () => {
  installWorkspaceHost(null);
  const refresh = vi.fn();
  api.initialize.mockRejectedValueOnce(new Error('Folder is not writable'));
  await act(async () => { tree = create(<WorkspaceProvider><WorkspaceFixture refresh={refresh} /></WorkspaceProvider>); });
  await settle();
  expect(api.get).not.toHaveBeenCalled();

  await act(async () => { await workspace.applyProjectRoot('/projects/picked'); });
  await settle();
  expect(api.get).toHaveBeenCalledTimes(1);
  expect(api.initialize).toHaveBeenCalledTimes(1);
  expect(api.initialize).toHaveBeenCalledWith('/projects/picked', expect.any(AbortSignal));
  expect(text()).toContain('Folder is not writable');
  expect(text()).toContain('Use this folder');
  expect(refresh).not.toHaveBeenCalled();
  await settle();
  expect(api.initialize).toHaveBeenCalledTimes(1);

  api.initialize.mockResolvedValue(binding);
  api.get.mockResolvedValue(registered('ready-to-start'));
  await act(async () => { button('Use this folder').props.onClick(); await Promise.resolve(); await Promise.resolve(); await Promise.resolve(); });
  expect(api.initialize).toHaveBeenCalledTimes(2);
  expect(text()).toContain('Sign in');
  expect(text()).not.toContain('Allow provider network');
  expect(refresh).toHaveBeenCalledTimes(1);
});

it('sets up a newly picked unregistered folder automatically and republishes on re-selection only', async () => {
  installWorkspaceHost(null);
  const refresh = vi.fn();
  api.initialize.mockResolvedValue(binding);
  await act(async () => { tree = create(<WorkspaceProvider><WorkspaceFixture refresh={refresh} /></WorkspaceProvider>); });
  await settle();

  api.get.mockResolvedValueOnce({ registration: 'required' }).mockResolvedValue(registered('ready-to-start'));
  await act(async () => { await workspace.applyProjectRoot('/projects/picked'); });
  await settle();
  expect(api.initialize).toHaveBeenCalledTimes(1);
  expect(text()).toContain('Sign in');
  expect(text()).not.toContain('Allow provider network');
  expect(refresh).toHaveBeenCalledTimes(1);

  await act(async () => { await workspace.applyProjectRoot('/projects/picked'); });
  await settle();
  expect(api.initialize).toHaveBeenCalledTimes(1);
});

it('does not set up a root restored from storage on startup', async () => {
  installWorkspaceHost('/projects/restored');
  const refresh = vi.fn();
  await act(async () => { tree = create(<WorkspaceProvider><WorkspaceFixture refresh={refresh} /></WorkspaceProvider>); });
  await settle();
  expect(workspace.projectRoot).toBe('/projects/restored');
  expect(workspace.lastSelection).toBeNull();
  expect(api.get).toHaveBeenCalledWith('/projects/restored', expect.any(AbortSignal));
  expect(api.initialize).not.toHaveBeenCalled();
  expect(text()).toContain('Use this folder');
});

it('keeps setup available after a binding conflict and surfaces the error without changing files implicitly', async () => {
  api.get.mockRejectedValue(new Error('Another working root is currently bound'));
  await act(async () => { tree = create(<Fixture />); });
  await act(async () => { await Promise.resolve(); });
  expect(text()).toContain('Another working root is currently bound');
  expect(text()).toContain('Use this folder');
  expect(api.initialize).not.toHaveBeenCalled();
});

it('does not restart hydration when the caller supplies a new refresh callback', async () => {
  await act(async () => { tree = create(<Fixture refresh={() => {}} />); });
  await act(async () => { await Promise.resolve(); });
  expect(api.get).toHaveBeenCalledOnce();

  await act(async () => { tree.update(<Fixture refresh={() => {}} />); });
  await act(async () => { await Promise.resolve(); });
  expect(api.get).toHaveBeenCalledOnce();
});

it('distinguishes signed-in state from readiness and publishes the ready transition once', async () => {
  vi.useFakeTimers();
  const refresh = vi.fn();
  api.get.mockResolvedValue(registered('signed-in', 'establishing'));
  await act(async () => { tree = create(<Fixture refresh={refresh} />); });
  await act(async () => { await Promise.resolve(); });
  expect(hostedBootstrapSummary(latest)).toBe('Signed in · Preparing engine');
  expect(button('Sign out').props.title).toContain('still preparing');
  expect(refresh).toHaveBeenCalledTimes(1);

  api.get.mockResolvedValue(registered('signed-in', 'ready'));
  await act(async () => { await vi.advanceTimersByTimeAsync(1000); });
  expect(hostedBootstrapSummary(latest)).toBe('Signed in · Ready to work');
  expect(button('Sign out').props.title).toContain('Codex is ready.');
  expect(refresh).toHaveBeenCalledTimes(2);
});

it('never exposes identity, private paths, or digests in hosted status presentation', async () => {
  api.get.mockResolvedValue(registered('signed-in', 'ready'));
  await act(async () => { tree = create(<Fixture />); });
  await act(async () => { await Promise.resolve(); });
  expect(text()).not.toMatch(/email|token|digest|CODEX_HOME|\.codex/i);
});

it('rejects a late A result across an A to B to A root cycle', async () => {
  const firstA = deferred<typeof binding>();
  let actionSignal!: AbortSignal;
  api.initialize.mockImplementation((_projectRoot: string, signal: AbortSignal) => { actionSignal = signal; return firstA.promise; });
  const refresh = vi.fn();
  await act(async () => { tree = create(<Fixture projectRoot="/projects/a" refresh={refresh} />); });
  await act(async () => { await Promise.resolve(); });
  await act(async () => button('Use this folder').props.onClick());
  await act(async () => tree.update(<Fixture projectRoot="/projects/b" refresh={refresh} />));
  await act(async () => tree.update(<Fixture projectRoot="/projects/a" refresh={refresh} />));
  await act(async () => { await Promise.resolve(); });
  expect(text()).toContain('Use this folder');
  await act(async () => { firstA.resolve(binding); await Promise.resolve(); await Promise.resolve(); });
  expect(actionSignal.aborted).toBe(true);
  expect(text()).toContain('Use this folder');
  expect(text()).not.toContain('Ready to work');
  expect(refresh).not.toHaveBeenCalled();
});

it('aborts a pending action on unmount without publishing its late result', async () => {
  const setup = deferred<typeof binding>();
  let actionSignal!: AbortSignal;
  api.initialize.mockImplementation((_projectRoot: string, signal: AbortSignal) => { actionSignal = signal; return setup.promise; });
  const refresh = vi.fn();
  await act(async () => { tree = create(<Fixture refresh={refresh} />); });
  await act(async () => { await Promise.resolve(); });
  await act(async () => button('Use this folder').props.onClick());
  await act(async () => tree.unmount());
  expect(actionSignal.aborted).toBe(true);
  await act(async () => { setup.resolve(binding); await Promise.resolve(); });
  expect(refresh).not.toHaveBeenCalled();
});

it('does not let an in-flight pending poll overwrite a completed cancellation', async () => {
  vi.useFakeTimers();
  const poll = deferred<ReturnType<typeof registered>>();
  let pollSignal!: AbortSignal;
  api.get.mockResolvedValueOnce(registered('pending', 'establishing')).mockImplementationOnce((_root: string, signal: AbortSignal) => {
    pollSignal = signal;
    return poll.promise;
  });
  api.cancel.mockResolvedValue(status('cancelled'));
  await act(async () => { tree = create(<Fixture />); });
  await act(async () => { await Promise.resolve(); });
  await act(async () => { vi.advanceTimersByTime(1000); await Promise.resolve(); });
  await act(async () => { button('Cancel').props.onClick(); await Promise.resolve(); await Promise.resolve(); });
  expect(pollSignal.aborted).toBe(true);
  expect(text()).toContain('previous sign-in was cancelled');
  await act(async () => { poll.resolve(registered('pending', 'establishing')); await Promise.resolve(); await Promise.resolve(); });
  expect(text()).toContain('previous sign-in was cancelled');
  expect(text()).not.toContain('Waiting for sign-in');
});

it('resumes pending status polling after cancellation fails', async () => {
  vi.useFakeTimers();
  const refresh = vi.fn();
  // Hydrate, the re-read after the failed cancel (still pending), then the poll.
  api.get.mockResolvedValueOnce(registered('pending', 'establishing')).mockResolvedValueOnce(registered('pending', 'establishing')).mockResolvedValue(registered('signed-in', 'ready'));
  api.cancel.mockRejectedValue(new Error('Cancellation transport failed'));
  await act(async () => { tree = create(<Fixture refresh={refresh} />); });
  await act(async () => { await Promise.resolve(); });
  await act(async () => { button('Cancel').props.onClick(); await Promise.resolve(); await Promise.resolve(); await Promise.resolve(); });
  expect(api.get).toHaveBeenCalledTimes(2);
  expect(text()).toContain('Cancellation transport failed');
  expect(text()).toContain('Waiting for sign-in');
  await act(async () => { await vi.advanceTimersByTimeAsync(1000); });
  expect(text()).toContain('Signed in · Ready to work');
  expect(text()).not.toContain('Cancellation transport failed');
  expect(refresh).toHaveBeenCalledTimes(2);
});

it('keeps the login link, cancellation, and polling when status reconciliation fails after start', async () => {
  vi.useFakeTimers();
  api.get
    .mockResolvedValueOnce(registered('ready-to-start'))
    .mockRejectedValueOnce(new Error('Status reconciliation failed'))
    .mockResolvedValue(registered('signed-in', 'ready'));
  api.start.mockResolvedValue({ loginId: 'login-recovery', authUrl: 'https://auth.openai.example/login-recovery' });
  await act(async () => { tree = create(<Fixture />); });
  await act(async () => { await Promise.resolve(); });
  await act(async () => { button('Sign in with your ChatGPT account').props.onClick(); await Promise.resolve(); await Promise.resolve(); });
  expect(text()).toContain('Waiting for sign-in');
  expect(text()).toContain('Status reconciliation failed');
  expect(latest.snapshot?.registration === 'registered' ? latest.snapshot.status.admission : null).toBe('unavailable');
  expect(button('Cancel')).toBeDefined();
  expect(openWindow).toHaveBeenLastCalledWith('https://auth.openai.example/login-recovery', '_blank', 'noopener,noreferrer');
  expect(button('Open sign-in page again')).toBeDefined();
  expect(tree.root.findAllByType('button').some(node => node.children.join('') === 'Sign in with your ChatGPT account')).toBe(false);

  await act(async () => { await vi.advanceTimersByTimeAsync(1000); });
  expect(text()).toContain('Signed in · Ready to work');
  expect(text()).not.toContain('Status reconciliation failed');
  expect(tree.root.findAllByType('button').some(node => node.children.join('') === 'Open sign-in page again')).toBe(false);
});

it('signs out Chirality only and republishes readiness after a new sign-in', async () => {
  const refresh = vi.fn();
  api.get.mockResolvedValueOnce(registered('signed-in', 'ready'));
  const signedOut = deferred<ReturnType<typeof status>>();
  api.signOut.mockReturnValue(signedOut.promise);
  await act(async () => { tree = create(<Fixture refresh={refresh} />); });
  await act(async () => { await Promise.resolve(); });
  expect(button('Sign out')).toBeDefined();
  expect(button('Sign out').props.title).toContain('affects only Chirality');
  expect(refresh).toHaveBeenCalledTimes(1);

  await act(async () => button('Sign out').props.onClick());
  expect(button('Signing out…').props.title).toContain('Signing out of Codex in Chirality');
  expect(button('Signing out…').props.disabled).toBe(true);
  expect(refresh).toHaveBeenCalledTimes(1);
  await act(async () => { signedOut.resolve(status('ready-to-start')); await Promise.resolve(); await Promise.resolve(); });
  expect(text()).toContain('Sign in');
  expect(refresh).toHaveBeenCalledTimes(2);

  api.start.mockResolvedValue({ loginId: 'again', authUrl: 'https://auth.openai.example/again' });
  api.get.mockResolvedValue(registered('signed-in', 'ready'));
  await act(async () => { button('Sign in with your ChatGPT account').props.onClick(); await Promise.resolve(); await Promise.resolve(); });
  expect(text()).toContain('Signed in · Ready to work');
  expect(refresh).toHaveBeenCalledTimes(3);
});

it('keeps sign-out uncertainty unavailable, refreshes after reconciliation, and does not claim success', async () => {
  const refresh = vi.fn();
  api.get.mockResolvedValueOnce(registered('signed-in', 'ready')).mockResolvedValueOnce(registered('failed', 'unavailable'));
  api.signOut.mockRejectedValue(new Error('transport detail'));
  await act(async () => { tree = create(<Fixture refresh={refresh} />); });
  await act(async () => { await Promise.resolve(); });
  await act(async () => { button('Sign out').props.onClick(); await Promise.resolve(); await Promise.resolve(); await Promise.resolve(); });
  expect(text()).toContain('Sign-out could not be confirmed');
  expect(text()).not.toContain('Sign-in failed');
  expect(text()).not.toContain('Ready to work');
  expect(latest.snapshot?.registration === 'registered' ? latest.snapshot.status.admission : null).toBe('unavailable');
  expect(refresh).toHaveBeenCalledTimes(2);
});

it('renders a ready status unchanged when it also carries the model catalog and selection', async () => {
  const ready = registered('signed-in', 'ready');
  api.get.mockResolvedValue({ ...ready, status: { ...ready.status,
    models: [{ model: 'gpt-default', isDefault: true, defaultReasoningEffort: 'high', supportedReasoningEfforts: ['low', 'high'] }],
    selection: { model: 'gpt-default', reasoningEffort: 'high' } } });
  await act(async () => { tree = create(<Fixture />); });
  await act(async () => { await Promise.resolve(); });
  expect(text()).toContain('Signed in');
  expect(text()).toContain('Sign out');
  expect(text()).not.toContain('gpt-default');
  expect(hostedBootstrapSummary(latest)).toBe('Signed in · Ready to work');
});

it('rejects a late sign-out result across an A to B to A root cycle', async () => {
  const late = deferred<ReturnType<typeof status>>();
  let signal!: AbortSignal;
  api.get.mockResolvedValueOnce({ registration: 'registered', projectId: 'a', status: { ...status('signed-in', 'ready'), projectId: 'a' } }).mockResolvedValue({ registration: 'required' });
  api.signOut.mockImplementation((_root: string, actionSignal: AbortSignal) => { signal = actionSignal; return late.promise; });
  await act(async () => { tree = create(<Fixture projectRoot="/projects/a" />); });
  await act(async () => { await Promise.resolve(); });
  await act(async () => button('Sign out').props.onClick());
  await act(async () => tree.update(<Fixture projectRoot="/projects/b" />));
  await act(async () => tree.update(<Fixture projectRoot="/projects/a" />));
  await act(async () => { await Promise.resolve(); });
  await act(async () => { late.resolve(status('ready-to-start')); await Promise.resolve(); await Promise.resolve(); });
  expect(signal.aborted).toBe(true);
  expect(text()).toContain('Use this folder');
});

it('does not let an in-flight readiness poll restore ready after sign-out starts', async () => {
  vi.useFakeTimers();
  const poll = deferred<ReturnType<typeof registered>>();
  const logout = deferred<ReturnType<typeof status>>();
  api.get.mockResolvedValueOnce(registered('signed-in', 'establishing')).mockReturnValueOnce(poll.promise);
  api.signOut.mockReturnValue(logout.promise);
  await act(async () => { tree = create(<Fixture />); });
  await act(async () => { await Promise.resolve(); });
  await act(async () => { await vi.advanceTimersByTimeAsync(1000); });
  await act(async () => button('Sign out').props.onClick());
  await act(async () => { poll.resolve(registered('signed-in', 'ready')); await Promise.resolve(); await Promise.resolve(); });
  expect(button('Signing out…').props.title).toContain('Signing out of Codex in Chirality');
  expect(text()).not.toContain('Ready to work');
  await act(async () => { logout.resolve(status('ready-to-start')); await Promise.resolve(); await Promise.resolve(); });
  expect(text()).toContain('Sign in');
  expect(text()).not.toContain('Allow provider network');
});

it('re-reads status after a rejected sign-in and shows the reason on the existing error line', async () => {
  api.get.mockResolvedValueOnce(registered('ready-to-start')).mockResolvedValue(registered('failed'));
  api.start.mockRejectedValue(new Error('Sign-in could not start (CODEX_REQUEST_REJECTED).'));
  await act(async () => { tree = create(<Fixture />); });
  await act(async () => { await Promise.resolve(); });
  expect(api.get).toHaveBeenCalledTimes(1);
  await act(async () => { button('Sign in with your ChatGPT account').props.onClick(); await Promise.resolve(); await Promise.resolve(); await Promise.resolve(); });
  expect(api.get).toHaveBeenCalledTimes(2);
  expect(api.get).toHaveBeenLastCalledWith(root, expect.any(AbortSignal));
  expect(text()).toContain('Sign-in could not start (CODEX_REQUEST_REJECTED).');
  expect(text()).toContain('Sign-in failed. You can start a new sign-in attempt.');
  expect(tree.root.findAllByType('a')).toHaveLength(0);
  expect(button('Sign in with your ChatGPT account').props.disabled).toBe(false);
  // Exactly one inline reason line, no new surface.
  expect(tree.root.findAllByProps({ role: 'alert' }).filter(node => node.type === 'p')).toHaveLength(2);
});

it('reflects the signed-out state from the re-read after a rejected action, as after a service restart', async () => {
  api.get.mockResolvedValueOnce(registered('signed-in', 'ready')).mockResolvedValue(registered('ready-to-start'));
  api.signOut.mockRejectedValue(new Error('Sign-out could not be confirmed.'));
  await act(async () => { tree = create(<Fixture />); });
  await act(async () => { await Promise.resolve(); });
  await act(async () => { button('Sign out').props.onClick(); await Promise.resolve(); await Promise.resolve(); await Promise.resolve(); });
  expect(text()).toContain('Sign in');
  expect(hostedBootstrapSummary(latest)).toBe('Sign in required');
  expect(text()).not.toContain('consent');
});

it('keeps the action error when the re-read after a rejected sign-in fails too', async () => {
  api.get.mockResolvedValueOnce(registered('ready-to-start')).mockRejectedValueOnce(new Error('Hosted account service is unavailable.'));
  api.start.mockRejectedValue(new Error('Sign-in could not start (CODEX_REQUEST_REJECTED).'));
  await act(async () => { tree = create(<Fixture />); });
  await act(async () => { await Promise.resolve(); });
  await act(async () => { button('Sign in with your ChatGPT account').props.onClick(); await Promise.resolve(); await Promise.resolve(); await Promise.resolve(); });
  expect(api.get).toHaveBeenCalledTimes(2);
  expect(text()).toContain('Sign-in could not start (CODEX_REQUEST_REJECTED).');
  expect(text()).toContain('Sign in');
});

it('re-reads status when the surface reopens and drops a stale error, but not while busy or polling', async () => {
  api.get.mockResolvedValueOnce(registered('ready-to-start'));
  api.start.mockRejectedValueOnce(new Error('Sign-in could not start (CODEX_REQUEST_REJECTED).'));
  await act(async () => { tree = create(<Fixture />); });
  await act(async () => { await Promise.resolve(); });
  api.get.mockResolvedValueOnce(registered('failed'));
  await act(async () => { button('Sign in with your ChatGPT account').props.onClick(); await Promise.resolve(); await Promise.resolve(); await Promise.resolve(); });
  expect(text()).toContain('CODEX_REQUEST_REJECTED');

  // The service was restarted in between: reopening shows its real state.
  api.get.mockResolvedValue(registered('ready-to-start'));
  await act(async () => { latest.onRefresh(); await Promise.resolve(); await Promise.resolve(); });
  expect(api.get).toHaveBeenCalledTimes(3);
  expect(text()).toContain('Sign in');
  expect(text()).not.toContain('CODEX_REQUEST_REJECTED');

  // A refresh while an action is in flight does not race the action's own read.
  const started = deferred<{ loginId: string; authUrl: string }>();
  api.start.mockReturnValue(started.promise);
  await act(async () => button('Sign in with your ChatGPT account').props.onClick());
  await act(async () => { latest.onRefresh(); await Promise.resolve(); });
  expect(api.get).toHaveBeenCalledTimes(3);
  api.get.mockResolvedValue(registered('cancelled'));
  await act(async () => { started.resolve({ loginId: 'login-x', authUrl: 'https://auth.openai.example/login-x' }); await Promise.resolve(); await Promise.resolve(); await Promise.resolve(); });
  expect(text()).toContain('Sign in');

  vi.useFakeTimers();
  api.start.mockResolvedValue({ loginId: 'login-2', authUrl: 'https://auth.openai.example/login-2' });
  api.get.mockResolvedValue(registered('pending', 'establishing'));
  await act(async () => { button('Sign in with your ChatGPT account').props.onClick(); await Promise.resolve(); await Promise.resolve(); });
  const pollingReads = api.get.mock.calls.length;
  await act(async () => { latest.onRefresh(); await Promise.resolve(); });
  expect(api.get).toHaveBeenCalledTimes(pollingReads);
});

it('re-reads status once when the runtime reconnects and not on repeated connected reports', async () => {
  const snapshot = (state: 'connected' | 'disconnected', changedAt: string) => ({ state, failedAttempts: 0, lastError: null, changedAt });
  connectivity.current = snapshot('disconnected', '2026-09-11T00:00:00.000Z');
  try {
    api.get.mockResolvedValue(registered('ready-to-start'));
    await act(async () => { tree = create(<Fixture />); });
    await act(async () => { await Promise.resolve(); });
    expect(api.get).toHaveBeenCalledTimes(1);

    api.get.mockResolvedValue(registered('ready-to-start'));
    connectivity.current = snapshot('connected', '2026-09-11T00:00:05.000Z');
    await act(async () => { tree.update(<Fixture />); await Promise.resolve(); await Promise.resolve(); });
    expect(api.get).toHaveBeenCalledTimes(2);
    expect(text()).toContain('Sign in');
  expect(text()).not.toContain('Allow provider network');

    connectivity.current = snapshot('connected', '2026-09-11T00:00:15.000Z');
    await act(async () => { tree.update(<Fixture />); await Promise.resolve(); await Promise.resolve(); });
    expect(api.get).toHaveBeenCalledTimes(2);

    connectivity.current = snapshot('disconnected', '2026-09-11T00:00:20.000Z');
    await act(async () => { tree.update(<Fixture />); await Promise.resolve(); await Promise.resolve(); });
    expect(api.get).toHaveBeenCalledTimes(2);
  } finally {
    connectivity.current = null;
  }
});

// Item 14: account authentication is a fact of the Codex host, not of the
// selected folder. Switching to a folder the Runtime cannot bind yet must keep
// the signed-in account visible and name the folder problem as such.
function conflictError(): Error & { status: number } {
  return Object.assign(new Error('A different project is already bound to the Desktop runtime client'), { status: 409 });
}

it('keeps the signed-in account across a folder switch whose binding conflicts, and names the folder problem rather than sign-in', async () => {
  api.get.mockResolvedValue(registered('signed-in', 'ready'));
  await act(async () => { tree = create(<Fixture projectRoot="/projects/a" />); });
  await settle();
  expect(hostedBootstrapSummary(latest)).toBe('Signed in · Ready to work');
  expect(latest.project.state).toBe('registered');

  api.get.mockRejectedValue(conflictError());
  await act(async () => tree.update(<Fixture projectRoot="/projects/b" />));
  await settle();
  expect(latest.account?.ceremony).toBe('signed-in');
  expect(latest.project).toEqual({ state: 'conflict', message: 'A different project is already bound to the Desktop runtime client' });
  expect(hostedBootstrapSummary(latest)).toBe('Signed in · Another folder is active');
  expect(text()).not.toContain('Sign in required');
  expect(text()).not.toContain('Sign in with your ChatGPT account');
  expect(text()).toContain('Use this folder');
  expect(text()).toContain('moves it here; your sign-in is not affected');
  // A restored (not explicitly selected) root never rebinds on its own.
  expect(api.initialize).not.toHaveBeenCalled();

  api.get.mockRejectedValue(Object.assign(new Error('The selected project folder is inaccessible'), { status: 404 }));
  await act(async () => tree.update(<Fixture projectRoot="/projects/missing" />));
  await settle();
  expect(latest.project.state).toBe('unavailable');
  expect(hostedBootstrapSummary(latest)).toBe('Signed in · Folder unavailable');
  expect(text()).toContain('could not be read or registered');
});

it('rebinds an explicitly selected folder once when hydration reports a binding conflict', async () => {
  installWorkspaceHost('/projects/a');
  const refresh = vi.fn();
  api.get.mockResolvedValue(registered('signed-in', 'ready'));
  await act(async () => { tree = create(<WorkspaceProvider><WorkspaceFixture refresh={refresh} /></WorkspaceProvider>); });
  await settle();
  expect(hostedBootstrapSummary(latest)).toBe('Signed in · Ready to work');

  api.get.mockRejectedValueOnce(conflictError()).mockResolvedValue({ registration: 'registered', projectId: 'project-b', status: { ...status('signed-in', 'ready'), projectId: 'project-b' } });
  api.initialize.mockResolvedValue({ registration: 'registered', projectId: 'project-b' });
  await act(async () => { await workspace.applyProjectRoot('/projects/b'); });
  await settle();
  expect(api.initialize).toHaveBeenCalledTimes(1);
  expect(api.initialize).toHaveBeenCalledWith('/projects/b', expect.any(AbortSignal));
  expect(latest.project.state).toBe('registered');
  expect(latest.snapshot).toMatchObject({ registration: 'registered', projectId: 'project-b' });
  expect(hostedBootstrapSummary(latest)).toBe('Signed in · Ready to work');
  expect(refresh).toHaveBeenCalled();
  await settle();
  expect(api.initialize).toHaveBeenCalledTimes(1);
});

it('reports a signed-out account with the folder standing instead of a bare sign-in demand', async () => {
  api.get.mockResolvedValue(registered('ready-to-start'));
  await act(async () => { tree = create(<Fixture projectRoot="/projects/a" />); });
  await settle();
  expect(hostedBootstrapSummary(latest)).toBe('Sign in required');
  api.get.mockRejectedValue(conflictError());
  await act(async () => tree.update(<Fixture projectRoot="/projects/b" />));
  await settle();
  expect(hostedBootstrapSummary(latest)).toBe('Not signed in · Another folder is active');
});
