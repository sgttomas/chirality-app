/**
 * App-owned Runtime service child (D-GOV-43, topology A2).
 *
 * One `chirality-runtime-service daemon --config <file>` process per running
 * App. The main process writes a private config file, launches the service as
 * a Node child of this Electron process, waits for its single ready line,
 * restarts it with bounded backoff when it exits unexpectedly, gives up after
 * a burst of failures, and stops it deliberately on quit. No LaunchAgent, no
 * second socket, no TCP.
 *
 * Kept free of `electron` imports: the launcher is a port supplied by the
 * caller (`runtime-service-launcher.ts` in production, `child_process` in
 * tests), so the whole lifecycle is checkable under plain Node with a fake
 * service script.
 */

import { chmod, mkdir, rename, rm, writeFile } from 'node:fs/promises';
import path from 'node:path';
import { createInterface } from 'node:readline';

export const MACOS_UNIX_SOCKET_PATH_MAX_BYTES = 103;

export function assertRuntimeSocketPathSupported(
  socketPath: string,
  platform: NodeJS.Platform = process.platform
): { measuredBytes: number; maximumBytes: number } {
  const measuredBytes = Buffer.byteLength(socketPath, 'utf8');
  if (platform === 'darwin' && measuredBytes > MACOS_UNIX_SOCKET_PATH_MAX_BYTES) {
    throw new Error(
      `Runtime control socket path is ${measuredBytes} UTF-8 bytes; macOS maximum is ${MACOS_UNIX_SOCKET_PATH_MAX_BYTES} bytes`
    );
  }
  return { measuredBytes, maximumBytes: MACOS_UNIX_SOCKET_PATH_MAX_BYTES };
}

export const RUNTIME_SERVICE_CONFIG_SCHEMA = 'chirality-app-owned/v1';
export const RUNTIME_SERVICE_SOCKET_NAME = 'control.sock';
export const RUNTIME_SERVICE_CLIENT_TOKEN_NAME = 'client-token';
export const RUNTIME_SERVICE_CONFIG_NAME = 'service-config.json';
export const RUNTIME_SERVICE_EFFECTIVE_HOME_NAME = 'codex-home';

export type RuntimeServiceConfig = {
  schema: typeof RUNTIME_SERVICE_CONFIG_SCHEMA;
  socketPath: string;
  runtimeDirectory: string;
  instructionRoot: string;
  productInstructionsPath?: string;
  clientTokenFile: string;
  codex: {
    executablePath: string;
    userCodexHome: string;
    effectiveHome: string;
    expectedVersion: string;
  };
};

export type RuntimeServicePaths = {
  runtimeDirectory: string;
  socketPath: string;
  clientTokenFile: string;
  configPath: string;
  effectiveHome: string;
};

/**
 * Every App-owned path lives under `<userData>/runtime`. The socket path may
 * be overridden (isolated verification runs) and is checked against the macOS
 * `sun_path` limit either way.
 */
export function resolveRuntimeServicePaths(input: {
  userDataDirectory: string;
  socketPathOverride?: string;
  platform?: NodeJS.Platform;
}): RuntimeServicePaths {
  const runtimeDirectory = path.join(path.resolve(input.userDataDirectory), 'runtime');
  const override = input.socketPathOverride?.trim();
  const socketPath = override ? path.resolve(override) : path.join(runtimeDirectory, RUNTIME_SERVICE_SOCKET_NAME);
  assertRuntimeSocketPathSupported(socketPath, input.platform);
  return {
    runtimeDirectory,
    socketPath,
    clientTokenFile: path.join(runtimeDirectory, RUNTIME_SERVICE_CLIENT_TOKEN_NAME),
    configPath: path.join(runtimeDirectory, RUNTIME_SERVICE_CONFIG_NAME),
    effectiveHome: path.join(runtimeDirectory, RUNTIME_SERVICE_EFFECTIVE_HOME_NAME)
  };
}

export function buildRuntimeServiceConfig(input: {
  paths: RuntimeServicePaths;
  instructionRoot: string;
  productInstructionsPath?: string;
  codexExecutablePath: string;
  userCodexHome: string;
  expectedCodexVersion: string;
}): RuntimeServiceConfig {
  for (const [label, value] of Object.entries({
    instructionRoot: input.instructionRoot,
    ...(input.productInstructionsPath === undefined ? {} : { productInstructionsPath: input.productInstructionsPath }),
    codexExecutablePath: input.codexExecutablePath,
    userCodexHome: input.userCodexHome
  })) {
    if (!path.isAbsolute(value)) {
      throw new Error(`Runtime service ${label} must be an absolute path`);
    }
  }
  return {
    schema: RUNTIME_SERVICE_CONFIG_SCHEMA,
    socketPath: input.paths.socketPath,
    runtimeDirectory: input.paths.runtimeDirectory,
    instructionRoot: path.resolve(input.instructionRoot),
    ...(input.productInstructionsPath === undefined ? {} : { productInstructionsPath: path.resolve(input.productInstructionsPath) }),
    clientTokenFile: input.paths.clientTokenFile,
    codex: {
      executablePath: path.resolve(input.codexExecutablePath),
      userCodexHome: path.resolve(input.userCodexHome),
      effectiveHome: input.paths.effectiveHome,
      expectedVersion: input.expectedCodexVersion
    }
  };
}

/** Write the config privately (directory 0700, file 0600) and atomically. */
export async function writeRuntimeServiceConfig(
  configPath: string,
  config: RuntimeServiceConfig
): Promise<void> {
  await mkdir(path.dirname(configPath), { recursive: true, mode: 0o700 });
  const pending = `${configPath}.${process.pid}.tmp`;
  await rm(pending, { force: true });
  await writeFile(pending, `${JSON.stringify(config, null, 2)}\n`, { encoding: 'utf8', mode: 0o600, flag: 'wx' });
  await chmod(pending, 0o600);
  await rename(pending, configPath);
  await chmod(configPath, 0o600);
}

export function runtimeServiceArguments(configPath: string): string[] {
  return ['daemon', '--config', configPath];
}

/** The one stdout line the service prints once it is listening. */
export type RuntimeServiceReadyLine = {
  ready: true;
  role: string;
  socketPath: string;
  clientTokenFile: string;
};

export function parseRuntimeServiceReadyLine(line: string): RuntimeServiceReadyLine | null {
  const trimmed = line.trim();
  if (!trimmed.startsWith('{')) return null;
  let parsed: unknown;
  try {
    parsed = JSON.parse(trimmed);
  } catch {
    return null;
  }
  if (typeof parsed !== 'object' || parsed === null) return null;
  const record = parsed as Record<string, unknown>;
  if (record.ready !== true) return null;
  if (typeof record.socketPath !== 'string' || typeof record.clientTokenFile !== 'string') return null;
  return {
    ready: true,
    role: typeof record.role === 'string' ? record.role : 'daemon',
    socketPath: record.socketPath,
    clientTokenFile: record.clientTokenFile
  };
}

/** A launched service child, already spawned (pid known). */
export type RuntimeServiceChild = {
  readonly pid: number;
  readonly stdout: NodeJS.ReadableStream | null;
  readonly stderr: NodeJS.ReadableStream | null;
  /** Invoked exactly once when the child exits. */
  onExit(listener: (exit: { code: number | null; signal: string | null }) => void): void;
  kill(signal: 'SIGTERM' | 'SIGKILL'): void;
};

export type RuntimeServiceLaunchInput = {
  entry: string;
  args: string[];
  env: Record<string, string>;
};

/** Resolves once the child has spawned; rejects when it could not be spawned. */
export type RuntimeServiceLauncher = (input: RuntimeServiceLaunchInput) => Promise<RuntimeServiceChild>;

export type RuntimeServiceStatus =
  | 'idle'
  | 'starting'
  | 'ready'
  | 'restarting'
  | 'stopping'
  | 'stopped'
  | 'failed';

export type RuntimeServiceState = {
  status: RuntimeServiceStatus;
  pid: number | null;
  socketPath: string;
  clientTokenFile: string;
  /** Successful (ready) launches after the first one. */
  restarts: number;
  /** Failures inside the current give-up window. */
  recentFailures: number;
  lastExit: { code: number | null; signal: string | null; at: string } | null;
  lastError: string | null;
  nextRestartAt: string | null;
  changedAt: string;
};

export const DEFAULT_READY_TIMEOUT_MS = 30_000;
export const DEFAULT_RESTART_DELAYS_MS: readonly number[] = [1_000, 2_000, 4_000, 8_000, 16_000, 30_000];
export const DEFAULT_FAILURE_WINDOW_MS = 180_000;
export const DEFAULT_MAX_FAILURES = 5;
/**
 * SIGTERM to SIGKILL grace for the service. It exceeds the service's own worst-case
 * close budget (turn interrupt grace 3 s, daemon stop 2.5 s, app-server kill grace 2 s)
 * so a slow supplier is settled by the service, never hard-killed mid-settlement.
 */
export const DEFAULT_KILL_GRACE_MS = 10_000;

export type RuntimeServiceHostOptions = {
  config: RuntimeServiceConfig;
  configPath: string;
  serviceEntry: string;
  environment: Record<string, string>;
  launch: RuntimeServiceLauncher;
  log?: (level: 'info' | 'warn' | 'error', event: string, detail?: unknown) => void;
  /** Receives every service stderr line; the desktop log redacts at its writer. */
  writeServiceStderr?: (line: string) => void;
  onStateChange?: (state: RuntimeServiceState) => void;
  readyTimeoutMs?: number;
  restartDelaysMs?: readonly number[];
  failureWindowMs?: number;
  maxFailures?: number;
  killGraceMs?: number;
  setTimeoutFn?: (handler: () => void, delayMs: number) => unknown;
  clearTimeoutFn?: (handle: unknown) => void;
  now?: () => Date;
};

export type RuntimeServiceHost = {
  /**
   * Write the config and launch. Resolves once the first attempt has settled
   * (ready, or failed with a restart scheduled or the budget exhausted); it
   * never rejects because of the child, only because the config could not be
   * written.
   */
  start(): Promise<RuntimeServiceState>;
  /** Operator retry: reset the failure budget and launch again (replacing a live child). */
  restart(): Promise<RuntimeServiceState>;
  /** Teardown: SIGTERM, then SIGKILL after the grace period. Never restarts afterwards. */
  stop(): Promise<void>;
  state(): RuntimeServiceState;
};

type LaunchOutcome = { ready: true } | { ready: false; reason: string };

export function createRuntimeServiceHost(options: RuntimeServiceHostOptions): RuntimeServiceHost {
  const readyTimeoutMs = options.readyTimeoutMs ?? DEFAULT_READY_TIMEOUT_MS;
  const restartDelaysMs =
    options.restartDelaysMs && options.restartDelaysMs.length > 0
      ? options.restartDelaysMs
      : DEFAULT_RESTART_DELAYS_MS;
  const failureWindowMs = options.failureWindowMs ?? DEFAULT_FAILURE_WINDOW_MS;
  const maxFailures = options.maxFailures ?? DEFAULT_MAX_FAILURES;
  const killGraceMs = options.killGraceMs ?? DEFAULT_KILL_GRACE_MS;
  const schedule = options.setTimeoutFn ?? ((handler, delayMs) => setTimeout(handler, delayMs));
  const cancel = options.clearTimeoutFn ?? ((handle: unknown) => clearTimeout(handle as NodeJS.Timeout));
  const now = options.now ?? (() => new Date());
  const log = options.log ?? (() => undefined);
  const writeStderr = options.writeServiceStderr ?? (() => undefined);

  let state: RuntimeServiceState = {
    status: 'idle',
    pid: null,
    socketPath: options.config.socketPath,
    clientTokenFile: options.config.clientTokenFile,
    restarts: 0,
    recentFailures: 0,
    lastExit: null,
    lastError: null,
    nextRestartAt: null,
    changedAt: now().toISOString()
  };
  let child: RuntimeServiceChild | undefined;
  let childExited: Promise<{ code: number | null; signal: string | null }> | undefined;
  let stopping = false;
  let restartTimer: unknown;
  let consecutiveFailures = 0;
  const failureTimestamps: number[] = [];
  let readyCount = 0;
  let launchGeneration = 0;

  const publish = (patch: Partial<RuntimeServiceState>): void => {
    state = { ...state, ...patch, changedAt: now().toISOString() };
    options.onStateChange?.(state);
  };

  const clearRestartTimer = (): void => {
    if (restartTimer !== undefined) {
      cancel(restartTimer);
      restartTimer = undefined;
    }
  };

  const delay = (ms: number): Promise<void> =>
    new Promise((resolve) => {
      schedule(resolve, ms);
    });

  const recordFailure = (): { giveUp: boolean } => {
    const at = now().getTime();
    failureTimestamps.push(at);
    while (failureTimestamps.length > 0 && at - failureTimestamps[0] > failureWindowMs) {
      failureTimestamps.shift();
    }
    consecutiveFailures += 1;
    return { giveUp: failureTimestamps.length >= maxFailures };
  };

  const scheduleRestart = (reason: string): void => {
    const { giveUp } = recordFailure();
    if (giveUp) {
      log('error', 'runtime.service.gave_up', {
        failures: failureTimestamps.length,
        windowMs: failureWindowMs,
        reason
      });
      publish({
        status: 'failed',
        pid: null,
        recentFailures: failureTimestamps.length,
        lastError: `Runtime service stopped after ${failureTimestamps.length} failures within ${Math.round(failureWindowMs / 1000)} s: ${reason}`,
        nextRestartAt: null
      });
      return;
    }
    const delayMs = restartDelaysMs[Math.min(consecutiveFailures - 1, restartDelaysMs.length - 1)];
    const nextRestartAt = new Date(now().getTime() + delayMs).toISOString();
    log('warn', 'runtime.service.restart_scheduled', { delayMs, attempt: consecutiveFailures, reason });
    publish({
      status: 'restarting',
      pid: null,
      recentFailures: failureTimestamps.length,
      lastError: reason,
      nextRestartAt
    });
    clearRestartTimer();
    restartTimer = schedule(() => {
      restartTimer = undefined;
      if (stopping) return;
      void launchOnce();
    }, delayMs);
  };

  const terminateChild = async (target: RuntimeServiceChild, exited: Promise<unknown>): Promise<void> => {
    let done = false;
    void exited.then(() => {
      done = true;
    });
    try {
      target.kill('SIGTERM');
    } catch {
      // Already gone.
    }
    await Promise.race([exited, delay(killGraceMs)]);
    if (!done) {
      log('warn', 'runtime.service.sigkill', { pid: target.pid, graceMs: killGraceMs });
      try {
        target.kill('SIGKILL');
      } catch {
        // Already gone.
      }
      await Promise.race([exited, delay(killGraceMs)]);
    }
  };

  const attachOutput = (
    target: RuntimeServiceChild,
    onReady: (line: RuntimeServiceReadyLine) => void
  ): void => {
    let readySeen = false;
    if (target.stdout) {
      createInterface({ input: target.stdout }).on('line', (line) => {
        if (!readySeen) {
          const parsed = parseRuntimeServiceReadyLine(line);
          if (parsed) {
            readySeen = true;
            onReady(parsed);
            return;
          }
        }
        if (line.trim().length > 0) log('info', 'runtime.service.stdout', line);
      });
    }
    if (target.stderr) {
      createInterface({ input: target.stderr }).on('line', (line) => {
        if (line.trim().length > 0) writeStderr(line);
      });
    }
  };

  async function launchOnce(): Promise<LaunchOutcome> {
    if (stopping) return { ready: false, reason: 'stopping' };
    const generation = ++launchGeneration;
    publish({ status: consecutiveFailures > 0 || readyCount > 0 ? 'restarting' : 'starting', pid: null, nextRestartAt: null });
    let launched: RuntimeServiceChild;
    try {
      launched = await options.launch({
        entry: options.serviceEntry,
        args: runtimeServiceArguments(options.configPath),
        env: options.environment
      });
    } catch (error) {
      const reason = `launch failed: ${error instanceof Error ? error.message : String(error)}`;
      log('error', 'runtime.service.launch_failed', { reason });
      if (!stopping) scheduleRestart(reason);
      return { ready: false, reason };
    }
    if (generation !== launchGeneration || stopping) {
      // A restart or teardown overtook this launch while it was spawning.
      const exited = new Promise<{ code: number | null; signal: string | null }>((resolve) => launched.onExit(resolve));
      await terminateChild(launched, exited);
      return { ready: false, reason: 'superseded' };
    }
    child = launched;
    const exited = new Promise<{ code: number | null; signal: string | null }>((resolve) => launched.onExit(resolve));
    childExited = exited;
    log('info', 'runtime.service.spawned', { pid: launched.pid, entry: options.serviceEntry });
    publish({ pid: launched.pid });

    let readyResolve!: (outcome: LaunchOutcome) => void;
    const settled = new Promise<LaunchOutcome>((resolve) => {
      readyResolve = resolve;
    });
    let settledFlag = false;
    const settle = (outcome: LaunchOutcome): void => {
      if (settledFlag) return;
      settledFlag = true;
      readyResolve(outcome);
    };

    attachOutput(launched, (line) => {
      readyCount += 1;
      consecutiveFailures = 0;
      log('info', 'runtime.service.ready', {
        pid: launched.pid,
        socketPath: line.socketPath,
        clientTokenFile: line.clientTokenFile,
        role: line.role
      });
      publish({
        status: 'ready',
        pid: launched.pid,
        socketPath: line.socketPath,
        clientTokenFile: line.clientTokenFile,
        restarts: Math.max(0, readyCount - 1),
        lastError: null,
        nextRestartAt: null
      });
      settle({ ready: true });
    });

    let timeoutReason: string | undefined;
    const readyTimer = schedule(() => {
      if (settledFlag || stopping) return;
      log('error', 'runtime.service.ready_timeout', { pid: launched.pid, timeoutMs: readyTimeoutMs });
      timeoutReason = `no ready line within ${Math.round(readyTimeoutMs / 1000)} s`;
      settle({ ready: false, reason: timeoutReason });
      void terminateChild(launched, exited);
    }, readyTimeoutMs);

    void exited.then((exit) => {
      cancel(readyTimer);
      if (child === launched) {
        child = undefined;
        childExited = undefined;
      }
      const at = now().toISOString();
      const wasReady = state.status === 'ready' && state.pid === launched.pid;
      if (stopping) {
        log('info', 'runtime.service.exited', { pid: launched.pid, ...exit, expected: true });
        publish({ status: 'stopped', pid: null, lastExit: { ...exit, at }, nextRestartAt: null });
        settle({ ready: false, reason: 'stopped' });
        return;
      }
      if (generation !== launchGeneration) {
        // Replaced by an operator restart; the new launch owns the state.
        return;
      }
      const reason = timeoutReason
        ?? `exited with ${exit.signal ? `signal ${exit.signal}` : `code ${String(exit.code)}`}${wasReady ? '' : ' before ready'}`;
      log('error', 'runtime.service.exited', { pid: launched.pid, ...exit, expected: false, wasReady });
      publish({ lastExit: { ...exit, at } });
      settle({ ready: false, reason });
      scheduleRestart(reason);
    });

    const outcome = await settled;
    if (!outcome.ready && outcome.reason.startsWith('no ready line')) {
      // The exit handler runs after the kill; give it a chance to schedule the
      // restart so the caller observes a settled state.
      await exited;
    }
    return outcome;
  }

  return {
    async start(): Promise<RuntimeServiceState> {
      if (stopping) return state;
      await writeRuntimeServiceConfig(options.configPath, options.config);
      log('info', 'runtime.service.config_written', { configPath: options.configPath });
      await launchOnce();
      return state;
    },
    async restart(): Promise<RuntimeServiceState> {
      if (stopping) return state;
      clearRestartTimer();
      failureTimestamps.length = 0;
      consecutiveFailures = 0;
      const previous = child;
      const previousExit = childExited;
      launchGeneration += 1;
      if (previous && previousExit) {
        child = undefined;
        childExited = undefined;
        log('info', 'runtime.service.restart_requested', { pid: previous.pid });
        await terminateChild(previous, previousExit);
      } else {
        log('info', 'runtime.service.restart_requested', { pid: null });
      }
      await writeRuntimeServiceConfig(options.configPath, options.config);
      await launchOnce();
      return state;
    },
    async stop(): Promise<void> {
      if (stopping) return;
      stopping = true;
      clearRestartTimer();
      const target = child;
      const exited = childExited;
      publish({ status: 'stopping', nextRestartAt: null });
      if (target && exited) {
        log('info', 'runtime.service.stopping', { pid: target.pid });
        await terminateChild(target, exited);
      }
      child = undefined;
      childExited = undefined;
      if (state.status !== 'stopped') {
        publish({ status: 'stopped', pid: null });
      }
    },
    state: () => state
  };
}
