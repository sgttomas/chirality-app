# project-decomp — contract

## Non-negotiable invariants

- **Human-validated scope.** The agent prepares proposals and checks before
  three grouped human checkpoints: (1) basis, normalized scope, vocabulary, and
  objectives; (2) proposed Packages and Deliverables with coverage findings and
  exceptions; and (3) the audited final decomposition for downstream use.
  Internal analysis, repair, or asset-quality evidence does not add prompts.
- **Checkpoint snapshots.** Each accepted group finalizes a new immutable
  snapshot under `checkpoint_snapshots/` with `DECISION.md`,
  `ACCEPTED_MANIFEST.csv`, and `HANDOFF_STATE.md`, then updates that group's
  authorized pointer. Each later group consumes the preceding accepted
  snapshot rather than mutable working files alone.
- **No invention.** Do not create scope items, objectives, packages, deliverables, or artifacts beyond what the user’s intent supports. If unknown, mark `TBD` and surface as an open issue.
- **Packages are flat.** Do not create sub-packages. If more partitioning is needed, propose additional Packages.
- **No overlap / no gaps at the package level.** Every SSOW scope item must be assigned to exactly one Package (forced decision if ambiguous; human resolves at checkpoint group 2).
- **Design packages are discipline-exclusive.** Any Package that includes design work MUST correspond to exactly one discipline. If scope mixes design disciplines, split into multiple Packages so each design Package has one discipline.
- **Stable identifiers.** Once assigned, IDs must remain stable across revisions unless the user explicitly requests renumbering.
- **Deterministic DeliverableID ↔ PackageID coupling.**
  - Package IDs MUST be fixed-width: `PKG-XX` (2 digits, zero-padded; e.g., `PKG-12`).
  - Deliverable IDs MUST be fixed-width and mechanically derived from the parent package: `DEL-XX-YY_{shortDescription}`.
    - The first `XX` MUST equal the numeric portion of `ParentPackageID` / `PackageID`.
    - The `YY` is a sequential counter **unique within that package** (`01`, `02`, …).
  - Example: `PKG-12` → `DEL-12-03_Pre-commissioning-Installation`
  - `{shortDescription}` MUST be filesystem-safe (no spaces; use hyphens); SHOULD be kebab-case; once set, keep stable.
  - MUST NOT use the older dot style (`DEL-XX.YY_{...}`) or non–package-coupled IDs, because downstream folder paths and lookups assume deterministic mapping.
- **Design deliverables are artifact-kind based.** Within design Packages, Deliverables MUST be defined by distinct knowledge-artifact kinds (for example: drawing set, calculation package, specification set, model package). Repeated instances of a kind (for example: many sheets in one drawing set) MUST be represented as Artifacts under that Deliverable, not as separate Deliverables.
- **Objective mapping is best-effort.** Objectives are derived from SSOW. Unmapped objectives must be surfaced as open issues.
- **Traceable rationale.** Non-trivial assignment decisions must be recorded as explicit decisions in the decomposition output.
- **Production-contract boundary.** PROJECT deliverables declare anticipated
  artifacts and objective mappings without choosing legacy initialization.
  Downstream new production uses `SOW_V1`; DOMAIN/KTY and independent schemas
  remain outside this rule.

---

## Glossary (minimal)

- **SOW**: user’s messy scope of work (input).
- **SSOW**: structured scope of work (agent-produced, user-confirmed output).
- **Scope Item**: an atomic SSOW statement; the unit of coverage checking.
- **Package**: a flat partition of SSOW scope (no nesting).
- **Deliverable**: a unit of scope that produces value; belongs to exactly one Package; has a responsible party; has a type.
- **Artifact**: an anticipated tangible output that satisfies a Deliverable; artifacts must match deliverable type.
- **Objective**: a success condition derived from SSOW and satisfied through Deliverables (best-effort mapping).
- **Scope Ledger**: a table enumerating all scope items with stable IDs and explicit assignments/mappings.
- **Coverage & Telemetry**: a summary of counts and gaps that makes decomposition quality measurable and comparable over iterations.

---

## Package Architecture (PROJECT variant)

The `project-decomp` workflow conforms to the package architecture defined in `docs/DECOMPOSITION_STANDARD.md`. The PROJECT canonical working package consists of:

- one concise main decomposition document (the working surface)
- authoritative companion registers when heavy machine-truth warrants separate files (e.g., Scope Ledger CSV, objective mappings, coverage telemetry)
- `_ScopeChange/_LATEST.md` and the active amendment snapshot (when the project has been amended)

### Decomposition truth vs derivative review/publication bundle

The main decomposition document and any companion registers constitute **authoritative decomposition truth**. Any single-file review bundle, publication render, or formatted export assembled from these surfaces is a **derived publication artifact** and must not be treated as the primary amendment surface.

### When to use companion registers

Companion registers (CSV/JSON) SHOULD be used when:

- the Scope Ledger exceeds manageable inline size for the main document
- coverage telemetry, objective mappings, or open-issue registers benefit from machine-readable companion files
- downstream automation consumes structured data that is better maintained in a dedicated file

When companion registers exist, the main decomposition document should carry summaries and a companion inventory, not exhaustive duplicated truth.

---

## Validity

### Normative — "What must it be?"

This section defines requirements for a valid project decomposition.

### Completeness requirements

A decomposition is complete when:

| Requirement | Validation |
|---|---|
| Scope defined | SSOW exists; each scope item has an ID and in/out/TBD status |
| Objectives derived | Objectives list exists and is user-confirmed |
| Packages flat and scoped | Package list exists; each package has a scope description |
| Design package discipline exclusivity | Each package with design work declares exactly one discipline |
| Package coverage | Every Scope Item is assigned to exactly one Package |
| Deliverables defined | Deliverables exist within each Package with IDs, types, responsibilities (TBD allowed) |
| Design deliverable granularity | In design packages, deliverables are organized by knowledge-artifact kind (not per-instance) |
| Deliverable assignment | Every Deliverable belongs to exactly one Package |
| Artifacts anticipated | Each Deliverable lists anticipated artifacts (TBD allowed) |
| Scope Ledger present | Scope Ledger table exists with stable IDs and mappings |
| Coverage & Telemetry present | Summary metrics and open issue taxonomy exist |
| Vocabulary Map present | Canonical terms ↔ synonyms table exists |

### Consistency requirements

A decomposition is consistent when:

| Requirement | Validation |
|---|---|
| No scope overlaps | A scope item is not assigned to multiple packages |
| No scope gaps | No scope item remains unassigned to a package |
| Design discipline isolation | No design package contains more than one discipline |
| Design type/instance separation | In design packages, per-instance outputs are represented as artifacts under a kind-level deliverable |
| Stable IDs | IDs do not change across revisions unless explicitly requested |
| Terminology consistent | Canonical terms are used consistently; synonyms are mapped |
| Decisions explicit | Non-trivial assignment decisions are recorded and referencable |

### Anti-patterns (invalid outputs)

| Anti-pattern | Why it fails |
|---|---|
| Inventing scope items/objectives | Breaks grounding; corrupts downstream work |
| Nested packages | Breaks partition invariants; complicates automation |
| Mixed-discipline design package | Blurs discipline accountability and breaks discipline-based routing |
| Instance-level design deliverables | Inflates deliverable graph and obscures artifact-kind ownership |
| Silent ambiguity resolution | Hides defects; makes later reconciliation impossible |
| No stable IDs | Prevents tracking and longitudinal comparison |
| Missing scope ledger | Prevents machine-checkable coverage |
| Missing coverage telemetry | Prevents antifragile feedback over revisions |

## Artifacts and schemas

### Descriptive — "What is it?"

This section defines the entities and required tables in the decomposition output.

### Required entities

#### Scope Item
- `ScopeItemID` (stable; e.g., `SOW-0001`)
- `Statement` (normalized atomic scope statement)
- `InOutStatus` (`IN|OUT|TBD`)
- `SourceRef` (best-effort; `TBD` allowed)
- `Notes`

#### Objective
- `ObjectiveID` (stable; e.g., `OBJ-001`)
- `Statement`
- `Notes`
- `MappedDeliverables` (best-effort; may be empty but must be flagged)

#### Package
- `PackageID` (stable; e.g., `PKG-01`)
- `Name`
- `ScopeDescription`
- `Discipline` (required for design packages; exactly one discipline value)
- `InclusionCriteria` (optional)
- `Exclusions` (optional)

#### Deliverable
- `DeliverableID` (stable; follows `DEL-XX-YY_{shortDescription}`, e.g., `DEL-12-03_Pre-commissioning-Installation`)
- `Name`
- `ParentPackageID`
- `Description`
- `ResponsibleParty` (`TBD` allowed)
- `Type` (for design packages, this is the knowledge-artifact kind, e.g., drawing set / calculation package / specification set / model package)
- `AnticipatedArtifacts` (list; `TBD` allowed)
- `CoversScopeItems` (best-effort)
- `SupportsObjectives` (best-effort)

Optional downstream automation tags (non-breaking; only if explicitly provided):
- `CBSHint` (optional cost breakdown / cost category code; `TBD` allowed)
- `EstimateMethodHint` (`QUOTE|RATE_TABLE|HISTORICAL|PARAMETRIC|ALLOWANCE|TBD`) — only when explicitly stated by the human or source materials
- `StageHint` (optional stage label if the project uses stage concepts)

Rules:
- These fields are OPTIONAL and must not be invented.
- If absent, downstream agents must infer conservatively or treat as `TBD`.

#### Artifact
- `ArtifactID` (optional stable ID if helpful)
- `Name`
- `ParentDeliverableID`
- `Type` (must match deliverable type / knowledge-artifact kind; artifacts are instances of that kind)
- `Notes`

---

### Required tables/sections in the Decomposition Document

#### 1) Vocabulary Map (table)
Minimum columns:
- `CanonicalTerm`
- `Synonyms`
- `Notes`

#### 2) Scope Ledger (table)
Minimum columns:
- `ScopeItemID`
- `InOutStatus`
- `ScopeItemStatement`
- `SourceRef`
- `PackageID`
- `DeliverableID(s)` (one or many; or `TBD`)
- `ObjectiveID(s)` (zero or many; or `TBD`)
- `DecisionRef` (optional; points to Decision Log entry)
- `OpenIssue` (`TRUE|FALSE`)
- `Notes`

**Hard rule:** Every `ScopeItemID` has exactly one `PackageID`.

#### 3) Coverage & Telemetry (summary block)
Minimum fields:
- `ScopeItemCount`
- `PackageCount`
- `DeliverableCount`
- `ObjectiveCount`
- `UnassignedScopeItems` (must be 0 for acceptance)
- `ScopeItemsWithoutDeliverableMapping` (count)
- `UnmappedObjectives` (count)
- `OpenIssuesByType` (counts, with IDs)
- `Revision` identifier and date

#### 4) Open Issues list
- A list of unresolved items referencing stable IDs:
  - `SOW-####`, `OBJ-###`, `PKG-XX`, `DEL-XX-YY_{shortDescription}` pattern (e.g., `DEL-12-03_Pre-commissioning-Installation`)

#### 5) Decision Log / Change Log
- A small section where non-trivial choices are recorded so later work can trace why boundaries were set.

---
