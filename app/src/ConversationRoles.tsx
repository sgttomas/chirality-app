import { useEffect, useRef, useState } from "react";
import { EXACT_TEXT } from "./exactText";
type Json = any; // eslint-disable-line @typescript-eslint/no-explicit-any

// Conversation roles (DEL-01-04 NIR §5.4 ST-5/ST-6, §5.8 CA-1…CA-4; DEL-02-04
// ROLE §3.1–§3.3, §4.4, §6.2). A conversation's role is fixed for its life
// (L-2): nothing here changes it. "Continue as" starts a new conversation with
// another role; "Fork" is a same-role copy. The role's limits are shown as the
// limit account hands them ("Stated, not enforced").

const list = (value: Json): Json[] => (Array.isArray(value) ? value : []);
const text = (value: Json): string => value === null || value === undefined ? "" : typeof value === "string" ? value : JSON.stringify(value);

/** Roles a person may start a conversation with (ROLE SL-1; owner ruling
 * 2026-10-10: "TASK is not a conversational role"). TASK stays one of the four
 * standing roles: a manager assigns bounded work to it, and its guidance is
 * supplied for that delegation. The host's role set names the same list. */
export const CONVERSATION_ROLES = ["HELP_HUMAN", "HELPS_HUMANS", "WORKING_ITEMS"];

export function roleName(appRole: Json): string {
  if (appRole?.standing === "app-observed") return appRole.role ? text(appRole.role) : "No role";
  return `Role not established in this App process (${text(appRole?.reason) || "no original App binding"})`;
}

/** GC-1: only an actual change of a file this conversation started with is
 * "guidance changed"; a store that could not be read is no change. */
export function guidanceChange(notices: Json): { changed: Json[]; notRead: Json[] } {
  const rows = list(notices);
  return {
    changed: rows.filter((n: Json) => n?.kind === "changed" || n?.kind === "missing"),
    notRead: rows.filter((n: Json) => n?.kind === "not-read"),
  };
}

/** LA-4: the limits as handed by the limit account, per role. */
export function RoleLimits({ limits, role }: { limits: Json; role: string | null }) {
  if (!role) return <p><small>No role: the conversation gets the product guidance only. No role limits are stated.</small></p>;
  const entry = list(limits?.account?.roles).find((r: Json) => r?.role === role);
  const unread = list(limits?.notRead).find((r: Json) => r?.role === role);
  if (!entry) return <p><small>Limits of {role}: {unread ? `${text(unread.reading)} (${text(unread.reason)})` : "not available"}.</small></p>;
  return <ul aria-label={`Limits of ${role}`}>
    {list(entry.limits).map((l: Json) => <li key={text(l.limitId)}><small>{text(l.statement)}: <b>{text(l.presentedAs)}</b>. Not this limit's enforcement: {list(l.notEnforcement).map(text).join(", ")}.</small></li>)}
  </ul>;
}

/** ST-5: the start display's role choice, readable. The default is shown as a
 * preselection the person can change or clear before starting. */
// `group` is the radio group's name: each instance on screen needs its own (the
// start display's picker and a clean trial's picker must not share one group).
export function RoleChoice({ roleSet, limits, role, setRole, preselected, group }: { roleSet: Json; limits: Json; role: string; setRole: (role: string) => void; preselected: boolean; group: string }) {
  if (!roleSet?.available) return <p>Role set unavailable: {text(roleSet?.reason)}. Only “No role” can be chosen.</p>;
  const offered: string[] = Array.isArray(roleSet.conversationRoles) ? roleSet.conversationRoles.map(text) : CONVERSATION_ROLES;
  const roles = list(roleSet.roles).filter((r: Json) => CONVERSATION_ROLES.includes(text(r.name)) && offered.includes(text(r.name)));
  return <fieldset>
    <legend>Conversation role (fixed for the conversation's life)</legend>
    {roles.map((r: Json) => {
      const name = text(r.name);
      return <div key={name}>
        <label><input type="radio" name={group} value={name} checked={role === name} onChange={() => setRole(name)} /> <b>{name}</b>: {text(r.meaning)}{r.default_for_new_chat ? (role === name && preselected ? " (preselected; change or clear it before starting)" : " (the default for a new conversation)") : ""}</label>
        {role === name && <RoleLimits limits={limits} role={name} />}
      </div>;
    })}
    <label><input type="radio" name={group} value="" checked={role === ""} onChange={() => setRole("")} /> <b>No role</b>: product guidance only.</label>
    <p><small>{text(limits?.standing)}</small></p>
    <p><small>TASK is not a conversation role: a manager assigns bounded work to it, and its guidance is supplied for that delegation.</small></p>
  </fieldset>;
}

/** A prepared catalog is supply only when the original native start receipt
 * matches the complete carrier, including every child composition and file. */
function originalSupplyReceipt(supply: Json): Json {
  return list(supply?.originalStartReceipts).find((r: Json) =>
    typeof supply.supplyRef === "string" && supply.supplyRef.length > 0 && r.supplyRef === supply.supplyRef &&
    r.activeAdmission === true && r.writeResult === "written" && r.outcome === "response-observed-result" &&
    typeof r.requestRef === "string" && r.requestRef.length > 0 && r.requestIdentity != null &&
    Object.prototype.hasOwnProperty.call(supply, "selection") && r.selection === (supply.selection ?? null) &&
    supply.generation != null && r.generation != null && supply.roleSet != null && r.roleSet != null && r.carried?.developerInstructions != null &&
    JSON.stringify(r.generation) === JSON.stringify(supply.generation) &&
    JSON.stringify(r.roleSet) === JSON.stringify(supply.roleSet) &&
    JSON.stringify(r.carried) === JSON.stringify(supply.carried));
}

const childWithholding: Record<string, string> = {
  "not-offered-by-role": "Not offered by this conversation's role.",
  "mechanism-not-supported-at-pin": "Child-role carrier support is not established for this acting supplier.",
  "user-configuration-not-read": "Configuration origins or source currency could not be established.",
  "user-configuration-defines-role": "A person-defined role with this name was preserved.",
  "child-guidance-unavailable": "Child guidance could not be read or composed.",
  "child-file-unavailable": "The App child guidance file could not be published or verified.",
};

/** CR-1/CR-2: receipt-bound supply, with visible withholding. The native
 * configuration reading is bounded evidence, never a lock on future inputs. */
export function NativeChildRoles({ supply }: { supply: Json }) {
  const children = list(supply?.carried?.nativeChildRoles);
  if (children.length === 0) return null;
  const supplied = !!originalSupplyReceipt(supply);
  const namespace = supply?.childNamespaceObservation ?? supply?.carried?.nativeChildObservation;
  return <section aria-label="Native child role supply">
    <p><b>Native child role guidance</b></p>
    <ul>{children.map((child, i) => <li key={`${text(child.role)}:${i}`}>
      <b>{text(child.role)}</b>: {child.status === "supplied"
        ? (supplied ? "Supplied in the original parent start." : "Prepared; native supply not established.")
        : `Not supplied. ${childWithholding[text(child.reason)] ?? (text(child.reason) || "Reason unknown.")}`}
    </li>)}</ul>
    {namespace && <details><summary>Configuration observation</summary>
      <p>{text(namespace.standing)}</p>
      {Array.isArray(namespace.candidateNames) && <p>Observed role names: {namespace.candidateNames.length ? namespace.candidateNames.map(text).join(", ") : "none"}. Sources observed: {text(namespace.sourceCount)}.</p>}
      {namespace.config && <p>Configuration identity: {text(namespace.config.method)} · {text(namespace.config.value)}</p>}
    </details>}
    <p><small>Child supply does not establish that a child was started, provider uptake or consumer adoption. The App preserves the person's roles, features, depth and permissions. TASK's default nondelegation limit is stated, not enforced.</small></p>
  </section>;
}

/** The child's original supply observation is separate from its primary
 * conversation role. Kept in memory across resume; quoted files restore none. */
export function ChildGuidance({ guidance }: { guidance: Json }) {
  if (!guidance) return null;
  if (guidance.standing !== "app-observed-child-supply") return <p>Child guidance unknown: {text(guidance.reason) || "no original App supply association"}.</p>;
  return <div aria-label="Original child guidance">
    <p>Original App child guidance: <b>{text(guidance.role)}</b> (observed). Parent conversation: {text(guidance.native?.parentThreadId ?? guidance.parentThreadId)}. Provider uptake remains unknown.</p>
    <RoleLimits limits={{ account: { roles: [guidance.limitAccount] } }} role={text(guidance.role)} />
    <p><small>This is evidence of the original child supply. It does not set the primary conversation role or restore current role authority. Resume, fork and later generations do not authorize new child associations from this catalog.</small></p>
    {guidance.roleSupplyRecord?.state === "not-confirmed" && <p role="alert">Child association history was not confirmed: {text(guidance.roleSupplyRecord.limit)}.</p>}
    <details><summary>Original child supply evidence</summary><pre style={{ whiteSpace: "pre-wrap" }}>{JSON.stringify(guidance, null, 2)}</pre></details>
  </div>;
}

export function ChildAssociations({ associations }: { associations: Json }) {
  const rows = list(associations);
  if (rows.length === 0) return null;
  return <section aria-label="Observed native child associations">
    <p><b>Observed native children</b></p>
    {rows.map((row, i) => <details key={i}>
      <summary>Child {text(row.native?.threadId)} · parent {text(row.native?.parentThreadId)} · {row.guidance?.standing === "app-observed-child-supply" ? `original ${text(row.guidance.role)} guidance observed` : "guidance unknown"}</summary>
      <ChildGuidance guidance={row.guidance ?? { standing: "unknown" }} />
      <details><summary>Native child event</summary><pre style={{ whiteSpace: "pre-wrap" }}>{JSON.stringify(row.native, null, 2)}</pre></details>
    </details>)}
  </section>;
}

/** DL-3: compare the action with the original child guidance. An association
 * retained across generations establishes no renewed supply or authority. */
export function RoleLimitObservations({ observations }: { observations: Json }) {
  const rows = list(observations);
  if (rows.length === 0) return null;
  return <section aria-label="Observed TASK delegations">
    <p><b>Native delegation compared with original TASK guidance</b></p>
    {rows.map((row, i) => {
      const original = row.originalAssociation;
      const originalGeneration = original?.generation ?? row.root?.generation;
      const actionGeneration = row.actionGeneration ?? row.generation;
      return <div key={i}>
        <p>Child {text(row.parentThreadId)} started child {text(row.threadId)}. Original TASK limit standing: <b>{row.standing === "stated-not-enforced" ? "Stated, not enforced" : text(row.standing) || "unknown"}</b>. The App did not prevent this delegation.</p>
        <p><small>Native event: {text(row.itemId)} · {text(row.source)} · receipt position {text(row.receiptPosition)}. Original root parent: {text(row.root?.parentThreadId)} · original parent supply: {text(original?.parentSupplyRef ?? row.parentSupplyRef)}{original?.associationId ? ` · original TASK association: ${text(original.associationId)}` : ""}.</small></p>
        {originalGeneration && actionGeneration && JSON.stringify(originalGeneration) !== JSON.stringify(actionGeneration) && <p><small>Original guidance generation: {text(originalGeneration)}. Native action generation: {text(actionGeneration)}.</small></p>}
        <p><small>Comparison with original guidance only; no renewed supply, provider uptake or current role authority is established.</small></p>
        {row.roleSupplyRecord?.state === "not-confirmed" && <p role="alert">TASK delegation history was not confirmed: {text(row.roleSupplyRecord.limit)}.</p>}
        <details><summary>TASK delegation evidence</summary><pre style={{ whiteSpace: "pre-wrap" }}>{JSON.stringify(row, null, 2)}</pre></details>
      </div>;
    })}
  </section>;
}

/** The last start's supply, readable (ROLE §6.1, §6.4): the five facts stay apart. */
export function SupplyStatus({ supply }: { supply: Json }) {
  if (!supply) return <p>Role guidance: no conversation started in this home yet.</p>;
  const parts = list(supply.carried?.developerInstructions?.parts);
  const receipt = originalSupplyReceipt(supply);
  return <div>
    {supply.state ? <p>Last start call: {text(supply.state)} · role {supply.selection ? text(supply.selection) : "none"}{supply.continuedFrom ? ` · continues conversation ${text(supply.continuedFrom.sourceThread)}` : ""}.
      {supply.reason ? ` Refused before sending: ${text(supply.reason)}.` : ""}</p> : <p>Role guidance: no conversation started in this home yet.</p>}
    {parts.length > 0 && <p><small>{receipt ? "Supplied at start (retained original receipt)" : "Prepared App guidance; native supply not established by a matching retained receipt"}: {parts.map((p: Json) => `${text(p.source?.path)} (${text(p.source?.state)}, ${text(p.length)} bytes)`).join(" + ")}; App base instructions not set. Whether the model takes it up is unknown.</small></p>}
    <NativeChildRoles supply={supply} />
    <ChildAssociations associations={supply.childAssociations} />
    <RoleLimitObservations observations={supply.roleLimitObservations} />
    {supply.roleSupplyRecord?.state === "not-confirmed" && <p role="alert">Role-supply history was not confirmed: {text(supply.roleSupplyRecord.limit)}. Native effects remain as observed; nothing is resent.</p>}
    <details><summary>Role supply evidence (JSON)</summary><pre style={{ whiteSpace: "pre-wrap" }}>{JSON.stringify(supply, null, 2)}</pre></details>
  </div>;
}

/** ST-6 and §5.8: the conversation header's role line, its relation, the
 * guidance-changed flag and the two ways to go on in another conversation. */
/** WR TT-3b, TT-4: the trial line beside the role header, worded by the host.
 * A clean trial conversation (or a fork of one) shows the host's header; an
 * authoring conversation lists the trials started here. Display only. */
export function TrialHeader({ trialConversation, trialsStartedHere }: { trialConversation?: Json; trialsStartedHere?: Json }) {
  const started = list(trialsStartedHere?.trials);
  if (!trialConversation && started.length === 0) return null;
  return <div aria-label="Trial header">
    {trialConversation && <p role="note"><b>{text(trialConversation.header)}</b></p>}
    {started.length > 0 && <p><small>Trials started here: {started.map((t: Json) => `trial ${text(t.sequence)} of draft ${text(t.draftName)} (${t.kind === "clean" ? "clean" : "delegated"})`).join("; ")}.</small></p>}
  </div>;
}

export function RoleSupplyHistory({ view }: { view: Json }) {
  if (!view) return null;
  return <section aria-label="Quoted role supply history">
    <p><b>Quoted App role-supply history</b>. {text(view.standing)}</p>
    {list(view.limits).map((limit, i) => <p role="alert" key={i}>{text(limit)}</p>)}
    {list(view.observations).map((observation, i) => <details key={i}>
      <summary>{text(observation.record?.trigger)} · {text(observation.record?.outcome)} · {text(observation.record?.supplyId)}</summary>
      <pre style={{whiteSpace:"pre-wrap"}}>{JSON.stringify(observation.record, null, 2)}</pre>
      {list(observation.limits).map((limit, j) => <p role="alert" key={j}>{text(limit)}</p>)}
      {observation.sourceBytes ? <details><summary>Recorded App instruction bytes (quoted evidence)</summary>
        <pre style={{whiteSpace:"pre-wrap"}}>{text(observation.sourceBytes.composed)}</pre>
        {list(observation.sourceBytes.parts).map((part, j) => <details key={j}><summary>{text(part.source?.path)} · {text(part.kind)}</summary><pre style={{whiteSpace:"pre-wrap"}}>{text(part.text)}</pre></details>)}
        {list(observation.sourceBytes.nativeChildren).map((child, j) => <details key={`child:${j}`}><summary>Recorded {text(child.role)} child instruction bytes (quoted evidence)</summary>
          <pre style={{whiteSpace:"pre-wrap"}}>{text(child.composed)}</pre>
          {list(child.parts).map((part, k) => <details key={k}><summary>{text(part.source?.path)} · {text(part.kind)}</summary><pre style={{whiteSpace:"pre-wrap"}}>{text(part.text)}</pre></details>)}
          <details><summary>Recorded child configuration file bytes</summary><pre style={{whiteSpace:"pre-wrap"}}>{text(child.envelope)}</pre></details>
          <details><summary>Recorded child limit account</summary><pre style={{whiteSpace:"pre-wrap"}}>{JSON.stringify(child.limitAccount, null, 2)}</pre></details>
        </details>)}
      </details> : <p><small>Exact App instruction bytes are not established by this observation.</small></p>}
    </details>)}
    {list(view.observations).length === 0 && <p>No role-supply observations were returned. The limits above apply.</p>}
    <p><small>This history does not set the conversation's role or restore CCE authority. Quoted child bytes do not restore child associations. Supplier adoption remains unknown.</small></p>
  </section>;
}

export function RoleHistoryReader({ read, scope, ready }: { read?: () => Promise<Json>; scope: string; ready: boolean }) {
  const [view, setView] = useState<Json>(null);
  const [reading, setReading] = useState(false);
  const serial = useRef(0);
  useEffect(() => { serial.current++; setView(null); setReading(false); return () => { serial.current++; }; }, [scope]);
  const inspect = async () => {
    if (!read) return;
    const current = ++serial.current; setReading(true);
    try { const next = await read(); if (serial.current === current) setView(next); }
    catch (error) { if (serial.current === current) setView({ limits: [String(error)], observations: [], standing: "Role history unavailable; no current role or authority restored" }); }
    finally { if (serial.current === current) setReading(false); }
  };
  return <div><button disabled={!ready || !read || reading} onClick={() => { void inspect(); }}>{reading ? "Reading role-supply history…" : "Read quoted role-supply history"}</button><RoleSupplyHistory view={view} /></div>;
}

export function RoleHeader({ thread, limits, busy, ready, continueAs, fork, trialConversation, trialsStartedHere, readSupplyHistory }: { thread: Json; limits: Json; busy: boolean; ready: boolean; continueAs: (role: string | null) => void; fork: () => void; trialConversation?: Json; trialsStartedHere?: Json; readSupplyHistory?: () => Promise<Json> }) {
  const appRole = thread?.appRole;
  const own: string | null | undefined = appRole?.standing === "app-observed" ? (appRole.role ?? null) : undefined;
  // The choice starts at this conversation's own role (Continue as the same role takes up new guidance).
  const [target, setTarget] = useState<string>(own === undefined ? CONVERSATION_ROLES[0] : (own ?? ""));
  const relation = thread?.roleRelation;
  const { changed, notRead } = guidanceChange(thread?.futureGuidanceNotices);
  return <div aria-label="Conversation role">
    <p>Role: <b>{roleName(appRole)}</b>. It is fixed for this conversation's life; native role hints do not set it.</p>
    <ChildGuidance guidance={thread?.childGuidance} />
    <RoleLimitObservations observations={thread?.roleLimitObservations} />
    <RoleHistoryReader read={readSupplyHistory} scope={JSON.stringify([thread?.generation, thread?.threadId])} ready={ready} />
    <TrialHeader trialConversation={trialConversation} trialsStartedHere={trialsStartedHere} />
    {relation?.kind === "continued-from" && <p><small>Continues conversation {text(relation.from?.sourceThread)} (its role: {roleName(relation.from?.sourceRole)}); a relation only: no history was carried.</small></p>}
    {(relation?.kind === "inherited-fork" || thread?.forkedFrom) && <p><small>Fork of conversation {text(relation?.sourceThread ?? thread?.forkedFrom?.threadId)} (same role): the fork was sent no instructions, so it keeps the source's guidance.</small></p>}
    {own !== undefined && <RoleLimits limits={limits} role={own} />}
    {changed.length > 0 && <p role="status"><b>Guidance changed since this conversation started</b>: {changed.map((n: Json) => `${text(n.path)} (${n.kind === "missing" ? "missing now" : "edited"})`).join(", ")}. Nothing was sent to this conversation; it keeps the guidance it started with. New conversations use the current guidance.{" "}
      {own !== undefined && <button disabled={busy || !ready} onClick={() => continueAs(own)}>Continue as {own ?? "no role"}…</button>}</p>}
    {notRead.length > 0 && <p><small>Current guidance could not be read ({notRead.map((n: Json) => text(n.path)).join(", ")}), so it was not compared.</small></p>}
    <p>
      <label>Continue as <select value={target} disabled={busy} onChange={e => setTarget(e.target.value)}>
        {CONVERSATION_ROLES.map(r => <option key={r} value={r}>{r}</option>)}<option value="">No role</option>
      </select></label>{" "}
      <button disabled={busy || !ready} onClick={() => continueAs(target === "" ? null : target)}>Continue as {target || "no role"}…</button>{" "}
      <button disabled={busy || !ready} onClick={fork}>Fork (same role)</button>
    </p>
    <p><small>Continue as starts a new conversation with that role; this conversation keeps its role. The App first asks this conversation's agent for a handoff summary in a visible turn here, and you edit it before anything is sent. Fork copies this conversation with the same role and guidance.</small></p>
  </div>;
}

export type StartChoice = { model: string; modelProvider: string; entryId: string };

/** The model and the configured provider are exact Codex identifiers, sent as
 * typed; the webview must not capitalise or correct them (EXACT_TEXT). Used by
 * the start display and by Continue as. */
export function ModelProviderFields({ model, modelProvider, setModel, setModelProvider }: { model: string; modelProvider: string; setModel: (model: string) => void; setModelProvider: (provider: string) => void }) {
  return <>
    <label>Model <input {...EXACT_TEXT} value={model} onChange={e => setModel(e.target.value)} /></label>{" "}
    <label>Configured Codex provider <input {...EXACT_TEXT} value={modelProvider} onChange={e => setModelProvider(e.target.value)} /></label>
    <small> The chosen access entry must match this provider: cloud entries use built-in OpenAI; local entries use a configured Responses provider without credentials. An unavailable definition prevents Start.</small>
  </>;
}

/** The handoff message's send state. "sent" only after the send resolved
 * with a result; a refusal or error keeps the draft and allows another try. */
export type SendState = { state: "unsent" | "sending" | "sent" | "failed"; failure?: string; detail?: string; prefillKept?: boolean };
export async function attemptSend(send: (text: string) => Promise<boolean>, draft: string): Promise<SendState> {
  try {
    return (await send(draft)) ? { state: "sent" } : { state: "failed", failure: "The message was not accepted; see the App message below." };
  } catch (e) {
    return { state: "failed", failure: String(e) };
  }
}
export function SendOutcome({ outcome }: { outcome: SendState }) {
  if (outcome.state === "sending") return <p><small>Sending; waiting for Codex's response.</small></p>;
  if (outcome.state === "sent") return <p><small>Sent once as an ordinary message; see the new conversation for Codex's response.</small></p>;
  if (outcome.state === "failed") return <p role="alert"><small>Not sent: {outcome.failure} The draft is kept; nothing is resent automatically. You can send it again.</small></p>;
  return null;
}

/** A projection of the handoff owner's original private attempt. This is not
 * a trial SendState, a new native admission or a renderer-created receipt. */
export type HandoffSendOutcome = {
  state: "unsent" | "sending" | "not-attempted" | "sent" | "native-failed" | "unknown";
  attemptRef?: string; target?: Json; reason?: string; nativeResponse?: Json;
  readAvailable?: boolean; sourceCurrent?: boolean; observationFailure?: string;
};
const unknownHandoff = (reason: string): HandoffSendOutcome => ({ state: "unknown", reason });
function handoffOutcome(value: Json): HandoffSendOutcome {
  if (!value || !["unsent", "sending", "not-attempted", "sent", "native-failed", "unknown"].includes(value.state)) return unknownHandoff("The original send observation is unavailable.");
  if (["not-attempted", "sent", "native-failed"].includes(value.state) && (!value.attemptRef || !value.target?.generation || !value.target?.threadId)) return unknownHandoff("The original attempt binding is unavailable.");
  return value;
}
function retainHandoffOutcome(previous: HandoffSendOutcome, next: HandoffSendOutcome): HandoffSendOutcome {
  if (["sent", "native-failed"].includes(previous.state) && next.state !== previous.state) return { ...previous, observationFailure: next.observationFailure ?? next.reason ?? "The current source observation is unavailable." };
  return next;
}
export function HandoffSendStatus({ outcome }: { outcome: HandoffSendOutcome }) {
  return <>
    {outcome.state === "sending" && <p role="status"><small>Waiting for the original send. A second send is blocked while its outcome is observed.</small></p>}
    {outcome.state === "sent" && <p role="status"><small>Sent once as an ordinary message; the original native turn response was observed. Provider completion remains as observed in the new conversation.</small></p>}
    {outcome.state === "not-attempted" && <p role="alert"><small>Not sent: the native owner established that no write attempt occurred. {outcome.reason} The draft is kept; you can send it again.</small></p>}
    {outcome.state === "native-failed" && <p role="alert"><small>The original request received a native error: {text(outcome.nativeResponse?.error?.message ?? outcome.reason)}. The draft is kept; nothing is resent automatically.</small></p>}
    {outcome.state === "unknown" && <p role="alert"><small>Send outcome unknown: {outcome.reason} The draft is kept. Nothing is resent automatically; no second send is offered as proved safe.</small></p>}
    {outcome.observationFailure && <p role="alert"><small>View refresh unavailable: {outcome.observationFailure}. The original send outcome above is retained.</small></p>}
  </>;
}

/** CA-2, CA-3: one open handoff. The draft is editable and unsent; the new
 * conversation starts with no model chosen; its first message is sent only
 * when the person sends it. */
export function ContinueAsPanel({ handoff, entries, busy, ready, start, send, read, open, dismiss }: {
  handoff: Json; entries: { value: string; label: string }[]; busy: boolean; ready: boolean;
  start: (choice: StartChoice) => void; send: (text: string) => Promise<HandoffSendOutcome>; read?: () => Promise<HandoffSendOutcome>; open: () => void; dismiss: () => void;
}) {
  const [draft, setDraft] = useState<string>(text(handoff?.draftText));
  const [seededFrom, setSeededFrom] = useState<string>(text(handoff?.draft?.state));
  const [choice, setChoice] = useState<StartChoice>({ model: "", modelProvider: "", entryId: "" });
  const [sending, setSending] = useState<HandoffSendOutcome>(() => handoff?.sendOutcome ? handoffOutcome(handoff.sendOutcome) : { state: "unsent" });
  const [reading, setReading] = useState(false);
  const pressed = useRef(!["unsent", "not-attempted"].includes(sending.state));
  const sendEpoch = useRef(0);
  const blocked = !["unsent", "not-attempted"].includes(sending.state);
  const sendDraft = () => {
    if (pressed.current || busy || !ready || !draft || blocked) return;
    const epoch = ++sendEpoch.current;
    pressed.current = true;
    setSending({ state: "sending" });
    void Promise.resolve().then(() => send(draft)).then(handoffOutcome, error => unknownHandoff(String(error))).then(outcome => {
      if (epoch !== sendEpoch.current) return;
      if (outcome.state === "unsent") outcome = unknownHandoff("The original send has no observed receipt yet.");
      pressed.current = outcome.state !== "not-attempted";
      setSending(previous => retainHandoffOutcome(previous, outcome));
    });
  };
  const readOriginal = async () => {
    if (!read || reading) return;
    const epoch = sendEpoch.current;
    setReading(true);
    try {
      let outcome = handoffOutcome(await read());
      if (epoch !== sendEpoch.current) return;
      if (outcome.state === "unsent" && pressed.current) outcome = unknownHandoff("The original attempt is not observed yet; no replacement send is allowed.");
      pressed.current = !["unsent", "not-attempted"].includes(outcome.state);
      setSending(previous => retainHandoffOutcome(previous, outcome));
    } catch (error) { if (epoch === sendEpoch.current) setSending(previous => retainHandoffOutcome(previous, unknownHandoff(String(error)))); }
    finally { setReading(false); }
  };
  // The draft is seeded once when the summary arrives. It cannot be edited while
  // the summary is still awaited, so the seed never replaces the person's edits.
  useEffect(() => {
    const state = text(handoff?.draft?.state);
    if (state !== seededFrom && state !== "waiting") { if (!pressed.current) setDraft(text(handoff?.draftText)); setSeededFrom(state); }
  }, [handoff?.draft?.state, handoff?.draftText, seededFrom]);
  const started = handoff?.started;
  const target = handoff?.targetRole ? text(handoff.targetRole) : "no role";
  return <section aria-label="Continue as" style={{ border: "1px solid #888", padding: 8, margin: "8px 0" }}>
    <h3>Continue as {target} from conversation {text(handoff?.sourceThread)}</h3>
    <p>Source conversation: {text(handoff?.sourceThread)} ({text(handoff?.sourceRoleLabel)}); it keeps its role. {text(handoff?.draft?.reading)}</p>
    <label>Handoff message {blocked ? "(original draft retained)" : "(editable; not sent)"} <textarea value={draft} disabled={busy || blocked || text(handoff?.draft?.state) === "waiting"} onChange={e => setDraft(e.target.value)} rows={6} style={{ display: "block", width: "100%" }} /></label>
    {!started && <div>
      <p>The new conversation starts with no model selected; choose one.</p>
      <ModelProviderFields model={choice.model} modelProvider={choice.modelProvider}
        setModel={model => setChoice({ ...choice, model })} setModelProvider={modelProvider => setChoice({ ...choice, modelProvider })} />{" "}
      <label>Access entry <select value={choice.entryId} onChange={e => setChoice({ ...choice, entryId: e.target.value })}><option value="">No entry selected</option>{entries.map(e => <option key={e.value} value={e.value}>{e.label}</option>)}</select></label>
      <p><button disabled={busy || !ready || !choice.model.trim() || !choice.modelProvider.trim() || !choice.entryId} onClick={() => start(choice)}>Start new conversation as {target}</button>{" "}
        <button disabled={busy} onClick={dismiss}>Close without starting</button></p>
      {(!choice.model.trim() || !choice.modelProvider.trim()) && <p><small>Not started — no model selected.</small></p>}
    </div>}
    {started && <div>
      <p>New conversation {text(started.threadId)} started with {target}.{!blocked && " Nothing has been sent to it."}</p>
      <button disabled={busy || !ready || !draft || blocked} onClick={sendDraft}>Send this message to the new conversation</button>{" "}
      {read && blocked && <><button disabled={busy || reading} onClick={() => { void readOriginal(); }}>Read the original send outcome</button>{" "}</>}
      <button disabled={busy} onClick={open}>Open the new conversation</button>{" "}
      <button disabled={busy} onClick={dismiss}>Close</button>
      <HandoffSendStatus outcome={sending} />
    </div>}
    <details><summary>Summary request sent to the source conversation</summary><p>{text(handoff?.requestText)}</p><p>Request: {text(handoff?.request?.state)}{handoff?.request?.reason ? ` (${text(handoff.request.reason)})` : ""}</p></details>
  </section>;
}
