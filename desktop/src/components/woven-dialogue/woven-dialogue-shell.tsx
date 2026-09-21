'use client';

import type { WorkflowFeedbackRequest } from '../../lib/harness/workflow-feedback';

import { usePathname, useRouter, useSearchParams } from 'next/navigation';
import {
  default as React,
  Suspense,
  useCallback,
  useEffect,
  useMemo,
  useRef,
  useState,
  type CSSProperties,
  type PointerEvent
} from 'react';
import type { SessionRecord } from '@chirality/runtime-contracts/types';
import { listHarnessSessions, harnessApiErrorMessage } from '../../lib/harness/client';
import type { SelectedSessionReplayState } from '../../lib/woven-dialogue/contracts';
import { buildRecordedAgentHierarchy } from '../../lib/woven-dialogue/recorded-agent-hierarchy';
import { createChatReplayReader, deriveChatTitle, visibleActiveChatSessions, type ChatReplayReader } from '../../lib/woven-dialogue/chat-organization';
import { guardRecordedSessionSelection } from '../../lib/woven-dialogue/guarded-session-selection';
import {
  createSelectedSessionReplayLoader,
  canContinueRecordedConversation,
  type SelectedSessionReplayLoader
} from '../../lib/woven-dialogue/selected-session-replay';
import {
  clearProjectScopedWovenWorkspaceState,
  createDefaultWovenWorkspaceState,
  indexWovenChats,
  readWovenWorkspaceStateFromStorage,
  recordWovenSessionSurface,
  writeWovenWorkspaceStateToStorage,
  type WovenWorkspaceState
} from '../../lib/woven-dialogue/woven-workspace-state';
import type { TurnPhase } from '../../lib/shell/turn-phase';
import { publishLiveTurnPhase } from '../../lib/shell/live-work-store';
import { useHarnessStreaming, useHarnessEvents } from '../workspace/harness-events-provider';
import { useWorkspace } from '../workspace/workspace-provider';
import { ChatPanel, type ResumeConversationRequest } from '../shell/chat-panel';
import { useRuntimeEpoch } from '../shell/runtime-connectivity-provider';
import { ShellFrame } from '../shell/shell-frame';
import { ActivityStrip } from './activity-shelf';
import { CoordinationPanel } from './coordination-panel';
import { RightPanel } from './right-panel';
import { useConversationFileCatalog } from '../../lib/workspace/use-conversation-file-catalog';
import { DialogueViewport } from './dialogue-viewport';
import { ChatAttentionDialog, useChatAttention } from './chat-attention';
import { useLiveSessionRequests } from '../shell/request-card';
import { Navigator, type NavigatorFolderNotice, type WovenSurface } from './navigator';
import { SelectedSessionReplayLens } from './selected-session-replay-lens';
import type { QualifiedMethodReference } from '../../lib/harness/method-selection-client';
import type { NativePlanPanelModel } from '../shell/native-plan-panel';
import { resolveRightPanelView } from '../../lib/woven-dialogue/woven-workspace-state';

type WovenDialogueShellProps = {
  defaultSurface: WovenSurface;
};

type ResizeTarget = 'navigator' | 'coordination';

function selectedReplayId(state: SelectedSessionReplayState): string | undefined {
  if (state.status === 'READY') {
    return state.projection.selectedSessionId;
  }
  if (state.status === 'LOADING' || state.status === 'UNAVAILABLE') {
    return state.selectedSessionId;
  }
  return undefined;
}

function clamp(value: number, minimum: number, maximum: number): number {
  return Math.max(minimum, Math.min(maximum, value));
}

export function WovenDialogueShell(_props: WovenDialogueShellProps): JSX.Element {
  const pathname = usePathname();
  const router = useRouter();
  const searchParams = useSearchParams();
  const workspace = useWorkspace();
  const { projectRoot } = workspace;
  const streaming = useHarnessStreaming();
  const { events } = useHarnessEvents();
  const [binding, setBinding] = useState<{ root: string | null; locked: boolean }>({ root: null, locked: false });
  const [folderSelectionPending, setFolderSelectionPending] = useState(false);
  const [newChatRequest, setNewChatRequest] = useState(0);
  const [focusNavigatorSearchRequest, setFocusNavigatorSearchRequest] = useState(0);
  const [navigatorModalOpen, setNavigatorModalOpen] = useState(false);
  const runtimeEpoch = useRuntimeEpoch();
  const { paths: currentFileCatalog, acceptCatalog: handleFileCatalog } = useConversationFileCatalog(projectRoot, streaming, runtimeEpoch);
  const [primarySessionId, setPrimarySessionId] = useState<string>();
  const [selectedMethods, setSelectedMethods] = useState<QualifiedMethodReference[]>([]);
  const [pendingResume, setPendingResume] = useState<ResumeConversationRequest>();
  const resumeSequence = useRef(0);
  const [workspaceState, setWorkspaceState] = useState<WovenWorkspaceState>(
    createDefaultWovenWorkspaceState
  );
  const [availableWidth, setAvailableWidth] = useState(1440);
  const workspaceRef = useRef<HTMLElement | null>(null);
  const [coordinationView, setCoordinationView] = useState<'session' | 'agents'>('agents');
  const rightView = resolveRightPanelView(workspaceState.rightPanelView);
  const [planPanel, setPlanPanel] = useState<NativePlanPanelModel | null>(null);
  const [planFocusRevision, setPlanFocusRevision] = useState<{ revision: number; sequence: number } | undefined>(undefined);
  const [turnPhase, setTurnPhase] = useState<TurnPhase>('idle');
  // Surfaces outside the shell (the update controls) read whether work is live here.
  useEffect(() => { publishLiveTurnPhase(turnPhase); return () => publishLiveTurnPhase('idle'); }, [turnPhase]);
  // Chats recorded in other folders are opened by switching to that folder
  // first and resuming once its sessions are listed. `expectedRoot` null means
  // "whichever folder the human locates".
  const pendingFolderChat = useRef<{ sessionId: string; expectedRoot: string | null; awaitingNewChat?: boolean } | null>(null);
  const [folderNotices, setFolderNotices] = useState<Record<string, NavigatorFolderNotice>>({});
  const [failedFolder, setFailedFolder] = useState<string | null>(null);
  const restoredLastChat = useRef(false);
  const lastPrimaryRef = useRef<string | undefined>(undefined);
  const widthKey = rightView === 'files' && workspaceState.openDocumentPath ? 'document' : rightView === 'agents' && coordinationView === 'session' ? 'session' : rightView;
  const rightWidth = workspaceState.rightPanelWidths?.[widthKey] ?? (widthKey === 'files' ? 300 : widthKey === 'agents' ? 360 : 480);
  const maximumRightWidth = Math.max(280, Math.min(Math.round(availableWidth * 0.6 / 8) * 8, availableWidth - (workspaceState.navigatorCollapsed ? 56 : clamp(workspaceState.navigatorWidth, 220, 360)) - 444));
  const [stateHydrated, setStateHydrated] = useState(false);
  useEffect(() => {
    if (!projectRoot || !stateHydrated) return;
    setWorkspaceState(current => ({ ...current, knownRoots: [
      { path: projectRoot, lastUsedAt: new Date().toISOString() },
      ...(current.knownRoots ?? []).filter(root => root.path !== projectRoot)
    ].slice(0, 50) }));
  }, [projectRoot, stateHydrated]);
  const [attentionSessionId, setAttentionSessionId] = useState<string | null>(null);
  const [sessions, setSessions] = useState<SessionRecord[]>([]);
  const [referenceDay, setReferenceDay] = useState('1970-01-01');
  const [sessionsLoading, setSessionsLoading] = useState(false);
  // The folder the current `sessions` list was read for; a folder change
  // leaves the previous list on screen until the new one arrives.
  const [sessionsRoot, setSessionsRoot] = useState<string | null>(null);
  const [otherRunningSessions, setOtherRunningSessions] = useState<SessionRecord[]>([]);
  const primaryRequests = useLiveSessionRequests(primarySessionId ?? null, streaming);
  const backgroundRunningSessionIds = sessionsRoot === projectRoot ? [...sessions, ...otherRunningSessions].filter(session => session.sessionId !== primarySessionId && 'status' in session && session.status === 'running').map(session => session.sessionId) : [];
  const attention = useChatAttention([...new Set(backgroundRunningSessionIds)]);
  const primaryNeedsAnswer = primaryRequests.length > 0;
  const needsAnswerSessionIds = [...Object.keys(attention.rows), ...(primaryNeedsAnswer && primarySessionId ? [primarySessionId] : [])];

  // Keep read state outside the collapsible RightPanel.
  const [readPlanRevisions, setReadPlanRevisions] = useState<Record<string, number>>({});
  const markPlanRead = useCallback((sessionId: string, revision: number) => {
    setReadPlanRevisions(current => (current[sessionId] ?? 0) >= revision ? current : { ...current, [sessionId]: revision });
  }, []);
  const workflowFeedbackSequence = useRef(0);
  const [workflowFeedback, setWorkflowFeedback] = useState<WorkflowFeedbackRequest>();
  const [sessionsError, setSessionsError] = useState<string | null>(null);
  const [sessionRefreshToken, setSessionRefreshToken] = useState(0);
  const directHistorySelection = useRef<string>();
  const replayLoaderRef = useRef<SelectedSessionReplayLoader>();
  const titleReaderRef = useRef<ChatReplayReader>();
  const previousProjectRootRef = useRef(projectRoot);
  const [replayState, setReplayState] = useState<SelectedSessionReplayState>({
    status: 'IDLE'
  });
  const dialogueInputRef = useRef<HTMLInputElement | HTMLTextAreaElement | null>(null);
  const resizeRef = useRef<{
    target: ResizeTarget;
    startX: number;
    startY: number;
    startValue: number;
  } | null>(null);

  if (!replayLoaderRef.current) {
    replayLoaderRef.current = createSelectedSessionReplayLoader();
  }

  useEffect(() => {
    const loader = replayLoaderRef.current as SelectedSessionReplayLoader;
    const unsubscribe = loader.subscribe(setReplayState);
    return () => {
      unsubscribe();
      loader.dispose();
    };
  }, []);
  useEffect(() => {
    const reader = createChatReplayReader(); titleReaderRef.current = reader;
    return () => { if (titleReaderRef.current === reader) titleReaderRef.current = undefined; reader.dispose(); };
  }, []);

  useEffect(() => {
    if (typeof window === 'undefined' || typeof window.addEventListener !== 'function') return;
    const keydown = (event: KeyboardEvent): void => {
      if (!(event.metaKey || event.ctrlKey) || event.key.toLocaleLowerCase() !== 'k') return;
      event.preventDefault();
      if (navigatorModalOpen || attentionSessionId) return;
      setWorkspaceState(current => ({ ...current, navigatorCollapsed: false }));
      setFocusNavigatorSearchRequest(value => value + 1);
    };
    window.addEventListener('keydown', keydown); return () => window.removeEventListener('keydown', keydown);
  }, [navigatorModalOpen, attentionSessionId]);

  useEffect(() => {
    if (typeof window === 'undefined') {
      return;
    }
    const stored = readWovenWorkspaceStateFromStorage(window.localStorage);
    setWorkspaceState(stored);
    setReferenceDay(new Date().toISOString().slice(0, 10));
    // Retired Work preferences fall back to the recorded Agents projection.
    setCoordinationView('agents');
    setStateHydrated(true);
  }, []);

  useEffect(() => {
    if (!stateHydrated || typeof window === 'undefined') {
      return;
    }
    writeWovenWorkspaceStateToStorage(window.localStorage, workspaceState);
  }, [stateHydrated, workspaceState]);

  useEffect(() => {
    const element = workspaceRef.current;
    if (!element || typeof ResizeObserver === 'undefined') return;
    const observer = new ResizeObserver(entries => {
      const width = entries[0]?.contentRect.width;
      if (width) setAvailableWidth(width);
    });
    observer.observe(element);
    return () => observer.disconnect();
  }, []);

  // The recorded session list carries no surface field, so the shell tags the
  // dialogue surface when a session is first observed. Local
  // annotation only (no project truth); first attribution wins, so this is a
  // no-op — same state reference — for every session already tagged.
  useEffect(() => {
    if (!stateHydrated || !primarySessionId) {
      return;
    }
    setWorkspaceState((current) =>
      recordWovenSessionSurface(current, primarySessionId, 'dialogue')
    );
  }, [primarySessionId, stateHydrated]);

  useEffect(() => {
    replayLoaderRef.current?.cancel();
    setPendingResume(undefined);
    setSessions([]);
    setAttentionSessionId(null);
    setSessionsError(null);
    if (
      previousProjectRootRef.current &&
      previousProjectRootRef.current !== projectRoot
    ) {
      setWorkspaceState(clearProjectScopedWovenWorkspaceState);
    }
    previousProjectRootRef.current = projectRoot;
  }, [projectRoot]);

  useEffect(() => {
    if (primarySessionId) {
      setSessionRefreshToken((token) => token + 1);
    }
  }, [primarySessionId, streaming]);

  useEffect(() => {
    if (!projectRoot) {
      setSessions([]);
      setSessionsRoot(null);
      setSessionsLoading(false);
      return;
    }

    let cancelled = false;
    setSessionsLoading(true);
    setSessionsError(null);
    listHarnessSessions(projectRoot)
      .then((records) => {
        if (!cancelled) {
          setSessions(records);
          setSessionsRoot(projectRoot);
          setWorkspaceState(current => indexWovenChats(current, projectRoot, records));
        }
      })
      .catch((error) => {
        if (!cancelled) {
          setSessionsError(harnessApiErrorMessage(error));
        }
      })
      .finally(() => {
        if (!cancelled) {
          setSessionsLoading(false);
        }
      });

    return () => {
      cancelled = true;
    };
    // `runtimeEpoch` re-lists after a reconnect. The Navigator's flat list and
    // the Coordination panel's hierarchy are both projections of `sessions`, so
    // one re-list repairs all three surfaces at once.
  }, [projectRoot, sessionRefreshToken, runtimeEpoch]);

  useEffect(() => {
    if (!projectRoot) return;
    let cancelled = false;
    let pending = false;
    const refresh = async () => {
      if (pending) return;
      pending = true;
      try {
        const records = await listHarnessSessions(projectRoot);
        if (!cancelled) { setSessions(records); setSessionsRoot(projectRoot); }
      } catch { /* Preserve the other chats when a refresh is temporarily unavailable. */ }
      finally { pending = false; }
    };
    const timer = window.setInterval(() => void refresh(), 5000);
    window.addEventListener('focus', refresh);
    return () => { cancelled = true; window.clearInterval(timer); window.removeEventListener('focus', refresh); };
  }, [projectRoot, runtimeEpoch]);

  useEffect(() => {
    const reader = titleReaderRef.current as ChatReplayReader;
    const requestedRoot = projectRoot;
    const visibleSessions = visibleActiveChatSessions(sessions, workspaceState.chatArchived ?? [], workspaceState.chatDeleted ?? []);
    const sessionById = new Map(visibleSessions.map(session => [session.sessionId, session]));
    if (visibleSessions.length === 0) { reader.cancel(); return; }
    let current = true;
    void reader.loadFirstOperatorMessages(visibleSessions, new Date().toISOString()).then(messages => {
      if (!current || requestedRoot !== previousProjectRootRef.current) return;
      setWorkspaceState(state => {
        const titles = { ...(state.chatTitles ?? {}) };
        let changed = false;
        for (const [sessionId, prompt] of Object.entries(messages)) {
          const session = sessionById.get(sessionId);
          if (!session || Object.hasOwn(titles, sessionId)) continue;
          titles[sessionId] = deriveChatTitle({ firstOperatorMessage: prompt, persona: session.persona, sessionId });
          changed = true;
        }
        return changed ? { ...state, chatTitles: titles } : state;
      });
    }).catch(() => {});
    return () => { current = false; reader.cancel(); };
  }, [sessions, projectRoot, runtimeEpoch, workspaceState.chatArchived, workspaceState.chatDeleted]);

  // Read at reconnect time only, so the recovery effect below can depend on the
  // epoch alone: depending on the replay state itself would re-arm the effect
  // with every load it performs.
  const replayStateRef = useRef(replayState);
  replayStateRef.current = replayState;
  const sessionsRef = useRef(sessions);
  sessionsRef.current = sessions;

  // A replay lens left showing UNAVAILABLE is the same stale-error class as the
  // panes above, and it is still on screen — the lens is only hidden when the
  // state is IDLE. Reload it once, straight through the loader: the selection
  // guard is for operator clicks, and it answers UNCHANGED for a re-request of
  // the session already selected.
  useEffect(() => {
    if (runtimeEpoch === 0) {
      return;
    }
    const current = replayStateRef.current;
    if (current.status !== 'UNAVAILABLE') {
      return;
    }
    void replayLoaderRef.current?.load(current.selectedSessionId, {
      observedAt: new Date().toISOString(),
      availableSessionIds: new Set(
        sessionsRef.current.map((session) => session.sessionId)
      )
    });
  }, [runtimeEpoch]);

  const hierarchy = useMemo(() => {
    const observedAt = new Date().toISOString();
    return buildRecordedAgentHierarchy(
      sessions.map((session) => {
        const source = session as SessionRecord & Record<string, unknown>;
        return {
          ...source,
          sourceReference: `session:${session.sessionId}`,
          observedAt,
          currency: 'UNKNOWN',
          status: source.status,
          role: source.role
        };
      })
    );
  }, [sessions]);

  const legacyHref = useMemo(() => {
    const params = new URLSearchParams(searchParams.toString());
    params.set('legacy', '1');
    return `${pathname}?${params.toString()}`;
  }, [pathname, searchParams]);

  const updateWorkspaceState = useCallback(
    (patch: Partial<WovenWorkspaceState>): void => {
      setWorkspaceState((current) => ({ ...current, ...patch }));
    },
    []
  );

  const restoreExpanded = useCallback(() => {
    setWorkspaceState(current => {
      if (!current.rightPanelExpanded) return current;
      const previous = current.preExpandState;
      return { ...current, rightPanelExpanded: false, preExpandState: null,
        navigatorCollapsed: previous?.leftCollapsed ?? current.navigatorCollapsed,
        rightPanelWidths: { ...current.rightPanelWidths, [widthKey]: previous?.rightWidth ?? rightWidth }
      };
    });
  }, [widthKey, rightWidth]);

  const returnToPrimaryDialogue = useCallback((): void => {
    directHistorySelection.current = undefined;
    setPendingResume(undefined);
    replayLoaderRef.current?.cancel();
    updateWorkspaceState({ selectedReplaySessionId: null });
    window.requestAnimationFrame(() => {
      const input = document.querySelector<HTMLInputElement | HTMLTextAreaElement>('[data-chat-input="primary"]');
      dialogueInputRef.current = input;
      input?.focus();
    });
  }, [updateWorkspaceState]);

  const continueRecordedConversation = useCallback((projection: Extract<SelectedSessionReplayState, { status: 'READY' }>['projection']): void => {
    const continuation = projection.session?.continuation;
    if (!continuation || !canContinueRecordedConversation(projection, projectRoot, streaming)) return;
    const request = { requestId: ++resumeSequence.current, projection };
    const currentRole = searchParams.get('agent');
    setPendingResume(request);
    if (currentRole !== continuation.roleId) {
      const params = new URLSearchParams(searchParams.toString());
      params.set('agent', continuation.roleId);
      router.replace(`${pathname}?${params.toString()}`);
    }
  }, [pathname, projectRoot, router, searchParams, streaming]);

  useEffect(() => {
    if (!directHistorySelection.current || directHistorySelection.current !== selectedReplayId(replayState)) return;
    if (replayState.status !== 'READY' && replayState.status !== 'UNAVAILABLE') return;
    directHistorySelection.current = undefined;
    if (replayState.status === 'READY' && canContinueRecordedConversation(replayState.projection, projectRoot, streaming)) {
      continueRecordedConversation(replayState.projection);
    } else {
      // An incompatible or unavailable recording still needs its inspection/retry surface.
      restoreExpanded();
      updateWorkspaceState({ rightPanelView: 'agents', coordinationCollapsed: false });
      setCoordinationView('session');
    }
  }, [replayState, projectRoot, streaming, continueRecordedConversation, restoreExpanded, updateWorkspaceState]);

  // Chats recorded in other folders come from the local index so every folder's
  // chats share one navigator; the live listing replaces the index for the
  // selected folder as soon as it arrives.
  const navigatorSessions = useMemo<SessionRecord[]>(() => {
    const visible = [...new Map([...otherRunningSessions, ...sessions].map(session => [session.sessionId, session])).values()];
    const live = new Set(visible.map(session => session.sessionId));
    const indexed = Object.entries(workspaceState.chatIndex ?? {})
      .filter(([sessionId, entry]) => !live.has(sessionId) && entry.projectRoot !== projectRoot)
      .map(([sessionId, entry]) => ({ sessionId, projectRoot: entry.projectRoot, persona: entry.persona ?? '', mode: '', createdAt: entry.createdAt, updatedAt: entry.updatedAt }));
    return [...visible, ...indexed];
  }, [sessions, otherRunningSessions, workspaceState.chatIndex, projectRoot]);
  const knownRootPaths = useMemo(() => (workspaceState.knownRoots ?? []).map(root => root.path), [workspaceState.knownRoots]);
  const attentionRootsKey = JSON.stringify(knownRootPaths.filter(root => root !== projectRoot));
  useEffect(() => {
    const roots = JSON.parse(attentionRootsKey) as string[];
    setOtherRunningSessions([]);
    if (!roots.length) return;
    let cancelled = false;
    let pending = false;
    let cursor = 0;
    const refresh = async () => {
      if (pending) return;
      const root = roots[cursor++ % roots.length];
      pending = true;
      try {
        const records = await listHarnessSessions(root);
        if (!cancelled) setOtherRunningSessions(current => [...current.filter(session => session.projectRoot !== root), ...records.filter(session => 'status' in session && session.status === 'running')]);
      } catch { /* A missing folder does not clear another folder's live attention. */ }
      finally { pending = false; }
    };
    void refresh();
    const timer = window.setInterval(() => void refresh(), 5000);
    return () => { cancelled = true; window.clearInterval(timer); };
  }, [attentionRootsKey, runtimeEpoch]);


  const switchToFolderChat = useCallback(async (sessionId: string, folderPath: string): Promise<void> => {
    if (typeof workspace.applyProjectRoot !== 'function') return;
    pendingFolderChat.current = { sessionId, expectedRoot: folderPath };
    setFailedFolder(null);
    setFolderNotices(current => ({ ...current, [folderPath]: { kind: 'indexed', message: 'Opening this chat: switching to its folder…' } }));
    setFolderSelectionPending(true);
    let applied = false;
    try { applied = await workspace.applyProjectRoot(folderPath); }
    finally { setFolderSelectionPending(false); }
    if (applied) return;
    pendingFolderChat.current = null;
    setFailedFolder(folderPath);
    setFolderNotices(current => ({ ...current, [folderPath]: { kind: 'unavailable', message: 'This folder could not be opened. Its chats stay recorded and are never moved to another folder. Locate the folder if it moved, or forget it.' } }));
  }, [workspace]);

  // Opening a chat from another folder first closes the chat open in the
  // panel, through the same New chat path (its unsent-draft confirmation
  // included), so the folder never switches under a bound chat. The switch
  // proceeds once the panel reports the chat closed; a declined confirmation
  // leaves everything as it was.
  const openChatInFolder = useCallback(async (sessionId: string, folderPath: string): Promise<void> => {
    if (streaming || folderSelectionPending || typeof workspace.applyProjectRoot !== 'function') return;
    if (!binding.locked) { await switchToFolderChat(sessionId, folderPath); return; }
    pendingFolderChat.current = { sessionId, expectedRoot: folderPath, awaitingNewChat: true };
    setFolderNotices(current => ({ ...current, [folderPath]: { kind: 'indexed', message: 'Opening this chat: closing the current chat first…' } }));
    setNewChatRequest(value => value + 1);
  }, [streaming, folderSelectionPending, workspace, binding.locked, switchToFolderChat]);
  const handleNewChatSettled = useCallback((started: boolean): void => {
    const pending = pendingFolderChat.current;
    if (!pending?.awaitingNewChat) return;
    const folderPath = pending.expectedRoot ?? '';
    pendingFolderChat.current = null;
    if (!started) { setFolderNotices(current => { const next = { ...current }; delete next[folderPath]; return next; }); return; }
    void switchToFolderChat(pending.sessionId, folderPath);
  }, [switchToFolderChat]);

  // The workspace reports why a folder failed after the failed apply; attach
  // that reason to the notice so the human sees the actual problem.
  useEffect(() => {
    if (!failedFolder || !workspace.errorMessage) return;
    const reason = workspace.errorMessage;
    setFolderNotices(current => current[failedFolder]?.kind === 'unavailable' && !current[failedFolder].message.includes(reason)
      ? { ...current, [failedFolder]: { kind: 'unavailable', message: `This folder could not be opened (${reason}). Its chats stay recorded and are never moved to another folder. Locate the folder if it moved, or forget it.` } }
      : current);
  }, [failedFolder, workspace.errorMessage]);

  const locateFolder = useCallback(async (folderPath: string): Promise<void> => {
    if (streaming || folderSelectionPending || typeof workspace.chooseProjectRoot !== 'function') return;
    const pending = pendingFolderChat.current;
    if (pending) pendingFolderChat.current = { sessionId: pending.sessionId, expectedRoot: null };
    setFolderSelectionPending(true);
    let applied = false;
    try { applied = await workspace.chooseProjectRoot(); }
    finally { setFolderSelectionPending(false); }
    if (applied) setFolderNotices(current => { const next = { ...current }; delete next[folderPath]; return next; });
  }, [streaming, folderSelectionPending, workspace]);

  const forgetFolder = useCallback((folderPath: string): void => {
    if (pendingFolderChat.current && (workspaceState.chatIndex ?? {})[pendingFolderChat.current.sessionId]?.projectRoot === folderPath) pendingFolderChat.current = null;
    setFolderNotices(current => { const next = { ...current }; delete next[folderPath]; return next; });
    setFailedFolder(current => current === folderPath ? null : current);
    setWorkspaceState(current => ({ ...current,
      knownRoots: (current.knownRoots ?? []).filter(root => root.path !== folderPath),
      chatIndex: Object.fromEntries(Object.entries(current.chatIndex ?? {}).filter(([, entry]) => entry.projectRoot !== folderPath)),
      foldersCollapsed: (current.foldersCollapsed ?? []).filter(path => path !== folderPath)
    }));
  }, [workspaceState.chatIndex]);

  const loadReplay = useCallback(
    (sessionId: string, inspect = false): void => {
      const indexed = (workspaceState.chatIndex ?? {})[sessionId];
      const listed = sessions.some(session => session.sessionId === sessionId);
      if (!listed && indexed && indexed.projectRoot !== projectRoot) {
        // Recorded in another folder: restore that folder, then open the chat there.
        if (!inspect) void openChatInFolder(sessionId, indexed.projectRoot);
        return;
      }
      const decision = guardRecordedSessionSelection({
        currentState: replayState,
        requestedSessionId: sessionId,
        primarySessionId,
        recordedSessionIds: sessions.map((session) => session.sessionId),
        liveTurnActive: streaming,
        replayIsolationAvailable: true
      });
      if (decision.outcome === 'RETURN_TO_PRIMARY') {
        returnToPrimaryDialogue();
        return;
      }
      if (decision.outcome === 'UNCHANGED') {
        if (!inspect) return;
        restoreExpanded();
        updateWorkspaceState({ coordinationCollapsed: false, rightPanelView: 'agents' });
        setCoordinationView('session');
        return;
      }
      if (decision.outcome !== 'SELECT_REPLAY') {
        return;
      }

      setPendingResume(undefined);
      directHistorySelection.current = inspect ? undefined : sessionId;
      updateWorkspaceState({ selectedReplaySessionId: sessionId });
      if (inspect) {
        restoreExpanded();
        updateWorkspaceState({ rightPanelView: 'agents', coordinationCollapsed: false });
        setCoordinationView('session');
      }
      void replayLoaderRef.current?.load(sessionId, {
        observedAt: new Date().toISOString(),
        availableSessionIds: new Set(sessions.map((session) => session.sessionId))
      });
    },
    [
      primarySessionId,
      replayState,
      returnToPrimaryDialogue,
      restoreExpanded,
      sessions,
      streaming,
      updateWorkspaceState,
      workspaceState.chatIndex,
      projectRoot,
      openChatInFolder
    ]
  );

  // Once the folder switch lands and its sessions are listed, resume the chat
  // that asked for it; a chat the folder does not list is reported, not guessed.
  useEffect(() => {
    const pending = pendingFolderChat.current;
    if (!pending || pending.awaitingNewChat || sessionsLoading || !projectRoot || sessionsRoot !== projectRoot) return;
    if (pending.expectedRoot !== null && pending.expectedRoot !== projectRoot) return;
    pendingFolderChat.current = null;
    const recordedRoot = (workspaceState.chatIndex ?? {})[pending.sessionId]?.projectRoot ?? pending.expectedRoot ?? projectRoot;
    setFolderNotices(current => { const next = { ...current }; delete next[recordedRoot]; return next; });
    if (sessions.some(session => session.sessionId === pending.sessionId)) {
      loadReplay(pending.sessionId);
    } else if (!sessionsError) {
      setFolderNotices(current => ({ ...current, [recordedRoot]: { kind: 'unavailable', message: `The chat was not found in ${projectRoot}. It stays listed under its recorded folder; locate that folder or forget it.` } }));
    }
    // loadReplay is intentionally read at the time the listing settles.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [sessions, sessionsRoot, sessionsLoading, sessionsError, projectRoot]);

  // The chat open when the window was last used comes back on the next launch,
  // once its folder's sessions confirm it still exists; never while a turn runs.
  useEffect(() => {
    if (!stateHydrated || restoredLastChat.current || streaming) return;
    // A chat already open takes precedence: there is nothing to restore over
    // it, and recording may begin (otherwise the gate would never lift).
    if (primarySessionId) { restoredLastChat.current = true; return; }
    if (sessionsLoading || !projectRoot || sessionsRoot !== projectRoot) return;
    const last = workspaceState.lastActiveChat;
    if (!last) { restoredLastChat.current = true; return; }
    // A last chat from another folder is left alone: the folder for new chats
    // is the one the user chose, and that chat stays reachable in the navigator.
    if (last.projectRoot !== projectRoot) { restoredLastChat.current = true; return; }
    restoredLastChat.current = true;
    if (sessions.some(session => session.sessionId === last.sessionId)) loadReplay(last.sessionId);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [stateHydrated, sessions, sessionsRoot, sessionsLoading, projectRoot, streaming, primarySessionId]);

  useEffect(() => {
    // Nothing is recorded until the launch-time restore has had its chance,
    // so an empty panel at startup never erases the remembered chat.
    if (!stateHydrated || !restoredLastChat.current) return;
    // Only a chat this window actually had open can be forgotten: an empty
    // panel while a restore is still in flight leaves the record alone.
    const hadPrimary = lastPrimaryRef.current !== undefined;
    lastPrimaryRef.current = primarySessionId;
    if (!primarySessionId && !hadPrimary) return;
    setWorkspaceState(current => {
      const next = primarySessionId && projectRoot ? { sessionId: primarySessionId, projectRoot } : null;
      const previous = current.lastActiveChat ?? null;
      if ((previous === null && next === null) || (previous && next && previous.sessionId === next.sessionId && previous.projectRoot === next.projectRoot)) return current;
      return { ...current, lastActiveChat: next };
    });
  }, [primarySessionId, projectRoot, stateHydrated]);

  // Document context follows the chat: opening a chat restores the document it
  // had open; a document opened while a chat is active is remembered for it.
  const documentSessionRef = useRef<string | undefined>(undefined);
  useEffect(() => {
    if (!stateHydrated) return;
    const previous = documentSessionRef.current;
    documentSessionRef.current = primarySessionId;
    if (!primarySessionId || previous === primarySessionId) return;
    const remembered = (workspaceState.chatDocuments ?? {})[primarySessionId];
    if (remembered && remembered !== workspaceState.openDocumentPath) setWorkspaceState(current => ({ ...current, openDocumentPath: remembered, rightPanelView: 'files' }));
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [primarySessionId, stateHydrated]);
  // Only a document opened or closed while this chat is active is recorded for
  // it: a chat without a remembered document does not inherit whatever was on
  // screen when it was opened (review F-2).
  const documentRecordSessionRef = useRef<string | undefined>(undefined);
  useEffect(() => {
    if (!stateHydrated) return;
    // The ref follows the chat through "no chat" too: a document opened while
    // no chat was active is not attributed to the chat resumed afterwards.
    const sessionChanged = documentRecordSessionRef.current !== primarySessionId;
    documentRecordSessionRef.current = primarySessionId;
    if (sessionChanged || !primarySessionId) return;
    const path = workspaceState.openDocumentPath;
    setWorkspaceState(current => {
      const documents = { ...(current.chatDocuments ?? {}) };
      if (path) { if (documents[primarySessionId] === path) return current; documents[primarySessionId] = path; }
      else { if (!(primarySessionId in documents)) return current; delete documents[primarySessionId]; }
      return { ...current, chatDocuments: Object.fromEntries(Object.entries(documents).slice(-500)) };
    });
  }, [workspaceState.openDocumentPath, primarySessionId, stateHydrated]);

  const stacked = availableWidth < 960;
  const leftWidth = workspaceState.navigatorCollapsed ? 56 : Math.min(clamp(workspaceState.navigatorWidth, 220, 360), Math.max(220, availableWidth - 724));
  // Keep the preferred per-tab width in state; announce and resize the width
  // that fits the current layout without replacing it when the viewport changes.
  const effectiveRightWidth = Math.max(280, Math.min(
    workspaceState.rightPanelExpanded ? Math.round(availableWidth * 0.6 / 8) * 8 : rightWidth,
    availableWidth - leftWidth - 444
  ));
  const visibleRightWidth = workspaceState.coordinationCollapsed ? 56 : effectiveRightWidth;

  const beginResize = useCallback(
    (event: PointerEvent<HTMLDivElement>, target: ResizeTarget): void => {
      if (event.button !== 0) {
        return;
      }
      event.preventDefault();
      if (target === 'coordination') restoreExpanded();
      const startValue =
        target === 'navigator'
          ? clamp(workspaceState.navigatorWidth, 220, 360)
          : effectiveRightWidth;
      resizeRef.current = {
        target,
        startX: event.clientX,
        startY: event.clientY,
        startValue
      };
    },
    [workspaceState, effectiveRightWidth, restoreExpanded]
  );

  useEffect(() => {
    const handleMove = (event: globalThis.PointerEvent): void => {
      const resize = resizeRef.current;
      if (!resize) {
        return;
      }
      if (resize.target === 'navigator') {
        updateWorkspaceState({
          navigatorWidth: clamp(resize.startValue + event.clientX - resize.startX, 220, 360),
          navigatorCollapsed: false
        });
      } else if (resize.target === 'coordination') {
        const width = clamp(resize.startValue - event.clientX + resize.startX, 280, maximumRightWidth);
        setWorkspaceState(current => ({ ...current,
          rightPanelWidths: { ...current.rightPanelWidths, [widthKey]: width },
          coordinationWidth: width, coordinationCollapsed: false
        }));

      }
    };
    const handleUp = (): void => {
      resizeRef.current = null;
    };
    window.addEventListener('pointermove', handleMove);
    window.addEventListener('pointerup', handleUp);
    window.addEventListener('pointercancel', handleUp);
    return () => {
      window.removeEventListener('pointermove', handleMove);
      window.removeEventListener('pointerup', handleUp);
      window.removeEventListener('pointercancel', handleUp);
    };
  }, [updateWorkspaceState, widthKey, maximumRightWidth]);

  const resizeByKeyboard = useCallback(
    (target: ResizeTarget, key: string, shift: boolean): void => {
      if (target === 'coordination') restoreExpanded();
      const step = shift ? 40 : 16;
      if (target === 'navigator') {
        const value =
          key === 'Home'
            ? 220
            : key === 'End'
              ? 360
              : clamp(workspaceState.navigatorWidth, 220, 360) + (key === 'ArrowRight' ? step : -step);
        updateWorkspaceState({
          navigatorWidth: clamp(value, 220, 360),
          navigatorCollapsed: key === 'Home'
        });
      } else if (target === 'coordination') {
        const value =
          key === 'Home'
            ? 280
            : key === 'End'
              ? maximumRightWidth
              : effectiveRightWidth + (key === 'ArrowLeft' ? step : -step);
        updateWorkspaceState({
          rightPanelWidths: { ...workspaceState.rightPanelWidths, [widthKey]: clamp(value, 280, maximumRightWidth) },
          coordinationWidth: clamp(value, 280, maximumRightWidth),
          coordinationCollapsed: key === 'Home'
        });

      }
    },
    [updateWorkspaceState, workspaceState, effectiveRightWidth, widthKey, restoreExpanded, maximumRightWidth]
  );

  const toggleExpanded = () => {
    if (workspaceState.rightPanelExpanded) { restoreExpanded(); return; }
    updateWorkspaceState({ rightPanelExpanded: true,
      preExpandState: { rightWidth, leftCollapsed: workspaceState.navigatorCollapsed },
      navigatorCollapsed: true, coordinationCollapsed: false });
  };
  const style = {
    ...(!stacked ? { gridTemplateColumns: `${leftWidth}px 12px minmax(420px, 1fr) 12px ${visibleRightWidth}px` } : {}),
    '--woven-activity-height': '32px'
  } as CSSProperties;
  const replayVisible = replayState.status !== 'IDLE';
  const openContainedFile = useCallback((filePath: string): void => {
    if (!projectRoot) return;
    const prefix = `${projectRoot.replace(/\/$/, '')}/`;
    if (!filePath.startsWith(prefix)) return;
    restoreExpanded();
    updateWorkspaceState({ openDocumentPath: filePath.slice(prefix.length), rightPanelView: 'files', coordinationCollapsed: false });
  }, [projectRoot, restoreExpanded, updateWorkspaceState]);

  return (
    <ShellFrame
      section="CHAT"
      title="Woven Dialogue"
      subtitle="A shared professional workspace where dialogue produces inspectable artifacts and governed work."
      variant="workspace"
      folderLocked={binding.locked || streaming || folderSelectionPending}
      onFolderSelectionPending={setFolderSelectionPending}
      legacyHref={legacyHref}
      onOpenSettings={() => { restoreExpanded(); updateWorkspaceState({ rightPanelView: 'settings', coordinationCollapsed: false }); }}
      renderWorkspaceContent={({ reconnectControl, settingsControl, settingsView }) => (
      <section ref={workspaceRef} className={`woven-workspace woven-t3-workspace${stacked ? ' is-stacked' : ''}`} style={style} data-woven-surface="dialogue">
        <style>{`
          .woven-t3-workspace .woven-right-panel { display:flex; flex-direction:column; min-width:0; height:100%; overflow:auto; }
          .woven-t3-workspace:not(.is-stacked) > .woven-region.is-collapsed > .woven-region-toggle { display:grid; place-items:center; max-width:none; color:var(--ink); font-size:1rem; }
          .woven-t3-workspace > .woven-region.is-collapsed > .woven-region-toggle::after { content:none; }
          .woven-t3-workspace > .woven-region--coordination { display:flex; flex-direction:column; }
          .woven-t3-workspace > .woven-region--coordination:not(.is-collapsed) > .woven-region-toggle { position:static; align-self:flex-end; flex:0 0 auto; margin:0.4rem 0.65rem; }
          .woven-t3-workspace > .woven-region--coordination > .woven-right-panel { height:auto; min-height:0; flex:1 1 0; }
          .woven-t3-workspace .woven-right-panel > .panel { min-height:0; flex:1; }
          .woven-t3-workspace .woven-right-panel nav { overflow-wrap:anywhere; min-width:0; }
          .woven-t3-workspace .tree-item-name { text-align:left; overflow-wrap:anywhere; min-width:0; }
          .woven-t3-workspace .tree-item-name[aria-current=true] { background:var(--ground); font-weight:600; }
          .shell--workspace:has(> .woven-t3-workspace.is-stacked) { height:auto; min-height:100vh; overflow:visible; }
          .woven-t3-workspace.is-stacked { grid-template-columns:minmax(0,1fr); grid-template-rows:minmax(620px,70vh) auto auto 32px; height:auto; overflow:visible; }
          .woven-t3-workspace.is-stacked > .woven-dialogue-region { grid-column:1; grid-row:1; }
          .woven-t3-workspace.is-stacked > .woven-region--navigator { grid-column:1; grid-row:2; max-height:none; }
          .woven-t3-workspace.is-stacked .woven-navigator { height:auto; grid-template-rows:auto minmax(0,1fr) auto; }
          .woven-t3-workspace.is-stacked > .woven-region--coordination { grid-column:1; grid-row:3; height:520px; }
          .woven-t3-workspace.is-stacked > .woven-region.is-collapsed { display:flex; flex-direction:row; align-items:center; gap:0.75rem; height:auto; min-height:56px; max-height:none; padding:0.4rem 0.75rem; }
          .woven-t3-workspace.is-stacked > .woven-region.is-collapsed > .woven-region-toggle { position:static; inset:auto; transform:none; width:auto; max-width:none; min-height:36px; padding:0.4rem 0.65rem; color:var(--ink); flex:0 0 auto; }
          .woven-t3-workspace.is-stacked > .woven-region.is-collapsed > .woven-region-toggle::after { content:none; }
          .woven-t3-workspace.is-stacked > .woven-region.is-collapsed > .woven-collapsed-label { position:static; writing-mode:horizontal-tb; transform:none; min-width:0; overflow-wrap:anywhere; }
          .woven-t3-workspace.is-stacked > .woven-resize-handle--vertical { display:none; }
          .woven-t3-workspace.is-stacked > .woven-resize-handle--horizontal { grid-column:1; grid-row:4; }
          .woven-t3-workspace.is-stacked > .woven-activity-strip { grid-column:1; grid-row:4; }
        `}</style>
        <main className="woven-dialogue-region" aria-label="Primary Dialogue">
          <DialogueViewport
            primaryDialogue={
              <>
                {replayVisible && !streaming ? <p role="status">Opening recorded chat. The current composer is paused until you open this chat or return.</p> : null}
                <fieldset disabled={replayVisible && !streaming} style={{ border: 0, padding: 0, margin: 0, minWidth: 0, minHeight: 0, display: 'contents' }}>
                <Suspense fallback={<p className="panel-empty">Loading primary dialogue…</p>}>
                  <ChatPanel workflowFeedback={workflowFeedback} onWorkflowFeedbackHandled={() => setWorkflowFeedback(undefined)} presentation="woven" onDraftCaptured={restoreExpanded} onActiveSessionChange={setPrimarySessionId}
                    selectedMethods={selectedMethods} onSelectedMethodsChange={setSelectedMethods}
                    onOpenMethods={() => { restoreExpanded(); updateWorkspaceState({ rightPanelView: 'workflows', coordinationCollapsed: false }); }}
                    onPlanPanelChange={setPlanPanel}
                    onTurnPhaseChange={setTurnPhase}
                    onOpenPlan={revision => { restoreExpanded(); updateWorkspaceState({ rightPanelView: 'plan', coordinationCollapsed: false }); setPlanFocusRevision(current => ({ revision, sequence: (current?.sequence ?? 0) + 1 })); }}
                    fileCatalog={currentFileCatalog} onOpenFile={openContainedFile}
                    onSessionBootedPrompt={({ sessionId, prompt, persona }) => setWorkspaceState(current => Object.hasOwn(current.chatTitles ?? {}, sessionId) ? current : { ...current, chatTitles: { ...(current.chatTitles ?? {}), [sessionId]: deriveChatTitle({ firstOperatorMessage: prompt, persona, sessionId }) } })}
                    resumeConversation={pendingResume?.projection.session?.continuation?.roleId === searchParams.get('agent') &&
                      pendingResume.projection.session.continuation.projectRoot === projectRoot ? pendingResume : undefined}
                    onConversationResumed={() => { setPendingResume(undefined); returnToPrimaryDialogue(); }}
                    knownRoots={workspaceState.knownRoots ?? []} onBindingChange={setBinding} onNewChatSettled={handleNewChatSettled} newChatRequest={newChatRequest} folderSelectionPending={folderSelectionPending} onFolderSelectionPending={setFolderSelectionPending} />
                </Suspense>
                </fieldset>
              </>
            }
          />
        </main>

        <div
          className={
            workspaceState.navigatorCollapsed
              ? 'woven-region woven-region--navigator is-collapsed'
              : 'woven-region woven-region--navigator'
          }
        >
          <button
            type="button"
            className="woven-region-toggle button-muted"
            aria-label={workspaceState.navigatorCollapsed ? 'Open Navigator' : 'Close Navigator'}
            onClick={() => {
              updateWorkspaceState({
                navigatorCollapsed: !workspaceState.navigatorCollapsed
              });
            }}
          >
            {workspaceState.navigatorCollapsed ? <span className="woven-collapsed-brand" aria-hidden="true">C</span> : <span aria-hidden="true">‹</span>}
          </button>
          {!workspaceState.navigatorCollapsed ? (
            <Navigator
              footerSlot={settingsControl}
              onNewChat={() => { if (!streaming && !folderSelectionPending) setNewChatRequest(value => value + 1); }}
              activeSurface="dialogue"
              legacyHref={legacyHref}
              sessions={navigatorSessions}
              sessionSurfaces={workspaceState.sessionSurfaces}
              liveSessionId={primarySessionId}
              selectedSessionId={selectedReplayId(replayState)}
              selectionDisabled={streaming}
              needsAnswerSessionIds={needsAnswerSessionIds}
              onNeedsAnswer={id => {
                if (id === primarySessionId) {
                  const anchor = document.getElementById(`requests-${id}`);
                  anchor?.scrollIntoView({ block: 'nearest' });
                  anchor?.querySelector<HTMLElement>('input, button, summary')?.focus();
                } else setAttentionSessionId(id);
              }}
              sessionsLoading={sessionsLoading}
              sessionsError={sessionsError}
              chatTitles={workspaceState.chatTitles ?? {}}
              chatPins={workspaceState.chatPins ?? []}
              chatArchived={workspaceState.chatArchived ?? []}
              chatDeleted={workspaceState.chatDeleted ?? []}
              chatGroups={workspaceState.chatGroups ?? []}
              groupsCollapsed={workspaceState.groupsCollapsed ?? []}
              currentRoot={projectRoot}
              folderOrder={knownRootPaths}
              foldersCollapsed={workspaceState.foldersCollapsed ?? []}
              folderNotices={folderNotices}
              onLocateFolder={path => { void locateFolder(path); }}
              onForgetFolder={forgetFolder}
              referenceDay={referenceDay}
              searchEpoch={`${projectRoot ?? ''}:${runtimeEpoch}`}
              focusSearchRequest={focusNavigatorSearchRequest}
              onModalStateChange={setNavigatorModalOpen}
              onOrganizationChange={updateWorkspaceState}
              onOpenSurface={returnToPrimaryDialogue}
              onSelectSession={loadReplay}
            />
          ) : (
            <div className="woven-collapsed-strip" aria-label="Collapsed chat navigation">
              {needsAnswerSessionIds.length ? <button type="button" aria-label={`${needsAnswerSessionIds.length} chats need an answer`} onClick={() => updateWorkspaceState({ navigatorCollapsed: false })}>!</button> : null}
              <button type="button" aria-label="Search chats" onClick={() => { updateWorkspaceState({ navigatorCollapsed: false }); setFocusNavigatorSearchRequest(value => value + 1); }}>⌕</button>
              <button type="button" aria-label="New chat" disabled={streaming || folderSelectionPending} onClick={() => { if (!streaming && !folderSelectionPending) setNewChatRequest(value => value + 1); }}>＋</button>
              <div className="woven-collapsed-settings">{settingsControl}</div>
            </div>
          )}
        </div>

        <div
          className="woven-resize-handle woven-resize-handle--vertical woven-resize-handle--navigator"
          role="separator"
          tabIndex={0}
          aria-label="Resize Navigator"
          aria-orientation="vertical"
          aria-valuemin={220}
          aria-valuemax={360}
          aria-valuenow={clamp(workspaceState.navigatorWidth, 220, 360)}
          onPointerDown={(event) => {
            beginResize(event, 'navigator');
          }}
          onKeyDown={(event) => {
            if (
              ['ArrowLeft', 'ArrowRight', 'Home', 'End'].includes(event.key)
            ) {
              event.preventDefault();
              resizeByKeyboard('navigator', event.key, event.shiftKey);
            }
          }}
        />

        <div
          className="woven-resize-handle woven-resize-handle--vertical woven-resize-handle--coordination"
          role="separator"
          tabIndex={0}
          aria-label="Resize Coordination Panel"
          aria-orientation="vertical"
          aria-valuemin={280}
          aria-valuemax={maximumRightWidth}
          aria-valuenow={effectiveRightWidth}
          onPointerDown={(event) => {
            beginResize(event, 'coordination');
          }}
          onKeyDown={(event) => {
            if (
              ['ArrowLeft', 'ArrowRight', 'Home', 'End'].includes(event.key)
            ) {
              event.preventDefault();
              resizeByKeyboard('coordination', event.key, event.shiftKey);
            }
          }}
        />

        <aside
          className={
            workspaceState.coordinationCollapsed
              ? 'woven-region woven-region--coordination is-collapsed'
              : 'woven-region woven-region--coordination'
          }
        >
          {workspaceState.coordinationCollapsed ? <button type="button" className="woven-region-toggle button-muted" aria-label="Open Coordination" onClick={() => updateWorkspaceState({ coordinationCollapsed: false })}>›</button> : null}
          {!workspaceState.coordinationCollapsed ? (
            <RightPanel readPlanRevisions={readPlanRevisions} onPlanRead={markPlanRead} workflowFeedbackDisabled={replayVisible || folderSelectionPending} onWorkflowFeedback={request => { restoreExpanded(); setWorkflowFeedback({ ...request, sequence: ++workflowFeedbackSequence.current }); }} settingsView={settingsView} folderLocked={binding.locked || streaming || folderSelectionPending} onFolderSelectionPending={setFolderSelectionPending} folderMismatch={binding.locked && Boolean(binding.root && binding.root !== projectRoot)} state={workspaceState} sessionOpen={coordinationView === 'session'}
              replayState={replayState} recordedSessionIds={sessions.map(session => session.sessionId)}
              primarySessionId={primarySessionId} liveTurnActive={streaming} onOpenParent={sessionId => loadReplay(sessionId, true)}
              onView={(view) => {
                restoreExpanded();
                updateWorkspaceState({ rightPanelView: view, ...(view === 'files' ? { openDocumentPath: null } : {}) });
                if (view === 'agents') setCoordinationView('agents');
              }}
              onOpenFile={openContainedFile}
              selectedMethods={selectedMethods}
              onSelectedMethodsChange={setSelectedMethods}
              planPanel={planPanel}
              planFocusRevision={planFocusRevision}
              onFileCatalog={handleFileCatalog}
              onExpand={toggleExpanded}
              onRefreshSessions={() => setSessionRefreshToken(token => token + 1)}
              onClose={() => {
                restoreExpanded();
                if (rightView === 'files' && workspaceState.openDocumentPath) updateWorkspaceState({ openDocumentPath: null });
                else if (rightView === 'agents' && coordinationView === 'session') setCoordinationView('agents');
                else updateWorkspaceState({ coordinationCollapsed: true });
              }}
              coordination={<CoordinationPanel embedded
              nativeEvents={events.filter(event => event.sessionId === primarySessionId)}
              activeView={coordinationView}
              replaySlot={
                replayVisible ? (
                  <SelectedSessionReplayLens
                    state={replayState}
                    primarySessionId={primarySessionId}
                    onReturnToPrimary={returnToPrimaryDialogue}
                    onContinue={continueRecordedConversation}
                    onRetry={() => {
                      const sessionId = selectedReplayId(replayState);
                      if (sessionId) {
                        void replayLoaderRef.current?.load(sessionId, {
                          observedAt: new Date().toISOString(),
                          availableSessionIds: new Set(sessions.map((session) => session.sessionId))
                        });
                      }
                    }}
                  />
                ) : undefined
              }
              hierarchy={hierarchy}
              sessionsLoading={sessionsLoading}
              sessionsError={sessionsError}
              selectedSessionId={selectedReplayId(replayState)}
              selectionDisabled={streaming}
              onSelectView={(coordinationView) => {
                restoreExpanded();
                setCoordinationView(coordinationView);
              }}
              onRefreshSessions={() => {
                setSessionRefreshToken((token) => token + 1);
              }}
              onSelectSession={sessionId => loadReplay(sessionId, true)}
            />} />
          ) : (
            <span className="woven-collapsed-label">Coordination</span>
          )}
        </aside>

        {attention.observers}
        {attentionSessionId ? <ChatAttentionDialog sessionId={attentionSessionId} title={workspaceState.chatTitles?.[attentionSessionId] ?? deriveChatTitle({ sessionId: attentionSessionId, persona: sessions.find(session => session.sessionId === attentionSessionId)?.persona })} rows={attention.rows[attentionSessionId] ?? []} onClose={() => setAttentionSessionId(null)} /> : null}
        <ActivityStrip primarySessionId={primarySessionId} reconnectControl={reconnectControl} running={streaming} phase={turnPhase} events={events}
          onOpenDetails={() => { restoreExpanded(); updateWorkspaceState({ rightPanelView: 'activity', coordinationCollapsed: false }); }} />
      </section>
      )}
    />
  );
}
