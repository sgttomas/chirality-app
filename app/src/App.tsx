import { NativeWaitingBridge } from "./NativeWaitingBridge";
import { ConnectorSourcePanel } from "./ConnectorSourcePanel";
import { FleetRecordsPanel, readFleetPacket, type FleetPacket } from "./FleetRecordsPanel";
import { ConnectorRoutePanel, emptyRouteRead, routeReadTransition, type RouteReadState, type RouteView } from "./ConnectorRoutePanel";
// The interface reads host snapshots and asks the host to act. It holds no pipe
// (HOSTING H2), writes no record and cannot capture an act: the native
// confirmation is the host's (AAC §6.2 P-2). Views per DECISION_VIEW.md §4.
import { useCallback, useEffect, useRef, useState } from "react";
import { invoke } from "@tauri-apps/api/core";
import { appHome, CodexProcessControls, stopLabel } from "./CodexControls";
import { ContinueAsPanel, ModelProviderFields, RoleChoice, RoleHeader, RoleHistoryReader, SupplyStatus, type HandoffSendOutcome } from "./ConversationRoles";
import { EXACT_TEXT } from "./exactText";
import { ArrivalRecord, HistoryReferenceNotice, RunBringBack, RunPanel, SelectedWorkflow, hasUnsavedHistoryReference, isRecordedRun, runBringBackDefault, type OpenArrivalFileAct } from "./RunPanel";
import { chatWorkflow, workflowArguments, workflowContext } from "./workflowSelection";
import { FileActPanel, type FileActPanelHandle } from "./FileActPanel";
import { NativeActivityView } from "./NativeActivity";
import { ContinuationContext, historyPageBinding, StoredItemPage, StoredTurnPage } from "./NativeHistory";
import { ObserverAttachment } from "./ObserverAttachment";
import { PlanModeControl } from "./PlanMode";
import { NativeRequestCard, WaitingRequestsIndicator, answerable, hostRequests, requestThread, requestScopeKey, requestReplyGuarded, type RequestAnswer, type ReadRequestCustody, type RequestReplyObservation, type WaitingRequestGroup } from "./RequestCards";
import { RunOffer, type RunAct } from "./RunOffers";
import { RecoveryCustodyPanel } from "./RecoveryCustodyPanel";
import { LastCleanTrialLine, WorkflowDraftsView } from "./WorkflowDrafts";
import { LibraryEntries } from "./LibraryEntries";
import { WorkflowRegistrationReview } from "./WorkflowRegistrationReview";
import { BringBackComposer, CleanTrialPanel, DelegatedTrialComposer, composersFor, hostMessage } from "./TrialComposer";
import { DIGEST_LIMIT, digestComparison, readablePaths, reviewDigest, suppliedSummary, type ReviewDigestView } from "./presentation";

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
const startEntries = (host: Json) => host?.homeRouting?.activeModeHomeClass === "api-key"
  ? [{ value: "api-key", label: "API key in separate configured key home" }]
  : [{ value: "chatgpt-account", label: "ChatGPT account in configured account home" }, { value: "local-provider", label: "Configured local provider" }];

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

export function ConversationPanel({ host, threadKey, setThreadKey, answer, readRequest, replyObservations, runAct, trialRunAct, send, steer, submitAttachments, interrupt, checkPlanMode, codexBusy, forkConversation, handoffSend, handoffRead }: { forkConversation?: (generation: Json, sourceThread: string) => Promise<void>; handoffSend?: (id: string, text: string) => Promise<HandoffSendOutcome>; handoffRead?: (id: string) => Promise<HandoffSendOutcome>; codexBusy: boolean; host: Json; threadKey: string; setThreadKey: (key: string) => void; trialRunAct?: RunAct; answer: RequestAnswer; readRequest?: ReadRequestCustody; replyObservations?: Record<string, RequestReplyObservation>; runAct: RunAct; checkPlanMode: (generation: Json) => Promise<void>; submitAttachments: (generation: Json, thread: string, expected: string | null, text: string, owner: string, revision: number, refs: string[]) => Promise<void>; send: (generation: Json, thread: string, text: string, mode?: "plan" | "default") => Promise<void>; steer: (generation: Json, thread: string, expected: string, text: string) => Promise<void>; interrupt: (generation: Json, thread: string, turn: string) => Promise<void> }) {
  const [turnId, setTurnId] = useState<string>("");
  const [offerBusy, setOfferBusy] = useState(false);
  const [text, setText] = useState<string>("");
  const [ownBusy, setBusy] = useState<string>("");
  const [forkBusy, setForkBusy] = useState(false);
  const forking = useRef(false);
  // While Start/Stop/Restart Codex runs, no text, steer or attachment send is offered
  // (the host also refuses new turns once a stop is confirmed).
  const busy = ownBusy || (codexBusy ? "Stop or Restart Codex in progress" : "");
  const [error, setError] = useState<string>("");
  const generationKey = JSON.stringify(host?.generation);
  const currentThreads = (host?.threads ?? []).filter((thread: Json) => JSON.stringify(thread.generation) === generationKey);
  const selected = currentThreads.find((thread: Json) => JSON.stringify([thread.generation, thread.threadId]) === threadKey);
  const liveTurns = (host?.conversationTurns ?? []).filter((turn: Json) => selected && JSON.stringify(turn.generation) === generationKey && turn.threadId === selected.threadId && turn.nativeTurn?.status === "inProgress" && !turn.observationEnded && !turn.terminalEventObserved);
  const live = liveTurns.find((turn: Json) => turn.turnId === turnId);
  const steering = (host?.steeringTargets ?? []).find((row: Json) => selected && JSON.stringify(row.generation) === generationKey && row.threadId === selected.threadId);
  const steeringTarget = steering?.target && JSON.stringify(steering.target.generation) === generationKey && steering.target.threadId === selected?.threadId ? steering.target : null;
  const alreadyRequested = (host?.turnInterruptRequests ?? []).some((request: Json) => live && JSON.stringify(request.binding?.generation) === generationKey && request.binding?.threadId === live.threadId && request.binding?.turnId === live.turnId && (request.clientRequest?.outcome === "response-observed-result" || (request.clientRequest?.outcome === "pending" && request.clientRequest?.writeResult === "written")));
  const sendText = async (mode?: "plan" | "default") => {
    if (!selected || !text || busy) return;
    setBusy(mode ? `sending in ${mode} mode` : "sending"); setError("");
    try { await send(selected.generation, selected.threadId, text, mode); setText(""); }
    catch (e) { setError(String(e)); }
    finally { setBusy(""); }
  };
  const steerText = async () => {
    if (!selected || !steeringTarget || !text || busy) return;
    setBusy("steering"); setError("");
    try { await steer(selected.generation, selected.threadId, steeringTarget.turnId, text); setText(""); }
    catch (e) { setError(String(e)); }
    finally { setBusy(""); }
  };
  const attachmentText = async (expected: string | null) => {
    const selection = host?.attachmentSelections;
    if (!selected || !selection?.ownerRef || !(selection.selections ?? []).length || busy) return;
    setBusy(expected ? "steering with attachments" : "sending with attachments"); setError("");
    try {
      await submitAttachments(selected.generation, selected.threadId, expected, text, selection.ownerRef, selection.listRevision, selection.selections.map((row: Json) => row.selection.selectionRef));
      setText("");
    } catch (e) { setError(String(e)); }
    finally { setBusy(""); }
  };
  const interruptTurn = async () => {
    if (!selected || !live || ownBusy || alreadyRequested) return;
    setBusy("interrupting"); setError("");
    try { await interrupt(live.generation, live.threadId, live.turnId); }
    catch (e) { setError(String(e)); }
    finally { setBusy(""); }
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
  const trialConversation = (workflowRoot?.trialConversations ?? []).find((row: Json) => selected && row?.threadId === selected.threadId);
  const trialsStartedHere = (workflowRoot?.trialsStartedHere ?? []).find((row: Json) => selected && row?.threadId === selected.threadId);
  // Keys of this section's direct children must differ from each other: the role
  // header and the activity view once shared the thread ID as key, and React then
  // left the previous conversation's header mounted on every switch (witness
  // 2026-10-10 D-1). Each per-conversation child keys on its own prefix.
  return <section id="conversation">
    <h2>Conversation text and turn control</h2>
    <label>Current-generation conversation <select disabled={!!ownBusy} value={threadKey} onChange={e => { setThreadKey(e.target.value); setTurnId(""); setError(""); }}>
      <option value="">Select a conversation</option>
      {currentThreads.map((thread: Json) => <option key={JSON.stringify([thread.generation, thread.threadId])} value={JSON.stringify([thread.generation, thread.threadId])}>{thread.threadId} · {thread.model ?? "model not reported"} via {thread.modelProvider ?? "provider not reported"}</option>)}
    </select></label>
    {selected && <RoleHeader key={`role-header:${JSON.stringify([selected.generation, selected.threadId])}`} thread={selected} limits={host?.roleLimits} busy={!!busy || forkBusy} ready={host?.state === "ready"} trialConversation={trialConversation} trialsStartedHere={trialsStartedHere}
      readSupplyHistory={() => invoke("role_supply_history", { generation: selected.generation, thread: selected.threadId })}
      continueAs={role => { void roleAct("asking for a handoff summary", "continue_as_begin", { generation: selected.generation, threadId: selected.threadId, role }); }}
      fork={() => { void forkSelected(); }} />}
    {selected && <ContinuationContext key={`prior-work:${JSON.stringify([selected.generation, selected.threadId, selected.resumeRequestRef])}`} host={host} thread={selected} />}
    {threadKey && !selected && <p>Selected conversation is no longer available in this generation; choose a current conversation.</p>}
    {handoffs.map((handoff: Json) => <ContinueAsPanel key={handoff.id} handoff={handoff} entries={startEntries(host)} busy={!!busy} ready={host?.state === "ready"}
      start={choice => { void roleAct("starting the new conversation", "thread_start", { ...choice, modeHomeClass: host?.homeRouting?.activeModeHomeClass, role: handoff.targetRole ?? null, preselected: false, continueAs: handoff.id }); }}
      send={draft => handoffSend ? handoffSend(handoff.id, draft) : Promise.resolve({ state: "unknown", reason: "The original handoff sender is unavailable." })}
      read={handoffRead ? () => handoffRead(handoff.id) : undefined}
      open={() => { const started = handoff.started; if (started) setThreadKey(JSON.stringify([started.generation, started.threadId])); }}
      dismiss={() => { void roleAct("closing the handoff", "continue_as_dismiss", { id: handoff.id }); }} />)}
    {composers.clean.map((pending: Json) => <CleanTrialPanel key={`clean-trial:${pending.reference}`} pending={pending} roleSet={host?.roleSet} limits={host?.roleLimits} entries={startEntries(host)}
      modeHomeClass={host?.homeRouting?.activeModeHomeClass} busy={!!busy} ready={host?.state === "ready"} act={trialAct} />)}
    {composers.delegated.map((pending: Json) => <DelegatedTrialComposer key={`trial:${selected?.threadId}:${pending.reference}`} pending={pending} conversations={currentThreads} busy={!!busy} ready={host?.state === "ready"} act={trialAct} />)}
    {composers.bringBacks.map((pending: Json) => <BringBackComposer key={`bring-back:${selected?.threadId}:${pending.id}`} pending={pending} conversations={currentThreads} busy={!!busy} ready={host?.state === "ready"} act={trialAct} />)}
    <NativeActivityView key={`activity:${selected?.threadId ?? ""}`} view={host?.nativeView} threadId={selected?.threadId} runs={runs} offers={offers}
      trialTurns={workflowRoot?.trialTurns} trialChildren={workflowRoot?.trialChildren} delegation={selected?.delegation}
      stopLabelFor={(thread, turn) => stopLabel(host?.codexStops, thread, turn, host?.stopRequests, appHome(host?.homeRouting?.activeModeHomeClass))}
      renderOffer={offer => <RunOffer offer={offer} generation={host?.generation} ready={host?.state === "ready"} busy={offerBusy} act={offerAct} />} />
    {selected && <div aria-label="Requests from Codex in this conversation">
      <h3>Requests from Codex in this conversation ({requests.filter(answerable).length} waiting)</h3>
      {ordered.length === 0 && <p>No requests from Codex in this conversation.</p>}
      {ordered.map((request: Json) => <NativeRequestCard key={JSON.stringify([request.generation, request.requestIdentity])} request={request} view={host?.nativeView} answer={answer} readRequest={readRequest} observation={replyObservations?.[requestScopeKey(request)]} />)}
    </div>}
    <p><label>Text <textarea disabled={!!busy} value={text} onChange={e => setText(e.target.value)} rows={4} style={{ display: "block", width: "100%" }} /></label></p>
    <button disabled={host?.state !== "ready" || !selected || !text || !!busy} onClick={() => { void sendText(); }}>{(host?.attachmentSelections?.selections ?? []).length > 0 ? "Send text only" : "Send text"}</button>
    {selected && <PlanModeControl planMode={host?.planMode} requested={(host?.requestedModes ?? []).find((r: Json) => JSON.stringify(r.generation) === generationKey && r.threadId === selected.threadId) ?? null}
      ready={host?.state === "ready"} busy={!!busy} hasText={!!text}
      check={() => { setError(""); checkPlanMode(selected.generation).catch(e => setError(String(e))); }} send={mode => { void sendText(mode); }} />}
    {(host?.attachmentSelections?.selections ?? []).length > 0 && <p>This plain-text action excludes the selected attachments. Use the explicit ordered-attachment action to include the entire private selection.</p>}
    <p>Text is sent unchanged to the selected native conversation. Its role, model and provider remain the conversation's existing settings.</p>
    {(host?.attachmentSelections?.selections ?? []).length > 0 && <div>
      <button disabled={host?.state !== "ready" || !selected || !!busy || host?.attachmentCustody?.state !== "opened"} onClick={() => attachmentText(null)}>Send text and ordered attachments</button>{" "}
      <button disabled={host?.state !== "ready" || !selected || !steeringTarget || !!busy || host?.attachmentCustody?.state !== "opened"} onClick={() => attachmentText(steeringTarget.turnId)}>Steer current turn with ordered attachments</button>
      <p>Every selected source is revalidated as one whole list. Source/custody/context failures retain the draft and evidence; no text-only fallback or automatic resend. Native acknowledgments remain separate from completion and provider uptake.</p>
      {host?.attachmentCustody?.state !== "opened" && <p>Attachment custody unavailable: {host?.attachmentCustody?.error}. Plain-text controls remain available.</p>}
    </div>}
    <SteeringControl target={steeringTarget} reason={steering?.reason} ready={host?.state === "ready" && !!selected} busy={!!busy} text={text} submit={() => { void steerText(); }} />
    <label>Observed live turn <select disabled={!!ownBusy} value={turnId} onChange={e => setTurnId(e.target.value)}><option value="">Select a live turn</option>{liveTurns.map((turn: Json) => <option key={turn.turnId} value={turn.turnId}>{turn.turnId} · {turn.nativeTurn.status}</option>)}</select></label>{" "}
    <button disabled={host?.state !== "ready" || !live || !!ownBusy || alreadyRequested} onClick={interruptTurn}>Interrupt selected live turn</button>
    <p>An interrupt acknowledgment does not establish turn end or rollback. Turn status comes from native observations.</p>
    {(host?.conversationTurns ?? []).filter((turn: Json) => turn.terminalEventObserved && turn.nativeTurn?.status === "inProgress").map((turn: Json) => <p key={JSON.stringify([turn.generation, turn.threadId, turn.turnId])}>Native turn inconsistency: {turn.threadId}/{turn.turnId} has a terminal event observation and contradictory progress status; interruption is unavailable.</p>)}
    {(host?.conversationTurns ?? []).flatMap((turn: Json) => (turn.inconsistencyLimits ?? []).map((limit: Json, index: number) => <p key={JSON.stringify([turn.generation, turn.threadId, turn.turnId, index])}>Native lifecycle limit for {JSON.stringify(turn.generation)} · {turn.threadId}/{turn.turnId}: {JSON.stringify(limit)}</p>))}
    {alreadyRequested && <p>Interrupt already requested; awaiting native turn status.</p>}
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

export function HistoryPanel({ host, refresh, threadKey, setThreadKey, captureContinueNavigation }: {
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
  const history = host?.nativeHistory;
  const selected = history?.selected;
  const generation = history?.generation;
  const epoch = history?.selectionEpoch;
  const available = host?.state === "ready" && history?.state === "history-receiving" && JSON.stringify(generation) === JSON.stringify(host?.generation);
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
    setContinueNotice("Continue admission confirmed; opened the matched conversation. No automatic resend.");
    setError("");
    setThreadKey(JSON.stringify([ticket.generation, ticket.threadId]));
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
      try {
        if (navigation) await navigation.observe();
        else await refresh();
      } catch (e) { setError(String(e)); }
      if (navigation) {
        setPendingContinue(ticket);
        setContinueNotice(ticket ? "Continue admission confirmed; waiting for its matched current conversation view. No automatic retry."
          : "No matched Continue admission was returned. The conversation selection is retained; no automatic retry.");
      }
      busyRef.current = false;
      setBusy(false);
    }
  };
  const select = async (threadId: string) => {
    if (!threadId || busyRef.current) return;
    busyRef.current = true;
    operation.current++;
    activeNavigation.current = null;
    setPendingContinue(null); setContinueNotice("");
    setBusy(true); setError("");
    try { await invoke("history_select", { generation, selectionEpoch: epoch, threadId }); }
    catch (e) { setError(String(e)); }
    finally { try { await refresh(); } catch (e) { setError(String(e)); } busyRef.current = false; setBusy(false); }
  };
  const pageButtons = (action: string, page: Json, reference: string | null = null, pageDirection = direction) => <span>
    {typeof page?.nextCursor === "string" && <button disabled={!available || busy} onClick={() => run(action, page.nextCursor, reference, pageDirection)}>Next page</button>}
    {typeof page?.backwardsCursor === "string" && <button disabled={!available || busy} onClick={() => run(action, page.backwardsCursor, reference, pageDirection === "desc" ? "asc" : "desc")}>Previous page</button>}
    <small> Cursor: {page === null || page === undefined ? "not read" : page.nextCursor === null ? "exhausted" : page.nextCursor === undefined ? "not reported" : "available"}</small>
  </span>;
  return <section>
    <h2>Stored native conversations and history</h2>
    <p>These disposable pages come from the selected native home. Reading history does not make a conversation operational. Original App role evidence remains unknown after a cold App restart.</p>
    <label>Page direction <select value={direction} disabled={busy} onChange={e => setDirection(e.target.value)}><option value="desc">Newest first</option><option value="asc">Oldest first</option></select></label>{" "}
    <button disabled={!available || busy} onClick={() => run("list")}>Read stored conversations</button>{" "}{pageButtons("list", history?.listPage, null, history?.listDirection ?? direction)}
    <p><label>Stored conversation <select value={selected?.threadId ?? ""} disabled={!available || busy} onChange={e => select(e.target.value)}><option value="">Select a received conversation</option>{(history?.threads ?? []).map((row: Json) => <option key={row.native.id} value={row.native.id}>{row.native.id} · {row.native.status?.type ?? "status not reported"} · {row.native.preview || "empty preview"}</option>)}</select></label></p>
    {selected && <>
      <p>History state: {selected.state}. App role in force: {JSON.stringify(selected.appRole)}. Native agentRole: {JSON.stringify(selected.metadata?.thread?.agentRole === undefined ? { state: "not reported" } : selected.metadata.thread.agentRole)}.</p>
      {(selected.futureGuidanceNotices ?? []).map((notice: Json) => <p key={notice.path}>{notice.path}: {notice.kind === "not-read" ? `current guidance not compared (${notice.reason})` : notice.reason}; new conversations use the current guidance. This conversation retains its original role.</p>)}
      <button disabled={!available || busy} onClick={() => run("metadata")}>Read metadata</button>{" "}
      <button disabled={!available || busy} onClick={() => run("turns")}>Read turns</button>{" "}
      <button disabled={!available || busy} onClick={() => run("goal")}>Read goal</button>{" "}
      <button disabled={!available || busy} onClick={() => run("continue")}>Continue selected conversation</button>
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
    {busy && <p>Waiting for native protocol response; no automatic retry.</p>}
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
  return JSON.stringify(result);
}

/** The active library's registered revisions (WR §4.6 LS-1). A revision this App
 * process holds a registration or re-confirmation result for is offered Select;
 * the host resolves it from the revision store (SL-1, SL-4). Every row keeps Refine. */
export function RegisteredRevisions({ library, rows, busy, act, chatAvailable = true }:{ library: string; rows: Json[]; busy: boolean; chatAvailable?: boolean; act: (command:string,args:Record<string,unknown>)=>unknown }) {
  return <ul aria-label="Registered revisions in the active library">{rows.map((row:Json)=><li key={`${row.name}@${row.revision}`}>{row.name} · revision {row.sequence} · {row.label}
    {row.selectable===true&&<> <button disabled={busy||!chatAvailable} onClick={()=>act("workflow_select_listed",{libraryRef:library,name:row.name,revision:row.revision})}>Select revision {row.sequence}</button></>}
    {" "}<button disabled={busy} onClick={()=>act("workflow_refine_registered",{name:row.name,revision:row.revision})}>Refine from the revision store…</button></li>)}</ul>;
}

export function RecordsCapabilityBindings({ host }:{ host: Json }) {
  const rows=(host?.threads??[]).filter((row:Json)=>JSON.stringify(row.generation)===JSON.stringify(host?.generation)&&row.recordsCapabilityBinding);
  if (!rows.length) return null;
  return <section aria-label="Conversation records capability"><h3>Conversation records capability</h3>
    {rows.map((row:Json)=><p key={row.threadId}>{row.threadId}: {row.recordsCapabilityBinding.state}. {row.recordsCapabilityBinding.persistence??""}{row.recordsCapabilityBinding.limit?` · ${row.recordsCapabilityBinding.limit}`:""}</p>)}
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

/** RS §13.8: the records store, project identity, package recovery and the
 *  separate explicit import of §13.7 records still in the project. */
export function RecordsStorePanel({ store, act }: { store: Json; act: (command: string, args?: Record<string, unknown>) => Promise<void> }) {
  if (!store) return null;
  const project = store.project;
  const attachment = project?.attachment;
  const retention = project?.retention;
  const packageImport = store.packageImport;
  const packageBlocked = packageImport?.state === "incomplete" || packageImport?.state === "unavailable";
  const kept = retention?.disposition === "kept";
  const identityRepair = !packageBlocked && (retention == null || kept);
  const holdable = kept || retention?.disposition === "disposal incomplete";
  const terminalDisposition = ["disposed", "disposal incomplete", "completion durability uncertain"].includes(retention?.disposition);
  const packageImportable = store.state === "available" && !packageBlocked && !terminalDisposition;
  const packageRepairable = store.state === "available" && !terminalDisposition && packageImport?.canRepair === true;
  return <section aria-label="Records store">
    <h3>Records store</h3>
    {store.state === "available"
      ? <p>Store: {String(store.root)} ({String(store.placement)}).</p>
      : <p role="alert">No records store: {String(store.error)}. Nothing is recorded; there is no fallback.</p>}
    {(store.limits ?? []).map((l: string) => <p key={l} role="note">{l}</p>)}
    {project && <>
      <p>Project: {attachment?.projectId ? String(attachment.projectId) : "no identity yet"}; reading {String(project.reading ?? project.state)}.</p>
      {attachment?.refusal && <p role="alert">{String(attachment.refusal)}</p>}
      {(project.notes ?? []).map((n: string) => <p key={n} role="note">{n}</p>)}
      {attachment?.projectId && !attachment?.refusal && kept && !packageBlocked && project.reading === "records store" && <p>
        <button onClick={() => act("records_store_export")}>Export project records</button>{" "}
        <small>Creates a verified package in a folder you choose.</small>
      </p>}
      {packageImportable && <p>
        <button onClick={() => act("records_store_import_package", { action: "import" })}>Import verified package</button>{" "}
        <small>Choose a package for the identity already named by this folder’s project file. Exact bytes and the original identity are retained; conflicting files are refused. Unsigned package content stays quoted evidence.</small>
      </p>}
      {packageImportable && <p>
        <button onClick={() => act("records_store_import_package", { action: "restore" })}>Restore project from package</button>{" "}
        <small>Recover the package’s original project identity. The App checks whether this folder has no identity or only an unused identity created at startup. It refuses to replace an identity with records, a legal hold, closure or disposal, and retains existing bytes.</small>
      </p>}
      {packageImport?.state === "incomplete" && <p role="alert">
        Package import is interrupted. Project records remain unavailable until it is finished.{" "}
        <button onClick={() => act("records_store_import_package", { action: "resume" })}>Finish package import</button>
      </p>}
      {packageImport?.state === "unavailable" && <p role="alert">Package import status is unavailable. Project records remain unavailable.</p>}
      {packageRepairable && <p>
        <button onClick={() => act("records_store_import_package", { action: "repair" })}>Repair package controls</button>{" "}
        <small>Uses the original native intent and retained evidence. Differing control bytes or a missing original act keep recovery held. Package claims stay quoted evidence and grant no authority to replay acts.</small>
      </p>}
      {packageImport?.reason && <p role="note">Package recovery: {String(packageImport.reason)}</p>}
      {packageImport?.repairReason && packageImport.repairReason !== packageImport.reason && packageImport.repairReason !== packageImport.limit && <p role="note">Package repair: {String(packageImport.repairReason)}</p>}
      {typeof packageImport?.needsPackage === "boolean" && <p role="note">Original package needed for repair: {packageImport.needsPackage ? "yes; the native selector will ask you to choose it again" : "no"}.</p>}
      {packageImport?.limit && packageImport.limit !== packageImport.reason && <p role="note">Package import: {String(packageImport.limit)}</p>}
      {(packageImport?.importId || packageImport?.packageIdentity) && <p>Package import: {String(packageImport.state)}. {packageImport.importId && <>Import reference: {String(packageImport.importId)}. </>}{packageImport.packageIdentity && <>Package identity: {String(packageImport.packageIdentity)}.</>}</p>}
      {retention && <p role="note">{retention.disposition === "unavailable"
        ? "Retention state unavailable. Project closure and legal hold are unknown."
        : <>{retention.closed ? "Project closed to recording." : "Project open."} Legal hold: {retention.legalHold ? "set" : "not set"}. Records: {String(retention.disposition)}.</>}{" "}{retention.limit && String(retention.limit)}</p>}
      {attachment?.projectId && !attachment?.refusal && holdable && !packageBlocked && <p>
        {kept && <><button onClick={()=>act("records_store_retention",{action:retention.closed ? "reopen" : "close"})}>{retention.closed ? "Reopen project" : "Close project"}</button>{" "}</>}
        <button onClick={()=>act("records_store_retention",{action:retention.legalHold ? "release-hold" : "set-hold"})}>{retention.legalHold ? "Release legal hold" : "Set legal hold"}</button>{" "}
        {kept && retention.closed && !retention.legalHold && <button onClick={()=>act("records_store_retention",{action:"dispose"})}>Dispose of records after verified export</button>}
      </p>}
      {(retention?.disposition === "disposal incomplete" || retention?.disposition === "completion durability uncertain") && <p role="alert">Disposal or completion publication is unconfirmed and recording is blocked. {retention.legalHold ? <small>Legal hold blocks further disposal.</small> : !packageBlocked && <button onClick={()=>act("records_store_retention",{action:"resume-disposal"})}>Finish disposal</button>}</p>}
      {project.notImported > 0 && kept && !retention.closed && !packageBlocked && <p>
        <button onClick={() => act("records_store_import")}>Import {String(project.notImported)} record file(s){project.notImportedKinds ? ` (${String(project.notImportedKinds)})` : ""}</button>{" "}
        <small>{String(project.importStanding ?? "")}</small>
      </p>}
      {(attachment?.refusal || (attachment?.limits ?? []).length > 0) && identityRepair && <p>
        <button onClick={() => act("records_store_identity", { action: "adopt" })}>This folder is that project</button>{" "}
        <button onClick={() => act("records_store_identity", { action: "new-identity" })}>Give this folder a new identity</button>{" "}
        <button onClick={() => act("records_store_identity", { action: "restore-link" })}>Restore the project file</button>
      </p>}
    </>}
    <p><button onClick={() => act("records_store_verify_export")}>Verify an exported package</button></p>
  </section>;
}

export function WorkflowRootPanel({ data, host, act, observeView, openFileAct, fileActBusy = false }:{ data: Json; host: Json; act: (command:string,args:Record<string,unknown>)=>Promise<Json>; observeView?: ()=>Promise<unknown>; openFileAct?: OpenArrivalFileAct; fileActBusy?: boolean }) {
  const [name,setName]=useState("coordinated-knowledge-work");
  const [revision,setRevision]=useState("");
  const [thread,setThread]=useState("");
  // A source switch clears the local chat control; repeated bare thread IDs do not transfer it.
  useEffect(()=>setThread(""),[data?.context?.sourceRef,JSON.stringify(host?.generation)]);
  const context=workflowContext(data,host,thread);
  const selected=thread ? chatWorkflow(data,data?.context?.sourceRef,thread) : data?.inspection;
  const chatAvailable=!!context&&!!thread;
  const [text,setText]=useState("");
  const [busy,setBusy]=useState(false);
  const [outcome,setOutcome]=useState<{relation:{command:string;source:Json;request:Record<string,unknown>};message:string;limits:string[]}>();
  // Native results and later observation limits belong to the original press.
  // Children receive the unchanged native value, including pre-fill results.
  const action=async(command:string,args:Record<string,unknown>):Promise<Json>=>{
    setBusy(true);
    let request:Record<string,unknown>;
    try{request=workflowArguments(command,args,data,host,thread);}
    catch(error){setOutcome({relation:{command,source:structuredClone(data?.context??null),request:structuredClone(args)},message:String(error),limits:[]});setBusy(false);return undefined;}
    const relation={command,source:structuredClone(data?.context??null),request:structuredClone(request)};
    setOutcome({relation,message:"",limits:[]});
    const limit=(message:string)=>setOutcome(old=>old?.relation===relation?{...old,limits:[...old.limits,message]}:old);
    const observe=async(after:string)=>{if(observeView)try{await observeView();}catch(error){limit(`View refresh after ${after} failed: ${String(error)}. The original command response is retained as reported.`);}};
    // Capture this metadata request before awaiting the command or a new view.
    let draftRequest:Record<string,unknown>|undefined,draftRequestError:unknown;
    if(command==="workflow_create_draft"||command==="workflow_refine_registered"){
      try{draftRequest=command==="workflow_create_draft"?{context:structuredClone(request.context)}:workflowArguments("workflow_observe_drafts",{},data,host,thread);}
      catch(error){draftRequestError=error;}
    }
    try{
      const result=await act(command,request);
      setOutcome(old=>old?.relation===relation?{...old,message:workflowActionMessage(command,result)}:old);
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
    }catch(error){setOutcome(old=>old?.relation===relation?{...old,message:String(error)}:old);return undefined;}
    finally{setBusy(false);}
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
  return <section><h2>Workflow selection and native registration</h2><a href="#file-acts">Review a workspace draft file for a separate standing act</a>
    <label>Workflow chat <select value={thread} onChange={e=>setThread(e.target.value)} disabled={busy}><option value="">No chat — inspect library content</option>{(host?.threads??[]).filter((entry:Json)=>JSON.stringify(entry.generation)===JSON.stringify(host?.generation)).map((entry:Json)=><option key={entry.threadId} value={entry.threadId}>{entry.threadId} · {entry.modelProvider}/{entry.model}</option>)}</select></label>
    <p>{thread ? "This chat keeps its own pending workflow selection. Started runs keep their own revision." : "Library browsing is shared. Inspection here selects no workflow for a new chat."}</p>
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
    <SelectedWorkflow selection={selected} inspection={!thread}/>
    {thread&&<NewerRevisionNotice selection={selected} busy={busy||!context} act={action}/>}
    <details><summary>Selection and libraries as the host reports them (paths shown as text; identities keep their exact bytes; a path that is not valid UTF-8 is marked)</summary>
    <pre style={{whiteSpace:"pre-wrap"}}>{JSON.stringify(readablePaths({selection:selected,inspection:data?.inspection,chatContext:context,libraries:data?.libraries,activeLibrary:data?.activeLibrary}),null,2)}</pre></details>
    <WorkflowDraftsView data={data?.drafts} workspace={data?.projectLibraryAvailable===true} pointerLimits={data?.trialPointerLimits} conversations={conversations}
      runs={[...(data?.runs??[]),...(data?.reopened?.runs??[])]} pending={data?.pendingTrials} busy={busy} act={action}/>
    <label>New draft name, or in-place library entry name <input {...EXACT_TEXT} value={name} onChange={e=>setName(e.target.value)} disabled={busy}/></label>
    <button disabled={busy||!context||!selected||!data?.activeLibrary} onClick={()=>action("workflow_create_draft",{name})}>{thread?"Create draft from this chat’s selected content":"Create draft from inspected content"}</button>
    {(data?.libraries??[]).filter((l:Json)=>l.reference===data?.activeLibrary&&Array.isArray(l.registered)).map((l:Json)=><RegisteredRevisions key={l.reference} library={l.reference} rows={l.registered} busy={busy} chatAvailable={chatAvailable} act={action}/>)}
    {(data?.libraries??[]).filter((l:Json)=>l.reference===data?.activeLibrary).map((l:Json)=><LibraryEntries key={`${l.reference}:${l.entryListing?.reference??"unobserved"}`} library={l} busy={busy} available={!!context} act={action}/>)}
    {(data?.libraries??[]).filter((l:Json)=>l.reference===data?.activeLibrary).map((l:Json)=><RegistrationEvidence key={l.reference} evidence={l.registrationEvidence}/>)}
    <label>Registered revision (content identity) <input {...EXACT_TEXT} value={revision} onChange={e=>setRevision(e.target.value)} disabled={busy}/></label>
    <button disabled={busy||!data?.activeLibrary||!name||!revision} onClick={()=>action("workflow_refine_registered",{name,revision})}>Refine registered revision from the revision store (no selection)</button>
    <button disabled={busy||!data?.activeLibrary||!name} onClick={()=>action("workflow_review",{names:[name],inPlace:true})}>Review this unregistered in-place library entry</button>
    <small> Drafts are reviewed from the draft list above.</small>
    {orderedReviews.map(review=><article key={review.reference}>
      <h3>{review.reference===data?.activeReview?"Current review":"Retained review"} · {review.reference}</h3>
      {digests[review.reference]&&<p>{digestComparison(digests[review.reference])}{review.status?.presentation?<> Read the complete review below before choosing {review.status.presentation.entries?.[0]?.disposition==="re-confirmation"?"Re-confirm":"Register"}: the native confirmation shows the act statement and this digest, not the review itself.</>:" (as last shown with the review; while the native confirmation is open, the review it names is shown under \"Content named by an open native confirmation\")"}</p>}
      {review.status?.presentation?.entries?.[0]?.disposition==="re-confirmation"&&<p role="note">{review.status.presentation.entries[0].message}. {review.status.presentation.entries[0].reconfirmation?.statement}</p>}
      {review.status?.presentation&&<p><button disabled={busy||review.reference!==data?.activeReview} onClick={()=>action("workflow_register_native",{reviewRef:review.reference})}>{review.status?.presentation?.entries?.[0]?.disposition==="re-confirmation"?"Re-confirm this revision for use in this App session through native A15 confirmation…":"Register this review through native A15 confirmation…"}</button></p>}
      {review.status?.presentation ? <>
        {typeof review.status.state === "string" && <p>Review state: {review.status.state}</p>}
        <WorkflowRegistrationReview presentation={review.status.presentation} />
        <details><summary>Complete reported review status (diagnostic JSON)</summary><pre style={{whiteSpace:"pre-wrap"}}>{JSON.stringify(readablePaths(review.status),null,2)}</pre></details>
      </> : <pre style={{whiteSpace:"pre-wrap"}}>{JSON.stringify(readablePaths(review.status??review),null,2)}</pre>}
      <LastCleanTrialLine line={review.lastCleanTrial} busy={busy} act={action}/>
      <button disabled={busy} onClick={()=>action("workflow_continue_registration",{reviewRef:review.reference})}>Continue original captured registration</button>
      <ReviewSelectButtons review={review} libraries={data?.libraries??[]} busy={busy} chatAvailable={chatAvailable} act={action}/>
    </article>)}
    <h3>Send selected workflow text</h3>
    <label>Person text <textarea value={text} onChange={e=>setText(e.target.value)} disabled={busy} rows={3}/></label>
    {selected&&selected.runnable!==true&&<p role="note">Not runnable: {selected.runLimit}</p>}
    <button disabled={busy||!context||host?.state!=="ready"||!thread||selected?.runnable!==true} onClick={()=>action("workflow_prepare_run",{generation:host.generation,threadId:thread,personText:text})}>Prepare exact selected workflow text</button>
    <button disabled={busy} onClick={()=>action("workflow_read_records",{})}>Read recorded workflow supply (durable, read-only)</button>
    <button disabled={busy} onClick={()=>action("workflow_reopen",{})}>Reopen recorded workflow runs (read-only)</button>
    {data?.reopened&&<article><h3>Recorded runs (reopened from project records)</h3><p>{data.reopened.standing}</p>
      <ul>{(data.reopened.runs??[]).map((r:Json)=><li key={r.run}>{r.run} · conversation {r.conversation??"unknown"} · {r.state}{r.detail?` (${typeof r.detail==="string"?r.detail:JSON.stringify(r.detail)})`:""}{r.follows?` · follows ${r.follows}`:""}{(r.restartInterruptions??[]).length?` · App restart interruptions: ${r.restartInterruptions.length}`:""}
        {r.workflow&&<p>Recorded workflow {r.workflow.origin}:{r.workflow.name}, revision {String(r.workflow.revision??"").slice(0,12)}.</p>}
        {!(data?.runs??[]).some((h:Json)=>h.reference===r.run)&&<RunBringBack run={r} conversations={conversations} defaultThread={runBringBackDefault(data,r.run)} busy={busy} act={action}/>}
        {r.state?.startsWith("open")&&!(data?.runs??[]).some((h:Json)=>h.reference===r.run)&&<button disabled={busy} onClick={()=>action("workflow_end_recorded",{runId:r.run,threadId:r.conversation??null})}>End this interrupted run</button>}</li>)}</ul>
      {(data.reopened.limits??[]).length>0&&<p>Record limits: {JSON.stringify(data.reopened.limits)}</p>}
      {data.reopened.restartLimits&&<p>App-restart interruption limits (written by the host at startup): {(data.reopened.restartLimits.outcomes??[]).map((o:Json)=>`${o.threadId}: ${o.outcome}${o.run?` on ${o.run}`:""}${typeof o.detail==="string"?` (${o.detail})`:""}`).join("; ")||data.reopened.restartLimits.reason||"no restart facts"}</p>}</article>}
    {data?.afterRunEnd&&<article><h3>After-run-end observations</h3><p>{data.afterRunEnd.standing}</p>
      {(data.afterRunEnd.limits??[]).length>0&&<p role="alert">Observation/recording limits: {JSON.stringify(data.afterRunEnd.limits)}</p>}
      {(data.afterRunEnd.held??[]).map((r:Json)=><p key={r.recordId} role="status">Not yet recorded: {r.recordId} for ended run {r.run}, first observed {r.observedAt}. {r.limit}</p>)}
      <details><summary>Recorded post-end source history (JSON)</summary><pre style={{whiteSpace:"pre-wrap"}}>{JSON.stringify(data.afterRunEnd.runs??[],null,2)}</pre></details>
      {(data.afterRunEnd.runs??[]).filter((r:Json)=>!(data?.runs??[]).some((h:Json)=>h.reference===r.run)).map((r:Json)=><div key={r.run}><p>Ended run {r.run}. Source project {r.source?.projectId}.</p><ul>{(r.records??[]).filter((e:Json)=>e.kind==="checkpoint_arrival").map((e:Json)=><ArrivalRecord key={e.recordId} arrival={e} all={r.records??[]}/>)}</ul></div>)}
    </article>}
    {(data?.endedAfterRelaunch??[]).map((end:Json)=><article key={end.run}><h3>{end.run} (ended after the relaunch)</h3>
      <p>End notice: {end.endNotice?.state??"none"}. {end.limit}</p>
      <HistoryReferenceNotice pointers={end.learningPointers}/>
      {(end.endNotice?.state?.startsWith("pending")||hasUnsavedHistoryReference(end))&&<p role="status">{end.endNotice?.state?.startsWith("pending")&&<>The next message in conversation {end.conversation} carries this end notice first, once. </>}
        <button disabled={busy} onClick={()=>action("workflow_reopened_notice",{runId:end.run,action:"retry"})}>{end.endNotice?.state?.startsWith("pending")?"Retry the end-notice record":"Retry saving records (never sends)"}</button>
        {end.endNotice?.state?.startsWith("pending")&&end.noticeRecordFailure&&<button disabled={busy} onClick={()=>action("workflow_reopened_notice",{runId:end.run,action:"skip"})}>Send without the end notice (recorded as not supplied)</button>}</p>}
    </article>)}
    {(data?.runs??[]).map((run:Json)=>{const next=chatWorkflow(data,data?.context?.sourceRef,run.conversation);return <article key={run.reference}><h3>{run.reference}</h3>
      <p>Run: {run.lifecycle?.state}{run.lifecycle?.follows?` · follows ${run.lifecycle.follows}`:""}{run.lifecycle?.end?` · ${run.lifecycle.end.cause}`:""}. Records: {run.publication?.state}. Send: {run.status?.state}{run.status?.limit?` (${run.status.limit})`:""}. Supplied: {suppliedSummary(run)}. Adoption: unknown.</p>
      {run.endNotice&&<p>End notice: {run.endNotice.state}</p>}
      {!isRecordedRun(run)&&run.endNotice?.state?.startsWith("pending")&&<p role="status">The next message in this conversation, with or without attachments or a mode, carries this end notice first, once.{run.status?.limit?` Last attempt: ${run.status.limit}`:""}
        <button disabled={busy} onClick={()=>action("workflow_retry_records",{runRef:run.reference})}>Retry the end-notice record</button>
        {run.noticeRecordFailure&&<button disabled={busy} onClick={()=>action("workflow_skip_notice",{runRef:run.reference})}>Send without the end notice (recorded as not supplied)</button>}</p>}
      <ul>{[...(run.checks??[]),...(run.noticeChecks??[])].map((check:Json)=><li key={check.reference}>{check.readAt}: {check.state} ({check.supplyReading}); check record {check.published?"recorded":`pending${check.publicationLimit?` — ${check.publicationLimit}`:""}`}; R3 {check.r3?.state}{check.r3?.limit?` — ${check.r3.limit}`:""}</li>)}</ul>
      <RunPanel run={run} conversations={conversations} bringBackDefault={runBringBackDefault(data,run.reference)} busy={busy || fileActBusy} act={action} openFileAct={openFileAct}/>
      <details><summary>Complete run evidence (paths shown as text)</summary><pre style={{whiteSpace:"pre-wrap"}}>{JSON.stringify(readablePaths(run),null,2)}</pre></details>
      {!isRecordedRun(run)&&<>
      <button disabled={busy||!!run.source||host?.state!=="ready"} onClick={()=>action("workflow_send_run",{runRef:run.reference})}>Record, then send original prepared text once</button>
      <button disabled={busy||!run.turn||host?.state!=="ready"} onClick={()=>action("workflow_check_supply",{runRef:run.reference})}>Check original native supplied text pages (new check)</button>
      <button disabled={busy||(!run.pendingRecords&&!hasUnsavedHistoryReference(run))} onClick={()=>action("workflow_retry_records",{runRef:run.reference})}>Retry pending records (never sends)</button>
      {run.lifecycle?.state?.startsWith("open")&&<>
        <button disabled={busy} onClick={()=>action("workflow_end_run",{runRef:run.reference,finishedReport:null})}>End run</button>
        <button disabled={busy||host?.state!=="ready"||run.home!==host?.generation?.home||next?.runnable!==true} onClick={()=>action("workflow_end_and_start",{runRef:run.reference,generation:host.generation,threadId:run.conversation,personText:text})}>End this run and start {next?.identity?.name??"this chat’s selected workflow"}</button>
      </>}
      {run.endNotice?.state?.startsWith("sent")&&<button disabled={busy||host?.state!=="ready"} onClick={()=>action("workflow_check_notice",{runRef:run.reference})}>Check the end notice in native history (new check)</button>}
      <p>Selection and run text are recorded before sending; if recording fails nothing is sent. A run opens when its start turn is observed and ends only when the person ends it: an interrupt, stop, quit, failed or completed turn, or an agent's "Workflow finished" line does not end it. Ending here records "ended by the person"; when the agent writes its "Workflow finished" line, the conversation offers End run beneath that message, which records cause "completed". After an end, the next message in this conversation (text, a plan or default mode turn, an attachment-bearing turn or a Continue-as request) carries the end notice first, once. Load/select this conversation and its received turn in native History before checking.</p>
      </>}
    </article>;})}
    {outcome&&<div aria-label="Workflow action response">
      <p>Original workflow action: <code>{outcome.relation.command}</code> · source <code>{outcome.relation.source?.sourceRef??"not supplied"}</code>. Response and observation limits belong to this request.</p>
      {outcome.message&&<p role="status" aria-label="Workflow command result" style={{whiteSpace:"pre-wrap"}}>{outcome.message}</p>}
      {outcome.limits.map((message,index)=><p role="status" aria-label="Workflow observation limit" key={index} style={{whiteSpace:"pre-wrap"}}>{message}</p>)}
      <details><summary>Original workflow request</summary><pre style={{whiteSpace:"pre-wrap"}}>{JSON.stringify(outcome.relation,null,2)}</pre></details>
    </div>}
  </section>;
}

export function HomeAccessPanel({ routing, access, resources, oauth, generation, navigating = false, act }: { routing: Json; access: Json; resources: Json; oauth?: Json; generation: Json; navigating?: boolean; act: (command: string, args: Record<string, unknown>) => Promise<void> }) {
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const action = async (command: string, args: Record<string, unknown>) => {
    if (command === "select_home" && navigating) return;
    setBusy(true); setError("");
    try { await act(command, args); } catch (e) { setError(String(e)); } finally { setBusy(false); }
  };
  const entries: Json[] = routing?.entries ?? [];
  return <section><h2>Separate Codex homes and access</h2>
    <p>Active home class: {routing?.activeModeHomeClass ?? "unavailable"}. The full native generation identifies its owning source; switching homes does not transfer a conversation.</p>
    {entries.map(entry => <article key={entry.modeHomeClass}><p>{entry.modeHomeClass} · {entry.state} · {JSON.stringify(entry.generation)} · {entry.configurationLimit}</p><button disabled={busy || navigating || routing?.activeModeHomeClass === entry.modeHomeClass} onClick={() => action("select_home", {modeHomeClass: entry.modeHomeClass})}>Use {entry.modeHomeClass} home</button></article>)}
    <button disabled={busy || !generation || !routing?.activeModeHomeClass} onClick={() => action("read_home_access", {generation, modeHomeClass:routing.activeModeHomeClass})}>Read native login policy and account</button>
    <button disabled={busy || routing?.activeModeHomeClass !== "account" || !generation} onClick={() => action("oauth_start", {generation,mode:"browser"})}>Sign in with your ChatGPT account (through Codex)…</button>
    <button disabled={busy || routing?.activeModeHomeClass !== "account" || !generation} onClick={() => action("oauth_start", {generation,mode:"device-code"})}>Sign in through native device code…</button>
    <button disabled={busy || routing?.activeModeHomeClass !== "account" || !generation || !oauth?.source?.presentationAvailable} onClick={() => action("oauth_present", {generation})}>Show pending native sign-in…</button>
    <button disabled={busy || routing?.activeModeHomeClass !== "account" || !generation || !oauth?.source?.cancelAvailable} onClick={() => action("oauth_cancel", {generation})}>Cancel original pending sign-in with native confirmation…</button>
    <p>{oauth?.source?.cancelStatus === "notFound" ? "Signed out: Codex had no pending sign-in." : oauth?.source?.cancelStatus === "canceled" ? "Signed out: original sign-in canceled." : oauth?.source?.phase === "CompletedSuccess" ? "Matching sign-in completed; read native account to confirm." : oauth?.source?.phase === "CompletedFailure" || oauth?.source?.phase === "StartRejected" ? "Native sign-in failed; sensitive diagnostic withheld." : oauth?.source?.phase === "Pending" ? "Waiting for sign-in; silence does not complete it." : oauth?.state ?? "Native sign-in observation unavailable."}</p>
    <details><summary>Safe original sign-in observation</summary><pre style={{whiteSpace:"pre-wrap"}}>{JSON.stringify(oauth ?? {state:"unavailable"},null,2)}</pre></details>
    <button disabled={busy || !generation || !routing?.activeModeHomeClass} onClick={() => action("logout_home", {generation,modeHomeClass:routing.activeModeHomeClass})}>Log out / remove key with native live-work warning…</button>
    <button disabled={busy || !resources?.keyConfigured || !!resources?.wholeSetLimit} onClick={() => action("add_api_key", {})}>Add or replace key in native secure field…</button>
    {error && <p role="alert">{error}</p>}
    <details open><summary>Source-owned account observations and limits</summary><pre style={{whiteSpace:"pre-wrap"}}>{JSON.stringify(access, null, 2)}</pre></details>
    <details><summary>Explicit receiving homes and shared-resource observations</summary><pre style={{whiteSpace:"pre-wrap"}}>{JSON.stringify(resources ?? {state:"explicit shared-resource descriptors not configured; existing account path remains available"}, null, 2)}</pre></details>
    <p>Native login acknowledgment reports presence with validity unknown until actual use. Credential fields, browser URLs and device codes are never accepted through this webview. Resource links do not establish native discovery or authorize a future configuration write.</p>
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
    {(view?.limits ?? []).length > 0 && <p>View limits: {view.limits.join(" | ")}</p>}
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
  const [host, setHost] = useState<Json>(null);
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
    document.getElementById("file-acts")?.scrollIntoView?.({ block: "start" });
  };
  const [view, setView] = useState<Json>(null);
  const [offer, setOffer] = useState<Json>(null);
  const [choice, setChoice] = useState<string>("");
  const [name, setName] = useState<string>("");
  const [message, setMessage] = useState<string>("");
  const homeClass = host?.homeRouting?.activeModeHomeClass ?? null;
  const chooserHome = useRef({ mode: homeClass, epoch: 0 });
  if (chooserHome.current.mode !== homeClass) {
    // A different active home invalidates its previous chooser even if the
    // person returns before an earlier request finishes. A spawn update alone
    // is not a new choice: the command reports the actual admitted generation.
    chooserHome.current = { mode: homeClass, epoch: chooserHome.current.epoch + 1 };
  }
  const editRevision = useRef(0);
  const [conversationChoice, setConversationChoice] = useState({ ...emptyConversationChoice, homeEpoch: 0 });
  const choiceRef = useRef(conversationChoice);
  const reviseChoice = (patch: Partial<typeof emptyConversationChoice>) => {
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
  const entryCompatible = (homeClass === "account" || homeClass === "api-key") && startEntries(host).some(entry => entry.value === entryId);
  const [role, setRole] = useState<string>("");
  const [roleTouched, setRoleTouched] = useState(false);
  const [threadKey, updateThreadKey] = useState<string>("");
  const threadChoiceRevision = useRef(0);
  const setThreadKey = (key: string) => { threadChoiceRevision.current++; updateThreadKey(key); };
  const forkSequence = useRef(0);
  const forkInFlight = useRef(false);
  const [pendingFork, setPendingFork] = useState<ForkNavigation | null>(null);
  const roleInitialized = useRef(false);
  useEffect(() => {
    if (!roleInitialized.current && host?.roleSet?.available) {
      roleInitialized.current = true;
      setRole(host.roleSet.defaultRole ?? "");
    }
  }, [host?.roleSet]);


  const refresh = useCallback(async () => {
    const snapshot: Json = await invoke("host_status");
    setHost(snapshot);
    try {
      setView(await invoke("decision_view"));
    } catch (e) {
      setView({ error: String(e) });
    }
    return snapshot;
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
      const snapshot: Json = await invoke("host_status");
      if (isCurrent()) setHost(snapshot);
      try {
        const decision: Json = await invoke("decision_view");
        if (isCurrent()) setView(decision);
      } catch (e) { if (isCurrent()) setView({ error: String(e) }); }
      return snapshot;
    } };
  };

  useEffect(() => {
    refresh();
    const t = setInterval(() => invoke("host_status").then(setHost).catch(e => setMessage(String(e))), 1000);
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
      setMessage(`${cmd}: ${JSON.stringify(r).slice(0, 300)}`);
    } catch (e) {
      setMessage(`${cmd}: ${String(e)}`);
    }
    await refresh();
  };
  const startConversation = async () => {
    const source = currentHost.current;
    const mode = source?.homeRouting?.activeModeHomeClass;
    const submitted = choiceRef.current;
    const epoch = chooserHome.current.epoch;
    if (startPendingRef.current || homePendingRef.current || source?.state !== "ready" || submitted.homeEpoch !== epoch ||
        !submitted.model.trim() || !submitted.modelProvider.trim() || !(mode === "account" || mode === "api-key") ||
        !startEntries(source).some(entry => entry.value === submitted.entryId)) return;
    const revision = editRevision.current;
    forkStartRevision.current++;
    continueStartRevision.current++;
    startPendingRef.current = true;
    setStartPending(true);
    try {
      const response: Json = await invoke("thread_start", { model: submitted.model, modelProvider: submitted.modelProvider, entryId: submitted.entryId,
        modeHomeClass: mode, role: role || null, preselected: !roleTouched && !!role && role === source?.roleSet?.defaultRole });
      const opened = startedConversationKey(response);
      if (opened) {
        setThreadKey(opened);
        // Consume only the submitted edit, before the independent refresh.
        // Even an edit away and back is a newer choice and must survive.
        if (editRevision.current === revision && chooserHome.current.epoch === epoch) reviseChoice(emptyConversationChoice);
      }
      setMessage(`thread_start: ${JSON.stringify(response).slice(0, 300)}`);
    } catch (error) {
      setMessage(`thread_start: ${String(error)}`);
    } finally {
      startPendingRef.current = false;
      setStartPending(false);
      try { await refresh(); }
      catch (error) { setMessage(previous => `${previous}; current host view unavailable: ${String(error)}`); }
    }
  };
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
    try { const result: Json = await invoke(command, args); const snapshot = await refresh(); return { result, snapshot }; }
    finally { if (navigating) { homePendingRef.current = false; setHomePending(false); } }
  };
  // Start / Stop / Restart Codex: one at a time; the host asks first for Stop and Restart.
  const [processBusy, setProcessBusy] = useState(false);
  const processAct = async (cmd: string, args: Record<string, unknown>) => {
    setProcessBusy(true);
    try {
      const r: Json = await invoke(cmd, args);
      setMessage(r?.state === "cancelled" ? `${r.action}: ${r.reading}` : cmd === "codex_stop" ? `${r?.action}: see the outcome under Codex host.` : `${cmd}: ${JSON.stringify(r).slice(0, 300)}`);
    } catch (e) {
      setMessage(`${cmd}: ${String(e)}`);
    } finally {
      setProcessBusy(false);
      await refresh();
    }
  };

  const conversationAction = async (command: "conversation_send_text" | "conversation_steer_text" | "conversation_interrupt", args: Record<string, unknown>) => {
    let failed = false;
    let failure: unknown;
    try {
      await invoke(command, args);
      setMessage(command === "conversation_send_text" ? "Native turn/start response received; outcomes remain as observed below." : command === "conversation_steer_text" ? "Native steering acknowledgment received; turn replacement and completion remain determined by native events." : "Native interrupt acknowledgment received; turn end and rollback are not established by this acknowledgment.");
    } catch (e) { failed = true; failure = e; setMessage(`${command}: ${String(e)}`); }
    try { setHost(await invoke("host_status")); }
    catch (e) { setMessage(`${command}: ${failed ? "request failed" : "native response received"}; view refresh failed: ${String(e)}`); }
    if (failed) throw failure;
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
      document.getElementById(current ? "conversation" : "other-requests")?.scrollIntoView?.();
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
        !["account", "api-key"].includes(scope.modeHomeClass)) return;
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
    } catch (error) { if (forkContextCurrent(scope, currentHost.current)) setMessage(`Fork outcome is not confirmed: ${String(error)}`); }
    finally {
      try {
        const snapshot = await invoke("host_status");
        // Ignore a response to an older intent/source; it cannot restore that
        // home over a newer choice or make a stale fork current.
        if (forkContextCurrent(scope, currentHost.current)) setHost(snapshot);
      } catch (error) { if (forkContextCurrent(scope, currentHost.current)) setMessage(previous => `${previous}; original source view refresh unavailable: ${String(error)}`); }
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
    try { await refresh(); }
    catch (error) {
      outcome = { ...outcome, observationFailure: String(error) };
      setMessage(`Continue-as: ${outcome.state}; view refresh failed: ${String(error)}`);
    }
    return outcome;
  };
  const runAct: RunAct = async (command, args) => {
    try {
      const result = await invoke(command, args);
      setMessage(`${command}: ${JSON.stringify(result).slice(0, 600)}`);
      return result;
    } catch (e) { setMessage(`${command}: ${String(e)}`); }
    finally { await refresh(); }
  };
  // As runAct, but a host error rejects with the host's message (trial sends show it as given).
  const trialRunAct: RunAct = async (command, args) => {
    try {
      const result = await invoke(command, args);
      setMessage(`${command}: ${JSON.stringify(result).slice(0, 600)}`);
      return result;
    } catch (e) { setMessage(`${command}: ${String(e)}`); throw e; }
    finally { await refresh(); }
  };
  // The conversation the panel actually shows (current generation only), so no request is hidden.
  const selectedThread: string | null = (host?.threads ?? []).find((t: Json) => JSON.stringify([t.generation, t.threadId]) === threadKey && JSON.stringify(t.generation) === JSON.stringify(host?.generation))?.threadId ?? null;

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

  return (
    <main style={{ fontFamily: "system-ui, sans-serif", padding: 16 }}>
      <h1>Chirality App v4 — walking skeleton</h1>
      <NativeWaitingBridge ready={!!host} report={setMessage}
        checkpoint={() => ({ signature: JSON.stringify([threadChoiceRevision.current, chooserHome.current.epoch, editRevision.current]),
          pristine: threadChoiceRevision.current === 0 && editRevision.current === 0 })} capture={() => {
        const revision = threadChoiceRevision.current;
        const homeEpoch = chooserHome.current.epoch;
        const chooserRevision = editRevision.current;
        const wasBusy = homePendingRef.current || startPendingRef.current;
        return async group => {
          if (wasBusy || homePendingRef.current || startPendingRef.current) {
            setMessage("Waiting-request navigation refused while another home or conversation operation is pending; choose again from the current menu."); return;
          }
          if (revision !== threadChoiceRevision.current || homeEpoch !== chooserHome.current.epoch || chooserRevision !== editRevision.current) {
            setMessage("Waiting-request navigation superseded by a newer home or conversation choice; choose again from the current menu."); return;
          }
          await openRequests(group);
        };
      }} />
      <WaitingRequestsIndicator overview={host?.waitingRequests} busy={homePending} open={group => { void openRequests(group); }} />
      <NativeConfirmationContent />
      <ConnectorSourcePanel availability={host?.connectorRouteAvailability} command={(name,args)=>invoke(name,args)} />
      <ConnectorRoutePanel availability={host?.connectorRouteAvailability} state={routeRead} onRead={readRoutes} />
      <FileActPanel command={(name,args)=>invoke(name,args)} controlRef={fileActPanel} onBusyChange={setFileActBusy} />

      <WorkflowRootPanel data={host?.workflowRoot} host={host} openFileAct={openArrivalFileAct} fileActBusy={fileActBusy} act={(command,args)=>invoke<Json>(command,args)} observeView={refresh} />
      <HomeAccessPanel routing={host?.homeRouting} access={host?.homeAccess} oauth={host?.homeOAuth} resources={{...host?.homeResources,namespaceProtection:host?.nativeNamespaces,keyAdmission:host?.keyNamespaceAdmission}} generation={host?.generation} navigating={homePending} act={async (command, args) => { await homeAction(command, args); }} />

      <section>
        <h2>Codex host</h2>
        {host?.configurationProblem && <p>Configuration: {host.configurationProblem}</p>}
        <p>
          State: <b>{host?.state}</b> · generation {host?.generation ? JSON.stringify(host.generation) : "—"} · version{" "}
          {host?.versionIdentity?.observedVersionLabel ?? "—"} · verification{" "}
          {host?.verification ? JSON.stringify(host.verification) : "—"}
        </p>
        <p>Supplier standing: {host?.supplierStanding ?? "not started"}</p>
        <p>
          <ModelProviderFields model={model} modelProvider={modelProvider} setModel={model => reviseChoice({model})} setModelProvider={modelProvider => reviseChoice({modelProvider})} />
        </p>
        <p><label>Access entry <select value={entryId} onChange={e => reviseChoice({entryId:e.target.value})}><option value="">No entry selected</option>{startEntries(host).map(entry => <option key={entry.value} value={entry.value}>{entry.label}</option>)}</select></label></p>
        <p>Choose a model, provider and entry for this new conversation in the selected home. Switching homes never transfers an existing conversation.</p>
        <RoleChoice group="start-thread-role" roleSet={host?.roleSet} limits={host?.roleLimits} role={role} preselected={!roleTouched && !!role && role === host?.roleSet?.defaultRole}
          setRole={next => { roleInitialized.current = true; setRoleTouched(true); setRole(next); }} />
        <p><small>Role set: {host?.roleSet?.standing ?? host?.roleSet?.reason ?? "unavailable"}.</small></p>
        <SupplyStatus supply={host?.roleSupply} />
        <RoleHistoryReader scope={JSON.stringify(host?.generation)} ready={host?.state === "ready"} read={() => invoke("role_supply_history", { generation: host?.generation, thread: null })} />
        {host?.instructionsProblem && <p role="alert">Role guidance store: {host.instructionsProblem}</p>}
        <RecordsStorePanel store={host?.recordsStore} act={act} />
        <FleetRecordsPanel packet={fleet} error={fleetError} busy={fleetBusy} refresh={() => { void refreshFleet(); }} />
        <p aria-label="New conversation choice">{!model.trim() || !modelProvider.trim() ? "not started — no model selected" : entryCompatible ? `New conversation choice: ${model} via ${modelProvider} (${entryId})` : "Choose an access entry for the current home."}</p>
        <details><summary>Last native start selection in this home</summary><pre>{JSON.stringify(host?.accessSelection ?? null, null, 2)}</pre></details>
        <p>Account (App-observed, identity not verified): {JSON.stringify(host?.accountObservation ?? { state: "unknown" })}</p>
        <p>
          <button onClick={startConversation} disabled={host?.state !== "ready" || !model.trim() || !modelProvider.trim() || !entryCompatible || startPending || homePending}>Start thread</button>
        </p>
        <CodexProcessControls host={host} busy={processBusy} act={(command, args) => { void processAct(command, args); }} />
        <p>Threads: {(host?.threads ?? []).map((t: Json) => `${t.threadId} (${t.status?.type ?? "?"}, gen ${JSON.stringify(t.generation)})`).join(", ") || "none"}</p>
        <RecordsCapabilityBindings host={host} />

        <h3>Expected network contacts</h3>
        <p>Codex can contact the selected model provider at thread start, before a model turn. This view describes supplier behavior; socket measurements remain separate evidence.</p>
        <ul>{(host?.networkDisclosure?.entries ?? []).map((entry: Json, index: number) => <li key={index}>{entry.purpose} · {entry.phase} · {entry.destination} · {entry.detail ?? entry.condition}</li>)}</ul>
        <details>
          <summary>Lifecycle events ({host?.lifecycle?.length ?? 0}) and frames ({host?.journal?.length ?? 0})</summary>
          <pre>{JSON.stringify({ lifecycle: host?.lifecycle, clientRequests: host?.clientRequests }, null, 2)}</pre>
        </details>
      </section>

      <AttachmentSelectionPanel data={host?.attachmentSelections} act={async (command, args) => {
        try { await invoke(command, args); } finally { setHost(await invoke("host_status")); }
      }} />

      <RecoveryCustodyPanel key={JSON.stringify([host?.homeRouting?.activeModeHomeClass, host?.generation])}
        modeHomeClass={host?.homeRouting?.activeModeHomeClass} generation={host?.generation ?? null}
        nativeHistoryGeneration={host?.nativeHistory?.generation ?? null}
        read={() => invoke("read_recovery_custody", { modeHomeClass: host?.homeRouting?.activeModeHomeClass, generation: host?.generation ?? null })}
        readRequests={(cursor: Json) => invoke("read_recovery_request_history", { modeHomeClass: host?.homeRouting?.activeModeHomeClass, generation: host?.generation ?? null, cursor: cursor ?? null })}
        retry={(threadId: string) => invoke("recovery_retry", { modeHomeClass: host?.homeRouting?.activeModeHomeClass, generation: host?.generation ?? null, threadId })} />
      <HistoryPanel host={host} refresh={refresh} threadKey={threadKey} setThreadKey={setThreadKey} captureContinueNavigation={captureContinueNavigation} />

      <ConversationPanel forkConversation={forkConversation} handoffSend={(id, text) => handoffAction("continue_as_send", { id, text })} handoffRead={id => handoffAction("continue_as_send_read", { id })} codexBusy={processBusy} host={host} threadKey={threadKey} setThreadKey={setThreadKey} answer={answerRequest} readRequest={readRequestCustody} replyObservations={replyObservations} runAct={runAct} trialRunAct={trialRunAct} send={async (generation, threadId, text, mode) => {
        await conversationAction("conversation_send_text", { generation, threadId, text, mode: mode ?? null });
      }} checkPlanMode={async generation => {
        try { await invoke("collaboration_modes_read", { generation }); } finally { setHost(await invoke("host_status")); }
      }} steer={async (generation, threadId, expectedTurnId, text) => {
        await conversationAction("conversation_steer_text", { generation, threadId, expectedTurnId, text });
      }} submitAttachments={async (generation, threadId, expectedTurnId, text, ownerRef, listRevision, selectionRefs) => {
        try {
          await invoke("submit_attachments", { generation, threadId, expectedTurnId, text, ownerRef, listRevision, selectionRefs });
          setMessage("Matching attachment native acknowledgment observed; provider uptake and completion remain unestablished.");
        } finally { setHost(await invoke("host_status")); }
      }} interrupt={async (generation, threadId, turnId) => {
        await conversationAction("conversation_interrupt", { generation, threadId, turnId });
      }} />

      <section>
        <h2>Native requests and execution</h2>
        <p>Recovery initialization: {host?.recoveryInitialization?.state ?? "not-initialized"} · host configured: {String(host?.recoveryInitialization?.hostConfigured ?? false)}</p>
        {(host?.recoveryInitialization?.historyLimits ?? []).map((limit: string) => <p role="alert" key={limit}>App history limit: {limit}</p>)}
        <p>SQLite recovery ledger: {host?.recoveryInitialization?.database ?? "location not established"} {host?.recoveryInitialization?.path?.pathDisplayLimit}</p>
        <p>Legacy JSON Lines import location: {host?.recoveryInitialization?.path?.displayPath ?? "location not established"} {host?.recoveryInitialization?.path?.pathDisplayLimit}</p>
        {host?.recoveryInitialization?.configurationError && <p role="alert">Ledger initialization failed: {host.recoveryInitialization.configurationError}. Native supplier processing is not blocked.</p>}
        <p>Directory publication: {host?.recoveryInitialization?.directoryPublication ?? "not established"} · later persistence failure: {host?.recoveryPersistenceError ?? "none reported"}</p>
        <details><summary>Recovery initialization and historical pointer state</summary><pre>{JSON.stringify({ initialization: host?.recoveryInitialization, recovery: host?.recovery }, null, 2)}</pre></details>
        <ObserverAttachment host={host} />
        {(host?.nativeViewLimits ?? []).map((limit: string, i: number) => <p key={i}>{limit}</p>)}
        <div id="other-requests">
          <h3>Requests outside the selected conversation</h3>
          <p>Requests of the selected conversation are shown beside it above. Select another conversation to answer its requests there.</p>
          {hostRequests(host).filter((request: Json) => requestThread(request) === null || requestThread(request) !== selectedThread).map((request: Json) => <NativeRequestCard key={JSON.stringify([request.generation, request.requestIdentity])} request={request} view={host?.nativeView} answer={answerRequest} readRequest={readRequestCustody} observation={replyObservations[requestScopeKey(request)]} />)}
        </div>
        <a href="#file-acts">Act on a saved App-side output file (select it explicitly)</a>
        <details><summary>Native plans, tools, goals, turns and descendants as received (JSON)</summary><pre>{JSON.stringify({ current: host?.nativeView, observationEnded: host?.nativeViewObservationEnded, priorObservations: host?.priorNativeViews, recovery: host?.observerRecovery }, null, 2)}</pre></details>
        <details><summary>Raw native envelopes (including unknown fields)</summary><pre>{JSON.stringify(host?.journal, null, 2)}</pre></details>
      </section>

      <ExternalObservationPanel data={host?.externalObservation} select={async () => {
        try {
          const result: Json = await invoke("select_external_observation");
          setMessage(`External selection: ${result.selection?.state ?? "unknown"} ${result.selection?.stage ?? ""}`);
        } catch (e) { setMessage(String(e)); }
        setHost(await invoke("host_status"));
      }} />

      <TraceReceivingPanel data={host?.traceReceiving} currentContext={{ hostState: host?.state, generation: host?.generation, nativeSupplier: host?.versionIdentity, supplierStanding: host?.supplierStanding, accessSelection: host?.accessSelection, accountObservation: host?.accountObservation, appExecutableIdentity: "not established by this selector" }} select={async (recordKind, evidenceKind) => {
        try {
          const received: Json = await invoke("select_trace_record", { recordKind, evidenceKind });
          setMessage(`Supplied trace selection: ${received.selection?.state ?? "unknown"}`);
        } finally { setHost(await invoke("host_status")); }
      }} />

      <DecisionPackagesPanel view={view} name={name} setName={setName} recordName={() => { void invoke("set_person_name", { name }); }} refresh={refresh} continueRecording={async () => { await act("continue_decision_recording"); }} openControl={openControl} />

      {offer && (
        <section style={{ border: "1px solid #888", padding: 8 }}>
          <h2>Act control: {offer.wording} ({offer.actKind})</h2>
          <p>
            {offer.subject.ref} · {offer.subject.contentIdentity.value}
            <br />
            Purpose: {offer.purpose} · Scope: {offer.scope} · {offer.answers.standing}
          </p>
          {offer.alternatives.map((a: Json) => (
            <label key={a.id} style={{ display: "block" }}>
              <input type="radio" name="alt" value={a.id} checked={choice === a.id} onChange={() => setChoice(a.id)} />{" "}
              <b>{a.id}</b> {a.statement} — {a.consequences.join("; ")}
            </label>
          ))}
          <p>The host shows its own confirmation with this text; only that confirmation records the decision.</p>
          <button onClick={decide} disabled={!choice}>Decide…</button> <button onClick={() => setOffer(null)}>Close</button>
        </section>
      )}

      <p>{message}</p>
    </main>
  );
}
