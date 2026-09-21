import { describe, expect, it } from 'vitest';
import { DIRECT_ENTRY_ROLE_IDS } from '../../lib/portal/agent-matrix-cells';
import { mergeMatrixTargetIntoCurrentUrl } from '../../lib/portal/agent-matrix-launch';
import { resolvePersona } from '../../lib/shell/persona-resolution';
import {
  validatePipelineDispatchIntent
} from '../../lib/pipeline/pipeline-dispatch-contract';

describe('PKG-08 compatibility and authority boundaries', () => {
  it('keeps retired route labels inside the four-role entry boundary', () => {
    expect(resolvePersona('ORCHESTRATE')).toBe('HELP_HUMAN');
    expect(resolvePersona('CHANGE')).toBe('HELP_HUMAN');
    expect(DIRECT_ENTRY_ROLE_IDS).toEqual(['HELP_HUMAN', 'HELPS_HUMANS', 'WORKING_ITEMS']);
  });

  it('round-trips unknown query parameters through the existing matrix compatibility helper', () => {
    expect(
      mergeMatrixTargetIntoCurrentUrl(
        '/pipeline?category=AUDIT',
        '/',
        new URLSearchParams(
          'agent=WORKING_ITEMS&row=NORMATIVE&column=JUDGING&future=keep&category=TASK&scopeKey=old'
        )
      )
    ).toBe('/?agent=WORKING_ITEMS&row=NORMATIVE&column=JUDGING&future=keep&category=AUDIT');
  });

  it('does not turn Pipeline presentation state into delegation authority', () => {
    const result = validatePipelineDispatchIntent(
      {
        category: 'AUDIT',
        option: 'AGENTS'
      },
      {
        knowledgeDecompositionEnabled: false,
        deliverableKeys: [],
        knowledgeTypes: []
      }
    );

    expect(result.valid).toBe(true);
    if (result.valid) {
      expect(result.intent.executionAuthorized).toBe(false);
      expect('delegate_agent' in result.intent).toBe(false);
      expect('approvalRef' in result.intent).toBe(false);
      expect('writeTargets' in result.intent).toBe(false);
    }
  });
});
