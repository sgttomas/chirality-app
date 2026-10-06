import { useState } from "react";
type Json = any;
const text = (value: Json) => value == null ? "not established" : typeof value === "string" ? value : JSON.stringify(value);
const detail = (value: Json) => <pre style={{ whiteSpace: "pre-wrap", overflowWrap: "anywhere" }}>{JSON.stringify(value, null, 2)}</pre>;

export function RecoveryCustodyDetails({ data }: { data: Json }) {
  const custody = data.custody;
  return <>
    <p>Read at {data.readAt}. Source home: {data.source.modeHomeClass}; App session: {text(data.source.appSession)}; generation: {text(data.source.generation)}.</p>
    <p>{data.readStanding}</p><p>{custody.standing}</p>
    <p>Automatic resume: {custody.automaticResume === false ? "off; no resume was requested" : "not established"}.</p>
    <h3>Pending persistence</h3>
    <p>Unpersisted pointer facts in this Host's queue: {text(custody.pendingPointerFacts)}. Live observations are not proof of durable recording.</p>
    {(custody.limits ?? []).map((limit: string, i: number) => <p role="status" key={i}>{limit}</p>)}
    <h3>Live and retained in-memory pointer observations</h3>
    <p>These are the App's observations, including loss of observation. They do not establish that a turn is currently running.</p>
    {(custody.live?.limits ?? []).map((limit: string, i: number) => <p key={i}>{limit}</p>)}
    {(custody.live?.observations ?? []).map((row: Json, i: number) => <article key={i}>
      <p>Thread {row.threadId}; source generation {text(row.generation)}; observed state {row.state}.</p>
      <p>Observed live-turn pointer: {text(row.liveTurn)}. Index: {row.indexKnown ? "known to the source" : "not known; memory-only observation, cold lookup unavailable"}.</p>
      <p>{row.standing}</p>
      <details><summary>Original open item pointers</summary>{detail(row.openItems)}</details>
    </article>)}
    <h3>Loss events observed in this App process</h3>
    <p>A source event is separate from whether its pointer facts reached durable storage.</p>
    {(custody.live?.events ?? []).map((event: Json, i: number) => <details key={event.eventId ?? i}><summary>{event.kind}: {event.cause} · {text(event.generation)}</summary>{detail(event)}</details>)}
    <h3>Restart observations derived from persisted prior-session facts</h3>
    {(custody.restartEvents ?? []).length === 0 && <p>No restart interruption is established by the available persisted facts.</p>}
    {(custody.restartEvents ?? []).map((event: Json, i: number) => <details key={event.eventId ?? i}><summary>{event.kind}: home {event.home}, thread {event.threadId}, prior session {event.priorSession}</summary>{detail(event)}</details>)}
    <h3>Persisted conversation pointer history</h3>
    <p>{data.historicalScope}</p>
    {(custody.historicalConversations ?? []).map((row: Json, i: number) => <article key={i}>
      <h4>Home {row.index.home} · thread {row.index.threadId}</h4>
      <p>{row.standing}</p>
      <p>Execution source generation: {text(row.executionGeneration)}. Last observed state: {text(row.index.lastObservedExecution?.state)}; live-turn pointer: {text(row.index.lastObservedExecution?.liveTurn)}.</p>
      <p>Execution index project: {text(row.index.project)}; observation session: {text(row.index.session)}. Latest metadata append session: {text(row.metadataIndex?.session)}; metadata project: {text(row.metadataIndex?.project)}.</p>
      <p>{row.openItemCorrelation}</p>
      {(row.openItemAssociations ?? []).map((item: Json, j: number) => <div key={j}>
        <p>Item {item.itemId} ({item.itemType}); turn {item.turnId == null ? "unknown — absent from this historical row" : item.turnId}; {item.correlation}.</p>
        <p>{item.standing}</p>
        <details><summary>Original item association and full tuple</summary>{detail(item)}</details>
      </div>)}
      <details><summary>Execution index and latest metadata index (separate originals)</summary>{detail({ executionGeneration: row.executionGeneration, index: row.index, metadataIndex: row.metadataIndex })}</details>
      <p>Native history: {row.nativeHistory}</p>
    </article>)}
    <p>{data.nativeHistory}</p><p>{data.compatibility}</p>
  </>;
}

export function RecoveryCustodyPanel({ modeHomeClass, generation, nativeHistoryGeneration, read }: { modeHomeClass?: string; generation: Json; nativeHistoryGeneration: Json; read: () => Promise<Json> }) {
  const [data, setData] = useState<Json>(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const refresh = async () => {
    setBusy(true); setError("");
    try {
      const result = await read();
      if (result.source.modeHomeClass !== modeHomeClass || JSON.stringify(result.source.generation) !== JSON.stringify(generation)) throw new Error("Recovery result belongs to a different source; refresh the selected home.");
      setData(result);
    } catch (e) { setError(String(e)); }
    finally { setBusy(false); }
  };
  return <section aria-labelledby="recovery-custody-heading">
    <h2 id="recovery-custody-heading">App recovery pointer observations</h2>
    <p>Selected home: {modeHomeClass ?? "not established"}. Source generation: {text(generation)}. Native History's separately selected generation: {text(nativeHistoryGeneration)}.</p>
    <button disabled={busy || !modeHomeClass} onClick={refresh}>Read recovery metadata for this home</button>
    <p>This explicit read does not flush pending facts, contact Codex, resume a conversation, or record a human act or external operation. Use the existing Native History controls separately.</p>
    {error && <p role="alert">{error}</p>}
    {data ? <RecoveryCustodyDetails data={data} /> : <p>Not read for this selection. Missing data is not evidence of completed work.</p>}
  </section>;
}
