// The Workflows tab after sign-in: one conversation started and idle; the person opened the
// project's workflows (a new project: nothing registered, entries not yet looked for); nothing chosen for it.
import { readyHost, accountRead, CHATGPT_ACCOUNT, signInCompleted, threadRow, workflowRoot, projectLibrary, LIBRARY_REF, historyEmpty } from "./_shared.js";
import { selfIssued, pressesAfterMount, chooseWorkflowsTab } from "./_commands.js";

// The panel shows Workflows at launch; the press is kept so the state still says which tab it is.
pressesAfterMount("workflows-tab", [chooseWorkflowsTab]);

export default {
  title: "Workflows tab: included workflows, nothing chosen",
  host: readyHost({
    ...accountRead(CHATGPT_ACCOUNT),
    homeOAuth: signInCompleted,
    threads: [threadRow()],
    nativeHistory: historyEmpty(),
    // runtime_session.rs snapshot: the included catalogue as shipped, the project library as open_project_library leaves it.
    workflowRoot: workflowRoot({ libraries: [projectLibrary], activeLibrary: LIBRARY_REF }),
  }),
  commands: selfIssued(),
};
