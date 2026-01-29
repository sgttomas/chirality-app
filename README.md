# Chirality App

A multi-agent framework for EPC (Engineering, Procurement, Construction) and design-build projects.

Chirality App provides a structured, deliverable-centric approach to producing engineering and project documentation using coordinated AI agents. Work is organized around **deliverables** that progress through a defined lifecycle, with clear boundaries between local (single-deliverable) and cross-project operations.

## Core Concepts

### Project Decomposition
Every project starts with a **decomposition file** that defines:
- Packages (work breakdown structure)
- Deliverables within each package
- Objectives and scope boundaries
- Reference documents
- Key decisions and constraints

The decomposition is the source of truth that initializes all agent workflows.

### Filesystem as State
Project truth lives on disk. Agents read and write files directly—there is no hidden database or divergent state. The folder structure itself encodes project status.

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

### Coordination Modes
The framework separates how teams coordinate from how dependencies are tracked:

| Coordination Representation | Description |
|---|---|
| Schedule-first | Gantt/stage gates drive sequencing |
| Declared deps | Explicit interface-critical edges only |
| Full graph | Complete dependency DAG |

| Dependency Tracking Mode | Behavior |
|---|---|
| `NOT_TRACKED` | No blocker analysis |
| `DECLARED` | Advisory blockers from declared edges |
| `FULL_GRAPH` | Full DAG analysis |

Most EPC projects work best with **Schedule-first** + **NOT_TRACKED** or **DECLARED**.

## Agents

| Agent | Purpose |
|---|---|
| **CHIRALITY-APP** | Human guidance / navigator—helps choose the right next step |
| **ORCHESTRATOR** | Workspace setup, status reporting, spawns sub-agents |
| **PREPARATION** | Scaffolds package/deliverable folders and metadata files |
| **4_DOCUMENTS** | Generates initial drafts (Datasheet, Specification, Guidance, Procedure) |
| **CHIRALITY_FRAMEWORK** | Generates semantic lens matrices (`_SEMANTIC.md`) |
| **WORKING_ITEMS** | Human-in-the-loop production sessions for one deliverable |
| **RECONCILIATION** | Cross-deliverable coherence checks (read-only) |
| **AGGREGATION** | Project-level synthesis across files (reports, registers, rollups) |
| **ESTIMATING** | Cost estimate snapshots with Qty/Unit/UnitRate line items |

Agent instruction files are located in `agents/`.

## Deliverable Folder Structure

Each deliverable folder contains:

```
{PKG-ID}_{PkgLabel}/
└── 1_Working/
    └── {DEL-ID}_{DelLabel}/
        ├── _CONTEXT.md        # Identity + decomposition pointer
        ├── _DEPENDENCIES.md   # Dependency mode + declared edges
        ├── _STATUS.md         # Lifecycle state + history
        ├── _REFERENCES.md     # Source document pointers
        ├── _SEMANTIC.md       # Semantic lens (optional)
        ├── Datasheet.md       # Key parameters and data
        ├── Specification.md   # Technical requirements
        ├── Guidance.md        # Design guidance and rationale
        └── Procedure.md       # Execution procedures
```

Project-level outputs live in separate tool roots:
- `execution/_Aggregation/` — Aggregation snapshots
- `execution/_Estimates/` — Cost estimate snapshots
- `execution/_Reconciliation/` — Reconciliation reports

## Getting Started

### 1. Create a Project Decomposition
Write a decomposition file defining your packages, deliverables, objectives, and reference documents. Use the framework's decomposition format.

### 2. Initialize the Workspace
Run ORCHESTRATOR to ingest your decomposition and choose your coordination representation and dependency tracking mode.

### 3. Scaffold Folders
ORCHESTRATOR spawns PREPARATION to create the folder structure and minimum viable filesets.

### 4. Generate Initial Drafts
ORCHESTRATOR spawns 4_DOCUMENTS for each deliverable to create draft Datasheet/Specification/Guidance/Procedure files.

### 5. (Optional) Generate Semantic Lenses
Run CHIRALITY_FRAMEWORK to generate `_SEMANTIC.md` files—question-shaping scaffolds that help structure subsequent work.

### 6. Work on Deliverables
Use WORKING_ITEMS for human + agent sessions inside individual deliverable folders. The human engineer is the validator.

### 7. Cross-Deliverable Operations
When needed, run:
- **RECONCILIATION** for coherence checks at freeze points
- **AGGREGATION** for project-wide synthesis
- **ESTIMATING** for cost snapshots

## Quality Rules

- **No invention**: If it isn't in a source, mark `TBD` or label `ASSUMPTION/PROPOSAL`
- **Cite sources**: Every non-trivial claim should be traceable to a reference
- **Conflict handling**: Contradictions produce a Conflict Table requiring human ruling
- **Scope discipline**: WORKING_ITEMS stays inside one deliverable; use RECONCILIATION/AGGREGATION for cross-scope work

## Documentation

- `AGENTS.md` — Operator-facing guide to agents and prompt templates
- `agents/AGENT_CHIRALITY-APP.md` — Start here for workflow coaching
- `agents/AGENT_*.md` — Individual agent instruction files
