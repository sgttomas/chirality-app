'use client';

import React, { useEffect, useMemo, useState } from 'react';
import { decideHarnessPermission } from '../../lib/harness/client';
import {
  selectPendingPermissionRequests,
  type PermissionRequestRow
} from '../../lib/shell/harness-event-views';
import { useHarnessEvents } from '../workspace/harness-events-provider';

type PermissionDecisionCardsProps = {
  sessionId: string | null;
  requests: PermissionRequestRow[];
};

/**
 * Presentational approval cards over already-derived pending requests,
 * decoupled from context so they can be rendered to static markup in tests.
 */
export function PermissionDecisionCards({
  sessionId,
  requests
}: PermissionDecisionCardsProps): JSX.Element | null {
  const [submitting, setSubmitting] = useState<Record<string, 'allow' | 'deny'>>({});
  const [error, setError] = useState<string | null>(null);

  const requestKeys = requests.map((row) => row.key).join('|');

  // Prune transient state for requests that are no longer pending (e.g. a new
  // turn cleared the stream) so it never bleeds into a later approval card.
  useEffect(() => {
    const live = new Set(requestKeys.length > 0 ? requestKeys.split('|') : []);
    setSubmitting((current) => {
      const next: Record<string, 'allow' | 'deny'> = {};
      let changed = false;
      for (const [key, value] of Object.entries(current)) {
        if (live.has(key)) {
          next[key] = value;
        } else {
          changed = true;
        }
      }
      return changed ? next : current;
    });
    if (live.size === 0) {
      setError(null);
    }
  }, [requestKeys]);

  async function decide(row: PermissionRequestRow, verdict: 'allow' | 'deny'): Promise<void> {
    // Prefer the session captured on the request itself, so a pending approval
    // stays actionable even if the operator navigated away and the panel's
    // `sessionId` prop is now null/different (DESIGN §5.3 item b).
    const targetSessionId = row.sessionId || sessionId;
    if (!targetSessionId) {
      return;
    }
    setSubmitting((current) => ({ ...current, [row.key]: verdict }));
    setError(null);
    try {
      await decideHarnessPermission({ sessionId: targetSessionId, toolUseId: row.key, verdict });
      // The follow-up tool.permission event removes this card from the stream.
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : 'Unable to submit decision.');
      setSubmitting((current) => {
        const next = { ...current };
        delete next[row.key];
        return next;
      });
    }
  }

  if (requests.length === 0) {
    return null;
  }

  return (
    <section
      className="permission-card-list"
      role="region"
      aria-label="Pending tool approvals"
      aria-live="polite"
    >
      {requests.map((row) => {
        const pendingVerdict = submitting[row.key];
        const pathEntries = Object.entries(row.pathFields);
        const canDecide = Boolean(row.sessionId || sessionId);
        return (
          <article
            key={row.key}
            className="permission-card"
            role="group"
            aria-label={`Approval required: ${row.toolName}`}
          >
            <header className="permission-card-header">
              <span className="permission-card-tool" title={row.toolName}>
                {row.toolName}
              </span>
              <span className="permission-card-badge">approval required</span>
            </header>
            {row.reason ? <p className="permission-card-reason">{row.reason}</p> : null}
            {row.method ? <p className="harness-stream-meta">{row.method}{row.requestId ? ` · request ${row.requestId}` : ''}</p> : null}
            {pathEntries.length > 0 ? (
              <ul className="permission-card-paths">
                {pathEntries.map(([field, value]) => (
                  <li key={field} title={`${field}: ${value}`}>
                    <span className="permission-card-path-field">{field}</span>
                    <span className="permission-card-path-value">{value}</span>
                  </li>
                ))}
              </ul>
            ) : null}
            <div className="permission-card-actions">
              <button
                type="button"
                className="permission-card-approve"
                disabled={Boolean(pendingVerdict) || !canDecide}
                onClick={() => {
                  void decide(row, 'allow');
                }}
              >
                {pendingVerdict === 'allow' ? 'Approving...' : 'Approve'}
              </button>
              <button
                type="button"
                className="button-muted permission-card-deny"
                disabled={Boolean(pendingVerdict) || !canDecide}
                onClick={() => {
                  void decide(row, 'deny');
                }}
              >
                {pendingVerdict === 'deny' ? 'Denying...' : 'Deny'}
              </button>
            </div>
          </article>
        );
      })}
      {error ? <p className="permission-card-error">{error}</p> : null}
    </section>
  );
}

/**
 * Live wrapper: reads the bridged harness-event stream and surfaces only the
 * Codex approvals (`tool.permission` with behavior `ask`) awaiting a decision.
 * Isolated from the chat transcript so its per-event re-renders stay cheap.
 *
 * `active` is the Runtime's own turn state (turn/state, or the live stream the
 * panel observes), not a local guess. When a turn ends the Runtime answers every
 * still-pending request as cancelled, so a leftover `pending` row is no longer
 * actionable and is hidden the moment the turn is reported over. Pending
 * approvals survive renderer disconnects: reopening the chat replays them from
 * the persisted events while the Runtime still reports the turn active.
 */
export function PermissionRequests({
  sessionId,
  active = true
}: {
  sessionId: string | null;
  active?: boolean;
}): JSX.Element | null {
  const { events } = useHarnessEvents();
  const pending = useMemo(
    () => selectPendingPermissionRequests(events, active),
    [events, active]
  );
  return <PermissionDecisionCards sessionId={sessionId} requests={pending.filter(row => !row.requestId)} />;
}
