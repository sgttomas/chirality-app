'use client';

import React, { useMemo } from 'react';
import type { HarnessEvent } from '@chirality/runtime-contracts/event-schema';
import { deriveSubagentActivity } from '../../lib/shell/harness-event-views';
import type { RecordedAgentHierarchy } from '../../lib/woven-dialogue/contracts';
import { AgentsProjection } from './agents-projection';

type CoordinationPanelProps = {
  embedded?: boolean;
  nativeEvents?: readonly HarnessEvent[];
  activeView: 'session' | 'agents';
  replaySlot?: React.ReactNode;
  hierarchy: RecordedAgentHierarchy;
  sessionsLoading: boolean;
  sessionsError: string | null;
  selectedSessionId?: string;
  selectionDisabled: boolean;
  onSelectView: (view: 'session' | 'agents') => void;
  onRefreshSessions: () => void;
  onSelectSession: (sessionId: string) => void;
};

export function CoordinationPanel({
  activeView,
  nativeEvents,
  embedded = false,
  replaySlot,
  hierarchy,
  sessionsLoading,
  sessionsError,
  selectedSessionId,
  selectionDisabled,
  onSelectView,
  onRefreshSessions,
  onSelectSession
}: CoordinationPanelProps): JSX.Element {
  const nativeChildren = useMemo(() => deriveSubagentActivity(nativeEvents ?? []).filter(row => row.key.startsWith('native:')), [nativeEvents]);
  return (
    <section className="woven-coordination" aria-label="Coordination Panel">
      {!embedded ? <header className="woven-region-header">
        <div>
          <p className="woven-eyebrow">Recorded coordination</p>
          <h2>Coordination</h2>
        </div>
        <div className="woven-coordination-tabs" aria-label="Coordination views">
          {(['session', 'agents'] as const).map((view) => (
            <button
              key={view}
              type="button"
              aria-pressed={activeView === view}
              className={activeView === view ? 'is-active' : undefined}
              onClick={() => {
                onSelectView(view);
              }}
            >
              {view === 'session' ? 'Session' : 'Agents'}
            </button>
          ))}
        </div>
      </header> : null}
      <div className="woven-coordination-body">
        {activeView === 'session'
          ? replaySlot ?? (
              <p className="panel-empty">Select a recorded session to inspect its replay.</p>
            )
          : null}
        {activeView === 'agents' && nativeChildren.length ? <section aria-label="Native work in current chat">
          <h3>Native work in current chat</h3>
          {nativeChildren.map(child => <details key={child.key} className="turn-activity"><summary>{child.agentName === 'subagent' ? child.agentPath ?? 'Observed child' : child.agentName} · {child.status}{child.observationEnded ? ' · last observed' : ''}</summary>
            {child.nativeThreadId ? <p>Thread: {child.nativeThreadId}</p> : null}
            {child.agentRole ? <p>Role: {child.agentRole}</p> : null}
            {child.agentPath && child.agentName !== 'subagent' ? <p>Path: {child.agentPath}</p> : null}
            {child.parentThreadId ? <p>Parent thread: {child.parentThreadId}</p> : null}
            {child.observationEnded ? <p role="status">{child.observationEnded}</p> : null}
            {child.description ? <p>{child.description}</p> : null}{child.summary ? <p className="transcript-text">{child.summary}</p> : null}
          </details>)}
        </section> : null}
        {activeView === 'agents' ? (
          <AgentsProjection
            hierarchy={hierarchy}
            loading={sessionsLoading}
            error={sessionsError}
            selectedSessionId={selectedSessionId}
            selectionDisabled={selectionDisabled}
            onRefresh={onRefreshSessions}
            onSelectSession={onSelectSession}
          />
        ) : null}
      </div>
    </section>
  );
}
