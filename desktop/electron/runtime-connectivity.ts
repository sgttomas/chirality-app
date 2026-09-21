/**
 * Runtime-daemon connectivity: shared contract plus the main-process supervisor
 * that keeps the desktop harness bound to the daemon.
 *
 * Before this module the GUI bound its harness routes exactly once during
 * startup and swallowed any failure. If the daemon was not reachable at that
 * instant — the common case when the daemon had been terminated at app-launch
 * time — every subsequent harness request failed with `ENGINE_UNAVAILABLE`
 * until the operator manually reloaded, and nothing in the UI said why. The only
 * rebind path was the daemon-status IPC handler, which depends on a renderer
 * actually opening the runtime settings panel.
 *
 * The supervisor instead owns binding as a main-process concern: it retries with
 * backoff until it binds, keeps probing afterwards, rebinds when the daemon
 * disappears and returns, and publishes every transition so the top bar can show
 * runtime connectivity.
 *
 * Kept free of `electron` imports so it can be unit-tested under plain Node.
 */

export const RUNTIME_CONNECTIVITY_QUERY_CHANNEL = 'chirality:runtime-connectivity-query';
export const RUNTIME_CONNECTIVITY_CHANGED_CHANNEL =
  'chirality:runtime-connectivity-changed';

export type RuntimeConnectivityState = 'connecting' | 'connected' | 'disconnected';

export type RuntimeConnectivitySnapshot = {
  state: RuntimeConnectivityState;
  /** Consecutive failed bind attempts since the last successful bind. */
  failedAttempts: number;
  /** Redacted reason for the most recent failure, or `null` when connected. */
  lastError: string | null;
  /** ISO timestamp of the most recent state change. */
  changedAt: string;
};

/**
 * Backoff ladder for bind retries: fast enough that a daemon restart is picked
 * up before an operator notices, slow enough to be a negligible steady-state
 * cost. The final value is reused for every later attempt and for the
 * steady-state liveness probe.
 *
 * These are the *fallback* timings. `runtime-socket-watch.ts` drives
 * `refreshNow()` from the control socket appearing or disappearing, so a
 * graceful daemon stop and a daemon coming back are both acted on in
 * milliseconds and never wait for a rung of this ladder. The ladder still
 * governs the cases the filesystem cannot report — a SIGKILLed daemon leaves
 * its socket file behind, and a listening-but-unhealthy daemon changes nothing
 * on disk.
 */
export const DEFAULT_BIND_RETRY_DELAYS_MS: readonly number[] = [1_000, 2_000, 5_000];
export const DEFAULT_STEADY_PROBE_INTERVAL_MS = 10_000;

export type RuntimeBindingSupervisorOptions = {
  /** Perform the actual harness binding. Rejects when the daemon is unusable. */
  bind: () => Promise<void>;
  /** Cheap liveness probe used once bound. Resolves `false` when unreachable. */
  probe: () => Promise<boolean>;
  /** Called on every state transition (never for an unchanged state). */
  onStateChange?: (snapshot: RuntimeConnectivitySnapshot) => void;
  log?: (level: 'info' | 'warn' | 'error', event: string, detail?: unknown) => void;
  retryDelaysMs?: readonly number[];
  steadyProbeIntervalMs?: number;
  setTimeoutFn?: (handler: () => void, delayMs: number) => unknown;
  clearTimeoutFn?: (handle: unknown) => void;
  now?: () => Date;
};

export type RuntimeBindingSupervisor = {
  /**
   * Begin the bind/retry/probe loop. Idempotent. The returned promise settles
   * after the *first* cycle so startup can still await an initial bind attempt;
   * every later cycle is driven by timers and never blocks a caller.
   */
  start: () => Promise<void>;
  /** Stop all scheduled work. Idempotent. */
  stop: () => void;
  /** Current connectivity snapshot. */
  snapshot: () => RuntimeConnectivitySnapshot;
  /**
   * Force an immediate bind/probe cycle, cancelling any pending timer. Used when
   * an external signal (an operator starting the daemon from the UI) makes
   * waiting out the backoff pointless.
   */
  refreshNow: () => Promise<void>;
};

const CREDENTIALISH_PATTERN = /(?:Bearer|token|credential|api[_ -]?key)\s+\S+/giu;

function describeError(error: unknown, fallback: string): string {
  const message =
    error instanceof Error && error.message.trim() ? error.message.trim() : fallback;
  return message.replaceAll(CREDENTIALISH_PATTERN, '[redacted]');
}

export function createRuntimeBindingSupervisor(
  options: RuntimeBindingSupervisorOptions
): RuntimeBindingSupervisor {
  const retryDelaysMs =
    options.retryDelaysMs && options.retryDelaysMs.length > 0
      ? options.retryDelaysMs
      : DEFAULT_BIND_RETRY_DELAYS_MS;
  const steadyProbeIntervalMs =
    options.steadyProbeIntervalMs ?? DEFAULT_STEADY_PROBE_INTERVAL_MS;
  const schedule = options.setTimeoutFn ?? ((handler, delayMs) => setTimeout(handler, delayMs));
  const cancel =
    options.clearTimeoutFn ?? ((handle: unknown) => clearTimeout(handle as NodeJS.Timeout));
  const now = options.now ?? (() => new Date());
  const log = options.log ?? (() => undefined);

  let snapshot: RuntimeConnectivitySnapshot = {
    state: 'connecting',
    failedAttempts: 0,
    lastError: null,
    changedAt: now().toISOString()
  };
  let timer: unknown;
  let running = false;
  let cycleInFlight = false;
  /**
   * A refresh arrived while a cycle was already running. Without this the
   * refresh would be dropped *after* its caller had already cancelled the
   * pending timer, leaving the supervisor with no scheduled work and no cycle
   * to reschedule it — a permanent stall. Reachable before the socket watcher
   * existed (two `onDaemonAvailable` calls in quick succession); routine with
   * it, because filesystem events arrive in bursts.
   */
  let refreshPending = false;

  const publish = (
    state: RuntimeConnectivityState,
    lastError: string | null,
    failedAttempts: number
  ): void => {
    const changed = state !== snapshot.state || lastError !== snapshot.lastError;
    snapshot = {
      state,
      failedAttempts,
      lastError,
      changedAt: changed ? now().toISOString() : snapshot.changedAt
    };
    if (changed) {
      options.onStateChange?.(snapshot);
    }
  };

  const clearTimer = (): void => {
    if (timer !== undefined) {
      cancel(timer);
      timer = undefined;
    }
  };

  const scheduleNext = (delayMs: number): void => {
    clearTimer();
    if (!running) {
      return;
    }
    timer = schedule(() => {
      timer = undefined;
      void runCycle();
    }, delayMs);
  };

  /**
   * Delay before the retry that follows the Nth consecutive failure: walk the
   * ladder once, then settle into the steady probe interval forever.
   */
  const retryDelayFor = (failedAttempts: number): number =>
    retryDelaysMs[failedAttempts - 1] ?? steadyProbeIntervalMs;

  async function runCycle(): Promise<void> {
    if (!running) {
      return;
    }
    if (cycleInFlight) {
      // Coalesce rather than drop: the in-flight cycle re-runs when it finishes.
      refreshPending = true;
      return;
    }
    cycleInFlight = true;
    try {
      // While bound, a cheap probe is enough; only a lost daemon triggers a
      // full rebind, so the steady-state cost is one status call per interval.
      if (snapshot.state === 'connected') {
        let reachable = false;
        try {
          reachable = await options.probe();
        } catch (error) {
          log('warn', 'runtime.connectivity.probe_failed', {
            reason: describeError(error, 'probe threw')
          });
          reachable = false;
        }
        if (reachable) {
          scheduleNext(steadyProbeIntervalMs);
          return;
        }
        publish('disconnected', 'Runtime daemon stopped responding', 0);
        log('warn', 'runtime.connectivity.lost');
        // Fall through and attempt an immediate rebind.
      }

      const attemptsBeforeBind = snapshot.failedAttempts;
      try {
        await options.bind();
        const reconnected = snapshot.state !== 'connected';
        publish('connected', null, 0);
        if (reconnected) {
          log('info', 'runtime.connectivity.bound', { priorFailedAttempts: attemptsBeforeBind });
        }
        scheduleNext(steadyProbeIntervalMs);
      } catch (error) {
        const failedAttempts = snapshot.failedAttempts + 1;
        const reason = describeError(error, 'project binding unavailable');
        publish('disconnected', reason, failedAttempts);
        // The first few failures are the normal "daemon not up yet" case; only
        // escalate the level once retrying has clearly stopped helping.
        log(failedAttempts > retryDelaysMs.length ? 'error' : 'warn', 'runtime.connectivity.bind_failed', {
          attempt: failedAttempts,
          reason
        });
        scheduleNext(retryDelayFor(failedAttempts));
      }
    } finally {
      cycleInFlight = false;
    }
    if (refreshPending && running) {
      refreshPending = false;
      clearTimer();
      await runCycle();
    }
  }

  return {
    start(): Promise<void> {
      if (running) {
        return Promise.resolve();
      }
      running = true;
      log('info', 'runtime.connectivity.supervisor_started');
      return runCycle();
    },
    stop(): void {
      running = false;
      refreshPending = false;
      clearTimer();
    },
    snapshot: () => snapshot,
    refreshNow: async (): Promise<void> => {
      clearTimer();
      await runCycle();
    }
  };
}
