// The Run tab when the agent's turn has ended with a question and no finished line: the run is open, Codex reports the
// conversation idle (threads[].status, hosting.rs thread/status/changed), no request is outstanding (the approval was
// answered), the host offers nothing (run_offers.rs: no line form in the last message) and the native view holds no
// delegated agent (native_items.rs descendants: none). So "Your move" (RunJourney.tsx runWord).
import { readyHost, accountRead, CHATGPT_ACCOUNT, signInCompleted, threadRow, workflowRoot, projectLibrary, includedSelection, LIBRARY_REF, historyEmpty, runRow, turnReadings, nativeView, itemRow, waitingOverview } from "./_shared.js";
import { selfIssued, pressesAfterMount, chooseConversation, chooseRunTab } from "./_commands.js";
import { answered, finishedItems, editsLevel, COMPLETED_AT } from "./_later.js";

pressesAfterMount("run-tab-your-move", [chooseConversation, chooseRunTab]);

export const QUESTION = "The definition now reflects the November soundings. One thing decides how the review step is written: does the survey lead review the draft alone, or with the harbour master?";
// finishedItems up to the last file change, then a question in place of the finished message (agentMessage, final_answer).
export const questionItems = [...finishedItems.slice(0, -1), itemRow({ type: "agentMessage", id: "item-msg-4", text: QUESTION, phase: "final_answer", memoryCitation: null }, 10)];
const turn = turnReadings("completed", { completedAt: COMPLETED_AT });
export const yourMoveHost = (view = nativeView(questionItems, [turn.nativeTurn], [answered])) => readyHost({
  ...accountRead(CHATGPT_ACCOUNT), homeOAuth: signInCompleted, threads: [threadRow({ level: editsLevel })], nativeHistory: historyEmpty(),
  serverRequests: [answered], waitingRequests: waitingOverview([answered]),
  conversationTurns: turn.conversationTurns, turnEventBoundaries: turn.turnEventBoundaries, steeringTargets: turn.steeringTargets, modelTurnExercised: null,
  nativeView: view,
  workflowRoot: workflowRoot({ libraries: [projectLibrary], activeLibrary: LIBRARY_REF, selections: [includedSelection("define-work")], runs: [runRow("open", { levelId: "edits" })], offers: [] }),
});
export default { title: "Run tab: Your move", host: yourMoveHost(), commands: selfIssued() };
