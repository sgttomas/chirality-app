# TYPES — Domain Vocabulary and Hierarchy

This document is the authoritative vocabulary reference for the Chirality project execution system. It defines the canonical entities, stable identifier formats, enumerated types, agent roles, and lifecycle states.

All agents and governance documents use the terms defined here. Where a term is used differently elsewhere, this document governs.

---

## 1. Project Hierarchy

The project hierarchy is flat: **packages contain deliverables**. There are no phases, sub-packages, or task sub-levels within deliverables.

```
{EXECUTION_ROOT}/
└── PKG-XX_{PkgLabel}/          # Package (flat partition of scope)
    └── 1_Working/
        └── DEL-XX-YY_{DelLabel}/   # Deliverable (unit of production)
```

### 1.1 Package

A **package** is a flat partition of project scope. Packages do not nest.

- Every scope item belongs to exactly one package (no overlaps, no gaps).
- Packages are defined by PROJECT_DECOMP and confirmed by the human.

### 1.2 Deliverable

A **deliverable** is a unit of production within a package. Each deliverable:

- Belongs to exactly one package.
- Has a responsible party.
- Has a type (e.g., compliance document, design package, methodology narrative).
- Produces one or more anticipated artifacts.
- Occupies one folder under `{PKG}/1_Working/`.

### 1.3 Artifact

An **artifact** is a tangible output produced within a deliverable folder. Artifacts include the document kit (Datasheet, Specification, Guidance, Procedure) and any additional outputs appropriate to the deliverable type.

---

## 2. Stable Identifiers

Identifiers are assigned once and persist across renames, path changes, and restructuring. Path is a physical projection of the decomposition, not identity itself.

| Entity | Format | Example | Assigned By |
|--------|--------|---------|-------------|
| Package | `PKG-XX` | `PKG-01` | PROJECT_DECOMP |
| Deliverable | `DEL-XX-YY` | `DEL-01-01` | PROJECT_DECOMP |
| Dependency | `DEP-XX-YY-NNN` | `DEP-01-01-001` | DEPENDENCIES |
| Scope Item | `SOW-NNN` | `SOW-003` | PROJECT_DECOMP |
| Objective | `OBJ-NNN` | `OBJ-001` | PROJECT_DECOMP |

### 2.1 ID Rules

- `XX` in package IDs is a zero-padded numeric sequence (e.g., `01`, `02`, ... `09`, `10`).
- `YY` in deliverable IDs is a zero-padded numeric sequence scoped to the package.
- `NNN` in dependency IDs is a zero-padded numeric sequence scoped to the deliverable.
- IDs MUST NOT change across revisions unless the human explicitly requests renumbering.
- Deliverable IDs use hyphen separators (`DEL-01-01`), not dot separators (`DEL-01.01`).

### 2.2 Folder Labels

Folder names combine the stable ID with a human-readable label:

- Package: `{PKG-ID}_{Sanitize(PackageName)}`
- Deliverable: `{DEL-ID}_{Sanitize(DeliverableName)}`

The canonical (unsanitized) name is recorded in `_CONTEXT.md`. Sanitization rules are defined in `SPEC.md` Section 10.

---

## 3. Dependency Vocabulary

Dependencies capture relationships between deliverables, definition nodes, and external entities. The dependency model distinguishes two fundamental classes of edges.

### 3.1 Dependency Classes

| Class | Meaning | Graph Role |
|-------|---------|------------|
| **ANCHOR** | Connects a deliverable to a definition/traceability node (parent WBS, requirement) | Tree edge (vertical) |
| **EXECUTION** | Captures information flow, prerequisites, handoffs, and constraints between work items | DAG edge (horizontal) |

Together, ANCHOR (tree) and EXECUTION (DAG) form a **knowledge graph**: the tree preserves stable intent; the DAG captures execution couplings.

### 3.2 Anchor Types

| Value | Meaning |
|-------|---------|
| `IMPLEMENTS_NODE` | Parent definition node — exactly one per deliverable |
| `TRACES_TO_REQUIREMENT` | Requirement trace link — zero or more per deliverable |
| `NOT_APPLICABLE` | Used for EXECUTION rows only |

### 3.3 Direction

Direction is always relative to the host deliverable:

| Value | Meaning |
|-------|---------|
| `UPSTREAM` | This deliverable requires information FROM the target |
| `DOWNSTREAM` | This deliverable produces information FOR the target |

Legacy values `INBOUND` and `OUTBOUND` normalize to `UPSTREAM` and `DOWNSTREAM` respectively.

### 3.4 Dependency Types

| Value | Class | Meaning |
|-------|-------|---------|
| `PREREQUISITE` | Execution | Required input or approval before work can proceed |
| `INTERFACE` | Execution | Explicit data/artifact exchange between deliverables |
| `HANDOVER` | Execution | Output of one deliverable consumed as input to another |
| `CONSTRAINT` | Execution | Explicit constraint or condition |
| `ENABLES` | Execution | This deliverable enables downstream work |
| `OTHER` | Both | Default for ANCHOR rows; catch-all for EXECUTION rows |

Legacy types `COORDINATION` and `INFORMATION` MUST NOT be emitted in new extractions.

### 3.5 Target Types

| Value | Meaning |
|-------|---------|
| `DELIVERABLE` | Another deliverable in the project |
| `PACKAGE` | A package |
| `WBS_NODE` | Work breakdown structure or scope node |
| `REQUIREMENT` | A specific requirement (SOW item, objective) |
| `DOCUMENT` | An external or reference document |
| `EQUIPMENT` | Physical equipment or asset |
| `EXTERNAL` | External entity (organization, standard) |
| `UNKNOWN` | Target cannot be confidently resolved |

### 3.6 Provenance and Confidence

| Dimension | Values | Meaning |
|-----------|--------|---------|
| `Explicitness` | `EXPLICIT`, `IMPLICIT` | Whether the dependency is directly stated in source text |
| `Confidence` | `HIGH`, `MEDIUM`, `LOW` | Strength of evidence supporting the dependency |
| `Origin` | `DECLARED`, `EXTRACTED` | Human-declared vs. agent-extracted |

### 3.7 Satisfaction and Status

| Dimension | Values | Tracks |
|-----------|--------|--------|
| `SatisfactionStatus` | `TBD`, `PENDING`, `IN_PROGRESS`, `SATISFIED`, `WAIVED`, `NOT_APPLICABLE` | Closure lifecycle (has the dependency been fulfilled?) |
| `Status` | `ACTIVE`, `RETIRED` | Extraction lifecycle (is the dependency currently observed in sources?) |

---

## 4. Agent Roles

Agents are classified into three types following the 0-1-2 model.

### 4.1 Agent Types

| Type | Name | Role | Scope |
|------|------|------|-------|
| **Type 0** | Architect | Defines and maintains standards, contracts, and role boundaries | Project-wide |
| **Type 1** | Manager | Interprets intent, decomposes work, routes to specialists, merges results | Package or project scope |
| **Type 2** | Specialist | Executes bounded briefs with minimal context; returns outputs + evidence | Single deliverable or narrow task |

### 4.2 Classification Properties

| Property | Values | Meaning |
|----------|--------|---------|
| `AGENT_CLASS` | `PERSONA`, `TASK` | Persona agents run interactive sessions; Task agents run straight-through pipelines |
| `INTERACTION_SURFACE` | `chat`, `INIT-TASK`, `spawned`, `both` | How the agent is invoked |
| `WRITE_SCOPE` | `repo-wide`, `deliverable-local`, `tool-root-only`, `workspace-scaffold-only`, `repo-metadata-only`, `none` | What the agent is allowed to write |
| `BLOCKING` | `never`, `allowed` | Whether the agent may pause for human input |

### 4.3 Authority Model

- Type 0 proposes rules (what "correct" means).
- Type 1 prepares workspaces and orchestrates (what the specialist can see).
- Type 2 does the work (within bounded scope).
- Human approves at gates.

Authority flows downward; escalation flows upward. A Type 2 agent cannot modify rules set by Type 0. A Type 1 agent cannot approve deliverables for external reliance.

---

## 5. Deliverable Lifecycle States

### 5.1 State Definitions

```
OPEN → INITIALIZED → SEMANTIC_READY → IN_PROGRESS → CHECKING → ISSUED
```

| State | Meaning |
|-------|---------|
| `OPEN` | Folder exists with minimum viable fileset; no content yet |
| `INITIALIZED` | Document kit (Datasheet, Specification, Guidance, Procedure) has been drafted |
| `SEMANTIC_READY` | Semantic lens (`_SEMANTIC.md`) has been generated |
| `IN_PROGRESS` | Active human + agent work underway |
| `CHECKING` | Under review |
| `ISSUED` | Released for use |

### 5.2 Stage Gates vs. Lifecycle

**Lifecycle states** are tracked in `_STATUS.md` and represent the deliverable's production status.

**Stage gates** (30%, 60%, 90%, IFC, etc.) are human-managed milestones that represent project-level progress checkpoints. Stage gates are NOT lifecycle states and are tracked separately in coordination records.

### 5.3 Semantic Step

The `INITIALIZED → SEMANTIC_READY` transition is optional. If the semantic lensing step is skipped, deliverables may transition directly from `INITIALIZED → IN_PROGRESS`.

---

## 6. Coordination Representations

The framework separates **how teams coordinate** (schedule-first, declared dependencies, or full graph) from **how the system tracks dependencies** (always maintains deliverable-local registers).

| Representation | Meaning |
|---------------|---------|
| `SCHEDULE_FIRST` | Gantt drives sequencing; dependency tracking active for blocker detection and audit |
| `DEPENDENCY_TRACKED` | Dependency graph drives sequencing |
| `HYBRID` | Combination of schedule-first and dependency-tracked |

The coordination representation is recorded in `_COORDINATION.md` and chosen per project instance.

---

## 7. Document Kit Types

Each deliverable contains a standard four-document kit:

| Document | Purpose |
|----------|---------|
| `Datasheet.md` | Key parameters, identification, structured metadata |
| `Specification.md` | Technical requirements, scope definition, acceptance criteria |
| `Guidance.md` | Design guidance, rationale, best practices, contextual direction |
| `Procedure.md` | Step-by-step execution workflow, sequencing, checklists |

---

## 8. Decomposition Entities

The project decomposition document (produced by PROJECT_DECOMP) defines these additional entities:

| Entity | ID Format | Purpose |
|--------|-----------|---------|
| **Scope Item** | `SOW-NNN` | Atomic, testable scope statement from the Structured Scope of Work |
| **Objective** | `OBJ-NNN` | Success criterion derived from scope; mapped to supporting deliverables |
| **Vocabulary Map** | (table) | Canonical terms and synonyms to prevent semantic drift |
| **Scope Ledger** | (table) | Machine-checkable mapping of every scope item to packages and deliverables |
| **Coverage & Telemetry** | (summary) | Metrics (counts, gaps, open issues) that make decomposition quality measurable |

---

## 9. UI Navigation Vocabulary

The desktop frontend uses canonical UI terms for matrix routing and pipeline selection state.

### 9.1 Matrix Axes

| Type | Values | Meaning |
|------|--------|---------|
| `MatrixRow` | `NORMATIVE`, `OPERATIVE`, `EVALUATIVE` | Major intent lane used for routing to WORKBENCH or PIPELINE |
| `MatrixColumn` | `GUIDING`, `APPLYING`, `JUDGING`, `REVIEWING` | Role-oriented matrix column shared across all rows |

### 9.2 Pipeline Selectors

| Type | Values | Meaning |
|------|--------|---------|
| `PipelineCategory` | `DECOMP*`, `PREP*`, `TASK*`, `AUDIT*` | Top-level pipeline mode selected in the header |
| `TaskScopeMode` | `DELIVERABLES`, `KNOWLEDGE_TYPES` | Dynamic scope mode used only when `PipelineCategory=TASK*` |

### 9.3 Knowledge Decomposition Terms

| Term | Meaning |
|------|---------|
| **Knowledge decomposition marker** | A decomposition-document signal (e.g., headings/phrases containing `Knowledge Categories`, `Knowledge Types`, or equivalent marker text) that enables knowledge-type scope in TASK selectors. |
| **Knowledge type option** | A canonical file-type bucket (e.g., Datasheet, Specification, Guidance, Procedure, Dependencies, References, Context, Status, Semantic, Memory) returned by API scanning and selectable in TASK scope mode. |

---

## 10. Epistemic Labels

Agents use these labels in `Notes` fields and dependency records to distinguish knowledge certainty:

| Label | Meaning |
|-------|---------|
| `FACT` | Directly observed in source text with citation |
| `ASSUMPTION` | Reasonable inference not directly stated; requires validation |
| `PROPOSAL` | Agent suggestion; requires human decision to become binding |
| `TBD` | Unknown; placeholder requiring resolution |

---

EOF
