// The Run tab for a conversation that carries no workflow: one conversation started and idle, nothing chosen or run
// (workflowRoot.runs empty, runtime_session.rs snapshot). The tab says so and offers the Workflows tab.
import { readyHost, accountRead, CHATGPT_ACCOUNT, signInCompleted, threadRow, workflowRoot, projectLibrary, LIBRARY_REF, historyEmpty } from "./_shared.js";
import { selfIssued, pressesAfterMount, chooseConversation, chooseRunTab } from "./_commands.js";

pressesAfterMount("run-tab-no-run", [chooseConversation, chooseRunTab]);

export default {
  title: "Run tab: no run in this conversation",
  host: readyHost({ ...accountRead(CHATGPT_ACCOUNT), homeOAuth: signInCompleted, threads: [threadRow()], nativeHistory: historyEmpty(),
    workflowRoot: workflowRoot({ libraries: [projectLibrary], activeLibrary: LIBRARY_REF }) }),
  commands: selfIssued(),
};
