'use client';

import React, { useMemo } from 'react';
import {
  deriveSubagentActivity,
  type SubagentActivityRow
} from '../../lib/shell/harness-event-views';
import { useHarnessEvents } from '../workspace/harness-events-provider';

function SubagentActivityItem({ row }: { row: SubagentActivityRow }): JSX.Element {
  return (
    <li className={`harness-stream-item harness-stream-item--${row.status}`}>
      <div className="harness-stream-row">
        <span className="harness-stream-name" title={row.agentName}>
          {row.agentName === 'subagent' ? row.agentPath ?? 'Observed child' : row.agentName}
        </span>
        <span className={`harness-status-badge harness-status-badge--${row.status}`}>
          {row.status}{row.observationEnded ? ' · last observed' : ''}
        </span>
      </div>
      {row.description ? <p className="harness-stream-description">{row.description}</p> : null}
      {row.observationEnded ? <p role="status">{row.observationEnded}</p> : null}
      {row.summary ? <p className="harness-stream-summary">{row.summary}</p> : null}
      <p className="harness-stream-meta">
        {row.lastToolName ? `last: ${row.lastToolName} · ` : ''}
        {row.outputArtifactPath ? 'output saved · ' : ''}
        {row.eventCount} event{row.eventCount === 1 ? '' : 's'}
      </p>
    </li>
  );
}

/**
 * Presentational list over already-derived rows, decoupled from context so it
 * can be rendered to static markup in tests.
 */
export function SubagentStreamList({ rows }: { rows: SubagentActivityRow[] }): JSX.Element {
  return (
    <aside className="panel panel--stream panel--subagents">
      <header className="panel-header">
        <h2>Subagents</h2>
        <p className="chat-meta">Delegated child runs from the harness event stream.</p>
      </header>
      <div className="panel-body">
        {rows.length === 0 ? (
          <p className="panel-empty">
            No subagent activity yet. Governed delegated runs appear here when the
            runtime records them.
          </p>
        ) : (
          <ul className="harness-stream-list">
            {rows.map((row) => (
              <SubagentActivityItem key={row.key} row={row} />
            ))}
          </ul>
        )}
      </div>
    </aside>
  );
}

export function SubagentStreamView(): JSX.Element {
  const { events } = useHarnessEvents();
  const rows = useMemo(() => deriveSubagentActivity(events), [events]);
  return <SubagentStreamList rows={rows} />;
}
