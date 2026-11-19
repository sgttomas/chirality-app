// J1: the run of define-work started and open; Codex reports the conversation active and waiting on an approval.
// The App's default level (full access) never asks, so a run at the default raises no request; the request shown
// here arises because the person chose Project edits for this conversation before starting, and the agent asked to
// run a command that needs the network (git fetch). Everything the agent and Codex said is invented.
import { readyHost, accountRead, CHATGPT_ACCOUNT, signInCompleted, threadRow, workflowRoot, projectLibrary, includedSelection, LIBRARY_REF, historyEmpty,
  runRow, turnReadings, nativeView, itemRow, runStartMessage, chosenView, LEVELS, GEN, THREAD, TURN, PROJECT, at, unix, waitingOverview } from "./_shared.js";
import { selfIssued, pressesAfterMount, openInNavigator } from "./_commands.js";

// The person opens the conversation from the navigator; it has a run, so the right panel shows Run.
pressesAfterMount("run-open", [openInNavigator]);

const LEVEL_ENTRY = "level-chosen:6c8e0a2c-4e6a-4c8e-9a0c-2e4a6c8e0a2c";
const reportedAtStart = { from: "thread/start", at: at(2, 1), requestRef: "request:thread-start-1", requestedLevelId: "full", approvalPolicy: "never", approvalsReviewer: "user",
  sandbox: { type: "dangerFullAccess" }, agreement: "agrees", differs: [] };
// hosting_level.rs level_status: the conversation's own level (chosen), last sent on the run's turn/start; Codex confirms a level only
// in a start, resume or fork reply, so the reply on record is still the start's, for full access, and agreement is not confirmed.
const level = { chosen: chosenView("edits", "conversation", LEVEL_ENTRY, at(4, 30)),
  sent: { method: "turn/start", requestRef: "request:turn-start-run", levelId: "edits", fields: { approvalPolicy: "on-request", approvalsReviewer: "user", sandboxPolicy: LEVELS.edits.sandboxPolicy },
    chosen: LEVEL_ENTRY, writeResult: "written", at: at(5, 1) },
  reported: reportedAtStart, agreement: "not-confirmed", takesEffect: "now" };

const shell = command => `/bin/zsh -lc '${command}'`;
const command = (id, cmd, actions, output, durationMs) => ({ type: "commandExecution", id, command: shell(cmd), commandActions: actions, cwd: PROJECT, processId: null, source: "agent",
  status: "completed", aggregatedOutput: output, exitCode: 0, durationMs });
const message = (id, text) => ({ type: "agentMessage", id, text, phase: "commentary", memoryCitation: null });
export const BRIEF = "# Harbour survey: summary report\n\nPurpose: summarise the autumn soundings of the north basin for the harbour board.\n\n- Audience: harbour board, non-specialist\n- Length: about four pages\n- Due: before the December board meeting\n- Latest soundings: on the shared survey repository (not yet in notes/)\n";
export const REPORT_DEFINITION = "# Work definition: harbour survey summary report\n\n## Contribution\nA four-page summary of the autumn soundings of the north basin, written for the harbour board.\n\n## Must cover\n- Depth changes against the previous survey\n- Areas below the charted depth\n- What the board is asked to note or decide\n\n## Reviewed by\nThe survey lead, before it goes to the board.\n\n## Done when\nThe survey lead accepts the draft and the figures match the latest soundings.\n";
export const items = [
  itemRow(runStartMessage(), 0),
  itemRow(message("item-msg-1", "I'll read the survey notes in notes/ before drafting the work definition."), 1),
  itemRow(command("item-cmd-1", "ls notes", [{ type: "listFiles", command: "ls notes", path: "notes" }], "field-log-2026-10.md\nsoundings-2026-09.csv\nsurvey-brief.md\n", 38), 2),
  itemRow(command("item-cmd-2", "sed -n 1,40p notes/survey-brief.md", [{ type: "read", command: "sed -n 1,40p notes/survey-brief.md", name: "survey-brief.md", path: "notes/survey-brief.md" }], BRIEF, 31), 3),
  itemRow(message("item-msg-2", "The brief fixes the audience, length and deadline. I've drafted the work definition from it in work/report-definition.md."), 4),
  itemRow({ type: "fileChange", id: "item-patch-1", status: "completed", changes: [{ path: `${PROJECT}/work/report-definition.md`, kind: { type: "add" },
    diff: REPORT_DEFINITION }] }, 5),
  itemRow(message("item-msg-3", "The brief says the latest soundings are on the shared survey repository, not yet in notes/. I'd like to fetch it so the definition reflects them; that needs network access."), 6),
];
export const approval = { recordKind: "server-request-entry", requestIdentity: 0, generation: GEN, method: "item/commandExecution/requestApproval", classification: "known-answerable", originClass: "a14",
  nativeParameters: { threadId: THREAD, turnId: TURN, itemId: "item-cmd-3", approvalId: null, startedAtMs: unix(6, 40) * 1000, kind: "command", environmentId: null,
    command: shell("git fetch origin"), cwd: PROJECT, commandActions: [{ type: "unknown", command: "git fetch origin" }],
    reason: "Fetch the latest soundings from the shared survey repository; this needs network access.",
    proposedExecpolicyAmendment: ["git", "fetch", "origin"], proposedNetworkPolicyAmendments: null, networkApprovalContext: null, additionalPermissions: null, availableDecisions: null },
  receiptPosition: 31, state: "outstanding", replyWriteResult: "not-attempted", acknowledgmentObservation: { status: "not-observed" },
  subjectReferences: { thread: THREAD, turn: TURN, item: "item-cmd-3" } };

const turn = turnReadings("inProgress");
export default {
  title: "Run open; Codex waiting on a command approval",
  host: readyHost({
    ...accountRead(CHATGPT_ACCOUNT),
    homeOAuth: signInCompleted,
    threads: [threadRow({ status: { type: "active", activeFlags: ["waitingOnApproval"] }, level })],
    serverRequests: [approval], waitingRequests: waitingOverview([approval]),
    conversationTurns: turn.conversationTurns, turnEventBoundaries: turn.turnEventBoundaries, steeringTargets: turn.steeringTargets, modelTurnExercised: null,
    nativeView: nativeView(items, [turn.nativeTurn], [approval]),
    nativeHistory: historyEmpty(),
    workflowRoot: workflowRoot({ libraries: [projectLibrary], activeLibrary: LIBRARY_REF, selections: [includedSelection("define-work")], runs: [runRow("open", { levelId: "edits" })] }),
  }),
  commands: selfIssued(),
};
