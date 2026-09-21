'use client';

import React, { useCallback, useEffect, useRef, useState } from 'react';
import { RequestCards, useLiveSessionRequests } from '../shell/request-card';
import type { ServerRequestRow } from '../../lib/shell/harness-event-views';

/** Share each background chat's one live request reader between its badge and dialog. */
function RequestObserver({ sessionId, onRows }: { sessionId: string; onRows: (id: string, rows: ServerRequestRow[]) => void }): null {
  const rows = useLiveSessionRequests(sessionId);
  const serialized = JSON.stringify(rows);
  useEffect(() => {
    onRows(sessionId, JSON.parse(serialized) as ServerRequestRow[]);
    return () => onRows(sessionId, []);
  }, [sessionId, serialized, onRows]);
  return null;
}

export function useChatAttention(sessionIds: readonly string[]) {
  const [rowsBySession, setRows] = useState<Record<string, ServerRequestRow[]>>({});
  const onRows = useCallback((id: string, rows: ServerRequestRow[]) => {
    setRows(current => {
      if (rows.length === 0 && !current[id]) return current;
      const next = { ...current };
      if (rows.length) next[id] = rows; else delete next[id];
      return next;
    });
  }, []);
  const live = new Set(sessionIds);
  const rows = Object.fromEntries(Object.entries(rowsBySession).filter(([id]) => live.has(id)));
  return { rows, observers: sessionIds.map(id => <RequestObserver key={id} sessionId={id} onRows={onRows} />) };
}

export function ChatAttentionDialog({ sessionId, title, rows, onClose }: {
  sessionId: string; title: string; rows: ServerRequestRow[]; onClose: () => void;
}): JSX.Element {
  const ref = useRef<HTMLDivElement>(null);
  const headingId = React.useId();
  useEffect(() => {
    const previous = document.activeElement instanceof HTMLElement ? document.activeElement : null;
    ref.current?.querySelector<HTMLButtonElement>('button')?.focus();
    return () => { if (previous?.isConnected) previous.focus(); };
  }, []);
  return <div className="woven-chat-dialog-backdrop"><div ref={ref} className="woven-chat-dialog" style={{ maxHeight: '80vh', overflowY: 'auto' }} role="dialog" aria-modal="true" aria-labelledby={headingId}
    onKeyDown={event => {
      if (event.key === 'Escape') { event.preventDefault(); event.stopPropagation(); onClose(); }
      if (event.key !== 'Tab') return;
      const controls = [...(ref.current?.querySelectorAll<HTMLElement>('button:not(:disabled), input:not(:disabled), select:not(:disabled), textarea:not(:disabled), summary, [tabindex="0"]') ?? [])];
      const first = controls[0]; const last = controls[controls.length - 1];
      if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last?.focus(); }
      else if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first?.focus(); }
    }}>
    <h2 id={headingId}>{title}</h2>
    <button type="button" className="button-muted" onClick={onClose}>Close requests</button>
    {rows.length ? <RequestCards sessionId={sessionId} requests={rows} /> : <p role="status">No pending requests for this chat.</p>}
  </div></div>;
}
