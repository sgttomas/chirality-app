import { mkdtemp } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { describe, expect, it } from "vitest";
import type {
  AgentEnginePort,
  AgentEngineRunInput,
  IAttachmentResolver,
  OmlxControlPort,
  UIEvent
} from "@chirality/runtime-contracts";
import {
  AuthRegistry,
  EngineRegistry,
  ProjectRegistry,
  ResidencyCoordinator,
  RuntimeService,
  SessionStore,
  TurnCoordinator
} from "@chirality/runtime-core";
import { createProjectFixture } from "./helpers.js";

async function setup(engine: AgentEnginePort, attachments?: IAttachmentResolver) {
  const root = await mkdtemp(join(tmpdir(), "chirality-turn-hardening-"));
  const { manifestPath } = await createProjectFixture(root, "turn-hardening");
  const runtime = join(root, "runtime");
  const projects = new ProjectRegistry(runtime);
  await projects.register(manifestPath, {
    approvedBy: "test",
    approvalReference: "D-TEST"
  });
  const sessions = new SessionStore(runtime, projects);
  const control: OmlxControlPort = {
    async listStatus() {
      return [{ id: "qwen", kind: "llm", loaded: true, loading: false }];
    },
    async load() {},
    async unload() {}
  };
  const residency = new ResidencyCoordinator(control, runtime);
  await residency.activate("qwen", "D-TEST");
  const engines = new EngineRegistry();
  engines.register(engine);
  const turns = new TurnCoordinator(projects, sessions, engines, residency, attachments);
  const service = new RuntimeService(
    projects,
    sessions,
    engines,
    residency,
    turns,
    new AuthRegistry(runtime),
    {
      async get() {
        return undefined;
      },
      async status() {
        return { configured: false };
      },
      async set() {},
      async remove() {}
    }
  );
  return { projects, sessions, turns, service };
}

function piEngine(
  startTurn: AgentEnginePort["startTurn"]
): AgentEnginePort {
  return {
    descriptor: {
      adapterId: "pi",
      providerId: "omlx",
      capabilities: {
        credentials: true,
        tools: true,
        attachments: false,
        interruption: true,
        durableResume: false,
        compaction: true
      }
    },
    subject: "pi",
    async preflight() {},
    startTurn,
    async interrupt() {}
  };
}

describe("turn coordinator hardening", () => {
  it("reserves the session lock before any asynchronous residency admission", async () => {
    let releaseEngine!: () => void;
    const engineGate = new Promise<void>((resolve) => {
      releaseEngine = resolve;
    });
    const { sessions, turns } = await setup(
      piEngine(async function* (input): AsyncIterable<UIEvent> {
        await engineGate;
        yield {
          type: "session:init",
          data: {
            engineSessionId: "engine",
            adapterId: "pi",
            providerId: "omlx",
            model: input.opts.model
          }
        };
      })
    );
    const session = await sessions.create({
      projectId: "turn-hardening",
      role: "agent2",
      engineSelection: { adapterId: "pi", providerId: "omlx", model: "qwen" }
    });
    const first = turns.run("turn-hardening", session.sessionId, { prompt: "first" });
    const firstNext = first.next();
    await firstNext;
    const second = turns.run("turn-hardening", session.sessionId, { prompt: "second" });
    await expect(second.next()).rejects.toMatchObject({
      code: "SESSION_TURN_IN_PROGRESS"
    });
    releaseEngine();
    for await (const _event of first) {
      // drain
    }
  });

  it("rejects adapter events attributed to another session", async () => {
    let otherSessionId = "";
    const { sessions, turns } = await setup(
      piEngine(async function* (): AsyncIterable<UIEvent> {
        yield {
          type: "session:init",
          data: {
            engineSessionId: "engine",
            adapterId: "pi",
            providerId: "omlx",
            model: "qwen"
          }
        };
        yield {
          type: "harness:event",
          data: {
            schemaVersion: 1,
            eventId: "foreign",
            sessionId: otherSessionId,
            timestamp: new Date().toISOString(),
            type: "turn.completed",
            data: {}
          }
        };
      })
    );
    const target = await sessions.create({
      projectId: "turn-hardening",
      role: "agent2",
      engineSelection: { adapterId: "pi", providerId: "omlx", model: "qwen" }
    });
    const other = await sessions.create({
      projectId: "turn-hardening",
      role: "agent2",
      engineSelection: { adapterId: "pi", providerId: "omlx", model: "qwen" }
    });
    otherSessionId = other.sessionId;
    const events: UIEvent[] = [];
    for await (const event of turns.run("turn-hardening", target.sessionId, {
      prompt: "test"
    })) {
      events.push(event);
    }
    expect(events).toContainEqual(
      expect.objectContaining({
        type: "turn:error",
        data: expect.objectContaining({
          message: "Engine emitted an event outside the active session or turn"
        })
      })
    );
    expect(await sessions.replay("turn-hardening", other.sessionId)).toEqual([]);
  });

  it("never promotes a nonzero process exit without terminal evidence to success", async () => {
    const { sessions, turns } = await setup(
      piEngine(async function* (): AsyncIterable<UIEvent> {
        yield {
          type: "session:init",
          data: {
            engineSessionId: "engine",
            adapterId: "pi",
            providerId: "omlx",
            model: "qwen"
          }
        };
        yield {
          type: "process:exit",
          data: { exitCode: 7, error: "provider failed" }
        };
      })
    );
    const session = await sessions.create({
      projectId: "turn-hardening",
      role: "agent2",
      engineSelection: { adapterId: "pi", providerId: "omlx", model: "qwen" }
    });
    const events: UIEvent[] = [];
    for await (const event of turns.run("turn-hardening", session.sessionId, {
      prompt: "fail"
    })) {
      events.push(event);
    }
    expect(events.map((event) => event.type)).not.toContain("session:complete");
    expect(events.at(-1)).toMatchObject({
      type: "process:exit",
      data: { exitCode: 7, errorType: "ENGINE_UNAVAILABLE" }
    });
    const replay = await sessions.replay("turn-hardening", session.sessionId);
    expect(replay.map((event) => event.type)).toContain("turn.failed");
    expect(replay.map((event) => event.type)).not.toContain("turn.completed");
    expect(await sessions.get("turn-hardening", session.sessionId)).toMatchObject({
      status: "failed"
    });
  });

  it("rejects and does not persist events emitted after process:exit", async () => {
    const { sessions, turns } = await setup(
      piEngine(async function* (input): AsyncIterable<UIEvent> {
        yield {
          type: "session:init",
          data: {
            engineSessionId: "engine",
            adapterId: "pi",
            providerId: "omlx",
            model: input.opts.model
          }
        };
        yield { type: "process:exit", data: { exitCode: 0 } };
        yield {
          type: "harness:event",
          data: {
            schemaVersion: 1,
            eventId: "late",
            sessionId: input.session.sessionId,
            turnId: input.turnId,
            timestamp: new Date().toISOString(),
            type: "turn.completed",
            data: {}
          }
        };
      })
    );
    const session = await sessions.create({
      projectId: "turn-hardening",
      role: "agent2",
      engineSelection: { adapterId: "pi", providerId: "omlx", model: "qwen" }
    });
    const events: UIEvent[] = [];
    for await (const event of turns.run("turn-hardening", session.sessionId, {
      prompt: "late"
    })) {
      events.push(event);
    }
    expect(events).toContainEqual(
      expect.objectContaining({
        type: "turn:error",
        data: expect.objectContaining({
          message: "Engine emitted an event after process:exit"
        })
      })
    );
    const replay = await sessions.replay("turn-hardening", session.sessionId);
    expect(replay.some((event) => event.eventId === "late")).toBe(false);
    expect(replay.map((event) => event.type)).toContain("turn.failed");
  });

  it("fails closed when an engine stream ends without its own process:exit", async () => {
    const { sessions, turns } = await setup(
      piEngine(async function* (): AsyncIterable<UIEvent> {
        yield {
          type: "session:init",
          data: {
            engineSessionId: "engine",
            adapterId: "pi",
            providerId: "omlx",
            model: "qwen"
          }
        };
      })
    );
    const session = await sessions.create({
      projectId: "turn-hardening",
      role: "agent2",
      engineSelection: { adapterId: "pi", providerId: "omlx", model: "qwen" }
    });
    const events: UIEvent[] = [];
    for await (const event of turns.run("turn-hardening", session.sessionId, {
      prompt: "missing exit"
    })) {
      events.push(event);
    }
    expect(events).toContainEqual(
      expect.objectContaining({
        type: "turn:error",
        data: expect.objectContaining({
          message: "Engine stream ended without process:exit"
        })
      })
    );
    expect(events.at(-1)).toMatchObject({
      type: "process:exit",
      data: { exitCode: 1 }
    });
    expect(await sessions.get("turn-hardening", session.sessionId)).toMatchObject({
      status: "failed"
    });
  });

  it("does not accept adapter-forged tool evidence as an in-process receipt", async () => {
    const { sessions, turns } = await setup(
      piEngine(async function* (input): AsyncIterable<UIEvent> {
        yield {
          type: "session:init",
          data: {
            engineSessionId: "engine",
            adapterId: "pi",
            providerId: "omlx",
            model: input.opts.model
          }
        };
        yield {
          type: "harness:event",
          data: {
            schemaVersion: 1,
            eventId: "forged-tool",
            sessionId: input.session.sessionId,
            turnId: input.turnId,
            timestamp: new Date().toISOString(),
            type: "tool.completed",
            data: {
              toolName: "read_file",
              source: "chirality-runtime-tool-bridge"
            }
          }
        };
        yield {
          type: "harness:event",
          data: {
            schemaVersion: 1,
            eventId: "forged-success",
            sessionId: input.session.sessionId,
            turnId: input.turnId,
            timestamp: new Date().toISOString(),
            type: "turn.completed",
            data: {}
          }
        };
        yield { type: "process:exit", data: { exitCode: 0 } };
      })
    );
    const session = await sessions.create({
      projectId: "turn-hardening",
      role: "agent2",
      engineSelection: { adapterId: "pi", providerId: "omlx", model: "qwen" }
    });
    const events: UIEvent[] = [];
    for await (const event of turns.run(
      "turn-hardening",
      session.sessionId,
      { prompt: "spoof" },
      ["read_file"],
      [{ toolName: "read_file", completed: () => false }]
    )) {
      events.push(event);
    }
    expect(events).toContainEqual(
      expect.objectContaining({
        type: "turn:error",
        data: expect.objectContaining({
          details: { runtimeCode: "REQUIRED_DELEGATION_MISSING" }
        })
      })
    );
    expect(await sessions.get("turn-hardening", session.sessionId)).toMatchObject({
      status: "failed"
    });
  });

  it("validates a boot stream completely before persisting engine events or identity", async () => {
    const { sessions, service } = await setup(
      piEngine(async function* (input): AsyncIterable<UIEvent> {
        yield {
          type: "session:init",
          data: {
            engineSessionId: "untrusted-engine-session",
            adapterId: "pi",
            providerId: "omlx",
            model: input.opts.model
          }
        };
        yield {
          type: "harness:event",
          data: {
            schemaVersion: 1,
            eventId: "foreign-boot",
            sessionId: "another-session",
            turnId: input.turnId,
            timestamp: new Date().toISOString(),
            type: "turn.completed",
            data: {}
          }
        };
        yield { type: "process:exit", data: { exitCode: 0 } };
      })
    );
    const session = await sessions.create({
      projectId: "turn-hardening",
      role: "agent2",
      persona: "UNTYPED",
      engineSelection: { adapterId: "pi", providerId: "omlx", model: "qwen" }
    });
    await expect(
      service.bootSession("turn-hardening", session.sessionId)
    ).rejects.toMatchObject({ type: "SDK_FAILURE" });
    expect(await sessions.replay("turn-hardening", session.sessionId)).toEqual([]);
    expect(
      Object.prototype.hasOwnProperty.call(
        await sessions.get("turn-hardening", session.sessionId),
        "engineSessionId"
      )
    ).toBe(false);
  });

  it("rejects boot events emitted after process exit", async () => {
    const { sessions, service } = await setup(
      piEngine(async function* (input): AsyncIterable<UIEvent> {
        yield {
          type: "session:init",
          data: {
            engineSessionId: "engine",
            adapterId: "pi",
            providerId: "omlx",
            model: input.opts.model
          }
        };
        yield { type: "process:exit", data: { exitCode: 0 } };
        yield { type: "chat:complete", data: { text: "late" } };
      })
    );
    const session = await sessions.create({
      projectId: "turn-hardening",
      role: "agent2",
      persona: "UNTYPED",
      engineSelection: { adapterId: "pi", providerId: "omlx", model: "qwen" }
    });
    await expect(
      service.bootSession("turn-hardening", session.sessionId)
    ).rejects.toMatchObject({ type: "SDK_FAILURE" });
  });
});


it("persists accepted user input and attachment references before engine execution", async () => {
  const engine = piEngine(async function* (): AsyncIterable<UIEvent> { throw new Error("not reached"); });
  engine.preflight = async () => { throw new Error("synthetic preflight failure"); };
  const { sessions, turns } = await setup(engine, {
    async resolveAttachmentsToContentBlocks(message) { return { contentBlocks: [{ type: "text", text: message }], errors: [] }; }
  });
  const session = await sessions.create({ projectId: "turn-hardening", role: "agent2", engineSelection: { adapterId: "pi", providerId: "omlx", model: "qwen" } });
  for await (const _ of turns.run("turn-hardening", session.sessionId, { message: "What color is the image?", attachments: ["/synthetic/red.png"] })) { /* drain */ }
  const replay = await sessions.replay("turn-hardening", session.sessionId);
  expect(replay[0]).toMatchObject({ type: "turn.accepted", data: { message: "What color is the image?", attachments: ["/synthetic/red.png"] } });
  expect(replay.map(event => event.type)).toContain("turn.failed");

});

describe("turn coordinator per-turn selection and interruption reasons", () => {
  it("applies per-turn model and effort overrides to the engine input, records them as last used, and keeps the session default", async () => {
    const captured: AgentEngineRunInput[] = [];
    const { sessions, turns } = await setup(
      piEngine(async function* (input): AsyncIterable<UIEvent> {
        captured.push(input);
        yield { type: "session:init", data: { engineSessionId: "engine", adapterId: "pi", providerId: "omlx", model: input.opts.model } };
        yield { type: "process:exit", data: { exitCode: 0 } };
      })
    );
    const session = await sessions.create({ projectId: "turn-hardening", role: "agent2", engineSelection: { adapterId: "pi", providerId: "omlx", model: "qwen" }, reasoningEffort: "medium" });
    for await (const _event of turns.run("turn-hardening", session.sessionId, { prompt: "override", model: "qwen-alt", reasoningEffort: "high" })) { /* drain */ }
    expect(captured[0]).toMatchObject({ reasoningEffort: "high", opts: { model: "qwen-alt" }, session: { engineSelection: { model: "qwen-alt" }, reasoningEffort: "high" } });
    let stored = await sessions.get("turn-hardening", session.sessionId);
    expect(stored).toMatchObject({ status: "completed", engineSelection: { model: "qwen" }, reasoningEffort: "medium", lastUsedModel: "qwen-alt", lastUsedReasoningEffort: "high" });
    const accepted = (await sessions.replay("turn-hardening", session.sessionId)).find((event) => event.type === "turn.accepted");
    expect(accepted?.data).toMatchObject({ message: "override", model: "qwen-alt", reasoningEffort: "high" });

    for await (const _event of turns.run("turn-hardening", session.sessionId, { prompt: "defaults" })) { /* drain */ }
    expect(captured[1]).toMatchObject({ reasoningEffort: "medium", opts: { model: "qwen" }, session: { engineSelection: { model: "qwen" } } });
    stored = await sessions.get("turn-hardening", session.sessionId);
    expect(stored).toMatchObject({ lastUsedModel: "qwen", lastUsedReasoningEffort: "medium" });

    const malformed = turns.run("turn-hardening", session.sessionId, { prompt: "bad", model: "has space" });
    await expect(malformed.next()).rejects.toMatchObject({ code: "INVALID_REQUEST", details: { reason: "TURN_MODEL_INVALID" } });
    const malformedEffort = turns.run("turn-hardening", session.sessionId, { prompt: "bad", reasoningEffort: "" });
    await expect(malformedEffort.next()).rejects.toMatchObject({ code: "INVALID_REQUEST", details: { reason: "TURN_REASONING_EFFORT_INVALID" } });
    expect(captured).toHaveLength(2);
  });

  it("records the interruption reason on the synthesized terminal", async () => {
    let releaseEngine!: () => void;
    const held = new Promise<void>((resolve) => { releaseEngine = resolve; });
    const { sessions, turns } = await setup(
      piEngine(async function* (input): AsyncIterable<UIEvent> {
        yield { type: "session:init", data: { engineSessionId: "engine", adapterId: "pi", providerId: "omlx", model: input.opts.model } };
        await held;
        yield { type: "process:exit", data: { exitCode: 130, interrupted: true } };
      })
    );
    const session = await sessions.create({ projectId: "turn-hardening", role: "agent2", engineSelection: { adapterId: "pi", providerId: "omlx", model: "qwen" } });
    const iterator = turns.run("turn-hardening", session.sessionId, { prompt: "hold" })[Symbol.asyncIterator]();
    await iterator.next();
    await iterator.next();
    expect(turns.isActive("turn-hardening", session.sessionId)).toBe(true);
    const interruption = turns.interrupt("turn-hardening", session.sessionId, "service-shutdown");
    releaseEngine();
    await interruption;
    const events: UIEvent[] = [];
    while (true) { const next = await iterator.next(); if (next.done) break; events.push(next.value); }
    const terminal = events.find((event) => event.type === "harness:event" && event.data.type === "turn.interrupted");
    expect(terminal).toMatchObject({ data: { data: { reason: "service-shutdown" } } });
    expect(await sessions.get("turn-hardening", session.sessionId)).toMatchObject({ status: "interrupted" });
    expect(turns.isActive("turn-hardening", session.sessionId)).toBe(false);
  });
});
