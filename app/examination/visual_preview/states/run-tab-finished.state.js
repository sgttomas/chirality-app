// The Run tab for run-finished's conversation: the run is open, Codex reports the conversation idle and the host offers
// the finished end the agent's last line names (run_offers.rs read_lines, FN-1), so the tab says "Agent says finished"
// and offers End run as completed beside End run. The native view holds the fileChange items Codex reported
// (native_items.rs NativeView::item), listed under Results. Nothing delegated: nativeView.descendants is empty.
import runFinished from "./run-finished.state.js";
import { selfIssued, pressesAfterMount, chooseConversation, chooseRunTab } from "./_commands.js";

pressesAfterMount("run-tab-finished", [chooseConversation, chooseRunTab]);

export default { title: "Run tab: Agent says finished", host: runFinished.host, commands: selfIssued() };
