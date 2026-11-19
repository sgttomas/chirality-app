// J1: the person pressed End as completed, on the agent's report: the run is ended as completed (run_end_cause
// "completed", the finished report kept on the run); its end notice waits for the conversation's next ordinary turn;
// Results lists the run. The host no longer offers the finished end (the run is not in force).
import { readyHost, accountRead, CHATGPT_ACCOUNT, signInCompleted, threadRow, workflowRoot, projectLibrary, includedSelection, LIBRARY_REF, historyEmpty, runRow, turnReadings, nativeView, waitingOverview, TURN } from "./_shared.js";
import { selfIssued, pressesAfterMount, chooseRunConversation } from "./_commands.js";
import { answered, finishedItems, editsLevel, finishedReport, COMPLETED_AT } from "./_later.js";

pressesAfterMount("run-ended", [chooseRunConversation]);

const turn = turnReadings("completed", { completedAt: COMPLETED_AT });
export const endedRun = { ...runRow("ended", { levelId: "edits", end: "completed", finishedReport, endedAfterTurn: TURN }),
  endNotice: { state: "pending: the next ordinary turn in this conversation carries it" } };
export const endedHost = over => readyHost({
  ...accountRead(CHATGPT_ACCOUNT), homeOAuth: signInCompleted, threads: [threadRow({ level: editsLevel })], nativeHistory: historyEmpty(),
  serverRequests: [answered], waitingRequests: waitingOverview([answered]),
  conversationTurns: turn.conversationTurns, turnEventBoundaries: turn.turnEventBoundaries, steeringTargets: turn.steeringTargets, modelTurnExercised: null,
  nativeView: nativeView(finishedItems, [turn.nativeTurn], [answered]),
  workflowRoot: workflowRoot({ libraries: [projectLibrary], activeLibrary: LIBRARY_REF, selections: [includedSelection("define-work")], runs: [endedRun] }),
  ...over,
});
export default { title: "Run ended as completed; Results lists it", host: endedHost(), commands: selfIssued() };
