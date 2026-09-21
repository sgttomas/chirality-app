import { beforeEach, afterEach, describe, expect, it } from "vitest";
import { mkdtemp, realpath, rm, readdir, readFile, lstat, symlink, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { execFile } from "node:child_process";
import { promisify } from "node:util";
import { WorkerRetirementCoordinator } from "../packages/core/src/worker-retirement.js";
import type { RetirementRecord, WorkerContinuity, WorkerTerminalRecord } from "@chirality/runtime-contracts";

let root: string;
let identity: WorkerContinuity;
let coordinator: WorkerRetirementCoordinator;
let basis: RetirementRecord;
let terminal: WorkerTerminalRecord;
beforeEach(async () => {
  root = await realpath(await mkdtemp(join(tmpdir(), "retirement-test-")));
  identity = { canonicalRoot: root, cwd: root, accountId: "fixture-account", accountEpoch: 1, policyDigest: "fixture-policy" };
  coordinator = new WorkerRetirementCoordinator({ directory: join(root, "retirement") });
  basis = { turnId: "turn-1", identity, threadId: "thread-1", state: "prepared" };
  terminal = { turnId: basis.turnId, workerId: "worker-1", generation: "generation-1", outcome: "interrupted", recordedAt: "2026-09-06T00:00:00Z" };
});
afterEach(async () => { await rm(root, { recursive: true, force: true }); });

describe("durable worker retirement", () => {
  it("survives coordinator loss, fences unresolved restart, and resumes only after terminalization", async () => {
    await coordinator.prepare(basis);
    const recovered = new WorkerRetirementCoordinator({ directory: coordinator.directory });
    expect((await recovered.read(basis.turnId))?.state).toBe("prepared");
    expect((await recovered.reconcile())[0]?.state).toBe("reconciliation-required");
    await expect(recovered.restart(basis.turnId, identity)).rejects.toMatchObject({ code: "DELEGATION_POLICY_VIOLATION" });
    await recovered.terminalize(terminal);
    expect((await recovered.reconcile())[0]?.state).toBe("committed");
    expect(await recovered.restart(basis.turnId, identity)).toEqual({ method: "thread/resume", threadId: "thread-1" });
  });
  it("recovers a prepared turn left by an abruptly terminated OS process", async () => {
    const moduleUrl = new URL("../packages/core/dist/worker-retirement.js", import.meta.url).href;
    const child = `import { WorkerRetirementCoordinator } from ${JSON.stringify(moduleUrl)}; const c = new WorkerRetirementCoordinator({directory:process.argv[1]}); await c.prepare(JSON.parse(process.argv[2])); process.kill(process.pid, "SIGKILL");`;
    await expect(promisify(execFile)(process.execPath, ["--input-type=module", "-e", child, coordinator.directory, JSON.stringify(basis)])).rejects.toMatchObject({ signal: "SIGKILL" });
    expect((await coordinator.reconcile())[0]?.state).toBe("reconciliation-required");
    await expect(coordinator.restart(basis.turnId, identity)).rejects.toMatchObject({ code: "DELEGATION_POLICY_VIOLATION" });
    await coordinator.terminalize(terminal);
    expect((await coordinator.read(basis.turnId))?.state).toBe("committed");
  });
  it("atomically chooses one terminal under competing independent processes", async () => {
    await coordinator.prepare(basis);
    const moduleUrl = new URL("../packages/core/dist/worker-retirement.js", import.meta.url).href;
    const child = `import { WorkerRetirementCoordinator } from ${JSON.stringify(moduleUrl)}; const c = new WorkerRetirementCoordinator({directory:process.argv[1]}); try { console.log(JSON.stringify(await c.terminalize(JSON.parse(process.argv[2])))); } catch(e) { console.log(JSON.stringify({code:e.code})); }`;
    const outcomes = await Promise.all([terminal, { ...terminal, outcome: "failed" }, terminal, terminal].map(value => promisify(execFile)(process.execPath, ["--input-type=module", "-e", child, coordinator.directory, JSON.stringify(value)])));
    const results = outcomes.map(value => JSON.parse(value.stdout));
    const actual = (await coordinator.read(basis.turnId))?.terminal;
    expect(actual).toBeDefined();
    expect(results.every(value => value.code === "DELEGATION_POLICY_VIOLATION" || JSON.stringify(value) === JSON.stringify(actual))).toBe(true);
    expect((await readdir(coordinator.directory)).filter(name => name.endsWith(".terminal.json"))).toHaveLength(1);
  });
  it("makes same-terminal retries idempotent without overwriting the original timestamp", async () => {
    await coordinator.prepare(basis);
    await coordinator.prepare(basis);
    await coordinator.terminalize(terminal);
    expect(await coordinator.terminalize({ ...terminal, recordedAt: "2026-09-07T00:00:00Z" })).toEqual(terminal);
    await expect(coordinator.terminalize({ ...terminal, generation: "generation-2" })).rejects.toMatchObject({ code: "DELEGATION_POLICY_VIOLATION" });
  });
  it("refuses collision of one turn ID with another identity or thread", async () => {
    await coordinator.prepare(basis);
    await expect(coordinator.prepare({ ...basis, identity: { ...identity, accountId: "other" } })).rejects.toMatchObject({ code: "DELEGATION_POLICY_VIOLATION" });
    await expect(coordinator.prepare({ ...basis, threadId: "another-thread" })).rejects.toMatchObject({ code: "DELEGATION_POLICY_VIOLATION" });
  });
  it.each(["accountId", "accountEpoch", "policyDigest"] as const)("starts fresh on %s drift", async field => {
    await coordinator.prepare(basis); await coordinator.terminalize(terminal);
    expect(await coordinator.restart(basis.turnId, { ...identity, [field]: field === "accountEpoch" ? 2 : "changed" })).toEqual({ method: "thread/start" });
  });
  it("starts fresh on a different canonical root or absent recorded thread", async () => {
    await coordinator.prepare(basis); await coordinator.terminalize(terminal);
    const other = await realpath(await mkdtemp(join(root, "other-")));
    expect(await coordinator.restart(basis.turnId, { ...identity, canonicalRoot: other, cwd: other })).toEqual({ method: "thread/start" });
    expect(await coordinator.restart("not-recorded", identity)).toEqual({ method: "thread/start" });
  });
  it("rejects noncanonical cwd before any restart", async () => {
    await expect(coordinator.restart("turn-1", { ...identity, cwd: join(root, "different") })).rejects.toMatchObject({ code: "FORBIDDEN" });
  });
  it("does not mistake an unpublished crash temporary file for a terminal", async () => {
    await coordinator.prepare(basis);
    await writeFile(join(coordinator.directory, "turn-1.terminal.json.crashed.tmp"), JSON.stringify(terminal), { mode: 0o600 });
    expect((await coordinator.reconcile())[0]?.state).toBe("reconciliation-required");
    await coordinator.terminalize(terminal);
    expect((await coordinator.read(basis.turnId))?.terminal).toEqual(terminal);
  });
  it("refuses missing prepare, traversal, malformed records and terminal symlinks", async () => {
    await expect(coordinator.terminalize(terminal)).rejects.toMatchObject({ code: "NOT_FOUND" });
    await expect(coordinator.read("../escape")).rejects.toMatchObject({ code: "INVALID_REQUEST" });
    await coordinator.prepare(basis);
    await symlink(join(coordinator.directory, "turn-1.prepared.json"), join(coordinator.directory, "turn-1.terminal.json"));
    await expect(coordinator.terminalize(terminal)).rejects.toMatchObject({ code: "INTERNAL_FAILURE" });
  });
  it("reconciliation racing a terminal publication always preserves committed outcome", async () => {
    await coordinator.prepare(basis);
    await Promise.all([coordinator.reconcile(), coordinator.terminalize(terminal)]);
    expect((await coordinator.read(basis.turnId))?.state).toBe("committed");
  });
});

it("binds a newly created provider thread into immutable terminal recovery", async () => {
  const { threadId: _thread, ...fresh } = basis;
  await coordinator.prepare(fresh);
  await coordinator.associateThread(basis.turnId, "provider-thread");
  await coordinator.terminalize(terminal);
  const recovered = new WorkerRetirementCoordinator({ directory: coordinator.directory });
  expect(await recovered.restart(basis.turnId, identity)).toEqual({ method: "thread/resume", threadId: "provider-thread" });
  await expect(recovered.associateThread(basis.turnId, "other-thread")).rejects.toMatchObject({ code: "DELEGATION_POLICY_VIOLATION" });
  expect(await recovered.restart(basis.turnId, { ...identity, accountEpoch: 2 })).toEqual({ method: "thread/start" });
});


it("keeps terminal records readable across concurrent thread association in 30 interleavings", async () => {
  const { threadId: _thread, ...fresh } = basis;
  for (let index = 0; index < 30; index++) {
    const turnId = `association-race-${index}`;
    const currentTerminal = { ...terminal, turnId };
    await coordinator.prepare({ ...fresh, turnId });
    await Promise.allSettled([coordinator.associateThread(turnId, `provider-thread-${index}`), coordinator.terminalize(currentTerminal)]);
    const committed = await coordinator.read(turnId);
    expect(committed?.terminal).toEqual(currentTerminal);
    const diskTerminal = JSON.parse(await readFile(join(coordinator.directory, `${turnId}.terminal.json`), "utf8"));
    expect(await coordinator.restart(turnId, identity)).toEqual(diskTerminal.threadDigest === undefined ? { method: "thread/start" } : { method: "thread/resume", threadId: `provider-thread-${index}` });
  }
});

it("ignores an unbound late or malformed association without granting resume", async () => {
  const { threadId: _thread, ...fresh } = basis;
  await coordinator.prepare(fresh); await coordinator.terminalize(terminal);
  await writeFile(join(coordinator.directory, `${basis.turnId}.thread.json`), "{broken late association", { mode: 0o600 });
  expect((await coordinator.read(basis.turnId))?.terminal).toEqual(terminal);
  expect(await coordinator.terminalize({ ...terminal, recordedAt: "2026-09-07T00:00:00Z" })).toEqual(terminal);
  expect(await coordinator.restart(basis.turnId, identity)).toEqual({ method: "thread/start" });
});

it("validates a terminal-bound association strictly", async () => {
  const { threadId: _thread, ...fresh } = basis;
  await coordinator.prepare(fresh); await coordinator.associateThread(basis.turnId, "provider-thread"); await coordinator.terminalize(terminal);
  const path = join(coordinator.directory, `${basis.turnId}.thread.json`);
  const thread = JSON.parse(await readFile(path, "utf8"));
  await writeFile(path, JSON.stringify({ ...thread, threadId: "different-thread" }), { mode: 0o600 });
  await expect(coordinator.read(basis.turnId)).rejects.toMatchObject({ code: "DELEGATION_POLICY_VIOLATION" });
});

it("refuses mismatching prepared thread before any association publication", async () => {
  await coordinator.prepare(basis);
  await expect(coordinator.associateThread(basis.turnId, "different-thread")).rejects.toMatchObject({ code: "DELEGATION_POLICY_VIOLATION" });
  await expect(lstat(join(coordinator.directory, `${basis.turnId}.thread.json`))).rejects.toMatchObject({ code: "ENOENT" });
  await coordinator.terminalize(terminal);
  expect(await coordinator.restart(basis.turnId, identity)).toEqual({ method: "thread/resume", threadId: basis.threadId });
});

it("preserves immutable role policy and starts fresh on a missing or different role digest", async () => {
  const digest = "a".repeat(64);
  await coordinator.prepare({ ...basis, rolePolicyDigest: digest });
  await coordinator.prepare({ ...basis, rolePolicyDigest: digest });
  await expect(coordinator.prepare({ ...basis, rolePolicyDigest: "b".repeat(64) })).rejects.toMatchObject({ code: "DELEGATION_POLICY_VIOLATION" });
  await expect(coordinator.prepare(basis)).rejects.toMatchObject({ code: "DELEGATION_POLICY_VIOLATION" });
  await coordinator.terminalize(terminal);
  expect((await coordinator.read(basis.turnId))?.rolePolicyDigest).toBe(digest);
  expect(await coordinator.restart(basis.turnId, identity, digest)).toEqual({ method: "thread/resume", threadId: basis.threadId });
  expect(await coordinator.restart(basis.turnId, identity, "b".repeat(64))).toEqual({ method: "thread/start" });
  const legacyTurn = "legacy-without-role";
  await coordinator.prepare({ ...basis, turnId: legacyTurn }); await coordinator.terminalize({ ...terminal, turnId: legacyTurn });
  expect(await coordinator.restart(legacyTurn, identity, digest)).toEqual({ method: "thread/start" });
  await expect(coordinator.prepare({ ...basis, turnId: "bad-digest", rolePolicyDigest: "not-a-sha" })).rejects.toMatchObject({ code: "INVALID_REQUEST" });
  await expect(coordinator.restart(basis.turnId, identity, "not-a-sha")).rejects.toMatchObject({ code: "INVALID_REQUEST" });
});
