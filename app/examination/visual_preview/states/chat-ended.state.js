// An ended turn: the third turn ended interrupted (turn/completed with TurnStatus interrupted), its command interrupted
// too (CommandExecutionStatus interrupted). The transcript says the turn was interrupted and claims nothing more.
import { readyHost, accountRead, CHATGPT_ACCOUNT, signInCompleted, threadRow, nativeView, historyEmpty } from "./_shared.js";
import { selfIssued, pressesAfterMount, chooseConversation } from "./_commands.js";
import { earlierTurns, earlierTurnReadings, turnObservation, steering, at, you, agent, command, nativeTurn, TURN_3 } from "./_chat.js";

pressesAfterMount("chat-ended", [chooseConversation]);

const ended = nativeTurn(TURN_3, "interrupted", 5, 6);
const stopped = { ...command("c-3", "head -5 notes/soundings-2026-09.csv", null), status: "interrupted", aggregatedOutput: null, exitCode: null };
const items = [...earlierTurns,
  at(TURN_3, you("u-3", "Yes, write section 1."), 8),
  at(TURN_3, agent("a-4", "Checking the soundings file for the survey dates first.", "commentary"), 9),
  at(TURN_3, stopped, 10, "interrupted"),
];
const turns = [...earlierTurnReadings, ended];
export default {
  title: "Conversation: the last turn ended interrupted",
  host: readyHost({
    ...accountRead(CHATGPT_ACCOUNT), homeOAuth: signInCompleted,
    threads: [threadRow({ preview: "What is in notes/? Just a short overview, please." })],
    conversationTurns: turns.map((turn, i) => turnObservation(turn, 20 + i * 10)), steeringTargets: steering(null),
    nativeView: nativeView(items, turns),
    nativeHistory: historyEmpty(),
  }),
  commands: selfIssued(),
};
