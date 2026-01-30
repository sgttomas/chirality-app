# INIT-TASK — Session Initialization (Task Agent)

Use this INIT file when you want to run a **task agent directly**. Task agents should execute a bounded assignment straight-through, producing durable, auditable outputs (typically into a tool root) without requiring mid-run human decisions.

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
- [ ] `PROJECT_DECOMP` — create/repair a project decomposition from messy scope inputs
- [ ] `PREPARATION` — scaffold execution workspace + minimum viable filesets
- [ ] `4_DOCUMENTS` — generate initial drafts (Datasheet/Spec/Guidance/Procedure)
- [ ] `CHIRALITY_FRAMEWORK` — generate `_SEMANTIC.md` semantic lens per deliverable
- [ ] `DEPENDENCIES` — extract emergent dependencies into a trackable register
- [ ] `RECONCILIATION` — cross-deliverable coherence checks (read-only posture)
- [ ] `AGGREGATION` — synthesize/collate across files into snapshots (e.g., estimates + BoE)
- [ ] `CHANGE` (git state) — inspect git diffs + optional git actions with explicit approval

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
3. Selected task agent instructions
4. Decomposition file (if applicable)
5. Scope folders/files (if applicable)

---

---

## Quick Start Suggestions (prudent defaults)

Use one of these short blocks to run a common task agent workflow. Edit bracketed fields.

### QS-1: Create/repair a project decomposition (foundation)
```markdown
Assigned Task Agent: PROJECT_DECOMP
Task Summary: Create/repair decomposition from current SOW and references
Inputs Available: [attach/paste SOW, links, notes]
Expected Output Artifacts: Decomposition doc + Scope Ledger + Coverage summary
```

### QS-2: Scaffold workspace (folders + minimum viable files)
```markdown
Assigned Task Agent: PREPARATION
Task Summary: Create execution scaffolding and minimum viable filesets for scoped deliverables
Scope: Packages: [PKG-###]  Deliverables: [optional]
Expected Output Location: [execution root]
```

### QS-3: Generate initial 4 documents for a package or deliverable set
```markdown
Assigned Task Agent: 4_DOCUMENTS
Task Summary: Draft Datasheet/Specification/Guidance/Procedure for scoped deliverables
Scope: Packages: [PKG-###] or Deliverables: [DEL-###]
Constraints: Use project templates; leave unknowns as TBD; cite sources
```

### QS-4: Generate semantic lens artifacts
```markdown
Assigned Task Agent: CHIRALITY_FRAMEWORK
Task Summary: Generate _SEMANTIC.md for each scoped deliverable to guide WORKING_ITEMS
Scope: Packages: [PKG-###] or Deliverables: [DEL-###]
Expected Outputs: _SEMANTIC.md in each deliverable folder
```

### QS-5: Extract dependencies into a trackable register
```markdown
Assigned Task Agent: DEPENDENCIES
Task Summary: Discover and record dependencies emerging from the 4 documents
Scope: Packages: [PKG-###] or Deliverables: [DEL-###]
Expected Outputs: Dependencies register + coverage report
```

### QS-6: Aggregate estimates + BoE + risks/assumptions (deliverable-by-deliverable recommended)
```markdown
Assigned Task Agent: AGGREGATION
Task Summary: Collate Estimate + Basis of Estimate + Risks + Assumptions into aggregation snapshots
Scope: Deliverables: [DEL-###] (repeat per deliverable / per package)
Expected Output Location: [execution/_Aggregation/...]
Constraints: Treat missing items as TBD; preserve provenance; surface duplicates/conflicts
```

### QS-7: Stage-gate coherence check (read-only)
```markdown
Assigned Task Agent: RECONCILIATION
Task Summary: Run cross-deliverable coherence checks for a stage gate
Scope: Packages: [PKG-###]
Constraints: Read-only; produce findings + issues list; no edits
```

### QS-8: Git state check (and optionally execute actions with approval)
```markdown
Assigned Task Agent: CHANGE (git state)
Task Summary: Summarize differences vs upstream and advise what it signifies
ALLOW_EXECUTION: [FALSE | TRUE]
Constraints: Execute only after explicit APPROVE token
```

## Start Instruction to Agent

**Agent:** Read this INIT-TASK file fully, then execute the assigned task agent instructions for the given scope.  
**Operating stance:** Straight-through, bounded scope, provenance-first, no invention, and report coverage/QA/conflicts as outputs.
