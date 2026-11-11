# Embedded agent host

Status: implementation design for RT-E1, 2026-10-28. No live bridge or
supplier/model round trip is established by this document. SWBPIPE owns the
catalog and host; App v4 owns its separate implementation and release evidence.

## Activation basis and portable delivery

On 2026-10-29 the owner directed, verbatim: **“Switch it on. The app should be
built so it will work on other machines too.”** Agent 0 relayed this as lifting
the owner activation gate and accepting the libinfo later-binding residual
recorded in [agent-libinfo-elimination.md](agent-libinfo-elimination.md).
It authorizes implementation and automated qualification while the owner is
AFK; it is not evidence that isolation, cleanup or integration already works.
The pre-exposure cleanup/native-isolation duties below still apply.

The current delivery order is runtime client/dispatcher, webview bridge and
ingress-admitted completion, proposal review, then a minimal functional panel.
Every change remains a proposal for the person's review through the sole
operation engine. Substantial UI/interaction design and App's owner-attended
A/B GUI sessions wait for the owner's return. The Decisions API stays excluded.

[Portable runtime design](embedded-agent-portability.md) governs user-configured
providers and generic keychain custody, the Rust-owned loopback relay, runtime
profile/path derivation, dual-architecture stock supplier packaging, automated
cleanup/isolation proof and explicit unavailability on unqualified platforms.
The unwired launcher now takes an explicit model and a one-shot endpoint from
an observed-ready HTTP relay. [Provider custody](agent-provider-custody.md)
adds the explicit metadata/Keychain core, still without a command or UI;
packaged supplier selection and actual workspace integration remain incomplete.
[HTTP relay design](embedded-agent-relay.md) records its origin/authentication,
TLS, bounds, shutdown and evidence limits. Historical experiment paragraphs
below retain their actual then-current holds; this activation basis supersedes
their pending-owner-authorization status, not their unestablished evidence.

The unwired macOS profile now emits the fixture-qualified exact libinfo lookup
and explicit fork denial. The [permission basis and qualification](agent-libinfo-elimination.md)
records the decision, later-binding review condition, pinned old/new profile
hash guard, C/Rust boundary probes and no-tools loaded-config snapshot. The
device and shell metadata denials remain. This introduces no activation route;
cleanup, credential diagnostics, full round trip and criterion 17 remain open.

## Basis and scope

The owner authorized SWBPIPE's App v4 integration for v1.0 and then explicitly
authorized this manager to build shared needs: “That agent can also build in
SWBPIPE in conjunction with the App v4 agent, working on shared needs.” The
closure-only hold on other SWBPIPE lanes does not prohibit this work. RT-E1 and
exit criterion 17 entered main through #1732, merge `541446a9f1`.

The objective is an agent that operates SWBPIPE effectively through its own
capabilities. The first increment queues every change for the person's review.
It introduces no autonomy grant, acceptance tool, issuance or release act.
DEC-041 and earlier App designs are historical context, not implementation
instructions. The Decisions API is excluded entirely.

The current implementation order and activation authorization are stated above.
Official stock Codex acquisition and user-configured local or hosted providers
are authorized within the portable design. Credentials remain person-supplied
and keychain-held; local and hosted evidence identifies which route was used.
Publication/release and broader UI design remain distinct owner acts.

## Catalog ownership

[`agent-capability-catalog.json`](agent-capability-catalog.json) is SWBPIPE's
implementation contract. Its origin is App commit
`e1e3f4615b6f766b313c3492506f68254afd8a06`, path
`execution/PKG-09/DEL-09-06/Design/SWBPIPE_CATALOG_PROPOSAL.json`, SHA-256
`64aad707acd1d409f3d255381fc597e2ee74e7a4d048aadc5382414d63c64f8c`.
The initial local version 1 changed catalog identity/standing and added origin
metadata. Version 2 also adds bounded proposal assumptions and distinguishes
live-basis admission from completion against retained proposal/run evidence,
repairing independent review findings. Version 3 (RT-E1 milestone 1, below)
changes the admitted operation intents, the summary and the result-read input;
limits and the dynamic projection rule are unchanged. Version 4 (milestone 2,
below) adds a seventh read tool and the component, support-configuration and
deletion intents. The App copy stays
origin evidence and is not a second editable catalog. A local contract commit,
integration into main, and demonstrated runtime conformance are distinct facts.

Versions 1 to 3 had six tools: read the summary, read nodes, propose
operations, observe a proposal, solve, and read results. Version 4 adds
`swbpipe_read_records`. Version 2 admitted only native
`EditorOperationIntent` `modify` / `Node` / `set_field` on `position.x`,
`position.y` or `position.z`, which could not build a model.

### Catalog version 3: building W9-A from blank (milestone 1)

`swbpipe-catalog/3` keeps the six tools and admits these native discriminators,
each pinned in its own `operationIntent` variant (operation kind, object type,
field path, unit/dimension and the `before` form). The applier's change kinds
are used as they are; `add_object`/`remove_object` in
`schemas/model_operation.schema.json` are not applier kinds and are not used.

| Change kind | Operation / object / field | Use |
|---|---|---|
| `set_field` | modify / Node / `position.x\|y\|z` | move a node (v2) |
| `create_material` | create / Material / `materials` | E with G or ν, α |
| `create_node` | create / Node / `nodes` | node position |
| `connect_pipe_run` | connect / Element / `pipe_segments` | straight pipe, inline section |
| `create_support` | create / Support / `supports` | restraint set |
| `create_load_case` | create / Load / `load_cases` | primitive user load case |
| `create_primitive_load` | create / Load / `primitive_loads` | thermal, force, moment, imposed displacement |
| `update_load` | modify / Load / `pressure_regions` | regions before the exact route |
| `set_field` | modify / Model / `pressure_profile` | activate `3.0.0/exact_pressure_v3` and its shear model |

Everything else is refused at the schema: deletes, components, bend insertion,
library records, combinations and model settings. The applier remains the
semantic validator and still refuses an agent-written bend flexibility factor.
A proposal is one atomic batch; each step applies to the document the previous
step left, so later operations may name ids created earlier in the batch.

The agent sends `operation_id`, `operation_kind`, `target`, `change` and
`rationale` only. The host (`embeddedAgentSession.ts` `stampAgentOperations`)
stamps `operation_status: proposed`, `author_type: agent`, `queue_id`, `source`,
not-run `validation` and the constant `audit_boundary` and
`professional_boundary` records; the catalog refuses any of these in the
arguments. This keeps the native batch unchanged while the full W9-A exact-route
build (13 operations) measures about 9 KB of arguments, inside the 16 KiB
`argumentBytes` limit; the full native form measured about 17.6 KB. `after`
remains the applier's JSON text, so the host re-encodes no agent number. The
schema keyword `description` is now admitted as projected guidance only; it
asserts and confers nothing.

The summary adds `projectId`, `schemaVersion`, `pressureContract` and
`pressureProfileBefore` (the exact `before` text `pressure_profile` requires),
and lists the admitted kinds. `swbpipe_read_results` takes an optional
`filter` on result kinds and entity references; a cursor is bound to its filter.

Milestone 1 evidence, on the candidate named in its PR:

- `core/model_operations/operation_applier/tests/agent_w9a_journey.rs` applies
  the fixture's W9-A proposal (`fixtures/model_operations/agent_w9a_journey.json`),
  stamped as `author_type: agent`, to the desktop blank document as one batch
  and solves it on PF and on EX (Euler-Bernoulli) in both solver modes. All 90
  frozen W9-A rows of `validation/references/w9_benchmarks/references.json` meet
  the W-9 criterion in each run, and a stale basis applies nothing.
- `embedded_agent/catalog.rs` tests admit the fixture's arguments for both
  routes within `argumentBytes`, refuse other kinds, fields and host fields, and
  bound the thread/start frame with all six declarations and maximum
  instructions under the 128 KiB frame cap.
- `embeddedAgentW9a.test.ts` binds the blank document and the host stamp to the
  fixture and applies the stamped batch through the desktop batch service on the
  wasm engine; `embeddedAgentSession.test.ts` covers the summary fields and the
  filtered, filter-bound result cursor.

These establish the catalog, stamp, applier and solver links separately. They
do not establish a model's tool use, the native webview review journey or the
person's Apply in the running app; that is the pinned live W9-A witness, still
to be run. Criterion 17's reference system is not established by W9-A. That system is
specified in DEL-09-01 `Work/reference-system.md`; its §11.3 lists the operation families
the agent needs, from which the later catalog milestones take their admitted kinds.

### Catalog version 4: components, supports and corrections (milestone 2)

`swbpipe-catalog/4` admits these further native discriminators toward exit
criterion 1's families (the reference system is DEL-09-01's, PR #17):

| Change kind | Operation / object / field | Use |
|---|---|---|
| `insert_component_symbol` | insert / Component / `components` | bend marker, tee, reducer (eccentric offset), valve, flange, expansion joint |
| `set_field` | modify / Component / `objective_connector.hardware\|pressure_model` | tie rods, effective-area pressure model |
| `update_support` | modify / Support / `configuration` | change a support's family, restraints, stiffness, hanger or nonlinear behaviour |
| `delete_component`, `delete_support`, `delete_pipe_run`, `delete_node` | delete | correct an applied build; refused while dependents exist, never cascading |

**Prompt cost.** Every turn carries the tool declarations, which matters for a
local model. Version 4 replaces version 3's per-kind intent variants with one
intent schema whose `change_kind` and `field_path` are closed enumerations of
the admitted values, plus one compact kind table in the proposal tool's
description. The catalog's `admittedOperations` rows then admit only the listed
(operation kind, object type, change kind, field path) combinations; the host
checks them in `validate_proposal_context` after schema validation, and they are
not part of the declarations. Each row must lie inside the declared schema and
none may repeat, or the catalog does not load. Per-kind unit, dimension and
`before` forms are guidance; the applier refuses any that are wrong.

| Catalog | Declarations (bytes, compact JSON) | About tokens | Admitted kinds |
|---|---|---|---|
| v3 | 23,806 | 6,000 | 9 |
| v4 as first drafted (16 pinned variants, long guidance) | 40,650 | 10,200 | 16 |
| v4 | 17,530 | 4,400 | 16 |

Adding a kind now costs one table row of guidance (about 100 to 400 bytes) and
enumeration values, not a repeated envelope. The exact route's objective-connector
shape is not spelled out in the declarations; the agent asks the person for its
stiffness, axes and offsets. An on-demand guide tool is the route if that proves
insufficient.

`create_support`'s guidance names guides, line stops, springs, variable spring
and constant-effort hangers, and gap, lift-off, one-way and friction behaviour.
The milestone 2 journey creates anchors, a guide, a vertical support, a
variable spring hanger, a constant-effort support and nonlinear friction and
gap supports; line stops, plain springs and spring hangers are covered by
guidance only. Creation needs at least one linear restraint, and a
nonlinear behaviour acts on a DOF the support does not restrain linearly.

**k and SIF stay the person's (owner ruling, O5).** No `modifiers` field,
`bend_realization`, `insert_bend_at_corner` or `apply_library_record` is
admitted, and the applier refuses an agent-authored bend or tee insertion that
carries modifiers, as it refuses any agent-written k. The agent proposes a bend as a geometry marker and a tee
without modifiers. The person then realizes each bend through Insert bend at
corner (converting the agent's marker, keeping its id) and enters k, the SIFs
and their source in the app. Insert bend at corner moves the corner and
shortens its two pipes, so it is refused while anything attaches to them: the
journey asks for it right after the components proposal, before supports or
loads. Batch review submissions are immutable, so k is entered after Apply as
the person's own operation, never inside the agent's batch. Until then the
solver warns (`BEND_USER_MODIFIER_INPUT_MISSING`,
`BRANCH_USER_MODIFIER_INPUT_MISSING`) rather than refuses; the summary's
`componentsAwaitingUserModifiers` reports the same condition so the agent asks
before solving. An unrealized bend marker behaves differently on the two
routes. The exact route refuses it before solving
(`EXACT_PRESSURE_FAMILY_NOT_ADMITTED`), so `swbpipe_solve` refuses up front and
names the bends the person must realize. The pressure-free route solves it as a
straight chord: k does not affect the chord's stiffness, a supplied positive
scalar SIF applies to the chord, and without one no intensified measure is
published. The solve result's message names those bends and says which have a
scalar SIF, so a result is never reported as if they were realized. Identifiers
in tool messages and in `componentsAwaitingUserModifiers` are bounded to the
catalog's limits. Identifier lengths here are JavaScript string lengths, that is
UTF-16 code units; 160 code units are never more than the 160 characters the
catalog schema's `maxLength` allows. A message names the leading bends whose
lengths, each plus two for the separator, sum to at most 300 code units (200 for
the bends without a scalar SIF) and ends with an ellipsis if any are left out,
so it stays inside the 1,000-character message bound. The summary lists the
first 32 identifiers of at most 160 code units, omitting longer ones, while
`count` stays complete.

**Applier refusal (M2-D1).** The applier refuses an agent-authored write of k
or any other component modifier, whatever route the operation takes; see
"Author routes and the trust boundary" below for the codes, the routes that
stamp `agent` and the accepted residuals.

`swbpipe_read_records` reads a bounded page of components, supports, pipes or
nodes at the current live basis, like node reads. Each record carries its
canonical JSON text and the exact `before` texts its admitted edits and
deletions require, as the applier compares them: the engine's canonical JSON
for a component and a support configuration, and for a deletion the applier's
own summary (trimmed label; a node's coordinates in the applier's number form,
which never uses an exponent). A record whose deletion the applier would refuse
for a missing label or coordinate carries no `delete` text. The bounds:

- Each text (`recordText` and every `before` value): the UTF-8 byte length of
  the raw string is at most 16,384.
- The page: each entry is measured as the UTF-8 byte length of the compact
  `JSON.stringify({id, recordText, before})`. Entries are accepted, up to the
  requested limit (at most 50), while the running sum of those lengths is at
  most 49,152; the next entry starts the next page. Array punctuation and the
  result envelope are not counted. The whole serialized result is separately
  capped at 64 KiB, and exceeding that cap is an `execution_error`.
- A record id, like a node id in `swbpipe_read_nodes`, is a non-empty string of
  at most 160 UTF-16 code units.

A record over any of these bounds, including a single entry over 49,152 bytes,
fails the whole call as `unavailable`; nothing is cut or skipped. The message
names the record, except when its id is itself the cause. The cursor is bound
to its family.
It is a read through the existing `embedded_agent_host` command; no Tauri or
ingress command is added. Load-case and primitive-load deletions are not yet
admitted, because their `before` texts are private to the load-case panel.

A reference-system build exceeds one 16-operation proposal. The agent builds in
phases, each applied by the person before the next: materials, nodes and pipes;
components; the person's bend realization and modifiers; supports; loads; then
any corrections.

Milestone 2 evidence, on the candidate named in its PR:

- `core/model_operations/operation_applier/tests/agent_m2_component_journey.rs`
  applies the five agent proposals of
  `fixtures/model_operations/agent_m2_component_journey.json` to the desktop
  blank document, including an edit and two deletions whose `before` texts it
  derives as the applier compares them. The invented pressure-free model has
  one of each component family (the expansion joint is annotation-only on this
  route) and six support families (anchor, guide, vertical support, nonlinear
  friction and gap, variable spring hanger, constant effort). Built by the agent alone, it solves in both
  solver modes with the two modifier warnings, and an agent-written k is
  refused. In the journey order, with the person's bend realization, k, SIFs
  and source entered after the components proposal, it solves with neither
  warning. This is a build-and-solve check on invented data, not a numerical
  reference.
- `embeddedAgentM2.test.ts` applies the same proposals through the desktop
  batch service on the wasm engine, with the corrections' `before` texts taken
  from the session's record producer, and checks the awaiting-modifiers report.
  It also deletes a support, a pipe and two nodes with padded labels and
  coordinates such as 1e-7 and 2.5e21 using the producer's texts, and confirms
  the applier refuses the ECMAScript form. `embeddedAgentSession.test.ts` covers
  record pages, exact texts, UTF-8 byte bounds, the family-bound cursor,
  long-identifier bounds and the scalar-SIF wording of both solve paths. The catalog tests admit the new variants and refuse every
  modifiers path, bend realization, bend insertion, library record and other
  component or support field.

The exact route's objective-connector expansion joint and its tie rods are
admitted with guidance but are not exercised by this witness. Tees, nonlinear
and constant-effort supports, and reducers in pressure regions are refused on
the exact route until RT-A3 and RT-S2/S3 land.

The internal descriptor/result convention follows stateless MCP 2026-07-28,
with explicit workspace/proposal/run/page handles. It is projected to Codex
dynamic tools, not transported by MCP. Expand catalog-local schema references
into standalone descriptors. Retain output schemas and annotations in SWBPIPE;
annotations are descriptive and confer no permission. Project only the fields
supported by the selected supplier schema. Validate results before JSON text
encoding into dynamic `contentItems`; `success` follows the catalog policy.

## Existing authority and interfaces

Source inspected at `541446a9f1`; product source is unchanged from
`1560bbf7f7add4637a20572a2b0d404ef121af63` for these interfaces.

| Responsibility | Existing route | Required integration behavior |
|---|---|---|
| Live model, hash and undo | `apps/desktop/src/features/workspace/workspaceSession.ts` | Webview retains authority; bind each call to the session and revision |
| Queue registration | `workspaceSession.ts::registerOperationBatch` | Check claimed hash before registration; registration snapshots the current model and is not itself a stale-agent-basis check |
| Review/application | `workspaceSession.ts::handleRunOperationBatch`, `features/toolkit/BatchReviewPanel.tsx` | Existing explicit human apply; preserve preview requirements and immutable submissions |
| Validation/application | `services/operationBatchService.ts`; `src-tauri/src/lib.rs::model_operation_batch_args`; `core/model_operations/operation_applier` | Stateless Rust commands consume supplied model/batch/hash; the existing applier remains semantic authority |
| Solve | `workspaceSession.ts::handleRun`, `services/previewService.ts` | Recheck basis before admission, preserve evaluated hash, and retain actual job/run outcomes |
| Result disclosure | `features/results/resultReader.ts`, `features/result-export/csvTable.ts` | Preserve current view, exact-value semantics, withheld values and redaction floors |
| Native admission | `src-tauri/src/command_ingress.rs`, `user_release_reach_scan.rs` | Admit each new command; independently review permissions and repin reach evidence |

Abbreviated frontend paths in this table are relative to `apps/desktop/src`;
`src-tauri` paths are relative to `apps/desktop`. Live-session source references are not evidence that the new
agent adapter already exists.

## Host and session protocol

SWBPIPE starts one stock Codex app-server child over private stdio for its
admitted context. There is no network listener or MCP child. Keep its Codex home
and empty working directory separate from authoritative project storage. Do not
inherit the developer's Codex home, project instructions, configured MCP servers
or credentials. Disable built-in shell, file/patch and web tools using features
supported by the selected pin; configuration and prompting alone do not prove
isolation. Harmless denied-operation probes must establish actual behavior.

Initialize with the selected pin's experimental opt-in; offer the catalog as
`dynamicTools` on `thread/start`. Keep the frame reader responsive while calls,
human review or solve wait. Bound frames before JSON materialization and retain
bounded notification queues. Unknown requests fail explicitly; never grant an
unrequested shell/file/network approval. Provider selection is configuration,
not proof of network destination control.

On `item/tool/call`, Rust admits size/count budgets and validates the full
arguments against the SWBPIPE schema, irrespective of provider schema handling.
It captures the original RPC id, conversation/turn/call/tool, host application
generation, workspace handle and model basis/revision. Check workspace and
generation against the admitted session before dispatch. Summary captures a live
basis; node reads, new proposals and solve require the current live basis.
Proposal observation instead binds its retained proposal basis, and result
reads bind the retained run's evaluated basis. A current-model revision change
does not alone invalidate those historical records. Issue an opaque `requestRef` for that
pending call and forward only to the admitted webview. Handles are scoped to
that generation/workspace and are neither filesystem paths nor identity proof.

The webview rechecks its generation and the call-specific revision/hash before executing. The
summary bootstraps the current handle/basis without caller-supplied paths.
Reads are bounded at the producer, not serialized wholesale and then truncated.
Page cursors bind tool, workspace, basis, run and next offset; drift yields an
explicit stale/unavailable outcome. Values retain the document's stored units;
proposed units must match those units exactly. No silent conversion is allowed.

One new ingress-admitted completion command returns `requestRef` and the bounded
outcome. Rust looks up the original RPC destination; the webview cannot supply
an arbitrary RPC id. Reject unknown, duplicate, wrong-session, wrong-generation
or mismatched completions. Binding means correspondence to the immutable pending
call, not requiring every call's revision to equal the latest live revision.
Summary/node completion requires an unchanged live revision. Proposal submission
completion binds the actual immutable queue registration; observation binds its
proposal record and original basis; solve completion binds the admitted job and
evaluated hash; result reads bind the retained run/cursor basis. These last four
may complete after a live edit with explicitly captured/historical standing.
The returned basis must never be rewritten to the newer live model. A human
Apply advancing the revision does not erase its correlated applied outcome.
Invalidate detached sessions and outstanding handles;
never automatically redispatch. Validate output schema and standing before
answering Codex. Missing/uncertain application evidence yields `unknown`, not
success, rejection or a retry that might duplicate mutation.

## Proposal and interruption behavior

### Rust dispatcher component

`embedded_agent/dispatcher.rs` is an explicit host-driven component, still
unwired to commands or a live model. It consumes the existing protocol's tool
events in order, checks the original host-session token, confirmed thread/turn,
admitted webview/workspace/generation and catalog input, and issues a borrowed
dispatch view. It stores no argument clone and exposes no vendor RPC id.
The coordinator must serialize/retain any outgoing webview copy under its own
admission; the event batch's borrowed backing cannot be silently transferred.

Summary captures current basis; nodes/proposal/solve admission requires current
basis and the native claimed hash for changes/solve. Observation/result reads
require a trusted lookup of the exact retained proposal/run handle and basis,
including after a live revision changes. These lookup/evidence inputs are
Rust-only obligations on the future coordinator; they must come from actual
webview/domain records, not copied model arguments or completion assertions.
The future command derives invocation origin from the real webview/session.

The dispatcher reserves GENERAL state (8 MiB), at most 16 concurrent completion
parses (32 MiB each) and each raw record's 64 KiB envelope plus 128 KiB metadata
allowance **before dispatch**. The actual prescan price must fit the reserved
parse allowance before numeric checking/materialization. Schema/basis/evidence
validation precedes capturing a record; invalid input does not consume the
pending call. Current-basis read success must still match at completion.
Proposal/run completion instead preserves original record basis, handles,
run id/evaluated hash and actual standing across later live edits. Solve reply
status must equal trusted catalog standing derived from the actual job owner;
a successful result read requires a completed run. Matching run identities
alone cannot establish completion. Standing mismatch preserves both pending
reservations and allows the truthful failure/unfinished outcome to be recorded.
Applied
observation requires a non-null outcome hash vouched by the record owner.
Applied completion retains that schema-valid hash alongside the raw outcome,
including when the proposal-submission wire result carries only its handle.

Validated raw outcome bytes, original provenance and their backing are retained
before any session-driver completion attempt. Queued, detached, lost and
unconfirmed delivery remain separate from the domain outcome. Closing the
connection loses vendor references but can still capture a correlated late
domain outcome; it cannot reopen or redispatch a call. Duplicate completion and
older-reference replay remain refused after custody transfer. At 64 retained
entries the dispatcher refuses further work; it never evicts an unresolved or
completed record implicitly. `take_actual` transfers an Arc with its reservation
to the actual outcome owner, who must preserve the domain/receipt evidence.
Dropping a delivery object does not remove the ledger's outcome.

These are requested-allocation/GENERAL reservations, not RSS or retained-solver
pricing claims. No allocator, pool, solver policy, thread/process startup,
listener, credential, persistence or mutation route is changed. The 19 focused
dispatcher checks exercise binding, invalid/rounded-byte outcomes, history,
applied outcome retention through failed delivery, admission pressure and
bounded custody. They do not establish the future coordinator's actual record
lookups, command authentication, native cleanup or model integration.

### Claimed webview transport component

`embedded_agent/webview_bridge.rs` and `services/embeddedAgentBridge.ts` implement
the next transport seam, explicitly constructed and still without a live Tauri
command, listener or workspace registration. A notice carries only `requestRef`.
Native code retains the original validated argument envelope; the actual invoking
webview/session must claim it before any webview domain work. A claim rechecks
origin and current basis for live calls, preserves admitted historical basis,
and consumes execution authority before returning its response. Response loss
never reopens the claim. Detachment/close retires unclaimed work; an already
claimed operation can still report its correlated late actual outcome.

The native transport serializes borrowed arguments without cloning their Value,
under a separate 512 KiB GENERAL allowance per offered claim (64 KiB wire cap).
Its 128 KiB state allowance covers 64 bounded entries. Offered buffers are moved
with their leases into claims and discarded on retirement; 64 claim tombstones
remain until bridge destruction, including after actual-outcome custody transfer.
These allowances price requested allocations, not RSS or retained solver usage.
The eventual native adapter must serialize responses while holding claim backing;
framework-owned IPC copies retain the existing command-ingress residual.

The webview transport accepts only the native claim response as execution input,
rechecks actual workspace state immediately before execution, bounds UTF-8 claim
and completion bytes, limits active calls to 16, and retains 64 tombstones without
implicit eviction. It retains the actual record reference and raw catalog outcome
before its single completion attempt. Queued/detached/lost/unconfirmed delivery
cannot erase it or trigger domain replay; taking actual custody keeps the
execution tombstone. Execution exceptions yield delivery uncertainty rather than
invented rejection or rollback. The authoritative domain owner must retain
actual/unknown records even if its execute hook throws after an effect.

This seam does not authenticate an installed command or prove actual record
lookups: the future adapter must derive native Origin from the real invoking
webview, admit its raw command bytes, construct trusted Evidence from actual
queue/job owners, and admit retained frontend IPC copies before use. Domain
producer hooks must recheck basis across asynchronous preparation and bound reads
at the producer. No execute hook is attached to workspaceSession by this PR.
The focused transport regressions establish one-shot binding/custody behavior,
not native-session isolation, cleanup, integration, AC-005 or criterion 17.

Require `claimedModelHash == basis.modelHash == current session hash` before
`registerOperationBatch`; repeat the existing current-basis check at application.
Construct the batch in the host and stamp `author_type: agent` plus original
conversation/turn/call ids. Caller-supplied validation, attribution or source
fields are untrusted. Preserve native intent shape and per-operation rationale.
The proposal envelope also requires a separate `assumptions` array: at most 16
records, each with a bounded stable id, statement and affected native operation
ids. An empty array declares none. Reject duplicate assumption ids or references
outside the submitted operation ids. Capture these records immutably alongside
the proposal handle, batch id, attribution and original basis; display them in
review and retain them with session outcomes/receipts, including reject,
withdrawal and unknown. Do not flatten them into rationale or add undeclared
fields to the native intent. This context storage is not durable audit history;
attribution is not authenticated identity. Queue registration never applies.

Use existing validation, immutable registration, diff/review and human Apply.
Observe pending review, rejected, withdrawn, applied and unknown distinctly.
Turn interruption withdraws a proposal only while it is still pending. Serialize
withdrawal with application admission: if application has begun, preserve the
actual result or unknown. Interruption is neither rollback nor solve-job
cancellation. Restart loses session handles and cannot manufacture durable
acceptance history. DEL-16-03's durable audit/history residual remains open.

Solve requires a matching claimed basis before `handleRun`; retain solver mode,
evaluated hash, actual run handle and health. Progress goes through existing
supported host notifications/panel mechanisms. Result pages retain route,
health/check standing and the evaluated basis even when the live model changes.
Withheld/unavailable values carry no substitute numeric value.

## Boundaries and reconciliation

F-PIP-3, FR-AGENT-005, DEC-081 and Root `docs/PRODUCT_BOUNDARIES.md` govern all
agent-visible claims. Agents do not record, imply or derive engineering
acceptance, issuance, certification or code compliance. Numerical results and
passed checks do not confer professional authority. Human model-change review
and professional acceptance remain distinct. Existing claims checks and runtime
boundary scrutiny must cover new emitting surfaces; do not claim the Python
rationale reference is already integrated into the native path.

`docs/IP_AND_DATA_BOUNDARY.md` §6.1 permits owner-configured runtime transmission
of the owner's private inputs to the selected provider. It grants no public
redistribution rights and no exception for third-party protected standards.
Fixtures and public observations use invented data only. Do not commit supplier
logs containing private inputs, credentials, account identities or machine data.

DEL-16-06 owns this adapter's controlled-operation contract. DEL-16-01/02 retain
schema and preview; DEL-16-03 retains acceptance/audit; DEL-16-04 retains claims
and rationale; DEL-02-05 retains persistence; the workspace retains session
coordination. The new bridge does not close their existing residuals. The old
R7/F3 reference and candidate-generator program in DEL-16-04 are not the plan
for this authorized host slice; its matching scope wording must explicitly
separate the current integration from that older program before integration.
Neither standalone App qualification nor workflow-act machinery is inferred.

## Author routes and the trust boundary

The applier refuses an agent-authored write of any value the person enters:
the bend flexibility factor k (`OP-BEND-FLEXIBILITY-USER-ENTRY-REQUIRED`) and,
from RT-E1 M2-D1 (approved by Agent 0), every other component modifier
(`OP-COMPONENT-MODIFIER-USER-ENTRY-REQUIRED`). Those are the SIFs, stiffness
scaling and stiffness, and the modifier source. The refusal applies to a field
edit, a component created with modifiers, or a library record copying modifier
members. It reads `author_type`. The live catalog route refuses author and
source fields in the agent's arguments and stamps `agent`. Offline intake now
stamps every imported operation `agent` host-side. Requeue of retained records
re-stamps recognizable agent or imported content `agent` and refuses a
claimed-`user` record that writes a person-entered value (DEL-16-03
`Work/operation-authorship.md`).

**Residual, accepted by Agent 0 (2026-10-31):** a record saved before this
change that was imported claiming `user`, and that writes none of the protected
values, keeps `user`'s leniency when it is requeued: it may have no source and
an empty rationale, which an `agent` operation may not. The protected values are
k, the SIFs and other component modifiers, bend realization and insertion, and
library modifier members, and none of them can be reached this way. Re-stamping
every ambiguous `user` record as `agent` would misattribute the person's own
saved edits, so that is not done.

**Residual, recorded on Agent 0's decision:** any trusted webview code can
assert `author_type: user` to the applier commands. A source-role check in the
applier would prove nothing more, because the source is equally the webview's
claim. This is the same trust assumption as the live session's: the bundled
webview is trusted, and the native host binds an agent's calls to the admitted
session.

**Library and hanger values.** A library or hanger record that the person
explicitly chooses to apply, from a library the person imported, is the
person's own act. Its k, SIFs and other modifiers count as user-entered under
the owner's ruling. The applied record keeps its library provenance, so each
value's source stays traceable. The embedded agent cannot route
`apply_library_record`: the catalog's closed change kinds exclude it, and the
applier refuses an agent-authored library record that copies modifier members.

## Live-session integration candidate

`Work/agent-live-session.md` describes the native command, private workspace
producer capability, actual queue/job hooks and original-process observer now
with the selected ARM pin/profile now qualified as recorded there. Its public
Start branch permits ARM and refuses unqualified Intel. The minimal panel
described there starts a session only on the person's explicit action; there is
no automatic start. The
following component descriptions retain the evidence limits of their original
increments. The new candidate does not qualify AC-005 or criterion 17 by source
integration alone.

## Verification sequence and open observations

### Rust component implementation

The earlier component increment declared `embedded_agent` without an agent
command, start control, session dispatcher or webview route. The current live
increment above supersedes that unwired standing. `catalog.rs` embeds a generated
byte-identical product resource of this catalog, expands its references for the
six dynamic declarations, validates
inputs/results and checks proposal assumption membership. `protocol.rs` owns
the fixed initialization/thread/turn RPC sequence and opaque pending-call
references. Invalid inputs fail before dispatch; turn end/disconnect detaches
pending calls without claiming cancellation or reversing an applied change.
The caller must still authenticate the session, supply a trusted error basis,
and retain admission leases through all derived events and outbound values.

`framing.rs` caps a complete private-stdio frame at 128 KiB before any `Value`
materialization. It uses the existing general interactive ingress reservation,
checks borrowed argument/outcome spans against catalog limits, and poisons a
reader after invalid/oversized input. `numeric.rs` rejects delivered number
tokens that change decimal value on materialization. This protects the RPC
bytes received from Codex; the pinned supplier protocol does not establish
preservation of the model's original number lexemes upstream. Native operation
decimal strings remain strings. The only dependency-feature change is enabling
the existing `serde_json` dependency's `raw_value`; Cargo.lock is unchanged.

`tools/agent_catalog_resource.py` generates
`apps/desktop/src-tauri/resources/agent-capability-catalog.json` directly from
the authoritative Work bytes; do not edit the product resource independently.
The registered project check `agent-catalog-resource` uses `--check` to fail on
absent, linked, oversized or differing input. Both project and Root selectors
route its inputs. The Root software-workflow regression suite executes this
registered command in the existing full-checkout Repository checks job. Sparse
desktop builds and public source exports compile the product resource without
requiring the excluded execution tree. No workflow file, required status or
harness aggregate is changed. Equality establishes source correspondence, not
catalog semantics or runtime conformance.

`stdio_pump.rs` supplies an explicitly constructed portable stdio pump, with
32-slot incoming/outgoing queues and separate reader/writer threads. The catalog
admits 16 pending calls; the extra slots accommodate their control/status burst
without requiring a coordinator timeslice between each frame. It does
not launch a process or own protocol/session authorization. GENERAL interactive
admission reserves two 512 KiB stacks plus a 128 KiB bookkeeping allowance
before queue allocation/spawn; framing's reader buffers and each frame's backing
are separately admitted. Outbound values are moved and serialized to the stream,
with a byte-counting pass before enqueue and no full encoded-frame copy. Shared
backing references preserve custody, not a fresh budget for each clone. Queue
exhaustion is a terminal fault; no unknown operation is resubmitted.

Both workers wait behind a start gate. A second-spawn failure aborts that gate
and returns typed partial custody, rather than claiming completed rollback.
Stop request, terminal I/O, EOF and actual joined worker completion are separate
observations. A blocked generic read/write cannot be interrupted by this pump;
its caller must close/stop the owned process/streams and retain the pump until
workers can be joined. Observing joined workers confers no process-group or
descendant-empty evidence. Bookkeeping/finished joins have no hard wall-clock
guarantee. Abandoning unfinished custody deliberately retains it and its startup
reservation, even if a worker later finishes; integrating owners must keep that
custody rather than silently drop it and release live-stack accounting. This is
a fail-closed memory-retention limit, not crash cleanup qualification.

Pump component tests cover frame/backing custody, EOF before joined
completion, queue exhaustion, streamed output/newline/flush, serialization cap,
stalled read/write retention, second-spawn partial custody, static I/O faults and
constructor heap against the control/buffer reservations (not an OS/RSS proof).
They use controlled synthetic streams, not a supplier/model or native session.

`session_driver.rs` connects the pump to the fixed protocol operations. A trusted
host owner calls bounded polling continuously while domain/human work proceeds
asynchronously elsewhere. Each poll handles at most one frame and returns at
most 17 events, including the catalog's 16 detachments at turn end. This module
adds no scheduler, threads, process authority, Tauri route or live-model binding.
The host supplies a unique unpredictable connection token and current fallback
error basis; authenticating the generation/workspace and each call-specific
basis remains the dispatcher/webview's duty.

GENERAL admission reserves a nominal 8 MiB for v2 catalog/protocol bookkeeping,
then separate 2 MiB allowances before control construction, outcome encoding or
incoming-frame derivatives. Caller-owned input/outcome heap must already be
admitted. Leased event batches retain the incoming/derivative and session
backing; borrowers copying their payload must admit and retain that copy's
backing. Queue submission reports `Queued`, never peer delivery or application.
Control `Busy` refusals occur before protocol state changes; their admitted
input can be retried. Polling may instead defer one leased batch until a fresh
terminal observation. Invalid schema/reference completions leave valid pending
calls intact. Fallback-basis updates never substitute a newer basis into an
actual supplied outcome.

On observed EOF, I/O failure or invalid peer protocol, the driver stops dispatch
and disconnects once, reporting unresolved references without cancellation,
rollback or an invented domain outcome. Already-observed terminal state
suppresses queued new tool work. Partial startup returns custody for subsequent
observation; blocked I/O still needs the external process/stream owner. Actual
domain results remain outside the driver, including when an admitted completion
cannot be queued or its peer delivery becomes unknown. Synthetic driver cases
exercise handshake/declarations, original-RPC completion, preserved pending
references, interruption/detachment, terminal suppression, backing lifetime and
an admitted 16-call burst. The live host coordinator/session bridge remains
unimplemented and none of these checks establishes AC-005.

The protocol also treats the selected pin's unoffered built-in tool-activity
items as terminal on start/completion, including command/file/web, MCP,
sub-agent and image activity. Pending calls become lost references, never
fabricated application failures or cancellation. This observes a configuration
or isolation mismatch; notification timing cannot prove that an action was
prevented. The native process owner must still stop/clean up its supplier, and
actual disablement/OS isolation remains a separate activation proof obligation.

The macOS-only `macos.rs`/`sandbox.rs` launcher is not connected to product
startup. `supplier.rs` selects the process architecture's stock pin from the
committed supplier manifest and copies its exact bundled bytes, then the
launcher derives private home/cwd
and exact exec paths at runtime. It accepts a validated explicit model identifier
and a ready endpoint retaining the Rust-owned loopback scope; the sandbox's only network grant
uses that scope's runtime TCP port. The child's environment contains a fresh relay
capability, never the configured provider key. Config files contain neither
secret. Model strings are escaped before TOML construction. The provider alias
is now `swbpipe_relay`. The retained EOF fixture needs adaptation to the new
LaunchConfig/relay custody, probe port and provider alias before reuse; its
historical report bytes are unchanged.
The standalone Rust sandbox probe now requires `SWBPIPE_PROBE_ALLOWED_PORT` and
checks both named loopback families plus an unowned alias. Previous fixed-port
fixture reports remain historical; they do not qualify this dynamic-port path.

`loopback.rs` explicitly binds `127.0.0.1` and `::1` at the same OS-selected port,
refuses if either cannot be held, and exposes nonblocking accepts without giving
out listener ownership. Both listeners and the per-start random 256-bit capability
share a 64 KiB GENERAL userspace allowance. The relay separately admits its
90 MiB state/stack/kernel/connection allowances as described in its Design;
these are not an integrated native RSS/pricing qualification. The launcher retains an Arc through supplier
group cleanup, including retained Runtime custody on an unconfirmed live scope.
The relay owner retains listener/backing custody through actual worker shutdown;
its ready endpoint carries listener custody without the provider credential.

Literal root-directory reading and metadata on fixed OS aliases are needed for
the selected pin's startup; these do not grant reads of descendant user files.
The deny-by-default file restrictions, exact single exec, explicit fork deny and
accepted libinfo condition are unchanged. The one network line changes from
`(allow network-outbound (remote ip "localhost:8000"))` to
`(allow network-outbound (remote tcp "localhost:<owned-port>"))`. TCP-only
narrows the former IP rule because the scope does not own UDP endpoints.
Apple's installed `/usr/share/sandbox/com.apple.netbiosd.sb` uses `remote tcp`
with explicit ports; that is syntax precedent, not qualification of this recipe.
A test-only 8000 rendering, with only `remote tcp` inverted to `remote ip`,
reproduces the previously reviewed exact hash. This text guard is not native
enforcement evidence.
Alias/address coverage, actual per-start profile bytes, no-fork/exec/filesystem
and network denial still need native qualification on the selected candidate.
On code candidate `25228fe0994e5a9cb87292b3d6d5d86ffc3bedf5`, the guarded
`embedded_agent::sandbox::tests::native_permission_probes --exact --ignored`
run passed on the current arm64 Mac. The freshly copied standalone Rust probe
returned success only after all 15 checks passed: private home/cwd writes;
outside project/document/keychain reads and writes plus symlink-read denial;
both named loopback TCP endpoints; EPERM for `127.0.0.2` at the same port,
another loopback port, an off-host endpoint, listener creation and both forbidden
and self-spawn execution. No supplier, provider/model or credential was used.
The source-defined 15-check predicate and test exit status establish this bounded
observation; the generated per-run root/port profile bytes were not retained.
This is not comprehensive alias/UDP coverage, listener non-inheritance, explicit
C fork qualification, a stock-Codex round trip, EOF/crash cleanup or Intel proof.

The relay component adds explicit HTTP service/provider connections as described
in embedded-agent-relay.md; no product start or keychain/settings route, credential file,
new FFI/import, supervisor registration, packaging or platform-minimum change is
introduced here. Production stderr remains discarded. The ignored startup test
checks that bounded diagnostic text omits its fresh capability. Actual relay
credential acquisition, crash-output exclusion, Intel supplier and a complete
native-session witness remain unproved.

On shutdown the launcher retains the original unreaped `Child` through every
group observation and signal, then reaps it only after observing no live group
members. A census is evidence, not authority to signal an unrelated numeric
PID. Unknown cleanup retains a nonsecret exclusive marker and refuses the next
launch; no saved numeric PID is signalled. Parent-crash termination and absence
of escaped descendants remain unqualified. **Do not expose this launcher until
those cleanup duties and the remaining native-session isolation duties have
been established.** The early solver-worker dispatch and solver-specific memory
machinery are unchanged.

The opt-in native probes establish bounded observations on the selected Mac:
the actual pinned supplier initializes under this profile without a model;
owned-group stopping preserves an unrelated group; and the standalone invented
probe in `tools/agent_host_sandbox_probe.rs` checks 13 filesystem/network/process
outcomes. Private-home/cwd writes and the configured loopback endpoint succeed;
outside canary reads/writes, symlink escape, another loopback port, an off-host
address, listener creation and both other/self executable launches are denied.
The canaries named project/documents/keychain are invented files outside the
private runtime, not actual private documents or keychain files. These component
checks do not establish model execution under this Rust launcher, crash cleanup,
Windows capability, review-queue conformance or AC-005 completion.

Remaining implementation is the responsive runtime client/dispatcher, trusted
session bridge and ingress completion command, proposal-only review wiring,
operation expansion and criterion 17. The minimal explicit-start panel is in
`Work/agent-live-session.md`; its native journey evidence remains open. Existing
ScopeOfWork commitments and dependency conditions remain open and unchanged.

### Integration sequence

1. Validate all catalog schemas and standalone dynamic projections; compare the
   adopted fields with the identified App proposal. Review exact commitment
   wording independently and obtain Agent 0's confirmation.
2. Pin an official Codex binary and existing oMLX endpoint/model. Record version,
   official download URL and binary SHA-256 here before the live witness. Observe
   one harmless dynamic call, host validation, returned invented value, and a
   follow-up grounded in that value. Capture declared versus observed tool
   isolation separately. Greeting/listing/request capture alone is not a pass.
3. Exercise malformed/oversized frames and arguments, wrong initial binding,
   duplicate/unsolicited completions, revision/session replacement, interruption
   and uncertain outcomes with controlled protocol/session checks. Include a
   human Apply advancing revision while observation waits, solve completion
   after an edit, historical result pages, and retained structured assumptions.
4. Exercise actual proposal review, reject, stale refusal and one human-applied
   edit through the native route. Obtain independent permissions review for new
   Tauri/ingress commands and repin the reach scan as #1718 did. Preserve existing
   memory admission; re-price any changed retained route as its rules require.
5. Add admitted operation kinds for the build/solve/explain journey; verify the
   full criterion 17 reference separately from the smaller W9-A witness. A hosted
   journey must not be mislabeled as a local-model witness. Native packaging and
   product release remain separate owner acts. Catalog version 3 admits the
   W9-A kinds and version 4 the component, support and correction kinds, with
   the component evidence above. The live W9-A witness, the reference system
   itself and its remaining load and analysis kinds remain.

The selected supplier/model pin and actual harmless round trip are recorded in
[`agent-local-witness.md`](agent-local-witness.md). Those bounded observations do
not establish the desktop bridge or complete AC-005. The current
[official app-server guide](https://learn.chatgpt.com/docs/app-server), read
2026-10-28, documents stdio, initialization, generated version-specific schemas
and experimental opt-in. The selected binary's generated schema and actual
observations govern implementation, not assumptions from newer documentation.
