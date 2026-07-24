import {
  RuntimeError,
  type OmlxControlPort,
  type OmlxModelKind,
  type OmlxModelStatus,
  type ProviderCredentialPort
} from "@chirality/runtime-contracts";

export const DEFAULT_OMLX_BASE_URL = "http://127.0.0.1:8000/v1";
const BASE_URL_PATTERN = /^http:\/\/127\.0\.0\.1(?::[0-9]{1,5})?\/v1\/?$/u;

export function normalizeOmlxBaseUrl(value = DEFAULT_OMLX_BASE_URL): string {
  if (value.trim() !== value || !BASE_URL_PATTERN.test(value)) {
    throw new RuntimeError(
      "INVALID_REQUEST",
      "oMLX base URL must be literal http://127.0.0.1:<port>/v1"
    );
  }
  const url = new URL(value);
  const port = url.port === "" ? 80 : Number.parseInt(url.port, 10);
  if (
    url.protocol !== "http:" ||
    url.hostname !== "127.0.0.1" ||
    url.username !== "" ||
    url.password !== "" ||
    url.search !== "" ||
    url.hash !== "" ||
    port < 1 ||
    port > 65_535
  ) {
    throw new RuntimeError("INVALID_REQUEST", "Unsafe oMLX endpoint");
  }
  return `${url.origin}/v1`;
}

export interface OmlxClientOptions {
  credentials: ProviderCredentialPort;
  baseUrl?: string;
  fetchImpl?: typeof fetch;
  timeoutMs?: number;
}

export class OmlxClient implements OmlxControlPort {
  private readonly baseUrl: string;
  private readonly fetchImpl: typeof fetch;
  private readonly timeoutMs: number;

  constructor(private readonly options: OmlxClientOptions) {
    this.baseUrl = normalizeOmlxBaseUrl(options.baseUrl);
    this.fetchImpl = options.fetchImpl ?? globalThis.fetch.bind(globalThis);
    this.timeoutMs = options.timeoutMs ?? 30_000;
  }

  async listStatus(signal?: AbortSignal): Promise<readonly OmlxModelStatus[]> {
    const payload = await this.request("/models/status", { method: "GET", signal });
    const entries = Array.isArray(payload)
      ? payload
      : Array.isArray((payload as { models?: unknown })?.models)
        ? (payload as { models: unknown[] }).models
        : Array.isArray((payload as { data?: unknown })?.data)
          ? (payload as { data: unknown[] }).data
          : undefined;
    if (entries === undefined) {
      throw new RuntimeError("OMLX_PROTOCOL_FAILURE", "Malformed oMLX status response", 502);
    }
    return entries.map((entry) => this.parseStatus(entry));
  }

  async load(modelId: string, signal?: AbortSignal): Promise<void> {
    await this.request(`/models/${encodeURIComponent(this.exactId(modelId))}/load`, {
      method: "POST",
      signal
    });
  }

  async unload(modelId: string, signal?: AbortSignal): Promise<void> {
    await this.request(`/models/${encodeURIComponent(this.exactId(modelId))}/unload`, {
      method: "POST",
      signal
    });
  }

  private async request(
    path: string,
    init: { method: "GET" | "POST"; signal?: AbortSignal }
  ): Promise<unknown> {
    const key = await this.options.credentials.get("omlx");
    if (key === undefined || key.trim() === "") {
      throw new RuntimeError(
        "OMLX_AUTHENTICATION_FAILED",
        "oMLX credential is not configured",
        401
      );
    }
    const timeout = AbortSignal.timeout(this.timeoutMs);
    const signal =
      init.signal === undefined ? timeout : AbortSignal.any([init.signal, timeout]);
    let response: Response;
    try {
      response = await this.fetchImpl(`${this.baseUrl}${path}`, {
        method: init.method,
        headers: {
          accept: "application/json",
          authorization: `Bearer ${key}`,
          ...(init.method === "POST" ? { "content-type": "application/json" } : {})
        },
        redirect: "manual",
        signal
      });
    } catch {
      throw new RuntimeError("OMLX_UNAVAILABLE", "oMLX is unavailable on loopback", 503);
    }
    if (response.status >= 300 && response.status < 400) {
      throw new RuntimeError("OMLX_PROTOCOL_FAILURE", "oMLX redirects are forbidden", 502);
    }
    if (response.status === 401 || response.status === 403) {
      throw new RuntimeError("OMLX_AUTHENTICATION_FAILED", "oMLX authentication failed", 401);
    }
    if (!response.ok) {
      throw new RuntimeError(
        "OMLX_PROTOCOL_FAILURE",
        `oMLX control request failed with HTTP ${response.status}`,
        502
      );
    }
    if (response.status === 204) return {};
    try {
      return await response.json();
    } catch {
      throw new RuntimeError("OMLX_PROTOCOL_FAILURE", "oMLX returned malformed JSON", 502);
    }
  }

  private parseStatus(value: unknown): OmlxModelStatus {
    if (typeof value !== "object" || value === null) {
      throw new RuntimeError("OMLX_PROTOCOL_FAILURE", "Malformed oMLX model status", 502);
    }
    const item = value as Record<string, unknown>;
    const id = item["id"] ?? item["model_id"];
    if (typeof id !== "string" || id.length === 0) {
      throw new RuntimeError("OMLX_PROTOCOL_FAILURE", "oMLX status omitted exact model ID", 502);
    }
    // oMLX 0.5.x exposes the discovered category as `model_type` and the
    // implementation as `engine_type`. Keep the older `kind`/`type` aliases
    // for fake-provider and compatibility fixtures, but never infer a
    // generative model from its name.
    const rawKind = item["kind"] ?? item["type"] ?? item["model_type"];
    const engineType = item["engine_type"];
    const kind: OmlxModelKind =
      item["is_helper"] === true
        ? "helper"
        : rawKind === "llm" ||
            rawKind === "vlm" ||
            engineType === "batched" ||
            engineType === "simple" ||
            engineType === "vlm"
          ? "llm"
          : rawKind === "embedding" || engineType === "embedding"
            ? "embedding"
            : rawKind === "reranker" || engineType === "reranker"
              ? "reranker"
              : rawKind === "helper"
                ? "helper"
                : "unknown";
    const size =
      item["actual_size"] ??
      item["estimated_size"] ??
      item["size_bytes"] ??
      item["sizeBytes"];
    return {
      id,
      kind,
      loaded: item["loaded"] === true || item["status"] === "loaded",
      loading: item["loading"] === true || item["is_loading"] === true,
      ...(item["managed"] === true ? { managed: true } : {}),
      ...(typeof size === "number" && Number.isFinite(size) ? { sizeBytes: size } : {})
    };
  }

  private exactId(value: string): string {
    if (value.length === 0 || value.trim() !== value || /[\u0000-\u001f]/u.test(value)) {
      throw new RuntimeError("INVALID_REQUEST", "An exact non-empty model ID is required");
    }
    return value;
  }
}
