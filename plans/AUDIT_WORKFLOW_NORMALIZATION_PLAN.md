# Plan: Audit Workflow Normalization

## Context

The audit layer is currently represented as a family of standalone Type 2 agents:

- `AUDIT_AGENTS`
- `AUDIT_DECOMP`
- `AUDIT_DEP_CLOSURE`
- `AUDIT_EPISTEMIC`
- `AUDIT_GOVERNANCE`
- `AUDIT_HYPERGRAPH_CLOSURE`
- `AUDIT_SCOPE_CLOSURE`

Architecturally, these are bounded execution methods rather than distinct shells. They are therefore strong candidates to move behind the canonical `TASK` shell as skills.

At the same time, auditing is a genuinely human-facing workflow: scope selection, audit composition, finding interpretation, remediation prioritization, and rerun decisions are managerial tasks. That justifies a dedicated Type 1 manager if the audit workflow is promoted to a first-class human-facing path.

---

## Target Architecture

### New Type 1 manager

Introduce **`AUDIT`** as a Type 1 persona if audit orchestration is being promoted to a first-class workflow.

`AUDIT` should own:

- audit scope selection
- audit family selection
- batching/sequencing of audit runs
- synthesis of findings across multiple audit skills
- presentation of remediation priorities and rerun recommendations to the human

If added, `AUDIT` is the natural occupant of the currently empty `EVALUATIVE × APPLYING` cell in the architecture matrix.

### Type 2 execution path

Audit execution should run through `TASK` using skills:

- `audit-agents`
- `audit-decomp`
- `audit-dep-closure`
- `audit-epistemic`
- `audit-governance`
- `audit-hypergraph-closure`
- `audit-scope-closure`

### Tool boundary

Existing deterministic checks, parsers, and helper scripts remain tools. Skill migration must not absorb deterministic logic back into prose.

---

## Migration Rules

### Preserve first-pass outputs

The first migration should preserve:

- existing output roots
- existing report filenames
- existing machine-readable output schemas

The invocation path changes; the audit payloads should not.

### No new audit-specific shell

Do not introduce a new standalone Type 2 shell for auditing. If a skill needs special runtime guidance, encode it in:

- `BRIEF_SCHEMA.md`
- `TOOL_POLICY.md`
- `QA_CHECKS.md`
- deterministic tools

### Human-facing manager only if used as a workflow

If the project does not intend to expose audit as a first-class human-facing workflow, skip `AGENT_AUDIT.md` and migrate the audit methods directly into skills callable by existing managers. If the workflow is being elevated, add `AUDIT` explicitly.

Default for this plan: **add `AUDIT`**.

---

## Implementation Shape

### Phase 1 — Add `AUDIT` manager

- Create `agents/AGENT_AUDIT.md` as a Type 1 persona
- Define:
  - supported audit families
  - scope model
  - output/reporting responsibilities
  - dispatch rules to `TASK + TaskSkill`
- Update `AGENTS.md` and related matrix/governance docs

### Phase 2 — Create audit skills

Create one skill per existing audit method, initially mirroring current behavior:

- skill purpose and inputs track the current agent contract
- output schemas and write roots remain unchanged
- deterministic helper usage is moved into explicit tool policy

### Phase 3 — Update dispatch paths

- Update any human-facing or manager instructions that currently reference standalone audit Type 2 agents
- Route audit execution through `TASK + TaskSkill`

### Phase 4 — Archive legacy audit agents

- Archive the old `AGENT_AUDIT_*` instruction files once parity is confirmed
- Remove them from the live Type 2 index

---

## Verification

- A representative run of each migrated audit method produces the same output artifacts and equivalent findings as the legacy path.
- `AUDIT` can compose multiple audit skills in one human-facing workflow and return a coherent synthesis.
- No migrated audit method requires a standalone Type 2 shell to function.
- Audit skill docs pass the skill validator and expose explicit tool/QA contracts.

---

## Assumptions

- Audit workflows are sufficiently human-facing to justify a dedicated Type 1 manager.
- First-pass migration values architectural normalization over output redesign.
- The audit family is migrated as a coherent set rather than one agent at a time, to avoid dual invocation patterns lingering indefinitely.

---
