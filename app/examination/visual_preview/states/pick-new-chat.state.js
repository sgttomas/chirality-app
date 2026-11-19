// New chat with a workflow picked: the person pressed New chat, chose a model, picked the included workflow define-work
// under Workflows ("Use in message") and wrote what it should work on. Nothing is started or sent: the pick is the
// renderer's alone (WorkflowPick.tsx), so the host holds no selection and no conversation for it yet. The chip names the
// workflow from the catalogue entry (runtime_session.rs snapshot productionCatalog); its tools are not shown, since the
// host checks them only for a selection in a conversation (workflow_proposal_advisory.rs decorate_selected_compatibility).
import { readyHost, accountRead, CHATGPT_ACCOUNT, signInCompleted, threadRow, workflowRoot, projectLibrary, LIBRARY_REF, historyEmpty, PERSON_TEXT } from "./_shared.js";
import { selfIssued, availableModels, pressesAfterMount, chooseWorkflowsTab, pickIncludedCard, typeInComposer, pressNewChat, chooseListedModel } from "./_commands.js";

pressesAfterMount("pick-new-chat", [pressNewChat, chooseListedModel("example-model"), chooseWorkflowsTab, pickIncludedCard("define-work"), typeInComposer(PERSON_TEXT)]);

export default {
  title: "New chat: define-work picked, what to work on written",
  host: readyHost({
    ...accountRead(CHATGPT_ACCOUNT), homeOAuth: signInCompleted,
    threads: [threadRow({ preview: "What is in notes/? Just a short overview, please." })],
    nativeHistory: historyEmpty(),
    workflowRoot: workflowRoot({ libraries: [projectLibrary], activeLibrary: LIBRARY_REF }),
  }),
  commands: selfIssued({ read_available_models: availableModels }),
};
