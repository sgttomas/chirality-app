# Chirality App

Chirality App is a desktop harness for running AI agents against a user-selected folder on your local filesystem.

It bundles a release-managed “agent operating system” (instructions + framework docs) inside the app, and lets users point the runtime at any working directory (`projectRoot`) where agents read/write state as plain files. There is no separate database to install and no server to run: the filesystem is the state.

This repo ships:
- The desktop UI (session control + streaming logs).
- A harness runtime (tool calling, permissions, and event streaming).
- A structured, auditable “filesystem-as-state” project model intended for deliverable-heavy work across multiple domains: EPC/design-build projects, software development, and domain knowledge curation.

If you can choose a folder, you can run Chirality: pick a working directory, start a session, and let agents create/update the project structure under that root.

## Core Concepts

### Decomposition
Every project starts with a **decomposition document** produced through a gate-controlled conversation. The invariant decomposition protocol is defined in `AGENT_DECOMP_BASE.md` and realized by three domain-specific agents:

- **PROJECT_DECOMP** — EPC / design-build projects (Packages → Deliverables)
- **SOFTWARE_DECOMP** — software development (Work Domain Packages → agent-executable Deliverables with Context Envelope sizing)
- **DOMAIN_DECOMP** — handbook / knowledge domains (Categories → Knowledge Types)

SOFTWARE_DECOMP can **extend** any branch (wherever there's software to build). DOMAIN_DECOMP can run **parallel** to any branch (wherever there's domain knowledge to organize).

All decomposition documents include:

- **Structured Outline** — Normalized, atomic units with stable IDs (called Scope Items, Handbook Units, etc. depending on the domain)
- **Decomposition Ledger** — Machine-checkable table mapping every atomic unit to exactly one Partition and (best-effort) to Production Units
- **Partitions** — Flat groupings of scope (no nesting; no overlaps; no gaps) — called Packages, Categories, etc. by domain
- **Production Units** — Units of work within each Partition, with types, responsibilities, and anticipated Artifacts — called Deliverables, Knowledge Types, etc. by domain
- **Decomposition invariant** — Decomposition is always organized as **Partitions containing Production Units**. Optional mappings (objectives, hints, etc.) must preserve this grouping.
- **Objectives** — Success criteria derived from scope, mapped to supporting Production Units
- **Vocabulary Map** — Canonical terms and synonyms to prevent semantic drift
- **Coverage & Telemetry** — Metrics summary (counts, gaps, open issues) that makes decomposition quality measurable across revisions

The decomposition is the source of truth that initializes all downstream agent workflows. Its stable IDs enable longitudinal tracking and cross-deliverable reconciliation.

### Decomposition variant entity terminology

The framework uses abstract structural concepts that map to domain-specific terms in each decomposition variant:

| Abstract concept | PROJECT_DECOMP | SOFTWARE_DECOMP | DOMAIN_DECOMP |
|-----------------|---------------|-----------------|---------------|
| **Partition** | Package (`PKG-XXX`) | Work Domain Package (`PKG-XX`) | Category (`CAT-###`) |
| **Production Unit** | Deliverable (`DEL-XXX-YY`) | Deliverable (`DEL-XX-YY`) | Knowledge Type (`KTY-CC-TT`) |
| **Production documents** | Datasheet, Specification, Guidance, Procedure | Datasheet, Specification, Guidance, Procedure | Knowledge Artifacts (variable per Knowledge Type) |
| **Dependency register** | `Dependencies.csv` (v3.1 schema) | `Dependencies.csv` (v3.1 schema) | Not applicable (DOMAIN has no dependency graph) |
| **Metadata files** | `_CONTEXT.md`, `_STATUS.md`, `_REFERENCES.md`, `_DEPENDENCIES.md` | Same | `_CONTEXT.md`, `_STATUS.md`, `_REFERENCES.md` (no `_DEPENDENCIES.md`) |

**Key distinctions:**
- PROJECT and SOFTWARE variants share the same four-document production set and dependency tracking infrastructure. SOFTWARE adds Context Envelope sizing for agent-executable work estimation.
- DOMAIN variant uses **variable production documents** — each Knowledge Type folder contains whatever Knowledge Artifact files are appropriate for that topic, discovered by scanning for non-metadata `.md` files. There is no fixed four-document set.
- DOMAIN variant has **no dependency graph**. The DEPENDENCIES agent operates on PROJECT/SOFTWARE only. DOMAIN Knowledge Type folders will have no `Dependencies.csv`; agents that encounter them handle this gracefully (e.g., recording `MISSING_DEPENDENCIES_CSV` in coverage).

Agents that operate across variants use a `DECOMP_VARIANT` parameter (`PROJECT` | `SOFTWARE` | `DOMAIN`) and include entity binding tables that map protocol terminology to domain-specific terms. When `DECOMP_VARIANT` is not explicitly provided, agents auto-detect from folder naming conventions (`KTY-` prefix → DOMAIN, otherwise PROJECT/SOFTWARE).

### Filesystem as State

Project state lives entirely in git-tracked files—no database, no server state, no configuration files. The filesystem IS the knowledge graph:
- **Nodes:** Production unit folders and partition folders — Deliverable folders (`DEL-XXX-YY`), Package folders (`PKG-XXX`), Knowledge Type folders (`KTY-CC-TT`), Category folders (`CAT-###`)
- **Edges:** Rows in `Dependencies.csv` and ANCHOR rows connecting tree to graph (PROJECT/SOFTWARE only; DOMAIN has no dependency edges)
- **Properties:** Production documents — Markdown files whose names and count depend on the decomposition variant

Agents traverse this implicit graph on-demand. Analysis artifacts (closure reports, aggregations) are materialized as markdown/JSON in `_Reconciliation/` or `_Aggregation/`, then git-committed for auditability.

**Key advantage:** No synchronization burden. The graph is always current because it's derived from files, not copied into a database.

### Instruction Root vs Working Root

In deployable desktop builds, Chirality separates:
- **Instruction root**: release-managed app bundle containing `README.md`, `AGENTS.md`, `agents/*`, and related framework docs.
- **Working root (`projectRoot`)**: user-selected filesystem location where agents execute and create/update deliverable state.

This preserves a stable agent operating system while keeping project execution fully filesystem-native in user-controlled folders.

### Production Unit Lifecycle
Each production unit (Deliverable or Knowledge Type) progresses through local lifecycle states:

```
OPEN → INITIALIZED → SEMANTIC_READY → IN_PROGRESS → CHECKING → ISSUED
```

- `OPEN`: Folder exists, no content yet
- `INITIALIZED`: Draft production documents generated
- `SEMANTIC_READY`: Semantic lens (`_SEMANTIC.md`) generated (optional step)
- `IN_PROGRESS`: Active human + agent work
- `CHECKING`: Under review
- `ISSUED`: Released

This lifecycle applies uniformly across all decomposition variants. The content of the production documents differs by variant (four fixed documents for PROJECT/SOFTWARE, variable Knowledge Artifacts for DOMAIN), but the lifecycle progression is the same.

Stage gates (30/60/90/IFC) are human-managed milestones, separate from lifecycle states.

### Coordination Representation

The framework separates **how teams coordinate** (schedule-first, declared dependencies, or full graph) from **how the system tracks dependencies** (always maintains the full DAG, but humans choose which edges to enforce for scheduling).

Most EPC projects use **schedule-first coordination** (Gantt drives sequencing) while **dependency tracking** remains active for blocker detection and audit purposes. The dependency graph exists whether or not it drives the schedule.

DOMAIN_DECOMP workspaces typically do not use dependency-driven coordination — Knowledge Types are organized by topic rather than execution sequence. The scheduling, estimating, and dependency closure agents operate on PROJECT/SOFTWARE variants only.

See `_COORDINATION.md` in each execution instance for the chosen representation.

## Agents

Agent roles and conventions are described in `AGENTS.md`.

Agent instruction files are located in `agents/` (flat directory; all agent types).

### The Agent Matrix

Agents are organized along two axes from the chirality semantic framework (Matrix A):

| | **GUIDING** | **APPLYING** | **JUDGING** | **REVIEWING** |
| :--- | :--- | :--- | :--- | :--- |
| **NORMATIVE** | HELP | ORCHESTRATE | WORKING_ITEMS | AGGREGATE |
| **OPERATIVE** | DECOMP\* | PREP\* | TASK\* | AUDIT\* |
| **EVALUATIVE** | AGENTS | DEPENDENCIES | CHANGE | RECONCILING |

- **NORMATIVE** and **EVALUATIVE** rows are accessible from the **WORKBENCH** page (interactive persona sessions).
- **OPERATIVE** row is accessible from the **PIPELINE** page (pipeline execution with category dropdown menus — each `*` cell expands into subcategories).

See `AGENTS.md` §3 for the full OPERATIVE category breakdown and UI routing details.

### Agent variant scope

Not all agents operate across all three decomposition variants. Agents fall into three categories:

| Variant scope | Agents | Notes |
|--------------|--------|-------|
| **All variants** | DECOMP agents, PREPARATION, TASK, WORKING_ITEMS, CHIRALITY_FRAMEWORK, CHIRALITY_LENS, HELP_HUMAN, ORCHESTRATOR, CHANGE, REVIEW, AGGREGATION, RECONCILIATION | These agents are parameterized by `DECOMP_VARIANT` and use entity binding tables to map protocol terminology to domain-specific terms |
| **PROJECT / SOFTWARE only** | DEPENDENCIES, AUDIT_DEP_CLOSURE, ESTIMATING, ESTIMATE_PREP, SCHEDULING | These agents rely on the dependency graph, scheduling, or estimation infrastructure that DOMAIN does not use |
| **Variant-independent** | HELPS_HUMANS (Type 0), AUDIT_AGENTS | These agents operate on agent instruction files or framework standards, not on production unit content |

Agents that support all variants use `DECOMP_VARIANT` auto-detection (folder name prefix `KTY-` → DOMAIN, otherwise PROJECT/SOFTWARE) when the variant is not explicitly provided.

### Key instruction files

- `agents/AGENT_HELPS_HUMANS.md` — Canonical standard for agent design (Type 0)
- `agents/AGENT_DECOMP_BASE.md` — Invariant decomposition protocol shared by all decomposition agents (Type 0)
- `agents/AGENT_HELP_HUMAN.md` — Human support manager (Type 1)
- `agents/AGENT_RECONCILIATION.md` — Cross-deliverable reconciliation manager (Type 1)
- `agents/AGENT_DEPENDENCIES.md` — Dependency extraction specialist (Type 2; PROJECT/SOFTWARE only)
- `agents/AGENT_AUDIT_DEP_CLOSURE.md` — Closure analysis specialist (Type 2; PROJECT/SOFTWARE only)

## Production Unit Folder Structure

### PROJECT / SOFTWARE Deliverable Folders

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

### DOMAIN Knowledge Type Folders

```
{CAT-ID}_{CategoryLabel}/
└── {KTY-CC-TT}_{KnowledgeTypeDesc}/
    ├── _CONTEXT.md              # Identity + decomposition pointer
    ├── _STATUS.md               # Lifecycle state + history
    ├── _REFERENCES.md           # Source document pointers
    ├── MEMORY.md                # Working memory
    ├── {KnowledgeArtifact1}.md  # Variable production documents —
    ├── {KnowledgeArtifact2}.md  #   names and count depend on the
    ├── ...                      #   Knowledge Type's subject matter
    ├── _SEMANTIC.md             # Semantic lens (optional)
    └── _SEMANTIC_LENSING.md     # Semantic analysis (optional)
```

DOMAIN folders have **no `_DEPENDENCIES.md`** and **no `Dependencies.csv`** — the dependency graph is a PROJECT/SOFTWARE concept. Production documents are not a fixed four-document set; agents discover them by scanning for non-metadata `.md` files.

### Project-level outputs

Project-level outputs live in separate tool roots:
- `execution-*/_Aggregation/` — Aggregation snapshots
- `execution-*/_Estimates/` — Cost estimate snapshots (driven by `BASIS_OF_ESTIMATE`; no agent-authored BOE required by default)
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
