# software-decomp — contract

## Non-negotiable invariants

- **Human-validated scope.** The agent prepares proposals and checks before
  three grouped human checkpoints: (1) basis, normalized scope, vocabulary, and
  objectives; (2) proposed Packages and Deliverables with coverage findings and
  exceptions; and (3) the audited final decomposition for downstream use.
  Internal analysis and repair evidence does not add prompts.
- **Checkpoint snapshots.** Each accepted group finalizes a new immutable
  snapshot under `checkpoint_snapshots/` with `DECISION.md`,
  `ACCEPTED_MANIFEST.csv`, and `HANDOFF_STATE.md`, then updates that group's
  authorized pointer. Each later group consumes the preceding accepted
  snapshot rather than mutable working files alone.
- **No invention.** Do not create scope items, objectives, packages, deliverables, or artifacts beyond what the user’s intent supports. If unknown, mark `TBD` and surface as an open issue.
- **Packages are flat.** Do not create sub-packages.
- **No overlap / no gaps at the package level.** Every SSOW scope item must be assigned to exactly one Package (forced decision if ambiguous; human resolves at checkpoint group 2).
- **Deliverables are the smallest unit.** There is no task sub-level inside a deliverable. Therefore deliverables MUST be sized to be executable by a Type 2 specialist with bounded context.
- **Stable identifiers.** Once assigned, IDs must remain stable across revisions unless the human explicitly requests renumbering.
- **Identifier format must conform to the repo’s canonical SPEC/TYPES.**
  - Packages: `PKG-XX` (two digits, zero-padded)
  - Deliverables: `DEL-XX-YY` (two digits for package, two digits within package)
  - If other instruction sets or legacy materials require a different width (e.g., `PKG-XXX`), the agent MUST surface the mismatch as a contradiction and request a human ruling before proceeding.
- **Deterministic DeliverableID ↔ PackageID coupling.**
  - The first `XX` in `DEL-XX-YY` MUST equal the package numeric portion.
  - The `YY` is a sequential counter unique within that package (`01`, `02`, …).
- **Artifacts align to deliverable type.** Anticipated artifacts must match the deliverable’s declared type (or be declared as sub-artifacts within a software artifact taxonomy).
- **Objective mapping is best-effort.** Objectives are derived from SSOW. Unmapped objectives must be surfaced as open issues.
- **Traceable rationale.** Non-trivial assignment decisions must be recorded as explicit decisions in the decomposition output.

---

## Glossary (software-focused, minimal)

- **SOW**: user’s messy scope of work (input).
- **SSOW**: structured scope of work (agent-produced, user-confirmed output).
- **Scope Item**: an atomic SSOW statement; unit of coverage checking.
- **Work Domain Package**: a flat partition of scope by *category/domain of work* (not a phase), chosen to minimize the context needed to work within it.
- **Deliverable**: the smallest unit of production; sized so a specialist agent can complete it within a bounded context window.
- **Artifact**: a tangible output produced by a deliverable (code, tests, config, docs, scripts, schemas).
- **Objective**: a success condition derived from SSOW and satisfied through deliverables (best-effort mapping).
- **Context Envelope**: a size classification used to ensure a deliverable is agent-executable (see STRUCTURE).

---

## Package Architecture (SOFTWARE variant)

The `software-decomp` workflow conforms to the package architecture defined in `docs/DECOMPOSITION_STANDARD.md`. The SOFTWARE canonical working package consists of:

- one concise main decomposition document (the working surface)
- authoritative companion registers when heavy machine-truth warrants separate files (e.g., Scope Ledger CSV, Context Budget QA, coverage telemetry)
- `_ScopeChange/_LATEST.md` and the active amendment snapshot (when the project has been amended)

### Preventing monolithic drift

As software decompositions grow companion analysis surfaces (dependency graphs, context budget analyses, coverage telemetry), those surfaces SHOULD live in companion files rather than being embedded in the main decomposition document. The main document remains a concise control surface.

Any single-file review bundle, reporting dashboard, or publication render assembled from the modular package is a **derived publication artifact** and must be explicitly labeled as such. It must not silently become the authoritative amendment surface.

### Package-role labeling

All major decomposition outputs must declare their package role:

- the main decomposition document is the **working surface**
- any companion CSV/JSON files are **authoritative companion registers**
- any assembled review/publication bundles are **derived publication artifacts**

---

## Validity

### Normative — \"What must it be?\"

This section defines requirements for a valid software development decomposition.

### Completeness requirements

A decomposition is complete when:

| Requirement | Validation |
|---|---|
| Scope defined | SSOW exists; each scope item has an ID and `IN|OUT|TBD` status |
| Objectives derived | Objectives list exists and is human-confirmed |
| Packages flat and domain-based | Package list exists; each package has a scope description that is a *work domain/category* (not a phase) |
| Package coverage | Every `ScopeItemID` is assigned to exactly one Package |
| Deliverables defined | Deliverables exist within each Package with IDs, types, responsibilities (TBD allowed) |
| Deliverable assignment | Every deliverable belongs to exactly one Package |
| Artifacts anticipated | Each deliverable lists anticipated artifacts (TBD allowed) |
| Scope Ledger present | Scope Ledger table exists with stable IDs and mappings |
| Coverage & Telemetry present | Summary metrics and open issue taxonomy exist |
| Vocabulary Map present | Canonical terms ↔ synonyms table exists |
| Context Budget QA present | Every deliverable has `ContextEnvelope`; `XL` items are split or explicitly accepted as open issues |

### Consistency requirements

A decomposition is consistent when:

| Requirement | Validation |
|---|---|
| No scope overlaps | A scope item is not assigned to multiple packages |
| No scope gaps | No scope item remains unassigned to a package |
| Stable IDs | IDs do not change across revisions unless explicitly requested |
| Terminology consistent | Canonical terms are used consistently; synonyms are mapped |
| Decisions explicit | Non-trivial choices are recorded and referencable |
| Agent-executable deliverables | Deliverables are sized to be completed by a Type 2 specialist within bounded context; items that cannot be are flagged and gated |

### Anti-patterns (invalid outputs)

| Anti-pattern | Why it fails |
|---|---|
| Packages are phases (e.g., “Phase 1/2/3”) | Packages must be domain partitions, not a timeline layer |
| Deliverables are epic-sized capabilities | Deliverables are the smallest unit; downstream agents cannot safely execute them |
| Cross-domain “god deliverables” | Violates bounded-context intent; must be split across packages |
| Inventing scope items/objectives | Breaks grounding; corrupts downstream work |
| Nested packages | Breaks flat partition invariants |
| Silent ambiguity resolution | Hides defects; blocks later reconciliation |
| Missing scope ledger / telemetry | Prevents machine-checkable coverage and iteration quality |

## Artifacts and schemas

Size examples and file-count ranges are planning calibration, not model capability limits. Judge semantic coupling, context sufficiency, and verification demands against the actual undertaking; record current run constraints in its brief.


### Descriptive — \"What is it?\"

This section defines the entities and required tables in the decomposition output.

### Required entities

#### Scope Item
- `ScopeItemID` (stable; e.g., `SOW-003`)
- `Statement` (atomic scope statement)
- `InOutStatus` (`IN|OUT|TBD`)
- `SourceRef` (best-effort; `TBD` allowed)
- `Notes`

#### Objective
- `ObjectiveID` (stable; e.g., `OBJ-001`)
- `Statement`
- `Notes`
- `MappedDeliverables` (best-effort; may be empty but must be flagged)

#### Package (Work Domain)
- `PackageID` (stable; `PKG-XX`)
- `Name`
- `ScopeDescription` (work category/domain; must not be a phase)
- `InclusionCriteria` (optional)
- `Exclusions` (optional)

#### Deliverable (Agent-executable unit)
Minimum fields (in addition to the project-global deliverable fields):
- `DeliverableID` (stable; `DEL-XX-YY`)
- `Name`
- `ParentPackageID`
- `Description`
- `ResponsibleParty` (`TBD` allowed)
- `Type` (software-oriented deliverable type; see taxonomy below)
- `AnticipatedArtifacts` (list; `TBD` allowed)
- `CoversScopeItems` (best-effort)
- `SupportsObjectives` (best-effort)
- `ContextEnvelope` (`S|M|L|XL`) — REQUIRED for this agent
- `ContextEnvelopeNotes` (why it is sized as such; MUST be present when `L` or `XL`)

##### ContextEnvelope rubric (guidance; used in QA)
- `S` (Small): single subsystem; ≤ ~5 files touched; one primary change + tests/docs; minimal dependencies.
- `M` (Medium): single subsystem; ≤ ~15 files touched; one cohesive feature slice; clear acceptance tests.
- `L` (Large): still single package/domain, but may involve multiple components within that domain; SHOULD be split if possible.
- `XL` (Too large): cross-domain or broad refactor; MUST be split, or explicitly accepted as an exception at checkpoint group 2 and carried into the final audit.

#### Artifact (software-aware)
Artifacts are anticipated tangible outputs. They MAY be listed plainly or structured.

Optional structured artifact fields (only if useful):
- `ArtifactID` (optional)
- `Name`
- `ParentDeliverableID`
- `Type` (suggested software taxonomy: `CODE|TEST|DOC|CONFIG|MIGRATION|SCRIPT|OTHER`)
- `Notes`

Rules:
- Do not invent artifact details. If unknown, use `TBD`.

---

### Required sections / tables in the Decomposition Document

#### 1) Vocabulary Map (table)
Columns:
- `CanonicalTerm`
- `Synonyms`
- `Notes`

#### 2) SSOW (list or table)
Minimum: atomic scope items with IDs and `IN|OUT|TBD`.

#### 3) Packages (table or grouped sections)
Minimum: `PackageID`, `Name`, `ScopeDescription`, and inclusion/exclusion notes.

#### 4) Deliverables (tables grouped by Package)
Minimum: deliverable fields above + `ContextEnvelope`.

#### 5) Scope Ledger (table)
Minimum columns:
- `ScopeItemID`
- `InOutStatus`
- `ScopeItemStatement`
- `SourceRef`
- `PackageID`
- `DeliverableID(s)` (one or many; or `TBD`)
- `ObjectiveID(s)` (zero or many; or `TBD`)
- `DecisionRef` (optional)
- `OpenIssue` (`TRUE|FALSE`)
- `Notes`

Hard rule: every `ScopeItemID` has exactly one `PackageID`.

#### 6) Coverage & Telemetry (summary block)
Minimum fields:
- `ScopeItemCount`
- `PackageCount`
- `DeliverableCount`
- `ObjectiveCount`
- `UnassignedScopeItems` (must be 0 for acceptance)
- `ScopeItemsWithoutDeliverableMapping`
- `UnmappedObjectives`
- `ContextEnvelopeCounts` (S/M/L/XL)
- `OpenIssuesByType` (counts + IDs)
- `Revision` + date

#### 7) Open Issues list
List unresolved items referencing stable IDs.

#### 8) Decision Log / Change Log
Record non-trivial boundary or sizing decisions.

---

### Deliverable type taxonomy (software-oriented; suggestive, not mandatory)

Use these values (or project-specific equivalents) to keep deliverable types legible:

- `REQ_SLICE` — requirement/acceptance criteria slice
- `UX_UI_SLICE` — UI/UX component/view slice
- `API_CONTRACT` — endpoint/contract definition (OpenAPI/TS types/etc.)
- `BACKEND_FEATURE_SLICE` — backend behavior slice (single bounded feature)
- `DATA_MODEL_CHANGE` — schema/model change (with migration/rollback notes)
- `MIGRATION_SCRIPT` — migration job/one-off data movement tool
- `TEST_SUITE` — unit/integration/e2e test additions for a bounded behavior set
- `CI_CD_CHANGE` — pipeline/build/release config change
- `OBSERVABILITY` — logging/metrics/tracing additions for a bounded surface
- `SECURITY_CONTROL` — authn/authz, secrets, hardening, policy enforcement
- `DOC_UPDATE` — developer/user documentation update

Rule: if the SOW explicitly requires a different type naming scheme, adopt it and record in the Vocabulary Map.
