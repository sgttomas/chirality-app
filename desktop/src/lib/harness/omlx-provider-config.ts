import { getOmlxApiKey } from './api-key-store';

export const DEFAULT_OMLX_BASE_URL = 'http://127.0.0.1:8000/v1';

export type OmlxProviderErrorCode =
  | 'OMLX_CONFIG_INVALID'
  | 'OMLX_OFFLINE'
  | 'OMLX_AUTHENTICATION'
  | 'OMLX_PROTOCOL'
  | 'OMLX_MODELS_MALFORMED'
  | 'OMLX_MODELS_EMPTY'
  | 'OMLX_MODEL_UNKNOWN';

export class OmlxProviderError extends Error {
  readonly name = 'OmlxProviderError';

  constructor(
    readonly code: OmlxProviderErrorCode,
    message: string,
    readonly status?: number
  ) {
    super(message);
  }
}

export type OmlxProviderConfig = {
  baseUrl: string;
  apiKey: string;
};

export type OmlxDiscoveryOptions = {
  baseUrl?: string;
  apiKey?: string;
  fetchImpl?: typeof fetch;
  timeoutMs?: number;
};

const OMLX_BASE_URL_PATTERN = /^http:\/\/127\.0\.0\.1(?::[0-9]{1,5})?\/v1\/?$/;

export function normalizeOmlxBaseUrl(value = DEFAULT_OMLX_BASE_URL): string {
  if (value.trim() !== value || !OMLX_BASE_URL_PATTERN.test(value)) {
    throw new OmlxProviderError(
      'OMLX_CONFIG_INVALID',
      'oMLX base URL must be literal http://127.0.0.1:<port>/v1'
    );
  }

  let parsed: URL;
  try {
    parsed = new URL(value);
  } catch {
    throw new OmlxProviderError('OMLX_CONFIG_INVALID', 'oMLX base URL is invalid');
  }

  const port = parsed.port ? Number.parseInt(parsed.port, 10) : 80;
  if (!Number.isSafeInteger(port) || port < 1 || port > 65_535) {
    throw new OmlxProviderError('OMLX_CONFIG_INVALID', 'oMLX base URL port is invalid');
  }
  if (
    parsed.protocol !== 'http:' ||
    parsed.hostname !== '127.0.0.1' ||
    parsed.username !== '' ||
    parsed.password !== '' ||
    parsed.search !== '' ||
    parsed.hash !== '' ||
    (parsed.pathname !== '/v1' && parsed.pathname !== '/v1/')
  ) {
    throw new OmlxProviderError(
      'OMLX_CONFIG_INVALID',
      'oMLX base URL must be literal http://127.0.0.1:<port>/v1'
    );
  }
  return `${parsed.origin}/v1`;
}

export function resolveOmlxProviderConfig(
  options: Pick<OmlxDiscoveryOptions, 'baseUrl' | 'apiKey'> = {}
): OmlxProviderConfig {
  const apiKey = options.apiKey?.trim() || getOmlxApiKey();
  if (!apiKey) {
    throw new OmlxProviderError(
      'OMLX_AUTHENTICATION',
      'oMLX API key is not configured in secure storage or CHIRALITY_OMLX_API_KEY'
    );
  }
  return {
    baseUrl: normalizeOmlxBaseUrl(options.baseUrl),
    apiKey
  };
}

function parseModelIds(payload: unknown): string[] {
  if (!payload || typeof payload !== 'object' || !Array.isArray((payload as { data?: unknown }).data)) {
    throw new OmlxProviderError('OMLX_MODELS_MALFORMED', 'oMLX returned a malformed models response');
  }

  const data = (payload as { data: unknown[] }).data;
  if (
    data.some(
      (entry) =>
        !entry ||
        typeof entry !== 'object' ||
        typeof (entry as { id?: unknown }).id !== 'string' ||
        (entry as { id: string }).id.length === 0
    )
  ) {
    throw new OmlxProviderError('OMLX_MODELS_MALFORMED', 'oMLX returned a malformed models response');
  }

  const modelIds = data.map((entry) => (entry as { id: string }).id);
  if (modelIds.length === 0) {
    throw new OmlxProviderError('OMLX_MODELS_EMPTY', 'oMLX has no loaded models');
  }
  return modelIds;
}

export async function discoverOmlxModels(options: OmlxDiscoveryOptions = {}): Promise<string[]> {
  const config = resolveOmlxProviderConfig(options);
  const fetchImpl = options.fetchImpl ?? fetch;
  const timeoutMs = options.timeoutMs ?? 5_000;
  const abortController = new AbortController();
  const timeout = setTimeout(() => abortController.abort(), timeoutMs);

  let response: Response;
  try {
    response = await fetchImpl(`${config.baseUrl}/models`, {
      method: 'GET',
      headers: {
        accept: 'application/json',
        authorization: `Bearer ${config.apiKey}`
      },
      redirect: 'manual',
      signal: abortController.signal
    });
  } catch {
    throw new OmlxProviderError('OMLX_OFFLINE', 'oMLX is unavailable on the configured loopback endpoint');
  } finally {
    clearTimeout(timeout);
  }

  if (response.redirected || (response.status >= 300 && response.status < 400)) {
    throw new OmlxProviderError('OMLX_PROTOCOL', 'oMLX redirects are not permitted', response.status);
  }
  if (response.status === 401 || response.status === 403) {
    throw new OmlxProviderError('OMLX_AUTHENTICATION', 'oMLX authentication failed', response.status);
  }
  if (!response.ok) {
    throw new OmlxProviderError('OMLX_PROTOCOL', 'oMLX model discovery failed', response.status);
  }

  let payload: unknown;
  try {
    payload = await response.json();
  } catch {
    throw new OmlxProviderError('OMLX_MODELS_MALFORMED', 'oMLX returned a malformed models response');
  }
  return parseModelIds(payload);
}

export async function requireOmlxModel(
  modelId: string,
  options: OmlxDiscoveryOptions = {}
): Promise<string> {
  if (typeof modelId !== 'string' || modelId.length === 0) {
    throw new OmlxProviderError('OMLX_MODEL_UNKNOWN', 'The requested oMLX model is not loaded');
  }
  const modelIds = await discoverOmlxModels(options);
  if (!modelIds.includes(modelId)) {
    throw new OmlxProviderError('OMLX_MODEL_UNKNOWN', 'The requested oMLX model is not loaded');
  }
  return modelId;
}
