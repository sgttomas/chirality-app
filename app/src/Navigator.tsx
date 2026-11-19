import { useState } from "react";
import { agentTextParts, numberWords, safeName, wordOf } from "./AgentText";
import type { WaitingEntry } from "./WaitingOnYou";

type Json = any; // eslint-disable-line @typescript-eslint/no-explicit-any

// The left panel, in the form of 3.0.1's navigator: every project the host's navigator read gives, each with its
// conversations under it, and for the open project each conversation's latest workflow run and how many it carries;
// conversations of no project in their own section. The read is navigator_read (app/src-tauri/src/navigator_read.rs,
// "What the read returns"); App.tsx makes it on a timer and hands each answer to navigatorAfterRead, and this module
// draws what that holds. It reads nothing itself and keeps nothing beyond the session.
//
// Whose words. A conversation's title is Codex's and is the entry's visible label, alone, in the navigator's type
// (App Agent 0's decision, DEL-01-04 REQ-002). The App's own state words (Needs answer, Approval needed, Your move,
// Agent says finished, the running turn's mark) are drawn only in the App's mark, a bordered pill a title cannot
// take, and come first in the entry's accessible name, so a title that imitates them is still read as a title. The
// sentences the host gives as the App's own (a runs reading's reason and limits, the registry's limits, a run's
// stateReason, why an entry cannot be opened) are shown whole, never recomposed. Folder names are shown as text,
// never in a control.

// ---- Successive readings: what the panel holds ----

/** The runs reading's reason while Chirality is working on the open project's runs (navigator_read.rs ROOT_BUSY). */
export const ROOT_BUSY = "Chirality is working on this project's runs; they are shown at the next reading.";
/** How many readings in a row must say ROOT_BUSY before the panel says it (App Agent 0's busy rule): that state is
 * usually shorter than a second, and the panel must not blink. */
export const BUSY_READINGS = 3;

/** What the panel holds: the last answer it shows (with the busy rule applied), when it was answered, the failure of
 * a later reading, and how many readings in a row each project's runs have been busy. */
export type NavigatorHeld = {
  read: Json | null;
  /** When the shown answer arrived (ms since the epoch). */
  readAt: number | null;
  /** The last reading failed, at this time; what is shown is the earlier answer. */
  failedAt: number | null;
  /** By project root: readings in a row whose runs were busy. */
  busy: Readonly<Record<string, number>>;
};
export const NO_NAVIGATOR_READ: NavigatorHeld = { read: null, readAt: null, failedAt: null, busy: {} };
export type NavigatorReading = { read: Json; at: number } | { failed: true; at: number };

const list = (value: Json): Json[] => (Array.isArray(value) ? value : []);
/** An answer of the read's shape: anything else is taken as a failed reading. */
const wellFormed = (read: Json) => !!read && typeof read === "object" && ["projects", "unassigned", "conversations", "registryLimits", "unplacedRequests"].every(key => Array.isArray(read[key]));
const runsBusy = (project: Json) => project?.runsRead?.state === "not-read" && project?.runsRead?.reason === ROOT_BUSY;
const entryKey = (entry: Json) => JSON.stringify([entry?.home ?? null, entry?.id ?? null]);

/**
 * The panel after one more reading. A failed reading keeps what is shown and says when it failed; it never empties
 * the list. A good one replaces it, except under the busy rule: where a project's runs are not read only because
 * Chirality is working on them, the run lines last shown are kept (its conversations are the new answer's) and the
 * sentence is shown only once BUSY_READINGS readings in a row have said it. Every other reason is shown at once and
 * no earlier run line is kept as current.
 */
export function navigatorAfterRead(held: NavigatorHeld, reading: NavigatorReading): NavigatorHeld {
  if ("failed" in reading || !wellFormed(reading.read)) return { ...held, failedAt: reading.at };
  const before = new Map<string, Json>(list(held.read?.projects).map((p: Json) => [p.root, p]));
  const busy: Record<string, number> = {};
  const projects = list(reading.read.projects).map((project: Json) => {
    if (!runsBusy(project)) return project;
    const count = (held.busy[project.root] ?? 0) + 1;
    busy[project.root] = count;
    if (count >= BUSY_READINGS) return project;
    const shown = before.get(project.root);
    const runs = new Map<string, Json>(list(shown?.entries).map((e: Json) => [entryKey(e), e]));
    return { ...project, runsRead: shown?.runsRead ?? null, unplacedRuns: shown?.unplacedRuns ?? 0,
      entries: list(project.entries).map((e: Json) => ({ ...e, run: runs.get(entryKey(e))?.run ?? null, runCount: runs.get(entryKey(e))?.runCount ?? 0 })) };
  });
  return { read: { ...reading.read, projects }, readAt: reading.at, failedAt: null, busy };
}

// ---- Requests waiting on the person, from "Waiting on you"'s own readings ----

/** A conversation's requests: questions (the agent asks the person), approvals (a permission), and requests counted
 * in another home whose kind the host does not give there; with the first of each to go to. */
export type EntryRequests = { questions: number; approvals: number; first: { answer: WaitingEntry | null; approve: WaitingEntry | null } };
/** The requests "Waiting on you" counts that are the person's to answer: one in the active home's register (a
 * question or a tool permission) or a count in another home. */
export const isPersonRequest = (entry: WaitingEntry) => entry.target.kind === "request" && (entry.source === "supplier-request" || entry.source === "waiting-overview");

/** Each request placed on the navigator entry of its conversation (the root it descends from, or its own), by home,
 * and the requests whose conversation is not an entry. The same records "Waiting on you" counts, so the two agree. */
export function placeRequests(entries: readonly WaitingEntry[], shown: ReadonlySet<string>): { on: Map<string, EntryRequests>; unplaced: WaitingEntry[] } {
  const on = new Map<string, EntryRequests>(), unplaced: WaitingEntry[] = [];
  for (const entry of entries.filter(isPersonRequest)) {
    const home = entry.concerns.kind === "conversation" ? entry.concerns.home : null;
    const own = entry.concerns.kind === "conversation" ? entry.concerns.threadId : null;
    const root = entry.group.label.kind === "conversation" ? entry.group.label.threadId : null;
    const at = [root, own].map(id => JSON.stringify([home, id])).find(key => shown.has(key));
    if (!at) { unplaced.push(entry); continue; }
    const marks = on.get(at) ?? { questions: 0, approvals: 0, first: { answer: null, approve: null } };
    if (entry.kind === "tool-permission") { marks.approvals += entry.count; marks.first.approve ??= entry; }
    else { marks.questions += entry.count; marks.first.answer ??= entry; }
    on.set(at, marks);
  }
  return { on, unplaced };
}

// ---- Times, in the App's words ----

const MONTHS = { "0": "Jan", "1": "Feb", "2": "Mar", "3": "Apr", "4": "May", "5": "Jun", "6": "Jul", "7": "Aug", "8": "Sep", "9": "Oct", "10": "Nov", "11": "Dec" } as const;
const WEEKDAYS = { "0": "Sun", "1": "Mon", "2": "Tue", "3": "Wed", "4": "Thu", "5": "Fri", "6": "Sat" } as const;
const DAY_MS = 86_400_000;
const twoDigits = (n: number) => n < 10 ? `0${numberWords(n)}` : numberWords(n);
const instantOf = (at: unknown): Date | null => { if (typeof at !== "string") return null; const d = new Date(at); return Number.isFinite(d.getTime()) ? d : null; };
/** The date as the navigator shows it, in local time: "Nov 3", with the year where it is not this year's. */
const dateWords = (d: Date, now: Date) => d.getFullYear() === now.getFullYear()
  ? `${wordOf(MONTHS, String(d.getMonth()))} ${numberWords(d.getDate())}` : `${wordOf(MONTHS, String(d.getMonth()))} ${numberWords(d.getDate())}, ${numberWords(d.getFullYear())}`;
/** An entry's time: today's as HH:MM, a day of the last six as its weekday, else its date. `exact` adds the time of
 * day to a date, and the seconds where `seconds` is asked for. Null for a time that is not one. */
export function whenWords(at: unknown, nowMs: number, exact: "short" | "minutes" | "seconds" = "short"): string | null {
  const d = instantOf(at);
  if (!d) return null;
  const now = new Date(nowMs);
  const clock = exact === "seconds" ? `${twoDigits(d.getHours())}:${twoDigits(d.getMinutes())}:${twoDigits(d.getSeconds())}` : `${twoDigits(d.getHours())}:${twoDigits(d.getMinutes())}`;
  if (exact !== "short") return `${dateWords(d, now)}, ${clock}`;
  const sameDay = d.getFullYear() === now.getFullYear() && d.getMonth() === now.getMonth() && d.getDate() === now.getDate();
  if (sameDay) return clock;
  const age = nowMs - d.getTime();
  return age > 0 && age < 6 * DAY_MS ? wordOf(WEEKDAYS, String(d.getDay())) : dateWords(d, now);
}
/** A time the App holds (ms), as HH:MM:SS. */
export const clockOf = (ms: number | null) => { if (ms === null) return null; const d = new Date(ms); return `${twoDigits(d.getHours())}:${twoDigits(d.getMinutes())}:${twoDigits(d.getSeconds())}`; };

// ---- One entry as drawn ----

/** How an entry opens: chosen in the conversation view (a loaded conversation of the active home), selected in
 * History (where it can be continued), or not from here, with the App's sentence why. */
export type EntryOpen = { kind: "choose"; key: string } | { kind: "history"; generation: Json; selectionEpoch: number; threadId: string } | { kind: "none"; why: string };

/** The run line's state, in a word: for an open run, the turn's state as the read gives it. */
const RUN_WORDS = { ended: "Ended", "start-not-confirmed": "Start not confirmed", unknown: "State not known" } as const;
export function runWord(run: Json, live: unknown, requested: boolean): string | null {
  if (!run) return null;
  if (run.state !== "open") return wordOf(RUN_WORDS, run.state) ?? "State not known";
  if (requested) return null;
  if (live === "running") return "Working";
  if (run.finishedReported === true) return "Agent says finished";
  return live === "idle" || live === "not-loaded" ? "Your move" : "Open";
}
/** The workflow's name where the App's own name rule admits it, else the App's words. */
const workflowWords = (name: unknown) => { const n = safeName(name); return n === "a workflow whose name is shown beside" ? "A workflow" : n; };

const sameJson = (a: Json, b: Json) => JSON.stringify(a) === JSON.stringify(b);
/** The App's sentences for an entry that is not opened from here (the read's own reason is shown as given). */
export const NOT_OPEN_PROJECT = "This project is not open in this running App, so its conversations are listed here and not opened from here.";
export const OTHER_HOME = "This conversation is in another Codex home; choose that home under Connection & access to open it.";
export const NOT_CURRENT = "This conversation was listed by a Codex that is no longer the one running; it can be opened once the list is read again.";

/** How an entry opens, given the active home and its current generation, and whether its section is a project open
 * here (or no project). Offers only what the host can do now. */
export function entryOpen(entry: Json, activeHome: string | null, generation: Json, openHere: boolean): EntryOpen {
  const open = entry?.open;
  if (open?.kind === "not-openable") return { kind: "none", why: typeof open.reason === "string" ? open.reason : NOT_CURRENT };
  if (entry?.home !== activeHome) return { kind: "none", why: OTHER_HOME };
  if (!sameJson(open?.generation, generation)) return { kind: "none", why: NOT_CURRENT };
  if (open?.kind === "loaded") return { kind: "choose", key: JSON.stringify([open.generation, open.threadId]) };
  if (open?.kind === "history" && Number.isSafeInteger(open.selectionEpoch)) return openHere ? { kind: "history", generation: open.generation, selectionEpoch: open.selectionEpoch, threadId: open.threadId } : { kind: "none", why: NOT_OPEN_PROJECT };
  return { kind: "none", why: NOT_CURRENT };
}

/** One entry with what its row needs: the read's own entry, its place in its list, whether its time is shown to the
 * minute (its title is shared) and whether its entry number is said (its title and that time are both shared), the
 * requests placed on it, whether a turn is running in it, the live state the run line reads, and how it opens. */
export type EntryShown = {
  key: string; e: Json; position: number; exact: boolean; numbered: boolean;
  live: boolean; liveWord: unknown; requests: EntryRequests | null; open: EntryOpen;
};
const titleOf = (e: Json): string | null => typeof e?.title === "string" && e.title !== "" ? e.title : null;
/** A section's entries as drawn: equal titles are told apart by their times (to the minute) and, where those are equal
 * too, by their entry numbers. A status the last read did not refresh says nothing current about a turn. */
export function shownEntries(entries: readonly Json[], ctx: { now: number; requests: Map<string, EntryRequests>; activeHome: string | null; generation: Json; openHere: boolean; statusCurrent: boolean }): EntryShown[] {
  const count = (keys: string[]) => { const m = new Map<string, number>(); for (const k of keys) m.set(k, (m.get(k) ?? 0) + 1); return m; };
  const titles = count(entries.map(e => JSON.stringify(titleOf(e))));
  const exact = entries.map(e => (titles.get(JSON.stringify(titleOf(e))) ?? 0) > 1);
  const times = count(entries.map((e, i) => JSON.stringify([titleOf(e), exact[i] ? whenWords(e?.updatedAt, ctx.now, "minutes") : null])));
  return entries.map((e: Json, i: number) => ({
    key: entryKey(e), e, position: i + 1, exact: exact[i],
    numbered: exact[i] && (times.get(JSON.stringify([titleOf(e), whenWords(e?.updatedAt, ctx.now, "minutes")])) ?? 0) > 1,
    live: ctx.statusCurrent && e?.live === "running", liveWord: ctx.statusCurrent ? e?.live : "unknown",
    requests: ctx.requests.get(entryKey(e)) ?? null, open: entryOpen(e, ctx.activeHome, ctx.generation, ctx.openHere),
  }));
}

/** An entry's time as shown: to the minute where its title is shared, else as short as tells the day. */
export const entryWhen = (updatedAt: unknown, loaded: boolean, now: number, exact: boolean) =>
  whenWords(updatedAt, now, exact ? "minutes" : "short") ?? (loaded ? "now" : "time not known");
const runsWords = (n: unknown) => n === 1 ? "1 run" : `${numberWords(n)} runs`;
const requested = (r: EntryRequests | null) => !!r && r.questions + r.approvals > 0;

/** The App's state words before an entry's title in its accessible name, each ending ". ", then "Title: " where the
 * conversation has one: a title imitating a state word is read after "Title:", never as one of them. */
export function namePrefix(entry: EntryShown): string {
  const word = runWord(entry.e?.run, entry.liveWord, requested(entry.requests));
  const questions = (entry.requests?.questions ?? 0) > 0, approvals = (entry.requests?.approvals ?? 0) > 0;
  return `${questions ? "Needs answer. " : ""}${approvals ? "Approval needed. " : ""}${entry.live && word !== "Working" ? "Working. " : ""}${word === null ? "" : `${word}. `}${titleOf(entry.e) !== null ? "Title: " : ""}`;
}

/** The entry's accessible description, in the App's words: who supplied the title, its time, its entry number where
 * the times are equal too, its run, and how it opens where that is not the conversation view. */
export function entryDescription(entry: EntryShown, now: number): string {
  const e = entry.e;
  return `${titleOf(e) !== null ? "Title supplied by Codex." : "No title supplied."} Updated ${entryWhen(e?.updatedAt, e?.open?.kind === "loaded", now, entry.exact)}.${entry.numbered ? ` Entry ${numberWords(entry.position)} in this list.` : ""}${e?.run ? ` Latest run: ${workflowWords(e?.run?.workflow?.name)}; ${runsWords(e?.runCount)} in this conversation.` : ""}${entry.open.kind === "history" ? " Opens in History, where it can be continued." : entry.open.kind === "none" ? " Not opened from here; the reason is shown under it." : ""}`;
}

// ---- Drawing ----

const HOME_WORDS = { account: "The account home", "api-key": "The API key home", "local-provider": "The local model home" } as const;

function EntryRow({ entry, now, selected, chooserReady, choose, openInHistory, answer }: {
  entry: EntryShown; now: number; selected: boolean; chooserReady: boolean; choose: (key: string) => void;
  openInHistory: (open: Extract<EntryOpen, { kind: "history" }>) => void; answer: (request: WaitingEntry) => void;
}) {
  const e = entry.e, open = entry.open;
  const usable = open.kind !== "none" && chooserReady;
  const press = () => { if (open.kind === "choose") choose(open.key); else if (open.kind === "history") openInHistory(open); };
  const title = titleOf(e);
  const parts = title !== null ? agentTextParts(title) : [];
  const word = runWord(e?.run, entry.liveWord, requested(entry.requests));
  const answerFirst = entry.requests?.first.answer ?? null, approveFirst = entry.requests?.first.approve ?? null;
  return <li>
    <div className="woven-navigator-session-row">
      <button type="button" className={`woven-navigator-session${entry.live ? " woven-navigator-session--live" : ""}${open.kind === "none" ? " v4-nav-unavailable" : ""}`} data-session-id={entry.e?.id}
        disabled={!usable} aria-pressed={selected} aria-description={entryDescription(entry, now)} onClick={() => { if (usable) press(); }}>
        <span className="woven-navigator-session-heading">
          <span className="visually-hidden">{namePrefix(entry)}</span>
          {entry.live ? <span className="woven-navigator-session-dot" aria-hidden="true"/> : null}
          {title !== null
            ? <span className="woven-navigator-session-title v4-nav-title">{parts.map((part, i) => part.mark ? <span key={i} className="v4-nav-title-mark">{part.text}</span> : <span key={i}>{part.text}</span>)}</span>
            : <span className="woven-navigator-session-title v4-nav-untitled">Untitled chat</span>}
          <span className="woven-navigator-session-when">{entryWhen(e?.updatedAt, e?.open?.kind === "loaded", now, entry.exact)}</span>
        </span>
        {e?.run ? <span className="woven-navigator-session-folder v4-nav-run" aria-hidden="true">
          <span>◇ </span>{workflowWords(e?.run?.workflow?.name)}
          {word !== null ? <> · <span className="v4-nav-mark">{word}</span></> : null}
          {Number.isSafeInteger(e?.runCount) && e.runCount > 1 ? ` · ${runsWords(e?.runCount)}` : null}
        </span> : null}
      </button>
      {answerFirst ? <button type="button" className="v4-nav-mark v4-nav-mark--you" aria-label={entry.numbered ? `Needs answer, entry ${numberWords(entry.position)}: go to the request` : "Needs answer: go to the request"} onClick={() => answer(answerFirst)}>Needs answer</button> : null}
      {approveFirst ? <button type="button" className="v4-nav-mark v4-nav-mark--you" aria-label={entry.numbered ? `Approval needed, entry ${numberWords(entry.position)}: go to the request` : "Approval needed: go to the request"} onClick={() => answer(approveFirst)}>Approval needed</button> : null}
    </div>
    {e?.run?.state === "unknown" && typeof e?.run?.stateReason === "string" ? <p className="woven-navigator-session-notice">{e.run.stateReason}</p> : null}
    {open.kind === "none" && open.why !== NOT_OPEN_PROJECT ? <p className="woven-navigator-session-notice">{open.why}</p> : null}
  </li>;
}

/** One project's runs reading, said where it is not whole: the reason of a reading not made, shown whole; the limits of
 * a limited one behind a disclosure; the runs that could not be placed. */
function RunsReading({ project }: { project: Json }) {
  const runs = project?.runsRead;
  const limits = list(runs?.limits).filter((l: Json) => typeof l === "string");
  const unplaced = Number.isSafeInteger(project?.unplacedRuns) ? project.unplacedRuns : 0;
  return <>
    {runs?.state === "not-read" && typeof runs.reason === "string" ? <p className="woven-navigator-session-notice">{runs.reason}</p> : null}
    {unplaced > 0 ? <p className="woven-navigator-session-notice">{unplaced === 1 ? "1 recorded run of this project is not shown under any conversation." : `${unplaced} recorded runs of this project are not shown under any conversation.`}</p> : null}
    {limits.length > 0 ? <details className="v4-nav-limits"><summary>{runs?.state === "not-read" ? "What was not read" : "Runs read with limits"}</summary>{limits.map((limit: string, i: number) => <p key={i}>{limit}</p>)}</details> : null}
  </>;
}

/** What every section's list needs from the navigator. */
type ListContext = {
  now: number; selectedThread: string | null; activeHome: string | null; chooserReady: boolean; choose: (key: string) => void;
  openInHistory: (open: Extract<EntryOpen, { kind: "history" }>) => void; answer: (request: WaitingEntry) => void;
};
const needsYou = (entries: EntryShown[]) => entries.some(e => requested(e.requests));
function EntryList({ entries, at, listId }: { entries: EntryShown[]; at: ListContext; listId: string }) {
  return <ul id={listId} className="woven-navigator-session-list">
    {entries.map(entry => <EntryRow key={entry.key} entry={entry} now={at.now} selected={at.selectedThread !== null && entry.e?.id === at.selectedThread && entry.e?.home === at.activeHome}
      chooserReady={at.chooserReady} choose={at.choose} openInHistory={at.openInHistory} answer={at.answer}/>)}
  </ul>;
}
/** A project: its folder's name as recorded (the person's words, so not inside a control), whether it is the one new
 * conversations open in, its count, a separate fold control, what is not whole about it, and its conversations. */
function ProjectSection({ project, entries, at, folded, fold, listId }: { project: Json; entries: EntryShown[]; at: ListContext; folded: boolean; fold: () => void; listId: string }) {
  const current = project?.current === true;
  const unavailable = project?.state === "unavailable";
  const notice = project?.notice && typeof project.notice.message === "string" ? project.notice.message : null;
  return <section className="woven-chat-section woven-chat-section--folder" data-project-state={project?.state === "open" ? "open" : unavailable ? "unavailable" : "listed"}>
    <div className={`woven-chat-section-heading woven-chat-section-heading--folder${current ? " is-current" : ""}`}>
      <span><span aria-hidden="true">▱ </span>{typeof project?.label === "string" && project.label ? project.label : "A folder whose name is not recorded"}{current ? <span className="woven-chat-section-current"> · current</span> : null}</span>
      <span className="v4-nav-heading-end">
        {folded && needsYou(entries) ? <span className="v4-nav-mark v4-nav-mark--you">Needs you</span> : null}
        <span>{entries.length}</span>
        <button type="button" className="v4-nav-fold" aria-expanded={!folded} aria-controls={listId} aria-label={folded ? "Show this project's conversations" : "Fold this project's conversations"} onClick={fold}>{folded ? "▸" : "▾"}</button>
      </span>
    </div>
    {notice !== null ? <div className={unavailable ? "woven-folder-notice woven-folder-notice--unavailable" : "woven-folder-notice"} role="note"><p>{notice}</p></div> : null}
    {!folded ? <>
      {entries.some(e => e.open.kind === "none" && e.open.why === NOT_OPEN_PROJECT) ? <p className="woven-navigator-session-notice">{NOT_OPEN_PROJECT}</p> : null}
      <RunsReading project={project}/>
      <EntryList entries={entries} at={at} listId={listId}/>
    </> : null}
  </section>;
}
/** Conversations that belong to no project: the App's heading, which is its own fold control. */
function UnassignedSection({ entries, at, folded, fold, listId }: { entries: EntryShown[]; at: ListContext; folded: boolean; fold: () => void; listId: string }) {
  return <section className="woven-chat-section">
    <button type="button" className="woven-chat-section-heading" aria-expanded={!folded} aria-controls={listId} onClick={fold}>
      <span>Conversations without a project</span><span>{numberWords(entries.length)}</span>
    </button>
    {!folded ? <EntryList entries={entries} at={at} listId={listId}/> : null}
  </section>;
}

/** The account row's place at the foot of the navigator: here it opens Settings & tools. */
export function AccountRow({ open }: { open: () => void }) {
  return <div className="account-controls-root">
    <button type="button" className="account-controls-row" aria-label="Settings & tools" onClick={open}>
      <span className="account-controls-avatar" aria-hidden="true"><svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="8.5" r="3.5"/><path d="M4.5 20c.9-3.6 3.8-5.5 7.5-5.5s6.6 1.9 7.5 5.5"/></svg></span>
      <span className="account-controls-identity"><strong>Settings &amp; tools</strong></span>
    </button>
  </div>;
}

/** Which sections are open at first: the project new conversations open in, the conversations of no project, and
 * any section with a request waiting on the person. The person's own folding then holds for the session. */
export const openAtFirst = (key: string, current: boolean, entries: EntryShown[]) => key === "unassigned" || current || needsYou(entries);

/** Everything the navigator draws, from what the panel holds and the "Waiting on you" readings. */
export function navigatorShown(held: NavigatorHeld, waiting: readonly WaitingEntry[], ctx: { now: number; activeHome: string | null; generation: Json; statusCurrent: boolean }) {
  const read = held.read;
  const sections: { key: string; project: Json | null; entries: Json[]; openHere: boolean }[] = [
    ...list(read?.projects).map((p: Json) => ({ key: `project:${String(p?.root)}`, project: p, entries: list(p?.entries), openHere: p?.current === true && p?.state === "open" })),
    ...(list(read?.unassigned).length > 0 ? [{ key: "unassigned", project: null, entries: list(read?.unassigned), openHere: true }] : []),
  ];
  const keys = new Set(sections.flatMap(s => s.entries.map(entryKey)));
  const { on, unplaced } = placeRequests(waiting, keys);
  return {
    sections: sections.map(s => ({ ...s, shown: shownEntries(s.entries, { ...ctx, requests: on, openHere: s.openHere }) })),
    unplaced,
  };
}

/**
 * The left region: the brand, New chat, every project with its conversations, the conversations of no project, what
 * the read could not give, and the account row. `choose` is the conversation view's own choice (null while that view
 * takes no choice); `openInHistory` selects a conversation in History; `answer` goes to a request's card as "Waiting
 * on you" does.
 */
export function Navigator({ held, waiting, now, activeHome, generation, statusCurrent, selectedThread, choose, openInHistory, answer, newChat, openSettings }: {
  held: NavigatorHeld; waiting: readonly WaitingEntry[]; now: number; activeHome: string | null; generation: Json; statusCurrent: boolean; selectedThread: string | null;
  choose: ((key: string) => void) | null; openInHistory: (open: Extract<EntryOpen, { kind: "history" }>) => void; answer: (request: WaitingEntry) => void;
  newChat: () => void; openSettings: () => void;
}) {
  const [folding, setFolding] = useState<Record<string, boolean>>({});
  const read = held.read;
  const { sections, unplaced } = navigatorShown(held, waiting, { now, activeHome, generation, statusCurrent });
  const homesNotRead = list(read?.conversations).filter((c: Json) => c?.state === "not-read" && typeof c?.reason === "string");
  const registryLimits = list(read?.registryLimits).filter((l: Json) => typeof l === "string");
  const stale = held.readAt !== null && now - held.readAt > 10_000;
  const at: ListContext = { now, selectedThread, activeHome, chooserReady: !!choose, choose: key => choose?.(key), openInHistory, answer };
  const foldedOf = (s: typeof sections[number]) => folding[s.key] ?? !openAtFirst(s.key, s.project?.current === true, s.shown);
  const foldOf = (s: typeof sections[number]) => () => { const folded = foldedOf(s); setFolding(old => ({ ...old, [s.key]: !folded })); };
  const firstUnplaced = unplaced[0] ?? null;
  const unplacedCount = unplaced.reduce((n, e) => n + e.count, 0);
  return <nav className="woven-navigator" aria-label="Workspace Navigator">
    <header className="woven-navigator-brand">Chirality</header>
    <div className="woven-navigator-sections">
      <button type="button" className="woven-new-chat" disabled={!choose} onClick={newChat}><span aria-hidden="true">＋</span> New chat</button>
      <div className="woven-navigator-sessions">
        {read === null && held.failedAt === null ? <p className="panel-empty" role="status">Reading your projects and conversations…</p> : null}
        {read === null && held.failedAt !== null ? <p className="panel-error" role="status">Your projects and conversations could not be read at {clockOf(held.failedAt)}; the App reads them again shortly.</p> : null}
        {read !== null && (held.failedAt !== null || stale) ? <p className="woven-navigator-session-notice" role="status">Shown as read at {clockOf(held.readAt)}{held.failedAt !== null ? `; the reading at ${clockOf(held.failedAt)} failed` : "; a newer reading has not answered yet"}.</p> : null}
        {registryLimits.map((limit: string, i: number) => <div key={`registry-${i}`} className="woven-folder-notice" role="note"><p>{limit}</p></div>)}
        {homesNotRead.map((c: Json, i: number) => <div key={`home-${i}`} className="woven-folder-notice" role="note"><p>{wordOf(HOME_WORDS, c.home) ?? "A Codex home"}: {c.reason}</p></div>)}
        {firstUnplaced ? <div className="woven-folder-notice" role="note"><p>{unplacedCount === 1 ? "1 request waits on a conversation not listed here." : `${unplacedCount} requests wait on conversations not listed here.`}</p>
          <div className="woven-folder-notice-actions"><button type="button" onClick={() => answer(firstUnplaced)}>Go to it</button></div></div> : null}
        {read !== null && sections.length === 0 ? <p className="panel-empty">No projects or conversations yet. New chat starts one.</p> : null}
        {sections.map((s, i) => s.project
          ? <ProjectSection key={s.key} project={s.project} entries={s.shown} at={at} folded={foldedOf(s)} fold={foldOf(s)} listId={`navigator-section-${i}`}/>
          : <UnassignedSection key={s.key} entries={s.shown} at={at} folded={foldedOf(s)} fold={foldOf(s)} listId={`navigator-section-${i}`}/>)}
      </div>
    </div>
    <footer className="woven-compatibility"><AccountRow open={openSettings}/></footer>
  </nav>;
}

/** The collapsed strip's request mark: how many conversations have a request waiting on the person, as the navigator
 * places them, and the requests placed on none. */
export function waitingConversations(held: NavigatorHeld, waiting: readonly WaitingEntry[], ctx: { now: number; activeHome: string | null; generation: Json; statusCurrent: boolean }): number {
  const { sections, unplaced } = navigatorShown(held, waiting, ctx);
  return sections.reduce((n, s) => n + s.shown.filter(e => e.requests !== null).length, 0) + (unplaced.length > 0 ? 1 : 0);
}

/** The folder's name: the last part of its path. */
export function folderName(path: string): string {
  const parts = path.split(/[\\/]+/).filter(Boolean);
  return parts.length ? parts[parts.length - 1] : path;
}
/** The same path as written, but for one trailing separator. Two spellings of one folder (an alias) do not match. */
export const samePath = (a: string, b: string) => a.replace(/\/$/, "") === b.replace(/\/$/, "");
