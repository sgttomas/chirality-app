# App v4 contract issues

The CI-1…CI-9 reports below retain the original walking-skeleton findings from
`APP-V4-GRAPH-CLOSURE-20261004`. Run `APP-V4-GROUP-A-20261004` resolves their
current path through named reviewed Design changes and tested code. Native
qualification and later Group A consumers remain separate obligations.

| Issue | Current P0 disposition and evidence |
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

Canonical review and command evidence lives in this run's `changes/`,
`reviews/` and `validation/`. The Group A work graph carries incomplete
consumer/native/qualification work. CI-10 below remains an open custody issue.

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
- **Unfinished required work:** trustworthy persistent replay and protected capture-origin proof remain in Group A I3. SEAL-2 selection requires the human App implementation owner's concrete decision; CAPTURE_CUSTODY_DECISION.md is preparation, not acceptance. Packaging/signing qualification stays with Group B at its actual point of need; moving the obligation does not complete it.
