// The centre's conversation with several turns, all ended as Codex reported them (turn/completed, TurnStatus completed);
// no turn runs and nothing waits. The person's messages, the agent's prose and each turn's folded activity.
import { readyHost, accountRead, CHATGPT_ACCOUNT, signInCompleted, threadRow, nativeView, historyEmpty } from "./_shared.js";
import { selfIssued, pressesAfterMount, chooseConversation } from "./_commands.js";
import { earlierTurns, earlierTurnReadings, turnObservation, steering } from "./_chat.js";

pressesAfterMount("chat-turns", [chooseConversation]);

export default {
  title: "Conversation: several turns, none running",
  host: readyHost({
    ...accountRead(CHATGPT_ACCOUNT), homeOAuth: signInCompleted,
    threads: [threadRow({ preview: "What is in notes/? Just a short overview, please." })],
    conversationTurns: earlierTurnReadings.map((turn, i) => turnObservation(turn, 20 + i * 10)), steeringTargets: steering(null),
    nativeView: nativeView(earlierTurns, earlierTurnReadings),
    nativeHistory: historyEmpty(),
  }),
  commands: selfIssued(),
};
