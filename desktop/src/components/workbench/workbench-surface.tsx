'use client';

import { useSearchParams } from 'next/navigation';
import React from 'react';
import { useEffect, useMemo, useState, type FormEvent } from 'react';
import { DocumentView } from '../shell/document-view';
import { useWorkspace } from '../workspace/workspace-provider';
import {
  canAgentTransitionLifecycle,
  currentIsoDate,
  fetchDeliverableDependencies,
  fetchDeliverableStatus,
  isExecutionBlockerSubsetRow,
  nextLifecycleTargets,
  requiresApprovalShaForTarget,
  summarizeDependencyRows,
  transitionDeliverableStatus,
  workspaceApiErrorMessage,
  type DeliverableDependenciesSnapshot,
  type DeliverableStatusSnapshot
} from '../../lib/workspace/deliverable-api';

type ScopeItem = {
  id: string;
  label: string;
  path: string;
};

type ScopeResponse = {
  deliverables: ScopeItem[];
  knowledgeTypes: ScopeItem[];
  hasKnowledgeDecomposition: boolean;
  truncated: boolean;
  scannedAt: string;
};

type Option = {
  value: string;
  label: string;
};

type WorkbenchLifecycleTransitionFormProps = {
  availableTransitionTargets: readonly string[];
  canSubmitTransition: boolean;
  requiresApprovalSha: boolean;
  transitionActor: string;
  transitionApprovalSha: string;
  transitionDate: string;
  transitionError: string | null;
  transitionSubmitting: boolean;
  transitionTarget: string;
  onActorChange: (value: string) => void;
  onApprovalShaChange: (value: string) => void;
  onDateChange: (value: string) => void;
  onSubmit: (event: FormEvent<HTMLFormElement>) => void;
  onTargetChange: (value: string) => void;
};

const TRANSITION_ACTOR_OPTIONS: Option[] = [
  { value: 'WORKING_ITEMS', label: 'WORKING_ITEMS' },
  { value: 'HUMAN', label: 'HUMAN' },
  { value: 'CHIRALITY_FRAMEWORK', label: 'CHIRALITY_FRAMEWORK' },
  { value: '4_DOCUMENTS', label: '4_DOCUMENTS' }
];

function normalizeAgent(rawValue: string | null): string {
  if (!rawValue) {
    return 'WORKING_ITEMS';
  }

  return rawValue.trim() || 'WORKING_ITEMS';
}

export function WorkbenchLifecycleTransitionForm({
  availableTransitionTargets,
  canSubmitTransition,
  requiresApprovalSha,
  transitionActor,
  transitionApprovalSha,
  transitionDate,
  transitionError,
  transitionSubmitting,
  transitionTarget,
  onActorChange,
  onApprovalShaChange,
  onDateChange,
  onSubmit,
  onTargetChange
}: WorkbenchLifecycleTransitionFormProps): JSX.Element {
  return (
    <form
      className="pipeline-transition-form"
      onSubmit={(event) => {
        onSubmit(event);
      }}
    >
      <h4>Lifecycle Transition</h4>
      <div className="pipeline-transition-grid">
        <label>
          Target state
          <select
            value={transitionTarget}
            onChange={(event) => {
              onTargetChange(event.target.value);
            }}
            disabled={availableTransitionTargets.length === 0}
          >
            {availableTransitionTargets.length === 0 ? (
              <option value="">No forward transition available</option>
            ) : null}
            {availableTransitionTargets.map((state) => (
              <option key={state} value={state}>
                {state}
              </option>
            ))}
          </select>
        </label>

        <label>
          Actor
          <select
            value={transitionActor}
            onChange={(event) => {
              onActorChange(event.target.value);
            }}
          >
            {TRANSITION_ACTOR_OPTIONS.map((option) => (
              <option
                key={option.value}
                value={option.value}
                disabled={requiresApprovalSha && option.value !== 'HUMAN'}
              >
                {option.label}
              </option>
            ))}
          </select>
        </label>

        <label>
          Transition date
          <input
            type="date"
            value={transitionDate}
            onChange={(event) => {
              onDateChange(event.target.value);
            }}
          />
        </label>

        <label>
          {requiresApprovalSha ? 'Approval SHA (required)' : 'Approval SHA (optional)'}
          <input
            value={transitionApprovalSha}
            onChange={(event) => {
              onApprovalShaChange(event.target.value);
            }}
            placeholder={requiresApprovalSha ? 'e.g. abcd1234' : 'Optional (required at CHECKING/ISSUED)'}
          />
        </label>
      </div>

      {transitionError ? <p className="panel-error">{transitionError}</p> : null}

      <div className="pipeline-transition-actions">
        <button type="submit" disabled={!canSubmitTransition}>
          {transitionSubmitting ? 'Applying Transition...' : 'Apply Transition'}
        </button>
      </div>
    </form>
  );
}

export function WorkbenchSurface(): JSX.Element {
  const { projectRoot } = useWorkspace();
  const searchParams = useSearchParams();
  const agent = normalizeAgent(searchParams.get('agent'));
  const row = searchParams.get('row') ?? 'NORMATIVE';
  const column = searchParams.get('column') ?? 'GUIDING';
  const [scopeLoading, setScopeLoading] = useState(false);
  const [scopeError, setScopeError] = useState<string | null>(null);
  const [scopeData, setScopeData] = useState<ScopeResponse | null>(null);
  const [selectedDeliverablePath, setSelectedDeliverablePath] = useState('');
  const [contractsLoading, setContractsLoading] = useState(false);
  const [contractsError, setContractsError] = useState<string | null>(null);
  const [contractsRefreshToken, setContractsRefreshToken] = useState(0);
  const [statusSnapshot, setStatusSnapshot] = useState<DeliverableStatusSnapshot | null>(null);
  const [dependenciesSnapshot, setDependenciesSnapshot] =
    useState<DeliverableDependenciesSnapshot | null>(null);
  const [transitionTarget, setTransitionTarget] = useState('');
  const [transitionActor, setTransitionActor] = useState('WORKING_ITEMS');
  const [transitionDate, setTransitionDate] = useState(currentIsoDate);
  const [transitionApprovalSha, setTransitionApprovalSha] = useState('');
  const [transitionError, setTransitionError] = useState<string | null>(null);
  const [transitionSubmitting, setTransitionSubmitting] = useState(false);

  useEffect(() => {
    let cancelled = false;

    async function loadScopeData(): Promise<void> {
      if (!projectRoot) {
        setScopeData(null);
        setScopeError(null);
        setSelectedDeliverablePath('');
        return;
      }

      setScopeLoading(true);
      setScopeError(null);

      try {
        const response = await fetch(
          `/api/working-root/scope?projectRoot=${encodeURIComponent(projectRoot)}`
        );
        const payload = (await response.json()) as ScopeResponse & {
          error?: { message?: string };
        };

        if (!response.ok || !payload) {
          throw new Error(payload.error?.message ?? 'Unable to scan deliverable scopes');
        }

        if (!cancelled) {
          setScopeData(payload);
          setSelectedDeliverablePath(payload.deliverables[0]?.path ?? '');
        }
      } catch (error) {
        if (!cancelled) {
          const message = error instanceof Error ? error.message : 'Unable to scan deliverable scopes';
          setScopeError(message);
          setScopeData(null);
          setSelectedDeliverablePath('');
        }
      } finally {
        if (!cancelled) {
          setScopeLoading(false);
        }
      }
    }

    void loadScopeData();

    return () => {
      cancelled = true;
    };
  }, [projectRoot]);

  useEffect(() => {
    let cancelled = false;

    async function loadContracts(): Promise<void> {
      if (!projectRoot || !selectedDeliverablePath) {
        setContractsError(null);
        setStatusSnapshot(null);
        setDependenciesSnapshot(null);
        return;
      }

      setContractsLoading(true);
      setContractsError(null);

      try {
        const [status, dependencies] = await Promise.all([
          fetchDeliverableStatus(projectRoot, selectedDeliverablePath),
          fetchDeliverableDependencies(projectRoot, selectedDeliverablePath)
        ]);

        if (!cancelled) {
          setStatusSnapshot(status);
          setDependenciesSnapshot(dependencies);
        }
      } catch (error) {
        if (!cancelled) {
          setContractsError(workspaceApiErrorMessage(error));
          setStatusSnapshot(null);
          setDependenciesSnapshot(null);
        }
      } finally {
        if (!cancelled) {
          setContractsLoading(false);
        }
      }
    }

    void loadContracts();

    return () => {
      cancelled = true;
    };
  }, [projectRoot, selectedDeliverablePath, contractsRefreshToken]);

  const currentLifecycleState = statusSnapshot?.status.currentState;
  const transitionEnabled = useMemo(() => canAgentTransitionLifecycle(agent), [agent]);
  const availableTransitionTargets = useMemo(
    () => (currentLifecycleState ? nextLifecycleTargets(currentLifecycleState) : []),
    [currentLifecycleState]
  );
  const requiresApprovalSha = useMemo(
    () => requiresApprovalShaForTarget(transitionTarget),
    [transitionTarget]
  );

  useEffect(() => {
    if (!currentLifecycleState) {
      setTransitionTarget('');
      return;
    }

    const allowedTargets = nextLifecycleTargets(currentLifecycleState);
    setTransitionTarget((existing) => {
      if (existing && allowedTargets.some((state) => state === existing)) {
        return existing;
      }
      return allowedTargets[0] ?? '';
    });
    setTransitionError(null);
  }, [currentLifecycleState]);

  useEffect(() => {
    if (!requiresApprovalSha) {
      return;
    }

    if (transitionActor !== 'HUMAN') {
      setTransitionActor('HUMAN');
    }
  }, [requiresApprovalSha, transitionActor]);

  const scopeSummary = useMemo(() => {
    if (!projectRoot) {
      return 'No Working Root selected.';
    }

    if (scopeLoading) {
      return 'Scanning working root for deliverable scope...';
    }

    if (scopeError) {
      return scopeError;
    }

    if (!scopeData) {
      return 'No scope data available.';
    }

    return `${scopeData.deliverables.length} deliverables available for WORKBENCH contract checks.`;
  }, [projectRoot, scopeLoading, scopeError, scopeData]);

  const selectedDeliverable = useMemo(
    () => scopeData?.deliverables.find((item) => item.path === selectedDeliverablePath) ?? null,
    [scopeData, selectedDeliverablePath]
  );

  const dependencySummary = useMemo(
    () => (dependenciesSnapshot ? summarizeDependencyRows(dependenciesSnapshot.rows) : null),
    [dependenciesSnapshot]
  );

  const blockerCandidateIds = useMemo(() => {
    if (!dependenciesSnapshot) {
      return [] as string[];
    }

    return dependenciesSnapshot.rows
      .filter((row) => isExecutionBlockerSubsetRow(row))
      .slice(0, 5)
      .map((row) => row.DependencyID);
  }, [dependenciesSnapshot]);

  const canSubmitTransition =
    transitionEnabled &&
    Boolean(projectRoot) &&
    Boolean(selectedDeliverablePath) &&
    Boolean(transitionTarget) &&
    (!requiresApprovalSha || Boolean(transitionApprovalSha.trim())) &&
    !transitionSubmitting &&
    !contractsLoading;

  async function submitTransition(event: FormEvent<HTMLFormElement>): Promise<void> {
    event.preventDefault();

    if (!transitionEnabled || !projectRoot || !selectedDeliverablePath || !transitionTarget) {
      return;
    }

    if (requiresApprovalSha && !transitionApprovalSha.trim()) {
      setTransitionError('APPROVAL_SHA_REQUIRED: approvalSha is required for CHECKING/ISSUED transitions.');
      return;
    }

    setTransitionSubmitting(true);
    setTransitionError(null);

    try {
      const effectiveActor = requiresApprovalSha ? 'HUMAN' : transitionActor;
      const result = await transitionDeliverableStatus({
        projectRoot,
        deliverablePath: selectedDeliverablePath,
        targetState: transitionTarget,
        actor: effectiveActor,
        date: transitionDate.trim() || undefined,
        approvalSha: transitionApprovalSha.trim() || undefined
      });
      setStatusSnapshot(result);
    } catch (error) {
      setTransitionError(workspaceApiErrorMessage(error));
    } finally {
      setTransitionSubmitting(false);
    }
  }

  return (
      <section className="workbench-layout">
        <section className="workbench-card">
          <header>
            <h3>Active Agent Context</h3>
          </header>
          <dl>
            <div>
              <dt>Agent</dt>
              <dd>{agent}</dd>
            </div>
            <div>
              <dt>Matrix Row</dt>
              <dd>{row}</dd>
            </div>
            <div>
              <dt>Matrix Column</dt>
              <dd>{column}</dd>
            </div>
          </dl>
          <p>{scopeSummary}</p>
          <p>
            WORKBENCH preserves chat-driven orchestration while PIPELINE handles spawned task
            execution. This view now consumes deliverable contract routes for persona-led checks.
          </p>
        </section>

        <article className="pipeline-contracts">
          <header className="pipeline-contracts-header">
            <div>
              <h3>{transitionEnabled ? 'Deliverable Contracts' : 'Deliverable Contracts (Read-Only)'}</h3>
              <p className="pipeline-note">
                Uses lifecycle/dependency contract APIs for dependency and reconciliation reviews.
                {transitionEnabled
                  ? ' CHANGE and WORKING_ITEMS sessions may apply lifecycle transitions here with approval-SHA enforcement.'
                  : ' Transition writes are disabled for this agent.'}
              </p>
            </div>
            <button
              type="button"
              className="button-muted"
              disabled={!projectRoot || !selectedDeliverablePath || contractsLoading}
              onClick={() => {
                setContractsRefreshToken((value) => value + 1);
              }}
            >
              Refresh
            </button>
          </header>

          <label>
            Deliverable scope
            <select
              value={selectedDeliverablePath}
              onChange={(event) => {
                setSelectedDeliverablePath(event.target.value);
              }}
              disabled={!scopeData || scopeData.deliverables.length === 0}
            >
              {scopeData?.deliverables.length ? null : <option value="">No deliverables found</option>}
              {scopeData?.deliverables.map((item) => (
                <option key={item.path} value={item.path}>
                  {item.id} — {item.label}
                </option>
              ))}
            </select>
          </label>

          {!projectRoot ? (
            <p className="panel-empty">Select a Working Root to load contract snapshots.</p>
          ) : contractsLoading ? (
            <p className="panel-empty">Loading contract snapshots...</p>
          ) : contractsError ? (
            <p className="panel-error">{contractsError}</p>
          ) : !statusSnapshot || !dependenciesSnapshot ? (
            <p className="panel-empty">No contract data available for the selected deliverable.</p>
          ) : (
            <>
              <p className="pipeline-contract-path" title={statusSnapshot.deliverablePath}>
                {statusSnapshot.deliverablePath}
              </p>

              {selectedDeliverable ? (
                <p className="pipeline-note">
                  Selected deliverable: {selectedDeliverable.id} — {selectedDeliverable.label}
                </p>
              ) : null}

              <dl className="pipeline-contract-metrics">
                <div>
                  <dt>Current state</dt>
                  <dd>{statusSnapshot.status.currentState}</dd>
                </div>
                <div>
                  <dt>Last updated</dt>
                  <dd>{statusSnapshot.status.lastUpdated}</dd>
                </div>
                <div>
                  <dt>History entries</dt>
                  <dd>{statusSnapshot.status.history.length}</dd>
                </div>
                <div>
                  <dt>Dependency rows</dt>
                  <dd>{dependencySummary?.totalRows ?? 0}</dd>
                </div>
                <div>
                  <dt>Active rows</dt>
                  <dd>{dependencySummary?.activeRows ?? 0}</dd>
                </div>
                <div>
                  <dt>Blocker-subset rows</dt>
                  <dd>{dependencySummary?.activeUpstreamBlockerCandidates ?? 0}</dd>
                </div>
              </dl>

              {blockerCandidateIds.length > 0 ? (
                <div className="pipeline-contract-warnings">
                  <h4>Top blocker-subset candidates</h4>
                  <ul>
                    {blockerCandidateIds.map((dependencyId) => (
                      <li key={dependencyId}>{dependencyId}</li>
                    ))}
                  </ul>
                </div>
              ) : null}

              {dependenciesSnapshot.warnings.length > 0 ? (
                <div className="pipeline-contract-warnings">
                  <h4>Register warnings</h4>
                  <ul>
                    {dependenciesSnapshot.warnings.slice(0, 3).map((warning) => (
                      <li key={warning}>{warning}</li>
                    ))}
                  </ul>
                </div>
              ) : null}

              {transitionEnabled ? (
                <WorkbenchLifecycleTransitionForm
                  availableTransitionTargets={availableTransitionTargets}
                  canSubmitTransition={canSubmitTransition}
                  requiresApprovalSha={requiresApprovalSha}
                  transitionActor={transitionActor}
                  transitionApprovalSha={transitionApprovalSha}
                  transitionDate={transitionDate}
                  transitionError={transitionError}
                  transitionSubmitting={transitionSubmitting}
                  transitionTarget={transitionTarget}
                  onActorChange={(value) => {
                    setTransitionActor(value);
                    if (transitionError) {
                      setTransitionError(null);
                    }
                  }}
                  onApprovalShaChange={(value) => {
                    setTransitionApprovalSha(value);
                    if (transitionError) {
                      setTransitionError(null);
                    }
                  }}
                  onDateChange={(value) => {
                    setTransitionDate(value);
                    if (transitionError) {
                      setTransitionError(null);
                    }
                  }}
                  onSubmit={(event) => {
                    void submitTransition(event);
                  }}
                  onTargetChange={(value) => {
                    setTransitionTarget(value);
                    if (transitionError) {
                      setTransitionError(null);
                    }
                  }}
                />
              ) : null}
            </>
          )}
        </article>

        <section className="workbench-card workbench-documents-block" aria-label="Documents">
          <header>
            <h3>Documents</h3>
          </header>
          <p className="pipeline-note">
            Deliverable documents, evidence, and contracts read from the Working Root.
          </p>
          <DocumentView />
        </section>
      </section>
  );
}
