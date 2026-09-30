# Decision log — SCA-V4-002 pre-change baseline (node P3)

These are the TASK's defaults, overrides and judgments. None of them changes the decomposition.

- **D-1 · Output location.** The brief confines writes to `BASELINE/` in the run folder, so the snapshot contents
  go here instead of `_Evaluation/DecompCoverage/`. This follows the earlier BASELINE, POSTCHANGE and POSTACCEPT runs.
  No scaffolding script was run. No `_LATEST.md` was created or moved. The integrator may copy
  `coverage_summary.json` into the SCA-V4-002 snapshot as `Pre_Change_Coverage.json`.

- **D-2 · Expected source: GROUP3 as amended by SCA-V4-001.**
  - **Pointer of record:** `_ScopeChange/_LATEST.md` (sha256 `a9a7cdc8…339d`). It names
    `_ScopeChange/SCA-V4-001_2026-09-28_2155/` as the active snapshot, with status `OPEN_PENDING_DERIVATIVE_CLOSURE`.
    It records the group-3 acceptance (DECISION-8).
  - **Base:** `_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z`.
  - **Why this pointer:**
    - `_Decomposition/checkpoint_snapshots/_LATEST_ACCEPTED.md` still names GROUP3 alone, and
      `_Decomposition/_LATEST.md` reads `Latest: (none)`. Neither pointer says that GROUP3 has been amended. That gap is
      ASC-ISS-006, which SCA-V4-002 addresses as Q-12 (B-06a/b/c).
    - The scope-change contract has each stage consume the preceding accepted snapshot. The owner-facing reading rule
      proposed in Q-12 is "GROUP3 as amended by the active amendment".
    - GROUP3 alone would be the wrong expected source. Seven working decomposition files legitimately differ from it
      because SCA-V4-001 amended them (COV-128, 129, 131–135).
  - **Parity check.** The run checked working bytes against the SCA-V4-001 accepted poststate, using two sources:
    - the post-acceptance validation `applied_hashes` (13 files), and
    - the group-3 `ACCEPTED_MANIFEST.csv` rows marked "unchanged after this act" (9 files).

    All **22/22** are equal (`coverage_summary.json` `extensions.expected_source`).
  - **Changes since acceptance.** Commits after SCA-V4-001 acceptance (`a0af39f8c`..`f05bd1bbd`) changed nothing under
    `_Decomposition/`, `docs/` or `_ScopeChange/`. They changed only the derivative-closure work: the 16 SoW REVISEs
    and the dependency registers.

- **D-3 · Scope: PKG-01, 02, 03, 04, 05, 09, 10 (32 deliverables).**
  - **Derivation.** The script derives the scope from the proposed register in IMPACT_ASSESSMENT §3.2 (rows 1–16). It
    takes the `EntityID` of each DELIVERABLE row, plus every deliverable folder named in `AffectedFiles`, and asserts
    that the result equals the audited scope (`extensions.scope_check.scope_equals_register_packages = true`).
  - **PKG-05 beyond the brief's minimum.** The brief's minimum is PKG-01, 02, 03, 04, 09 and 10. Register row 16
    (B-06c, Q-12) edits the `_CONTEXT.md` files of **DEL-05-01 and DEL-05-02**, so PKG-05 is added.
  - **PKG-08 is excluded.** No row names a PKG-08 entity. The earlier SCA-V4-001 runs included it; this run does not.
  - **Whole-decomposition rows.** Rows 10–13 and 15 touch `docs/HOST_INTEGRATION.md`, `Consolidated_Coverage.csv`,
    OI-012, the Decision Log and the two decomposition pointers. They are covered because Checks 7, 8, 9 and 9b run
    over the whole registers.
  - **ASC-ISS-008.** The §7 re-quote of DEL-04-03 falls in PKG-04, which is already in scope.
  - **Post-change audit.** It must use `PKG-01,PKG-02,PKG-03,PKG-04,PKG-05,PKG-09,PKG-10`.
  - **Whole-repository totals.** These are in `repository_topology`. `structure.json` covers all 41 units.

- **D-4 · Reuse not admissible (method step 5).** The reuse rule requires the recorded audit inputs to be
  byte-identical to the current pre-change state. Three candidates fail:
  - **POSTACCEPT** (`3d006a909` plus the edits committed at `a0af39f8c`). The decomposition package is byte-identical,
    but 16 scoped `ScopeOfWork.md` files were revised afterwards (`340ecf341`), which changes Check 5 and 6 inputs. Its
    scope also differs: PKG-08 in, PKG-10 out.
  - **CA1** (`_Evaluation/ScopeClosureAudit/ScopeClosure_SCA-V4-001_2026-09-29_1222/`). This is an
    `audit-scope-closure` run, not an `audit-decomp` run. It has no `coverage_summary.json`, so it cannot serve as
    this baseline.

  A fresh run was therefore made. `INPUT_MANIFEST.sha256` records the audited bytes (170 files), so a later rerun can
  test reuse or parity.

- **D-5 · Script.** `audit_checks.py` is POSTACCEPT's script. The Check 1–11 logic, rules, severities and issue order
  are unchanged. The changes are these:
  - **(c) Wording only.** The descriptions of Check 9 observations no longer make claims that are false at
    `f05bd1bbd`:
    - the "bytes identical to the frozen GROUP3" SoW claim;
    - the stale "A30" and "IA §8" references;
    - the pointer note;
    - the GROUP3-difference explanation, which is now derived from SCA-V4-001 `Amendment_Actions.csv` `AffectedFiles`
      instead of being asserted.
  - **(d) One Check 10 INFO, appended last.** It records the result of the registered pointer parser.
  - **(e) Expected-source parity and scope derivation.** These are recorded in `extensions`.

  A control run on a `git archive` of `a0af39f8c` checked both scripts:
  - POSTACCEPT's script reproduces POSTACCEPT's IssueLog (`ecaea862…`) and Matrix (`32ec176d…`) byte for byte.
  - This script's IssueLog differs only in the Description text of 11 Check 9 rows and in the one appended INFO row.
    Its Matrix is identical.

- **D-6 · Relationship to POSTACCEPT.** This run shares 28 deliverables with POSTACCEPT. Their matrix rows are
  identical. The count differences come from scope alone:
  - INFO 94 → 101: two more deliverables in scope, and the appended COV-139;
  - artifact presence 11.22 % → 10.78 %;
  - WARNING 38 → 38.

- **D-7 · Check 10 INFO for the registered parser (COV-139).** The audit-decomp Step 10 reading passes: exactly one
  `**Active snapshot:**` line, the folder exists, all 13 required artifacts are present, and the state fields are
  admissible. Separately, `_latest_pointer_target` in `tools/validation/validate_domain_decomposition_integrity.py`
  returns `None` for this pointer (V13 F2). Its severity is INFO, not BLOCKER:
  - the parser is the DOMAIN integrity tool's helper, not the SOFTWARE audit-decomp check;
  - the pointer is unambiguous to Step 10;
  - the fix is already decided scope of SCA-V4-002 (item 5a, C-01).

  The post-change audit should still show it, because C-01 lands only at group 3. The post-acceptance run should not.

- **D-8 · Severities kept.** The 37 Check 6 WARNINGs are anticipated artifacts absent at IN_PROGRESS. They remain
  WARNINGs, as in POSTACCEPT D-6. The run records no `EXPECTED_CONSEQUENCE`.

- **D-9 · Unchanged defaults.** BASELINE (APP-V4-BASIS-ALIGN) decisions D-4 to D-9 apply unchanged:
  - Check 7 uses the ledger `ObjectiveIDs` column as the authority;
  - Checks 7 and 8 evaluate the whole registers;
  - Check 5 compares 15 fields exactly after whitespace normalization;
  - Check 6 uses the fuzzy artifact rule;
  - Check 9 is SKIPPED for a non-DOMAIN variant.
