import { chmod, mkdtemp, realpath, rm, writeFile } from "node:fs/promises";
import { createServer, type IncomingMessage, type ServerResponse } from "node:http";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { afterEach, describe, expect, it } from "vitest";
import type { RuntimeSessionRecord } from "@chirality/runtime-contracts";
import { RuntimeClient, RuntimeTransportError } from "../src/index.js";

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
