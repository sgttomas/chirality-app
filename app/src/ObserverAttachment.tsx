import { useEffect, useRef, useState } from "react";
import { invoke } from "@tauri-apps/api/core";

type Json = any; // eslint-disable-line @typescript-eslint/no-explicit-any
type Observe = (source: Json, cursor: Json, after: number) => Promise<Json>;
const nativeObserve: Observe = (sourceGeneration, generation, after) => invoke("host_observe", { sourceGeneration, generation, after });
const position = (value: unknown): value is number => Number.isSafeInteger(value) && (value as number) >= 0;
const historyLimit = (limit: unknown): string => {
  switch (limit) {
    case "supplier-history-error": return "Codex could not read this conversation’s history.";
    case "invalid-native-history-response": return "The Codex reply could not be read as history.";
    case "metadata-thread-mismatch": return "Codex returned a different conversation; those results were not used.";
    case "original-source-no-longer-ready": return "The original Codex source changed or stopped before this read finished.";
    case "target-no-longer-loaded": return "This conversation was no longer loaded when history was read.";
    case "history-result-not-observed": return "No history result was observed before waiting ended.";
    case "history-request-not-written": return "The history request was not written to Codex.";
    default: return "This history read was unavailable. Current activity is received separately.";
  }
};

// This cursor belongs to this window only. The Rust projection and private
// receipts retain their own custody; neither is acknowledged by this reader.
export function ObserverAttachment({ host, observe = nativeObserve }: { host: Json; observe?: Observe }) {
  const source = host?.generation;
  const scope = JSON.stringify(source ?? null);
  const home = JSON.stringify([source?.appSession, source?.home]);
  const retention = host?.observerRetention;
  const high = retention?.deliveredThrough;
  const floor = retention?.omittedThrough;
  const ready = host?.state === "ready" && host?.generationClosed !== true;
  const cursors = useRef(new Map<string, { generation: Json; position: number }>());
  const pending = useRef(new Set<string>());
  const attempted = useRef(new Map<string, string>());
  const current = useRef(scope);
  current.current = scope;
  const alive = useRef(true);
  const [cursorRevision, setCursorRevision] = useState(0);
  const [attachment, setAttachment] = useState<{ scope: string; status: string; gap?: boolean; limit?: string }>({ scope, status: "waiting" });
  useEffect(() => { alive.current = true; return () => { alive.current = false; }; }, []);
  useEffect(() => {
    if (!ready) {
      setAttachment({ scope, status: "waiting" });
      return;
    }
    if (!source?.appSession || !source?.home || !position(source?.spawnCounter) || source.spawnCounter === 0 ||
      JSON.stringify(retention?.generation) !== scope || !position(high) || !position(floor) || floor > high) {
      setAttachment({ scope, status: "unavailable", limit: "Window replay coverage is unavailable; refresh the current source." });
      return;
    }
    const saved = cursors.current.get(home);
    const cursor = saved && JSON.stringify(saved.generation) === scope ? saved : undefined;
    if (cursor && floor <= cursor.position) {
      // The received status already contains the Host's current projection and
      // retained replay. Avoid transferring the same complete snapshot twice.
      // An actual scoped reply can be newer than the last polled status. Keep
      // that trusted same-generation cursor until status catches up.
      if (cursor.position <= high) cursors.current.set(home, { generation: source, position: high });
      setAttachment(previous => previous.scope === scope && previous.status !== "waiting" ? previous : { scope, status: "attached", gap: false });
      return;
    }
    const attempt = JSON.stringify([scope, floor, cursor?.position ?? null]);
    if (pending.current.has(scope) || attempted.current.get(home) === attempt) return;
    attempted.current.set(home, attempt);
    pending.current.add(scope);
    setAttachment({ scope, status: "attaching" });
    void observe(source, cursor?.generation ?? null, cursor?.position ?? 0).then(result => {
      // Release before publishing cursor state: its render may already need a
      // new attachment if replay expired while this reply was in flight.
      pending.current.delete(scope);
      if (!alive.current || current.current !== scope) {
        if (attempted.current.get(home) === attempt) attempted.current.delete(home);
        return;
      }
      if (result?.sourceUnavailable || result?.error || JSON.stringify(result?.generation) !== scope || !position(result?.position)) {
        setAttachment({ scope, status: "unavailable", limit: "The source changed or window attachment was unavailable; refresh the current source." });
        return;
      }
      cursors.current.set(home, { generation: source, position: result.position });
      setAttachment({ scope, status: "attached", gap: result.gap === true });
      setCursorRevision(revision => revision + 1);
    }).catch(() => {
      pending.current.delete(scope);
      if (!alive.current || current.current !== scope) {
        if (attempted.current.get(home) === attempt) attempted.current.delete(home);
        return;
      }
      setAttachment({ scope, status: "unavailable", limit: "Window attachment could not be read; current native activity remains separately received." });
    });
  }, [scope, ready, high, floor, observe, cursorRevision]); // full source identity is scope

  const shown: typeof attachment = ready && attachment.scope === scope ? attachment : { scope, status: "waiting" };
  const rebuild = host?.observerRebuild;
  const matchingRebuild = JSON.stringify(rebuild?.generation) === scope;
  const targets: Json[] = matchingRebuild && Array.isArray(rebuild?.targets) ? rebuild.targets : [];
  return <section aria-label="Window reattachment">
    <h3>Window reattachment</h3>
    {shown.status === "waiting" && <p>Window replay waits for a ready Codex source. The latest App observations remain available.</p>}
    {shown.status === "attaching" && <p>Attaching this window to current observations…</p>}
    {shown.status === "unavailable" && <p role="alert">{shown.limit}</p>}
    {shown.status === "attached" && <p>{shown.gap ? "Earlier events are outside this window’s replay. Codex history reconstruction is shown separately below." : "Window replay is current."}</p>}
    {matchingRebuild && (targets.length > 0 || rebuild?.noKnownTargets) && <div>
      <p>History reconstruction: {rebuild.status}. Metadata and the latest turn-summary page can be read here. Earlier pages and item pages are not loaded; this is partial history, and checklist revisions are not reconstructed.</p>
      {rebuild.noKnownTargets && <p>No loaded conversations were available for this history read.</p>}
      {targets.map(target => <article key={target.threadId}>
        <h4>Recovered history · {target.threadId}</h4>
        <p>{target.status}{target.readAt ? ` · read ${target.readAt}` : ""}. This history does not establish current activity.</p>
        {target.limit && <p>{historyLimit(target.limit)}</p>}
        {target.metadata?.thread && <p>Conversation: {target.metadata.thread.id}{target.metadata.thread.preview ? ` · ${target.metadata.thread.preview}` : ""}</p>}
        {Array.isArray(target.turns?.data) && <ul>{target.turns.data.map((turn: Json) => <li key={turn.id}>Turn {turn.id} · {turn.status ?? "status unavailable"} · recovered from Codex</li>)}</ul>}
        {target.turns && <p>{Object.hasOwn(target.turns, "nextCursor") ? target.turns.nextCursor === null ? "No further turn-summary cursor was returned. Item history remains unloaded." : "Earlier turn summaries remain available in stored history." : "Turn-summary pagination coverage was not reported."}</p>}
      </article>)}
    </div>}
  </section>;
}
