import { useCallback, useRef, useState } from "react";
import { invoke } from "./hostReads";

type Json = any; // eslint-disable-line @typescript-eslint/no-explicit-any
const text = (value: Json): string => (typeof value === "string" ? value : "");

/** The host's read of a workflow's own text (`workflow_read_text`). */
export const READ_TEXT = "workflow_read_text";

const IDENTITY_FIELDS = ["kind", "origin", "source_root", "name", "revision", "revision_method"];
/**
 * A text is held against the whole source-qualified identity it was read for,
 * as the host gives it. An identity missing any field holds nothing.
 */
export function identityKey(identity: Json): string | null {
  if (!identity || typeof identity !== "object") return null;
  if (!IDENTITY_FIELDS.every(field => typeof identity[field] === "string" && identity[field] !== "")) return null;
  return JSON.stringify(IDENTITY_FIELDS.map(field => identity[field]));
}

/** One read, held for one place in the guide and the identity it was read for. */
export type HeldText =
  | { key: string; state: "reading" }
  | { key: string; state: "read"; identity: Json; text: string; bytes: number; files: { path: string; bytes: number }[] }
  | { key: string; state: "refused"; reason: string; cause: string };

const NOT_CURRENT = "this view is out of date, so nothing was read. Read it again once the view has refreshed";

/**
 * What the host's reply establishes, and nothing more. Text is held only for a
 * read whose bytes the host tied to the identity that was asked for; any other
 * reply is a refusal, in the host's words where it gave them.
 */
export function heldFromReply(key: string, reply: Json): HeldText {
  if (reply?.state === "read") {
    if (reply.matched !== true || typeof reply.text !== "string") return { key, state: "refused", reason: "the App's reply did not say that the text matched this revision, so it is not shown", cause: "" };
    if (identityKey(reply.identity) !== key) return { key, state: "refused", reason: "the App's reply was for another workflow or revision than the one shown here, so it is not shown", cause: "" };
    const files = (Array.isArray(reply.files) ? reply.files : []).filter((file: Json) => typeof file?.path === "string" && Number.isInteger(file?.bytes))
      .map((file: Json) => ({ path: file.path as string, bytes: file.bytes as number }));
    return { key, state: "read", identity: reply.identity, text: reply.text, bytes: Number.isInteger(reply.bytes) ? reply.bytes : new TextEncoder().encode(reply.text).length, files };
  }
  if (reply?.state === "refused" && typeof reply.reason === "string" && reply.reason) return { key, state: "refused", reason: reply.reason, cause: text(reply.cause) };
  return { key, state: "refused", reason: "the App's reply could not be read", cause: "" };
}

export type WorkflowTexts = {
  held: Record<string, HeldText>;
  /** Read the text for `slot`, for the identity shown there. `context` is the displayed workflow context, or undefined when the view is not current. */
  read: (slot: string, identity: Json, target: Record<string, unknown>, context: Json) => void;
  hide: (slot: string) => void;
  /** The text held for `slot` when it was read for exactly this identity. */
  of: (slot: string, identity: Json) => HeldText | undefined;
};

/**
 * The texts a person asked to read, held by the guide itself so that they are
 * still there when its steps come back after the status read that follows the
 * press. A reply applies only to the latest read of its place, and is shown
 * only while that place shows the identity it was read for.
 */
export function useWorkflowTexts(): WorkflowTexts {
  const [held, setHeld] = useState<Record<string, HeldText>>({});
  const issued = useRef<Record<string, number>>({});
  const read = useCallback((slot: string, identity: Json, target: Record<string, unknown>, context: Json) => {
    const key = identityKey(identity);
    if (!key) return;
    const n = (issued.current[slot] ?? 0) + 1;
    issued.current[slot] = n;
    const settle = (next: HeldText) => { if (issued.current[slot] === n) setHeld(old => ({ ...old, [slot]: next })); };
    if (!context) { settle({ key, state: "refused", reason: NOT_CURRENT, cause: "" }); return; }
    settle({ key, state: "reading" });
    invoke<Json>(READ_TEXT, { target, context }).then(reply => settle(heldFromReply(key, reply)),
      error => settle({ key, state: "refused", reason: String(error).replace(/^Error: /, ""), cause: "" }));
  }, []);
  const hide = useCallback((slot: string) => {
    issued.current[slot] = (issued.current[slot] ?? 0) + 1;
    setHeld(old => { const next = { ...old }; delete next[slot]; return next; });
  }, []);
  const of = useCallback((slot: string, identity: Json) => {
    const found = held[slot], key = identityKey(identity);
    return found && key && found.key === key ? found : undefined;
  }, [held]);
  return { held, read, hide, of };
}

const size = (bytes: number) => (bytes === 1 ? "1 byte" : `${bytes} bytes`);

/**
 * The control to read one workflow's own text, and the text once read. The
 * words around the text say which revision it is and that its files matched
 * that revision when read, and nothing else: not what the workflow needs, not
 * whether anything it names is present, not whether it will work, and no
 * account of what the text says. The text itself is shown exactly as read.
 */
export function WorkflowTextControl({ slot, identity, target, context, source, texts, disabled }: {
  slot: string; identity: Json; target: Record<string, unknown>; context: () => Json; source: string; texts: WorkflowTexts; disabled: boolean;
}) {
  const key = identityKey(identity);
  if (!key) return null;
  const name = text(identity.name), revision = text(identity.revision);
  const current = texts.of(slot, identity);
  const earlier = !current && texts.held[slot] !== undefined && texts.held[slot].state !== "reading";
  const read = () => texts.read(slot, identity, target, context());
  if (!current) return <div aria-label={`Text of ${name}`}>
    {earlier && <p><small>The text read earlier here was of another workflow or revision; it is not shown.</small></p>}
    <button disabled={disabled} onClick={read}>Read {name}'s text</button>
  </div>;
  if (current.state === "reading") return <div aria-label={`Text of ${name}`}>
    <button disabled>Reading {name}'s text…</button>
  </div>;
  if (current.state === "refused") return <div aria-label={`Text of ${name}`}>
    <p role="alert">The App did not show {name}'s text: {current.reason}.</p>
    {current.cause && <details><summary>What the App reported</summary><pre style={{ whiteSpace: "pre-wrap" }}>{current.cause}</pre></details>}
    <button disabled={disabled} onClick={read}>Read {name}'s text again</button>{" "}
    <button onClick={() => texts.hide(slot)}>Dismiss</button>
  </div>;
  return <div aria-label={`Text of ${name}`}>
    <p aria-label={`What this text is`}>The <code>WORKFLOW.md</code> of <strong>{name}</strong>{source ? ` — ${source}` : ""}, revision <code title={revision}>{revision.slice(0, 12)}…</code>, as the App read it when you asked ({size(current.bytes)}). Its files matched this revision when they were read. Shown exactly as read.</p>
    <pre aria-label={`${name} WORKFLOW.md`} tabIndex={0} style={{ whiteSpace: "pre-wrap", overflowWrap: "anywhere", maxHeight: "28em", overflow: "auto" }}>{current.text}</pre>
    {current.files.length > 0 && <details><summary>This revision's other {current.files.length === 1 ? "file" : `${current.files.length} files`}</summary>
      <ul>{current.files.map(file => <li key={file.path}><code>{file.path}</code> ({size(file.bytes)})</li>)}</ul>
    </details>}
    <button onClick={() => texts.hide(slot)}>Hide {name}'s text</button>
  </div>;
}
