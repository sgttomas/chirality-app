import { describe, expect, it } from 'vitest';
import { mergeMatrixTargetIntoCurrentUrl } from '../../lib/portal/agent-matrix-launch';

describe('matrix launch URL merging', () => {
  it('keeps persona launches on the current loop shell route', () => {
    expect(
      mergeMatrixTargetIntoCurrentUrl(
        '/?agent=CHANGE&row=EVALUATIVE&column=JUDGING',
        '/workbench',
        new URLSearchParams('category=TASK')
      )
    ).toBe('/workbench?category=TASK&agent=CHANGE&row=EVALUATIVE&column=JUDGING');
  });

  it('opens Pipeline intent in place and clears stale Pipeline scope query', () => {
    expect(
      mergeMatrixTargetIntoCurrentUrl(
        '/pipeline?category=AUDIT',
        '/',
        new URLSearchParams(
          'agent=WORKING_ITEMS&category=TASK&taskScopeMode=DELIVERABLES&scopeKey=pkg%3A%3Aold'
        )
      )
    ).toBe('/?agent=WORKING_ITEMS&category=AUDIT');
  });
});
