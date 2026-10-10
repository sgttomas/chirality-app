import { useEffect, useState } from "react";
type Json = any; // eslint-disable-line @typescript-eslint/no-explicit-any

// Conversation roles (DEL-01-04 NIR §5.4 ST-5/ST-6, §5.8 CA-1…CA-4; DEL-02-04
// ROLE §3.1–§3.3, §4.4, §6.2). A conversation's role is fixed for its life
// (L-2): nothing here changes it. "Continue as" starts a new conversation with
// another role; "Fork" is a same-role copy. The role's limits are shown as the
// limit account hands them ("Stated, not enforced").

const list = (value: Json): Json[] => (Array.isArray(value) ? value : []);
const text = (value: Json): string => value === null || value === undefined ? "" : typeof value === "string" ? value : JSON.stringify(value);

/** Roles a person may start a conversation with here. TASK is a bounded
 * executor for delegated work, not a conversation entry. */
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
export function RoleChoice({ roleSet, limits, role, setRole, preselected }: { roleSet: Json; limits: Json; role: string; setRole: (role: string) => void; preselected: boolean }) {
  if (!roleSet?.available) return <p>Role set unavailable: {text(roleSet?.reason)}. Only “No role” can be chosen.</p>;
  const roles = list(roleSet.roles);
  return <fieldset>
    <legend>Conversation role (fixed for the conversation's life)</legend>
    {roles.map((r: Json) => {
      const name = text(r.name);
      const offered = CONVERSATION_ROLES.includes(name);
      return <div key={name}>
        <label><input type="radio" name="conversation-role" value={name} checked={role === name} disabled={!offered} onChange={() => setRole(name)} /> <b>{name}</b>: {text(r.meaning)}{r.default_for_new_chat ? (role === name && preselected ? " (preselected; change or clear it before starting)" : " (the default for a new conversation)") : ""}</label>
        {!offered && <small> Not offered as a conversation role here: a bounded executor for delegated work.</small>}
        {role === name && <RoleLimits limits={limits} role={name} />}
      </div>;
    })}
    <label><input type="radio" name="conversation-role" value="" checked={role === ""} onChange={() => setRole("")} /> <b>No role</b>: product guidance only.</label>
    <p><small>{text(limits?.standing)}</small></p>
  </fieldset>;
}

/** The last start's supply, readable (ROLE §6.1, §6.4): the five facts stay apart. */
export function SupplyStatus({ supply }: { supply: Json }) {
  if (!supply || !supply.state) return <p>Role guidance: no conversation started in this home yet.</p>;
  const parts = list(supply.carried?.developerInstructions?.parts);
  return <div>
    <p>Last start: {text(supply.state)} · role {supply.selection ? text(supply.selection) : "none"}{supply.continuedFrom ? ` · continues conversation ${text(supply.continuedFrom.sourceThread)}` : ""}.
      {supply.reason ? ` Refused before sending: ${text(supply.reason)}.` : ""}</p>
    {parts.length > 0 && <p><small>Supplied at start: {parts.map((p: Json) => `${text(p.source?.path)} (${text(p.source?.state)}, ${text(p.length)} bytes)`).join(" + ")}; base instructions not set. Whether the model takes it up is unknown.</small></p>}
    <details><summary>Role supply evidence (JSON)</summary><pre style={{ whiteSpace: "pre-wrap" }}>{JSON.stringify(supply, null, 2)}</pre></details>
  </div>;
}

/** ST-6 and §5.8: the conversation header's role line, its relation, the
 * guidance-changed flag and the two ways to go on in another conversation. */
export function RoleHeader({ thread, limits, busy, ready, continueAs, fork }: { thread: Json; limits: Json; busy: boolean; ready: boolean; continueAs: (role: string | null) => void; fork: () => void }) {
  const appRole = thread?.appRole;
  const own: string | null | undefined = appRole?.standing === "app-observed" ? (appRole.role ?? null) : undefined;
  // The choice starts at this conversation's own role (Continue as the same role takes up new guidance).
  const [target, setTarget] = useState<string>(own === undefined ? CONVERSATION_ROLES[0] : (own ?? ""));
  const relation = thread?.roleRelation;
  const { changed, notRead } = guidanceChange(thread?.futureGuidanceNotices);
  return <div aria-label="Conversation role">
    <p>Role: <b>{roleName(appRole)}</b>. It is fixed for this conversation's life; native role hints do not set it.</p>
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

/** The handoff message's send state. "sent" only after the send resolved
 * with a result; a refusal or error keeps the draft and allows another try. */
export type SendState = { state: "unsent" | "sending" | "sent" | "failed"; failure?: string };
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

/** CA-2, CA-3: one open handoff. The draft is editable and unsent; the new
 * conversation starts with no model chosen; its first message is sent only
 * when the person sends it. */
export function ContinueAsPanel({ handoff, entries, busy, ready, start, send, open, dismiss }: {
  handoff: Json; entries: { value: string; label: string }[]; busy: boolean; ready: boolean;
  start: (choice: StartChoice) => void; send: (text: string) => Promise<boolean>; open: () => void; dismiss: () => void;
}) {
  const [draft, setDraft] = useState<string>(text(handoff?.draftText));
  const [seededFrom, setSeededFrom] = useState<string>(text(handoff?.draft?.state));
  const [choice, setChoice] = useState<StartChoice>({ model: "", modelProvider: "", entryId: "" });
  const [sending, setSending] = useState<SendState>({ state: "unsent" });
  const sent = sending.state === "sent" || sending.state === "sending";
  // The draft is seeded once when the summary arrives; the person's edits are kept after that.
  useEffect(() => {
    const state = text(handoff?.draft?.state);
    if (state !== seededFrom && state !== "waiting") { setDraft(text(handoff?.draftText)); setSeededFrom(state); }
  }, [handoff?.draft?.state, handoff?.draftText, seededFrom]);
  const started = handoff?.started;
  const target = handoff?.targetRole ? text(handoff.targetRole) : "no role";
  return <section aria-label="Continue as" style={{ border: "1px solid #888", padding: 8, margin: "8px 0" }}>
    <h3>Continue as {target} from conversation {text(handoff?.sourceThread)}</h3>
    <p>Source conversation: {text(handoff?.sourceThread)} ({text(handoff?.sourceRoleLabel)}); it keeps its role. {text(handoff?.draft?.reading)}</p>
    <label>Handoff message (editable; not sent) <textarea value={draft} disabled={busy || sent} onChange={e => setDraft(e.target.value)} rows={6} style={{ display: "block", width: "100%" }} /></label>
    {!started && <div>
      <p>The new conversation starts with no model selected; choose one.</p>
      <label>Model <input value={choice.model} onChange={e => setChoice({ ...choice, model: e.target.value })} /></label>{" "}
      <label>Configured Codex provider <input value={choice.modelProvider} onChange={e => setChoice({ ...choice, modelProvider: e.target.value })} /></label>{" "}
      <label>Access entry <select value={choice.entryId} onChange={e => setChoice({ ...choice, entryId: e.target.value })}><option value="">No entry selected</option>{entries.map(e => <option key={e.value} value={e.value}>{e.label}</option>)}</select></label>
      <p><button disabled={busy || !ready || !choice.model.trim() || !choice.modelProvider.trim() || !choice.entryId} onClick={() => start(choice)}>Start new conversation as {target}</button>{" "}
        <button disabled={busy} onClick={dismiss}>Close without starting</button></p>
      {(!choice.model.trim() || !choice.modelProvider.trim()) && <p><small>Not started — no model selected.</small></p>}
    </div>}
    {started && <div>
      <p>New conversation {text(started.threadId)} started with {target}. Nothing has been sent to it.</p>
      <button disabled={busy || !ready || !draft || sent} onClick={() => { setSending({ state: "sending" }); void attemptSend(send, draft).then(setSending); }}>Send this message to the new conversation</button>{" "}
      <button disabled={busy} onClick={open}>Open the new conversation</button>{" "}
      <button disabled={busy} onClick={dismiss}>Close</button>
      <SendOutcome outcome={sending} />
    </div>}
    <details><summary>Summary request sent to the source conversation</summary><p>{text(handoff?.requestText)}</p><p>Request: {text(handoff?.request?.state)}{handoff?.request?.reason ? ` (${text(handoff.request.reason)})` : ""}</p></details>
  </section>;
}
