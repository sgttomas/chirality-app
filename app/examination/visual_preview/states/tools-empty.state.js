// An open conversation with nothing observed yet, its Conversation tools tab shown and the activity's "Activity
// source and limits" opened: where the conversation's tools carry what the centre no longer does (NativeActivity.tsx
// ActivitySource): that no activity is observed, and where the activity is read from and its limits.
import { readyHost, accountRead, CHATGPT_ACCOUNT, signInCompleted, threadRow, historyEmpty } from "./_shared.js";
import { selfIssued, pressesAfterMount, chooseConversation } from "./_commands.js";

const chooseToolsTab = doc => doc.getElementById("right-tab-conversation-tools");
// Opened and brought into view, as a person scrolling the tab to it would.
const openActivitySource = doc => {
  const summary = doc.querySelector('#conversation-tools-content section[aria-label="Activity"] details > summary');
  summary?.closest("section")?.scrollIntoView({ block: "start" });
  return summary;
};
pressesAfterMount("tools-empty", [chooseConversation, chooseToolsTab, openActivitySource]);

export default {
  title: "Conversation tools: an empty conversation's activity, its source and limits",
  host: readyHost({
    ...accountRead(CHATGPT_ACCOUNT), homeOAuth: signInCompleted,
    threads: [threadRow()],
    nativeHistory: historyEmpty(),
  }),
  commands: selfIssued(),
};
