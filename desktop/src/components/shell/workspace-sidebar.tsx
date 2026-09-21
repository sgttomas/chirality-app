'use client';

import React, {
  createContext,
  useContext,
  useMemo,
  useRef,
  type KeyboardEvent,
  type ReactNode
} from 'react';
import { DocumentView } from './document-view';
import { FileTreePanel } from './file-tree-panel';
import { OperatorToolkitPanel } from './operator-toolkit-panel';
import { SessionListView } from './session-list-view';
import { SubagentStreamView } from './subagent-stream-view';
import { ToolStreamView } from './tool-stream-view';
import { TranscriptStreamView } from './transcript-stream-view';

export type SidebarTabId =
  | 'portal'
  | 'workbench'
  | 'pipeline'
  | 'files'
  | 'sessions'
  | 'transcript'
  | 'tools'
  | 'subagents'
  | 'document'
  | 'workflow'
  | 'toolkit';

type SidebarTab = {
  id: SidebarTabId;
  label: string;
};

const SIDEBAR_TABS: readonly SidebarTab[] = [
  { id: 'files', label: 'Files' },
  { id: 'sessions', label: 'Sessions' },
  { id: 'transcript', label: 'Transcript' },
  { id: 'tools', label: 'Tools' },
  { id: 'subagents', label: 'Subagents' },
  { id: 'document', label: 'Document' },
  { id: 'workflow', label: 'Workflow' },
  { id: 'toolkit', label: 'Tool Kit' }
];

const PORTAL_TAB: SidebarTab = { id: 'portal', label: 'Portal' };
const WORKBENCH_TAB: SidebarTab = { id: 'workbench', label: 'Workbench' };
const PIPELINE_TAB: SidebarTab = { id: 'pipeline', label: 'Pipeline' };

const TAB_PANEL_ID = 'workspace-sidebar-panel';

type WorkspaceSidebarActions = {
  openTab: (tab: SidebarTabId) => void;
};

const WorkspaceSidebarActionsContext = createContext<WorkspaceSidebarActions | null>(null);

export function useWorkspaceSidebarActions(): WorkspaceSidebarActions | null {
  return useContext(WorkspaceSidebarActionsContext);
}

function tabButtonId(id: SidebarTabId): string {
  return `workspace-sidebar-tab-${id}`;
}

function SidebarPlaceholder({ title, note }: { title: string; note: string }): JSX.Element {
  return (
    <aside className="panel panel--stream panel--placeholder">
      <header className="panel-header">
        <h2>{title}</h2>
      </header>
      <div className="panel-body">
        <p className="panel-empty">{note}</p>
      </div>
    </aside>
  );
}

type WorkspaceSidebarProps = {
  activeTab: SidebarTabId;
  onTabChange: (tab: SidebarTabId) => void;
  pipelineTab?: ReactNode;
  portalTab?: ReactNode;
  workbenchTab?: ReactNode;
};

/**
 * The collapsible multi-view sidebar (DESIGN §3.2). One tabbed pane is the
 * normal modality for reaching the workspace views: the live file tree, the
 * bridge-fed Tools and Subagents streams, and (seeded) Document/Workflow peeks,
 * plus the local Tool Kit folded in from its former dedicated pane.
 *
 * Active-tab state is lifted to the parent shell so it survives the pane being
 * unmounted on collapse. Implements the WAI-ARIA tabs pattern: roving tabindex,
 * arrow/Home/End navigation, and a labelled tabpanel.
 */
export function WorkspaceSidebar({
  activeTab,
  onTabChange,
  pipelineTab,
  portalTab,
  workbenchTab
}: WorkspaceSidebarProps): JSX.Element {
  const tabRefs = useRef<Partial<Record<SidebarTabId, HTMLButtonElement | null>>>({});
  const tabs = [
    ...(portalTab ? [PORTAL_TAB] : []),
    ...(workbenchTab ? [WORKBENCH_TAB] : []),
    ...(pipelineTab ? [PIPELINE_TAB] : []),
    ...SIDEBAR_TABS
  ];
  const visibleActiveTab = tabs.some((tab) => tab.id === activeTab) ? activeTab : tabs[0].id;
  const sidebarActions = useMemo<WorkspaceSidebarActions>(
    () => ({
      openTab: onTabChange
    }),
    [onTabChange]
  );

  function focusTab(id: SidebarTabId): void {
    onTabChange(id);
    tabRefs.current[id]?.focus();
  }

  function handleTabKeyDown(event: KeyboardEvent<HTMLButtonElement>): void {
    const index = tabs.findIndex((tab) => tab.id === visibleActiveTab);
    if (index < 0) {
      return;
    }

    if (event.key === 'ArrowRight' || event.key === 'ArrowDown') {
      event.preventDefault();
      focusTab(tabs[(index + 1) % tabs.length].id);
      return;
    }

    if (event.key === 'ArrowLeft' || event.key === 'ArrowUp') {
      event.preventDefault();
      focusTab(tabs[(index - 1 + tabs.length) % tabs.length].id);
      return;
    }

    if (event.key === 'Home') {
      event.preventDefault();
      focusTab(tabs[0].id);
      return;
    }

    if (event.key === 'End') {
      event.preventDefault();
      focusTab(tabs[tabs.length - 1].id);
    }
  }

  return (
    <WorkspaceSidebarActionsContext.Provider value={sidebarActions}>
      <div className="workspace-sidebar">
        <div className="workspace-sidebar-tabs" role="tablist" aria-label="Workspace views">
          {tabs.map((tab) => {
            const isActive = tab.id === visibleActiveTab;
            return (
              <button
                key={tab.id}
                ref={(node) => {
                  tabRefs.current[tab.id] = node;
                }}
                type="button"
                role="tab"
                id={tabButtonId(tab.id)}
                aria-selected={isActive}
                aria-controls={TAB_PANEL_ID}
                tabIndex={isActive ? 0 : -1}
                className={
                  isActive
                    ? 'workspace-sidebar-tab workspace-sidebar-tab--active'
                    : 'workspace-sidebar-tab'
                }
                onClick={() => {
                  onTabChange(tab.id);
                }}
                onKeyDown={handleTabKeyDown}
              >
                {tab.label}
              </button>
            );
          })}
        </div>

        <div
          className="workspace-sidebar-body"
          role="tabpanel"
          id={TAB_PANEL_ID}
          aria-labelledby={tabButtonId(visibleActiveTab)}
          tabIndex={0}
        >
          {visibleActiveTab === 'portal' && portalTab ? portalTab : null}
          {visibleActiveTab === 'workbench' && workbenchTab ? workbenchTab : null}
          {visibleActiveTab === 'pipeline' && pipelineTab ? pipelineTab : null}
          {visibleActiveTab === 'files' ? <FileTreePanel /> : null}
          {visibleActiveTab === 'sessions' ? <SessionListView /> : null}
          {visibleActiveTab === 'transcript' ? <TranscriptStreamView /> : null}
          {visibleActiveTab === 'tools' ? <ToolStreamView /> : null}
          {visibleActiveTab === 'subagents' ? <SubagentStreamView /> : null}
          {visibleActiveTab === 'document' ? <DocumentView /> : null}
          {visibleActiveTab === 'workflow' ? (
            <SidebarPlaceholder
              title="Workflow"
              note="Workflow design is a thin peek now; the full surface is the deferred secondary phase."
            />
          ) : null}
          {visibleActiveTab === 'toolkit' ? <OperatorToolkitPanel /> : null}
        </div>
      </div>
    </WorkspaceSidebarActionsContext.Provider>
  );
}
