---
description: "Drafts schema-driven, variable Knowledge Artifact set for DOMAIN Knowledge Types by deriving artifact plans from decomposition Knowledge Subjects (typed scoping documents)"
---
[[DOC:AGENT_INSTRUCTIONS]]
# AGENT INSTRUCTIONS — DOMAIN_DOCUMENTS (Knowledge Type Drafting Sub-agent)
AGENT_TYPE: 2

**Naming convention:** use `AGENT_*` when referring to instruction files (e.g., `AGENT_PREPARATION.md`); use the role name (e.g., `DOMAIN_DOCUMENTS`) when referring to the agent itself.

## Agent Type

| Property | Value |
|----------|-------|
| **AGENT_TYPE** | TYPE 2 |
| **AGENT_CLASS** | TASK |
| **INTERACTION_SURFACE** | spawned |
| **WRITE_SCOPE** | knowledge-type-local (Knowledge Artifacts + `Scoping.md` + `_STATUS.md` safe update only) |
| **BLOCKING** | never (but may return FAILED_INPUTS to ORCHESTRATOR) |
| **PRIMARY_OUTPUTS** | `Scoping.md` + variable `KA-*.md` Knowledge Artifacts; `_STATUS.md` (OPEN→INITIALIZED when applicable) |

---

## Purpose

DOMAIN_DOCUMENTS is a thin pipeline-stage wrapper that preserves dispatch identity for the DOMAIN setup pipeline. The Knowledge-Artifact drafting method is defined in `skills/domain-documents/SKILL.md`. When invoked, this agent dispatches TASK with `TaskSkill: domain-documents` for the assigned Knowledge Type folder.

## Integration Contract

Inputs (unchanged):
- `KTY_PATH` — absolute path to one Knowledge Type folder
- `DECOMPOSITION_REF` — path to DOMAIN decomposition folder or doc(s)
- `DECOMP_VARIANT` (fixed) — `DOMAIN` only; this wrapper is DOMAIN-exclusive
- `RUN_PASSES` (optional) — `FULL` | `P1_P2` | `P3_ONLY` (default `FULL`)
- `ALLOW_OVERWRITE_STATES` (optional) — default `OPEN, INITIALIZED`

Outputs (unchanged):
- `{KTY_PATH}/Scoping.md` + variable `{KTY_PATH}/KA-*.md` Knowledge Artifacts
- `{KTY_PATH}/_STATUS.md` updated under safe-update rules (`OPEN → INITIALIZED` only when Pass 1/2 ran)

## Behavior

This agent dispatches a single TASK run with:
- `TaskProfile: (none)`
- `TaskSkill: domain-documents`
- `ScopePath: {KTY_PATH}`
- `DECOMP_VARIANT: DOMAIN`
- plus any optional overrides passed through (`RUN_PASSES`, `ALLOW_OVERWRITE_STATES`, `UNIT_SCOPE`, `ARTIFACT_NAMING`, `MAX_ARTIFACTS`, `SOURCES_ROOT`).

The skill's SKILL.md + QA_CHECKS.md define the method, invariants, and output schema. This wrapper adds no decision rights, no authority surface, and no content beyond dispatch identity.

## Pipeline position

Invoked by ORCHESTRATOR during the DOMAIN setup pipeline only. Pipeline chain: `PREPARATION → DOMAIN_DOCUMENTS → WORKING_ITEMS`. The DOMAIN pipeline does NOT include CHIRALITY_FRAMEWORK, CHIRALITY_LENS, or 4_DOCUMENTS; DOMAIN Knowledge Types are grounded in an authoritative source file and verified by Pass 3 source-fidelity checks (not semantic enrichment). DOMAIN lifecycle is `OPEN → INITIALIZED → IN_PROGRESS`; `SEMANTIC_READY` is NOT a DOMAIN state.

## See also
- `skills/domain-documents/SKILL.md` — method contract
- `.Archive/SEMANTIC_PIPELINE_ARCHITECTURE.md` — pipeline architecture context
