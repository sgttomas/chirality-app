# App v4 contract issues

The CI-1…CI-9 reports below retain the original walking-skeleton findings from
`APP-V4-GRAPH-CLOSURE-20261004`. Run `APP-V4-GROUP-A-20261004` resolves their
current path through named reviewed Design changes and tested code. Native
qualification and later Group A consumers remain separate obligations.

| Issue | Current disposition and evidence |
|---|---|
| CI-1 | CC-R declared-ID references adopted; Rust embedded registry and Node canonical-schema checks pass without rewriting refs. |
| CI-2 | CC-H/SUP1 full hosting generation adopted; NIR and NPTD definitions/prototypes reviewed. Current host records and cross-generation negatives pass. Standalone NPTD cross-home consumers remain named next-slice work. |
| CI-3 | Package snapshot has no invented requester identity; the source-route kind and separately referenced missing-identity limit are recorded and tested. |
| CI-4 | Owner chose exact absence label; omitted/empty/nonempty cases preserve request source and offer/capture/act wording. |
| CI-5 | CC-A/P selected host-native frozen alternative mechanism is implemented and tested with explicit confirmation stand-ins; actual native authenticity witness remains open. |
| CI-6 | Atomic durable capture, writer-owned IDs, ordered trusted late writes, add-once backlink and AC-7 link-pending semantics repaired/backchecked. CI-10 governs unverified cold replay. |
| CI-7 | CC-H LT-24 unverified development route implemented. Hash alone never qualifies; known version/content contradictions refuse, preserving frames and metadata. |
| CI-8 | Expected thread-start model contact is disclosed with its observation limits; explicit model/provider selection preserves Codex configuration. No new product network default selected. |
| CI-9 | Approved jsonschema 0.58.5 runtime gate validates complete entries before append, with offline declared-ID resolution and refusal/no-mutation tests. |
| CI-10 | Fail-closed native-origin repair is reviewed; trustworthy persistent replay still requires the retained SEAL-2 custody choice and evidence. |
| CI-11 | Native userVerification positive acceptance remains unsupplied; published proof mapping is known, but truthful-client supplier route and exact backend binding are prerequisites. |
| CI-12 | Bounded current reader/control repair addressed through reviewed RS/DV change; incomparable claims remain explicit, public reads are pure, and request binding is rechecked. Downstream adoption remains open. |
| CI-13 | Explicit App project/submission context uses the reviewed REC owning join; native cwd/home/run cannot supply it by inference. Reviewed known/unknown association and bounded native attachment consumer adopted; native/cold/other-home witnesses remain. |
| CI-14 | Generic request/frame/response retention is unsafe for credential-bearing native account RPC; synthetic-only method-aware transient/redacted repair is underway. |

Canonical review and command evidence lives in this run's `changes/`,
`reviews/` and `validation/`. The Group A work graph carries incomplete
consumer/native/qualification work. CI-10 custody and CI-11 native supplier receiving remain open below.

## CI-1 RS schema: relative `$ref` under a URN `$id`

- **Where:** DEL-04-03 `RS_RECORD.schema.json`. These entry kinds point into
  DEL-02-03 `checkpoint-record-entries.schema.json`:
  - `checkpointArrival`, `actRequest` and `actLapsed`;
  - the other checkpoint bodies (19 refs in all).
- **Found:**
  - The refs are relative file paths, `../../../../PKG-02_…/checkpoint-record-entries.schema.json#/$defs/…`.
  - The schema's own `$id` is `urn:chirality:app-v4:del-04-03:rs-record:0.1`.
  - Under JSON Schema 2020-12 and RFC 3986, a relative reference resolves
    against the base URI, which here is the URN, not the file location.
  - A standard validator (Ajv 8.20) therefore cannot reach the target.
  - The target has its own `$id`, `chirality:del-02-03/exec-checkpoint-entry-bodies/proposed-0.7`.
  - The Pass 4 prototype's own validator resolves by file path, so it never
    hit this.
- **Did:** the test rewrites those refs in memory to the target's `$id` before
  compiling. The file on disk is unchanged. The test asserts that the rewrite
  matched at least once.
- **Proposed:** in `RS_RECORD.schema.json`, refer to the checkpoint schema by
  its `$id`, `chirality:del-02-03/exec-checkpoint-entry-bodies/proposed-0.7#/$defs/…`.
  This is how it already refers to DEL-04-02's settings-in schema.

## CI-2 Generation identity: H5 against the hosting record schemas

- **Where:** DEL-01-01 `HOSTING_BOUNDARY.md` §3 H5 (v0.9; R18-1 C-20, R19-4
  L-1) against `hosting.lifecycle-event.schema.json` and
  `hosting.client-request-record.schema.json` (v0.8).
- **Found:**
  - H5 makes the generation identity {App session, App-owned home, spawn
    counter}.
  - Both schemas type `generation` as an integer.
- **Did:** the records carry the spawn counter as the integer generation. The
  session and the home are held in the host, not in the record.
- **Proposed:** move the schemas to v0.9 with a `generation` object
  {appSession, home, spawnCounter}. Alternatively, have H5 state that the
  record carries the counter and the session and home are given by the
  record's container.

## CI-3 The requester of a package file the recorder finds

- **Where:** RS §13.6 (decision packages; R23-24), DEL-02-03
  `$defs/actRequest.requester`.
- **Found:**
  - The mapping says the recorder supplies `requester`.
  - Nothing says how the recorder establishes which agent wrote a file it finds
    in `project/decisions/`.
  - The Pass 4 fixture uses `thread:fx-u1-manager`, an invented value.
- **Did:** the skeleton writes `{"kind": "agent"}` with no `identity`. The
  schema allows this. The decide-flow test compares bodies apart from
  `requester` and `time`.
- **Proposed:** RS §13.6 should state the source of the requester identity. One
  option is the thread whose file-change item wrote the file, when the App
  observed one. Otherwise the identity is absent, with a stated limit.

## CI-4 Package `scope` is optional, but the offer and capture require it

- **Where:** DEL-02-03 `$defs/decisionPackageFile.scope`, which is optional,
  against DEL-01-04 `aac.offer.schema.json` and
  `aac.capture-evidence.schema.json`, where `scope` is required with
  `minLength` 1. RS `humanAct.scope` is required.
- **Found:** a valid package file without `scope` cannot produce a valid A16
  offer.
- **Did:** the control does not offer such a package. The reason is shown:
  "the package names no scope, which the offer requires".
- **Proposed:** pick one of these:
  - make `scope` required in `decisionPackageFile`; or
  - have AAC §1.2 (A16 row) state the scope wording to use when the package
    names none, for example "not named by the package", as CE-4 does for its
    own elements.

## CI-5 Native confirmation (P-2) for a choice among alternatives

- **Where:** AAC §6.2 P-2 and §1.2 A16 row.
- **Found:**
  - P-2 has the host fill a native confirmation with the offer and "the
    buttons".
  - A16 needs a choice among two or more alternatives.
  - A native message dialog has at most three buttons (tauri-plugin-dialog
    2.7.2), so the alternatives do not all fit as buttons.
  - AAC does not say where the choice is made.
- **Did:**
  - The person picks the alternative in the webview offer.
  - The host then opens a native dialog it fills itself. The dialog shows the
    package, its identity, purpose and scope, and the chosen alternative with
    its consequences. It names the actor as "identity not verified". Its
    buttons are "Decide" and "Cancel".
  - Only "Decide" captures.
  - A webview script can change which alternative is pre-selected. It cannot
    press "Decide" or change the dialog's text.
- **Proposed:** AAC §6.2 should state this for A16. The alternative may be
  chosen in the webview. The native confirmation must show the chosen
  alternative's own text from the package file. The capture binds the
  alternative the dialog showed.

## CI-6 Capture evidence `recordId` "once written"

- **Where:** AAC §5.2 ("the RS record identity once written") and AK-e ("the
  capture evidence exists before any record is written").
- **Found:**
  - The capture is written before the record, so its `recordId` can only be
    added after it already exists.
  - AAC does not say whether the capture store entry is updated, or whether a
    second object is written.
- **Did:** the capture file is rewritten once, adding `recordId` after the RS
  append succeeds. Nothing else in it changes.
- **Proposed:** AAC §5.2 should state the rule. Either the store adds
  `recordId` to the capture once, or the record identity is minted at capture
  and written then.

## CI-7 Verification: LT-04's guard against U-06

- **Where:** HOSTING §7.2 (verification rule) and U-06, against §4.7 LT-04
  (guard `verified`).
- **Found:**
  - No pin is qualified, so no expected distribution identity is recorded
    (§7.1).
  - Every start is therefore `unverifiable` and goes to `refused` (LT-05).
  - U-06 allows a development run, "never labeled the pinned supplier", but no
    LT row covers it.
- **Did:** the start is refused unless one of two settings is given:
  - `CHIRALITY_CODEX_EXPECTED_SHA256`, which gives `verified` when it matches;
  - `CHIRALITY_ALLOW_UNVERIFIED=1`, which writes LT-04 with the actual
    `unverifiable` result and the reason "U-06 development run: unverified
    distribution, not the pinned supplier".
- **Proposed:** close U-06. Add an LT row, or a guard on LT-04, for the
  development run, and give the record element that labels it.

## CI-8 Network contact at `thread/start` with Codex's default provider (observation)

- **Where:** DEL-01-05 `ACCOUNT_AND_PROVIDER_ACCESS.md` §9 (K-12 start-up
  traffic table) and HOSTING §8.3.
- **Found (observed 2026-10-04, Codex 0.158.0, fresh scratch home, no sign-in,
  no credential, plugins and analytics off):**
  - With no model provider configured, `thread/start` with no turn made Codex
    open a websocket to `wss://api.openai.com/v1/responses`.
  - Codex's diagnostic output reported "HTTP error: 401 Unauthorized".
  - This contact happens at thread start, before any turn.
  - The §9 table lists model traffic only as "of a conversation", and OBS-1
    always had a local provider configured.
  - With a provider at 127.0.0.1 configured, no internet socket was seen in the
    process group (lsof polled every 50 ms during start and thread start).
- **Did:**
  - The tests configure a local provider where no server runs, so no outside
    contact is made.
  - The one contact above happened in a probe I ran before writing the tests.
    It is recorded in EVIDENCE.md, N-1.
- **Proposed:**
  - Add a row to the §9 table: "model destination contacted at thread start
    (websocket prewarm), before any turn".
  - Have the network view show it as model traffic.

## CI-9 RS W-1 "validates the entry against the schema" in the Rust writer

- **Where:** RS §14.1 W-1.
- **Found:**
  - W-1 says the writer validates each entry before writing.
  - The writer is the Rust host (AAC §6.2, R17-5).
  - The offline cargo cache has no JSON Schema validator crate; `jsonschema`,
    `boon` and `valico` are all absent.
- **Did:**
  - The writer writes without validating.
  - The test validates every entry the skeleton writes with Ajv 2020, against
    the schema as it is.
  - This is a gap against W-1. It is listed in README and EVIDENCE.
- **Proposed:** do one of the following:
  - approve a validator crate for the host (owner download decision; see
    EVIDENCE "Blocked"); or
  - have W-1 allow validation by a checker other than the writer, with the
    writer refusing what the checker rejects.

## CI-10 Cold pending recovery lacks native-origin proof

- **Run:** APP-V4-GROUP-A-20261004; independent review [V1-ACT](../execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/reviews/V1-ACT.md), ACT1. This new issue does not replace CI-1…CI-9 history.
- **Where:** app act_control.rs `recover_pending`/`write_pending`, AAC §5.2a no-matching-record replay against NA-1/HA-10, AAC §6.3 SEAL-1/SEAL-2 and §6.4 writable-file limits.
- **Found:** schema-valid matching pending and capture files in the writable project store can trigger `decision_view` to append a new `human_act`; inputSource text alone does not establish a native event. A file-drop/watch-folder route cannot create a person's act.
- **Disposition:** required fail-closed repair and named AAC/RS prerequisite clarification CC-CUST-A/CC-CUST-R: trusted hot-process original capture may retry; an existing valid matching RS entry may repair its backlink without upgrading provenance; cold unverified files retain facts and a visible limit, with no new human_act. Fail-closed repair and source/code backchecks passed (V0-CUST, V1-ACT-R2).
- **Unfinished required work:** trustworthy persistent replay and protected capture-origin proof remain in Group A I3. The owner explicitly decided “Keep SEAL-2 deferred; continue other work”; no seal/schema/keychain/signing adoption follows. CAPTURE_CUSTODY_DECISION.md remains preparation, not acceptance. Packaging/signing qualification stays with Group B at its actual point of need; deferral or moving the obligation does not complete it.

## CI-11 Native userVerification receiving route is not supplied

- **Observed source assessment:** 2026-10-05, stock Codex 0.160.0; [availability and NIR consequence packet](../execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/NATIVE_USER_VERIFICATION_AVAILABILITY.md). This is a separate discovery; CI-1…CI-10 history remains unchanged.
- **Where:** NIR §4.1 known-answerable/person-input mode and FO-6 positive acceptance; pinned supplier initialization capability advertisement and documented proof handoff.
- **Found:** published documentation supplies direct native proof in elicitation content, but the inspected advertisement predicate requires experimental API, supported hardware and codex-tui or exact local `Codex Desktop`. The App truthfully identifies as `chirality-app-v4`. This is source-derived capability advertisement evidence, not an observed or global claim that every verification primitive is unavailable. The inspected pages describe backend enrollment sequence but do not supply the exact backend endpoint contract.
- **Pinned-source follow-up:** [stock route investigation and Parent corroboration](../execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/investigations/UV_STOCK_ROUTE_FOLLOWUP.md) distinguish direct experimental local RPC admission from hosted elicitation delivery. The inspected dispatcher permits truthful initialized local clients subject to platform/account/connection guards; no successful primitive call was witnessed. Enrollment creates local credential metadata and leaves backend registration to the caller. Hosted verification requests separately require an eligible connection; direct RPC access does not establish that Chirality delivery route or backend binding. No status/device/key/enrollment operation was performed.
- **Current handling:** native acceptance without proof is explicitly unsupported; decline/cancel remain available. Truthful negotiated handling can conform while unavailable, but it does not complete the promised positive acceptance path. No spoofed client name, patched supplier, gated invocation or scope narrowing is adopted.
- **Unfinished required work:** a documented stock-supplier receiving route for Chirality's truthful identity, exact enrollment/verifier binding and appropriate native success/rejection witnesses. Group A I1-UV retains the obligation. Continuing a disclosed increment does not close it; removing it needs an owning scope disposition. Native verification is separate from P3 per-act presence and SEAL-2 capture provenance.

## CI-12 Reader order across independent record logs needs a basis

- **Found:** 2026-10-05 during the next actual decision-view reader assessment, [I3-READER-NEXT](../execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/changes/I3-READER-NEXT.md). RS R-1 gathers independent writer and cited act logs; R-6 builds corrections and R-8 uses latest dispositions. The recovered contracts do not supply a total order for competing branches across independent logs. Existing reader work must not silently select by opaque record ID, filesystem path or discovery order.
- **Adoption:** named `CC-RS-READER-ORDER` has independent RS and DV source concurrence. Current reader removes filename/UUID/time precedence, resolves duplicate/conflicting identities conservatively, preserves each contender and lapse history, and distinguishes recorded admission-order claims from human chronology/native verification. Explicit relations and the bounded source-reported P0 queue warrant remain usable. Core R2 and shared integration reviews are READY; original failures and intermediate findings remain in their records.
- **Current checks and limits:** Core 54 and shared 42 focused author checks passed; independent original-reader controls and request-binding/hot-pending controls passed. Public decision-view reads write nothing; startup/explicit writer continuation is separate. Confirmation rechecks the immutable bound request without vetoing unrelated partial-tail recovery or ambiguous prior act history. Downstream DV adoption notice remains for its loop; native UI, full reader journeys and CI-10 trusted cold provenance remain unfinished. This disposition is bounded code receiving, not whole Group A or gate acceptance.

## CI-13 Explicit project association at attachment/context receiving

- **Found:** 2026-10-05, [attachment consuming plan](../execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/changes/I1-ATTACHMENT-UI-PLAN.md) and [REC/RS source proposal](../execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/changes/CC-REC-ATTACHMENT-PROJECT-CONTEXT.md). App project association, native thread cwd/projectId, Codex home and workflow run are distinct. Current ACCESS preparation passes cwd as its project string; REC has a conversation-index project slot, but its actual owning association/tag join is absent. NIR0.2 and HOST0.10 have no equivalent project/run field.
- **Route:** owning REC/NIR/ACCESS source agents prepare the smallest reviewed explicit context handoff through existing contracts. Preserve historical thread project P when sourced, otherwise unknown; freeze explicitly selected App project Q for a new submission. Unknown membership must not become a temporary-cwd project. No arbitrary canonical field, new sidecar, native turn inference, human approval gate or source-scope acceptance is adopted by this issue.
- **Definition disposition:** REC R1 and ACCESS explicit-context definitions are independently READY with NIR source concurrence. Known explicit Root project references and private unknown are distinct; unknown emits no canonical ACCESS or REC project row, while ordinary input remains available under native guards. Durable and hot submission tags jointly refuse same-token retagging; hot-only bindings retain explicit cold limits. The original known-index/hot-tag model failure remains in the REC review chain.
- **Bounded adoption:** actual ACCESS/Host-owned REC APIs and native selection/submission consumer are independently READY. Core context/access/recovery checks passed; the genuine private Host/helper/custody/ledger/pipe joins plus affected consumers passed77 checks. Historical P/current Q and unknown/no-row/hot-only behavior are explicit. That historical contribution supplied H-acct only; later reviewed PR1096 access work supplies H-key startup and explicit mode/home routing. These code contributions do not establish native authentication or provider journeys.
- **Remaining:** actual native UI/provider and other-home journey observations and cold provenance; these are not established by callback/pipe mocks. WR run-prefix carriage is a separate producer/consumer join; ordinary text attachment work has no blanket workflow-parser hold.

## CI-14 Credential-bearing native account RPC evidence

- **Found:** 2026-10-05 during [next ACCESS source preparation](../execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/changes/I1-ACCESS-HOME-NEXT.md). Current generic `SourceRequest` retains full params/frame and attempted frame and exposes reply/journal/snapshot material. Using it unchanged for `account/login/start` API-key input would violate ACCESS CR1/CR2 credential custody; this is source-confirmed retention, not a claim that a real key leaked.
- **Route:** bounded Unit A uses only synthetic canaries to implement the source-defined transient submission lifetime and truthful redacted/unavailable request, response, error, journal, snapshot and diagnostic evidence. Preserve actual source/outcome; a redacted view is never labelled the original sent frame. No long-lived duplicate solely for matching, generic filtering of unrelated notifications, or erasure guarantee is introduced.
- **Bounded adoption:** Unit A's transient request/reply/error/journal/snapshot/diagnostic receiving paths and Unit B/Root namespace/session routing have independent reviews and synthetic connected checks; PR1096 merged the bounded access contribution. Native secure-field/logout execution and full access qualification remain separate. Those warrants cover their actual vectors, not every malformed framing form.
- **OH-1 affected privacy continuation (2026-10-05):** [OAuth Host receiving review](../execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/reviews/V3-I1-OAUTH-HOST-RECEIVING.md) reproduced two retained-evidence canary failures while admission correctly stayed Pending/unmatched: private material echoed in a known completion's unexpected top-level `id`, and unexpected-key-only echo in a wrong-typed original RPC reply. The same genuine synthetic SourceRequest/cat controls also failed on immutable merged e2/196 baseline Host6c48/auth566. These are pre-existing known-auth reflection gaps preserved by the new OAuth projection, not newly introduced admission/cancel defects or real credential exposure. Original Unit A and candidate116 passes remain valid for their recorded vectors; only this framing/weak-association privacy scope is reopened.
- **OH-1 bounded repair:** exact original controls now pass unchanged; source-warranted typed public framing and privacy-only weak association preserve unmatched standing, while mandatory malformed-auth replies retain raw IDs only on the private original pipe. Host84/controller15 pass99 distinct checks and independent original-vector/preservation backcheck is READYdabb7e40. Prior baseline0/2 and successor0/2 failures remain historical; no generic filtering/DLP over unrelated notifications was adopted.
- **Remaining:** actual native UI/authentication/browser/device/model/provider qualification still needs its own actual witnesses. No real credential/home content, authentication, native key operation or provider model execution is authorized by this issue.

## CI-15 Native child-role collision discovery and shared-resource fit

- **Found:** 2026-10-05 through Parent's isolated stock 0.160.0 probe, [carrier and collision evidence](../execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/probes/ROLE_0160_THREAD_CARRIER_AND_COLLISION.json). Per-thread agent definitions appear only in that thread, but a same-name definition shadows a synthetic standalone user agent. `config/read` reports `agents:null` without those origins. The complete published package repeats the result; no child or real model was executed.
- **Contract fit:** ROLE CR2's `config/read` route cannot establish complete collision exclusion from this response. ACCESS/HOST's current M-A boundary explicitly shares `config.toml`, `AGENTS.md` and `skills`, with other home files not linked; native `agents/` definitions are not covered. [CC-ROLE-ACCESS-0160-FIT](../execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/changes/CC-ROLE-ACCESS-0160-FIT.md) preserves both clauses and the required discovery, namespace-protection and receiving consequences.
- **Standing:** open named source/Design fit, with no fourth target, process-wide fallback, user-configuration edit or governance change adopted. Current child supply remains not supplied. Complete discovery/collision exclusion, additive child content/base preservation and actual child association require their own inputs; ordinary workflow and native operations continue.

## CI-16 WR supplier records and RS native supply receiving

WR's run-text/supply check pipeline previously returned preparation and comparison
values without immutable supplier publication or an R3 receiving path. Existing
R3 required a numeric turn and omitted WR's adopted incomparable state.

Named WR/RS owning-source changes are technically adopted under the coordinated
Group A implementation authority after independent V6 source review. WR §16.8
now specifies explicit project-local immutable supplier envelopes and resolution;
RS preserves legacy integer coordinates and adds an exclusive opaque native-turn
form with faithful incomparable standing and adoption unknown. Source adoption
and exact hashes are in `CC-WR-RS-SOURCE-ADOPTION.json` in the Group A run.

Consumer propagation, actual publication and the source-bound Root/R3 join remain
in progress. Historical envelopes cannot mint native check authority. Unknown
project has no fallback; pending record publication never resends a turn. The
successful exact832 native text witness remains delivery evidence only. EXEC
open/end/chain ownership and full lifecycle records are separate unfinished work.

## CI-17 Per-item native turn custody across restart

The reviewed recovery core exposed a source fit: ledger0.2 openItems could retain
item IDs/types but not their known native turn associations. Live-turn inference
or a cold-correlation disclaimer cannot fulfill the required pointer custody.

CC-REC-ITEM-TURN-CUSTODY is technically adopted after independent V6-S1 review.
Ledger schema0.3 adds an optional opaque actual turnId; exact0.2 bytes remain
available, legacy absence stays unknown, and older readers reject the new rows.
No native content, new recorder, liveTurn inference or automatic resume is added.
The adopted source is implemented with cold-tuple tests (cold03); the final V6
custody review records RC1-COLD as repaired for the core scope. Root consumer
integration is in the combined checkpoint. Actual native quit/relaunch evidence
and external PI-6 mapping remain open. Exact source pins are in the Group A run's
CC-REC-ITEM-TURN-SOURCE-ADOPTION.json; review status in V6-RECOVERY-CUSTODY-CORE.md.

## CI-18 Development workflow selections were composed and sent as runs

- **Found:** 2026-10-07 during J1 publication work (run APP-V4-GROUP-A-20261004;
  TASK dispatched by HELP_HUMAN). The prior J1 reading was checked by HELP_HUMAN
  against the WR text and rechecked here.
- **Conflicting texts.** WR Design (`DEL-02-02 …/Design/WORKSPACE_AND_REGISTRATION.md`,
  accepted, governs):
  - TT-1 (SETTLED): "Only registered revisions (and bundled or host-listed
    workflows, LS-5, LS-6) are selectable for a run."
  - TX-1: "Only a selected revision with standing LS-1, LS-5, LS-6 or LS-8 is
    composed."
  - WP-6: "Selected-development evidence cannot be laundered into a registered
    selection_record."

  Run record `changes/I2-DEVELOPMENT-CATALOG.md` (affected receivers): "explicit
  per-run selection only, supply via existing WR run-start text after its usual
  checks." The built-in catalog's `coordinated-knowledge-work` has standing
  "App-v4 development build candidate; not a published release", which is none of
  LS-1, LS-5, LS-6 or LS-8. Root `prepare_run`/`send` nevertheless composed and sent
  development selections.
- **Correction (code only; no Design change).** A development selection may still
  be admitted, selected and shown with its development standing. Root
  `prepare_run` refuses to prepare, record or send a run from it, naming TT-1/TX-1;
  the panel shows the refusal and disables preparation. No standing is invented.
  The ordinary journey runs a hot registered revision (development copy → draft →
  review → A15 → registered selection → run). `PreparedRunPublication` already
  refused development admission for a `selection_record`. The library-level
  `PreparedRunText::start` composer still accepts any admitted `Selection`, because
  a maintained catalog test asserts development provenance through composition;
  production reaches it only after the Root refusal.
- **Tests moved, assertions unchanged:**
  `workflow_root_closed_prepare_scoped_send_failed_turn_and_genuine_pages` and
  `workflow_root_stale_prepared_scope_keeps_original_receipt_without_resend` now use
  a registered selection. The new test
  `workflow_root_development_selection_run_is_refused_tt1_tx1` shows the refusal,
  with no run, no WR record and no `turn/start`.
- **Alternative for the design owner and the owner:** if development runs are
  wanted, a named, reviewed WR Design change could add an explicit development
  standing (for example an LS-9 "development build candidate") with its own
  selection_record standing value, TX-1 composition rule, framing and limits, and
  RS R3 consequences. Until then the accepted Design governs.
- **Consequence:** the earlier exact832ec9 native workflow witness
  (`probes/NATIVE_WORKFLOW_832ec9_ATTEMPT_2.json`) ran the development selection
  `coordinated-knowledge-work`. It remains valid historical delivery evidence for
  those bytes, but it is not evidence of a conforming registered workflow run, and
  it cannot be reused as such. A registered-selection native witness is still needed.

## CI-19 (J2) EXEC compatibility report: representation limits at publication

- **Found:** 2026-10-07, J2 TASK of `APP-V4-GROUP-A-20261004`, while
  implementing `execution_compatibility::report::evaluate`, which publishes the
  EXEC report body (`compatibility-report.schema.json`, proposed-0.6, embedded
  byte-identical at `src-tauri/resources/workflow_role/`) only from supplied facts.
- **(a) Unrecognized elements.** EXEC EV-2 reports an unrecognized required-tool
  element as *not established*, never skipped, and CR-9 lists every declared
  checkpoint. The schema's requirement row requires `class` and `necessity`
  from closed enums. Its checkpoint row requires a recognized required act,
  reached-when kind, subject class and held-actions form, and a boolean
  `governed`, so an unrecognized `governed` value (FB-19: preserved, never
  assumed) has no place either. Such an element cannot be represented. The
  code refuses publication, naming the element. Nothing is dropped or guessed.
  For an unrepresentable required-tool element, the advisory preparation still
  reports the check as *not established*. For an unrepresentable checkpoint,
  the Phase-1 check is unchanged (PH-3) and may pass; only publication is
  refused. Proposed EXEC change for the Design owner (not made): allow
  `not_established` for row `class`/`necessity` and for the checkpoint fields
  including `governed`, or add a list of unrecognized elements carried as found.
- **(b) Revision method.** The report identity (CR-2) has no `revision_method`,
  which WD-v0.8 §6.1 and CC-CONTENT-IDENTITY carry. The code omits it from the
  identity and states it in `limitations`. Proposed: an optional
  `revision_method` in the report identity.
- **(c) Host facts for App-only runs.** `host.host_id`, `host.catalog_edition`,
  `host.catalog_readable` and `surface.channel_state` are required. A workflow
  that needs only harness capabilities, checked for an App run on X with no
  external host, has no host identity, edition, catalog readability or channel
  state to supply. It therefore has no publishable report unless the caller
  supplies them. The code refuses instead of inventing them. The Design owner
  should say what CR-4 and CR-5 mean for an App-only run.
- **(d) R14 without a report.** RS R14 keeps "no report evaluated" explicit,
  but `compatibilityReportRef` requires a report reference even for that
  value. The code produces no R14 body when publication is refused and never
  uses a preparation id as a report reference. RS should say how the absence
  is written.
- **(e) Strictness.** `report_check` now treats any unrecognized required-tool
  element, including one marked optional, as *not established* (WD §3.4). This
  is in tension with EXEC PS-5 ("optional references never block") and with the
  older `Compatibility::check`, which still ignores unrecognized optional
  elements; the Design owner should confirm which reading governs.
- **Not changed:** channel state stays `enabled`/`not_enabled`; an unobserved
  channel or an unobserved catalog refuses publication (V6: no schema change
  follows from collector absence). `actual_host` standing needs a real
  environment collector, which does not exist; current origins are
  caller-supplied (`illustrative`) or test double (`test_double`).
- **Standing:** open Design questions. Implementation and tests are in
  `compatibility_report.rs` and `compatibility_report_tests.rs` (`j2_*`, `v8_*`).

## CI-20 J1/J3 supply and lifecycle: gaps found in implementation

Found 2026-10-07 by the J1/J3 TASK of `APP-V4-GROUP-A-20261004`, partly through
independent review V9 (`reviews/V9-J1-PUBLICATION.md`). Each item states what
the accepted text says, what the code does, and what remains for the design
owner or the owner. No Design file was changed.

- **(a) Unknown `turn/start` outcome (V9 F-1).** WR §16.4 ("`turn/start` refused
  or fails before the item is recorded" → `supply_check` *not found*) and RN-4
  name a state for a refused or failed start, but none for an outcome that is
  genuinely unknown: no response, a timeout, or transport loss after the frame
  may have been delivered. The App now mints *not found* only from a typed
  Host refusal (`Host::prepared_turn_refusal`: the exact written `turn/start`
  received a correlated native error). The check cites that request's receipt,
  has no `turn` or item, and R3 stays unavailable (RS §13.6a). For an unknown
  outcome it mints nothing, shows "outcome unknown", records the run start as
  not confirmed and never resends. *Not found* there would be an unsupported
  claim, since the text may have been supplied. Proposed for the WR owner: name
  an unknown-outcome state (for example *outcome unknown*, with a later read
  of the turn when an identity becomes known), or rule that an unknown start
  leaves no `supply_check`. A start that fails before any frame is written has
  no Host receipt and is treated the same way.
- **(b) App-minted run identity (V9 F-7).** WR §16.1–16.2 make the run identity
  DEL-02-03's (EXEC). No EXEC producer exists, so Root mints an App-local opaque
  `run:workflow:<uuid>`, chosen to satisfy RS `$defs/runId`
  (`^run:[A-Za-z0-9._:/-]+$`). At J1 (`8a785ac4e3`), R3 `supplied_guidance`
  entries were written under that id with no `run_opened`, although RS R1
  marks the run identity record Required. This is interim. J3 closes the
  missing record: the App writer records `run_opened` (with `follows` for a
  sequential run) when the start turn is observed (EXEC A-2), and `run_ended`
  only on the person's explicit end (AE-7). The identity itself stays
  App-minted until the EXEC owner supplies or adopts one; a later EXEC identity
  must not relabel runs already recorded under this id.
- **(c) No end notice after relaunch (J3).** TX-5 and SQ-END require the
  end notice on the person's next turn after a run ends with no successor.
  After relaunch, the person can end a run that the record shows open and
  interrupted (`end_recorded_run`; `run_ended`, *the person*). But the notice is
  composed only from the typed `PreparedRunText` that the run's own process
  held. `PreparedEndPublication` deliberately refuses cold evidence ("cold
  evidence does not create a lifecycle event or a new sendable notice"). So no
  notice is sent for such an end, and the panel says so. For the WR owner:
  either permit composing the notice from the resolved run-start `run_text`
  (name, revision, run) plus the recorded end, or rule that an end after
  relaunch carries no notice.
- **(d) REC run tag and restart limit (J3).** EXEC A-2 and §2.7 have the run
  starter tag the conversation with the run reference through REC
  `tag / look up / tags of` (RECOVERY §4.1). On relaunch, RS writes the
  "App-restart interruption" `evidence_limit` on the run that was current. The
  ledger's tag write is owned by the Host (`hosting.rs`), which supplies only
  the NIR submission-context tag. J3's fence did not include a run-tag write or
  a startup RS writer. The App therefore stores no run tag. The record writes
  no restart limit, and records no automatic RE-4 "interruption not
  recovered" run-owner end. Reopen instead finds runs and conversations from
  the project's own RS `run_opened.conversationRef`, and shows the REC
  `app_restart_interruption` facts that name each conversation. Needed: the
  Host or REC owner adds a run-tag owner and lookup, and a startup writer for
  the restart limit.
- **(e) Start not confirmed, and liveness (J3).** EXEC A-3 says a turn that is
  not started leaves the run not opened. A refused or unknown start therefore
  records no `run_opened`, and is not live. A new start in the conversation is
  allowed. When the outcome was unknown and Codex did start the turn, its text
  sits in history with no run record (see (a)).

  "End ‹A› and start ‹B›" (corrected by V10 G-2):
  - **Before A ends.** B is prepared first: admission, verified selection,
    project, publication, composition and CK-1. If that fails, A is not ended.
  - **A's end is held.** It is recorded in memory and written only when B's
    start outcome is known.
  - **B opens.** A's `run_ended` ("ended to start ‹B›") is written, then B's
    `run_opened`.
  - **B does not open.** This covers a refused or unknown start, or nothing
    sent. A's end is written as a plain end ("ended by the person"; WR's
    end-notice pattern admits only that cause or *completed*). Its end
    notice is pending for the next ordinary turn. A B that was never sent is
    withdrawn.
  - **Every outcome releases A's end (V10 R-2).** The start call that claims
    B's hold owns A's held end and writes it on every outcome, including a
    failure before any send (for example another run of the conversation is
    busy, or B's publication fails). A being busy does not stop B's start; A's
    end is written once A is free, before B's `run_opened`.
  - **The step reserves its conversation (V10 R-5).** Until B's start outcome
    is known, the held B and the held A count as live in both one-run checks
    (prepare and dispatch). No third run can be prepared or started there, so
    a fallback "No workflow is in force" can never follow a live run.
  - **In-memory window.** Between the person's confirmed step and the start's
    outcome (one command, normally moments), A's end exists only in this
    process. If the process is lost in that window, A reopens as *open;
    interrupted* and the person ends it again (`end_recorded_run`).
  - **Residual.** When B's outcome is unknown, B's chain line ("ended to start
    ‹B›") may have reached the model while the record says "ended by the
    person", and the notice follows as well. For the WR and EXEC owners: name
    the cause for an end whose successor did not start, or allow "ended to
    start ‹B›" in the end notice.
  - **B's own records after a definite refusal (V10 review).** B's
    `selection_record` and `run_text` are published before its send. They
    keep `prior_run.ended` and the chain line "ended to start ‹B›", while A's
    `run_ended` says "ended by the person". They are the records of a run
    that never opened: B has no `run_opened`, so they make no RS lifecycle
    claim, and immutable records are not rewritten (WP-1). A reader must
    take A's ending from A's `run_ended`, not from B's records.
- **(f) Predecessor across relaunch (J3).** CH-2 and RE-7: a later run cites
  the run before it (`follows`, `prior_run`, chain line). The chain is composed
  only from an `OwnerRunEnd` held by this process, the typed owner callback.
  A predecessor ended in an earlier process gives the next run no chain line,
  `follows` or `prior_run`. Needed: a ruling on whether a recorded `run_ended`
  may supply the owner end for chaining.
- **(g) Compatibility wiring (J3, with CI-19).**
  - Root evaluates CK-1 when a selection is prepared for a run in a
    conversation, and CK-2 immediately before the start turn. Both are made
    from the run's own selection, holding library, home, generation and
    conversation. The result is shown and never gates a start.
  - With no environment collector, the inventory is unobserved, so
    publication is refused and no R14 is written.
  - Even a published report has no App store: WR envelopes admit only WR
    bodies, and RS has no report location. Root would therefore still write no
    R14 (CI-19 (d)).
  - `RoleBinding` exposes home and thread but no generation. The
    same-conversation obligation is met by looking up the binding for the
    run's own home and thread after the run's generation is checked as
    current. A missing binding stays `Unknown`.
  - No catalog edition is ever observed, so CK-3 is never evaluated.
- **(h) `run_ended.waitingArrivals` (J3).** The App has no checkpoint recorder
  (EXEC §2.4). `run_ended` writes `waitingArrivals: []`, meaning only that the
  App recorded no arrivals. It is not evidence that none were reached.
- **(i) Notice dispatch is counted once (J3; corrected by V10 G-1).** TX-5 says
  "once".
  - When consumed: only when the Host observed a write attempt of the
    `turn/start` frame carrying it.
  - Refusals before any write: the notice stays pending, and the next ordinary
    turn carries it. These refusals are parameter or scope validation, a
    refused request, or a record that could not be written. A pending notice is
    re-scoped to the current generation of the same home, so a Codex relaunch
    does not strand it. Its record identity and bytes are unchanged.
  - After its frame was written: if Codex then refuses the turn, or the outcome
    is unknown, the notice is not resent, and the model may not have received
    it. The panel shows the outcome. A *native* fork
  is not observed by the App, which has no `thread/fork` route. A run belongs to
  its (home, thread), so any other thread, a fork included, has no live run.
- **(j) An earlier record that can never be written holds `run_ended` (V10
  R-3).** RS W-2 has a run's log written in observation order.
  `flush_records` stops at the first record that cannot be written and holds
  every later one; each gets its "record write failed" limit when it is
  written late. W-2 gives no way past a record that can *never* be written,
  for example an R3 whose reserved record identity conflicts with an existing
  entry.
  - **Behaviour.** The person's later `run_ended` stays held. In this process
    the view says it is "held behind an earlier unwritten record of this run
    (W-2)", and
    the run is ended. After a relaunch the record has no `run_ended`, so the
    run reads *open; interrupted* although the person ended it (review probe
    P4). The person can end it again from the record (`end_recorded_run`).
  - **Options for the RS owner.**
    1. Keep strict order, as now. The person's end is lost on relaunch, and
       the person ends the run again.
    2. Define a terminal *not writable* state for such an entry. Record an
       `evidence_limit` naming the record and why it can never be written,
       then let later entries proceed.
    3. Let lifecycle entries (`run_ended`) pass a stuck R3, with a limit
       naming the R3 they passed.
  - No code change was made for this item.

## CI-21 (J5) App-kept draft bases and re-registration after relaunch

Found 2026-10-07 by the J5 TASK of `APP-V4-GROUP-A-20261004`, repairing J4
finding 1 (after process loss, the same workflow could not be registered again
in the same library). No Design file was changed. SEAL-2 stays deferred: no old
`RegisteredRevision`, `Selection` or A15 receipt is rebuilt from disk.

- **(a) Where the base is kept.** WR §3: "Draft bases | App data folder, keyed
  by draft key | The App only | App-kept pointer (R17-4); lost if the App data
  is lost — then the draft has no base (U-WR-12)". §8 gives the record:
  `draft_reference`, "App-recorded base", with `base` only when
  `base_recorded_by` is *app*. The App writes one such record per draft key at
  `<App user-data>/runtime/wr/draft-bases/<sha256 of the draft key JSON>.json`.
  It validates the record against the WR schema before writing and again when
  reading, and replaces it atomically. WR names only "App data folder" (§3 is
  PROPOSED; OI-008 open), so the sub-path and file name are this
  implementation's choice. For the WR owner: confirm or name the location.
  **Trust assumption (V11 J5-1).** The record is a claim, not proof. Any
  process running as the user can write it, including an agent whose Codex
  sandbox allows full access (D3). The App checks the record's schema and
  draft key. Since V11 it also requires that the first tuple in the base's
  lineage naming the target slot be a revision that the slot's ledger
  registered (SP-3: "a revision of that slot"). Otherwise the review refuses
  with DS-3 ("lineage not established") and names the tuple as ID-4's "lineage
  incomplete at ‹tuple›". A base naming another slot or origin cannot be
  checked against that library's ledger. For DS-1 (empty slot) the claimed
  base is still disclosed and becomes the new revision's `derived_from`, so a
  forged record can still place a false `derived_from` on a first revision.
  The `state`, `content` and `findings` fields record what the App saw when it
  wrote the record (V11 J5-6). They are not refreshed on later edits.
- **(b) Identical bytes cannot run again after relaunch.** *Closed by adoption
  (J8, 2026-10-08).* The owner chose "A15 re-confirmation now (Recommended)",
  and the WR change CC-WR-RECONFIRM is adopted (commit `007489e72b`). After a
  relaunch, identical bytes review as DS-8. A new genuine A15 re-confirms the
  registered revision with no new revision, and the result is selectable in
  that process only (WR §4.8). DS-4 still applies while the revision is
  selectable in the process, or when it is not LS-1. App implementation and its
  limits: CI-24. The original text follows, for history: "DS-4 refuses content
  identical to a registered revision ("select it instead"). Cold selection of
  that revision stays refused (SEAL-2). After relaunch, the person can run the
  workflow from the same library only by registering changed content (a
  refinement, DS-2)."
- **(c) Base freshness.** RB-3 names two freshness conditions: the live draft
  and the slot's latest revision. Following the I2 owner plan ("disclosed,
  frozen and checked under lock"), the App also freezes its App-kept base
  observation at review. It rechecks that observation at `current()` and under
  the ledger lock at G1:
  - a changed base withdraws the review, or after capture ends the attempt as
    *not completed* (the act is kept, with no effect);
  - an unreadable or malformed base keeps the attempt pending, with the exact
    cause.
  For the WR owner: confirm that base change belongs to RB-3.
- **(d) No base for in-place entries.** §5.1 and G-6 record the new revision as
  the *draft's* base. Before J5, the in-memory map also recorded a base, keyed
  by name, after an in-place registration. Within that process, a same-name
  draft written from scratch would then have passed SP-3. Now only draft
  registrations record a base.
- **(e) Folder removal.** §5.1: "Folder removed → the App's base pointer is
  dropped". The App drops the pointer when it observes the draft folder absent,
  at listing or at review. It does not watch the folder between its own
  observations (D3). A draft that an agent deletes and recreates between two
  App observations keeps its pointer.
- **(f) Exact ledger causes.** The ledger reader names the path, the line and
  the cause: *unreadable*, *malformed* (incomplete final line, not JSON, or
  refused by the WR `library_entry` schema) or *ambiguous* (`ledger_seq` out of
  order). For the slot under review, the registered lines must form one series
  under SP-1 and G-4: `sequence` 1, 2, …; each `prior_revision` naming the
  previous registered revision; and no revision registered twice. Otherwise the
  latest revision is reported as ambiguous, with the line that breaks the
  series. These reader checks are this implementation's reading of SP-1 and
  G-4. WR states no reader rule beyond LS-1.
- **(g) Root wiring.** `WorkflowRootSession::set_app_user_data` is called from
  `lib.rs` setup with the App data folder. `open_library` attaches that folder
  to each `LibraryOwner` (`attach_app_kept_bases`). An owner with no attached
  folder keeps bases in process memory only, and its review presentation says
  so.
  - **V11 J5-2.** `create_selected_draft` copies the draft and then records
    its base. If recording fails, a draft with no base could register only
    as DS-3, and D-1 forbids the App to overwrite it. So the App removes its
    own copy (`discard_unbased_copy`), but only when the folder still holds
    exactly the copied bytes. The refusal says that the copy was removed.
    Otherwise the draft is kept and the refusal names the folder to remove.

## CI-22 (J6) Readable native confirmations: what the A15 alert shows

Found 2026-10-08 by the J6 TASK of `APP-V4-GROUP-A-20261004`, repairing the
native journey witness defect D-1 (PR 1113 witness). The A15 alert embedded the
complete review and offer JSON. It grew taller than the screen, so the person
could not read the statement or reach the buttons, and pressed Return unseen.
No Design file was changed. The A15 repair uses only what AAC already
permits (below). The A16 App route and the three-button layout, added after
review V14 by HELP_HUMAN direction and the owner's decision, go beyond the
committed §4.1a and §6.2 text; the adoption text they need is at the end.

- §6.2 P-2 lists what the native confirmation shows: "the act wording, subject
  and its identity, scope, purpose, the arrival or 'standing act', and the
  buttons". It does not require the review itself.
- §4.2 step 1: "DEL-02-02 shows the review package". §6.2: "The interface may
  show the offer in the webview too, for reading; only the native confirmation
  captures."
- §4.1a (A16): "The host must display all selected text without silent
  truncation; if the surface cannot do so, it refuses presentation with the
  cause and captures nothing."

What the code now does (J6, revised after independent review V14):

- **(a) A15 statement.** The alert carries a bounded statement: the wording;
  each entry's name, origin, disposition, short revision and full revision on
  its own line, revision method and prior revision; the library, scope,
  purpose and standing; the review reference and the sha-256 digest of the
  complete review (`aac-offer-digest/0.1` canonical form); the offer and its
  short digest; the consequence; the actor with "identity not verified"; and
  what each button does. The App shows the complete review beside the digest
  the host reports, before the alert and, while the alert is open, under
  "Content named by an open native confirmation". Capture still binds the
  frozen offer (digest checked) and the frozen review (full equality). It now
  also checks that the review digest equals the one the statement named.
  The wording, consequence and act label follow the descriptor's kind and
  disposition (V14 F7). A *re-confirmation* descriptor (AAC §4.2 as adopted
  by CC-WR-RECONFIRM) gets "Re-confirm revision ‹k› of ‹origin›:‹name› for use
  in this App session. This registers no new revision." and the buttons
  [Don't re-confirm] [Re-confirm] [Cancel]. WR does not yet compose such a
  descriptor (J8); the statement is tested with a synthetic one.
- **(b) Bound, and the App route.** Each native statement is limited to 30
  lines and 1500 characters (not natively witnessed). Nothing is truncated.
  - When a logout/key-removal assessment, an A16 chosen alternative, a request
    answer or an attachment comparison does not fit, the App shows that
    content whole while the alert is open, and the alert names it by sha-256
    digest (V14 F1, F5). The logout alert always gives the counts and, when
    they fit, one line per live turn, outstanding request, active child,
    child with unknown activity and unresolved turn observation (DEL-01-05
    AE-12, KE-13, Q-5: "listing all three"). Counts alone are never the whole
    statement. The binding of each operation is unchanged and host-side: the
    frozen A16 offer and digest; the logout assessment's material recheck;
    the answer preview's recheck; the attachment owner/revision recheck.
  - A hard refusal with its cause remains only where no such route exists:
    an A15 whose entries' identities do not fit (with a ~120-character
    library path: a single draft fits; two in-place entries fit; a third is
    refused, so the person registers fewer entries per act); a statement
    whose fixed parts alone exceed the bound (for example a package purpose
    longer than the alert); a sign-in cancellation (a short fixed field set);
    and file acts (below).
  - A refusal is reported to the App as a refusal with its cause, never as
    the person's cancel (V14 F4).
- **(c) Default key: owner decision.** OWNER_DECISIONS "Native confirmation
  default key — 2026-10-08", answer "Three buttons; Return is safe
  (Recommended)". A15, A16 and request-answer confirmations use
  `YesNoCancelCustom("Don't ‹act›", "‹Act›", "Cancel")`: Return chooses
  "Don't ‹act›", which records nothing; tauri-plugin-dialog 2.7.2 reports any
  unmatched, failed or aborted alert as the third label, "Cancel"; only the
  middle label acts. Escape: the act sits in the alternate slot, so before
  the witness Escape had to be observed natively before reliance, with the
  layout revisited if it reached the middle slot (V14-R1 R1-1). Witnessed
  2026-10-08 (`probes/NATIVE_RECONFIRM_WITNESS_8cd69ff7.md`), on macOS
  (Darwin 25.6), for A15:
  - Escape and Return each closed the alert with no capture or
    registration, and "Don't register" was the highlighted default.
  - The App does not report which non-act slot either key took.
  - The middle button registered when clicked; the Cancel button was not
    clicked.
  - The A16 and request-answer dialogs were not witnessed natively.

  **Known limit: file acts are excluded.** Their three slots are
  act, decline and Cancel; under the three-button layout an aborted alert
  would map to the third slot, which there would be a decline. They keep
  [act (default)] [Decline this act] [Cancel], so Return still performs a
  file act, until a custom dialog exists. Logout, sign-in cancellation and
  attachment source keep their two-button layouts (the owner's decision
  names A15, A16 and request answers).
- **(d) File acts (V14 F3).** The file-act statement is bounded inside the
  freeze, before the actor and context are frozen and the offer is
  Presented; a refused statement leaves the offer Composed. The dead
  24 000-byte check is removed. The statement is readable lines (file path,
  content identity in full, scope, purpose, requirement, actor, standing),
  with no raw JSON.
- **(e) Numbers (V14 F2).** AAC §5.1 defines `aac-offer-digest/0.1` over
  integers only. Content holding a non-integer number cannot be named by
  digest: it is refused with the number's JSON Pointer location and that
  cause ("defines integers only"), not "the offer is not offered". A review is
  refused when it is opened for A15 (compose), so the person learns it at
  review time. Integers above 2^53 are digested exactly by the host. The
  App's own JSON parsing has already rounded them, so the App shows the
  host's digest and says it cannot recompute it.
- **(f) The App's digest is a reading aid (V14 F8).** The App shows the digest
  reported by the host and its own recomputation from the content it shows.
  A compromised webview could show other bytes beside the right digest; the
  binding is checked by the host at capture, never by the view. The App
  states this beside every digest.

AAC adoption text needed (for the AAC owner; the code above implements it
ahead of adoption, as directed by HELP_HUMAN after V14; not applied to the
Design):

> §6.2, after "the buttons": "The native confirmation shows a statement the
> person can read whole with its buttons on screen. Where content the act or
> operation binds is too large for that surface (an A15 review; an A16
> alternative and its consequences), the statement names it by reference and
> digest (`aac-offer-digest/0.1` form, integers only) and the App shows the
> complete content with the same digest before and while the confirmation is
> open; the capture binds that content as before, and the App's display is a
> reading aid only. A statement the surface cannot show whole and that has no
> such route is refused with its cause and nothing is captured. The act
> confirmations for A15 and A16 present [Don't ‹act›] [‹Act›] [Cancel], with
> the first the default; only ‹Act› captures, and an aborted or failed
> confirmation captures nothing (OWNER_DECISIONS 2026-10-08). A file act's
> confirmation keeps [‹act›] [Decline] [Cancel] until a surface exists whose
> abort cannot be read as a decline."
>
> §4.1a, replace "if the surface cannot do so, it refuses presentation with
> the cause and captures nothing" with "if the surface cannot do so, the App
> shows the selected alternative's statement and every consequence whole and
> the native statement names them by digest (§6.2); only when that is not
> possible is presentation refused with the cause, capturing nothing".

DEL-01-05 (AE-12, KE-13, Q-5) and NIR are met as written: the logout list is
shown in full (in the alert or in the App while the alert is open), and a
request answer of any length can be confirmed unless its content holds a
non-integer number, which is refused with its location (V14-R1 R1-1).

## CI-23 RS schema `if` breaks the DEL-04-03 and WR prototypes

Found 2026-10-08 by independent review V13 (CC-WR-RECONFIRM, Q8), and
reproduced on an unmodified tree. `RS_RECORD.schema.json`
`#/$defs/suppliedGuidance/allOf/2` uses the keyword `if`. DEL-04-03's
`minischema` does not support it, so DEL-04-03 `run_prototype.py` and WR
`wrproto.py` exit 1 ("unsupported keyword 'if'") before running any check.
The keyword entered with the CC-RS-WR-SUPPLY-FIT candidate (checkpoint
`0a2ed81b47`), which was checked with the installed `jsonschema` rather
than `minischema`. The App's validator, `jsonschema`, is unaffected, and
App tests pass.

Owner: DEL-04-03 (RS). Options: rewrite the rule with `anyOf`/`not`, or add
`if`/`then` to `minischema`. The App copy must follow either way. Until
then, the Design prototypes do not run as evidence.

## CI-24 (J8) Re-confirmation and Refine without a selection: implementation notes

Found 2026-10-08 by the J8 TASK of `APP-V4-GROUP-A-20261004`, implementing
the adopted CC-WR-RECONFIRM: WR §4.8 RC-1…RC-10, §4.6 RF-1, and the change
record's "App implementation items". No Design or schema file was changed.

- **(a) Where "selectable in this process" lives.** RC-2 makes ‹k› selectable
  only while the App holds the result of its registration (G-4) or
  re-confirmation (G-4R). The library owner keeps an in-memory set, filled only
  by its own hot commits. Root's `WorkflowReviewContext.registered` values hold
  the selectable revisions. Both end with the process, and neither is rebuilt
  from disk. DS-4 "select it instead" and RC-5 (d) read the owner's set. LS-1
  "as read" (ledger line, A15 record with the same bound content, store
  recompute) only gates the DS-8 offer (V13 R2-N2).
- **(b) Attempt journal placement (X-1, X-2).** WR §5.2 names an "attempt
  journal (App-kept)" without a location, and X-1 reads "each library's
  attempt journal". The App writes one journal file per *stored*
  re-confirmation at
  `<library>/.chirality/.workflow-staging/attempts/<sha256 of the A15 record id>.json`.
  This is inside §3's App-written, temporary staging area. The file is
  removed when the attempt closes. X-2 runs when a library owner is opened (in
  Root, once per library per process). It takes the ledger lock, then lists
  the journal directory and treats a journal that has gone as already closed
  (V15 F8). It rereads the ledger for a line citing the A15. If one exists it
  writes nothing; otherwise it writes *not completed* "process lost before
  re-confirmation committed", but only if the App's RC-9 reader would accept
  that line. If not, it writes nothing, keeps the journal and reports
  "X-2 pending" with the exact cause (V15 F1). It never completes a
  re-confirmation. Its outcomes appear in the Root snapshot's
  `libraries[].reconciliation`. For the WR owner: name the journal location.

  **Second App process (corrected after V15 F1; the earlier text understated
  it).** A journal is visible outside the lock only when the attempt is
  pending: the append failed or was uncertain, or the journal's own
  publication failed after the file was visible.
  - If a second App process opens the library then, its X-2 closes the
    attempt as lost and writes *not completed* citing the A15.
  - When the first process continues, G-1R finds the ledger already citing its
    A15. It appends nothing and ends the attempt *not completed* in that
    process, naming the line ("already has ledger line ‹n›"). ‹k› is not held.
  - So one act keeps one ledger line (RC-7, RB-8), and the ledger stays
    readable.
  - The person's act had no effect and they review again; a second review and
    A15 re-confirms.
  - Tested: `v15_p2_second_process_x2_then_continue_keeps_one_line_per_act`,
    through the `storage::fail_directory_for_test` hook.
  - **Exception (V15-R1 R1-1, open).** The ending above holds only when the
    first process's attempt is not in *Intended*. If its append failed
    without writing anything, the attempt is *Intended*. On every Continue
    it then takes the intended-line path, is refused on `ledger_seq`, and
    reports "registration ledger durability uncertain; same hot attempt
    retained" for as long as the process runs. This is safe: there is still
    one ledger line for the act, the ledger stays readable, and ‹k› is not
    held. But it never shows the definite *not completed* line already in
    the ledger. The repair is to fail on the intended path with the same
    "already has ledger line ‹n›" reason, with the reviewer's probe P6 as a
    test. It is open as a follow-up.
- **(c) Registration X-2 is still absent.** The App keeps no attempt journal
  for a *registration* (F15). A registration lost after G-3 and before G-4
  leaves its store folder and no ledger line, as before J8.
- **(d) F14, rollback and version skew.** G-1, G-1R and RB-3 (b) now compare
  the slot's latest *registered* revision, not the whole slot. *Re-confirmed*
  and *not completed* lines therefore never fail a concurrent attempt or stale
  a review. Once a *re-confirmed* line exists, an App binary built on the
  preimage WR schema refuses the whole ledger (`read_ledger` →
  `wr_validate("library_entry")`). That is acceptable for development builds.
  Rolling back to such a binary needs the *re-confirmed* lines set aside by
  hand.
- **(e) A single in-place registration is refused by the AAC offer schema
  (found, not introduced).** WR's single in-place entry (DS-7) goes out as an
  `a15_descriptor` with an `entry:` reviewed reference. The adopted
  `aac.offer.schema.json` `allOf/6` requires the `draft:` form for an
  `a15_descriptor`, so `compose_a15` refuses it. Two or more in-place entries
  (`a15_multi_descriptor`) work. The RF-1 test therefore registers in place
  with two entries. For the AAC and WR owners: admit `entry:` for a single
  in-place `a15_descriptor`, or route DS-7 through another form.
- **(f) Native statement and buttons (AAC §4.2 re-confirmation): J6's, now
  integrated.** J8 does not write the native statement or dialog code.
  `a15_native.rs` and the J6 dialog code in `act_control_a15.rs` are as J6
  merged them (integration head `9d1e0bb0cd`, merged into J8).
  - **What J8 supplies:**
    - the descriptor's wording "re-confirm workflow revision for use",
      disposition *re-confirmation*, re-confirm purpose and `reconfirms`;
    - the offer that `compose_a15` builds from them unchanged;
    - the review presentation's `entries[0].reconfirmation.statement`.
  - **What J6 does with them.** J6's `a15_variant` selects the
    re-confirmation statement when the descriptor kind is `a15_descriptor` and
    the disposition is *re-confirmation*. The statement reads "Re-confirm
    revision ‹short k› of ‹origin›:‹name› for use in this App session. This
    registers no new revision." It has no "Registering makes …" sentence. The
    owner's three-button layout (OWNER_DECISIONS, 2026-10-08; V15 F6) then
    gives [Don't re-confirm (default)] [Re-confirm] [Cancel], where only
    "Re-confirm" acts.
  - **Tests.** Journey step 9 checks, on the combined code, that the
    descriptor the DS-8 path composes selects that variant:
    - the act label is "Re-confirm";
    - the statement opens with the re-confirm wording and contains the
      re-confirm sentence for revision three;
    - no registration sentence appears;
    - a registration keeps "Register".

    J6's `reconfirmation_descriptor_has_its_own_statement_and_act_label` also
    passes.
  - **Limit.** No native witness of the dialog has been taken; the tests use
    the synthetic event.
- **(g) Capture outcome not written.** `aac.capture-evidence` now admits the
  entry outcome *re-confirmed*. The App writes no capture entry outcome for
  any registration, so none is written for a re-confirmation either. The
  ledger line and Root status carry the outcome.
- **(h) Base freshness interacts with G-6R (CI-21 (c)).** G-6R rewrites the
  draft's App-kept base record. A second review of the same draft taken
  before that commit then goes stale ("App-kept base changed since review").
  At G-1R the WR checks run first, so a concurrent re-confirmation of an
  already selectable ‹k› reports "already selectable in this App session".
- **(i) RF-1 Root route.** `WorkflowRootSession::refine_registered(name,
  revision)` and the `workflow_refine_registered` command call
  `LibraryOwner::refine_from_store`. The owner recomputes the store, makes the
  draft (D-1: never overwrites), and records ‹k› as the App-kept base (on
  failure the copy is removed, as in V11 J5-2). It makes no selection.
  `create_selected_draft` (from a hot selection) is kept.
- **(j) Not touched.** V13 R2-N1: WR's LS-4 row still offers "Review to
  register", while a draft with an LS-4 revision's bytes reviews as DS-4 with
  the restore route. That is left to the WR owner. U-WR-21 (re-confirmation
  from the listing without a draft) stays deferred.
- **(k) An unreadable act log is a read limit, not LS-4 (V15 F4).** WR LS-4
  names "A15 record missing or bound to other content". The App separates a
  third case: an act log it cannot read completely (an unreadable or invalid
  line anywhere, a sequence gap, an I/O error).
  - At review, ‹k›'s standing cannot be read as LS-1, so the review is DS-4
    with that exact cause and DS-8 is not offered. As before, any unreadable
    line in the library act log, even one unrelated to ‹k›, blocks DS-8.
  - At G-1R, after the person's act was captured, the attempt stays *pending*
    with the cause, and no ledger line is written. Once the log reads again,
    the same attempt continues. A missing record, or one bound to other
    content, still ends the attempt *not completed*.
  - Tested: `v15_f4_unreadable_act_log_keeps_g1r_pending`.
  - For the WR owner: confirm that a read limit at G-1R is "pending", as for
    an unreadable ledger.
- **(l) Listing of registered revisions (V15 F5; WR §4.6 LS-1 note, §5.4).**
  Each library in the Root snapshot gains a `registered` list: name, sequence,
  revision, registration time, disposition, and the label "registered —
  re-confirm to use in this App session", or "registered — selectable in this
  App session" when this process holds the result. The workflow panel shows
  the active library's rows, each with a Refine action (RF-1), so the content
  identity need not be typed. The list reads the ledger only. It does not
  check LS-1; Refine checks it.
- **(m) RF-1 failure cleanup (V15 F3).**
  - RF-1 copies exactly the store snapshot that `standing_as_read` verified.
  - The copy uses the store's exclusive, self-cleaning writer
    (`publish_reserved_store`).
  - Any later failure removes the App's own copy, using the exact-bytes check
    (sync of the copy or its parent, or recording the base). So RF-1 leaves no
    draft without an App-kept base.
  - Tested: `v15_f3_rf1_removes_its_copy_on_every_failure`.

## CI-25 (J8, V15 F1) WR G-1R "registered line changed or missing" against RC-9

Found 2026-10-08 by independent review V15 (probe P5) of J8. No Design file was
changed.

- **The WR rule.** WR §4.8 RC-6, G-1R: when the registered line ‹ledger_seq›
  has changed or is missing after capture, write *not completed* "registered
  line ‹ledger_seq› no longer reads as reviewed", citing the A15.
- **The conflict.** RC-9 requires that every line with disposition
  *re-confirmation*, a *not completed* one included, name in `reconfirms` an
  earlier *registered* line of the same slot, with the same tuple and
  sequence.
  - If line ‹ledger_seq› was removed, or no longer reads as *registered* for
    ‹k›'s tuple and sequence, no *not completed* line can satisfy RC-9.
  - If the App wrote one anyway, its own reader would refuse the whole library
    ledger: every review, registration, Refine and X-2, until a hand repair.
  - A related path has the same result: when the line no longer reads as
    registered, the slot's latest also changes, and G-1R's "slot moved on"
    *not completed* line runs into the same refusal.
- **What the App does.**
  - Before every append of a line with disposition *re-confirmation* (G-1R
    and G-2R/G-3R failures, G-4R, the in-process retry and X-2), the App runs
    its RC-9 reader over the ledger as it would then read.
  - If the reader would refuse, the App appends nothing. The attempt stays
    *pending* in the process, with the cause "re-confirmation line not
    appended: the App's RC-9 reader would refuse it (…)".
  - The person's act stands, recorded in the act log, with no effect. ‹k› is
    not selectable.
  - A change that still leaves ‹k›'s line reading as registered for its tuple
    and sequence (for example a changed `written_at`) is written *not
    completed* as WR says.
  - X-2 likewise keeps a journal whose *not completed* line would breach RC-9,
    reporting "X-2 pending" with the cause.
  - Tests: `v15_p5_g1r_line_no_longer_registered_appends_nothing`,
    `v15_p1_x2_never_appends_a_line_its_reader_refuses` and
    `v15_f2_g1r_registered_line_changed_is_not_completed`.
- **For the WR owner.** Rule on the case, for example:
  - G-1R ends the attempt without a ledger line when RC-9 cannot be met (the
    act log keeps the act); or
  - RC-9 admits a *not completed* re-confirmation line whose `reconfirms` no
    longer resolves, which the reader then reports instead of refusing; or
  - another form.

  Until then, the App's behaviour above stands. It is stricter than WR: it
  never writes an unreadable ledger.


## CI-26 Group B full EXP support identity versus record fields

- **Found:** 2026-10-08 by Group B first-slice TASK while implementing the
  offline EXP/PKG file checker; run APP-V4-GROUP-B-20261008.
- **Source:** DEL-09-01 EXP §4.4 defines a support revision as its version,
  all three schema IDs and the prototype digest. The EXP result schema carries
  its own `schema_id` and optional `prototype_digest`; PKG's identity schema
  carries only the EXP version in `support_revision`.
- **Preserved legacy behavior:** schema validation preserves those exact fields
  and optionality. The new package-link check additionally requires the pinned
  prototype digest under §4.4, checks result schema/version and matching package
  version, and reports maintained tool/rule/source identities separately. It
  claims only this partial file-consistency check, never complete support
  admission or qualification.
- **Owning route:** DEL-09-01 and DEL-01-06 design owners confirm how a complete
  M1 support identity is bound across package and result records before full M1
  reliance (Group B B3). Any changed interface uses a named reviewed change and
  consumer propagation; no schema or Design change was made by that original slice.

- **CC-EXP-SUPPORT-IDENTITY-01 scoped disposition:** additive
  `EXP-SUPPORT-BINDING-v1` is implemented for independent review and named
  technical adoption. Its canonical EXP Design supplement is
  `DEL-09-01/Design/support-identity-v1/METHOD.md`; PKG receives it through
  `DEL-01-06/Design/SUPPORT_IDENTITY_BINDING_V1.md`. The unchanged EXP-v0.2
  tuple and canonical source bytes are identified at prior publication merge
  `09106477e351c6e5bde85259c55a00cc8fc5f7f5` (PR #1077). The new method has a
  distinct version and becomes effective at the reviewed merge of this named
  contribution; authoring or checking it before merge does not adopt it.
- **Initial consumer cohort:** `app/examination/support_identity/canonical.py`
  fixes declaration/method/schema/PKG supplement selection outside record
  input and performs complete exact-byte result/review/change/current-package
  joins through unchanged validators. A record writer cannot mint publication.
  Current producer declaration and historical correspondence remain distinct;
  neither authenticates actual producer use. All prior schemas, prototypes,
  proposed checker bytes and source locks are preserved.
- **Closure boundary:** the reviewed named technical merge closes CI-26's
  representational gap and this explicit consumer cohort, recorded in
  `AgentRuns/APP-V4-GROUP-B-20261008/support-identity-adoption/`. It does not
  establish complete M1 runner/native qualification, M2/M3 witnesses, or
  SQ/native-form/S4 receiving adoption. Those consumers retain their existing
  partial basis until their separately identified receiving work; no blanket
  adoption or qualification follows from a consistent file join.

## CI-27 Full-distribution verification identity and PKG record coverage

- **Found:** 2026-10-08, Group B B2 input inspection and separately commissioned
  DEL-01-01 A-IN investigation; run APP-V4-GROUP-B-20261008.
- **Source:** HOSTING §7 and U-08/U-17 leave qualified distribution identity
  and composition/launcher selection unresolved. PKG v0.2 records the regular-file
  manifest/counts and Mach-O identities but cannot express the complete modes
  and directory inventory needed by the proposed full-tree comparison.
- **Current bounded behavior:** offline B2 inventories/stages an explicitly
  supplied tree and records preparation facts against existing v0.2 definitions.
  Neither matching inventory nor the development main-binary digest establishes
  verified runtime standing, a qualified expected reference or FP-2/W-4.
- **Owning route:** HELP_HUMAN coordinates DEL-01-01 and DEL-01-06 named
  CC-HOSTING-DISTRIBUTION-01, including versioned successor identity records and
  verifier/consumer propagation. The A-IN proposal in
  execution/_Coordination/AgentRuns/APP-V4-GROUP-B-20261008/distribution_input/
  is investigation, not adopted Design. Supplier-reference qualification must
  remain distinct from packaged-candidate qualification to avoid circular
  reliance on FP-2. B2 preparation can continue; FP-2/W-4 waits for the reviewed
  Design, qualified expected input and connected implementation.


- **Receiving disposition — CC-HOSTING-DISTRIBUTION-01:** the in-place amendment
  at `4c5f691c82` is superseded for integration by explicit proposed-successor
  staging. Current HOSTING/PKG contract bytes and all three consumer source locks
  remain on accepted bytes preserved at `45796bc`; no bare repin or new-method
  support claim. Proposed inventory schema/model rejects malformed digests.
  See `execution/_Coordination/AgentRuns/APP-V4-GROUP-B-20261008/distribution_integration/INTEGRATION.md`.
  CI-27 remains OPEN: Group B graph A-IN-S1…S5 assigns versioned contracts,
  connected implementation, reference qualification, consumer joins and final
  packaged witness. Staging satisfies none of those successor obligations.

## CI-28 SQ J-2 omitted its already required ST-4 stimulus

- **Found:** Group B B7 preparation, 2026-10-08. SQ §3.1/§3.4 and ST-4
  staged_at required J-2 delegation, while its step-map stimuli array was empty.
- **Disposition:** named CC-SQ-J2-ST4 b66d0b16f2 independently reviewed READY
  and integrated by manager as d6bcee8ce6 under the authorized faithful-correction
  scope. J-2 now carries ST-4; counts, order, schema and rule semantics unchanged.
  The definition checker passes 119 checks; all 17 existing vector outcomes match
  their prior sets. B7 consumer adoption is explicit in 8d05714c84 and awaits
  final combined review. No examination or native result is inferred.
- **Receiving route:** DEL-11-03 owner assesses its pinned SQ prose/example
  identities; historical fixtures stay frozen. Existing actual dossiers, if
  any, require the examiner's EXP §6.2 affected-claim assessment. Group E's
  receiving notice is carried in the Group B work graph, not automatic adoption.

## CI-29 Wholly unavailable sources in a connector route account

- **Found:** 2026-10-08 by independent Group C source preparation;
  run APP-V4-GROUP-C-20261008.
- **Source:** DEL-07-02 CONNECTOR_FALLBACK §7 says a missing or unreadable
  source produces a gap with its responsible party and leaves the affected
  part unsupported. ScopeOfWork REQ-002 and VER-002 include unavailable
  underlying sources. The current connector.route-account schema requires
  `sources` with `minItems: 1`; §4 describes each source read with its revision
  and digest. A wholly unavailable source set cannot be represented by
  inventing a successful source read.
- **Current bounded behavior:** C1 computes semantic standing and identifies
  question parts needing the source route. It writes no route account and
  changes no schema, source identity or criterion. Missing evidence remains
  missing; this issue does not prevent the bounded in-memory slice.
- **Owning route:** Group C C3, DEL-07-02 source-owner design treatment with
  affected PEC/Domains receiving and later fleet/examination consumer review,
  before persistent account writing. Resolve through a named reviewed change;
  no product meaning or group order is changed here. A consequential choice
  returns through HELP_HUMAN to the owner. No fabricated source entry or
  weakened test may conceal the mismatch.
- **C3 source successor:** named CI-29 / CFB-v0.3 defines route-account
  format 0.2 in the additive `Design/CONNECTOR_FALLBACK_v0.3.md` and
  `connector.route-account.v0.2.schema.json`. With no successful source reads,
  it requires empty facts and supported conclusions, nonempty gaps with
  effects/responsibility, and unsupported conclusions. Historical 0.1 bytes,
  pins and evidence are unchanged. Source preparation is not consumer adoption
  or persistent behavior; independent source review is READY at `96791613ed`,
  with combined integration review and placement disposition separate.
- **Consumer and placement account:** Group C
  `AgentRuns/APP-V4-GROUP-C-20261008/C3_DESIGN_TREATMENT.md` identifies
  PEC, Domains, fleet, examination and later research receiving work. O-D
  placement was subsequently selected through C3-PLACE-01; this correction adds no
  requirement for Group D software and changes no accepted group order.
- **Placement follow-through:** C3-PLACE-01 / CRP-v0.2 is technically selected
  in the Group C `C3_PLACEMENT_ADOPTION.md` after repaired independent review
  and DEL-06-01 concurrence. It selects project-local connector records and
  opened-directory capability containment with explicit rename residuals;
  no continuous-path safety or finished persistence is claimed. CI-29's
  source-only successor merged in PR #1130; backend behavior remains C3-P.
- **Persistence implementation:** the bounded C3-P backend now has a tested
  writer, cold discovery and reference reconciliation for caller-supplied
  schema-valid accounts; independent repair review is READY at `f1ff1699e0`,
  with final combined-head READY at `2ecde9055d` and all selected CI passed;
  PR #1137 merged as `412cf7fa01`. Initial code passed 25 checks but failed two independent temporary-name
  substitution checks. Named CRP-R2 / CRP-v0.3 selects exclusive no-replace
  rename with no automatic unlink, exact intended binding checks and explicit
  late-substitution uncertainty. The repaired author candidate `8f1195761d`
  passed 31 connector checks; independent review passed those plus three
  substitution probes. `C3_PERSISTENCE_REVIEW.md` preserves the original
  finding; a passing rerun alone does not establish its repair. This backend
  does not reconstruct the question from real sources, establish source truth,
  perform duties, wire providers, or supply UI/connected witness behavior.

## CI-30 Executed SQ dossier/result/review receiving contract

- **Owner and scope:** DEL-09-02 receiving with DEL-09-01 support-method
  adaptation; Group B manager owns this entry. HELP_HUMAN reserved CI-30 in
  the active coordination after checking current main and Group C.
- **Gap:** existing preparation captures canonical support identity, but the
  six-record EXP/PKG selection does not define executed SQ dossier, direct-step
  and primary-review byte joins. Reusing it indiscriminately would impose
  unsupported package/change obligations on native_development.
- **Named technical change:** CC-SQ-EXP-RECEIVING-01 selects a separate fixed
  SQ receiving route, exact dossier/direct-step/review mappings, explicit
  review-set file mapping and citation-conditional package/change attachments.
  The direct-step case/scenario convention is newly selected for this route,
  not a retroactive legacy schema rule. Existing six-record consumers remain.
- **Source disposition:** HELP_HUMAN selected reviewed proposal
  762d1ba2d03d5d2b809c7631ce009fa8a1b6fdfc as the bounded Design target.
  Additive DEL-09-02 Design/sq-exp-receiving-v1/RECEIVING.md and DEL-09-01
  Design/sq-exp-receiving-v1/METHOD_ADAPTATION.md were independently READY at
  bb10cf3190b1f0593eb871394aae58ce967e22bd, review
  5517c203162ee1af76e60b6a0b31353413b14192. This is technical disposition
  conveyed through the parent, not personal owner review or qualification.
- **Implementation state:** bounded connected receiver authorized after source
  review; implementation, independent code review and integration remain open.
  Missing review/attachments stay incomplete or unsupported as specified;
  contradictory mappings refuse. Failed/not-run/history retain their meaning.
- **Limits and propagation:** no actual examination, native/supplier witness,
  package qualification, generic evidence resolver or release. No S3/signing
  prerequisite is added to native_development. DEL-11-03 handoff rights and
  DEL-01-06 conditional package contract are unchanged. Exact source/custody
  records: AgentRuns/APP-V4-GROUP-B-20261008/sq-result-receiver-adoption.
