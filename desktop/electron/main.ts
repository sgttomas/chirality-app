import { PLAN_EXPORT_DIALOG_CHANNEL } from './plan-export-ipc-contract';
import { createPlanExportDialogHandler } from './plan-export-dialog';
import { app, BrowserWindow, dialog, ipcMain, shell, Menu } from 'electron';
import { isAuthorizedSender } from './ipc-sender-policy';
import { createDocumentHandoffHandler, validateRevealRoot, FilePolicyError } from '../src/app/api/working-root/file/file-policy';
import { existsSync, mkdirSync, readFileSync } from 'node:fs';
import { mkdir, readFile, stat, writeFile } from 'node:fs/promises';
import { createServer, type IncomingMessage, type ServerResponse } from 'node:http';
import type { AddressInfo } from 'node:net';
import os from 'node:os';
import path from 'node:path';
import { RuntimeClient } from '@chirality/runtime-client';
import { registerApiKeyHandlers, unregisterApiKeyHandlers } from './api-key-ipc';
import { buildApplicationMenuTemplate } from './application-menu';
import {
  createAppUpdateController,
  createPolicyGuardedFetch,
  startAppUpdatePolling,
  type AppUpdateController
} from './app-update';
import {
  APP_ABOUT_SHOW_CHANNEL,
  APP_UPDATE_CHANGED_CHANNEL,
  APP_UPDATE_CHECK_CHANNEL,
  APP_UPDATE_GET_CHANNEL,
  APP_UPDATE_OPEN_DOWNLOAD_CHANNEL,
  type AppUpdateState
} from './app-update-ipc-contract';
import { APP_UPDATE_ALLOWED_FEED_HOSTS, resolveAppUpdateSource } from './app-update-source';
import { PRODUCT_INSTRUCTIONS_CHANNEL } from './product-instructions-ipc-contract';
import { createProductInstructionsHandler, createProductInstructionsStore, resolveProductInstructionsDefault } from './product-instructions';
import { ATTACHMENT_SELECT_FILES_CHANNEL } from './attachment-ipc-contract';
import { createAttachmentSelectionHandler } from './attachment-picker';
import { CODEX_PINNED_VERSION, resolveCodexExecutable } from './codex-executable';
import {
  createDesktopLogger,
  createNoopDesktopLogger,
  type DesktopLogger
} from './desktop-log';
import { resolveUserDataOverride } from './desktop-process-policy';
import {
  applyPackagedRendererRequestPolicy,
  buildRendererContentSecurityPolicy,
  installRendererWindowPolicy,
  rendererWebPreferences,
  runEgressLayerProbe,
  runRendererSecurityProbe
} from './renderer-window-policy';
import {
  createRuntimeBindingSupervisor,
  RUNTIME_CONNECTIVITY_CHANGED_CHANNEL,
  RUNTIME_CONNECTIVITY_QUERY_CHANNEL,
  type RuntimeBindingSupervisor,
  type RuntimeConnectivitySnapshot
} from './runtime-connectivity';
import {
  registerRuntimeControlHandlers,
  unregisterRuntimeControlHandlers
} from './runtime-control-ipc';
import {
  buildRuntimeServiceConfig,
  createRuntimeServiceHost,
  resolveRuntimeServicePaths,
  type RuntimeServiceHost,
  type RuntimeServiceState
} from './runtime-service-host';
import { launchRuntimeServiceChild } from './runtime-service-launcher';
import {
  createSocketPresenceWatcher,
  type SocketPresenceWatcher
} from './runtime-socket-watch';
import { shouldPreventNativeQuit } from './runtime-shutdown-policy';
import { bindStableRendererServer } from './renderer-server-port';

type RendererServer = {
  close: () => Promise<void>;
  url: string;
};

type RendererProbeResult = {
  url: string;
  ok: boolean;
  status: number | null;
  type: string | null;
  error: string | null;
};

/** What the renderer receives: daemon reachability plus the owned child's state. */
type RuntimeConnectivityReport = RuntimeConnectivitySnapshot & {
  service: RuntimeServiceState | null;
};

const SELECT_DIRECTORY_CHANNEL = 'chirality:select-directory';
const FOLDER_REGISTER_RECENT_CHANNEL = 'chirality:folder-register-recent';
const FOLDER_OPEN_READY_CHANNEL = 'chirality:folder-open-ready';
const FOLDER_OPEN_INTENT_CHANNEL = 'chirality:folder-open-intent';
let pendingFolderIntent: string | undefined;
let folderIntentGeneration = 0;
let folderIntentReceiver: import('electron').WebContents | undefined;
let folderIntentOrigin: string | undefined;
let folderIntentRendererUrl: string | undefined;

export async function registerRecentFolder(event: import('./ipc-sender-policy').IpcSenderEvent, input: unknown,
  rendererOrigin: string, instructionRoot: string, register: (root: string) => void = root => app.addRecentDocument(root)
): Promise<{ ok: true } | { ok: false; error: string }> {
  if (!isAuthorizedSender(event, rendererOrigin)) return { ok: false, error: 'Unauthorized folder request.' };
  try {
    const root = await validateRevealRoot({ projectRoot: input }, instructionRoot);
    register(root);
    return { ok: true };
  } catch (error) { return { ok: false, error: error instanceof Error ? error.message : 'Unable to register folder.' }; }
}

async function deliverFolderIntent(): Promise<void> {
  const receiver = folderIntentReceiver;
  if (!receiver || receiver.isDestroyed() || !folderIntentOrigin || !pendingFolderIntent) return;
  if (!isAuthorizedSender({ senderFrame: { url: receiver.getURL() } }, folderIntentOrigin)) return;
  const generation = folderIntentGeneration;
  const requested = pendingFolderIntent;
  pendingFolderIntent = undefined;
  try {
    const root = await validateRevealRoot({ projectRoot: requested }, resolveInstructionRootForProcess());
    if (generation === folderIntentGeneration && receiver === folderIntentReceiver && !receiver.isDestroyed() && isAuthorizedSender({ senderFrame: { url: receiver.getURL() } }, folderIntentOrigin)) receiver.send(FOLDER_OPEN_INTENT_CHANNEL, { path: root });
  } catch (error) {
    if (generation === folderIntentGeneration && receiver === folderIntentReceiver && !receiver.isDestroyed() && isAuthorizedSender({ senderFrame: { url: receiver.getURL() } }, folderIntentOrigin)) receiver.send(FOLDER_OPEN_INTENT_CHANNEL, { error: error instanceof Error ? error.message : 'Unable to open this folder.' });
  }
}

const RUNTIME_NETWORK_POLICY_ID = 'REQ-NET-001';
const DEFAULT_RENDERER_PROBE_DELAY_MS = 1500;
const DEFAULT_RENDERER_PROBE_TIMEOUT_MS = 8000;

const ALLOWED_ANTHROPIC_API_HOSTNAMES = new Set<string>(['api.anthropic.com']);
const ALLOWED_LOOPBACK_HOSTNAMES = new Set<string>(['localhost', '127.0.0.1', '[::1]']);
const RENDERER_EGRESS_FILTER_URLS = ['http://*/*', 'https://*/*', 'ws://*/*', 'wss://*/*'];

let rendererServer: RendererServer | undefined;
let runtimeServiceHost: RuntimeServiceHost | undefined;
let shutdownStarted = false;
let shutdownCompleted = false;
let bindingSupervisor: RuntimeBindingSupervisor | undefined;
let socketWatcher: SocketPresenceWatcher | undefined;
let desktopLogger: DesktopLogger = createNoopDesktopLogger();
let appUpdateController: AppUpdateController | undefined;
let unsubscribeAppUpdate: (() => void) | undefined;
let stopAppUpdatePolling: (() => void) | undefined;

/**
 * Honor `CHIRALITY_USER_DATA` for the app itself.
 *
 * The App-owned Runtime service resolves every private path from the App's
 * `userData`, so one variable pins the App, its service child and its Codex
 * effective home to one isolated root, which is what lets a verification run
 * drive a fully isolated App without touching an operator's real userData.
 *
 * Must run before anything reads `app.getPath('userData')` and before `ready`,
 * because the value also selects the Chromium profile directory. Relative values
 * are rejected rather than resolved against an unpredictable cwd. `app.setPath`
 * throws when the directory is absent, so create it first. Applies to packaged
 * and unpackaged runs alike.
 */
function applyUserDataOverride(): void {
  const override = resolveUserDataOverride(process.env);
  if (override.kind === 'absent') {
    return;
  }
  if (override.kind === 'rejected') {
    console.warn(
      'Ignoring CHIRALITY_USER_DATA because it is not an absolute path',
      JSON.stringify({ requested: override.requested })
    );
    return;
  }
  try {
    mkdirSync(override.directory, { recursive: true, mode: 0o700 });
    app.setPath('userData', override.directory);
  } catch (error) {
    console.error(
      'Failed to apply CHIRALITY_USER_DATA override',
      error instanceof Error ? error.message : String(error)
    );
  }
}

applyUserDataOverride();

type RendererEgressPolicyDecision =
  | { allowed: true }
  | { allowed: false; category: 'INVALID_URL' | 'NETWORK_POLICY_VIOLATION'; reason: string };

type RendererRequestDestination = {
  hostname: string;
  port: string | null;
  protocol: string;
};

function isAllowedLoopbackHostname(hostname: string): boolean {
  return ALLOWED_LOOPBACK_HOSTNAMES.has(hostname.toLowerCase());
}

function summarizeRendererRequestDestination(rawUrl: string): RendererRequestDestination | null {
  try {
    const parsed = new URL(rawUrl);
    return {
      hostname: parsed.hostname,
      port: parsed.port || null,
      protocol: parsed.protocol
    };
  } catch {
    return null;
  }
}

function resolveAppVersion(): string {
  if (app.isPackaged) return app.getVersion();
  // `electron dist-electron/main.js` makes dist-electron the app path; the
  // frontend package.json sits one level up.
  const appPath = app.getAppPath();
  for (const directory of [appPath, path.dirname(appPath)]) {
    try {
      const parsed = JSON.parse(readFileSync(path.join(directory, 'package.json'), 'utf8')) as { name?: unknown; version?: unknown };
      if (parsed.name === 'chirality-frontend' && typeof parsed.version === 'string' && parsed.version.length > 0) return parsed.version;
    } catch { /* try the next candidate, then fall back to the Electron-reported version */ }
  }
  return app.getVersion();
}

function parsePositiveInteger(raw: string | undefined, fallback: number): number {
  const parsed = Number.parseInt(raw ?? '', 10);
  if (!Number.isSafeInteger(parsed) || parsed <= 0) {
    return fallback;
  }
  return parsed;
}

function readRendererProbeUrls(): string[] {
  const raw = process.env.CHIRALITY_NETWORK_POLICY_PROBE_URLS?.trim();
  if (!raw) {
    return [];
  }

  return raw
    .split(',')
    .map((value) => value.trim())
    .filter((value) => value.length > 0);
}

function evaluateRendererEgressPolicy(rawUrl: string): RendererEgressPolicyDecision {
  let parsed: URL;
  try {
    parsed = new URL(rawUrl);
  } catch {
    return {
      allowed: false,
      category: 'INVALID_URL',
      reason: 'url_parse_failed'
    };
  }

  const hostname = parsed.hostname.toLowerCase();
  if (ALLOWED_ANTHROPIC_API_HOSTNAMES.has(hostname)) {
    if (parsed.protocol !== 'https:') {
      return {
        allowed: false,
        category: 'NETWORK_POLICY_VIOLATION',
        reason: `anthropic_protocol_not_allowlisted:${parsed.protocol}`
      };
    }

    if (parsed.port !== '' && parsed.port !== '443') {
      return {
        allowed: false,
        category: 'NETWORK_POLICY_VIOLATION',
        reason: `anthropic_port_not_allowlisted:${parsed.port}`
      };
    }

    return { allowed: true };
  }

  if (isAllowedLoopbackHostname(hostname)) {
    return { allowed: true };
  }

  return {
    allowed: false,
    category: 'NETWORK_POLICY_VIOLATION',
    reason: `host_not_allowlisted:${hostname}`
  };
}

function registerRendererEgressPolicy(window: BrowserWindow): void {
  window.webContents.session.webRequest.onBeforeRequest(
    { urls: RENDERER_EGRESS_FILTER_URLS },
    (details, callback) => {
      const decision = evaluateRendererEgressPolicy(details.url);
      if (decision.allowed) {
        callback({ cancel: false });
        return;
      }

      console.warn('Blocked renderer outbound request by network policy', {
        category: decision.category,
        policy: RUNTIME_NETWORK_POLICY_ID,
        reason: decision.reason,
        destination: summarizeRendererRequestDestination(details.url),
        method: details.method,
        resourceType: details.resourceType,
        webContentsId: details.webContentsId
      });

      callback({ cancel: true });
    }
  );
}

async function runRendererNetworkProbe(window: BrowserWindow): Promise<void> {
  const urls = readRendererProbeUrls();
  if (urls.length === 0) {
    return;
  }

  const delayMs = parsePositiveInteger(
    process.env.CHIRALITY_NETWORK_POLICY_PROBE_DELAY_MS,
    DEFAULT_RENDERER_PROBE_DELAY_MS
  );
  const timeoutMs = parsePositiveInteger(
    process.env.CHIRALITY_NETWORK_POLICY_PROBE_TIMEOUT_MS,
    DEFAULT_RENDERER_PROBE_TIMEOUT_MS
  );

  const runProbe = async (): Promise<void> => {
    const script = `
(() => {
  const urls = ${JSON.stringify(urls)};
  const timeoutMs = ${timeoutMs};
  const run = async () => {
    const results = [];
    for (const url of urls) {
      const controller = new AbortController();
      const timer = setTimeout(() => controller.abort(), timeoutMs);
      try {
        const response = await fetch(url, {
          method: 'GET',
          mode: 'no-cors',
          cache: 'no-store',
          signal: controller.signal
        });
        results.push({
          url,
          ok: true,
          status: typeof response?.status === 'number' ? response.status : null,
          type: typeof response?.type === 'string' ? response.type : null,
          error: null
        });
      } catch (error) {
        const errorMessage = error instanceof Error ? error.message : String(error);
        results.push({
          url,
          ok: false,
          status: null,
          type: null,
          error: errorMessage
        });
      } finally {
        clearTimeout(timer);
      }
    }
    return results;
  };
  return run();
})();
`;

    try {
      const results = (await window.webContents.executeJavaScript(script, true)) as RendererProbeResult[];
      console.info(
        '[network-policy-probe]',
        JSON.stringify({
          policy: RUNTIME_NETWORK_POLICY_ID,
          results
        })
      );
    } catch (error) {
      console.error(
        '[network-policy-probe]',
        JSON.stringify({
          policy: RUNTIME_NETWORK_POLICY_ID,
          error: error instanceof Error ? error.message : String(error)
        })
      );
    }
  };

  const scheduleProbe = (): void => {
    setTimeout(() => {
      void runProbe();
    }, delayMs);
  };

  if (window.webContents.isLoadingMainFrame()) {
    window.webContents.once('did-finish-load', scheduleProbe);
  } else {
    scheduleProbe();
  }
}

function resolveInstructionRootForProcess(): string {
  const envOverride = process.env.CHIRALITY_INSTRUCTION_ROOT?.trim();
  if (envOverride) {
    return path.resolve(envOverride);
  }

  if (app.isPackaged) {
    return path.resolve(process.resourcesPath);
  }

  const candidates: string[] = [];
  for (const start of [process.cwd(), __dirname]) {
    let candidate = path.resolve(start);
    for (;;) {
      candidates.push(candidate);
      const parent = path.dirname(candidate);
      if (parent === candidate) break;
      candidate = parent;
    }
  }
  const resolved = candidates.find(
    (candidate) =>
      existsSync(path.join(candidate, 'agents')) &&
      existsSync(path.join(candidate, 'AGENTS.md')) &&
      existsSync(path.join(candidate, 'docs', 'DIRECTIVE.md'))
  );
  if (resolved === undefined) {
    throw new Error('Unable to resolve the Chirality instruction root');
  }
  return resolved;
}

/** The instruction root handed to the Runtime service (packaged: the staged bundle). */
function resolveServiceInstructionRoot(): string {
  return app.isPackaged
    ? path.join(process.resourcesPath, 'instruction-root')
    : resolveInstructionRootForProcess();
}

/** Development frontend root: `dist-electron/main.js` sits one level below it. */
function resolveFrontendRoot(): string {
  return path.resolve(__dirname, '..');
}

/**
 * Service entry: development uses the built Runtime workspace
 * (`tsc -b` output); the packaged App carries the esbuild bundle produced by
 * `scripts/build-electron.mjs` under `Contents/Resources/runtime-service`.
 */
function resolveRuntimeServiceEntry(): string {
  const override = process.env.CHIRALITY_RUNTIME_SERVICE_ENTRY?.trim();
  if (override) return path.resolve(override);
  if (app.isPackaged) {
    return path.join(process.resourcesPath, 'runtime-service', 'standalone-bin.mjs');
  }
  return path.resolve(
    resolveFrontendRoot(),
    '..',
    '..',
    'chirality-runtime',
    'packages',
    'daemon',
    'dist',
    'standalone-bin.js'
  );
}

function resolveUserCodexHome(): string {
  const override = process.env.CODEX_HOME?.trim();
  return override ? path.resolve(override) : path.join(os.homedir(), '.codex');
}

/** The child's environment: this process's, without Electron-only switches. */
function runtimeServiceEnvironment(): Record<string, string> {
  const environment: Record<string, string> = {};
  for (const [name, value] of Object.entries(process.env)) {
    if (value === undefined) continue;
    if (name === 'ELECTRON_RUN_AS_NODE' || name === 'NODE_OPTIONS') continue;
    environment[name] = value;
  }
  return environment;
}

export function createDirectorySelectionHandler(
  preferencePath: string,
  homePath: string,
  showOpenDialog: typeof dialog.showOpenDialog = dialog.showOpenDialog
): () => Promise<{ cancelled: boolean; path?: string; error?: string }> {
  let lastSelectedPath: string | undefined;
  return async () => {
    if (!lastSelectedPath) {
      try {
        const stored: unknown = JSON.parse(await readFile(preferencePath, 'utf8'));
        if (typeof stored === 'string' && path.isAbsolute(stored)) lastSelectedPath = stored;
      } catch { /* A missing or unreadable preference starts at home. */ }
    }
    let defaultPath = homePath;
    if (lastSelectedPath) {
      try { if ((await stat(lastSelectedPath)).isDirectory()) defaultPath = lastSelectedPath; } catch { /* The remembered folder may have moved. */ }
    }
    // The folder picker is the project-preparation moment: choosing a folder is
    // the whole of "creating a project" for the operator.
    const dialogResult = await showOpenDialog({
      defaultPath,
      title: 'Choose a project folder',
      buttonLabel: 'Use this folder',
      message: 'Chirality will work in this folder and add a chirality.project.json file if one is missing.',
      properties: ['openDirectory', 'createDirectory']
    });

    if (dialogResult.canceled || dialogResult.filePaths.length === 0) {
      return { cancelled: true };
    }

    const selectedPath = path.resolve(dialogResult.filePaths[0]);

    try {
      const selectedStat = await stat(selectedPath);
      if (!selectedStat.isDirectory()) {
        return {
          cancelled: true,
          error: 'Selected path is not a directory'
        };
      }
    } catch {
      return {
        cancelled: true,
        error: 'Selected path is not accessible'
      };
    }

    lastSelectedPath = selectedPath;
    try {
      await mkdir(path.dirname(preferencePath), { recursive: true });
      await writeFile(preferencePath, JSON.stringify(selectedPath), { mode: 0o600 });
    } catch { /* Selection still succeeds if only preference persistence fails. */ }
    return {
      cancelled: false,
      path: selectedPath
    };
  };
}

async function registerDirectorySelectionHandler(): Promise<void> {
  ipcMain.removeHandler(SELECT_DIRECTORY_CHANNEL);
  ipcMain.handle(SELECT_DIRECTORY_CHANNEL, createDirectorySelectionHandler(
    path.join(app.getPath('userData'), 'selected-directory.json'), app.getPath('home')
  ));
}

/**
 * Native multi-file attachment picker, scoped to the renderer origin like every
 * other privileged channel. Validation lives in `attachment-picker.ts`; only the
 * dialog and the sender policy are bound here.
 */
function registerAttachmentSelectionHandler(rendererOrigin: string): void {
  ipcMain.removeHandler(ATTACHMENT_SELECT_FILES_CHANNEL);
  ipcMain.handle(
    ATTACHMENT_SELECT_FILES_CHANNEL,
    createAttachmentSelectionHandler({
      authorized: (event) => isAuthorizedSender(event, rendererOrigin),
      showOpenDialog: (options) => dialog.showOpenDialog(options)
    })
  );
}

async function startPackagedRendererServer(): Promise<RendererServer> {
  const rendererRoot = path.join(process.resourcesPath, 'app.asar');
  const nextModule = await import('next');
  const nextFactory = (nextModule.default ?? nextModule) as unknown as (config: {
    dev: boolean;
    dir: string;
  }) => {
    getRequestHandler: () => (
      req: IncomingMessage,
      res: ServerResponse<IncomingMessage>
    ) => Promise<void> | void;
    prepare: () => Promise<void>;
  };

  const nextApp = nextFactory({
    dev: false,
    dir: rendererRoot
  });

  await nextApp.prepare();
  const handle = nextApp.getRequestHandler();
  const server = createServer((req, res) => {
    // Derive the policy once per request and install the one-shot response
    // finalizer before Next can commit headers. The finalizer preserves these
    // nonce bytes for HTML and substitutes only the exact eligible PDF tuple.
    applyPackagedRendererRequestPolicy(req, res);
    try {
      void Promise.resolve(handle(req, res)).catch((error: unknown) => {
        if (res.headersSent) {
          res.destroy(error instanceof Error ? error : new Error(String(error)));
          return;
        }
        res.statusCode = 500;
        res.end('Internal Server Error');
      });
    } catch (error) {
      if (res.headersSent) res.destroy(error instanceof Error ? error : new Error(String(error)));
      else { res.statusCode = 500; res.end('Internal Server Error'); }
    }
  });

  const bound = await bindStableRendererServer({
    userDataDirectory: app.getPath('userData'),
    bind: async (port) => {
      await new Promise<void>((resolve, reject) => {
        server.once('error', reject);
        server.listen(port, '127.0.0.1', () => {
          server.off('error', reject);
          resolve();
        });
      });
      const address = server.address() as AddressInfo | null;
      if (!address || typeof address === 'string') {
        await new Promise<void>((resolve) => server.close(() => resolve()));
        throw new Error('Renderer server failed to bind a TCP port');
      }
      return {
        port: address.port,
        close: async () => {
          await new Promise<void>((resolve, reject) => {
            server.close((error) => error ? reject(error) : resolve());
          });
        }
      };
    }
  });

  return {
    close: bound.close,
    url: `http://127.0.0.1:${bound.port}`
  };
}

const RENDERER_SECURITY_PROBE_ROUTES = ['/', '/chat', '/pipeline', '/workbench'] as const;

function createMainWindow(rendererUrl: string, route = '/'): BrowserWindow {
  const rendererOrigin = new URL(rendererUrl).origin;
  const rendererPageUrl = new URL(route, rendererUrl).toString();
  // Web preferences come from the hardening policy and are asserted there:
  // creation fails closed rather than producing a weaker window.
  const window = new BrowserWindow({
    title: 'Chirality',
    width: 1280,
    height: 840,
    show: false,
    webPreferences: rendererWebPreferences({ preload: path.join(__dirname, 'preload.js') })
  });

  window.once('ready-to-show', () => {
    window.show();
  });

  registerRendererEgressPolicy(window);
  installRendererWindowPolicy(window, {
    rendererOrigin,
    // Packaged responses must keep the request nonce created by the custom
    // server; synthesizing a static response fallback here would disagree with
    // the rendered inline scripts. Development keeps its existing static
    // fallback and allowances.
    contentSecurityPolicy: app.isPackaged
      ? undefined
      : buildRendererContentSecurityPolicy({ mode: 'development', rendererOrigin }),
    // http(s) targets of a renderer window.open / target="_blank" go to the
    // system browser rather than a child window carrying this app's bridge.
    openExternal: (url) => shell.openExternal(url),
    log: (level, event, detail) => desktopLogger.log(level, event, detail)
  });
  window.loadURL(rendererPageUrl);
  void runRendererNetworkProbe(window);
  runRendererSecurityProbe(window, { env: process.env });
  runEgressLayerProbe(window, { env: process.env });

  return window;
}

/** Push a connectivity transition to every live renderer. */
function broadcastRuntimeConnectivity(report: RuntimeConnectivityReport): void {
  for (const window of BrowserWindow.getAllWindows()) {
    if (window.isDestroyed()) {
      continue;
    }
    window.webContents.send(RUNTIME_CONNECTIVITY_CHANGED_CHANNEL, report);
  }
}

/** Push an app-update transition to every live renderer. */
function broadcastAppUpdateState(state: AppUpdateState): void {
  for (const window of BrowserWindow.getAllWindows()) {
    if (window.isDestroyed()) {
      continue;
    }
    window.webContents.send(APP_UPDATE_CHANGED_CHANNEL, state);
  }
}

/**
 * The window a menu action should land in: the focused one, else any live
 * one, else a new one. Main-to-renderer sends go only to a receiver whose
 * loaded URL has the renderer origin, as the folder-intent path does.
 */
function focusOrCreateMainWindow(rendererUrl: string): BrowserWindow {
  const existing = BrowserWindow.getFocusedWindow() ?? BrowserWindow.getAllWindows().find((window) => !window.isDestroyed());
  if (existing) {
    if (existing.isMinimized()) existing.restore();
    existing.focus();
    return existing;
  }
  return createMainWindow(rendererUrl);
}

function sendAboutShowSignal(rendererUrl: string): void {
  const rendererOrigin = new URL(rendererUrl).origin;
  const window = focusOrCreateMainWindow(rendererUrl);
  const deliver = (): void => {
    if (window.isDestroyed()) return;
    if (!isAuthorizedSender({ senderFrame: { url: window.webContents.getURL() } }, rendererOrigin)) return;
    window.webContents.send(APP_ABOUT_SHOW_CHANNEL);
  };
  if (window.webContents.isLoading()) {
    window.webContents.once('did-finish-load', deliver);
  } else {
    deliver();
  }
}

function currentConnectivityReport(): RuntimeConnectivityReport | null {
  const snapshot = bindingSupervisor?.snapshot();
  if (!snapshot) return null;
  return { ...snapshot, service: runtimeServiceHost?.state() ?? null };
}

async function registerRuntimeConnectivityHandler(): Promise<void> {
  ipcMain.removeHandler(RUNTIME_CONNECTIVITY_QUERY_CHANNEL);
  ipcMain.handle(
    RUNTIME_CONNECTIVITY_QUERY_CHANNEL,
    async (): Promise<RuntimeConnectivityReport | null> => currentConnectivityReport()
  );
}

/**
 * One startup path for the App and its owned Runtime service (D-GOV-43, A2).
 *
 * The service is a child of this process: its config is written privately
 * under `userData/runtime`, it is launched before the renderer, and the Next
 * routes and the main-process `RuntimeClient` reach it through the same socket
 * and per-launch client token. Nothing here installs, starts or stops a
 * LaunchAgent; quitting the App stops the service.
 */
async function initializeGui(): Promise<void> {
  const servicePaths = resolveRuntimeServicePaths({
    userDataDirectory: app.getPath('userData'),
    socketPathOverride: process.env.CHIRALITY_RUNTIME_SOCKET_PATH
  });
  // Set before the in-process Next server starts: its harness port reads
  // these lazily per request, and the token file appears once the service is
  // ready. The retired bootstrap-token variable must not linger from an older
  // launcher's environment.
  process.env.CHIRALITY_RUNTIME_DIRECTORY = servicePaths.runtimeDirectory;
  process.env.CHIRALITY_RUNTIME_SOCKET_PATH = servicePaths.socketPath;
  process.env.CHIRALITY_RUNTIME_TOKEN_FILE = servicePaths.clientTokenFile;
  delete process.env.CHIRALITY_RUNTIME_BOOTSTRAP_TOKEN_FILE;
  desktopLogger = createDesktopLogger({
    directory: path.join(app.getPath('userData'), 'logs')
  });
  // The bundle's product name is set by electron-builder, but app.name is the
  // package name; any native panel must read Chirality with the real version.
  // Unpackaged (npm run dev) app.getVersion() reports Electron's own version,
  // so the source checkout's package version is used there instead.
  const appVersion = resolveAppVersion();
  app.setAboutPanelOptions({ applicationName: 'Chirality', applicationVersion: appVersion, version: appVersion });
  const appUpdateSource = resolveAppUpdateSource();
  const appUpdate = createAppUpdateController({
    appVersion,
    source: appUpdateSource,
    // Public GitHub release metadata only, without credentials or redirects.
    // Downloads remain an explicit handoff to the system browser.
    fetchImpl: createPolicyGuardedFetch({ source: appUpdateSource, allowedHosts: APP_UPDATE_ALLOWED_FEED_HOSTS }),
    openExternal: (url) => shell.openExternal(url),
    log: (level, event, detail) => desktopLogger.log(level, event, detail)
  });
  appUpdateController = appUpdate;
  unsubscribeAppUpdate = appUpdate.subscribe(broadcastAppUpdateState);
  const runtimeClient = new RuntimeClient({
    socketPath: servicePaths.socketPath,
    tokenFile: servicePaths.clientTokenFile
  });
  await registerDirectorySelectionHandler();
  await registerRuntimeConnectivityHandler();
  const productInstructionsDefault = resolveProductInstructionsDefault({
    packaged: app.isPackaged,
    resourcesPath: process.resourcesPath,
    frontendRoot: resolveFrontendRoot(),
    instructionRootOverride: process.env.CHIRALITY_INSTRUCTION_ROOT
  });
  process.env.CHIRALITY_INSTRUCTION_ROOT = resolveInstructionRootForProcess();
  desktopLogger.info('desktop.gui.starting', {
    packaged: app.isPackaged,
    userData: app.getPath('userData'),
    socketPath: servicePaths.socketPath,
    pid: process.pid
  });

  const codex = resolveCodexExecutable({
    packaged: app.isPackaged,
    resourcesPath: process.resourcesPath,
    nodeModulesRoot: path.join(resolveFrontendRoot(), 'node_modules')
  });
  const productInstructions = createProductInstructionsStore({
    userDataDirectory: app.getPath('userData'),
    defaultInstructionsPath: productInstructionsDefault
  });
  await productInstructions.initialize();
  const serviceConfig = buildRuntimeServiceConfig({
    paths: servicePaths,
    instructionRoot: resolveServiceInstructionRoot(),
    productInstructionsPath: productInstructions.instructionsPath,
    codexExecutablePath: codex.executablePath,
    userCodexHome: resolveUserCodexHome(),
    expectedCodexVersion: CODEX_PINNED_VERSION
  });
  const serviceEntry = resolveRuntimeServiceEntry();

  // Binding is a supervised main-process concern, not a one-shot startup step:
  // a service that is still starting, or that dies later, must not leave the
  // window permanently unable to reach the runtime. The host nudges the
  // supervisor on every ready line and exit, and the socket watcher covers the
  // moments in between, so the ladder below is only the fallback.
  bindingSupervisor = createRuntimeBindingSupervisor({
    bind: async () => {
      await runtimeClient.daemonStatus();
    },
    probe: async () => {
      try {
        await runtimeClient.daemonStatus();
        return true;
      } catch {
        return false;
      }
    },
    onStateChange: (snapshot) => {
      desktopLogger.info('runtime.connectivity.state', snapshot);
      broadcastRuntimeConnectivity({ ...snapshot, service: runtimeServiceHost?.state() ?? null });
    },
    log: (level, event, detail) => desktopLogger.log(level, event, detail)
  });

  runtimeServiceHost = createRuntimeServiceHost({
    config: serviceConfig,
    configPath: servicePaths.configPath,
    serviceEntry,
    environment: runtimeServiceEnvironment(),
    launch: launchRuntimeServiceChild,
    log: (level, event, detail) => desktopLogger.log(level, event, detail),
    // The desktop log redacts account e-mails at its writer.
    writeServiceStderr: (line) => desktopLogger.info('runtime.service.stderr', line),
    onStateChange: (state) => {
      desktopLogger.info('runtime.service.state', {
        status: state.status,
        pid: state.pid,
        restarts: state.restarts,
        recentFailures: state.recentFailures,
        lastError: state.lastError
      });
      const snapshot = bindingSupervisor?.snapshot();
      if (snapshot) broadcastRuntimeConnectivity({ ...snapshot, service: state });
      if (state.status === 'ready' || state.status === 'restarting' || state.status === 'failed') {
        void bindingSupervisor?.refreshNow();
      }
    }
  });
  desktopLogger.info('runtime.service.starting', {
    entry: serviceEntry,
    codexExecutable: codex.executablePath,
    codexSource: codex.source,
    expectedCodexVersion: CODEX_PINNED_VERSION,
    runtimeDirectory: servicePaths.runtimeDirectory
  });
  // Not awaited: the window must not wait out a 30 s ready timeout when the
  // service is broken. Connectivity is reported live through the supervisor.
  void runtimeServiceHost.start().catch((error) => {
    desktopLogger.error('runtime.service.start_failed', error);
  });

  socketWatcher = createSocketPresenceWatcher({
    socketPath: servicePaths.socketPath,
    onChange: () => {
      void bindingSupervisor?.refreshNow();
    },
    log: (level, event, detail) => desktopLogger.log(level, event, detail)
  });
  socketWatcher.start();

  await bindingSupervisor.start();

  const rendererUrl = app.isPackaged
    ? (rendererServer = await startPackagedRendererServer()).url
    : process.env.ELECTRON_RENDERER_URL ?? 'http://localhost:3000';
  const rendererOrigin = new URL(rendererUrl).origin;

  // Credential channels are registered only once the renderer origin is known:
  // every one of them rejects senders from any other origin, so they cannot
  // exist before the origin does. The window is created after this, so no
  // renderer can invoke them in the gap.
  folderIntentOrigin = rendererOrigin;
  folderIntentRendererUrl = rendererUrl;
  ipcMain.removeHandler(FOLDER_REGISTER_RECENT_CHANNEL);
  ipcMain.handle(FOLDER_REGISTER_RECENT_CHANNEL, (event, input: unknown) =>
    registerRecentFolder(event, input, rendererOrigin, resolveInstructionRootForProcess()));
  ipcMain.removeHandler(FOLDER_OPEN_READY_CHANNEL);
  ipcMain.handle(FOLDER_OPEN_READY_CHANNEL, event => {
    if (!isAuthorizedSender(event, rendererOrigin)) return { ok: false };
    folderIntentReceiver = event.sender;
    void deliverFolderIntent();
    return { ok: true };
  });
  registerAttachmentSelectionHandler(rendererOrigin);
  ipcMain.removeHandler(PRODUCT_INSTRUCTIONS_CHANNEL);
  ipcMain.handle(PRODUCT_INSTRUCTIONS_CHANNEL, createProductInstructionsHandler({
    authorized: event => isAuthorizedSender(event as import('electron').IpcMainInvokeEvent, rendererOrigin),
    store: productInstructions,
    open: file => shell.openPath(file),
    confirmRestore: async () => (await dialog.showMessageBox({
      type: 'question',
      message: 'Restore the default agent instructions?',
      detail: 'A backup of your edits will remain in the instructions folder. Running agents keep their current instructions.',
      buttons: ['Cancel', 'Restore default'],
      defaultId: 0,
      cancelId: 0
    })).response === 1
  }));
  ipcMain.removeHandler(PLAN_EXPORT_DIALOG_CHANNEL);
  ipcMain.handle(PLAN_EXPORT_DIALOG_CHANNEL, createPlanExportDialogHandler({
    authorized: event => isAuthorizedSender(event, rendererOrigin),
    showSaveDialog: options => dialog.showSaveDialog(options),
    showMessageBox: options => dialog.showMessageBox(options)
  }));
  ipcMain.removeHandler(APP_UPDATE_GET_CHANNEL);
  ipcMain.handle(APP_UPDATE_GET_CHANNEL, (event): AppUpdateState | null => {
    if (!isAuthorizedSender(event, rendererOrigin)) return null;
    return appUpdate.getState();
  });
  ipcMain.removeHandler(APP_UPDATE_CHECK_CHANNEL);
  ipcMain.handle(APP_UPDATE_CHECK_CHANNEL, async (event): Promise<AppUpdateState | null> => {
    if (!isAuthorizedSender(event, rendererOrigin)) return null;
    return appUpdate.check();
  });
  ipcMain.removeHandler(APP_UPDATE_OPEN_DOWNLOAD_CHANNEL);
  ipcMain.handle(APP_UPDATE_OPEN_DOWNLOAD_CHANNEL, async (event) => {
    if (!isAuthorizedSender(event, rendererOrigin)) return { ok: false, error: 'App update request was denied.' };
    return appUpdate.openDownload();
  });
  if (process.platform === 'darwin') {
    Menu.setApplicationMenu(Menu.buildFromTemplate(buildApplicationMenuTemplate({
      onCheckForUpdates: () => {
        // The result is broadcast to renderers, so make sure one is there to show it.
        focusOrCreateMainWindow(rendererUrl);
        void appUpdate.check();
      },
      onShowAbout: () => sendAboutShowSignal(rendererUrl)
    })));
  }

  ipcMain.removeHandler('chirality:document-handoff');
  ipcMain.handle('chirality:document-handoff', createDocumentHandoffHandler<import('electron').IpcMainInvokeEvent>({
    authorized: (event) => isAuthorizedSender(event, rendererOrigin),
    instructionRoot: resolveInstructionRootForProcess,
    preview: (event, target) => {
      if (process.platform !== 'darwin') throw new FilePolicyError('QUICK_LOOK_UNAVAILABLE', 400, 'Quick Look requires macOS.');
      const window = BrowserWindow.fromWebContents(event.sender);
      if (!window || window.isDestroyed()) throw new FilePolicyError('WINDOW_UNAVAILABLE', 409, 'Document window is unavailable.');
      window.previewFile(target);
    },
    open: (target) => shell.openPath(target),
    reveal: (target) => shell.showItemInFolder(target)
  }));

  registerApiKeyHandlers(runtimeClient, {
    rendererOrigin,
    log: (level, event, detail) => desktopLogger.log(level, event, detail)
  });

  registerRuntimeControlHandlers({
    rendererOrigin,
    // The renderer's retry after the host gave up: reset the budget and relaunch.
    restartService: async () => {
      if (!runtimeServiceHost) throw new Error('Runtime service host is not running');
      return runtimeServiceHost.restart();
    }
  });

  if (app.isPackaged && process.env.CHIRALITY_RENDERER_SECURITY_PROBE === '1') {
    // The isolated packaged proof loads every operator route in a real
    // BrowserWindow. Outside that explicit proof environment, startup remains
    // one window at `/` as before.
    for (const route of RENDERER_SECURITY_PROBE_ROUTES) {
      createMainWindow(rendererUrl, route);
    }
  } else {
    createMainWindow(rendererUrl);
    stopAppUpdatePolling = startAppUpdatePolling(appUpdate);
  }

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createMainWindow(rendererUrl);
    }
  });
}

/**
 * Release everything this process owns, without exiting.
 *
 * Order matters: the renderer server closes first so no route can reach the
 * service while it is stopping; then the owned Runtime service child receives
 * SIGTERM (SIGKILL after the grace period) and quit waits for its exit. Window
 * close and hide never reach this function; only quit does.
 */
async function teardown(exitCode: number, reason: string): Promise<number> {
  if (shutdownStarted) {
    return exitCode;
  }
  shutdownStarted = true;
  stopAppUpdatePolling?.();
  stopAppUpdatePolling = undefined;
  desktopLogger.info('desktop.shutdown.started', {
    reason,
    exitCode,
    pid: process.pid
  });
  socketWatcher?.stop();
  socketWatcher = undefined;
  bindingSupervisor?.stop();
  bindingSupervisor = undefined;
  ipcMain.removeHandler('chirality:document-handoff');
  ipcMain.removeHandler(SELECT_DIRECTORY_CHANNEL);
  ipcMain.removeHandler(ATTACHMENT_SELECT_FILES_CHANNEL);
  ipcMain.removeHandler(RUNTIME_CONNECTIVITY_QUERY_CHANNEL);
  ipcMain.removeHandler(APP_UPDATE_GET_CHANNEL);
  ipcMain.removeHandler(APP_UPDATE_CHECK_CHANNEL);
  ipcMain.removeHandler(APP_UPDATE_OPEN_DOWNLOAD_CHANNEL);
  unsubscribeAppUpdate?.();
  unsubscribeAppUpdate = undefined;
  appUpdateController = undefined;
  unregisterApiKeyHandlers();
  unregisterRuntimeControlHandlers();

  if (rendererServer) {
    try {
      await rendererServer.close();
    } catch (error) {
      exitCode = 1;
      desktopLogger.error('desktop.renderer_server.close_failed', error);
    }
    rendererServer = undefined;
  }

  if (runtimeServiceHost) {
    try {
      await runtimeServiceHost.stop();
    } catch (error) {
      exitCode = 1;
      desktopLogger.error('runtime.service.stop_failed', error);
    }
    runtimeServiceHost = undefined;
  }
  desktopLogger.info('desktop.shutdown.completed', { reason, exitCode });
  return exitCode;
}

async function shutdown(exitCode = 0, reason = 'unspecified'): Promise<void> {
  if (shutdownStarted) {
    return;
  }
  const finalExitCode = await teardown(exitCode, reason);
  shutdownCompleted = true;
  app.exit(finalExitCode);
}

app
  .whenReady()
  .then(async () => {
    await initializeGui();
  })
  .catch((error) => {
    desktopLogger.error(
      'desktop.gui.initialize_failed',
      error instanceof Error ? error.message : String(error)
    );
    void shutdown(1, 'initialize-failed');
  });

app.on('window-all-closed', () => {
  // Closing the last window is not quitting on macOS: the owned service keeps
  // running and a later activate reopens the window against it.
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

// The single quit funnel. A native quit (menu, Cmd+Q, SIGTERM routed by
// Chromium into `app.quit()`) is turned into our graceful teardown, and a
// concurrent native quit is vetoed while that teardown is in flight; only the
// final owned `app.exit()` is allowed through.
app.on('before-quit', (event) => {
  const hasOwnedResources = runtimeServiceHost !== undefined || rendererServer !== undefined;
  if (
    shouldPreventNativeQuit({ shutdownStarted, shutdownCompleted, hasOwnedResources })
  ) {
    event.preventDefault();
    if (!shutdownStarted) {
      void shutdown(0, 'before-quit');
    }
  }
});

app.on('open-file', (event, filePath) => {
  event.preventDefault();
  // One latest unhandled intent is retained during renderer startup. This is
  // selection intent only; the renderer still validates and enforces chat lock.
  folderIntentGeneration++;
  pendingFolderIntent = filePath;
  if (folderIntentRendererUrl && BrowserWindow.getAllWindows().length === 0) createMainWindow(folderIntentRendererUrl);
  void deliverFolderIntent();
});

for (const signal of ['SIGINT', 'SIGTERM'] as const) {
  process.once(signal, () => {
    void shutdown(signal === 'SIGINT' ? 130 : 0, `signal:${signal}`);
  });
}
