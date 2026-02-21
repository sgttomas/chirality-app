# AGENTS.md — How to use the agent framework in this repo

This file is the operator-facing index and “rules of the road” for using the agents shipped with this repository.

**Naming convention:** use `AGENT_*` when referring to instruction files (e.g., `AGENT_CHANGE.md`); use the role name (e.g., `CHANGE`) when referring to the agent itself. This applies to all agents.

---

## 0) Standards & precedence (canonical spec)

- **Canonical standard:** `AGENT_HELPS_HUMANS.md`. Where any other `AGENT_*` file disagrees, **the other file must be edited to conform**.
- **Decomposition base specification:** `AGENT_DECOMP_BASE.md`. Defines the invariant decomposition protocol (7-gate workflow, abstract entities, ledger/telemetry contract, extension rules) shared by all decomposition agents. Conforming agents: PROJECT_DECOMP, SOFTWARE_DECOMP, DOMAIN_DECOMP.
- **Required metadata:** every `AGENT_*` instruction file should include the canonical Agent Header Block fields (e.g., `AGENT_CLASS`, `INTERACTION_SURFACE`, `WRITE_SCOPE`, `BLOCKING`, `PRIMARY_OUTPUTS`) and use canonical terminology.
- **Contract discipline:** Type 0 defines/maintains contracts. Type 1 Managers write briefs and orchestrate; Type 2 Specialists execute bounded briefs and return checkable outputs + evidence.
- **Auditing:** use `AGENT_AUDIT_AGENTS.md` as the fill-in rubric when adding agents or checking conformance across the suite.

---

## 1) The core model (the rules that keep the system coherent)

### Decomposition
- Work that lacks structure cannot be effectively worked on by agents.
- Decomposition is what initiates all other agentic workflows.
- **Decomposition invariant:** the abstract protocol (intake → normalize → partition → operationalize → verify → publish) is defined in `AGENT_DECOMP_BASE.md`. All decomposition agents conform to it.
- **Decomposition variants** exist for different domains:
  - **PROJECT_DECOMP** — EPC / design-build projects (Packages → Deliverables, `PKG-XXX` / `DEL-XXX-YY`)
  - **SOFTWARE_DECOMP** — software development (Work Domain Packages → agent-executable Deliverables with Context Envelope sizing, `PKG-XX` / `DEL-XX-YY`)
  - **DOMAIN_DECOMP** — handbook / knowledge domains (Categories → Knowledge Types, `CAT-###` / `KTY-CC-TT`)
- The decomposition file is located here:

`{EXECUTION_ROOT}/_Decomposition/`

### Filesystem is the state
- Project “truth” is what is on disk: folders + `_STATUS.md` + the four documents.
- Agents must not maintain a hidden database or private state that diverges from the filesystem.

### Deliverables (working-items) are local
- A **deliverable** (`DEL-XXX-YY`) is one folder under `{EXECUTION_ROOT}/{PKG-ID}_{PkgLabel}/1_Working/{DEL-ID}_{DelLabel}/`.
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
- **ESTIMATING**: estimate snapshot generation across a defined scope (read-only deliverables) → writes under `execution/_Estimates/`. Runs are parameterized by `BASIS_OF_ESTIMATE` (QUOTE | RATE_TABLE | HISTORICAL | PARAMETRIC | ALLOWANCE). No agent-authored BOE is required by default.
- **SCHEDULING**: parameterized schedule generation from the dependency graph (read-only deliverables) → writes under `execution/_Schedule/`. Supports PRECEDENCE, CONSTRAINT, or HYBRID scheduling basis.

---

## 2) Agent classification (quick reference)

Agents are classified by how they interact, what they write, and whether they can block for human input.

### Classification Properties

| Property | Values | Meaning |
|----------|--------|---------|
| **AGENT_CLASS** | `PERSONA` / `TASK` | Persona agents run interactive sessions; Task agents run pipelines |
| **INTERACTION_SURFACE** | `chat` / `INIT-TASK` / `spawned` / `both` | How the agent is invoked |
| **WRITE_SCOPE** | `project-level` / `tool-root-only` / `deliverable-local` / `repo-metadata-only` / `none` | What the agent is allowed to write |
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
| **AUDIT_DECOMP** | TASK | spawned | `Decomp-Coverage_Report.md`, `Decomp-Coverage_IssueLog.csv`, `Decomp-Coverage_Matrix.csv`, and `coverage_summary.json` |
| **AUDIT_DEP_CLOSURE** | TASK | spawned | Dependencies state report |
| **CHANGE** | PERSONA | chat | Git state report; optional git actions after explicit approval |
| **CHIRALITY_FRAMEWORK** | TASK | spawned | `_SEMANTIC.md`, `_STATUS.md` |
| **CHIRALITY_LENS** | TASK | spawned | `_SEMANTIC_LENSING.md` |
| **CONTEXT_TRANSPOSE** | PERSONA | chat | CTSP snapshot; patch plan; optional applied patch; QA report |
| **DECOMP_BASE** | PERSONA | chat | Decomposition base specification; defines the invariant protocol for conforming agents (PROJECT_DECOMP, SOFTWARE_DECOMP, DOMAIN_DECOMP) |
| **DEPENDENCIES** | TASK | spawned | `_DEPENDENCIES.md`, `Dependencies.csv` |
| **DOMAIN_DECOMP** | PERSONA | chat | Domain decomposition document (conforms to DECOMP_BASE) |
| **ESTIMATE_PREP** | TASK | INIT-TASK | Pricing CSVs, `INDEX.md`, BOE scaffold or full `BASIS_OF_ESTIMATE.md`, QA/provenance logs |
| **ESTIMATING** | TASK | spawned | Estimate snapshots in `_Estimates/` |
| **HELP_HUMAN** | PERSONA | chat | Briefs, checklists, interpretations, next-step recommendations |
| **HELPS_HUMANS** | PERSONA | chat | Workflow design standards; agent instruction maintenance guidance |
| **ORCHESTRATOR** | PERSONA | chat | `_COORDINATION.md`; spawns sub-agents |
| **PREPARATION** | TASK | spawned | Folders, metadata files |
| **PROJECT_DECOMP** | PERSONA | chat | Decomposition document (conforms to DECOMP_BASE) |
| **RECONCILIATION** | PERSONA | chat | Reports in `_Reconciliation/` |
| **REVIEW** | PERSONA | chat | Review checklist, finding register, review summary, lifecycle transition record |
| **SCHEDULING** | PERSONA | chat | Schedule structure, duration model, Gantt (Mermaid + CSV), critical path / risk report in `_Schedule/` — parameterized by `BASIS_OF_SCHEDULE` (PRECEDENCE / CONSTRAINT / HYBRID) |
| **SCOPE_CHANGE** | PERSONA | chat | Amended decomposition, updated `_CONTEXT.md` files, impact assessment, propagation record |
| **SOFTWARE_DECOMP** | PERSONA | chat | Software decomposition document with Context Envelope sizing (conforms to DECOMP_BASE) |
| **TASK** | TASK | INIT-TASK | Proposals; optional edits to authorized deliverable-local files |
| **WORKING_ITEMS** | PERSONA | chat | User defined output |


---

EOF
