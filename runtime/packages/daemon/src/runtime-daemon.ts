import { randomUUID } from "node:crypto";
import { chmod, lstat, readFile, unlink } from "node:fs/promises";
import { createServer, type IncomingMessage, type Server, type ServerResponse } from "node:http";
import { dirname } from "node:path";
import {
  HarnessError,
  RUNTIME_API_VERSION,
  RuntimeError,
  deriveTranscriptView,
  type Agent1RunRequest,
  type CreateSessionRequest,
  type CredentialMutationRequest,
  type DaemonStatusResponse,
  type HealthResponse,
  type PermissionDecisionRequest,
  type ProjectRegistrationRequest,
  type RuntimeErrorBody,
  type ScaffoldRequest,
  type RuntimeSessionBootRequest,
  type SessionTurnRequest,
  type UIEvent
} from "@chirality/runtime-contracts";
import {
  ensurePrivateDirectory,
  atomicWriteJson,
  type AuthRegistry,
  type RuntimeScope,
  type RuntimeService
} from "@chirality/runtime-core";

const JSON_LIMIT_BYTES = 1024 * 1024;

export interface RuntimeDaemonOptions {
  socketPath: string;
  runtimeDirectory: string;
  service: RuntimeService;
}

export class RuntimeDaemon {
  readonly daemonId = randomUUID();
  readonly startedAt = new Date().toISOString();
  private server?: Server;
  private readonly ownerFile: string;

  constructor(private readonly options: RuntimeDaemonOptions) {
    this.ownerFile = `${options.socketPath}.owner.json`;
  }

  async start(): Promise<{ socketPath: string; operatorTokenFile: string }> {
    if (this.server !== undefined) throw new Error("Runtime daemon is already started");
    await ensurePrivateDirectory(this.options.runtimeDirectory);
    await ensurePrivateDirectory(dirname(this.options.socketPath));
    await this.recoverStaleSocket();
    await atomicWriteJson(this.ownerFile, {
      schemaVersion: "chirality.daemon-owner/v1",
      daemonId: this.daemonId,
      pid: process.pid,
      uid: process.getuid?.() ?? -1,
      socketPath: this.options.socketPath,
      startedAt: this.startedAt
    });
    const operator = await this.options.service.auth.ensureClient("operator", [
      "runtime:read",
      "projects:write",
      "sessions:read",
      "sessions:write",
      "models:read",
      "models:write",
      "credentials:read",
      "credentials:write"
    ]);
    const server = createServer((request, response) => {
      void this.route(request, response).catch((error) => this.error(response, error));
    });
    this.server = server;
    await new Promise<void>((resolve, reject) => {
      server.once("error", (error) => {
        void unlink(this.ownerFile).catch(() => undefined);
        reject(error);
      });
      server.listen(this.options.socketPath, () => {
        server.off("error", reject);
        resolve();
      });
    });
    await chmod(this.options.socketPath, 0o600);
    return { socketPath: this.options.socketPath, operatorTokenFile: operator.tokenFile };
  }

  async stop(): Promise<void> {
    const server = this.server;
    this.server = undefined;
    if (server !== undefined) {
      await new Promise<void>((resolve, reject) => {
        server.close((error) => (error === undefined ? resolve() : reject(error)));
      });
    }
    await unlink(this.options.socketPath).catch((error: NodeJS.ErrnoException) => {
      if (error.code !== "ENOENT") throw error;
    });
    await this.removeOwnedRecord();
  }

  private async route(request: IncomingMessage, response: ServerResponse): Promise<void> {
    try {
      const url = new URL(request.url ?? "/", "http://chirality.invalid");
      const method = request.method ?? "GET";
      const segments = url.pathname.split("/").filter(Boolean).map(decodeURIComponent);
      if (segments[0] !== "v1") throw new RuntimeError("NOT_FOUND", "Route not found", 404);

      if (method === "GET" && url.pathname === "/v1/health") {
        await this.authorize(request, "runtime:read");
        return this.json(response, 200, this.health());
      }
      if (method === "GET" && url.pathname === "/v1/daemon/status") {
        await this.authorize(request, "runtime:read");
        const body: DaemonStatusResponse = {
          ...this.health(),
          startedAt: this.startedAt,
          socketPath: this.options.socketPath,
          engines: this.options.service.engines.descriptors()
        };
        return this.json(response, 200, body);
      }
      if (method === "GET" && url.pathname === "/v1/projects") {
        const principal = await this.authorize(request, "runtime:read");
        const projects =
          principal.projectId === undefined
            ? await this.options.service.projects.list()
            : [await this.options.service.projects.status(principal.projectId)];
        return this.json(response, 200, { projects });
      }
      if (method === "POST" && url.pathname === "/v1/projects/register") {
        await this.authorize(request, "projects:write");
        const body = await this.body<ProjectRegistrationRequest>(request);
        return this.json(
          response,
          201,
          await this.options.service.registerProject(
            body.manifestPath,
            body.approvedBy,
            body.approvalReference
          )
        );
      }
      if (segments[1] === "credentials" && typeof segments[2] === "string") {
        const providerId = segments[2];
        if (method === "GET") {
          await this.authorize(request, "credentials:read");
          return this.json(response, 200, {
            providerId,
            ...(await this.options.service.credentials.status(providerId))
          });
        }
        if (method === "PUT") {
          await this.authorize(request, "credentials:write");
          const body = await this.body<CredentialMutationRequest>(request);
          if (body.credential.trim() === "") {
            throw new RuntimeError("INVALID_REQUEST", "Credential cannot be empty");
          }
          await this.options.service.credentials.set(providerId, body.credential);
          return this.json(response, 200, { providerId, configured: true });
        }
        if (method === "DELETE") {
          await this.authorize(request, "credentials:write");
          await this.options.service.credentials.remove(providerId);
          return this.json(response, 200, { providerId, configured: false });
        }
      }
      if (segments[1] === "models") {
        if (segments.length === 2 && method === "GET") {
          await this.authorize(request, "models:read");
          return this.json(response, 200, {
            residency: await this.options.service.residency.status()
          });
        }
        if (segments.length === 4 && segments[3] === "activate" && method === "POST") {
          await this.authorize(request, "models:write");
          const body = await this.body<{ approvalReference: string }>(request);
          return this.json(response, 200, {
            residency: await this.options.service.residency.activate(
              segments[2] ?? "",
              body.approvalReference
            )
          });
        }
      }
      if (segments[1] === "projects" && typeof segments[2] === "string") {
        const projectId = segments[2];
        if (segments.length === 4 && segments[3] === "status" && method === "GET") {
          await this.authorize(request, "runtime:read", projectId);
          return this.json(response, 200, await this.options.service.projects.status(projectId));
        }
        if (segments.length === 4 && segments[3] === "agents" && method === "GET") {
          await this.authorize(request, "sessions:read", projectId);
          return this.json(response, 200, {
            agents: await this.options.service.listAgents(
              projectId,
              url.searchParams.get("directChat") === "1"
            )
          });
        }
        if (segments.length === 4 && segments[3] === "scaffold" && method === "POST") {
          await this.authorize(request, "sessions:write", projectId);
          const body = await this.body<ScaffoldRequest>(request);
          return this.json(response, 200, {
            scaffold: await this.options.service.scaffold(projectId, body)
          });
        }
        if (segments.length === 4 && segments[3] === "runs" && method === "POST") {
          await this.authorize(request, "sessions:write", projectId);
          const body = await this.body<Agent1RunRequest>(request);
          let managerSessionId: string | undefined;
          const source = this.options.service.runAgent1(projectId, body);
          const tracked = (async function* (): AsyncIterable<UIEvent> {
            for await (const event of source) {
              if (managerSessionId === undefined && event.type === "harness:event") {
                managerSessionId = event.data.sessionId;
              }
              yield event;
            }
          })();
          return await this.sse(
            response,
            tracked,
            async () => {
              if (managerSessionId !== undefined) {
                await this.options.service.interruptSession(projectId, managerSessionId);
              }
            }
          );
        }
        if (segments[3] === "sessions") {
          return await this.sessionRoute(request, response, method, projectId, segments);
        }
      }
      throw new RuntimeError("NOT_FOUND", "Route not found", 404);
    } catch (error) {
      this.error(response, error);
    }
  }

  private async sessionRoute(
    request: IncomingMessage,
    response: ServerResponse,
    method: string,
    projectId: string,
    segments: string[]
  ): Promise<void> {
    if (segments.length === 4) {
      if (method === "GET") {
        await this.authorize(request, "sessions:read", projectId);
        return this.json(response, 200, {
          sessions: await this.options.service.sessions.list(projectId)
        });
      }
      if (method === "POST") {
        await this.authorize(request, "sessions:write", projectId);
        const body = await this.body<Omit<CreateSessionRequest, "projectId">>(request);
        return this.json(response, 201, {
          session: await this.options.service.createSession({ ...body, projectId })
        });
      }
    }
    const sessionId = segments[4];
    if (sessionId === undefined) throw new RuntimeError("NOT_FOUND", "Route not found", 404);
    if (segments.length === 5) {
      if (method === "GET") {
        await this.authorize(request, "sessions:read", projectId);
        return this.json(response, 200, {
          session: await this.options.service.sessions.get(projectId, sessionId)
        });
      }
      if (method === "DELETE") {
        await this.authorize(request, "sessions:write", projectId);
        await this.options.service.sessions.delete(projectId, sessionId);
        return this.json(response, 200, { deleted: true, sessionId });
      }
    }
    if (segments.length !== 6) throw new RuntimeError("NOT_FOUND", "Route not found", 404);
    const action = segments[5];
    if (action === "boot" && method === "POST") {
      await this.authorize(request, "sessions:write", projectId);
      const body = await this.body<RuntimeSessionBootRequest>(request);
      return this.json(
        response,
        200,
        await this.options.service.bootSession(
          projectId,
          sessionId,
          body.opts,
          body.expectedSelection
        )
      );
    }
    if (action === "replay" && method === "GET") {
      await this.authorize(request, "sessions:read", projectId);
      const session = await this.options.service.sessions.get(projectId, sessionId);
      const replay = await this.options.service.sessions.replayDetailed(projectId, sessionId);
      return this.json(response, 200, {
        session,
        ...replay,
        transcript: deriveTranscriptView(replay.events, session)
      });
    }
    if (action === "turn" && method === "POST") {
      await this.authorize(request, "sessions:write", projectId);
      const body = await this.body<SessionTurnRequest>(request);
      return await this.sse(
        response,
        this.options.service.runSessionTurn(projectId, sessionId, body),
        () => this.options.service.interruptSession(projectId, sessionId)
      );
    }
    if (action === "interrupt" && method === "POST") {
      await this.authorize(request, "sessions:write", projectId);
      await this.options.service.interruptSession(projectId, sessionId);
      return this.json(response, 200, { interrupted: true, sessionId });
    }
    if (action === "permission" && method === "POST") {
      await this.authorize(request, "sessions:write", projectId);
      await this.options.service.sessions.get(projectId, sessionId);
      const body = await this.body<PermissionDecisionRequest>(request);
      await this.options.service.decidePermission(projectId, sessionId, body);
      return this.json(response, 200, {
        accepted: true,
        requestId: body.requestId,
        decision: body.decision
      });
    }
    throw new RuntimeError("NOT_FOUND", "Route not found", 404);
  }

  private health(): HealthResponse {
    return {
      apiVersion: RUNTIME_API_VERSION,
      status: "ok",
      daemonId: this.daemonId,
      pid: process.pid
    };
  }

  private authorize(
    request: IncomingMessage,
    scope: RuntimeScope,
    projectId?: string
  ) {
    const value = Array.isArray(request.headers.authorization)
      ? request.headers.authorization[0]
      : request.headers.authorization;
    return this.options.service.auth.authenticate(value, scope, projectId);
  }

  private async body<T>(request: IncomingMessage): Promise<T> {
    const chunks: Buffer[] = [];
    let total = 0;
    for await (const chunk of request) {
      const buffer = Buffer.isBuffer(chunk) ? chunk : Buffer.from(chunk);
      total += buffer.length;
      if (total > JSON_LIMIT_BYTES) {
        throw new RuntimeError("INVALID_REQUEST", "Request body is too large", 413);
      }
      chunks.push(buffer);
    }
    try {
      return JSON.parse(Buffer.concat(chunks).toString("utf8")) as T;
    } catch {
      throw new RuntimeError("INVALID_REQUEST", "Request body must be valid JSON");
    }
  }

  private async discardOptionalBody(request: IncomingMessage): Promise<void> {
    for await (const _chunk of request) {
      // Drain the stream without interpreting unused compatibility input.
    }
  }

  private json(response: ServerResponse, status: number, value: unknown): void {
    if (response.headersSent) return;
    const body = JSON.stringify(value);
    response.writeHead(status, {
      "content-type": "application/json; charset=utf-8",
      "content-length": Buffer.byteLength(body)
    });
    response.end(body);
  }

  private async sse(
    response: ServerResponse,
    events: AsyncIterable<UIEvent>,
    onDisconnect?: () => Promise<void>
  ): Promise<void> {
    const iterator = events[Symbol.asyncIterator]();
    let finished = false;
    let streamStarted = false;
    let disconnected = response.destroyed;
    const disconnectTasks: Promise<void>[] = [];
    const notifyDisconnect = (): void => {
      if (onDisconnect === undefined) return;
      disconnectTasks.push(onDisconnect().catch(() => undefined));
    };
    const close = (): void => {
      if (finished) return;
      disconnected = true;
      notifyDisconnect();
    };
    response.once("close", close);
    try {
      const first = await iterator.next();
      streamStarted = true;
      if (response.destroyed && !disconnected) disconnected = true;
      if (disconnected) {
        // A run stream may not know its manager session until the first event.
        // Retry the idempotent interrupt after that identity has been captured.
        notifyDisconnect();
      } else {
        response.writeHead(200, {
          "content-type": "text/event-stream",
          "cache-control": "no-cache, no-transform",
          connection: "keep-alive",
          "x-accel-buffering": "no"
        });
      }
      if (!first.done && !disconnected) {
        response.write(
          `event: ${first.value.type}\ndata: ${JSON.stringify(first.value.data)}\n\n`
        );
      }
      while (true) {
        const next = await iterator.next();
        if (next.done) break;
        if (!disconnected) {
          response.write(
            `event: ${next.value.type}\ndata: ${JSON.stringify(next.value.data)}\n\n`
          );
        }
      }
    } finally {
      finished = true;
      response.off("close", close);
      await Promise.allSettled(disconnectTasks);
      if (streamStarted && !response.destroyed) response.end();
    }
  }

  private error(response: ServerResponse, error: unknown): void {
    if (response.headersSent) {
      response.end();
      return;
    }
    const normalized =
      error instanceof RuntimeError
        ? error
        : error instanceof HarnessError
          ? new RuntimeError(
              error.type === "SESSION_NOT_FOUND" ? "SESSION_NOT_FOUND" : "INTERNAL_FAILURE",
              error.message,
              error.status
            )
          : new RuntimeError("INTERNAL_FAILURE", "Unexpected runtime failure", 500);
    const body: RuntimeErrorBody = {
      error: {
        code: normalized.code,
        message: normalized.message,
        ...(normalized.details === undefined ? {} : { details: normalized.details })
      }
    };
    this.json(response, normalized.status, body);
  }

  private async recoverStaleSocket(): Promise<void> {
    const owner = await this.readOwner();
    let metadata;
    try {
      metadata = await lstat(this.options.socketPath);
    } catch (error) {
      if ((error as NodeJS.ErrnoException).code === "ENOENT") {
        if (owner === undefined) return;
        if (this.pidIsDemonstrablyAbsent(owner.pid)) {
          await unlink(this.ownerFile);
          return;
        }
        throw new RuntimeError(
          "FORBIDDEN",
          "Daemon owner is live or ambiguous while the socket is absent",
          409
        );
      }
      throw error;
    }
    if (!metadata.isSocket()) {
      throw new RuntimeError("FORBIDDEN", "Refusing to replace a non-socket control path", 409);
    }
    if (process.getuid !== undefined && metadata.uid !== process.getuid()) {
      throw new RuntimeError("FORBIDDEN", "Refusing to replace another user's socket", 403);
    }
    if (owner === undefined) {
      throw new RuntimeError(
        "FORBIDDEN",
        "Refusing stale-socket recovery without an authenticated owner record",
        409
      );
    }
    if (
      owner.socketPath !== this.options.socketPath ||
      owner.uid !== (process.getuid?.() ?? -1)
    ) {
      throw new RuntimeError("FORBIDDEN", "Daemon owner record does not match this user/socket", 403);
    }
    if (!this.pidIsDemonstrablyAbsent(owner.pid)) {
      throw new RuntimeError(
        "RESIDENCY_TRANSITION_IN_PROGRESS",
        "Runtime daemon owner is live or ambiguous",
        409
      );
    }
    await unlink(this.options.socketPath);
    await unlink(this.ownerFile);
  }

  private async readOwner(): Promise<
    | {
        schemaVersion: "chirality.daemon-owner/v1";
        daemonId: string;
        pid: number;
        uid: number;
        socketPath: string;
        startedAt: string;
      }
    | undefined
  > {
    let metadata;
    try {
      metadata = await lstat(this.ownerFile);
    } catch (error) {
      if ((error as NodeJS.ErrnoException).code === "ENOENT") return undefined;
      throw error;
    }
    if (
      !metadata.isFile() ||
      (process.getuid !== undefined && metadata.uid !== process.getuid()) ||
      (metadata.mode & 0o077) !== 0
    ) {
      throw new RuntimeError("FORBIDDEN", "Unsafe daemon owner record", 403);
    }
    let value: unknown;
    try {
      value = JSON.parse(await readFile(this.ownerFile, "utf8"));
    } catch {
      throw new RuntimeError("FORBIDDEN", "Malformed daemon owner record", 409);
    }
    const owner = value as Record<string, unknown>;
    if (
      owner["schemaVersion"] !== "chirality.daemon-owner/v1" ||
      typeof owner["daemonId"] !== "string" ||
      typeof owner["pid"] !== "number" ||
      !Number.isSafeInteger(owner["pid"]) ||
      typeof owner["uid"] !== "number" ||
      typeof owner["socketPath"] !== "string" ||
      typeof owner["startedAt"] !== "string"
    ) {
      throw new RuntimeError("FORBIDDEN", "Malformed daemon owner record", 409);
    }
    return owner as Awaited<ReturnType<RuntimeDaemon["readOwner"]>>;
  }

  private pidIsDemonstrablyAbsent(pid: number): boolean {
    if (pid <= 0) return false;
    try {
      process.kill(pid, 0);
      return false;
    } catch (error) {
      return (error as NodeJS.ErrnoException).code === "ESRCH";
    }
  }

  private async removeOwnedRecord(): Promise<void> {
    const owner = await this.readOwner().catch(() => undefined);
    if (owner?.daemonId !== this.daemonId || owner.pid !== process.pid) return;
    await unlink(this.ownerFile).catch((error: NodeJS.ErrnoException) => {
      if (error.code !== "ENOENT") throw error;
    });
  }
}
