# AGENTS.md — How to use the agent framework in this repo

This file is the operator-facing index and “rules of the road” for using the agents shipped with this repository.

**Naming convention:** use `AGENT_*` when referring to instruction files (e.g., `AGENT_CHANGE.md`); use the role name (e.g., `CHANGE`) when referring to the agent itself. This applies to all agents.

---

## 0) Standards & precedence (canonical spec)

- **Canonical standard:** `AGENT_HELPS_HUMANS.md`. Where any other `AGENT_*` file disagrees, **the other file must be edited to conform**.
- **Required metadata:** every `AGENT_*` instruction file should include the canonical Agent Header Block fields (e.g., `AGENT_CLASS`, `INTERACTION_SURFACE`, `WRITE_SCOPE`, `BLOCKING`, `PRIMARY_OUTPUTS`) and use canonical terminology.
- **Contract discipline:** Type 0 defines/maintains contracts. Type 1 Managers write briefs and orchestrate; Type 2 Specialists execute bounded briefs and return checkable outputs + evidence.
- **Auditing:** use `AUDIT_AGENT.md` as the fill-in rubric when adding agents or checking conformance across the suite.

---

## 1) The core model (the rules that keep the system coherent)

### Project Decomposition
- A project that lacks structure cannot be effectively worked on by agents.
- Project decomposition is what initiates all other agentic workflows.
- Use **PROJECT_DECOMP** to create a decomposition from a messy Scope of Work (SOW).
- The project decomposition file is located here:

`/Users/ryan/ai-env/projects/chirality-app-test/test/execution-*/_Decomposition/`

### Filesystem is the state
- Project “truth” is what is on disk: folders + `_STATUS.md` + the four documents.
- Agents must not maintain a hidden database or private state that diverges from the filesystem.

### Deliverables (working-items) are local
- A **deliverable** (`DEL-xx.yy`) is one folder under `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-*/{PKG-ID}_{PkgLabel}/1_Working/{DEL-ID}_{DelLabel}/`.
- Work inside that folder is **local**: no cross-deliverable “crosstalk” by default.

### Local lifecycle (not stage gates)
Deliverables progress through a local lifecycle:

`OPEN → INITIALIZED → SEMANTIC_READY → IN_PROGRESS → CHECKING → ISSUED`

- **Stage gates** (30/60/90/IFC, etc.) are *human-managed* milestones and are **not** lifecycle states.
- **SEMANTIC_READY** indicates `_SEMANTIC.md` exists (semantic lens). If the lens step is skipped, deliverables may move from `INITIALIZED → IN_PROGRESS` directly.
- `_STATUS.md` is the authoritative lifecycle indicator.

### Cross-deliverable operations are opt-in and human-triggered
- **RECONCILIATION**: coherence checks across a human-defined scope (read-only deliverables) → writes under `execution/_Reconciliation/`.
- **AGGREGATION**: synthesis/collection across a human-defined scope (read-only inputs by default) → writes under `execution/_Aggregation/`.
- **ESTIMATING**: estimate snapshot generation across a defined scope (read-only deliverables) → writes under `execution/_Estimates/`.

---

## 2) Agent classification (quick reference)

Agents are classified by how they interact, what they write, and whether they can block for human input.

### Classification Properties

| Property | Values | Meaning |
|----------|--------|---------|
| **AGENT_CLASS** | `PERSONA` / `TASK` | Persona agents run interactive sessions; Task agents run pipelines |
| **INTERACTION_SURFACE** | `chat` / `INIT-TASK` / `spawned` / `both` | How the agent is invoked |
| **WRITE_SCOPE** | `project-level` / `tool-root-only` / `deliverable-local` / `none` | What the agent is allowed to write |
| **BLOCKING** | `allowed` / `never` | Whether the agent may pause for human input |

Each agent instruction file also declares **AGENT_TYPE**:
- `0` — intent alignment and operator control (Type 0)
- `1` — interactive orchestration (Type 1)
- `2` — bounded task execution (Type 2)

### Full Agent Type Table

| Agent | CLASS | INTERACTION | PRIMARY_OUTPUTS |
| --- | --- | --- | --- |
| **4_DOCUMENTS** | TASK | spawned | 4 docs, `_STATUS.md` (OPEN→INITIALIZED) |
| **AGGREGATION** | TASK | spawned | Snapshots in `_Aggregation/` |
| **AUDIT_AGENTS** | TASK | spawned | Agent state report |
| **AUDIT_DEPENDENCIES** | TASK | spawned | Dependencies state report |
| **CHANGE** | PERSONA | chat | Git state report; optional git actions after explicit approval |
| **CHIRALITY_FRAMEWORK** | TASK | spawned | `_SEMANTIC.md`, `_STATUS.md` |
| **CHIRALITY_LENS** | TASK | spawned | `_SEMANTIC_LENSING.md`, `_STATUS.md` |
| **DEPENDENCIES** | TASK | spawned | `_DEPENDENCIES.md`, `Dependencies.csv` |
| **ESTIMATING** | TASK | spawned | Estimate snapshots in `_Estimates/` |
| **HELP_HUMAN** | PERSONA | chat | Briefs, checklists, interpretations, next-step recommendations |
| **HELPS_HUMANS** | PERSONA | chat | Workflow design standards; agent instruction maintenance guidance |
| **ORCHESTRATOR** | PERSONA | chat | `_COORDINATION.md`; spawns sub-agents |
| **PREPARATION** | TASK | spawned | Folders, metadata files |
| **PROJECT_CONTROLS** | PERSONA | chat | Project controls register, decision capture, run plans |
| **PROJECT_DECOMP** | PERSONA | chat | Decomposition document |
| **RECONCILIATION** | PERSONA | chat | Reports in `_Reconciliation/` |
| **TASK_SETUP** | TASK | spawned | Initialized agent instructions specific to the deliverable |
| **WORKING_ITEMS** | PERSONA | chat | User defined output |

### When to use which class

**Persona agents** — Use when you need an interactive session:
- `PROJECT_DECOMP`: Starting a new project from a messy SOW
- `HELP_HUMAN`: Need help choosing the right next step
- `ORCHESTRATOR`: Initializing workspace, scanning status, spawning sub-agents
- `PROJECT_CONTROLS`: Interactive control plane; invokes Type 2 pipelines
- `WORKING_ITEMS`: Production work on a specific deliverable (human-in-the-loop)
- `HELPS_HUMANS`: Workflow design standard for writing/maintaining agent instructions

**Task agents** — Use for pipeline work 
- `PREPARATION`: Scaffolding folders and metadata
- `4_DOCUMENTS`: Generating initial drafts
- `CHIRALITY_FRAMEWORK`: Generating semantic lenses 
- `DEPENDENCIES`: Discovering dependencies from content 
- `AGGREGATION`: Cross-file rollups and synthesis 
- `CHANGE`: Git state review and optional actions with explicit approval
- `ESTIMATING`: Cost estimate snapshots

---

EOF
