# Owner replacement evidence packet

- **Contribution:** DEL-11-03/RP-v0.5. It supersedes RP-v0.4 (sha256 `5bfa93036466e3b894608f595a4f8fda070f6335470bdca6433e939dbcd98271`, unit EU-F2, READY in RV3-EUF1.md Addendum 6). It is part of unit **EU-F3**, with DEL-11-01 CA-v0.2 and DEL-11-02 AA-v0.1. RP-v0.5 does three things:
  - repairs EUF4-R1: `evidence_standing` and `candidate.identified` are derived, not declared, and a fixture package is never presented or decided;
  - carries DEL-11-02's adoption status as supplied item S-6;
  - takes CA-1 v2.

  Earlier versions:
  - RP-v0.3 `164c082c…` (RR-EUF3, 36/36; EU-F1 passed, R23-49);
  - RP-v0.2 `80e88983…` (RR-EUF2);
  - RP-v0.1 `1a06262b…` (RR-EUF1).
- **Status:** DRAFT DEFINITION — proposed, unsupplied, not implemented, not accepted. Beside this file are two PROPOSED schemas, `rp.packet-manifest.schema.json` and `rp.disposition.schema.json`. The prototype, fixture and consumption check are under `_Coordination/AgentRuns/APP-V4-DESIGN-PASS-4-20261003/F/` (RUN/F). No candidate exists; no replacement witness exists; this fixture is never presented to the owner (a real packet may be: §6.3).
- **Run and owner:** `APP-V4-DESIGN-PASS-4-20261003`, tranche 2; owner O-F (Type 2, Claude Opus 5.5); 2026-10-04.
- **Serves:** OUT-001, OUT-002, OUT-003; REQ-001…REQ-006; designed cases for VER-001…VER-006 (§8).
- **Rulings applied (cited by ID, R23-21):** R23-32 (P-1…P-7 are the person's acts at their own points of need; F-R1…F-R16 as S2-F proposed them), R23-33 (EXP's `candidate_subject` is the canonical App candidate identity), R23-36 (LHQ-v0.2 CI-5 adds the CIR mapping), R23-24 (package file shape), R23-19/R23-20 (outcome labels), R23-11 (overtaken wording carried).
- **ScopeOfWork pin (R23-5):** `ScopeOfWork.md` sha256 `0177354357b07ea177491cffc2b1c75ffac578e179ba96e63e91d6ba34dcf5b6`. This is the INIT contract; no SCA-V4-001/002/003 block changed it. Overtaken wording followed, not edited: CLM-004 reads OI-001 as unresolved; D2 ruled it for App/shared contracts. It is listed for the next amendment (R23-11).
- **Basis pins** (`shasum -a 256`, 2026-10-04): `docs/PRD.md` `bb6e786f7a6c01dc5ce2f16f58e6c600989a12808ff47ce4fd87924bcc6c49bd` (§8 V4-REP-01, §9 OQ-08, OQ-12, §11); `docs/EXAMINATION.md` `471798bc2f2dc0202ae40d9d5cf033a22ae41af2a0afdf58032cf37a687957d0` (§2, §7, V4-EXM-10/11/20); `reference/REFERENCES.md` `07fe44e0494634ee40ae57a0b112f6fed7ae0b937fd3e2502574cd5431b240fc` (§2, the fallback).
- **Supplier pins** (committed and unchanged since `d150856784`, except LHQ-v0.2 as stated):
  - DEL-09-02 SQ-v0.2 `STANDALONE_QUALIFICATION.md` `3e5d0f12c6190710ae11971a01a5be81bd3e5c31eddd9bbb0b835759649d8391` (§1, §2 O-1, §8), with `sq.dossier.valid.examples.json` `426165ba047ac7c53edb1d81debb0f917121866ebbdd7fd7ecc00bca835de7db`.
  - DEL-09-07 DOS-v0.1 `QUALIFICATION_DOSSIER.md` (§1, §4 DH-1/DH-2, §6 DF-5, DX-1…DX-3). RP-v0.4 deliberately re-pins `lhq.dossier-manifest.valid.examples.json` to O-C's DX-3 version (commit `aa95aff4e1`; sha256 `dbf8463f45dc2b9c…`, vendored; RV3 N9). In it, `DOS-EXAMPLE-INVENTED` names no run and no receipt and has no DEL-09-11 hand-over, and `DOS-EXAMPLE-INVENTED-POPULATED` keeps RC-1 in all three places. FX-RP1-3 stays pinned to the earlier copy (`9873df65…`) as history.
  - DEL-11-01 CA-v0.2 and DEL-11-02 AA-v0.1 (this unit): `ca.continuity-account.schema.json` `$defs/continuity_handoff` and `aa.adoption-account.schema.json` `$defs/adoption_status`, with the built hand-overs `RUN/F/ca/records/CA-1.handoff.json` and `RUN/F/aa/records/AA-1.status.json`. The CA hand-over:, and the built hand-over `RUN/F/ca/records/CA-1.handoff.json`.
  - **Vendored supplier bytes (R23-44).** Every supplier schema and example the checks read is copied into `RUN/F/vendor/` with its source path, sha256 and source commit (`vendor/VENDOR.json`). The checks read the copies; `check_rp.py` V-1 verifies them, and prints a NOTICE (it does not fail) when a live source has moved since vendoring, so that the owner re-pins deliberately (R23-21).
  - DEL-09-07 LHQ-v0.2 (R23-36; committed at `141a6cc8b4`; its schema and examples vendored) `LOCAL_HOST_QUALIFICATION.md` `90f461cbbe98de20cdd19e13be6adb82818fa23ea55166cab04833108df8523e` (§3 CIR, CI-5 with LHQ2-R1: where both are given, the mapping agrees with the element's `value`, so consumers reconcile on the mapping; the OI-013/014 row). RP-v0.2 read the uncommitted `5cd31e09…`; the change adds the agreement rule only, which RP-R3 relies on and nothing else here changes, with `lhq.candidate-identification.schema.json` `3fb8f586b0bc1ca32c2ba4e82008e384109d3adc1189a0bf5091d598c46b5fc5` and `….valid.examples.json` `c7684ee595bcb1e91a6a3b86bb4a37022a0c4c57dfcacc3ffad8326b41b2d9d4`. RP-v0.1 relied on LHQ-v0.1 (`20361a0b…`); the fixture's CIR record is byte-identical in both versions.
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
| I-3 | Continuity hand-over (DEL-11-01 CA `$defs/continuity_handoff`; from RP-v0.4, replacing the first cut) | DEL-11-01 | DEP-11-03-008, held (SCC-006; F-R8: SCC-CASE-007 R1) | Packet assembly | Carried as *not supplied*; gap named |
| I-4 | Practitioner standing (first cut `$defs/practitioner_standing`) | DEL-09-12 | DEP-11-03-009, admitted | Packet assembly | Standing *not_supplied*; never a gap for replacement |
| I-5 | Adoption status: DEL-11-02's AA `$defs/adoption_status` (S-6, `owner_record`, from RP-v0.5) | DEL-11-02 | DEP-11-02-015, admitted (supplier's row) | Packet assembly | *not supplied*; gap G-ADOPT named |
| I-6 | v3.0.1 baseline identity | `reference/REFERENCES.md` §2 | DEP-11-03-010 (not topological; was UNKNOWN, F-R2) | Packet assembly | Packet not assembled |
| I-7 | EXP result records the dossiers cite; EXP change-impact records | DEL-09-01 records (EXP-v0.2) | through I-1/I-2 | Establishing an obligation | Obligation *not established* |
| O-1 | Package file (R23-24 shape) | The owner, when presented | DEP-11-03-014 (not topological) | **Any time** (R23-43). It states plainly what is and is not established, and claims replacement qualification only when both witnesses hold | — |
| O-2 | Disposition record | DEL-11-01 and affected consumers | DEP-11-03-015 (held), DEP-11-03-016 | After an attributable owner act | Disposition stays as recorded (§6.2) |

## 3. The packet manifest (`rp.packet-manifest.schema.json`)

One manifest per packet version.
- It names every supplied item by path and sha256, together with the source it was copied from (file, sha256, record id).
- It states what the rules (§4, §5) derive from those items. Nothing in it is filled from a definition.
- `evidence_standing` is `illustrative` whenever any supplier input is an example or fixture. An illustrative packet can establish nothing.
- `fixture` and `candidate.identified` (RP-v0.4; RV3 Addendum 4; RR-EUF3 #1). A packet whose candidate is not identified is refused unless it is a fixture. A fixture's package purpose **opens** with "FIXTURE, NOT FOR THE OWNER: no real candidate is identified", so a placeholder subject can never be put to the owner as a decision (RP-R6; B-45, B-47; A-20).
- **Both are derived, never declared (RP-v0.5; EUF4-R1).**
  - `evidence_standing` is `illustrative` if any supplied item's own standing is illustrative or a first cut; otherwise `candidate`.
  - `candidate.identified` holds only if all three hold:
    - the subject maps to EXP's `candidate_subject`;
    - its revision and build carry no placeholder marker (illustrative, invented, example, placeholder);
    - every counted core-loop result resolves to a record of an identified candidate.
  - A-9 recomputes both from the supplied copies. RP-R6 refuses a manifest whose declared values differ from the derivation, and decides the fixture refusal on the derived values. RV3's probe is now B-48: notice removed, `fixture: false`, standing "established", `identified: true`, placeholder subject still present. It is refused on both counts.
  - B-47, B-49 and B-50 are the positive and boundary controls.
- `core_loop.dossier_review.dossier_states_independent` shows the dossier's own claim of independence beside the review's resolved `state`, so the claim is not read as a review (RR-EUF3 #4). `journey.host_contributions` counts the CIR's contributions by LHQ ladder standing; "answered" is not counted as committed, delivered, adopted or examined (RR-EUF3 #3). `comparison_rule` says that no direct measurement of v3.0.1 exists (RR-EUF3 #5).
- Each supplied item states `produced_by` (who produced its content) and `source_kind`. For `copied_record`, `source` names the supplier file, its sha256 and the record. For `shape_only`, `source` says in words that the item is a first cut by the DEL-11-03 owner pending DEL-11-01's or DEL-09-12's own record, and `shape` names the `$def` it follows (RP-v0.3; RV3 EUF1-R3). `RUN/F/EU-F1.key-grounding.md` marks which key answers rest on these first cuts.
- The fixture carries its legend (the two RP schemas) inside it, so an input set no longer depends on live Design files (RP-v0.3; the lesson of IS-FX-RP1-1).
- `terms` defines every code or identifier the package, packet, disposition, excerpts and legend use (for example A16, P20-A, CIR, OI-nnn, DEP-001, DECISION-3, PEC, Domains, 'fallback'), so a person deciding without project context can read them. Codes inside the supplier copies keep their owners' vocabulary; the term "supplier records" says so and defines the few the packet copies (ST-4, U-SQ-5, TT-7). The builder refuses, and `check_rp.py` A-13 fails, any code in those texts with no term (RP-v0.3 widened the scope after RR-EUF2).
- `basis_excerpts` names a file of the exact passages the decision rests on, each with its source sha256: PRD §8, EXAMINATION §7, DEL-11-03 CLM-001, CLM-003, REQ-004, REQ-005 and AX-001, REFERENCES §2, and App v3's BUILD_AND_RELEASE §12, which underlies ALT-PUBLISHED's inference (reader issue I-7).
- `basis` quotes the reserving texts with their source sha256. The builder checks each quote against the current bytes.
- `baseline` is REFERENCES §2. `remote_rechecked` stays false until someone re-reads the published release. `comparison_rule` states how "at least at v3.0.1's level" is judged: by V4-EXM-10 and V4-EXM-11 passing on the candidate (EXAMINATION §7; F-R2; reader issue I-8). The baseline also carries the v3 reference limit: SQ's `v3_reference` values cite v3.0.0-era journeys (`266c121bb` is not an ancestor of the v3.0.1 source). They are context only.
- `not_established` always lists the six things the packet never establishes: replacement decision, public release, retirement, professional reliance, consumer adoption and practitioner validation.
- `gaps` names each missing contribution, its supplier and its point of need. **A gap holds back only the packet's claim of replacement qualification, never putting the packet to the owner** (R23-43). AX-001 says, in its own words: "A packet may accurately report partial or adverse evidence, but cannot claim replacement qualification until both applicable witnesses hold; even then the actual owner act remains separate." So a replacement-condition gap reads "before the packet can claim replacement qualification", quoting those words, and the other gaps read "carried for the owner; not a replacement condition". RP-v0.2's "presentation is not gated: DEL-11-03 AX-001" attributed to AX-001 something it does not say (RV3 EUF2-R1); RP-v0.1's "before the package is presented" invented a presentation gate. A-16 checks the wording. `open_matters` carries P-1, P-5, OI-024, OI-021, DEP-001, OI-016 (App v4) and the OI-013/014 residue, each with its owner.

### 3.3 Inputs from DEL-11-01 and DEL-09-12

- **Continuity (from RP-v0.4: DEL-11-01's own hand-over, CA-v0.1).** S-4 is a `copied_record` of `CA-1.handoff.json` (standing `owner_record`), validated against DEL-11-01's `$defs/continuity_handoff`. The packet repeats its results (A-21): thesis `matches`, archives `passed` (a real run of `archive_digests.py verify`), and continuing obligations `not_supplied`. The first cut below is **superseded** and kept only so that FX-RP1…FX-RP1-3 stay readable.
- **`continuity_input` (first cut, RP-v0.1…v0.3)** carried:
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
- Each element carries two facts, kept apart:
  - `recorded`, what the dossier records for its counted steps, in EXP's outcome vocabulary, worst first: `recorded_fail`, `recorded_blocked`, `recorded_not_run`, `recorded_inconclusive`, `recorded_pass`; or `not_recorded`;
  - `status`, what the evidence supports, with `status_reason` naming each non-pass step, its outcome and the step's own stated cause:
    - `met` only when every counted step resolves to a supplied EXP result record with `run_basis: candidate` and outcome `pass` (EXP-R3);
    - `not_met` only when a counted step resolves to a candidate record with outcome **`fail`**;
    - otherwise `not_evidenced`. A `blocked`, `not-run` or `inconclusive` step is a **missing result, not a failure** (SQ-R4; R23-20). It never yields `not_met`, whether or not it is resolved (RV3 EUF1-R1b, fixed in RP-v0.3; RP-v0.2 read any non-pass as `not_met`).
  - Example: S11-6 is recorded `blocked` because stimulus ST-4 was not produced ("route cannot delegate; no recording (U-SQ-5)", the record's own cause), an input gap. Restart is `recorded_blocked` and `not_evidenced`, and its gap says "a missing result, not a failure".
- The obligation is `met` only if all seven are `met`; `not_met` if any is `not_met`; otherwise `not_evidenced`.
- **Established** requires all of: obligation `met`; the dossier `handed_over` and `reported_as_independent` (SQ-R8); and no unresolved step.
- `dossier_review` reports the standalone dossier's own independent review separately from the journey's, and names what each covers. Its state is `present` only when the named review record resolves to a supplied record; a review the dossier names but nobody supplied (an illustrative one) is `named_not_resolved`, and it holds back "established" (RP-v0.3; RR-EUF2's point that an illustrative review read as present).
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

- **RP-R6:** see §6.1. The package validates against DEL-02-03's `$defs/decisionPackageFile`, and the rules there apply. RP-v0.4 adds:
  - with the manifest, an unidentified or illustrative candidate is refused outside a fixture, and a fixture's purpose must open with the fixture notice;
  - a consequence that rests on App v3's BUILD_AND_RELEASE must keep "manual" and "on request".
- **RP-R7:** see §6.2. RP-v0.5 adds: given its manifest, a fixture package is never `presented_no_decision` or `decided` (B-51, B-52).
- **RP-R8:** every supplied item's sha256 in the manifest equals the file. Each copied supplier record equals its source record at the named source sha256. The manifest's derived values recompute to themselves from the supplied copies.

## 5. Candidate identity (R23-33)

| Source | Form | Maps to EXP `candidate_subject` | Today |
|---|---|---|---|
| EXP-v0.2 `$defs/candidate_subject` | `{kind, app_candidate{revision, build_identity, packaged, package_record}, host_candidate, identification_record}` | Canonical | — |
| SQ-v0.2 `candidate` | `{revision, build_identity, codex_pin, package_record}` | `revision` and `build_identity` copied; `packaged` = whether `package_record` is present; `codex_pin` is configuration, not identity (EXP §3) | **Maps; no SQ row needed** |
| LHQ CIR `elements.app_candidate` with LHQ-v0.2's `app_candidate_subject` (CI-5; R23-36) | `app_candidate_subject` is a checked copy of EXP's `candidate_subject.app_candidate`; it is present only while the element is supplied | Copied as `app_candidate`; `host_candidate` from the CIR's host element; `identification_record` = the CIR id | **Maps** (B-18…B-23, on O-C's example `LHQ-CIR-EXAMPLE-MAPPED`) |
| The same element without `app_candidate_subject` | `{value, source, standing}`: one string | Cannot be split without inventing a convention | Not mappable (B-24) |

Reconciliation values:
- `reconciled`: both map, and their identities are equal **by EXP's identity semantics**: `revision`, `build_identity`, `packaged` (absent means `false`), and `package_record` when packaged. This is not a literal object comparison, so a CIR that omits `packaged` does not give a false `differ` against SQ's explicit `false` (RP-v0.3; RV3 EUF1-R4; B-24…B-26);
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

| ID | Statement (short) | Performs the public-release act | Needs it as a separate owner act | v3.0.1 remains the fallback without a further act | Retires anything |
|---|---|---|---|---|---|
| ALT-OWN-USE | The owner's own work moves to the candidate; v3.0.1 stays the published product and the fallback | no | no | yes | no |
| ALT-PUBLISHED | The candidate is to replace v3.0.1 as the published product, once the owner also performs the separate public-release act | **no** | **yes** (P-5; PRD OQ-08; CLM-003) | **yes**: until that act, v3.0.1 remains the published product and the fallback | no |
| ALT-DEFER | Decide again when the named gaps close | no | no | yes | no |
| ALT-DECLINE | This candidate does not replace v3.0.1 | no | no | yes | no |

RP-v0.3 states what choosing ALT-PUBLISHED does (RV3 EUF1-R2). Choosing it does not perform the release, and the release stays the owner's separate act (P-5). RP-R6 refuses an ALT-PUBLISHED that does not say so (B-35). "Fallback" is defined in the packet's terms: the published product that stays in place until the owner decides v4 has replaced it. Which App the owner personally uses is not the fallback.

The `purpose` says plainly where the packet stands (R23-43; RR-EUF2's question about choosing on incomplete evidence):
- "V4-REP-01 states when v4 may replace v3.0.1; the packet states what is and is not established". Here it adds "the two witnesses are not shown to hold, so it does not claim replacement qualification".
- "Choosing any alternative remains the owner's act, on the evidence as presented; this package neither forbids nor recommends a choice."

The package invents no gate and implies no permission. RP-R6 requires the choice sentence (B-36). A-19 requires the qualification claim to match `replacement_evidence.complete`.

`subject[0]` asks "whether, and at what scope", and ALT-OWN-USE's statement says what it replaces: v3.0.1 in the owner's own work only (RP-v0.2; reader issue I-3). `purpose` names the act in words: A16, 'decide', choosing exactly one alternative (reader issue I-1). ALT-PUBLISHED's consequences include an inference, labelled as one. App v3's records (`BUILD_AND_RELEASE.md` §12, excerpted) say "Manual checks read its latest published stable release" and that a newer installer "opens in the system browser on request". So, after the release act, v3.0.x's manual update check would on request open v4's installer or release page. RP-v0.3 had dropped "manual" and "on request" (RV3 Addendum 4). Every alternative states "No retirement" (RP-R6). The package holds no recorder element (R23-24).

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
- A fixture package is never presented or decided (RP-v0.5; EUF4-R1).
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
5. When the coordinator puts the package to the owner: `presented_no_decision`. This may be at any time (R23-43). The packet states what is and is not established, and claims replacement qualification only when both witnesses hold. The owner's act stays separate and is the owner's to make on the evidence as presented.
6. When the owner acts: `decided`, recorded as in §6.2.
7. Return the disposition to DEL-11-01 and the affected consumers.

A supplier change makes a new manifest version, and so a new package. An earlier package and its disposition stay as history.

## 7. Failure behaviour

| # | What fails | Record left | Next |
|---|---|---|---|
| RF-1 | A supplier handoff is missing | Gap with supplier and point of need; obligation *not evidenced* | Packet kept and may still be put to the owner, stating the gap; no claim of replacement qualification (R23-43) |
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
| **EU-F1 consumption check** | REQ-004 (the owner can decide from the files) | An isolated reader given only the input set answers fixed questions; an examiner compares the answers with the frozen key, field by field | RR-EUF1 on IS-FX-RP1-1 (RP-v0.1): 33/33 fields, 11 issues. RR-EUF2 on IS-FX-RP1-2 (RP-v0.2): 33/33, 10 issues. Each issue is judged in O-F.md. IS-FX-RP1-3 (RP-v0.3, Q-1…Q-13) is staged and keyed, not read |

Prototype at freeze (RP-v0.5, fixture FX-RP1-5): `check_rp.py` **76/76**. It adds:
- A-9 now recomputes the derived standing and identification;
- A-22: adoption status is DEL-11-02's own;
- B-48…B-52: RV3's probe, the derivation controls, and fixture presentation and decision refused.

`--fixture FX-RP1-3` and `--fixture FX-RP1-4` give 13/23 and 18/23 under the current rules: earlier fixtures, as history.

At RP-v0.4 (fixture FX-RP1-4), `check_rp.py` was **70/70**. It added:
- A-20: fixture and identification;
- A-21: the continuity hand-over is DEL-11-01's own;
- B-45…B-47: the non-fixture refusal, the inference wording, and a real-packet positive control.

The basis excerpts now include DEL-11-03 REQ-006, VER-003 and VER-004, and R23-32 and R23-43, so that every clause the terms say is excerpted is excerpted (RV3 Addendum 4; RR-EUF3 #7). `check_rp.py --fixture FX-RP1 / FX-RP1-2 / FX-RP1-3` gives 8/22, 11/22 and 13/22 of Part A and V-1 under the current rules and the re-pinned vendor copies.

At RP-v0.3 (fixture FX-RP1-3), `check_rp.py` was **65/65**:
- A-1…A-19: the fixture, including the legend it carries (A-18) and the purpose against completeness (A-19);
- V-1: vendoring;
- B-1…B-44: rule cases. Among them, blocked, not-run and inconclusive are never `not_met` (B-4, B-6); only fail is (B-5). An illustrative review is never `present` (B-12). O-C's repaired DOS examples supply the receipt cases (B-13…B-15). Identity semantics are covered by B-24…B-26, and the ALT-PUBLISHED and purpose refusals by B-35 and B-36.

`check_rp.py --fixture FX-RP1` and `--fixture FX-RP1-2` reproduce which current checks the earlier fixtures fail (RV3 N4): 9/20 and 12/20 of Part A and V-1.

`compare_rp.py` validates each set's account against that set's own schema. RP-v0.2's tool always used set 1's schema, which is why it reported RR-EUF2's valid account as invalid. Self-checks: set 3 18/18 (16 plus Q-13 and the ALT-PUBLISHED release check). The builder is deterministic.

## 9. Open matters

| Item | Owner | Point of need | Effect here |
|---|---|---|---|
| RQ-LHQ-1: closed by R23-36 (LHQ-v0.2 CI-5, committed `141a6cc8b4`) | — | — | Reconciliation works on a CIR that supplies it (B-19…B-26) |
| EUF1-S1 (DOS example receipts): closed by O-C (DX-1, DX-2) | — | — | FX-RP1-3 uses the repaired example; B-13…B-15 use both examples |
| SQ dossier's `core_loop_element` is a free string | O-B (optional) | — | RP-R1's closed list catches drift (RF-5); no row requested |
| P-1 replacing v3.0.1; P-5 public release | The owner | P-1: the owner's act whenever the owner takes it, on the evidence as presented; the packet may be put to the owner at any time (R23-43). P-5: before public release | Prepared only; never performed or implied |
| OI-021, DEP-001, host joins (DECISION-3) | Owner via the SWB session; SWBPIPE | Before V4-EXM-20 can run | OUT-002 stays incomplete |
| OI-013/014 residue (App candidate's role in V4-EXM-20) | Shared contract owner with the SWB owner | Before the CIR's App element is fixed for CA/E | Carried |
| Remote re-check of REFERENCES §2 | DEL-11-03 coordinator | When a real package is prepared for the owner | `remote_rechecked: false` until then |

## 10. Changes

| Version | Change |
|---|---|
| RP-v0.5 (2026-10-04) | Unit EU-F3:
- EUF4-R1: `evidence_standing` and `candidate.identified` derived (`rplib.derive_standing`) and recomputed in A-9; RP-R6 refuses a declared/derived mismatch; RP-R7 refuses presenting or deciding a fixture; RV3's probe is B-48.
- S-6: DEL-11-02's AA-1 status (adoption supplied; G-ADOPT not raised).
- CA-1 v2 consumed.
- Fixture FX-RP1-5; manifest format RP-v0.5 |
| RP-v0.4 (2026-10-04) | With DEL-11-01 CA-v0.1 (unit EU-F2):
- the continuity hand-over adopted (S-4 `owner_record`);
- RV3 Addendum 4: an illustrative subject refused outside a fixture and announced in a fixture; ALT-PUBLISHED's "manual" and "on request" restored; REQ-006, VER-003 and VER-004 (and R23-32, R23-43) excerpted;
- N9: DOS examples re-pinned to DX-3;
- RR-EUF3 cheap fixes: `identified`, `dossier_states_independent`, `host_contributions`, the no-direct-v3.0.1 sentence;
- manifest format RP-v0.4; fixture FX-RP1-4.

No reader, keys or input sets added (R23-49) |
| RP-v0.3 (2026-10-04) | One repair round, covering RV3-EUF1 and RR-EUF2:
- EUF1-R1b: only a resolved `fail` gives `not_met`; blocked, not-run and inconclusive are missing results. `recorded` uses EXP's vocabulary; `status_reason` gives the causes.
- EUF1-R2: ALT-PUBLISHED does not perform the release, which stays a separate owner act.
- EUF1-R3: `source` and `shape` for first cuts, and `EU-F1.key-grounding.md`.
- EUF1-R4: reconciliation by EXP identity semantics.
- EUF2-R1 under R23-43: presentation at any time, a claim only when both witnesses hold, AX-001 quoted in its own words. Restated in §2 O-1, §3, §6.3 step 5, RF-1 and P-1.
- EUF2-R2: fixture FX-RP1-3 on O-C's repaired DOS example, under a new input set.
- N4: `check_rp.py --fixture`.
- R23-44: supplier bytes vendored; legend inside the fixture.
- RR-EUF2: the purpose states the qualification claim and the choice sentence; 'fallback' and the other codes the reader met are defined; an illustrative review is `named_not_resolved`; uncounted steps carry the dossier's reason.
- `compare_rp.py` validates each set's account against that set's own schema.
- Manifest format `RP-v0.3`; the disposition schema is unchanged. FX-RP1, FX-RP1-2, their input sets and keys are kept unchanged |
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
