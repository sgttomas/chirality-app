# Plan: Evaluation Workflow Normalization

## Context

The repo already has a human-facing evaluation manager:

- `agents/AGENT_EVALUATION.md`

But evaluation execution still relies on standalone Type 2 specialists:

- `EVALUATION_REPORT`
- `EVALUATION_STRUCTURE_AUDIT`
- `EVALUATION_DEPENDENCY_AUDIT`

This creates the same mixed-state issue seen in the audit family: the manager is already Type 1, but the bounded execution methods are not yet normalized behind `TASK`.

---

## Target Architecture

### Keep `EVALUATION` as the manager

`EVALUATION` remains the human-facing Type 1 orchestrator for:

- evaluation scope selection
- dimension selection
- sequencing of digest generation and evaluation runs
- synthesis of scored outputs
- presentation of results to the human

No new Type 1 evaluation agent is needed.

### Move execution methods into skills

Replace standalone evaluation specialists with `TASK` skills:

- `evaluation-report`
- `evaluation-structure-audit`
- `evaluation-dependency-audit`

`content-digest` remains the existing supporting skill in the evaluation pipeline.

### Tool boundary

Deterministic evaluation helpers stay under `tools/`. The first migration should preserve current helper usage rather than redesign the tool layer.

---

## Migration Rules

### Preserve first-pass outputs

Keep unchanged where practical:

- report filenames
- output paths
- machine-readable result shapes
- deterministic helper invocation semantics

The first migration is about execution architecture, not evaluation-product redesign.

### One-to-one skill mapping first

Do not collapse multiple evaluation specialists into a single mega-skill in the first migration. Use one-to-one skill mappings so parity with the current system is easy to prove:

- `EVALUATION_REPORT` -> `evaluation-report`
- `EVALUATION_STRUCTURE_AUDIT` -> `evaluation-structure-audit`
- `EVALUATION_DEPENDENCY_AUDIT` -> `evaluation-dependency-audit`

Potential later consolidation is a separate decision.

---

## Implementation Shape

### Phase 1 — Create evaluation skills

Create three new skills that mirror the current specialist contracts:

- inputs and runtime overrides derived from the current INIT-TASK contracts
- outputs preserve the current report roots and schemas
- tool usage moved into explicit skill/tool contracts

### Phase 2 — Update `EVALUATION`

Rewrite `EVALUATION` dispatch logic to use:

- `TASK + content-digest`
- `TASK + evaluation-report`
- `TASK + evaluation-structure-audit`
- `TASK + evaluation-dependency-audit`

The orchestration logic stays in `EVALUATION`; only the bounded specialists move.

### Phase 3 — Archive legacy evaluation specialists

Once parity is verified:

- archive `AGENT_EVALUATION_REPORT.md`
- archive `AGENT_EVALUATION_STRUCTURE_AUDIT.md`
- archive `AGENT_EVALUATION_DEPENDENCY_AUDIT.md`
- remove them from the live Type 2 inventory

---

## Verification

- `EVALUATION` can run end-to-end using only `TASK`-dispatched skills for bounded execution.
- Representative evaluation runs produce equivalent reports to the current path.
- The new skills validate successfully and explicitly document tool usage and QA checks.
- No human-facing functionality is lost during the migration.

---

## Assumptions

- `EVALUATION` remains the single Type 1 manager for evaluation workflows.
- First-pass migration preserves outputs and concentrates on normalization of execution path.
- `content-digest` stays in place as an existing supporting skill rather than being redesigned as part of this slice.

---
