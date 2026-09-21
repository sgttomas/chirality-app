'use client';

import React, { useState, type ReactNode } from 'react';
import { WorkspaceSidebar, type SidebarTabId } from './workspace-sidebar';

type SidebarRightLoopLayoutProps = {
  children: ReactNode;
  defaultSidebarTab?: SidebarTabId;
  pipelineTab?: ReactNode;
  portalTab?: ReactNode;
  workbenchTab?: ReactNode;
};

/**
 * Shared loop-first layout primitive: primary content on the left, collapsible
 * multi-view workspace sidebar on the right. Collapsing the sidebar changes
 * only the grid/sidebar contents, so primary children stay mounted.
 */
export function SidebarRightLoopLayout({
  children,
  defaultSidebarTab = 'files',
  pipelineTab,
  portalTab,
  workbenchTab
}: SidebarRightLoopLayoutProps): JSX.Element {
  const [sidebarTab, setSidebarTab] = useState<SidebarTabId>(defaultSidebarTab);
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);

  return (
    <section
      className={
        sidebarCollapsed ? 'loop-grid loop-grid--sidebar-collapsed' : 'loop-grid'
      }
    >
      <section className="loop-main">{children}</section>

      <div
        className={
          sidebarCollapsed
            ? 'shell-pane shell-pane--sidebar shell-pane--collapsed loop-sidebar'
            : 'shell-pane shell-pane--sidebar loop-sidebar'
        }
      >
        <button
          type="button"
          className="shell-pane-toggle button-muted"
          onClick={() => {
            setSidebarCollapsed((value) => !value);
          }}
        >
          {sidebarCollapsed ? 'Expand' : 'Collapse'}
        </button>
        {sidebarCollapsed ? (
          <span className="shell-pane-collapsed-label">Workspace</span>
        ) : (
          <WorkspaceSidebar
            activeTab={sidebarTab}
            onTabChange={setSidebarTab}
            pipelineTab={pipelineTab}
            portalTab={portalTab}
            workbenchTab={workbenchTab}
          />
        )}
      </div>
    </section>
  );
}
