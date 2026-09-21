import { getProviderUiApiKey } from './api-key-store';

function asNonEmptyString(value: string | undefined): string | undefined {
  if (typeof value !== 'string') {
    return undefined;
  }
  const trimmed = value.trim();
  return trimmed.length > 0 ? trimmed : undefined;
}

function escapeRegExp(value: string): string {
  return value.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

function toLowercasePercentEncoding(value: string): string {
  return value.replace(/%[0-9A-F]{2}/g, (match) => match.toLowerCase());
}

function addEncodedKeyVariantCandidates(variants: Set<string>, encoded: string): Set<string> {
  const nextRoundInputs = new Set<string>();
  if (encoded.length === 0) {
    return nextRoundInputs;
  }

  const lowercaseEncoded = toLowercasePercentEncoding(encoded);
  variants.add(encoded);
  variants.add(lowercaseEncoded);
  nextRoundInputs.add(encoded);
  nextRoundInputs.add(lowercaseEncoded);

  if (encoded.includes('%20')) {
    const queryEncoded = encoded.replace(/%20/g, '+');
    variants.add(queryEncoded);
    nextRoundInputs.add(queryEncoded);
  }
  if (lowercaseEncoded.includes('%20')) {
    const lowercaseQueryEncoded = lowercaseEncoded.replace(/%20/g, '+');
    variants.add(lowercaseQueryEncoded);
    nextRoundInputs.add(lowercaseQueryEncoded);
  }

  return nextRoundInputs;
}

function addUrlEncodedKeyVariants(variants: Set<string>, key: string): void {
  let roundInputs = new Set<string>([key]);
  for (let index = 0; index < 2; index += 1) {
    const nextRoundInputs = new Set<string>();
    for (const roundInput of roundInputs) {
      const encoded = encodeURIComponent(roundInput);
      const candidates = addEncodedKeyVariantCandidates(variants, encoded);
      for (const candidate of candidates) {
        nextRoundInputs.add(candidate);
      }
    }

    if (nextRoundInputs.size === 0) {
      break;
    }
    roundInputs = nextRoundInputs;
  }
}

export function readConfiguredApiKeyVariants(): string[] {
  const configuredKeys = [
    getProviderUiApiKey('anthropic'),
    getProviderUiApiKey('omlx'),
    asNonEmptyString(process.env.ANTHROPIC_API_KEY),
    asNonEmptyString(process.env.CHIRALITY_ANTHROPIC_API_KEY),
    asNonEmptyString(process.env.CHIRALITY_OMLX_API_KEY)
  ].filter((value): value is string => Boolean(value));
  const variants = new Set<string>();
  for (const key of configuredKeys) {
    variants.add(key);
    addUrlEncodedKeyVariants(variants, key);
  }

  return Array.from(variants).sort((a, b) => b.length - a.length);
}

export function redactConfiguredApiKeys(message: string | undefined): string | undefined {
  if (typeof message !== 'string' || message.length === 0) {
    return message;
  }

  const configuredApiKeys = readConfiguredApiKeyVariants();
  if (configuredApiKeys.length === 0) {
    return message;
  }

  const pattern = configuredApiKeys.map(escapeRegExp).join('|');
  return message.replace(new RegExp(pattern, 'g'), '[REDACTED_API_KEY]');
}

export function redactJsonLike<T>(value: T): T {
  if (typeof value === 'string') {
    return redactConfiguredApiKeys(value) as T;
  }
  if (Array.isArray(value)) {
    return value.map((item) => redactJsonLike(item)) as T;
  }
  if (value && typeof value === 'object') {
    return Object.fromEntries(
      Object.entries(value as Record<string, unknown>).map(([key, entry]) => [
        key,
        redactJsonLike(entry)
      ])
    ) as T;
  }
  return value;
}
