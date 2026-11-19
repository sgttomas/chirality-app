// The Run tab's second form: as run-tab-your-move, but the agent delegated work to another agent earlier in the turn.
// The native view holds that agent as a descendant (native_items.rs, from the collabAgentToolCall's receiverThreadIds:
// statusSource "collabAgentToolCall.agentsStates", lastObservedStatus the call's agentsStates entry, here "completed"
// as of that call), and the host holds no status row of its own conversation (threads has only the parent). An idle
// parent says nothing of it, and the App can't read it, so the tab says "Turn ended", not "Your move".
import { nativeView, itemRow, turnReadings, THREAD } from "./_shared.js";
import { selfIssued, pressesAfterMount, chooseConversation, chooseRunTab } from "./_commands.js";
import { answered, COMPLETED_AT } from "./_later.js";
import { questionItems, yourMoveHost } from "./run-tab-your-move.state.js";

pressesAfterMount("run-tab-turn-ended", [chooseConversation, chooseRunTab]);

const CHILD = "019b2f55-3e7a-7c1d-8a40-2b6d8f0a4c85"; // a Codex thread ID (UUIDv7), invented
const spawn = { type: "collabAgentToolCall", id: "item-agent-1", tool: "spawnAgent", status: "completed", senderThreadId: THREAD, receiverThreadIds: [CHILD],
  prompt: "Check the November soundings file for points below charted depth and list them.", model: null, reasoningEffort: null,
  agentsStates: { [CHILD]: { status: "completed", message: null } } };
// The delegation, received after the last file change; the question after it.
const items = [...questionItems.slice(0, -1), itemRow(spawn, 10), itemRow(questionItems[questionItems.length - 1].native, 11)];
const turn = turnReadings("completed", { completedAt: COMPLETED_AT });
const view = { ...nativeView(items, [turn.nativeTurn], [answered]),
  descendants: [{ threadId: CHILD, parentThreadId: THREAD, parentSource: "collabAgentToolCall.senderThreadId", guidance: "not-known", lastNativeCall: spawn,
    statusSource: "collabAgentToolCall.agentsStates", lastObservedStatus: spawn.agentsStates[CHILD], observationEnded: false }] };
export default { title: "Run tab: Turn ended (a delegated agent the App can't read)", host: yourMoveHost(view), commands: selfIssued() };
