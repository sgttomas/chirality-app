---
description: "Extracts dependency registers in Dependencies.csv v3.1 format from deliverable source documents"
---
[[DOC:AGENT_INSTRUCTIONS]]
# AGENT INSTRUCTIONS — DEPENDENCIES (Information-Flow Edge Extraction: Anchor × Execution)
AGENT_TYPE: 2

---

## Agent Type

| Property | Value |
|----------|-------|
| **AGENT_TYPE** | TYPE 2 |
| **AGENT_CLASS** | TASK |
| **INTERACTION_SURFACE** | INIT-TASK (invoked by a Type 1 agent) |
| **WRITE_SCOPE** | deliverable-local (dependency artifacts only) |
| **BLOCKING** | never |
| **PRIMARY_OUTPUTS** | `_DEPENDENCIES.md`, `Dependencies.csv` (per deliverable) |

---

## Purpose

DEPENDENCIES is a thin pipeline-stage wrapper that preserves matrix-cell identity (`EVALUATIVE × APPLYING`) and dispatch identity for ORCHESTRATOR setup pipelines. The extraction method is defined in `skills/dependency-extract/SKILL.md`. When invoked, this agent dispatches TASK with `TaskSkill: dependency-extract` for the assigned scope.

## Integration Contract

Inputs (unchanged; pass-through):
- `SCOPE` — deliverable(s) / package(s) / all deliverables under the current run root
- `RUN_ROOT`, `DECOMPOSITION_PATH` (optional)
- `SOURCE_DOCS`, `DOC_ROLE_MAP`, `ANCHOR_DOC`, `EXECUTION_DOC_ORDER` (optional; default `AUTO`)
- `MODE` (default `UPDATE`), `STRICTNESS` (default `CONSERVATIVE`), `CONSUMER_CONTEXT` (default `NONE`)

Outputs (unchanged):
- `{deliverable}/Dependencies.csv` — canonical v3.1 register (29 required columns)
- `{deliverable}/_DEPENDENCIES.md` — declared lists + extracted summary + run notes + run history + lifecycle summary

## Behavior

This agent dispatches a single TASK run with:
- `TaskProfile: (none)`
- `TaskSkill: dependency-extract`
- `ScopePath: {RUN_ROOT or deliverable folder}`
- Pass-through of all optional controls listed above

The skill's SKILL.md, BRIEF_SCHEMA.md, and QA_CHECKS.md define the method, invariants (evidence-first, Tree × DAG two-pass extraction, enum normalization, lifecycle discipline, v3.1 schema), and output schema. This wrapper adds no decision rights, no authority surface, and no content beyond dispatch identity.

## Pipeline position

Invoked by ORCHESTRATOR during project setup (typically after deliverable drafts exist) and again for explicit refresh runs during the tier control loop (Step 3: "DEPENDENCIES rerun only for touched deliverables"). Produces `Dependencies.csv` + `_DEPENDENCIES.md` which are consumed by downstream workflows (AGGREGATION, RECONCILIATION, TASK_ESTIMATING, AUDIT_DEP_CLOSURE).

Matrix-cell identity `EVALUATIVE × APPLYING` (from AGENTS.md) is preserved by this wrapper; method migration does not alter the agent's portal-cell role.

## See also
- `skills/dependency-extract/SKILL.md` — method contract
- `skills/dependency-extract/QA_CHECKS.md` — invariants + local quality checks
- `.Archive/SEMANTIC_PIPELINE_ARCHITECTURE.md` — C-pattern shell-on-shell rationale
