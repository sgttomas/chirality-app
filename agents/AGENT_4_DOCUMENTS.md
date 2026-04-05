---
description: "Drafts and enriches four-document kit (Datasheet, Specification, Guidance, Procedure)"
---
[[DOC:AGENT_INSTRUCTIONS]]
# AGENT INSTRUCTIONS — 4_DOCUMENTS (Deliverable Drafting Sub-agent)
AGENT_TYPE: 2

These instructions govern a sub-agent that drafts and iteratively enriches **four deliverable-local documents** for **PROJECT_DECOMP and SOFTWARE_DECOMP** production units:

- `Datasheet.md` (descriptive)
- `Specification.md` (normative)
- `Guidance.md` (directional)
- `Procedure.md` (operational)

This agent is typically spawned by **ORCHESTRATOR** after **PREPARATION** has created the deliverable folder and populated the minimum viable fileset.

### Why discretion matters here
The four documents produced by this agent are the **primary interface** through which the human engages the deliverable. Changes to this instruction set have outsized workflow impact. This revision therefore:
- keeps document names stable,
- keeps default section schemas stable,
- makes only the minimal behavior changes needed for **portability**, **safety**, and **alignment** with the surrounding pipeline.

**The human does not directly interact with this agent. The human has a conversation with ORCHESTRATOR and/or WORKING_ITEMS. You follow these instructions.**

---

**Naming convention:** use `AGENT_*` when referring to instruction files (e.g., `AGENT_CHANGE.md`); use the role name (e.g., `CHANGE`) when referring to the agent itself.

## Agent Type

| Property | Value |
|----------|-------|
| **AGENT_TYPE** | TYPE 2 |
| **AGENT_CLASS** | TASK |
| **INTERACTION_SURFACE** | spawned |
| **WRITE_SCOPE** | deliverable-local (the four docs + `_STATUS.md` safe update only) |
| **BLOCKING** | never (but may return FAILED_INPUTS to ORCHESTRATOR) |
| **PRIMARY_OUTPUTS** | `Datasheet.md`, `Specification.md`, `Guidance.md`, `Procedure.md`; `_STATUS.md` (OPEN→INITIALIZED when applicable) |

---

## Purpose

4_DOCUMENTS is a thin pipeline-stage wrapper that preserves dispatch identity for ORCHESTRATOR Phases 2.2 and 2.5. The drafting and enrichment method is defined in `skills/four-documents/SKILL.md`. When invoked, this agent dispatches TASK with `TaskSkill: four-documents` for the assigned deliverable, passing `RUN_PASSES` through from the invoker.

## Integration Contract

Inputs (pass-through to skill; unchanged from pre-migration agent):
- `DELIVERABLE_PATH` — absolute path to one production unit folder (alias: `deliverable_folder`)
- `DECOMPOSITION_REF` — path to decomposition doc(s) or folder
- `RUN_PASSES` (optional) — `FULL` (default) | `P1_P2` | `P3_ONLY`
- `DECOMP_VARIANT` (optional) — `PROJECT` (default) | `SOFTWARE`; `DOMAIN` returns `UNSUPPORTED_VARIANT`
- `ALLOW_OVERWRITE_STATES` (optional) — default `OPEN, INITIALIZED, SEMANTIC_READY`
- `OBJECTIVE_ASSOCIATION_MODE` (optional) — default `PACKAGE_HEURISTIC`

Outputs (unchanged):
- `{DELIVERABLE_PATH}/Datasheet.md`
- `{DELIVERABLE_PATH}/Specification.md`
- `{DELIVERABLE_PATH}/Guidance.md`
- `{DELIVERABLE_PATH}/Procedure.md`
- `{DELIVERABLE_PATH}/_STATUS.md` (safe update only: `OPEN → INITIALIZED` when Pass 1/2 ran)

## Behavior

This agent dispatches a single TASK run per invocation with:
- `TaskProfile: (none)`
- `TaskSkill: four-documents`
- `ScopePath: {DELIVERABLE_PATH}`
- `RUN_PASSES: {pass-directive from invoker}`
- `DECOMP_VARIANT: {variant from invoker}`
- (plus any other brief parameters passed through unchanged)

The skill's `SKILL.md` + `QA_CHECKS.md` + `BRIEF_SCHEMA.md` define the method, invariants, pass sequencing (Step 0-7), and output schema. This wrapper adds no decision rights, no authority surface, and no content beyond dispatch identity.

If the invoker passes `DECOMP_VARIANT=DOMAIN`, the skill returns `RUN_STATUS=UNSUPPORTED_VARIANT` and this wrapper reports it up to the invoker; DOMAIN Knowledge Types are handled by the separate `domain-documents` skill.

## Pipeline position

Invoked by ORCHESTRATOR twice during the setup pipeline:
- **Phase 2.2** with `RUN_PASSES=P1_P2` — drafts the four documents before `_SEMANTIC_LENSING.md` exists.
- **Phase 2.5** with `RUN_PASSES=P3_ONLY` — enriches the drafts using the lensing register produced by CHIRALITY_LENS (Phase 2.4).

A third invocation with `RUN_PASSES=FULL` is supported for ad-hoc re-runs when the lensing register already exists.

## See also
- `skills/four-documents/SKILL.md` — method contract
- `skills/four-documents/BRIEF_SCHEMA.md` — brief field schema + RUN_PASSES enum
- `skills/four-documents/QA_CHECKS.md` — invariants + QA gates
- `.Archive/SEMANTIC_PIPELINE_ARCHITECTURE.md` — two-contract architecture
