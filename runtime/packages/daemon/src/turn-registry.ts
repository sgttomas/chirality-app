import { randomUUID } from "node:crypto";
import {
  RuntimeError,
  type SessionTurnRequest,
  type SessionTurnState,
  type HarnessEvent,
  type UIEvent
} from "@chirality/runtime-contracts";

/**
 * Runtime-owned turn execution (D-GOV-43 topology A2, disconnection rule).
 *
 * The Runtime service owns every active turn. A browser or renderer connection
 * only observes it through a subscription over the turn's frame buffer; closing
 * a subscription never affects the turn. Explicit Stop is `interrupt`.
 * Reopening a conversation recovers missed frames by sequence.
 */

export const DEFAULT_TURN_RETENTION_MS = 10 * 60_000;
/** Close grace; with the daemon stop and the app-server kill grace it stays inside the App host's kill window. */
const DEFAULT_CLOSE_GRACE_MS = 3_000;

export interface TurnFrame {
  /** 1-based, contiguous per turn; the SSE `id:` field. */
  readonly seq: number;
  readonly event: UIEvent;
}

/** The slice of RuntimeService the registry depends on. */
export interface TurnRegistryService {
  runSessionTurn(projectId: string, sessionId: string, request: SessionTurnRequest): AsyncIterable<UIEvent>;
  interruptSession(projectId: string, sessionId: string, reason?: string): Promise<void>;
}

/** Shutdown settlement for turns that outlive the service's grace; optional. */
export interface TurnShutdownSettlementPort {
  markInterruptedOnShutdown(projectId: string, sessionId: string, turnId: string, reason?: string): Promise<boolean>;
}

export interface TurnRegistryLogger {
  warn(event: string, fields?: Readonly<Record<string, unknown>>): void;
}

export interface TurnRegistryOptions {
  /** How long a finished turn's buffer stays attachable after its terminal frame. */
  retentionMs?: number;
  sessions?: TurnShutdownSettlementPort;
  logger?: TurnRegistryLogger;
}

export interface StartedTurn {
  turnId: string;
  startedAt: string;
}

export interface ActiveTurnSummary {
  projectId: string;
  sessionId: string;
  turnId: string;
  startedAt: string;
}

export interface TurnSubscription extends AsyncIterable<TurnFrame> {
  /** Stops delivery immediately; the turn is unaffected. Idempotent. */
  close(): void;
}

export interface TurnRegistryCloseResult {
  /** Turns that were active when close began. */
  interrupted: readonly ActiveTurnSummary[];
  /** Turns that had not reached their terminal frame within the grace period. */
  unsettled: readonly ActiveTurnSummary[];
}

interface TurnRecord {
  readonly key: string;
  readonly projectId: string;
  readonly sessionId: string;
  readonly turnId: string;
  readonly startedAt: string;
  endedAt?: string;
  readonly frames: TurnFrame[];
  terminal: boolean;
  readonly waiters: Set<() => void>;
  interruption?: Promise<void>;
  retention?: ReturnType<typeof setTimeout>;
}

function safeMessage(error: unknown): string {
  const text = error instanceof Error ? error.message : String(error ?? "");
  return text.replace(/[\x00-\x1f\x7f]/g, " ").slice(0, 200);
}

class Subscription implements TurnSubscription {
  private cursor: number;
  private closed = false;
  private wake?: () => void;
  private readonly notify = (): void => {
    const wake = this.wake;
    this.wake = undefined;
    wake?.();
  };

  constructor(private readonly record: TurnRecord, afterSeq: number) {
    this.cursor = afterSeq;
    record.waiters.add(this.notify);
  }

  close(): void {
    if (this.closed) return;
    this.closed = true;
    this.record.waiters.delete(this.notify);
    this.notify();
  }

  [Symbol.asyncIterator](): AsyncIterator<TurnFrame> {
    return {
      next: () => this.next(),
      return: async () => {
        this.close();
        return { done: true, value: undefined };
      }
    };
  }

  private async next(): Promise<IteratorResult<TurnFrame>> {
    while (true) {
      if (this.closed) return { done: true, value: undefined };
      // frames[i].seq === i + 1, so the first frame with seq > cursor sits at index cursor.
      const frame = this.record.frames[this.cursor];
      if (frame !== undefined) {
        this.cursor = frame.seq;
        return { done: false, value: frame };
      }
      if (this.record.terminal) {
        this.close();
        return { done: true, value: undefined };
      }
      // The executor runs synchronously, so a frame appended after the check above cannot be missed.
      await new Promise<void>((resolve) => {
        this.wake = resolve;
      });
    }
  }
}

export class TurnRegistry {
  private readonly turns = new Map<string, TurnRecord>();
  /** Turns whose first event is still being awaited; they count as active for admission and state. */
  private readonly starting = new Map<string, StartedTurn>();
  private readonly retentionMs: number;

  constructor(private readonly service: TurnRegistryService, private readonly options: TurnRegistryOptions = {}) {
    this.retentionMs = options.retentionMs ?? DEFAULT_TURN_RETENTION_MS;
  }

  /**
   * Starts the turn in the background. Resolves once the service produced its
   * first event, so pre-stream failures (unknown session, empty message, a turn
   * already in progress) reject here with their typed error and no turn is recorded.
   */
  async start(projectId: string, sessionId: string, request: SessionTurnRequest): Promise<StartedTurn> {
    const key = this.key(projectId, sessionId);
    const existing = this.turns.get(key);
    if (this.starting.has(key) || (existing !== undefined && !existing.terminal)) {
      throw new RuntimeError("SESSION_TURN_IN_PROGRESS", "Session already has an active turn", 409, {
        sessionId,
        turnId: this.starting.get(key)?.turnId ?? existing?.turnId
      });
    }
    const turnId = typeof request.turnId === "string" && request.turnId.trim() !== "" ? request.turnId : randomUUID();
    const startedAt = new Date().toISOString();
    const started: StartedTurn = { turnId, startedAt };
    this.starting.set(key, started);
    let iterator: AsyncIterator<UIEvent>;
    let first: IteratorResult<UIEvent>;
    try {
      iterator = this.service.runSessionTurn(projectId, sessionId, { ...request, turnId })[Symbol.asyncIterator]();
      first = await iterator.next();
    } catch (error) {
      if (this.starting.get(key) === started) this.starting.delete(key);
      throw error;
    }
    if (this.starting.get(key) !== started) {
      // close() ran while the first event was pending; do not register a turn the registry no longer tracks.
      void this.discard(iterator);
      throw new RuntimeError("ENGINE_UNAVAILABLE", "Turn registry closed while the turn was starting", 503, { sessionId });
    }
    this.starting.delete(key);
    if (existing !== undefined) this.forget(existing);
    const record: TurnRecord = { key, projectId, sessionId, turnId, startedAt, frames: [], terminal: false, waiters: new Set() };
    this.turns.set(key, record);
    if (first.done) {
      this.finish(record);
      return started;
    }
    this.append(record, first.value);
    void this.drain(record, iterator);
    return started;
  }

  /** Buffered frames with `seq > afterSeq`, then live frames until the terminal frame. */
  subscribe(projectId: string, sessionId: string, afterSeq = 0, turnId?: string): TurnSubscription {
    if (!Number.isSafeInteger(afterSeq) || afterSeq < 0) {
      throw new RuntimeError("INVALID_REQUEST", "after must be a non-negative integer", 400, { reason: "TURN_AFTER_INVALID" });
    }
    const key = this.key(projectId, sessionId);
    if (turnId !== undefined && this.starting.get(key)?.turnId === turnId) {
      throw new RuntimeError("ENGINE_UNAVAILABLE", "The matching turn is still starting", 503, { sessionId, turnId, reason: "TURN_STARTING" });
    }
    const record = this.turns.get(key);
    if (record === undefined || (turnId !== undefined && record.turnId !== turnId)) {
      throw new RuntimeError("TURN_NOT_ACTIVE", "No matching active or retained turn for this session", 404, { sessionId, ...(turnId === undefined ? {} : { turnId }) });
    }
    return new Subscription(record, afterSeq);
  }

  state(projectId: string, sessionId: string): SessionTurnState {
    const key = this.key(projectId, sessionId);
    const starting = this.starting.get(key);
    if (starting !== undefined) return { active: true, turnId: starting.turnId, lastSeq: 0, startedAt: starting.startedAt };
    const record = this.turns.get(key);
    if (record === undefined) return { active: false, lastSeq: 0 };
    return {
      active: !record.terminal,
      turnId: record.turnId,
      lastSeq: record.frames.length,
      startedAt: record.startedAt,
      ...(record.endedAt === undefined ? {} : { endedAt: record.endedAt })
    };
  }

  /** Publishes already-persisted side input evidence without creating a turn. */
  publishEvidence(projectId: string, sessionId: string, event: HarnessEvent): void {
    const current = this.turns.get(this.key(projectId, sessionId));
    if (current && current.turnId === event.turnId && event.sessionId === sessionId) {
      this.append(current, { type: "harness:event", data: event });
    }
  }

  /** Explicit Stop. Concurrent calls for the same active turn join one in-flight interruption. */
  interrupt(projectId: string, sessionId: string, reason?: string): Promise<void> {
    const record = this.turns.get(this.key(projectId, sessionId));
    if (record === undefined || record.terminal) return this.service.interruptSession(projectId, sessionId, reason);
    if (record.interruption === undefined) {
      const pending = this.service.interruptSession(projectId, sessionId, reason);
      record.interruption = pending;
      const clear = (): void => {
        if (record.interruption === pending) record.interruption = undefined;
      };
      void pending.then(clear, clear);
    }
    return record.interruption;
  }

  activeTurns(): readonly ActiveTurnSummary[] {
    const active: ActiveTurnSummary[] = [];
    for (const [key, started] of this.starting) {
      const [projectId, sessionId] = this.split(key);
      active.push({ projectId, sessionId, turnId: started.turnId, startedAt: started.startedAt });
    }
    for (const record of this.turns.values()) {
      if (record.terminal) continue;
      active.push({ projectId: record.projectId, sessionId: record.sessionId, turnId: record.turnId, startedAt: record.startedAt });
    }
    return active;
  }

  /**
   * Service shutdown: interrupts every active turn with the reason, waits up to
   * the grace for their terminal frames, and settles the session record of any
   * turn that did not finish so a relaunch never shows it as still running.
   */
  async close(options: { reason?: string; graceMs?: number } = {}): Promise<TurnRegistryCloseResult> {
    const reason = options.reason ?? "service-shutdown";
    const graceMs = options.graceMs ?? DEFAULT_CLOSE_GRACE_MS;
    const interrupted = this.activeTurns();
    const deadline = Date.now() + graceMs;
    // The interrupt fan-out is bounded by the same grace: a supplier slow to
    // honour turn/interrupt must not push the settlement below past the host's
    // kill window, or a relaunch would find the session still running.
    let graceTimer: ReturnType<typeof setTimeout> | undefined;
    await Promise.race([
      Promise.allSettled(interrupted.map((turn) => this.interrupt(turn.projectId, turn.sessionId, reason))),
      new Promise<void>((resolve) => { graceTimer = setTimeout(resolve, graceMs); })
    ]);
    clearTimeout(graceTimer);
    const unsettled: ActiveTurnSummary[] = [];
    for (const turn of interrupted) {
      const settled = await this.waitForTerminal(turn, Math.max(0, deadline - Date.now()));
      if (!settled) unsettled.push(turn);
    }
    for (const turn of unsettled) {
      const record = this.turns.get(this.key(turn.projectId, turn.sessionId));
      if (record !== undefined && !record.terminal) this.finish(record);
      this.starting.delete(this.key(turn.projectId, turn.sessionId));
      if (this.options.sessions !== undefined) {
        await this.options.sessions.markInterruptedOnShutdown(turn.projectId, turn.sessionId, turn.turnId, reason).catch((error) => {
          this.options.logger?.warn("runtime.turn_registry.shutdown_settlement_failed", { projectId: turn.projectId, sessionId: turn.sessionId, turnId: turn.turnId, message: safeMessage(error) });
        });
      }
    }
    return { interrupted, unsettled };
  }

  private waitForTerminal(turn: ActiveTurnSummary, timeoutMs: number): Promise<boolean> {
    const key = this.key(turn.projectId, turn.sessionId);
    const record = this.turns.get(key);
    if (record === undefined) return Promise.resolve(!this.starting.has(key));
    if (record.terminal) return Promise.resolve(true);
    return new Promise((resolve) => {
      const timer = setTimeout(() => {
        record.waiters.delete(check);
        resolve(record.terminal);
      }, timeoutMs);
      const check = (): void => {
        if (!record.terminal) return;
        clearTimeout(timer);
        record.waiters.delete(check);
        resolve(true);
      };
      record.waiters.add(check);
    });
  }

  private async drain(record: TurnRecord, iterator: AsyncIterator<UIEvent>): Promise<void> {
    try {
      while (true) {
        const next = await iterator.next();
        if (next.done) break;
        if (record.terminal) continue; // settled by close(); keep draining without publishing
        this.append(record, next.value);
      }
    } catch (error) {
      // The coordinator converts its own failures into events; anything reaching here is a
      // defect in the stream itself. Subscribers still receive a terminal frame.
      this.options.logger?.warn("runtime.turn_registry.turn_stream_failed", { projectId: record.projectId, sessionId: record.sessionId, turnId: record.turnId, message: safeMessage(error) });
      if (!record.terminal) {
        this.append(record, {
          type: "process:exit",
          data: { exitCode: 1, error: safeMessage(error), errorType: "INTERNAL_FAILURE", status: 500, severity: "error", fatal: true }
        });
      }
    } finally {
      this.finish(record);
    }
  }

  private async discard(iterator: AsyncIterator<UIEvent>): Promise<void> {
    try {
      while (!(await iterator.next()).done) { /* drain to release the service's turn */ }
    } catch { /* already reported by the service */ }
  }

  private append(record: TurnRecord, event: UIEvent): void {
    record.frames.push({ seq: record.frames.length + 1, event });
    this.notify(record);
  }

  private finish(record: TurnRecord): void {
    if (record.terminal) return;
    record.terminal = true;
    record.endedAt = new Date().toISOString();
    this.notify(record);
    record.retention = setTimeout(() => {
      if (this.turns.get(record.key) === record) this.turns.delete(record.key);
    }, this.retentionMs);
    record.retention.unref?.();
  }

  private forget(record: TurnRecord): void {
    if (record.retention !== undefined) clearTimeout(record.retention);
    if (this.turns.get(record.key) === record) this.turns.delete(record.key);
  }

  private notify(record: TurnRecord): void {
    for (const waiter of [...record.waiters]) waiter();
  }

  private key(projectId: string, sessionId: string): string {
    return `${projectId}\0${sessionId}`;
  }

  private split(key: string): [string, string] {
    const index = key.indexOf("\0");
    return [key.slice(0, index), key.slice(index + 1)];
  }
}
