import { afterEach, describe, expect, it } from 'vitest';
import {
  readConfiguredApiKeyVariants,
  redactConfiguredApiKeys,
  redactJsonLike
} from '../../lib/harness/run-logger';

afterEach(() => {
  delete process.env.ANTHROPIC_API_KEY;
  delete process.env.CHIRALITY_ANTHROPIC_API_KEY;
  delete process.env.CHIRALITY_OMLX_API_KEY;
  delete (globalThis as typeof globalThis & {
    __CHIRALITY_PROVIDER_API_KEYS__?: Partial<Record<'anthropic' | 'omlx', string>>;
  }).__CHIRALITY_PROVIDER_API_KEYS__;
});

function lowercasePercentEncoding(value: string): string {
  return value.replace(/%[0-9A-F]{2}/g, (match) => match.toLowerCase());
}

describe('run logger redaction', () => {
  it('redacts raw and encoded configured API-key variants', () => {
    const key = 'test key/with space';
    process.env.ANTHROPIC_API_KEY = key;

    const encoded = encodeURIComponent(key);
    const lowercaseEncoded = lowercasePercentEncoding(encoded);
    const queryEncoded = encoded.replace(/%20/g, '+');
    const doubleEncoded = encodeURIComponent(encoded);
    const lowercaseDoubleEncoded = lowercasePercentEncoding(doubleEncoded);
    const doubleQueryEncoded = encodeURIComponent(queryEncoded);
    const variants = [
      key,
      encoded,
      lowercaseEncoded,
      queryEncoded,
      doubleEncoded,
      lowercaseDoubleEncoded,
      doubleQueryEncoded
    ];

    expect(readConfiguredApiKeyVariants()).toEqual(expect.arrayContaining(variants));
    for (const variant of variants) {
      const redacted = redactConfiguredApiKeys(`diagnostic=${variant}`);
      expect(redacted).toBe('diagnostic=[REDACTED_API_KEY]');
      expect(redacted).not.toContain(variant);
    }
  });

  it('redacts overlapping configured keys longest-first', () => {
    process.env.ANTHROPIC_API_KEY = 'KEY';
    process.env.CHIRALITY_ANTHROPIC_API_KEY = 'KEY_LONG';

    expect(redactConfiguredApiKeys('canonical=KEY alias=KEY_LONG')).toBe(
      'canonical=[REDACTED_API_KEY] alias=[REDACTED_API_KEY]'
    );
  });

  it('redacts nested JSON-like values while preserving non-secret audit metadata', () => {
    process.env.CHIRALITY_ANTHROPIC_API_KEY = 'sk-test-nested-secret';

    const redacted = redactJsonLike({
      type: 'hook.failed',
      status: 500,
      diagnostics: [
        'stderr contains sk-test-nested-secret',
        { message: 'Bearer sk-test-nested-secret', retryable: false }
      ]
    });

    expect(redacted).toEqual({
      type: 'hook.failed',
      status: 500,
      diagnostics: [
        'stderr contains [REDACTED_API_KEY]',
        { message: 'Bearer [REDACTED_API_KEY]', retryable: false }
      ]
    });
    expect(JSON.stringify(redacted)).not.toContain('sk-test-nested-secret');
  });

  it('redacts both secure UI and environment oMLX credentials', () => {
    const uiKey = 'omlx-ui-secret/with space';
    const envKey = 'omlx-env-secret?token=true';
    (globalThis as typeof globalThis & {
      __CHIRALITY_PROVIDER_API_KEYS__?: Partial<Record<'anthropic' | 'omlx', string>>;
    }).__CHIRALITY_PROVIDER_API_KEYS__ = { omlx: uiKey };
    process.env.CHIRALITY_OMLX_API_KEY = envKey;

    const redacted = redactJsonLike({
      uiDiagnostic: `Bearer ${uiKey}`,
      encodedUiDiagnostic: encodeURIComponent(uiKey),
      envDiagnostic: `authorization=${envKey}`,
      encodedEnvDiagnostic: encodeURIComponent(envKey)
    });

    expect(redacted).toEqual({
      uiDiagnostic: 'Bearer [REDACTED_API_KEY]',
      encodedUiDiagnostic: '[REDACTED_API_KEY]',
      envDiagnostic: 'authorization=[REDACTED_API_KEY]',
      encodedEnvDiagnostic: '[REDACTED_API_KEY]'
    });
    expect(JSON.stringify(redacted)).not.toContain(uiKey);
    expect(JSON.stringify(redacted)).not.toContain(envKey);
  });
});
