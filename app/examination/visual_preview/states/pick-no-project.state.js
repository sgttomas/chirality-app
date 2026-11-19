// An App launched with no project folder (lib.rs host_status: currentAppProjectContext unavailable; host_tick.rs
// workflow_status projectLibraryAvailable false, since state.workspace is None) and define-work picked in a new chat.
// Preparing would refuse ("No explicit App project (CHIRALITY_WORKSPACE)…", runtime_session.rs prepare_run_with), so
// Start run is not offered and the composer says where to set one.
import { readyHost, accountRead, CHATGPT_ACCOUNT, signInCompleted, workflowRoot, historyEmpty, PERSON_TEXT } from "./_shared.js";
import { selfIssued, availableModels, pressesAfterMount, chooseWorkflowsTab, pickIncludedCard, typeInComposer, pressNewChat } from "./_commands.js";

pressesAfterMount("pick-no-project", [pressNewChat, chooseWorkflowsTab, pickIncludedCard("define-work"), typeInComposer(PERSON_TEXT)]);

export default {
  title: "No project folder: a run needs one",
  host: readyHost({
    ...accountRead(CHATGPT_ACCOUNT), homeOAuth: signInCompleted,
    nativeHistory: historyEmpty(),
    currentAppProjectContext: null, currentAppProjectContextLimit: "explicit App project reference not established",
    workflowRoot: workflowRoot({ projectLibraryAvailable: false }),
  }),
  commands: selfIssued({ read_available_models: availableModels }),
};
