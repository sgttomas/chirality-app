# INIT-TASK — Session Initialization (Task Agent)

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

Use this INIT file when you want to run a **Type 2 task agent directly**. Task agents should execute a bounded assignment straight-through, producing durable, auditable outputs (typically into a tool root) without requiring mid-run human decisions. Use **INIT-PERSONA** for **Type 0 / Type 1** agents.

---

## 0) Session Header

**Date:** 2026-01-30  
**Session Name:** [Short label, e.g., `Aggregate PKG-08 estimates`, `Generate 4 docs for PKG-07`, `Dependency extraction DEL-14.03`]  
**Invoker:** [Human name/handle]

---

## 1) Project Context

**Project Name:** [ ]  
**Project Workspace (absolute):** [ ]  
**Execution Root (absolute):** [ ]  
**Decomposition File (absolute):** [path or `TBD`]

**Key Reference Documents (paths):**
- [ ]
- [ ]

---

## 2) Task Agent Selection

**Assigned Task Agent (choose exactly one):**
- [ ] `PREPARATION` — scaffold execution workspace + minimum viable filesets
- [ ] `4_DOCUMENTS` — generate initial drafts (Datasheet/Spec/Guidance/Procedure)
- [ ] `CHIRALITY_FRAMEWORK` — generate `_SEMANTIC.md` semantic lens per deliverable
- [ ] `DEPENDENCIES` — extract emergent dependencies into a trackable register
- [ ] `RECONCILIATION` — cross-deliverable coherence checks (read-only posture)
- [ ] `AGGREGATION` — synthesize/collate across files into snapshots (e.g., estimates + BoE)

**Agent Instructions File (absolute):**  
[Path to the relevant `AGENT_*.md` instructions file.]

---

## 3) Task Definition

**Task Summary (one sentence):**  
[What to accomplish.]

**Scope (be explicit):**
- Packages: [ ]
- Deliverables: [ ]
- Paths included: [ ]
- Paths excluded: [ ]

**Inputs Available:**
- [ ] Decomposition exists
- [ ] Deliverable folders exist
- [ ] Four docs exist
- [ ] Estimates exist (Detail + BoE + risks/assumptions)
- [ ] Tool roots exist
- [ ] Other: [ ]

---

## 4) Output Contract (what must exist when done)

**Expected Output Location (absolute):**  
[Usually a tool root like `execution/_Aggregation/...` or `execution/_Estimates/...`]

**Expected Output Artifacts (list):**
- [ ]
- [ ]

**Success Criteria (short):**
- [ ]
- [ ]

---

## 5) Execution Constraints

- [ ] Read-only mode (no writes)
- [ ] Tool-root-only writes (recommended)
- [ ] Single deliverable only
- [ ] Single package only
- [ ] Project-wide scope
- [ ] Other: [ ]

---

## 6) Approval Controls (only if applicable)

If the task involves optional execution (e.g., git actions), define approval posture:

**ALLOW_EXECUTION:** [TRUE/FALSE]  
**Approval Rule:** [e.g., “Only execute after explicit APPROVE token”]

---

## 7) Orientation Files (read before acting)

1. `[repo]/README.md`
2. `[repo]/AGENTS.md`
3. Selected task agent instructions (must conform to `AGENT_HELPS_HUMANS.md`)
4. Decomposition file (if applicable)
5. Scope folders/files (if applicable)

---
