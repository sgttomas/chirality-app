import { useRef, useState } from "react";
import { itemAnchorId, requestAnchorId, sameActivityGeneration } from "./NativeActivity";
import { EXACT_TEXT } from "./exactText";
type Json = any; // eslint-disable-line @typescript-eslint/no-explicit-any
export type RequestActivityLink = (request: Json) => { open: () => void } | null;

// Readable request cards (DEL-01-04 NIR §4.1–§4.8). A card presents what Codex
// asks and sends the native answer value unchanged; classification, the answer
// values and the register's checks are the host's and stay as they are. The
// App's own words on a tool-permission card never say "accept", "approve",
// "approval" or "approved" (LB-2); supplier names and values that contain them
// appear only in code spans or quoted supplier text. Answering a tool permission
// is the person's routine Codex permission choice: it is not a recorded act and
// it is not approval of the work (NR-9; owner decision D3).

const COMMAND = "item/commandExecution/requestApproval";
const FILE_CHANGE = "item/fileChange/requestApproval";
const PERMISSIONS = "item/permissions/requestApproval";
const LEGACY_EXEC = "execCommandApproval";
const LEGACY_PATCH = "applyPatchApproval";
const QUESTION = "item/tool/requestUserInput";
const ELICITATION = "mcpServer/elicitation/request";
const TOOL_PERMISSION = [COMMAND, FILE_CHANGE, PERMISSIONS, LEGACY_EXEC, LEGACY_PATCH];

export const pre = { whiteSpace: "pre-wrap" as const, overflowWrap: "anywhere" as const, margin: "4px 0" };
const text = (value: Json): string => value === null || value === undefined ? "" : typeof value === "string" ? value : JSON.stringify(value);

/** The conversation a request belongs to, as Codex names it (legacy requests use conversationId). */
export function requestThread(request: Json): string | null {
  const p = request?.nativeParameters ?? {};
  const thread = p.threadId ?? p.conversationId;
  return typeof thread === "string" && thread ? thread : null;
}

/** WI-1: the requests that wait for the person's answer (what the card offers controls for). */
export function answerable(request: Json): boolean {
  return request?.state === "outstanding" && request?.classification === "known-answerable" && request?.originClass !== "named-service";
}

/** A UI observation belongs to the full H5 tuple and typed native ID. It
 * supplies no request authority and contains no answer content. */
export const requestScopeKey = (request: Json): string => JSON.stringify([
  request?.generation?.appSession, request?.generation?.home, request?.generation?.spawnCounter,
  typeof request?.requestIdentity, request?.requestIdentity,
]);
export type RequestCustodyObservation = { scope: string; available: boolean; state?: string; reason?: string };
export type RequestReplyObservation = {
  scope: string;
  command: { kind: "pending" | "written" | "dismissed" } | { kind: "rejected"; reason: string } | { kind: "unconfirmed"; writeResult: string };
  custody: RequestCustodyObservation;
};
export type RequestAnswer = (request: Json, answer: Json) => Promise<RequestReplyObservation | void>;
export type ReadRequestCustody = (request: Json) => Promise<RequestCustodyObservation>;

function replyObservationWords(observation: RequestReplyObservation): string {
  switch (observation.command.kind) {
    case "pending": return "Answer command in progress; waiting for native confirmation or a reply write result.";
    case "written": return "The reply was written locally. Codex receipt or action is not confirmed by that write.";
    case "dismissed": return "Native confirmation dismissed; no reply write was attempted.";
    case "rejected": return `Native answer command reported: ${observation.command.reason}. A complete local reply write is not established by this error alone.`;
    case "unconfirmed": return `Reply write outcome not established (${observation.command.writeResult}); whether Codex received or acted on a reply is unknown.`;
  }
}
export const requestReplyGuarded = (reply: RequestReplyObservation | null | undefined, scope: string): boolean => !!reply && reply.scope === scope &&
  (reply.command.kind === "pending" || reply.command.kind === "written" || reply.command.kind === "unconfirmed" || !reply.custody.available ||
    reply.custody.scope !== scope || reply.custody.state !== "outstanding");

/** §4.1 card titles. */
export function requestTitle(request: Json): string {
  switch (request?.method) {
    case COMMAND: return "Tool permission: run a command";
    case FILE_CHANGE: return "Tool permission: change files";
    case PERMISSIONS: return "Tool permission: extra permissions";
    case LEGACY_EXEC: return "Tool permission: run a command (legacy request)";
    case LEGACY_PATCH: return "Tool permission: change files (legacy request)";
    case QUESTION: return "Question from the agent";
    case ELICITATION: return `Input request from MCP server ${text(request?.nativeParameters?.serverName) || "(name not reported)"} or the agent (not established)`;
    // RS §13.9: the App answers its own records capability's calls by rule.
    case "item/tool/call": if (request?.originClass === "named-service" && request?.nativeParameters?.tool === "chirality_records_read_v1") return "The agent read this project's records (the App's records capability answered; each read is in the read log)";
      return `Request from Codex the App does not answer itself (${text(request?.method)})`;
    default: return `Request from Codex the App does not answer itself (${text(request?.method) || "no method"})`;
  }
}

/** LB-1 App words for each native decision form (the value itself is shown beside them). */
export function decisionWords(decision: Json): string {
  const key = typeof decision === "string" ? decision : decision && typeof decision === "object" ? Object.keys(decision)[0] : "";
  switch (key) {
    case "accept": case "approved": return "Allow once";
    case "acceptForSession": case "approved_for_session": return "Allow for this session";
    case "acceptWithExecpolicyAmendment": case "approved_execpolicy_amendment": return "Allow, and add a lasting rule (see below)";
    case "applyNetworkPolicyAmendment": case "network_policy_amendment": return "Apply the proposed network rule for this host";
    case "decline": return "Don't allow; the agent continues the turn";
    case "cancel": return "Don't allow, and interrupt the turn";
    case "denied": return "Don't allow; the agent tries something else";
    case "abort": return "Don't allow; the agent waits for your next message";
    default: return "Codex option";
  }
}

/** Where a tool-permission request's work lands, as the host reports it: the
 * conversation's project folder (`currentAppProjectContext`, its folder only
 * where the App can display it), or that the conversation has no project, and
 * the working folder Codex reported for the conversation (thread rows' `cwd`).
 * `permissionProfile` is the profile id Codex reported for the conversation;
 * the host does not pass it to the view today, so it is null. */
export type RequestPlace = {
  project: { kind: "folder"; folder: string } | { kind: "none" } | { kind: "unknown" };
  conversationFolder: string | null;
  permissionProfile?: string | null;
};
const keyOf = (decision: Json): string => typeof decision === "string" ? decision : decision && typeof decision === "object" ? Object.keys(decision)[0] ?? "" : "";

/** The place of a request from the host snapshot; `projectFolder` is the
 * displayable project folder (WorkflowContext's appProjectFolder). */
/**
 * What Codex may do in one conversation, as Codex reported it in that conversation's start reply
 * (its sandbox and approval setting, carried on the host's thread row): the person's words for the
 * forms the pinned Codex's source establishes, the reported value beside them, and the value alone
 * for any other form. Nothing is inferred from defaults; an unreported setting is said as unreported.
 */
export function conversationPermissionWords(thread: Json): string {
  const sandbox = thread?.sandbox, approval = thread?.approvalPolicy;
  const type = typeof sandbox === "string" ? sandbox : typeof sandbox?.type === "string" ? sandbox.type : null;
  const net = sandbox && typeof sandbox === "object" && sandbox.networkAccess === true;
  const reads = type === "readOnly" ? `it can read files your account can read and change none without your permission (read-only${net ? ", with network" : ""})`
    : type === "workspaceWrite" ? `it can read files your account can read and change files in its working folder without asking (workspace-write${net ? ", with network" : ""})`
    : type === "dangerFullAccess" ? "it runs without Codex's sandbox, with your account's access (full access)"
    : type ? `Codex reported its sandbox as ${type}` : "Codex did not report its sandbox";
  const asks = approval === "on-request" ? "it asks you before doing more than that (on-request)"
    : approval === "never" ? "it never asks you (never)"
    : typeof approval === "string" && approval ? `Codex reported its approval setting as ${approval}`
    : approval && typeof approval === "object" ? `Codex reported its approval setting as ${JSON.stringify(approval)}`
    : "Codex did not report when it asks you";
  return `${reads}; ${asks}`;
}
export function ConversationPermissions({ thread }: { thread: Json }) {
  return <p aria-label="What Codex may do in this conversation"><strong>What Codex may do here:</strong> {conversationPermissionWords(thread)}, as Codex reported it when this conversation started.</p>;
}
export function requestPlace(request: Json, host: Json, projectFolder: string | null): RequestPlace {
  const context = host?.currentAppProjectContext;
  const project: RequestPlace["project"] = projectFolder !== null ? { kind: "folder", folder: projectFolder }
    : context && typeof context === "object" && (context.reference === null || context.reference === undefined) && !host?.currentAppProjectContextLimit ? { kind: "none" }
    : { kind: "unknown" };
  const thread = requestThread(request);
  const row = (Array.isArray(host?.threads) ? host.threads : []).filter((t: Json) => t?.threadId === thread && JSON.stringify(t?.generation) === JSON.stringify(request?.generation)).pop();
  const profile = row?.activePermissionProfile?.id;
  return { project, conversationFolder: typeof row?.cwd === "string" && row.cwd ? row.cwd : null, permissionProfile: typeof profile === "string" && profile ? profile : null };
}

const windowsAbsolute = (path: string) => /^[A-Za-z]:[\\/]/.test(path);
/** Lexical resolution: `.` and `..` are folded by name; nothing on disk is consulted. */
export function resolvePath(path: string, base: string | null): { path: string; relative: boolean } | null {
  const absolute = path.startsWith("/") || windowsAbsolute(path);
  if (!absolute && (!base || !(base.startsWith("/") || windowsAbsolute(base)))) return null;
  const full = absolute ? path : `${base}/${path}`;
  const windows = windowsAbsolute(full);
  const parts = full.split(windows ? /[\\/]/ : "/");
  const root = windows ? parts.shift()! : "";
  const kept: string[] = [];
  for (const part of windows ? parts : parts.slice(1)) {
    if (part === "" || part === ".") continue;
    if (part === "..") kept.pop(); else kept.push(part);
  }
  return { path: windows ? `${root}\\${kept.join("\\")}` : `/${kept.join("/")}`, relative: !absolute };
}
/** The part of `path` after `folder`, or null when `path` is not inside it. */
export function insideFolder(path: string, folder: string): string | null {
  const base = resolvePath(folder, null)?.path;
  if (!base) return null;
  const sep = windowsAbsolute(base) ? "\\" : "/";
  if (path === base) return "";
  const prefix = base.endsWith(sep) ? base : base + sep;
  return path.startsWith(prefix) ? path.slice(prefix.length) : null;
}

const builtInProfile = (place: RequestPlace | undefined) => typeof place?.permissionProfile === "string" && place.permissionProfile.startsWith(":");
const folderWords = (place: RequestPlace | undefined) => place?.project.kind === "none" ? "this conversation’s working folder" : "your project folder";
const ruleWords = (request: Json, decision: Json): string | null => {
  const inner = decision && typeof decision === "object" ? decision.acceptWithExecpolicyAmendment?.execpolicy_amendment : undefined;
  const words = Array.isArray(inner) ? inner : request?.nativeParameters?.proposedExecpolicyAmendment;
  return Array.isArray(words) && words.length ? words.join(" ") : null;
};

/** The App's words beside one answer: what that answer lets Codex do. */
function DecisionNote({ request, decision, place }: { request: Json; decision: Json; place?: RequestPlace }) {
  const key = keyOf(decision);
  if (key === "acceptForSession" && request?.method === FILE_CHANGE) return <small> Later changes to only these same files are not asked again until Codex stops. Nothing is saved.</small>;
  if (key === "acceptForSession" && request?.method === COMMAND) return <small> This same command, in this folder, is not asked again until Codex stops. Nothing is saved.</small>;
  if (key === "acceptWithExecpolicyAmendment" && request?.method === COMMAND) {
    const words = ruleWords(request, decision);
    return <small> This adds a lasting rule to the rules file in this App’s sign-in folder: from then on, in every conversation of this home, any command beginning with <code>{words ?? "(rule words not reported)"}</code> {builtInProfile(place) ? "runs outside Codex’s sandbox without asking" : "runs with more access than Codex’s sandbox gives, without asking"}. It stays until it is removed from that file.</small>;
  }
  return null;
}

/** The lines above a tool-permission card's answers. */
function AnswerConsequences({ request, forms, place, changesArrived }: { request: Json; forms: { decision: Json }[]; place?: RequestPlace; changesArrived: boolean }) {
  const keys = forms.map(f => keyOf(f.decision));
  const noDecline = keys.includes("cancel") && !keys.some(k => k === "decline" || k === "denied" || k === "abort");
  return <>
    {request?.method === COMMAND && <p>{builtInProfile(place)
      ? "If you allow this command, it runs once outside Codex’s sandbox, with your account’s access to all your files and to the network, in the working folder shown."
      : "If you allow this command, it runs once with more access than Codex’s sandbox gives, which may be all of your account’s access to your files and the network, in the working folder shown."}</p>}
    {request?.method === FILE_CHANGE && changesArrived && <p>If you allow this, Codex writes these files where they are shown, including any outside {folderWords(place)}.</p>}
    {(request?.method === COMMAND || request?.method === FILE_CHANGE) && noDecline && <p>Codex offers no way to refuse and let the agent continue: refusing interrupts the turn, and you can then tell the agent what to do instead.</p>}
  </>;
}

/** One location on a file-change line: the full path, how it was resolved and where it is. */
function ChangeLocation({ path, place, cwd }: { path: Json; place?: RequestPlace; cwd: string | null }) {
  const given = text(path);
  const resolved = resolvePath(given, cwd);
  if (!resolved) return <><code>{given}</code> (relative to a working folder the App has not received; where it goes cannot be shown)</>;
  const base = place?.project.kind === "folder" ? place.project.folder : place?.project.kind === "none" ? place.conversationFolder : null;
  const rest = base ? insideFolder(resolved.path, base) : null;
  return <>
    <code>{resolved.path}</code>{resolved.relative && <> (relative to <code>{text(cwd)}</code>)</>}
    {base === null || base === undefined ? null : rest !== null ? <> — in {folderWords(place)}, at <code>{rest === "" ? "." : rest}</code></> : <> — OUTSIDE {folderWords(place)}</>}
  </>;
}

/** FO-1…FO-3: the decision forms a tool-permission card offers and the native answer each
 * sends, unchanged. With `availableDecisions` exactly those, in order; otherwise the
 * generated forms, the amendment forms only when proposed; legacy forms without `timed_out`. */
export function decisionForms(request: Json): { decision: Json; answer: Json }[] {
  const method = request?.method;
  const p = request?.nativeParameters ?? {};
  if (method === COMMAND || method === FILE_CHANGE) {
    let decisions: Json[] = p.availableDecisions ?? ["accept", "acceptForSession", "decline", "cancel"];
    if (!p.availableDecisions && method === COMMAND) {
      if (p.proposedExecpolicyAmendment) decisions = [...decisions, { acceptWithExecpolicyAmendment: { execpolicy_amendment: p.proposedExecpolicyAmendment } }];
      for (const amendment of p.proposedNetworkPolicyAmendments ?? []) decisions = [...decisions, { applyNetworkPolicyAmendment: { network_policy_amendment: amendment } }];
    }
    return decisions.map(decision => ({ decision, answer: { decision } }));
  }
  if (method === LEGACY_EXEC || method === LEGACY_PATCH) {
    const denied = { denied: { rejection: "" } };
    return [...["approved", "approved_for_session", "abort"].map(decision => ({ decision, answer: { decision } })), { decision: denied, answer: { decision: denied } }];
  }
  return [];
}

/** DM-3: the longest rejection text a person may write on a legacy decline, in
 * characters; the host refuses longer text (native_requests.rs REJECTION_LIMIT). */
export const REJECTION_LIMIT = 2000;
/** Why the host would refuse this rejection text, or null: too long, a control
 * character other than a line break or tab, or a bidirectional formatting
 * character (the host's BIDI_FORMATTING set: U+202A–U+202E, U+2066–U+2069,
 * U+200E, U+200F, U+061C; other format characters, such as the zero-width joiner
 * in emoji, are allowed). Checked before anything is sent. */
export function rejectionProblem(rejection: string): string | null {
  if (Array.from(rejection).length > REJECTION_LIMIT) return `The reason is longer than ${REJECTION_LIMIT} characters.`;
  if (/[\u0000-\u0008\u000b-\u001f\u007f-\u009f]/.test(rejection)) return "The reason has a control character other than a line break or tab.";
  if (/[‪-‮⁦-⁩‎‏؜]/.test(rejection)) return "The reason has a bidirectional formatting character, which could make the confirmation read differently from what is sent.";
  return null;
}
/** DM-3: the legacy `denied` decline carrying the person's text exactly as written ("" when none). */
export const deniedWith = (rejection: string): Json => ({ decision: { denied: { rejection } } });

/** The register's entries, each ended-unanswered one with the context its
 * Codex process ended in (`serverRequestEndContexts`; DEL-01-02's stop
 * record), for CS-7's "when you quit". */
export function hostRequests(host: Json): Json[] {
  const contexts: Json[] = host?.serverRequestEndContexts ?? [];
  return (host?.serverRequests ?? []).map((request: Json) => {
    const known = contexts.find((c: Json) => JSON.stringify(c?.generation) === JSON.stringify(request?.generation) && JSON.stringify(c?.requestIdentity) === JSON.stringify(request?.requestIdentity));
    return known ? { ...request, endContext: known.context } : request;
  });
}

/** §4.4 card states, in the person's words, from the register entry. */
export function cardState(request: Json): string {
  const origin = request?.settlement?.origin;
  const confirmed = request?.acknowledgmentObservation?.status === "observed";
  const method = text(request?.method);
  switch (request?.state) {
    // A request the App answers by rule (no person answer): its reply is either about to be written or was withheld.
    case "received": return request?.originClass === "none" ? "Received; the App's reply has not been sent to Codex" : "Received; not yet shown for an answer";
    case "errored":
      if (request?.closedGeneration) return request?.replyWriteResult === "written" ? "The error reply was written locally; whether Codex received or acted on it is unknown" : "The error reply could not be completely written; whether Codex received or acted on it is unknown";
      return origin?.class === "app-rule" ? `Codex asked for something the App does not provide (${method}): answered with an error by rule ${text(origin.ruleName)}` : `Unrecognized request from Codex (${method}): answered with an error`;
    // A named service the App answers (current time, a records or offered call) waits for the App, not the person.
    case "outstanding": return answerable(request) ? "Waiting for your answer" : "Waiting for a reply from the App; none has been sent to Codex";
    case "settling": return "Sending your answer: not yet written to Codex";
    case "reply-outcome-unknown": return "Reply outcome unknown: the Codex process ended before a write result was observed. Whether Codex received or acted on the reply is unknown";
    case "answered": return confirmed ? "Your answer was written; Codex reported the request resolved" : request?.closedGeneration ? "Your answer was written locally; whether Codex received or acted on it is unknown" : "Your answer was written to Codex; Codex has not confirmed it";
    case "declined":
      if (origin?.class === "app-rule") return `Declined by App rule ${text(origin.ruleName)}, not by you`;
      return confirmed ? "You declined; written; Codex reported the request resolved" : request?.closedGeneration ? "You declined; the reply was written locally; whether Codex received or acted on it is unknown" : "You declined; written to Codex; Codex has not confirmed it";
    case "settle-write-failed": return "Your answer could not be written; whether Codex received it is unknown";
    case "resolved-by-supplier": return `Resolved by Codex before you answered (cause: ${text(request?.supplierResolution?.cause) || "not reported"})`;
    case "ended-unanswered": return request?.endContext === "app-quit" ? "Ended unanswered: the Codex process ended when you quit" : "Ended unanswered: the Codex process ended";
    default: return `Register state ${text(request?.state) || "not reported"}`;
  }
}

/** RT-05: a refused answer leaves the card waiting; the reason in words. */
export function refusalWords(error: string): string {
  const reasons: [string, string][] = [
    ["no-such-request", "this request is no longer known"],
    ["generation-closed", "Codex restarted since this was asked"],
    ["already-resolved", "Codex already resolved it"],
    ["already-settled", "already answered"],
    ["invalid-answer", "that answer is not one this request offers"],
  ];
  const known = reasons.find(([code]) => error.includes(code));
  return known ? `Last answer not taken: ${known[1]} (${error})` : `Last answer not taken: ${error}`;
}

const Quoted = ({ label, value }: { label: string; value: Json }) => value === undefined || value === null || value === "" ? null : <div>{label}: <q>{text(value)}</q></div>;
const Code = ({ label, value }: { label: string; value: Json }) => value === undefined || value === null || value === "" ? null : <div>{label}: <code>{text(value)}</code></div>;

/** What the request is about, read from its native parameters (§4.1 "What the person sees"). */
const fileChanges = (item: Json): Json[] => Array.isArray(item?.native?.changes) ? item.native.changes : [];
const diffBox = { ...pre, maxHeight: "24em", overflow: "auto" as const, border: "1px solid #ccc", padding: 4 };

function Subject({ request, item, place }: { request: Json; item: Json; place?: RequestPlace }) {
  const p = request?.nativeParameters ?? {};
  switch (request?.method) {
    case COMMAND:
      return <div>
        <Code label="Command" value={p.command} />
        <Code label="Working folder" value={p.cwd} />
        {p.kind && p.kind !== "command" && <Code label="Kind" value={p.kind} />}
        <Quoted label="Reason given" value={p.reason} />
        <Code label="Proposed exec-policy rule" value={p.proposedExecpolicyAmendment} />
        {(Array.isArray(p.proposedNetworkPolicyAmendments) ? p.proposedNetworkPolicyAmendments : []).map((rule: Json, i: number) => <Code key={i} label="Proposed network rule" value={rule} />)}
        <Code label="Additional permissions requested" value={p.additionalPermissions} />
      </div>;
    case FILE_CHANGE: {
      const changes = fileChanges(item);
      const cwd = typeof p.cwd === "string" && p.cwd ? p.cwd : place?.conversationFolder ?? null;
      return <div>
        <Quoted label="Reason given" value={p.reason} />
        {p.grantRoot && <div>Also asks to write under <code>{text(p.grantRoot)}</code> for the rest of the session (Codex marks this UNSTABLE).</div>}
        {changes.length === 0 ? <p>The App has not received the list of files, so it cannot show where these changes go. You can refuse, or wait for the list to appear, before allowing a change you cannot see.</p>
          : <section aria-label="Files this change writes">
            <p>Changes to {changes.length} {changes.length === 1 ? "file" : "files"}:</p>
            {changes.map((change: Json, i: number) => <div key={i}>
              <div>{text(change?.kind?.type) || "change"} <ChangeLocation path={change?.path} place={place} cwd={cwd} />
                {typeof change?.kind?.move_path === "string" && change.kind.move_path && <>; moved to <ChangeLocation path={change.kind.move_path} place={place} cwd={cwd} /></>}</div>
              <pre style={diffBox}>{text(change?.diff)}</pre>
            </div>)}
            <p><small>Locations are read from the paths Codex gave; the App has not followed links.</small></p>
            {(place?.project.kind ?? "unknown") === "unknown" && <p><small>The App has not established where your project folder is, so it cannot mark which of these are inside it.</small></p>}
          </section>}
      </div>;
    }
    case PERMISSIONS:
      return <div><Code label="Working folder" value={p.cwd} /><Quoted label="Reason given" value={p.reason} />
        <div>Requested permissions:</div><pre style={pre}>{JSON.stringify(p.permissions ?? null, null, 2)}</pre></div>;
    case LEGACY_EXEC:
      return <div><Code label="Command" value={Array.isArray(p.command) ? p.command.join(" ") : p.command} /><Code label="Working folder" value={p.cwd} /><Quoted label="Reason given" value={p.reason} /></div>;
    case LEGACY_PATCH:
      return <div><Quoted label="Reason given" value={p.reason} />{p.grantRoot && <div>Also asks to write under <code>{text(p.grantRoot)}</code> for the session.</div>}
        {Object.keys(p.fileChanges && typeof p.fileChanges === "object" ? p.fileChanges : {}).map(path => <div key={path}>File: <code>{path}</code></div>)}</div>;
    case QUESTION:
      return p.isBlocking === false ? <div>Not blocking the turn: the agent continues while this waits.</div> : null;
    case ELICITATION:
      return <div>
        <Quoted label="Message" value={p.message ?? p.description} />
        {p.mode === "url" && <div>Address (the App never opens it): <code>{text(p.url)}</code></div>}
        {p.mode === "openai/userVerification" && <div>Challenge (only you can complete it, outside this App): <code>{text(p.challenge)}</code></div>}
        {p.requestedSchema !== undefined && <details><summary>Requested fields (as Codex sent them)</summary><pre style={pre}>{JSON.stringify(p.requestedSchema, null, 2)}</pre></details>}
      </div>;
    default:
      return null;
  }
}

/** §4.7: "about: ‹item›", linking to the activity row; the supplier's identity when the row is absent. */
function About({ request, item, navigation }: { request: Json; item: Json; navigation: { open: () => void } | null }) {
  const p = request?.nativeParameters ?? {};
  if (!p.itemId) return null;
  if (item && navigation) return <div>About: <a href={`#${itemAnchorId(item.threadId, item.turnId, item.native?.id)}`} onClick={event => { event.preventDefault(); navigation.open(); }}>{text(item.native?.type) || "item"} in this conversation’s activity</a></div>;
  return <div>About: Codex item <code>{text(p.itemId)}</code> in turn <code>{text(p.turnId)}</code> (not in this view’s activity)</div>;
}

/** The activity row of the item a request is about, if this view holds it. */
export function requestItem(request: Json, view: Json): Json {
  const p = request?.nativeParameters ?? {};
  if (!sameActivityGeneration(request?.generation, view?.generation) || view?.home !== request.generation.home) return null;
  return (Array.isArray(view?.items) ? view.items : []).find((row: Json) => row?.threadId === p.threadId && row?.turnId === p.turnId && row?.native?.id === p.itemId) ?? null;
}

// Request-local drafts are disposable. Secret content is never echoed or saved.
export function NativeRequestCard({ request, view, answer, readRequest, observation, activityLink, place }: { request: Json; view?: Json; answer: RequestAnswer; readRequest?: ReadRequestCustody; observation?: RequestReplyObservation; activityLink?: RequestActivityLink; place?: RequestPlace }) {
  const [drafts, setDrafts] = useState<Record<string, string>>({});
  const [scope, setScope] = useState("turn");
  const [content, setContent] = useState("");
  const [rejection, setRejection] = useState("");
  const scopeKey = requestScopeKey(request);
  const currentScope = useRef(scopeKey);
  currentScope.current = scopeKey;
  const busyRef = useRef<{ scope: string } | null>(null);
  const [busyScope, setBusyScope] = useState<string | null>(null);
  const busy = busyScope === scopeKey;
  const [scopedError, setScopedError] = useState<{ scope: string; message: string } | null>(null);
  const setError = (message: string) => setScopedError({ scope: scopeKey, message });
  const error = scopedError?.scope === scopeKey ? scopedError.message : "";
  const [lastReply, setLastReply] = useState<RequestReplyObservation | null>(null);
  const replyRef = useRef<RequestReplyObservation | null>(null);
  if (observation?.scope === scopeKey) replyRef.current = observation;
  const observeReply = (observation: RequestReplyObservation) => { replyRef.current = observation; setLastReply(observation); };
  const reply = observation?.scope === scopeKey ? observation : lastReply?.scope === scopeKey ? lastReply : null;
  // A completed write cannot be undone by a delayed outstanding snapshot.
  // A dismissed/rejected command permits retry only after a source-bound
  // custody read reports that exact request still outstanding.
  const replyGuard = requestReplyGuarded(reply, scopeKey);
  const unreconciled = answerable(request) && replyGuard;
  const p = request.nativeParameters ?? {};
  const method = request.method;
  const send = async (value: Json) => {
    if (currentScope.current !== scopeKey || busyRef.current?.scope === scopeKey || !answerable(request) || requestReplyGuarded(replyRef.current, scopeKey)) return;
    const token = { scope: scopeKey };
    busyRef.current = token;
    setBusyScope(scopeKey); setError("");
    // Remove drafts from the rendered control before crossing the IPC boundary.
    setDrafts({}); setContent(""); setRejection("");
    try {
      let completion: ReturnType<RequestAnswer>;
      try { completion = answer(request, value); }
      finally { value = undefined; }
      const observation = await completion;
      if (currentScope.current === scopeKey && observation?.scope === scopeKey) observeReply(observation);
    } catch (e) { if (currentScope.current === scopeKey) setError(refusalWords(String(e))); }
    finally { if (busyRef.current === token) { busyRef.current = null; setBusyScope(null); } }
  };
  const reread = async () => {
    if (!readRequest || !reply || busyRef.current?.scope === scopeKey) return;
    const token = { scope: scopeKey };
    busyRef.current = token; setBusyScope(scopeKey);
    try {
      const custody = await readRequest(request);
      if (currentScope.current === scopeKey && custody.scope === scopeKey && replyRef.current?.scope === scopeKey) observeReply({ ...replyRef.current, custody });
    } catch (e) {
      if (currentScope.current === scopeKey && replyRef.current?.scope === scopeKey) observeReply({ ...replyRef.current, custody: { scope: scopeKey, available: false, reason: String(e) } });
    } finally { if (busyRef.current === token) { busyRef.current = null; setBusyScope(null); } }
  };
  const decisionButton = (decision: Json, value: Json, blocked = false) => <button key={JSON.stringify(decision)} disabled={busy || blocked} onClick={() => send(value)}>{decisionWords(decision)} <code>{JSON.stringify(decision)}</code></button>;
  const modern = method === COMMAND || method === FILE_CHANGE;
  const legacy = method === LEGACY_EXEC || method === LEGACY_PATCH;
  // DM-3: the legacy decline sends the person's reason exactly as written, "" when none.
  const rejectionRefused = rejectionProblem(rejection);
  const formButton = (form: { decision: Json; answer: Json }) => legacy && form.decision?.denied
    ? decisionButton(deniedWith(rejection).decision, deniedWith(rejection), rejectionRefused !== null)
    : decisionButton(form.decision, form.answer);
  const forms = decisionForms(request);
  const formMode = ["form", "openai/form", "openaiForm"].includes(p.mode);
  const elicitationAcceptSupported = formMode || p.mode === "url";
  const item = requestItem(request, view);
  const a14 = TOOL_PERMISSION.includes(method);
  return <article id={requestAnchorId(request.generation, request.requestIdentity)} style={{ borderTop: "1px solid #ccc", padding: 8 }}>
    <h3>{requestTitle(request)}</h3>
    <p><b>{unreconciled ? reply?.command.kind === "pending" ? "Answer command in progress" : "Current request state unavailable or not reconciled" : cardState(request)}</b>{unreconciled && <>. Last observed: {cardState(request)}</>}</p>
    {reply && <section aria-label="Native reply observation">
      <p>{replyObservationWords(reply)}</p>
      {!reply.custody.available && reply.command.kind !== "pending" && <p role="alert">Request state unavailable: {reply.custody.reason || "the original request custody could not be read"}</p>}
      {unreconciled && reply.command.kind !== "pending" && readRequest && <button disabled={busy} onClick={() => { void reread(); }}>Read current request state</button>}
    </section>}
    <About request={request} item={item} navigation={activityLink?.(request) ?? null} />
    <Subject request={request} item={item} place={place} />
    {a14 && <p>Tool permission only. Your answer decides whether Codex may use this tool; it does not mark anything checked, take the work as done, give engineering sign-off or rely on the result, and it is not recorded as a human act. <a href="#file-acts">Open the App act control</a> (a separate standing facility; nothing is filled in from this request).</p>}
    {(method === QUESTION || method === ELICITATION) && <p>Your answer goes to the agent as conversation input; it is not a recorded act. <a href="#file-acts">Open the App act control</a> (a separate standing facility; nothing is filled in from this request).</p>}
    {answerable(request) && !replyGuard && <div>
      {modern && <AnswerConsequences request={request} forms={forms} place={place} changesArrived={fileChanges(item).length > 0} />}
      {forms.map(form => modern ? <div key={JSON.stringify(form.decision)}>{formButton(form)}<DecisionNote request={request} decision={form.decision} place={place} /></div> : formButton(form))}
      {modern && forms.length === 0 && <p>This request offers no answer forms.</p>}
      {legacy && <div>
        <label>Reason for Codex with “{decisionWords("denied")}” (optional; sent exactly as written, up to {REJECTION_LIMIT} characters) <textarea {...EXACT_TEXT} disabled={busy} value={rejection} onChange={e => setRejection(e.target.value)} /></label>
        {rejectionRefused && <p role="alert">{rejectionRefused} Nothing is sent until it is changed.</p>}
      </div>}
      {method === PERMISSIONS && <>
        <label>Grant scope <select value={scope} onChange={e => setScope(e.target.value)}><option value="turn">turn</option><option value="session">session</option></select></label>
        <button disabled={busy} onClick={() => send({ permissions: p.permissions, scope })}>Grant the requested permissions</button>
        <button disabled={busy} onClick={() => send({ permissions: {}, scope })}>Grant nothing</button>
        <label>Grant part of them (native JSON) <input {...EXACT_TEXT} value={content} onChange={e => setContent(e.target.value)} /></label>
        <button disabled={busy || !content} onClick={() => { try { void send({ permissions: JSON.parse(content), scope }); } catch { setError("Invalid permission JSON"); } }}>Send partial grant…</button>
      </>}
      {method === QUESTION && <>
        {(p.questions ?? []).map((q: Json) => <div key={q.id}><p><b>{text(q.header)}</b>: {text(q.question)}</p>
          {(q.options ?? []).map((o: Json) => <button disabled={busy} key={o.label} onClick={() => setDrafts(d => ({ ...d, [q.id]: o.label }))}>{text(o.label)} · {text(o.description)}</button>)}
          {q.isOther && <label>Answer <input autoComplete="off" type={q.isSecret ? "password" : "text"} value={drafts[q.id] ?? ""} onChange={e => setDrafts(d => ({ ...d, [q.id]: e.target.value }))} /></label>}
          <button disabled={busy} onClick={() => setDrafts(d => { const next = { ...d }; delete next[q.id]; return next; })}>Leave unanswered</button>
          {!q.isOther && <p>Selected: {q.isSecret ? (drafts[q.id] ? "[masked]" : "—") : drafts[q.id] ?? "—"}</p>}
        </div>)}
        <button disabled={busy} onClick={() => send({ answers: Object.fromEntries(Object.entries(drafts).map(([id, value]) => [id, { answers: [value] }])) })}>Send current question answers…</button>
        <p>Unanswered questions are omitted; entered empty answers are preserved.</p>
        <button disabled={busy} onClick={() => send({ answers: {} })}>Decline to answer</button>
      </>}
      {method === ELICITATION && <>
        <p>Codex input mode: <code>{text(p.mode)}</code>.</p>
        {formMode && <label>Form content (JSON, masked) <input type="password" autoComplete="off" value={content} onChange={e => setContent(e.target.value)} /></label>}
        {elicitationAcceptSupported && <button disabled={busy || (formMode && !content)} onClick={() => { try { void send({ action: "accept", content: formMode ? JSON.parse(content) : null, _meta: null }); } catch { setError("Invalid native form JSON"); } }}>Send this input <code>accept</code>…</button>}
        {!elicitationAcceptSupported && <p>Sending input is not supported for this mode in this App path. Device verification requires actual device proof; this App supplies none.</p>}
        <button disabled={busy} onClick={() => send({ action: "decline", content: null, _meta: null })}>Decline <code>decline</code></button>
        <button disabled={busy} onClick={() => send({ action: "cancel", content: null, _meta: null })}>Cancel <code>cancel</code></button>
      </>}
      <p>Sending opens a native confirmation. Closing this card leaves the request waiting; the App never answers it by itself.</p>
    </div>}
    {error && <p role="alert">{error}</p>}
    <p><small>Register: state <code>{text(request.state)}</code> · reply <code>{text(request.replyWriteResult)}</code> · Codex confirmation <code>{text(request.acknowledgmentObservation?.status ?? "not-observed")}</code>{request.settlement && <> · settled by <code>{text(request.settlement.origin)}</code> as <code>{text(request.settlement.kind)}</code></>}</small></p>
    {request.closedGeneration && request.settlement && <section aria-label="Retained reply">
      <p>Prepared reply:</p>
      {request.settlement.nativeContent !== undefined && <pre style={pre}>{JSON.stringify(request.settlement.nativeContent, null, 2)}</pre>}
      {request.settlement.redaction && <p>Secret answer values are removed; the original question references are retained.</p>}
    </section>}
    <details><summary>Native request parameters and owning generation (as received)</summary><pre style={pre}>{JSON.stringify({ method, requestIdentity: request.requestIdentity, generation: request.generation, parameters: p }, null, 2)}</pre></details>
  </article>;
}

export type WaitingRequestGroup = { modeHomeClass: string; generation: Json; threadId: string | null; count: number };

/** WI-1…WI-3: local all-home metadata only; opening revalidates its native source. */
export function WaitingRequestsIndicator({ overview, busy = false, open }: { overview: Json; busy?: boolean; open: (group: WaitingRequestGroup) => void }) {
  const available = Array.isArray(overview?.groups);
  const waiting: WaitingRequestGroup[] = available ? overview.groups : [];
  const total = waiting.reduce((sum, row) => sum + row.count, 0);
  return <section aria-label="Requests waiting for your answer" style={{ border: "1px solid #888", padding: "4px 8px", margin: "8px 0" }}>
    <b>{!available ? "Waiting-request overview unavailable." : total === 0 ? "No current waiting requests observed in configured homes." : `${total} request${total === 1 ? "" : "s"} from Codex waiting for your answer`}</b>
    {waiting.map(row => <div key={JSON.stringify([row.modeHomeClass, row.generation, row.threadId])}>
      <button disabled={busy} onClick={() => open(row)}>{row.modeHomeClass} · {row.threadId ? `conversation ${row.threadId}` : "no conversation named"}: {row.count}</button>
      <small> Source: {JSON.stringify(row.generation)}.</small>
    </div>)}
    {available && <p><small>{overview.coverage} {(overview.sources ?? []).filter((source: Json) => source.state !== "ready").map((source: Json) => `${source.modeHomeClass}: ${source.state}; no current waiting groups shown. `).join("")}</small></p>}
    {total > 0 && <small> Opening shows the original home's request cards; it answers nothing and resumes no conversation.</small>}
  </section>;
}
