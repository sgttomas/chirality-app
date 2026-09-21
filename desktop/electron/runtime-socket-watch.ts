/**
 * Watch the runtime control socket's *presence* and report every change.
 *
 * The connectivity supervisor alone can only learn that the daemon went away by
 * failing its next liveness probe, so a loss costs up to one steady probe
 * interval (10 s) to notice and then walks the retry ladder from the beginning
 * to get back — even when the daemon returned almost immediately. Measured on
 * the operator's machine, one daemon bounce cost 3.9 s to detect plus 4.3 s of
 * ladder *after* the replacement was already listening, on top of the restart
 * itself.
 *
 * The filesystem already carries both signals, exactly and immediately:
 *
 * - **Graceful stop** unlinks the socket (`RuntimeDaemon.stop()` closes the
 *   server and then `unlink`s `control.sock`). The unlink *is* the loss event,
 *   delivered in milliseconds.
 * - **Start** re-creates it (`server.listen(socketPath)`), and the operator
 *   token is written before the listen, so the socket appearing means the
 *   daemon is ready to answer — not merely that a process exists.
 *
 * So one watcher gives instant loss detection and instant recovery, and the
 * ladder becomes a fallback rather than the normal path.
 *
 * **Known limitation, by construction:** `SIGKILL` leaves the socket file
 * behind, so an ungraceful death produces no unlink and no event. Detection of
 * that case still costs one steady probe interval. The subsequent *recovery* is
 * still instant, because the replacement daemon reclaims the stale path by
 * unlinking and re-listening, which the watcher does see.
 *
 * The directory is watched rather than the socket itself: `fs.watch` on a path
 * that does not exist throws, and a watch on the file would not survive the
 * unlink/re-create cycle that is the entire point.
 *
 * Kept free of `electron` imports, with every effect injectable, so the
 * behaviour is testable under plain Node.
 */

import { watch, type FSWatcher } from 'node:fs';
import { existsSync, mkdirSync } from 'node:fs';
import path from 'node:path';

export type SocketPresenceLogger = (
  level: 'info' | 'warn' | 'error',
  event: string,
  detail?: unknown
) => void;

export type SocketWatchHandle = {
  close: () => void;
  on: (event: 'error', listener: (error: unknown) => void) => void;
};

export type SocketPresenceWatcherOptions = {
  /** Absolute path of the control socket. Its directory is what gets watched. */
  socketPath: string;
  /**
   * Called only when presence actually changes, never for a repeat of the
   * current value. `present` is the socket's state after the change.
   */
  onChange: (present: boolean) => void;
  log?: SocketPresenceLogger;
  /**
   * Shortest gap between two `onChange` deliveries. A rename storm, or a daemon
   * restarting in a tight loop, must not turn the supervisor's rebind into a
   * busy loop. Small enough to stay well inside the 1 s detection budget.
   */
  minChangeIntervalMs?: number;
  /** Delay before re-establishing a watch that errored out. */
  rewatchDelayMs?: number;
  watchFn?: (directory: string, listener: () => void) => SocketWatchHandle;
  existsFn?: (candidate: string) => boolean;
  ensureDirectoryFn?: (directory: string) => void;
  setTimeoutFn?: (handler: () => void, delayMs: number) => unknown;
  clearTimeoutFn?: (handle: unknown) => void;
};

export type SocketPresenceWatcher = {
  /** Begin watching. Idempotent. Never throws — a failed watch degrades to the probe. */
  start: () => void;
  /** Stop watching and cancel any pending re-watch. Idempotent. */
  stop: () => void;
  /** Last observed presence. */
  present: () => boolean;
};

export const DEFAULT_MIN_CHANGE_INTERVAL_MS = 250;
export const DEFAULT_REWATCH_DELAY_MS = 5_000;

export function createSocketPresenceWatcher(
  options: SocketPresenceWatcherOptions
): SocketPresenceWatcher {
  const directory = path.dirname(options.socketPath);
  const log = options.log ?? (() => undefined);
  const exists = options.existsFn ?? ((candidate: string) => existsSync(candidate));
  const minChangeIntervalMs = options.minChangeIntervalMs ?? DEFAULT_MIN_CHANGE_INTERVAL_MS;
  const rewatchDelayMs = options.rewatchDelayMs ?? DEFAULT_REWATCH_DELAY_MS;
  const schedule =
    options.setTimeoutFn ?? ((handler: () => void, delayMs: number) => setTimeout(handler, delayMs));
  const cancel =
    options.clearTimeoutFn ?? ((handle: unknown) => clearTimeout(handle as NodeJS.Timeout));
  const ensureDirectory =
    options.ensureDirectoryFn ??
    ((target: string) => {
      mkdirSync(target, { recursive: true, mode: 0o700 });
    });
  const startWatch =
    options.watchFn ??
    ((target: string, listener: () => void): SocketWatchHandle => {
      // `persistent: false` so a watcher can never be the reason the process
      // stays alive; the app's own event sources own the process lifetime.
      const watcher: FSWatcher = watch(target, { persistent: false }, () => listener());
      return {
        close: () => watcher.close(),
        on: (event, handler) => watcher.on(event, handler)
      };
    });

  let handle: SocketWatchHandle | undefined;
  let rewatchTimer: unknown;
  let settleTimer: unknown;
  let running = false;
  let present = false;
  let lastChangeAt = Number.NEGATIVE_INFINITY;

  const clearRewatch = (): void => {
    if (rewatchTimer !== undefined) {
      cancel(rewatchTimer);
      rewatchTimer = undefined;
    }
  };

  const clearSettle = (): void => {
    if (settleTimer !== undefined) {
      cancel(settleTimer);
      settleTimer = undefined;
    }
  };

  /**
   * Re-read presence and publish a change. Rate-limited: when events arrive
   * faster than the floor, the check is deferred once rather than dropped, so
   * the *final* state is always published.
   */
  const evaluate = (): void => {
    if (!running) {
      return;
    }
    const elapsed = Date.now() - lastChangeAt;
    if (elapsed < minChangeIntervalMs) {
      if (settleTimer === undefined) {
        settleTimer = schedule(() => {
          settleTimer = undefined;
          evaluate();
        }, minChangeIntervalMs - elapsed);
      }
      return;
    }

    let observed: boolean;
    try {
      observed = exists(options.socketPath);
    } catch (error) {
      log('warn', 'runtime.socket_watch.stat_failed', {
        error: error instanceof Error ? error.message : String(error)
      });
      return;
    }
    if (observed === present) {
      return;
    }
    present = observed;
    lastChangeAt = Date.now();
    log('info', 'runtime.socket_watch.presence_changed', { present });
    try {
      options.onChange(present);
    } catch (error) {
      log('error', 'runtime.socket_watch.handler_failed', {
        error: error instanceof Error ? error.message : String(error)
      });
    }
  };

  const attach = (): void => {
    if (!running || handle !== undefined) {
      return;
    }
    try {
      ensureDirectory(directory);
    } catch (error) {
      // Not fatal: the daemon creates this directory too, and the probe ladder
      // still covers connectivity while it is missing.
      log('warn', 'runtime.socket_watch.directory_unavailable', {
        directory,
        error: error instanceof Error ? error.message : String(error)
      });
    }
    try {
      handle = startWatch(directory, evaluate);
      handle.on('error', (error) => {
        log('warn', 'runtime.socket_watch.failed', {
          error: error instanceof Error ? error.message : String(error)
        });
        detach();
        scheduleRewatch();
      });
      log('info', 'runtime.socket_watch.started', { directory });
    } catch (error) {
      handle = undefined;
      log('warn', 'runtime.socket_watch.unavailable', {
        directory,
        error: error instanceof Error ? error.message : String(error)
      });
      scheduleRewatch();
    }
  };

  const detach = (): void => {
    if (handle !== undefined) {
      try {
        handle.close();
      } catch {
        // A watcher that cannot be closed is already unusable.
      }
      handle = undefined;
    }
  };

  const scheduleRewatch = (): void => {
    if (!running || rewatchTimer !== undefined) {
      return;
    }
    rewatchTimer = schedule(() => {
      rewatchTimer = undefined;
      attach();
      // The socket may well have changed while no watch was in place.
      evaluate();
    }, rewatchDelayMs);
  };

  return {
    start(): void {
      if (running) {
        return;
      }
      running = true;
      // Seed from the current state so the first real event is a genuine change
      // rather than a restatement of what the supervisor already knows.
      try {
        present = exists(options.socketPath);
      } catch {
        present = false;
      }
      attach();
    },
    stop(): void {
      running = false;
      clearRewatch();
      clearSettle();
      detach();
    },
    present: () => present
  };
}
