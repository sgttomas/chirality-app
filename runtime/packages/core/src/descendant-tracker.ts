import { execFile } from 'node:child_process';
import { promisify } from 'node:util';

export interface ProcessIdentity { pid: number; ppid: number; pgid: number; uid: number; startIdentity: string }
export interface DescendantTrackerOptions {
  leaderPid: number;
  intervalMs?: number;
  maxDurationMs?: number;
  maxProcesses?: number;
  census?: () => Promise<ProcessIdentity[]>;
}
const execFileAsync = promisify(execFile);
const same = (a: ProcessIdentity, b: ProcessIdentity) => a.pid === b.pid && a.uid === b.uid && a.startIdentity === b.startIdentity;

/** Metadata only: no command, argv, environment or executable name is collected.
 * ps lstart is coarse: matching records are observations, never PID-safe kill tokens. */
export async function censusProcesses(): Promise<ProcessIdentity[]> {
  if (!['darwin', 'linux'].includes(process.platform)) throw new Error('Process census supports macOS/Linux only');
  const { stdout } = await execFileAsync('/bin/ps', [process.platform === 'darwin' ? '-axo' : '-eo', 'pid=,ppid=,pgid=,uid=,lstart='], {
    encoding: 'utf8', maxBuffer: 2 * 1024 * 1024, timeout: 2000,
    env: { PATH: '/usr/bin:/bin', LC_ALL: 'C', LANG: 'C' },
  });
  return stdout.split('\n').filter(line => line.trim()).map(line => {
    const match = /^\s*(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+([A-Za-z]{3}\s+[A-Za-z]{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2}\s+\d{4})\s*$/.exec(line);
    if (!match) throw new Error('Malformed process metadata census');
    const [pid, ppid, pgid, uid] = match.slice(1, 5).map(Number);
    if (![pid, ppid, pgid, uid].every(value => Number.isSafeInteger(value) && value! >= 0)) throw new Error('Invalid process metadata identity');
    return { pid: pid!, ppid: ppid!, pgid: pgid!, uid: uid!, startIdentity: match[5]!.replace(/\s+/g, ' ') };
  });
}

/** Bounded observation and group reconciliation, deliberately not an orphan killer.
 * Group cleanup remains caller-owned. Unobserved fast detach and coarse PID reuse
 * cannot be resolved by polling and must remain visible in closure evidence. */
export class DescendantTracker {
  private readonly records = new Map<number, ProcessIdentity>();
  private readonly census: () => Promise<ProcessIdentity[]>;
  private leader?: ProcessIdentity;
  private timer?: ReturnType<typeof setTimeout>;
  private pending?: Promise<void>;
  private latest: ProcessIdentity[] = [];
  private startedAt = 0;
  private closed = false;
  private failure?: string;
  private scans = 0;
  constructor(private readonly options: DescendantTrackerOptions) {
    if (!Number.isSafeInteger(options.leaderPid) || options.leaderPid <= 0) throw new Error('Invalid leader PID');
    if ((options.intervalMs ?? 100) < 10 || (options.intervalMs ?? 100) > 10000 || (options.maxDurationMs ?? 300000) < 10 || (options.maxDurationMs ?? 300000) > 3600000) throw new Error('Tracker bounds invalid');
    if (![options.intervalMs ?? 100, options.maxDurationMs ?? 300000, options.maxProcesses ?? 16384].every(Number.isSafeInteger) || (options.maxProcesses ?? 16384) < 1 || (options.maxProcesses ?? 16384) > 100000) throw new Error('Tracker numeric bounds invalid');
    this.census = options.census ?? censusProcesses;
  }
  async start(): Promise<void> {
    if (this.startedAt || this.closed) throw new Error('Tracker already started or stopped');
    this.startedAt = Date.now();
    await this.sample();
    if (!this.leader) throw new Error('Leader identity unavailable before observation');
    this.schedule();
  }
  private schedule(): void {
    if (this.closed || this.failure) return;
    if (Date.now() - this.startedAt >= (this.options.maxDurationMs ?? 300000)) { this.failure = 'OBSERVATION_DEADLINE'; return; }
    this.timer = setTimeout(() => { void this.sample().then(() => this.schedule()).catch(() => {}); }, this.options.intervalMs ?? 100);
    this.timer.unref();
  }
  async sample(): Promise<void> {
    if (this.closed) return;
    if (this.pending) return this.pending;
    this.pending = this.scan();
    try { await this.pending; } finally { this.pending = undefined; }
  }
  private async scan(): Promise<void> {
    try {
      const rows = await this.census();
      if (rows.length > (this.options.maxProcesses ?? 16384)) throw new Error('Process census limit exceeded');
      const byPid = new Map(rows.map(row => [row.pid, row]));
      if (byPid.size !== rows.length) throw new Error('Duplicate PID in census');
      this.latest = rows; this.scans++;
      if (!this.leader) {
        const leader = byPid.get(this.options.leaderPid);
        if (!leader) return;
        this.leader = { ...leader }; this.records.set(leader.pid, { ...leader });
      }
      let changed = true;
      while (changed) {
        changed = false;
        for (const row of rows) {
          if (this.records.has(row.pid) || row.uid !== this.leader.uid) continue;
          const parent = this.records.get(row.ppid); const liveParent = byPid.get(row.ppid);
          if (parent && liveParent && same(parent, liveParent)) { this.records.set(row.pid, { ...row }); changed = true; }
        }
      }
    } catch (error) { this.failure = error instanceof Error ? error.message : 'CENSUS_FAILED'; throw error; }
  }
  async reconcile() {
    if (!this.closed) {
      // A reconciliation boundary needs a census started after the call. A
      // pending poll may have captured rows before caller-owned cleanup.
      await this.pending?.catch(() => {});
      await this.sample().catch(() => {});
    }
    const byPid = new Map(this.latest.map(row => [row.pid, row]));
    const ownedGroup: ProcessIdentity[] = [], detached: ProcessIdentity[] = [], gone: ProcessIdentity[] = [], identityChanged: ProcessIdentity[] = [];
    for (const recorded of this.records.values()) {
      const current = byPid.get(recorded.pid);
      if (!current) gone.push(recorded);
      else if (!same(recorded, current)) identityChanged.push(recorded);
      else if (current.pgid === this.leader?.pgid) ownedGroup.push(current);
      else detached.push(current);
    }
    return { leader: this.leader, observed: this.records.size, scans: this.scans, ownedGroup, detached, gone, identityChanged, failure: this.failure,
      signalAuthority: 'NONE' as const,
      limitations: ['UNOBSERVED_DETACH_BETWEEN_POLLS', 'PS_START_IDENTITY_COARSE_NOT_PID_SAFE', ...(this.failure ? ['LATEST_CENSUS_MAY_BE_STALE'] : [])],
    };
  }
  async stop(): Promise<void> { this.closed = true; clearTimeout(this.timer); await this.pending?.catch(() => {}); }
}
