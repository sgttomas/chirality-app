// New chat: signed in with one conversation in this Codex session, none chosen (the person pressed New chat), so the
// centre is the empty conversation with the composer and the new conversation's settings line. Its first message
// would run thread_start, then the ordinary send. The App reads the model list itself (lib.rs read_available_models).
import { readyHost, accountRead, CHATGPT_ACCOUNT, signInCompleted, threadRow, nativeView, historyEmpty } from "./_shared.js";
import { selfIssued, availableModels } from "./_commands.js";
import { earlierTurns, earlierTurnReadings, turnObservation, steering } from "./_chat.js";

export default {
  title: "New chat: the empty conversation",
  host: readyHost({
    ...accountRead(CHATGPT_ACCOUNT), homeOAuth: signInCompleted,
    threads: [threadRow({ preview: "What is in notes/? Just a short overview, please." })],
    conversationTurns: earlierTurnReadings.map((turn, i) => turnObservation(turn, 20 + i * 10)), steeringTargets: steering(null),
    nativeView: nativeView(earlierTurns, earlierTurnReadings),
    nativeHistory: historyEmpty(),
  }),
  commands: selfIssued({ read_available_models: availableModels }),
};
