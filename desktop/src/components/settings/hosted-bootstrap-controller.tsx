'use client';

import { useCallback, useEffect, useRef, useState } from 'react';
import {
  cancelHostedBootstrapLogin,
  getHostedBootstrapStatus,
  getHostedBootstrapStatusWithRetry,
  initializeHostedBootstrapProject,
  hydrateHostedBootstrapProject,
  signOutHostedBootstrapProject,
  startHostedBootstrapLogin
} from '../../lib/harness/hosted-bootstrap-client';
import { isRuntimeReconnect } from '../../lib/shell/runtime-connectivity';
import { useRuntimeConnectivitySnapshot } from '../shell/runtime-connectivity-provider';
import { useWorkspaceSelection } from '../workspace/workspace-provider';

export type HostedBootstrapStatusResult = Awaited<ReturnType<typeof getHostedBootstrapStatus>>;
type RegisteredBootstrap = Extract<HostedBootstrapStatusResult, { registration: 'registered' }>;
export type HostedAccountStatus = RegisteredBootstrap['status'];

/**
 * The selected folder's standing with the Runtime, kept apart from the
 * account. Sign-in belongs to the Codex host and survives folder changes; a
 * folder can be unregistered, bound behind another folder in this Runtime
 * session (`conflict`), or unreadable (`unavailable`) while the account stays
 * signed in.
 */
export type HostedProjectState =
  | { state: 'none' | 'checking' | 'registered' | 'setup-required'; message: null }
  | { state: 'conflict' | 'unavailable'; message: string };

export type HostedBootstrapController = {
  projectRoot: string | null;
  snapshot: HostedBootstrapStatusResult | null;
  /**
   * The last account status the Runtime reported for any folder in this
   * session. It outlives folder changes and project failures, so the account
   * row and the model selectors never read a folder problem as signed out.
   */
  account: HostedAccountStatus | null;
  project: HostedProjectState;
  loading: boolean;
  busyAction: 'setup' | 'login' | 'cancel' | 'logout' | null;
  error: string | null;
  signOutUncertain: boolean;
  authUrl: string | null;
  onSetup: () => void;
  onStartLogin: () => void;
  /** Open the pending sign-in page again in the browser (the URL is retained for this session only). */
  onReopenLogin: () => void;
  onCancelLogin: () => void;
  onSignOut: () => void;
  /** Re-read account status from the daemon when the surface is (re)opened. */
  onRefresh: () => void;
};

/**
 * Sign-in is one action: the OpenAI page opens in the system browser as soon
 * as Codex returns it. The desktop window policy routes every http(s)
 * `window.open` to `shell.openExternal` and denies the child window, so no
 * preload surface is needed; in a plain browser this opens a tab.
 */
export function openSignInPage(url: string): boolean {
  if (typeof window === 'undefined' || typeof window.open !== 'function' || !/^https:\/\//.test(url)) return false;
  try { window.open(url, '_blank', 'noopener,noreferrer'); return true; } catch { return false; }
}

function messageFrom(error: unknown): string {
  return error instanceof Error ? error.message : 'The OpenAI account request could not be completed.';
}

function withStatus(current: HostedBootstrapStatusResult | null, status: RegisteredBootstrap['status']): HostedBootstrapStatusResult | null {
  return current?.registration === 'registered' ? { ...current, status } : current;
}

type LoadFailure = { status: number | null; message: string };

function loadFailureFrom(error: unknown): LoadFailure {
  // HostedBootstrapClientError carries the route status; read it by shape so a
  // substituted client module still classifies its failures.
  const candidate = error instanceof Error ? (error as Error & { status?: unknown }).status : undefined;
  const status = typeof candidate === 'number' ? candidate : null;
  return { status, message: messageFrom(error) };
}

/** A 409 from the bind or status route: another folder is bound in this Runtime session, and explicit setup rebinds. */
function isBindingConflict(failure: LoadFailure | null): boolean {
  return failure?.status === 409;
}

export function hostedProjectState(input: {
  projectRoot: string | null; loading: boolean; snapshot: HostedBootstrapStatusResult | null; loadFailure: LoadFailure | null;
}): HostedProjectState {
  if (!input.projectRoot) return { state: 'none', message: null };
  if (input.snapshot?.registration === 'registered') return { state: 'registered', message: null };
  if (input.snapshot?.registration === 'required') return { state: 'setup-required', message: null };
  if (input.loadFailure) {
    return isBindingConflict(input.loadFailure)
      ? { state: 'conflict', message: input.loadFailure.message }
      : { state: 'unavailable', message: input.loadFailure.message };
  }
  return { state: input.loading ? 'checking' : 'setup-required', message: null };
}

export function useHostedBootstrapController(projectRoot: string | null, onBindingChanged: () => void): HostedBootstrapController {
  const [observed, setObserved] = useState<{ projectRoot: string | null; snapshot: HostedBootstrapStatusResult | null }>({ projectRoot, snapshot: null });
  const snapshot = observed.projectRoot === projectRoot ? observed.snapshot : null;
  // Account status is global to the Codex host: every registered snapshot,
  // for whichever folder, refreshes it, and a folder change does not clear it.
  const [account, setAccount] = useState<HostedAccountStatus | null>(null);
  const [loadFailure, setLoadFailure] = useState<{ projectRoot: string | null; failure: LoadFailure } | null>(null);
  const [loading, setLoading] = useState(Boolean(projectRoot));
  const [busyAction, setBusyAction] = useState<HostedBootstrapController['busyAction']>(null);
  const [error, setError] = useState<string | null>(null);
  const [authUrl, setAuthUrl] = useState<string | null>(null);
  const [signOutUncertain, setSignOutUncertain] = useState(false);
  const lastSelection = useWorkspaceSelection();
  const rootRef = useRef(projectRoot);
  const snapshotRef = useRef(snapshot);
  const onBindingChangedRef = useRef(onBindingChanged);
  const publishedBindingKeys = useRef(new Set<string>());
  const autoSetupSequence = useRef<number | null>(null);
  const operationGeneration = useRef(0);
  const actionController = useRef<AbortController | null>(null);
  const pollController = useRef<AbortController | null>(null);
  rootRef.current = projectRoot;
  snapshotRef.current = snapshot;
  onBindingChangedRef.current = onBindingChanged;

  useEffect(() => {
    if (observed.snapshot?.registration === 'registered') setAccount(observed.snapshot.status);
  }, [observed]);

  const publishBinding = useCallback((root: string, projectId: string): void => {
    const key = `${root}:${projectId}:registered`;
    if (publishedBindingKeys.current.has(key)) return;
    publishedBindingKeys.current.add(key);
    onBindingChangedRef.current();
  }, []);

  const load = useCallback(async (root: string, generation: number, signal?: AbortSignal): Promise<void> => {
    const result = await hydrateHostedBootstrapProject(
      root,
      (binding) => {
        if (
          !signal?.aborted &&
          operationGeneration.current === generation &&
          rootRef.current === root
        ) {
          publishBinding(root, binding.projectId);
        }
      },
      signal
    );
    if (!signal?.aborted && operationGeneration.current === generation && rootRef.current === root) {
      setObserved({ projectRoot: root, snapshot: result });
      setLoadFailure(null);
      setError(null);
      setLoading(false);
    }
  }, [publishBinding]);

  // Explicit setup registers and binds through the App tier, publishes the
  // verified binding exactly as hydration does, then reads account status
  // through the App status route.
  const setup = useCallback(async (root: string, signal: AbortSignal, generation: number): Promise<void> => {
    const binding = await initializeHostedBootstrapProject(root, signal);
    if (signal.aborted || operationGeneration.current !== generation || rootRef.current !== root) return;
    publishBinding(root, binding.projectId);
    const result = await getHostedBootstrapStatusWithRetry(root, signal);
    if (signal.aborted || operationGeneration.current !== generation || rootRef.current !== root) return;
    setObserved({ projectRoot: root, snapshot: result });
    setLoadFailure(null);
    setAuthUrl(null);
  }, [publishBinding]);

  // Re-read status through the App status route and adopt it if still current.
  // Used after a rejected action, on reconnect, and when the surface reopens,
  // so the popover shows the Runtime's real state (for example signed out after
  // a service restart) rather than the last optimistic write. A failed re-read
  // is swallowed: the caller's own error, if any, stays in place.
  const reconcile = useCallback(async (root: string, generation: number, signal: AbortSignal, clearError = false): Promise<void> => {
    try {
      const result = await getHostedBootstrapStatusWithRetry(root, signal);
      if (!signal.aborted && operationGeneration.current === generation && rootRef.current === root) {
        setObserved({ projectRoot: root, snapshot: result });
        if (clearError) setError(null);
      }
    } catch {}
  }, []);

  const withReconcile = useCallback(async <T,>(
    root: string, signal: AbortSignal, generation: number, request: () => Promise<T>
  ): Promise<T> => {
    try { return await request(); }
    catch (reason) {
      if (!signal.aborted && operationGeneration.current === generation && rootRef.current === root) await reconcile(root, generation, signal);
      throw reason;
    }
  }, [reconcile]);

  const busyRef = useRef(busyAction);
  const loadingRef = useRef(loading);
  busyRef.current = busyAction;
  loadingRef.current = loading;
  const refresh = useCallback((): void => {
    const root = rootRef.current;
    // Hydration, an action, and the pending/establishing poll each already own
    // a status read; a refresh alongside them would only race their result.
    if (!root || loadingRef.current || busyRef.current) return;
    if (pollController.current && !pollController.current.signal.aborted) return;
    void reconcile(root, operationGeneration.current, new AbortController().signal, true);
  }, [reconcile]);

  const connectivity = useRuntimeConnectivitySnapshot();
  const previousConnectivity = useRef(connectivity);
  useEffect(() => {
    const previous = previousConnectivity.current;
    previousConnectivity.current = connectivity;
    if (connectivity !== null && isRuntimeReconnect(previous, connectivity)) refresh();
  }, [connectivity, refresh]);

  useEffect(() => {
    const generation = ++operationGeneration.current;
    actionController.current?.abort();
    pollController.current?.abort();
    publishedBindingKeys.current.clear();
    setObserved({ projectRoot, snapshot: null });
    setLoadFailure(null);
    setAuthUrl(null);
    setError(null);
    setSignOutUncertain(false);
    setBusyAction(null);
    if (!projectRoot) { setLoading(false); return; }
    setLoading(true);
    const controller = new AbortController();
    void load(projectRoot, generation, controller.signal).catch(reason => {
      if (!controller.signal.aborted && operationGeneration.current === generation && rootRef.current === projectRoot) {
        setLoadFailure({ projectRoot, failure: loadFailureFrom(reason) });
        setError(messageFrom(reason));
        setLoading(false);
      }
    });
    return () => {
      ++operationGeneration.current;
      controller.abort();
      actionController.current?.abort();
      pollController.current?.abort();
    };
  }, [projectRoot, load]);

  useEffect(() => {
    if (!projectRoot || snapshot?.registration !== 'registered') return;
    const keys = [`${projectRoot}:${snapshot.projectId}:registered`];
    if (snapshot.status.admission === 'ready') keys.push(`${projectRoot}:${snapshot.projectId}:ready`);
    let publish = false;
    for (const key of keys) {
      if (publishedBindingKeys.current.has(key)) continue;
      publishedBindingKeys.current.add(key);
      publish = true;
    }
    if (publish) onBindingChanged();
    if (['signed-in', 'failed', 'cancelled'].includes(snapshot.status.ceremony)) setAuthUrl(null);
  }, [projectRoot, snapshot, onBindingChanged]);

  useEffect(() => {
    if (!projectRoot || busyAction || snapshot?.registration !== 'registered') return;
    const status = snapshot.status;
    if (status.ceremony !== 'pending' && status.admission !== 'establishing') return;
    const controller = new AbortController();
    pollController.current = controller;
    const generation = operationGeneration.current;
    let active = false;
    const poll = (): void => {
      if (active || controller.signal.aborted) return;
      active = true;
      void load(projectRoot, generation, controller.signal).catch(reason => {
        if (!controller.signal.aborted && operationGeneration.current === generation && rootRef.current === projectRoot) setError(messageFrom(reason));
      }).finally(() => { active = false; });
    };
    const timer = window.setInterval(poll, 1000);
    return () => {
      controller.abort();
      if (pollController.current === controller) pollController.current = null;
      window.clearInterval(timer);
    };
  }, [projectRoot, snapshot, busyAction, load]);

  const perform = useCallback(async (
    action: NonNullable<HostedBootstrapController['busyAction']>,
    run: (root: string, signal: AbortSignal, generation: number) => Promise<void>
  ): Promise<void> => {
    const root = rootRef.current;
    if (!root || busyAction) return;
    const generation = ++operationGeneration.current;
    actionController.current?.abort();
    pollController.current?.abort();
    const controller = new AbortController();
    actionController.current = controller;
    setBusyAction(action);
    setError(null);
    if (action !== 'logout') setSignOutUncertain(false);
    try { await run(root, controller.signal, generation); }
    catch (reason) {
      if (!controller.signal.aborted && operationGeneration.current === generation && rootRef.current === root) setError(messageFrom(reason));
    } finally {
      if (actionController.current === controller) actionController.current = null;
      if (!controller.signal.aborted && operationGeneration.current === generation && rootRef.current === root) setBusyAction(null);
    }
  }, [busyAction]);

  const currentFailure = loadFailure && loadFailure.projectRoot === projectRoot ? loadFailure.failure : null;
  const project = hostedProjectState({ projectRoot, loading, snapshot, loadFailure: currentFailure });

  // A folder the user chose explicitly in this session (native picker or an
  // applied path) that hydrates as unregistered, or as bound behind another
  // folder in this Runtime session, is set up once for that selection: explicit
  // setup is the supported way to move the Runtime to the chosen folder. Roots
  // restored from storage never auto-initialize, and a failed automatic setup
  // leaves the manual action and its error in place.
  useEffect(() => {
    if (
      !projectRoot ||
      !lastSelection ||
      lastSelection.path !== projectRoot ||
      autoSetupSequence.current === lastSelection.sequence ||
      loading ||
      busyAction ||
      (snapshot?.registration !== 'required' && !isBindingConflict(currentFailure))
    ) return;
    autoSetupSequence.current = lastSelection.sequence;
    void perform('setup', setup);
  }, [projectRoot, lastSelection, loading, busyAction, snapshot, currentFailure, perform, setup]);

  return {
    projectRoot, snapshot, account, project, loading, busyAction, error, authUrl, signOutUncertain,
    onSetup: () => void perform('setup', setup),
    onRefresh: refresh,
    onStartLogin: () => void perform('login', async (root, signal, generation) => {
      const result = await withReconcile(root, signal, generation, () => startHostedBootstrapLogin(root, signal));
      if (signal.aborted || operationGeneration.current !== generation || rootRef.current !== root) return;
      setAuthUrl(result.authUrl);
      openSignInPage(result.authUrl);
      setObserved(current => ({
        projectRoot: root,
        snapshot: current.projectRoot === root && current.snapshot?.registration === 'registered'
          ? { ...current.snapshot, status: { ...current.snapshot.status, ceremony: 'pending', canStartLogin: false } }
          : current.snapshot
      }));
      await load(root, generation, signal);
    }),
    onReopenLogin: () => { if (authUrl) openSignInPage(authUrl); },
    onCancelLogin: () => void perform('cancel', async (root, signal, generation) => {
      const status = await withReconcile(root, signal, generation, () => cancelHostedBootstrapLogin(root, signal));
      if (signal.aborted || operationGeneration.current !== generation || rootRef.current !== root) return;
      setAuthUrl(null);
      setObserved(current => ({ projectRoot: root, snapshot: withStatus(current.projectRoot === root ? current.snapshot : null, status) }));
    }),
    onSignOut: () => void perform('logout', async (root, signal, generation) => {
      const currentSnapshot = snapshotRef.current;
      if (currentSnapshot?.registration === 'registered') {
        publishedBindingKeys.current.delete(`${root}:${currentSnapshot.projectId}:ready`);
      }
      setAuthUrl(null);
      setSignOutUncertain(false);
      setObserved(current => {
        if (current.projectRoot !== root || current.snapshot?.registration !== 'registered') return current;
        return { projectRoot: root, snapshot: withStatus(current.snapshot, { ...current.snapshot.status, admission: 'unavailable' }) };
      });
      try {
        const status = await signOutHostedBootstrapProject(root, signal);
        if (signal.aborted || operationGeneration.current !== generation || rootRef.current !== root) return;
        setObserved(current => ({ projectRoot: root, snapshot: withStatus(current.projectRoot === root ? current.snapshot : null, status) }));
        onBindingChanged();
      } catch {
        if (signal.aborted || operationGeneration.current !== generation || rootRef.current !== root) return;
        setSignOutUncertain(true);
        try {
          const reconciled = await getHostedBootstrapStatusWithRetry(root, signal);
          if (!signal.aborted && operationGeneration.current === generation && rootRef.current === root) {
            setObserved({
              projectRoot: root,
              snapshot: reconciled.registration === 'registered'
                ? { ...reconciled, status: { ...reconciled.status, admission: 'unavailable' } }
                : reconciled
            });
          }
        } catch {}
        if (!signal.aborted && operationGeneration.current === generation && rootRef.current === root) onBindingChanged();
        throw new Error('Sign-out could not be confirmed. Check this project’s status before signing in again.');
      }
    })
  };
}
