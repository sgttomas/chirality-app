import { lstat, readFile, realpath } from "node:fs/promises";
import { request as httpRequest, type IncomingMessage } from "node:http";
import { resolve } from "node:path";
import {
  RUNTIME_ROUTES,
  RuntimeError,
  validateHostedBootstrapStatus,
  type Agent1RunRequest,
  type HostedBootstrapStatus,
  type HostedBootstrapLoginStartResponse,
  type AgentDefinitionSummary,
  type AgentsResponse,
  type CredentialMutationResponse,
  type CredentialStatusResponse,
  type CreateSessionRequest,
  type DaemonStatusResponse,
  type HealthResponse,
  type InterruptResponse,
  type ModelsResponse,
  type PermissionDecisionRequest,
  type PermissionDecisionResponse,
  type ProjectRegistrationRequest,
  type HostedBootstrapProjectRegistrationRequest,
  type HostedBootstrapProjectInitializationRequest,
  type HostedBootstrapProjectRegistrationResponse,
  type ProjectRegistrationResponse,
  type ProjectStatus,
  type ProjectsResponse,
  type RegisteredProject,
  type ResidencyStatus,
  type RuntimeSseFrame,
  type RuntimeSessionBootRequest,
  type RuntimeSessionRecord,
  type ScaffoldRequest,
  type ScaffoldResponse,
  type SessionDeleteResponse,
  type SessionBootResponse,
  type SessionReplayResponse,
  type SessionResponse,
  type SessionsResponse,
  type SessionTurnRequest,
  type SessionTurnState,
  type SessionSteerRequest,
  type SessionSteerReceiptRequest,
  type SessionSteerResponse,
  type SessionRequestsResponse,
  type AnswerSessionRequestRequest,
  type AnswerSessionRequestResponse,
  type ServerRequestAnswer
  , type ApplicationToolRegistrationRequest
  , type ApplicationToolCatalog
  , type ApplicationToolBinding
  , type ApplicationToolInvocation
  , type ApplicationToolCompletionRequest
  , type RolesResponse
  , type MethodsResponse
  , type MethodInspectionResponse
  , type ResolveSelectedContextRequest
  , type ResolveSelectedContextResponse
  , type ReplaceSelectedMethodsRequest
  , type ReplaceSelectedMethodsResponse
  , type NativePlanCapabilityResponse
  , type NativePlanClarificationsResponse
  , type NativePlanRevisionsResponse
  , type ExportNativePlanRequest
  , type ExportNativePlanResponse
  , type ReplyNativePlanClarificationRequest
  , type ReplyNativePlanClarificationResponse
} from "@chirality/runtime-contracts";
import { RuntimeTransportError, runtimeErrorFromResponse } from "./errors.js";
import { parseSse, parseUiEvent, type SseFrame } from "./sse.js";

export const STREAM_TRANSPORT_TIMEOUT_MS = 25_000;

const MAX_JSON_BYTES = 16 * 1024 * 1024;

export interface RuntimeClientOptions {
  socketPath: string;
  tokenFile: string;
  /** Idle timeout for JSON requests (default 30 s), independent of stream transport health. */
  timeoutMs?: number;
  /** Byte inactivity and connection-opening deadline; Runtime comments count as activity. */
  streamTransportTimeoutMs?: number;
  loadToken?: (tokenFile: string) => Promise<string>;
}

export interface AttachSessionTurnOptions {
  /** Deliver only frames with a sequence greater than this value (0 replays the whole buffer). */
  after?: number;
  /** If present, atomically attach only to this Runtime turn identity. */
  turnId?: string;
}

export interface CancellableStream<T> extends AsyncIterable<T> {
  cancel(reason?: unknown): void;
}

export type RuntimeStream = CancellableStream<RuntimeSseFrame>;
export type RawSseStream = CancellableStream<SseFrame>;

type JsonRequestOptions = {
  timeoutMs?: number;
  method?: "GET" | "POST" | "PUT" | "PATCH" | "DELETE";
  body?: unknown;
  signal?: AbortSignal;
};

async function defaultLoadToken(tokenFile: string): Promise<string> {
  const metadata = await lstat(tokenFile);
  if (!metadata.isFile() || metadata.isSymbolicLink()) {
    throw new RuntimeTransportError("Runtime token path must be a regular file");
  }
  if ((metadata.mode & 0o077) !== 0) {
    throw new RuntimeTransportError("Runtime token file permissions must be 0600 or stricter");
  }
  if (process.getuid !== undefined && metadata.uid !== process.getuid()) {
    throw new RuntimeTransportError("Runtime token file must be owned by the current user");
  }
  const token = (await readFile(tokenFile, "utf8")).trim();
  if (!/^[A-Za-z0-9_-]+$/u.test(token)) {
    throw new RuntimeTransportError("Runtime token file is empty or malformed");
  }
  return token;
}

async function readResponseJson(response: IncomingMessage): Promise<unknown> {
  const chunks: Buffer[] = [];
  let bytes = 0;
  for await (const chunk of response) {
    const buffer = Buffer.isBuffer(chunk) ? chunk : Buffer.from(chunk);
    bytes += buffer.byteLength;
    if (bytes > MAX_JSON_BYTES) {
      response.destroy();
      throw new RuntimeTransportError("Runtime JSON response exceeds the size limit");
    }
    chunks.push(buffer);
  }
  if (chunks.length === 0) return undefined;
  const source = Buffer.concat(chunks).toString("utf8");
  try {
    return JSON.parse(source);
  } catch (cause) {
    throw new RuntimeTransportError("Runtime returned malformed JSON", cause);
  }
}

export class RuntimeClient {
  private readonly timeoutMs: number;
  private readonly loadToken: (tokenFile: string) => Promise<string>;

  constructor(private readonly options: RuntimeClientOptions) {
    if (!options.socketPath) {
      throw new RuntimeTransportError("A Unix socket path is required");
    }
    if (!options.tokenFile) {
      throw new RuntimeTransportError("A runtime token file is required");
    }
    this.timeoutMs = options.timeoutMs ?? 30_000;
    this.loadToken = options.loadToken ?? defaultLoadToken;
  }

  async requestJson<T>(
    path: string,
    options: JsonRequestOptions = {}
  ): Promise<T> {
    const token = await this.loadToken(this.options.tokenFile);
    const body =
      options.body === undefined ? undefined : Buffer.from(JSON.stringify(options.body), "utf8");
    const response = await this.request(path, {
      method: options.method ?? "GET",
      token,
      body,
      signal: options.signal,
      accept: "application/json",
      timeoutMs: options.timeoutMs
    });
    const value = await readResponseJson(response);
    const status = response.statusCode ?? 500;
    if (status < 200 || status >= 300) {
      throw runtimeErrorFromResponse(status, value);
    }
    return value as T;
  }

  async requestSse(
    path: string,
    options: Omit<JsonRequestOptions, "method"> & { method?: "GET" | "POST" } = {}
  ): Promise<RawSseStream> {
    const token = await this.loadToken(this.options.tokenFile);
    const body =
      options.body === undefined ? undefined : Buffer.from(JSON.stringify(options.body), "utf8");
    const controller = new AbortController();
    const abort = (): void => controller.abort(options.signal?.reason);
    if (options.signal?.aborted) abort();
    else options.signal?.addEventListener("abort", abort, { once: true });
    const transportTimeoutMs = this.options.streamTransportTimeoutMs ?? STREAM_TRANSPORT_TIMEOUT_MS;
    // This deadline bounds opening, even before a socket has connected. Once
    // open, the socket idle timeout resets on bytes (including SSE comments),
    // not model output. Neither deadline interrupts the Runtime-owned turn.
    const opening = setTimeout(() => controller.abort(new RuntimeTransportError("Runtime stream opening timed out", undefined, "timeout")), transportTimeoutMs);
    let response: IncomingMessage;
    try {
      response = await this.request(path, {
        method: options.method ?? "GET", token, body, signal: controller.signal,
        accept: "text/event-stream", timeoutMs: transportTimeoutMs
      });
    } catch (error) {
      options.signal?.removeEventListener("abort", abort);
      if (controller.signal.reason instanceof RuntimeTransportError) throw controller.signal.reason;
      throw error;
    } finally {
      clearTimeout(opening);
    }
    const status = response.statusCode ?? 500;
    if (status < 200 || status >= 300) {
      const value = await readResponseJson(response);
      options.signal?.removeEventListener("abort", abort);
      throw runtimeErrorFromResponse(status, value);
    }
    const contentType = response.headers["content-type"] ?? "";
    if (!contentType.toLowerCase().includes("text/event-stream")) {
      response.destroy();
      options.signal?.removeEventListener("abort", abort);
      throw new RuntimeTransportError("Runtime stream response is not text/event-stream");
    }
    const iterator = (async function* (): AsyncGenerator<SseFrame> {
      try {
        yield* parseSse(response);
      } finally {
        options.signal?.removeEventListener("abort", abort);
        response.destroy();
      }
    })();
    return {
      [Symbol.asyncIterator](): AsyncIterator<SseFrame> {
        return iterator;
      },
      cancel(reason?: unknown): void {
        controller.abort(reason);
        response.destroy();
      }
    };
  }

  async requestEvents(
    path: string,
    options: Omit<JsonRequestOptions, "method"> & { method?: "GET" | "POST" } = {}
  ): Promise<RuntimeStream> {
    const source = await this.requestSse(path, options);
    const iterator = (async function* (): AsyncGenerator<RuntimeSseFrame> {
      try {
        for await (const frame of source) {
          yield parseUiEvent(frame);
        }
      } finally {
        source.cancel();
      }
    })();
    return {
      [Symbol.asyncIterator](): AsyncIterator<RuntimeSseFrame> {
        return iterator;
      },
      cancel(reason?: unknown): void {
        source.cancel(reason);
      }
    };
  }

  health(signal?: AbortSignal): Promise<HealthResponse> {
    return this.requestJson(RUNTIME_ROUTES.health, { signal });
  }

  daemonStatus(signal?: AbortSignal): Promise<DaemonStatusResponse> {
    return this.requestJson(RUNTIME_ROUTES.daemonStatus, { signal });
  }

  async listProjects(signal?: AbortSignal): Promise<readonly ProjectStatus[]> {
    const response = await this.requestJson<ProjectsResponse>(RUNTIME_ROUTES.projects, {
      signal
    });
    return response.projects;
  }

  registerProject(
    request: ProjectRegistrationRequest,
    signal?: AbortSignal
  ): Promise<ProjectRegistrationResponse> {
    return this.requestJson(RUNTIME_ROUTES.projectRegister, {
      method: "POST",
      body: request,
      signal
    });
  }

  async registerHostedBootstrapProject(request: HostedBootstrapProjectRegistrationRequest, signal?: AbortSignal): Promise<HostedBootstrapProjectRegistrationResponse> {
    return this.safeHostedProjectRegistration(await this.requestJson(RUNTIME_ROUTES.hostedBootstrapProjectRegister, { method: "POST", body: request, signal }));
  }

  async initializeHostedBootstrapProject(request: HostedBootstrapProjectInitializationRequest, signal?: AbortSignal): Promise<HostedBootstrapProjectRegistrationResponse> {
    return this.safeHostedProjectRegistration(await this.requestJson(RUNTIME_ROUTES.hostedBootstrapProjectInitialize, { method: "POST", body: request, signal }));
  }

  private safeHostedProjectRegistration(value: unknown): HostedBootstrapProjectRegistrationResponse {
    if (!value || typeof value !== "object" || Array.isArray(value) || Object.keys(value).sort().join(",") !== "manifestHash,projectId") throw new RuntimeError("INVALID_REQUEST", "Invalid hosted project registration response");
    const result = value as Record<string, unknown>;
    if (typeof result.projectId !== "string" || !/^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$/u.test(result.projectId) || typeof result.manifestHash !== "string" || !/^[a-f0-9]{64}$/u.test(result.manifestHash)) throw new RuntimeError("INVALID_REQUEST", "Invalid hosted project registration response");
    return { projectId: result.projectId, manifestHash: result.manifestHash };
  }

  projectStatus(projectId: string, signal?: AbortSignal): Promise<ProjectStatus> {
    return this.requestJson(RUNTIME_ROUTES.projectStatus(projectId), { signal });
  }

  listRoles(projectId: string, signal?: AbortSignal): Promise<RolesResponse> {
    return this.requestJson(RUNTIME_ROUTES.roles(projectId), { signal });
  }

  listMethods(projectId: string, signal?: AbortSignal): Promise<MethodsResponse> {
    return this.requestJson(RUNTIME_ROUTES.methods(projectId), { signal });
  }

  inspectMethod(projectId: string, qualifiedId: string, signal?: AbortSignal): Promise<MethodInspectionResponse> {
    return this.requestJson(RUNTIME_ROUTES.method(projectId, qualifiedId), { signal });
  }

  async resolveProjectByRoot(
    projectRoot: string,
    signal?: AbortSignal
  ): Promise<RegisteredProject> {
    const requested = await realpath(resolve(projectRoot)).catch(() => resolve(projectRoot));
    const projects = await this.listProjects(signal);
    const match = projects.find(
      ({ project }) => resolve(project.canonicalRoot) === requested
    );
    if (match === undefined) {
      throw new RuntimeError(
        "PROJECT_NOT_FOUND",
        `No registered project owns ${requested}`,
        404
      );
    }
    if (match.manifestDrift || !match.adaptersEnabled) {
      throw new RuntimeError(
        "PROJECT_MANIFEST_DRIFT",
        "Project manifest changed after registration",
        409,
        { projectId: match.project.projectId }
      );
    }
    return match.project;
  }

  async listSessions(
    projectId: string,
    signal?: AbortSignal
  ): Promise<readonly RuntimeSessionRecord[]> {
    const response = await this.requestJson<SessionsResponse>(RUNTIME_ROUTES.sessions(projectId), {
      signal
    });
    return response.sessions;
  }

  /** Host-only. Bind after createSession and before boot/first turn; the descriptor catalog is immutable. */
  registerApplicationTools(projectId: string, sessionId: string, request: ApplicationToolRegistrationRequest, signal?: AbortSignal): Promise<ApplicationToolBinding> {
    return this.requestJson(RUNTIME_ROUTES.applicationTools(projectId, sessionId), { method: "PUT", body: request, signal });
  }

  applicationTools(projectId: string, sessionId: string, signal?: AbortSignal): Promise<{ catalog?: ApplicationToolCatalog; binding?: ApplicationToolBinding }> {
    return this.requestJson(RUNTIME_ROUTES.applicationTools(projectId, sessionId), { signal });
  }

  releaseApplicationTools(projectId: string, sessionId: string, bindingId: string, signal?: AbortSignal): Promise<{ released: true }> {
    return this.requestJson(RUNTIME_ROUTES.applicationTools(projectId, sessionId), { method: "DELETE", body: { bindingId }, signal });
  }

  listApplicationToolCalls(projectId: string, sessionId: string, bindingId: string, signal?: AbortSignal): Promise<{ calls: ApplicationToolInvocation[] }> {
    return this.requestJson(`${RUNTIME_ROUTES.applicationToolCalls(projectId, sessionId)}?bindingId=${encodeURIComponent(bindingId)}`, { signal });
  }

  completeApplicationToolCall(projectId: string, sessionId: string, invocationId: string, request: ApplicationToolCompletionRequest, signal?: AbortSignal): Promise<{ state: "completed" | "already-completed" }> {
    return this.requestJson(RUNTIME_ROUTES.applicationToolResult(projectId, sessionId, invocationId), { method: "POST", body: request, signal });
  }

  async createSession(
    projectId: string,
    request: CreateSessionRequest,
    signal?: AbortSignal
  ): Promise<RuntimeSessionRecord> {
    if (request.projectId !== projectId) {
      throw new RuntimeError(
        "INVALID_REQUEST",
        "Session request projectId does not match the route",
        400
      );
    }
    const { projectId: _projectId, ...daemonRequest } = request;
    const response = await this.requestJson<SessionResponse>(RUNTIME_ROUTES.sessions(projectId), {
      method: "POST",
      body: daemonRequest,
      signal
    });
    return response.session;
  }

  getSession(
    projectId: string,
    sessionId: string,
    signal?: AbortSignal
  ): Promise<RuntimeSessionRecord> {
    return this.requestJson<SessionResponse>(
      RUNTIME_ROUTES.session(projectId, sessionId),
      { signal }
    ).then((response) => response.session);
  }

  deleteSession(
    projectId: string,
    sessionId: string,
    signal?: AbortSignal
  ): Promise<SessionDeleteResponse> {
    return this.requestJson(RUNTIME_ROUTES.session(projectId, sessionId), {
      method: "DELETE",
      signal
    });
  }

  async resolveSessionOwner(
    sessionId: string,
    signal?: AbortSignal
  ): Promise<{ project: RegisteredProject; session: RuntimeSessionRecord }> {
    const projects = await this.listProjects(signal);
    for (const status of projects) {
      try {
        const session = await this.getSession(status.project.projectId, sessionId, signal);
        return { project: status.project, session };
      } catch (error) {
        if (
          error instanceof RuntimeError &&
          (error.code === "SESSION_NOT_FOUND" || error.code === "NOT_FOUND")
        ) {
          continue;
        }
        throw error;
      }
    }
    throw new RuntimeError("SESSION_NOT_FOUND", `Unknown session: ${sessionId}`, 404);
  }

  async bootSession(
    projectId: string,
    sessionId: string,
    request: RuntimeSessionBootRequest = {},
    signal?: AbortSignal
  ): Promise<SessionBootResponse> {
    try {
      return await this.requestJson<SessionBootResponse>(
        RUNTIME_ROUTES.sessionBoot(projectId, sessionId),
        { method: "POST", body: request, signal, timeoutMs: 180_000 }
      );
    } catch (error) {
      if (error instanceof RuntimeTransportError) throw new RuntimeTransportError(
        error.reason === "timeout" ? "Session boot request timed out" : "Session boot transport failed",
        error, error.reason, "boot", sessionId
      );
      throw error;
    }
  }

  replaySession(
    projectId: string,
    sessionId: string,
    signal?: AbortSignal
  ): Promise<SessionReplayResponse> {
    return this.requestJson(RUNTIME_ROUTES.sessionReplay(projectId, sessionId), {
      signal
    });
  }

  resolveSelectedContext(projectId: string, sessionId: string, request: ResolveSelectedContextRequest, signal?: AbortSignal): Promise<ResolveSelectedContextResponse> {
    return this.requestJson(RUNTIME_ROUTES.sessionContextResolve(projectId, sessionId), { method: "POST", body: request, signal });
  }

  replaceSelectedMethods(projectId: string, sessionId: string, request: ReplaceSelectedMethodsRequest, signal?: AbortSignal): Promise<ReplaceSelectedMethodsResponse> {
    return this.requestJson(RUNTIME_ROUTES.sessionMethods(projectId, sessionId), { method: "PUT", body: request, signal });
  }

  getNativePlanCapability(projectId: string, sessionId: string, signal?: AbortSignal): Promise<NativePlanCapabilityResponse> {
    return this.requestJson(RUNTIME_ROUTES.nativePlanCapability(projectId, sessionId), { signal });
  }

  listNativePlanRevisions(projectId: string, sessionId: string, signal?: AbortSignal): Promise<NativePlanRevisionsResponse> {
    return this.requestJson(RUNTIME_ROUTES.nativePlanRevisions(projectId, sessionId), { signal });
  }

  listNativePlanClarifications(projectId: string, sessionId: string, signal?: AbortSignal): Promise<NativePlanClarificationsResponse> {
    return this.requestJson(RUNTIME_ROUTES.nativePlanClarifications(projectId, sessionId), { signal });
  }

  replyNativePlanClarification(projectId: string, sessionId: string, request: ReplyNativePlanClarificationRequest, signal?: AbortSignal): Promise<ReplyNativePlanClarificationResponse> {
    return this.requestJson(RUNTIME_ROUTES.nativePlanClarificationReply(projectId, sessionId), { method: "POST", body: request, signal });
  }

  exportNativePlan(projectId: string, sessionId: string, request: ExportNativePlanRequest, signal?: AbortSignal): Promise<ExportNativePlanResponse> {
    return this.requestJson(RUNTIME_ROUTES.nativePlanExport(projectId, sessionId), { method: "POST", body: request, signal });
  }

  turnSession(
    projectId: string,
    sessionId: string,
    request: SessionTurnRequest,
    signal?: AbortSignal
  ): Promise<RuntimeStream> {
    return this.requestEvents(RUNTIME_ROUTES.sessionTurn(projectId, sessionId), {
      method: "POST",
      body: request,
      signal
    });
  }

  /**
   * Attaches to the session's active (or recently finished) turn owned by the
   * Runtime. Cancelling the stream unsubscribes only; the turn continues.
   */
  attachSessionTurn(
    projectId: string,
    sessionId: string,
    options: AttachSessionTurnOptions = {},
    signal?: AbortSignal
  ): Promise<RuntimeStream> {
    const after = options.after ?? 0;
    if (!Number.isSafeInteger(after) || after < 0) {
      throw new RuntimeError("INVALID_REQUEST", "after must be a non-negative integer", 400);
    }
    return this.requestEvents(`${RUNTIME_ROUTES.sessionTurnStream(projectId, sessionId)}?after=${after}${options.turnId === undefined ? "" : `&turnId=${encodeURIComponent(options.turnId)}`}`, {
      method: "GET",
      signal
    });
  }

  sessionTurnState(
    projectId: string,
    sessionId: string,
    signal?: AbortSignal
  ): Promise<SessionTurnState> {
    return this.requestJson(RUNTIME_ROUTES.sessionTurnState(projectId, sessionId), { signal });
  }

  sessionTurnSteer(projectId: string, sessionId: string, request: SessionSteerRequest, signal?: AbortSignal): Promise<SessionSteerResponse> {
    return this.requestJson(RUNTIME_ROUTES.sessionTurnSteer(projectId, sessionId), { method: "POST", body: request, signal });
  }

  sessionTurnSteerReceipt(projectId: string, sessionId: string, request: SessionSteerReceiptRequest, signal?: AbortSignal): Promise<SessionSteerResponse> {
    return this.requestJson(RUNTIME_ROUTES.sessionTurnSteerReceipt(projectId, sessionId), { method: "POST", body: request, signal });
  }

  listSessionRequests(
    projectId: string,
    sessionId: string,
    signal?: AbortSignal
  ): Promise<SessionRequestsResponse> {
    return this.requestJson(RUNTIME_ROUTES.sessionRequests(projectId, sessionId), { signal });
  }

  answerSessionRequest(
    projectId: string,
    sessionId: string,
    requestId: string,
    answer: ServerRequestAnswer,
    signal?: AbortSignal
  ): Promise<AnswerSessionRequestResponse> {
    const body: AnswerSessionRequestRequest = { answer };
    return this.requestJson(RUNTIME_ROUTES.sessionRequestAnswer(projectId, sessionId, requestId), {
      method: "POST",
      body,
      signal
    });
  }

  interruptSession(
    projectId: string,
    sessionId: string,
    signal?: AbortSignal
  ): Promise<InterruptResponse> {
    return this.requestJson(RUNTIME_ROUTES.sessionInterrupt(projectId, sessionId), {
      method: "POST",
      signal
    });
  }

  decidePermission(
    projectId: string,
    sessionId: string,
    request: PermissionDecisionRequest,
    signal?: AbortSignal
  ): Promise<PermissionDecisionResponse> {
    return this.requestJson(RUNTIME_ROUTES.sessionPermission(projectId, sessionId), {
      method: "POST",
      body: request,
      signal
    });
  }

  async listAgents(
    projectId: string,
    signal?: AbortSignal
  ): Promise<readonly AgentDefinitionSummary[]> {
    const response = await this.requestJson<AgentsResponse>(RUNTIME_ROUTES.agents(projectId), {
      signal
    });
    return response.agents;
  }

  scaffold(
    projectId: string,
    request: ScaffoldRequest,
    signal?: AbortSignal
  ): Promise<ScaffoldResponse["scaffold"]> {
    return this.requestJson<ScaffoldResponse>(RUNTIME_ROUTES.scaffold(projectId), {
      method: "POST",
      body: request,
      signal
    }).then((response) => response.scaffold);
  }

  runAgent1(
    projectId: string,
    request: Agent1RunRequest,
    signal?: AbortSignal
  ): Promise<RuntimeStream> {
    return this.requestEvents(RUNTIME_ROUTES.runs(projectId), {
      method: "POST",
      body: request,
      signal
    });
  }

  async listModels(signal?: AbortSignal): Promise<ResidencyStatus> {
    const response = await this.requestJson<ModelsResponse>(RUNTIME_ROUTES.models, {
      signal
    });
    return response.residency;
  }

  activateModel(
    modelId: string,
    approvalReference: string,
    signal?: AbortSignal
  ): Promise<ResidencyStatus> {
    return this.requestJson<ModelsResponse>(RUNTIME_ROUTES.modelActivate(modelId), {
      method: "POST",
      body: { approvalReference },
      signal
    }).then((response) => response.residency);
  }

  credentialStatus(
    providerId: string,
    signal?: AbortSignal
  ): Promise<CredentialStatusResponse> {
    return this.requestJson(RUNTIME_ROUTES.credentials(providerId), { signal });
  }

  storeCredential(
    providerId: string,
    credential: string,
    signal?: AbortSignal
  ): Promise<CredentialMutationResponse> {
    return this.requestJson(RUNTIME_ROUTES.credentials(providerId), {
      method: "PUT",
      body: { credential },
      signal
    });
  }

  removeCredential(
    providerId: string,
    signal?: AbortSignal
  ): Promise<CredentialMutationResponse> {
    return this.requestJson(RUNTIME_ROUTES.credentials(providerId), {
      method: "DELETE",
      signal
    });
  }

  async hostedBootstrapStatus(projectId: string, signal?: AbortSignal): Promise<HostedBootstrapStatus> {
    return validateHostedBootstrapStatus(await this.requestJson(RUNTIME_ROUTES.hostedBootstrapStatus(projectId), { method: "GET", signal }));
  }

  async grantHostedProviderNetworkConsent(projectId: string, signal?: AbortSignal): Promise<HostedBootstrapStatus> {
    return validateHostedBootstrapStatus(await this.requestJson(RUNTIME_ROUTES.hostedBootstrapConsent(projectId), { method: "POST", body: { consent: true }, signal }));
  }

  async startHostedBootstrapLogin(projectId: string, signal?: AbortSignal): Promise<HostedBootstrapLoginStartResponse> {
    const result = await this.requestJson<HostedBootstrapLoginStartResponse>(RUNTIME_ROUTES.hostedBootstrapLoginStart(projectId), { method: "POST", body: {}, signal });
    if (!result || typeof result !== "object" || Array.isArray(result) || Object.keys(result).sort().join(",") !== "authUrl,loginId") throw new RuntimeError("INVALID_REQUEST", "Unsafe hosted login response");
    let url: URL;
    try { url = new URL(result.authUrl); } catch { throw new RuntimeError("INVALID_REQUEST", "Invalid hosted login URL"); }
    if (url.protocol !== "https:" || url.username || url.password || result.authUrl.length > 8192 || typeof result.loginId !== "string" || !result.loginId || result.loginId.length > 512) throw new RuntimeError("INVALID_REQUEST", "Unsafe hosted login response");
    return result;
  }

  async cancelHostedBootstrapLogin(projectId: string, signal?: AbortSignal): Promise<HostedBootstrapStatus> {
    return validateHostedBootstrapStatus(await this.requestJson(RUNTIME_ROUTES.hostedBootstrapLoginCancel(projectId), { method: "POST", body: {}, signal }));
  }

  /** Signs out this hosted project after the Runtime has fenced its admission. */
  async signOutHostedProject(projectId: string, signal?: AbortSignal): Promise<HostedBootstrapStatus> {
    return validateHostedBootstrapStatus(await this.requestJson(RUNTIME_ROUTES.hostedBootstrapLogout(projectId), { method: "POST", body: {}, signal }));
  }

  private async request(
    path: string,
    input: {
      method: string;
      token: string;
      body?: Buffer;
      signal?: AbortSignal;
      accept: string;
      timeoutMs?: number;
    }
  ): Promise<IncomingMessage> {
    return new Promise<IncomingMessage>((resolveResponse, reject) => {
      let settled = false;
      const fail = (error: unknown): void => {
        if (settled) return;
        settled = true;
        reject(
          error instanceof RuntimeTransportError
            ? error
            : new RuntimeTransportError(
                `Unable to reach the Chirality runtime at ${this.options.socketPath}`,
                error
              )
        );
      };
      const request = httpRequest(
        {
          socketPath: this.options.socketPath,
          path,
          method: input.method,
          signal: input.signal,
          headers: {
            Accept: input.accept,
            Authorization: `Bearer ${input.token}`,
            ...(input.body === undefined
              ? {}
              : {
                  "Content-Type": "application/json",
                  "Content-Length": String(input.body.byteLength)
                })
          }
        },
        (response) => {
          if (settled) {
            response.destroy();
            return;
          }
          settled = true;
          resolveResponse(response);
        }
      );
      const timeoutMs = input.timeoutMs ?? this.timeoutMs;
      if (timeoutMs > 0) {
        request.setTimeout(timeoutMs, () => {
          request.destroy(new RuntimeTransportError("Runtime request timed out", undefined, "timeout"));
        });
      }
      request.once("error", fail);
      if (input.body !== undefined) request.write(input.body);
      request.end();
    });
  }
}
