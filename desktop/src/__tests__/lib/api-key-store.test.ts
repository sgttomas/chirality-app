import { afterEach, describe, expect, it } from 'vitest';
import {
  getOmlxApiKey,
  getProviderApiKey,
  getProviderUiApiKey,
  getUiApiKey
} from '../../lib/harness/api-key-store';

const globalState = globalThis as typeof globalThis & {
  __CHIRALITY_UI_API_KEY__?: string;
  __CHIRALITY_PROVIDER_API_KEYS__?: Partial<Record<'anthropic' | 'omlx', string>>;
};

afterEach(() => {
  delete globalState.__CHIRALITY_UI_API_KEY__;
  delete globalState.__CHIRALITY_PROVIDER_API_KEYS__;
  delete process.env.ANTHROPIC_API_KEY;
  delete process.env.CHIRALITY_ANTHROPIC_API_KEY;
  delete process.env.CHIRALITY_OMLX_API_KEY;
});

describe('provider API key store', () => {
  it('preserves the legacy Anthropic global and isolates the oMLX key', () => {
    globalState.__CHIRALITY_UI_API_KEY__ = 'legacy-anthropic';
    globalState.__CHIRALITY_PROVIDER_API_KEYS__ = { omlx: 'ui-omlx' };

    expect(getUiApiKey()).toBe('legacy-anthropic');
    expect(getProviderUiApiKey('omlx')).toBe('ui-omlx');
    expect(getOmlxApiKey()).toBe('ui-omlx');
  });

  it('uses only the oMLX environment variable as its fallback', () => {
    process.env.ANTHROPIC_API_KEY = 'anthropic-secret';
    expect(getOmlxApiKey()).toBeUndefined();

    process.env.CHIRALITY_OMLX_API_KEY = '  omlx-secret  ';
    expect(getOmlxApiKey()).toBe('omlx-secret');
    expect(getProviderApiKey('anthropic')).toBe('anthropic-secret');
  });
});
