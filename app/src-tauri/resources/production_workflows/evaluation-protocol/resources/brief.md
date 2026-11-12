# BRIEF SCHEMA — evaluation-protocol

This file defines the undertaking brief for WORKING_ITEMS with `Workflow: evaluation-protocol`.

## Purpose

Use this workflow when WORKING_ITEMS needs to run the read-only, five-phase evaluation
method over an accepted project scope and produce the `_Evaluation/` artifact set
(protocol, findings, report, handoff) plus preserved child returns.

The workflow is method-only. All write authority, dispatch, and fan-in validation
remain with the WORKING_ITEMS shell. This brief supplies the accepted basis, scope,
questions, toolbelt, and write targets under `_Evaluation/`.

## Scope model

- `ScopePath` should normally be the execution root.
- `AllowedWriteTargets` should be limited to the intended output paths under
  `{EXECUTION_ROOT}/_Evaluation/`. The workflow never writes outside them.
- `RequestedBy` defaults to `WORKING_ITEMS`.

## Required brief fields

| Field | Type | Meaning | Example |
|---|---|---|---|
| `PURPOSE` | string | Why this evaluation run exists | `Assess PKG-014 structure and dependency closure.` |
| `RequestedBy` | string | Dispatching manager | `WORKING_ITEMS` |
| `ScopePath` | path | Execution root | `/repo/execution/` |
| `Workflow` | string | Must equal the workflow folder/name | `evaluation-protocol` |
| `RuntimeOverrides.EXECUTION_ROOT` | path | Project execution root | `/repo/execution/` |
| `AcceptedBasis` | list[ref] | Accepted snapshot / source / decomposition basis references | `[snapshots/decomp/2026-07-10/]` |
| `EvaluationQuestions` | list[string] | Human-framed questions to answer | `["Are declared dependencies closed?"]` |
| `Scope` | list[path or id] | Deliverables/packages/surfaces in scope | `[/repo/execution/PKG-014/]` |
| `PermittedToolbelt` | list[capability] | Accepted audits/workflows/tools/specialists | `[TASK (workflow: audit-dep-closure), content-digest]` |
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
  performed by the WORKING_ITEMS shell, not by this workflow.
