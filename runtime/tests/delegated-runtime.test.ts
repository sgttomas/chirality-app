import { mkdir, mkdtemp, realpath, rm } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { afterEach, describe, expect, it } from "vitest";
import { RuntimeError, validateHarnessEventV2, type DelegatedTurnProgressEvent, type PendingServerRequest, type ServerRequestAnswer, type WorkerHandle, type WorkerResult } from "@chirality/runtime-contracts";
import { DelegatedRuntime, type DelegatedProjectBinding } from "../packages/core/src/delegated-runtime.js";
import { WorkerRetirementCoordinator } from "../packages/core/src/worker-retirement.js";

const cleanups: (() => Promise<unknown>)[] = [];
afterEach(async () => { for (const cleanup of cleanups.splice(0).reverse()) await cleanup(); });

interface FixtureWorker { handle: WorkerHandle; input: string; release: Promise<WorkerResult>; settle(result: WorkerResult): void; settled: boolean; pending: Map<string, PendingServerRequest & { answer?: ServerRequestAnswer }>; progress: DelegatedTurnProgressEvent[] }
/** In-memory supervisor with an explicit release promise per worker; nothing here depends on wall-clock time. */
function fixtureSupervisor() {
  const workers = new Map<string, FixtureWorker>();
  const retirements = new Map<string, Promise<void>>();
  const log: string[] = [];
  let acquiredCount = 0;
  const entry = (workerId: string, generation: string): FixtureWorker => {
    const worker = workers.get(workerId);
    if (!worker || worker.handle.generation !== generation) throw new RuntimeError("ENGINE_UNAVAILABLE", "unknown or stale worker generation", 503);
    return worker;
  };
  const supervisor = {
    log, workers,
    async acquire(workerId: string, input: string): Promise<WorkerHandle> {
      const handle: WorkerHandle = { workerId, generation: `g-${++acquiredCount}`, pid: 4242, state: "running" };
      let settle!: (result: WorkerResult) => void;
      const release = new Promise<WorkerResult>(resolve => { settle = resolve; });
      const worker: FixtureWorker = { handle, input, release, settled: false, pending: new Map(), progress: [], settle(result) { if (worker.settled) return; worker.settled = true; worker.handle.state = "exited"; settle(result); } };
      workers.set(workerId, worker);
      log.push(`acquire:${workerId}`);
      return { ...handle };
    },
    async inventory(): Promise<readonly WorkerHandle[]> { return [...workers.values()].map(worker => ({ ...worker.handle })); },
    async reconnect(workerId: string, generation: string): Promise<WorkerHandle> { return { ...entry(workerId, generation).handle }; },
    async wait(workerId: string, generation: string): Promise<WorkerResult> { return entry(workerId, generation).release; },
    async interrupt(workerId: string, generation: string): Promise<void> {
      const worker = entry(workerId, generation);
      log.push(`interrupt:${workerId}`);
      await worker.release;
    },
    retire(workerId: string, generation: string): Promise<void> {
      const key = `${workerId}\0${generation}`;
      const memo = retirements.get(key);
      if (memo) return memo;
      let worker: FixtureWorker;
      try { worker = entry(workerId, generation); } catch (error) { return Promise.reject(error); }
      const attempt = (async () => { log.push(`retire:${workerId}`); if (!worker.settled) worker.settle(failed(worker, "retired")); workers.delete(workerId); })();
      retirements.set(key, attempt);
      return attempt;
    },
    async drainTurnProgress(workerId: string, generation: string) { return entry(workerId, generation).progress.splice(0); },
    async pendingRequests(workerId: string, generation: string) { return [...entry(workerId, generation).pending.values()].map(({ answer: _answer, ...request }) => request); },
    async answerRequest(workerId: string, generation: string, requestId: string, answer: ServerRequestAnswer) {
      const worker = entry(workerId, generation);
      const pending = worker.pending.get(requestId);
      if (!pending) throw new RuntimeError("NOT_FOUND", "not pending", 404);
      worker.pending.delete(requestId);
      log.push(`answer:${requestId}:${JSON.stringify(answer)}`);
      return { sent: true as const };
    },
    complete(workerId: string, text = "done") { const worker = workers.get(workerId)!; worker.settle({ worker: { ...worker.handle, state: "exited" }, exitCode: 0, signal: null, threadId: threadOf(worker), stdout: text, stderr: "" }); },
    interrupted(workerId: string) { const worker = workers.get(workerId)!; worker.settle({ worker: { ...worker.handle, state: "exited" }, exitCode: null, signal: "SIGTERM", threadId: threadOf(worker), stdout: "", stderr: "" }); },
    fail(workerId: string, reason: string) { const worker = workers.get(workerId)!; worker.settle(failed(worker, reason)); },
    request(workerId: string, request: PendingServerRequest) { workers.get(workerId)!.pending.set(request.requestId, request); }
  };
  // A resumed thread keeps its identity, as the real supervisor reports it.
  const threadOf = (worker: FixtureWorker): string => { try { return JSON.parse(worker.input).resumeThreadId ?? `thread-${worker.handle.workerId}`; } catch { return `thread-${worker.handle.workerId}`; } };
  const failed = (worker: FixtureWorker, reason: string): WorkerResult => ({ worker: { ...worker.handle, state: "exited" }, exitCode: 1, signal: null, threadId: threadOf(worker), stdout: "", stderr: reason });
  return supervisor;
}
type FixtureSupervisor = ReturnType<typeof fixtureSupervisor>;

const catalog = {
  models: [
    { model: "gpt-default", isDefault: true, defaultReasoningEffort: "high", supportedReasoningEfforts: ["medium", "high"] },
    { model: "gpt-alt", isDefault: false, defaultReasoningEffort: "low", supportedReasoningEfforts: ["low", "medium"] }
  ],
  default: { model: "gpt-default", isDefault: true, defaultReasoningEffort: "high", supportedReasoningEfforts: ["medium", "high"] }
};
async function fixture(options: { withCatalog?: boolean; supervisor?: FixtureSupervisor } = {}) {
  const root = await realpath(await mkdtemp(join(tmpdir(), "dr-")));
  cleanups.push(() => rm(root, { recursive: true, force: true }));
  const project = join(root, "project"); await mkdir(project);
  const identity = { canonicalRoot: project, cwd: project, accountId: "chirality-app", accountEpoch: 0, policyDigest: "stock-codex" };
  const supervisor = options.supervisor ?? fixtureSupervisor();
  const retirement = new WorkerRetirementCoordinator({ directory: join(root, "journal") });
  const binding: DelegatedProjectBinding = { identity, supervisor, retirement, actual: { adapterId: "codex-app-server", providerId: "openai", model: "gpt-default", reasoningEffort: "high" }, ...(options.withCatalog === false ? {} : { catalog }) };
  const delegated = new DelegatedRuntime({ daemonId: "fixture-daemon", projects: new Map([["project", binding]]) });
  // Settle anything a failed assertion left running so close() cannot wait on an explicit release forever.
  cleanups.push(async () => { for (const worker of supervisor.workers.values()) if (!worker.settled) supervisor.interrupted(worker.handle.workerId); await delegated.close(); });
  // Waits until the supervisor holds the worker; the runtime publishes the live turn in the same tick as the acquisition.
  const acquired = async (workerId: string) => { const deadline = Date.now() + 5000; while (!supervisor.workers.has(workerId)) { if (Date.now() > deadline) throw new Error(`worker ${workerId} was not acquired`); await new Promise(resolve => setTimeout(resolve, 2)); } };
  return { root, delegated, supervisor, retirement, identity, binding, acquired };
}

describe("delegated runtime over the shared Codex supervisor", () => {
  it("runs a turn through the private envelope and records the committed terminal", async () => {
    const f = await fixture();
    const progress: DelegatedTurnProgressEvent[] = [];
    const turn = f.delegated.turn("project", { turnId: "turn-1", prompt: "hello", sessionId: "s1", requestedRole: "agent1", permissionMode: "readOnly", developerInstructions: "# Chirality role: agent1" }, [], { onProgress(event) { progress.push(event); } });
    await f.acquired("turn-1");
    const envelope = JSON.parse(f.supervisor.workers.get("turn-1")!.input);
    expect(envelope).toMatchObject({ schema: "chirality-codex-turn/v1", prompt: "hello", cwd: f.identity.canonicalRoot, developerInstructions: "# Chirality role: agent1", policy: { approvalPolicy: "on-request", sandbox: "read-only" }, interactionMode: "chat", requestedRole: "agent1", projectId: "project", sessionId: "s1", clientTurnId: "turn-1" });
    expect(envelope).not.toHaveProperty("resumeThreadId");
    f.supervisor.workers.get("turn-1")!.progress.push({ type: "text", providerThreadId: "thread-turn-1", providerTurnId: "t", text: "partial" });
    f.supervisor.complete("turn-1", "full text");
    const result = await turn;
    expect(result).toMatchObject({ output: "full text", providerThreadId: "thread-turn-1", evidenceClass: "provider-observed", terminal: { outcome: "completed", workerId: "turn-1" } });
    expect(result.event.type).toBe("turn.completed");
    expect(result.event.attribution).toEqual({ adapterId: "codex-app-server", providerId: "openai", model: "gpt-default", reasoningEffort: "high" });
    expect(result.roleEvidence).toMatchObject({ selectedRole: "agent1", enforcementLabel: "role not mechanically enforced", policyDigest: expect.stringMatching(/^[a-f0-9]{64}$/u) });
    expect(validateHarnessEventV2(result.event)).toBe(true);
    expect(progress).toEqual([{ type: "text", providerThreadId: "thread-turn-1", providerTurnId: "t", text: "partial" }]);
    const record = await f.retirement.read("turn-1");
    expect(record).toMatchObject({ state: "committed", threadId: "thread-turn-1", terminal: result.terminal });
    expect(await f.supervisor.inventory()).toEqual([]);
    expect(f.supervisor.log).toEqual(["acquire:turn-1", "retire:turn-1"]);
    // The follow-up turn under the same role policy resumes the durable thread and carries the current developer instructions and role configuration.
    const next = f.delegated.turn("project", { turnId: "turn-2", previousTurnId: "turn-1", prompt: "again", sessionId: "s1", requestedRole: "agent1", permissionMode: "readOnly", developerInstructions: "new", nativeRoleConfig: { "agents.TASK.config_file": "/tmp/role.toml" } });
    await f.acquired("turn-2");
    expect(JSON.parse(f.supervisor.workers.get("turn-2")!.input)).toMatchObject({ resumeThreadId: "thread-turn-1", developerInstructions: "new", nativeRoleConfig: { "agents.TASK.config_file": "/tmp/role.toml" } });
    f.supervisor.fail("turn-2", "scripted failure");
    const failed = await next;
    expect(failed.terminal.outcome).toBe("failed");
    expect(failed.event).toMatchObject({ type: "turn.failed", data: { code: "WORKER_FAILED", message: "scripted failure" } });
    await expect(f.delegated.turn("project", { turnId: "turn-1", prompt: "replay" })).rejects.toMatchObject({ code: "INVALID_REQUEST", status: 409 });
  });

  it("exposes pending Codex requests of the session's live turn and routes answers, including approvals by tool-use id", async () => {
    const f = await fixture();
    expect(await f.delegated.pendingRequests("project", "s1")).toEqual([]);
    await expect(f.delegated.answerRequest("project", "s1", "r1", { kind: "approval", verdict: "allow" })).rejects.toMatchObject({ code: "NOT_FOUND", status: 404 });
    const turn = f.delegated.turn("project", { turnId: "turn-1", prompt: "hello", sessionId: "s1" });
    await f.acquired("turn-1");
    f.supervisor.request("turn-1", { requestId: "7", method: "item/commandExecution/requestApproval", params: { itemId: "cmd-1" }, itemId: "cmd-1", receivedAt: new Date().toISOString() });
    f.supervisor.request("turn-1", { requestId: "8", method: "item/tool/requestUserInput", params: {}, itemId: "ask-1", receivedAt: new Date().toISOString() });
    expect((await f.delegated.pendingRequests("project", "s1")).map(request => request.requestId)).toEqual(["7", "8"]);
    await expect(f.delegated.answerApprovalByToolUseId("project", "s1", "ask-1", "deny")).rejects.toMatchObject({ code: "NOT_FOUND" });
    await expect(f.delegated.answerApprovalByToolUseId("project", "s1", "cmd-1", "deny")).resolves.toEqual({ sent: true });
    await expect(f.delegated.answerRequest("project", "s1", "8", { kind: "userInput", answers: { q: { answers: ["x"] } } })).resolves.toEqual({ sent: true });
    await expect(f.delegated.answerRequest("project", "s1", "8", { kind: "elicitation", action: "maybe" } as never)).rejects.toMatchObject({ code: "INVALID_REQUEST" });
    expect(f.supervisor.log.filter(line => line.startsWith("answer:"))).toEqual(['answer:7:{"kind":"approval","verdict":"deny"}', 'answer:8:{"kind":"userInput","answers":{"q":{"answers":["x"]}}}']);
    f.supervisor.complete("turn-1");
    await turn;
    expect(await f.delegated.pendingRequests("project", "s1")).toEqual([]);
  });

  it("interrupts an active worker once and records the closed interrupted terminal", async () => {
    const f = await fixture();
    const turn = f.delegated.turn("project", { turnId: "interrupt-turn", prompt: "slow" });
    await f.acquired("interrupt-turn");
    const interrupting = f.delegated.interruptTurn("project", { turnId: "interrupt-turn" });
    let interruptSettled = false;
    void interrupting.finally(() => { interruptSettled = true; });
    await new Promise(resolve => setImmediate(resolve));
    expect(interruptSettled).toBe(false);
    expect(f.supervisor.log).toEqual(["acquire:interrupt-turn", "interrupt:interrupt-turn"]);
    f.supervisor.interrupted("interrupt-turn");
    await expect(interrupting).resolves.toMatchObject({ interrupted: true, turnId: "interrupt-turn" });
    const result = await turn;
    expect(result.terminal.outcome).toBe("interrupted");
    expect(result.event.type).toBe("turn.interrupted");
    expect(validateHarnessEventV2(result.event)).toBe(true);
    expect((await f.retirement.read("interrupt-turn"))?.terminal).toEqual(result.terminal);
    await expect(f.delegated.interruptTurn("project", { turnId: "interrupt-turn" })).rejects.toMatchObject({ code: "FORBIDDEN" });
    expect(await f.supervisor.inventory()).toEqual([]);
    expect(f.supervisor.log).toEqual(["acquire:interrupt-turn", "interrupt:interrupt-turn", "retire:interrupt-turn"]);
  });

  it("latches cancellation before acquisition publication and awaits genuine terminal settlement", async () => {
    const f = await fixture();
    let publish!: () => void, began!: () => void;
    const entered = new Promise<void>(resolve => { began = resolve; });
    const gate = new Promise<void>(resolve => { publish = resolve; });
    const acquire = f.supervisor.acquire;
    f.supervisor.acquire = async (id, input) => { began(); await gate; return acquire(id, input); };
    let interrupts = 0;
    const interrupt = f.supervisor.interrupt;
    f.supervisor.interrupt = async (id, generation) => { expect([id, generation]).toEqual(["early", "g-1"]); interrupts++; await interrupt(id, generation); };
    const controller = new AbortController();
    let settled = false;
    const running = f.delegated.turn("project", { turnId: "early", prompt: "bootstrap" }, [], { signal: controller.signal, onProgress() {} }).finally(() => { settled = true; });
    await entered; controller.abort(); expect(interrupts).toBe(0); publish();
    await expect.poll(() => interrupts).toBe(1); expect(settled).toBe(false);
    f.supervisor.interrupted("early");
    await expect(running).resolves.toMatchObject({ terminal: { outcome: "interrupted" } });
  });

  describe("section 8: interrupt and completion race", () => {
    async function assertSingleSettlement(f: Awaited<ReturnType<typeof fixture>>, turnId: string, expected: "interrupted" | "completed") {
      const record = await f.retirement.read(turnId);
      expect(record?.state).toBe("committed");
      expect(record?.terminal?.outcome).toBe(expected);
      expect(f.supervisor.log.filter(line => line === `retire:${turnId}`)).toHaveLength(1);
      expect(f.supervisor.log.filter(line => line === `interrupt:${turnId}`)).toHaveLength(1);
      expect(await f.supervisor.inventory()).toEqual([]);
      // A second retirement of the exact generation joins the settled memo; a stale generation rejects.
      await expect(f.supervisor.retire(turnId, "g-1")).resolves.toBeUndefined();
      await expect(f.supervisor.retire(turnId, "g-stale")).rejects.toMatchObject({ code: "ENGINE_UNAVAILABLE", message: "unknown or stale worker generation" });
      await expect(f.delegated.interruptTurn("project", { turnId })).rejects.toMatchObject({ code: "FORBIDDEN" });
    }
    it("order A: interrupt, then the interrupted terminal, then cleanup settles once", async () => {
      const f = await fixture();
      const turn = f.delegated.turn("project", { turnId: "race-a", prompt: "slow", sessionId: "s1" });
      await f.acquired("race-a");
      const interrupting = f.delegated.interruptTurn("project", { turnId: "race-a" });
      f.supervisor.interrupted("race-a");
      await expect(interrupting).resolves.toMatchObject({ interrupted: true, turnId: "race-a", workerGeneration: "g-1" });
      const result = await turn;
      expect(result.terminal).toMatchObject({ outcome: "interrupted", workerId: "race-a", generation: "g-1" });
      expect(result.event.type).toBe("turn.interrupted");
      await assertSingleSettlement(f, "race-a", "interrupted");
    });
    it("order B: the completed terminal, then a late interrupt, then cleanup settles once without a rejected inner request", async () => {
      const f = await fixture();
      const turn = f.delegated.turn("project", { turnId: "race-b", prompt: "fast", sessionId: "s1" });
      await f.acquired("race-b");
      f.supervisor.complete("race-b", "finished");
      const interrupting = f.delegated.interruptTurn("project", { turnId: "race-b" });
      await expect(interrupting).resolves.toMatchObject({ interrupted: true, turnId: "race-b", workerGeneration: "g-1" });
      const result = await turn;
      expect(result.terminal).toMatchObject({ outcome: "completed", workerId: "race-b", generation: "g-1" });
      expect(result.output).toBe("finished");
      expect(result.event.type).toBe("turn.completed");
      await assertSingleSettlement(f, "race-b", "completed");
    });
  });

  it("closes by interrupting live turns and retiring every worker", async () => {
    const f = await fixture();
    const turn = f.delegated.turn("project", { turnId: "live", prompt: "slow" });
    await f.acquired("live");
    const closing = f.delegated.close();
    await new Promise(resolve => setImmediate(resolve));
    expect(f.supervisor.log).toContain("interrupt:live");
    f.supervisor.interrupted("live");
    await closing;
    await expect(turn).resolves.toMatchObject({ terminal: { outcome: "interrupted" } });
    expect(await f.supervisor.inventory()).toEqual([]);
    await expect(f.delegated.turn("project", { turnId: "after", prompt: "x" })).rejects.toMatchObject({ code: "ENGINE_UNAVAILABLE" });
  });

  describe("per-turn catalog choice", () => {
    const run = async (f: Awaited<ReturnType<typeof fixture>>, turnId: string, choice: { model?: string; reasoningEffort?: string }) => {
      const turn = f.delegated.turn("project", { turnId, prompt: "hello", ...choice });
      await f.acquired(turnId);
      f.supervisor.complete(turnId);
      return turn;
    };
    it("carries the chosen model and effort in the envelope and stamps them on the terminal attribution", async () => {
      const f = await fixture();
      const chosen = await run(f, "chosen", { model: "gpt-alt", reasoningEffort: "medium" });
      const envelopes = () => f.supervisor.log.filter(line => line.startsWith("acquire:"));
      expect(envelopes()).toHaveLength(1);
      expect(chosen.event.attribution).toEqual({ adapterId: "codex-app-server", providerId: "openai", model: "gpt-alt", reasoningEffort: "medium" });
      expect(chosen.roleEvidence.actual).toEqual(chosen.event.attribution);
      const admitted = await run(f, "admitted", {});
      expect(admitted.event.attribution).toEqual({ adapterId: "codex-app-server", providerId: "openai", model: "gpt-default", reasoningEffort: "high" });
      const modelOnly = await run(f, "model-only", { model: "gpt-alt" });
      expect(modelOnly.event.attribution).toEqual({ adapterId: "codex-app-server", providerId: "openai", model: "gpt-alt", reasoningEffort: "low" });
    });
    it("refuses an unknown model or unsupported effort before any envelope is sent", async () => {
      const f = await fixture();
      await expect(f.delegated.turn("project", { turnId: "unknown", prompt: "hello", model: "gpt-unknown", reasoningEffort: "low" })).rejects.toMatchObject({ code: "ENGINE_UNAVAILABLE", status: 503, details: { reason: "MODEL_NOT_IN_CATALOG", model: "gpt-unknown", available: ["gpt-default", "gpt-alt"] } });
      await expect(f.delegated.turn("project", { turnId: "effort", prompt: "hello", model: "gpt-alt", reasoningEffort: "high" })).rejects.toMatchObject({ code: "ENGINE_UNAVAILABLE", status: 503, details: { reason: "REASONING_EFFORT_UNSUPPORTED", model: "gpt-alt", supported: ["low", "medium"] } });
      await expect(f.delegated.turn("project", { turnId: "shape", prompt: "hello", model: "gpt alt" })).rejects.toMatchObject({ code: "INVALID_REQUEST" });
      expect(f.supervisor.log).toEqual([]);
      expect(await f.retirement.read("unknown")).toBeUndefined();
      const uncatalogued = await fixture({ withCatalog: false });
      await expect(uncatalogued.delegated.turn("project", { turnId: "other", prompt: "hello", model: "gpt-alt" })).rejects.toMatchObject({ code: "ENGINE_UNAVAILABLE", status: 503, details: { reason: "MODEL_NOT_IN_CATALOG", model: "gpt-alt", available: ["gpt-default"] } });
      await expect(uncatalogued.delegated.turn("project", { turnId: "other-effort", prompt: "hello", reasoningEffort: "low" })).rejects.toMatchObject({ code: "ENGINE_UNAVAILABLE", status: 503, details: { reason: "REASONING_EFFORT_UNSUPPORTED" } });
      expect(uncatalogued.supervisor.log).toEqual([]);
    });
  });
});
