# D-GOV-43 — Codex Host Re-platform: Stock App Server Owned by the App Host

Status: `PROPOSED — AWAITING OWNER RULING` (revision 3)

Decision ID: `D-GOV-43` (verified next free after D-GOV-42 on the preparation basis)

Date: `2026-09-11` (America/Edmonton); revisions 2 and 3 after independent review

Framed by: HELP_HUMAN, Chirality v3 Codex-only MVP trial session, after the
Stage26/R17 native pass and the plan/execute/workflow demonstration recorded in
`projects/chirality-app-dev/execution/_Coordination/AgentRuns/APP_V3_TRIAL_COMPLETION_20260910/R17_FUNCTIONAL_FINDINGS.md`
(findings R17-F1 and R17-F2). Revision 2 incorporated the round-1 review in
`REVIEW_FEEDBACK_R1.md`; revision 3 incorporates the round-2 review in
`REVIEW_FEEDBACK_R2.md`.

Accepted preparation basis: `main@a75adecf13f055c092ffa92809f66e7817c44242`
(PR #766 merge). Prepared on branch `claude/chirality-v3-mvp-trial-ab05cb`.

Supersedes if ruled: D-GOV-20 ruled-architecture items 2, 3 and 4 as they
apply to the App MVP Codex path; D-GOV-36's daemon-owned custody exception and
bootstrap namespace to the extent they presuppose that daemon; the DEL-02-08
byte-for-byte supply pin, the DEL-02-09 root-private Codex home, the DEL-02-10
closed provider-event projection and the DEL-02-11 continuity gate as
requirements on the App MVP path (their register rows are already
`RETIRED — SCA-005`; this ruling confirms the disposition). D-GOV-20 items 1,
5, 6, 7, 8 and 10, D-GOV-35's delegation-class recognition, the Codex
sole-engine rule, K-WRITE-2, K-PROJECT-1, K-STORE-2, K-ROLE-2 and K-EXPORT-1
are preserved with the re-expressions listed in "Surfaces touched".

## Decision requested

Approve or reject re-platforming the Chirality App's Codex integration from a
per-user Runtime daemon that hosts a patched, pinned, event-filtered and
configuration-vetoed Codex App Server behind a Unix socket and an SSE relay,
to a stock, version-pinned OpenAI Codex App Server child owned by the App's
own Electron main process over stdio, speaking the published protocol in
full, with Chirality's conversational interface, roles and reusable workflows
supplied through supported upstream mechanisms, authentication separated from
the user's other Codex clients, and approval and sandbox policy chosen by the
user. The same ruling authorizes, together and as a bounded act, the named
Root, Runtime and App governance changes that remove the daemon's obsolete
requirements, holds and checks. The working target throughout is
plan → execute → save → reuse → iterate.

## Owner direction already recorded

Owner Ryan Tufts, 2026-09-11 (America/Edmonton), in the trial session,
verbatim:

> I approve the second re-platform route. You are right to start with the
> governance, and any impacted deliverable's and their scopes of work may
> need to be revised accordingly too.

The "second re-platform route" was defined in the same session as: the
Electron main process owns a stock `codex app-server` child over one channel
to the renderer; the Next turn route and most of the daemon are dropped; the
App leans on Codex's own persistence for restart. The direction authorizes
preparing this governance packet and the revision of impacted deliverables and
scopes. It is not itself the ruling on this record.

The owner also stated, verbatim, in the same session:

> I need to have the Codex agents in their full glory, so to speak. There
> should not be any limits on tool use or the useful features that come baked
> in to the Codex agents.

and:

> Also, the things built to-date are also, hopefully, useful when we get to
> the local LLM server expansion for Chirality App.

and, relaying the round-1 review:

> Let's iterate to get the best proposal. How do you see this matter now? You
> don't have to adopt everything, it's offered as feedback for your
> consideration.

and, relaying the round-2 review:

> Once more consider the other agent's feedback. Seek any further answers
> from me if needed. Otherwise update your proposal for my direction.

## Findings that motivate the decision

Established from source at the preparation basis and from the upstream
protocol schema at Codex `rust-v0.154.0` (released 2026-09-09):

1. The Runtime daemon accepts eight Codex notification methods and
   quarantines every other item type. Command executions, file changes, MCP
   tool calls, web searches, reasoning, sub-agent items, token usage and rate
   limits never reach the App. Tool work therefore produces no stream bytes,
   the client's default 30 s socket idle timeout destroys the turn stream, and
   the daemon's close handler interrupts the turn (R17-F2). The App's Activity
   Actions view is empty by construction.
2. The daemon refuses to run unless the effective Codex configuration has
   empty `mcp_servers`, `hooks`, `plugins`, `profiles` and `notify`, plugin and
   shell-snapshot features off, approval policy pinned to `never` (or
   `on-request` only for a patched network-ask posture), and a sandbox matching
   an exact table. Codex runs in an App-private home, so the user's own
   configuration, MCP servers, skills and instructions are excluded.
3. The pinned App Server 0.149.0 "supplier" is patched with private protocol
   extensions (`chiralityAdmissionAuthority` on `initialize`,
   `account/identitySnapshot`, a `chiralityRuntime` carrier, a non-schema
   `permissions` thread parameter). None exist in the upstream schema. Upstream
   is five releases ahead; every release requires re-patching and
   re-qualification. The Runtime README records shell canaries still failing
   under the sandbox diagnostics for the accepted payload.
4. The App front end translates Codex into a generic multi-engine harness
   vocabulary retained from the Claude SDK and Pi eras; Codex-native items have
   no rendering target.
5. Turn transport is daemon to Unix socket to SSE to a Next API route to the
   browser, with three independent timeouts and no keepalive, re-deriving state
   that Codex persists in its own thread store. Model and reasoning are frozen
   per chat by the App although Codex accepts them per turn.
6. The upstream protocol already carries what the App needs: 101 client
   methods including `thread/start|resume|fork|list|read|compact/start`,
   `turn/start|interrupt|steer`, `model/list`, `config/read`, `skills/list`,
   `mcpServerStatus/list`, `account/login/start|logout|read|rateLimits/read`,
   `review/start`, `permissionProfile/list`; 82 server notifications including
   `item/started|completed`, `item/agentMessage/delta`, `item/reasoning/*`,
   `item/commandExecution/outputDelta`, `item/fileChange/*`,
   `item/mcpToolCall/progress`, `item/plan/delta`, `turn/plan/updated`,
   `thread/tokenUsage/updated`, `thread/compacted`; and ten server requests
   including `item/commandExecution/requestApproval`,
   `item/fileChange/requestApproval`, `item/permissions/requestApproval`,
   `item/tool/requestUserInput`, `item/tool/call` (dynamic tools) and
   `mcpServer/elicitation/request`. Thread start and resume accept
   `developerInstructions` and `baseInstructions`. Codex persists threads
   under the Codex home. The exported schema omits experimental fields; in
   particular `TurnStartParams` carries no `collaborationMode`, although the
   field is accepted at runtime under `experimentalApi` and is what Plan Mode
   uses today.
7. An open-source Electron client of the same protocol (T3 Code, MIT)
   demonstrates a schema-generated TypeScript client with augmented
   experimental fields, stdio launch with pass-through of user config
   arguments, a Codex home layout that shares configuration and sessions while
   keeping `auth.json` private per client, inline approvals and thread resume.
   Pi (MIT) is a complete harness with its own agent loop and is not a Codex
   client; it informs UX only.

## Proposed ruling

1. **Hosting.** The Chirality App hosts a stock OpenAI Codex App Server
   (`codex app-server` from the official `@openai/codex` distribution) as a
   child process owned by the App's Electron main process, speaking the
   published JSON-RPC v2 protocol over stdio. The App pins the exact Codex
   version in its package manifest and lockfile and updates the pin routinely
   with re-validation. Upstream drift is a dependency update, not a stop
   condition. No patched, forked or privately extended supplier is used; the
   private protocol extensions in finding 3 are retired. Ordinary software
   integrity is retained: lockfile-pinned dependencies, the App bundle's code
   signing and notarization covering the bundled binary, and the security
   checks a desktop application normally carries. No runtime admission,
   supplier certification, payload hashing or identity binding is re-created
   under any name.
2. **Faithful transport.** The App forwards the complete App Server
   notification and server-request stream to its renderer over one
   long-lived channel (Electron IPC through the preload bridge with validated
   message shapes, `contextIsolation` on, no credential material in the
   renderer), with no notification whitelist, quarantine, projection to a
   closed generic event schema, or client-side idle timeout that terminates a
   turn. Notifications and server requests are treated differently. A
   familiar notification gets a purpose-built card; an unfamiliar notification
   is rendered for generic inspection and kept in the event log, never
   dropped. Every server request receives a response: familiar requests
   (command, file-change and permission approvals, user input, dynamic tool
   calls, MCP elicitation) through their cards or the user's recorded policy;
   an unfamiliar request receives an explicit JSON-RPC error response and a
   visible "unsupported request" outcome in the transcript. No request is
   left unanswered, so Codex never waits indefinitely, and a generic card
   never implies approval.
3. **Chirality's effective Codex home with separated authentication.** The
   App runs Codex against a Chirality-owned effective home that shares the
   user's configuration and resources by reference (config, skills, plugins,
   MCP definitions, instruction caches and the sessions store) and keeps
   authentication private (`auth.json` and the models cache). This is
   authentication separation, not filesystem or account-data isolation:
   configuration, skills, MCP servers and threads are the user's, and threads
   written by Chirality are ordinary Codex threads. Chirality never copies
   credentials to populate the overlay; the user signs into Chirality through
   Codex's own flow. The actual credential backend (file versus OS keyring) is
   verified so that signing into or out of Chirality does not sign another
   Codex client in or out; if a backend cannot separate, the App reports it
   and does not silently share. Separation is the only mode implemented and
   verified for the MVP; a direct shared-authentication opt-in is deferred.
   There is no effective-configuration veto.
4. **Chosen policy.** Approval policy and sandbox mode are the user's choice
   per project with per-turn override, taken from Codex's own options
   (approval `untrusted`, `on-request`, `on-failure`, `never`; sandbox
   `read-only`, `workspace-write`, `danger-full-access`; network per the
   user's Codex configuration). The recommended new-project default is
   `on-request` with `workspace-write`. Full access is available by explicit
   user choice. The composer shows the active policy; evidence records it.
   Chirality `permissionMode` maps onto these settings and grants nothing by
   itself.
5. **Continuity from Codex.** Thread persistence, resume, fork, list,
   compaction, token usage and rate limits come from the App Server. The App
   keeps its own chat index and metadata (titles, roles, plan revisions,
   workflow selections, evidence pointers) keyed by Codex thread ID in
   operational user-data state; the sidebar shows the App's index, not every
   thread in the shared store. App relaunch resumes threads through
   `thread/resume`; the daemon's restart-admission mechanism is retired.
   Daemon-era trial chats and their evidence are preserved unchanged in
   place. If the App's existing session reader renders them without new
   work, they remain viewable; otherwise they are retained as an accessible
   archive. No history-import feature is a release prerequisite, and
   continuation of those chats as Codex threads is not promised.
6. **Authentication.** Sign-in and sign-out use Codex's own
   `account/login/start`, `account/login/cancel` and `account/logout` within
   the Chirality effective home, with credentials custodied by Codex as
   upstream designs. The App never reads, copies or relays credential
   material. This replaces D-GOV-36's daemon-owned custody exception and
   bootstrap namespace on the App path.
7. **Daemon retirement.** The per-user Runtime daemon, its LaunchAgent, Unix
   control socket, client tokens, accepted supervisor-socket design, hosted
   admission and identity binding, packaged-basis hashing, native admission
   addon and the SSE-over-Next turn route are retired from the App MVP path,
   together with the requirements, holds and checks that governed them
   (item 11). K-RUNTIME-1's exclusive-owner language transfers to the App
   host process for its own App Server child. No network-exposed control
   listener is introduced.
8. **Instructions.** Upstream base instructions and tool behaviour are
   preserved. The active Chirality role and any selected workflow context are
   supplied through supported additive mechanisms: `developerInstructions` at
   thread start and resume, additive turn input for a selection made
   mid-conversation, and project `AGENTS.md` discovery for project
   instructions. Delegated work (Codex native sub-agents configured through
   the upstream `[agents]` table) receives the intended role instructions,
   and the spike demonstrates it.
9. **Evidence.** Chirality evidence (AgentRuns, plan revisions, workflow
   selections, actual model attribution under K-ROLE-2, approvals given and
   the active policy) is recorded by the App from the same event stream into
   checkout-contained project evidence where the governing workflow requires
   it. Codex's session store is operational, non-authoritative state.
   Historical evidence is preserved and is not regenerated to resemble the
   new architecture. Executed checklists, packaging records and prior
   findings are preserved unchanged; the new procedures supersede their
   applicability rather than editing them.
10. **Roles, skills, workflows, Plan Mode.** HELP_HUMAN, HELPS_HUMANS,
    WORKING_ITEMS and TASK remain, supplied per item 8; D-GOV-35's
    recognition of delegated-harness-native descendants stands with its "hard
    outer envelope" re-expressed as the user-chosen policy of item 4. Skill
    availability follows Codex's native discovery (`skills/list` over
    project, user and bundled skills); the App offers read-only, less
    prominent skill inspection with origins, and the bundled-only trust
    restriction on ordinary App skill resolution is superseded. Workflows
    remain Chirality project, user and bundled packages, prominent in the
    UI, created and revised through conversation and supplied as context;
    catalog refresh remains an App function. Native Plan Mode continues
    through `collaborationMode`, carried as an explicitly declared
    experimental-field augmentation of the generated bindings and covered by
    an integration check against the pinned Codex.
11. **Governance simplification is a primary deliverable, under a bounded
    coordinated authority.** This ruling authorizes together the Root
    amendments in "Surfaces touched" and the Runtime and App contract, scope,
    deliverable, hold and notice changes named in `IMPACT.md`. Notices to
    those loops record the application; they do not reopen approval of this
    decision. The authorization is bounded to this decision and does not
    change how unrelated project loops adopt Root changes. The application
    tranche applies a purpose test by family of shared purpose: a family
    whose purpose disappears with the daemon is deleted outright, not renamed,
    re-seated or mapped onto new checks. In particular the nine held release
    bindings are not mapped onto the spike checks, and the Stage 9–13
    twenty-five-step packaging procedure is superseded by a new short
    procedure rather than trimmed. A concise rationale in the tranche and the
    reviewed Git changes are the record of simplification; no register or
    hash table is built to demonstrate it. Retained: ordinary software
    integrity (dependency integrity, application signing, renderer isolation
    and validated IPC, request and session correctness tests). Retired as
    gates: cosmetic whitespace, README self-hash machinery, and repeated test
    execution where one run establishes the fact; a test runs once per
    distinct condition. The human decisions retained are this ruling, the
    owner's native trial and explicit publishing approval. Independent source
    review before the consolidated build is an engineering responsibility,
    not a human approval prompt. Material scope changes and consequential
    findings return to the owner; routine implementation choices do not.
12. **Measure of done.** The functional spike extends the R17 demonstration
    and is complete when, against the pinned stock Codex in a trial project,
    one App instance demonstrates all of:
    - S-1 native Plan Mode with discussion and at least one revision;
    - S-2 execution with real file reads and tool use, including work that
      runs silently longer than the former 30 s stream-silence timeout;
    - S-3 saving a reusable workflow through conversation;
    - S-4 reusing that workflow on another assignment and iterating on it;
    - S-5 one real delegated task whose child demonstrably receives the
      intended role instructions;
    - S-6 quit and relaunch followed by a successful continuation of the same
      chat;
    - S-7 correct interruption and approval handling, including a denied
      approval;
    - S-8 sign-in and sign-out scoped to Chirality, with another Codex client's
      state unchanged.
    Every action is visible in Activity, with no read-free workaround and no
    interrupted turn attributable to transport. The eight checks are an
    acceptance set, not a requirement to build two implementations or to
    rerun every test after packaging. The spike is built on the production
    path. After the consolidated signed build, only the checks that exercise
    a distinct packaged or native condition are repeated: S-6, S-8, and
    verification of the bundle signature and the Codex pin.
13. **Local models deferred; residency requirements retired.** Local-model
    integration is not part of this ruling. When taken up it uses Codex model
    providers (`model_provider`, `[model_providers.<id>]`, `--oss`,
    `oss_provider`), keeping Codex the sole engine. K-RESIDENCY-1, SPEC §14.3
    and the residency types are retired from live contracts with the daemon
    rather than kept as prospective text nothing implements; their history is
    preserved. Useful prior work (the Pi and oMLX validation records and
    provider research) is preserved as reference without release obligations.
14. **Exclusions.** This ruling does not authorize release, publishing,
    acceptance of unknown future bytes, any change to the Codex sole-engine
    rule, any change to Root decomposition workflows, or reliance on the
    retired daemon path.

## Choices folded into the ruling, with the alternative noted

Revision 2 surfaced three choices. The round-2 review supported the
recommendations and revision 3 folds them into the ruling text. The owner may
strike any of them when ruling.

- **Coordinated authority** (item 11): one bounded authorization for the
  named Root, Runtime and App changes, notices as records. Alternative:
  route notices and let each loop re-decide adoption of the same decision.
- **Daemon-era trial chats** (item 5): preserved unchanged, viewable through
  the existing reader if that is straightforward, otherwise an accessible
  archive; no continuation and no import feature as a prerequisite.
  Alternative: migrate their thread records into the shared sessions store.
- **Residency requirements** (item 13): retired with the daemon. Alternative:
  keep K-RESIDENCY-1, SPEC §14.3 and the residency types as prospective text.

## Surfaces touched by the proposed ruling

Ratified Root surfaces to be amended in the coordinated application tranche
(M2/G4):

- `AGENTS.md` — skills paragraph (bundled-only trust), ordinary-context
  sentence, and the Execution and governance section; the exact inactive
  delta is `AGENTS.proposed.patch` (shared configuration and resources,
  Chirality-separated Codex-custodied authentication, additive role
  instructions, every server request answered).
- `docs/CONTRACT.md` §1.13 — re-express K-RUNTIME-1 (App host owns the App
  Server child), K-CONTROL-1 (no network control listener; daemon and
  supervisor sockets retired), retire K-RESIDENCY-1 (item 13), and revise the
  §1.13 closing paragraph and the enforcement-map row "Shared runtime daemon
  and clients".
- `docs/SPEC.md` §14 — replace §14.1 with the App-host App Server child
  description; keep §14.2 project manifests and re-express session storage as
  the shared Codex sessions store plus the App index; retire §14.3 and §14.4
  to history.
- `docs/DIRECTIVE.md` §5 constraint row "No external server requirement" and
  §7 Shared Runtime Direction.
- `docs/TYPES.md` §12 — retire `RuntimeClientCredential`,
  `RuntimeDaemonStatus`, `RuntimeBackend` and the residency types; add
  `CodexHostStatus`, `CodexThreadIndexEntry`, `PolicySelection`,
  `ApprovalRecord`.
- `docs/AGENT_WORKFLOW_RUNTIME.md` — skills paragraphs and the
  `permissionMode` sentence, aligned to items 4, 8 and 10.
- `docs/PLAN.md`, `docs/PRD_ROOT.md` — the D-GOV-20 transcriptions read with
  this amendment; PRD annex by superseding instrument bound to a git SHA.
- `.github/workflows/harness-premerge.yml` and
  `tools/validation/validate_candidate_whitespace.py` — whitespace becomes
  advisory or is removed as a gate (item 11).

Decision records superseded in the stated parts, never edited: D-GOV-20,
D-GOV-36. Decision records read with this ruling: D-GOV-28, D-GOV-35,
D-GOV-37 through D-GOV-42.

Runtime and App loop changes authorized together with the Root amendments
(item 11) are enumerated in `IMPACT.md`; `projects/pec` receives a notice as
a record.

## Application, compatibility, and closure gates

1. Owner ruling on this record (K-AUTH-1).
2. One coordinated application tranche with its own M2/G4 manifest applying
   the Root amendments and the Runtime and App changes named in `IMPACT.md`,
   with the family dispositions and a concise rationale; notices routed as
   records.
3. Functional spike on the production path against item 12, reusing the
   existing conversation, plan pane, workflow, attachment and viewer
   components, with generated bindings and the declared experimental-field
   augmentation. Existing installations and trial evidence are preserved,
   not deleted.
4. Independent source review, as an engineering responsibility, before one
   consolidated signed build; then the distinct packaged and native checks of
   item 12 by the owner's direct tester.
5. The owner's trial, the system-prompt discussion, and explicit publishing
   approval remain separate acts.

## Owner ruling

Not yet recorded.
