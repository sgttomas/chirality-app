import { createElement } from 'react';
import { renderToStaticMarkup } from 'react-dom/server';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import {
  WorkbenchLifecycleTransitionForm,
  WorkbenchSurface
} from '../../components/workbench/workbench-surface';

const mockState = vi.hoisted(() => ({
  projectRoot: '/repo/projects/chirality-app-dev',
  searchParams: new URLSearchParams()
}));

vi.mock('next/navigation', () => ({
  useSearchParams: () => mockState.searchParams
}));

vi.mock('../../components/workspace/workspace-provider', () => ({
  useWorkspace: () => ({ projectRoot: mockState.projectRoot })
}));

// `DocumentView` drags the react-markdown ESM graph plus `fetch` into this node
// environment; the Workbench Documents block only needs to prove the mount point.
vi.mock('../../components/shell/document-view', async () => {
  const { createElement: h } = await import('react');
  return {
    DocumentView: () => h('div', { 'data-document-view': 'mounted' }, 'Document view')
  };
});

function disabledAttributeCount(html: string): number {
  return (html.match(/disabled=""/g) ?? []).length;
}

describe('WorkbenchSurface rendering', () => {
  beforeEach(() => {
    mockState.projectRoot = '/repo/projects/chirality-app-dev';
    mockState.searchParams = new URLSearchParams();
  });

  it('renders unsupported agents as read-only while preserving matrix context', () => {
    mockState.searchParams = new URLSearchParams({
      agent: 'HELP_HUMAN',
      row: 'EVALUATIVE',
      column: 'JUDGING'
    });

    const html = renderToStaticMarkup(createElement(WorkbenchSurface));

    expect(html).toContain('Active Agent Context');
    expect(html).toContain('HELP_HUMAN');
    expect(html).toContain('EVALUATIVE');
    expect(html).toContain('JUDGING');
    expect(html).toContain('Deliverable Contracts (Read-Only)');
    expect(html).toContain('Transition writes are disabled for this agent.');
    expect(html).not.toContain('Apply Transition');
  });

  it('mounts the folded Documents block inside the Workbench surface', () => {
    const html = renderToStaticMarkup(createElement(WorkbenchSurface));

    expect(html).toContain('aria-label="Documents"');
    expect(html).toContain('<h3>Documents</h3>');
    expect(html).toContain('Deliverable documents, evidence, and contracts read from the Working Root.');
    expect(html).toContain('data-document-view="mounted"');
  });

  it('keeps the Documents block mounted for read-only agents', () => {
    mockState.searchParams = new URLSearchParams({ agent: 'HELP_HUMAN' });

    const html = renderToStaticMarkup(createElement(WorkbenchSurface));

    expect(html).toContain('Deliverable Contracts (Read-Only)');
    expect(html).toContain('data-document-view="mounted"');
    expect(html).not.toContain('Apply Transition');
  });
});

describe('WorkbenchLifecycleTransitionForm rendering', () => {
  const noop = () => {};

  it('requires approval SHA and locks actor choice to HUMAN for human-gated transitions', () => {
    const html = renderToStaticMarkup(
      createElement(WorkbenchLifecycleTransitionForm, {
        availableTransitionTargets: ['CHECKING'],
        canSubmitTransition: false,
        requiresApprovalSha: true,
        transitionActor: 'HUMAN',
        transitionApprovalSha: '',
        transitionDate: '2026-06-21',
        transitionError: null,
        transitionSubmitting: false,
        transitionTarget: 'CHECKING',
        onActorChange: noop,
        onApprovalShaChange: noop,
        onDateChange: noop,
        onSubmit: noop,
        onTargetChange: noop
      })
    );

    expect(html).toContain('Approval SHA (required)');
    expect(html).toContain('placeholder="e.g. abcd1234"');
    expect(html).toContain('<option value="HUMAN" selected="">HUMAN</option>');
    expect(html).toContain('<option value="WORKING_ITEMS" disabled="">WORKING_ITEMS</option>');
    expect(html).toContain('<button type="submit" disabled="">Apply Transition</button>');
    expect(disabledAttributeCount(html)).toBe(4);
  });

  it('keeps the approval SHA optional for non-human-gated transitions', () => {
    const html = renderToStaticMarkup(
      createElement(WorkbenchLifecycleTransitionForm, {
        availableTransitionTargets: ['IN_PROGRESS'],
        canSubmitTransition: true,
        requiresApprovalSha: false,
        transitionActor: 'WORKING_ITEMS',
        transitionApprovalSha: '',
        transitionDate: '2026-06-21',
        transitionError: null,
        transitionSubmitting: false,
        transitionTarget: 'IN_PROGRESS',
        onActorChange: noop,
        onApprovalShaChange: noop,
        onDateChange: noop,
        onSubmit: noop,
        onTargetChange: noop
      })
    );

    expect(html).toContain('Approval SHA (optional)');
    expect(html).toContain('Optional (required at CHECKING/ISSUED)');
    expect(html).toContain('<option value="WORKING_ITEMS" selected="">WORKING_ITEMS</option>');
    expect(html).not.toContain('value="WORKING_ITEMS" disabled');
    expect(html).not.toContain('<button type="submit" disabled="">');
  });
});
