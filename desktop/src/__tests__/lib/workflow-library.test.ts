import { describe, expect, it } from 'vitest';
import type { MethodDescriptor } from '../../lib/harness/method-selection-client';
import { groupWorkflowLibrary, methodMatchesQuery, workflowDisplayName } from '../../lib/shell/workflow-library';

const method = (name: string, input: Partial<MethodDescriptor> = {}): MethodDescriptor => ({
  qualifiedId: `${input.sourceRootId ?? 'chirality-root'}/workflow/${name}`, sourceRootId: input.sourceRootId ?? 'chirality-root', source: 'bundled', kind: 'workflow', name,
  description: `${name} description`, central: false, compatibility: 'canonical', executionRoleIds: ['TASK'], resources: [], ...input
});

describe('groupWorkflowLibrary', () => {
  it('follows the catalog navigation and source for every bucket, sorting by recorded order', () => {
    const plan = { key: 'plan-organize', label: 'Plan & organize', order: 0 };
    const review = { key: 'review-check', label: 'Review & check', order: 6 };
    const library = groupWorkflowLibrary([
      method('review', { navigation: { category: 'core', tier: 'primary', order: 7, displayName: 'Review results' } }),
      method('project-setup', { central: true, navigation: { category: 'core', tier: 'primary', order: 0 } }),
      method('audit-agents', { navigation: { category: 'specialist', tier: 'primary', order: 0, group: review } }),
      method('evaluation-report', { navigation: { category: 'specialist', tier: 'supporting', order: 9, group: review } }),
      method('preparation', { navigation: { category: 'specialist', tier: 'primary', order: 0, group: plan } }),
      method('pdf2md-page', { compatibility: 'legacy', navigation: { category: 'superseded', tier: 'primary', order: 1, supersededBy: 'pdf2md-page-full' } }),
      method('saved-plan', { source: 'project', sourceRootId: 'project-1' }),
      method('mine', { source: 'user', sourceRootId: 'user-1' }),
      method('skill-x', { kind: 'skill' }),
      method('unplaced')
    ]);
    expect(library.core.map(workflowDisplayName)).toEqual(['project-setup', 'Review results']);
    expect(library.specialist.map(group => [group.label, group.primary.map(item => item.name), group.supporting.map(item => item.name)])).toEqual([
      ['Plan & organize', ['preparation'], []],
      ['Review & check', ['audit-agents'], ['evaluation-report']]
    ]);
    expect(library.projectSpecific.map(item => item.name)).toEqual(['saved-plan']);
    expect(library.personal.map(item => item.name)).toEqual(['mine']);
    expect(library.superseded.map(item => item.navigation?.supersededBy)).toEqual(['pdf2md-page-full']);
    expect(library.unplaced.map(item => item.name)).toEqual(['unplaced']);
  });

  it('matches queries against identifier, display name, description, group and metadata', () => {
    const item = method('task-management', { navigation: { category: 'core', tier: 'primary', order: 6, displayName: 'Manage tasks' }, metadata: { applicability: ['Backlog grooming'] } });
    for (const query of ['manage', 'TASK-MANAGEMENT', 'description', 'backlog', '  ']) expect(methodMatchesQuery(item, query)).toBe(true);
    expect(methodMatchesQuery(item, 'estimate')).toBe(false);
  });
});
