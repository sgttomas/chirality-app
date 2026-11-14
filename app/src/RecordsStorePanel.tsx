import { useRef, useState } from "react";
import { REFRESH_FAILED } from "./statusRefresh";

type Json = any; // eslint-disable-line @typescript-eslint/no-explicit-any
type Act = (command: string, args?: Record<string, unknown>) => Promise<void>;
/** The last records control the person used, and what the host answered. */
export type RecordsOutcome = { command: string; args?: Record<string, unknown>; result?: Json; error?: string; refreshFailed?: boolean };

const text = (value: unknown) => typeof value === "string" ? value : value == null ? "" : JSON.stringify(value);
const count = (n: unknown, one: string, many = `${one}s`) => `${Number(n) || 0} ${Number(n) === 1 ? one : many}`;

/** What a package or export states about its logs' own integrity, as its own
 *  sentences: never folded into "verified", which speaks of the bytes. */
export function integrityLines(integrity: Json): string[] {
  if (integrity?.state === "limited") {
    const limits: string[] = Array.isArray(integrity.limits) ? integrity.limits.map(text) : [];
    return ["Log integrity: limited. Package consistency does not establish that its logs are intact.",
      ...limits.map(limit => `Integrity limit: ${limit}`)];
  }
  if (integrity?.state === "no chain recorded broken") return ["Log integrity: no chain is recorded broken."];
  if (integrity?.state === "not stated") return ["Log integrity: not stated."];
  return [];
}

const UNSIGNED = "The package is unsigned: this shows it agrees with its own manifests and recorded chain heads, not who made it.";
const RETENTION_DONE: Record<string, string> = {
  close: "Project closed. Ordinary recording stops for it, and Codex does not start in it, until you reopen it. Setting or releasing a legal hold and disposal are still recorded.",
  reopen: "Project reopened. Other recording limits, if any, still apply.",
  "set-hold": "Legal hold set. This project’s records cannot be disposed of until you release it.",
  "release-hold": "Legal hold released. The App still checks all disposal preconditions.",
};

/** A records control's answer in the person's words: what happened, and what
 *  it means for the records. A refusal keeps the host's own reason. */
export function outcomeWords(outcome: RecordsOutcome | null): { tone: "done" | "refused" | "cancelled"; lines: string[] } | null {
  if (!outcome) return null;
  const { command, result } = outcome;
  if (outcome.error != null) return { tone: "refused", lines: [`The host reported an error. ${command === "records_store_verify_export" || command === "records_chain_heads" ? "The read did not complete." : "Changes may already be present; read the current state before trying again."} Reason: ${outcome.error}`] };
  const state = text(result?.state);
  if (/cancelled|dismissed/.test(state)) return { tone: "cancelled", lines: [`${state[0].toUpperCase()}${state.slice(1)}.`] };
  const done = (...lines: (string | false | null | undefined)[]) => ({ tone: "done" as const, lines: lines.filter(Boolean) as string[] });
  switch (command) {
    case "records_store_export":
      if (!state.includes("export created")) break;
      return done(`Export created in ${text(result?.folder)}: ${count(result?.files, "file")}, each compared with the store’s file.`,
        "Package bytes: consistent with the manifests and the recorded chain heads.", ...integrityLines(result?.logIntegrity), UNSIGNED);
    case "records_store_verify_export":
      if (!state.startsWith("package bytes consistent")) break;
      return done(`Package bytes: consistent. ${count(result?.files, "payload file")} and the export’s own files agree with the manifests and the recorded chain heads.`,
        result?.chainHeadProfile && `Chain-head profile: ${text(result.chainHeadProfile)}.`,
        result?.exportedLogs ? `Exported logs: ${text(result.exportedLogs)}.` : "Exported log bytes: not stated by this package’s verification result.",
        ...integrityLines(result?.logIntegrity), text(result?.administration).includes("unknown") && "This is an older package with no record of closing, holding or disposing; it cannot be used for disposal.", UNSIGNED);
    case "records_store_import_package":
      if (state.startsWith("package controls")) return done(
        state.includes("partly") ? "Some package controls were recovered; others remain held." : "Package controls recovered.",
        ...(Array.isArray(result?.logIntegrity) ? result.logIntegrity.flatMap((entry: Json) => integrityLines(entry.logIntegrity).map(line => `Import ${text(entry.importId)}: ${line}`)) : []),
        text(result?.limit), text(result?.standing));
      if (!state.startsWith("package imported") && !state.startsWith("package already present")) break;
      return done(state.startsWith("package already present")
          ? "This package’s records are already here. Nothing was copied or overwritten."
          : `Package imported: ${count(result?.copied, "file")} copied, ${count(result?.alreadyPresent, "file")} already here and left as they were.`,
        Array.isArray(result?.duplicateIdentities) && result.duplicateIdentities.length > 0 && `The package reports ${count(result.duplicateIdentities.length, "duplicate record identity", "duplicate record identities")}: ${result.duplicateIdentities.map(text).join(", ")}.`,
        ...integrityLines(result?.logIntegrity), text(result?.standing));
    case "records_store_retention":
      if (state === "disposed") return done("Records disposed.",
        result?.administration?.disposition === "unavailable" && "Retention state unavailable. Project closure and legal hold are unknown.",
        text(result?.administration?.limit), text(result?.limit), text(result?.standing),
        ...integrityLines(result?.exportLogIntegrity), text(result?.completion));
      if (state === "recorded") return done(RETENTION_DONE[text(result?.action)] ?? `Recorded: ${text(result?.action)}.`);
      break;
    case "records_store_identity":
      if (state === "adopted") return done(`This folder is now attached to the project its file names (${text(result?.projectId)}).`, text(result?.limit));
      if (state === "new identity") return done(`This folder has a new identity (${text(result?.projectId)}) and takes none of the store’s records under an earlier identity.`, "Records kept under any earlier identity stay in the store under that identity.");
      if (state === "link restored") return done(`The project file was written again to name ${text(result?.projectId)}. The refreshed status shows whether its records are attached.`);
      break;
    case "records_store_import": {
      if (!state.startsWith("imported")) break;
      const conflicts: Json[] = Array.isArray(result?.conflicts) ? result.conflicts : [];
      return done(`${count(result?.copied, "record file")} copied into the records store and compared with the original; ${count(result?.alreadyPresent, "file")} already there.`,
        ...conflicts.map(c => `Not copied: ${text(c?.original)}. ${text(c?.reason)}`), ...(Array.isArray(result?.censusChanged) ? result.censusChanged.map(text) : []),
        text(result?.standing));
    }
    case "records_store_choose":
      if (!["chosen", "default placement chosen", "default placement already in use"].includes(state)) break;
      return done(`From the next time the App starts, it keeps its records in ${text(result?.location)}.`, "Until then it keeps recording where it does now.", text(result?.limit) && `${text(result.limit)[0].toUpperCase()}${text(result.limit).slice(1)}.`);
    case "records_chain_heads":
      return done("The log reader’s report is under “Log integrity” below.");
  }
  return done(state ? `${state[0].toUpperCase()}${state.slice(1)}.` : "The host returned no outcome state; what happened is not known.", text(result?.limit), text(result?.standing));
}

function OutcomeView({ outcome }: { outcome: RecordsOutcome | null }) {
  const words = outcomeWords(outcome);
  if (!words) return null;
  return <div role={words.tone === "refused" ? "alert" : "status"} aria-label="Result of the last records action">
    {words.lines.map((line, index) => <p key={index} style={{ whiteSpace: "pre-wrap" }}>{line}</p>)}
    {outcome?.refreshFailed && <p role="alert">{REFRESH_FAILED}</p>}
  </div>;
}

/** RS §13.8 "Placement": where the store is kept, and the person's choice of
 *  another place. The folder is picked in a native dialog owned by the host;
 *  this view sends only the offered action. */
function PlacementChoice({ choice, busy, act }: { choice: Json; busy: boolean; act: Act }) {
  if (!choice) return null;
  if (choice.offered !== true) return choice.reason ? <p role="note">{text(choice.reason)}</p> : null;
  return <div role="group" aria-label="Where records are kept">
    {choice.choiceUnreadable && <p role="alert">The saved choice of location cannot be read, so the next-start location is not known. Choose a folder again, or return to the App’s data folder. ({text(choice.choiceUnreadable)})</p>}
    {choice.chosen && <p>Saved location: {text(choice.chosen)}.</p>}
    {choice.nextStart && !choice.pending && <p>{choice.overridden ? "Saved location for a start without the override" : "Next-start location"}: {text(choice.nextStart)}.</p>}
    {choice.pending && <p role="note">From the next time the App starts, it keeps its records in {text(choice.nextStart)}. Until then it keeps recording where it does now. Records already kept are not moved.</p>}
    {choice.overridden && <p role="note">{text(choice.overridden)}.</p>}
    <p>
      <button disabled={busy} onClick={() => act("records_store_choose", { action: "choose" })}>Choose where records are kept…</button>{" "}
      {(choice.chosen || choice.choiceUnreadable) && <><button disabled={busy} onClick={() => act("records_store_choose", { action: "default" })}>Keep records in the App’s data folder</button>{" "}</>}
      <small>Takes effect the next time the App starts; you confirm the folder first. Records already kept are not moved or copied. A folder inside the project, a Codex home or a temporary folder is refused.</small>
    </p>
  </div>;
}

const CHAIN_LIMIT = "What the chain shows: a line changed, removed or reordered after it was written, where the lines after it still carry their original links. It does not show a change to the last line of a log, lines removed from its end, or an edit by someone who recomputed the links; log checkpoints are unsigned in this release.";

/** RS §13.8 "Tamper-evidence": what the store's reader reports of the
 *  project's logs. A broken chain is shown by log and line, and never
 *  repaired; `heads` is the answer to "Check the logs now". */
function LogIntegrity({ chain, heads, busy, act }: { chain: Json; heads: Json; busy: boolean; act: Act }) {
  const read = chain?.state === "as the records index last read it";
  const broken: string[] = Array.isArray(heads?.broken) ? heads.broken.map(text) : [];
  const notes: string[] = Array.isArray(heads?.notes) ? heads.notes.map(text) : [];
  const logs: Json[] = Array.isArray(heads?.logs) ? heads.logs : [];
  const limits: string[] = Array.isArray(heads?.limits) ? heads.limits.map(text) : [];
  // Notes can include a role-reader failure: retain them as limits without
  // interpreting their prose as proof that every chain was examined.
  const limited = heads && (heads.discoveryLimit || heads.error || heads.state === "unavailable" || notes.length > 0 || limits.length > 0 || !Array.isArray(heads.limits) || !Array.isArray(heads.logs));
  return <div role="group" aria-label="Log integrity">
    {!heads && read && (chain.historyNotices ?? []).map((notice:string,i:number)=><p role="note" key={`history-${i}`}>{notice}</p>)}
    {read && <p>As last read{chain.readAt ? ` (${text(chain.readAt)})` : ""}:</p>}
    {read && Number(chain.broken) > 0 && <p role="alert">{count(chain.broken, "log has", "logs have")} a broken chain, of {count(chain.logs, "log")} read{Array.isArray(chain.brokenLogs) && chain.brokenLogs.length ? ` (${chain.brokenLogs.map(text).join(", ")})` : ""}. The records are kept as they are and nothing is repaired. Check the logs now to see each line.</p>}
    {read && Number(chain.broken) === 0 && <p>{count(chain.logs, "log")} listed in the last read.{" Chain integrity is not established by this count; check now for the reader’s limits."}{Number(chain.legacy) > 0 ? ` ${count(chain.legacy, "log has", "logs have")} lines written before chaining began.` : ""}</p>}
    {read && chain.discoveryLimit && <p role="alert">Not every log could be listed: {text(chain.discoveryLimit)}</p>}
    {!read && <p>{chain?.state && chain.state !== "not read yet in this process" ? `Log integrity: ${text(chain.state)}.` : "This project’s logs have not been read yet in this session."}</p>}
    <p><button disabled={busy} onClick={() => act("records_chain_heads")}>Check the logs now</button>{" "}<small>Refreshes the project’s log-integrity report and shows the reader’s limits.</small></p>
    {heads && <div aria-label="Logs as checked now">
      {(heads.error || heads.state === "unavailable") && <p role="alert">Log integrity unavailable: {text(heads.error ?? heads.state)}</p>}
      {heads.discoveryLimit && <p role="alert">Not every log could be listed: {text(heads.discoveryLimit)}</p>}
      {limited && <p role="alert">Log integrity: UNKNOWN. Chain integrity is not established for every log.</p>}
      {(heads.historyNotices ?? []).map((notice:string,i:number)=><p role="note" key={`history-${i}`}>{notice}</p>)}
      {limits.length > 0 && <ul>{limits.map((limit, i) => <li key={i}>{limit}</li>)}</ul>}
      {broken.length > 0
        ? <><p role="alert">Checked now: {count(broken.length, "broken chain link")} in {count(logs.length, "log")}. Each is kept as it is and never repaired:</p><ul>{broken.map((line, i) => <li key={i}>{line}</li>)}</ul></>
        : !limited && <p role="status">Checked now: {logs.length === 0 ? "chain integrity is not established for every log." : `${count(logs.length, "log")}; no chain is reported broken.`}</p>}
      {notes.length > 0 && <details><summary>{count(notes.length, "reader note or limit", "reader notes or limits")}</summary><ul>{notes.map((note, i) => <li key={i}>{note}</li>)}</ul></details>}
    </div>}
    <p><small>{CHAIN_LIMIT}</small></p>
  </div>;
}

/** What stands between a folder and its records, in the person's words
 *  (the host names the fault; `records_store::Attachment::fault`). */
const IDENTITY_FAULTS: Record<string, string> = {
  "link missing": "This folder’s project file is missing, so its records are not attached.",
  "link unreadable": "This folder’s project file cannot be read, so its records are not attached.",
  "link changed": "This folder’s project file names a different project than the one recorded for this folder, so no records are attached.",
  "several identities": "The records store has this folder recorded for more than one project, so no records are attached.",
  "moved": "This project’s records are recorded for another folder, so they are not attached here.",
  "duplicated": "Another folder already holds this project’s identity, so this folder is treated as a copy and no records are attached.",
  "another store": "This project’s records were kept in another records store, so nothing is attached here.",
  "link names another store": "This folder’s project file names another records store than this one, so its records are not attached.",
  "no folder recorded": "The records store holds the project this folder’s file names and has no folder recorded for it, so its records are not attached here yet.",
  "association not known": "The records store’s list of project folders was not read whole, and what it could read records no project for this folder, so nothing is attached here.",
};

/** RS §13.8 "Project identity": only the acts the host says resolve this
 *  folder's fault are offered, each with what it does. Nothing is attached,
 *  read or written for an unattached folder until the person chooses one. */
export function IdentityResolution({ attachment, act, linkOnly = false, busy = false }: { attachment: Json; act: Act; linkOnly?: boolean; busy?: boolean }) {
  // With a disposal standing for the recorded project, only the project file
  // can be put back (it reads no record); the folder's identity stays as it is.
  const named: string[] = Array.isArray(attachment?.resolutions) ? attachment.resolutions : [];
  const offered = linkOnly ? named.filter(act_ => act_ === "restore-link") : named;
  if (offered.length === 0) return null;
  const recorded = attachment?.recordedHere ? String(attachment.recordedHere) : null;
  const linked = attachment?.linkedIdentity ? String(attachment.linkedIdentity) : null;
  const identity = (act_: string) => () => act("records_store_identity", { action: act_ });
  return <div role="group" aria-label="Resolve this project’s identity">
    {attachment?.fault && <p role="note">{IDENTITY_FAULTS[String(attachment.fault)] ?? String(attachment.fault)}{attachment?.refusal ? (offered.length === 1 ? " Nothing is recorded for this project until you do this." : " Nothing is recorded for this project until you choose one of these.") : ""}</p>}
    {offered.includes("restore-link") && <p>
      <button disabled={busy} onClick={identity("restore-link")}>Restore the project file</button>{" "}
      <small>For a file that was deleted or edited by mistake. The file is written again to name the project recorded for this folder{recorded ? ` (${recorded})` : ""}. The refreshed status shows whether its records are attached.</small>
    </p>}
    {offered.includes("adopt") && <p>
      <button disabled={busy} onClick={identity("adopt")}>This folder is the project its file names</button>{" "}
      <small>For a project folder you moved or put here. This folder is attached to the project its file names{linked ? ` (${linked})` : ""}, and any earlier folder of that project is released.{recorded ? ` The records of ${recorded} stay in the store under that identity and are no longer attached to this folder.` : ""}</small>
    </p>}
    {offered.includes("new-identity") && <p>
      <button disabled={busy} onClick={identity("new-identity")}>Give this folder a new identity</button>{" "}
      <small>For a copy or a new project. This folder takes none of the records kept in the store under an earlier identity; they stay in the store under that identity.</small>
    </p>}
  </div>;
}

/** RS §13.8: the records store, project identity, package recovery and the
 *  separate explicit import of §13.7 records still in the project. */
export function RecordsStoreView({ store, chain, outcome = null, heads = null, busy = false, act }: { store: Json; chain?: Json; outcome?: RecordsOutcome | null; heads?: Json; busy?: boolean; act: Act }) {
  if (!store) return null;
  const project = store.project;
  const attachment = project?.attachment;
  const retention = project?.retention;
  const packageImport = store.packageImport;
  const packageBlocked = packageImport?.state === "incomplete" || packageImport?.state === "unavailable";
  const kept = retention?.disposition === "kept";
  // The identity acts are for this folder's own state: withheld while its own
  // package import is unfinished. Once a disposal stands, only the project
  // file can be restored.
  const identityRepair = !packageBlocked;
  const linkOnly = !(retention == null || kept);
  const holdable = kept || retention?.disposition === "disposal incomplete";
  const terminalDisposition = ["disposed", "disposal incomplete", "completion durability uncertain"].includes(retention?.disposition);
  const packageImportable = store.state === "available" && !packageBlocked && !terminalDisposition;
  const packageRepairable = store.state === "available" && !terminalDisposition && packageImport?.canRepair === true;
  return <section aria-label="Records store">
    <h3>Records store</h3>
    <OutcomeView outcome={outcome}/>
    {store.state === "available"
      ? <p>Store: {String(store.root)} ({String(store.placement)}).</p>
      : <p role="alert">No records store: {String(store.error)}. Nothing is recorded; there is no fallback.</p>}
    {store.state !== "available" && store.configured && <p>Configured location: {String(store.configured)} ({String(store.placement)}).</p>}
    {(store.limits ?? []).map((l: string) => <p key={l} role="note">{l}</p>)}
    <PlacementChoice choice={store.placementChoice} busy={busy} act={act}/>
    {store.registry && <p role="alert">{String(store.registry)}</p>}
    {project && <>
      <p>Project: {attachment?.projectId ? String(attachment.projectId) : "attached identity not reported"}; reading {String(project.reading ?? project.state)}.</p>
      {attachment?.refusal && <p role="alert">{String(attachment.refusal)}</p>}
      {(project.notes ?? []).map((n: string) => <p key={n} role="note">{n}</p>)}
      {attachment?.projectId && !attachment?.refusal && kept && !packageBlocked && project.reading === "records store" && <p>
        <button disabled={busy} onClick={() => act("records_store_export")}>Export project records</button>{" "}
        <small>Creates a verified package in a folder you choose.</small>
      </p>}
      {packageImportable && <p>
        <button disabled={busy} onClick={() => act("records_store_import_package", { action: "import" })}>Import verified package</button>{" "}
        <small>Choose a package for the identity already named by this folder’s project file. Exact bytes and the original identity are retained; conflicting files are refused. Unsigned package content stays quoted evidence.</small>
      </p>}
      {packageImportable && <p>
        <button disabled={busy} onClick={() => act("records_store_import_package", { action: "restore" })}>Restore project from package</button>{" "}
        <small>Recover the package’s original project identity. The App checks whether this folder has no identity or only an unused identity created at startup. It refuses to replace an identity with records, a legal hold, closure or disposal, and retains existing bytes.</small>
      </p>}
      {packageImport?.state === "incomplete" && <p role="alert">
        Package import is interrupted. Project records remain unavailable until it is finished.{" "}
        {packageImport.canFinish === true
          ? <button disabled={busy} onClick={() => act("records_store_import_package", { action: "resume" })}>Finish package import</button>
          : <>It cannot be finished from here now{packageImport.finishReason ? `: ${String(packageImport.finishReason)}` : "."}</>}
      </p>}
      {packageImport?.state === "unavailable" && <p role="alert">Package import status is unavailable. Project records remain unavailable.</p>}
      {packageRepairable && <p>
        <button disabled={busy} onClick={() => act("records_store_import_package", { action: "repair" })}>Repair package controls</button>{" "}
        <small>Uses the original native intent and retained evidence. Differing control bytes or a missing original act keep recovery held. Package claims stay quoted evidence and grant no authority to replay acts.</small>
      </p>}
      {packageImport?.reason && <p role="note">Package recovery: {String(packageImport.reason)}</p>}
      {packageImport?.repairReason && packageImport.repairReason !== packageImport.reason && packageImport.repairReason !== packageImport.limit && <p role="note">Package repair: {String(packageImport.repairReason)}</p>}
      {typeof packageImport?.needsPackage === "boolean" && <p role="note">Original package needed for repair: {packageImport.needsPackage ? "yes; the native selector will ask you to choose it again" : "no"}.</p>}
      {packageImport?.limit && packageImport.limit !== packageImport.reason && <p role="note">Package import: {String(packageImport.limit)}</p>}
      {(packageImport?.importId || packageImport?.packageIdentity) && <p>Package import: {String(packageImport.state)}. {packageImport.importId && <>Import reference: {String(packageImport.importId)}. </>}{packageImport.packageIdentity && <>Package identity: {String(packageImport.packageIdentity)}.</>}</p>}
      {retention && <p role="note">{retention.disposition === "unavailable"
        ? "Retention state unavailable. Project closure and legal hold are unknown."
        : <>{retention.closed ? "Project closed to recording." : "Project open."} Legal hold: {retention.legalHold ? "set" : "not set"}. Records: {String(retention.disposition)}.</>}{" "}{retention.limit && String(retention.limit)}</p>}
      {attachment?.projectId && !attachment?.refusal && holdable && !packageBlocked && <p>
        {kept && <><button disabled={busy} onClick={()=>act("records_store_retention",{action:retention.closed ? "reopen" : "close"})}>{retention.closed ? "Reopen project" : "Close project"}</button>{" "}</>}
        <button disabled={busy} onClick={()=>act("records_store_retention",{action:retention.legalHold ? "release-hold" : "set-hold"})}>{retention.legalHold ? "Release legal hold" : "Set legal hold"}</button>{" "}
        {kept && retention.closed && !retention.legalHold && <button disabled={busy} onClick={()=>act("records_store_retention",{action:"dispose"})}>Dispose of records after verified export</button>}
      </p>}
      {(retention?.disposition === "disposal incomplete" || retention?.disposition === "completion durability uncertain") && <p role="alert">Disposal or completion publication is unconfirmed and recording is blocked. {retention.legalHold ? <small>Legal hold blocks further disposal.</small> : packageBlocked ? null : attachment?.projectId && !attachment?.refusal ? <button disabled={busy} onClick={()=>act("records_store_retention",{action:"resume-disposal"})}>Finish disposal</button> : <small>The disposal can be finished once this folder is attached to its records again; restore the project file first.</small>}</p>}
      {project.notImported > 0 && kept && !retention.closed && !packageBlocked && <p>
        <button disabled={busy} onClick={() => act("records_store_import")}>Import {String(project.notImported)} record file(s){project.notImportedKinds ? ` (${String(project.notImportedKinds)})` : ""}</button>{" "}
        <small>{String(project.importStanding ?? "")}</small>
      </p>}
      {attachment?.projectId && !attachment?.refusal && project.reading === "records store" && <LogIntegrity chain={chain} heads={heads} busy={busy} act={act}/>}
      {identityRepair && <IdentityResolution attachment={attachment} act={act} linkOnly={linkOnly} busy={busy}/>}
    </>}
    <p><button disabled={busy} onClick={() => act("records_store_verify_export")}>Verify an exported package</button></p>
  </section>;
}

/** Keeps each answer with the project whose control was pressed. A failed
 * refresh is visible alongside that answer; no operation is retried. */
export function RecordsStorePanel({ store, chain, invoke, refresh }: { store: Json; chain?: Json; invoke: (command: string, args?: Record<string, unknown>) => Promise<Json>; refresh: () => Promise<unknown> | void }) {
  const scope = JSON.stringify([store?.root ?? store?.configured, store?.project?.attachment?.root, store?.project?.attachment?.projectId]);
  const [last, setLast] = useState<{ scope: string; outcome: RecordsOutcome; heads: Json } | null>(null);
  const [busy, setBusy] = useState(false);
  const running = useRef(false);
  const act: Act = async (command, args) => {
    if (running.current) return;
    running.current = true;
    setBusy(true);
    setLast(null);
    let outcome: RecordsOutcome;
    let heads: Json = null;
    try {
      const result = await invoke(command, args);
      if (command === "records_chain_heads") heads = result;
      outcome = { command, args, result };
    } catch (error) {
      outcome = { command, args, error: String(error) };
    }
    setLast({ scope, outcome, heads });
    try { await refresh(); }
    catch { outcome = { ...outcome, refreshFailed: true }; }
    finally {
      setLast({ scope, outcome, heads });
      running.current = false;
      setBusy(false);
    }
  };
  return <RecordsStoreView store={store} chain={chain} outcome={last?.scope === scope ? last.outcome : null} heads={last?.scope === scope ? last.heads : null} busy={busy} act={act}/>;
}
