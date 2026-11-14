import { ActionFeedback } from "./ActionFeedback";
import { LOCAL_ENTRY, LOCAL_FORK_AVAILABLE, LOCAL_FORK_UNAVAILABLE, LOCAL_MODE, LocalProviderAccess, generationKey, localRoute, localViewFrom, readAttemptedLocalEntries, recordAttemptedLocalEntry, forgetAttemptedLocalEntry, type LocalView } from "./LocalProviderAccess";
import { NativeWaitingBridge } from "./NativeWaitingBridge";
import { ConnectorSourcePanel } from "./ConnectorSourcePanel";
import { FleetRecordsPanel, readFleetPacket, type FleetPacket } from "./FleetRecordsPanel";
import { RecordsStorePanel } from "./RecordsStorePanel";
import { ConnectorRoutePanel, emptyRouteRead, routeReadTransition, type RouteReadState, type RouteView } from "./ConnectorRoutePanel";
// The interface reads host snapshots and asks the host to act. It holds no pipe
// (HOSTING H2), writes no record and cannot capture an act: the native
// confirmation is the host's (AAC §6.2 P-2). Views per DECISION_VIEW.md §4.
import { useCallback, useEffect, useRef, useState, type Ref } from "react";
import { appHome, CodexProcessControls, stopLabel } from "./CodexControls";
import { ContinueAsPanel, ModelIdField, RoleChoice, RoleHeader, RoleHistoryReader, SupplyStatus, type ContinueStartOutcome, type HandoffSendOutcome } from "./ConversationRoles";
import { EXACT_TEXT } from "./exactText";
import { ArrivalRecord, CompatibilityAdvisory, HistoryReferenceNotice, RunBringBack, RunPanel, SelectedWorkflow, hasUnsavedHistoryReference, isRecordedRun, runBringBackDefault, type OpenArrivalFileAct } from "./RunPanel";
import { chatWorkflow, workflowArguments, workflowContext } from "./workflowSelection";
import { FileActPanel, type FileActPanelHandle } from "./FileActPanel";
import { NativeActivityView, activityModel, sameActivityGeneration, type NativeActivityHandle } from "./NativeActivity";
import { ContinuationContext, historyPageBinding, StoredItemPage, StoredTurnPage } from "./NativeHistory";
import { ObserverAttachment } from "./ObserverAttachment";
import { PlanModeControl } from "./PlanMode";
import { NativeRequestCard, WaitingRequestsIndicator, answerable, hostRequests, requestItem, requestPlace, requestThread, requestScopeKey, requestReplyGuarded, type RequestActivityLink, type RequestAnswer, type ReadRequestCustody, type RequestReplyObservation, type WaitingRequestGroup } from "./RequestCards";
import { RunOffer, type RunAct } from "./RunOffers";
import { RecoveryCustodyPanel } from "./RecoveryCustodyPanel";
import { CompareResult, initialDraftsState, LastCleanTrialLine, WorkflowDraftsView, type DraftsState } from "./WorkflowDrafts";
import { LibraryEntries } from "./LibraryEntries";
import { WorkflowRegistrationReview } from "./WorkflowRegistrationReview";
import { BringBackComposer, CleanTrialPanel, DelegatedTrialComposer, composersFor, conversationKey, findConversation, hostMessage, prefillKept } from "./TrialComposer";
import { preparedMessages, preparedMessageLimit, type PreparedMessage } from "./preparedMessages";
import { ConversationContext, ProjectLibraryContext, appProjectFolder, conversationFromKey, workflowSourceLimit } from "./WorkflowContext";
import { DailyWorkspace, WorkspaceDisclosure, WorkspaceConnectionStatus, revealWorkspaceTarget, registerWorkspaceViews, WORKSPACE_VIEWS } from "./DailyWorkspace";
import { flushSync } from "react-dom";
import { DesktopSetupPanel } from "./DesktopSetupPanel";
// Every host command goes through hostReads' invoke, which marks when a command that may change the host settles.
import { invoke, useOrderedHost, shownBeforePress, POLL_MS } from "./hostReads";
import { readingAfterWrite, readingSentence } from "./readingSentences";
import { REFRESH_FAILED, commandThenRefresh, observationLine, observationText, refreshAfterAction, withRefreshFailure } from "./statusRefresh";
import { FirstUseSetup } from "./FirstUse";
import { AccountStatus, type ReadAccountStatus } from "./AccountStatus";
import { RunWorkflowGuide, registeredRevisionAnchor, runEvidenceAnchor } from "./RunJourney";
import { MakeWorkflowGuide } from "./MakeJourney";
import { acknowledgeBringBackDoubt, beginBringBack, bringBackRefusal, doubtDestination, endBringBack, noteBringBackDoubt, resetBringBackDoubts, sendKey, useBringBackDoubts, type BringBackDoubt } from "./bringBackDoubts";
import { AccessRouteChoice, AvailableModels, OfferedEffortChoice, modelMatch, validModelPacket } from "./ModelChoice";
/** One App-composed message for the person to edit and send; never sent by the App. */
export type ComposerOffer = { sequence: number; threadKey: string; text: string };
import { conversationTitle, DIGEST_LIMIT, digestComparison, nativePathText, readablePaths, reviewDigest, suppliedSummary, type ReviewDigestView, conversationLabel } from "./presentation";

type Json = any; // eslint-disable-line @typescript-eslint/no-explicit-any

export function SteeringControl({ target, reason, ready, busy, text, submit }: { target: Json; reason?: string; ready: boolean; busy: boolean; text: string; submit: () => void }) {
  return <div>
    <p>Current observed steering turn: {target?.turnId ?? "not established"} {target?.source && `· ${target.source}`}.</p>
    {!target && <p>{reason ?? "Choose a loaded conversation with an observed current live turn."}</p>}
    <button disabled={!ready || busy || !target?.turnId || !text} onClick={submit}>Steer current live turn</button>
    <p>Steering sends this text unchanged with the expected native turn ID. A steering acknowledgment does not establish turn replacement or completion. Source/target changes can refuse the request; the draft is retained on failure and no automatic resend occurs.</p>
  </div>;
}

// The access entries a new conversation may use in the active home.
const startEntries = (host: Json) => host?.homeRouting?.activeModeHomeClass === LOCAL_MODE
  ? [{ value: LOCAL_ENTRY, label: "oMLX in the local home (key kept by Codex)" }]
  : host?.homeRouting?.activeModeHomeClass !== "account"
  ? []
  : [{ value: "chatgpt-account", label: "ChatGPT account" }];

// The ordinary native command resolves only after private receipt admission
// and finalization, then adds its actual H5 tuple (lib.rs start_conversation).
// Record publication and the reported model are independent observations.
const startedConversationKey = (response: Json): string | null => {
  const generation = response?.startGeneration;
  const thread = response?.result?.thread?.id;
  if (!response || Object.hasOwn(response, "error") || !generation || Object.keys(generation).length !== 3 ||
      typeof generation.appSession !== "string" || !generation.appSession || typeof generation.home !== "string" || !generation.home ||
      !Number.isSafeInteger(generation.spawnCounter) || generation.spawnCounter <= 0 || typeof thread !== "string" || !thread) return null;
  return JSON.stringify([generation, thread]);
};

const emptyConversationChoice = { model: "", modelProvider: "", entryId: "" };

type ForkScope = { generation: Json; sourceThread: string; modeHomeClass: string; choiceRevision: number; homeEpoch: number; startRevision: number; sequence: number };
type ForkNavigation = ForkScope & { threadId: string; requestRef: string };
const sameForkGeneration = (a: Json, b: Json) => a?.appSession === b?.appSession && a?.home === b?.home && a?.spawnCounter === b?.spawnCounter;
// The dedicated native command returns Host::thread_fork_finish's admitted row.
// Role binding/publication standing is separate; no renderer field admits a
// thread. Selection also requires this exact row in the actual Host snapshot.
const admittedForkTarget = (response: Json, scope: ForkScope): Pick<ForkNavigation, "threadId" | "requestRef"> | null => {
  const row = response?.thread, generation = row?.generation, from = row?.forkedFrom;
  if (!response || Object.hasOwn(response, "error") || typeof generation?.appSession !== "string" || !generation.appSession ||
      typeof generation?.home !== "string" || !generation.home || !Number.isSafeInteger(generation?.spawnCounter) || generation.spawnCounter <= 0 ||
      !sameForkGeneration(generation, scope.generation) || typeof row?.threadId !== "string" || !row.threadId || row.threadId === scope.sourceThread ||
      from?.threadId !== scope.sourceThread || from?.reportedForkedFromId !== scope.sourceThread || typeof from?.forkRequestRef !== "string" || !from.forkRequestRef) return null;
  return { threadId: row.threadId, requestRef: from.forkRequestRef };
};

type AttachmentRequest = { generation: Json; threadId: string; expectedTurnId: string | null; text: string; ownerRef: string; listRevision: number; selectionRefs: string[] };
type AttachmentOutcome = { request: AttachmentRequest; result: { acknowledged: true; nativeValue: Json } | { acknowledged: false; nativeError: unknown }; observationLimit?: string };
type OrdinaryTextRequest = { generation: Json; threadId: string; text: string; mode?: "plan" | "default"; model?: string; effort?: string };
type OrdinaryTextOutcome = { request: OrdinaryTextRequest; result: { acknowledged: true; nativeValue: Json } | { acknowledged: false; nativeError: unknown }; observationLimit?: string };
/** An ordinary send without a native acknowledgement (any error, or a missing
 * result). It may have been sent, so the same conversation ID is held until the
 * person says they read it; it is kept for this window and never parsed. */
type UnconfirmedSend = { id: number; request: OrdinaryTextRequest; reported: string; acknowledged: boolean };
// Model choice has one local lifetime, keyed to the actual full conversation.
// Ordinary text intentionally remains one global draft across conversations.
const ordinaryConversationRef = (generation: Json, thread: string | undefined) => thread && generation
  ? JSON.stringify([generation.home, generation.appSession, generation.spawnCounter, thread]) : "";
type PreparedComposerReveal = { sequence: number; item: PreparedMessage; isCurrent: () => boolean; finish: (shown: boolean) => void };

export function ConversationPanel({ localRoute = null, focusComposer, startAct, composerOffer, host, threadKey, setThreadKey, answer, readRequest, replyObservations, runAct, trialRunAct, send, observeOrdinaryView, steer, submitAttachments, observeAttachmentView, interrupt, checkPlanMode, codexBusy, forkConversation, handoffSend, handoffRead, activityNavigationRef, activityLink, preparedReveal }: { localRoute?: LocalView | null; focusComposer?: number; startAct?: RunAct; composerOffer?: ComposerOffer | null; preparedReveal?: PreparedComposerReveal | null; activityNavigationRef?: Ref<NativeActivityHandle>; activityLink?: RequestActivityLink; forkConversation?: (generation: Json, sourceThread: string) => Promise<void>; handoffSend?: (id: string, text: string) => Promise<HandoffSendOutcome>; handoffRead?: (id: string) => Promise<HandoffSendOutcome>; codexBusy: boolean; host: Json; threadKey: string; setThreadKey: (key: string) => void; trialRunAct?: RunAct; answer: RequestAnswer; readRequest?: ReadRequestCustody; replyObservations?: Record<string, RequestReplyObservation>; runAct: RunAct; checkPlanMode: (generation: Json) => Promise<void>; submitAttachments: (generation: Json, thread: string, expected: string | null, text: string, owner: string, revision: number, refs: string[]) => Promise<Json>; observeAttachmentView?: (request: AttachmentRequest) => Promise<void>; send: (generation: Json, thread: string, text: string, mode?: "plan" | "default", model?: string, effort?: string) => Promise<Json>; observeOrdinaryView?: (request: OrdinaryTextRequest, isCurrent: () => boolean) => Promise<void>; steer: (generation: Json, thread: string, expected: string, text: string) => Promise<boolean | void>; interrupt: (generation: Json, thread: string, turn: string) => Promise<boolean | void> }) {
  const [turnId, setTurnId] = useState<string>("");
  const [offerBusy, setOfferBusy] = useState(false);
  const [text, setText] = useState<string>("");
  const textRevision = useRef(0);
  const composerField = useRef<HTMLTextAreaElement>(null);
  const [ordinaryModel, setOrdinaryModel] = useState({ owner: "", value: "", effort: "", effortModel: "", revision: 0 });
  const [ordinaryOutcome, setOrdinaryOutcome] = useState<OrdinaryTextOutcome | null>(null);
  // Unconfirmed ordinary sends, read at every press through the ref (not the render).
  const [unconfirmed, setUnconfirmedState] = useState<UnconfirmedSend[]>([]);
  const unconfirmedRef = useRef<UnconfirmedSend[]>([]);
  const unconfirmedSequence = useRef(0);
  const modelRevisionRef = useRef(0);
  const setUnconfirmed = (update: (rows: UnconfirmedSend[]) => UnconfirmedSend[]) => { unconfirmedRef.current = update(unconfirmedRef.current); setUnconfirmedState(unconfirmedRef.current); };
  const heldSend = (threadId: string | undefined) => !!threadId && unconfirmedRef.current.some(row => !row.acknowledged && row.request.threadId === threadId);
  // The draft is one global text; say where it goes when it was written for another conversation.
  const textWrittenFor = useRef<string>("");
  // One synchronous owner across ordinary turn controls, before React renders busy.
  const turnActionPending = useRef(false);
  const ordinaryView = useRef({ owner: "", epoch: 0, ready: false });
  const [ownBusy, setBusy] = useState<string>("");
  const [forkBusy, setForkBusy] = useState(false);
  const forking = useRef(false);
  // While Start/Stop/Restart Codex runs, no text, steer or attachment send is offered
  // (the host also refuses new turns once a stop is confirmed).
  const busy = ownBusy || (codexBusy ? "Stop or Restart Codex in progress" : "");
  const [error, setError] = useState<string>("");
  const [attachmentOutcome, setAttachmentOutcome] = useState<AttachmentOutcome | null>(null);
  const attachmentView = useRef({ generation: host?.generation, threadKey });
  attachmentView.current = { generation: host?.generation, threadKey };
  const generationKey = JSON.stringify(host?.generation);
  const currentThreads = (host?.threads ?? []).filter((thread: Json) => JSON.stringify(thread.generation) === generationKey);
  const selected = currentThreads.find((thread: Json) => JSON.stringify([thread.generation, thread.threadId]) === threadKey);
  const ordinaryOwner = ordinaryConversationRef(selected?.generation, selected?.threadId);
  const sourceReady = host?.state === "ready" && host?.generationClosed !== true;
  if (ordinaryView.current.owner !== ordinaryOwner || ordinaryView.current.ready !== sourceReady) {
    ordinaryView.current = { owner: ordinaryOwner, epoch: ordinaryView.current.epoch + 1, ready: sourceReady };
  }
  useEffect(() => {
    setOrdinaryModel(current => current.owner === ordinaryOwner ? current : { owner: ordinaryOwner, value: "", effort: "", effortModel: "", revision: current.revision + 1 });
  }, [ordinaryOwner]);
  const ordinaryModelValue = ordinaryModel.owner === ordinaryOwner ? ordinaryModel.value : "";
  const liveTurns = (host?.conversationTurns ?? []).filter((turn: Json) => selected && JSON.stringify(turn.generation) === generationKey && turn.threadId === selected.threadId && turn.nativeTurn?.status === "inProgress" && !turn.observationEnded && !turn.terminalEventObserved);
  const live = liveTurns.find((turn: Json) => turn.turnId === turnId);
  const steering = (host?.steeringTargets ?? []).find((row: Json) => selected && JSON.stringify(row.generation) === generationKey && row.threadId === selected.threadId);
  const steeringTarget = steering?.target && JSON.stringify(steering.target.generation) === generationKey && steering.target.threadId === selected?.threadId ? steering.target : null;
  const alreadyRequested = (host?.turnInterruptRequests ?? []).some((request: Json) => live && JSON.stringify(request.binding?.generation) === generationKey && request.binding?.threadId === live.threadId && request.binding?.turnId === live.turnId && (request.clientRequest?.outcome === "response-observed-result" || (request.clientRequest?.outcome === "pending" && request.clientRequest?.writeResult === "written")));
  // The send intent this render shows: its conversation view, text edit, model
  // choice and the unconfirmed attempts so far. A Send or plan/default control
  // acts only while all are still current, so a control captured before a
  // failed attempt or a newer choice never sends (even after an acknowledgement).
  const sendBinding = { owner: ordinaryView.current.owner, epoch: ordinaryView.current.epoch, textRevision: textRevision.current, modelRevision: ordinaryModel.revision, attempts: unconfirmedSequence.current };
  modelRevisionRef.current = ordinaryModel.revision;
  const sendText = async (mode?: "plan" | "default") => {
    if (!selected || !text || busy || turnActionPending.current || !sourceReady) return;
    if (ordinaryView.current.owner !== sendBinding.owner || ordinaryView.current.epoch !== sendBinding.epoch || !ordinaryView.current.ready
      || textRevision.current !== sendBinding.textRevision || modelRevisionRef.current !== sendBinding.modelRevision || unconfirmedSequence.current !== sendBinding.attempts) {
      setError("Not sent: that Send belonged to an earlier view of the conversation, text or model. Check them and press Send again."); return;
    }
    // Shared by Send text and the plan/default controls; a retained control can't bypass it.
    if (heldSend(selected.threadId)) { setError("Not sent: an earlier message to this conversation wasn't confirmed and may have been sent. Read the conversation, then confirm below before sending again."); return; }
    const request: OrdinaryTextRequest = { generation: { ...selected.generation }, threadId: selected.threadId, text,
      ...(mode ? { mode } : {}), ...(ordinaryModelValue ? { model: ordinaryModelValue } : {}), ...(ordinaryModel.owner === ordinaryOwner && ordinaryModel.effort ? { effort: ordinaryModel.effort, model: ordinaryModel.effortModel } : {}) };
    const view = ordinaryView.current, revision = textRevision.current, choice = ordinaryModel;
    const isCurrent = () => ordinaryView.current.owner === view.owner && ordinaryView.current.epoch === view.epoch && ordinaryView.current.ready;
    turnActionPending.current = true;
    setBusy(mode ? `sending in ${mode} mode` : "sending"); setError(""); setOrdinaryOutcome(null);
    let outcome: OrdinaryTextOutcome;
    try {
      const nativeValue = request.effort
        ? await send(request.generation, request.threadId, request.text, request.mode, request.model, request.effort)
        : await send(request.generation, request.threadId, request.text, request.mode, request.model);
      // A missing reply is not an acknowledgement: nothing is cleared, and it is held.
      if (nativeValue === undefined || nativeValue === null) throw new Error("The host did not report this send's outcome; it may or may not have been sent.");
      outcome = { request, result: { acknowledged: true, nativeValue } };
      if (isCurrent()) {
        if (textRevision.current === revision) setText(current => current === request.text ? "" : current);
        setOrdinaryModel(current => current.owner === choice.owner && current.revision === choice.revision
          ? { ...current, value: "", effort: "", effortModel: "", revision: current.revision + 1 } : current);
      }
    } catch (nativeError) {
      outcome = { request, result: { acknowledged: false, nativeError } };
      const reported = nativeError instanceof Error ? nativeError.message : String(nativeError);
      setUnconfirmed(rows => [...rows, { id: ++unconfirmedSequence.current, request: structuredClone(request), reported, acknowledged: false }]);
    }
    setOrdinaryOutcome(outcome);
    try { await observeOrdinaryView?.(request, isCurrent); }
    catch (error) { setOrdinaryOutcome({ ...outcome, observationLimit: observationText(error) }); }
    finally { turnActionPending.current = false; setBusy(""); }
  };
  const steerText = async () => {
    if (!sourceReady || !selected || !steeringTarget || !text || busy || turnActionPending.current) return;
    const view = ordinaryView.current, revision = textRevision.current;
    const isCurrent = () => ordinaryView.current.owner === view.owner && ordinaryView.current.epoch === view.epoch && ordinaryView.current.ready;
    turnActionPending.current = true;
    setBusy("steering"); setError("");
    try {
      const currentAcknowledgment = await steer(selected.generation, selected.threadId, steeringTarget.turnId, text);
      // The parent also guards navigation intents that leave and return before
      // this panel renders. A later edit, even to identical text, stays unsent.
      if (currentAcknowledgment !== false && isCurrent() && textRevision.current === revision) setText(current => current === text ? "" : current);
    }
    catch (e) { if (isCurrent()) setError(String(e)); }
    finally { turnActionPending.current = false; setBusy(""); }
  };
  const attachmentText = async (expected: string | null) => {
    const selection = host?.attachmentSelections;
    if (!sourceReady || !selected || !selection?.ownerRef || !(selection.selections ?? []).length || busy || turnActionPending.current) return;
    const request: AttachmentRequest = { generation: selected.generation, threadId: selected.threadId, expectedTurnId: expected, text, ownerRef: selection.ownerRef, listRevision: selection.listRevision, selectionRefs: selection.selections.map((row: Json) => row.selection.selectionRef) };
    turnActionPending.current = true;
    setBusy(expected ? "steering with attachments" : "sending with attachments"); setError("");
    setAttachmentOutcome(null);
    let outcome: AttachmentOutcome;
    try {
      const nativeValue = await submitAttachments(request.generation, request.threadId, request.expectedTurnId, request.text, request.ownerRef, request.listRevision, request.selectionRefs);
      // Fulfilment is the host's matching-ack contract. A later view read cannot
      // change it, clear another conversation's draft or erase a newer edit.
      outcome = { request, result: { acknowledged: true, nativeValue } };
      if (JSON.stringify(attachmentView.current.generation) === JSON.stringify(request.generation) && attachmentView.current.threadKey === JSON.stringify([request.generation, request.threadId])) {
        setText(current => current === request.text ? "" : current);
      }
    } catch (nativeError) { outcome = { request, result: { acknowledged: false, nativeError } }; }
    setAttachmentOutcome(outcome);
    try { await observeAttachmentView?.(request); }
    catch (e) { setAttachmentOutcome({ ...outcome, observationLimit: observationText(e) }); }
    finally { turnActionPending.current = false; setBusy(""); }
    return outcome.result.acknowledged ? outcome.result.nativeValue : undefined;
  };
  const interruptTurn = async () => {
    if (!sourceReady || !selected || !live || ownBusy || turnActionPending.current || alreadyRequested) return;
    const view = ordinaryView.current;
    turnActionPending.current = true;
    setBusy("interrupting"); setError("");
    try { await interrupt(live.generation, live.threadId, live.turnId); }
    catch (e) { if (ordinaryView.current.owner === view.owner && ordinaryView.current.epoch === view.epoch && ordinaryView.current.ready) setError(String(e)); }
    finally { turnActionPending.current = false; setBusy(""); }
  };
  // NIR §4.1/§4.8: this conversation's request cards sit beside its activity, waiting ones first.
  const requests: Json[] = hostRequests(host).filter((request: Json) => selected && requestThread(request) === selected.threadId);
  const ordered = [...requests.filter(answerable), ...requests.filter((request: Json) => !answerable(request))];
  const offers: Json[] = (host?.workflowRoot?.offers ?? []).filter((offer: Json) => selected && offer?.message?.threadId === selected.threadId);
  const runs: Json[] = (host?.workflowRoot?.runs ?? []).filter((run: Json) => selected && run?.conversation === selected.threadId && run?.home === selected.generation?.home);
  const offerAct: RunAct = async (command, args) => { setOfferBusy(true); try { return await runAct(command, args); } finally { setOfferBusy(false); } };
  // NIR §5.8: Continue as and Fork go through the host; neither changes this conversation's role.
  // Resolves to the host's result, or undefined when the command failed (runAct shows the error).
  const roleAct = async (label: string, command: string, args: Record<string, unknown>, after?: (result: Json) => void): Promise<Json> => {
    setBusy(label); setError("");
    try { const result = await runAct(command, args); if (result === undefined) setError(`${label} did not complete; see the message below.`); else after?.(result); return result; }
    finally { setBusy(""); }
  };
  // Continue as: the start's outcome goes to its own panel in plain words. A
  // rejection carries the host's message; it is not read for whether Codex started.
  const startContinueAs = async (args: Record<string, unknown>): Promise<ContinueStartOutcome> => {
    setBusy("starting the new conversation"); setError("");
    try {
      const result = await (startAct ?? runAct)("thread_start", args);
      return result === undefined ? { ok: false, message: "The App did not report the start's outcome." } : { ok: true };
    } catch (error) { return { ok: false, message: hostMessage(error) }; }
    finally { setBusy(""); }
  };
  const forkSelected = async () => {
    if (!selected || busy || forking.current) return;
    if (!forkConversation) { setError("The original Fork handler is unavailable."); return; }
    forking.current = true; setForkBusy(true); setError("");
    try { await forkConversation(selected.generation, selected.threadId); }
    catch (error) { setError(String(error)); }
    finally { forking.current = false; setForkBusy(false); }
  };
  const handoffs: Json[] = host?.continueAs ?? [];
  // WR TT-3a, TT-3b, TT-10: what the host pre-filled for the person to send.
  // Every send below happens only on the person's Send press.
  // A trial or bring-back command rejects with the host's message as given, so
  // the composer can show it (the host says whether the message stays
  // pre-filled or was withdrawn); it is also shown in this panel's alert.
  const trialAct = async (command: string, args: Record<string, unknown>): Promise<Json> => {
    const label = `trial: ${command}`;
    setBusy(label); setError("");
    try {
      const result: Json = await (trialRunAct ?? runAct)(command, args);
      if (result === undefined) setError(`${label} did not complete; see the message below.`);
      else if (command === "workflow_trial_start_clean" && result?.thread?.threadId) setThreadKey(JSON.stringify([result.thread.generation, result.thread.threadId]));
      return result;
    } catch (e) { setError(`${label}: ${hostMessage(e)}`); throw e; }
    finally { setBusy(""); }
  };
  const workflowRoot = host?.workflowRoot;
  const composers = composersFor(workflowRoot, selected);
  const prepared = preparedMessages(host);
  const preparedNodes = useRef(new Map<string, HTMLDivElement>());
  const announcedDoubt = useRef(new Set<string>());
  const doubts = useBringBackDoubts();
  // An offered request fills only an empty composer of its own conversation; unsent
  // text is never replaced without the person's press, and nothing is sent.
  const [heldOffer, setHeldOffer] = useState<ComposerOffer | null>(null);
  const handledOffer = useRef(0);
  // A navigation that admitted this conversation (History Continue) lands in its message box.
  useEffect(() => {
    if (!focusComposer) return;
    composerField.current?.scrollIntoView?.({ block: "center" });
    composerField.current?.focus?.({ preventScroll: true });
  }, [focusComposer]);
  // A new unconfirmed send for the shown conversation takes the focus once, so
  // keyboard and screen-reader users land on why Send is held.
  const announcedUnconfirmed = useRef(new Set<number>());
  useEffect(() => {
    if (!composerOffer || handledOffer.current === composerOffer.sequence || composerOffer.threadKey !== threadKey) return;
    handledOffer.current = composerOffer.sequence;
    if (text === "") { textRevision.current += 1; textWrittenFor.current = composerOffer.threadKey; setText(composerOffer.text); setHeldOffer(null); }
    else setHeldOffer(composerOffer);
    // Reveal the message box itself: with a conversation selected it sits
    // below the role and activity sections.
    revealWorkspaceTarget("conversation");
    composerField.current?.scrollIntoView?.({ block: "center" });
    composerField.current?.focus?.({ preventScroll: true });
  }, [composerOffer, threadKey]); // eslint-disable-line react-hooks/exhaustive-deps
  const handledReveal = useRef(0);
  useEffect(() => {
    if (!preparedReveal || handledReveal.current === preparedReveal.sequence) return;
    handledReveal.current = preparedReveal.sequence;
    const { item } = preparedReveal;
    const node = preparedNodes.current.get(item.identity);
    const shown = !!node && !node.hidden && !!findConversation(selected ? [selected] : [], item.owner)
      && preparedMessageLimit(host, item) === null && preparedReveal.isCurrent();
    // Refs identify the exact original composer after React has unhidden it.
    // No transcript-bearing DOM ID or later poll can repeat this reveal.
    if (shown) {
      node.scrollIntoView?.({ block: "start" });
      // Land on the composer's message itself, ready to read and edit.
      let field: HTMLElement | null = null;
      try { field = typeof node.querySelector === "function" ? node.querySelector("textarea") : null; } catch { field = null; }
      if (!field) node.setAttribute("tabindex", "-1");
      (field ?? node).focus?.({ preventScroll: true });
    }
    preparedReveal.finish(shown);
  }, [preparedReveal, host, threadKey]); // eslint-disable-line react-hooks/exhaustive-deps
  const trialConversation = (workflowRoot?.trialConversations ?? []).find((row: Json) => selected && row?.threadId === selected.threadId);
  const trialsStartedHere = (workflowRoot?.trialsStartedHere ?? []).find((row: Json) => selected && row?.threadId === selected.threadId);
  // Keys of this section's direct children must differ from each other: the role
  // header and the activity view once shared the thread ID as key, and React then
  // left the previous conversation's header mounted on every switch (witness
  // 2026-10-10 D-1). Each per-conversation child keys on its own prefix.
  const sendReadiness = !sourceReady ? "Connect to Codex before sending. Your draft stays here."
    : !selected ? "Choose a current conversation, start a new one, or continue one from History. Your draft is not sent by choosing."
    : busy ? "An operation is pending. New messages are paused until its result is received."
    : unconfirmed.some(row => !row.acknowledged && row.request.threadId === selected.threadId) ? "An earlier message to this conversation wasn't confirmed and may have been sent. Read the conversation, then confirm below before sending again. Your text is kept."
    : !text ? "Write a message to send to the selected conversation."
    : `Ready to send text to ${conversationLabel(host, selected)}. Sending does not change its role or access entry.`;
  const interruptReadiness = !sourceReady ? "Interruption is unavailable because this Codex source is not ready."
    : !selected ? "Choose the conversation whose turn you want to interrupt."
    : ownBusy ? "Wait for the pending conversation operation before interrupting."
    : liveTurns.length === 0 ? "No current live turn is observed in this conversation. This does not prove that all work has ended."
    : !live ? "Choose an observed live turn below. Interruption targets that turn only."
    : alreadyRequested ? "Interrupt already requested; awaiting native turn status."
    : "The selected live turn can be interrupted. This does not end a workflow run or prove that child work has stopped.";
  return <section id="conversation" aria-labelledby="conversation-heading">
    <h2 id="conversation-heading">Conversation</h2>
    <label>Current-generation conversation <select disabled={!!ownBusy} value={threadKey} onChange={e => { setThreadKey(e.target.value); setTurnId(""); setError(""); }}>
      <option value="">Select a conversation</option>
      {currentThreads.map((thread: Json) => <option key={JSON.stringify([thread.generation, thread.threadId])} value={JSON.stringify([thread.generation, thread.threadId])}>{conversationLabel(host, thread)} via {thread.modelProvider ?? "provider not reported"}</option>)}
    </select></label>
    {selected && <details className="conversation-identity"><summary>Exact conversation ID</summary><code>{selected.threadId}</code></details>}
    {selected && <details className="conversation-options"><summary>Role and continuation options</summary><RoleHeader key={`role-header:${JSON.stringify([selected.generation, selected.threadId])}`} thread={selected} limits={host?.roleLimits} busy={!!busy || forkBusy} ready={host?.state === "ready"} trialConversation={trialConversation} trialsStartedHere={trialsStartedHere}
      readSupplyHistory={() => invoke("role_supply_history", { generation: selected.generation, thread: selected.threadId })}
      continueAs={role => { void roleAct("asking for a handoff summary", "continue_as_begin", { generation: selected.generation, threadId: selected.threadId, role }); }}
      forkUnavailable={host?.homeRouting?.activeModeHomeClass === LOCAL_MODE && !LOCAL_FORK_AVAILABLE ? LOCAL_FORK_UNAVAILABLE : undefined}
      fork={() => { void forkSelected(); }} /></details>}
    {selected && <ContinuationContext key={`prior-work:${JSON.stringify([selected.generation, selected.threadId, selected.resumeRequestRef])}`} host={host} thread={selected} />}
    {threadKey && !selected && <p>Selected conversation is no longer available in this generation; choose a current conversation.</p>}
    {handoffs.map((handoff: Json) => <ContinueAsPanel key={handoff.id} handoff={handoff} entries={startEntries(host)} homeClass={host?.homeRouting?.activeModeHomeClass ?? null} generation={host?.generation ?? null} busy={!!busy} ready={host?.state === "ready"} local={localRoute}
      start={(choice, source) => startContinueAs({ ...choice, modeHomeClass: source.modeHomeClass, generation: source.generation, role: handoff.targetRole ?? null, preselected: false, continueAs: handoff.id })}
      send={draft => handoffSend ? handoffSend(handoff.id, draft) : Promise.resolve({ state: "unknown", reason: "The original handoff sender is unavailable." })}
      read={handoffRead ? () => handoffRead(handoff.id) : undefined}
      open={() => { const started = handoff.started; if (started) setThreadKey(JSON.stringify([started.generation, started.threadId])); }}
      dismiss={() => { void roleAct("closing the handoff", "continue_as_dismiss", { id: handoff.id }); }} />)}
    {[...doubts].sort((a, b) => Number(doubtDestination(b, selected) !== "other") - Number(doubtDestination(a, selected) !== "other")).map(row => {
      const id = `${row.kind}:${row.ref}:${row.preparedId}`;
      // Every unconfirmed send stays reachable here, whichever conversation is
      // shown; it is described by where it actually went, never relabelled.
      const where = doubtDestination(row, selected);
      const what = row.kind === "trial" ? `Trial ${String(row.sequence ?? "")}'s` : "The run's";
      const loaded = (host?.threads ?? []).find((t: Json) => t?.threadId === row.target?.threadId && JSON.stringify(t?.generation) === JSON.stringify(row.target?.generation) && JSON.stringify(t?.generation) === JSON.stringify(host?.generation));
      const destination = where === "same" ? "this conversation" : loaded ? conversationLabel(host, loaded) : `conversation ${String(row.target?.threadId ?? "")} in a Codex session that isn't loaded now`;
      return <div key={`doubt:${id}`} role={row.acknowledged ? "note" : "alert"} tabIndex={-1} ref={node => { if (node && where === "same" && !announcedDoubt.current.has(id)) { announcedDoubt.current.add(id); node.focus?.({ preventScroll: false }); } }} aria-label="Bring-back send not confirmed">
        <p><strong>{what} results may have been sent to {destination}.</strong> The App couldn't confirm the send. {(host?.workflowRoot?.pendingBringBacks ?? []).some((pending: Json) => pending?.id === row.preparedId)
          ? "Its prepared message is still listed, but that copy is not sent again; after reading the conversation you can remove it."
          : "The prepared message was withdrawn, so nothing is resent."} Read that conversation to see whether it arrived.{row.acknowledged ? " You've said you checked; bringing it back there again is allowed." : " Bringing it back there again is held until you've checked."}</p>
        {where === "same-id-other-source" && <p><small>Codex or the home has changed since that send. The conversation shown now has the same ID, so bringing these results back to it is held too; that doesn't make the earlier destination this one.</small></p>}
        {!row.acknowledged && <p><button onClick={() => acknowledgeBringBackDoubt(row)}>I've checked this conversation — allow bringing it back again</button> <small>Starts nothing; this record stays.</small></p>}
        <details><summary>Your message and what was reported</summary><p><small>Your message: {row.personText || "(empty)"}</small></p><p><small>Reported: {row.message}</small></p>
          <p><small>Original destination: conversation <code>{String(row.target?.threadId ?? "")}</code> in Codex session {String(row.target?.generation?.spawnCounter ?? "not reported")} of the {String(row.source?.modeHomeClass ?? "unreported")} home.</small></p></details>
      </div>;
    })}
    {prepared.map(item => <div key={item.identity} ref={node => { if (node) preparedNodes.current.set(item.identity, node); else preparedNodes.current.delete(item.identity); }} hidden={item.kind === "delegated" ? !composers.delegated.includes(item.pending) : item.kind === "bring-back" ? !composers.bringBacks.includes(item.pending) : false}>
      {item.kind === "clean" ? <div aria-label="Original composer owner"><p>This trial starts its own new conversation; it isn't sent in an existing one.</p>
        <details><summary>Exact scope</summary><p><small>Trial reference <code>{item.pending?.reference ?? "not reported"}</code>. Its composer belongs to no existing conversation; Send starts the new conversation with the connection and model you choose.</small></p></details></div>
        : <ConversationContext label="Original composer owner" host={host} reference={item.owner} workflow limit={preparedMessageLimit(host, item)} />}
      {item.kind === "clean" ? <CleanTrialPanel pending={item.pending} roleSet={host?.roleSet} limits={host?.roleLimits} entries={startEntries(host)}
        modeHomeClass={host?.homeRouting?.activeModeHomeClass} generation={host?.generation ?? null} busy={!!busy} ready={host?.state === "ready" && host?.generationClosed !== true} act={trialAct} local={localRoute} />
        : item.kind === "delegated" ? <DelegatedTrialComposer pending={item.pending} conversations={currentThreads} busy={!!busy} ready={host?.state === "ready" && host?.generationClosed !== true} act={trialAct} />
        : <BringBackComposer pending={item.pending} conversations={currentThreads} busy={!!busy} ready={host?.state === "ready" && host?.generationClosed !== true} act={trialAct} />}
    </div>)}
    <NativeActivityView navigationRef={activityNavigationRef} key={`activity:${JSON.stringify([selected?.generation, selected?.threadId])}`} view={host?.nativeView} threadId={selected?.threadId} runs={runs} offers={offers}
      trialTurns={workflowRoot?.trialTurns} trialChildren={workflowRoot?.trialChildren} delegation={selected?.delegation}
      stopLabelFor={(thread, turn) => stopLabel(host?.codexStops, thread, turn, host?.stopRequests, appHome(host?.homeRouting?.activeModeHomeClass))}
      renderOffer={offer => <RunOffer offer={offer} generation={host?.generation} ready={host?.state === "ready"} busy={offerBusy} act={offerAct} />} />
    {selected && <div id="conversation-requests" aria-label="Requests from Codex in this conversation">
      <h3>Requests from Codex in this conversation ({requests.filter(answerable).length} waiting)</h3>
      {ordered.length === 0 && <p>No requests from Codex in this conversation.</p>}
      {ordered.map((request: Json) => <NativeRequestCard activityLink={activityLink} key={JSON.stringify([request.generation, request.requestIdentity])} request={request} view={host?.nativeView} answer={answer} readRequest={readRequest} place={requestPlace(request, host, appProjectFolder(host))} observation={replyObservations?.[requestScopeKey(request)]} />)}
    </div>}
    <p id="ordinary-send-readiness" role="status" aria-live="polite">{sendReadiness}</p>
    {!sourceReady && <p><a href="#workspace-connection">Open connection controls</a></p>}
    {sourceReady && !selected && <p><a href="#workspace-start">Choose a new conversation</a>{" · "}<a href="#workspace-history">Find a past conversation</a></p>}
    {heldOffer && heldOffer.threadKey === threadKey && <p role="status" aria-label="Prepared workflow request">A workflow-draft request is ready for this conversation. Your unsent text is kept.{" "}
      <button disabled={!!busy} onClick={() => { textRevision.current += 1; textWrittenFor.current = heldOffer.threadKey; setText(heldOffer.text); setHeldOffer(null); }}>Replace my text with the request</button>{" "}
      <button onClick={() => setHeldOffer(null)}>Discard the request</button></p>}
    {unconfirmed.length > 0 && <div aria-label="Unconfirmed messages">{unconfirmed.map(row => {
      const shownHere = !!selected && row.request.threadId === selected.threadId;
      const sameSource = shownHere && JSON.stringify(row.request.generation) === JSON.stringify(selected.generation);
      const loaded = currentThreads.find((t: Json) => t.threadId === row.request.threadId && JSON.stringify(t.generation) === JSON.stringify(row.request.generation));
      const destination = sameSource ? "this conversation" : loaded ? conversationLabel(host, loaded) : `conversation ${row.request.threadId} in a Codex session that isn't loaded now`;
      return <div key={row.id} role={row.acknowledged ? "note" : "alert"} tabIndex={-1} ref={node => { if (node && shownHere && !announcedUnconfirmed.current.has(row.id)) { announcedUnconfirmed.current.add(row.id); node.focus?.({ preventScroll: false }); } }}>
        <p><strong>Your message to {destination} may have been sent.</strong> The App couldn't confirm it, so it isn't resent and its text was not cleared.{row.acknowledged ? " You've said you read that conversation; sending there again is allowed." : " Sending to that conversation again is held until you've read it."}</p>
        {shownHere && !sameSource && <p><small>Codex or the home has changed since that send. The conversation shown now has the same ID, so sending to it is held too; that doesn't make the earlier destination this one.</small></p>}
        {!row.acknowledged && <p><button onClick={() => setUnconfirmed(rows => rows.map(r => r.id === row.id ? { ...r, acknowledged: true } : r))}>I've read that conversation — allow sending again</button> <small>Sends nothing; this record stays.</small></p>}
        <details><summary>The message and what was reported</summary><pre style={{ whiteSpace: "pre-wrap" }}>{row.request.text}</pre>
          <p><small>Mode {row.request.mode ?? "not overridden"} · model {row.request.model ?? "not chosen"} · conversation <code>{row.request.threadId}</code> in Codex session {String(row.request.generation?.spawnCounter ?? "")} of home {String(row.request.generation?.home ?? "")}.</small></p>
          <p><small>Reported: {row.reported}</small></p></details>
      </div>;
    })}</div>}
    {text && selected && textWrittenFor.current && textWrittenFor.current !== threadKey && <p role="note" aria-label="Where your text goes">Your unsent text was written while another conversation was shown. It is kept; if you send it now it goes to {conversationLabel(host, selected)}.</p>}
    <p><label>Text <textarea id="ordinary-composer-text" ref={composerField} aria-describedby="ordinary-send-readiness" disabled={!!busy} value={text} onChange={e => { textRevision.current += 1; textWrittenFor.current = threadKey; setText(e.target.value); }} rows={4} style={{ display: "block", width: "100%" }} /></label></p>
    <button className="setup-primary" aria-describedby="ordinary-send-readiness" disabled={!sourceReady || !selected || !text || !!busy || unconfirmed.some(row => !row.acknowledged && row.request.threadId === selected?.threadId)} onClick={() => { void sendText(); }}>{(host?.attachmentSelections?.selections ?? []).length > 0 ? "Send text only" : "Send text"}</button>
    <details className="conversation-model-options"><summary>Model and effort{ordinaryModel.owner === ordinaryOwner && ordinaryModel.effort ? ` · next send: ${ordinaryModel.effort}` : ""}</summary>
    <p><label>Optional model identifier for next ordinary text turn <input {...EXACT_TEXT} disabled={!selected || !!busy} value={ordinaryModelValue}
      onChange={e => setOrdinaryModel(current => ({ owner: ordinaryOwner, value: e.target.value, effort: "", effortModel: "", revision: current.revision + 1 }))} aria-describedby="ordinary-model-help" /></label></p>
    <p id="ordinary-model-help">Applies to Send text and the plan/default text controls below. Empty keeps the existing native model choice. An explicit identifier overrides the model for this turn and subsequent native turns; clearing this field does not revert it. Attachment, steering and prepared-message sends do not use this field.</p>
    <OfferedEffortChoice owner={ordinaryOwner} threadId={selected?.threadId ?? ""} generation={selected?.generation} homeClass={host?.homeRouting?.activeModeHomeClass ?? null}
      modelProvider={selected?.modelProvider ?? ""} entryId={selected?.requestedDestination?.entryId ?? (selected?.modelProvider === "openai" ? (host?.homeRouting?.activeModeHomeClass === "api-key" ? "api-key" : "chatgpt-account") : "local-provider")}
      model={ordinaryModelValue} effort={ordinaryModel.owner === ordinaryOwner ? ordinaryModel.effort : ""} disabled={!sourceReady || !selected || !!busy}
      choose={(effort, effortModel) => setOrdinaryModel(current => ({ ...current, owner: ordinaryOwner, effort, effortModel, revision: current.revision + 1 }))} />
    </details>
    {selected && <PlanModeControl planMode={host?.planMode} requested={(host?.requestedModes ?? []).find((r: Json) => JSON.stringify(r.generation) === generationKey && r.threadId === selected.threadId) ?? null}
      ready={sourceReady} busy={!!busy} hasText={!!text && !unconfirmed.some(row => !row.acknowledged && row.request.threadId === selected.threadId)}
      check={() => { setError(""); checkPlanMode(selected.generation).catch(e => setError(String(e))); }} send={mode => { void sendText(mode); }} />}
    {(host?.attachmentSelections?.selections ?? []).length > 0 && <p>This plain-text action excludes the selected attachments. Use the explicit ordered-attachment action to include the entire private selection.</p>}
    <p>Text is sent unchanged to the selected native conversation. Its role, access entry, provider and home remain the conversation's existing settings; a model choice opens no new run.</p>
    {ordinaryOutcome && <div aria-label="Ordinary text submission outcome">
      <details><summary>Original message destination and choices</summary><p>Original ordinary text turn · conversation {ordinaryOutcome.request.threadId} · Home {ordinaryOutcome.request.generation.home} · App session {ordinaryOutcome.request.generation.appSession} · spawn {ordinaryOutcome.request.generation.spawnCounter} · {ordinaryOutcome.request.mode ?? "no mode override"} · requested model {ordinaryOutcome.request.model ?? "no override"} · requested effort {ordinaryOutcome.request.effort ?? "no override"}.</p></details>
      {ordinaryOutcome.result.acknowledged
        ? <p role="status">Native turn/start response received. Model adoption, execution and completion remain unestablished; reported model facts are separate.</p>
        : <p role="alert">{String(ordinaryOutcome.result.nativeError)} Text and model choice retained unless superseded by a newer edit or conversation. No automatic retry or substitution.</p>}
      {ordinaryOutcome.observationLimit && <p role="alert">{observationLine(ordinaryOutcome.observationLimit, "Ordinary text view refresh unavailable for this original request: ")} The command outcome above is unchanged; no automatic resend.</p>}
    </div>}
    {(host?.attachmentSelections?.selections ?? []).length > 0 && <div>
      <button disabled={!sourceReady || !selected || !!busy || host?.attachmentCustody?.state !== "opened"} onClick={() => attachmentText(null)}>Send text and ordered attachments</button>{" "}
      <button disabled={!sourceReady || !selected || !steeringTarget || !!busy || host?.attachmentCustody?.state !== "opened"} onClick={() => attachmentText(steeringTarget.turnId)}>Steer current turn with ordered attachments</button>
      <p>Every selected source is revalidated as one whole list. Source/custody/context failures retain the draft and evidence; no text-only fallback or automatic resend. Native acknowledgments remain separate from completion and provider uptake.</p>
      {host?.attachmentCustody?.state !== "opened" && <p>Attachment custody unavailable: {host?.attachmentCustody?.error}. Plain-text controls remain available.</p>}
    </div>}
    {attachmentOutcome && <div aria-label="Attachment submission outcome">
      <p>Original {attachmentOutcome.request.expectedTurnId === null ? "Send" : "Steer"} with ordered attachments · conversation {attachmentOutcome.request.threadId} · Home {attachmentOutcome.request.generation?.home}{attachmentOutcome.request.expectedTurnId !== null && ` · expected turn ${attachmentOutcome.request.expectedTurnId}`}.</p>
      {attachmentOutcome.result.acknowledged
        ? <p role="status">Matching attachment native acknowledgment observed; provider uptake and completion remain unestablished.</p>
        : <p role="alert">{String(attachmentOutcome.result.nativeError)} No automatic retry.</p>}
      {attachmentOutcome.observationLimit && <p role="alert">{observationLine(attachmentOutcome.observationLimit, "Attachment view refresh unavailable for this original request: ")} The command outcome above is unchanged; no automatic resend.</p>}
      <details><summary>Original attachment request identity</summary>
        <p>App session: {attachmentOutcome.request.generation?.appSession} · spawn: {attachmentOutcome.request.generation?.spawnCounter} · selection owner: {attachmentOutcome.request.ownerRef} · list revision: {attachmentOutcome.request.listRevision}.</p>
        <ol>{attachmentOutcome.request.selectionRefs.map((ref, index) => <li key={`${index}:${ref}`}>{ref}</li>)}</ol>
      </details>
    </div>}
    <SteeringControl target={steeringTarget} reason={steering?.reason} ready={sourceReady && !!selected} busy={!!busy} text={text} submit={() => { void steerText(); }} />
    <section aria-label="Turn interruption"><h3>Interrupt a live turn</h3>
    <p id="conversation-interrupt-readiness" role="status" aria-live="polite">{interruptReadiness}</p>
    <label>Observed live turn <select disabled={!!ownBusy} value={turnId} onChange={e => setTurnId(e.target.value)}><option value="">Select a live turn</option>{liveTurns.map((turn: Json) => <option key={turn.turnId} value={turn.turnId}>{turn.turnId} · {turn.nativeTurn.status}</option>)}</select></label>{" "}
    <button aria-describedby="conversation-interrupt-readiness" disabled={!sourceReady || !live || !!ownBusy || alreadyRequested} onClick={interruptTurn}>Interrupt selected live turn</button>
    <p>An interrupt acknowledgment does not establish turn end or rollback. Turn status comes from native observations.</p>
    {(host?.conversationTurns ?? []).filter((turn: Json) => turn.terminalEventObserved && turn.nativeTurn?.status === "inProgress").map((turn: Json) => <p key={JSON.stringify([turn.generation, turn.threadId, turn.turnId])}>Native turn inconsistency: {turn.threadId}/{turn.turnId} has a terminal event observation and contradictory progress status; interruption is unavailable.</p>)}
    {(host?.conversationTurns ?? []).flatMap((turn: Json) => (turn.inconsistencyLimits ?? []).map((limit: Json, index: number) => <p key={JSON.stringify([turn.generation, turn.threadId, turn.turnId, index])}>Native lifecycle limit for {JSON.stringify(turn.generation)} · {turn.threadId}/{turn.turnId}: {JSON.stringify(limit)}</p>))}
    </section>
    {ownBusy && <p>{ownBusy}: waiting for protocol response; no automatic retry.</p>}
    {!ownBusy && codexBusy && <p>Stop or Restart Codex is in progress: sending text, steering and attachments is paused; interrupting a live turn stays available.</p>}
    {error && <p role="alert">{error} No automatic retry.</p>}
    <p>Text-turn protocol requests: {host?.modelTurnEvidence?.protocolRequests?.length ?? 0}. {host?.modelTurnEvidence?.standing ?? "Provider/model execution is not established by this view."}</p>
    <details><summary>Observed native turns, steering and interrupt request state</summary><pre style={{ whiteSpace: "pre-wrap" }}>{JSON.stringify({ turns: host?.conversationTurns, steeringTargets: host?.steeringTargets, steeringRequests: (host?.clientRequests ?? []).filter((request: Json) => request.method === "turn/steer"), interrupts: host?.turnInterruptRequests, protocolEvidence: host?.modelTurnEvidence }, null, 2)}</pre></details>
  </section>;
}

type ContinueNavigation = { isCurrent: () => boolean; observe: () => Promise<Json> };
type ContinueNavigationTicket = {
  generation: Json; epoch: number; threadId: string; requestRef: string;
  resolution: string; previousResolution: string | undefined; threadKey: string;
  operation: number; navigation: ContinueNavigation;
};

export function HistoryPanel({ host, refresh, threadKey, setThreadKey, captureContinueNavigation, openConversation, searchHint }: { openConversation?: (key: string) => void; searchHint?: { sequence: number; text: string } | null;
  host: Json; refresh: () => Promise<Json>; threadKey: string; setThreadKey: (key: string) => void;
  captureContinueNavigation: (generation: Json, historyCurrent: (history: Json) => boolean) => ContinueNavigation;
}) {
  const [busy, setBusy] = useState(false);
  const busyRef = useRef(false);
  const [error, setError] = useState("");
  const [continueNotice, setContinueNotice] = useState("");
  const [pendingContinue, setPendingContinue] = useState<ContinueNavigationTicket | null>(null);
  const operation = useRef(0);
  const activeNavigation = useRef<ContinueNavigation | null>(null);
  const [direction, setDirection] = useState("desc");
  const [search, setSearch] = useState("");
  const searchInput = useRef<HTMLInputElement>(null);
  const [progress, setProgress] = useState("");
  const history = host?.nativeHistory;
  const selected = history?.selected;
  const generation = history?.generation;
  const epoch = history?.selectionEpoch;
  const available = host?.state === "ready" && history?.state === "history-receiving" && JSON.stringify(generation) === JSON.stringify(host?.generation);
  const searchSource = JSON.stringify([history?.home, generation]);
  useEffect(() => { setSearch(""); }, [searchSource]);
  // A saved conversation ID from elsewhere (e.g. a draft's trial) only fills
  // the local search, which reads nothing: no history read, selection, home
  // change or Continue happens until the person does it here.
  const [hintShown, setHintShown] = useState("");
  useEffect(() => {
    if (!searchHint) return;
    setSearch(searchHint.text); setHintShown(searchHint.text);
    searchInput.current?.scrollIntoView?.({ block: "center" });
    searchInput.current?.focus?.({ preventScroll: true });
  }, [searchHint?.sequence]); // eslint-disable-line react-hooks/exhaustive-deps
  const received = (history?.threads ?? []) as Json[];
  const query = search.trim().toLocaleLowerCase();
  const matches = received.filter(row => [row.native.name, row.native.id, row.native.preview].some(value => typeof value === "string" && value.toLocaleLowerCase().includes(query)));
  const outsideFilter = !!selected?.threadId && !matches.some(row => row.native.id === selected.threadId);
  const retainedSelection = outsideFilter ? received.find(row => row.native.id === selected.threadId) : null;
  const selectedDescription = received.find(row => row.native.id === selected?.threadId)?.native ?? selected?.metadata?.thread;
  const guidance = !available ? "Connect to the selected Codex home to read stored conversations."
    : busy ? progress : !selected ? "Read stored conversations, then choose one to inspect. Reading does not open it for new messages."
    : "Read turns to inspect prior work. Use Continue only when you want to open this conversation for new messages.";
  const turnPage = historyPageBinding(host, "turns");
  const itemPage = historyPageBinding(host, "items");
  const same = (a: Json, b: Json) => JSON.stringify(a) === JSON.stringify(b);
  // Only identity/revision metadata is retained across an observer failure.
  // The returned resume body, transcript and native role hints stay out of it.
  const admissionTicket = (result: Json, priorRequests: Set<unknown>, navigation: ContinueNavigation, requestOperation: number): ContinueNavigationTicket | null => {
    const resolution = result?.selected?.streamResolutions?.["thread-state"];
    const query = resolution?.query;
    const previous = selected?.streamResolutions?.["thread-state"];
    const positive = (value: Json) => Number.isSafeInteger(value) && value > 0;
    if (!positive(epoch) || !positive(resolution?.revision) || resolution.revision <= (previous?.revision ?? 0)
      || resolution.outcome !== "native-result-observed" || !positive(query?.factory_id) || !positive(query?.query_id)
      || query.home !== generation?.home || !same(query.generation, generation) || query.method !== "thread/resume"
      || !query.params || Object.keys(query.params).length !== 2
      || query.params.threadId !== selected?.threadId || query.params.excludeTurns !== true) return null;
    const dispatch = (result?.dispatches ?? []).find((row: Json) => typeof row.requestRef === "string" && row.requestRef && !priorRequests.has(row.requestRef)
      && row.writeResult === "written" && row.outcome === "response-observed-result" && row.sourceCurrent === true
      && row.home === generation?.home && same(row.generation, generation) && same(row.localQuery, query));
    const admitted = dispatch?.activeAdmission;
    if (admitted?.nativeResumeObserved !== true || admitted.resumeRequestRef !== dispatch.requestRef
      || typeof admitted.threadId !== "string" || !admitted.threadId || admitted.threadId !== selected?.threadId
      || !admitted.generation || !same(admitted.generation, generation) || !same(result?.generation, generation)
      || result?.home !== generation?.home || result?.selectionEpoch !== epoch || result?.selected?.threadId !== admitted.threadId
      || result.selected.state !== "resume-response-observed" || result.selected.resumeEligibilityCurrent !== true) return null;
    return { generation: { appSession: generation.appSession, home: generation.home, spawnCounter: generation.spawnCounter },
      epoch, threadId: admitted.threadId, requestRef: dispatch.requestRef, resolution: JSON.stringify(resolution),
      previousResolution: JSON.stringify(previous), threadKey, operation: requestOperation, navigation };
  };
  useEffect(() => {
    // Check even while the command/observer is in flight. Once invalidated, a
    // token cannot regain currency after an away-and-back source or UI choice.
    activeNavigation.current?.isCurrent();
    if (!pendingContinue) return;
    const ticket = pendingContinue;
    const currentHistory = host?.nativeHistory, currentSelected = currentHistory?.selected;
    const cancel = () => {
      setPendingContinue(null);
      setContinueNotice("Continue admission was confirmed; a newer choice or changed source superseded its navigation. No automatic retry.");
    };
    if (ticket.operation !== operation.current || !ticket.navigation.isCurrent() || threadKey !== ticket.threadKey
      || host?.state !== "ready" || host.generationClosed === true || !same(host.generation, ticket.generation)
      || currentHistory?.state !== "history-receiving" || currentHistory.home !== ticket.generation.home
      || !same(currentHistory.generation, ticket.generation) || currentHistory.selectionEpoch !== ticket.epoch
      || currentSelected?.threadId !== ticket.threadId) { cancel(); return; }
    const currentResolution = JSON.stringify(currentSelected.streamResolutions?.["thread-state"]);
    if (currentResolution !== ticket.resolution) {
      const accepted = JSON.parse(ticket.resolution), waiting = currentSelected.streamResolutions?.["thread-state"];
      const originalPending = waiting?.outcome === "pending" && waiting.revision === accepted.revision && same(waiting.query, accepted.query);
      // A failed observation can leave the pre-command view or the original
      // pending query rendered. Neither supplies admission; wait for acceptance.
      // Any other query/revision supersedes it; it is never a stale fallback.
      if (currentResolution !== ticket.previousResolution && !originalPending) cancel();
      return;
    }
    if (currentSelected.state !== "resume-response-observed" || currentSelected.resumeEligibilityCurrent !== true) { cancel(); return; }
    if (!(host.threads ?? []).some((row: Json) => row.threadId === ticket.threadId && same(row.generation, ticket.generation)
      && row.nativeResumeObserved === true && row.resumeRequestRef === ticket.requestRef)) return;
    setPendingContinue(null);
    activeNavigation.current = null;
    const admitted = (host.threads ?? []).find((row: Json) => row.threadId === ticket.threadId && same(row.generation, ticket.generation));
    setContinueNotice(`Continue admission confirmed; opened ${admitted ? conversationLabel(host, admitted) : "the matched conversation"} in Conversation. Nothing was sent.`);
    setError("");
    // Show the admitted conversation itself, with its message box focused.
    const key = JSON.stringify([ticket.generation, ticket.threadId]);
    if (openConversation) openConversation(key); else setThreadKey(key);
  });
  const captureHistoryCurrency = () => {
    const source = JSON.stringify(generation), home = history?.home, selectionEpoch = epoch, threadId = selected?.threadId;
    const previous = selected?.streamResolutions?.["thread-state"];
    const previousResolution = JSON.stringify(previous), previousRevision = previous?.revision ?? 0;
    const identity = (resolution: Json) => JSON.stringify({ query: resolution?.query, revision: resolution?.revision });
    let observed: string | undefined, returned: string | undefined;
    return {
      // This comes only from admissionTicket's matched original result. Merely
      // observing a prospective query never supplies an admission or a ticket.
      admitted: (resolution: string) => { returned = identity(JSON.parse(resolution)); },
      isCurrent: (shown: Json) => {
        if (shown?.state !== "history-receiving" || shown.home !== home || JSON.stringify(shown.generation) !== source
          || shown.selectionEpoch !== selectionEpoch || shown.selected?.threadId !== threadId) return false;
        const resolution = shown.selected.streamResolutions?.["thread-state"];
        if (JSON.stringify(resolution) === previousResolution) return observed === undefined;
        const query = resolution?.query;
        if (!Number.isSafeInteger(resolution?.revision) || resolution.revision <= previousRevision
          || !Number.isSafeInteger(query?.factory_id) || query.factory_id <= 0 || !Number.isSafeInteger(query?.query_id) || query.query_id <= 0
          || query.home !== home || JSON.stringify(query.generation) !== source || query.method !== "thread/resume"
          || !query.params || Object.keys(query.params).length !== 2 || query.params.threadId !== threadId || query.params.excludeTurns !== true
          || !["pending", "native-result-observed"].includes(resolution.outcome)) return false;
        const current = identity(resolution);
        if ((returned !== undefined && returned !== current) || (observed !== undefined && observed !== current)) return false;
        // One original resume may progress from pending to accepted at this
        // exact query/revision. A newer query or a return to the baseline is
        // supersession, even while the command or its observer is still waiting.
        observed = current;
        return true;
      }
    };
  };
  const run = async (action: string, cursor: string | null = null, reference: string | null = null, pagingDirection = direction) => {
    if (busyRef.current) return;
    busyRef.current = true;
    const requestOperation = ++operation.current;
    setPendingContinue(null);
    const historyCurrency = action === "continue" ? captureHistoryCurrency() : null;
    const navigation = historyCurrency ? captureContinueNavigation(generation, historyCurrency.isCurrent) : null;
    activeNavigation.current = navigation;
    setContinueNotice("");
    setBusy(true); setError("");
    setProgress(({ list: "Reading stored conversations…", metadata: "Reading conversation details…", turns: "Reading turns…", items: "Reading messages and activity…", goal: "Reading the conversation goal…", child: "Reading child conversation details…", continue: "Waiting for this conversation to be admitted for continuation…" } as Record<string, string>)[action] ?? "Waiting for the history request…");
    const priorRequests = new Set((history?.dispatches ?? []).map((dispatch: Json) => dispatch.requestRef));
    let ticket: ContinueNavigationTicket | null = null;
    try {
      const result: Json = await invoke("history_action", { generation, selectionEpoch: epoch, action, cursor, direction: pagingDirection, reference });
      if (navigation) {
        ticket = admissionTicket(result, priorRequests, navigation, requestOperation);
        if (ticket) historyCurrency!.admitted(ticket.resolution);
      }
    }
    catch (e) { setError(String(e)); }
    finally {
      await refreshAfterAction(async () => { if (navigation) await navigation.observe(); else await refresh(); }, () => setError(withRefreshFailure));
      if (navigation) {
        setPendingContinue(ticket);
        setContinueNotice(ticket ? "Continue admission confirmed; waiting for its matched current conversation view. No automatic retry."
          : "No matched Continue admission was returned. The conversation selection is retained; no automatic retry.");
      }
      busyRef.current = false;
      setBusy(false); setProgress("");
    }
  };
  const select = async (threadId: string) => {
    if (!threadId || busyRef.current) return;
    busyRef.current = true;
    operation.current++;
    activeNavigation.current = null;
    setPendingContinue(null); setContinueNotice("");
    setBusy(true); setError(""); setProgress("Selecting the stored conversation for inspection…");
    try { await invoke("history_select", { generation, selectionEpoch: epoch, threadId }); }
    catch (e) { setError(String(e)); }
    // The selection's own error stands; a failed refresh adds the fixed line once and nothing raw.
    finally { await refreshAfterAction(refresh, () => setError(withRefreshFailure)); busyRef.current = false; setBusy(false); setProgress(""); }
  };
  const pageButtons = (action: string, page: Json, reference: string | null = null, pageDirection = direction) => <span className="history-pagination">
    {typeof page?.nextCursor === "string" && <button aria-label={`Next ${action === "list" ? "conversations" : action} page`} disabled={!available || busy} onClick={() => run(action, page.nextCursor, reference, pageDirection)}>Next page</button>}
    {typeof page?.backwardsCursor === "string" && <button aria-label={`Previous ${action === "list" ? "conversations" : action} page`} disabled={!available || busy} onClick={() => run(action, page.backwardsCursor, reference, pageDirection === "desc" ? "asc" : "desc")}>Previous page</button>}
    <small> Cursor: {page === null || page === undefined ? "not read" : page.nextCursor === null ? "exhausted" : page.nextCursor === undefined ? "not reported" : "available"}</small>
  </span>;
  return <section aria-label="Stored conversations" aria-busy={busy}>
    <h2>Find a past conversation</h2>
    <p id="history-guidance" role="status" aria-live="polite">{guidance}</p>
    {!available && <p><a href="#workspace-connection">Open connection controls</a></p>}
    <div className="history-browser">
    <p>These disposable pages come from the selected native home. Reading history does not make a conversation operational. Original App role evidence remains unknown after a cold App restart.</p>
    <label>Page direction <select value={direction} disabled={busy} onChange={e => setDirection(e.target.value)}><option value="desc">Newest first</option><option value="asc">Oldest first</option></select></label>{" "}
    <button aria-describedby="history-guidance" disabled={!available || busy} onClick={() => run("list")}>Read stored conversations</button>{" "}{pageButtons("list", history?.listPage, null, history?.listDirection ?? direction)}
    {hintShown && search === hintShown && <p role="note" aria-label="Searching for a saved conversation">Looking for <code>{hintShown}</code>, an ID saved with an earlier trial. It is only a search: nothing is read, chosen or continued. If it isn't among the received conversations, it may be in another home; choose that home under Connection &amp; access, read its history, then search again.</p>}
    <div className="history-search">
      <label>Find in received conversations <input ref={searchInput} type="search" aria-describedby="history-search-count" value={search} onChange={event => setSearch(event.target.value)} /></label>
      <button disabled={!search} onClick={() => { setSearch(""); searchInput.current?.focus?.(); }}>Clear search</button>
    </div>
    <p id="history-search-count" className="history-hint" role="status">{matches.length} matching of {received.length} received conversations. Search checks received names, previews and IDs only; it does not fetch other pages.</p>
    {received.length === 0 && <p>{history?.listPage ? "No conversation rows are available from the received list. Other pages or homes may contain more." : "No conversations have been received here yet. Select Read stored conversations to request a page."}</p>}
    {query && matches.length === 0 && received.length > 0 && <p>No received conversation matches. Clear the search or explicitly read another page.</p>}
    <p><label>Stored conversation <select aria-describedby="history-guidance history-search-count" value={selected?.threadId ?? ""} disabled={!available || busy} onChange={e => select(e.target.value)}><option value="">Select a received conversation</option>{matches.map((row: Json) => <option key={row.native.id} value={row.native.id}>{conversationTitle(row.native, "Untitled conversation")} · {row.native.status?.type ?? "status not reported"}</option>)}{outsideFilter && <option value={selected.threadId}>{conversationTitle(retainedSelection?.native ?? selectedDescription, "Selected conversation")} · selected{retainedSelection ? " — outside this search" : " — not in the received list"}</option>}</select></label></p>
    {outsideFilter && <p>The selected conversation stays selected. Filtering does not change which conversation you inspect or continue.</p>}
    {history?.listError && <p role="alert">The conversation list could not be refreshed. Received rows are retained observations, not a successful refresh. See History dispatch and pending/error evidence below for the source error.</p>}
    </div>
    {selected && <>
      <h3>Inspect selected conversation: {conversationTitle(selectedDescription, "Untitled conversation")}</h3>
      <details><summary>Conversation source and role details</summary>
      <p>Conversation ID: <code>{selected.threadId}</code>.</p>
      <p>History state: {selected.state}. App role in force: {JSON.stringify(selected.appRole)}. Native agentRole: {JSON.stringify(selected.metadata?.thread?.agentRole === undefined ? { state: "not reported" } : selected.metadata.thread.agentRole)}.</p></details>
      {(selected.futureGuidanceNotices ?? []).map((notice: Json) => <p key={notice.path}>{notice.path}: {notice.kind === "not-read" ? `current guidance not compared (${notice.reason})` : notice.reason}; new conversations use the current guidance. This conversation retains its original role.</p>)}
      <button disabled={!available || busy} onClick={() => run("metadata")}>Read metadata</button>{" "}
      <button disabled={!available || busy} onClick={() => run("turns")}>Read turns</button>{" "}
      <button disabled={!available || busy} onClick={() => run("goal")}>Read goal</button>{" "}
      <button aria-describedby="history-guidance" disabled={!available || busy} onClick={() => run("continue")}>Continue selected conversation</button>
      <p>Current resume eligibility: {String(selected.resumeEligibilityCurrent ?? false)}. Active admission is reported in the dispatch evidence below and the operational conversation selector.</p>
      <p>Continue sends the native thread ID and waits for a matching resume response before active admission. Its existing guidance and settings remain in force. No automatic resend.</p>
      <p>Goal: {selected.goalAvailability}. {selected.goal?.goal === null ? "Native reported no goal." : selected.goal ? JSON.stringify(selected.goal.goal) : "Goal has not been read."}</p>
      <p>{selected.checklists}</p>
      <h3>Turns</h3>{turnPage.accepted && pageButtons("turns", turnPage.page, null, turnPage.query.params.sortDirection)}
      <StoredTurnPage binding={turnPage} canRead={available && !busy} readItems={turn => run("items", null, turn)} />
      <h3>Selected item page</h3>{itemPage.accepted && pageButtons("items", itemPage.page, itemPage.query.params.turnId, itemPage.query.params.sortDirection)}
      <StoredItemPage binding={itemPage} />
      <h3>Native child references</h3>
      {(selected.knownChildren ?? []).map((child: Json) => <p key={child.threadId}>{child.threadId} · source {child.sourceItemId} <button disabled={!available || busy} onClick={() => run("child", null, child.threadId)}>Read child metadata</button></p>)}
      <details><summary>Metadata, child reads, standalone receiver references and stream errors</summary><pre style={{ whiteSpace: "pre-wrap" }}>{JSON.stringify({ metadata: selected.metadata, childReads: selected.childReads, receiverReferences: selected.receiverReferences, errors: selected.errorsByStream, errorHistory: selected.errorHistory, resolutions: selected.streamResolutions, resumeEligibilityCurrent: selected.resumeEligibilityCurrent }, null, 2)}</pre></details>
      {selected.originalRoleSupply && <details><summary>Original App role supply evidence (memory only; adoption unknown)</summary><pre style={{ whiteSpace: "pre-wrap" }}>{JSON.stringify(selected.originalRoleSupply, null, 2)}</pre></details>}
    </>}
    {busy && <p role="status">{progress} No automatic retry.</p>}
    {continueNotice && <p role="status">{continueNotice}</p>}
    {error && <p role="alert">{error}</p>}
    {(history?.receivingLimits ?? history?.limits ?? []).map((limit: string, index: number) => <p key={index}>{limit}</p>)}
    <details><summary>History dispatch and pending/error evidence</summary><pre style={{ whiteSpace: "pre-wrap" }}>{JSON.stringify({ generation, selectionEpoch: epoch, listError: history?.listError, pending: history?.pending, dispatches: history?.dispatches, originalStartReceipts: history?.startReceipts }, null, 2)}</pre></details>
  </section>;
}

function ExternalObservationPanel({ data, select }: { data: Json; select: () => Promise<void> }) {
  const observation = data?.observation;
  const evidence = (key: string, title: string) => {
    const document = observation?.[key];
    if (!document) return <p key={key}>{title}: not supplied; no comparison established.</p>;
    return <article key={key} style={{ borderTop: "1px solid #ccc", paddingTop: 8 }}>
      <h3>{title} · {document.assessment}</h3>
      <p>Selected file: {document.displayPath}</p>
      {document.pathDisplayLimit && <p>Path display limit: {document.pathDisplayLimit}</p>}
      <details><summary>Exact selected native path identity</summary><pre>{JSON.stringify(document.selectedPath, null, 2)}</pre></details>
      {document.reason && <p>Receiving limit: {document.reason}</p>}
      <h4>Complete supplied JSON: tables, basis, diagnostics and standing retained</h4>
      {document.originalDocument !== null ? <pre style={{ whiteSpace: "pre-wrap" }}>{JSON.stringify(document.originalDocument, null, 2)}</pre> : <p>No parsed JSON available; see the receiving assessment.</p>}
      <details><summary>Original bytes retained in App memory ({document.originalBytes?.length ?? "unavailable"})</summary><pre style={{ whiteSpace: "pre-wrap" }}>{JSON.stringify(document.originalBytes)}</pre></details>
    </article>;
  };
  return <section>
    <h2>Supplied external observation</h2>
    <p>Choose a catalog and read document, with an optional counterpart. Documents remain in App memory for this session.</p>
    <button disabled={data?.selection?.state === "selecting"} onClick={select}>Select observation documents…</button>
    <p>Selection: {data?.selection?.state ?? "not-selected"} {data?.selection?.stage ?? ""} {data?.selection?.reason ?? ""}</p>
    {data?.selection?.previousObservationRetained && <p>The previous supplied observation is retained.</p>}
    {observation && <>
      <p>{observation.provenance} · host origin: {observation.hostOrigin} · qualification: {observation.qualification}</p>
      <p>Currency: {JSON.stringify(observation.reportedCurrency)} ({observation.currencyMeaning}) · basis citation: {observation.basisCitationAssessment ?? "not established"}</p>
      <p>Comparison: {observation.comparison} · scope: {observation.comparisonScope}. A supplied counterpart is not verified host evidence.</p>
      {observation.comparison === "host_table_not_supplied" && <p>No counterpart supplied; comparison not established.</p>}
      <p>Dispatch: {observation.dispatch}</p>
      <p>Evidence limits: {JSON.stringify(observation.evidenceLimits)}</p>
      {evidence("catalog", "Supplied catalog")}
      {evidence("read", "Supplied read")}
      {evidence("counterpart", "Optional supplied counterpart")}
      <details><summary>Complete reported receiving snapshot</summary><pre style={{ whiteSpace: "pre-wrap" }}>{JSON.stringify(observation, null, 2)}</pre></details>
    </>}
  </section>;
}

// V14 F1/F5: while a native confirmation is open and names content by digest
// (a logout assessment, an A16 alternative, a request answer, an attachment
// comparison or an A15 review), the host publishes that content here so the
// person can read it whole. Read-only; it is withdrawn when the alert closes.
function NativeConfirmationContent() {
  const [shown, setShown] = useState<Json[]>([]);
  const [checks, setChecks] = useState<Record<string, string>>({});
  useEffect(() => {
    let live = true;
    const poll = () => invoke<Json[]>("native_confirmation_content").then(async (rows) => {
      if (!live) return;
      setShown(rows ?? []);
      const next: Record<string, string> = {};
      for (const row of rows ?? []) {
        try { next[row.digest] = (await reviewDigest(row.content)) === row.digest ? "This view recomputed the same digest from the content below." : "This view recomputed a different digest: do not rely on this view; cancel the native confirmation."; }
        catch (e) { next[row.digest] = `This view cannot recompute it (${e instanceof Error ? e.message : String(e)}).`; }
      }
      if (live) setChecks(next);
    }).catch(() => undefined);
    poll();
    const t = setInterval(poll, 1000);
    return () => { live = false; clearInterval(t); };
  }, []);
  if (!shown.length) return null;
  return <section role="region" aria-label="Content named by an open native confirmation" style={{ border: "2px solid #a60", padding: 8 }}>
    <h2>Content named by an open native confirmation</h2>
    {shown.map((row: Json) => <article key={row.digest}>
      <h3>{row.kind}</h3>
      <p>sha-256 digest, as named in the native confirmation: <code style={{ userSelect: "all", overflowWrap: "anywhere" }}>{row.digest}</code>. {checks[row.digest] ?? ""} {DIGEST_LIMIT}</p>
      {row.kind === "A15 complete review" && Array.isArray(row.content?.entries) && row.content.entries.every((entry: Json) => entry !== null && typeof entry === "object" && !Array.isArray(entry))
        ? <WorkflowRegistrationReview presentation={row.content} />
        : <pre style={{ whiteSpace: "pre-wrap" }}>{JSON.stringify(readablePaths(row.content), null, 2)}</pre>}
    </article>)}
  </section>;
}

/** The status line under the workflow panel after a press. The result of
 * pre-filling a trial or a bring-back is not echoed: its pre-filled or
 * sent state is shown, current, by the conversation panel and the draft list,
 * and a copy here would go stale (trial witness 2026-10-10 (d)). Read again
 * and other non-prefill results keep their reported outcomes and limits. */
const PREFILL_RESULTS = new Set(["workflow_trial_prepare", "workflow_trial_again", "workflow_trial_bring_back", "workflow_run_bring_back"]);
export function workflowActionMessage(command: string, result: Json): string {
  if (PREFILL_RESULTS.has(command)) return "";
  if (Array.isArray(result?.recordAdmissionRefusals)&&result.recordAdmissionRefusals.length) return result.recordAdmissionRefusals.join("\n");
  if (result?.retryAvailable===false&&typeof result.limit==="string") return result.limit;
  return JSON.stringify(result);
}

export function WorkflowAssuranceSetting({ setting, act }: { setting: Json; act: (command: string, args: Record<string, unknown>) => Promise<unknown> }) {
  const [pending, setPending] = useState(false);
  const [error, setError] = useState("");
  const choose = async (command: string) => {
    if (pending) return;
    setPending(true); setError("");
    try { await act(command, {}); } catch (cause) { setError(String(cause)); } finally { setPending(false); }
  };
  if (!setting) return <section aria-label="Workflow approval"><p>Workflow approval setting unavailable.</p></section>;
  const verification = setting.verification ?? {};
  const robust = setting.level === "robust";
  return <section aria-label="Workflow approval" aria-busy={pending}>
    <p><strong>Workflow approval: {setting.policy}</strong>. {setting.source}.</p>
    <p>Keychain verification: <strong>{verification.state}</strong>. {verification.detail}</p>
    {robust && verification.available !== true && <p role="note">{setting.robustWithoutVerification}: a registered workflow runs only after you confirm it in this session.</p>}
    {setting.note && <p role="note">{setting.note}</p>}
    <details><summary>Change workflow approval</summary>
      <p>Require verified approval: a workflow runs when you approved it in this App session, or when your approval is verified by your keychain seal. Allow disk records: a workflow you registered earlier runs after a fresh check that its ledger entry, approval record and stored bytes agree on disk; who approved it is not verified.</p>
      <p>{setting.storage}</p>
      <button disabled={pending || (robust && verification.state !== "recovery required")} onClick={() => { void choose("workflow_assurance_robust"); }}>{verification.state === "recovery required" ? "Restore verified approval in your keychain" : "Require verified approval"}</button>{" "}
      <button disabled={pending || !robust} onClick={() => { void choose("workflow_assurance_relaxed"); }}>Allow disk records (native confirmation)…</button>
      {verification.state === "recovery required" && <>{" "}<button disabled={pending} onClick={() => { void choose("workflow_assurance_recheck"); }}>Check keychain again</button></>}
      <p>{setting.lowering}</p>
      {setting.protect?.offered === true
        ? <p><button disabled={pending} onClick={() => { void choose("workflow_protect_with_keychain"); }}>Protect registered workflows with your keychain…</button> Your keychain then verifies approvals across sessions and keeps this setting; you confirm in the App's native dialog.</p>
        : <p>Protect registered workflows with your keychain: unavailable. {setting.protect?.reason}</p>}
    </details>
    {error && <p role="alert">{error}</p>}
  </section>;
}

/** The active library's registered revisions (WR §4.6 LS-1). A revision the
 * host admits under the person's approval policy is offered Select, with its
 * approval evidence; the host resolves it from the revision store (SL-1, SL-4).
 * Every row keeps Refine. */
export function RegisteredRevisions({ library, rows, busy, act, chatAvailable = true }:{ library: string; rows: Json[]; busy: boolean; chatAvailable?: boolean; act: (command:string,args:Record<string,unknown>)=>unknown }) {
  return <ul aria-label="Registered revisions in the active library">{rows.map((row:Json)=><li key={`${row.name}@${row.revision}`} id={registeredRevisionAnchor(library,row.name,row.revision)}>{row.name} · revision {row.sequence} · {row.label}
    {row.selectable===true&&<> <button disabled={busy||!chatAvailable} onClick={()=>act("workflow_select_listed",{libraryRef:library,name:row.name,revision:row.revision})}>Select revision {row.sequence}</button></>}
    {" "}<button disabled={busy} onClick={()=>act("workflow_refine_registered",{name:row.name,revision:row.revision})}>Refine from the revision store…</button>
    {row.reconfirm===true&&<small> To use it again in this App session: Refine makes a draft with its bytes; review that draft and confirm in the App's dialog (re-confirmation).</small>}</li>)}</ul>;
}

/** What "bound in current generation" says, by what the binding rests on, and
 * only that. None says the project now at the path is the one bound: every
 * read an agent makes goes through the records capability's answer, which
 * checks that again. */
export const BOUND_MEANING:Record<string,string>={
  "receipt":" (a receipt held for this conversation; whether the project at its path is still the one it names is checked again on every read)",
  "offer":" (offered to this conversation when it started in this generation, with no receipt held; whether the project at its path is still the one offered is checked again on every read)",
  "fork of an offered conversation":" (admitted to this conversation as a fork of one offered it in this generation, with no receipt held; whether the project at its path is still the one offered is checked again on every read)",
};
/** The meaning of a bound row, or none where its basis is not stated. */
export const boundMeaning=(binding:Json)=>binding?.state==="bound in current generation"?(BOUND_MEANING[binding?.basis]??""):"";
export function RecordsCapabilityBindings({ host }:{ host: Json }) {
  const rows=(host?.threads??[]).filter((row:Json)=>JSON.stringify(row.generation)===JSON.stringify(host?.generation)&&row.recordsCapabilityBinding);
  // Why the last read could not be recorded (LIM-014 among them): shown whole,
  // since agents read nothing until it is resolved.
  const readLogLimit=host?.recordsCapability?.readLogLimit;
  if (!rows.length && !readLogLimit) return null;
  return <section aria-label="Conversation records capability"><h3>Conversation records capability</h3>
    {readLogLimit&&<p role="alert">Records capability: {readLogLimit}</p>}
    {rows.map((row:Json)=><p key={row.threadId}>{row.threadId}: {row.recordsCapabilityBinding.state}{boundMeaning(row.recordsCapabilityBinding)}. {row.recordsCapabilityBinding.persistence??""}{row.recordsCapabilityBinding.limit?` · ${row.recordsCapabilityBinding.limit}`:""}</p>)}
  </section>;
}

/** Stored claims remain quoted evidence even when their name/content matches
 * a revision held locally. This view exposes no selection or registration act. */
export function RegistrationEvidence({ evidence }:{ evidence: Json }) {
  if (!evidence) return null;
  return <section aria-label="Quoted registration history"><h3>Quoted registration history</h3>
    <p>These stored claims do not make a workflow selectable here. Use a new review and your own registration to use its content.</p>
    {(evidence.limits??[]).map((limit:string,i:number)=><p key={i}>History limit: {limit}</p>)}
    <ul>{(evidence.rows??[]).map((row:Json,i:number)=><li key={`${row.ledgerSequence??i}`}>
      {row.identity?.origin}:{row.identity?.name} · recorded source {row.identity?.source_root} · revision {row.identity?.revision} · recorded outcome {row.outcome}
      <p>Quoted act reference: {row.act?.record_id}. Recorded at {row.recordedAt}.</p>
      {(row.evidenceLimits??[]).map((limit:string,k:number)=><p key={k}>Quoted limit: {limit}</p>)}
      {(row.claims??[]).length===0&&<p>Capturing installation unknown; no readable A15 record for this reference.</p>}
      {(row.claims??[]).map((claim:Json,j:number)=><div key={j}>
        <p>{claim.installation?.reference ? `Recorded installation reference ${claim.installation.reference} — unverified attribution` : "Capturing installation unknown — unverified attribution"}</p>
        <p>Quoted actor claim: {JSON.stringify(claim.decisionActor)}.</p>
        <p>Quoted subjects: {JSON.stringify(claim.boundSubject)}.</p>
        {(claim.evidenceLimits??[]).map((limit:string,k:number)=><p key={k}>Quoted limit: {limit}</p>)}
      </div>)}
    </li>)}</ul>
  </section>;
}

/** "Select revision ‹n›" on a retained review, for each revision that review
 * registered or re-confirmed in this App process (RC-2). The host resolves it
 * from the revision store (SL-4); nothing here picks a folder. ‹n› is the
 * revision's sequence as the library lists it, or its first 12 characters. */
export function ReviewSelectButtons({ review, libraries, busy, act, chatAvailable = true }:{ review: Json; libraries: Json[]; busy: boolean; chatAvailable?: boolean; act: (command:string,args:Record<string,unknown>)=>unknown }) {
  // Only the library that holds this tuple (its origin and source root): the same
  // content may be registered under another sequence in another library.
  const listed=(id:Json)=>libraries.filter((l:Json)=>l.origin===id?.origin&&l.sourceRoot===id?.source_root)
    .flatMap((l:Json)=>Array.isArray(l.registered)?l.registered:[])
    .find((row:Json)=>row.name===id?.name&&row.revision===id?.revision)?.sequence;
  return <>{(review?.status?.entries??[]).filter((entry:Json)=>entry.state==="registered"||entry.state==="re-confirmed").map((entry:Json)=>
    <button key={entry.identity.revision} disabled={busy||!chatAvailable} onClick={()=>act("workflow_select_registered",{reviewRef:review.reference,revision:entry.identity.revision})}>Select revision {listed(entry.identity)??String(entry.identity.revision).slice(0,12)}</button>)}</>;
}

/** WR SL-2: "newer revision ‹n› available" beside the selection. The selection
 * stays on its revision; only the person's press selects the newer one, as a new
 * selection that cites the one it replaces. */
export function NewerRevisionNotice({ selection, busy, act }:{ selection: Json; busy: boolean; act: (command:string,args:Record<string,unknown>)=>unknown }) {
  const newer = selection?.newerRevision;
  if (!newer) return null;
  if (newer.limit) return <p role="note">Newer revisions: {String(newer.limit)}</p>;
  return <p role="note" aria-label="Newer revision">{String(newer.notice)}. The selection stays on revision {String(selection?.identity?.revision ?? "").slice(0, 12)} until you select another.
    {newer.selectable===true
      ? <> <button disabled={busy} onClick={()=>act("workflow_follow_newer_revision",{selectionRef:selection.reference,revision:newer.revision})}>{String(newer.offered)}</button></>
      : ` ${String(newer.offered)}.`}</p>;
}

export function WorkflowRootPanel({ viewStale = false, readFailure = null, data, host, act, observeView, openFileAct, fileActBusy = false, openPreparedMessage, operationalReference, offerComposer, showConversation, view, findInHistory }:{ viewStale?: boolean; readFailure?: string | null; findInHistory?: (hint: string) => void; view?: string; showConversation?: (threadId: string, target?: string) => void; offerComposer?: (threadKey: string, text: string) => void; data: Json; host: Json; act: (command:string,args:Record<string,unknown>)=>Promise<Json>; observeView?: ()=>Promise<unknown>; openFileAct?: OpenArrivalFileAct; fileActBusy?: boolean; openPreparedMessage?: (item: PreparedMessage) => void; operationalReference?: Json }) {
  const [name,setName]=useState("");
  const [revision,setRevision]=useState("");
  const [draftsState,setDraftsState]=useState<DraftsState>(initialDraftsState);
  const [thread,setThread]=useState("");
  const [chatChoice, setChatChoice] = useState<{ source: string; reference: Json } | null>(null);
  const chatScope = JSON.stringify([data?.context?.sourceRef, data?.context?.generation]);
  const chatChoiceLimit = chatChoice?.reference && chatChoice.reference.threadId !== thread
    ? "the previous Workflow chat choice was cleared; choose a chat or No chat explicitly"
    : chatChoice && chatChoice.source !== chatScope ? "the previous Workflow chat choice belongs to another source or generation; choose explicitly" : null;
  const chooseWorkflowChat = (value: string) => {
    setChatChoice({source:chatScope,reference:value ? {generation:host?.generation,threadId:value} : null});
    setThread(value);
  };
  // A source switch clears the local chat control; repeated bare thread IDs do not transfer it.
  useEffect(()=>setThread(""),[data?.context?.sourceRef,JSON.stringify(host?.generation)]);
  const context=workflowContext(data,host,thread);
  const selected=thread ? chatWorkflow(data,data?.context?.sourceRef,thread) : data?.inspection;
  const chatAvailable=!!context&&!!thread;
  const [text,setText]=useState("");
  const [busy,setBusy]=useState(false);
  const pendingAction = useRef(false);
  const [progress, setProgress] = useState("");
  const [outcome,setOutcome]=useState<{relation:{command:string;source:Json;request:Record<string,unknown>};message:string;limits:string[];historyNotices?:string[];readLimits?:string[];failed?:boolean;settled?:boolean}>();
  // Native results and later observation limits belong to the original press.
  // Children receive the unchanged native value, including pre-fill results.
  const action=async(command:string,args:Record<string,unknown>):Promise<Json>=>{
    if (pendingAction.current) return undefined;
    pendingAction.current = true;
    setBusy(true);
    setProgress(command === "workflow_create_draft" ? "Creating the draft, then reading its recorded state…"
      : command === "workflow_open_library" ? "Opening the selected workflow library…"
      : command === "workflow_register_native" ? "Waiting for the native registration result…"
      : command.startsWith("workflow_select_") ? "Reading the selected workflow content…"
      : "Waiting for the workflow operation and its current view…");
    let request:Record<string,unknown>;
    try{request=workflowArguments(command,args,data,host,thread);}
    catch(error){setOutcome({relation:{command,source:structuredClone(data?.context??null),request:structuredClone(args)},message:String(error),limits:[],failed:true,settled:true});pendingAction.current=false;setBusy(false);setProgress("");return undefined;}
    const relation={command,source:structuredClone(data?.context??null),request:structuredClone(request)};
    setOutcome({relation,message:"",limits:[]});
    const limit=(message:string)=>setOutcome(old=>old?.relation===relation?{...old,limits:[...old.limits,message]}:old);
    const observe=async(after:string)=>{if(observeView)try{await observeView();}catch(error){limit(`View refresh after ${after} failed: ${observationLine(observationText(error),"")} The original command response is retained as reported.`);}};
    // Capture this metadata request before awaiting the command or a new view.
    let draftRequest:Record<string,unknown>|undefined,draftRequestError:unknown;
    if(command==="workflow_create_draft"||command==="workflow_refine_registered"){
      try{draftRequest=command==="workflow_create_draft"?{context:structuredClone(request.context)}:workflowArguments("workflow_observe_drafts",{},data,host,thread);}
      catch(error){draftRequestError=error;}
    }
    try{
      const result=await act(command,request);
      setOutcome(old=>old?.relation===relation?{...old,message:workflowActionMessage(command,result),historyNotices:result?.historyNotices??[],readLimits:command==="workflow_read_records"?(result?.rsLimits??[]):[],failed:false,settled:true}:old);
      await observe(command);
      // SQ-D D-2 stays one original-context read even if the view refresh failed.
      if(command==="workflow_create_draft"||command==="workflow_refine_registered"){
        try{
          if(!draftRequest)throw draftRequestError;
          await act("workflow_observe_drafts",draftRequest);
          await observe(`workflow_observe_drafts for ${command}`);
        }catch(error){limit(`Draft observation (workflow_observe_drafts) after ${command} failed: ${String(error)}. The original command response is retained as reported.`);}
      }
      return result;
    }catch(error){setOutcome(old=>old?.relation===relation?{...old,message:String(error),failed:true,settled:true}:old);return undefined;}
    finally{pendingAction.current=false;setBusy(false);setProgress("");}
  };
  const conversations:Json[]=(host?.threads??[]).filter((entry:Json)=>JSON.stringify(entry.generation)===JSON.stringify(host?.generation));
  const entries:Json[]=data?.reviews??[];
  const orderedReviews=entries.filter(review=>review.reference===data?.activeReview).concat(entries.filter(review=>review.reference!==data?.activeReview));
  // J6 D-1 / V14 F2, F8: the digest of each complete review as the host
  // reports it (the native A15 statement names the same value), and this
  // view's own recomputation as a check. Kept per review so it stays readable
  // while the native confirmation holds the review.
  const [digests,setDigests]=useState<Record<string,ReviewDigestView>>({});
  const presentations=JSON.stringify(entries.map(review=>[review.reference,review.status?.presentation??null]));
  useEffect(()=>{
    let live=true;
    (async()=>{
      const next:Record<string,ReviewDigestView>={};
      for(const review of entries){
        if(!review.status?.presentation)continue;
        const row:ReviewDigestView={};
        try{const host=await invoke<Json>("workflow_review_digest",{reviewRef:review.reference});if(host.digest)row.host=host.digest;else row.hostUnavailable=String(host.unavailable);}
        catch(e){row.hostUnavailable=String(e);}
        try{row.app=await reviewDigest(review.status.presentation);}
        catch(e){row.appUnavailable=e instanceof Error?e.message:String(e);}
        next[review.reference]=row;
      }
      if(live&&Object.keys(next).length)setDigests(old=>({...old,...next}));
    })();
    return()=>{live=false;};
  },[presentations]); // eslint-disable-line react-hooks/exhaustive-deps
  const draftLibrary = (data?.libraries ?? []).find((library: Json) => library.reference === data?.activeLibrary);
  const draftReason = busy ? progress : !context ? "The workflow source is unavailable or changed. Refresh the App view before creating a draft."
    : !data?.activeLibrary ? "Open a project or user workflow library for the new draft."
    : !selected ? "Inspect bundled content or a development copy, or choose content for the Workflow chat."
    : !name.trim() ? "Enter a name for your new draft. The App will check the exact name and destination."
    : "Ready to create a draft from the displayed content in the opened library. This does not register or run it.";
  const guideOutcome = outcome ? { command: outcome.relation.command, message: outcome.message, failed: outcome.failed === true, settled: outcome.settled === true } : null;
  const unsavedRecords: {reference:string;limit:string}[] = [];
  for (const run of data?.runs??[]) {
    if (run.publication?.admissionRefusal) unsavedRecords.push({reference:run.reference,limit:run.publication.admissionRefusal});
    if (run.endNotice?.admissionRefusal) unsavedRecords.push({reference:run.endNotice.record,limit:run.endNotice.admissionRefusal});
    for (const check of [...(run.checks??[]),...(run.noticeChecks??[])]) {
      if (check.retryAvailable===false&&check.publicationLimit) unsavedRecords.push({reference:check.reference,limit:check.publicationLimit});
    }
  }
  for (const end of data?.endedAfterRelaunch??[]) {
    if (end.endNotice?.admissionRefusal) unsavedRecords.push({reference:end.endNotice.record,limit:end.endNotice.admissionRefusal});
  }
  return <section aria-label="Workflow studio controls" aria-busy={busy}>
    {busy && <p role="status" aria-live="polite">{progress} No automatic retry.</p>}
    {unsavedRecords.length>0&&<aside aria-label="Workflow records not saved">{unsavedRecords.map((record,index)=><p role="alert" key={`${record.reference}:${index}`}>{record.reference}: {record.limit}</p>)}</aside>}
    <div id="view-run" data-workspace-view="run" hidden={view !== undefined && view !== "run"}>
    <RunWorkflowGuide data={data} host={host} thread={thread} chooseThread={chooseWorkflowChat} act={action} busy={busy} text={text} setText={setText}
      outcome={guideOutcome} showConversation={showConversation} viewStale={viewStale} readFailure={readFailure}/>
    </div>
    <div id="view-make" data-workspace-view="make" hidden={view !== undefined && view !== "make"}>
    {offerComposer && <MakeWorkflowGuide data={data} host={host} act={action} busy={busy} outcome={guideOutcome} viewStale={viewStale} readFailure={readFailure} offerComposer={offerComposer} openPreparedMessage={openPreparedMessage} showConversation={showConversation} findInHistory={findInHistory}/>}
    </div>
    {/* The detailed studio follows the guides, collapsed, in both workflow views. */}
    <details id="workflow-studio" className="workspace-disclosure workspace-advanced" data-workspace-view="make" open={view === undefined ? true : undefined}>
    <summary><strong>Advanced: workflow studio</strong><span>Every selection, library, draft, trial, review, registration and run control in detail</span></summary>
    <div className="workspace-disclosure-content">
    <h2>Workflow selection and native registration</h2>
    <p>Make a new workflow or change one: choose content and a library, create a named draft, then try and review it before registration.</p>
    <a href="#file-acts">Review a workspace draft file for a separate standing act</a>
    <aside aria-label="Workflow working context">
      <ProjectLibraryContext host={host} />
      <ConversationContext label="Operational conversation viewed" host={host} reference={operationalReference} empty={operationalReference === null ? "No operational conversation selected." : undefined} />
      <ConversationContext label="Workflow chat context" host={host} reference={chatChoice?.reference ?? null} workflow
        empty={!thread ? "No chat — library inspection." : undefined} limit={chatChoiceLimit || workflowSourceLimit(host)} />
    </aside>
    <label>Workflow chat <select value={thread} onChange={e=>chooseWorkflowChat(e.target.value)} disabled={busy}><option value="">No chat — inspect library content</option>{(host?.threads??[]).filter((entry:Json)=>JSON.stringify(entry.generation)===JSON.stringify(host?.generation)).map((entry:Json)=><option key={entry.threadId} value={entry.threadId}>{entry.threadId} · {entry.modelProvider}/{entry.model}</option>)}</select></label>
    {chatChoiceLimit && <button type="button" disabled={busy} onClick={()=>chooseWorkflowChat("")}>Use No chat — inspect library content</button>}
    <p>{thread ? "This chat keeps its own pending workflow selection. Started runs keep their own revision." : "Library browsing is shared. Inspection here selects no workflow for a new chat."}</p>
    <section className="workflow-stage" aria-label="Choose workflow content and library"><h3>1. Choose content and a library</h3>
    <p>Development content, native registration, supplied text, model adoption and run standing remain separate observations.</p>
    <p>Bundle candidate content can be inspected or copied into a draft. It is not runnable as a shipped workflow; release registration remains pending.</p>
    {(data?.productionCatalog?.entries??[]).map((entry:Json)=><article key={entry.name}>
      <p>{entry.name} · {entry.revision}</p>
      <button disabled={busy||!context} onClick={()=>action("workflow_select_production_bundle",{name:entry.name})}>Inspect bundled candidate</button>
      <button disabled={busy||!context||!data?.activeLibrary} onClick={()=>action("workflow_select_production_copy",{name:entry.name})}>Inspect matching candidate in opened library</button>
    </article>)}
    <button disabled={busy||!context} onClick={()=>action("workflow_select_development",{})}>Select exact development workflow holding copy…</button>
    <button disabled={busy||!context} onClick={()=>action("workflow_open_library",{origin:"project"})}>Open project workflow library…</button>
    <button disabled={busy||!context} onClick={()=>action("workflow_open_library",{origin:"user"})}>Open user workflow library…</button>
    </section>
    <SelectedWorkflow selection={selected} inspection={!thread}/>
    {thread&&<NewerRevisionNotice selection={selected} busy={busy||!context} act={action}/>}
    <details><summary>Selection and libraries as the host reports them (paths shown as text; identities keep their exact bytes; a path that is not valid UTF-8 is marked)</summary>
    <pre style={{whiteSpace:"pre-wrap"}}>{JSON.stringify(readablePaths({selection:selected,inspection:data?.inspection,chatContext:context,libraries:data?.libraries,activeLibrary:data?.activeLibrary}),null,2)}</pre></details>
    <section className="workflow-stage" aria-label="Create a workflow draft"><h3>2. Create a named draft</h3>
    <p id="workflow-draft-next-step" role="status">{draftReason}</p>
    {draftLibrary && <p>Draft destination: {draftLibrary.origin ?? "origin not reported"} library · {nativePathText(draftLibrary.root) ?? draftLibrary.sourceRoot ?? "folder not reported"}. The host checks this opened library again before writing.</p>}
    <label>New draft name, or in-place library entry name <input {...EXACT_TEXT} aria-describedby="workflow-draft-next-step" value={name} onChange={e=>setName(e.target.value)} disabled={busy}/></label>
    <button className="setup-primary" aria-describedby="workflow-draft-next-step" disabled={busy||!context||!selected||!data?.activeLibrary||!name.trim()} onClick={()=>action("workflow_create_draft",{name})}>{thread?"Create draft from this chat’s selected content":"Create draft from inspected content"}</button>
    </section>
    <h3>3. Try and review drafts</h3>
    <WorkflowDraftsView data={data?.drafts} workspace={data?.projectLibraryAvailable===true} pointerLimits={data?.trialPointerLimits} conversations={conversations} contextHost={host}
      state={draftsState} update={patch=>setDraftsState(state=>({...state,...patch}))} comparisonOutside
      runs={[...(data?.runs??[]),...(data?.reopened?.runs??[])]} pending={data?.pendingTrials} busy={busy} act={action}/>
    {openPreparedMessage && preparedMessages(host).map(item => <div key={item.identity}>
      <small>{item.kind !== "bring-back" ? `Trial ${item.pending.sequence} of draft ${item.pending.draftName}` : item.pending.trial ? "Trial feedback" : "Run feedback"} · prepared message.</small>{" "}
      {item.kind === "clean" ? <div aria-label="Original composer owner"><p>This trial starts its own new conversation; it isn't sent in an existing one.</p>
        <details><summary>Exact scope</summary><p><small>Trial reference <code>{item.pending?.reference ?? "not reported"}</code>. Its composer belongs to no existing conversation; Send starts the new conversation with the connection and model you choose.</small></p></details></div>
        : <><ConversationContext label="Original composer owner" host={host} reference={item.owner} workflow limit={preparedMessageLimit(host, item)} />
          <button onClick={() => openPreparedMessage(item)}>View prepared message in conversation {item.owner?.threadId ?? "unavailable"}</button></>}
    </div>)}
    {(data?.libraries??[]).filter((l:Json)=>l.reference===data?.activeLibrary&&Array.isArray(l.registered)).map((l:Json)=><RegisteredRevisions key={l.reference} library={l.reference} rows={l.registered} busy={busy} chatAvailable={chatAvailable} act={action}/>)}
    {(data?.libraries??[]).filter((l:Json)=>l.reference===data?.activeLibrary).map((l:Json)=><LibraryEntries key={`${l.reference}:${l.entryListing?.reference??"unobserved"}`} library={l} busy={busy} available={!!context} act={action}/>)}
    {(data?.libraries??[]).filter((l:Json)=>l.reference===data?.activeLibrary).map((l:Json)=><RegistrationEvidence key={l.reference} evidence={l.registrationEvidence}/>)}
    <details className="workflow-stage"><summary>Advanced: exact revision or in-place entry</summary>
    <p>The name field above is also used by these explicit operations. No revision is selected automatically.</p>
    <label>Registered revision (content identity) <input {...EXACT_TEXT} value={revision} onChange={e=>setRevision(e.target.value)} disabled={busy}/></label>
    <button disabled={busy||!data?.activeLibrary||!name||!revision} onClick={()=>action("workflow_refine_registered",{name,revision})}>Refine registered revision from the revision store (no selection)</button>
    <button disabled={busy||!data?.activeLibrary||!name} onClick={()=>action("workflow_review",{names:[name],inPlace:true})}>Review this unregistered in-place library entry</button>
    <small> Drafts are reviewed from the draft list above.</small>
    </details>
    <div id="workflow-reviews">{orderedReviews.map(review=><article key={review.reference}>
      <h3>{review.reference===data?.activeReview?"Current review":"Retained review"} · {review.reference}</h3>
      {digests[review.reference]&&<p>{digestComparison(digests[review.reference])}{review.status?.presentation?<> Read the complete review below before choosing {review.status.presentation.entries?.[0]?.disposition==="re-confirmation"?"Re-confirm":"Register"}: the native confirmation shows the act statement and this digest, not the review itself.</>:" (as last shown with the review; while the native confirmation is open, the review it names is shown under \"Content named by an open native confirmation\")"}</p>}
      {review.status?.presentation?.entries?.[0]?.disposition==="re-confirmation"&&<p role="note">{review.status.presentation.entries[0].message}. {review.status.presentation.entries[0].reconfirmation?.statement}</p>}
      {review.status?.presentation&&<p><button disabled={busy||review.reference!==data?.activeReview} onClick={()=>action("workflow_register_native",{reviewRef:review.reference})}>{review.status?.presentation?.entries?.[0]?.disposition==="re-confirmation"?"Re-confirm this revision for use in this App session through native A15 confirmation…":"Register this review through native A15 confirmation…"}</button></p>}
      {review.status?.presentation ? <>
        {typeof review.status.state === "string" && <p>Review state: {review.status.state}</p>}
        <WorkflowRegistrationReview presentation={review.status.presentation} />
        <details><summary>Complete reported review status (diagnostic JSON)</summary><pre style={{whiteSpace:"pre-wrap"}}>{JSON.stringify(readablePaths(review.status),null,2)}</pre></details>
      </> : <>
        {review.status?.state==="native confirmation dismissed; no capture/registration"&&<p role="status">You cancelled the App's confirmation, so nothing was captured or registered. Review the draft again to register it.</p>}
        {review.status?.state==="native review/capture unavailable; original owner state retained"&&<p role="status">The review or its confirmation became unavailable, so registration did not complete and no receipt was made{typeof review.status?.limit==="string"?`: ${review.status.limit}`:""}. The original attempt is kept: you can continue it below, or review the draft again.</p>}
        <details open={!["native confirmation dismissed; no capture/registration","native review/capture unavailable; original owner state retained"].includes(review.status?.state)}><summary>Complete reported review status</summary><pre style={{whiteSpace:"pre-wrap"}}>{JSON.stringify(readablePaths(review.status??review),null,2)}</pre></details>
      </>}
      <LastCleanTrialLine line={review.lastCleanTrial} busy={busy} act={action}/>
      <button disabled={busy} onClick={()=>action("workflow_continue_registration",{reviewRef:review.reference})}>Continue original captured registration</button>
      <ReviewSelectButtons review={review} libraries={data?.libraries??[]} busy={busy} chatAvailable={chatAvailable} act={action}/>
    </article>)}</div>
    <h3>Send selected workflow text</h3>
    <label>Person text <textarea value={text} onChange={e=>setText(e.target.value)} disabled={busy} rows={3}/></label>
    {selected&&selected.runnable!==true&&<p role="note">Not runnable: {selected.runLimit}</p>}
    <button disabled={busy||!context||host?.state!=="ready"||!thread||selected?.runnable!==true} onClick={()=>action("workflow_prepare_run",{generation:host.generation,threadId:thread,personText:text})}>Prepare exact selected workflow text</button>
    {(data?.endedAfterRelaunch??[]).map((end:Json)=><article key={end.run}><h3>{end.run} (ended after the relaunch)</h3>
      <p>End notice: {end.endNotice?.state??"none"}. {end.limit}</p>
      {end.endNotice?.admissionRefusal&&<p role="alert">{end.endNotice.admissionRefusal}</p>}
      <HistoryReferenceNotice pointers={end.learningPointers}/>
      {(end.endNotice?.state?.startsWith("pending")||end.endNotice?.admissionRefusal||hasUnsavedHistoryReference(end))&&<p role="status">{end.endNotice?.state?.startsWith("pending")&&<>The next message in conversation {end.conversation} carries this end notice first, once. </>}
        <button disabled={busy||!!end.endNotice?.admissionRefusal} onClick={()=>action("workflow_reopened_notice",{runId:end.run,action:"retry"})}>{end.endNotice?.state?.startsWith("pending")||end.endNotice?.admissionRefusal?"Retry the end-notice record":"Retry saving records (never sends)"}</button>
        {(end.endNotice?.state?.startsWith("pending")&&end.noticeRecordFailure||end.endNotice?.admissionRefusal)&&<button disabled={busy} onClick={()=>action("workflow_reopened_notice",{runId:end.run,action:"skip"})}>Send without the end notice (recorded as not supplied)</button>}</p>}
    </article>)}
    {(data?.runs??[]).map((run:Json)=>{const next=chatWorkflow(data,data?.context?.sourceRef,run.conversation);return <article key={run.reference} id={runEvidenceAnchor(run.reference)}><h3>{run.reference}</h3>
      <p>Run: {run.lifecycle?.state}{run.lifecycle?.follows?` · follows ${run.lifecycle.follows}`:""}{run.lifecycle?.end?` · ${run.lifecycle.end.cause}`:""}. Records: {run.publication?.state}. Send: {run.status?.state}{run.status?.limit?` (${run.status.limit})`:""}. Supplied: {suppliedSummary(run)}. Adoption: unknown.</p>
      {run.publication?.admissionRefusal&&<p role="alert">{run.publication.admissionRefusal}</p>}
      {run.endNotice&&<p>End notice: {run.endNotice.state}</p>}
      {run.endNotice?.admissionRefusal&&<p role="alert">{run.endNotice.admissionRefusal}</p>}
      {!isRecordedRun(run)&&(run.endNotice?.state?.startsWith("pending")||run.endNotice?.admissionRefusal)&&<p role="status">{!run.endNotice?.admissionRefusal&&<>The next message in this conversation, with or without attachments or a mode, carries this end notice first, once.{run.status?.limit?` Last attempt: ${run.status.limit}`:""}</>}
        <button disabled={busy||!!run.endNotice?.admissionRefusal} onClick={()=>action("workflow_retry_records",{runRef:run.reference})}>Retry the end-notice record</button>
        {(run.noticeRecordFailure||run.endNotice?.admissionRefusal)&&<button disabled={busy} onClick={()=>action("workflow_skip_notice",{runRef:run.reference})}>Send without the end notice (recorded as not supplied)</button>}</p>}
      <ul>{[...(run.checks??[]),...(run.noticeChecks??[])].map((check:Json)=><li key={check.reference}>{check.readAt}: {check.state} ({check.supplyReading}); check record {check.published?"recorded":`${check.publicationState??"pending"}${check.publicationLimit?` — ${check.publicationLimit}`:""}`}; R3 {check.r3?.state}{check.r3?.limit?` — ${check.r3.limit}`:""}</li>)}</ul>
      <RunPanel run={run} conversations={conversations} bringBackDefault={runBringBackDefault(data,run.reference)} busy={busy || fileActBusy} act={action} openFileAct={openFileAct}/>
      <details><summary>Complete run evidence (paths shown as text)</summary><pre style={{whiteSpace:"pre-wrap"}}>{JSON.stringify(readablePaths(run),null,2)}</pre></details>
      {!isRecordedRun(run)&&<>
      <button disabled={busy||!!run.source||host?.state!=="ready"||!!run.publication?.admissionRefusal} onClick={()=>action("workflow_send_run",{runRef:run.reference})}>Record, then send original prepared text once</button>
      <button disabled={busy||!run.turn||host?.state!=="ready"} onClick={()=>action("workflow_check_supply",{runRef:run.reference})}>Check original native supplied text pages (new check)</button>
      <button disabled={busy||!!run.publication?.admissionRefusal||(!run.pendingRecords&&!hasUnsavedHistoryReference(run))} onClick={()=>action("workflow_retry_records",{runRef:run.reference})}>Retry pending records (never sends)</button>
      {run.lifecycle?.state?.startsWith("open")&&<>
        <button disabled={busy} onClick={()=>action("workflow_end_run",{runRef:run.reference,finishedReport:null})}>End run</button>
        {next&&run.home===host?.generation?.home&&<section aria-label="Selected workflow for the next run">
          <p>Next selected workflow for conversation {run.conversation}: {next.identity?.kind??"kind not supplied"} <b>{next.identity?.name??"name not supplied"}</b> · {next.identity?.origin??"origin not supplied"} library “{next.identity?.source_root??"source root not supplied"}”, revision <code style={{overflowWrap:"anywhere"}}>{next.identity?.revision??"revision not supplied"}</code> ({next.identity?.revision_method??"revision method not supplied"}).</p>
          <p>Holding library: {next.compatibility?.holdingLibrary??"not supplied"}.</p>
          <ul><CompatibilityAdvisory entry={next.compatibility}/></ul>
        </section>}
        <button disabled={busy||host?.state!=="ready"||run.home!==host?.generation?.home||next?.runnable!==true} onClick={()=>action("workflow_end_and_start",{runRef:run.reference,generation:host.generation,threadId:run.conversation,personText:text})}>End this run and start {next?.identity?.name??"this chat’s selected workflow"}</button>
      </>}
      {run.endNotice?.state?.startsWith("sent")&&<button disabled={busy||host?.state!=="ready"} onClick={()=>action("workflow_check_notice",{runRef:run.reference})}>Check the end notice in native history (new check)</button>}
      <p>Selection and run text are recorded before sending; if recording fails nothing is sent. A run opens when its start turn is observed and ends only when the person ends it: an interrupt, stop, quit, failed or completed turn, or an agent's "Workflow finished" line does not end it. Ending here records "ended by the person"; when the agent writes its "Workflow finished" line, the conversation offers End run beneath that message, which records cause "completed". After an end, the next message in this conversation (text, a plan or default mode turn, an attachment-bearing turn or a Continue-as request) carries the end notice first, once. Load/select this conversation and its received turn in native History before checking.</p>
      </>}
    </article>;})}
    </div>
    </details>
    <button disabled={busy} onClick={()=>action("workflow_read_records",{})}>Read recorded workflow supply (durable, read-only)</button>
    <CompareResult result={draftsState.compared}/>
    <button disabled={busy} onClick={()=>action("workflow_reopen",{})}>Reopen recorded workflow runs (read-only)</button>
    {data?.reopened&&<article><h3>Recorded runs (reopened from project records)</h3><p>{data.reopened.standing}</p>
      <ul>{(data.reopened.runs??[]).map((r:Json)=><li key={r.run}>{r.run} · conversation {r.conversation??"unknown"} · {r.state}{r.detail?` (${typeof r.detail==="string"?r.detail:JSON.stringify(r.detail)})`:""}{r.follows?` · follows ${r.follows}`:""}{(r.restartInterruptions??[]).length?` · App restart facts recorded for this conversation: ${r.restartInterruptions.length}`:""}
        {r.workflow&&<p>Recorded workflow {r.workflow.origin}:{r.workflow.name}, revision {String(r.workflow.revision??"").slice(0,12)}.</p>}
        {!(data?.runs??[]).some((h:Json)=>h.reference===r.run)&&<RunBringBack run={r} conversations={conversations} defaultThread={runBringBackDefault(data,r.run)} busy={busy} act={action}/>}
        {r.state?.startsWith("open")&&!(data?.runs??[]).some((h:Json)=>h.reference===r.run)&&<button disabled={busy} onClick={()=>action("workflow_end_recorded",{runId:r.run,threadId:r.conversation??null})}>End this interrupted run</button>}</li>)}</ul>
      {(data.reopened.historyNotices??[]).map((notice:string,i:number)=><p role="note" key={i}>{notice}</p>)}
      {(data.reopened.limits??[]).length>0&&<p>Record limits: {JSON.stringify(data.reopened.limits)}</p>}
      {data.reopened.restartLimits&&<p>App-restart interruption limits (written by the host at startup): {(data.reopened.restartLimits.outcomes??[]).map((o:Json)=>`${o.threadId}: ${o.outcome}${o.run?` on ${o.run}`:""}${typeof o.detail==="string"?` (${o.detail})`:""}`).join("; ")||data.reopened.restartLimits.reason||"no restart facts"}</p>}</article>}
    {data?.afterRunEnd&&<article><h3>After-run-end observations</h3><p>{data.afterRunEnd.standing}</p>
      {(data.afterRunEnd.historyNotices??[]).map((notice:string,i:number)=><p role="note" key={i}>{notice}</p>)}
      {(data.afterRunEnd.limits??[]).length>0&&<p role="alert">Observation/recording limits: {JSON.stringify(data.afterRunEnd.limits)}</p>}
      {(data.afterRunEnd.held??[]).map((r:Json)=><p key={r.recordId} role="status">Not yet recorded: {r.recordId} for ended run {r.run}, first observed {r.observedAt}. {r.limit}</p>)}
      <details><summary>Recorded post-end source history (JSON)</summary><pre style={{whiteSpace:"pre-wrap"}}>{JSON.stringify(data.afterRunEnd.runs??[],null,2)}</pre></details>
      {(data.afterRunEnd.runs??[]).filter((r:Json)=>!(data?.runs??[]).some((h:Json)=>h.reference===r.run)).map((r:Json)=><div key={r.run}><p>Ended run {r.run}. Source project {r.source?.projectId}.</p><ul>{(r.records??[]).filter((e:Json)=>e.kind==="checkpoint_arrival").map((e:Json)=><ArrivalRecord key={e.recordId} arrival={e} all={r.records??[]}/>)}</ul></div>)}
    </article>}
    {/* The exact reply and request of the last press. The guides say the result in words. */}
    {outcome&&<div aria-label="Workflow action response">
      {(outcome.historyNotices??[]).map((notice,i)=><p role="note" key={i}>{notice}</p>)}
      {(outcome.readLimits??[]).map((limit,i)=><p role="alert" key={`read-${i}`}>{limit}</p>)}
      {outcome.message&&<ActionFeedback message={`${outcome.relation.command}: ${outcome.message}`} label="Workflow command result"/>}
      <details><summary>Original workflow request</summary><pre style={{whiteSpace:"pre-wrap"}}>{JSON.stringify(outcome.relation,null,2)}</pre></details>
    </div>}
    {outcome?.limits.map((message,index)=><p role="status" aria-label="Workflow observation limit" key={index} style={{whiteSpace:"pre-wrap"}}>{message}</p>)}
  </section>;
}

export type LocalAccess = { view: LocalView | null; attempted: string[]; pending: boolean; message: { kind: "status" | "alert"; text: string } | null; prepare: () => void; enterKey: (generation: Json) => void; settingsTouched?: () => void };
export function HomeAccessPanel({ host, resources, navigating = false, act, readAccount, local }: { host: Json; resources: Json; navigating?: boolean; act: (command: string, args: Record<string, unknown>) => Promise<void>; readAccount: ReadAccountStatus; local?: LocalAccess }) {
  const routing = host?.homeRouting, access = host?.homeAccess, oauth = host?.homeOAuth, generation = host?.generation;
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const action = async (command: string, args: Record<string, unknown>) => {
    if (command === "select_home" && navigating) return;
    setBusy(true); setError("");
    try { await act(command, args); } catch (e) { setError(String(e)); } finally { setBusy(false); }
  };
  const entries: Json[] = (routing?.entries ?? []).filter((entry: Json) => entry.modeHomeClass === "account");
  return <section aria-label="Account connection"><h2>Connect to a model</h2>
    <p>Use your ChatGPT account, or a model server running on this machine. Each has its own home; switching between them leaves the other set up.</p>
    {routing?.activeModeHomeClass === "api-key" && <p role="status">Choose the account connection to continue. An older access home is retained without changing its saved configuration.</p>}
    {routing?.activeModeHomeClass === LOCAL_MODE && <p role="status">The local oMLX home is in use. ChatGPT sign-in applies to the account home.</p>}
    {routing?.activeModeHomeClass !== "account" && entries.map(entry => <article key={entry.modeHomeClass}><p>{entry.state}{entry.configurationLimit ? ` — ${entry.configurationLimit}` : ""}</p><details><summary>Connection source</summary><pre>{JSON.stringify(entry.generation, null, 2)}</pre></details><button disabled={busy || navigating || routing?.activeModeHomeClass === entry.modeHomeClass} onClick={() => action("select_home", {modeHomeClass: entry.modeHomeClass})}>Use {entry.modeHomeClass} home</button></article>)}
    <AccountStatus host={host} navigating={navigating} busy={busy} read={readAccount}/>
    {routing?.activeModeHomeClass === "account" && <p aria-label="Provider in this home">In this home the App starts Codex on its built-in OpenAI provider, whatever default provider your own Codex settings name. Your Codex files are not changed. A local model server is set up below, under “Use oMLX / a local model”.</p>}
    {routing?.activeModeHomeClass === "account" && <p aria-label="Where a sign-in will be kept">Before you sign in, you can see where Codex will keep your sign-in: press “Read effective storage and plugin settings” below.</p>}
    <button className="setup-primary" disabled={busy || routing?.activeModeHomeClass !== "account" || !generation} onClick={() => action("oauth_start", {generation,mode:"browser"})}>Sign in with your ChatGPT account (through Codex)…</button>
    <details><summary>Other sign-in options</summary>
    <button disabled={busy || routing?.activeModeHomeClass !== "account" || !generation} onClick={() => action("oauth_start", {generation,mode:"device-code"})}>Sign in through native device code…</button>
    <button disabled={busy || routing?.activeModeHomeClass !== "account" || !generation || !oauth?.source?.presentationAvailable} onClick={() => action("oauth_present", {generation})}>Show pending native sign-in…</button>
    <button disabled={busy || routing?.activeModeHomeClass !== "account" || !generation || !oauth?.source?.cancelAvailable} onClick={() => action("oauth_cancel", {generation})}>Cancel original pending sign-in with native confirmation…</button>
    <button disabled={busy || !generation || routing?.activeModeHomeClass !== "account"} onClick={() => action("logout_home", {generation,modeHomeClass:routing.activeModeHomeClass})}>Sign out of ChatGPT…</button></details>
    <section className="local-access-alternative" aria-label="oMLX and local providers"><h3>Use oMLX / a local model</h3>
      <p>Local providers use their own credentials, separate from ChatGPT sign-in.</p>
      {local && <LocalProviderAccess host={host} view={local.view} attempted={local.attempted} pending={local.pending || busy} message={local.message} navigating={navigating}
        prepare={local.prepare} enterKey={local.enterKey} settingsChanged={local.settingsTouched} useHome={() => { void action("select_home", { modeHomeClass: LOCAL_MODE }); }}/>}
    </section>
    <details><summary>Safe original sign-in observation</summary><pre style={{whiteSpace:"pre-wrap"}}>{JSON.stringify(oauth ?? {state:"unavailable"},null,2)}</pre></details>
    {error && <p role="alert">{error}</p>}
    <details><summary>Source-owned account observations and limits</summary><pre style={{whiteSpace:"pre-wrap"}}>{JSON.stringify(access, null, 2)}</pre></details>
    <details><summary>Explicit receiving homes and shared-resource observations</summary><pre style={{whiteSpace:"pre-wrap"}}>{JSON.stringify(resources ?? {state:"explicit shared-resource descriptors not configured; existing account path remains available"}, null, 2)}</pre></details>
    <CodexSessionSettings settings={host?.codexSessionSettings}/>
    <details><summary>Connection and credential boundaries</summary><p>Native login acknowledgment reports presence with validity unknown until actual use. Credential fields, browser URLs and device codes are never accepted through this webview. Resource links do not establish native discovery or authorize a future configuration write.</p></details>
  </section>;
}

/** DEL-01-05 REQ-010: every setting the App applies to its own Codex when it starts it, with its reason. */
export function CodexSessionSettings({ settings }: { settings: Json }) {
  const rows: Json[] = Array.isArray(settings) ? settings.filter((row: Json) => typeof row?.setting === "string" && typeof row?.reason === "string") : [];
  return <section aria-label="Settings the App applies to its Codex"><h3>Settings the App applies to its Codex</h3>
    {!Array.isArray(settings) ? <p>Not available for this connection.</p> : rows.length === 0 ? <p>The App applies no settings of its own to Codex in this home.</p>
      : <><p>The App starts Codex in this home with these settings and no others. They apply to the App's own Codex process only; your Codex files are not written.</p>
        <ul>{rows.map((row: Json) => <li key={row.setting}><code>{row.setting}</code> — {row.reason}</li>)}</ul></>}
  </section>;
}

const accessSettingSources: Record<string, string> = {
  packagedDefaults: "Packaged defaults", mdm: "Managed preferences", system: "System configuration",
  enterpriseManaged: "Enterprise configuration", user: "User configuration", project: "Project configuration",
  sessionFlags: "Session overrides", legacyManagedConfigTomlFromFile: "Legacy managed configuration",
  legacyManagedConfigTomlFromMdm: "Legacy managed preferences",
};
/** Where Codex keeps a sign-in, in the person's words, from the credential store Codex reported; the
 * value Codex gave stays in brackets. Nothing is inferred when Codex reported none. */
export function signInKept(field: Json): string {
  const value = field?.state === "reported" ? field?.value : undefined;
  switch (value) {
    case "file": return "in a file, auth.json, in this home's sign-in folder (file)";
    case "keyring": return "in your Mac's keychain (keyring)";
    case "auto": return "in your Mac's keychain where available, otherwise in a file, auth.json, in this home's sign-in folder (auto)";
    case "ephemeral": return "not kept after Codex stops (ephemeral)";
    default: return "Codex did not report it";
  }
}
export function EffectiveAccessSettingsPanel({ host, navigating, refresh }: { host: Json; navigating: boolean; refresh: (isCurrent: () => boolean) => Promise<Json> }) {
  const scopeOf = (snapshot: Json) => JSON.stringify([snapshot?.homeRouting?.activeModeHomeClass, snapshot?.generation, snapshot?.currentAppProjectContext ?? null, snapshot?.state, snapshot?.generationClosed]);
  const context = useRef({ key: "", epoch: 0, host });
  const key = JSON.stringify([scopeOf(host), navigating]);
  if (context.current.key !== key) context.current = { key, epoch: context.current.epoch + 1, host };
  context.current.host = host;
  const epoch = context.current.epoch;
  const mounted = useRef(true), sequence = useRef(0), pending = useRef(false);
  const revisionsDuringRead = useRef(new Set<Json>());
  const [reading, setReading] = useState(false), [error, setError] = useState("");
  const [observation, setObservation] = useState<{ packet: Json; epoch: number; sequence: number } | null>(null);
  useEffect(() => { mounted.current = true; return () => { mounted.current = false; sequence.current++; }; }, []);
  const ready = host?.state === "ready" && !host?.generationClosed && !!host?.generation
    && ["account", "api-key"].includes(host?.homeRouting?.activeModeHomeClass) && !navigating;
  if (pending.current) revisionsDuringRead.current.add(host?.accessSettingsReadRevision);
  // Retire the receipt permanently: a delayed older host status must not make
  // it current again after a newer read or source transition was observed.
  if (observation?.sequence === sequence.current && (!ready || observation.epoch !== epoch
    || observation.packet.scope.readRevision !== host?.accessSettingsReadRevision)) sequence.current++;
  const read = async () => {
    // Retained handlers and late replies cannot cross a home/source transition,
    // including a switch away and back to the same home.
    if (!ready || pending.current || context.current.epoch !== epoch || !mounted.current) return;
    const original = context.current.host, source = scopeOf(original), attempt = ++sequence.current;
    revisionsDuringRead.current = new Set([original.accessSettingsReadRevision]);
    let expectedRevision: string | undefined;
    const current = () => mounted.current && sequence.current === attempt && context.current.epoch === epoch && scopeOf(context.current.host) === source
      && (expectedRevision === undefined || [...revisionsDuringRead.current, context.current.host?.accessSettingsReadRevision]
        .every(revision => revision === original.accessSettingsReadRevision || revision === expectedRevision));
    pending.current = true; setReading(true); setError(""); setObservation(null);
    try {
      const packet: Json = await invoke("read_effective_access_settings", { generation: original.generation, modeHomeClass: original.homeRouting.activeModeHomeClass });
      if (!current()) return;
      if (packet?.state !== "observed" || typeof packet?.scope?.readRevision !== "string"
        || JSON.stringify(packet.scope.generation) !== JSON.stringify(original.generation)
        || packet.scope.modeHomeClass !== original.homeRouting.activeModeHomeClass) throw Error("unavailable");
      expectedRevision = packet.scope.readRevision;
      if (!current()) return;
      const latest = await refresh(current);
      if (!current() || scopeOf(latest) !== source || latest?.accessSettingsReadRevision !== packet.scope.readRevision
        || (context.current.host?.accessSettingsReadRevision !== original.accessSettingsReadRevision
          && context.current.host?.accessSettingsReadRevision !== packet.scope.readRevision)) return;
      setObservation({ packet, epoch, sequence: attempt });
    } catch (error) {
      if (current()) setError(readingSentence(error) ?? "Effective access settings unavailable; private diagnostic withheld. Read again from the current Codex source.");
    } finally { pending.current = false; if (mounted.current) setReading(false); }
  };
  const current = ready && observation?.epoch === epoch && observation.sequence === sequence.current
    && observation.packet.scope.readRevision === host?.accessSettingsReadRevision;
  const row = (label: string, field: Json, storage: boolean) => {
    const value = field?.state === "reported" && (storage
      ? ["file", "keyring", "auto", "ephemeral"].includes(field?.value)
      : typeof field?.value === "boolean") ? String(field.value) : "Unknown / not exposed";
    const source = field?.source;
    const kind = source?.state === "reported" && Object.hasOwn(accessSettingSources, source?.kind) ? accessSettingSources[source.kind] : null;
    const layer = Number.isSafeInteger(source?.layerIndex) && source.layerIndex >= 0 && source.layerIndex < 4096 ? source.layerIndex + 1 : null;
    return <p><strong>{label}:</strong> {value}. Source: {kind && layer ? `${kind} (layer ${layer})` : "Unknown / not established"}.</p>;
  };
  return <section aria-label="Effective access settings"><h3>Effective access settings</h3>
    <button disabled={!ready || reading} onClick={read}>Read effective storage and plugin settings</button>
    {reading && <p role="status">Reading the selected Codex source…</p>}
    {current ? <div role="status">
      <p aria-label="Where your sign-in is kept"><strong>Where your sign-in is kept:</strong> {signInKept(observation.packet.credentialStore)}, as Codex reported it for this launch.</p>
      {row("Credential storage", observation.packet.credentialStore, true)}
      {row("Plugins", observation.packet.plugins, false)}
      {host.homeRouting.activeModeHomeClass === "account" && (observation.packet.personDefaultProvider?.state === "reported" && observation.packet.personDefaultProvider.value !== "openai"
        ? <p><strong>Default provider in your Codex settings:</strong> <code>{String(observation.packet.personDefaultProvider.value)}</code>. It is not used in this home, where the App starts Codex on its built-in OpenAI provider.</p>
        : observation.packet.personDefaultProvider?.state === "none" || observation.packet.personDefaultProvider?.state === "reported" ? <p><strong>Default provider in your Codex settings:</strong> {observation.packet.personDefaultProvider.state === "none" ? "none named" : "the built-in OpenAI provider"}.</p>
        : <p><strong>Default provider in your Codex settings:</strong> Unknown / not established.</p>)}
      <p>Read from the selected {host.homeRouting.activeModeHomeClass} home’s current Codex process. A source category is shown only when its reported origin matches an enabled layer and that layer reports the same setting.</p>
    </div> : <p>No current settings observation. An earlier reading is not reused after a source change or a newer configuration read.</p>}
    {error && !current && <p role="alert">{error}</p>}
    <p>Only these two settings are shown from Codex’s effective configuration response, at the time of the read. Missing values and sources stay unknown. This is separate from login requirements and does not prove credential custody, actual file or keychain effects, plugin activity or ongoing configuration freshness. Reading changes no setting and starts no sign-in, model or conversation.</p>
  </section>;
}

export function AttachmentSelectionPanel({ data, act }: { data: Json; act: (command: string, args: Record<string, unknown>) => Promise<void> }) {
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const rows: Json[] = data?.selections ?? [];
  const args = { ownerRef: data?.ownerRef, listRevision: data?.listRevision };
  const invokeAction = async (command: string, extra: Record<string, unknown> = {}) => {
    setBusy(true); setError("");
    try { await act(command, { ...args, ...extra }); } catch (e) { setError(String(e)); }
    finally { setBusy(false); }
  };
  const move = (index: number, delta: number) => {
    const order = rows.map(row => row.selection.selectionRef);
    const other = index + delta; [order[index], order[other]] = [order[other], order[index]];
    void invokeAction("reorder_attachments", { selectionRefs: order });
  };
  return <section>
    <h2>Selected text attachments</h2>
    <p>Native selection keeps private source handles and original identities. Selected files are sent only by an explicit attachment-bearing submission; whole-list/source failures do not fall back to text-only sending.</p>
    <button disabled={busy || !data?.ownerRef} onClick={() => invokeAction("select_attachment")}>Select text attachment…</button>
    <p>List revision: {data?.listRevision ?? "unavailable"} · operation: {data?.operation?.state ?? data?.state ?? "not initialized"}.</p>
    {data?.reason && <p>{data.reason}</p>}{data?.operation?.message && <p role="alert">{data.operation.message}</p>}{error && <p role="alert">{error}</p>}
    {data?.operation?.state === "draft-prefilled-not-sent" && <div role="status"><p>Draft {data.operation.draft?.name} added ({data.operation.added} files). {data.operation.standing}</p>
      {(data.operation.notAttached ?? []).length > 0 && <ul role="alert" aria-label="Draft files not attached">{data.operation.notAttached.map((f: Json) => <li key={f.path}>Not attached: {f.path} ({f.bytes} bytes) — {f.reason}</li>)}</ul>}</div>}
    {rows.map((row, index) => <article key={row.selection.selectionRef} style={{ borderTop: "1px solid #ccc", paddingTop: 8 }}>
      <h3>{index + 1}. {row.selection.displayName} · {row.selection.standing}</h3>
      {row.selection.draft && <p>draft {row.selection.draft.name} at content {String(row.selection.draft.content?.value ?? "").slice(0, 12)} — not a registered workflow; this conversation is not a workflow run.</p>}
      <p>{row.selection.displayPath} · carrier: {row.selection.carrier}.</p>
      <pre>{JSON.stringify(readablePaths({ selectionRef: row.selection.selectionRef, nativePath: row.selection.nativePath, identityAtSelection: row.selection.identityAtSelection, draft: row.selection.draft }), null, 2)}</pre>
      <button disabled={busy || index === 0} onClick={() => move(index, -1)}>Move earlier</button>{" "}
      <button disabled={busy || index === rows.length - 1} onClick={() => move(index, 1)}>Move later</button>{" "}
      <button disabled={busy} onClick={() => invokeAction("remove_attachment", { selectionRef: row.selection.selectionRef })}>Remove</button>{" "}
      <button disabled={busy || !!row.selection.draft} onClick={() => invokeAction("reconfirm_attachment", { selectionRef: row.selection.selectionRef })}>Confirm current source…</button>
      {row.selection.draft && <small> A pre-filled draft file keeps the content it was read with; if the draft changed, remove its files and Try again.</small>}
    </article>)}
    <details><summary>Explicit App project observation and source limits</summary><pre>{JSON.stringify(data?.launchAppProjectObservation, null, 2)}</pre></details>
    <p>{data?.workflowRun}</p><p>{data?.submissionStanding}</p><p>{data?.custody}</p>
    {(data?.submissions ?? []).map((submission: Json) => <article key={submission.submissionRef}><h3>Submission {submission.submissionRef} · {submission.state}</h3><p>Frozen App context and native source outcome are distinct; native turn identity is used only when Core supplies a matching reference.</p><pre style={{ whiteSpace: "pre-wrap" }}>{JSON.stringify(submission, null, 2)}</pre></article>)}
    <p>Plain-text controls remain available independently. Workflow-run prefix/draft association and provider uptake require their owning evidence.</p>
  </section>;
}

export function TraceReceivingPanel({ data, currentContext, select }: { data: Json; currentContext: Json; select: (record: string, evidence: string) => Promise<void> }) {
  const [record, setRecord] = useState("");
  const [evidence, setEvidence] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const choose = async () => {
    if (!record || !evidence || busy) return;
    setBusy(true); setError("");
    try { await select(record, evidence); } catch (e) { setError(String(e)); }
    finally { setBusy(false); }
  };
  return <section>
    <h2>Supplied examination and trace records</h2>
    <p>Imports retain unverified declared facts and independent source buffers. They do not establish the current App executable, examination clock, native examination or host origin.</p>
    <label>Declared record kind <select value={record} disabled={busy} onChange={e => setRecord(e.target.value)}><option value="">Choose a record kind</option><option value="exam_result">Examination result</option><option value="xt_result">XT result</option><option value="xt_work">XT work account</option></select></label>{" "}
    <label>Declared evidence category <select value={evidence} disabled={busy} onChange={e => setEvidence(e.target.value)}><option value="">Choose an evidence category</option><option value="own_code">Own code</option><option value="native_supplier">Native supplier claim</option><option value="actual_host">Actual host claim</option><option value="extension">Extension claim</option><option value="definition_or_rehearsal">Definition or rehearsal</option></select></label>{" "}
    <button disabled={!record || !evidence || busy} onClick={choose}>Select supplied record…</button>
    <p>Selection: {data?.selection?.state ?? "not selected"} {data?.selection?.reason}</p>
    {busy && <p>Waiting for native selection and one source read.</p>}{error && <p role="alert">{error}</p>}
    <details><summary>Current App-observed context, separate from imported records</summary><p>This context never fills an imported subject, configuration, date or host origin. App executable identity is not established by this selector.</p><pre style={{ whiteSpace: "pre-wrap" }}>{JSON.stringify(currentContext, null, 2)}</pre></details>
    {(data?.receiving?.imports ?? []).map((imported: Json, index: number) => <article key={index} style={{ borderTop: "1px solid #ccc", paddingTop: 8 }}>
      <h3>Import {index + 1} · {imported.recordKind} · {imported.assessment}</h3>
      <p>Declared evidence category: {imported.declaredEvidenceCategory}. {imported.source?.sourceStanding}</p>
      {imported.reason && <p>Receiving limit: {imported.reason}</p>}
      <p>Selected source: {imported.source?.displayPath} · read: {imported.source?.readState} · {imported.source?.identityScope}</p>
      {imported.source?.pathDisplayLimit && <p>Path display limit: {imported.source.pathDisplayLimit}</p>}
      <details><summary>Exact native path and observed input-buffer identity</summary><pre>{JSON.stringify({ selectedPath: imported.source?.selectedPath, bufferIdentity: imported.source?.bufferIdentity, readMechanism: imported.source?.readMechanism, reason: imported.source?.reason }, null, 2)}</pre></details>
      {imported.suppliedBasis ? <div>
        <h4>Full declared subject and configuration (unverified)</h4><pre style={{ whiteSpace: "pre-wrap" }}>{JSON.stringify({ subject: imported.suppliedBasis.subject, configuration: imported.suppliedBasis.configuration, case: imported.suppliedBasis.case }, null, 2)}</pre>
        <p>{imported.suppliedBasis.date?.source === "stated_by_person" ? "Person-stated date (unverified)" : "Record-declared date/source (unverified)"}: {JSON.stringify(imported.suppliedBasis.date)}.</p>
        <details><summary>Complete supplied basis and source reference</summary><pre style={{ whiteSpace: "pre-wrap" }}>{JSON.stringify(imported.suppliedBasis, null, 2)}</pre></details>
      </div> : <p>No complete candidate/configuration/date basis is bound. Original facts remain available; no previous import's basis is inherited.</p>}
      <p>Current executable: {imported.currentExecutableIdentity} · native examination: {imported.nativeExamination} · host origin: {imported.hostOrigin}. {imported.semanticAssessment}</p>
      <details><summary>Full original supplied document and account/refusal facts</summary><pre style={{ whiteSpace: "pre-wrap" }}>{JSON.stringify({ originalDocument: imported.originalDocument, account: imported.account }, null, 2)}</pre></details>
      <details><summary>Exact original source bytes (memory only)</summary><pre style={{ whiteSpace: "pre-wrap" }}>{JSON.stringify(imported.source?.originalBytes)}</pre></details>
      <p>EXM-24 witness count: {String(imported.countsTowardV4Exm24)} · EXM-25 witness count: {String(imported.countsTowardV4Exm25)} · {imported.oi003} · {imported.hostJoin}.</p>
    </article>)}
    <p>These imports supply no EXM-24/EXM-25 joined witness. OI-003 remains unresolved; external-host join remains deferred under DECISION-3.</p>
    <p>{data?.receiving?.custody}</p>
  </section>;
}

export function DecisionPackagesPanel({ view, name, setName, recordName, refresh, continueRecording, openControl }: {
  view: Json; name: string; setName: (name: string) => void; recordName: () => void;
  refresh: () => Promise<void>; continueRecording: () => Promise<void>; openControl: (request: string) => Promise<void>;
}) {
  const writer = view?.writerStatus;
  const claim = (decision: Json) => <>
    <p>Recorded decision claim: <b>{decision.alternativeChosen}</b> {decision.statement} · decided by {decision.decidedBy} · recorded by {decision.recordedBy} ({decision.recordingMode}) · act record {decision.act ?? "no single record ID selected"}.</p>
    {(decision.equivalentCaptureRecords ?? []).length > 1 && <p>Equivalent records of the same agreeing capture: {decision.equivalentCaptureRecords.join(", ")}. Each original record's source and time remains available below.</p>}
    <p>Capture time: {decision.capturedAt ?? "not reported"} · observed at: {decision.observedAt ?? ((decision.equivalentCaptureRecords ?? []).length > 1 ? "multiple records; see individual observations" : "not reported")} · record written at: {decision.recordedAt ?? ((decision.equivalentCaptureRecords ?? []).length > 1 ? "multiple records; see individual written times" : "not reported")}. Recorded observation order does not establish human performance chronology.</p>
    <p>{decision.lapse} · {decision.captureProvenance}</p>
    {decision.currentContentComparison && <p>Current file comparison: {JSON.stringify(decision.currentContentComparison)}. This describes current bytes separately from past lapse history.</p>}
    {decision.historyResolution && <p>Recorded lapse history resolution: {JSON.stringify(decision.historyResolution)}.</p>}
    {decision.historyIncomplete && <p>Recorded history is incomplete; unresolved observations remain in the source details below.</p>}
    <details><summary>Scoped record sources, correction/lapse history and provenance</summary><pre style={{ whiteSpace: "pre-wrap" }}>{JSON.stringify(decision, null, 2)}</pre></details>
  </>;
  return <section>
    <h2>Decision packages</h2>
    <p>Your name on acts you record: <input {...EXACT_TEXT} value={name} onChange={e => setName(e.target.value)} onBlur={recordName} /></p>
    {view?.error && <p role="alert">{view.error}</p>}
    <button onClick={refresh}>Read decision packages</button>{" "}
    <button onClick={continueRecording}>Continue pending recording and record new requests</button>
    <p>Reading refreshes the view without writing records. Writer continuation runs separately at App startup and when requested above.</p>
    <p>Last writer continuation: {writer?.trigger ?? "not run"} · {writer?.state ?? "not run"} · new requests recorded: {writer?.requestsRecordedNow ?? 0}.</p>
    {(writer?.captureRecovery ?? []).filter((r: Json) => r.state !== "AC-7 recorded" || r.backlinkPending || r.delayEvidencePending).map((r: Json, i: number) => <p key={i}>Capture: {r.state} · {r.statusDetail ?? r.writeFailure ?? r.backlinkFailure ?? r.delayEvidenceFailure ?? r.captureDurability}</p>)}
    {(writer?.limits ?? []).map((limit: string, index: number) => <p key={index}>Writer limit: {limit}</p>)}
    {(view?.rows ?? []).map((row: Json) => <article key={row.package} style={{ borderTop: "1px solid #ccc", paddingTop: 8 }}>
      <h3>{row.package} — {row.actRequested} — {row.state}</h3>
      <p>Request resolution: {row.requestResolution ?? "not reported"}. Recorded request sources: {JSON.stringify(row.requestSources ?? [])}.</p>
      {row.state === "unresolvable request identity" && <p>The recorded request identity conflicts. No current request or act is selected by this view; existing package and record admission checks remain in force.</p>}
      <p>Subject: {(row.subject ?? []).join("; ")} · Purpose: {row.purpose} · Scope: {row.scope ?? "—"} · File: {row.packageFile}</p>
      <ul>{(row.alternatives ?? []).map((a: Json) => <li key={a.id}><b>{a.id}</b> {a.statement} — {(a.consequences ?? []).join("; ")}</li>)}</ul>
      {row.state === "ambiguous current standing" && <p>Current recorded standing is ambiguous. No current act is selected from these claims; this row does not establish a pending human act. The act control retains its current package and offer checks.</p>}
      {row.decision && claim(row.decision)}
      {(row.contenders ?? []).length > 0 && <div><h4>Recorded contenders</h4>{row.contenders.map((contender: Json) => <article key={contender.act}><h5>{contender.act}</h5>{claim(contender)}</article>)}</div>}
      {row.currentCandidates && <p>Current recorded candidates: {row.currentCandidates.join(", ") || "none established"}.</p>}
      {(row.limits ?? []).length > 0 && <p>Limits: {row.limits.join(" | ")}</p>}
      <button onClick={() => openControl(row.package)}>Open act control (decide)</button>
    </article>)}
    {(view?.historyNotices ?? []).map((notice:string,i:number)=><p role="note" key={`history-${i}`}>{notice}</p>)}
    {(view?.limits ?? []).length > 0 && <p>View limits: {view.limits.join(" | ")}</p>}
  </section>;
}

/**
 * Where the App's first read of its host state stands: "reading" before any status read has been
 * applied and none has failed; "failed" when one has failed and none has been applied since; "read"
 * once one has been applied. A read that fails after one was applied leaves "read": the person keeps
 * what is shown, and the guides say their last read failed (hostReads.ts).
 */
export function firstReadState(reads: { applied: number; failure: string | null }): "reading" | "failed" | "read" {
  return reads.applied > 0 ? "read" : reads.failure ? "failed" : "reading";
}

/** How long after launch, with no status read applied and none failed, the starting line says the App is
 * taking longer than usual (App Agent 0's number). The status timer starts a new read every POLL_MS whether
 * or not an earlier one has been answered, so the App is still trying while a read hangs. */
export const FIRST_READ_PATIENCE_MS = 10_000;

/** What stands in for the welcome and the workspace until the first status read is applied. The read's
 * own diagnostic is not shown: hostReads drops it at the source, so no status read's raw text is rendered. */
function FirstReadStatus({ failed, slow, retry }: { failed: boolean; slow: boolean; retry: () => void }) {
  if (!failed && !slow) return <p role="status">Starting Chirality…</p>;
  return <section aria-label="Chirality could not start">
    {failed ? <p role="alert">Chirality could not read its own state. It keeps trying; you can also try again now.</p>
      : <p role="status">Chirality is taking longer than usual to start. It keeps trying; you can also try again now.</p>}
    <p><button onClick={retry}>Try again</button></p>
  </section>;
}

export function App() {
  const [fleet, setFleet] = useState<FleetPacket | null>(null);
  const [fleetError, setFleetError] = useState("");
  const [fleetBusy, setFleetBusy] = useState(false);
  const refreshFleet = async () => {
    setFleetBusy(true); setFleetError("");
    try { setFleet(await readFleetPacket(command => invoke<FleetPacket>(command))); }
    catch (error) { setFleet(null); setFleetError(String(error)); }
    finally { setFleetBusy(false); }
  };
  const [routeRead, setRouteRead] = useState<RouteReadState>(emptyRouteRead);
  const readRoutes = async () => {
    setRouteRead(s => routeReadTransition(s, {type: "start"}));
    try {
      const result = await invoke<RouteView>("read_connector_routes");
      setRouteRead(s => routeReadTransition(s, {type: "success", view: result}));
    } catch (error) {
      setRouteRead(s => routeReadTransition(s, {type: "failure", error: String(error)}));
    }
  };
  // Every status read is numbered when it starts and applied only if newer than the one shown (hostReads.ts).
  const { host, hostReads, readHost, applyHost } = useOrderedHost();
  // Whether FIRST_READ_PATIENCE_MS has passed since launch; it only changes what the not-yet-read state says.
  const [firstReadSlow, setFirstReadSlow] = useState(false);
  useEffect(() => { const t = setTimeout(() => setFirstReadSlow(true), FIRST_READ_PATIENCE_MS); return () => clearTimeout(t); }, []);
  // Safe reply observations outlive a card's move between the selected chat
  // and other requests. They are transient App UI facts, never register rows.
  const [replyObservations, setReplyObservations] = useState<Record<string, RequestReplyObservation>>({});
  const replyObservationsRef = useRef<Record<string, RequestReplyObservation>>({});
  const pendingReplies = useRef(new Map<string, Promise<RequestReplyObservation>>());
  const observeReply = (observation: RequestReplyObservation) => {
    const next = { ...replyObservationsRef.current, [observation.scope]: observation };
    replyObservationsRef.current = next;
    setReplyObservations(next);
    return observation;
  };
  const fileActPanel = useRef<FileActPanelHandle>(null);
  const [fileActBusy, setFileActBusy] = useState(false);
  const openArrivalFileAct: OpenArrivalFileAct = async (runRef, arrivalRecordId) => {
    await fileActPanel.current?.openArrival(runRef, arrivalRecordId);
    // Navigation follows this explicit click, never an arriving record or poll.
    revealWorkspaceTarget("file-acts");
  };
  const [view, setView] = useState<Json>(null);
  const [offer, setOffer] = useState<Json>(null);
  const [choice, setChoice] = useState<string>("");
  const [name, setName] = useState<string>("");
  const [message, setMessage] = useState<string>("");
  const trialObservationSequence = useRef(0);
  const [trialObservation, setTrialObservation] = useState<{ relation: { attempt: number; command: string; source: Json; reference: unknown; target: Json }; limit: string | null } | null>(null);
  const homeClass = host?.homeRouting?.activeModeHomeClass ?? null;
  // Keyed oMLX local status (see localCommand); never contains a key.
  const [localView, setLocalViewState] = useState<LocalView | null>(null);
  const localViewRef = useRef<LocalView | null>(null);
  const setLocalView = (view: LocalView | null) => { localViewRef.current = view; setLocalViewState(view); };
  // Native consumes one entry per generation for its process; a renderer
  // reload keeps this nonsecret record so no refused retry is offered.
  const [localAttempted, setLocalAttempted] = useState<string[]>(readAttemptedLocalEntries);
  const [localPending, setLocalPending] = useState(false);
  const [localMessage, setLocalMessage] = useState<LocalAccess["message"]>(null);
  const localPendingRef = useRef(false), localSequence = useRef(0);
  const chooserHome = useRef({ mode: homeClass, epoch: 0 });
  if (chooserHome.current.mode !== homeClass) {
    // A different active home invalidates its previous chooser even if the
    // person returns before an earlier request finishes. A spawn update alone
    // is not a new choice: the command reports the actual admitted generation.
    chooserHome.current = { mode: homeClass, epoch: chooserHome.current.epoch + 1 };
  }
  const editRevision = useRef(0);
  const providerReadSequence = useRef(0);
  const providerReadPending = useRef(false);
  const [providerReading, setProviderReading] = useState(false);
  const [providerObservation, setProviderObservation] = useState<{ packet: Json; source: string; epoch: number; sequence: number } | null>(null);
  const [providerObservationMessage, setProviderObservationMessage] = useState("");
  const providerRowChoice = useRef<{ id: string; source: string; epoch: number; sequence: number; revision: string } | null>(null);
  const [conversationChoice, setConversationChoice] = useState({ ...emptyConversationChoice, homeEpoch: 0 });
  const choiceRef = useRef(conversationChoice);
  const reviseChoice = (patch: Partial<typeof emptyConversationChoice>) => {
    if (Object.hasOwn(patch, "modelProvider") || Object.hasOwn(patch, "entryId")) providerRowChoice.current = null;
    expireEndpointPreview();
    editRevision.current++;
    const previous = choiceRef.current.homeEpoch === chooserHome.current.epoch ? choiceRef.current : emptyConversationChoice;
    const next = { ...previous, ...patch, homeEpoch: chooserHome.current.epoch };
    choiceRef.current = next;
    setConversationChoice(next);
  };
  const { model, modelProvider, entryId } = conversationChoice.homeEpoch === chooserHome.current.epoch ? conversationChoice : emptyConversationChoice;
  const [startPending, setStartPending] = useState(false);
  const startPendingRef = useRef(false);
  const forkStartRevision = useRef(0);
  const continueStartRevision = useRef(0);
  const [homePending, setHomePending] = useState(false);
  const homePendingRef = useRef(false);
  const currentHost = useRef(host);
  currentHost.current = host;
  const actionSource = useRef({ identity: "", epoch: 0 });
  const actionSourceIdentity = JSON.stringify([host?.generation, host?.state, host?.generationClosed]);
  if (actionSource.current.identity !== actionSourceIdentity) actionSource.current = { identity: actionSourceIdentity, epoch: actionSource.current.epoch + 1 };
  const [conversationOutcome, setConversationOutcome] = useState<{
    command: string; args: Json; native: "pending" | "acknowledged" | "failed"; error?: string; observationLimit?: string;
  } | null>(null);
  const endpointRevision = useRef(0);
  const endpointOperation = useRef(0);
  const endpointMounted = useRef(true);
  const endpointBackendObserved = useRef(false);
  const endpointBusyRef = useRef(false);
  const [endpointBusy, setEndpointBusy] = useState(false);
  const [endpointEditor, setEndpointEditor] = useState<Json>(null);
  const endpointEditorRef = useRef<Json>(null);
  const updateEndpointEditor = (next: Json) => { endpointEditorRef.current = next; setEndpointEditor(next); };
  const expireEndpointPreview = () => {
    endpointRevision.current++;
    const current = endpointEditorRef.current;
    if (current) updateEndpointEditor({ ...current, offer: null, message: current.kind === "add" ? "Review this provider draft again before adding." : "Review this endpoint draft again before saving." });
    if (endpointBackendObserved.current) void invoke("provider_endpoint_discard").catch(() => {});
  };
  useEffect(() => {
    endpointMounted.current = true;
    return () => { endpointMounted.current = false; endpointRevision.current++; if (endpointBackendObserved.current) void invoke("provider_endpoint_discard").catch(() => {}); };
  }, []);
  useEffect(() => {
    if (host?.providerEndpointEdit && !endpointBackendObserved.current) {
      endpointBackendObserved.current = true; void invoke("provider_endpoint_discard").catch(() => {});
    }
  }, [!!host?.providerEndpointEdit]);
  // HomeSession's effective cwd is frozen with its actual source. The project
  // view and full generation are observed here; the read returns that exact cwd.
  const providerSource = (snapshot: Json) => JSON.stringify([snapshot?.homeRouting?.activeModeHomeClass, snapshot?.generation, snapshot?.currentAppProjectContext ?? null]);
  const providerObservationCurrent = !!providerObservation && host?.state === "ready" && !host?.generationClosed && homeClass === "account"
    && providerObservation.source === providerSource(host) && providerObservation.epoch === chooserHome.current.epoch
    && providerObservation.sequence === providerReadSequence.current
    && providerObservation.packet.scope.readRevision === host?.configuredProviderReadRevision;
  // DEL-01-05 model discovery: read only at the person's press, bound to the
  // home, generation and project it was read for and to this chooser epoch.
  const modelReadSequence = useRef(0);
  const modelReadPending = useRef(false);
  const [modelReading, setModelReading] = useState(false);
  const [modelObservation, setModelObservation] = useState<{ packet: Json; source: string; epoch: number; sequence: number } | null>(null);
  const [modelObservationMessage, setModelObservationMessage] = useState("");
  const modelObservationCurrent = !!modelObservation && host?.state === "ready" && !host?.generationClosed
    && modelObservation.source === providerSource(host) && modelObservation.epoch === chooserHome.current.epoch
    && modelObservation.sequence === modelReadSequence.current;
  const readAvailableModels = async () => {
    const original = currentHost.current;
    const mode = original?.homeRouting?.activeModeHomeClass;
    if (modelReadPending.current || startPendingRef.current || homePendingRef.current || original?.state !== "ready" || original?.generationClosed
      || mode !== "account") return;
    const source = providerSource(original), epoch = chooserHome.current.epoch, sequence = ++modelReadSequence.current;
    const current = () => sequence === modelReadSequence.current && epoch === chooserHome.current.epoch && source === providerSource(currentHost.current)
      && currentHost.current?.state === "ready" && !currentHost.current?.generationClosed && !homePendingRef.current;
    modelReadPending.current = true; setModelReading(true); setModelObservation(null); setModelObservationMessage("");
    try {
      const packet: Json = await invoke("read_available_models", { generation: original.generation, modeHomeClass: mode });
      if (!current()) return;
      if (!validModelPacket(packet, original.generation, mode)) throw Error("the reply was not a model list for this Codex source");
      setModelObservation({ packet, source, epoch, sequence });
    } catch (error) {
      if (current()) setModelObservationMessage(`Model list unavailable: ${error instanceof Error ? error.message : String(error)}. You can still enter a model ID under “Advanced: enter a model ID yourself”.`);
    } finally {
      modelReadPending.current = false; setModelReading(false);
    }
  };
  const chooseListedModel = (row: Json) => {
    const shown = modelObservation;
    if (!shown || !modelObservationCurrent || modelReadPending.current || startPendingRef.current || homePendingRef.current) return;
    if (!shown.packet.models.some((entry: Json) => entry.id === row.id && entry.model === row.model)) return;
    const choice = choiceRef.current;
    if (modelMatch(shown.packet, choice.modelProvider, choice.entryId) === "none") return;
    reviseChoice({ model: row.model });
  };
  const endpointSourceCurrent = (editor: Json) => !!editor && editor.source === providerSource(currentHost.current)
    && editor.epoch === chooserHome.current.epoch && currentHost.current?.state === "ready" && !currentHost.current?.generationClosed
    && currentHost.current?.homeRouting?.activeModeHomeClass === "account" && !homePendingRef.current && !startPendingRef.current;
  useEffect(() => {
    const editor = endpointEditorRef.current;
    if (editor && !endpointSourceCurrent(editor)) { expireEndpointPreview(); updateEndpointEditor(null); }
  }, [providerSource(host), homeClass, host?.state, host?.generationClosed, chooserHome.current.epoch]);
  const openEndpointEditor = (row: Json) => {
    if (!providerObservationCurrent || currentHost.current?.providerEndpointEdit?.available !== true || endpointBusyRef.current || providerReadPending.current || startPendingRef.current || homePendingRef.current) return;
    expireEndpointPreview();
    updateEndpointEditor({ kind: "endpoint", id: row.id, endpoint: row.endpoint, source: providerSource(currentHost.current), epoch: chooserHome.current.epoch, offer: null, message: "Only this existing provider's endpoint can be edited." });
  };
  const endpointUrl = (value: unknown) => {
    if (typeof value !== "string" || value.length > 2048 || !/^[\x21-\x7e]+$/.test(value) || /[@?#\\%]/.test(value)) return false;
    try { const parsed = new URL(value); return ["http:", "https:"].includes(parsed.protocol) && !!parsed.hostname
      && !parsed.username && !parsed.password && !parsed.search && !parsed.hash && (parsed.href === value || parsed.href === `${value}/`)
      && /^[A-Za-z0-9._~/-]*$/.test(parsed.pathname); } catch { return false; }
  };
  const reviewEndpoint = async () => {
    const editor = endpointEditorRef.current;
    if (editor?.kind === "add" || !endpointSourceCurrent(editor) || currentHost.current?.providerEndpointEdit?.available !== true || endpointBusyRef.current || providerReadPending.current || !endpointUrl(editor.endpoint)) return;
    const revision = endpointRevision.current, operation = ++endpointOperation.current;
    const current = () => endpointMounted.current && revision === endpointRevision.current && endpointSourceCurrent(editor) && endpointEditorRef.current?.id === editor.id;
    endpointBusyRef.current = true; setEndpointBusy(true);
    updateEndpointEditor({ ...editor, offer: null, message: "Reading an edit-specific offer…" });
    try {
      const epoch: unknown = await invoke("provider_endpoint_discard");
      if (!current()) return;
      if (typeof epoch !== "string" || !epoch) throw Error("Unavailable endpoint checkpoint");
      const packet: Json = await invoke("provider_endpoint_offer", { generation: currentHost.current.generation, providerId: editor.id, endpoint: editor.endpoint, epoch });
      if (!current()) return;
      if (typeof packet?.token !== "string" || packet.providerId !== editor.id || packet.label !== "Configured local provider"
        || packet.proposedEndpoint !== editor.endpoint || !endpointUrl(packet.currentEndpoint) || packet.wireApi !== "responses"
        || JSON.stringify(packet.scope?.generation) !== JSON.stringify(currentHost.current.generation)
        || JSON.stringify(packet.scope?.projectContext) !== JSON.stringify(currentHost.current.currentAppProjectContext ?? null)
        || typeof packet.scope?.cwd !== "string" || typeof packet.scope?.readRevision !== "string") throw Error("Unavailable endpoint offer");
      const latestRead = await readHost(invoke<Json>("host_status")); const latest: Json = latestRead.snapshot;
      if (!current() || providerSource(latest) !== editor.source || latest.providerOfferReadRevision !== packet.scope.readRevision) return;
      applyHost(latestRead);
      updateEndpointEditor({ ...editor, offer: packet, message: "Review the exact endpoint change. Saving opens two separate native decisions." });
    } catch (error) {
      if (current()) updateEndpointEditor({ ...editor, offer: null, message: readingSentence(error) ?? "Endpoint edit unavailable; private values and diagnostics withheld. Manual conversation choices remain independent." });
    } finally { if (operation === endpointOperation.current) { endpointBusyRef.current = false; setEndpointBusy(false); } }
  };
  const saveEndpoint = async () => {
    const editor = endpointEditorRef.current;
    if (editor?.kind === "add" || !endpointSourceCurrent(editor) || !editor.offer || endpointBusyRef.current || providerReadPending.current) return;
    const revision = endpointRevision.current, operation = ++endpointOperation.current;
    const current = () => endpointMounted.current && revision === endpointRevision.current && endpointSourceCurrent(editor) && endpointEditorRef.current?.id === editor.id;
    endpointBusyRef.current = true; setEndpointBusy(true);
    try {
      const outcome: Json = await invoke("provider_endpoint_save", { token: editor.offer.token });
      if (!current()) return;
      const messages: Record<string, string> = {
        "not-sent": "No endpoint write was sent.",
        "refused-not-sent": "Endpoint change refused before a write was sent.",
        "unknown": "Endpoint write outcome unknown. No automatic retry or source continuation.",
        "write-observed-source-unconfirmed": "Write observed; the current source has not been continued. No automatic retry.",
        "overridden": "Write observed with an override reported; the current source has not been continued.",
        "continued": "Endpoint write and current source continuation observed. Current choices and drafts stay unchanged.",
      };
      // A reading again after the write that was not sent: the write's outcome first, then why.
      updateEndpointEditor({ ...editor, offer: null, message: readingAfterWrite(outcome?.message) ?? messages[outcome?.state] ?? "Endpoint change outcome unavailable; no automatic retry." });
      // A refresh cannot revoke the save outcome already received; its failure is withheld.
      try {
        const latestRead = await readHost(invoke<Json>("host_status")); const latest: Json = latestRead.snapshot; if (current() && providerSource(latest) === editor.source) applyHost(latestRead);
      } catch { /* Retain the known save outcome; private refresh diagnostics withheld. */ }
    } catch { if (current()) updateEndpointEditor({ ...editor, offer: null, message: "Endpoint change unavailable. No automatic retry; a write may already have occurred." }); }
    finally { if (operation === endpointOperation.current) { endpointBusyRef.current = false; setEndpointBusy(false); } }
  };
  const openProviderCreate = () => {
    if (currentHost.current?.providerCreate?.available !== true || currentHost.current?.state !== "ready" || currentHost.current?.generationClosed
      || currentHost.current?.homeRouting?.activeModeHomeClass !== "account" || endpointBusyRef.current || providerReadPending.current || startPendingRef.current || homePendingRef.current) return;
    expireEndpointPreview();
    updateEndpointEditor({ kind: "add", id: "", name: "", endpoint: "", source: providerSource(currentHost.current), epoch: chooserHome.current.epoch, offer: null, message: "Add one anonymous Responses definition. This draft does not choose a provider or model." });
  };
  const createDraftValid = (editor: Json) => typeof editor?.id === "string" && /^[A-Za-z][A-Za-z0-9._-]{0,63}$/.test(editor.id) && editor.id !== "openai"
    && typeof editor.name === "string" && editor.name.length >= 1 && editor.name.length <= 128 && /^[\x20-\x7e]+$/.test(editor.name) && /[^ ]/.test(editor.name) && endpointUrl(editor.endpoint);
  const reviewProviderCreate = async () => {
    const editor = endpointEditorRef.current;
    if (editor?.kind !== "add" || !endpointSourceCurrent(editor) || !createDraftValid(editor) || currentHost.current?.providerCreate?.available !== true || endpointBusyRef.current || providerReadPending.current) return;
    const revision = endpointRevision.current, operation = ++endpointOperation.current;
    const current = () => endpointMounted.current && revision === endpointRevision.current && endpointSourceCurrent(editor) && endpointEditorRef.current?.kind === "add";
    endpointBusyRef.current = true; setEndpointBusy(true); updateEndpointEditor({ ...editor, offer: null, message: "Reading an Add-specific absence and version offer…" });
    try {
      const epoch: unknown = await invoke("provider_create_discard");
      if (!current()) return;
      if (typeof epoch !== "string" || !epoch) throw Error("Add checkpoint unavailable");
      const packet: Json = await invoke("provider_create_offer", { generation: currentHost.current.generation, providerId: editor.id, name: editor.name, endpoint: editor.endpoint, epoch });
      if (!current()) return;
      if (packet?.kind !== "add-provider" || typeof packet.token !== "string" || packet.providerId !== editor.id || packet.submittedName !== editor.name || packet.endpoint !== editor.endpoint
        || packet.wireApi !== "responses" || packet.requiresOpenaiAuth !== false || JSON.stringify(packet.scope?.generation) !== JSON.stringify(currentHost.current.generation)
        || JSON.stringify(packet.scope?.projectContext) !== JSON.stringify(currentHost.current.currentAppProjectContext ?? null) || typeof packet.scope?.cwd !== "string" || typeof packet.scope?.readRevision !== "string") throw Error("Add offer unavailable");
      const latestRead = await readHost(invoke<Json>("host_status")); const latest: Json = latestRead.snapshot;
      if (!current() || providerSource(latest) !== editor.source || latest.providerOfferReadRevision !== packet.scope.readRevision) return;
      applyHost(latestRead); updateEndpointEditor({ ...editor, offer: packet, message: "Review exactly this submitted definition. Adding opens two separate native decisions." });
    } catch (error) { if (current()) updateEndpointEditor({ ...editor, offer: null, message: readingSentence(error) ?? "Provider Add unavailable; absence or safe review could not be established. Private values and diagnostics withheld." }); }
    finally { if (operation === endpointOperation.current) { endpointBusyRef.current = false; setEndpointBusy(false); } }
  };
  const saveProviderCreate = async () => {
    const editor = endpointEditorRef.current;
    if (editor?.kind !== "add" || !endpointSourceCurrent(editor) || !editor.offer || endpointBusyRef.current || providerReadPending.current) return;
    const revision = endpointRevision.current, operation = ++endpointOperation.current;
    const current = () => endpointMounted.current && revision === endpointRevision.current && endpointSourceCurrent(editor) && endpointEditorRef.current?.kind === "add";
    endpointBusyRef.current = true; setEndpointBusy(true);
    try {
      const outcome: Json = await invoke("provider_create_save", { token: editor.offer.token });
      if (!current()) return;
      const messages: Record<string, string> = {
        "not-sent": "No provider write was sent.", "refused-not-sent": "Provider Add refused before a write was sent.",
        "unknown": "Provider Add write outcome unknown. No automatic retry or source continuation.",
        "write-observed-source-unconfirmed": "Provider addition write observed; the current source has not been continued. No automatic retry.",
        "overridden": "Provider addition write observed with an override reported; the current source has not been continued.",
        "continued": "Provider addition write and current source continuation observed. Read configured providers to see current rows. Your provider/model choice is unchanged.",
      };
      // A reading again after the write that was not sent: the write's outcome first, then why.
      updateEndpointEditor({ ...editor, offer: null, message: readingAfterWrite(outcome?.message) ?? messages[outcome?.state] ?? "Provider Add outcome unavailable; no automatic retry." });
      // A refresh cannot revoke the factual save outcome already received.
      // Its failure also cannot attach an old outcome to a newer editor/source.
      try {
        const latestRead = await readHost(invoke<Json>("host_status")); const latest: Json = latestRead.snapshot; if (current() && providerSource(latest) === editor.source) applyHost(latestRead);
      } catch { /* Retain the known save outcome; private refresh diagnostics withheld. */ }
    } catch (error) {
      // Refused at the configuration reading before the write: nothing was written; that sentence alone.
      if (current()) updateEndpointEditor({ ...editor, offer: null, message: readingSentence(error) ?? "Provider Add unavailable; no automatic retry. Private diagnostics withheld." });
    }
    finally { if (operation === endpointOperation.current) { endpointBusyRef.current = false; setEndpointBusy(false); } }
  };
  const configuredRowChoiceStale = () => {
    const selected = providerRowChoice.current, choice = choiceRef.current, source = currentHost.current;
    return !!selected && choice.modelProvider === selected.id && choice.entryId === "local-provider"
      && (source?.state !== "ready" || source?.generationClosed || selected.source !== providerSource(source)
        || selected.epoch !== chooserHome.current.epoch || selected.sequence !== providerReadSequence.current
        || selected.revision !== source?.configuredProviderReadRevision);
  };
  const rowChoiceStale = configuredRowChoiceStale();
  const readConfiguredProviders = async () => {
    const original = currentHost.current;
    if (endpointBusyRef.current || providerReadPending.current || startPendingRef.current || homePendingRef.current || original?.state !== "ready"
      || original?.generationClosed || original?.homeRouting?.activeModeHomeClass !== "account") return;
    const source = providerSource(original), epoch = chooserHome.current.epoch, sequence = ++providerReadSequence.current;
    const current = () => sequence === providerReadSequence.current && epoch === chooserHome.current.epoch
      && source === providerSource(currentHost.current) && currentHost.current?.state === "ready" && !currentHost.current?.generationClosed
      && !startPendingRef.current && !homePendingRef.current;
    expireEndpointPreview();
    providerReadPending.current = true; setProviderReading(true); setProviderObservation(null); setProviderObservationMessage("");
    try {
      const packet: Json = await invoke("read_configured_providers", { generation: original.generation, modeHomeClass: "account" });
      if (!current()) return;
      const valid = packet?.state === "observed" && packet?.schema === "ConfigReadResponse" && Array.isArray(packet.rows)
        && packet.scope?.modeHomeClass === "account" && JSON.stringify(packet.scope.generation) === JSON.stringify(original.generation)
        && JSON.stringify(packet.scope.projectContext) === JSON.stringify(original.currentAppProjectContext ?? null)
        && typeof packet.scope.cwd === "string" && typeof packet.scope.readRevision === "string"
        && ["Some configured definitions or metadata were withheld; no private names, values or diagnostics are offered",
          "Configured metadata only; not authentication, reachability, model/capability availability or Start authority"].includes(packet.limit)
        && packet.rows.every((row: Json) => typeof row.id === "string" && /^[A-Za-z][A-Za-z0-9._-]{0,63}$/.test(row.id)
          && row.label === "Configured local provider" && typeof row.endpoint === "string" && row.wireApi === "responses");
      if (!valid) throw Error("unavailable projection");
      const latestRead = await readHost(invoke<Json>("host_status")); const latest: Json = latestRead.snapshot;
      if (!current() || providerSource(latest) !== source || latest?.state !== "ready" || latest?.generationClosed
        || latest?.configuredProviderReadRevision !== packet.scope.readRevision
        || (currentHost.current?.configuredProviderReadRevision !== original.configuredProviderReadRevision
          && currentHost.current?.configuredProviderReadRevision !== packet.scope.readRevision)) return;
      applyHost(latestRead);
      // A row chosen from an earlier read of this same source (home, Codex
      // generation and project) stays chosen when this read still lists it;
      // otherwise, and after a Codex restart, it stays retired.
      const chosen = providerRowChoice.current, choice = choiceRef.current;
      if (chosen && chosen.source === source && chosen.epoch === epoch && choice.modelProvider === chosen.id && choice.entryId === "local-provider"
        && packet.rows.some((row: Json) => row.id === chosen.id)) providerRowChoice.current = { id: chosen.id, source, epoch, sequence, revision: packet.scope.readRevision };
      setProviderObservation({ packet, source, epoch, sequence });
    } catch (error) {
      if (current()) setProviderObservationMessage(readingSentence(error) ?? "Configured provider observation unavailable; private diagnostic withheld. Manual explicit choices remain independent.");
    } finally {
      providerReadPending.current = false; setProviderReading(false);
    }
  };
  const chooseConfiguredProvider = (id: string) => {
    const source = currentHost.current;
    if (!providerObservation || source?.state !== "ready" || source?.generationClosed || providerObservation.source !== providerSource(source)
      || providerObservation.epoch !== chooserHome.current.epoch || providerObservation.sequence !== providerReadSequence.current
      || providerObservation.packet.scope.readRevision !== source?.configuredProviderReadRevision
      || providerReadPending.current || startPendingRef.current || homePendingRef.current
      || !providerObservation.packet.rows.some((row: Json) => row.id === id)) return;
    reviseChoice({ modelProvider: id, entryId: "local-provider" });
    providerRowChoice.current = { id, source: providerObservation.source, epoch: providerObservation.epoch,
      sequence: providerObservation.sequence, revision: providerObservation.packet.scope.readRevision };
  };
  const fixedLocal = localRoute(localView, host);
  const entryCompatible = startEntries(host).some(entry => entry.value === entryId) && (homeClass === "account"
    || (homeClass === LOCAL_MODE && !!fixedLocal && model === fixedLocal.model && modelProvider === fixedLocal.providerId));
  // Why the provider row chosen earlier no longer counts, and what restores it.
  const rowChoiceNote = !rowChoiceStale ? "" : providerObservationCurrent
    ? (providerObservation.packet.rows.some((row: Json) => row.id === modelProvider)
      ? `Provider ${modelProvider} was chosen before Codex or the connection changed. Choose it again from the list.`
      : `Provider ${modelProvider} is not in the list just read. Choose a provider from the list, or enter one under “Advanced: enter IDs yourself”.`)
    : providerReading ? "Reading configured local providers…"
    : `Provider ${modelProvider} was chosen from a provider list that is now out of date. Read configured local providers again; if the choice is not kept, choose it again from the list.`;
  // The first thing that keeps Start unavailable, in the order a person meets it.
  const startBlocked = host?.state !== "ready" ? "Codex is not connected. Start it under Connection and access."
    : startPending ? "Starting the conversation…"
    : homePending ? "Changing the connection…"
    : providerReading ? "Reading configured local providers…"
    : endpointBusy ? "A provider change is in progress."
    : !modelProvider.trim() ? "Choose how this conversation connects (step 1)."
    : !model.trim() ? ("Choose a model (step 2).")
    : !entryCompatible ? "This choice does not belong to the connection in use. Choose again in step 1."
    : rowChoiceStale ? rowChoiceNote
    : "";
  const [role, setRole] = useState<string>("");
  const [roleTouched, setRoleTouched] = useState(false);
  const [threadKey, updateThreadKey] = useState<string>("");
  const threadChoiceRevision = useRef(0);
  const activityNavigationRef = useRef<NativeActivityHandle>(null);
  const setThreadKey = (key: string) => { threadChoiceRevision.current++; updateThreadKey(key); };
  // Task views (DailyWorkspace): one visible at a time, all mounted. An intent
  // that navigates sets its view in the same update as its own state, so the
  // reveal that follows finds its target visible.
  const [taskView, setTaskView] = useState<string>("run");
  const taskViewRef = useRef(taskView);
  const showView = (next: string) => { taskViewRef.current = next; setTaskView(next); };
  useEffect(() => registerWorkspaceViews(next => {
    if (taskViewRef.current === next) return;
    taskViewRef.current = next;
    flushSync(() => setTaskView(next));
  }), []);
  const [composerOffer, setComposerOffer] = useState<ComposerOffer | null>(null);
  const composerOfferSequence = useRef(0);
  // A guide's "show the conversation": the person's explicit navigation selects
  // that conversation of the current generation, then reveals the target after
  // the selection has rendered. It answers, sends or resumes nothing.
  const [conversationReveal, setConversationReveal] = useState<{ sequence: number; target: string } | null>(null);
  const conversationRevealSequence = useRef(0);
  const showConversation = (threadId: string, target = "conversation") => {
    const row = (currentHost.current?.threads ?? []).find((t: Json) => t.threadId === threadId && JSON.stringify(t.generation) === JSON.stringify(currentHost.current?.generation));
    if (!row) return;
    setThreadKey(JSON.stringify([row.generation, row.threadId]));
    showView("conversation");
    conversationRevealSequence.current += 1;
    setConversationReveal({ sequence: conversationRevealSequence.current, target });
  };
  useEffect(() => {
    if (!conversationReveal) return;
    // The message box: showView already made the Conversation view current, and
    // the panel scrolls to and focuses its own field. Scrolling to the section's
    // top here would move the focused box out of view.
    if (conversationReveal.target === "ordinary-composer-text") return;
    revealWorkspaceTarget(document.getElementById?.(conversationReveal.target) ? conversationReveal.target : "conversation", true);
  }, [conversationReveal]);
  // A saved conversation ID as a History search hint: shows History and fills its search only.
  const [historyHint, setHistoryHint] = useState<{ sequence: number; text: string } | null>(null);
  const findInHistory = (hint: string) => { showView("history"); setHistoryHint(previous => ({ sequence: (previous?.sequence ?? 0) + 1, text: hint })); };
  // History Continue admitted this exact conversation (source-checked there):
  // select it, show the Conversation view and focus its message box.
  const openAdmittedConversation = (key: string) => {
    setThreadKey(key);
    showView("conversation");
    conversationRevealSequence.current += 1;
    setConversationReveal({ sequence: conversationRevealSequence.current, target: "ordinary-composer-text" });
  };
  const offerComposer = (key: string, text: string) => { setThreadKey(key); showView("conversation"); composerOfferSequence.current += 1; setComposerOffer({ sequence: composerOfferSequence.current, threadKey: key, text }); };
  const forkSequence = useRef(0);
  const forkInFlight = useRef(false);
  const [pendingFork, setPendingFork] = useState<ForkNavigation | null>(null);
  const [preparedNotice, setPreparedNotice] = useState("");
  const [preparedReveal, setPreparedReveal] = useState<PreparedComposerReveal | null>(null);
  const preparedOpenSequence = useRef(0);
  const preparedNavigation = useRef<{ check: () => string | null } | null>(null);
  // Observe invalidation while an Open read is pending. Once refused, an
  // away-and-back source or selection cannot revive the original click.
  preparedNavigation.current?.check();
  const openPreparedMessage = async (item: PreparedMessage): Promise<void> => {
    const sequence = ++preparedOpenSequence.current;
    setPreparedReveal(null);
    threadChoiceRevision.current++;
    const source = currentHost.current;
    const choiceRevision = threadChoiceRevision.current, chooserRevision = editRevision.current;
    const homeEpoch = chooserHome.current.epoch, startRevision = continueStartRevision.current;
    let refusal: string | null = null;
    const ticket = { check: (): string | null => {
      if (!refusal) {
        if (preparedNavigation.current !== ticket || threadChoiceRevision.current !== choiceRevision || editRevision.current !== chooserRevision
          || chooserHome.current.epoch !== homeEpoch || continueStartRevision.current !== startRevision || homePendingRef.current || startPendingRef.current) refusal = "A newer navigation or conversation choice superseded this Open.";
        else refusal = preparedMessageLimit(currentHost.current, item);
      }
      return refusal;
    } };
    preparedNavigation.current = ticket;
    const sourceLabel = `${source?.workflowRoot?.context?.sourceRef ?? "source unavailable"}, conversation ${item.owner?.threadId ?? "unavailable"}, generation ${JSON.stringify(item.owner?.generation ?? null)}`;
    const refuse = (reason: string) => { if (sequence === preparedOpenSequence.current) setPreparedNotice(`Prepared-message navigation refused: ${reason} (${sourceLabel})`); };
    const initial = ticket.check();
    if (initial) { refuse(initial); preparedNavigation.current = null; return; }
    setPreparedNotice("Reading the original prepared message and composer conversation…");
    try {
      // A current-pending navigation is just one observation. In particular it
      // never uses a prepare command's result or invokes a workflow operation.
      const snapshotRead = await readHost(invoke<Json>("host_status")); const snapshot: Json = snapshotRead.snapshot;
      const limit = ticket.check() ?? (currentHost.current !== source ? "A newer host observation superseded this delayed read; open again from the current view." : null)
        ?? preparedMessageLimit(snapshot, item);
      if (limit) { refuse(limit); return; }
      applyHost(snapshotRead);
      setThreadKey(conversationKey(findConversation(snapshot.threads, item.owner)));
      const revealRevision = threadChoiceRevision.current;
      const reveal: PreparedComposerReveal = { sequence, item,
        isCurrent: () => sequence === preparedOpenSequence.current && threadChoiceRevision.current === revealRevision
          && editRevision.current === chooserRevision && chooserHome.current.epoch === homeEpoch && continueStartRevision.current === startRevision
          && !homePendingRef.current && !startPendingRef.current && preparedMessageLimit(currentHost.current, item) === null,
        finish: shown => {
          setPreparedReveal(current => current === reveal ? null : current);
          if (sequence === preparedOpenSequence.current) {
            if (shown) setPreparedNotice(`Prepared composer shown (${sourceLabel}). Opening sends nothing.`);
            else refuse("The exact composer reveal was superseded or is no longer available.");
          }
        } };
      showView("conversation");
      setPreparedReveal(reveal);
    } catch (error) { refuse(`The original view refresh failed: ${observationLine(observationText(error), "")} Open again from a current view.`); }
    finally { if (preparedNavigation.current === ticket) preparedNavigation.current = null; }
  };
  const roleInitialized = useRef(false);
  useEffect(() => {
    if (!roleInitialized.current && host?.roleSet?.available) {
      roleInitialized.current = true;
      setRole(host.roleSet.defaultRole ?? "");
    }
  }, [host?.roleSet]);


  const refresh = useCallback(async () => {
    const snapshotRead = await readHost(invoke<Json>("host_status")); const snapshot: Json = snapshotRead.snapshot;
    applyHost(snapshotRead);
    try {
      setView(await invoke("decision_view"));
    } catch (e) {
      setView({ error: String(e) });
    }
    return snapshot;
  }, []);

  const refreshEffectiveAccessSettings = useCallback(async (isCurrent: () => boolean) => {
    const sourceAtRead = currentHost.current;
    const snapshotRead = await readHost(invoke<Json>("host_status")); const snapshot: Json = snapshotRead.snapshot;
    // This explicit settings refresh cannot replace a newer App observation.
    // Other refresh and polling behavior keeps its existing semantics.
    if (isCurrent() && currentHost.current === sourceAtRead) applyHost(snapshotRead);
    return snapshot;
  }, []);

  const readAccountStatus: ReadAccountStatus = useCallback(async (generation, modeHomeClass, isCurrent) => {
    const homeEpoch = chooserHome.current.epoch, sourceEpoch = actionSource.current.epoch;
    const current = () => isCurrent() && !homePendingRef.current && chooserHome.current.epoch === homeEpoch
      && actionSource.current.epoch === sourceEpoch && currentHost.current?.state === "ready" && !currentHost.current?.generationClosed
      && currentHost.current?.homeRouting?.activeModeHomeClass === modeHomeClass
      && sameActivityGeneration(currentHost.current?.generation, generation);
    if (!current()) return;
    // The native command validates the same source and uses account/read with
    // empty params. No forced credential refresh, reauthentication or model call.
    await invoke("read_home_access", { generation, modeHomeClass });
    if (!current()) return;
    const viewAtRead = currentHost.current;
    const snapshotRead = await readHost(invoke<Json>("host_status")); const snapshot: Json = snapshotRead.snapshot;
    if (!current() || currentHost.current !== viewAtRead) return;
    // A current host_status may itself report a replacement source. It is a
    // new observation, never confirmation of the original account read.
    applyHost(snapshotRead);
  }, []);

  const captureContinueNavigation = (generation: Json, historyCurrent: (history: Json) => boolean): ContinueNavigation => {
    const source = JSON.stringify(generation);
    const mode = chooserHome.current.mode, epoch = chooserHome.current.epoch;
    const choiceRevision = threadChoiceRevision.current, startRevision = continueStartRevision.current;
    let current = true;
    const isCurrent = () => {
      const shown = currentHost.current;
      current = current && !homePendingRef.current && !startPendingRef.current
        && shown?.state === "ready" && shown.generationClosed !== true
        && JSON.stringify(shown.generation) === source && shown.homeRouting?.activeModeHomeClass === mode
        && chooserHome.current.epoch === epoch && threadChoiceRevision.current === choiceRevision
        && continueStartRevision.current === startRevision && historyCurrent(shown.nativeHistory);
      return current;
    };
    return { isCurrent, observe: async () => {
      // The same two observer reads as refresh, bounded to this original
      // navigation's last-known source/intent. Shared refresh semantics stay put.
      const snapshotRead = await readHost(invoke<Json>("host_status")); const snapshot: Json = snapshotRead.snapshot;
      if (isCurrent()) applyHost(snapshotRead);
      try {
        const decision: Json = await invoke("decision_view");
        if (isCurrent()) setView(decision);
      } catch (e) { if (isCurrent()) setView({ error: String(e) }); }
      return snapshot;
    } };
  };

  useEffect(() => {
    // A failed first read is shown by firstReadState; its rejection needs no other handler.
    void refresh().catch(() => undefined);
    const t = setInterval(() => refreshAfterAction(() => readHost(invoke<Json>("host_status")).then(applyHost), () => setMessage(withRefreshFailure)), POLL_MS);
    // RECOVERY SQ-W W-4, W-5: when the window is shown again after it was
    // closed (hidden; DEF-1), the view replaces what it rendered with the
    // host's current snapshot at once. Nothing is sent to Codex.
    const shown = () => { if (document.visibilityState === "visible") refresh(); };
    document.addEventListener("visibilitychange", shown);
    return () => { clearInterval(t); document.removeEventListener("visibilitychange", shown); };
  }, [refresh]);

  const act = async (cmd: string, args?: Record<string, unknown>) => {
    try {
      const r: Json = await invoke(cmd, args);
      setMessage(`${cmd}: ${JSON.stringify(r)}`);
    } catch (e) {
      setMessage(`${cmd}: ${String(e)}`);
    }
    // The command's own message stands and the act resolves: a failed refresh adds the fixed line
    // once and never stops what a caller does after it (decide closes its offer).
    await refreshAfterAction(refresh, () => setMessage(withRefreshFailure));
  };
  // A local Start is bound to the current fixed route of this exact ready generation.
  const localStartBound = (submitted: { model: string; modelProvider: string; entryId: string }, source: Json) => {
    const route = localRoute(localViewRef.current, source);
    return !!route && submitted.entryId === LOCAL_ENTRY && submitted.model === route.model && submitted.modelProvider === route.providerId
      && sameActivityGeneration(source?.generation, route.generation);
  };
  const startConversation = async () => {
    const source = currentHost.current;
    const mode = source?.homeRouting?.activeModeHomeClass;
    const submitted = choiceRef.current;
    const epoch = chooserHome.current.epoch;
    if (endpointBusyRef.current || startPendingRef.current || homePendingRef.current || providerReadPending.current || configuredRowChoiceStale() || source?.state !== "ready" || submitted.homeEpoch !== epoch ||
        !submitted.model.trim() || !submitted.modelProvider.trim() || (mode !== "account" && mode !== LOCAL_MODE) ||
        (mode === LOCAL_MODE && !localStartBound(submitted, source)) ||
        !startEntries(source).some(entry => entry.value === submitted.entryId)) return;
    expireEndpointPreview();
    const revision = editRevision.current;
    forkStartRevision.current++;
    continueStartRevision.current++;
    startPendingRef.current = true;
    setStartPending(true);
    try {
      // `generation` is the one shown when the person pressed Start. The current
      // native receiver ignores it; a native follow-up will require it at admission.
      const response: Json = await invoke("thread_start", { model: submitted.model, modelProvider: submitted.modelProvider, entryId: submitted.entryId,
        modeHomeClass: mode, generation: source.generation, role: role || null, preselected: !roleTouched && !!role && role === source?.roleSet?.defaultRole });
      const opened = startedConversationKey(response);
      if (opened) {
        setThreadKey(opened);
        // Consume only the submitted edit, before the independent refresh.
        // Even an edit away and back is a newer choice and must survive.
        if (editRevision.current === revision && chooserHome.current.epoch === epoch) reviseChoice(emptyConversationChoice);
      }
      setMessage(`thread_start: ${JSON.stringify(response)}`);
    } catch (error) {
      setMessage(`thread_start: ${String(error)}`);
    } finally {
      startPendingRef.current = false;
      setStartPending(false);
      await refreshAfterAction(refresh, () => setMessage(withRefreshFailure));
    }
  };
  // Keyed oMLX: one local command at a time. Its view is shown only while it
  // describes the current local generation; an attempted key entry is recorded
  // before dispatch because native consumes it even on cancel or unknown outcome.
  const localCommand = async (command: "prepare_local_provider" | "submit_local_provider_key", generation?: Json) => {
    if (localPendingRef.current || homePendingRef.current) return;
    localPendingRef.current = true; setLocalPending(true); setLocalMessage(null);
    const sequence = ++localSequence.current;
    const what = command === "prepare_local_provider" ? "oMLX preparation" : "oMLX key entry";
    if (generation) { const recorded = recordAttemptedLocalEntry(generationKey(generation)); setLocalAttempted(previous => [...new Set([...previous, ...recorded])]); }
    try {
      const view = localViewFrom(await invoke(command, generation ? { generation } : undefined));
      if (!view) { setLocalView(null); setLocalMessage({ kind: "alert", text: `${what}: the reply was not an oMLX status, so nothing from it is shown.` }); }
      else {
        setLocalView(view);
        if (generation) setLocalMessage(view.credentialState === "configured-not-verified"
          ? { kind: "status", text: "Codex reports the key saved in the oMLX home. It is not verified." }
          : { kind: "status", text: "No key was saved: the secure field closed without one." });
      }
    } catch (error) {
      // A refusal (including an administrator configuration Codex reads above
      // the App's settings) supplies no key state; an earlier view is withdrawn.
      setLocalView(null); setLocalMessage({ kind: "alert", text: `${what} did not complete: ${String(error)}` });
      // Refused at a reading, before native began the entry: it can be offered again.
      if (generation && readingSentence(error)) { const key = generationKey(generation); forgetAttemptedLocalEntry(key); setLocalAttempted(previous => previous.filter(item => item !== key)); }
    }
    finally {
      // The latch is held through this refresh, which cannot replace a newer
      // observation or home navigation that arrived while it was read.
      try {
        await refreshAfterAction(() => refreshEffectiveAccessSettings(() => sequence === localSequence.current && !homePendingRef.current),
          () => setLocalMessage(previous => ({ kind: "alert", text: withRefreshFailure(previous?.text) })));
      }
      finally { localPendingRef.current = false; setLocalPending(false); }
    }
  };
  const localAccess: LocalAccess = { view: localView, attempted: localAttempted, pending: localPending, message: localMessage,
    prepare: () => { void localCommand("prepare_local_provider"); }, enterKey: generation => { void localCommand("submit_local_provider_key", generation); },
    // A settings save, or one whose outcome is not established, can change the route and the key
    // state: what was shown is withdrawn (and any chosen local route with it) until it is read again.
    settingsTouched: () => { localSequence.current++; setLocalView(null);
      setLocalMessage({ kind: "status", text: "The local model settings were saved or their save did not complete. The connection and key state shown before are withdrawn; prepare the oMLX connection again to read them." }); } };
  const homeAction = async (command: string, args: Record<string, unknown>) => {
    const navigating = command === "select_home" || command === "open_waiting_requests";
    if (navigating) {
      if (homePendingRef.current) return;
      homePendingRef.current = true;
      setHomePending(true);
      // Same-home request navigation preserves the separate unsent chooser.
      // A home choice invalidates it at intent, even if the snapshot returns here.
      if (command === "select_home" || args.modeHomeClass !== currentHost.current?.homeRouting?.activeModeHomeClass) {
        chooserHome.current = { ...chooserHome.current, epoch: chooserHome.current.epoch + 1 };
        reviseChoice(emptyConversationChoice);
      }
    }
    try {
      const result: Json = await invoke(command, args);
      // The command's outcome stands: a refresh that fails after it does not make the command look
      // failed. It adds the fixed line once to the App line, nothing raw, and gives no snapshot.
      const snapshot: Json = await refreshAfterAction(refresh, () => setMessage(withRefreshFailure));
      return { result, snapshot };
    }
    finally { if (navigating) { homePendingRef.current = false; setHomePending(false); } }
  };
  // Start / Stop / Restart Codex: one at a time; the host asks first for Stop and Restart.
  const [processBusy, setProcessBusy] = useState(false);
  const processAct = async (cmd: string, args: Record<string, unknown>) => {
    setProcessBusy(true);
    try {
      const r: Json = await invoke(cmd, args);
      setMessage(r?.state === "cancelled" ? `${r.action}: ${r.reading}` : cmd === "codex_stop" ? `${r?.action}: see the outcome under Codex host.` : `${cmd}: ${JSON.stringify(r)}`);
    } catch (e) {
      setMessage(`${cmd}: ${String(e)}`);
    } finally {
      // The outcome and the busy state are set first; a failed refresh adds the fixed line once.
      setProcessBusy(false);
      await refreshAfterAction(refresh, () => setMessage(withRefreshFailure));
    }
  };

  const ordinarySend = (generation: Json, threadId: string, text: string, mode?: "plan" | "default", model?: string, effort?: string) =>
    invoke<Json>("conversation_send_text", { generation, threadId, text, mode: mode ?? null, ...(model ? { model } : {}), ...(effort ? { effort } : {}) });
  const observeOrdinaryView = async (request: OrdinaryTextRequest, isCurrent: () => boolean) => {
    const viewAtRead = currentHost.current;
    if (!isCurrent() || !sameActivityGeneration(viewAtRead?.generation, request.generation)) throw new Error("The original conversation/source was superseded; its view was not applied");
    const snapshotRead = await readHost(invoke<Json>("host_status")); const snapshot: Json = snapshotRead.snapshot;
    if (!isCurrent() || currentHost.current !== viewAtRead || !sameActivityGeneration(currentHost.current?.generation, request.generation) || !sameActivityGeneration(snapshot?.generation, request.generation)) {
      throw new Error("A newer conversation/source observation superseded this original refresh; its view was not applied");
    }
    applyHost(snapshotRead);
  };
  const conversationAction = async (command: "conversation_steer_text" | "conversation_interrupt", args: Record<string, unknown>): Promise<boolean> => {
    // Capture before native dispatch, not after it. Epochs also invalidate an
    // away-and-back choice whose final generation/thread happens to match.
    const sourceAtDispatch = currentHost.current;
    const choiceRevision = threadChoiceRevision.current, homeEpoch = chooserHome.current.epoch, sourceEpoch = actionSource.current.epoch;
    const current = () => threadChoiceRevision.current === choiceRevision && chooserHome.current.epoch === homeEpoch
      && actionSource.current.epoch === sourceEpoch && !homePendingRef.current
      && sameActivityGeneration(currentHost.current?.generation, args.generation);
    const original = { command, args: structuredClone(args) };
    setConversationOutcome({ ...original, native: "pending" });
    let acknowledged = false, error: string | undefined;
    try { await invoke(command, args); acknowledged = true; }
    catch (e) { error = String(e); }
    const outcome = { ...original, native: acknowledged ? "acknowledged" as const : "failed" as const, error };
    // The result is readable while its optional observer read waits, and keeps
    // the original source even when the selected conversation has changed.
    setConversationOutcome(outcome);
    try {
      if (!current() || currentHost.current !== sourceAtDispatch) throw new Error("Original view refresh superseded before reading; no old snapshot was applied");
      const snapshotRead = await readHost(invoke<Json>("host_status")); const snapshot: Json = snapshotRead.snapshot;
      if (!current() || currentHost.current !== sourceAtDispatch || !sameActivityGeneration(snapshot?.generation, args.generation)) {
        throw new Error("Original view refresh superseded while reading; no old snapshot was applied");
      }
      applyHost(snapshotRead);
    } catch (e) { setConversationOutcome({ ...outcome, observationLimit: observationText(e) }); }
    // A refusal never clears text. A skipped/failed read never rewrites the
    // native result, and a superseded acknowledgment never clears a new owner.
    return acknowledged && current();
  };

  const readOriginalRequest: ReadRequestCustody = async r => {
    const scope = requestScopeKey(r);
    try {
      const snapshot = await refresh();
      const current = (snapshot?.serverRequests ?? []).find((entry: Json) => requestScopeKey(entry) === scope);
      return current ? { scope, available: true, state: current.state } : { scope, available: false, reason: "The original request is not present in this source view." };
    } catch (error) { return { scope, available: false, reason: String(error) }; }
  };
  const readRequestCustody: ReadRequestCustody = async r => {
    const scope = requestScopeKey(r);
    const previous = replyObservationsRef.current[scope];
    const custody = await readOriginalRequest(r);
    // A stale observer completion cannot replace a newer command/read result.
    if (previous && replyObservationsRef.current[scope] === previous) observeReply({ ...previous, custody });
    return custody;
  };
  const answerRequest: RequestAnswer = (r, answer) => {
    const scope = requestScopeKey(r);
    const pending = pendingReplies.current.get(scope);
    if (pending) return pending;
    const previous = replyObservationsRef.current[scope];
    if (requestReplyGuarded(previous, scope)) return Promise.resolve(previous);
    observeReply({ scope, command: { kind: "pending" }, custody: { scope, available: false } });
    // Only this IPC phase holds the entered answer. The App owner retains
    // safe observations, and drops its promise latch when IPC completes.
    const command = Promise.resolve().then(() => {
      const input = answer;
      answer = undefined;
      return invoke<Json>("answer_native_request", { generation: r.generation, requestId: r.requestIdentity, answer: input });
    }).then<RequestReplyObservation["command"], RequestReplyObservation["command"]>(result => {
      // The Host reports a local write separately from supplier acknowledgment.
      // Native confirmation dismissal resolves without attempting that write.
      if (result && !Object.hasOwn(result, "error") && result.replyWriteResult === "written" && result.acknowledgment === "not-observed" && result.state !== "dismissed") return { kind: "written" };
      if (result?.state === "dismissed" && result.replyWriteResult === "not-attempted" && !Object.hasOwn(result, "error")) return { kind: "dismissed" };
      return { kind: "unconfirmed", writeResult: ["write-failed", "unknown", "not-attempted"].includes(result?.replyWriteResult) ? result.replyWriteResult : "unconfirmed response" };
    }, error => ({ kind: "rejected", reason: String(error) }));
    const operation = command.then(async result => {
      pendingReplies.current.delete(scope);
      const received = observeReply({ scope, command: result, custody: { scope, available: false, reason: "Reading the original request state." } });
      setMessage(`Native answer: ${JSON.stringify(result)}`);
      // Observer failure cannot replace the command's actual outcome or reason.
      const custody = await readOriginalRequest(r);
      if (replyObservationsRef.current[scope] === received) return observeReply({ ...received, custody });
      return replyObservationsRef.current[scope];
    });
    pendingReplies.current.set(scope, operation);
    return operation;
  };
  // WI-3: opening a conversation from the indicator shows its cards; it answers nothing.
  const openRequests = async (group: WaitingRequestGroup) => {
    if (homePendingRef.current) return;
    const revision = threadChoiceRevision.current;
    const viewAtIntent = currentHost.current;
    try {
      // Cross-home navigation uses the home controls' chooser boundary.
      // The native command validates the original group,
      // not a bare thread ID or the active home's lookalike conversation.
      const opened = await homeAction("open_waiting_requests", { modeHomeClass: group.modeHomeClass, generation: group.generation, threadId: group.threadId });
      if (!opened) return;
      const { result, snapshot } = opened;
      // No status was read after the command: the fixed line is shown; nothing is navigated.
      if (snapshot === undefined) return;
      const same = (a: Json, b: Json) => JSON.stringify(a) === JSON.stringify(b);
      // React may batch the new snapshot until this callback finishes. Use it
      // when no newer view rendered; otherwise the newer rendered source wins.
      const viewNow = currentHost.current === viewAtIntent ? snapshot : currentHost.current;
      if (threadChoiceRevision.current !== revision || result?.modeHomeClass !== group.modeHomeClass || !same(result?.generation, group.generation) || result?.threadId !== group.threadId ||
          snapshot?.state !== "ready" || snapshot?.homeRouting?.activeModeHomeClass !== group.modeHomeClass || !same(snapshot?.generation, group.generation) ||
          viewNow?.homeRouting?.activeModeHomeClass !== group.modeHomeClass || !same(viewNow?.generation, group.generation)) {
        setMessage("Waiting-request navigation superseded or its original source is no longer current; refresh the overview."); return;
      }
      const current = result.threadLoaded && (snapshot.threads ?? []).find((t: Json) => t.threadId === group.threadId && same(t.generation, group.generation));
      setThreadKey(current ? JSON.stringify([current.generation, current.threadId]) : "");
      revealWorkspaceTarget(current ? "conversation" : "other-requests");
    } catch (error) { setMessage(`Waiting-request navigation: ${String(error)}`); }
  };
  const forkContextCurrent = (scope: ForkScope, snapshot: Json) =>
    forkSequence.current === scope.sequence && threadChoiceRevision.current === scope.choiceRevision && chooserHome.current.epoch === scope.homeEpoch &&
    forkStartRevision.current === scope.startRevision && !startPendingRef.current && !homePendingRef.current && snapshot?.state === "ready" && snapshot?.generationClosed !== true &&
    snapshot?.homeRouting?.activeModeHomeClass === scope.modeHomeClass && sameForkGeneration(snapshot?.generation, scope.generation) &&
    (snapshot?.threads ?? []).some((row: Json) => row.threadId === scope.sourceThread && sameForkGeneration(row.generation, scope.generation));
  // Only an observed admitted row completes pending navigation. A read cannot
  // replay Fork or replace the source/receipt supplied by the original command.
  useEffect(() => {
    if (!pendingFork) return;
    if (!forkContextCurrent(pendingFork, host)) { setPendingFork(null); return; }
    const row = (host?.threads ?? []).find((row: Json) => row.threadId === pendingFork.threadId && sameForkGeneration(row.generation, pendingFork.generation));
    if (row?.forkedFrom?.threadId !== pendingFork.sourceThread || row?.forkedFrom?.reportedForkedFromId !== pendingFork.sourceThread || row?.forkedFrom?.forkRequestRef !== pendingFork.requestRef) return;
    setPendingFork(null);
    setThreadKey(JSON.stringify([pendingFork.generation, pendingFork.threadId]));
  }, [host, pendingFork, threadKey, startPending, homePending]);
  const forkViewRevision = threadChoiceRevision.current;
  const forkConversation = async (generation: Json, sourceThread: string): Promise<void> => {
    if (forkInFlight.current || forkViewRevision !== threadChoiceRevision.current || threadKey !== JSON.stringify([generation, sourceThread])) return;
    const scope: ForkScope = { generation: { appSession: generation?.appSession, home: generation?.home, spawnCounter: generation?.spawnCounter }, sourceThread,
      modeHomeClass: currentHost.current?.homeRouting?.activeModeHomeClass, choiceRevision: threadChoiceRevision.current, homeEpoch: chooserHome.current.epoch,
      startRevision: forkStartRevision.current, sequence: forkSequence.current + 1 };
    if (typeof scope.generation.appSession !== "string" || !scope.generation.appSession || typeof scope.generation.home !== "string" || !scope.generation.home || !Number.isSafeInteger(scope.generation.spawnCounter) || scope.generation.spawnCounter <= 0 ||
        !["account", "api-key", ...(LOCAL_FORK_AVAILABLE ? [LOCAL_MODE] : [])].includes(scope.modeHomeClass)) return;
    forkSequence.current = scope.sequence;
    if (!forkContextCurrent(scope, currentHost.current)) return;
    forkInFlight.current = true;
    setPendingFork(null);
    try {
      const response = await invoke<Json>("conversation_fork", { generation: scope.generation, threadId: sourceThread });
      const target = admittedForkTarget(response, scope);
      if (!target) { setMessage("Fork admission is not confirmed; the current conversation is retained."); }
      else {
        const current = forkContextCurrent(scope, currentHost.current);
        setMessage(`Fork ${target.threadId} was admitted as a same-role copy from conversation ${sourceThread} in the original ${scope.modeHomeClass} home. ${current ? "Reading its original source view." : "Navigation was superseded; no switch was made."} Record publication remains separate.`);
        if (current) setPendingFork({ ...scope, ...target });
      }
    } catch (error) { if (forkContextCurrent(scope, currentHost.current)) setMessage(readingSentence(error) ?? `Fork outcome is not confirmed: ${String(error)}`); }
    finally {
      await refreshAfterAction(async () => {
        const snapshotRead = await readHost(invoke<Json>("host_status"));
        // Ignore a response to an older intent/source; it cannot restore that
        // home over a newer choice or make a stale fork current.
        if (forkContextCurrent(scope, currentHost.current)) applyHost(snapshotRead);
      }, () => { if (forkContextCurrent(scope, currentHost.current)) setMessage(withRefreshFailure); });
      forkInFlight.current = false;
    }
  };
  // Continue-as owns an original native attempt separately from observation.
  // IPC/observer errors never become a claim that no submission was attempted.
  const handoffAction = async (command: "continue_as_send" | "continue_as_send_read", args: Record<string, unknown>): Promise<HandoffSendOutcome> => {
    let outcome: HandoffSendOutcome;
    try { outcome = await invoke<HandoffSendOutcome>(command, args); }
    catch (error) { outcome = { state: "unknown", reason: String(error) }; }
    if (!outcome || !["unsent", "sending", "not-attempted", "sent", "native-failed", "unknown"].includes(outcome.state)) {
      outcome = { state: "unknown", reason: "The original send observation was unavailable." };
    }
    setMessage(`Continue-as: ${outcome.state}${outcome.reason ? ` (${outcome.reason})` : ""}`);
    // The send's outcome stands; a failed refresh adds the fixed line once and nothing raw.
    await refreshAfterAction(refresh, () => {
      outcome = { ...outcome, observationFailure: REFRESH_FAILED };
      setMessage(withRefreshFailure);
    });
    return outcome;
  };
  const runAct: RunAct = async (command, args) => {
    try {
      const result = await invoke(command, args);
      setMessage(`${command}: ${JSON.stringify(result)}`);
      return result;
    } catch (e) { setMessage(`${command}: ${String(e)}`); }
    finally { await refreshAfterAction(refresh, () => setMessage(withRefreshFailure)); }
  };
  // As runAct, but a host error rejects with the host's message, for a start
  // whose own panel reports the outcome (Continue as).
  const startRunAct: RunAct = async (command, args) => {
    try {
      const result = await invoke(command, args);
      setMessage(`${command}: ${result === undefined ? "The host did not report an outcome." : JSON.stringify(result)}`);
      return result;
    } catch (e) { setMessage(`${command}: ${String(e)}`); throw e; }
    finally { await refreshAfterAction(refresh, () => setMessage(withRefreshFailure)); }
  };
  // A bring-back send the host could not confirm withdraws its pre-fill, so its
  // composer and outcome would disappear. Its original attempt (trial or run,
  // prepared message, source, target and text) is captured before the call and
  // kept for this window (bringBackDoubts), so no entry point offers a blind second one.
  useEffect(() => () => resetBringBackDoubts(), []);
  const captureBringBackSend = (source: Json, args: Record<string, unknown>): Omit<BringBackDoubt, "message" | "acknowledged"> | null => {
    const pending = (source?.workflowRoot?.pendingBringBacks ?? []).find((row: Json) => row?.id === args.id);
    const kind = typeof pending?.trial === "string" && pending.trial ? "trial" : typeof pending?.run === "string" && pending.run ? "run" : null;
    if (!kind) return null;
    const ref = kind === "trial" ? pending.trial : pending.run;
    return { kind, ref, sequence: pending.sequence ?? null, draftName: pending.draftName ?? null, preparedId: String(args.id),
      source: structuredClone({ sourceRef: source?.workflowRoot?.context?.sourceRef ?? null, modeHomeClass: source?.homeRouting?.activeModeHomeClass ?? null, generation: source?.generation ?? null }),
      target: structuredClone({ generation: args.generation ?? null, threadId: args.threadId ?? null }), personText: String(args.personText ?? "") };
  };
  // As runAct, but a host error rejects with the host's message (trial sends show it as given).
  const trialRunAct: RunAct = async (command, args) => {
    // Observer limits belong to this original trial attempt, independently of
    // the shared command-result line. Equal result text is not equal custody.
    const source = currentHost.current;
    const relation = { attempt: ++trialObservationSequence.current, command,
      source: structuredClone({ sourceRef: source?.workflowRoot?.context?.sourceRef ?? null, modeHomeClass: source?.homeRouting?.activeModeHomeClass ?? null, generation: source?.generation ?? null }),
      reference: args.reference ?? args.id ?? null,
      target: structuredClone({ generation: args.generation ?? null, threadId: args.threadId ?? null }) };
    // Every bring-back send is checked against the host's current view first:
    // a held doubt or a send of the same results in flight issues nothing.
    const refusal = bringBackRefusal(command, args, source);
    if (refusal) throw Error(refusal);
    setTrialObservation({ relation, limit: null });
    const bringBack = command === "workflow_bring_back_send" ? captureBringBackSend(source, args) : null;
    const flight = bringBack ? sendKey(bringBack.kind, bringBack.ref, bringBack.target) : null;
    if (flight && !beginBringBack(flight)) throw Error("Not sent: these results are being sent to this conversation now.");
    try {
      const result = await invoke(command, args);
      // A send that resolves without a reported outcome is not a confirmed one.
      if (bringBack && (result === undefined || result === null)) noteBringBackDoubt({ ...bringBack, message: "The host did not report the send's outcome.", acknowledged: false });
      setMessage(`${command}: ${result === undefined ? "The host did not report an outcome." : JSON.stringify(result)}`);
      return result;
    } catch (e) { setMessage(`${command}: ${String(e)}`); if (bringBack && !prefillKept(e)) noteBringBackDoubt({ ...bringBack, message: hostMessage(e), acknowledged: false }); throw e; }
    finally {
      if (flight) endBringBack(flight);
      await refreshAfterAction(refresh, () => setTrialObservation(previous => previous?.relation === relation ? { relation, limit: REFRESH_FAILED } : previous));
    }
  };
  // The conversation the panel actually shows (current generation only), so no request is hidden.
  const selectedThread: string | null = (host?.threads ?? []).find((t: Json) => JSON.stringify([t.generation, t.threadId]) === threadKey && JSON.stringify(t.generation) === JSON.stringify(host?.generation))?.threadId ?? null;

  const activityLink: RequestActivityLink = request => {
    const snapshot = currentHost.current;
    const root = (snapshot?.threads ?? []).find((row: Json) => JSON.stringify([row.generation, row.threadId]) === threadKey
      && sameActivityGeneration(row.generation, snapshot?.generation));
    const item = requestItem(request, snapshot?.nativeView);
    if (!root || !item || !(typeof request.requestIdentity === "string" || Number.isSafeInteger(request.requestIdentity))) return null;
    const generation = { appSession: request.generation.appSession, home: request.generation.home, spawnCounter: request.generation.spawnCounter };
    const location = { generation, rootThreadId: root.threadId, threadId: item.threadId, turnId: item.turnId, itemId: item.native.id };
    const scope = requestScopeKey(request), method = request.method;
    const choiceRevision = threadChoiceRevision.current, homeEpoch = chooserHome.current.epoch;
    // An ended source still supplies readable rows. Bind this click to its
    // observed phase so close invalidates an older pending intent, while a
    // fresh click can navigate the same retained source without live authority.
    const phase = JSON.stringify([snapshot.state, snapshot.generationClosed === true, snapshot.nativeViewObservationEnded === true]);
    let current = true;
    const isCurrent = () => {
      const shown = currentHost.current;
      const original = hostRequests(shown).find(row => requestScopeKey(row) === scope && row.method === method
        && row.nativeParameters?.threadId === location.threadId && row.nativeParameters?.turnId === location.turnId && row.nativeParameters?.itemId === location.itemId);
      current = current && threadChoiceRevision.current === choiceRevision && chooserHome.current.epoch === homeEpoch && !homePendingRef.current
        && JSON.stringify([shown?.state, shown?.generationClosed === true, shown?.nativeViewObservationEnded === true]) === phase
        && sameActivityGeneration(shown.generation, generation) && !!original && !!requestItem(original, shown.nativeView)
        && (shown.threads ?? []).some((row: Json) => row.threadId === location.rootThreadId && sameActivityGeneration(row.generation, generation))
        && (location.threadId === location.rootThreadId || activityModel(shown.nativeView, location.rootThreadId).subtree.some(child => child.threadId === location.threadId));
      return current;
    };
    if (!isCurrent()) return null;
    return { open: () => {
      if (isCurrent()) activityNavigationRef.current?.reveal({ location, isCurrent });
    } };
  };

  const openControl = async (requestRef: string) => {
    try {
      setOffer(await invoke("compose_offer", { requestRef }));
      setChoice("");
    } catch (e) {
      setMessage(String(e));
    }
  };

  const decide = async () => {
    if (!offer || !choice) return;
    await act("decide", { offerId: offer.offerId, alternative: choice });
    setOffer(null);
  };

  const outsideRequests = hostRequests(host).filter((request: Json) => requestThread(request) === null || requestThread(request) !== selectedThread);
  // First use: while the launch needs setup, a focused welcome replaces the
  // workspace, whose controls cannot work yet. Everything stays mounted.
  // App data held by another process shows the same focused surface, with its reason.
  const setupRequired = ["setup-required", "data-held", "home-held", "set-aside-occupied"].includes(host?.desktopSetup?.launch?.state);
  // Until the first status read is applied, neither the welcome nor the workspace is in the document,
  // only the line that says the App is starting (or, after FIRST_READ_PATIENCE_MS, taking longer than usual),
  // or that the read failed (firstReadState).
  const firstRead = firstReadState(hostReads);
  return (<DailyWorkspace>
        {firstRead !== "read" && <FirstReadStatus failed={firstRead === "failed"} slow={firstReadSlow} retry={() => { void refresh().catch(() => undefined); }}/>}
        {setupRequired && <FirstUseSetup view={host.desktopSetup}/>}
        {firstRead === "read" && <div hidden={setupRequired}>
        <header className="workspace-heading"><div><h1>Chirality</h1><p>Workflow workspace</p></div><p>Make, try, review and refine workflows through conversation.</p></header>
        <WorkflowAssuranceSetting setting={host?.workflowRoot?.assuranceSetting} act={async (command, args) => commandThenRefresh(() => invoke(command, args), refresh, () => setMessage(withRefreshFailure))}/>
        <nav className="workspace-nav" aria-label="Workspace navigation">
          {WORKSPACE_VIEWS.map(item => <a key={item.id} href={`#${item.target}`} aria-current={taskView === item.id ? "page" : undefined}>{item.label}</a>)}
        </nav>
        <WorkspaceConnectionStatus state={host?.state} setupRequired={host?.desktopSetup?.launch?.state === "setup-required"} savedSetup={!!host?.desktopSetup?.pending} generationClosed={host?.generationClosed} startRefusal={host?.lastStartRefusal} codexHome={host?.codexHome} refusalCause={host?.startRefusalCause} build={host?.build}/>
        </div>}
        <NativeWaitingBridge ready={!!host} report={setMessage} checkpoint={() => ({ signature: JSON.stringify([threadChoiceRevision.current, chooserHome.current.epoch, editRevision.current]),
          pristine: threadChoiceRevision.current === 0 && editRevision.current === 0 })} capture={() => {
          const revision = threadChoiceRevision.current;
          const homeEpoch = chooserHome.current.epoch;
          const chooserRevision = editRevision.current;
          const wasBusy = homePendingRef.current || startPendingRef.current;
          return async (group) => {
              if (wasBusy || homePendingRef.current || startPendingRef.current) {
                  setMessage("Waiting-request navigation refused while another home or conversation operation is pending; choose again from the current menu.");
                  return;
              }
              if (revision !== threadChoiceRevision.current || homeEpoch !== chooserHome.current.epoch || chooserRevision !== editRevision.current) {
                  setMessage("Waiting-request navigation superseded by a newer home or conversation choice; choose again from the current menu.");
                  return;
              }
              await openRequests(group);
          };
      }}/>
        {firstRead === "read" && <div hidden={setupRequired}><WaitingRequestsIndicator overview={host?.waitingRequests} busy={homePending} open={group => { void openRequests(group); }}/></div>}
        <NativeConfirmationContent />
        {firstRead === "read" && <div hidden={setupRequired}>
        {offer && (<section style={{ border: "1px solid #888", padding: 8 }}>
            <h2>Act control: {offer.wording} ({offer.actKind})</h2>
            <p>
              {offer.subject.ref} · {offer.subject.contentIdentity.value}
              <br />
              Purpose: {offer.purpose} · Scope: {offer.scope} · {offer.answers.standing}
            </p>
            {offer.alternatives.map((a: Json) => (<label key={a.id} style={{ display: "block" }}>
                <input type="radio" name="alt" value={a.id} checked={choice === a.id} onChange={() => setChoice(a.id)}/>{" "}
                <b>{a.id}</b> {a.statement} — {a.consequences.join("; ")}
              </label>))}
            <p>The host shows its own confirmation with this text; only that confirmation records the decision.</p>
            <button onClick={decide} disabled={!choice}>Decide…</button> <button onClick={() => setOffer(null)}>Close</button>
          </section>)}
        <div className="workspace-notices"><div id="other-requests">
            {outsideRequests.length > 0 && <h3>Requests outside the selected conversation</h3>}
            {outsideRequests.length > 0 && <p>Requests of the selected conversation are shown beside it. Select another conversation to answer its requests there.</p>}
            {outsideRequests.map((request: Json) => <NativeRequestCard activityLink={activityLink} key={JSON.stringify([request.generation, request.requestIdentity])} request={request} view={host?.nativeView} answer={answerRequest} readRequest={readRequestCustody} place={requestPlace(request, host, appProjectFolder(host))} observation={replyObservations[requestScopeKey(request)]}/>)}
          </div>

  <ActionFeedback message={message}/>
        {trialObservation?.limit && <p role="status" aria-label="Trial view observation limit">
          Trial view refresh unavailable for {trialObservation.relation.command} (attempt {trialObservation.relation.attempt}; prepared message {JSON.stringify(trialObservation.relation.reference)};
          source {trialObservation.relation.source.sourceRef ?? "unavailable"}; home {trialObservation.relation.source.modeHomeClass ?? "unavailable"}; generation {JSON.stringify(trialObservation.relation.source.generation)};
          requested target {JSON.stringify(trialObservation.relation.target)}): {String(trialObservation.limit).replace(/\.$/, "")}. The original command outcome is unchanged.
        </p>}</div>
        <div id="view-conversation" data-workspace-view="conversation" className="workspace-view" hidden={taskView !== "conversation"}>
        <WorkspaceDisclosure id="workspace-start" title="New conversation" description="Model, provider, access entry and role — start explicitly" open={host?.state !== "ready" || !(host?.threads?.length) ? true : undefined}>
          <h2>New conversation</h2>
          <div className="workspace-start-fields">
          <h3>1. How it connects</h3>
          <AccessRouteChoice homeClass={homeClass} modelProvider={modelProvider} entryId={entryId} model={model} disabled={startPending || homePending || providerReading || endpointBusy}
            local={fixedLocal} choose={route => reviseChoice(route)}/>
          {homeClass === "account" && <p aria-label="Local model servers">Custom local providers are not offered from this home. <a href="#workspace-connection">Set up the App’s local model connection</a> under Connection &amp; access, and switch to its home to start a conversation with it.</p>}
          <h3>2. Model</h3>
          <AvailableModels packet={modelObservation?.packet ?? null} current={modelObservationCurrent} reading={modelReading} message={modelObservationMessage}
            model={model} modelProvider={modelProvider} entryId={entryId} read={() => { void readAvailableModels(); }} choose={chooseListedModel}
            setModel={model => reviseChoice({ model })} fixedModel={fixedLocal && entryId === fixedLocal.entryId ? fixedLocal.model : null}
            localHome={homeClass === LOCAL_MODE ? (fixedLocal ? "prepared" : "unprepared") : null}
            disabled={host?.state !== "ready" || !!host?.generationClosed || homeClass !== "account" || startPending || homePending || endpointBusy}/>
          {homeClass === "account" && <details className="workflow-stage"><summary>Advanced: enter a model ID yourself</summary>
          <p><ModelIdField model={model} setModel={model => reviseChoice({ model })}/></p>
          </details>}
          <p>Choose how this conversation connects and a model, then a role. Switching homes never transfers an existing conversation.</p>
          <RoleChoice group="start-thread-role" roleSet={host?.roleSet} limits={host?.roleLimits} role={role} preselected={!roleTouched && !!role && role === host?.roleSet?.defaultRole} setRole={next => { expireEndpointPreview(); roleInitialized.current = true; setRoleTouched(true); setRole(next); }}/></div>
          <p aria-label="New conversation choice">{!model.trim() || !modelProvider.trim() ? "not started — no model selected" : entryCompatible ? `New conversation choice: ${model} via ${modelProvider} (${entryId})` : "Choose an access entry for the current home."}</p>
          <p>
            <button onClick={startConversation} disabled={!!startBlocked} aria-describedby={startBlocked ? "start-conversation-blocked" : undefined}>Start thread</button>
            {startBlocked && <>{" "}<span id="start-conversation-blocked" role="status">{startBlocked}</span></>}
          </p>
          <a href="#workspace-connection">Set up access or start Codex</a>
        </WorkspaceDisclosure>
        <div className="workspace-primary">
          <div className="workspace-primary-column" aria-label="Conversation workspace">
            <ConversationPanel localRoute={fixedLocal} focusComposer={conversationReveal?.target === "ordinary-composer-text" ? conversationReveal.sequence : undefined} composerOffer={composerOffer} preparedReveal={preparedReveal} activityNavigationRef={activityNavigationRef} activityLink={activityLink} forkConversation={forkConversation} handoffSend={(id, text) => handoffAction("continue_as_send", { id, text })} handoffRead={id => handoffAction("continue_as_send_read", { id })} codexBusy={processBusy} host={host} threadKey={threadKey} setThreadKey={setThreadKey} answer={answerRequest} readRequest={readRequestCustody} replyObservations={replyObservations} runAct={runAct} trialRunAct={trialRunAct} startAct={startRunAct} send={ordinarySend} observeOrdinaryView={observeOrdinaryView} checkPlanMode={async (generation) => {
          // The check's own failure stands, with the fixed line after it when the refresh failed too.
          // A completed check whose refresh fails rejects with the fixed line alone: its result is
          // visible only through the refreshed status, and that line says the status was not read.
          let failure: unknown = null, failed = false, refreshFailed = false;
          try { await invoke("collaboration_modes_read", { generation }); }
          catch (error) { failure = error; failed = true; }
          await refreshAfterAction(async () => { applyHost(await readHost(invoke<Json>("host_status"))); }, () => { refreshFailed = true; });
          if (failed) throw refreshFailed ? withRefreshFailure(String(failure)) : failure;
          if (refreshFailed) throw REFRESH_FAILED;
      }} steer={async (generation, threadId, expectedTurnId, text) => {
          return await conversationAction("conversation_steer_text", { generation, threadId, expectedTurnId, text });
      }} submitAttachments={async (generation, threadId, expectedTurnId, text, ownerRef, listRevision, selectionRefs) => {
          return await invoke("submit_attachments", { generation, threadId, expectedTurnId, text, ownerRef, listRevision, selectionRefs });
      }} observeAttachmentView={async (request) => {
          const viewAtRead = currentHost.current;
          const snapshotRead = await readHost(invoke<Json>("host_status")); const snapshot: Json = snapshotRead.snapshot;
          // This read belongs to the original attachment request, not a Home or
          // generation selected while its native response/read was pending.
          if (JSON.stringify(currentHost.current?.generation) !== JSON.stringify(request.generation) || JSON.stringify(snapshot?.generation) !== JSON.stringify(request.generation)) {
              throw new Error("The current source changed; this original request's view was not applied");
          }
          if (currentHost.current !== viewAtRead) {
              throw new Error("A newer view arrived while this original request's refresh was pending; its snapshot was not applied");
          }
          applyHost(snapshotRead);
      }} interrupt={async (generation, threadId, turnId) => {
          return await conversationAction("conversation_interrupt", { generation, threadId, turnId });
      }}/>
            {conversationOutcome && <div aria-label="Original conversation action outcome">
              <p>Original {conversationOutcome.command === "conversation_steer_text" ? "steering" : "interrupt"} request · conversation {conversationOutcome.args.threadId} · Home {conversationOutcome.args.generation?.home} · App session {conversationOutcome.args.generation?.appSession} · spawn {conversationOutcome.args.generation?.spawnCounter} · turn {conversationOutcome.args.expectedTurnId ?? conversationOutcome.args.turnId}.</p>
              <p role="status">{conversationOutcome.native === "pending" ? "Waiting for the original native response."
                : conversationOutcome.native === "failed" ? `Original native request failed: ${conversationOutcome.error}`
                : conversationOutcome.command === "conversation_steer_text" ? "Native steering acknowledgment received; turn replacement and completion remain determined by native events."
                : "Native interrupt acknowledgment received; turn end and rollback are not established by this acknowledgment."} No automatic retry.</p>
              {conversationOutcome.observationLimit && <p role="status">{observationLine(conversationOutcome.observationLimit, "")} The original command outcome is unchanged.</p>}
            </div>}
            <WorkspaceDisclosure id="workspace-attachments" title="Message attachments" description="Select and review files for a message">
              <AttachmentSelectionPanel data={host?.attachmentSelections} act={async (command, args) => {
          await commandThenRefresh(() => invoke(command, args), async () => { applyHost(await readHost(invoke<Json>("host_status"))); }, () => setMessage(withRefreshFailure));
      }}/>
            </WorkspaceDisclosure>
          </div>
        </div>
        </div>
        <div id="view-workflows" className="workspace-view workspace-view-narrow" hidden={taskView !== "run" && taskView !== "make"}>
          <div className="workspace-primary-column" aria-label="Workflow studio">
            <WorkflowRootPanel viewStale={shownBeforePress(hostReads)} readFailure={hostReads.failure} findInHistory={findInHistory} view={taskView} showConversation={showConversation} offerComposer={offerComposer} data={host?.workflowRoot} host={host} operationalReference={threadKey ? conversationFromKey(threadKey) ?? undefined : null} openFileAct={openArrivalFileAct} fileActBusy={fileActBusy} act={(command, args) => { const refusal = bringBackRefusal(command, args, currentHost.current); return refusal ? Promise.reject(Error(refusal)) : invoke<Json>(command, args); }} observeView={refresh} openPreparedMessage={item => { void openPreparedMessage(item); }}/>
        {preparedNotice && <p role="status">{preparedNotice}</p>}
          </div>
        </div>
        <div id="view-history" data-workspace-view="history" className="workspace-view workspace-view-narrow" hidden={taskView !== "history"}>
          <WorkspaceDisclosure id="workspace-history" title="History and recovery" description="Read prior conversations and inspect recovery custody" open>
            <RecoveryCustodyPanel key={JSON.stringify([host?.homeRouting?.activeModeHomeClass, host?.generation])} modeHomeClass={host?.homeRouting?.activeModeHomeClass} generation={host?.generation ?? null} nativeHistoryGeneration={host?.nativeHistory?.generation ?? null} read={() => invoke("read_recovery_custody", { modeHomeClass: host?.homeRouting?.activeModeHomeClass, generation: host?.generation ?? null })} readRequests={(cursor: Json) => invoke("read_recovery_request_history", { modeHomeClass: host?.homeRouting?.activeModeHomeClass, generation: host?.generation ?? null, cursor: cursor ?? null })} retry={(threadId: string) => invoke("recovery_retry", { modeHomeClass: host?.homeRouting?.activeModeHomeClass, generation: host?.generation ?? null, threadId })}/>
        <HistoryPanel host={host} refresh={refresh} threadKey={threadKey} setThreadKey={setThreadKey} captureContinueNavigation={captureContinueNavigation} openConversation={openAdmittedConversation} searchHint={historyHint}/>
          </WorkspaceDisclosure>
        </div>
        <section id="workspace-tools" data-workspace-view="settings" className="workspace-tools workspace-view workspace-view-narrow" aria-label="Workspace tools" hidden={taskView !== "settings"}>
          <h2>Settings &amp; tools</h2>
          <DesktopSetupPanel view={host?.desktopSetup}/>
          <WorkspaceDisclosure id="workspace-connection" title="Connection and access" description="Home, sign-in, provider setup and Codex controls" open={host?.state !== "ready" ? true : undefined}>
            <HomeAccessPanel host={host} resources={{ ...host?.homeResources, namespaceProtection: host?.nativeNamespaces, keyAdmission: host?.keyNamespaceAdmission }} navigating={homePending} readAccount={readAccountStatus} local={localAccess} act={async (command, args) => { await homeAction(command, args); }}/>
            <EffectiveAccessSettingsPanel host={host} navigating={homePending} refresh={refreshEffectiveAccessSettings}/>
  <CodexProcessControls host={host} busy={processBusy} act={(command, args) => { void processAct(command, args); }}/>
          </WorkspaceDisclosure>
          <WorkspaceDisclosure id="workspace-files" title="Files and standing acts" description="Review a saved App-side output and its original act context">
            <FileActPanel command={(name, args) => invoke(name, args)} controlRef={fileActPanel} onBusyChange={setFileActBusy}/>
          </WorkspaceDisclosure>
          <WorkspaceDisclosure id="workspace-records" title="Records and Fleet" description="Project records, capability bindings and cross-source records">
            <RecordsStorePanel store={host?.recordsStore} chain={host?.recordChain} invoke={(command, args) => invoke<Json>(command, args)} refresh={refresh}/>
          <FleetRecordsPanel packet={fleet} error={fleetError} busy={fleetBusy} refresh={() => { void refreshFleet(); }}/>
  <RecordsCapabilityBindings host={host}/>
          </WorkspaceDisclosure>
          <WorkspaceDisclosure id="workspace-evidence" title="Connectors and examination" description="Supplied observations, connector routes and decision packages">
            <ConnectorSourcePanel availability={host?.connectorRouteAvailability} command={(name, args) => invoke(name, args)}/>
        <ConnectorRoutePanel availability={host?.connectorRouteAvailability} state={routeRead} onRead={readRoutes}/>
  <ExternalObservationPanel data={host?.externalObservation} select={async () => {
          try {
              const result: Json = await invoke("select_external_observation");
              setMessage(`External selection: ${result.selection?.state ?? "unknown"} ${result.selection?.stage ?? ""}`);
          }
          catch (e) {
              setMessage(String(e));
          }
          // The selection's own message stands; a failed refresh adds the fixed line once.
          await refreshAfterAction(async () => { applyHost(await readHost(invoke<Json>("host_status"))); }, () => setMessage(withRefreshFailure));
      }}/>

        <TraceReceivingPanel data={host?.traceReceiving} currentContext={{ hostState: host?.state, generation: host?.generation, nativeSupplier: host?.versionIdentity, supplierStanding: host?.supplierStanding, accessSelection: host?.accessSelection, accountObservation: host?.accountObservation, appExecutableIdentity: "not established by this selector" }} select={async (recordKind, evidenceKind) => {
          await commandThenRefresh(async () => {
              const received: Json = await invoke("select_trace_record", { recordKind, evidenceKind });
              setMessage(`Supplied trace selection: ${received.selection?.state ?? "unknown"}`);
          }, async () => { applyHost(await readHost(invoke<Json>("host_status"))); }, () => setMessage(withRefreshFailure));
      }}/>
  <DecisionPackagesPanel view={view} name={name} setName={setName} recordName={() => { void invoke("set_person_name", { name }); }} refresh={refresh} continueRecording={async () => { await act("continue_decision_recording"); }} openControl={openControl}/>
          </WorkspaceDisclosure>
          <WorkspaceDisclosure id="workspace-diagnostics" title="Host diagnostics" description="Source identities, role supply, native envelopes and recovery details">
            <section><h2>Codex host</h2>
          {host?.configurationProblem && <p>Configuration: {host.configurationProblem}</p>}
          <p>
            State: <b>{host?.state}</b> · generation {host?.generation ? JSON.stringify(host.generation) : "—"} · version{" "}
            {host?.versionIdentity?.observedVersionLabel ?? "—"} · verification{" "}
            {host?.verification ? JSON.stringify(host.verification) : "—"}
          </p>
          <p>Supplier standing: {host?.supplierStanding ?? "not started"}</p>
  <SupplyStatus supply={host?.roleSupply}/>
          <RoleHistoryReader scope={JSON.stringify(host?.generation)} ready={host?.state === "ready"} read={() => invoke("role_supply_history", { generation: host?.generation, thread: null })}/>
          {host?.instructionsProblem && <p role="alert">Role guidance store: {host.instructionsProblem}</p>}
  <details><summary>Last native start selection in this home</summary><pre>{JSON.stringify(host?.accessSelection ?? null, null, 2)}</pre></details>
          <p>Account (App-observed, identity not verified): {JSON.stringify(host?.accountObservation ?? { state: "unknown" })}</p>
  <p>Threads: {(host?.threads ?? []).map((t: Json) => `${t.threadId} (${t.status?.type ?? "?"}, gen ${JSON.stringify(t.generation)})`).join(", ") || "none"}</p>


          <h3>Expected network contacts</h3>
          <p>Codex can contact the selected model provider at thread start, before a model turn. This view describes supplier behavior; socket measurements remain separate evidence.</p>
          <ul>{(host?.networkDisclosure?.entries ?? []).map((entry: Json, index: number) => <li key={index}>{entry.purpose} · {entry.phase} · {entry.destination} · {entry.detail ?? entry.condition}</li>)}</ul>
          <details>
            <summary>Lifecycle events ({host?.lifecycle?.length ?? 0}) and frames ({host?.journal?.length ?? 0})</summary>
            <pre>{JSON.stringify({ lifecycle: host?.lifecycle, clientRequests: host?.clientRequests }, null, 2)}</pre>
          </details></section>
            <section>
          <h2>Native requests and execution</h2>
          <p>Recovery initialization: {host?.recoveryInitialization?.state ?? "not-initialized"} · host configured: {String(host?.recoveryInitialization?.hostConfigured ?? false)}</p>
          {(host?.recoveryInitialization?.historyLimits ?? []).map((limit: string) => <p role="alert" key={limit}>App history limit: {limit}</p>)}
          <p>SQLite recovery ledger: {host?.recoveryInitialization?.database ?? "location not established"} {host?.recoveryInitialization?.path?.pathDisplayLimit}</p>
          <p>Legacy JSON Lines import location: {host?.recoveryInitialization?.path?.displayPath ?? "location not established"} {host?.recoveryInitialization?.path?.pathDisplayLimit}</p>
          {host?.recoveryInitialization?.configurationError && <p role="alert">Ledger initialization failed: {host.recoveryInitialization.configurationError}. Native supplier processing is not blocked.</p>}
          <p>Directory publication: {host?.recoveryInitialization?.directoryPublication ?? "not established"} · later persistence failure: {host?.recoveryPersistenceError ?? "none reported"}</p>
          <details><summary>Recovery initialization and historical pointer state</summary><pre>{JSON.stringify({ initialization: host?.recoveryInitialization, recovery: host?.recovery }, null, 2)}</pre></details>
          <ObserverAttachment host={host}/>
          {(host?.nativeViewLimits ?? []).map((limit: string, i: number) => <p key={i}>{limit}</p>)}
                  <a href="#file-acts">Act on a saved App-side output file (select it explicitly)</a>
          <details><summary>Native plans, tools, goals, turns and descendants as received (JSON)</summary><pre>{JSON.stringify({ current: host?.nativeView, observationEnded: host?.nativeViewObservationEnded, priorObservations: host?.priorNativeViews, recovery: host?.observerRecovery }, null, 2)}</pre></details>
          <details><summary>Raw native envelopes (including unknown fields)</summary><pre>{JSON.stringify(host?.journal, null, 2)}</pre></details>
        </section>
          </WorkspaceDisclosure>
        </section>
        </div>}
      </DailyWorkspace>);
}
