import { HarnessError } from '@chirality/runtime-contracts/errors';

/**
 * D-APP-52 pec bridge transport client (bridge-lane P2).
 *
 * Loopback-only, endpoint-allowlisted HTTP client for the pec engine seam,
 * exactly per the ruled D-T0-19 O-2A transport and the D-T0-20 O-B structural
 * bound (adopted bridge design brief §3/§4/§6):
 *
 * - The base URL is always `http://127.0.0.1:<port>` — the constructor takes a
 *   port only and has NO host parameter (rider 3). Redirects are refused
 *   (`redirect: 'error'`).
 * - The surface is exactly four operations — login, createProposal,
 *   refreshProposal, getProposal — each with a hard-coded method+path template
 *   (endpoint allowlist by construction, rider 4). No generic
 *   `request(method, path)` is exported or reachable; no list, export, intake,
 *   accept, reject, apply, or force method exists (rider 5).
 * - Credentials come from the local environment (`CHIRALITY_PEC_AGENT_EMAIL`,
 *   `CHIRALITY_PEC_AGENT_PASSWORD`), are read only inside `login()`, and never
 *   enter errors, results, or logs (rider 2). The login response body (session
 *   identity) is discarded. The `pec_session` cookie lives in a private field
 *   only and is cleared by `dispose()`.
 * - Error taxonomy per rider 6: one 401 re-login+retry cycle and otherwise
 *   ZERO retries; `409 STALE_PROPOSAL` is surfaced as normal flow with the
 *   ruled refresh→human-re-accept guidance.
 * - No `Origin` header is sent (Node fetch default) — the pec RV-21 guard
 *   permits header-less programmatic clients; this is recorded honestly in the
 *   tool envelopes, not hidden.
 * - The client never starts, stops, or owns any pec server or DB (rider 8).
 */

export const PEC_BRIDGE_DEFAULT_PORT = 4810;
export const PEC_BRIDGE_LOOPBACK_HOST = '127.0.0.1';
/** Client-side mirror of pec's RV-14 proposal CSV cap. */
export const PEC_BRIDGE_MAX_CSV_BYTES = 5 * 1024 * 1024;
/** The ruled 409 STALE_PROPOSAL normal-flow guidance (packet rider 6). */
export const PEC_STALE_PROPOSAL_GUIDANCE =
  'refresh the dry-run; a human re-reviews and re-accepts in pec';

export type PecBridgeConfig = {
  port: number;
};

export function resolvePecBridgeConfig(
  env: Record<string, string | undefined> = process.env
): PecBridgeConfig {
  const raw = env.CHIRALITY_PEC_PORT?.trim();
  if (!raw) {
    return { port: PEC_BRIDGE_DEFAULT_PORT };
  }
  const port = Number(raw);
  if (!Number.isInteger(port) || port < 1 || port > 65535) {
    throw new HarnessError(
      'INVALID_REQUEST',
      400,
      'CHIRALITY_PEC_PORT must be an integer between 1 and 65535',
      {
        configuredValue: raw
      }
    );
  }
  return { port };
}

export type PecBridgeErrorClass =
  | 'auth_failed'
  | 'forbidden'
  | 'bad_request'
  | 'not_found'
  | 'stale_proposal'
  | 'version_conflict'
  | 'server_error'
  | 'network_error';

export type PecEngineErrorPayload = {
  code: string;
  message: string;
  details?: unknown;
};

export class PecBridgeError extends Error {
  readonly errorClass: PecBridgeErrorClass;
  readonly status?: number;
  readonly engineError?: PecEngineErrorPayload;
  /** true only for 409 STALE_PROPOSAL — the ruled recovery loop, not a fault. */
  readonly normalFlow: boolean;
  readonly guidance?: string;

  constructor(input: {
    errorClass: PecBridgeErrorClass;
    message: string;
    status?: number;
    engineError?: PecEngineErrorPayload;
    normalFlow?: boolean;
    guidance?: string;
  }) {
    super(input.message);
    this.name = 'PecBridgeError';
    this.errorClass = input.errorClass;
    this.status = input.status;
    this.engineError = input.engineError;
    this.normalFlow = input.normalFlow ?? false;
    this.guidance = input.guidance;
  }
}

type PecAllowlistedOperation = {
  method: 'GET' | 'POST';
  path: string;
  /** Pre-serialized JSON body; only login/propose/refresh carry one. */
  body?: string;
};

function scrubSecretText(text: string, secrets: readonly string[]): string {
  let out = text;
  for (const secret of secrets) {
    if (secret && secret.length > 0) {
      out = out.split(secret).join('[redacted]');
    }
  }
  return out;
}

function scrubSecretJson(value: unknown, secrets: readonly string[]): unknown {
  if (value === undefined) {
    return undefined;
  }
  try {
    return JSON.parse(scrubSecretText(JSON.stringify(value), secrets));
  } catch {
    return undefined;
  }
}

function assertRecordId(value: number, field: string): number {
  if (!Number.isInteger(value) || value <= 0) {
    throw new PecBridgeError({
      errorClass: 'bad_request',
      message: `${field} must be a positive integer; refused client-side before any network call`
    });
  }
  return value;
}

export class PecBridgeClient {
  readonly #port: number;
  readonly #baseUrl: string;
  #cookie: string | null = null;

  constructor(config: PecBridgeConfig) {
    const port = config.port;
    if (!Number.isInteger(port) || port < 1 || port > 65535) {
      throw new HarnessError(
        'INVALID_REQUEST',
        400,
        'PecBridgeClient port must be an integer between 1 and 65535',
        {
          configuredPort: port
        }
      );
    }
    this.#port = port;
    // Loopback by construction: no host parameter exists anywhere on this class.
    this.#baseUrl = `http://${PEC_BRIDGE_LOOPBACK_HOST}:${port}`;
  }

  /** Transport facts for evidence envelopes; never the cookie or credentials. */
  endpointDescriptor(): { host: '127.0.0.1'; port: number } {
    return { host: PEC_BRIDGE_LOOPBACK_HOST, port: this.#port };
  }

  /** Discard the in-memory session cookie. */
  dispose(): void {
    this.#cookie = null;
  }

  /**
   * Authenticate as the owner-provisioned pec agent person. Credentials are
   * read from the local environment inside this call only; the login response
   * body is discarded and never propagated anywhere.
   */
  async login(): Promise<void> {
    const email = process.env.CHIRALITY_PEC_AGENT_EMAIL ?? '';
    const password = process.env.CHIRALITY_PEC_AGENT_PASSWORD ?? '';
    if (!email.trim() || !password.trim()) {
      throw new PecBridgeError({
        errorClass: 'auth_failed',
        message:
          'pec agent credentials are not configured; set CHIRALITY_PEC_AGENT_EMAIL and CHIRALITY_PEC_AGENT_PASSWORD in the local environment (values are never logged)'
      });
    }

    let response: Response;
    try {
      response = await fetch(`${this.#baseUrl}/api/auth/login`, {
        method: 'POST',
        redirect: 'error',
        headers: {
          'content-type': 'application/json'
        },
        body: JSON.stringify({ email, password })
      });
    } catch (error) {
      throw this.#networkError(error);
    }

    if (!response.ok) {
      // Never map the login response payload into the error: it relates to the
      // credential exchange and must not leak request material.
      await response.arrayBuffer().catch(() => undefined);
      throw new PecBridgeError({
        errorClass: 'auth_failed',
        status: response.status,
        message:
          'pec login failed; check the locally configured agent credentials (never echoed into results or errors)'
      });
    }

    const setCookie = response.headers.get('set-cookie') ?? '';
    const match = /pec_session=([^;]+)/.exec(setCookie);
    // Login response body carries the session identity — read and DISCARD.
    await response.arrayBuffer().catch(() => undefined);
    if (!match) {
      throw new PecBridgeError({
        errorClass: 'auth_failed',
        status: response.status,
        message: 'pec login response carried no pec_session cookie'
      });
    }
    this.#cookie = match[1];
  }

  /** POST /api/projects/:pid/import-proposals?contract=…[&filename=…] with body {csv}. */
  async createProposal(
    projectId: number,
    contract: string,
    csv: string,
    sourceName?: string
  ): Promise<unknown> {
    assertRecordId(projectId, 'projectId');
    const csvBytes = Buffer.byteLength(csv, 'utf8');
    if (csvBytes > PEC_BRIDGE_MAX_CSV_BYTES) {
      throw new PecBridgeError({
        errorClass: 'bad_request',
        message: `CSV is ${csvBytes} bytes and exceeds the ${
          PEC_BRIDGE_MAX_CSV_BYTES / 1024 / 1024
        } MiB proposal cap (RV-14 mirror); refused client-side before any network call`
      });
    }
    const query = new URLSearchParams({ contract });
    if (sourceName !== undefined) {
      query.set('filename', sourceName);
    }
    return this.#call({
      method: 'POST',
      path: `/api/projects/${projectId}/import-proposals?${query.toString()}`,
      body: JSON.stringify({ csv })
    });
  }

  /** POST /api/projects/:pid/import-proposals/:id/refresh with body {version}. */
  async refreshProposal(
    projectId: number,
    proposalId: number,
    expectedVersion: number
  ): Promise<unknown> {
    assertRecordId(projectId, 'projectId');
    assertRecordId(proposalId, 'proposalId');
    if (!Number.isInteger(expectedVersion)) {
      throw new PecBridgeError({
        errorClass: 'bad_request',
        message:
          'expectedVersion must be an integer; refused client-side before any network call'
      });
    }
    return this.#call({
      method: 'POST',
      path: `/api/projects/${projectId}/import-proposals/${proposalId}/refresh`,
      body: JSON.stringify({ version: expectedVersion })
    });
  }

  /** GET /api/projects/:pid/import-proposals/:id — read-only; never recomputes. */
  async getProposal(projectId: number, proposalId: number): Promise<unknown> {
    assertRecordId(projectId, 'projectId');
    assertRecordId(proposalId, 'proposalId');
    return this.#call({
      method: 'GET',
      path: `/api/projects/${projectId}/import-proposals/${proposalId}`
    });
  }

  #secrets(): string[] {
    return [
      process.env.CHIRALITY_PEC_AGENT_EMAIL ?? '',
      process.env.CHIRALITY_PEC_AGENT_PASSWORD ?? '',
      this.#cookie ?? ''
    ];
  }

  #networkError(error: unknown): PecBridgeError {
    const detail = error instanceof Error ? error.message : String(error);
    return new PecBridgeError({
      errorClass: 'network_error',
      message: scrubSecretText(
        `pec engine is unreachable at ${this.#baseUrl}: ${detail}`,
        this.#secrets()
      )
    });
  }

  async #send(operation: PecAllowlistedOperation): Promise<Response> {
    const headers: Record<string, string> = {};
    if (operation.body !== undefined) {
      headers['content-type'] = 'application/json';
    }
    if (this.#cookie) {
      headers.cookie = `pec_session=${this.#cookie}`;
    }
    try {
      return await fetch(`${this.#baseUrl}${operation.path}`, {
        method: operation.method,
        redirect: 'error',
        headers,
        ...(operation.body !== undefined ? { body: operation.body } : {})
      });
    } catch (error) {
      throw this.#networkError(error);
    }
  }

  /**
   * Module-internal dispatch used ONLY by the three allowlisted data methods.
   * Exactly one 401 re-login+retry cycle; zero retries on anything else.
   */
  async #call(operation: PecAllowlistedOperation): Promise<unknown> {
    if (!this.#cookie) {
      await this.login();
    }
    let response = await this.#send(operation);
    if (response.status === 401) {
      await response.arrayBuffer().catch(() => undefined);
      this.#cookie = null;
      await this.login();
      response = await this.#send(operation);
      if (response.status === 401) {
        await response.arrayBuffer().catch(() => undefined);
        throw new PecBridgeError({
          errorClass: 'auth_failed',
          status: 401,
          message:
            'pec rejected the session after one re-login attempt; no further retries are made'
        });
      }
    }
    if (!response.ok) {
      throw await this.#mapErrorResponse(response);
    }
    try {
      return await response.json();
    } catch {
      throw new PecBridgeError({
        errorClass: 'server_error',
        status: response.status,
        message: 'pec returned a non-JSON success payload'
      });
    }
  }

  async #mapErrorResponse(response: Response): Promise<PecBridgeError> {
    const secrets = this.#secrets();
    let engineError: PecEngineErrorPayload | undefined;
    try {
      const parsed = (await response.json()) as { error?: PecEngineErrorPayload } | undefined;
      if (parsed && typeof parsed === 'object' && parsed.error && typeof parsed.error === 'object') {
        engineError = scrubSecretJson(parsed.error, secrets) as PecEngineErrorPayload;
      }
    } catch {
      engineError = undefined;
    }

    const status = response.status;
    const summary = scrubSecretText(
      `pec refused the request (${status} ${engineError?.code ?? 'UNKNOWN'}): ${
        engineError?.message ?? 'no engine error payload'
      }`,
      secrets
    );

    if (status === 400) {
      return new PecBridgeError({ errorClass: 'bad_request', status, engineError, message: summary });
    }
    if (status === 403) {
      // Engine refusal reported verbatim; never escalated or retried.
      return new PecBridgeError({ errorClass: 'forbidden', status, engineError, message: summary });
    }
    if (status === 404) {
      return new PecBridgeError({ errorClass: 'not_found', status, engineError, message: summary });
    }
    if (status === 409 && engineError?.code === 'STALE_PROPOSAL') {
      return new PecBridgeError({
        errorClass: 'stale_proposal',
        status,
        engineError,
        normalFlow: true,
        guidance: PEC_STALE_PROPOSAL_GUIDANCE,
        message: summary
      });
    }
    if (status === 409) {
      return new PecBridgeError({
        errorClass: 'version_conflict',
        status,
        engineError,
        message: summary
      });
    }
    return new PecBridgeError({ errorClass: 'server_error', status, engineError, message: summary });
  }
}
