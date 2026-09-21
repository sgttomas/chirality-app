import { execFile } from "node:child_process";
import { createHash } from "node:crypto";
import { chmod, mkdir, writeFile } from "node:fs/promises";
import { dirname, isAbsolute, join, resolve } from "node:path";
import { promisify } from "node:util";
import {
  CHIRALITY_INSTRUCTION_ROOT_ENV, resolveHostedModelSelection, RuntimeError,
  type EngineSelection, type HostedModelCatalog, type NativePlanAdapterTrialAdmission, type NativePlanCapabilityResponse, type NativePlanClarificationsResponse,
  type NativePlanRevisionsResponse, type ReplyNativePlanClarificationRequest, type RuntimeSessionRecord, type WorkerContinuity,
  CODEX_ENGINE_ADAPTER_ID
} from "@chirality/runtime-contracts";
import {
  AuthRegistry, createDelegatedEngineAdapter, createDelegatedPermissionBroker, DelegatedRuntime, EngineRegistry, privateDirectory, ProjectRegistry,
  ResidencyCoordinator, RuntimeAttachmentResolver, RuntimeService, SessionStore, TrustedNativePlanRegistry, TurnCoordinator, WorkerRetirementCoordinator,
  type DelegatedNativePlanSink, type DelegatedNativePlanWorkerBinding, type DelegatedProjectBinding, type TrustedNativePlanAdapterRegistry
} from "@chirality/runtime-core";
import { CodexAppServerHost, spawnCodexAppServer, type CodexAppServerTransportFactory, type CodexLogger } from "./codex-app-server-client.js";
import { prepareCodexEffectiveHome, type CodexEffectiveHomeReport } from "./codex-effective-home.js";
import { CodexLogin } from "./codex-login.js";
import { CodexSupervisor } from "./codex-supervisor.js";
import { HostedBootstrapController } from "./hosted-bootstrap.js";
import { NOOP_RUNTIME_DAEMON_LOGGER, RuntimeDaemon, describeRuntimeFailure, type RuntimeDaemonLogger } from "./runtime-daemon.js";
import { TurnRegistry } from "./turn-registry.js";
import { ApplicationToolRegistry } from "./application-tools.js";

/**
 * The App-owned Codex composition (SPIKE_DESIGN section 7): one stock
 * `codex app-server` per service, shared by every registered project, with
 * Chirality's sign-in custodied by Codex in the effective home.
 */
export const APP_OWNED_CONFIG_SCHEMA = "chirality-app-owned/v1";
export const APP_HOST_CLIENT_ID = "app-host";
export const CODEX_ENGINE_SELECTION = Object.freeze({ adapterId: CODEX_ENGINE_ADAPTER_ID, providerId: "openai" } as const);
/** Native Plan trial admission for the spike: D-GOV-43 local human trial over the stock app-server plan items. */
export const CODEX_NATIVE_PLAN_TRIAL_ADMISSION: Readonly<NativePlanAdapterTrialAdmission> = Object.freeze({
  adapterId: CODEX_ENGINE_SELECTION.adapterId, providerId: CODEX_ENGINE_SELECTION.providerId,
  dispositionId: "D-GOV-43:app-owned-codex-spike:local-human-trial",
  admissionSha256: createHash("sha256").update("chirality-app-owned/v1 codex-app-server plan items local-human-trial").digest("hex"),
  evidenceClass: "native-adapter-local-human-trial"
});

export interface AppOwnedRuntimeConfig {
  schema: typeof APP_OWNED_CONFIG_SCHEMA;
  socketPath: string;
  runtimeDirectory: string;
  /** Root of the bundled instruction tree (`CHIRALITY_INSTRUCTION_ROOT`). */
  instructionRoot: string;
  productInstructionsPath?: string;
  /** Where the App-host client token is written (0600). */
  clientTokenFile: string;
  codex: {
    executablePath: string;
    /** The user's `~/.codex`. */
    userCodexHome: string;
    /** Chirality's effective home, normally `<runtimeDirectory>/codex-home`. */
    effectiveHome: string;
    /** Pinned stock version; the composition refuses any other `codex --version`. */
    expectedVersion: string;
  };
}
export interface AppOwnedRuntimeOptions {
  logger?: RuntimeDaemonLogger;
  /** Test seam: replaces the real `codex app-server` spawn. */
  transportFactory?: CodexAppServerTransportFactory;
  /** Test seam: skips the `codex --version` check (implied by `transportFactory`). */
  skipVersionCheck?: boolean;
  requestTimeoutMs?: number;
}
export interface AppOwnedRuntime {
  daemon: RuntimeDaemon;
  service: RuntimeService;
  delegated: DelegatedRuntime;
  login: CodexLogin;
  supervisor: CodexSupervisor;
  host: CodexAppServerHost;
  hostedBootstrap: HostedBootstrapController;
  turnRegistry: TurnRegistry;
  applicationTools: ApplicationToolRegistry;
  effectiveHome: CodexEffectiveHomeReport;
  socketPath: string;
  clientTokenFile: string;
  /** Interrupts live turns as `service-shutdown`, stops the daemon and terminates the app-server. Idempotent. */
  close(): Promise<void>;
}

const invalid = (message: string) => new RuntimeError("INVALID_REQUEST", message);
function absolutePath(value: unknown, label: string): string {
  if (typeof value !== "string" || !isAbsolute(value) || resolve(value) !== value || /[\x00-\x1f]/.test(value)) throw invalid(`${label} must be a normalized absolute path`);
  return value;
}
function exactKeys(value: unknown, keys: readonly string[], label: string): Record<string, unknown> {
  if (!value || typeof value !== "object" || Array.isArray(value)) throw invalid(`${label} must be an object`);
  const present = Object.keys(value);
  if (present.length !== keys.length || present.some(key => !keys.includes(key))) throw invalid(`${label} must have exactly ${keys.join(", ")}`);
  return value as Record<string, unknown>;
}
export function validateAppOwnedRuntimeConfig(value: unknown): AppOwnedRuntimeConfig {
  const config = exactKeys(value, ["schema", "socketPath", "runtimeDirectory", "instructionRoot", "clientTokenFile", "codex", ...(value && typeof value === "object" && Object.hasOwn(value, "productInstructionsPath") ? ["productInstructionsPath"] : [])], "App-owned runtime configuration");
  if (config.schema !== APP_OWNED_CONFIG_SCHEMA) throw invalid(`Unsupported configuration schema; expected ${APP_OWNED_CONFIG_SCHEMA}`);
  const codex = exactKeys(config.codex, ["executablePath", "userCodexHome", "effectiveHome", "expectedVersion"], "codex configuration");
  const socketPath = absolutePath(config.socketPath, "socketPath");
  if (Buffer.byteLength(socketPath) > 103) throw invalid("socketPath exceeds the Unix socket path limit (103 bytes)");
  if (typeof codex.expectedVersion !== "string" || !/^\d+\.\d+\.\d+$/.test(codex.expectedVersion)) throw invalid("codex.expectedVersion must be a semantic version");
  const productInstructionsPath = config.productInstructionsPath === undefined ? undefined : absolutePath(config.productInstructionsPath, "productInstructionsPath");
  if (productInstructionsPath !== undefined && [codex.userCodexHome, codex.effectiveHome].some(home => typeof home === "string" && (productInstructionsPath === home || productInstructionsPath.startsWith(`${home}/`)))) throw invalid("productInstructionsPath must be outside Codex homes");
  return {
    ...(productInstructionsPath === undefined ? {} : { productInstructionsPath }),
    schema: APP_OWNED_CONFIG_SCHEMA, socketPath,
    runtimeDirectory: absolutePath(config.runtimeDirectory, "runtimeDirectory"),
    instructionRoot: absolutePath(config.instructionRoot, "instructionRoot"),
    clientTokenFile: absolutePath(config.clientTokenFile, "clientTokenFile"),
    codex: { executablePath: absolutePath(codex.executablePath, "codex.executablePath"), userCodexHome: absolutePath(codex.userCodexHome, "codex.userCodexHome"), effectiveHome: absolutePath(codex.effectiveHome, "codex.effectiveHome"), expectedVersion: codex.expectedVersion }
  };
}

const execFileAsync = promisify(execFile);
/** `codex --version` prints `codex-cli <version>`; anything else is refused before the app-server starts. */
export async function assertCodexVersion(executablePath: string, expectedVersion: string): Promise<string> {
  let stdout: string;
  try { ({ stdout } = await execFileAsync(executablePath, ["--version"], { timeout: 15_000, maxBuffer: 64 * 1024, env: { ...process.env } })); }
  catch (error) { throw new RuntimeError("ENGINE_UNAVAILABLE", `Codex executable is unavailable (${(error as NodeJS.ErrnoException)?.code ?? "spawn failed"})`, 503, { reason: "CODEX_EXECUTABLE_UNAVAILABLE" }); }
  const match = /(\d+\.\d+\.\d+)/.exec(stdout);
  const observed = match?.[1];
  if (observed !== expectedVersion) throw new RuntimeError("ENGINE_UNAVAILABLE", `Codex version ${observed ?? "unknown"} does not match the pinned ${expectedVersion}`, 503, { reason: "CODEX_VERSION_MISMATCH", expected: expectedVersion, observed: observed ?? null });
  return observed;
}

/** Per-project trusted native Plan registries behind the single service-wide registry seam. */
class ProjectNativePlanRegistry implements TrustedNativePlanAdapterRegistry, DelegatedNativePlanSink {
  private readonly registries = new Map<string, TrustedNativePlanRegistry>();
  constructor(private readonly sessions: SessionStore) {}
  for(projectId: string): TrustedNativePlanRegistry {
    let registry = this.registries.get(projectId);
    if (registry === undefined) { registry = new TrustedNativePlanRegistry({ projectId, sessions: this.sessions, admission: CODEX_NATIVE_PLAN_TRIAL_ADMISSION }); this.registries.set(projectId, registry); }
    return registry;
  }
  capability(session: RuntimeSessionRecord): Promise<NativePlanCapabilityResponse> { return this.for(session.projectId).capability(session); }
  revisions(projectId: string, sessionId: string): Promise<NativePlanRevisionsResponse> { return this.for(projectId).revisions(projectId, sessionId); }
  clarifications(projectId: string, sessionId: string): Promise<NativePlanClarificationsResponse> { return this.for(projectId).clarifications(projectId, sessionId); }
  replyClarification(projectId: string, sessionId: string, request: ReplyNativePlanClarificationRequest): Promise<{ sent: true }> {
    const registry = this.for(projectId);
    if (typeof registry.replyClarification !== "function") throw new RuntimeError("ENGINE_UNAVAILABLE", "Native Plan clarifications are unavailable", 503);
    return registry.replyClarification(projectId, sessionId, request);
  }
  open(binding: DelegatedNativePlanWorkerBinding, bridge: Parameters<DelegatedNativePlanSink["open"]>[1]): Promise<void> { return this.for(binding.projectId).open(binding, bridge); }
  capture(binding: DelegatedNativePlanWorkerBinding, events: Parameters<DelegatedNativePlanSink["capture"]>[1], clarifications: Parameters<DelegatedNativePlanSink["capture"]>[2]): Promise<void> { return this.for(binding.projectId).capture(binding, events, clarifications); }
  close(binding: DelegatedNativePlanWorkerBinding): Promise<void> { return this.for(binding.projectId).close(binding); }
}

function codexLogger(logger: RuntimeDaemonLogger): CodexLogger {
  return { warn: (event, fields) => logger.warn(event, fields), error: (event, fields) => logger.error(event, fields) };
}

export async function startAppOwnedRuntime(rawConfig: AppOwnedRuntimeConfig, options: AppOwnedRuntimeOptions = {}): Promise<AppOwnedRuntime> {
  const config = validateAppOwnedRuntimeConfig(rawConfig);
  const logger = options.logger ?? NOOP_RUNTIME_DAEMON_LOGGER;
  await privateDirectory(config.runtimeDirectory);
  const effectiveHome = await prepareCodexEffectiveHome({ userCodexHome: config.codex.userCodexHome, effectiveHome: config.codex.effectiveHome });
  if (options.transportFactory === undefined && options.skipVersionCheck !== true) await assertCodexVersion(config.codex.executablePath, config.codex.expectedVersion);

  const host = new CodexAppServerHost({
    clientVersion: config.codex.expectedVersion, logger: codexLogger(logger), ...(options.requestTimeoutMs === undefined ? {} : { requestTimeoutMs: options.requestTimeoutMs }),
    transportFactory: options.transportFactory ?? (() => spawnCodexAppServer({ executablePath: config.codex.executablePath, effectiveHome: config.codex.effectiveHome, cwd: config.runtimeDirectory, onStderr: line => logger.warn("codex.app-server.stderr", { line: line.slice(0, 512) }) }))
  });
  await host.start();
  const login = new CodexLogin({ host, logger: codexLogger(logger) });

  const projects = new ProjectRegistry(config.runtimeDirectory, { ...process.env, [CHIRALITY_INSTRUCTION_ROOT_ENV]: config.instructionRoot });
  const sessions = new SessionStore(config.runtimeDirectory, projects);
  const applicationTools = new ApplicationToolRegistry({ sessions });
  const supervisor = new CodexSupervisor({ host, logger: codexLogger(logger), applicationTools });
  // A fresh service owns no turns: sessions a hard-killed or crashed service left
  // `running` settle now, so no relaunch refuses them with SESSION_TURN_IN_PROGRESS.
  for (const status of await projects.list().catch(() => [])) {
    const projectId = status.project.projectId;
    const settled = await sessions.settleRunningOnStart(projectId, "service-restart").catch((error: unknown) => { logger.warn("runtime.sessions.settle_on_start_failed", { projectId, ...describeRuntimeFailure(error) }); return [] as readonly string[]; });
    if (settled.length > 0) logger.warn("runtime.sessions.settled_on_start", { projectId, count: settled.length });
  }
  const engines = new EngineRegistry();
  const offline = async (): Promise<never> => { throw new RuntimeError("ENGINE_UNAVAILABLE", "Local model residency is not part of the App-owned Codex composition", 503); };
  const residency = new ResidencyCoordinator({ async listStatus() { return []; }, load: offline, unload: offline }, config.runtimeDirectory);
  const auth = new AuthRegistry(config.runtimeDirectory);
  const hostedBootstrap = new HostedBootstrapController({ login, projects, logger });
  const nativePlan = new ProjectNativePlanRegistry(sessions);

  const retirements = new Map<string, Promise<WorkerRetirementCoordinator>>();
  const retirementFor = (projectId: string): Promise<WorkerRetirementCoordinator> => {
    let pending = retirements.get(projectId);
    if (pending === undefined) {
      pending = (async () => {
        const directory = join(config.runtimeDirectory, "retirement", projectId);
        await mkdir(directory, { recursive: true, mode: 0o700 });
        const coordinator = new WorkerRetirementCoordinator({ directory });
        await coordinator.reconcile();
        return coordinator;
      })();
      retirements.set(projectId, pending);
      pending.catch(() => retirements.delete(projectId));
    }
    return pending;
  };
  const delegated = new DelegatedRuntime({
    daemonId: "app-owned-starting",
    async resolveProject(projectId): Promise<DelegatedProjectBinding | undefined> {
      const project = await projects.requireAuthorized(projectId);
      const identity: WorkerContinuity = { canonicalRoot: project.canonicalRoot, cwd: project.canonicalRoot, accountId: "chirality-app", accountEpoch: 0, policyDigest: "stock-codex" };
      // A service that just started has read no catalog yet; a turn before the
      // first status read must not fail its model and effort validation for that.
      const catalog = hostedBootstrap.catalog() ?? await hostedBootstrap.refreshCatalog().catch(() => undefined);
      return { identity, supervisor, retirement: await retirementFor(projectId), nativePlanSink: nativePlan, ...(catalog === undefined ? {} : { catalog, actual: { ...CODEX_ENGINE_SELECTION, model: catalog.default.model, reasoningEffort: catalog.default.defaultReasoningEffort } }), evidenceClass: "provider-observed" };
    }
  });
  const catalogNow = (): Readonly<HostedModelCatalog> | undefined => hostedBootstrap.catalog();
  engines.register(createDelegatedEngineAdapter({ delegated, selection: { ...CODEX_ENGINE_SELECTION, model: "codex-default" }, catalog: catalogNow, nativeRoleDirectory: join(config.runtimeDirectory, "native-role-bases") }));

  const defaultSessionPolicy = {
    async resolve({ agentType, modelSelection }: { agentType: 0 | 1; modelSelection?: { model: string; reasoningEffort: string } }) {
      const catalog = hostedBootstrap.catalog() ?? await hostedBootstrap.refreshCatalog();
      if (catalog === undefined) throw new RuntimeError("ENGINE_UNAVAILABLE", "Chirality is not signed in to Codex", 503, { reason: "CODEX_SIGNED_OUT" });
      const selection = resolveHostedModelSelection(catalog, modelSelection);
      const engineSelection: EngineSelection = { ...CODEX_ENGINE_SELECTION, model: selection.model };
      return { role: agentType === 0 ? "agent0" as const : "agent1" as const, engineSelection, reasoningEffort: selection.reasoningEffort };
    }
  };
  const credentials = { async get() { return undefined; }, async status() { return { configured: false as const }; }, set: offline, remove: offline };
  const service = new RuntimeService(projects, sessions, engines, residency, new TurnCoordinator(projects, sessions, engines, residency, new RuntimeAttachmentResolver()), auth, credentials, undefined, undefined, createDelegatedPermissionBroker(delegated), defaultSessionPolicy, nativePlan, { nativeProjectDiscovery: true, ...(config.productInstructionsPath === undefined ? {} : { productInstructionsPath: config.productInstructionsPath }) });
  const turnRegistry = new TurnRegistry(service, { sessions, logger });
  const daemon = new RuntimeDaemon({ socketPath: config.socketPath, runtimeDirectory: config.runtimeDirectory, service, turnRegistry, requests: delegated, delegated, hostedBootstrap, applicationTools, applicationToolHostClientId: APP_HOST_CLIENT_ID, logger });

  let closing: Promise<void> | undefined;
  const close = (): Promise<void> => {
    if (closing !== undefined) return closing;
    closing = (async () => {
      const failures: unknown[] = [];
      const step = async (name: string, action: () => Promise<unknown>) => { try { await action(); } catch (error) { failures.push(error); logger.error("app-owned.close.failed", { step: name, ...describeRuntimeFailure(error) }); } };
      await step("turns", () => turnRegistry.close({ reason: "service-shutdown" }));
      await step("delegated", () => delegated.close());
      await step("daemon", () => daemon.stop());
      await step("hosted-bootstrap", () => hostedBootstrap.close());
      login.close();
      await step("supervisor", () => supervisor.close());
      applicationTools.close();
      await step("app-server", () => host.close());
      if (failures.length > 0) throw failures[0];
    })();
    return closing;
  };

  try {
    await daemon.start();
    const issued = await auth.issueClient(APP_HOST_CLIENT_ID, ["runtime:read", "projects:write", "sessions:read", "sessions:write", "models:read", "models:write", "credentials:read", "credentials:write"]);
    await mkdir(dirname(config.clientTokenFile), { recursive: true, mode: 0o700 });
    await writeFile(config.clientTokenFile, `${issued.token}\n`, { encoding: "utf8", mode: 0o600 });
    await chmod(config.clientTokenFile, 0o600);
  } catch (error) {
    await close().catch(() => undefined);
    throw error;
  }
  return { daemon, service, delegated, login, supervisor, host, hostedBootstrap, turnRegistry, applicationTools, effectiveHome, socketPath: config.socketPath, clientTokenFile: config.clientTokenFile, close };
}
