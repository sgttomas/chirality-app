import { describe, expect, it } from 'vitest';
import {
  buildDeliverableCompositeKey,
  normalizeTaskScopeMode,
  sanitizeTaskSelection
} from '../../lib/workspace/task-scope';

describe('task scope selection helpers', () => {
  it('builds pkg::id deliverable keys', () => {
    expect(
      buildDeliverableCompositeKey('PKG-02_Desktop_UI_Workflow', 'DEL-02-02')
    ).toBe('PKG-02_Desktop_UI_Workflow::DEL-02-02');
  });

  it('normalizes KNOWLEDGE_TYPES mode only when marker is enabled', () => {
    expect(normalizeTaskScopeMode('KNOWLEDGE_TYPES', true)).toBe('KNOWLEDGE_TYPES');
    expect(normalizeTaskScopeMode('KNOWLEDGE_TYPES', false)).toBe('DELIVERABLES');
    expect(normalizeTaskScopeMode('DELIVERABLES', true)).toBe('DELIVERABLES');
    expect(normalizeTaskScopeMode('unknown', true)).toBe('DELIVERABLES');
  });

  it('clears stale deliverable keys when scan results no longer include the key', () => {
    const next = sanitizeTaskSelection(
      {
        scopeMode: 'DELIVERABLES',
        scopeKey: 'PKG-02_Desktop_UI_Workflow::DEL-02-09',
        targetDeliverableKey: ''
      },
      {
        knowledgeDecompositionEnabled: true,
        deliverableKeys: ['PKG-02_Desktop_UI_Workflow::DEL-02-02'],
        knowledgeTypes: []
      }
    );

    expect(next).toEqual({
      scopeMode: 'DELIVERABLES',
      scopeKey: '',
      targetDeliverableKey: ''
    });
  });

  it('resets KNOWLEDGE_TYPES selection when the decomposition marker is absent', () => {
    const next = sanitizeTaskSelection(
      {
        scopeMode: 'KNOWLEDGE_TYPES',
        scopeKey: 'datasheet',
        targetDeliverableKey: 'PKG-02_Desktop_UI_Workflow::DEL-02-02'
      },
      {
        knowledgeDecompositionEnabled: false,
        deliverableKeys: ['PKG-02_Desktop_UI_Workflow::DEL-02-02'],
        knowledgeTypes: [
          {
            id: 'datasheet',
            matchingDeliverableKeys: ['PKG-02_Desktop_UI_Workflow::DEL-02-02']
          }
        ]
      }
    );

    expect(next).toEqual({
      scopeMode: 'DELIVERABLES',
      scopeKey: '',
      targetDeliverableKey: ''
    });
  });

  it('clears stale knowledge-type target keys that no longer resolve to deliverables', () => {
    const next = sanitizeTaskSelection(
      {
        scopeMode: 'KNOWLEDGE_TYPES',
        scopeKey: 'datasheet',
        targetDeliverableKey: 'PKG-02_Desktop_UI_Workflow::DEL-02-04'
      },
      {
        knowledgeDecompositionEnabled: true,
        deliverableKeys: ['PKG-02_Desktop_UI_Workflow::DEL-02-02'],
        knowledgeTypes: [
          {
            id: 'datasheet',
            matchingDeliverableKeys: ['PKG-02_Desktop_UI_Workflow::DEL-02-02']
          }
        ]
      }
    );

    expect(next).toEqual({
      scopeMode: 'KNOWLEDGE_TYPES',
      scopeKey: 'datasheet',
      targetDeliverableKey: ''
    });
  });

  it('preserves valid knowledge-type target keys', () => {
    const next = sanitizeTaskSelection(
      {
        scopeMode: 'KNOWLEDGE_TYPES',
        scopeKey: 'datasheet',
        targetDeliverableKey: 'PKG-02_Desktop_UI_Workflow::DEL-02-02'
      },
      {
        knowledgeDecompositionEnabled: true,
        deliverableKeys: ['PKG-02_Desktop_UI_Workflow::DEL-02-02'],
        knowledgeTypes: [
          {
            id: 'datasheet',
            matchingDeliverableKeys: ['PKG-02_Desktop_UI_Workflow::DEL-02-02']
          }
        ]
      }
    );

    expect(next).toEqual({
      scopeMode: 'KNOWLEDGE_TYPES',
      scopeKey: 'datasheet',
      targetDeliverableKey: 'PKG-02_Desktop_UI_Workflow::DEL-02-02'
    });
  });
});
