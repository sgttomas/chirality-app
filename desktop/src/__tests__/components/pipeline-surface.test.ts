import { createElement } from 'react';
import { renderToStaticMarkup } from 'react-dom/server';
import { beforeEach, describe, expect, it, vi } from 'vitest';

const mockState = vi.hoisted(() => {
  const baseScan = {
    projectRoot: '/repo/projects/chirality-app-dev',
    scannedAt: '2026-06-21T00:00:00.000Z',
    truncated: false,
    deliverables: [
      {
        id: 'DEL-02-01',
        name: 'Desktop Shell and Matrix Navigation',
        pkg: 'PKG-02',
        status: 'CHECKING',
        path: '/repo/execution/PKG-02/DEL-02-01',
        key: 'PKG-02::DEL-02-01'
      }
    ],
    knowledgeDecomposition: {
      enabled: false,
      markerFile: null as string | null
    },
    knowledgeTypes: [] as Array<{
      id: string;
      label: string;
      matchingDeliverableKeys: string[];
    }>
  };

  return {
    projectRoot: '/repo/projects/chirality-app-dev',
    searchParams: new URLSearchParams(),
    baseScan,
    scan: baseScan
  };
});

vi.mock('next/navigation', () => ({
  useSearchParams: () => mockState.searchParams
}));

vi.mock('../../components/workspace/workspace-provider', () => ({
  useWorkspace: () => ({ projectRoot: mockState.projectRoot })
}));

vi.mock('../../components/workspace/deliverables-provider', () => ({
  useDeliverables: () => ({
    loading: false,
    error: null,
    scan: mockState.scan,
    refresh: () => {}
  })
}));

describe('PipelineSurface rendering', () => {
  beforeEach(() => {
    mockState.projectRoot = '/repo/projects/chirality-app-dev';
    mockState.searchParams = new URLSearchParams();
    mockState.scan = mockState.baseScan;
  });

  it('renders operative category controls, TASK split selectors, and disabled coming-soon options', async () => {
    const { PipelineSurface } = await import('../../components/pipeline/pipeline-surface');
    const html = renderToStaticMarkup(createElement(PipelineSurface));

    expect(html).toContain('DECOMP*');
    expect(html).toContain('PREP*');
    expect(html).toContain('TASK*');
    expect(html).toContain('AUDIT*');
    expect(html).toContain('Task agent');
    expect(html).toContain('Scope Mode');
    expect(html).toContain('Scope (dynamic)');
    expect(html).toContain('PKG-02::DEL-02-01');
    expect(html).toContain('`KNOWLEDGE_TYPES` scope mode is unavailable');
    expect(html).toContain('BASE (create new) (coming soon)');
    expect(html).toContain('ESTIMATING (coming soon)');
    expect(html).toContain('SCHEDULING (coming soon)');
    expect(html).toContain('SCHEDULES (coming soon)');
    expect(html.match(/disabled=""/g)?.length ?? 0).toBeGreaterThanOrEqual(4);
  });

  it('renders valid TASK knowledge-type deep links with required target deliverables', async () => {
    mockState.searchParams = new URLSearchParams({
      category: 'TASK',
      taskScopeMode: 'KNOWLEDGE_TYPES',
      scopeKey: 'Specification',
      targetDeliverableKey: 'PKG-02::DEL-02-01'
    });
    mockState.scan = {
      ...mockState.baseScan,
      knowledgeDecomposition: {
        enabled: true,
        markerFile: '/repo/projects/chirality-app-dev/_Decomposition/source.md'
      },
      knowledgeTypes: [
        {
          id: 'Specification',
          label: 'Specification',
          matchingDeliverableKeys: ['PKG-02::DEL-02-01']
        }
      ]
    };

    const { PipelineSurface } = await import('../../components/pipeline/pipeline-surface');
    const html = renderToStaticMarkup(createElement(PipelineSurface));

    expect(html).toContain('Selected category: <strong>TASK</strong>');
    expect(html).toContain('Knowledge decomposition marker detected');
    expect(html).toContain('Specification (1)');
    expect(html).toContain('Target Deliverable (required)');
    expect(html).toContain('Selected knowledge type: <code>Specification</code>');
    expect(html).toContain('target <code>PKG-02::DEL-02-01</code>');
  });

  it('resets stale TASK knowledge-target deep links during initial render', async () => {
    mockState.searchParams = new URLSearchParams({
      category: 'TASK',
      taskScopeMode: 'KNOWLEDGE_TYPES',
      scopeKey: 'Specification',
      targetDeliverableKey: 'PKG-99::DEL-99-99'
    });
    mockState.scan = {
      ...mockState.baseScan,
      knowledgeDecomposition: {
        enabled: true,
        markerFile: '/repo/projects/chirality-app-dev/_Decomposition/source.md'
      },
      knowledgeTypes: [
        {
          id: 'Specification',
          label: 'Specification',
          matchingDeliverableKeys: ['PKG-02::DEL-02-01']
        }
      ]
    };

    const { PipelineSurface } = await import('../../components/pipeline/pipeline-surface');
    const html = renderToStaticMarkup(createElement(PipelineSurface));

    expect(html).toContain('Selected knowledge type: <code>Specification</code>');
    expect(html).not.toContain('PKG-99::DEL-99-99');
    expect(html).not.toContain('target <code>');
  });
});

describe('PipelineLifecycleTransitionForm rendering', () => {
  const noop = () => {};

  it('requires approval SHA and locks actor choice to HUMAN for human-gated transitions', async () => {
    const { PipelineLifecycleTransitionForm } = await import(
      '../../components/pipeline/pipeline-surface'
    );
    const html = renderToStaticMarkup(
      createElement(PipelineLifecycleTransitionForm, {
        availableTransitionTargets: ['CHECKING'],
        canSubmitTransition: false,
        requiresApprovalSha: true,
        transitionActor: 'HUMAN',
        transitionApprovalSha: '',
        transitionDate: '2026-07-19',
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

    expect(html).toContain('<option value="HUMAN" selected="">HUMAN</option>');
    expect(html).toContain('<option value="WORKING_ITEMS" disabled="">WORKING_ITEMS</option>');
    expect(html).toContain(
      '<option value="CHIRALITY_FRAMEWORK" disabled="">CHIRALITY_FRAMEWORK</option>'
    );
    expect(html).toContain('<option value="4_DOCUMENTS" disabled="">4_DOCUMENTS</option>');
    expect(html).toContain('Approval SHA (required)');
    expect(html).toContain('required=""');
    expect(html).toContain('<button type="submit" disabled="">Apply Transition</button>');
  });

  it('keeps approval SHA optional and submission active for ordinary transitions', async () => {
    const { PipelineLifecycleTransitionForm } = await import(
      '../../components/pipeline/pipeline-surface'
    );
    const html = renderToStaticMarkup(
      createElement(PipelineLifecycleTransitionForm, {
        availableTransitionTargets: ['IN_PROGRESS'],
        canSubmitTransition: true,
        requiresApprovalSha: false,
        transitionActor: 'WORKING_ITEMS',
        transitionApprovalSha: '',
        transitionDate: '2026-07-19',
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

    expect(html).toContain(
      '<option value="WORKING_ITEMS" selected="">WORKING_ITEMS</option>'
    );
    expect(html).not.toContain('value="WORKING_ITEMS" disabled');
    expect(html).toContain('Approval SHA (optional)');
    expect(html).not.toContain('required=""');
    expect(html).not.toContain('<button type="submit" disabled="">');
    expect(html).toContain('<button type="submit">Apply Transition</button>');
  });
});
