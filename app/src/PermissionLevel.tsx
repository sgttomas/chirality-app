import { createContext, useContext, useEffect, useRef, useSyncExternalStore, type ReactNode } from "react";
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
const ORIGINS = { chosen: "Chosen by you.", "app-default": "The App's default level.", "session-only": "Chosen for this session only.", "save-unconfirmed": "Chosen by you; saving is not confirmed." };
const RECORDED = { recorded: "Recorded", "not-recorded": "Not recorded", "not-confirmed": "Not confirmed" };
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

/** The lasting rules in the Codex home: behind their own disclosure in the full panel; in view (`open`) where the
 * panel is itself one press from the level's name. */
function LastingRules({ rules, homeClass, open = false }: { rules: Json; homeClass: Json; open?: boolean }) {
  const home = list(rules?.homes).find(row => row.modeHomeClass === homeClass);
  const reading = home?.lastingRules;
  const Wrap = open ? "div" : "details";
  return <Wrap aria-label={open ? "Lasting rules in this Codex home" : undefined}>{open ? <p><strong>Lasting rules in this Codex home</strong></p> : <summary>Lasting rules in this Codex home</summary>}
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
  </Wrap>;
}

function ProjectTrust({ trust }: { trust: Json }) {
  return <div aria-label="Project trust requested and sent to Codex">
    {trust ? <>
      {/* These lines are built solely from codex_level.rs's closed sentences and its own read time. */}
      {list(trust.lines).map((line, i) => <p key={i}>{line}</p>)}
      {trust.projectRoot && <p>Project: <AgentText source="file" value={trust.projectRoot}/></p>}
      {trust.requested && <p>Trust entry requested: <AgentText source="record" value={trust.requested}/></p>}
      {trust.requestedKey && <p>Settings key requested: <AgentText source="file" value={trust.requestedKey}/></p>}
      {trust.sent && <p>Trust entry sent: <AgentText source="record" value={trust.sent}/></p>}
      {trust.sentKey && <p>Settings key sent: <AgentText source="file" value={trust.sentKey}/></p>}
      {trust.matchedKey && <p>Settings key read: <AgentText source="file" value={trust.matchedKey}/></p>}
      {trust.detail?.text && <ReportedValue value={trust.detail.text}/>}
    </> : <p>Project trust has not been reported for a start, resume or fork.</p>}
  </div>;
}

/** One choice, one pending latch and one outcome for each level owner, conversation and scope, shared by every
 * mounted copy of the level's chooser (the ask above the composer and the panel in Conversation tools): they never
 * show two selections, and a write held by one disables the other. `initial` is the host's preselected or in-force
 * level the choice started from: when the host reports another, the choice starts again from it. */
type LevelOutcome = { error?: string; reply?: Json; refreshFailed?: boolean };
type SharedChoice = { initial?: string; choice?: string; pending?: boolean; outcome?: LevelOutcome | null };
class LevelChoices {
  private entries = new Map<string, SharedChoice>();
  private listeners = new Set<() => void>();
  version = 0;
  get = (key: string): SharedChoice | undefined => this.entries.get(key);
  set = (key: string, patch: SharedChoice) => {
    this.entries.set(key, { ...this.entries.get(key), ...patch });
    this.version++;
    for (const listener of [...this.listeners]) listener();
  };
  subscribe = (listener: () => void) => { this.listeners.add(listener); return () => { this.listeners.delete(listener); }; };
  snapshot = () => this.version;
}
const LevelChoiceStore = createContext<LevelChoices | null>(null);
/** Shares the level's choice among every chooser inside it; inside another one it adds nothing. */
export function LevelChoiceShare({ children }: { children: ReactNode }) {
  const outer = useContext(LevelChoiceStore);
  const own = useRef<LevelChoices | null>(null);
  if (outer) return <>{children}</>;
  own.current ??= new LevelChoices();
  return <LevelChoiceStore.Provider value={own.current}>{children}</LevelChoiceStore.Provider>;
}

/** Said where the conversation chosen has no row in the current status: nothing of the default stands in for its level. */
export const LEVEL_CONVERSATION_MISSING = "The conversation chosen is not available now, so its permission level is not shown and cannot be changed here.";

/** A fresh component per home/generation/conversation: a pending choice or result never follows navigation. */
export function PermissionLevel({ host, threadId, missing = false }: { host: Json; threadId?: string; missing?: boolean }) {
  if (missing) return <section className="workflow-stage" aria-label="Conversation permission level"><h3>Permission level</h3><p>{LEVEL_CONVERSATION_MISSING}</p></section>;
  return <LevelPanel key={JSON.stringify([levelOwner(host), threadId])} host={host} threadId={threadId}/>;
}

/** The App's ask to choose a level before a conversation runs, in view above the composer without a press: the
 * host's sentence saying why, the level preselected, what the press changes where it changes more than this
 * conversation, and the one button that continues. It is the full panel's own choice (the same shared state,
 * conditions and command), drawn without the rest of the panel; nothing when the App is not asking. */
export function PermissionLevelAsk({ host, threadId, missing = false }: { host: Json; threadId?: string; missing?: boolean }) {
  if (missing) return null;
  return <LevelPanel key={JSON.stringify([levelOwner(host), threadId])} host={host} threadId={threadId} askOnly/>;
}

/** The level in force for a conversation (its own level) or, with no conversation, for new conversations, and
 * whether the App asks the person to choose one: what the settings line names. A conversation chosen whose row is
 * missing has neither. */
export function levelInForce(host: Json, threadId?: string, missing = false): { name: string; ask: boolean } {
  if (missing) return { name: "Not available", ask: false };
  const row = threadId ? list(host?.threads).find(t => t.threadId === threadId && JSON.stringify(t.generation) === JSON.stringify(host?.generation)) : null;
  const level = threadId ? row?.level?.chosen : host?.levelDefault;
  const ask = !!row?.level?.ask || (!level && typeof host?.levelRecordMissing === "string");
  return { name: level ? name(level.id) : "No permission level reported", ask };
}

/** Where the App names levels with none in force, so no host sentence on reading comes with one (an ask, a chooser),
 * it says what the host's READING_SENTENCE says, in the same words (PRD V4-AUT-06: wherever else the App shows a level,
 * it says there that reading is not limited). */
export const READING_NOT_LIMITED = "Reading is not limited at any permission level.";

/** What the level panel reads for one conversation (or, with none, for new conversations). */
function levelReading(host: Json, threadId?: string) {
  const row = threadId ? list(host?.threads).find(t => t.threadId === threadId && JSON.stringify(t.generation) === JSON.stringify(host?.generation)) : null;
  // A selected conversation never borrows the default when its own projection is absent or asked about.
  const level = threadId ? row?.level?.chosen : host?.levelDefault;
  const globalAsk = !level && !row?.level?.ask && typeof host?.levelRecordMissing === "string";
  const ask = row?.level?.ask ?? (globalAsk ? { sentence: host.levelRecordMissing, preselected: host.levelAskPreselected } : null);
  const cause = threadId ? row?.level?.refused : host?.levelSendRefusal?.threadId == null ? host?.levelSendRefusal?.cause : null;
  const scope: Scope = threadId && !globalAsk ? { conversation: threadId } : "default";
  return { row, level, globalAsk, ask, cause, scope };
}

/** The level in force and what it allows, where it comes from, that reading is not limited and, at a level that
 * asks, what allowing a command means, with the host's notes on reading the level: the full panel's read-only words. */
function LevelInForce({ host, threadId, level }: { host: Json; threadId?: string; level: Json }) {
  return <>
    <p><strong>{level ? name(level.id) : "No permission level reported"}</strong>{threadId ? " · this conversation" : " · new conversations"}</p>
    {level && <>
      <p>{wordOf(ORIGINS, level.origin) ?? "The origin of this level was not reported."}</p>
      {/* The host supplies closed App sentences; no supplier text is interpolated into these fields. */}
      {typeof level.originSentence === "string" && <p>{level.originSentence}</p>}
      <p>Current level’s choice record: {wordOf(RECORDED, level.recorded) ?? "Not established"}.</p>
      {typeof level.explanation === "string" && <p>{level.explanation}</p>}
      <p>{wordOf(WRITES, level.dimensions?.writes) ?? "Write access was not reported."} {wordOf(NETWORK, level.dimensions?.network) ?? "Network access was not reported."} {wordOf(ASKS, level.dimensions?.asks) ?? "When Codex asks was not reported."}</p>
      {typeof level.readingSentence === "string" ? <p>{level.readingSentence}</p> : <p>The reading limit was not reported.</p>}
      {typeof level.allowing === "string" && <p>{level.allowing}</p>}
      {level.id === "full" && <p>At full access commands and file changes are not asked about.</p>}
      {level.sessionOnly?.detail?.text && <ReportedValue value={level.sessionOnly.detail.text}/>}
    </>}
    {!level && <p>{READING_NOT_LIMITED}</p>}
    {typeof host?.levelLaunchRead?.reason === "string" && <p>{host.levelLaunchRead.reason}</p>}
    {host?.levelSessionOnlyOffered?.detail?.text && <ReportedValue value={host.levelSessionOnlyOffered.detail.text}/>}
    {host?.levelLaunchRead?.homeState?.state === "unknown" && host.levelLaunchRead.homeState.detail?.text && <ReportedValue value={host.levelLaunchRead.homeState.detail.text}/>}
    {typeof host?.levelRecordsUnread === "string" && <p>{host.levelRecordsUnread}</p>}
  </>;
}

/** What the App last sent to Codex for the conversation, what Codex reported back and whether they agree, a change
 * taking effect from the next turn, and the project's trust as sent: the full panel's read-only words. */
function LevelSent({ row }: { row: Json }) {
  return <>
    {typeof row?.level?.scopeSentence === "string" && <p>{row.level.scopeSentence}</p>}
    <p>Last level sent: {name(row?.level?.sent?.levelId)}. {row?.level?.sent?.writeResult === "written" ? "Written to Codex." : "Writing it to Codex is not established."}</p>
    {row?.level?.reported ? <div>
      <p>Codex reply for the {name(row.level.reported.requestedLevelId)} request:</p>
      <p>Approval policy: <AgentText source="codex" value={JSON.stringify(row.level.reported.approvalPolicy) ?? "not supplied"}/></p>
      <p>Approval reviewer: <AgentText source="codex" value={JSON.stringify(row.level.reported.approvalsReviewer) ?? "not supplied"}/></p>
      <p>Sandbox: <AgentText source="codex" value={JSON.stringify(row.level.reported.sandbox) ?? "not supplied"}/></p>
    </div> : <p>Codex has not reported a level.</p>}
    <p>{wordOf(AGREEMENT, row?.level?.agreement) ?? "Agreement has not been reported."}</p>
    {typeof row?.level?.takesEffectSentence === "string" && <p>{row.level.takesEffectSentence}</p>}
    {row?.level?.inheritancePersistence?.state === "not-confirmed" && <div role="alert">
      <p>{row.level.inheritancePersistence.sentence}</p>
      {row.level.inheritancePersistence.detail?.text && <ReportedValue value={row.level.inheritancePersistence.detail.text}/>}
    </div>}
    <p>{CHILD_LEVEL}</p>
    <ProjectTrust trust={row?.level?.projectTrust}/>
  </>;
}

/** What a press on the level's chooser changes, in the full panel's words: the host's sentence for the default, where
 * it sent one, else the App's. */
function ScopeWords({ host, scope }: { host: Json; scope: Scope }) {
  if (scope !== "default") return <p>This choice applies to this conversation.</p>;
  return typeof host?.levelDefaultScopeSentence === "string" ? <p>{host.levelDefaultScopeSentence}</p> : <p>This choice is the default for new conversations.</p>;
}

/** The settings line's level panel, one press from the level's name: the full panel's own read-only rendering of
 * what the level in force allows, where it came from, that reading is not limited, at a level that asks what allowing
 * a command means, and with them what was sent to Codex and what it reported (the reported policy, reviewer and
 * sandbox), a change taking effect from the next turn, the project's trust as sent with its project root and the
 * lasting rules in the Codex home, in view without a further disclosure. Changing the level is the full panel's
 * (`change`). A conversation chosen whose row is missing shows only that it is not available. */
export function PermissionLevelSummary({ host, threadId, change, missing = false }: { host: Json; threadId?: string; change: () => void; missing?: boolean }) {
  if (missing) return <div className="v4-level-summary"><p>{LEVEL_CONVERSATION_MISSING}</p></div>;
  const { row, level, ask, cause, scope } = levelReading(host, threadId);
  return <div className="v4-level-summary">
    <LevelInForce host={host} threadId={threadId} level={level}/>
    {ask && <p role="alert">{ask.sentence}</p>}
    {scope === "default" && typeof host?.levelDefaultScopeSentence === "string" && <p>{host.levelDefaultScopeSentence}</p>}
    <LevelRefusal cause={cause}/>
    {threadId && <div className="v4-level-sent" aria-label="What the App sent to Codex and what Codex reported"><LevelSent row={row}/></div>}
    <LastingRules rules={host?.codexHomeRules} homeClass={host?.homeRouting?.activeModeHomeClass} open/>
    <p><button type="button" onClick={change}>{ask ? "Choose a permission level to continue" : "Change permission level"}</button></p>
  </div>;
}

/** Start composers use the same active-home reading as the ordinary New conversation view. */
export function StartPermissionLevel({ threadId, generation }: { threadId?: string; generation?: Json }) {
  const actions = useContext(PermissionLevelActions);
  if (actions?.host && threadId && generation && JSON.stringify(generation) !== JSON.stringify(actions.host.generation)) {
    return <p>Permission level is not available for this conversation's Codex session.</p>;
  }
  return actions?.host ? <PermissionLevel host={actions.host} threadId={threadId}/> : null;
}

function LevelPanel({ host, threadId, askOnly = false }: { host: Json; threadId?: string; askOnly?: boolean }) {
  const actions = useContext(PermissionLevelActions);
  const { row, level, globalAsk, ask, cause, scope } = levelReading(host, threadId);
  const save = JSON.stringify(host?.levelChoiceSave?.scope) === JSON.stringify(scope) ? host.levelChoiceSave : null;
  const initial: string = ask?.preselected ?? level?.id ?? "";
  // The choice, latch and outcome are the shared ones for this owner, conversation and scope.
  const outer = useContext(LevelChoiceStore);
  const ownStore = useRef<LevelChoices | null>(null);
  const store = outer ?? (ownStore.current ??= new LevelChoices());
  useSyncExternalStore(store.subscribe, store.snapshot, store.snapshot);
  const key = JSON.stringify([levelOwner(host), threadId ?? null, scope]);
  const choiceNow = (): string => { const entry = store.get(key); return entry && entry.initial === initial && typeof entry.choice === "string" ? entry.choice : initial; };
  const choice = choiceNow();
  const setChoice = (next: string) => store.set(key, { initial, choice: next });
  const pending = !!store.get(key)?.pending;
  const outcome = store.get(key)?.outcome ?? null;
  const previousSave = useRef(save);
  useEffect(() => {
    // A complete host read clears the latest attempt; do not resurrect its command error locally.
    if (previousSave.current && !save) store.set(key, { outcome: null });
    previousSave.current = save;
  }, [save]); // eslint-disable-line react-hooks/exhaustive-deps
  // A copy no longer mounted (its conversation, home or generation left the view) sends nothing.
  const mounted = useRef(true);
  useEffect(() => { mounted.current = true; return () => { mounted.current = false; }; }, []);
  const latest = useRef({ actions }); latest.current = { actions };
  const allowed = (id: string) => {
    if (["project-path-breaks-codex-sandbox", "app-folders-not-established", "project-not-established"].includes(cause?.refused)) return id === "full";
    return cause?.refused !== "edits-level-reaches-app-folders" || id === "full" || id === "supervised";
  };
  const change = async () => {
    // Read at the press from the shared state: a copy whose render is behind, or a write held by any copy, sends nothing.
    if (!mounted.current || !actions || latest.current.actions?.unavailable || latest.current.actions?.stale || store.get(key)?.pending || choiceNow() !== choice || !wordOf(NAMES, choice) || !allowed(choice)) return;
    store.set(key, { pending: true, outcome: null });
    try {
      const result = await actions.change(levelOwner(host), scope, choice);
      store.set(key, { outcome: { error: result.error, reply: result.result, refreshFailed: result.refreshFailed } });
    } catch (error) { store.set(key, { outcome: { error: error instanceof Error ? error.message : String(error) } }); }
    finally { store.set(key, { pending: false }); }
  };
  const reading = actions?.readFailed ? <p role="status">The last permission-level reading could not be refreshed. The level shown may be out of date.</p> : actions?.stale ? <p role="status">The App is reading the current permission level. The last reading below may be out of date.</p> : null;
  const asking = ask && <div role="alert"><p>{ask.sentence}</p>
    {choice !== ask.preselected && <p>Your pending choice is {name(choice)}. It takes effect only when you press “Use selected level and continue”.</p>}
  </div>;
  const chooser = <>
    <label>Permission level <select aria-label="Permission level" value={choice} onChange={event => setChoice(event.target.value)} disabled={pending || !!actions?.unavailable || !!actions?.stale || !actions}>
      {!wordOf(NAMES, choice) && <option value="">Choose a level</option>}
      {Object.keys(NAMES).map(id => <option key={id} value={id} disabled={!allowed(id)}>{wordOf(NAMES, id)}</option>)}
    </select></label>{" "}
    <button onClick={() => { void change(); }} disabled={!actions || pending || actions.unavailable || actions.stale || !wordOf(NAMES, choice) || !allowed(choice)}>{ask ? "Use selected level and continue" : threadId ? "Use for this conversation" : "Use for new conversations"}</button>
  </>;
  const results = <>
    {pending && <p role="status">Changing the permission level…</p>}
    {save && <div aria-label="Latest permission-level save attempt">
      <p>Latest choice save: {wordOf(RECORDED, save.recorded) ?? "Not established"}.</p>
      {typeof save.sentence === "string" && <p>{save.sentence}</p>}
      {save.writeFailure?.text && <ReportedValue value={save.writeFailure.text}/>}
    </div>}
    {outcome?.error && outcome.error !== save?.sentence && <div role="alert"><p>The permission level was not changed.</p><p>{outcome.error}</p></div>}
    {outcome?.reply && <p role="status">{outcome.reply.state === "chosen" ? "The App accepted your level choice." : "The App returned a result for the level choice."}</p>}
    {outcome?.refreshFailed && outcome?.reply?.sentence && <p>{outcome.reply.sentence}</p>}
    {outcome?.refreshFailed && outcome?.reply?.writeFailure?.text && <ReportedValue value={outcome.reply.writeFailure.text}/>}
    {outcome?.refreshFailed && <p role="alert">{REFRESH_FAILED}</p>}
  </>;
  // Above the composer: only while the App asks, and only the ask, with what its press changes where that is more
  // than this conversation (the default for new and saved conversations), in the full panel's words.
  if (askOnly) return ask ? <section className="v4-level-ask" aria-label="Choose a permission level to continue">
    {reading}
    {asking}
    <p>{READING_NOT_LIMITED}</p>
    {typeof host?.levelRecordsUnread === "string" && <p>{host.levelRecordsUnread}</p>}
    {scope === "default" && <ScopeWords host={host} scope={scope}/>}
    <LevelRefusal cause={cause}/>
    <p>{chooser}</p>
    {results}
  </section> : null;
  return <section className="workflow-stage" aria-label={threadId ? "Conversation permission level" : "Permission level for new conversations"}>
    <h3>Permission level</h3>
    {reading}
    <LevelInForce host={host} threadId={threadId} level={level}/>
    {asking}
    {scope === "default" && typeof host?.levelDefaultScopeSentence === "string" && <p>{host.levelDefaultScopeSentence}</p>}
    <LevelRefusal cause={cause}/>
    {host?.levelStartRefusal && <div role="alert"><p>Codex could not start with this home.</p><ReportedValue value={host.levelStartRefusal}/></div>}
    <details open={ask ? true : undefined}><summary>{ask ? "Choose a permission level to continue" : "Change permission level"}</summary>
      {chooser}
      <p>{threadId && !globalAsk ? "This choice applies to this conversation." : "This choice is the default for new conversations."}</p>
    </details>
    {results}
    {threadId && <LevelSent row={row}/>}
    <LastingRules rules={host?.codexHomeRules} homeClass={host?.homeRouting?.activeModeHomeClass}/>
  </section>;
}
