// The navigator's read (navigator_read.rs, "What the read returns"), constructed: the answer a state gives by default,
// built from its host snapshot (the launched project with the current generation's conversations and the runs the
// workflow root holds for them), and the builders the navigator's own states use. Shapes follow the Rust types and
// tests/navigator.test.mjs; the content is invented. Not a state.
import { GEN, PROJECT, at } from "./_shared.js";

// The host's own sentences, as navigator_read.rs and the modules it quotes word them.
export const LIST_WORDS = "saved conversations, not archived, as Codex listed them when it became ready";
export const ROOT_BUSY = "Chirality is working on this project's runs; they are shown at the next reading.";
export const RUNS_FAILED = "The project's recorded runs could not be read."; // runtime_session.rs REOPEN_NOT_READ_WORDS[1]
export const NOT_OPEN_RUNS = "Chirality reads a project's recorded runs once the project is open in this running App.";
export const RUN_PENDING = "An operation on this run is in progress in this running App, so its state is not known at this moment.";
export const UNIMPORTED = "This project's records are kept in the records store. Records in the project folder have not been imported and may not be shown in this view.";

const TITLE_CHARS = 60;
/** navigator_read.rs title: Codex's name, else its preview with whitespace made single spaces and cut on a word. */
export function title(name, preview) {
  if (typeof name === "string" && name.trim()) return name.trim();
  const words = typeof preview === "string" ? preview.split(/\s+/).filter(Boolean).join(" ") : "";
  if (!words) return null;
  if ([...words].length <= TITLE_CHARS) return words;
  const head = [...words].slice(0, TITLE_CHARS).join("");
  return [...words][TITLE_CHARS] === " " ? head : head.slice(0, head.lastIndexOf(" ") > 0 ? head.lastIndexOf(" ") : head.length).trimEnd();
}
const label = root => root.split("/").filter(Boolean).pop();
const live = status => ({ active: "running", idle: "idle", notLoaded: "not-loaded" })[status?.type] ?? "unknown";

export const workflow = name => ({ name, title: null, origin: "included with the App", release: "Chirality Library 3.4.0" });
let runs = 0;
export const run = (state, over = {}) => ({ runId: `run:workflow:invented-${++runs}`, workflow: workflow("define-work"), state,
  stateReason: null, endedBy: state === "ended" ? { stoppedBy: "person", cause: "completed" } : null, finishedReported: null, resultCount: null, ...over });
/** A stored conversation of the account home, not loaded now: History's own path opens it. */
export const stored = (id, titleText, minutesAgo, over = {}) => ({ id, home: "account", projectRoot: PROJECT, projectSource: "recorded", title: titleText, titleSource: titleText === null ? "none" : "name",
  createdAt: null, updatedAt: new Date(Date.parse(at(0)) + 3 * 3600_000 - minutesAgo * 60_000).toISOString(), live: "not-loaded", needsAnswer: 0, needsAnswerOn: [], archived: false,
  open: { kind: "history", home: "account", generation: GEN, selectionEpoch: 1, threadId: id }, run: null, runCount: 0, childrenRunning: null, ...over });
export const project = (root, over = {}) => ({ projectId: `project:${label(root)}`, root, label: label(root), current: false, state: "listed", notice: null,
  runsRead: { state: "not-read", reason: NOT_OPEN_RUNS, readAt: null, limits: [] }, unplacedRuns: 0, entries: [], ...over });
export const launched = (entries, over = {}) => project(PROJECT, { current: true, state: "open", runsRead: { state: "read", readAt: at(0, 30), limits: [] }, entries, ...over });
export const navigatorAnswer = (projects, over = {}) => ({ readAt: at(2), projects, unassigned: [], registryLimits: [], unplacedRequests: [],
  conversations: [{ home: "account", list: LIST_WORDS, readAt: null, state: "read" }], ...over });

/** The read a state's host snapshot implies: its launched project with the current generation's conversations, each
 * with the latest run the workflow root holds for it, the finished report offered where the run guide offers one. */
export function readFromHost(host) {
  if (!host || host.state === "absent") return navigatorAnswer([]);
  const current = (host.threads ?? []).filter(t => JSON.stringify(t.generation) === JSON.stringify(host.generation));
  const runs = host.workflowRoot?.runs ?? [];
  const entries = current.map(t => {
    const mine = runs.filter(r => r.conversation === t.threadId && r.status?.state !== "prepared; WR records pending; not sent");
    const latest = mine.at(-1);
    return { id: t.threadId, home: host.homeRouting?.activeModeHomeClass ?? "account", projectRoot: PROJECT, projectSource: "recorded", title: title(t.name, t.preview), titleSource: t.name ? "name" : t.preview ? "preview" : "none",
      createdAt: null, updatedAt: null, live: live(t.status), needsAnswer: 0, needsAnswerOn: [], archived: null, open: { kind: "loaded", generation: t.generation, threadId: t.threadId },
      run: latest ? run(latest.lifecycle?.end ? "ended" : "open", { runId: latest.reference, workflow: workflow(latest.workflow?.name ?? null), finishedReported: latest.lifecycle?.end ? null : (host.workflowRoot?.offers ?? []).some(o => o?.finished?.run === latest.reference) }) : null,
      runCount: mine.length, childrenRunning: null };
  });
  return navigatorAnswer(host.currentAppProjectContext ? [launched(entries)] : [], host.currentAppProjectContext ? {} : { unassigned: entries });
}
