import { Fragment, type CSSProperties } from "react";
import { THREAD_STATUS } from "./nativeWords";
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

export type AgentTextSource = "agent" | "tool" | "person" | "codex" | "file" | "record";

/** The visible label and the accessibility name for each source of text. */
export const AGENT_TEXT_WORDS: Record<AgentTextSource, { label: string; name: string }> = {
  agent: { label: "The agent wrote:", name: "Text the agent wrote, not the App's words" },
  tool: { label: "Tool output:", name: "Output of a tool the agent called, not the App's words" },
  person: { label: "Recorded as your message:", name: "Text Codex recorded as your message, not the App's words" },
  codex: { label: "Codex sent:", name: "Text Codex sent, not the App's words" },
  file: { label: "From a file:", name: "Text from a file the App read, not the App's words" },
  // A record or report the App keeps or received. It may hold values the App did not write (an agent's, a tool's,
  // a file's or Codex's), so it is shown marked; its plain label is true of App-only and mixed records alike.
  record: { label: "Recorded text:", name: "Recorded text" },
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
/** The App's own workflow-name rule (workflow_workspace::valid_name): lowercase letters, digits and single hyphens,
 * at most 64 characters. A name from a file an agent may have written stands in the App's words only in this form. */
export const SAFE_WORKFLOW_NAME = /^[a-z0-9]+(-[a-z0-9]+)*$/;
export const safeName = (value: unknown): string => typeof value === "string" && value.length <= 64 && SAFE_WORKFLOW_NAME.test(value) ? value : "a workflow whose name is shown beside";
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
export function AgentText({ value, source = "agent", label, name, block = false, style, tabIndex, exactLineEnds = false, alreadyMarkedByHost = false }: { value: Json; source?: AgentTextSource; label?: string; name?: string; block?: boolean; style?: CSSProperties; tabIndex?: number;
  /** For a view that shows exact bytes: lines break only at a line feed, so a carriage return stays visible as a mark. */
  exactLineEnds?: boolean;
  /** Block-only: the native host has already marked this statement and bound its exact text by digest.
   * Keep its characters verbatim inside the supplied-text wrapper; never use for raw package/record values. */
  alreadyMarkedByHost?: boolean }) {
  const words = AGENT_TEXT_WORDS[source];
  const shownLabel = label ?? words.label;
  const text = agentTextValue(value, block);
  if (!block) return <span role="group" aria-label={name ?? words.name} className="agent-text" style={{ ...inlineBox, ...style }}>
    <span className="agent-text-label" style={labelStyle}>{shownLabel}</span>{" "}
    <span className="agent-text-value" style={valueStyle}><Parts value={text} /></span>
  </span>;
  const lines = text.split(exactLineEnds || alreadyMarkedByHost ? /\n/ : /\r?\n/);
  return <div role="group" aria-label={`${name ?? words.name}, ${lines.length} ${lines.length === 1 ? "line" : "lines"}`} className="agent-text agent-text-block" style={{ ...blockBox, ...style }} tabIndex={tabIndex}>
    <div className="agent-text-label" style={labelStyle}>{shownLabel}</div>
    <div className="agent-text-value" style={valueStyle}>
      {lines.map((line, i) => <div key={i} className="agent-text-line">
        <span className="agent-text-line-number" style={lineNumberStyle}>{i + 1}</span>{alreadyMarkedByHost ? line : <Parts value={line} />}{i < lines.length - 1 && <span className="agent-text-mark" style={markStyle}>{LINE_BREAK_MARK}</span>}
      </div>)}
    </div>
  </div>;
}

// ---- The agent's prose ----
// An agent's message in the conversation, formatted: paragraphs, emphasis and strong, ordered and unordered lists,
// headings (drawn as a small bold line, never as a heading element), inline and fenced code, block quotes, tables
// and a thematic break. Nothing else is interpreted. A link is drawn as its text followed by its target in plain
// text, and is not a link; an image and raw HTML are drawn as their source text. Every character in Unicode's
// "Other" categories and the line and paragraph separators is drawn as a visible mark, as in AgentText. The output
// holds only p, br, strong, em, code, pre, ul, ol, li, blockquote, table, thead, tbody, tr, td, hr and span
// elements: never a heading, button, link, form control, details element or image, never an element with a role
// (other than the one named group around it), an id, a class taken from the text, or an event handler. The group's
// accessibility name says whose text it is; the conversation shows the speaker's label above it.

/** One piece of inline prose. */
export type ProseInline =
  | { kind: "text"; text: string }
  | { kind: "code"; text: string }
  | { kind: "em"; children: ProseInline[] }
  | { kind: "strong"; children: ProseInline[] }
  | { kind: "link"; children: ProseInline[]; target: string };
/** One block of prose. */
export type ProseBlock =
  | { kind: "paragraph"; lines: ProseInline[][] }
  | { kind: "heading"; level: number; content: ProseInline[] }
  | { kind: "list"; ordered: boolean; start: number; items: ProseBlock[][] }
  | { kind: "code"; text: string }
  | { kind: "quote"; blocks: ProseBlock[] }
  | { kind: "table"; header: ProseInline[][]; rows: ProseInline[][][] }
  | { kind: "rule" };

const ESCAPABLE = /[!"#$%&'()*+,\-./:;<=>?@[\\\]^_`{|}~]/;
const WORD_CHAR = /[\p{L}\p{N}]/u;

/** Inline prose: code spans, links (drawn as text and target), emphasis and strong; everything else is text. */
export function proseInlines(source: string): ProseInline[] {
  const out: ProseInline[] = [];
  let text = "";
  const flush = () => { if (text) { out.push({ kind: "text", text }); text = ""; } };
  let i = 0;
  while (i < source.length) {
    const c = source[i];
    if (c === "\\" && i + 1 < source.length && ESCAPABLE.test(source[i + 1])) { text += source[i + 1]; i += 2; continue; }
    if (c === "`") {
      let n = 0;
      while (source[i + n] === "`") n++;
      const fence = "`".repeat(n);
      let close = source.indexOf(fence, i + n);
      while (close !== -1 && source[close + n] === "`") { let m = close; while (source[m] === "`") m++; close = source.indexOf(fence, m); }
      if (close === -1) { text += fence; i += n; continue; }
      let inner = source.slice(i + n, close);
      if (inner.length > 1 && inner.startsWith(" ") && inner.endsWith(" ") && inner.trim() !== "") inner = inner.slice(1, -1);
      flush(); out.push({ kind: "code", text: inner }); i = close + n; continue;
    }
    if (c === "!" && source[i + 1] === "[") {
      // An image is drawn as its source text, so its label is never read as a link.
      const image = /^!\[[^\]\n]*\]\([^)\n]*\)/.exec(source.slice(i));
      if (image) { text += image[0]; i += image[0].length; continue; }
    }
    if (c === "[") {
      const link = /^\[((?:\\.|[^\]\\\n])+)\]\(\s*<?([^\s()<>]+)>?(?:\s+"[^"\n]*")?\s*\)/.exec(source.slice(i));
      if (link) { flush(); out.push({ kind: "link", children: proseInlines(link[1]), target: link[2] }); i += link[0].length; continue; }
    }
    if (c === "<") {
      const auto = /^<((?:https?|mailto|ftp):[^\s<>]+)>/i.exec(source.slice(i));
      if (auto) { flush(); out.push({ kind: "link", children: [{ kind: "text", text: auto[1] }], target: auto[1] }); i += auto[0].length; continue; }
    }
    if (c === "*" || c === "_") {
      const double = source[i + 1] === c;
      const marker = double ? c + c : c;
      const before = i > 0 ? source[i - 1] : "";
      const after = source[i + marker.length] ?? "";
      const opens = after !== "" && !/\s/.test(after) && !(c === "_" && WORD_CHAR.test(before));
      if (opens) {
        let close = -1;
        for (let j = i + marker.length + 1; j <= source.length - marker.length; j++) {
          if (source.startsWith(marker, j) && !/\s/.test(source[j - 1]) && (double || source[j + 1] !== c) && (double || source[j - 1] !== c)
            && !(c === "_" && WORD_CHAR.test(source[j + marker.length] ?? ""))) { close = j; break; }
          if (source[j] === "`") { const end = source.indexOf("`", j + 1); if (end !== -1) j = end; }
        }
        if (close !== -1) {
          flush();
          const children = proseInlines(source.slice(i + marker.length, close));
          out.push(double ? { kind: "strong", children } : { kind: "em", children });
          i = close + marker.length; continue;
        }
      }
      text += marker; i += marker.length; continue;
    }
    text += c; i++;
  }
  flush();
  return out;
}

const FENCE = /^( {0,3})(`{3,}|~{3,})(.*)$/;
const ATX = /^ {0,3}(#{1,6})(?:[ \t]+(.*?))?(?:[ \t]+#+)?[ \t]*$/;
const RULE = /^ {0,3}([-*_])(?:[ \t]*\1){2,}[ \t]*$/;
const QUOTE = /^ {0,3}> ?(.*)$/;
const ITEM = /^( {0,3})([-*+]|\d{1,9}[.)])([ \t]+(.*))?$/;
const TABLE_RULE = /^ {0,3}\|?[ \t]*:?-+:?[ \t]*(\|[ \t]*:?-+:?[ \t]*)*\|?[ \t]*$/;
const SETEXT = /^ {0,3}(=+|-+)[ \t]*$/;
const blank = (line: string) => line.trim() === "";
const cells = (line: string) => {
  let row = line.trim();
  if (row.startsWith("|")) row = row.slice(1);
  if (row.endsWith("|") && !row.endsWith("\\|")) row = row.slice(0, -1);
  return row.split(/(?<!\\)\|/).map(cell => proseInlines(cell.trim().replace(/\\\|/g, "|")));
};
const startsBlock = (line: string, next: string | undefined) => FENCE.test(line) || ATX.test(line) || RULE.test(line) || QUOTE.test(line) || ITEM.test(line)
  || (line.includes("|") && next !== undefined && TABLE_RULE.test(next) && next.includes("-"));

/** Prose blocks from the agent's text. Lines are split at line feeds; a carriage return before one is dropped. */
export function proseBlocks(source: string): ProseBlock[] {
  return blocksOf(source.split(/\r?\n/));
}
function blocksOf(lines: string[]): ProseBlock[] {
  const blocks: ProseBlock[] = [];
  let i = 0;
  while (i < lines.length) {
    const line = lines[i];
    if (blank(line)) { i++; continue; }
    const fence = FENCE.exec(line);
    if (fence && !(fence[2][0] === "`" && fence[3].includes("`"))) {
      const indent = fence[1].length, mark = fence[2];
      const body: string[] = [];
      i++;
      while (i < lines.length && !new RegExp(`^ {0,3}${mark[0] === "`" ? "`" : "~"}{${mark.length},}[ \\t]*$`).test(lines[i])) {
        body.push(lines[i].replace(new RegExp(`^ {0,${indent}}`), ""));
        i++;
      }
      i++;
      blocks.push({ kind: "code", text: body.join("\n") });
      continue;
    }
    const atx = ATX.exec(line);
    if (atx) { blocks.push({ kind: "heading", level: atx[1].length, content: proseInlines(atx[2] ?? "") }); i++; continue; }
    if (RULE.test(line)) { blocks.push({ kind: "rule" }); i++; continue; }
    if (QUOTE.test(line)) {
      const inner: string[] = [];
      while (i < lines.length && !blank(lines[i]) && (QUOTE.test(lines[i]) || inner.length > 0 && !startsBlock(lines[i], lines[i + 1]))) {
        const quoted = QUOTE.exec(lines[i]);
        inner.push(quoted ? quoted[1] : lines[i]);
        i++;
      }
      blocks.push({ kind: "quote", blocks: blocksOf(inner) });
      continue;
    }
    const item = ITEM.exec(line);
    if (item) {
      const ordered = /\d/.test(item[2]);
      const start = ordered ? Number.parseInt(item[2], 10) : 1;
      const items: ProseBlock[][] = [];
      while (i < lines.length) {
        const current = ITEM.exec(lines[i]);
        if (!current || /\d/.test(current[2]) !== ordered) break;
        const contentIndent = current[1].length + current[2].length + Math.max(1, Math.min(4, (current[3] ?? " ").length - (current[4] ?? "").length));
        const body: string[] = [current[4] ?? ""];
        i++;
        while (i < lines.length) {
          const next = lines[i];
          if (blank(next)) {
            // A blank line continues the item only when an indented line follows it.
            let j = i; while (j < lines.length && blank(lines[j])) j++;
            if (j < lines.length && lines[j].search(/\S/) >= contentIndent) { for (; i < j; i++) body.push(""); continue; }
            break;
          }
          const indent = next.search(/\S/);
          if (indent >= contentIndent) { body.push(next.slice(contentIndent)); i++; continue; }
          if (ITEM.test(next) || startsBlock(next, lines[i + 1])) break;
          // A lazy continuation of the item's paragraph.
          body.push(next.trim()); i++;
        }
        items.push(blocksOf(body));
        let j = i; while (j < lines.length && blank(lines[j])) j++;
        const following = j < lines.length ? ITEM.exec(lines[j]) : null;
        if (following && /\d/.test(following[2]) === ordered && following[1].length <= 3) i = j; else break;
      }
      blocks.push({ kind: "list", ordered, start, items });
      continue;
    }
    if (line.includes("|") && i + 1 < lines.length && TABLE_RULE.test(lines[i + 1]) && lines[i + 1].includes("-")) {
      const header = cells(line);
      const rows: ProseInline[][][] = [];
      i += 2;
      while (i < lines.length && !blank(lines[i]) && lines[i].includes("|")) { rows.push(cells(lines[i])); i++; }
      blocks.push({ kind: "table", header, rows });
      continue;
    }
    const paragraph: string[] = [line];
    i++;
    while (i < lines.length && !blank(lines[i])) {
      if (SETEXT.test(lines[i])) {
        const level = lines[i].trim()[0] === "=" ? 1 : 2;
        blocks.push({ kind: "heading", level, content: proseInlines(paragraph.map(l => l.trim()).join(" ")) });
        paragraph.length = 0; i++; break;
      }
      if (startsBlock(lines[i], lines[i + 1])) break;
      paragraph.push(lines[i]); i++;
    }
    if (paragraph.length) blocks.push({ kind: "paragraph", lines: paragraph.map(l => proseInlines(l.replace(/^[ \t]+/, "").replace(/(?: {2,}|\\)$/, ""))) });
  }
  return blocks;
}

function ProseText({ value }: { value: string }) {
  return <>{agentTextParts(value).map((part, i) => part.mark ? <span key={i} className="agent-text-mark" style={markStyle}>{part.text}</span> : part.text)}</>;
}
function ProseInlines({ value }: { value: ProseInline[] }) {
  return <>{value.map((node, i) => {
    switch (node.kind) {
      case "text": return <ProseText key={i} value={node.text} />;
      case "code": return <code key={i}><ProseText value={node.text} /></code>;
      case "em": return <em key={i}><ProseInlines value={node.children} /></em>;
      case "strong": return <strong key={i}><ProseInlines value={node.children} /></strong>;
      case "link": {
        // Not a link: the text, then its target in plain text (once, when the text is the target itself).
        const same = node.children.length === 1 && node.children[0].kind === "text" && node.children[0].text === node.target;
        return <span key={i} className="agent-prose-link"><ProseInlines value={node.children} />{same ? null : <> (<span className="agent-prose-target"><ProseText value={node.target} /></span>)</>}</span>;
      }
    }
  })}</>;
}
const tight = (blocks: ProseBlock[]) => blocks.length === 1 && blocks[0].kind === "paragraph";
function ProseBlocks({ value }: { value: ProseBlock[] }) {
  return <>{value.map((block, i) => {
    switch (block.kind) {
      case "paragraph": return <p key={i}>{block.lines.map((line, k) => <Fragment key={k}>{k > 0 && <br />}<ProseInlines value={line} /></Fragment>)}</p>;
      case "heading": return <p key={i} className={block.level <= 2 ? "agent-prose-heading agent-prose-heading--major" : "agent-prose-heading"}><strong><ProseInlines value={block.content} /></strong></p>;
      case "list": {
        const items = block.items.map((item, k) => <li key={k}>{tight(item) && item[0].kind === "paragraph"
          ? item[0].lines.map((line, n) => <Fragment key={n}>{n > 0 && <br />}<ProseInlines value={line} /></Fragment>)
          : <ProseBlocks value={item} />}</li>);
        return block.ordered ? <ol key={i} start={block.start !== 1 ? block.start : undefined}>{items}</ol> : <ul key={i}>{items}</ul>;
      }
      case "code": return <pre key={i} className="agent-prose-code"><code>{block.text.split("\n").map((line, k) => <Fragment key={k}>{k > 0 && "\n"}<ProseText value={line} /></Fragment>)}</code></pre>;
      case "quote": return <blockquote key={i}><ProseBlocks value={block.blocks} /></blockquote>;
      case "table": return <table key={i} className="agent-prose-table">
        <thead><tr>{block.header.map((cell, k) => <td key={k}><strong><ProseInlines value={cell} /></strong></td>)}</tr></thead>
        <tbody>{block.rows.map((row, r) => <tr key={r}>{block.header.map((_, k) => <td key={k}><ProseInlines value={row[k] ?? []} /></td>)}</tr>)}</tbody>
      </table>;
      case "rule": return <hr key={i} />;
    }
  })}</>;
}

/** The accessibility name of the agent's formatted prose. */
export const AGENT_PROSE_NAME = "Text the agent wrote, not the App's words";
/** An agent's message in the conversation, formatted as described above. Every other supplied text stays in AgentText. */
export function AgentProse({ value, name = AGENT_PROSE_NAME }: { value: Json; name?: string }) {
  return <div role="group" aria-label={name} className="agent-prose chat-markdown"><ProseBlocks value={proseBlocks(agentTextValue(value))} /></div>;
}

export const RECORDED_DATA_LABEL = "Recorded data (JSON):";
/** A diagnostic record shown as indented JSON, in a marked box since it may hold values the App did not write. JSON
 * escapes line breaks but not direction or other format characters, so the marking matters inside JSON too. */
export function RecordedData({ value, label = RECORDED_DATA_LABEL, name, style }: { value: Json; label?: string; name?: string; style?: CSSProperties }) {
  let shown: string;
  try { shown = JSON.stringify(value, null, 2) ?? String(value); } catch { shown = String(value); }
  return <AgentText block value={shown} source="record" label={label} name={name ?? "Recorded data"} style={style} />;
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

// A choice among conversations (the controls rule: a control's name holds only the App's words, except a
// conversation's title in the form adopted here). An <option> cannot hold a box, so a choice is a list of native
// radio buttons, each with its label. The label begins with the App's words ("Conversation" and an identifier that
// tells it apart in the list, or its entry number), then the title as Codex supplied it, marked inside the label
// (dotted outline, every line break, control or direction character shown as a mark, a long title shortened with
// how much is shown said). The list says once, under its legend, that its titles are supplied by Codex; each label
// also carries, hidden from sight, the per-item attribution before its title, so its accessible name reads the App's
// words, then who supplied the title, then the title. Only the radio button and its label are clickable. The model
// and provider stand beside the label, outside it, boxed, and reach the radio button only as its accessible
// description, after the App's words saying who supplied them.

/** One conversation offered: `key` is what choosing it submits; every other field is shown as Codex reported it. */
export type ConversationChoice = {
  key: string;
  /** The conversation's identity (thread ID) as Codex reported it. */
  id: unknown;
  /** Its name, or its first message, as Codex supplied it. */
  title?: unknown;
  /** Shown only when the field is present (null shows "not reported"). */
  model?: unknown;
  provider?: unknown;
  /** ThreadStatus's type; shown only when the field is present (null shows "not recorded"). */
  status?: unknown;
  /** The relationship as recorded (a fork's source, a spawned child's parent), never read from the title. */
  relation?: { kind: "child" | "fork"; id: unknown } | null;
  /** A chosen conversation kept in the list though the current list would not show it. */
  retained?: "outside-search" | "not-received";
};

/** The longest title shown: a longer one is shown as its first characters, with the count said in a small element after the title, inside the choice's label. */
export const CHOICE_TITLE_LIMIT = 120;
/** The fewest characters of an identifier shown when it is shortened. */
export const SHORT_ID_MIN = 8;

/** The title as shown in a choice: at most CHOICE_TITLE_LIMIT characters (whole code points), and how many there are. */
export function boundedTitle(value: unknown): { text: string; total: number; shortened: boolean } | null {
  const text = agentTextValue(value as Json);
  if (!text) return null;
  const points = [...text];
  return points.length > CHOICE_TITLE_LIMIT ? { text: points.slice(0, CHOICE_TITLE_LIMIT).join(""), total: points.length, shortened: true } : { text, total: points.length, shortened: false };
}
/** The App's words after a shortened title: how much of it is shown. */
const titleCount = (title: { total: number; shortened: boolean }) => title.shortened ? ` (its first ${CHOICE_TITLE_LIMIT} of ${title.total} characters)` : "";
/** The list's one visible attribution for its titles; each choice's accessible name repeats it before its own title. */
export const CHOICE_TITLES_ATTRIBUTION = "The titles shown are supplied by Codex, not the App's words.";
/** Said in each choice's accessible name before its title, and not shown: a screen reader or a tool reads a row on its own. */
export const CHOICE_TITLE_NAME_WORDS = ", title supplied by Codex:";

/** Each identity's shortest form that tells it apart in the list: the shortest prefix of at least SHORT_ID_MIN
 * characters that no other identity in the list begins with, followed by … when shortened; the whole identity when
 * no prefix does; null for an identity that is not a plain identifier. */
export function shortIds(ids: readonly unknown[]): (string | null)[] {
  const plain = ids.map(id => plainId(typeof id === "number" && Number.isSafeInteger(id) ? String(id) : id));
  return plain.map((id, i) => {
    if (id === null) return null;
    const others = plain.filter((other, j) => j !== i && other !== null) as string[];
    for (let n = Math.min(SHORT_ID_MIN, id.length); n <= id.length; n++) {
      const prefix = id.slice(0, n);
      if (others.every(other => other.slice(0, n) !== prefix)) return n < id.length ? `${prefix}…` : prefix;
    }
    return id;
  });
}

/** The App's words naming one choice: its shortened identifier, or its place in the list when the identity is not a
 * plain identifier (the identity is then shown beside, boxed), and the recorded relationship. */
export function choiceLabels(rows: readonly ConversationChoice[]): string[] {
  const shorts = shortIds(rows.map(row => row.id));
  const plain = rows.map(row => plainId(row.id));
  const shortOf = (id: unknown): string => {
    const p = plainId(id);
    if (p === null) return "a conversation whose identity is shown beside";
    const at = plain.indexOf(p);
    return `conversation ${at >= 0 ? shorts[at] : p}`;
  };
  return rows.map((row, i) => {
    const repeated = plain[i] !== null && plain.filter(p => p === plain[i]).length > 1;
    const own = shorts[i] === null ? `Conversation ${i + 1} (identity shown beside)` : `Conversation ${shorts[i]}${repeated ? ` (entry ${i + 1}; this identity is listed more than once)` : ""}`;
    const relation = row.relation ? `, ${row.relation.kind === "child" ? "child" : "fork"} of ${shortOf(row.relation.id)}` : "";
    return own + relation;
  });
}

/** The accessible description of one choice: each supplied value beside its label (the title is in the label), after the
 * App's attribution, every mark in place; null when there is none. */
export function choiceDescription(row: ConversationChoice): string | null {
  const parts: string[] = [];
  const supplied = (words: string, value: unknown) => { if (value !== null && value !== undefined) parts.push(`${words}: ${agentTextShown(agentTextValue(value as Json))}`); };
  supplied("Model reported by Codex", row.model);
  supplied("Provider reported by Codex", row.provider);
  if (row.status !== undefined && row.status !== null) {
    const word = wordOf(THREAD_STATUS, row.status);
    parts.push(word !== null ? `Status: ${word}` : `Status reported by Codex: ${agentTextShown(agentTextValue(row.status as Json))}`);
  }
  if (plainId(row.id) === null) supplied("Identity reported by Codex", row.id);
  if (row.relation && plainId(row.relation.id) === null) supplied("Recorded identity of the related conversation", row.relation.id);
  return parts.length > 0 ? parts.join(". ") : null;
}

// The title inside a choice's label: the compact marked inline form. Not an AgentText box: a box is a named group, and in
// a control's accessible name a descendant's own name replaces its content, so the title would vanish from the name.
const choiceTitleStyle: CSSProperties = { outline: "1px dotted var(--ink-faint, #786f5f)", outlineOffset: 1, borderRadius: 2, padding: "0 2px", fontFamily: "var(--font-code, monospace)", whiteSpace: "pre-wrap", overflowWrap: "anywhere" };
const visuallyHidden: CSSProperties = { position: "absolute", width: 1, height: 1, margin: -1, padding: 0, border: 0, overflow: "hidden", clip: "rect(0 0 0 0)", whiteSpace: "nowrap" };

const RETAINED_WORDS = { "outside-search": "chosen — outside this search", "not-received": "chosen — not in the received list" } as const;
const choiceRowStyle: CSSProperties = { display: "block", margin: "2px 0" };

/**
 * A conversation's supplied title inside a choice, after the App's words and the identifier: the App's words saying
 * who supplied it (in the accessible name only), then the title set apart, with its line breaks and control
 * characters as marks, and how much of it is shown when it is shortened. Nothing where no title is supplied. Every
 * list of conversation choices shows a title through this.
 */
export function ChoiceTitle({ value }: { value: unknown }) {
  const title = boundedTitle(value);
  if (!title) return null;
  return <><span className="conversation-choice-title-name" style={visuallyHidden}>{CHOICE_TITLE_NAME_WORDS}</span> <span className="conversation-choice-title" style={choiceTitleStyle}><Parts value={title.text} /></span>{title.shortened && <small>{titleCount(title)}</small>}</>;
}

/**
 * A choice among conversations, as native radio buttons in a fieldset with the App's legend. `value` is the list
 * offered; `chosen` is the key chosen ("" for none); `onChoose` is called with a key; `none`, when given, offers a
 * first choice submitting "" and is named by those words; `group` is the radio buttons' shared name, unique on the
 * page. Hookless, so a view that is walked as an element tree can hold it.
 */
export function ConversationChoices({ legend, value, chosen, onChoose, group, disabled = false, none, describedBy, style }: {
  legend: string; value: readonly ConversationChoice[]; chosen: string; onChoose: (key: string) => void; group: string;
  disabled?: boolean; none?: string; describedBy?: string; style?: CSSProperties;
}) {
  const rows: readonly ConversationChoice[] = Array.isArray(value) ? value : [];
  const labels = choiceLabels(rows);
  return <fieldset className="conversation-choices" disabled={disabled} aria-describedby={describedBy} style={{ border: "none", padding: 0, margin: "4px 0", ...style }}>
    <legend>{legend}</legend>
    {rows.some(row => boundedTitle(row.title) !== null) && <p className="conversation-choices-attribution" style={{ margin: "0 0 2px" }}><small>{CHOICE_TITLES_ATTRIBUTION}</small></p>}
    {none !== undefined && <div className="conversation-choice" style={choiceRowStyle}>
      <label><input type="radio" name={group} value="" checked={chosen === ""} disabled={disabled} onChange={() => onChoose("")} /> {none}</label>
    </div>}
    {rows.map((row, i) => {
      const title = boundedTitle(row.title);
      return <div key={row.key} className="conversation-choice" style={choiceRowStyle}>
        <label><input type="radio" name={group} value={row.key} checked={chosen === row.key} disabled={disabled} onChange={() => onChoose(row.key)} aria-description={choiceDescription(row) ?? undefined} /> {labels[i]}
          <ChoiceTitle value={row.title} /></label>
        {plainId(row.id) === null && <>{" "}<AgentText value={row.id} source="codex" label="Identity:" name="The conversation's identity as Codex reported it, not the App's words" /></>}
        {row.relation && plainId(row.relation.id) === null && <>{" "}<AgentText value={row.relation.id} source="record" label="Related conversation:" name="The recorded identity of the related conversation" /></>}
        {!title && <>{" "}<i>no title supplied</i></>}
        {row.model !== undefined && <>{" "}{row.model !== null ? <AgentText value={row.model} source="codex" label="Model:" name="The model as Codex reported it, not the App's words" /> : <i>model not reported</i>}</>}
        {row.provider !== undefined && <>{" "}{row.provider !== null ? <AgentText value={row.provider} source="codex" label="Provider:" name="The provider as Codex reported it, not the App's words" /> : <i>provider not reported</i>}</>}
        {row.status !== undefined && <>{" "}<small>Status: <Word value={row.status} words={THREAD_STATUS} /></small></>}
        {row.retained && <>{" "}<small>{RETAINED_WORDS[row.retained]}</small></>}
      </div>;
    })}
  </fieldset>;
}
