'use client';

import React, { useEffect, useMemo, useState, useRef, useCallback, useSyncExternalStore } from 'react';
import type { ServerRequestAnswer } from '@chirality/runtime-contracts';
import { answerHarnessSessionRequest, listHarnessSessionRequests } from '../../lib/harness/client';
import {
  readElicitationMessage,
  readUserInputQuestions,
  selectPendingServerRequests,
  deriveServerRequests,
  derivePermissionRequests,
  classifyServerRequestMethod,
  type ServerRequestRow,
  type UserInputQuestion
} from '../../lib/shell/harness-event-views';
import { record } from '../../lib/shell/native-progress';
import { useHarnessEvents } from '../workspace/harness-events-provider';

type RequestCardProps = {
  row: ServerRequestRow;
  pending: boolean;
  onAnswer: (row: ServerRequestRow, answer: ServerRequestAnswer) => void;
};

function methodLabel(row: ServerRequestRow): string {
  if (row.kind === 'approval') return row.status === 'pending' ? 'Approval required' : 'Approval request';
  if (row.kind === 'userInput') return row.status === 'pending' ? 'Codex needs your input' : 'Codex input request';
  if (row.kind === 'elicitation') return row.status === 'pending' ? 'A tool server asks for confirmation' : 'Tool server confirmation';
  return row.method;
}

function supportsSessionApproval(row: ServerRequestRow): boolean {
  if (row.method === 'item/permissions/requestApproval') return true;
  if (!['item/commandExecution/requestApproval', 'item/fileChange/requestApproval'].includes(row.method)) return false;
  const decisions = record(row.request).availableDecisions;
  return Array.isArray(decisions) && decisions.includes('acceptForSession');
}

const questionDrafts = new Map<string, Record<string, string>>();
const questionDraftKey = (row: ServerRequestRow) => `${row.sessionId}:${row.requestId}:${row.timestamp}`;

function UserInputForm({ row, pending, onAnswer }: RequestCardProps): JSX.Element {
  const questions = useMemo(() => readUserInputQuestions(row.request), [row.request]);
  const [values, setValues] = useState<Record<string, string>>(() => questionDrafts.get(questionDraftKey(row)) ?? {});
  useEffect(() => {
    questionDrafts.set(questionDraftKey(row), Object.fromEntries(Object.entries(values).filter(([id]) => !questions.find(question => question.id === id)?.isSecret)));
    if (questionDrafts.size > 100) questionDrafts.delete(questionDrafts.keys().next().value!);
  }, [row.sessionId, row.requestId, row.timestamp, values, questions]);
  const complete = questions.length > 0 && questions.every((question) => Boolean(values[question.id]?.trim()));
  const answerFor = (question: UserInputQuestion): string => values[question.id]?.trim() ?? '';
  return (
    <form
      className="native-plan-clarification"
      onSubmit={(event) => {
        event.preventDefault();
        if (!complete || pending) return;
        onAnswer(row, {
          kind: 'userInput',
          answers: Object.fromEntries(questions.map((question) => [question.id, { answers: [answerFor(question)] }]))
        });
      }}
    >
      {questions.length === 0 ? <p>This request carries no questions. Inspect it in the Activity panel.</p> : null}
      {questions.map((question) => (
        <fieldset key={question.id}>
          <legend>{question.header}</legend>
          {question.question ? <p>{question.question}</p> : null}
          {question.options.map((option) => (
            <label key={option.label}>
              <input
                type="radio"
                name={`${row.requestId}:${question.id}`}
                value={option.label}
                checked={values[question.id] === option.label}
                disabled={pending}
                onChange={() => setValues((current) => ({ ...current, [question.id]: option.label }))}
              />
              <span>
                <strong>{option.label}</strong>
                {option.description ? <small>{option.description}</small> : null}
              </span>
            </label>
          ))}
          {question.isOther || question.options.length === 0 ? (
            <label className="native-plan-clarification-other">
              <span>{question.options.length === 0 ? 'Your answer' : 'Other answer'}</span>
              <input
                type={question.isSecret ? 'password' : 'text'}
                value={values[question.id] && !question.options.some((option) => option.label === values[question.id]) ? values[question.id] : ''}
                disabled={pending}
                autoComplete="off"
                onChange={(event) => setValues((current) => ({ ...current, [question.id]: event.target.value }))}
              />
            </label>
          ) : null}
        </fieldset>
      ))}
      <button type="submit" disabled={!complete || pending}>{pending ? 'Sending answers...' : 'Send answers'}</button>
    </form>
  );
}

function ElicitationForm({ row, pending, onAnswer }: RequestCardProps): JSX.Element {
  const message = readElicitationMessage(row.request);
  return (
    <div className="native-plan-clarification">
      {message ? <p>{message}</p> : <p>The tool server asked for confirmation without a message.</p>}
      <details>
        <summary>Request details</summary>
        <pre className="transcript-text">{JSON.stringify(row.request ?? null, null, 2)}</pre>
      </details>
      <div className="permission-card-actions">
        <button type="button" className="permission-card-approve" disabled={pending} onClick={() => onAnswer(row, { kind: 'elicitation', action: 'accept' })}>
          {pending ? 'Sending...' : 'Accept'}
        </button>
        <button type="button" className="button-muted permission-card-deny" disabled={pending} onClick={() => onAnswer(row, { kind: 'elicitation', action: 'decline' })}>
          Decline
        </button>
      </div>
    </div>
  );
}

/** One answerable Codex server request (user-input questions or an MCP elicitation). */
export function RequestCard({ row, pending, onAnswer }: RequestCardProps): JSX.Element {
  return (
    <article className="permission-card request-card" role="group" aria-label={`Request: ${methodLabel(row)}`}>
      <header className="permission-card-header">
        <span className="permission-card-tool" title={row.method}>{methodLabel(row)}</span>
        <span className="permission-card-badge">answer required</span>
      </header>
      {row.kind === 'approval' ? <div><p>{String(record(row.request).reason ?? record(row.request).command ?? 'Codex requests permission to continue.')}</p><details><summary>Request details</summary><pre className="transcript-text">{JSON.stringify(row.request, null, 2)}</pre></details><div className="permission-card-actions"><button disabled={pending} onClick={() => onAnswer(row, { kind: 'approval', verdict: 'allow' })}>Approve</button>{supportsSessionApproval(row) ? <button disabled={pending} onClick={() => onAnswer(row, { kind: 'approval', verdict: 'allowForSession' })}>Allow for this session</button> : null}<button disabled={pending} onClick={() => onAnswer(row, { kind: 'approval', verdict: 'deny' })}>Deny</button></div></div> : row.kind === 'userInput'
        ? <UserInputForm row={row} pending={pending} onAnswer={onAnswer} />
        : <ElicitationForm row={row} pending={pending} onAnswer={onAnswer} />}
    </article>
  );
}

type RequestCardsProps = {
  sessionId: string | null;
  requests: ServerRequestRow[];
  /** Request ids already presented elsewhere (the Plan Mode clarification card); hidden here. */
  suppressedRequestIds?: ReadonlySet<string>;
  answer?: typeof answerHarnessSessionRequest;
};

/**
 * Presentational list over already-derived pending requests, answering through
 * the session request route. The follow-up `codex.request.resolved` event
 * removes a card from the stream; a failed post keeps the card and shows why.
 */
export function RequestCards({ sessionId, requests, suppressedRequestIds, answer = answerHarnessSessionRequest }: RequestCardsProps): JSX.Element | null {
  const [pending, setPending] = useState<Record<string, true>>({});
  const [error, setError] = useState<string | null>(null);
  const currentSession = useRef(sessionId);
  currentSession.current = sessionId;
  const visible = requests.filter((row) => !suppressedRequestIds?.has(row.requestId));
  const keys = visible.map((row) => row.key).join('|');

  useEffect(() => {
    const live = new Set(keys ? keys.split('|') : []);
    setPending((current) => {
      const next: Record<string, true> = {};
      let changed = false;
      for (const key of Object.keys(current)) {
        if (live.has(key)) next[key] = true;
        else changed = true;
      }
      return changed ? next : current;
    });
    if (live.size === 0) setError(null);
  }, [keys]);

  async function submit(row: ServerRequestRow, value: ServerRequestAnswer): Promise<void> {
    const targetSessionId = row.sessionId || sessionId;
    if (!targetSessionId) return;
    setPending((current) => ({ ...current, [row.key]: true }));
    setError(null);
    try {
      if (answer === answerHarnessSessionRequest) {
        const live = await listHarnessSessionRequests(targetSessionId);
        if (!live.requests.some(request => request.requestId === row.requestId && request.method === row.method)) throw new Error('This request is no longer pending.');
      }
      await answer({ sessionId: targetSessionId, requestId: row.requestId, answer: value });
      questionDrafts.delete(questionDraftKey(row));
    } catch (caught) {
      if (currentSession.current !== targetSessionId) return;
      setError(caught instanceof Error ? caught.message : 'Unable to send the answer.');
      setPending((current) => {
        const next = { ...current };
        delete next[row.key];
        return next;
      });
    }
  }

  if (visible.length === 0) return null;
  return (
    <section className="permission-card-list" role="region" aria-label="Pending requests" aria-live="polite">
      {visible.map((row) => (
        <RequestCard key={row.key} row={row} pending={Boolean(pending[row.key])} onAnswer={(target, value) => { void submit(target, value); }} />
      ))}
      {error ? <p className="permission-card-error">{error}</p> : null}
    </section>
  );
}

/** Live wrapper over the bridged event stream; `active` comes from the Runtime turn state. */
export function ServerRequests({ sessionId, active, suppressedRequestIds }: {
  sessionId: string | null;
  active: boolean;
  suppressedRequestIds?: ReadonlySet<string>;
}): JSX.Element | null {
  const { events } = useHarnessEvents();
  const pending = useMemo(() => selectPendingServerRequests(events, active), [events, active]);
  return <RequestCards sessionId={sessionId} requests={pending} suppressedRequestIds={suppressedRequestIds} />;
}

/** Authorized live request listing is the actionability boundary; history alone never enables a card. */
const EMPTY_REQUESTS: ServerRequestRow[] = [];
type RequestSubscription = { rows: ServerRequestRow[]; listeners: Set<() => void>; stop: () => void };
const requestSubscriptions = new Map<string, RequestSubscription>();

function subscribeRequests(sessionId: string, listener: () => void): () => void {
  let subscription = requestSubscriptions.get(sessionId);
  if (!subscription) {
    const controller = new AbortController();
    const entry: RequestSubscription = { rows: EMPTY_REQUESTS, listeners: new Set(), stop: () => {} };
    requestSubscriptions.set(sessionId, entry);
    let pending = false;
    const publish = (rows: ServerRequestRow[]) => {
      if (controller.signal.aborted || JSON.stringify(rows) === JSON.stringify(entry.rows)) return;
      entry.rows = rows;
      for (const notify of entry.listeners) notify();
    };
    const refresh = async () => {
      if (pending) return;
      pending = true;
      try {
        const result = await listHarnessSessionRequests(sessionId, controller.signal);
        publish(result.requests.map(request => ({
          key: `${sessionId}:${request.requestId}`, sessionId, requestId: request.requestId, method: request.method,
          kind: classifyServerRequestMethod(request.method),
          request: request.params, status: 'pending' as const, timestamp: request.receivedAt
        })).filter(row => ['approval', 'userInput', 'elicitation'].includes(row.kind)));
      } catch { publish(EMPTY_REQUESTS); }
      finally { pending = false; }
    };
    const timer = window.setInterval(() => void refresh(), 2000);
    window.addEventListener?.('focus', refresh);
    entry.stop = () => { controller.abort(); window.clearInterval(timer); window.removeEventListener?.('focus', refresh); };
    subscription = entry;
    void refresh();
  }
  subscription.listeners.add(listener);
  return () => {
    subscription.listeners.delete(listener);
    if (!subscription.listeners.size) { subscription.stop(); requestSubscriptions.delete(sessionId); }
  };
}

/** Multiple attention/inline subscribers share one authorized listing for a session. */
export function useLiveSessionRequests(sessionId: string | null, active = true): ServerRequestRow[] {
  const subscribe = useCallback((listener: () => void) => sessionId && active ? subscribeRequests(sessionId, listener) : () => {}, [sessionId, active]);
  const snapshot = useCallback(() => sessionId && active ? requestSubscriptions.get(sessionId)?.rows ?? EMPTY_REQUESTS : EMPTY_REQUESTS, [sessionId, active]);
  return useSyncExternalStore(subscribe, snapshot, () => EMPTY_REQUESTS);
}

export function LiveSessionRequests({ sessionId, active = true, showHistory = true }: { sessionId: string | null; active?: boolean; showHistory?: boolean }): JSX.Element {
  const rows = useLiveSessionRequests(sessionId, active);
  const { events } = useHarnessEvents();
  const retained = useRef<{ sessionId: string | null; events: Map<string, (typeof events)[number]> }>({ sessionId, events: new Map() });
  if (retained.current.sessionId !== sessionId) retained.current = { sessionId, events: new Map() };
  for (const event of events) if (event.sessionId === sessionId && (event.type === 'codex.request' || event.type === 'codex.request.resolved' || event.type === 'tool.permission')) retained.current.events.set(event.eventId, event);
  const historyEvents = [...retained.current.events.values()];
  const history = deriveServerRequests(historyEvents);
  const approvals = derivePermissionRequests(historyEvents).filter(row => row.requestId && row.status !== 'pending');
  return <div id={sessionId ? `requests-${sessionId}` : undefined}>
    <RequestCards sessionId={sessionId} requests={rows} />
    {showHistory ? approvals.map(row => <details key={`approval:${row.key}`} className="request-card"><summary>{row.toolName} · {row.status}</summary><p>{row.reason}</p></details>) : null}
    {showHistory ? history.filter(row => row.status !== 'pending').map(row => <details key={row.key} className="request-card"><summary>{methodLabel(row)} · {row.status}</summary>
      {readUserInputQuestions(row.request).map(question => <p key={question.id}>{question.question}</p>)}
      {row.decision !== undefined && !readUserInputQuestions(row.request).some(question => question.isSecret) ? <pre className="transcript-text">{JSON.stringify(row.decision, null, 2)}</pre> : null}
    </details>) : null}
  </div>;
}
