import { expect, it } from 'vitest';
import { spawn } from 'node:child_process';
import { once } from 'node:events';
import { DescendantTracker, censusProcesses, type ProcessIdentity } from '../packages/core/src/descendant-tracker.js';

const row = (pid: number, ppid: number, pgid = 10, startIdentity = 'start-1'): ProcessIdentity => ({ pid, ppid, pgid, uid: 42, startIdentity });
it('retains observed detached descendants and rejects reused identities without signaling', async () => {
  let rows = [row(10, 1), row(11, 10), row(12, 11, 12), row(30, 1)];
  const tracker = new DescendantTracker({ leaderPid: 10, census: async () => rows, intervalMs: 10000 });
  await tracker.start();
  rows = [row(11, 1, 10, 'reused'), row(12, 1, 12), row(30, 1)];
  const result = await tracker.reconcile(); await tracker.stop();
  expect(result.observed).toBe(3); expect(result.detached.map(p => p.pid)).toEqual([12]);
  expect(result.identityChanged.map(p => p.pid)).toEqual([11]); expect(result.gone.map(p => p.pid)).toEqual([10]);
  expect(result.signalAuthority).toBe('NONE'); expect(result.limitations).toContain('PS_START_IDENTITY_COARSE_NOT_PID_SAFE');
});
it('bounds census and closes its timer without treating stale observation as closure proof', async () => {
  let calls = 0;
  const tracker = new DescendantTracker({ leaderPid: 10, maxProcesses: 1, census: async () => { calls++; return [row(10, 1), row(11, 10)]; } });
  await expect(tracker.start()).rejects.toThrow('limit'); await tracker.stop();
  await tracker.sample(); expect(calls).toBe(1);
  expect((await tracker.reconcile()).limitations).toContain('LATEST_CENSUS_MAY_BE_STALE');
});
it.skipIf(!['darwin', 'linux'].includes(process.platform))('observes an actual detached descendant after its controlled leader exits', async () => {
  // Child has a fixed natural lifetime; cleanup never sends a signal to a PID learned from ps.
  const program = `const {spawn}=require('node:child_process');
  const child=spawn(process.execPath,['-e','process.stdout.write("ready");setTimeout(()=>process.exit(0),2200)'],{detached:true,stdio:['ignore','pipe','ignore']});
  child.stdout.once('data',()=>process.stdout.write(String(child.pid)+'\\n'));
  process.stdin.once('data',()=>process.exit(0));`;
  const leader = spawn(process.execPath, ['-e', program], { detached: true, stdio: ['pipe', 'pipe', 'pipe'] });
  const tracker = new DescendantTracker({ leaderPid: leader.pid!, intervalMs: 50, maxDurationMs: 5000 });
  const closed = once(leader, 'close');
  try {
    const [chunk] = await once(leader.stdout, 'data'); const descendant = Number(String(chunk).trim());
    expect(Number.isSafeInteger(descendant)).toBe(true);
    await tracker.start();
    expect((await tracker.reconcile()).detached.some(row => row.pid === descendant)).toBe(true);
    leader.stdin.write('exit'); await closed;
    const result = await tracker.reconcile();
    expect(result.detached.some(row => row.pid === descendant)).toBe(true);
    expect(result.gone.some(row => row.pid === leader.pid)).toBe(true);
    expect((await censusProcesses()).every(row => !('args' in row))).toBe(true);
  } finally { await tracker.stop(); if (leader.exitCode === null) leader.kill(); await new Promise(resolve => setTimeout(resolve, 2300)); }
}, 10000);


it.each(['gone', 'live', 'detached', 'identity-changed', 'failure'] as const)('reconciliation drains a pre-cleanup census then starts fresh (%s)', async outcome => {
  let rows = [row(10, 1)];
  let hold = false, fail = false, release!: () => void, calls = 0;
  const tracker = new DescendantTracker({ leaderPid: 10, intervalMs: 10000, census: async () => {
    calls++;
    const captured = rows, capturedFailure = fail;
    if (hold) await new Promise<void>(resolve => { release = resolve; });
    if (capturedFailure) throw new Error('fresh census failure');
    return captured;
  } });
  try {
    await tracker.start();
    hold = true;
    const pending = tracker.sample(); // Captures the leader before cleanup.
    rows = outcome === 'gone' || outcome === 'failure' ? []
      : outcome === 'detached' ? [row(10, 1, 20)]
      : outcome === 'identity-changed' ? [row(10, 1, 10, 'new-identity')]
      : [row(10, 1)];
    const reconciled = tracker.reconcile(); // Invoked after controlled cleanup.
    hold = false;
    fail = outcome === 'failure';
    release();
    await pending;
    const state = await reconciled;
    expect(calls).toBe(3); // Initial, old pending poll, newly initiated census.
    expect(state.ownedGroup.length).toBe(outcome === 'live' || outcome === 'failure' ? 1 : 0);
    expect(state.detached.length).toBe(outcome === 'detached' ? 1 : 0);
    expect(state.identityChanged.length).toBe(outcome === 'identity-changed' ? 1 : 0);
    if (outcome === 'failure') {
      expect(state.failure).toBe('fresh census failure');
      fail = false;
      const later = await tracker.reconcile();
      expect(later.ownedGroup).toEqual([]);
      expect(later.failure).toBe('fresh census failure'); // Observation gaps stay visible.
    } else expect(state.failure).toBeUndefined();
  } finally { await tracker.stop(); }
});
