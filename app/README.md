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

Process placement follows the owner's OI-008 ruling of 2026-10-10
(`docs/ARCHITECTURE.md` §3): "The Rust host owns everything that writes the
person's files or the App's records, talks to Codex, or captures a person's
act. The web view presents, and sends only what the person initiates. It never
writes records or operates the act control." `src-tauri/` holds that host;
`src/` holds the web view.

## Developer start

This is the development App; the published fallback remains v3.0.1 in
[chirality-app](https://github.com/sgttomas/chirality-app). Build commands below
run from `projects/chirality-app-v4/app/` in the Chirality repository.

Use Rust **1.97.1**, Node **24** and Python **3**. These Rust and Node versions
match [App v4 CI](../../../.github/workflows/app-v4.yml). Install dependencies
with `npm ci` when downloads are authorized, or use the prepared-cache route in
[Offline build and checks](#offline-build-and-checks).

```sh
npm ci
npm run build
(cd src-tauri && cargo build --locked)
(cd src-tauri && python3 schemas/sync.py)
```

Before running supplier-dependent checks, prepare the complete stock Codex
0.160.0 platform package and set the binary path and expected hash as described
in [Offline build and checks](#offline-build-and-checks). For a development
launch, follow [Run the development App](#run-the-development-app), including
its scratch workspace and Codex home. The offline stand-in does not run a model
turn. [Storage and remaining work](#storage-and-remaining-work) states the
implemented behavior and qualification limits.

## Current path

1. The Rust host starts the stock App Server, completes its handshake and keeps
   native frames with full `{appSession, home, spawnCounter}` generation identity.
2. The person chooses a primary role (or none) and explicitly enters a model
   and a configured Codex provider for a new thread. Codex retains its own configuration and permissions. The view
   discloses expected model contact at thread start, before a turn; it does not
   represent that notice as measured socket traffic. Reviewed v4 guidance seeds
   an editable App instruction copy without overwriting edits; new conversations
   read current bytes. Native child roles remain not supplied by the App. The
   opt-in [supplier child-carrier check](supplier_checks/child_roles.py) and its
   [receiving account](../execution/PKG-02/DEL-02-04/Design/CHILD_ROLE_CARRIER_0.160.0.md)
   observe per-thread TASK configuration and exact child guidance in scripted
   stock-supplier execution; the App configuration/publication join remains open.
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
   under NIR §4.1 FO-6. Ended/replaced observations keep explicit checklist/history limits.
8. The person can select catalog/read JSON and an optional counterpart through
   native selectors. Rust retains exact bytes in memory; the panel shows complete
   reported content, unverified host origin and comparison/path-display limits.
9. Current native threads accept unchanged text input; live turns can receive an
   explicit interrupt request. Native acknowledgment is separate from turn end or
   rollback. Contradictory late starts cannot revive a completed tuple.
10. An App-owned pointer-only recovery ledger initializes before supplier startup
   in a SQLite database at the App user-data `runtime/recovery.ledger.sqlite`
   path (DEL-01-02 §7; PRD R-STORE). Entries are only inserted (the schema's
   triggers refuse updates and deletes), batches that stand together are one
   transaction. An entry is reported recorded only after its commit returned
   (journal and database file synced with `F_FULLFSYNC`) and the App then
   flushed the database's folder with `F_FULLFSYNC`, so the journal's removal
   that makes the commit durable is on the device too. The JSON Lines ledger
   earlier builds wrote at `runtime/recovery.ledger.jsonl` is imported once,
   every complete valid line in order. Only a torn (not newline-closed) final
   line is kept as a limit, shown with the recovery initialization. A complete
   invalid line, a file changed since its import, or a file returned after the
   App recorded without it fails initialization visibly and imports nothing;
   no App recovery is recorded until the file is repaired or moved aside
   (moving it aside gives up its entries). The file itself is never written. The host holds only the ledger's
   current entries and shows a bounded snapshot of it, not its entries.
   Initialization errors remain visible without blocking native protocol
   processing or relocating data.

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

    One existing unregistered library entry can be reviewed in place through
    **Review this unregistered in-place library entry**, followed by native
    **Register** confirmation. Its single A15 uses the reviewed `entry:` reference
    and no prior revision; no draft is created. Only the newly captured hot
    registration makes it selectable here; quoted earlier history remains separate.
    **Reuse (WR §4.4, §4.6).** The active library's list of registered revisions
    offers **Select revision ‹n›** on a revision whose registration or
    re-confirmation result this App process holds (RC-2) and whose revision
    store still recomputes when the list is read (a row that does not says
    so, LS-4); the press names its library, and a press after another library
    became active selects nothing. The host resolves the selection from the
    revision store, never the published copy, and verifies its bytes there
    again (SL-1, SL-4). Every registered selection resolves from the revision
    store this way: from the list, from a retained review's **Select revision
    ‹n›** (the revision that review registered or re-confirmed; no folder is
    picked), from "newer revision ‹n› available", and from a confirmed agent
    proposal (item 20). An edited published copy or an identical copy
    elsewhere is never used, and a store that does not recompute refuses with
    the selection unchanged. A run's files line (WR TX-7) therefore names the
    revision's store folder, project- or `~`-relative, and the selection's
    holding library is recorded as that folder's parent. Other rows keep Refine and re-confirmation through a
    draft; selecting one, a draft or an unregistered library entry is refused
    with its standing and route (SL-5). Beside a registered selection the view
    shows "newer revision ‹n› available" when the slot's ledger has a newer
    registered revision; the selection stays where it is (SL-2, SL-4). Its
    **Select revision ‹n›** is offered only when this process holds that
    revision; following it is a new selection whose `selection_record` cites
    the one it replaces (`replaces`). Any person's selection of a registered
    revision replacing another registered selection in the same chat cites it
    the same way (§5.4); a candidate selection that cannot run is not cited.
    The owner chose: "Each chat keeps its own selection (Recommended)".
    Each chat keeps its pending choice in its actual App home source; started
    runs retain their own revision, and a new chat has no selection. Library
    browsing and explicit no-chat inspection stay shared; inspection supplies
    no next-workflow default. The App constructs a selection record when a run
    is prepared and publishes it before dispatch, since the record names the
    run's conversation; a replaced selection no run used has no record of its
    own. Whether a record is due at selection itself remains open with the WR
    owner. Bundled (LS-5) entries remain inspect-only candidates.
17. The selected conversation shows its native activity readably: messages,
    reasoning summaries, plan items and checklist revisions, tool rows and
    descendants, grouped by turn in native start order and, within a turn, in
    the order this App first received each item. Each row keeps the native item
    and status beside its display reading; unknown, not-completed and
    result-not-supplied stay distinct, and no act, return or integration is
    inferred. Agent text, reasoning summaries, plans and command output stream
    as labelled previews that the completed native item replaces. Stored-history
    pages the person reads (turns, items, thread read) are added as
    recovered-from-supplier rows, as are the pages the host's recovery reads
    return after a restart (item 22b); items are added only as their pages
    are read. Only a plan
    observed live shows a revision number in this conversation; a later run
    does not reset it. Each plan revision, checklist and tool row in a turn a
    workflow run was in force at, as the App's run markers place it (from
    its start turn to the turn it ended after), carries "During the run of
    ‹workflow› ‹revision›" (NPTD §5.7). Messages carry none, and so does a row
    outside any run, between runs, or past the start turn of a run whose end
    this view cannot place; nothing says which run caused an item. A row the
    view cannot read shows its JSON instead of breaking the view.
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
    person". The press resolves the proposed revision from the revision store
    and verifies it there, as a selection from the library list does (SL-4); an
    edited published copy is not used, and a store that does not recompute
    refuses with nothing selected or started. Unresolved proposals show their notice. The activity view marks run
    starts and ends from the App's run records and folds the supplied run text.
    Run-start checks distinguish native homes when the App retains the original
    run source and its exact recorded opening. An open run in another home
    with the same bare native thread ID then leaves this chat available. Busy,
    missing or conflicting source proof, and cold history without that proof,
    retain the existing conservative refusal.
21. **Save a workflow** starts from a draft list. Under the owner's OI-008 ruling
    (first given for the draft workspace as "A, proceed with the Rust host."), the Rust host observes
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
    **Trials (WR §4.2, owner direction U-WR-24).** A trial mirrors a real run:
    the host takes a content-addressed trial snapshot and composes the trial
    text, a trial header followed by the run text a registered run of that
    exact content would receive, whose files line names the snapshot folder.
    Nothing is sent until the person presses Send, and the trial link is
    written only when Codex acknowledges the turn. **Try with the authoring
    agent** pre-fills, in the conversation chosen as authoring conversation,
    the person's editable message and then the trial text as a removable card;
    the message asks the authoring agent to run the trial through one
    sub-agent and report. The host reads delegation availability (NPTD §7.1:
    the model's `multiAgentVersion`, `features.multi_agent`, the provider's
    `namespaceTools`) for each conversation's model and provider when Try is
    pressed and on its tick when needed (once per conversation model, and again
    for a *missing* reading after two minutes); readings from Codex's
    provider-wide reads count only when the app-server's own provider is the
    conversation's. With no `model_provider` configured (the usual case) the
    reading is therefore *not established* until the native witness settles
    what Codex 0.160.0 reports for an unconfigured home; *missing* hides the
    button with the reason,
    *not established* offers it with that note. **Try in a fresh
    conversation** is optional: a new-conversation panel takes the person's
    role and model, puts the trial text first, then the editable inputs
    message; that conversation offers no workflow run, and neither does a fork
    of it, across a relaunch too (an App-kept trial conversation mark). On its own tick (about once a second) the host reads a new
    sub-agent's first input once and links it when it carries the trial's
    begin marker, with a fidelity reading ("workflow given verbatim", "the
    sub-agent's input differs from the run text" or "not checked"); the person
    can link, unlink or read again. At Codex 0.160.0 a sub-agent's task
    arrives as an encrypted inter-agent message, not a user message, so the
    row reads "not checkable" with that reason, the sub-agent stays offered for
    the person to link, and Read again is not offered when an encrypted inter-agent task is seen; a first turn that merely shows no user message stays open to reading again (WR TT-9). Each draft lists its trials newest first,
    with **Try again**, **Bring trial back** (a transcript read from Codex's
    history, pre-filled unsent in the authoring conversation; *brought back*
    is recorded on acknowledgment) and **Compare** (two trials, or a trial and
    a run of the same slot, side by side with the version difference). A run
    offers **Bring a real run back to authoring**. Proposal and finished lines
    in a trial's turn, conversation or sub-agent offer nothing. The review
    shows the last clean trial (matches, differs or none) as information
    only. Earlier attachment trial pointers are still listed. A draft's files
    the person attaches are ordinary attachments.
    **Review for registration…** opens the existing review for the listed
    content, refused as DS-6 if the draft changed since listing.
    Registration stays the person's A15 act at the native confirmation; once
    it registers or re-confirms, the review offers **Select revision ‹n›**,
    resolved from the revision store like every registered selection (item 16).
    A trial is not a run, registration, checking or acceptance.
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
    with the reason, a gap in the Design's send values. At the next start the
    App writes SR-08 for each stop request an earlier session left sent with
    no final status (AS-02, R-2), and RQ-06 for the requests such a session left
    listed (*app-ended-without-record*; no reply is sent).
22a. **Quit asks first** (DEL-01-02 DEF-6, K-4, SQ-Q; DEL-01-04 §5.2). Quit is
    the App's own menu item (Cmd/Ctrl+Q). The host assesses live work across
    every App-owned home and records `quit_requested` with the lists. With
    nothing live it quits without asking. Otherwise a native question lists
    the live turns, waiting requests, delegated agents and workflow runs in
    force, with no time limit; **Keep running** is the default, and it and
    Cancel record `quit_answered` *cancelled* and change nothing. On **Quit**
    every ready home is closed to new turns and assessed again (a changed list
    is recorded and asked again); then `quit_answered` *confirmed*, each live
    turn's stop request (SR-01, cause *quit*) and its interrupt; the App waits
    up to the stop wait limit for those turns to end, exits, stops each home's
    Codex and writes `session_ended` *quit* with each quit stop request's
    state. A relaunch reads *quit-with-live-work* and "interrupted by quit".
    An exit nobody decided is held and asked as Quit. **Closing the window is
    not quit** (DEF-1, SQ-W): it hides the window (macOS; the Dock icon shows
    it again) or minimizes it; work and requests continue, and the view
    re-reads the host's snapshot when shown. The Dock icon shows the number of
    supplier requests waiting for the person (C-24; macOS only). Quit and
    Stop/Restart Codex refuse each other while one is under way. *Limits:* on macOS the
    Dock's Quit, logout and shutdown reach the App as `terminate:` and cannot
    be held; they are recorded as `session_ended` *system-terminated* with no
    question. The indicator gives a count only; the conversations are listed
    in the window's request cards, and clicking the Dock icon opens the App,
    not a particular conversation (WI-3). Quit has not been witnessed natively.
22b. **Recovery after a restart** (DEL-01-02 §3.2 CV-11…CV-15, CV-19, CV-22;
    §3.4 SR-09; §5 R-4, X-3…X-5). When a home's Codex is ready again (Start or
    Restart Codex, or the App's start after a relaunch), the host reads, on
    that process, each conversation of that home whose process ended while it
    was loaded, or that an earlier App session left unsettled: `thread/read`
    (metadata only), then `thread/turns/list` newest first, page by page
    until the turn last seen live is found. The reads run on the host's trial
    tick, are journalled as `app-rule:recovery-read`, and change nothing in
    Codex: nothing is resumed and no prompt is re-sent. The App then records
    `observation_recovered` *accessible* and, for the turn last seen live,
    `turn_outcome` with Codex's final status (*recovered-from-supplier*), or
    *unknown* when history reports it in progress or does not have it; its
    items seen open read "not completed (turn ended)" only when Codex reports
    the turn ended. Codex's status is shown beside the App's reading, and a
    turn live when the App stopped Codex carries the graceful-stop note. A
    stop request of that turn whose outcome was unknown records SR-09 with
    that status. A failed read leaves the conversation *unavailable* with the
    reason; it is read again when the person chooses **Read this conversation
    from Codex again** in the recovery panel, or at the next ready. If Codex
    ends or is stopped during the reads, the conversation waits for the next
    ready. The pages are added
    to the activity view (item 17). *Limits:* a conversation with no App index
    (no home recorded) is not read; a turn not found within 20 pages is
    *unavailable*, not absent; a read Codex does not answer within 20 s ends
    that pass, leaving the conversations not yet read *unavailable*; the
    graceful-stop note is inferred from the App's stop, not from whether the
    stop had to force the process to end; after a relaunch only each
    conversation's latest persisted state is read, so a loss not yet
    recovered when the conversation was loaded again before the App ended is
    not read; the events are kept in this App process, and
    the ledger keeps the conversation's recovery states. Not witnessed
    natively.
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
    observe its arrival, and one `declaration_finding` (CE-2) per WD code of an
    invalid or not-established checkpoint, which never arrives. Arrivals come
    only from native items observed live in the run's conversation and turns:
    a completed agent message whose first non-empty line is exactly the
    output's designating line (AW-6); a completed file change that adds or
    updates the declared path, or moves a file onto it (AW-7 as this App reads
    it; a delete or a move away is not a production), bound to the file's
    exact bytes as the App reads them when it observes the change; or the
    start of each agent item of a harness capability's own kind for a kind (a)
    checkpoint on that capability (AW-3; a name with no active presence rule,
    and every host operation, stay not evaluable, AW-1, AW-2, AW-4). Each
    arrival is written as `checkpoint_arrival` (CE-3), with the item, its
    time, the bound subject and its limits, then a *waiting*
    `disposition_change`. **Acts are counted** (CE-5, CE-6, CE-8) from the
    App-file act and decline records in the project's record set, each only
    through the one capture object it cites: current after correction,
    written by the capturing surface, its capture resolved, valid, sealed
    under a key this App installation holds (AAC §6.3 SEAL-C) and saying
    what the record says, one record per capture (SP-3, RS R-8). Any other
    record naming the arrival's file adds an "unresolvable reference" limit
    and is never an act. An act of the required kind on the arrival's file and
    current content makes the arrival *performed*; before the arrival the
    latest decision of that kind on that content governs ("by earlier act",
    or a decline resolving it negatively); after it, a decline of that kind on
    that content resolves it negatively; another kind, older content or
    other content is `act_not_counted` with its reason, and another content
    method is neither. The first deciding act decides; later acts are not
    recorded against a decided arrival. A message arrival, or a subject the App cannot identify (a call's targets,
    the objects an output concerns), binds no act and stays waiting. A
    supplier person-input request or MCP elicitation received in the run while
    an arrival waits is written as `act_request` (CE-4), associated only when
    exactly one waits, with RS's "requester identity not established" limit.
    The agent's next own action (RC-9) records `continued_past` once (CE-12),
    and the first action evidenced as started after the deciding act records
    `run_resumed` (CE-11; with no supplier start time none is claimed, A-9).
    **Lapses (CE-10).** While the run is live, at each observation (after the
    items it delivered for a *performed* arrival, before counting acts for one
    waiting again after a lapse), the App reads the file each act answering an arrival's latest performance is
    bound to (rehashing it only when its metadata changes) and compares it
    with the act's bound content as the file-act view does. A changed identity
    is written as `act_lapsed` *lapsed*, a missing file *lapsed (subject
    absent)*, with the observation's own time and the act record unchanged.
    Before the recorded resume point the arrival becomes *waiting* "waiting —
    lapsed at ‹t›" (and "subject absent"), and an act on the content now
    current performs it again with the next ordinal; after it, the arrival
    stays *performed* with "act lapsed at ‹t›" and nothing re-holds (RC-8,
    PH-8); then an act of the required kind on the content now current,
    whatever its capture time (SP-6), performs it again with the next ordinal
    and answers it alone (one referent, JA-1), and the first agent action
    started after both that act's capture and the lapse observation is a new
    resume point. Other acts and declines are
    not recorded against the still *performed* arrival. A file that cannot be read is *unknown (unavailable)*, and content
    back at the acted content "matches c0 again after observed lapse"; both
    are written without changing the label (A-10; RS U-12). A repeated
    observation is not written again; a lapse whose label was not written
    gets it at the next observation. The file-act view reads these entries
    as the act's lapse history.
    **Observation lost and recovered (CE-13, CE-14).** The record tick and
    the End run paths receive DEL-01-02's custody events with the native
    view. Each `observation_lost` of this App session that names the run's
    conversation, from the Codex generation the run opened in on, is written
    once as `observation_lost` with its cause (DEF-5, or DEF-6 for a quit).
    It is *deciding* when an item it left in flight may be a listed
    checkpoint's named event: a message whose streamed text has not settled
    on another first line, or a file change whose received changes do not
    exclude the declared path (AW-12). A deciding loss names no arrival and
    writes no *unknown* label. A later recovery read *accessible* of that
    conversation, matched to the loss by the live turn it reports, is written
    once as `observation_recovered` with its own time; it reads turns only,
    so it recovers no item and changes no label (RP-1). An unavailable read
    writes nothing. A conversation with no App index gets no custody loss, so
    its run records none.
    **Tool-permission settlements (RS R13, R11).** Each A14 request of the
    run (an approval request in the register: the run's App session and
    conversation, a turn of the run, from the generation it opened in) is
    written once as `tool_permission_settlement` when the register shows it
    settled: answered or declined by the person, declined by a named App
    rule, errored explicitly or by a named rule, resolved by Codex, or ended
    unanswered with the context its process ended in (supplier exit, supplier
    stop, App quit, system termination) and DEL-01-02's
    `request_ended_unanswered` event (RECOVERY RQ-04, written at the
    generation's close). A reply written to Codex and never acknowledged
    before the close is RS's "lost acknowledgement" limit, from
    `acknowledgment_not_observed` (RQ-05). A request still open, or whose
    reply could not be written, is not written; nor is a reply still being
    written when the process ended, whose write result the host does not
    record after the close (no transition is designed for it). A settlement inside Codex by
    the user's own Codex mode never reaches the App and is not recorded. None
    is a human act. The request card says "when you quit" for a request
    ended at a quit (NIR CS-7).
    Recording never sends, opens, pauses or ends anything (RC-4). When the
    person ends the run, lapses since the last observation and then acts
    recorded since are written first, also for a run ended after a relaunch
    (when the act records cannot be read, the end still ends the run and, if
    an arrival waits, a limit naming them is written first), and `run_ended`
    lists the arrivals still waiting (CE-17). Each checkpoint shows its listing or
    finding, its arrivals with their labels, requests, counted and not-counted
    acts, lapses and limits. A run record entry that cannot be
    written is shown on the run (A-12). It is written later, in order, with a
    "record write failed" limit (CE-19), and is never written elsewhere. The
    App writes no host-outcome, A5 item or A12 entries (AW-8…AW-10, CE-7,
    CE-9), no observation loss or recovery of an earlier App session (after a
    relaunch the custody events of the session that ended are gone, and the
    run gets RS's "App-restart interruption" limit instead) and, since it observes
    no run after its end, no after-end lapse or act (CE-10 *after run end*,
    CE-16). A path is compared as text
    (U-E26). Recording follows the active home's view while the App
    refreshes, and when the person ends the run. Each declared output shows its
    promise apart from its standing facets (AS §8), which come only from the
    run record: with nothing recorded they read none reported, not recorded or
    missing. An arrival bound to the output adds only where the agent put it.
    An output that declares a gating checkpoint shows, in its human-act facet
    only, the record's act standing for that checkpoint's latest arrival: the
    counted act (with "by earlier act" and "answered by ‹n› acts"), "prior act
    not counted" and other not-counted acts with their reasons, a decline, and
    the latest recorded lapse observation (lapsed, with c₀; lapsed (subject
    absent); matches c₀ again; unknown (incomparable / unavailable)). With no
    lapse recorded it reads *not yet evaluated*, never *not lapsed*; a performed
    label without its counted act reads unknown. An output with no gating
    checkpoint reads acts unknown once an act entry concerns an arrival bound
    to it. A tool-permission settlement (R13) changes no facet: AS §8 names
    no source for it and an A14 settlement is never an act (DS-3); nor does
    a model turn (R5 `model_turn`), whose destination AS §2 shows in the
    channel status, "not here". A "lost
    acknowledgement" limit (R11) adds an *unknown* note to Evidence
    completeness only, the facet AS §8 gives record-out evidence limits.
    Other record entries this view does not read, other limits and an
    observation loss or recovery among them, make the facets unknown. The
    advisory compatibility (DEL-02-03 CK-1/CK-2) is shown readably; a role
    outside the written-for roles names both and points to Continue as
    (U-R10, chosen display).
    **Across a relaunch (WR TX-5 / SQ-END, (d), (j)).** When a run opens, the host
    tags its conversation in the App's recovery ledger with the run reference
    (owner `DEL-02-03`). A tag that cannot be stored is kept in memory only and
    shown on the run; the run goes on. At startup the host writes one "App-restart
    interruption" limit for each recovery restart fact. The limit goes on the run
    opened last in that conversation with no `run_ended`, found by the tag, or by
    `run_opened.conversationRef` when no tag is stored (the limit says which). It
    is written once per run and fact, and earlier ended runs are untouched.
    **Reopen** shows what the startup writer did. Nothing ends a run
    automatically: there is no "interruption not recovered" end. When the person
    ends an interrupted run from the record, that end gets its end notice. The
    notice is composed from the run's recorded run-start text, checked against
    its `run_opened`, and the next message in that conversation carries it
    once. Until then a new run cannot start there. If the record is missing or
    does not match, no notice is sent and the reason is shown. The pending
    notice is held in this process only. Reopen lists it, with "Retry the
    end-notice record" and "Send without the end notice" when its record cannot
    be written. A record the writer refuses permanently is not held: it is
    nonconformant, or its reserved identity is held by a different entry. A
    "record write failed" limit names it as never written, and later records,
    including the person's `run_ended`, are written in order. I/O failures still
    hold strict order.
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

    The Rust host records each App start/fork attempt's actual supply
    observations in the project's explicit records store (ROLE §6.1a),
    retaining content-identified copies of the exact App-owned guidance
    bytes. **Read quoted role-supply history** inspects those bytes and
    recorded outcomes without a native request. Cold history is unsigned,
    unverified file evidence; it leaves the current conversation's role
    unknown and restores no role binding or CCE owner.

25. **Records capability** (RS §13.8 "Agent access", §13.9; owner U-STORE-4,
    "I choose option B"). Conversations the App starts in its current project
    (`CHIRALITY_WORKSPACE`) are offered one read-only tool,
    `chirality_records_read_v1` (`dynamicTools` on `thread/start`). Stock
    0.160.0 retains its declaration through hot and cold resume and fork in
    the opt-in [records supplier check](supplier_checks/records_delivery.py).
    That capture-only fixture uses the actual App definition, has no model
    prediction or App handler, and observes only `namespaceTools: true`
    routes (RS §13.9). Its optional `--include-flat-model` case checks the
    catalogue-reported `gpt-5.5` model's flat function declarations; that
    renderer omits scalar length/range bounds, while the App separately
    validates actual call arguments. A fork admitted from a known offered source in the
    same Codex generation inherits the App's handler binding; a fake-peer
    Host journey verifies its read-log and project-scope behavior. An actual
    offered/admitted start keeps a compact unverified receipt in REC's existing
    conversation-index tags. A fresh explicit native resume joins one matching
    receipt to the same home, explicit App project and physical directory;
    only then is the current-generation handler installed. A genuine fork can
    inherit that provenance. Missing, conflicting, unsupported or changed
    receipts remain visibly unknown/unsupported, even at the same native cwd.
    Receipt-publication failure leaves hot use available with a cold limit;
    a landed COMMIT may be read after healthy fresh REC initialization (RS
    §13.9). No instructions, settings or tools are re-sent on resume/fork. Its operations are `list_runs`, `read_run` and
    `read_acts`. Pages hold at most 50 items and the final text stays within
    32 KiB (fewer items, or a refusal, when it would not); larger entries and
    summaries come back as stubs, and a cursor continues the next page. The
    Rust host answers on a worker thread by the App rule `records-read` and
    reads only this project's records. It never returns keys, capture
    evidence files, other projects' records, library acts (also when the
    project is the library) or refused lines' content. Path-valued fields
    (`workflow.sourceRoot`, `boundSubject`) come back as
    `{"rewrittenPath":"<project>/…"}` or `{"withheldPath":"outside-project"}`;
    every other string is quoted exactly and may contain paths. Every
    return is one JSON document marked as quoted evidence, not instructions
    or authority. Before the
    agent gets an answer, the call (returned or refused) is written to the
    read log in the project's records store subtree
    (`reads/records-reads.jsonl`) and synced, so a read that cannot be
    recorded (no store, a project with no identity yet, which an agent's
    read never mints, or a project the store cannot attach) returns
    nothing. Reads are recorded there before the project's records are
    imported too. The App-wide `runtime/records-reads.jsonl` of earlier
    builds holds reads of several projects, so it is not imported or split:
    it stays in App data unchanged and the host status shows it. "returned" there means prepared for
    return; whether the reply reached Codex is the request register's entry. The host status shows the capability
    and its latest 20 reads, never what was returned. The agent can still
    read the record files directly; Codex 0.160.0 cannot prevent that, and
    such reads are not recorded.

## Modules

| Module | Contribution |
|---|---|
| `src-tauri/src/hosting.rs` | HOSTING/ACCESS lifecycle, generation, request correlation, ordered native journal, development verification and network disclosure; reviewed 0.160.0 protocol resources in `resources/supplier/` |
| `native_requests.rs`, `recovery.rs`, `native_items.rs`, `access.rs` | Typed native request custody, pointer ledger, scoped live/ended activity and reported account/destination observations |
| `src-tauri/src/recovery_store.rs`, `recovery_store_tests.rs` | The pointer ledger's SQLite store (DEL-01-02 §7): append-only triggers, one transaction per batch, synced commits, the held current entries' indexed query, the once-only JSON Lines import; tests include the flat cost from 1,000 to 100,000 rows |
| `role_supply.rs`, `runtime_session.rs`, `resources/instructions/` | Reviewed v4 defaults, fixed composition bytes, seeding and generation-bound receiving/startup; supplier/model adoption remains a separate warrant |
| `catalog.rs`, `proposal.rs`, `external_adapter.rs`, `receiving.rs`, `external_observation.rs` | Reviewed receiving contracts and exact person-selected observation custody; no external host dispatch or origin verification implied |
| `src-tauri/src/schema_validation.rs`, `schemas/` | W-1 plus complete package/offer/capture checks; declared-ID registry with external retrieval disabled; embedded resources checked by `schemas/sync.py` |
| `src-tauri/src/records.rs` | Validated append, UUID identities, sequence/read completeness, serialization and ordered capture late-write accounting |
| `src-tauri/src/records_index.rs`, `records_query.rs`, `records_index_tests.rs` | RS §13.8 derived SQLite query cache: disk-backed identities and positions, streamed rebuilding, authoritative line revalidation, and source-scan fallback; cache metadata is disposable |
| `src-tauri/src/record_lines.rs`, `record_lines_tests.rs` | RS §13.8 lines: one entry or one group per line (read whole or not at all), each line's chain link to the one before, unchained (legacy) and broken-chain limits, and each log's chain head |
| `src-tauri/src/records_access.rs`, `records_access_tests.rs`, `records_continuity.rs`, `records_continuity_tests.rs`, `resources/runtime_core/records-read-log.entry.schema.json` | The agents' read-only records capability (RS §13.9): the offered tool, its storage-independent source (the logs R-1 discovers: the project's records store subtree, or §13.7 logs before an import), bounded quoted pages and the read log written before each answer; tests include a fake-peer journey in which the agent calls it |
| `src-tauri/src/records_store.rs`, `records_store_tests.rs` | The App's records store (RS §13.8): placement and the explicit override, project identity and its limits, the explicit import of §13.7 records, and the host status `recordsStore` |
| `src-tauri/src/records_export.rs`, `records_export_tests.rs`, `tools/verify_records_bag.py` | RS §13.8 BagIt export: native folder selection, byte-preserving payload and prior administration snapshot, SHA-256 manifests and copied-log chain heads; package verification in the App and a standalone Python verifier |
| `src-tauri/src/records_retention.rs`, `records_retention_tests.rs`, `resources/runtime_core/records-administration.entry.schema.json` | Native close/reopen, legal hold/release and recorded disposal after verified export; surviving administrative evidence, stable write admission and activity leases, truthful partial-failure recovery |
| `src-tauri/src/storage.rs` | Store, project/run/writer and library paths, R-1 discovery (store subtree, or §13.7 paths in place before an import), atomic capture persistence and locking |
| `src-tauri/src/recorder.rs` | Package byte snapshot and request/provenance-limit mapping |
| `src-tauri/src/act_control.rs`, `act_control_a15.rs`, `act_control_file.rs`, `file_act_native.rs`, `canonical.rs` | A16, hot A15 and App-file offer/native custody; capture versus publication uncertainty, ordered retry and original content binding |
| `file_act_root.rs`, `file_act_view.rs`, `src/FileActPanel.tsx` | Original file-offer ownership, separate read-only act/decline comparison and per-offer controls; no cold native-origin upgrade |
| `src-tauri/src/decision_view.rs`, `act_policy.rs`, `standing.rs` | Decision projection, A16 method-aware standing and provenance limits; recorded claims do not establish native act admission |
| `attachments.rs`, `hosting::attachment_custody`, `resources/attachments/` | Native-selected immutable ordered text sources, durable metadata/client pointers before scoped send, and explicit native outcome limits |
| `trace_receiving.rs`, `record_relations.rs` | Independent unverified trace imports and general record correction claims; neither verifies native origin |
| `native_history.rs`, `role_lifecycle.rs` | Read-only native history, scoped Continue receiving and immutable original guidance bindings |
| `role_observations.rs`, `role_observations_tests.rs`, `role_observations_host_tests.rs`, `src/ConversationRoles.tsx` | App start/fork supply observations and exact retained App guidance bytes, with explicit quoted cold-history inspection; cold claims restore no role/CCE authority, and the R3 reference/resolver receiving path remains unbuilt |
| `connector_standing.rs`, `connector_route_store.rs`, `connector_route_view.rs`, `src/ConnectorRoutePanel.tsx` | Provider-independent standing, caller-account persistence (in the project's records store subtree; earlier in-project accounts read in place until imported) and read-only inspection; saved claims do not verify source truth or actor duties |
| `src/RequestCards.tsx` | Readable DEL-01-04 request cards, item anchors and the waiting-request indicator; answer values come unchanged from the host's register |
| `src-tauri/src/codex_stop.rs`, `src/CodexControls.tsx` | Stop/Restart Codex (DEL-01-02 §4.1 C-12 with the DEL-01-04 §5.2 question): live-work assessment with runs in force, ask-first sequence, the ledger `codex_stop` record, interrupts before the stop within the stop wait limit, TO-4 labels and the in-process outcome panel |
| `src-tauri/src/app_quit.rs` | App quit asked first (DEL-01-02 DEF-6, K-4, SQ-Q; DEL-01-04 §5.2): assessment across homes, `quit_requested`/`quit_answered`, quit interrupts (cause *quit*), the exit's process stops and `session_ended` (AS-09, AS-10); the DEF-1 exit rule; the C-24 waiting count |
| `src-tauri/src/stop_records.rs`, `resources/runtime_core/recovery.stop-request.schema.json` | REC stop-request records (DEL-01-02 §3.4 SR-01…SR-12): validated transitions and outcome labels, the `codex_stop` ledger entry, and the read-back after a relaunch; the Host writes them through its recovery writer before each interrupt send |
| `src-tauri/src/hosting_recovery_reads.rs`, `execution_custody.rs` | Recovery after a restart (DEL-01-02 §3.2 CV-11…CV-15, CV-19, CV-22; SR-09): the reads on the home's ready process, `observation_lost`/`observation_recovered`/`turn_outcome`, and the conversations' recovery states in the ledger; run on the host's trial tick or on the person's retry |
| `src-tauri/src/checkpoint_recorder.rs` | EXEC §2.4 first slice: CE-1 listing, CE-3 arrivals from observed AW-6/AW-7 native items, CE-11/CE-12, CE-17 waiting arrivals; written through the run's RS writer with CE-19 late-write limits; never reacts (RC-4) |
| `src-tauri/src/model_turn_recorder.rs` | RS R5 `model_turn` entries (HOSTING §8.3): thread-scope reports and one entry per run turn, effective only from a `model/rerouted` naming the turn; observes `native_items.rs`'s `modelReroutes` and the host's thread rows; never reacts |
| `src-tauri/src/run_restart.rs`, `run_restart_tests.rs` | EXEC §2.7 / RECOVERY §4.1: the REC run tag at `run_opened` (owner `DEL-02-03`) and the host's startup writer of RS "App-restart interruption" limits; tests also cover WR TX-5 / SQ-END end notices after relaunch and (j) permanent refusals |
| `src-tauri/src/run_offers.rs`, `src/RunOffers.tsx` | Exact run-offer line forms (WR §16.5 PR/FN), the finished-report proof for a *completed* end, and their presentation beneath the message |
| `src-tauri/src/workflow_drafts.rs`, `src/WorkflowDrafts.tsx` | DEL-02-02 draft workspace in the Rust host (SQ-D D-2…D-4 observation, hygiene, §5.1 states) and its list presentation in NIR §7 words, with the two Try buttons and each draft's trial list; nothing here registers, reviews or runs |
| `src-tauri/src/workflow_trials.rs`, `workflow_package_copy.rs`, `workflow_workspace.rs` (`compose_run_text`, `TrialText`, `files_folder`) | DEL-02-02 trial core (WR §17 steps 1–4): one composer for run texts and trial texts (TT-3), TX-7's files-line folder with content-addressed supply copies, TT-8 trial snapshots, and the create-once TT-4 trial links and observations |
| `src-tauri/src/trial_flows.rs`, `workflow_trial_transcript.rs`, `src/TrialComposer.tsx` | DEL-02-02 trial flows (WR §17 steps 5–8): pre-filled delegated and clean trials sent only by the person, links on acknowledgment, TT-9 linking and fidelity reads, bring-back transcripts, Compare, TT-2's run refusal and offer silencing, the review's last clean trial line; the composers in the conversation view |
| `src-tauri/src/host_tick.rs` | The host's own ticks (OI-008): a record tick receives native frames and records checkpoint observations, and a separate trial tick makes due trial reads, whether or not the interface polls; each tick is guarded and a failure is shown in `host_status`, which only reads |
| `src/RunPanel.tsx` | Run panel and selected-workflow view (NIR §9 PD-1…PD-7): readable declared part, checkpoints as guidance with their recorded listing and arrivals, the run-record write notice, output standing facets from the record only (AS §8), readable advisory compatibility |
| `src-tauri/src/conversation_roles.rs`, `src/ConversationRoles.tsx` | Continue as ‹role› handoffs and same-role Fork through the Host (NIR §5.8, ROLE §3.3), the role limit account (ROLE §6.2), the readable start display, role header and guidance-changed flag (ROLE §4.4) |
| `src/NativeActivity.tsx`, `src/PlanMode.tsx` | Readable per-thread native activity from the `native_items.rs` view (DEL-01-03 plans/tools/delegation with the DEL-01-04 message part) and the experimental plan-mode element |
| `src-tauri/src/lib.rs`, `src/App.tsx` | Native command boundary and presentation; the webview cannot confirm a capture itself |

## Offline build and checks

Use Rust 1.97.1, Node 24, Python 3 and prepared Cargo/npm caches. Set
`CARGO_HOME` to the dependency cache you prepared if it is isolated. The offline
commands require those caches to contain the locked dependencies; use the
[developer start](#developer-start) to prepare dependencies when downloads are
authorized.

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

On macOS, the opt-in records supplier check uses that already prepared binary
with fresh credential-free homes and a localhost-only OS sandbox. It captures
declarations for started, resumed and forked threads, includes threads without
the capability as negative controls, and returns HTTP400 without a model
prediction. Decoded frames and requests stay in the reported private scratch
directory. From `app/`:

```sh
records_probe_dir=$(mktemp -d)
CHIRALITY_SKIP_CODEX=1 cargo run --offline --locked --manifest-path src-tauri/Cargo.toml \
  --example records_tool_definition > "$records_probe_dir/definition.json"
python3 supplier_checks/records_delivery.py --codex "$CHIRALITY_CODEX_BIN" \
  --definition "$records_probe_dir/definition.json"
```

Add `--include-flat-model` to exercise the supported alternate flat function
renderer as well. The check reports the actual model/provider and hot/cold
`namespaceTools` values; a flat declaration does not establish a false value.

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

The App keeps a project's records in its own records store (RS §13.8;
`src-tauri/src/records_store.rs`), outside the project and every Codex home:
`<App data>/records/` by default, or a folder the person chose (from the next
start). Tests and development name it with `CHIRALITY_RECORDS_STORE`; a
development build without it records nothing, and there is no fallback. Each
project has one subtree, `projects/<safe-project-key>/`, holding
`runs/<safe-run-key>/<safe-writer-key>.jsonl`, `acts/<safe-writer-key>.jsonl`,
`captures/` and `workflow/` (WR WP-1 records), and the App's own logs for the
project (U-STORE-6, "Split by who writes"): `connectors/route-accounts/`
(connector route accounts) and `reads/records-reads.jsonl` (the agents'
records read log). The project is linked to it by
`.chirality/project.json`, an identity the App mints once; the store's own
record of the project's roots governs. A changed link is a limit; a missing
or unreadable one, a duplicate, or a moved project attaches nothing until the
person restores the link, adopts the project or gives the folder a new
identity. Records an earlier App wrote at the §13.7 paths
(`.chirality/records/runs/`, `…/acts/`, `…/workflow/`, `.chirality/captures/`,
the registered `records/coordination.rs.jsonl`, and connector route accounts
in `.chirality/records/connectors/route-accounts/`) are read in place, and
recording is refused ("import needed") until the person imports them:
byte-identical copies verified by SHA-256, committed by the import's
"completed" line (an interrupted import is resumed by running it again), with
the originals left unchanged and no longer read. A copy carries only the
trust of the folder it came from. A library's own act log in the project is
library evidence, never part of the project's record set. The override
`CHIRALITY_RECORDS_STORE` is read only by development and test builds, and a
store inside the project or a Codex home is refused. The host status (`recordsStore`)

shows the store, the project's identity and any import or identity limit.
The records-store panel offers **Export project records**, choosing a parent
folder natively and creating a new verified BagIt package. Its payload preserves
project store files byte for byte, with SHA-256 manifests and each copied RS
log's chain head. Store-wide query caches and the two known owning lock controls are omitted;
imported connector publication evidence is preserved.
**Verify an exported package** checks inventories, hashes and RS heads again.
The included `verify.py` checks bytes and inventories with standard Python 3,
without the App. Exports are unsigned until App signing; byte verification
confers no source authenticity. New packages include a protected
`records-administration.json` tag, reversibly retaining each prior administrative
event's exact UTF-8 bytes and its project identity. Legacy packages without it
have unknown retention history and cannot satisfy disposal prerequisites.
New export folders and files are owner-only from creation (0700/0600),
including staging and intermediate payload folders. Verification changes no
existing package permissions. Package import remains unbuilt (RS §13.8).

Records have no expiry. The records panel offers native **Close project** /
**Reopen project** and **Set legal hold** / **Release legal hold** controls.
Close only after supplier activity, hot workflow runs and pending native record
publications have settled; the App never ends them implicitly. Closure prevents
new App recording and Codex starts for that identity. A hold prevents disposal, including finishing an incomplete disposal. A closed
retained project can still be explicitly adopted after a folder move without
reopening its records.
**Dispose of records after verified export** requires closure, no hold and an
existing verified bag matching every current payload byte and the prior
administrative history. Its native question freezes project, actor, closure,
hold and export/payload identity; the host rechecks them after the choice.
Only that project's `projects/<key>/` subtree is removed. The verified export,
project/library files and `administration/<key>/events/<sequence>.json` history
survive. Each create-once administrative event has the previous file's exact
SHA-256 and records the unverified observed person separately from the App
recorder. Disposal's original native act is durable before removal; completion
is an App observation. An incomplete disposal blocks recording and offers
**Finish disposal**, verifying the original export and every remaining source
or staged file as an unchanged member of it. Members move exclusively to
`administration/<key>/removal/<original-relative-path>` before checking against
the original manifest and unlinking; unknown bytes are retained, and empty-only
directory cleanup never sweeps late files. The original bag/source context is
rechecked after the durable act publication. A visible but unsynced completion
is shown as completion durability uncertain, with Finish disposal syncing the
existing evidence instead of recording another act. No automatic deletion or retry is performed;
malformed administrative history, extra/changed remaining files and changed
exports refuse the operation. Disposed identities cannot be re-imported,
replaced or silently reassociated. Ordinary project/WR reads reject disposed or
incomplete identities even if source files reappear; retained legacy originals
never become the record source again. The App remembers observed administrative
heads; a durable history-started marker detects cold missing/empty event history.
Missing history must be restored from verified evidence. Unsigned evidence cannot
detect cold removal of a valid nonempty tail or the whole administrative control
including its marker, and cannot verify actor identity or outside time.

The fleet coordination log has no App writer yet (DEL-06-01). When it is
built, the log stays one co-written file in the project,
`.chirality/fleet/coordination.fleet.jsonl`, with every entry, and the App
also records its own observations in the store (`fleet/coordination.fleet.jsonl`),
whose copy governs inside the App (owner: "Write to both (Recommended)";
FLEET_RECORDS FR-D1). File-native readers read the project file as it is. That
file is not the registered legacy log `records/coordination.rs.jsonl`.
Library A15 allocation uses the library's
`.chirality/records/acts.jsonl` and `.chirality/captures/`; its native registration
witness remains unfinished. There is no registration attempt journal (owner
ruling 2026-10-10): when a library is opened, SQ-X finds A15 records that no
ledger line cites and decides from the record and the revision store (WR §6
X-1, X-2; WR §4.8 / SQ-X (b)). Each open review holds
`.chirality/workflow-registration.live.lock` shared until its attempt is
closed, and X-2 runs only when it can hold that file exclusively, so a live
attempt is not closed as lost while its review holds the lock (tested with
separate owners in one process; release at process death is `flock`'s, not
tested). A
`.chirality/.workflow-staging/attempts/` folder left by an earlier build is
no longer read. Storage keys are separate from governed identities.
Explicitly registered legacy `records/coordination.rs.jsonl` stays intact (imported, not rewritten).
Unwritable or incomplete targets report limits without silent relocation.

Each RS line the App writes is linked to the line before it in its log (RS
§13.8 Tamper-evidence: the SHA-256 of that line's bytes), and entries that
must stand together, such as an act counted and the disposition change it
makes, are written as one group line and read whole or not at all. Lines
written before the chain, imported ones included, read as "unchained
(legacy)", a limit that leaves the log complete; the chain starts after
them. An edited, removed or unlinked line after the chain started is a broken
chain: the log is incomplete and nothing repairs it. Until a chain head is
kept elsewhere (signed checkpoints, export manifests), removing a log's last
lines, or every link of a log this process has not read chained, is not
detected. The host status
(`recordChain`) shows bounded counts of chained, legacy and broken logs;
each log's chain head comes on demand (`records_chain_heads`).
Signed checkpoints wait for App signing (OI-011).

The derived records index keeps identities, positions and membership counts in
process-owned SQLite files under the store's `indexes/`; record bodies stay in
their logs. Cold use rebuilds from authoritative sources, and returned entries
are reread and revalidated, including their exact line hash. Changed or unusable
caches rebuild or use source scans. A private temporary cache can serve a process
when the store cannot host derived metadata; records themselves have no fallback.
Index metadata for ordinary valid entries is per log and directory; diagnostics
grow with reported limits. Full act projections retain their
separate result-sized memory cost (RS §13.8, §14.3).


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

App-file act and decline captures are sealed with this installation's key,
kept in the App user-data `capture-seal/keys.json` (owner-only), and only a
capture whose seal verifies there counts (AAC §6.3 SEAL-C; AAC §6.3 / EXEC §2.4–2.5). This
narrows R-1 but does not close it: anything that can read that file, including
an agent under Codex's default read access, can seal. Trustworthy persistent
cold replay remains unfinished under AAC §6.3 U-AAC-3 and I3-CUST, and SEAL-2 stays
deferred. Current code refuses unverified replay while preserving evidence.
Native authenticity, real process-kill/fsync failure witnesses, durable history rebuild (the recovery reads after a restart, item 22b, read metadata and turn summaries only), native witnesses of those reads and cold role-source reconciliation, child role supply, native A15/registered-library and file-act witnesses, and remaining policy/standing/control journeys remain in the Group A graph. Per-home configuration/resource linking is implemented with observed ownership limits. CommonMark parsing and one closed, explicitly development-candidate workflow catalog are supplied; the production native-page supply path and hot registration transaction are implemented, while their actual native consumer witnesses remain separate. General file/arrival entry surfaces and complete file-act lapse-history evidence also remain unfinished: lapses are recorded only for acts that answer an arrival of a live run. External dispatch and host qualification remain unsupplied. Native text-turn and interrupt controls use the selected native thread and
retain generation/terminal limits. Transport and receiving tests do not prove a
provider prediction. A separately frozen controlled live backend greeting passed;
its exact source pins and limits are recorded in the run. An approved no-supplier native window inspection establishes tool/window reachability only; corrected UI/storage, browser/device/auth/provider and capture journeys remain separate unfinished witnesses. Host joins stay deferred to their owning sessions.

REC stop-request records and the ledger `codex_stop` entry (item 22) are
appended to the existing pointer ledger, as are the conversations' recovery
states (item 22b, `conversation_index` rows). Checkpoint entries (item 23) go to the
run's own RS log. Neither opens a new store.

The run panel (item 23) records output arrivals (AW-6, AW-7), harness-capability
call starts (AW-3), requests, counted App-file acts and, while the run is live,
their lapses, with their labels and recording gaps, and the Codex observation
losses and recovery reads of its conversation in this App session (CE-1…CE-6,
CE-8, CE-10…CE-14, CE-17…CE-19). It does not yet record host-operation or
host-outcome arrivals, A5 items or A12 relations (CE-7, CE-9), the *unknown*
label of a deciding loss, losses or recoveries of an earlier App session,
replaced arrivals (CE-15, which follows only from A5
items), anything after the run's end (CE-10 *after run end*, CE-16), or output
records. An output gated by a checkpoint shows that checkpoint's recorded act
standing, *lapsed* included; an observation loss or recovery still makes an
output's facets unknown.

Each run also records RS R5 `model_turn` entries (HOSTING §8.3), through the
same writer and the host's record tick. The host keeps `model/rerouted`
notifications as observations; it changes nothing it sends. Every thread-level
report of the run's conversation (thread start, resume or fork, from the run's
generation on) is written with scope *thread* and no turn. Each turn of the
run (the conversation's turns from the start turn on, observed live while the
run is open) gets an entry with its ordinal in the run, written when the turn
is observed to end, or at the run's end before `run_ended` for a turn still
live. `requested` and `effective` are written as "‹provider›/‹model›",
as "‹model›" when no provider is known, or as *unknown*. A turn's `requested`
is the App's request in force for it, from the App's own `turn/start` as the
host correlated the response. A plan- or default-mode turn carries
`collaborationMode.settings.model` (the conversation's reported model) and
asked for that. A plain text, run or attachment turn carries no model, so its
`requested` is the latest request the App sent for this conversation in this
Codex process: the latest mode's model, or else the provider and model the
App asked for at thread start. That Codex keeps a mode for later turns is its
documented behaviour (item 18); it has not been observed, and no witness has
shown which model a later plain turn actually ran under. A mode turn's
`requested`, and a plain turn's that inherits it, is "‹model›" with no
provider, because the mode element carries only the conversation's reported
model. A turn the App did not start, a plain turn after a mode sent in an
earlier Codex process, and a conversation the App did not start in this
session have *unknown*. `effective` comes only from a `model/rerouted`
naming that turn, otherwise *unknown*, never from the thread or an earlier
turn. Each re-route is recorded with its turn, `reroute` true: a turn
re-routed twice gets two entries, and a re-route received after its turn's
entry was written is a further entry for that turn. With no re-route observed
`reroute` is omitted, since `model/rerouted` has not been observed live
(HOSTING U-19) and its absence shows nothing. The destination class is DEL-01-05's mapping of the access entry,
known only for the conversation the home last started (otherwise *unknown*).
The re-route's reason and the native turn identity have no place in the entry
body. Nothing is recorded after the run's end.

Conversation roles (item 24)
keep handoffs in process memory and write no persistent role-supply log;
delete or archive beside Fork waits on U-R13.

The ask-first App quit (item 22a) and the startup SR-08 write are
implemented but not witnessed natively, as are the startup RQ-06 endings. The Restart Codex question
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
command can still complete (see the note), and the bundle gap PKG §4.1 P-2/P-3 (since
fixed: the default configuration declares the instruction and workflow
resources).

Open contract conditions live beside their governing clauses in each
deliverable's `Design/`. Implementation discoveries are added there; the PR
describes the repair and its verification. Retain a witness or capture in
Design only while a current requirement, test or ruling uses it.

## Recorded connector route accounts

With an explicitly associated App project, **Read / refresh accounts** inspects
its canonical connector route-account directory without creating it: in the
project's records store subtree (`connectors/route-accounts/`), or, before the
person imports them, the accounts an earlier build wrote in the project, read
in place (CRP-v0.3 §1). The view says which. Accounts are written only in the
store; reading mints no project identity. A binding taken before the import
names the original file and is refused afterwards as a location mismatch for
explicit reconciliation; it is never rebound to the copy. The view
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
