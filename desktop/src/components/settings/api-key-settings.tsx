'use client';

import React, { useCallback, useEffect, useState } from 'react';
import type { ChangeEvent } from 'react';
import type { CredentialStorageState } from '../../lib/credential-storage-state';

export type ApiKeyStatus = {
  hasKey: boolean;
  encryptionAvailable: boolean;
  source: 'ui' | 'env' | 'none';
  /**
   * Typed safeStorage state of the stored blob (DEL-02-05-V3-01 REQ-002):
   * `missing`, `storageUnavailable`, `decryptFailed`, or `available`. Absent
   * only when the bridge could not obtain a real answer.
   */
  storage?: CredentialStorageState;
  /**
   * Set by the bridge when no real answer was obtained (runtime daemon not
   * reachable). Distinct from every storage state: nothing is known.
   */
  unavailable?: boolean;
  /** Bridge-side error text for a non-answer (daemon unreachable, invalid status, denied). */
  error?: string;
};

export type ApiKeySettingsViewProps = {
  title?: string;
  environmentVariable?: string;
  placeholder?: string;
  keyInput: string;
  revealed: boolean;
  status: ApiKeyStatus | null;
  error: string | null;
  saving: boolean;
  bridgeAvailable: boolean;
  onKeyInputChange: (value: string) => void;
  onRevealToggle: () => void;
  onSave: () => void;
  onRemove: () => void;
};

type ApiKeyStoreResult = {
  ok: boolean;
  error?: string;
};

type ChiralityApiKeyBridge = {
  store: (key: string) => Promise<ApiKeyStoreResult>;
  remove: () => Promise<ApiKeyStoreResult>;
  status: () => Promise<ApiKeyStatus>;
};

type ProviderCredentialId = 'anthropic' | 'omlx';

type ChiralityProviderApiKeyBridge = {
  store: (providerId: ProviderCredentialId, key: string) => Promise<ApiKeyStoreResult>;
  remove: (providerId: ProviderCredentialId) => Promise<ApiKeyStoreResult>;
  status: (providerId: ProviderCredentialId) => Promise<ApiKeyStatus>;
};

type ChiralityWindow = typeof window & {
  chirality?: {
    apiKey?: ChiralityApiKeyBridge;
    providerApiKey?: ChiralityProviderApiKeyBridge;
  };
};

function getApiKeyBridge(providerId: ProviderCredentialId): ChiralityApiKeyBridge | undefined {
  if (typeof window === 'undefined') {
    return undefined;
  }
  const chirality = (window as ChiralityWindow).chirality;
  if (chirality?.providerApiKey) {
    return {
      store: (key) => chirality.providerApiKey!.store(providerId, key),
      remove: () => chirality.providerApiKey!.remove(providerId),
      status: () => chirality.providerApiKey!.status(providerId)
    };
  }
  return providerId === 'anthropic' ? chirality?.apiKey : undefined;
}

export function ApiKeySettings(): JSX.Element {
  return (
    <>
      <ProviderApiKeySettings
        providerId="anthropic"
        title="Anthropic API Key"
        environmentVariable="ANTHROPIC_API_KEY"
        placeholder="sk-ant-..."
      />
      <ProviderApiKeySettings
        providerId="omlx"
        title="oMLX API Key"
        environmentVariable="CHIRALITY_OMLX_API_KEY"
        placeholder="Enter the key configured in oMLX"
      />
    </>
  );
}

type ProviderApiKeySettingsProps = {
  providerId: ProviderCredentialId;
  title: string;
  environmentVariable: string;
  placeholder: string;
};

function ProviderApiKeySettings({
  providerId,
  title,
  environmentVariable,
  placeholder
}: ProviderApiKeySettingsProps): JSX.Element {
  const [keyInput, setKeyInput] = useState('');
  const [revealed, setRevealed] = useState(false);
  const [status, setStatus] = useState<ApiKeyStatus | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [saving, setSaving] = useState(false);
  const [bridgeAvailable, setBridgeAvailable] = useState(false);

  const refreshStatus = useCallback(async () => {
    const bridge = getApiKeyBridge(providerId);
    if (!bridge) {
      setBridgeAvailable(false);
      return;
    }

    setBridgeAvailable(true);
    try {
      const result = await bridge.status();
      setStatus(result);
    } catch {
      setStatus(null);
    }
  }, [providerId]);

  useEffect(() => {
    void refreshStatus();
  }, [refreshStatus]);

  async function handleSave(): Promise<void> {
    const bridge = getApiKeyBridge(providerId);
    if (!bridge) {
      setError('Secure storage is not available (not running in Electron)');
      return;
    }

    const trimmed = keyInput.trim();
    if (!trimmed) {
      setError('Please enter an API key');
      return;
    }

    setSaving(true);
    setError(null);

    try {
      const result = await bridge.store(trimmed);
      if (!result.ok) {
        setError(result.error ?? 'Failed to save key');
        return;
      }

      setKeyInput('');
      setRevealed(false);
      await refreshStatus();
    } catch {
      setError('Failed to save key. Check system storage availability.');
    } finally {
      setSaving(false);
    }
  }

  async function handleRemove(): Promise<void> {
    const bridge = getApiKeyBridge(providerId);
    if (!bridge) {
      return;
    }

    setError(null);

    try {
      const result = await bridge.remove();
      if (!result.ok) {
        setError(result.error ?? 'Failed to remove key');
        return;
      }

      await refreshStatus();
    } catch {
      setError('Failed to remove key');
    }
  }

  return (
    <ApiKeySettingsView
      title={title}
      environmentVariable={environmentVariable}
      placeholder={placeholder}
      keyInput={keyInput}
      revealed={revealed}
      status={status}
      error={error}
      saving={saving}
      bridgeAvailable={bridgeAvailable}
      onKeyInputChange={(value) => {
        setKeyInput(value);
        if (error) {
          setError(null);
        }
      }}
      onRevealToggle={() => {
        setRevealed(!revealed);
      }}
      onSave={() => void handleSave()}
      onRemove={() => void handleRemove()}
    />
  );
}

type RenderedStorageState = CredentialStorageState | 'unknown';

/** True when the bridge answered without a real credential status. */
function isNonAnswer(status: ApiKeyStatus): boolean {
  return status.unavailable === true || typeof status.error === 'string';
}

/**
 * The storage state the panel renders. A bridge that reports the typed state is
 * used as-is. A non-answer (daemon unreachable, denied, invalid) is `unknown`
 * — it says nothing about the keychain, so it must never be shown as
 * `storageUnavailable`. Only an older bridge that reports neither a typed
 * state nor a non-answer, and says `encryptionAvailable: false`, is mapped to
 * `storageUnavailable`; anything else without a typed state is `unknown`.
 */
function resolveStorageState(status: ApiKeyStatus | null): RenderedStorageState {
  if (!status) {
    return 'unknown';
  }
  if (status.storage) {
    return status.storage;
  }
  if (isNonAnswer(status)) {
    return 'unknown';
  }
  return status.encryptionAvailable ? 'unknown' : 'storageUnavailable';
}

function statusLabel(status: ApiKeyStatus | null, storageState: RenderedStorageState): string {
  if (!status) {
    return 'Checking...';
  }
  if (!status.storage && isNonAnswer(status)) {
    return 'Cannot determine credential status right now';
  }
  if (status.source === 'ui') {
    return 'Key configured (stored in secure storage)';
  }
  if (status.source === 'env') {
    return 'Key configured (from environment variable)';
  }
  if (storageState === 'decryptFailed') {
    return 'Stored key cannot be read';
  }
  if (storageState === 'storageUnavailable') {
    return 'Secure storage is unavailable';
  }
  return 'No API key configured';
}

export function ApiKeySettingsView({
  title = 'Anthropic API Key',
  environmentVariable = 'ANTHROPIC_API_KEY',
  placeholder = 'sk-ant-...',
  keyInput,
  revealed,
  status,
  error,
  saving,
  bridgeAvailable,
  onKeyInputChange,
  onRevealToggle,
  onSave,
  onRemove
}: ApiKeySettingsViewProps): JSX.Element {
  const storageState = resolveStorageState(status);
  const storageUnavailable = storageState === 'storageUnavailable';
  const decryptFailed = storageState === 'decryptFailed';
  const nonAnswer = status !== null && !status.storage && isNonAnswer(status);
  // Entry stays available while the bridge is still checking, and is hidden
  // when it reported that storage cannot be used or that it could not answer
  // (the behaviour the panel had before the typed states).
  const canUseStorage =
    bridgeAvailable && !storageUnavailable && status?.encryptionAvailable !== false;

  return (
    <div className="api-key-settings">
      <h3 className="api-key-settings-title">{title}</h3>

      <p
        className="api-key-status"
        data-source={status?.source ?? 'unknown'}
        data-storage={storageState}
        data-answer={nonAnswer ? 'unavailable' : 'status'}
      >
        {statusLabel(status, storageState)}
      </p>

      {nonAnswer && status?.error ? (
        <p className="api-key-hint" data-status-error="true">
          {status.error}
        </p>
      ) : null}

      {storageUnavailable ? (
        <p className="api-key-warning" data-storage-state="storageUnavailable">
          Secure storage is not available on this platform. Chirality cannot read or save a
          stored key until the operating system keychain is available, and any previously
          stored key is left in place unread. To continue now, set the{' '}
          <code>{environmentVariable}</code> environment variable and restart Chirality.
        </p>
      ) : null}

      {decryptFailed ? (
        <p className="api-key-warning" data-storage-state="decryptFailed">
          The stored key could not be decrypted, so it cannot be used. The previous encrypted
          entry has been kept unchanged and nothing was deleted. Re-enter the key below to
          replace it, or remove the stored entry explicitly.
          {status?.source === 'env'
            ? ` Until then, Chirality is using the ${environmentVariable} environment variable.`
            : ''}
        </p>
      ) : null}

      {canUseStorage ? (
        <>
          <div className="api-key-input-row">
            <input
              type={revealed ? 'text' : 'password'}
              className="api-key-input"
              value={keyInput}
              onChange={(event: ChangeEvent<HTMLInputElement>) => {
                onKeyInputChange(event.target.value);
              }}
              placeholder={placeholder}
              autoComplete="off"
              autoCorrect="off"
              autoCapitalize="off"
              spellCheck={false}
              data-lpignore="true"
              data-1p-ignore="true"
            />
            <button
              type="button"
              className="button-muted"
              onClick={onRevealToggle}
            >
              {revealed ? 'Hide' : 'Reveal'}
            </button>
            <button
              type="button"
              onClick={onSave}
              disabled={saving || !keyInput.trim()}
            >
              {saving ? 'Saving...' : 'Save Key'}
            </button>
          </div>

          {status?.source === 'ui' || decryptFailed ? (
            <button
              type="button"
              className="button-muted api-key-remove"
              onClick={onRemove}
            >
              Remove Stored Key
            </button>
          ) : null}
        </>
      ) : null}

      {!bridgeAvailable ? (
        <p className="api-key-hint">
          Running outside Electron. Set the <code>{environmentVariable}</code> environment variable
          to configure the API key.
        </p>
      ) : null}

      {error ? <p className="api-key-error">{error}</p> : null}
    </div>
  );
}
