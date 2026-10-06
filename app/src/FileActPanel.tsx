import { useState } from "react";
type Json = any;
export function FileActPanel({ command }: { command: (name: string, args: Record<string, unknown>) => Promise<Json> }) {
  const [kind, setKind] = useState("A4");
  const [scope, setScope] = useState("");
  const [purpose, setPurpose] = useState("");
  const [preview, setPreview] = useState<Json>(null);
  const [view, setView] = useState<Json>(null);
  const [outcomes, setOutcomes] = useState<Record<string, Json>>({});
  const [selectionStatus, setSelectionStatus] = useState<Json>(null);
  const [busy, setBusy] = useState(false);
  const [attempts, setAttempts] = useState<Record<string, boolean>>({});
  const status = preview ? outcomes[preview.reference] : selectionStatus;
  const attempted = preview ? attempts[preview.reference] === true : false;
  const [error, setError] = useState("");
  const run = async (name: string, args: Record<string, unknown>) => {
    setBusy(true); setError("");
    try {
      const result = await command(name, args);
      if (name === "file_act_select") {
        setPreview(result.reference ? result : null); setSelectionStatus(result.reference ? null : result);
      } else if (name === "file_act_read") setView(result);
      else {
        const reference = String(args.reference);
        setOutcomes(old => ({ ...old, [reference]: result }));
        setAttempts(old => ({ ...old, [reference]: true }));
      }
    } catch (e) { setError(String(e)); }
    finally { setBusy(false); }
  };
  return <section id="file-acts" aria-labelledby="file-act-heading">
    <h2 id="file-act-heading">App file acts and act log</h2>
    <p>Open a standing act on one workspace file or saved output. No arrival or request is associated. This facility answers no supplier request.</p>
    <label>Kind <select disabled={busy} value={kind} onChange={e => setKind(e.target.value)}>
      <option value="A4">mark checked</option><option value="A6">approve (engineering approval)</option><option value="A7">rely (professional reliance)</option>
    </select></label>{" "}
    <label>Scope <input disabled={busy} value={scope} onChange={e => setScope(e.target.value)} /></label>{" "}
    <label>Purpose <input disabled={busy} value={purpose} onChange={e => setPurpose(e.target.value)} /></label>
    <button disabled={busy || !scope.trim() || !purpose.trim()} onClick={() => run("file_act_select", { kind, scope, purpose })}>Select file and freeze preview…</button>
    <button disabled={busy} onClick={() => run("file_act_read", {})}>Read file-act log and current content</button>
    {preview && <article>
      <h3>Frozen offer: {preview.offer.wording}</h3>
      <p>Subject: {preview.offer.subject.ref} · {preview.byteLength} bytes</p>
      <p>Scope: {preview.offer.scope} · Purpose: {preview.offer.purpose}</p>
      <p>Actor requirement: {preview.offer.actorRequirement}. Identity not verified. A7 professional standing is the person's own statement; no certification is established.</p>
      <p>{preview.previewStanding}. Changes to the kind, scope or purpose fields above require selecting and reviewing a new offer.</p>
      <pre style={{ whiteSpace: "pre-wrap", overflowWrap: "anywhere" }}>{JSON.stringify(preview.offer, null, 2)}</pre>
      {preview.utf8 !== null && <details open><summary>Exact frozen UTF-8 text</summary><pre style={{ whiteSpace: "pre-wrap", overflowWrap: "anywhere", maxHeight: 360, overflow: "auto" }}>{preview.utf8}</pre></details>}
      <details><summary>Exact frozen bytes (hexadecimal)</summary><pre style={{ whiteSpace: "pre-wrap", overflowWrap: "anywhere", maxHeight: 360, overflow: "auto" }}>{preview.hex}</pre></details>
      <button disabled={busy || attempted} onClick={() => run("file_act_confirm", { reference: preview.reference })}>Review native act / decline / cancel…</button>
      <button disabled={busy || attempted} onClick={() => run("file_act_dismiss", { reference: preview.reference })}>Dismiss offer without capture</button>
    </article>}
    {error && <p role="alert">{error}</p>}
    {status && <div role="status"><p>{status.state}</p><pre>{JSON.stringify(status, null, 2)}</pre></div>}
    <p>Uncertain capture publication is neither a recorded act nor an act awaiting its record. A definite capture failure requires a new review and confirmation. A durable capture with a failed record remains missing in record until its original continuation succeeds.</p>
    {(view?.hotOffers ?? []).map((offer: Json) => <article key={offer.reference}>
      <p>Original offer {offer.reference}: {outcomes[offer.reference]?.state ?? offer.status?.state ?? offer.state}</p>
      <pre>{JSON.stringify(outcomes[offer.reference] ?? offer.status, null, 2)}</pre>
      {(offer.status?.capture || offer.status?.captureId) && <button disabled={busy} onClick={() => run("file_act_continue", { reference: offer.reference })}>Continue original capture/record only</button>}
    </article>)}
    {preview && (status?.capture || status?.captureId) && <button disabled={busy} onClick={() => run("file_act_continue", { reference: preview.reference })}>Continue this original capture/record only</button>}
    <p>{view?.standing}</p>
    {(view?.rows ?? []).map((row: Json, index: number) => <article key={`${row.recordId}-${index}`}>
      <h3>{row.kind}: {row.event}</h3>
      <p>Subject: {row.subject} · Scope: {row.scope ?? "unavailable"} · Purpose: {row.purpose ?? "unavailable"}</p>
      <p>Actor (identity not verified): {JSON.stringify(row.actor)}. Recorder: {JSON.stringify(row.recordedBy)}.</p>
      <p>{row.comparison}. Captured at: {row.captureTime}. {row.identityResolution}.</p>
      {row.limits.map((limit: string, i: number) => <p key={i}>{limit}</p>)}
      <details><summary>Source, content identities and correction relations</summary><pre>{JSON.stringify(row, null, 2)}</pre></details>
    </article>)}
    <details><summary>Read limits and correction groups</summary><pre>{JSON.stringify({ limits: view?.limits, diagnostics: view?.diagnostics, correctionGroups: view?.correctionGroups }, null, 2)}</pre></details>
  </section>;
}
