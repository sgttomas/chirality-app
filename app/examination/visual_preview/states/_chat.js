// Shared parts of the conversation states (the centre's chat). Not a state. Shapes follow the Rust host: native_items.rs
// NativeView (items, turns, turnRecords) and NativeItem rows, hosting.rs conversation_turns and steering_targets (the
// ConversationTurnObservation and SteeringTarget readings turnReadings in _shared.js builds), server_requests.rs
// ServerRequestEntry. Everything a person, the agent or Codex said is invented.
import { GEN, THREAD, TURN, PROJECT, unix } from "./_shared.js";

export const TURN_1 = "019b2f4f-1d2e-7a3b-8c4d-5e6f7a8b9c01"; // UUIDv7, earlier than TURN
export const TURN_2 = TURN;
export const TURN_3 = "019b2f53-6e7f-7a8b-9c0d-1e2f3a4b5c6d";

/** One native item row as NativeView::item keeps an item received live (native_items.rs). */
export const at = (turnId, native, order, state = "completed") => ({ threadId: THREAD, turnId, native, displayState: state, standing: "live-observed", observationEnded: false,
  observedOrder: order, receipt: { generation: GEN, started: 15 + order * 2, ...(state === "completed" ? { completed: 16 + order * 2 } : {}) } });
/** A person's message: ThreadItem userMessage, its content as Codex recorded it. */
export const you = (id, text) => ({ type: "userMessage", id, content: [{ type: "text", text, text_elements: [] }] });
/** An agent's message: ThreadItem agentMessage with its MessagePhase. */
export const agent = (id, text, phase = "final_answer") => ({ type: "agentMessage", id, text, phase, memoryCitation: null });
export const reasoning = (id, summary) => ({ type: "reasoning", id, summary: [summary], content: [] });
const shell = command => `/bin/zsh -lc '${command}'`;
/** ThreadItem commandExecution; `status` is CommandExecutionStatus. */
export const command = (id, cmd, output, status = "completed") => ({ type: "commandExecution", id, command: shell(cmd), commandActions: [{ type: "unknown", command: cmd }], cwd: PROJECT,
  processId: null, source: "agent", status, aggregatedOutput: status === "inProgress" ? null : output, exitCode: status === "inProgress" ? null : 0, durationMs: status === "inProgress" ? null : 40 });

/** ThreadTurn as Codex reports it (TurnStatus: completed, interrupted, failed, inProgress). */
export const nativeTurn = (id, status, startMinute, endMinute = null, error = null) => ({ id, items: [], status, error,
  startedAt: unix(startMinute, 2), completedAt: endMinute === null ? null : unix(endMinute, 0), durationMs: endMinute === null ? null : (unix(endMinute, 0) - unix(startMinute, 2)) * 1000 });
/** hosting.rs conversation_turns: one observation per turn the App started or saw end. */
export const turnObservation = (turn, position) => ({ generation: GEN, threadId: THREAD, turnId: turn.id, nativeTurn: turn,
  source: turn.status === "inProgress" ? "turn/started" : "turn/completed", receiptPosition: position, terminalEventObserved: turn.status !== "inProgress", observationEnded: false,
  appTurnStart: { collaborationMode: false, requestRef: `request:turn-start-${turn.id.slice(-4)}`, requestedContext: null } });
/** hosting.rs steering_targets: the live turn when one runs, otherwise no target and the host's reason. */
export const steering = live => [live
  ? { generation: GEN, threadId: THREAD, target: { generation: GEN, threadId: THREAD, turnId: live.id, source: "turn/started", receiptPosition: 60,
      standing: "current observed target; actual Host rechecks full source/generation/target at send and response; no lifecycle outcome inferred" } }
  : { generation: GEN, threadId: THREAD, target: null, reason: "current live steering target is unavailable or ambiguous; refresh native observations" }];

/** The first two turns every conversation state shares: a question about the survey notes, then a draft outline. */
export const earlierTurns = [
  at(TURN_1, you("u-1", "What is in notes/? Just a short overview, please."), 0),
  at(TURN_1, reasoning("r-1", "Listing the notes folder"), 1),
  at(TURN_1, command("c-1", "ls notes", "field-log-2026-10.md\nsoundings-2026-09.csv\nsurvey-brief.md\n"), 2),
  at(TURN_1, agent("a-1", "There are three files in **notes/**:\n\n- `field-log-2026-10.md`: the October field log\n- `soundings-2026-09.csv`: the September soundings\n- `survey-brief.md`: the brief for the summary report\n\nThe brief asks for a four-page report for the harbour board."), 3),
  at(TURN_2, you("u-2", "Draft an outline for the report."), 4),
  at(TURN_2, command("c-2", "sed -n 1,40p notes/survey-brief.md", "# Harbour survey: summary report\n"), 5),
  at(TURN_2, agent("a-2", "Reading the brief again before I outline.", "commentary"), 6),
  at(TURN_2, agent("a-3", "## Outline\n\n1. Purpose and audience\n2. Depth changes against the previous survey\n3. Areas needing dredging\n4. Next steps\n\n> Each section stays under a page.\n\nShall I write section 1?"), 7),
];
export const earlierTurnReadings = [nativeTurn(TURN_1, "completed", 1, 2), nativeTurn(TURN_2, "completed", 3, 4)];
