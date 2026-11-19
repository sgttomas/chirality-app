// J1: the run is prepared and nothing sent (prepared in the workflow studio, under More; the composer's Start run
// prepares and sends in one press). The conversation keeps the App's default level (full access), as in workflow-chosen.
import { readyHost, accountRead, CHATGPT_ACCOUNT, signInCompleted, threadRow, workflowRoot, projectLibrary, includedSelection, LIBRARY_REF, historyEmpty, runRow } from "./_shared.js";
import { selfIssued, pressesAfterMount, openInNavigator } from "./_commands.js";

// The person opens the conversation from the navigator; it has a run, so the right panel shows Run.
pressesAfterMount("run-prepared", [openInNavigator]);

export default {
  title: "Run prepared, nothing sent",
  host: readyHost({
    ...accountRead(CHATGPT_ACCOUNT), homeOAuth: signInCompleted, threads: [threadRow()], nativeHistory: historyEmpty(),
    workflowRoot: workflowRoot({ libraries: [projectLibrary], activeLibrary: LIBRARY_REF, selections: [includedSelection("define-work")], runs: [runRow("prepared")] }),
  }),
  commands: selfIssued(),
};
