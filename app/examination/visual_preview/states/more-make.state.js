// More › Make a workflow: the Make guide and, below it, the workflow studio with every detailed control, with the way
// back to More's list. The App as in workflow-chosen.
import workflowChosen from "./workflow-chosen.state.js";
import { selfIssued, pressesAfterMount, openInNavigator, chooseMoreTab, chooseMoreEntry } from "./_commands.js";

pressesAfterMount("more-make", [openInNavigator, chooseMoreTab, chooseMoreEntry("make")]);

export default { title: "More: Make a workflow open", host: workflowChosen.host, commands: selfIssued() };
