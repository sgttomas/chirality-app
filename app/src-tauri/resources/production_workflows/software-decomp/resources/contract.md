# software-decomp — contract

## Precedence (conflict resolution)

This package follows this precedence order:

1. **PROTOCOL** — [method](method.md#method) governs sequencing and interaction
   rules.
2. **SPEC** — [Validity](#validity) governs pass/fail requirements.
3. **STRUCTURE** — [Artifacts and schemas](#artifacts-and-schemas) defines the
   allowed entities, relationships, and required sections.
4. **RATIONALE** — the stated purpose of this package governs interpretation
   when ambiguity remains.

If any instruction appears to conflict, do not silently reconcile. Surface the
conflict as a contradiction and request the human's resolution.

---

## Inputs and outputs

Inputs:

- The accepted software intent (for example, a PRD handed off by
  `software-prd` or a successor PRD handed off by
  `reverse-engineer-software`), identified by path, content hash, and the
  separate acceptance decision record, together with its accepted portions and
  shared constraints. Material outside the accepted portions is not accepted
  scope; see Group 1 preparation in the [method](method.md).
- Supporting requirements, tickets, notes, architecture, constraints, and prior
  decompositions named in the brief.

Outputs are written under `DECOMP_ROOT`, the `_Decomposition/` folder of the
project's `EXECUTION_ROOT` (often `execution/`):

| Output | Package role |
|---|---|
| Main decomposition document | working surface |
| `Deliverables.csv` | authoritative companion register, when registers are kept as files |
| `ScopeLedger.csv` | authoritative companion register, when registers are kept as files |
| `ContextBudgetQA.csv` | authoritative companion register, when registers are kept as files |
| `Companion_Inventory.csv` | optional file backing the main document's required companion-inventory section (filename, package role, description for every companion) |
| `{DECOMP_ROOT}/checkpoint_snapshots/<group>-<UTC>/{DECISION.md,ACCEPTED_MANIFEST.csv,HANDOFF_STATE.md}` | immutable accepted checkpoint snapshot |
| `{DECOMP_ROOT}/checkpoint_snapshots/_LATEST_GROUP1.md`, `_LATEST_GROUP2.md`, `_LATEST_ACCEPTED.md` | pointers to the accepted snapshots |

When registers are kept as companion files, use these headers, because the
register validator reads these names (list cells are separated by `;`):

- `Deliverables.csv`: `DeliverableID,PackageID,Name,Description,Type,ResponsibleParty,AnticipatedArtifacts,CoversScopeItems,SupportsObjectives,ContextEnvelope,ContextEnvelopeNotes,PhaseHint`
- `ScopeLedger.csv`: `ScopeItemID,InOutStatus,ScopeItemStatement,SourceRef,PackageID,DeliverableIDs,ObjectiveIDs,DecisionRef,OpenIssue,Notes`
- `ContextBudgetQA.csv`: `DeliverableID,PackageID,ContextEnvelope,Risk,RecommendedAction,Notes`

The entity fields below map to these columns: a Deliverable's `ParentPackageID`
is the `PackageID` column, and a Scope Item's `DeliverableID(s)` and
`ObjectiveID(s)` are the `DeliverableIDs` and `ObjectiveIDs` columns.

Before checkpoint groups 2 and 3, check the registers with
`python3 tools/validation/validate_decomposition_registers.py <EXECUTION_ROOT> --families XRG`
(report-only; XRG cross-checks `Deliverables.csv`, `ScopeLedger.csv`, and
`ContextBudgetQA.csv` independently of dependency storage or locality layout;
`--list-checks` lists the scope/objective/context checks).
Findings route repair or are presented as exceptions; they do not add a
checkpoint.

The accepted package is consumed downstream by `project-setup`, then by
`scope-of-work` with `MODE=INIT` for each deliverable's production contract.

---

## Dependency handoff to setup

Carry source-grounded needed inputs with the responsible consuming Deliverable,
the actual intended use/condition, relevant case or trigger, and the source
location. Keep an unknown producer/source explicitly unresolved. These are
inputs to the consumer's later local authoring, not producer commitments or a
complete execution network. Do not expand a general interface into every
producer/consumer pair or merge distinct uses because endpoints match.

After scope exists, `project-setup` uses `dependency-extract` to author actual
needs in each consumer's `deliverable.yaml` from scope and sources. Reverse links and undertaking-specific graphs are derived on demand.
Do not create an authoritative dependency graph or dependency CSV/Markdown
companions in decomposition. Existing scope, objective, coverage and context
registers retain their decomposition roles; technical holds and acceptance
remain with their actual authorities.

---

## Non-negotiable invariants

- **Human-validated scope.** The agent prepares proposals and checks before
  three grouped human checkpoints: (1) basis, normalized scope, vocabulary, and
  objectives; (2) proposed Packages and Deliverables with coverage findings and
  exceptions; and (3) the audited final decomposition for downstream use.
  Internal analysis and repair evidence does not add prompts.
  For a small, reversible undertaking the human may choose to decide all three
  groups in one sitting; the independent audit still precedes the decision
  and the three snapshots are still written in order (see the method).
- **Checkpoint snapshots.** Each accepted group finalizes a new immutable
  snapshot under `checkpoint_snapshots/` with `DECISION.md`,
  `ACCEPTED_MANIFEST.csv`, and `HANDOFF_STATE.md`, then updates that group's
  authorized pointer. Each later group consumes the preceding accepted
  snapshot rather than mutable working files alone (except in a combined
  review sitting, where snapshots are written in order after the decision).
- **No invention.** Do not create scope items, objectives, packages, deliverables, or artifacts beyond what the user’s intent supports. If unknown, mark `TBD` and surface as an open issue.
- **Packages are flat.** Do not create sub-packages.
- **No overlap / no gaps at the package level.** Every SSOW scope item, whether `IN`, `OUT` or `TBD`, must be assigned to exactly one Package as its accountable home (forced decision if ambiguous; human resolves at checkpoint group 2). Only IN items map to Deliverables; an OUT or TBD item keeps its Package home and `SourceRef` for traceability and needs no production mapping.
- **Deliverables are the smallest unit.** There is no task sub-level inside a deliverable. Therefore deliverables MUST be sized to be executable by a Type 2 specialist with bounded context.
- **Stable identifiers.** Once assigned, IDs must remain stable across revisions unless the human explicitly requests renumbering.
- **Identifier format.**
  - Packages: `PKG-XX` (two digits, zero-padded)
  - Deliverables: `DEL-XX-YY` (two digits for package, two digits within package)
  - Scope Items: `SOW-NNN`
  - Objectives: `OBJ-NNN`
  - Identifiers use hyphen separators (`DEL-01-01`, not `DEL-01.01`). `tools/validation/validate_id_format.sh` also accepts `SOW-` with four digits and an optional lowercase letter; that acceptance does not establish conformance, so check against the patterns above.
  - If other instruction sets or legacy materials require a different width (e.g., `PKG-XXX`), the agent MUST surface the mismatch as a contradiction and request a human ruling before proceeding.
  - Check ID format and coupling against these patterns (the register validator above reads deliverable folders as `DEL-\d{2}-\d{2}`). `tools/validation/validate_id_format.sh` accepts these forms (and 3-digit widths, so it does not flag `PKG-001` or enforce the 2-digit width; check the width against the patterns above); a rejection of a conforming ID by any checker is a tool defect to report, not a decomposition finding.
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
- **Context Envelope**: a size classification used to ensure a deliverable is agent-executable (see the ContextEnvelope rubric under [Artifacts and schemas](#artifacts-and-schemas)).
- **Thin end-to-end path**: the narrowest route through the proposed deliverables that exercises the combined result. It may cross packages and is not a package or a phase.
- **Coupled core**: deliverables whose shared interfaces are still being decided together, so that none can be examined with the others held still. They keep separate IDs and contracts and share one integration owner and one check.

---

## Package Architecture (SOFTWARE variant)

The output of `software-decomp` is a canonical working package, not a single monolithic document. The SOFTWARE canonical working package consists of:

- one concise main decomposition document (the working surface)
- authoritative companion registers when heavy machine-truth warrants separate files (e.g., Scope Ledger CSV, Context Budget QA, coverage telemetry)
- `_ScopeChange/_LATEST.md` and the active amendment snapshot (when the project has been amended)

### Preventing monolithic drift

As software decompositions grow companion analysis surfaces (context budget analyses, coverage telemetry), those surfaces SHOULD live in companion files rather than being embedded in the main decomposition document. Dependency views remain derived queries from local needs, rather than authoritative decomposition companions. The main document remains a concise control surface.

Any single-file review bundle, reporting dashboard, or publication render assembled from the modular package is a **derived publication artifact** and must be explicitly labeled as such. It must not silently become the authoritative amendment surface.

### Package-role labeling

All major decomposition outputs must declare their package role, using one of
four labels:

- the main decomposition document is the **working surface**
- any companion CSV/JSON files are **authoritative companion registers**
- an accepted checkpoint or amendment snapshot, or a handoff-state record, is a
  **snapshot / handoff artifact**
- any assembled review/publication bundles are **derived publication artifacts**

A companion register is authoritative for its machine-truth unless the package
explicitly documents otherwise.

---

## Validity

### Normative — "What must it be?"

This section defines requirements for a valid software development decomposition.

### Completeness requirements

A decomposition is complete when:

| Requirement | Validation |
|---|---|
| Scope defined | SSOW exists; each scope item has an ID and `IN|OUT|TBD` status |
| Objectives derived | Objectives list exists and is human-confirmed |
| Packages flat and domain-based | Package list exists; each package has a scope description that is a *work domain/category* (not a phase) |
| Package coverage | Every `ScopeItemID`, whether IN, OUT or TBD, is assigned to exactly one Package; only IN items map to Deliverables |
| Deliverables defined | Deliverables exist within each Package with IDs, types, responsibilities (TBD allowed) |
| Deliverable assignment | Every deliverable belongs to exactly one Package |
| Artifacts anticipated | Each deliverable lists anticipated artifacts (TBD allowed) |
| Scope Ledger present | Scope Ledger table exists with stable IDs and mappings |
| Coverage & Telemetry present | Summary metrics and open issue taxonomy exist |
| Vocabulary Map present | Canonical terms ↔ synonyms table exists |
| Context Budget QA present | Every deliverable has `ContextEnvelope`; `XL` items are split or explicitly accepted as open issues |
| Examination stated | For a decomposition begun under this text: the Examination and Integrated Path section exists; every deliverable has an expected examination or `TBD`; every objective has a check and a carrier, or `TBD`; the thin end-to-end path is named or stated absent; every `TBD`, and every deliverable with no inexpensive examination, is listed as an open issue |

### Consistency requirements

A decomposition is consistent when:

| Requirement | Validation |
|---|---|
| No scope overlaps | A scope item is not assigned to multiple packages |
| No scope gaps | No scope item, whether IN, OUT or TBD, remains unassigned to a package |
| Stable IDs | IDs do not change across revisions unless explicitly requested |
| Terminology consistent | Canonical terms are used consistently; synonyms are mapped |
| Decisions explicit | Non-trivial choices are recorded and referencable |
| Agent-executable deliverables | Deliverables are sized to be completed by a Type 2 specialist within bounded context; items that cannot be are flagged and gated |

### Package-role requirements

A decomposition declares its package roles when:

| Requirement | Validation |
|---|---|
| Package-role labeling | Every major output is labeled as working surface, authoritative companion register, snapshot / handoff artifact, or derived publication artifact |
| Companion inventory | The main decomposition document has a companion inventory section listing every companion register and its role |
| Authoritative surface declaration | The output states which surfaces are authoritative and which are derived |
| No unlabeled monolithic output | Any single-file render is labeled as a derived publication artifact |

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
| No stable IDs | Prevents tracking and comparison across revisions |
| Undeclared package roles | Downstream agents cannot tell authoritative surfaces from derived ones |
| Monolithic main document embedding heavy companion truth | Inflates the working surface, makes narrow diffs harder and invites disagreement with the companion registers |

## Artifacts and schemas

Size examples and file-count ranges are planning calibration, not model capability limits. Judge semantic coupling, context sufficiency, and verification demands against the actual undertaking; record current run constraints in its brief.


### Descriptive — "What is it?"

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
Minimum fields:
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
- `PackageID` (exactly one for every item, whether IN, OUT or TBD)
- `DeliverableID(s)` (IN items: one or many, or `TBD`; blank for OUT and TBD items)
- `ObjectiveID(s)` (zero or many; or `TBD`)
- `DecisionRef` (optional)
- `OpenIssue` (`TRUE|FALSE`)
- `Notes`

Hard rule: every `ScopeItemID`, whether IN, OUT or TBD, has exactly one
`PackageID`. Only IN items require Deliverable mappings; an OUT or TBD item's
home is for accountability and traceability.

#### 6) Coverage & Telemetry (summary block)
Minimum fields:
- `ScopeItemCount`
- `PackageCount`
- `DeliverableCount`
- `ObjectiveCount`
- `UnassignedScopeItems` (scope items of any status without a Package; must be 0 for acceptance)
- `ScopeItemsWithoutDeliverableMapping` (IN items)
- `UnmappedObjectives`
- `ContextEnvelopeCounts` (S/M/L/XL)
- `OpenIssuesByType` (counts + IDs)
- `Revision` + date

#### 7) Open Issues list
List unresolved items referencing stable IDs.

#### 8) Decision Log / Change Log
Record non-trivial boundary or sizing decisions.

#### 9) Examination and Integrated Path
A section of the main document. It adds no register column and no companion
file. It is required of a decomposition begun under this text. An earlier
accepted decomposition remains valid without it, including when it is later
amended. Minimum content:

- per Deliverable: `DeliverableID`, the expected examination and what it would
  observe (`TBD` allowed), and whether that examination is inexpensive enough
  to run repeatedly while the work is under way;
- per Objective: `ObjectiveID`, its check, and the Deliverable or integration
  owner that carries it (a check may be shared, and may be the thin path;
  `TBD` allowed);
- the thin end-to-end path and its carrier, or one line stating that the
  undertaking has no integrated path;
- any coupled core: member `DeliverableID`s, the integration owner, the shared
  check, and why separate checks would not serve.

These entries describe intended examination. Setup draws on them when it
authors each Deliverable's verification entries (`scope-of-work` defines the
kinds). They are not acceptance criteria and establish no result. Do not
invent an examination or an Objective's check; an unknown one is `TBD` and an
open issue.

#### 10) Companion Inventory
List every companion register and other major output with its filename,
package role and a one-line description, so that a later agent can tell which
surfaces are authoritative and which are derived. `Companion_Inventory.csv`
may back this section. A package with no companion files says so in one line.

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
