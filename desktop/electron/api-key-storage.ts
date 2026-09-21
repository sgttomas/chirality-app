/**
 * Provider credential storage.
 *
 * Credentials are encrypted with Electron safeStorage and persisted under the
 * app userData directory. The Anthropic filename and process-global are kept
 * for compatibility with existing installations and server-side consumers.
 */

import { app, safeStorage } from 'electron';
import { chmod, mkdir, readFile, rm, writeFile } from 'node:fs/promises';
import path from 'node:path';
import type { CredentialStorageState } from '../src/lib/credential-storage-state';

export const PROVIDER_CREDENTIAL_IDS = ['anthropic', 'omlx'] as const;
export type ProviderCredentialId = (typeof PROVIDER_CREDENTIAL_IDS)[number];
export type ProviderCredentialSource = 'ui' | 'env' | 'none';
export type { CredentialStorageState as ProviderCredentialStorageState };

/**
 * Outcome of reading one provider's encrypted blob. Only `available` carries
 * the plaintext; every other state is a bare discriminator so callers that
 * merely want the typed state can never receive key material by accident.
 */
export type ProviderCredentialRead =
  | { state: 'available'; value: string }
  | { state: 'missing' }
  | { state: 'storageUnavailable' }
  | { state: 'decryptFailed' };

const LEGACY_ANTHROPIC_STORAGE_FILENAME = 'api-key.enc';
const PROVIDER_STORAGE_FILENAMES: Record<ProviderCredentialId, string> = {
  anthropic: LEGACY_ANTHROPIC_STORAGE_FILENAME,
  omlx: 'api-key.omlx.enc'
};
const LEGACY_ANTHROPIC_GLOBAL_KEY = '__CHIRALITY_UI_API_KEY__';
const PROVIDER_GLOBAL_KEY = '__CHIRALITY_PROVIDER_API_KEYS__';

type ApiKeyGlobal = typeof globalThis & {
  [LEGACY_ANTHROPIC_GLOBAL_KEY]?: string;
  [PROVIDER_GLOBAL_KEY]?: Partial<Record<ProviderCredentialId, string>>;
};

const apiKeyGlobal = globalThis as ApiKeyGlobal;

export function isProviderCredentialId(value: unknown): value is ProviderCredentialId {
  return typeof value === 'string' && PROVIDER_CREDENTIAL_IDS.includes(value as ProviderCredentialId);
}

function getStoragePath(providerId: ProviderCredentialId): string {
  return path.join(app.getPath('userData'), 'credentials', PROVIDER_STORAGE_FILENAMES[providerId]);
}

async function ensureStorageDir(providerId: ProviderCredentialId): Promise<void> {
  const directory = path.dirname(getStoragePath(providerId));
  await mkdir(directory, { recursive: true, mode: 0o700 });
  // mkdir ignores mode for an existing directory, and process umask can relax
  // it for a new one, so the private mode is asserted rather than requested.
  await chmod(directory, 0o700);
}

function setProviderGlobal(providerId: ProviderCredentialId, key: string | undefined): void {
  const providerKeys = apiKeyGlobal[PROVIDER_GLOBAL_KEY] ?? {};
  if (key) {
    providerKeys[providerId] = key;
  } else {
    delete providerKeys[providerId];
  }
  apiKeyGlobal[PROVIDER_GLOBAL_KEY] = providerKeys;

  if (providerId === 'anthropic') {
    apiKeyGlobal[LEGACY_ANTHROPIC_GLOBAL_KEY] = key;
  }
}

export async function storeProviderApiKey(
  providerId: ProviderCredentialId,
  key: string
): Promise<void> {
  if (!safeStorage.isEncryptionAvailable()) {
    throw new Error('Secure storage is not available on this platform');
  }

  const encrypted = safeStorage.encryptString(key);
  await ensureStorageDir(providerId);
  const storagePath = getStoragePath(providerId);
  await writeFile(storagePath, encrypted, { mode: 0o600 });
  // writeFile applies mode only when creating the file, so an existing
  // credential written before this became owner-only is repaired here.
  await chmod(storagePath, 0o600);
  setProviderGlobal(providerId, key);
}

/**
 * Read one provider's encrypted blob and classify it (DEL-04-05-V3-01).
 *
 * Exact state definitions:
 * - `storageUnavailable` — `safeStorage.isEncryptionAvailable()` is false. The
 *   blob is not even opened; nothing can be read or written.
 * - `missing` — no ciphertext could be read (no file, or the read failed), or
 *   the ciphertext decrypts to an empty string (nothing usable is stored).
 * - `decryptFailed` — ciphertext bytes were read but `safeStorage` threw while
 *   decrypting them.
 * - `available` — decrypted to a non-empty key.
 *
 * This read is strictly non-destructive: the blob's bytes are never rewritten,
 * truncated, or deleted here, whatever the outcome. A `decryptFailed` blob is
 * retained exactly as found so the operator can investigate and decide; only
 * an explicit store or remove replaces it. There is no fallback to any plaintext
 * or alternate store. The only mutation is the owner-only mode repair below,
 * which touches permission bits, not content.
 */
export async function readProviderCredential(
  providerId: ProviderCredentialId
): Promise<ProviderCredentialRead> {
  if (!safeStorage.isEncryptionAvailable()) {
    return { state: 'storageUnavailable' };
  }

  const storagePath = getStoragePath(providerId);
  let encrypted: Buffer;
  try {
    encrypted = await readFile(storagePath);
  } catch {
    return { state: 'missing' };
  }

  // Repair credentials stored before the owner-only mode was enforced, so an
  // installation heals on first read rather than only when a key is re-entered.
  await chmod(storagePath, 0o600).catch(() => undefined);
  await chmod(path.dirname(storagePath), 0o700).catch(() => undefined);

  let decrypted: string;
  try {
    decrypted = safeStorage.decryptString(encrypted);
  } catch {
    // Preserve corrupted blobs for operator investigation.
    return { state: 'decryptFailed' };
  }
  if (decrypted.trim().length === 0) {
    return { state: 'missing' };
  }
  return { state: 'available', value: decrypted };
}

/** Typed storage state only — the plaintext, if any, is discarded here. */
export async function probeProviderCredentialStorage(
  providerId: ProviderCredentialId
): Promise<CredentialStorageState> {
  return (await readProviderCredential(providerId)).state;
}

export async function retrieveProviderApiKey(
  providerId: ProviderCredentialId
): Promise<string | null> {
  const read = await readProviderCredential(providerId);
  return read.state === 'available' ? read.value : null;
}

export async function removeProviderApiKey(providerId: ProviderCredentialId): Promise<void> {
  setProviderGlobal(providerId, undefined);
  try {
    await rm(getStoragePath(providerId));
  } catch {
    // Missing files are already in the desired state.
  }
}

export async function hasStoredProviderApiKey(providerId: ProviderCredentialId): Promise<boolean> {
  if (getProviderUiApiKey(providerId)) {
    return true;
  }

  try {
    await readFile(getStoragePath(providerId));
    return true;
  } catch {
    return false;
  }
}

export function isEncryptionAvailable(): boolean {
  return safeStorage.isEncryptionAvailable();
}

/** Load every supported provider credential during Electron startup. */
export async function loadStoredKeyIntoGlobal(): Promise<void> {
  await Promise.all(
    PROVIDER_CREDENTIAL_IDS.map(async (providerId) => {
      const key = await retrieveProviderApiKey(providerId);
      if (key) {
        setProviderGlobal(providerId, key);
      }
    })
  );
}

export function getProviderUiApiKey(providerId: ProviderCredentialId): string | undefined {
  const providerValue = apiKeyGlobal[PROVIDER_GLOBAL_KEY]?.[providerId];
  if (typeof providerValue === 'string' && providerValue.trim().length > 0) {
    return providerValue;
  }
  if (providerId === 'anthropic') {
    return apiKeyGlobal[LEGACY_ANTHROPIC_GLOBAL_KEY];
  }
  return undefined;
}

export type ProviderCredentialStatus = {
  configured: boolean;
  source: ProviderCredentialSource;
  /**
   * Typed safeStorage state of the provider's stored blob. Non-secret and
   * orthogonal to `source`: an environment credential can be in use while the
   * stored blob is `decryptFailed`, and the renderer needs both facts.
   */
  storage: CredentialStorageState;
};

/**
 * Runtime-daemon credential port backed exclusively by Electron safeStorage.
 *
 * Environment credentials remain a read-only compatibility source. Mutations
 * always target the encrypted provider blobs, and values never cross the
 * daemon control API except on an authenticated store request.
 */
export class SafeStorageCredentialStore {
  private async resolve(providerId: string): Promise<{
    value: string | undefined;
    source: ProviderCredentialSource;
    storage: CredentialStorageState;
  }> {
    if (!isProviderCredentialId(providerId)) {
      return { value: undefined, source: 'none', storage: 'missing' };
    }
    const read = await readProviderCredential(providerId);
    if (read.state === 'available') {
      setProviderGlobal(providerId, read.value);
      return { value: read.value, source: 'ui', storage: 'available' };
    }
    // Source precedence is unchanged by the typed state: when the stored blob
    // is not usable (for whatever reason) the environment remains the accepted
    // compatibility source. The state travels alongside so nothing is hidden.
    if (providerId === 'omlx') {
      const value = process.env.CHIRALITY_OMLX_API_KEY?.trim() || undefined;
      return { value, source: value ? 'env' : 'none', storage: read.state };
    }
    const value =
      process.env.ANTHROPIC_API_KEY?.trim() ||
      process.env.CHIRALITY_ANTHROPIC_API_KEY?.trim() ||
      undefined;
    return { value, source: value ? 'env' : 'none', storage: read.state };
  }

  async get(providerId: string): Promise<string | undefined> {
    return (await this.resolve(providerId)).value;
  }

  async status(providerId: string): Promise<ProviderCredentialStatus> {
    const resolved = await this.resolve(providerId);
    return {
      configured: resolved.value !== undefined,
      source: resolved.source,
      storage: resolved.storage
    };
  }

  async set(providerId: string, value: string): Promise<void> {
    if (!isProviderCredentialId(providerId)) {
      throw new Error(`Unsupported credential provider '${providerId}'`);
    }
    const normalized = value.trim();
    if (!normalized) {
      throw new Error('Credential must be a non-empty string');
    }
    await storeProviderApiKey(providerId, normalized);
  }

  async remove(providerId: string): Promise<void> {
    if (!isProviderCredentialId(providerId)) {
      throw new Error(`Unsupported credential provider '${providerId}'`);
    }
    await removeProviderApiKey(providerId);
  }
}

// Anthropic compatibility API. These deliberately retain the original
// filename, global, signatures, and behavior.
export const storeApiKey = (key: string): Promise<void> => storeProviderApiKey('anthropic', key);
export const retrieveApiKey = (): Promise<string | null> => retrieveProviderApiKey('anthropic');
export const removeApiKey = (): Promise<void> => removeProviderApiKey('anthropic');
export const hasStoredApiKey = (): Promise<boolean> => hasStoredProviderApiKey('anthropic');
export const getUiApiKey = (): string | undefined => getProviderUiApiKey('anthropic');
