type Json = any;
export type FleetPacket = {
  format: string; formatVersion: string; standing: string;
  project: { canonicalRoot: string };
  briefs: Json[]; graphs: Json[];
  coordination: { projectRecords: Json[]; governingStoreRecords: Json[]; appObservations: Json[]; nativeRelationships?: Json[]; recordingEvents?: Json[]; protected: { state: string } };
  limits: { source: { home?: string; path?: string; line?: number }; reason: string }[];
  nativeRecording: string;
  workspace?: { standing: string; graphIdentityMethod: string; undertakings: Json[]; limits: string[] };
};

/** One explicit manual read, with no caller-supplied path or selection. */
export function readFleetPacket(invoke: (command: string) => Promise<FleetPacket>): Promise<FleetPacket> {
  return invoke("read_fleet_records");
}

export function FleetRecordsPanel({ packet, error, busy, refresh }: {
  packet: FleetPacket | null; error: string; busy: boolean; refresh: () => void;
}) {
  return <section aria-label="Fleet source records">
    <h3>Fleet source records</h3>
    <p><button onClick={refresh} disabled={busy}>{busy ? "Reading fleet records…" : "Refresh fleet records"}</button></p>
    {!packet && !error && <p>Read the saved fleet packet in this project's fixed fleet folder.</p>}
    {error && <p role="alert">Fleet read failed: {error}</p>}
    {packet && <>
      <p>Project: {packet.project.canonicalRoot}</p>
      <p>{packet.briefs.length} brief record(s), {packet.graphs.length} graph revision(s), {packet.coordination.projectRecords.length} entries from the project log.</p>
      <p>Store source: {packet.coordination.protected.state}. {packet.coordination.governingStoreRecords.length} record(s) in governing store order; {packet.coordination.appObservations.length} protected App observation(s) in protected-store order.</p>
      <p>This is a file snapshot. Claimed recorders and source lines stay with each record.</p>
      {packet.workspace && <FleetWorkspace workspace={packet.workspace} />}
      <p>{packet.nativeRecording}</p>
      {(packet.coordination.nativeRelationships?.length ?? 0) > 0 && <div aria-label="Recorded native conversation links">
        <h4>Recorded native conversation links</h4>
        <ul>{packet.coordination.nativeRelationships!.map((row, index) => <li key={index}>
          {row.record.body.thread.threadId} {row.record.body.relation} {row.record.body.source.threadId}, home {row.record.body.nativeHome.homeId} (store order {row.storeOrder}). Source and request context are retained below; this historical file does not activate a conversation.
        </li>)}</ul>
      </div>}
      {(packet.coordination.recordingEvents?.length ?? 0) > 0 && <div aria-label="Native link recording outcomes">
        <h4>Native link recording outcomes</h4>
        <ul>{packet.coordination.recordingEvents!.map((row, index) => <li key={index}>
          {row.record.kind}: {row.record.body.originalObservationId}, {row.record.body.phase}: {row.record.body.statement}
        </li>)}</ul>
      </div>}
      {packet.limits.length > 0 && <div role="alert"><p>Source and relationship limits:</p><ul>{packet.limits.map((limit, index) => <li key={index}>
        {limit.source.home}{limit.source.path ? `: ${limit.source.path}` : ""}{limit.source.line ? ` (line ${limit.source.line})` : ""}: {limit.reason}
      </li>)}</ul></div>}
      <details><summary>Complete fleet packet, sources and provenance</summary><pre>{JSON.stringify(packet, null, 2)}</pre></details>
    </>}
  </section>;
}

function FleetWorkspace({ workspace }: { workspace: NonNullable<FleetPacket["workspace"]> }) {
  return <div aria-label="Fleet coordination workspace">
    <h4>Returns and waiting work</h4>
    <p>{workspace.standing}</p>
    {workspace.undertakings.length === 0 && <p>No undertaking graph or selector was read. No conclusion about absent work follows.</p>}
    {workspace.undertakings.map(view => <section key={view.undertaking} aria-label={`Undertaking ${view.undertaking}`}>
      <h4>{view.undertaking}</h4>
      {view.graph ? <p>{view.currentGraphEstablished ? "Current graph" : "Last readable graph; currentness unknown"}: {view.graph}, revision {view.revision}.</p>
        : <p>No current graph established. Returns and waiting work cannot be reconstructed for this undertaking.</p>}
      {view.notes.length > 0 && <ul>{view.notes.map((note: string, i: number) => <li key={i}>{note}</li>)}</ul>}
      <h5>Return-review queue {view.queueComplete ? "(complete for the read packet)" : "(incomplete)"}</h5>
      {view.queue.length === 0 && <p>{view.queueComplete ? "No recorded returns await review or integration in this graph." : "No readable queued return shown; more work may be unrecorded or unread."}</p>}
      <ul>{view.queue.map((row: Json) => <li key={row.returnRef}>
        <b>{row.item}: {row.outcome}</b> — {row.state}
        <p>Returned by {row.returnedBy}; recorded by {row.recordedBy}. Who examines: {row.examines}.
          {row.examiner ? ` Recorded reviewer: ${row.examiner}.` : " No review recorded."}</p>
        {row.examinesProvenance && <p>Brief preparer source: {row.examinesProvenance.basis === "return-brief"
          ? `return's named brief ${row.examinesProvenance.briefId}.`
          : row.examinesProvenance.briefId
            ? `${view.currentGraphEstablished ? "current" : "last readable"} graph's brief ${row.examinesProvenance.briefId}${view.currentGraphEstablished ? "" : " (currentness unknown)"}; return does not name a brief.`
            : `return does not name a brief; ${view.currentGraphEstablished ? "current" : "last readable"} graph has no brief for this item${view.currentGraphEstablished ? "" : " (currentness unknown)"}.`}
          {row.examinesProvenance.briefId && !row.examinesProvenance.briefSource ? " No preparer established from the named brief." : ""}</p>}
        <p>Return: {row.returnRef}. Returned references: {row.returned.map((ref: Json) => ref.ref).join(", ")}.</p>
        <details><summary>Return evidence and sources</summary><pre>{JSON.stringify({evidence: row.evidence, sources: row.sources, examinesProvenance: row.examinesProvenance}, null, 2)}</pre></details>
      </li>)}</ul>
      <h5>Selected work and waiting causes</h5>
      <ul>{view.waiting.map((row: Json) => <li key={row.item}>
        <b>{row.item}: {row.outcome}</b> — <strong>{row.category}</strong>
        <p>Owner: {row.owner}{row.next ? `. Next: ${typeof row.next === "string" ? row.next : JSON.stringify(row.next)}` : ""}</p>
        <ul>{row.causes.map((cause: string, i: number) => <li key={i}>{cause}</li>)}</ul>
        <details><summary>Work evidence, needs and sources</summary><pre>{JSON.stringify({needs: row.needs, writeScope: row.writeScope, sources: row.sources}, null, 2)}</pre></details>
      </li>)}</ul>
    </section>)}
    <details><summary>Reconstruction limits</summary><ul>{workspace.limits.map((limit, i) => <li key={i}>{limit}</li>)}</ul></details>
  </div>;
}
