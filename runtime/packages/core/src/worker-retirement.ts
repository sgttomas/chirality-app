import { readdir } from "node:fs/promises";
import { join } from "node:path";
import { RuntimeError, type RetirementRecord, type WorkerContinuity, type WorkerRetirementCoordinatorPort, type WorkerTerminalRecord } from "@chirality/runtime-contracts";
import { assertContinuity, privateDirectory, privateRead, publishPrivate, recordKey, sameContinuity, validContinuity } from "./fs.js";

const conflict = (message: string) => new RuntimeError("DELEGATION_POLICY_VIOLATION", message, 409);
function identifier(value: string): void {
  if (typeof value !== "string" || !/^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$/.test(value)) throw new RuntimeError("INVALID_REQUEST", "Invalid retirement identifier");
}
function validRoleDigest(value: unknown): boolean { return value === undefined || (typeof value === "string" && /^[a-f0-9]{64}$/.test(value)); }
function checkTerminal(value: WorkerTerminalRecord): void {
  if (!value) throw new RuntimeError("INVALID_REQUEST", "Terminal record is required");
  identifier(value.turnId); identifier(value.workerId); identifier(value.generation);
  if (!["completed", "failed", "interrupted"].includes(value.outcome) || typeof value.recordedAt !== "string" || !Number.isFinite(Date.parse(value.recordedAt))) throw new RuntimeError("INVALID_REQUEST", "Invalid terminal outcome or timestamp");
}
function sameTerminal(a: WorkerTerminalRecord, b: WorkerTerminalRecord): boolean {
  return a.turnId === b.turnId && a.workerId === b.workerId && a.generation === b.generation && a.outcome === b.outcome;
}

/** Exactly one durable terminal record per turn, not exactly-once external effects. */
export class WorkerRetirementCoordinator implements WorkerRetirementCoordinatorPort {
  readonly directory: string;
  constructor(options: { directory: string }) { this.directory = options.directory; }
  private path(turnId: string, suffix: string): string { identifier(turnId); return join(this.directory, `${turnId}.${suffix}.json`); }
  async prepare(record: RetirementRecord): Promise<void> {
    if (!record || record.state !== "prepared" || record.terminal !== undefined) throw new RuntimeError("INVALID_REQUEST", "Only a new prepared retirement may be submitted");
    identifier(record.turnId);
    if (record.threadId !== undefined) identifier(record.threadId);
    if (!validRoleDigest(record.rolePolicyDigest)) throw new RuntimeError("INVALID_REQUEST", "Role policy digest must be a SHA256 hex identity");
    await assertContinuity(record.identity);
    await privateDirectory(this.directory);
    const postimage: RetirementRecord = { turnId: record.turnId, identity: { ...record.identity }, state: "prepared", ...(record.threadId === undefined ? {} : { threadId: record.threadId }), ...(record.rolePolicyDigest === undefined ? {} : { rolePolicyDigest: record.rolePolicyDigest }) };
    await publishPrivate(this.path(record.turnId, "prepared"), postimage, true);
    const existing = await this.prepared(record.turnId);
    if (!existing || !sameContinuity(existing.identity, record.identity) || existing.threadId !== record.threadId || existing.rolePolicyDigest !== record.rolePolicyDigest) throw conflict("Turn identity or recorded thread conflicts with existing retirement");
  }
  private async prepared(turnId: string): Promise<RetirementRecord | undefined> {
    const value = await privateRead<RetirementRecord>(this.path(turnId, "prepared"));
    if (value && (value.turnId !== turnId || value.state !== "prepared" || value.terminal !== undefined || !validRoleDigest(value.rolePolicyDigest) || !validContinuity(value.identity) || (value.threadId !== undefined && (typeof value.threadId !== "string" || !/^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$/.test(value.threadId))))) throw conflict("Invalid persisted retirement basis");
    return value;
  }
  async associateThread(turnId: string, threadId: string): Promise<void> {
    identifier(turnId); identifier(threadId);
    const basis = await this.prepared(turnId);
    if (!basis) throw new RuntimeError("NOT_FOUND", "Retirement was not prepared", 404);
    if (basis.threadId !== undefined && basis.threadId !== threadId) throw conflict("Conflicting prepared thread identity");
    if ((await this.read(turnId))?.terminal) throw conflict("Cannot attach a thread after terminal commitment");
    const record = { basisDigest: recordKey(basis), threadId };
    await publishPrivate(this.path(turnId, "thread"), record, true);
    const actual = await privateRead<typeof record>(this.path(turnId, "thread"));
    if (recordKey(actual) !== recordKey(record)) throw conflict("Conflicting thread association");
    const committed = await privateRead<{ threadDigest?: string }>(this.path(turnId, "terminal"));
    if (committed && committed.threadDigest !== recordKey(record)) throw conflict("Terminal commitment excludes this late thread association");
  }
  async terminalize(terminal: WorkerTerminalRecord): Promise<WorkerTerminalRecord> {
    checkTerminal(terminal);
    await privateDirectory(this.directory);
    const basis = await this.prepared(terminal.turnId);
    if (!basis) throw new RuntimeError("NOT_FOUND", "Retirement was not prepared", 404);
    const existing = (await this.read(terminal.turnId))?.terminal;
    if (existing) {
      if (!sameTerminal(existing, terminal)) throw conflict("Turn already has a different terminal record");
      return existing;
    }
    const thread = await this.thread(terminal.turnId, basis);
    await publishPrivate(this.path(terminal.turnId, "terminal"), { basisDigest: recordKey(basis), terminal, ...(thread ? { threadDigest: recordKey(thread) } : {}) }, true);
    const committed = (await this.read(terminal.turnId))?.terminal;
    if (!committed || !sameTerminal(committed, terminal)) throw conflict("Turn already has a different terminal record");
    // A retry's timestamp does not overwrite the first durable timestamp.
    return committed;
  }
  private async thread(turnId: string, basis: RetirementRecord): Promise<{ basisDigest: string; threadId: string } | undefined> {
    const thread = await privateRead<{ basisDigest: string; threadId: string }>(this.path(turnId, "thread"));
    if (thread) { identifier(thread.threadId); if (thread.basisDigest !== recordKey(basis) || (basis.threadId !== undefined && basis.threadId !== thread.threadId)) throw conflict("Invalid persisted thread association"); }
    return thread;
  }
  async read(turnId: string): Promise<RetirementRecord | undefined> {
    await privateDirectory(this.directory);
    const basis = await this.prepared(turnId);
    if (!basis) return undefined;
    // The terminal's immutable binding decides whether an association is authoritative.
    // Do not even read an unbound late file: it cannot invalidate committed evidence.
    const committed = await privateRead<{ basisDigest: string; terminal: WorkerTerminalRecord; threadDigest?: string }>(this.path(turnId, "terminal"));
    if (committed) {
      checkTerminal(committed.terminal);
      if (committed.basisDigest !== recordKey(basis) || committed.terminal.turnId !== turnId) throw conflict("Terminal record does not bind this retirement");
      const thread = committed.threadDigest === undefined ? undefined : await this.thread(turnId, basis);
      if (committed.threadDigest !== undefined && (!thread || recordKey(thread) !== committed.threadDigest)) throw conflict("Terminal does not bind current thread association");
      return { ...basis, ...(thread ? { threadId: thread.threadId } : {}), state: "committed", terminal: committed.terminal };
    }
    await this.thread(turnId, basis);
    const reconcile = await privateRead<{ basisDigest: string }>(this.path(turnId, "reconciliation"));
    if (reconcile && reconcile.basisDigest !== recordKey(basis)) throw conflict("Reconciliation record does not bind this retirement");
    return { ...basis, state: reconcile ? "reconciliation-required" : "prepared" };
  }
  async reconcile(): Promise<readonly RetirementRecord[]> {
    await privateDirectory(this.directory);
    const result: RetirementRecord[] = [];
    for (const file of (await readdir(this.directory)).filter(file => file.endsWith(".prepared.json")).sort()) {
      const turnId = file.slice(0, -".prepared.json".length);
      const basis = await this.prepared(turnId);
      if (!basis) throw conflict("Retirement basis disappeared during reconciliation");
      const current = await this.read(turnId);
      if (!current?.terminal) await publishPrivate(this.path(turnId, "reconciliation"), { basisDigest: recordKey(basis) }, true);
      // Terminal publication always wins over an earlier reconciliation marker.
      const final = await this.read(turnId);
      if (final) result.push(final);
    }
    return result;
  }
  async restart(turnId: string, identity: WorkerContinuity, expectedRolePolicyDigest?: string): Promise<{ method: "thread/resume" | "thread/start"; threadId?: string }> {
    await assertContinuity(identity);
    if (!validRoleDigest(expectedRolePolicyDigest)) throw new RuntimeError("INVALID_REQUEST", "Expected role policy digest must be a SHA256 hex identity");
    const record = await this.read(turnId);
    if (record && !record.terminal) throw conflict("Active turn must terminalize before restart; reconciliation is required");
    if (record?.terminal && record.threadId && sameContinuity(record.identity, identity) && (expectedRolePolicyDigest === undefined || record.rolePolicyDigest === expectedRolePolicyDigest)) return { method: "thread/resume", threadId: record.threadId };
    return { method: "thread/start" };
  }
}
