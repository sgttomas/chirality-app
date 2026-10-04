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
| EU-F2 | DEL-11-01 CA-v0.1 + DEL-11-03 RP-v0.4 | DEL-11-01 `Design/`, DEL-11-03 `Design/`, `F/` (incl. `F/ca/`) | see "EU-F2 — frozen" | **READY** (RV3-CA1.md; RV3-EUF1.md Addendum 6); MINORs carried into EU-F3 |
| EU-F3 | DEL-11-02 AA-v0.1 + DEL-11-01 CA-v0.2 + DEL-11-03 RP-v0.5 | the three `Design/` folders; `F/` (incl. `F/aa/`, `F/ca/`) | see "EU-F3 — frozen" | Committed `b2fbfdbac8`; **REPAIR** (RV3-AA1: AA1-R1 MAJOR); superseded by EU-F3R |
| EU-F3R | DEL-11-02 AA-v0.2 + DEL-11-01 CA-v0.3 + DEL-11-03 RP-v0.6 | as EU-F3, plus `F/fixtures/FX-RP1-6/` | see "EU-F3R — frozen" | Committed `0e0036b685`; **READY** (RV3-AA1 addendum, `0d23f45985`); AA2-R1 MINOR and CA2-N1 taken in EU-F3R2 |
| EU-F3R2 | DEL-11-02 AA-v0.3 + DEL-11-01 CA-v0.4 (checker and Design only; AA-1 v2, CA-1 v3, RP-v0.6 and FX-RP1-6 unchanged) | DEL-11-02 and DEL-11-01 `Design/`; `F/aa/check_aa.py`, `F/ca/check_ca.py`, `F/README.md` | see "EU-F3R2 — frozen" | **FROZEN 2026-10-04; for HELP_HUMAN to commit by path, then RV3 to confirm AA2-R1** |
| EU-F4 | DEL-09-12 PV-v0.2 | DEL-09-12 `Design/`, `F/pv/` | see "EU-F4 — refrozen" | Committed `0e3591a65d`; **REPAIR** (RV2-PV1, `a3b91c843f`: PV1-R1 MAJOR) |
| EU-F4R | DEL-09-12 PV-v0.3 | DEL-09-12 `Design/`, `F/pv/` | see "EU-F4R — frozen" | **FROZEN 2026-10-04; for HELP_HUMAN to commit by path, then RV2 to confirm** |

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

## EU-F3 — frozen (DEL-11-02 AA-v0.1, with DEL-11-01 CA-v0.2 and DEL-11-03 RP-v0.5)

**Why one unit.** AA-v0.1's status hand-over feeds both CA-v0.2 (adoption status) and RP-v0.5 (S-6). The interface is checked from all three ends: `check_aa` K-9, `check_ca` K-13, and `check_rp` A-7, A-8 and A-22. CA-v0.2 and RP-v0.5 also carry RV3's MINORs on EU-F2.

**Claims.**
1. **DEL-11-02 (AA-v0.1)** records, per renewal and consumer, eight separately warranted facts read from git at `122c5abcf516f31ffdb1fdb17d9d5b0f96603154`. Separation rules SR-1…SR-4 and the schema keep the facts apart. The real case is RN-1, D-GOV-52:
   - **App v4:** adopted, by agent act AD-1 (R23-30's exact text). Supply, provider adoption and behaviour are not established. Its three Design files are "pending next revision", recomputed (K-10).
   - **App v3 and Runtime:** notice delivered; receiving decision not recorded. The search found no other mention and no commit after the tranche.
   - **Piping and PEC:** no notice by design; the manifest's "reads … live" is quoted, not taken as observed and not counted as adoption.
   - **The owner's approval A-1** is faithfully recorded, with recorder HELP_HUMAN as the file states.

   RN-2 (the renewed v4 basis) shows no adopter among the four X-1 consumers; OI-024's owner and point of need are carried. Packaging: the export manifest is established; publication is not. Currency: no reliance, so no comparison is run. The consumers are checked against DEL-10-03 RA-v0.2's X-1 (F-R11).
2. **DEL-11-01 (CA-v0.2):**
   - **CA1-R1:** OD-09's recorder is now "not named by the record", quoting DECISIONS.md's own custody ("the grouping and IDs are the agent's"), with OPENING_BRIEF.md as custody. K-9's string-comparison limit is stated in the check and in the Design.
   - **CA1-R2:** all three OD-09 sentences, each with its classes. The archive-root home path in sentence 2 is replaced by ‹archive root›, matched as one token, so an altered sentence still fails (N-9).
   - **CA1-N1:** RA re-pinned to v0.2 (`811c868c…`, `ce64a97a2a`); VENDOR.json, the header and CF-5 corrected.
   - DEL-11-02's status is recorded (U-CA-4 closed).
   - Rebuilt at `122c5abcf5`: identity results unchanged, archive verify 19/19.
3. **DEL-11-03 (RP-v0.5), EUF4-R1:**
   - `evidence_standing` and `candidate.identified` are derived from the supplied items' standings, the subject's placeholder markers and the unresolved results, and recomputed in A-9.
   - `check_package` refuses a declared/derived mismatch and decides the fixture refusal on the derived values. RV3's probe is B-48 and is refused on both counts.
   - `check_disposition` refuses presenting or deciding a fixture package (B-51, B-52).
   - B-47 (made genuinely real-looking), B-49 and B-50 are the controls.
   - S-6 adoption status is supplied.

**Checks run.**
- `aa/check_aa.py`: **19/19**. Its K-3 rebuild reproduces the account exactly.
- `ca/check_ca.py`: **23/23**. Its K-3 rebuild reproduces it exactly, with the archives verified; no drift NOTICE.
- `check_rp.py`: **76/76**. `--fixture FX-RP1-3` gives 13/23 and `--fixture FX-RP1-4` gives 18/23 (history).
- All three builders are deterministic (`cmp`).
- Pins: CA-v0.2 has 11, RP-v0.5 13 and AA-v0.1 3. Each matches its current file except the one superseded version each names (CA-v0.1, RP-v0.4). AA's Root-level pins (`AGENTS.md`, tranche manifest) were recomputed separately.
- Quotes: every quote in the AA evidence is checked against its file at the commit (K-4). The OWNER_DECISIONS and AGENTS.md quotes in ADOPTION_ACCOUNT.md §1 were checked by script.
- `git status --ignored` on the unit's paths shows nothing ignored; records are in `records/`, not `out/`.
- Home paths: none except the refusal regexes in the four builder and checker scripts.

**Files (sha256)** — paths for the R23-41 commit:

| File | sha256 |
|---|---|
| `DEL-11-02_…/Design/ADOPTION_ACCOUNT.md` (AA-v0.1) | `583637e3fd71dca76e87998fb0927906bee8c3b5a8d7a4a70ed1778ccaa0b878` |
| `DEL-11-02_…/Design/aa.adoption-account.schema.json` | `0fd3c573c7fa7580afc44424adfbb0fd8c1e39857ed92fa09355ae47085799bb` |
| `DEL-11-01_…/Design/CONTINUITY_ACCOUNT.md` (CA-v0.2) | `ecde63b47d3a820c8ffbf35ad0ad3c17d40c506626528afb505506b42fbc1c8d` |
| `DEL-11-01_…/Design/ca.continuity-account.schema.json` (0.2) | `b575dd4e7c182e1d65b3370b32435638a5702d66a96ed9c6353f8612ed54dbfe` |
| `DEL-11-03_…/Design/REPLACEMENT_PACKET.md` (RP-v0.5) | `f928cd0274d14a41ad693b8d073bf9a7a286f5fc7a0ff71fc6be082292107644` |
| `DEL-11-03_…/Design/rp.packet-manifest.schema.json` (RP-v0.5) | `90629f17dcb621df7626325974a65b48e393574b69a187998855deb5df9fa290` |
| `F/rplib.py` | `52e645640ff9d42772ea3b5cda94fb9d63212ef5ab03afcf8ea3b6fd15ed9cd3` |
| `F/build_fx_rp1.py` | `0754e56b09dd19d25b2954df15c98e5840f082dd4c89aefdf69be606b8cfef9d` |
| `F/check_rp.py` | `71987a463bc8c52eac73af2f3e8261572d2f915350fcf40e5c56cd71f4b46c3a` |
| `F/README.md` | `14b3a3ebcbdfdb13d9edca3ea7322521042d59a3746a527f1dccb9ed41c372e8` |
| `F/fixtures/FX-RP1-5/MANIFEST.sha256` (12 files) | `c8a267ff5149c3f5315ec56f041e680e10a9eef249c14f702a0630068744d700` |
| `F/ca/build_ca.py` | `7b33c8ac80e12d1e67275c68e2999485b5ef68f4da68fb678094b2ae2daccf66` |
| `F/ca/check_ca.py` | `2ba5c7d070789b416452a466c6e5ca494b4e1ddc0e4e91d6d81fb5f7ab65d22f` |
| `F/ca/vendor/VENDOR.json` (+ RA-v0.2 `811c868c…`) | `f608edcfe78fc3cc585347468b236a6dcbe48555600986245a262f55c0acd966` |
| `F/ca/records/MANIFEST.sha256` (CA-1 v2) | `0382842e674a63bb3d5a371a413f8987e84dc089468782afaf823aad4eadca77` |
| `F/aa/build_aa.py` | `4b435bee26ff7a84f910b0ae12d0692dd6ced96d82e67ba08685d481500087c2` |
| `F/aa/check_aa.py` | `a5d5feee13e58d8f3effea54e0e0e77c9ef03725111520956933be9fce323d8f` |
| `F/aa/records/MANIFEST.sha256` (AA-1) | `3ea37d116a9600534c830338013e390d32e5be9b33e55e79269253d30366d0d7` |

**Unchanged:**
- FX-RP1…FX-RP1-4;
- input sets 1–3 and their keys;
- the reader briefs and schemas;
- `compare_rp.py`, `stage_is.py`, `F/vendor/`;
- the disposition schema.

**Limits.**
- AA-1's facts for App v3, Runtime, Piping and PEC are what git holds. Whether a loop read its notice is not observable (U-AA-1).
- RN-2 has no adopter, and first adopters are the owner's decision (U-AA-2; P-4).
- CA's archive check needs the original checkout.
- All DEL-11-03 supplier evidence is still illustrative; the package is a fixture and can never be presented (B-51).

**Next.** DEL-09-12, its own observation record (F-R12, F-R13, F-R14). It will be designed while EU-F3 waits and frozen after.

## EU-F4 — frozen (DEL-09-12 PV-v0.1)

**Claims.**
1. **F-R12.** DEL-09-12 keeps its own records, in five kinds:
   - arrangement, observation, disposition;
   - `method_note`, the hand-over to DEL-10-02;
   - `practitioner_standing`, the hand-over to DEL-11-03.

   No kind has an outcome, verdict or score field, and the schema is closed (K-7). An observation carries V4-EXM-41's four aims as source-linked observations with `observed` or `not_observed` coverage; "not observed" never carries statements. EXP's `activity: validation` is not used, which is a note for O-B (U-PV-4).
2. **F-R13.** Routing goes through the real ScopeLedger at the build commit (IN rows by ScopeItemID or SourceRef anchor):
   - V4-EXE-01 → DEL-01-02;
   - V4-EXM-41 and SOW-209 → DEL-09-12;
   - method observations → DEL-10-02;
   - an unknown anchor → `unresolved`, which is reported and never invented (K-10).

   PV-R3 refuses any other recipient.
3. **F-R14.** The schema makes `open_issue` the constant "OI-016 (App v4)". A rule refuses an unqualified mention and accepts "SWBPIPE OI-016". Every DEL-09-12 Design file and record passes, except the one deliberate negative example (K-8, K-9).
4. **The real state** (PV-ARR-1, PV-STANDING-1, built at `b2fbfdbac8`):
   - `not_agreed`, with no agreement, no period, and **no activity proposed**: activities are the owner's choice (P-2), and none can run before a candidate exists;
   - both expressions are `blocked`, each with its stated cause. SWBPIPE's cause quotes DECISION-3 ("defer the host joins") and names OI-021;
   - standing `not_agreed`, 0 observations, `is_replacement_condition: false` (F-R3).

   The builder stops if OI-016 (App v4) or OI-021 is no longer OPEN, or if DECISION-3's text is gone.
5. **Hand-overs.**
   - `method_note` has exactly DEL-10-02 UC §5's eleven field groups, read from UC at the commit (K-11). UC §9 states it receives them this way.
   - `practitioner_standing` carries the values DEL-11-03's first cut reads (K-12). DEL-11-03 adopts it at its next revision (U-PV-3); EU-F3 is under review and is not edited.
6. **Act boundary.** The agreement is recorded only from the owner's act, in OWNER_DECISIONS form (actor the owner, recorder someone else). A plan or proposal is never agreement. Rule PV-R2 also refuses an agreed arrangement with activities the owner did not select.

**Checks run.**
- `F/pv/check_pv.py`: **13/13**. That covers 7 valid examples, and 14 invalid ones: 10 refused by the schema and 4 refused by their own rule while passing the schema. I printed each invalid example's refusal reason and confirmed it is the one its `why` names.
- The builder is deterministic (`cmp`), and K-3 rebuilds exactly at the commit.
- The six quotes in PRACTITIONER_VALIDATION.md (ScopeOfWork REQ-002 and VER-004, EXAMINATION V4-EXM-40 and V4-EXM-41, Open_Issues) were checked against their sources by script.
- All 7 pins match current files. The suppliers (ScopeLedger, Open_Issues, UC, EXP, EXAMINATION) are committed and clean, and the prototype reads them from git at the commit, so no vendoring is needed.
- `git status --ignored` shows nothing ignored.
- No home paths in the records or Design files (K-13).
- EU-F3's paths are unchanged against `b2fbfdbac8` (`git diff --stat` is empty).

**Files (sha256)** — paths for the R23-41 commit:

| File | sha256 |
|---|---|
| `DEL-09-12_…/Design/PRACTITIONER_VALIDATION.md` (PV-v0.1) | `f917357afd2cc82949d79baf82832b029dbe7985a2e8c7213bd21fef325c0a73` |
| `DEL-09-12_…/Design/pv.practitioner-validation.schema.json` | `2b7c2b9e8b5fdd1c8ea0dda5b0e5799affd9d7f94f1b6d76175f8956ebd5366f` |
| `DEL-09-12_…/Design/pv.examples.valid.json` (7) | `82ab49ae1dcdaac5976f730f5a8b6af801ee17f29c1fb826a8746afd175fdc6a` |
| `DEL-09-12_…/Design/pv.examples.invalid.json` (14) | `c15ccd2601baf1110e25c96b3d2c693ec7427e4327b674d21deb0ad58cc6e67a` |
| `F/pv/pvlib.py` | `fc82093c2bedb086dc4c21e544f20ace82fc2ae77a05b7bec46a21a68986af36` |
| `F/pv/check_pv.py` | `9184774ad3c603f81ddefd38e0501acced0753b0713efa93eb530b1b113646af` |
| `F/pv/records/MANIFEST.sha256` (PV-ARR-1, PV-STANDING-1, BUILT_AT) | `32256269ea3ed1f470793ae01d7a28bfc74f1a72c2befd3cbb63cb62a337b538` |

**Limits.**
- No real observation, agreement or disposition exists, and none is invented; the examples are illustrative.
- The ScopeLedger routing is as good as the ledger's SourceRef anchors. A requirement with no IN row is reported `unresolved`.
- Whether to prepare a proposal before candidates exist is left as an inference in §4 (not now).

**Carried into DEL-11-03's next revision (after RV3 on EU-F3):** adopt `practitioner_standing` (U-PV-3), together with any RV3 findings HELP_HUMAN routes.

## EU-F3R — frozen (repair of EU-F3 for RV3-AA1: DEL-11-02 AA-v0.2, DEL-11-01 CA-v0.3, DEL-11-03 RP-v0.6)

DEL-09-12 was paused at a safe point: EU-F4 had been frozen (PV-v0.1) and not yet reported. This repair round was done first, and the coordinator's checker audit (2026-10-04) was applied to all four deliverables before freezing.

**Repairs.**
- **AA1-R1 (MAJOR), enforced, not only stated.**
  - Per-fact evidence whitelist (§3 table), in the schema (`if established then` per fact) and in `check_aa` SR-1. `resolved`/`supplied`/`provider_adopted`/`observed_behavior` take only `candidate_record`/`observation_record` (new kinds; none exists yet). `absence_search` and `design_file_state` establish nothing.
  - SR-2: `delivered` only by a file inside the receiving lane.
  - SR-3: `consumer_adopted` only by an `agent_act` of class `adoption`, for that consumer, whose record lies in that consumer's lane; a file beside it must be the act's record. A person's `human_act` never counts (F-R10), even with every other field made right (N-15).
  - SR-4: the act text contains adopt/adopts/adopted/adoption and no negation (keyword-based; stated as a limit).
  - Acts gain `act_class` (A-1 `change_approval`, AD-1 `adoption`) and `recording_mode` (A-1 `faithful recording`, AD-1 `direct capture`, RV3 N1).
  - RV3's five variants, reproduced from RV3-AA1.md as built there, are N-9…N-13; each is refused by the rule named in its line. Variant 4's act cites `R23_RESOLUTIONS.md` and its text "notice delivered; receiving decision not recorded" is in that file, so K-5 passes on it as RV3 found; SR-3 (lane) and SR-4 (text) refuse it.
- **AA1-R2 (MINOR).** Statement now: "… a notice was delivered to App v3's and Runtime's coordination folders, and no receiving decision is recorded (whether either loop read it is not shown) …". Carried into CA-1 `adoption_status.ref` and RP S-6/`adoption.statement`. **Version call:** CA and RP each step a version (CA-v0.3, RP-v0.6), because their built content changes (CA-1 v3; fixture FX-RP1-6) and a frozen version id should name one content. CA's record format (CA-v0.1) and schema are unchanged. RP's manifest format steps to RP-v0.6 because the standing enum is renamed (N2).
- **AA1-R3 (MINOR).** RN-2 Root search: `git grep -F 'APP-V4-BASIS-20260926' 122c5abcf5 -- '.' ':(exclude)projects/chirality-app-v4'` (0 files; rerun by me), with RV3's own search cited second, attributed to RV3 (`reviews/RV3-AA1.md, AA1-R3`).
- **Notes.** N1 AD-1 named direct capture (record and §1). N2 `owner_record` → `deliverable_record` (RP schema enum and description, builder, A-21, A-22, B-47, B-49), defined in the packet's terms ("standing (supplied item)"). N3 the placeholder test is stated as keyword-based (RP §3; PV §3.2).

**Checker audit (coordinator, 2026-10-04).** Each checker now computes each claimed rule as one function, and each negative breaks the real record (AA-1, CA-1, the FX-RP1-6 fixture, PV-ARR-1/PV-STANDING-1) in memory and runs that same function, naming the rule that must refuse it. A negative no longer re-derives its rule (AA's old N-7 and CA's old N-5/N-9 did). This found one real gap: CA never compared a lane's recorded `retirement_eligible` with RE-1's result (old N-3 passed on the rule function alone); K-14 now does. No check was weakened; old N-3 in AA now names SR-3 (the renumbered "own consumer" rule) instead of SR-4.

**Claimed rules with a negative case (one line each):**
- AA schema (act required, adoption point, recorder not actor, evidence required, per-fact kinds): N-1, N-19, N-5, N-6, N-8…N-11.
- AA SR-1 per-fact kinds: N-2, N-8, N-9, N-10, N-11.
- AA SR-2 delivery by a lane file: N-11, N-17.
- AA SR-3 own loop's adoption act in its lane: N-1, N-3, N-8, N-12…N-15, N-18.
- AA SR-4 adoption text: N-12, N-13, N-14, N-16.
- AA K-2 N-27; K-3 N-28; K-4 N-20, N-21, N-22; K-5 N-4, N-16; K-7 N-23; K-8 N-11, N-24; K-9 N-7, N-26; K-10 N-25; K-11 N-29.
- CA schema (standing, retention, fallback kept, RE-1 conditions, recorder): N-8, N-6, N-7, N-2, N-3, N-4.
- CA RE-1 recorded = rule (K-14): N-2, N-3.
- CA K-2 N-18; K-3 N-19; K-4 N-12, N-13; K-7 N-17; K-9 N-4, N-5, N-9, N-10, N-11; K-10 N-14; K-11 N-15; K-12 N-20; K-13 N-16.
- RP Part A: A-1 C-1; A-2 C-2; A-3 C-3; A-4 C-4; A-5 C-5; A-6 C-1, C-6; A-7 C-7; A-8 C-1; A-9 C-8, B-48; A-10 C-9; A-11 C-10; A-12 C-11; A-13 C-12; A-14 C-13; A-15 C-14; A-16 C-15; A-17 C-16; A-18 C-17; A-19 C-18; A-20 C-19; A-21 C-20; A-22 C-1, C-21.
- RP rules: RP-R1 B-1, B-3…B-8, B-10, B-12; RP-R2 B-14, B-17, B-18; RP-R3 B-21, B-25…B-27; RP-R4 B-29, B-30; RP-R6 B-31…B-36, B-45, B-46, B-48; RP-R7 B-38…B-44, B-51, B-52.
- PV (EU-F4, below): schema N-1, N-3, N-4, N-5, N-6; PV-R2 N-2; K-2 N-12; K-3 N-13; K-4 N-5, N-8; K-7 N-9; K-8 N-6, N-7; K-11 N-10; K-12 N-11; K-13 N-14.

**Claimed rules without a negative case, or not enforced (one line each):**
- AA SR-4 is keyword-based: "App v3 adopts nothing" would pass.
- AA `act_class`/`recording_mode` are checked as fields, not against the act's record: a mislabelled record passes SR-3 if its lane and text pass.
- AA/CA actor-not-recorder is a string comparison; a false recorder name passes.
- AA `candidate_record`/`observation_record` are accepted by kind only; no check resolves them (none exists).
- AA K-8 covers RN-1 notices only; K-10 recomputes only `applied` (REQ-004's `checked` and its own evidence are not enforced); packaging states and currency are by inspection; K-7/CA K-10 match consumer names as strings.
- CA N-1 holds by construction (`retirement_eligible` never reads the replacement disposition); not a refusal.
- CA K-5 (thesis tree hash) and K-6 (thesis working tree clean): no negative, since breaking them means touching the thesis; K-8 tests the listing detector, which K-5 does not call.
- CA archive verify (C-3): no negative (the owner's archive is not altered).
- RP V-1 vendored bytes: no negative (would edit a vendored file).
- RP RP-R5: by construction (`replacement_evidence_complete` never reads the standing); B-28 and C-11 only.
- RP RP-R8: detected only when the check reruns (A-1, A-6, A-8, B-41).
- RP placeholder test is keyword-based ("TBD", "xxx" pass).
- RP `produced_by`, `shape_only` wording, `open_matters`: by inspection.
- PV-R1 and PV-R3: no real observation or disposition exists; refused only on invalid examples 11, 13, 14 (K-10 runs routing on the real ledger).
- PV placeholder test is keyword-based (as RP's).
- Act boundaries (AA §1, CA VER-007, RP RP-VC-06, PV VER-006): by review.

**Checks run.**
- `aa/check_aa.py` **43/43**; `ca/check_ca.py` **36/36** (with archives; no drift NOTICE); `check_rp.py` **99/99**; `pv/check_pv.py` **27/27**.
- History: `check_rp.py --fixture FX-RP1 … FX-RP1-5` give 8/23, 11/23, 13/23, 16/23, 16/23. FX-RP1-5 fails A-2, A-7, A-8, A-13, A-18, A-21, A-22 (format, renamed standing, terms, legend, AA-1 v2), as expected.
- All four builders run twice: identical bytes for every record and fixture file.
- `git status --ignored` on the unit paths: nothing ignored. FX-RP1…FX-RP1-5, `F/vendor/`, `F/ca/vendor/`, the CA schema and the RP disposition schema are unchanged against `b2fbfdbac8`.
- Home paths: none, except the refusal regexes and the split synthetic string in the negative tests.
- Pins rechecked: Root `AGENTS.md` `f96feb19…`, tranche manifest `559dcf43…`, export manifest `8e532540…`, RA-v0.2 `811c868c…`, the three ScopeOfWork pins (`2d962646…`, `272f7622…`, `01773543…`). Superseded versions named: AA-v0.1 `583637e3…`, CA-v0.2 `ecde63b4…`, RP-v0.5 `f928cd02…`, each hashed from `git show b2fbfdbac8:…`.

**Files (sha256)** — paths for the R23-41 commit (from `projects/chirality-app-v4/execution/`):

| File | sha256 |
|---|---|
| `PKG-11_…/DEL-11-02_…/Design/ADOPTION_ACCOUNT.md` (AA-v0.2) | `3d4ba2ec9fbd614a1e36c897aca45b7f4ed33cb859cb506f6af833d4639edba3` |
| `PKG-11_…/DEL-11-02_…/Design/aa.adoption-account.schema.json` (0.2) | `70b5d215c86574192792d42a267c2fb367cc37b731073caa0da3509337e52c3f` |
| `PKG-11_…/DEL-11-01_…/Design/CONTINUITY_ACCOUNT.md` (CA-v0.3) | `8f47aa080b4767f2d4c6f44bfc2ead12e53ca982060bcd19242851eb9fde0a87` |
| `PKG-11_…/DEL-11-03_…/Design/REPLACEMENT_PACKET.md` (RP-v0.6) | `71eb2881ea605252876f4553932a3fc9e889b1743a2e27263e079b80783d805a` |
| `PKG-11_…/DEL-11-03_…/Design/rp.packet-manifest.schema.json` (RP-v0.6) | `5b2a4b2a6f698039ffb62b6d1366aa429830b18057e6878ef24f3f02d80a0a63` |
| `RUN/F/aa/build_aa.py` | `4ee20957286d70a31c6625281e515cbd53d603f4d08b9d5b4e27345be4e62e54` |
| `RUN/F/aa/check_aa.py` | `2a531ad435ca2c437aedc0c8728b67c4dc6c28713ac83c98e2cc2f22d3cab906` |
| `RUN/F/aa/records/MANIFEST.sha256` (AA-1 v2) | `6e9fd68a72e069dfadb01904af3e4323a2910444bb472ded2863ba193ac8952d` |
| `RUN/F/ca/build_ca.py` | `00269f5ad9617bed1e32054cd7f5996ec8f7c6f7336d55705c7930a57aeb0687` |
| `RUN/F/ca/check_ca.py` | `74f9b9c0ed052b92f2d675b07b5b236d4e807a11edee3b1d10f8cc655ab21308` |
| `RUN/F/ca/records/MANIFEST.sha256` (CA-1 v3) | `c7e7d62d80f16d5f2328acf2893e6853c35d96856d28cf60d6ef5e00fa6e3ba7` |
| `RUN/F/rplib.py` | `61ec11af20c4ca139ff9785ac6227971cf3aca03244167d6dbe7a851e7a44819` |
| `RUN/F/build_fx_rp1.py` | `ee3d0c0d2ec9a28764f3aa9f1f28306155f3e63a093cc9d2bd47148c7262d56a` |
| `RUN/F/check_rp.py` | `9e2a8575ef71d7a99bb0ed51fc9e3be80cc4c0338f44c3ac58e924b0b9130d45` |
| `RUN/F/fixtures/FX-RP1-6/MANIFEST.sha256` (12 files; new folder) | `19050b1266523c49dc1b5928725db385dafdde2a3142c59351e5a537c7bca65a` |
| `RUN/F/README.md` | `409efe9797259aa0be33c5db89d3d1d1677893b3560c25562bcc960dcea98e3f` |

Unchanged and not to be re-committed: `ca.continuity-account.schema.json` (`b575dd4e…`), `rp.disposition.schema.json` (`d5a69bc2…`), `F/ca/vendor/` (`VENDOR.json` `f608edcf…`), `F/vendor/`, FX-RP1…FX-RP1-5, input sets, keys, reader briefs, `compare_rp.py`, `stage_is.py`.

**Limits.**
- The separation is now enforced for the kinds of evidence and the act's class, consumer, lane and wording; it still cannot read meaning (the keyword limit) or verify a label against its record.
- Two units now wait (EU-F4 and EU-F3R), against the one-waiting rule. EU-F4 was frozen before the repair request arrived; EU-F3R is the coordinator's priority, so RV3 takes it first.
- U-PV-3 (DEL-11-03 adopting `practitioner_standing`) is not folded into RP-v0.6, which is a repair round; it stays carried to DEL-11-03's next revision.

## EU-F4 — refrozen (DEL-09-12 PV-v0.2), before any review

PV-v0.1 (`f917357a…`, record above) was frozen and not yet reported. PV-v0.2 applies the coordinator's checker audit and nothing else, limited to what DEL-09-12's own design question needs (no new rule, no new record kind):
- `check_pv.py`: K-4, K-7, K-11, K-12 and K-2 are functions of the records (or schema text); N-1…N-14 break the real PV-ARR-1/PV-STANDING-1 (or, for F-R12 and UC §5, the schema text) in memory and name the refusing rule. Per-kind refusals are checked against the kind's own `$def`, not the top-level `oneOf`, so a refusal names its reason.
- PRACTITIONER_VALIDATION.md §8: count 27/27 and the covered/uncovered lists (in the EU-F3R lists above); §3.2 states the placeholder test's keyword limit; U-PV-3 and the O-3 note now name RP-v0.6.
- Records, schema, examples and `pvlib.py` unchanged; `records/MANIFEST.sha256` still `32256269…` after a rebuild at `b2fbfdbac8`.

**Files (sha256)** — paths for the R23-41 commit:

| File | sha256 |
|---|---|
| `PKG-09_…/DEL-09-12_…/Design/PRACTITIONER_VALIDATION.md` (PV-v0.2) | `2240ab360eeb5e5f5ac5c6375e7bfe20b7805bb9943d517a5b980ce75e0708f4` |
| `PKG-09_…/DEL-09-12_…/Design/pv.practitioner-validation.schema.json` | `2b7c2b9e8b5fdd1c8ea0dda5b0e5799affd9d7f94f1b6d76175f8956ebd5366f` |
| `PKG-09_…/DEL-09-12_…/Design/pv.examples.valid.json` (7) | `82ab49ae1dcdaac5976f730f5a8b6af801ee17f29c1fb826a8746afd175fdc6a` |
| `PKG-09_…/DEL-09-12_…/Design/pv.examples.invalid.json` (14) | `c15ccd2601baf1110e25c96b3d2c693ec7427e4327b674d21deb0ad58cc6e67a` |
| `RUN/F/pv/pvlib.py` | `fc82093c2bedb086dc4c21e544f20ace82fc2ae77a05b7bec46a21a68986af36` |
| `RUN/F/pv/check_pv.py` | `628e63d306d85531a1a85e5ea11e78e12995e1553ca0054dde77b71f592317d4` |
| `RUN/F/pv/records/MANIFEST.sha256` | `32256269ea3ed1f470793ae01d7a28bfc74f1a72c2befd3cbb63cb62a337b538` |

**Next.** Resume DEL-09-12 (its review findings, when routed), and DEL-11-03's adoption of `practitioner_standing` (U-PV-3) at its next revision.

## EU-F4R — frozen (DEL-09-12 PV-v0.3, repair for RV2-PV1)

RV2-PV1 (`a3b91c843f`): REPAIR, nothing BLOCKING. RV2's probe script was in its temp directory, so probes A, B, C, D, E, G and H were rebuilt from the review text. Only DEL-09-12 `Design/` and `F/pv/` were edited; every AA, CA and RP path was left alone for this repair.

**Repairs.**
- **PV1-R1 (MAJOR).** A disposition's decision is now someone else's act, recorded as such:
  - `proposed` carries only `proposed_by`; a proposal carrying a decider, actor, recorder or record is refused (schema).
  - `decided` requires `decider`, `actor`, `recorder`, `recorder_stated_by_record`, `recording_mode`, `record_ref` and `scope` (schema).
  - The decider is fixed by the case: feature or workflow, `owning_deliverable`, with `deliverable` among the recipients and named by `record_ref` (PV-R5); method, `owner_at_stage_decision`, actor "the owner" (schema; UC §7), recorded in an OWNER_DECISIONS file (PV-R5); successor basis, `owner_with_affected_consumers`, actor "the owner", plus `adoption_ref` (schema) different from `record_ref` (PV-R5).
  - An agent never decides a method or a successor basis: probe E is invalid 20, and invalid 21 hardens it (every other field made right). Both are refused by the schema.
  - Actor "the owner" forces a faithful recording by someone else (schema); otherwise faithful recording needs recorder ≠ actor and direct capture recorder = actor (PV-R5).
- **PV1-R2.** Exactly one `app` and one `swbpipe` expression (`contains` each, two items). Probe A is invalid 15 and N-15 on the real PV-ARR-1.
- **PV1-R3.**
  - PV-R4 ties actual use to a supplied arrangement that is `agreed` or `in_use`, an `available` expression, an owner-selected activity for that expression, and that expression's candidate. Probe C is invalid 18 and N-24 on the real PV-ARR-1. P-1 is the positive control, and N-20…N-23 break it each way.
  - An agreed arrangement's `available` expressions need a candidate and material: probe B is invalid 16 and N-16.
  - A standing past `not_agreed` needs `agreement_ref`: probe H is invalid 17 and N-17.
- **PV1-R4.** Candidates by expression: `app` is `{app_candidate}`; `swbpipe` is `{host_candidate, app_candidate|null}` (EXP `host_candidate`, e.g. the LHQ identification record). A SWBPIPE observation must name its host candidate (invalid 19). `configuration.host_candidate` is removed.
- **PV1-R5.** `observations` is now an array of observation ids, matching RP's first cut. The remaining differences are stated in §2 O-3: format `PV-v0.3` against `RP-v0.1-first-cut`, plus the added `arrangement_ref` and `is_replacement_condition`, which the closed first cut refuses. K-12 reads RP's first-cut `$def` at the build commit, compares every field's name, type, const and enum, checks the added fields equal the stated list, and validates the real record against the first cut with the stated differences undone. N-11, N-18 and N-19 break it. **RP is not changed in this round.** U-PV-3 now says DEL-11-03's next revision must take the format and the two added fields.
- **PV1-R6.** "Owner" is kept for the person: the header ("prepared by O-F (design owner agent)"), §1's rows, §7's column ("Decided or done by"; U-PV-2 "supplied by"; U-PV-3 "assigned to O-F (design owner agent)"), and the real record's `prepared_by`.
- **PV1-R7.**
  - N-2 is now schema-valid, so it tests PV-R2 with the schema passing.
  - §8's example numbers are corrected.
  - Valid example 2's limit now reads "illustrative example of an agreed arrangement; the owner's agreement is INVENTED".
  - The docstring names PV-R1…PV-R5 and PV-v0.3.
  - K-6 checks each schema refusal against the kind's own `$def`.
- **PV1-R8.** Carried to DEL-09-01's next revision, as recorded by HELP_HUMAN (U-PV-4).

**Audit rechecked.** RV2's three probes broke rules my PV-v0.2 list omitted. §8's lists are rewritten against the repaired rules:
- **Probes refused:** A, B, C, E and H.
- **Probes that still pass**, stated as limits:
  - D ("TBD" placeholder): PV-R1 is keyword-based, and PV-R4 then requires the same string in the arrangement.
  - G (recorder "The owner", capitalised): actor-not-recorder tests are string comparisons.
- **Also stated as not enforced:**
  - PV-R5's deliverable and OWNER_DECISIONS checks are textual;
  - `adoption_ref` is checked as present and distinct, not whose adoption it is;
  - PV-R4 does not compare dates with the period;
  - K-12 cannot show DEL-11-03 will take the differences;
  - no real observation or disposition exists, so PV-R1 and PV-R3…R5 are broken only on examples and in-memory records.

**Checks run.**
- `check_pv.py` **38/38**, with 12 valid and 27 invalid examples. I printed each new invalid example's own-`$def` or rule refusal and confirmed it is the reason its `why` names.
- Records rebuilt at `b2fbfdbac8`; twice gives identical bytes. The content changes are the format, `observations: []` and `prepared_by`.
- `git status --ignored`: nothing ignored on the unit paths.
- No home paths.

**Files (sha256)** — paths for the R23-41 commit (from `projects/chirality-app-v4/execution/`):

| File | sha256 |
|---|---|
| `PKG-09_…/DEL-09-12_…/Design/PRACTITIONER_VALIDATION.md` (PV-v0.3) | `16718ee59275e915b2ab124bbd6846f81b7ce8d13906d4492a03ec78e4f36871` |
| `PKG-09_…/DEL-09-12_…/Design/pv.practitioner-validation.schema.json` (0.3) | `181c0c5bcc5e1f5f47ea60a2c4305ad7965152c2e000946cfabbaf67ce2c0303` |
| `PKG-09_…/DEL-09-12_…/Design/pv.examples.valid.json` (12) | `5e2204d55795694f7c05de708fc8f6e2da37a6588e205c5810492f0475c2a683` |
| `PKG-09_…/DEL-09-12_…/Design/pv.examples.invalid.json` (27) | `e176c3741117e45fedf65eea2bc33617fa0e8aab72d5c04bd723b09c79c64b3c` |
| `RUN/F/pv/pvlib.py` | `1c46fba0a879d4513aa34cdee1bd0646c9b8e08218f2373a22cddb4ccbe76245` |
| `RUN/F/pv/check_pv.py` | `e6fdb064c38266089a0f33f9b1bb190e2c3e5ca2c525138b08d1c6c0d3f1b166` |
| `RUN/F/pv/records/MANIFEST.sha256` (PV-ARR-1, PV-STANDING-1, BUILT_AT) | `02fa9aab1161a55632afac4d530b843c9f83548fdb7753fe24b5e5b5fe6dda32` |

Superseded: PV-v0.2 `2240ab36…` (from `git show 0e3591a65d:…`).

## EU-F3R2 — frozen (RV3 AA2-R1 and CA2-N1; DEL-11-02 AA-v0.3, DEL-11-01 CA-v0.4)

RV3 found EU-F3R READY (`0d23f45985`), with one MINOR (AA2-R1) and two NOTEs.

**Repairs.**
- **AA2-R1: evidence bound to the renewal, not just the lane.**
  - SR-2 now also requires `delivered` evidence to be a notice that the renewal's own change record routes, i.e. the paths listed in its tranche manifest. A renewal with no change record (RN-2) cannot have `delivered` established.
  - SR-3 now also requires the adoption act's record entry to name the renewal. The entry runs from the last heading or top-level bold item before the exact text, and it must contain an identifier from the renewal's `what` or its change record's stem.
  - AD-1's entry is R23-30's head ("R23-30 Adopting D-GOV-52 in App v4"), so it passes (P-4).
  - RV3's two constructions, rebuilt as RV3 described them, are N-30 and N-31:
    - N-30, App v3's README offered as delivery: refused by SR-2 only (I printed it).
    - N-31, the real "UPD-133 adopts the stricter live rule …" sentence in App v3's DEL-07-05 ScopeOfWork, with the status updated to match: refused by SR-3's renewal test.
  - Both are checker and Design changes only. AA-1 v2, its record format AA-v0.2 and the schema are unchanged, so CA-1 and FX-RP1-6 are byte-identical (rebuilt and compared). **RP is not stepped.**
- **CA2-N1.** N-21 is RV3's understated case: every RE-1 condition met, eligibility recorded false, schema-valid. To make it break K-14 alone, K-11 now checks the *recorded* eligibility, and only K-14 compares it with RE-1. Printed: only `RE-1` errors. CA-1 v3 is unchanged.
- **AA2-N1.** No change, as directed; it is stated in AA §7's uncovered list.
- **LHQ re-pin (closeout).** O-C changed LHQ in place at `18d6eae3e4` (`90f461cb…` → `d59a1ea0…`). I read the diff: one CI-5 sentence (LHQ2-R2) and its change row, saying a mapped CIR validates only under the v0.2 CIR schema `3fb8f586…`. That is the schema RP already vendors (`F/vendor/VENDOR.json`, unchanged) and validates with (A-7, B-19). **Re-pinned** in REPLACEMENT_PACKET.md's supplier pins with a one-line note. The pin appears only in that Design text; no fixture, vendored file or check reads it, so RP's built content is unchanged (`check_rp.py` 99/99; FX-RP1-6 and `F/vendor/` unchanged against `0d23f45985`). It is a pin note in place, and RP stays RP-v0.6.

**Uncovered, stated plainly (AA §7).**
- SR-3's renewal test is textual: an in-lane entry that names the renewal and says "adopts" passes whatever it decides.
- The entry boundary is a heading or a bold item.
- The negation list refuses "adopts … without amendment".

**Checks run.**
- `check_aa.py` **46/46**; `check_ca.py` **37/37** (with archives); `check_rp.py` **99/99** (unchanged code).
- AA, CA, RP and FX-RP1-6 built content is unchanged: rebuilt twice, identical to the committed `0e0036b685` bytes.
- `git diff 0d23f45985` is empty for the RP schema, prototype, fixture and vendor, and for the AA and CA builders and records. The only RP change is the pin line.

**Files (sha256):**

| File | sha256 |
|---|---|
| `PKG-11_…/DEL-11-02_…/Design/ADOPTION_ACCOUNT.md` (AA-v0.3) | `c17c5d8ceed3d32a39f44d460b7321e0a4641fd4ac5641679e595a968fc37f4a` |
| `PKG-11_…/DEL-11-01_…/Design/CONTINUITY_ACCOUNT.md` (CA-v0.4) | `ea171162a236043ef625bf6716242e051240122a28195017034ff9a6abd84e64` |
| `RUN/F/aa/check_aa.py` | `2e1fb631c1417fe684e2156a4d18d6e30ccc6ea70fe7b97b649a804d915395e5` |
| `RUN/F/ca/check_ca.py` | `42b8fa67b83dd59354b57cdb254de30b80e33005d37175110e8c539c0dbbd3fa` |
| `RUN/F/README.md` (shared with EU-F4R) | `7b0a4c9b6b2697b7e9d945bc93da98a050ab2e83820f939c28b134bfe5d82b89` |
| `PKG-11_…/DEL-11-03_…/Design/REPLACEMENT_PACKET.md` (RP-v0.6, LHQ pin note only) | `42eef807a5fbcecb256495b9f1a2e0797f97ed83c5b0142c7d733396106e3d02` |

Superseded: AA-v0.2 `3d4ba2ec…`, CA-v0.3 `8f47aa08…` (from `git show 0e0036b685:…`). Unchanged: the AA schema, `build_aa.py`, `build_ca.py`, the AA and CA records, and every RP path except the one pin line in REPLACEMENT_PACKET.md (superseded text `71eb2881…`).

**Waiting units:** two (EU-F4R for RV2, EU-F3R2 for RV3), each with its own reviewer, as the coordinator directed.

**Next.** DEL-11-03's next revision: adopt `practitioner_standing` with the stated differences (U-PV-3).
