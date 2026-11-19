// The open conversation with define-work chosen and picked; the person pressed Start run and the host refused to
// prepare the run (lib.rs workflow_prepare_run → workflow_selection.rs verify_home_within: another reader held the
// history context past the press's wait, HISTORY_BUSY). The composer keeps the text and the
// pick and says, in one sentence, that nothing was sent; the next press goes on from preparing.
import { readyHost, accountRead, CHATGPT_ACCOUNT, signInCompleted, threadRow, workflowRoot, projectLibrary, includedSelection, LIBRARY_REF, historyEmpty, PERSON_TEXT } from "./_shared.js";
import { selfIssued, pressesAfterMount, chooseConversation, chooseWorkflowsTab, pickIncludedCard, typeInComposer, pressStartRun } from "./_commands.js";

pressesAfterMount("pick-not-prepared", [chooseConversation, chooseWorkflowsTab, pickIncludedCard("define-work"), typeInComposer(PERSON_TEXT), pressStartRun]);

export default {
  title: "Start run: the run wasn't prepared",
  host: readyHost({
    ...accountRead(CHATGPT_ACCOUNT), homeOAuth: signInCompleted,
    threads: [threadRow()],
    nativeHistory: historyEmpty(),
    workflowRoot: workflowRoot({ libraries: [projectLibrary], activeLibrary: LIBRARY_REF, selections: [includedSelection("define-work")] }),
  }),
  commands: selfIssued({
    workflow_prepare_run: () => { throw "Native history context is busy; refresh the workflow choice"; },
  }),
};
