// The interface reads host snapshots and asks the host to act. It holds no pipe
// (HOSTING H2), writes no record and cannot capture an act: the native
// confirmation is the host's (AAC §6.2 P-2). Views per DECISION_VIEW.md §4.
import { useCallback, useEffect, useState } from "react";
import { invoke } from "@tauri-apps/api/core";

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

function ConversationPanel({ host, send, steer, interrupt }: { host: Json; send: (generation: Json, thread: string, text: string) => Promise<void>; steer: (generation: Json, thread: string, expected: string, text: string) => Promise<void>; interrupt: (generation: Json, thread: string, turn: string) => Promise<void> }) {
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
    <button disabled={host?.state !== "ready" || !selected || !text || !!busy} onClick={sendText}>Send text</button>
    <p>Text is sent unchanged to the selected native conversation. Its role, model and provider remain the conversation's existing settings.</p>
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
        <p><label>Access entry <select value={entryId} onChange={e => setEntryId(e.target.value)}><option value="">No entry selected</option><option value="chatgpt-account">ChatGPT account in configured account home</option><option value="local-provider">Configured local provider</option></select></label></p>
        <p>Choose a model, provider and entry for this new conversation. API-key home is not connected.</p>
        <p><label>Conversation role <select value={role} onChange={e => setRole(e.target.value)}><option value="">No role selected</option><option value="HELP_HUMAN">HELP_HUMAN</option><option value="HELPS_HUMANS">HELPS_HUMANS</option><option value="WORKING_ITEMS">WORKING_ITEMS</option></select></label></p>
        <p>Role guidance: {JSON.stringify(host?.roleSupply)} {host?.instructionsProblem}</p>
        <p>Selection: {host?.accessSelection ? JSON.stringify(host.accessSelection) : "No model selected"}</p>
        <p>Account (App-observed, identity not verified): {JSON.stringify(host?.accountObservation ?? { state: "unknown" })}</p>
        <p>
          <button onClick={() => act("thread_start", { model, modelProvider, entryId, role: role || null })} disabled={host?.state !== "ready" || !model.trim() || !modelProvider.trim() || !entryId}>Start thread</button>{" "}
          <button onClick={() => act("host_start")}>Start Codex</button>{" "}
          <button onClick={() => act("host_stop")}>Stop Codex</button>
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

      <HistoryPanel host={host} refresh={refresh} />

      <ConversationPanel host={host} send={async (generation, threadId, text) => {
        await conversationAction("conversation_send_text", { generation, threadId, text });
      }} steer={async (generation, threadId, expectedTurnId, text) => {
        await conversationAction("conversation_steer_text", { generation, threadId, expectedTurnId, text });
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
