import { chmod, mkdtemp, realpath, rm, writeFile } from "node:fs/promises";
import { createServer, type IncomingMessage, type ServerResponse } from "node:http";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { afterEach, describe, expect, it } from "vitest";
import type { RuntimeSessionRecord } from "@chirality/runtime-contracts";
import { RuntimeClient, RuntimeTransportError, parseUiEvent } from "../src/index.js";

type RequestHandler = (
  request: IncomingMessage,
  response: ServerResponse
) => void | Promise<void>;

const temporaryDirectories: string[] = [];

async function fixture(handler: RequestHandler): Promise<{
  client: RuntimeClient;
  close(): Promise<void>;
  requests: IncomingMessage[];
  root: string;
}> {
  const root = await mkdtemp(join(tmpdir(), "chirality-runtime-client-"));
  temporaryDirectories.push(root);
  const socketPath = join(root, "control.sock");
  const tokenFile = join(root, "operator.token");
  await writeFile(tokenFile, "test-runtime-token\n", { mode: 0o600 });
  await chmod(tokenFile, 0o600);
  const requests: IncomingMessage[] = [];
  const server = createServer((request, response) => {
    requests.push(request);
    void handler(request, response);
  });
  await new Promise<void>((resolve, reject) => {
    server.once("error", reject);
    server.listen(socketPath, resolve);
  });
  return {
    root,
    requests,
    client: new RuntimeClient({ socketPath, tokenFile, timeoutMs: 2_000 }),
    close: () =>
      new Promise<void>((resolve, reject) => {
        server.close((error) => (error === undefined ? resolve() : reject(error)));
      })
  };
}

function json(response: ServerResponse, status: number, value: unknown): void {
  response.writeHead(status, { "content-type": "application/json" });
  response.end(JSON.stringify(value));
}

function session(projectId: string, sessionId: string): RuntimeSessionRecord {
  return {
    schemaVersion: "chirality.session/v2",
    projectId,
    projectRoot: `/projects/${projectId}`,
    sessionId,
    persona: "WORKING_ITEMS",
    mode: "direct",
    createdAt: "2026-07-22T00:00:00.000Z",
    updatedAt: "2026-07-22T00:00:00.000Z",
    role: "agent1",
    engineSelection: {
      adapterId: "claude-agent-sdk",
      providerId: "anthropic",
      model: "test-model"
    },
    status: "idle"
  };
}

afterEach(async () => {
  await Promise.all(
    temporaryDirectories.splice(0).map((directory) =>
      rm(directory, { recursive: true, force: true })
    )
  );
});

describe("RuntimeClient Unix-socket transport", () => {
  it("uses the token file and exact response envelopes without a TCP fallback", async () => {
    const project = {
      projectId: "project-a",
      displayName: "Project A",
      canonicalRoot: "/projects/project-a",
      manifestPath: "/projects/project-a/chirality.project.json",
      manifestHash: "abc",
      registeredAt: "2026-07-22T00:00:00.000Z",
      approval: { approvedBy: "owner", approvalReference: "D-GOV-20" },
      clientId: "project-project-a",
      enabledAdapterIds: ["claude-agent-sdk"],
      legacySessionRoots: []
    };
    const projectStatus = {
      project,
      manifestDrift: false,
      adaptersEnabled: true
    };
    const testSession = session("project-a", "sess-a");
    const server = await fixture((request, response) => {
      expect(request.headers.authorization).toBe("Bearer test-runtime-token");
      if (request.url === "/v1/projects") {
        return json(response, 200, { projects: [projectStatus] });
      }
      if (request.url === "/v1/projects/project-a/sessions/sess-a") {
        return json(response, 200, { session: testSession });
      }
      if (request.url === "/v1/projects/project-a/sessions/sess-a/boot") {
        return json(response, 200, {
          session: testSession,
          boot: {
            engineSessionId: "engine-a",
            adapterId: "claude-agent-sdk",
            providerId: "anthropic",
            model: "test-model",
            bootFingerprint: "fingerprint",
            runtimeFingerprint: {
              schemaVersion: "v2",
              personaComposerVersion: "v1",
              permissionPolicyVersion: "v1",
              managedDelegationPolicyVersion: "v1",
              subagentPolicyVersion: "v1",
              toolRegistryVersion: "v1",
              sdkPackageVersion: "1",
              mcpServers: [],
              fingerprintSha256: "hash"
            },
            bootedAt: "2026-07-22T00:00:01.000Z"
          }
        });
      }
      return json(response, 404, {
        error: { code: "NOT_FOUND", message: "not found" }
      });
    });

    expect(await server.client.listProjects()).toEqual([projectStatus]);
    expect(await server.client.getSession("project-a", "sess-a")).toEqual(testSession);
    expect((await server.client.bootSession("project-a", "sess-a")).boot).toMatchObject({
      engineSessionId: "engine-a",
      model: "test-model"
    });
    expect(server.requests.every((request) => request.socket.remoteAddress === undefined)).toBe(true);
    await server.close();
  });

  it("resolves project roots and session ownership through authorized project queries", async () => {
    const root = await mkdtemp(join(tmpdir(), "chirality-project-root-"));
    temporaryDirectories.push(root);
    const canonicalRoot = await realpath(root);
    const statuses = ["one", "two"].map((projectId) => ({
      project: {
        projectId,
        displayName: projectId,
        canonicalRoot: projectId === "two" ? canonicalRoot : `/projects/${projectId}`,
        manifestPath: `/projects/${projectId}/chirality.project.json`,
        manifestHash: projectId,
        registeredAt: "2026-07-22T00:00:00.000Z",
        approval: { approvedBy: "owner", approvalReference: "approval" },
        clientId: `client-${projectId}`,
        enabledAdapterIds: [],
        legacySessionRoots: []
      },
      manifestDrift: false,
      adaptersEnabled: true
    }));
    const server = await fixture((request, response) => {
      if (request.url === "/v1/projects") {
        return json(response, 200, { projects: statuses });
      }
      if (request.url === "/v1/projects/one/sessions/target") {
        return json(response, 404, {
          error: { code: "SESSION_NOT_FOUND", message: "missing" }
        });
      }
      if (request.url === "/v1/projects/two/sessions/target") {
        return json(response, 200, { session: session("two", "target") });
      }
      return json(response, 404, {
        error: { code: "NOT_FOUND", message: "not found" }
      });
    });

    expect((await server.client.resolveProjectByRoot(root)).projectId).toBe("two");
    expect((await server.client.resolveSessionOwner("target")).project.projectId).toBe("two");
    await server.close();
  });

  it("parses UIEvent SSE frames and cancellation closes the Unix-socket stream", async () => {
    let closedResolve: (() => void) | undefined;
    const closed = new Promise<void>((resolve) => {
      closedResolve = resolve;
    });
    const server = await fixture((request, response) => {
      if (request.url !== "/v1/projects/project-a/sessions/sess-a/turn") {
        return json(response, 404, {
          error: { code: "NOT_FOUND", message: "not found" }
        });
      }
      request.once("close", () => closedResolve?.());
      response.writeHead(200, { "content-type": "text/event-stream" });
      response.write('event: chat:delta\ndata: {"text":"hello"}\n\n');
    });
    const stream = await server.client.turnSession("project-a", "sess-a", {
      prompt: "test"
    });
    const iterator = stream[Symbol.asyncIterator]();

    await expect(iterator.next()).resolves.toEqual({
      done: false,
      value: { type: "chat:delta", data: { text: "hello" } }
    });
    stream.cancel();
    await closed;
    await server.close();
  });

  it("returns typed runtime errors and rejects malformed tokens before transport", async () => {
    const server = await fixture((_request, response) => {
      json(response, 409, {
        error: {
          code: "PROJECT_MANIFEST_DRIFT",
          message: "re-register",
          details: { projectId: "project-a" }
        }
      });
    });
    await expect(server.client.projectStatus("project-a")).rejects.toMatchObject({
      code: "PROJECT_MANIFEST_DRIFT",
      status: 409,
      details: { projectId: "project-a" }
    });
    await server.close();

    const root = await mkdtemp(join(tmpdir(), "chirality-invalid-token-"));
    temporaryDirectories.push(root);
    const tokenFile = join(root, "token");
    await writeFile(tokenFile, "not a bearer token\n");
    const client = new RuntimeClient({
      socketPath: join(root, "missing.sock"),
      tokenFile
    });
    await expect(client.health()).rejects.toBeInstanceOf(RuntimeTransportError);
  });
});

it("keeps boot waiting past the generic JSON deadline and labels transport failures", async () => {
  const server = await fixture(async (_request, response) => {
    await new Promise(resolve => setTimeout(resolve, 40));
    json(response, 200, { boot: { engineSessionId: "actual-boot" } });
  });
  const client = new RuntimeClient({ socketPath: join(server.root, "control.sock"), tokenFile: join(server.root, "operator.token"), timeoutMs: 10 });
  try {
    await expect(client.requestJson("/slow")).rejects.toMatchObject({ reason: "timeout" });
    await expect(client.bootSession("project-a", "sess-a")).resolves.toMatchObject({ boot: { engineSessionId: "actual-boot" } });
    const controller = new AbortController(); controller.abort();
    await expect(client.bootSession("project-a", "sess-a", {}, controller.signal)).rejects.toMatchObject({ reason: "transport", operation: "boot", sessionId: "sess-a" });
  } finally { await server.close(); }
});

describe("RuntimeClient turn ownership transport (D-GOV-43)", () => {
  it("no longer carries the retired v2 delegated, hosted-login, consent, preflight or approval surface", () => {
    const retired = [
      "startHostedLogin", "hostedLoginStatus", "cancelHostedLogin",
      "runDelegatedTurn", "interruptDelegatedTurn", "delegatedCapabilities", "delegatedPreflight",
      "grantDelegatedConsent", "pendingDelegatedApprovals", "decideDelegatedApproval",
      "pendingRuntimeApprovals", "decideRuntimeApproval"
    ];
    const surface = Object.getOwnPropertyNames(RuntimeClient.prototype);
    expect(retired.filter((name) => surface.includes(name))).toEqual([]);
    for (const kept of ["hostedBootstrapStatus", "startHostedBootstrapLogin", "cancelHostedBootstrapLogin", "signOutHostedProject", "grantHostedProviderNetworkConsent", "attachSessionTurn", "sessionTurnState", "listSessionRequests", "answerSessionRequest", "decidePermission"]) {
      expect(surface).toContain(kept);
    }
  });

  it("parses any named SSE event, surfaces the wire id as seq, and rejects nameless frames", () => {
    expect(parseUiEvent({ event: "harness:event", data: '{"type":"codex.notification"}', id: "7", seq: 7 })).toEqual({ type: "harness:event", data: { type: "codex.notification" }, seq: 7 });
    expect(parseUiEvent({ event: "vendor:unknown", data: "{}" })).toEqual({ type: "vendor:unknown", data: {} });
    expect(() => parseUiEvent({ data: "{}" })).toThrow(expect.objectContaining({ code: "INTERNAL_FAILURE" }));
    expect(() => parseUiEvent({ event: "chat:delta", data: "[]" })).toThrow(expect.objectContaining({ code: "INTERNAL_FAILURE" }));
  });

  it("attaches to a Runtime-owned turn with after=, keeps the stream open past the JSON idle timeout, and cancel only unsubscribes", async () => {
    let closedResolve: (() => void) | undefined;
    const closed = new Promise<void>((resolve) => { closedResolve = resolve; });
    const seen: string[] = [];
    const server = await fixture(async (request, response) => {
      seen.push(`${request.method} ${request.url}`);
      if (request.url === "/v1/projects/project-a/sessions/sess-a/turn/stream?after=3&turnId=turn%2F1") {
        request.once("close", () => closedResolve?.());
        // Silence longer than the client's JSON idle timeout must not end a turn subscription.
        await new Promise((resolve) => setTimeout(resolve, 40));
        response.writeHead(200, { "content-type": "text/event-stream" });
        response.write(": keepalive\n\n");
        response.write('id: 4\nevent: chat:delta\ndata: {"text":"late"}\n\n');
        return;
      }
      return json(response, 404, { error: { code: "NOT_FOUND", message: "not found" } });
    });
    const client = new RuntimeClient({ socketPath: join(server.root, "control.sock"), tokenFile: join(server.root, "operator.token"), timeoutMs: 10 });
    const stream = await client.attachSessionTurn("project-a", "sess-a", { after: 3, turnId: "turn/1" });
    const iterator = stream[Symbol.asyncIterator]();
    await expect(iterator.next()).resolves.toEqual({ done: false, value: { type: "chat:delta", data: { text: "late" }, seq: 4 } });
    stream.cancel();
    await closed;
    expect(seen).toEqual(["GET /v1/projects/project-a/sessions/sess-a/turn/stream?after=3&turnId=turn%2F1"]);
    expect(() => client.attachSessionTurn("project-a", "sess-a", { after: -1 })).toThrow(expect.objectContaining({ code: "INVALID_REQUEST" }));
    await server.close();
  });

  it("reads turn state, lists pending server requests, answers one, and passes per-turn model and effort through", async () => {
    const bodies: { url: string; body: unknown }[] = [];
    const server = await fixture(async (request, response) => {
      const chunks: Buffer[] = [];
      for await (const chunk of request) chunks.push(Buffer.from(chunk));
      const body = chunks.length === 0 ? undefined : JSON.parse(Buffer.concat(chunks).toString("utf8"));
      bodies.push({ url: `${request.method} ${request.url}`, body });
      if (request.url === "/v1/projects/project-a/sessions/sess-a/turn/state") return json(response, 200, { active: true, turnId: "t-1", lastSeq: 9, startedAt: "2026-09-12T00:00:00.000Z" });
      if (request.url === "/v1/projects/project-a/sessions/sess-a/requests") return json(response, 200, { requests: [{ requestId: "42", method: "item/commandExecution/requestApproval", params: { itemId: "item-1" }, itemId: "item-1", receivedAt: "2026-09-12T00:00:01.000Z" }] });
      if (request.url === "/v1/projects/project-a/sessions/sess-a/requests/42/answer") return json(response, 200, { sent: true });
      if (request.url === "/v1/projects/project-a/sessions/sess-a/turn") {
        response.writeHead(200, { "content-type": "text/event-stream" });
        response.end('id: 1\nevent: process:exit\ndata: {"exitCode":0}\n\n');
        return;
      }
      return json(response, 404, { error: { code: "NOT_FOUND", message: "not found" } });
    });
    try {
      expect(await server.client.sessionTurnState("project-a", "sess-a")).toEqual({ active: true, turnId: "t-1", lastSeq: 9, startedAt: "2026-09-12T00:00:00.000Z" });
      expect((await server.client.listSessionRequests("project-a", "sess-a")).requests[0]).toMatchObject({ requestId: "42", itemId: "item-1" });
      expect(await server.client.answerSessionRequest("project-a", "sess-a", "42", { kind: "approval", verdict: "deny" })).toEqual({ sent: true });
      const stream = await server.client.turnSession("project-a", "sess-a", { message: "go", model: "gpt-alt", reasoningEffort: "high" });
      const frames = [];
      for await (const frame of stream) frames.push(frame);
      expect(frames).toEqual([{ type: "process:exit", data: { exitCode: 0 }, seq: 1 }]);
      expect(bodies.find((entry) => entry.url.endsWith("/requests/42/answer"))?.body).toEqual({ answer: { kind: "approval", verdict: "deny" } });
      expect(bodies.find((entry) => entry.url === "POST /v1/projects/project-a/sessions/sess-a/turn")?.body).toEqual({ message: "go", model: "gpt-alt", reasoningEffort: "high" });
    } finally { await server.close(); }
  });
});

it("bounds stream opening separately from JSON timeout without sending an interrupt", async () => {
  const server = await fixture(() => {});
  const client = new RuntimeClient({ socketPath: join(server.root, "control.sock"), tokenFile: join(server.root, "operator.token"), streamTransportTimeoutMs: 80 });
  try {
    await expect(client.attachSessionTurn("project-a", "sess-a", { after: 4 })).rejects.toMatchObject({ reason: "timeout" });
    expect(server.requests.map(request => request.url)).toEqual(["/v1/projects/project-a/sessions/sess-a/turn/stream?after=4"]);
  } finally { await server.close(); }
});

it("keeps heartbeat-only observations healthy, then expires missing bytes without interrupting", async () => {
  let stopHeartbeat!: () => void;
  const server = await fixture((_request, response) => {
    response.writeHead(200, { "content-type": "text/event-stream" });
    response.flushHeaders();
    const timer = setInterval(() => response.write(": keepalive\n\n"), 25);
    stopHeartbeat = () => clearInterval(timer);
    response.once("close", stopHeartbeat);
  });
  const client = new RuntimeClient({ socketPath: join(server.root, "control.sock"), tokenFile: join(server.root, "operator.token"), timeoutMs: 10, streamTransportTimeoutMs: 150 });
  try {
    const stream = await client.attachSessionTurn("project-a", "sess-a", { after: 4 });
    let ended = false;
    const pending = stream[Symbol.asyncIterator]().next();
    const rejected = expect(pending).rejects.toBeInstanceOf(Error);
    void pending.then(() => { ended = true; }, () => { ended = true; });
    await new Promise(resolve => setTimeout(resolve, 400));
    expect(ended).toBe(false);
    stopHeartbeat();
    await rejected;
    expect(server.requests.map(request => request.method)).toEqual(["GET"]);
  } finally { stopHeartbeat?.(); await server.close(); }
});
