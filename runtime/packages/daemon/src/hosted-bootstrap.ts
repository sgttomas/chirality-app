import { resolveHostedModelSelection, RuntimeError, type HostedBootstrapStatus, type HostedModelCatalog, type HostedModelSelection } from "@chirality/runtime-contracts";
import type { CodexLogin } from "./codex-login.js";
import { NOOP_RUNTIME_DAEMON_LOGGER, describeRuntimeFailure, type RuntimeDaemonLogger } from "./runtime-daemon.js";

/**
 * Status and login controller for the `hosted-bootstrap` routes over the
 * App-owned Codex sign-in. There is no per-project admission any more: the
 * account is shared by every project, `admission` is `ready` exactly when
 * Codex reports a signed-in account, and the model catalog comes from
 * `model/list`. Provider-network consent is retained on the wire as a no-op
 * because the stock supplier decides its own network use.
 */
export interface HostedBootstrapProjectPort { requireAuthorized(projectId: string): Promise<unknown> }
export interface HostedBootstrapControllerOptions {
  login: CodexLogin;
  /** When supplied, every operation revalidates the project registration first. */
  projects?: HostedBootstrapProjectPort;
  logger?: RuntimeDaemonLogger;
}

export class HostedBootstrapController {
  private readonly logger: RuntimeDaemonLogger;
  private catalogCache?: HostedModelCatalog;
  private closed = false;
  constructor(private readonly options: HostedBootstrapControllerOptions) { this.logger = options.logger ?? NOOP_RUNTIME_DAEMON_LOGGER; }

  private async project(projectId: string): Promise<void> {
    if (this.closed) throw new RuntimeError("ENGINE_UNAVAILABLE", "Hosted bootstrap is closed", 503);
    if (!/^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$/.test(projectId)) throw new RuntimeError("INVALID_REQUEST", "Invalid project ID");
    await this.options.projects?.requireAuthorized(projectId);
  }

  async status(projectId: string): Promise<HostedBootstrapStatus> {
    await this.project(projectId);
    const account = await this.options.login.status();
    let ceremony: HostedBootstrapStatus["ceremony"] = "ready-to-start";
    if (account.signedIn) ceremony = "signed-in";
    else if (account.login?.state === "pending") ceremony = "pending";
    else if (account.login?.state === "failed") ceremony = "failed";
    else if (account.login?.state === "cancelled") ceremony = "cancelled";
    let catalog: HostedModelCatalog | undefined;
    if (account.signedIn) {
      try { catalog = await this.options.login.models(); }
      catch (error) { this.logger.warn("hosted.catalog.unavailable", describeRuntimeFailure(error)); }
      this.catalogCache = catalog;
    } else this.catalogCache = undefined;
    const admission: HostedBootstrapStatus["admission"] = account.signedIn ? (catalog === undefined ? "establishing" : "ready") : "unavailable";
    return {
      schema: "chirality-hosted-bootstrap-status/v1", projectId, ceremony, admission,
      canStartLogin: !account.signedIn && ceremony !== "pending",
      ...(catalog === undefined ? {} : { models: catalog.models.map(entry => ({ ...entry, supportedReasoningEfforts: [...entry.supportedReasoningEfforts] })), selection: resolveHostedModelSelection(catalog) })
    };
  }

  /** Provider-network consent is not a runtime decision in the App-owned composition; the status is returned unchanged. */
  async grantProviderNetworkConsent(projectId: string, _provenance: { approvedBy: string; approvalReference: string; approvedAt: string }): Promise<HostedBootstrapStatus> {
    return this.status(projectId);
  }
  async startLogin(projectId: string): Promise<{ loginId: string; authUrl: string }> {
    await this.project(projectId);
    if ((await this.options.login.status()).signedIn) throw new RuntimeError("INVALID_REQUEST", "Chirality is already signed in to Codex", 409);
    return this.options.login.startLogin();
  }
  async cancelLogin(projectId: string): Promise<HostedBootstrapStatus> {
    await this.project(projectId);
    await this.options.login.cancelLogin();
    return this.status(projectId);
  }
  async signOut(projectId: string): Promise<HostedBootstrapStatus> {
    await this.project(projectId);
    await this.options.login.signOut();
    this.catalogCache = undefined;
    return this.status(projectId);
  }

  /** Last catalog observed by `status`; refreshed on every signed-in status read. */
  catalog(): HostedModelCatalog | undefined { return this.catalogCache; }
  selection(): HostedModelSelection | undefined { return this.catalogCache === undefined ? undefined : resolveHostedModelSelection(this.catalogCache); }
  /** Reads the catalog from Codex now; undefined when signed out. */
  async refreshCatalog(): Promise<HostedModelCatalog | undefined> {
    if (!(await this.options.login.status()).signedIn) { this.catalogCache = undefined; return undefined; }
    this.catalogCache = await this.options.login.models();
    return this.catalogCache;
  }
  async close(): Promise<void> {
    if (this.closed) return;
    this.closed = true;
    await this.options.login.cancelLogin().catch(() => undefined);
  }
}
