'use client';

import React, { useEffect, useRef, useState } from 'react';
import { listWorkflowDrafts, registerWorkflowDraft, type WorkflowDraft } from '../../lib/harness/workflow-drafts';
import type { WorkflowFeedbackRequest } from '../../lib/harness/workflow-feedback';
import { useRuntimeEpoch } from '../shell/runtime-connectivity-provider';
import { ChatMarkdown } from '../shell/chat-markdown';

export function WorkflowDraftReview({ projectRoot, refresh, onRegistered, onFeedback, feedbackDisabled = false }: {
  projectRoot: string;
  refresh: number;
  onRegistered: () => void;
  onFeedback?: (request: Omit<WorkflowFeedbackRequest, 'sequence'>) => void;
  feedbackDisabled?: boolean;
}): JSX.Element | null {
  const [drafts, setDrafts] = useState<WorkflowDraft[]>([]);
  const [review, setReview] = useState<{ root: string; draft: WorkflowDraft } | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [notice, setNotice] = useState<string | null>(null);
  const [pending, setPending] = useState(false);
  const scope = useRef(0);
  const panel = useRef<HTMLElement>(null);
  const epoch = useRuntimeEpoch();
  useEffect(() => {
    scope.current++;
    setDrafts([]); setReview(null); setError(null); setNotice(null); setPending(false);
  }, [projectRoot]);
  useEffect(() => {
    const controller = new AbortController();
    void listWorkflowDrafts(projectRoot, controller.signal).then(result => {
      if (!controller.signal.aborted) { setDrafts(result.drafts.filter(draft => !draft.registered)); setError(null); }
    }).catch(reason => {
      if (!controller.signal.aborted) setError(reason instanceof Error ? reason.message : 'Workflow drafts are unavailable.');
    });
    return () => controller.abort();
  }, [projectRoot, refresh, epoch]);
  useEffect(() => {
    if (review) { panel.current?.focus(); panel.current?.scrollIntoView?.({ block: 'start' }); }
  }, [review]);
  const current = review?.root === projectRoot ? review.draft : null;
  const latest = current ? drafts.find(item => item.name === current.name && item.source === current.source) : undefined;
  const stale = current !== null && (!latest || latest.reviewToken !== current.reviewToken);
  async function register(): Promise<void> {
    if (!current || pending || stale || current.destinationExists) return;
    const generation = scope.current;
    setPending(true); setError(null); setNotice(null);
    try {
      await registerWorkflowDraft({ projectRoot, name: current.name, source: current.source, reviewToken: current.reviewToken });
      if (generation !== scope.current) return;
      setReview(null); setDrafts(items => items.filter(item => item.name !== current.name || item.source !== current.source));
      setNotice(`${current.name} registered.`); onRegistered();
    } catch (reason) {
      if (generation === scope.current) setError(reason instanceof Error ? reason.message : 'The workflow could not be registered.');
    } finally { if (generation === scope.current) setPending(false); }
  }
  if (!drafts.length && !current && !error && !notice) return null;
  return <section className="workflow-draft-review" aria-label="Workflow drafts">
    {error ? <p role="alert">{error}</p> : null}
    {notice ? <p role="status">{notice}</p> : null}
    {current ? <article ref={panel} tabIndex={-1} aria-label={`Review ${current.name}`}>
      <button type="button" disabled={pending} onClick={() => setReview(null)}>‹ Drafts</button>
      <h3>{current.name}</h3>
      <p>{current.description}</p>
      <p className="method-card-meta">{current.source === 'project' ? 'This project' : 'Your library'} · Draft</p>
      <div className="workflow-draft-content"><ChatMarkdown source={current.content} /></div>
      <details><summary>Included files ({current.files.length})</summary><ul>{current.files.map(file => <li key={file.path}>
        <span>{file.path} · {file.size} bytes{file.mode ? ` · permissions ${file.mode}` : ''}</span>
        {'content' in file && typeof file.content === 'string' && file.path !== 'WORKFLOW.md' ? <details><summary>Read file</summary><pre>{file.content}</pre></details> : null}
      </li>)}</ul></details>
      {current.destinationExists ? <p role="status">A workflow with this name is already registered. Request a distinct name to preserve the existing workflow.</p> : null}
      {stale ? <p role="status">This draft has changed. Open its latest version before registering.{latest ? <button type="button" disabled={pending} onClick={() => setReview({ root: projectRoot, draft: latest })}>Review latest draft</button> : null}</p> : null}
      <div className="method-card-actions">
        {onFeedback ? <button type="button" disabled={pending || feedbackDisabled} onClick={() => onFeedback({ projectRoot, name: current.name, source: current.source })}>Request changes in chat</button> : null}
        <button type="button" disabled={pending || stale || current.destinationExists} onClick={() => { void register(); }}>{pending ? 'Registering…' : 'Register workflow'}</button>
      </div>
    </article> : drafts.length ? <>
      <h3>Ready for review</h3>
      <ul className="method-library-list">{drafts.map(draft => <li key={`${draft.source}:${draft.name}`}>
        <strong>{draft.name}</strong><p>{draft.description}</p>
        <p className="method-card-meta">{draft.source === 'project' ? 'This project' : 'Your library'}</p>
        <button type="button" onClick={() => { setReview({ root: projectRoot, draft }); setNotice(null); }}>Review draft</button>
      </li>)}</ul>
    </> : null}
  </section>;
}
