/**
 * Renderer-side view of runtime-daemon connectivity.
 *
 * The main process supervises the harness binding and publishes each transition;
 * this module is the pure mapping from that snapshot to top-bar presentation, so
 * the mapping is unit-testable without a DOM or an Electron bridge.
 *
 * Types are duplicated rather than imported from `electron/` on purpose: the
 * renderer bundle must not reach into main-process modules, and the boundary is
 * an IPC payload shape, not a shared implementation.
 */

export type RuntimeConnectivityState = 'connecting' | 'connected' | 'disconnected';

export type RuntimeConnectivitySnapshot = {
  state: RuntimeConnectivityState;
  failedAttempts: number;
  lastError: string | null;
  changedAt: string;
};

export type RuntimeConnectivityBridge = {
  get: () => Promise<RuntimeConnectivitySnapshot | null>;
  subscribe: (listener: (snapshot: RuntimeConnectivitySnapshot) => void) => () => void;
};

/** Tone names map onto the existing status palette; see globals.css. */
export type RuntimeConnectivityTone = 'ready' | 'pending' | 'error';

export type RuntimeConnectivityPresentation = {
  tone: RuntimeConnectivityTone;
  label: string;
  title: string;
};

export function isRuntimeConnectivitySnapshot(
  value: unknown
): value is RuntimeConnectivitySnapshot {
  if (typeof value !== 'object' || value === null) {
    return false;
  }
  const candidate = value as Partial<RuntimeConnectivitySnapshot>;
  return (
    (candidate.state === 'connecting' ||
      candidate.state === 'connected' ||
      candidate.state === 'disconnected') &&
    typeof candidate.failedAttempts === 'number' &&
    typeof candidate.changedAt === 'string' &&
    (candidate.lastError === null || typeof candidate.lastError === 'string')
  );
}

/**
 * True when `next` is the moment the daemon became reachable again.
 *
 * "Again" is load-bearing. The first snapshot a renderer ever observes has no
 * predecessor, so it is never a reconnect: whatever mounted alongside it already
 * fetched under that state. Only an observed non-connected → connected step means
 * "requests that failed a moment ago would succeed now", which is the one event
 * worth re-fetching on.
 *
 * `connecting` counts as non-connected on purpose. The live defect was a renderer
 * that mounted while the first bind was still in flight: its fetches failed with
 * ENGINE_UNAVAILABLE and nothing ever re-issued them. Treating `connecting` as
 * connected would leave exactly that case unfixed.
 */
export function isRuntimeReconnect(
  previous: RuntimeConnectivitySnapshot | null,
  next: RuntimeConnectivitySnapshot
): boolean {
  return previous !== null && previous.state !== 'connected' && next.state === 'connected';
}

/**
 * Derive the top-bar chip from a snapshot.
 *
 * Returns `null` when there is nothing to say — no snapshot at all, which is the
 * browser/SSR case where no desktop bridge exists. A web render must not claim a
 * runtime state it cannot observe, so the chip is absent rather than "unknown".
 */
export function deriveRuntimeConnectivityPresentation(
  snapshot: RuntimeConnectivitySnapshot | null
): RuntimeConnectivityPresentation | null {
  if (snapshot === null) {
    return null;
  }

  if (snapshot.state === 'connected') {
    return {
      tone: 'ready',
      label: 'connected',
      title: 'Runtime daemon connected'
    };
  }

  if (snapshot.state === 'connecting') {
    return {
      tone: 'pending',
      label: 'connecting',
      title: 'Connecting to the runtime daemon'
    };
  }

  // Disconnected. The attempt count is the operator's cue for "transient restart"
  // versus "this is not coming back on its own", and the reason is the detail that
  // used to exist only in an invisible console warning.
  const attempts = snapshot.failedAttempts;
  const retryNote = attempts > 1 ? ` after ${attempts} attempts` : '';
  return {
    tone: 'error',
    label: 'offline',
    title: snapshot.lastError
      ? `Runtime daemon unreachable${retryNote}: ${snapshot.lastError}`
      : `Runtime daemon unreachable${retryNote}`
  };
}
