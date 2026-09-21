import { afterEach, describe, expect, it, vi } from 'vitest';
import {
  createSocketPresenceWatcher,
  DEFAULT_MIN_CHANGE_INTERVAL_MS,
  DEFAULT_REWATCH_DELAY_MS,
  type SocketWatchHandle
} from '../../../electron/runtime-socket-watch';

const SOCKET = '/tmp/chirality-test/runtime/control.sock';
const DIRECTORY = '/tmp/chirality-test/runtime';

/**
 * Deterministic harness. The watcher's contract is *which* changes it reports
 * and how fast, so both the filesystem and the clock are injected; nothing here
 * touches a real disk and nothing sleeps.
 */
function createHarness(options: { initiallyPresent?: boolean } = {}) {
  const scheduled: Array<{ handle: number; handler: () => void; delayMs: number }> = [];
  let nextHandle = 1;
  let socketExists = options.initiallyPresent ?? false;
  let watchListener: (() => void) | undefined;
  let errorListener: ((error: unknown) => void) | undefined;
  const changes: boolean[] = [];
  const logs: Array<{ level: string; event: string }> = [];
  const ensuredDirectories: string[] = [];
  const watchedDirectories: string[] = [];
  let closeCount = 0;
  let watchThrows = false;

  const watcher = createSocketPresenceWatcher({
    socketPath: SOCKET,
    onChange: (present) => changes.push(present),
    log: (level, event) => logs.push({ level, event }),
    existsFn: () => socketExists,
    ensureDirectoryFn: (directory) => ensuredDirectories.push(directory),
    watchFn: (directory, listener): SocketWatchHandle => {
      if (watchThrows) {
        throw new Error('EMFILE: too many open files');
      }
      watchedDirectories.push(directory);
      watchListener = listener;
      return {
        close: () => {
          closeCount += 1;
          watchListener = undefined;
        },
        on: (_event, handler) => {
          errorListener = handler;
        }
      };
    },
    setTimeoutFn: (handler, delayMs) => {
      const handle = nextHandle++;
      scheduled.push({ handle, handler, delayMs });
      return handle;
    },
    clearTimeoutFn: (handle) => {
      const index = scheduled.findIndex((entry) => entry.handle === handle);
      if (index >= 0) scheduled.splice(index, 1);
    }
  });

  return {
    watcher,
    changes,
    logs,
    ensuredDirectories,
    watchedDirectories,
    get closeCount() {
      return closeCount;
    },
    get pendingTimers() {
      return scheduled.length;
    },
    get pendingDelays() {
      return scheduled.map((entry) => entry.delayMs);
    },
    failNextWatch(): void {
      watchThrows = true;
    },
    allowWatch(): void {
      watchThrows = false;
    },
    setSocket(present: boolean): void {
      socketExists = present;
    },
    /** Simulate one filesystem event in the watched directory. */
    fire(): void {
      watchListener?.();
    },
    fireError(error: unknown): void {
      errorListener?.(error);
    },
    watching(): boolean {
      return watchListener !== undefined;
    },
    runPendingTimers(): void {
      const due = scheduled.splice(0, scheduled.length);
      for (const entry of due) entry.handler();
    }
  };
}

describe('createSocketPresenceWatcher', () => {
  afterEach(() => {
    vi.restoreAllMocks();
  });

  it('watches the socket directory, not the socket itself', () => {
    const harness = createHarness();
    harness.watcher.start();
    // A watch on the socket path could not survive the unlink/re-create cycle
    // that is the whole point, and fs.watch throws on a path that is absent.
    expect(harness.watchedDirectories).toEqual([DIRECTORY]);
    expect(harness.ensuredDirectories).toEqual([DIRECTORY]);
    harness.watcher.stop();
  });

  it('reports the socket disappearing — the graceful-stop signal', () => {
    vi.spyOn(Date, 'now').mockReturnValue(1_000_000);
    const harness = createHarness({ initiallyPresent: true });
    harness.watcher.start();
    expect(harness.watcher.present()).toBe(true);
    expect(harness.changes).toEqual([]);

    harness.setSocket(false);
    harness.fire();

    expect(harness.changes).toEqual([false]);
    expect(harness.watcher.present()).toBe(false);
    harness.watcher.stop();
  });

  it('reports the socket appearing — the daemon-is-ready signal', () => {
    vi.spyOn(Date, 'now').mockReturnValue(1_000_000);
    const harness = createHarness({ initiallyPresent: false });
    harness.watcher.start();

    harness.setSocket(true);
    harness.fire();

    expect(harness.changes).toEqual([true]);
    harness.watcher.stop();
  });

  it('seeds from current presence so start() alone reports nothing', () => {
    const harness = createHarness({ initiallyPresent: true });
    harness.watcher.start();
    harness.fire();
    // The supervisor already attempts a bind at startup; restating the state it
    // is about to discover would be pure noise.
    expect(harness.changes).toEqual([]);
    harness.watcher.stop();
  });

  it('ignores events that do not change presence', () => {
    vi.spyOn(Date, 'now').mockReturnValue(1_000_000);
    const harness = createHarness({ initiallyPresent: false });
    harness.watcher.start();

    harness.fire();
    harness.fire();
    harness.fire();

    expect(harness.changes).toEqual([]);
    harness.watcher.stop();
  });

  it('reports a full unlink/re-create cycle as two changes', () => {
    const now = vi.spyOn(Date, 'now').mockReturnValue(1_000_000);
    const harness = createHarness({ initiallyPresent: true });
    harness.watcher.start();

    harness.setSocket(false);
    harness.fire();
    now.mockReturnValue(1_000_000 + DEFAULT_MIN_CHANGE_INTERVAL_MS);
    harness.setSocket(true);
    harness.fire();

    expect(harness.changes).toEqual([false, true]);
    harness.watcher.stop();
  });

  it('rate-limits a rename storm but still publishes the final state', () => {
    const now = vi.spyOn(Date, 'now').mockReturnValue(1_000_000);
    const harness = createHarness({ initiallyPresent: true });
    harness.watcher.start();

    harness.setSocket(false);
    harness.fire();
    expect(harness.changes).toEqual([false]);

    // Second change inside the floor: deferred, not dropped.
    now.mockReturnValue(1_000_010);
    harness.setSocket(true);
    harness.fire();
    harness.fire();
    harness.fire();
    expect(harness.changes).toEqual([false]);
    expect(harness.pendingDelays).toEqual([DEFAULT_MIN_CHANGE_INTERVAL_MS - 10]);

    now.mockReturnValue(1_000_000 + DEFAULT_MIN_CHANGE_INTERVAL_MS);
    harness.runPendingTimers();
    expect(harness.changes).toEqual([false, true]);
    harness.watcher.stop();
  });

  it('degrades to no watch, without throwing, when fs.watch fails', () => {
    const harness = createHarness();
    harness.failNextWatch();

    expect(() => harness.watcher.start()).not.toThrow();
    expect(harness.watching()).toBe(false);
    expect(harness.logs.map((entry) => entry.event)).toContain(
      'runtime.socket_watch.unavailable'
    );
    // Connectivity is still covered by the supervisor's probe ladder.
    expect(harness.pendingDelays).toEqual([DEFAULT_REWATCH_DELAY_MS]);
    harness.watcher.stop();
  });

  it('re-establishes a watch that errored, and re-evaluates on reattach', () => {
    vi.spyOn(Date, 'now').mockReturnValue(1_000_000);
    const harness = createHarness({ initiallyPresent: true });
    harness.watcher.start();

    harness.fireError(new Error('watch closed'));
    expect(harness.watching()).toBe(false);
    expect(harness.pendingDelays).toEqual([DEFAULT_REWATCH_DELAY_MS]);

    // The socket went away while nothing was watching.
    harness.setSocket(false);
    harness.runPendingTimers();

    expect(harness.watching()).toBe(true);
    expect(harness.changes).toEqual([false]);
    harness.watcher.stop();
  });

  it('survives a directory that cannot be created', () => {
    const harness = createSocketPresenceWatcher({
      socketPath: SOCKET,
      onChange: () => undefined,
      existsFn: () => false,
      ensureDirectoryFn: () => {
        throw new Error('EACCES');
      },
      watchFn: () => ({ close: () => undefined, on: () => undefined })
    });
    expect(() => harness.start()).not.toThrow();
    harness.stop();
  });

  it('does not let a throwing handler break the watcher', () => {
    vi.spyOn(Date, 'now').mockReturnValue(1_000_000);
    const logs: string[] = [];
    let socketExists = true;
    let listener: (() => void) | undefined;
    const watcher = createSocketPresenceWatcher({
      socketPath: SOCKET,
      onChange: () => {
        throw new Error('supervisor exploded');
      },
      log: (_level, event) => logs.push(event),
      existsFn: () => socketExists,
      ensureDirectoryFn: () => undefined,
      watchFn: (_directory, handler) => {
        listener = handler;
        return { close: () => undefined, on: () => undefined };
      }
    });
    watcher.start();
    socketExists = false;
    expect(() => listener?.()).not.toThrow();
    expect(logs).toContain('runtime.socket_watch.handler_failed');
    // Presence still advanced, so the next change is still detected.
    expect(watcher.present()).toBe(false);
    watcher.stop();
  });

  it('stops cleanly and reports nothing afterwards', () => {
    vi.spyOn(Date, 'now').mockReturnValue(1_000_000);
    const harness = createHarness({ initiallyPresent: true });
    harness.watcher.start();
    harness.watcher.stop();

    expect(harness.closeCount).toBe(1);
    expect(harness.pendingTimers).toBe(0);

    harness.setSocket(false);
    harness.fire();
    expect(harness.changes).toEqual([]);
  });

  it('is idempotent across repeated start and stop', () => {
    const harness = createHarness();
    harness.watcher.start();
    harness.watcher.start();
    expect(harness.watchedDirectories).toEqual([DIRECTORY]);
    harness.watcher.stop();
    harness.watcher.stop();
    expect(harness.closeCount).toBe(1);
  });
});
