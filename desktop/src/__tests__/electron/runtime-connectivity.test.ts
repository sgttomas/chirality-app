import { describe, expect, it, vi } from 'vitest';
import {
  createRuntimeBindingSupervisor,
  DEFAULT_BIND_RETRY_DELAYS_MS,
  DEFAULT_STEADY_PROBE_INTERVAL_MS,
  RUNTIME_CONNECTIVITY_CHANGED_CHANNEL,
  RUNTIME_CONNECTIVITY_QUERY_CHANNEL,
  type RuntimeConnectivitySnapshot
} from '../../../electron/runtime-connectivity';

/**
 * Deterministic timer queue. The supervisor's whole purpose is the *timing* of
 * retries, so the delays it asks for are asserted directly rather than waited
 * out; nothing here sleeps.
 */
function createClock() {
  const scheduled: Array<{ handle: number; handler: () => void; delayMs: number }> = [];
  let nextHandle = 1;
  let currentMs = 0;
  return {
    delays: [] as number[],
    setTimeoutFn(handler: () => void, delayMs: number): unknown {
      const handle = nextHandle++;
      this.delays.push(delayMs);
      scheduled.push({ handle, handler, delayMs });
      return handle;
    },
    clearTimeoutFn(handle: unknown): void {
      const index = scheduled.findIndex((entry) => entry.handle === handle);
      if (index >= 0) {
        scheduled.splice(index, 1);
      }
    },
    pending(): number {
      return scheduled.length;
    },
    /** Fire the single pending timer. */
    async tick(): Promise<void> {
      const next = scheduled.shift();
      if (!next) {
        throw new Error('No timer is pending');
      }
      currentMs += next.delayMs;
      next.handler();
      // Let the async cycle the timer kicked off run to completion.
      await Promise.resolve();
      await Promise.resolve();
      await Promise.resolve();
    },
    now(): Date {
      currentMs += 1;
      return new Date(currentMs);
    }
  };
}

type Harness = {
  clock: ReturnType<typeof createClock>;
  states: RuntimeConnectivitySnapshot[];
  supervisor: ReturnType<typeof createRuntimeBindingSupervisor>;
};

function harness(options: {
  bind: () => Promise<void>;
  probe?: () => Promise<boolean>;
}): Harness {
  const clock = createClock();
  const states: RuntimeConnectivitySnapshot[] = [];
  const supervisor = createRuntimeBindingSupervisor({
    bind: options.bind,
    probe: options.probe ?? (async () => true),
    onStateChange: (snapshot) => states.push(snapshot),
    setTimeoutFn: (handler, delayMs) => clock.setTimeoutFn(handler, delayMs),
    clearTimeoutFn: (handle) => clock.clearTimeoutFn(handle),
    now: () => clock.now()
  });
  return { clock, states, supervisor };
}

describe('runtime connectivity channels', () => {
  it('namespaces both IPC channels under the chirality prefix', () => {
    expect(RUNTIME_CONNECTIVITY_QUERY_CHANNEL).toBe('chirality:runtime-connectivity-query');
    expect(RUNTIME_CONNECTIVITY_CHANGED_CHANNEL).toBe(
      'chirality:runtime-connectivity-changed'
    );
  });

  it('walks the documented backoff ladder before settling', () => {
    expect(DEFAULT_BIND_RETRY_DELAYS_MS).toEqual([1_000, 2_000, 5_000]);
    expect(DEFAULT_STEADY_PROBE_INTERVAL_MS).toBe(10_000);
  });
});

describe('createRuntimeBindingSupervisor', () => {
  it('reports connected and starts steady probing when the first bind succeeds', async () => {
    const bind = vi.fn(async () => undefined);
    const { clock, states, supervisor } = harness({ bind });

    await supervisor.start();

    expect(bind).toHaveBeenCalledOnce();
    expect(supervisor.snapshot().state).toBe('connected');
    expect(supervisor.snapshot().lastError).toBeNull();
    expect(states.map((entry) => entry.state)).toEqual(['connected']);
    expect(clock.delays).toEqual([DEFAULT_STEADY_PROBE_INTERVAL_MS]);

    supervisor.stop();
  });

  it('retries a failing bind on 1s/2s/5s then settles at the steady interval', async () => {
    const bind = vi.fn(async () => {
      throw new Error('daemon socket refused');
    });
    const { clock, states, supervisor } = harness({ bind });

    await supervisor.start();
    expect(supervisor.snapshot().state).toBe('disconnected');
    expect(supervisor.snapshot().lastError).toBe('daemon socket refused');
    expect(supervisor.snapshot().failedAttempts).toBe(1);

    for (let attempt = 0; attempt < 4; attempt += 1) {
      await clock.tick();
    }

    expect(bind).toHaveBeenCalledTimes(5);
    expect(clock.delays).toEqual([1_000, 2_000, 5_000, 10_000, 10_000]);
    expect(supervisor.snapshot().failedAttempts).toBe(5);
    // A single transition: repeated identical failures must not spam the renderer.
    expect(states).toHaveLength(1);
    expect(states[0]?.state).toBe('disconnected');

    supervisor.stop();
  });

  it('rebinds and reports connected once a previously absent daemon appears', async () => {
    let available = false;
    const bind = vi.fn(async () => {
      if (!available) {
        throw new Error('project binding unavailable');
      }
    });
    const { clock, states, supervisor } = harness({ bind });

    await supervisor.start();
    expect(supervisor.snapshot().state).toBe('disconnected');

    available = true;
    await clock.tick();

    expect(supervisor.snapshot().state).toBe('connected');
    expect(supervisor.snapshot().failedAttempts).toBe(0);
    expect(states.map((entry) => entry.state)).toEqual(['disconnected', 'connected']);

    supervisor.stop();
  });

  it('detects a daemon that stops responding and rebinds without a renderer call', async () => {
    let daemonUp = true;
    const bind = vi.fn(async () => {
      if (!daemonUp) {
        throw new Error('daemon gone');
      }
    });
    const probe = vi.fn(async () => daemonUp);
    const { clock, states, supervisor } = harness({ bind, probe });

    await supervisor.start();
    expect(supervisor.snapshot().state).toBe('connected');

    // The daemon dies between probes: the probe fails, connectivity drops, and an
    // immediate rebind is attempted in the same cycle.
    daemonUp = false;
    await clock.tick();
    expect(probe).toHaveBeenCalledTimes(1);
    expect(supervisor.snapshot().state).toBe('disconnected');
    expect(states.map((entry) => entry.state)).toEqual([
      'connected',
      'disconnected',
      'disconnected'
    ]);

    // launchd restarts it; the next scheduled cycle reconnects with no UI action.
    daemonUp = true;
    await clock.tick();
    expect(supervisor.snapshot().state).toBe('connected');
    expect(states[states.length - 1]?.state).toBe('connected');

    supervisor.stop();
  });

  it('treats a throwing probe as an unreachable daemon', async () => {
    let bindOk = true;
    const bind = vi.fn(async () => {
      if (!bindOk) {
        throw new Error('still gone');
      }
    });
    const probe = vi.fn(async () => {
      throw new Error('socket hung up');
    });
    const { clock, supervisor } = harness({ bind, probe });

    await supervisor.start();
    bindOk = false;
    await clock.tick();

    expect(supervisor.snapshot().state).toBe('disconnected');
    expect(supervisor.snapshot().lastError).toBe('still gone');

    supervisor.stop();
  });

  it('redacts credential-shaped text out of the surfaced failure reason', async () => {
    const bind = vi.fn(async () => {
      throw new Error('refused with Bearer sk-secret-value while binding');
    });
    const { supervisor } = harness({ bind });

    await supervisor.start();

    expect(supervisor.snapshot().lastError).toBe('refused with [redacted] while binding');
    expect(supervisor.snapshot().lastError).not.toContain('sk-secret-value');

    supervisor.stop();
  });

  it('refreshNow cancels the pending backoff and retries immediately', async () => {
    let available = false;
    const bind = vi.fn(async () => {
      if (!available) {
        throw new Error('unavailable');
      }
    });
    const { clock, supervisor } = harness({ bind });

    await supervisor.start();
    expect(clock.pending()).toBe(1);

    available = true;
    await supervisor.refreshNow();

    expect(supervisor.snapshot().state).toBe('connected');
    expect(bind).toHaveBeenCalledTimes(2);

    supervisor.stop();
  });

  it('stop halts the loop and start is idempotent', async () => {
    const bind = vi.fn(async () => undefined);
    const { clock, supervisor } = harness({ bind });

    await supervisor.start();
    await supervisor.start();
    expect(bind).toHaveBeenCalledOnce();

    supervisor.stop();
    expect(clock.pending()).toBe(0);

    // A cycle that fires after stop must not reschedule anything.
    await supervisor.refreshNow();
    expect(clock.pending()).toBe(0);
    expect(bind).toHaveBeenCalledOnce();
  });

  it('coalesces a refresh that arrives mid-cycle instead of stalling', async () => {
    // Regression: `refreshNow()` cancels the pending timer *before* running a
    // cycle. When a cycle was already in flight the new one returned
    // immediately, so nothing rescheduled the timer and the supervisor stopped
    // probing forever. Reachable from two quick `onDaemonAvailable` calls;
    // routine once a filesystem watcher drives refreshes, because fs events
    // arrive in bursts.
    // The first bind blocks until released, then fails; the second succeeds. So
    // a refresh that arrives mid-cycle has real work to do, and dropping it
    // would leave the supervisor disconnected with no timer pending.
    let releaseBind: (() => void) | undefined;
    let bindCalls = 0;
    const bind = vi.fn(async () => {
      bindCalls += 1;
      if (bindCalls === 1) {
        await new Promise<void>((resolve) => {
          releaseBind = resolve;
        });
        throw new Error('daemon socket refused');
      }
    });
    const { clock, supervisor } = harness({ bind });

    const started = supervisor.start();
    expect(bind).toHaveBeenCalledOnce();

    // A watcher event lands while the first bind is still awaiting.
    const refreshed = supervisor.refreshNow();
    expect(bind).toHaveBeenCalledOnce();

    releaseBind?.();
    await started;
    await refreshed;

    // The deferred refresh ran rather than being dropped...
    expect(bind).toHaveBeenCalledTimes(2);
    expect(supervisor.snapshot().state).toBe('connected');
    // ...and the supervisor is still scheduled, not stalled.
    expect(clock.pending()).toBe(1);
    expect(clock.delays.at(-1)).toBe(DEFAULT_STEADY_PROBE_INTERVAL_MS);

    supervisor.stop();
  });

  it('collapses a burst of mid-cycle refreshes into one follow-up cycle', async () => {
    let releaseBind: (() => void) | undefined;
    let bindCalls = 0;
    const bind = vi.fn(async () => {
      bindCalls += 1;
      if (bindCalls === 1) {
        await new Promise<void>((resolve) => {
          releaseBind = resolve;
        });
        throw new Error('daemon socket refused');
      }
    });
    const { clock, supervisor } = harness({ bind });

    const started = supervisor.start();
    const refreshes = [
      supervisor.refreshNow(),
      supervisor.refreshNow(),
      supervisor.refreshNow()
    ];

    releaseBind?.();
    await started;
    await Promise.all(refreshes);

    // Three events, one extra cycle — a rename storm cannot become a busy loop.
    expect(bind).toHaveBeenCalledTimes(2);
    expect(clock.pending()).toBe(1);

    supervisor.stop();
  });

  it('does not run a deferred refresh after stop', async () => {
    let releaseBind: (() => void) | undefined;
    let bindCalls = 0;
    const bind = vi.fn(async () => {
      bindCalls += 1;
      if (bindCalls === 1) {
        await new Promise<void>((resolve) => {
          releaseBind = resolve;
        });
      }
    });
    const { clock, supervisor } = harness({ bind });

    const started = supervisor.start();
    const refreshed = supervisor.refreshNow();
    supervisor.stop();

    releaseBind?.();
    await started;
    await refreshed;

    expect(bind).toHaveBeenCalledOnce();
    expect(clock.pending()).toBe(0);
  });

  it('exposes a queryable snapshot before the first cycle completes', () => {
    const { supervisor } = harness({ bind: async () => undefined });
    const snapshot = supervisor.snapshot();
    expect(snapshot.state).toBe('connecting');
    expect(snapshot.failedAttempts).toBe(0);
    expect(snapshot.lastError).toBeNull();
    expect(typeof snapshot.changedAt).toBe('string');
  });
});
