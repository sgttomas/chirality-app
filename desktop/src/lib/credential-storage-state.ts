/**
 * Typed safeStorage states for a provider credential (DEL-04-05-V3-01 /
 * DEL-02-05-V3-01, AT-057 storage-state portion).
 *
 * Shared by the Electron credential store (main process), the credential IPC
 * projection, and the renderer settings panel so all three agree on one
 * vocabulary. The state describes only the encrypted blob under
 * `userData/credentials/`; it is orthogonal to the daemon-owned
 * `ui | env | none` *source* status, which says where the effective credential
 * comes from. It never carries key material.
 *
 * - `missing`            — no ciphertext is stored for the provider.
 * - `storageUnavailable` — Electron `safeStorage` encryption is not available
 *                          (for example the OS keychain cannot be reached), so
 *                          nothing can be read or written.
 * - `decryptFailed`      — ciphertext is present but `safeStorage` could not
 *                          decrypt it. The bytes are retained untouched; the
 *                          operator must re-enter (or explicitly remove) the key.
 * - `available`          — ciphertext is present and decrypts to a usable key.
 */
export const CREDENTIAL_STORAGE_STATES = [
  'missing',
  'storageUnavailable',
  'decryptFailed',
  'available'
] as const;

export type CredentialStorageState = (typeof CREDENTIAL_STORAGE_STATES)[number];

export function isCredentialStorageState(value: unknown): value is CredentialStorageState {
  return (
    typeof value === 'string' &&
    (CREDENTIAL_STORAGE_STATES as readonly string[]).includes(value)
  );
}
