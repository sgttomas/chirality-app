// J1: later in the same session, after the run ended: the person opened History, pressed Read stored conversations (one
// page, read to its end: this App's new home holds only the J1 conversation) and chose that conversation; its turns were
// read (thread/turns/list, summary view). Reading opens nothing. Codex's preview of the conversation is the start of its
// first user message, which is the App's run-start text (the exact length Codex keeps is not reproduced here).
import { defaultRoleBinding, HOME, GEN, THREAD, TURN, PROJECT, MODEL, unix, runStartMessage, historyEmpty } from "./_shared.js";
import { selfIssued, pressesAfterMount, chooseMoreTab, chooseMoreEntry } from "./_commands.js";
import { endedHost } from "./run-ended.state.js";
import { FINISHED_TEXT, COMPLETED_AT } from "./_later.js";

// History is under More: the person opens More, then History in its list.
pressesAfterMount("history", [chooseMoreTab, chooseMoreEntry("history")]);

const ROLE_UNKNOWN = { standing: "unknown", reason: "original request-bound App role/source metadata not supplied; native agentRole, config, runtime record or fork relation does not establish it" }; // native_history.rs role_unknown
// HistorySession::snapshot sets appRole on each listed row and on the selection from the session's role binding: this
// conversation was started in this App session with the default role.
const APP_ROLE = defaultRoleBinding().appRole;
const preview = runStartMessage().content[0].text.split("\n")[0];
const stored = { id: THREAD, cliVersion: "0.169.0", createdAt: unix(2, 0), updatedAt: COMPLETED_AT, cwd: PROJECT, ephemeral: false, modelProvider: "openai", model: MODEL,
  preview, projectId: null, sessionId: "019b2f4e-8c1a-7d3e-9f20-4a6b8c0d2e40", source: "appServer", status: { type: "idle" }, turns: [], name: null,
  path: "/Users/example/Library/Application Support/dev.chirality.app-v4.skeleton/account-homes/account-3b8f2c1d-6e4a-4f0b-9c2d-7a1e5b3c8d90/sessions/2026/11/19/rollout-2026-11-19T09-02-00-019b2f4e-8c1a-7d3e-9f20-4a6b8c0d2e41.jsonl" };
const listPage = { data: [stored], nextCursor: null, backwardsCursor: null };
const turnQuery = { factory_id: 1, query_id: 3, home: HOME, generation: GEN, method: "thread/turns/list", params: { threadId: THREAD, itemsView: "summary", sortDirection: "asc" } };
const turnsPage = { data: [{ id: TURN, status: "completed", itemsView: "summary", startedAt: unix(5, 2), completedAt: COMPLETED_AT, durationMs: (COMPLETED_AT - unix(5, 2)) * 1000, error: null,
  items: [runStartMessage(), { type: "agentMessage", id: "item-msg-4", text: FINISHED_TEXT, phase: "final_answer", memoryCitation: null }] }], nextCursor: null, backwardsCursor: null };
const nativeHistory = { ...historyEmpty([{ native: stored, appRole: APP_ROLE }]), selectionEpoch: 1, listPage, listCursor: { state: "exhausted" },
  readAtReady: { generation: GEN, state: "read-to-end" },
  selected: { threadId: THREAD, state: "indexed-read-only", metadata: stored, turnsPage, turnCursor: { state: "exhausted" }, itemsPage: null, itemCursor: { state: "not-reported" },
    goal: null, goalAvailability: "not-reported", knownChildren: [], receiverReferences: [], childReads: [], resume: null, resumeEligibilityCurrent: false, error: null, errorsByStream: {}, errorHistory: [],
    streamResolutions: { "turn-pages": { query: turnQuery, revision: 1, outcome: "native-result-observed" } }, appRole: APP_ROLE,
    checklists: "not kept in supplier history; prior checklist updates cannot be reconstructed after restart/relaunch", turnDirection: "asc", itemDirection: "desc", itemTurnId: null,
    childGuidance: null, roleLimitObservations: [], originalRoleSupply: null, futureGuidanceNotices: [] },
  pending: [], activeBindingPerformed: false, durableNativeData: false,
  limits: ["Native history is read from the engine; these are disposable page views.", "notLoaded/summary/empty/null/unreported are distinct native facts, not absent events.", "Parent/child status is not return, review or integration.", "ForkedFromId is relation only; original App role stays unknown without bound supply evidence."] };

export default { title: "History: stored conversations read, one selected with its turns", host: endedHost({ nativeHistory }), commands: selfIssued() };
