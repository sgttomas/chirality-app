// A turn running: Codex reported turn/started for the third turn and the App still receives from that process
// (TurnStatus inProgress, observationEnded false); its command is in progress (CommandExecutionStatus inProgress) and
// the host names it the steering target, so the composer offers Update and Stop. Nothing waits for the person.
import { readyHost, accountRead, CHATGPT_ACCOUNT, signInCompleted, threadRow, nativeView, historyEmpty } from "./_shared.js";
import { selfIssued, pressesAfterMount, chooseConversation } from "./_commands.js";
import { earlierTurns, earlierTurnReadings, turnObservation, steering, at, you, agent, command, nativeTurn, TURN_3 } from "./_chat.js";

pressesAfterMount("chat-running", [chooseConversation]);

const running = nativeTurn(TURN_3, "inProgress", 5);
const items = [...earlierTurns,
  at(TURN_3, you("u-3", "Yes, write section 1."), 8),
  at(TURN_3, agent("a-4", "Checking the soundings file for the survey dates first.", "commentary"), 9),
  at(TURN_3, command("c-3", "head -5 notes/soundings-2026-09.csv", null, "inProgress"), 10, "in-progress"),
];
const turns = [...earlierTurnReadings, running];
export default {
  title: "Conversation: a turn running",
  host: readyHost({
    ...accountRead(CHATGPT_ACCOUNT), homeOAuth: signInCompleted,
    threads: [threadRow({ status: { type: "active", activeFlags: [] }, preview: "What is in notes/? Just a short overview, please." })],
    conversationTurns: turns.map((turn, i) => turnObservation(turn, 20 + i * 10)), steeringTargets: steering(running),
    nativeView: nativeView(items, turns),
    nativeHistory: historyEmpty(),
  }),
  commands: selfIssued(),
};
