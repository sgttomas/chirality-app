import { describe, expect, it } from 'vitest';
import type { HarnessErrorType } from '@chirality/runtime-contracts/types';
import { asHarnessError } from '@chirality/runtime-contracts/errors';

const providerNeutralTypes = [
  'ENGINE_UNAVAILABLE',
  'MODEL_UNAVAILABLE',
  'PROVIDER_AUTH_FAILURE',
  'PROVIDER_PROTOCOL_FAILURE',
  'CONTEXT_EXHAUSTED'
] as const satisfies readonly HarnessErrorType[];

describe('asHarnessError', () => {
  it.each(providerNeutralTypes)('retains the provider-neutral structural type %s', (type) => {
    const converted = asHarnessError({
      type,
      status: 503,
      message: `typed ${type}`,
      details: { provider: 'omlx' }
    });

    expect(converted).toMatchObject({
      type,
      status: 503,
      message: `typed ${type}`,
      details: { provider: 'omlx' }
    });
  });

  it('still falls back to SDK_FAILURE for unknown structural error types', () => {
    const converted = asHarnessError({
      type: 'UNRECOGNIZED_PROVIDER_ERROR',
      status: 503,
      message: 'must not pass through'
    });

    expect(converted).toMatchObject({
      type: 'SDK_FAILURE',
      status: 500,
      message: 'Unexpected harness runtime error'
    });
  });
});
