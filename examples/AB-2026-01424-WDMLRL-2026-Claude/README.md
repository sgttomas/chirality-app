# Chirality App — Project Delivery (PROJECT) Context

Chirality App is a desktop harness for running AI agents against a user-selected folder on your local filesystem.

It bundles a release-managed **agent operating system** (instructions + framework docs) inside the app, and lets users point the runtime at any working directory (`projectRoot`) where agents read/write state as plain files. There is no separate database to install and no server to run: **the filesystem is the state**.

This repository ships:
- The desktop UI (session control + streaming logs).
- A harness runtime (tool calling, permissions, and event streaming).
- A structured, auditable **filesystem-as-state** model designed for **deliverable-heavy EPC / design-build projects**.

If you can choose a folder, you can run Chirality: pick a working directory, start a session, and let agents create/update the project structure under that root.

---

## Core concepts

### Decomposition

Every project starts with a **decomposition document** produced through a gate-controlled conversation. The invariant decomposition protocol is defined in `AGENT_DECOMP_BASE.md` and is realized for projects by:

- **PROJECT_DECOMP** — decomposes an EPC / design-build project into **Packages → Deliverables** with stable IDs.

All decomposition documents include:

- **Structured Outline** — normalized, atomic scope units with stable IDs (your scope source-of-truth).
- **Decomposition Ledger** — a machine-checkable table mapping every atomic unit to exactly one Package and (best-effort) to Deliverables.
- **Packages** — flat groupings of scope (**no nesting; no overlaps; no gaps**), identified as `PKG-XXX`.
- **Deliverables** — units of work within each Package, with responsibilities and anticipated artifacts, identified as `DEL-XXX-YY`.
- **Decomposition invariant** — decomposition is always organized as **Packages containing Deliverables**. Optional mappings (objectives, hints, etc.) must preserve this grouping.
- **Objectives** — success criteria derived from scope, mapped to supporting Deliverables.
- **Vocabulary Map** — canonical terms and synonyms to prevent semantic drift.
- **Coverage & Telemetry** — metrics summary (counts, gaps, open issues) that makes decomposition quality measurable across revisions.

The decomposition is the source of truth that initializes all downstream workflows. Stable IDs enable longitudinal tracking and cross-deliverable reconciliation.

---

### Project entity terminology

The framework uses an abstract structural model that binds to project terminology:

| Abstract concept | PROJECT terminology |
|---|---|
| **Partition** | Package (`PKG-XXX`) |
| **Production Unit** | Deliverable (`DEL-XXX-YY`) |
| **Production documents** | Datasheet, Specification, Guidance, Procedure |
| **Dependency register** | `Dependencies.csv` (v3.1 schema) |
| **Metadata files** | `_CONTEXT.md`, `_STATUS.md`, `_REFERENCES.md`, `_DEPENDENCIES.md` |

---

### Filesystem as state

Project state lives entirely in git-tracked files—no database, no server state, no extra configuration. The filesystem acts as a project graph:

- **Nodes:** Package folders and Deliverable folders.
- **Edges:** rows in `Dependencies.csv` plus the derived dependency summary in `_DEPENDENCIES.md`.
- **Properties:** the production documents (Markdown files) for each Deliverable.

Agents traverse this implicit graph on-demand. Analysis artifacts (closure reports, aggregations) are materialized as Markdown/JSON in `_Reconciliation/` or `_Aggregation/`, then git-committed for auditability.

**Key advantage:** no synchronization burden. The graph is always current because it's derived from files, not copied into a database.

---

### Instruction root vs working root

In deployable desktop builds, Chirality separates:

- **Instruction root**: release-managed app bundle containing `README.md`, `AGENTS.md`, `agents/*`, and related framework docs.
- **Working root (`projectRoot`)**: the user-selected filesystem location where agents execute and create/update project state.

This preserves a stable agent operating system while keeping project execution fully filesystem-native in user-controlled folders.

---

### Deliverable lifecycle

Each deliverable progresses through local lifecycle states:

```
OPEN → INITIALIZED → SEMANTIC_READY → IN_PROGRESS → CHECKING → ISSUED
```

- `OPEN`: folder exists, no content yet
- `INITIALIZED`: draft production documents generated
- `SEMANTIC_READY`: semantic lens (`_SEMANTIC.md`) generated (optional)
- `IN_PROGRESS`: active human + agent work
- `CHECKING`: under review
- `ISSUED`: released

This is a **local** lifecycle: it belongs to each deliverable folder.

> Stage gates (30/60/90/IFC, etc.) are human-managed milestones and are **not** lifecycle states.

---

### Coordination representation

The framework separates:

- **How teams coordinate** (schedule-first, declared dependencies, or full graph), from
- **How the system tracks dependencies** (maintains the full DAG for blocker detection and auditability).

Most EPC projects use **schedule-first coordination** (Gantt drives sequencing) while dependency tracking remains active for blocker detection and audit purposes.

See `_COORDINATION.md` in each execution instance for the chosen representation.

---

## Agents

Agent roles and conventions are described in `AGENTS.md`.

Agent instruction files are located in `agents/` (flat directory; all agent types).

### The Agent Matrix

Agents are organized along two axes from the chirality semantic framework (Matrix A):

| | **GUIDING** | **APPLYING** | **JUDGING** | **REVIEWING** |
| :--- | :--- | :--- | :--- | :--- |
| **NORMATIVE** | HELP | ORCHESTRATE | WORKING_ITEMS | AGGREGATE |
| **OPERATIVE** | DECOMP* | PREP* | TASK* | AUDIT* |
| **EVALUATIVE** | AGENTS | DEPENDENCIES | CHANGE | RECONCILING |

- **NORMATIVE** and **EVALUATIVE** rows are accessible from the **WORKBENCH** page (interactive persona sessions).
- **OPERATIVE** row is accessible from the **PIPELINE** page (pipeline execution with dropdown menus — each `*` cell expands into submenus).

See `AGENTS.md` §3 for the full OPERATIVE breakdown and UI routing details.

### Key instruction files (operator starting points)

(The list below is limited to filenames explicitly referenced in the source README.)

- `agents/AGENT_HELPS_HUMANS.md` — canonical standard for agent design (Type 0)
- `agents/AGENT_DECOMP_BASE.md` — invariant decomposition protocol (Type 0)
- `agents/AGENT_HELP_HUMAN.md` — human support manager (Type 1)
- `agents/AGENT_RECONCILIATION.md` — cross-deliverable reconciliation manager (Type 1)
- `agents/AGENT_DEPENDENCIES.md` — dependency extraction specialist (Type 2)
- `agents/AGENT_AUDIT_DEP_CLOSURE.md` — dependency closure analysis specialist (Type 2)

---

## Deliverable folder structure

### PROJECT deliverable folders

```
{PKG-ID}_{PkgLabel}/
└── 1_Working/
    └── {DEL-ID}_{DelLabel}/
        ├── _CONTEXT.md          # Identity + decomposition pointer
        ├── _STATUS.md           # Lifecycle state + history
        ├── _REFERENCES.md       # Source document pointers
        ├── _DEPENDENCIES.md     # Dependency summary + run notes
        ├── Dependencies.csv     # Structured dependency register (v3.1 schema)
        ├── MEMORY.md            # Working memory (shared by WORKING_ITEMS and TASK agents)
        ├── Datasheet.md         # Key parameters and data
        ├── Specification.md     # Technical requirements
        ├── Guidance.md          # Design guidance and rationale
        ├── Procedure.md         # Execution procedures
        ├── _SEMANTIC.md         # Semantic lens with derivation work (optional)
        └── _SEMANTIC_LENSING.md # Semantic analysis (optional)
```

---

## Project-level tool roots

Project-level outputs live in separate tool roots under each execution instance:

- `execution-*/_Aggregation/` — aggregation snapshots
- `execution-*/_Estimates/` — cost estimate snapshots (parameterized by `BASIS_OF_ESTIMATE`)
- `execution-*/_Reconciliation/` — reconciliation reports, closure analysis
- `execution-*/_Schedule/` — schedule snapshots and reports
- `execution-*/_Archive/` — baseline snapshots with checksums
- `execution-*/_Scripts/` — deployment and analysis scripts

---

## Regulated, high-stakes, and professional-responsibility environments

Many EPC and design-build programs run in environments where deliverables are:

- **Safety-significant** (people, environment, critical infrastructure)
- **Contractually binding** (scope, acceptance, claims, and payment milestones often depend on document content)
- **Subject to codes/standards, regulator expectations, and internal QA** (document control, traceability, configuration management)
- Produced under **high professional responsibility** (engineering duty of care; formal review and sign-off)

In these settings, agent workflows are only valuable if they are **auditable, controllable, and review-friendly**. The approach used in this project model is intentionally conservative: agents accelerate production, but project truth remains explicit in files, and humans remain the accountable validators.

### What “an agent” means in high-stakes workflows

A “great agent” is a **composed system** with clear layers:

- **Type 0 (Architect):** defines and maintains standards, contracts, and role boundaries
- **Type 1 (Manager):** interprets intent, decomposes work, writes briefs, routes to Specialists, and merges results
- **Type 2 (Specialist):** executes a narrow brief with minimal context and returns outputs + evidence

In regulated work, this layered design is prudent because it:

- Creates **separation of concerns** (standards vs orchestration vs execution), making failures easier to localize and fix
- Enables **stateless, brief-driven Specialists**, reducing hidden context, drift, and improving repeatability
- Supports **deterministic debugging** (“is this a standards problem, a routing problem, or an execution problem?”)
- Encourages **fan-out/fan-in** when appropriate, making reviews faster (specialists produce bounded artifacts that can be checked independently)

### Responsible-use note

This framework is designed to support professional responsibility, not replace it.

- Treat agent outputs as **drafts and structured assistance**, not authoritative engineering judgment.
- Keep **human review and sign-off** as the decision gate for safety, compliance, and contractual commitments.
