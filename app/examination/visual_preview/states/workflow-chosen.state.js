// J1: after setup, relaunch and sign-in. Signed in with a ChatGPT account (plan reported); the project from
// setup is the App's project; one conversation started and idle, with the default role; the person opened
// the project's workflows and chose the included workflow define-work for that conversation; nothing prepared.
import { readyHost, accountRead, CHATGPT_ACCOUNT, signInCompleted, threadRow, workflowRoot, projectLibrary, includedSelection, LIBRARY_REF, historyEmpty } from "./_shared.js";
import { selfIssued, pressesAfterMount, chooseRunConversation } from "./_commands.js";

// The person chose the conversation in the guide before choosing the workflow; the renderer alone holds that choice.
pressesAfterMount("workflow-chosen", [chooseRunConversation]);

export default {
  title: "Workflow chosen (define-work), nothing prepared",
  host: readyHost({
    ...accountRead(CHATGPT_ACCOUNT),
    homeOAuth: signInCompleted,
    threads: [threadRow()],
    nativeHistory: historyEmpty(),
    workflowRoot: workflowRoot({ libraries: [projectLibrary], activeLibrary: LIBRARY_REF, selections: [includedSelection("define-work")] }),
  }),
  commands: selfIssued(),
};
