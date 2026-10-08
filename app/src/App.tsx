// The interface reads host snapshots and asks the host to act. It holds no pipe
// (HOSTING H2), writes no record and cannot capture an act: the native
// confirmation is the host's (AAC §6.2 P-2). Views per DECISION_VIEW.md §4.
import { useCallback, useEffect, useRef, useState } from "react";
import { invoke } from "@tauri-apps/api/core";
import { FileActPanel } from "./FileActPanel";
import { RecoveryCustodyPanel } from "./RecoveryCustodyPanel";
import { DIGEST_LIMIT, digestComparison, readablePaths, reviewDigest, suppliedSummary, type ReviewDigestView } from "./presentation";

type Json = any; // eslint-disable-line @typescript-eslint/no-explicit-any

// Request-local drafts are disposable. Secret content is never echoed or saved.
function NativeRequestCard({ request, answer }: { request: Json; answer: (r: Json, a: Json) => Promise<void> }) {
  const [drafts, setDrafts] = useState<Record<string, string>>({});
  const [scope, setScope] = useState("turn");
  const [content, setContent] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const p = request.nativeParameters ?? {};
  const method = request.method;
  const send = async (value: Json) => {
    setBusy(true); setError("");
    // Remove drafts from the rendered control before crossing the IPC boundary.
    setDrafts({}); setContent("");
    try { await answer(request, value); } catch (e) { setError(String(e)); }
    finally { setBusy(false); }
  };
  const button = (label: string, value: Json) => <button key={JSON.stringify(value)} disabled={busy} onClick={() => send(value)}>{label}</button>;
  const modern = method === "item/commandExecution/requestApproval" || method === "item/fileChange/requestApproval";
  const legacy = method === "execCommandApproval" || method === "applyPatchApproval";
  const formMode = ["form", "openai/form", "openaiForm"].includes(p.mode);
  const elicitationAcceptSupported = formMode || p.mode === "url";
  let decisions: Json[] = p.availableDecisions ?? ["accept", "acceptForSession", "decline", "cancel"];
  if (modern && !p.availableDecisions && method === "item/commandExecution/requestApproval") {
    if (p.proposedExecpolicyAmendment) decisions = [...decisions, { acceptWithExecpolicyAmendment: { execpolicy_amendment: p.proposedExecpolicyAmendment } }];
    for (const amendment of p.proposedNetworkPolicyAmendments ?? []) decisions = [...decisions, { applyNetworkPolicyAmendment: { network_policy_amendment: amendment } }];
  }
  return <article style={{ borderTop: "1px solid #ccc", padding: 8 }}>
    <h3>{method} · {JSON.stringify(request.requestIdentity)}</h3>
    <a href="#file-acts">Open standing App-file act facility (no request answer or prefilled act)</a>
    <p>State: {request.state} · reply: {request.replyWriteResult} · acknowledgment: {request.acknowledgmentObservation?.status ?? "not-observed"}</p>
    {request.supplierResolution && <p>Supplier resolution: {JSON.stringify(request.supplierResolution)}</p>}
    {request.settlement && <p>Settlement origin: {JSON.stringify(request.settlement.origin)} · {request.settlement.kind}</p>}
    <details><summary>Native request parameters and owning generation</summary><pre>{JSON.stringify({ generation: request.generation, parameters: p }, null, 2)}</pre></details>
    {request.state === "outstanding" && request.classification === "known-answerable" && request.originClass !== "named-service" && <div>
      {modern && decisions.map((decision: Json) => button(JSON.stringify(decision), { decision }))}
      {legacy && <>{["approved", "approved_for_session", "abort"].map(decision => button(decision, { decision }))}{button("denied", { decision: { denied: { rejection: "" } } })}</>}
      {method === "item/permissions/requestApproval" && <>
        <label>Grant scope <select value={scope} onChange={e => setScope(e.target.value)}><option value="turn">turn</option><option value="session">session</option></select></label>
        {button("Grant requested permissions", { permissions: p.permissions, scope })}{button("Grant nothing", { permissions: {}, scope })}
        <label>Partial permissions (native JSON) <input value={content} onChange={e => setContent(e.target.value)} /></label>
        <button disabled={busy || !content} onClick={() => { try { void send({ permissions: JSON.parse(content), scope }); } catch { setError("Invalid permission JSON"); } }}>Send partial grant…</button>
      </>}
      {method === "item/tool/requestUserInput" && <>
        {(p.questions ?? []).map((q: Json) => <div key={q.id}><p>{q.header}: {q.question}</p>
          {(q.options ?? []).map((o: Json) => <button disabled={busy} key={o.label} onClick={() => setDrafts(d => ({ ...d, [q.id]: o.label }))}>{o.label} · {o.description}</button>)}
          {q.isOther && <label>Answer <input autoComplete="off" type={q.isSecret ? "password" : "text"} value={drafts[q.id] ?? ""} onChange={e => setDrafts(d => ({ ...d, [q.id]: e.target.value }))} /></label>}
          <button disabled={busy} onClick={() => setDrafts(d => { const next = { ...d }; delete next[q.id]; return next; })}>Leave unanswered</button>
          {!q.isOther && <p>Selected: {q.isSecret ? (drafts[q.id] ? "[masked]" : "—") : drafts[q.id] ?? "—"}</p>}
        </div>)}
        <button disabled={busy} onClick={() => send({ answers: Object.fromEntries(Object.entries(drafts).map(([id, value]) => [id, { answers: [value] }])) })}>Send current question answers…</button>
        <p>Unanswered questions are omitted; entered empty answers are preserved.</p>
        {button("Decline question input", { answers: {} })}
      </>}
      {method === "mcpServer/elicitation/request" && <>
        <p>Native elicitation mode: {p.mode}. Requested schema is available above.</p>
        {formMode && <label>Native form content (JSON, masked) <input type="password" autoComplete="off" value={content} onChange={e => setContent(e.target.value)} /></label>}
        {elicitationAcceptSupported && <button disabled={busy || (formMode && !content)} onClick={() => { try { void send({ action: "accept", content: formMode ? JSON.parse(content) : null, _meta: null }); } catch { setError("Invalid native form JSON"); } }}>accept…</button>}
        {!elicitationAcceptSupported && <p>Acceptance is not supported for this mode in this App path. Device verification requires actual device proof; this App supplies none.</p>}
        {button("decline", { action: "decline", content: null, _meta: null })}{button("cancel", { action: "cancel", content: null, _meta: null })}
      </>}
      <p>Sending opens a native confirmation. Closing this card leaves the request waiting.</p>
    </div>}
    {error && <p role="alert">{error}</p>}
  </article>;
}

export function SteeringControl({ target, reason, ready, busy, text, submit }: { target: Json; reason?: string; ready: boolean; busy: boolean; text: string; submit: () => void }) {
  return <div>
    <p>Current observed steering turn: {target?.turnId ?? "not established"} {target?.source && `· ${target.source}`}.</p>
    {!target && <p>{reason ?? "Choose a loaded conversation with an observed current live turn."}</p>}
    <button disabled={!ready || busy || !target?.turnId || !text} onClick={submit}>Steer current live turn</button>
    <p>Steering sends this text unchanged with the expected native turn ID. A steering acknowledgment does not establish turn replacement or completion. Source/target changes can refuse the request; the draft is retained on failure and no automatic resend occurs.</p>
  </div>;
}

function ConversationPanel({ host, send, steer, submitAttachments, interrupt }: { host: Json; submitAttachments: (generation: Json, thread: string, expected: string | null, text: string, owner: string, revision: number, refs: string[]) => Promise<void>; send: (generation: Json, thread: string, text: string) => Promise<void>; steer: (generation: Json, thread: string, expected: string, text: string) => Promise<void>; interrupt: (generation: Json, thread: string, turn: string) => Promise<void> }) {
  const [threadKey, setThreadKey] = useState<string>("");
  const [turnId, setTurnId] = useState<string>("");
  const [text, setText] = useState<string>("");
  const [busy, setBusy] = useState<string>("");
  const [error, setError] = useState<string>("");
  const generationKey = JSON.stringify(host?.generation);
  const currentThreads = (host?.threads ?? []).filter((thread: Json) => JSON.stringify(thread.generation) === generationKey);
  const selected = currentThreads.find((thread: Json) => JSON.stringify([thread.generation, thread.threadId]) === threadKey);
  const liveTurns = (host?.conversationTurns ?? []).filter((turn: Json) => selected && JSON.stringify(turn.generation) === generationKey && turn.threadId === selected.threadId && turn.nativeTurn?.status === "inProgress" && !turn.observationEnded && !turn.terminalEventObserved);
  const live = liveTurns.find((turn: Json) => turn.turnId === turnId);
  const steering = (host?.steeringTargets ?? []).find((row: Json) => selected && JSON.stringify(row.generation) === generationKey && row.threadId === selected.threadId);
  const steeringTarget = steering?.target && JSON.stringify(steering.target.generation) === generationKey && steering.target.threadId === selected?.threadId ? steering.target : null;
  const alreadyRequested = (host?.turnInterruptRequests ?? []).some((request: Json) => live && JSON.stringify(request.binding?.generation) === generationKey && request.binding?.threadId === live.threadId && request.binding?.turnId === live.turnId && (request.clientRequest?.outcome === "response-observed-result" || (request.clientRequest?.outcome === "pending" && request.clientRequest?.writeResult === "written")));
  const sendText = async () => {
    if (!selected || !text || busy) return;
    setBusy("sending"); setError("");
    try { await send(selected.generation, selected.threadId, text); setText(""); }
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
    if (!selected || !live || busy || alreadyRequested) return;
    setBusy("interrupting"); setError("");
    try { await interrupt(live.generation, live.threadId, live.turnId); }
    catch (e) { setError(String(e)); }
    finally { setBusy(""); }
  };
  return <section>
    <h2>Conversation text and turn control</h2>
    <label>Current-generation conversation <select disabled={!!busy} value={threadKey} onChange={e => { setThreadKey(e.target.value); setTurnId(""); setError(""); }}>
      <option value="">Select a conversation</option>
      {currentThreads.map((thread: Json) => <option key={JSON.stringify([thread.generation, thread.threadId])} value={JSON.stringify([thread.generation, thread.threadId])}>{thread.threadId} · {thread.model ?? "model not reported"} via {thread.modelProvider ?? "provider not reported"}</option>)}
    </select></label>
    {selected && <p>Original App role: {JSON.stringify(selected.appRole ?? { standing: "unknown", reason: "original App supply binding not established" })}. Native role hints do not establish an App role.</p>}
    {(selected?.futureGuidanceNotices ?? []).map((notice: Json) => <p key={notice.path}>{notice.path}: {notice.reason}; applies to future conversations.</p>)}
    {threadKey && !selected && <p>Selected conversation is no longer available in this generation; choose a current conversation.</p>}
    <p><label>Text <textarea disabled={!!busy} value={text} onChange={e => setText(e.target.value)} rows={4} style={{ display: "block", width: "100%" }} /></label></p>
    <button disabled={host?.state !== "ready" || !selected || !text || !!busy} onClick={sendText}>{(host?.attachmentSelections?.selections ?? []).length > 0 ? "Send text only" : "Send text"}</button>
    {(host?.attachmentSelections?.selections ?? []).length > 0 && <p>This plain-text action excludes the selected attachments. Use the explicit ordered-attachment action to include the entire private selection.</p>}
    <p>Text is sent unchanged to the selected native conversation. Its role, model and provider remain the conversation's existing settings.</p>
    {(host?.attachmentSelections?.selections ?? []).length > 0 && <div>
      <button disabled={host?.state !== "ready" || !selected || !!busy || host?.attachmentCustody?.state !== "opened"} onClick={() => attachmentText(null)}>Send text and ordered attachments</button>{" "}
      <button disabled={host?.state !== "ready" || !selected || !steeringTarget || !!busy || host?.attachmentCustody?.state !== "opened"} onClick={() => attachmentText(steeringTarget.turnId)}>Steer current turn with ordered attachments</button>
      <p>Every selected source is revalidated as one whole list. Source/custody/context failures retain the draft and evidence; no text-only fallback or automatic resend. Native acknowledgments remain separate from completion and provider uptake.</p>
      {host?.attachmentCustody?.state !== "opened" && <p>Attachment custody unavailable: {host?.attachmentCustody?.error}. Plain-text controls remain available.</p>}
    </div>}
    <SteeringControl target={steeringTarget} reason={steering?.reason} ready={host?.state === "ready" && !!selected} busy={!!busy} text={text} submit={() => { void steerText(); }} />
    <label>Observed live turn <select disabled={!!busy} value={turnId} onChange={e => setTurnId(e.target.value)}><option value="">Select a live turn</option>{liveTurns.map((turn: Json) => <option key={turn.turnId} value={turn.turnId}>{turn.turnId} · {turn.nativeTurn.status}</option>)}</select></label>{" "}
    <button disabled={host?.state !== "ready" || !live || !!busy || alreadyRequested} onClick={interruptTurn}>Interrupt selected live turn</button>
    <p>An interrupt acknowledgment does not establish turn end or rollback. Turn status comes from native observations.</p>
    {(host?.conversationTurns ?? []).filter((turn: Json) => turn.terminalEventObserved && turn.nativeTurn?.status === "inProgress").map((turn: Json) => <p key={JSON.stringify([turn.generation, turn.threadId, turn.turnId])}>Native turn inconsistency: {turn.threadId}/{turn.turnId} has a terminal event observation and contradictory progress status; interruption is unavailable.</p>)}
    {(host?.conversationTurns ?? []).flatMap((turn: Json) => (turn.inconsistencyLimits ?? []).map((limit: Json, index: number) => <p key={JSON.stringify([turn.generation, turn.threadId, turn.turnId, index])}>Native lifecycle limit for {JSON.stringify(turn.generation)} · {turn.threadId}/{turn.turnId}: {JSON.stringify(limit)}</p>))}
    {alreadyRequested && <p>Interrupt already requested; awaiting native turn status.</p>}
    {busy && <p>{busy}: waiting for protocol response; no automatic retry.</p>}
    {error && <p role="alert">{error} No automatic retry.</p>}
    <p>Text-turn protocol requests: {host?.modelTurnEvidence?.protocolRequests?.length ?? 0}. {host?.modelTurnEvidence?.standing ?? "Provider/model execution is not established by this view."}</p>
    <details open><summary>Observed native turns, steering and interrupt request state</summary><pre style={{ whiteSpace: "pre-wrap" }}>{JSON.stringify({ turns: host?.conversationTurns, steeringTargets: host?.steeringTargets, steeringRequests: (host?.clientRequests ?? []).filter((request: Json) => request.method === "turn/steer"), interrupts: host?.turnInterruptRequests, protocolEvidence: host?.modelTurnEvidence }, null, 2)}</pre></details>
  </section>;
}

export function HistoryPanel({ host, refresh }: { host: Json; refresh: () => Promise<void> }) {
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [direction, setDirection] = useState("desc");
  const history = host?.nativeHistory;
  const selected = history?.selected;
  const generation = history?.generation;
  const epoch = history?.selectionEpoch;
  const available = host?.state === "ready" && history?.state === "history-receiving" && JSON.stringify(generation) === JSON.stringify(host?.generation);
  const run = async (action: string, cursor: string | null = null, reference: string | null = null, pagingDirection = direction) => {
    setBusy(true); setError("");
    try { await invoke("history_action", { generation, selectionEpoch: epoch, action, cursor, direction: pagingDirection, reference }); }
    catch (e) { setError(String(e)); }
    finally { try { await refresh(); } catch (e) { setError(String(e)); } setBusy(false); }
  };
  const select = async (threadId: string) => {
    if (!threadId) return;
    setBusy(true); setError("");
    try { await invoke("history_select", { generation, selectionEpoch: epoch, threadId }); }
    catch (e) { setError(String(e)); }
    finally { try { await refresh(); } catch (e) { setError(String(e)); } setBusy(false); }
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
      {(selected.futureGuidanceNotices ?? []).map((notice: Json) => <p key={notice.path}>{notice.path}: {notice.reason}; applies to future conversations. This conversation retains its original role.</p>)}
      <button disabled={!available || busy} onClick={() => run("metadata")}>Read metadata</button>{" "}
      <button disabled={!available || busy} onClick={() => run("turns")}>Read turns</button>{" "}
      <button disabled={!available || busy} onClick={() => run("goal")}>Read goal</button>{" "}
      <button disabled={!available || busy} onClick={() => run("continue")}>Continue selected conversation</button>
      <p>Current resume eligibility: {String(selected.resumeEligibilityCurrent ?? false)}. Active admission is reported in the dispatch evidence below and the operational conversation selector.</p>
      <p>Continue sends the native thread ID and waits for a matching resume response before active admission. Its existing guidance and settings remain in force. No automatic resend.</p>
      <p>Goal: {selected.goalAvailability}. {selected.goal?.goal === null ? "Native reported no goal." : selected.goal ? JSON.stringify(selected.goal.goal) : "Goal has not been read."}</p>
      <p>{selected.checklists}</p>
      <h3>Turns</h3>{pageButtons("turns", selected.turnsPage, null, selected.turnDirection ?? direction)}
      {selected.turnsPage?.data?.length === 0 && <p>Native returned an empty turn page.</p>}
      {(selected.turnsPage?.data ?? []).map((turn: Json) => <article key={turn.id}><p>{turn.id} · {turn.status} · items view: {turn.itemsView ?? "not reported"}</p><button disabled={!available || busy} onClick={() => run("items", null, turn.id)}>Read items for this turn</button><details><summary>Native turn summary</summary><pre>{JSON.stringify(turn, null, 2)}</pre></details></article>)}
      <h3>Selected item page</h3>{pageButtons("items", selected.itemsPage, selected.itemTurnId ?? null, selected.itemDirection ?? direction)}
      <pre style={{ whiteSpace: "pre-wrap" }}>{JSON.stringify(selected.itemsPage ?? { state: "not read" }, null, 2)}</pre>
      <h3>Native child references</h3>
      {(selected.knownChildren ?? []).map((child: Json) => <p key={child.threadId}>{child.threadId} · source {child.sourceItemId} <button disabled={!available || busy} onClick={() => run("child", null, child.threadId)}>Read child metadata</button></p>)}
      <details><summary>Metadata, child reads, standalone receiver references and stream errors</summary><pre style={{ whiteSpace: "pre-wrap" }}>{JSON.stringify({ metadata: selected.metadata, childReads: selected.childReads, receiverReferences: selected.receiverReferences, errors: selected.errorsByStream, errorHistory: selected.errorHistory, resolutions: selected.streamResolutions, resumeEligibilityCurrent: selected.resumeEligibilityCurrent }, null, 2)}</pre></details>
      {selected.originalRoleSupply && <details><summary>Original App role supply evidence (memory only; adoption unknown)</summary><pre style={{ whiteSpace: "pre-wrap" }}>{JSON.stringify(selected.originalRoleSupply, null, 2)}</pre></details>}
    </>}
    {busy && <p>Waiting for native protocol response; no automatic retry.</p>}
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
      <pre style={{ whiteSpace: "pre-wrap" }}>{JSON.stringify(readablePaths(row.content), null, 2)}</pre>
    </article>)}
  </section>;
}

export function WorkflowRootPanel({ data, host, act }:{ data: Json; host: Json; act: (command:string,args:Record<string,unknown>)=>Promise<Json> }) {
  const [name,setName]=useState("coordinated-knowledge-work");
  const [inPlace,setInPlace]=useState(false);
  const [revision,setRevision]=useState("");
  const [thread,setThread]=useState("");
  const [text,setText]=useState("");
  const [busy,setBusy]=useState(false);
  const [message,setMessage]=useState("");
  const action=async(command:string,args:Record<string,unknown>)=>{setBusy(true);try{const result=await act(command,args);setMessage(JSON.stringify(result));}catch(e){setMessage(String(e));}finally{setBusy(false);}};
  const entries:Json[]=data?.reviews??[];
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
    <p>Development content, native registration, supplied text, model adoption and run standing remain separate observations.</p>
    <p>Bundle candidate content can be inspected or copied into a draft. It is not runnable as a shipped workflow; release registration remains pending.</p>
    {(data?.productionCatalog?.entries??[]).map((entry:Json)=><article key={entry.name}>
      <p>{entry.name} · {entry.revision}</p>
      <button disabled={busy} onClick={()=>action("workflow_select_production_bundle",{name:entry.name})}>Inspect bundled candidate</button>
      <button disabled={busy||!data?.activeLibrary} onClick={()=>action("workflow_select_production_copy",{name:entry.name})}>Inspect matching candidate in opened library</button>
    </article>)}
    <button disabled={busy} onClick={()=>action("workflow_select_development",{})}>Select exact development workflow holding copy…</button>
    <button disabled={busy} onClick={()=>action("workflow_open_library",{origin:"project"})}>Open project workflow library…</button>
    <button disabled={busy} onClick={()=>action("workflow_open_library",{origin:"user"})}>Open user workflow library…</button>
    <p>Paths are shown as text (display only: identities keep their exact bytes; a path that is not valid UTF-8 is marked).</p>
    <pre style={{whiteSpace:"pre-wrap"}}>{JSON.stringify(readablePaths({selection:data?.selection,libraries:data?.libraries,activeLibrary:data?.activeLibrary}),null,2)}</pre>
    <label>Draft or entry name <input value={name} onChange={e=>setName(e.target.value)} disabled={busy}/></label>
    <button disabled={busy||!data?.selection||!data?.activeLibrary} onClick={()=>action("workflow_create_draft",{name})}>Create draft from selected content</button>
    {(data?.libraries??[]).filter((l:Json)=>l.reference===data?.activeLibrary&&Array.isArray(l.registered)).map((l:Json)=><ul key={l.reference} aria-label="Registered revisions in the active library">{l.registered.map((row:Json)=><li key={`${row.name}@${row.revision}`}>{row.name} · revision {row.sequence} · {row.label} <button disabled={busy} onClick={()=>action("workflow_refine_registered",{name:row.name,revision:row.revision})}>Refine from the revision store…</button></li>)}</ul>)}
    <label>Registered revision (content identity) <input value={revision} onChange={e=>setRevision(e.target.value)} disabled={busy}/></label>
    <button disabled={busy||!data?.activeLibrary||!name||!revision} onClick={()=>action("workflow_refine_registered",{name,revision})}>Refine registered revision from the revision store (no selection)</button>
    <label><input type="checkbox" checked={inPlace} onChange={e=>setInPlace(e.target.checked)} disabled={busy}/> Review existing unregistered in-place entry</label>
    <button disabled={busy||!data?.activeLibrary||!name} onClick={()=>action("workflow_review",{names:[name],inPlace})}>Read actual library entry for review</button>
    {entries.map(review=><article key={review.reference}>
      <h3>{review.reference}</h3>
      {digests[review.reference]&&<p>{digestComparison(digests[review.reference])}{review.status?.presentation?"":" (as last shown with the review; while the native confirmation is open, the review it names is shown under \"Content named by an open native confirmation\")"}. Read the complete review below before choosing {review.status?.presentation?.entries?.[0]?.disposition==="re-confirmation"?"Re-confirm":"Register"}: the native confirmation shows the act statement and this digest, not the review itself.</p>}
      {review.status?.presentation?.entries?.[0]?.disposition==="re-confirmation"&&<p role="note">{review.status.presentation.entries[0].message}. {review.status.presentation.entries[0].reconfirmation?.statement}</p>}
      <pre style={{whiteSpace:"pre-wrap"}}>{JSON.stringify(readablePaths(review.status??review),null,2)}</pre>
      <button disabled={busy||review.reference!==data?.activeReview} onClick={()=>action("workflow_register_native",{reviewRef:review.reference})}>{review.status?.presentation?.entries?.[0]?.disposition==="re-confirmation"?"Re-confirm this revision for use in this App session through native A15 confirmation…":"Register this review through native A15 confirmation…"}</button>
      <button disabled={busy} onClick={()=>action("workflow_continue_registration",{reviewRef:review.reference})}>Continue original captured registration</button>
      {(review.status?.entries??[]).filter((entry:Json)=>entry.state==="registered"||entry.state==="re-confirmed").map((entry:Json)=><button key={entry.identity.revision} disabled={busy} onClick={()=>action("workflow_select_registered",{reviewRef:review.reference,revision:entry.identity.revision})}>Select hot {entry.state} {entry.identity.name} holding copy…</button>)}
    </article>)}
    <h3>Send selected workflow text</h3>
    <label>Current native conversation <select value={thread} onChange={e=>setThread(e.target.value)} disabled={busy}><option value="">Select conversation</option>{(host?.threads??[]).filter((entry:Json)=>JSON.stringify(entry.generation)===JSON.stringify(host?.generation)).map((entry:Json)=><option key={entry.threadId} value={entry.threadId}>{entry.threadId} · {entry.modelProvider}/{entry.model}</option>)}</select></label>
    <label>Person text <textarea value={text} onChange={e=>setText(e.target.value)} disabled={busy} rows={3}/></label>
    {data?.selection&&data.selection.runnable!==true&&<p role="note">Not runnable: {data.selection.runLimit}</p>}
    <button disabled={busy||host?.state!=="ready"||!thread||data?.selection?.runnable!==true} onClick={()=>action("workflow_prepare_run",{generation:host.generation,threadId:thread,personText:text})}>Prepare exact selected workflow text</button>
    <button disabled={busy} onClick={()=>action("workflow_read_records",{})}>Read recorded workflow supply (durable, read-only)</button>
    <button disabled={busy} onClick={()=>action("workflow_reopen",{})}>Reopen recorded workflow runs (read-only)</button>
    {data?.reopened&&<article><h3>Recorded runs (reopened from project records)</h3><p>{data.reopened.standing}</p>
      <ul>{(data.reopened.runs??[]).map((r:Json)=><li key={r.run}>{r.run} · conversation {r.conversation??"unknown"} · {r.state}{r.detail?` (${typeof r.detail==="string"?r.detail:JSON.stringify(r.detail)})`:""}{r.follows?` · follows ${r.follows}`:""}{(r.restartInterruptions??[]).length?` · App restart interruptions: ${r.restartInterruptions.length}`:""}
        {r.state?.startsWith("open")&&!(data?.runs??[]).some((h:Json)=>h.reference===r.run)&&<button disabled={busy} onClick={()=>action("workflow_end_recorded",{runId:r.run,threadId:r.conversation??null})}>End this interrupted run</button>}</li>)}</ul>
      {(data.reopened.limits??[]).length>0&&<p>Record limits: {JSON.stringify(data.reopened.limits)}</p>}</article>}
    {(data?.runs??[]).map((run:Json)=><article key={run.reference}><h3>{run.reference}</h3>
      <p>Run: {run.lifecycle?.state}{run.lifecycle?.follows?` · follows ${run.lifecycle.follows}`:""}{run.lifecycle?.end?` · ${run.lifecycle.end.cause}`:""}. Records: {run.publication?.state}. Send: {run.status?.state}{run.status?.limit?` (${run.status.limit})`:""}. Supplied: {suppliedSummary(run)}. Adoption: unknown.</p>
      {run.endNotice&&<p>End notice: {run.endNotice.state}</p>}
      {run.endNotice?.state?.startsWith("pending")&&<p role="status">Ordinary messages in this conversation wait for this end notice: it goes first, once.{run.status?.limit?` Last attempt: ${run.status.limit}`:""}
        <button disabled={busy} onClick={()=>action("workflow_retry_records",{runRef:run.reference})}>Retry the end-notice record</button>
        {run.noticeRecordFailure&&<button disabled={busy} onClick={()=>action("workflow_skip_notice",{runRef:run.reference})}>Send without the end notice (recorded as not supplied)</button>}</p>}
      <ul>{[...(run.checks??[]),...(run.noticeChecks??[])].map((check:Json)=><li key={check.reference}>{check.readAt}: {check.state} ({check.supplyReading}); check record {check.published?"recorded":`pending${check.publicationLimit?` — ${check.publicationLimit}`:""}`}; R3 {check.r3?.state}{check.r3?.limit?` — ${check.r3.limit}`:""}</li>)}</ul>
      <ul>{(run.compatibility??[]).map((c:Json,i:number)=><li key={i}>{c.occasion} (advisory, never gates a start): {c.statement??c.state??c.checkResult??"evaluated"}; publication {c.publication?.state}; {c.r14}</li>)}</ul>
      <details><summary>Complete run evidence (paths shown as text)</summary><pre style={{whiteSpace:"pre-wrap"}}>{JSON.stringify(readablePaths(run),null,2)}</pre></details>
      <button disabled={busy||!!run.source||host?.state!=="ready"} onClick={()=>action("workflow_send_run",{runRef:run.reference})}>Record, then send original prepared text once</button>
      <button disabled={busy||!run.turn||host?.state!=="ready"} onClick={()=>action("workflow_check_supply",{runRef:run.reference})}>Check original native supplied text pages (new check)</button>
      <button disabled={busy||!run.pendingRecords} onClick={()=>action("workflow_retry_records",{runRef:run.reference})}>Retry pending records (never sends)</button>
      {run.lifecycle?.state?.startsWith("open")&&<>
        <button disabled={busy} onClick={()=>action("workflow_end_run",{runRef:run.reference,completed:false})}>End run</button>
        <button disabled={busy} onClick={()=>action("workflow_end_run",{runRef:run.reference,completed:true})}>End run (the workflow is finished)</button>
        <button disabled={busy||host?.state!=="ready"||data?.selection?.runnable!==true} onClick={()=>action("workflow_end_and_start",{runRef:run.reference,generation:host.generation,threadId:run.conversation,personText:text})}>End this run and start {data?.selection?.identity?.name??"the selected workflow"}</button>
      </>}
      {run.endNotice?.state?.startsWith("sent")&&<button disabled={busy||host?.state!=="ready"} onClick={()=>action("workflow_check_notice",{runRef:run.reference})}>Check the end notice in native history (new check)</button>}
      <p>Selection and run text are recorded before sending; if recording fails nothing is sent. A run opens when its start turn is observed and ends only when the person ends it: an interrupt, stop, quit, failed or completed turn, or an agent's "finished" line does not end it. After an end, the next ordinary message in this conversation carries the end notice once. Load/select this conversation and its received turn in native History before checking.</p>
    </article>)}
    {message&&<p role="status" style={{whiteSpace:"pre-wrap"}}>{message}</p>}
  </section>;
}

export function HomeAccessPanel({ routing, access, resources, oauth, generation, act }: { routing: Json; access: Json; resources: Json; oauth?: Json; generation: Json; act: (command: string, args: Record<string, unknown>) => Promise<void> }) {
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const action = async (command: string, args: Record<string, unknown>) => {
    setBusy(true); setError("");
    try { await act(command, args); } catch (e) { setError(String(e)); } finally { setBusy(false); }
  };
  const entries: Json[] = routing?.entries ?? [];
  return <section><h2>Separate Codex homes and access</h2>
    <p>Active home class: {routing?.activeModeHomeClass ?? "unavailable"}. The full native generation identifies its owning source; switching homes does not transfer a conversation.</p>
    {entries.map(entry => <article key={entry.modeHomeClass}><p>{entry.modeHomeClass} · {entry.state} · {JSON.stringify(entry.generation)} · {entry.configurationLimit}</p><button disabled={busy || routing?.activeModeHomeClass === entry.modeHomeClass} onClick={() => action("select_home", {modeHomeClass: entry.modeHomeClass})}>Use {entry.modeHomeClass} home</button></article>)}
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
    {rows.map((row, index) => <article key={row.selection.selectionRef} style={{ borderTop: "1px solid #ccc", paddingTop: 8 }}>
      <h3>{index + 1}. {row.selection.displayName} · {row.selection.standing}</h3>
      <p>{row.selection.displayPath} · carrier: {row.selection.carrier}.</p>
      <pre>{JSON.stringify(readablePaths({ selectionRef: row.selection.selectionRef, nativePath: row.selection.nativePath, identityAtSelection: row.selection.identityAtSelection, draft: row.selection.draft }), null, 2)}</pre>
      <button disabled={busy || index === 0} onClick={() => move(index, -1)}>Move earlier</button>{" "}
      <button disabled={busy || index === rows.length - 1} onClick={() => move(index, 1)}>Move later</button>{" "}
      <button disabled={busy} onClick={() => invokeAction("remove_attachment", { selectionRef: row.selection.selectionRef })}>Remove</button>{" "}
      <button disabled={busy} onClick={() => invokeAction("reconfirm_attachment", { selectionRef: row.selection.selectionRef })}>Confirm current source…</button>
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
    <p>Your name on acts you record: <input value={name} onChange={e => setName(e.target.value)} onBlur={recordName} /></p>
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
  const [host, setHost] = useState<Json>(null);
  const [view, setView] = useState<Json>(null);
  const [offer, setOffer] = useState<Json>(null);
  const [choice, setChoice] = useState<string>("");
  const [name, setName] = useState<string>("");
  const [message, setMessage] = useState<string>("");
  const [model, setModel] = useState<string>("");
  const [modelProvider, setModelProvider] = useState<string>("");
  const [entryId, setEntryId] = useState<string>("");
  const [role, setRole] = useState<string>("");
  const roleInitialized = useRef(false);
  useEffect(() => {
    if (!roleInitialized.current && host?.roleSet?.available) {
      roleInitialized.current = true;
      setRole(host.roleSet.defaultRole ?? "");
    }
  }, [host?.roleSet]);


  const refresh = useCallback(async () => {
    setHost(await invoke("host_status"));
    try {
      setView(await invoke("decision_view"));
    } catch (e) {
      setView({ error: String(e) });
    }
  }, []);

  useEffect(() => {
    refresh();
    const t = setInterval(() => invoke("host_status").then(setHost).catch(e => setMessage(String(e))), 1000);
    return () => clearInterval(t);
  }, [refresh]);

  const act = async (cmd: string, args?: Record<string, unknown>) => {
    try {
      const r = await invoke(cmd, args);
      setMessage(`${cmd}: ${JSON.stringify(r).slice(0, 300)}`);
    } catch (e) {
      setMessage(`${cmd}: ${String(e)}`);
    }
    await refresh();
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
      <NativeConfirmationContent />
      <FileActPanel command={(name,args)=>invoke(name,args)} />

      <WorkflowRootPanel data={host?.workflowRoot} host={host} act={async(command,args)=>{const result=await invoke<Json>(command,args);await refresh();return result;}} />
      <HomeAccessPanel routing={host?.homeRouting} access={host?.homeAccess} oauth={host?.homeOAuth} resources={{...host?.homeResources,namespaceProtection:host?.nativeNamespaces,keyAdmission:host?.keyNamespaceAdmission}} generation={host?.generation} act={async (command,args) => { await invoke(command,args); await refresh(); }} />

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
          <label>Model <input value={model} onChange={(e) => setModel(e.target.value)} /></label>{" "}
          <label>Configured Codex provider <input value={modelProvider} onChange={(e) => setModelProvider(e.target.value)} /></label>
        </p>
        <p><label>Access entry <select value={entryId} onChange={e => setEntryId(e.target.value)}><option value="">No entry selected</option>{host?.homeRouting?.activeModeHomeClass === "api-key" ? <option value="api-key">API key in separate configured key home</option> : <><option value="chatgpt-account">ChatGPT account in configured account home</option><option value="local-provider">Configured local provider</option></>}</select></label></p>
        <p>Choose a model, provider and entry for this new conversation in the selected home. Switching homes never transfers an existing conversation.</p>
        <p><label>Conversation role <select value={role} onChange={e => { roleInitialized.current = true; setRole(e.target.value); }}><option value="">No role selected</option>{(host?.roleSet?.roles??[]).filter((entry:Json)=>entry.name!=="TASK").map((entry:Json)=><option key={entry.name} value={entry.name}>{entry.name}</option>)}</select></label></p>
        <p>Role set: {host?.roleSet?.standing ?? host?.roleSet?.reason ?? "unavailable"}</p>
        <p>Role guidance: {JSON.stringify(host?.roleSupply)} {host?.instructionsProblem}</p>
        <p>Selection: {host?.accessSelection ? JSON.stringify(host.accessSelection) : "No model selected"}</p>
        <p>Account (App-observed, identity not verified): {JSON.stringify(host?.accountObservation ?? { state: "unknown" })}</p>
        <p>
          <button onClick={() => act("thread_start", { model, modelProvider, entryId, modeHomeClass: host?.homeRouting?.activeModeHomeClass, role: role || null })} disabled={host?.state !== "ready" || !model.trim() || !modelProvider.trim() || !entryId}>Start thread</button>{" "}
          <button onClick={() => act("host_start", {modeHomeClass:host?.homeRouting?.activeModeHomeClass})}>Start Codex</button>{" "}
          <button onClick={() => act("host_stop", {generation:host?.generation})}>Stop Codex</button>
        </p>
        <p>Threads: {(host?.threads ?? []).map((t: Json) => `${t.threadId} (${t.status?.type ?? "?"}, gen ${JSON.stringify(t.generation)})`).join(", ") || "none"}</p>

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
        read={() => invoke("read_recovery_custody", { modeHomeClass: host?.homeRouting?.activeModeHomeClass, generation: host?.generation ?? null })} />
      <HistoryPanel host={host} refresh={refresh} />

      <ConversationPanel host={host} send={async (generation, threadId, text) => {
        await conversationAction("conversation_send_text", { generation, threadId, text });
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
        <p>Ledger: {host?.recoveryInitialization?.path?.displayPath ?? "location not established"} {host?.recoveryInitialization?.path?.pathDisplayLimit}</p>
        {host?.recoveryInitialization?.configurationError && <p role="alert">Ledger initialization failed: {host.recoveryInitialization.configurationError}. Ledger failure does not block native supplier processing; App recovery recording remains limited.</p>}
        <p>Directory publication: {host?.recoveryInitialization?.directoryPublication ?? "not established"} · later persistence failure: {host?.recoveryPersistenceError ?? "none reported"}</p>
        <details><summary>Recovery initialization and historical pointer state</summary><pre>{JSON.stringify({ initialization: host?.recoveryInitialization, recovery: host?.recovery }, null, 2)}</pre></details>
        <p>Observer: {JSON.stringify(host?.observerCursor)} · gap: {String(host?.observerGap ?? true)}</p>
        {(host?.nativeViewLimits ?? []).map((limit: string, i: number) => <p key={i}>{limit}</p>)}
        {(host?.serverRequests ?? []).map((request: Json) => <NativeRequestCard key={JSON.stringify([request.generation, request.requestIdentity])} request={request} answer={async (r, answer) => {
          try {
            const result = await invoke("answer_native_request", { generation: r.generation, requestId: r.requestIdentity, answer });
            setMessage(`Native answer: ${JSON.stringify(result)}`);
          } finally { await refresh(); }
        }} />)}
        <a href="#file-acts">Act on a saved App-side output file (select it explicitly)</a>
        <details><summary>Native plans, tools, goals, turns and descendants</summary><pre>{JSON.stringify({ current: host?.nativeView, observationEnded: host?.nativeViewObservationEnded, priorObservations: host?.priorNativeViews, recovery: host?.observerRecovery }, null, 2)}</pre></details>
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
