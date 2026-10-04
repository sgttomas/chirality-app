# Practitioner validation and feedback disposition

- **Contribution:** DEL-09-12/PV-v0.2, the first Design file of DEL-09-12, frozen as unit **EU-F4**. PV-v0.1 was frozen but not yet sent for review; PV-v0.2 adds the coordinator's checker audit (§8) and nothing else. The records, schema and examples are unchanged.
- **Status:** DRAFT DEFINITION — proposed, not accepted. Beside it are:
  - the PROPOSED schema `pv.practitioner-validation.schema.json`, with five record kinds;
  - illustrative examples `pv.examples.valid.json` (7) and `pv.examples.invalid.json` (14).

  The prototype is under `_Coordination/AgentRuns/APP-V4-DESIGN-PASS-4-20261003/F/pv/` (RUN/F/pv): `pvlib.py` builds the current real records and holds the rules; `check_pv.py` checks them. The real records state what is true now: **no validation is agreed, and no practitioner use has occurred**. Every example is labelled ILLUSTRATIVE or INVENTED and is not a practitioner observation (VER-003).
- **Run and owner:** `APP-V4-DESIGN-PASS-4-20261003`, tranche 2; owner O-F (Type 2, Claude Opus 5.5); 2026-10-04.
- **Serves:** OUT-001, OUT-002, OUT-003; REQ-001…REQ-006; designed cases for VER-001…VER-006 (§8).
- **Rulings (cited by ID):**
  - R23-32: F-R3 (practitioner validation is not a replacement condition), F-R12 (DEL-09-12 keeps its own observation record, not an EXP outcome), F-R13 (observations route to their owning deliverable through the ScopeLedger), F-R14 (always "OI-016 (App v4)" or "SWBPIPE OI-016"); P-2, P-3 and P-6 as the person's acts;
  - R23-33 (EXP's candidate identity);
  - R23-44.
- **ScopeOfWork pin (R23-5):** `ScopeOfWork.md` sha256 `40eaf09fd80f9f3908af710a865b0204948b12f26e71b399cdecfdc3ad598bd1`. This is the INIT contract; no SCA-V4 block changed it. TBD-002 reads OI-001 and OI-002 as open, and D2/D3 ruled them for the App; the wording is carried to the next amendment (R23-11).
- **Basis and suppliers** (sha256; commit holding the bytes; all clean in the working tree):
  - `docs/EXAMINATION.md` `471798bc2f2dc0202ae40d9d5cf033a22ae41af2a0afdf58032cf37a687957d0` (§1, V4-EXM-40…42);
  - `docs/OPERATING_METHOD.md` `98836b5240ed235ec2ad38b08a9525dc9f2b366145c0736f7c70d22c1c93c5dd` (V4-OPS-20…23);
  - `_Decomposition/ScopeLedger.csv` `d813629785ecfcca8dba613c908fd64a66df8849928523587bdd6b58458b935f` (`230bf1e646`);
  - `_Decomposition/Open_Issues.csv` `9c2d916c277f8ce4b847c9c532822d0566e59517ba9e0a86b650fe0450f3515d`;
  - DEL-09-01 EXP-v0.2 `EXAMINATION_PROTOCOL.md` `ff0187dafd9e1f0268a19f9266914bdba64f39e0c8befdcaf20d3da7a7206a93` (§1, §3.3);
  - DEL-10-02 UC `UNDERTAKING_CONTROLS.md` `da0176cbf2ae806dc1c4e98b9fbd8bb7af635639c7cac4e114b7da42d0d8b533` (`68f83d6b20`; §5, §7, §9).

  The prototype reads the committed suppliers from git at the build commit (`b2fbfdbac84368c74a33e555815452fb8fcb199c`), so no vendored copy is needed (R23-44 concerns in-progress files).
- **Labels.** *States* means a file says it; *inference* marks this file's reading; PROPOSED marks a rule introduced here.

## 0. What this deliverable is

V4-EXM-40 says: "The owner uses v4 for real design work of the owner's choosing over an agreed period, in both the Chirality App and SWBPIPE, with invented or owner-controlled data." DEL-09-12 arranges that validation, preserves what actually happens, and routes what is learned. It keeps three record kinds of its own (F-R12), plus two hand-overs:

| Record | Output | What it holds |
|---|---|---|
| `pv_arrangement` | OUT-001 | Both expressions, their candidates, the owner's selected activities, material, the period, and the owner's agreement as a faithfully recorded act |
| `pv_observation` | OUT-002 | One session of the owner's real use: expression, candidate, configuration, date, conditions, V4-EXM-41's four aims as observations, limits |
| `pv_disposition` | OUT-003 | Observation → owning commitment → recipient → proposed treatment → decision |
| `method_note` | hand-over to DEL-10-02 | A method observation in DEL-10-02 UC §5's own field set (UC §9) |
| `practitioner_standing` | hand-over to DEL-11-03 | Standing, agreement reference, observation count; `is_replacement_condition: false` |

**Not here:**
- an examination outcome, verdict or score of any kind (F-R12; REQ-002: "without numerical pass scores or an assumed favorable fitness conclusion");
- choosing activities or a period (P-2);
- the use itself (P-3);
- changing a requirement or a manual (feature owners; DEL-10-01/10-02; OI-020; P-6);
- EXP result records. EXP §3.3's `activity: validation` is not used by DEL-09-12. That is a note for O-B; EXP is not changed.

## 1. Act boundary (REQ-003, REQ-006; CLM-001…CLM-005)

| Act | Who | Here |
|---|---|---|
| Agreeing the period and selecting activities | The owner. OI-016 (App v4): Owner "Owner", "Agree period and owner-selected activities", "Before practitioner validation in use" (P-2) | Recorded only from the owner's own act: actor the owner, a named recorder, custody (§3.1). A coordinator may **propose**; a proposal is never agreement |
| Using v4 and judging fitness | The owner as practitioner (CLM-002; V4-EXM-41: "the owner's measure"; P-3) | Observed and recorded; never inferred from tool success, a fixture, or an automated pass |
| Requirement changes and focused checks | The feature owners | Routed (§4), never made |
| Method and manual changes | DEL-10-02 at the stage discussion (UC §7, where the owner decides); OI-020 before any manual revision (P-6) | Handed over as UC §5 notes |
| Unresolved operation policy, SWBPIPE construction | Owner with App/SWB contract owners; the SWBPIPE session (DEP-001) | Carried, not decided |
| Replacement; adoption and retirement | The owner (P-1); the owner with affected consumers (OI-024) | Standing handed to DEL-11-03; validation is not a replacement condition (F-R3) |

## 2. Interfaces

| ID | Input or output | Other end | Arc (DAG-004) | Point of need | If absent |
|---|---|---|---|---|---|
| I-1 | The owner's agreement on period and activities | The owner (OI-016 (App v4)) | DEP-09-12-007, not topological | Before validation in use | Arrangement `not_agreed`; nothing counts as validation |
| I-2 | Identified candidates for each expression | DEL-09-02 (App), DEL-09-07 and SWBPIPE (host); DEP-001 | DEP-09-12-008, -009 | Before use in that expression | That expression `blocked`, with its cause |
| I-3 | Adopted operation policy for recording acts | DEL-04-01 ACT | DEP-09-12-011, admitted | When an observed session involves human acts | Acts are recorded as ACT names them; no unsettled class is decided |
| I-4 | Examination support | DEL-09-01 EXP | DEP-09-01-029, admitted | Observation records | Candidate identity uses EXP `candidate_subject` (R23-33); no EXP result record is written (F-R12) |
| I-5 | The owner's use records and observations | The owner | DEP-09-12-010, not topological | Each session | No observation exists; none is invented |
| O-1 | Method notes (UC §5 fields) | DEL-10-02 | DEP-09-12-012, admitted | When a method observation exists | — |
| O-2 | Feature and workflow dispositions | The owning deliverable via the ScopeLedger | DEP-09-12-013, not topological (target UNKNOWN in the register) | When an observation implicates a commitment | Recipient `unresolved`, reported |
| O-3 | `practitioner_standing` | DEL-11-03 | DEP-11-03-009, admitted | Each packet version | DEL-11-03 records *not supplied* |

O-3 supersedes DEL-11-03's first-cut `$defs/practitioner_standing` (S-5 in RP-v0.5 and RP-v0.6). DEL-11-03 adopts it at its next revision. DEL-11-03's paths are not edited by this unit. The values the first cut reads (open issue, standing, no agreement and no observation while not agreed) are carried identically (`check_pv.py` K-12).

## 3. Records

### 3.1 Arrangement (OUT-001; REQ-001; VER-001)

- **States:** `not_agreed`, `proposed`, `agreed`, `in_use`, `ended`. **Nothing before `agreed` counts as validation.**
- **Agreement.** `agreement` must be null in `not_agreed` and `proposed`. In `agreed`, `in_use` and `ended` it must be an owner act with:
  - actor "the owner";
  - a recorder other than the owner;
  - `recorder_stated_by_record`;
  - `record_ref`, `exact_text` and custody.

  This is the project's OWNER_DECISIONS form, as for the replacement decision (F-R4).
- **Expressions.** There are always two, `app` and `swbpipe`. Each has a candidate (EXP `candidate_subject.app_candidate`, or null), activities, material (`invented`, `owner_controlled`, or null) and availability (`available`, `blocked` or `not_yet`, with its cause).
- **Activities.** Each carries `selected_by` (`the owner` or `proposed_not_selected`). **PV-R2 (PROPOSED):** an agreed arrangement has only owner-selected activities, and every available expression has at least one.
- **Period:** `one_for_both` or `per_expression`, as the owner chooses at the agreement. V4-EXM-40 says "an agreed period"; the record allows either, and does not presume one.

### 3.2 Observation (OUT-002; REQ-002; VER-002)

- **Fields:**
  - expression, candidate, configuration (model and model server required; Codex pin, route and host candidate where they apply), date, activity;
  - observer "the owner", and the recorder;
  - conditions, limits;
  - `standing`: `actual_use`, or `illustrative` for examples.
- **The four aims** of V4-EXM-41: `confidence_for_attention`, `workarounds`, `perception_gaps` and `records_missing_or_unused`. Each has `coverage` (`observed` or `not_observed`) and a list of source-linked statements. "Not observed" never carries statements, and it is never read as "no issue" (REQ-002: "Absence of an observed issue does not prove unobserved use").
- **No outcome, verdict or score field exists** (F-R12). The schema is closed (`additionalProperties: false`). Unfavourable findings are recorded as found (AX-002).
- **PV-R1 (PROPOSED):** `actual_use` on an illustrative or unidentified candidate is refused. The placeholder test matches DEL-11-03's (RP-v0.5, unchanged in RP-v0.6), and like it is **keyword-based** (illustrative, invented, example, placeholder): a placeholder spelled otherwise would pass it.

### 3.3 Disposition (OUT-003; REQ-004; VER-004)

- **Kinds:** `feature`, `workflow`, `method`.
- `owning_commitment` carries the requirement or clause id and its source. A method disposition also needs the manual section and the work-graph node (V4-OPS-20).
- **Proposed treatment:** `proposed_revision`, `scoped_departure`, `no_change` or `successor_basis_proposal` (a possible v5.0 basis, V4-EXM-42, kept proposed until its own decision and adoption).
- **Decision:** `proposed`, or `decided` with actor, `record_ref` and scope. A decided disposition without its record is refused.

### 3.4 Routing (F-R13; PV-R3, PROPOSED)

- **Method** observations go to DEL-10-02 (UC §9).
- **Feature and workflow** observations go to the deliverables in the IN rows of `_Decomposition/ScopeLedger.csv` whose `ScopeItemID` is the reference, or whose `SourceRef` anchor is. Examples: `V4-EXE-01` → DEL-01-02; `V4-EXM-41` → DEL-09-12; `SOW-209` → DEL-09-12.
- When there is no IN row, the recipient is `unresolved` and is reported. It is never invented (VER-004: "An unresolved recipient or unmade decision is reported, not invented").
- PV-R3 refuses a recipient or route that differs from this lookup. It is checked on the real ScopeLedger at the build commit (K-10).

### 3.5 Hand-overs

- **`method_note`** has exactly DEL-10-02 UC §5's fields, read from UC at the commit (K-11):
  - id, node, date;
  - observer (the owner) and recorder;
  - conditions;
  - practice exercised;
  - class (`useful`, `ill-fitting`, `ambiguous`);
  - applied (`yes`, `no`, `partly`, `n/a`);
  - consequence;
  - evidence (the DEL-09-12 record);
  - inference;
  - proposed treatment (UC's four values);
  - disposition (`pending`, `settled by …`, or `applied locally by …`).

  UC §7 then takes the note to the stage discussion.
- **`practitioner_standing`** for DEL-11-03:
  - `not_agreed` forces a null agreement and zero observations;
  - `is_replacement_condition` is the constant `false` (F-R3).

## 4. The real records now (`F/pv/records`, built at `b2fbfdbac8`)

- **PV-ARR-1** (`not_agreed`). No agreement, no period, and **no activity proposed**: the activities are the owner's choice, and none could run before a candidate exists. Both expressions are `blocked`:
  - App: "no App v4 candidate exists: DEL-09-02's dossier is an illustrative example and nothing is built";
  - SWBPIPE: "no SWBPIPE candidate; the owner deferred the host joins (DECISION-3: 'defer the host joins'); OI-021 is open".

  The builder stops if OI-016 (App v4) or OI-021 is no longer OPEN in Open_Issues.csv at the commit, or if DECISION-3's text is missing, so the record cannot silently outlive its basis.
- **PV-STANDING-1** (`not_agreed`, 0 observations, not a replacement condition): the value DEL-11-03 should carry.

**Inference, not a decision.** Whether to prepare a proposal now (state `proposed`) is the coordinator's ordinary choice. A proposal has no use until a candidate exists, and preparing one invites no owner act. This unit therefore records `not_agreed`, with no proposal.

## 5. Sequence

1. When a candidate exists for an expression, the coordinator may prepare a proposal (`proposed`). Its activities are proposed and not selected.
2. The owner agrees, an act at OI-016 (App v4)'s point of need (P-2). It is recorded in OWNER_DECISIONS form, and the arrangement becomes `agreed`.
3. The owner uses v4 (P-3). Each session is recorded as a `pv_observation` (`actual_use`), and the state becomes `in_use`.
4. Each observation that implicates a commitment gets a disposition, routed by §3.4.
5. Method observations become UC §5 notes for DEL-10-02.
6. The period ends (`ended`).
7. The standing is handed to DEL-11-03 at each packet version.
8. A changed candidate or basis reopens the affected observations; prior observations stay as evidence of their own subject.

## 6. Failure behaviour

| # | What fails | Record left | Next |
|---|---|---|---|
| PF-1 | A session's candidate or configuration is not identified | No `actual_use` observation (PV-R1); a limit in the arrangement | Identify it first |
| PF-2 | An aim was not looked at | `coverage: not_observed`, never "no issue" | — |
| PF-3 | No ScopeLedger row owns the commitment | Recipient `unresolved`, reported | To HELP_HUMAN for routing |
| PF-4 | The owner's answer is ambiguous about period or activities | Arrangement stays `proposed`; the answer is quoted in `limits` | Never inferred |
| PF-5 | Open_Issues or DECISION-3 changes | The builder stops | The arrangement is rebuilt from the new record |

## 7. Open matters

| ID | Item | Owner | Point of need |
|---|---|---|---|
| U-PV-1 | The agreement on period and activities | The owner (OI-016 (App v4); P-2) | Before validation in use; possible only when candidates exist |
| U-PV-2 | Candidates for each expression | DEL-09-02; DEL-09-07 with SWBPIPE (DEP-001, OI-021; host joins deferred) | Before use in that expression |
| U-PV-3 | DEL-11-03 adopts `practitioner_standing` in place of its first cut | O-F, at DEL-11-03's next revision after RP-v0.6 (RP-v0.6 is a repair round and does not take it) | — |
| U-PV-4 | EXP §3.3's `activity: validation` is not used by DEL-09-12 (F-R12) | O-B, as a note | EXP's next revision |
| U-PV-5 | OI-020 before any manual revision proposed from feedback | The owner (P-6) | When one is proposed |

## 8. Verification (designed; `check_pv.py` 27/27 at freeze)

Each rule about the real records is one function in `check_pv.py`; each negative case N-1…N-14 breaks a real record (or, for F-R12 and UC §5, the schema text) in memory and runs the same function, naming the rule that must refuse it. The examples' cases (K-5, K-6) are kept.

| VER | Case | Held by |
|---|---|---|
| VER-001 | The real arrangement is `not_agreed`, with causes; an illustrative proposal and an agreed arrangement validate; a plan offered as agreement and a self-recorded agreement are refused; an agreed arrangement with unselected activities is refused | K-1, K-4, K-5, K-6 (invalid 3, 4; PV-R2) |
| VER-002 | An observation with four aims, no score or outcome; "not observed" holding statements is refused; actual use on a placeholder is refused | K-5, K-6 (invalid 1, 2, 9; PV-R1), K-7 |
| VER-003 | Illustrative cases are marked as such and are never practitioner observations; acts keep actor and recorder apart | Examples' `standing`; K-6 (invalid 4) |
| VER-004 | Observation → commitment → recipient through the real ScopeLedger; unresolved is reported; a decided disposition needs its record; a method observation goes to DEL-10-02 with section and node | K-10, K-6 (invalid 5, 6; PV-R3 ×2), K-11 |
| VER-005 | OI-016 (App v4), OI-021 and OI-024 carried; no invented period; validation is not a replacement condition; F-R14 qualification everywhere | K-4, K-8, K-9, K-12, K-6 (invalid 7, 8, 10) |
| VER-006 | Act boundary (§1) | Review |

**Claimed rules with a negative case on a real record:** schema: a plan offered as agreement (N-1), observations or an agreement while not agreed (N-3, N-4), a replacement condition (N-5), an unqualified open issue (N-6); PV-R2 (N-2); K-2 (N-12); K-3 (N-13); K-4 (N-5, N-8); K-7 F-R12 (N-9); K-8 F-R14 (N-6, N-7; K-9 tests the rule both ways); K-11 UC §5 fields (N-10); K-12 (N-11); K-13 (N-14).

**Without a negative case on a real record, or not enforced:**
- PV-R1 and PV-R3 apply to observations and dispositions, and no real one exists; they are refused only on the invalid examples (K-6: invalid 11 for PV-R1; 13 and 14 for PV-R3). K-10 runs PV-R3's routing on the real ScopeLedger, including an unknown anchor.
- PV-R1's placeholder test is keyword-based (§3.2).
- K-12 checks the open issue and the standing value; "no agreement and no observation while not agreed" is the schema's (N-3, N-4).
- An agreement's actor-not-recorder test is the schema's string comparison (invalid 4); a false recorder name passes.
- VER-006 (the act boundary) is by review.

## 9. Changes

| Version | Change |
|---|---|
| PV-v0.2 (2026-10-04) | Coordinator's checker audit: rules as functions of the real records; N-1…N-14 break them; covered and uncovered rules listed (§8). The placeholder test's keyword limit stated (§3.2). Records, schema and examples unchanged; record format PV-v0.1. Unit EU-F4, refrozen before review |
| PV-v0.1 (2026-10-04) | First Design file; unit EU-F4 (frozen, not sent for review) |
