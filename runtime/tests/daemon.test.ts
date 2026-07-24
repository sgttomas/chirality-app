import { request as httpRequest } from "node:http";
import { chmod, mkdir, mkdtemp, readFile, stat, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { afterEach, describe, expect, it } from "vitest";
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
  TurnCoordinator,
  atomicWriteJson
} from "@chirality/runtime-core";
import { RuntimeDaemon } from "@chirality/runtime-daemon";
import { createProjectFixture } from "./helpers.js";

const active: RuntimeDaemon[] = [];
afterEach(async () => {
  await Promise.all(active.splice(0).map(async (daemon) => daemon.stop().catch(() => undefined)));
});

function request(
  socketPath: string,
  path: string,
  token?: string,
  method = "GET",
  body?: unknown
): Promise<{ status: number; body: string }> {
  return new Promise((resolve, reject) => {
    const encoded = body === undefined ? undefined : JSON.stringify(body);
    const outgoing = httpRequest(
      {
        socketPath,
        path,
        method,
        headers: {
          ...(token === undefined ? {} : { authorization: `Bearer ${token}` }),
          ...(encoded === undefined
            ? {}
            : {
                "content-type": "application/json",
                "content-length": Buffer.byteLength(encoded)
              })
        }
      },
      (response) => {
        const chunks: Buffer[] = [];
        response.on("data", (chunk) => chunks.push(Buffer.from(chunk)));
        response.on("end", () =>
          resolve({
            status: response.statusCode ?? 0,
            body: Buffer.concat(chunks).toString("utf8")
          })
        );
      }
    );
    outgoing.once("error", reject);
    if (encoded !== undefined) outgoing.write(encoded);
    outgoing.end();
  });
}

function disconnectAfterFirstChunk(
  socketPath: string,
  path: string,
  token: string,
  body: unknown
): Promise<void> {
  return new Promise((resolve, reject) => {
    const encoded = JSON.stringify(body);
    const outgoing = httpRequest(
      {
        socketPath,
        path,
        method: "POST",
        headers: {
          authorization: `Bearer ${token}`,
          "content-type": "application/json",
          "content-length": Buffer.byteLength(encoded)
        }
      },
      (response) => {
        response.once("data", () => {
          response.destroy();
          outgoing.destroy();
          resolve();
        });
        response.once("error", (error) => {
          if (!response.destroyed) reject(error);
        });
      }
    );
    outgoing.once("error", (error) => {
      if (!outgoing.destroyed) reject(error);
    });
    outgoing.write(encoded);
    outgoing.end();
  });
}

async function fixture(
  root: string,
  runner: { run(): AsyncIterable<UIEvent>; interrupt?(): Promise<void> } = {
    async *run(): AsyncIterable<UIEvent> {
      yield { type: "chat:delta", data: { text: "hello" } };
      yield { type: "process:exit", data: { exitCode: 0 } };
    }
  }
) {
  const runtime = join(root, "runtime");
  const projects = new ProjectRegistry(runtime);
  const sessions = new SessionStore(runtime, projects);
  const engines = new EngineRegistry();
  const control: OmlxControlPort = {
    async listStatus() {
      return [];
    },
    async load() {},
    async unload() {}
  };
  const residency = new ResidencyCoordinator(control, runtime);
  const auth = new AuthRegistry(runtime);
  const credentials = {
    async get() {
      return undefined;
    },
    async status() {
      return { configured: false };
    },
    async set() {},
    async remove() {}
  };
  const turns = new TurnCoordinator(projects, sessions, engines, residency);
  const service = new RuntimeService(
    projects,
    sessions,
    engines,
    residency,
    turns,
    auth,
    credentials,
    undefined,
    runner
  );
  return { runtime, service, engines, sessions };
}

describe("Unix-domain runtime daemon", () => {
  it("revokes every superseded project credential during re-registration", async () => {
    const root = await mkdtemp(join(tmpdir(), "chirality-reregister-"));
    const { service } = await fixture(root);
    const { manifestPath } = await createProjectFixture(
      join(root, "project"),
      "reregister-project"
    );
    await expect(
      service.registerProject(manifestPath, "test", "   ")
    ).rejects.toMatchObject({ code: "INVALID_REQUEST" });
    const first = await service.registerProject(manifestPath, "test", "D-TEST-1");
    const firstToken = (await readFile(first.tokenFile, "utf8")).trim();
    await expect(
      service.auth.authenticate(
        `Bearer ${firstToken}`,
        "sessions:read",
        "reregister-project"
      )
    ).resolves.toMatchObject({ projectId: "reregister-project" });

    const second = await service.registerProject(manifestPath, "test", "D-TEST-2");
    const secondToken = (await readFile(second.tokenFile, "utf8")).trim();
    await expect(
      service.auth.authenticate(
        `Bearer ${firstToken}`,
        "sessions:read",
        "reregister-project"
      )
    ).rejects.toMatchObject({ code: "UNAUTHORIZED" });
    await expect(
      service.auth.authenticate(
        `Bearer ${secondToken}`,
        "sessions:read",
        "reregister-project"
      )
    ).resolves.toMatchObject({ clientId: second.clientId });
  });

  it("uses private files, authenticates, and preserves UIEvent SSE wire format", async () => {
    const root = await mkdtemp(join(tmpdir(), "chirality-daemon-"));
    const { runtime, service } = await fixture(root);
    const socketPath = join(runtime, "control.sock");
    const daemon = new RuntimeDaemon({ runtimeDirectory: runtime, socketPath, service });
    active.push(daemon);
    const started = await daemon.start();
    expect((await stat(runtime)).mode & 0o777).toBe(0o700);
    expect((await stat(socketPath)).mode & 0o777).toBe(0o600);
    expect((await stat(`${socketPath}.owner.json`)).mode & 0o777).toBe(0o600);
    expect((await request(socketPath, "/v1/health")).status).toBe(401);
    const operator = (await readFile(started.operatorTokenFile, "utf8")).trim();
    const health = await request(socketPath, "/v1/health", operator);
    expect(health.status).toBe(200);
    expect(JSON.parse(health.body)).toMatchObject({ apiVersion: "v1", status: "ok" });

    const projectRoot = join(root, "project");
    const { manifestPath } = await createProjectFixture(projectRoot, "daemon-project");
    const registered = await service.registerProject(manifestPath, "test", "D-TEST");
    const projectToken = (await readFile(registered.tokenFile, "utf8")).trim();
    const stream = await request(
      socketPath,
      "/v1/projects/daemon-project/runs",
      projectToken,
      "POST",
      { brief: "test", approvalReference: "D-TEST" }
    );
    expect(stream.status).toBe(200);
    expect(stream.body).toContain("event: chat:delta\ndata: {\"text\":\"hello\"}\n\n");
    expect(stream.body).not.toContain("\"type\":\"chat:delta\"");

    const otherRoot = join(root, "other-project");
    const { manifestPath: otherManifest } = await createProjectFixture(
      otherRoot,
      "other-project"
    );
    await service.registerProject(otherManifest, "test", "D-TEST");
    const visible = await request(socketPath, "/v1/projects", projectToken);
    expect(JSON.parse(visible.body).projects).toHaveLength(1);
    expect(JSON.parse(visible.body).projects[0].project.projectId).toBe(
      "daemon-project"
    );
  });

  it("returns a typed non-200 response when a stream fails before its first event", async () => {
    const root = await mkdtemp(join(tmpdir(), "ch-daemon-fail-"));
    const { runtime, service } = await fixture(root, {
      async *run(): AsyncIterable<UIEvent> {
        throw new Error("pre-stream failure");
      }
    });
    const socketPath = join(runtime, "control.sock");
    const daemon = new RuntimeDaemon({ runtimeDirectory: runtime, socketPath, service });
    active.push(daemon);
    await daemon.start();
    const projectRoot = join(root, "project");
    const { manifestPath } = await createProjectFixture(projectRoot, "stream-fail");
    const registered = await service.registerProject(manifestPath, "test", "D-TEST");
    const token = (await readFile(registered.tokenFile, "utf8")).trim();
    const response = await request(
      socketPath,
      "/v1/projects/stream-fail/runs",
      token,
      "POST",
      { brief: "test", approvalReference: "D-TEST" }
    );
    expect(response.status).toBe(500);
    expect(JSON.parse(response.body)).toMatchObject({
      error: { code: "INTERNAL_FAILURE" }
    });
  });

  it("interrupts and drains a disconnected SSE turn through canonical terminal persistence", async () => {
    const root = await mkdtemp(join(tmpdir(), "ch-daemon-disconnect-"));
    const { runtime, service, engines, sessions } = await fixture(root);
    let releaseEngine!: () => void;
    const interrupted = new Promise<void>((resolve) => {
      releaseEngine = resolve;
    });
    const engine: AgentEnginePort = {
      descriptor: {
        adapterId: "stub",
        providerId: "stub",
        capabilities: {
          credentials: false,
          tools: false,
          attachments: false,
          interruption: true,
          durableResume: false,
          compaction: false
        }
      },
      subject: "disconnect-test",
      async preflight() {},
      async *startTurn(input) {
        yield {
          type: "session:init",
          data: {
            engineSessionId: `engine-${input.session.sessionId}`,
            adapterId: "stub",
            providerId: "stub",
            model: input.opts.model
          }
        };
        await interrupted;
      },
      async interrupt() {
        releaseEngine();
      }
    };
    engines.register(engine);

    const socketPath = join(runtime, "control.sock");
    const daemon = new RuntimeDaemon({ runtimeDirectory: runtime, socketPath, service });
    active.push(daemon);
    await daemon.start();
    const projectRoot = join(root, "project");
    const { manifestPath } = await createProjectFixture(
      projectRoot,
      "disconnect-project"
    );
    const registered = await service.registerProject(manifestPath, "test", "D-TEST");
    const token = (await readFile(registered.tokenFile, "utf8")).trim();
    const session = await service.createSession({
      projectId: "disconnect-project",
      role: "agent1",
      engineSelection: {
        adapterId: "stub",
        providerId: "stub",
        model: "blocking"
      },
      persona: "WORKING_ITEMS"
    });

    await disconnectAfterFirstChunk(
      socketPath,
      `/v1/projects/disconnect-project/sessions/${session.sessionId}/turn`,
      token,
      { prompt: "wait for disconnect" }
    );

    let events = await sessions.replay("disconnect-project", session.sessionId);
    let storedSession = await sessions.get("disconnect-project", session.sessionId);
    for (let attempt = 0; attempt < 100; attempt += 1) {
      if (
        events.some((event) => event.type === "turn.interrupted") &&
        storedSession.status === "interrupted"
      ) {
        break;
      }
      await new Promise((resolve) => setTimeout(resolve, 10));
      events = await sessions.replay("disconnect-project", session.sessionId);
      storedSession = await sessions.get("disconnect-project", session.sessionId);
    }
    expect(events.filter((event) => event.type === "turn.interrupted")).toHaveLength(1);
    expect(
      events.filter((event) =>
        ["turn.completed", "turn.failed", "turn.cancelled"].includes(event.type)
      )
    ).toHaveLength(0);
    expect(storedSession).toMatchObject({ status: "interrupted" });
  });

  it("fails closed for a non-socket or ambiguous live owner record", async () => {
    const root = await mkdtemp(join(tmpdir(), "chirality-daemon-stale-"));
    const first = await fixture(root);
    const socketPath = join(first.runtime, "control.sock");
    await mkdir(first.runtime, { recursive: true });
    await writeFile(socketPath, "not a socket", "utf8");
    const daemon = new RuntimeDaemon({
      runtimeDirectory: first.runtime,
      socketPath,
      service: first.service
    });
    await expect(daemon.start()).rejects.toMatchObject({ code: "FORBIDDEN" });

    const root2 = await mkdtemp(join(tmpdir(), "chirality-daemon-owner-"));
    const second = await fixture(root2);
    const socket2 = join(second.runtime, "control.sock");
    await atomicWriteJson(`${socket2}.owner.json`, {
      schemaVersion: "chirality.daemon-owner/v1",
      daemonId: "live",
      pid: process.pid,
      uid: process.getuid?.() ?? -1,
      socketPath: socket2,
      startedAt: new Date().toISOString()
    });
    await chmod(`${socket2}.owner.json`, 0o600);
    const daemon2 = new RuntimeDaemon({
      runtimeDirectory: second.runtime,
      socketPath: socket2,
      service: second.service
    });
    await expect(daemon2.start()).rejects.toMatchObject({ code: "FORBIDDEN" });
  });
});
