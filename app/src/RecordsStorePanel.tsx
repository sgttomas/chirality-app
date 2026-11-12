type Json = any; // eslint-disable-line @typescript-eslint/no-explicit-any

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
  "link names another store": "This folder’s project file names another records store. This store’s records for the project stay attached.",
};

/** RS §13.8 "Project identity": only the acts the host says resolve this
 *  folder's fault are offered, each with what it does. Nothing is attached,
 *  read or written for an unattached folder until the person chooses one. */
export function IdentityResolution({ attachment, act }: { attachment: Json; act: (command: string, args?: Record<string, unknown>) => Promise<void> }) {
  const offered: string[] = Array.isArray(attachment?.resolutions) ? attachment.resolutions : [];
  if (offered.length === 0) return null;
  const recorded = attachment?.recordedHere ? String(attachment.recordedHere) : null;
  const linked = attachment?.linkedIdentity ? String(attachment.linkedIdentity) : null;
  const identity = (act_: string) => () => act("records_store_identity", { action: act_ });
  return <div role="group" aria-label="Resolve this project’s identity">
    {attachment?.fault && <p role="note">{IDENTITY_FAULTS[String(attachment.fault)] ?? String(attachment.fault)}{attachment?.refusal ? " Nothing is recorded for this project until you choose one of these." : ""}</p>}
    {offered.includes("restore-link") && <p>
      <button onClick={identity("restore-link")}>Restore the project file</button>{" "}
      <small>For a file that was deleted or edited by mistake. The file is written again to name the project recorded for this folder{recorded ? ` (${recorded})` : ""}, and that project’s records are attached.</small>
    </p>}
    {offered.includes("adopt") && <p>
      <button onClick={identity("adopt")}>This folder is the project its file names</button>{" "}
      <small>For a project folder you moved or put here. This folder is attached to the project its file names{linked ? ` (${linked})` : ""}, and any earlier folder of that project is released.{recorded ? ` The records of ${recorded} stay in the store under that identity and are no longer attached to this folder.` : ""}</small>
    </p>}
    {offered.includes("new-identity") && <p>
      <button onClick={identity("new-identity")}>Give this folder a new identity</button>{" "}
      <small>For a copy or a new project. This folder starts with no records. Records kept under any earlier identity stay in the store under that identity.</small>
    </p>}
  </div>;
}

/** RS §13.8: the records store, project identity, package recovery and the
 *  separate explicit import of §13.7 records still in the project. */
export function RecordsStorePanel({ store, act }: { store: Json; act: (command: string, args?: Record<string, unknown>) => Promise<void> }) {
  if (!store) return null;
  const project = store.project;
  const attachment = project?.attachment;
  const retention = project?.retention;
  const packageImport = store.packageImport;
  const packageBlocked = packageImport?.state === "incomplete" || packageImport?.state === "unavailable";
  const kept = retention?.disposition === "kept";
  const identityRepair = !packageBlocked && (retention == null || kept);
  const holdable = kept || retention?.disposition === "disposal incomplete";
  const terminalDisposition = ["disposed", "disposal incomplete", "completion durability uncertain"].includes(retention?.disposition);
  const packageImportable = store.state === "available" && !packageBlocked && !terminalDisposition;
  const packageRepairable = store.state === "available" && !terminalDisposition && packageImport?.canRepair === true;
  return <section aria-label="Records store">
    <h3>Records store</h3>
    {store.state === "available"
      ? <p>Store: {String(store.root)} ({String(store.placement)}).</p>
      : <p role="alert">No records store: {String(store.error)}. Nothing is recorded; there is no fallback.</p>}
    {(store.limits ?? []).map((l: string) => <p key={l} role="note">{l}</p>)}
    {project && <>
      <p>Project: {attachment?.projectId ? String(attachment.projectId) : "no identity yet"}; reading {String(project.reading ?? project.state)}.</p>
      {attachment?.refusal && <p role="alert">{String(attachment.refusal)}</p>}
      {(project.notes ?? []).map((n: string) => <p key={n} role="note">{n}</p>)}
      {attachment?.projectId && !attachment?.refusal && kept && !packageBlocked && project.reading === "records store" && <p>
        <button onClick={() => act("records_store_export")}>Export project records</button>{" "}
        <small>Creates a verified package in a folder you choose.</small>
      </p>}
      {packageImportable && <p>
        <button onClick={() => act("records_store_import_package", { action: "import" })}>Import verified package</button>{" "}
        <small>Choose a package for the identity already named by this folder’s project file. Exact bytes and the original identity are retained; conflicting files are refused. Unsigned package content stays quoted evidence.</small>
      </p>}
      {packageImportable && <p>
        <button onClick={() => act("records_store_import_package", { action: "restore" })}>Restore project from package</button>{" "}
        <small>Recover the package’s original project identity. The App checks whether this folder has no identity or only an unused identity created at startup. It refuses to replace an identity with records, a legal hold, closure or disposal, and retains existing bytes.</small>
      </p>}
      {packageImport?.state === "incomplete" && <p role="alert">
        Package import is interrupted. Project records remain unavailable until it is finished.{" "}
        <button onClick={() => act("records_store_import_package", { action: "resume" })}>Finish package import</button>
      </p>}
      {packageImport?.state === "unavailable" && <p role="alert">Package import status is unavailable. Project records remain unavailable.</p>}
      {packageRepairable && <p>
        <button onClick={() => act("records_store_import_package", { action: "repair" })}>Repair package controls</button>{" "}
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
        {kept && <><button onClick={()=>act("records_store_retention",{action:retention.closed ? "reopen" : "close"})}>{retention.closed ? "Reopen project" : "Close project"}</button>{" "}</>}
        <button onClick={()=>act("records_store_retention",{action:retention.legalHold ? "release-hold" : "set-hold"})}>{retention.legalHold ? "Release legal hold" : "Set legal hold"}</button>{" "}
        {kept && retention.closed && !retention.legalHold && <button onClick={()=>act("records_store_retention",{action:"dispose"})}>Dispose of records after verified export</button>}
      </p>}
      {(retention?.disposition === "disposal incomplete" || retention?.disposition === "completion durability uncertain") && <p role="alert">Disposal or completion publication is unconfirmed and recording is blocked. {retention.legalHold ? <small>Legal hold blocks further disposal.</small> : !packageBlocked && <button onClick={()=>act("records_store_retention",{action:"resume-disposal"})}>Finish disposal</button>}</p>}
      {project.notImported > 0 && kept && !retention.closed && !packageBlocked && <p>
        <button onClick={() => act("records_store_import")}>Import {String(project.notImported)} record file(s){project.notImportedKinds ? ` (${String(project.notImportedKinds)})` : ""}</button>{" "}
        <small>{String(project.importStanding ?? "")}</small>
      </p>}
      {identityRepair && <IdentityResolution attachment={attachment} act={act}/>}
    </>}
    <p><button onClick={() => act("records_store_verify_export")}>Verify an exported package</button></p>
  </section>;
}
