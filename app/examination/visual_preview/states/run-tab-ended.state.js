// The Run tab for run-ended's conversation: the person ended the run as completed (run_end_cause "completed"), so the
// tab says "Ended" and "You ended it as completed, on the agent's report." with nothing to act on.
import { endedHost } from "./run-ended.state.js";
import { selfIssued, pressesAfterMount, chooseConversation, chooseRunTab } from "./_commands.js";

pressesAfterMount("run-tab-ended", [chooseConversation, chooseRunTab]);

export default { title: "Run tab: Ended", host: endedHost(), commands: selfIssued() };
