// Shared parts of the J1 states. Not a state (only *.state.js files are). Every field name, value
// and host sentence here follows the Rust host (app/src-tauri/src) and the front-end tests; the
// function or constant each part rests on is named beside it. What a person, the agent or Codex
// would supply is invented and plainly fictional: the example project, its conversation, the
// agent's messages and commands, opaque identifiers and times.
import manifest from "../../../src-tauri/resources/production_workflows/MANIFEST.json";

// ---- Invented identities (opaque in the host; fixed here so the states agree with each other) ----
export const HOME = "app-home:5f1c0d7e9a2b4c6d8e0f1a3b5c7d9e1f2a4b6c8d0e2f4a6b8c0d2e4f6a8b0c2d"; // hosting::home_identity: "app-home:" + sha256 hex
export const GEN = { appSession: "app-session:7c3e9a1b-2d4f-4e6a-8b0c-1d2e3f4a5b6c", home: HOME, spawnCounter: 1 }; // hosting.rs: generation after spawn
export const PROJECT = "/Users/example/Projects/harbour-survey"; // invented project folder
export const APP_DATA = "/Users/example/Library/Application Support/dev.chirality.app-v4.skeleton"; // tauri.conf.json identifier under the platform's app-data folder
export const ACCOUNT_HOME = `${APP_DATA}/account-homes/account-3b8f2c1d-6e4a-4f0b-9c2d-7a1e5b3c8d90`; // desktop_account_homes + opaque_id("account-")
export const SETTINGS_FOLDER = `${APP_DATA}/shared-settings/settings-9d2e4f6a-1b3c-4d5e-8f7a-0b1c2d3e4f5a`; // SETTINGS + opaque_id("settings-")
export const RESOURCES = "/Users/example/dev/chirality-app/app/src-tauri/target/debug"; // a development build's resource folder (invented location)
export const THREAD = "019b2f4e-8c1a-7d3e-9f20-4a6b8c0d2e41"; // Codex thread IDs are UUIDv7
export const TURN = "019b2f51-0a3c-7e5f-8b12-6c8d0e2f4a63";
export const SOURCE_REF = "workflow-source:4e2a6c8d-0f1b-4a3c-9e5d-7b9d1f3a5c7e"; // HomeSession::workflow_source_ref (opaque)
export const LIBRARY_REF = "workflow-library:2c4e6a8b-0d1f-4b3d-8e5f-9a1b3c5d7e9f"; // an opened library's reference (opaque)
export const MODEL = "example-model"; // invented model ID: no real model is named in these files
export const PROVIDER = "openai";
export const EMAIL = "harbour.surveyor@example.com"; // invented account
export const PLAN = "plus"; // AccountStatus.tsx PLAN_TYPES
export const at = (minute, second = 0) => `2026-11-19T09:${String(minute).padStart(2, "0")}:${String(second).padStart(2, "0")}Z`;
export const unix = (minute, second = 0) => Math.floor(Date.parse(at(minute, second)) / 1000);

/** attachments::native_path_identity on unix. */
export const nativePath = text => ({ encoding: "unix_bytes", bytes: [...new TextEncoder().encode(text)] });

// ---- The included workflows: workflow_catalog.rs ProductionCatalog::parse, mapped as
// WorkflowRootSession::snapshot reports each entry (runtime_session.rs). ----
export const SNAPSHOT_METHOD = "chirality.app.workflow-package.sha256/v1"; // workflow_workspace.rs
export const PRODUCTION_STANDING = "production bundle candidate; not a published release"; // workflow_catalog.rs
export const BUNDLED_STANDING = "bundled with this App build (WR LS-5); runs without A15; this build is a release candidate, not a published release";
export const RELEASE_SUBJECT = "chirality-library:library-v3.4.0";
export const includedIdentity = pkg => ({ kind: "workflow", origin: "bundled", source_root: RELEASE_SUBJECT, name: pkg.name, revision: pkg.revision, revision_method: SNAPSHOT_METHOD });
const byName = [...manifest.packages].sort((a, b) => (a.name < b.name ? -1 : a.name > b.name ? 1 : 0)); // BTreeMap order
export const productionCatalog = {
  standing: PRODUCTION_STANDING,
  source: manifest.source,
  // A development build records its own resource folder as the installed bundle (configure_installed_bundle), so each
  // entry the manifest names resolves there and is runnable with no limit.
  entries: byName.map(pkg => ({ name: pkg.name, revision: pkg.revision, origin: "bundled", sourceRoot: RELEASE_SUBJECT, revisionMethod: SNAPSHOT_METHOD,
    identity: includedIdentity(pkg), runnable: true, runLimit: null, bundledStanding: BUNDLED_STANDING,
    description: pkg.description, central: pkg.central, compatibility: pkg.compatibility, roles: pkg.roles, navigation: pkg.navigation,
    libraryExecution: pkg.library_execution, libraryPathsNamed: pkg.library_paths_named })),
};
export const packageOf = name => manifest.packages.find(pkg => pkg.name === name);

/** workflow_declaration::read on a WORKFLOW.md with no declaration block (none of the 71 has one). */
export const undeclared = { raw: null, reading: "undeclared", categories: { checkpoints: "undeclared", expected_inputs: "undeclared", required_tools: "undeclared", returned_evidence: "undeclared", returned_outputs: "undeclared" }, elements: {}, findings: [] };

// ---- Permission level: hosting_level.rs level_status / chosen_view, codex_level.rs and codex_levels.json ----
export const LEVELS = {
  full: { id: "full", dimensions: { writes: "everywhere", network: "on", asks: "never" }, approvalPolicy: "never", sandbox: "danger-full-access", sandboxPolicy: { type: "dangerFullAccess" } },
  edits: { id: "edits", dimensions: { writes: "project", network: "off", asks: "when-beyond-the-sandbox" }, approvalPolicy: "on-request", sandbox: "workspace-write",
    sandboxPolicy: { type: "workspaceWrite", writableRoots: [], networkAccess: false, excludeTmpdirEnvVar: true, excludeSlashTmp: true },
    workspaceWrite: { network_access: false, exclude_slash_tmp: true, exclude_tmpdir_env_var: true, writable_roots: [] } },
};
const READING_SENTENCE = "Reading is not limited at any permission level.";
const APP_DEFAULT_SENTENCE = "The App's default level, not chosen by you. You can choose another level at any time.";
const APP_DEFAULT_EXPLAINED = "The App's default level is full access: commands run with no sandbox, with your account's access to your files and the network, including the App's own records and settings. You can choose another level at any time.";
const SUPERVISED_ALLOWING = "When a command needs your approval, Codex asks. If you allow it, the command can run outside the sandbox, with your account's access to all your files and to the network; Codex cannot run it limited to this project. Your own rules and hooks can allow or refuse a command without asking you.";
const DEFAULT_SCOPE_SENTENCE = "Changing the level here changes the default for new conversations and for saved conversations that have no level of their own. Conversations with their own level keep it.";
const FOLLOWS_DEFAULT_SENTENCE = "This conversation follows the default. Changing the default changes its level until you set a level for this conversation.";
const TRUST_UNTRUSTED_SENT = "The App sent an untrusted entry for the project root shown below.";
/** chosen_view for the App's default (Origin::AppDefault). */
export const appDefaultView = scope => ({ id: "full", dimensions: LEVELS.full.dimensions, ledgerEntry: null, chosenAt: null, scope, reading: "not-limited", readingSentence: READING_SENTENCE,
  origin: "app-default", recorded: "not-recorded", originSentence: APP_DEFAULT_SENTENCE, explanation: APP_DEFAULT_EXPLAINED });
/** chosen_view for a level the person chose and the ledger recorded (Origin::Chosen). */
export const chosenView = (id, scope, entry, chosenAt) => ({ id, dimensions: LEVELS[id].dimensions, ledgerEntry: entry, chosenAt, scope, reading: "not-limited", readingSentence: READING_SENTENCE,
  origin: "chosen", recorded: "recorded", ...(LEVELS[id].approvalPolicy !== "never" ? { allowing: SUPERVISED_ALLOWING } : {}) });
/** The top-level level fields of a home whose launch read found no level chosen, after an earlier session (read_levels_with_account_state). */
export const levelStatus = () => ({
  levelDefaultScopeSentence: DEFAULT_SCOPE_SENTENCE, levelChoiceSave: null, levelDefault: appDefaultView("default"), levelStartRefusal: null, levelSendRefusal: null,
  levelLaunchRead: { state: "read", accepted: [], refused: [], appDefault: "full" }, levelRecordMissing: null, levelAskPreselected: null, levelRecordsUnread: null,
  levelAppDefault: "full", levelSessionOnlyOffered: null,
});
/** TrustReading::status_for_write(true) for a project the person's settings do not mark (TrustCase::Unmarked). */
export const projectTrust = { case: "unmarked", sent: "untrusted", requested: "untrusted", lines: [TRUST_UNTRUSTED_SENT], projectRoot: PROJECT, sentKey: PROJECT, requestedKey: PROJECT, matchedKey: null, readAt: null, standing: "Folders and keys are supplied text." };
/** A conversation row's `level` (level_status), for a conversation started at `levelId` with Codex's reply agreeing. */
export function threadLevel({ levelId = "full", chosen = null, sentAt = at(2, 1), startRef = "request:thread-start-1" } = {}) {
  const level = LEVELS[levelId];
  const fields = { approvalPolicy: level.approvalPolicy, approvalsReviewer: "user", sandbox: level.sandbox,
    config: { ...(level.workspaceWrite ? { sandbox_workspace_write: level.workspaceWrite } : {}), projects: { [PROJECT]: { trust_level: "untrusted" } } } };
  const row = {
    chosen: chosen ?? appDefaultView("default"),
    sent: { method: "thread/start", requestRef: startRef, levelId, fields, chosen: chosen?.ledgerEntry ?? null, writeResult: "written", at: sentAt, projectTrust },
    reported: { from: "thread/start", at: sentAt, requestRef: startRef, requestedLevelId: levelId, approvalPolicy: level.approvalPolicy, approvalsReviewer: "user", sandbox: level.sandboxPolicy, agreement: "agrees", differs: [] },
    agreement: "agrees", takesEffect: "now", projectTrust,
  };
  if (row.chosen.scope === "default") row.scopeSentence = FOLLOWS_DEFAULT_SENTENCE;
  return row;
}

// ---- Account: access.rs AccountObservation::snapshot, hosting.rs SourceRequest::evidence and
// account_rpc_observation, auth_rpc.rs project_frame / typed_observation ----
export const CHATGPT_ACCOUNT = { type: "chatgpt", email: EMAIL, planType: PLAN }; // what Codex's account/read returns for a ChatGPT sign-in
/** One account/read as the host records it: the App's own read at ready, answered with `account` (null: no account). */
export function accountRead(account, { requestIdentity = 3, ref = "request:account-read-1" } = {}) {
  const frame = { id: requestIdentity, method: "account/read", params: {} };
  const projected = { requiresOpenaiAuth: true, account: account === null ? null : { type: "chatgpt", detailsUnavailable: true } }; // project_frame for account/read
  const response = { id: requestIdentity, result: projected };
  const lastClientObservation = { generation: GEN, requestIdentity, method: "account/read", outcome: "response-observed-result", writeResult: "written", initiator: { kind: "app-rule", name: "app-at-ready" } };
  return {
    homeAccess: { modeHomeClass: "account", limit: "native source facts; credential validity and actor identity are not inferred", observations: [{
      source: { generation: GEN, home: HOME, requestIdentity, requestRef: ref, frameEvidence: "explicit redacted account projection; not original wire bytes", responseReduced: false, sensitiveFieldsRedacted: true,
        authPolicyStanding: null, authResponseShapeValid: true, attemptedFrame: frame, sentFrame: frame, writeAttemptInProgress: false, effectiveWriteOutcome: "complete source write observed",
        lastClientObservation, writeResult: "written", actualWriteAttemptObserved: true, noAttemptCause: null, canonicalProjectionAvailable: true, sourceLimit: null,
        outcome: "response-observed-result", waitingEnded: false, response, writeError: null, sourceCurrent: true },
      accountObservation: { state: account === null ? "native account null observed" : "native account type observed", account: projected.account, requiresOpenaiAuth: true, identityVerified: false },
      standing: "redacted source facts only; no credential validity/home/actor qualification" }] },
    accountObservation: { home: HOME, generation: GEN, state: "observed", nativeAccount: account, codexAccount: account === null ? null : account.email, identityVerified: false },
  };
}
/** homeOAuth after a browser sign-in Codex reported complete (first-view.test.mjs completed(); runtime_session native_oauth_observation). */
export const signInCompleted = { state: "source-observed", source: { generation: GEN, requestIdentity: 5, observationRef: "oauth-observation:1", phase: "CompletedSuccess", mode: "Browser", actualWriteObserved: true } };

// ---- Conversation rows: hosting.rs ordinary start row (Host start admission) ----
export const NETWORK_DISCLOSURE = { currentSupplierVersion: "0.169.0", observationSourceVersion: "0.158.0", source: "expected-at-pin", observedByApp: false,
  samplingLimits: "historical bounded observations; current child sockets not sampled by this snapshot",
  entries: [
    { phase: "startup", purpose: "supplier-service", destination: "chatgpt.com; github.com/openai/plugins", condition: "provider/plugin/account dependent; plugins follow user configuration" },
    { phase: "thread-start", purpose: "model", destination: "selected model provider", detail: "Responses websocket prewarm can contact the selected model provider before a turn; default hosted provider observed at 0.158.0" },
  ] };
export function threadRow({ status = { type: "idle" }, level = threadLevel(), preview = null, name = null } = {}) {
  return { generation: GEN, threadId: THREAD, threadSource: "appServer", name, preview, status,
    model: MODEL, modelProvider: PROVIDER, reasoningEffort: "medium", cwd: PROJECT, approvalPolicy: level.reported.approvalPolicy, sandbox: level.reported.sandbox, activePermissionProfile: null,
    supplierStanding: null, requestedDestination: { source: "person-selected", model: MODEL, modelProvider: PROVIDER }, reportedDestination: { scope: "thread", model: MODEL, modelProvider: PROVIDER },
    networkDisclosure: NETWORK_DISCLOSURE, level, ...defaultRoleBinding() };
}

// ---- Roles: resources/instructions/roles.json (role_supply.rs RoleSet), lib.rs role_set_metadata,
// conversation_roles.rs limit_account / limit_entries / frozen_limit_account, role_lifecycle.rs RoleInForce ----
import roleSet from "../../../src-tauri/resources/instructions/roles.json";
const CONTENT_METHOD = "chirality.app.exact-bytes.sha256/v1";
const ROLES_SHA256 = "e4dd8fe201337e10e3113dc0077472dd4e0ba0cf8c868122303a477260df23c0"; // shasum -a 256 resources/instructions/roles.json
const GUIDANCE_SHA256 = { HELP_HUMAN: "88aee799de1f7e8d490fd6e4b30affee17d3a2654ff67a4628ac4d45dc834ad3", HELPS_HUMANS: "771453ac033e038c7ee26bce397e02fedbf7e021ed1d4dd5c7ebb48a73e012ae",
  WORKING_ITEMS: "051a57528a1de4e549aa18f03c1acd7e685977c81b5f9c8085f391c2bed48cc8", TASK: "c11c1020dcf50ecd9fd596c65aab4add5e263bf786d60dcb6fdd479b7e588908" }; // resources/instructions/agents/AGENT_*.md, the seeded defaults
export const ROLE_SET = { available: true, roles: roleSet.roles, defaultRole: "HELP_HUMAN", conversationRoles: ["HELP_HUMAN", "HELPS_HUMANS", "WORKING_ITEMS"],
  identity: { method: CONTENT_METHOD, value: ROLES_SHA256 }, standing: "candidate; U-R6 open" };
const LIMIT_ALL = { limitId: "L-ALL-1", statement: "Work within the brief's write targets", basis: "A brief is text; Codex sandbox and approval are the person's own settings (D3), not role enforcement", notEnforcement: ["brief-text", "worktree", "sandbox", "approval-policy"], standing: "stated-not-enforced", presentedAs: "Stated, not enforced" };
const LIMIT_TASK = { limitId: "L-TASK-1", statement: "A task agent does not delegate", basis: "DECISION-K3 K-10; stated in the shipped TASK guidance; no supplier control is named at the pin", notEnforcement: ["approval-policy", "sandbox", "user-configuration", "depth-limit"], standing: "stated-not-enforced", presentedAs: "Stated, not enforced" };
const limitsOf = role => (role === "TASK" ? [LIMIT_TASK, LIMIT_ALL] : [LIMIT_ALL]);
export const ROLE_LIMITS = { available: true, notRead: [],
  account: { format: "chirality.role.limits", formatVersion: "0.2", accountId: `lim:${ROLES_SHA256}`, appRelease: "chirality-app-v4-unqualified-group-a-entry", supplierPin: "0.169.0",
    roles: roleSet.roles.map(r => ({ role: r.name, meaning: r.meaning, delegation: r.delegation, guidanceState: "default", guidanceContent: { method: CONTENT_METHOD, value: GUIDANCE_SHA256[r.name] }, limits: limitsOf(r.name) })) },
  standing: "Stated in the role's guidance; Codex does not enforce it. Approval policy, sandbox, your configuration and the depth limit are not this limit's enforcement." };
export const SUPPLY_REF = "sup:3f5b7d9e-1a2c-4e6f-8a0b-2c4e6f8a0b2c";
/** The role fields host_tick::project_status_history copies onto a conversation started with the default role
 * (HistorySession::role_details with a binding). The composed instructions' own content is not reproduced here. */
export const defaultRoleBinding = () => ({
  appRole: { standing: "app-observed", role: "HELP_HUMAN", supply_ref: SUPPLY_REF },
  roleRelation: { kind: "start" },
  suppliedLimitAccount: { subject: { kind: "original-supply", suppliedTo: THREAD, supplyRef: SUPPLY_REF, thisConversation: true },
    basis: "made once from the composition supplied at that start; no guidance file is read for it", standing: "established",
    account: { format: "chirality.role.limits.observation", formatVersion: "0.1", role: "HELP_HUMAN", roleSet: { method: CONTENT_METHOD, value: ROLES_SHA256 },
      limits: [LIMIT_ALL], basis: "original App composition; role instructions do not establish supplier enforcement" } },
  futureGuidanceNotices: [],
});

// ---- The ready host: lib.rs host_status, for an App launched from a saved setup with a project ----
export function readyHost(over = {}) {
  const host = {
    state: "ready", generation: GEN, generationClosed: false, lastStartRefusal: null, startRefusalCause: null, build: "development",
    supplierStanding: null, versionIdentity: null, verification: null, declaredCapabilities: { experimentalApi: true, requestAttestation: false, explicitGatewayOauth: true } /* hosting.rs initialize */, configurationIdentity: null, lifecycle: null, distributionSuccessor: null,
    networkDisclosure: NETWORK_DISCLOSURE,
    clientRequests: [], clientRequestObservationStanding: "Canonical rows are last observations; an in-flight native write has unknown current outcome, never a current no-send or complete-write proof.",
    reservedNativeRequests: [], inFlightNativeWrites: [], serverRequests: [], recordsCapability: null, serverRequestEndContexts: [],
    recovery: null, recoveryPendingObservations: [], recoveryProjectionLimits: [], recoveryPersistenceError: null, recoveryInitializationError: null,
    journal: [], observerRetention: null, observerRebuild: null, continuationContexts: [], turnEventBoundaries: [], accountNamespaceRevision: 0, malformedFrames: [],
    threads: [], planMode: { state: "not-checked", reason: "collaboration modes not read for this Codex generation", experimental: true, presets: null } /* plan_mode_availability */, requestedModes: [], conversationTurns: [], turnInterruptRequests: [], stopRequests: [], modelTurnExercised: false,
    modelTurnEvidence: { standing: "provider/model execution not established by request or mock result", protocolRequests: [] }, unansweredTurnStarts: [],
    ...levelStatus(),
    nativeView: nativeView([]), accountObservation: null, nativeViewLimits: [], observerCursor: { generation: GEN, position: 40 }, observerGap: false, priorNativeViews: [], nativeViewObservationEnded: false,
    accessSelection: null,
    recoveryInitialization: { state: "configured", historyLimits: [], hostConfigured: true,
      path: { displayPath: `${APP_DATA}/runtime/recovery.ledger.jsonl`, nativePath: { encoding: "native_encoded_bytes", platform: "macos", bytes: [...new TextEncoder().encode(`${APP_DATA}/runtime/recovery.ledger.jsonl`)] }, pathDisplayLimit: null },
      database: `${APP_DATA}/runtime/recovery.ledger.sqlite`, historyFile: "existing", configurationError: null, directoryPublication: "sync-calls-succeeded", blocksSupplierStart: false,
      standing: "App-observed recovery pointers; no native human-act proof" },
    codexHome: HOME,
    roleSupply: null, roleSet: ROLE_SET, compiledDevelopmentSelection: null,
    desktopSetup: savedSetupView(),
    providerEndpointEdit: { available: false, standing: "Source metadata only; a fresh private user-layer offer and two explicit native decisions remain required" },
    providerCreate: { available: false, standing: "Source metadata only; fresh private absence/version proof and two native decisions remain required" },
    nativeHistory: historyEmpty(),
    roleLimits: ROLE_LIMITS,
    steeringTargets: [],
    homeRouting: { activeModeHomeClass: "account", entries: [{ modeHomeClass: "account", generation: GEN, state: "ready", configurationLimit: null }], limit: "mode selection does not transfer native threads; each source retains its full generation/home" },
    waitingRequests: waitingOverview([]),
    codexHomeRules: { appSentence: LASTING_RULES_APP_SENTENCE, homes: [{ home: ACCOUNT_HOME, lastingRules: { state: "none", readAt: at(1, 2), files: [], skippedEntries: 0 }, modeHomeClass: "account" }] },
    homeAccess: { modeHomeClass: "account", observations: [], limit: "native source facts; credential validity and actor identity are not inferred" },
    hostTicks: null,
    workflowRoot: workflowRoot(),
    homeOAuth: null, continueAs: null,
    codexStops: { outcomes: [], stopWaitLimitSeconds: 10, records: STOP_RECORDS }, // codex_stop.rs STOP_WAIT_LIMIT, RECORDS_LIMIT
    currentAppProjectContext: { reference: PROJECT, sourceCaption: "configured App directory", standing: "explicit frozen Root observation; no native/actor authority inferred" },
    currentAppProjectContextLimit: null,
    attachmentSelections: attachmentSelections(),
    attachmentCustody: { state: "opened", root: `${APP_DATA}/attachments` },
    configuredProviderReadRevision: null, providerOfferReadRevision: null, accessSettingsReadRevision: null,
    // hosting.rs applied_session_settings over HostConfig::new's session flags for the account home.
    codexSessionSettings: [{ setting: "analytics.enabled=false", reason: "Turns off Codex's analytics traffic." },
      { setting: 'model_provider="openai"', reason: "Codex runs a conversation only on the provider it was started with, so this home's Codex is started on its built-in OpenAI provider, whatever default your Codex settings name. Your files are not changed." }],
    ...over,
  };
  // lib.rs host_status: one steering target (or its reason) for each current conversation.
  if (!("steeringTargets" in over)) host.steeringTargets = host.threads.length ? IDLE_STEERING : [];
  return host;
}
export const LASTING_RULES_APP_SENTENCE = "Conversations already open hold the rules as they were when Codex started them, so this is the file as read at the time shown, not necessarily what a running conversation applies."; // lasting_rules.rs APP_SENTENCE

const STOP_RECORDS = "Recorded in the App's recovery ledger: a codex_stop record when you confirm, then a stop-request record for each interrupt before it is sent, with its outcome. After a relaunch the App reads the turns' labels back from these records. A record the ledger has not accepted is shown as not yet written and kept in this App process; the stop still proceeds. The outcome panel itself is kept in this App process only.";
/** waiting_requests::overview: one group per conversation with known answerable outstanding requests. */
export function waitingOverview(requests) {
  const groups = [];
  for (const request of requests) {
    if (request.state !== "outstanding" || request.classification !== "known-answerable" || request.originClass === "named-service") continue;
    const group = groups.find(g => g.threadId === request.nativeParameters.threadId);
    if (group) group.count += 1; else groups.push({ modeHomeClass: "account", generation: GEN, threadId: request.nativeParameters.threadId, count: 1 });
  }
  return { groups, sources: [{ modeHomeClass: "account", generation: GEN, state: "ready", count: groups.reduce((n, g) => n + g.count, 0) }],
    coverage: "Known answerable requests awaiting the person in ready, current local registers of all configured App conversation homes. Sequential snapshots, not an atomic cross-home observation; counts can change before opening. No supplier read." };
}
/** AttachmentSelection snapshot (runtime_session.rs) with the launch source lib.rs host_status substitutes for a saved desktop launch. */
export const attachmentSelections = () => ({ ownerRef: "attachment-owner:6b8d0f2a-4c6e-4a8c-9e0b-2d4f6a8c0e2b", listRevision: 0, selections: [], operation: null, submissions: [],
  launchAppProjectObservation: { source: "explicit saved desktop request, revalidated this launch", nativeRoot: nativePath(PROJECT),
    associationStanding: "launch source only; no accepted REC context/persistent thread-project binding established by this picker" },
  workflowRun: "no workflow run is supplied with attachments; a draft reaches a trial as its trial text, never as attachments (WR TT-3, NIR AT-8), so a draft's files you attach are ordinary attachments",
  submissionStanding: "private source handles; each immutable submission has its own source outcome below", custody: "private App memory; DTO/path/hash cannot construct a selection" });

/** NativeView::snapshot_with_requests (native_items.rs) for this generation, with `items` and `turns`. */
export function nativeView(items, turns = [], requests = []) {
  const withRequests = items.map(item => {
    const request = [...requests].reverse().find(r => r.nativeParameters?.threadId === item.threadId && r.nativeParameters?.turnId === item.turnId && r.nativeParameters?.itemId === item.native.id);
    return request ? { ...item, requestRef: { generation: request.generation, requestIdentity: request.requestIdentity }, settlementOrigin: null, ...(request.state === "outstanding" ? { displayState: "waiting-on-request" } : {}) } : item;
  });
  return { home: HOME, generation: GEN, position: 40, observationEnded: false, supplierStanding: null, distributionEvidence: null,
    items: withRequests, revisions: [], descendants: [], turns, modelReroutes: [], turnErrors: [], unreadableTurnErrors: [],
    turnRecords: turns.map(turn => ({ threadId: THREAD, turnId: turn.id })), typesPin: "0.169.0", goals: {}, checklistGaps: [],
    limits: ["Tool success is not checking, acceptance or reliance.", "Parent completion says nothing about children.", "Child completion, return, review and integration are not inferred.", "Plan item references require this receiving home namespace; standalone cross-home export remains unsupported."] };
}

/** The stored conversations read for this Codex session, to the end (runtime_session.rs HistorySession snapshot, read_history_at_ready). */
export function historyEmpty(threads = []) {
  return { state: "history-receiving", home: HOME, generation: GEN, selectionEpoch: 0, threads, listCursor: { state: "exhausted" }, listError: null, dispatches: [], startReceipts: [],
    readAtReady: { generation: GEN, state: "read-to-end" }, childAssociations: [], roleLimitObservations: [], listDirection: "desc", receivingLimits: [] };
}

// ---- Desktop setup: desktop_startup.rs DesktopSetup::view ----
const SUPPLIER = { selection: "bundled-owner-use-development", path: `${RESOURCES}/codex/bin/codex`,
  standing: "Explicit owner-use development only. Label/generated-reference/binary assertion checks still apply; derived byte identity is not authenticated qualification. A compiled production successor still refuses without installed custody." };
const NEXT_LAUNCH = "Preparation/save changes only a pending request. Quit normally when ready and launch again; no automatic quit, restart, login, conversation or model selection.";
const setupBase = { appData: APP_DATA, noProjectFolder: `${APP_DATA}/conversations-without-project`, workingFiles: `${APP_DATA} Working Files`, workingFilesKept: null, appDataProblem: null,
  supplier: SUPPLIER, activeResourceProblem: null, custodyProblem: null, nextLaunch: NEXT_LAUNCH };
/** First launch on a new machine: no saved request (resolve → saved_launch → admit_root). */
export const setupRequiredView = () => ({ ...setupBase, retainProject: { available: false, reason: "Retaining an account requires this process's admitted saved-desktop source; no environment, pending or setup-only adoption" },
  launch: { state: "setup-required", reason: "No explicit desktop request saved", operationalData: "not admitted; setup-only local input capability retained" },
  pending: null, activeResources: null });
/** The saved request's pending view after prepare_and_save for new settings (resources as OwnedHomePlan::prepare observed them). */
export const pendingSave = () => ({ state: "saved-for-next-launch", accountHome: ACCOUNT_HOME, project: PROJECT,
  resources: ["config.toml", "AGENTS.md", "skills"].map(name => ({ name, state: "Linked", limit: null })),
  standing: "Pending request only; the current workspace, homes, records, attachments, recovery, choices and prepared messages are unchanged" });
/** A launch from the saved request (resolve → saved-request), as every later launch reports it. */
export const savedSetupView = () => ({ ...setupBase, retainProject: { available: true, accountHome: ACCOUNT_HOME },
  launch: { state: "saved-request", standing: "Fresh launch revalidated explicit desktop sources; supplier qualification remains unavailable" },
  pending: null, activeResources: null });

// ---- The workflow part: host_tick::workflow_status (WorkflowRootSession::snapshot, offers,
// decorate_selected_compatibility, decorate_status) and workflow_selection::publish_context ----
export const ROOT_LIMIT = "actual hot registrations and the App's own included LS-5 workflows may run; development, library-held and other production bundle candidate selections are shown, never run (TT-1/TX-1); runs open and end only by their recorded lifecycle; compatibility is advisory; no cold file authority or model adoption claim";
/** The project library as WorkflowRootSession::open_project_library leaves it for a new project: nothing registered, entries not yet looked for. */
export const projectLibrary = { reference: LIBRARY_REF, root: nativePath(PROJECT), origin: "project", sourceRoot: PROJECT, reconciliation: null, registered: [], registrationEvidence: null,
  entryListing: { state: "not observed", entries: [], limits: [], standing: "Refresh library entries to observe this library" } };
/** The recorded runs read at launch (lib.rs LaunchRead → reopen_recorded_runs → read_reopened_history): none in a new
 * project (record_supply.rs RunsReading::view_bounded, with the history notices attached and readAt). */
export const REOPENED_EMPTY = { runs: [], limits: [], standing: "reopened from project records only; completion is never inferred from a native turn, and no live process run is claimed", historyNotices: [], readAt: at(1, 3) };
export function workflowRoot(over = {}) {
  return { productionCatalog, selections: [], inspection: null, libraries: [], assuranceSetting: null, activeLibrary: null, activeReview: null, reviews: [], runs: [],
    afterRunEnd: null, reopened: REOPENED_EMPTY, reopenedNotRead: null, restartLimits: [], endedAfterRelaunch: [], drafts: null, trialPointerLimits: [], limit: ROOT_LIMIT,
    offers: [], projectLibraryAvailable: true, pendingTrials: [], pendingBringBacks: [], trialConversations: [], trialsStartedHere: [], trialTurns: [], trialChildren: [],
    context: { sourceRef: SOURCE_REF, generation: GEN, historyEpoch: 0 }, ...over };
}
/** selection_view for an included workflow selected for this conversation (select_production_bundle, LS-5). */
export function includedSelection(name, { selectedAt = at(3, 10), reference = "selection:5a7c9e1b-3d5f-4a7c-9e1b-3d5f7a9c1e3b" } = {}) {
  const pkg = packageOf(name);
  return { sourceRef: SOURCE_REF, threadId: THREAD, selection: { reference, identity: includedIdentity(pkg), standing: BUNDLED_STANDING, assurance: null,
    package: nativePath(`${RESOURCES}/workflows/${name}`), currentLimit: null, selectedAt, replaces: null, newerRevision: null, runnable: true, runLimit: null, declaration: undeclared } };
}

// ---- A workflow run of define-work in this conversation: runtime_session.rs WorkflowRun::view / lifecycle_view,
// workflow_workspace.rs compose_run_text / PreparedRunText::start / turn_params, hosting.rs turn_start_prepared_run_text ----
import defineWorkText from "../../../src-tauri/resources/production_workflows/define-work/WORKFLOW.md?raw";
export const RUN_REF = "run:workflow:8e0a2c4e-6a8c-4e0a-9c2e-4a6c8e0a2c4e"; // opaque_id("run:workflow:")
export const CLIENT_MESSAGE = "workflow-message:0c2e4a6c-8e0a-4c2e-8a4c-6e8a0c2e4a6c"; // opaque_id("workflow-message:")
export const PERSON_TEXT = "Define the work for the harbour survey's summary report: what the report must cover, who reviews it, and what counts as done. The survey notes are in notes/.";
const DEFINE_WORK = packageOf("define-work");
const SUPPLY_FOLDER = ".chirality/workflow-supply/define-work/2d8f18aa3453810e855a366b3f6697320d735541ac92c1bce6d1a70ae3d3c05e/define-work"; // package_copy::content_folder, storage::key(revision)
/** compose_run_text for define-work as an included (bundled) workflow, its other file supplied as a project copy (TX-7 (c)). */
export function runStartText() {
  const rev = DEFINE_WORK.revision.slice(0, 12);
  return [
    `[Chirality] Workflow run start: define-work from the bundled library "${RELEASE_SUBJECT}", revision ${rev}, run ${RUN_REF}. Follow the workflow between the two markers below for this run, until the person ends the run.`,
    `[Chirality] When you judge this workflow finished, end the message with a line of its own "Workflow finished: bundled:define-work". To propose that another registered workflow runs next, end the message with a line of its own "Next workflow: <origin>:<name>", where <origin> is project, user, bundled or host; when you write both, the finished line comes just before it. The person decides; nothing ends or starts until they confirm.`,
    `[Chirality] Other files of this revision, in the folder "${SUPPLY_FOLDER}": resources/walkthroughs.md (sha256 7ecf52be6397)`,
    `<<<chirality-workflow define-work@${rev} begin>>>`,
  ].join("\n") + `\n${defineWorkText}\n<<<chirality-workflow define-work@${rev} end>>>`;
}
/** The userMessage Codex records for the run's turn/start (turn_params: the run text, then the person's text). */
export const runStartMessage = () => ({ type: "userMessage", id: "item-user-1", clientId: CLIENT_MESSAGE,
  content: [{ type: "text", text: runStartText(), text_elements: [] }, { type: "text", text: PERSON_TEXT, text_elements: [] }] });
const RECORDS = { selection: "wr-record:selection:2a4c6e8a-0c2e-4a6c-8e0a-2c4e6a8c0e2a", runText: "wr-record:run-text:4c6e8a0c-2e4a-4c8e-8a0c-4e6a8c0e2a4c" }; // opaque record references
const FILES = { basis: "supply copy in the project (written, recomputed)", folder: SUPPLY_FOLDER, retention: "never rewritten or removed by the App; if deleted, the next run preparation recreates it" };
/** The turn/start SourceRequest evidence (hosting.rs SourceRequest::evidence) for the run's start, at `levelId`. */
function runStartSource(levelId) {
  const level = LEVELS[levelId];
  const frame = { id: 12, method: "turn/start", params: { threadId: THREAD, clientUserMessageId: CLIENT_MESSAGE, input: runStartMessage().content,
    approvalPolicy: level.approvalPolicy, approvalsReviewer: "user", sandboxPolicy: level.sandboxPolicy } };
  const response = { id: 12, result: { turn: { id: TURN, items: [], status: "inProgress", error: null, startedAt: unix(5, 2), completedAt: null, durationMs: null } } };
  return { generation: GEN, home: HOME, requestIdentity: 12, requestRef: "request:turn-start-run", frameEvidence: "original source frame", responseReduced: false, sensitiveFieldsRedacted: false,
    authPolicyStanding: null, authResponseShapeValid: null, attemptedFrame: frame, sentFrame: frame, writeAttemptInProgress: false, effectiveWriteOutcome: "complete source write observed",
    lastClientObservation: { generation: GEN, requestIdentity: 12, method: "turn/start", outcome: "response-observed-result", writeResult: "written" }, writeResult: "written",
    actualWriteAttemptObserved: true, noAttemptCause: null, canonicalProjectionAvailable: true, sourceLimit: null, outcome: "response-observed-result", waitingEnded: false,
    response, writeError: null, sourceCurrent: true };
}
const LIFECYCLE = { prepared: "prepared; not a run until its start turn is observed", open: "open (live); only the person's explicit end ends it", ended: "ended by the person" };
/** One run row of workflowRoot.runs at `stage` ("prepared", "open" or "ended"); `end` is the run_end_cause when ended. */
export function runRow(stage, { levelId = "full", end = null, finishedReport = null, endedAfterTurn = null } = {}) {
  const sent = stage !== "prepared";
  const status = sent
    ? { state: "native workflow-text turn observed; run opened", records: RECORDS, replyStatus: "inProgress", observedStatus: "inProgress", supplied: "not yet checked", adoption: "unknown",
        runStanding: "open until the person ends it; a failed or completed native turn does not end it" }
    : { state: "prepared; WR records pending; not sent", recorded: false, sent: false, supplied: "not supplied", adoption: "unknown", runStanding: "not opened: a run opens when its start turn is observed", otherFiles: FILES };
  return {
    reference: RUN_REF,
    runText: { record_kind: "run_text", purpose: "run start", framing: "WR-FRAME-1", run: RUN_REF, conversation: THREAD, workflow: includedIdentity(DEFINE_WORK), holding_library: null,
      workflow_file: { path: "WORKFLOW.md", content: { method: "chirality.app.exact-bytes.sha256/v1", value: "0b4fa7c4e12a8edffaba9ad80dc5923b337a6b99c945689dd17c8e600e22e4dc" }, bytes: 6201 },
      chain: null, origin_of_start: "selected by the person", selection: "selection:5a7c9e1b-3d5f-4a7c-9e1b-3d5f7a9c1e3b",
      other_files: [{ path: "resources/walkthroughs.md", sha256: "7ecf52be63972e05900acacc00b4ebc3c039bbd8ff9ed87bf86313850bf00a55" }] },
    project: nativePath(PROJECT),
    publication: sent ? { state: "selection and run_text recorded before send", selection: RECORDS.selection, runText: RECORDS.runText }
      : { state: "pending; not recorded", selection: RECORDS.selection, runText: RECORDS.runText, lastFailure: null },
    source: sent ? runStartSource(levelId) : null, turn: sent ? TURN : null, status, supply: null,
    checks: [], pendingRecords: !sent, lifecycle: { state: LIFECYCLE[stage], follows: null, end: end ? { run: RUN_REF, cause: end } : null, records: [] },
    conversation: THREAD, endNotice: null, noticeRecordFailure: null, noticeChecks: [], compatibility: [], checkpointRecorder: null, fileActEntries: [],
    workflow: { origin: "bundled", name: "define-work", revision: DEFINE_WORK.revision, sourceRoot: RELEASE_SUBJECT },
    home: HOME, generation: GEN, runTag: null, endedAfterTurn, finishedReport,
    adoption: "unknown", runStanding: "lifecycle as recorded below; completion is never inferred from a native turn", preparationOrder: 0,
  };
}
/** The status's turn readings for the run's turn (hosting.rs remember_turn, conversationTurns; turnEventBoundaries). */
export function turnReadings(status, { completedAt = null } = {}) {
  const nativeTurn = { id: TURN, items: [], status, error: null, startedAt: unix(5, 2), completedAt, durationMs: completedAt ? (completedAt - unix(5, 2)) * 1000 : null };
  const completed = status !== "inProgress";
  return {
    conversationTurns: [{ generation: GEN, threadId: THREAD, turnId: TURN, nativeTurn, source: completed ? "turn/completed" : "turn/started", receiptPosition: completed ? 39 : 14, terminalEventObserved: completed, observationEnded: false,
      appTurnStart: { collaborationMode: false, requestRef: "request:turn-start-run", requestedContext: null } }],
    turnEventBoundaries: [{ generation: GEN, threadId: THREAD, turnId: TURN, method: "turn/started", status: "inProgress", position: 14 },
      ...(completed ? [{ generation: GEN, threadId: THREAD, turnId: TURN, method: "turn/completed", status, position: 39 }] : [])],
    steeringTargets: [completed
      ? { generation: GEN, threadId: THREAD, target: null, reason: "current live steering target is unavailable or ambiguous; refresh native observations" }
      : { generation: GEN, threadId: THREAD, target: { generation: GEN, threadId: THREAD, turnId: TURN, source: "turn/started", receiptPosition: 14,
          standing: "current observed target; actual Host rechecks full source/generation/target at send and response; no lifecycle outcome inferred" } }],
    nativeTurn,
  };
}
export const IDLE_STEERING = [{ generation: GEN, threadId: THREAD, target: null, reason: "current live steering target is unavailable or ambiguous; refresh native observations" }];
/** One native item row as NativeView::item keeps a completed item received live. */
export const itemRow = (native, order, state = "completed") => ({ threadId: THREAD, turnId: TURN, native, displayState: state, standing: "live-observed", observationEnded: false,
  observedOrder: order, receipt: { generation: GEN, started: 15 + order * 2, ...(state === "completed" ? { completed: 16 + order * 2 } : {}) } });

// ---- First launch on a new machine: setup required, nothing operational started (desktop_startup.rs resolve →
// saved_launch "No explicit desktop request saved" → admit_root), so no Codex process and no App project ----
const NO_REQUEST = "No explicit desktop request saved";
export function setupHost(over = {}) {
  return readyHost({
    state: "absent", generation: null, generationClosed: false, declaredCapabilities: null,
    planMode: { state: "not-offered", reason: "experimental API not declared for this Codex connection", experimental: true, presets: null },
    nativeView: null, nativeViewObservationEnded: false, observerCursor: { generation: null, position: 0 },
    configurationProblem: NO_REQUEST, codexHome: null, codexSessionSettings: null,
    levelDefault: null, levelLaunchRead: null, levelAppDefault: "full",
    desktopSetup: setupRequiredView(),
    nativeHistory: { state: "unavailable", readAtReady: null, limits: [], durableNativeData: false, childAssociations: [], roleLimitObservations: [], startReceipts: [] },
    homeRouting: { activeModeHomeClass: "account", entries: [{ modeHomeClass: "account", generation: null, state: "absent", configurationLimit: NO_REQUEST }], limit: "mode selection does not transfer native threads; each source retains its full generation/home" },
    waitingRequests: { groups: [], sources: [{ modeHomeClass: "account", generation: null, state: "absent", count: 0 }], coverage: waitingOverview([]).coverage },
    codexHomeRules: { appSentence: LASTING_RULES_APP_SENTENCE, homes: [{ home: null, lastingRules: { state: "not-known", readAt: null, files: [], skippedEntries: 0, reason: "Not read yet." }, modeHomeClass: "account" }] },
    homeAccess: { modeHomeClass: "account", observations: [], limit: "native source facts; credential validity and actor identity are not inferred" },
    workflowRoot: workflowRoot({ projectLibraryAvailable: false, reopened: null,
      reopenedNotRead: { state: "not read", words: "No project is open, so there are no recorded runs to read.", detail: "no explicit App project", project: null },
      context: { sourceRef: SOURCE_REF, generation: null, historyEpoch: null } }),
    currentAppProjectContext: { reference: null, sourceCaption: "App project not established", standing: "explicit frozen Root observation; no native/actor authority inferred" },
    currentAppProjectContextLimit: "no explicit App project",
    attachmentSelections: { ...attachmentSelections(), launchAppProjectObservation: { source: "desktop setup required", nativeRoot: null,
      associationStanding: "launch source only; no accepted REC context/persistent thread-project binding established by this picker" } },
    recoveryInitialization: { state: "not-initialized", historyLimits: [], hostConfigured: false, path: null, database: null, historyFile: "not-established", configurationError: null,
      directoryPublication: "not-confirmed", blocksSupplierStart: false, standing: "App-observed recovery pointers; no native human-act proof" },
    ...over,
  });
}
/** desktop_setup_new_settings_preview (DesktopSetup::preview_new_settings over preview) for the project chosen. */
export function newSettingsPreview(project = PROJECT) {
  return { defaults: { heading: "What applies by default", sentences: [
      "With new settings, Codex's own defaults apply; the App sets none of these.",
      "By default, Codex can read any file your Mac account can read, inside and outside your project, so choose a project folder with that in mind.",
      "By default your ChatGPT sign-in is kept as a file, auth.json, in the sign-in folder listed under Exact locations, readable only by your account. Connection and access shows where Codex keeps it before you sign in.",
      "After you reopen the App, Connection and access shows what Codex reports for this launch.",
    ] },
    token: "desktop-preview-7e9a1c3e-5a7c-4e9a-8c1e-3a5c7e9a1c3e", kind: "new-settings", affirmative: "Create settings and save for next launch", accountHome: ACCOUNT_HOME,
    effects: [
      "Create a new settings folder for this App, inside its data folder",
      "In it, create an empty config.toml, an empty AGENTS.md and a skills folder; Codex adds its own system skills there, and its own working files to the sign-in folder, when it starts",
      "Create a new sign-in folder for this App, linked to those settings",
      `Project when you next open the App: ${project ?? "none"}`,
      "Save these choices privately for the next launch",
    ],
    project,
    // OwnedHomePlan::inspect before anything exists: the settings files are not yet there (state as the plan reads a missing target).
    resources: ["config.toml", "AGENTS.md", "skills"].map(name => ({ name, state: "TargetMissing", source: "source unavailable; no fallback or content copy", limit: null })),
    standing: "Nothing is created until you confirm. No other Codex settings, home or credential is read, imported or changed.",
    settings: SETTINGS_FOLDER,
    locations: [{ name: "Settings folder", path: SETTINGS_FOLDER }, { name: "Sign-in folder", path: ACCOUNT_HOME }, { name: "Saved choices", path: `${APP_DATA}/desktop-startup/request.json` }],
  };
}
