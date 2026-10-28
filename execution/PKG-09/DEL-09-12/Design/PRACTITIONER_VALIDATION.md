# Practitioner validation and feedback disposition

- **Contribution:** DEL-09-12/PV-v0.4 (unit **EU-F4R2**): RV2's PV2-R1 (an owner act's recorder is never the owner in any case or spacing) and PV2-N2 ("design agent O-F"). The real arrangement's `prepared_by` changes, so the version steps; the record format stays PV-v0.3. PV-v0.3 (sha256 `16718ee59275e915b2ab124bbd6846f81b7ce8d13906d4492a03ec78e4f36871`, unit EU-F4R, commit `9ba5dfe49c`, READY) stays in git as history. PV-v0.3 was the repair of PV-v0.2 (sha256 `2240ab360eeb5e5f5ac5c6375e7bfe20b7805bb9943d517a5b980ce75e0708f4`, unit EU-F4, commit `0e3591a65d`) for RV2's review RV2-PV1 (PV1-R1 MAJOR; PV1-R2…R6 MINOR; PV1-R7 NOTE). Unit **EU-F4R**. The record format steps to PV-v0.3 (§9).
- **Status:** DRAFT DEFINITION — proposed, not accepted. Beside it are:
  - the PROPOSED schema `pv.practitioner-validation.schema.json`, with five record kinds;
  - illustrative examples `pv.examples.valid.json` (12) and `pv.examples.invalid.json` (29).

  The prototype is under `_Coordination/AgentRuns/APP-V4-DESIGN-PASS-4-20261003/F/pv/` (RUN/F/pv): `pvlib.py` builds the current real records and holds the rules; `check_pv.py` checks them. The real records state what is true now: **no validation is agreed, and no practitioner use has occurred**. Every example is labelled ILLUSTRATIVE or INVENTED and is not a practitioner observation (VER-003).
- **Run and assignment:** `APP-V4-DESIGN-PASS-4-20261003`, tranche 2; prepared by design agent O-F (Type 2, Claude Opus 5.5); 2026-10-04. In this file "the owner" is always the person; agents and deliverables are named as such.
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
| `practitioner_standing` | hand-over to DEL-11-03 | Standing, agreement reference, the actual-use observations' ids; `is_replacement_condition: false` |

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
| Requirement changes and focused checks | The feature owners (CLM-003), through the owning deliverable's own record | Routed (§3.4), never made. A decided disposition cites that record (§3.3) |
| Method and manual changes | DEL-10-02 at the stage discussion (UC §7, where the owner decides); OI-020 before any manual revision (P-6) | Handed over as UC §5 notes |
| Unresolved operation policy, SWBPIPE construction | The owner with the App/SWB contract owners and host policy owner (REQ-006); the SWBPIPE session (DEP-001) | Carried, not decided |
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

O-3 supersedes DEL-11-03's first-cut `$defs/practitioner_standing` (S-5 in RP-v0.5 and RP-v0.6). DEL-11-03 adopts it at its next revision. DEL-11-03's paths are not edited by this unit. **It is not identical to the first cut** (PV1-R5). Every first-cut field is present with the first cut's name, type, const and enum; `observations` is an array of observation ids, as the first cut reads it (PV-v0.1/0.2 emitted an integer count; PV-v0.3 matches the first cut). The stated differences are:
- `format` is `PV-v0.3`, where the first cut has the constant `RP-v0.1-first-cut`;
- `arrangement_ref` and `is_replacement_condition` are added. The first cut is closed (`additionalProperties: false`), so it refuses them.

DEL-11-03's first cut therefore refuses this record as it stands. Its next revision (U-PV-3) must take the format and the two added fields. `check_pv.py` K-12 recomputes these differences from the first cut at the commit, and validates the real record against the first cut with them undone.

## 3. Records

### 3.1 Arrangement (OUT-001; REQ-001; VER-001)

- **States:** `not_agreed`, `proposed`, `agreed`, `in_use`, `ended`. **Nothing before `agreed` counts as validation.**
- **Agreement.** `agreement` must be null in `not_agreed` and `proposed`. In `agreed`, `in_use` and `ended` it must be an owner act with:
  - actor "the owner";
  - a recorder other than the owner (never "the owner" in any case or spacing; PV2-R1);
  - `recorder_stated_by_record`;
  - `record_ref`, `exact_text` and custody.

  This is the project's OWNER_DECISIONS form, as for the replacement decision (F-R4).
- **Expressions.** There are always exactly two, one `app` and one `swbpipe` (schema: two items, each kind `contains`ed; PV1-R2). Each has a candidate, activities, material (`invented`, `owner_controlled`, or null) and availability (`available`, `blocked` or `not_yet`, with its cause).
- **Candidates by expression (PV1-R4; R23-33).**
  - `app`: `{app_candidate}`, EXP `candidate_subject.app_candidate`; no host.
  - `swbpipe`: `{host_candidate, app_candidate}`. `host_candidate` is EXP `candidate_subject.host_candidate`: the host build, or the DEL-09-07 LHQ candidate identification record that names it (I-2: DEL-09-07 and SWBPIPE supply it). `app_candidate` is the App candidate when one takes part, else null; the App candidate's role in V4-EXM-20 is the OI-013/014 residue, so it is recorded, not presumed.
  - Either is null while no candidate is identified.
- **An agreed arrangement (`agreed`, `in_use`, `ended`) has a candidate and material on every `available` expression** (schema; AC-001; PV1-R3).
- **Activities.** Each carries `selected_by` (`the owner` or `proposed_not_selected`). **PV-R2 (PROPOSED):** an agreed arrangement has only owner-selected activities, and every available expression has at least one.
- **Period:** `one_for_both` or `per_expression`, as the owner chooses at the agreement. V4-EXM-40 says "an agreed period"; the record allows either, and does not presume one.

### 3.2 Observation (OUT-002; REQ-002; VER-002)

- **Fields:**
  - expression, candidate (as in §3.1; a SWBPIPE observation always names its host candidate, PV1-R4), configuration (model and model server required; Codex pin and route where they apply), date, activity;
  - `arrangement_ref`, the arrangement and version the session ran under (`PV-ARR-n vN`);
  - observer "the owner", and the recorder;
  - conditions, limits;
  - `standing`: `actual_use`, or `illustrative` for examples.
- **The four aims** of V4-EXM-41: `confidence_for_attention`, `workarounds`, `perception_gaps` and `records_missing_or_unused`. Each has `coverage` (`observed` or `not_observed`) and a list of source-linked statements. "Not observed" never carries statements, and it is never read as "no issue" (REQ-002: "Absence of an observed issue does not prove unobserved use").
- **No outcome, verdict or score field exists** (F-R12). The schema is closed (`additionalProperties: false`). Unfavourable findings are recorded as found (AX-002).
- **PV-R1 (PROPOSED):** `actual_use` on an illustrative or unidentified candidate is refused. The placeholder test matches DEL-11-03's (RP-v0.5, unchanged in RP-v0.6), and like it is **keyword-based** (illustrative, invented, example, placeholder): a placeholder spelled otherwise ("TBD") would pass it. For SWBPIPE it reads the host candidate and, where present, the App candidate.
- **PV-R4 (PROPOSED; PV1-R3):** an `actual_use` observation ties to what makes it validation. Its arrangement (by `arrangement_ref`) must be supplied and `agreed` or `in_use`. The observation's expression must be `available` there. Its activity must be owner-selected for that expression. Its candidate must equal that expression's candidate. Nothing before `agreed` counts as validation (REQ-001; AC-001).

### 3.3 Disposition (OUT-003; REQ-004; VER-004)

- **Kinds:** `feature`, `workflow`, `method`.
- `owning_commitment` carries the requirement or clause id and its source. A method disposition also needs the manual section and the work-graph node (V4-OPS-20).
- **Proposed treatment:** `proposed_revision`, `scoped_departure`, `no_change` or `successor_basis_proposal` (a possible v5.0 basis, V4-EXM-42, kept proposed until its own decision and adoption).
- **The disposition is DEL-09-12's; the decision is not** (REQ-003, REQ-004, CLM-003; PV1-R1). DEL-09-12 (an agent) may route and propose. It decides nothing.
- **Decision `proposed`:** `proposed_by` only. A proposal carrying a decider, actor, recorder or record is refused (schema).
- **Decision `decided`:** `decider`, `actor`, `recorder`, `recorder_stated_by_record`, `recording_mode` (`direct capture` or `faithful recording`), `record_ref` and `scope` are all required (schema). The decider must be the one the case requires:

  | Case | `decider` | Actor and record |
  |---|---|---|
  | `feature` or `workflow` | `owning_deliverable` | `deliverable` names one of the recipients, and `record_ref` names that deliverable's own record (PV-R5). The actor is that deliverable's accountable party (CLM-003: feature owners) |
  | `method` | `owner_at_stage_decision` | Actor "the owner" (schema), at the DEL-10-02 stage decision (UC §7, "reserved to the person"), recorded in an OWNER_DECISIONS file (PV-R5). OI-020 still applies before any manual revision (P-6) |
  | `successor_basis_proposal`, any kind | `owner_with_affected_consumers` | Actor "the owner" (schema), plus `adoption_ref`, the adoption's own record, which must differ from the decision's `record_ref` (PV-R5). `adoption_ref` appears only here (schema) |

- **Recorder.** When the actor is "the owner", the recording is `faithful recording` and the recorder is someone else: never "the owner" in any case or spacing (schema; PV2-R1). Otherwise a `faithful recording` names a recorder other than the actor, and a `direct capture` names the actor as recorder (PV-R5). Both are string comparisons.
- An `unresolved` disposition stays `proposed` (schema).
- **PV-R5 (PROPOSED):** the cross-field parts of the above that the schema cannot express.

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
- **`practitioner_standing`** for DEL-11-03 (O-3, with its stated differences from the first cut, §2):
  - `observations` lists the actual-use observations' ids;
  - `not_agreed` forces a null agreement and no observations;
  - `agreed`, `in_use` and `ended` require an agreement reference (PV1-R3);
  - `is_replacement_condition` is the constant `false` (F-R3).

## 4. The real records now (`F/pv/records`, built at `b2fbfdbac8`)

- **PV-ARR-1** (`not_agreed`). No agreement, no period, and **no activity proposed**: the activities are the owner's choice, and none could run before a candidate exists. Both expressions are `blocked`:
  - App: "no App v4 candidate exists: DEL-09-02's dossier is an illustrative example and nothing is built";
  - SWBPIPE: "no SWBPIPE candidate; the owner deferred the host joins (DECISION-3: 'defer the host joins'); OI-021 is open".

  The builder stops if OI-016 (App v4) or OI-021 is no longer OPEN in Open_Issues.csv at the commit, or if DECISION-3's text is missing, so the record cannot silently outlive its basis.
- **PV-STANDING-1** (`not_agreed`, no observations, not a replacement condition): the value DEL-11-03 should carry.

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

| ID | Item | Decided or done by | Point of need |
|---|---|---|---|
| U-PV-1 | The agreement on period and activities | The owner, the person (OI-016 (App v4); P-2) | Before validation in use; possible only when candidates exist |
| U-PV-2 | Candidates for each expression | Supplied by DEL-09-02 (App) and DEL-09-07 with SWBPIPE (host) (DEP-001, OI-021; host joins deferred) | Before use in that expression |
| U-PV-3 | DEL-11-03 adopts `practitioner_standing` in place of its first cut, taking the stated differences (§2 O-3: format, `arrangement_ref`, `is_replacement_condition`) | Assigned to design agent O-F at DEL-11-03's next revision | — |
| U-PV-4 | EXP §3.3's `activity: validation` is not used by DEL-09-12 (F-R12) | DEL-09-01's next revision (recorded by HELP_HUMAN; RV2 PV1-R8) | EXP's next revision |
| U-PV-5 | OI-020 before any manual revision proposed from feedback | The owner (P-6) | When one is proposed |

## 8. Verification (designed; `check_pv.py` 38/38 at freeze; 29 invalid examples)

Each rule about the real records is one function in `check_pv.py`; each negative case breaks a real record (or, for F-R12, UC §5 and the hand-over, the schema text) in memory and runs the same function, naming the rule that must refuse it. Where no real record of a kind exists (observations, dispositions), the rule is broken on the examples (K-6) or on an in-memory record built for the case (PV-R4: P-1, N-20…N-23). K-6 checks each schema refusal against the record kind's own `$def`.

| VER | Case | Held by |
|---|---|---|
| VER-001 | The real arrangement is `not_agreed`, with causes; an illustrative proposal and an agreed arrangement validate; a plan offered as agreement and a self-recorded agreement are refused; exactly the two expressions; an agreed arrangement with unselected activities, or an available expression with no candidate or material, is refused | K-1, K-4, K-5; K-6 (invalid 3, 4, 15, 16; PV-R2 invalid 12); N-1, N-2, N-15, N-16 |
| VER-002 | An observation with four aims, no score or outcome; "not observed" holding statements is refused; actual use on a placeholder, outside an agreed arrangement, on an unselected activity or on another candidate is refused; a SWBPIPE observation names its host candidate | K-5, K-7; K-6 (invalid 1, 2, 9, 19; PV-R1 invalid 11; PV-R4 invalid 18); P-1, N-20…N-24 |
| VER-003 | Illustrative cases are marked as such and are never practitioner observations; acts keep actor and recorder apart | Examples' `standing`; K-6 (invalid 4, 24, 28, 29; PV-R5 invalid 26) |
| VER-004 | Observation → commitment → recipient through the real ScopeLedger; unresolved is reported; a decided disposition names the decider its case requires, a recorder, and its record; a method decision is the owner's at the stage decision; a successor basis stays proposed until its own decision and adoption; an agent never decides; a method observation goes to DEL-10-02 with section and node | K-10, K-11; K-6 (invalid 5, 6, 20, 21, 23, 27; PV-R3 invalid 13, 14; PV-R5 invalid 22, 25) |
| VER-005 | OI-016 (App v4), OI-021 and OI-024 carried; no invented period; validation is not a replacement condition; F-R14 qualification everywhere; the hand-over to DEL-11-03 differs from the first cut only as stated | K-4, K-8, K-9, K-12; K-6 (invalid 7, 8, 10, 17); N-17, N-18, N-19 |
| VER-006 | Act boundary (§1) | Review |

**RV2's probes, rebuilt from RV2-PV1.md:** A (two `app` expressions) is invalid 15 and N-15; B (agreed, available, no candidate or material) is invalid 16 and N-16; C (actual use under not-agreed PV-ARR-1, activity in no arrangement) is invalid 18 and N-24; E (a successor basis "decided" by an agent on one reference) is invalid 20, with invalid 21 hardening it; H (`in_use` with no agreement reference) is invalid 17 and N-17. G (agreement recorder "The owner") is now invalid 28, and RV2's E8 (a method decision recorded by "The owner") is invalid 29, here with doubled spacing (PV2-R1). D still passes, as listed below.

**Claimed rules with a negative case:**
- schema, arrangement: a plan offered as agreement (N-1; invalid 3), a self-recorded agreement (invalid 4; in any case or spacing, invalid 28), the two expressions (N-15; invalid 15), candidate and material when available in an agreed arrangement (N-16; invalid 16), an unqualified open issue (N-6; invalid 10).
- schema, observation: outcome or score (invalid 1, 2), not-observed with statements (invalid 9), the SWBPIPE host candidate (invalid 19).
- schema, disposition: a decision needs its decider, recorder and record (invalid 5, 24, 20), a method decision by an agent (invalid 23), an owner's decision recorded by the owner in any case or spacing (invalid 29), a successor basis decided by an agent (invalid 20, 21), a proposal shown as a decision (invalid 27), method routing (invalid 6).
- schema, standing: observations or an agreement while not agreed (N-3, N-4; invalid 8), an agreement reference once agreed (N-17; invalid 17), a replacement condition (N-5; invalid 7), the observation ids' type (N-18).
- PV-R1 (invalid 11); PV-R2 (N-2, schema-valid; invalid 12); PV-R3 (invalid 13, 14); PV-R4 (N-20…N-24; invalid 18; P-1 the positive control); PV-R5 (invalid 22, 25, 26).
- K-2 (N-12); K-3 (N-13); K-4 (N-5, N-8); K-7 F-R12 (N-9); K-8 F-R14 (N-6, N-7; K-9 tests the rule both ways); K-11 UC §5 fields (N-10); K-12 hand-over (N-11, N-18, N-19); K-13 (N-14).

**Without a negative case on a real record, or not enforced:**
- No real observation or disposition exists. PV-R1, PV-R3, PV-R4 and PV-R5 are broken only on examples and in-memory records; K-10 runs PV-R3's routing on the real ScopeLedger, including an unknown anchor.
- PV-R1's placeholder test is keyword-based (§3.2): RV2's probe D ("TBD") passes it. PV-R4 then requires the arrangement's candidate to be the same string, so a placeholder in both still passes.
- Actor-not-recorder tests are string comparisons. Where the actor is the owner, any case or spacing of "the owner" is refused (schema; PV2-R1), but another name for the person ("Ryan") passes. For other decisions (PV-R5) the comparison is exact, so a recorder differing from the actor only by case passes (RV2's E7). A false recorder name passes.
- PV-R5's "the owning deliverable's own record" is textual: `record_ref` must contain the deliverable's id. Whether the cited record exists and says what it is cited for is not checked; nor is whether the actor is that deliverable's accountable party.
- PV-R5's method check looks for "OWNER_DECISIONS" in `record_ref`; it does not read the file or the stage.
- A successor basis's `adoption_ref` is checked as present and different from `record_ref`; whose adoption it records (the affected consumers) is not checked.
- PV-R4 does not compare the observation's date with the arrangement's period, and does not check the observation's configuration.
- K-12 compares the hand-over with DEL-11-03's first cut field by field; it cannot show that DEL-11-03's next revision will take the stated differences (U-PV-3).
- VER-006 (the act boundary) is by review.

## 9. Changes

| Version | Change |
|---|---|
| PV-v0.4 (2026-10-04) | Unit EU-F4R2, the last tranche-2 round: PV2-R1, the owner-as-recorder refusal in any case or spacing for the agreement and for an owner's decision (schema pattern), with RV2's probes G and E8 as invalid 28 and 29; PV2-N2, "design agent O-F" in this file, the examples and the real arrangement's `prepared_by`. Records rebuilt at `b2fbfdbac8`; record format PV-v0.3 unchanged |
| PV-v0.3 (2026-10-04) | RV2-PV1 repair (unit EU-F4R):
- PV1-R1: a decision has a decider fixed by its case, a recorder and a recording mode; method and successor-basis decisions are the owner's; a successor basis needs its own adoption record; a proposal carries only `proposed_by`; PV-R5 added. Probe E is invalid 20.
- PV1-R2: exactly one `app` and one `swbpipe` expression (schema).
- PV1-R3: PV-R4 ties actual use to an agreed arrangement, an owner-selected activity and that expression's candidate; an agreed arrangement's available expressions need a candidate and material; a standing past `not_agreed` needs an agreement reference.
- PV1-R4: candidates by expression; SWBPIPE carries EXP's `host_candidate` (required on its observations), and `configuration.host_candidate` is removed.
- PV1-R5: `observations` is an array of ids, as DEL-11-03's first cut reads it; the remaining differences are stated (§2 O-3) and recomputed by K-12, which now checks every first-cut field.
- PV1-R6: "owner" kept for the person (header, §1, §7, the real record's `prepared_by`).
- PV1-R7: N-2 is schema-valid; §8's example numbers corrected; valid example 2's limit corrected; `pvlib.py`'s docstring names PV-R1…PV-R5.
- PV1-R8: carried to DEL-09-01's next revision (U-PV-4).
- Record format PV-v0.3; real records rebuilt at `b2fbfdbac8` (format, `observations: []`, `prepared_by`). Examples: 12 valid, 27 invalid. Audit lists rechecked (§8) |
| PV-v0.2 (2026-10-04) | Coordinator's checker audit: rules as functions of the real records; N-1…N-14 break them; covered and uncovered rules listed (§8). The placeholder test's keyword limit stated (§3.2). Records, schema and examples unchanged; record format PV-v0.1. Unit EU-F4, refrozen before review |
| PV-v0.1 (2026-10-04) | First Design file; unit EU-F4 (frozen, not sent for review) |
