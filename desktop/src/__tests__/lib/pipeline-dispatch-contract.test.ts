import { describe, expect, it } from 'vitest';
import {
  PIPELINE_CATEGORY_OPTIONS,
  PIPELINE_CATEGORY_ORDER,
  mergePipelineQueryParameters,
  validatePipelineDispatchIntent
} from '../../lib/pipeline/pipeline-dispatch-contract';

const context = {
  knowledgeDecompositionEnabled: true,
  deliverableKeys: ['pkg::DEL-01', 'pkg::DEL-02'],
  knowledgeTypes: [
    {
      id: 'datasheet',
      matchingDeliverableKeys: ['pkg::DEL-01']
    }
  ]
};

describe('presentation-neutral Pipeline dispatch contract', () => {
  it('preserves the exact DECOMP/PREP/TASK/AUDIT taxonomy and option states', () => {
    expect(PIPELINE_CATEGORY_ORDER).toEqual(['DECOMP', 'PREP', 'TASK', 'AUDIT']);
    expect(PIPELINE_CATEGORY_OPTIONS.DECOMP).toEqual([
      { value: 'SOFTWARE', label: 'SOFTWARE', enabled: true },
      { value: 'PROJECT', label: 'PROJECT', enabled: true },
      { value: 'DOMAIN', label: 'DOMAIN', enabled: true },
      { value: 'BASE', label: 'BASE (create new)', enabled: false }
    ]);
    expect(PIPELINE_CATEGORY_OPTIONS.PREP).toEqual([
      { value: 'PREPARATION', label: 'PREPARATION', enabled: true },
      { value: '4_DOCUMENTS', label: '4_DOCUMENTS', enabled: true },
      { value: 'CHIRALITY_FRAMEWORK', label: 'CHIRALITY_FRAMEWORK', enabled: true },
      { value: 'CHIRALITY_LENS', label: 'CHIRALITY_LENS', enabled: true }
    ]);
    expect(PIPELINE_CATEGORY_OPTIONS.TASK.map(({ value, enabled }) => [value, enabled])).toEqual([
      ['SCOPE_CHANGE', true],
      ['SCOPE_PREP', true],
      ['ESTIMATE_PREP', true],
      ['AUDIT_PREP', true],
      ['SCHEDULE_PREP', true],
      ['ESTIMATING', false],
      ['SCHEDULING', false]
    ]);
    expect(PIPELINE_CATEGORY_OPTIONS.AUDIT.map(({ value, enabled }) => [value, enabled])).toEqual([
      ['AGENTS', true],
      ['DEPENDENCIES', true],
      ['ESTIMATES', false],
      ['REFERENCES', true],
      ['SCHEDULES', false],
      ['SCOPE', true]
    ]);
  });

  it('returns inert data for an admitted deliverable-scoped TASK intent', () => {
    const result = validatePipelineDispatchIntent(
      {
        category: 'TASK',
        option: 'SCOPE_CHANGE',
        taskScopeMode: 'DELIVERABLES',
        scopeKey: 'pkg::DEL-01'
      },
      context
    );

    expect(result).toEqual({
      valid: true,
      intent: {
        kind: 'PIPELINE_DISPATCH_INTENT',
        executionAuthorized: false,
        category: 'TASK',
        option: 'SCOPE_CHANGE',
        taskScope: {
          mode: 'DELIVERABLES',
          scopeKey: 'pkg::DEL-01'
        }
      },
      issues: []
    });
    if (result.valid) {
      expect(Object.values(result.intent).some((value) => typeof value === 'function')).toBe(
        false
      );
      expect('delegate' in result.intent).toBe(false);
      expect('execute' in result.intent).toBe(false);
    }
  });

  it('rejects disabled options without hiding them', () => {
    const result = validatePipelineDispatchIntent(
      {
        category: 'DECOMP',
        option: 'BASE'
      },
      context
    );

    expect(PIPELINE_CATEGORY_OPTIONS.DECOMP.find((option) => option.value === 'BASE')).toEqual({
      value: 'BASE',
      label: 'BASE (create new)',
      enabled: false
    });
    expect(result).toEqual({
      valid: false,
      issues: [
        {
          code: 'OPTION_DISABLED',
          message: 'Option BASE is visible but disabled.'
        }
      ]
    });
  });

  it('requires exact recorded scope and a target for knowledge-type TASK intent', () => {
    const missingTarget = validatePipelineDispatchIntent(
      {
        category: 'TASK',
        option: 'SCOPE_CHANGE',
        taskScopeMode: 'KNOWLEDGE_TYPES',
        scopeKey: 'datasheet'
      },
      context
    );
    const admitted = validatePipelineDispatchIntent(
      {
        category: 'TASK',
        option: 'SCOPE_CHANGE',
        taskScopeMode: 'KNOWLEDGE_TYPES',
        scopeKey: 'datasheet',
        targetDeliverableKey: 'pkg::DEL-01'
      },
      context
    );

    expect(missingTarget).toEqual({
      valid: false,
      issues: [
        {
          code: 'TARGET_DELIVERABLE_REQUIRED',
          message: 'KNOWLEDGE_TYPES dispatch requires a target deliverable.'
        }
      ]
    });
    expect(admitted.valid).toBe(true);
  });

  it('preserves persona, matrix, and unknown query parameters while patching Pipeline intent', () => {
    const next = mergePipelineQueryParameters(
      'agent=WORKING_ITEMS&row=NORMATIVE&column=JUDGING&future=keep&scopeKey=old',
      {
        category: 'TASK',
        taskScopeMode: 'DELIVERABLES',
        scopeKey: 'pkg::DEL-01',
        targetDeliverableKey: null
      }
    );

    expect(next.get('agent')).toBe('WORKING_ITEMS');
    expect(next.get('row')).toBe('NORMATIVE');
    expect(next.get('column')).toBe('JUDGING');
    expect(next.get('future')).toBe('keep');
    expect(next.get('category')).toBe('TASK');
    expect(next.get('taskScopeMode')).toBe('DELIVERABLES');
    expect(next.get('scopeKey')).toBe('pkg::DEL-01');
    expect(next.has('targetDeliverableKey')).toBe(false);
  });
});
