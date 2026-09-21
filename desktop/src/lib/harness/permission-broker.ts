import { randomUUID } from 'node:crypto';

/**
 * In-process broker that suspends an `ask`-mode `canUseTool` decision until a
 * human verdict arrives from the UI (or a timeout elapses). The SDK invokes
 * `canUseTool` in this (parent) process, and the `POST /api/harness/permission`
 * route runs in the same process, so a module/global singleton bridges them.
 *
 * This is the decision channel referenced in DESIGN §5.3: the permission overlay
 * emits a `tool.permission` (behavior `ask`) event, awaits this broker, and the
 * operator's inline approve/deny resolves the pending promise.
 */
export type PermissionVerdict = 'allow' | 'deny';

type PendingEntry = {
  key: string;
  sessionId: string;
  toolUseId: string;
  /**
   * Opaque per-turn identity (the turn's AbortController). Lets a turn's teardown
   * clear only the approvals it registered, so a stale turn's `finally` cannot
   * deny a newer same-session turn's pending approvals (DESIGN §5.3 identity guard).
   */
  turnToken?: unknown;
  resolve: (verdict: PermissionVerdict) => void;
  timer: ReturnType<typeof setTimeout> | null;
};

export const DEFAULT_PERMISSION_TIMEOUT_MS = 5 * 60 * 1000;

function resolveDefaultTimeoutMs(): number {
  const raw = process.env.CHIRALITY_PERMISSION_TIMEOUT_MS;
  if (!raw) {
    return DEFAULT_PERMISSION_TIMEOUT_MS;
  }
  const parsed = Number(raw);
  return Number.isFinite(parsed) && parsed >= 0 ? parsed : DEFAULT_PERMISSION_TIMEOUT_MS;
}

function keyFor(sessionId: string, toolUseId: string): string {
  return `${sessionId}::${toolUseId}`;
}

export class PermissionBroker {
  private readonly pending = new Map<string, PendingEntry>();

  /**
   * Register a pending approval and return a promise that resolves when a
   * verdict is delivered (or the timeout denies it). Returns the resolved
   * verdict and the `toolUseId` the UI must echo back to decide it.
   */
  request(input: {
    sessionId: string;
    toolUseId?: string;
    timeoutMs?: number;
    turnToken?: unknown;
  }): { toolUseId: string; verdict: Promise<PermissionVerdict> } {
    const toolUseId = input.toolUseId ?? `perm_${randomUUID()}`;
    const key = keyFor(input.sessionId, toolUseId);
    // A second request for the same key supersedes the first (deny the stale one).
    this.settle(key, 'deny');

    const verdict = new Promise<PermissionVerdict>((resolve) => {
      const timeoutMs = input.timeoutMs ?? resolveDefaultTimeoutMs();
      const timer =
        timeoutMs > 0
          ? setTimeout(() => {
              this.settle(key, 'deny');
            }, timeoutMs)
          : null;
      if (timer && typeof timer.unref === 'function') {
        timer.unref();
      }
      this.pending.set(key, {
        key,
        sessionId: input.sessionId,
        toolUseId,
        turnToken: input.turnToken,
        resolve,
        timer
      });
    });

    return { toolUseId, verdict };
  }

  /** Deliver an operator verdict. Returns false if no matching pending request. */
  decide(input: { sessionId: string; toolUseId: string; verdict: PermissionVerdict }): boolean {
    return this.settle(keyFor(input.sessionId, input.toolUseId), input.verdict);
  }

  /**
   * Resolve pending requests for a session (e.g. on interrupt or turn teardown).
   * When `turnToken` is given, only entries registered by that turn are settled,
   * so a stale turn's teardown cannot deny a newer same-session turn's approvals.
   * Omitting it (the explicit-interrupt path, which holds the one-turn lock and
   * therefore targets the single active turn) clears every pending entry.
   */
  clearSession(
    sessionId: string,
    verdict: PermissionVerdict = 'deny',
    turnToken?: unknown
  ): number {
    let count = 0;
    for (const entry of [...this.pending.values()]) {
      if (entry.sessionId !== sessionId) {
        continue;
      }
      if (turnToken !== undefined && entry.turnToken !== turnToken) {
        continue;
      }
      this.settle(entry.key, verdict);
      count += 1;
    }
    return count;
  }

  pendingCount(sessionId?: string): number {
    if (!sessionId) {
      return this.pending.size;
    }
    let count = 0;
    for (const entry of this.pending.values()) {
      if (entry.sessionId === sessionId) {
        count += 1;
      }
    }
    return count;
  }

  private settle(key: string, verdict: PermissionVerdict): boolean {
    const entry = this.pending.get(key);
    if (!entry) {
      return false;
    }
    if (entry.timer) {
      clearTimeout(entry.timer);
    }
    this.pending.delete(key);
    entry.resolve(verdict);
    return true;
  }
}

type PermissionBrokerGlobal = typeof globalThis & {
  __CHIRALITY_PERMISSION_BROKER__?: PermissionBroker;
};

const permissionBrokerGlobal = globalThis as PermissionBrokerGlobal;

export function getPermissionBroker(): PermissionBroker {
  if (!permissionBrokerGlobal.__CHIRALITY_PERMISSION_BROKER__) {
    permissionBrokerGlobal.__CHIRALITY_PERMISSION_BROKER__ = new PermissionBroker();
  }
  return permissionBrokerGlobal.__CHIRALITY_PERMISSION_BROKER__;
}

export function resetPermissionBrokerForTests(): void {
  delete permissionBrokerGlobal.__CHIRALITY_PERMISSION_BROKER__;
}
