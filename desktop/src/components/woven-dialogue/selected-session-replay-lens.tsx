'use client';

import React, { useEffect, useState } from 'react';
import type { TranscriptItem } from '@chirality/runtime-contracts/transcript-replay';
import type {
  FrozenInstructionBasisV3,
  InstructionHistoryRecordV3,
  QualifiedMethodReference
} from '@chirality/runtime-contracts/v3';
import type { NativePlanRevision } from '@chirality/runtime-contracts/v3';
import { nativePlanText } from '../../lib/harness/native-plan-text';
import { listNativePlanRevisions } from '../../lib/harness/method-selection-client';
import type {
  ProjectionDiagnostic,
  SelectedSessionReplayProjection,
  SelectedSessionReplayState
} from '../../lib/woven-dialogue/contracts';

export type SelectedSessionReplayLensProps = {
  state: SelectedSessionReplayState;
  primarySessionId?: string;
  onReturnToPrimary: () => void;
  onRetry?: () => void;
  onContinue?: (projection: SelectedSessionReplayProjection) => void;
};

function ReplayHeader({
  selectedSessionId,
  primarySessionId,
  onReturnToPrimary,
  onContinue
}: {
  selectedSessionId: string;
  primarySessionId?: string;
  onReturnToPrimary: () => void;
  onContinue?: () => void;
}): JSX.Element {
  return (
    <header className="woven-replay-header">
      <div>
        <p className="woven-replay-eyebrow">Recorded chat · read-only</p>
        <h2>Recorded session</h2>
        <details><summary>Session details</summary><p>
          <span>Selected session: </span>
          <code>{selectedSessionId}</code>
        </p>
        {primarySessionId ? (
          <p>
            <span>Primary dialogue remains mounted: </span>
            <code>{primarySessionId}</code>
          </p>
        ) : null}</details>
      </div>
      <button type="button" onClick={onReturnToPrimary}>
        Return to primary dialogue
      </button>
      {onContinue ? <button type="button" onClick={onContinue}>Continue this chat</button> : null}
    </header>
  );
}

function DiagnosticList({
  diagnostics
}: {
  diagnostics: readonly ProjectionDiagnostic[];
}): JSX.Element | null {
  if (diagnostics.length === 0) {
    return null;
  }

  return (
    <ul className="woven-replay-diagnostics" aria-label="Replay disclosures">
      {diagnostics.map((diagnostic, index) => (
        <li key={`${diagnostic.code}:${index}`}>
          <strong>{diagnostic.code}</strong>: {diagnostic.message}
        </li>
      ))}
    </ul>
  );
}

function TranscriptItemView({ item }: { item: TranscriptItem }): JSX.Element {
  const artifactReference =
    item.artifact?.artifactRelativePath ?? item.artifact?.artifactPath;

  return (
    <li className="woven-replay-item">
      <div>
        <strong>{item.title}</strong>
        <span> — {item.status}</span>
      </div>
      {item.text ? <p>{item.text}</p> : null}
      {item.attachments?.length ? <ul aria-label="Recorded attachments">{item.attachments.map((path, index) => <li key={`${path}:${index}`}>{path.split(/[\\/]/).at(-1)}</li>)}</ul> : null}
      {item.summary ? <p>{item.summary}</p> : null}
      {artifactReference ? (
        <p>
          <span>Artifact reference: </span>
          <code>{artifactReference}</code>
        </p>
      ) : null}
      <details><summary>Event details</summary><p>
        <span>Event: </span>
        <code>{item.eventId}</code>
        <span> / {item.eventType}</span>
      </p></details>
    </li>
  );
}

function methodLabel(method: QualifiedMethodReference): string {
  return `${method.name} · ${method.source} ${method.kind}`;
}

function historyBasisId(record: InstructionHistoryRecordV3): string | undefined {
  return typeof record.basisId === 'string' ? record.basisId : undefined;
}

function historyLabel(record: InstructionHistoryRecordV3): string {
  switch (record.type) {
    case 'selection.changed': return 'Role or method selection updated';
    case 'resource.loaded': return 'Method resource loaded';
    case 'instruction-basis.resolved': return 'Instruction basis recorded';
    case 'method-change.requested': return 'Method change requested';
    case 'method-change.applied': return 'Method change applied';
    case 'method-change.failed': return 'Method change failed';
    case 'native-plan.revised': return 'Native plan revised';
    case 'provider-span.prepared': return 'Conversation continuation prepared';
    case 'provider-span.committed': return 'Conversation continuation committed';
    case 'provider-span.continued': return 'Conversation continued with a new provider span';
    case 'provider-span.cancelled': return 'Conversation continuation cancelled';
    case 'provider-span.failed': return 'Conversation continuation failed';
    default: return 'Instruction context updated';
  }
}

function InstructionHistoryView({
  history,
  bases
}: {
  history: readonly InstructionHistoryRecordV3[];
  bases: readonly FrozenInstructionBasisV3[];
}): JSX.Element | null {
  if (history.length === 0 && bases.length === 0) return null;
  return <section className="woven-instruction-history" aria-label="Recorded instruction history">
    <h3>Instruction history</h3>
    <p>Recorded selections, loaded resources, and instruction bases. These records do not indicate workflow progress.</p>
    {history.length ? <ol>
      {history.map(record => <li key={record.historyId}>
        <strong>{historyLabel(record)}</strong>
        <span> · sequence {record.sequence}</span>
        {historyBasisId(record) ? <span> · basis <code>{historyBasisId(record)}</code></span> : null}
        <time dateTime={record.timestamp}> · {record.timestamp}</time>
      </li>)}
    </ol> : null}
    {bases.map(basis => <details key={basis.basisId}>
      <summary>Basis {basis.basisId} · {basis.roleId}</summary>
      <dl>
        <dt>Recorded</dt><dd>{basis.createdAt}</dd>
        <dt>Interaction</dt><dd>{basis.interactionMode}</dd>
        <dt>Permission</dt><dd>{basis.permissionMode}</dd>
      </dl>
      {basis.selectedMethods.length ? <ul aria-label="Selected methods">
        {basis.selectedMethods.map(method => <li key={`${method.sourceRootId}:${method.kind}:${method.name}`}>{methodLabel(method)}</li>)}
      </ul> : <p>No methods selected.</p>}
      {basis.suppliedEntries.length ? <ul aria-label="Supplied instruction entries">
        {basis.suppliedEntries.map((entry, index) => <li key={`${entry.sha256}:${index}`}>
          <strong>{entry.kind}</strong> · {entry.id}<br />
          <small>{entry.origin} · <code>{entry.sha256}</code></small>
        </li>)}
      </ul> : <p>No supplied instruction entries were recorded.</p>}
    </details>)}
  </section>;
}

function RecordedNativePlans({ sessionId }: { sessionId: string }): JSX.Element | null {
  const [revisions, setRevisions] = useState<readonly NativePlanRevision[]>([]);
  useEffect(() => {
    const controller = new AbortController();
    setRevisions([]);
    void listNativePlanRevisions(sessionId, controller.signal)
      .then(result => { if (!controller.signal.aborted) setRevisions(result.revisions); })
      .catch(() => { if (!controller.signal.aborted) setRevisions([]); });
    return () => controller.abort();
  }, [sessionId]);
  if (!revisions.length) return null;
  return <section className="woven-native-plan-history" aria-label="Recorded native plans">
    <h3>Native plans</h3>
    {revisions.map(revision => <details key={revision.revision}>
      <summary>Revision {revision.revision}</summary>
      <pre>{nativePlanText(revision)}</pre>
    </details>)}
  </section>;
}

function ReadyReplay({
  projection
}: {
  projection: SelectedSessionReplayProjection;
}): JSX.Element {
  const attribution = projection.session;

  return (
    <>
      <details><summary>Inspect recorded session</summary>
      <section
        className="woven-replay-provenance"
        aria-label="Replay provenance and status"
        // The Session panel is narrower than the former full-width replay.
        // Stack both the groups and their label/value tracks so values retain
        // the panel's available width, including long canonical source paths.
        style={{ gridTemplateColumns: 'minmax(0, 1fr)' }}
      >
        <dl style={{ gridTemplateColumns: 'minmax(0, 1fr)' }}>
          <dt>Source</dt>
          <dd>
            <code>{projection.sourceReference}</code>
          </dd>
          <dt>Observed</dt>
          <dd>{projection.observedAt}</dd>
          <dt>Disclosure</dt>
          <dd>{projection.disclosure}</dd>
          <dt>Currency</dt>
          <dd>{projection.currency}</dd>
          <dt>Events</dt>
          <dd>{projection.sourceEventCount}</dd>
          <dt>Transcript items shown</dt>
          <dd>
            {projection.bounded
              ? `${projection.bounded.rendered} of ${projection.bounded.available}`
              : projection.renderedItemCount}
          </dd>
          <dt>Malformed records skipped</dt>
          <dd>{projection.malformedLineCount}</dd>
        </dl>
        {attribution ? (
          <dl
            aria-label="Recorded session attribution"
            style={{ gridTemplateColumns: 'minmax(0, 1fr)' }}
          >
            {attribution.persona ? (
              <>
                <dt>Recorded legacy role</dt>
                <dd>{attribution.persona}</dd>
              </>
            ) : null}
            {attribution.role ? (
              <>
                <dt>Role</dt>
                <dd>{attribution.role}</dd>
              </>
            ) : null}
            {attribution.runtimeStatus ? (
              <>
                <dt>Recorded runtime status</dt>
                <dd>{attribution.runtimeStatus}</dd>
              </>
            ) : null}
            {attribution.adapterId ? (
              <>
                <dt>Adapter</dt>
                <dd>{attribution.adapterId}</dd>
              </>
            ) : null}
            {attribution.providerId ? (
              <>
                <dt>Provider</dt>
                <dd>{attribution.providerId}</dd>
              </>
            ) : null}
            {attribution.model ? (
              <>
                <dt>Recorded model selection</dt>
                <dd>{attribution.model}</dd>
              </>
            ) : null}
            {attribution.reasoningEffort ? (
              <>
                <dt>Reasoning</dt>
                <dd>{attribution.reasoningEffort}</dd>
              </>
            ) : null}
            {attribution.residencyEpoch ? (
              <>
                <dt>Residency epoch</dt>
                <dd>{attribution.residencyEpoch}</dd>
              </>
            ) : null}
          </dl>
        ) : (
          <p>Session metadata unavailable; event evidence only.</p>
        )}
      </section>

      <DiagnosticList diagnostics={projection.diagnostics} />

      <InstructionHistoryView
        history={projection.instructionHistory}
        bases={projection.instructionBases}
      />

      </details>
      <RecordedNativePlans sessionId={projection.selectedSessionId} />

      <section className="woven-replay-transcript" aria-label="Read-only transcript">
        {projection.transcript.items.length === 0 ? (
          <p>
            {projection.disclosure === 'EVIDENCE_ONLY'
              ? 'No transcript items were recorded; canonical event evidence may still exist.'
              : 'No transcript items were recorded for this session.'}
          </p>
        ) : (
          <ol>
            {projection.transcript.items.map((item) => (
              <TranscriptItemView key={item.key} item={item} />
            ))}
          </ol>
        )}
      </section>
    </>
  );
}

/**
 * Observational presentation only. The component intentionally exposes no
 * send, continue, interrupt, permission, resume, boot, delete, or lifecycle
 * action.
 */
export function SelectedSessionReplayLens({
  state,
  primarySessionId,
  onReturnToPrimary,
  onRetry,
  onContinue
}: SelectedSessionReplayLensProps): JSX.Element | null {
  if (state.status === 'IDLE') {
    return null;
  }

  const selectedSessionId =
    state.status === 'READY'
      ? state.projection.selectedSessionId
      : state.selectedSessionId;

  return (
    <section
      className="woven-replay-lens"
      style={{ overflowWrap: 'anywhere' }}
      aria-label="Selected-session read-only replay"
      data-replay-state={state.status}
      data-replay-disclosure={
        state.status === 'READY' ? state.projection.disclosure : undefined
      }
    >
      <ReplayHeader
        selectedSessionId={selectedSessionId}
        primarySessionId={primarySessionId}
        onReturnToPrimary={onReturnToPrimary}
        onContinue={state.status === 'READY' && state.projection.session?.continuation && !['CONFLICTING', 'STALE', 'MALFORMED', 'BOUNDED'].includes(state.projection.disclosure) && onContinue
          ? () => onContinue(state.projection) : undefined}
      />

      {state.status === 'LOADING' ? (
        <p role="status">Loading canonical replay evidence…</p>
      ) : null}

      {state.status === 'UNAVAILABLE' ? (
        <div role="alert">
          <p>Replay unavailable: {state.message}</p>
          {onRetry ? (
            <button type="button" onClick={onRetry}>
              Retry
            </button>
          ) : null}
        </div>
      ) : null}

      {state.status === 'READY' ? (
        <ReadyReplay projection={state.projection} />
      ) : null}
    </section>
  );
}
