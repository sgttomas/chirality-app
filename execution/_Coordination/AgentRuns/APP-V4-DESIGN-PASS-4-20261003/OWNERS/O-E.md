# O-E — owner of DEL-10-01…DEL-10-04 (PKG-10)

Standing owner (Type 2 TASK, Claude Opus 5.5), run
`APP-V4-DESIGN-PASS-4-20261003`, tranche 2. Survey: `SURVEY/S2-E.md`. Rulings:
R23-31 (all survey items ruled as proposed). Write area:
- new files under each PKG-10 deliverable's `Design/`;
- this file.

No coordination record, ScopeOfWork, register, `_STATUS`, `_DAG` or
scope-change file is written by O-E.

## EB-1 — frozen for review, 2026-10-04

**Unit.** DEL-10-01 `Design/` (paths below are relative to
`projects/chirality-app-v4/execution/PKG-10_Project definition and manual-led practice/1_Working/DEL-10-01_Project execution basis and manual application/Design/`):

| File | sha256 | Role |
|---|---|---|
| `EXECUTION_BASIS.md` | `e24101b210b9ef16347d9747169034b19b1f1ef5971e7cc31039b97cbc013baa` | The account (EB-v0.1): basis chain §2, pins §3, handoff §4, positions §5, application and departures §6 |
| `eb1/IS-EB1-1.input-set.json` | `907709e54c77bb033ae4f8cceb1a5a28f856735cdec7f759a08b2849f4c761a8` | Input set: RRM-v0.1 format, DEL-09-11's schema unchanged; 44 items; 7 withheld identities |
| `eb1/EB1_READER_BRIEF.md` | `3a9d25299150de8eb992b2ee8a0396c412d778715bc44af7dbe1f421876491e5` | For the reader: rules, questions Q1–Q8, return format |
| `eb1/EB1_QUESTION_KEY.md` | `0ef838449736e0442761309968c53c2e1aee661001e3088724f56df63d2e1f23` | **Examiner only. Frozen before any reader runs.** 45 key items, 23 critical, with scoring and the pass rule |
| `prototype/make_input_set.py` | `165dd43c06575fe589173fab8fe89f216097ebb47cb3c8e42a22006886c39246` | Builds the manifest |
| `prototype/eb1_check.py` | `2845775a1e73041a6e1bbfadaf933fc2e86b52a7a20f250d9119ffc0b3779165` | Pin, manifest and copy checks |

**Claims.**
1. Every sha256 in §3 equals today's bytes. The nine definition-run pins and
   four of the five later-selected methods also equal their bytes at
   `ffb2b628…`, the commit CURRENT_EXECUTION_BASIS names.
   `coordinated-knowledge-work` is absent there, and OWNER_DECISIONS.md
   recorded it with its hash. No pin has drifted.
2. Each row of the basis chain (§2) states only what its record states.
   Where a record does not name its writer (Group3, setup), the row says so.
3. §2.1 separates acts that are not the owner's: the R23 rulings, lifecycle
   moves, App v4's D-GOV-52 adoption, and the review-independence
   observation.
4. §6 finds no departure that awaits the owner.

**Checks run.**
- `python3 prototype/eb1_check.py`: **PASS 94, FAIL 0**. That covers 14 pins
  (P-1 today, P-2 at `ffb2b628`), the three manual hashes found verbatim in
  CURRENT_EXECUTION_BASIS (P-3), the manifest valid against
  `rrm.input-set-manifest.schema.json` with jsonschema 4.26 (M-1), all 44
  item hashes (M-2), the key and survey not supplied (M-3), and every pin
  path supplied (M-4).
- **Negative cases**, to test the checker itself (tranche-1 lesson). Each
  fails as intended:
  - a changed item hash → M-2;
  - an extra key and a bad standing → M-1;
  - the key added as an item → M-3;
  - an empty copy folder → V-1, 44 failures;
  - a changed pin in the account text → detected by `pin_rows`.
- Key facts were rechecked against the records by quoting them (each key
  row names its primary record).

**Open (not claimed).**
- VER-004 and VER-005: the per-row comparison with Consolidated §1.7 and
  User Manual §5. VER-007 and VER-008 are also not run.
- The approval record for LOOP_INIT's v4 text (`afc65e2b22`) was not
  located.

### For the dispatcher (HELP_HUMAN)

1. **Copy at the manifest's hashes, then verify.** Copy the 44 items into a
   scratch folder, keeping the repository-relative paths, together with
   `IS-EB1-1.input-set.json` and `EB1_READER_BRIEF.md`. Then run
   `python3 prototype/eb1_check.py --verify-dir <folder>` (V-1). Do **not**
   supply `EB1_QUESTION_KEY.md`, `SURVEY/S2-E.md` or this file.
2. **The manifest includes working bytes that may change.** Four items are
   uncommitted working bytes: `OWNER_DECISIONS_2.md`, `R23_RESOLUTIONS.md`,
   the pass-4 `WORK_GRAPH.md` and the account itself. Other owners are
   active, and R23 is append-only but growing. If any of these changes
   before you copy, M-2 fails. Rerun `prototype/make_input_set.py` and tell
   me, so I can confirm the key is unaffected. A new ruling does not
   invalidate the key unless it changes R23-28, 30 or 31.
3. **The reader's return.** Give me its `account.json` and report. I compare
   them with the key. Every miss is traced to the index, to the records or to
   the reader before any repair (key "Scoring").

## Proposals to HELP_HUMAN (coordination records are yours, R23-31.2)

- **P-E1 is withdrawn (2026-10-04).** It asked CURRENT_EXECUTION_BASIS to
  state R23-31.3's rule, which R23-35 has superseded.
  CURRENT_EXECUTION_BASIS's own sentence ("a later undertaking or changed
  source must bind its own applicable basis before reliance") was right. The
  gap was the run's missing binding, now closed by `BASIS_BINDING.md`.
- **P-E2 (optional, low value).** One line under CURRENT_EXECUTION_BASIS
  "Reliance and continuation": "Each undertaking's binding is in its run
  folder, for example `AgentRuns/APP-V4-DESIGN-PASS-4-20261003/BASIS_BINDING.md`
  (R23-35)." It would help a cold reader find bindings. Not needed for
  correctness.
- **P-E3 (your call).** The first increment and design passes 2 and 3 have
  no located basis binding. Every method they named is byte-identical at
  `ffb2b628` and today, which O-E checked. Whether to record that
  retroactively is open in EB-v0.2 §9.

## Next

- **DEL-10-03 population bound** (R23-31.7) proceeds in parallel while EB-1
  waits for review.
- **DEL-10-02 and DEL-10-04** wait until EB-1 passes.

## EB-1 result — RR-EB1 scored, 2026-10-04

Comparison: DEL-10-01 `Design/eb1/EB1_COMPARISON.md` (sha256
`fa8e7aeec0c122234b2425ea82ddf0edcf126b8edd50319098db1f3bf71310d1`). Reader
account `RUN/RR-EB1/account.json` `018ebe7b…`. The supplied set equals the
frozen manifest; the reader's RD-0 found 0 mismatches. Key unchanged
(`0ef83844…`).

**Score (45 items, 23 critical).**

| Reading | Critical | Non-critical | CONTRADICTED | Rule |
|---|---|---|---|---|
| Literal, against the frozen key | 22/23 MATCH; K7.d diverges | 21/22 MATCH; K3.3 MISS | 0 | Fails on one critical item |
| Adjudicated (divergences decided by the supplied records) | 23/23 | 21/22 (95%) | 0 | Meets the pass rule |

**Critical misses: one, K7.d, and it is a key error.** The supplied
`OWNER_DECISIONS_2.md` holds the owner's act "Same-session review is
acceptable. …". The reader reported it correctly; my key and my account
missed it. Whether EB-1 counts as passed is yours to decide.

**Tracing.**

| Item | Traced to |
|---|---|
| Account defects | D-1 (no row for the owner act), D-2 (selection merged with recording), D-3 (followed R23-31.3), D-4 (four omissions and an unsupplied citation), D-5 (Git checks presented as record facts) |
| Records | The run's missing basis binding (D-3), closed by `BASIS_BINDING.md` under R23-35. No owner decision record for LOOP_INIT's v4 text (D-5) |
| Reader | No fault found. All seven `unknown`s are correct |
| Key findings | KF-1 (K1.3 states the superseded R23-31.3), KF-2 (K7.d), KF-3 (K3.3 was never asked), KF-4 (K1.2 scope-phrase attribution, minor) |

**Root cause (practice observation PN-1, for DEL-10-02).** I hashed the
working bytes at freeze but wrote the account and the key from earlier
reads, so the hashed bytes carried content I had not read. A hash check
does not detect a stale reading. At freeze, re-read the changed sections of
every supplied record that the key or index relies on.

**Practice observation PN-2 (for DEL-10-02, the 60% discussion).** No
undertaking's start step currently produces a basis binding. Pass 4 lacked
one until RR-EB1 found the gap. Making it a loop step would change LOOP_INIT,
a project instruction, so it is noted here, not proposed.

## EB-1 refrozen for RV3 — EB-v0.2, 2026-10-04

| File | sha256 |
|---|---|
| `EXECUTION_BASIS.md` (EB-v0.2) | `f9b8911f027880a72ca08149a42b19c4dc814c35cac7153f64db6cd8778cd61f` |
| `eb1/EB1_COMPARISON.md` | `fa8e7aeec0c122234b2425ea82ddf0edcf126b8edd50319098db1f3bf71310d1` |
| `eb1/EB1_QUESTION_KEY.md` (unchanged) | `0ef838449736e0442761309968c53c2e1aee661001e3088724f56df63d2e1f23` |
| `eb1/EB1_READER_BRIEF.md` (unchanged) | `3a9d25299150de8eb992b2ee8a0396c412d778715bc44af7dbe1f421876491e5` |
| `eb1/IS-EB1-1.input-set.json` (unchanged; the record of what was read) | `907709e54c77bb033ae4f8cceb1a5a28f856735cdec7f759a08b2849f4c761a8` |
| `prototype/eb1_check.py` (P-4 and `--post-dispatch` added) | `54ec042d3a4bee53c82e2f2e376f46ee88f794e968400015741721febed7b3ee` |
| `prototype/make_input_set.py` (unchanged) | `165dd43c06575fe589173fab8fe89f216097ebb47cb3c8e42a22006886c39246` |

**Claims.** EB-v0.2 repairs D-1…D-5, indexes R23-35 and `BASIS_BINDING.md`
(`93160e1d…`), and lists every repair with its cause in "Changes". The
frozen key is unchanged; its errors are recorded as findings.

**Checks run.**
- `eb1_check.py --post-dispatch RUN/RR-EB1/SUPPLIED.sha256`: **PASS 119,
  FAIL 0.**
  - P-1/P-2: 14 pins.
  - P-3: manual hashes in CURRENT_EXECUTION_BASIS.
  - P-4: BASIS_BINDING's 11 rows equal today's bytes and §3.
  - M-1: the manifest is schema-valid.
  - D-1: the supplied record equals the frozen manifest.
  - Expected drift since the read: the account (this repair) and
    `R23_RESOLUTIONS.md` (R23-35/36 appended).
- The pre-dispatch mode now fails M-2 on those two drifted items, as
  intended.
- Negative cases: a changed BASIS_BINDING hash → P-4; a changed supplied
  hash → D-1.

**Open.**
- VER-004, 005, 007 and 008.
- P-E2 and P-E3.
- A second reader on EB-v0.2: not run, and not proposed unless you want the
  repairs read cold.
- DEL-10-02 and DEL-10-04 stay held pending your decision on EB-1.

## RV3-EB1 (review of EB-v0.1) — disposition plan, 2026-10-04

`reviews/RV3-EB1.md` (`a8772e5a…`) reviews **EB-v0.1** (`e24101b2…`), not
EB-v0.2. Its verdict is REPAIR: 1 BLOCKING, 4 MAJOR, 9 MINOR, 5 NOTE.
EB-v0.2, written from RR-EB1's disagreements before I saw RV3, already
covers most of it.

EB-v0.2 (`f9b8911f…`) is held for RV3. I do not edit it now, so the
subject under review does not move. The residual repairs below are applied
together as EB-v0.3 once RV3 returns on v0.2, unless you want them sooner.

| Finding | State at EB-v0.2 | Residual for EB-v0.3 |
|---|---|---|
| EB1-R1 (BLOCKING, K7.d) | Recorded as KF-2 in `EB1_COMPARISON.md`; the key stays frozen (R23-38.1) | None; RV3's "pre-scoring correction" in the key is not made, per R23-38.1 |
| EB1-R2 (owner act) | B-18; §2.1 and §6 rewritten | None |
| EB1-R3 (selection actor) | §1, §3.1 | None |
| EB1-R4 (K8.2) | — | New key finding KF-5 in the comparison. The reader answered "none recorded … inferred", sourced, so it is MATCH under either reading and the score does not change |
| EB1-R5 (R23-35) | §3.3 rewritten; header | §3.3 item 5 becomes R23-38.5's observation: no retroactive bindings, and the methods are byte-identical (checked by O-E). Add RV3's grep fact: no later undertaking's graph, BRIEFS or DISPATCH cites the pins |
| EB1-R6 (LOOP_INIT approval) | Commit message only | Cite `docs/governance_harness/tranche_manifests/APP-V4-LOOP-ENTRY-20260928.yaml` `m2_gate` (verified): the owner requested the revision, `authorized_by: Ryan`, integration owner Codex HELP_HUMAN `/root`, self-merged under the owner-authorized PR gate. Add the act to §2; close §9 row 2 |
| EB1-R7 ("—" limits) | Partly (B-11, B-12, B-13) | Give one stated limit per row, or define "—" |
| EB1-R8 (B-2, B-6 writer) | — | B-2: "written by WORKING_ITEMS" (`DIRECTION.md`: "WORKING_ITEMS authored this bounded correction", verified). B-6: "record does not name its writer" |
| EB1-R9 (omissions, ordering) | B-12 completed; B-13 download | Add the DAG-001 hold ("DO NOT BEGIN …", "finish your tasks …") to B-7. Move DAG-002 between B-8 and B-9. §5: say which act started work toward 60%, or that it lies outside the indexed records |
| EB1-R10 (selected vs directed) | B-14 corrected | Recheck the §3.2 wording; add key note KF-7 (the work graph says "owner's selection"). No score change: the reader reported both |
| EB1-R11 (optional elements) | — | Key note KF-6 (K3.1 recorder, K4c.2 manifest). No score change: the reader gave both |
| EB1-R12 (§5 DAG timing) | — | "Constructed and examined before the gate; accepted in the act that completed it (B-7)" |
| EB1-R13 (SCA verbatim) | — | Quote "Accept (Recommended)" from the in-set records, after checking them |
| EB1-R14 (R23 range) | v0.2 says R23-1…R23-36 | "R23 rulings (R23-1 onward)" |
| N4 (checker) | — | Extend P-3 to the six method hashes in CURRENT_EXECUTION_BASIS's route table. Keep EB's §3 tables as a checked index (P-1…P-4); they duplicate BASIS_BINDING by design (R23-38.4: EB indexes each undertaking's binding) |
| N1, N2 | P-E1 withdrawn; P-E2 not taken (R23-38.4) | None for O-E. N2 (lifecycle) is HELP_HUMAN's |

**Review-protocol note.** RV3 reviewed a version the reader had already
shown to be wrong. A reviewer and a cold reader running in parallel on the
same frozen bytes find overlapping defects twice. Next time, the reader's
return should go to the reviewer before review starts, or review should
start after scoring. This is noted for DEL-10-02's practice notes (PN-3).

## Brief received, 2026-10-04 (from HELP_HUMAN; recorded under UC-v0.1 G-1, my transcription)

- **Ruling:** R23-38. EB-1 passed as an early path. There is no second cold
  read; RV3 reviews EB-v0.2. P-E1 is withdrawn and P-E2 not taken. P-E3:
  no retroactive bindings, and EB records the byte-identical observation.
- **Work:**
  - DEL-10-02 first: the practice-note convention (R23-31.4), seeded with
    tranche 1's lessons and the stale-reading note, plus the per-run
    capability and check account (R23-31.6);
  - then DEL-10-04's mapping onto DAG-001…004 and their cases;
  - DEL-10-03's population bound continues.
- **Hold:** keep the next unit drafted and unfrozen until RV3 returns on EB.
- **Write grant:** as before (new files in PKG-10 `Design/` folders; this
  file).
- **Escalate only for:**
  - restructuring an earlier Design file;
  - a register row;
  - an owner-reserved item;
  - a weakened check.

## DEL-10-02 UC-v0.1 — drafted, NOT frozen (2026-10-04)

`DEL-10-02_…/Design/UNDERTAKING_CONTROLS.md` covers:
- §2: the controls map against the actual records, with gaps G-1…G-3;
- §3: brief and return conventions checked element by element, and the G-1
  convention;
- §4: the capability and check account form, with a worked pass-4 instance;
- §5–§7: the practice-note convention, seed notes PN-1…PN-7 with manual
  loci, and the stage-disposition package;
- §8: DAG use and SCC-CASE-006;
- §9: DEL-09-12 receiving;
- §10: verification design.

It is held unfrozen until RV3 returns on EB-v0.2.

**Proposals (coordination records are HELP_HUMAN's):**
- P-E4: create `RUN/PRACTICE_NOTES.md` with PN-1…PN-7, linked from the graph;
- P-E5: put UC §4.2's capability account into DISPATCH;
- P-E6: give the next reviewer the reader's scored result first (PN-3).
