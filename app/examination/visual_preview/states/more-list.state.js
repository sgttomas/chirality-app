// The right panel's More tab as it opens: its list of Make a workflow, History and Conversation tools, one line each.
// The App as in workflow-chosen: one conversation, define-work chosen for it, nothing run.
import workflowChosen from "./workflow-chosen.state.js";
import { selfIssued, pressesAfterMount, openInNavigator, chooseMoreTab } from "./_commands.js";

pressesAfterMount("more-list", [openInNavigator, chooseMoreTab]);

export default { title: "More: its list", host: workflowChosen.host, commands: selfIssued() };
