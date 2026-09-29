# Brief — post-acceptance audit (node AK2), APP-V4-BASIS-ALIGN-20260928

## Brief (from the integrator, HELP_HUMAN; the audit item, verbatim)

> 4. **H-5.** Run the post-acceptance validation under `_PostAcceptanceValidation/`, as the contract specifies. Rerun audit-decomp read-only with the seven-package scope (PKG-01, 02, 03, 04, 05, 08, 09), writing to the run folder's POSTACCEPT/. Compare with POSTCHANGE/ and BASELINE/. COV-131 (the Change Register binding) should now close.

The same brief directs node AK2 to do the following first:
- write the SCA-V4-001 group-3 decision snapshot (owner DECISION-8);
- apply H-1…H-4;
- finalize the accepted snapshot and `_ScopeChange/_LATEST.md`.

Its constraints:
- Write scope for this item: `POSTACCEPT/`, plus the `_PostAcceptanceValidation/` record.
- Scratch: the session scratchpad `AK2/`.
- Git read-only; no network.

## Normalized parameters (audit-decomp contract, "Inputs")

| Parameter | Value |
|---|---|
| `EXECUTION_ROOT` | `projects/chirality-app-v4/execution` |
| `DECOMPOSITION_PATH` | `projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md`, with the companion registers of `Companion_Inventory.csv` |
| `DECOMP_VARIANT` | `SOFTWARE` |
| `SCOPE` | `PKG-01, PKG-02, PKG-03, PKG-04, PKG-05, PKG-08, PKG-09` (30 deliverables), identical to BASELINE and POSTCHANGE |
| `RUN_LABEL` | `APP_V4_SCA_V4_001_POSTACCEPT` |
| `REQUESTED_BY` | HELP_HUMAN integrator of APP-V4-BASIS-ALIGN-20260928 (scope-change post-acceptance validation, method "After acceptance") |
| `PRIOR_RUN_LABEL` | `APP_V4_SCA_V4_001_POSTCHANGE` (POSTCHANGE/) and `APP_V4_SCA_V4_001_PRECHANGE` (BASELINE/); the comparison is in `COMPARISON.md` |
| `EXPECTED_SOURCE_SNAPSHOT` | `_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z` (accepted decomposition), amended by the accepted SCA-V4-001 |
| `EXPECTED_HANDOFF_PHASE` | post-acceptance. `_ScopeChange/_LATEST.md` names `SCA-V4-001_2026-09-28_2155` |
| `ACCEPTED_DECISIONS` | `execution/_ScopeChange/checkpoint_snapshots/SCA-V4-001_GROUP-1_2026-09-28/`, `…_GROUP-2_2026-09-28/` (DECISION-7), `…_GROUP-3_2026-09-29/` (DECISION-8); run DECISION-6 (lifecycle) |
| Subject tree | commit `3d006a909`, plus the uncommitted post-acceptance edits: H-1…H-4 in 6 files, the finalized snapshot records and `_LATEST.md` |
| Executor | Claude Code subagent (Type 2 TASK, node AK2); no delegation; git read-only; no network |
