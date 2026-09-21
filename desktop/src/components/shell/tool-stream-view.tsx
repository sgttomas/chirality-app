'use client';

import React, { useMemo } from 'react';
import { deriveToolActivity, type ToolActivityRow } from '../../lib/shell/harness-event-views';
import { useHarnessEvents } from '../workspace/harness-events-provider';

function ToolActivityItem({ row }: { row: ToolActivityRow }): JSX.Element {
  const pathEntries = Object.entries(row.pathFields);

  return (
    <li className={`harness-stream-item harness-stream-item--${row.status}`}>
      <div className="harness-stream-row">
        <span className="harness-stream-name" title={row.toolName}>
          {row.toolName}
        </span>
        <span className={`harness-status-badge harness-status-badge--${row.status}`}>
          {row.status}
        </span>
      </div>
      {pathEntries.length > 0 ? (
        <ul className="harness-stream-paths">
          {pathEntries.map(([field, value]) => (
            <li key={field} title={`${field}: ${value}`}>
              <span className="harness-stream-path-field">{field}</span>
              <span className="harness-stream-path-value">{value}</span>
            </li>
          ))}
        </ul>
      ) : null}
      <p className="harness-stream-meta">
        {row.source ? `${row.source} · ` : ''}
        {row.surface ? `${row.surface} · ` : ''}
        {row.eventCount} event{row.eventCount === 1 ? '' : 's'}
      </p>
    </li>
  );
}

/**
 * Presentational list over already-derived rows, decoupled from context so it
 * can be rendered to static markup in tests.
 */
export function ToolStreamList({ rows }: { rows: ToolActivityRow[] }): JSX.Element {
  return (
    <aside className="panel panel--stream panel--tools">
      <header className="panel-header">
        <h2>Tools</h2>
        <p className="chat-meta">Live tool calls from the harness event stream.</p>
      </header>
      <div className="panel-body">
        {rows.length === 0 ? (
          <p className="panel-empty">
            No tool activity yet. Governed tool calls appear here when the selected engine
            exposes them.
          </p>
        ) : (
          <ul className="harness-stream-list">
            {rows.map((row) => (
              <ToolActivityItem key={row.key} row={row} />
            ))}
          </ul>
        )}
      </div>
    </aside>
  );
}

export function ToolStreamView(): JSX.Element {
  const { events } = useHarnessEvents();
  const rows = useMemo(() => deriveToolActivity(events), [events]);
  return <ToolStreamList rows={rows} />;
}
