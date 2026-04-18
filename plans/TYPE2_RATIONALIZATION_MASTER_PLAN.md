# Plan: Type 2 Rationalization Toward `TASK` + Skills + Tools

## Context

The repo is in a mixed architectural state.

The intended direction is already visible in:

- `agents/AGENT_TASK.md` — `TASK` as the canonical bounded-task shell
- `agents/AGENT_SKILLMAKER.md` — method logic belongs in skills, deterministic logic in tools
- `AGENTS.md` — prior wrapper methods already moved behind `TASK + TaskSkill`

At the same time, the live Type 2 inventory still contains a mix of:

- the canonical shell (`TASK`)
- a built-in compatibility profile (`DELIVERABLE_TASK`)
- grandfathered ORCHESTRATOR-pipeline specialists
- standalone method-heavy Type 2 agents that are better expressed as `TASK` skills

This plan defines the end state and the migration rules.

---

## Target End State

### Core model

- **`TASK` remains the canonical Type 2 shell.**
- **Profiles remain few.** `DELIVERABLE_TASK` stays as a compatibility profile unless and until a narrower replacement exists.
- **Skills own method contracts.** Bounded execution methods move into repo-native skill folders under `skills/`.
- **Tools own deterministic transforms and checks.** No new method-heavy agent files should be created where a tool or skill is sufficient.
- **Type 1 agents own human-facing orchestration.** Human scope selection, batching, run composition, consolidation, and gate-controlled decision loops remain Type 1 responsibilities.

### Grandfathered exception

The existing `ORCHESTRATOR` pipeline stays intact. Its retained subordinate Type 2 path is treated as a grandfathered operational spine rather than the default model for new work.

### Governance rule for new work

No new standalone Type 2 instruction files should be introduced unless they represent:

1. a genuinely new shell-level execution substrate, or
2. a true profile-level specialization of `TASK`, not merely method prose.

If the behavior is primarily about **how** bounded work is performed, it should be a skill. If it is deterministic, it should be a tool.

---

## Current Type 2 Inventory and Disposition

| Current Item | Current Role | Target State | Disposition |
|--------------|--------------|--------------|-------------|
| `TASK` | Canonical bounded-task shell | Retained | Keep as the single canonical Type 2 shell |
| `DELIVERABLE_TASK` | Built-in compatibility profile | Retained as profile | Keep, but do not expand with new method behavior |
| `PREPARATION` | ORCHESTRATOR subordinate scaffold shell | Grandfathered exception | Keep as part of the preserved ORCHESTRATOR pipeline |
| `AGGREGATION` | ORCHESTRATOR subordinate synthesis shell | Grandfathered exception | Keep as part of the preserved ORCHESTRATOR pipeline |
| `DOMAIN_HYPERGRAPH` | ORCHESTRATOR subordinate hypergraph shell | Grandfathered exception | Keep as part of the preserved ORCHESTRATOR pipeline |
| `AUDIT_AGENTS` | Method-heavy audit specialist | Replace with skill | Migrate to `TASK + audit-agents` under a human-facing audit workflow |
| `AUDIT_DECOMP` | Method-heavy audit specialist | Replace with skill | Migrate to `TASK + audit-decomp` |
| `AUDIT_DEP_CLOSURE` | Method-heavy audit specialist | Replace with skill | Migrate to `TASK + audit-dep-closure` |
| `AUDIT_EPISTEMIC` | Method-heavy audit specialist | Replace with skill | Migrate to `TASK + audit-epistemic` |
| `AUDIT_GOVERNANCE` | Method-heavy audit specialist | Replace with skill | Migrate to `TASK + audit-governance` |
| `AUDIT_HYPERGRAPH_CLOSURE` | Method-heavy audit specialist | Replace with skill | Migrate to `TASK + audit-hypergraph-closure` |
| `AUDIT_SCOPE_CLOSURE` | Method-heavy audit specialist | Replace with skill | Migrate to `TASK + audit-scope-closure` |
| `EVALUATION_REPORT` | Evaluation execution specialist | Replace with skill | Migrate under `EVALUATION` as `TASK + evaluation-report` |
| `EVALUATION_STRUCTURE_AUDIT` | Evaluation execution specialist | Replace with skill | Migrate under `EVALUATION` as `TASK + evaluation-structure-audit` |
| `EVALUATION_DEPENDENCY_AUDIT` | Evaluation execution specialist | Replace with skill | Migrate under `EVALUATION` as `TASK + evaluation-dependency-audit` |

---

## Migration Principles

### Output compatibility first

For first-pass migrations:

- preserve current artifact roots
- preserve current output schemas
- preserve existing report filenames where practical

The first migration goal is architectural normalization, not output redesign.

### Archive only after parity

Legacy Type 2 agent files are archived only after:

- the replacement skill path exists
- the owning Type 1 workflow is updated
- cross-references are updated
- output parity is verified on representative runs

### Documentation update is part of each migration

Every migrated family must update:

- `AGENTS.md`
- any affected Type 1 manager instructions
- the relevant skill docs
- any plan docs that reference the old agent names

---

## Migration Sequence

### Phase 1 — Planning and governance alignment

- Refactor `docs/PLAN.md` into a thin roadmap/index
- Add the new rationalization plans
- Record the end-state rules in the planning corpus before code migration begins

### Phase 2 — Audit workflow normalization

- Add a human-facing audit manager if the repo adopts one
- Migrate the `AUDIT_*` family into `TASK` skills
- Archive the old standalone Type 2 audit agents after parity

### Phase 3 — Evaluation workflow normalization

- Keep `EVALUATION` as the Type 1 manager
- Migrate the `EVALUATION_*` Type 2 specialists into `TASK` skills
- Archive the old standalone evaluation agents after parity

### Phase 4 — Inventory and architecture cleanup

- Update `AGENTS.md` inventory and any matrix language affected by the reduced standalone Type 2 set
- Reconcile DBM / thesis / frontend selector docs with the new normalized Type 2 layer

---

## Acceptance Criteria

- `TASK` is the default and explicit execution shell for all new bounded specialist workflows.
- No new remnant-style standalone Type 2 method agents are introduced.
- Outside the grandfathered ORCHESTRATOR path, remaining method-heavy Type 2 agents are either:
  - migrated into skills, or
  - justified as true shell/profile exceptions.
- Audit and evaluation migration paths are documented and decision-complete before implementation begins.

---

## Assumptions

- The working `ORCHESTRATOR` pipeline is preserved rather than rewritten as part of this normalization.
- `DELIVERABLE_TASK` remains a compatibility profile during this migration window.
- Architectural cleanliness is the main driver; output schema redesign is explicitly out of scope for first-pass migration.

---
