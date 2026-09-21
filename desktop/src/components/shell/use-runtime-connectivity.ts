'use client';

import { useEffect, useState } from 'react';
import {
  isRuntimeConnectivitySnapshot,
  type RuntimeConnectivityBridge,
  type RuntimeConnectivitySnapshot
} from '../../lib/shell/runtime-connectivity';

type RuntimeConnectivityWindow = typeof window & {
  chirality?: {
    runtime?: {
      connectivity?: RuntimeConnectivityBridge;
    };
  };
};

function getConnectivityBridge(): RuntimeConnectivityBridge | undefined {
  if (typeof window === 'undefined') {
    return undefined;
  }
  return (window as RuntimeConnectivityWindow).chirality?.runtime?.connectivity;
}

/**
 * Track runtime-daemon connectivity as reported by the main process.
 *
 * Returns `null` whenever there is nothing observable: during SSR, in a plain
 * browser, or on an older desktop build whose preload predates the connectivity
 * bridge. Callers render no indicator in that case.
 *
 * Deliberately push-driven. The daemon-status IPC already existed but only ran
 * when a renderer asked, which is why a daemon that came back after startup was
 * never noticed. Here the main process owns the polling and this hook only
 * mirrors its state, so one supervisor serves every mounted shell.
 *
 * `enabled` exists so `RuntimeConnectivityProvider` can be the app's single
 * subscriber while this hook stays usable standalone (a `ShellFrame` rendered
 * without the provider, as several suites do). A disabled call registers no
 * listener and stays at `null`; the caller is reading the context instead.
 */
export function useRuntimeConnectivity(enabled = true): RuntimeConnectivitySnapshot | null {
  const [snapshot, setSnapshot] = useState<RuntimeConnectivitySnapshot | null>(null);

  useEffect(() => {
    if (!enabled) {
      return;
    }

    const bridge = getConnectivityBridge();
    if (!bridge) {
      return;
    }

    let active = true;
    let pushed = false;
    const accept = (value: unknown, source: 'push' | 'hydrate'): void => {
      if (!active || !isRuntimeConnectivitySnapshot(value)) {
        return;
      }
      // Subscribe runs before the hydrating query resolves, so a transition can
      // land first. Never let the older in-flight answer overwrite it.
      if (source === 'hydrate' && pushed) {
        return;
      }
      if (source === 'push') {
        pushed = true;
      }
      setSnapshot(value);
    };

    const unsubscribe = bridge.subscribe((value) => accept(value, 'push'));
    void Promise.resolve(bridge.get())
      .then((value) => accept(value, 'hydrate'))
      .catch(() => undefined);

    return () => {
      active = false;
      unsubscribe();
    };
  }, [enabled]);

  return snapshot;
}
