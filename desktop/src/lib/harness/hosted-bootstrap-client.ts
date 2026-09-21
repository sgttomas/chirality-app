import type {
  HostedBootstrapLoginStartResponse,
  HostedBootstrapStatus
} from '@chirality/runtime-contracts';
import type {
  HostedBootstrapStatusResponse,
  HostedProjectInitializationResponse
} from '../runtime-client/daemon-harness-port';

export type { HostedBootstrapStatusResponse, HostedProjectInitializationResponse };

export type HostedProjectBindingResponse =
  | { registration: 'required' }
  | { registration: 'registered'; projectId: string };

export class HostedBootstrapClientError extends Error {
  constructor(readonly status: number, message: string) {
    super(message);
    this.name = 'HostedBootstrapClientError';
  }
}

/**
 * Every hosted-bootstrap call goes through the App's own API routes, which
 * proxy to the App-owned Runtime over its socket. The status read walks a
 * short retry ladder while the Runtime service is still coming up after an
 * App launch or a service restart (the App tier answers 503 until then).
 */
const HOST_ACCOUNT_RETRY_DELAYS_MS = [250, 1_000, 5_000] as const;

function preflightSignal(signal?: AbortSignal): void {
  if (signal?.aborted) {
    throw signal.reason ?? new DOMException('The operation was aborted.', 'AbortError');
  }
}

function retryDelay(delayMs: number, signal?: AbortSignal): Promise<void> {
  preflightSignal(signal);
  return new Promise<void>((resolve, reject) => {
    const timer = setTimeout(() => {
      signal?.removeEventListener('abort', abort);
      resolve();
    }, delayMs);
    const abort = (): void => {
      clearTimeout(timer);
      reject(signal?.reason ?? new DOMException('The operation was aborted.', 'AbortError'));
    };
    signal?.addEventListener('abort', abort, { once: true });
  });
}

function isTransientHostAccountError(error: unknown): boolean {
  return error instanceof HostedBootstrapClientError && error.status === 503;
}

async function requestJson<T>(url: string, init?: RequestInit): Promise<T> {
  const response = await fetch(url, init);
  let payload: unknown;
  try {
    payload = await response.json();
  } catch {
    payload = undefined;
  }
  if (!response.ok) {
    const message = payload && typeof payload === 'object' && 'error' in payload &&
      typeof (payload as { error?: { message?: unknown } }).error?.message === 'string'
      ? (payload as { error: { message: string } }).error.message
      : 'The hosted runtime bootstrap service is unavailable.';
    throw new HostedBootstrapClientError(response.status, message);
  }
  return payload as T;
}

function post(projectRoot: string, signal?: AbortSignal, extra: object = {}): RequestInit {
  return {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ projectRoot, ...extra }),
    signal
  };
}

export async function getHostedBootstrapStatus(
  projectRoot: string,
  signal?: AbortSignal
): Promise<HostedBootstrapStatusResponse> {
  preflightSignal(signal);
  const url = `/api/harness/hosted-bootstrap/status?projectRoot=${encodeURIComponent(projectRoot)}`;
  return requestJson(url, { method: 'GET', signal });
}

export function bindHostedBootstrapProject(
  projectRoot: string,
  signal?: AbortSignal
): Promise<HostedProjectBindingResponse> {
  return requestJson(
    '/api/harness/hosted-bootstrap/project/bind',
    post(projectRoot, signal)
  );
}

/**
 * Reads hosted account status, walking the transient-retry ladder while the
 * Runtime service is still coming up. Non-transient failures and exhausted
 * retries surface unchanged.
 */
export async function getHostedBootstrapStatusWithRetry(
  projectRoot: string,
  signal?: AbortSignal
): Promise<HostedBootstrapStatusResponse> {
  for (let attempt = 0; ; attempt += 1) {
    try {
      return await getHostedBootstrapStatus(projectRoot, signal);
    } catch (error) {
      const delayMs = HOST_ACCOUNT_RETRY_DELAYS_MS[attempt];
      if (!isTransientHostAccountError(error) || delayMs === undefined) throw error;
      await retryDelay(delayMs, signal);
    }
  }
}

export async function hydrateHostedBootstrapProject(
  projectRoot: string,
  onBound: (binding: HostedProjectInitializationResponse) => void,
  signal?: AbortSignal
): Promise<HostedBootstrapStatusResponse> {
  const binding = await bindHostedBootstrapProject(projectRoot, signal);
  if (binding.registration === 'registered') onBound(binding);
  return getHostedBootstrapStatusWithRetry(projectRoot, signal);
}

export function initializeHostedBootstrapProject(
  projectRoot: string,
  signal?: AbortSignal
): Promise<HostedProjectInitializationResponse> {
  return requestJson(
    '/api/harness/hosted-bootstrap/project/initialize',
    post(projectRoot, signal)
  );
}

export async function startHostedBootstrapLogin(
  projectRoot: string,
  signal?: AbortSignal
): Promise<HostedBootstrapLoginStartResponse> {
  preflightSignal(signal);
  return requestJson('/api/harness/hosted-bootstrap/login/start', post(projectRoot, signal));
}

export async function cancelHostedBootstrapLogin(
  projectRoot: string,
  signal?: AbortSignal
): Promise<HostedBootstrapStatus> {
  preflightSignal(signal);
  return requestJson('/api/harness/hosted-bootstrap/login/cancel', post(projectRoot, signal));
}

export async function signOutHostedBootstrapProject(
  projectRoot: string,
  signal?: AbortSignal
): Promise<HostedBootstrapStatus> {
  preflightSignal(signal);
  return requestJson('/api/harness/hosted-bootstrap/logout', post(projectRoot, signal));
}
