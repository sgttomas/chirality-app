import { EmbeddedAgentSession, type AgentContext, type AgentRunReceipt } from "../../services/embeddedAgentSession";
import { requeueRetainedRecord, type ImportContext } from "../../services/operationAuthorship";
import { hasCurrentSourceContract } from "../results/resultReader";
import type React from "react";
import {
  acknowledgeNativeCloseRequest, isTauriRuntime, NATIVE_CLOSE_REQUEST_DOM_EVENT, nativeCloseRequestFrom,
  resolveNativeCloseRequest, syncNativeShellState, type NativeCloseRequest
} from "../../services/nativeMenu";
import { useEffect, useLayoutEffect, useMemo, useRef, useState } from "react";
import {
  canonicalSha256Hex,
  checkedJsonText,
  computeModelHash,
  computeProjectEnvelopeHash
} from "../../services/hashService";
import { buildCurrentSessionInputManifest } from "../../services/inputManifestService";
import { NO_RULE_PACK_RESOLUTION, recordRulePackExclusions, resolveModelRulePacks } from "../../services/modelRulePackResolution";
import type { CurrentSessionInputManifestEvidence } from "../../services/inputManifestService";
import { applyOperationBatch, validateOperationBatch } from "../../services/operationBatchService";
import type { OperationBatch, OperationBatchOutcome } from "../../services/operationBatchService";
import {
  applyModelOperation,
  validateModelOperation,
  warmupOperationEngine
} from "../../services/operationService";
import {
  buildAnalysisRunPreview,
  abandonPreviewMechanicsJob,
  beginSessionResultCustodyReset,
  cancelPreviewMechanicsJob,
  loadDesignKnowledge,
  loadBundledMechanicsReference,
  loadPreviewModel,
  loadSampleProposal,
  hasNativeMechanicsInvocation,
  discardPreviewMechanicsJobResult,
  disposeDeliveredMechanicsResult,
  startPreviewMechanicsJob,
  takePreviewMechanicsJobResult,
  terminalJobError
} from "../../services/previewService";
import { ResourceUnavailableError } from "../../services/memoryPool";
import { IngressRequestRetiredError, nativeFailureText } from "../../services/nativeIngress";
import {
  buildBlankLocalModelDocument,
  buildBlankLoadStateModelDocument,
  createLocalProject,
  findLocalProject,
  getLocalStorageCapability,
  listLocalProjects,
  openLocalProject,
  StoredProjectUnitsRefusal,
  saveLocalProject,
  SI_PROJECT_UNITS,
  type ProjectUnitMap
} from "../../services/projectService";
import type { BlankProjectKind, BlankProjectUnitsRequest } from "../project-units/ProjectUnitsDialog";
import { MODEL_DOCUMENT_FILE_SOURCE, modelFileRefusalMessage, modelFileWarningSuffix, type ModelDocumentSource } from "../../services/modelDocumentFile";
import { checkModelLibraryRefs, modelLibraryRefs } from "../../services/libraryImportService";
import { currentLibraryRefFindings, libraryRefDiagnostics, publishLibraryRefFindings } from "../library/libraryRefFindings";
import { cancelNativeModelChecks, runModelChecks, type ModelCheckRun } from "../diagnostics/modelChecks";
import { modelDocumentSlotValidation } from "../model-file/modelDocumentShape";
import {
  keptStoredProjectMessage,
  type ReplaceProjectChoice,
  type ReplaceProjectPromptState,
  type StoredProjectWrite
} from "../project-storage/storedProjectConflict";
import { MODEL_FILE_SHAPE } from "../model-file/modelDocumentShape";
import {
  MODEL_DOC_SAVE_HASH_PENDING,
  modelDocumentSaveFailureMessage,
  modelDocumentSaveMessage,
  modelDocumentSaveRefusalMessage,
  prepareModelDocumentSave,
  resolveLibraryDispositions,
  saveModelDocumentFile
} from "../model-file/modelDocumentSave";
import type { ModelDocumentSaveDialogRequest } from "../model-file/ModelDocumentSaveDialog";
import {
  saveStoredModelDocumentFile,
  storedDocumentExportFailureMessage,
  storedDocumentExportMessage,
  storedProjectDescription,
  type StoredDocumentExportTarget
} from "../model-file/storedDocumentExport";
import {
  HANDOFF_SAVE_DESKTOP_ONLY,
  HANDOFF_SAVE_ROUTE,
  handoffBasis,
  handoffSaveFailureMessage,
  handoffSaveMessage,
  handoffSaveRefusalMessage,
  saveHandoffPackage,
  type HandoffBasis
} from "../handoff/handoffPackageSave";
import type { HandoffSaveChoice, HandoffSaveDialogRequest } from "../handoff/HandoffSaveDialog";
import { invokeReportPackageSave, prepareReportPackageSave } from "../../services/reportPackageSaveService";
import type { RuleCheckStatus } from "../../services/ruleCheckService";
import type { SessionRuleCheckRun } from "../report/renderableReportInput";
import type {
  AnalysisRunEnvelope,
  AppliedOperationReceipt,
  OperationOutcome,
  EditorOperationIntent,
  EntityRef,
  LocalProjectEnvelope,
  MechanicsResult,
  ModelHashEvidence,
  ProjectEnvelopeHashEvidence,
  PreviewModel,
  SolveJobAuditState
} from "../../types";
import { defaultSelection } from "../model-workspace/modelView";
import { intentKey } from "../operations/OperationApplyPanel";
import { buildReportPackageRequest, reportPackageExactSubmission } from "../report/reportPackageRequest";
import { controlReportPackageRequest } from "../report/reportRedactionProjector";
import { buildBundledReferenceContext, buildHistoricalRunContext } from "../results/HistoricalRunContext";
import type { HistoricalRunContext } from "../results/HistoricalRunContext";
import {
  resolveDiagnosticEntitySelection,
  resolveEntitySelection
} from "../results/resultInterpretation";
import { MODEL_SCHEMA_VERSION } from "../../services/modelSchemaVersion";
import type { RuleCheckRunBasis } from "../rule-check/RuleCheckRunPanel";
import { batchRequiresPreview, operationRequiresPreview, previewSatisfied, PREVIEW_REQUIRED_REASON, type QueuedBatch } from "../toolkit/BatchReviewPanel";
import { capabilityAvailability, capabilityRoute } from "../toolkit/capabilityCatalog";
import type { ToolkitCapability } from "../toolkit/capabilityCatalog";
import type { CreationTool, ViewportExposureInteraction } from "../viewport/PipeViewport";
import {
  applyResultMatchesSubmission,
  sameSubmission,
  validationMatchesSubmission
} from "../viewport/routeDraft";
import type { DraftSubmission, FrozenDraftReview } from "../viewport/routeDraft";
import { deriveViewportVisibility } from "../viewport/viewportVisibility";
import { useChromeSessionState } from "./chromeSessionState";
import type { R3JourneyEvent } from "./chromeSessionState";
import { isMenuCommandId } from "./menuCommands";
import type { MenuCommandId } from "./menuCommands";
import { buildModelIndex, modelIndexFor } from "./modelIndex";
import { useModelSessionState } from "./modelSessionState";
import { useOperationsSessionState } from "./operationsSessionState";
import {
  canPublishPersistenceObservation,
  ownsOpenPersistenceObservation,
  verifiedWriteBasis, isLocalModelEdited,
  deriveModelHashIntegrity,
  deriveProjectEnvelopeHashIntegrity
} from "./projectPersistenceIntegrity";
import { persistenceHashesMatch } from "./savedModelBasis";
import { useModelStateHistory, type LandedProjectSave, type ProjectBinding } from "../history/useModelStateHistory";
import { unsavedChangesRefusal, useUnsavedChangesGuard } from "../project-storage/unsavedChangesGuard";
import { openAutosaveSource, useAutosave } from "../autosave";
import { createModalHolds, type ModalHolds } from "../project-storage/modalHolds";
import { withinRunBusyReason, type WithinRunPair } from "../comparison/withinRunComparison";
import { listModelStates, modelStateDescription, saveModelState, type ModelStateRead } from "../../services/modelStateService";
import { useProjectSessionState } from "./projectSessionState";
import { useResultsSessionState } from "./resultsSessionState";
import { useSelectionSessionState } from "./selectionSessionState";
import {
  applyBoxSelection,
  applyDisplayedRange,
  applySelection,
  emptySelection,
  primarySelection,
  pruneSelection,
  sameSelection,
  singletonSelection
} from "./selectionState";
import type { EntityKey, OrderedSelectionState, SelectionModifiers } from "./selectionState";
import {
  clonePreviewModel,
  selectionForOperationOutcome,
  uiModelIdentityHash,
  type SessionModelCheckpoint
} from "./sessionModel";
import { commitModelAfterSolveInvalidation } from "./solveGates";
import {
  awaitBackendSolveJob,
  blankProjectCreatedSolveJob,
  cancelledBeforeBackendStartSolveJob,
  cancelledSolveJob,
  cancelledWithoutBackendSolveJob,
  completeSolveJob,
  failSolveJob,
  initialSolveJob,
  modelChangedSolveJob,
  pendingBackendStartCancellationSolveJob,
  progressSolveJob,
  refusedAtTakeSolveJob,
  refusedBeforeBackendStartSolveJob,
  refusedSolveJob,
  recordBackendCancellationFailure,
  recordBackendCancellationReceipt,
  requestSolveCancellation,
  sessionHistoryChangedSolveJob,
  startSolveJob
} from "./solveJobAudit";
import { publishUiModelAssignmentStarted } from "./uiDiagnostics";
import {
  EMPTY_STAGE_VIEW_MEMORY,
  SHELL_STAGES,
  SHELL_VIEWS,
  canvasAuthoringPanelActive,
  isStageSurface,
  railStageState,
  rememberStageView,
  runPresenceFromCells,
  sectionAfterPageClose,
  sectionForStage,
  shellLocation,
  stageSurfaceAfter,
  viewForStage
} from "./shellLayout";
import type { ShellStage, ShellView } from "./shellLayout";
import type { UiDensityPreference, UiThemePreference } from "./uiPreferences";
import { updateUiPreferences, writeUiPreferences } from "./uiPreferences";
import { observeWorkspaceCanvasBudget } from "./workspaceCanvasBudget";
import { EXPENSIVE_LIFECYCLE_SECTIONS } from "./workspaceSections";
import { createSessionEventChannel } from "./sessionEvents";
import type { WorkspaceSectionId } from "./workspaceSections";

/** W-13 §3.5 / W-17 §2.7: the model's library references checked against the
 * local store at open and load. Warnings only; the recorded versions stand. */
async function libraryReferenceWarnings(model: PreviewModel): Promise<string> {
  publishLibraryRefFindings(model.project.id, []);
  try {
    const checked = await checkModelLibraryRefs(model.project.id, modelLibraryRefs(model));
    if (checked.route !== "tauri_backend" || checked.findings.length === 0) return "";
    publishLibraryRefFindings(model.project.id, checked.findings);
    return modelFileWarningSuffix(checked.findings.map((finding) => ({ code: finding.code, path: finding.entity_ref, message: finding.message })));
  } catch (error) {
    return ` Library references were not checked: ${String(error)}.`;
  }
}

// Diagnostics generations must not repeat across real same-page App remounts.
let nextUiModelPublicationGeneration = 0;

function formatPackageSaveError(error: unknown): string {
  if (error instanceof Error) return error.message;
  if (error && typeof error === "object") {
    try {
      return JSON.stringify(error);
    } catch {
      return "REPORT-PACKAGE-SAVE-FAILED: native error was not serializable";
    }
  }
  return String(error);
}

/**
 * The workspace session: the six state hooks, all thirteen effects and every
 * handler, in one closure and in the order `AppSession` declared them.
 * `AppSession` in `App.tsx` calls it once and renders what it returns; nothing
 * else calls it.
 *
 * The order is kept because it carries meaning. The results hook bumps the two
 * basis refs during render, before `ruleCheckRunBasis` and `dormantOutputBasis`
 * read them. The layout effect on `[model]` advances `modelRevision` and
 * invalidates the solve gate. The mount effect keeps the first render's closure
 * on purpose. `runMenuCommandRef` is assigned on every render, so the native
 * menu listener, registered once, runs the current `runMenuCommand`.
 * `nextUiModelPublicationGeneration` is module state beside `commitModel`, so a
 * generation does not repeat across remounts.
 *
 * It returns six slices: `model`, `selection`, `results`, `operations`,
 * `project` and `chrome`. Each holds only what the view reads. Apart from the
 * chrome setters, the setters handed out are the two visibility sets
 * (`setHiddenEntityKeys`, `setIsolationSelectionKeys`) and the two run options
 * (`setSolverMode`, `setReportPackagePrivateIntent`). No setter of the model,
 * of a result, of an operations cell or of a project cell leaves the session:
 * those change only in its effects and handlers, where the stale-response
 * guards and the paths that clear computed state sit together.
 */
export function useWorkspaceSession() {
  const {
    uiPreferences, setUiPreferences,
    setSystemDark,
    resolvedTheme,
    activeSection, setActiveSection,
    activatedExpensiveSections, setActivatedExpensiveSections,
    toolkitFocus, setToolkitFocus,
    propertyTaskRequestSequenceRef,
    propertyTaskRequest, setPropertyTaskRequest,
    openMenu, setOpenMenu,
    armedCreationTool, setArmedCreationTool,
    viewportViewCommandRef,
    workspaceShellRef,
    workspaceBudgetRef,
    narrowWindow, setNarrowWindow,
    treeCollapsed, setTreeCollapsed,
    inspectorCollapsed, setInspectorCollapsed,
    treeToggleRef,
    inspectorToggleRef,
    activeResizeCleanupRef,
    operationTab, setOperationTab,
    setR3JourneyState,
    reviewDetailsOpen, setReviewDetailsOpen,
    auditDrawerOpen, setAuditDrawerOpen,
    issuesDrawerOpen, setIssuesDrawerOpen,
    stageSurface, setStageSurface,
    stageViewMemory, setStageViewMemory
  } = useChromeSessionState();
  const {
    model, setModel,
    knowledge, setKnowledge,
    projectSessionGeneration, setProjectSessionGeneration,
    projectSessionGenerationRef,
    uiModelRevision, setUiModelRevision,
    uiModelRevisionRef,
    modelPublicationGenerationRef,
    modelAssignment, setModelAssignment,
    modelHash, setModelHash,
    modelRevision,
    currentModel,
    activeModelIndex
  } = useModelSessionState();
  // Chrome-only canonical comparison. A revision shortcut is used only for a
  // verified snapshot, or the untouched initial loaded-source snapshot (which
  // makes no claim of a file save). Later revisions need a current owned hash.
  const [savedModelBasis, setSavedModelBasis] = useState<{
    generation: number; revision: number; hash: string | null;
    source: "loaded-source" | "open" | "create" | "save";
  } | null>(null);
  const savedBasisSequence = useRef(0);
  // The open replace prompt, if a save onto a stored project id is waiting for the user.
  const [replaceProjectPrompt, setReplaceProjectPrompt] = useState<ReplaceProjectPromptState | null>(null);
  // While the prompt is open, menu commands and shell accelerators are ignored.
  const replacePromptOpenRef = useRef(false);
  // The prompts' shared hold on that flag: set until the last open prompt closes.
  const modalHolds = useRef<ModalHolds | null>(null);
  if (!modalHolds.current) modalHolds.current = createModalHolds(replacePromptOpenRef);
  const holdModal = () => modalHolds.current!.hold();
  // The open "Units at creation" dialog (W-17 §3), if a blank project is waiting
  // for its units. It is modal in the same way as the replace prompt.
  const [blankProjectUnitsRequest, setBlankProjectUnitsRequest] = useState<BlankProjectUnitsRequest | null>(null);
  const projectUnitsDialogOpenRef = useRef(false);
  // The open Save Model Document… dialog (DEL-15-01 W-6a), modal in the same way.
  const [modelDocumentSaveRequest, setModelDocumentSaveRequest] = useState<ModelDocumentSaveDialogRequest | null>(null);
  const modelDocumentSaveDialogOpenRef = useRef(false);
  // The open Save Handoff… dialog (DEL-15-01 W-6b), modal in the same way.
  const [handoffSaveRequest, setHandoffSaveRequest] = useState<HandoffSaveDialogRequest | null>(null);
  const handoffSaveDialogOpenRef = useRef(false);
  // The stored project this session is, at the revision it last opened or wrote:
  // its id and stored envelope hash. Set wherever an open or a write lands for
  // this project session, whether or not a later edit superseded the request,
  // so a save in place always carries the revision this session itself last saw.
  const storedBaseRef = useRef<{ projectId: string; value: string | null } | null>(null);
  function recordStoredBase(envelope: LocalProjectEnvelope) {
    storedBaseRef.current = { projectId: envelope.summary.project_id, value: envelope.project_envelope_hash?.value ?? null };
  }
  // Service fulfillment is our observable landed-write order, before canonical
  // verification can complete out of order. This is not a backend commit clock.
  const persistedWriteObservation = useRef(0);
  const latestVerifiedWriteObservation = useRef(0);
  // `modelRevision` is the model revision the hash was computed for (`modelRevision.current`).
  const modelHashOwner = useRef<{ generation: number; revision: number; modelRevision: number } | null>(null);
  const currentHashOwned = modelHashOwner.current?.generation === projectSessionGeneration &&
    modelHashOwner.current?.revision === uiModelRevision;
  const modelEdited = Boolean(model && isLocalModelEdited(savedModelBasis, projectSessionGeneration,
    uiModelRevision, currentHashOwned, modelHash));
  // The unsaved-changes guard reads the current notion when a command starts.
  const modelEditedRef = useRef(modelEdited);
  modelEditedRef.current = modelEdited;
  // The Save Local Project that landed, for the continuations that ran it
  // (the guard's "Save first" and Save Model State's prerequisite save).
  const projectSaveLanded = useRef<LandedProjectSave | null>(null);
  // What Save Model Document… saves: the session's current model and its hash,
  // only while that hash is owned by the current generation and revision.
  const modelDocumentSaveBasisRef = useRef<{ model: PreviewModel | null; modelHash: ModelHashEvidence | null }>({ model: null, modelHash: null });
  modelDocumentSaveBasisRef.current = { model, modelHash: currentHashOwned ? modelHash : null };

  const {
    selection, setPrimarySelection,
    orderedSelection, setOrderedSelection,
    orderedSelectionRef,
    hiddenEntityKeys, setHiddenEntityKeys,
    isolationSelectionKeys, setIsolationSelectionKeys,
    treePublication,
    handleTreePublication,
    selectedPipeRefs
  } = useSelectionSessionState();
  const {
    result, setResult,
    historicalRun, setHistoricalRun,
    currentSolvedResult,
    numericallyEligible,
    numericalHealth,
    numericalHealthHold,
    analysisRun, setAnalysisRun,
    resultBasisRef,
    analysisBasisRef,
    inputManifest, setInputManifest,
    ruleCheckAggregate, setRuleCheckAggregate,
    ruleCheckReportRun, heldRuleCheckRun, setRuleCheckReportRun,
    ruleCheckAggregateRef, ruleCheckReportRunRef,
    proposal, setProposal,
    selectedReviewTarget, setSelectedReviewTarget,
    solveJob, setSolveJob,
    solveProof, setSolveProof,
    running, setRunning,
    solverMode, setSolverMode,
    reportPackagePrivateIntent, setReportPackagePrivateIntent,
    reportPackageBusy, setReportPackageBusy,
    reportPackageRedaction, setReportPackageRedaction,
    reportPackageRoute, setReportPackageRoute,
    reportPackageRequestGenerationRef,
    reportPackageBusyGenerationRef,
    solveRunGate,
    ruleRevisionGate,
    currentSolvedResultRef,
    currentInputManifestRef,
    activeSolveJob,
    solveCancellationTombstones,
    comparison,
    comparisonUnavailable,
    packagedWithinRun,
    withinRun,
    droppedWithinRunBases,
    setHeldWithinRunSelection,
    setDroppedWithinRunBases
  } = useResultsSessionState();
  // Reference inspection is a transient view. Keep genuine persistence bytes
  // separate, scoped to the unchanged model/session, without retaining Current.
  const referencePersistence = useRef<{
    model: PreviewModel;
    generation: number;
    modelContent: string;
    history: HistoricalRunContext | null;
    result: MechanicsResult | null;
    analysisRun: AnalysisRunEnvelope | null;
  } | null>(null);
  function retainedReferencePersistence(requestModel: PreviewModel) {
    const retained = referencePersistence.current;
    try {
      return retained?.model === requestModel && retained.generation === projectSessionGenerationRef.current
        && retained.modelContent === checkedJsonText(requestModel) ? retained : null;
    } catch { return null; }
  }
  const {
    editorIntents, setEditorIntents,
    retainedReviewContext, setRetainedReviewContext,
    operationOutcomes, setOperationOutcomes,
    appliedOperations, setAppliedOperations,
    undoStack, setUndoStack,
    redoStack, setRedoStack,
    queuedBatches, setQueuedBatches,
    batchOutcomes, setBatchOutcomes,
    batchReceipts, setBatchReceipts,
    batchMessage, setBatchMessage,
    requestEpoch, setRequestEpoch,
    requestEpochRef,
    getPreparationEpoch,
    directDraftCommitToken, setDirectDraftCommitToken,
    batchSequence,
    operationBusy, setOperationBusy,
    operationMessage, setOperationMessage,
    historyFailure, setHistoryFailure,
    operationEngineStatus, setOperationEngineStatus,
    intentSequence,
    operationRequest,
    directDraftReviews,
    directDraftReviewSequence
  } = useOperationsSessionState();
  const {
    projectRequest, projectOperationOwner,
    storageCapability, setStorageCapability,
    projectSummary, setProjectSummary,
    projectIndex, setProjectIndex,
    modelHashIntegrity, setModelHashIntegrity,
    projectEnvelopeHash, setProjectEnvelopeHash,
    modelDocumentVersion, setModelDocumentVersion,
    projectEnvelopeHashIntegrity, setProjectEnvelopeHashIntegrity,
    projectMessage, setProjectMessage,
    projectOperation, setProjectOperation,
    projectBusy, setProjectBusy
  } = useProjectSessionState();

  // Run sheet S2 (DEL-07-02 Design `run-sheet-entry.md` §3.6): the session's
  // one transient event callback. A listener's failure outside a publication
  // is reported in the batch message and changes nothing else.
  const [sessionEvents] = useState(() => createSessionEventChannel((error, event) => {
    setBatchMessage(`The run sheet did not follow the session's ${event.type} event: ${nativeFailureText(error)}`);
  }));

  const ruleCheckRunBasis: RuleCheckRunBasis = {
    projectSessionGeneration,
    modelRevision: uiModelRevision,
    resultSequence: resultBasisRef.current.sequence
  };
  // Dormant output panels receive this key only when they reconcile again.
  // Thus accepted model/result changes do not wake an inactive full-model scan,
  // while the next activation remounts local packet/route state before paint.
  const dormantOutputBasis = `${uiModelRevision}:${resultBasisRef.current.sequence}:${analysisBasisRef.current.sequence}`;
  useEffect(() => {
    if (!activeSection || !EXPENSIVE_LIFECYCLE_SECTIONS.has(activeSection)) return;
    setActivatedExpensiveSections((current) => {
      if (current.has(activeSection)) return current;
      return new Set([...current, activeSection]);
    });
  }, [activeSection]);
  // The stage surface follows the one navigation cell: a page leaves it alone,
  // anything else becomes it. A presentation cell only; it reads and writes
  // nothing of the model, the results, the operations or the project.
  useEffect(() => {
    setStageSurface((current) => stageSurfaceAfter(current, activeSection));
    // A section summoned into the table pane is meant to be read: where the pane
    // is a collapsed drawer, summoning one opens the drawer.
    if (activeSection !== null && isStageSurface(activeSection)) setTreeCollapsed(false);
  }, [activeSection]);
  // Where the shell is: derived on every render, never stored. The ref serves
  // the listeners that are registered once (the keys, the native menu).
  const shellNow = shellLocation(activeSection, stageSurface);
  const stageViewNow = viewForStage(stageViewMemory, shellNow.stage);
  // Routing temporarily borrows the inspector without changing its remembered
  // open/closed state. A queued viewport intent keeps the same routing surface.
  const routingPanelActive = canvasAuthoringPanelActive(armedCreationTool, editorIntents);
  const routingInspectorRestore = useRef<boolean | null>(null);
  useLayoutEffect(() => {
    if (routingPanelActive) {
      if (routingInspectorRestore.current === null) routingInspectorRestore.current = inspectorCollapsed;
      setInspectorCollapsed(false);
    } else if (routingInspectorRestore.current !== null) {
      const restoreCollapsed = routingInspectorRestore.current;
      routingInspectorRestore.current = null;
      if (restoreCollapsed && document.getElementById("shell-inspector")?.contains(document.activeElement)) {
        workspaceShellRef.current?.querySelector<HTMLButtonElement>('[data-testid="workspace-select"]')?.focus();
      }
      setInspectorCollapsed(restoreCollapsed);
    }
  }, [routingPanelActive]);
  const shellNowRef = useRef({ location: shellNow, view: stageViewNow, stageSurface });
  shellNowRef.current = { location: shellNow, view: stageViewNow, stageSurface };
  const pageReturnFocusRef = useRef<HTMLElement | null>(null);
  const previousPageRef = useRef(shellNow.page);
  useLayoutEffect(() => {
    const wasOpen = previousPageRef.current !== null;
    previousPageRef.current = shellNow.page;
    if (!wasOpen || shellNow.page) return;
    const shell = workspaceShellRef.current;
    if (!shell) return;
    const available = (element: HTMLElement | null): element is HTMLElement => {
      if (!element?.isConnected || element.closest('[inert], [hidden], [aria-hidden="true"]') ||
          element.matches(":disabled") || element.getAttribute("aria-disabled") === "true") return false;
      const box = element.getBoundingClientRect();
      return box.width > 0 && box.height > 0 && getComputedStyle(element).visibility !== "hidden";
    };
    // A deliberate navigation control may already own visible focus. Otherwise
    // restore the pre-page opener, or a persistent visible stage/Select control.
    const focused = document.activeElement instanceof HTMLElement ? document.activeElement : null;
    if (focused !== document.body && available(focused)) return;
    const preferred = pageReturnFocusRef.current;
    const stage = shell.querySelector<HTMLElement>(`[data-testid="rail-stage-${shellNow.stage}"]`);
    const select = shell.querySelector<HTMLElement>('[data-testid="workspace-select"]');
    (available(preferred) ? preferred : available(stage) ? stage : select)?.focus();
  }, [shellNow.page, shellNow.stage]);
  useEffect(() => {
    const update = () => setNarrowWindow(window.innerWidth < 1280);
    window.addEventListener("resize", update);
    return () => window.removeEventListener("resize", update);
  }, []);
  useLayoutEffect(() => {
    if (!toolkitFocus) return;
    const target = toolkitFocus.elementId ? document.getElementById(toolkitFocus.elementId) : document.querySelector<HTMLElement>(`[data-testid="${toolkitFocus.testId}"]`);
    // Reveal contextual details before transferring focus from command search.
    for (let parent = target?.parentElement; parent; parent = parent.parentElement) {
      if (parent instanceof HTMLDetailsElement) parent.open = true;
    }
    target?.focus();
    target?.scrollIntoView?.({ block: "nearest" });
  }, [toolkitFocus]);
  useLayoutEffect(() => {
    const workspace = workspaceBudgetRef.current;
    if (!model || !workspace) return;
    return observeWorkspaceCanvasBudget(workspace);
  }, [Boolean(model)]);
  const viewportVisibility = useMemo(
    () => activeModelIndex
      ? deriveViewportVisibility(activeModelIndex, hiddenEntityKeys, isolationSelectionKeys)
      : { hiddenKeys: new Set<EntityKey>(), dimmedKeys: new Set<EntityKey>(), hiddenCount: 0, isolationActive: isolationSelectionKeys !== null },
    [activeModelIndex, hiddenEntityKeys, isolationSelectionKeys]
  );

  function handleClearVisibility() {
    setHiddenEntityKeys(new Set());
    setIsolationSelectionKeys(null);
  }

  useEffect(() => {
    if (!activeModelIndex) return;
    setHiddenEntityKeys((current) => {
      const next = new Set([...current].filter((key) => activeModelIndex.entities.has(key)));
      return next.size === current.size ? current : next;
    });
    setIsolationSelectionKeys((current) => {
      if (current === null) return current;
      const next = new Set([...current].filter((key) => activeModelIndex.entities.has(key)));
      return next.size === current.size ? current : next;
    });
  }, [activeModelIndex]);

  useEffect(() => {
    writeUiPreferences(uiPreferences);
  }, [uiPreferences]);

  useEffect(() => () => activeResizeCleanupRef.current?.(), []);

  // The design tokens (tokens.css) are scoped on :root[data-theme]; the document root follows the
  // resolved theme so they hold for the shell and for anything rendered outside it.
  useLayoutEffect(() => {
    const root = document.documentElement;
    const previous = root.getAttribute("data-theme");
    root.setAttribute("data-theme", resolvedTheme);
    return () => {
      if (previous === null) root.removeAttribute("data-theme");
      else root.setAttribute("data-theme", previous);
    };
  }, [resolvedTheme]);

  useEffect(() => {
    if (typeof window.matchMedia !== "function") return;
    const query = window.matchMedia("(prefers-color-scheme: dark)");
    const update = () => setSystemDark(query.matches);
    query.addEventListener?.("change", update);
    return () => query.removeEventListener?.("change", update);
  }, []);

  function commitSelectionState(next: OrderedSelectionState, fallbackModel: PreviewModel | null = model): boolean {
    const previous = orderedSelectionRef.current;
    const membershipChanged = !sameSelection(previous, next);
    if (!membershipChanged && previous.focusKey === next.focusKey && previous.rangeAnchorKey === next.rangeAnchorKey) return false;
    orderedSelectionRef.current = next;
    setOrderedSelection(next);
    if (membershipChanged) {
      invalidateDirectDraftContext();
      if (fallbackModel) setPrimarySelection(primarySelection(next, defaultSelection(fallbackModel)));
      else setPrimarySelection(next.primaryKey ? primarySelection(next, { type: "project", id: "" }) : null);
    }
    return membershipChanged;
  }

  function setSelection(next: EntityRef | null): void {
    if (!next) {
      const previous = orderedSelectionRef.current;
      const empty = emptySelection(orderedSelectionRef.current.preparationEpoch + 1);
      orderedSelectionRef.current = empty;
      setOrderedSelection(empty);
      setPrimarySelection(null);
      if (!sameSelection(previous, empty)) invalidateDirectDraftContext();
      return;
    }
    commitSelectionState(singletonSelection(next, orderedSelectionRef.current));
  }

  useEffect(() => {
    let active = true;
    Promise.all([loadPreviewModel(), loadDesignKnowledge(), getLocalStorageCapability()]).then(
      ([loadedModel, loadedKnowledge, loadedStorageCapability]) => {
        if (!active) return;
        advanceProjectSession();
        commitModel(loadedModel);
        const generation = projectSessionGenerationRef.current;
        const revision = uiModelRevisionRef.current;
        const sequence = ++savedBasisSequence.current;
        setSavedModelBasis({ generation, revision, hash: null, source: "loaded-source" });
        computeModelHash(loadedModel).then((hash) => {
          if (active && generation === projectSessionGenerationRef.current && sequence === savedBasisSequence.current) {
            setSavedModelBasis({ generation, revision, hash: hash?.value ?? null, source: "loaded-source" });
          }
        }).catch(() => {
          // Keep only the untouched loaded-source revision. No saved-file claim
          // or canonical equality for a later revision follows from this failure.
        });
        setKnowledge(loadedKnowledge);
        setSelection(defaultSelection(loadedModel));
        setStorageCapability(loadedStorageCapability);
      }
    );
    return () => {
      active = false;
    };
  }, []);

  useLayoutEffect(() => {
    let active = true;
    const retained = referencePersistence.current;
    if (retained && (retained.model !== model || retained.generation !== projectSessionGenerationRef.current)) referencePersistence.current = null;
    modelRevision.current += 1;
    // Run sheet S2 (§3.6 step 1): a registration prepared on an earlier model is retired.
    retireStaleBatchRegistrations();
    solveRunGate.current.invalidate();
    activeSolveJob.current = null;
    setRunning(false);
    setSolveProof(null);
    setModelHash(null);
    if (!model) return;
    const generation = projectSessionGenerationRef.current;
    const revision = uiModelRevisionRef.current;
    const counted = modelRevision.current;
    computeModelHash(model).then((hash) => {
      if (active && currentModel.current === model && generation === projectSessionGenerationRef.current && revision === uiModelRevisionRef.current) {
        modelHashOwner.current = { generation, revision, modelRevision: counted };
        setModelHash(hash);
      }
    }).catch(() => { /* An unavailable current hash cannot prove a clean comparison. */ });
    return () => {
      active = false;
    };
  }, [model]);

  // Native result custody (DEL-04-07): the session publishes a delivered result
  // only through `setResult`, so the result it stops holding (replaced by a new
  // solve, cleared by model edits, undo/redo, project changes or reference
  // inspection) is released to the native custody ledger here, as is the held
  // result when the session ends.
  const heldResultRef = useRef<MechanicsResult | null>(null);
  // A new webview session holds no delivered result, so whatever the native
  // host still retains or counts as held by an earlier page is released once,
  // before any solve can start (a start waits for it). Tauri runtime only; a
  // failure never blocks the session.
  useEffect(() => { void beginSessionResultCustodyReset(); }, []);
  useEffect(() => {
    const previous = heldResultRef.current;
    heldResultRef.current = result;
    if (previous && previous !== result) void disposeDeliveredMechanicsResult(previous);
  }, [result]);
  useEffect(() => () => { void disposeDeliveredMechanicsResult(heldResultRef.current); }, []);

  // Advanced by every commit of the session's model (applied operations, undo/redo,
  // opens and creates), and by nothing else. A pending New Blank checks it rather
  // than the request epoch, which selection and draft invalidation also advance:
  // only a change to the model or project on screen supersedes the blank.
  const modelCommitEpochRef = useRef(0);

  // A model commit is split so that an apply path can order it as Prepare,
  // Publish, Notify: `prepareModelPublication` holds the fallible work and
  // changes nothing; `publishModel` only assigns session state and
  // session-owned refs; `retireViewportBoxGesture` calls out to the viewport.
  // `commitModel` keeps the earlier behaviour for every other caller: the
  // viewport is told first, so its failure still precedes publication.
  type ModelPublication = Readonly<{ model: PreviewModel; identityHash: string }>;

  function prepareModelPublication(nextModel: PreviewModel): ModelPublication {
    return { model: nextModel, identityHash: uiModelIdentityHash(nextModel) };
  }

  function retireViewportBoxGesture() {
    viewportViewCommandRef.current?.({ type: "retire-box-gesture" });
  }

  // Notify for an apply, undo or redo path: the viewport's failure is returned
  // for the caller to report beside its message; the publication stands.
  function retireViewportBoxGestureAfterPublication(): string | null {
    try {
      retireViewportBoxGesture();
      return null;
    } catch (error) {
      return `The viewport did not retire its box gesture: ${nativeFailureText(error)}`;
    }
  }

  // Prepare for a publication: the ordered selection pruned to the entities of
  // `nextModel`, under the index generation `publishModel` assigns, as
  // `preserveAndPruneSelection` would build it after the commit.
  function prunedSelectionForPublication(nextModel: PreviewModel): OrderedSelectionState {
    const nextIndex = modelIndexFor(nextModel, projectSessionGenerationRef.current, uiModelRevisionRef.current + 1);
    return pruneSelection(
      orderedSelectionRef.current,
      new Set(nextIndex.entities.keys()),
      { type: "project", id: nextModel.project.id }
    );
  }

  function commitModel(nextModel: PreviewModel, directDraftToken: string | null = null) {
    retireViewportBoxGesture();
    publishModel(prepareModelPublication(nextModel), directDraftToken);
  }

  function publishModel(prepared: ModelPublication, directDraftToken: string | null = null) {
    const { model: nextModel, identityHash } = prepared;
    modelCommitEpochRef.current += 1;
    // A later model supersedes an earlier undo or redo failure.
    setHistoryFailure(null);
    referencePersistence.current = null;
    modelHashOwner.current = null;
    invalidateReportPackageComputedState();
    const assignmentStartedAt = performance.now();
    const modelPublicationGeneration = ++nextUiModelPublicationGeneration;
    publishUiModelAssignmentStarted(modelPublicationGeneration, assignmentStartedAt);
    const nextUiModelRevision = uiModelRevisionRef.current + 1;
    const indexGeneration = `${projectSessionGenerationRef.current}:${nextUiModelRevision}`;
    setModelAssignment({
      status: "started",
      generation: modelPublicationGeneration,
      indexGeneration,
      identityHash,
      startedAt: assignmentStartedAt,
      committedAt: null
    });
    requestEpochRef.current += 1;
    setRequestEpoch(requestEpochRef.current);
    setDirectDraftCommitToken(directDraftToken);
    uiModelRevisionRef.current = nextUiModelRevision;
    setUiModelRevision(nextUiModelRevision);
    currentModel.current = nextModel;
    setHistoricalRun(null);
    operationRequest.current.sequence += 1;
    operationRequest.current.busy = false;
    directDraftReviews.current.clear();
    setOperationBusy(false);
    commitModelAfterSolveInvalidation(solveRunGate.current, modelRevision, () => {
      modelPublicationGenerationRef.current = modelPublicationGeneration;
      activeSolveJob.current = null;
      setRunning(false);
      setSolveProof(null);
      setModelHash(null);
      setModelAssignment({
        status: "committed",
        generation: modelPublicationGeneration,
        indexGeneration,
        identityHash,
        startedAt: assignmentStartedAt,
        committedAt: performance.now()
      });
      setModel(nextModel);
    });
  }

  function preserveAndPruneSelection(nextModel: PreviewModel) {
    const nextIndex = modelIndexFor(
      nextModel,
      projectSessionGenerationRef.current,
      uiModelRevisionRef.current
    );
    commitSelectionState(
      pruneSelection(
        orderedSelectionRef.current,
        new Set(nextIndex.entities.keys()),
        { type: "project", id: nextModel.project.id }
      ),
      nextModel
    );
  }

  function advanceProjectSession(): void {
    viewportViewCommandRef.current?.({ type: "cancel-box-selection" });
    invalidateReportPackageComputedState();
    const nextGeneration = ++projectSessionGenerationRef.current;
    setProjectSessionGeneration(nextGeneration);
    setHiddenEntityKeys(new Set());
    setIsolationSelectionKeys(null);
    setPropertyTaskRequest(null);
  }

  // Warm up the operation engine and report its honest route/readiness.
  // Browser mode lazily loads the wasm32 operation_applier build; an absent
  // artifact surfaces as an explicit unavailable status, never a fallback.
  useEffect(() => {
    let active = true;
    warmupOperationEngine().then((status) => {
      if (active) setOperationEngineStatus(status);
    });
    return () => {
      active = false;
    };
  }, []);

  function dispatchActiveSolveCancellation(runGeneration: number) {
    const active = activeSolveJob.current;
    const tombstone = solveCancellationTombstones.current.get(runGeneration);
    if (
      !active ||
      active.generation !== runGeneration ||
      active.cancellation_dispatched ||
      !tombstone?.requested ||
      tombstone.dispatched ||
      !solveRunGate.current.isCurrent(runGeneration) ||
      active.job.backend_job_seam !== "tauri_backend_job" ||
      !active.job.backend_job_id
    ) return;
    active.cancellation_dispatched = true;
    tombstone.dispatched = true;
    void cancelPreviewMechanicsJob(
      active.job.backend_job_id,
      active.job.backend_cancellation_token
    )
      .then((receipt) => {
        if (
          !solveRunGate.current.isCurrent(runGeneration) ||
          receipt.job_id !== active.job.job_id
        ) return;
        setSolveJob((current) =>
          current.job_id === active.job.job_id
            ? recordBackendCancellationReceipt(current, receipt)
            : current
        );
      })
      .catch((error) => {
        if (!solveRunGate.current.isCurrent(runGeneration)) return;
        setSolveJob((current) =>
          current.job_id === active.job.job_id
            ? recordBackendCancellationFailure(current, error)
            : current
        );
      });
  }

  async function handleInspectBundledReference() {
    if (!model) return;
    if (result || analysisRun || historicalRun?.designation === "historical_saved_run"
      || !retainedReferencePersistence(model)) {
      referencePersistence.current = {
        model, generation: projectSessionGenerationRef.current, modelContent: checkedJsonText(model),
        history: historicalRun?.designation === "historical_saved_run" ? structuredClone(historicalRun) : null,
        result: result ? structuredClone(result) : null,
        analysisRun: analysisRun ? structuredClone(analysisRun) : null,
      };
    }
    // Retire any pending backend publication before loading the separate example.
    handleCancelRun();
    solveRunGate.current.invalidate();
    activeSolveJob.current = null;
    const referenceGeneration = solveRunGate.current.tryStart()!;
    setRunning(false);
    setSolveProof(null);
    invalidateReportPackageComputedState();
    ruleRevisionGate.current.invalidate();
    setHistoricalRun(null);
    setResult(null); setAnalysisRun(null); setInputManifest(null);
    setRuleCheckAggregate(null); setSolveJob(initialSolveJob());
    // Review proposals and selected review context remain the user's work;
    // only current mechanics qualification is retired by reference inspection.
    try {
      const reference = await loadBundledMechanicsReference(solverMode);
      if (!solveRunGate.current.isCurrent(referenceGeneration)) return;
      setHistoricalRun(buildBundledReferenceContext(reference));
      setActiveSection("results");
    } finally {
      solveRunGate.current.finish(referenceGeneration);
    }
  }

  async function handleRun(): Promise<void> { await handleRunWithAgentReceipt(); }

  async function handleRunWithAgentReceipt(): Promise<AgentRunReceipt | undefined> {
    const runGeneration = solveRunGate.current.tryStart();
    if (runGeneration === null) return;
    invalidateReportPackageComputedState();
    ruleRevisionGate.current.invalidate();
    solveCancellationTombstones.current.set(runGeneration, {
      requested: false,
      dispatched: false
    });
    setRunning(true);
    setSolveProof(null);
    setResult(null);
    setAnalysisRun(null);
    setInputManifest(null);
    // A fresh solve invalidates any prior rule-check run against the old result.
    setRuleCheckAggregate(null);
    let startedJob: SolveJobAuditState | null = null;
    // A delivered result this run did not publish is released in `finally`.
    let deliveredOutput: MechanicsResult | null = null;
    // A started native job whose result this run has neither taken nor
    // released; `finally` releases it, so no path leaves it retained natively.
    // `completed` records that the job was seen completed (its result awaits a take).
    let unsettledJob: { jobId: string; token: string; completed: boolean } | null = null;
    let publishedOutput = false;
    try {
      if (!model) {
        throw new Error(
          "INPUT-MANIFEST-MODEL-INCOMPLETE: a current session model is required before solve."
        );
      }
      // Keep the caller representation in the manifest (including -0). The
      // native service separately captures the exact serialized dispatch.
      const solveModel = structuredClone(model);
      const solveModelRevision = modelRevision.current;
      const solveModelHash = await computeModelHash(solveModel);
      if (
        !solveModelHash ||
        modelRevision.current !== solveModelRevision ||
        !solveRunGate.current.isCurrent(runGeneration)
      ) return;
      if (
        solveRunGate.current.isCancellationRequested(runGeneration) ||
        solveCancellationTombstones.current.get(runGeneration)?.requested
      ) {
        setSolveJob(cancelledBeforeBackendStartSolveJob(solveModel));
        return;
      }
      // Capture the original live caller representation as well as dispatched JSON.
      let startReceipt: Awaited<ReturnType<typeof startPreviewMechanicsJob>>;
      try {
        startReceipt = await startPreviewMechanicsJob(model, solverMode);
      } catch (error) {
        // A start the native memory pool refuses is a typed refusal, recorded as such.
        if (error instanceof ResourceUnavailableError) {
          if (solveRunGate.current.isCurrent(runGeneration)) setSolveJob(refusedBeforeBackendStartSolveJob(solveModel, error));
          return;
        }
        throw error;
      }
      // Reference records never create a fresh solve. Only a real backend job
      // can publish current result/manifest/proof cells through this path.
      if (startReceipt.mode !== "backend_job") {
        throw new Error("SOLVE_BACKEND_INVOCATION_REQUIRED: a reference-only receipt cannot publish Current mechanics.");
      }
      unsettledJob = { jobId: startReceipt.job_id, token: startReceipt.backend_cancellation_token, completed: false };
      const cancellationTombstone = solveCancellationTombstones.current.get(runGeneration);
      if (
        modelRevision.current !== solveModelRevision ||
        !solveRunGate.current.isCurrent(runGeneration)
      ) {
        // The originating generation is already detached from visible UI: the
        // started job is abandoned in `finally` (cancellation, then release of
        // anything it retains); a failed best effort must not resurrect stale state.
        if (cancellationTombstone) cancellationTombstone.dispatched = true;
        return;
      }
      if (startReceipt.mode !== "backend_job") throw new Error("BROWSER_REFERENCE_RECEIPT_NOT_A_CURRENT_SOLVE");
      startedJob = startSolveJob(solveModel, startReceipt);
      const cancellationRequested =
        solveRunGate.current.isCancellationRequested(runGeneration) ||
        cancellationTombstone?.requested === true;
      const visibleStartedJob = cancellationRequested
        ? requestSolveCancellation(startedJob)
        : startedJob;
      activeSolveJob.current = {
        generation: runGeneration,
        job: visibleStartedJob,
        cancellation_dispatched: false
      };
      setSolveJob(visibleStartedJob);
      if (cancellationRequested) {
        if (startReceipt.mode === "backend_job") {
          dispatchActiveSolveCancellation(runGeneration);
        } else {
          setSolveJob(cancelledWithoutBackendSolveJob(visibleStartedJob));
          return;
        }
      }
      let output: MechanicsResult;
      if (startReceipt.mode === "backend_job") {
        const visibleJobId = startedJob.job_id;
        const terminal = await awaitBackendSolveJob(startReceipt.job_id, (status) => {
          // Show the native state while the job waits, including its queue reason.
          if (!solveRunGate.current.isCurrent(runGeneration)) return;
          setSolveJob((current) => current.job_id === visibleJobId ? progressSolveJob(current, status) : current);
        });
        // A completed job's result awaits a take; any other terminal job retains none.
        if (terminal.job_id === startReceipt.job_id) {
          if (terminal.state === "completed") unsettledJob.completed = true;
          else unsettledJob = null;
        }
        // A superseded run's completed result is released from native retention unread (`finally`).
        if (!solveRunGate.current.isCurrent(runGeneration)) return;
        if (terminal.job_id !== startedJob.job_id) {
          throw new Error(
            `SOLVE-JOB-IDENTITY-MISMATCH: expected ${startedJob.job_id}; received ${terminal.job_id}`
          );
        }
        if (terminal.state === "cancelled") {
          setSolveJob((current) =>
            current.job_id === startedJob?.job_id
              ? cancelledSolveJob(current, terminal)
              : current
          );
          return;
        }
        if (terminal.state === "refused" && terminal.resource_refusal) {
          const refusal = terminal.resource_refusal;
          setSolveJob((current) =>
            current.job_id === startedJob?.job_id
              ? refusedSolveJob(current, refusal)
              : current
          );
          return;
        }
        if (terminal.state !== "completed") throw terminalJobError(terminal);
        // The poll carries no result: take the producer's bytes. A refused take
        // (custody_full, or headroom for the handoff copy) is recorded as a typed
        // refusal at the take; the session does not retry a failed take, so
        // `finally` releases the retained result.
        try {
          output = await takePreviewMechanicsJobResult(startReceipt.job_id);
        } catch (error) {
          if (!(error instanceof ResourceUnavailableError)) throw error;
          if (solveRunGate.current.isCurrent(runGeneration)) {
            setSolveJob((current) =>
              current.job_id === startedJob?.job_id ? refusedAtTakeSolveJob(current, error) : current
            );
          }
          return;
        }
        deliveredOutput = output;
        unsettledJob = null;
      } else {
        throw new Error("SOLVE_BACKEND_INVOCATION_REQUIRED: browser references are not completed solve results.");
      }
      if (!hasNativeMechanicsInvocation(output, solveModel, solverMode)) {
        throw new Error("SOLVE_NATIVE_INVOCATION_BINDING_REQUIRED: the received result is not bound to this actual native model/mode invocation.");
      }
      if (!hasCurrentSourceContract(output) || !output.producer) {
        throw new Error("SOLVE-PRODUCER-CONTRACT-UNSUPPORTED: a fresh result requires a recognized current producer contract; historical and unsupported carriers remain available only through their inspection routes.");
      }
      // The model's rule-pack references, resolved against the local store now
      // (identity only: nothing here reaches the solve, and no check is run).
      // A model without references makes no store call and keeps `[]`.
      const rulePacks = solveModel.rule_pack_refs?.length
        ? await resolveModelRulePacks(solveModel)
        : NO_RULE_PACK_RESOLUTION;
      if (!solveRunGate.current.isCurrent(runGeneration)) return;
      const manifest = await buildCurrentSessionInputManifest({
        model: solveModel,
        solver: {
          solver_name: output.producer.component_name,
          solver_version: output.producer.component_version,
          solver_build_ref: `${output.producer.component_name}@${output.producer.component_version}`,
          solver_mode: solverMode,
          settings: {
            nonlinear_iteration_policy:
              "DEC-046-CV-B-product-preview-active-set-count-v1",
            sparse_evidence_lane: solverMode === "sparse_interactive"
          }
        },
        active_rule_packs: rulePacks.active_rule_packs,
        external_assets: []
      });
      if (!solveRunGate.current.isCurrent(runGeneration)) return;
      // References left out of active_rule_packs become the record's diagnostics.
      const runRecord = await buildAnalysisRunPreview(output, {
        inputManifest: manifest,
        rulePackExclusions: rulePacks.excluded
      });
      if (
        modelRevision.current !== solveModelRevision ||
        !solveRunGate.current.isCurrent(runGeneration)
      ) return;
      if (output.model_ref !== solveModel.project.id) {
        throw new Error(
          `SOLVE-RESULT-MODEL-MISMATCH: expected ${solveModel.project.id}; received ${output.model_ref}`
        );
      }
      setSolveJob((current) =>
        current.job_id === startedJob?.job_id
          ? completeSolveJob(current, output, runRecord)
          : current
      );
      referencePersistence.current = null;
      setHistoricalRun(null);
      publishedOutput = true;
      setResult(output);
      setSelectedReviewTarget(null);
      setProposal(null);
      setInputManifest(manifest);
      setAnalysisRun(runRecord);
      setModelHash(solveModelHash);
      setSolveProof({
        state: "completed",
        run_generation: runGeneration,
        job_id: startedJob.job_id,
        backend_job_seam: startedJob.backend_job_seam,
        project_ref: solveModel.project.id,
        model_sha256: solveModelHash.value,
        input_manifest_sha256: manifest.manifest_sha256,
        result_run_id: output.run_id,
        result_model_ref: output.model_ref,
        result_row_count: output.results.length
      });
      return { jobId: startedJob.job_id, runId: output.run_id, modelHash: solveModelHash,
        solverMode, health: output.status.mechanics };
    } catch (error) {
      if (solveRunGate.current.isCurrent(runGeneration)) {
        setSolveJob((current) =>
          !startedJob || current.job_id === startedJob.job_id
            ? failSolveJob(current, error)
            : current
        );
      }
    } finally {
      if (deliveredOutput && !publishedOutput) void disposeDeliveredMechanicsResult(deliveredOutput);
      if (unsettledJob?.completed) void discardPreviewMechanicsJobResult(unsettledJob.jobId);
      else if (unsettledJob) void abandonPreviewMechanicsJob(unsettledJob.jobId, unsettledJob.token);
      solveCancellationTombstones.current.delete(runGeneration);
      if (activeSolveJob.current?.generation === runGeneration) {
        activeSolveJob.current = null;
      }
      if (solveRunGate.current.finish(runGeneration)) setRunning(false);
    }
  }

  // Record (or clear) the GUI rule-check aggregate in the app-held analysis-run
  // envelope (TP-C4-APPAGG-001). Rebuilding re-derives only the
  // analysis_run_record status/hash and analysis_status; the embedded
  // result_envelope hash still binds the raw solve, so the hash-bound solve
  // envelope is never mutated. With no solved result there is no app-held
  // envelope to annotate.
  async function handleRuleCheckAggregate(
    aggregate: RuleCheckStatus | null,
    renderedBasis: Readonly<{
      projectSessionGeneration: number;
      modelRevision: number;
      result: MechanicsResult | null;
      inputManifest: CurrentSessionInputManifestEvidence | null;
    }>,
    run: SessionRuleCheckRun | null = null
  ) {
    const renderedBasisIsCurrent = () =>
      projectSessionGenerationRef.current === renderedBasis.projectSessionGeneration &&
      uiModelRevisionRef.current === renderedBasis.modelRevision &&
      currentSolvedResultRef.current === renderedBasis.result &&
      currentInputManifestRef.current === renderedBasis.inputManifest;
    if (!renderedBasisIsCurrent()) return;
    // The report reads the run only while its aggregate is the current one.
    const previousRun = heldRuleCheckRun;
    const nextRun = aggregate !== null && run?.result.aggregate_status === aggregate ? run : null;
    setRuleCheckReportRun(nextRun);
    // A different run makes the previously assembled report package stale, even
    // under the same aggregate (another pack or other outcomes; DEL-08-01 Design
    // `report-package-current-results.md` §2.5), so this comes before the early
    // return. The private-package intent remains an independent user choice.
    const runChanged = nextRun !== previousRun;
    if (runChanged) invalidateReportPackageComputedState();
    if (aggregate === ruleCheckAggregate) return;
    const previousAggregate = ruleCheckAggregate;
    const revision = ruleRevisionGate.current.start();
    // A different aggregate immediately makes the previously assembled report
    // package stale. Clear its computed route before publishing the new rule
    // state.
    if (!runChanged) invalidateReportPackageComputedState();
    setRuleCheckAggregate(aggregate);
    if (!currentSolvedResult || !inputManifest) return;
    const capturedResult = currentSolvedResult;
    const capturedManifest = inputManifest;
    // The solve-time record's rule-pack reference diagnostics carry over to the revised record.
    const capturedRulePackExclusions = recordRulePackExclusions(analysisRun, inputManifest.manifest, currentSolvedResult.diagnostics.length);
    const capturedModelRevision = modelRevision.current;
    const capturedSolveGeneration = solveRunGate.current.current();
    const stillCurrent = () =>
      ruleRevisionGate.current.isCurrent(revision) &&
      modelRevision.current === capturedModelRevision &&
      solveRunGate.current.current() === capturedSolveGeneration &&
      currentSolvedResultRef.current === capturedResult &&
      currentInputManifestRef.current === capturedManifest &&
      currentModel.current?.project.id === capturedResult.model_ref &&
      renderedBasisIsCurrent();
    try {
      const revisedRecord = await buildAnalysisRunPreview(capturedResult, {
          inputManifest: capturedManifest,
          ruleCheckAggregate: aggregate,
          rulePackExclusions: capturedRulePackExclusions
      });
      if (!stillCurrent()) return;
      setAnalysisRun(revisedRecord);
    } catch {
      if (!stillCurrent()) return;
      // Recording the aggregate failed (e.g. hashing unavailable); keep the
      // solve-time analysis-run envelope rather than surfacing a false outcome.
      setRuleCheckAggregate(previousAggregate);
      setRuleCheckReportRun(previousRun);
    }
  }

  function recordR3JourneyEvent(event: R3JourneyEvent) {
    setR3JourneyState((current) => {
      if (current[event]) return current;
      return { ...current, [event]: true };
    });
  }

  function handleCancelRun() {
    const runGeneration = solveRunGate.current.current();
    if (runGeneration === null) return;
    if (!solveRunGate.current.requestCancellation(runGeneration)) return;
    const tombstone = solveCancellationTombstones.current.get(runGeneration);
    if (tombstone) tombstone.requested = true;
    const active = activeSolveJob.current;
    if (!active || active.generation !== runGeneration) {
      setSolveJob((current) => pendingBackendStartCancellationSolveJob(current));
      return;
    }
    active.job = requestSolveCancellation(active.job);
    setSolveJob((current) =>
      current.job_id === active.job.job_id
        ? requestSolveCancellation(current)
        : current
    );
    if (active.job.backend_job_seam === "tauri_backend_job") {
      dispatchActiveSolveCancellation(runGeneration);
    } else {
      setSolveJob(cancelledWithoutBackendSolveJob(active.job));
    }
  }

  async function handleProposal() {
    setProposal(await loadSampleProposal(result, selectedReviewTarget));
  }

  function handleQueueEditorIntent(intent: EditorOperationIntent) {
    intentSequence.current += 1;
    setEditorIntents((current) => [
      {
        ...intent,
        queue_id: `editor-intent-${intentSequence.current}`
      },
      ...current
    ]);
    setActiveSection("operations");
    setOperationTab("review");
  }

  function handleClearReviewQueue() {
    requestEpochRef.current += 1;
    setRequestEpoch(requestEpochRef.current);
    withdrawBatchRegistrations();
    setQueuedBatches([]);
    setBatchOutcomes({});
    setBatchMessage("Pending batches cleared. Running requests will not change this session.");
    // Withdrawal invalidates callbacks synchronously, including the hash waits
    // in apply. An older response or finally block cannot revive this queue.
    operationRequest.current.sequence += 1;
    operationRequest.current.busy = false;
    setOperationBusy(false);
    setEditorIntents([]);
    setProposal(null);
    setOperationOutcomes({});
    setOperationMessage("Pending changes cleared. Requests already running will not change this session.");
  }

  // W-10: the live registry of queued submissions. A run resolves its batch
  // here (never from render-time state or the caller's entry), bound to the
  // queue epoch it was registered in. Every withdrawal (clear, new, open or
  // replaced project) revokes all registrations synchronously, with the
  // canonical fingerprint and outcome of their validation, and moves the
  // epoch. (The request epoch is not used: it also moves on every selection
  // change, which would strand queued batches whenever a ref is selected.)
  const batchRegistrations = useRef(new Map<string, BatchRegistration>());
  const batchQueueEpoch = useRef(0);
  function withdrawBatchRegistrations() {
    const withdrawn = [...batchRegistrations.current.values()];
    batchRegistrations.current.clear();
    batchQueueEpoch.current += 1;
    for (const { entry } of withdrawn) sessionEvents.emit({ type: "withdrawn", batchId: entry.batch.batch_id, key: entry.key });
  }
  // Run sheet S2 (DEL-07-02 Design `run-sheet-entry.md` §3.6 step 1): after the
  // revision advances, every registration prepared on another revision is
  // revoked, whatever its producer (none of them could run). Its Pending
  // changes entry becomes a retired notice whose only action is Dismiss, and
  // `invalidated` is emitted once per registration. An applied batch is
  // deregistered in its own Publish block, so it is never retired here.
  function retireStaleBatchRegistrations() {
    const stale = [...batchRegistrations.current.values()].filter(({ entry }) => entry.basisRevision !== modelRevision.current);
    if (stale.length === 0) return;
    const keys = new Set(stale.map(({ entry }) => entry.key));
    for (const key of keys) batchRegistrations.current.delete(key);
    setQueuedBatches((current) => current.map((entry) => keys.has(entry.key) && !entry.retired ? { ...entry, retired: RETIRED_BATCH_NOTICE } : entry));
    for (const { entry } of stale) sessionEvents.emit({ type: "invalidated", batchId: entry.batch.batch_id, key: entry.key, reason: RETIRED_BATCH_NOTICE });
  }
  function handleDismissRetiredBatch(key: string) {
    setQueuedBatches((current) => current.filter((entry) => !(entry.key === key && entry.retired)));
    setBatchOutcomes((current) => {
      if (!(key in current)) return current;
      const { [key]: _dismissed, ...rest } = current;
      return rest;
    });
  }

  const agentApplyingRef = useRef(new Set<string>());
  const agentProposalStandingRef = useRef(new Map<string, {status:"pending_review"|"withdrawn"|"applied"|"unknown";outcomeModelHash:ModelHashEvidence|null}>());
  useEffect(() => sessionEvents.listen(event => {
    if (event.type !== "withdrawn" && event.type !== "abandoned" && event.type !== "invalidated") return;
    const retained = agentProposalStandingRef.current.get(event.key);
    if (!retained || retained.status === "applied") return;
    return () => { retained.status = event.type === "withdrawn" ? "withdrawn" : "unknown"; };
  }), [sessionEvents]);

  async function handleQueueOperationBatch(batch: OperationBatch, options: { importContext?: ImportContext } = {}): Promise<void> {
    await registerOperationBatch(batch, options.importContext ? { importContext: options.importContext } : {});
  }

  /** Requeue a stored record with its author re-derived host-side (DEL-16-03).
   * Returns the refusal, if any, for display beside the stored record. */
  async function handleRequeueRetainedRecord(intent: unknown, index: number): Promise<string | null> {
    const result = requeueRetainedRecord(intent, index);
    if ("refused" in result) { setBatchMessage(`Record could not be requeued: ${result.refused}`); return result.refused; }
    await registerOperationBatch(result.batch);
    return null;
  }

  /** Queue a batch and return its registration key, or null when it was not registered.
   * `reveal: false` (the run sheet, §5.1) leaves the section and focus where they are. */
  async function registerOperationBatch(batch: OperationBatch, options: { reveal?: boolean; agentContext?: AgentContext; importContext?: ImportContext } = {}): Promise<string | null> {
    if (!model) return null;
    const revision = modelRevision.current;
    const epoch = requestEpochRef.current;
    const queueEpoch = batchQueueEpoch.current;
    const basisModel = clonePreviewModel(model);
    const submitted = structuredClone(batch);
    try {
      const basisHash = await computeModelHash(basisModel);
      if (revision !== modelRevision.current || epoch !== requestEpochRef.current || queueEpoch !== batchQueueEpoch.current) return null;
      if (!basisHash) throw new Error("The current model hash is unavailable.");
      const key = `operation-batch-${++batchSequence.current}`;
      // W-10: derived centrally from the batch contents, whatever its producer
      // (geometry builder, offline intake, requeue or a routed single intent).
      const requiresPreview = batchRequiresPreview(submitted);
      // The registered submission is immutable: runs resolve it by key and never
      // read a caller's entry contents.
      const registered = deepFreeze({ key, batch: submitted, basisModel, basisHash, basisRevision: revision, requiresPreview,
        ...(options.agentContext ? { agentContext: structuredClone(options.agentContext) } : {}),
        ...(options.importContext ? { importContext: structuredClone(options.importContext) } : {}) });
      batchRegistrations.current.set(key, { entry: registered, epoch: queueEpoch });
      if (options.agentContext) agentProposalStandingRef.current.set(key, {status:"pending_review",outcomeModelHash:null});
      setQueuedBatches((current) => [...current, registered]);
      setBatchMessage("Batch queued for validation and explicit application.");
      if (options.reveal !== false) {
        setActiveSection("operations");
        setOperationTab("review");
        setToolkitFocus({ testId: "", elementId: "batch-review" });
      }
      sessionEvents.emit({ type: "queued", batchId: submitted.batch_id, key, basisRevision: revision, basisHash: basisHash.value });
      return key;
    } catch (error) {
      if (revision === modelRevision.current && epoch === requestEpochRef.current) {
        setBatchMessage(`Batch could not be queued: ${nativeFailureText(error)}`);
      }
      return null;
    }
  }

  async function handleRunOperationBatch(requested: QueuedBatch, apply: boolean) {
    // W-10: only the registered, immutable submission runs, resolved by key;
    // the caller's entry contents (batch, flags, basis) are ignored.
    const registration = batchRegistrations.current.get(String(requested?.key));
    const registered = () => batchRegistrations.current.get(registration!.entry.key) === registration && registration!.epoch === batchQueueEpoch.current;
    if (!registration || !registered()) {
      setBatchMessage(`Batch ${String(requested?.batch?.batch_id ?? requested?.key ?? "unknown")} is not registered in the review queue; it was not run.`);
      return;
    }
    const entry = registration.entry;
    if (operationRequest.current.busy || entry.basisRevision !== modelRevision.current) return;
    // The gate follows the registered batch's operations, with the same
    // predicate as the Apply button, and the preview must be of this exact
    // batch content (its canonical fingerprint at validation).
    const gated = apply && batchRequiresPreview(entry.batch);
    const refusePreview = () => setBatchMessage(`Batch ${entry.batch.batch_id} was not applied. ${PREVIEW_REQUIRED_REASON(entry.batch)}`);
    if (gated && (!registration.validated || !previewSatisfied(entry, registration.validated.outcome, modelRevision.current))) {
      refusePreview();
      return;
    }
    const revision = modelRevision.current;
    const request = ++operationRequest.current.sequence;
    if (apply) agentApplyingRef.current.add(entry.key);
    operationRequest.current.busy = true;
    const stillCurrent = () => operationRequest.current.sequence === request && modelRevision.current === revision;
    // §3.6 step 3: a run that ends with neither an outcome nor a retirement or
    // withdrawal of its registration (both emit their own event) is abandoned.
    const abandon = (reason: string) => {
      if (registered()) sessionEvents.emit({ type: "abandoned", batchId: entry.batch.batch_id, key: entry.key, reason });
    };
    setOperationBusy(true);
    setBatchMessage(null);
    try {
      if (!currentModel.current) return abandon("The session holds no model.");
      const fingerprint = await canonicalSha256Hex(entry.batch);
      if (!stillCurrent()) return abandon("The request was superseded before the batch ran.");
      if (!registered()) throw new Error("The batch was withdrawn from the review queue; it was not run.");
      if (gated && fingerprint !== registration.validated?.fingerprint) {
        refusePreview();
        return;
      }
      const initialHash = await computeModelHash(currentModel.current);
      if (!stillCurrent()) return abandon("The request was superseded before the batch ran.");
      if (!initialHash || initialHash.value !== entry.basisHash.value) throw new Error("The model changed. Prepare a new batch.");
      const outcome = await (apply ? applyOperationBatch : validateOperationBatch)(entry.basisModel, entry.batch, entry.basisHash);
      if (!stillCurrent() || !currentModel.current) return abandon("The request was superseded while the batch ran; its result was discarded.");
      const currentHash = await computeModelHash(currentModel.current);
      if (!stillCurrent()) return abandon("The request was superseded while the batch ran; its result was discarded.");
      if (
        currentHash?.value !== initialHash.value ||
        outcome.initial_model_hash?.value !== initialHash.value ||
        outcome.batch_id !== entry.batch.batch_id
      ) {
        throw new Error("The batch result does not match the original model basis; it was discarded.");
      }
      if (!apply && (outcome.acceptance || outcome.applied_model || outcome.validation.application_status === "applied_to_session_model")) {
        throw new Error("Validation returned an application result; it was discarded.");
      }
      if (!registered()) throw new Error("The batch was withdrawn from the review queue; its result was discarded.");
      if (!apply) registration.validated = { fingerprint, outcome };
      // A validation, or an apply that did not apply, is shown at once. An
      // applied outcome is published only with its model, below, so a failed
      // preparation keeps the earlier preview and its Apply gate.
      if (!apply || outcome.validation.application_status !== "applied_to_session_model") {
        setBatchOutcomes((current) => ({ ...current, [entry.key]: outcome }));
        const passed = outcome.validation.batch_validation_status === "passed" && outcome.simulation_disposition !== "rolled_back_no_model_published";
        sessionEvents.emit({ type: passed ? "validated" : "refused", batchId: entry.batch.batch_id, key: entry.key, outcome });
        return;
      }
      if (!outcome.applied_model || !outcome.acceptance || outcome.simulation_disposition !== "committed_as_one_batch") {
        throw new Error("The batch did not return a complete application receipt; the model was not changed.");
      }
      // Prepare: every value the publication needs, computed before any state
      // changes. A failure here leaves the history, receipts, review context,
      // applied operations, registration and queue as they were.
      const appliedModel = outcome.applied_model;
      const agentStanding = agentProposalStandingRef.current.get(entry.key);
      const agentAppliedHash = outcome.applied_model_backend_hash ? { ...entry.basisHash, value: outcome.applied_model_backend_hash } : null;
      const publication = prepareModelPublication(appliedModel);
      const checkpoint: SessionModelCheckpoint = {
        checkpoint_id: `undo-${entry.key}`,
        operation_id: entry.batch.batch_id,
        model: clonePreviewModel(entry.basisModel),
        selection: selection ?? defaultSelection(entry.basisModel)
      };
      const batchReceipt = { batch: entry.batch, outcome, ...(entry.agentContext ? {agentContext:entry.agentContext} : {}), ...(entry.importContext ? {importContext:entry.importContext} : {}) };
      const reviewContext = structuredClone(entry.batch.operations);
      const appliedReceiptId = `applied-${entry.key}`;
      const appliedFields: Omit<AppliedOperationReceipt, "receipt_id" | "sequence"> = {
        operation_id: entry.batch.batch_id,
        change_id: entry.batch.batch_id,
        target_object_type: "Model",
        target_ref: entry.basisModel.project.id,
        field_path: "batch",
        before: entry.basisHash.value,
        after: outcome.applied_model_backend_hash ?? "not_reported",
        application_route: outcome.application_route === "local_wasm_engine" ? "local_wasm_engine" : "tauri_backend_apply",
        applied_model_hash: outcome.applied_model_backend_hash ?? "not_reported",
        acceptance: outcome.acceptance!,
        diagnostics: outcome.diagnostics,
        professional_boundary: outcome.professional_boundary
      };
      const prunedSelection = prunedSelectionForPublication(appliedModel);
      const appliedSolveJob = sessionHistoryChangedSolveJob("batch", entry.batch.batch_id);
      // Run sheet S2: the session event listeners' staged transition (§3.6).
      const publishEvents = sessionEvents.stage({ type: "checkpoint", operationId: entry.batch.batch_id, appliedModel, operationOutcomes: outcome.operation_outcomes });

      // Publish: one synchronous block of state setters and session-owned ref
      // writes; nothing here throws.
      setBatchOutcomes((current) => ({ ...current, [entry.key]: outcome }));
      setUndoStack((current) => [checkpoint, ...current].slice(0, 25));
      setRedoStack([]);
      setBatchReceipts((current) => [...current, batchReceipt]);
      setRetainedReviewContext((current) => [...current, ...reviewContext]);
      setAppliedOperations((current) => [...current, { receipt_id: appliedReceiptId, sequence: current.length + 1, ...appliedFields }]);
      publishModel(publication);
      if (agentStanding) { agentStanding.status = "applied"; agentStanding.outcomeModelHash = agentAppliedHash; }
      commitSelectionState(prunedSelection, appliedModel);
      batchRegistrations.current.delete(entry.key);
      setQueuedBatches((current) => current.filter((candidate) => candidate.key !== entry.key));
      publishEvents();
      clearComputedModelState(appliedSolveJob);
      setProposal(null);
      setSelectedReviewTarget(null);
      const appliedMessage = "Batch applied once. Previous solve results were cleared; one undo checkpoint is available.";
      setBatchMessage(appliedMessage);

      // Notify: external callbacks, each caught and reported; the published
      // batch is not rolled back.
      try {
        retireViewportBoxGesture();
      } catch (error) {
        setBatchMessage(`${appliedMessage} The viewport did not retire its box gesture: ${nativeFailureText(error)}`);
      }
    } catch (error) {
      if (stillCurrent()) setBatchMessage(`Batch request failed: ${nativeFailureText(error)}`);
    } finally {
      agentApplyingRef.current.delete(entry.key);
      if (operationRequest.current.sequence === request) {
        operationRequest.current.busy = false;
        setOperationBusy(false);
      }
    }
  }

  async function handleAddDraftReview(
    submission: DraftSubmission,
    generation: number
  ): Promise<FrozenDraftReview | null> {
    if (!model || operationRequest.current.busy) return null;
    const revision = modelRevision.current;
    const epoch = requestEpochRef.current;
    const request = ++operationRequest.current.sequence;
    operationRequest.current.busy = true;
    const basisModel = clonePreviewModel(model);
    const frozenSubmission = structuredClone(submission);
    const stillCurrent = () =>
      operationRequest.current.sequence === request &&
      modelRevision.current === revision &&
      requestEpochRef.current === epoch;
    setOperationBusy(true);
    setOperationMessage(null);
    try {
      const basisHash = await computeModelHash(basisModel);
      if (!stillCurrent() || !basisHash) return null;
      const outcome = frozenSubmission.kind === "single"
        ? await validateModelOperation(basisModel, frozenSubmission.intent, basisHash)
        : await validateOperationBatch(basisModel, frozenSubmission.batch, basisHash);
      if (!stillCurrent() || !currentModel.current) return null;
      const currentHash = await computeModelHash(currentModel.current);
      if (!stillCurrent() || currentHash?.value !== basisHash.value) return null;
      if (!validationMatchesSubmission(frozenSubmission, outcome)) {
        setOperationMessage("Draft validation did not produce a clean, matching diff. Update the draft and Add again.");
        return null;
      }
      const review: FrozenDraftReview = {
        reviewId: `viewport-draft-review-${++directDraftReviewSequence.current}`,
        generation,
        basisRevision: revision,
        basisEpoch: epoch,
        basisHash,
        submission: frozenSubmission,
        outcome
      };
      directDraftReviews.current.clear();
      directDraftReviews.current.set(review.reviewId, review);
      return structuredClone(review);
    } catch (error) {
      if (stillCurrent()) setOperationMessage(`Draft validation failed to run: ${nativeFailureText(error)}`);
      return null;
    } finally {
      if (operationRequest.current.sequence === request) {
        operationRequest.current.busy = false;
        setOperationBusy(false);
      }
    }
  }

  async function handleApplyDraftReview(review: FrozenDraftReview): Promise<boolean> {
    if (!model || operationRequest.current.busy) return false;
    const registered = directDraftReviews.current.get(review.reviewId);
    if (
      !registered ||
      registered.basisRevision !== modelRevision.current ||
      registered.basisEpoch !== requestEpochRef.current ||
      registered.basisHash.value !== review.basisHash.value ||
      !sameSubmission(registered.submission, review.submission) ||
      !validationMatchesSubmission(registered.submission, registered.outcome)
    ) return false;

    const revision = modelRevision.current;
    const epoch = requestEpochRef.current;
    const request = ++operationRequest.current.sequence;
    operationRequest.current.busy = true;
    // The review stays registered until its model is published (`publishModel`
    // clears every draft review), so a failure before publication can be retried.
    const basisModel = clonePreviewModel(model);
    const frozenSubmission = structuredClone(registered.submission);
    const stillCurrent = () =>
      operationRequest.current.sequence === request &&
      modelRevision.current === revision &&
      requestEpochRef.current === epoch;
    setOperationBusy(true);
    setOperationMessage(null);
    try {
      const currentHash = await computeModelHash(basisModel);
      if (!stillCurrent() || currentHash?.value !== registered.basisHash.value) return false;
      if (frozenSubmission.kind === "batch") {
        const outcome = await applyOperationBatch(basisModel, frozenSubmission.batch, registered.basisHash);
        if (!stillCurrent() || !currentModel.current) return false;
        const afterWaitHash = await computeModelHash(currentModel.current);
        if (!stillCurrent() || afterWaitHash?.value !== registered.basisHash.value) return false;
        if (!applyResultMatchesSubmission(frozenSubmission, outcome, registered.basisHash)) return false;
        const [appliedHash, batchHash] = await Promise.all([
          computeModelHash(outcome.applied_model!),
          canonicalSha256Hex(frozenSubmission.batch)
        ]);
        if (
          !stillCurrent() ||
          appliedHash?.value !== outcome.applied_model_backend_hash ||
          `sha256:${batchHash}` !== outcome.batch_hash
        ) return false;
        // Prepare: every value the publication needs, computed before any state
        // changes. A failure here leaves the model, history, receipts, review
        // context, applied operations and the registered review as they were.
        const appliedModel = outcome.applied_model!;
        const publication = prepareModelPublication(appliedModel);
        const checkpoint: SessionModelCheckpoint = {
          checkpoint_id: `undo-${review.reviewId}`,
          operation_id: frozenSubmission.batch.batch_id,
          model: basisModel,
          selection: selection ?? defaultSelection(basisModel)
        };
        const batchReceipt = { batch: frozenSubmission.batch, outcome };
        const reviewContext = structuredClone(frozenSubmission.batch.operations);
        const appliedFields: Omit<AppliedOperationReceipt, "receipt_id" | "sequence"> = {
          operation_id: frozenSubmission.batch.batch_id,
          change_id: frozenSubmission.batch.batch_id,
          target_object_type: "Model",
          target_ref: basisModel.project.id,
          field_path: "batch",
          before: registered.basisHash.value,
          after: outcome.applied_model_backend_hash ?? "not_reported",
          application_route: outcome.application_route === "local_wasm_engine" ? "local_wasm_engine" : "tauri_backend_apply",
          applied_model_hash: outcome.applied_model_backend_hash ?? "not_reported",
          acceptance: outcome.acceptance!,
          diagnostics: outcome.diagnostics,
          professional_boundary: outcome.professional_boundary
        };
        const endpoint = frozenSubmission.batch.operations.at(-1)?.change.after;
        const endpointId = endpoint ? (JSON.parse(endpoint) as { to?: string }).to : null;
        const appliedSelection = singletonSelection(
          endpointId ? { type: "node", id: endpointId } : defaultSelection(appliedModel),
          orderedSelectionRef.current
        );
        const appliedSolveJob = sessionHistoryChangedSolveJob("batch", frozenSubmission.batch.batch_id);
        const publishEvents = sessionEvents.stage({ type: "checkpoint", operationId: checkpoint.operation_id });

        // Publish: one synchronous block of state setters and session-owned ref
        // writes; nothing here throws.
        setUndoStack((current) => [checkpoint, ...current].slice(0, 25));
        setRedoStack([]);
        publishEvents();
        setBatchReceipts((current) => [...current, batchReceipt]);
        setRetainedReviewContext((current) => [...current, ...reviewContext]);
        setAppliedOperations((current) => [...current, { receipt_id: `applied-${review.reviewId}`, sequence: current.length + 1, ...appliedFields }]);
        publishModel(publication, review.reviewId);
        commitSelectionState(appliedSelection, appliedModel);
        clearComputedModelState(appliedSolveJob);
        const appliedMessage = "Applied the reviewed route as one atomic batch; one undo checkpoint is available.";
        setOperationMessage(appliedMessage);

        // Notify: external callbacks, each caught and reported; the published
        // batch is not rolled back.
        const viewportFailure = retireViewportBoxGestureAfterPublication();
        if (viewportFailure) setOperationMessage(`${appliedMessage} ${viewportFailure}`);
        return true;
      }

      const intent = frozenSubmission.intent;
      const outcome = await applyModelOperation(basisModel, intent, registered.basisHash);
      if (!stillCurrent() || !currentModel.current) return false;
      const afterWaitHash = await computeModelHash(currentModel.current);
      if (
        !stillCurrent() ||
        afterWaitHash?.value !== registered.basisHash.value ||
        !applyResultMatchesSubmission(frozenSubmission, outcome, registered.basisHash)
      ) return false;
      const appliedHash = await computeModelHash(outcome.applied_model!);
      if (!stillCurrent() || appliedHash?.value !== outcome.applied_model_backend_hash) return false;
      // Prepare: as for the batch above.
      const appliedModel = outcome.applied_model!;
      const publication = prepareModelPublication(appliedModel);
      const receipt: AppliedOperationReceipt = {
        receipt_id: `applied-${review.reviewId}`,
        sequence: appliedOperations.length + 1,
        operation_id: outcome.operation_id,
        change_id: outcome.change_id,
        target_object_type: outcome.target_object_type,
        target_ref: outcome.target_ref,
        field_path: intent.change.field_path,
        before: intent.change.before,
        after: intent.change.after,
        application_route: outcome.application_route,
        applied_model_hash: outcome.applied_model_backend_hash ?? "not_reported",
        acceptance: outcome.acceptance,
        diagnostics: outcome.diagnostics,
        professional_boundary: outcome.professional_boundary
      };
      const reviewContext = structuredClone(intent);
      const checkpoint: SessionModelCheckpoint = {
        checkpoint_id: `undo-${review.reviewId}`,
        operation_id: outcome.operation_id,
        model: basisModel,
        selection: selection ?? defaultSelection(basisModel)
      };
      const appliedSelection = singletonSelection(
        selectionForOperationOutcome(outcome) ?? defaultSelection(appliedModel),
        orderedSelectionRef.current
      );
      const appliedSolveJob = modelChangedSolveJob(outcome);
      const publishEvents = sessionEvents.stage({ type: "checkpoint", operationId: checkpoint.operation_id });

      // Publish: one synchronous block of state setters and session-owned ref
      // writes; nothing here throws.
      setAppliedOperations((current) => [receipt, ...current]);
      setRetainedReviewContext((current) => [...current, reviewContext]);
      setUndoStack((current) => [checkpoint, ...current].slice(0, 25));
      setRedoStack([]);
      publishEvents();
      publishModel(publication, review.reviewId);
      commitSelectionState(appliedSelection, appliedModel);
      clearComputedModelState(appliedSolveJob);
      const appliedMessage = `Applied reviewed ${outcome.operation_id}; previous solve results were cleared.`;
      setOperationMessage(appliedMessage);

      // Notify: external callbacks, each caught and reported; the published
      // operation is not rolled back.
      const viewportFailure = retireViewportBoxGestureAfterPublication();
      if (viewportFailure) setOperationMessage(`${appliedMessage} ${viewportFailure}`);
      return true;
    } catch (error) {
      if (stillCurrent()) setOperationMessage(`Draft apply failed to run: ${nativeFailureText(error)}`);
      return false;
    } finally {
      if (operationRequest.current.sequence === request) {
        operationRequest.current.busy = false;
        setOperationBusy(false);
      }
    }
  }

  async function handleValidateIntent(intent: EditorOperationIntent) {
    if (!model || operationRequest.current.busy) return;
    const revision = modelRevision.current;
    const request = ++operationRequest.current.sequence;
    operationRequest.current.busy = true;
    const stillCurrent = () => operationRequest.current.sequence === request && modelRevision.current === revision;
    setOperationBusy(true);
    setOperationMessage(null);
    try {
      const outcome = await validateModelOperation(model, intent, modelHash);
      if (!stillCurrent()) return;
      setOperationOutcomes((current) => ({ ...current, [intentKey(intent)]: outcome }));
    } catch (error) {
      if (stillCurrent()) setOperationMessage(`Operation validation failed to run: ${nativeFailureText(error)}`);
    } finally {
      if (operationRequest.current.sequence === request) {
        operationRequest.current.busy = false;
        setOperationBusy(false);
      }
    }
  }

  async function handleApplyIntent(intent: EditorOperationIntent, ownedOutcome?: { current?: Readonly<OperationOutcome> }): Promise<boolean> {
    if (!model || operationRequest.current.busy) return false;
    // W-10, O6: an operation that requires preview (a reconnect, a bend
    // insertion) is never applied without one; route it to batch review.
    if (operationRequiresPreview(intent?.change?.change_kind)) {
      const reconnect = intent.change.change_kind === "reconnect_pipe_run";
      setOperationMessage(reconnect
        ? "Reconnect is applied through batch review; it has been queued there."
        : `${intent.change.change_kind} is applied through batch review after a preview; it has been queued there.`);
      await handleQueueOperationBatch({ batch_id: `${reconnect ? "reconnect" : "preview"}-${intentKey(intent)}`, operations: [structuredClone(intent)] });
      return false;
    }
    const revision = modelRevision.current;
    const request = ++operationRequest.current.sequence;
    operationRequest.current.busy = true;
    const stillCurrent = () => operationRequest.current.sequence === request && modelRevision.current === revision;
    setOperationBusy(true);
    setOperationMessage(null);
    try {
      const initialHash = await computeModelHash(model);
      if (!stillCurrent() || !initialHash) return false;
      const outcome = await applyModelOperation(model, intent, initialHash);
      if (!stillCurrent() || !currentModel.current) return false;
      const currentHash = await computeModelHash(currentModel.current);
      // The hash computation is asynchronous too; generation must still match
      // after it resolves before any outcome, receipt or checkpoint is published.
      if (!stillCurrent() || currentHash?.value !== initialHash.value) return false;
      // An outcome that did not apply is shown at once. An applied outcome is
      // published only with its model, below, so a failed preparation keeps
      // the earlier outcome.
      if (outcome.validation.application_status !== "applied_to_session_model" || !outcome.applied_model) {
        setOperationOutcomes((current) => ({ ...current, [intentKey(intent)]: outcome }));
        // Internal owned result only; this is not acknowledgement of a React publication.
        if (ownedOutcome) ownedOutcome.current = outcome;
        setOperationMessage(
          `Operation ${outcome.operation_id} was not applied (${outcome.validation.application_status}); see its diagnostics.`
        );
        return false;
      }
      // Prepare: every value the publication needs, computed before any state
      // changes. A failure here leaves the model, history, receipts, review
      // context, applied operations, queued intents and earlier outcome as they were.
      const appliedModel = outcome.applied_model;
      const publication = prepareModelPublication(appliedModel);
      const receipt: AppliedOperationReceipt = {
        receipt_id: `applied-${appliedOperations.length + 1}-${intentKey(intent)}`,
        sequence: appliedOperations.length + 1,
        operation_id: outcome.operation_id,
        change_id: outcome.change_id,
        target_object_type: outcome.target_object_type,
        target_ref: outcome.target_ref,
        field_path: intent.change.field_path,
        before: intent.change.before,
        after: intent.change.after,
        application_route: outcome.application_route,
        applied_model_hash: outcome.applied_model_backend_hash ?? "not_reported",
        acceptance: outcome.acceptance,
        diagnostics: outcome.diagnostics,
        professional_boundary: outcome.professional_boundary
      };
      const reviewContext = structuredClone(intent);
      const checkpoint: SessionModelCheckpoint = {
        checkpoint_id: `undo-${appliedOperations.length + 1}-${intentKey(intent)}`,
        operation_id: outcome.operation_id,
        model: clonePreviewModel(model),
        selection: selection ?? defaultSelection(model)
      };
      const authoredSelection = selectionForOperationOutcome(outcome);
      // Explicit creation deliberately focuses the authored entity. Ordinary
      // edits and deletion preserve ordered membership and prune only refs the
      // accepted model no longer contains.
      const appliedSelection = authoredSelection && /^(create_|insert_|connect_)/.test(outcome.change_kind)
        ? singletonSelection(authoredSelection, orderedSelectionRef.current)
        : prunedSelectionForPublication(appliedModel);
      const appliedIntentKey = intentKey(intent);
      const appliedSolveJob = modelChangedSolveJob(outcome);
      const publishEvents = sessionEvents.stage({ type: "checkpoint", operationId: checkpoint.operation_id });

      // Publish: one synchronous block of state setters and session-owned ref
      // writes; nothing here throws.
      setOperationOutcomes((current) => ({ ...current, [appliedIntentKey]: outcome }));
      setAppliedOperations((current) => [receipt, ...current]);
      setRetainedReviewContext((current) => [...current, reviewContext]);
      setUndoStack((current) => [checkpoint, ...current].slice(0, 25));
      setRedoStack([]);
      publishEvents();
      publishModel(publication);
      commitSelectionState(appliedSelection, appliedModel);
      setEditorIntents((current) => current.filter((queued) => intentKey(queued) !== appliedIntentKey));
      // Earlier solve output no longer describes the edited model document;
      // keeping it visible would overstate what was computed.
      setResult(null);
      setAnalysisRun(null);
      setInputManifest(null);
      setRuleCheckAggregate(null);
      setProposal(null);
      setSelectedReviewTarget(null);
      setSolveJob(appliedSolveJob);
      let appliedMessage =
        `Applied ${outcome.operation_id} to the session model; previous solve results were cleared. Run a new solve, then save the project to store the edited model locally.`;
      setOperationMessage(appliedMessage);

      // Notify: external callbacks, each caught and reported; the published
      // operation is not rolled back. A caller's owned outcome may be an accessor.
      const viewportFailure = retireViewportBoxGestureAfterPublication();
      if (viewportFailure) {
        appliedMessage = `${appliedMessage} ${viewportFailure}`;
        setOperationMessage(appliedMessage);
      }
      if (ownedOutcome) {
        try {
          // Internal owned result only; this is not acknowledgement of a React publication.
          ownedOutcome.current = outcome;
        } catch (error) {
          setOperationMessage(`${appliedMessage} The caller did not receive the applied outcome: ${nativeFailureText(error)}`);
        }
      }
      return true;
    } catch (error) {
      if (stillCurrent()) setOperationMessage(`Operation apply failed to run: ${nativeFailureText(error)}`);
      return false;
    } finally {
      if (operationRequest.current.sequence === request) {
        operationRequest.current.busy = false;
        setOperationBusy(false);
      }
    }
  }

  function handleApplyNextQueuedIntent() {
    if (operationBusy) return;
    const [nextIntent] = editorIntents;
    if (!nextIntent) return;
    setActiveSection("operations");
    setOperationTab("review");
    void handleApplyIntent(nextIntent);
  }

  function handleUndoSessionModelEdit() {
    stepSessionHistory("undo");
  }

  function handleRedoSessionModelEdit() {
    stepSessionHistory("redo");
  }

  // Undo and redo move one checkpoint between the stacks with the model it
  // restores, ordered Prepare, Publish, Notify like an apply. Neither throws:
  // a failure is reported in the operation message.
  function stepSessionHistory(action: "undo" | "redo") {
    const source = action === "undo" ? undoStack : redoStack;
    if (operationRequest.current.busy || !model || !selection || source.length === 0) return;
    const [checkpoint, ...remaining] = source;

    // Prepare: every value the publication needs, computed before any state
    // changes. A failure leaves the model and both stacks as they were, so the
    // step can be retried.
    let prepared: Readonly<{
      restoredModel: PreviewModel;
      publication: ModelPublication;
      reverse: SessionModelCheckpoint;
      restoredSelection: OrderedSelectionState;
      solveJob: SolveJobAuditState;
      publishEvents: () => void;
    }>;
    try {
      const restoredModel = clonePreviewModel(checkpoint.model);
      prepared = {
        restoredModel,
        publication: prepareModelPublication(restoredModel),
        reverse: {
          checkpoint_id: `${action === "undo" ? "redo" : "undo"}-${checkpoint.checkpoint_id}`,
          operation_id: checkpoint.operation_id,
          model: clonePreviewModel(model),
          selection
        },
        restoredSelection: singletonSelection(checkpoint.selection, orderedSelectionRef.current),
        solveJob: sessionHistoryChangedSolveJob(action, checkpoint.operation_id),
        publishEvents: sessionEvents.stage({ type: action === "undo" ? "undone" : "redone", operationId: checkpoint.operation_id })
      };
    } catch (error) {
      const failure = `${action === "undo" ? "Undo" : "Redo"} failed to run: ${nativeFailureText(error)}`;
      setOperationMessage(failure);
      setHistoryFailure(failure);
      return;
    }

    // Publish: one synchronous block of state setters and session-owned ref
    // writes; nothing here throws.
    if (action === "undo") {
      setUndoStack(remaining);
      setRedoStack((current) => [prepared.reverse, ...current].slice(0, 25));
    } else {
      setRedoStack(remaining);
      setUndoStack((current) => [prepared.reverse, ...current].slice(0, 25));
    }
    prepared.publishEvents();
    publishModel(prepared.publication);
    commitSelectionState(prepared.restoredSelection, prepared.restoredModel);
    clearComputedModelState(prepared.solveJob);
    const steppedMessage =
      `${action === "undo" ? "Undid" : "Redid"} ${checkpoint.operation_id} in the local session; previous solve results were cleared. Save is still required to persist the current session model.`;
    setOperationMessage(steppedMessage);

    // Notify: external callbacks, each caught and reported; the step is not
    // rolled back.
    const viewportFailure = retireViewportBoxGestureAfterPublication();
    if (viewportFailure) {
      setOperationMessage(`${steppedMessage} ${viewportFailure}`);
      setHistoryFailure(`${action === "undo" ? "Undid" : "Redid"} ${checkpoint.operation_id}. ${viewportFailure}`);
    }
  }

  function clearComputedModelState(nextSolveJob: SolveJobAuditState) {
    invalidateReportPackageComputedState();
    ruleRevisionGate.current.invalidate();
    setHistoricalRun(null);
    setResult(null);
    setAnalysisRun(null);
    setInputManifest(null);
    setRuleCheckAggregate(null);
    setProposal(null);
    setSelectedReviewTarget(null);
    setSolveJob(nextSolveJob);
  }

  function invalidateReportPackageComputedState() {
    reportPackageRequestGenerationRef.current += 1;
    reportPackageBusyGenerationRef.current = null;
    setReportPackageBusy(false);
    setReportPackageRedaction(null);
    setReportPackageRoute(null);
  }

  const latestIntegrityObservation = useRef(0);
  function recordPersistenceObservation(envelope: LocalProjectEnvelope, modelHash: ModelHashEvidence | null,
    envelopeHash: ProjectEnvelopeHashEvidence | null, source: "save" | "create", generation: number,
    observation: number, responseValid: boolean, payloadRef: string, retainedHistoricalCarrier = false) {
    if (!canPublishPersistenceObservation(generation, projectSessionGenerationRef.current, observation, latestIntegrityObservation.current)) return;
    latestIntegrityObservation.current = observation;
    const observedAt = new Date().toISOString();
    setModelHashIntegrity({ ...deriveModelHashIntegrity(envelope.model_hash ?? null, modelHash, payloadRef, source, observedAt, responseValid),
      claim_standing: retainedHistoricalCarrier ? "retained_historical_carrier" : "canonical_payload" });
    setProjectEnvelopeHashIntegrity(deriveProjectEnvelopeHashIntegrity(envelope.project_envelope_hash ?? null, envelopeHash, payloadRef, source, observedAt, responseValid));
  }

  function acquireProjectOperation(): symbol | null {
    if (projectOperationOwner.current !== null) return null;
    const owner = Symbol("project operation");
    projectOperationOwner.current = owner;
    setProjectBusy(true);
    return owner;
  }

  function releaseProjectOperation(owner: symbol) {
    if (projectOperationOwner.current !== owner) return;
    projectOperationOwner.current = null;
    setProjectBusy(false);
  }

  /** HELP_HUMAN rulings (2026-10-10): the app never silently replaces a stored
   * project. Every write goes out unconfirmed. Save Local Project of the
   * session's own stored project carries its base (the stored envelope hash it
   * last opened or saved), which the store admits as a save in place while that
   * is still the stored revision. A refusal (`PROJECT-ID-EXISTS`, or
   * `PROJECT-BASE-MOVED` when another window or process saved that id since)
   * asks the user: Replace (retry, confirmed), Save as a new project, or
   * Cancel, the default. */
  async function writeWithReplaceConfirmation(
    kind: "create" | "save",
    requestModel: PreviewModel,
    write: (confirmedRevision: string | null) => Promise<LocalProjectEnvelope>
  ): Promise<StoredProjectWrite> {
    const refusalCode = (error: unknown) => /^(?:Error: )?(PROJECT-ID-EXISTS|PROJECT-BASE-MOVED): /.exec(String(error))?.[1];
    let stale = false;
    try {
      return { outcome: "written", envelope: await write(null) };
    } catch (error) {
      const code = refusalCode(error);
      if (!code) throw error;
      stale = code === "PROJECT-BASE-MOVED";
    }
    for (;;) {
      const existing = await findLocalProject(requestModel.project.id);
      if (!existing) return { outcome: "written", envelope: await write(null) };
      const choice = await new Promise<ReplaceProjectChoice>((resolve) => {
        const release = holdModal();
        // Captured before the workspace turns inert, which drops its focus.
        const opener = document.activeElement instanceof HTMLElement ? document.activeElement : null;
        setReplaceProjectPrompt({
          kind, existing, stale, opener,
          choose: (picked) => { release(); setReplaceProjectPrompt(null); resolve(picked); }
        });
      });
      if (choice === "cancel") return { outcome: "kept", existing };
      if (choice === "save-as-new") return { outcome: "save-as-new", model: await withUnusedProjectId(requestModel) };
      // Replace confirms the revision the prompt showed. If another writer saved
      // the project while the prompt was open, the store refuses and the user is
      // asked again about the revision now stored.
      try {
        return { outcome: "written", envelope: await write(existing.revision) };
      } catch (error) {
        if (refusalCode(error) !== "PROJECT-BASE-MOVED") throw error;
        stale = true;
      }
    }
  }

  /** The same document under a project id the store does not hold. Only
   * `project.id` changes, so the model hash changes with it. */
  async function withUnusedProjectId(source: PreviewModel): Promise<PreviewModel> {
    const token = new Date().toISOString().replace(/[^0-9TZ]/g, "").toLowerCase();
    const base = `${source.project.id}:copy-${token}`;
    let candidate = base;
    for (let suffix = 2; await findLocalProject(candidate); suffix += 1) candidate = `${base}-${suffix}`;
    const renamed = structuredClone(source);
    renamed.project.id = candidate;
    return renamed;
  }

  function adoptSavedAsNewModel(renamed: PreviewModel) {
    commitModel(renamed);
    storedBaseRef.current = null;
    preserveAndPruneSelection(renamed);
    // Undo checkpoints hold the old identity; Save as new starts a fresh history.
    setUndoStack([]);
    sessionEvents.emit({ type: "history-reset", projectId: renamed.project.id });
    setRedoStack([]);
    setProjectSummary(null);
    setProjectEnvelopeHash(null);
    setResult(null);
    setAnalysisRun(null);
    setInputManifest(null);
    setRuleCheckAggregate(null);
    setSolveJob(initialSolveJob());
  }

  const SAVE_AS_NEW_SUPERSEDED = "Not saved: the session changed while the replace prompt was open; nothing was written.";
  /** A New Blank whose create landed after the model on screen changed is stored but
   * not opened; the session keeps the changed model and the stored blank is kept. */
  const NEW_BLANK_SUPERSEDED = "NEW-BLANK-SUPERSEDED";
  const newBlankSupersededMessage = (stored: PreviewModel["project"]) =>
    `${NEW_BLANK_SUPERSEDED}: the new blank project "${stored.name}" (${stored.id}) was created but not opened, because the model changed while it was being created. This session keeps the changed model. The blank is stored locally: open it from List Local Projects.`;

  async function handleCreateProject() {
    return createProject(null);
  }

  /** `saveAsNew`: the renamed document after the user chose Save as a new
   * project. The session already holds it; the run solved under the old
   * identity is not written under the new one. */
  async function createProject(saveAsNew: PreviewModel | null) {
    if (!model) return;
    const owner = acquireProjectOperation();
    if (!owner) return;
    const request = ++projectRequest.current;
    let epoch = requestEpochRef.current;
    // Save as a new project follows the session's own adoption of the renamed
    // document, after which the shell may settle its selection; that write is
    // current while the session still holds exactly that document.
    const stillCurrent = () => request === projectRequest.current &&
      (saveAsNew ? currentModel.current === saveAsNew : epoch === requestEpochRef.current);
    const requestModel = saveAsNew ?? model;
    const dropRun = saveAsNew !== null;
    let pendingSaveAsNew: PreviewModel | null = null;
    const generation = projectSessionGenerationRef.current;
    const requestRevision = uiModelRevisionRef.current;
    const sameProjectSession = () => generation === projectSessionGenerationRef.current && currentModel.current?.project.id === requestModel.project.id;
    const retainedRun = dropRun ? null : retainedReferencePersistence(requestModel);
    const requestHistoricalRun = dropRun ? null : historicalRun?.designation === "historical_saved_run" ? historicalRun : retainedRun?.history ?? null;
    let pendingObservation: { envelope: LocalProjectEnvelope; ordinal: number } | null = null;
    try {
      const combinedContext = structuredClone([...retainedReviewContext, ...editorIntents, ...queuedBatches.flatMap((entry) => entry.batch.operations)]);
      const actualRequestModelHash = await computeModelHash(requestModel);
      const snapshotModelHash = requestHistoricalRun ? requestHistoricalRun.modelHash : actualRequestModelHash;
      const snapshotResult = requestHistoricalRun ? requestHistoricalRun.rawMechanicsResult as MechanicsResult | null : retainedRun?.result ?? (dropRun ? null : result);
      const snapshotAnalysisRun = requestHistoricalRun ? requestHistoricalRun.rawAnalysisRun as AnalysisRunEnvelope | null : retainedRun?.analysisRun ?? (dropRun ? null : analysisRun);
      if (!stillCurrent()) return;
      const computedEnvelopeHash = await computeProjectEnvelopeHash({
        model: requestModel,
        editor_intents: combinedContext,
        proposal,
        selected_review_target: selectedReviewTarget,
        mechanics_result: snapshotResult,
        analysis_run: snapshotAnalysisRun,
        model_hash: snapshotModelHash
      });
      const envelopeHash = requestHistoricalRun && computedEnvelopeHash?.value === requestHistoricalRun.envelopePayloadHash
        ? requestHistoricalRun.envelopeHash : computedEnvelopeHash;
      if (!stillCurrent()) return;
      const written = await writeWithReplaceConfirmation("create", requestModel, (confirmedRevision) => createLocalProject(
          requestModel,
          combinedContext,
          proposal,
          selectedReviewTarget,
          snapshotResult,
          snapshotAnalysisRun,
          snapshotModelHash,
          envelopeHash,
          confirmedRevision
        ));
      if (written.outcome === "kept") {
        setProjectMessage(keptStoredProjectMessage(written.existing));
        setProjectOperation("create_kept_stored_project");
        return;
      }
      if (written.outcome === "save-as-new") {
        pendingSaveAsNew = written.model;
        return;
      }
      const created = written.envelope;
      const writeObservation = ++persistedWriteObservation.current;
      if (!sameProjectSession()) return;
      pendingObservation = { envelope: created, ordinal: writeObservation };
      if (created.summary.project_id === requestModel.project.id) recordStoredBase(created);
      // Retire the old observation while verification of rewritten bytes is pending.
      setModelHashIntegrity(null);
      setProjectEnvelopeHashIntegrity(null);
      const returnedModelHash = await computeModelHash(created.model);
      if (!sameProjectSession()) return;
      const recomputedReturnedEnvelopeHash = await computeProjectEnvelopeHash({
        model: created.model,
        editor_intents: created.editor_intents,
        proposal: created.proposal,
        selected_review_target: created.selected_review_target,
        mechanics_result: created.mechanics_result,
        analysis_run: created.analysis_run,
        model_hash: created.model_hash
      });
      if (!sameProjectSession()) return;
      const responseModelChanged = returnedModelHash?.value !== actualRequestModelHash?.value;
      const verifiedResponse = Boolean(actualRequestModelHash && returnedModelHash &&
        created.model.project.id === requestModel.project.id &&
        created.summary.project_id === requestModel.project.id &&
        persistenceHashesMatch(created, returnedModelHash, recomputedReturnedEnvelopeHash, !responseModelChanged ? requestHistoricalRun?.modelHash ?? null : null) &&
        !responseModelChanged);
      recordPersistenceObservation(created, returnedModelHash, recomputedReturnedEnvelopeHash, "create", generation, writeObservation, verifiedResponse, requestModel.project.id, Boolean(verifiedResponse && requestHistoricalRun && !responseModelChanged));
      pendingObservation = null;
      if (created.model.project.id !== requestModel.project.id || created.summary.project_id !== requestModel.project.id) {
        if (!stillCurrent()) return;
        setProjectMessage("Create failed: PROJECT-PERSISTENCE-RESPONSE-INTEGRITY: returned project identity does not match the requested project.");
        setProjectOperation("create_failed");
        return;
      }
      if (responseModelChanged) {
        if (!stillCurrent()) return;
        setProjectMessage("Create failed: PROJECT-PERSISTENCE-RESPONSE-INTEGRITY: the returned model differs from the requested model; the store never rewrites a model document.");
        setProjectOperation("create_failed");
        return;
      }
      // Failed/missing later requests do not retire an actual same-session
      // write. Only a newer verified fulfillment may supersede this observation;
      // current-only metadata/model/history adoption keeps its stricter gate.
      const verifiedBasis = verifiedWriteBasis(verifiedResponse, generation, projectSessionGenerationRef.current,
        writeObservation, latestVerifiedWriteObservation.current, responseModelChanged ? -1 : requestRevision, returnedModelHash, "create");
      if (verifiedBasis) {
        latestVerifiedWriteObservation.current = writeObservation;
        savedBasisSequence.current += 1;
        setSavedModelBasis(verifiedBasis);
      }
      if (!stillCurrent()) return;
      const returnedHistory = requestHistoricalRun
        ? await buildHistoricalRunContext(created)
        : null;
      if (!stillCurrent()) return;
      if (requestHistoricalRun) {
        setHistoricalRun((current) => current === requestHistoricalRun ? returnedHistory : current);
      }
      setProjectSummary(created.summary);
      setProposal(created.proposal ?? null);
      setSelectedReviewTarget(created.selected_review_target ?? null);
      setProjectEnvelopeHash(created.project_envelope_hash ?? null);
      setModelDocumentVersion(created.model_document_version ?? null);
      setProjectMessage(created.summary.message);
      setProjectOperation("create");
      void autosave.afterProjectSaved(created.summary.project_id, returnedModelHash?.value ?? null);
    } catch (error) {
      if (pendingObservation && sameProjectSession() &&
        pendingObservation.envelope?.model?.project?.id === requestModel.project.id &&
        pendingObservation.envelope?.summary?.project_id === requestModel.project.id) {
        recordPersistenceObservation(pendingObservation.envelope, null, null, "create", generation,
          pendingObservation.ordinal, false, requestModel.project.id);
      }
      if (!stillCurrent()) return;
      setProjectMessage(`Create failed: ${nativeFailureText(error)}`);
      setProjectOperation("create_failed");
    } finally {
      releaseProjectOperation(owner);
      // Save as a new project: adopt the renamed document, then write it as a
      // project of its own (an early return in the try block still reaches here).
      if (pendingSaveAsNew && stillCurrent()) {
        adoptSavedAsNewModel(pendingSaveAsNew);
        await createProject(pendingSaveAsNew);
      } else if (pendingSaveAsNew) {
        setProjectMessage(SAVE_AS_NEW_SUPERSEDED);
        setProjectOperation("create_superseded");
      }
    }
  }

  /** W-17 §3: "New blank", "Blank load/reference model" and `file.new-blank` ask for
   * the project units first. Create builds the blank with the chosen map; Cancel
   * creates nothing. */
  function requestBlankProject(kind: BlankProjectKind) {
    // A project operation in flight refuses a blank, as the create itself would.
    if (projectSessionBusy()) return;
    // Captured before the workspace turns inert, which drops its focus.
    const opener = document.activeElement instanceof HTMLElement ? document.activeElement : null;
    const askUnits = () => {
      const close = () => { projectUnitsDialogOpenRef.current = false; setBlankProjectUnitsRequest(null); };
      projectUnitsDialogOpenRef.current = true;
      setBlankProjectUnitsRequest({
        kind,
        opener,
        cancel: close,
        create: (units) => {
          close();
          void (kind === "load_state" ? handleCreateBlankLoadStateProject(units) : handleCreateBlankProject(units));
        }
      });
    };
    // A new blank replaces the working model: with unsaved edits it asks first.
    if (!replacingNeedsConfirmation()) {
      askUnits();
      return;
    }
    void confirmReplacingEdits({
      action: kind === "load_state" ? "Creating a new blank load/reference model" : "Creating a new blank project",
      verb: "create it"
    }).then((guarded) => {
      if (guarded !== "proceed") {
        ++projectRequest.current;
        setProjectMessage(unsavedChangesRefusal(guarded, "Not created"));
        setProjectOperation("create_blank_kept_edits");
        return;
      }
      if (projectSessionBusy()) return;
      askUnits();
    });
  }

  /** Creates the blank at once with `units` (SI when omitted); the UI reaches it through requestBlankProject. */
  async function handleCreateBlankProject(units: ProjectUnitMap = SI_PROJECT_UNITS) {
    return createBlankProjectFrom(() => buildBlankLocalModelDocument(new Date(), units), "Created blank local model document without fixture entities or external file copies.");
  }

  /** T1 WP3: a blank load/reference-state document (B7b: the current model version with the exact
   * pressure contract, no engineering content) through the same create path as New Blank. */
  async function handleCreateBlankLoadStateProject(units: ProjectUnitMap = SI_PROJECT_UNITS) {
    return createBlankProjectFrom(() => buildBlankLoadStateModelDocument(new Date(), units), `Created blank local load/reference-state model ${MODEL_SCHEMA_VERSION} document without fixture entities, engineering values or external file copies.`);
  }

  async function createBlankProjectFrom(buildBlankModel: () => PreviewModel, createdMessage: string) {
    const owner = acquireProjectOperation();
    if (!owner) return;
    const request = ++projectRequest.current;
    let modelEpoch = modelCommitEpochRef.current;
    const stillCurrent = () => request === projectRequest.current && modelEpoch === modelCommitEpochRef.current;
    // A landed create superseded by a model change (not by another project
    // operation, which owns the status line) is named, never dropped silently.
    // `stored` is the project the create wrote (after any PROJECT-ID-EXISTS suffix).
    const superseded = (stored: PreviewModel["project"]) => {
      if (request !== projectRequest.current) return;
      setProjectMessage(newBlankSupersededMessage(stored));
      setProjectOperation("create_blank_superseded");
    };
    try {
      let blankModel = buildBlankModel();
      const blankId = blankModel.project.id;
      let blankModelHash: ModelHashEvidence | null;
      let created: LocalProjectEnvelope;
      for (let attempt = 2; ; attempt += 1) {
        blankModelHash = await computeModelHash(blankModel);
        const envelopeHash = await computeProjectEnvelopeHash({
          model: blankModel,
          editor_intents: [],
          proposal: null,
          selected_review_target: null,
          mechanics_result: null,
          analysis_run: null,
          model_hash: blankModelHash
        });
        try {
          created = await createLocalProject(blankModel, [], null, null, null, null, blankModelHash, envelopeHash);
          break;
        } catch (error) {
          // A new blank has no identity of its own to keep. If its time-stamped
          // id is already stored, it takes a suffixed id; the stored project is
          // never replaced (HELP_HUMAN ruling 2026-10-10).
          if (!String(error).includes("PROJECT-ID-EXISTS") || attempt > 20) throw error;
          blankModel = { ...blankModel, project: { ...blankModel.project, id: `${blankId}-${attempt}` } };
        }
      }
      if (!stillCurrent()) { superseded(blankModel.project); return; }
      const returnedHash = await computeModelHash(created.model);
      const returnedEnvelopeHash = await computeProjectEnvelopeHash({
        model: created.model, editor_intents: created.editor_intents,
        proposal: created.proposal, selected_review_target: created.selected_review_target,
        mechanics_result: created.mechanics_result, analysis_run: created.analysis_run,
        model_hash: created.model_hash
      });
      if (!stillCurrent()) { superseded(blankModel.project); return; }
      const verifiedBlankResponse = Boolean(blankModelHash && returnedHash &&
        created.model.project.id === blankModel.project.id &&
        created.summary.project_id === blankModel.project.id &&
        persistenceHashesMatch(created, returnedHash, returnedEnvelopeHash) &&
        returnedHash.value === blankModelHash.value);
      const createdSummary = {
        ...created.summary,
        message: createdMessage
      };
      // The create commits here. A create that fails leaves the open project's
      // rule revision gate and integrity cells as they were.
      ruleRevisionGate.current.invalidate();
      setModelHashIntegrity(null);
      setProjectEnvelopeHashIntegrity(null);
      advanceProjectSession();
      recordPersistenceObservation(created, returnedHash, returnedEnvelopeHash, "create", projectSessionGenerationRef.current, ++persistedWriteObservation.current, verifiedBlankResponse, blankModel.project.id);
      // A successful New Blank starts the first-open shell context. Failed or
      // superseded creates never reach this commit boundary or change chrome.
      routingInspectorRestore.current = null;
      pageReturnFocusRef.current = null;
      setArmedCreationTool(null);
      setToolkitFocus(null);
      setOpenMenu(null);
      setActiveSection(null);
      setStageSurface(null);
      setStageViewMemory(EMPTY_STAGE_VIEW_MEMORY);
      setTreeCollapsed(window.innerWidth < 1280);
      setInspectorCollapsed(true);
      setReviewDetailsOpen(false);
      setAuditDrawerOpen(false);
      setIssuesDrawerOpen(false);
      setOperationTab("review");
      commitModel(created.model);
      recordStoredBase(created);
      if (verifiedBlankResponse) setSavedModelBasis({ generation: projectSessionGenerationRef.current, revision: uiModelRevisionRef.current, hash: returnedHash!.value, source: "create" });
      setSelection(defaultSelection(created.model));
      modelEpoch = modelCommitEpochRef.current;
      setUndoStack([]);
      sessionEvents.emit({ type: "history-reset", projectId: created.model.project.id });
      setRedoStack([]);
      setAppliedOperations([]);
      withdrawBatchRegistrations();
      setQueuedBatches([]);
      setBatchOutcomes({});
      setBatchReceipts([]);
      setBatchMessage(null);
      setOperationOutcomes({});
      setOperationMessage(null);
      setResult(null);
      setAnalysisRun(null);
      setInputManifest(null);
      setRuleCheckAggregate(null);
      setProposal(null);
      setRetainedReviewContext(created.editor_intents ?? []);
      setEditorIntents([]);
      setSelectedReviewTarget(null);
      setSolveJob(blankProjectCreatedSolveJob(created.model));
      setProjectSummary(createdSummary);
      setProjectEnvelopeHash(created.project_envelope_hash ?? null);
      setModelHash(created.model_hash ?? blankModelHash);
      setModelDocumentVersion(created.model_document_version ?? null);
      setProjectMessage(createdSummary.message);
      setProjectOperation("create_blank");
    } catch (error) {
      if (!stillCurrent()) return;
      setProjectMessage(`Blank create failed: ${nativeFailureText(error)}`);
      setProjectOperation("create_blank_failed");
    } finally {
      releaseProjectOperation(owner);
    }
  }

  async function handleOpenProject(projectId: string | null = null) {
    // Another project operation or prompt owns the session: nothing starts.
    if (projectSessionBusy()) return;
    // An open replaces the working model: with unsaved edits it asks first.
    if (replacingNeedsConfirmation()) {
      const guarded = await confirmReplacingEdits({
        action: projectId ? `Opening local project ${projectId}` : "Opening the most recent local project",
        verb: "open it"
      });
      if (guarded !== "proceed") {
        ++projectRequest.current;
        setProjectMessage(unsavedChangesRefusal(guarded, "Not opened"));
        setProjectOperation("open_kept_edits");
        return;
      }
    }
    const owner = acquireProjectOperation();
    if (!owner) return;
    const request = ++projectRequest.current;
    let epoch = requestEpochRef.current;
    const stillCurrent = () => request === projectRequest.current && epoch === requestEpochRef.current;
    let recovery: StoredDocumentExportTarget | null = null;
    try {
      const opened = await openLocalProject(projectId);
      if (!stillCurrent()) return;
      if (!opened) {
        setProjectMessage(
          projectId ? `No local project snapshot found for ${projectId}.` : "No local project snapshot found."
        );
        setProjectOperation("open_missing");
        return;
      }
      const restoredHistory = await buildHistoricalRunContext(opened);
      if (!stillCurrent()) return;
      // The open commits here. An open that finds nothing, fails or is
      // superseded leaves the open project's rule revision gate and integrity
      // cells as they were.
      ruleRevisionGate.current.invalidate();
      setModelHashIntegrity(null);
      setProjectEnvelopeHashIntegrity(null);
      advanceProjectSession();
      commitModel(opened.model);
      recordStoredBase(opened);
      const openedGeneration = projectSessionGenerationRef.current;
      const openedRevision = uiModelRevisionRef.current;
      const openedBasisSequence = ++savedBasisSequence.current;
      const observationOwner = { request, generation: openedGeneration, projectId: opened.model.project.id, basisSequence: openedBasisSequence };
      const stillOwnsOpenedObservation = () => ownsOpenPersistenceObservation(observationOwner, {
        request: projectRequest.current, generation: projectSessionGenerationRef.current,
        projectId: currentModel.current?.project.id, basisSequence: savedBasisSequence.current
      });
      setSelection(defaultSelection(opened.model));
      epoch = requestEpochRef.current;
      setUndoStack([]);
      sessionEvents.emit({ type: "history-reset", projectId: opened.model.project.id });
      setRedoStack([]);
      setAppliedOperations([]);
      withdrawBatchRegistrations();
      setQueuedBatches([]);
      setBatchOutcomes({});
      setBatchReceipts([]);
      setBatchMessage(null);
      setOperationOutcomes({});
      setOperationMessage(null);
      setHistoricalRun(restoredHistory);
      setResult(null);
      setAnalysisRun(null);
      // Persisted analysis-run refs do not include the exact current-session
      // manifest payload needed to recompute its hash. A new solve is required
      // before report-package save can become ready.
      setInputManifest(null);
      setRuleCheckAggregate(null);
      setProposal(opened.proposal ?? null);
      setRetainedReviewContext(opened.editor_intents ?? []);
      setEditorIntents([]);
      setSelectedReviewTarget(opened.selected_review_target ?? null);
      setSolveJob(initialSolveJob());
      setProjectSummary(opened.summary);
      setProjectEnvelopeHash(opened.project_envelope_hash ?? null);
      setModelDocumentVersion(opened.model_document_version ?? null);
      // W-13 §5.3: the validator's warnings show at project load (blocking
      // findings were refused by the store).
      setProjectMessage(`${opened.summary.message}${modelFileWarningSuffix(modelDocumentSlotValidation(opened.model).warnings)}`);
      setProjectOperation(projectId ? "open_by_id" : "open");
      setActiveSection(restoredHistory ? "results" : null);
      const libraryWarnings = await libraryReferenceWarnings(opened.model);
      if (libraryWarnings && stillCurrent()) setProjectMessage((message) => `${message}${libraryWarnings}`);
      const recomputedHash = await computeModelHash(opened.model);
      if (recomputedHash && openedGeneration === projectSessionGenerationRef.current && openedBasisSequence === savedBasisSequence.current) {
        setSavedModelBasis({ generation: openedGeneration, revision: openedRevision, hash: recomputedHash.value, source: "open" });
      }
      // D5 §3: the opened project's autosaves are offered once it has opened.
      void autosave.afterStoredProjectOpened(opened.model.project.id, recomputedHash?.value ?? null);
      if (!stillOwnsOpenedObservation()) return;
      setModelHashIntegrity(deriveModelHashIntegrity(opened.model_hash ?? null, recomputedHash, opened.model.project.id));
      const recomputedEnvelopeHash = await computeProjectEnvelopeHash({
        model: opened.model,
        editor_intents: opened.editor_intents ?? [],
        proposal: opened.proposal ?? null,
        selected_review_target: opened.selected_review_target ?? null,
        mechanics_result: opened.mechanics_result ?? null,
        analysis_run: opened.analysis_run ?? null,
        model_hash: opened.model_hash ?? null
      });
      if (!stillOwnsOpenedObservation()) return;
      setProjectEnvelopeHashIntegrity(
        deriveProjectEnvelopeHashIntegrity(
          opened.project_envelope_hash ?? null,
          recomputedEnvelopeHash,
          opened.model.project.id
        )
      );
    } catch (error) {
      if (!stillCurrent()) return;
      setProjectMessage(`Open failed: ${String(error)}`);
      setProjectOperation("open_failed");
      // W-17: a stored project refused for lacking project.units is offered the
      // recovery export (desktop store only); nothing was adopted.
      if (error instanceof StoredProjectUnitsRefusal && isTauriRuntime()) {
        recovery = { projectId: error.projectId, stateId: null, description: storedProjectDescription(error.projectId), refusal: error.message };
      }
    } finally {
      releaseProjectOperation(owner);
    }
    if (recovery) {
      requestStoredDocumentExport(recovery, (message, operation) => {
        setProjectMessage(message);
        setProjectOperation(operation);
      });
    }
  }

  /** File > Open Model Document…: adopt a model document file from disk as the
   * session's model, unchanged. It starts unsaved, as the bundled demo does; New
   * Local Project saves it as a project. A refusal leaves the session as it was. */
  async function handleOpenModelDocument(source: ModelDocumentSource = MODEL_DOCUMENT_FILE_SOURCE) {
    // Another project operation or prompt owns the session: nothing starts.
    if (projectSessionBusy()) return;
    // An open replaces the working model: with unsaved edits it asks first.
    if (replacingNeedsConfirmation()) {
      const guarded = await confirmReplacingEdits({ action: source.action, verb: "open it" });
      if (guarded !== "proceed") {
        ++projectRequest.current;
        setProjectMessage(unsavedChangesRefusal(guarded, "Not opened"));
        setProjectOperation("open_model_kept_edits");
        return;
      }
    }
    const owner = acquireProjectOperation();
    if (!owner) return;
    const request = ++projectRequest.current;
    const epoch = requestEpochRef.current;
    const stillCurrent = () => request === projectRequest.current && epoch === requestEpochRef.current;
    try {
      const opened = await source.read();
      if (!stillCurrent() || opened.outcome === "cancelled") return;
      if (opened.outcome === "refused") {
        setProjectMessage(modelFileRefusalMessage(opened.file_name, opened.diagnostics));
        setProjectOperation("open_model_refused");
        return;
      }
      const document = opened.document;
      // Last guard behind the shape check: a document the desktop cannot index
      // is refused here rather than unmounting the workspace after adoption.
      try {
        buildModelIndex(document, 0, 0);
      } catch (error) {
        setProjectMessage(modelFileRefusalMessage(opened.file_name, [{
          code: MODEL_FILE_SHAPE, path: "", message: `The desktop could not index the document: ${String(error)}.`
        }]));
        setProjectOperation("open_model_refused");
        return;
      }
      ruleRevisionGate.current.invalidate();
      setModelHashIntegrity(null);
      setProjectEnvelopeHashIntegrity(null);
      advanceProjectSession();
      commitModel(document);
      storedBaseRef.current = null;
      const generation = projectSessionGenerationRef.current;
      const revision = uiModelRevisionRef.current;
      const sequence = ++savedBasisSequence.current;
      setSavedModelBasis({ generation, revision, hash: null, source: "loaded-source" });
      setSelection(defaultSelection(document));
      setUndoStack([]);
      sessionEvents.emit({ type: "history-reset", projectId: document.project.id });
      setRedoStack([]);
      setAppliedOperations([]);
      withdrawBatchRegistrations();
      setQueuedBatches([]);
      setBatchOutcomes({});
      setBatchReceipts([]);
      setBatchMessage(null);
      setOperationOutcomes({});
      setOperationMessage(null);
      setHistoricalRun(null);
      setResult(null);
      setAnalysisRun(null);
      setInputManifest(null);
      setRuleCheckAggregate(null);
      setProposal(null);
      setRetainedReviewContext([]);
      setEditorIntents([]);
      setSelectedReviewTarget(null);
      setSolveJob(initialSolveJob());
      setProjectSummary(null);
      setProjectEnvelopeHash(null);
      setModelDocumentVersion(null);
      setProjectMessage(`${source.opened(opened)} Not saved as a local project yet.${modelFileWarningSuffix(opened.warnings)}`);
      setProjectOperation(source.operation);
      setActiveSection(null);
      const libraryWarnings = await libraryReferenceWarnings(document);
      if (libraryWarnings && stillCurrent()) setProjectMessage((message) => `${message}${libraryWarnings}`);
      const hash = await computeModelHash(document);
      if (generation === projectSessionGenerationRef.current && sequence === savedBasisSequence.current) {
        setSavedModelBasis({ generation, revision, hash: hash?.value ?? null, source: "loaded-source" });
      }
    } catch (error) {
      if (!stillCurrent()) return;
      setProjectMessage(`Open model document failed: ${String(error)}`);
      setProjectOperation("open_model_failed");
    } finally {
      releaseProjectOperation(owner);
    }
  }

  /** File > Save Model Document… (DEL-15-01 W-6a): asks for the explicit
   * local-private intent first. Available whenever a model is open, on either
   * route; it needs no solve. Nothing happens while another project operation
   * or modal is open. */
  function requestSaveModelDocument() {
    const saveModel = modelDocumentSaveBasisRef.current.model;
    if (!saveModel) return;
    if (replacePromptOpenRef.current || projectUnitsDialogOpenRef.current || modelDocumentSaveDialogOpenRef.current || handoffSaveDialogOpenRef.current || projectOperationOwner.current !== null) return;
    // Captured before the workspace turns inert, which drops its focus.
    const opener = document.activeElement instanceof HTMLElement ? document.activeElement : null;
    const close = () => { modelDocumentSaveDialogOpenRef.current = false; setModelDocumentSaveRequest(null); };
    modelDocumentSaveDialogOpenRef.current = true;
    setModelDocumentSaveRequest({
      projectName: saveModel.project.name,
      opener,
      cancel: close,
      save: (explicitLocalPrivateIntent) => {
        close();
        void handleSaveModelDocument(explicitLocalPrivateIntent);
      }
    });
  }

  /** W-17 recovery export (`storedDocumentExport.ts`): offers to save a stored
   * document the open refused for lacking `project.units` to a file, exactly as
   * stored, behind the Save Model Document dialog's explicit intent. Nothing is
   * adopted; `report` gets the outcome's status line. False when another
   * operation or modal owns the session (nothing is offered then). */
  function requestStoredDocumentExport(target: StoredDocumentExportTarget, report: (message: string, operation: string) => void): boolean {
    if (projectSessionBusy()) return false;
    const opener = document.activeElement instanceof HTMLElement ? document.activeElement : null;
    const close = () => { modelDocumentSaveDialogOpenRef.current = false; setModelDocumentSaveRequest(null); };
    modelDocumentSaveDialogOpenRef.current = true;
    setModelDocumentSaveRequest({
      projectName: target.projectId,
      opener,
      cancel: close,
      recovery: { description: target.description, refusal: target.refusal },
      save: (explicitLocalPrivateIntent) => {
        close();
        void handleStoredDocumentExport(target, explicitLocalPrivateIntent, report);
      }
    });
    return true;
  }

  async function handleStoredDocumentExport(target: StoredDocumentExportTarget, explicitLocalPrivateIntent: boolean, report: (message: string, operation: string) => void) {
    const owner = acquireProjectOperation();
    if (!owner) return;
    ++projectRequest.current;
    try {
      const outcome = await saveStoredModelDocumentFile(target, explicitLocalPrivateIntent);
      report(storedDocumentExportMessage(target, outcome), outcome.outcome === "saved" ? "export_stored_document"
        : outcome.outcome === "cancelled" ? "export_stored_document_cancelled" : "export_stored_document_refused");
    } catch (error) {
      report(storedDocumentExportFailureMessage(target, error), "export_stored_document_failed");
    } finally {
      releaseProjectOperation(owner);
    }
  }

  /** Saves the session's model document under the dialog's intent. Reads the
   * session and changes only the status line: the model, its hash, the results
   * and the solve standing are untouched. */
  async function handleSaveModelDocument(explicitLocalPrivateIntent: boolean) {
    const { model: saveModel, modelHash: saveHash } = modelDocumentSaveBasisRef.current;
    if (!saveModel) return;
    const owner = acquireProjectOperation();
    if (!owner) return;
    ++projectRequest.current;
    try {
      const libraries = await resolveLibraryDispositions(saveModel);
      const prepared = await prepareModelDocumentSave({ model: saveModel, modelHash: saveHash, explicitLocalPrivateIntent, libraries });
      if (prepared.status === "refused") {
        setProjectMessage(modelDocumentSaveRefusalMessage(prepared.diagnostics));
        setProjectOperation("save_model_document_refused");
        return;
      }
      const outcome = await saveModelDocumentFile(prepared.args);
      setProjectMessage(modelDocumentSaveMessage(outcome));
      setProjectOperation(outcome.outcome === "saved" ? "save_model_document"
        : outcome.outcome === "cancelled" ? "save_model_document_cancelled" : "save_model_document_refused");
    } catch (error) {
      setProjectMessage(modelDocumentSaveFailureMessage(error));
      setProjectOperation("save_model_document_failed");
    } finally {
      releaseProjectOperation(owner);
    }
  }

  /** File > Save Handoff… (DEL-15-01 W-6b): finds the basis (the project's saved
   * state of this model, or a new `handoff_basis` state to confirm) and asks for
   * the explicit local-private intent. Desktop only (states live in the native
   * store); it needs no solve. Nothing happens while another project operation
   * or modal is open. */
  async function requestSaveHandoff() {
    const { model: saveModel, modelHash: saveHash } = modelDocumentSaveBasisRef.current;
    if (!saveModel || projectSessionBusy()) return;
    // This request's project-command generation; nothing below advances it.
    const request = ++projectRequest.current;
    const refuse = (code: string, message: string) => {
      setProjectMessage(handoffSaveRefusalMessage([{ code, path: "", message }]));
      setProjectOperation("save_handoff_refused");
    };
    if (!isTauriRuntime()) return refuse(HANDOFF_SAVE_DESKTOP_ONLY, "Saving a handoff package needs the desktop app: its basis is a saved model state in the local store.");
    if (!saveHash) return refuse(MODEL_DOC_SAVE_HASH_PENDING, "The session's model hash is not computed yet; try again once it is shown.");
    // Captured before the workspace turns inert, which drops its focus.
    const opener = document.activeElement instanceof HTMLElement ? document.activeElement : null;
    // The session moved on while the states were listed (a newer project
    // command started, the model or its hash changed, or an operation or prompt
    // owns the session): the listing's outcome, success or failure, is dropped,
    // so it cannot overwrite a newer status line or open a dialog over it.
    const saveHashValue = saveHash.value;
    const sessionMovedOn = () => projectRequest.current !== request
      || modelDocumentSaveBasisRef.current.model !== saveModel
      || modelDocumentSaveBasisRef.current.modelHash?.value !== saveHashValue || projectSessionBusy();
    let basis: HandoffBasis;
    try {
      // The basis is chosen among the readable saved states; a row the store
      // cannot read (W-12) is never a basis.
      basis = handoffBasis((await listModelStates(saveModel.project.id)).states, saveModel.project.id, saveHashValue);
    } catch (error) {
      if (sessionMovedOn()) return;
      setProjectMessage(handoffSaveFailureMessage(error));
      setProjectOperation("save_handoff_failed");
      return;
    }
    // Nothing is asked of a session that moved on.
    if (sessionMovedOn()) return;
    const close = () => { handoffSaveDialogOpenRef.current = false; setHandoffSaveRequest(null); };
    handoffSaveDialogOpenRef.current = true;
    setHandoffSaveRequest({
      projectName: saveModel.project.name,
      basis,
      opener,
      cancel: close,
      save: (choice) => {
        close();
        void handleSaveHandoff(choice, basis, saveModel);
      }
    });
  }

  /** Saves the handoff under the dialog's answers. A new basis state is saved
   * through W-12 S1's store first (after Save Local Project's flow when the
   * session is not that stored project), then the package is published; a
   * state left by a refused or cancelled publication stays and is reused.
   * Changes only the status line (and, for a new state, the History list). */
  async function handleSaveHandoff(choice: HandoffSaveChoice, basis: HandoffBasis, dialogModel: PreviewModel) {
    ++projectRequest.current;
    let saveModel = modelDocumentSaveBasisRef.current.model;
    let saveHash = modelDocumentSaveBasisRef.current.modelHash;
    const refuse = (message: string, operation = "save_handoff_refused") => {
      setProjectMessage(`Save handoff refused: ${message}`);
      setProjectOperation(operation);
    };
    if (!saveModel || saveModel !== dialogModel) return refuse("the working model changed while the dialog was open; nothing was saved.", "save_handoff_superseded");
    let stateId = basis.kind === "existing" ? basis.state.state_id : null;
    let parentStateId = history.basisStateId;
    if (stateId === null && !isStoredProjectFor(saveModel.project.id)) {
      setProjectMessage("A handoff basis state needs its project's stored copy: saving the local project first.");
      const landed = await saveLocalProjectFirst();
      if (!landed || !isStoredProjectFor(landed.projectId)) return refuse("the local project was not saved, so no basis state and no package were saved.", "save_handoff_needs_project");
      if (currentModel.current !== landed.model) return refuse("the working model changed while the local project was saved; nothing else was saved.", "save_handoff_superseded");
      // After "Save as a new project" the working model is the renamed copy.
      if (landed.projectId !== saveModel.project.id) parentStateId = null;
      saveModel = landed.model;
      saveHash = await computeModelHash(saveModel);
    }
    const owner = acquireProjectOperation();
    if (!owner) return refuse("another project operation is in progress; try again when it finishes.", "save_handoff_busy");
    let basisNote = "";
    try {
      const libraries = await resolveLibraryDispositions(saveModel);
      const prepared = await prepareModelDocumentSave({
        model: saveModel, modelHash: saveHash, explicitLocalPrivateIntent: choice.explicitLocalPrivateIntent, libraries, route: HANDOFF_SAVE_ROUTE
      });
      if (prepared.status === "refused") {
        setProjectMessage(handoffSaveRefusalMessage(prepared.diagnostics));
        setProjectOperation("save_handoff_refused");
        return;
      }
      if (stateId === null) {
        const saved = await saveModelState({
          expectedBase: storedBaseRef.current!.value!,
          model: saveModel,
          kind: "handoff_basis",
          parentStateId,
          labels: { state_name: choice.newStateName ?? "", tags: [], notes: [], assumptions: [] }
        });
        stateId = saved.state.state_id;
        basisNote = saved.outcome === "saved"
          ? `Saved model state ${modelStateDescription(saved.state)} as the handoff basis; it stays saved.`
          : `This model was already saved as state ${modelStateDescription(saved.state)}; that state is the basis.`;
        void history.refreshStates(saveModel.project.id);
      }
      const outcome = await saveHandoffPackage({ ...prepared.args, basisStateId: stateId, packageLabel: choice.packageLabel });
      setProjectMessage(handoffSaveMessage(outcome, basisNote));
      setProjectOperation(outcome.outcome === "saved" ? "save_handoff"
        : outcome.outcome === "cancelled" ? "save_handoff_cancelled" : "save_handoff_refused");
    } catch (error) {
      setProjectMessage(`${handoffSaveFailureMessage(error)}${basisNote ? ` ${basisNote}` : ""}`);
      setProjectOperation("save_handoff_failed");
    } finally {
      releaseProjectOperation(owner);
    }
  }

  /** The session is the stored project `projectId`, with a stored base. */
  function isStoredProjectFor(projectId: string): boolean {
    return storedBaseRef.current?.projectId === projectId && Boolean(storedBaseRef.current.value);
  }

  async function handleSaveProject() {
    return saveProject(null);
  }

  /** `saveAsNew`: the renamed document after the user chose Save as a new
   * project. The session already holds it; the run solved under the old
   * identity is not written under the new one. */
  async function saveProject(saveAsNew: PreviewModel | null) {
    if (!model) return;
    const owner = acquireProjectOperation();
    if (!owner) return;
    const request = ++projectRequest.current;
    let epoch = requestEpochRef.current;
    // Save as a new project follows the session's own adoption of the renamed
    // document, after which the shell may settle its selection; that write is
    // current while the session still holds exactly that document.
    const stillCurrent = () => request === projectRequest.current &&
      (saveAsNew ? currentModel.current === saveAsNew : epoch === requestEpochRef.current);
    const requestModel = saveAsNew ?? model;
    const dropRun = saveAsNew !== null;
    let pendingSaveAsNew: PreviewModel | null = null;
    const generation = projectSessionGenerationRef.current;
    const requestRevision = uiModelRevisionRef.current;
    const sameProjectSession = () => generation === projectSessionGenerationRef.current && currentModel.current?.project.id === requestModel.project.id;
    const retainedRun = dropRun ? null : retainedReferencePersistence(requestModel);
    const requestHistoricalRun = dropRun ? null : historicalRun?.designation === "historical_saved_run" ? historicalRun : retainedRun?.history ?? null;
    let pendingObservation: { envelope: LocalProjectEnvelope; ordinal: number } | null = null;
    try {
      const combinedContext = structuredClone([...retainedReviewContext, ...editorIntents, ...queuedBatches.flatMap((entry) => entry.batch.operations)]);
      const actualRequestModelHash = await computeModelHash(requestModel);
      const snapshotModelHash = requestHistoricalRun ? requestHistoricalRun.modelHash : actualRequestModelHash;
      const snapshotResult = requestHistoricalRun ? requestHistoricalRun.rawMechanicsResult as MechanicsResult | null : retainedRun?.result ?? (dropRun ? null : result);
      const snapshotAnalysisRun = requestHistoricalRun ? requestHistoricalRun.rawAnalysisRun as AnalysisRunEnvelope | null : retainedRun?.analysisRun ?? (dropRun ? null : analysisRun);
      if (!stillCurrent()) return;
      const computedEnvelopeHash = await computeProjectEnvelopeHash({
        model: requestModel,
        editor_intents: combinedContext,
        proposal,
        selected_review_target: selectedReviewTarget,
        mechanics_result: snapshotResult,
        analysis_run: snapshotAnalysisRun,
        model_hash: snapshotModelHash
      });
      const envelopeHash = requestHistoricalRun && computedEnvelopeHash?.value === requestHistoricalRun.envelopePayloadHash
        ? requestHistoricalRun.envelopeHash : computedEnvelopeHash;
      if (!stillCurrent()) return;
      const written = await writeWithReplaceConfirmation("save", requestModel, (confirmedRevision) => saveLocalProject(
          requestModel,
          combinedContext,
          proposal,
          selectedReviewTarget,
          snapshotResult,
          snapshotAnalysisRun,
          snapshotModelHash,
          envelopeHash,
          confirmedRevision,
          // The session's own stored project: a save in place from the revision it
          // last opened or wrote. Without a recorded hash there is no base to
          // check, and the save asks.
          storedBaseRef.current?.projectId === requestModel.project.id ? storedBaseRef.current.value : null
        ));
      if (written.outcome === "kept") {
        setProjectMessage(keptStoredProjectMessage(written.existing));
        setProjectOperation("save_kept_stored_project");
        return;
      }
      if (written.outcome === "save-as-new") {
        pendingSaveAsNew = written.model;
        return;
      }
      const saved = written.envelope;
      const writeObservation = ++persistedWriteObservation.current;
      if (!sameProjectSession()) return;
      pendingObservation = { envelope: saved, ordinal: writeObservation };
      if (saved.summary.project_id === requestModel.project.id) recordStoredBase(saved);
      // Retire the old observation while verification of rewritten bytes is pending.
      setModelHashIntegrity(null);
      setProjectEnvelopeHashIntegrity(null);
      const returnedModelHash = await computeModelHash(saved.model);
      if (!sameProjectSession()) return;
      const recomputedReturnedEnvelopeHash = await computeProjectEnvelopeHash({
        model: saved.model,
        editor_intents: saved.editor_intents,
        proposal: saved.proposal,
        selected_review_target: saved.selected_review_target,
        mechanics_result: saved.mechanics_result,
        analysis_run: saved.analysis_run,
        model_hash: saved.model_hash
      });
      if (!sameProjectSession()) return;
      const responseModelChanged = returnedModelHash?.value !== actualRequestModelHash?.value;
      const verifiedResponse = Boolean(actualRequestModelHash && returnedModelHash &&
        saved.model.project.id === requestModel.project.id &&
        saved.summary.project_id === requestModel.project.id &&
        persistenceHashesMatch(saved, returnedModelHash, recomputedReturnedEnvelopeHash, !responseModelChanged ? requestHistoricalRun?.modelHash ?? null : null) &&
        !responseModelChanged);
      recordPersistenceObservation(saved, returnedModelHash, recomputedReturnedEnvelopeHash, "save", generation, writeObservation, verifiedResponse, requestModel.project.id, Boolean(verifiedResponse && requestHistoricalRun && !responseModelChanged));
      pendingObservation = null;
      if (saved.model.project.id !== requestModel.project.id || saved.summary.project_id !== requestModel.project.id) {
        if (!stillCurrent()) return;
        setProjectMessage("Save failed: PROJECT-PERSISTENCE-RESPONSE-INTEGRITY: returned project identity does not match the requested project.");
        setProjectOperation("save_failed");
        return;
      }
      if (responseModelChanged) {
        if (!stillCurrent()) return;
        setProjectMessage("Save failed: PROJECT-PERSISTENCE-RESPONSE-INTEGRITY: the returned model differs from the requested model; the store never rewrites a model document.");
        setProjectOperation("save_failed");
        return;
      }
      // Failed/missing later requests do not retire an actual same-session
      // write. Only a newer verified fulfillment may supersede this observation;
      // current-only metadata/model/history adoption keeps its stricter gate.
      const verifiedBasis = verifiedWriteBasis(verifiedResponse, generation, projectSessionGenerationRef.current,
        writeObservation, latestVerifiedWriteObservation.current, responseModelChanged ? -1 : requestRevision, returnedModelHash, "save");
      if (verifiedBasis) {
        latestVerifiedWriteObservation.current = writeObservation;
        savedBasisSequence.current += 1;
        setSavedModelBasis(verifiedBasis);
      }
      if (!stillCurrent()) return;
      const returnedHistory = requestHistoricalRun
        ? await buildHistoricalRunContext(saved)
        : null;
      if (!stillCurrent()) return;
      if (requestHistoricalRun) {
        // Preserve a fresh Current solve that completed while the native save
        // was pending. Only the still-owned Historical snapshot may refresh.
        setHistoricalRun((current) => current === requestHistoricalRun ? returnedHistory : current);
      }
      setProjectSummary(saved.summary);
      setProposal(saved.proposal ?? null);
      setSelectedReviewTarget(saved.selected_review_target ?? null);
      setProjectEnvelopeHash(saved.project_envelope_hash ?? null);
      setModelDocumentVersion(saved.model_document_version ?? null);
      setProjectMessage(saved.summary.message);
      projectSaveLanded.current = { projectId: saved.summary.project_id, base: saved.project_envelope_hash?.value ?? null, model: requestModel };
      setProjectOperation("save");
      void autosave.afterProjectSaved(saved.summary.project_id, returnedModelHash?.value ?? null);
    } catch (error) {
      if (pendingObservation && sameProjectSession() &&
        pendingObservation.envelope?.model?.project?.id === requestModel.project.id &&
        pendingObservation.envelope?.summary?.project_id === requestModel.project.id) {
        recordPersistenceObservation(pendingObservation.envelope, null, null, "save", generation,
          pendingObservation.ordinal, false, requestModel.project.id);
      }
      if (!stillCurrent()) return;
      setProjectMessage(`Save failed: ${nativeFailureText(error)}`);
      setProjectOperation("save_failed");
    } finally {
      releaseProjectOperation(owner);
      // Save as a new project: adopt the renamed document, then write it as a
      // project of its own (an early return in the try block still reaches here).
      if (pendingSaveAsNew && stillCurrent()) {
        adoptSavedAsNewModel(pendingSaveAsNew);
        await saveProject(pendingSaveAsNew);
      } else if (pendingSaveAsNew) {
        setProjectMessage(SAVE_AS_NEW_SUPERSEDED);
        setProjectOperation("save_superseded");
      }
    }
  }

  async function handleListProjects() {
    const owner = acquireProjectOperation();
    if (!owner) return;
    ++projectRequest.current;
    try {
      const listed = await listLocalProjects();
      setProjectIndex(listed);
      setProjectMessage(
        `Listed ${listed.length} local project snapshot${listed.length === 1 ? "" : "s"} from the local store index.`
      );
      setProjectOperation("list");
    } catch (error) {
      setProjectMessage(`List failed: ${String(error)}`);
      setProjectOperation("list_failed");
    } finally {
      releaseProjectOperation(owner);
    }
  }

  function handleSelectResult(resultId: string) {
    setSelectedReviewTarget({ target_type: "result", id: resultId });
    const item = result?.results.find((candidate) => candidate.id === resultId);
    if (!item || !model) return;
    const entitySelection = resolveEntitySelection(model, item.entity_ref);
    if (entitySelection) {
      handleSelectEntity(entitySelection);
    }
  }

  function handleSelectDiagnostic(diagnosticId: string) {
    setSelectedReviewTarget({ target_type: "diagnostic", id: diagnosticId });
    if (!model) return;
    const entitySelection = resolveDiagnosticEntitySelection({ model, result, knowledge, diagnosticId });
    if (entitySelection) {
      handleSelectEntity(entitySelection);
    }
  }

  function handleSelectEntity(
    entity: EntityRef,
    modifiers: SelectionModifiers & Readonly<{ range?: boolean }> = {},
    displayedOrder: readonly EntityKey[] = []
  ): OrderedSelectionState {
    const next = modifiers.range
      ? applyDisplayedRange(orderedSelectionRef.current, entity, displayedOrder)
      : applySelection(orderedSelectionRef.current, entity, modifiers);
    commitSelectionState(next);
    return orderedSelectionRef.current;
  }

  function handleBoxSelection(
    keys: readonly EntityKey[],
    modifiers: SelectionModifiers
  ): OrderedSelectionState {
    const next = applyBoxSelection(orderedSelectionRef.current, keys, modifiers);
    commitSelectionState(next);
    return next;
  }

  function invalidateDirectDraftContext() {
    requestEpochRef.current += 1;
    setRequestEpoch(requestEpochRef.current);
    directDraftReviews.current.clear();
  }

  function handleArmCreationTool(tool: CreationTool | null) {
    viewportViewCommandRef.current?.({ type: "cancel-box-selection" });
    if ((tool === "node" || tool === "pipe" || tool === "component") && routingInspectorRestore.current === null) {
      routingInspectorRestore.current = inspectorCollapsed;
    }
    setArmedCreationTool(tool);
    if (!tool) return;
    if (tool === "load") {
      setActiveSection("loads");
      return;
    }
    setActiveSection(null);
    revealModelStageCanvas();
    if (tool === "support") {
      openWorkspaceRail("inspector");
      if (selection) setPropertyTaskRequest({
        sequence: ++propertyTaskRequestSequenceRef.current,
        target: { ...selection },
        view: "properties",
        focusTestId: "create-support-id"
      });
    } else {
      exposeViewportForNarrowInteraction(`authoring-${tool}`);
      // Re-selecting an armed routing tool also reveals its inspector home.
      setInspectorCollapsed(false);
    }
  }

  function handleToolkitCommand(capability: ToolkitCapability) {
    if (!selection) return;
    const context = { selection, selectionCardinality: orderedSelectionRef.current.orderedKeys.length, canUndo: undoStack.length > 0, canRedo: redoStack.length > 0, busy: operationRequest.current.busy || operationBusy, windConfigured: Boolean(selection.type === "load" && model?.load_cases.find((load) => load.id === selection.id)?.equivalent_static?.wind) };
    if (!capabilityAvailability(capability, context).enabled) return;
    if (capability.history) {
      if (capability.history === "undo") handleUndoSessionModelEdit();
      else handleRedoSessionModelEdit();
      setToolkitFocus({ testId: "toolkit-entry" });
      return;
    }
    const route = capabilityRoute(capability, context);
    if (!route) return;
    viewportViewCommandRef.current?.({ type: "cancel-box-selection" });
    if ((route.tool === "node" || route.tool === "pipe" || route.tool === "component") && routingInspectorRestore.current === null) {
      routingInspectorRestore.current = inspectorCollapsed;
    }
    setArmedCreationTool(route.tool ?? null);
    if (route.tool && route.surface === "viewport") {
      exposeViewportForNarrowInteraction(`authoring-${route.tool}`);
      // Commit visibility with the focus request. A later auto-open effect is
      // too late for a browser to focus a control in the hidden inspector.
      if (route.tool === "node" || route.tool === "pipe" || route.tool === "component") setInspectorCollapsed(false);
    }
    if (route.surface === "operations") {
      const tabs: Record<string, string> = { "geometry-tools": "geometry", "boundary-authoring": "supports", "hanger-selection": "supports", "self-weight-plan": "weight", "offline-proposal-intake": "agent" };
      setOperationTab(tabs[route.elementId ?? ""] ?? "review");
    }
    if (route.surface === "inspector") {
      setPropertyTaskRequest({
        sequence: ++propertyTaskRequestSequenceRef.current,
        target: { ...selection },
        view: route.inspectorView ?? "properties",
        focusTestId: route.focusTestId,
        elementId: route.elementId
      });
      revealModelStageCanvas();
      openWorkspaceRail("inspector");
      setActiveSection(null);
    }
    else if (route.surface === "tree") { openWorkspaceRail("tree"); setActiveSection(null); }
    else if (route.surface === "viewport") { revealModelStageCanvas(); setActiveSection(null); }
    else setActiveSection(route.surface);
    if (route.surface !== "inspector") setToolkitFocus({ testId: route.focusTestId, elementId: route.elementId });
  }

  // "Within this run" (W-12 S3c): the load case and combination choice. It is
  // disabled with the stated reason, and refused, while another project operation
  // or prompt owns the session (the one-owner check and the modal holds), a solve
  // runs or a report package is being prepared. The choice is the
  // session's choice, revalidated against every Current run (resultsSessionState.ts);
  // a new choice clears the notice of a dropped one.
  const withinRunDisabledReason = withinRunBusyReason({ projectBusy, running, reportPackageBusy });
  const withinRunBusyRef = useRef<string | null>(null);
  withinRunBusyRef.current = withinRunDisabledReason;
  function handleSelectWithinRunBases(pair: WithinRunPair) {
    // The latest render's reason, the one owner and an active solve, read at the
    // call: a handler from an earlier render cannot choose while the session is busy.
    if (withinRunBusyRef.current || projectSessionBusy() || solveRunGate.current.current() !== null || reportPackageBusyGenerationRef.current !== null) return;
    setHeldWithinRunSelection({ left: pair.left, right: pair.right });
    setDroppedWithinRunBases(null);
  }

  async function handleSaveReportPackage() {
    if (!model || !currentSolvedResult || !analysisRun || !inputManifest || running || reportPackageBusy) return;
    const generation = ++reportPackageRequestGenerationRef.current;
    const basis = {
      projectSessionGeneration: projectSessionGenerationRef.current,
      modelRevision: uiModelRevisionRef.current,
      model,
      result: currentSolvedResult,
      inputManifest,
      analysisRun,
      comparison,
      comparisonUnavailable,
      projectSummary,
      ruleCheckAggregate,
      ruleCheckRun: ruleCheckReportRun,
      privateIntent: reportPackagePrivateIntent
    } as const;
    // Refs, because the awaited build and preparation outlive this render's closure.
    const isCurrent = () =>
      reportPackageRequestGenerationRef.current === generation &&
      reportPackageBusyGenerationRef.current === generation &&
      projectSessionGenerationRef.current === basis.projectSessionGeneration &&
      uiModelRevisionRef.current === basis.modelRevision &&
      currentModel.current === basis.model &&
      currentSolvedResultRef.current === basis.result &&
      currentInputManifestRef.current === basis.inputManifest &&
      analysisBasisRef.current.value === basis.analysisRun &&
      ruleCheckAggregateRef.current === basis.ruleCheckAggregate &&
      ruleCheckReportRunRef.current === basis.ruleCheckRun;
    reportPackageBusyGenerationRef.current = generation;
    setReportPackageBusy(true);
    setReportPackageRoute(null);
    try {
      const request = await buildReportPackageRequest({
        model: basis.model,
        result: basis.result,
        analysisRun: basis.analysisRun,
        inputManifest: basis.inputManifest,
        projectSummary: basis.projectSummary,
        comparison: basis.comparison,
        comparisonUnavailable: basis.comparisonUnavailable,
        ruleCheckAggregate: basis.ruleCheckAggregate,
        ruleCheckRun: basis.ruleCheckRun
      });
      if (!isCurrent()) return;
      const controlled = controlReportPackageRequest(request, basis.privateIntent);
      setReportPackageRedaction(controlled);
      if (controlled.blocked || controlled.payload === null) {
        setReportPackageRoute({
          route: "redaction_blocked",
          diagnostic: `REPORT-PACKAGE-REDACTION-BLOCKED: ${controlled.findings.length} finding(s) prevent package assembly or persistence.`
        });
        return;
      }
      // W-11 (DEL-08-01 Design `exact-route-report-sections.md` §3.1, §3.6): a request
      // from an exact source carries the texts the native save binds, and its admission
      // is re-checked immediately before each send (null for a pressure-free request).
      const exactSubmission = reportPackageExactSubmission(request);
      const prepared = await prepareReportPackageSave(controlled, basis.model, request, basis.inputManifest.manifest, exactSubmission);
      if (!isCurrent()) return;
      if (prepared.route !== "ready") {
        setReportPackageRoute(prepared);
        return;
      }
      const exactStillCurrent = () => {
        if (exactSubmission === null) return true;
        try { reportPackageExactSubmission(request); return true; } catch { return false; }
      };
      // The last guard runs inside the invocation, immediately before each send.
      const saved = await invokeReportPackageSave(prepared, () => isCurrent() && exactStillCurrent());
      if (!isCurrent()) return;
      setReportPackageRoute(saved);
    } catch (error) {
      // A basis retired before a send: nothing was sent, and the newer basis owns the state.
      if (error instanceof IngressRequestRetiredError || !isCurrent()) return;
      setReportPackageRedaction(null);
      setReportPackageRoute({
        route: "redaction_blocked",
        diagnostic: formatPackageSaveError(error)
      });
    } finally {
      if (isCurrent()) {
        reportPackageBusyGenerationRef.current = null;
        setReportPackageBusy(false);
      }
    }
  }

  // B11 on-demand model checks (DEL-04-06 Design `on-demand-model-checks.md`):
  // the session's last run, shown in the Issues drawer. The checks read the
  // model as it stands and never change it.
  // In the app the solve's checks run natively under the memory pool, so a run
  // is asynchronous: a later request (or a new project session) supersedes it.
  const [modelCheckRun, setModelCheckRun] = useState<ModelCheckRun | null>(null);
  const [modelCheckBusy, setModelCheckBusy] = useState(false);
  const modelCheckRequest = useRef(0);
  // Whether the latest request is a native check still in progress.
  const nativeModelCheckInFlight = useRef(false);
  // A new project session retires a run in progress and the last run's list
  // (Codex review r2 of #1665): neither describes the new session's model.
  // A native check in progress is cancelled, so its worker's grant is
  // released (Codex review r3).
  useEffect(() => {
    modelCheckRequest.current += 1;
    if (nativeModelCheckInFlight.current) void cancelNativeModelChecks();
    nativeModelCheckInFlight.current = false;
    setModelCheckBusy(false);
    setModelCheckRun(null);
  }, [projectSessionGeneration]);
  async function handleRunModelChecks() {
    if (!model) return;
    const request = ++modelCheckRequest.current;
    const generation = projectSessionGenerationRef.current;
    setIssuesDrawerOpen(true);
    setModelCheckBusy(true);
    nativeModelCheckInFlight.current = isTauriRuntime();
    const run = await runModelChecks(model, () => libraryRefDiagnostics(currentLibraryRefFindings(model)));
    if (request !== modelCheckRequest.current || generation !== projectSessionGenerationRef.current) return;
    nativeModelCheckInFlight.current = false;
    setModelCheckBusy(false);
    setModelCheckRun(run);
  }

  // Single command sink for both the in-DOM menu bar (tested) and the native
  // macOS menu bar (Tauri shell only). View commands summon/dismiss workspace
  // sections and toggle the tree/inspector rails; the spatial core (tree |
  // viewport | inspector) is always present, so Insert commands arm the same
  // creation tools exposed in the command bar instead of acting as navigation.
  function runMenuCommand(command: MenuCommandId) {
    if (replacePromptOpenRef.current || projectUnitsDialogOpenRef.current || modelDocumentSaveDialogOpenRef.current || handoffSaveDialogOpenRef.current) return;
    setOpenMenu(null);
    switch (command) {
      case "file.new-local":
        void handleCreateProject();
        break;
      case "file.new-blank":
        requestBlankProject("local");
        break;
      case "file.open-model":
        void handleOpenModelDocument();
        break;
      case "file.open-local":
        void handleOpenProject();
        break;
      case "file.list-local":
        void handleListProjects();
        break;
      case "file.save-local":
        void handleSaveProject();
        break;
      case "file.save-model-document":
        requestSaveModelDocument();
        break;
      case "file.save-handoff":
        void requestSaveHandoff();
        break;
      case "file.save-report-package":
        setActiveSection("report");
        void handleSaveReportPackage();
        break;
      case "edit.undo":
        handleUndoSessionModelEdit();
        break;
      case "edit.redo":
        handleRedoSessionModelEdit();
        break;
      case "view.issues":
        setIssuesDrawerOpen((open) => !open);
        break;
      case "view.audit":
        setAuditDrawerOpen((open) => !open);
        break;
      case "view.close-panels":
        closeShellPage();
        break;
      case "view.tree":
        // The table pane collapses only where it is a drawer (Model view; Both view below 1280 px).
        if (shellNowRef.current.view === "model" || (shellNowRef.current.view === "both" && window.innerWidth < 1280)) toggleWorkspaceRail("tree");
        break;
      case "view.inspector":
        // As the toolbar's Inspector toggle: it acts in Both view only.
        if (shellNowRef.current.view === "both") toggleWorkspaceRail("inspector");
        break;
      case "insert.load":
        handleArmCreationTool("load");
        break;
      case "insert.node":
        handleArmCreationTool("node");
        break;
      case "insert.pipe":
        handleArmCreationTool("pipe");
        break;
      case "insert.support":
        handleArmCreationTool("support");
        break;
      case "insert.component":
        handleArmCreationTool("component");
        break;
      case "analyze.run":
        setActiveSection("solve");
        void handleRun();
        break;
      case "analyze.cancel":
        void handleCancelRun();
        break;
      case "analyze.rule-checks":
        setActiveSection("solve");
        break;
      case "analyze.check-model":
        void handleRunModelChecks();
        break;
      default: {
        const prefix = "view.section.";
        if (command.startsWith(prefix)) {
          const sectionId = command.slice(prefix.length) as WorkspaceSectionId;
          // Choosing the open page again closes it onto the stage underneath;
          // choosing the current stage surface again returns to the model tree, as before.
          setActiveSection((current) => current !== sectionId
            ? sectionId
            : isStageSurface(sectionId) ? null : sectionAfterPageClose(shellNowRef.current.stageSurface));
        } else if (command.startsWith("view.view.")) {
          chooseStageView(command.slice("view.view.".length) as ShellView);
        } else if (command.startsWith("view.stage.")) {
          enterStage(command.slice("view.stage.".length) as ShellStage);
        } else if (command.startsWith("view.theme.")) {
          const theme = command.slice("view.theme.".length) as UiThemePreference;
          setUiPreferences((current) => updateUiPreferences(current, { theme }));
        } else if (command.startsWith("view.density.")) {
          const density = command.slice("view.density.".length) as UiDensityPreference;
          setUiPreferences((current) => updateUiPreferences(current, { density }));
        }
        break;
      }
    }
  }

  const nativeRunPresence = runPresenceFromCells({ result, historicalRun, solveJob, hasQualifiedCurrentResult: currentSolvedResult !== null, numericalHealthHold });
  const nativeResultsEnabled = railStageState("results", nativeRunPresence).enabled;
  const nativeReviewEnabled = railStageState("review", nativeRunPresence).enabled;
  const nativeProjectName = projectSummary?.project_name ?? model?.project.name ?? null;
  useEffect(() => {
    if (!isTauriRuntime()) return;
    void syncNativeShellState({
      projectName: nativeProjectName,
      modelEdited,
      projectBusy,
      stage: shellNow.stage,
      view: stageViewNow,
      theme: uiPreferences.theme,
      density: uiPreferences.density,
      resultsStageEnabled: nativeResultsEnabled,
      reviewStageEnabled: nativeReviewEnabled,
      inspectorOpen: stageViewNow === "model" || (stageViewNow === "both" && !inspectorCollapsed),
      canUndo: undoStack.length > 0 && !operationBusy,
      canRedo: redoStack.length > 0 && !operationBusy,
      canRun: !running,
      canCancel: running
    }).catch((error: unknown) => console.warn("Native shell state sync failed", error));
  }, [Boolean(model), nativeProjectName, modelEdited, projectBusy, shellNow.stage, stageViewNow, uiPreferences.theme, uiPreferences.density,
    nativeResultsEnabled, nativeReviewEnabled, inspectorCollapsed, undoStack.length, redoStack.length, operationBusy, running]);

  // Latest-closure ref so native menu events (registered once) always dispatch
  // against current state rather than the first render. The Rust menu handler
  // injects this DOM event directly into the main webview; this avoids relying
  // on a frontend Tauri event subscription that is not available in the
  // packaged capability set.
  const runMenuCommandRef = useRef(runMenuCommand);
  runMenuCommandRef.current = runMenuCommand;
  useEffect(() => {
    const handleNativeMenuCommand = (event: Event) => {
      if (
        !(event instanceof CustomEvent) ||
        typeof event.detail !== "string" ||
        !isMenuCommandId(event.detail)
      ) {
        return;
      }
      runMenuCommandRef.current(event.detail);
    };
    window.addEventListener("openpipestress-native-menu-command", handleNativeMenuCommand);
    return () => {
      window.removeEventListener("openpipestress-native-menu-command", handleNativeMenuCommand);
    };
  }, []);

  // W-17 (HF-08; Codex r1): a window close or quit. The native host holds
  // every one and asks here (`src-tauri/src/close_guard.rs`); it never decides
  // from the synced dirty flag. Each attempt is acknowledged first, and the
  // user is asked only once the host accepted it: an accepted attempt has no
  // deadline, and a refused or failed one means the host closes on its own
  // deadline, so nothing is shown on a closing window. Then, for a new request:
  // - a dialog or prompt holds the window: nothing closes (the modal rule);
  //   the status line says to finish or cancel it first;
  // - a project operation is running: the user chooses between waiting and
  //   quitting without saving (never silently);
  // - otherwise the unsaved-changes prompt asks while the model has edits, and
  //   the request goes ahead at once without them.
  // A repeat while a request is being decided asks nothing more while a prompt
  // is showing; while the save chosen for it is still running, it offers the
  // same explicit choice. In the browser preview, the page's unload prompt
  // guards a reload or tab close.
  const nativeCloseFlow = useRef<number | null>(null);
  async function handleNativeCloseRequest({ requestId, attempt, kind }: NativeCloseRequest) {
    let accepted = false;
    try {
      accepted = await acknowledgeNativeCloseRequest(requestId, attempt);
    } catch (error: unknown) {
      console.warn("Close request acknowledgement failed", error);
    }
    if (!accepted) return;
    const refused = kind === "quit" ? "Not quit" : "Window not closed";
    const verb = kind === "quit" ? "quit" : "close the window";
    const answer = (proceed: boolean) =>
      resolveNativeCloseRequest(requestId, proceed).catch((error: unknown) => console.warn("Close request answer failed", error));
    // Any dialog or prompt holding the window, read after the busy prompt has
    // released its own hold: a dialog that opened behind it (a replace prompt
    // after a refused save) must be decided first (Codex r2 P2).
    const dialogOpen = () => replacePromptOpenRef.current || projectUnitsDialogOpenRef.current || modelDocumentSaveDialogOpenRef.current || handoffSaveDialogOpenRef.current;
    const keptForDialog = () => {
      setProjectMessage(`${refused}: a dialog is open. Finish or cancel it first; nothing was closed.`);
      setProjectOperation(kind === "quit" ? "quit_dialog_open" : "close_dialog_open");
    };
    if (nativeCloseFlow.current === requestId) {
      if (replacePromptOpenRef.current) return;
      const choice = await confirmQuitWhileBusy({ verb, running: "The save you chose before you asked to " + verb });
      if (choice !== "quit" || nativeCloseFlow.current !== requestId) return;
      if (dialogOpen()) {
        keptForDialog();
        return;
      }
      nativeCloseFlow.current = null;
      await answer(true);
      return;
    }
    if (nativeCloseFlow.current !== null) {
      await answer(false);
      return;
    }
    nativeCloseFlow.current = requestId;
    let proceed = false;
    try {
      if (dialogOpen()) {
        keptForDialog();
      } else if (projectOperationOwner.current !== null) {
        proceed = (await confirmQuitWhileBusy({ verb, running: "An open, save or create of a local project" })) === "quit";
        if (proceed && dialogOpen()) {
          proceed = false;
          keptForDialog();
        } else if (!proceed) {
          setProjectMessage(`${refused}: the project operation is still running; nothing was closed.`);
          setProjectOperation(kind === "quit" ? "quit_kept_waiting" : "close_kept_waiting");
        }
      } else {
        const outcome = await confirmReplacingEdits(kind === "quit"
          ? { action: "Quitting SWBPIPE", verb: "quit", consequence: "Quitting SWBPIPE closes the working model." }
          : { action: "Closing the window", verb: "close it", consequence: "Closing the window quits SWBPIPE and closes the working model." });
        proceed = outcome === "proceed";
        if (outcome !== "proceed") {
          setProjectMessage(unsavedChangesRefusal(outcome, refused));
          setProjectOperation(kind === "quit" ? "quit_kept_edits" : "close_kept_edits");
        }
      }
    } finally {
      if (nativeCloseFlow.current === requestId) {
        nativeCloseFlow.current = null;
        dismissQuitWhileBusy();
        await answer(proceed);
      }
    }
  }
  const nativeCloseRequestRef = useRef(handleNativeCloseRequest);
  nativeCloseRequestRef.current = handleNativeCloseRequest;
  useEffect(() => {
    const onCloseRequest = (event: Event) => {
      const request = event instanceof CustomEvent ? nativeCloseRequestFrom(event.detail) : null;
      if (request) void nativeCloseRequestRef.current(request);
    };
    const onBeforeUnload = (event: BeforeUnloadEvent) => {
      if (isTauriRuntime() || !modelEditedRef.current) return;
      event.preventDefault();
      event.returnValue = "";
    };
    window.addEventListener(NATIVE_CLOSE_REQUEST_DOM_EVENT, onCloseRequest);
    window.addEventListener("beforeunload", onBeforeUnload);
    return () => {
      window.removeEventListener(NATIVE_CLOSE_REQUEST_DOM_EVENT, onCloseRequest);
      window.removeEventListener("beforeunload", onBeforeUnload);
    };
  }, []);

  // Bubble after local React handlers so drawers and the palette can consume
  // Escape, including when the unconsumed key originates outside the shell.
  useEffect(() => {
    function handleWorkspaceEscape(event: KeyboardEvent) {
      const shell = workspaceShellRef.current;
      if (!shell || event.key !== "Escape" || event.defaultPrevented) return;
      // Inspect the DOM home, including portalled routing controls, after child
      // controls have had their cancellation opportunity. Model stays docked.
      const target = event.target instanceof Node ? event.target : document.activeElement;
      const inspector = document.getElementById("shell-inspector");
      const surfaces = shell.querySelector(".shell-surfaces");
      if (shellNowRef.current.view === "both" && !shellNowRef.current.location.page &&
          target && inspector?.contains(target) && surfaces && !surfaces.classList.contains("inspector-collapsed")) {
        event.preventDefault();
        runMenuCommandRef.current("view.inspector");
        inspectorToggleRef.current?.focus();
        return;
      }
      viewportViewCommandRef.current?.({ type: "cancel-box-selection" });
      setOpenMenu(null);
      setArmedCreationTool(null);
      // ⎋ accelerates the open page's close control. It never leaves a stage.
      setActiveSection((current) => isStageSurface(current) ? current : sectionAfterPageClose(shellNowRef.current.stageSurface));
      setAuditDrawerOpen(false);
      setIssuesDrawerOpen(false);
      shell.querySelector<HTMLButtonElement>('[data-testid="workspace-select"]')?.focus();
    }
    window.addEventListener("keydown", handleWorkspaceEscape);
    return () => window.removeEventListener("keydown", handleWorkspaceEscape);
  }, []);

  // The shell's two splitters: the Both view's split (the table pane's share of
  // the surface) and the Model view's table drawer. Both are presentation
  // preferences; neither touches the model.
  function handleWorkspaceSplitterKeyDown(
    event: React.KeyboardEvent<HTMLButtonElement>,
    target: "both" | "drawer"
  ) {
    if (target === "both") {
      if (event.key !== "ArrowLeft" && event.key !== "ArrowRight") return;
      event.preventDefault();
      const delta = event.key === "ArrowLeft" ? -2 : 2;
      setUiPreferences((current) => updateUiPreferences(current, { bothSplitPct: current.bothSplitPct + delta }));
      return;
    }
    if (event.key !== "ArrowUp" && event.key !== "ArrowDown") return;
    event.preventDefault();
    const delta = event.key === "ArrowUp" ? 16 : -16;
    setUiPreferences((current) => updateUiPreferences(current, { tableDrawerPx: current.tableDrawerPx + delta }));
  }

  function beginWorkspaceResize(
    event: React.PointerEvent<HTMLButtonElement>,
    target: "both" | "drawer"
  ) {
    event.preventDefault();
    activeResizeCleanupRef.current?.();
    const startX = event.clientX;
    const startY = event.clientY;
    const initial = uiPreferences;
    const surfaceWidth = workspaceBudgetRef.current?.getBoundingClientRect().width ?? 0;
    const move = (pointer: PointerEvent) => {
      const patch = target === "both"
        ? (surfaceWidth > 0 ? { bothSplitPct: initial.bothSplitPct + ((pointer.clientX - startX) / surfaceWidth) * 100 } : {})
        : { tableDrawerPx: initial.tableDrawerPx + startY - pointer.clientY };
      setUiPreferences((current) => updateUiPreferences(current, patch));
    };
    const finish = () => {
      window.removeEventListener("pointermove", move);
      window.removeEventListener("pointerup", finish);
      window.removeEventListener("pointercancel", finish);
      if (activeResizeCleanupRef.current === finish) activeResizeCleanupRef.current = null;
    };
    activeResizeCleanupRef.current = finish;
    window.addEventListener("pointermove", move);
    window.addEventListener("pointerup", finish);
    window.addEventListener("pointercancel", finish);
  }

  function handleNarrowDrawerKeyDown(
    event: React.KeyboardEvent<HTMLDivElement>,
    side: "tree" | "inspector"
  ) {
    if (event.defaultPrevented) return;
    if (side === "inspector" && event.key === "Escape" && shellNowRef.current.view !== "both") return;
    if (window.innerWidth >= 1280 || (side === "tree" ? treeCollapsed : inspectorCollapsed)) return;
    const pane = event.currentTarget;
    if (event.key === "Escape") {
      event.preventDefault();
      if (side === "inspector") routingInspectorRestore.current = null;
      closeWorkspaceRail(side, true);
      return;
    }
    if (event.key !== "Tab") return;
    const focusable = [...pane.querySelectorAll<HTMLElement>(
      'button:not(:disabled), input:not(:disabled), select:not(:disabled), textarea:not(:disabled), [href], [tabindex]:not([tabindex="-1"])'
    )].filter((element) => !element.hidden && !element.closest("[hidden]"));
    if (focusable.length === 0) return;
    const first = focusable[0];
    const last = focusable[focusable.length - 1];
    if (event.shiftKey && document.activeElement === first) {
      event.preventDefault();
      last.focus();
    } else if (!event.shiftKey && document.activeElement === last) {
      event.preventDefault();
      first.focus();
    }
  }

  function closeWorkspaceRail(side: "tree" | "inspector", restoreFocus = false) {
    const toggle = side === "tree" ? treeToggleRef.current : inspectorToggleRef.current;
    const focused = document.activeElement;
    const pane = side === "tree" ? toggle?.closest(".workspace-pane") : document.getElementById("shell-inspector");
    // Move focus to the persistent opener only when the closing drawer owns
    // focus. A viewport command that closes an overlapping drawer keeps focus
    // on its already-visible initiating control.
    if (restoreFocus || (focused instanceof HTMLElement && pane?.contains(focused))) toggle?.focus();
    if (side === "tree") setTreeCollapsed(true);
    else setInspectorCollapsed(true);
  }

  function exposeViewportForNarrowInteraction(
    _interaction: ViewportExposureInteraction | `authoring-${CreationTool}`
  ) {
    if (window.innerWidth >= 1280) return;
    // Below 1280 px the table drawer is in flow and the inspector slides over
    // the canvas. Mounted children and drafts remain alive as exposure changes.
    // A page over the stage closes onto it; the stage itself is never left.
    closeWorkspaceRail("tree");
    closeWorkspaceRail("inspector");
    closeShellPage();
  }

  function openWorkspaceRail(side: "tree" | "inspector") {
    // Explicit navigation into a property editor supersedes routing's temporary
    // borrowing; its destination must stay open and retain the requested focus.
    if (side === "inspector" && routingPanelActive) routingInspectorRestore.current = null;
    const openingToggle = side === "tree" ? treeToggleRef.current : inspectorToggleRef.current;
    const invokedFromToggle = document.activeElement === openingToggle;
    if (window.innerWidth < 1280) {
      if (side === "tree" && !inspectorCollapsed) closeWorkspaceRail("inspector");
      if (side === "inspector" && !treeCollapsed) closeWorkspaceRail("tree");
      // A page would cover the pane being opened; close it onto its stage,
      // retaining its mounted draft state.
      closeShellPage();
    }
    if (side === "tree") setTreeCollapsed(false);
    else setInspectorCollapsed(false);
    if (invokedFromToggle) openingToggle?.focus();
  }

  function toggleWorkspaceRail(side: "tree" | "inspector") {
    if (side === "inspector" && routingPanelActive) routingInspectorRestore.current = null;
    const collapsed = side === "tree" ? treeCollapsed : inspectorCollapsed;
    if (collapsed) openWorkspaceRail(side);
    else closeWorkspaceRail(side);
  }

  // --- The shell's presentation handlers (slice B3). Each one writes chrome
  // cells only; `setActiveSection` stays the one navigation primitive.

  /** The toolbar's view switch, the View menu and ⌘1 ⌘2 ⌘3: the current stage's view. */
  function chooseStageView(view: ShellView) {
    const stage = shellNowRef.current.location.stage;
    setStageViewMemory((memory) => rememberStageView(memory, stage, view));
  }

  /** The rail and the View menu: enter a stage, unless the rail disables it. */
  function enterStage(stage: ShellStage) {
    if (!railStageState(stage, runPresenceFromCells({ result, historicalRun, solveJob, hasQualifiedCurrentResult: currentSolvedResult !== null, numericalHealthHold })).enabled) return;
    setActiveSection(sectionForStage(stage, shellNowRef.current.stageSurface));
  }

  function rememberShellFocus(event: React.SyntheticEvent<HTMLElement>) {
    if (shellNowRef.current.location.page || !(event.target instanceof Element)) return;
    const target = event.target.closest<HTMLElement>("button, a[href], input, select, textarea, [tabindex], [contenteditable]");
    if (target) pageReturnFocusRef.current = target;
  }

  /** A page's close control (⎋ accelerates it): back to the stage surface it was opened over. */
  function closeShellPage() {
    setActiveSection((current) => isStageSurface(current) ? current : sectionAfterPageClose(shellNowRef.current.stageSurface));
  }

  /**
   * A command that needs the canvas or the inspector is about to return to the
   * Model stage: if that stage was left in Table view, show it in Both view.
   */
  function revealModelStageCanvas() {
    setStageViewMemory((memory) => viewForStage(memory, "model") === "table" ? rememberStageView(memory, "model", "both") : memory);
  }

  // ⌘1 ⌘2 ⌘3 accelerate the view switch, ⌘I the Inspector toggle, and
  // ⌘Z / ⇧⌘Z the same model history handlers as the toolbar and menu.
  // Each key does what its visible control does, and nothing when that control is disabled.
  const shellKeyHandlers = {
    chooseStageView, toggleWorkspaceRail,
    canUndo: undoStack.length > 0 && !operationBusy,
    canRedo: redoStack.length > 0 && !operationBusy
  };
  const shellKeyHandlersRef = useRef(shellKeyHandlers);
  shellKeyHandlersRef.current = shellKeyHandlers;
  useEffect(() => {
    function handleShellAccelerator(event: KeyboardEvent) {
      if (replacePromptOpenRef.current || projectUnitsDialogOpenRef.current || modelDocumentSaveDialogOpenRef.current || handoffSaveDialogOpenRef.current) return;
      if ((!event.metaKey && !event.ctrlKey) || event.altKey || event.defaultPrevented) return;
      const key = event.key.toLowerCase();
      // ⇧⌘M runs the model checks (Analyze → Check Model). AppKit owns it in the
      // native runtime, where the menu item carries the same accelerator.
      if (key === "m" && event.shiftKey && !isTauriRuntime()) {
        event.preventDefault();
        runMenuCommandRef.current("analyze.check-model");
        return;
      }
      // ⌘S is File › Save Local Project. AppKit owns it in the native runtime,
      // where the menu item carries the same accelerator; either way it waits
      // while a modal holds the window (above, and runMenuCommand).
      if (key === "s" && !event.shiftKey) {
        if (isTauriRuntime()) return;
        event.preventDefault();
        runMenuCommandRef.current("file.save-local");
        return;
      }
      if (key === "z") {
        const target = event.target instanceof HTMLElement ? event.target : document.activeElement;
        if (target instanceof HTMLElement && (target.isContentEditable || target.closest('input, textarea, [contenteditable="true"], [contenteditable=""]'))) return;
        const handlers = shellKeyHandlersRef.current;
        if (event.shiftKey ? handlers.canRedo : handlers.canUndo) {
          event.preventDefault();
          runMenuCommandRef.current(event.shiftKey ? "edit.redo" : "edit.undo");
        }
        return;
      }
      // AppKit owns the remaining shell keys. History stays in the webview in
      // both runtimes so editable controls retain their normal text undo.
      if (isTauriRuntime() || event.shiftKey) return;
      const now = shellNowRef.current;
      if (key === "1" || key === "2" || key === "3") {
        const view = SHELL_VIEWS[Number(key) - 1];
        event.preventDefault();
        if (SHELL_STAGES.includes(now.location.stage) && (now.location.stage !== "review" || view === "table")) {
          shellKeyHandlersRef.current.chooseStageView(view);
        }
      } else if (key === "i") {
        event.preventDefault();
        if (now.view === "both") shellKeyHandlersRef.current.toggleWorkspaceRail("inspector");
      }
    }
    window.addEventListener("keydown", handleShellAccelerator);
    return () => window.removeEventListener("keydown", handleShellAccelerator);
  }, []);

  /** W-12 S1 Open State: the saved state's snapshot becomes the working model of
   * the same stored project, as an open does. It starts a new project session:
   * the undo and redo history is cleared, so undo never walks back into the
   * model the session held before; results, queued operations and the review
   * context go with it. The stored base is unchanged (the session is still that
   * stored project), and the saved basis is the state's model hash, so the
   * first edit makes a new, edited working model. */
  function adoptStateSnapshot(opened: ModelStateRead, snapshotHash: ModelHashEvidence, binding: ProjectBinding): Promise<string> {
    ruleRevisionGate.current.invalidate();
    setModelHashIntegrity(null);
    setProjectEnvelopeHashIntegrity(null);
    advanceProjectSession();
    commitModel(opened.model);
    savedBasisSequence.current += 1;
    setSavedModelBasis({ generation: projectSessionGenerationRef.current, revision: uiModelRevisionRef.current, hash: snapshotHash.value, source: "open" });
    setSelection(defaultSelection(opened.model));
    setUndoStack([]);
    sessionEvents.emit({ type: "history-reset", projectId: opened.model.project.id });
    setRedoStack([]);
    setAppliedOperations([]);
    withdrawBatchRegistrations();
    setQueuedBatches([]);
    setBatchOutcomes({});
    setBatchReceipts([]);
    setBatchMessage(null);
    setOperationOutcomes({});
    setOperationMessage(null);
    setHistoricalRun(null);
    setResult(null);
    setAnalysisRun(null);
    setInputManifest(null);
    setRuleCheckAggregate(null);
    setProposal(null);
    setRetainedReviewContext([]);
    setEditorIntents([]);
    setSelectedReviewTarget(null);
    setSolveJob(initialSolveJob());
    setModelDocumentVersion(opened.model_document_version ?? null);
    // The session is the state's project. Its stored base is one this session
    // saw for that project, never one read afresh from the store (that would
    // hide another window's save from the stale-window check):
    // - the base the session holds now, when it is that project's (no save, or
    //   the guard's Save first saved it in place);
    // - otherwise the base captured before the guard, when that was the
    //   project's (the guard's Save first went to "Save as a new project");
    // - otherwise none: the session never saw a stored revision of it, so a
    //   save of it asks, as an opened model document's does.
    const stateProject = opened.model.project.id;
    if (storedBaseRef.current?.projectId !== stateProject) {
      const bound = binding.base?.projectId === stateProject;
      storedBaseRef.current = bound ? binding.base : null;
      setProjectSummary(bound ? binding.summary : null);
      setProjectEnvelopeHash(bound ? binding.envelopeHash : null);
    }
    return libraryReferenceWarnings(opened.model);
  }

  function captureProjectBinding(): ProjectBinding {
    return { base: storedBaseRef.current, summary: projectSummary, envelopeHash: projectEnvelopeHash };
  }

  /** Save Local Project's flow, reporting whether a save landed (the
   * unsaved-changes guard's "Save first"). */
  /** Another project operation, or any project prompt, owns the session. The
   * model-replacing commands, Open State and Save Model State start nothing then. */
  function projectSessionBusy(): boolean {
    return projectOperationOwner.current !== null || replacePromptOpenRef.current || projectUnitsDialogOpenRef.current
      || modelDocumentSaveDialogOpenRef.current || handoffSaveDialogOpenRef.current;
  }

  async function saveLocalProjectFirst(): Promise<LandedProjectSave | null> {
    projectSaveLanded.current = null;
    await saveProject(null);
    return projectSaveLanded.current;
  }

  const { unsavedChangesPrompt, replacingNeedsConfirmation, confirmReplacingEdits, quitWhileBusyPrompt, confirmQuitWhileBusy, dismissQuitWhileBusy } = useUnsavedChangesGuard({
    modelEditedRef, holdModal, projectSessionBusy, saveLocalProject: async () => (await saveLocalProjectFirst()) !== null
  });

  // D5 slice 2: the autosave timer, its settings and status line, and the
  // recovery offer, whose Open runs the guard and adopts the record as Open
  // Model Document adopts a file.
  const autosave = useAutosave({
    native: isTauriRuntime(),
    modelEditedRef,
    saveBasisRef: modelDocumentSaveBasisRef,
    projectSessionBusy,
    holdModal,
    workingModel: () => currentModel.current ? { name: currentModel.current.project.name, edited: modelEditedRef.current } : null,
    openAutosave: (fileName, writtenAt) => handleOpenModelDocument(openAutosaveSource(fileName, writtenAt))
  });

  const history = useModelStateHistory({
    model, currentModel, projectSessionGeneration, projectSessionGenerationRef, storedBaseRef,
    confirmReplacingEdits, acquireProjectOperation, releaseProjectOperation,
    saveLocalProject: saveLocalProjectFirst, captureProjectBinding, adoptStateSnapshot, projectSessionBusy,
    requestStoredDocumentExport,
    runSlot: { result, analysisRun, inputManifest, restored: historicalRun?.designation === "historical_saved_run" }
  });

  // Pure registration over the actual owner; no native owner/timer/process is
  // created until a later explicit panel action requests start/configuration.
  const agentOwnerRef = useRef<import("../../services/embeddedAgentSession").WorkspaceExecution | null>(null);
  agentOwnerRef.current = {
    // The hash is published only for the model revision it was computed for, read live from
    // the owner so a closure from an earlier render cannot pair an older hash with a newer
    // model. (Comparing uiModelRevision with modelRevision.current mixed two counters that
    // advance on different events; the [model] layout effect also advances the second, so
    // they differ from the first load on and the agent could never start.)
    snapshot: () => ({ model: currentModel.current, hash: currentHashOwned && modelHashOwner.current?.modelRevision === modelRevision.current && projectSessionGeneration === projectSessionGenerationRef.current ? modelHash : null,
      revision: modelRevision.current, generation: projectSessionGenerationRef.current,
      result: currentSolvedResultRef.current, standing: { eligible: numericallyEligible, health: numericalHealth } }),
    register: (batch, context) => registerOperationBatch(batch, { agentContext: context }),
    proposal: (key) => agentProposalStandingRef.current.get(key) ?? null,
    solve: () => handleRunWithAgentReceipt(),
    withdraw: key => {
      const standing=agentProposalStandingRef.current.get(key);
      const registration=batchRegistrations.current.get(key);
      if(!registration || standing?.status!=="pending_review" || agentApplyingRef.current.has(key))return;
      batchRegistrations.current.delete(key);
      setQueuedBatches(current=>current.filter(entry=>entry.key!==key));
      sessionEvents.emit({type:"withdrawn",batchId:registration.entry.batch.batch_id,key});
    }
  };
  const agentSessionRef = useRef<EmbeddedAgentSession | null>(null);
  if (!agentSessionRef.current) agentSessionRef.current = new EmbeddedAgentSession({
    snapshot: () => agentOwnerRef.current!.snapshot(), register: (batch, context) => agentOwnerRef.current!.register(batch, context),
    proposal: (key) => agentOwnerRef.current!.proposal(key), solve: () => agentOwnerRef.current!.solve(), withdraw: key => agentOwnerRef.current!.withdraw(key)
  });
  useEffect(() => () => { void agentSessionRef.current?.close(); }, []);

  return {
    agent: agentSessionRef.current,
    model: {
      model,
      knowledge,
      modelHash,
      modelAssignment,
      activeModelIndex,
      projectSessionGeneration,
      uiModelRevision,
      modelRevision
    },
    selection: {
      selection,
      orderedSelection,
      orderedSelectionRef,
      hiddenEntityKeys, setHiddenEntityKeys,
      isolationSelectionKeys, setIsolationSelectionKeys,
      effectiveHiddenKeys: viewportVisibility.hiddenKeys,
      dimmedKeys: viewportVisibility.dimmedKeys,
      hiddenCount: viewportVisibility.hiddenCount,
      isolationActive: viewportVisibility.isolationActive,
      handleClearVisibility,
      selectedPipeRefs,
      treePublication,
      handleTreePublication,
      commitSelectionState,
      handleSelectEntity,
      handleBoxSelection
    },
    results: {
      result,
      currentSolvedResult,
      numericallyEligible,
      numericalHealth,
      numericalHealthHold,
      historicalRun,
      analysisRun,
      inputManifest,
      ruleCheckAggregate,
      ruleCheckReportRun,
      ruleCheckRunBasis,
      dormantOutputBasis,
      comparison,
      comparisonUnavailable,
      packagedWithinRun,
      withinRun,
      droppedWithinRunBases,
      withinRunDisabledReason,
      handleSelectWithinRunBases,
      proposal,
      selectedReviewTarget,
      solveJob,
      solveProof,
      running,
      solverMode, setSolverMode,
      reportPackagePrivateIntent, setReportPackagePrivateIntent,
      reportPackageBusy,
      reportPackageRedaction,
      reportPackageRoute,
      handleRun,
      handleInspectBundledReference,
      handleCancelRun,
      handleRuleCheckAggregate,
      handleProposal,
      handleSelectResult,
      handleSelectDiagnostic,
      handleSaveReportPackage
    },
    operations: {
      editorIntents,
      retainedReviewContext,
      operationOutcomes,
      appliedOperations,
      undoStack,
      redoStack,
      queuedBatches,
      batchOutcomes,
      batchReceipts,
      batchMessage,
      requestEpoch,
      getPreparationEpoch,
      directDraftCommitToken,
      operationBusy,
      operationMessage,
      historyFailure,
      operationEngineStatus,
      operationRequest,
      handleQueueEditorIntent,
      handleClearReviewQueue,
      handleQueueOperationBatch,
      handleRequeueRetainedRecord,
      registerOperationBatch,
      handleRunOperationBatch,
      handleDismissRetiredBatch,
      sessionEvents,
      handleAddDraftReview,
      handleApplyDraftReview,
      handleValidateIntent,
      handleApplyIntent,
      handleUndoSessionModelEdit,
      handleRedoSessionModelEdit,
      invalidateDirectDraftContext
    },
    project: {
      modelEdited,
      storageCapability,
      projectSummary,
      projectIndex,
      modelHashIntegrity,
      projectEnvelopeHash,
      projectEnvelopeHashIntegrity,
      modelDocumentVersion,
      projectMessage,
      projectOperation,
      projectBusy,
      handleCreateProject,
      handleCreateBlankProject,
      handleCreateBlankLoadStateProject,
      requestBlankProject,
      blankProjectUnitsRequest,
      handleOpenProject,
      handleOpenModelDocument,
      handleSaveProject,
      handleListProjects,
      replaceProjectPrompt,
      unsavedChangesPrompt,
      // D5 slice 2: autosave settings, status line and recovery offer.
      autosave,
      quitWhileBusyPrompt,
      // W-12 S1: the saved model states of the session's project (History panel).
      history,
      requestSaveModelDocument,
      modelDocumentSaveRequest,
      requestSaveHandoff,
      handoffSaveRequest
    },
    chrome: {
      uiPreferences, setUiPreferences,
      resolvedTheme,
      activeSection, setActiveSection,
      activatedExpensiveSections,
      propertyTaskRequest,
      openMenu, setOpenMenu,
      armedCreationTool,
      viewportViewCommandRef,
      workspaceShellRef,
      workspaceBudgetRef,
      treeCollapsed,
      inspectorCollapsed,
      treeToggleRef,
      inspectorToggleRef,
      operationTab, setOperationTab,
      reviewDetailsOpen, setReviewDetailsOpen,
      auditDrawerOpen, setAuditDrawerOpen,
      issuesDrawerOpen, setIssuesDrawerOpen,
      modelCheckRun,
      modelCheckBusy,
      handleRunModelChecks,
      stageSurface,
      stageViewMemory, setStageViewMemory,
      narrowWindow,
      chooseStageView,
      enterStage,
      closeShellPage,
      rememberShellFocus,
      recordR3JourneyEvent,
      handleArmCreationTool,
      handleToolkitCommand,
      runMenuCommand,
      handleWorkspaceSplitterKeyDown,
      beginWorkspaceResize,
      handleNarrowDrawerKeyDown,
      exposeViewportForNarrowInteraction,
      toggleWorkspaceRail
    }
  };
}

/** What the view receives: the six slices `useWorkspaceSession` returns. */
export type WorkspaceSession = ReturnType<typeof useWorkspaceSession>;

/** Freeze a queued submission recursively (W-10): no caller can alter it after registration. */
function deepFreeze<T>(value: T): T {
  if (value && typeof value === "object" && !Object.isFrozen(value)) {
    Object.freeze(value);
    for (const child of Object.values(value as Record<string, unknown>)) deepFreeze(child);
  }
  return value;
}

/** W-10: one queued submission as the live registry holds it. */
/** The retired notice of a queued batch whose basis is no longer current (§3.6 step 1). */
export const RETIRED_BATCH_NOTICE = "Prepared on an earlier model and withdrawn. Prepare it again.";

type BatchRegistration = {
  entry: QueuedBatch;
  epoch: number;
  validated?: { fingerprint: string; outcome: OperationBatchOutcome };
};
