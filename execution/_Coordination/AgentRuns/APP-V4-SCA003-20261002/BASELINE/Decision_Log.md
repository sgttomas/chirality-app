# Decision log — SCA-V4-003 pre-change baseline (node P3)

These are the TASK's defaults, overrides and judgments. None of them changes the decomposition, a register, a
ScopeOfWork, a pointer or a DAG file.

- **D-1 · Output location.** The brief confines writes to `BASELINE/` in the run folder, so the snapshot contents go
  here instead of `_Evaluation/DecompCoverage/`, as in the SCA-V4-002 BASELINE, POSTCHANGE and POSTACCEPT runs. No
  scaffolding script was run; no `_LATEST.md` was created or moved. The integrator may copy `coverage_summary.json`
  into the SCA-V4-003 snapshot as `Pre_Change_Coverage.json`.

- **D-2 · Expected source: GROUP3 as amended by SCA-V4-001 and SCA-V4-002, with SCA-V4-002's propagation.**
  - **Pointer of record:** `_ScopeChange/_LATEST.md` (sha256 `2b7938bc…c2e1`, SPEC §11.2 form): `Latest:
    SCA-V4-002_2026-09-29_1901`, accepted predecessor SCA-V4-001, closure `OPEN_PENDING_DERIVATIVE_CLOSURE`. The
    registered parser resolves it (`pointer_matches_active` True).
  - **Reading rule:** now stated by the decomposition pointers themselves. `_Decomposition/checkpoint_snapshots/
    _LATEST_ACCEPTED.md` carries B-06a ("read this snapshot as amended by the active scope-change snapshot named in
    `../../_ScopeChange/_LATEST.md`"; commit `1efd4bcda`), and `_Decomposition/_LATEST.md` carries B-06b. ASC-ISS-006
    is therefore closed in the bytes.
  - **Parity check (148 files, all equal).** Working bytes were checked against three accepted records:
    - SCA-V4-002 `post_acceptance_checks.json` `applied_hashes` (9 files);
    - SCA-V4-002 GROUP-3 `ACCEPTED_MANIFEST.csv` rows "unchanged after this act" (9 files);
    - DAG-003 `SOURCE_MANIFEST.sha256` (130 entries; 130 new to the list): every `ScopeOfWork.md`, `Dependencies.csv`
      and `_DEPENDENCIES.md`, `_LATEST_ACCEPTED.md`, GROUP3's decision and four canonical registers, and
      `_COORDINATION.md`. These are the post-REVISE/UPDATE bytes the owner accepted DAG-003 on (DECISION-4).
  - **Changes since SCA-V4-002 acceptance.** `git log af918ee50..897a107cc` over `_Decomposition/`, `_ScopeChange/`,
    `docs/` and every scoped `ScopeOfWork.md`, `Dependencies.csv`, `_CONTEXT.md` and `_STATUS.md` shows only
    `1efd4bcda` (9 REVISEs, B-06a), `8cd783d8d` (11 register UPDATEs) and `877b63b38` (closure audit and effective-state
    record). Design passes 2 and 3 changed none of these files; they added and edited `Design/` files only.

- **D-3 · Scope: PKG-01, 02, 03, 04, 05, 09, 10 (32 deliverables).**
  - **Derivation.** P1's ledger and impact assessment did not exist when this run started (they are written in
    parallel). The script therefore derives the target deliverables from the proposal records P1 consolidates:
    the per-deliverable sections of design pass 2 closeout C1-A, C1-B, C1-C and design pass 3 closeout C1-A, C1-B,
    and the register rows of pass-3 `F/F0_JOINS.md` §3 (the deliverable whose register carries each NR/M/ST row).
    Result: 20 deliverables in PKG-01 (01-01…01-05), PKG-02 (02-01…02-04), PKG-03 (03-01…03-04), PKG-04
    (04-01…04-03), PKG-05 (05-01, 05-02) and PKG-09 (09-06, 09-09). `extensions.scope_check` records each one with
    its source record and asserts `scope_covers_record_packages = true`.
  - **PKG-10 kept.** No record targets a DEL-10-03 file; DEL-10-03 is named only as a receiver (SC2-02-01-2,
    SC2-02-03-6, SC3-02-04-9) or as the existing counterpart of a mirror row (R-02-2, R3-02-04-b). It is kept so the
    scope equals the SCA-V4-002 baseline and post-acceptance audits, which makes `COMPARISON.md` like for like.
  - **Whole-decomposition items.** `Open_Issues.csv` (pass-3 C1-B: OI-009 kept with amendments, OI-018 pointer
    optional) and the five pass-2 basis items (C1-B §7, C1-C; no text) touch whole-decomposition surfaces. Checks 7,
    8, 9 and 9b evaluate the whole registers, so they are covered.
  - **Check for P1.** If P1's IMPACT_ASSESSMENT names a target outside these six packages, the post-change audit
    needs a wider scope and this baseline a rerun on it. At the time of writing `AMENDMENT_PACKET/` was empty.

- **D-4 · Reuse not admissible (method step 5).** POSTACCEPT (`APP_V4_SCA_V4_002_POSTACCEPT`) has the same scope, but
  21 of its 185 shared input files have changed since (the 9 REVISEs, 11 registers and B-06a), and Design files added
  by design passes 2 and 3 change Check 6 inputs. A fresh run was made. `INPUT_MANIFEST.sha256` records 215 audited
  files for a later reuse or parity test.

- **D-5 · Script.** `audit_checks.py` is POSTACCEPT's script with five documented changes and no check, rule,
  severity or ordering change:
  - **(h)** the Check 9 INFO on `_Decomposition/_LATEST.md` (POSTACCEPT COV-127, ASC-ISS-006) is emitted only while
    `_LATEST_ACCEPTED.md` lacks the reading rule. Its POSTACCEPT wording ("does not say that the active amendment …
    amends it") is false at the subject. The pointer state goes to `extensions.decomposition_pointers`. POSTACCEPT's
    COMPARISON had recorded that this finding "closes only with B-06a";
  - **(i)** the GROUP3-difference INFO attributes each file to the rows of both accepted amendments' Amendment_Actions;
  - **(j)** the parity basis is SCA-V4-002's accepted poststate with its propagation (D-2);
  - **(e2)** the scope derivation reads the SCA-V4-003 proposal records (D-3);
  - **(k)** `extensions.artifact_matches` lists the file names that satisfy the fuzzy Check 6 rule.

  Controls (scratch, not deliverables), both described in QA_Report:
  - POSTACCEPT's script on a `git archive` of `af918ee50` reproduces POSTACCEPT's IssueLog and Matrix byte for byte.
  - POSTACCEPT's script on the current state gives 0 / 35 / 94; this script gives 0 / 35 / 93. The Matrix is
    identical; the IssueLogs differ only by (h) (one row not emitted) and (i) (five Check 9 descriptions).

- **D-6 · Check 6 reading.** The 9 anticipated artifacts newly counted as found (3 WARNING and 6 INFO rows fewer than
  POSTACCEPT) are matched by Design documents, schemas, examples and prototypes that design passes 2 and 3 added, for
  example DEL-02-03 "CODE: required-tool and checkpoint receiving behavior" by `Design/prototype/required_tool_check.py`.
  The rule matches file names, not product code, and the closeouts state that prototypes are design aids. The
  10.78 % → 19.61 % rise is a heuristic effect and not evidence of production. Severities are kept (as POSTACCEPT D-6).

- **D-7 · Concurrent changes; subject kept at `897a107cc`.** During the run other actors edited three Design files
  (DEL-01-02 `EXECUTION_AND_RECOVERY.md`, DEL-01-04 `NATIVE_INTERACTION_RECEIVING.md`, DEL-02-04 `ROLE_SUPPLY.md`) and
  wrote the pass-3 `closeout/CLOSEOUT_ACCOUNT.md`, then committed them (`e510aa84f`, `bb9ab6182`, merge `f47ca8f6b`)
  with the DEL-03-04 GUIDE re-pin, 18 `MEMORY.md` files and pass-3 run records. None is an audit input except by file name (Check 6); the only
  added files in scoped deliverables are five `MEMORY.md`, which Check 6 excludes as control files. The manifest
  passes 215/215 at `f47ca8f6b` and a rerun there gave identical IssueLog and Matrix, so this baseline holds for
  both commits. Design-file contents and the pass-3 CLOSEOUT_ACCOUNT are not hashed: the scope derivation reads the
  C1-A/B records and F0_JOINS, which are committed and hashed.

- **D-8 · Unchanged defaults.** As in the SCA-V4-002 BASELINE (D-8, D-9): Check 6 absences stay WARNING at
  IN_PROGRESS and INFO at INITIALIZED; Check 7 uses the ledger `ObjectiveIDs` column; Checks 7 and 8 evaluate the whole
  registers; Check 5 compares 15 fields after whitespace normalization; Check 9 (DOMAIN parity) is SKIPPED for SOFTWARE.
  No `EXPECTED_CONSEQUENCE` is recorded.
