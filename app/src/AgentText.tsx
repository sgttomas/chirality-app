import type { CSSProperties } from "react";
type Json = any; // eslint-disable-line @typescript-eslint/no-explicit-any

// Text the App did not write, shown so it cannot pass for the App's own words,
// a control or a request card (DEL-01-04 request cards; DEL-01-03 activity).
// Everything an agent, its tools or Codex supplies goes through AgentText: it
// sits in a bordered box with a visible label and an accessibility name that
// says whose text it is. Inside the box nothing the text contains is acted on:
// a line break in an inline value is shown as ⏎, a tab as →, and control,
// bidirectional and invisible format characters as ‹U+XXXX›. Multi-line text
// is drawn line by line inside the box, each line numbered, so no line stands
// alone outside it. The box is never a heading, button, link or list item and
// carries no role that reads as a control (it is a named group).

export type AgentTextSource = "agent" | "tool" | "person" | "codex" | "file";

/** The visible label and the accessibility name for each source of text. */
export const AGENT_TEXT_WORDS: Record<AgentTextSource, { label: string; name: string }> = {
  agent: { label: "The agent wrote:", name: "Text the agent wrote, not the App's words" },
  tool: { label: "Tool output:", name: "Output of a tool the agent called, not the App's words" },
  person: { label: "Recorded as your message:", name: "Text Codex recorded as your message, not the App's words" },
  codex: { label: "Codex sent:", name: "Text Codex sent, not the App's words" },
  file: { label: "From a file:", name: "Text from a file the App read, not the App's words" },
};

// Every character in Unicode's "Other" categories (controls, format
// characters such as direction marks, overrides, isolates, zero-width and tag
// characters, surrogates, private use, and unassigned code points) and the
// line and paragraph separators is shown as a mark, by category rather than a
// hand-kept list. A character assigned in a later Unicode version than this
// runtime knows is unassigned to it, so it is marked too. Line feeds and tabs
// have their own marks.
const MARKED = /[\p{C}\p{Zl}\p{Zp}]/u;
const SPECIAL = /(\r?\n|\t|[\p{C}\p{Zl}\p{Zp}])/u;

/** A Codex-supplied identifier (a thread's, for example) that may stand in the App's own words or in a
 * control: letters, digits and . _ : - only, at most 128 characters. Anything else is shown beside, as
 * text the App did not write. */
export const PLAIN_ID = /^[A-Za-z0-9._:-]{1,128}$/;
export const plainId = (value: unknown): string | null => typeof value === "string" && PLAIN_ID.test(value) ? value : null;
/** A Codex-supplied identifier or enum in the App's own words, where no box can stand (a control's name, an
 * attribute, a sentence the App builds as one string): as written when it is a plain identifier, "not recorded"
 * when there is none, else the App's words for one that is not (the value itself is then shown beside, boxed). */
export const idWords = (value: unknown): string => value === null || value === undefined ? "not recorded" : plainId(typeof value === "number" && Number.isSafeInteger(value) ? String(value) : value) ?? "with an identity that is not a plain identifier";
/** The App's word for a supplied value, when the value is one of the table's own keys; null for anything else.
 * The table is the App's: a const object of literal words in the caller's file (the presentation guard checks
 * this). A generated type is no guarantee at run time, so the value is checked here. */
export const wordOf = (words: Readonly<Record<string, string>>, value: unknown): string | null =>
  typeof value === "string" && Object.prototype.hasOwnProperty.call(words, value) ? words[value] : null;
/** A supplied time in seconds since the epoch, in the App's words (ISO 8601, UTC); null for anything that is not a
 * finite number giving a valid date. */
export const isoSeconds = (value: unknown): string | null => {
  if (typeof value !== "number" || !Number.isFinite(value)) return null;
  const date = new Date(value * 1000);
  return Number.isFinite(date.getTime()) ? date.toISOString() : null;
};
const pad2 = (n: number) => String(n).padStart(2, "0");
/** A time the App holds (milliseconds since the epoch), as local HH:MM:SS in the App's words; null for anything
 * that is not a finite number giving a valid date. */
export const clockWords = (at: unknown): string | null => {
  if (typeof at !== "number" || !Number.isFinite(at)) return null;
  const d = new Date(at);
  return Number.isFinite(d.getTime()) ? `${pad2(d.getHours())}:${pad2(d.getMinutes())}:${pad2(d.getSeconds())}` : null;
};
/** A supplied number in the App's words: a finite number as written, else null. */
export const numberWords = (value: unknown): string | null => typeof value === "number" && Number.isFinite(value) ? String(value) : null;

export const LINE_BREAK_MARK = "⏎";
export const TAB_MARK = "→";
const codePoint = (c: string) => `‹U+${c.codePointAt(0)!.toString(16).toUpperCase().padStart(4, "0")}›`;

/** One piece of shown text: as written, or a visible mark standing for a character that is never acted on. */
export type AgentTextPart = { text: string; mark: boolean };

/** The parts of one line (or of an inline value: its line breaks become ⏎). */
export function agentTextParts(value: string): AgentTextPart[] {
  const parts: AgentTextPart[] = [];
  for (const piece of value.split(SPECIAL)) {
    if (piece === "") continue;
    if (piece === "\n" || piece === "\r\n") parts.push({ text: LINE_BREAK_MARK, mark: true });
    else if (piece === "\t") parts.push({ text: TAB_MARK, mark: true });
    else if ([...piece].length === 1 && MARKED.test(piece)) parts.push({ text: codePoint(piece), mark: true });
    else parts.push({ text: piece, mark: false });
  }
  return parts;
}

/** The text as it is shown inline: every mark in place of what it stands for. */
export const agentTextShown = (value: string): string => agentTextParts(value).map(part => part.text).join("");

/** Structured text (indented JSON) with its own line structure kept and every other mark in place. */
export const agentTextLinesShown = (value: string): string => value.split(/\r?\n/).map(agentTextShown).join("\n");

/** A supplied value as text: strings as written, anything else as JSON (indented for multi-line display). */
export function agentTextValue(value: Json, multiline = false): string {
  if (value === null || value === undefined) return "";
  if (typeof value === "string") return value;
  try { return JSON.stringify(value, null, multiline ? 2 : undefined) ?? String(value); } catch { return String(value); }
}

const box: CSSProperties = { border: "1px dashed var(--ink-faint, #786f5f)", borderRadius: 3, background: "var(--surface, #fcfaf4)", color: "var(--ink, #29231a)" };
const inlineBox: CSSProperties = { ...box, display: "inline", padding: "0 4px", boxDecorationBreak: "clone", WebkitBoxDecorationBreak: "clone" };
const blockBox: CSSProperties = { ...box, display: "block", padding: "2px 6px", margin: "4px 0" };
const labelStyle: CSSProperties = { fontStyle: "italic", fontSize: "0.85em", color: "var(--ink-soft, #5f584a)", fontFamily: "var(--font-body, sans-serif)" };
const valueStyle: CSSProperties = { fontFamily: "var(--font-code, monospace)", whiteSpace: "pre-wrap", overflowWrap: "anywhere" };
const markStyle: CSSProperties = { color: "var(--accent, #99552f)", background: "var(--accent-soft, #f1e5d6)", borderRadius: 2, padding: "0 1px" };
const lineNumberStyle: CSSProperties = { display: "inline-block", minWidth: "2.5em", marginRight: 6, paddingRight: 4, textAlign: "right", color: "var(--ink-faint, #786f5f)", borderRight: "1px solid var(--rule-strong, #d0c8b5)", userSelect: "none" };

function Parts({ value }: { value: string }) {
  return <>{agentTextParts(value).map((part, i) => part.mark ? <span key={i} className="agent-text-mark" style={markStyle}>{part.text}</span> : part.text)}</>;
}

/**
 * A value the App did not write. `block` shows it line by line (a message,
 * plan, diff, output or JSON); otherwise it is one inline value whose line
 * breaks are shown as ⏎. `label` replaces the visible label where a shorter
 * one sits better beside a field; `name` replaces the accessibility name.
 */
export function AgentText({ value, source = "agent", label, name, block = false, style }: { value: Json; source?: AgentTextSource; label?: string; name?: string; block?: boolean; style?: CSSProperties }) {
  const words = AGENT_TEXT_WORDS[source];
  const shownLabel = label ?? words.label;
  const text = agentTextValue(value, block);
  if (!block) return <span role="group" aria-label={name ?? words.name} className="agent-text" style={{ ...inlineBox, ...style }}>
    <span className="agent-text-label" style={labelStyle}>{shownLabel}</span>{" "}
    <span className="agent-text-value" style={valueStyle}><Parts value={text} /></span>
  </span>;
  const lines = text.split(/\r?\n/);
  return <div role="group" aria-label={`${name ?? words.name}, ${lines.length} ${lines.length === 1 ? "line" : "lines"}`} className="agent-text agent-text-block" style={{ ...blockBox, ...style }}>
    <div className="agent-text-label" style={labelStyle}>{shownLabel}</div>
    <div className="agent-text-value" style={valueStyle}>
      {lines.map((line, i) => <div key={i} className="agent-text-line">
        <span className="agent-text-line-number" style={lineNumberStyle}>{i + 1}</span><Parts value={line} />{i < lines.length - 1 && <span className="agent-text-mark" style={markStyle}>{LINE_BREAK_MARK}</span>}
      </div>)}
    </div>
  </div>;
}

// The presentations a supplied value may take on a guarded view (tests/support/presentation-guard.mjs). Each
// shows the App's own words only for a value it has checked at run time, and the value itself, boxed, for
// anything else. An identifier or a number shown as written is still a supplied value: only its presentation
// is the App's.

/** A supplied identifier: as written in code type when it is a plain identifier, else boxed. */
export function SuppliedId({ value, source = "codex", label = "Identity:", name = "Identity as Codex reported it, not the App's words" }: { value: Json; source?: AgentTextSource; label?: string; name?: string }) {
  const plain = plainId(typeof value === "number" && Number.isSafeInteger(value) ? String(value) : value);
  if (value === null || value === undefined) return <i>not recorded</i>;
  return plain !== null ? <code>{plain}</code> : <AgentText value={value} source={source} label={label} name={name} />;
}
/** A supplied value from a closed vocabulary: the App's word when the value is one of the table's keys, else boxed. */
export function Word({ value, words, source = "codex", label = "Codex sent:", name = "A value Codex sent that the App does not recognise, not the App's words" }: { value: Json; words: Readonly<Record<string, string>>; source?: AgentTextSource; label?: string; name?: string }) {
  const word = wordOf(words, value);
  if (value === null || value === undefined) return <i>not recorded</i>;
  return word !== null ? <>{word}</> : <AgentText value={value} source={source} label={label} name={name} />;
}
/** A supplied number: as written when it is a finite number, else boxed. */
export function Num({ value, source = "codex", label = "Codex sent:", name = "A value Codex sent where a number was expected, not the App's words" }: { value: Json; source?: AgentTextSource; label?: string; name?: string }) {
  const shown = numberWords(value);
  if (value === null || value === undefined) return <i>not recorded</i>;
  return shown !== null ? <>{shown}</> : <AgentText value={value} source={source} label={label} name={name} />;
}
/** A supplied boolean in the App's words, else boxed. */
export function Flag({ value, yes, no, source = "codex", label = "Codex sent:", name = "A value Codex sent where yes or no was expected, not the App's words" }: { value: Json; yes: string; no: string; source?: AgentTextSource; label?: string; name?: string }) {
  if (value === null || value === undefined) return <i>not recorded</i>;
  return value === true ? <>{yes}</> : value === false ? <>{no}</> : <AgentText value={value} source={source} label={label} name={name} />;
}
