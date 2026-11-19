// A request waiting: in the running third turn the agent asked the person a question (item/tool/requestUserInput,
// ServerRequestEntry outstanding, not yet answered); Codex reports the conversation active and waiting on user input
// (ThreadActiveFlag waitingOnUserInput). The card is the conversation's; its answers are v4's.
import { readyHost, accountRead, CHATGPT_ACCOUNT, signInCompleted, threadRow, nativeView, historyEmpty, waitingOverview, GEN, THREAD } from "./_shared.js";
import { selfIssued, pressesAfterMount, chooseConversation } from "./_commands.js";
import { earlierTurns, earlierTurnReadings, turnObservation, steering, at, you, agent, nativeTurn, TURN_3 } from "./_chat.js";

pressesAfterMount("chat-waiting", [chooseConversation]);

const running = nativeTurn(TURN_3, "inProgress", 5);
const question = { recordKind: "server-request-entry", requestIdentity: 4, generation: GEN, method: "item/tool/requestUserInput", classification: "known-answerable", originClass: "person-input",
  nativeParameters: { threadId: THREAD, turnId: TURN_3, itemId: "item-question-1", isBlocking: true,
    questions: [{ id: "scope", header: "Scope", question: "Should section 1 cover the whole harbour or only the north basin?", isOther: true, isSecret: false,
      options: [{ label: "North basin only", description: "As the brief's purpose says" }, { label: "Whole harbour", description: "Adds the south channel soundings" }] }] },
  receiptPosition: 64, state: "outstanding", replyWriteResult: "not-attempted", acknowledgmentObservation: { status: "not-observed" },
  subjectReferences: { thread: THREAD, turn: TURN_3, item: "item-question-1" } };
const items = [...earlierTurns,
  at(TURN_3, you("u-3", "Yes, write section 1."), 8),
  at(TURN_3, agent("a-4", "Before I write it, one question about scope.", "commentary"), 9),
];
const turns = [...earlierTurnReadings, running];
export default {
  title: "Conversation: the agent's question waiting for an answer",
  host: readyHost({
    ...accountRead(CHATGPT_ACCOUNT), homeOAuth: signInCompleted,
    threads: [threadRow({ status: { type: "active", activeFlags: ["waitingOnUserInput"] }, preview: "What is in notes/? Just a short overview, please." })],
    serverRequests: [question], waitingRequests: waitingOverview([question]),
    conversationTurns: turns.map((turn, i) => turnObservation(turn, 20 + i * 10)), steeringTargets: steering(running),
    nativeView: nativeView(items, turns, [question]),
    nativeHistory: historyEmpty(),
  }),
  commands: selfIssued(),
};
