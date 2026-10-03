# Brief — SCA-V4-003 pre-change baseline (node P3), APP-V4-SCA003-20261002

## Verbatim brief (from the dispatching agent)

> You are a Chirality Type 2 TASK executor (bounded assignment; you do not delegate). Repository worktree: /Users/ryan/ai-env/projects/chirality/.claude/worktrees/test-ci-optimization-f6cacd . Project execution root: projects/chirality-app-v4/execution (E). Run folder: E/_Coordination/AgentRuns/APP-V4-SCA003-20261002 (RUN).
>
> Your node: **P3** of SCA-V4-003, the pre-change baseline. Read RUN/BRIEFS.md (common rules and section P3) and RUN/OWNER_DECISIONS.md. Model: E/_Coordination/AgentRuns/APP-V4-SCA002-20260929/BASELINE/ (its Brief.md, RUN_SUMMARY.md, audit_checks.py, INPUT_MANIFEST.sha256 and reports) and that run's DISPATCH row P3; method workflows/scope-change/resources/method.md (pre-change baseline step). Reproduce the same baseline for the current state (decomposition, registers, ScopeOfWork files, `_ScopeChange/_LATEST.md` naming SCA-V4-002, DAG-003), noting any finding that differs from SCA-V4-002's post-acceptance audit. Another executor (P1) writes RUN/AMENDMENT_PACKET/ in parallel.
>
> Write only RUN/BASELINE/ and scratch under $TMPDIR. Nothing applied. Read-only git; no network; no Codex or model runs. Reply with a short summary: BLOCKER/WARNING/INFO counts, differences from the SCA-V4-002 poststate, anything that bears on the amendment.

`RUN/BRIEFS.md` section P3 (as written): "As SCA-V4-002's P3 (`BASELINE/`): coverage audit of the current
decomposition and registers, input manifest. Output `BASELINE/`." Its common rules apply: read-only git, no network,
write only the fence, nothing applied, every item cites its source.

## Normalized parameters (audit-decomp contract, "Inputs")

| Parameter | Value |
|---|---|
| `EXECUTION_ROOT` | `projects/chirality-app-v4/execution` |
| `DECOMPOSITION_PATH` | `projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md`, with the companion registers named in `Companion_Inventory.csv` |
| `DECOMP_VARIANT` | `SOFTWARE` (as SCA-V4-001 and SCA-V4-002) |
| `SCOPE` | **`PKG-01, PKG-02, PKG-03, PKG-04, PKG-05, PKG-09, PKG-10`** (32 deliverables), the SCA-V4-002 baseline and post-acceptance scope. It covers every package the SCA-V4-003 proposal records target (PKG-01…05, 09); PKG-10 is kept for comparability. See Decision_Log D-3. The post-change audit must reuse this exact scope |
| `RUN_LABEL` | `APP_V4_SCA_V4_003_PRECHANGE` |
| `REQUESTED_BY` | HELP_HUMAN, dispatcher of run APP-V4-SCA003-20261002 (scope-change method step 5) |
| `PRIOR_RUN_LABEL` | none (comparison mode not requested). `COMPARISON.md` sets this run against `APP_V4_SCA_V4_002_POSTACCEPT` as the brief asks |
| `EXPECTED_SOURCE_SNAPSHOT` | `_ScopeChange/SCA-V4-002_2026-09-29_1901/` (the active accepted amendment named by `_ScopeChange/_LATEST.md`) over `_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z`, with SCA-V4-002's completed propagation (the post-REVISE/UPDATE bytes DAG-003 was accepted on). See Decision_Log D-2 |
| `EXPECTED_HANDOFF_PHASE` | scope-change SCA-V4-003 pre-change baseline, before checkpoint group 1. SCA-V4-002 is `OPEN_PENDING_DERIVATIVE_CLOSURE` for owner-deferred derivatives only (its EFFECTIVE_STATE record) |
| `ACCEPTED_DECISIONS` | SCA-V4-002 group snapshots `_ScopeChange/checkpoint_snapshots/SCA-V4-002_GROUP-{1,2,3}_2026-09-29/`; DAG-003 acceptance (`_DAG/DAG-003/ACCEPTANCE_RECORD.md`). No finding needed an `EXPECTED_CONSEQUENCE` classification |
| Basis commit | `897a107cc90e48792cf4e05b5d1313017292f290`. HEAD moved to `f47ca8f6b` during the run with no audited input changed (QA_Report, "Subject"; Decision_Log D-7) |
| Executor | Claude Code subagent (Type 2 TASK, node P3); no delegation; git read-only; no network; no Codex or model runs |
