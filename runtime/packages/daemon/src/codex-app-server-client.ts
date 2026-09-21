import { spawn } from "node:child_process";
import type { Readable, Writable } from "node:stream";
import { RuntimeError } from "@chirality/runtime-contracts";

/**
 * Newline-delimited JSON-RPC 2.0 client for the stock `codex app-server`
 * (pinned `@openai/codex@0.154.0`). It carries requests, answers server
 * requests through one handler, and passes every notification through
 * unchanged. Payloads that can carry account data are never logged; method
 * names and ids only.
 */

export interface CodexLogger {
  warn(event: string, fields?: Readonly<Record<string, unknown>>): void;
  error(event: string, fields?: Readonly<Record<string, unknown>>): void;
}
export const NOOP_CODEX_LOGGER: CodexLogger = Object.freeze({ warn() {}, error() {} });

export interface CodexAppServerExit { code: number | null; signal: NodeJS.Signals | null }
export interface CodexAppServerTransport {
  readonly pid?: number;
  readonly stdin: Writable;
  readonly stdout: Readable;
  readonly exited: Promise<CodexAppServerExit>;
  /** SIGTERM, then SIGKILL after the grace period; resolves once the child has exited. */
  terminate(): Promise<void>;
}
export type CodexAppServerTransportFactory = () => Promise<CodexAppServerTransport>;

export interface SpawnCodexAppServerOptions {
  executablePath: string;
  /** Effective Codex home (section 3 overlay). `HOME` stays the user's real home. */
  effectiveHome: string;
  cwd?: string;
  killGraceMs?: number;
  /** Receives one stderr line at a time, already redacted of e-mail-like tokens. */
  onStderr?: (line: string) => void;
}
// Release unsubscribed idle thread caches promptly so a cold resume can adopt
// updated developer guidance. Stock Codex still waits for active work to finish.
export const CODEX_APP_SERVER_ARGUMENTS = Object.freeze(["-c", 'cli_auth_credentials_store="file"', "-c", "thread_unload_delay_secs=0", "app-server"] as const);

/** Replaces e-mail-like tokens so account identifiers never reach a log. */
export function redactAccountText(value: string): string {
  return value.replace(/\S+@\S+/g, "[redacted]");
}

/** SIGTERM to SIGKILL grace for the app-server child; part of the service close budget the App host's kill window must exceed. */
export const DEFAULT_APP_SERVER_KILL_GRACE_MS = 2_000;

export async function spawnCodexAppServer(options: SpawnCodexAppServerOptions): Promise<CodexAppServerTransport> {
  const child = spawn(options.executablePath, [...CODEX_APP_SERVER_ARGUMENTS], {
    env: { ...process.env, CODEX_HOME: options.effectiveHome },
    cwd: options.cwd,
    stdio: ["pipe", "pipe", "pipe"],
    shell: false,
    detached: false
  });
  const exited = new Promise<CodexAppServerExit>(resolve => { child.once("close", (code, signal) => resolve({ code, signal })); });
  child.on("error", () => undefined);
  child.stdin.on("error", () => undefined);
  let stderrBuffer = "";
  child.stderr.setEncoding("utf8");
  child.stderr.on("data", (chunk: string) => {
    if (!options.onStderr) return;
    stderrBuffer += chunk;
    let index: number;
    while ((index = stderrBuffer.indexOf("\n")) >= 0) {
      const line = stderrBuffer.slice(0, index); stderrBuffer = stderrBuffer.slice(index + 1);
      if (line.trim()) options.onStderr(redactAccountText(line).slice(0, 2048));
    }
    if (stderrBuffer.length > 65_536) stderrBuffer = stderrBuffer.slice(-65_536);
  });
  await new Promise<void>((resolve, reject) => { child.once("spawn", resolve); child.once("error", reject); }).catch(() => { throw new RuntimeError("ENGINE_UNAVAILABLE", "codex app-server could not be started", 503); });
  let terminating: Promise<void> | undefined;
  return {
    pid: child.pid,
    stdin: child.stdin,
    stdout: child.stdout,
    exited,
    terminate: () => terminating ??= (async () => {
      if (child.exitCode === null && child.signalCode === null) {
        try { child.kill("SIGTERM"); } catch { /* exited */ }
        let timer: ReturnType<typeof setTimeout> | undefined;
        await Promise.race([exited, new Promise<void>(resolve => { timer = setTimeout(resolve, options.killGraceMs ?? DEFAULT_APP_SERVER_KILL_GRACE_MS); })]);
        clearTimeout(timer);
        if (child.exitCode === null && child.signalCode === null) { try { child.kill("SIGKILL"); } catch { /* exited */ } }
      }
      await exited;
    })()
  };
}

export type CodexRequestId = string | number;
export interface CodexServerRequest { id: CodexRequestId; method: string; params: unknown }
export interface CodexNotification { method: string; params: unknown }
export type CodexServerRequestOutcome = { result: unknown } | { error: { code: number; message: string; data?: unknown } };
export type CodexServerRequestHandler = (request: CodexServerRequest) => Promise<CodexServerRequestOutcome>;
export const JSON_RPC_METHOD_NOT_FOUND = -32601;

export interface CodexAppServerClientOptions {
  logger?: CodexLogger;
  /** Default request timeout; 0 disables it. */
  requestTimeoutMs?: number;
}
interface PendingRequest { method: string; resolve(value: unknown): void; reject(error: unknown): void; timer?: ReturnType<typeof setTimeout> }

export class CodexAppServerClient {
  private nextId = 1;
  private readonly pending = new Map<number, PendingRequest>();
  private readonly notificationListeners = new Set<(notification: CodexNotification) => void>();
  private serverRequestHandler: CodexServerRequestHandler = async () => ({ error: { code: JSON_RPC_METHOD_NOT_FOUND, message: "unsupported request" } });
  private buffer = "";
  private exitInfo: CodexAppServerExit | undefined;
  private malformedLines = 0;
  readonly exited: Promise<CodexAppServerExit>;
  private readonly logger: CodexLogger;
  constructor(private readonly transport: CodexAppServerTransport, private readonly options: CodexAppServerClientOptions = {}) {
    this.logger = options.logger ?? NOOP_CODEX_LOGGER;
    transport.stdout.setEncoding("utf8");
    transport.stdout.on("data", (chunk: string) => this.consume(chunk));
    this.exited = transport.exited.then(info => { this.settleExit(info); return info; });
  }
  get pid(): number | undefined { return this.transport.pid; }
  get isRunning(): boolean { return this.exitInfo === undefined; }

  onNotification(listener: (notification: CodexNotification) => void): () => void {
    this.notificationListeners.add(listener);
    return () => { this.notificationListeners.delete(listener); };
  }
  setServerRequestHandler(handler: CodexServerRequestHandler): void { this.serverRequestHandler = handler; }

  request<T = unknown>(method: string, params: unknown, options: { timeoutMs?: number } = {}): Promise<T> {
    if (this.exitInfo !== undefined) return Promise.reject(this.unavailable(this.exitInfo));
    const id = this.nextId++;
    const timeoutMs = options.timeoutMs ?? this.options.requestTimeoutMs ?? 60_000;
    return new Promise<T>((resolve, reject) => {
      const entry: PendingRequest = { method, resolve: value => resolve(value as T), reject };
      if (timeoutMs > 0) entry.timer = setTimeout(() => { this.pending.delete(id); reject(new RuntimeError("ENGINE_UNAVAILABLE", `codex app-server did not answer ${method} within ${timeoutMs} ms`, 503, { method, id })); }, timeoutMs);
      this.pending.set(id, entry);
      this.write({ jsonrpc: "2.0", id, method, params }).catch(error => { clearTimeout(entry.timer); this.pending.delete(id); reject(error); });
    });
  }
  notify(method: string, params: unknown): Promise<void> { return this.write({ jsonrpc: "2.0", method, params }); }

  async close(): Promise<CodexAppServerExit> {
    await this.transport.terminate();
    return this.exited;
  }

  private write(message: Record<string, unknown>): Promise<void> {
    return new Promise<void>((resolve, reject) => {
      if (this.exitInfo !== undefined) { reject(this.unavailable(this.exitInfo)); return; }
      this.transport.stdin.write(`${JSON.stringify(message)}\n`, error => error ? reject(new RuntimeError("ENGINE_UNAVAILABLE", "codex app-server stdin is closed", 503)) : resolve());
    });
  }
  private unavailable(exit: CodexAppServerExit): RuntimeError {
    return new RuntimeError("ENGINE_UNAVAILABLE", `codex app-server exited (code ${exit.code ?? "null"}, signal ${exit.signal ?? "null"})`, 503, { reason: "CODEX_APP_SERVER_EXITED", code: exit.code, signal: exit.signal });
  }
  private settleExit(info: CodexAppServerExit): void {
    if (this.exitInfo !== undefined) return;
    this.exitInfo = info;
    const error = this.unavailable(info);
    for (const [id, entry] of this.pending) { clearTimeout(entry.timer); this.pending.delete(id); entry.reject(error); }
    this.logger.warn("codex.app-server.exit", { code: info.code, signal: info.signal, malformedLines: this.malformedLines });
  }
  private consume(chunk: string): void {
    this.buffer += chunk;
    let index: number;
    while ((index = this.buffer.indexOf("\n")) >= 0) {
      const line = this.buffer.slice(0, index); this.buffer = this.buffer.slice(index + 1);
      if (!line.trim()) continue;
      let message: unknown;
      try { message = JSON.parse(line); } catch { this.malformedLines++; continue; }
      this.dispatch(message);
    }
    if (this.buffer.length > 64 * 1024 * 1024) { this.buffer = ""; this.malformedLines++; }
  }
  private dispatch(message: unknown): void {
    if (!message || typeof message !== "object" || Array.isArray(message)) { this.malformedLines++; return; }
    const frame = message as { id?: unknown; method?: unknown; params?: unknown; result?: unknown; error?: unknown };
    const hasId = frame.id !== undefined && frame.id !== null;
    if (typeof frame.method === "string") {
      if (hasId) { void this.answerServerRequest({ id: frame.id as CodexRequestId, method: frame.method, params: frame.params }); return; }
      const notification: CodexNotification = { method: frame.method, params: frame.params };
      for (const listener of this.notificationListeners) { try { listener(notification); } catch (error) { this.logger.warn("codex.notification.listener_failed", { method: frame.method, error: error instanceof Error ? error.name : "unknown" }); } }
      return;
    }
    if (hasId && typeof frame.id === "number") {
      const entry = this.pending.get(frame.id);
      if (!entry) return;
      this.pending.delete(frame.id);
      clearTimeout(entry.timer);
      if (frame.error !== undefined) {
        const error = frame.error as { code?: unknown; message?: unknown; data?: unknown };
        entry.reject(new RuntimeError("ENGINE_UNAVAILABLE", `codex app-server rejected ${entry.method}: ${typeof error?.message === "string" ? error.message.slice(0, 512) : "error"}`, 503, { method: entry.method, jsonRpcCode: typeof error?.code === "number" ? error.code : undefined, ...(error?.data === undefined ? {} : { data: error.data }) }));
      } else entry.resolve(frame.result);
      return;
    }
    this.malformedLines++;
  }
  private async answerServerRequest(request: CodexServerRequest): Promise<void> {
    let outcome: CodexServerRequestOutcome;
    try { outcome = await this.serverRequestHandler(request); }
    catch (error) { this.logger.warn("codex.server-request.handler_failed", { method: request.method, id: request.id, error: error instanceof Error ? error.name : "unknown" }); outcome = { error: { code: -32603, message: "request handling failed" } }; }
    await this.write("result" in outcome ? { jsonrpc: "2.0", id: request.id, result: outcome.result } : { jsonrpc: "2.0", id: request.id, error: outcome.error }).catch(() => undefined);
  }
}

export interface CodexInitializeResponse { userAgent: string; codexHome: string; platformFamily: string; platformOs: string }
export interface CodexAppServerHostOptions {
  transportFactory: CodexAppServerTransportFactory;
  clientVersion: string;
  logger?: CodexLogger;
  requestTimeoutMs?: number;
  /** Restart delays in ms; the last value repeats. Defaults to 1, 2, 4, 8, 16, 30 s. */
  restartBackoffMs?: readonly number[];
  /** Stop restarting after this many failures within `failureWindowMs`. */
  maxFailures?: number;
  failureWindowMs?: number;
}
export type CodexAppServerHostState = "starting" | "running" | "restarting" | "stopped" | "closed";
export interface CodexAppServerHostStatus { state: CodexAppServerHostState; generation: number; pid?: number; failures: number; lastExit?: CodexAppServerExit }

/**
 * One long-lived app-server child per service. It initializes the child,
 * restarts it with backoff when it exits unexpectedly, fans notifications
 * out to subscribers and routes server requests to one handler.
 */
export class CodexAppServerHost {
  private client: CodexAppServerClient | undefined;
  private state: CodexAppServerHostState = "stopped";
  private generationNumber = 0;
  private failureTimes: number[] = [];
  private lastExit: CodexAppServerExit | undefined;
  private restartTimer: ReturnType<typeof setTimeout> | undefined;
  private starting: Promise<CodexInitializeResponse> | undefined;
  private closing = false;
  private readonly notificationListeners = new Set<(notification: CodexNotification) => void>();
  private readonly exitListeners = new Set<(exit: CodexAppServerExit, generation: number) => void>();
  private readonly startListeners = new Set<(generation: number) => void>();
  private serverRequestHandler: CodexServerRequestHandler = async () => ({ error: { code: JSON_RPC_METHOD_NOT_FOUND, message: "unsupported request" } });
  private readonly logger: CodexLogger;
  constructor(private readonly options: CodexAppServerHostOptions) { this.logger = options.logger ?? NOOP_CODEX_LOGGER; }

  get generation(): number { return this.generationNumber; }
  status(): CodexAppServerHostStatus {
    return { state: this.state, generation: this.generationNumber, ...(this.client?.pid === undefined ? {} : { pid: this.client.pid }), failures: this.failureTimes.length, ...(this.lastExit === undefined ? {} : { lastExit: this.lastExit }) };
  }
  onNotification(listener: (notification: CodexNotification) => void): () => void { this.notificationListeners.add(listener); return () => { this.notificationListeners.delete(listener); }; }
  onExit(listener: (exit: CodexAppServerExit, generation: number) => void): () => void { this.exitListeners.add(listener); return () => { this.exitListeners.delete(listener); }; }
  onStart(listener: (generation: number) => void): () => void { this.startListeners.add(listener); return () => { this.startListeners.delete(listener); }; }
  setServerRequestHandler(handler: CodexServerRequestHandler): void { this.serverRequestHandler = handler; this.client?.setServerRequestHandler(handler); }

  /** Spawns and initializes the child. Rejects when the child cannot start or refuses `initialize`. */
  start(): Promise<CodexInitializeResponse> {
    if (this.closing) return Promise.reject(new RuntimeError("ENGINE_UNAVAILABLE", "codex app-server host is closed", 503));
    if (this.starting) return this.starting;
    if (this.client?.isRunning) return Promise.reject(new RuntimeError("ENGINE_UNAVAILABLE", "codex app-server is already running", 503));
    this.state = "starting";
    this.starting = (async () => {
      const transport = await this.options.transportFactory();
      const client = new CodexAppServerClient(transport, { logger: this.logger, requestTimeoutMs: this.options.requestTimeoutMs });
      const generation = ++this.generationNumber;
      client.setServerRequestHandler(request => this.serverRequestHandler(request));
      client.onNotification(notification => { for (const listener of this.notificationListeners) { try { listener(notification); } catch (error) { this.logger.warn("codex.notification.listener_failed", { method: notification.method, error: error instanceof Error ? error.name : "unknown" }); } } });
      this.client = client;
      void client.exited.then(exit => this.handleExit(client, generation, exit));
      let initialized: CodexInitializeResponse;
      try {
        initialized = await client.request<CodexInitializeResponse>("initialize", { clientInfo: { name: "chirality", title: "Chirality", version: this.options.clientVersion }, capabilities: { experimentalApi: true } });
      } catch (error) {
        // A child that refuses initialize is not a running generation; its exit must not schedule a restart.
        if (this.client === client) this.client = undefined;
        await client.close().catch(() => undefined);
        throw error;
      }
      this.state = "running";
      for (const listener of this.startListeners) { try { listener(generation); } catch { /* listener failure is not a host failure */ } }
      return initialized;
    })();
    void this.starting.catch(() => { if (this.state === "starting") this.state = "stopped"; }).finally(() => { this.starting = undefined; });
    return this.starting;
  }

  request<T = unknown>(method: string, params: unknown, options?: { timeoutMs?: number }): Promise<T> {
    const client = this.client;
    if (!client?.isRunning || this.state !== "running") return Promise.reject(new RuntimeError("ENGINE_UNAVAILABLE", `codex app-server is ${this.state}`, 503, { reason: "CODEX_APP_SERVER_UNAVAILABLE", state: this.state }));
    return client.request<T>(method, params, options);
  }

  private handleExit(client: CodexAppServerClient, generation: number, exit: CodexAppServerExit): void {
    if (this.client !== client) return;
    this.lastExit = exit;
    for (const listener of this.exitListeners) { try { listener(exit, generation); } catch { /* observers only */ } }
    if (this.closing) { this.state = "closed"; return; }
    const now = Date.now();
    this.failureTimes = this.failureTimes.filter(time => now - time < (this.options.failureWindowMs ?? 180_000));
    this.failureTimes.push(now);
    if (this.failureTimes.length >= (this.options.maxFailures ?? 5)) {
      this.state = "stopped";
      this.logger.error("codex.app-server.stopped", { failures: this.failureTimes.length, code: exit.code, signal: exit.signal });
      return;
    }
    const backoff = this.options.restartBackoffMs ?? [1000, 2000, 4000, 8000, 16000, 30000];
    const delay = backoff[Math.min(this.failureTimes.length - 1, backoff.length - 1)] ?? 30000;
    this.state = "restarting";
    this.logger.warn("codex.app-server.restart", { attempt: this.failureTimes.length, delayMs: delay });
    this.restartTimer = setTimeout(() => {
      this.restartTimer = undefined;
      if (this.closing) return;
      this.state = "stopped";
      const previous = this.client;
      void this.start().catch(error => {
        this.logger.error("codex.app-server.restart_failed", { error: error instanceof Error ? error.name : "unknown" });
        // A failed spawn leaves the exited client in place; count it as another failure.
        // A failed initialize replaced the client, whose own exit reports itself.
        if (!this.closing && this.client === previous && previous !== undefined) this.handleExit(previous, generation, this.lastExit ?? exit);
      });
    }, delay);
  }

  /** Terminates the child (SIGTERM, SIGKILL after the grace period) and stops restarting. */
  async close(): Promise<void> {
    this.closing = true;
    if (this.restartTimer) { clearTimeout(this.restartTimer); this.restartTimer = undefined; }
    await this.starting?.catch(() => undefined);
    const client = this.client;
    this.state = "closed";
    if (client) await client.close().catch(() => undefined);
  }
}
