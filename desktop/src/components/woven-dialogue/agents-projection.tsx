'use client';

import React from 'react';
import type {
  OperatorSessionProjection,
  RecordedAgentHierarchy
} from '../../lib/woven-dialogue/contracts';

type AgentsProjectionProps = {
  hierarchy: RecordedAgentHierarchy;
  loading: boolean;
  error: string | null;
  selectedSessionId?: string;
  selectionDisabled: boolean;
  onRefresh: () => void;
  onSelectSession: (sessionId: string) => void;
};

type Relationship =
  | { kind: 'ROOT' }
  | { kind: 'CHILD'; parent: OperatorSessionProjection }
  | { kind: 'DETACHED' };

const ROLE_LABELS: Record<NonNullable<OperatorSessionProjection['role']>, string> = {
  agent0: 'Type 0',
  agent1: 'Type 1',
  agent2: 'Type 2'
};

function recordedAgentLabel(session: OperatorSessionProjection): string | undefined {
  return session.persona ?? (session.role ? ROLE_LABELS[session.role] : undefined);
}

function relationshipLabel(relationship: Relationship): string {
  if (relationship.kind === 'ROOT') {
    return 'Top-level';
  }
  if (relationship.kind === 'DETACHED') {
    return 'Parent relationship unavailable';
  }
  const parentLabel = recordedAgentLabel(relationship.parent);
  return parentLabel ? `Parent: ${parentLabel}` : 'Parent relationship recorded';
}

function SessionCard({
  session,
  relationship,
  depth,
  childrenByParentSessionId,
  selectedSessionId,
  selectionDisabled,
  onSelectSession
}: {
  session: OperatorSessionProjection;
  relationship: Relationship;
  depth: number;
  childrenByParentSessionId: RecordedAgentHierarchy['childrenByParentSessionId'];
  selectedSessionId?: string;
  selectionDisabled: boolean;
  onSelectSession: (sessionId: string) => void;
}): JSX.Element {
  const children = childrenByParentSessionId[session.sessionId] ?? [];
  const roleLabel = session.role ? ROLE_LABELS[session.role] : undefined;
  const agentLabel = recordedAgentLabel(session);

  return (
    <li className="woven-agent-branch">
      <button
        type="button"
        className={
          selectedSessionId === session.sessionId
            ? 'woven-agent-card woven-agent-card--selected'
            : 'woven-agent-card'
        }
        style={{ '--agent-depth': depth } as React.CSSProperties}
        disabled={selectionDisabled}
        aria-pressed={selectedSessionId === session.sessionId}
        onClick={() => {
          onSelectSession(session.sessionId);
        }}
      >
        {roleLabel ? <strong>{roleLabel}</strong> : null}
        {session.persona ? <span>Role: {session.persona}</span> : null}
        <small>{relationshipLabel(relationship)}</small>
      </button>
      {children.length > 0 ? (
        <ol
          className="woven-agent-children"
          aria-label={agentLabel ? `Agents reporting to ${agentLabel}` : 'Child agents'}
        >
          {children.map((child) => (
            <SessionCard
              key={child.sessionId}
              session={child}
              relationship={{ kind: 'CHILD', parent: session }}
              depth={depth + 1}
              childrenByParentSessionId={childrenByParentSessionId}
              selectedSessionId={selectedSessionId}
              selectionDisabled={selectionDisabled}
              onSelectSession={onSelectSession}
            />
          ))}
        </ol>
      ) : null}
    </li>
  );
}

export function AgentsProjection({
  hierarchy,
  loading,
  error,
  selectedSessionId,
  selectionDisabled,
  onRefresh,
  onSelectSession
}: AgentsProjectionProps): JSX.Element {
  return (
    <section className="woven-projection" aria-label="Recorded agent tree">
      <div className="woven-projection-toolbar">
        <p>Recorded agent tree</p>
        <button type="button" className="button-muted" disabled={loading} onClick={onRefresh}>
          {loading ? 'Refreshing…' : 'Refresh'}
        </button>
      </div>

      {selectionDisabled ? (
        <p className="woven-projection-notice" role="status">
          Agent selection is paused while the primary dialogue is running.
        </p>
      ) : null}
      {error ? (
        <p className="panel-error" role="alert">
          {error}
        </p>
      ) : null}

      {!loading && hierarchy.roots.length === 0 ? (
        hierarchy.detached.length === 0 ? (
          <p className="panel-empty">No recorded agents are available for this Working Root.</p>
        ) : null
      ) : (
        <ol className="woven-agent-tree" aria-label="Top-level agents">
          {hierarchy.roots.map((session) => (
            <SessionCard
              key={session.sessionId}
              session={session}
              relationship={{ kind: 'ROOT' }}
              depth={0}
              childrenByParentSessionId={hierarchy.childrenByParentSessionId}
              selectedSessionId={selectedSessionId}
              selectionDisabled={selectionDisabled}
              onSelectSession={onSelectSession}
            />
          ))}
        </ol>
      )}

      {hierarchy.detached.length > 0 ? (
        <section className="woven-detached-agents" aria-label="Agents without an available parent">
          <h3>Parent relationship unavailable</h3>
          <ol className="woven-agent-tree">
            {hierarchy.detached.map((session) => (
              <SessionCard
                key={session.sessionId}
                session={session}
                relationship={{ kind: 'DETACHED' }}
                depth={0}
                childrenByParentSessionId={{}}
                selectedSessionId={selectedSessionId}
                selectionDisabled={selectionDisabled}
                onSelectSession={onSelectSession}
              />
            ))}
          </ol>
        </section>
      ) : null}
    </section>
  );
}
