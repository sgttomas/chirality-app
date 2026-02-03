# INIT-PERSONA — Session Initialization (Persona Agent)

Use this INIT file when you want to start a **human-facing session** with a **Type 0 or Type 1 agent**. These agents are conversational interfaces that help you steer work, interpret outputs, and decide what to do next in the context of the full project system. Use **INIT-TASK** for **Type 2** (bounded task) agents.


**Layer mapping (Type 0 / Type 1 / Type 2):**
- **Type 0 (Architect):** maintains the canonical standards/contracts for the agent system (e.g., `AGENT_HELPS_HUMANS.md`). Use when you are changing the system itself.
- **Type 1 (Manager):** runs the human-facing session: interprets intent, decomposes work, writes briefs, routes to Type 2 specialists, and synthesizes results.
- **Type 2 (Specialist):** executes a bounded brief and returns outputs + evidence; does not redefine global policy/contracts.


> **Personas:** `HELP_HUMAN`, `HELPS_HUMANS`, `CHIRALITY-APP`, `PROJECT_DECOMP`, `ORCHESTRATOR`, `WORKING_ITEMS`, `PROJECT_CONTROLS`

---

## 0) Session Header

**Date:** 2026-01-30  
**Session Name:** [Short label, e.g., `PKG-08 kickoff`, `DEL-14.03 work session`, `Estimate review`]  
**Invoker:** [Human name/handle]

---

## 1) Project Context

**Project Name:** [e.g., Canola Oil Transload Facility]  
**Project Workspace (absolute):** [e.g., `/Users/ryan/ai-env/projects/chirality-app-test/test/`]  
**Execution Root (absolute):** [e.g., `/Users/ryan/ai-env/projects/chirality-app-test/test/execution/`]  
**Decomposition File (absolute):** [path or `TBD`]

**Repository Root (absolute, optional):** [path]  
**Current Branch (optional):** [e.g., `main`, `feature/...`]

**Key Reference Documents (paths):**
- [ ]
- [ ]
- [ ]

---

## 2) Persona Selection

**Selected Persona (choose exactly one):**
- [ ] `HELP_HUMAN` — scoped briefs, checklists, next-step guidance
- [ ] `HELPS_HUMANS` — workflow design standards and agent instruction guidance
- [ ] `PROJECT_DECOMP` — interactive decomposition from messy SOW (gate-controlled)
- [ ] `ORCHESTRATOR` — project control plane: initialize/scan state, coordinate pipelines
- [ ] `WORKING_ITEMS` — focused production session on a deliverable (human-in-the-loop)
- [ ] `PROJECT_CONTROLS` — interactive control plane; invokes Type 2 pipelines (e.g., ESTIMATING)
- [ ] `CHANGE` — manage the state of the files; reconcile dependencies across deliverables.


---

## 3) Session Goals and Decisions

**Goal (one sentence):**  
[What you want to accomplish by the end of this session.]

**Decisions you expect to make (if any):**
- [ ] Scope boundary / priorities
- [ ] Coordination representation choice (schedule/declared/full graph)
- [ ] Acceptance of a deliverable / stage gate
- [ ] What gets estimated / what gets aggregated
- [ ] What gets published (git)
- [ ] Other: [ ]

**Non-decisions (explicitly out of scope for this session):**
- [ ]

---

## 4) Scope

**Scope Type (choose one):**
- [ ] Single deliverable
- [ ] Single package
- [ ] Multiple packages
- [ ] Whole project

**In-Scope IDs / Paths:**
- Packages: [e.g., `PKG-08`]
- Deliverables: [e.g., `DEL-14.03`]
- Paths: [absolute paths if needed]

**Out-of-Scope (explicit exclusions):**
- [ ]

---

## 5) Inputs Available

Check what exists now (best-effort):

- [ ] Decomposition exists and is current
- [ ] Workspace scaffolded (execution root exists)
- [ ] Deliverable folders exist
- [ ] 4 documents exist for deliverables
- [ ] `_SEMANTIC.md` exists (semantic lens)
- [ ] Estimates exist (Detail + BoE + risks/assumptions)
- [ ] Aggregation tool root exists (`execution/_Aggregation/`)
- [ ] Reconciliation tool root exists (`execution/_Reconciliation/`)
- [ ] Other: [ ]

If uncertain, state it here:
- [ ]

---

## 6) Expected Outputs (what should exist when done)

Persona sessions may produce:
- A clear next-step plan and scoping choices
- A draft `INIT-TASK` brief for a task agent run (optional)
- A short checklist for the human (optional)
- A decision list (what was decided, what remains open)

**Outputs you want from this session:**
- [ ]
- [ ]

---

## 7) Optional: Task Invocations Requested

If you want this persona to trigger task work, list requested task invocations here. The persona should translate these into bounded task briefs.

- Task agent name: [ ]  
  Scope: [ ]  
  Desired outputs: [ ]

- Task agent name: [ ]  
  Scope: [ ]  
  Desired outputs: [ ]

---

## 8) Orientation Files (read before acting)

1. `[repo]/README.md`
2. `[repo]/AGENTS.md`
3. `[repo]/WHAT-IS-AN-AGENT.md` (when designing/changing agents or debugging role boundaries)
4. The selected persona’s agent instructions
5. Decomposition file (if applicable)
6. Any deliverable folder(s) in scope (if applicable)
7. `[repo]/DIRECTORY_TREE.md`

---

## 9) Session Constraints

- [ ] Read-only mode (no file modifications)
- [ ] Single deliverable only
- [ ] Single package only
- [ ] Cross-package scope (list): [ ]
- [ ] Time-boxed session: [ ]
- [ ] Other constraints: [ ]

---
