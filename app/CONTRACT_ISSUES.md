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
