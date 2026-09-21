'use client';

import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useRef,
  useState,
  type ReactNode
} from 'react';
import {
  isRuntimeReconnect,
  type RuntimeConnectivitySnapshot
} from '../../lib/shell/runtime-connectivity';
import { useRuntimeConnectivity } from './use-runtime-connectivity';

type RuntimeConnectivityContextValue = {
  snapshot: RuntimeConnectivitySnapshot | null;
  /**
   * Monotonic counter, one increment per observed reconnect. It is a *dependency
   * value*, not a status: components put it in an effect's dependency array and
   * get exactly one re-run per reconnect, for free, with no listener of their own.
   */
  epoch: number;
  /** Publish one renderer refresh after an explicit project binding changes. */
  refreshBindings: () => void;
};

const RuntimeConnectivityContext = createContext<RuntimeConnectivityContextValue | null>(
  null
);

/**
 * App-wide runtime-connectivity state plus the reconnect epoch.
 *
 * Why an epoch at all: every runtime-backed pane fetches once at mount and keeps
 * whatever it got. When the app opens while the daemon is being replaced, those
 * fetches land in the dead-socket window, latch a terminal error, and stay wrong
 * forever — the top bar flips to "connected" while the persona roster still says
 * unavailable. The main process already publishes the transition; the missing
 * half was a renderer-side signal that says "re-ask, once".
 *
 * One counter rather than a refresh bus or per-pane listeners: it composes with
 * React's own re-run rule, so a pane opts in by adding one dependency, and there
 * is no subscription for a pane to forget to unsubscribe from. Re-fetching is
 * strictly one pass per transition — the main process owns retry and backoff, so
 * a renderer that also retried would be a second, uncoordinated retry loop.
 */
export function RuntimeConnectivityProvider({
  children
}: {
  children: ReactNode;
}): JSX.Element {
  const snapshot = useRuntimeConnectivity();
  const [epoch, setEpoch] = useState(0);
  const previousRef = useRef<RuntimeConnectivitySnapshot | null>(null);
  const refreshBindings = useCallback(() => setEpoch((value) => value + 1), []);

  useEffect(() => {
    const previous = previousRef.current;
    previousRef.current = snapshot;
    if (snapshot !== null && isRuntimeReconnect(previous, snapshot)) {
      setEpoch((value) => value + 1);
    }
  }, [snapshot]);

  const value = useMemo<RuntimeConnectivityContextValue>(
    () => ({ snapshot, epoch, refreshBindings }),
    [snapshot, epoch, refreshBindings]
  );

  return (
    <RuntimeConnectivityContext.Provider value={value}>
      {children}
    </RuntimeConnectivityContext.Provider>
  );
}

/**
 * The reconnect epoch, or `0` where there is no provider — SSR, a plain browser,
 * and the many suites that render one pane in isolation. `0` means "no reconnect
 * has been observed", so an epoch-dependent effect behaves exactly as it did
 * before this mechanism existed: it runs once and stays put.
 */
export function useRuntimeEpoch(): number {
  return useContext(RuntimeConnectivityContext)?.epoch ?? 0;
}

/** Re-fetch runtime-backed panes after an explicit renderer-initiated binding. */
export function useRuntimeBindingRefresh(): () => void {
  return useContext(RuntimeConnectivityContext)?.refreshBindings ?? (() => {});
}

/**
 * Connectivity snapshot for presentation. Reads the provider when one is mounted
 * so the whole app shares a single bridge subscription, and falls back to its own
 * subscription when rendered standalone.
 */
export function useRuntimeConnectivitySnapshot(): RuntimeConnectivitySnapshot | null {
  const context = useContext(RuntimeConnectivityContext);
  const standalone = useRuntimeConnectivity(context === null);
  return context ? context.snapshot : standalone;
}
