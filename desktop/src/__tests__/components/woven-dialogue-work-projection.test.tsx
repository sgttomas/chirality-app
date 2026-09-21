import { createElement } from 'react';
import { renderToStaticMarkup } from 'react-dom/server';
import { describe, expect, it } from 'vitest';
import {
  WORK_PROJECTION_EMPTY_STATE,
  WorkProjection
} from '../../components/woven-dialogue/work-projection';
import type { CoordinationWorkItem } from '../../lib/woven-dialogue/contracts';

describe('Woven Dialogue Work projection', () => {
  it('renders an honest empty state instead of synthesizing work from dialogue', () => {
    const html = renderToStaticMarkup(createElement(WorkProjection, { items: [] }));

    expect(html).toContain(WORK_PROJECTION_EMPTY_STATE);
    expect(html).not.toContain('Recorded work items');
    expect(html).not.toContain('<button');
  });

  it('renders only supplied evidence with visible authority, provenance, and currency', () => {
    const items: CoordinationWorkItem[] = [
      {
        id: 'work-1',
        title: 'Implement Woven Dialogue state',
        workClass: 'HUMAN_APPROVED_EXECUTION',
        sourceReference: 'execution/_ScopeChange/SCA-APP-004/Handoff_State.md',
        statusBasis: 'Owner-approved implementation activation',
        currency: 'CURRENT',
        statusLabel: 'IN_PROGRESS',
        responsibleReference: 'PKG-02',
        relatedReferences: ['DEL-02-04', 'SOW-004'],
        runtimeStatus: 'running',
        lifecycleStatus: 'IN_PROGRESS'
      }
    ];

    const html = renderToStaticMarkup(createElement(WorkProjection, { items }));

    expect(html).toContain('Implement Woven Dialogue state');
    expect(html).toContain('HUMAN_APPROVED_EXECUTION');
    expect(html).toContain(
      'execution/_ScopeChange/SCA-APP-004/Handoff_State.md'
    );
    expect(html).toContain('Owner-approved implementation activation');
    expect(html).toContain('CURRENT');
    expect(html).toContain('PKG-02');
    expect(html).toContain('DEL-02-04');
    expect(html).toContain('SOW-004');
    expect(html).toContain('Runtime status');
    expect(html).toContain('Project lifecycle status');
    expect(html).toContain('running');
    expect(html).toContain('IN_PROGRESS');
    expect(html).toContain('data-work-class="HUMAN_APPROVED_EXECUTION"');
    expect(html).toContain('data-currency="CURRENT"');
    expect(html).not.toContain('<button');
  });

  it('discloses unrecorded optional evidence without inferring assignments or status', () => {
    const items: CoordinationWorkItem[] = [
      {
        id: 'work-2',
        title: 'Agent working proposal',
        workClass: 'AGENT_WORKING_PROPOSAL',
        sourceReference: 'proposal://work-2',
        statusBasis: 'Proposal record only',
        currency: 'UNKNOWN',
        relatedReferences: []
      }
    ];

    const html = renderToStaticMarkup(createElement(WorkProjection, { items }));

    expect(html).toContain('AGENT_WORKING_PROPOSAL');
    expect(html).toContain('UNKNOWN');
    expect(html).toContain('Proposal record only');
    expect((html.match(/Not recorded/g) ?? []).length).toBeGreaterThanOrEqual(5);
    expect(html).not.toContain('approved');
    expect(html).not.toContain('assigned');
    expect(html).not.toContain('<button');
  });
});
