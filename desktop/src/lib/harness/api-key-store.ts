/** Server-side access to Electron-owned provider credentials. */

export type ProviderCredentialId = 'anthropic' | 'omlx';

const LEGACY_ANTHROPIC_GLOBAL_KEY = '__CHIRALITY_UI_API_KEY__';
const PROVIDER_GLOBAL_KEY = '__CHIRALITY_PROVIDER_API_KEYS__';

type ApiKeyGlobal = typeof globalThis & {
  [LEGACY_ANTHROPIC_GLOBAL_KEY]?: string;
  [PROVIDER_GLOBAL_KEY]?: Partial<Record<ProviderCredentialId, string>>;
};

const apiKeyGlobal = globalThis as ApiKeyGlobal;

function asNonEmptyString(value: string | undefined): string | undefined {
  if (typeof value !== 'string') {
    return undefined;
  }
  const trimmed = value.trim();
  return trimmed.length > 0 ? trimmed : undefined;
}

export function getProviderUiApiKey(providerId: ProviderCredentialId): string | undefined {
  const providerValue = asNonEmptyString(apiKeyGlobal[PROVIDER_GLOBAL_KEY]?.[providerId]);
  if (providerValue) {
    return providerValue;
  }
  return providerId === 'anthropic'
    ? asNonEmptyString(apiKeyGlobal[LEGACY_ANTHROPIC_GLOBAL_KEY])
    : undefined;
}

export function getProviderApiKey(providerId: ProviderCredentialId): string | undefined {
  const uiKey = getProviderUiApiKey(providerId);
  if (uiKey) {
    return uiKey;
  }
  if (providerId === 'omlx') {
    return asNonEmptyString(process.env.CHIRALITY_OMLX_API_KEY);
  }
  return (
    asNonEmptyString(process.env.ANTHROPIC_API_KEY) ??
    asNonEmptyString(process.env.CHIRALITY_ANTHROPIC_API_KEY)
  );
}

export function hasProviderApiKey(providerId: ProviderCredentialId): boolean {
  return getProviderApiKey(providerId) !== undefined;
}

// Anthropic compatibility helpers retain their existing UI-only semantics.
export function getUiApiKey(): string | undefined {
  return getProviderUiApiKey('anthropic');
}

export function hasUiApiKey(): boolean {
  return getUiApiKey() !== undefined;
}

export function getOmlxApiKey(): string | undefined {
  return getProviderApiKey('omlx');
}
