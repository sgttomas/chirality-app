// The run of define-work after its approval was answered (shared by run-finished, run-ended and history). Not a state.
import { GEN, THREAD, TURN, PROJECT, LEVELS, at, unix, itemRow, chosenView } from "./_shared.js";
import { items as openItems, approval } from "./run-open.state.js";

export const FINISHED_TEXT = "The work definition is in work/report-definition.md. It now reflects the latest soundings from the shared repository: the report must cover depth changes against the previous survey, the areas below charted depth, and what the board is asked to note. The survey lead reviews it before it goes to the board; it is done when the survey lead accepts the draft and its figures match the latest soundings.\n\nWorkflow finished: bundled:define-work";
const shell = command => `/bin/zsh -lc '${command}'`;
// native_requests.rs records(): answered by the person (Allow once), the reply written and Codex's resolution observed after it.
export const answered = { ...approval, state: "answered", replyWriteResult: "written",
  acknowledgmentObservation: { status: "observed", what: "serverRequest/resolved after written reply" },
  settlement: { kind: "answer", origin: { class: "person-via-interaction", actorRef: "actor:person:1d3f5b7d-9f1b-4d3f-8b5d-7f9b1d3f5b7d" }, nativeContent: { decision: "accept" } } };
export const finishedItems = [
  ...openItems,
  itemRow({ type: "commandExecution", id: "item-cmd-3", command: shell("git fetch origin"), commandActions: [{ type: "unknown", command: "git fetch origin" }], cwd: PROJECT, processId: null, source: "agent",
    status: "completed", aggregatedOutput: "From example.org:harbour/survey\n   3c1d2e4..8f9a0b1  main       -> origin/main\n", exitCode: 0, durationMs: 1840 }, 7),
  itemRow({ type: "commandExecution", id: "item-cmd-4", command: shell("git show origin/main:soundings-2026-11.csv | head -5"), commandActions: [{ type: "unknown", command: "git show origin/main:soundings-2026-11.csv | head -5" }],
    cwd: PROJECT, processId: null, source: "agent", status: "completed",
    aggregatedOutput: "point,depth_m,charted_m\nNB-01,6.2,6.5\nNB-02,5.8,6.0\nNB-03,4.9,5.5\nNB-04,6.6,6.5\n", exitCode: 0, durationMs: 52 }, 8),
  itemRow({ type: "fileChange", id: "item-patch-2", status: "completed", changes: [{ path: `${PROJECT}/work/report-definition.md`, kind: { type: "update", move_path: null },
    diff: "@@ -6,3 +6,4 @@\n ## Must cover\n-- Depth changes against the previous survey\n+- Depth changes against the previous survey, using the November soundings\n - Areas below the charted depth\n" }] }, 9),
  itemRow({ type: "agentMessage", id: "item-msg-4", text: FINISHED_TEXT, phase: "final_answer", memoryCitation: null }, 10),
];
// The conversation's own level, as in run-open.
const LEVEL_ENTRY = "level-chosen:6c8e0a2c-4e6a-4c8e-9a0c-2e4a6c8e0a2c";
export const editsLevel = { chosen: chosenView("edits", "conversation", LEVEL_ENTRY, at(4, 30)),
  sent: { method: "turn/start", requestRef: "request:turn-start-run", levelId: "edits", fields: { approvalPolicy: "on-request", approvalsReviewer: "user", sandboxPolicy: LEVELS.edits.sandboxPolicy }, chosen: LEVEL_ENTRY, writeResult: "written", at: at(5, 1) },
  reported: { from: "thread/start", at: at(2, 1), requestRef: "request:thread-start-1", requestedLevelId: "full", approvalPolicy: "never", approvalsReviewer: "user", sandbox: { type: "dangerFullAccess" }, agreement: "agrees", differs: [] },
  agreement: "not-confirmed", takesEffect: "now" };
/** run_offers.rs: the finished report the host recognises in the run's last agent message (FinishedReport::view) and the offer row. */
export const finishedMessage = { threadId: THREAD, turnId: TURN, itemId: "item-msg-4" };
export const finishedReport = { message: finishedMessage, run: "run:workflow:8e0a2c4e-6a8c-4e0a-9c2e-4a6c8e0a2c4e", statement: "Workflow finished: bundled:define-work",
  standing: "the agent's statement in its message; the person ended the run" };
export const finishedOffer = { message: finishedMessage, finished: finishedReport, proposal: null };
export const COMPLETED_AT = unix(9, 12);
export { GEN };
