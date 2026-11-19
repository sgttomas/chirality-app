// The conversation of chat-turns in a project whose fleet records are all present and read complete, with no return
// awaiting review, and no decision package: every source of "Waiting on you" is read whole and nothing waits, so the
// top line says only "Nothing is waiting" (WaitingOnYou.tsx nothingWaiting). The fleet packet is the one
// fleet_records::read_for_workspace gives for a project whose .chirality/fleet folder holds an empty coordination log.
import { readyHost, accountRead, CHATGPT_ACCOUNT, signInCompleted, threadRow, nativeView, historyEmpty } from "./_shared.js";
import { selfIssued, pressesAfterMount, chooseConversation, fleetPacket } from "./_commands.js";
import { earlierTurns, earlierTurnReadings, turnObservation, steering } from "./_chat.js";

// The returns are read on the App's 15-second timer and each time the list is opened: the list is opened once, which
// reads them, and closed again, as a person glancing at it would.
const waitingLine = doc => doc.querySelector("#waiting-on-you > summary");
const closedAgain = doc => doc.querySelector("#waiting-on-you[open]") && /^Nothing is waiting$/.test(waitingLine(doc)?.textContent ?? "") ? waitingLine(doc) : null;
pressesAfterMount("chat-quiet", [chooseConversation, waitingLine, closedAgain]);

const readComplete = source => ({ ...source, status: "read", complete: true });
const fleetRead = () => {
  const packet = fleetPacket();
  return { ...packet, limits: [],
    coordination: { ...packet.coordination, project: readComplete(packet.coordination.project), protectedLog: readComplete(packet.coordination.protectedLog) } };
};

export default {
  title: "Conversation: every source read whole, nothing waiting",
  host: readyHost({
    ...accountRead(CHATGPT_ACCOUNT), homeOAuth: signInCompleted,
    threads: [threadRow({ preview: "What is in notes/? Just a short overview, please." })],
    conversationTurns: earlierTurnReadings.map((turn, i) => turnObservation(turn, 20 + i * 10)), steeringTargets: steering(null),
    nativeView: nativeView(earlierTurns, earlierTurnReadings),
    nativeHistory: historyEmpty(),
  }),
  commands: selfIssued({ read_fleet_records: fleetRead() }),
};
