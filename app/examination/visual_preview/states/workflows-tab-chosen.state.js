// The Workflows tab with the included workflow define-work chosen for the one conversation (select_production_bundle),
// as in the state workflow-chosen; nothing prepared.
import { readyHost, accountRead, CHATGPT_ACCOUNT, signInCompleted, threadRow, workflowRoot, projectLibrary, includedSelection, LIBRARY_REF, historyEmpty } from "./_shared.js";
import { selfIssued, pressesAfterMount, chooseWorkflowsTab, pickIncludedCard } from "./_commands.js";

pressesAfterMount("workflows-tab-chosen", [chooseWorkflowsTab, pickIncludedCard("define-work")]);

export default {
  title: "Workflows tab: define-work picked",
  host: readyHost({
    ...accountRead(CHATGPT_ACCOUNT),
    homeOAuth: signInCompleted,
    threads: [threadRow()],
    nativeHistory: historyEmpty(),
    workflowRoot: workflowRoot({ libraries: [projectLibrary], activeLibrary: LIBRARY_REF, selections: [includedSelection("define-work")] }),
  }),
  commands: selfIssued(),
};
