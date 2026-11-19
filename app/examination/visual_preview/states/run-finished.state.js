// J1: the approval was answered (Allow once), the turn completed and Codex reports the conversation idle; the run is still
// open, and the agent's last message ends with the line "Workflow finished: bundled:define-work", which the host
// recognises (run_offers.rs read_lines, FN-1) and offers as a completed end in the conversation and the Run tab.
import { readyHost, accountRead, CHATGPT_ACCOUNT, signInCompleted, threadRow, workflowRoot, projectLibrary, includedSelection, LIBRARY_REF, historyEmpty, runRow, turnReadings, nativeView, waitingOverview } from "./_shared.js";
import { selfIssued, pressesAfterMount, openInNavigator } from "./_commands.js";
import { answered, finishedItems, editsLevel, finishedOffer, COMPLETED_AT } from "./_later.js";

// The person opens the conversation from the navigator; it has a run, so the right panel shows Run.
pressesAfterMount("run-finished", [openInNavigator]);

const turn = turnReadings("completed", { completedAt: COMPLETED_AT });
export default {
  title: "Run open; the agent wrote Workflow finished",
  host: readyHost({
    ...accountRead(CHATGPT_ACCOUNT), homeOAuth: signInCompleted, threads: [threadRow({ level: editsLevel })], nativeHistory: historyEmpty(),
    serverRequests: [answered], waitingRequests: waitingOverview([answered]),
    conversationTurns: turn.conversationTurns, turnEventBoundaries: turn.turnEventBoundaries, steeringTargets: turn.steeringTargets, modelTurnExercised: null,
    nativeView: nativeView(finishedItems, [turn.nativeTurn], [answered]),
    workflowRoot: workflowRoot({ libraries: [projectLibrary], activeLibrary: LIBRARY_REF, selections: [includedSelection("define-work")], runs: [runRow("open", { levelId: "edits" })], offers: [finishedOffer] }),
  }),
  commands: selfIssued(),
};
