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

/** One read of the fixed fleet folder, with no caller-supplied path or selection. */
export function readFleetPacket(invoke: (command: string) => Promise<FleetPacket>): Promise<FleetPacket> {
  return invoke("read_fleet_records");
}

/** The source records behind the derived views: counts, store state, native
 * links and recording outcomes, source limits and the complete packet. */
export function FleetSourceRecords({ packet }: { packet: FleetPacket }) {
  return <section aria-label="Fleet source records">
    <p>Project: {packet.project.canonicalRoot}</p>
    <p>{packet.briefs.length} brief record(s), {packet.graphs.length} graph revision(s), {packet.coordination.projectRecords.length} entries from the project log.</p>
    <p>Store source: {packet.coordination.protected.state}. {packet.coordination.governingStoreRecords.length} record(s) in governing store order; {packet.coordination.appObservations.length} protected App observation(s) in protected-store order.</p>
    <p>This is a file snapshot. Claimed recorders and source lines stay with each record.</p>
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
  </section>;
}

const reference = (ref: Json) => <>{ref.kind}: <code>{ref.ref}</code>{ref.contentIdentity ? <> (content {ref.contentIdentity.method} {ref.contentIdentity.value})</> : null}</>;

/** Each undertaking's selected work, with state and causes, and its
 * return-review queue, as the read packet gives them. */
export function FleetWorkspace({ workspace }: { workspace: NonNullable<FleetPacket["workspace"]> }) {
  return <div aria-label="Fleet coordination workspace">
    <p>{workspace.standing}</p>
    {workspace.undertakings.length === 0 && <p>No undertaking graph or selector was read. No conclusion about absent work follows. Delegated work appears here once an undertaking's records are in the project's <code>.chirality/fleet/</code> folder.</p>}
    {workspace.undertakings.map(view => <section key={view.undertaking} aria-label={`Undertaking ${view.undertaking}`}>
      <h3>Undertaking {view.undertaking}</h3>
      {view.graph ? <p>{view.currentGraphEstablished ? "Current graph" : <><strong>Limit:</strong> Last readable graph; currentness unknown</>}: {view.graph}, revision {view.revision}.</p>
        : <p><strong>Limit:</strong> No current graph established. Returns and waiting work cannot be reconstructed for this undertaking.</p>}
      {view.notes.length > 0 && <ul>{view.notes.map((note: string, i: number) => <li key={i}>{note}</li>)}</ul>}
      <h4>Selected work and waiting causes</h4>
      {view.waiting.length === 0 && <p>No selected work item is shown for this undertaking.</p>}
      <ul>{view.waiting.map((row: Json) => <li key={row.item}>
        <p><b>{row.item}: {row.outcome}</b> — <strong>{row.category}</strong></p>
        <p>Owner: {row.owner}. Next: {row.next ? (typeof row.next === "string" ? row.next : JSON.stringify(row.next)) : "not stated in the records"}.</p>
        {row.causes.length > 0 ? <><p>Causes the records give:</p><ul>{row.causes.map((cause: string, i: number) => <li key={i}>{cause}</li>)}</ul></>
          : <p>The records give no cause.</p>}
        <details><summary>Work evidence, needs and sources</summary><pre>{JSON.stringify({needs: row.needs, writeScope: row.writeScope, sources: row.sources}, null, 2)}</pre></details>
      </li>)}</ul>
      <h4>Return-review queue {view.queueComplete ? "(complete for the read packet)" : "(incomplete)"}</h4>
      {!view.queueComplete && <p><strong>Limit:</strong> Not every record was read or established, so this queue may not be the whole.</p>}
      {view.queue.length === 0 && <p>{view.queueComplete ? "No recorded returns await review or integration in this graph." : "No readable queued return shown; more work may be unrecorded or unread."}</p>}
      <ul>{view.queue.map((row: Json) => <li key={row.returnRef}>
        <p><b>{row.item}: {row.outcome}</b> — {row.state}</p>
        <p>Return: {row.returnRef}. Returned by {row.returnedBy}; recorded by {row.recordedBy}. Who examines: {row.examines}.
          {row.examiner ? ` Recorded reviewer: ${row.examiner}.` : " No review recorded."}</p>
        {row.examinesProvenance && <p>Brief preparer source: {row.examinesProvenance.basis === "return-brief"
          ? `return's named brief ${row.examinesProvenance.briefId}.`
          : row.examinesProvenance.briefId
            ? `${view.currentGraphEstablished ? "current" : "last readable"} graph's brief ${row.examinesProvenance.briefId}${view.currentGraphEstablished ? "" : " (currentness unknown)"}; return does not name a brief.`
            : `return does not name a brief; ${view.currentGraphEstablished ? "current" : "last readable"} graph has no brief for this item${view.currentGraphEstablished ? "" : " (currentness unknown)"}.`}
          {row.examinesProvenance.briefId && !row.examinesProvenance.briefSource ? " No preparer established from the named brief." : ""}</p>}
        <p>Returned:</p>
        <ul>{(row.returned ?? []).map((ref: Json, i: number) => <li key={i}>{reference(ref)}</li>)}</ul>
        <details><summary>Return evidence and sources</summary><pre>{JSON.stringify({evidence: row.evidence, sources: row.sources, examinesProvenance: row.examinesProvenance}, null, 2)}</pre></details>
      </li>)}</ul>
    </section>)}
    <details><summary>Reconstruction limits</summary><ul>{workspace.limits.map((limit, i) => <li key={i}>{limit}</li>)}</ul></details>
  </div>;
}
