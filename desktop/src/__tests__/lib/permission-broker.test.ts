import { afterEach, describe, expect, it } from 'vitest';
import {
  PermissionBroker,
  getPermissionBroker,
  resetPermissionBrokerForTests
} from '../../lib/harness/permission-broker';

afterEach(() => {
  resetPermissionBrokerForTests();
});

describe('PermissionBroker', () => {
  it('resolves a pending request when the matching verdict is delivered', async () => {
    const broker = new PermissionBroker();
    const { toolUseId, verdict } = broker.request({ sessionId: 's1', toolUseId: 'tool-1' });

    expect(toolUseId).toBe('tool-1');
    expect(broker.pendingCount('s1')).toBe(1);

    const decided = broker.decide({ sessionId: 's1', toolUseId: 'tool-1', verdict: 'allow' });
    expect(decided).toBe(true);
    await expect(verdict).resolves.toBe('allow');
    expect(broker.pendingCount('s1')).toBe(0);
  });

  it('returns false and leaves the request pending when the verdict does not match', async () => {
    const broker = new PermissionBroker();
    const { verdict } = broker.request({ sessionId: 's1', toolUseId: 'tool-1' });

    expect(broker.decide({ sessionId: 's1', toolUseId: 'other', verdict: 'allow' })).toBe(false);
    expect(broker.decide({ sessionId: 'other', toolUseId: 'tool-1', verdict: 'allow' })).toBe(false);
    expect(broker.pendingCount()).toBe(1);

    broker.decide({ sessionId: 's1', toolUseId: 'tool-1', verdict: 'deny' });
    await expect(verdict).resolves.toBe('deny');
  });

  it('denies on timeout', async () => {
    const broker = new PermissionBroker();
    const { verdict } = broker.request({ sessionId: 's1', toolUseId: 'tool-1', timeoutMs: 5 });
    await expect(verdict).resolves.toBe('deny');
    expect(broker.pendingCount()).toBe(0);
  });

  it('denies all pending requests for a session on clearSession', async () => {
    const broker = new PermissionBroker();
    const a = broker.request({ sessionId: 's1', toolUseId: 'a' });
    const b = broker.request({ sessionId: 's1', toolUseId: 'b' });
    const other = broker.request({ sessionId: 's2', toolUseId: 'c' });

    const cleared = broker.clearSession('s1', 'deny');
    expect(cleared).toBe(2);
    await expect(a.verdict).resolves.toBe('deny');
    await expect(b.verdict).resolves.toBe('deny');
    expect(broker.pendingCount('s2')).toBe(1);

    broker.decide({ sessionId: 's2', toolUseId: 'c', verdict: 'allow' });
    await expect(other.verdict).resolves.toBe('allow');
  });

  it('clears only the owning turn when a turnToken is supplied', async () => {
    const broker = new PermissionBroker();
    const tokenN = new AbortController();
    const tokenN1 = new AbortController();
    // Two turns share a session (the cancel/disconnect race); each tags its requests.
    const stale = broker.request({ sessionId: 's1', toolUseId: 'a', turnToken: tokenN });
    const fresh = broker.request({ sessionId: 's1', toolUseId: 'b', turnToken: tokenN1 });

    // The stale turn's teardown must deny only its own request, not the newer one.
    const cleared = broker.clearSession('s1', 'deny', tokenN);
    expect(cleared).toBe(1);
    await expect(stale.verdict).resolves.toBe('deny');
    expect(broker.pendingCount('s1')).toBe(1);

    broker.decide({ sessionId: 's1', toolUseId: 'b', verdict: 'allow' });
    await expect(fresh.verdict).resolves.toBe('allow');
  });

  it('still clears every pending request for a session when no turnToken is given', async () => {
    const broker = new PermissionBroker();
    const a = broker.request({ sessionId: 's1', toolUseId: 'a', turnToken: new AbortController() });
    const b = broker.request({ sessionId: 's1', toolUseId: 'b', turnToken: new AbortController() });

    // The explicit-interrupt path holds the one-turn lock and clears all.
    expect(broker.clearSession('s1', 'deny')).toBe(2);
    await expect(a.verdict).resolves.toBe('deny');
    await expect(b.verdict).resolves.toBe('deny');
  });

  it('supersedes an earlier request for the same key by denying it', async () => {
    const broker = new PermissionBroker();
    const first = broker.request({ sessionId: 's1', toolUseId: 'dup' });
    const second = broker.request({ sessionId: 's1', toolUseId: 'dup' });

    await expect(first.verdict).resolves.toBe('deny');
    expect(broker.pendingCount('s1')).toBe(1);

    broker.decide({ sessionId: 's1', toolUseId: 'dup', verdict: 'allow' });
    await expect(second.verdict).resolves.toBe('allow');
  });

  it('exposes a process-wide singleton that can be reset for tests', () => {
    const first = getPermissionBroker();
    expect(getPermissionBroker()).toBe(first);
    resetPermissionBrokerForTests();
    expect(getPermissionBroker()).not.toBe(first);
  });
});
