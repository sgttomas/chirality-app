# Owner replacement evidence packet

- **Contribution:** DEL-11-03/RP-v0.2. It supersedes RP-v0.1 (sha256 `1a06262bcf516972c745cf954e8b07d1b697b9f0732d9bd22020e4e372069c8c`, frozen as EU-F1 and read by the isolated reader RR-EUF1), repaired for that reader's findings (O-F.md "EU-F1 — reader result"). It is the unit **EU-F1**, the tranche-2 early path for PKG-11 and DEL-09-12: one replacement decision package, assembled from the suppliers' dossiers and read, with the decision left pending.
- **Status:** DRAFT DEFINITION — proposed, unsupplied, not implemented, not accepted. Beside this file are two PROPOSED schemas, `rp.packet-manifest.schema.json` and `rp.disposition.schema.json`. The prototype, fixture and consumption check are under `_Coordination/AgentRuns/APP-V4-DESIGN-PASS-4-20261003/F/` (RUN/F). No candidate exists; no replacement witness exists; nothing is presented to the owner.
- **Run and owner:** `APP-V4-DESIGN-PASS-4-20261003`, tranche 2; owner O-F (Type 2, Claude Opus 5.5); 2026-10-04.
- **Serves:** OUT-001, OUT-002, OUT-003; REQ-001…REQ-006; designed cases for VER-001…VER-006 (§8).
- **Rulings applied (cited by ID, R23-21):** R23-32 (P-1…P-7 are the person's acts at their own points of need; F-R1…F-R16 as S2-F proposed them), R23-33 (EXP's `candidate_subject` is the canonical App candidate identity), R23-36 (LHQ-v0.2 CI-5 adds the CIR mapping), R23-24 (package file shape), R23-19/R23-20 (outcome labels), R23-11 (overtaken wording carried).
- **ScopeOfWork pin (R23-5):** `ScopeOfWork.md` sha256 `0177354357b07ea177491cffc2b1c75ffac578e179ba96e63e91d6ba34dcf5b6`. This is the INIT contract; no SCA-V4-001/002/003 block changed it. Overtaken wording followed, not edited: CLM-004 reads OI-001 as unresolved; D2 ruled it for App/shared contracts. It is listed for the next amendment (R23-11).
- **Basis pins** (`shasum -a 256`, 2026-10-04): `docs/PRD.md` `bb6e786f7a6c01dc5ce2f16f58e6c600989a12808ff47ce4fd87924bcc6c49bd` (§8 V4-REP-01, §9 OQ-08, OQ-12, §11); `docs/EXAMINATION.md` `471798bc2f2dc0202ae40d9d5cf033a22ae41af2a0afdf58032cf37a687957d0` (§2, §7, V4-EXM-10/11/20); `reference/REFERENCES.md` `07fe44e0494634ee40ae57a0b112f6fed7ae0b937fd3e2502574cd5431b240fc` (§2, the fallback).
- **Supplier pins** (committed and unchanged since `d150856784`, except LHQ-v0.2 as stated):
  - DEL-09-02 SQ-v0.2 `STANDALONE_QUALIFICATION.md` `3e5d0f12c6190710ae11971a01a5be81bd3e5c31eddd9bbb0b835759649d8391` (§1, §2 O-1, §8), with `sq.dossier.valid.examples.json` `426165ba047ac7c53edb1d81debb0f917121866ebbdd7fd7ecc00bca835de7db`.
  - DEL-09-07 DOS-v0.1 `QUALIFICATION_DOSSIER.md` `b2ffba7135652c9e5d2ebaece3d1b002a4aef6f394f9f876dc2b3600cdde0ccd` (§1, §4 DH-1/DH-2, §6 DF-5), with `lhq.dossier-manifest.valid.examples.json` `4d659926675a5c7e4bad32a627a7aef738fd0c9fb5aa606abe9314271784f9bd`.
  - DEL-09-07 LHQ-v0.2 (R23-36; O-C's working bytes, not yet committed) `LOCAL_HOST_QUALIFICATION.md` `5cd31e097a8faae46298202d854b9bb9cba27e8355c31fef997310b49c15f07b` (§3 CIR, CI-5; the OI-013/014 row), with `lhq.candidate-identification.schema.json` `3fb8f586b0bc1ca32c2ba4e82008e384109d3adc1189a0bf5091d598c46b5fc5` and `….valid.examples.json` `c7684ee595bcb1e91a6a3b86bb4a37022a0c4c57dfcacc3ffad8326b41b2d9d4`. RP-v0.1 relied on LHQ-v0.1 (`20361a0b…`); the fixture's CIR record is byte-identical in both versions.
  - DEL-09-01 EXP-v0.2 `EXAMINATION_PROTOCOL.md` `ff0187dafd9e1f0268a19f9266914bdba64f39e0c8befdcaf20d3da7a7206a93` and `exam.result-record.schema.json` `f7871c96cef25bb974aea73feca009ed3caf843db5077d80612f13b130af2081` (`$defs/candidate_subject`, `$defs/outcome`).
  - DEL-02-03 `checkpoint-record-entries.schema.json` proposed-0.7 `a5271857c8bf71f67077fc52760a35d41ee0c30f8bd6d487a93d3c882308b45c` (`$defs/decisionPackageFile`, used read-only).
- **Labels.** *States* means a file says it; *inference* marks this file's own reading; PROPOSED marks rules this file introduces.

## 0. What this version contains, and what it leaves out

It contains the packet's interfaces, records, rules, states and failure behaviour, as far as one complete pass through them needs (EU-F1):
- the packet manifest (§3);
- the core-loop and journey rules (§4);
- the candidate identity rule (§5);
- the package file and the disposition record (§6).

It leaves out:
- assembling any real dossier (no candidate exists);
- choosing OI-021;
- any release step and any retirement;
- presenting anything to the owner;
- the continuity account itself (DEL-11-01) and the practitioner record itself (DEL-09-12). For each of these, only the first-cut input DEL-11-03 expects is defined, as `$defs` in the manifest schema. The owning deliverable's own file supersedes it.

## 1. Owner and act boundary (REQ-006; CLM-001…CLM-004)

| Act | Who | This file |
|---|---|---|
| Standalone qualification and its dossier | DEL-09-02 (O-B) | Consumes the dossier's handoff (§4.1) |
| Local host qualification, CIR and dossier | DEL-09-07 (O-C), with the SWBPIPE owner (DEP-001) | Consumes the handoff and CIR (§4.2, §5) |
| Continuity account | DEL-11-01 (O-F) | Consumes it (first cut, §3.3) |
| Practitioner standing | DEL-09-12 (O-F) | Carries it; never a condition (F-R3) |
| Adoption status | DEL-11-02 (O-F) | Carries it |
| Assembling the packet, the package file and the disposition record | DEL-11-03 coordinator | Defined here |
| **Replacing v3.0.1** | **The owner** (PRD §8: "The owner decides the replacement"; P-1) | Prepared, never performed or implied |
| **Public release** | **The owner** (PRD OQ-08; CLM-003; P-5) | Kept apart in the alternatives (§6.1) |
| **Retirement, adoption** | **Owner with affected consumers** (OI-024; P-4) | Never implied; every alternative retires nothing |
| Professional reliance | The accountable professional | Never claimed |

## 2. Interfaces

| ID | Input or output | Other end | Arc (DAG-004) | Point of need | If absent |
|---|---|---|---|---|---|
| I-1 | SQ dossier record and its `handoff` (`to: DEL-11-03`) | DEL-09-02 | DEP-11-03-006, admitted | Packet assembly | OUT-001 *not evidenced*; gap named |
| I-2 | DOS dossier manifest `handoff_del_11_03` and the CIR it cites | DEL-09-07 | DEP-11-03-007, admitted | Packet assembly | OUT-002 *incomplete*; gap named |
| I-3 | Continuity input (first cut `$defs/continuity_input`) | DEL-11-01 | DEP-11-03-008, held (SCC-006; F-R8: SCC-CASE-007 R1) | Packet assembly | Carried as *not supplied*; gap named |
| I-4 | Practitioner standing (first cut `$defs/practitioner_standing`) | DEL-09-12 | DEP-11-03-009, admitted | Packet assembly | Standing *not_supplied*; never a gap for replacement |
| I-5 | Adoption status | DEL-11-02 | DEP-11-02-015, admitted (supplier's row) | Packet assembly | *not supplied*; gap named |
| I-6 | v3.0.1 baseline identity | `reference/REFERENCES.md` §2 | DEP-11-03-010 (not topological; was UNKNOWN, F-R2) | Packet assembly | Packet not assembled |
| I-7 | EXP result records the dossiers cite; EXP change-impact records | DEL-09-01 records (EXP-v0.2) | through I-1/I-2 | Establishing an obligation | Obligation *not established* |
| O-1 | Package file (R23-24 shape) | The owner, when presented | DEP-11-03-014 (not topological) | When both witnesses exist | — |
| O-2 | Disposition record | DEL-11-01 and affected consumers | DEP-11-03-015 (held), DEP-11-03-016 | After an attributable owner act | Disposition stays as recorded (§6.2) |

## 3. The packet manifest (`rp.packet-manifest.schema.json`)

One manifest per packet version.
- It names every supplied item by path and sha256, together with the source it was copied from (file, sha256, record id).
- It states what the rules (§4, §5) derive from those items. Nothing in it is filled from a definition.
- `evidence_standing` is `illustrative` whenever any supplier input is an example or fixture. An illustrative packet can establish nothing.
- Each supplied item states `produced_by` (who produced its content) and `source_kind`: `copied_record` (it equals a record in the named source file) or `shape_only` (the named source gives only its shape). The first-cut continuity and practitioner inputs are `shape_only`, produced by DEL-11-03's builder standing in for DEL-11-01 and DEL-09-12 (RP-v0.2; reader issue I-9).
- `terms` defines every code or identifier the package, packet and disposition use (for example A16, P20-A, CIR, OI-nnn, DEP-001, DECISION-3), so a person deciding without project context can read them. The prototype refuses a packet that uses a code with no term (A-13; reader issues I-1, I-6).
- `basis_excerpts` names a file of the exact passages the decision rests on, each with its source sha256: PRD §8, EXAMINATION §7, DEL-11-03 CLM-001, CLM-003, REQ-004, REQ-005 and AX-001, REFERENCES §2, and App v3's BUILD_AND_RELEASE §12, which underlies ALT-PUBLISHED's inference (reader issue I-7).
- `basis` quotes the reserving texts with their source sha256. The builder checks each quote against the current bytes.
- `baseline` is REFERENCES §2. `remote_rechecked` stays false until someone re-reads the published release. `comparison_rule` states how "at least at v3.0.1's level" is judged: by V4-EXM-10 and V4-EXM-11 passing on the candidate (EXAMINATION §7; F-R2; reader issue I-8). The baseline also carries the v3 reference limit: SQ's `v3_reference` values cite v3.0.0-era journeys (`266c121bb` is not an ancestor of the v3.0.1 source). They are context only.
- `not_established` always lists the six things the packet never establishes: replacement decision, public release, retirement, professional reliance, consumer adoption and practitioner validation.
- `gaps` names each missing contribution, its supplier and its point of need. A gap never gates presentation: AX-001 lets a packet "accurately report partial or adverse evidence". Its point of need is "before the replacement evidence can be complete", or "carried for the owner; not a replacement condition" (RP-v0.2; RP-v0.1 wrote "before the package is presented", reader issue I-10). `open_matters` carries P-1, P-5, OI-024, OI-021, DEP-001, OI-016 (App v4) and the OI-013/014 residue, each with its owner.

### 3.3 First-cut inputs

- **`continuity_input`** (from DEL-11-01) carries:
  - the thesis identity check: method, expected and observed tree, the commit, and its limits;
  - the fallback identity: source, retained, not re-checked remotely;
  - the archive `verify` result;
  - the continuing-obligation status, with OI-024's owner and point of need;
  - adoption status;
  - `replacement_standing: "replacement pending; v3.0.1 retained"`, the R1 lifecycle of SCC-006.
- **`practitioner_standing`** (from DEL-09-12) carries "OI-016 (App v4)" (F-R14) and a standing (`not_agreed` … `ended`). When the standing is `not_agreed`, there is no agreement reference and no observation.

## 4. Rules (PROPOSED; implemented in RUN/F `rplib.py`)

### 4.1 RP-R1 Core-loop obligation (REQ-001, VER-001; EXAMINATION §7)

- The seven elements form a closed list owned here: planning, execution, workflow saving, reuse, approvals, interruption, restart. SQ's `core_loop_element` strings map to it one for one.
- Only V4-EXM-10 and V4-EXM-11 count. Other scenarios (V4-EXM-12) are listed as *outside the core loop*.
- A V4-EXM-10/11 step whose element is outside the list is an interface error. The obligation is then never established.
- An uncounted step (for example J-8R) is shown and changes no element.
- Each element carries two facts, kept apart (RP-v0.2; finding EUF1-D1):
  - `recorded`, what the dossier records for its counted steps: `recorded_pass` (all recorded pass), `recorded_not_pass` (one recorded with another outcome), or `not_recorded`;
  - `status`, what the evidence supports. An element is `met` or `not_met` only when `evidence_resolved` is true. That means every counted step's `result_record` resolves to a supplied EXP result record with `run_basis: candidate` and the same outcome (EXP-R3). Otherwise its status is `not_evidenced`, whatever the dossier records.
- The obligation is `met` only if all seven are `met`; `not_met` if any is `not_met`; otherwise `not_evidenced`.
- **Established** requires all of: obligation `met`; the dossier `handed_over` and `reported_as_independent` (SQ-R8); and no unresolved step.
- `dossier_review` reports the standalone dossier's own independent review separately from the journey's, and names what each covers (reader issue I-5).
- RP-v0.1 derived `met` from what the dossier records alone. It showed six elements "met" on illustrative records, a claim EXP-R3 does not allow even in a fixture.

### 4.2 RP-R2 Journey obligation (REQ-002, VER-002; DOS §4 DH-1 as written)

- The journey is `completed_witness` only if all of these hold:
  - the handoff counts P20-A;
  - it cites at least one acceptance act, each with actor ≠ recorder;
  - the dossier has an independent review record.
- It is **established** only if, in addition, P20-A's EXP record is a `candidate` `pass`.
- Receipts: every receipt reference anywhere in the dossier is carried, kept apart by where it appears. That covers the DEL-11-03 handoff (`in_handoff`), the host evidence index and the DEL-09-11 handoff (`elsewhere_in_dossier`). Each keeps its resolution status, and a session-only receipt stays *unresolvable* (DF-5). A receipt the dossier names elsewhere but omits from its hand-over to DEL-11-03 makes the journey not established (`receipts_in_dossier_missing_from_handoff`). RP-v0.1 read only the handoff block and counted 0 while the dossier named RC-1 (finding EUF1-D2).

### 4.3 RP-R3 One candidate (F-R1; R23-33)

See §5. Results join across the two obligations only when the reconciliation is `reconciled`, or `reconciled_by_applicability` with an EXP change-impact record named.

### 4.4 RP-R4 Completeness, RP-R5 practitioner standing

- Replacement evidence is complete only if the core loop is established, the journey is established and the candidate is reconciled.
- Practitioner standing is shown and never consulted (F-R3; REQ-005: no "third fixed-duration replacement gate").
- Completeness is never the decision (AX-001).

### 4.5 RP-R6 Package file, RP-R7 disposition, RP-R8 integrity

- **RP-R6:** see §6.1. The package validates against DEL-02-03's `$defs/decisionPackageFile`, and the rules there apply.
- **RP-R7:** see §6.2.
- **RP-R8:** every supplied item's sha256 in the manifest equals the file. Each copied supplier record equals its source record at the named source sha256. The manifest's derived values recompute to themselves from the supplied copies.

## 5. Candidate identity (R23-33)

| Source | Form | Maps to EXP `candidate_subject` | Today |
|---|---|---|---|
| EXP-v0.2 `$defs/candidate_subject` | `{kind, app_candidate{revision, build_identity, packaged, package_record}, host_candidate, identification_record}` | Canonical | — |
| SQ-v0.2 `candidate` | `{revision, build_identity, codex_pin, package_record}` | `revision` and `build_identity` copied; `packaged` = whether `package_record` is present; `codex_pin` is configuration, not identity (EXP §3) | **Maps; no SQ row needed** |
| LHQ CIR `elements.app_candidate` with LHQ-v0.2's `app_candidate_subject` (CI-5; R23-36) | `app_candidate_subject` is a checked copy of EXP's `candidate_subject.app_candidate`; it is present only while the element is supplied | Copied as `app_candidate`; `host_candidate` from the CIR's host element; `identification_record` = the CIR id | **Maps** (B-18…B-23, on O-C's example `LHQ-CIR-EXAMPLE-MAPPED`) |
| The same element without `app_candidate_subject` | `{value, source, standing}`: one string | Cannot be split without inventing a convention | Not mappable (B-24) |

Reconciliation values:
- `reconciled`: both map, and their `app_candidate` objects are equal;
- `differ`: both map but differ, with no change-impact record. Results are not joined;
- `reconciled_by_applicability`: they differ and an EXP change-impact record is named (V4-EXM-03; F-R1);
- `not_established`: either side is not supplied or not mappable.

The packet's subject is the SQ-mapped `candidate_subject`. When the CIR maps, it also carries `host_candidate` and `identification_record`. The OI-013/014 residue (what the App candidate contributes to an embedded journey; LHQ's open row) is carried as an open matter.

## 6. Package, presentation and the owner's act

### 6.1 The package file (O-1; R23-24 shape; F-R4, F-R5)

- `actKind: "A16"` (decide).
- `subject[0]` names the candidate. `subject[1]` is `packet manifest sha256:<hex>`. The decision therefore binds to the exact evidence, and a changed manifest means a new package.
- `reservedBy` cites PRD §8 V4-REP-01 and EXAMINATION §7 with their exact statements. `scope` is "the v3.0.1 fallback only".
- Exactly four alternatives, in this order:

| ID | Statement (short) | v3.0.1 remains the fallback | Also a release act | Retires anything |
|---|---|---|---|---|
| ALT-OWN-USE | The owner's own work moves to the candidate; v3.0.1 stays published | yes | no | no |
| ALT-PUBLISHED | The candidate replaces v3.0.1 as the published product | no | **yes** (OQ-08, decided separately) | no |
| ALT-DEFER | Decide again when the named gaps close | yes | no | no |
| ALT-DECLINE | This candidate does not replace v3.0.1 | yes | no | no |

`subject[0]` asks "whether, and at what scope", and ALT-OWN-USE's statement says what it replaces: v3.0.1 in the owner's own work only (RP-v0.2; reader issue I-3). `purpose` names the act in words: A16, 'decide', choosing exactly one alternative (reader issue I-1). ALT-PUBLISHED's consequences include an inference, labelled as one: App v3's records (`BUILD_AND_RELEASE.md` §12) say v3.0.x installs check the latest published stable release, so they would be offered v4. Every alternative states "No retirement" (RP-R6). The package holds no recorder element (R23-24).

### 6.2 The disposition record (O-2; `rp.disposition.schema.json`; REQ-004, VER-004)

States:
- `not_presented`: prepared only. A fixture is always in this state, with its reason.
- `presented_no_decision`: put before the owner, with no attributable act yet. Silence, timeout, a tool receipt or an agent's claim never moves it on.
- `decided`: an attributable owner act chose one of the package's alternatives.

The owner's act is recorded in the project's OWNER_DECISIONS form (F-R4), and the disposition references it. The reference carries:
- the record and heading;
- the exact text;
- the custody (for example "the owner's chat message, transcribed by the recorder; no platform timestamp");
- the actor ("the owner") and a recorder distinct from the actor;
- `act_time`, either available with value and source, or not available, kept apart from `recorded_at`.

If the owner instead decides through a candidate App's act control, that A16 record is cited as well. No ACT, RS, AAC or shared schema changes.

RP-R7:
- An undecided record keeps "v3.0.1 remains the fallback".
- A decided record names an alternative the package names.
- A package whose sha256 differs from the presented one makes the disposition *lapsed*, as an A16 on a changed file lapses (RS L-1).
- No favourable state is a completion criterion.
- The disposition returns to DEL-11-01 as the next continuity-account version (SCC-CASE-007 R1).

### 6.3 Sequence

1. Receive the supplier handoffs (I-1…I-5).
2. Build the manifest (RP-R1…R5, R8).
3. Write the package (RP-R6).
4. Write the disposition as `not_presented`.
5. When both witnesses are established and the coordinator presents the package: `presented_no_decision`.
6. When the owner acts: `decided`, recorded as in §6.2.
7. Return the disposition to DEL-11-01 and the affected consumers.

A supplier change makes a new manifest version, and so a new package. An earlier package and its disposition stay as history.

## 7. Failure behaviour

| # | What fails | Record left | Next |
|---|---|---|---|
| RF-1 | A supplier handoff is missing | Gap with supplier and point of need; obligation *not evidenced* | Packet kept; not presented |
| RF-2 | A step's result record does not resolve to a candidate EXP record | `not_established_because` names it | Returned to DEL-09-02 or DEL-09-07 |
| RF-3 | Candidates differ, or one side is not mappable | Reconciliation `differ` or `not_established`; obligations not joined | Change-impact record (DEL-09-01 form) or the CIR row (RQ-LHQ-1) |
| RF-4 | A supplier record changes after assembly | RP-R8 fails; new manifest version; a new package | The old package and its disposition become history; a decided disposition on it lapses |
| RF-5 | A V4-EXM-10/11 step names an element outside the closed list | Interface error | Returned to O-B |
| RF-6 | An owner response is ambiguous, or does not name an alternative | `presented_no_decision`, with the response quoted in `limits` | The state stays; no alternative is ever inferred from the response |

## 8. Verification (designed; the prototype results are not candidate evidence)

| Case | Serves | Expected | Status 2026-10-04 |
|---|---|---|---|
| RP-VC-01 Core-loop account | VER-001, AC-001 | RP-R1: per element, `recorded` and `status` kept apart; no `met` or `not_met` without resolved candidate evidence; "met" refused with an element short | Rules run (RUN/F B-1…B-11) |
| RP-VC-02 Journey account | VER-002, AC-002 | RP-R2: DH-1 as written; acceptance actor ≠ recorder; review required | Rules run (B-12…B-17) |
| RP-VC-03 Reconciliation and negatives | VER-003, AC-003 | RP-R3/R4; the historical, illustrative, merged and isolated-component negatives cannot pass | Rules run (B-18…B-28); live negatives need a candidate |
| RP-VC-04 Disposition | VER-004, AC-004 | RP-R7; fabricated decision, actor = recorder, unknown alternative, lapsed package, undecided record dropping v3.0.1 | Rules run (B-33…B-40) on invented records; no owner act requested |
| RP-VC-05 Continuity and open matters | VER-005, AC-005 | First-cut continuity input carried; P-1/P-5/OI-024/OI-021/DEP-001/OI-016 (App v4) carried; no PEC or Domains gate | Fixture FX-RP1-2 (A-11, A-12, A-14) |
| RP-VC-06 Act boundary | VER-006, AC-006 | §1 table; the package never performs or implies an owner act | Review |
| **EU-F1 consumption check** | REQ-004 (the owner can decide from the files) | An isolated reader given only IS-FX-RP1-1 answers Q-1…Q-12 (`READER_BRIEF.md`). An examiner compares the answers with the frozen key, field by field | RR-EUF1 on IS-FX-RP1-1 (RP-v0.1): 33/33 fields, 11 issues, judged in O-F.md; IS-FX-RP1-2 is ready with its own key, should a second reader be wanted |

Prototype at freeze (RP-v0.2, fixture FX-RP1-2): `check_rp.py` 57/57.
- A-1…A-17 cover the fixture: integrity, schemas, copies, recomputation, thesis identity, terms, excerpts, receipts, points of need and evidence-before-status.
- B-1…B-40 are 40 rule cases.
- A-13, A-15, A-16 and A-17 fail on the RP-v0.1 fixture, as they should; this was checked.

The consumption check on RP-v0.1: RR-EUF1's account held 33/33 fields against the frozen key, with 11 issues referred. Each issue is judged in O-F.md. `compare_rp.py --set 2 --self-check` holds 16/16 for the IS-FX-RP1-2 key. The builder is deterministic.

## 9. Open matters

| Item | Owner | Point of need | Effect here |
|---|---|---|---|
| RQ-LHQ-1: closed by R23-36. LHQ-v0.2 CI-5 adds `app_candidate_subject`. It is O-C's working bytes, not yet committed | — | — | Reconciliation works on a CIR that supplies it (B-18…B-23) |
| DOS example inconsistency: the dossier's DEL-09-11 handoff names RC-1, while its host evidence index and its DEL-11-03 handoff are empty (finding EUF1-S1) | O-C | At DOS's next revision | RP-R2 now detects it (B-15); no effect on DOS's rules |
| SQ dossier's `core_loop_element` is a free string | O-B (optional) | — | RP-R1's closed list catches drift (RF-5); no row requested |
| P-1 replacing v3.0.1; P-5 public release | The owner | Their own points of need | Prepared only |
| OI-021, DEP-001, host joins (DECISION-3) | Owner via the SWB session; SWBPIPE | Before V4-EXM-20 can run | OUT-002 stays incomplete |
| OI-013/014 residue (App candidate's role in V4-EXM-20) | Shared contract owner with the SWB owner | Before the CIR's App element is fixed for CA/E | Carried |
| Remote re-check of REFERENCES §2 | DEL-11-03 coordinator | When a package is prepared for presentation | `remote_rechecked: false` until then |

## 10. Changes

| Version | Change |
|---|---|
| RP-v0.2 (2026-10-04) | Repaired for RR-EUF1:
- EUF1-D1: RP-R1 separates `recorded` from `status`, and status needs resolved candidate evidence.
- EUF1-D2: RP-R2 carries every receipt in the dossier.
- Gaps no longer gate presentation (AX-001).
- `terms`, `basis_excerpts`, `comparison_rule`, `produced_by` and `source_kind`, and `dossier_review` were added.
- Package wording: "at what scope", and what ALT-OWN-USE replaces.
- LHQ-v0.2 CI-5 mapping (R23-36).
- New fixture FX-RP1-2 and input set IS-FX-RP1-2 with its own key. FX-RP1, IS-FX-RP1-1 and the original key are kept unchanged.
- Manifest format `RP-v0.2`; the disposition schema is unchanged |
| RP-v0.1 (2026-10-04) | First Design file. EU-F1: manifest, rules RP-R1…R8, candidate mapping (R23-33), package and disposition (F-R4, F-R5); fixture FX-RP1 and the consumption check in RUN/F |
