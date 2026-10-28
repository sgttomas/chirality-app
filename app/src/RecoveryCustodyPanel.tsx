import { useEffect, useRef, useState } from "react";
type Json = any;
const text = (value: Json) => value == null ? "not established" : typeof value === "string" ? value : JSON.stringify(value);
const detail = (value: Json) => <pre style={{ whiteSpace: "pre-wrap", overflowWrap: "anywhere" }}>{JSON.stringify(value, null, 2)}</pre>;

export function RecoveryCustodyDetails({ data, retry }: { data: Json; retry?: (threadId: string) => void }) {
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
      {row.state === "recovering" && <p>Recovering: the App is reading this conversation from Codex history.</p>}
      {row.state === "recovery-pending" && <p>Recovering when Codex is ready: the App reads this conversation from Codex history then.</p>}
      {row.state === "unavailable" && <p role="status">Earlier events unavailable: {text(row.unavailableReason)}.{" "}
        {retry && <button onClick={() => retry(row.threadId)}>Read this conversation from Codex again</button>}</p>}
      <details><summary>Original open item pointers</summary>{detail(row.openItems)}</details>
    </article>)}
    <h3>Loss and recovery events observed in this App process</h3>
    <p>A source event is separate from whether its pointer facts reached durable storage. A recovery event reports what Codex history said when the App read it after a restart; the App sent Codex only those history reads, resumed nothing and sent nothing to the conversation.</p>
    {(custody.live?.events ?? []).map((event: Json, i: number) => <details key={event.eventId ?? i}><summary>{event.kind}: {event.cause ?? event.priorEvents ?? event.outcome} · {text(event.generation ?? event.threadId)}</summary>{detail(event)}</details>)}
    <h3>Restart observations derived from persisted prior-session facts</h3>
    {(custody.restartEvents ?? []).length === 0 && <p>No restart interruption is established by the available persisted facts.</p>}
    {(custody.restartEvents ?? []).map((event: Json, i: number) => <details key={event.eventId ?? i}><summary>{event.kind}: home {event.home}, thread {event.threadId}, prior session {event.priorSession}</summary>{detail(event)}</details>)}
    <h3>Requests ended unanswered after an App restart</h3>
    <p>These are recorded endings of earlier requests. They cannot be answered in this App session.</p>
    {(custody.requestEndEvents ?? []).map((event: Json, i: number) => <details key={event.eventId ?? i}><summary>Ended unanswered: {event.entry.method} · {text(event.entry.subject?.threadId)} · recorded {event.at}</summary>{detail(event)}</details>)}
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

export function RecoveryRequestHistory({ modeHomeClass, generation, read }: { modeHomeClass?: string; generation: Json; read: (cursor: Json) => Promise<Json> }) {
  const [data, setData] = useState<Json>(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const active = useRef(true);
  const pending = useRef(false);
  useEffect(() => { active.current = true; return () => { active.current = false; }; }, []);
  const load = async (cursor: Json) => {
    if (pending.current) return;
    pending.current = true;
    setBusy(true); setError(""); setData(null);
    try {
      const result = await read(cursor);
      if (!active.current) return;
      if (result.source.modeHomeClass !== modeHomeClass || JSON.stringify(result.source.generation) !== JSON.stringify(generation)) throw new Error("Request history belongs to a different source; refresh the selected home.");
      setData(result);
    } catch (e) { if (active.current) setError(String(e)); }
    finally { pending.current = false; if (active.current) setBusy(false); }
  };
  return <section aria-label="Persisted terminal request summaries">
    <h3>Persisted terminal request summaries</h3>
    <p>Historical App pointer metadata only. These are not current requests and cannot be answered here. Original source homes and generations remain separate from the selected home; project association is not inferred.</p>
    <button disabled={busy || !modeHomeClass} onClick={() => load(null)}>Read latest request summaries</button>
    {error && <p role="alert">{error}</p>}
    {data && <>
      <p>Read at {data.readAt}. {data.readStanding}</p>
      <p>{data.page.coverage}. Ledger cut: {data.page.throughSequence}; this page: {data.page.entries.length} summaries; row bound: {data.page.rowLimit}.</p>
      <p>{data.page.standing}</p>
      <p>Pending pointer facts excluded from this persisted page: {text(data.page.pendingPointerFacts)}.</p>
      {data.page.persistenceLimit && <p role="status">Persistence limit: {text(data.page.persistenceLimit)}</p>}
      {data.page.entries.length === 0 && <p>No terminal summaries on this page. This says nothing about current unanswered requests.</p>}
      {data.page.entries.map((entry: Json, i: number) => {
        const summary = entry.summary;
        return <details key={JSON.stringify([summary.generation, summary.requestIdentity]) + i}>
          <summary>{text(summary.endedAs)}: {summary.method} · request {summary.requestIdentity}{entry.requestIdentityType === "legacy-unknown" ? " (legacy type unknown)" : ""} · recorded {summary.at}</summary>
          <p>Source home: {text(entry.sourceGeneration?.home)}; source App session: {text(entry.sourceGeneration?.appSession)}; spawn: {text(entry.sourceGeneration?.spawnCounter)}.</p>
          <p>Transition: {summary.transition}; context: {text(summary.context)}; reply write: {summary.replyWrite}; acknowledgment: {summary.acknowledgment}.</p>
          <p>{entry.projectAssociation}</p>
          {detail(entry)}
        </details>;
      })}
      {data.page.nextCursor ? <button disabled={busy} onClick={() => load(data.page.nextCursor)}>Read earlier request summaries</button> : <p>No earlier terminal summaries at this ledger cut.</p>}
    </>}
  </section>;
}

export function RecoveryCustodyPanel({ modeHomeClass, generation, nativeHistoryGeneration, read, readRequests, retry }: { modeHomeClass?: string; generation: Json; nativeHistoryGeneration: Json; read: () => Promise<Json>; readRequests?: (cursor: Json) => Promise<Json>; retry?: (threadId: string) => Promise<Json> }) {
  const [data, setData] = useState<Json>(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const run = async (operation: () => Promise<Json>) => {
    setBusy(true); setError("");
    try {
      const result = await operation();
      if (result.source.modeHomeClass !== modeHomeClass || JSON.stringify(result.source.generation) !== JSON.stringify(generation)) throw new Error("Recovery result belongs to a different source; refresh the selected home.");
      setData(result);
    } catch (e) { setError(String(e)); }
    finally { setBusy(false); }
  };
  const refresh = () => run(read);
  return <section aria-labelledby="recovery-custody-heading">
    <h2 id="recovery-custody-heading">App recovery pointer observations</h2>
    <p>Selected home: {modeHomeClass ?? "not established"}. Source generation: {text(generation)}. Native History's separately selected generation: {text(nativeHistoryGeneration)}.</p>
    <button disabled={busy || !modeHomeClass} onClick={refresh}>Read recovery metadata for this home</button>
    <p>This explicit read does not flush pending facts, contact Codex, resume a conversation, or record a human act or external operation. Use the existing Native History controls separately.</p>
    {readRequests && <RecoveryRequestHistory key={JSON.stringify([modeHomeClass, generation])} modeHomeClass={modeHomeClass} generation={generation} read={readRequests} />}
    {error && <p role="alert">{error}</p>}
    {data ? <RecoveryCustodyDetails data={data} retry={retry && !busy ? (threadId) => run(() => retry(threadId)) : undefined} /> : <p>Not read for this selection. Missing data is not evidence of completed work.</p>}
  </section>;
}
