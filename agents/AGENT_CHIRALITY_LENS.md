---
description: "Applies semantic lensing to produce _SEMANTIC_LENSING.md from matrices and production documents"
---
[[DOC:AGENT_INSTRUCTIONS]]
# AGENT INSTRUCTIONS — Chirality Lens (CHIRALITY_LENS)
AGENT_TYPE: 2

**Naming convention:** use `AGENT_*` when referring to instruction files (e.g., `AGENT_CHIRALITY_LENS.md`); use the role name (e.g., `CHIRALITY_LENS`) when referring to the agent itself. This applies to all agents.

## Agent Type

| Property | Value |
|---|---|
| **AGENT_TYPE** | TYPE 2 |
| **AGENT_CLASS** | TASK |
| **INTERACTION_SURFACE** | spawned or INIT-TASK |
| **WRITE_SCOPE** | deliverable-local |
| **BLOCKING** | never |
| **PRIMARY_OUTPUTS** | `_SEMANTIC_LENSING.md` |

---

## Purpose

CHIRALITY_LENS is a thin pipeline-stage wrapper that preserves dispatch identity for ORCHESTRATOR Phase 2.4. The lensing method is defined in `skills/lens-register/SKILL.md`. When invoked, this agent dispatches TASK with `TaskSkill: lens-register` for the assigned deliverable.

## Integration Contract

Inputs (unchanged):
- `deliverable_folder` — absolute path to one production unit folder
- `DECOMP_VARIANT` (optional) — `PROJECT` | `SOFTWARE` (default `PROJECT`). DOMAIN is not supported; DOMAIN pipelines skip this step.

Outputs (unchanged):
- `{deliverable_folder}/_SEMANTIC_LENSING.md`

## Behavior

This agent dispatches a single TASK run with:
- `TaskProfile: (none)`
- `TaskSkill: lens-register`
- `ScopePath: {deliverable_folder}`
- `DECOMP_VARIANT: {variant}`

The skill's SKILL.md + QA_CHECKS.md define the method, invariants, and output schema. This wrapper adds no decision rights, no authority surface, and no content beyond dispatch identity.

## Pipeline position

Invoked by ORCHESTRATOR Phase 2.4. Produces `_SEMANTIC_LENSING.md` which is consumed by 4_DOCUMENTS Pass 3 (Phase 2.5) and optionally by DELIVERABLE_TASK with `UseSemanticLensing: true` (via `skills/semantic-lensing/`).

## See also
- `skills/lens-register/SKILL.md` — method contract
- `skills/semantic-lensing/SKILL.md` — interactive proposal workflow consuming the register
- `plans/SEMANTIC_PIPELINE_ARCHITECTURE.md` — two-contract architecture
