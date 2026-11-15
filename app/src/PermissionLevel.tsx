import { createContext, useContext, useEffect, useRef, useState } from "react";
import { AgentText, numberWords, wordOf } from "./AgentText";
import { REFRESH_FAILED } from "./statusRefresh";

type Json = any;
type Scope = "default" | { conversation: string };
export const PermissionLevelActions = createContext<null | {
  change: (owner: string, scope: Scope, levelId: string) => Promise<{ result?: Json; error?: string; refreshFailed: boolean }>;
  unavailable: boolean;
  stale: boolean;
  readFailed?: boolean;
  host?: Json;
}>(null);
export const levelOwner = (host: Json): string => JSON.stringify([host?.homeRouting?.activeModeHomeClass, host?.generation]);

const NAMES = { supervised: "Supervised", edits: "Project edits", "edits-network": "Project edits and network", "edits-no-asking": "Project edits without asking", full: "Full access" } as const;
const WRITES = { nowhere: "Commands cannot write within the sandbox.", project: "Commands can write in the project within the sandbox.", everywhere: "Commands can write with your account's access, including outside the project." };
const NETWORK = { off: "Network access is off within the sandbox.", on: "Commands can reach the network." };
const ASKS = { "before-a-command-not-known-safe": "Codex asks before a command it does not know to be safe.", "when-beyond-the-sandbox": "Codex can ask to run beyond the sandbox.", never: "Commands run without asking." };
const ORIGINS = { chosen: "Chosen by you.", "app-default": "The App's default level.", "session-only": "Chosen for this session only." };
const AGREEMENT = { agrees: "Codex's report agrees with the level in force.", differs: "Codex reported another level. The next turn is refused.", "not-confirmed": "Codex has not confirmed the level in force." };
const REFUSALS = {
  "edits-level-reaches-app-folders": "Project edits would reach the App's own folders. Supervised and Full access remain offered.",
  "project-path-breaks-codex-sandbox": "The project path cannot be used with Codex's sandbox. Only Full access remains offered here.",
  "app-folders-not-established": "The App's folders have not been established for a sandboxed level. Only Full access remains offered here.",
  "project-not-established": "The project folder has not been established for a sandboxed level. Only Full access remains offered here.",
  "codex-reported-another-level": "Codex reported another level. The App refused the next turn.",
};
const CHILD_LEVEL = "An agent already started by this conversation keeps the level it was started with.";
const list = (value: Json): Json[] => Array.isArray(value) ? value : [];
const name = (id: Json) => wordOf(NAMES, id) ?? "Not established";

function ReportedValue({ value }: { value: Json }) {
  return <AgentText source="record" value={typeof value === "string" ? value : JSON.stringify(value) ?? "not supplied"} />;
}

function LevelRefusal({ cause }: { cause: Json }) {
  if (!cause) return null;
  return <div role="alert"><p>{wordOf(REFUSALS, cause.refused) ?? "The App refused to send this level. Its reason is shown below."}</p>
    {!wordOf(REFUSALS, cause.refused) && <ReportedValue value={cause}/>}
    {cause.folder && <p>Folder: <AgentText source="file" value={cause.folder}/></p>}
  </div>;
}

function LastingRules({ rules, homeClass }: { rules: Json; homeClass: Json }) {
  const home = list(rules?.homes).find(row => row.modeHomeClass === homeClass);
  const reading = home?.lastingRules;
  return <details><summary>Lasting rules in this Codex home</summary>
    {/* appSentence is a closed constant from lasting_rules.rs; paths and file lines are separate. */}
    {typeof rules?.appSentence === "string" && <p>{rules.appSentence}</p>}
    <p>{reading?.state === "none" ? "No lasting rules files were found." : reading?.state === "read" ? "Lasting rules files were read." : "Lasting rules are not fully known."}</p>
    {reading?.readAt && <p>Read at: <ReportedValue value={reading.readAt}/></p>}
    {home?.home && <p>Codex home: <AgentText source="file" value={home.home}/></p>}
    {reading?.reason && <ReportedValue value={reading.reason}/>}
    {list(reading?.files).map((file, i) => <div key={i}>
      <p>Rules file: <AgentText source="file" value={file.path}/></p>
      {[...list(file.prefixRules), ...list(file.networkRules)].map((rule, j) => <AgentText key={j} block source="file" value={rule.line}/>)}
      {file.unreadLines > 0 && <p>Lines not read as rules: {numberWords(file.unreadLines)}.</p>}
    </div>)}
    {list(reading?.unreadFiles).map((file, i) => <div key={i}><AgentText source="file" value={file.path}/><ReportedValue value={file.reason}/></div>)}
    {reading?.skippedEntries > 0 && <p>Entries skipped: {numberWords(reading.skippedEntries)}.</p>}
  </details>;
}

function ProjectTrust({ trust }: { trust: Json }) {
  return <div aria-label="Project trust sent to Codex">
    {trust ? <>
      {/* These lines are built solely from codex_level.rs's closed sentences and its own read time. */}
      {list(trust.lines).map((line, i) => <p key={i}>{line}</p>)}
      {trust.projectRoot && <p>Project: <AgentText source="file" value={trust.projectRoot}/></p>}
      {trust.sentKey && <p>Settings key sent: <AgentText source="file" value={trust.sentKey}/></p>}
      {trust.matchedKey && <p>Settings key read: <AgentText source="file" value={trust.matchedKey}/></p>}
      {trust.detail?.text && <ReportedValue value={trust.detail.text}/>}
    </> : <p>Project trust has not been reported for a start, resume or fork.</p>}
  </div>;
}

/** A fresh component per home/generation/conversation: a pending choice or result never follows navigation. */
export function PermissionLevel({ host, threadId }: { host: Json; threadId?: string }) {
  return <LevelPanel key={JSON.stringify([levelOwner(host), threadId])} host={host} threadId={threadId}/>;
}

/** Start composers use the same active-home reading as the ordinary New conversation view. */
export function StartPermissionLevel({ threadId, generation }: { threadId?: string; generation?: Json }) {
  const actions = useContext(PermissionLevelActions);
  if (actions?.host && threadId && generation && JSON.stringify(generation) !== JSON.stringify(actions.host.generation)) {
    return <p>Permission level is not available for this conversation's Codex session.</p>;
  }
  return actions?.host ? <PermissionLevel host={actions.host} threadId={threadId}/> : null;
}

function LevelPanel({ host, threadId }: { host: Json; threadId?: string }) {
  const actions = useContext(PermissionLevelActions);
  const row = threadId ? list(host?.threads).find(t => t.threadId === threadId && JSON.stringify(t.generation) === JSON.stringify(host?.generation)) : null;
  // A selected conversation never borrows the default when its own projection is absent or asked about.
  const level = threadId ? row?.level?.chosen : host?.levelDefault;
  const globalAsk = !level && !row?.level?.ask && typeof host?.levelRecordMissing === "string";
  const ask = row?.level?.ask ?? (globalAsk ? { sentence: host.levelRecordMissing, preselected: host.levelAskPreselected } : null);
  const cause = threadId ? row?.level?.refused : host?.levelSendRefusal?.threadId == null ? host?.levelSendRefusal?.cause : null;
  const initial = ask?.preselected ?? level?.id ?? "";
  const [choice, setChoice] = useState<string>(initial);
  const [pending, setPending] = useState(false);
  const pendingRef = useRef(false);
  const [outcome, setOutcome] = useState<{ error?: string; reply?: Json; refreshFailed?: boolean } | null>(null);
  const mounted = useRef(true);
  useEffect(() => { mounted.current = true; return () => { mounted.current = false; }; }, []);
  const latest = useRef({ actions, choice }); latest.current = { actions, choice };
  useEffect(() => { setChoice(initial); }, [initial]);
  const allowed = (id: string) => {
    if (["project-path-breaks-codex-sandbox", "app-folders-not-established", "project-not-established"].includes(cause?.refused)) return id === "full";
    return cause?.refused !== "edits-level-reaches-app-folders" || id === "full" || id === "supervised";
  };
  const change = async () => {
    if (!mounted.current || !actions || latest.current.actions?.unavailable || latest.current.actions?.stale || latest.current.choice !== choice || pendingRef.current || !wordOf(NAMES, choice) || !allowed(choice)) return;
    pendingRef.current = true; setPending(true); setOutcome(null);
    try {
      const result = await actions.change(levelOwner(host), threadId && !globalAsk ? { conversation: threadId } : "default", choice);
      if (mounted.current) setOutcome({ error: result.error, reply: result.result, refreshFailed: result.refreshFailed });
    } catch (error) { if (mounted.current) setOutcome({ error: error instanceof Error ? error.message : String(error) }); }
    finally { pendingRef.current = false; if (mounted.current) setPending(false); }
  };
  return <section className="workflow-stage" aria-label={threadId ? "Conversation permission level" : "Permission level for new conversations"}>
    <h3>Permission level</h3>
    {actions?.readFailed ? <p role="alert">{REFRESH_FAILED}</p> : actions?.stale ? <p role="status">The App is reading the current permission level. The last reading below may be out of date.</p> : null}
    <p><strong>{level ? name(level.id) : "No permission level reported"}</strong>{threadId ? " · this conversation" : " · new conversations"}</p>
    {level && <>
      <p>{wordOf(ORIGINS, level.origin) ?? "The origin of this level was not reported."}</p>
      {/* The host supplies closed App sentences; no supplier text is interpolated into these fields. */}
      {typeof level.originSentence === "string" && <p>{level.originSentence}</p>}
      {typeof level.explanation === "string" && <p>{level.explanation}</p>}
      <p>{wordOf(WRITES, level.dimensions?.writes) ?? "Write access was not reported."} {wordOf(NETWORK, level.dimensions?.network) ?? "Network access was not reported."} {wordOf(ASKS, level.dimensions?.asks) ?? "When Codex asks was not reported."}</p>
      {typeof level.readingSentence === "string" ? <p>{level.readingSentence}</p> : <p>The reading limit was not reported.</p>}
      {typeof level.allowing === "string" && <p>{level.allowing}</p>}
      {level.id === "full" && <p>At full access commands and file changes are not asked about.</p>}
      {level.sessionOnly?.detail?.text && <ReportedValue value={level.sessionOnly.detail.text}/>}
    </>}
    {typeof host?.levelLaunchRead?.reason === "string" && <p>{host.levelLaunchRead.reason}</p>}
    {host?.levelSessionOnlyOffered?.detail?.text && <ReportedValue value={host.levelSessionOnlyOffered.detail.text}/>}
    {host?.levelLaunchRead?.homeState?.state === "unknown" && host.levelLaunchRead.homeState.detail?.text && <ReportedValue value={host.levelLaunchRead.homeState.detail.text}/>}
    {typeof host?.levelRecordsUnread === "string" && <p>{host.levelRecordsUnread}</p>}
    {ask && <div role="alert"><p>{ask.sentence}</p>
      {choice !== ask.preselected && <p>Your pending choice is {name(choice)}. It takes effect only when you press “Use selected level and continue”.</p>}
    </div>}
    {ask && host?.levelSessionOnlyOffered && <p>A choice made now is kept for this session only.</p>}
    <LevelRefusal cause={cause}/>
    {host?.levelStartRefusal && <div role="alert"><p>Codex could not start with this home.</p><ReportedValue value={host.levelStartRefusal}/></div>}
    <details open={ask ? true : undefined}><summary>{ask ? "Choose a permission level to continue" : "Change permission level"}</summary>
      <label>Permission level <select aria-label="Permission level" value={choice} onChange={event => setChoice(event.target.value)} disabled={pending || !!actions?.unavailable || !!actions?.stale || !actions}>
        {!wordOf(NAMES, choice) && <option value="">Choose a level</option>}
        {Object.keys(NAMES).map(id => <option key={id} value={id} disabled={!allowed(id)}>{wordOf(NAMES, id)}</option>)}
      </select></label>{" "}
      <button onClick={() => { void change(); }} disabled={!actions || pending || actions.unavailable || actions.stale || !wordOf(NAMES, choice) || !allowed(choice)}>{ask ? "Use selected level and continue" : threadId ? "Use for this conversation" : "Use for new conversations"}</button>
      <p>{threadId && !globalAsk ? "This choice applies to this conversation." : "This choice is the default for new conversations."}</p>
    </details>
    {pending && <p role="status">Changing the permission level…</p>}
    {outcome?.error && <div role="alert"><p>The permission level was not changed.</p><p>{outcome.error}</p></div>}
    {outcome?.reply && <p role="status">{outcome.reply.state === "chosen" ? "The App accepted your level choice." : "The App returned a result for the level choice."}</p>}
    {outcome?.reply?.sentence && <p>{outcome.reply.sentence}</p>}
    {outcome?.reply?.writeFailure && <ReportedValue value={outcome.reply.writeFailure}/>}
    {outcome?.refreshFailed && !actions?.readFailed && <p role="alert">{REFRESH_FAILED}</p>}
    {threadId && <>
      <p>Last level sent: {name(row?.level?.sent?.levelId)}. {row?.level?.sent?.writeResult === "written" ? "Written to Codex." : "Writing it to Codex is not established."}</p>
      {row?.level?.reported ? <div>
        <p>Codex reply for the {name(row.level.reported.requestedLevelId)} request:</p>
        <p>Approval policy: <AgentText source="codex" value={JSON.stringify(row.level.reported.approvalPolicy) ?? "not supplied"}/></p>
        <p>Approval reviewer: <AgentText source="codex" value={JSON.stringify(row.level.reported.approvalsReviewer) ?? "not supplied"}/></p>
        <p>Sandbox: <AgentText source="codex" value={JSON.stringify(row.level.reported.sandbox) ?? "not supplied"}/></p>
      </div> : <p>Codex has not reported a level.</p>}
      <p>{wordOf(AGREEMENT, row?.level?.agreement) ?? "Agreement has not been reported."}</p>
      {typeof row?.level?.takesEffectSentence === "string" && <p>{row.level.takesEffectSentence}</p>}
      {row?.level?.inheritancePersistence?.state === "not-recorded" && <div role="alert">
        <p>{row.level.inheritancePersistence.sentence}</p>
        {row.level.inheritancePersistence.detail?.text && <ReportedValue value={row.level.inheritancePersistence.detail.text}/>}
      </div>}
      <p>{CHILD_LEVEL}</p>
      <ProjectTrust trust={row?.level?.projectTrust}/>
    </>}
    <LastingRules rules={host?.codexHomeRules} homeClass={host?.homeRouting?.activeModeHomeClass}/>
  </section>;
}
