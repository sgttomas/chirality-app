// More › Conversation tools for the open conversation, with the way back to More's list. The App as in workflow-chosen.
import workflowChosen from "./workflow-chosen.state.js";
import { selfIssued, pressesAfterMount, openInNavigator, chooseMoreTab, chooseMoreEntry } from "./_commands.js";

pressesAfterMount("more-conversation-tools", [openInNavigator, chooseMoreTab, chooseMoreEntry("conversation-tools")]);

export default { title: "More: Conversation tools open", host: workflowChosen.host, commands: selfIssued() };
