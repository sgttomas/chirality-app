// The Run tab for run-open's conversation: the run of define-work is open and Codex has asked for a command approval
// (an outstanding server request for this conversation, hosting.rs server_requests), so the tab says "Needs answer"
// (RunJourney.tsx runWord, runReading's first waiting branch). Everything the agent and Codex said is invented.
import runOpen from "./run-open.state.js";
import { selfIssued, pressesAfterMount, chooseConversation, chooseRunTab } from "./_commands.js";

// The conversation is opened in the centre (the Run tab reads that one), then the tab is selected.
pressesAfterMount("run-tab-needs-answer", [chooseConversation, chooseRunTab]);

export default { title: "Run tab: Needs answer", host: runOpen.host, commands: selfIssued() };
