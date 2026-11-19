// Answers to the commands the web view issues by itself (timers and mount effects), shaped as the
// host's command functions return them (lib.rs). Not a state.
import { PROJECT, nativePath } from "./_shared.js";
const missingSource = (path, home = "selected project") => ({ path, nativePath: nativePath(path), home, line: null });
const fleetLimits = [
  { source: missingSource(".chirality/fleet/briefs"), reason: "fleet folder missing; no empty-work conclusion" },
  { source: missingSource(".chirality/fleet/graphs"), reason: "fleet folder missing; no empty-work conclusion" },
  { source: missingSource(".chirality/fleet/coordination.fleet.jsonl"), reason: "source missing; no empty-work conclusion" },
  { source: missingSource("fleet/coordination.fleet.jsonl", "configured records store"), reason: "source missing; no empty-work conclusion" },
];
export const fleetPacket = () => ({ format: "chirality.fleet.read", formatVersion: "0.2",
  standing: "Read-only file observations. Records say what was recorded, not that it happened. Records retain their claimed recorder. Prepared work, supplier observations, returns, review, integration and human acts remain separate. The workspace derives file-based claims only; it establishes no current native execution or human act.",
  project: { configuredRoot: PROJECT, canonicalRoot: PROJECT, nativeRoot: nativePath(PROJECT), physical: { device: 16777234, inode: 4821907 } },
  schema: { format: "chirality.fleet.record", versions: ["0.1 quoted compatibility", "0.2 native links and delegation"] },
  briefs: [], graphs: [],
  coordination: { project: { source: fleetLimits[2].source, status: "missing", complete: false }, projectRecords: [], protected: { state: "attached" },
    protectedLog: { source: fleetLimits[3].source, status: "missing", complete: false }, protectedRecords: [], governingStoreRecords: [], appObservations: [], nativeRelationships: [], nativeDelegation: [], recordingEvents: [] },
  workspace: { standing: "Derived file-based coordination claims, not native execution, permission, human acceptance or authority. Rebuild writes nothing.", graphIdentityMethod: "chirality.app.exact-bytes.sha256/v1", undertakings: [],
    limits: ["Decision needs remain unknown until their current human-act standing is available; a recorded decision alone is insufficient.",
      "A dispatch is shown only from the App's own recorded observation, tied to an item only by what its record says the brief its spawn prompt named was for, read when the dispatch was recorded; that shows which brief was named, not that the child received or read it. It establishes a child and its parent, never work done, a return, a review or an integration. Legacy 0.1 child observations do not establish a current native relationship."] },
  limits: fleetLimits,
  nativeRecording: "Only actual App Fork/Continue-as source-issued request/result observations produce 0.2 relationships, and only a completed spawn item the App received live produces a 0.2 dispatch, with the child's status as Codex last reported it and the end of its observation. A dispatch is tied to a brief only by the reference in its spawn prompt; the prompt's text is not recorded. Source files are quoted on read, never native authority; 0.1 undertaking fields establish no native join. A dispatch seen only in Codex history is not recorded.",
  delegationReconciliation: null });

export const selfIssued = (over = {}) => ({
  // lib.rs native_confirmation_content: the native confirmations pending in this App process; none.
  native_confirmation_content: [],
  // lib.rs request_answer_companions → request_answer_presentation::companions: no frozen answer snapshot for any request.
  request_answer_companions: [],
  // lib.rs decision_view → runtime_session::read_decision_packages (decision_view.rs derive) on a project with no decision
  // packages: the four arrays WaitingOnYou.tsx reads, empty, with the reader's own two fields.
  decision_view: { rows: [], limits: [], historyNotices: [], unresolvedRecords: [], workspace: PROJECT, readOnly: true },
  // lib.rs read_fleet_records → fleet_records::read_for_workspace on a new project: no .chirality/fleet folder yet, so each
  // source is "missing; no empty-work conclusion" and returns read with limits (WaitingOnYou.tsx returnsReading).
  read_fleet_records: fleetPacket(),
  // lib.rs provider_endpoint_discard → endpoint_checkpoint: the endpoint controller's fresh epoch (provider_endpoint.rs).
  provider_endpoint_discard: "endpoint-source-epoch-1e3c5a7b-9d0f-4b2c-8e4a-6c8e0a2c4e6a",
  // lib.rs read_home_access → runtime_session::read_native_home_access: HomeSession::account_view after the reads,
  // which is the status's homeAccess (the read it makes is already among its observations here).
  read_home_access: (_args, state) => state.host.homeAccess,
  ...over,
});

/**
 * A press the person made in this session that only the renderer holds (such as the conversation the
 * Run a workflow guide is set to), replayed once after the page has rendered, for the named state only:
 * every state module is imported by states/index.js, so the check on the URL keeps it to its own page.
 * `steps` are functions of the document returning an element to click, tried until each is found.
 */
export function pressesAfterMount(state, steps) {
  if (typeof location === "undefined" || new URLSearchParams(location.search).get("state") !== state) return;
  let index = 0, tries = 0;
  const next = () => {
    if (index >= steps.length || tries++ > 200) return;
    const element = steps[index](document);
    if (element) { element.click(); index += 1; }
    setTimeout(next, 100);
  };
  setTimeout(next, 300);
}
/** The run guide's choice of the one conversation (RunJourney.tsx ConversationChoices, group run-conversation). */
export const chooseRunConversation = doc => [...doc.querySelectorAll('input[type="radio"][name="run-conversation"]')].find(input => input.value !== "");
/** The Conversation view's choice of the one conversation (App.tsx ConversationChoices, group current-conversation). */
export const chooseConversation = doc => [...doc.querySelectorAll('input[type="radio"][name="current-conversation"]')].find(input => input.value !== "");
/** lib.rs read_available_models → model_catalog::view, for the account home: a short invented list (no real model is named). */
export const availableModels = (args = {}) => ({ state: "observed", generation: args.generation ?? null,
  models: [
    { id: "example-model", model: "example-model", displayName: "Example model", description: "Invented entry for the preview: a general model.", isDefault: true,
      supportedReasoningEfforts: [{ reasoningEffort: "low", description: "Faster replies" }, { reasoningEffort: "medium", description: "Balanced" }, { reasoningEffort: "high", description: "More reasoning" }], defaultReasoningEffort: "medium" },
    { id: "example-model-mini", model: "example-model-mini", displayName: "Example model mini", description: "Invented entry for the preview: a smaller, faster model.", isDefault: false,
      supportedReasoningEfforts: [{ reasoningEffort: "low", description: "Faster replies" }, { reasoningEffort: "medium", description: "Balanced" }], defaultReasoningEffort: "medium" },
  ],
  complete: true, limits: [], readAt: "2026-11-19T09:02:30Z",
  standing: "Models Codex reports for the app-server's own provider in this Codex generation. A listed model is the supplier's reported availability for that provider, not your account's entitlement or access; Start still checks the current configuration.",
  serverProvider: "openai", serverProviderState: "named", modeHomeClass: args.modeHomeClass ?? "account" });
/** The right panel's Workflows tab (WorkspaceShell.tsx RIGHT_PANEL_TABS). */
export const chooseWorkflowsTab = doc => doc.getElementById("right-tab-workflows");
/** The right panel's Run tab (WorkspaceShell.tsx RIGHT_PANEL_TABS, id current-run). */
export const chooseRunTab = doc => doc.getElementById("right-tab-current-run");
