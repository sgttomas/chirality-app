# BRIEF SCHEMA — evaluation-protocol

This file defines the INIT-TASK dispatch contract for `TASK + evaluation-protocol`.

## Purpose

Use this skill when EVALUATION needs to run the read-only, five-phase evaluation
method over an accepted project scope and produce the `_Evaluation/` artifact set
(protocol, findings, report, handoff) plus preserved child returns.

The skill is method-only. All write authority, dispatch, and fan-in validation
remain with the EVALUATION shell. This brief supplies the accepted basis, scope,
questions, toolbelt, and write targets under `_Evaluation/`.

## Scope model

- `ScopePath` should normally be the execution root.
- `AllowedWriteTargets` should be limited to the intended output paths under
  `{EXECUTION_ROOT}/_Evaluation/`. The skill never writes outside them.
- `RequestedBy` defaults to `EVALUATION`.

## Required brief fields

| Field | Type | Meaning | Example |
|---|---|---|---|
| `PURPOSE` | string | Why this evaluation run exists | `Assess PKG-014 structure and dependency closure.` |
| `RequestedBy` | string | Dispatching manager | `EVALUATION` |
| `ScopePath` | path | Execution root | `/repo/execution/` |
| `TaskSkill` | string | Must equal the skill folder/name | `evaluation-protocol` |
| `RuntimeOverrides.EXECUTION_ROOT` | path | Project execution root | `/repo/execution/` |
| `AcceptedBasis` | list[ref] | Accepted snapshot / source / decomposition basis references | `[snapshots/decomp/2026-07-10/]` |
| `EvaluationQuestions` | list[string] | Human-framed questions to answer | `["Are declared dependencies closed?"]` |
| `Scope` | list[path or id] | Deliverables/packages/surfaces in scope | `[/repo/execution/PKG-014/]` |
| `PermittedToolbelt` | list[capability] | Accepted audits/skills/tools/specialists | `[AUDIT_DEP_CLOSURE, content-digest]` |
| `AllowedWriteTargets` | list[path] | Output targets under `_Evaluation/` | `[/repo/execution/_Evaluation/]` |
| `ExpectedOutputs` | list[path] | Artifacts this run must produce | `[/repo/execution/_Evaluation/EVALUATION_REPORT.md, /repo/execution/_Evaluation/FINDINGS.csv, /repo/execution/_Evaluation/HANDOFF.md]` |
| `AcceptanceCriteria` | list[string] | What makes the run complete and valid | `["All findings evidence-linked", "Handoff names owners"]` |

## Optional brief fields

| Field | Type | Meaning | Default |
|---|---|---|---|
| `ScoringRubric` | ref/spec | Accepted rubric; required before any dimension is scored | none — no score produced |
| `FanOutAuthorization` | bool/spec | Human authorization for concurrent independent-scope dispatch | absent — stepwise dispatch only |

## Runtime-override guidance

- `EXECUTION_ROOT` must identify the project execution root; all `_Evaluation/`
  write targets resolve under it.
- Nothing outside `PermittedToolbelt` is dispatched.
- Without `ScoringRubric`, the run produces no score; findings and
  recommendations are still produced.
- Without `FanOutAuthorization`, dispatch is stepwise: at most one Agent 2 per
  cycle, returning implications before continuing.
- Dispatch, brief-sealing, and fan-in validation for any child capability are
  performed by the EVALUATION shell, not by this skill.

## CustomInstructions guidance

Recommended run-specific reinforcement (does not replace skill hydration):

- Restate that all writes stay under `AllowedWriteTargets` and no subject file is
  modified.
- Restate the `FINDINGS.csv` column order and that every row must be
  evidence-linked.
- Restate that closure requires basis, coverage, conflicts, blockers, and rerun
  requirements to be recorded.
