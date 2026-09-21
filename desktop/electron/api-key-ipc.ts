import { ipcMain } from 'electron';
import { isProviderCredentialId, type ProviderCredentialId } from './api-key-storage';
import { describeIpcSender, isAuthorizedSender, type IpcSenderEvent } from './ipc-sender-policy';
import {
  isCredentialStorageState,
  type CredentialStorageState
} from '../src/lib/credential-storage-state';

// Existing Anthropic-only channels remain stable for renderer compatibility.
export const API_KEY_STORE_CHANNEL = 'chirality:api-key-store';
export const API_KEY_REMOVE_CHANNEL = 'chirality:api-key-remove';
export const API_KEY_STATUS_CHANNEL = 'chirality:api-key-status';

export const PROVIDER_API_KEY_STORE_CHANNEL = 'chirality:provider-api-key-store';
export const PROVIDER_API_KEY_REMOVE_CHANNEL = 'chirality:provider-api-key-remove';
export const PROVIDER_API_KEY_STATUS_CHANNEL = 'chirality:provider-api-key-status';

export const CREDENTIAL_IPC_DENIED_EVENT = 'desktop.credential_ipc.denied';
const CREDENTIAL_REQUEST_DENIED = 'Credential request was denied';

export type ApiKeyStorageState = CredentialStorageState;

export type ApiKeyStatusResult = {
  hasKey: boolean;
  encryptionAvailable: boolean;
  source: 'ui' | 'env' | 'none';
  /**
   * Typed safeStorage state of the stored blob (DEL-04-05-V3-01). Present on
   * every real answer from the daemon; absent only when no answer was obtained
   * (`unavailable`, invalid status, or a denied sender).
   */
  storage?: ApiKeyStorageState;
  /**
   * Set when the daemon could not be reached at all, so the renderer can tell
   * "no key stored" apart from "cannot currently tell". Absent on a real answer.
   */
  unavailable?: true;
  error?: string;
};

export type ApiKeyStoreResult = {
  ok: boolean;
  error?: string;
};

export interface DaemonCredentialClient {
  credentialStatus(providerId: ProviderCredentialId): Promise<unknown>;
  storeCredential(
    providerId: ProviderCredentialId,
    credential: string
  ): Promise<{ configured: boolean }>;
  removeCredential(providerId: ProviderCredentialId): Promise<{ configured: boolean }>;
}

export type ApiKeyHandlerLog = (
  level: 'info' | 'warn' | 'error',
  event: string,
  detail?: unknown
) => void;

export type ApiKeyHandlerOptions = {
  /**
   * Exact origin of the renderer the main process created the window for.
   * Every credential channel rejects senders from any other origin
   * (DEL-09-06-V3-01); the policy is `ipc-sender-policy.ts`, shared with the
   * runtime-control channels.
   */
  rendererOrigin: string;
  /** Desktop log sink for denied requests. Receives no key material. */
  log?: ApiKeyHandlerLog;
};

function invalidProviderResult(): ApiKeyStoreResult {
  return { ok: false, error: 'Unsupported credential provider' };
}

function deniedStoreResult(): ApiKeyStoreResult {
  return { ok: false, error: CREDENTIAL_REQUEST_DENIED };
}

function deniedStatusResult(): ApiKeyStatusResult {
  return {
    hasKey: false,
    encryptionAvailable: false,
    source: 'none',
    error: CREDENTIAL_REQUEST_DENIED
  };
}

/**
 * Credential status when the daemon cannot be reached.
 *
 * A status *query* must not reject into the renderer. When the daemon is down the
 * client throws (`ENOENT` on the operator token or the control socket), which
 * surfaced as an unhandled `Error occurred in handler for …` on the IPC channel
 * every time the app started without a running daemon. The connectivity
 * indicator already reports that state; this returns it as data instead.
 */
function unavailableStatusResult(error: unknown): ApiKeyStatusResult {
  return {
    hasKey: false,
    encryptionAvailable: false,
    source: 'none',
    unavailable: true,
    error: error instanceof Error ? error.message : 'Runtime daemon unavailable'
  };
}

function parseCredentialStatus(
  status: unknown
): Pick<ApiKeyStatusResult, 'hasKey' | 'source'> & { storage?: ApiKeyStorageState } | null {
  if (!status || typeof status !== 'object') {
    return null;
  }
  const { configured, source, storage } = status as {
    configured?: unknown;
    source?: unknown;
    storage?: unknown;
  };
  if (
    typeof configured !== 'boolean' ||
    (source !== 'ui' && source !== 'env' && source !== 'none') ||
    configured !== (source !== 'none')
  ) {
    return null;
  }

  let storageState: ApiKeyStorageState | undefined;
  if (storage === undefined) {
    // Compatibility with a daemon that predates the typed storage state (the
    // LaunchAgent may still run the previous build during an update): a `ui`
    // source is by construction a decryptable stored blob, so that one state is
    // certain; anything else is left unknown rather than asserted, because such
    // a daemon cannot tell `missing` from `decryptFailed` or `storageUnavailable`.
    storageState = source === 'ui' ? 'available' : undefined;
  } else if (isCredentialStorageState(storage)) {
    storageState = storage;
  } else {
    return null;
  }

  // A UI-sourced credential is by definition a decryptable stored blob, and a
  // decryptable stored blob is always the winning source. Anything else is an
  // inconsistent answer and fails closed rather than being guessed at.
  if ((source === 'ui') !== (storageState === 'available')) {
    return null;
  }

  return storageState === undefined
    ? { hasKey: configured, source }
    : { hasKey: configured, source, storage: storageState };
}

function invalidStatusResult(): ApiKeyStatusResult {
  return {
    hasKey: false,
    encryptionAvailable: false,
    source: 'none',
    error: 'Runtime daemon returned an invalid credential status'
  };
}

async function credentialStatusResult(
  client: DaemonCredentialClient,
  providerId: ProviderCredentialId
): Promise<ApiKeyStatusResult> {
  let status: unknown;
  try {
    status = await client.credentialStatus(providerId);
  } catch (error) {
    return unavailableStatusResult(error);
  }
  const parsed = parseCredentialStatus(status);
  if (!parsed) {
    return invalidStatusResult();
  }
  return {
    hasKey: parsed.hasKey,
    encryptionAvailable: parsed.storage !== 'storageUnavailable',
    source: parsed.source,
    ...(parsed.storage === undefined ? {} : { storage: parsed.storage })
  };
}

export function registerApiKeyHandlers(
  client: DaemonCredentialClient,
  options: ApiKeyHandlerOptions
): void {
  unregisterApiKeyHandlers();

  const { rendererOrigin, log } = options;

  const denied = (event: IpcSenderEvent, channel: string): boolean => {
    if (isAuthorizedSender(event, rendererOrigin)) {
      return false;
    }
    log?.('warn', CREDENTIAL_IPC_DENIED_EVENT, {
      channel,
      sender: describeIpcSender(event)
    });
    return true;
  };

  ipcMain.handle(API_KEY_STORE_CHANNEL, async (event, key: unknown): Promise<ApiKeyStoreResult> => {
    if (denied(event, API_KEY_STORE_CHANNEL)) {
      return deniedStoreResult();
    }
    if (typeof key !== 'string' || key.trim().length === 0) {
      return { ok: false, error: 'Key must be a non-empty string' };
    }
    try {
      await client.storeCredential('anthropic', key.trim());
      return { ok: true };
    } catch (error) {
      return { ok: false, error: error instanceof Error ? error.message : 'Failed to store key' };
    }
  });

  ipcMain.handle(API_KEY_REMOVE_CHANNEL, async (event): Promise<ApiKeyStoreResult> => {
    if (denied(event, API_KEY_REMOVE_CHANNEL)) {
      return deniedStoreResult();
    }
    try {
      await client.removeCredential('anthropic');
      return { ok: true };
    } catch (error) {
      return { ok: false, error: error instanceof Error ? error.message : 'Failed to remove key' };
    }
  });

  ipcMain.handle(API_KEY_STATUS_CHANNEL, async (event): Promise<ApiKeyStatusResult> => {
    if (denied(event, API_KEY_STATUS_CHANNEL)) {
      return deniedStatusResult();
    }
    return credentialStatusResult(client, 'anthropic');
  });

  ipcMain.handle(
    PROVIDER_API_KEY_STORE_CHANNEL,
    async (event, providerId: unknown, key: unknown): Promise<ApiKeyStoreResult> => {
      if (denied(event, PROVIDER_API_KEY_STORE_CHANNEL)) {
        return deniedStoreResult();
      }
      if (!isProviderCredentialId(providerId)) {
        return invalidProviderResult();
      }
      if (typeof key !== 'string' || key.trim().length === 0) {
        return { ok: false, error: 'Key must be a non-empty string' };
      }
      try {
        await client.storeCredential(providerId, key.trim());
        return { ok: true };
      } catch (error) {
        return { ok: false, error: error instanceof Error ? error.message : 'Failed to store key' };
      }
    }
  );

  ipcMain.handle(
    PROVIDER_API_KEY_REMOVE_CHANNEL,
    async (event, providerId: unknown): Promise<ApiKeyStoreResult> => {
      if (denied(event, PROVIDER_API_KEY_REMOVE_CHANNEL)) {
        return deniedStoreResult();
      }
      if (!isProviderCredentialId(providerId)) {
        return invalidProviderResult();
      }
      try {
        await client.removeCredential(providerId);
        return { ok: true };
      } catch (error) {
        return { ok: false, error: error instanceof Error ? error.message : 'Failed to remove key' };
      }
    }
  );

  ipcMain.handle(
    PROVIDER_API_KEY_STATUS_CHANNEL,
    async (event, providerId: unknown): Promise<ApiKeyStatusResult | ApiKeyStoreResult> => {
      if (denied(event, PROVIDER_API_KEY_STATUS_CHANNEL)) {
        return deniedStatusResult();
      }
      if (!isProviderCredentialId(providerId)) {
        return invalidProviderResult();
      }
      return credentialStatusResult(client, providerId);
    }
  );
}

export function unregisterApiKeyHandlers(): void {
  for (const channel of [
    API_KEY_STORE_CHANNEL,
    API_KEY_REMOVE_CHANNEL,
    API_KEY_STATUS_CHANNEL,
    PROVIDER_API_KEY_STORE_CHANNEL,
    PROVIDER_API_KEY_REMOVE_CHANNEL,
    PROVIDER_API_KEY_STATUS_CHANNEL
  ]) {
    ipcMain.removeHandler(channel);
  }
}
