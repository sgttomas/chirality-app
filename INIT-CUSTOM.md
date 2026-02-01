# INIT-CUSTOM — Custom Session Initialization (Framework-Consistent)

## Standards & precedence (canonical)

- **Canonical standard:** `AGENT_HELPS_HUMANS.md`  
  Where any instruction or template conflicts with the canonical standard, **this file (and any downstream instructions) must be edited to conform to v2**.
- **Audit rubric:** `AUDIT_AGENT.md` (use it to check conformance across files)

## Layer model (0/1/2) — how to choose the right INIT

This repository uses a layered agent architecture:

- **Agent 0 / Type 0 (Architect):** defines and maintains canonical standards, contracts, and role boundaries.
- **Agent 1 / Type 1 (Manager):** interprets intent, decomposes work, writes briefs, routes to Specialists, and merges results.
- **Agent 2 / Type 2 (Specialist):** executes a narrow brief straight-through and returns outputs + evidence.

**Rule of thumb:**
- Use **INIT-PERSONA** for sessions that involve interpretation, orchestration, or multi-step planning (Type 0/1 behavior).
- Use **INIT-TASK** for direct execution by a Type 2 task agent.
- Use **INIT-CUSTOM** when you need a bespoke INIT but still want to remain framework-consistent.

Use this template when you need a **custom INIT** for a specialized workflow, but you want it to remain consistent with the framework’s operating approach.

This file is designed to help you (the human) create a custom INIT that:
- Defines **what exists and where** (work objects and paths),
- Defines **what counts as valid evidence** (sources and provenance),
- Defines **how work will be performed** (steps, write zones, outputs),
- Defines **what matters most** (success criteria and non-negotiables).

> This is a practical standard template. Fill it in and rename it for your session (e.g., `INIT-MYWORKFLOW.md`).

---

## 0) Session Header

**Date:** 2026-01-30  
**Custom INIT Name:** [e.g., `INIT-Estimate-Collation-PKG08`, `INIT-Docs-Refresh`, `INIT-Repo-Release`]  
**Invoker:** [Human name/handle]

---

## 1) Project Context (required)

**Project Name:** [ ]  
**Project Workspace (absolute):** [ ]  
**Execution Root (absolute):** [ ]  
**Decomposition File (absolute):** [path or `TBD`]

**Current Project State Notes (optional):**
- [What is “true now” about the project? e.g., “PKG-08 initialized; 4 docs drafted; estimates completed for 12 deliverables.”]

---

## 2) Agent Assignment (custom)

**Agent Name (existing or new):** [ ]  
**Agent Class (choose one):** `PERSONA | TASK | HYBRID`  
**Agent Instructions File (absolute):** [path or `TBD`]

**Write Scope (choose one):**
- `none`
- `deliverable-local`
- `tool-root-only`
- `repo-metadata-only`

**Tool Root (if writing):** [e.g., `execution/_Aggregation/`, `execution/_Estimates/`, `execution/_Reconciliation/`]

---

## 3) Ontology — Work Objects and Locations (required)

Define the objects this session will operate on.

**Objects in scope (choose what applies):**
- [ ] Packages (`PKG-*`)
- [ ] Deliverables (`DEL-*`)
- [ ] Deliverable artifacts (4 docs, semantic lens, dependencies register, estimate files)
- [ ] Project-level tool roots (aggregation, estimates, reconciliation)
- [ ] Repository state (git)

**Scope identifiers / paths:**
- Packages: [ ]
- Deliverables: [ ]
- Paths included: [ ]
- Paths excluded: [ ]

**Stable identifiers used (if any):**
- [e.g., `PKG-###`, `DEL-###`, `DEP-...`, line item keys]

---

## 4) Epistemology — Evidence and Validity (required)

Define what sources count and how claims are justified.

**Authoritative sources for this session:**
- [ ] Decomposition document
- [ ] Deliverable folder artifacts (`_CONTEXT`, `_STATUS`, 4 docs, etc.)
- [ ] Tool-root snapshots (aggregation, estimates)
- [ ] External references (list paths/URLs): [ ]

**Provenance required for outputs (minimum):**
- `SourcePath`
- `SectionRef` (best-effort)
- `Timestamp` or snapshot ID (if applicable)

**Unknown handling policy:**
- Use `TBD` (do not guess)
- Record assumptions explicitly (where?):
  - [ ] In a run log
  - [ ] In the output artifact
  - [ ] Both

**Conflict handling policy:**
- Do not silently resolve conflicts
- Surface contenders explicitly (conflicts/duplicates list)

---

## 5) Praxeology — Execution Plan (required)

Define how work will be performed.

**Run mode (choose one):**
- [ ] Read-only analysis
- [ ] Straight-through pipeline (writes outputs)
- [ ] Interactive session with approval gates

**Steps (high level, 5–12 bullets):**
1. [ ]
2. [ ]
3. [ ]

**Approval gates (if any):**
- [ ] Required before write actions
- [ ] Required before destructive actions
- Approval token format (if used): [ ]

**Snapshot policy (if writing):**
- Each run writes a new snapshot (no overwrite)
- Pointer files may be updated (e.g., `_LATEST.md`)

---

## 6) Axiology — Success Criteria and Non-Negotiables (required)

Define what “good” means for this session.

**Primary success artifacts (what must exist when done):**
- [ ]
- [ ]

**Quality checks (minimum):**
- Coverage: [what must be included]
- Schema validity: [required columns / structure]
- Provenance completeness: [expectations]
- Risk posture: [what must be surfaced]

**Non-negotiables:**
- [ ] No invention
- [ ] No source edits
- [ ] Tool-root-only writes
- [ ] Explicit decision capture
- [ ] Other: [ ]

---

## 7) Orientation Files (read before acting)

1. `[repo]/README.md`
2. `[repo]/AGENTS.md`
3. Agent instructions file
4. Decomposition file (if applicable)
5. Scope folders/files relevant to this session

---

---

## Quick Start Suggestions (prudent defaults)

Use these examples when you’re creating a custom workflow INIT. Keep them small, bounded, and rerunnable.

### QS-1: Custom rollup across a defined set (non-destructive)
```markdown
Agent Class: TASK
Write Scope: tool-root-only
Tool Root: execution/_Aggregation/
Ontology: Packages [PKG-###] / Deliverables [DEL-###]
Epistemology: sources are deliverable folders + prior snapshots; provenance required
Praxeology: scan → extract → collate → write snapshot → write coverage/QA
Axiology: completeness + traceability > elegance; surface conflicts; no silent fixes
```

### QS-2: Custom quality audit (coverage + schema compliance)
```markdown
Agent Class: TASK
Write Scope: tool-root-only
Tool Root: execution/_Reconciliation/
Scope: Packages [PKG-###]
Plan: inventory required artifacts → validate schemas → report missing/invalid → recommend fixes
Success: human gets a short punch list per deliverable
```

### QS-3: Custom publication readiness (no publishing)
```markdown
Agent Class: TASK
Write Scope: none
Scope: repo state only
Epistemology: git outputs are authoritative; no invention
Plan: diff vs upstream → group changes → identify risky/unintended paths → recommend options
```

### QS-4: Custom one-off extractor (register creation)
```markdown
Agent Class: TASK
Write Scope: tool-root-only
Tool Root: execution/_[YourToolRoot]/
Scope: Deliverables [DEL-###]
Plan: define schema → extract fields with SourcePath/SectionRef → write register + QA
```

## Start Instruction to Agent

**Agent:** Read this INIT-CUSTOM file fully. Then follow the assigned agent instructions (or execute the custom plan described here) within the defined write scope and constraints.  
**Operating stance:** Make scope explicit, preserve provenance, surface conflicts/gaps, and produce durable outputs that can be rerun safely.

Add these if your session involves agent design, orchestration, or auditing:

6. `[repo]/WHAT-IS-AN-AGENT.md` — Architecture philosophy (role boundaries, composition, debugging)
7. `[repo]/AGENT_HELPS_HUMANS.md` — Canonical standard (contracts, schemas, precedence)
8. `[repo]/AUDIT_AGENT.md` — Audit rubric (checklists + issue log)
