# INIT — Session Initialization

This document initializes an agent session. Fill in the sections below to orient the agent to your task.

---

## 1) Project Context

**Project Name:** [Your project name]

**Project Workspace:** [Absolute path to project workspace, e.g., `/path/to/project/`]

**Decomposition File:** [Path to decomposition document, or "TBD" if not yet created]

**Reference Documents:** [List key reference documents and their locations]

---

## 2) Agent Assignment

**Assigned Agent:** [Choose one from the list below]

| Agent | Use When |
|-------|----------|
| `PROJECT_DECOMP` | You have a messy SOW and need to create a structured decomposition |
| `CHIRALITY-APP` | You need help choosing the right next step (human guidance) |
| `ORCHESTRATOR` | You have a decomposition and need to initialize the workspace |
| `HELP_HUMAN` | You need scoped briefs, checklists, or minimal next-step guidance |
| `HELPS_HUMANS` | You need workflow design standards for agent instructions/pipelines |
| `PREPARATION` | You need to scaffold folders and minimum viable filesets |
| `4_DOCUMENTS` | You need to generate initial document drafts for deliverables |
| `CHIRALITY_FRAMEWORK` | You need to generate semantic lenses (`_SEMANTIC.md`) |
| `WORKING_ITEMS` | You're doing production work on a specific deliverable |
| `RECONCILIATION` | You need cross-deliverable coherence checks |
| `AGGREGATION` | You need project-level synthesis/rollups |
| `ESTIMATING` | You need cost estimate snapshots |
| `DEPENDENCIES` | You need to discover and document dependencies |
| `CHANGE` | You need a git state report and optional actions with explicit approval |

**Agent Instructions File:** `/Users/ryan/ai-env/projects/chirality-app/agents/AGENT_[NAME].md`

---

## 3) Task Definition

**Task Summary:** [One sentence describing what you want to accomplish]

**Scope:** [What's included / excluded from this task]

**Inputs Available:**
- [ ] Decomposition document exists
- [ ] Reference documents available
- [ ] Workspace scaffolded
- [ ] Initial drafts generated
- [ ] Other: [specify]

**Expected Outputs:** [What should exist when the task is complete]

---

## 4) Session Instructions

[Provide specific instructions for this session. Examples:]

- "Process all deliverables in PKG-08"
- "Start a WORKING_ITEMS session for DEL-14.03"
- "Run reconciliation for PKG-07 and PKG-08 at 30% freeze"
- "Create a decomposition from the attached SOW"

---

## 5) Orientation Files

Before starting, read these files in order:

1. `/Users/ryan/ai-env/projects/chirality-app/README.md` — Framework overview
2. `/Users/ryan/ai-env/projects/chirality-app/AGENTS.md` — Agent index and conventions
3. `[Agent instructions file]` — Specific agent protocol
4. `[Decomposition file]` — Project structure (if applicable)

---

## 6) Key Paths (fill in for your project)

| Item | Path |
|------|------|
| Project workspace | [TBD] |
| Execution root | [TBD] |
| Decomposition document | [TBD] |
| Agent instructions | `/Users/ryan/ai-env/projects/chirality-app/agents/` |
| Reference documents | [TBD] |

---

## 7) Session Constraints

- [ ] Read-only mode (no file modifications)
- [ ] Single deliverable scope
- [ ] Single package scope
- [ ] Cross-package scope (specify packages): [list]
- [ ] Project-wide scope
- [ ] Other: [specify]

---

## Quick Start Templates

### Template A: Start a new project (no decomposition yet)
```
Agent: PROJECT_DECOMP
Task: Create a structured decomposition from my Scope of Work
Inputs: [Attach or paste SOW]
```

### Template B: Initialize workspace from decomposition
```
Agent: ORCHESTRATOR
Task: Initialize workspace and scaffold folders
Decomposition: [path]
Coordination mode: [Schedule-first | Declared deps | Full graph]
Dependency tracking: [NOT_TRACKED | DECLARED | FULL_GRAPH]
```

### Template C: Work on a specific deliverable
```
Agent: WORKING_ITEMS
Task: Production session for [DEL-ID]
Deliverable folder: [path]
Focus areas: [list]
```

### Template D: Cross-deliverable analysis
```
Agent: [RECONCILIATION | AGGREGATION | DEPENDENCIES]
Task: [describe]
Scope: [packages/deliverables to include]
Output location: [path]
```

---

*Fill in the sections above, then instruct the agent to read this file and begin.*
