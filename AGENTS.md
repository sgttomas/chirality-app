# AGENTS.md — How to use the agent framework in this repo

This file is the operator-facing index and “rules of the road” for using the agents shipped with this repository.

If you’re new, start with /Users/ryan/ai-env/projects/chirality-app/agents/AGENT_CHIRALITY-APP.md (the human guidance agent). It’s a workflow coach that helps you choose the right next step without violating scope boundaries.

**Naming convention:** use `AGENT_*` when referring to instruction files (e.g., `AGENT_CHANGE.md`); use the role name (e.g., `CHANGE`) when referring to the agent itself. This applies to all agents.

---

## 0) Standards & precedence (canonical spec)

- **Canonical standard:** `AGENT_HELPS_HUMANS.md`. Where any other `AGENT_*` file disagrees, **the other file must be edited to conform**.
- **Required metadata:** every `AGENT_*` instruction file should include the canonical Agent Header Block fields (e.g., `AGENT_CLASS`, `INTERACTION_SURFACE`, `WRITE_SCOPE`, `BLOCKING`, `PRIMARY_OUTPUTS`) and use canonical terminology.
- **Contract discipline:** Type 1 Managers write briefs and orchestrate; Type 2 Specialists execute bounded briefs and return checkable outputs + evidence; Type 0 defines/maintains contracts.
- **Auditing:** use `AUDIT_AGENT.md` as the fill-in rubric when adding agents or checking conformance across the suite.

---

## 1) The core model (the rules that keep the system coherent)

### Project Decomposition
- A project that lacks structure cannot be effectively worked on by agents.
- Project decomposition is what initiates all other agentic workflows.
- Use **PROJECT_DECOMP** to create a decomposition from a messy Scope of Work (SOW).
- The project decomposition file is located here:

`/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md`

### Filesystem is the state
- Project “truth” is what is on disk: folders + `_STATUS.md` + the four documents.
- Agents must not maintain a hidden database or private state that diverges from the filesystem.

### Deliverables (working-items) are local
- A **deliverable** (`DEL-xx.yy`) is one folder under `/Users/ryan/ai-env/projects/chirality-app/test/execution/{PKG-ID}_{PkgLabel}/1_Working/{DEL-ID}_{DelLabel}/`.
- Work inside that folder is **local**: no cross-deliverable “crosstalk” by default.

### Local lifecycle (not stage gates)
Deliverables progress through a local lifecycle:

`OPEN → INITIALIZED → SEMANTIC_READY → IN_PROGRESS → CHECKING → ISSUED`

- **Stage gates** (30/60/90/IFC, etc.) are *human-managed* milestones and are **not** lifecycle states.
- **SEMANTIC_READY** indicates `_SEMANTIC.md` exists (semantic lens). If the lens step is skipped, deliverables may move from `INITIALIZED → IN_PROGRESS` directly.
- `_STATUS.md` is the authoritative lifecycle indicator.

### Coordination representation vs dependency tracking mode
The framework separates:
- **Coordination representation**: *how humans coordinate* (Schedule-first | Declared deps | Full graph)
- **Dependency tracking mode**: *how much dependency data is captured in-file* (`NOT_TRACKED` | `DECLARED` | `FULL_GRAPH`)

Rules of thumb:
- If `NOT_TRACKED`, do **not** compute or claim “blocked/unblocked” status.
- If `DECLARED`, only declared interface-critical edges may be used for advisory blocker reporting.
- If `FULL_GRAPH`, the graph is intended to be complete and acyclic (DAG).

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

| Agent | CLASS | INTERACTION | WRITE_SCOPE | BLOCKING | PRIMARY_OUTPUTS |
|-------|-------|-------------|-------------|----------|-----------------|
| **PROJECT_DECOMP** | PERSONA | chat | project-level | allowed | Decomposition document |
| **ORCHESTRATOR** | PERSONA | chat | tool-root-only | allowed | `_COORDINATION.md`; spawns sub-agents |
| **PROJECT_CONTROLS** | PERSONA | chat | tool-root-only | allowed | Project controls register, decision capture, run plans |
| **WORKING_ITEMS** | PERSONA | chat | deliverable-local | allowed | 4 docs, `_STATUS.md` updates; may invoke ESTIMATING |
| **HELP_HUMAN** | PERSONA | chat | none | never | Briefs, checklists, interpretations, next-step recommendations |
| **HELPS_HUMANS** | PERSONA | chat | none | never | Workflow design standards; agent instruction maintenance guidance |
| **PREPARATION** | TASK | spawned | deliverable-local | never | Folders, metadata files |
| **4_DOCUMENTS** | TASK | spawned | deliverable-local | never | 4 docs, `_STATUS.md` (OPEN→INITIALIZED) |
| **CHIRALITY_FRAMEWORK** | TASK | spawned | deliverable-local | never | `_SEMANTIC.md`, `_STATUS.md` |
| **DEPENDENCIES** | TASK | spawned | deliverable-local | never | `_DEPENDENCIES.md`, `Dependencies.csv` |
| **AGGREGATION** | TASK | spawned | tool-root-only | never | Snapshots in `_Aggregation/` |
| **RECONCILIATION** | TASK | spawned | tool-root-only | never | Reports in `_Reconciliation/` |
| **ESTIMATING** | PERSONA | chat | tool-root-only | never | Estimate snapshots in `_Estimates/` |
| **CHANGE** | PERSONA | chat | none | allowed | Git state report; optional git actions after explicit approval |


### When to use which class

**Persona agents** — Use when you need an interactive session:
- `PROJECT_DECOMP`: Starting a new project from a messy SOW
- `HELP_HUMAP`: Need help choosing the right next step
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
- `RECONCILIATION`: Cross-deliverable coherence checks 
- `ESTIMATING`: Cost estimate snapshots
- `CHANGE`: Git state review and optional actions with explicit approval

---

## 3) Agent index (what each one is for)

> Filenames may include `_REVISED_..._v3` (or later). Treat the names below as *agent types*.

### PROJECT_DECOMP (Project Decomposition)
- **What it does:** Transforms a messy, user-supplied Scope of Work (SOW) into a structured scope output (SSOW), then decomposes SSOW into flat Packages, Deliverables, and anticipated Artifacts. Runs a conversational, gate-controlled process with the user.
- **What it does not do:** Produce engineering content; skip confirmation gates; resolve ambiguities silently; approve its own output.

File: `/Users/ryan/ai-env/projects/chirality-app/agents/AGENT_PROJECT_DECOMP.md`

### HELP_HUMAN (Human Support Persona)
- **What it does:** Helps the human choose the correct next step and avoid framework misuse.
- **What it does not do:** Draft engineering content; change `_STATUS.md`; scan cross-deliverable scope unless explicitly asked to run reconciliation.

File: `/Users/ryan/ai-env/projects/chirality-app/agents/AGENT_HELP_HUMAN.md`

### ORCHESTRATOR (Workspace + visibility)
- **What it does:** Ingests the decomposition; records coordination representation + dependency mode; spawns bounded sub-agents; scans/reports status.
- **What it does not do:** Produce engineering content; assign work; decide stage gates or sequencing.

File: `/Users/ryan/ai-env/projects/chirality-app/agents/AGENT_ORCHESTRATOR.md`

### PROJECT_CONTROLS (Interactive control plane)
- **What it does:** Maintains project control intent, orchestrates Type 2 pipelines, and records decisions/run plans.
- **What it does not do:** Draft engineering content; resolve semantic conflicts; modify deliverable artifacts directly.

File: `/Users/ryan/ai-env/projects/chirality-app/agents/AGENT_PROJECT_CONTROLS.md`

### HELPS_HUMANS (Workflow Design Standard)
- **What it does:** Defines standards for designing agentic workflows and writing/maintaining agent instruction sets.
- **What it does not do:** Produce engineering deliverable content; execute project work.

File: `/Users/ryan/ai-env/projects/chirality-app/agents/AGENT_HELPS_HUMANS.md`

### PREPARATION (Scaffolding)
- **What it does:** Creates package/deliverable folders and writes the minimum viable fileset (`_CONTEXT.md`, `_DEPENDENCIES.md`, `_STATUS.md`, `_REFERENCES.md`) idempotently.
- **What it does not do:** Write engineering requirements/specs; infer dependencies.

File: `/Users/ryan/ai-env/projects/chirality-app/agents/AGENT_PREPARATION.md`

### 4_DOCUMENTS (Initialize drafts)
- **What it does:** Generates initial drafts of `Datasheet.md`, `Specification.md`, `Guidance.md`, `Procedure.md` for one deliverable.
- **Status rule:** May set `_STATUS.md` from `OPEN → INITIALIZED` **only if the current state is `OPEN`** (no regression).
- **Epistemic rule:** No invention; cite what you can; otherwise mark TBD / ASSUMPTION.

File: `/Users/ryan/ai-env/projects/chirality-app/agents/AGENT_4_DOCUMENTS.md`

### CHIRALITY_FRAMEWORK (Semantic Lens / Matrices)
- **What it does:** Generates deliverable-specific semantic matrices after drafts exist; writes/overwrites `_SEMANTIC.md`; may advance `_STATUS.md` from `INITIALIZED → SEMANTIC_READY` (only when current state is `INITIALIZED`).
- **What it does not do:** Invent requirements/parameters; modify the four documents; enforce the matrices as constraints (they are a lens, not authority).

File: `/Users/ryan/ai-env/projects/chirality-app/agents/AGENT_CHIRALITY_FRAMEWORK.md`

### WORKING_ITEMS (Human-in-the-loop production)
- **What it does:** Runs a working session for **one** deliverable folder to iteratively produce a coherent set of all four documents.
- **Core rule:** The human engineer is the validator / halting condition.

File: `/Users/ryan/ai-env/projects/chirality-app/agents/AGENT_WORKING_ITEMS.md`

### RECONCILIATION (Cross-deliverable dependency checks)
- **What it does:** Read-only scan across the dependency mapping between deliverables and compares to current state of `4 Documents` for coherence and consistency.
- **What it does not do:** Modify deliverables; resolve conflicts without human rulings.

File: `/Users/ryan/ai-env/projects/chirality-app/agents/AGENT_RECONCILIATION.md`

### AGGREGATION (Project-level synthesis across files)
- **What it does:** Aggregates across any human-defined scope (deliverables, packages, tool roots) and writes a timestamped snapshot under `execution/_Aggregation/` (does not edit inputs).
- **What it does not do:** Modify source files; silently expand scope; overwrite prior snapshots (except `_LATEST.md` pointer).

File: `/Users/ryan/ai-env/projects/chirality-app/agents/AGENT_AGGREGATION.md`

### ESTIMATING (Project cost estimate snapshots)
- **What it does:** Produces an estimate snapshot under `execution/_Estimates/` including `Detail.csv` line items with **Qty, Unit, UnitRate**, plus Summary and `BOE.md` (Basis of Estimate).
- **What it does not do:** Edit deliverable folders; produce binding quotes; require mid-run human decisions (it can log decisions and proceed).

File: `/Users/ryan/ai-env/projects/chirality-app/agents/AGENT_ESTIMATING.md`

### DEPENDENCIES (Emergent dependency discovery)
- **What it does:** Identifies emergent dependencies stated or implied within the four deliverable documents and records them in a machine-trackable register (`Dependencies.csv`) for project-level synthesis by AGGREGATION.
- **What it does not do:** Create engineering content; modify the four documents; invent target IDs without evidence.

File: `/Users/ryan/ai-env/projects/chirality-app/agents/AGENT_DEPENDENCIES.md`

### CHANGE (Diff • Interpret • Recommend • Execute with Approval)
- **What it does:** Inspects git state, summarizes changes, and optionally executes git actions after explicit approval. Creates output in `_DEPENDENCIES.md` per deliverable.
- **What it does not do:** Change repo state without approval; perform destructive actions without heightened approval.

File: `/Users/ryan/ai-env/projects/chirality-app/agents/AGENT_CHANGE.md`

---

## 4) Non-negotiable quality rules (how to avoid bad output)

- **No invention:** if it isn’t in a source, mark **TBD** or label **ASSUMPTION/PROPOSAL**.
- **Cite sources:** every non-trivial claim, requirement, or value should be traceable to a reference.
- **Conflict handling:** contradictions produce a **Conflict Table** and a request for a human ruling.
- **Keep scope clean:** WORKING_ITEMS stays inside one deliverable folder. Use CHIRALITY_FRAMEWORK for semantic lens generation (`_SEMANTIC.md`), RECONCILIATION for coherence checks, and AGGREGATION/ESTIMATING for cross-scope synthesis/costing.
- **Don’t confuse stage gates with lifecycle:** stage gates can be recorded in coordination notes, but `_STATUS.md` uses only the lifecycle states.

EOF
