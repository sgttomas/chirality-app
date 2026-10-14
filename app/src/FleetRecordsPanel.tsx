type Json = any;
export type FleetPacket = {
  format: string; formatVersion: string; standing: string;
  project: { canonicalRoot: string };
  briefs: Json[]; graphs: Json[];
  coordination: { projectRecords: Json[]; governingStoreRecords: Json[]; appObservations: Json[]; nativeRelationships?: Json[]; recordingEvents?: Json[]; protected: { state: string } };
  limits: { source: { home?: string; path?: string; line?: number }; reason: string }[];
  nativeRecording: string;
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
      <p>This is a file snapshot. Claimed recorders and source lines stay with each record. No work state or current graph is selected here.</p>
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
      <details open><summary>Complete fleet packet, sources and provenance</summary><pre>{JSON.stringify(packet, null, 2)}</pre></details>
    </>}
  </section>;
}
