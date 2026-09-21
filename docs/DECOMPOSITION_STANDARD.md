# Decomposition Standard

> **Status: PROSPECTIVE CHIRALITY V3 AMENDMENT — implementation authorized by
> the owner on 2026-09-09.** The owner approved implementing the named grouped
> checkpoint design. These candidate bytes do not themselves constitute final
> acceptance, downstream qualification, release, or project-loop adoption. Until
> the prospective amendment is accepted through its governing closeout, the
> D-GOV-14 edition at commit `ee35409f5cf3a81ecb29a271527156b991df97b9`
> remains the ratified decomposition protocol.

This normative document defines the invariant protocol, validity requirements,
entity schemas, and required output sections shared by decomposition workflows
in this framework. It is an external constraint on runtime agents, not an
agent, persona, or delegation position.

The `project-decomp`, `software-decomp`, and `domain-decomp` workflows, and
future decomposition workflows, MUST conform to this standard and extend it
with domain-specific semantics. HELPS_HUMANS provides conversational design
and conformance assistance for decomposition components; WORKING_ITEMS
coordinates their execution.

Where a conforming workflow package disagrees with this standard,
surface the conflict and apply the repository's authority and conflict rules.

---

## Conforming workflows

The following central workflows currently conform to this specification:

| Workflow | Domain | Partition Entity | Production Unit Entity | ID Width |
|---|---|---|---|---|
| **project-decomp** | EPC / design-build projects | Package (`PKG-XX`) | Deliverable (`DEL-XX-YY_{desc}`) | 2-digit |
| **software-decomp** | Software development | Package (`PKG-XX`) | Deliverable (`DEL-XX-YY`) | 2-digit |
| **domain-decomp** | Handbook / knowledge domains | Category (`CAT-###`) | Knowledge Type (`KTY-CC-TT_{desc}`) | 2–3 digit |

Each conforming workflow binds the abstract entities defined in this
specification to domain-specific names, ID formats, type taxonomies, and
stage-level actions. See **Extension contract** in STRUCTURE.

---

## Precedence (conflict resolution)

All conforming workflows MUST use this precedence order:

1. **PROTOCOL** governs sequencing and interaction rules (how to run the process).
2. **SPEC** governs validity (pass/fail requirements; what is considered correct).
3. **STRUCTURE** defines the allowed entities and relationships (the ontology / schemas).
4. **RATIONALE** governs interpretation when ambiguity remains (values/intent).

If any instruction appears to conflict, do not silently reconcile. Surface the conflict as a contradiction and request user resolution.

---

## Non-negotiable invariants

These invariants MUST hold across all conforming decomposition workflows,
regardless of domain.

- **I1 — Human-validated decomposition.** Agents prepare the proposed state and
  relevant checks before each required human checkpoint. PROJECT and SOFTWARE
  use three grouped checkpoints. DOMAIN uses one combined source-admission and
  source-fidelity checkpoint before atomization, followed by three grouped
  checkpoints expressed in domain terms. A required checkpoint may not be
  skipped or multiplied merely because a tool or asset-quality check produced
  evidence.
- **I2 — No invention.** Do not create atomic units, objectives, partitions, production units, or artifacts beyond what the source material and user intent support. If unknown, mark `TBD` and surface as an open issue.
- **I3 — Partitions are flat.** Do not create nested partitions. If more granularity is needed, propose additional partitions at the same level.
- **I4 — No overlap / no gaps at the partition level.** Every IN-scope atomic unit MUST be assigned to exactly one partition. Forced decision if ambiguous; human resolves at the applicable grouped checkpoint.
- **I5 — Stable identifiers.** Once assigned, IDs MUST remain stable across revisions unless the human explicitly requests renumbering.
- **I6 — Deterministic production-unit ID ↔ partition ID coupling.** The production unit ID MUST be mechanically derived from its parent partition ID. The coupling format is domain-specific (defined by the conforming workflow) but the coupling itself is invariant.
- **I7 — Objective mapping is best-effort.** Objectives are derived from the source material. Unmapped objectives MUST be surfaced as open issues.
- **I8 — Traceable rationale.** Non-trivial assignment decisions MUST be recorded as explicit decisions in the decomposition output.
- **I9 — Ledger + telemetry.** Every decomposition MUST include a machine-checkable ledger and a Coverage & Telemetry summary. These make coverage provable and quality comparable across revisions.
- **I10 — Vocabulary discipline.** Every decomposition MUST include a Vocabulary Map. Canonical terms are used consistently; synonyms are mapped; semantic drift is prevented.

---

## Abstract glossary

These are the abstract entity names used in this specification. Conforming agents bind them to domain-specific names.

| Abstract Entity | Role | Examples (concrete bindings) |
|---|---|---|
| **Source Corpus** | The input material to be decomposed | SOW (PROJECT, SOFTWARE); Handbook (DOMAIN) |
| **Structured Outline** | The normalized, decomposed representation of the source | SSOW (PROJECT, SOFTWARE); SDO (DOMAIN) |
| **Atomic Unit** | A single normalized statement extracted from the source; the unit of coverage checking | Scope Item (PROJECT, SOFTWARE); Handbook Unit (DOMAIN) |
| **Partition** | A flat grouping of atomic units; no nesting, no overlaps, no gaps | Package (PROJECT, SOFTWARE); Category (DOMAIN) |
| **Production Unit** | An operational unit within a partition that produces tangible outputs; belongs to exactly one partition | Deliverable (PROJECT, SOFTWARE); Knowledge Type (DOMAIN) |
| **Artifact** | An anticipated tangible output of a production unit | Artifact (PROJECT, SOFTWARE); Knowledge Subject (DOMAIN) |
| **Objective** | A success condition derived from the source material | Objective (all) |
| **Decomposition Ledger** | A table proving coverage: every atomic unit mapped to partitions and production units | Scope Ledger (PROJECT, SOFTWARE); Domain Ledger (DOMAIN) |
| **Coverage & Telemetry** | A structured summary of counts and gaps | Coverage & Telemetry (all) |

---

## Package Architecture

### Canonical working package

The normative output of every conforming decomposition workflow is a **canonical working package**, not a single monolithic document. A canonical working package consists of:

- one concise main decomposition document (the control surface)
- zero or more **authoritative companion registers** (CSV, JSON, or structured markdown files holding heavy machine-truth)
- `_ScopeChange/_LATEST.md` and the active amendment snapshot (when the root has been amended)

The main decomposition document is a concise control surface. It contains status, objectives, vocabulary highlights, partition and production-unit summaries, high-level telemetry, open issues, and a decision/change log. It should not embed the full decomposition ledger or exhaustive derivative tables when that same truth already lives in companion files.

### Authoritative companion register

An **authoritative companion register** is a CSV, JSON, or structured markdown file that holds heavy machine-truth as the primary working surface for that data. Examples include:

- decomposition ledger (the row-level unit-to-partition-to-production-unit mapping table)
- partition register / telemetry
- production-unit register
- artifact / subject register
- objective register / objective mappings
- open issues register
- validation checks
- vocabulary map
- node summary / coverage telemetry

When a companion register exists for a given truth surface, the companion register is authoritative for machine-truth unless explicitly documented otherwise. Duplication of that truth in the main document must be intentional and justified.

### Derived publication artifact

A **derived publication artifact** is any single-file render, publication bundle, or review document assembled from the modular package. Examples include monolithic full-package renders, publication bundles, and formatted review documents.

Derived publication artifacts:
- are not the amendment surface
- may be regenerated deterministically from the canonical working package
- must be explicitly labeled as derived and non-authoritative for amendment work

### Package-role label

Every major decomposition artifact should declare its role using one of these labels:

| Label | Meaning |
|---|---|
| `working surface` | The main decomposition document; the primary human-facing control surface |
| `authoritative companion register` | A companion file holding heavy machine-truth as the primary working surface for that data |
| `snapshot / handoff artifact` | An immutable amendment snapshot or handoff-state record |
| `derived publication artifact` | A render, bundle, or review document assembled from the modular package; not the amendment surface |

### Modular packages are the preferred default

Conforming decomposition workflows MUST default to producing modular working packages. Heavy machine-truth (ledgers, registers, telemetry, objective mappings) SHOULD live in companion files rather than being embedded in the main decomposition document.

If a conforming workflow produces a monolithic single-file output for publication or review purposes, that output MUST be declared as a derived publication artifact and MUST NOT be treated as the authoritative amendment surface.

---

[[BEGIN:PROTOCOL]]
## PROTOCOL — Abstract Decomposition Protocol

### Operational — "How to do?"

Conforming decomposition workflows perform the preparation stages below and
stop only at the grouped human checkpoints. A stage may contain deterministic
checks, repair loops, or bounded TASK assignments. Those operations produce the
evidence presented at a checkpoint; they do not create extra approval prompts.
Conforming workflows extend each stage with domain-specific actions and outputs.

After every required human checkpoint is accepted, finalize a new immutable
checkpoint snapshot before beginning the next stage. The snapshot contains the
recorded decision, an accepted artifact manifest with hashes and package roles,
and a handoff state naming its upstream basis, derivative status, closure
verdict, rerun requirements, and blockers. Update only that checkpoint's
authorized pointer after the snapshot is complete. The next stage resolves and
consumes that accepted snapshot; it does not rely on the mutable working package
alone. Reopened decisions produce successor snapshots and never overwrite an
earlier accepted snapshot.

### Output Target

The agent maintains the canonical working package and revises its working
surface and authoritative companion registers after human feedback until the
required checkpoints pass.

### Preparation stages and checkpoints

#### Stage A — Establish and normalize the basis

Collect the source corpus, constraints, references, and prior accepted state.
Normalize content into atomic units with stable IDs and `IN | OUT | TBD`
classification. Develop the Vocabulary Map. For PROJECT and SOFTWARE, derive
testable objectives and map them to atomic units on a best-effort basis.

Before asking for a decision, the agent prepares the full basis package,
identifies unsupported or conflicting interpretations, and runs available
structural checks.

**PROJECT/SOFTWARE checkpoint group 1 — basis, normalized scope, vocabulary,
and objectives.** The human confirms this group as the basis for structural
proposals.

**DOMAIN pre-atomization checkpoint — source admission and fidelity.** DOMAIN
first presents the proposed admitted corpus together with source-fidelity and
asset-quality evidence as one combined checkpoint. Repair loops occur before
the checkpoint where possible. Asset-quality evidence routes repairs and is
included in the package; it does not create separate human prompts. Atomization
begins only after the human accepts the admitted source basis and its fidelity
posture.

**DOMAIN checkpoint group 1 — normalized scope and meaning.** After
atomization, the human confirms the Handbook Units, `IN | OUT | TBD`
classifications, source bindings, Vocabulary Map, and surfaced meaning
conflicts as the normalized representation of the admitted corpus.

#### Stage B — Propose the structure

Propose flat partitions and assign every IN-scope atomic unit to exactly one.
If a unit would overlap, split it with human-visible provenance or present the
forced boundary decision. Define production units within their parent
partitions with stable coupled IDs, responsibility, type, anticipated artifacts,
and best-effort mappings. Run coverage, cohesion, sizing, and referential checks
before presenting the proposal; surface all exceptions and open issues.

**PROJECT/SOFTWARE checkpoint group 2 — proposed packages/deliverables,
coverage findings, and exceptions.** The human decides the proposed structure
with its coverage evidence and unresolved exceptions together.

**DOMAIN checkpoint group 2 — Category, Knowledge Type, and Knowledge Subject
structure.** The human decides the proposed domain structure with its
retrieval-assisted cohesion evidence, mappings, coverage findings, and
exceptions together.

#### Stage C — Audit and prepare the final package

Incorporate the preceding decisions, assemble the canonical working package,
and dispatch a separate review instance that did not author the candidate. Show
the final identifiers, mappings, coverage, telemetry, open issues, companion
inventory, and change record. Publication or output writing occurs around the
accepted state and does not add a checkpoint.

**PROJECT/SOFTWARE checkpoint group 3 — audited final decomposition accepted
for downstream use.** The human accepts the reviewed package as the basis for
downstream work.

**DOMAIN checkpoint group 3 — audited final acceptance.** The human accepts
the reviewed domain package as the basis for downstream work.

If the material basis changes after a checkpoint, reopen only the decisions
whose warrants, mappings, or consequences are affected. Refresh dependent
checks before returning to the next applicable checkpoint; do not replay
unaffected decisions.

[[END:PROTOCOL]]

---

[[BEGIN:SPEC]]
## SPEC — Validity Requirements

### Normative — "What must it be?"

These requirements apply to all conforming decomposition workflows.
Domain-specific variants MAY add requirements; they MUST NOT weaken these.

### Completeness requirements

A decomposition is complete when:

| Requirement | Validation |
|---|---|
| Source normalized | Atomic unit list exists; each unit has an ID and `IN\|OUT\|TBD` status |
| Objectives derived | Objectives list exists and is human-confirmed |
| Partitions flat and scoped | Partition list exists; each partition has a scope description |
| Partition coverage | Every IN-scope atomic unit is assigned to exactly one partition |
| Production units defined | Production units exist within each partition with IDs, types, responsibilities (`TBD` allowed) |
| Production unit assignment | Every production unit belongs to exactly one partition |
| Artifacts anticipated | Each production unit lists anticipated artifacts (`TBD` allowed) |
| Decomposition Ledger present | Ledger table exists with stable IDs and mappings |
| Coverage & Telemetry present | Summary metrics and open issue taxonomy exist |
| Vocabulary Map present | Canonical terms, synonyms, and notes table exists |

### Consistency requirements

A decomposition is consistent when:

| Requirement | Validation |
|---|---|
| No overlaps | An IN-scope atomic unit is not assigned to multiple partitions |
| No gaps | No IN-scope atomic unit remains unassigned to a partition |
| Stable IDs | IDs do not change across revisions unless explicitly requested |
| ID coupling | Production unit IDs are mechanically derived from parent partition IDs |
| Terminology consistent | Canonical terms are used consistently; synonyms are mapped |
| Decisions explicit | Non-trivial assignment decisions are recorded and referenceable |

### Package-role requirements

A decomposition output declares its package roles when:

| Requirement | Validation |
|---|---|
| Package-role labeling | Every major output artifact is labeled as working surface, authoritative companion register, snapshot/handoff artifact, or derived publication artifact |
| Companion inventory | The main decomposition document includes a companion inventory section listing all companion registers and their roles |
| Authoritative surface declaration | The output explicitly declares which surfaces are authoritative vs derived |
| No unlabeled monolithic output | Any single-file monolithic render is explicitly labeled as a derived publication artifact, not left ambiguous |

Conforming agents MAY add domain-specific package-role requirements. They MUST NOT weaken these.

### Anti-patterns (invalid outputs)

| Anti-pattern | Why it fails |
|---|---|
| Inventing atomic units, objectives, or content | Breaks grounding; corrupts downstream work |
| Nested partitions | Breaks flat partition invariants; complicates automation |
| Silent ambiguity resolution | Hides defects; makes later reconciliation impossible |
| No stable IDs | Prevents tracking and longitudinal comparison |
| Missing Decomposition Ledger | Prevents machine-checkable coverage |
| Missing Coverage & Telemetry | Prevents anti-fragile feedback over revisions |
| Undeclared package roles | Prevents downstream agents from distinguishing authoritative surfaces from derived artifacts |
| Monolithic main doc embedding heavy companion truth | Inflates the control surface; makes targeted retrieval and narrow diffs harder; invites parity failures with companion registers |

Conforming agents MAY add domain-specific anti-patterns. They MUST NOT remove these.

[[END:SPEC]]

---

[[BEGIN:STRUCTURE]]
## STRUCTURE — Required Entities, Sections, and Schemas

### Descriptive — "What is it?"

This section defines the abstract entity schemas and required output sections. Conforming agents bind these to domain-specific names and MAY add domain-specific fields.

### Required entities (abstract)

#### Atomic Unit
- `UnitID` (stable; format defined by conforming workflow)
- `Statement` (normalized atomic statement)
- `InOutStatus` (`IN|OUT|TBD`)
- `SourceRef` (best-effort; `TBD` allowed)
- `Notes`

#### Objective
- `ObjectiveID` (stable; `OBJ-NNN`)
- `Statement`
- `Notes`
- `MappedProductionUnits` (best-effort; may be empty but must be flagged)

#### Partition
- `PartitionID` (stable; format defined by conforming workflow)
- `Name`
- `ScopeDescription`
- `InclusionCriteria` (optional)
- `Exclusions` (optional)

#### Production Unit
- `ProductionUnitID` (stable; mechanically coupled to `ParentPartitionID`; format defined by conforming workflow)
- `Name`
- `ParentPartitionID`
- `Description`
- `ResponsibleParty` (`TBD` allowed)
- `Type` (domain-specific taxonomy defined by conforming workflow)
- `AnticipatedArtifacts` (list; `TBD` allowed)
- `CoversUnits` (best-effort; atomic unit IDs)
- `SupportsObjectives` (best-effort; objective IDs)

Conforming workflows MAY add fields (for example, `ContextEnvelope` in
`software-decomp`, `CanonicalSchema` in `domain-decomp`, or `CBSHint` in
`project-decomp`). Added fields MUST NOT conflict with the base schema.

#### Artifact
- `ArtifactID` (optional stable ID)
- `Name`
- `ParentProductionUnitID`
- `Type` (domain-specific taxonomy defined by conforming workflow)
- `Notes`

---

### Required sections in the Decomposition Document

Every conforming workflow's output MUST include these sections. Order is recommended but not mandatory.

#### 1) Vocabulary Map (table)
Minimum columns:
- `CanonicalTerm`
- `Synonyms`
- `Notes`

#### 2) Decomposition Ledger (table)
Minimum columns:
- `UnitID`
- `InOutStatus`
- `UnitStatement`
- `SourceRef`
- `PartitionID` (required for IN; blank for OUT)
- `ProductionUnitID(s)` (one or many; or `TBD`)
- `ObjectiveID(s)` (zero or many; or `TBD`)
- `DecisionRef` (optional; points to Decision Log entry)
- `OpenIssue` (`TRUE|FALSE`)
- `Notes`

**Hard rule:** every IN-scope `UnitID` has exactly one `PartitionID`.

Conforming workflows use domain-specific column names (for example,
`ScopeItemID` / `PackageID` / `DeliverableID(s)` in `project-decomp`, or
`UnitID` / `CategoryID` / `KnowledgeTypeID(s)` in `domain-decomp`). The
structural contract — every IN unit maps to exactly one partition — is invariant.

#### 3) Coverage & Telemetry (summary block)
Minimum fields:
- `UnitCount`
- `PartitionCount`
- `ProductionUnitCount`
- `ObjectiveCount`
- `UnassignedINUnits` (must be 0 for acceptance)
- `UnitsWithoutProductionUnitMapping` (count)
- `UnmappedObjectives` (count)
- `OpenIssuesByType` (counts, with IDs)
- `Revision` identifier and date

Conforming workflows MAY add domain-specific telemetry fields (for example,
`ContextEnvelopeCounts` in `software-decomp`). They MUST NOT omit the base fields.

#### 4) Open Issues list
Unresolved items referencing stable IDs.

#### 5) Decision Log / Change Log
Non-trivial assignment and boundary decisions, recorded so later work can trace rationale.

---

### Extension contract (what a conforming workflow MUST provide)

When creating a new decomposition workflow that conforms to this standard, its
package MUST:

1. **Reference this standard.** State conformance to `docs/DECOMPOSITION_STANDARD.md`.
2. **Bind abstract entities to domain-specific names.** Provide a glossary that maps Source Corpus, Atomic Unit, Partition, Production Unit, and Artifact to domain-specific terms.
3. **Define ID formats.** Specify the stable ID format and width for each entity (partition IDs, production unit IDs, atomic unit IDs).
4. **Define the production-unit type taxonomy.** Provide the domain-specific type values (e.g., `API_CONTRACT`, `BACKEND_FEATURE_SLICE` for software; `Procedure`, `Checklist`, `Template` for knowledge domains).
5. **Extend stage actions.** Add domain-specific actions and outputs while
   preserving the applicable grouped checkpoint semantics and count.
6. **Declare execution restrictions when needed.** Put workflow-specific
   capability or command restrictions in `execution.json`; actual writes remain
   supplied by the run brief and host.
7. **Add domain-specific fields, anti-patterns, and SPEC requirements** as needed. These extend the base; they do not replace it.
8. **Declare domain-specific telemetry fields** beyond the base Coverage & Telemetry schema.

9. **Declare package architecture.** Specify which output surfaces are authoritative working surfaces, which are authoritative companion registers, and which (if any) are derived publication artifacts. Include a companion inventory section in the main decomposition document so downstream agents can discover the package layout.

A conforming workflow SHOULD also:
- Include domain-specific rationale explaining why the extensions exist.
- Document any deviations from the base specification with explicit justification.

[[END:STRUCTURE]]

---

[[BEGIN:RATIONALE]]
## RATIONALE

### Why a base specification exists

The decomposition method — intake, normalize, partition, operationalize,
verify, and prepare accepted output — is broadly invariant across domains. The
three central decomposition workflows share the precedence order, the
non-negotiable invariants, the required output sections (ledger, telemetry,
vocabulary map, open issues, decision log), and the completeness and
consistency requirements.

Variants express preparation stages through their own ontology while preserving
the checkpoint contract above. DOMAIN omits the Objectives layer because domain
knowledge handbooks rarely state explicit decomposable objectives; principles,
goals, and intent are absorbed into Knowledge Types of `Guidance / Playbook`
schema. This changes the domain entities within the grouped checkpoints, not the
requirement for human confirmation. See `workflows/domain-decomp/WORKFLOW.md`
and its variant contract.

The remaining differences across variants are in domain-specific semantics: what entities are called, how IDs are formatted, what type taxonomies apply, and what domain-specific constraints are added (e.g., Context Envelope for software sizing).

Extracting the invariant protocol into a normative standard:
- **Reduces duplication.** The shared contract is defined once and referenced, not copy-pasted.
- **Makes conformance auditable.** New decomposition variants can be checked against the base specification for completeness and consistency.
- **Clarifies what is invariant vs what is domain-specific.** The extension contract makes the boundary explicit, preventing accidental drift where one variant evolves a structural change that the others don't track.
- **Supports future variants.** A new decomposition workflow for a different domain (e.g., regulatory compliance, curriculum design, research programs) can conform to this specification and inherit the full protocol with only domain-specific extensions required.

### What stays in the concrete variants

Domain-specific content that cannot be abstracted without losing meaning:
- Entity names and ID formats
- Type taxonomies and canonical schemas
- Stage-level actions specific to the domain (e.g., domain-signal identification
  during SOFTWARE normalization)
- Domain-specific sizing constraints (e.g., Context Envelope)
- Domain-specific anti-patterns (e.g., "packages are phases" in `software-decomp`)
- WRITE_SCOPE (varies by domain purpose)
- Downstream pipeline references (what agents consume the decomposition)

### References
- `docs/WORKFLOW_COMPONENT_STANDARD.md` — canonical workflow-component design standard
- `agents/AGENT_HELPS_HUMANS.md` — component-design manager
- `workflows/project-decomp/WORKFLOW.md` — EPC/design-build decomposition workflow
- `workflows/software-decomp/WORKFLOW.md` — software decomposition workflow
- `workflows/domain-decomp/WORKFLOW.md` — handbook/knowledge decomposition workflow

[[END:RATIONALE]]
