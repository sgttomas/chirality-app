'use client';

import React, { useCallback, useEffect, useRef, useState } from 'react';
import {
  harnessApiErrorMessage,
  listHarnessSessions,
  replaySessionEvents
} from '../../lib/harness/client';
import type { SessionRecord } from '@chirality/runtime-contracts/types';
import {
  useHarnessEventActions,
  useHarnessStreaming
} from '../workspace/harness-events-provider';
import { useWorkspace } from '../workspace/workspace-provider';
import { useRuntimeEpoch } from './runtime-connectivity-provider';

type SessionListPanelProps = {
  hasProjectRoot: boolean;
  sessions: SessionRecord[];
  loading: boolean;
  error: string | null;
  notice: string | null;
  openingId: string | null;
  streaming: boolean;
  onRefresh: () => void;
  onOpen: (sessionId: string) => void;
};

/**
 * Presentational session list, decoupled from context so it can be rendered to
 * static markup in tests (mirrors `ToolStreamList`).
 */
export function SessionListPanel({
  hasProjectRoot,
  sessions,
  loading,
  error,
  notice,
  openingId,
  streaming,
  onRefresh,
  onOpen
}: SessionListPanelProps): JSX.Element {
  return (
    <aside className="panel panel--stream panel--sessions">
      <header className="panel-header">
        <h2>Sessions</h2>
        <p className="chat-meta">Reopen a past session to load its event history (D-APP-22).</p>
      </header>
      <div className="panel-body">
        {!hasProjectRoot ? (
          <p className="panel-empty">Select a Working Root to list its sessions.</p>
        ) : (
          <>
            <div className="session-list-controls">
              <button
                type="button"
                className="button-muted"
                onClick={onRefresh}
                disabled={loading}
              >
                {loading ? 'Loading…' : 'Refresh'}
              </button>
            </div>
            {error ? (
              <p className="panel-error" role="alert">
                {error}
              </p>
            ) : null}
            {streaming ? (
              <p className="session-list-notice" role="status">
                A turn is running — finish or interrupt it before opening a past session (its live
                events would otherwise be replaced).
              </p>
            ) : notice ? (
              <p className="session-list-notice" role="status">
                {notice}
              </p>
            ) : null}
            {!loading && sessions.length === 0 ? (
              <p className="panel-empty">No sessions recorded for this Working Root yet.</p>
            ) : (
              <ul className="session-list">
                {sessions.map((session) => (
                  <li key={session.sessionId} className="session-list-item">
                    <div className="session-list-meta">
                      <span className="session-list-persona">{session.persona}</span>
                      <span className="session-list-mode">{session.mode}</span>
                      <span className="session-list-time" title={session.createdAt}>
                        {session.createdAt}
                      </span>
                    </div>
                    <button
                      type="button"
                      className="session-list-open"
                      onClick={() => {
                        onOpen(session.sessionId);
                      }}
                      disabled={openingId !== null || streaming}
                    >
                      {openingId === session.sessionId ? 'Opening…' : 'Open'}
                    </button>
                  </li>
                ))}
              </ul>
            )}
          </>
        )}
      </div>
    </aside>
  );
}

/**
 * Session-list sidebar view (D-APP-22). Lists the Working Root's sessions and,
 * on "Open", replays the session's persisted events and hydrates the live
 * buffer — so transcript, tool, and subagent views render that past session's history.
 * Hydrate REPLACES the buffer (bounded), so it never double-counts live events.
 */
export function SessionListView(): JSX.Element {
  const { projectRoot } = useWorkspace();
  const { hydrateEvents } = useHarnessEventActions();
  const streaming = useHarnessStreaming();
  const [sessions, setSessions] = useState<SessionRecord[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [notice, setNotice] = useState<string | null>(null);
  const [openingId, setOpeningId] = useState<string | null>(null);
  const [refreshNonce, setRefreshNonce] = useState(0);
  const runtimeEpoch = useRuntimeEpoch();

  // Track the live projectRoot so an in-flight open can detect a switch on
  // resolve and abandon a now-stale hydrate (the shared event buffer is global).
  const projectRootRef = useRef(projectRoot);
  projectRootRef.current = projectRoot;

  // Any open-result notice / in-flight "Opening…" belongs to the previous
  // Working Root; clear them when the root changes (not on a same-root refresh).
  useEffect(() => {
    setNotice(null);
    setOpeningId(null);
  }, [projectRoot]);

  useEffect(() => {
    if (!projectRoot) {
      setSessions([]);
      setError(null);
      setLoading(false);
      return;
    }

    let cancelled = false;
    setLoading(true);
    setError(null);
    listHarnessSessions(projectRoot)
      .then((records) => {
        if (!cancelled) {
          setSessions(records);
        }
      })
      .catch((cause) => {
        if (!cancelled) {
          setError(harnessApiErrorMessage(cause));
        }
      })
      .finally(() => {
        if (!cancelled) {
          setLoading(false);
        }
      });

    return () => {
      cancelled = true;
    };
    // `runtimeEpoch` re-lists after a reconnect: a list fetched against a dead
    // socket is an error banner over an empty list, and the operator has no way
    // to tell that from "this root genuinely has no sessions".
  }, [projectRoot, refreshNonce, runtimeEpoch]);

  const openSession = useCallback(
    async (sessionId: string): Promise<void> => {
      // Hydrating mid-turn would replace the live turn's events with a past
      // session's (D-APP-22 "no same-turn mix"); the button is also disabled.
      if (streaming) {
        return;
      }

      const rootAtOpen = projectRootRef.current;
      setOpeningId(sessionId);
      setError(null);
      try {
        const replay = await replaySessionEvents(sessionId);
        if (projectRootRef.current !== rootAtOpen) {
          // Working Root switched while the replay was in flight — abandon it
          // so we never hydrate another root's events into the shared buffer.
          return;
        }
        hydrateEvents(replay.events);
        const malformed =
          replay.malformedLineCount > 0
            ? ` (${replay.malformedLineCount} malformed line${
                replay.malformedLineCount === 1 ? '' : 's'
              } skipped)`
            : '';
        setNotice(
          `Loaded ${replay.events.length} event${
            replay.events.length === 1 ? '' : 's'
          }${malformed}. View them in the Transcript / Tools / Subagents tabs.`
        );
      } catch (cause) {
        if (projectRootRef.current === rootAtOpen) {
          setError(harnessApiErrorMessage(cause));
        }
      } finally {
        setOpeningId((current) => (current === sessionId ? null : current));
      }
    },
    [streaming, hydrateEvents]
  );

  return (
    <SessionListPanel
      hasProjectRoot={Boolean(projectRoot)}
      sessions={sessions}
      loading={loading}
      error={error}
      notice={notice}
      openingId={openingId}
      streaming={streaming}
      onRefresh={() => {
        setRefreshNonce((nonce) => nonce + 1);
      }}
      onOpen={(sessionId) => {
        void openSession(sessionId);
      }}
    />
  );
}
