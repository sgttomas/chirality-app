'use client';

import React, { useCallback, useState } from 'react';
import { deriveRuntimeConnectivityPresentation, type RuntimeConnectivitySnapshot } from '../../lib/shell/runtime-connectivity';
import { useRuntimeConnectivitySnapshot } from '../shell/runtime-connectivity-provider';

/**
 * The preload's `runtime.service.restart()` result: the main process either
 * relaunched the service child or explains why it could not. Mirrors
 * `electron/runtime-control-ipc-contract.ts` as an IPC payload shape.
 */
export type RuntimeServiceRestartResult =
  | { ok: true; service: { status: string } }
  | { ok: false; error: string };

export type RuntimeServiceRestart = () => Promise<RuntimeServiceRestartResult>;

export function resolveRuntimeServiceRestart(): RuntimeServiceRestart | null {
  if (typeof window === 'undefined') return null;
  const restart = window.chirality?.runtime?.service?.restart;
  return typeof restart === 'function' ? restart : null;
}

/**
 * Runtime group of Settings for the App-owned Runtime service (D-GOV-43). The
 * service is a child of the App: it starts with the App, restarts on crash and
 * stops on quit, so there is nothing to install or uninstall. This view reports
 * the main process's connectivity snapshot and, once the service is stopped,
 * offers the one operator action left: a retry after the App gave up
 * restarting the service on its own.
 */
export function RuntimeStatusView({
  snapshot,
  restart = null
}: {
  snapshot: RuntimeConnectivitySnapshot | null;
  restart?: RuntimeServiceRestart | null;
}): JSX.Element {
  const [restarting, setRestarting] = useState(false);
  const [restartError, setRestartError] = useState<string | null>(null);
  const presentation = deriveRuntimeConnectivityPresentation(snapshot);
  const label = !presentation ? 'Unavailable outside Chirality Desktop'
    : presentation.tone === 'ready' ? 'Running'
    : presentation.tone === 'pending' ? 'Starting'
    : 'Stopped';

  const handleRestart = useCallback(() => {
    if (!restart || restarting) return;
    setRestarting(true);
    setRestartError(null);
    void restart().then(
      (result) => {
        if (!result.ok) setRestartError(result.error);
      },
      (error: unknown) => {
        setRestartError(error instanceof Error && error.message ? error.message : 'Unable to restart the runtime service');
      }
    ).finally(() => setRestarting(false));
  }, [restart, restarting]);

  return (
    <section className="runtime-settings" aria-labelledby="runtime-settings-title">
      <h3 className="api-key-settings-title" id="runtime-settings-title">Runtime</h3>
      <p>
        <span className="runtime-status" data-running={presentation?.tone === 'ready' ? 'true' : 'false'} title={presentation?.title}>{label}</span>
      </p>
      {presentation?.tone === 'error' ? (
        <>
          <p className="api-key-error">{presentation.title}. Chirality restarts its Runtime service on its own; if this persists, quit and reopen the App.</p>
          {restart ? (
            <p>
              <button
                type="button"
                className="button-muted"
                onClick={handleRestart}
                disabled={restarting}
                aria-busy={restarting}
                data-testid="runtime-service-restart"
              >
                {restarting ? 'Restarting Runtime' : 'Restart Runtime'}
              </button>
            </p>
          ) : null}
          {restartError ? <p className="api-key-error">{restartError}</p> : null}
        </>
      ) : null}
      <p className="api-key-hint">
        The Runtime service and the Codex App Server are started and stopped by Chirality itself. Sign-in is under Account.
      </p>
    </section>
  );
}

export function RuntimeStatus(): JSX.Element {
  const snapshot = useRuntimeConnectivitySnapshot();
  return <RuntimeStatusView snapshot={snapshot} restart={resolveRuntimeServiceRestart()} />;
}
