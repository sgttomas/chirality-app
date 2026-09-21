'use client';

import { isSessionBootConfirmed } from '../../lib/harness/session-boot-readiness';
import { deriveTranscriptView, type TranscriptItem } from '@chirality/runtime-contracts/transcript-replay';
import { mergeSteeringReceipt, persistSteeringReceipt, recoverSteeringReceipts, type SteeringReceipt } from '../../lib/shell/steering-receipts';
import { nativePlanText } from '../../lib/harness/native-plan-text';

import { usePathname, useSearchParams } from 'next/navigation';
import React, { FormEvent, useEffect, useMemo, useRef, useState, useCallback } from 'react';
import {
  HarnessApiClientError,
  attachHarnessTurn,
  bootHarnessSession,
  getHarnessSession,
  getHarnessTurnState,
  createHarnessSession,
  interruptHarnessSession,
  steerHarnessSession,
  checkHarnessSteeringReceipt,
  replaySessionEvents,
  streamHarnessTurn,
  type HarnessModelSelection,
  type HarnessTurnStreamEvent
} from '../../lib/harness/client';
import { isSelectionInCatalog, modelSelectorUnavailableTitle, selectAccountModelCatalog, selectHostedModelCatalog, useHostedBootstrap } from '../../lib/harness/hosted-bootstrap-context';
import { toHarnessUiError, type HarnessUiError } from '../../lib/harness/error-display';
import {
  buildChatDraftStorageKey,
  persistChatDraftSnapshotToStorage,
  readChatDraftSnapshotFromStorage
} from '../../lib/harness/chat-draft';
import { buildUiAttachment, type UiAttachment } from '../../lib/harness/ui-attachments';
import { getNativeAttachmentBridge } from '../../lib/shell/native-attachments';
import type { HarnessEvent } from '@chirality/runtime-contracts/event-schema';
import { CHAT_SECTION } from '../../lib/shell/loop-first';
import { resolvePersona } from '../../lib/shell/persona-resolution';
import { useHarnessEventActions, useHarnessEvents } from '../workspace/harness-events-provider';
import { deriveTurnActivityFromEvents, deriveTurnActivityFromTranscript, type TurnActivity } from '../../lib/shell/turn-activity';
import { selectPendingPermissionRequests, selectPendingServerRequests } from '../../lib/shell/harness-event-views';
import { interruptedTurnPresentation, turnOutcomeDescription, turnOutcomeLabel, turnPhaseStatusLine, type TurnOutcome, type TurnPhase } from '../../lib/shell/turn-phase';
import {
  beginPlanExecution, detectPlanExecution, planExecutionMarker, readPlanExecutionRecords, runningPlanExecution,
  settlePlanExecution, writePlanExecutionRecords, type PlanExecutionRecord
} from '../../lib/harness/plan-executions';
import { NativePlanPanel, type NativePlanPanelModel } from './native-plan-panel';
import { TurnActivityDisclosure } from './turn-activity';
import { useToolkit } from '../workspace/toolkit-provider';
import { useWorkspace } from '../workspace/workspace-provider';
import { FolderSelect, getNativeFolderBridge } from './folder-select';
import { PersonaPicker } from './persona-picker';
import { ChatMarkdown } from './chat-markdown';
import { workflowFeedbackPrompt, type WorkflowFeedbackRequest } from '../../lib/harness/workflow-feedback';
import { ConversationMessage } from './conversation-message';
import { FilePicker } from './file-picker';
import { PermissionRequests } from './permission-requests';
import { LiveSessionRequests } from './request-card';
import { useRuntimeEpoch } from './runtime-connectivity-provider';
import {
  getNativePlanCapability,
  exportNativePlanRevision,
  listNativePlanClarifications,
  listNativePlanRevisions,
  replyNativePlanClarification,
  replaceSelectedMethods,
  resolveSelectedContext,
  type InteractionMode,
  type QualifiedMethodReference,
  type ChiralityRoleName,
  MethodSelectionClientError
} from '../../lib/harness/method-selection-client';
import type { FrozenInstructionBasisV3, InstructionHistoryRecordV3, NativePlanCapabilityResponse, NativePlanClarification, NativePlanRevision } from '@chirality/runtime-contracts/v3';
import type { SelectedSessionReplayProjection } from '../../lib/woven-dialogue/contracts';
import type { RuntimeSessionRecordV3 } from '@chirality/runtime-contracts';

type ChatMessage = {
  id: string;
  role: 'operator' | 'assistant';
  interrupted?: boolean;
  /** How the Runtime-owned turn behind this reply ended, once known. */
  outcome?: TurnOutcome;
  outcomeDescription?: string;
  persona?: string;
  projectRoot?: string;
  text: string;
  attachments?: UiAttachment[];
  methods?: QualifiedMethodReference[];
  instructionBasis?: FrozenInstructionBasisV3;
  instructionHistory?: readonly InstructionHistoryRecordV3[];
  /** Runtime turn identity once known; scopes the live activity shown under the reply. */
  turnId?: string;
  /** Activity recorded for a resumed turn (from the transcript projection). */
  recordedActivity?: TurnActivity;
  nativeItems?: TranscriptItem[];
  phase?: TranscriptItem['phase'];
  receipt?: string;
};

type ActiveSession = {
  sessionId: string;
  projectRoot: string;
  selectedRootAtBinding: string;
  persona: string;
  mode: string;
  selectedMethods: readonly QualifiedMethodReference[];
  methodSelectionRevision: number;
  instructionBasisId: string;
  /** Last recorded `engineSelection.model` / `reasoningEffort`; the default for the next turn. */
  model?: string;
  reasoningEffort?: string;
  bootstrapPending?: boolean;
};

export type ResumeConversationRequest = {
  requestId: number;
  projection: SelectedSessionReplayProjection;
};

// The App permission mode is the user's Codex policy selection (TYPES §12
// `PolicySelection`): each mode is a fixed approval policy plus sandbox pair
// that the Runtime applies at thread start and re-sends when it changes. Sent
// per turn; it grants nothing beyond what Codex itself enforces.
type OperatorModeOption = {
  value: 'readOnly' | 'ask' | 'workspaceWrite' | 'bypass';
  label: string;
  /** Codex terms: approval policy and sandbox mode. */
  description: string;
};

export const OPERATOR_MODES: readonly OperatorModeOption[] = [
  { value: 'readOnly', label: 'Read only', description: 'Codex sandbox read-only, approval on request: the agent can read the project but every write or command outside the sandbox asks first.' },
  { value: 'ask', label: 'Ask before changes', description: 'Codex sandbox workspace-write, approval on request: the agent asks before commands or edits that leave the sandbox.' },
  { value: 'workspaceWrite', label: 'Write in workspace', description: 'Codex sandbox workspace-write, approval never: the agent edits inside the project folder without asking; anything outside it is refused.' },
  { value: 'bypass', label: 'Full access', description: 'Codex sandbox danger-full-access, approval never: no sandbox and no approval prompts. Use only when you accept every action the agent takes.' }
];

const DEFAULT_OPERATOR_MODE = 'workspaceWrite';
const MODEL_SELECTOR_HELP = 'Codex model for the next turn, from your authenticated account catalog. Changeable between turns.';
const REASONING_SELECTOR_HELP = 'Reasoning effort supported by the selected model, sent with the next turn. Separate from Plan Mode and from permissions.';
const PERMISSION_SELECTOR_HELP = 'Codex approval policy and sandbox for this chat. Applied at the next turn.';
const TERMINAL_HARNESS_EVENTS = new Set(['turn.completed', 'turn.failed', 'turn.interrupted', 'turn.cancelled']);
const RECONNECT_DELAYS_MS = [1_000, 2_000, 4_000, 8_000, 15_000, 30_000] as const;
/** Follow re-arms only within this band above the bottom, so reading history is never yanked back down. */
const FOLLOW_REARM_THRESHOLD_PX = 40;
// Stable defaults: the Plan panel model is memoised over these props, and a
// fresh array per render would re-publish the model to its host on every render.
const NO_KNOWN_ROOTS: readonly { path: string; lastUsedAt: string }[] = [];
const NO_FILE_CATALOG: readonly string[] = [];
const NO_SELECTED_METHODS: QualifiedMethodReference[] = [];
const IGNORE_SELECTED_METHODS = (): void => {};

function isSupportedOperatorMode(mode: string): mode is OperatorModeOption['value'] {
  return OPERATOR_MODES.some(option => option.value === mode);
}

function wait(ms: number, signal: AbortSignal): Promise<void> {
  return new Promise(resolve => {
    if (signal.aborted) { resolve(); return; }
    const timer = setTimeout(() => { signal.removeEventListener('abort', done); resolve(); }, ms);
    const done = (): void => { clearTimeout(timer); resolve(); };
    signal.addEventListener('abort', done, { once: true });
  });
}

function isTurnNotActive(error: unknown): boolean {
  if (!(error instanceof HarnessApiClientError)) return false;
  const reason = error.details && typeof error.details === 'object' ? (error.details as Record<string, unknown>).reason : undefined;
  return error.status === 404 || reason === 'TURN_NOT_ACTIVE';
}

/**
 * The recorded pair from a Runtime session record: `engineSelection.model` and
 * the additive `reasoningEffort`. Read from the booted record first, then the
 * created one; absent fields stay absent (never inferred).
 */
function recordedModelSelection(...records: ReadonlyArray<Partial<RuntimeSessionRecordV3> | null | undefined>): Pick<ActiveSession, 'model' | 'reasoningEffort'> {
  const selection: Pick<ActiveSession, 'model' | 'reasoningEffort'> = {};
  for (const record of records) {
    const model = record?.engineSelection?.model;
    if (selection.model === undefined && typeof model === 'string' && model.trim()) selection.model = model;
    const effort = record?.reasoningEffort;
    if (selection.reasoningEffort === undefined && typeof effort === 'string' && effort.trim()) selection.reasoningEffort = effort;
  }
  return selection;
}

function readTextField(data: unknown): string | undefined {
  if (!data || typeof data !== 'object') {
    return undefined;
  }

  const text = (data as Record<string, unknown>).text;
  return typeof text === 'string' ? text : undefined;
}

function resolveMode(pathname: string): string {
  if (pathname.startsWith('/workbench')) {
    return 'WORKBENCH';
  }

  if (pathname.startsWith('/pipeline')) {
    return 'PIPELINE';
  }

  if (pathname.startsWith('/chat')) {
    return CHAT_SECTION;
  }

  return 'PORTAL';
}

function mergeAttachments(existing: UiAttachment[], incoming: UiAttachment[]): UiAttachment[] {
  const deduped = new Map<string, UiAttachment>();
  for (const item of existing) {
    deduped.set(item.path, item);
  }
  for (const item of incoming) {
    deduped.set(item.path, item);
  }
  return [...deduped.values()];
}

function sameMethodSelection(
  left: readonly QualifiedMethodReference[],
  right: readonly QualifiedMethodReference[]
): boolean {
  return left.length === right.length && left.every((item, index) => {
    const other = right[index];
    return other !== undefined && item.kind === other.kind && item.name === other.name &&
      item.source === other.source && item.sourceRootId === other.sourceRootId;
  });
}

function AttachmentChips({ items }: { items: UiAttachment[] }): JSX.Element | null {
  if (items.length === 0) {
    return null;
  }

  return (
    <ul className="attachment-chip-list">
      {items.map((item) => (
        <li key={item.path} className="attachment-chip" title={item.path}>
          <span>{item.displayName}</span>
          <small>{item.clientType}</small>
        </li>
      ))}
    </ul>
  );
}


function nativePlanAvailable(capability: NativePlanCapabilityResponse): boolean {
  return capability.status === 'qualified' || capability.status === 'trial';
}

function instructionActivityLabel(record: InstructionHistoryRecordV3): string {
  switch (record.type) {
    case 'selection.changed': return 'Role or method selection updated';
    case 'resource.loaded': return 'Method resource loaded';
    case 'instruction-basis.resolved': return 'Instruction basis recorded';
    case 'native-plan.revised': return 'Native plan revised';
    case 'provider-span.continued': return 'Conversation continued with a new provider span';
    default: return 'Instruction context updated';
  }
}

function recordedRoleForTurn(
  turnId: string | undefined,
  history: readonly InstructionHistoryRecordV3[],
  bases: readonly FrozenInstructionBasisV3[]
): ChiralityRoleName | undefined {
  if (!turnId) return undefined;
  const basisRecord = history.find(record => {
    if (record.type !== 'instruction-basis.resolved') return false;
    const accepted = record.acceptedTurn;
    return record.turnId === turnId || (accepted !== null && typeof accepted === 'object' && 'turnId' in accepted && accepted.turnId === turnId);
  });
  const basisId = basisRecord && typeof basisRecord.basisId === 'string' ? basisRecord.basisId : undefined;
  return basisId ? bases.find(basis => basis.basisId === basisId)?.roleId : undefined;
}

function isHarnessEvent(value: unknown): value is HarnessEvent {
  return (
    Boolean(value) &&
    typeof value === 'object' &&
    typeof (value as Record<string, unknown>).type === 'string'
  );
}

type ChatPanelProps = {
  presentation?: 'woven';
  knownRoots?: readonly { path: string; lastUsedAt: string }[];
  newChatRequest?: number;
  folderSelectionPending?: boolean;
  onFolderSelectionPending?: (pending: boolean) => void;
  onBindingChange?: (binding: { root: string | null; locked: boolean }) => void;
  /** Reports whether a New chat request went ahead (false when the unsent-draft confirmation was declined or a turn was running). */
  onNewChatSettled?: (started: boolean) => void;
  onDraftCaptured?: () => void;
  workflowFeedback?: WorkflowFeedbackRequest;
  onWorkflowFeedbackHandled?: () => void;
  onActiveSessionChange?: (sessionId: string | undefined) => void;
  onSessionBootedPrompt?: (input: { sessionId: string; prompt: string; persona: string }) => void;
  fileCatalog?: readonly string[];
  onOpenFile?: (path: string) => void;
  selectedMethods?: QualifiedMethodReference[];
  onSelectedMethodsChange?: (methods: QualifiedMethodReference[]) => void;
  onOpenMethods?: () => void;
  /** The Plan tab model, or null when this chat has no plan state to show. */
  onPlanPanelChange?: (model: NativePlanPanelModel | null) => void;
  /** A "Plan · Revision N" link in the conversation asks the host to open that revision. */
  onOpenPlan?: (revision: number) => void;
  /** What the agent is doing now (working, waiting for an answer, reconnecting, stopping, idle). */
  onTurnPhaseChange?: (phase: TurnPhase) => void;
  resumeConversation?: ResumeConversationRequest;
  onConversationResumed?: (sessionId: string) => void;
};

export function ChatPanel({ workflowFeedback, onWorkflowFeedbackHandled, onDraftCaptured, onActiveSessionChange, onSessionBootedPrompt, presentation, knownRoots = NO_KNOWN_ROOTS, newChatRequest = 0, folderSelectionPending = false, onFolderSelectionPending, onBindingChange, onNewChatSettled, fileCatalog = NO_FILE_CATALOG, onOpenFile, selectedMethods = NO_SELECTED_METHODS, onSelectedMethodsChange = IGNORE_SELECTED_METHODS, onOpenMethods, onPlanPanelChange, onOpenPlan, onTurnPhaseChange, resumeConversation, onConversationResumed }: ChatPanelProps = {}): JSX.Element {
  const { projectRoot, applyProjectRoot } = useWorkspace();
  const { optsPayload } = useToolkit();
  const { appendEvent, clearEvents, hydrateEvents, setStreaming } = useHarnessEventActions();
  const pathname = usePathname();
  const searchParams = useSearchParams();
  const [draft, setDraft] = useState('');
  const [attachments, setAttachments] = useState<UiAttachment[]>([]);
  const [draftStorageWritable, setDraftStorageWritable] = useState(true);
  const [draftStorageWarning, setDraftStorageWarning] = useState<string | null>(null);
  const [loadedDraftKey, setLoadedDraftKey] = useState<string | null>(null);
  const [pickerOpen, setPickerOpen] = useState(false);
  const [operatorMode, setOperatorMode] = useState<string>(DEFAULT_OPERATOR_MODE);
  const [interactionMode, setInteractionMode] = useState<InteractionMode>('chat');
  // Explicit model/reasoning choice for the next session. Null means the
  // catalog default published by Runtime status; a pair outside the current
  // catalog is dropped rather than substituted.
  const [modelChoice, setModelChoice] = useState<HarnessModelSelection | null>(null);
  const hostedBootstrap = useHostedBootstrap();
  // The catalog belongs to the signed-in account. While the selected folder
  // is still being checked or set up, the last reported account catalog keeps
  // the selectors meaningful; a folder problem never reads as signed out.
  const modelCatalog = useMemo(
    () => selectHostedModelCatalog(hostedBootstrap.snapshot) ?? (hostedBootstrap.snapshot?.registration === 'registered' ? null : selectAccountModelCatalog(hostedBootstrap.account)),
    [hostedBootstrap.snapshot, hostedBootstrap.account]
  );
  const modelSelectorTitle = useMemo(() => modelSelectorUnavailableTitle(hostedBootstrap), [hostedBootstrap]);
  useEffect(() => {
    if (modelCatalog && modelChoice && !isSelectionInCatalog(modelCatalog, modelChoice)) setModelChoice(null);
  }, [modelCatalog, modelChoice]);
  const [planCapability, setPlanCapability] = useState<NativePlanCapabilityResponse>({ schemaVersion: 'chirality.native-plan-capability/v3', status: 'unavailable', reason: 'Start a chat to check native Plan Mode support.' });
  const [planRevisions, setPlanRevisions] = useState<readonly NativePlanRevision[]>([]);
  const [planClarifications, setPlanClarifications] = useState<readonly NativePlanClarification[]>([]);
  const [planRefreshing, setPlanRefreshing] = useState(false);
  const [clarificationPendingId, setClarificationPendingId] = useState<string | number>();
  const [planClarificationError, setPlanClarificationError] = useState<string | null>(null);
  const [planExportStatus, setPlanExportStatus] = useState<string | null>(null);
  const [conversationBinding, setConversationBinding] = useState<{ projectRoot: string; selectedRootAtBinding: string } | null>(null);
  const [activeSession, setActiveSession] = useState<ActiveSession | null>(null);
  const activeSessionIdRef = useRef<string>();
  const lastInstructionSequenceRef = useRef(0);
  const [isRunning, setIsRunning] = useState(false);
  // Live turn facts behind the phase shown to the reader: whether the stream is
  // open yet, whether the panel is re-attaching after a dropped connection
  // (attempt count), and whether Stop was pressed and is awaiting the Runtime.
  const [turnStage, setTurnStage] = useState<'preparing' | 'streaming' | null>(null);
  const [reconnectAttempt, setReconnectAttempt] = useState<number | null>(null);
  const [stopRequested, setStopRequested] = useState(false);
  // Plan executions for the active session: which revision each execution
  // turn ran and how it ended (local record; the Runtime keeps the turns).
  const [planExecutions, setPlanExecutions] = useState<readonly PlanExecutionRecord[]>([]);
  const [preparedExecution, setPreparedExecution] = useState<{ revision: number } | null>(null);
  // Runtime owns the turn; this panel only observes it. The abort controller
  // closes the current observation (start or attach) without touching the turn.
  const turnObservation = useRef<AbortController | null>(null);
  const [nativeFolderError, setNativeFolderError] = useState<string | null>(null);
  const [attachmentPickPending, setAttachmentPickPending] = useState(false);
  const nativeSelectionActive = useRef(false);
  const [folderSyncError, setFolderSyncError] = useState<string | null>(null);
  const composerRef = useRef<HTMLTextAreaElement | null>(null);
  const bindingGeneration = useRef(0);
  // True only while a create request is outstanding, so a MODEL_NOT_IN_CATALOG
  // rejection can be told apart from one raised for an existing session.
  const sessionCreateInFlight = useRef(false);
  // A failed boot response never means creation failed. Retain its identity so
  // the next explicit Send only reconciles this session, never creates twice.
  const pendingBootstrap = useRef<{
    session: Awaited<ReturnType<typeof createHarnessSession>>;
    selectedRootAtBinding: string;
    persona: string;
    mode: string;
  }>();
  const canonicalTransition = useRef<{ from: string; to: string; persona: string; mode: string } | null>(null);
  const previousContext = useRef<{ root: string | null; persona: string; mode: string } | null>(null);
  const newChatSeen = useRef(newChatRequest);
  const resumeRequestSeen = useRef(0);
  const capturedTitleSessions = useRef(new Set<string>());
  const selectedMethodsSnapshot = useRef<readonly QualifiedMethodReference[]>(selectedMethods);
  const selectedMethodsRevision = useRef(0);
  const [runtimeStatus, setRuntimeStatus] = useState<string | null>(null);
  const [runtimeError, setRuntimeError] = useState<HarnessUiError | null>(null);
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: 'seed-1',
      role: 'assistant',
      persona: resolvePersona(searchParams.get('agent')),
      text: presentation === 'woven' ? 'What would you like to work on?' : 'Harness chat wiring is active. Select a Working Root and send a prompt.'
    }
  ]);

  const runtimeEpoch = useRuntimeEpoch();

  // The pair shown in the selectors and sent with the next turn: the explicit
  // choice when it is in the catalog, else the session's last recorded pair
  // when that is, else the catalog default. Never a pair Runtime did not publish.
  const recordedPair = activeSession ?? (pendingBootstrap.current ? recordedModelSelection(pendingBootstrap.current.session) : null);
  const recordedSelection: HarnessModelSelection | null = recordedPair?.model && recordedPair.reasoningEffort
    ? { model: recordedPair.model, reasoningEffort: recordedPair.reasoningEffort } : null;
  const nextTurnSelection: HarnessModelSelection | null = modelCatalog
    ? (isSelectionInCatalog(modelCatalog, modelChoice) ? modelChoice
      : isSelectionInCatalog(modelCatalog, recordedSelection) ? recordedSelection : modelCatalog.selection)
    : null;

  const refreshNativePlan = useCallback(async (sessionId: string, signal?: AbortSignal, manual = false): Promise<void> => {
    if (manual) setPlanRefreshing(true);
    try {
      const result = await listNativePlanRevisions(sessionId, signal);
      if (!signal?.aborted && activeSessionIdRef.current === sessionId) setPlanRevisions(result.revisions);
    } finally {
      if (manual && !signal?.aborted && activeSessionIdRef.current === sessionId) setPlanRefreshing(false);
    }
  }, []);

  const refreshNativePlanClarifications = useCallback(async (sessionId: string, signal?: AbortSignal): Promise<void> => {
    const result = await listNativePlanClarifications(sessionId, signal);
    if (!signal?.aborted && activeSessionIdRef.current === sessionId) setPlanClarifications(result.clarifications);
  }, []);

  const clearNativePlanProjection = useCallback((): void => {
    setPlanCapability({ schemaVersion: 'chirality.native-plan-capability/v3', status: 'unavailable', reason: 'Checking Native Plan Mode support for this chat.' });
    setPlanRevisions([]);
    setPlanClarifications([]);
    setPlanRefreshing(false);
    setClarificationPendingId(undefined);
    setPlanClarificationError(null);
    setPlanExportStatus(null);
  }, []);

  useEffect(() => {
    activeSessionIdRef.current = activeSession?.sessionId;
    onActiveSessionChange?.(activeSession?.sessionId);
  }, [activeSession?.sessionId, onActiveSessionChange]);

  // Leaving a session (new chat, another chat, unmount) only stops observing
  // its turn; the Runtime keeps running it and reopening recovers it.
  useEffect(() => () => { turnObservation.current?.abort(); }, []);

  // The red banner under the composer is a record of one failed attempt, not a
  // live status. Once the main process reports a fresh binding, the reason it
  // gives ("runtime daemon client is not configured") is no longer true, so it
  // is dropped rather than left to outlive the outage. Cleared, never retried:
  // re-sending an operator's prompt without them asking is not ours to do.
  useEffect(() => {
    if (runtimeEpoch === 0) {
      return;
    }
    setRuntimeError(null);
  }, [runtimeEpoch]);

  const activePersona = useMemo(
    () => resolvePersona(searchParams.get('agent')),
    [searchParams]
  );
  const personaLabel = activePersona.toLowerCase().split('_').map(word => word[0].toUpperCase() + word.slice(1)).join(' ');
  const activeMode = useMemo(() => resolveMode(pathname), [pathname]);

  if (!sameMethodSelection(selectedMethodsSnapshot.current, selectedMethods)) {
    selectedMethodsSnapshot.current = selectedMethods;
    selectedMethodsRevision.current += 1;
  }

  const draftRoot = activeSession?.projectRoot ?? conversationBinding?.selectedRootAtBinding ?? projectRoot;
  // Unbound entry drafts remain role-specific. Once a Runtime session exists,
  // its stable id owns the draft across role transitions and keeps two chats
  // with the same root and role isolated from one another.
  const draftPersona = activeSession ? `session:${activeSession.sessionId}` : activePersona;
  const draftStorageKey = useMemo(() => {
    if (!draftRoot) {
      return null;
    }
    return buildChatDraftStorageKey(draftRoot, draftPersona, activeMode);
  }, [draftRoot, draftPersona, activeMode]);
  const currentAttachmentContext = useRef({ projectRoot, draftStorageKey });
  currentAttachmentContext.current = { projectRoot, draftStorageKey };
  const draftIdentityReady = typeof window === 'undefined' || Boolean(draftStorageKey && loadedDraftKey === draftStorageKey);

  useEffect(() => {
    setActiveSession((existing) => {
      if (
        existing &&
        (existing.projectRoot === projectRoot || existing.selectedRootAtBinding === projectRoot) &&
        existing.mode === activeMode
      ) {
        return existing;
      }
      return null;
    });
  }, [projectRoot, activePersona, activeMode]);

  const previousDraftContext = useRef({ root: draftRoot, persona: draftPersona });
  useEffect(() => {
    const prior = previousDraftContext.current;
    const roleOnlyChange = !activeSession && prior.root === draftRoot && prior.persona !== draftPersona && !prior.persona.startsWith('session:');
    previousDraftContext.current = { root: draftRoot, persona: draftPersona };
    if (!draftStorageKey || typeof window === 'undefined') {
      setLoadedDraftKey(null);
      setDraft('');
      setAttachments([]);
      onSelectedMethodsChange([]);
      setModelChoice(null);
      setDraftStorageWritable(true);
      setDraftStorageWarning(null);
      return;
    }

    const result = readChatDraftSnapshotFromStorage(window.localStorage, draftStorageKey);
    setDraft(result.snapshot.draft);
    setAttachments(result.snapshot.attachments);
    if (!roleOnlyChange) setModelChoice(result.snapshot.model && result.snapshot.reasoningEffort
      ? { model: result.snapshot.model, reasoningEffort: result.snapshot.reasoningEffort }
      : null);
    // A chat's unsent permission or interaction choice belongs to that chat:
    // it comes back with the chat and never with a new chat's entry key.
    if (draftPersona.startsWith('session:')) {
      if (result.snapshot.permissionMode && isSupportedOperatorMode(result.snapshot.permissionMode)) setOperatorMode(result.snapshot.permissionMode);
      if (result.snapshot.interactionMode) setInteractionMode(result.snapshot.interactionMode);
    }
    const hydratedMethods = isRunning && activeSession && result.snapshot.methods.length === 0
      ? selectedMethodsSnapshot.current
      : result.snapshot.methods;
    onSelectedMethodsChange([...hydratedMethods]);
    setDraftStorageWritable(result.writable);
    setDraftStorageWarning(result.warning);
    setLoadedDraftKey(draftStorageKey);
  }, [draftStorageKey]);

  useEffect(() => {
    if (!draftStorageKey || loadedDraftKey !== draftStorageKey || typeof window === 'undefined' || !draftStorageWritable) {
      return;
    }

    const result = persistChatDraftSnapshotToStorage(
      window.localStorage,
      draftStorageKey,
      {
        draft,
        attachments,
        methods: selectedMethods,
        ...(modelChoice ? { model: modelChoice.model, reasoningEffort: modelChoice.reasoningEffort } : {}),
        ...(draftPersona.startsWith('session:') && isSupportedOperatorMode(operatorMode) ? { permissionMode: operatorMode, interactionMode } : {})
      }
    );

    if (!result.writable) {
      setDraftStorageWritable(false);
    }

    if (result.warning) {
      setDraftStorageWarning((existing) => existing ?? result.warning);
    }
  }, [draftStorageKey, loadedDraftKey, draft, attachments, selectedMethods, modelChoice, draftStorageWritable, draftPersona, operatorMode, interactionMode]);

  // Plan execution records follow the session. A record left "running" by a
  // closed window is settled from the Runtime's own turn state and log below
  // (recoverActiveTurn); it is never assumed complete.
  useEffect(() => {
    const sessionId = activeSession?.sessionId;
    setPreparedExecution(null);
    if (!sessionId || typeof window === 'undefined') { setPlanExecutions([]); return; }
    setPlanExecutions(readPlanExecutionRecords(window.localStorage, sessionId));
  }, [activeSession?.sessionId]);
  const planExecutionsLoadedFor = useRef<string | undefined>(undefined);
  useEffect(() => {
    const sessionId = activeSession?.sessionId;
    if (!sessionId || typeof window === 'undefined') { planExecutionsLoadedFor.current = undefined; return; }
    if (planExecutionsLoadedFor.current !== sessionId) { planExecutionsLoadedFor.current = sessionId; return; }
    writePlanExecutionRecords(window.localStorage, sessionId, planExecutions);
  }, [planExecutions, activeSession?.sessionId]);

  useEffect(() => {
    if (!activeSession) {
      clearNativePlanProjection();
      setInteractionMode('chat');
      return;
    }
    const controller = new AbortController();
    void getNativePlanCapability(activeSession.sessionId, controller.signal)
      .then(capability => {
        if (controller.signal.aborted || activeSessionIdRef.current !== activeSession.sessionId) return;
        setPlanCapability(capability);
        if (!nativePlanAvailable(capability)) setInteractionMode('chat');
      })
      .catch(error => {
        if (controller.signal.aborted || activeSessionIdRef.current !== activeSession.sessionId) return;
        setPlanCapability({ schemaVersion: 'chirality.native-plan-capability/v3', status: 'unavailable', reason: error instanceof Error ? error.message : 'Native Plan Mode is unavailable.' });
        setInteractionMode('chat');
      });
    void refreshNativePlan(activeSession.sessionId, controller.signal)
      .catch(() => { if (!controller.signal.aborted) setPlanRevisions([]); });
    void refreshNativePlanClarifications(activeSession.sessionId, controller.signal)
      .catch(() => { if (!controller.signal.aborted) setPlanClarifications([]); });
    return () => controller.abort();
  }, [activeSession?.sessionId, runtimeEpoch, refreshNativePlan, refreshNativePlanClarifications, clearNativePlanProjection]);

  useEffect(() => {
    if (!activeSession || !isRunning || interactionMode !== 'native-plan') return;
    const controller = new AbortController();
    let requestActive = false;
    const poll = async (): Promise<void> => {
      if (requestActive || controller.signal.aborted) return;
      requestActive = true;
      try {
        await Promise.allSettled([
          refreshNativePlanClarifications(activeSession.sessionId, controller.signal),
          refreshNativePlan(activeSession.sessionId, controller.signal)
        ]);
      } finally {
        requestActive = false;
      }
    };
    void poll();
    const interval = window.setInterval(() => { void poll(); }, 1_000);
    return () => { controller.abort(); window.clearInterval(interval); };
  }, [activeSession?.sessionId, isRunning, interactionMode, refreshNativePlan, refreshNativePlanClarifications]);

  useEffect(() => {
    const expected = canonicalTransition.current;
    const previous = previousContext.current;
    const isCanonicalSynchronization = expected && previous?.root === expected.from && projectRoot === expected.to && activePersona === expected.persona && activeMode === expected.mode;
    if (!isCanonicalSynchronization) bindingGeneration.current++;
    canonicalTransition.current = null;
    previousContext.current = { root: projectRoot, persona: activePersona, mode: activeMode };
  }, [projectRoot, activePersona, activeMode]);

  useEffect(() => {
    onBindingChange?.({ root: conversationBinding?.projectRoot ?? projectRoot, locked: Boolean(conversationBinding) || isRunning });
  }, [conversationBinding, projectRoot, isRunning, onBindingChange]);

  useEffect(() => {
    const field = composerRef.current;
    if (!field) return;
    field.style.height = 'auto';
    field.style.height = `${Math.min(field.scrollHeight, 132)}px`;
  }, [draft]);

  // Closes the open chat in this panel (New chat). This clears only the
  // current local view; no runtime record is deleted.
  const resetConversationRef = useRef<() => void>(() => {});
  resetConversationRef.current = () => {
    bindingGeneration.current++;
    turnObservation.current?.abort();
    activeSessionIdRef.current = undefined;
    pendingBootstrap.current = undefined;
    clearNativePlanProjection();
    lastInstructionSequenceRef.current = 0;
    setActiveSession(null); setConversationBinding(null); setDraft(''); setAttachments([]); onSelectedMethodsChange([]); setMessages([]);
    setOperatorMode(DEFAULT_OPERATOR_MODE);
    setRuntimeError(null); setRuntimeStatus(null); setFolderSyncError(null);
    clearEvents();
  };

  useEffect(() => {
    if (newChatSeen.current === newChatRequest) return;
    newChatSeen.current = newChatRequest;
    if (isRunning || folderSelectionPending) { onNewChatSettled?.(false); return; }
    if ((draft.trim() || attachments.length || selectedMethods.length) && !window.confirm('Start a new chat and discard the unsent draft, attachments, and methods?')) { onNewChatSettled?.(false); return; }
    resetConversationRef.current();
    onNewChatSettled?.(true);
  }, [newChatRequest, isRunning, folderSelectionPending, draft, attachments, selectedMethods, onNewChatSettled]);

  useEffect(() => {
    if (!resumeConversation || resumeConversation.requestId === resumeRequestSeen.current || isRunning) return;
    const { projection } = resumeConversation;
    const continuation = projection.session?.continuation;
    if (!continuation || continuation.roleId !== activePersona || continuation.projectRoot !== projectRoot) return;
    resumeRequestSeen.current = resumeConversation.requestId;
    setSteerReceipts(recoverSteeringReceipts(projection.selectedSessionId, projection.events ?? [], typeof window !== 'undefined' ? window.localStorage : undefined));
    pendingBootstrap.current = undefined;
    bindingGeneration.current += 1;
    lastInstructionSequenceRef.current = projection.instructionHistory.reduce((maximum, record) => Math.max(maximum, record.sequence), 0);
    const nextMessages: ChatMessage[] = projection.transcript.items.flatMap<ChatMessage>(item => {
      if (item.kind === 'terminal' && item.status === 'interrupted') {
        const ending = interruptedTurnPresentation(item.terminalReason);
        return [{ id: `replay-${item.key}`, role: 'assistant' as const, text: ending.message, outcome: ending.outcome, outcomeDescription: ending.message, interrupted: ending.outcome === 'interrupted', turnId: item.turnId }];
      }
      if (item.kind !== 'message' || !item.role || (!item.text && !item.attachments?.length)) return [];
      const recordedRole = item.role === 'assistant'
        ? recordedRoleForTurn(item.turnId, projection.instructionHistory, projection.instructionBases)
        : undefined;
      return [{ id: `replay-${item.key}`, role: item.role === 'user' ? 'operator' as const : 'assistant' as const,
        ...(item.role === 'assistant' ? { ...(recordedRole ? { persona: recordedRole } : {}), projectRoot: continuation.projectRoot,
          ...(item.turnId ? { turnId: item.turnId, recordedActivity: projection.events ? deriveTurnActivityFromEvents(projection.events, item.turnId) : deriveTurnActivityFromTranscript(projection.transcript.items, item.turnId) } : {}) } : {}),
        turnId: item.turnId, phase: item.phase, receipt: item.eventType === 'codex.steer' ? (item.summary ?? (item.status === 'accepted' ? 'Update received' : item.status === 'failed' ? 'Update rejected' : 'Awaiting update receipt')) : undefined,
        text: item.text ?? '', ...(item.role === 'user' && item.attachments?.length ? { attachments: item.attachments.map(buildUiAttachment) } : {}) }];
    });
    const latestBasis = projection.instructionBases.at(-1);
    let lastOperatorIndex = -1;
    for (let index = nextMessages.length - 1; index >= 0; index -= 1) {
      if (nextMessages[index]?.role === 'operator') { lastOperatorIndex = index; break; }
    }
    if (lastOperatorIndex >= 0 && (latestBasis || projection.instructionHistory.length)) {
      nextMessages[lastOperatorIndex] = { ...nextMessages[lastOperatorIndex],
        ...(latestBasis ? { instructionBasis: latestBasis } : {}), instructionHistory: projection.instructionHistory };
    }
    const nextSession: ActiveSession = {
      sessionId: projection.selectedSessionId,
      ...(projection.session?.bootstrapConfirmed === false ? { bootstrapPending: true } : {}),
      projectRoot: continuation.projectRoot,
      selectedRootAtBinding: continuation.projectRoot,
      persona: continuation.roleId,
      mode: activeMode,
      selectedMethods: continuation.selectedMethods,
      methodSelectionRevision: continuation.methodSelectionRevision,
      instructionBasisId: continuation.instructionBasisId,
      ...(projection.session?.model ? { model: projection.session.model } : {}),
      ...(projection.session?.reasoningEffort ? { reasoningEffort: projection.session.reasoningEffort } : {})
    };
    if (nextSession.bootstrapPending) pendingBootstrap.current = {
      session: { sessionId: nextSession.sessionId, projectRoot: nextSession.projectRoot, persona: nextSession.persona,
        mode: nextSession.mode, createdAt: projection.observedAt, updatedAt: projection.observedAt },
      selectedRootAtBinding: nextSession.selectedRootAtBinding, persona: nextSession.persona, mode: nextSession.mode
    };
    activeSessionIdRef.current = nextSession.sessionId;
    clearNativePlanProjection();
    setConversationBinding({ projectRoot: continuation.projectRoot, selectedRootAtBinding: continuation.projectRoot });
    setActiveSession(nextSession);
    setOperatorMode(continuation.permissionMode);
    setInteractionMode(continuation.interactionMode);
    setMessages(nextMessages.length ? nextMessages : [{ id: `resumed-${projection.selectedSessionId}`, role: 'assistant', persona: continuation.roleId, projectRoot: continuation.projectRoot, text: 'Continue this conversation when you are ready.',
      ...(latestBasis ? { instructionBasis: latestBasis } : {}), instructionHistory: projection.instructionHistory }]);
    setRuntimeError(null); setRuntimeStatus(null); setFolderSyncError(null);
    if (projection.events) hydrateEvents([...projection.events]); else clearEvents();
    onConversationResumed?.(nextSession.sessionId);
    void recoverActiveTurn(nextSession);
  }, [resumeConversation, isRunning, activePersona, activeMode, projectRoot, clearEvents, onConversationResumed, clearNativePlanProjection]);

  const selectNativeFolder = useCallback(async (intent: { path?: string; error?: string }) => {
    if (intent.error) { setNativeFolderError(intent.error); return; }
    if (conversationBinding || isRunning || folderSelectionPending || nativeSelectionActive.current) {
      setNativeFolderError('Start a new chat before opening another folder.'); return;
    }
    if (!intent.path) { setNativeFolderError('Drop a folder from Finder to choose it.'); return; }
    nativeSelectionActive.current = true; onFolderSelectionPending?.(true); setNativeFolderError(null);
    try {
      if (!await applyProjectRoot(intent.path)) setNativeFolderError('This folder could not be selected.');
    } finally { nativeSelectionActive.current = false; onFolderSelectionPending?.(false); }
  }, [conversationBinding, isRunning, folderSelectionPending, applyProjectRoot, onFolderSelectionPending]);

  useEffect(() => {
    if (presentation !== 'woven') return;
    return getNativeFolderBridge()?.subscribeOpen(intent => { void selectNativeFolder(intent); });
  }, [presentation, selectNativeFolder]);

  useEffect(() => {
    if (presentation !== 'woven' || !projectRoot) return;
    let cancelled = false;
    void getNativeFolderBridge()?.registerRecent(projectRoot).then(result => {
      if (!cancelled && !result.ok) setNativeFolderError(result.error ?? 'Unable to register this folder in Open Recent.');
    }).catch(() => { if (!cancelled) setNativeFolderError('Unable to register this folder in Open Recent.'); });
    return () => { cancelled = true; };
  }, [presentation, projectRoot]);

  async function ensureSessionBooted(): Promise<ActiveSession> {
    if (!projectRoot) {
      throw new Error('Select a Working Root before sending a prompt.');
    }

    if (
      activeSession && !activeSession.bootstrapPending &&
      (activeSession.projectRoot === projectRoot || activeSession.selectedRootAtBinding === projectRoot) &&
      activeSession.mode === activeMode
    ) {
      return activeSession;
    }

    const generation = bindingGeneration.current;
    const selectedRootAtBinding = conversationBinding?.selectedRootAtBinding ?? projectRoot;
    const pending = pendingBootstrap.current;
    if (pending && (pending.persona !== activePersona || pending.mode !== activeMode ||
      (pending.selectedRootAtBinding !== projectRoot && pending.session.projectRoot !== projectRoot))) {
      throw new HarnessApiClientError(409, 'INVALID_REQUEST', 'The created chat is still awaiting initialization.', { bootstrapState: 'conflict', sessionId: pending.session.sessionId });
    }
    let session = pending?.session;
    let boot: { session: Awaited<ReturnType<typeof getHarnessSession>> };
    if (pending) {
      setRuntimeStatus('Checking session initialization...');
      const recorded = await getHarnessSession(pending.session.sessionId);
      const recordedRole = 'schemaVersion' in recorded && recorded.schemaVersion === 'chirality.session/v3'
        ? ('roleId' in recorded ? recorded.roleId : undefined) : recorded.persona;
      if (recordedRole !== pending.persona || recorded.sessionId !== pending.session.sessionId ||
        (pending.session.projectRoot && recorded.projectRoot !== pending.session.projectRoot)) {
        throw new HarnessApiClientError(409, 'INVALID_REQUEST', 'Session reconciliation returned a different chat.', { bootstrapState: 'conflict', sessionId: pending.session.sessionId });
      }
      if (!isSessionBootConfirmed(recorded)) {
        const status = 'status' in recorded ? recorded.status : undefined;
        throw new HarnessApiClientError(409, 'ENGINE_UNAVAILABLE', 'Session initialization is not confirmed.', {
          bootstrapState: status === 'running' ? 'pending' : status === 'failed' || status === 'interrupted' ? 'failed' : 'unknown',
          sessionId: pending.session.sessionId
        });
      }
      boot = { session: recorded };
    } else {
    setRuntimeStatus('Creating session...');
    sessionCreateInFlight.current = true;
    session = await createHarnessSession({
      projectRoot: conversationBinding?.projectRoot ?? projectRoot,
      persona: activePersona,
      roleId: activePersona,
      mode: activeMode,
      interactionMode,
      permissionMode: operatorMode as 'readOnly' | 'ask' | 'workspaceWrite' | 'bypass',
      selectedMethods,
      // The pair shown in the selectors is the session default. Runtime
      // validates it against the catalog and rejects rather than substitutes;
      // each turn then carries its own model and effort.
      ...(nextTurnSelection ? { modelSelection: nextTurnSelection } : {})
    });
    sessionCreateInFlight.current = false;
    pendingBootstrap.current = { session, selectedRootAtBinding, persona: activePersona, mode: activeMode };

    setRuntimeStatus('Booting session...');
    boot = await bootHarnessSession(
      optsPayload
        ? {
            sessionId: session.sessionId,
            opts: optsPayload
          }
        : {
            sessionId: session.sessionId
          }
    );
    }

    if (generation !== bindingGeneration.current) throw new Error('The chat context changed while the session was starting.');
    const runtimeSession = boot.session as typeof boot.session & Partial<RuntimeSessionRecordV3>;
    const nextSession: ActiveSession = {
      sessionId: boot.session.sessionId,
      projectRoot: boot.session.projectRoot,
      selectedRootAtBinding,
      persona: activePersona,
      mode: activeMode,
      selectedMethods: runtimeSession.schemaVersion === 'chirality.session/v3' && Array.isArray(runtimeSession.selectedMethods)
        ? runtimeSession.selectedMethods : selectedMethods,
      methodSelectionRevision: runtimeSession.schemaVersion === 'chirality.session/v3' && typeof runtimeSession.methodSelectionRevision === 'number'
        ? runtimeSession.methodSelectionRevision : 0,
      instructionBasisId: runtimeSession.schemaVersion === 'chirality.session/v3' && typeof runtimeSession.instructionBasisId === 'string'
        ? runtimeSession.instructionBasisId : '',
      ...recordedModelSelection(runtimeSession, session)
    };
    activeSessionIdRef.current = nextSession.sessionId;
    if (conversationBinding && nextSession.projectRoot !== conversationBinding.projectRoot) {
      throw new Error('The new agent session returned a different folder. Start a new chat to use that folder.');
    }
    if (presentation === 'woven') {
      setConversationBinding(existing => existing ?? { projectRoot: nextSession.projectRoot, selectedRootAtBinding });
    }
    setActiveSession(nextSession);
    pendingBootstrap.current = undefined;
    if (presentation === 'woven' && nextSession.projectRoot !== projectRoot) {
      canonicalTransition.current = { from: projectRoot, to: nextSession.projectRoot, persona: activePersona, mode: activeMode };
      const applied = await applyProjectRoot(nextSession.projectRoot);
      if (!applied) canonicalTransition.current = null;
      if (generation !== bindingGeneration.current) throw new Error('The chat context changed while its folder was being synchronized.');
      if (!applied) setFolderSyncError('The session is bound to its recorded folder, but file browsing could not switch to it. Start a new chat to choose a folder again.');
    }
    return nextSession;
  }

  type TurnObservationOutcome = { rejectedBeforeStart?: boolean; assistantText: string; error: HarnessApiClientError | Error | null; terminal: boolean; outcome: TurnOutcome | null; turnId?: string };

  /**
   * Observe one Runtime-owned turn to its end. `start` opens the first stream
   * (POST turn, or an attach). A stream that closes without a terminal frame is
   * a lost connection, never a finished turn: the panel re-attaches from the
   * last seen frame with backoff and shows "Reconnecting" until the Runtime
   * reports the turn over. Harness events are de-duplicated by eventId, so an
   * attach from seq 0 after a persisted replay never double-counts.
   */
  async function observeTurn(input: {
    session: ActiveSession;
    assistantId: string;
    signal: AbortSignal;
    start: (onEvent: (event: HarnessTurnStreamEvent) => void) => Promise<void>;
    resetTextOnStart?: boolean;
    /** This turn is already Runtime-owned; an initial failed attach must retry. */
    reattach?: boolean;
    turnId?: string;
    /** Event ids already in the bridged log (hydrated from replay); never appended again. */
    seenEventIds?: Iterable<string>;
  }): Promise<TurnObservationOutcome> {
    const { session, assistantId, signal } = input;
    const seen = new Set<string>(input.seenEventIds ?? []);
    // Text deltas are assembled from the observed stream even when the log
    // already holds them: an attach from seq 0 is the complete text source.
    const textSeen = new Set<string>();
    let lastSeq = 0;
    let receivedFrames = 0;
    let streamOpened = false;
    let assistantText = '';
    const observedEvents = new Map<string, HarnessEvent>();
    let nativeTextObserved = false;
    let textSource: 'chat:delta' | 'message.delta' | null = null;
    let terminal = false;
    let turnIdSeen = Boolean(input.turnId);
    let turnId: string | undefined = input.turnId;
    let interrupted = false;
    let interruption: ReturnType<typeof interruptedTurnPresentation> | undefined;
    // Set only when the turn ended without a terminal fact for it: the stream
    // dropped, the Runtime no longer holds the turn, and the log for this turn
    // shows no end. Never inferred from silence alone.
    let outcomeUnknown = false;
    let error: HarnessApiClientError | Error | null = null;

    const setAssistant = (patch: Partial<ChatMessage>): void => {
      setMessages((existing) => existing.map((item) => item.id === assistantId ? { ...item, ...patch } : item));
    };
    if (turnId) setAssistant({ turnId });
    const appendText = (chunk: string, source: 'chat:delta' | 'message.delta'): void => {
      if (!chunk || nativeTextObserved) return;
      textSource ??= source;
      if (textSource !== source) return;
      assistantText += chunk;
      setAssistant({ text: assistantText });
    };

    const recordInterruption = (reason: unknown): void => {
      // A generic exit frame must not erase the terminal's specific cause.
      if (!interruption || reason === 'service-shutdown' || reason === 'service-restart') {
        interruption = interruptedTurnPresentation(reason);
      }
      interrupted = interruption.outcome === 'interrupted';
      setAssistant({ interrupted, outcome: interruption.outcome, outcomeDescription: interruption.message, ...(!assistantText ? { text: interruption.message } : {}) });
      if (!assistantText) assistantText = interruption.message;
    };
    const onEvent = (streamEvent: HarnessTurnStreamEvent): void => {
      if (signal.aborted) return;
      streamOpened = true;
      // Emitted only when the proxy has an actual Runtime subscription. Its
      // own keepalive comments are never evidence of Runtime recovery.
      setReconnectAttempt(null);
      setRuntimeStatus('Running turn...');
      if (streamEvent.event === 'transport:connected') return;
      if (streamEvent.event === 'harness:event' && isHarnessEvent(streamEvent.data) && turnId && streamEvent.data.turnId && streamEvent.data.turnId !== turnId) {
        throw new HarnessApiClientError(404, 'SESSION_NOT_FOUND', 'The stream belongs to a different turn.', { reason: 'TURN_NOT_ACTIVE' });
      }
      receivedFrames += 1;
      if (typeof streamEvent.seq === 'number' && streamEvent.seq > lastSeq) lastSeq = streamEvent.seq;

      if (streamEvent.event === 'harness:event') {
        if (!isHarnessEvent(streamEvent.data)) return;
        const harnessEvent = { ...streamEvent.data, data: streamEvent.data.data ?? {} };
        observedEvents.set(harnessEvent.eventId, harnessEvent);
        if (harnessEvent.type === 'codex.steer') {
          const data = harnessEvent.data;
          if (typeof data.operationId === 'string' && typeof data.expectedTurnId === 'string' && typeof data.text === 'string' && ['submitted', 'accepted', 'rejected', 'unknown'].includes(String(data.status))) {
            recordSteeringReceipt({ sessionId: session.sessionId, operationId: data.operationId, expectedTurnId: data.expectedTurnId, text: data.text, status: data.status as SteeringReceipt['status'], message: typeof data.message === 'string' ? data.message : undefined });
            if (data.status === 'accepted') setDraft(current => current.trim() === data.text ? '' : current);
          }
        }
        const nativeItems = deriveTranscriptView([...observedEvents.values()]).items.filter(item => item.nativeItemId || item.eventType === 'codex.steer');
        if (nativeItems.some(item => item.nativeItemId)) {
          nativeTextObserved = true;
          assistantText = nativeItems.filter(item => item.role === 'assistant').map(item => item.text ?? '').join('\n\n');
          setAssistant({ text: assistantText, nativeItems });
        } else if (nativeItems.length) setAssistant({ nativeItems });

        const duplicate = seen.has(harnessEvent.eventId);
        seen.add(harnessEvent.eventId);
        if (!duplicate) appendEvent(harnessEvent);
        if (!turnIdSeen && typeof harnessEvent.turnId === 'string' && harnessEvent.turnId) {
          turnIdSeen = true;
          turnId = harnessEvent.turnId;
          setAssistant({ turnId: harnessEvent.turnId });
        }
        if (harnessEvent.type === 'message.delta') {
          if (!textSeen.has(harnessEvent.eventId)) {
            textSeen.add(harnessEvent.eventId);
            appendText(readTextField(harnessEvent.data) ?? '', 'message.delta');
          }
          return;
        }
        if (harnessEvent.type === 'turn.interrupted') {
          // Rendered the moment it arrives, not after the stream closes (R17-F1).
          terminal = true;
          recordInterruption(harnessEvent.data?.reason);
          return;
        }
        if (harnessEvent.type === 'turn.failed') {
          terminal = true;
          const payload = harnessEvent.data ?? {};
          const message = typeof payload.message === 'string' && payload.message.trim() ? payload.message : 'Turn failed.';
          const code = typeof payload.code === 'string' && payload.code.trim() ? payload.code : 'SDK_FAILURE';
          error ??= new HarnessApiClientError(500, code, message, payload.details);
          return;
        }
        if (TERMINAL_HARNESS_EVENTS.has(harnessEvent.type)) { terminal = true; return; }
        if (harnessEvent.type.includes('clarification') || harnessEvent.type.includes('native-plan') ||
          ((harnessEvent.type === 'codex.request' || harnessEvent.type === 'codex.request.resolved') && interactionMode === 'native-plan')) {
          void refreshNativePlanClarifications(session.sessionId).catch(() => {});
        }
        return;
      }

      if (streamEvent.event === 'chat:delta') {
        appendText(readTextField(streamEvent.data) ?? '', 'chat:delta');
        return;
      }

      if (streamEvent.event === 'chat:complete') {
        const completed = readTextField(streamEvent.data);
        if (completed && !nativeTextObserved) { assistantText = completed; setAssistant({ text: assistantText }); }
        return;
      }

      if (streamEvent.event === 'turn:error' && streamEvent.data && typeof streamEvent.data === 'object') {
        const payload = streamEvent.data as Record<string, unknown>;
        const fatal = payload.fatal !== false;
        const errorMessage = typeof payload.message === 'string' && payload.message.trim().length > 0 ? payload.message : 'Turn failed during streaming.';
        if (fatal) {
          const errorType = typeof payload.errorType === 'string' && payload.errorType.trim().length > 0 ? payload.errorType : 'SDK_FAILURE';
          const errorStatus = typeof payload.status === 'number' ? payload.status : 500;
          error = new HarnessApiClientError(errorStatus, errorType, errorMessage, payload.details);
          // An engine failure can fence the signed-in account underneath a
          // "ready" status. Re-read status so the account row reports it.
          if (errorType === 'ENGINE_UNAVAILABLE') hostedBootstrap.refresh?.();
        }
        return;
      }

      if (streamEvent.event === 'process:exit' && streamEvent.data && typeof streamEvent.data === 'object') {
        terminal = true;
        const payload = streamEvent.data as Record<string, unknown>;
        const exitCode = typeof payload.exitCode === 'number' ? payload.exitCode : 0;
        const exitInterrupted = payload.interrupted === true;
        if (exitInterrupted) {
          recordInterruption(payload.reason);
        }
        // Runtime normalizes a confirmed operator interruption to 130 plus
        // interrupted:true. A bare 130 or any other nonzero exit still fails.
        if (exitCode !== 0 && !(exitCode === 130 && exitInterrupted) && !error) {
          const errorMessage = typeof payload.error === 'string' && payload.error.trim().length > 0 ? payload.error : `Turn failed with exit code ${exitCode}.`;
          const errorType = typeof payload.errorType === 'string' && payload.errorType.trim().length > 0 ? payload.errorType : null;
          const errorStatus = typeof payload.status === 'number' ? payload.status : 500;
          error = errorType ? new HarnessApiClientError(errorStatus, errorType, errorMessage, payload.errorDetails) : new Error(errorMessage);
        }
      }
    };

    let attempt = 0;
    let open = input.start;
    while (!signal.aborted) {
      let dropped = false;
      const framesBefore = receivedFrames;
      try {
        await open(onEvent);
      } catch (caught) {
        if (signal.aborted) break;
        const transportFailure = !(caught instanceof HarnessApiClientError) ||
          Boolean(caught.details && typeof caught.details === 'object' && 'transportReason' in caught.details);
        if (!input.reattach && !streamOpened && !transportFailure && attempt === 0 && open === input.start && receivedFrames === framesBefore) {
          // The first stream never opened: report it as today.
          return { assistantText, error: caught instanceof Error ? caught : new Error(String(caught)), terminal: false, outcome: null, rejectedBeforeStart: true };
        }
        if (isTurnNotActive(caught)) {
          // Nothing left to attach to: the turn ended while we were away, or
          // the Runtime restarted. The persisted log carries the outcome.
          await settleFromReplay();
          break;
        }
        dropped = true;
      }
      if (terminal || signal.aborted) break;
      // The stream closed without a terminal frame. Ask the Runtime whether
      // the turn is still running before deciding anything: a clean close of
      // a finished turn settles from the log, and only a turn that is still
      // active (or a Runtime that cannot be reached) is a reconnect.
      let state: Awaited<ReturnType<typeof getHarnessTurnState>> | undefined;
      if (!dropped) {
        try { state = await getHarnessTurnState(session.sessionId, signal); } catch { state = undefined; }
      }
      if (signal.aborted) break;
      if (state && turnId && state.turnId !== turnId) {
        await settleFromReplay();
        break;
      }
      if (state && !state.active && state.lastSeq <= lastSeq) {
        await settleFromReplay();
        break;
      }
      if (!state || state.active) {
        // The connection dropped while the turn continues. Never show Idle.
        setRuntimeStatus(attempt === 0 ? 'Reconnecting to the running turn...' : `Reconnecting to the running turn (attempt ${attempt + 1})...`);
        setReconnectAttempt(attempt + 1);
        await wait(RECONNECT_DELAYS_MS[Math.min(attempt, RECONNECT_DELAYS_MS.length - 1)], signal);
        attempt += 1;
        if (signal.aborted) break;
      }
      // Either the turn is still active, or it finished with frames we have
      // not seen: attach after the last frame we processed.
      if (!turnId) {
        // Without a submission identity, neither a retained stream nor an
        // older replay ending can establish which request was accepted.
        await settleFromReplay();
        break;
      }
      const after = lastSeq;
      open = (handler) => attachHarnessTurn(session.sessionId, after, handler, signal, turnId);
    }
    if (terminal) setReconnectAttempt(null);

    async function settleFromReplay(): Promise<void> {
      terminal = true;
      setReconnectAttempt(null);
      try {
        const replay = await replaySessionEvents(session.sessionId);
        const scoped = turnId ? replay.events.filter(event => event.turnId === turnId) : [];
        const events = scoped.filter(event => !seen.has(event.eventId));
        // Text the Runtime recorded after the connection dropped belongs to
        // this reply: append what was missed rather than showing a torn message.
        for (const event of events) {
          seen.add(event.eventId); appendEvent(event); observedEvents.set(event.eventId, event);
          if (assistantText && event.type === 'message.delta' && (!turnId || event.turnId === turnId) && !textSeen.has(event.eventId)) {
            textSeen.add(event.eventId);
            appendText(readTextField(event.data) ?? '', 'message.delta');
          }
        }
        // Settle from this turn's own record. With the turn id known, only its
        // events count; an older turn's ending is never read as this one's.
        const last = [...scoped].reverse().find(event => TERMINAL_HARNESS_EVENTS.has(event.type));
        if (!last) {
          // No terminal for this exact turn means its outcome is unknown;
          // a clean observer close alone cannot establish completion.
          if (!error) outcomeUnknown = true;
        } else if (last.type === 'turn.interrupted') {
          recordInterruption(last.data?.reason);
        } else if (last.type === 'turn.failed' && !error) {
          const payload = last.data ?? {};
          error = new HarnessApiClientError(500, typeof payload.code === 'string' ? payload.code : 'SDK_FAILURE', typeof payload.message === 'string' ? payload.message : 'Turn failed.', payload.details);
        }
        const recovered = deriveTranscriptView(scoped).items.filter(item => item.nativeItemId || item.eventType === 'codex.steer');
        if (recovered.some(item => item.nativeItemId)) {
          assistantText = recovered.filter(item => item.role === 'assistant').map(item => item.text ?? '').join('\n\n');
          setAssistant({ text: assistantText, nativeItems: recovered });
        } else if (recovered.length) setAssistant({ nativeItems: recovered });
        if (!assistantText) {
          const textTurnId = turnId ?? last?.turnId;
          const text = scoped.filter(event => event.type === 'message.delta' && event.turnId === textTurnId).map(event => readTextField(event.data) ?? '').join('');
          if (text) { assistantText = text; setAssistant({ text }); }
        }
      } catch {
        // Without a readable terminal record, the observer cannot establish
        // completion. Keep streamed text and report the uncertainty.
        if (!error) outcomeUnknown = true;
      }
    }

    const outcome: TurnOutcome | null = !terminal ? null : interruption ? interruption.outcome : outcomeUnknown ? 'unknown' : interrupted ? 'interrupted' : error ? 'failed' : 'completed';
    if (outcome) setAssistant({ outcome });
    if (terminal && observedEvents.size) setAssistant({ recordedActivity: deriveTurnActivityFromEvents([...observedEvents.values()], turnId) });
    return { assistantText, error: interruption && interruption.outcome !== 'interrupted' ? null : error, terminal, outcome, ...(turnId ? { turnId } : {}) };
  }

  /**
   * Opening a chat asks the Runtime whether it owns an active turn for it. If so
   * the persisted events are replayed, the panel is marked running, and the
   * live turn is attached from seq 0 (de-duplicated by eventId) so missed
   * activity, streamed text and outstanding decisions are recovered without
   * re-sending anything.
   */
  async function recoverActiveTurn(session: ActiveSession): Promise<void> {
    let state: Awaited<ReturnType<typeof getHarnessTurnState>>;
    try { state = await getHarnessTurnState(session.sessionId); } catch { return; }
    if (!state.active || activeSessionIdRef.current !== session.sessionId) return;
    const observation = new AbortController();
    turnObservation.current?.abort();
    turnObservation.current = observation;
    const assistantId = `assistant-recovered-${session.sessionId}-${state.turnId ?? Date.now()}`;
    setIsRunning(true);
    setStreaming(true);
    setRuntimeError(null);
    setStopRequested(false);
    setTurnStage('streaming');
    setReconnectAttempt(1);
    setRuntimeStatus('Reconnecting to the running turn...');
    setMessages((existing) => {
      // The retained stream replays this active turn from seq 0. Replace its
      // replayed assistant/steering items instead of showing two copies.
      const withoutPartial = existing.filter(message => state.turnId && message.turnId === state.turnId
        ? message.role === 'operator' && !message.receipt
        : !(message.role === 'assistant' && !message.text && !message.interrupted && message.id.startsWith('replay-')));
      return [...withoutPartial, { id: assistantId, role: 'assistant', persona: session.persona, projectRoot: session.projectRoot, text: '', ...(state.turnId ? { turnId: state.turnId } : {}) }];
    });
    try {
      const hydratedIds: string[] = [];
      try {
        const replay = await replaySessionEvents(session.sessionId);
        if (!observation.signal.aborted) {
          hydrateEvents(replay.events);
          for (const event of replay.events) hydratedIds.push(event.eventId);
        }
      } catch {
        // Missed activity is then recovered from the retained turn buffer alone.
      }
      if (observation.signal.aborted) return;
      const outcome = await observeTurn({
        session, assistantId, signal: observation.signal, seenEventIds: hydratedIds, reattach: true, turnId: state.turnId,
        start: (onEvent) => attachHarnessTurn(session.sessionId, 0, onEvent, observation.signal, state.turnId)
      });
      if (observation.signal.aborted) return;
      if (outcome.error) setRuntimeError(toHarnessUiError(outcome.error, { sessionModel: session.model, origin: 'session' }));
      if (outcome.outcome === 'unknown') setRuntimeError({ title: 'Turn outcome unknown', message: 'The connection to the Runtime was lost and its record does not show how this turn ended.', nextStep: 'Reopen the chat to check the recorded result. Nothing was re-sent.' });
      // Only an observed ending settles the record. When the attach never
      // opened the Runtime still owns the turn; the record stays running and
      // the no-live-turn effect settles it from the log later.
      if (outcome.terminal) settleRecoveredExecution(state.turnId, outcome.outcome ?? 'unknown');
      if (!outcome.assistantText.trim() && !outcome.error) {
        setMessages((existing) => existing.map((item) => item.id === assistantId ? { ...item, text: 'No assistant text was returned for this turn.' } : item));
      }
      const replay = await replaySessionEvents(session.sessionId).catch(() => undefined);
      const replaySession = replay?.session;
      if (replaySession && 'schemaVersion' in replaySession && replaySession.schemaVersion === 'chirality.session/v3') {
        const recorded = recordedModelSelection(replaySession as RuntimeSessionRecordV3);
        setActiveSession(existing => existing?.sessionId === session.sessionId ? { ...existing, ...recorded } : existing);
      }
      if (interactionMode === 'native-plan') void refreshNativePlan(session.sessionId).catch(() => {});
    } finally {
      if (turnObservation.current === observation) turnObservation.current = null;
      if (!observation.signal.aborted) {
        setRuntimeStatus(null);
        setIsRunning(false);
        setStreaming(false);
        setTurnStage(null);
        setReconnectAttempt(null);
        setStopRequested(false);
      }
    }
  }

  /**
   * A plan execution left "running" by an earlier window is settled from the
   * Runtime: the live turn we just observed, or the log for its turn id. A
   * record whose turn the log cannot settle ends as unknown, never completed.
   */
  function settleRecoveredExecution(turnId: string | undefined, outcome: TurnOutcome): void {
    setPlanExecutions(current => {
      const running = runningPlanExecution(current);
      if (!running) return current;
      const matches = Boolean(running.turnId && turnId === running.turnId);
      // Never assign an observed turn to an idless or differently bound plan
      // attempt. Its own ending remains unproved, even if this turn completed.
      return settlePlanExecution(current, running, { status: matches ? outcome : 'unknown', endedAt: new Date().toISOString() });
    });
  }

  // Opening a chat with no live turn: any execution still marked running is
  // settled from the log (by its turn id) or reported as unknown.
  useEffect(() => {
    const sessionId = activeSession?.sessionId;
    if (!sessionId || isRunning) return;
    const running = runningPlanExecution(planExecutions);
    if (!running) return;
    let cancelled = false;
    void (async () => {
      let outcome: TurnOutcome = 'unknown';
      try {
        const state = await getHarnessTurnState(sessionId);
        if (state.active) return;
        if (running.turnId) {
          const replay = await replaySessionEvents(sessionId);
          const last = [...replay.events].reverse().find(event => event.turnId === running.turnId && TERMINAL_HARNESS_EVENTS.has(event.type));
          if (last?.type === 'turn.completed') outcome = 'completed';
          else if (last?.type === 'turn.interrupted') outcome = interruptedTurnPresentation(last.data?.reason).outcome;
          else if (last?.type === 'turn.cancelled') outcome = 'interrupted';
          else if (last?.type === 'turn.failed') outcome = 'failed';
        }
      } catch {
        // The Runtime could not be asked: leave the record running for now.
        return;
      }
      if (cancelled || activeSessionIdRef.current !== sessionId) return;
      setPlanExecutions(current => settlePlanExecution(current, running, { status: outcome, endedAt: new Date().toISOString() }));
    })();
    return () => { cancelled = true; };
  }, [activeSession?.sessionId, isRunning, planExecutions]);

  async function interruptTurn(): Promise<void> {
    if (!activeSession || !isRunning) {
      return;
    }

    try {
      setStopRequested(true);
      setRuntimeStatus('Interrupt requested...');
      setRuntimeError(null);
      await interruptHarnessSession({ sessionId: activeSession.sessionId });
    } catch (error) {
      setStopRequested(false);
      setRuntimeError(toHarnessUiError(error));
      setRuntimeStatus(null);
    }
  }

  const [steerReceipts, setSteerReceipts] = useState<SteeringReceipt[]>([]);
  const sessionSteerReceipts = steerReceipts.filter(receipt => receipt.sessionId === activeSession?.sessionId);
  const [steerPending, setSteerPending] = useState(false);
  const [receiptChecking, setReceiptChecking] = useState<string | null>(null);
  const receiptCheckInFlight = useRef(false);
  const steerOperationInFlight = useRef(false);
  const currentRuntimeTurnId = [...messages].reverse().find(message => message.role === 'assistant')?.turnId;
  const steerReceipt = isRunning ? sessionSteerReceipts.filter(receipt => receipt.expectedTurnId === currentRuntimeTurnId).at(-1) : undefined;
  const unknownSteerDraft = sessionSteerReceipts.some(receipt => (receipt.status === 'unknown' || receipt.status === 'submitted') && receipt.text === draft.trim());
  function recordSteeringReceipt(receipt: SteeringReceipt): void {
    persistSteeringReceipt(receipt, typeof window !== 'undefined' ? window.localStorage : undefined);
    setSteerReceipts(current => mergeSteeringReceipt(current, receipt));
  }

  async function checkSteeringReceipt(receipt: SteeringReceipt): Promise<void> {
    if (receiptCheckInFlight.current) return;
    receiptCheckInFlight.current = true;
    setReceiptChecking(receipt.operationId);
    try {
      const result = await checkHarnessSteeringReceipt(receipt.sessionId, { operationId: receipt.operationId, expectedTurnId: receipt.expectedTurnId });
      if (result.operationId !== receipt.operationId || result.turnId !== receipt.expectedTurnId) throw new Error('The returned receipt identifies another update. Delivery remains unconfirmed.');
      recordSteeringReceipt({ ...receipt, status: result.status, message: result.message });
      if (activeSessionIdRef.current !== receipt.sessionId) return;
      if (result.status === 'accepted') setDraft(current => current.trim() === receipt.text ? '' : current);
      // A completed turn no longer has a live event subscription. Reflect the
      // receipt response in its existing message; Runtime owns durable evidence.
      const key = `steer:${JSON.stringify([receipt.sessionId, receipt.operationId])}`;
      const label = result.status === 'accepted' ? 'Update received' : result.status === 'rejected' ? 'Update rejected' : 'Delivery unconfirmed';
      setMessages(current => current.map(message => ({ ...message,
        ...(message.id === `replay-${key}` ? { receipt: label } : {}),
        ...(message.nativeItems ? { nativeItems: message.nativeItems.map(item => item.key === key ? { ...item, status: result.status === 'accepted' ? 'accepted' : result.status === 'rejected' ? 'failed' : 'queued', summary: label } : item) } : {})
      })));
    } catch (error) {
      recordSteeringReceipt({ ...receipt, message: error instanceof Error ? error.message : 'Update delivery remains unconfirmed.' });
    } finally { receiptCheckInFlight.current = false; setReceiptChecking(null); }
  }

  async function submitSteering(): Promise<void> {
    if (!activeSession || !currentRuntimeTurnId || steerOperationInFlight.current || stopRequested || reconnectAttempt !== null || unknownSteerDraft || !draft.trim()) return;
    steerOperationInFlight.current = true;
    const sessionId = activeSession.sessionId;
    const text = draft.trim();
    const operationId = crypto.randomUUID();
    const receipt: SteeringReceipt = { sessionId, operationId, expectedTurnId: currentRuntimeTurnId, text, status: 'submitted' };
    setSteerPending(true);
    // Save identity before the browser request: it may fail before Runtime can
    // persist intent, and a reload must still check without re-sending text.
    recordSteeringReceipt(receipt);
    try {
      const result = await steerHarnessSession(sessionId, { operationId, expectedTurnId: currentRuntimeTurnId, text });
      recordSteeringReceipt({ ...receipt, status: result.status, message: result.message });
      if (activeSessionIdRef.current === sessionId && result.status === 'accepted') setDraft(current => current.trim() === text ? '' : current);
    } catch (error) {
      recordSteeringReceipt({ ...receipt, status: 'unknown', message: error instanceof Error ? error.message : 'The update receipt could not be confirmed.' });
    } finally { steerOperationInFlight.current = false; setSteerPending(false); }
  }

  async function submitDraft(event: FormEvent<HTMLFormElement>): Promise<void> {
    event.preventDefault();
    if (isRunning) { await submitSteering(); return; }
    if (unknownSteerDraft) return;
    if (folderSelectionPending || nativeSelectionActive.current || !draftIdentityReady || !isSupportedOperatorMode(operatorMode)) return;
    const text = draft.trim();

    if (!text && attachments.length === 0) {
      return;
    }

    const requestGeneration = bindingGeneration.current;
    const preservedDraft = draft;
    const preservedAttachments = attachments;
    const preservedMethods = [...selectedMethods];
    const submittedMethodsRevision = selectedMethodsRevision.current;
    const submittedDraftStorageKey = draftStorageKey;
    const submittedWithoutSession = activeSession === null;
    const submittedModelChoice = modelChoice;
    let bootedSession: ActiveSession | null = activeSession;
    let definitelyNotStarted = true;
    // Sending the prepared "Execute plan" request is that revision's execution
    // attempt; an edited message without the marker is an ordinary turn.
    const submittedTurnId = crypto.randomUUID();
    const executedRevision = detectPlanExecution(text, preparedExecution);
    let submittedExecutions: readonly PlanExecutionRecord[] | undefined;
    let executionAttempt: { revision: number; attempt: number } | null = null;
    if (executedRevision !== null) {
      const startedAt = new Date().toISOString();
      const next = beginPlanExecution(planExecutions, executedRevision, startedAt, submittedTurnId);
      submittedExecutions = next;
      executionAttempt = { revision: executedRevision, attempt: next.at(-1)!.attempt };
      setPlanExecutions(next);
    }
    setPreparedExecution(null);

    setRuntimeError(null);
    setRuntimeStatus('Preparing turn...');
    setTurnStage('preparing');
    setReconnectAttempt(null);
    setStopRequested(false);
    setDraft('');
    setAttachments([]);
    setIsRunning(true);
    setStreaming(true);
    clearEvents();

    const operatorMessageId = `operator-${Date.now()}`;
    const assistantId = `assistant-${Date.now() + 1}`;

    const operatorMessage: ChatMessage = {
      id: operatorMessageId,
      role: 'operator',
      text,
      attachments: preservedAttachments,
      methods: preservedMethods
    };
    const assistantMessage: ChatMessage = {
      id: assistantId,
      role: 'assistant',
      persona: activePersona,
      text: ''
    };

    setMessages((existing) => [...existing, operatorMessage, assistantMessage]);

    try {
      const session = await ensureSessionBooted();
      bootedSession = session;
      const roleChanged = session.persona !== activePersona;
      let activeMethods = session.selectedMethods;
      let activeRevision = session.methodSelectionRevision;
      let activeBasisId = session.instructionBasisId;
      if (preservedMethods.length > 0 || roleChanged) {
        // A completed turn can adopt edited instructions or a different mode,
        // changing the basis without changing the method revision. Read the
        // current projection before forming the transition's compare-and-swap.
        const current = await getHarnessSession(session.sessionId) as RuntimeSessionRecordV3;
        if (current.sessionId !== session.sessionId || current.projectRoot !== session.projectRoot ||
          current.schemaVersion !== 'chirality.session/v3' ||
          (current.roleId !== undefined && current.roleId !== session.persona)) {
          throw new Error('The chat context changed before the workflow could be selected. Reload the conversation and try again.');
        }
        const replacement = await replaceSelectedMethods(session.sessionId, preservedMethods.length ? preservedMethods : undefined, {
          ...(roleChanged ? { roleId: activePersona as ChiralityRoleName } : {}),
          boundaryConfirmed: true,
          ...(preservedMethods.length ? { selectionMode: 'merge' as const } : {}),
          expectedRevision: current.methodSelectionRevision,
          expectedBasisId: current.instructionBasisId
        });
        activeMethods = replacement.methods;
        activeRevision = replacement.revision;
        activeBasisId = replacement.basisPreview.id;
        // The transition is durable even if the subsequent provider turn
        // fails. Advance the local CAS projection immediately so a retry does
        // not submit the pre-transition revision.
        setActiveSession(existing => existing?.sessionId === session.sessionId ? {
          ...existing,
          persona: activePersona,
          selectedMethods: activeMethods,
          methodSelectionRevision: activeRevision,
          instructionBasisId: activeBasisId
        } : existing);
      }
      await resolveSelectedContext({
        sessionId: session.sessionId,
        roleId: activePersona as ChiralityRoleName,
        methods: activeMethods,
        interactionMode,
        permissionMode: operatorMode as 'readOnly' | 'ask' | 'workspaceWrite' | 'bypass'
      });
      setMessages((existing) => existing.map((item) => item.id === assistantId ? { ...item, projectRoot: session.projectRoot } : item));
      if (text && !capturedTitleSessions.current.has(session.sessionId)) {
        capturedTitleSessions.current.add(session.sessionId);
        onSessionBootedPrompt?.({ sessionId: session.sessionId, prompt: text, persona: activePersona });
      }

      let nativePlanProduced = false;

      setRuntimeStatus('Running turn...');
      setTurnStage('streaming');

      const observation = new AbortController();
      turnObservation.current?.abort();
      turnObservation.current = observation;
      if (submittedExecutions) {
        // Do not wait for a React effect or for observation to finish: reload
        // after an ambiguous POST must retain this attempt's exact identity.
        setPlanExecutions(submittedExecutions);
        if (typeof window !== 'undefined') writePlanExecutionRecords(window.localStorage, session.sessionId, submittedExecutions);
      }
      definitelyNotStarted = false;
      const outcome = await observeTurn({
        session,
        assistantId,
        turnId: submittedTurnId,
        signal: observation.signal,
        start: (onEvent) => streamHarnessTurn(
          {
            sessionId: session.sessionId,
            turnId: submittedTurnId,
            message: text,
            attachments: preservedAttachments.map((item) => item.path),
            interactionMode,
            permissionMode: operatorMode as 'readOnly' | 'ask' | 'workspaceWrite' | 'bypass',
            // Model and reasoning effort are per turn (Codex `turn/start`).
            ...(nextTurnSelection ? { model: nextTurnSelection.model, reasoningEffort: nextTurnSelection.reasoningEffort } : {}),
            opts: { ...(optsPayload ?? {}), mode: operatorMode }
          },
          onEvent,
          observation.signal
        )
      });
      if (turnObservation.current === observation) turnObservation.current = null;
      if (observation.signal.aborted) return;
      const assistantText = outcome.assistantText;
      if (executionAttempt) {
        const target = executionAttempt;
        setPlanExecutions(current => settlePlanExecution(current,
          target, { status: outcome.outcome ?? (outcome.error ? 'failed' : 'unknown'), endedAt: new Date().toISOString() }));
      }
      const outcomeUnknown = outcome.outcome === 'unknown';
      if (outcomeUnknown) {
        // The request reached the Runtime and may have run to completion; the
        // message stays in the conversation (not back in the composer) so it
        // cannot be re-sent by accident. Session bookkeeping below still runs.
        setRuntimeError({ title: 'Turn outcome unknown', message: 'The connection to the Runtime was lost and its record does not show how this turn ended.', nextStep: 'Reopen the chat to check the recorded result. Nothing was re-sent.' });
      } else if (outcome.error) {
        definitelyNotStarted = outcome.rejectedBeforeStart === true;
        throw outcome.error;
      }

      if (!assistantText.trim() && !nativePlanProduced && interactionMode === 'native-plan') {
        const latest = await listNativePlanRevisions(session.sessionId).catch(() => undefined);
        nativePlanProduced = Boolean(latest?.revisions.some(revision => revision.revision > (planRevisions.at(-1)?.revision ?? 0)));
      }
      if (!assistantText.trim() && nativePlanProduced) {
        setMessages(existing => existing.filter(item => item.id !== assistantId));
      } else if (!assistantText.trim()) {
        setMessages((existing) =>
          existing.map((item) =>
            item.id === assistantId
              ? {
                  ...item,
                  text: outcomeUnknown ? 'No reply was received before the connection was lost.' : 'No assistant text was returned for this turn.'
                }
              : item
          )
        );
      }

      setRuntimeStatus(null);
      const replay = await replaySessionEvents(session.sessionId).catch(() => undefined);
      const recordedBasis = replay?.instructionBases.at(-1);
      const replaySession = replay?.session;
      const replayRuntimeSession: RuntimeSessionRecordV3 | undefined = replaySession && 'schemaVersion' in replaySession && replaySession.schemaVersion === 'chirality.session/v3'
        ? replaySession as RuntimeSessionRecordV3
        : undefined;
      const newInstructionHistory = replay?.instructionHistory.filter(record => record.sequence > lastInstructionSequenceRef.current) ?? [];
      if (replay?.instructionHistory.length) {
        lastInstructionSequenceRef.current = Math.max(...replay.instructionHistory.map(record => record.sequence));
      }
      if (recordedBasis || newInstructionHistory.length) {
        setMessages(existing => existing.map(item => item.id === operatorMessageId ? { ...item, ...(recordedBasis ? { instructionBasis: recordedBasis } : {}), instructionHistory: newInstructionHistory } : item));
      }
      setActiveSession(existing => existing?.sessionId === session.sessionId ? {
        ...existing,
        persona: activePersona,
        selectedMethods: replayRuntimeSession?.selectedMethods ?? recordedBasis?.selectedMethods ?? activeMethods,
        methodSelectionRevision: replayRuntimeSession?.methodSelectionRevision ?? activeRevision,
        instructionBasisId: replayRuntimeSession?.instructionBasisId ?? recordedBasis?.basisId ?? activeBasisId,
        ...(replayRuntimeSession ? recordedModelSelection(replayRuntimeSession) : {})
      } : existing);
      // Composer method references apply to the submitted message. A selection
      // made while this turn was streaming belongs to the next message and must
      // survive completion of the earlier turn.
      if (selectedMethodsRevision.current === submittedMethodsRevision) {
        onSelectedMethodsChange([]);
      }
      // The first successful turn moves draft ownership from the entry key to
      // the canonical Runtime session key. Consume the exact prior entry key
      // so its submitted method references cannot reappear in a later New
      // chat. Edits made during the turn already belong to the session key.
      // The model choice is not a per-message reference: it stays on the entry
      // key so the next new chat offers the same pair (still re-checked
      // against the current catalog before use).
      if (submittedWithoutSession && submittedDraftStorageKey && typeof window !== 'undefined') {
        persistChatDraftSnapshotToStorage(window.localStorage, submittedDraftStorageKey, {
          draft: '', attachments: [], methods: [],
          ...(submittedModelChoice ? { model: submittedModelChoice.model, reasoningEffort: submittedModelChoice.reasoningEffort } : {})
        });
      }
      if (interactionMode === 'native-plan') {
        void refreshNativePlan(session.sessionId)
          .catch(() => {});
      }
    } catch (error) {
      const origin = sessionCreateInFlight.current ? 'session-create' : 'session';
      sessionCreateInFlight.current = false;
      const uiError = toHarnessUiError(error, { sessionModel: bootedSession?.model, origin, bootBeforePrompt: Boolean(pendingBootstrap.current) && !bootedSession });
      // A bound chat can lose its visible context while this pre-turn request
      // is outstanding. Recover to its own draft key, never the newly selected
      // chat, and only when rejection proves no turn was started.
      if (definitelyNotStarted && !submittedWithoutSession && requestGeneration !== bindingGeneration.current && submittedDraftStorageKey && typeof window !== 'undefined') {
        const stored = readChatDraftSnapshotFromStorage(window.localStorage, submittedDraftStorageKey);
        if (stored.writable && !stored.snapshot.draft.trim() && stored.snapshot.attachments.length === 0) {
          const restored = persistChatDraftSnapshotToStorage(window.localStorage, submittedDraftStorageKey, {
            ...stored.snapshot, draft: preservedDraft, attachments: preservedAttachments, methods: preservedMethods
          });
          if (restored.writable) uiError.nextStep = 'Your unsent message is saved with its original chat. Reopen that chat to retry manually.';
        }
      }
      setRuntimeError(uiError);
      setRuntimeStatus(null);
      if (executionAttempt) {
        const target = executionAttempt;
        setPlanExecutions(current => runningPlanExecution(current)?.revision === target.revision ? settlePlanExecution(current, target, { status: 'failed', endedAt: new Date().toISOString() }) : current);
      }
      if (requestGeneration === bindingGeneration.current) {
        setDraft(preservedDraft);
        setAttachments(preservedAttachments);
        // The unbound-to-session draft-key transition may have hydrated an
        // empty composer while the first turn was starting. Restore the
        // submitted references unless the operator already chose a newer
        // nonempty set for the next message during the turn.
        if (preservedMethods.length > 0 && selectedMethodsRevision.current === submittedMethodsRevision) {
          onSelectedMethodsChange(preservedMethods);
        }
      }
      setMessages((existing) =>
        existing.filter((item) => item.id !== operatorMessageId && item.id !== assistantId)
      );
    } finally {
      setIsRunning(false);
      setStreaming(false);
      setTurnStage(null);
      setReconnectAttempt(null);
      setStopRequested(false);
    }
  }

  // What the agent is doing, for the status line, the activity strip and the
  // host. Waiting means the Runtime holds a request (approval or user input)
  // that the turn cannot proceed without; reconnecting means the stream
  // dropped while the Runtime still owns the turn.
  const { events: phaseEvents } = useHarnessEvents();
  const pendingRequestCount = useMemo(() => isRunning
    ? selectPendingServerRequests(phaseEvents, true).length + selectPendingPermissionRequests(phaseEvents, true).length
    : 0, [phaseEvents, isRunning]);
  const turnPhase: TurnPhase = !isRunning ? 'idle'
    : stopRequested ? 'stopping'
    : reconnectAttempt !== null ? 'reconnecting'
    : pendingRequestCount > 0 ? 'waiting'
    : turnStage === 'preparing' ? 'preparing'
    : 'working';
  useEffect(() => { onTurnPhaseChange?.(turnPhase); }, [turnPhase, onTurnPhaseChange]);
  useEffect(() => () => { onTurnPhaseChange?.('idle'); }, [onTurnPhaseChange]);
  const phaseStatusLine = turnPhaseStatusLine(turnPhase, { detail: turnPhase === 'preparing' || turnPhase === 'working' ? runtimeStatus : null, reconnectAttempt: reconnectAttempt ?? undefined, pendingRequests: pendingRequestCount });

  const appliedWorkflowFeedback = useRef<number>();
  useEffect(() => {
    if (!workflowFeedback || appliedWorkflowFeedback.current === workflowFeedback.sequence) return;
    if (folderSelectionPending || !draftIdentityReady) return;
    appliedWorkflowFeedback.current = workflowFeedback.sequence;
    onWorkflowFeedbackHandled?.();
    if (workflowFeedback.projectRoot !== projectRoot || isRunning) return;
    const prompt = workflowFeedbackPrompt(workflowFeedback);
    setDraft(current => current.trim() ? `${current}\n\n${prompt}` : prompt);
    onDraftCaptured?.();
    window.requestAnimationFrame(() => composerRef.current?.focus());
  }, [workflowFeedback, projectRoot, isRunning, folderSelectionPending, draftIdentityReady, onDraftCaptured, onWorkflowFeedbackHandled]);

  function beginPlanRevision(revision: number | undefined): void {
    setInteractionMode('native-plan');
    setDraft(revision
      ? `Revise plan revision ${revision}. Describe the changes you want me to make:\n\n`
      : 'Create a plan for:\n\n');
    onDraftCaptured?.();
    window.requestAnimationFrame(() => composerRef.current?.focus());
  }

  function beginPlanFollowUp(revision: NativePlanRevision, intent: 'execute' | 'workflow'): void {
    setInteractionMode('chat');
    const recordedPlan = nativePlanText(revision);
    // Execute prepares the request in the composer; the reader reviews and
    // sends it. Sending it is recorded as this revision's execution attempt.
    setPreparedExecution(intent === 'execute' ? { revision: revision.revision } : null);
    setDraft(intent === 'execute'
      ? `Execute the accepted native Plan Mode revision ${revision.revision} below. Preserve its recorded constraints.\n\n${planExecutionMarker(revision.revision)}\n${recordedPlan}`
      : `Use the core create-workflow method to prepare native Plan Mode revision ${revision.revision} below as a reusable project workflow draft at .chirality/workflow-drafts/<suitable-name>/WORKFLOW.md. Do not register it in .chirality/workflows or execute the plan. I will inspect the draft, provide feedback, and register it through the Workflows panel. Preserve its constraints and add valid purpose and applicability metadata.\n\n${planExecutionMarker(revision.revision)}\n${recordedPlan}`);
    onDraftCaptured?.();
    window.requestAnimationFrame(() => composerRef.current?.focus());
  }

  async function savePlanRevision(revision: NativePlanRevision): Promise<void> {
    if (!activeSession) return;
    const { sessionId, projectRoot: root } = activeSession;
    const bridge = window.chirality?.plans;
    try {
      const selection = bridge
        ? await bridge.chooseExportTarget({ projectRoot: root, revision: revision.revision })
        : { cancelled: false as const, targetRelativePath: window.prompt(`Save this plan in ${root} as`, `plans/native-plan-${revision.revision}.md`)?.trim() };
      if (activeSessionIdRef.current !== sessionId) return;
      if (selection.cancelled) {
        setPlanExportStatus(selection.error ?? 'Save cancelled.');
        return;
      }
      const targetRelativePath = selection.targetRelativePath;
      if (!targetRelativePath) { setPlanExportStatus('Save cancelled.'); return; }
      setPlanExportStatus('Saving plan…');
      const request = { sessionId, revision: revision.revision, targetRelativePath };
      let result;
      try {
        result = await exportNativePlanRevision(request);
      } catch (error) {
        if (activeSessionIdRef.current !== sessionId) return;
        if (!(error instanceof MethodSelectionClientError && error.status === 409)) throw error;
        const overwrite = bridge
          ? await bridge.confirmOverwrite({ projectRoot: root, targetRelativePath })
          : window.confirm(`${targetRelativePath} already exists. Replace it?`);
        if (activeSessionIdRef.current !== sessionId) return;
        if (!overwrite) { setPlanExportStatus('Save cancelled.'); return; }
        result = await exportNativePlanRevision({ ...request, overwrite: true });
      }
      if (activeSessionIdRef.current === sessionId) setPlanExportStatus(`Plan saved to ${root}/${result.targetRelativePath}`);
    } catch (error) {
      if (activeSessionIdRef.current === sessionId) setPlanExportStatus(error instanceof Error ? error.message : 'The plan could not be saved.');
    }
  }

  async function answerPlanClarification(clarification: NativePlanClarification, answers: Record<string, { answers: string[] }>): Promise<void> {
    if (!activeSession || clarificationPendingId !== undefined) return;
    const sessionId = activeSession.sessionId;
    setClarificationPendingId(clarification.requestId);
    setPlanClarificationError(null);
    try {
      await replyNativePlanClarification({ sessionId, requestId: clarification.requestId, answers });
      if (activeSessionIdRef.current !== sessionId) return;
      setPlanClarifications(current => current.filter(item => item.requestId !== clarification.requestId));
      await refreshNativePlan(sessionId).catch(() => {});
      await refreshNativePlanClarifications(sessionId).catch(() => {});
    } catch (error) {
      if (activeSessionIdRef.current !== sessionId) return;
      setPlanClarificationError(error instanceof Error ? error.message : 'The planning answers could not be sent. Try again.');
    } finally {
      if (activeSessionIdRef.current === sessionId) setClarificationPendingId(undefined);
    }
  }

  // The Plan tab renders the plan; this panel owns its state and the composer
  // the actions write into. Handlers read the latest closure through a ref so
  // the model only changes when the plan does.
  const planHandlers = useRef({ beginPlanRevision, beginPlanFollowUp, savePlanRevision, answerPlanClarification, refreshNativePlan });
  planHandlers.current = { beginPlanRevision, beginPlanFollowUp, savePlanRevision, answerPlanClarification, refreshNativePlan };
  const activeSessionForPlan = activeSession?.sessionId;
  const stablePlanHandlers = useMemo(() => ({
    onRefresh: () => { const id = activeSessionIdRef.current; if (id) void planHandlers.current.refreshNativePlan(id, undefined, true).catch(() => {}); },
    onRevise: (revision: number | undefined) => planHandlers.current.beginPlanRevision(revision),
    onExecute: (revision: NativePlanRevision) => planHandlers.current.beginPlanFollowUp(revision, 'execute'),
    onSaveAsWorkflow: (revision: NativePlanRevision) => planHandlers.current.beginPlanFollowUp(revision, 'workflow'),
    onSave: (revision: NativePlanRevision) => { void planHandlers.current.savePlanRevision(revision); },
    onReplyClarification: (clarification: NativePlanClarification, answers: Record<string, { answers: string[] }>) => { void planHandlers.current.answerPlanClarification(clarification, answers); }
  }), []);
  const planPanelModel = useMemo<NativePlanPanelModel | null>(() => {
    if (presentation !== 'woven' || (interactionMode !== 'native-plan' && planRevisions.length === 0 && planClarifications.length === 0)) return null;
    return {
      sessionId: activeSessionForPlan, revisions: planRevisions, clarifications: planClarifications, active: interactionMode === 'native-plan', refreshing: planRefreshing,
      projectRoot: activeSession?.projectRoot, fileCatalog, clarificationPendingId, clarificationError: planClarificationError, exportStatus: planExportStatus,
      executions: planExecutions, preparedRevision: preparedExecution?.revision,
      actionsDisabled: isRunning || !nativePlanAvailable(planCapability), onOpenFile, ...stablePlanHandlers
    };
  }, [presentation, interactionMode, planRevisions, planClarifications, planRefreshing, activeSessionForPlan, activeSession?.projectRoot, fileCatalog, clarificationPendingId, planClarificationError, planExportStatus, planExecutions, preparedExecution, isRunning, planCapability, onOpenFile, stablePlanHandlers]);
  useEffect(() => { onPlanPanelChange?.(planPanelModel); }, [planPanelModel, onPlanPanelChange]);
  useEffect(() => () => { onPlanPanelChange?.(null); }, [onPlanPanelChange]);

  // Live activity for the turn under observation: the buffer holds this turn's
  // events (it is cleared at send) or, after a reconnect, the whole session's,
  // scoped by turn id once the Runtime has named it.
  const liveEvents = phaseEvents;
  const liveActivity = useMemo(() => {
    const target = [...messages].reverse().find(message => message.role === 'assistant');
    const result = new Map<string, TurnActivity>();
    for (const message of messages) {
      if (message.role !== 'assistant') continue;
      if (message.turnId && liveEvents.some(event => event.turnId === message.turnId)) result.set(message.id, deriveTurnActivityFromEvents(liveEvents, message.turnId));
      else if (!message.turnId && message === target && isRunning) result.set(message.id, deriveTurnActivityFromEvents(liveEvents));
    }
    return result;
  }, [messages, liveEvents, isRunning]);

  // Follow new content while the reader is at (or within a short band of) the
  // bottom; a deliberate scroll up preserves their place and offers a way back.
  const transcriptRef = useRef<HTMLDivElement | null>(null);
  const [following, setFollowing] = useState(true);
  const suppressFollowUntil = useRef(0);
  const scrollToLatest = useCallback((behavior: ScrollBehavior = 'auto') => {
    const node = transcriptRef.current;
    if (!node) return;
    node.scrollTo?.({ top: node.scrollHeight, behavior });
    if (!node.scrollTo) node.scrollTop = node.scrollHeight;
  }, []);
  const onTranscriptScroll = useCallback(() => {
    const node = transcriptRef.current;
    if (!node) return;
    const gap = node.scrollHeight - node.scrollTop - node.clientHeight;
    setFollowing(gap <= FOLLOW_REARM_THRESHOLD_PX);
  }, []);
  const renderedMessages = messages.flatMap(message => message.nativeItems?.some(item => item.nativeItemId)
    ? message.nativeItems.map((item, index) => ({ ...message, id: `${message.id}:${item.key}`, role: item.role === 'user' ? 'operator' as const : 'assistant' as const,
      text: item.text ?? '', phase: item.phase, nativeItems: undefined,
      recordedActivity: item.role === 'assistant' && !message.nativeItems!.slice(index + 1).some(next => next.role === 'assistant') ? (liveActivity.get(message.id) ?? message.recordedActivity) : undefined,
      interrupted: item.role === 'assistant' && !message.nativeItems!.slice(index + 1).some(next => next.role === 'assistant') ? message.interrupted : undefined,
      outcome: item.role === 'assistant' && !message.nativeItems!.slice(index + 1).some(next => next.role === 'assistant') ? message.outcome : undefined,
      receipt: item.eventType === 'codex.steer' ? (item.summary ?? (item.status === 'accepted' ? 'Update received' : item.status === 'failed' ? 'Update rejected' : 'Awaiting update receipt')) : undefined }))
    : [...(message.nativeItems ?? []).filter(item => item.eventType === 'codex.steer').map(item => ({
      ...message, id: `${message.id}:${item.key}`, role: 'operator' as const, text: item.text ?? '',
      nativeItems: undefined, recordedActivity: undefined, interrupted: undefined, outcome: undefined,
      receipt: item.summary ?? (item.status === 'accepted' ? 'Update received' : item.status === 'failed' ? 'Update rejected' : 'Awaiting update receipt')
    })), message]);
  const lastAssistantIndex = renderedMessages.reduce((last, message, index) => message.role === 'assistant' ? index : last, -1);
  const messageCount = messages.length;
  const lastMessageId = messages.at(-1)?.id;
  useEffect(() => {
    // A new message (send, reply, resume) always lands in view; the reader can
    // scroll up afterwards to keep reading history.
    setFollowing(true);
    if (typeof window !== 'undefined' && typeof window.requestAnimationFrame === 'function') window.requestAnimationFrame(() => scrollToLatest());
    else scrollToLatest();
  }, [messageCount, lastMessageId, activeSession?.sessionId, scrollToLatest]);
  useEffect(() => {
    const node = transcriptRef.current;
    if (!node || typeof ResizeObserver === 'undefined') return;
    const content = node.firstElementChild;
    if (!content) return;
    const observer = new ResizeObserver(() => {
      if (!following || !isRunning || Date.now() < suppressFollowUntil.current) return;
      scrollToLatest();
    });
    observer.observe(content);
    return () => observer.disconnect();
  }, [following, isRunning, scrollToLatest]);
  const onTranscriptToggle = useCallback(() => { suppressFollowUntil.current = Date.now() + 400; }, []);

  // Desktop builds pick attachments through the native dialog (main process
  // canonicalises explicit selections; Runtime copies files on send). Web builds keep the in-app picker.
  const pickAttachments = async (): Promise<void> => {
    if (!projectRoot || attachmentPickPending) return;
    const bridge = getNativeAttachmentBridge();
    if (!bridge) { setPickerOpen(true); return; }
    const generation = bindingGeneration.current;
    const context = currentAttachmentContext.current;
    const isCurrent = () => generation === bindingGeneration.current
      && context.projectRoot === currentAttachmentContext.current.projectRoot
      && context.draftStorageKey === currentAttachmentContext.current.draftStorageKey;
    setAttachmentPickPending(true); setNativeFolderError(null);
    try {
      const result = await bridge.selectFiles({ projectRoot });
      if (!isCurrent()) return;
      if (result.cancelled) { if (result.error) setNativeFolderError(result.error); return; }
      const incoming = result.paths.map(buildUiAttachment);
      if (incoming.length) setAttachments(existing => mergeAttachments(existing, incoming));
    } catch (error) {
      if (!isCurrent()) return;
      setNativeFolderError(error instanceof Error ? error.message : 'Unable to attach files.');
    } finally { setAttachmentPickPending(false); }
  };

  return (
    <aside className={`panel panel--chat${presentation === 'woven' ? ' chat-panel--woven' : ''}`}>
      {presentation !== 'woven' ? <header className="panel-header">
        <h2>Chat Panel</h2>
        <p className="chat-meta">
          Role: {activePersona} | Section: {activeMode}
        </p>
      </header> : null}

      <div className="chat-conversation-stage">
      <div ref={transcriptRef} className={following ? 'panel-body chat-transcript' : 'panel-body chat-transcript chat-transcript--detached'} onScroll={onTranscriptScroll} onToggle={onTranscriptToggle}>
      <div className="chat-transcript-content">
        {!projectRoot ? (
          <p className="panel-empty">{presentation === 'woven' ? 'Choose a folder below to start a chat.' : 'Select a Working Root before starting a harness turn.'}</p>
        ) : null}
        {renderedMessages.map((message, index) => {
          const isStreaming = isRunning && message.role === 'assistant' && index === lastAssistantIndex;
          const lastForTurn = !renderedMessages.slice(index + 1).some(item => item.role === 'assistant' && item.turnId && item.turnId === message.turnId);
          const activity = lastForTurn ? (liveActivity.get(message.id) ?? message.recordedActivity ?? (isStreaming ? { items: [], running: 0, failed: 0, pendingApproval: 0 } : undefined)) : undefined;
          return <ConversationMessage key={message.id} id={message.id} role={message.role} presentation={presentation}
            speaker={message.role === 'operator' ? 'You' : (message.persona ?? 'Assistant').toLowerCase().split('_').map(word => word[0].toUpperCase() + word.slice(1)).join(' ')}
            persona={message.persona} streaming={isStreaming} phase={message.phase}
            body={message.text ? (message.role === 'assistant'
              ? <ChatMarkdown source={message.text} projectRoot={message.projectRoot} fileCatalog={fileCatalog} onOpenFile={onOpenFile} />
              : message.text) : null}
            activity={activity && message.role === 'assistant' ? <TurnActivityDisclosure activity={activity} running={isStreaming} /> : null}>
            {message.receipt ? <p role="status">{message.receipt}</p> : null}
            {isStreaming && (turnPhase === 'waiting' || turnPhase === 'reconnecting' || turnPhase === 'stopping') ? <p className="chat-runtime-status" data-turn-phase={turnPhase} role="status">{phaseStatusLine}</p> : null}
            {message.attachments && message.attachments.length > 0 ? (
              <AttachmentChips items={message.attachments} />
            ) : null}
            {message.role === 'assistant' && message.outcome && (message.outcome !== 'completed' || index === renderedMessages.length - 1)
              ? <p className={`chat-turn-status chat-turn-status--${message.outcome}`} role="status" data-turn-outcome={message.outcome} title={message.outcomeDescription ?? turnOutcomeDescription(message.outcome)}>{turnOutcomeLabel(message.outcome)}</p>
              : message.interrupted ? <p className="chat-turn-status chat-turn-status--interrupted" role="status" data-turn-outcome="interrupted" title={turnOutcomeDescription('interrupted')}>{turnOutcomeLabel('interrupted')}</p> : null}
            {message.methods?.length ? <ul className="method-chip-list" aria-label="Selected methods">{message.methods.map(method => <li key={`${method.sourceRootId}:${method.kind}:${method.name}`} className="method-chip"><span>{method.name}</span><small>{method.source}</small></li>)}</ul> : null}
            {message.instructionBasis || message.instructionHistory?.length ? <details className="chat-instruction-basis"><summary>Instruction basis</summary>
            {message.instructionBasis ? <>

              <p><code>{message.instructionBasis.basisId}</code> · {message.instructionBasis.roleId}</p>
              <ul>{message.instructionBasis.suppliedEntries.map((entry, index) => <li key={`${entry.sha256}:${index}`}><strong>{entry.kind}</strong> · {entry.id} · <code>{entry.sha256.slice(0, 12)}</code></li>)}</ul>
            </> : null}
            {message.instructionHistory?.length ? <ul className="chat-instruction-events" aria-label="Recorded instruction activity">
              {message.instructionHistory.map(record => <li key={record.historyId}>{instructionActivityLabel(record)}</li>)}
            </ul> : null}
            </details> : null}
          </ConversationMessage>;
        })}
        {presentation !== 'woven' ? planRevisions.map(revision => <article key={`native-plan-${revision.revision}`} className="chat-bubble chat-bubble--assistant native-plan-revision">
          <p className="chat-speaker">Native plan · revision {revision.revision}</p>
          <ChatMarkdown source={nativePlanText(revision)} projectRoot={activeSession?.projectRoot} fileCatalog={fileCatalog} onOpenFile={onOpenFile} />
          <button type="button" className="button-muted" onClick={() => savePlanRevision(revision)}>Export plan…</button>
        </article>) : null}
        {presentation !== 'woven' && planExportStatus ? <p role="status">{planExportStatus}</p> : null}
        {presentation === 'woven' && planRevisions.length ? <ul className="chat-plan-links" aria-label="Plan revisions">
          {planRevisions.map(revision => <li key={`plan-link-${revision.revision}`}><button type="button" className="chat-plan-link" title="Open this plan revision in the Plan tab" onClick={() => onOpenPlan?.(revision.revision)}>Plan · Revision {revision.revision}</button></li>)}
        </ul> : null}
        {presentation === 'woven' && !onPlanPanelChange && planPanelModel ? <NativePlanPanel model={planPanelModel} /> : null}
        <PermissionRequests sessionId={activeSession?.sessionId ?? null} active={isRunning} />
        <LiveSessionRequests sessionId={activeSession?.sessionId ?? null} active={isRunning} />
      </div>
      </div>
      {!following ? <button type="button" className="chat-jump-to-latest" onClick={() => { setFollowing(true); scrollToLatest('smooth'); }}>Jump to latest ↓</button> : null}
      </div>

      {/* Composer dock: every notice that sits between the transcript and the
          composer lives in one block, so the chat panel always lays out as
          exactly four rows (header / transcript / dock / composer). Before
          this wrapper the row count varied with state, the transcript's
          flexible row was squeezed below its own padding, and its box
          overflowed on top of the Attachments row (Stage C defect). */}
      <div className="chat-composer-dock">
        {sessionSteerReceipts.filter(receipt => receipt.status === 'unknown' || receipt.status === 'submitted').map(receipt => <div key={receipt.operationId} className="chat-steer-receipt">
          {receipt !== steerReceipt ? <p role="status">Update delivery unconfirmed: {receipt.text}{receipt.message ? ` · ${receipt.message}` : ''}</p> : null}
          <button type="button" className="button-muted" disabled={steerPending || receiptChecking !== null} onClick={() => void checkSteeringReceipt(receipt)}>{receiptChecking === receipt.operationId ? 'Checking delivery…' : 'Check delivery'}</button>
        </div>)}
        {draftStorageWarning ? (
          <div className="chat-storage-warning toolkit-warning" role="status" aria-live="polite">
            <p>{draftStorageWarning}</p>
            <button
              type="button"
              className="button-muted"
              onClick={() => {
                setDraftStorageWarning(null);
              }}
            >
              Dismiss
            </button>
          </div>
        ) : null}

        {presentation !== 'woven' ? (        <div className="chat-attachment-preview" aria-live="polite">
          <div className="chat-attachment-header">
            <strong>Attachments</strong>
            <div>
              <button
                type="button"
                className="button-muted"
                onClick={() => {
                  setPickerOpen(true);
                }}
                disabled={!projectRoot || isRunning}
              >
                Attach Files
              </button>
              <button
                type="button"
                className="button-muted"
                onClick={() => {
                  setAttachments([]);
                }}
                disabled={attachments.length === 0 || isRunning}
              >
                Clear
              </button>
            </div>
          </div>

          {attachments.length === 0 ? (
            <p className="panel-empty">No attachments selected.</p>
          ) : (
            <ul className="attachment-chip-list">
              {attachments.map((item) => (
                <li key={item.path} className="attachment-chip" title={item.path}>
                  <span>{item.displayName}</span>
                  <small>{item.clientType}</small>
                  <button
                    type="button"
                    className="button-muted"
                    onClick={() => {
                      setAttachments((existing) =>
                        existing.filter((entry) => entry.path !== item.path)
                      );
                    }}
                  >
                    Remove
                  </button>
                </li>
              ))}
            </ul>
          )}
        </div>) : null}

        {!isRunning && runtimeStatus ? <p className="chat-runtime-status">{runtimeStatus}</p> : null}

        {runtimeError ? (
          <div className="chat-runtime-error">
            <p className="chat-runtime-error-title">
              {runtimeError.title}
              {runtimeError.code ? ` (${runtimeError.code})` : ''}
            </p>
            <p>{runtimeError.message}</p>
            <p>{runtimeError.nextStep}</p>
          </div>
        ) : null}
        {!isSupportedOperatorMode(operatorMode) ? <p className="chat-runtime-error" role="alert">
          This recorded chat used an unknown permission mode ({operatorMode}). <button type="button" disabled={isRunning} onClick={() => setOperatorMode(DEFAULT_OPERATOR_MODE)}>Continue with Write in workspace</button>
        </p> : null}
      </div>

      <form
        className="chat-input-row"
        onDragOver={presentation === 'woven' ? event => { if (event.dataTransfer.types.includes('Files')) event.preventDefault(); } : undefined}
        onDrop={presentation === 'woven' ? event => {
          event.preventDefault();
          const bridge = getNativeFolderBridge();
          const files = event.dataTransfer.files;
          if (!bridge || files.length !== 1) { setNativeFolderError('Drop one folder from Finder to choose it.'); return; }
          void selectNativeFolder({ path: bridge.pathForFile(files[0]) });
        } : undefined}
        onSubmit={(event) => {
          void submitDraft(event);
        }}
      >
        {presentation === 'woven' && attachments.length ? <ul className="attachment-chip-list">{attachments.map(item => <li key={item.path} className="attachment-chip" title={item.path}>
          <span>{item.displayName}</span><button type="button" aria-label={`Remove ${item.displayName}`} disabled={isRunning} onClick={() => setAttachments(current => current.filter(entry => entry.path !== item.path))}>×</button>
        </li>)}</ul> : null}
        {presentation === 'woven' && selectedMethods.length ? <ul className="method-chip-list" aria-label="Methods for next turn">{selectedMethods.map(method => <li key={`${method.sourceRootId}:${method.kind}:${method.name}`} className="method-chip" title={`${method.source} · ${method.kind}`}>
          <span>{method.name}</span><small>{method.source}</small><button type="button" aria-label={`Remove ${method.name}`} disabled={isRunning} onClick={() => onSelectedMethodsChange(selectedMethods.filter(item => item !== method))}>×</button>
        </li>)}</ul> : null}
        <div className={presentation === 'woven' ? 'chat-composer-line' : 'chat-composer-line--legacy'}>
        {presentation === 'woven' ? (        <textarea
          ref={composerRef}
          rows={1}
          aria-label="Chat input"
          data-chat-input="primary"
          value={draft}
          disabled={!projectRoot || steerPending || folderSelectionPending || !draftIdentityReady}
          onKeyDown={event => {
            if (event.key === 'Enter' && !event.shiftKey && !event.nativeEvent.isComposing) {
              event.preventDefault(); event.currentTarget.form?.requestSubmit();
            }
          }}
          onCompositionEnd={event => {
            setDraft(event.currentTarget.value);
            onDraftCaptured?.();
          }}
          onChange={(event) => {
            setDraft(event.target.value);
            if (!(event.nativeEvent as InputEvent | undefined)?.isComposing) onDraftCaptured?.();
            if (runtimeError) {
              setRuntimeError(null);
            }
          }}
          placeholder={
            projectRoot ? presentation === 'woven' ? `Message ${personaLabel}…` : `Send prompt as ${activePersona}...` : presentation === 'woven' ? 'Choose a folder first…' : 'Select a Working Root first...'
          }
        />) : (        <input
          aria-label="Chat input"
          data-chat-input="primary"
          value={draft}
          disabled={!projectRoot || steerPending}
          onChange={(event) => {
            setDraft(event.target.value);
            if (runtimeError) {
              setRuntimeError(null);
            }
          }}
          placeholder={
            projectRoot ? presentation === 'woven' ? `Message ${personaLabel}…` : `Send prompt as ${activePersona}...` : presentation === 'woven' ? 'Choose a folder first…' : 'Select a Working Root first...'
          }
        />)}
        {presentation === 'woven' ? <button type="button" aria-label="Attach files" title="Attach files" disabled={!projectRoot || isRunning || folderSelectionPending || !draftIdentityReady || attachmentPickPending} onClick={() => void pickAttachments()}>⊕</button> : null}
        {presentation === 'woven' ? <button type="button" className="chat-workflow-button" aria-label="Choose a workflow" title="Open workflows" disabled={!projectRoot || isRunning || folderSelectionPending || !draftIdentityReady} onClick={onOpenMethods}>Workflows</button> : null}
        <button
          type="submit"
          className={isRunning ? 'chat-submit-update' : undefined}
          aria-label={isRunning ? 'Update running turn' : 'Send'}
          disabled={!projectRoot || steerPending || unknownSteerDraft || (isRunning && (!currentRuntimeTurnId || !draft.trim() || stopRequested || reconnectAttempt !== null)) || folderSelectionPending || !draftIdentityReady || !isSupportedOperatorMode(operatorMode) || (!draft.trim() && attachments.length === 0)}
        >
          {isRunning ? (steerPending ? 'Sending…' : 'Update') : presentation === 'woven' ? '↑' : 'Send'}
        </button>
        {presentation !== 'woven' || isRunning ? (        <button
          type="button"
          className="button-muted"
          onClick={() => {
            void interruptTurn();
          }}
          disabled={!isRunning || !activeSession}
        >
          Stop
        </button>) : null}
        </div>
        {steerReceipt && steerReceipt.sessionId === activeSession?.sessionId ? <p role="status" className="chat-steer-receipt">
          {steerReceipt.status === 'accepted' ? 'Update received by the running turn.' : steerReceipt.status === 'rejected' ? 'Update rejected. Your draft is preserved.' : steerReceipt.status === 'submitted' ? 'Awaiting update receipt…' : 'Update delivery unconfirmed. Your draft is preserved; it will not be resent automatically.'}
          {steerReceipt.message ? ` ${steerReceipt.message}` : ''}
        </p> : null}
      </form>
      {presentation === 'woven' ? <div className="chat-context" role="group" aria-label="Chat context">
        <span>{conversationBinding ? 'Working in' : 'Start in'}</span>
        <FolderSelect knownRoots={knownRoots} root={conversationBinding?.projectRoot ?? projectRoot} locked={Boolean(conversationBinding)} disabled={isRunning || folderSelectionPending} onPendingChange={onFolderSelectionPending} />
        <span aria-hidden="true">·</span><PersonaPicker compact disabled={isRunning} />
        <span aria-hidden="true">·</span><label className="chat-mode-selector"><span className="visually-hidden">Interaction mode</span><select aria-label="Interaction mode" value={interactionMode} disabled={isRunning} onChange={event => setInteractionMode(event.target.value as InteractionMode)}>
          <option value="chat">Chat</option><option value="native-plan" disabled={Boolean(activeSession) && !nativePlanAvailable(planCapability)} title={activeSession && planCapability.status === 'unavailable' ? `Plan Mode unavailable: ${planCapability.reason}` : undefined}>Plan Mode</option>
        </select></label>
        {/* Permissions are the Codex policy selection; model and reasoning are per-turn catalog choices. All three are distinct from Plan Mode (interaction). */}
        <span aria-hidden="true">·</span><label className="chat-mode-selector"><span className="visually-hidden">Permissions</span><select aria-label="Permissions"
          value={isSupportedOperatorMode(operatorMode) ? operatorMode : ''}
          disabled={isRunning}
          title={OPERATOR_MODES.find(option => option.value === operatorMode)?.description ?? PERMISSION_SELECTOR_HELP}
          onChange={event => { if (isSupportedOperatorMode(event.target.value)) setOperatorMode(event.target.value); }}>
          {isSupportedOperatorMode(operatorMode) ? null : <option value="">Permissions</option>}
          {OPERATOR_MODES.map(option => <option key={option.value} value={option.value} title={option.description}>{option.label}</option>)}
        </select></label>
        <span aria-hidden="true">·</span><label className="chat-mode-selector"><span className="visually-hidden">Model</span><select aria-label="Model"
          value={nextTurnSelection?.model ?? recordedSelection?.model ?? ''}
          disabled={!modelCatalog || isRunning}
          title={modelCatalog ? MODEL_SELECTOR_HELP : modelSelectorTitle}
          onChange={event => {
            const entry = modelCatalog?.models.find(model => model.model === event.target.value);
            if (entry) setModelChoice({ model: entry.model, reasoningEffort: entry.defaultReasoningEffort });
          }}>
          {modelCatalog
            ? modelCatalog.models.map(entry => <option key={entry.model} value={entry.model}>{entry.model}</option>)
            : <option value={recordedSelection?.model ?? ''}>{recordedSelection?.model ?? 'Model'}</option>}
        </select></label>
        <span aria-hidden="true">·</span><label className="chat-mode-selector"><span className="visually-hidden">Reasoning</span><select aria-label="Reasoning"
          value={nextTurnSelection?.reasoningEffort ?? recordedSelection?.reasoningEffort ?? ''}
          disabled={!modelCatalog || isRunning}
          title={modelCatalog ? REASONING_SELECTOR_HELP : modelSelectorTitle}
          onChange={event => {
            const entry = nextTurnSelection && modelCatalog?.models.find(model => model.model === nextTurnSelection.model);
            if (entry && entry.supportedReasoningEfforts.includes(event.target.value)) setModelChoice({ model: entry.model, reasoningEffort: event.target.value });
          }}>
          {modelCatalog && nextTurnSelection
            ? (modelCatalog.models.find(entry => entry.model === nextTurnSelection.model)?.supportedReasoningEfforts ?? []).map(effort => <option key={effort} value={effort}>{effort}</option>)
            : <option value={recordedSelection?.reasoningEffort ?? ''}>{recordedSelection?.reasoningEffort ?? 'Reasoning'}</option>}
        </select></label>
        {folderSyncError ? <p role="alert">{folderSyncError}</p> : null}
        {nativeFolderError ? <p role="alert">{nativeFolderError}</p> : null}
      </div> : null}

      <FilePicker
        open={pickerOpen}
        projectRoot={projectRoot ?? ''}
        existingPaths={attachments.map((item) => item.path)}
        onClose={() => {
          setPickerOpen(false);
        }}
        onAddAttachments={(incoming) => {
          setAttachments((existing) => mergeAttachments(existing, incoming));
        }}
      />
    </aside>
  );
}
