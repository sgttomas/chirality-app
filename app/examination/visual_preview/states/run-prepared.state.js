// J1: the person described the work and pressed Prepare this run: the run is prepared, nothing sent. The conversation
// keeps the App's default level (full access), as in workflow-chosen.
import { readyHost, accountRead, CHATGPT_ACCOUNT, signInCompleted, threadRow, workflowRoot, projectLibrary, includedSelection, LIBRARY_REF, historyEmpty, runRow } from "./_shared.js";
import { selfIssued, pressesAfterMount, chooseRunConversation } from "./_commands.js";

pressesAfterMount("run-prepared", [chooseRunConversation]);

export default {
  title: "Run prepared, nothing sent",
  host: readyHost({
    ...accountRead(CHATGPT_ACCOUNT), homeOAuth: signInCompleted, threads: [threadRow()], nativeHistory: historyEmpty(),
    workflowRoot: workflowRoot({ libraries: [projectLibrary], activeLibrary: LIBRARY_REF, selections: [includedSelection("define-work")], runs: [runRow("prepared")] }),
  }),
  commands: selfIssued(),
};
