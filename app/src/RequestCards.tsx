import { useState } from "react";
import { itemAnchorId, requestAnchorId } from "./NativeActivity";
import { EXACT_TEXT } from "./exactText";
type Json = any; // eslint-disable-line @typescript-eslint/no-explicit-any

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
    default: return `Request from Codex the App does not answer itself (${text(request?.method) || "no method"})`;
  }
}

/** LB-1 App words for each native decision form (the value itself is shown beside them). */
export function decisionWords(decision: Json): string {
  const key = typeof decision === "string" ? decision : decision && typeof decision === "object" ? Object.keys(decision)[0] : "";
  switch (key) {
    case "accept": case "approved": return "Allow once";
    case "acceptForSession": case "approved_for_session": return "Allow for this session";
    case "acceptWithExecpolicyAmendment": case "approved_execpolicy_amendment": return "Allow, and add the proposed rule to your Codex exec policy";
    case "applyNetworkPolicyAmendment": case "network_policy_amendment": return "Apply the proposed network rule for this host";
    case "decline": return "Don't allow; the agent continues the turn";
    case "cancel": return "Don't allow, and interrupt the turn";
    case "denied": return "Don't allow; the agent tries something else";
    case "abort": return "Don't allow; the agent waits for your next message";
    default: return "Codex option";
  }
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

/** §4.4 card states, in the person's words, from the register entry. */
export function cardState(request: Json): string {
  const origin = request?.settlement?.origin;
  const confirmed = request?.acknowledgmentObservation?.status === "observed";
  const method = text(request?.method);
  switch (request?.state) {
    case "received": return "Received; not yet shown for an answer";
    case "errored": return origin?.class === "app-rule" ? `Codex asked for something the App does not provide (${method}): answered with an error by rule ${text(origin.ruleName)}` : `Unrecognized request from Codex (${method}): answered with an error`;
    case "outstanding": return "Waiting for your answer";
    case "settling": return "Sending your answer: not yet written to Codex";
    case "answered": return confirmed ? "Your answer was written; Codex reported the request resolved" : "Your answer was written to Codex; Codex has not confirmed it";
    case "declined":
      if (origin?.class === "app-rule") return `Declined by App rule ${text(origin.ruleName)}, not by you`;
      return confirmed ? "You declined; written; Codex reported the request resolved" : "You declined; written to Codex; Codex has not confirmed it";
    case "settle-write-failed": return "Your answer could not be written; whether Codex received it is unknown";
    case "resolved-by-supplier": return `Resolved by Codex before you answered (cause: ${text(request?.supplierResolution?.cause) || "not reported"})`;
    case "ended-unanswered": return "Ended unanswered: the Codex process ended";
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
function Subject({ request, item }: { request: Json; item: Json }) {
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
      const changes: Json[] = Array.isArray(item?.native?.changes) ? item.native.changes : [];
      return <div>
        <Quoted label="Reason given" value={p.reason} />
        {p.grantRoot && <div>Also asks to write under <code>{text(p.grantRoot)}</code> for the rest of the session (Codex marks this UNSTABLE).</div>}
        {changes.length === 0 ? <div>The changes are not shown here: Codex reports them on the file-change item, which this view has not received.</div>
          : changes.map((change: Json, i: number) => <details key={i}><summary>{text(change?.kind?.type) || "change"} <code>{text(change?.path)}</code></summary><pre style={pre}>{text(change?.diff)}</pre></details>)}
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
function About({ request, item }: { request: Json; item: Json }) {
  const p = request?.nativeParameters ?? {};
  if (!p.itemId) return null;
  if (item) return <div>About: <a href={`#${itemAnchorId(item.threadId, item.turnId, item.native?.id)}`}>{text(item.native?.type) || "item"} in this conversation’s activity</a></div>;
  return <div>About: Codex item <code>{text(p.itemId)}</code> in turn <code>{text(p.turnId)}</code> (not in this view’s activity)</div>;
}

/** The activity row of the item a request is about, if this view holds it. */
export function requestItem(request: Json, view: Json): Json {
  const p = request?.nativeParameters ?? {};
  return (Array.isArray(view?.items) ? view.items : []).find((row: Json) => row?.threadId === p.threadId && row?.turnId === p.turnId && row?.native?.id === p.itemId) ?? null;
}

// Request-local drafts are disposable. Secret content is never echoed or saved.
export function NativeRequestCard({ request, view, answer }: { request: Json; view?: Json; answer: (r: Json, a: Json) => Promise<void> }) {
  const [drafts, setDrafts] = useState<Record<string, string>>({});
  const [scope, setScope] = useState("turn");
  const [content, setContent] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const p = request.nativeParameters ?? {};
  const method = request.method;
  const send = async (value: Json) => {
    setBusy(true); setError("");
    // Remove drafts from the rendered control before crossing the IPC boundary.
    setDrafts({}); setContent("");
    try { await answer(request, value); } catch (e) { setError(refusalWords(String(e))); }
    finally { setBusy(false); }
  };
  const decisionButton = (decision: Json, value: Json) => <button key={JSON.stringify(decision)} disabled={busy} onClick={() => send(value)}>{decisionWords(decision)} <code>{JSON.stringify(decision)}</code></button>;
  const modern = method === COMMAND || method === FILE_CHANGE;
  const forms = decisionForms(request);
  const formMode = ["form", "openai/form", "openaiForm"].includes(p.mode);
  const elicitationAcceptSupported = formMode || p.mode === "url";
  const item = requestItem(request, view);
  const a14 = TOOL_PERMISSION.includes(method);
  return <article id={requestAnchorId(request.generation, request.requestIdentity)} style={{ borderTop: "1px solid #ccc", padding: 8 }}>
    <h3>{requestTitle(request)}</h3>
    <p><b>{cardState(request)}</b></p>
    <About request={request} item={item} />
    <Subject request={request} item={item} />
    {a14 && <p>Tool permission only. Your answer decides whether Codex may use this tool; it does not mark anything checked, take the work as done, give engineering sign-off or rely on the result, and it is not recorded as a human act. <a href="#file-acts">Open the App act control</a> (a separate standing facility; nothing is filled in from this request).</p>}
    {(method === QUESTION || method === ELICITATION) && <p>Your answer goes to the agent as conversation input; it is not a recorded act. <a href="#file-acts">Open the App act control</a> (a separate standing facility; nothing is filled in from this request).</p>}
    {answerable(request) && <div>
      {forms.map(form => decisionButton(form.decision, form.answer))}
      {modern && forms.length === 0 && <p>This request offers no answer forms.</p>}
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
    <details><summary>Native request parameters and owning generation (as received)</summary><pre style={pre}>{JSON.stringify({ method, requestIdentity: request.requestIdentity, generation: request.generation, parameters: p }, null, 2)}</pre></details>
  </article>;
}

/** WI-1…WI-3: how many supplier requests wait for the person, in which conversations. */
export function waitingByConversation(requests: Json[]): { thread: string | null; count: number }[] {
  const counts = new Map<string | null, number>();
  for (const request of Array.isArray(requests) ? requests : []) if (answerable(request)) counts.set(requestThread(request), (counts.get(requestThread(request)) ?? 0) + 1);
  return Array.from(counts.entries()).map(([thread, count]) => ({ thread, count }));
}

export function WaitingRequestsIndicator({ requests, open }: { requests: Json[]; open: (thread: string | null) => void }) {
  const waiting = waitingByConversation(requests);
  const total = waiting.reduce((sum, row) => sum + row.count, 0);
  return <section aria-label="Requests waiting for your answer" style={{ border: "1px solid #888", padding: "4px 8px", margin: "8px 0" }}>
    <b>{total === 0 ? "No requests from Codex are waiting for your answer." : `${total} request${total === 1 ? "" : "s"} from Codex waiting for your answer`}</b>
    {waiting.map(row => <span key={row.thread ?? ""}>{" · "}<button onClick={() => open(row.thread)}>{row.thread ? `conversation ${row.thread}` : "no conversation named"}: {row.count}</button></span>)}
    {total > 0 && <small> Opening a conversation shows its request cards; it answers nothing.</small>}
  </section>;
}
