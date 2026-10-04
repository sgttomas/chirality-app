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
