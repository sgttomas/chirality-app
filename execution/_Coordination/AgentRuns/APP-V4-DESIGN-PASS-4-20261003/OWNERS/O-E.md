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

## Drafts held unfrozen behind EB-v0.2's review (2026-10-04)

| Unit | File | sha256 at writing | Content |
|---|---|---|---|
| DEL-10-02 UC-v0.1 | `DEL-10-02_…/Design/UNDERTAKING_CONTROLS.md` | `2db908e7aef70d85d9fbe981fe0fe9677c3748655e2a111530c124126cef2f25` | As above |
| DEL-10-04 DA-v0.1 | `DEL-10-04_…/Design/DAG_ACCOUNT.md` | `7b8c8aba79cd896e07f5382393201803e436acbbf48faece94efa9662813d8ee` | Evidence account over DAG-001…004: versions with owner words, recorders, counts and reviews; obligation-to-evidence map for REQ-001…009; currency procedure (§5); consumers; SCC-CASE-006 (R1) |
| DEL-10-03 RA-v0.1 | `DEL-10-03_…/Design/RESPONSIBILITY_ACCOUNT.md` | `6a6ff98b9d71ed31e08bd949b04a707470da8ff76552481a7637ce495caff850` | §1 population bound complete (R23-31.7): 9 supplier entries (S-1…S-9), 5 cross-project or open-allocation entries (X-1…X-5), exclusions with reasons, cycle guard. §2–§5 outlined |

**Checks run for DA-v0.1 (by O-E, read-only):**
- each version's `MANIFEST.sha256` passes `shasum -c` (61, 37, 37 and 37
  entries);
- `audit_dag.py --canonical --strict` (`830d0d53…`) exits 0 on DAG-001…004,
  with 109, 124, 124 and 129 admitted edges and 0 SCCs; output went to scratch
  only;
- CSV record counts equal each handoff's stated counts;
- DAG-004's `SOURCE_MANIFEST` is 128 of 130 OK from `E/`; the 2 failures are
  the recorded DEL-01-03 drift.

**Pending for EB-v0.3 (applied after RV3 returns on v0.2):**
- the RV3-EB1 residuals above;
- R23-38.5's observation in EB §3.3 item 5: no retroactive bindings; every
  method the first increment and passes 2–3 used is byte-identical then and
  now, checked by O-E with Git.

**Request to O-A (for later, under R23-21, when RA §2 maps it; R23-31.10):**
fill ACT-POLICY's consumer row "DEL-10-03 … Not mapped in detail". Not yet
sent; RA §2 comes first.

## Brief received, 2026-10-04 (G-1)

- **From HELP_HUMAN.** RV3 found EB-v0.2 READY (addendum).
- **EB-v0.3:** carries EB2-R1 (LOOP_INIT's decision record, as R23-42.1
  states it) and EB2-R2 (R23-38.5), together with the planned residuals
  (R6–R9, R12, R13). It is made with the next freeze, not as a separate
  round.
- **EB-v0.2:** committed at `d43665498d`.
- **Next:** continue with DEL-10-02 and DEL-10-04.

## Freeze — UC-v0.1 with EB-v0.3, for RV3 (2026-10-04)

**Paths for HELP_HUMAN's path-limited commit (R23-41).** All under
`projects/chirality-app-v4/execution/PKG-10_Project definition and manual-led practice/1_Working/`:

| Path | sha256 |
|---|---|
| `DEL-10-01_Project execution basis and manual application/Design/EXECUTION_BASIS.md` (EB-v0.3) | `e9f7e9a6100f805d1bfd992bc681056d3ef68b21c203750d69b1a3def6f904ee` |
| `…/DEL-10-01_…/Design/eb1/EB1_COMPARISON.md` (§6 dated corrections appended) | `af3f2d6c91ba6872d0ddff39266f1a092790c8bb1c239e5826edb3d93023c216` |
| `…/DEL-10-01_…/Design/prototype/eb1_check.py` (P-3 widened to 9 hashes) | `712c6f8f4c5f9556939faa9faab6f83a232575fb308eba569891bd46bb829bff` |
| `DEL-10-02_Proportionate undertaking controls and practice feedback/Design/UNDERTAKING_CONTROLS.md` (UC-v0.1, new) | `e25fbe9b79376863951912fc7e7b20a201568cd591938eca6a20117574ce337f` |

The other EB files are unchanged and committed:
- the key `0ef83844…`;
- the brief `3a9d2529…`;
- the manifest `907709e5…`;
- `make_input_set.py` `165dd43c…`.

**Not in this freeze (drafts, keep out of the commit).** DEL-10-03
`Design/RESPONSIBILITY_ACCOUNT.md` and DEL-10-04 `Design/DAG_ACCOUNT.md`.

**R23-44 check.** Every input `eb1_check.py` reads is tracked and clean in
git:
- the RRM schema (DEL-09-11);
- `BASIS_BINDING.md` and `CURRENT_EXECUTION_BASIS.md`;
- `RR-EB1/SUPPLIED.sha256`;
- the manifest and all 44 of its items.

UC-v0.1 has no executable check of its own.

**PN-1 applied (re-read before freeze).** I re-hashed every record the two
units rely on.
- **Changed since my last read, then re-read:**
  - `R23_RESOLUTIONS.md` (`31c2261d…`): R23-39…R23-44 read; R23-41, 42 and 44
    bear on this freeze and are applied;
  - `reviews/RV3-EB1.md` (`bc3add0d…`): addendum read in full;
  - `DISPATCH.md` (`984a093f…`): tail read.
- **Unchanged since my reads:**
  - `OWNER_DECISIONS.md` `e4350f61…`, `OWNER_DECISIONS_2.md` `3a861c52…`;
  - `BASIS_BINDING.md` `93160e1d…`, `CURRENT_EXECUTION_BASIS.md` `99d08009…`;
  - `RECEIPT.md` `a45055e2…`, `BRIEFS.md` `53f8d877…`;
  - pass-4 `WORK_GRAPH.md` `34b2e489…`.

**Claims.**
1. **EB-v0.3** repairs every RV3 residual its plan assigned (R6–R9, R12,
   R13, R14) and EB2-R1/R2. It lists each in "Changes". B-19 states exactly
   what the LOOP-ENTRY manifest records, and what no record states.
2. **The comparison's D-5 trace is corrected by a dated §6.** KF-5…KF-7 are
   recorded as key findings with no score effect. The key is unchanged.
3. **UC-v0.1** meets OUT-001…003 as conventions over existing records:
   - the controls map;
   - the G-1 brief convention;
   - the capability and check account form, with the pass-4 instance;
   - the practice-note convention and PN-1…PN-8;
   - the stage-disposition package;
   - DAG use;
   - DEL-09-12 receiving.

   It creates no register and writes no coordination record. Proposals
   P-E4…P-E6 are HELP_HUMAN's to take.

**Checks run.**
- `eb1_check.py --post-dispatch RUN/RR-EB1/SUPPLIED.sha256`: **PASS 125,
  FAIL 0.** That is 119 as before plus 6 from the P-3 widening. Expected
  drift since the read: the account and R23. In default mode, M-2 reports
  that drift, by design.
- `check_boundary_owner_resolution.py` (`22ef57e0…`) on all four PKG-10 SoWs:
  1 boundary requirement checked each, 0 failing, 0 citing no claim.
- UC VER-001 walk of the pass-4 graph:
  - structure holds;
  - the current position is stale (PN-8).
- UC VER-002, VER-003 and VER-006 (manual-locus check) are done; see UC §10.

**Open.**
- UC VER-005 (after RV3's return).
- UC VER-007 (stage discussion).
- EB VER-005, VER-007 and O-E's own VER-004 record (M §1.7, U §5).
- RA §2–§5 and DA §4/§7: drafts, next units.

## Brief received, 2026-10-04 (labelled transcription; the brief as sent is `BRIEFS_AS_SENT.md` entry 100, R23-46)

- **EB-v0.3:** READY. Next touch carries N-a (§8 wording) and N-b (B-19's
  writer).
- **UC-v0.1:** REPAIR per RV3-UC1:
  - UC1-R1 → R23-46: G-1 restated; VER-002's second case partial;
  - UC1-R2: branch, with R23-47's wording;
  - UC1-R3: class vs applied; SPEC §9.8 for PN-8;
  - UC1-R4: PN-1 loci;
  - notes: §5/§11 PRACTICE_NOTES, §7 range, PN-9.
- **Folding:** all of it goes into the next freeze, with DEL-10-03 or
  DEL-10-04.

## Freeze — DA-v0.1 + UC-v0.2 + EB-v0.4, for RV3 (2026-10-04)

**Paths for the path-limited commit (R23-41, R23-44, R23-48).** All under
`projects/chirality-app-v4/execution/PKG-10_Project definition and manual-led practice/1_Working/`:

| Path | sha256 |
|---|---|
| `DEL-10-04_Project production dependency DAG/Design/DAG_ACCOUNT.md` (DA-v0.1, new) | `611adec3d58bfa6a2789090ff3cb15dd08b9d82619525d036b1292ce0a1aa29d` |
| `DEL-10-02_Proportionate undertaking controls and practice feedback/Design/UNDERTAKING_CONTROLS.md` (UC-v0.2) | `da0176cbf2ae806dc1c4e98b9fbd8bb7af635639c7cac4e114b7da42d0d8b533` |
| `DEL-10-01_Project execution basis and manual application/Design/EXECUTION_BASIS.md` (EB-v0.4) | `b12c55c7b585aa0b1720b0a2426693627c9439eecad5856f74acbe1d74277392` |

**Not in this freeze:** `DEL-10-03_…/Design/RESPONSIBILITY_ACCOUNT.md`, a
draft; keep it out of the commit.

**Commit-readiness checks.**
- `git status --short --ignored` on the PKG-10 paths shows no ignored file
  (R23-48).
- No executable check is new in this unit. EB's checker and its inputs are
  unchanged and committed.

**PN-1 applied before freeze.** I re-hashed the records relied on.
- **Changed, then re-read:**
  - R23 (`aa281119…`): R23-45…R23-48; only R23-48's ignored-path check
    bears on this freeze;
  - DISPATCH (`757b781d…`): its tail and capability section (R23-47
    wording);
  - BRIEFS_AS_SENT (`159eb64f…`): structure and O-E's entries;
  - RV3-EB1 (`d187914a…`): addendum 2;
  - RV3-UC1 (`071f142f…`): read in full.
- **Unchanged:** `OWNER_DECISIONS.md` `e4350f61…`, `OWNER_DECISIONS_2.md`
  `3a861c52…`, `BASIS_BINDING.md` `93160e1d…`.

**Claims.**
1. **DA-v0.1** maps OUT-001/002 and REQ-001…009 onto DAG-001…004, their
   checkpoint packages, closure and currency records, and the seven cases.
   It sets the currency procedure for the rest of the pass, keeping
   successor acceptance reserved to the person. It writes nothing under
   `_DAG/` or `_Evaluation/`.
2. **UC-v0.2** repairs UC1-R1…R4 and N1–N4 under R23-46/47 and adds PN-9.
   Each repair is listed in its "Changes".
3. **EB-v0.4** carries addendum 2's N-a and N-b, nothing else.

**Checks run.**
- **DA:**
  - each `MANIFEST.sha256` (DAG-001…004) passes `shasum -c`;
  - `audit_dag.py --canonical --strict` (`830d0d53…`) exits 0 on all four
    (109, 124, 124 and 129 admitted edges; 0 SCCs), output to scratch only;
  - CSV record counts equal the handoffs;
  - DAG-004 `SOURCE_MANIFEST` is 128 of 130 from `E/`, the two failures
    being the recorded DEL-01-03 drift;
  - each successor's `CHECKPOINT_C.md` hash equals its acceptance record's
    "Package presented";
  - frozen vs current `External_Dependencies.csv`, field by field: only
    DEP-002 changed;
  - each case's `Ruling_Register.csv` holds CP1-20260928 only;
  - `check_boundary_owner_resolution.py` gives 1 checked, 0 failing.
- **UC:** each changed quotation (PN-1, PN-8, PN-9 loci) was re-checked
  against F §5.4, M §5.4, SPEC §9.8 and U §10.

**Findings for HELP_HUMAN in DA §8 (records only; no edit by O-E):**
- CASE-002's drafted evidence update for DAG-004 is not yet applied: last
  committed change `b547125dbe` (2026-09-29), with the proposal still in
  SCA003's `DAG_PREP/`.
- DEP-005's row text predates D4 and R23-22; its owner updates it at the
  next amendment.

**Open.**
- UC VER-002 unit-brief case, against `BRIEFS_AS_SENT.md`.
- UC VER-005; VER-007 at the stage discussion.
- DA §5 step 2 at the pass closeout.
- RA §2–§5 (DEL-10-03), next unit.

## Brief received, 2026-10-04 (labelled transcription; the brief as sent is in `BRIEFS_AS_SENT.md`)

- **Committed:** DA-v0.1, UC-v0.2 and EB-v0.4 at `68f83d6b20`, queued for
  RV3. The CASE-002 update and DEP-005's text are HELP_HUMAN's (closeout
  list; next amendment).
- **Next:** RA §2–§5, bounded by R23-31.7. When the map exists, send the
  ACT-POLICY row request to O-A through HELP_HUMAN. Freeze when ready.

## Request to O-A, through HELP_HUMAN (R23-31.10; RA §2.3)

To O-A, owner of DEL-04-01. ACT-POLICY-v0.10 §10.3, "Receivers by register
row", has the row:

| DEL-10-03 | DEP-10-03-013 | none | Not mapped in detail |

DEL-10-03 RA-v0.1 now consumes ACT under entry S-6:
- §2.1, the act list with decision actor, subject and evidence;
- §3, the settled distinctions S1–S12;
- §8, the policy representation (DECISION-1's reserved acts in §8.2, the
  values still open in §8.4).

That is the mapping, offered for your wording. Make the row under R23-21,
with a version label if your practice requires one. RA cites ACT by
section, not by version line.

Separately, for your information: ACT is one of three suppliers whose
ScopeOfWork names no DEL-10-03 receiver and whose register holds no mirror
row (RA §3.4, F-RA1). That goes to the next amendment and is not yours to
fix now.

## Freeze — DEL-10-03 RA-v0.1, for RV3 (2026-10-04)

**Paths for the path-limited commit.** Under
`projects/chirality-app-v4/execution/PKG-10_Project definition and manual-led practice/1_Working/DEL-10-03_Shared commitments and consumer responsibility account/`:

| Path | sha256 |
|---|---|
| `Design/RESPONSIBILITY_ACCOUNT.md` (RA-v0.1) | `531b65b7b63f2e705ad6eb033dfe52ce3812ddf5879dff3af74b0cef122d8934` |
| `Design/prototype/ra_check.py` | `ccbab0b3ebcffa2ee4329b204fadc3abc82207b33ae6d2b76821e18d8a159269` |

**Commit-readiness (R23-41, R23-44, R23-48).**
- `git status --ignored` shows nothing ignored under DEL-10-03.
- Everything `ra_check.py` reads is tracked and clean: the nine supplier
  Design files and ScopeOfWorks, and every `Dependencies.csv`.

**Claims.**
1. **§1, the population bound (R23-31.7):** 9 supplier entries and 5
   cross-project or open-allocation entries, with exclusions.
2. **§2, the map:** the 14 entries by class, App v4 owner, host part,
   consumers, open allocation and confirmation state. Each indexes its
   supplier section and restates none (SQ-E2). No common implementation is
   named.
3. **§3, two-way trace.**
   - Each entry goes to its supplier SoW clause and mirror row (checked).
   - The reverse scan finds nothing outside the bound.
   - Seed V4-ARC-20's five shared-layer items all have v4 owners, so the
     relocation lost no promise.
   - Finding **F-RA1:** DEL-04-01, 05-01 and 05-02 supply DEL-10-03 on
     admitted arcs, but their SoWs and registers do not record the
     receiver. These would be SAME_ARC mirrors (no SCC). They go to the
     next amendment; no row is added.
4. **§4.**
   - Historical applicability H-1…H-3, quoting the seed and current text,
     with seed hashes checked.
   - Consumer, packaging and tool-path account, static only: App v3
     (historical), App v4 P-2/P-3 (proposed), Root, Runtime, Piping and PEC,
     each with its outstanding check and point of need.
5. **Owner boundary.** No adoption is performed or claimed. No register or
   ScopeOfWork is written.

**Checks run.**
- `ra_check.py`: **PASS 31, FAIL 0** (H-1 ×9, P-1, R-1 ×9, R-2 ×9, F-1 ×3).
- `ra_check.py --self-test`: H-1, P-1, R-1, R-2 and F-1 each **detected** a
  mutation.
- `check_boundary_owner_resolution.py` on DEL-10-03's SoW: 1 checked, 0
  failing.
- Ledger dispositions for SC2-02-01-2, SC2-04-03-1 and SC3-02-04-9: all
  INCLUDE.

**PN-1, re-read before freeze.**
- Re-read because they changed: R23 (`0f79ed06…`, R23-49, not bearing on
  RA) and DISPATCH (`dc6855b4…`).
- Unchanged: `OWNER_DECISIONS_2.md` `3a861c52…`.
- No supplier Design file has uncommitted changes.

**Open.**
- F-RA1: next amendment.
- ACT's consumer row: O-A, on request.
- Build and runtime checks for P-2/P-3: at the first package (DEL-01-06).
- WD U-17 confirmations: deliverable owners (R23-31.8).

## Freeze — DEL-10-04 DA-v0.2, for RV3 confirmation (2026-10-04)

**Brief (labelled transcription; as sent in `BRIEFS_AS_SENT.md`).**
- RV3 found DA-v0.1, UC-v0.2 and EB-v0.4 READY.
- Fix DA1-R1 (cycle test in arc terms) and DA1-R2 (recommended treatments
  for all cases) while RV3 holds RA.
- Freeze and report for a by-path commit.

**Paths.** Under
`projects/chirality-app-v4/execution/PKG-10_Project definition and manual-led practice/1_Working/DEL-10-04_Project production dependency DAG/`:

| Path | sha256 |
|---|---|
| `Design/DAG_ACCOUNT.md` (DA-v0.2) | `738f8287e31240102ce627280e5108f8ca3a23b261fb8e37ba92c421d16f13b4` |
| `Design/prototype/dag_reach.py` (new) | `42e8b0e6daa60bef3a9d503eeec96b8135efcaffd5bf7123f92fe0a6be3b98f6` |

**Commit-readiness.**
- `git status --ignored` shows nothing ignored under DEL-10-04.
- `dag_reach.py` reads only the committed `_DAG/_LATEST.md` and DAG-004's
  edge CSVs (R23-44).

**Claims.**
- **§5 step 1 (DA1-R1)** states the test in arc terms: a proposed C → S
  forms a cycle exactly when S already reaches C over both layers. It names
  `prototype/dag_reach.py`.
- **§7 (DA1-R2, N1)** quotes each case's recommended treatment from its
  datasheet:
  - R1 for cases 001, 003, 005, 006 and 007;
  - R-01/R-03 for 002;
  - R004-A for 004.

  All are unruled; CP1 is the only ruling recorded. The datasheet is named
  as the source of the state.

**Checks run.**
- `dag_reach.py --self-test` on DAG-004: 212 arcs over both layers (129
  admitted + 83 held). All 5 cases are as expected:
  - DEL-02-04 → DEL-10-03: SCC-forming;
  - DEL-06-01 → DEL-10-02: no cycle;
  - DEL-10-03 → DEL-02-04: existing arc;
  - self-arc: cycle;
  - DEL-10-01 → DEL-10-04: SCC-forming.
- The five case quotations were checked against each `Case_Datasheet.md`
  and against R23-32 F-R8.

**Open.**
- PKG-10 waits on RV3's confirmation of RA-v0.1 and of this DA-v0.2 repair.
- The pass closeout: DA §5 step 2 currency; the CASE-002 update and DEP-005
  are HELP_HUMAN's.
