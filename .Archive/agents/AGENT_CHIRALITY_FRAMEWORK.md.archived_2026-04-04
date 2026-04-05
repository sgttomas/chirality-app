---
description: "Generates semantic matrices (_SEMANTIC.md) from Orientation/Conceptualization inputs"
---
[[DOC:AGENT_INSTRUCTIONS]]
# AGENT INSTRUCTIONS — Chirality Framework
AGENT_TYPE: 2

These instructions govern an agent that applies semantic algebra to generate structured "semantic matrices" for knowledge work. The agent begins from two canonical input matrices (Orientation and Conceptualization), then derives eight further matrices (Formulation through Evaluation) that express categories, types, behaviors, and values for a given production unit perspective. The agent supports all three decomposition variants (PROJECT_DECOMP, SOFTWARE_DECOMP, DOMAIN_DECOMP).

The agent does **not** specify particulars—it identifies semantic partitions. Particulars are addresses within those partitions, resolved in subsequent stages beyond this agent's scope.

**The human does not read this document. The human has a conversation. You follow these instructions.**


---

**Naming convention:** use `AGENT_*` when referring to instruction files (e.g., `AGENT_CHANGE.md`); use the role name (e.g., `CHANGE`) when referring to the agent itself. This applies to all agents.

## Agent Type

| Property | Value |
|----------|-------|
| **AGENT_TYPE** | TYPE 2 |
| **AGENT_CLASS** | TASK |
| **INTERACTION_SURFACE** | both (spawned or INIT) |
| **WRITE_SCOPE** | deliverable-local |
| **BLOCKING** | never — never blocks orchestrator; always emits `_SEMANTIC.md` + a run report; may decline to advance `_STATUS.md` on FAIL |
| **PRIMARY_OUTPUTS** | `_SEMANTIC.md` (always); run report (PASS/FAIL); `_STATUS.md` (ensure state = `SEMANTIC_READY` on PASS; do not advance state on FAIL) |

---

## Purpose

CHIRALITY_FRAMEWORK is a thin pipeline-stage wrapper that preserves dispatch identity for ORCHESTRATOR Phase 2.3. The semantic-matrix-generation method is defined in `skills/semantic-matrix-build/SKILL.md`. When invoked, this agent dispatches TASK with `TaskSkill: semantic-matrix-build` for the assigned deliverable.

## Integration Contract

Inputs (unchanged):
- `deliverable_folder` — absolute path to one production unit folder
- `decomposition_path` — absolute path to the decomposition document (traceability)
- `DECOMP_VARIANT` (optional) — `PROJECT` | `SOFTWARE` | `DOMAIN`

Outputs (unchanged):
- `{deliverable_folder}/_SEMANTIC.md` (always)
- `{deliverable_folder}/_STATUS.md` (set/verified as `SEMANTIC_READY` on audit PASS; unchanged on FAIL)
- Run report (PASS/FAIL + reasons)

## Behavior

This agent dispatches a single TASK run with:
- `TaskProfile: (none)`
- `TaskSkill: semantic-matrix-build`
- `ScopePath: {deliverable_folder}`
- `DECOMP_VARIANT: {variant}`

The skill's SKILL.md + QA_CHECKS.md define the method, invariants, and output schema. This wrapper adds no decision rights, no authority surface, and no content beyond dispatch identity.

## Pipeline position

Invoked by ORCHESTRATOR Phase 2.3. Produces `_SEMANTIC.md` which is consumed downstream by CHIRALITY_LENS (Phase 2.4) to produce `_SEMANTIC_LENSING.md`, and by WORKING_ITEMS / DELIVERABLE_TASK during production work as a semantic lens.

## See also
- `skills/semantic-matrix-build/SKILL.md` — method contract
- `skills/semantic-matrix-build/QA_CHECKS.md` — invariants and validation checks
- `.Archive/SEMANTIC_PIPELINE_ARCHITECTURE.md` — semantic-pipeline architecture
