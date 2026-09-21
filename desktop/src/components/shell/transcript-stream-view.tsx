'use client';

import React, { useMemo } from 'react';
import {
  deriveTranscriptView,
  type TranscriptArtifactLink,
  type TranscriptItem,
  type TranscriptItemStatus
} from '@chirality/runtime-contracts/transcript-replay';
import { useHarnessEvents } from '../workspace/harness-events-provider';

function statusClass(status: TranscriptItemStatus): string {
  if (status === 'failed' || status === 'cancelled' || status === 'interrupted') {
    return 'failed';
  }
  if (status === 'completed') {
    return 'completed';
  }
  if (status === 'started') {
    return 'running';
  }
  if (status === 'queued' || status === 'accepted') {
    return 'queued';
  }
  return 'permission';
}

function artifactEntries(artifact: TranscriptArtifactLink | undefined): Array<[string, string]> {
  if (!artifact) {
    return [];
  }
  return [
    ['artifact', artifact.artifactRelativePath ?? artifact.artifactPath],
    [
      'size',
      artifact.artifactByteLength === undefined
        ? undefined
        : `${artifact.artifactByteLength} bytes`
    ],
    ['sha256', artifact.sha256],
    ['retention', artifact.retentionPolicy],
    ['truncated', artifact.truncated === undefined ? undefined : String(artifact.truncated)]
  ].filter((entry): entry is [string, string] => typeof entry[1] === 'string' && entry[1].length > 0);
}

function TranscriptItemView({ item }: { item: TranscriptItem }): JSX.Element {
  const status = statusClass(item.status);
  const artifacts = artifactEntries(item.artifact);

  return (
    <li className={`harness-stream-item harness-stream-item--${status}`}>
      <div className="harness-stream-row">
        <span className="harness-stream-name" title={item.title}>
          {item.title}
        </span>
        <span className={`harness-status-badge harness-status-badge--${status}`}>
          {item.status}
        </span>
      </div>
      {item.text ? <p className="harness-stream-description transcript-text">{item.text}</p> : null}
      {item.summary ? <p className="harness-stream-summary">{item.summary}</p> : null}
      {artifacts.length > 0 ? (
        <ul className="harness-stream-paths">
          {artifacts.map(([field, value]) => (
            <li key={field} title={`${field}: ${value}`}>
              <span className="harness-stream-path-field">{field}</span>
              <span className="harness-stream-path-value">{value}</span>
            </li>
          ))}
        </ul>
      ) : null}
      <p className="harness-stream-meta">
        {item.role ? `${item.role} / ` : ''}
        {item.toolName ? `${item.toolName} / ` : ''}
        {item.eventType}
      </p>
    </li>
  );
}

export function TranscriptStreamList({ items }: { items: TranscriptItem[] }): JSX.Element {
  return (
    <aside className="panel panel--stream panel--transcript">
      <header className="panel-header">
        <h2>Transcript</h2>
        <p className="chat-meta">Reconstructed from the harness event stream.</p>
      </header>
      <div className="panel-body">
        {items.length === 0 ? (
          <p className="panel-empty">No transcript events loaded.</p>
        ) : (
          <ol className="harness-stream-list transcript-list">
            {items.map((item) => (
              <TranscriptItemView key={item.key} item={item} />
            ))}
          </ol>
        )}
      </div>
    </aside>
  );
}

export function TranscriptStreamView(): JSX.Element {
  const { events } = useHarnessEvents();
  const transcript = useMemo(() => deriveTranscriptView(events), [events]);
  return <TranscriptStreamList items={transcript.items} />;
}
