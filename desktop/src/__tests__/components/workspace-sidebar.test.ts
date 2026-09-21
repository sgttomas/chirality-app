import { createElement } from 'react';
import { renderToStaticMarkup } from 'react-dom/server';
import { describe, expect, it } from 'vitest';
import { WorkspaceSidebar } from '../../components/shell/workspace-sidebar';
import { SidebarRightLoopLayout } from '../../components/shell/sidebar-right-loop-layout';

describe('WorkspaceSidebar tertiary tabs', () => {
  it('renders Portal, Workbench, and Pipeline as sidebar tabs when provided', () => {
    const html = renderToStaticMarkup(
      createElement(WorkspaceSidebar, {
        activeTab: 'workbench',
        onTabChange: () => {},
        pipelineTab: createElement('div', null, 'Pipeline tertiary form'),
        portalTab: createElement('div', null, 'Portal matrix'),
        workbenchTab: createElement('div', null, 'Workbench tertiary form')
      })
    );

    expect(html).toContain('role="tab"');
    expect(html).toContain('Portal');
    expect(html).toContain('Workbench');
    expect(html).toContain('Pipeline');
    expect(html).toContain('Workbench tertiary form');
    expect(html).not.toContain('Pipeline tertiary form');
  });

  it('keeps the primary loop content mounted while a tertiary tab owns the right sidebar', () => {
    const html = renderToStaticMarkup(
      createElement(
        SidebarRightLoopLayout,
        {
          defaultSidebarTab: 'pipeline',
          children: createElement('div', null, 'Mounted live loop'),
          pipelineTab: createElement('div', null, 'Pipeline tertiary form'),
          portalTab: createElement('div', null, 'Portal matrix'),
          workbenchTab: createElement('div', null, 'Workbench tertiary form')
        }
      )
    );

    expect(html).toContain('loop-grid');
    expect(html).toContain('loop-main');
    expect(html).toContain('loop-sidebar');
    expect(html).toContain('Mounted live loop');
    expect(html).toContain('Collapse');
    expect(html).toContain('Pipeline tertiary form');
    expect(html).not.toContain('Workbench tertiary form');
  });
});
