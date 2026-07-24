import { mkdtemp, readFile, readdir, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { describe, expect, it } from "vitest";
import type {
  AgentEnginePort,
  OmlxControlPort,
  RuntimeToolDefinition,
  UIEvent
} from "@chirality/runtime-contracts";
import {
  AuthRegistry,
  EngineRegistry,
  GovernedAgent1RunCoordinator,
  ProjectRegistry,
  ResidencyCoordinator,
  RuntimeService,
  SessionStore,
  TurnCoordinator
} from "@chirality/runtime-core";
import { createProjectFixture } from "./helpers.js";

async function setup(
  managerMode: "success" | "missing" | "blocking" | "child-blocking" | "child-no-tool"
) {
  const root = await mkdtemp(join(tmpdir(), "chirality-agent1-"));
  const { manifestPath } = await createProjectFixture(root, "agent-pilot");
  await writeFile(join(root, "known.txt"), "known-value\n", "utf8");
  const runtime = join(root, "user-data", "runtime");
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
  const bindings = new Map<string, readonly RuntimeToolDefinition[]>();
  const engines = new EngineRegistry();
  let releaseChild!: () => void;
  let markChildStarted!: () => void;
  const childReleased = new Promise<void>((resolve) => {
    releaseChild = resolve;
  });
  const childStarted = new Promise<void>((resolve) => {
    markChildStarted = resolve;
  });
  let childInterrupts = 0;
  const engine: AgentEnginePort = {
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
    async *startTurn(input) {
      const tool = bindings.get(input.session.sessionId)?.[0];
      const shouldCallTool = managerMode !== "child-no-tool";
      yield {
        type: "session:init",
        data: {
          engineSessionId: `engine-${input.session.sessionId}`,
          adapterId: "pi",
          providerId: "omlx",
          model: input.opts.model
        }
      };
      const result =
        tool === undefined || !shouldCallTool
          ? "missing-tool"
          : await tool.execute({}, new AbortController().signal);
      if (managerMode === "child-blocking") {
        markChildStarted();
        await childReleased;
      }
      if (shouldCallTool && tool !== undefined) {
        yield { type: "tool:result", data: { name: "read_file", ok: true, output: "known-value" } };
        yield {
          type: "harness:event",
          data: {
            schemaVersion: 1,
            eventId: `tool-completed-${input.turnId}`,
            sessionId: input.session.sessionId,
            turnId: input.turnId,
            timestamp: new Date().toISOString(),
            type: "tool.completed",
            data: { toolName: "read_file" }
          }
        };
      }
      yield { type: "chat:complete", data: { text: JSON.stringify(result) } };
      yield { type: "process:exit", data: { exitCode: 0 } };
    },
    async interrupt() {
      childInterrupts += 1;
      releaseChild();
    }
  };
  engines.register(engine);
  const turns = new TurnCoordinator(projects, sessions, engines, residency);
  const manager = {
    async *execute(
      _session: unknown,
      _request: unknown,
      hooks: {
        delegate(input: { sealedBrief: string }): Promise<{ childSessionId: string }>;
        review(input: {
          childSessionId: string;
          decision: "accepted";
          rationale: string;
        }): Promise<void>;
      },
      signal: AbortSignal
    ): AsyncIterable<UIEvent> {
      if (managerMode === "blocking") {
        await new Promise<void>((resolve) => {
          if (signal.aborted) resolve();
          else signal.addEventListener("abort", () => resolve(), { once: true });
        });
        return;
      }
      if (
        managerMode === "success" ||
        managerMode === "child-blocking" ||
        managerMode === "child-no-tool"
      ) {
        const child = await hooks.delegate({ sealedBrief: "Read the governed file." });
        await hooks.review({
          childSessionId: child.childSessionId,
          decision: "accepted",
          rationale: "The return contains the known value."
        });
      }
      yield { type: "chat:complete", data: { text: "manager-finished" } };
    }
  };
  const coordinator = new GovernedAgent1RunCoordinator({
    projects,
    sessions,
    turns,
    residency,
    manager,
    tools: {
      async bind(sessionId, tools) {
        bindings.set(sessionId, tools);
        return async () => {
          bindings.delete(sessionId);
        };
      }
    },
    async resolveManagerSelection() {
      return { adapterId: "stub", providerId: "stub", model: "manager" };
    }
  });
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
    },
    undefined,
    coordinator
  );
  return {
    coordinator,
    service,
    root,
    sessions,
    childStarted,
    childInterrupts: () => childInterrupts
  };
}

describe("governed Agent 1 local-child pilot", () => {
  it("rejects empty approval attribution before creating a run", async () => {
    const { coordinator } = await setup("missing");
    const stream = coordinator.run("agent-pilot", {
      brief: "Must remain attributed.",
      agentId: "WORKING_ITEMS",
      approvalReference: " "
    });
    await expect(stream.next()).rejects.toMatchObject({
      code: "INVALID_REQUEST"
    });
  });

  it("rejects the Agent 0 HELP_HUMAN seat as a direct Agent 1 target", async () => {
    const { coordinator } = await setup("missing");
    const stream = coordinator.run("agent-pilot", {
      brief: "Do not misclassify Agent 0.",
      agentId: "HELP_HUMAN",
      approvalReference: "D-TEST"
    });
    await expect(stream.next()).rejects.toMatchObject({
      code: "DELEGATION_POLICY_VIOLATION"
    });
  });

  it("runs exactly one read-only Agent 2, records parentage/model epoch, and requires review", async () => {
    const { coordinator, root, sessions } = await setup("success");
    const events: UIEvent[] = [];
    for await (const event of coordinator.run("agent-pilot", {
      brief: "Delegate the file check and review it.",
      localModel: "qwen",
      agentId: "WORKING_ITEMS",
      approvalReference: "D-TEST",
      readOnlyTool: { name: "read_file", relativePath: "known.txt" }
    })) {
      events.push(event);
    }
    expect(events.at(-1)).toMatchObject({ type: "process:exit", data: { exitCode: 0 } });
    const runRoots = await readdir(
      join(root, "execution", "_Coordination", "AgentRuns", "runtime")
    );
    const record = JSON.parse(
      await readFile(
        join(
          root,
          "execution",
          "_Coordination",
          "AgentRuns",
          "runtime",
          runRoots[0]!,
          "run.json"
        ),
        "utf8"
      )
    );
    expect(record).toMatchObject({
      status: "completed",
      child: {
        role: "agent2",
        selection: { adapterId: "pi", providerId: "omlx", model: "qwen" },
        sealedBrief: "Read the governed file.",
        returnHash: expect.any(String),
        evidenceReference: {
          projectId: "agent-pilot",
          source: "canonical-session-events"
        },
        acceptance: { decision: "accepted" },
        permissions: ["read"],
        tool: "read_file"
      },
      review: { decision: "accepted" }
    });
    const childSession = (await sessions.list("agent-pilot")).find(
      (session) => session.role === "agent2"
    );
    expect(childSession).toMatchObject({
      persona: "TASK",
      mode: "readOnly",
      approvalRef: "D-TEST",
      allowedWriteTargets: []
    });
    const childEvents = await sessions.replay("agent-pilot", childSession!.sessionId);
    expect(childEvents.map((event) => event.type)).toEqual(
      expect.arrayContaining([
        "tool.permission",
        "tool.started",
        "tool.completed",
        "turn.completed"
      ])
    );
    const toolCompleted = childEvents.find((event) => event.type === "tool.completed");
    expect(toolCompleted?.data).toMatchObject({
      toolName: "read_file",
      source: "chirality-runtime-tool-bridge",
      resultMetadata: {
        rawOutputPersisted: false,
        byteLength: expect.any(Number)
      }
    });
    expect(JSON.stringify(toolCompleted)).not.toContain("known-value");
  });

  it("fails with REQUIRED_DELEGATION_MISSING when the manager skips the child", async () => {
    const { coordinator } = await setup("missing");
    const events: UIEvent[] = [];
    for await (const event of coordinator.run("agent-pilot", {
      brief: "Must delegate.",
      localModel: "qwen",
      agentId: "WORKING_ITEMS",
      approvalReference: "D-TEST",
      readOnlyTool: { name: "read_file", relativePath: "known.txt" }
    })) {
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
    expect(events.at(-1)).toMatchObject({ type: "process:exit", data: { exitCode: 1 } });
  });

  it("fails closed when the child answers without executing read_file", async () => {
    const { coordinator, sessions } = await setup("child-no-tool");
    const events: UIEvent[] = [];
    for await (const event of coordinator.run("agent-pilot", {
      brief: "The child must actually read the file.",
      localModel: "qwen",
      agentId: "WORKING_ITEMS",
      approvalReference: "D-TEST",
      readOnlyTool: { name: "read_file", relativePath: "known.txt" }
    })) {
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
    expect(events.at(-1)).toMatchObject({ type: "process:exit", data: { exitCode: 1 } });
    const records = await sessions.list("agent-pilot");
    const managerSession = records.find((session) => session.role === "agent1");
    const childSession = records.find((session) => session.role === "agent2");
    expect(managerSession).toMatchObject({ status: "failed" });
    expect(childSession).toMatchObject({ status: "failed" });
    const childEvents = await sessions.replay("agent-pilot", childSession!.sessionId);
    expect(childEvents.map((event) => event.type)).toContain("turn.failed");
    expect(childEvents.map((event) => event.type)).not.toContain("turn.completed");
  });

  it("persists a failed child terminal status when tool preparation fails", async () => {
    const { coordinator, root } = await setup("success");
    const events: UIEvent[] = [];
    for await (const event of coordinator.run("agent-pilot", {
      brief: "Attempt the missing governed file.",
      localModel: "qwen",
      agentId: "WORKING_ITEMS",
      approvalReference: "D-TEST",
      readOnlyTool: { name: "read_file", relativePath: "missing.txt" }
    })) {
      events.push(event);
    }
    expect(events.at(-1)).toMatchObject({ type: "process:exit", data: { exitCode: 1 } });
    const runRoots = await readdir(
      join(root, "execution", "_Coordination", "AgentRuns", "runtime")
    );
    const record = JSON.parse(
      await readFile(
        join(
          root,
          "execution",
          "_Coordination",
          "AgentRuns",
          "runtime",
          runRoots[0]!,
          "run.json"
        ),
        "utf8"
      )
    );
    expect(record).toMatchObject({
      status: "failed",
      child: { status: "failed" }
    });
  });

  it("interrupts an active manager and persists an interrupted AgentRun", async () => {
    const { coordinator, root, sessions } = await setup("blocking");
    const stream = coordinator.run("agent-pilot", {
      brief: "Wait for interruption.",
      agentId: "WORKING_ITEMS",
      approvalReference: "D-TEST"
    });
    const accepted = await stream.next();
    expect(accepted.value).toMatchObject({ type: "harness:event" });
    const managerSessionId =
      accepted.value?.type === "harness:event"
        ? accepted.value.data.sessionId
        : "";
    const pending = stream.next();
    await coordinator.interrupt("agent-pilot", managerSessionId);
    const terminal = await pending;
    expect(terminal.value).toMatchObject({
      type: "harness:event",
      data: { type: "turn.interrupted" }
    });
    const remaining: UIEvent[] = [];
    for await (const event of stream) remaining.push(event);
    expect(remaining.at(-1)).toMatchObject({
      type: "process:exit",
      data: { exitCode: 1, errorType: "INTERRUPTED" }
    });
    const runRoots = await readdir(
      join(root, "execution", "_Coordination", "AgentRuns", "runtime")
    );
    const record = JSON.parse(
      await readFile(
        join(
          root,
          "execution",
          "_Coordination",
          "AgentRuns",
          "runtime",
          runRoots[0]!,
          "run.json"
        ),
        "utf8"
      )
    );
    expect(record.status).toBe("interrupted");
    const managerSession = (await sessions.list("agent-pilot")).find(
      (session) => session.role === "agent1"
    );
    expect(managerSession).toMatchObject({ status: "interrupted" });
  });

  it("interrupts an active Agent 2 child and preserves canonical child interruption evidence", async () => {
    const { coordinator, root, childStarted, childInterrupts } =
      await setup("child-blocking");
    const stream = coordinator.run("agent-pilot", {
      brief: "Delegate, then wait while the child is active.",
      localModel: "qwen",
      agentId: "WORKING_ITEMS",
      approvalReference: "D-TEST",
      readOnlyTool: { name: "read_file", relativePath: "known.txt" }
    });
    const accepted = await stream.next();
    const managerSessionId =
      accepted.value?.type === "harness:event"
        ? accepted.value.data.sessionId
        : "";
    const pending = stream.next();
    await childStarted;
    await coordinator.interrupt("agent-pilot", managerSessionId);
    const events: UIEvent[] = [];
    const firstAfterInterrupt = await pending;
    if (!firstAfterInterrupt.done) events.push(firstAfterInterrupt.value);
    for await (const event of stream) events.push(event);

    expect(childInterrupts()).toBeGreaterThan(0);
    expect(events).toContainEqual(
      expect.objectContaining({
        type: "harness:event",
        data: expect.objectContaining({ type: "turn.interrupted" })
      })
    );
    expect(events.at(-1)).toMatchObject({
      type: "process:exit",
      data: { exitCode: 1, errorType: "INTERRUPTED" }
    });

    const runRoots = await readdir(
      join(root, "execution", "_Coordination", "AgentRuns", "runtime")
    );
    const record = JSON.parse(
      await readFile(
        join(
          root,
          "execution",
          "_Coordination",
          "AgentRuns",
          "runtime",
          runRoots[0]!,
          "run.json"
        ),
        "utf8"
      )
    );
    expect(record).toMatchObject({
      status: "interrupted",
      failureCode: "INTERRUPTED",
      child: {
        status: "interrupted",
        sealedBrief: "Read the governed file."
      }
    });
    const childEvents = JSON.parse(
      await readFile(
        join(
          root,
          "user-data",
          "runtime",
          "projects",
          "agent-pilot",
          "sessions",
          record.child.sessionId,
          "events.jsonl"
        ),
        "utf8"
      ).then((line) => `[${line.trim().split("\n").join(",")}]`)
    );
    expect(childEvents).toContainEqual(
      expect.objectContaining({ type: "turn.interrupted" })
    );
  });

  it("reserves the manager session against ordinary turns for the whole governed run", async () => {
    const { coordinator, service, childStarted } = await setup("child-blocking");
    const stream = coordinator.run("agent-pilot", {
      brief: "Keep the manager reservation while the child runs.",
      localModel: "qwen",
      agentId: "WORKING_ITEMS",
      approvalReference: "D-TEST",
      readOnlyTool: { name: "read_file", relativePath: "known.txt" }
    });
    const accepted = await stream.next();
    const managerSessionId =
      accepted.value?.type === "harness:event"
        ? accepted.value.data.sessionId
        : "";
    const pending = stream.next();
    await childStarted;
    expect(() =>
      service.runSessionTurn("agent-pilot", managerSessionId, {
        prompt: "must not interleave"
      })
    ).toThrowError(
      expect.objectContaining({ code: "SESSION_TURN_IN_PROGRESS" })
    );
    await coordinator.interrupt("agent-pilot", managerSessionId);
    await pending;
    for await (const _event of stream) {
      // drain
    }
  });
});
