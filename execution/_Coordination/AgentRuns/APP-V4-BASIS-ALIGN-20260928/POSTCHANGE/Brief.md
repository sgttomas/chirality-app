# Brief — post-change audit (node AK1), APP-V4-BASIS-ALIGN-20260928

## Brief (from the integrator, HELP_HUMAN; the audit item, verbatim)

> 4. **Post-change audit.** Run `workflows/audit-decomp` read-only with the **same seven-package scope** as BASELINE/ (PKG-01, 02, 03, 04, 05, 08, 09). Write it to `POSTCHANGE/` in the run folder, and compare it with BASELINE/coverage_summary.json, listing every difference and its cause.

The same brief directs node AK1 to write the SCA-V4-001 group-1 and group-2
decision snapshots, apply the accepted candidate edits and regenerate the
affected derivatives first. Write scope for this item: `POSTCHANGE/` only.
Scratch: the session scratchpad `AK1/`. Git read-only; no network.

## Normalized parameters (audit-decomp contract, "Inputs")

| Parameter | Value |
|---|---|
| `EXECUTION_ROOT` | `projects/chirality-app-v4/execution` |
| `DECOMPOSITION_PATH` | `projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md`, with the companion registers of `Companion_Inventory.csv` |
| `DECOMP_VARIANT` | `SOFTWARE` |
| `SCOPE` | `PKG-01, PKG-02, PKG-03, PKG-04, PKG-05, PKG-08, PKG-09` (30 deliverables), identical to BASELINE |
| `RUN_LABEL` | `APP_V4_SCA_V4_001_POSTCHANGE` |
| `REQUESTED_BY` | HELP_HUMAN integrator of APP-V4-BASIS-ALIGN-20260928 (scope-change group-3 preparation, method step 5) |
| `PRIOR_RUN_LABEL` | `APP_V4_SCA_V4_001_PRECHANGE` (BASELINE/); the comparison is in `COMPARISON.md` |
| `EXPECTED_SOURCE_SNAPSHOT` | `_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z` (accepted decomposition), amended by the SCA-V4-001 candidate |
| `EXPECTED_HANDOFF_PHASE` | scope-change group-3 preparation; candidate `execution/_ScopeChange/SCA-V4-001_2026-09-28_2155/`, posture FIRST_AMENDMENT |
| `ACCEPTED_DECISIONS` | `execution/_ScopeChange/checkpoint_snapshots/SCA-V4-001_GROUP-1_2026-09-28/`, `SCA-V4-001_GROUP-2_2026-09-28/` (DECISION-7); run DECISION-6 (lifecycle) |
| Subject tree | commit `f4ba34c2c` plus the uncommitted SCA-V4-001 candidate edits (15 files) |
| Executor | Claude Code subagent (Type 2 TASK, node AK1); no delegation; git read-only; no network |
