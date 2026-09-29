# Brief — pre-change baseline (node P3), APP-V4-BASIS-ALIGN-20260928

## Verbatim brief (from the integrator, HELP_HUMAN under a recorded WORKING_ITEMS consultation)

> You are a Type 2 TASK executor (node P3) for Chirality App v4, run APP-V4-BASIS-ALIGN-20260928. You do not delegate.
>
> Working directory (git worktree): /Users/ryan/ai-env/projects/chirality/.claude/worktrees/test-ci-optimization-f6cacd
> Execution root: projects/chirality-app-v4/execution. Basis commit: 306291bdd.
> Run folder: execution/_Coordination/AgentRuns/APP-V4-BASIS-ALIGN-20260928/.
>
> **Task.** Produce the scope-change **pre-change baseline**, as required by `workflows/scope-change/resources/method.md` step 5 and packet item O-20 in AMENDMENT_PACKET/OWNER_ITEMS.md. Read O-20, and IMPACT_ASSESSMENT.md, for why the earlier GROUP3 audit cannot be reused.
>
> Steps:
> - Load `workflows/audit-decomp/WORKFLOW.md` and its resources.
> - Run it read-only against the accepted decomposition, resolved through execution/_Decomposition/ (the `_LATEST` pointer or accepted snapshot), at 306291bdd.
> - Produce `coverage_summary.json` and the audit report the scope-change method expects as its baseline.
>
> **Write scope:** `BASELINE/` under the run folder only. For scratch, use /private/tmp/…/scratchpad/P3/. Read-only git. No network. Change no decomposition, doc, SoW, register or _DAG file.
>
> Return: the baseline paths, their sha256, the key coverage figures, the tool versions and hashes, and any finding that would affect the amendment.

## Normalized parameters (audit-decomp contract, "Inputs")

| Parameter | Value |
|---|---|
| `EXECUTION_ROOT` | `projects/chirality-app-v4/execution` |
| `DECOMPOSITION_PATH` | `projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md`, with the authoritative companion registers named in `Companion_Inventory.csv` |
| `DECOMP_VARIANT` | `SOFTWARE` |
| `SCOPE` | `PKG-01, PKG-02, PKG-03, PKG-04, PKG-05, PKG-08, PKG-09` (30 deliverables); see Decision_Log D-3 |
| `RUN_LABEL` | `APP_V4_SCA_V4_001_PRECHANGE` |
| `REQUESTED_BY` | HELP_HUMAN integrator of APP-V4-BASIS-ALIGN-20260928 (scope-change method step 5; packet O-20 / IMPACT_ASSESSMENT U-1, U-3) |
| `PRIOR_RUN_LABEL` | none (no comparison mode) |
| `EXPECTED_SOURCE_SNAPSHOT` | `_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z` (via `_LATEST_ACCEPTED.md`) |
| `EXPECTED_HANDOFF_PHASE` | scope-change pre-change baseline before checkpoint group 1 (K1) |
| `ACCEPTED_DECISIONS` | none supplied; no finding is classified `EXPECTED_CONSEQUENCE` |
| Basis commit | `306291bddde7862e2a4a14856e325dcf8bf5e2cd` (working tree clean at start) |
| Executor | Claude Code subagent (Type 2 TASK, node P3); no delegation; git read-only; no network |
