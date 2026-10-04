# RV3-EUF1 — review of DEL-11-03 RP-v0.1 (unit EU-F1, owner O-F)

- **Reviewer:** RV3, a Type 2 TASK running as Claude Opus 5.5 (`claude-opus-5-5`). It was dispatched within the HELP_HUMAN session and did not author the unit; same-session review is accepted for design units (OWNER_DECISIONS_2.md). The review was written 2026-10-04. Method: `coordinated-knowledge-work` §3, which asks whether the unit is correct. Usability is the isolated reader's question.
- **Unit as frozen** (`OWNERS/O-F.md` "EU-F1 — frozen"):
  - `REPLACEMENT_PACKET.md` `1a06262b…9c8c`;
  - `rp.disposition.schema.json` `d5a69bc2…99cf`;
  - `rp.packet-manifest.schema.json` `456e4380…1b6c`;
  - `F/` files as listed there;
  - fixture `MANIFEST.sha256` `96291b9c…211b` (all 8 files `OK` under `shasum -c`);
  - key `ec0c8320…11c9`;
  - input set `125eb921…a314`.

  I checked all of these at the start of the review, and all matched.
- **The unit moved during review.** O-F is repairing, citing a finding "EUF1-D1" in the new `rplib.py` docstring. These files changed after the freeze:
  - `F/rplib.py`: 10:47:15, now `2589ccf0…`;
  - `rp.packet-manifest.schema.json`: 10:47:34, now `7dd6dee7…`, requiring `RP-v0.2`;
  - `F/build_fx_rp1.py`: 10:48:24, now `95de6860…`;
  - `F/compare_rp.py`: now `2d76e4f3…`.

  `F/` and DEL-11-03 `Design/` are untracked, so the frozen bytes of these four files cannot be recovered from Git. This review therefore rests on:
  - the frozen design text, which is unchanged;
  - the frozen fixture and key, both unchanged;
  - my rerun of `check_rp.py` against the frozen `rplib.py`. That run took place before 10:47; I infer this because A-9 held, and it fails under the new `rplib.py`.
- **Basis read:**
  - DEL-11-03 `ScopeOfWork.md` (`01773543…`, which matches the pin);
  - S2-F's F-R table and early-unit plan;
  - R23-24, R23-32, R23-33 and R23-36;
  - SQ-v0.2 §8/§9 and `sq.dossier.schema.json`;
  - DOS-v0.1 §4 DH-1/DH-2 and §6;
  - LHQ-v0.1/v0.2 §3 and the CIR schema and examples;
  - EXP-v0.2 `$defs/candidate_subject` (`f7871c96…`);
  - DEL-02-03 `checkpoint-record-entries.schema.json` (`a5271857…`);
  - PRD §8/§11 and EXAMINATION §7.
- **Not read:** anything under `RUN/RR-EUF1/` or the session's rr-euf1 folder.

## Verdict: **REPAIR**

The verdict rests on 1 MAJOR finding. There are also 3 MINOR findings and 3 NOTEs.

Several things stand and can be kept:
- the derived results, all of which recompute from the supplier copies;
- RP-R2, which is stricter than DOS DH-1, never weaker;
- the candidate mapping and its `not_established` result;
- RP-R7 and the disposition;
- the act boundary: no owner act is requested or implied, and v3.0.1 remains the fallback in every undecided state;
- the package shape, which validates against DEL-02-03's `decisionPackageFile` unchanged;
- the basis quotes, which match their sources.

## Findings

### EUF1-R1 — MAJOR — RP-R1's element and obligation status says `met` from dossier records alone, and `not_met` for a `blocked` step (§4.1; REQ-001, AC-001, VER-001; key Q-3)

- **Claim.** §4.1 sets each element's status as follows:
  - `not_met` if a counted step is recorded with any outcome other than `pass`;
  - `met` if every counted step is recorded `pass`;
  - the obligation is `met` only if all seven are `met`;
  - "The status is what the dossier records; established is what the evidence supports."
- **Evidence.**
  - DEL-11-03 AC-001: "any missing evidence prevents claiming that the core-loop obligation is met."
  - VER-001: "Reject a conclusion of at-least-v3.0.1 coverage when any required element lacks applicable evidence."
  - S2-F's own early-unit plan, check (a): "no 'core loop met' while any element lacks an applicable `candidate` `pass` (VER-001)".
  - In the fixture, six elements read `met` on `evidence_standing: illustrative` with every step unresolved (`unresolved_steps` lists all 15).
  - In the other direction, "restart" reads `not_met` because S11-6 is `blocked`. SQ keeps `blocked` apart from `fail`: SQ-R4 "never hides a failed or blocked step"; R23-20 defines `blocked` as stopped by a stated precondition. The cause is an input gap: SQ U-SQ-6, "without it S11-6 is `blocked` (SF-8)". It is not a candidate defect.
- **Consequence.**
  - In the owner's view, the status says more than the evidence supports in one direction, and reads a missing run as a failure in the other.
  - A packet with S11-6 passing but still illustrative would show "core loop: met", which AC-001 forbids.
  - Choosing between ALT-DEFER and ALT-DECLINE depends on knowing whether a gap is a defect or a missing run.
  - Key Q-3 encodes both readings.
- **Repair.**
  - Make status what the evidence supports; `rplib.py`'s new docstring indicates this is under way.
  - Keep the dossier's recorded outcome as a separate field.
  - Give `blocked`, `not-run` and `inconclusive` their own label (for example `not_evidenced`, with the step outcome shown), distinct from `fail`.
  - Then refreeze with a rebuilt fixture, a new input-set id and a re-derived key Q-3. The reader's account stays evidence for IS-FX-RP1-1.

### EUF1-R2 — MINOR — ALT-PUBLISHED is "also a public-release act, which the owner decides separately". It is unclear whether choosing it performs the release (§6.1; package `alternatives[1]`; key Q-7)

- **Evidence.**
  - Package: "This is also a public-release act, which the owner decides separately (PRD OQ-08; DEL-11-03 CLM-003)". Its first consequence states, unconditionally, "v3.0.1 is no longer the fallback for the published product".
  - CLM-003: "The owner retains public-release decisions … None follows from replacement".
  - R23-32 keeps P-5 (public release) as its own act.
  - R23-32.5 rules "published replacement (also a release act)", so the label follows the ruling.
- **Consequence.** A decision maker cannot tell whether choosing ALT-PUBLISHED performs P-5, or needs P-5 as a second act, before v3.0.1 stops being the published fallback. That touches "nothing requests or implies an owner act".
- **Repair.** "Requires the separate public-release act (P-5, OQ-08); choosing this alternative does not perform it. Until that act, v3.0.1 remains the published product." Make the first consequence conditional on that act, and define the key's `also_a_public_release_act` accordingly.

### EUF1-R3 — MINOR — key Q-9 and Q-11 rest on first-cut inputs that O-F wrote, not on supplier records (§3.3; manifest `supplied` S-4/S-5; key Q-9, Q-11)

- **Evidence.**
  - The manifest gives the source of `continuity-handoff.json` and `practitioner-standing.json` as `rp.packet-manifest.schema.json` `$defs/continuity_input` and `$defs/practitioner_standing`, which are O-F's own schema.
  - DEL-11-01 and DEL-09-12 have no files yet (§0).
  - The reader brief says only that "supplier evidence is illustrative (copied from schema examples)".
- **Consequence.** The values are not wrong:
  - the thesis tree `47fc49e9…` equals PRD §11 at `d2929fd62b` and at HEAD;
  - `remote_rechecked: false` matches REFERENCES §2's standing.

  But the key presents them as if a supplier had stated them. The manifest's `source` should say "first cut by the DEL-11-03 owner pending DEL-11-01/DEL-09-12", and the key should mark Q-9 and Q-11 as grounded there.
- **Repair.** Relabel `source`, and add a note to the key's `why`.

### EUF1-R4 — MINOR — reconciliation compares `app_candidate` objects literally, so an unpackaged candidate whose CIR omits `packaged` reads `differ` (§5 "Reconciliation values"; `rplib.reconcile`)

- **Evidence.**
  - §5: "`reconciled`: both map, and their `app_candidate` objects are equal".
  - The SQ mapping always emits `packaged` (§5: "`packaged` = whether `package_record` is present").
  - EXP's `candidate_subject.app_candidate` and LHQ-v0.2's `app_candidate_subject` both make `packaged` optional.
  - Demonstrated with the current `rplib`: a CIR with `app_candidate_subject: {revision: r1, build_identity: b1}` against SQ `{revision: r1, build_identity: b1}` gives `differ`.
- **Consequence.** A false `differ` blocks joining two results for one candidate (RP-R3, RP-R4).
- **Repair.** Treat an absent `packaged` as `false` before comparing, or compare `revision`, `build_identity` and `package_record`. Add a B-case for it.

## Notes

- **N1 — A-8 now fails, as designed.** `check_rp.py` on the frozen bytes gives 43/44; the only failure is A-8. `lhq.candidate-identification.valid.examples.json` moved from `dcb9f4a0…` to `c7684ee5…` under O-C's LHQ-v0.2. The copied record `LHQ-CIR-EXAMPLE-STATE-2026-10-03` is byte-equal in HEAD and in the current file. RP-R8 / RF-4 caught a supplier change, which is what it is for. The refreeze needs the new source sha256.
- **N2 — the state mid-repair.** Against the current working files, `check_rp.py` gives 37/44: A-2, A-8, A-9, B-1, B-6, B-9 and B-18 fail. These are the frozen fixture against the new rules and schema, as expected during a repair. It is not a finding. I will confirm the repair on the refrozen bytes.
- **N3 — the key self-check.** `compare_rp.py --self-check` gives 16 HOLDS and none failing, against the frozen key and fixture. The run used both the frozen and the changed `compare_rp.py`; the result is the same.

## The brief's questions

- **Rules RP-R1…R8.**
  - RP-R1 needs repair (EUF1-R1).
  - RP-R2 applies DOS DH-1 by relying on the dossier's `counts_as_completed_witness`, which DOS sets under DH-1. It adds an acceptance act with actor ≠ recorder, an independent review record and a candidate `pass`. These are stricter conditions, matching REQ-002 ("to the person's acceptance").
  - RP-R3/R4: correct apart from EUF1-R4.
  - RP-R5: practitioner standing is shown and never consulted (A-12; REQ-005).
  - RP-R6/R7/R8: correct. B-21…B-32 all hold, and each refuses for its own rule.
- **Derived results follow from the supplier records.**
  - I derived the core-loop table independently from `sq-dossier.SQ-EX-05.json`, step by step (scenario, element, counts, state, outcome). It matches the manifest: J-8R and J-9R are uncounted; V4-EXM-12's six steps are outside; restart has S11-5 `pass` and S11-6 `blocked`.
  - The journey matches DOS-EXAMPLE-INVENTED's `handoff_del_11_03`: not counted, 0 acceptance acts, no review record, P20-A `not-run`.
  - The candidate matches SQ's `candidate` mapped to EXP; the CIR's `app_candidate` is `not_supplied`, so the result is `not_established`.
  - The gaps G-* and `not_complete_because` follow from these.
  - Source records: SQ-EX-05 and DOS-EXAMPLE-INVENTED equal their source files at the named sha256. The CIR record is equal and its file has moved (N1).
- **No owner act requested or implied; v3.0.1 stays the fallback.**
  - The disposition is `not_presented`, with no `decision` element, and `limits` says "no owner act exists or is implied".
  - The package `purpose` says "not for presentation to the owner".
  - Every alternative states "No retirement".
  - ALT-OWN-USE, ALT-DEFER and ALT-DECLINE keep v3.0.1 as the fallback.
  - The only qualification is EUF1-R2.
- **The key is fair and grounded in primary records.**
  - Q-1, Q-2, Q-4, Q-5, Q-6, Q-8, Q-10 and Q-12 follow from the fixture records and the supplier copies.
  - Q-3 is fair to the frozen packet ("what status does the packet give") but encodes EUF1-R1.
  - Q-7 follows R23-32.5's label (EUF1-R2).
  - Q-9 and Q-11 rest on O-F-authored first-cut inputs (EUF1-R3).

## What I checked and how

- `shasum -a 256` on every listed file, at the start and again after I noticed the change.
- `python3 -B check_rp.py`: 43/44 on the frozen bytes, then 37/44 mid-repair.
- `python3 -B compare_rp.py --self-check`: 16/16.
- Independent derivation of the core-loop table, journey and candidate from the supplied copies (a short script in scratch).
- `jsonschema` 2020-12, run by me:
  - the package against DEL-02-03 `$defs/decisionPackageFile`: 0 errors;
  - the disposition against `rp.disposition.schema.json`: 0 errors;
  - the frozen manifest schema: A-2 held in my frozen run.
- The package's `subject[1]` equals the manifest sha256 `c6c62225…`. The disposition's `package_file.sha256` equals the package (`7e5e8dbb…`).
- Basis and `reservedBy` quotes against PRD, EXAMINATION and the ScopeOfWork: each matches after whitespace normalisation (the sources are hard-wrapped), and each `source_sha256` equals the current file.
- Thesis tree: `git rev-parse d2929fd62b:…/foundation/thesis` and `HEAD:…` both give `47fc49e9…`, equal to PRD §11. The working tree is clean there.

## What I did not check

- The usability of the reader's account (not read).
- `stage_is.py`'s staging (not rerun).
- Determinism of the builder (the builder has changed).
- REFERENCES §2's remote values (no network).
- The repaired RP-v0.2 bytes: these come back to me when they are refrozen.

---

# Addendum — O-C's RQ-LHQ-1 change in DEL-09-07 (LHQ-v0.2, under R23-36), 2026-10-04

- **Subject** (`OWNERS/O-C.md` "Tranche 2: RQ-LHQ-1"), each re-hashed and matching:
  - `LOCAL_HOST_QUALIFICATION.md` `5cd31e09…f07b`;
  - `lhq.candidate-identification.schema.json` `3fb8f586…5fc5`;
  - `….valid.examples.json` `c7684ee5…d9d4`;
  - `….invalid.examples.json` `b823d54b…ceed`.

  Before-state: the HEAD blobs (LHQ-v0.1 `20361a0b…`).

## Verdict: **READY**

There is no BLOCKING or MAJOR finding. There are 2 MINOR findings and 1 NOTE.

## Answers to the four questions

1. **Purely additive; earlier examples behave as before.**
   - `git diff HEAD`, text: one row's pointer, the CI-5 bullet, the header and a "Changes" table. Nothing else changed.
   - `git diff HEAD`, schema: one optional property, one `$def` and one top-level `allOf` guard.
   - The HEAD valid example is unchanged in the current file and validates under both the old and new schemas, with 0 errors.
   - Each of the three HEAD invalid examples is unchanged and is rejected under both schemas with the same single error: CI-1, BR-2 and the ladder.
   - New examples:
     - valid `LHQ-CIR-EXAMPLE-MAPPED`: 0 errors;
     - invalid "CI-5: a mapping while … not supplied": 1 error, the guard;
     - invalid "packaged without its package record": 1 error, `package_record` required.
2. **The element equals EXP-v0.2's `candidate_subject.app_candidate`.** A Python equality test of `$defs/app_candidate_subject` against EXP (`f7871c96…`) `$defs/candidate_subject.properties.app_candidate` gives `True`. Wrapped as `{kind: candidate, app_candidate: …}`, the new example's mapping validates against EXP's own `candidate_subject` with 0 errors.
3. **CI-5's guard holds.** With the mapping present:
   - standing `observed`, `host_stated` or `app_stated`: 0 errors;
   - standing `not_supplied`: rejected ("'not_supplied' should not be valid …").

   The element's existing CI-1 rule still forbids a `value` when it is not supplied.
4. **EU-F1 can reconcile a CIR with the canonical identity when one is supplied.** Tested with O-F's current `rplib.map_cir_candidate` / `reconcile`, which read `app_candidate_subject`:
   - mapped example against an equal SQ candidate → `reconciled`;
   - mapped example against a different revision → `differ`;
   - the earlier `not_supplied` example → `not_established`.

   One caveat is EUF1-R4: an omitted `packaged` against SQ's explicit `false` gives a false `differ`. That is a consumer fix in DEL-11-03, not an LHQ defect.

## Findings

### LHQ2-R1 — MINOR — CI-5 says nothing about the mapping agreeing with the element's `value`

- **Evidence.** The schema accepts a CIR whose `app_candidate_subject.revision` is changed to "DIFFERENT" while `elements.app_candidate.value` still names `…+abc1234` (tested). CI-5: "It changes nothing in `value`, `source` or `standing`."
- **Consequence.** Two identities can disagree in one record, and a consumer reconciling on the mapping would not see it.
- **Repair.** One sentence in CI-5: both describe the same build; a disagreement is a CIR defect for the examiner (a schema cannot check it); and the mapping is what consumers reconcile on.

### LHQ2-R2 — MINOR — mapped CIRs keep `format: LHQ-v0.1` and `$id …:0.1`, but the v0.1 schema rejects them

- **Evidence.** The new valid example under the HEAD schema gives "Additional properties are not allowed ('app_candidate_subject' was unexpected)". O-C records that TOP and DOS keep their LHQ-v0.1 pins (R23-21 item 3), and DOS cites the CIR schema.
- **Consequence.** Older records stay valid under the new schema, but a new mapped record fails against a consumer's pinned v0.1 schema while carrying the same format label. The R23-23.3 precedent (AAC/RS: no format bump for additive rows) covers the label, but the dependence on the schema version is not stated.
- **Repair.** No bump is needed under R23-23.3. Add one line to CI-5 or the schema description: a CIR carrying `app_candidate_subject` validates only under LHQ-v0.2's schema. Make sure the closeout's stale-pin pass (R23-21 item 4) puts DOS's pin in front of its owner, rather than re-pinning it by script.

### Note

The `allOf`/`if`/`not` guard is the form DEL-02-03's subset checker could not read (R23-23.1). O-C reports that DEL-01-01's subset validator handles it. I did not run DEL-01-01's validator; I ran `jsonschema` only.

## How I checked

- Re-hashed the four files.
- `git diff HEAD` on the text and schema.
- A `jsonschema` Draft 2020-12 script over every HEAD and current example, under both schemas.
- Guard edge cases built by deep-copying the mapped example.
- The `$defs` equality test against EXP.
- Reconciliation exercised through O-F's current `rplib` functions.
- Not run: `top_check.py`; DEL-01-01's subset validator.

---

# Addendum 2 — RP-v0.2 (refrozen after RR-EUF1), 2026-10-04

- **Subject** (`O-F.md` "EU-F1 — refrozen as RP-v0.2"). All files were re-hashed and match:
  - `REPLACEMENT_PACKET.md` `80e88983…1869`;
  - `rp.packet-manifest.schema.json` `7dd6dee7…70f6`;
  - `rp.disposition.schema.json` `d5a69bc2…` (unchanged);
  - `F/rplib.py` `2589ccf0…`, `build_fx_rp1.py` `532219a3…`, `check_rp.py` `e2886b4d…`, `compare_rp.py` `2d76e4f3…`, `stage_is.py` `120d9eae…`;
  - `FX-RP1-2/MANIFEST.sha256` `534cd210…` (all 9 files `OK`);
  - `IS-FX-RP1-2.input-set.sha256` `e1fd19df…`;
  - the brief, account schema and key v2.
- **Key handling.** I formed my own expected answers to Q-1…Q-12 from the fixture and the rules before opening `EU-F1-2.answer-key.json` (`52eaf68e…`).
- **Checks.**
  - `check_rp.py`: 57/57 at first.
  - `compare_rp.py --set 2 --self-check`: 16/16.
  - All eight `basis-excerpts.md` blocks are byte-exact against their sources, at the line ranges and sha256 values stated.
- **Not read:** `RUN/RR-EUF1/` and anything belonging to the second reader.

## Verdict on RP-v0.2: **REPAIR**

There is 1 MAJOR finding: a new one, about when the packet may be put to the owner. There are also 4 MINOR findings (three carried over, one new) and 2 NOTEs.

The two rule defects O-F names are genuinely fixed:
- EUF1-D1 (RP-R1);
- EUF1-D2 (RP-R2 receipts).

So are the legibility repairs:
- `terms`, including A16 matching ACT-v0.10 §2.1's row;
- `basis_excerpts`;
- `comparison_rule`, a faithful paraphrase of EXAMINATION §7;
- `produced_by` and `source_kind`;
- `dossier_review`;
- the subject's "whether, and at what scope", and the ALT-OWN-USE statement.

## Status of the RP-v0.1 findings

| Finding | At RP-v0.2 |
|---|---|
| EUF1-R1 MAJOR (RP-R1) | **Half resolved, so downgraded to MINOR (EUF1-R1b).** `status` now requires resolved candidate evidence, `recorded` is kept apart, and the fixture shows all seven elements and the obligation as `not_evidenced`. **Not resolved:** with resolved evidence, `rplib.core_loop` still maps any recorded outcome other than pass to `not_met`. A candidate EXP record that is `blocked`, `not-run` or `inconclusive` therefore reads as a failure (`recorded_not_pass → not_met`). R23-20 and SQ-R4 keep those outcomes apart from `fail`. Repair: `not_met` only when some counted step is `fail`; otherwise `not_evidenced`, with the outcome shown. Add a B-case |
| EUF1-R2 MINOR (ALT-PUBLISHED) | **Not resolved.** The wording is unchanged: "also a public-release act, which the owner decides separately", while the first consequence still reads, unconditionally, "v3.0.1 is no longer the fallback for the published product". Key Q-7 still encodes it |
| EUF1-R3 MINOR (first-cut grounding) | **Resolved.** S-4 and S-5 are `source_kind: shape_only`, with `produced_by` naming DEL-11-03's builder standing in for DEL-11-01/DEL-09-12 |
| EUF1-R4 MINOR (`packaged` omitted → false `differ`) | **Not resolved.** `rplib.py` is byte-identical to what I tested (`2589ccf0…`). The B-18…B-24 cases use O-C's packaged example, so they do not exercise the case |

## New findings

### EUF2-R1 — MAJOR — the packet now states two contradictory conditions for presenting the reserved decision, and cites AX-001 for one that AX-001 does not state (§3 `gaps` bullet; fixture `gaps[].point_of_need`; against §2 O-1, §6.3 step 5, §7 RF-1, `open_matters` P-1)

- **Claim.**
  - §3: "A gap never gates presentation: AX-001 lets a packet 'accurately report partial or adverse evidence'".
  - Each fixture gap: "(presentation is not gated: DEL-11-03 AX-001)".
- **Evidence.**
  - AX-001 (byte-exact in the packet's own `basis-excerpts.md`): "A packet may accurately report partial or adverse evidence, but cannot claim replacement qualification until both applicable witnesses hold". It does not speak to presentation.
  - EXAMINATION §7, also excerpted: "The evidence presented for that decision is: V4-EXM-10 and V4-EXM-11 passed … and V4-EXM-20 passed".
  - The design itself keeps the gate in several places:
    - §2 O-1, point of need "When both witnesses exist";
    - §6.3 step 5, "When both witnesses are established and the coordinator presents the package";
    - RF-1, "Packet kept; not presented";
    - the manifest's P-1, "when both witnesses exist; an act, not a question now".
- **Consequence.**
  - The person deciding, and the second reader, are told both that the decision is not put to the owner before both witnesses exist, and that gaps never gate presentation.
  - The second statement is an inference attributed to a contract clause.
  - It bears on the act boundary (whether the owner may be asked now) and on what ALT-DEFER and ALT-DECLINE mean with gaps open.
  - RP-v0.1 was consistent here. The I-10 repair over-corrected: the reader's point concerned only a fixture that is never presented.
- **Repair.** Pick one condition and state it everywhere. Mark the choice DERIVED from EXAMINATION §7, or ask HELP_HUMAN for a one-line ruling if presenting a gapped packet, for example for DEFER or DECLINE, is wanted. If the gate stays, a gap's point of need can read "before the package is presented to the owner (EXAMINATION §7); this fixture is never presented". Drop the AX-001 attribution in either case.

### EUF2-R2 — MINOR — FX-RP1-2 is already out of date: O-C's EUF1-S1 repair changed `DOS-EXAMPLE-INVENTED` (A-8 fails; G-J-WITNESS's RC-1 clause rests on the superseded example)

- **Evidence.**
  - On rerunning `check_rp.py` after 10:55, the result is 56/57, with A-8 failing.
  - Source `lhq.dossier-manifest.valid.examples.json`: `4d659926…` at refreeze, now `9873df65…`.
  - O-C's DOS change (DX-1, DX-2): "`DOS-EXAMPLE-INVENTED` (no case run) names no receipt anywhere". The fixture copy still has RC-1 in `handoff_del_09_11.receipt_refs`. Hence:
    - the manifest's `receipts_in_dossier_missing_from_handoff`;
    - G-J-WITNESS's clause "the dossier names a host receipt (RC-1 (invented)) that its hand-over to DEL-11-03 does not list".
- **Consequence.**
  - RP-R8 and RF-4 are working as designed. The second reader's account stays valid evidence for IS-FX-RP1-2.
  - The next fixture build drops that reason. G-J-WITNESS remains for its other four reasons, so the key's Q-4 and Q-6 fields are unaffected.
  - EUF1-D2's positive case now has a supplier counterpart in O-C's `DOS-EXAMPLE-INVENTED-POPULATED`. That record lists RC-1 in all three places, and it can replace the in-memory case.
- **Repair.** Rebuild after EUF2-R1 under a new input-set id; add a B-case on the populated example. FX-RP1-2 and IS-FX-RP1-2 stay as history.

## The key (EU-F1-2)

My independent expectations match every field of `EU-F1-2.answer-key.json`:
- Q-1, Q-2 and Q-4…Q-12 exactly;
- Q-3: all seven elements and the obligation `not_evidenced`, `established: false`, outside scenarios `V4-EXM-12`.

The key is fair and grounded:
- the core-loop fields follow from SQ-EX-05 under the repaired RP-R1;
- the journey fields from the DOS copy;
- the candidate fields from the SQ and CIR copies;
- Q-9 and Q-11 now visibly rest on `shape_only` inputs.

It does not depend on the packet's own inferences. It inherits EUF1-R2 at Q-7 ALT-PUBLISHED. No question tests EUF1-D2 (receipts); A-15 covers it mechanically. KEY-F1 on the first key is correct: that key's Q-3 encoded the defect my EUF1-R1 described.

## Notes

- **N4.** `check_rp.py` has no option to select a fixture: `--fixture` is ignored, and the default fixture runs. So I could not reproduce O-F's claim that A-13, A-15, A-16 and A-17 fail on FX-RP1. I did not check it.
- **N5.** The v2 reader-account schema differs from v1 only in `$id`, description and the input-set constant (diff). The brief differs only in the input-set name and schema name. This confirms the comparison is like for like.

## Act boundary, again

On RP-v0.2's bytes:
- the disposition is `not_presented` with no decision element;
- `limits` says no owner act exists or is implied;
- the package `purpose` says it is not for presentation to the owner;
- every alternative states "No retirement";
- v3.0.1 remains the fallback in every undecided state.

The only qualifications are EUF1-R2 and EUF2-R1.

---

# Addendum 3 — confirming O-C's repairs at `141a6cc8b4` (EUF1-S1, LHQ2-R1), 2026-10-04

- **Subject:** commit `141a6cc8b4` ("DEL-09-07 LHQ-v0.2 + DOS DX rules (EUF1-S1, LHQ2-R1)"). The working tree of DEL-09-07 `Design/` is clean against it (`git status` empty).
- **Hashes.** Every file in `O-C.md`'s hash table was re-hashed and matches, including:
  - `QUALIFICATION_DOSSIER.md` `687032c0…8465`;
  - `LOCAL_HOST_QUALIFICATION.md` `90f461cb…523e`;
  - `dos_check.py` `07bc7791…2903`;
  - `cir_check.py` `6f32a951…2bad`;
  - the unchanged CIR schema `3fb8f586…` and the unchanged `top_check.py` `cf128073…`.

  The two prototype hashes embedded in the DOS and LHQ texts equal the files.

## Verdict: **both repairs confirmed**

There are no BLOCKING, MAJOR or MINOR findings, and 2 NOTEs.
- LHQ2-R1 is closed.
- O-F's EUF1-S1 is closed on the supplier side.
- LHQ-v0.2 at `90f461cb…` stays **READY**. This supersedes my confirmation of `5cd31e09…`.

LHQ2-R2 (DOS's pinned CIR schema) stays held for the closeout, as directed.

## What I reran

| Check | Input | Result |
|---|---|---|
| `dos_check.py` | dossier valid examples | exit 0: `DOS-EXAMPLE-INVENTED` OK, `DOS-EXAMPLE-INVENTED-POPULATED` OK |
| `dos_check.py` | `dx-violations` | exit 1. Each of the three fails for its own rule: the old example (DX-1 and DX-2), resolution differs (DX-1), missing from DEL-11-03 (DX-2) |
| `dos_check.py` | dossier invalid examples | exit 0 (none carries a DX inconsistency any longer) |
| `cir_check.py` | CIR valid examples | exit 0 (both OK) |
| `cir_check.py` | `ci5-violations` | exit 1. Both fail: the revision mismatch and the build-identity mismatch |
| `cir_check.py` | CIR invalid examples | exit 0 (does not trip on them) |
| `top_check.py` | traffic valid examples | exit 0 (4 of 5 contacts compared) |
| `top_check.py` | `cb1-violations` | exit 1. Both MIS-TAGGED |

**Schemas: my own `jsonschema` Draft 2020-12 run.** All three pass `check_schema`.

| File | Items | Errors each |
|---|---|---|
| dossier valid | 2 | 0 |
| dossier invalid | 7 | 1 |
| dossier `dx-violations` | 3 | 0 (schema-valid, as intended) |
| CIR valid | 2 | 0 |
| CIR invalid | 5 | 1 |
| CIR `ci5-violations` | 2 | 0 |
| traffic valid | 1 | 0 |
| traffic invalid | 12 | 1 each, except one with 2 (see note) |
| traffic `cb1-violations` | 2 | 0 |

CIR `$defs/app_candidate_subject` still equals EXP-v0.2's `candidate_subject.app_candidate` (Python equality).

## Substance

- **EUF1-S1.**
  - The record set:
    - `DOS-EXAMPLE-INVENTED` names no receipt anywhere: the index, the DEL-11-03 hand-over and the DEL-09-11 hand-over are all empty.
    - `DOS-EXAMPLE-INVENTED-POPULATED` lists RC-1 in all three places, *unresolvable* each time. Its LHQ-20 result is `inconclusive`, and a limitation states why RC-1 cannot be resolved.
  - **DX-1 and DX-2** state what DOS §1 already required and make it checkable.
  - **For O-F's RP-v0.3:**
    - the rebuilt fixture's copy of `DOS-EXAMPLE-INVENTED` loses the RC-1 clause and the `receipts_in_dossier_missing_from_handoff` reason (EUF2-R2);
    - the populated example gives EUF1-D2's receipt rule a real-file positive case;
    - under DX-2 a DOS-conformant dossier can no longer omit a receipt from the DEL-11-03 hand-over, so RP-R2's check becomes a defence in depth (keep it).
- **LHQ2-R1.** CI-5 now reads: "When both `value` and `app_candidate_subject` are given, they describe the same build, and a disagreement is a CIR defect for the examiner. The mapping is what consumers reconcile on …". Both violation records are schema-valid and rejected by `cir_check`. That is exactly the gap I demonstrated: the schema accepted a contradicting mapping.

## Notes

- **N6.** `cir_check` is a substring test.
  - A mapping whose `revision` is a shorter prefix of the one `value` names passes. Tested: `abc` against a value containing `abc1234` gives OK.
  - The text says "Passing it is necessary, not sufficient", which is accurate.
  - If CIRs come to carry full revision hashes, a token or whole-word match would be tighter. No repair is required now.
- **N7.** One traffic-observation invalid example gives 2 errors under `jsonschema`. That file has not changed since `d150856784` (tranche 1) and is not part of this change. It is recorded only so that "fails only for its stated rule", which O-C claims for the dossier invalid examples, is not read as covering the traffic file.

## Not run

DEL-01-01's subset validator (O-C reports it agrees). I ran `jsonschema` only.

---

# Addendum 4 — RP-v0.3 (refrozen; committed `741d55094d`), with RR-EUF3's result, 2026-10-04

- **Subject** (`O-F.md` "EU-F1 — RP-v0.3"). All files were re-hashed and match:
  - `REPLACEMENT_PACKET.md` `164c082c…f9af`;
  - `rp.packet-manifest.schema.json` `20de252d…8b64`;
  - `rp.disposition.schema.json` `d5a69bc2…` (unchanged);
  - `F/rplib.py` `89fc8e64…`, `build_fx_rp1.py` `4bdad3a7…`, `check_rp.py` `11104ded…`, `compare_rp.py` `208903ab…`, `stage_is.py` `5845d029…`;
  - `EU-F1.key-grounding.md` `7158f256…`, `vendor/VENDOR.json` `4d9e4158…`;
  - FX-RP1-3 `MANIFEST.sha256` `ca5c8665…` (all 11 files `OK`);
  - `IS-FX-RP1-3.input-set.sha256` `537d8b81…`;
  - key `EU-F1-3.answer-key.json` `80873710…`.

  The working tree is clean for the unit's paths, and `git status --ignored` lists none of them (R23-48.1).
- **Reader's result read before confirming (P-E6).** `RR-EUF3/account.json` (`862be3c5…`), `COMPARE.txt` (`6daa6976…`), `DISPATCH_RECORD.md`, and R23-49.

## Verdict on RP-v0.3: **READY**

Every finding of mine is resolved. RR-EUF3's eight referred issues are legibility points except three:
- one supplier-example defect, which goes to O-C as R23-49 says;
- two small defects in the packet's own text;
- one latent rule gap.

Each of the three is MINOR and none blocks the unit; they belong in O-F's next unit (R23-49.2).

## My findings, confirmed

| Finding | State | How I checked |
|---|---|---|
| EUF1-R1b (blocked folded into `not_met`) | **Resolved** | I called `rplib.core_loop` with every counted result resolved to a candidate record, varying S11-6's outcome. `fail` gives restart `recorded_fail`/`not_met` and obligation `not_met`. `blocked`, `not-run` and `inconclusive` give `recorded_blocked`, `recorded_not_run` and `recorded_inconclusive`, each with status `not_evidenced`. `pass` gives `met`. Unresolved results give `not_evidenced` |
| EUF1-R2 (ALT-PUBLISHED) | **Resolved** | The package consequence reads "Choosing this alternative does not perform the public-release act; publishing remains a separate owner act (P-5; PRD OQ-08; DEL-11-03 CLM-003)" and "Until the owner performs that act, v3.0.1 remains the published product and the fallback". RP-R6 refuses an ALT-PUBLISHED without that wording (B-35). Key Q-7 now asks the unambiguous questions |
| EUF1-R3 (first-cut grounding) | **Resolved** | `source_kind`/`shape` on S-4 and S-5. `EU-F1.key-grounding.md` marks Q-9 and Q-11 as first cut (O-F) |
| EUF1-R4 (literal identity comparison) | **Resolved** | `identity_key` probes: an omitted `packaged` against SQ's explicit false gives `reconciled`; packaged true against unpackaged gives `differ`; explicit false gives `reconciled` |
| EUF2-R1 under R23-43 | **Resolved** | Gaps read "before the packet can claim replacement qualification (AX-001: a packet \"cannot claim replacement qualification until both applicable witnesses hold\"); it does not hold back putting the packet to the owner", with AX-001 quoted in its own words. §2 O-1, §6.3 step 5, RF-1, P-1 and the purpose all match. A-16, A-19 and B-36 hold it |
| EUF2-R2 (DOS example moved) | **Resolved** | FX-RP1-3's DOS copy is O-C's repaired `DOS-EXAMPLE-INVENTED`, with no receipts. B-13…B-15 use the repaired and the populated examples |
| N4 (`--fixture` ignored) | **Resolved** | `check_rp.py --fixture FX-RP1` gives 9/20 and `--fixture FX-RP1-2` gives 12/20, as O-F states. The failures name the checks the old fixtures cannot meet |

**Correction to my EUF1-R1 (O-F's observation; your slip carried into it).** In SQ-EX-05, S11-6 is `blocked` because stimulus ST-4 was `not_produced`, with cause "route cannot delegate; no recording (U-SQ-5)". ST-5 was produced by replay. I cited SQ's general U-SQ-6 row instead of the record's own cause. The conclusion, an input gap and not a candidate defect, stands. RP-v0.3 copies the record's cause, which is correct.

## Other things checked

- **EUF2-D1 (an illustrative review read as present): confirmed repaired.**
  - `dossier_review.state` is `present` only when the named record is among the supplied reviews; otherwise it is `named_not_resolved`, which holds back "established". This is how FX-RP1-3 reads.
  - *Note:* "resolves" means the record's id is supplied. Nothing checks the review's subject or its separation. Name that as a limit, or check it once real review records exist.
- **Vendored supplier bytes (R23-44): all 8 hold.** Each file in `F/vendor/` equals the sha256 in `VENDOR.json`, the blob at its stated source commit, and the live source today. `check_rp.py` V-1 reports drift as a NOTICE and none is reported.
- **Checks rerun.**
  - `check_rp.py`: 65/65, with no NOTICE.
  - `compare_rp.py --set 3 --self-check`: 18/18.
- **Key EU-F1-3.** I formed my own answers to Q-1…Q-13 from FX-RP1-3 and the v3 brief and schema first. Comparing field by field (set fields as sets) gives **0 differences**.
  - Q-13's "any time" is stated inside the input set: in the legend's manifest description, P-1's point of need and the R23-43 term. A reader can therefore reach it from the files.
  - The key is fair and grounded as the grounding file states.

## RR-EUF3: 36/36 fields; which referred issues are defects

I read the account's statements against the files and found no contradiction. The reader got the three points that matter right: presentation at any time with no qualification claimed, ALT-PUBLISHED's separate release act, and blocked as a missing result.

| # | Issue | Judgment |
|---|---|---|
| 1 | No identifiable candidate in the subject | Legibility in the fixture. **There is also a latent rule gap (MINOR, O-F).** Under R23-43 a real packet may be put to the owner at any time, and REQ-004 requires it to "identify the exact proposed fallback-replacement scope and candidate". `check_package` has no rule that refuses a placeholder candidate, or `evidence_standing: illustrative`, in a packet that is not a fixture. Add one, for example by refusing presentation (`presented_no_decision`) of a package whose subject is a placeholder or whose packet is illustrative |
| 2 | Not-run dossier names a journey run | **A defect in the supplier example (O-C), as R23-49.2 rules.** `DOS-EXAMPLE-INVENTED` has all four cases with `not-run-example` results and the limitation "no case has run", yet `handoff_del_09_11` names `journey_run_ref: LHQ-20-EXAMPLE-RUN`, a record set and run authors. DX-1 and DX-2 cover receipts only, so `dos_check` does not catch this. A DX-3-style check (a not-run journey case carries no run reference) would |
| 3 | CIR contributions "answered" | Legibility. The term defines it, and the CA §7.2 ladder is the supplier's vocabulary |
| 4 | Dossier says independent; review unresolved | Legibility. The packet already handles this correctly (`named_not_resolved`; not established) |
| 5 | No measured v3.0.1 baseline | Legibility, by design: F-R2 and `comparison_rule` (EXAMINATION §7) |
| 6 | Fallback and the ALT-PUBLISHED inference not re-checked | Mostly legibility, since both are labelled. **One small wording defect (MINOR, O-F).** The excerpt says "Manual checks read its latest published stable release … opens in the system browser on request". The consequence says v3.0.x installs "check the latest published stable release, so they would be offered v4", which drops "manual" and "on request". Restate it as "a v3.0.x install's manual update check would find v4". The excerpt's "does not assert the latest remote release" concerns the record's knowledge of the current release; it does not contradict the mechanism |
| 7 | Cited clauses not supplied | Mostly legibility. **One false statement in the packet (MINOR, O-F).** The term for "CLM-001, CLM-003, REQ-004, REQ-005, REQ-006, AX-001, VER-003, VER-004" says "those of DEL-11-03 are excerpted". `basis-excerpts.md` holds only CLM-001, CLM-003, REQ-004, REQ-005 and AX-001; REQ-006, VER-003 and VER-004 are not excerpted. Either excerpt them or say which ones are |
| 8 | Refinement steps counted as workflow saving | Legibility for the packet. The mapping is SQ's step map (O-B's), carried by RP-R1 one for one. Whether "reuse" should rest on J-7 alone is a question for SQ's owner at its next revision, not a packet defect |

## Not run

- `stage_is.py --set 3` (the reader's `SUPPLIED.sha256` has 14 entries, and O-F reports every hash matched).
- The builder's determinism.

---

# Addendum 5 — confirming O-C's DX-3 fix for RR-EUF3's run-artefact point (R23-49; commit `aa95aff4e1`), 2026-10-04

- **Subject.** Re-hashed, all as in `O-C.md` "Tranche 2: RR-EUF3 item (R23-49)":
  - `QUALIFICATION_DOSSIER.md` `8c4f4fa1…`;
  - dossier valid examples `dbf8463f…`, invalid `571e7ddb…`, `dx-violations` `8a183339…`, `exp-outcomes` `15d9ae2d…`;
  - `prototype/dos_check.py` `bf20d8fc…`;
  - the dossier schema `88cd9948…`, unchanged.

  `git status --ignored` on DEL-09-07 `Design/` is clean.

## Verdict: **confirmed**

There are no BLOCKING, MAJOR or MINOR findings, and 2 NOTEs. The point I graded as a supplier defect in Addendum 4 (item 2) is fixed, and the check I suggested ("a DX-3-style check") exists and works.

- **The examples.**
  - `DOS-EXAMPLE-INVENTED` no longer has a DEL-09-11 hand-over. A limitation states why: "LHQ-20 not run: no source journey, so no DEL-09-11 hand-over, and the DEL-11-03 hand-over names no run (DX-3)".
  - `DOS-EXAMPLE-INVENTED-POPULATED` now says "only LHQ-20 has run (outcome inconclusive)". Its withheld item names its own case results.
- **DX-3** (`dos_check.py --outcomes lhq.dossier-manifest.exp-outcomes.examples.json`):

| Input | Exit | Result |
|---|---|---|
| valid examples | 0 | both OK |
| invalid examples | 0 | no DX finding |
| `dx-violations` | 1 | all 5 fail for their stated rules. `DX-VIOL-not-run-names-run` gives "names run LHQ-20-EXAMPLE-RUN". `DX-VIOL-not-run-11-03-names-acts` reports acts and receipts under DX-3 only, because its receipt is indexed |

- **Schemas** (my own `jsonschema` 2020-12 run): every example file behaves as O-C's table states.
  - Dossier: valid 2 × 0; invalid 7 × 1; DX violations 5 × 0.
  - CIR: 2 × 0; 5 × 1; CI-5 violations 2 × 0.
  - Traffic: 1 × 0; 12 rejected (one with 2 errors, as noted before); CB-1 violations 2 × 0.
- **Other checkers.** `cir_check` and `top_check` give exit 0 on the valid examples and exit 1 on their violation files.

## Notes

- **N8 — "not checked" exits 0.** Without `--outcomes`, DX-3 prints "DX-3 not checked: no outcome supplied …" and still exits 0 (tested). The text is honest, but a caller that reads only the exit status would pass the rule silently. A `--require-outcomes` flag, or a distinct exit code for "not checked", would close this.
- **N9 — knock-on for EU-F1 (R23-44 working as designed).** `check_rp.py` still holds 65/65, and now prints "NOTICE the live supplier file for lhq_manifest_examples has moved since vendoring (9873df65c9b4 -> dbf8463f45dc); re-pin deliberately (R23-21)". RP-v0.3's fixture copy of `DOS-EXAMPLE-INVENTED` keeps the DEL-09-11 hand-over the source has now dropped. The packet does not rely on that hand-over (it has no receipts), so no derived value changes. O-F re-pins deliberately in its next DEL-11 unit.

---

# Addendum 6 — RP-v0.4 (unit EU-F2, with DEL-11-01 CA-v0.1; committed `f324107696`), 2026-10-04

- **Subject.** Re-hashed, all as in `O-F.md` "EU-F2 — frozen":
  - `REPLACEMENT_PACKET.md` `5bfa9303…8271`;
  - `rp.packet-manifest.schema.json` `9c80b95d…`;
  - `F/rplib.py` `c834e90b…`, `build_fx_rp1.py` `93545c62…`, `check_rp.py` `a0ae9335…`, `README.md` `15e04565…`;
  - `F/vendor/VENDOR.json` `982b7bb9…`;
  - FX-RP1-4 `MANIFEST.sha256` `ff30d234…` (all 11 files `OK`).

  `git status --ignored` is clean.
- **Checks.**
  - `check_rp.py`: **70/70**, with no drift NOTICE.
  - CA's side, in RV3-CA1: `check_ca.py` 21/21.

## Verdict on RP-v0.4: **READY**

My three MINOR findings from Addendum 4 and N9 are resolved, each with one qualification below. O-F's fixes for RR-EUF3 hold, and DEL-11-01's hand-over feeds the packet correctly. There is 1 new MINOR finding (EUF4-R1), which partly reopens Addendum 4's finding 1.

| Addendum 4 item | At RP-v0.4 | Checked |
|---|---|---|
| MINOR 1: no rule kept a placeholder candidate from the owner | **Resolved in form.** `check_package` refuses an illustrative or unidentified candidate outside a fixture (B-45). A fixture's purpose must open with "FIXTURE, NOT FOR THE OWNER: no real candidate is identified" (A-20; FX-RP1-4's purpose does). B-47 is the positive control. See EUF4-R1 for what the rule rests on | `rplib.py` l.385–392 |
| MINOR 2: "manual" and "on request" | **Resolved.** "After that act, inference from App v3's records (BUILD_AND_RELEASE.md §12, excerpted in the packet): v3.0.x's manual update check reads the latest published stable release, so on request it would open v4's installer or release page". This is faithful to the excerpt ("Manual checks read its latest published stable release … opens in the system browser on request"). RP-R6 refuses a BUILD_AND_RELEASE inference missing either word (B-46) | Package and excerpt text |
| MINOR 3: false "are excerpted" | **Resolved.** The term now reads "Every DEL-11-03 clause this entry names is excerpted"; CLM-001, CLM-003, REQ-004, REQ-005, REQ-006, VER-003, VER-004 and AX-001 are all in `basis-excerpts.md`. I checked all **12** excerpt blocks byte-exact at their stated lines and sha256. The two R23 excerpts are pinned to an earlier committed blob, which is sound because R23 is append-only | Script over `basis-excerpts.md` and git blobs |
| N9: DOS examples moved | **Resolved.** `F/vendor` re-pins `lhq.dossier-manifest.valid.examples.json` to `dbf8463f…` (source commit `aa95aff4e1`, DX-3). FX-RP1-4's `DOS-EXAMPLE-INVENTED` has no DEL-09-11 hand-over and carries the DX-3 limitation | Vendor record; fixture copy |

## O-F's fixes for RR-EUF3 (§3, §4, §5)

- **#3 Host contributions.** `journey.host_contributions` reads `{"by_standing": {"answered": 13}, "committed_delivered_adopted_or_examined": 0}`. That equals the CIR copy's 13 external contributions, all `answered`.
- **#4 Review.** `dossier_review` now carries `dossier_states_independent: true` beside `state: named_not_resolved`. That matches SQ-EX-05's `reported_as_independent: true`, with the review not supplied.
- **#5 Baseline.** `comparison_rule` adds "so no direct measurement of v3.0.1 exists".
- **#6, #7.** As in the table above.
- **#8.** O-F routes it to O-B as a note, with no packet change, which matches my Addendum 4 judgment.

## DEL-11-01's hand-over feeds RP-v0.4 correctly

- S-4 is `supplied/continuity-handoff.CA-1.json` (`850e0421…`), `source_kind: copied_record`, `standing: owner_record`.
- It is byte-identical (`cmp`) to `F/ca/records/CA-1.handoff.json`.
- The packet's `continuity` repeats the hand-over's results: `archives_verify: passed`, `thesis_identity: matches`, `continuing_obligations: not_supplied`, `fallback_retained: true`, account "CA-1 v1". A-21 checks this.
- The first-cut `continuity_input` is gone. The interface is checked from both ends (`check_ca` K-11; `check_rp` A-7, A-8, A-21).

## EUF4-R1 — MINOR — the fixture refusal rests on two fields the builder writes rather than derives (`rplib.check_package`; `build_fx_rp1.py`)

- **Evidence.**
  - `check_package` treats a packet as illustrative when `manifest["evidence_standing"] == "illustrative" or not manifest["candidate"]["identified"]`.
  - In `build_fx_rp1.py`, both are written as constants (`"evidence_standing": "illustrative"`; `"identified": False`). Nothing in `check_rp` recomputes them from the supplied items, even though the items carry their own standing (S-1…S-3 `illustrative`) and the subject still reads "ILLUSTRATIVE (SQ example; not a real candidate)".
  - My probe took FX-RP1-4's own package with the fixture notice removed, and its manifest with `fixture: false`, `evidence_standing: "established"` and `identified: true`. `check_package` returned **no error**, although the subject is still the placeholder.
- **Consequence.** The refusal protects against an honest builder forgetting the notice, not against a packet that misstates its standing. REQ-004's "identify the exact … candidate" is enforced only by declaration.
- **Repair.**
  - Derive `evidence_standing` from the supplied items: illustrative if any supplied item is illustrative or a first cut.
  - Derive `identified` from the candidate evidence: for example, the SQ candidate maps, its step results resolve to candidate EXP records, and the subject carries no placeholder marker.
  - Check both in A-9's recomputation.
  - Also make `check_disposition` refuse `presented_no_decision` or `decided` for a packet whose manifest is a fixture.

## Not run

- The builders' determinism.
- `--fixture` on FX-RP1…3 (O-F reports 8/22, 11/22 and 13/22, as expected under the current rules).

---

# Addendum 7 — RP-v0.5 (unit EU-F3; committed `b2fbfdbac8`), 2026-10-04

- **Subject.** Re-hashed:
  - `REPLACEMENT_PACKET.md` `f928cd02…7644`;
  - schema `90629f17…`;
  - `F/rplib.py` `52e64564…`, `check_rp.py` `71987a46…`, `build_fx_rp1.py` `0754e56b…`;
  - FX-RP1-5 `MANIFEST.sha256` `c8a267ff…`.
- **Checks.** `check_rp.py`: **76/76**.

## Verdict on RP-v0.5: **READY**

**EUF4-R1 is confirmed resolved.**

- **My probe** (Addendum 6), rerun unchanged against RP-v0.5, is FX-RP1-5's package with the fixture notice removed, and a manifest declaring `fixture: false`, `evidence_standing: "established"` and `identified: true`. It is now refused three ways:
  1. "the manifest's declared standing or identification disagrees with what its supplied items and subject derive (EUF4-R1)";
  2. the illustrative-candidate refusal;
  3. the missing fixture notice.
- **Derivation.** `derive_standing` derives `identified` from a mapped subject with no placeholder marker and no unresolved steps, and `evidence_standing` from the supplied items' standings. A-9 recomputes them.
- **Presentation.** `check_disposition` refuses `presented_no_decision` for a fixture package: "RP-R7: a fixture package is never presented or decided (EUF4-R1)". I tested this myself; it corresponds to B-51/B-52.
- **Limit (NOTE).** `PLACEHOLDER_RE` is keyword-based (`illustrative|invented|example|placeholder`). The other derivation conditions still hold any illustrative fixture (see RV3-AA1 N3).

**DEL-11-02's hand-over.** S-6 `supplied/adoption-status.AA-1.json` is byte-identical (`cmp`) to `F/aa/records/AA-1.status.json`, and `adoption.status` is `supplied`. RV3-AA1 AA1-R2's wording point ("received" should read "delivered") applies to the repeated statement. RV3-AA1 N2 ("owner_record" undefined) applies to S-4 and S-6.

---

# Addendum 8 — RP-v0.6 (EU-F3R, `0e0036b685`), 2026-10-04: **READY**

- **Checks.** `REPLACEMENT_PACKET.md` `71eb2881…`; schema `5b2a4b2a…`; FX-RP1-6 `19050b12…`; `check_rp.py` **99/99**.
- **Scope.** FX-RP1-6 differs from FX-RP1-5 only by:
  - AA1-R2's wording in S-6;
  - the `owner_record` → `deliverable_record` rename and its new term;
  - the CA-1 v3 and AA-1 v2 hand-overs, with the version, id and hash consequences.

  §3 adds my N3 keyword limit; §8 and C-1…C-21 are the coordinator's audit (RV3-AA1 addendum §3).
- **EUF4-R1** stays resolved: my Addendum 6 probe remains refused (shown in Addendum 7).
