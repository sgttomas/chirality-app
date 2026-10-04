# SCA-V4-003 — Decision log

**Standing: CANDIDATE amendment folder (posture `ACCEPTED_PREDECESSOR`);
checkpoint group 3 not yet presented.** Human decisions are quoted exactly;
execution-stage readings by node AK1 are labelled as such and are not owner
decisions. `RUN` = `execution/_Coordination/AgentRuns/APP-V4-SCA003-20261002`.

## Human decisions

| Ref | Date | Checkpoint | Owner's words (exact) | Record |
|---|---|---|---|---|
| DIR-1 | 2026-10-01 | Direction (design pass 3) | "Proceed as recommended." | `RUN/OWNER_DECISIONS.md`, "Direction to prepare" |
| DIR-2 | 2026-10-02 | Direction (closeout) | "yes, run the closeout." | same |
| DECISION-1 | 2026-10-03 | K1: scope-change groups 1 and 2 | "accept the remaining items as recommended" | same file (sha256 `59b20bb0…f919`), added by `5b16bb6831`. Recorded in `checkpoint_snapshots/SCA-V4-003_GROUP-1_2026-10-03/` (`3e747b7685`) and `SCA-V4-003_GROUP-2_2026-10-03/` (`ec267bdb9f`) |

DECISION-1 also accepted Q-13 (six deliverables INITIALIZED → IN_PROGRESS)
as a separate act outside the amendment; HELP_HUMAN recorded it at
`baa6e618d7`. The decision reference of supersession row D-021 is DECISION-1,
item Q-10, option B, bound to register row 21.

## Execution-stage records (node AK1, stage 2, after both snapshots were committed)

- **E-1 · Order.** Stage 1 wrote the group-1 and group-2 decision snapshots
  (HELP_HUMAN committed them with their pointers at `3e747b7685` and
  `ec267bdb9f`). Stage 2, from `ec267bdb9f`:
  1. the `Open_Issues.csv` application;
  2. this folder's byte copies and the delta;
  3. the accumulated map;
  4. the C-02 note;
  5. the transcriptions;
  6. the post-change audit;
  7. this log, `Handoff_State.md` and `RUN_SUMMARY.md`.
- **E-2 · Applied: B-02 option B and B-03** (`RUN/Application/apply_sca003.py`,
  `apply_log.json`).
  - The script reads the old and new whole-field values from the B-02/B-03
    table of BASIS_AMENDMENT.md. It first checks that the file matches the
    hash the group-2 manifest binds.
  - Checks before writing:
    - the target equalled its blob at `ec267bdb9f` and the bound pre-change
      hash `a1178218…80f0`;
    - the CSV writer (CRLF, minimal quoting) reproduced the unedited file
      byte for byte;
    - each old value equalled the current field;
    - re-parsing shows that only OI-009 `Status`, OI-009 `Consequence` and
      OI-018 `Consequence` differ.
  - Result: sha256 `9c2d916c277f8ce4b847c9c532822d0566e59517ba9e0a86b650fe0450f3515d`
    (the packet's stated hash for Q-10 B with the OI-018 pointer); OPEN
    23 → 22. A dry run to scratch first gave identical bytes.
- **E-3 · Held, not applied.**
  - B-01 (`SOFTWARE_DECOMP.md` Decision Log entry): untouched (sha256
    `ea3388bc…d7d5`); its old block occurs once.
  - C-01: `_ScopeChange/_LATEST.md` untouched (sha256 `2b7938bc…c2e1`; it
    still names SCA-V4-002).
  - No ScopeOfWork, register, `_DEPENDENCIES.md`, `_DAG`, `_STATUS.md`,
    `_CONTEXT.md`, basis or `Coverage_Telemetry.json` byte was written.
- **E-4 · Byte copies and the delta** (`RUN/Application/gen_candidate.py`,
  `gen_candidate_log.json`). Each source was checked against its bound hash
  before copying.
  - `Amendment_Actions.csv` copies the group-2 register (`9b7c2ce8…6d1c`).
  - `Impact_Assessment.md` copies the packet's IMPACT_ASSESSMENT
    (`46ea15e5…35f3`).
  - `Pre_Change_Coverage.json` copies `RUN/BASELINE/coverage_summary.json`
    (`99f016cc…e37f`).
  - `Supersession_Delta.csv` is BASIS_AMENDMENT Part D's csv block, byte for
    byte (sha256 `9c84814a…b19c`; 1 row, D-021; LF line endings, like
    SCA-V4-002's delta).
- **E-5 · Supersession map.** Command:
  `tools/coordination/accumulate_supersession_map.py --prior-map SCA-V4-002_2026-09-29_1901/Supersession_Map.csv --delta Supersession_Delta.csv --output-map Supersession_Map.csv`.
  - Result: exit 0, 30 rows (29 + 1), 0 findings
    (`RUN/Application/Supersession_Findings.csv`, header only). A second run
    with `--check-map` against the written map passes. The first 29 rows
    equal SCA-V4-002's map.
  - D-021 check: the superseded value `OPEN` is the GROUP3 canonical OI-009
    `Status`; the replacement `RESOLVED_BY_OWNER_DECISION` is the working
    value after E-2.
- **E-6 · C-02, the SCA-V4-002 effective-state note** (`RUN/Application/write_c02.py`,
  `c02_log.json`).
  - Written to
    `_ScopeChange/_PostAcceptanceValidation/SCA-V4-002_20261004T002903Z_EFFECTIVE_STATE/EFFECTIVE_STATE.md`
    (sha256 `ef2c22d7…6385`).
  - It is the C-02 text block of the bound BASIS_AMENDMENT.md, which already
    carries V23b's n-1 correction ("checked for SCA-V4-003 by review V23b:
    all 18 Design files that pin the basis documents carry their current
    hashes").
  - Slots filled: `{C02_UTC}` = `20261004T002903Z`; `{HEAD}` = `ec267bdb9f…`.
  - Two checks at writing: `Coverage_Telemetry.json` is still Revision
    `G3-draft-1` (ActiveOpenIssueCount 24), and the earlier record
    `SCA-V4-002_20260930T044342Z_EFFECTIVE_STATE` exists.
  - **Disclosure.** The accepted wording says "by HELP_HUMAN". The file was
    written by AK1, a Type 2 node HELP_HUMAN dispatched for this purpose.
    The accepted bytes were kept, not reworded; this entry records the
    actual writer.
- **E-7 · Transcriptions after the act.** No decision snapshot binds
  `Brief.md`, `Intake_Actions.csv`, `Amendment_Preview.md` or
  `Propagation_Plan.md`. Each states its sources and that the bound packet
  governs.
  - `Intake_Actions.csv` is the register's 23 rows with `ScopeChanging` blank
    and `Status` `PROPOSED` (`RUN/Application/gen_intake.py`), as SCA-V4-002
    did.
  - `Amendment_Preview.md` ends with BASIS_AMENDMENT.md from "## A." to its
    end, byte for byte (checked).
- **E-8 · Post-change audit** (`RUN/POSTCHANGE/`). Same scope and
  byte-identical script as the baseline.
  - Result: 0 BLOCKER, 52 WARNING, 77 INFO (baseline 0 / 35 / 93).
    `COMPARISON.md` attributes every difference:
    - 16 Check 6 rows INFO → WARNING: the Q-13 act;
    - COV-116 and COV-121: B-02/B-03;
    - COV-129 (new WARNING): this folder before its records, recommended
      `EXPECTED_CONSEQUENCE`.
  - The DEL-03-04 GUIDE change at `a68a9e06e2` moves no finding.
  - `Post_Change_Coverage.json` is a byte copy of that run's
    `coverage_summary.json` (`17fd4b0e…795d`).
- **E-9 · DAG-003 currency.** `shasum -a 256 -c _DAG/DAG-003/SOURCE_MANIFEST.sha256`
  (from the execution root) gives 130/130 OK (`RUN/Application/DAG_CURRENCY.txt`).
  The working `Open_Issues.csv` is not bound in DAG-003.
- **E-10 · Every register target at the basis.** All 42 `AffectedFiles`
  paths were hashed against their blobs at `ec267bdb9f`
  (`RUN/Application/target_hashes.txt`). 41 are unchanged; only
  `Open_Issues.csv` changed. The 19 ScopeOfWork files equal the SOW_REVISIONS
  prior hashes, 19/19.
- **E-11 · Not yet done.** The independent review of this candidate
  (method step 5) has not run. `Handoff_State.md` and `RUN_SUMMARY.md` are
  written before it, as the dispatcher directed. The review may require them
  to be revised before group 3 is presented.
- **E-12 · Review and record fix (2026-10-03, node AK1-R).** The candidate
  was committed at `fa16393978`. Independent review `RUN/reviews/V24.md`
  (`64a01f0c4c`) found it READY FOR GROUP 3 after M-1, with no blocking
  finding. E-11 above stays as history.
  - **What changed:** only `Handoff_State.md` and `RUN_SUMMARY.md` were
    revised.
  - **M-1:**
    - a parsable `**Closure verdict:**` line (proposed) was added;
    - V24 and `fa16393978` are cited;
    - stale statements were replaced;
    - the finalization edits F-1 to F-4 (group-3 snapshot, this log's
      group-3 entry, the accepted status lines) were listed beside H-1 to
      H-3.
  - **Minors:**
    - m-1: H-3 runs the baseline script unchanged;
    - m-2: the `{ACCEPT_DATE}` rule and the H-1 result rule;
    - m-3, m-5: one-line notes;
    - m-6: all 13 artifact hashes in
      `RUN/Application/CANDIDATE_ARTIFACTS.sha256`;
    - m-4, O-1 and O-2 are noted for the group-3 package.
  - **Simulated post-acceptance audit:**
    `RUN/Application/SIMULATED_POSTACCEPT.md`.
  - No applied, accepted or group-bound byte changed.
