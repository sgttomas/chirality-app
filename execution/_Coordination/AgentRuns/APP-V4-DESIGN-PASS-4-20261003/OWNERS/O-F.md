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
| EU-F1 | DEL-11-03 (early path for PKG-11 and DEL-09-12) | `…/DEL-11-03_Owner replacement evidence packet/Design/REPLACEMENT_PACKET.md`, two schemas, and `_Coordination/…/F/` | see "EU-F1 — refrozen as RP-v0.2" | **REFROZEN 2026-10-04 as RP-v0.2 for RV3** after reader RR-EUF1 (33/33 fields; 2 defects confirmed and repaired) |

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
