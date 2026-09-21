import type { HarnessEvent } from '@chirality/runtime-contracts/event-schema';

/**
 * A session-scoped, in-process channel for harness events that are produced
 * *outside* the SDK message stream — specifically the `tool.permission` events
 * emitted by `canUseTool` while the SDK is blocked awaiting a verdict. The
 * manager merges this channel into its live UIEvent stream so these events reach
 * the browser as `harness:event`s in real time (the manager's normal loop is
 * suspended on the SDK iterator during a pause and cannot surface them itself).
 */
export class SessionPermissionChannel {
  private readonly buffer: HarnessEvent[] = [];
  private waiter: ((result: IteratorResult<HarnessEvent>) => void) | null = null;
  private closed = false;

  publish(event: HarnessEvent): void {
    if (this.closed) {
      return;
    }
    const waiter = this.waiter;
    if (waiter) {
      this.waiter = null;
      waiter({ value: event, done: false });
      return;
    }
    this.buffer.push(event);
  }

  /** Resolves with the next event, or `done` once closed and drained. */
  next(): Promise<IteratorResult<HarnessEvent>> {
    if (this.buffer.length > 0) {
      return Promise.resolve({ value: this.buffer.shift() as HarnessEvent, done: false });
    }
    if (this.closed) {
      return Promise.resolve({ value: undefined as unknown as HarnessEvent, done: true });
    }
    return new Promise((resolve) => {
      this.waiter = resolve;
    });
  }

  /** Synchronously take any buffered events (used for a final flush). */
  drain(): HarnessEvent[] {
    const drained = [...this.buffer];
    this.buffer.length = 0;
    return drained;
  }

  close(): void {
    this.closed = true;
    const waiter = this.waiter;
    if (waiter) {
      this.waiter = null;
      waiter({ value: undefined as unknown as HarnessEvent, done: true });
    }
  }
}

export class PermissionEventChannelRegistry {
  private readonly channels = new Map<string, SessionPermissionChannel>();

  open(sessionId: string): SessionPermissionChannel {
    // Close any pre-existing channel for this session before replacing it, so a
    // re-`open` (an overlapping same-session turn, or a retried boot) cannot
    // strand the previous channel's parked waiter or leak it in the map.
    this.channels.get(sessionId)?.close();
    const channel = new SessionPermissionChannel();
    this.channels.set(sessionId, channel);
    return channel;
  }

  publish(sessionId: string, event: HarnessEvent): void {
    this.channels.get(sessionId)?.publish(event);
  }

  /**
   * Tear down a session channel. When `channel` is supplied, only close+delete
   * when it is still the registered instance — so a stale turn's teardown cannot
   * close a newer same-session turn's channel that has since replaced it in the
   * map (DESIGN §5.3 identity guard). Always closes the passed instance itself.
   */
  close(sessionId: string, channel?: SessionPermissionChannel): void {
    const registered = this.channels.get(sessionId);
    if (channel && registered !== channel) {
      // A newer turn owns this session's slot; only retire our own instance.
      channel.close();
      return;
    }
    if (registered) {
      registered.close();
      this.channels.delete(sessionId);
    }
  }
}

type PermissionEventChannelGlobal = typeof globalThis & {
  __CHIRALITY_PERMISSION_EVENT_CHANNEL__?: PermissionEventChannelRegistry;
};

const channelGlobal = globalThis as PermissionEventChannelGlobal;

export function getPermissionEventChannel(): PermissionEventChannelRegistry {
  if (!channelGlobal.__CHIRALITY_PERMISSION_EVENT_CHANNEL__) {
    channelGlobal.__CHIRALITY_PERMISSION_EVENT_CHANNEL__ = new PermissionEventChannelRegistry();
  }
  return channelGlobal.__CHIRALITY_PERMISSION_EVENT_CHANNEL__;
}

export function resetPermissionEventChannelForTests(): void {
  delete channelGlobal.__CHIRALITY_PERMISSION_EVENT_CHANNEL__;
}
