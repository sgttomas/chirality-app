import { describe, expect, it } from 'vitest';

const facadePairs = [
  ['root', () => import('@chirality/harness-contract'), () => import('@chirality/runtime-contracts')],
  [
    'agent-engine-port',
    () => import('@chirality/harness-contract/agent-engine-port'),
    () => import('@chirality/runtime-contracts/agent-engine-port')
  ],
  [
    'domain-profile',
    () => import('@chirality/harness-contract/domain-profile'),
    () => import('@chirality/runtime-contracts/domain-profile')
  ],
  [
    'engine-conformance',
    () => import('@chirality/harness-contract/engine-conformance'),
    () => import('@chirality/runtime-contracts/engine-conformance')
  ],
  [
    'errors',
    () => import('@chirality/harness-contract/errors'),
    () => import('@chirality/runtime-contracts/errors')
  ],
  [
    'event-schema',
    () => import('@chirality/harness-contract/event-schema'),
    () => import('@chirality/runtime-contracts/event-schema')
  ],
  [
    'mcp/tool-names',
    () => import('@chirality/harness-contract/mcp/tool-names'),
    () => import('@chirality/runtime-contracts/mcp/tool-names')
  ],
  [
    'operation-proposal',
    () => import('@chirality/harness-contract/operation-proposal'),
    () => import('@chirality/runtime-contracts/operation-proposal')
  ],
  [
    'sdk-version',
    () => import('@chirality/harness-contract/sdk-version'),
    () => import('@chirality/runtime-contracts/sdk-version')
  ],
  [
    'tool-catalog',
    () => import('@chirality/harness-contract/tool-catalog'),
    () => import('@chirality/runtime-contracts/tool-catalog')
  ],
  [
    'tool-descriptor',
    () => import('@chirality/harness-contract/tool-descriptor'),
    () => import('@chirality/runtime-contracts/tool-descriptor')
  ],
  [
    'transcript-replay',
    () => import('@chirality/harness-contract/transcript-replay'),
    () => import('@chirality/runtime-contracts/transcript-replay')
  ],
  [
    'types',
    () => import('@chirality/harness-contract/types'),
    () => import('@chirality/runtime-contracts/types')
  ]
] as const;

describe('deprecated harness-contract rollback facade', () => {
  it.each(facadePairs)(
    '%s resolves every runtime export to the canonical module identity',
    async (_label, loadFacade, loadCanonical) => {
      const facade = (await loadFacade()) as Record<string, unknown>;
      const canonical = (await loadCanonical()) as Record<string, unknown>;

      expect(Object.keys(facade).sort()).toEqual(Object.keys(canonical).sort());
      for (const exportName of Object.keys(canonical)) {
        expect(facade[exportName]).toBe(canonical[exportName]);
      }
    }
  );
});
