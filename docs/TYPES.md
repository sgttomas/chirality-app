# TYPES — Domain Vocabulary and Hierarchy

> **Status: RATIFIED — owner ratification 2026-07-11 (`CONTRACT.md` / K-AUTH-1).** Owner direction of record (2026-07-11, in-session, Ryan Tufts): "You can now take all the `docs/` out of the DRAFT state, making them authoritative." This document is accepted root governance in full. Provenance: it re-established the monorepo-root governance layer (root `docs/` was hollowed out during the four-repo merge; see `plans/monorepo_root_governance_and_path_anchoring_2026-06-15.md`), authored from the prior root canon (`.archive/TYPES.md`), preserving the established §1–§10 numbering (referenced as `TYPES §4` and `§9.2` from `AGENTS.md`), and adding the root/path-token vocabulary (§1.4–§1.5), the reconciled `WRITE_SCOPE` enum (§4.2), and the domain-decomposition entities (§8.2). **Ratification history:** the finding-severity taxonomy (§11) was ratified first per D-GOV-02 (`docs/governance_harness/_DECISIONS/D-GOV-02_verifier_severity_and_override.md`, ruled by owner 2026-07-01), and the §10.5 Status mapping and §10.6 review-severity registration were ruled per D-GOV-08 (2026-07-01); the 2026-07-11 full ratification subsumes those partial states while their rulings remain the records of the earlier basis.

This document is the authoritative vocabulary reference for the Chirality agent operating system. It defines the canonical entities, stable identifier formats, enumerated types, agent roles, and lifecycle states.

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

### 1.4 Roots and Working Surfaces

The path model is specified in `SPEC.md` §0.2. The entities it defines:

| Entity | Definition |
|---|---|
| **Repo Root** (`REPO_ROOT`) | The root of the active git checkout, resolved as `git rev-parse --show-toplevel`. Home of the shared instruction surface. In a git worktree it is the worktree's own root. |
| **Instruction Root** | The shared, release-managed agent operating system — `AGENTS.md`, `agents/`, `skills/`, `tools/`, root `docs/`, `init/`. `= REPO_ROOT` in this monorepo; the app bundle in desktop builds (see `DIRECTIVE.md` §2.6). |
| **Working Root** (`WORKING_ROOT`) | The active project or domain workspace — `projects/<name>/` or `domains/<name>/`, or a user-selected folder under the desktop harness. Where governed project truth lives. One instruction root serves many working roots. |
| **Execution Root** (`EXECUTION_ROOT`) | The execution-instance root within a working root; contains packages and tool roots. |
| **Tool Root** | A workspace-level directory for derived outputs under `{EXECUTION_ROOT}` (e.g. `_Decomposition/`, `_Evaluation/`, `_Reconciliation/`), isolated from source truth. The registry is `SPEC.md` §1.2. |

### 1.5 Path Tokens

Agent instructions and skills reference roots through `{*_ROOT}` tokens, each resolving against exactly one anchor. The authoritative registry — token → anchor → resolution — is `SPEC.md` §0.3. Key tokens: `{REPO_ROOT}`, `{INSTRUCTION_ROOT}`, `{WORKING_ROOT}`, `{EXECUTION_ROOT}`, `{COORDINATION_ROOT}`, `{DECOMP_ROOT}`, and the tool-root tokens (`{AGGREGATION_ROOT}`, `{EVALUATION_ROOT}`, `{RECONCILIATION_ROOT}`, `{ESTIMATES_ROOT}`, …). Instruction-surface tokens resolve `REPO_ROOT`-relative; workspace tokens resolve `WORKING_ROOT`-relative. Machine-absolute paths MUST NOT appear in instruction, coordination, or plan files (`SPEC.md` §0.2.4).

---

## 2. Stable Identifiers

Identifiers are assigned once and persist across renames, path changes, and restructuring. Path is a physical projection of the decomposition, not identity itself (`CONTRACT.md` K-ID-1).

| Entity | Format | Example | Assigned By |
|---|---|---|---|
| Package | `PKG-XX` | `PKG-01` | PROJECT_DECOMP |
| Deliverable | `DEL-XX-YY` | `DEL-01-01` | PROJECT_DECOMP |
| Dependency | `DEP-XX-YY-NNN` | `DEP-01-01-001` | TASK+dependency-extract |
| Scope Item | `SOW-NNN` | `SOW-003` | PROJECT_DECOMP |
| Objective | `OBJ-NNN` | `OBJ-001` | PROJECT_DECOMP |

Conforming decomposition variants define additional stable-ID families in their own contracts (e.g. domain-knowledge identifiers; see §8.2 and `docs/DECOMPOSITION_STANDARD.md`). The ID rules below apply to all families.

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
|---|---|---|
| **ANCHOR** | Connects a deliverable to a definition/traceability node (parent WBS, requirement) | Tree edge (vertical) |
| **EXECUTION** | Captures information flow, prerequisites, handoffs, and constraints between work items | DAG edge (horizontal) |

Together, ANCHOR (tree) and EXECUTION (DAG) form a **knowledge graph**: the tree preserves stable intent; the DAG captures execution couplings.

### 3.2 Anchor Types

| Value | Meaning |
|---|---|
| `IMPLEMENTS_NODE` | Parent definition node — exactly one per deliverable |
| `TRACES_TO_REQUIREMENT` | Requirement trace link — zero or more per deliverable |
| `NOT_APPLICABLE` | Used for EXECUTION rows only |

### 3.3 Direction

Direction is always relative to the host deliverable:

| Value | Meaning |
|---|---|
| `UPSTREAM` | This deliverable requires information FROM the target |
| `DOWNSTREAM` | This deliverable produces information FOR the target |

Legacy values `INBOUND` and `OUTBOUND` normalize to `UPSTREAM` and `DOWNSTREAM` respectively.

### 3.4 Dependency Types

| Value | Class | Meaning |
|---|---|---|
| `PREREQUISITE` | Execution | Required input or approval before work can proceed |
| `INTERFACE` | Execution | Explicit data/artifact exchange between deliverables |
| `HANDOVER` | Execution | Output of one deliverable consumed as input to another |
| `CONSTRAINT` | Execution | Explicit constraint or condition |
| `ENABLES` | Execution | This deliverable enables downstream work |
| `OTHER` | Both | Default for ANCHOR rows; catch-all for EXECUTION rows |

Legacy types such as `COORDINATION` / `INFORMATION`, and project-specific labels such as `ARCHITECTURE_BASIS`, `DOMAIN_MODEL`, `*_PREDECESSOR`, or `*_CONTRACT`, are read-only migration inputs. Current v3.1 registers MUST emit only the canonical values above and preserve the legacy label in provenance notes or documented extension fields.

### 3.5 Target Types

| Value | Meaning |
|---|---|
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
|---|---|---|
| `Explicitness` | `EXPLICIT`, `IMPLICIT` | Whether the dependency is directly stated in source text |
| `Confidence` | `HIGH`, `MEDIUM`, `LOW` | Strength of evidence supporting the dependency |
| `Origin` | `DECLARED`, `EXTRACTED` | Human-declared vs. agent-extracted |

### 3.7 Satisfaction and Status

| Dimension | Values | Tracks |
|---|---|---|
| `SatisfactionStatus` | `TBD`, `PENDING`, `IN_PROGRESS`, `SATISFIED`, `WAIVED`, `NOT_APPLICABLE` | Closure lifecycle (has the dependency been fulfilled?) |
| `Status` | `ACTIVE`, `RETIRED` | Extraction lifecycle (is the dependency currently observed in sources?) |

Candidate/non-gating graph dispositions are governance worklist states, not dependency `Status` values. They MUST NOT be represented as `Status=CANDIDATE` in current v3.1 registers.

---

## 4. Agent Roles

Agents are classified into three runtime positions following the 0-1-2 model.
See `AGENTS.md` for the live hierarchy and index.

### 4.1 Agent Types

| Type | Name | Role | Scope |
|---|---|---|---|
| **Type 0** | Supervising Architect | Aligns with the human, frames authority and decision points, supervises Agent 1 managers, and performs validated cross-manager fan-in | Human matter / workflow portfolio |
| **Type 1** | Manager | Converts human-approved intent into a governed workflow, makes manager-level decisions at human gates, delegates bounded work, and validates fan-in | Package, project, or specialist workflow scope |
| **Type 2** | Specialist | Executes a sealed bounded brief with declared context, tools, outputs, and write scope; returns outputs plus evidence and does not delegate | Single deliverable or narrow task |

The type number is a runtime delegation position, not a document-authority class. Normative standards live outside the hierarchy and constrain every layer. HELP_HUMAN is the sole canonical Agent 0. Agent 1 roles are directly invokable by a human and may also run under Agent 0.

Agent 2 has three valid construction forms: `TASK + skill + brief`; an ephemeral bounded generalist with no persistent `AGENT_*.md`; or an approved dedicated specialist instruction package. TASK is the default for recurring method work. A dedicated specialist requires evidence that TASK and ephemeral-generalist forms are inadequate, a HELPS_HUMANS proposal, and explicit human approval.

### 4.2 Classification Properties

| Property | Values | Meaning |
|---|---|---|
| `AGENT_CLASS` | `PERSONA`, `TASK` | Agent 0 and Agent 1 are interactive personas; persistent Agent 2 packages are straight-through specialists |
| `INTERACTION_SURFACE` | `chat`, `INIT-TASK`, `spawned`, `both` | Type 0/1 may use chat; Type 2 is delegated or pipeline-invoked and is not a top-level chat persona |
| `WRITE_SCOPE` | base values: `repo-wide`, `project-level`, `package-level`, `deliverable-local`, `tool-root-only`, `workspace-scaffold-only`, `repo-metadata-only`, `bounded-task-brief`, `none` | What the agent is allowed to write |
| `BLOCKING` | `never`, `allowed` | Whether the agent may pause for human input |

A `tool-root-only` scope MAY be parameterized to a registered tool root or subtree — for example `tool-root-only ({EXECUTION_ROOT}/_Evaluation/<subtree>/)`. `bounded-task-brief` is the `TASK` shell's scope: writes are authorized only by the effective bounded task brief and are always subject to ScopePath containment (`SPEC.md` §0.2.3, §9.5). The full enumeration and parameterization rules live in `SPEC.md` §9.5.

### 4.3 Authority Model

- Normative governance documents and domain standards constrain Agent 0, Agent 1, and Agent 2; they are not runtime agents.
- Agent 0 supervises only named Agent 1 managers.
- Agent 1 may delegate to named Agent 2 specialists, TASK, or an explicitly permitted ephemeral generalist.
- Agent 2 executes within its sealed brief and may not delegate.
- Human authority remains the halting condition at consequential gates.
  Consequential means at least: scope expansion, consequential-risk change,
  authority change, unresolved shared-write/ownership conflict, or acceptance
  criteria/lifecycle-acceptance change. Ambiguity returns to the human.

Authority and capability do not increase through delegation. Escalation flows upward. No agent may approve deliverables for external reliance on behalf of the accountable human.

### 4.4 Multi-Agent Orchestration

| Term | Meaning |
|---|---|
| `OrchestrationSelectionAuthority` | `HUMAN | AGENT_0 | AGENT_1` — who selected the current work graph |
| `OrchestrationPosture` | `TERMINAL_FAN_OUT_IN | SUPERVISED_MANY_TO_MANY | MIXED` — descriptive label for the graph |
| `CoordinationClaimStatus` | `PROVISIONAL | VALIDATED | ACCEPTED | DISPUTED` — relay disposition state, distinct from §10 epistemic labels and lifecycle status |
| `CoordinationDisposition` | `RECORD | RELAY | AMEND | HOLD | REPLAN | ESCALATE | ROUTE` — parent action on a child notice |
| `UpdateAcknowledgment` | `INCORPORATED | NO_EFFECT | BLOCKED | CONFLICT | HUMAN_DECISION_REQUIRED` — child response to a parent update |

The work graph records actual sequencing and concurrency; the posture is not a
complete execution language. Agent 0 owns cross-package graphs. A
WORKING_ITEMS Agent 1 instance owns exactly one activated package and its
intra-package graph.

Coordination claim-status authority is explicit:

- `PROVISIONAL`: an observation not yet validated; any managed child may report it.
- `VALIDATED`: a manager or deterministic check has validated the observation;
  the notice/update cites `validationRef`.
- `ACCEPTED`: a human accepted the proposition for the governed workflow; the
  notice/update cites `humanAcceptanceRef`. An agent may relay but never mint
  this state.
- `DISPUTED`: evidence conflicts or a recipient contests the proposition;
  conflict evidence remains attached and no silent resolution occurs.

An informational `RELAY` always cites its source `noticeId` and preserves the
source status. Claim status does not itself advance lifecycle state or satisfy
fan-in acceptance criteria.

---

## 5. Deliverable Lifecycle States

### 5.1 State Definitions

```
OPEN → INITIALIZED → SEMANTIC_READY → IN_PROGRESS → CHECKING → ISSUED
```

| State | Meaning |
|---|---|
| `OPEN` | Folder exists with minimum viable fileset; no content yet |
| `INITIALIZED` | The selected production contract exists and validates for its current format (`SOW_V1` or transitional `LEGACY_FOUR_DOC`) |
| `SEMANTIC_READY` | Semantic lens (`_SEMANTIC.md`) has been generated |
| `IN_PROGRESS` | Active human + agent work underway |
| `CHECKING` | Frozen candidate under review against a declared basis |
| `ISSUED` | Accepted baseline; released for use — subsequent changes only via the governed scope-change process |

### 5.2 Stage Gates vs. Lifecycle

**Lifecycle states** are tracked in `_STATUS.md` and represent the deliverable's production status: they are governed production and change-control regimes with maturity/readiness entry conditions, not percentage-complete scores (see `SPEC.md` §3.4 and `DELIVERABLE_CONCORDANCE_METHOD.md` §4).

**Stage gates** (30%, 60%, 90%, IFC, etc.) are human-managed milestones that represent project-level progress checkpoints. Stage gates are NOT lifecycle states and are tracked separately in coordination records.

### 5.3 Semantic Step

The `INITIALIZED → SEMANTIC_READY` transition is optional. If the semantic lensing step is skipped, deliverables may transition directly from `INITIALIZED → IN_PROGRESS`.

### 5.4 Change-Control Semantics

Each lifecycle state defines which changes are lawful and under what control. `IN_PROGRESS` permits ordinary authorized edits and holds whenever warranted open scope exists. Entry to `CHECKING` is layered: universal minimums (a warranted-empty `## Remaining` open-scope record, where adopted, bound to a current source-state evidence basis), a candidate-specific declared checking basis, and a human declaration that freezes the candidate. A `CHECKING` candidate is frozen — review evidence appends to run/review records, and reversal to `IN_PROGRESS` is the only exit from an unsuccessful or withdrawn check. Rebaselining is asymmetric: demotion to `IN_PROGRESS` requires only the absence of a current accepted basis for the asserted state, while promotion requires a contemporary declared basis. `ISSUED` is an accepted baseline; subsequent changes flow only through the governed scope-change process. The normative statement is `SPEC.md` §3.4.

---

## 6. Coordination Representations

The framework separates **how teams coordinate** (schedule-first, declared dependencies, or full graph) from **how the system tracks dependencies** (always maintains deliverable-local registers).

| Representation | Meaning |
|---|---|
| `SCHEDULE_FIRST` | Gantt drives sequencing; dependency tracking active for blocker detection and audit |
| `DEPENDENCY_TRACKED` | Dependency graph drives sequencing |
| `HYBRID` | Combination of schedule-first and dependency-tracked |

The coordination representation is recorded in `_COORDINATION.md` and chosen per project instance.

---

## 7. Deliverable Production Contract Types

Each PROJECT or SOFTWARE deliverable contains exactly one canonical production
contract. DOMAIN/KTY surfaces and analogous packet/case schemas retain their
own independent production grammars.

| Format | Files | Meaning |
|---|---|---|
| `SOW_V1` | One valid `ScopeOfWork.md` with schema `chirality-deliverable-sow/v1` | Canonical format for new and successfully converted PROJECT/SOFTWARE deliverables |
| `LEGACY_FOUR_DOC` | Complete `Datasheet.md`, `Specification.md`, `Guidance.md`, and `Procedure.md`; no `ScopeOfWork.md` | Transitional compatibility format for an existing unconverted deliverable |
| `MIGRATION_DUAL` | Both complete formats | Temporary conversion-workspace state only under an exact accepted migration authority; never an accepted deliverable baseline |
| `AMBIGUOUS` | Both complete formats without accepted migration authority | Invalid |
| `INVALID` | Partial legacy kit, invalid `ScopeOfWork.md`, or neither format at or beyond `INITIALIZED` | Invalid |

`ScopeOfWork.md` carries the stable deliverable target. `_STATUS.md ## Remaining`
records the warranted current delta against that target where the working root
adopts the remaining-work surface. Format migration does not change lifecycle
state, acceptance, or professional-reliance status.

An evidence-rich conversion candidate is a derivative migration artifact, not
an additional production-contract type. Deterministic finalization externalizes
its source markers, authority, and preparation bindings into reports and
produces the sole clean `SOW_V1` contract eligible for integration.

### 7.1 Scope-of-Work local identifier kinds

Local identifiers use exactly three decimal digits and are unique within one
`ScopeOfWork.md`. External references qualify them with the deliverable ID,
for example `DEL-07-03-AC-001`.

| Prefix | Meaning |
|---|---|
| `OUT` | Expected output |
| `CLM` | Descriptive claim |
| `REQ` | Normative requirement |
| `AC` | Acceptance criterion |
| `VER` | Verification method |
| `AX` | Governing value, rationale, or authority constraint |
| `TBD` | Unresolved information |
| `CON` | Unresolved conflict |
| `REM` | Remaining item in `_STATUS.md`; not defined in `ScopeOfWork.md` |

Migration dispositions are `PRESERVED`, `MERGED`, `SPLIT`, `SUPERSEDED`,
`DEFERRED`, and `CONFLICT`. They describe migration handling only and are not
epistemic labels, lifecycle states, or human rulings.

Blockquoted text in a finalized converted contract is preserved literal legacy
content. ID-shaped strings inside it do not define or reference SOW local IDs.

---

## 8. Decomposition Entities

### 8.1 Project Decomposition Entities

The project decomposition document (produced by PROJECT_DECOMP) defines these entities:

| Entity | ID Format | Purpose |
|---|---|---|
| **Scope Item** | `SOW-NNN` | Atomic, testable scope statement from the Structured Scope of Work |
| **Objective** | `OBJ-NNN` | Success criterion derived from scope; mapped to supporting deliverables |
| **Vocabulary Map** | (table) | Canonical terms and synonyms to prevent semantic drift |
| **Scope Ledger** | (table) | Machine-checkable mapping of every scope item to packages and deliverables |
| **Coverage & Telemetry** | (summary) | Metrics (counts, gaps, open issues) that make decomposition quality measurable |

### 8.2 Domain Decomposition Entities

The decomposition protocol is shared across variants by `docs/DECOMPOSITION_STANDARD.md`; `DOMAIN_DECOMP` binds its abstract entities to domain-knowledge names. The handbook/domain variant defines:

| Entity | ID Format | Purpose |
|---|---|---|
| **Category** | `CAT-###` | A flat partition of in-scope handbook units (no nesting, no overlaps, no gaps) |
| **Knowledge Type** | `KTY-CC-TT_{shortDesc}` | A reusable kind of knowledge object within a Category (Procedure, Checklist, Template, Guidance, Reference) |
| **Knowledge Subject** | `SUB-CC-TT-SS_{shortDesc}` | A specific domain topic within a Knowledge Type |
| **Handbook Unit (Atom)** | `HBA-<SOURCE_PREFIX>-NNNNN` | An atomic instruction/concept extracted from a source; the unit of coverage checking |
| **Section Node** | `SEC-<SOURCE_PREFIX>-NNNN` | A source section in the reviewed skeleton; the section-level retrieval substrate |

The standard's abstract entities (Atomic Unit, Partition, Production Unit, Decomposition Ledger, Coverage & Telemetry, Vocabulary Map) and seven-gate protocol are defined in `docs/DECOMPOSITION_STANDARD.md`; PROJECT_DECOMP, SOFTWARE_DECOMP, and DOMAIN_DECOMP bind them to domain-specific names and ID widths.

---

## 9. UI Navigation Vocabulary

The matrix and pipeline categories below are legacy-compatible desktop UI
routing vocabulary. They are not the Agent 0/1/2 runtime hierarchy, do not
classify document authority, and are not instantiated by root `AGENTS.md`.
Deployment-specific selector and API details are owned by runtime-project docs.

### 9.1 Matrix Axes

| Type | Values | Meaning |
|---|---|---|
| `MatrixRow` | `NORMATIVE`, `OPERATIVE`, `EVALUATIVE` | Epistemic-posture lane; also routes to WORKBENCH or PIPELINE |
| `MatrixColumn` | `GUIDING`, `APPLYING`, `JUDGING`, `REVIEWING` | Functional-role matrix column shared across all rows |

The matrix is a routing view only. Runtime delegation and authority follow the
Agent 0/1/2 hierarchy in `AGENTS.md`; standards constrain every layer.

### 9.2 Pipeline Selectors

| Type | Values | Meaning |
|---|---|---|
| `PipelineCategory` | `DECOMP*`, `PREP*`, `TASK*`, `AUDIT*` (and other live task families) | Top-level pipeline grouping; wildcard cells in the agent matrix expand to agent groups by this category |
| `TaskScopeMode` | `DELIVERABLES`, `KNOWLEDGE_TYPES` | Dynamic scope mode used when the category is `TASK*` |

### 9.3 Knowledge Decomposition Terms

| Term | Meaning |
|---|---|
| **Knowledge decomposition marker** | A decomposition-document signal (headings/phrases such as `Knowledge Categories`, `Knowledge Types`, or equivalent) that enables knowledge-type scope in TASK selectors. |
| **Knowledge type option** | A canonical file-type bucket (Datasheet, Specification, Guidance, Procedure, Dependencies, References, Context, Status, Semantic, Memory) selectable in TASK scope mode. |

---

## 10. Epistemic Ontology

The epistemology pillar (see `DIRECTIVE.md` §2) operates on a set of formally defined entities. These entities constitute the ontology of the epistemic layer — the things that the epistemic mechanisms (mandatory provenance, no invention, conflict surfacing, epistemic labeling) act upon.

### 10.1 Epistemic Primitives

| Primitive | Definition | Canonical Location |
|---|---|---|
| **Claim** | An assertion that something is the case. The atomic unit of the epistemology. Every non-trivial assertion produced by an agent in a governed workflow is a claim. | Dependency rows, document content, agent outputs |
| **Warrant** | The justification for believing a claim. Always extrinsic — a source citation (file + section + quote) — never intrinsic (model confidence or plausibility). | `EvidenceFile`, `SourceRef`, `EvidenceQuote` columns in `Dependencies.csv` (`SPEC.md` §6.5) |
| **Status** | The epistemic classification of a claim's certainty, expressed as one of four labels. | `Notes` fields, dependency records, agent output prose |
| **Gap** | The explicit, positive assertion that a warrant has not been found. A gap is not the absence of information — it is an entity representing that absence, making it visible and actionable. | `TBD` markers, `location TBD` in provenance fields, open issues |
| **Conflict** | Two or more claims with incompatible warrants about the same key. The existence of a conflict is itself an epistemic entity that must be resolved before the deliverable can advance. | Conflict Tables (`ConflictID`, `Key`, `Contenders`, `ProposedAuthority`, `HumanRuling`) |
| **Ruling** | A human decision that resolves a gap or conflict, transforming epistemic status. Rulings are binding and recorded in versioned files. | `HumanRuling` column in Conflict Tables, finding dispositions in REVIEW, gate decisions |

### 10.2 Epistemic Relationships

| Relationship | Description |
|---|---|
| A claim HAS a status | Exactly one of FACT, ASSUMPTION, PROPOSAL, or TBD |
| A claim MAY HAVE a warrant | Source file + section reference + optional quote; absence is structurally visible |
| A claim WITHOUT a warrant | Is a gap; status is TBD or uncited PROPOSAL; the absence of warrant is itself a finding |
| Two claims may be IN CONFLICT | Same key, incompatible values, different sources |
| A conflict REQUIRES a ruling | HumanRuling = TBD until the licensed professional adjudicates |
| A ruling TRANSFORMS status | Resolves gaps (TBD → FACT or ASSUMPTION), accepts or rejects proposals, and resolves conflicts (competing claims → one accepted) |

### 10.3 Epistemic Labels

The four epistemic labels classify the certainty status of claims:

| Label | Meaning | Reviewer Action |
|---|---|---|
| `FACT` | Directly observed in source text with citation | Verify citation; accept if source is authoritative |
| `ASSUMPTION` | Reasonable inference grounded in cited material; not directly stated and still requiring validation | Validate or reject; document decision |
| `PROPOSAL` | Suggested interpretation, action, or design move; may cite supporting context, but requires human decision to become binding | Decide; record rationale |
| `TBD` | Unknown; placeholder requiring resolution | Resolve before reliance |

### 10.4 Warrant Lifecycle

Claims within a deliverable progress through a warrant lifecycle that tracks their epistemic state, interleaved with the deliverable lifecycle (`§5`) that tracks production state:

```
UNWARRANTED → CITED → REVIEWED → AUTHENTICATED
```

| Warrant State | Meaning | Transition Mechanism |
|---|---|---|
| `UNWARRANTED` | Claim exists but has no source citation; status is TBD or uncited PROPOSAL | Agent produces claim; K-INVENT-1 requires TBD marking for gaps |
| `CITED` | Claim has a source citation; status is FACT, ASSUMPTION, or cited PROPOSAL | Agent attaches provenance; K-PROV-1 enforces |
| `REVIEWED` | Claim has been examined by a licensed professional; findings dispositioned | REVIEW gates; human rules on findings |
| `AUTHENTICATED` | Claim is part of an authenticated PWP; the professional warrants it under duty of care | Authentication binds to git SHA; K-AUTH-2 enforces |

The deliverable lifecycle asks: *what state is this work product in?* The warrant lifecycle asks: *what state is our knowledge about this work product in?* A deliverable is ready for issuance when its warrants are sufficient — when the licensed professional has determined that the epistemic state of the claims supports authentication under professional responsibility.

The two lifecycles are correlated but not identical. A deliverable in `IN_PROGRESS` contains a mixture of warranted and unwarranted claims. The transition to `CHECKING` requires layered entry conditions (`SPEC.md` §3.4): the universal entry minimums — that critical claims have been warranted (all CRITICAL findings must have non-TBD human disposition; see §10.6) and that the deliverable's `## Remaining` open-scope record, where adopted, is warranted-empty against a current source-state evidence basis — together with a candidate-specific declared checking basis and the human declaration that freezes the candidate. The transition to `ISSUED` requires that the professional has authenticated the work — the act of warranting the deliverable's claims under professional responsibility; post-issuance changes flow only through the governed scope-change process.

### 10.5 Enforcing Invariants

| Invariant | Epistemic Primitive Governed |
|---|---|
| K-PROV-1 (mandatory provenance) | Warrant — every claim must have an extrinsic warrant or explicit `location TBD` |
| Audit-time assessment (`AGENT_AUDIT_EPISTEMIC`; future harness `evidence-check`), bounded by K-CLAIM-1 | Status — the labeling act is assessed at audit time, not producer-emitted; per D-GOV-08 (ruled 2026-07-01) |
| K-INVENT-1 (no invention) | Gap — missing data must be represented as a gap (TBD), not filled with a fabrication |
| K-CONFLICT-1 (conflict surfacing) | Conflict — disagreements must be exposed as conflicts, not silently resolved |
| K-AUTH-1 (human authority) | Ruling — only humans may author binding rulings and approval records |
| K-AUTH-2 (SHA-bound approval) | Authentication — the warrant-to-content binding is mechanically verifiable |

### 10.6 Review Finding Severity

Registered per D-GOV-08 (`docs/governance_harness/_DECISIONS/D-GOV-08_epistemic_vocabulary_operationalization.md`), ruled by the owner 2026-07-01.

Review-gate findings are classified with the four-level enum defined by the review type system in `docs/SE_Design_Analysis.md` §7.3 (`FindingSeverity`):

```
CRITICAL | MAJOR | MINOR | OBSERVATION
```

This is the finding vocabulary that the "CRITICAL findings" gate conditions in §10.4 reference.

Distinctness:

- This enum is distinct from the governance-verifier taxonomy (`BLOCK`, `REVIEW`, `WARN`, `INFO`, `NOT_APPLICABLE`; §11): review severities classify review-gate findings about deliverable content; verifier severities classify governance harness findings.
- It is also distinct from the agent-conformance rubric's Blocker/High/Medium/Low (`docs/rubrics/AUDIT_AGENT.md`): that rubric grades agent-file conformance, not deliverable review findings.

---

## 11. Finding Severity (Governance Verifier Taxonomy)

Ratified per D-GOV-02 (`docs/governance_harness/_DECISIONS/D-GOV-02_verifier_severity_and_override.md`), ruled by the owner 2026-07-01. This section is accepted governance; the DRAFT status in the banner above applies to the remainder of the document.

Governance harness verifiers classify their findings using five severities, each carrying defined machine behavior and override authority.

### 11.1 Severity Levels

| Severity | Meaning | Machine behavior | Override |
|---|---|---|---|
| `BLOCK` | Objective violation **within the tool's declared observation boundary** | exit nonzero | Human only, recorded |
| `REVIEW` | Material issue requiring human judgment | exit 0 (nonzero in `--strict`) | Human disposition |
| `WARN` | Non-blocking inconsistency or hygiene issue | exit 0 | None needed |
| `INFO` | Contextual fact | exit 0 | n/a |
| `NOT_APPLICABLE` | Check skipped; preconditions absent | exit 0 + reason | n/a |

### 11.2 Exit-Code Convention

Harness verifiers adopt exit `0/1/2`, aligned with the newest validator class (e.g. `tools/validation/validate_domain_engine_profile.py`). This sets the convention going forward rather than inheriting a uniform existing one.

### 11.3 Caveats

- `BLOCK` means *mechanically blocked within the declared observation boundary*, never *globally proven safe/unsafe*.
- `Ruling SHA: TBD` is conditional: REVIEW when the artifact self-declares bind-at-publish (the lawful tier-0 flow); BLOCK only when the claim is being relied on as bound authority.
- No non-overridable BLOCK may attach to the CHECKING → ISSUED judgment itself (a K-GATE-1 derivation); BLOCKs apply to objective preconditions and hygiene only.

### 11.4 Distinctness

- This taxonomy is distinct from the epistemic labels (`FACT`, `ASSUMPTION`, `PROPOSAL`, `TBD`; §10.3): epistemic labels classify the certainty of a claim; finding severities classify verifier findings.
- Severity `NOT_APPLICABLE` is distinct from the dependency-vocabulary enum value `NOT_APPLICABLE` (§3.2, §3.7): same token, different vocabulary.

---

## 12. Shared Runtime Vocabulary

| Type | Meaning |
|---|---|
| `ChiralityProjectManifest` | Tracked `chirality.project/v1` declaration containing stable identity and relative authority/profile references, never secrets or machine-specific absolute paths. |
| `RegisteredProject` | User-data record binding a manifest hash to a canonical local root, approval reference, adapter allowlist, and scoped client authorization. |
| `RuntimeClientCredential` | Random per-client bearer secret stored outside the checkout; the daemon stores only its hash, scopes, project binding, and lifecycle metadata. |
| `RuntimeDaemonStatus` | Health and ownership state for the one per-user daemon and Unix-domain control socket. |
| `ResidencyState` | `NO_MODEL`, `READY`, `DRAINING`, `UNLOADING`, or `LOADING`; transitions are serialized and fail closed. |
| `ResidencyEpoch` | Monotonic attribution record for one verified primary local-model residency interval. |
| `ModelStatusRecord` | Exact oMLX model identity plus loaded/loading, type, helper, pin, size, and capability metadata returned by authenticated status discovery. |
| `Agent1RunRequest` | Direct human/external invocation of one Agent 1 with a sealed brief and optional requirement for one exact resident local Agent 2 child. |
| `AgentRunEvidence` | Checkout-contained record of parentage, sealed brief, role, adapter/provider/actual model, residency epoch, permissions, evidence, status, and acceptance result. |
| `RuntimeBackend` | Provider-neutral daemon composition port for session, turn, interruption, permission, delegation, credential, and residency operations. |

These types do not prescribe model capability tiers or durable model-to-role
assignments. Runtime attribution records what actually executed.
