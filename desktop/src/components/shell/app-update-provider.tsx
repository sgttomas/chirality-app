'use client';

import React, {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
  type ReactNode
} from 'react';

/**
 * Renderer-side view of app-update checking.
 *
 * Types are duplicated from `electron/app-update-ipc-contract.ts` on purpose:
 * the renderer bundle must not reach into main-process modules, and the
 * boundary is an IPC payload shape, not a shared implementation.
 */
export type AppUpdateFailureCode = 'no-release-source' | 'policy' | 'network' | 'invalid-feed';

export type AppUpdateStatus = 'idle' | 'checking' | 'up-to-date' | 'update-available' | 'failed';

export type AppUpdateState = {
  currentVersion: string;
  status: AppUpdateStatus;
  checkedAt?: string;
  failure?: { code: AppUpdateFailureCode; message: string };
  available?: { version: string; downloadUrl: string; releaseNotesUrl?: string; publishedAt?: string };
  releaseSource: { configured: boolean; description: string };
};

export type AppUpdateBridge = {
  get: () => Promise<AppUpdateState>;
  check: () => Promise<AppUpdateState>;
  openDownload: () => Promise<{ ok: boolean; error?: string }>;
  subscribe: (listener: (state: AppUpdateState) => void) => () => void;
  onShowAbout: (listener: () => void) => () => void;
};

export type AppUpdateContextValue = {
  /** `null` until the bridge answers, and always `null` without a bridge. */
  state: AppUpdateState | null;
  /** False in web dev, SSR and tests, where `window.chirality.appUpdate` is absent. */
  bridgeAvailable: boolean;
  check: () => Promise<void>;
  openDownload: () => Promise<void>;
  /** Monotonic counter, one increment per "About Chirality" menu signal. */
  aboutRequests: number;
};

const STATUSES: ReadonlySet<string> = new Set([
  'idle',
  'checking',
  'up-to-date',
  'update-available',
  'failed'
]);

export function isAppUpdateState(value: unknown): value is AppUpdateState {
  if (typeof value !== 'object' || value === null) return false;
  const candidate = value as Partial<AppUpdateState>;
  return (
    typeof candidate.currentVersion === 'string' &&
    typeof candidate.status === 'string' &&
    STATUSES.has(candidate.status) &&
    typeof candidate.releaseSource === 'object' &&
    candidate.releaseSource !== null &&
    typeof candidate.releaseSource.configured === 'boolean' &&
    typeof candidate.releaseSource.description === 'string'
  );
}

type AppUpdateWindow = typeof window & {
  chirality?: { appUpdate?: AppUpdateBridge };
};

function getAppUpdateBridge(): AppUpdateBridge | undefined {
  if (typeof window === 'undefined') return undefined;
  return (window as AppUpdateWindow).chirality?.appUpdate;
}

const noop = async (): Promise<void> => undefined;

const FALLBACK: AppUpdateContextValue = {
  state: null,
  bridgeAvailable: false,
  check: noop,
  openDownload: noop,
  aboutRequests: 0
};

const AppUpdateContext = createContext<AppUpdateContextValue | null>(null);

/**
 * App-wide app-update state plus the About signal from the application menu.
 *
 * One provider holds the single bridge subscription; the account menu and the
 * About dialog read the same state, so a check started from the macOS menu and
 * one started from the account menu show the same "checking" and the same
 * answer. `aboutRequests` is a dependency value, not a status: the About
 * dialog puts it in an effect's dependency array and opens once per signal.
 */
export function AppUpdateProvider({ children }: { children: ReactNode }): JSX.Element {
  const [bridge] = useState<AppUpdateBridge | undefined>(() => getAppUpdateBridge());
  const [state, setState] = useState<AppUpdateState | null>(null);
  const [aboutRequests, setAboutRequests] = useState(0);

  useEffect(() => {
    if (!bridge) return;
    let active = true;
    let pushed = false;
    const accept = (value: unknown, source: 'push' | 'hydrate'): void => {
      if (!active || !isAppUpdateState(value)) return;
      // Subscribe runs before the hydrating query resolves, so a transition
      // can land first. Never let the older in-flight answer overwrite it.
      if (source === 'hydrate' && pushed) return;
      if (source === 'push') pushed = true;
      setState(value);
    };
    const unsubscribe = bridge.subscribe((value) => accept(value, 'push'));
    const stopAbout = bridge.onShowAbout(() => {
      if (active) setAboutRequests((value) => value + 1);
    });
    void Promise.resolve(bridge.get())
      .then((value) => accept(value, 'hydrate'))
      .catch(() => undefined);
    return () => {
      active = false;
      unsubscribe();
      stopAbout();
    };
  }, [bridge]);

  const check = useCallback(async (): Promise<void> => {
    if (!bridge) return;
    try {
      const settled = await bridge.check();
      if (isAppUpdateState(settled)) setState(settled);
    } catch {
      // The main process owns the failure state and broadcasts it; a rejected
      // invoke (bridge torn down mid-check) leaves the last known state.
    }
  }, [bridge]);

  const openDownload = useCallback(async (): Promise<void> => {
    if (!bridge) return;
    try {
      // A refusal (`ok: false`) is logged by the main process; the state is
      // unchanged and the download simply does not open.
      await bridge.openDownload();
    } catch {
      // Same as above: nothing to surface beyond the unchanged state.
    }
  }, [bridge]);

  const value = useMemo<AppUpdateContextValue>(
    () => ({ state, bridgeAvailable: bridge !== undefined, check, openDownload, aboutRequests }),
    [state, bridge, check, openDownload, aboutRequests]
  );

  return <AppUpdateContext.Provider value={value}>{children}</AppUpdateContext.Provider>;
}

/**
 * App-update state for presentation. Without a provider (SSR, a plain browser,
 * suites that render one pane in isolation) the bridge reads as unavailable and
 * every action is a no-op, so callers can render nothing rather than guess.
 */
export function useAppUpdate(): AppUpdateContextValue {
  return useContext(AppUpdateContext) ?? FALLBACK;
}
