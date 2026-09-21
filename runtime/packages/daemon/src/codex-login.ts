import { hostedModelCatalog, RuntimeError, type HostedModelCatalog, type HostedModelCatalogEntry } from "@chirality/runtime-contracts";
import { NOOP_CODEX_LOGGER, type CodexAppServerHost, type CodexLogger } from "./codex-app-server-client.js";

/**
 * Chirality sign-in over the app-server account methods. Credentials are
 * custodied by Codex in the effective home; this controller only relays the
 * ChatGPT browser ceremony and observes presence. Account e-mail addresses
 * are never retained or logged.
 */
export type CodexLoginHost = Pick<CodexAppServerHost, "request" | "onNotification">;

export interface CodexAccountStatus {
  signedIn: boolean;
  accountType?: string;
  planType?: string;
  requiresOpenaiAuth: boolean;
  /** The most recent ceremony started by this process, while its outcome is still relevant. */
  login?: { loginId: string; state: "pending" | "completed" | "failed" | "cancelled"; error?: string };
}

export interface CodexLoginOptions { host: CodexLoginHost; logger?: CodexLogger }

interface AccountReadResponse { account: null | { type?: string; planType?: string }; requiresOpenaiAuth?: boolean }
interface ModelListResponse { data?: readonly unknown[]; nextCursor?: string | null }

function text(value: unknown, limit = 256): string | undefined {
  return typeof value === "string" && value.length > 0 ? value.slice(0, limit) : undefined;
}

export class CodexLogin {
  private readonly logger: CodexLogger;
  private login?: CodexAccountStatus["login"];
  private readonly unsubscribe: () => void;
  constructor(private readonly options: CodexLoginOptions) {
    this.logger = options.logger ?? NOOP_CODEX_LOGGER;
    this.unsubscribe = options.host.onNotification(notification => {
      if (notification.method !== "account/login/completed") return;
      const params = notification.params && typeof notification.params === "object" ? notification.params as Record<string, unknown> : {};
      const loginId = text(params.loginId, 512);
      if (this.login === undefined || (loginId !== undefined && loginId !== this.login.loginId)) return;
      if (params.success === true) { this.login = { loginId: this.login.loginId, state: "completed" }; this.logger.warn("codex.login.completed", {}); }
      else { this.login = { loginId: this.login.loginId, state: "failed", error: text(params.error, 512) ?? "login failed" }; this.logger.warn("codex.login.failed", {}); }
    });
  }

  async status(): Promise<CodexAccountStatus> {
    const response = await this.options.host.request<AccountReadResponse>("account/read", { refreshToken: false });
    const account = response.account && typeof response.account === "object" ? response.account : null;
    return {
      signedIn: account !== null,
      ...(account === null ? {} : { accountType: text(account.type, 64), ...(text(account.planType, 64) === undefined ? {} : { planType: text(account.planType, 64) }) }),
      requiresOpenaiAuth: response.requiresOpenaiAuth === true,
      ...(this.login === undefined ? {} : { login: { ...this.login } })
    };
  }

  async startLogin(): Promise<{ loginId: string; authUrl: string }> {
    if (this.login?.state === "pending") throw new RuntimeError("INVALID_REQUEST", "A Chirality sign-in is already pending", 409);
    const response = await this.options.host.request<{ type?: string; loginId?: string; authUrl?: string }>("account/login/start", { type: "chatgpt" });
    const loginId = text(response.loginId, 512), authUrl = text(response.authUrl, 8192);
    if (loginId === undefined || authUrl === undefined || !/^https?:\/\//.test(authUrl)) throw new RuntimeError("ENGINE_UNAVAILABLE", "Codex did not return a browser sign-in", 503);
    this.login = { loginId, state: "pending" };
    this.logger.warn("codex.login.started", {});
    return { loginId, authUrl };
  }

  async cancelLogin(): Promise<void> {
    const login = this.login;
    if (login === undefined || login.state !== "pending") return;
    try { await this.options.host.request("account/login/cancel", { loginId: login.loginId }); }
    finally { if (this.login === login) this.login = { loginId: login.loginId, state: "cancelled" }; }
  }

  async signOut(): Promise<void> {
    await this.cancelLogin().catch(() => undefined);
    await this.options.host.request("account/logout", undefined);
    this.login = undefined;
    this.logger.warn("codex.login.signed_out", {});
  }

  /** The non-hidden authenticated catalog, or undefined when signed out or the catalog is empty. */
  async models(): Promise<HostedModelCatalog | undefined> {
    const response = await this.options.host.request<ModelListResponse>("model/list", {});
    const entries: HostedModelCatalogEntry[] = [];
    for (const raw of Array.isArray(response.data) ? response.data : []) {
      const value = raw && typeof raw === "object" ? raw as Record<string, unknown> : {};
      if (value.hidden === true) continue;
      const model = text(value.model, 128);
      if (model === undefined) continue;
      const efforts: string[] = [];
      for (const effort of Array.isArray(value.supportedReasoningEfforts) ? value.supportedReasoningEfforts : []) {
        const name = typeof effort === "string" ? effort : text((effort as Record<string, unknown> | null)?.reasoningEffort ?? (effort as Record<string, unknown> | null)?.effort, 64);
        if (name !== undefined && !efforts.includes(name)) efforts.push(name);
      }
      const defaultEffort = text(value.defaultReasoningEffort, 64) ?? efforts[0];
      if (defaultEffort === undefined) continue;
      if (!efforts.includes(defaultEffort)) efforts.push(defaultEffort);
      entries.push({ model, isDefault: value.isDefault === true, defaultReasoningEffort: defaultEffort, supportedReasoningEfforts: efforts });
    }
    if (entries.length === 0) return undefined;
    if (!entries.some(entry => entry.isDefault)) entries[0] = { ...entries[0]!, isDefault: true };
    else if (entries.filter(entry => entry.isDefault).length > 1) { let seen = false; for (let index = 0; index < entries.length; index += 1) { if (entries[index]!.isDefault) { if (seen) entries[index] = { ...entries[index]!, isDefault: false }; seen = true; } } }
    return hostedModelCatalog(entries);
  }

  close(): void { this.unsubscribe(); }
}
