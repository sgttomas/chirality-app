import { useEffect, useRef, useState } from "react";
import { AgentText, idWords } from "./AgentText";
import { reviewDigest } from "./presentation";
type Json = any; // eslint-disable-line @typescript-eslint/no-explicit-any

// DEL-01-04 REQ-001/AC-001: the request and answer details a native answer
// confirmation names by digest, shown at the request's card. Each row is the
// host's frozen snapshot, taken when that confirmation opened
// (request_answer_companions): it is kept after the confirmation's Cancel,
// never refreshed in place, and a later confirmation whose details differ
// names its own snapshot by another digest. Nothing here records or claims
// that the person read or understood the details. The page does not
// establish whether this card can be read while a native confirmation is
// open; the native confirmation itself tells the person to cancel, read and
// answer again if they cannot read it then.

/** One snapshot as the host returns it. `content` is the typed envelope the digest is taken over. */
export type CompanionRow = { generation: Json; requestIdentity: Json; digest: string; content: Json; pending: boolean };
export type ReadCompanions = (generation: Json, requestId: Json) => Promise<CompanionRow[]>;

/** The requests whose confirmations name a companion (request_answer_presentation.rs `supported`). */
export const COMPANION_METHODS = [
  "item/commandExecution/requestApproval", "item/fileChange/requestApproval", "execCommandApproval", "applyPatchApproval", "item/tool/requestUserInput",
];
/** How often a card with a waiting request asks for its snapshots, in milliseconds. */
export const COMPANION_POLL_MS = 1000;

/** The typed encoding (request_answer_presentation.rs `typed`): every JSON value names its type, and a number
 * keeps its JSON spelling as text, so 0.5, "0.5" and {"number":"0.5"} stay three different values. */
export type Typed =
  | { type: "null" }
  | { type: "boolean"; value: boolean }
  | { type: "number"; value: string }
  | { type: "string"; value: string }
  | { type: "array"; value: Typed[] }
  | { type: "object"; value: [string, Typed][] };
const JSON_NUMBER = /^-?(0|[1-9]\d*)(\.\d+)?([eE][+-]?\d+)?$/;
// The supplier JSON decoder admits up to 128 levels; the frozen envelope
// adds context and presentation wrappers. Do not reject its admitted values.
const MAX_DEPTH = 256;
const plainObject = (v: Json) => v !== null && typeof v === "object" && !Array.isArray(v);
const exactKeys = (v: Json, keys: string[]) => plainObject(v) && Object.keys(v).length === keys.length && keys.every(k => Object.prototype.hasOwnProperty.call(v, k));

/** Whether a value is exactly the typed encoding: no other members, a number's spelling valid JSON, an object's
 * keys unique. Anything else is refused whole, so nothing is shown in a form it was not given in. */
export function isTyped(v: Json, depth = 0): v is Typed {
  if (depth > MAX_DEPTH || !plainObject(v)) return false;
  switch (v.type) {
    case "null": return exactKeys(v, ["type"]);
    case "boolean": return exactKeys(v, ["type", "value"]) && typeof v.value === "boolean";
    case "number": return exactKeys(v, ["type", "value"]) && typeof v.value === "string" && JSON_NUMBER.test(v.value);
    case "string": return exactKeys(v, ["type", "value"]) && typeof v.value === "string";
    case "array": return exactKeys(v, ["type", "value"]) && Array.isArray(v.value) && v.value.every((x: Json) => isTyped(x, depth + 1));
    case "object": {
      if (!exactKeys(v, ["type", "value"]) || !Array.isArray(v.value)) return false;
      const seen = new Set<string>();
      for (const entry of v.value) {
        if (!Array.isArray(entry) || entry.length !== 2 || typeof entry[0] !== "string" || seen.has(entry[0]) || !isTyped(entry[1], depth + 1)) return false;
        seen.add(entry[0]);
      }
      return true;
    }
    default: return false;
  }
}

/** A typed value as JSON text, indented, with each number exactly as spelled and object members in their order. */
export function typedJsonText(t: Typed, indent = 0): string {
  const pad = (n: number) => "  ".repeat(n);
  switch (t.type) {
    case "null": return "null";
    case "boolean": return t.value ? "true" : "false";
    case "number": return t.value;
    case "string": return JSON.stringify(t.value);
    case "array": return t.value.length === 0 ? "[]" : `[\n${t.value.map(x => pad(indent + 1) + typedJsonText(x, indent + 1)).join(",\n")}\n${pad(indent)}]`;
    case "object": return t.value.length === 0 ? "{}" : `{\n${t.value.map(([k, x]) => `${pad(indent + 1)}${JSON.stringify(k)}: ${typedJsonText(x, indent + 1)}`).join(",\n")}\n${pad(indent)}}`;
  }
}

const member = (t: Typed | undefined, key: string): Typed | undefined => t?.type === "object" ? t.value.find(([k]) => k === key)?.[1] : undefined;
const stringOf = (t: Typed | undefined): string | null => t?.type === "string" ? t.value : null;
// A sentence or label the host composed: one line of printable text. A value from Codex or the person is never read this way.
const APP_LINE = /^[^\p{C}\p{Zl}\p{Zp}]{1,2000}$/u;
const appLine = (t: Typed | undefined): string | null => { const s = stringOf(t); return s !== null && APP_LINE.test(s) ? s : null; };
const appLines = (t: Typed | undefined): string[] | null => {
  if (t?.type !== "array") return null;
  const lines = t.value.map(appLine);
  return lines.every((l): l is string => l !== null) ? lines : null;
};

export type CompanionDetail = { label: string; source: "codex" | "person"; value: Typed; notes: string[] };
export type CompanionEnvelope = { context: Typed; answer: Typed; head: string[]; details: CompanionDetail[]; itemCount: string };

/** The envelope's parts, or null when it is not exactly request-answer/1 in the typed encoding. */
export function readEnvelope(content: Json): CompanionEnvelope | null {
  if (!isTyped(content) || content.type !== "object") return null;
  if (stringOf(member(content, "schema")) !== "request-answer/1") return null;
  const context = member(content, "context"), answer = member(content, "answer"), presentation = member(content, "presentation");
  if (!context || !answer || presentation?.type !== "object") return null;
  const head = appLines(member(presentation, "head"));
  const count = member(presentation, "itemCount");
  const rawDetails = member(presentation, "details");
  if (head === null || count?.type !== "number" || !/^(0|[1-9]\d*)$/.test(count.value) || rawDetails?.type !== "array") return null;
  const details: CompanionDetail[] = [];
  for (const d of rawDetails.value) {
    const label = appLine(member(d, "label")), source = stringOf(member(d, "source")), value = member(d, "value"), notes = appLines(member(d, "notes"));
    if (label === null || (source !== "codex" && source !== "person") || !value || notes === null) return null;
    details.push({ label, source, value, notes });
  }
  return { context, answer, head, details, itemCount: count.value };
}

/** A location the host resolved (request_answer_sheet.rs `location`): the full path, and the folder a relative
 * path was resolved against, or null. Exactly those two members, or it is not read as one. */
function locationPair(t: Typed): { path: string; relativeTo: string | null } | null {
  if (t.type !== "object" || t.value.length !== 2) return null;
  const path = member(t, "path"), base = member(t, "relativeTo");
  if (path?.type !== "string" || !(base?.type === "string" || base?.type === "null")) return null;
  return { path: path.value, relativeTo: base.type === "string" ? base.value : null };
}

/** A detail's value: text as written, a resolved location as its two parts, or any other value as JSON with its
 * numbers as spelled; the label says which. */
function DetailValue({ detail }: { detail: CompanionDetail }) {
  const location = detail.label === "Path" ? locationPair(detail.value) : null;
  if (location) return detail.source === "codex" ? <>
    <AgentText block value={location.path} source="codex" label="Full path, resolved by name from Codex’s words (no link followed):" name="Codex's words, not the App's" />
    {location.relativeTo !== null && <AgentText block value={location.relativeTo} source="codex" label="Codex gave a relative path; the folder it was resolved against (Codex’s words):" name="Codex's words, not the App's" />}
  </> : <AgentText block value={typedJsonText(detail.value)} source="person" label="Your words, as you wrote them (JSON):" name="Your words, as you wrote them, not the App's" />;
  const text = detail.value.type === "string" ? detail.value.value : null;
  if (detail.source === "codex") return text !== null
    ? <AgentText block value={text} source="codex" label="Codex’s words, not the App’s (text):" name="Codex's words, not the App's" />
    : <AgentText block value={typedJsonText(detail.value)} source="codex" label="Codex’s words, not the App’s (JSON, exactly as sent):" name="Codex's words, not the App's" />;
  return text !== null
    ? <AgentText block value={text} source="person" label="Your words, as you wrote them (text):" name="Your words, as you wrote them, not the App's" />
    : <AgentText block value={typedJsonText(detail.value)} source="person" label="Your words, as you wrote them (JSON):" name="Your words, as you wrote them, not the App's" />;
}

type Check = "checking" | "same" | "different" | { unavailable: string };
type Held = { row: CompanionRow; check: Check };
const sameJson = (a: Json, b: Json) => JSON.stringify(a) === JSON.stringify(b);

function Snapshot({ held }: { held: Held }) {
  const { row, check } = held;
  const envelope = check === "same" ? readEnvelope(row.content) : null;
  return <article aria-label="Request and answer details named by a native confirmation" style={{ border: "1px solid #a60", padding: 8, margin: "8px 0" }}>
    <p>sha-256 digest, as named in the native confirmation: <code style={{ userSelect: "all", overflowWrap: "anywhere" }}>{idWords(row.digest) ?? "unavailable"}</code>.{" "}
      {check === "checking" ? "This view is recomputing the digest from the details below; they are shown once it matches."
        : check === "same" ? "This view recomputed the same digest from the details below."
        : check === "different" ? "This view recomputed a different digest: do not rely on these details. They are not shown."
        : "This view cannot recompute the digest, so the details are not shown."}</p>
    {typeof check === "object" && <AgentText block value={check.unavailable} source="record" label="Reported digest-check error:" />}
    <p>{row.pending
      ? "The native confirmation that names these details is open. They are the details as they were when it opened."
      : "The native confirmation that named these details has closed. They are kept here as they were when it opened, and they are not refreshed. If you cancelled it, you can read them here and answer again from this card; a new confirmation takes the details again, and if they have changed it names them by a new digest."}</p>
    {check === "same" && envelope === null && <p role="alert">These details are not in the form this App reads, so they are not shown. Do not rely on the confirmation that names them; cancel it and answer again from this card.</p>}
    {envelope && <>
      <p>The request and answer details: {envelope.itemCount} {envelope.itemCount === "1" ? "item" : "items"}.</p>
      {envelope.head.map((line, i) => <p key={`head:${i}`}>{line}</p>)}
      {envelope.details.map((detail, i) => <section key={`detail:${i}`} aria-label="One of the request and answer details">
        <p><b>{detail.label}</b></p>
        <DetailValue detail={detail} />
        {detail.notes.map((note, j) => <p key={`note:${j}`}><small>{note}</small></p>)}
      </section>)}
      <details><summary>What this confirmation was bound to, and the answer it would send (secret values masked by the host)</summary>
        <AgentText block value={typedJsonText(envelope.context)} source="record" label="The request, its conversation and its place, as bound (JSON, numbers as sent):" name="The context the confirmation was bound to, as the host recorded it; it holds Codex's words, not only the App's" />
        <AgentText block value={typedJsonText(envelope.answer)} source="record" label="The answer, as it would be sent, secret values masked (JSON):" name="The answer the confirmation would send, as the host recorded it, with secret values masked" />
      </details>
    </>}
  </article>;
}

/** The frozen snapshots for one request, at its card. It asks the host while mounted: every second while the
 * request waits, and at once whenever `refresh` changes (an answer command's outcome, such as the confirmation's
 * Cancel), so a cancelled confirmation's snapshot appears here without the native confirmation open. A digest
 * already held keeps the content first received under it; nothing is replaced in place. */
export function RequestAnswerCompanion({ request, read, refresh }: { request: Json; read: ReadCompanions; refresh?: unknown }) {
  const [held, setHeld] = useState<Held[]>([]);
  const heldRef = useRef<Held[]>([]);
  const supported = COMPANION_METHODS.includes(request?.method);
  const scope = JSON.stringify([request?.generation, typeof request?.requestIdentity, request?.requestIdentity]);
  const waiting = request?.state === "outstanding";
  useEffect(() => { heldRef.current = []; setHeld([]); }, [scope]);
  useEffect(() => {
    if (!supported) return;
    let live = true;
    const poll = async () => {
      let rows: CompanionRow[];
      try { rows = await read(request.generation, request.requestIdentity); } catch { return; }
      if (!live || !Array.isArray(rows)) return;
      const mine = rows.filter(r => r && typeof r.digest === "string" && sameJson(r.generation, request.generation) && sameJson(r.requestIdentity, request.requestIdentity));
      const previous = heldRef.current;
      const next: Held[] = mine.map(r => {
        const kept = previous.find(h => h.row.digest === r.digest);
        return kept ? { ...kept, row: { ...kept.row, pending: r.pending === true } } : { row: { ...r, pending: r.pending === true }, check: "checking" };
      });
      heldRef.current = next; setHeld(next);
      for (const h of next.filter(h => h.check === "checking")) {
        let check: Check;
        try { check = (await reviewDigest(h.row.content)) === h.row.digest ? "same" : "different"; }
        catch (e) { check = { unavailable: e instanceof Error ? e.message : String(e) }; }
        if (!live) return;
        heldRef.current = heldRef.current.map(x => x.row.digest === h.row.digest && x.check === "checking" ? { ...x, check } : x);
        setHeld(heldRef.current);
      }
    };
    void poll();
    const timer = waiting ? setInterval(() => { void poll(); }, COMPANION_POLL_MS) : null;
    return () => { live = false; if (timer) clearInterval(timer); };
  }, [scope, supported, waiting, refresh, read]); // eslint-disable-line react-hooks/exhaustive-deps
  if (!supported || held.length === 0) return null;
  return <section role="region" aria-label="Details named by native confirmations for this request">
    <h4>Details named by a native confirmation for this request</h4>
    {held.map(h => <Snapshot key={h.row.digest} held={h} />)}
  </section>;
}
