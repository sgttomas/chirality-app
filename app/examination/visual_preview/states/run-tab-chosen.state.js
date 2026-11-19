// The Run tab for a conversation with a workflow chosen and no run of it (the host's selection for the conversation,
// workflowRoot.runs empty), as in workflow-chosen: the person opened the conversation, then the Run tab.
import workflowChosen from "./workflow-chosen.state.js";
import { selfIssued, pressesAfterMount, openInNavigator, chooseRunTab } from "./_commands.js";

pressesAfterMount("run-tab-chosen", [openInNavigator, chooseRunTab]);

export default { title: "Run tab: define-work chosen, no run started", host: workflowChosen.host, commands: selfIssued() };
