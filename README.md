# Chirality App

Chirality App is a desktop harness for running AI agents against a user-selected folder on your local filesystem.

It bundles a release-managed “agent operating system” (instructions + framework docs) inside the app, and lets users point the runtime at any working directory (`projectRoot`) where agents read/write state as plain files. There is no separate database to install and no server to run: the filesystem is the state.

This repo ships:
- The desktop UI (session control + streaming logs).
- A harness runtime (tool calling, permissions, and event streaming).
- A structured, auditable “filesystem-as-state” project model intended for deliverable-heavy work (EPC/design-build and similar environments).

If you can choose a folder, you can run Chirality: pick a working directory, start a session, and let agents create/update the project structure under that root.

## Core Concepts

### Project Decomposition
Every project starts with a **decomposition document** produced by PROJECT_DECOMP through a gate-controlled conversation. The decomposition includes:

- **Structured Scope of Work (SSOW)** — Normalized, atomic scope items with stable IDs
- **Scope Ledger** — Machine-checkable table mapping every scope item to exactly one Package and (best-effort) to Deliverables
- **Packages** — Flat partitions of scope (no nesting; no overlaps; no gaps)
- **Deliverables** — Units of production within each Package, with types, responsibilities, and anticipated Artifacts
- **Objectives** — Success criteria derived from scope, mapped to supporting Deliverables
- **Vocabulary Map** — Canonical terms and synonyms to prevent semantic drift
- **Coverage & Telemetry** — Metrics summary (counts, gaps, open issues) that makes decomposition quality measurable across revisions

The decomposition is the source of truth that initializes all downstream agent workflows. Its stable IDs enable longitudinal tracking and cross-deliverable reconciliation.

### Filesystem as State

Project state lives entirely in git-tracked files—no database, no server state, no configuration files. The filesystem IS the knowledge graph:
- **Nodes:** Deliverable folders (DEL-XXX-XX), package folders (PKG-XXX)
- **Edges:** Rows in Dependencies.csv, ANCHOR rows connecting tree to graph
- **Properties:** Markdown files (Datasheet.md, Specification.md, etc.)

Agents traverse this implicit graph on-demand. Analysis artifacts (closure reports, aggregations) are materialized as markdown/JSON in `_Reconciliation/` or `_Aggregation/`, then git-committed for auditability.

**Key advantage:** No synchronization burden. The graph is always current because it's derived from files, not copied into a database.

### Instruction Root vs Working Root

In deployable desktop builds, Chirality separates:
- **Instruction root**: release-managed app bundle containing `README.md`, `AGENTS.md`, `agents/*`, and related framework docs.
- **Working root (`projectRoot`)**: user-selected filesystem location where agents execute and create/update deliverable state.

This preserves a stable agent operating system while keeping project execution fully filesystem-native in user-controlled folders.

### Deliverable Lifecycle
Each deliverable progresses through local lifecycle states:

```
OPEN → INITIALIZED → SEMANTIC_READY → IN_PROGRESS → CHECKING → ISSUED
```

- `OPEN`: Folder exists, no content yet
- `INITIALIZED`: Draft documents generated
- `SEMANTIC_READY`: Semantic lens (`_SEMANTIC.md`) generated (optional step)
- `IN_PROGRESS`: Active human + agent work
- `CHECKING`: Under review
- `ISSUED`: Released

Stage gates (30/60/90/IFC) are human-managed milestones, separate from lifecycle states.

### Coordination Representation

The framework separates **how teams coordinate** (schedule-first, declared dependencies, or full graph) from **how the system tracks dependencies** (always maintains the full DAG, but humans choose which edges to enforce for scheduling).

Most EPC projects use **schedule-first coordination** (Gantt drives sequencing) while **dependency tracking** remains active for blocker detection and audit purposes. The dependency graph exists whether or not it drives the schedule.

See `_COORDINATION.md` in each execution instance for the chosen representation.

## Agents

Agent roles and conventions are described in `AGENTS.md`.

Agent instruction files are located in `agents/` (Type 0/1 managers) and `agents/tasks/`, `agents/prep/`, `agents/audit/` (Type 2 specialists).

Key instruction files:
- `agents/AGENT_HELPS_HUMANS.md` — Canonical standard for agent design
- `agents/AGENT_RECONCILIATION.md` — Type 1 manager for cross-deliverable reconciliation
- `agents/AGENT_DEPENDENCIES.md` — Type 2 specialist for dependency extraction
- `agents/tasks/AGENT_AUDIT_DEP_CLOSURE.md` — Type 2 specialist for closure analysis

## Deliverable Folder Structure

Each deliverable folder contains:

```
{PKG-ID}_{PkgLabel}/
└── 1_Working/
    └── {DEL-ID}_{DelLabel}/
        ├── _CONTEXT.md          # Identity + decomposition pointer
        ├── _STATUS.md           # Lifecycle state + history
        ├── _REFERENCES.md       # Source document pointers
        ├── _DEPENDENCIES.md     # Dependency summary + run notes
        ├── Dependencies.csv     # Structured dependency register (v3.1 schema)
        ├── AGENT_TASK.md        # Deliverable-local task agent (self-initializing)
        ├── MEMORY.md            # Accumulated knowledge and context
        ├── Datasheet.md         # Key parameters and data
        ├── Specification.md     # Technical requirements
        ├── Guidance.md          # Design guidance and rationale
        ├── Procedure.md         # Execution procedures
        ├── _SEMANTIC.md         # Semantic lens (optional)
        └── _SEMANTIC_LENSING.md # Semantic analysis (optional)
```

Project-level outputs live in separate tool roots:
- `execution-*/_Aggregation/` — Aggregation snapshots
- `execution-*/_Estimates/` — Cost estimate snapshots
- `execution-*/_Reconciliation/` — Reconciliation reports, closure analysis
- `execution-*/_Archive/` — Baseline snapshots with checksums
- `execution-*/_Scripts/` — Deployment and analysis scripts

## Regulated, High-Stakes, and Professional-Responsibility Environments

Many EPC and design-build programs run in environments where deliverables are:

- **Safety-significant** (people, environment, critical infrastructure)
- **Contractually binding** (scope, acceptance, claims, and payment milestones often depend on document content)
- **Subject to codes/standards, regulator expectations, and internal QA** (document control, traceability, configuration management)
- Produced under **high professional responsibility** (engineering duty of care; formal review and sign-off)

In these settings, "agentic workflows" are only valuable if they are **auditable, controllable, and review-friendly**. The approach used in this Chirality App project is intentionally conservative: agents accelerate production, but the project truth remains explicit in files, and humans remain the accountable validators.

### What `WHAT-IS-AN-AGENT.md` means in high-stakes workflows

`WHAT-IS-AN-AGENT.md` frames a "great agent" as a **composed system** with clear layers:

- **Agent 0 / Type 0 (Architect):** defines and maintains the standards, contracts, and role boundaries
- **Agent 1 / Type 1 (Manager):** interprets intent, decomposes work, writes briefs, routes to Specialists, and merges results
- **Agent 2 / Type 2 (Specialist):** executes a narrow brief with minimal context and returns outputs + evidence

In regulated work, this layered design is prudent because it:

- Creates **separation of concerns** (policy/standards vs orchestration vs execution), making failures easier to localize and fix
- Enables **stateless, brief-driven Specialists**, reducing hidden context, reducing drift, and improving repeatability
- Supports **deterministic debugging** ("is this a standards problem, a routing problem, or an execution problem?")
- Encourages **fan-out/fan-in** when appropriate, making reviews faster (specialists produce bounded artifacts that can be checked independently)

### What `AGENT_HELPS_HUMANS.md` means in high-stakes workflows

`AGENT_HELPS_HUMANS.md` is the workflow-design standard for writing agent instruction sets and pipelines. In high-stakes environments, it functions like a lightweight **quality system for agent behavior**, emphasizing:

- **Explicit contracts** (clear inputs, outputs, acceptance criteria)
- **Write scope discipline** (what an agent is allowed to modify, and when)
- **Provenance and evidence expectations** (what must be cited, what must be marked as TBD/assumption)
- **QA gates** (checking steps that prevent silent failure or silent "fixes")
- **Snapshot-oriented outputs** (so review is anchored to stable artifacts, not transient chat context)

This is prudent because most real-world failures in regulated documentation are *not* "lack of content," but:
- ambiguous scope,
- untraceable rationale,
- uncontrolled revisions,
- inconsistent terminology across disciplines,
- and weak handoffs between contributors.

### How this framework supports common regulated-controls expectations

Without claiming "automatic compliance," the architecture supports the kinds of controls auditors and QA programs typically expect:

- **Traceability:** decomposition IDs, scope ledgers, references files, and deliverable-local context make "why is this requirement here?" answerable.
- **Document control:** "filesystem as state" and lifecycle gating align naturally with controlled document progression (draft → check → issue).
- **Configuration management:** snapshots and explicit change review reduce accidental drift and make diffs meaningful.
- **Verification & validation:** QA gates, conflict surfacing, and explicit uncertainty labeling create a reviewable V&V posture.
- **Segregation of duties:** Manager vs Specialist vs Human validator boundaries reduce the risk of one "all-powerful agent" making uncontrolled changes.
- **Information security & confidentiality:** least-privilege data handling and constrained write scopes reduce accidental exposure and unintended edits.

### Responsible-use note (important)

This framework is designed to support professional responsibility, not replace it.

- Treat agent outputs as **drafts and structured assistance**, not authoritative engineering judgment.
- Keep **human review and sign-off** as the decision gate for safety, compliance, and contractual commitments.
