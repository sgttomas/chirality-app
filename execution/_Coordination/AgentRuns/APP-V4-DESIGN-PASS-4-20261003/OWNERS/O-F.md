# O-F — owner notes and returns (DEL-11-01, DEL-11-02, DEL-11-03, DEL-09-12)

Owner: O-F (Type 2 TASK, Claude Opus 5.5, high effort; the S2-F survey agent). Method: `coordinated-knowledge-work` (WORKFLOW.md sha256 `44049bcd38b88378cd757ea34516f01edb0b0e93d8e9e3ac2b47ac61c9271b18`) under this run's work graph "Coordination". Rulings bound: R23-1…R23-33. They are cited by ID; R23-32 and R23-33 were read at `R23_RESOLUTIONS.md` sha256 `62bb5dae132edaea…`. Survey: `SURVEY/S2-F.md`.

Write area (HELP_HUMAN's assignment):
- new files in DEL-11-03 `Design/`, and later in DEL-11-01's, DEL-11-02's and DEL-09-12's;
- `RUN/F/`;
- this file.

Escalate only for:
- a restructure of an earlier Design file;
- a register row;
- an owner act requested or implied;
- a weakened check.

## Units

| Unit | Deliverable | Path (from `projects/chirality-app-v4/execution/`) | sha256 | State |
|---|---|---|---|---|
| EU-F1 | DEL-11-03 (early path for PKG-11 and DEL-09-12) | RP-v0.1…v0.3 | as recorded below | **PASSED as an early path (R23-49); RP-v0.3 READY (RV3 Addendum 4)** |
| EU-F2 | DEL-11-01 CA-v0.1 + DEL-11-03 RP-v0.4 | DEL-11-01 `Design/`, DEL-11-03 `Design/`, `F/` (incl. `F/ca/`) | see "EU-F2 — frozen" | **FROZEN 2026-10-04; for HELP_HUMAN to commit by path, then for review** |

## EU-F1 — frozen (RP-v0.1; superseded by the refreeze below, kept as the record RR-EUF1 read)

### Files (sha256 at freeze)

| File | sha256 |
|---|---|
| `PKG-11_…/DEL-11-03_…/Design/REPLACEMENT_PACKET.md` (RP-v0.1) | `1a06262bcf516972c745cf954e8b07d1b697b9f0732d9bd22020e4e372069c8c` |
| `PKG-11_…/DEL-11-03_…/Design/rp.packet-manifest.schema.json` | `456e438079314f2000174a733044bf6d5aff51de586f747c091ae679e6851b6c` |
| `PKG-11_…/DEL-11-03_…/Design/rp.disposition.schema.json` | `d5a69bc24d9ca346f4210c1a2ad9dee1407c6fb9f96af650f003258badbc99cf` |
| `F/rplib.py` | `1e0b224eea7273c1d785a67c70bcd668b86e133d5d151af5d8d04b47ba243ec6` |
| `F/build_fx_rp1.py` | `b3fad620c9683e0e162cecbd047cbf880bfaeffc30595bae26ba058b40ace6ca` |
| `F/check_rp.py` | `62011d9ec556fb0fe2ca503854237da387ab45cac56f6769b2af289ac4453eaa` |
| `F/compare_rp.py` | `bc72fb17dba653c4c60df30f18aadd5d548610be8de5c93ae70866ad023846ac` |
| `F/stage_is.py` | `6960810d5988c021c5bb9577ea45c8efbe00bd5ad8cbb693f36369b340f9a444` |
| `F/README.md` | `300fde37c564ea1b622de3f10e6d9c348be8abf9808d79a491621e7460c40209` |
| `F/READER_BRIEF.md` | `305dac85f95453db8c580678128ca4cbdcd2ae9708a4e942a20194f9f7f671ec` |
| `F/rp.reader-account.schema.json` | `be7f647185d6f21b312add31f16a5637bd2964c7a81e011c1f2ed8f1f7aa9f5b` |
| `F/fixtures/FX-RP1/MANIFEST.sha256` (8 files) | `96291b9c74dd499d80cc7506267c241d22843ab92621bb9f726ade872158211b` |
| `F/IS-FX-RP1-1.input-set.sha256` (13 files: the fixture, the brief, the account schema, the two RP schemas as `legend/`) | `125eb921fbcf1cb47a4bb8b95f4659a51a7e89cf4196660a66a65009a456a314` |
| **`F/EU-F1.answer-key.json` (withheld from the reader; fixed before any reader runs)** | **`ec0c8320fee434fc7f524445287f9e5c0be008d5b28e9885efbdc7648a3411c9`** |

Fixture identities:
- package file `pkg:app-v4:replacement:FX-RP1`, sha256 `7e5e8dbb…4db8`;
- packet manifest `RP-FX-RP1` v1, sha256 `c6c62225…9213`. The package's `subject[1]` names it;
- disposition `RPD-FX-RP1`, state `not_presented`.

### Claims

1. A replacement decision package can be assembled from the two tranche-1 dossier handoffs as they stand: SQ-v0.2's `handoff` and core-loop mapping, and DOS-v0.1's `handoff_del_11_03` with the CIR. It also takes first-cut continuity and practitioner inputs, the REFERENCES §2 baseline and the PRD §8 / EXAMINATION §7 basis. Every derived value recomputes from the supplied copies (RP-R8).
2. **R23-33 on real files.** SQ's `candidate` maps to EXP `candidate_subject` with no SQ change; the result validates against EXP's `$defs/candidate_subject`. The LHQ CIR's `app_candidate` element does **not** map: it is one string, and splitting it would invent a convention. This is row request RQ-LHQ-1 below. Until O-C acts, reconciliation with any CIR is `not_established`.
3. The R23-24 package shape fits a project-level reserved decision with no schema change (F-R4). `subject` names the candidate and binds the packet manifest's sha256, so a decision binds to the exact evidence. `reservedBy` cites PRD §8 and EXAMINATION §7. The four F-R5 alternatives each state their effect on v3.0.1, release and retirement. The file validates against DEL-02-03's `$defs/decisionPackageFile`.
4. RP-R1 makes the core-loop account per element over the seven REQ-001 elements:
   - SQ's V4-EXM-12 steps (element "model access") are set outside the core loop under EXAMINATION §7;
   - uncounted steps change nothing;
   - an element outside the closed list is an interface error;
   - "met" as recorded is kept apart from "established", which needs candidate EXP records.
5. RP-R2 applies DOS DH-1 as written, adding actor ≠ recorder and the review record.
6. RP-R4 and RP-R5: completeness needs both obligations established and one reconciled candidate. Practitioner standing is carried and never consulted (F-R3), and it is not a gap.
7. RP-R7: the disposition never holds a decision without an attributable owner act in the OWNER_DECISIONS form (F-R4). It keeps "v3.0.1 remains the fallback" while undecided and lapses on a changed package. The fixture's disposition is `not_presented`. **No owner act is requested or implied.**

### Checks run

- **Fixture and rules:** `python3 -B check_rp.py`: **44/44**.
  - A-1…A-12: integrity; manifest, disposition, package and candidate schemas; supplied items against their owners' schemas; copies equal their source records at the named sha256; recomputation; thesis tree at `d2929fd62b` equals PRD §11's; the six never-established items; practitioner not a gap.
  - B-1…B-32: rule cases, each negative paired with a positive control where one applies.
  - I printed the error texts of B-21, 22, 24, 29 and 30; each refuses for its own rule, not for an unrelated reason.
- **Determinism:** `build_fx_rp1.py` run three times gives the same bytes (MANIFEST.sha256 `96291b9c…211b` each time).
- **The key:** `compare_rp.py --self-check`: 16/16. The key was written by hand from the files, then checked against the fixture records wherever a record states the answer directly.
- **Staging:** `stage_is.py` staged exactly the 13 listed files into an empty temporary folder, and every hash matched. The key is not staged.
- **Pins:** every 64-hex pin in REPLACEMENT_PACKET.md (14) was recomputed and matched to its current file by script. The supplier Design folders are unchanged since `d150856784` (`git diff --stat`, `git status`).
- **Schemas:** the reader-account schema passes `Draft202012Validator.check_schema`. The quotes in `basis` are checked against current bytes by the builder.
- No network. `git` was used read-only. Nothing outside the write area was written. Scratch went to `$TMPDIR`.

### For the reader dispatch (HELP_HUMAN)

- Stage with `python3 -B F/stage_is.py <empty folder>`.
- Give the reader that folder and `READER_BRIEF.md`'s instructions. The reader returns `account.json`.
- I then run `python3 -B F/compare_rp.py <account.json>` and read the REFERRED statements and issues.
- **Pass:** every structured field holds, and no referred statement contradicts the records.
- Any mismatch is traced to its interface (SQ, DOS, CIR, EXP, DEL-02-03, or the first-cut DEL-11-01/DEL-09-12 inputs) before the four designs expand.

### Limits

- All supplier evidence is illustrative (schema examples). The unit tests the interfaces and the decision's legibility, not any qualification.
- The reader gets the two RP schemas as a legend. A presentation to the owner would need a rendered view. That is not designed in RP-v0.1.
- The thesis check is a committed-tree identity at a fixed commit, not a comparison of working bytes.
- REFERENCES §2's remote values were not re-checked (no network).

### Open

- RQ-LHQ-1 (below).
- The rendered view for presentation.
- DEL-11-01's and DEL-09-12's own files, which will supersede the first-cut `$defs`.
- RP-v0.1 §9.

## Row requests for other owners (R23-33; routed by HELP_HUMAN, not edited by O-F)

| ID | To | File | Request | Why | Restructure? |
|---|---|---|---|---|---|
| **RQ-LHQ-1** | O-C | DEL-09-07 `lhq.candidate-identification.schema.json` (LHQ-v0.1 §3) and its examples | Give `app_candidate` a form that maps to EXP `candidate_subject.app_candidate`: `revision`, `build_identity`, `packaged`, `package_record`. For example, an optional sibling `app_candidate_subject` holding that object, or a `$ref` to EXP's definition. Keep `{source, standing}` and `not_supplied`. The prototype uses the sibling form only in memory (B-15…B-17) | LHQ's element is one string; DEL-11-03 VER-003 cannot reconcile one candidate across the two obligations without inventing a split. R23-33 item 2 | No: an additive element. O-C to judge |
| (none) | O-B | SQ-v0.2 | No row needed. SQ's `candidate` maps cleanly. Note only: `core_loop_element` is a free string; RP-R1's closed list catches drift | — | — |

## Next, alongside the review wait (unchanged)

The DEL-11-02 D-GOV-52 adoption trace (F-R9, F-R10, F-R16) is a working draft, not frozen. It will be frozen only after EU-F1 leaves the review queue, so that no more than one unit waits.

## EU-F1 — reader result (RR-EUF1)

**Inputs.**
- The account is `RR-EUF1/account.json` (sha256 `b7570e01e9e86adba54b07c094d25147971f1f3a87fd4eae9a74de2f2569ca20`).
- `DISPATCH_RECORD.md` is `fcef54ad…`. `SUPPLIED.sha256` is `4dfdb38a…` and lists 14 files; its `legend/rp.packet-manifest.schema.json` entry (`456e4380…`) is the RP-v0.1 bytes.
- The reader reports that it read only the staged files, opened no repository and used no network. The host does not enforce that; separation rests on the brief and the reader's own report.

**Comparison:** `python3 -B F/compare_rp.py RR-EUF1/account.json`.
- The account is schema-valid and names IS-FX-RP1-1 by its sha256.
- **33/33 fields held.** 12 statements and 11 issues were referred.
- I read the 12 statements against the records. None contradicts them, and none claims an act, a decision or an established obligation. The Q-3 statement is accurate: six elements are marked met "on illustrative step results".

**Every issue, judged on the evidence.** "Real" means I confirmed it against the files.

| # | Reader's issue | Traced to | Judgment | Repair |
|---|---|---|---|---|
| I-2 | Six elements "met" while every step is unresolved and illustrative | **The packet's rule.** The derivation matched RP-v0.1's RP-R1 exactly: "`met` if every counted step is recorded `pass`" and "The status is what the dossier records". That rule contradicts EXP-R3 ("Only a `candidate` record stands for a scenario"). The rule's own principle, "established is what the evidence supports", was confined to the obligation | **Real defect, EUF1-D1.** "met" is a claim the evidence does not support, even in a fixture | RP-R1 now keeps `recorded` (what the dossier records) apart from `status` (met or not_met only with resolved candidate evidence; otherwise not_evidenced). FX-RP1-2: all seven elements not_evidenced (six recorded_pass, restart recorded_not_pass); obligation not_evidenced. A-17 and B-1…B-6 hold it |
| I-4 | 0 receipts in the packet, but the dossier lists RC-1 | **The packet's rule, and the supplier example.** RP-v0.1's RP-R2 read only `handoff_del_11_03.receipts` (empty). The same dossier names RC-1 (unresolvable) in `handoff_del_09_11.receipt_refs`, while its `host_evidence` index is empty although DOS §1 says that index lists every receipt the results cite | **Real defect, EUF1-D2** in the packet. **Supplier inconsistency, EUF1-S1** in DOS's example | RP-R2 now carries every receipt reference in the dossier, kept apart by where it appears. An omission from the DEL-11-03 handoff makes the journey not established (A-15, B-15, B-16). EUF1-S1 goes to O-C as a finding, not an edit |
| I-10 | Gaps "before the package is presented" in a never-presented fixture | **The packet.** DEL-11-03 AX-001 allows presenting "partial or adverse evidence", so a gap cannot gate presentation. RP-v0.1 implied a gate the contract does not have | **Real defect** (minor), found by examining the reader's issue | Points of need are now "before the replacement evidence can be complete" or "carried for the owner; not a replacement condition" (A-16) |
| I-1 | "A16" undefined | Packet legibility | **Needed by the person deciding**: it names what is being asked | `purpose` names the act in words; `terms` defines A16 (A-13) |
| I-6 | P20-A, O-C, O-F, RQ-LHQ-1, DECISION-3, DEP-001, OI-nnn, R23-32, B-HTML undefined | Packet legibility | **Partly needed.** P20-A, DECISION-3, DEP-001 and the OI codes bear on the decision, so they get terms. Agent IDs (O-C, O-F) and RQ-LHQ-1 are coordination internals, so they are removed from the packet: gaps name deliverables; the recorder is "DEL-11-03 coordinator (prototype builder)" | `terms` with 20 entries. The builder refuses any code without a term, and A-13 checks the fixture |
| I-3 | What ALT-OWN-USE replaces | Package wording | **Real legibility defect.** The subject said "replaces the v3.0.1 fallback", yet this alternative keeps v3.0.1 as the fallback | The subject asks "whether, and at what scope"; ALT-OWN-USE: "Replace v3.0.1 in the owner's own work only … For everyone else, v3.0.1 stays published and remains the fallback" |
| I-7 | Cited bases not supplied | Input set | **Partly needed.** The person needs the reserving texts, the comparison rule and the source of ALT-PUBLISHED's inference, not whole documents | `packet/basis-excerpts.md`: exact lines from PRD §8, EXAMINATION §7, DEL-11-03 CLM-001/003, REQ-004/005, AX-001, REFERENCES §2 and v3 BUILD_AND_RELEASE §12, each with its source sha256 (A-14) |
| I-8 | How "v3.0.1's level" is judged | Packet | **Real legibility gap.** F-R2's rule was not stated in the packet | `baseline.comparison_rule` quotes EXAMINATION §7's test |
| I-9 | Continuity and practitioner inputs "sourced from a schema" | Packet provenance | **Real, minor.** `source` named the schema `$def`, which gave only the shape; the content came from DEL-11-03's builder | `produced_by` and `source_kind` (`copied_record` or `shape_only`). The thesis result's method and commit are stated; that it cannot be re-run from the input set alone is a stated limit |
| I-5 | Two review records, one present and one absent | Packet legibility | **Not a defect** (different obligations), but unclear | `core_loop.dossier_review` reports the standalone dossier's review and what it covers, beside `journey.independent_review` (B-11) |
| I-11 | Placeholder hashes in the LHQ dossier | Supplier example | **Not a defect.** The example marks them invented, and the packet's `evidence_standing: illustrative` already says so | None |

**The reader:** no misreading found. The reader matched every field and caught the two real defects that the key, the checks and I had missed.

**Finding on the key, KEY-F1.** The frozen key `EU-F1.answer-key.json` (`ec0c8320…`) is unchanged. Its Q-3 `elements` (six "met") and Q-3 `obligation` ("not_met") encode the defective RP-R1 (EUF1-D1). The reader's 33/33 therefore shows only that the reader reproduced what the packet said. It does not show that the packet said something supportable. `compare_rp.py --self-check` of the original key against the repaired fixture fails on exactly Q-3 `elements` and `obligation`, plus Q-1 `package_id`, which changed by design: a changed manifest means a new package. Lesson: the key self-check confirms agreement with the fixture, not the soundness of the rules behind it. That is the gap workflow §3 names.

## EU-F1 — refrozen as RP-v0.2 (for RV3)

**What changed.**
- RP-R1 and RP-R2 (EUF1-D1, EUF1-D2).
- Gap points of need (AX-001).
- `terms`, `basis_excerpts`, `comparison_rule`, `produced_by` and `source_kind`, and `dossier_review`.
- Package wording (I-1, I-3).
- LHQ-v0.2 CI-5 mapping (R23-36), exercised on O-C's real example `LHQ-CIR-EXAMPLE-MAPPED`. It validates against LHQ-v0.2's schema, maps to a valid EXP `candidate_subject`, gives `differ` against the illustrative SQ candidate, `reconciled` against an equal identity, and `reconciled_by_applicability` with a change-impact record (B-18…B-24).

New fixture **FX-RP1-2** and input set **IS-FX-RP1-2**, with their own key written before any reader. FX-RP1, IS-FX-RP1-1 and the original key are kept unchanged.

| File | sha256 |
|---|---|
| `PKG-11_…/DEL-11-03_…/Design/REPLACEMENT_PACKET.md` (RP-v0.2) | `80e88983a4822c6d76b257e72cff39166817371cf7e2723afc6541c3f3da1869` |
| `…/Design/rp.packet-manifest.schema.json` (format RP-v0.2) | `7dd6dee7a1214bbce1e55ad89d58fd0c5ae77d20e600017854425a23650270f6` |
| `…/Design/rp.disposition.schema.json` (unchanged) | `d5a69bc24d9ca346f4210c1a2ad9dee1407c6fb9f96af650f003258badbc99cf` |
| `F/rplib.py` | `2589ccf0b6ea80fcec0780c68c90688767a6da93d6c9e16f7ef55f1e2a2a3de8` |
| `F/build_fx_rp1.py` | `532219a398c78f6b18d9c0b6919572943c1199d41e462d896d653b2f404219e1` |
| `F/check_rp.py` | `e2886b4dfacef8725aed0dd66035708484c978abf2afe07d4ccf21ff105b987b` |
| `F/compare_rp.py` | `2d76e4f3f3841140105890bc8bba1de073c01ba5f7046dc35ef8c370e1259fcf` |
| `F/stage_is.py` | `120d9eae573502feaef914adece9a1179e52eb6c5006ec63993b05f254c0c17e` |
| `F/README.md` | `ba0b03f3ca3167b284a1a0c5d4fd698d00405d9d26859233f46da0b00f218a2e` |
| `F/fixtures/FX-RP1-2/MANIFEST.sha256` (9 files) | `534cd2104396bf02fdfb768159b8dbaeb6d43f492bc61e6e05222c8e29a1a0fa` |
| `F/IS-FX-RP1-2.input-set.sha256` (14 files) | `e1fd19df81add5b07ce5d06027bbd253121390fb35a02d821c6a6c6d3934c930` |
| `F/READER_BRIEF.v2.md`, `F/rp.reader-account.v2.schema.json` | `0a0bd4db…c47c4`, `7c8e689f…d300` |
| `F/EU-F1-2.answer-key.json` (IS-FX-RP1-2; withheld; written before any reader) | `52eaf68e49c0d269783d40e8a30cb34a8fa0eddc4778c8883593a67fba1215d7` |
| `F/EU-F1.answer-key.json` (IS-FX-RP1-1; **unchanged**) | `ec0c8320fee434fc7f524445287f9e5c0be008d5b28e9885efbdc7648a3411c9` |

Fixture identities:
- package `pkg:app-v4:replacement:FX-RP1-2`, sha256 `61e53c08…6c16b`;
- packet manifest `RP-FX-RP1` v2, sha256 `7835b07f…1092`;
- disposition `RPD-FX-RP1-2`, `not_presented`.

**Checks run at refreeze.**
- `check_rp.py`: **57/57**. A-1…A-17 cover the fixture; B-1…B-40 are rule cases with paired positive controls.
- New A-13, A-15, A-16 and A-17 each **fail on the RP-v0.1 fixture**, as they should (run against `fixtures/FX-RP1`). They would have caught the confirmed defects.
- The builder is deterministic (two runs, same bytes) and refuses a code without a term.
- `compare_rp.py --set 2 --self-check`: 16/16.
- `compare_rp.py RR-EUF1/account.json` (set 1, frozen key): still 33/33.
- `stage_is.py --set 2` staged 14 files with every hash matching.
- All 15 64-hex pins in RP-v0.2 were recomputed; 14 match current files and 1 is the superseded RP-v0.1, as stated.
- No home path is in any written file (grep).

**Limits.**
- **IS-FX-RP1-1 can no longer be staged.** Its legend schema was overwritten by the RP-v0.2 schema, and `stage_is.py` refuses it by hash. Its bytes are attested only by `RR-EUF1/SUPPLIED.sha256` and this file. Lesson: an input set should carry copies of its legend, not live references.
- LHQ-v0.2 is O-C's uncommitted working bytes, pinned as such.
- All supplier evidence is still illustrative.
- A second reader on IS-FX-RP1-2 is prepared but not requested. Whether RV3's review suffices is HELP_HUMAN's call.

**Findings for other owners (routed by HELP_HUMAN; not edited by O-F).**
- **EUF1-S1, to O-C:** DOS's example `DOS-EXAMPLE-INVENTED` is internally inconsistent. Its `handoff_del_09_11.receipt_refs` names RC-1, while `host_evidence` and `handoff_del_11_03.receipts` are empty, and DOS §1 says the index lists every receipt the results cite. Inference: either the index and the DEL-11-03 handoff should list RC-1, or the DEL-09-11 handoff should not.
- No escalation: no earlier Design file was restructured, no register row was added, no owner act was requested or implied, and no check was weakened. The check set grew from 44 to 57; nothing was removed except the cases RP-v0.1's defective rule encoded, which were replaced by stricter ones.

## RV3-EUF1 checked against RP-v0.2 — repair held (R23-41)

`reviews/RV3-EUF1.md` reviewed RP-v0.1 and returned REPAIR (1 MAJOR, 3 MINOR, 3 NOTE). RP-v0.2 is committed at `d43665498d`. I checked it against git: every DEL-11-03 `Design/` file and every `F/` file is tracked, and the working tree is clean. RP-v0.2 is the unit under review, so **nothing in it is edited** until the second reader (RR-EUF2) returns. These notes are not part of the unit.

Each finding was tested against RP-v0.2's own committed code and fixture (a read-only script run from `F/`):

| Finding | State in RP-v0.2 | Evidence | Repair planned for RP-v0.3 |
|---|---|---|---|
| **EUF1-R1** (MAJOR), first half: `met` from records alone | **Fixed** by EUF1-D1 | FX-RP1-2: all seven elements `not_evidenced`; A-17, B-1 | None further |
| **EUF1-R1**, second half: `blocked` merged into `not_met` | **Still open** | With S11-6's record resolved to a candidate record, RP-v0.2 gives restart `recorded_not_pass` / `not_met` and the obligation `not_met`. B-4 encodes this. S11-6 is `blocked` by an input gap (SQ U-SQ-6, SF-8), not a candidate defect | `recorded` keeps the step outcomes in EXP's vocabulary (`pass`, `fail`, `blocked`, `not-run`, `inconclusive`). An element is `not_met` only on a resolved `fail`. A resolved `blocked`, `not-run` or `inconclusive` step makes it `not_evidenced`, with the outcome and its cause shown. Gap text says "blocked by an input gap" apart from a failure. B-4 is replaced by a blocked case (→ `not_evidenced`) and a fail case (→ `not_met`) |
| **EUF1-R2** (MINOR): does choosing ALT-PUBLISHED perform the release? | **Still open** | The package's first consequence still reads, unconditionally, "v3.0.1 is no longer the fallback for the published product" | The statement and consequences say that choosing ALT-PUBLISHED does **not** perform the public-release act (P-5, OQ-08), which stays a separate owner act, and that until it is performed v3.0.1 remains the published product and fallback. RP-R6 checks the wording. A future key would ask `performs_release_act` and `requires_separate_release_act`, not the ambiguous `also_a_public_release_act` |
| **EUF1-R3** (MINOR): key answers resting on O-F's first-cut inputs | **Partly addressed** | RP-v0.2 added `produced_by` and `source_kind: shape_only` for S-4/S-5. But `source.path` still names the schema `$def`, and neither key marks its grounding (EU-F1-2 `why` covers only Q-3, Q-6, Q-7) | `source` relabelled "first cut by the DEL-11-03 owner pending DEL-11-01 / DEL-09-12" (shape cited separately). The frozen keys are not edited: a new `F/EU-F1.key-grounding.md` marks each answer of both keys as grounded in a supplier record, a packet derivation, or O-F's first-cut input. Q-9 and Q-11 are first-cut; Q-12 partly |
| **EUF1-R4** (MINOR): literal comparison gives a false `differ` | **Still open** | A CIR `app_candidate_subject {revision r1, build_identity b1}` against SQ `{r1, b1}` gives `differ` | Compare by EXP identity semantics: absent `packaged` means `false`; compare `revision`, `build_identity`, `packaged`, and `package_record` when packaged. New B-cases: omitted versus explicit `false` → reconciled; packaged versus not → differ; different `package_record` → differ |
| N1 (A-8 after LHQ-v0.2) | Resolved in RP-v0.2 | The rebuild recorded the new source sha; A-8 holds | — |
| N2, N3 | Observations | — | — |

The one repair round, after RR-EUF2, covers these plus whatever the second reader's account shows. It is refrozen as RP-v0.3 with a new fixture and input-set id, and FX-RP1, FX-RP1-2 and both keys are kept unchanged.

## EU-F1 — RR-EUF2 result

**Account:** `RR-EUF2/account.json` (`0d53d0890106e712…`). `DISPATCH_RECORD.md` is `8c1e443e…`; `SUPPLIED.sha256` is `93d9a224…`.

**Score.** `python3 -B F/compare_rp.py --set 2 RR-EUF2/account.json`: **33/33 fields held**, 12 statements and 10 issues referred.
- The account is valid against the v2 account schema (checked with `jsonschema` directly).
- The tool's first line read "FAILS account valid against rp.reader-account.schema.json". **That was a defect in my tool, not in the account**: RP-v0.2's `compare_rp.py` validated every set against set 1's schema. It is repaired in RP-v0.3, and each set now uses its own schema.

**Statements.** None of the 12 contradicts the records.
- The Q-3 statement reads restart's "not-pass (S11-6 blocked)" correctly, without calling it a failure.
- The Q-7 statement repeats RP-v0.2's ALT-PUBLISHED wording, which RV3 EUF1-R2 found unclear; it is repaired below.

**Issues, judged on the evidence.**

| # | Reader's issue | Traced to | Judgment | RP-v0.3 |
|---|---|---|---|---|
| 1 | Brief file name | Dispatch prompt | HELP_HUMAN's slip; no change needed. The v2 schema's description also says `READER_BRIEF.md` | The v3 schema names `READER_BRIEF.v3.md` |
| 2 | Choosing a replacing alternative on incomplete evidence: permitted? | Package | **Real gap.** The files did not say | Resolved under R23-43. The purpose states that V4-REP-01 says when v4 may replace v3.0.1, that the packet says what is and is not established, that here the two witnesses are not shown to hold, so it claims no qualification, and: "Choosing any alternative remains the owner's act, on the evidence as presented; this package neither forbids nor recommends a choice." P-1's point of need is restated. No gate is invented and no permission implied. RP-R6 (B-36) and A-19 hold it |
| 3 | Scope of "fallback" under ALT-OWN-USE | Package | **Real ambiguity** | `terms` defines "fallback": the published product that stays in place until the owner decides v4 has replaced it; which App the owner personally uses is not the fallback. ALT-OWN-USE's statement points to that term |
| 4 | Restart: not-pass shown as not_evidenced, like the six passes | Packet legibility | The reader read it correctly (blocked is not a failure). The status alone hid the adverse record | `recorded` now uses EXP's vocabulary (`recorded_blocked`), and `status_reason` gives "S11-6 recorded blocked (ST-4 not produced: route cannot delegate; no recording (U-SQ-5)): a missing result, not a failure". Blocked is never merged into not_met (EUF1-R1b) |
| 5 | An illustrative "independent review" read as present | **Packet rule** | **Real defect (EUF2-D1)**, of the same kind as EUF1-D1: `dossier_review.state` was `present` because the dossier named a review record, though nothing resolved it | State is `present` only when the review record resolves; otherwise `named_not_resolved`, which holds back "established" (B-12) |
| 6 | Continuity input produced by the packet builder | Packet provenance | A disclosed limit, also RV3 EUF1-R3 | `source` says "none: first cut by the DEL-11-03 owner, pending DEL-11-01's own record"; `shape` names the `$def`; `EU-F1.key-grounding.md` |
| 7 | Fallback identity and the ALT-PUBLISHED consequence rest on unchecked or inferred facts | Packet | Not a defect: each is already labelled (`remote_rechecked: false`; "inference"; the v3 reference limit) | None |
| 8 | Undefined codes | Packet scope and legend | **Real, partly.** Some codes the person deciding meets were outside the term check: the legend's descriptions (RP-R1, R23-33, F-R4…), the excerpts (D-11, U2, PEC, Domains, OD-09, D-APP-131, SOW-113, S1…) and copied causes (ST-4, U-SQ-5, TT-7). Codes inside supplier copies (DEP-09-07-011, LHQ §7 …) are the suppliers' own vocabulary | The term check now covers the package, packet, disposition, excerpts and legend; internal finding ids are removed from the legend; a "supplier records" term explains supplier vocabulary and defines the copied ones; "answered" is defined |
| 9 | The CIR lists host contributions as "answered" while no candidate exists | Supplier record | Not a packet defect; a legibility risk | Term "answered": nothing committed, delivered or adopted by that (DEP-001; DECISION-3) |
| 10 | Uncounted reuse runs and WR TT-7 | Packet | **Real, minor**: the packet dropped the dossier's own reason | Uncounted steps carry `dossier_reason` (B-9); TT-7 and WR are defined |

**The reader:** no misreading. **The key (EU-F1-2):** fair, as RV3 also judged. Its Q-7 inherits EUF1-R2 (the key grounding records this).

**Observation for HELP_HUMAN.** RV3 and your message cite U-SQ-6 as S11-6's blocking cause. The record itself (SQ-EX-05, S11-6) cites **U-SQ-5**: ST-4 was not produced, "route cannot delegate; no recording (U-SQ-5)". U-SQ-6 concerns ST-5, which in this record was produced by replay. RP-v0.3 copies the record's cause. The conclusion, an input gap and not a candidate defect, is the same.

## EU-F1 — RP-v0.3 (refrozen; one repair round, covering RV3-EUF1 and RR-EUF2)

**Findings addressed, each checked in the files:**

| Finding | Repair | Held by |
|---|---|---|
| RV3 EUF1-R1b (blocked merged into not_met) | `not_met` only on a resolved `fail`; blocked, not-run and inconclusive are `not_evidenced`, with outcome and cause | B-4, B-5, B-6, A-17 |
| RV3 EUF1-R2 (ALT-PUBLISHED) | "Choosing this alternative does not perform the public-release act; publishing remains a separate owner act (P-5; PRD OQ-08; DEL-11-03 CLM-003)"; "Until the owner performs that act, v3.0.1 remains the published product and the fallback" | RP-R6, B-35; key 3 Q-7 |
| RV3 EUF1-R3 (first-cut grounding) | `source` and `shape` for first cuts; `EU-F1.key-grounding.md` (keys unchanged) | A-2, A-7 |
| RV3 EUF1-R4 (literal comparison) | `identity_key`: revision, build_identity, packaged (absent means false), package_record when packaged | B-24, B-25, B-26 |
| RV3 EUF2-R1 under R23-43 | Gaps: "before the packet can claim replacement qualification (AX-001: a packet \"cannot claim replacement qualification until both applicable witnesses hold\"); it does not hold back putting the packet to the owner". Restated in §2 O-1, §3, §6.3 step 5, RF-1, P-1 and the purpose | A-16, A-19, B-36 |
| RV3 EUF2-R2 (DOS example moved) | FX-RP1-3 is built on O-C's repaired `DOS-EXAMPLE-INVENTED` (no receipts). B-13…B-15 use `DOS-EXAMPLE-INVENTED-POPULATED` and the repaired example from the vendored file | A-8, A-15, B-13…B-15 |
| RV3 N4 (`--fixture` ignored) | `check_rp.py --fixture NAME`: FX-RP1 gives 9/20 and FX-RP1-2 gives 12/20 of Part A and V-1. That reproduces my RP-v0.2 claim (A-13, A-15, A-16, A-17 fail on FX-RP1) and shows what the RP-v0.2 fixture now fails (A-8, A-16, A-19 …) | reproduced |
| R23-44 | Supplier bytes vendored in `F/vendor/` with source commit; legend inside the fixture; drift reported as a NOTICE | V-1, A-18 |
| RR-EUF2 #2, 3, 4, 5, 8, 9, 10 | As in the table above | B-9, B-12, A-13 |
| My tool defect (compare schema per set) | `compare_rp.py` uses each set's own schema | set 2 RR-EUF2 account now HOLDS |

**Files at refreeze** (sha256). These are the unit's paths for the R23-41 commit.

| File | sha256 |
|---|---|
| `PKG-11_…/DEL-11-03_…/Design/REPLACEMENT_PACKET.md` (RP-v0.3) | `164c082c1ef4957acf9edca1040dd4e76e2647a0a1af540d755d992f3a58f9af` |
| `…/Design/rp.packet-manifest.schema.json` (RP-v0.3) | `20de252d9b766d43c365a236c8e17c6f1d35ae4acbfc24a4cfdf5e2a2c768b64` |
| `…/Design/rp.disposition.schema.json` (unchanged) | `d5a69bc24d9ca346f4210c1a2ad9dee1407c6fb9f96af650f003258badbc99cf` |
| `F/rplib.py` | `89fc8e64fa17730cd767c04a12a5c4fa18e36efc53e1b1f7009deb7e66fff04d` |
| `F/build_fx_rp1.py` | `4bdad3a782ceadca7669273d30fa2f98bc83224a77044a46e49036c840fac59c` |
| `F/check_rp.py` | `11104deddfb00b92ded78b1296a1be948ba8b7c6cf76e0a083523c3dd010a076` |
| `F/compare_rp.py` | `208903ab35b949274788b1d6969603cf9302d37c12782b66b8a15a9a80fe9416` |
| `F/stage_is.py` | `5845d0294ead9319ee911cac43d1dada6e1f55efd2a679a09ed714cd00f02a0c` |
| `F/README.md` | `ef6cf1f4d6800b1094c92a7e1474a2a1727be30bd1fd038c916355221f5adfd2` |
| `F/EU-F1.key-grounding.md` | `7158f256e08b2051f2315f69fe9bdc78c351120c512166e6b066e84f0b5e5709` |
| `F/vendor/VENDOR.json` (+ 8 vendored files listed in it) | `4d9e41587d9af16c51a27ae9b3d9f4edb74b66c6e29248c36cb305f5006b8dea` |
| `F/fixtures/FX-RP1-3/MANIFEST.sha256` (11 files, legend included) | `ca5c86654fbdaf52f9428edb69c2cd9313cc0dfb5f0657b68da4c79b2639452a` |
| `F/IS-FX-RP1-3.input-set.sha256` (14 files) | `537d8b8173fb6843917af323b66cf1ea83bdc52125d5ebd35cd5a894259f83a7` |
| `F/READER_BRIEF.v3.md`, `F/rp.reader-account.v3.schema.json` | `9167cc57…0bbce0e`, `e163fff3…3d7c9b` |
| **`F/EU-F1-3.answer-key.json`** (withheld; written before any reader) | **`808737109f876cc2d22e41c11ba3a6ce72ba038ca33a8ff06cdaa4ef6f33caff`** |
| Unchanged history: `EU-F1.answer-key.json`, `EU-F1-2.answer-key.json`, `fixtures/FX-RP1/`, `fixtures/FX-RP1-2/`, input sets 1 and 2 | as committed at `d43665498d` |

Fixture identities:
- package `pkg:app-v4:replacement:FX-RP1-3`, sha256 `47ee064a…5b361d`;
- manifest `RP-FX-RP1` v3, sha256 `a3274e75…cdb31`;
- disposition `RPD-FX-RP1-3`, `not_presented`.

**Checks at refreeze.**
- `check_rp.py`: **65/65**, with no NOTICE (every live supplier file equals its vendored copy).
- The builder is deterministic (two builds, `cmp` equal), and it refuses a code without a term.
- `compare_rp.py --set 3 --self-check`: 18/18. `--set 2 RR-EUF2/account.json`: 33/33, schema HOLDS. `--set 1 RR-EUF1/account.json`: 33/33.
- `stage_is.py --set 3`: 14 files staged, every hash matching.
- 13 pins in RP-v0.3. Eleven match current files. Two are superseded versions, stated as such: RP-v0.2 `80e88983…` and LHQ `5cd31e09…`. LHQ is re-pinned to its committed `90f461cb…`, which adds only LHQ2-R1.
- No home path in any written file (grep).
- Nothing in RP-v0.2's committed bytes or the earlier fixtures and keys was changed (`git status` shows only the RP-v0.3 paths).

**Limits.**
- All supplier evidence is illustrative.
- Input sets 1 and 2 cannot be restaged (their legend was live), which is why set 3 carries its own.
- IS-FX-RP1-3 is staged and keyed but not read. A third reader is HELP_HUMAN's call; RV3's confirmation may suffice. Q-13 and the new Q-7 fields would test R23-43 and EUF1-R2 directly.

**No escalation.**
- No earlier Design file restructured.
- No register row.
- No owner act requested or implied.
- No check weakened. Checks went from 57 to 65; the ones changed are those that encoded RV3's findings (old B-4, the A-16 wording), replaced by stricter ones.

## RR-EUF3 judgments (R23-49: EU-F1 passed; no fourth reader)

`RR-EUF3/COMPARE.txt`: **36/36 fields**, 8 issues referred. `compare_rp.py --set 3 RR-EUF3/account.json` reproduces 36/36. Each issue is judged on the files:

| # | Issue | Traced to | Judgment | Where fixed |
|---|---|---|---|---|
| 1 | No identifiable candidate in the subject; the alternatives read as if one existed | Packet | **Real** (also RV3 Addendum 4, MINOR 1): no rule kept a placeholder subject from reaching the owner | RP-v0.4: `candidate.identified`, `fixture`; refused outside a fixture; a fixture's purpose opens with "FIXTURE, NOT FOR THE OWNER: no real candidate is identified" (B-45, B-47, A-20) |
| 2 | DOS example: "not run", yet run artefacts in its DEL-09-11 hand-over | Supplier example | O-C's; routed by HELP_HUMAN and fixed by DX-3 | RP-v0.4 re-pins to the DX-3 example (RV3 N9) |
| 3 | CIR contributions all "answered" read as progress | Supplier vocabulary; packet legibility | Real, minor | `journey.host_contributions` counts by ladder standing (13 answered; 0 committed, delivered, adopted or examined) |
| 4 | The dossier says independent while its review is unresolved | Packet legibility | Real, minor (RP-v0.3 already showed `named_not_resolved`) | `dossier_review.dossier_states_independent` beside `state` |
| 5 | No measured v3.0.1 baseline | Basis (F-R2) | By design; the packet now says it | `comparison_rule`: "no direct measurement of v3.0.1 exists" |
| 6 | Fallback identity and the update inference not re-checked | Packet limits | Not a defect: both are labelled. The inference wording is now faithful to the excerpt (RV3 MINOR 2) | "manual" and "on request" restored; RP-R6 checks them (B-46) |
| 7 | Cited rules and clauses not supplied; terms claimed DEL-11-03's clauses were excerpted | Packet | **Real** (also RV3 MINOR 3): REQ-006, VER-003 and VER-004 were not excerpted | Excerpts now include REQ-006, VER-003, VER-004, R23-32 (with F-R2/F-R3) and R23-43; the terms are corrected; A-13 now also covers codes in the new excerpts |
| 8 | Refinement steps J-8/J-9 count as "workflow saving"; reuse rests on J-7 alone | Supplier design (SQ step map, WR TT-7) | Not a packet defect. The packet shows SQ's mapping and the dossier's own reason for uncounted runs. Whether reuse should rest on one counted step is O-B's design, offered as a note | None in DEL-11-03 |

## EU-F2 — frozen (DEL-11-01 CA-v0.1 with DEL-11-03 RP-v0.4)

**Why one unit.** RP-v0.4 adopts CA-v0.1's hand-over in place of the first cut. The interface is checked from both ends: `check_ca.py` K-11, and `check_rp.py` A-7, A-8 and A-21.

**Claims.**
1. DEL-11-01 is a linked view (F-R6) of seven preservation classes, each linked by git identity at commit `22ed9383a45e788ade4718b9e78053e9ceb72d90`. All checks are **real** except C-7:
   - C-1 fallback facts: matches;
   - C-2 App v3 lane: tree `3fb53704…`, active (225 commits after the v3.0.1 source);
   - C-3 archives: `archive_digests.py verify` 19/19 OK, exit 0;
   - C-4 thesis: tree equals PRD §11's, working tree clean, VER-003 negatives in memory;
   - C-5 and C-6: present;
   - C-7: not checked, because no digest record exists (U-CA-2).
2. Four DEP-006 lanes (App v3, Runtime, SWBPIPE, Root, checked against DEL-10-03's X-1) carry continuing obligations `not_supplied`. No retirement is intended; none is eligible. RE-1 makes eligibility need intent, supplied obligations and an evidenced disposition. A fallback replacement or an empty record never qualifies.
3. Two real owner acts are recorded faithfully, each with its exact text found in its record and actor ≠ recorder: OD-09, and this run's direction item 2 ("2 no rewrite").
4. RP-v0.4:
   - adopts the CA hand-over (S-4 `owner_record`);
   - refuses an illustrative subject outside a fixture and announces it in a fixture;
   - restores "manual" and "on request";
   - excerpts every clause its terms claim;
   - re-pins the DOS examples to DX-3;
   - carries RR-EUF3's cheap fixes.

**Checks run.**
- `check_ca.py`: **21/21**. K-3 rebuilds at the commit and reproduces the account exactly, with the archive check included. Five schema negatives were each confirmed to fail for their own rule.
- `check_rp.py`: **70/70**, no drift notice.
- `--fixture FX-RP1 / FX-RP1-2 / FX-RP1-3`: 8/22, 11/22, 13/22 (earlier fixtures under the current rules and vendor copies, as expected).
- Both builders are deterministic.
- `compare_rp.py --set 3 RR-EUF3/account.json`: 36/36.
- Pins recomputed: CA-v0.1 9/9 match current files. RP-v0.4 has 13 pins: 12 match, and 1 is the superseded RP-v0.3, stated.
- `git status --ignored`: the first build wrote CA records to `F/ca/out/`, which the root `.gitignore` (`**/out/`) ignores. They were moved to `F/ca/records/`, the scripts and Design text were updated, everything was rebuilt and rechecked, and the status re-run shows nothing ignored (`git check-ignore` on `records/` exits 1).
- Home paths: none in any record or Design file. The only matches are the refusal regex in `build_ca.py` and `check_ca.py`.

**Files (sha256)** — paths for the R23-41 commit:

| File | sha256 |
|---|---|
| `DEL-11-01_…/Design/CONTINUITY_ACCOUNT.md` (CA-v0.1) | `1a4a0ca6b1b6e74fe11e3c41b0c6b3d1316624e41c8aa4adb28f2c7d050f6ab2` |
| `DEL-11-01_…/Design/ca.continuity-account.schema.json` | `bf9737517d4bae89234e4a5586e49d8a130ba7dc40579bf4e783b9d2637dc886` |
| `DEL-11-03_…/Design/REPLACEMENT_PACKET.md` (RP-v0.4) | `5bfa93036466e3b894608f595a4f8fda070f6335470bdca6433e939dbcd98271` |
| `DEL-11-03_…/Design/rp.packet-manifest.schema.json` (RP-v0.4) | `9c80b95dd97bcafc8749893700028ba534153e6d081ab2fee91156d2a225e49d` |
| `F/rplib.py` | `c834e90b8298b5ef2c7bec7f58d7328d526670ebcd171602bc9d08b69dc96593` |
| `F/build_fx_rp1.py` | `93545c62d5eded2ee1f57701ea086a22b6018c09e7d4fa4fdf6e4455099d6f5c` |
| `F/check_rp.py` | `a0ae9335cf8e791560b12135459d545d3cb0b804bc5b1a9974301e009a982bce` |
| `F/README.md` | `15e045653514e67401194b2f43940961049ff426745de0f428c03582387a3934` |
| `F/vendor/VENDOR.json` (+ the re-pinned `lhq.dossier-manifest.valid.examples.json` `dbf8463f…`) | `982b7bb975b362ff82e81799420a4be39066f0995c014e37f5652073814b9d3f` |
| `F/fixtures/FX-RP1-4/MANIFEST.sha256` (11 files) | `ff30d2347b310105d5816b5f9b968b0127856526659fc13c7b5c444d434a0cb2` |
| `F/ca/build_ca.py` | `eb36d8293f8c814f85d873032ad2c250968e75befbbfd481cfa97fba679fb8e8` |
| `F/ca/check_ca.py` | `7a04f7525a395f77e763bba60548d99c29206eee43aedda46de5980bc25103be` |
| `F/ca/vendor/VENDOR.json` (+ `RESPONSIBILITY_ACCOUNT.md` `531b65b7…`) | `3502235f9f2337ffc8db3baf869626cfdbc740c504478ef51d64c752eb2bc415` |
| `F/ca/records/MANIFEST.sha256` (CA-1 account and hand-over) | `3107f6523e30690b7189744ed03a9473e8291534b771e1c474dbe80eade36e70` |

**Not changed:**
- FX-RP1, FX-RP1-2 and FX-RP1-3;
- all three input sets and keys;
- the reader schemas and briefs;
- `compare_rp.py` and `stage_is.py`;
- RP-v0.3's committed bytes, except the DEL-11-03 Design files superseded above.

The re-pin of `F/vendor/lhq.dossier-manifest.valid.examples.json` was deliberate (RV3 N9). FX-RP1-3's A-8 now fails against it, and is recorded as history.

**Limits.**
- C-3's verify needs the original checkout; elsewhere it is `not_run`, never `changed` (CF-1).
- C-7 cannot be checked (U-CA-2).
- The lane obligations wait for their owners (U-CA-1).
- DEL-10-03's RA is an unfrozen draft, vendored (CF-5).
- The thesis front-matter attribution reading is left for VER-003's production run (U-CA-5).
- All DEL-11-03 supplier evidence is still illustrative.

**Next.** DEL-11-02 (the D-GOV-52 adoption trace, consumers from DEL-10-03 X-1), then DEL-09-12. I work on them while EU-F2 waits, and do not freeze another unit until EU-F2 leaves review.
