import { spawn } from 'node:child_process';
import { mkdtemp, readFile, rm, stat } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import path from 'node:path';
import { afterEach, describe, expect, it } from 'vitest';
import { createDesktopLogger } from '../../../electron/desktop-log';
import {
  MACOS_UNIX_SOCKET_PATH_MAX_BYTES,
  RUNTIME_SERVICE_CONFIG_SCHEMA,
  assertRuntimeSocketPathSupported,
  buildRuntimeServiceConfig,
  createRuntimeServiceHost,
  parseRuntimeServiceReadyLine,
  resolveRuntimeServicePaths,
  runtimeServiceArguments,
  writeRuntimeServiceConfig,
  type RuntimeServiceChild,
  type RuntimeServiceLaunchInput,
  type RuntimeServiceState
} from '../../../electron/runtime-service-host';

const FAKE_SERVICE = path.resolve(__dirname, 'fixtures', 'fake-runtime-service.mjs');
const temporaryRoots: string[] = [];
const hosts: Array<{ stop: () => Promise<void> }> = [];

afterEach(async () => {
  await Promise.all(hosts.splice(0).map((host) => host.stop()));
  await Promise.all(temporaryRoots.splice(0).map((root) => rm(root, { recursive: true, force: true })));
});

async function userData(): Promise<string> {
  const root = await mkdtemp(path.join(tmpdir(), 'chirality-svc-'));
  temporaryRoots.push(root);
  return root;
}

/** Test launcher: the same shape the Electron `utilityProcess` launcher provides. */
function createLauncher(extraEnv: Record<string, string> = {}) {
  const launches: RuntimeServiceLaunchInput[] = [];
  const launch = async (input: RuntimeServiceLaunchInput): Promise<RuntimeServiceChild> => {
    launches.push(input);
    const child = spawn(process.execPath, [input.entry, ...input.args], {
      env: { ...input.env, ...extraEnv } as unknown as NodeJS.ProcessEnv,
      stdio: ['ignore', 'pipe', 'pipe']
    });
    await new Promise<void>((resolve, reject) => {
      child.once('spawn', () => resolve());
      child.once('error', reject);
    });
    const exited = new Promise<{ code: number | null; signal: string | null }>((resolve) => {
      child.once('exit', (code, signal) => resolve({ code, signal }));
    });
    return {
      pid: child.pid as number,
      stdout: child.stdout,
      stderr: child.stderr,
      onExit: (listener) => {
        void exited.then(listener);
      },
      kill: (signal) => {
        child.kill(signal);
      }
    };
  };
  return { launch, launches };
}

async function fixture(options: {
  env?: Record<string, string>;
  hostOptions?: Partial<Parameters<typeof createRuntimeServiceHost>[0]>;
} = {}) {
  const root = await userData();
  const paths = resolveRuntimeServicePaths({ userDataDirectory: root, platform: 'linux' });
  const config = buildRuntimeServiceConfig({
    paths,
    instructionRoot: root,
    codexExecutablePath: path.join(root, 'codex'),
    userCodexHome: path.join(root, '.codex'),
    expectedCodexVersion: '0.154.0'
  });
  const launcher = createLauncher(options.env);
  const states: RuntimeServiceState[] = [];
  const logs: Array<{ level: string; event: string; detail?: unknown }> = [];
  const stderrLines: string[] = [];
  const host = createRuntimeServiceHost({
    config,
    configPath: paths.configPath,
    serviceEntry: FAKE_SERVICE,
    environment: {},
    launch: launcher.launch,
    log: (level, event, detail) => logs.push({ level, event, detail }),
    writeServiceStderr: (line) => stderrLines.push(line),
    onStateChange: (state) => states.push(state),
    readyTimeoutMs: 2_000,
    restartDelaysMs: [20, 40, 80],
    failureWindowMs: 60_000,
    maxFailures: 3,
    killGraceMs: 300,
    ...options.hostOptions
  });
  hosts.push(host);
  return { root, paths, config, launcher, states, logs, stderrLines, host };
}

/** Polls a sync or async predicate. */
async function waitFor(predicate: () => boolean | Promise<boolean>, timeoutMs = 5_000): Promise<void> {
  const deadline = Date.now() + timeoutMs;
  while (!(await predicate())) {
    if (Date.now() > deadline) throw new Error('condition not met in time');
    await new Promise((resolve) => setTimeout(resolve, 10));
  }
}

describe('runtime service paths and config', () => {
  it('places every private path under userData/runtime and enforces the macOS socket limit', () => {
    const paths = resolveRuntimeServicePaths({ userDataDirectory: '/Users/x/Library/Application Support/Chirality', platform: 'darwin' });
    expect(paths).toEqual({
      runtimeDirectory: '/Users/x/Library/Application Support/Chirality/runtime',
      socketPath: '/Users/x/Library/Application Support/Chirality/runtime/control.sock',
      clientTokenFile: '/Users/x/Library/Application Support/Chirality/runtime/client-token',
      configPath: '/Users/x/Library/Application Support/Chirality/runtime/service-config.json',
      effectiveHome: '/Users/x/Library/Application Support/Chirality/runtime/codex-home'
    });
    const tooLong = `/Users/${'x'.repeat(120)}`;
    expect(() => resolveRuntimeServicePaths({ userDataDirectory: tooLong, platform: 'darwin' })).toThrow(/macOS maximum is 103 bytes/);
    expect(() => resolveRuntimeServicePaths({ userDataDirectory: tooLong, platform: 'linux' })).not.toThrow();
    expect(assertRuntimeSocketPathSupported('/tmp/a.sock', 'darwin')).toEqual({ measuredBytes: 11, maximumBytes: MACOS_UNIX_SOCKET_PATH_MAX_BYTES });
    expect(resolveRuntimeServicePaths({ userDataDirectory: '/u', socketPathOverride: ' /tmp/iso/control.sock ', platform: 'darwin' }).socketPath).toBe('/tmp/iso/control.sock');
  });

  it('writes the chirality-app-owned/v1 config privately and atomically', async () => {
    const root = await userData();
    const paths = resolveRuntimeServicePaths({ userDataDirectory: root, platform: 'linux' });
    const config = buildRuntimeServiceConfig({
      paths,
      instructionRoot: '/opt/instruction-root',
      codexExecutablePath: '/opt/codex/bin/codex',
      userCodexHome: '/home/x/.codex',
      expectedCodexVersion: '0.154.0'
    });
    expect(config).toEqual({
      schema: RUNTIME_SERVICE_CONFIG_SCHEMA,
      socketPath: paths.socketPath,
      runtimeDirectory: paths.runtimeDirectory,
      instructionRoot: '/opt/instruction-root',
      clientTokenFile: paths.clientTokenFile,
      codex: {
        executablePath: '/opt/codex/bin/codex',
        userCodexHome: '/home/x/.codex',
        effectiveHome: paths.effectiveHome,
        expectedVersion: '0.154.0'
      }
    });
    await writeRuntimeServiceConfig(paths.configPath, config);
    await writeRuntimeServiceConfig(paths.configPath, config);
    expect(JSON.parse(await readFile(paths.configPath, 'utf8'))).toEqual(config);
    expect((await stat(paths.configPath)).mode & 0o777).toBe(0o600);
    expect((await stat(paths.runtimeDirectory)).mode & 0o777).toBe(0o700);
    expect(runtimeServiceArguments(paths.configPath)).toEqual(['daemon', '--config', paths.configPath]);
    expect(() => buildRuntimeServiceConfig({ ...{ paths, instructionRoot: 'relative', codexExecutablePath: '/c', userCodexHome: '/h', expectedCodexVersion: '1' } })).toThrow(/absolute/);
  });

  it('parses only the one ready line shape', () => {
    expect(parseRuntimeServiceReadyLine('{"ready":true,"role":"daemon","socketPath":"/s","clientTokenFile":"/t"}')).toEqual({
      ready: true, role: 'daemon', socketPath: '/s', clientTokenFile: '/t'
    });
    expect(parseRuntimeServiceReadyLine('{"ready":false}')).toBeNull();
    expect(parseRuntimeServiceReadyLine('{"ready":true,"socketPath":"/s"}')).toBeNull();
    expect(parseRuntimeServiceReadyLine('plain log line')).toBeNull();
    expect(parseRuntimeServiceReadyLine('{not json')).toBeNull();
  });
});

describe('runtime service host lifecycle', () => {
  it('spawns daemon --config, becomes ready on the ready line and stops with SIGTERM on teardown', async () => {
    const f = await fixture({ env: { FAKE_SERVICE_STDERR: 'signed in as owner@example.com (redact me)' } });
    const state = await f.host.start();
    expect(state.status).toBe('ready');
    expect(state.pid).toBeGreaterThan(0);
    expect(state.socketPath).toBe(f.paths.socketPath);
    expect(state.clientTokenFile).toBe(f.paths.clientTokenFile);
    expect(f.launcher.launches).toHaveLength(1);
    expect(f.launcher.launches[0]).toEqual({
      entry: FAKE_SERVICE,
      args: ['daemon', '--config', f.paths.configPath],
      env: {}
    });
    await waitFor(() => f.stderrLines.some((line) => line.includes('owner@example.com')));
    expect(f.stderrLines.some((line) => line.startsWith('fake service argv'))).toBe(true);

    await f.host.stop();
    expect(f.host.state().status).toBe('stopped');
    expect(f.host.state().lastExit?.code).toBe(0);
    expect(f.host.state().lastExit?.signal).toBeNull();
    await waitFor(() => f.stderrLines.includes('stopping on SIGTERM'));
    expect(f.logs.some((entry) => entry.event === 'runtime.service.sigkill')).toBe(false);
    // Teardown never restarts.
    await new Promise((resolve) => setTimeout(resolve, 150));
    expect(f.launcher.launches).toHaveLength(1);
  });

  it('escalates to SIGKILL after the grace period when the child ignores SIGTERM', async () => {
    const f = await fixture({ env: { FAKE_SERVICE_IGNORE_SIGTERM: '1' } });
    await f.host.start();
    await f.host.stop();
    // The child acknowledged SIGTERM and stayed alive, so the grace period ran out.
    expect(f.stderrLines).toContain('ignoring SIGTERM');
    expect(f.host.state().status).toBe('stopped');
    expect(f.host.state().lastExit?.signal).toBe('SIGKILL');
    expect(f.logs.some((entry) => entry.event === 'runtime.service.sigkill')).toBe(true);
    expect(f.launcher.launches).toHaveLength(1);
  });

  it('restarts an exited child with the backoff ladder and counts restarts', async () => {
    const f = await fixture({ env: { FAKE_SERVICE_EXIT_AFTER_MS: '60', FAKE_SERVICE_EXIT_CODE: '9' }, hostOptions: { maxFailures: 10 } });
    await f.host.start();
    await waitFor(() => f.host.state().restarts >= 2, 8_000);
    const scheduled = f.logs.filter((entry) => entry.event === 'runtime.service.restart_scheduled');
    expect(scheduled.length).toBeGreaterThanOrEqual(2);
    // Each ready resets the ladder, so a crash-after-ready always retries at rung one.
    expect(scheduled.map((entry) => (entry.detail as { delayMs: number }).delayMs)).toEqual(scheduled.map(() => 20));
    expect(f.states.some((state) => state.status === 'restarting' && state.lastExit?.code === 9)).toBe(true);
    expect(f.launcher.launches.length).toBeGreaterThanOrEqual(3);
  });

  it('walks the ladder for consecutive pre-ready failures and gives up after the failure budget', async () => {
    const f = await fixture({ env: { FAKE_SERVICE_MODE: 'exit-before-ready' } });
    const state = await f.host.start();
    expect(['restarting', 'failed']).toContain(state.status);
    await waitFor(() => f.host.state().status === 'failed', 8_000);
    const failed = f.host.state();
    expect(failed.recentFailures).toBe(3);
    expect(failed.pid).toBeNull();
    expect(failed.lastError).toMatch(/stopped after 3 failures within 60 s: exited with code 3 before ready/);
    const delays = f.logs
      .filter((entry) => entry.event === 'runtime.service.restart_scheduled')
      .map((entry) => (entry.detail as { delayMs: number }).delayMs);
    expect(delays).toEqual([20, 40]);
    expect(f.launcher.launches).toHaveLength(3);
    expect(f.logs.some((entry) => entry.event === 'runtime.service.gave_up')).toBe(true);
    // Nothing else is scheduled once the host gave up.
    await new Promise((resolve) => setTimeout(resolve, 200));
    expect(f.launcher.launches).toHaveLength(3);

    // The operator retry resets the budget and launches again.
    f.launcher.launches.length = 0;
    const retried = await f.host.restart();
    expect(['restarting', 'failed']).toContain(retried.status);
    expect(f.launcher.launches.length).toBeGreaterThanOrEqual(1);
  });

  it('treats a missing ready line as a failure, kills the child and schedules a restart', async () => {
    const f = await fixture({ env: { FAKE_SERVICE_MODE: 'never-ready' }, hostOptions: { readyTimeoutMs: 150, maxFailures: 2 } });
    const state = await f.host.start();
    expect(state.status).toBe('restarting');
    expect(state.lastError).toMatch(/no ready line within/);
    expect(f.logs.some((entry) => entry.event === 'runtime.service.ready_timeout')).toBe(true);
    await waitFor(() => f.host.state().status === 'failed', 8_000);
    expect(f.host.state().recentFailures).toBe(2);
  });

  it('replaces a live child on an operator restart and keeps a single owner', async () => {
    const f = await fixture();
    const first = await f.host.start();
    const restarted = await f.host.restart();
    expect(restarted.status).toBe('ready');
    expect(restarted.pid).not.toBe(first.pid);
    expect(f.launcher.launches).toHaveLength(2);
    // The replaced child's exit must not have scheduled a restart.
    expect(f.logs.filter((entry) => entry.event === 'runtime.service.restart_scheduled')).toHaveLength(0);
  });

  it('stops without launching anything when torn down before start', async () => {
    const f = await fixture();
    await f.host.stop();
    expect(f.host.state().status).toBe('stopped');
    expect(await f.host.start()).toMatchObject({ status: 'stopped' });
    expect(f.launcher.launches).toHaveLength(0);
  });

  it('records a launch failure as a restartable failure', async () => {
    const root = await userData();
    const paths = resolveRuntimeServicePaths({ userDataDirectory: root, platform: 'linux' });
    const config = buildRuntimeServiceConfig({ paths, instructionRoot: root, codexExecutablePath: path.join(root, 'codex'), userCodexHome: root, expectedCodexVersion: '0.154.0' });
    let attempts = 0;
    const host = createRuntimeServiceHost({
      config,
      configPath: paths.configPath,
      serviceEntry: FAKE_SERVICE,
      environment: {},
      launch: async () => {
        attempts += 1;
        throw new Error('spawn ENOENT');
      },
      restartDelaysMs: [10],
      maxFailures: 2,
      readyTimeoutMs: 500
    });
    hosts.push(host);
    const state = await host.start();
    expect(state.status).toBe('restarting');
    expect(state.lastError).toBe('launch failed: spawn ENOENT');
    await waitFor(() => host.state().status === 'failed');
    expect(attempts).toBe(2);
  });

  it('redacts account e-mails from service stderr at the desktop log writer', async () => {
    const root = await userData();
    const logger = createDesktopLogger({ directory: path.join(root, 'logs'), mirrorToConsole: false });
    const f = await fixture({
      env: { FAKE_SERVICE_STDERR: 'account/read -> owner.name+tag@example.co.uk plan pro' },
      hostOptions: { writeServiceStderr: (line) => logger.info('runtime.service.stderr', line) }
    });
    await f.host.start();
    await waitFor(async () => {
      const contents = await readFile(logger.filePath, 'utf8').catch(() => '');
      return contents.includes('account/read');
    });
    const contents = await readFile(logger.filePath, 'utf8');
    expect(contents).toContain('runtime.service.stderr account/read -> [redacted-email] plan pro');
    expect(contents).not.toContain('@example');
    expect(contents.split('\n').filter((line) => line.includes('@'))).toEqual([]);
  });
});
