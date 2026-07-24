import { mkdtemp } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { describe, expect, it } from "vitest";
import type {
  AgentEnginePort,
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

async function setup(engine: AgentEnginePort) {
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
  const turns = new TurnCoordinator(projects, sessions, engines, residency);
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
