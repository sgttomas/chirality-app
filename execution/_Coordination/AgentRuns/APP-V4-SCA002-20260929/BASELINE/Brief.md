# Brief — SCA-V4-002 pre-change baseline (node P3), APP-V4-SCA002-20260929

## Verbatim brief (from the dispatching agent)

> You are a Type 2 TASK executor (node P3) for Chirality App v4, run APP-V4-SCA002-20260929. You do not delegate.
>
> Working directory (git worktree): /Users/ryan/ai-env/projects/chirality/.claude/worktrees/test-ci-optimization-f6cacd. Basis commit: f05bd1bbd.
> Execution root: E = projects/chirality-app-v4/execution. Run folder: E/_Coordination/AgentRuns/APP-V4-SCA002-20260929/.
>
> **Task.** Produce the scope-change **pre-change baseline** for amendment SCA-V4-002, per `workflows/scope-change/resources/method.md` step 5.
> - Read the run folder's AMENDMENT_PACKET/IMPACT_ASSESSMENT.md for the affected entities and packages. The affected deliverables include DEL-01-01, 01-04, 02-01, 02-02, 02-03, 03-03, 04-01, 04-02, 09-07 and 10-03, plus the decomposition registers.
> - Use the package scope that covers every affected entity. It should be at least PKG-01, 02, 03, 04, 09 and 10; confirm it against the impact assessment, and record it so the post-change audit reuses the same scope.
> - Load `workflows/audit-decomp/WORKFLOW.md` and its resources. Run it read-only against the working decomposition at f05bd1bbd.
> - Note that SCA-V4-001 is the active accepted amendment. Record which snapshot and pointer you treat as the expected source, and why.
> - The earlier run's baseline and post-accept audits are useful references: E/_Coordination/AgentRuns/APP-V4-BASIS-ALIGN-20260928/BASELINE/ and POSTACCEPT/, including their `audit_checks.py`.
>
> **Write scope:** `BASELINE/` in the run folder only. For scratch, use /private/tmp/claude-501/…/scratchpad/P3-002/. Read-only git. No network. Change nothing else.
>
> Return: the baseline paths with their sha256, the scope used, the key coverage figures, and any finding that affects the SCA-V4-002 amendment.

A later message from the dispatcher reported a transient connection error and asked for the baseline to be completed
exactly as briefed. The worktree was clean at `f05bd1bbd` apart from this folder, which did not yet exist.

## Normalized parameters (audit-decomp contract, "Inputs")

| Parameter | Value |
|---|---|
| `EXECUTION_ROOT` | `projects/chirality-app-v4/execution` |
| `DECOMPOSITION_PATH` | `projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md`, with the authoritative companion registers named in `Companion_Inventory.csv` |
| `DECOMP_VARIANT` | `SOFTWARE` (IMPACT_ASSESSMENT §1) |
| `SCOPE` | **`PKG-01, PKG-02, PKG-03, PKG-04, PKG-05, PKG-09, PKG-10`** (32 deliverables). See Decision_Log D-3. The post-change audit must reuse this exact scope |
| `RUN_LABEL` | `APP_V4_SCA_V4_002_PRECHANGE` |
| `REQUESTED_BY` | dispatcher of run APP-V4-SCA002-20260929 (scope-change method step 5; IMPACT_ASSESSMENT §4 and §11) |
| `PRIOR_RUN_LABEL` | none. Comparison mode was not requested; D-6 records how this run relates to POSTACCEPT |
| `EXPECTED_SOURCE_SNAPSHOT` | `_ScopeChange/SCA-V4-001_2026-09-28_2155/` (the active accepted amendment named by `_ScopeChange/_LATEST.md`) over `_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z`. See Decision_Log D-2 |
| `EXPECTED_HANDOFF_PHASE` | scope-change SCA-V4-002 pre-change baseline, before checkpoint group 1. SCA-V4-001 is `OPEN_PENDING_DERIVATIVE_CLOSURE` |
| `ACCEPTED_DECISIONS` | SCA-V4-001 group snapshots `_ScopeChange/checkpoint_snapshots/SCA-V4-001_GROUP-{1,2}_2026-09-28/` and `…_GROUP-3_2026-09-29/` (DECISION-7, DECISION-8). No finding needed an `EXPECTED_CONSEQUENCE` classification |
| Basis commit | `f05bd1bbd4d7822deed22eeacfe89ad8d7c96fbd`; the worktree was clean except for this folder |
| Executor | Claude Code subagent (Type 2 TASK, node P3); no delegation; git read-only; no network |
