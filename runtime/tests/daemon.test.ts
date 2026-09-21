import { Agent, request as httpRequest, type ClientRequest } from "node:http";
import { chmod, mkdir, mkdtemp, readFile, stat, unlink, writeFile } from "node:fs/promises";
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
import { RuntimeDaemon, describeRuntimeFailure } from "../packages/daemon/src/runtime-daemon.js";
import { RuntimeError, type PendingServerRequest, type ServerRequestAnswer } from "@chirality/runtime-contracts";
import { createDelegatedPermissionBroker, type PermissionDecisionPort } from "@chirality/runtime-core";
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

function openIncompleteRequest(
  socketPath: string,
  path: string,
  token: string
): Promise<{ outgoing: ClientRequest; disconnected: Promise<void> }> {
  return new Promise((resolve, reject) => {
    const outgoing = httpRequest({
      socketPath,
      path,
      method: "POST",
      headers: {
        authorization: `Bearer ${token}`,
        "content-type": "application/json",
        "content-length": "100"
      }
    });
    const disconnected = new Promise<void>((disconnectedResolve) => {
      outgoing.once("error", () => disconnectedResolve());
      outgoing.once("close", () => disconnectedResolve());
    });
    outgoing.once("socket", (socket) => {
      socket.once("connect", () => resolve({ outgoing, disconnected }));
    });
    outgoing.once("error", reject);
    outgoing.write("{");
  });
}

function openStream(
  socketPath: string,
  path: string,
  token: string,
  body: unknown
): Promise<{ outgoing: ClientRequest; firstChunk: Promise<void>; disconnected: Promise<void> }> {
  const encoded = JSON.stringify(body);
  const outgoing = httpRequest({
    socketPath,
    path,
    method: "POST",
    headers: {
      authorization: `Bearer ${token}`,
      "content-type": "application/json",
      "content-length": Buffer.byteLength(encoded)
    }
  });
  const firstChunk = new Promise<void>((resolve, reject) => {
    outgoing.once("response", (response) => response.once("data", () => resolve()));
    outgoing.once("error", reject);
  });
  const disconnected = new Promise<void>((resolve) => {
    outgoing.once("response", (response) => {
      response.once("error", () => resolve());
      response.once("close", () => resolve());
    });
    outgoing.once("error", () => resolve());
    outgoing.once("close", () => resolve());
  });
  outgoing.write(encoded);
  outgoing.end();
  return Promise.resolve({ outgoing, firstChunk, disconnected });
}

function daemonLifecycle(daemon: RuntimeDaemon): string {
  return (daemon as unknown as { lifecycle: string }).lifecycle;
}

function streamRequest(
  socketPath: string,
  path: string,
  token: string,
  method = "GET",
  body?: unknown
): { chunks: Promise<string[]>; outgoing: ClientRequest; status: Promise<number> } {
  const encoded = body === undefined ? undefined : JSON.stringify(body);
  const outgoing = httpRequest({
    socketPath,
    path,
    method,
    headers: {
      authorization: `Bearer ${token}`,
      ...(encoded === undefined ? {} : { "content-type": "application/json", "content-length": Buffer.byteLength(encoded) })
    }
  });
  const status = new Promise<number>((resolve, reject) => {
    outgoing.once("response", (response) => resolve(response.statusCode ?? 0));
    outgoing.once("error", reject);
  });
  const chunks = new Promise<string[]>((resolve, reject) => {
    outgoing.once("response", (response) => {
      const received: string[] = [];
      response.on("data", (chunk) => received.push(Buffer.from(chunk).toString("utf8")));
      response.once("end", () => resolve(received));
      response.once("error", reject);
    });
    outgoing.once("error", reject);
  });
  if (encoded !== undefined) outgoing.write(encoded);
  outgoing.end();
  return { chunks, outgoing, status };
}

function gatedEngine(adapterId = "stub"): { engine: AgentEnginePort; release(): void; interrupts: number; released: Promise<void> } {
  let release!: () => void;
  const released = new Promise<void>((resolve) => { release = resolve; });
  const state = { interrupts: 0 };
  const engine: AgentEnginePort = {
    descriptor: { adapterId, providerId: "stub", capabilities: { credentials: false, tools: false, attachments: false, interruption: true, durableResume: false, compaction: false } },
    subject: "gated",
    async preflight() {},
    async *startTurn(input) {
      yield { type: "session:init", data: { engineSessionId: `engine-${input.session.sessionId}`, adapterId, providerId: "stub", model: input.opts.model } };
      yield { type: "chat:delta", data: { text: "before" } };
      await released;
      if (input.signal?.aborted) { yield { type: "process:exit", data: { exitCode: 130, interrupted: true } }; return; }
      yield { type: "chat:delta", data: { text: "missed" } };
      yield { type: "process:exit", data: { exitCode: 0 } };
    },
    async interrupt() { state.interrupts += 1; release(); }
  };
  return { engine, release, released, get interrupts() { return state.interrupts; } };
}

async function fixture(
  root: string,
  runner: { run(): AsyncIterable<UIEvent>; interrupt?(): Promise<void> } = {
    async *run(): AsyncIterable<UIEvent> {
      yield { type: "chat:delta", data: { text: "hello" } };
      yield { type: "process:exit", data: { exitCode: 0 } };
    }
  },
  permissions?: PermissionDecisionPort
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
    runner,
    permissions
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
    const logged: Array<{ event: string; fields?: Readonly<Record<string, unknown>> }> = [];
    const logger = { warn(event: string, fields?: Readonly<Record<string, unknown>>) { logged.push({ event, fields }); }, error(event: string, fields?: Readonly<Record<string, unknown>>) { logged.push({ event, fields }); } };
    const daemon = new RuntimeDaemon({ runtimeDirectory: runtime, socketPath, service, logger });
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
    // A server-side failure is logged with its route identity and bounded diagnostics, never the body or query.
    const failed = logged.filter(entry => entry.event === "runtime.daemon.request.failed");
    expect(failed).toHaveLength(1);
    expect(failed[0]!.fields).toMatchObject({ method: "POST", path: "/v1/projects/stream-fail/runs", code: "INTERNAL_FAILURE", status: 500, cause: "pre-stream failure" });
    expect(JSON.stringify(failed[0]!.fields)).not.toContain("D-TEST");
    // Client errors stay quiet.
    const missing = await request(socketPath, "/v1/projects/stream-fail/unknown-route", token, "GET");
    expect(missing.status).toBe(404);
    expect(logged.filter(entry => entry.event === "runtime.daemon.request.failed")).toHaveLength(1);
  });

  it("describes a supplier rejection with its method, code and bounded message", () => {
    const described = describeRuntimeFailure(new RuntimeError("ENGINE_UNAVAILABLE", "Codex rejected the requested operation", 503, { reason: "CODEX_REQUEST_REJECTED", method: "turn/start", codexCode: -32600, codexMessage: `bad\u0000model ${"x".repeat(300)}` }));
    expect(described).toMatchObject({ code: "ENGINE_UNAVAILABLE", status: 503, reason: "CODEX_REQUEST_REJECTED", method: "turn/start", codexCode: -32600 });
    expect(described.codexMessage).toBe(`bad model ${"x".repeat(300)}`.slice(0, 256));
    expect(describeRuntimeFailure(new RuntimeError("ENGINE_UNAVAILABLE", "plain", 503))).not.toHaveProperty("method");
  });

  it("keeps a turn running after its subscriber disconnects and replays the missed frames on attach", async () => {
    const root = await mkdtemp(join(tmpdir(), "ch-daemon-disconnect-"));
    const { runtime, service, engines, sessions } = await fixture(root);
    const gated = gatedEngine();
    engines.register(gated.engine);
    const socketPath = join(runtime, "control.sock");
    const daemon = new RuntimeDaemon({ runtimeDirectory: runtime, socketPath, service });
    active.push(daemon);
    await daemon.start();
    const { manifestPath } = await createProjectFixture(join(root, "project"), "disconnect-project");
    const registered = await service.registerProject(manifestPath, "test", "D-TEST");
    const token = (await readFile(registered.tokenFile, "utf8")).trim();
    const session = await service.createSession({ projectId: "disconnect-project", role: "agent1", engineSelection: { adapterId: "stub", providerId: "stub", model: "blocking" }, persona: "WORKING_ITEMS" });
    const base = `/v1/projects/disconnect-project/sessions/${session.sessionId}`;

    await disconnectAfterFirstChunk(socketPath, `${base}/turn`, token, { prompt: "wait for disconnect" });

    // The Runtime still owns the turn: nothing was interrupted and the state reports it active.
    let state = JSON.parse((await request(socketPath, `${base}/turn/state`, token)).body);
    for (let attempt = 0; attempt < 100 && state.lastSeq < 3; attempt += 1) {
      await new Promise((resolve) => setTimeout(resolve, 10));
      state = JSON.parse((await request(socketPath, `${base}/turn/state`, token)).body);
    }
    expect(state).toMatchObject({ active: true, lastSeq: 3, turnId: expect.any(String), startedAt: expect.any(String) });
    expect(gated.interrupts).toBe(0);
    expect(await sessions.get("disconnect-project", session.sessionId)).toMatchObject({ status: "running" });
    // A second start is refused while the turn is active.
    const conflict = await request(socketPath, `${base}/turn`, token, "POST", { prompt: "second" });
    expect(conflict.status).toBe(409);
    expect(JSON.parse(conflict.body)).toMatchObject({ error: { code: "SESSION_TURN_IN_PROGRESS" } });

    // Attaching after the disconnect delivers the frames missed since seq 1, then the live remainder.
    const attached = streamRequest(socketPath, `${base}/turn/stream?after=1`, token);
    expect(await attached.status).toBe(200);
    gated.release();
    const body = (await attached.chunks).join("");
    expect(body).not.toContain("id: 1\n");
    expect(body).toContain("id: 2\nevent: session:init\n");
    expect(body).toContain("id: 3\nevent: chat:delta\ndata: {\"text\":\"before\"}\n\n");
    expect(body).toContain("id: 4\nevent: chat:delta\ndata: {\"text\":\"missed\"}\n\n");
    expect(body).toContain("event: process:exit\n");
    expect(gated.interrupts).toBe(0);
    const events = await sessions.replay("disconnect-project", session.sessionId);
    expect(events.filter((event) => event.type === "turn.completed")).toHaveLength(1);
    expect(events.filter((event) => event.type === "turn.interrupted")).toHaveLength(0);
    expect(await sessions.get("disconnect-project", session.sessionId)).toMatchObject({ status: "completed", lastUsedModel: "blocking" });
    const finished = JSON.parse((await request(socketPath, `${base}/turn/state`, token)).body);
    expect(finished).toMatchObject({ active: false, lastSeq: 6, endedAt: expect.any(String) });
    // The retained buffer is still attachable and replays completely.
    const replayed = await request(socketPath, `${base}/turn/stream?after=0`, token);
    expect(replayed.status).toBe(200);
    expect(replayed.body.match(/^id: /gmu)).toHaveLength(6);
    const matched = await request(socketPath, `${base}/turn/stream?after=0&turnId=${finished.turnId}`, token);
    expect(matched.status).toBe(200);
    const stale = await request(socketPath, `${base}/turn/stream?after=0&turnId=new-submission`, token);
    expect(stale.status).toBe(404);
    expect(JSON.parse(stale.body)).toMatchObject({ error: { code: "TURN_NOT_ACTIVE" } });
    expect(stale.body).not.toContain('event: chat:delta');
  });

  it("interrupts only through the interrupt route and reports 404 TURN_NOT_ACTIVE without a turn", async () => {
    const root = await mkdtemp(join(tmpdir(), "ch-daemon-interrupt-"));
    const { runtime, service, engines, sessions } = await fixture(root);
    const gated = gatedEngine();
    engines.register(gated.engine);
    const socketPath = join(runtime, "control.sock");
    const daemon = new RuntimeDaemon({ runtimeDirectory: runtime, socketPath, service });
    active.push(daemon);
    await daemon.start();
    const { manifestPath } = await createProjectFixture(join(root, "project"), "interrupt-project");
    const registered = await service.registerProject(manifestPath, "test", "D-TEST");
    const token = (await readFile(registered.tokenFile, "utf8")).trim();
    const session = await service.createSession({ projectId: "interrupt-project", role: "agent1", engineSelection: { adapterId: "stub", providerId: "stub", model: "blocking" }, persona: "WORKING_ITEMS" });
    const base = `/v1/projects/interrupt-project/sessions/${session.sessionId}`;

    const missing = await request(socketPath, `${base}/turn/stream`, token);
    expect(missing.status).toBe(404);
    expect(JSON.parse(missing.body)).toMatchObject({ error: { code: "TURN_NOT_ACTIVE" } });
    expect(JSON.parse((await request(socketPath, `${base}/turn/state`, token)).body)).toEqual({ active: false, lastSeq: 0 });
    const malformed = await request(socketPath, `${base}/turn/stream?after=-1`, token);
    expect(malformed.status).toBe(400);

    await disconnectAfterFirstChunk(socketPath, `${base}/turn`, token, { prompt: "hold" });
    const interrupted = await request(socketPath, `${base}/interrupt`, token, "POST");
    expect(interrupted.status).toBe(200);
    expect(gated.interrupts).toBe(1);
    let events = await sessions.replay("interrupt-project", session.sessionId);
    for (let attempt = 0; attempt < 100 && !events.some((event) => event.type === "turn.interrupted"); attempt += 1) {
      await new Promise((resolve) => setTimeout(resolve, 10));
      events = await sessions.replay("interrupt-project", session.sessionId);
    }
    expect(events.filter((event) => event.type === "turn.interrupted")).toHaveLength(1);
    expect(await sessions.get("interrupt-project", session.sessionId)).toMatchObject({ status: "interrupted" });
    expect(JSON.parse((await request(socketPath, `${base}/turn/state`, token)).body)).toMatchObject({ active: false });
  });

  it("emits keepalive comments on an idle stream without touching the turn", async () => {
    const root = await mkdtemp(join(tmpdir(), "ch-daemon-keepalive-"));
    const { runtime, service, engines } = await fixture(root);
    const gated = gatedEngine();
    engines.register(gated.engine);
    const socketPath = join(runtime, "control.sock");
    const daemon = new RuntimeDaemon({ runtimeDirectory: runtime, socketPath, service, sseKeepaliveMs: 20 });
    active.push(daemon);
    await daemon.start();
    const { manifestPath } = await createProjectFixture(join(root, "project"), "keepalive-project");
    const registered = await service.registerProject(manifestPath, "test", "D-TEST");
    const token = (await readFile(registered.tokenFile, "utf8")).trim();
    const session = await service.createSession({ projectId: "keepalive-project", role: "agent1", engineSelection: { adapterId: "stub", providerId: "stub", model: "blocking" }, persona: "WORKING_ITEMS" });
    const stream = streamRequest(socketPath, `/v1/projects/keepalive-project/sessions/${session.sessionId}/turn`, token, "POST", { prompt: "idle" });
    expect(await stream.status).toBe(200);
    await new Promise((resolve) => setTimeout(resolve, 120));
    expect(gated.interrupts).toBe(0);
    const state = JSON.parse((await request(socketPath, `/v1/projects/keepalive-project/sessions/${session.sessionId}/turn/state`, token)).body);
    const attached = streamRequest(socketPath, `/v1/projects/keepalive-project/sessions/${session.sessionId}/turn/stream?after=${state.lastSeq}`, token);
    // Headers and heartbeat arrive even when no buffered/model frame is due.
    expect(await attached.status).toBe(200);
    await new Promise(resolve => setTimeout(resolve, 80));
    expect(gated.interrupts).toBe(0);
    gated.release();
    const attachedBody = (await attached.chunks).join("");
    expect(attachedBody).toContain(": keepalive\n\n");
    expect(attachedBody).not.toContain("id: 1\n");
    const body = (await stream.chunks).join("");
    expect(body.split(": keepalive\n\n").length - 1).toBeGreaterThanOrEqual(2);
    expect(body.indexOf(": keepalive")).toBeGreaterThan(body.indexOf("id: 1\nevent: harness:event\n"));
    expect(body).toContain("event: process:exit\n");
  });

  it("serves pending server requests and answers, and validates answer shapes", async () => {
    const root = await mkdtemp(join(tmpdir(), "ch-daemon-requests-"));
    const { runtime, service } = await fixture(root);
    const pending: PendingServerRequest[] = [{ requestId: "17", method: "item/tool/requestUserInput", params: { itemId: "item-q" }, itemId: "item-q", receivedAt: "2026-09-12T00:00:00.000Z" }];
    const answered: { projectId: string; sessionId: string; requestId: string; answer: ServerRequestAnswer }[] = [];
    const socketPath = join(runtime, "control.sock");
    const daemon = new RuntimeDaemon({ runtimeDirectory: runtime, socketPath, service, requests: {
      async pendingRequests() { return pending; },
      async answerRequest(projectId, sessionId, requestId, answer) { answered.push({ projectId, sessionId, requestId, answer }); return { sent: true }; }
    } });
    active.push(daemon);
    await daemon.start();
    const { manifestPath } = await createProjectFixture(join(root, "project"), "requests-project");
    const registered = await service.registerProject(manifestPath, "test", "D-TEST");
    const token = (await readFile(registered.tokenFile, "utf8")).trim();
    const session = await service.createSession({ projectId: "requests-project", role: "agent1", engineSelection: { adapterId: "stub", providerId: "stub", model: "fixture" }, persona: "WORKING_ITEMS" });
    const base = `/v1/projects/requests-project/sessions/${session.sessionId}`;
    const listed = await request(socketPath, `${base}/requests`, token);
    expect(listed.status).toBe(200);
    expect(JSON.parse(listed.body)).toEqual({ requests: pending });
    // Side input is an authorized session route, and idle sessions never send it.
    const steering = { operationId: "route-steer-1", expectedTurnId: "expired", text: "Change direction" };
    expect((await request(socketPath, `${base}/turn/steer`, "invalid-token", "POST", steering)).status).toBe(401);
    expect((await request(socketPath, `${base}/turn/steer`, token, "POST", { ...steering, nativeThreadId: "unowned" })).status).toBe(400);
    const receiptRequest = { operationId: steering.operationId, expectedTurnId: steering.expectedTurnId };
    expect((await request(socketPath, `${base}/turn/steer/receipt`, "invalid-token", "POST", receiptRequest)).status).toBe(401);
    expect((await request(socketPath, `${base}/turn/steer/receipt`, token, "POST", steering)).status).toBe(400);
    const missingReceipt = await request(socketPath, `${base}/turn/steer/receipt`, token, "POST", receiptRequest);
    expect(missingReceipt.status).toBe(200);
    expect(JSON.parse(missingReceipt.body)).toMatchObject({ status: "unknown" });
    expect((await service.sessions.replay("requests-project", session.sessionId)).filter(event => event.type === "codex.steer")).toHaveLength(0);
    const staleSteer = await request(socketPath, `${base}/turn/steer`, token, "POST", steering);
    expect(staleSteer.status).toBe(200);
    expect(JSON.parse(staleSteer.body)).toMatchObject({ status: "rejected", turnId: "expired", operationId: "route-steer-1" });
    const steeringEvents = (await service.sessions.replay("requests-project", session.sessionId)).filter(event => event.type === "codex.steer");
    expect(steeringEvents.map(event => event.data.status)).toEqual(["submitted", "rejected"]);
    const rejectedReceipt = await request(socketPath, `${base}/turn/steer/receipt`, token, "POST", receiptRequest);
    expect(JSON.parse(rejectedReceipt.body)).toMatchObject({ status: "rejected" });
    expect((await request(socketPath, `${base}/turn/steer/receipt`, token, "POST", { ...receiptRequest, expectedTurnId: "wrong-turn" })).status).toBe(409);
    expect((await request(socketPath, `/v1/projects/requests-project/sessions/missing-session/turn/steer/receipt`, token, "POST", receiptRequest)).status).toBe(404);

    expect((await request(socketPath, `${base}/turn/steer`, token, "POST", { ...steering, text: "Conflicting reuse" })).status).toBe(409);

    expect((await request(socketPath, `/v1/projects/requests-project/sessions/missing-session/requests`, token)).status).toBe(404);
    for (const body of [{ verdict: "allow" }, { answer: { kind: "approval", verdict: "maybe" } }, { answer: { kind: "userInput", answers: { q1: ["x"] } } }, { answer: { kind: "elicitation", action: "later" } }, { answer: { kind: "approval", verdict: "allow" }, extra: 1 }]) {
      const rejected = await request(socketPath, `${base}/requests/17/answer`, token, "POST", body);
      expect(rejected.status).toBe(400);
      expect(JSON.parse(rejected.body)).toMatchObject({ error: { code: "INVALID_REQUEST" } });
    }
    expect(answered).toEqual([]);
    const accepted = await request(socketPath, `${base}/requests/17/answer`, token, "POST", { answer: { kind: "userInput", answers: { q1: { answers: ["blue"] } } } });
    expect(accepted.status).toBe(200);
    expect(JSON.parse(accepted.body)).toEqual({ sent: true });
    const elicited = await request(socketPath, `${base}/requests/18/answer`, token, "POST", { answer: { kind: "elicitation", action: "accept", content: { ok: true } } });
    expect(elicited.status).toBe(200);
    expect(answered).toEqual([
      { projectId: "requests-project", sessionId: session.sessionId, requestId: "17", answer: { kind: "userInput", answers: { q1: { answers: ["blue"] } } } },
      { projectId: "requests-project", sessionId: session.sessionId, requestId: "18", answer: { kind: "elicitation", action: "accept", content: { ok: true } } }
    ]);
  });

  it("answers 503 for request routes without a request port and routes permission decisions to the approval answer", async () => {
    const root = await mkdtemp(join(tmpdir(), "ch-daemon-permission-"));
    const verdicts: unknown[][] = [];
    const { runtime, service } = await fixture(root, undefined, createDelegatedPermissionBroker({ async answerApprovalByToolUseId(...args) { verdicts.push(args); return { sent: true }; } }));
    const socketPath = join(runtime, "control.sock");
    const daemon = new RuntimeDaemon({ runtimeDirectory: runtime, socketPath, service });
    active.push(daemon);
    await daemon.start();
    const { manifestPath } = await createProjectFixture(join(root, "project"), "permission-project");
    const registered = await service.registerProject(manifestPath, "test", "D-TEST");
    const token = (await readFile(registered.tokenFile, "utf8")).trim();
    const session = await service.createSession({ projectId: "permission-project", role: "agent1", engineSelection: { adapterId: "stub", providerId: "stub", model: "fixture" }, persona: "WORKING_ITEMS" });
    const base = `/v1/projects/permission-project/sessions/${session.sessionId}`;
    expect((await request(socketPath, `${base}/requests`, token)).status).toBe(503);
    expect((await request(socketPath, `${base}/requests/1/answer`, token, "POST", { answer: { kind: "approval", verdict: "allow" } })).status).toBe(503);
    const decided = await request(socketPath, `${base}/permission`, token, "POST", { requestId: "item-7", decision: "deny" });
    expect(decided.status).toBe(200);
    expect(JSON.parse(decided.body)).toEqual({ accepted: true, requestId: "item-7", decision: "deny" });
    expect(verdicts).toEqual([["permission-project", session.sessionId, "item-7", "deny"]]);
    const invalid = await request(socketPath, `${base}/permission`, token, "POST", { requestId: "item-7", decision: "later" });
    expect(invalid.status).toBe(400);
    expect(verdicts).toHaveLength(1);
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
    await expect(readFile(socketPath, "utf8")).resolves.toBe("not a socket");

    const root2 = await mkdtemp(join(tmpdir(), "chirality-daemon-owner-"));
    const second = await fixture(root2);
    const socket2 = join(second.runtime, "control.sock");
    const liveOwner = {
      schemaVersion: "chirality.daemon-owner/v1",
      daemonId: "live",
      pid: process.pid,
      uid: process.getuid?.() ?? -1,
      socketPath: socket2,
      startedAt: new Date().toISOString()
    } as const;
    await atomicWriteJson(`${socket2}.owner.json`, liveOwner);
    await chmod(`${socket2}.owner.json`, 0o600);
    const liveOwnerBytes = await readFile(`${socket2}.owner.json`, "utf8");
    const daemon2 = new RuntimeDaemon({
      runtimeDirectory: second.runtime,
      socketPath: socket2,
      service: second.service
    });
    await expect(daemon2.start()).rejects.toMatchObject({ code: "FORBIDDEN" });
    await expect(stat(socket2)).rejects.toMatchObject({ code: "ENOENT" });
    await expect(readFile(`${socket2}.owner.json`, "utf8")).resolves.toBe(liveOwnerBytes);
  });

  it("coalesces lifecycle transitions and supports an authenticated same-instance restart", async () => {
    const root = await mkdtemp(join(tmpdir(), "ch-life-"));
    const { runtime, service } = await fixture(root);
    const socketPath = join(runtime, "control.sock");
    const daemon = new RuntimeDaemon({ runtimeDirectory: runtime, socketPath, service });
    active.push(daemon);

    const firstStart = daemon.start();
    await expect(daemon.start()).rejects.toThrow(/cannot start while starting/);
    const firstStarted = await firstStart;
    const firstToken = (await readFile(firstStarted.operatorTokenFile, "utf8")).trim();
    expect((await request(socketPath, "/v1/health", firstToken)).status).toBe(200);

    const firstStop = daemon.stop();
    const concurrentStop = daemon.stop();
    expect(concurrentStop).toBe(firstStop);
    await firstStop;
    expect(daemonLifecycle(daemon)).toBe("STOPPED");
    await expect(daemon.stop()).resolves.toBeUndefined();
    await expect(stat(socketPath)).rejects.toMatchObject({ code: "ENOENT" });
    await expect(stat(`${socketPath}.owner.json`)).rejects.toMatchObject({ code: "ENOENT" });

    const restarted = await daemon.start();
    const restartedToken = (await readFile(restarted.operatorTokenFile, "utf8")).trim();
    expect((await request(socketPath, "/v1/health", restartedToken)).status).toBe(200);
    await daemon.stop();
    expect(daemonLifecycle(daemon)).toBe("STOPPED");
  });

  it("closes completed keep-alive transport during a graceful stop without interruption", async () => {
    const root = await mkdtemp(join(tmpdir(), "ch-keepalive-"));
    const { runtime, service } = await fixture(root);
    const socketPath = join(runtime, "control.sock");
    const daemon = new RuntimeDaemon({ runtimeDirectory: runtime, socketPath, service });
    active.push(daemon);
    const started = await daemon.start();
    const token = (await readFile(started.operatorTokenFile, "utf8")).trim();
    const agent = new Agent({ keepAlive: true });
    const health = await new Promise<number>((resolve, reject) => {
      const outgoing = httpRequest(
        {
          socketPath,
          path: "/v1/health",
          headers: { authorization: `Bearer ${token}` },
          agent
        },
        (response) => {
          response.resume();
          response.once("end", () => resolve(response.statusCode ?? 0));
        }
      );
      outgoing.once("error", reject);
      outgoing.end();
    });
    expect(health).toBe(200);
    const began = performance.now();
    await daemon.stop();
    expect(performance.now() - began).toBeLessThan(1_500);
    expect(daemonLifecycle(daemon)).toBe("STOPPED");
    expect(Object.keys(agent.freeSockets)).toHaveLength(0);
    agent.destroy();
  });

  it("forces an incomplete ordinary request at the exact production grace and cleans metadata", async () => {
    const root = await mkdtemp(join(tmpdir(), "ch-force-"));
    const { runtime, service } = await fixture(root);
    const socketPath = join(runtime, "control.sock");
    const daemon = new RuntimeDaemon({ runtimeDirectory: runtime, socketPath, service });
    active.push(daemon);
    const started = await daemon.start();
    const token = (await readFile(started.operatorTokenFile, "utf8")).trim();
    const pending = await openIncompleteRequest(
      socketPath,
      "/v1/projects/register",
      token
    );
    await unlink(socketPath);

    const began = performance.now();
    const stopping = daemon.stop();
    await expect(daemon.start()).rejects.toThrow(/cannot start before shutdown has drained/);
    await new Promise((resolve) => setTimeout(resolve, 1_850));
    expect(daemonLifecycle(daemon)).toBe("STOPPING");
    await expect(stat(socketPath)).rejects.toMatchObject({ code: "ENOENT" });
    expect(JSON.parse(await readFile(`${socketPath}.owner.json`, "utf8"))).toMatchObject({
      daemonId: daemon.daemonId
    });
    await stopping;
    const elapsed = performance.now() - began;
    expect(elapsed).toBeGreaterThanOrEqual(1_950);
    expect(elapsed).toBeLessThan(2_600);
    await pending.disconnected;
    pending.outgoing.destroy();
    expect(daemonLifecycle(daemon)).toBe("STOPPED");
    await expect(stat(socketPath)).rejects.toMatchObject({ code: "ENOENT" });
    await expect(stat(`${socketPath}.owner.json`)).rejects.toMatchObject({ code: "ENOENT" });
  }, 5_000);

  it("interrupts a live SSE once after closing admission and drains it during grace", async () => {
    const root = await mkdtemp(join(tmpdir(), "ch-sse-"));
    const { runtime, service, engines, sessions } = await fixture(root);
    let release!: () => void;
    const held = new Promise<void>((resolve) => {
      release = resolve;
    });
    let interrupts = 0;
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
      subject: "stop-test",
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
        await held;
      },
      async interrupt() {
        interrupts += 1;
        release();
      }
    };
    engines.register(engine);
    const socketPath = join(runtime, "control.sock");
    const daemon = new RuntimeDaemon({ runtimeDirectory: runtime, socketPath, service });
    active.push(daemon);
    await daemon.start();
    const { manifestPath } = await createProjectFixture(join(root, "project"), "stop-project");
    const registered = await service.registerProject(manifestPath, "test", "D-STOP");
    const token = (await readFile(registered.tokenFile, "utf8")).trim();
    const session = await service.createSession({
      projectId: "stop-project",
      role: "agent1",
      engineSelection: {
        adapterId: "stub",
        providerId: "stub",
        model: "held"
      },
      persona: "WORKING_ITEMS"
    });
    const stream = await openStream(
      socketPath,
      `/v1/projects/stop-project/sessions/${session.sessionId}/turn`,
      token,
      { prompt: "hold" }
    );
    await stream.firstChunk;
    const began = performance.now();
    const stopping = daemon.stop();
    stream.outgoing.destroy();
    await stopping;
    expect(performance.now() - began).toBeLessThan(1_500);
    expect(interrupts).toBe(1);
    let events = await sessions.replay("stop-project", session.sessionId);
    for (let attempt = 0; attempt < 100; attempt += 1) {
      if (events.some((event) => event.type === "turn.interrupted")) break;
      await new Promise((resolve) => setTimeout(resolve, 10));
      events = await sessions.replay("stop-project", session.sessionId);
    }
    expect(events.filter((event) => event.type === "turn.interrupted")).toHaveLength(1);
  });

  it("forces stubborn SSE transport without waiting on interrupt acknowledgement and degrades", async () => {
    const root = await mkdtemp(join(tmpdir(), "ch-stubborn-"));
    const { runtime, service, engines } = await fixture(root);
    const never = new Promise<void>(() => undefined);
    let interrupts = 0;
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
      subject: "stubborn-test",
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
        await never;
      },
      async interrupt() {
        interrupts += 1;
        await never;
      }
    };
    engines.register(engine);
    const socketPath = join(runtime, "control.sock");
    const daemon = new RuntimeDaemon({ runtimeDirectory: runtime, socketPath, service });
    active.push(daemon);
    await daemon.start();
    const { manifestPath } = await createProjectFixture(join(root, "project"), "stubborn-project");
    const registered = await service.registerProject(manifestPath, "test", "D-STUBBORN");
    const token = (await readFile(registered.tokenFile, "utf8")).trim();
    const session = await service.createSession({
      projectId: "stubborn-project",
      role: "agent1",
      engineSelection: {
        adapterId: "stub",
        providerId: "stub",
        model: "held"
      },
      persona: "WORKING_ITEMS"
    });
    const stream = await openStream(
      socketPath,
      `/v1/projects/stubborn-project/sessions/${session.sessionId}/turn`,
      token,
      { prompt: "hold" }
    );
    await stream.firstChunk;
    const began = performance.now();
    await expect(daemon.stop()).rejects.toMatchObject({ code: "STOPPED_DEGRADED" });
    const elapsed = performance.now() - began;
    expect(elapsed).toBeGreaterThanOrEqual(1_950);
    expect(elapsed).toBeLessThan(2_600);
    expect(interrupts).toBe(1);
    expect(daemonLifecycle(daemon)).toBe("STOPPED_DEGRADED");
    await expect(daemon.start()).rejects.toThrow(/cannot start while stopped_degraded/);
    stream.outgoing.destroy();
  }, 5_000);

  it("expires pre-identity Agent 1 cancellation at force and forbids a late interrupt", async () => {
    const root = await mkdtemp(join(tmpdir(), "ch-preid-"));
    let runnerEntered!: () => void;
    const entered = new Promise<void>((resolve) => {
      runnerEntered = resolve;
    });
    let releaseIdentity!: () => void;
    const identityGate = new Promise<void>((resolve) => {
      releaseIdentity = resolve;
    });
    let interrupts = 0;
    const { runtime, service } = await fixture(root, {
      async *run(): AsyncIterable<UIEvent> {
        runnerEntered();
        await identityGate;
        yield {
          type: "harness:event",
          data: {
            schemaVersion: 1,
            eventId: "late-event",
            sessionId: "late-agent1",
            timestamp: new Date().toISOString(),
            type: "session.created",
            data: {}
          }
        };
      },
      async interrupt() {
        interrupts += 1;
      }
    });
    const socketPath = join(runtime, "control.sock");
    const daemon = new RuntimeDaemon({ runtimeDirectory: runtime, socketPath, service });
    active.push(daemon);
    await daemon.start();
    const { manifestPath } = await createProjectFixture(
      join(root, "project"),
      "preidentity-project"
    );
    const registered = await service.registerProject(manifestPath, "test", "D-PREIDENTITY");
    const token = (await readFile(registered.tokenFile, "utf8")).trim();
    const stream = await openStream(
      socketPath,
      "/v1/projects/preidentity-project/runs",
      token,
      { brief: "hold identity", approvalReference: "D-PREIDENTITY" }
    );
    void stream.firstChunk.catch(() => undefined);
    await entered;
    const began = performance.now();
    await expect(daemon.stop()).rejects.toMatchObject({
      code: "STOPPED_DEGRADED",
      message: expect.stringContaining("INTERRUPTION_IDENTITY_UNAVAILABLE")
    });
    expect(performance.now() - began).toBeGreaterThanOrEqual(1_950);
    releaseIdentity();
    await new Promise((resolve) => setTimeout(resolve, 50));
    expect(interrupts).toBe(0);
    stream.outgoing.destroy();
  }, 5_000);

  it("interrupts once when Agent 1 identity appears in a later pre-force event", async () => {
    const root = await mkdtemp(join(tmpdir(), "ch-later-preid-"));
    let releaseIdentity!: () => void;
    const identityGate = new Promise<void>((resolve) => {
      releaseIdentity = resolve;
    });
    let releaseRun!: () => void;
    const runGate = new Promise<void>((resolve) => {
      releaseRun = resolve;
    });
    let interrupts = 0;
    const { runtime, service } = await fixture(root, {
      async *run(): AsyncIterable<UIEvent> {
        yield { type: "chat:delta", data: { text: "pre-identity" } };
        await identityGate;
        yield {
          type: "harness:event",
          data: {
            schemaVersion: 1,
            eventId: "later-identity-event",
            sessionId: "later-manager-session",
            timestamp: new Date().toISOString(),
            type: "session.created",
            data: {}
          }
        };
        await runGate;
      },
      async interrupt() {
        interrupts += 1;
        releaseRun();
      }
    });
    const socketPath = join(runtime, "control.sock");
    const daemon = new RuntimeDaemon({ runtimeDirectory: runtime, socketPath, service });
    active.push(daemon);
    await daemon.start();
    const { manifestPath } = await createProjectFixture(
      join(root, "project"),
      "later-preidentity-project"
    );
    const registered = await service.registerProject(
      manifestPath,
      "test",
      "D-LATER-PREIDENTITY"
    );
    const token = (await readFile(registered.tokenFile, "utf8")).trim();
    const stream = await openStream(
      socketPath,
      "/v1/projects/later-preidentity-project/runs",
      token,
      { brief: "later identity", approvalReference: "D-LATER-PREIDENTITY" }
    );
    await stream.firstChunk;
    const stopping = daemon.stop();
    releaseIdentity();
    await stopping;
    expect(interrupts).toBe(1);
    expect(daemonLifecycle(daemon)).toBe("STOPPED");
    stream.outgoing.destroy();
  }, 5_000);

  it("isolates late prior-generation iterator events after a successful forced stop and restart", async () => {
    const root = await mkdtemp(join(tmpdir(), "ch-generation-"));
    const { runtime, service, engines } = await fixture(root);
    let releaseOld!: () => void;
    const oldGate = new Promise<void>((resolve) => {
      releaseOld = resolve;
    });
    let interrupts = 0;
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
      subject: "generation-test",
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
        await oldGate;
      },
      async interrupt() {
        interrupts += 1;
      }
    };
    engines.register(engine);
    const socketPath = join(runtime, "control.sock");
    const daemon = new RuntimeDaemon({ runtimeDirectory: runtime, socketPath, service });
    active.push(daemon);
    await daemon.start();
    const { manifestPath } = await createProjectFixture(join(root, "project"), "generation-project");
    const registered = await service.registerProject(manifestPath, "test", "D-GENERATION");
    const projectToken = (await readFile(registered.tokenFile, "utf8")).trim();
    const session = await service.createSession({
      projectId: "generation-project",
      role: "agent1",
      engineSelection: { adapterId: "stub", providerId: "stub", model: "held" },
      persona: "WORKING_ITEMS"
    });
    const stream = await openStream(
      socketPath,
      `/v1/projects/generation-project/sessions/${session.sessionId}/turn`,
      projectToken,
      { prompt: "hold old generation" }
    );
    await stream.firstChunk;
    await daemon.stop();
    expect(interrupts).toBe(1);
    expect(daemonLifecycle(daemon)).toBe("STOPPED");

    const restarted = await daemon.start();
    const ownerBeforeLate = await readFile(`${socketPath}.owner.json`, "utf8");
    const operator = (await readFile(restarted.operatorTokenFile, "utf8")).trim();
    releaseOld();
    await new Promise((resolve) => setTimeout(resolve, 50));
    expect(await readFile(`${socketPath}.owner.json`, "utf8")).toBe(ownerBeforeLate);
    expect((await request(socketPath, "/v1/health", operator)).status).toBe(200);
    expect(interrupts).toBe(1);
    stream.outgoing.destroy();
    await daemon.stop();
  }, 6_000);

  it("caps post-force transport settlement at 500 ms before reporting cleanup failure", async () => {
    const root = await mkdtemp(join(tmpdir(), "ch-settle-"));
    const { runtime, service } = await fixture(root);
    const socketPath = join(runtime, "control.sock");
    const daemon = new RuntimeDaemon({ runtimeDirectory: runtime, socketPath, service });
    active.push(daemon);
    await daemon.start();
    const internal = daemon as unknown as {
      generation: { sockets: Set<{ destroy(): void }> };
    };
    const residual = { destroy(): void {} };
    internal.generation.sockets.add(residual);
    const began = performance.now();
    await expect(daemon.stop()).rejects.toMatchObject({ code: "STOP_FAILED_CLEANUP" });
    const elapsed = performance.now() - began;
    expect(elapsed).toBeGreaterThanOrEqual(2_450);
    expect(elapsed).toBeLessThan(2_800);
    internal.generation.sockets.delete(residual);
    await daemon.stop();
    expect(daemonLifecycle(daemon)).toBe("STOPPED");
  }, 6_000);

  it("retries only incomplete cleanup and never removes a foreign owner record", async () => {
    const root = await mkdtemp(join(tmpdir(), "ch-retry-"));
    const { runtime, service } = await fixture(root);
    const socketPath = join(runtime, "control.sock");
    const daemon = new RuntimeDaemon({ runtimeDirectory: runtime, socketPath, service });
    active.push(daemon);
    await daemon.start();
    const internals = daemon as unknown as {
      unlinkControlSocket(): Promise<void>;
    };
    const originalUnlink = internals.unlinkControlSocket.bind(daemon);
    let attempts = 0;
    internals.unlinkControlSocket = async () => {
      attempts += 1;
      if (attempts === 1) throw new Error("injected unlink failure");
      await originalUnlink();
    };
    await expect(daemon.stop()).rejects.toMatchObject({ code: "STOP_FAILED_CLEANUP" });
    expect(daemonLifecycle(daemon)).toBe("STOP_FAILED_CLEANUP");
    await expect(daemon.start()).rejects.toThrow(/cannot start while stop_failed_cleanup/);
    await daemon.stop();
    expect(attempts).toBe(2);
    expect(daemonLifecycle(daemon)).toBe("STOPPED");

    const root2 = await mkdtemp(join(tmpdir(), "ch-foreign-"));
    const second = await fixture(root2);
    const socket2 = join(second.runtime, "control.sock");
    const daemon2 = new RuntimeDaemon({
      runtimeDirectory: second.runtime,
      socketPath: socket2,
      service: second.service
    });
    active.push(daemon2);
    await daemon2.start();
    await atomicWriteJson(`${socket2}.owner.json`, {
      schemaVersion: "chirality.daemon-owner/v1",
      daemonId: "foreign-daemon",
      generationId: "foreign-generation",
      pid: process.pid,
      uid: process.getuid?.() ?? -1,
      socketPath: socket2,
      startedAt: new Date().toISOString()
    });
    await chmod(`${socket2}.owner.json`, 0o600);
    await daemon2.stop();
    expect(JSON.parse(await readFile(`${socket2}.owner.json`, "utf8"))).toMatchObject({
      daemonId: "foreign-daemon",
      generationId: "foreign-generation"
    });
  });
});
