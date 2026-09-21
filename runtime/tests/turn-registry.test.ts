import { afterEach, describe, expect, it, vi } from "vitest";
import { RuntimeError, type SessionTurnRequest, type UIEvent } from "@chirality/runtime-contracts";
import { TurnRegistry, type TurnFrame, type TurnRegistryService } from "../packages/daemon/src/turn-registry.js";

/** A turn whose events are released one at a time by the test. */
function scriptedTurn(events: readonly UIEvent[]) {
  const gates = events.map(() => {
    let release!: () => void;
    const opened = new Promise<void>((resolve) => { release = resolve; });
    return { opened, release };
  });
  let finished = false;
  let failure: Error | undefined;
  const iterable: AsyncIterable<UIEvent> = {
    async *[Symbol.asyncIterator]() {
      for (const [index, event] of events.entries()) {
        await gates[index]!.opened;
        if (failure !== undefined) throw failure;
        yield event;
      }
      finished = true;
    }
  };
  return {
    iterable,
    release(index: number) { gates[index]!.release(); },
    releaseAll() { for (const gate of gates) gate.release(); },
    fail(index: number, error: Error) { failure = error; gates[index]!.release(); },
    get finished() { return finished; }
  };
}

const delta = (text: string): UIEvent => ({ type: "chat:delta", data: { text } });
const exit: UIEvent = { type: "process:exit", data: { exitCode: 0 } };

function service(turns: Record<string, ReturnType<typeof scriptedTurn>> | ((request: SessionTurnRequest) => AsyncIterable<UIEvent>)) {
  const interruptions: { projectId: string; sessionId: string; reason?: string }[] = [];
  let hold = false;
  let releaseInterrupt: (() => void) | undefined;
  const stub: TurnRegistryService = {
    runSessionTurn(projectId, sessionId, request) {
      if (typeof turns === "function") return turns(request);
      const turn = turns[sessionId];
      if (turn === undefined) throw new RuntimeError("SESSION_NOT_FOUND", `Unknown session: ${sessionId}`, 404);
      return turn.iterable;
    },
    async interruptSession(projectId, sessionId, reason) {
      interruptions.push({ projectId, sessionId, ...(reason === undefined ? {} : { reason }) });
      if (hold) await new Promise<void>((resolve) => { releaseInterrupt = resolve; });
    }
  };
  return {
    stub,
    interruptions,
    holdInterrupts() { hold = true; },
    releaseInterrupt() { hold = false; releaseInterrupt?.(); releaseInterrupt = undefined; }
  };
}

async function collect(frames: AsyncIterable<TurnFrame>): Promise<TurnFrame[]> {
  const out: TurnFrame[] = [];
  for await (const frame of frames) out.push(frame);
  return out;
}

async function settle(): Promise<void> {
  for (let index = 0; index < 5; index += 1) await new Promise<void>((resolve) => setImmediate(resolve));
}

afterEach(() => { vi.useRealTimers(); });

describe("TurnRegistry", () => {
  it("close bounds a stalled interrupt by the grace and settles the session as interrupted", async () => {
    const turn = scriptedTurn([delta("one"), exit]);
    const s = service({ s1: turn });
    s.holdInterrupts();
    const marks: unknown[] = [];
    const registry = new TurnRegistry(s.stub, { sessions: { async markInterruptedOnShutdown(projectId, sessionId, turnId, reason) { marks.push({ projectId, sessionId, turnId, reason }); return true; } } });
    turn.release(0);
    await registry.start("p", "s1", { message: "hello", turnId: "turn-1" });
    const startedAt = Date.now();
    const result = await registry.close({ reason: "service-shutdown", graceMs: 100 });
    expect(Date.now() - startedAt).toBeLessThan(2_000);
    expect(s.interruptions).toEqual([{ projectId: "p", sessionId: "s1", reason: "service-shutdown" }]);
    expect(result.unsettled.map((item) => item.turnId)).toEqual(["turn-1"]);
    expect(marks).toEqual([{ projectId: "p", sessionId: "s1", turnId: "turn-1", reason: "service-shutdown" }]);
    expect(registry.state("p", "s1").active).toBe(false);
    s.releaseInterrupt();
  });

  it("runs the turn in the background, numbers frames from 1 and replays missed frames to a later subscriber", async () => {
    const turn = scriptedTurn([delta("one"), delta("two"), delta("three"), exit]);
    const { stub } = service({ s1: turn });
    const registry = new TurnRegistry(stub);
    turn.release(0);
    const started = await registry.start("p", "s1", { message: "hello", turnId: "turn-1" });
    expect(started.turnId).toBe("turn-1");
    expect(registry.state("p", "s1")).toMatchObject({ active: true, turnId: "turn-1", lastSeq: 1, startedAt: started.startedAt });

    // A first observer sees the buffered frame, then disconnects: the turn is unaffected.
    const first = registry.subscribe("p", "s1", 0);
    const firstIterator = first[Symbol.asyncIterator]();
    expect(await firstIterator.next()).toEqual({ done: false, value: { seq: 1, event: delta("one") } });
    first.close();
    expect(await firstIterator.next()).toEqual({ done: true, value: undefined });

    turn.release(1);
    turn.release(2);
    await settle();
    expect(registry.state("p", "s1")).toMatchObject({ active: true, lastSeq: 3 });

    // Re-attaching after the disconnect delivers exactly the missed frames, then live ones.
    const resumed = collect(registry.subscribe("p", "s1", 1));
    turn.release(3);
    const frames = await resumed;
    expect(frames.map((frame) => frame.seq)).toEqual([2, 3, 4]);
    expect(frames.at(-1)?.event).toEqual(exit);
    expect(registry.state("p", "s1")).toMatchObject({ active: false, turnId: "turn-1", lastSeq: 4 });
    expect(registry.state("p", "s1").endedAt).toEqual(expect.any(String));
    expect(turn.finished).toBe(true);

    // Matching is atomic: a retained prior turn cannot satisfy a new POST's identity.
    expect(() => registry.subscribe("p", "s1", 0, "turn-2")).toThrow(expect.objectContaining({ code: "TURN_NOT_ACTIVE", status: 404 }));
    expect((await collect(registry.subscribe("p", "s1", 0, "turn-1"))).map(frame => frame.seq)).toEqual([1, 2, 3, 4]);
    // Omitted identity retains legacy full replay.
    expect((await collect(registry.subscribe("p", "s1", 0))).map((frame) => frame.seq)).toEqual([1, 2, 3, 4]);
    expect(await collect(registry.subscribe("p", "s1", 4))).toEqual([]);
  });

  it("rejects a second start with 409 while a turn is active and admits one after the terminal frame", async () => {
    const first = scriptedTurn([delta("a"), exit]);
    const second = scriptedTurn([delta("b"), exit]);
    let calls = 0;
    const { stub } = service(() => (calls += 1) === 1 ? first.iterable : second.iterable);
    const registry = new TurnRegistry(stub);
    first.release(0);
    await registry.start("p", "s", { message: "first" });
    await expect(registry.start("p", "s", { message: "again" })).rejects.toMatchObject({ code: "SESSION_TURN_IN_PROGRESS", status: 409 });
    expect(calls).toBe(1);
    first.release(1);
    await settle();
    second.releaseAll();
    const started = await registry.start("p", "s", { message: "second" });
    expect(started.turnId).toEqual(expect.any(String));
    expect((await collect(registry.subscribe("p", "s", 0))).map((frame) => frame.event)).toEqual([delta("b"), exit]);
  });

  it("surfaces a pre-stream failure as the typed error without recording a turn", async () => {
    const retained = scriptedTurn([delta("kept"), exit]);
    retained.releaseAll();
    const { stub } = service({ s: retained });
    const registry = new TurnRegistry(stub);
    await registry.start("p", "s", { message: "ok" });
    await settle();
    await expect(registry.start("p", "unknown", { message: "x" })).rejects.toMatchObject({ code: "SESSION_NOT_FOUND", status: 404 });
    expect(registry.state("p", "unknown")).toEqual({ active: false, lastSeq: 0 });
    expect(() => registry.subscribe("p", "unknown", 0)).toThrow(expect.objectContaining({ code: "TURN_NOT_ACTIVE", status: 404 }));
    // The previous session's retained buffer survives an unrelated failed start.
    expect(registry.state("p", "s")).toMatchObject({ active: false, lastSeq: 2 });
  });

  it("answers 404 TURN_NOT_ACTIVE when nothing is active or retained and after retention expires", async () => {
    vi.useFakeTimers({ toFake: ["setTimeout", "clearTimeout"] });
    const turn = scriptedTurn([delta("only"), exit]);
    turn.releaseAll();
    const { stub } = service({ s: turn });
    const registry = new TurnRegistry(stub);
    expect(() => registry.subscribe("p", "s", 0)).toThrow(expect.objectContaining({ code: "TURN_NOT_ACTIVE", status: 404 }));
    await registry.start("p", "s", { message: "go" });
    await settle();
    expect(registry.state("p", "s")).toMatchObject({ active: false, lastSeq: 2 });
    vi.advanceTimersByTime(10 * 60_000 - 1);
    expect(registry.state("p", "s").lastSeq).toBe(2);
    vi.advanceTimersByTime(1);
    expect(registry.state("p", "s")).toEqual({ active: false, lastSeq: 0 });
    expect(() => registry.subscribe("p", "s", 0)).toThrow(expect.objectContaining({ code: "TURN_NOT_ACTIVE" }));
  });

  it("never interrupts on subscription close and delegates explicit interruption once per in-flight request", async () => {
    const turn = scriptedTurn([delta("start"), delta("after-stop"), exit]);
    const { stub, interruptions, holdInterrupts, releaseInterrupt } = service({ s: turn });
    const registry = new TurnRegistry(stub);
    turn.release(0);
    await registry.start("p", "s", { message: "hold" });
    const subscription = registry.subscribe("p", "s", 0);
    const iterator = subscription[Symbol.asyncIterator]();
    await iterator.next();
    const pending = iterator.next();
    await iterator.return?.();
    expect(await pending).toEqual({ done: true, value: undefined });
    await settle();
    expect(interruptions).toEqual([]);
    expect(registry.state("p", "s").active).toBe(true);

    holdInterrupts();
    const stopA = registry.interrupt("p", "s", "user-stop");
    const stopB = registry.interrupt("p", "s");
    expect(interruptions).toEqual([{ projectId: "p", sessionId: "s", reason: "user-stop" }]);
    releaseInterrupt();
    await Promise.all([stopA, stopB]);
    // The turn keeps producing until the service ends it; frames after the stop request are still buffered.
    turn.release(1);
    turn.release(2);
    await settle();
    expect((await collect(registry.subscribe("p", "s", 0))).map((frame) => frame.seq)).toEqual([1, 2, 3]);
    await registry.interrupt("p", "s");
    expect(interruptions).toHaveLength(2);
  });

  it("ends a stream that fails mid-turn with a terminal frame instead of hanging subscribers", async () => {
    const turn = scriptedTurn([delta("first"), delta("never")]);
    const warnings: string[] = [];
    const { stub } = service({ s: turn });
    const registry = new TurnRegistry(stub, { logger: { warn(event) { warnings.push(event); } } });
    turn.release(0);
    await registry.start("p", "s", { message: "boom" });
    const frames = collect(registry.subscribe("p", "s", 0));
    turn.fail(1, new Error("stream broke secret"));
    const received = await frames;
    expect(received.map((frame) => frame.seq)).toEqual([1, 2]);
    expect(received[1]?.event).toMatchObject({ type: "process:exit", data: { exitCode: 1, fatal: true, errorType: "INTERNAL_FAILURE" } });
    expect(String((received[1]?.event.data as { error?: string }).error)).not.toContain(" ");
    expect(warnings).toEqual(["runtime.turn_registry.turn_stream_failed"]);
    expect(registry.state("p", "s").active).toBe(false);
  });

  it("close() interrupts active turns with the shutdown reason and settles only the ones that do not finish", async () => {
    const quick = scriptedTurn([delta("q"), exit]);
    const stuck = scriptedTurn([delta("s"), exit]);
    const { stub, interruptions } = service({ quick, stuck });
    const settled: { sessionId: string; turnId: string; reason?: string }[] = [];
    const registry = new TurnRegistry(stub, {
      sessions: { async markInterruptedOnShutdown(_projectId, sessionId, turnId, reason) { settled.push({ sessionId, turnId, reason }); return true; } }
    });
    quick.release(0);
    stuck.release(0);
    await registry.start("p", "quick", { message: "a", turnId: "quick-turn" });
    await registry.start("p", "stuck", { message: "b", turnId: "stuck-turn" });
    const closing = registry.close({ graceMs: 50 });
    expect(interruptions.map((entry) => [entry.sessionId, entry.reason])).toEqual([["quick", "service-shutdown"], ["stuck", "service-shutdown"]]);
    quick.release(1);
    const result = await closing;
    expect(result.interrupted.map((turn) => turn.turnId)).toEqual(["quick-turn", "stuck-turn"]);
    expect(result.unsettled.map((turn) => turn.turnId)).toEqual(["stuck-turn"]);
    expect(settled).toEqual([{ sessionId: "stuck", turnId: "stuck-turn", reason: "service-shutdown" }]);
    expect(registry.state("p", "stuck")).toMatchObject({ active: false, lastSeq: 1 });
    expect(registry.state("p", "quick")).toMatchObject({ active: false, lastSeq: 2 });
  });
});


it("does not confuse a matching start still awaiting its first event with the old retained turn", async () => {
  const older = scriptedTurn([delta("old"), exit]);
  older.releaseAll();
  const current = scriptedTurn([delta("current"), exit]);
  let calls = 0;
  const { stub } = service(() => ++calls === 1 ? older.iterable : current.iterable);
  const registry = new TurnRegistry(stub);
  await registry.start("p", "s", { message: "older", turnId: "older" });
  await settle();
  const starting = registry.start("p", "s", { message: "current", turnId: "current" });
  expect(registry.state("p", "s")).toMatchObject({ active: true, turnId: "current" });
  expect(() => registry.subscribe("p", "s", 0, "current")).toThrow(expect.objectContaining({ status: 503, details: expect.objectContaining({ reason: "TURN_STARTING" }) }));
  current.releaseAll();
  await starting;
  expect((await collect(registry.subscribe("p", "s", 0, "current"))).map(frame => frame.event)).toEqual([delta("current"), exit]);
});
