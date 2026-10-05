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
        <p>Model turn: not exercised in this path.</p>
        <h3>Expected network contacts</h3>
        <p>Codex can contact the selected model provider at thread start, before a model turn. This view describes supplier behavior; socket measurements remain separate evidence.</p>
        <ul>{(host?.networkDisclosure?.entries ?? []).map((entry: Json, index: number) => <li key={index}>{entry.purpose} · {entry.phase} · {entry.destination} · {entry.detail ?? entry.condition}</li>)}</ul>
        <details>
          <summary>Lifecycle events ({host?.lifecycle?.length ?? 0}) and frames ({host?.journal?.length ?? 0})</summary>
          <pre>{JSON.stringify({ lifecycle: host?.lifecycle, clientRequests: host?.clientRequests }, null, 2)}</pre>
        </details>
      </section>

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

      <section>
        <h2>Decision packages</h2>
        <p>
          Your name on acts you record:{" "}
          <input value={name} onChange={(e) => setName(e.target.value)} onBlur={() => invoke("set_person_name", { name })} />
        </p>
        {view?.error && <p>{view.error}</p>}
        {(view?.captureRecovery ?? []).filter((r: Json) => r.state !== "AC-7 recorded" || r.backlinkPending || r.delayEvidencePending).map((r: Json, i: number) => <p key={i}>Capture: {r.state} · {r.statusDetail ?? r.writeFailure ?? r.backlinkFailure ?? r.delayEvidenceFailure ?? r.captureDurability}</p>)}
        <button onClick={refresh}>Refresh and retry pending recording</button>
        {(view?.rows ?? []).map((r: Json) => (
          <article key={r.package} style={{ borderTop: "1px solid #ccc", paddingTop: 8 }}>
            <h3>
              {r.package} — {r.actRequested} — {r.state}
            </h3>
            <p>
              Subject: {(r.subject ?? []).join("; ")} · Purpose: {r.purpose} · Scope: {r.scope ?? "—"} · File: {r.packageFile}
            </p>
            <ul>
              {r.alternatives.map((a: Json) => (
                <li key={a.id}>
                  <b>{a.id}</b> {a.statement} — {a.consequences.join("; ")}
                </li>
              ))}
            </ul>
            {r.decision && (
              <p>
                Decided: <b>{r.decision.alternativeChosen}</b> {r.decision.statement} · decided by {r.decision.decidedBy} · recorded by{" "}
                {r.decision.recordedBy} ({r.decision.recordingMode}) · captured {r.decision.capturedAt} · {r.decision.lapse} · act{" "}
                {r.decision.act} · {r.decision.captureProvenance}
              </p>
            )}
            {r.limits.length > 0 && <p>Limits: {r.limits.join(" | ")}</p>}
            <button onClick={() => openControl(r.package)}>Open act control (decide)</button>
          </article>
        ))}
        {(view?.limits ?? []).length > 0 && <p>View limits: {view.limits.join(" | ")}</p>}
      </section>

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
