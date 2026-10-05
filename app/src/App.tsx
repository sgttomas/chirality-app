// The interface reads host snapshots and asks the host to act. It holds no pipe
// (HOSTING H2), writes no record and cannot capture an act: the native
// confirmation is the host's (AAC §6.2 P-2). Views per DECISION_VIEW.md §4.
import { useCallback, useEffect, useState } from "react";
import { invoke } from "@tauri-apps/api/core";

type Json = any; // eslint-disable-line @typescript-eslint/no-explicit-any

export function App() {
  const [host, setHost] = useState<Json>(null);
  const [view, setView] = useState<Json>(null);
  const [offer, setOffer] = useState<Json>(null);
  const [choice, setChoice] = useState<string>("");
  const [name, setName] = useState<string>("");
  const [message, setMessage] = useState<string>("");
  const [model, setModel] = useState<string>("");
  const [modelProvider, setModelProvider] = useState<string>("");

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
    const t = setInterval(() => invoke("host_status").then(setHost), 1000);
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
        <p>Choose a model and a provider from your Codex configuration for this thread.</p>
        <p>
          <button onClick={() => act("thread_start", { model, modelProvider })} disabled={host?.state !== "ready" || !model.trim() || !modelProvider.trim()}>Start thread</button>{" "}
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
