'use client';

import React, { useEffect, useState } from 'react';
import type { NativePlanClarification, NativePlanRevision } from '@chirality/runtime-contracts/v3';
import { nativePlanText } from '../../lib/harness/native-plan-text';
import { latestPlanExecution, type PlanExecutionRecord } from '../../lib/harness/plan-executions';
import { turnOutcomeDescription, turnOutcomeLabel } from '../../lib/shell/turn-phase';
import { ChatMarkdown } from './chat-markdown';

/**
 * Everything the Plan tab needs, built by the chat panel (which owns the
 * session's plan state and the composer the actions write into) and rendered
 * by the right sidebar. Handlers are stable so the model changes only when the
 * plan itself does.
 */
export type NativePlanPanelModel = {
  sessionId?: string;
  revisions: readonly NativePlanRevision[];
  clarifications: readonly NativePlanClarification[];
  /** Plan Mode is the current interaction mode. */
  active: boolean;
  refreshing: boolean;
  projectRoot?: string;
  fileCatalog: readonly string[];
  clarificationPendingId?: string | number;
  clarificationError?: string | null;
  exportStatus?: string | null;
  /** Execution attempts recorded for this session's plan revisions (local record; the Runtime keeps the turns). */
  executions?: readonly PlanExecutionRecord[];
  /** Revision whose execution request is prepared in the composer but not yet sent. */
  preparedRevision?: number;
  actionsDisabled: boolean;
  onOpenFile?: (path: string) => void;
  onRefresh: () => void;
  onRevise: (revision: number | undefined) => void;
  onSave: (revision: NativePlanRevision) => void;
  onExecute: (revision: NativePlanRevision) => void;
  onSaveAsWorkflow: (revision: NativePlanRevision) => void;
  onReplyClarification: (clarification: NativePlanClarification, answers: Record<string, { answers: string[] }>) => void;
};

export function NativePlanClarificationCard({ clarification, pending, onReply }: {
  clarification: NativePlanClarification;
  pending: boolean;
  onReply: (clarification: NativePlanClarification, answers: Record<string, { answers: string[] }>) => void;
}): JSX.Element {
  const [values, setValues] = useState<Record<string, string>>({});
  const complete = clarification.questions.every(question => Boolean(values[question.id]?.trim()));
  return <form className="native-plan-clarification" onSubmit={event => {
    event.preventDefault();
    if (!complete || pending) return;
    onReply(clarification, Object.fromEntries(clarification.questions.map(question => [question.id, { answers: [values[question.id]!.trim()] }])));
  }}>
    <p className="native-plan-sidebar-meta">Planning needs your input{clarification.isBlocking ? ' before it can continue' : ''}.</p>
    {clarification.questions.map(question => <fieldset key={question.id}>
      <legend>{question.header}</legend>
      <p>{question.question}</p>
      {question.options.map(option => <label key={option.label}><input type="radio" name={`${String(clarification.requestId)}:${question.id}`} value={option.label}
        checked={values[question.id] === option.label} disabled={pending}
        onChange={() => setValues(current => ({ ...current, [question.id]: option.label }))} />
        <span><strong>{option.label}</strong>{option.description ? <small>{option.description}</small> : null}</span></label>)}
      {question.isOther ? <label className="native-plan-clarification-other"><span>Other answer</span><input type={question.isSecret ? 'password' : 'text'} value={values[question.id] && !question.options.some(option => option.label === values[question.id]) ? values[question.id] : ''}
        disabled={pending} autoComplete="off" onChange={event => setValues(current => ({ ...current, [question.id]: event.target.value }))} /></label> : null}
    </fieldset>)}
    <button type="submit" disabled={!complete || pending}>{pending ? 'Sending answers…' : 'Continue planning'}</button>
  </form>;
}

/**
 * The Plan tab. Shows the current revision, its actions, the earlier
 * revisions, and any clarification Codex is waiting on. `focusRevision`
 * (from a "Plan · Revision N" link in the conversation) opens that revision.
 */
function executionTime(value: string): string {
  const date = new Date(value);
  return Number.isFinite(date.getTime()) ? date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) : '';
}

/**
 * One line per revision: never executed, running (with the attempt number),
 * or how the latest attempt ended. The status belongs to a revision and an
 * attempt, so an executed revision is never shown as awaiting its first run.
 */
export function PlanExecutionStatus({ revision, executions, prepared }: { revision: number; executions: readonly PlanExecutionRecord[]; prepared: boolean }): JSX.Element {
  const latest = latestPlanExecution(executions, revision);
  const attempts = executions.filter(record => record.revision === revision).length;
  const attemptNote = attempts > 1 ? ` · attempt ${latest?.attempt ?? attempts} of ${attempts}` : '';
  let text: string;
  let title: string | undefined;
  if (!latest) {
    text = prepared ? 'Execution request prepared in the composer; send it to run this revision.' : 'Not executed';
  } else if (latest.status === 'running') {
    text = `Running${attemptNote}${latest.startedAt ? ` · started ${executionTime(latest.startedAt)}` : ''}`;
  } else {
    text = `${turnOutcomeLabel(latest.status)}${latest.endedAt ? ` ${executionTime(latest.endedAt)}` : ''}${attemptNote}`;
    title = turnOutcomeDescription(latest.status);
  }
  return <p className="native-plan-execution" data-plan-revision={revision} data-execution-status={latest?.status ?? (prepared ? 'prepared' : 'none')} title={title}>{text}</p>;
}

export function NativePlanPanel({ model, focusRevision }: { model: NativePlanPanelModel | null; focusRevision?: { revision: number; sequence: number } }): JSX.Element {
  const [openRevision, setOpenRevision] = useState<number | null>(null);
  useEffect(() => { setOpenRevision(focusRevision ? focusRevision.revision : null); }, [focusRevision]);
  if (!model) {
    return <section className="native-plan-sidebar native-plan-sidebar--empty" aria-label="Plan">
      <p>No plan in this chat yet. Choose Plan Mode in the conversation to start one.</p>
    </section>;
  }
  const { revisions, clarifications, active, refreshing, clarificationPendingId, clarificationError, exportStatus, projectRoot, fileCatalog, onOpenFile, actionsDisabled, executions = [], preparedRevision } = model;
  const current = revisions.at(-1);
  const focusIsCurrent = current !== undefined && openRevision === current.revision;
  const currentExecuted = current !== undefined && latestPlanExecution(executions, current.revision) !== undefined;
  const currentRunning = current !== undefined && latestPlanExecution(executions, current.revision)?.status === 'running';
  return <section className="native-plan-sidebar" aria-label="Plan">
    <header>
      <div><p className="woven-eyebrow">Plan Mode</p><h2>{current ? `Revision ${current.revision}` : 'Current plan'}</h2></div>
      <button type="button" className="button-muted" disabled={refreshing} onClick={model.onRefresh}>{refreshing ? 'Refreshing…' : 'Refresh'}</button>
    </header>
    {clarifications.length ? <p role="status">Answer the pending questions in the conversation.</p> : null}
    {clarificationError ? <p className="panel-error" role="alert">{clarificationError}</p> : null}
    {!current ? <p>{active ? 'Describe what you want to plan in the conversation. The first revision will appear here.' : 'Switch to Plan Mode to inspect and revise a plan in this conversation.'}</p> : <>
      <p className="native-plan-sidebar-meta">Current plan · read-only</p>
      <PlanExecutionStatus revision={current.revision} executions={executions} prepared={preparedRevision === current.revision} />
      <div className="native-plan-sidebar-body" data-plan-revision={current.revision} data-plan-focused={focusIsCurrent ? 'true' : undefined}><ChatMarkdown source={nativePlanText(current)} projectRoot={projectRoot} fileCatalog={fileCatalog} onOpenFile={onOpenFile} /></div>
      <div className="native-plan-sidebar-actions">
        <button type="button" disabled={actionsDisabled} title="Ask for changes to this plan in the conversation; the result is a new revision." onClick={() => model.onRevise(current.revision)}>Revise in chat</button>
        <button type="button" disabled={actionsDisabled || currentRunning} title={currentExecuted ? 'Prepare a new execution request for this same revision in the composer; you send it.' : 'Prepare the execution request in the composer; you send it.'} onClick={() => model.onExecute(current)}>{currentExecuted ? 'Run again' : 'Execute plan'}</button>
        <button type="button" disabled={actionsDisabled} className="button-muted" onClick={() => model.onSaveAsWorkflow(current)}>Turn into workflow</button>
        <button type="button" className="button-muted" onClick={() => model.onSave(current)}>Save plan…</button>
      </div>
      {exportStatus ? <p role="status" className="native-plan-sidebar-meta">{exportStatus}</p> : null}
      {revisions.length > 1 ? <details className="native-plan-history" open={openRevision !== null && !focusIsCurrent ? true : undefined}><summary>Earlier revisions ({revisions.length - 1})</summary>
        <ol>{revisions.slice(0, -1).reverse().map(revision => <li key={revision.revision}><details open={openRevision === revision.revision ? true : undefined} data-plan-revision={revision.revision}><summary>Revision {revision.revision}</summary><PlanExecutionStatus revision={revision.revision} executions={executions} prepared={preparedRevision === revision.revision} /><div><ChatMarkdown source={nativePlanText(revision)} projectRoot={projectRoot} fileCatalog={fileCatalog} onOpenFile={onOpenFile} /></div><div className="native-plan-sidebar-actions"><button type="button" className="button-muted" disabled={actionsDisabled || latestPlanExecution(executions, revision.revision)?.status === 'running'} title="Prepare an execution request for this earlier revision in the composer; you send it." onClick={() => model.onExecute(revision)}>{latestPlanExecution(executions, revision.revision) ? 'Run again' : 'Execute this revision'}</button><button type="button" className="button-muted" onClick={() => model.onSave(revision)}>Save this revision…</button></div></details></li>)}</ol>
      </details> : null}
    </>}
  </section>;
}
