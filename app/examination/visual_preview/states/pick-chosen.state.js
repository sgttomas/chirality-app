// The open conversation with define-work picked and already chosen for it (select_production_bundle; the state after
// Start run's first press, which chooses the workflow and stops before anything is sent): the chip, and beside it the
// host's own requirement check for that selection (selection_view declaration, undeclared for every included
// workflow: workflow_declaration::read), and what the person wrote. Start run would now prepare and send.
import { readyHost, accountRead, CHATGPT_ACCOUNT, signInCompleted, threadRow, workflowRoot, projectLibrary, includedSelection, LIBRARY_REF, historyEmpty, PERSON_TEXT } from "./_shared.js";
import { selfIssued, pressesAfterMount, chooseConversation, chooseWorkflowsTab, pickIncludedCard, typeInComposer } from "./_commands.js";

pressesAfterMount("pick-chosen", [chooseConversation, chooseWorkflowsTab, pickIncludedCard("define-work"), typeInComposer(PERSON_TEXT)]);

export default {
  title: "Conversation: define-work picked and chosen, ready to start",
  host: readyHost({
    ...accountRead(CHATGPT_ACCOUNT), homeOAuth: signInCompleted,
    threads: [threadRow()],
    nativeHistory: historyEmpty(),
    workflowRoot: workflowRoot({ libraries: [projectLibrary], activeLibrary: LIBRARY_REF, selections: [includedSelection("define-work")] }),
  }),
  commands: selfIssued(),
};
