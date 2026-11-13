# Chirality App v4 — runtime contract development

Run `APP-V4-GROUP-A-20261004` repairs and extends the walking skeleton from
`APP-V4-GRAPH-CLOSURE-20261004`. The current development integration targets stock Codex 0.167.0,
supplies reviewed v4 common/role guidance, receives native requests and activity,
loads external observations, records decision packages, and supplies native controls
for A16 decisions, A15 workflow registration, and A4/A6/A7 App-file acts. Separate
readers retain decision and file-act evidence limits. App v4 development resumed
by owner direction on 2026-10-28; packaging, supplier qualification and the owner's
stage gate remain separate work.

The 0.167 upgrade uses the exact canonical 42-file package and its
generated-schema subject under an unqualified development admission. The installed npm 41-file tree shares its
main but is not that acting distribution. The historical 0.160 supplier checks
and examples below retain their own pin/input requirements; they are not 0.167
runtime qualification. Production still refuses the old compiled reference.

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
run from `app/` in this repository.

Use Rust **1.97.1**, Node **24** and Python **3**. These Rust and Node versions
match [App v4 CI](../.github/workflows/app-v4.yml). Install dependencies
with `npm ci` when downloads are authorized, or use the prepared-cache route in
[Offline build and checks](#offline-build-and-checks).

```sh
npm ci
npm run build
(cd src-tauri && cargo build --locked)
```

Before running the historical supplier-dependent checks below, prepare their complete stock Codex
0.160.0 platform package and set the binary path and expected hash as described
in [Offline build and checks](#offline-build-and-checks). For a development
launch, follow [Run the development App](#run-the-development-app), including
its scratch workspace and Codex home. The offline stand-in does not run a model
turn. [Storage and remaining work](#storage-and-remaining-work) states the
implemented behavior and qualification limits.

## Current path

1. The Rust host starts the stock App Server, completes its handshake and keeps
   native frames with full `{appSession, home, spawnCounter}` generation identity.
   Startup EOF reports a handshake failure with observed exit facts if that
   attempt is still handshaking at settlement. Stop or replacement can win
   settlement; held startup frames keep the never-ready marker. The host keeps
   the actual leader reservation through every process-group census/signal.
   Unexpected EOF leaves surviving descendants running; natural empty-group
   cleanup reaps only the original leader. Later Stop retains its actual exit
   facts. Counts describe live members of the original reserved process group;
   detached or escaped descendants are unobserved. Current lifecycle JSON gives
   an unavailable count as
   `checked:false`, `surviving:null` with a reason; legacy records stay readable.
2. The person chooses a primary role (or none) and explicitly enters a model
   and a configured Codex provider for a new thread. The actual native
   configuration must establish that this provider matches the chosen access
   entry before Start, Continue as or a clean trial dispatches. Private config
   replies/errors are projected to safe outcomes; unavailable definitions refuse
   without a fallback. This is a source/folder observation, not a lock on later
   configuration or a credential-validity check (ACCESS §5.4). Codex retains its
   own configuration and permissions. The view
   discloses expected model contact at thread start, before a turn; it does not
   represent that notice as measured socket traffic. Reviewed v4 guidance seeds
   an editable App instruction copy without overwriting edits; new conversations
   read current bytes. The Rust host prepares additive native child roles
   from that frozen guidance, withholding colliding or unsupported names and
   rechecking configuration/source currentness before dispatch. The opt-in
   [supplier child-carrier check](supplier_checks/child_roles.py)
   distinguishes production preparation and scripted stock-supplier carriage
   from the App's private-receipt/live-association checks and qualification.
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
    Received turn summaries show native status, item coverage and message previews;
    the selected item page reads messages, reasoning summaries, plans, substantive
    tool results and delegation through the shared native item renderer. Each
    page identifies its source home, conversation/turn and direction and retains
    its complete native JSON and exact query evidence. Pending, failed or foreign
    stream resolutions withhold readable old rows and paging rather than assign
    them to the new request. Only the selected received page is rendered; this
    does not automatically read all history or keep a transcript copy. Statuses
    are observations at the read, recovered plans have no live revision number,
    and earlier checklist updates remain unrecoverable. Stored item rows have no
    live item anchors, request links, workflow offers or act controls.

    After an admitted **Continue selected conversation**, the opened conversation
    shows a separate prior-work context. The host queues the latest native turn
    page, then the newest received turn's item page. Each initial read is bounded
    (20 turns, 50 items); cursors are never drained automatically. Older turns
    and item pages remain explicit reads. Loading, empty, partial and unavailable
    states do not undo the admitted conversation or resend a message. This
    memory-only context belongs to the actual resume receipt and source, so a
    different stored-history selection cannot retarget it. It supplies no live
    execution, request, role or act authority.

12. Native text-file selections retain private handles and an ordered immutable
    source list. Explicit attachment-bearing send or steering uses that whole
    list, durable metadata and the actual Host request; failures do not fall back
    to text-only sending or automatic retry. A native acknowledgment is separate
    from provider uptake or completion. A failed view refresh is shown
    separately from the original Send or Steer result: it does not turn an
    acknowledgment into a rejected command or replace a native error. When a
    run-end notice is pending in the
    conversation (WR TX-5), an attachment-bearing new turn carries it in one
    frame, in NIR TC-2's order: the run-end line, then the person's text, then
    the attachments. The supply records still name only the attachments, in
    their order. The notice is marked sent only once that frame's write was
    attempted; a send refused or failed before then leaves it pending. An
    attachment steer is not a new turn and does not carry it.
    The Host's private positive attachment acknowledgment also saves the notice's
    exact original turn/client boundary in pointer-only REC metadata. With the
    original records and native history available after an App restart,
    **Bring a real run back** and **Compare** can read the closed run without a
    manual supply check; the carrier and later turns are excluded. A failed
    metadata save preserves the send and offers metadata-only retry while the
    original observation is held in this App process.
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
    **Observe file-act content changes and save history** records lapse
    observations for existing standing A4/A6/A7 file acts in the project's act
    log. Reading alone stays read-only. Recorded intervals, current comparison
    and unresolved source claims are shown separately. Each source log keeps
    its own sequence, including arrival history for a standing act later used
    in a run; order between logs is unknown. A return to the original bytes
    renews no act. Failed saves keep the original observation in this App
    session for **Retry saving held metadata only**, which writes metadata
    without capturing another act or replacing the observed content/time.
    Request/output/workflow links open the standing facility only through a person;
    they do not invent an arrival reference or settle a supplier request.
    An eligible live single-file arrival also offers an explicit review entry.
    The host resolves its original run, written arrival, declared kind, subject,
    scope and purpose, then freezes the matching file bytes for review and a
    separate native act/decline/cancel. Capture and record retain their run and
    arrival links in the original run log. Reopened-only history, ambiguous or
    stale sources and unsupported subjects stay unavailable for this entry;
    arrival display alone opens nothing. Existing checkpoint recording decides
    whether the act counts and never treats capture as resuming the run.
16. Workflow selection, owner-held review, hot A15 capture and immutable library
    registration are connected to prepared input and source-owned native page
    comparison. Code and synthetic checks do not establish a native person's
    registration, provider uptake or completed workflow execution.

    Opening a project or user library shows its observed workflow entries.
    **Refresh library entries** observes later changes. Choose eligible entries
    in the desired order, then **Review chosen entries…** to open their existing
    in-place review. The host rechecks the listed source and bytes; file presence
    alone registers or selects nothing. Unreadable or already registered entries
    show their limits and retain the existing revision controls.

    One existing unregistered library entry can also be reviewed in place through
    **Review this unregistered in-place library entry**, followed by native
    **Register** confirmation. Its single A15 uses the reviewed `entry:` reference
    and no prior revision; no draft is created. Only the newly captured hot
    registration makes it selectable here; quoted earlier history remains separate.
    The complete registration review shows literal workflow text alongside its
    target, content identities, files, findings and reported prior/base changes.
    The same frozen review remains readable while its native confirmation is
    open. Its digest and complete reported data remain available; reading the
    review captures no act.
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
    the selection unchanged. A run's files line (WR TX-7) names that folder
    project- or `~`-relative when possible; otherwise preparation creates a
    content-addressed supporting copy in the explicit project. An unattempted
    Send rechecks that generated copy against the original selected package,
    retaining the original revision-store check even after prepublication.
    Changed, missing or nonplain content refuses the start without rewriting
    the copy or prepared text. The selection still records its original
    holding library and revision store. Other rows keep Refine and re-confirmation through a
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
    other; the row never answers. About reveals an already-received parent or
    descendant item in the read-only activity view without changing the operational
    conversation or its unsent text. A row outside the current source/subtree
    keeps its supplier identity instead of a dead link. The top of the App counts current requests
    waiting for the person across configured homes, grouped by original source
    and conversation; opening one answers nothing. Requests of other
    conversations in the selected home stay listed under Native requests.
20. Workflow run offers come only from agent messages this App observed complete
    live. On the exact `Workflow finished: ‹origin›:‹name›` line naming the run in
    force, the message offers **End run**; the host re-reads the message and
    records cause *completed*. Any other end is "ended by the person"; no command
    can record *completed* without that observed report. On the exact
    `Next workflow: ‹origin›:‹name›` line naming one registered workflow held in
    this session, the message offers **Start ‹workflow› (proposed by the agent)**,
    or **End ‹A› and start ‹B›** while a run is in force (*completed* when the same
    message reports A finished). The proposal selects nothing until the person
    presses. Before that choice, the resolved candidate's advisory report shows
    its requirement purposes, the conversation's fixed role and the limits of
    the environment evidence. Unknown, unsupported or unavailable evaluations
    leave Start available; displaying the report selects, prepares and sends
    nothing. The selection is then recorded as "agent proposal confirmed by the
    person". The press rechecks the displayed source, message, current run and
    candidate, then resolves the proposed revision from the revision store
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
    A returned workflow command response stays visible if a later view read
    fails, with that observation limit shown separately. Create draft and
    Refine still attempt one draft observation through their original context;
    this does not repeat the write or infer that a native error left no files.
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
    10 s (U-R4 test value). The same deadline bounds each interrupt's write.
    Each interrupt is written on its own thread. If Codex is not reading its
    input, another write may hold the writer, or the interrupt's own write
    may block. Either way the host stops waiting at the deadline and goes on to
    stop the process. Ending the process group ends the blocked write.
    The outcome says, for each turn, whether the interrupt was acknowledged,
    sent and not acknowledged, not sent (with the reason), or of unknown
    write outcome. Each turn then shows one of the four TO-4 labels:
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
    next state: sent or not sent (SR-02/03; not sent only when no write
    began), Codex's answer (SR-04/05/12), the
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
    not list the items or delegated agents at the outcome. An interrupt whose
    write began and did not complete is recorded as neither sent nor not sent.
    The Design's send values have no value for it, so its record stays at
    SR-01. In this App process its record notes that whether it reached Codex
    is not known; after a relaunch it reads as a request whose send was not
    recorded. A turn that ended
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
    turn's stop request (SR-01, cause *quit*) and its interrupt, whose write is
    bounded by the same limit as Stop Codex's; the App waits
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
    question. The Dock indicator gives a count only, and clicking it opens the
    App. The macOS App's **Waiting requests** menu additionally names current
    source-qualified conversation groups; a person selection shows the window
    and uses guarded navigation to that original source. A process-owned,
    single-use handoff survives missed wake events and explicitly refuses
    interrupted, superseded or unconfirmed-view navigation; choose again from
    the current menu after the view is acknowledged. Cleanup failures retry
    cleanup without replaying navigation. These checks do not establish native
    menu interaction, other-platform outside-window coverage or person
    qualification. A bounded idle application-menu Quit was witnessed natively
    (see the native-observation summary below); its live/unknown-work question
    and durable final writes remain unwitnessed.
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

    These custody reads remain metadata/turn-summary reads. Item 11's separate
    prior-work context follows explicit Continue and changes no CV recovery
    transition, observer rebuild or ledger retention rule.
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
    run gets RS's "App-restart interruption" limit instead). The independent
    project record tick observes eligible later App-file acts (CE-16), and
    changes to the bound file of an already performed single App-file A4/A6/A7
    checkpoint (CE-10/CE-18), after its run ends. Hot and reopened views show
    these observations with their source and publication limits; continuation
    inherits no prior performance. A path is compared as text (U-E26).
    Recording uses the Rust host's own ticks across its held homes and project
    sources, independently of web-view refresh, and when the person ends the run. Each declared output shows its
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
    The direct **End this run and start** choice shows the chat's selected
    successor and its own advisory before the button, including its source,
    revision and holding library. Unsupported, unknown and unavailable
    evaluations leave the existing choice available; the displayed selection's
    original context is rechecked by the existing chaining command.
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
    start display lists the role set readably, each role with a plain line
    from its shipped guidance, with the `default_for_new_chat` role shown
    preselected and clearable (HELP_HUMAN in the bundled set, DEL-02-04
    TBD-004), "No role", and each role's limits as the limit account hands
    them, in plain words (TASK "A task agent does not delegate: Stated, not
    enforced", then that Codex does not enforce it and that approval, sandbox,
    configuration and depth do not either; a modified copy reads not known). The start display and Continue as offer HELP_HUMAN,
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
    the person sends it. The host keeps that original send attempt and its
    source receipt. A received native turn result stays visible if refreshing
    the view fails. Pending, incomplete-write and unavailable outcomes remain
    unknown and block another handoff send. **Read the original send outcome**
    observes that same attempt without sending again; only a proved no-attempt
    outcome offers an explicit retry. A native error remains separate from
    both no-attempt and unknown.
    **Fork (same role)** sends `thread/fork` with the thread id, no
    instructions or settings, and `deferGoalContinuation: true` so that a
    source goal starts no automatic turn in the fork that the person did not
    start. It admits the fork only when Codex reports a new thread
    forked from the source; the fork inherits the source's role binding. The
    App opens that admitted fork only when its matching row is observed in
    the original source view. A failed refresh leaves navigation pending for
    a later read; it sends no second Fork. Newer conversation choices, Start
    intents or home changes supersede that pending navigation. Neither
    changes the source conversation's role or record. Handoffs are kept in App
    process memory.

    Native child roles follow the parent matrix: HELP_HUMAN offers
    HELPS_HUMANS, WORKING_ITEMS and TASK; HELPS_HUMANS and WORKING_ITEMS offer
    TASK; a conversation with No role offers no child roles. Each
    content-bound App TOML file carries the complete common + child-role
    `developer_instructions`. Only
    `agents.<ROLE>.description/config_file` is added at `thread/start`;
    person-defined names, features, depth and permissions stay unchanged.
    Conservative name exclusion reads enabled supported declarations,
    referenced TOML content names and recursive native `agents/` sources.
    Unknown, unsupported, malformed, unreadable or changed context visibly
    withholds children. The path requires the acting supplier's recorded
    0.160.0 pin and identified stock `bin/codex` hash; a compatible response
    from another or unknown executable grants no child supply. Supported empty
    System context recognizes the standard macOS `/etc` alias; a config leaf
    link requires the App's owned descriptor and checked link/target
    identities. Native role roots stay at the reported home/project, never the link target's siblings. The reading establishes
    observed currentness, with no lock on later external edits.

    A live completed native started-child event can establish App child supply
    only with the same original generation/scope's private matched parent
    start receipt and correctly correlated child/parent/role metadata.
    `agentRole` alone, self/ancestor/fork/foreign references and older resumed
    or restarted parents grant no fresh association. An observed child's
    original guidance/limits stay fixed in memory for its same home/thread
    lifetime, including warm resume or Codex restart. Later native action may
    be compared with that original TASK statement. Across generations, live
    or quoted accounts separate original supply/association from the action
    generation and label the comparison as historical. This
    grants no new child association, renewed supplier uptake, role binding,
    CCE or current-source authority; current-run role attribution retains its
    own original-scope gates. Untyped or unmatched children retain unknown
    guidance. Observed TASK delegation is recorded and shown.
    Its default prohibition is **stated, not enforced**; an edited or
    unrecognized TASK copy keeps limits unknown. Native tools are not denied.

    The Rust host records each App start/fork attempt's actual supply
    observations in the project's explicit records store (ROLE §6.1a),
    retaining content-identified copies of the exact App-owned guidance
    bytes. New v0.3 observations also retain exact child compositions, source
    parts, TOML envelopes and historical limits; exact v0.1/v0.2 readers keep
    mixed history intact. **Read quoted role-supply history** inspects those
    bytes and recorded outcomes without a native request. Cold history is
    unsigned, unverified file evidence; it leaves the current conversation's role
    unknown and restores no role binding or CCE owner.

    A run opened with a confirmed original role supply records a role-guidance
    reference after `run_opened`, with adoption unknown. Its immutable sources
    retain the exact original guidance, historical limit assessment and
    source-qualified run-start context. The explicit workflow-supply read
    resolves these as quoted evidence and reports missing or substituted
    sources; reading files creates no role binding or native request.

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

    Full role-guidance records in a **read run** page can include a small
    historical metadata companion with source identities, recorded role limits
    and a narrow run context. Raw guidance and source rows are omitted; missing
    or oversized sources leave the original record visible with a qualified
    companion. This restores no role authority and does not check WR
    correspondence. The existing tool definition and read accounting remain
    unchanged.

26. The Rust host records actual **Fork** and **Continue as** relationships
    between native conversations in the selected project's records store,
    then copies each exact line to `.chirality/fleet/coordination.fleet.jsonl`.
    Session IDs are qualified by their actual native home/source. Recording
    requires no objective label or grouping choice. Unknown native outcomes
    and failed or uncertain recording remain visible limits; host ticks retry
    the original recording without sending another native command. The Fleet
    reader retains both format versions as quoted evidence. These logs are
    currently unsigned and unchained; cold reads restore no conversation or
    role authority.

    The host records what it observes of Codex's **native delegation** the
    same way, in the same 0.2 format (`fleet.native-links.schema.json`), with
    no undertaking named. A completed spawn item received live in a
    conversation of the selected project is written once as
    `dispatch_observed`: the home-qualified parent and child thread
    identities, the spawn item, the content identity of the spawn prompt
    (never its text, or that Codex supplied none) and the association. The
    association comes only from one line of the prompt,
    `Chirality-Brief: briefs/<file>.json sha256:<64 lowercase hex>` (path
    relative to `.chirality/fleet/`, digest of the file's exact bytes),
    compared with the brief file when the dispatch is recorded, and the dispatch
    records what that brief record itself states (its record identity, work
    item and undertaking): brief
    referenced, brief referenced whose content does not match the
    reference, brief reference not resolved (with the reason), or no brief
    reference. A match shows which brief was named, not that the child
    received or read it. A file that is not a brief record is never a
    reference that resolves, whatever its digest. `child_observed` is
    written when the status Codex reports for a child changes, and
    `observation_ended` when the generation it was observed in closes
    (Codex stopped or exited) or when the App itself exits (cause "App
    quit"). A session records the end only of its own observation, and every
    later fact of a child, in whatever generation of Codex reports it, goes
    through the recording context frozen when that child was first
    recorded, with the writer's physical check:
    nothing is ever written about a child another session recorded, or
    under another identity or folder, and after a crash or a kill no end is
    recorded at all. Each child's facts reach
    the store in the order observed; a later one waits while an earlier one
    of that child is unwritten. A dispatch establishes a child and its parent only. A spawn seen only in Codex history, or in a
    conversation whose folder is not the selected project, is not recorded.
    An observation whose project has no usable records-store attachment
    waits and is recorded once it has one.

27. **Refresh fleet records** rebuilds the file-based coordination workspace
    for each undertaking: the selected graph, outstanding returns and review
    ownership, recorded integration, selected work and waiting causes. It reads
    the fixed `.chirality/fleet/` folder and writes nothing. Agents and the
    person continue to author the source records with their file tools.
    New `current_graph` selectors use `graphContent.method` =
    `chirality.app.exact-bytes.sha256/v1` and `graphContent.value` = the
    lowercase SHA-256 hex digest of the exact graph file bytes; no prefix or
    JSON normalization. Prototype TEST VALUE selectors remain unsupported.
    Missing, changed or duplicate selections never fall back to an older graph.
    Inputs are contained Fleet-relative files; connector needs are interpreted
    from their declared receiving records with claim/route gaps shown. Decision
    needs remain unknown without their required evidence. A dispatch is
    tied by what its own record says: the work item and undertaking the
    referenced brief named when the dispatch was recorded. Nothing in the
    project's files is consulted to tie anything, so a brief file changed,
    replaced or superseded afterwards moves no worker. An item so held, with
    no return recorded, reads `dispatched` and lists every worker dispatched
    for it, each with its last recorded status, when it was recorded and
    that nothing has been recorded since; it reads `unknown` once an end of
    every such worker's observation is recorded, or where its named brief
    cannot be found. A dispatch under an earlier brief of the item still
    holds it and says so. A worker still observed for work that is not
    selected in the current graph leaves no row plainly ready. A child tied to no brief
    leaves no item plainly ready while it is observed. An incomplete source packet cannot produce unqualified readiness
    or an apparently complete empty queue. The complete source packet remains
    available beside the derived views.

## Modules

| Module | Contribution |
|---|---|
| `src-tauri/src/hosting.rs`, `process_group_custody.rs` | Source-owned process groups, exact/unavailable original-group census; HOSTING/ACCESS lifecycle, generation, request correlation, ordered native journal, development verification and network disclosure; reviewed 0.160.0 protocol resources in `resources/supplier/` |
| `src-tauri/src/hosting_startup_refusal_tests.rs` | Actual Host startup EOF settlement, never-ready frames, first/restarted source and Stop/replacement races; opt-in cached stock startup control/refusal without login or model calls |
| `native_requests.rs`, `recovery.rs`, `native_items.rs`, `access.rs` | Typed native request custody, pointer ledger, scoped live/ended activity and reported account/destination observations |
| `src-tauri/src/recovery_store.rs`, `recovery_store_tests.rs` | The pointer ledger's SQLite store (DEL-01-02 §7): append-only triggers, one transaction per batch, synced commits, the held current entries' indexed query, the once-only JSON Lines import; tests include the flat cost from 1,000 to 100,000 rows |
| `role_supply.rs`, `runtime_session.rs`, `resources/instructions/` | Reviewed v4 defaults, fixed composition bytes, seeding and generation-bound receiving/startup; supplier/model adoption remains a separate warrant |
| `child_roles.rs`, `access_provider.rs`, `hosting_child_roles.rs`, `native_child_guidance.rs` | Conservative native-name/currentness observation, immutable full child TOML publication, private guarded additive starts and original live child association; unknown origins and unmatched children stay qualified |
| `catalog.rs`, `proposal.rs`, `external_adapter.rs`, `receiving.rs`, `external_observation.rs` | Reviewed receiving contracts and exact person-selected observation custody; no external host dispatch or origin verification implied |
| `src-tauri/src/schema_validation.rs`, `schemas/` | W-1 plus complete package/offer/capture checks; declared-ID registry with external retrieval disabled |
| `src-tauri/src/records.rs` | Validated append, UUID identities, sequence/read completeness, serialization and ordered capture late-write accounting |
| `src-tauri/src/records_index.rs`, `records_query.rs`, `records_index_tests.rs` | RS §13.8 derived SQLite query cache: disk-backed identities and positions, streamed rebuilding, authoritative line revalidation, and source-scan fallback; cache metadata is disposable |
| `src-tauri/src/record_lines.rs`, `record_lines_tests.rs` | RS §13.8 lines: one entry or one group per line (read whole or not at all), each line's chain link to the one before, unchained (legacy) and broken-chain limits, and each log's chain head |
| `src-tauri/src/records_access.rs`, `records_access_tests.rs`, `records_continuity.rs`, `records_continuity_tests.rs`, `resources/runtime_core/records-read-log.entry.schema.json` | The agents' read-only records capability (RS §13.9): the offered tool, its storage-independent source (the logs R-1 discovers: the project's records store subtree, or §13.7 logs before an import), bounded quoted pages and the read log written before each answer; tests include a fake-peer journey in which the agent calls it |
| `src-tauri/src/records_store.rs`, `records_store_lines.rs`, `records_store_witness.rs`, `records_store_tests.rs`, `records_store_lines_tests.rs`, `records_store_witness_tests.rs`, `records_store_publication_tests.rs` | The App's records store (RS §13.8): coordinated first identity publication across App processes, placement and the explicit override, project identity and its limits, the explicit import of §13.7 records with the store's witness of it, the appender and shared reading of the store's own line files, and the host status `recordsStore` |
| `src/RecordsStorePanel.tsx` | The records store panel: the store's placement, the project's identity with the acts that resolve a link fault, export, package import and recovery, retention, legal hold and disposal |
| `src-tauri/src/records_export.rs`, `records_export_tests.rs`, `tools/verify_records_bag.py` | RS §13.8 BagIt export: native folder selection, byte-preserving payload and prior administration snapshot, SHA-256 manifests and copied-log chain heads; package verification in the App and a standalone Python verifier |
| `src-tauri/src/records_retention.rs`, `records_retention_tests.rs`, `resources/runtime_core/records-administration.entry.schema.json` | Native close/reopen, legal hold/release and recorded disposal after verified export; surviving administrative evidence, stable write admission and activity leases, truthful partial-failure recovery |
| `src-tauri/src/storage.rs` | Store, project/run/writer and library paths, R-1 discovery (store subtree, or §13.7 paths in place before an import), atomic capture persistence and locking |
| `src-tauri/src/recorder.rs` | Package byte snapshot and request/provenance-limit mapping |
| `src-tauri/src/act_control.rs`, `act_control_a15.rs`, `act_control_file.rs`, `file_act_native.rs`, `canonical.rs` | A16, hot A15 and App-file offer/native custody; capture versus publication uncertainty, ordered retry and original content binding |
| `file_act_root.rs`, `file_act_view.rs`, `src/FileActPanel.tsx` | Original file-offer ownership, separate read-only act/decline comparison and per-offer controls; no cold native-origin upgrade |
| `src-tauri/src/decision_view.rs`, `act_policy.rs`, `standing.rs` | Decision projection, A16 method-aware standing and provenance limits; recorded claims do not establish native act admission |
| `attachments.rs`, `hosting::attachment_custody`, `resources/attachments/` | Native-selected immutable ordered text sources, durable metadata/client pointers before scoped send, and explicit native outcome limits |
| `src/App.tsx`, `tests/attachment-outcome.test.mjs`, `src-tauri/src/attachment_outcome_tests.rs` | Ordered-attachment Send/Steer outcomes reach the composer separately from subsequent view-read failures; actual owned-list, write and source-correlation packets supply the mounted consumer checks |
| `trace_receiving.rs`, `record_relations.rs` | Independent unverified trace imports and general record correction claims; neither verifies native origin |
| `native_history.rs`, `role_lifecycle.rs` | Read-only native history, scoped Continue receiving and immutable original guidance bindings |
| `role_observations.rs`, `role_record_source.rs`, `role_observations_tests.rs`, `role_observations_host_tests.rs`, `role_r3_run_tests.rs`, `src/ConversationRoles.tsx` | App start/fork supply observations, exact retained App guidance and historical limits; private confirmed receipts supply role R3 references at run opening, with immutable source-qualified run context and explicit quoted cold inspection; cold claims restore no role/CCE authority |
| `connector_standing.rs`, `connector_route_store.rs`, `connector_route_view.rs`, `src/ConnectorRoutePanel.tsx` | Provider-independent standing, caller-account persistence (in the project's records store subtree; earlier in-project accounts read in place until imported) and read-only inspection; saved claims do not verify source truth or actor duties |
| `src/RequestCards.tsx` | Readable DEL-01-04 request cards, source-qualified read-only navigation to received item anchors and the waiting-request indicator; answer values come unchanged from the host's register |
| `src-tauri/src/native_waiting.rs`, `src/NativeWaitingBridge.tsx` | macOS native waiting-menu metadata, immutable original-source targets and single-use navigation handoff; no supplier response or restored request authority |
| `src-tauri/src/codex_stop.rs`, `src/CodexControls.tsx` | Stop/Restart Codex (DEL-01-02 §4.1 C-12 with the DEL-01-04 §5.2 question): live-work assessment with runs in force, ask-first sequence, the ledger `codex_stop` record, interrupts before the stop within the stop wait limit, TO-4 labels and the in-process outcome panel |
| `src-tauri/src/app_quit.rs` | App quit asked first (DEL-01-02 DEF-6, K-4, SQ-Q; DEL-01-04 §5.2): assessment across homes, `quit_requested`/`quit_answered`, quit interrupts (cause *quit*), the exit's process stops and `session_ended` (AS-09, AS-10); the DEF-1 exit rule; the C-24 waiting count |
| `src-tauri/src/stop_records.rs`, `resources/runtime_core/recovery.stop-request.schema.json` | REC stop-request records (DEL-01-02 §3.4 SR-01…SR-12): validated transitions and outcome labels, the `codex_stop` ledger entry, and the read-back after a relaunch; the Host writes them through its recovery writer before each interrupt send |
| `src-tauri/src/hosting_recovery_reads.rs`, `execution_custody.rs` | Recovery after a restart (DEL-01-02 §3.2 CV-11…CV-15, CV-19, CV-22; SR-09): the reads on the home's ready process, `observation_lost`/`observation_recovered`/`turn_outcome`, and the conversations' recovery states in the ledger; run on the host's trial tick or on the person's retry |
| `src-tauri/src/checkpoint_recorder.rs` | EXEC §2.4 first slice: CE-1 listing, CE-3 arrivals from observed AW-6/AW-7 native items, CE-11/CE-12, CE-17 waiting arrivals; written through the run's RS writer with CE-19 late-write limits; never reacts (RC-4) |
| `src-tauri/src/model_turn_recorder.rs` | RS R5 `model_turn` entries (HOSTING §8.3): thread-scope reports and one entry per run turn, effective only from a `model/rerouted` naming the turn; observes `native_items.rs`'s `modelReroutes` and the host's thread rows; never reacts |
| `src-tauri/src/run_restart.rs`, `run_restart_tests.rs` | EXEC §2.7 / RECOVERY §4.1: the REC run tag at `run_opened` (owner `DEL-02-03`) and the host's startup writer of RS "App-restart interruption" limits; tests also cover WR TX-5 / SQ-END end notices after relaunch and (j) permanent refusals |
| `src-tauri/src/run_offers.rs`, `src/RunOffers.tsx` | Exact run-offer line forms (WR §16.5 PR/FN), the finished-report proof for a *completed* end, and their presentation beneath the message |
| `src-tauri/src/workflow_proposal_advisory.rs` | Shared read-only CK-1 evaluation of the chat's closed selected revision and a verified offered candidate before the ordinary choice; existing source/selection or proposal correspondence is rechecked at the press |
| `src-tauri/src/workflow_library_entries.rs`, `src/LibraryEntries.tsx` | Explicit opened-library entry observations and ordered picks for the existing in-place review; host-held source/content correspondence, named refusal limits and no registration or selection authority from presence |
| `src/WorkflowRegistrationReview.tsx` | Read-only presentation of the existing frozen registration review before and during native A15 confirmation, with literal workflow text, reported metadata and unchanged digest input |
| `src/App.tsx`, `tests/workflow-action-result.test.mjs`, `src-tauri/src/workflow_action_result_tests.rs` | Workflow command responses remain distinct from later observation failures; actual draft-copy output reaches the mounted consumer and its once-only original-context draft observation |
| `src-tauri/src/workflow_drafts.rs`, `src/WorkflowDrafts.tsx` | DEL-02-02 draft workspace in the Rust host (SQ-D D-2…D-4 observation, hygiene, §5.1 states) and its list presentation in NIR §7 words, with the two Try buttons and each draft's trial list; nothing here registers, reviews or runs |
| `src-tauri/src/workflow_trials.rs`, `workflow_package_copy.rs`, `workflow_workspace.rs` (`compose_run_text`, `TrialText`, `files_folder`), `runtime_session.rs` (`WorkflowRun`) | DEL-02-02 trial core (WR §17 steps 1–4): one composer for run texts and trial texts (TT-3), TX-7's files-line folder with content-addressed supply copies rechecked before unattempted run dispatch, TT-8 trial snapshots, and the create-once TT-4 trial links and observations |
| `src-tauri/src/trial_flows.rs`, `workflow_trial_transcript.rs`, `src/TrialComposer.tsx` | DEL-02-02 trial flows (WR §17 steps 5–8): pre-filled delegated and clean trials sent only by the person, separate hot authoring and trial-source references, source-bound Try again/feedback defaults, links on acknowledgment, TT-9 linking and fidelity reads, bring-back transcripts, Compare, TT-2's run refusal and offer silencing, the review's last clean trial line; the composers in the conversation view |
| `src-tauri/src/workflow_trial_source.rs`, `workflow_trial_restart_tests.rs`, `tests/clean-trial-restart.test.mjs` | WR TT-9–TT-11 clean-trial source continuity after restart: a separate pointer from the original positive native acknowledgment, guarded current link/REC correspondence and explicit read/feedback through the original source; older links and delegated child sources remain unavailable without their own evidence |
| `src-tauri/src/historical_run_learning.rs`, `workflow_learning_pointers.rs`, `historical_trial_flows_tests.rs` | WR TT-10/11 historical Bring back and Compare: strict original WR/RS correspondence, pointer-only original native ACK coordinates in owned REC tags, separate current source and target homes, quoted activity and exact revision bytes without restored live run/supply/selection authority; unavailable source/history remains named |
| `src-tauri/src/file_act_lapse.rs`, `file_act_view.rs`, `src/FileActPanel.tsx` | Explicit standing A4/A6/A7 file-content observations in existing RS act logs, original-source-bound metadata retry and separate current comparison/resolved history/limited claims |
| `src-tauri/src/file_act_arrival.rs`, `file_act_root.rs`, `act_control_file.rs`, `src/RunPanel.tsx` | Explicit live App-file arrival entry through the original run/declaration/source, frozen file preview, native confirmation and original run-log capture continuation; historical-only and unsupported contexts remain unavailable |
| `src-tauri/src/host_tick.rs` | The host's own ticks (OI-008): a record tick receives native frames and records checkpoint observations, and a separate trial tick makes due trial reads, whether or not the interface polls; each tick is guarded and a failure is shown in `host_status`, which only reads |
| `src/RunPanel.tsx` | Run panel and selected-workflow view (NIR §9 PD-1…PD-7): readable declared part, checkpoints as guidance with their recorded listing and arrivals, the run-record write notice, output standing facets from the record only (AS §8), readable advisory compatibility |
| `src-tauri/src/conversation_roles.rs`, `src/ConversationRoles.tsx`, `src/App.tsx` | Source-bound navigation of admitted same-role Forks, Continue as ‹role› handoffs and same-role Fork through the Host (NIR §5.8, ROLE §3.3), the role limit account (ROLE §6.2), the readable start display, role header and guidance-changed flag (ROLE §4.4) |
| `src-tauri/src/conversation_handoff_send.rs`, `src-tauri/src/hosting_handoff_send.rs` | Original Continue-as send custody and read-only outcome observation; full-source attempt/write/response facts remain separate from view refresh, with the ordinary pending end-notice route preserved |
| `src/NativeActivity.tsx`, `src/PlanMode.tsx` | Readable per-thread native activity from the `native_items.rs` view (DEL-01-03 plans/tools/delegation with the DEL-01-04 message part) and the experimental plan-mode element |
| `src/NativeHistory.tsx`, `src/App.tsx`, `tests/native-history.test.mjs` | Source-bound readable stored turn summaries and the selected item page, shared native item bodies with retained raw source, and accepted-query paging regressions; reading and explicit Continue remain separate |
| `src-tauri/src/runtime_session.rs`, `host_tick.rs`, `hosting_manual_history_tests.rs` (`history_bridge` tests) | Person-directed history reaches native activity once through its original accepted query and current source; rejected pages leave the activity projection and counters unchanged, with raw receipts and limits retained |
| `src-tauri/src/lib.rs`, `src/App.tsx` | Native command boundary and presentation; the webview cannot confirm a capture itself |

## Offline build and checks

Packaged product instructions are the App-authored documents in
`src-tauri/resources/instructions/`; that directory is their one copy.
`python3 -m unittest tools.test_instruction_resources`, run from the repository
root, checks the eight-file payload and the retained four-role binding; CI
enforces it without a sibling Library.

Use Rust 1.97.1, Node 24, Python 3 and prepared Cargo/npm caches. Set
`CARGO_HOME` to the dependency cache you prepared if it is isolated. The offline
commands require those caches to contain the locked dependencies; use the
[developer start](#developer-start) to prepare dependencies when downloads are
authorized.

```sh
npm install --offline --no-audit --no-fund --ignore-scripts
npm run build
(cd src-tauri && cargo build --offline --locked)
```

From `app/`, set the supplier path to run the real offline handshake:

```sh
export CHIRALITY_CODEX_BIN=<stock codex 0.160.0 vendor binary>
export CHIRALITY_CODEX_EXPECTED_SHA256=112fae7a5a1223e673c8a1791d32338f37df8b527ff1159bb8adac6c4dbf1b4b
npm test
(cd src-tauri && cargo test --offline --locked)
```

The Rust tests share process-wide state (the configured records store,
environment variables and other statics) and do not pass on parallel libtest
threads. `app/.cargo/config.toml` therefore sets `RUST_TEST_THREADS=1` for cargo
run from `app/` or `app/src-tauri/`; an explicit `RUST_TEST_THREADS` or
`--test-threads` still wins. Cargo reads that file from the working directory,
so run cargo from those folders rather than from the repository root.

The JavaScript tests that run Rust fixtures through `cargo test --lib` first
build the lib test target once under a separate limit
(`tests/support/rust-prebuild.mjs`), so their fixture time limits do not
include a cold compile.

CI also runs six presentation tests that the `npm test` list does not yet name.
`app/package.json` is digest-pinned by the notice basis
(`packaging/notices/index.json` and `transitive-index.json`), so adding them to
its scripts needs a notice-basis reconciliation. Run them directly:

```sh
node --test tests/run-journey.test.mjs tests/make-journey.test.mjs \
  tests/journey-navigation.test.mjs tests/model-choice.test.mjs \
  tests/trial-continue-model-choice.test.mjs tests/ordinary-send-hold.test.mjs
```

The focused `node --test tests/file-act-panel.test.mjs` check runs offline Rust
file-act fixtures with `CHIRALITY_SKIP_CODEX=1` and consumes their actual cold
history and pending-save DTOs. `CHIRALITY_FILE_ACT_LAPSE_DTO_LOG` may point to
stdout from a completed passing run of those fixtures to reuse that evidence.

Use the complete published platform package, with its `bin/codex` entrypoint,
helper binaries, resources and `codex-package.json` retained in their original
layout. Include the package's `codex-path` directory in the child process's
`PATH`. With only `codex` copied, the stock supplier warns that Code Mode lacks
its required host and will fail closed. The approved 0.160.0 archive's complete layout was separately
verified and probed; earlier flat-binary observations remain source-specific.
This development setup does not establish qualified distribution identity.

On macOS, the opt-in startup refusal check uses the cached stock binary above,
fresh `mktemp -d` file-auth homes and a localhost-only OS sandbox. It compares
a supported initialize with a configuration refused before initialize, for
first start and restart. It sends no login, thread or model call:

```sh
(cd src-tauri && cargo test --offline --locked --lib \
  startup_refusal_stock_config_control_and_first_start_restart_refusal \
  -- --ignored --test-threads=1)
```

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

The opt-in local-auth supplier check uses the same identified binary and fresh
isolated homes. It supplies only an invented generated canary, captures exact
Bearer correspondence at a loopback HTTP400 fixture hot and after restart,
and checks the anonymous route, logout persistence and native ChatGPT-only
policy refusal. It makes no prediction or real-key validation. Redacted
evidence stays in the reported scratch directory; the owned auth leaf is
removed even on failure and Native stderr is discarded before transfer.
Authenticated local App access remains unoffered. From `app/`:

```sh
python3 supplier_checks/test_local_auth.py
python3 supplier_checks/local_auth.py --codex "$CHIRALITY_CODEX_BIN"
```

The macOS-only [linked configuration write contract](src-tauri/tests/config_write_contract.rs)
is ignored by default, including ordinary full-suite runs. It calls the actual
`OwnedHomePlan` seam and stock 0.160.0 stdio RPC using only invented providers.
Before running, receive a **new owned, physical, private `/private/tmp` stock
input root** from the input owner: complete vendor layout, the authenticated
134311083-byte archive, and `input-binding.json` with the handed-off SHA256.
The binding supplies root path/device/inode, `nativeBinary` and `archive`
path/inode/size/SHA256, and the input owner's retained `vendorTree` warrant.
The fixture validates the bound root and stock file identities/hashes; it reuses
the full-vendor/provenance warrant without another archive inventory or download.
An absent flag/input fails explicitly before supplier lookup or home creation.

Use a new private build home and target, copying only an approved prepared
Cargo registry into its new `cargo-home/registry`; never share a writable cache
or target or use a personal Codex home. With `CONTRACT_BUILD_ROOT` naming that
prepared physical directory and its empty `os-home`, `codex-home`, `tmp` and
`target` children, run from `app/`:

```sh
env -i PATH="$RUST_1971_BIN:/usr/bin:/bin:/usr/sbin:/sbin" \
  HOME="$CONTRACT_BUILD_ROOT/os-home" CODEX_HOME="$CONTRACT_BUILD_ROOT/codex-home" \
  TMPDIR="$CONTRACT_BUILD_ROOT/tmp" CARGO_HOME="$CONTRACT_BUILD_ROOT/cargo-home" \
  CARGO_TARGET_DIR="$CONTRACT_BUILD_ROOT/target" CARGO_NET_OFFLINE=true \
  CHIRALITY_SKIP_CODEX=1 \
  CHIRALITY_CONFIG_WRITE_CONTRACT=stock-0.160-invented-only \
  CHIRALITY_CONFIG_WRITE_INPUT="$NEW_STOCK_ROOT" \
  CHIRALITY_CONFIG_WRITE_BINDING_SHA256="$HANDED_OFF_BINDING_SHA256" \
  cargo test --offline --locked --manifest-path src-tauri/Cargo.toml \
    --test config_write_contract stock_linked_config_write_contract \
    -- --ignored --exact --nocapture --test-threads=1
```

For offline compilation only, use the same private environment, omit the three
`CHIRALITY_CONFIG_WRITE_*` input/opt-in assignments, and replace the test-name
and following arguments with `--no-run`. This compiles only the selected
integration fixture and its library dependency. Optional
`CHIRALITY_CONFIG_WRITE_CASES=endpoint` or `remaining` selects a bounded subset;
the default is `all`, and unselected cases establish no result.

Every case uses a fresh root with fresh HOME/CODEX_HOME/TMPDIR/cwd/XDG locations
and a cleared child environment with only those locations, fixed system PATH
and `LC_ALL=C`. `sandbox-exec` denies all network, child creation, `/Users`
reads and writes outside that case; unsupported isolation stops without fallback.
Only initialize/initialized, config/read and one versioned, explicit-target
config/batchWrite per case are sent; no account, model, thread, listener or App
is used. Unknown outcomes are inspected without replay. EOF and bounded cleanup
retain the original process-group identity until reaping. All raw exchanges,
diagnostics and effects stay in the reported private root: automatic native
notifications can include OS metadata. Public failure text is fixed.

The observations cover an endpoint edit, a real stale version, a controlled CLI
override, one invalid-value diagnostic and a quoted dotted provider ID. The
receiving link survived successful writes, while the target inode was replaced;
current desktop/shared identity checks therefore still need a receiving
continuation before a product writer can depend on this result (ACCESS F-A3,
U-R3). The supplier cases also populated the fresh linked skills directory;
the observation does not establish when within the case that happened. These
are isolated native contract effects, not App/person configuration acts,
loaded-thread reload behavior, account/server or start-up traffic qualification,
an implemented privacy guarantee, acceptance or release.

The separate ignored `stock_linked_provider_creation_contract` uses the same
immutable input guard and fresh private build/case isolation. It adds its own
opt-in flag, so enabling the original five-case entry alone does not enable
creation. With a newly prepared `CONTRACT_BUILD_ROOT` as above, run from `app/`:

```sh
env -i PATH="$RUST_1971_BIN:/usr/bin:/bin:/usr/sbin:/sbin" \
  HOME="$CONTRACT_BUILD_ROOT/os-home" CODEX_HOME="$CONTRACT_BUILD_ROOT/codex-home" \
  TMPDIR="$CONTRACT_BUILD_ROOT/tmp" CARGO_HOME="$CONTRACT_BUILD_ROOT/cargo-home" \
  CARGO_TARGET_DIR="$CONTRACT_BUILD_ROOT/target" CARGO_NET_OFFLINE=true \
  CHIRALITY_SKIP_CODEX=1 \
  CHIRALITY_PROVIDER_CREATION_CONTRACT=stock-0.160-invented-only \
  CHIRALITY_CONFIG_WRITE_CONTRACT=stock-0.160-invented-only \
  CHIRALITY_CONFIG_WRITE_INPUT="$NEW_STOCK_ROOT" \
  CHIRALITY_CONFIG_WRITE_BINDING_SHA256="$HANDED_OFF_BINDING_SHA256" \
  cargo test --offline --locked --manifest-path src-tauri/Cargo.toml \
    --test config_write_contract stock_linked_provider_creation_contract \
    -- --ignored --exact --nocapture --test-threads=1
```

`CHIRALITY_PROVIDER_CREATION_CASES` defaults to `all` (four fresh cases, one
write each). `positive`, `remaining`, or `existing-and-malformed` selects only
those cases; unselected cases establish no result. No case retries a write.
Missing opt-in/input fails before supplier lookup or case-home creation.
Compilation alone uses the earlier `--no-run` route without the opt-in/input
assignments. The original five-case entry is not run by this invocation.

The actual absent-ID case created the single quoted dotted ID with the exact
four-field definition in the user layer and supplier defaults in the effective
row. The real stale-version control preserved an external same-ID insertion;
the existing-ID fresh-version control accepted replacement, demonstrating no
create-only protection in this operation. The malformed-object control was
refused with independently unchanged file/link/reread state. Successful writes
preserved the receiving link but replaced the target inode; target mode was
preserved. The absent case retained its preexisting byte prefix/comments with
a table appended, without establishing general byte preservation. Raw versions,
paths, diagnostics and notifications remain private. These observations neither
implement Add nor establish person intent, App source admission, writer
provenance, arbitrary-writer exclusion, filesystem CAS, an atomic target/profile
commit or qualification. Current Q-8/F-A3 receiving limits still apply.

`npm test` validates actual Rust outputs against canonical Design schemas,
without reference rewrites. Rust tests also check runtime refusal, capture
failure/recovery, ordering, namespace and provenance negatives. With no supplier
binary, set `CHIRALITY_SKIP_CODEX=1` explicitly for Rust checks; the Node hosting
check then reports its skip. Skipped checks establish no supplier result.

Two library tests keep the same rule (`pinned_codex_observations`): they start
the pinned supplier through the host in invented folders below the system
temporary folder, in a fresh home nobody has signed in to, and fail without
`CHIRALITY_CODEX_BIN` unless the skip is set. One starts it with the development
model address set (below) and reads the setting back from the supplier's own
configuration reading; it runs no turn, so it shows that the supplier starts
with the setting, not where a model request goes. The other shows how far the
supplier's search for a `.codex/config.toml` above its working folder goes: not
at all where no folder above holds a `.git` entry, and up to the folder that
holds one where one does. They run in the hosted product job and nightly, not
in a pull request's own checks.

The handshake uses its own unique system-temp home, a local provider at
127.0.0.1 port 9, plugins off and analytics off. It starts no model turn, supplies
no credential, and checks its sampled process-group sockets. Test-owned scratch
files are cleaned after consumers finish.

## Recorded ST-5 and NV-04 seam replay

The offline recorded peer and actual Host/recovery tests exercise preserved redacted supplier traffic against current App source,
including unknown acknowledgment after process loss and a delegated child
outliving its parent. This is development verification; the existing C1 EXP
records remain capture-only and no candidate qualification is claimed.

## Supplier intake and recordings at a pin

A pin advance is deliberate (DEL-01-01 REQ-006). One of its steps is a maintained
tool, `supplier_checks/intake.py`, run from `app/`. It does not sign in, use a
model or read a person's Codex home, and fetching a release archive is not among
its acts (a download needs the owner's permission naming the file, source and
size).

A pin is a key of the table `PINS` in `intake.py`, which holds, for each pin
that has a consumer today, the release archive's address, size, SHA-256 and
source commit. The tool accepts no other pin and builds no path from a caller's
text; adding a pin is a reviewed change to that table.

`intake.py --archive <file> --pin <pin> --out <new directory>` checks the
archive's size and SHA-256 against the table, extracts regular files and
directories only, writes the distribution record (`CANONICAL_DISTRIBUTION.json`),
compares the tree with it, runs the supplier's schema generators and writes the
manifest, the two compiled bundles and `GENERATION.json`. A refusal at any point
removes the output directory.

What the generator is given is six variables (HOME, CODEX_HOME and TMPDIR in a
fresh scratch directory, PATH, LANG and TZ=UTC). Before each execution the tool
refuses when configuration from outside the fresh homes could reach the
supplier: a `.git` or `.codex` entry in any ancestor of the scratch working
directory, the system folder `/etc/codex`, or a managed preference the supplier
reads. Each is checked by presence alone; a check that cannot be made refuses,
and the generation record names the checks made. These are controls on what the
supplier is given, not a sandbox: they do not stop supplier code opening a file
by an absolute path. The generator's sockets are sampled while it runs, which is
not network isolation.

This is an operator-run tool on stable inputs. It is built so that a check that
was not made or that failed cannot come out as a distribution record or a
generated basis. It is not built to withstand a writer changing the inputs
during the run, nor someone with write access forging a record.

Recorded exchanges at a pin are kept as evidence under
`supplier_checks/recordings/<pin>/`, with a note beside them saying how they
were made and what the files do and do not establish. The harness that made
them is not maintained; `supplier_checks/test_recordings.py` checks what the
files themselves establish. Neither a recording nor a generated basis is
qualification of the pin (DEL-01-01 AC-011).

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
arguments, supported rules and remaining M1/M2/M3 work.

Examination source pins are generated. After a reviewed change to a pinned
source, run `python3 app/examination/repin.py` from the repository root and
commit the re-derived profiles and `app/examination/pins.lock.json`; CI runs
`--check` and fails when pins and sources disagree. See
[Source pins](examination/README.md#source-pins). The current Group B graph
is `execution/_Coordination/WorkGraphs/APP-V4-GROUP-B-20261008/WORK_GRAPH.md`
relative to the project.

## Run the development App

An owner-use debug bundle can obtain explicit inputs through **Desktop setup**
when no startup environment inputs are present. Choose the three shared
config.toml, AGENTS.md and skills references (an absolute absent-target path is
allowed), explicitly choose a project or **No project**, and explicitly select
the bundled unqualified development supplier. **Review setup effects** shows
the new App-owned account directory, links and private request path under the
actual resolved Tauri App-data root. **Prepare home and save for next launch**
opens the native question and performs create-only preparation; it imports no
credentials and adopts no existing home. Missing/broken resources remain shown
without a silent configuration fallback; dependent persistence features can be
unavailable.

The saved request is pending only. Quit normally when ready and launch again;
saving does not quit/restart or change the active project, home, account/model
choices, recovery, attachments or prepared text. A fresh launch revalidates the
requested sources and takes nonblocking, process-held App-data/profile/home
inode leases before operational consumers bind. A missing/invalid request,
replacement, overlap or custody conflict returns to setup without operational
Root data. These leases coordinate participating App binders, not arbitrary
third-party clients. Setup persists only nonsecret native references and the
explicit unqualified supplier selection in private bounded atomic storage.
It never saves credentials, model/provider choices, trust or a claimed lease.
The exact bundled supplier path and standing are shown; matching label,
generated reference and binary bytes do not authenticate or qualify it.

The existing environment route below remains complete and exclusive. Any
startup supplier/home/project/key/shared/development input selects it, even if
incomplete or invalid; there is no fallback or field merge from saved desktop
requests. A compiled production successor continues to refuse without its
installed-custody issuer, regardless of a desktop development selection.

One App at a time holds an App data directory and each Codex home it starts
Codex on, on this route as on the saved one. Each hold is an exclusive `flock`
on the directory itself; a conflicting lock shows that some process holds it,
not which one, so the refusals say what was observed and name no owner. An App
whose App data is held by another process starts nothing operational (no Codex,
no recovery ledger, no record) and shows "Chirality did not start here: its
data is held by another process on this computer"; a start of Codex on a home
held by another process is refused, and so is a home that does not exist. A
home this App still holds because a Codex process it started has not been
confirmed ended refuses a later start in the same App and says so; quitting
Chirality releases it. If App data cannot be resolved or held (an invalid
`CHIRALITY_APP_DATA`, an unavailable platform path), nothing operational starts
and the reason is shown. Every committed configuration uses the identifier
`dev.chirality.app-v4.skeleton`, so development runs that do not name their
App data share one directory and only the first of them starts. To run in
parallel, give each run its own `CHIRALITY_APP_DATA` (an absolute path; it is
created if missing, and setting it alone selects this route) and its own
existing `CHIRALITY_CODEX_HOME`.

When the App data hold is taken. On the environment route, at launch, after
the App data directory is created if missing. On the saved route, at launch
only if the App data directory already exists; with no directory the App sits
at setup with no hold and takes it when setup is first saved, which creates
the directory. Two Apps on a never-used machine can therefore both show setup;
the second to save is refused.

How an earlier App session is read. A later session start reads an earlier
session without a recorded end as ended only when this process holds the App
data directory that contains the ledger (established by device and inode, not
by path text) and that session is not alive in this process. A session's
liveness lock file can only ever say that it is still running (a held lock
refuses the start); a free, missing or replaced lock file says nothing, and a
crashed session's lock file is never what its ending rests on: it is removed
only after that session's end is recorded. Otherwise the start is refused,
nothing is written, and it is shown as a recovery limit. Limit: an App of a
build before this hold, started on the environment route, takes no lock of any
kind and cannot be excluded or detected; while it runs on the same App data, a
later App can hold that App data and read its session as ended.

What that reading says of live work. Where a conversation's turn was live when
the earlier session last recorded it, the custody view carries a restart fact
(`app_restart_interruption`) with standing `App-recorded`, the turn under
`liveTurnsLastRecorded`, and `liveAtSessionEnd` `not-known`: it is the record
as that session left it, not an observation of its end, and the turn may have
ended after the last record. Only where the App itself recorded at its own quit
that it lost sight of the live turn does the fact say `recorded-at-quit`. The
run-limit record the host writes from that fact says the same: what was last
recorded, that the end was not observed, and that no end of the run is
inferred. Records written before this change keep what they say.

What that reading says of stop requests. After this App session has
successfully started on the ledger and established the earlier sessions'
endings, startup closes an earlier session's unsettled stop request (SR-08)
only when that source session has a start record in the ledger. The view of stop outcomes follows the same rule: for a request of
a session with no start record it shows the record as recorded, derives no
label, does not call the session earlier or ended, and says as a limit that the
session's end is not established. An outcome-unknown record is read as "No
final turn status is recorded for this stop request. That does not establish
that Codex's process ended.", whichever way it came to be written.

What that reading records. A request the earlier session left listed is closed
in the ledger as `open-at-app-session-end` (RECOVERY RQ-06, context
`app-ended-without-record`), and the custody view shows it as the event
`request_open_at_app_session_end` with standing `App-recorded`: the App records
that its own earlier session ended while the request was recorded open. It is
not an observation. It asserts no Codex process exit and no missing reply; a
Codex the earlier session started may still be alive, and a reply sent after
the last record was not observed. Rows an earlier build wrote
(`ended-unanswered(process-exit)`) stay as written and keep their kind. The
custody-event schema is 0.3; 0.2 is retained beside it.

The home check before Codex starts compares the home's path with the held
directory by device and inode immediately before the label probe and again
before the app-server is spawned. A window remains between the last check and
the child's exec, because the child is handed the home by path (`CODEX_HOME`):
a directory put in place of the home inside that window is not detected.

The process lock of a home. Every start of Codex, for every home, first takes
an exclusive, non-waiting `flock` on one small private file the App keeps in
the home, `chirality-codex-process.lock` (created at the home's first start,
opened by name inside the held directory, never through a link). The Codex
child is given that one descriptor and the App closes its own copy as soon as
the child is spawned, so the lock is held by the Codex process, and by any
program it passed the descriptor to, for as long as each keeps it open, and by
nothing of the App. This is what excludes a second Codex on a home after an
App is killed (its Codex can outlive it: the supplier's app-server exits by
itself up to about 45 seconds after its input closes) and after a Stop that did
not end the process. A held lock refuses the start before it is an attempt: no
lifecycle record, the state unchanged, the reason kept as the host status's
`lastStartRefusal`, and no retry by the App; Start can be pressed again. What
the refusal says is what the App knows. Where this App started a Codex process
on the home and has not confirmed it ended, it says so with its census of that
process's group as just taken; otherwise it says only that a Codex process
started earlier, or a program it started, may hold the lock, and that the App
cannot tell which program it is. A lock that cannot be tried (a link in its
place, a file not private to the user, any other failure) refuses and never
reads as free. Limits. Taking the lock shows that nothing still holds it. It
does not show that every program Codex started has ended: a program that was
passed the descriptor can close it and keep running, and a process Codex
started without it never held it. At the pinned supplier version
the commands of a turn and local MCP servers are started with other descriptors
closed (best-effort on the supplier's side), so they do not hold the lock and a
free lock does not show they have ended; hooks and the notifier program of the
person's own Codex settings are started with Codex's descriptors, so one of
those left running keeps the home from being started on until it lets go of
the lock or ends. That the supplier itself keeps the descriptor for as long as
it runs is an assumption about the supplier: the hosted handshake test
observes the real supplier holding the lock while it is ready, and nothing
more. The App's census and settlement of the process groups it
started are unchanged and are what Quit and the home hold rest on, and they are
a second condition on a start, beside the lock: a Host starts no further Codex
on a home while a process group it started there is not established settled
(its leader's exit observed and its group known empty), whatever the lock says,
and none while the lock is held, whatever the Host believes. "There" is the
directory, by device and inode, recorded for each process when it is started:
the same home named through another spelling or a link is the same home, and a
process with no recorded home counts for every home. A process that was
created but whose exit reservation was already lost (another reaper had taken
its leader) is kept too, as one that can never be established settled: the
start fails as a failed spawn (its record says the process was created and
custody of it was lost), and for the life of that App process nothing further
is started on that home and the menu quit is withheld. For that state, and for
a reservation lost at any later observation, the person reads: "Chirality
cannot establish whether a Codex process group it started has ended. Retrying
Quit cannot resolve this in the current App session. You can end Chirality
using macOS Force Quit, but that does not establish that Codex or its
descendants have ended." A settlement that was only unavailable this time keeps
its earlier sentence. Force Quit can end the App without its end being
recorded, and a later start on that home is still answered by the home's lock. A start refused on
the first ground alone, the lock being free, is told that this App is still
holding the home for a Codex process not confirmed ended. A build
before this lock takes none and is not excluded by it. The lock is the file:
if the lock file is removed or replaced in the home while a Codex holds it, a
later start makes and takes a new file and is not excluded by that earlier
process. A Stop that cancels a start before anything is spawned releases that
start's lock at once.

Relaunch. The holds and the process lock have no wait and no retry, and
process exit is the reliable final release. A deliberate relaunch by the App itself would have to
start its successor after the predecessor has exited, or after an explicit,
proven release of each hold; a successor started first is refused at once.
The predecessor's exit releases its own holds only: a Codex it started that
still holds a home's process lock keeps a start on that home refused after it.
Tests construct their state in their own scratch folders and need neither.
`CHIRALITY_APP_DATA` is read only by a development run (`tauri dev`), as
`CHIRALITY_RECORDS_STORE` is; a built App does not read it, so it cannot point
an installed App at other data. It moves the App's own data only. The system
web view keeps its website data, caches and application support in folders
named for the build's bundle identifier within the launch's home. Set both
`CFFIXED_USER_HOME` and `HOME` to the same throwaway folder for a development
launch (the App does not set them): two runs of one build under different
throwaway homes then do not share web view storage. Without both set (`HOME`
alone redirects none of it), they share it under `~/Library`.

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

A configuration file does not decide where a development launch's model
requests go: the stand-in provider above applies only where a conversation
uses it, the first-use route writes its own configuration, and the App can
rewrite one while it runs. A conversation on the built-in provider is
addressed to the supplier's real service, signed in or not: the API address,
or with a ChatGPT sign-in the ChatGPT service address.

So a launch that is not the owner's sitting also sets
`CHIRALITY_DEV_OPENAI_BASE_URL` to a same-machine address, for example
`http://127.0.0.1:9/v1` (nothing listens there) or a loopback stub's address.
A development build passes it to the account home's Codex at every start as
the command-line setting `openai_base_url`, which outranks the person's and
the project's configuration files and replaces either default address. A
system managed configuration or managed preference outranks it, so such a home
is not started while either is present. The rule for the value: at most
2048 bytes; `http://` or `https://`; then `127.0.0.1` or `[::1]` written
literally (no name is accepted, `localhost` included, so nothing is resolved);
an optional port from 1 to 65535 without leading zeroes; and an optional path
containing only ASCII letters, digits and `._~/-`. No user or password part,
query or fragment. With any other value Codex is not started. Loopback restricts where the request goes; it does not make
whatever listens there trusted. The release configuration (built with
`distribution-successor`, and not a development run) never consults the input.
The dedicated local home never carries the setting; its provider has its own
address.

The input is for scratch homes nobody has signed in to, because a stand-in
that listens there may record what it receives. A home whose Codex would
carry the setting is not started while it holds a sign-in file (looked at by
name only); sign-in is refused in it; and the separate key home is not
prepared at all. Two things the App does not detect: a sign-in kept in the
login keychain instead of the file, and a sign-in file put there from outside
the App after its last check (if that happens between App start-up and the
first start, Codex is not started and the reason shows only when the person
starts it). The launch helper's home kind is the first hold: a home
made for the owner's sitting never carries the input.

The setting replaces the built-in provider's address for model requests, and
for the model list unless a model catalogue address is configured
(`model_providers.openai.model_catalog_url`, which it does not replace).
Nothing else: the sign-in, token, plugin, connector and analytics addresses
are separate. As far as the supplier's source shows, a home with no sign-in
does not ask for the model list at all and lists the catalogue bundled with
Codex; where a request is made and fails, Codex logs the failure and still
lists the bundled catalogue. For those, such a launch also sets the proxy
variables to a loopback port where nothing listens and exempts loopback, as
the examination launch helper does: `HTTPS_PROXY`, `HTTP_PROXY`, `ALL_PROXY`
and their lower-case forms to `http://127.0.0.1:9`, and `NO_PROXY` and
`no_proxy` to `127.0.0.1,localhost,::1`. The supplier's own HTTP and websocket
clients honour these by default. Not covered: a home whose configuration turns
on the supplier's system proxy feature, clients the supplier builds for direct
routing, redirects, anything Codex itself starts, the web view's helper
processes, and the system. So a launch made this way has had the built-in
provider's address replaced and some other clients obstructed; it has not been
held to this machine. What it shows is behaviour against a local substitute,
which does not qualify the account route to the real service.

Copy the maintained `tests/fixtures/FX-DP1/project/decisions` files into the
scratch workspace's `project/decisions/`, then run `npx --offline tauri dev`.
For the offline thread exercise, enter model `skeleton-no-model` and provider
`skeleton_local` explicitly. These are test choices, not product defaults.
Open a package, choose an alternative and confirm its full native text.
Authenticated/live model work remains coordinated with the owner.

A launch writes the system web view's data and caches, and the App's own data
unless redirected, under the home's `Library` in folders named for the build's
bundle identifier, whatever `HOME` alone is set to. Setting `CFFIXED_USER_HOME`
together with `HOME` to one throwaway folder redirects them;
[`examination/standalone/launch.py`](examination/standalone/launch.py) does that
for an identified development build. Agents do not remove those folders from
the owner's Library.

For stored history, choose **Read stored conversations**, then select a received
conversation. **Read metadata**, **Read turns**, **Read goal**, and per-turn item
controls read disposable native pages; opaque page cursors belong to their
received stream. Turn summaries distinguish `summary`, `notLoaded`, full and
empty items. **Read items for this turn** displays that received page readably,
with unchanged native item/page JSON in expandable details. Next/Previous use
that accepted page's turn, cursor and direction. While a new read is pending or
unavailable, retained raw evidence stays inspectable and prior readable rows and
page buttons are withheld. Reading does not supply live status or reconstruct
earlier checklist updates. **Continue selected conversation** separately requests native
resume before permitting operational text input, requesting `excludeTurns:true`
instead of deprecated full-history hydration. Its confirmed admission can finish opening on a later successful source
read when the immediate refresh fails or has not yet shown its row. A newer
conversation choice, Start intent, home/source change or stored-history
operation supersedes that pending navigation; an unknown result never opens a
conversation merely because a later read lists it. Its admitted conversation
then loads the bounded prior-work context described in item 11. A failed context page
has an explicit retry that reads history without another resume or send. It keeps the conversation’s
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
record of the project's roots governs. A link that is missing or unreadable,
that names another identity or another store than the store records for the
folder, that is a duplicate, or that belongs to a moved project attaches
nothing until the person restores the link, adopts the project or gives the
folder a new identity; the host status names which of those acts apply, and
the panel offers those. While an attachment is refused the project's records
are unavailable: one decision (`readable_home` in `records_store.rs`) says
where a project's records are read from, in the store or in the project
folder; it gives no location for a refused attachment, so files kept in the
project folder are not read in the place of records the store holds, and
status says nothing is read in place and asks for no import. Ordinary readers
take the place from that decision and writers from `write_dir`, with one
exception: the fleet reader (`fleet_records.rs`) must create nothing, so it
keeps association checks of its own and builds the protected folder only
after them; with the link removed or changed it reads no protected payload
and gives the cause. This is held by name and by a limited test, not by
construction: the test fails when selected source lines change (the lines
that name a records location in the project folder, and, outside the store
module, the lines that name one of nine of the store's path-returning
functions by its `records_store::` path or that begin with `use` and name
the store). It does not enforce the arrangement and is not a complete list
of who can obtain a location: among what it does not see are an import
spread over several lines, a file brought into the store module other than
by a path attribute in its usual spelling, a re-export or a new function of
the store, and an unchanged listed line whose argument now comes from
somewhere else; its comment lists them. Review and the behavioural tests
establish the permitted use, and making those functions private is later
work. One case stands
apart, unchanged: with no records store available at all and no link in the
folder, connector route accounts are read in place and nothing is written,
while ordinary records in that state are unavailable. A link naming a project whose records the store keeps
with no folder recorded for it (an adoption that stopped part way) reads as
"records kept, not attached", admits no Codex and is not registered on the
link alone; the person adopts it. Restoring the link reads no record, so it
stays possible when a disposal stands; finishing a disposal is offered only
once the folder is attached again, and finishing an interrupted package
import only where its folder and project file agree with the import's own
record. As containment, adopting a project or giving a folder a new identity
is refused while a record of an identity concerned is being read or written
or while that identity's activity is held (a running Codex, an open run, a
capture or a record waiting to be written), in this or another App window.
Present limits: that containment is not a binding of store and project across
an operation, and a writer that reaches the records by the project's path
after the act, with nothing holding the project's activity, is not covered; a
workflow record reader kept from before can be given a replacement folder at
the same path carrying a copied link; a connector account reader does not hold
the retention read admission, so payload put back from outside after a
disposal can be read again; and restoring the link of a folder with an
interrupted package import writes the App's link bytes, not those the import
recorded, so that import cannot then be finished from the App. When the last
line of the store's registry of project folders (`roots.jsonl`) is
incomplete, every attachment and the status say so and its bytes are kept;
records are read from what its complete lines record, and nothing is
written, minted, adopted or restored for any project. The App's only way out
of that state today is finishing an interrupted package import whose frozen
registry bytes begin with exactly the bytes found: the import completes a
tail that is byte for byte a prefix of those frozen bytes. The App cannot
tell whose interrupted write left such bytes; the result is exactly the line
the import would have written from a clean file, and another act that left
them never reported success and its line was never in force. Any other
incomplete line can only be resolved by hand, outside the App. Records an
earlier App wrote at the §13.7 paths
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
store inside the project or a Codex home is refused. The store's own line
files (`roots.jsonl`, the registry of project folders; each project's
`imports.jsonl`; and `legacy-imports.jsonl`, the store's witness of legacy
imports, written before any copy and kept outside every project's subtree)
are appended so that an append never changes the meaning of earlier bytes
(`src-tauri/src/records_store_lines.rs`): a new file is put in place whole,
and a fragment left by an interrupted append is closed with the byte 0x1E,
which no JSON line contains, and named by a
`chirality.records-store.unread-line` line before the next append or at
startup; its bytes are kept and never read. A complete line that cannot be
read and does not end in that mark is never set aside, by the writer or by a
naming line written for it, and a naming line in any form but the one the
App writes names nothing: either leaves the file not read whole, so that
reading continues, the limit is shown, nothing more is appended to it, and
the App does not repair it. A package import writes its registry lines as one
frozen write of its own; while that write is pending, every other registry
write is refused with the registry unchanged, another package import's
included, and if whether one is pending cannot be established (a journal
that cannot be examined) the write is refused too. The witness begins with a
store this build creates (or, in an older store, at the first startup,
registration or import) and is backfilled once from each readable account.
Its first line lists the store folder key of every project present when it
began, taken from the store's project folders and its registry; if they
cannot be listed whole the witness does not begin and the act that would
have begun it is refused. That list records which projects predate the
witness, and no time is compared. A witness line says an import was begun,
not that anything was copied. The witness is written by this build and
read by nothing that decides: its reader answers only that a legacy import
is established, from a witness line read whole and wholly formed or from
the project's account, or that it is not; it never concludes "no import",
since the absence of a line is not evidence that none was begun. Its
answer establishes the imports it lists, not an exhaustive history and not
an authenticated origin (the store's files are unsigned). Nothing in the App
reads it yet (the decision view does not consult it on this build), so exit
criterion 5 is not served by it until that view does.

The store is created (its folder and `store.json`) when the App starts, and
otherwise only by the acts that write for the person: attaching a project with
a newly minted identity, the imports and the identity acts. A read creates
no store, no folder, no lock file and no control, and repairs nothing (a
reader does take a shared lock on a control that already exists, which is
what keeps a disposal out while it reads): with no store, or a folder at the store's path that
holds no identity, every reader says the store is not created yet and nothing
is written there, elsewhere or in a temporary folder. Once opened, a process
stays bound to the store's physical folder and identity file (their device and
inode): a redirected alias is not followed, and a folder put at the store's
path in its place, even holding a copy of `store.json`, is refused by readers
and writers alike. So is a `store.json` replaced while the App runs, even with
the same bytes (a restore from a backup, for example): nothing is read or
written through it until the App is reopened, which opens the store afresh. Readers take only an admission control that already exists;
records with no control beside them read as unavailable with that reason
(development note: a store written by a development build from before
admission controls existed holds records with no control beside them, so its
role and workflow history reads as unavailable until the App next writes to
that project, which makes the control; no release wrote such a store). The
records capability's own read-log write is admitted through the control that
exists and is refused, with the read, when it is missing. A control that is
not a regular, singly linked file is refused without waiting. A store whose
state cannot be read reads as unavailable, never as empty or as "no records
yet": a project's import account is read whole, and nothing is concluded
from one that is not. An account that exists and yields no import line (an
empty file, or one holding only closed fragments and the lines that name
them), a partial last line or a closed line not yet named, a blank line, bytes outside a line's one JSON object, bytes that are
not UTF-8, a key given twice, a line that is not an object of the import
format and version with an import identity, an unknown event, a member no
form of import line has, a member the reader takes in a form it is not taken
as, or a census, files or conflicts list with an entry lacking what the
reader takes from it, each make the account unknown, and unknown is an error
in every reader that takes the account through the store's own reading (where
records are read from, write admission, import, coverage, notes, status and
export admission), never "no import" and never "the store holds records"; the
fleet view does not consult the account, and a workflow record handle kept
from an earlier read does not ask again. Only an account that is not there is
"no import". A fragment an interrupted append left, closed with the mark and
named by the store's appender, is left out with its naming line, as the
store's shared reading leaves it out; every other line is held to these
rules. No evidence beside an existing account, the witness of legacy
imports included, is taken to show that nothing was begun: the store's
appender makes a new account whole and later appends keep the lines before
them, so no supported path needs an existing account with no import line to
read as "no import"; a historical or damaged account needs recovery, which
reading it as "no import" would not give. And the witness reads a project's
account through the same reading: an account that exists and cannot be read
is an error there too, never "no account evidence"; and it concludes "no
import" only from a witness read in full, every line of it wholly formed
and naming a project. The reader checks every member of a line that it takes, for the
form it takes it as (the format, the version, the import identity, the event,
`storeHeld`, a started line's `at`, and the three lists), and checks no
member of a line that it does not take (`root`, `method`, `resumes`,
`censusChanged`, and `at` on a completed line), accepting a line that lacks
them. An entry of a census, files or conflicts list is held to its entry form
whole (`original`, `copy`, `sha256` and `bytes`; a conflict's `original` and
`reason`), although nothing after the reader reads a census entry's `copy` or
`bytes` or a file entry's `bytes`. This does not establish that a line is one
the App wrote: the store's files are unsigned, so a well-formed line added to
the account from outside the App reads as the App's own, a completed line
after an interrupted import included, and an export of such a project
verifies. Nor does it establish that lines once there are still there: an
account cut back at the end of a line reads as the shorter account, so a
later interrupted import whose started line is cut away reads as no
unfinished import, and an export verifies. Like an added line, that is a
change made to an unsigned file from outside the App; the App's own
interrupted append leaves a partial line or none and never removes one.
Signing does not by itself close it: a signed export of a cut account
authenticates the cut, and signed lines still allow a suffix to be removed.
Closing it needs trusted, retained evidence of the expected history, covering
the started line and checked before export, which the signing work has to
establish. An export of such an account that verifies says that the package's
present bytes agree with its manifests and heads, not that a preceding import
completed or that no history was removed.
Verification of a package says its bytes agree with its manifests and chain
heads, not that the import behind them completed. The store's appender makes
a new file whole or not at all, so the App leaves no empty account of its
own. The capability's read-log write makes only its own folder beneath
parents that exist. A read writes
only two things below an existing store: the records read log that the
agents' records capability writes for each call (`reads/records-reads.jsonl`),
and the derived query cache described below. The host status (`recordsStore`)

shows the store, the project's identity and any import or identity limit.
The records-store panel offers **Export project records**, choosing a parent
folder natively and creating a new verified BagIt package. Its payload preserves
project store files byte for byte, with SHA-256 manifests and each copied RS
log's chain head. Store-wide query caches and the two known owning lock controls are omitted;
imported connector publication evidence is preserved.
**Verify an exported package** checks inventories, hashes and RS heads again.
The included `verify.py`, with standard Python 3 and without the App, checks
bytes and inventories.
A package faithfully exported from a store whose chain was already
broken is not refused: its bytes are consistent, and the log's integrity is
limited at the line the package records, which the App's full statement
names with its log and line and which stays reported by the store's reader
after import. For a package whose chain-head
tag is of profile 0.3 its checks are three: the manifests and inventory; that
each chained log's exact length and SHA-256 equal the ones the tag records
for it; and each chain recomputed from the lines and compared with the
recorded head, line count and breaks. Then it lists limits under three
labels: FOUND by this verifier (a break in a recomputed chain that the
package records too; an unclosed final part of a log), STATED by the package
and not checked here (a line the package's account says the App set aside; a
role supply log the package says the App could not read), and NOT CHECKED (a
chain it did not recompute). It ends with exit status 0 when every check it
makes passed and no limit is listed, 2 when every check passed and at least
one limit is listed, and 1 when a check failed. Exit status 0 means exactly
that; it does not mean the records are intact, because `verify.py` does not
hold the record format and does not check the package's account.

Three things are kept apart, in the tag, in what either checker says and
here, and none stands for another: equal bytes say that an exported log is
the log that was exported; whether its records are intact is the chain
recomputation and, in the App, the reading of every line with the record
format; and nothing in a verification says whether a record may be disposed
of.

The chain-head tag `records-chain-heads.json` is written in profile 0.3
(`formatVersion` "0.3"; a package format addition decided by App Agent 0,
2026-11-12). Each log's head, as before, records the SHA-256 of its last
counted line, the lines counted, whether lines carry links, the lines written
before chaining began, and each place the chain was broken (the words of one
kind of break differ from those an earlier build wrote; see the earlier
profiles, below). Profile 0.3 adds,
for every chained log whose file the App could read when it wrote the tag,
`bytes` and `sha256`, the exact length and SHA-256 of the log file as
exported, also for a role supply log the App could not take; and for every
chained log the App took: `setAside`, the numbers (from 1) of the lines the
App counted in the chain without reading them as records; `torn`, the numbers
of the lines the App closed and set aside (not counted); and `unclosedEnd`,
the length of an unclosed final part or null.

What holds for a profile 0.3 package: a package altered in any chained log,
with the tag not changed to agree, fails verification in both checkers,
whether or not its manifests were regenerated. `verify.py` compares each
log's bytes with the tag before it makes anything of the lines. The App's
verification recomputes the whole tag from the payload, with the record
format, and compares it with the recorded one, which includes those members;
so it also refuses a package whose account differs from what its reader
finds. That equality, and not the chain's links, is what binds every byte:
the App does not examine the link of a line it sets aside, so the links alone
do not tie the lines before such a line to the recorded head. The package is
unsigned: someone who rewrites a log, the tag and the manifests together is
not detected (LIM-007).

Packages of profiles 0.1 and 0.2 record neither a log's bytes nor an account
of its lines. The App reads them as before, except that one whose log has a
break at a line no read line precedes, exported by a build before this
change, no longer verifies in the App, because the App compares the recorded
break's words with the ones it now writes. The App reports a line it sets
aside as a limit for a package of any profile, since it recomputes the
account from the payload. `verify.py` checks only the manifests and inventory of such a
package, lists every chain as NOT CHECKED; it
does not follow their chains, so for them a changed log with regenerated
manifests is shown only by the App. No release exported those profiles.

Where the App states a limit on log integrity (at verification, import,
repair and disposal) it gives the number of limits and each one as its
reader found it, or marked NOT CHECKED, and says nothing of when or why a
limit arose. The bounded summary in a native confirmation gives the number
only and says each is named in full in the App: it reads no limit's text, so
nothing a path or a line's content spells can be taken for a log or a line. Disposal may rely on an export
that carries a limited log: the native disposal question says so as its own
statement, and the disposal act records it in its `export` member as
`logIntegrity` (state "no chain recorded broken" or "limited", with each log
and line); an act recorded before that member existed reads as "not stated".
Exports are unsigned until App
signing: the verification compares a package with its own manifests and
recorded heads, so a package whose records, manifests and heads were replaced
together still verifies, and it confers no source authenticity. New packages include a protected
`records-administration.json` tag, reversibly retaining each prior administrative
event's exact UTF-8 bytes and its project identity. Legacy packages without it
have unknown retention history and cannot satisfy disposal prerequisites.
New export folders and files are owner-only from creation (0700/0600),
including staging and intermediate payload folders. Verification changes no
existing package permissions.

**Import verified package** selects the incoming bag natively and confirms its
project, destination, exact package identity and retained administrative state.
The selected folder must already have a readable link naming that project;
resolve a missing link explicitly before importing. This supports another
store's original project identity and restoration of missing files, without
overwriting unequal files, merging divergent logs or minting a new identity.
Valid newer local administrative history, holds and closure survive. Disposed
identities and conflicting or unknown history refuse import. Legacy bags with
no administrative snapshot remain verification-only evidence.

An interrupted import blocks ordinary project reads and recording. **Finish
package import** continues its original durable intent and retained private
package, including exact partial copies and association publications; it asks
for no replacement source and performs no second import act. Conflicting
recovery evidence stays held, and private stages remain available for recovery.
Source packages and originals remain unchanged. Imported content is unsigned
quoted evidence: native relationships, capture replay and capability authority
are not restored. Later local Fleet recording remains usable, with origin
checks keeping the imported prefix separate (RS §13.8).

**Restore project from package** handles a missing project link or an unused
startup identity after loss. Its native question names the original identity,
physical folder, store and any unused identity released from that folder.
Existing records and restrictions refuse displacement. The unused identity's
subtree stays unchanged. Recovery remains discoverable if a link or locator is
lost before publication finishes; queued writers retain their original identity
and cannot follow the folder into a different project's records.

**Repair package controls** is offered only when native evidence identifies a
recoverable original operation. It reconstructs exact missing derivatives and,
when needed, asks for the exact original bag to restore private custody. Valid
later local appends and administrative history remain. Conflicting controls or
a missing original native intent stay held. Disposal's legitimate removal of
the payload receipt does not require recreating that receipt. Moving the same
physical store folder preserves completed native history without rewriting its
original recorded paths. See RS §13.8 for the proof and recovery limits.

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

The fleet coordination log (DEL-06-01) is one co-written file in the project,
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
them. An edited, removed or unlinked line after the chain started, with the
links of the lines after it left as written, is a broken chain at the first
line whose link no longer agrees with the line before it: the log is
incomplete and nothing repairs it. The chain links alone do not show a change
to the content of a log's last line that keeps its own backward link, lines
removed from a log's end, an edit after which the later links were
recomputed, or the removal of every link of a log this process has not read
chained. Showing those needs comparison with a trusted head kept from before
the alteration, which the App does not keep while log checkpoints are
unsigned; the head an export package records shows such a change only against
that package. The host status
(`recordChain`) shows bounded counts of chained, legacy and broken logs;
each log's chain head comes on demand (`records_chain_heads`).
Signed checkpoints wait for App signing (OI-011).

The derived records index keeps identities, positions and membership counts in
process-owned SQLite files under the store's `indexes/`; record bodies stay in
their logs. Cold use rebuilds from authoritative sources, and returned entries
are reread and revalidated, including their exact line hash. Changed or unusable
caches rebuild or use source scans. The cache is the one stated exception to a
read writing nothing: a read may write it under `indexes/` of a store that
already exists and that the process has bound, never into a folder put in the
store's place, and never in a temporary folder (SQLite's own temporary
structures stay in memory). The decision view does not use it. Where the cache
cannot be written the sources are read directly and the chain report says so.
The cache is dispensable: deleting `indexes/` at any time changes no answer,
only how fast it comes.
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
deferred. Current code refuses unverified act replay while preserving evidence. Workflow reuse separately applies the person's workflow approval policy (WR §4.6/RC-2; owner decisions A/B/C, 2026-11-09). "Allow disk records" admits fresh LS-1 disk consistency; "Require verified approval" admits a keychain-sealed A15 bound to its record, complete identity and committed ledger line, or a present in-process A15. Records keep the requested policy apart from the evidence applied. The policy persists across launches: in the App's settings file until keychain protection is set up (an agent able to write that file could change it), then in the keychain. Lowering needs native confirmation, and a keychain or verification failure never lowers it. "Protect registered workflows with your keychain" is unavailable on unsigned and development builds.
Native authenticity, real process-kill/fsync failure witnesses, native witnesses of paged recovery and continued prior-work access (the custody reads in item 22b remain metadata/turn summaries; item 11 adds a separate bounded prior-work context), cold role-source reconciliation, native GUI child-role journeys, native A15/registered-library and file-act witnesses, and remaining policy/standing/control journeys remain in the Group A graph. Per-home configuration/resource linking is implemented with observed ownership limits. CommonMark parsing and one closed, explicitly development-candidate workflow catalog are supplied; the production native-page supply path and hot registration transaction are implemented, while their actual native consumer witnesses remain separate. Eligible hot live single-App-file arrivals now join the frozen file-act preview and native confirmation through an explicit person action. General output/attachment contextual shortcuts and historical-only arrival entry remain separate. Standing A4/A6/A7 App-file acts now have explicit durable lapse observations and separate current/history displays, while complete native file-act witnesses remain separate. External dispatch and host qualification remain unsupplied. Native text-turn and interrupt controls use the selected native thread and
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
items), or output records. The independent ended-run observer records eligible
later App-file acts (CE-16) and per-referent lapse of already performed single
App-file A4/A6/A7 checkpoints (CE-10/CE-18), with current source checks and
explicit pending/late-write limits. An output gated by a checkpoint shows that checkpoint's recorded act
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

Conversation roles (item 24) keep handoffs in process memory. Confirmed App
role-supply observations and content-addressed App instruction bytes are kept
in the current project's records store under `role-supply/observations.jsonl`
and `role-supply/content/`. An actual workflow run records role-guidance R3 by
reference to the original supply, limit account and run context. Pending or
unavailable publication stays qualified; cold source reading quotes historical
file evidence and restores no current role or CCE authority. Native child-role
preparation, guarded supply, live association and exact quoted child-source
retention are implemented within item 24's observed-origin and generation
limits. Supplier carriage evidence remains source-bound; native GUI journeys,
provider/model adoption and qualification remain separate. Delete or archive
beside Fork waits on U-R13.

The ask-first App quit (item 22a), startup SR-08 write and startup RQ-06
endings are implemented. On 2026-10-20, an owner-authorized native application-menu
Quit was observed on a development bundle using App code `1127b8ce` and stock
Codex 0.160.0. The only loaded conversation was idle, no waiting requests were
displayed, and the composer was empty. The exact App and known supplier processes
were absent in the following census; no signal or forced cleanup was used.
This establishes the bounded idle Quit transition, not the live/unknown-work
question, quit's durable final writes, SR-08 or RQ-06. Those remain unwitnessed natively.
The Restart Codex question
was witnessed natively once, on 2026-10-10, with nothing live: it listed nothing
in force and showed its three buttons with Keep Codex running as the default.
Restart Codex was pressed, and Cancel and Keep Codex running were not. The
Stop Codex question and a stop with live work remain unwitnessed.

A first native App witness was taken on 2026-10-10. It used an improvised
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

It qualifies nothing. That dated witness did not exercise attachments and the
run-end notice, workflow runs and A15, approval cards, delegation beyond that
run, quit, the WebKit/Chromium matrix or a packaged build. It also found that
an interrupted turn's running
command can still complete (see the note), and the bundle gap PKG §4.1 P-2/P-3 (since
fixed: the default configuration declares the instruction and workflow
resources).

Open contract conditions live in each deliverable's scope of work. The PR
describes a repair and its verification. Retain a witness or capture only
while a current requirement, test or ruling uses it, in the code location of
what reads it.

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
