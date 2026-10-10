# Chirality App v4 — runtime contract development

Run `APP-V4-GROUP-A-20261004` repairs and extends the walking skeleton from
`APP-V4-GRAPH-CLOSURE-20261004`. The current path hosts stock Codex 0.160.0,
supplies reviewed v4 common/role guidance, receives native requests and activity,
loads external observations, records decision packages, and supplies native controls
for A16 decisions, A15 workflow registration, and A4/A6/A7 App-file acts. Separate
readers retain decision and file-act evidence limits. Group A development remains active;
packaging, supplier qualification and the owner's stage gate are separate work.

Tests use the maintained invented `tests/fixtures/FX-DP1` content. Native
confirmation tests are explicit stand-ins; they do not establish that a person
performed an act.

## Current path

1. The Rust host starts the stock App Server, completes its handshake and keeps
   native frames with full `{appSession, home, spawnCounter}` generation identity.
2. The person chooses a primary role (or none) and explicitly enters a model
   and a configured Codex provider for a new thread. Codex retains its own configuration and permissions. The view
   discloses expected model contact at thread start, before a turn; it does not
   represent that notice as measured socket traffic. Reviewed v4 guidance seeds
   an editable App instruction copy without overwriting edits; new conversations
   read current bytes. Native child roles remain not supplied.
3. The recorder validates package files, records source-faithful requests and
   separately states when the requester identity is unestablished.
4. The host freezes the chosen alternative and all its consequences before
   native Decide/Cancel confirmation. Absent or empty package scope is shown as
   `not named by the package`; a nonempty scope stays unchanged.
5. Capture publication is atomic and durable before the writer prepares a
   record. The writer validates complete entries against embedded JSON Schema
   2020-12 resources before append. New App record IDs are secure UUIDv4 opaque
   tokens. Delayed trusted entries retain their facts, ID and original time.
6. Backlink failure leaves a recorded act with its link pending. Trusted pending
   captures flush before newer confirmations or recorder appends. Cold unverified
   files cannot create a new human act; existing recorded claims keep provenance
   limits when a backlink is repaired.

7. Native request controls keep the full generation and source identity; question
   answers may be partial, form aliases validate their content, and changed
   confirmation context refuses. User-verification acceptance remains unsupported
   under CI-11. Ended/replaced observations keep explicit checklist/history limits.
8. The person can select catalog/read JSON and an optional counterpart through
   native selectors. Rust retains exact bytes in memory; the panel shows complete
   reported content, unverified host origin and comparison/path-display limits.
9. Current native threads accept unchanged text input; live turns can receive an
   explicit interrupt request. Native acknowledgment is separate from turn end or
   rollback. Contradictory late starts cannot revive a completed tuple.
10. An App-owned pointer-only recovery ledger initializes before supplier startup
   at the App user-data `runtime/recovery.ledger.jsonl` path. Initialization errors
   remain visible without blocking native protocol processing or relocating data.

11. Stored native history is read without making a thread operational. Explicit
    Continue uses the latest validated native response and current generation.
    Original role guidance is retained in memory for threads started here; missing
    original guidance is shown as Unknown, independent of native role hints.

12. Native text-file selections retain private handles and an ordered immutable
    source list. Explicit attachment-bearing send or steering uses that whole
    list, durable metadata and the actual Host request; failures do not fall back
    to text-only sending or automatic retry. A native acknowledgment is separate
    from provider uptake or completion. When a run-end notice is pending in the
    conversation (WR TX-5), an attachment-bearing new turn carries it in one
    frame, in NIR TC-2's order: the run-end line, then the person's text, then
    the attachments. The supply records still name only the attachments, in
    their order. The notice is marked sent only once that frame's write was
    attempted; a send refused or failed before then leaves it pending. An
    attachment steer is not a new turn and does not carry it.
13. Explicit App project association comes from configured `CHIRALITY_WORKSPACE`,
    separately from native thread cwd, Codex home and workflow run. Unknown context
    produces no canonical project row. Historical project P remains intact when
    a new submission cites current Q; hot-only associations retain cold limits.
14. Selected examination JSON imports keep their complete declared basis and
    unverified standing independently. General record corrections preserve both
    entries and expose missing, conflicting or incomparable claim relationships.
15. A person can select a saved workspace file and explicitly choose mark checked,
    approve, or rely, with scope and purpose. The host freezes the bytes and
    observes actor/context before native act, decline, or cancel. Definite capture
    failure leaves no captured act; uncertain publication is held separately,
    while a durable capture with a failed record remains retryable without
    recapture. File-act reading is separate from decision packages and preserves
    actor/recorder, cold-origin, current-content and professional-statement limits.
    Request/output/workflow links open the standing facility only through a person;
    they do not invent an arrival reference or settle a supplier request.
16. Workflow selection, owner-held review, hot A15 capture and immutable library
    registration are connected to prepared input and source-owned native page
    comparison. Code and synthetic checks do not establish a native person's
    registration, provider uptake or completed workflow execution.
17. The selected conversation shows its native activity readably: messages,
    reasoning summaries, plan items and checklist revisions, tool rows and
    descendants, grouped by turn in native start order and, within a turn, in
    the order this App first received each item. Each row keeps the native item
    and status beside its display reading; unknown, not-completed and
    result-not-supplied stay distinct, and no act, return or integration is
    inferred. Agent text, reasoning summaries, plans and command output stream
    as labelled previews that the completed native item replaces. Stored-history
    pages the person reads (turns, items, thread read) are added as
    recovered-from-supplier rows; nothing is rebuilt automatically. Only a plan
    observed live shows a revision number in this conversation. A row the view
    cannot read shows its JSON instead of breaking the view.
18. Plan mode (experimental) is offered only when this Codex connection declared
    the experimental API and Codex lists a `plan` preset. Sending in plan or
    default mode puts `collaborationMode` on `turn/start` with the conversation's
    reported model and null developer instructions; it is ordinary input, never
    a recorded act. Codex keeps the mode until another is sent; the App shows
    the last mode it requested. A pending run-end notice goes first in a mode
    turn too, with its `collaborationMode` unchanged. A mode that cannot be
    sent is refused before the notice is touched.
19. Codex's requests are shown readably beside the conversation they belong to:
    tool permissions (command, file change, extra permissions, legacy forms),
    questions and input requests. A card names what is asked (command, working
    folder, reason, proposed rules, changes, requested permissions), states the
    register's state in words and offers the native forms with App words beside
    the verbatim native value; a tool-permission card says it is tool permission
    only and its words never say accept or approve. Classification, answer values
    and register checks are unchanged. A card and its activity row link to each
    other; the row never answers. The top of the App counts requests waiting for
    the person, per conversation; opening one answers nothing. Requests of other
    conversations stay listed under Native requests.
20. Workflow run offers come only from agent messages this App observed complete
    live. On the exact `Workflow finished: ‹origin›:‹name›` line naming the run in
    force, the message offers **End run**; the host re-reads the message and
    records cause *completed*. Any other end is "ended by the person"; no command
    can record *completed* without that observed report. On the exact
    `Next workflow: ‹origin›:‹name›` line naming one registered workflow held in
    this session, the message offers **Start ‹workflow› (proposed by the agent)**,
    or **End ‹A› and start ‹B›** while a run is in force (*completed* when the same
    message reports A finished). The proposal selects nothing until the person
    presses; the selection is then recorded as "agent proposal confirmed by the
    person". Unresolved proposals show their notice. The activity view marks run
    starts and ends from the App's run records and folds the supplied run text.
21. **Save a workflow** starts from a draft list. Under the owner's OI-008 ruling for
    the draft workspace ("A, proceed with the Rust host."), the Rust host observes
    the open library's `.chirality/workflow-drafts/` folders. **Open this App
    project's workflow library** opens the explicit `CHIRALITY_WORKSPACE`; the
    folder pickers still open other libraries. For each draft the host reports
    its content identity, the hygiene findings (HY-1…HY-5, HY-7), its WR §5.1
    state and its App-recorded base, or that it has none. Attribution names a
    Codex file-change item or an App action, or reads "not observed". Sizes are
    bounded from metadata before any file is read and again by a running read
    budget. Package files are opened no-follow and non-blocking relative to their
    opened folder: links, FIFOs and devices are refused. Transitions are
    observed only when the list is read; the folder is not watched.
    **Try in a conversation** adds the draft's text files, as listed, each with
    its draft reference (NIR AT-8), to the attachment list. It sends nothing. A
    pre-filled draft file cannot be re-confirmed as an ordinary source. The person
    chooses an ordinary conversation and sends. Draft files are refused for a
    conversation with a workflow run in force. An acknowledged send keeps one
    App-kept trial pointer per draft (TT-4), which survives a relaunch.
    Non-text files are listed "not attached". *Owner decision (WR U-WR-24,
    2026-10-10), not yet implemented:* WR §4.2 replaces this pre-fill with a
    trial that mirrors a real run. **Try with the authoring agent** pre-fills a
    message asking the authoring conversation's agent to run the draft's trial
    text through one sub-agent and report. **Try in a fresh conversation** is
    optional and opens a new conversation with the trial text pre-filled; its
    transcript can be brought back to the authoring conversation. Supporting
    files are named as a registered run names them. WR §17 is the
    implementation plan; until it lands the App behaves as described above.
    **Review for registration…** opens the existing review for the listed
    content, refused as DS-6 if the draft changed since listing.
    Registration stays the person's A15 act at the native confirmation. A trial
    is not a run, registration, checking or acceptance.
22. **Stop Codex…** and **Restart Codex…** always ask first (DEL-01-04 §5.2,
    C-12). A native question lists the live turns, waiting requests, delegated
    agents and workflow runs in force in that home, or says none were observed,
    and waits with no time limit. **Keep Codex running** is the default; it and
    Cancel change nothing. On **Stop Codex** or **Restart Codex**, the host
    stops sending new turns and steers (text, mode, workflow or attachment) to
    that Codex process. It then assesses the live work again; if the list
    changed since it was shown, the host reopens and asks again with the
    current list. The App writes `turn/interrupt` for every observed live turn
    before waiting. It then waits on one shared deadline for the
    acknowledgments and for Codex to report those turns ended, then stops the
    process (HOSTING §4.5). All of this stays within the stop wait limit of
    10 s (U-R4 test value). Each turn then shows one of the four TO-4 labels:
    "interrupted by Stop Codex", "completed (Stop Codex requested)",
    "failed (Stop Codex requested)" or "interrupted by Stop Codex (final status
    not observed)". The label comes from the observed `turn/completed`, never
    from the interrupt acknowledgment. Codex's own status is shown beside it. A
    refused stop is reported as a refusal; its turns get no label and new turns
    are allowed again. Interrupts go only to a `ready` process (DEL-01-02
    §4.1). A process in another state (for example a stuck handshake) is
    reported and may still be stopped, as HOSTING §4.6's stop operation allows.
    Waiting requests are not answered, and no workflow run ends. Restart then
    starts Codex as Start Codex does.
    It continues no conversation until the person chooses
    **Continue selected conversation** (R-6). A stop is the person's
    operational choice, not a recorded act.
    **Records (REC, DEL-01-02 §3.4 and §7; DRAFT/PROPOSED Design text).** On
    confirmation the App queues a ledger `codex_stop` entry (person, App-owned
    home, restart, live turns and waiting requests) and writes it before any
    interrupt. Every interrupt, the person's **Interrupt** in the conversation
    as well as the stop's, first writes a stop-request record (SR-01,
    `recovery.stop-request.schema.json`, embedded as a byte copy) to the App
    ledger, then sends `turn/interrupt`. Each later step appends the record's
    next state: sent or not sent (SR-02/03), Codex's answer (SR-04/05/12), the
    turn's observed end with its label (SR-06/07), the end of waiting (SR-10)
    or the end of the generation (SR-08). Every record is validated before it
    is appended. An interrupt refused before SR-01 (wrong generation, no live
    turn, a stop already requested) writes nothing. A ledger that does not
    accept a record never holds up the interrupt (SQ-I I-2): the record stays
    queued in this process, is shown as *not yet written*, and is written when
    the ledger accepts it. After a relaunch the activity and **Recorded stop
    requests** read each turn's label back from the ledger: "interrupted by the
    person", "completed (stop requested)", "interrupted by Stop Codex" and so
    on. A request whose App session ended before a final status was recorded
    reads *outcome unknown*, marked "(derived; not written)". *Limits:* SR records do
    not list the items or delegated agents at the outcome. A turn that ended
    after SR-01 but before the send is recorded as SR-03 *not-sent (not-ready)*
    with the reason, a gap in the Design's send values. Quitting the App does
    not ask first yet (K-4, SQ-Q Q-2): it stops each home's Codex on exit, as
    before, and writes no quit stop requests.
23. **Run panel** (NIR §9 PD-1…PD-7, AS §4, §8, §9). The selected workflow and
    each run show the declared part readably, as the host read it from the
    revision's own bytes: inputs, tools, checkpoints, outputs, returned
    evidence, written-for roles and tool ceiling, each with its reading and
    findings; the JSON stays in a fold. A checkpoint is plan guidance (OV-1,
    SD-1): act label (DS-1), actor, subject, when it is reached, purpose,
    scope, where the act is performed (SD-3), declared held actions and
    decision paths. `governed` is shown and changes nothing (OV-7); an invalid
    declaration is a finding. No hold, block, pause or hold-support value is
    shown (PD-6, OV-3). **Checkpoint records (EXEC §2.4 first slice;
    DRAFT/PROPOSED Design text).** When a run opens, the App writes one
    `checkpoint_listed` (CE-1) per recognized checkpoint, saying whether it can
    observe its arrival. Arrivals come only from native items observed live in
    the run's conversation and turns: a completed agent message whose first
    non-empty line is exactly the output's designating line (AW-6), or a
    completed file change that adds or updates the declared path, or moves a
    file onto it (AW-7 as this App reads it; a delete or a move away is not a
    production). Each arrival
    is written as `checkpoint_arrival` (CE-3), with the item, its time,
    the bound subject and its limits, then a *waiting* `disposition_change`.
    The agent's next own action (RC-9) records `continued_past` once (CE-12);
    `run_resumed` (CE-11) is implemented but cannot occur until acts are
    counted. Recording never sends, opens, pauses or ends anything (RC-4).
    `run_ended` lists the arrivals still waiting (CE-17). Acts are not counted
    yet, so an arrival stays waiting after its act, and `run_ended` can list it
    (CI-20 (h), partly addressed). Each checkpoint
    shows its listing, its arrivals with their labels and limits, and "no
    request from the agent observed". A run record entry that cannot be
    written is shown on the run (A-12). It is written later, in order, with a
    "record write failed" limit (CE-19), and is never written elsewhere. The
    App writes no tool-call, host-outcome or act-counting entries
    (AW-1…AW-4, AW-8…AW-10, CE-2, CE-4…CE-7). A path is compared as text
    (U-E26). Recording follows the active home's view while the App
    refreshes, and when the person ends the run. Each declared output shows its
    promise apart from its standing facets (AS §8), which come only from the
    run record: with nothing recorded they read none reported, not recorded or
    missing. An arrival bound to the output adds only where the agent put it.
    Record entries this view does not read make the facets unknown. The
    advisory compatibility (DEL-02-03 CK-1/CK-2) is shown readably; a role
    outside the written-for roles names both and points to Continue as
    (U-R10, chosen display).
24. **Conversation roles** (NIR §5.4, §5.8; ROLE §3.2, §3.3, §4.4, §6.2). The
    start display lists the role set readably, with the `default_for_new_chat`
    role labelled as a preselection (the bundled set marks none today, U-R11),
    "No role", and each role's limits as the limit account hands them (TASK
    "A task agent does not delegate: Stated, not enforced"; a modified copy
    reads not known). The start display and Continue as offer HELP_HUMAN,
    HELPS_HUMANS and WORKING_ITEMS (the host's `roleSet.conversationRoles`)
    and No role. TASK is not listed as a choice: it is the role a manager
    assigns bounded work to, and its guidance is supplied for that delegation
    (ROLE SL-1, CA-1; NIR ST-5; owner ruling 2026-10-10, "TASK is not a
    conversational role"). A TASK start that reaches composition anyway is
    refused before anything is sent. The conversation header shows the role, fixed for the
    conversation's life, and its relation (its own start, continued from, or
    fork of). **Guidance changed since this conversation started** appears
    only when a file the conversation started with now differs or is missing;
    a store that cannot be read is said to be not compared. **Continue as
    ‹role›…** sends one visible ordinary turn to the source conversation asking
    its agent for a handoff summary. It is refused, with nothing opened or
    sent, when the source is not a current conversation of a ready Codex. When
    a run-end notice is pending there, that request carries it first, once (as
    for any new turn); a request refused before any write closes the handoff
    and leaves the notice pending. The completed agent message observed
    live is placed under an App header naming the source and its role,
    editable and unsent; a written request whose turn failed, was interrupted
    or has an unknown outcome leaves the header only. The new
    conversation starts with no model chosen and records `continuedFrom`
    {source thread, source start record}; its first message is sent only when
    the person sends it, and it reads sent only once the send succeeded.
    **Fork (same role)** sends `thread/fork` with the thread id, no
    instructions or settings, and `deferGoalContinuation: true` so that a
    source goal starts no automatic turn in the fork that the person did not
    start. It admits the fork only when Codex reports a new thread
    forked from the source; the fork inherits the source's role binding. Neither
    changes the source conversation's role or record. Handoffs are kept in App
    process memory.

## Modules

| Module | Contribution |
|---|---|
| `src-tauri/src/hosting.rs` | HOSTING/ACCESS lifecycle, generation, request correlation, ordered native journal, development verification and network disclosure; reviewed 0.160.0 protocol resources in `resources/supplier/` |
| `native_requests.rs`, `recovery.rs`, `native_items.rs`, `access.rs` | Typed native request custody, pointer ledger, scoped live/ended activity and reported account/destination observations |
| `role_supply.rs`, `runtime_session.rs`, `resources/instructions/` | Reviewed v4 defaults, fixed composition bytes, seeding and generation-bound receiving/startup; supplier/model adoption remains a separate warrant |
| `catalog.rs`, `proposal.rs`, `external_adapter.rs`, `receiving.rs`, `external_observation.rs` | Reviewed receiving contracts and exact person-selected observation custody; no external host dispatch or origin verification implied |
| `src-tauri/src/schema_validation.rs`, `schemas/` | W-1 plus complete package/offer/capture checks; declared-ID registry with external retrieval disabled; embedded resources checked by `schemas/sync.py` |
| `src-tauri/src/records.rs` | Validated append, UUID identities, sequence/read completeness, serialization and ordered capture late-write accounting |
| `src-tauri/src/storage.rs` | Selected project/run/writer and library paths, legacy discovery, atomic capture persistence and locking |
| `src-tauri/src/recorder.rs` | Package byte snapshot and request/provenance-limit mapping |
| `src-tauri/src/act_control.rs`, `act_control_a15.rs`, `act_control_file.rs`, `file_act_native.rs`, `canonical.rs` | A16, hot A15 and App-file offer/native custody; capture versus publication uncertainty, ordered retry and original content binding |
| `file_act_root.rs`, `file_act_view.rs`, `src/FileActPanel.tsx` | Original file-offer ownership, separate read-only act/decline comparison and per-offer controls; no cold native-origin upgrade |
| `src-tauri/src/decision_view.rs`, `act_policy.rs`, `standing.rs` | Decision projection, A16 method-aware standing and provenance limits; recorded claims do not establish native act admission |
| `attachments.rs`, `hosting::attachment_custody`, `resources/attachments/` | Native-selected immutable ordered text sources, durable metadata/client pointers before scoped send, and explicit native outcome limits |
| `trace_receiving.rs`, `record_relations.rs` | Independent unverified trace imports and general record correction claims; neither verifies native origin |
| `native_history.rs`, `role_lifecycle.rs` | Read-only native history, scoped Continue receiving and immutable original guidance bindings; cold role-source custody remains unfinished |
| `connector_standing.rs`, `connector_route_store.rs`, `connector_route_view.rs`, `src/ConnectorRoutePanel.tsx` | Provider-independent standing, caller-account persistence and read-only inspection; saved claims do not verify source truth or actor duties |
| `src/RequestCards.tsx` | Readable DEL-01-04 request cards, item anchors and the waiting-request indicator; answer values come unchanged from the host's register |
| `src-tauri/src/codex_stop.rs`, `src/CodexControls.tsx` | Stop/Restart Codex (DEL-01-02 §4.1 C-12 with the DEL-01-04 §5.2 question): live-work assessment with runs in force, ask-first sequence, the ledger `codex_stop` record, interrupts before the stop within the stop wait limit, TO-4 labels and the in-process outcome panel |
| `src-tauri/src/stop_records.rs`, `resources/runtime_core/recovery.stop-request.schema.json` | REC stop-request records (DEL-01-02 §3.4 SR-01…SR-12): validated transitions and outcome labels, the `codex_stop` ledger entry, and the read-back after a relaunch; the Host writes them through its recovery writer before each interrupt send |
| `src-tauri/src/checkpoint_recorder.rs` | EXEC §2.4 first slice: CE-1 listing, CE-3 arrivals from observed AW-6/AW-7 native items, CE-11/CE-12, CE-17 waiting arrivals; written through the run's RS writer with CE-19 late-write limits; never reacts (RC-4) |
| `src-tauri/src/run_offers.rs`, `src/RunOffers.tsx` | Exact run-offer line forms (WR §16.5 PR/FN), the finished-report proof for a *completed* end, and their presentation beneath the message |
| `src-tauri/src/workflow_drafts.rs`, `src/WorkflowDrafts.tsx` | DEL-02-02 draft workspace in the Rust host (SQ-D D-2…D-4 observation, hygiene, §5.1 states, TT-3 composer sources, TT-4 trial pointers) and its list presentation in NIR §7 words; nothing here registers, reviews or runs |
| `src-tauri/src/workflow_trials.rs`, `workflow_package_copy.rs`, `workflow_workspace.rs` (`compose_run_text`, `TrialText`, `files_folder`) | DEL-02-02 trial core (WR §17 steps 1–4): one composer for run texts and trial texts (TT-3), TX-7's files-line folder with content-addressed supply copies, TT-8 trial snapshots, and the create-once TT-4 trial links and observations; the trial flows and their interface are not built yet, so drafts are still tried by the attachment pre-fill |
| `src/RunPanel.tsx` | Run panel and selected-workflow view (NIR §9 PD-1…PD-7): readable declared part, checkpoints as guidance with their recorded listing and arrivals, the run-record write notice, output standing facets from the record only (AS §8), readable advisory compatibility |
| `src-tauri/src/conversation_roles.rs`, `src/ConversationRoles.tsx` | Continue as ‹role› handoffs and same-role Fork through the Host (NIR §5.8, ROLE §3.3), the role limit account (ROLE §6.2), the readable start display, role header and guidance-changed flag (ROLE §4.4) |
| `src/NativeActivity.tsx`, `src/PlanMode.tsx` | Readable per-thread native activity from the `native_items.rs` view (DEL-01-03 plans/tools/delegation with the DEL-01-04 message part) and the experimental plan-mode element |
| `src-tauri/src/lib.rs`, `src/App.tsx` | Native command boundary and presentation; the webview cannot confirm a capture itself |

## Offline build and checks

Use Rust 1.92, Node 24 and prepared Cargo/npm caches. Set `CARGO_HOME` if the
approved dependency cache is isolated; its machine-local recovery path is in
this run's evidence. Package downloads require the owner's authorization.

```sh
npm install --offline --no-audit --no-fund --ignore-scripts
npm run build
(cd src-tauri && cargo build --offline --locked)
(cd src-tauri && python3 schemas/sync.py)
```

From `app/`, set the supplier path to run the real offline handshake:

```sh
export CHIRALITY_CODEX_BIN=<stock codex 0.160.0 vendor binary>
export CHIRALITY_CODEX_EXPECTED_SHA256=112fae7a5a1223e673c8a1791d32338f37df8b527ff1159bb8adac6c4dbf1b4b
npm test
(cd src-tauri && cargo test --offline --locked)
```

Use the complete published platform package, with its `bin/codex` entrypoint,
helper binaries, resources and `codex-package.json` retained in their original
layout. Include the package's `codex-path` directory in the child process's
`PATH`. With only `codex` copied, the stock supplier warns that Code Mode lacks
its required host and will fail closed. The approved 0.160.0 archive's complete layout was separately
verified and probed; earlier flat-binary observations remain source-specific.
This development setup does not establish qualified distribution identity.

`npm test` validates actual Rust outputs against canonical Design schemas,
without reference rewrites. Rust tests also check runtime refusal, capture
failure/recovery, ordering, namespace and provenance negatives. With no supplier
binary, set `CHIRALITY_SKIP_CODEX=1` explicitly for Rust checks; the Node hosting
check then reports its skip. Skipped checks establish no supplier result.

The handshake uses its own unique system-temp home, a local provider at
127.0.0.1 port 9, plugins off and analytics off. It starts no model turn, supplies
no credential, and checks its sampled process-group sockets. Test-owned scratch
files are cleaned after consumers finish.

## Group B offline examination support

`examination/check.py` checks EXP result and PKG identity files and their explicit
candidate/package association. It reads the pinned canonical Design sources,
refuses source drift and inconsistent records, and reports input hashes and
missing prerequisites. File-check success does not verify a native observation,
package signature or qualification. The maintained examples are invented.

From `app/`, with the prepared Python `jsonschema` 4.26.0 environment:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 tests/group_b_support_test.py
PYTHONDONTWRITEBYTECODE=1 python3 examination/check.py validate result tests/group_b_fixtures/result.json
```

The Python suite is separate from `npm test`. See
[the examination tool instructions](examination/README.md) for package-link
arguments, supported rules and remaining M1/M2/M3 work. The current Group B graph
is `execution/_Coordination/WorkGraphs/APP-V4-GROUP-B-20261008/WORK_GRAPH.md`
relative to the project.

## Run the development App

Set `CHIRALITY_WORKSPACE`, `CHIRALITY_CODEX_BIN` and a scratch
`CHIRALITY_CODEX_HOME`; never use `~/.codex` for development. A matching binary
hash is a development assertion. Full qualified distribution identity is absent,
so the development run requires `CHIRALITY_ALLOW_UNVERIFIED=1` and is labelled
`unverified-development` (LT-24); mismatches still refuse.

Make the workspace and Codex home with `mktemp -d`, and use their physical paths
(`cd <directory> && pwd -P`) because protected store paths reject symlink
ancestry. Put this stand-in configuration in the scratch home's `config.toml`:

```toml
model_provider = "skeleton_local"
model = "skeleton-no-model"
[model_providers.skeleton_local]
name = "Offline development stand-in"
base_url = "http://127.0.0.1:9/v1"
wire_api = "responses"
[features]
plugins = false
[analytics]
enabled = false
```

Copy the maintained `tests/fixtures/FX-DP1/project/decisions` files into the
scratch workspace's `project/decisions/`, then run `npx --offline tauri dev`.
For the offline thread exercise, enter model `skeleton-no-model` and provider
`skeleton_local` explicitly. These are test choices, not product defaults.
Open a package, choose an alternative and confirm its full native text.
Authenticated/live model work remains coordinated with the owner.

For stored history, choose **Read stored conversations**, then select a received
conversation. **Read metadata**, **Read turns**, **Read goal**, and per-turn item
controls read disposable native pages; opaque page cursors belong to their
received stream. **Continue selected conversation** separately requests native
resume before permitting operational text input. It keeps the conversation’s
existing guidance/settings and does not resend automatically. Original App role
evidence is shown only when retained in this process; a cold restart shows
Unknown. Reading child metadata does not supply a child role.

The decision view reads recorded claims without writing. Use **Continue pending
recording and record new requests** for explicit writer continuation; startup
also invokes that separate writer responsibility. Incomparable current claims,
conflicting record IDs and incomplete lapse histories remain visible, with each
source and time preserved. Reading a claim does not verify its native origin.

Use **Select text attachment…** to open the native selector. Move or remove
selections explicitly; **Confirm current source…** makes a new explicit source
choice when needed. **Send text and ordered attachments** and **Steer current
turn with ordered attachments** include the entire private selection. Plain-text
controls explicitly exclude it. An error can follow an actual native write;
inspect the submission's retained source/outcome instead of assuming no send or
retrying automatically.

The App routes configured account (`H-acct`) and explicitly prepared API-key (`H-key`) homes separately. Per-home resource and metadata guards preserve existing account use when a prospective key proposal fails. Key entry and OAuth controls use native source-bound adapters; their actual OS/auth/provider journeys remain unqualified. A continued conversation without a trustworthy home-class association stays unknown and may remain hot-only. Home class is independent of model/provider choice.

## Storage and remaining work

Project run logs use `.chirality/records/runs/<safe-run-key>/<safe-writer-key>.jsonl`;
outside-run acts use `.chirality/records/acts/<safe-writer-key>.jsonl` with captures
in `.chirality/captures/`. Library A15 allocation uses the library's
`.chirality/records/acts.jsonl` and `.chirality/captures/`; its native registration
witness remains unfinished. There is no registration attempt journal (owner
ruling 2026-10-10): when a library is opened, SQ-X finds A15 records that no
ledger line cites and decides from the record and the revision store (WR §6
X-1, X-2; CI-24 (b)). Each open review holds
`.chirality/workflow-registration.live.lock` shared until its attempt is
closed, and X-2 runs only when it can hold that file exclusively, so a live
attempt is not closed as lost while its review holds the lock (tested with
separate owners in one process; release at process death is `flock`'s, not
tested). A
`.chirality/.workflow-staging/attempts/` folder left by an earlier build is
no longer read. Storage keys are separate from governed identities.
Explicitly discovered legacy `records/coordination.rs.jsonl` stays intact.
Unwritable or incomplete targets report limits without silent relocation.

Attachment metadata arrays and pointer-only client request records live under
the App user-data `runtime/nir/attachment-supplies/` and
`runtime/hosting/client-requests/` directories. App-kept draft bases and draft
trial pointers (and the trial links and observations of WR TT-4) live under
`runtime/wr/draft-bases/` and `runtime/wr/trial-pointers/` there (WR §3). They
contain no selected text, native transcript or generated supplier prompt cache.
REC owns project/context tags through the existing pointer ledger; no competing
ledger is opened. In the project, `.chirality/workflow-supply/` holds
content-addressed copies of workflow package files named by a run text's files
line (WR TX-7) and `.chirality/workflow-trials/` trial snapshots (TT-8); the
App never rewrites or removes either, and recreates a deleted one when it is
next needed.

Trustworthy persistent cold replay and SEAL-2 remain unfinished under CI-10 and
I3-CUST. Current code refuses unverified replay while preserving evidence.
Native authenticity, real process-kill/fsync failure witnesses, durable history rebuild and cold role-source reconciliation, child role supply, native A15/registered-library and file-act witnesses, and remaining policy/standing/control journeys remain in the Group A graph. Per-home configuration/resource linking is implemented with observed ownership limits. CommonMark parsing and one closed, explicitly development-candidate workflow catalog are supplied; the production native-page supply path and hot registration transaction are implemented, while their actual native consumer witnesses remain separate. General file/arrival entry surfaces and complete file-act lapse-history evidence also remain unfinished. External dispatch and host qualification remain unsupplied. Native text-turn and interrupt controls use the selected native thread and
retain generation/terminal limits. Transport and receiving tests do not prove a
provider prediction. A separately frozen controlled live backend greeting passed;
its exact source pins and limits are recorded in the run. An approved no-supplier native window inspection establishes tool/window reachability only; corrected UI/storage, browser/device/auth/provider and capture journeys remain separate unfinished witnesses. Host joins stay deferred to their owning sessions.

REC stop-request records and the ledger `codex_stop` entry (item 22) are
appended to the existing pointer ledger. Checkpoint entries (item 23) go to the
run's own RS log. Neither opens a new store.

The run panel (item 23) records only output arrivals (AW-6, AW-7). It does not
yet record tool-call or host-outcome arrivals, act counting and its
dispositions (CE-2, CE-4…CE-7), or output records. Conversation roles (item 24)
keep handoffs in process memory and write no persistent role-supply log;
delete or archive beside Fork waits on U-R13.

Stop and Restart Codex (item 22) still lack an ask-first App quit with its
quit stop-request records (K-4) and the startup SR-08 write for an earlier
session's open requests (shown derived for now). The Restart Codex question
was witnessed natively once, on 2026-10-10, with nothing live: it listed nothing
in force and showed its three buttons with Keep Codex running as the default.
Restart Codex was pressed, and Cancel and Keep Codex running were not. The
Stop Codex question, a stop with live work and quit remain unwitnessed.

A [first native App witness](../execution/PKG-01/DEL-01-02/Design/NATIVE_WITNESS_2026-10-10.md) was taken on 2026-10-10. It used an improvised
debug bundle of `3a29171a44`, stock Codex 0.160.0 (unverified-development), and
`gpt-6-luna` on a ChatGPT account signed in by the owner. It observed:
- ChatGPT sign-in;
- a no-role start;
- text, plan-mode and default-mode turns;
- an interrupt;
- Restart Codex, then a history read and resume;
- Continue as with a role.
- in a second run, native delegation (spawn, wait, follow-up, close). Only
  `wait` appeared as a collab call item, and an agent could reach only its own
  spawn tree.

It qualifies nothing. Attachments and the run-end notice, workflow runs and A15,
approval cards, delegation beyond that run, quit, the WebKit/Chromium matrix and a packaged
build remain unwitnessed. It also found that an interrupted turn's running
command can still complete (see the note), and the bundle gap CI-31.

See `CONTRACT_ISSUES.md`, `EVIDENCE.md` and the current Group A `WORK_GRAPH.md`.

## Recorded connector route accounts

With an explicitly associated App project, **Read / refresh accounts** inspects
its canonical connector route-account directory without creating it. The view
shows the recorded question, gaps and responsibility, duties, and parsed source
and conclusion fields. Duplicate IDs and discovery issues remain visible; an
empty or incomplete scan does not establish that no work remains. Unknown or
mismatched project association refuses the read without a fallback directory.

The view does not open cited sources, resolve anchors, save accounts, submit
attachments, or perform recorded duties. Host-parsed JSON can normalize numeric
values; the displayed binding hash is a host observation of file bytes, not
frontend verification of displayed values. The source-bound manual comparison
in Group C `C3_SOURCE_WALK.md` and its maintained fixture are separately
evidenced. App-native source selection/reconstruction and its actual witness
remain unfinished, as do the recorded PEC/Domains and research activation joins.

## Transient source observation

**Observe a project text source** prepares one question and opens a native
selector for a file within the explicit App project. The first slice accepts
regular UTF-8 text up to 262144 bytes, without NUL or symlink descendants.
The host retains a session-memory snapshot; exact line excerpts refer to that
buffer even after the file changes. Cancellation and failed reads keep earlier
observations historical, with unresolved read failures separate from excerpt
failures. New preparation or a successful reread establishes a new basis.

Revision labels are caller assertions. Locating source text verifies inclusion
only; it establishes no authoritative revision, Git identity or source truth.
The preview creates no saved account, supported conclusion, attachment supply
or performed duty. It does not send source text elsewhere. Ordinary metadata
and path checks detect some changes; concurrent transient writes or renames
can evade them, so the buffer is not certified as a coherent historical revision.
The current evidence uses injected selection callbacks, real scratch reads and
component rendering. Actual native selection/use, the Git adapter and later
account materialization remain separate unfinished obligations.
