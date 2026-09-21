'use client';

import styles from './workflows.module.css';
import { ActivityView } from './activity-shelf';
import React, { useEffect, useRef, useState } from 'react';
import type { SelectedSessionReplayState } from '../../lib/woven-dialogue/contracts';
import { guardRecordedSessionSelection } from '../../lib/woven-dialogue/guarded-session-selection';
import { useWorkspace } from '../workspace/workspace-provider';
import { FileTreePanel, type FileCatalog } from '../shell/file-tree-panel';
import { DocumentView, handoffDocument } from '../shell/document-view';
import type { WovenWorkspaceState } from '../../lib/woven-dialogue/woven-workspace-state';
import type { QualifiedMethodReference } from '../../lib/harness/method-selection-client';
import type { WorkflowFeedbackRequest } from '../../lib/harness/workflow-feedback';
import { MethodLibraryView } from './method-library-view';
import { NativePlanPanel, type NativePlanPanelModel } from '../shell/native-plan-panel';
import { resolveRightPanelView, type WovenRightPanelView } from '../../lib/woven-dialogue/woven-workspace-state';

/** Tab order and labels. Settings is reached from the account menu, not a tab. */
const TABS: readonly { view: Exclude<WovenRightPanelView, 'settings'>; label: string }[] = [
  { view: 'files', label: 'Files' }, { view: 'plan', label: 'Plan' }, { view: 'workflows', label: 'Workflows' }, { view: 'agents', label: 'Agents' }, { view: 'activity', label: 'Activity' }
];

/** Deterministic projection of recorded metadata; never a generated purpose/result narrative. */
export function deriveSessionMenu(
  state: SelectedSessionReplayState,
  recordedSessionIds: readonly string[],
  primarySessionId: string | undefined,
  liveTurnActive: boolean
): { id?: string; summary?: string; parentId?: string; parentDisabledReason?: string } {
  if (state.status === 'IDLE') return { parentDisabledReason: 'Select a recorded session first.' };
  const id = state.status === 'READY' ? state.projection.selectedSessionId : state.selectedSessionId;
  if (state.status !== 'READY') return { id, parentDisabledReason: 'Parent information is unavailable until the recorded session loads.' };
  const projection = state.projection;
  const session = projection.session;
  const summary = 'Recorded session metadata (read-only snapshot)\n' + JSON.stringify({
    selectedSessionId: id,
    sourceReference: projection.sourceReference,
    observedAt: projection.observedAt,
    disclosure: projection.disclosure,
    currency: projection.currency,
    sourceEventCount: projection.sourceEventCount,
    renderedItemCount: projection.renderedItemCount,
    malformedLineCount: projection.malformedLineCount,
    ...(session ? { recordedAttribution: {
      sessionId: session.sessionId, sourceReference: session.sourceReference,
      observedAt: session.observedAt, currency: session.currency,
      persona: session.persona, role: session.role, runtimeStatus: session.runtimeStatus,
      providerId: session.providerId, model: session.model, parentage: session.parentage
    } } : {})
  }, null, 2);
  const blocked = (parentDisabledReason: string) => ({ id, summary, parentDisabledReason });
  if (projection.currency === 'CONFLICTING' || projection.disclosure === 'CONFLICTING' ||
      session?.currency === 'CONFLICTING' || (session && session.sessionId !== id) ||
      [...(projection.diagnostics ?? []), ...(session?.diagnostics ?? [])].some(item => item.code.includes('CONFLICT'))) {
    return blocked('Recorded parentage is conflicting; parent navigation is unavailable.');
  }
  if (session?.parentage.state !== 'RECORDED') return blocked('No parent session is recorded.');
  const parent = session.parentage;
  if (!parent.parentAvailable) return blocked('The recorded parent session is unavailable.');
  if (!parent.parentSessionId.trim() || parent.parentSessionId === id) return blocked('Recorded parentage is invalid.');
  const decision = guardRecordedSessionSelection({ currentState: state, requestedSessionId: parent.parentSessionId,
    primarySessionId, recordedSessionIds, liveTurnActive, replayIsolationAvailable: true });
  if (decision.outcome === 'BLOCKED') return blocked(decision.reason === 'LIVE_TURN_ACTIVE'
    ? 'Parent replay is unavailable while a live turn is running.' : 'The recorded parent session is unavailable.');
  return { id, summary, parentId: parent.parentSessionId };
}

type Props = {
  state: WovenWorkspaceState;
  sessionOpen: boolean;
  folderLocked?: boolean;
  onFolderSelectionPending?: (pending: boolean) => void;
  folderMismatch?: boolean;
  settingsView?: React.ReactNode;
  onView: (view: WovenRightPanelView) => void;
  planPanel?: NativePlanPanelModel | null;
  planFocusRevision?: { revision: number; sequence: number };
  onOpenFile: (path: string) => void;
  onFileCatalog?: (catalog: FileCatalog | null) => void;
  onClose: () => void;
  onExpand: () => void;
  coordination: React.ReactNode;
  onRefreshSessions?: () => void;
  replayState?: SelectedSessionReplayState;
  recordedSessionIds?: readonly string[];
  primarySessionId?: string;
  liveTurnActive?: boolean;
  onOpenParent?: (sessionId: string) => void;
  onWorkflowFeedback?: (request: Omit<WorkflowFeedbackRequest, 'sequence'>) => void;
  workflowFeedbackDisabled?: boolean;
  readPlanRevisions?: Readonly<Record<string, number>>;
  onPlanRead?: (sessionId: string, revision: number) => void;
  selectedMethods?: readonly QualifiedMethodReference[];
  onSelectedMethodsChange?: (methods: QualifiedMethodReference[]) => void;
};
export function RightPanel({ readPlanRevisions: suppliedReadPlanRevisions, onPlanRead, onWorkflowFeedback, workflowFeedbackDisabled = false, settingsView, state, sessionOpen, folderLocked = false, onFolderSelectionPending, folderMismatch = false, onView, onOpenFile, onFileCatalog, onClose, onExpand, coordination, onRefreshSessions, replayState = { status: 'IDLE' }, recordedSessionIds = [], primarySessionId, liveTurnActive = false, onOpenParent, selectedMethods = [], onSelectedMethodsChange = () => {}, planPanel = null, planFocusRevision }: Props): JSX.Element {
  const { projectRoot } = useWorkspace();
  const [refresh, setRefresh] = useState(0);
  const [completedWorkRevision, setCompletedWorkRevision] = useState(0);
  const previousTurnActive = useRef(liveTurnActive);
  useEffect(() => {
    if (previousTurnActive.current && !liveTurnActive) setCompletedWorkRevision(value => value + 1);
    previousTurnActive.current = liveTurnActive;
  }, [liveTurnActive]);
  const tabsRef = useRef<HTMLDivElement>(null);
  const [copyStatus, setCopyStatus] = useState<string | null>(null);
  const copyGeneration = useRef(0);
  const sessionMenu = deriveSessionMenu(replayState, recordedSessionIds, primarySessionId, liveTurnActive);
  const [menuError, setMenuError] = useState<string | null>(null);
  // Future stored views must leave existing content reachable, never blank it.
  const view = resolveRightPanelView(state.rightPanelView);
  const [localReadPlanRevisions, setLocalReadPlanRevisions] = useState<Record<string, number>>({});
  const readPlanRevisions = suppliedReadPlanRevisions ?? localReadPlanRevisions;
  const planSessionKey = planPanel?.sessionId ?? primarySessionId ?? '';
  const latestPlanRevision = Math.max(0, ...(planPanel?.revisions.map(revision => revision.revision) ?? []));
  const unreadPlanCount = view === 'plan' ? 0 : (planPanel?.revisions.filter(revision => revision.revision > (readPlanRevisions[planSessionKey] ?? 0)).length ?? 0);
  useEffect(() => {
    if (view !== 'plan' || !latestPlanRevision) return;
    if (onPlanRead) onPlanRead(planSessionKey, latestPlanRevision);
    else setLocalReadPlanRevisions(current => (current[planSessionKey] ?? 0) >= latestPlanRevision ? current : { ...current, [planSessionKey]: latestPlanRevision });
  }, [view, planSessionKey, latestPlanRevision, onPlanRead]);
  const target = view === 'files' ? state.openDocumentPath : null;
  const detailOpen = Boolean(target || (sessionOpen && view === 'agents'));
  const sessionDetail = sessionOpen && view === 'agents';
  useEffect(() => {
    const tabs = tabsRef.current;
    if (!tabs) return;
    const revealSelected = () => tabs.querySelector<HTMLButtonElement>('[aria-selected="true"]')?.scrollIntoView?.({ block: 'nearest', inline: 'nearest' });
    revealSelected();
    const observer = typeof ResizeObserver === 'undefined' ? null : new ResizeObserver(revealSelected);
    observer?.observe(tabs);
    return () => observer?.disconnect();
  }, [view, detailOpen]);
  useEffect(() => { copyGeneration.current++; setCopyStatus(null); setMenuError(null); }, [sessionMenu.id, target, view]);
  const copy = async (value: string, label: string) => {
    const generation = ++copyGeneration.current; setCopyStatus(null); setMenuError(null);
    try {
      if (!navigator.clipboard?.writeText) throw new Error('Clipboard is unavailable.');
      await navigator.clipboard.writeText(value);
      if (generation === copyGeneration.current) setCopyStatus(`${label} copied.`);
    } catch { if (generation === copyGeneration.current) setMenuError(`Unable to copy ${label.toLowerCase()}.`); }
  };
  return <section className="woven-right-panel" aria-label="Right panel">
    <header className={`woven-region-header woven-right-panel-header ${styles.header}`}>
      {view === 'settings' ? <nav aria-label="Settings breadcrumb"><button onClick={() => onView('files')}>‹ Files</button> › <strong tabIndex={-1} id="right-settings-title">Settings</strong></nav> : target ? <nav aria-label="Document breadcrumb"><button onClick={() => onView('files')}>Files</button> › <span>{target}</span></nav> :
        sessionOpen && view === 'agents' ? <nav aria-label="Session breadcrumb"><button onClick={() => onView('agents')}>Agents</button> › Session</nav> :
        <div ref={tabsRef} className={styles.tabs} role="tablist" aria-label="Right panel views" onKeyDown={(event) => {
          if (!['ArrowLeft', 'ArrowRight', 'Home', 'End'].includes(event.key)) return;
          event.preventDefault();
          const views = TABS.map(tab => tab.view);
          const index = Math.max(0, views.indexOf(view as (typeof views)[number]));
          const next = event.key === 'Home' ? views[0] : event.key === 'End' ? views[views.length - 1] : views[(index + (event.key === 'ArrowRight' ? 1 : views.length - 1)) % views.length];
          onView(next);
          event.currentTarget.querySelector<HTMLButtonElement>(`[data-view="${next}"]`)?.focus();
        }}>{TABS.map(tab => <button key={tab.view} role="tab" id={`right-tab-${tab.view}`} data-view={tab.view}
          aria-controls="right-view-content" aria-selected={view === tab.view} tabIndex={view === tab.view ? 0 : -1}
          onClick={() => onView(tab.view)}>{tab.label}{tab.view === 'plan' && unreadPlanCount ? <span className="woven-tab-count" aria-label={`${unreadPlanCount} unread plan revisions`}>{unreadPlanCount}</span> : null}</button>)}</div>}
      <div className="woven-right-panel-controls">
        <details><summary aria-label="Panel menu" title="Panel menu">⋮</summary>
          <div className="woven-panel-menu-content">
          {sessionDetail ? <>
            <button type="button" disabled={!sessionMenu.parentId || !onOpenParent}
              aria-describedby={sessionMenu.parentDisabledReason ? 'session-parent-explanation' : undefined}
              onClick={() => { if (sessionMenu.parentId) onOpenParent?.(sessionMenu.parentId); }}>Open parent chat</button>
            {sessionMenu.parentDisabledReason ? <p id="session-parent-explanation">{sessionMenu.parentDisabledReason}</p> : null}
            <button type="button" disabled={!sessionMenu.id} onClick={() => { if (sessionMenu.id) void copy(sessionMenu.id, 'Session id'); }}>Copy session id</button>
            <button type="button" disabled={!sessionMenu.summary} onClick={() => { if (sessionMenu.summary) void copy(sessionMenu.summary, 'Recorded metadata summary'); }}>Copy summary</button>
            {!sessionMenu.summary ? <p>Recorded metadata summary is unavailable until the session loads.</p> : null}
          </> : <button type="button" onClick={() => { setRefresh(value => value + 1); if (view === 'agents') onRefreshSessions?.(); }}>{target ? 'Reload document' : 'Refresh'}</button>}
          {view === 'files' ? <button type="button" disabled={!projectRoot} onClick={() => {
            const value = target ? `${projectRoot?.replace(/\/$/, '')}/${target}` : projectRoot;
            if (value) void copy(value, target ? 'File path' : 'Root path');
          }}>Copy {target ? 'file' : 'root'} path</button> : null}
          {view === 'files' && projectRoot ? <button type="button" onClick={() => {
            void handoffDocument(target ? { projectRoot, target, action: 'reveal' } : { projectRoot, action: 'reveal-root' }).catch(error => setMenuError(error instanceof Error ? error.message : 'Unable to reveal item.'));
          }}>Reveal {target ? 'file' : 'root'} in Finder</button> : null}
          {target && projectRoot ? <button type="button" onClick={() => {
            void handoffDocument({ projectRoot, target, action: 'open' }).catch(error => setMenuError(error instanceof Error ? error.message : 'Unable to open file.'));
          }}>Open in default app</button> : null}
          </div>
        </details>
        <button type="button" aria-label={state.rightPanelExpanded ? 'Return panel' : 'Expand panel'} title={state.rightPanelExpanded ? 'Return panel' : 'Expand panel'} aria-pressed={state.rightPanelExpanded ?? false} onClick={onExpand}>{state.rightPanelExpanded ? '⤡' : '⤢'}</button>
        <button type="button" aria-label={detailOpen ? 'Close detail' : 'Collapse right panel'} onClick={onClose}>×</button></div>
    </header>
    {copyStatus ? <p role="status">{copyStatus}</p> : null}
    {menuError ? <p role="alert">{menuError}</p> : null}
    <div id="right-view-content" role={detailOpen ? undefined : 'tabpanel'} aria-labelledby={view === 'settings' ? 'right-settings-title' : detailOpen ? undefined : `right-tab-${view}`} style={{ minHeight: 0, flex: 1, overflow: 'auto' }}>
      {view === 'settings' ? settingsView ?? <p>Settings are unavailable.</p>
        : view === 'plan' ? <NativePlanPanel model={planPanel} focusRevision={planFocusRevision} />
        : view === 'workflows' ? folderMismatch ? <p role="alert">The chat is bound to a different folder. The workflow library is unavailable until that folder is synchronized.</p> : projectRoot ? <MethodLibraryView onWorkflowFeedback={onWorkflowFeedback} feedbackDisabled={workflowFeedbackDisabled || liveTurnActive} view="workflows" projectRoot={projectRoot} selected={selectedMethods} onSelectedChange={onSelectedMethodsChange} refresh={refresh + completedWorkRevision} /> : <p>Choose a folder to see its workflow library.</p>
        : view === 'activity' ? <ActivityView /> : view === 'files' && folderMismatch ? <p role="alert">The chat is bound to a different folder. File browsing is unavailable until that folder is synchronized.</p> : view === 'files' ? target ? <DocumentView presentation="woven" key={refresh + completedWorkRevision} target={target} expanded={state.rightPanelExpanded} onOpenDocument={relative => { if (projectRoot) onOpenFile(`${projectRoot.replace(/\/$/, '')}/${relative}`); }} /> : <FileTreePanel presentation="woven" folderLocked={folderLocked} onFolderSelectionPending={onFolderSelectionPending} key={refresh} onOpenFile={onOpenFile} onFileCatalog={onFileCatalog} selectedPath={state.openDocumentPath && projectRoot ? `${projectRoot.replace(/\/$/, '')}/${state.openDocumentPath}` : null} /> : coordination}
    </div>
  </section>;
}
