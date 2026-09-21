'use client';

import React, { useEffect, useMemo, useRef, useState } from 'react';
import {
  inspectMethod,
  listMethods,
  qualifiedMethodId,
  type MethodDescriptor,
  type QualifiedMethodReference
} from '../../lib/harness/method-selection-client';
import type { MethodInspectionResponse } from '@chirality/runtime-contracts/v3';
import { groupWorkflowLibrary, methodMatchesQuery, workflowDisplayName } from '../../lib/shell/workflow-library';
import { WorkflowDraftReview } from './workflow-draft-review';
import type { WorkflowFeedbackRequest } from '../../lib/harness/workflow-feedback';
import { useRuntimeEpoch } from '../shell/runtime-connectivity-provider';

export type LibraryView = 'workflows' | 'skills';

function sameMethod(left: QualifiedMethodReference, right: QualifiedMethodReference): boolean {
  return left.kind === right.kind && left.name === right.name && left.source === right.source && left.sourceRootId === right.sourceRootId;
}

function metadataText(method: MethodDescriptor, ...keys: string[]): string | undefined {
  for (const key of keys) {
    const value = method.metadata?.[key];
    if (typeof value === 'string' && value.trim()) return value.trim();
    if (Array.isArray(value)) {
      const items = value.filter((item): item is string => typeof item === 'string' && Boolean(item.trim()));
      if (items.length) return items.join(', ');
    }
  }
  return undefined;
}

function sourceLabel(method: MethodDescriptor): string {
  if (method.source === 'project') return 'This project';
  if (method.source === 'user') return 'Your library';
  return 'Chirality library';
}

function MethodCard({ method, active, inspectionPending, onInspect, onToggle }: {
  method: MethodDescriptor;
  active: boolean;
  inspectionPending: boolean;
  onInspect: () => void;
  onToggle?: () => void;
}): JSX.Element {
  const purpose = metadataText(method, 'purpose', 'useWhen', 'use_when');
  const applicability = metadataText(method, 'applicability', 'appliesTo', 'applies_to');
  const displayName = workflowDisplayName(method);
  const superseded = method.navigation?.category === 'superseded';
  return <li className={method.central ? 'method-card method-card--central' : 'method-card'} data-method-source={method.source} data-method-kind={method.kind}>
    <div className="method-card-heading"><strong>{displayName}</strong>{displayName !== method.name ? <code className="method-card-identifier" title="Workflow identifier">{method.name}</code> : null}</div>
    <p>{purpose ?? method.description}</p>
    {applicability ? <p className="method-applicability"><strong>Useful for:</strong> {applicability}</p> : null}
    {superseded ? <p className="method-card-meta method-card-superseded">Superseded{method.navigation?.supersededBy ? <> · replaced by <code>{method.navigation.supersededBy}</code></> : null}</p> : null}
    <p className="method-card-meta"><small>{sourceLabel(method)}</small></p>
    <div className="method-card-actions">
      <button type="button" disabled={inspectionPending} onClick={onInspect}>{inspectionPending ? 'Opening…' : 'Inspect'}</button>
      {onToggle ? <button type="button" aria-pressed={active} onClick={onToggle}>{active ? 'Remove' : 'Use in message'}</button> : <small>Read-only reference</small>}
    </div>
  </li>;
}

function groupId(label: string): string {
  return `method-group-${label.replace(/\W+/g, '-').toLowerCase()}`;
}

export function MethodLibraryView({ projectRoot, selected, onSelectedChange, refresh = 0, onWorkflowFeedback, feedbackDisabled = false }: {
  projectRoot: string;
  selected: readonly QualifiedMethodReference[];
  onSelectedChange: (methods: QualifiedMethodReference[]) => void;
  refresh?: number;
  view?: LibraryView;
  onWorkflowFeedback?: (request: Omit<WorkflowFeedbackRequest, 'sequence'>) => void;
  feedbackDisabled?: boolean;
}): JSX.Element {
  const [registrationRefresh, setRegistrationRefresh] = useState(0);
  const inspectionRef = useRef<HTMLElement>(null);
  const [query, setQuery] = useState('');
  const [methods, setMethods] = useState<MethodDescriptor[]>([]);
  const [inspection, setInspection] = useState<MethodInspectionResponse | null>(null);
  const [inspectionPendingId, setInspectionPendingId] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const inspectionGeneration = useRef(0);
  const runtimeEpoch = useRuntimeEpoch();
  const catalogScope = useRef<{ projectRoot: string; query: string } | null>(null);

  useEffect(() => {
    const controller = new AbortController();
    const scopeChanged = catalogScope.current?.projectRoot !== projectRoot || catalogScope.current?.query !== query;
    catalogScope.current = { projectRoot, query };
    if (scopeChanged) {
      inspectionGeneration.current += 1;
      setInspection(null); setInspectionPendingId(null); setMethods([]); setLoading(true);
    }
    setError(null);
    const timer = setTimeout(() => {
      void listMethods(projectRoot, query, controller.signal)
        .then(result => { if (!controller.signal.aborted) setMethods([...result.methods]); })
        .catch(reason => { if (!controller.signal.aborted) setError(reason instanceof Error ? reason.message : 'The method catalog is unavailable.'); })
        .finally(() => { if (!controller.signal.aborted) setLoading(false); });
    }, query ? 150 : 0);
    return () => { clearTimeout(timer); controller.abort(); };
  }, [projectRoot, query, refresh, runtimeEpoch, registrationRefresh]);

  useEffect(() => {
    if (inspection) { inspectionRef.current?.focus(); inspectionRef.current?.scrollIntoView?.({ block: 'start' }); }
  }, [inspection]);

  const visible = useMemo(() => methods.filter(method => method.kind === 'workflow' && methodMatchesQuery(method, query)), [methods, query]);
  const library = useMemo(() => groupWorkflowLibrary(visible), [visible]);

  const openInspection = (method: MethodDescriptor): void => {
    const generation = inspectionGeneration.current + 1;
    inspectionGeneration.current = generation;
    const id = qualifiedMethodId(method);
    setError(null); setInspection(null); setInspectionPendingId(id);
    void inspectMethod(projectRoot, method)
      .then(result => { if (inspectionGeneration.current === generation) setInspection(result); })
      .catch(reason => { if (inspectionGeneration.current === generation) setError(reason instanceof Error ? reason.message : 'Method details are unavailable.'); })
      .finally(() => { if (inspectionGeneration.current === generation) setInspectionPendingId(null); });
  };

  const card = (method: MethodDescriptor): JSX.Element => {
    const active = selected.some(item => sameMethod(item, method));
    const selectable = method.kind === 'workflow';
    return <MethodCard key={qualifiedMethodId(method)} method={method} active={active}
      inspectionPending={inspectionPendingId === qualifiedMethodId(method)} onInspect={() => openInspection(method)}
      onToggle={selectable ? () => onSelectedChange(active
        ? selected.filter(item => !sameMethod(item, method))
        : [...selected, { kind: method.kind, name: method.name, source: method.source, sourceRootId: method.sourceRootId }]) : undefined} />;
  };
  const section = (label: string, entries: readonly MethodDescriptor[], extra?: React.ReactNode, note?: string): JSX.Element | null => entries.length === 0 && !extra ? null
    : <section className="method-library-group" key={label} aria-labelledby={groupId(label)}>
      <h3 id={groupId(label)}>{label}</h3>
      {note ? <p className="method-library-note">{note}</p> : null}
      {entries.length ? <ul className="method-library-list">{entries.map(card)}</ul> : null}
      {extra}
    </section>;

  const searchLabel = 'Search workflows';
  const empty = !loading && !error && visible.length === 0;
  return <section className="method-library" aria-label="Workflows" data-library-view="workflows">
    <input type="search" className="method-library-search" value={query} onChange={event => setQuery(event.target.value)} placeholder={searchLabel} aria-label={searchLabel} title={searchLabel} />
    {loading ? <p role="status">Loading…</p> : null}
    {error ? <p role="alert">{error}</p> : null}
    {empty ? <p>{query ? 'No matches.' : 'No workflows are available.'}</p> : null}
    {!inspection ? <WorkflowDraftReview projectRoot={projectRoot} refresh={refresh + registrationRefresh} onRegistered={() => setRegistrationRefresh(value => value + 1)} onFeedback={onWorkflowFeedback} feedbackDisabled={feedbackDisabled} /> : null}
    {!loading && !inspection ? <>
      {section('Core', library.core)}
      {library.specialist.length ? <section className="method-library-group" aria-labelledby={groupId('Specialist')}>
        <h3 id={groupId('Specialist')}>Specialist</h3>
        {library.specialist.map(group => <details className="method-library-subgroup" key={group.key} open={query ? true : undefined} data-method-category={group.key}>
          <summary><h4 id={groupId(`specialist-${group.key}`)}>{group.label}</h4><span className="method-library-count">{group.primary.length + group.supporting.length}</span></summary>
          {group.primary.length ? <ul className="method-library-list">{group.primary.map(card)}</ul> : null}
          {group.supporting.length ? <details className="method-library-supporting"><summary>Supporting steps ({group.supporting.length})</summary><ul className="method-library-list">{group.supporting.map(card)}</ul></details> : null}
        </details>)}
      </section> : null}
      {section('Project Specific', library.projectSpecific, undefined, library.projectSpecific.length ? undefined : 'Workflows saved in this project appear here, including plans saved as workflows.')}
      {section('Your workflows', library.personal)}
      {section('Other bundled workflows', library.unplaced)}
      {library.superseded.length ? <details className="method-library-superseded"><summary>Superseded ({library.superseded.length})</summary><ul className="method-library-list">{library.superseded.map(card)}</ul></details> : null}
    </> : null}
    {inspection ? <article ref={inspectionRef} tabIndex={-1} className="method-inspection method-inspection--focused" aria-label={`${inspection.method.name} method details`}>
      <button type="button" onClick={() => setInspection(null)}>‹ Workflows</button>
      <h3>{workflowDisplayName(inspection.method)}</h3>
      <p>{inspection.method.description}</p>
      <details><summary>Technical details</summary><dl><dt>Identifier</dt><dd><code>{inspection.method.name}</code></dd>
        <dt>Source</dt><dd>{sourceLabel(inspection.method)} · {inspection.method.sourceRootId}</dd>
        <dt>Kind</dt><dd>{inspection.method.kind}</dd>
        <dt>Compatibility</dt><dd>{inspection.method.compatibility}</dd>
        <dt>Eligible roles</dt><dd>{inspection.method.executionRoleIds.join(', ') || 'None recorded'}</dd></dl></details>
      <details open><summary>Read instructions</summary><pre>{inspection.entrypoint.content}</pre><small>SHA-256 {inspection.entrypoint.sha256}</small></details>
      {inspection.resources.length ? <details><summary>Included resources</summary><ul>{inspection.resources.map(resource => <li key={resource.path}>{resource.path} · {resource.sha256}</li>)}</ul></details> : null}
    </article> : null}
  </section>;
}
