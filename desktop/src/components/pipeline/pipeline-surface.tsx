'use client';

import { useSearchParams } from 'next/navigation';
import React from 'react';
import { useEffect, useMemo, useState, type FormEvent } from 'react';
import { useDeliverables } from '../workspace/deliverables-provider';
import { useWorkspace } from '../workspace/workspace-provider';
import { harnessApiErrorMessage, scaffoldHarnessExecutionRoot } from '../../lib/harness/client';
import type { CoordinationMode, ScaffoldExecutionRootResponse } from '@chirality/runtime-contracts/types';
import {
  currentIsoDate,
  fetchDeliverableDependencies,
  fetchDeliverableStatus,
  nextLifecycleTargets,
  requiresApprovalShaForTarget,
  summarizeDependencyRows,
  transitionDeliverableStatus,
  workspaceApiErrorMessage,
  type DeliverableDependenciesSnapshot,
  type DeliverableStatusSnapshot
} from '../../lib/workspace/deliverable-api';
import {
  normalizeTaskScopeMode,
  sanitizeTaskSelection,
  type TaskScopeMode
} from '../../lib/workspace/task-scope';

type OperativeCategory = 'DECOMP' | 'PREP' | 'TASK' | 'AUDIT';

type Option = {
  value: string;
  label: string;
  enabled: boolean;
};

type PipelineLifecycleTransitionFormProps = {
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

const CATEGORY_ORDER: OperativeCategory[] = ['DECOMP', 'PREP', 'TASK', 'AUDIT'];
const SATISFACTION_DISPLAY_ORDER = [
  'TBD',
  'PENDING',
  'IN_PROGRESS',
  'SATISFIED',
  'WAIVED',
  'NOT_APPLICABLE'
];

const TRANSITION_ACTOR_OPTIONS: Option[] = [
  { value: 'WORKING_ITEMS', label: 'WORKING_ITEMS', enabled: true },
  { value: 'HUMAN', label: 'HUMAN', enabled: true },
  { value: 'CHIRALITY_FRAMEWORK', label: 'CHIRALITY_FRAMEWORK', enabled: true },
  { value: '4_DOCUMENTS', label: '4_DOCUMENTS', enabled: true }
];

const DECOMP_OPTIONS: Option[] = [
  { value: 'SOFTWARE', label: 'SOFTWARE', enabled: true },
  { value: 'PROJECT', label: 'PROJECT', enabled: true },
  { value: 'DOMAIN', label: 'DOMAIN', enabled: true },
  { value: 'BASE', label: 'BASE (create new)', enabled: false }
];

const PREP_OPTIONS: Option[] = [
  { value: 'PREPARATION', label: 'PREPARATION', enabled: true },
  { value: '4_DOCUMENTS', label: '4_DOCUMENTS', enabled: true },
  { value: 'CHIRALITY_FRAMEWORK', label: 'CHIRALITY_FRAMEWORK', enabled: true },
  { value: 'CHIRALITY_LENS', label: 'CHIRALITY_LENS', enabled: true }
];

const TASK_AGENT_OPTIONS: Option[] = [
  { value: 'SCOPE_CHANGE', label: 'SCOPE_CHANGE', enabled: true },
  { value: 'SCOPE_PREP', label: 'SCOPE_PREP', enabled: true },
  { value: 'ESTIMATE_PREP', label: 'ESTIMATE_PREP', enabled: true },
  { value: 'AUDIT_PREP', label: 'AUDIT_PREP', enabled: true },
  { value: 'SCHEDULE_PREP', label: 'SCHEDULE_PREP', enabled: true },
  { value: 'ESTIMATING', label: 'ESTIMATING', enabled: false },
  { value: 'SCHEDULING', label: 'SCHEDULING', enabled: false }
];

const AUDIT_OPTIONS: Option[] = [
  { value: 'AGENTS', label: 'AGENTS', enabled: true },
  { value: 'DEPENDENCIES', label: 'DEPENDENCIES', enabled: true },
  { value: 'ESTIMATES', label: 'ESTIMATES', enabled: false },
  { value: 'REFERENCES', label: 'REFERENCES', enabled: true },
  { value: 'SCHEDULES', label: 'SCHEDULES', enabled: false },
  { value: 'SCOPE', label: 'SCOPE', enabled: true }
];

const COORDINATION_MODE_OPTIONS: CoordinationMode[] = [
  'DEPENDENCY_TRACKED',
  'SCHEDULE_FIRST',
  'HYBRID'
];

function normalizeCategory(rawValue: string | null): OperativeCategory {
  const fallback: OperativeCategory = 'DECOMP';
  if (!rawValue) {
    return fallback;
  }

  if (CATEGORY_ORDER.includes(rawValue as OperativeCategory)) {
    return rawValue as OperativeCategory;
  }

  return fallback;
}

function renderOptionLabel(option: Option): string {
  return option.enabled ? option.label : `${option.label} (coming soon)`;
}

export function PipelineLifecycleTransitionForm({
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
}: PipelineLifecycleTransitionFormProps): JSX.Element {
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
            placeholder={
              requiresApprovalSha
                ? 'required: commit SHA for human gate transition'
                : 'optional: commit SHA for approval evidence'
            }
            required={requiresApprovalSha}
          />
        </label>
      </div>

      {transitionError ? <p className="panel-error">{transitionError}</p> : null}

      <div className="pipeline-transition-actions">
        <button type="submit" disabled={!canSubmitTransition}>
          {transitionSubmitting ? 'Applying...' : 'Apply Transition'}
        </button>
      </div>
    </form>
  );
}

export function PipelineSurface(): JSX.Element {
  const { projectRoot } = useWorkspace();
  const { loading: scopeLoading, error: scopeError, scan: scopeData, refresh: refreshScopeData } =
    useDeliverables();
  const searchParams = useSearchParams();
  const deliverableOptions = scopeData?.deliverables ?? [];
  const knowledgeTypeOptions = scopeData?.knowledgeTypes ?? [];
  const hasKnowledgeDecomposition = scopeData?.knowledgeDecomposition.enabled ?? false;
  const initialTaskScopeMode = normalizeTaskScopeMode(
    searchParams.get('taskScopeMode'),
    hasKnowledgeDecomposition
  );
  const initialTaskSelection = sanitizeTaskSelection(
    {
      scopeMode: initialTaskScopeMode,
      scopeKey: (searchParams.get('scopeKey') ?? '').trim(),
      targetDeliverableKey:
        initialTaskScopeMode === 'KNOWLEDGE_TYPES'
          ? (searchParams.get('targetDeliverableKey') ?? '').trim()
          : ''
    },
    {
      knowledgeDecompositionEnabled: hasKnowledgeDecomposition,
      deliverableKeys: deliverableOptions.map((item) => item.key),
      knowledgeTypes: knowledgeTypeOptions
    }
  );

  const [selectedCategory, setSelectedCategory] = useState<OperativeCategory>(() =>
    normalizeCategory(searchParams.get('category'))
  );
  const [selectedDecomp, setSelectedDecomp] = useState('SOFTWARE');
  const [selectedPrep, setSelectedPrep] = useState('PREPARATION');
  const [selectedAudit, setSelectedAudit] = useState('AGENTS');
  const [selectedTaskAgent, setSelectedTaskAgent] = useState('SCOPE_CHANGE');
  const [taskScopeMode, setTaskScopeMode] = useState<TaskScopeMode>(
    initialTaskSelection.scopeMode
  );
  const [selectedScopeKey, setSelectedScopeKey] = useState(initialTaskSelection.scopeKey);
  const [selectedTargetDeliverableKey, setSelectedTargetDeliverableKey] = useState(
    initialTaskSelection.targetDeliverableKey
  );

  const [contractsRefreshToken, setContractsRefreshToken] = useState(0);
  const [contractsLoading, setContractsLoading] = useState(false);
  const [contractsError, setContractsError] = useState<string | null>(null);
  const [statusSnapshot, setStatusSnapshot] = useState<DeliverableStatusSnapshot | null>(null);
  const [dependenciesSnapshot, setDependenciesSnapshot] =
    useState<DeliverableDependenciesSnapshot | null>(null);

  const [transitionTarget, setTransitionTarget] = useState('');
  const [transitionActor, setTransitionActor] = useState('WORKING_ITEMS');
  const [transitionDate, setTransitionDate] = useState(currentIsoDate);
  const [transitionApprovalSha, setTransitionApprovalSha] = useState('');
  const [transitionError, setTransitionError] = useState<string | null>(null);
  const [transitionSubmitting, setTransitionSubmitting] = useState(false);

  const [scaffoldDecompositionPath, setScaffoldDecompositionPath] = useState('');
  const [scaffoldProjectName, setScaffoldProjectName] = useState('');
  const [scaffoldCoordinationMode, setScaffoldCoordinationMode] =
    useState<CoordinationMode>('DEPENDENCY_TRACKED');
  const [scaffoldSubmitting, setScaffoldSubmitting] = useState(false);
  const [scaffoldError, setScaffoldError] = useState<string | null>(null);
  const [scaffoldResult, setScaffoldResult] = useState<ScaffoldExecutionRootResponse | null>(null);

  useEffect(() => {
    setSelectedCategory(normalizeCategory(searchParams.get('category')));
  }, [searchParams]);

  useEffect(() => {
    setScaffoldResult(null);
    setScaffoldError(null);
    setScaffoldProjectName('');
    setScaffoldCoordinationMode('DEPENDENCY_TRACKED');
    setTaskScopeMode('DELIVERABLES');
    setSelectedScopeKey('');
    setSelectedTargetDeliverableKey('');
  }, [projectRoot]);

  const deliverableByKey = useMemo(
    () => new Map(deliverableOptions.map((item) => [item.key, item])),
    [deliverableOptions]
  );

  useEffect(() => {
    const requestedScopeMode = normalizeTaskScopeMode(
      searchParams.get('taskScopeMode'),
      hasKnowledgeDecomposition
    );
    const requestedScopeKey = (searchParams.get('scopeKey') ?? '').trim();
    const requestedTargetDeliverableKey = (searchParams.get('targetDeliverableKey') ?? '').trim();

    setTaskScopeMode(requestedScopeMode);
    setSelectedScopeKey(requestedScopeKey);
    setSelectedTargetDeliverableKey(
      requestedScopeMode === 'KNOWLEDGE_TYPES' ? requestedTargetDeliverableKey : ''
    );
  }, [searchParams, hasKnowledgeDecomposition]);

  useEffect(() => {
    if (!scopeError) {
      return;
    }

    setTaskScopeMode('DELIVERABLES');
    setSelectedScopeKey('');
    setSelectedTargetDeliverableKey('');
  }, [scopeError]);

  useEffect(() => {
    const normalized = sanitizeTaskSelection(
      {
        scopeMode: taskScopeMode,
        scopeKey: selectedScopeKey,
        targetDeliverableKey: selectedTargetDeliverableKey
      },
      {
        knowledgeDecompositionEnabled: hasKnowledgeDecomposition,
        deliverableKeys: deliverableOptions.map((item) => item.key),
        knowledgeTypes: knowledgeTypeOptions
      }
    );

    if (normalized.scopeMode !== taskScopeMode) {
      setTaskScopeMode(normalized.scopeMode);
    }
    if (normalized.scopeKey !== selectedScopeKey) {
      setSelectedScopeKey(normalized.scopeKey);
    }
    if (normalized.targetDeliverableKey !== selectedTargetDeliverableKey) {
      setSelectedTargetDeliverableKey(normalized.targetDeliverableKey);
    }
  }, [
    taskScopeMode,
    selectedScopeKey,
    selectedTargetDeliverableKey,
    deliverableOptions,
    knowledgeTypeOptions,
    hasKnowledgeDecomposition
  ]);

  const selectedKnowledgeType = useMemo(
    () => knowledgeTypeOptions.find((item) => item.id === selectedScopeKey) ?? null,
    [knowledgeTypeOptions, selectedScopeKey]
  );

  const knowledgeTargetOptions = useMemo(() => {
    if (!selectedKnowledgeType) {
      return [] as typeof deliverableOptions;
    }

    return selectedKnowledgeType.matchingDeliverableKeys
      .map((deliverableKey) => deliverableByKey.get(deliverableKey))
      .filter((candidate): candidate is (typeof deliverableOptions)[number] => Boolean(candidate));
  }, [selectedKnowledgeType, deliverableByKey]);

  const selectedDeliverableKey =
    taskScopeMode === 'KNOWLEDGE_TYPES' ? selectedTargetDeliverableKey : selectedScopeKey;
  const selectedDeliverableScope = deliverableByKey.get(selectedDeliverableKey)?.path ?? '';

  useEffect(() => {
    let cancelled = false;

    async function loadDeliverableContracts(): Promise<void> {
      if (!projectRoot || !selectedDeliverableScope) {
        setStatusSnapshot(null);
        setDependenciesSnapshot(null);
        setContractsError(null);
        return;
      }

      setContractsLoading(true);
      setContractsError(null);

      try {
        const [status, dependencies] = await Promise.all([
          fetchDeliverableStatus(projectRoot, selectedDeliverableScope),
          fetchDeliverableDependencies(projectRoot, selectedDeliverableScope)
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

    void loadDeliverableContracts();

    return () => {
      cancelled = true;
    };
  }, [projectRoot, selectedDeliverableScope, contractsRefreshToken]);

  const currentLifecycleState = statusSnapshot?.status.currentState;

  useEffect(() => {
    if (!currentLifecycleState) {
      setTransitionTarget('');
      return;
    }

    const allowedTargets = nextLifecycleTargets(currentLifecycleState);
    setTransitionTarget(allowedTargets[0] ?? '');
    setTransitionError(null);
  }, [currentLifecycleState]);

  const scopeSummary = useMemo(() => {
    if (!projectRoot) {
      return 'No Working Root selected.';
    }

    if (scopeLoading) {
      return 'Scanning working root for deliverables and knowledge types...';
    }

    if (scopeError) {
      return scopeError;
    }

    if (!scopeData) {
      return 'No scope data available.';
    }

    const baseSummary = `${scopeData.deliverables.length} deliverables, ${scopeData.knowledgeTypes.length} knowledge types`;
    if (!scopeData.truncated) {
      return baseSummary;
    }

    return `${baseSummary}. Scan truncated at directory cap for responsiveness.`;
  }, [projectRoot, scopeLoading, scopeError, scopeData]);

  const selectedDeliverable = useMemo(
    () => (selectedDeliverableKey ? deliverableByKey.get(selectedDeliverableKey) ?? null : null),
    [deliverableByKey, selectedDeliverableKey]
  );

  const dependencySummary = useMemo(
    () => (dependenciesSnapshot ? summarizeDependencyRows(dependenciesSnapshot.rows) : null),
    [dependenciesSnapshot]
  );

  const satisfactionSummary = useMemo(() => {
    if (!dependencySummary) {
      return [] as Array<{ key: string; count: number }>;
    }

    const seen = new Set<string>();
    const ordered: Array<{ key: string; count: number }> = [];

    for (const key of SATISFACTION_DISPLAY_ORDER) {
      const count = dependencySummary.bySatisfaction[key];
      if (count) {
        seen.add(key);
        ordered.push({ key, count });
      }
    }

    for (const [key, count] of Object.entries(dependencySummary.bySatisfaction)) {
      if (!seen.has(key)) {
        ordered.push({ key, count });
      }
    }

    return ordered;
  }, [dependencySummary]);

  const availableTransitionTargets = useMemo(
    () => (currentLifecycleState ? nextLifecycleTargets(currentLifecycleState) : []),
    [currentLifecycleState]
  );
  const requiresApprovalSha = useMemo(
    () => requiresApprovalShaForTarget(transitionTarget),
    [transitionTarget]
  );

  const scaffoldIssuePreview = useMemo(() => {
    if (!scaffoldResult || scaffoldResult.preparationCompatibility.ready) {
      return [] as Array<{ deliverableId: string; message: string }>;
    }

    const preview: Array<{ deliverableId: string; message: string }> = [];
    for (const item of scaffoldResult.preparationCompatibility.deliverables) {
      for (const issue of item.issues) {
        preview.push({
          deliverableId: item.id,
          message: issue
        });
        if (preview.length >= 5) {
          return preview;
        }
      }
    }

    return preview;
  }, [scaffoldResult]);

  const canSubmitTransition =
    Boolean(projectRoot) &&
    Boolean(selectedDeliverableScope) &&
    Boolean(transitionTarget) &&
    (!requiresApprovalSha || Boolean(transitionApprovalSha.trim())) &&
    !transitionSubmitting &&
    !contractsLoading;

  useEffect(() => {
    if (!requiresApprovalSha) {
      return;
    }

    if (transitionActor !== 'HUMAN') {
      setTransitionActor('HUMAN');
    }
  }, [requiresApprovalSha, transitionActor]);

  async function submitTransition(event: FormEvent<HTMLFormElement>): Promise<void> {
    event.preventDefault();

    if (!projectRoot || !selectedDeliverableScope || !transitionTarget) {
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
        deliverablePath: selectedDeliverableScope,
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

  async function submitScaffold(event: FormEvent<HTMLFormElement>): Promise<void> {
    event.preventDefault();

    if (!projectRoot) {
      setScaffoldError('Select a Working Root before running scaffold.');
      return;
    }

    const decompositionPath = scaffoldDecompositionPath.trim();
    if (!decompositionPath) {
      setScaffoldError('Decomposition path is required.');
      return;
    }

    setScaffoldSubmitting(true);
    setScaffoldError(null);

    try {
      const result = await scaffoldHarnessExecutionRoot({
        executionRoot: projectRoot,
        decompositionPath,
        projectName: scaffoldProjectName.trim() || undefined,
        coordinationMode: scaffoldCoordinationMode
      });

      setScaffoldResult(result);
      refreshScopeData();
      setContractsRefreshToken((value) => value + 1);
    } catch (error) {
      setScaffoldResult(null);
      setScaffoldError(harnessApiErrorMessage(error));
    } finally {
      setScaffoldSubmitting(false);
    }
  }

  function requestContractsRefresh(): void {
    setTransitionError(null);
    setContractsRefreshToken((value) => value + 1);
  }

  return (
      <section className="pipeline-layout">
        <section className="pipeline-grid">
          <article className={`pipeline-card ${selectedCategory === 'DECOMP' ? 'pipeline-card--active' : ''}`}>
            <header>
              <h3>DECOMP*</h3>
              <p>SOFTWARE, PROJECT, DOMAIN, and BASE create-new variant routing.</p>
            </header>
            <label>
              Decomposition lane
              <select
                value={selectedDecomp}
                onChange={(event) => {
                  setSelectedCategory('DECOMP');
                  setSelectedDecomp(event.target.value);
                }}
              >
                {DECOMP_OPTIONS.map((option) => (
                  <option key={option.value} value={option.value} disabled={!option.enabled}>
                    {renderOptionLabel(option)}
                  </option>
                ))}
              </select>
            </label>
          </article>

          <article className={`pipeline-card ${selectedCategory === 'PREP' ? 'pipeline-card--active' : ''}`}>
            <header>
              <h3>PREP*</h3>
              <p>Preparation and semantic framing pipelines.</p>
            </header>
            <label>
              Preparation lane
              <select
                value={selectedPrep}
                onChange={(event) => {
                  setSelectedCategory('PREP');
                  setSelectedPrep(event.target.value);
                }}
              >
                {PREP_OPTIONS.map((option) => (
                  <option key={option.value} value={option.value} disabled={!option.enabled}>
                    {renderOptionLabel(option)}
                  </option>
                ))}
              </select>
            </label>
          </article>

          <article className={`pipeline-card ${selectedCategory === 'TASK' ? 'pipeline-card--active' : ''}`}>
            <header>
              <h3>TASK*</h3>
              <p>Split selectors: static task agent + dynamic scope from Working Root.</p>
            </header>

            <label>
              Task agent
              <select
                value={selectedTaskAgent}
                onChange={(event) => {
                  setSelectedCategory('TASK');
                  setSelectedTaskAgent(event.target.value);
                }}
              >
                {TASK_AGENT_OPTIONS.map((option) => (
                  <option key={option.value} value={option.value} disabled={!option.enabled}>
                    {renderOptionLabel(option)}
                  </option>
                ))}
              </select>
            </label>

            <label>
              Scope Mode
              <select
                value={taskScopeMode}
                onChange={(event) => {
                  setSelectedCategory('TASK');
                  const nextMode = normalizeTaskScopeMode(
                    event.target.value,
                    hasKnowledgeDecomposition
                  );
                  setTaskScopeMode(nextMode);
                  setSelectedScopeKey('');
                  setSelectedTargetDeliverableKey('');
                }}
              >
                <option value="DELIVERABLES">DELIVERABLES</option>
                {hasKnowledgeDecomposition ? (
                  <option value="KNOWLEDGE_TYPES">KNOWLEDGE_TYPES</option>
                ) : null}
              </select>
            </label>

            <label>
              Scope (dynamic)
              <select
                value={selectedScopeKey}
                onChange={(event) => {
                  setSelectedCategory('TASK');
                  setSelectedScopeKey(event.target.value);
                  if (taskScopeMode === 'KNOWLEDGE_TYPES') {
                    setSelectedTargetDeliverableKey('');
                  }
                }}
                disabled={
                  scopeLoading ||
                  Boolean(scopeError) ||
                  (taskScopeMode === 'DELIVERABLES'
                    ? deliverableOptions.length === 0
                    : knowledgeTypeOptions.length === 0)
                }
              >
                {scopeLoading ? <option value="">Loading scope options...</option> : null}
                {!scopeLoading && scopeError ? <option value="">Scope load failed</option> : null}
                {!scopeLoading &&
                !scopeError &&
                taskScopeMode === 'DELIVERABLES' &&
                deliverableOptions.length === 0 ? (
                  <option value="">No deliverables found</option>
                ) : null}
                {!scopeLoading &&
                !scopeError &&
                taskScopeMode === 'KNOWLEDGE_TYPES' &&
                knowledgeTypeOptions.length === 0 ? (
                  <option value="">No knowledge types found</option>
                ) : null}
                {taskScopeMode === 'DELIVERABLES'
                  ? deliverableOptions.map((item) => (
                      <option key={item.key} value={item.key}>
                        {item.id} — {item.name}
                      </option>
                    ))
                  : knowledgeTypeOptions.map((item) => (
                      <option key={item.id} value={item.id}>
                        {item.label} ({item.matchingDeliverableKeys.length})
                      </option>
                    ))}
              </select>
            </label>

            {taskScopeMode === 'KNOWLEDGE_TYPES' ? (
              <label>
                Target Deliverable (required)
                <select
                  value={selectedTargetDeliverableKey}
                  onChange={(event) => {
                    setSelectedCategory('TASK');
                    setSelectedTargetDeliverableKey(event.target.value);
                  }}
                  disabled={scopeLoading || Boolean(scopeError) || knowledgeTargetOptions.length === 0}
                >
                  {scopeLoading ? <option value="">Loading target deliverables...</option> : null}
                  {!scopeLoading && scopeError ? <option value="">Scope load failed</option> : null}
                  {!scopeLoading && !scopeError && knowledgeTargetOptions.length === 0 ? (
                    <option value="">No matching deliverables available</option>
                  ) : null}
                  {knowledgeTargetOptions.map((item) => (
                    <option key={item.key} value={item.key}>
                      {item.id} — {item.name}
                    </option>
                  ))}
                </select>
              </label>
            ) : null}

            {hasKnowledgeDecomposition ? (
              <p className="pipeline-note">
                Knowledge decomposition marker detected:
                {scopeData?.knowledgeDecomposition.markerFile ? (
                  <> {scopeData.knowledgeDecomposition.markerFile}</>
                ) : (
                  ' yes'
                )}
              </p>
            ) : (
              <p className="pipeline-note">
                `KNOWLEDGE_TYPES` scope mode is unavailable: no decomposition marker detected.
              </p>
            )}

            {scopeError ? (
              <p className="panel-error">{scopeError}</p>
            ) : null}

            {taskScopeMode === 'DELIVERABLES' && selectedScopeKey ? (
              <p className="pipeline-note">
                Selected deliverable key: <code>{selectedScopeKey}</code>
              </p>
            ) : null}

            {taskScopeMode === 'KNOWLEDGE_TYPES' && selectedScopeKey ? (
              <p className="pipeline-note">
                Selected knowledge type: <code>{selectedScopeKey}</code>
                {selectedTargetDeliverableKey ? (
                  <>
                    {' -> target '}
                    <code>{selectedTargetDeliverableKey}</code>
                  </>
                ) : null}
              </p>
            ) : null}
          </article>

          <article className={`pipeline-card ${selectedCategory === 'AUDIT' ? 'pipeline-card--active' : ''}`}>
            <header>
              <h3>AUDIT*</h3>
              <p>Evaluation lanes with selective "coming soon" support.</p>
            </header>
            <label>
              Audit lane
              <select
                value={selectedAudit}
                onChange={(event) => {
                  setSelectedCategory('AUDIT');
                  setSelectedAudit(event.target.value);
                }}
              >
                {AUDIT_OPTIONS.map((option) => (
                  <option key={option.value} value={option.value} disabled={!option.enabled}>
                    {renderOptionLabel(option)}
                  </option>
                ))}
              </select>
            </label>
          </article>
        </section>

        <article className="pipeline-summary">
          <h3>Dynamic Scope Scan</h3>
          <p>{scopeSummary}</p>
          <p>
            Selected category: <strong>{selectedCategory}</strong>
          </p>
        </article>

        <article className="pipeline-contracts">
          <header className="pipeline-contracts-header">
            <div>
              <h3>Execution Root Scaffold</h3>
              <p className="pipeline-note">
                Runs `POST /api/harness/scaffold` and validates PREPARATION handoff compatibility.
              </p>
            </div>
          </header>

          {!projectRoot ? (
            <p className="panel-empty">Select a Working Root before running scaffold.</p>
          ) : (
            <form
              className="pipeline-transition-form"
              onSubmit={(event) => {
                void submitScaffold(event);
              }}
            >
              <div className="pipeline-transition-grid">
                <label>
                  Decomposition markdown path
                  <input
                    value={scaffoldDecompositionPath}
                    onChange={(event) => {
                      setScaffoldDecompositionPath(event.target.value);
                      if (scaffoldError) {
                        setScaffoldError(null);
                      }
                    }}
                    placeholder="/absolute/path/to/decomposition.md"
                  />
                </label>

                <label>
                  Coordination mode
                  <select
                    value={scaffoldCoordinationMode}
                    onChange={(event) => {
                      setScaffoldCoordinationMode(event.target.value as CoordinationMode);
                    }}
                  >
                    {COORDINATION_MODE_OPTIONS.map((mode) => (
                      <option key={mode} value={mode}>
                        {mode}
                      </option>
                    ))}
                  </select>
                </label>

                <label>
                  Project name (optional)
                  <input
                    value={scaffoldProjectName}
                    onChange={(event) => {
                      setScaffoldProjectName(event.target.value);
                    }}
                    placeholder="Overrides decomposition title"
                  />
                </label>
              </div>

              {scaffoldError ? <p className="panel-error">{scaffoldError}</p> : null}

              <div className="pipeline-transition-actions">
                <button
                  type="submit"
                  disabled={scaffoldSubmitting || !scaffoldDecompositionPath.trim()}
                >
                  {scaffoldSubmitting ? 'Scaffolding...' : 'Scaffold Execution Root'}
                </button>
              </div>
            </form>
          )}

          {scaffoldResult ? (
            <>
              <p className="pipeline-contract-path" title={scaffoldResult.executionRoot}>
                {scaffoldResult.executionRoot}
              </p>
              <p className="pipeline-note" title={scaffoldResult.decompositionPath}>
                Decomposition: {scaffoldResult.decompositionPath}
              </p>
              <dl className="pipeline-contract-metrics">
                <div>
                  <dt>Packages</dt>
                  <dd>{scaffoldResult.packageCount}</dd>
                </div>
                <div>
                  <dt>Deliverables</dt>
                  <dd>{scaffoldResult.deliverableCount}</dd>
                </div>
                <div>
                  <dt>Created directories</dt>
                  <dd>{scaffoldResult.created.directories.length}</dd>
                </div>
                <div>
                  <dt>Created files</dt>
                  <dd>{scaffoldResult.created.files.length}</dd>
                </div>
                <div>
                  <dt>Layout valid</dt>
                  <dd>{scaffoldResult.layoutValidation.valid ? 'YES' : 'NO'}</dd>
                </div>
                <div>
                  <dt>PREPARATION ready</dt>
                  <dd>{scaffoldResult.preparationCompatibility.ready ? 'YES' : 'NO'}</dd>
                </div>
              </dl>

              {!scaffoldResult.preparationCompatibility.ready ? (
                <div className="pipeline-contract-warnings">
                  <h4>PREPARATION Compatibility Issues</h4>
                  <ul>
                    {scaffoldIssuePreview.map((issue) => (
                      <li key={`${issue.deliverableId}:${issue.message}`}>
                        {issue.deliverableId}: {issue.message}
                      </li>
                    ))}
                  </ul>
                  {scaffoldResult.preparationCompatibility.issueCount > scaffoldIssuePreview.length ? (
                    <p className="pipeline-note">
                      +{scaffoldResult.preparationCompatibility.issueCount - scaffoldIssuePreview.length} additional
                      issue(s)
                    </p>
                  ) : null}
                </div>
              ) : null}
            </>
          ) : null}
        </article>

        <article className="pipeline-contracts">
          <header className="pipeline-contracts-header">
            <div>
              <h3>Deliverable Contracts</h3>
              <p className="pipeline-note">
                Consumes lifecycle and dependency contract routes for the selected deliverable.
              </p>
            </div>
            <button
              type="button"
              className="button-muted"
              onClick={requestContractsRefresh}
              disabled={!projectRoot || !selectedDeliverableScope || contractsLoading}
            >
              Refresh
            </button>
          </header>

          {!projectRoot ? (
            <p className="panel-empty">Select a Working Root to inspect deliverable contracts.</p>
          ) : !selectedDeliverableScope ? (
            <p className="panel-empty">Select a deliverable in the TASK lane to load contracts.</p>
          ) : contractsLoading ? (
            <p className="panel-empty">Loading deliverable contract snapshots...</p>
          ) : contractsError ? (
            <p className="panel-error">{contractsError}</p>
          ) : !statusSnapshot || !dependenciesSnapshot ? (
            <p className="panel-empty">No deliverable contract snapshot is currently available.</p>
          ) : (
            <>
              <p className="pipeline-contract-path" title={statusSnapshot.deliverablePath}>
                {statusSnapshot.deliverablePath}
              </p>

              {selectedDeliverable ? (
                <p className="pipeline-note">
                  Selected deliverable: {selectedDeliverable.id} — {selectedDeliverable.name}
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

              {satisfactionSummary.length > 0 ? (
                <div className="pipeline-contract-satisfaction">
                  <h4>Satisfaction Snapshot</h4>
                  <div className="pipeline-contract-tags">
                    {satisfactionSummary.map((entry) => (
                      <span key={entry.key} className="pipeline-contract-tag">
                        {entry.key}: {entry.count}
                      </span>
                    ))}
                  </div>
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

              <PipelineLifecycleTransitionForm
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
            </>
          )}
        </article>
      </section>
  );
}
