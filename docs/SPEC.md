# SPEC — Physical Structures and Mechanics

> **Status: RATIFIED — owner ratification 2026-07-11 (`CONTRACT.md` / K-AUTH-1).** Owner direction of record (2026-07-11, in-session, Ryan Tufts): "You can now take all the `docs/` out of the DRAFT state, making them authoritative." This document is accepted root governance in full. Provenance: it re-established the monorepo-root governance layer (root `docs/` was hollowed out during the four-repo merge; see `plans/monorepo_root_governance_and_path_anchoring_2026-06-15.md`), authored from the prior root canon (`.archive/SPEC.md`), preserving the established §1–§13 numbering and schemas, and adding the **Root Model and Path Anchoring** convention (§0.2–§0.3) plus reconciliations to the live agent surface. **Ratification history:** per D-GOV-05 (`docs/governance_harness/_DECISIONS/D-GOV-05_minimal_governance_basis.md`, ruled by owner 2026-07-01), K-WRITE-2 path containment (§0.2.3) was ratified first as part of the minimal harness basis; the 2026-07-11 full ratification subsumes that partial basis.

This document is the authoritative specification for the physical structures, file formats, schemas, and layout conventions used in the Chirality filesystem-as-state agent operating system.

All agents, tools, and governance documents reference this specification. Where an agent instruction file defines a format inline, this document is the canonical version; agent instructions MUST conform.

**Normative keywords:** MUST, MUST NOT, SHOULD, SHOULD NOT, MAY follow the conventions defined in `WORKFLOW_COMPONENT_STANDARD.md`.

---

## 0.1 Fractal Property: SPEC Sections Map to DIRECTIVE Pillars

This specification embodies the four-pillar philosophy defined in `DIRECTIVE.md` §2. The sections of this document instantiate those pillars:

| DIRECTIVE Pillar | SPEC Sections | What the Section Governs |
|---|---|---|
| **Ontology** — what exists? | §1–2, §10, §12 | Execution root layout, deliverable structure, filesystem-safe naming, structure validation |
| **Epistemology** — what can be known? | §5–6 | Dependency tracking, provenance requirements, evidence schema |
| **Praxiology** — how do we execute? | §0.2–0.3, §3–4, §9, §11 | Root model and path anchoring, lifecycle state machine, context and authority, agent instruction structure, snapshots |
| **Axiology** — what do we value? | §7–8, §13 | Reference and memory management, coordination representation, and the values embedded in schema structure |

This alignment ensures that project execution state (the filesystem) reflects the same philosophical commitments as the governance framework itself.

---

## 0.2 Root Model and Path Anchoring

> Numbering note: this section is placed in the §0 preamble (rather than as a new §1) so the established §1–§13 numbers — and every cross-reference to them, e.g. `SPEC §1.2` (tool roots) and `SPEC §6.5` (provenance) — remain stable.

Chirality runs in two deployment shapes that share one path model: the **canonical monorepo** (this repository) and the **desktop harness** (an app bundle pointed at a user-selected folder). The path model defines two roots and one containment rule.

### 0.2.1 `REPO_ROOT` — the active checkout

`REPO_ROOT` is the root of the active git checkout, resolved as:

```sh
REPO_ROOT="$(git rev-parse --show-toplevel)"
```

`REPO_ROOT` MUST be resolved at session start and never hard-coded. In a linked **git worktree**, `git rev-parse --show-toplevel` returns *that worktree's* root — so a worktree is a fully isolated checkout, and every path derived from `REPO_ROOT` re-anchors to it automatically. This is the mechanism that makes worktree-based isolation safe.

`REPO_ROOT` is the home of the **shared instruction surface** (`AGENTS.md`, `agents/`, `skills/`, `tools/`, root `docs/`, `init/`) — the release-managed agent operating system (the **instruction root**; see `DIRECTIVE.md` §2.6). The instruction surface is read-mostly: changing it is a repo-wide governance action, not ordinary working-root execution.

### 0.2.2 `WORKING_ROOT` — the active workspace

`WORKING_ROOT` is the project or domain workspace an agent is scoped to — `projects/<name>/` or `domains/<name>/` in this monorepo, or the user-selected folder under the desktop harness. It is where governed project truth lives (`{EXECUTION_ROOT}`, tool roots, deliverables, decomposition state).

- `WORKING_ROOT` MUST resolve to an absolute path under `REPO_ROOT` (monorepo) or to the user-selected root (desktop harness).
- One `REPO_ROOT` instruction surface serves **many** working roots without per-workspace instruction drift.
- A working root MUST NOT be the shared instruction surface itself; agents operating in a working root MUST NOT write to `agents/`, `skills/`, `tools/`, or root `docs/` except through an explicit, separately-authorized repo-wide instruction change.

### 0.2.3 ScopePath containment (binding)

Every `ScopePath` and every `AllowedWriteTarget` (see `AGENT_TASK.md`) MUST:

1. normalize to an absolute path, and
2. resolve **under `REPO_ROOT`** (the active checkout returned by `git rev-parse --show-toplevel`).

A `ScopePath` or write target that resolves outside the active checkout — including via symlink or `..` traversal — MUST be rejected (`SCOPE_OUTSIDE_WORKTREE`); the task stops rather than writing. This upgrades the existing `AGENT_TASK.md` rule ("`ScopePath` must resolve to an existing local path") to "…and must resolve within the active checkout," and is the deterministic backstop that prevents an agent launched in a worktree from writing back to the main checkout. It is a no-op in single-checkout (shared-monorepo) mode. This rule is bound as `CONTRACT.md` invariant **K-WRITE-2**.

### 0.2.4 Path reference discipline

- **Instruction-surface references** (to `agents/`, `skills/`, `tools/`, root `docs/`, `AGENTS.md`) resolve **`REPO_ROOT`-relative**.
- **Working-root references** (to `{EXECUTION_ROOT}`, tool roots, deliverables, `_Coordination/`, decomposition state) resolve **`WORKING_ROOT`-relative**.
- Instruction, coordination, and plan files MUST NOT embed machine-absolute paths (e.g. `/Users/<name>/...`). Absolute paths are permitted only in run records and evidence artifacts, where they record what actually happened and are never re-executed.

---

## 0.3 Path Token Registry

Agent instructions and skills reference roots through `{*_ROOT}` tokens. Each token resolves against exactly one anchor. Projects and domains MAY bind additional workspace-local tokens, but every such token MUST resolve under `WORKING_ROOT`.

| Token | Anchor | Resolves to |
|---|---|---|
| `{REPO_ROOT}` | self | `git rev-parse --show-toplevel` (the active checkout) |
| `{INSTRUCTION_ROOT}` | `REPO_ROOT`-relative | the shared instruction surface; `= REPO_ROOT` in the monorepo, the app bundle in desktop builds |
| `{WORKING_ROOT}` | `REPO_ROOT`-relative | the active `projects/<name>/` or `domains/<name>/` (or user-selected folder) |
| `{EXECUTION_ROOT}` | `WORKING_ROOT`-relative | the execution instance root (project-defined; often `WORKING_ROOT` or `WORKING_ROOT/execution`) |
| `{COORDINATION_ROOT}` | `EXECUTION_ROOT`-relative | `{EXECUTION_ROOT}/_Coordination/` |
| `{DECOMP_ROOT}` / `{DECOMPOSITION_ROOT}` | `EXECUTION_ROOT`-relative | `{EXECUTION_ROOT}/_Decomposition/` (or a domain pack's `_Decomposition/`) |
| `{AGGREGATION_ROOT}` | tool-root-relative | `{EXECUTION_ROOT}/_Aggregation/` |
| `{EVALUATION_ROOT}` | tool-root-relative | `{EXECUTION_ROOT}/_Evaluation/` |
| `{RECONCILIATION_ROOT}` | tool-root-relative | `{EXECUTION_ROOT}/_Reconciliation/` |
| `{ESTIMATES_ROOT}` | tool-root-relative | `{EXECUTION_ROOT}/_Estimates/` |
| `{SOURCE_AUDIT_ROOT}`, `{ASSETS_ROOT}`, `{PUBLICATION_ROOT}`, `{RESEARCH_ROOT}`, `{PLANNING_ROOT}`, `{RUN_ROOT}`, `{CONTEXT_ROOT}` | `WORKING_ROOT`-relative | domain/workspace-local roots bound by the owning agent/skill; MUST resolve under `WORKING_ROOT` |
| `{SKILL_ROOT}` | `REPO_ROOT`-relative | `{REPO_ROOT}/skills/<name>/` |
| `{TOOL_ROOT}` | context-dependent | `{REPO_ROOT}/tools/` when referring to the deterministic tool layer; a project tool root (`{EXECUTION_ROOT}/_<Name>/`) when referring to a derived-output root (see §1.2) |

The token vocabulary above is the registry; an agent that introduces a new `{*_ROOT}` token MUST declare its anchor in the agent's own instruction file and keep it consistent with this table.

---

## 1. Execution Root Layout

An execution instance is a self-contained project workspace rooted at `{EXECUTION_ROOT}/` (which resolves `WORKING_ROOT`-relative; see §0.2–0.3). The execution root contains packages (work partitions) and tool roots (derived/operational outputs).

```
{EXECUTION_ROOT}/
├── INIT.md                          # Session initialization parameters
├── PKG-XX_{PkgLabel}/               # One or more packages
│   ├── 0_References/                # Package-level reference materials
│   │   └── _Archive/
│   ├── 1_Working/                   # Active deliverable folders
│   │   ├── DEL-XX-YY_{DelLabel}/    # One or more deliverables
│   │   └── _Archive/
│   ├── 2_Checking/                  # Review staging
│   │   ├── From/
│   │   └── To/
│   └── 3_Issued/                    # Released deliverables
│       └── _Archive/
├── _Aggregation/                    # Aggregation snapshots
│   ├── _Archive/
│   └── _Templates/
├── _Change/                         # Change management records
├── _Coordination/                   # Coordination representation
│   └── _COORDINATION.md
├── _Decomposition/                  # Project/domain decomposition document(s)
│   └── _Archive/
├── _Estimates/                      # Cost estimate snapshots
├── _Evaluation/                     # Current audits, evaluations, and review snapshots
├── _Reconciliation/                 # Deliverable-corpus concordance; historical audit snapshots are immutable
├── _Archive/                        # Baseline snapshots with checksums
├── _Scripts/                        # Deployment and analysis scripts
└── _Sources/                        # Shared source/reference documents
```

### 1.1 Package Folders

**Naming:** `{PKG-ID}_{PkgLabel}/` where `PKG-ID` follows the `PKG-XX` format and `PkgLabel` is a filesystem-safe version of the package name (see Section 10).

**Required subfolders:**

| Subfolder | Purpose |
|---|---|
| `0_References/` | Package-level reference materials |
| `0_References/_Archive/` | Archived references |
| `1_Working/` | Active deliverable folders |
| `1_Working/_Archive/` | Archived working drafts |
| `2_Checking/` | Review staging area |
| `2_Checking/From/` | Incoming review items |
| `2_Checking/To/` | Outgoing review items |
| `3_Issued/` | Released deliverables |
| `3_Issued/_Archive/` | Archived issued versions |

### 1.2 Tool Roots

Tool roots are workspace-level directories for derived outputs, resolved `{EXECUTION_ROOT}`-relative. Each tool root is isolated from source truth (deliverable folders). A tool-root path is the canonical write destination for `tool-root-only` agents (see §9.5); `AUDIT_GOVERNANCE` validates that every agent's `WRITE_SCOPE` references a registered tool root and that every tool root has at least one writer.

| Tool Root | Purpose | Typical Writer |
|---|---|---|
| `_Aggregation/` | Aggregation snapshots and templates | AGGREGATION |
| `_Change/` | Change management records | CHANGE |
| `_Coordination/` | Coordination representation | PROJECT_SETUP |
| `_Decomposition/` | Project/domain decomposition document(s) and companions | PROJECT_DECOMP / SOFTWARE_DECOMP / DOMAIN_DECOMP |
| `_Estimates/` | Cost estimate snapshots | TASK + estimate skills |
| `_Evaluation/` | Current evaluation reports plus structural, dependency, epistemic, governance, agent, coherence, and review snapshots | EVALUATION / EVALUATION_* / REVIEW / AUDIT_* |
| `_Reconciliation/` | Calibrated deliverable-corpus concordance runs and historical immutable generic-audit artifacts | RECONCILIATION |
| `_Schedule/` | Schedule snapshots generated from the dependency graph | PROJECT_SETUP scheduling workflow |
| `_ScopeChange/` | Change-impact assessments and decomposition amendment snapshots | SCOPE_CHANGE |
| `_Sources/` | Shared source/reference documents | Human / source-extraction pipelines |
| `_LocalIndexes/` | Derived source-catalog and retrieval snapshots (domain packs) | DOMAIN_DECOMP / retrieval tools |
| `_Archive/` | Baseline snapshots with checksums | Human / CHANGE |
| `_Scripts/` | Deployment and analysis scripts | Human / tooling |

**Nested audit/snapshot subtrees are legal.** A registered tool root MAY contain
named subtrees that are themselves snapshot roots — e.g.
`_Evaluation/AgentAudit/`, `_Evaluation/DepClosure/`,
`_Evaluation/ScopeClosureAudit/`, `_Evaluation/HypergraphClosure/`,
`_Evaluation/EpistemicAudit/`, `_Evaluation/GovernanceAudit/`,
`_Evaluation/DecompCoverage/`, `_Evaluation/Reviews/`, and
`_Aggregation/Hypergraph/`. An agent whose `WRITE_SCOPE` is parameterized to
such a subtree satisfies the registry through its parent tool root. Legacy
generic-audit subtrees under `_Reconciliation/` remain readable immutable
evidence but are not current write destinations.

---

## 2. Deliverable Folder Layout

Each deliverable occupies a folder at:

```
{EXECUTION_ROOT}/{PKG-ID}_{PkgLabel}/1_Working/{DEL-ID}_{DelLabel}/
```

### 2.1 File Inventory

| File | Presence | Created By | Purpose |
|---|---|---|---|
| `_STATUS.md` | MUST | PREPARATION | Lifecycle state and history |
| `_CONTEXT.md` | MUST | PREPARATION | Identity, decomposition pointer, traceability |
| `_DEPENDENCIES.md` | MUST | PREPARATION | Dependency summary (human declarations + agent extractions) |
| `_REFERENCES.md` | MUST | PREPARATION | Source document pointers |
| `ScopeOfWork.md` | MUST* | TASK+scope-of-work | Canonical PROJECT/SOFTWARE production contract selected by schema marker |
| `Datasheet.md` | MAY* | TASK+four-documents (legacy compatibility) | Legacy key parameters and structured metadata |
| `Specification.md` | MAY* | TASK+four-documents (legacy compatibility) | Legacy technical requirements and scope definition |
| `Guidance.md` | MAY* | TASK+four-documents (legacy compatibility) | Legacy design guidance, rationale, and best practices |
| `Procedure.md` | MAY* | TASK+four-documents (legacy compatibility) | Legacy step-by-step execution workflow |
| `Dependencies.csv` | SHOULD | TASK+dependency-extract | Structured dependency register (v3.1 schema) |
| `_MEMORY.md` | SHOULD | PREPARATION | Working memory (shared by WORKING_ITEMS and deliverable-local task agents) |
| `_SEMANTIC.md` | MAY | TASK+semantic-matrix-build | Semantic lens with derivation work |
| `_SEMANTIC_LENSING.md` | MAY | TASK+lens-register | Semantic analysis narrative |
| `MEMORY.md` | MAY | PREPARATION | Compatibility pointer to `_MEMORY.md` |

**Minimum viable fileset (PREPARATION):** `_STATUS.md`, `_CONTEXT.md`, `_DEPENDENCIES.md`, `_REFERENCES.md`, `_SEMANTIC.md` (placeholder).

**Production contract:** At lifecycle state `INITIALIZED` or later, exactly one
valid production format is required. `SOW_V1` is one valid `ScopeOfWork.md`.
`LEGACY_FOUR_DOC` is the complete four-file kit retained only for an existing
unconverted deliverable during the authorized transition. The `MUST*` and
`MAY*` marks above are resolved by this exclusive format rule, not as five
simultaneous file requirements.

### 2.2 Production Format Resolution

| Files present | State | Validity |
|---|---|---|
| Valid `ScopeOfWork.md` only | `SOW_V1` | Canonical |
| Complete four-document kit only | `LEGACY_FOUR_DOC` | Transitional compatibility for an existing unconverted deliverable |
| Both complete formats | `MIGRATION_DUAL` only in an isolated conversion workspace with exact accepted migration authority; otherwise `AMBIGUOUS` | Never an accepted deliverable baseline |
| Partial legacy kit, invalid `ScopeOfWork.md`, or neither at or beyond `INITIALIZED` | `INVALID` | Invalid |

New PROJECT/SOFTWARE deliverables use `SOW_V1`. A successful legacy conversion
is prepared and verified in isolation, then integrated as one atomic
replacement that adds the clean finalized `ScopeOfWork.md` and removes all
four legacy production files. The evidence-rich migration candidate is kept
outside production; Git history and external migration/finalization receipts
preserve its source basis and bind the final production hash. No accepted
commit contains two competing canonical formats or migration-only metadata in
the production contract.

Format migration is lifecycle-neutral and leaves `_STATUS.md` byte-identical.
An `ISSUED` deliverable additionally requires an explicit human-approved
administrative representation-replacement record bound to its accepted basis
and source hashes. Any semantic change fails format migration and proceeds only
through the governed scope-change process.

---

## 3. `_STATUS.md` — Lifecycle State

### 3.1 Format

```markdown
# Status: {DEL-ID} {DeliverableName}

**Current State:** {STATE}
**Last Updated:** {YYYY-MM-DD}

## History
- {YYYY-MM-DD} — State set to {STATE} ({AGENT_OR_ACTOR})
```

A working root MAY host a `## Remaining` section in `_STATUS.md` as the deliverable-local record of warranted open scope. Where adopted, it is the sole deliverable-local executable work surface, and the CHECKING entry minimums in §3.4 reference it.

### 3.2 Valid Lifecycle States

```
OPEN → INITIALIZED → SEMANTIC_READY → IN_PROGRESS → CHECKING → ISSUED
```

| State | Meaning | Typical Trigger |
|---|---|---|
| `OPEN` | Folder exists, no content yet | PREPARATION creates folder |
| `INITIALIZED` | Selected production contract exists and validates | TASK+scope-of-work completes `SOW_V1`; retained legacy deliverables preserve their existing state |
| `SEMANTIC_READY` | Semantic lens generated | TASK+semantic-matrix-build writes `_SEMANTIC.md` |
| `IN_PROGRESS` | Active human + agent work | Human or WORKING_ITEMS begins work |
| `CHECKING` | Frozen candidate under review against a declared basis | Human declares the checking basis and freezes the candidate (entry conditions: §3.4) |
| `ISSUED` | Accepted baseline | Human approves and issues; subsequent changes only via the governed scope-change process (§3.4) |

The `SEMANTIC_READY` state is optional in the lifecycle; a working root MAY omit it where no semantic step applies.

### 3.3 Transition Rules

| Transition | Authorized Actor |
|---|---|
| `→ OPEN` | PREPARATION |
| `OPEN → INITIALIZED` | TASK+scope-of-work after `SOW_V1` validation |
| `INITIALIZED → SEMANTIC_READY` | TASK+semantic-matrix-build |
| `INITIALIZED → IN_PROGRESS` | Human, WORKING_ITEMS (when semantic step is skipped) |
| `SEMANTIC_READY → IN_PROGRESS` | Human, WORKING_ITEMS |
| `IN_PROGRESS → CHECKING` | Human |
| `CHECKING → ISSUED` | Human |
| `CHECKING → IN_PROGRESS` | Human (reversal — the sole exit from an unsuccessful or withdrawn check) |
| `ISSUED → IN_PROGRESS` | Human, via the governed scope-change process only (opens a new revision cycle) |

**Invariant:** `_STATUS.md` is the authoritative lifecycle indicator. No other file determines deliverable state (`CONTRACT.md` K-STATUS-1).

**Stage gates** (30/60/90/IFC, etc.) are human-managed milestones and are NOT lifecycle states. They are tracked separately in coordination records.

### 3.4 Lifecycle Regimes and CHECKING Entry Conditions

Lifecycle states are governed production and change-control regimes with maturity/readiness entry conditions; they are not percentage-complete scores. Advancing `IN_PROGRESS` → `CHECKING` → `ISSUED` carries maturity meaning — each transition asserts readiness against declared entry conditions — while the states themselves define which changes are lawful and under what control:

- `IN_PROGRESS` permits ordinary authorized edits. It is the honest holding state whenever warranted open scope exists, however advanced the implementation.
- `CHECKING` is a frozen candidate under review against a declared basis. Review evidence appends to run/review records, never to the frozen claim surfaces; reversal to `IN_PROGRESS` is the only edit path.
- `ISSUED` is an accepted baseline; changes flow only through the governed scope-change process.

**Entry to `CHECKING` is layered**, not a single trigger:

1. **Universal minimums (candidacy).** The deliverable's `## Remaining` open-scope record (where the working root adopts one in `_STATUS.md`; §3.1) is **warranted-empty** — empty, with a current evidence basis bound to the candidate source state certifying that the emptiness is warranted.
2. **Candidate-specific checking basis.** A declared checking basis appropriate to the deliverable's claims and risk. These criteria are emergent; maturity feedback from real checks hardens into reusable ruled profiles.
3. **Human declaration.** A human declares the checking basis and freezes the candidate; entry is a human act.

There are no disclosed-deferral carve-outs: any warranted Remaining item keeps the deliverable `IN_PROGRESS`. Boundary adjustments are rescoped through the project's decision process before freeze, never carved out during review. A failed check exits by reversal, its findings becoming Remaining items.

**Rebaseline asymmetry:** demotion to `IN_PROGRESS` requires no criteria beyond the absence of a current accepted basis for the asserted state; promotion requires a contemporary declared basis. Lifecycle corrections are human-authorized administrative acts.

These entry conditions are gate preconditions, not state determinants: `_STATUS.md` remains the sole lifecycle authority (`CONTRACT.md` K-STATUS-1), and every transition — reversals included — is recorded there. Nothing in this section creates a machine-enforced BLOCK on the `CHECKING → ISSUED` judgment (K-GATE-1 / D-GOV-02 posture unchanged).

Reference formulation: `docs/DELIVERABLE_CONCORDANCE_METHOD.md` §4 (ratified 2026-07-11). Amendment authorized by owner direction 2026-07-11: "attend to both now and resolve the issues you find as you recommended in the sequence 1, 2, 3, 4 just stated.  I give you approval to edit the SPEC/TYPES and just report back what you did."

Distinctness: the `IN_PROGRESS` token also appears as a `SatisfactionStatus` enum value (§6.3) — an unrelated vocabulary.

---

## 4. `_CONTEXT.md` — Identity and Traceability

### 4.1 Format

```markdown
# Context: {DEL-ID}

**Name:** {DeliverableName}
**Package:** {PKG-ID} {PackageName}
**Discipline:** {Discipline}
**Type:** {ArtifactType}
**Responsible:** {Role}

## Description
{Exact description from decomposition document}

## Acceptance Criteria
{Pass/fail conditions from decomposition}

## Anticipated Artifacts
- {List from decomposition; may be empty}

## Scope Traceability
- Scope items: {SOW-IDs}
- Objectives: {OBJ-IDs}

## Decomposition Reference
- **Decomposition file:** {path to decomposition document}
- **Deliverable ID:** {DEL-ID}
```

### 4.2 Rules

- Header fields MUST match the decomposition document exactly.
- `Decomposition Reference` MUST point to the specific decomposition document used.
- `_CONTEXT.md` is created by PREPARATION and MUST NOT be modified by other agents (human edits permitted).

---

## 5. `_DEPENDENCIES.md` — Dependency Summary

### 5.1 Format

`_DEPENDENCIES.md` is a hybrid container with two ownership zones:

**Human-owned sections** (PREPARATION creates; human/PROJECT_SETUP maintains):
- Dependency Tracking Mode
- Declared Upstream
- Declared Downstream

**Agent-owned sections** (TASK+dependency-extract populates):
- Extracted Dependency Register
- Run Notes & History
- Lifecycle Summary
- Consumer Handoff Notes

### 5.2 Schema

```markdown
# Dependencies: {DEL-ID} {DeliverableName}

## Dependency Tracking Mode
- **Mode:** {NOT_TRACKED | DECLARED | TRACKED}
- **Register:** Dependencies.csv (schema v3.1)

---

## Declared Upstream (I need these before I can proceed)
{Human-owned declarations, or "Dependencies coordinated externally by humans."}

## Declared Downstream (These need me)
{Human-owned declarations, or "Dependencies coordinated externally by humans."}

---

## Extracted Dependency Register
**Run date:** {YYYY-MM-DD}
**Schema version:** v3.1
**Total ACTIVE rows:** {N}
**ANCHOR rows (ACTIVE):** {N} ({parent count} parent + {trace count} trace)
**EXECUTION rows (ACTIVE):** {N}
**RETIRED rows:** {N}

### ANCHOR Rows
{Summary table}

### EXECUTION Rows (summary)
{Summary table}

---

## Lifecycle Summary
{Dimension / Count table}

---

## Run Notes
{Defaults, assumptions, paths used, warnings}

## Run History
{Append-only log: one entry per run}
```

### 5.3 Tracking Modes

| Mode | Meaning |
|---|---|
| `NOT_TRACKED` | Dependencies coordinated externally by humans |
| `DECLARED` | Human-declared upstream/downstream only; no agent extraction |
| `TRACKED` | Full extraction via TASK+dependency-extract; `Dependencies.csv` present |

---

## 6. Dependencies.csv — Structured Dependency Register (v3.1)

### 6.1 Schema Version

The `RegisterSchemaVersion` column MUST be present in every row and set to `v3.1`.

### 6.2 Column Specification

#### Core Columns (MUST be present)

| # | Column | Type | Required | Description |
|---|---|---|---|---|
| 1 | `RegisterSchemaVersion` | string | MUST | Schema version identifier (`v3.1`) |
| 2 | `DependencyID` | string | MUST | Unique within the deliverable register (e.g., `DEP-01-01-001`) |
| 3 | `FromPackageID` | string | MUST | Package ID of the host deliverable |
| 4 | `FromDeliverableID` | string | MUST | Deliverable ID of the host deliverable |
| 5 | `FromDeliverableName` | string | MUST | Human-readable name of the host deliverable |
| 6 | `DependencyClass` | enum | MUST | `ANCHOR` or `EXECUTION` |
| 7 | `AnchorType` | enum | MUST | See Section 6.3 |
| 8 | `Direction` | enum | MUST | `UPSTREAM` or `DOWNSTREAM` |
| 9 | `DependencyType` | enum | MUST | See Section 6.3 |
| 10 | `TargetType` | enum | MUST | See Section 6.3 |
| 11 | `TargetPackageID` | string | optional | Package ID of the target (when target is a deliverable) |
| 12 | `TargetDeliverableID` | string | optional | Deliverable ID of the target (when `TargetType=DELIVERABLE`) |
| 13 | `TargetRefID` | string | optional | Stable reference ID for non-deliverable targets (e.g., `SOW-003`, `OBJ-001`) |
| 14 | `TargetName` | string | SHOULD | Human-readable name/description of the target |
| 15 | `TargetLocation` | string | optional | Path, URL, or document identifier for the target |
| 16 | `Statement` | string | SHOULD | Human-readable dependency statement |
| 17 | `EvidenceFile` | string | MUST* | Source document containing evidence (* or `location TBD`) |
| 18 | `SourceRef` | string | MUST* | Path + heading/section within the evidence file (* or `location TBD`) |
| 19 | `EvidenceQuote` | string | SHOULD | Short quote from source (<= 30 words) |
| 20 | `Explicitness` | enum | SHOULD | `EXPLICIT` or `IMPLICIT` |
| 21 | `RequiredMaturity` | string | optional | Maturity level required for the dependency to be satisfied |
| 22 | `ProposedMaturity` | string | optional | Proposed maturity level (agent suggestion) |
| 23 | `SatisfactionStatus` | enum | SHOULD | See Section 6.3 |
| 24 | `Confidence` | enum | SHOULD | `HIGH`, `MEDIUM`, or `LOW` |
| 25 | `Origin` | enum | MUST | `DECLARED` or `EXTRACTED` |
| 26 | `FirstSeen` | date | MUST | ISO date of first extraction (`YYYY-MM-DD`) |
| 27 | `LastSeen` | date | MUST | ISO date of most recent confirmation (`YYYY-MM-DD`) |
| 28 | `Status` | enum | MUST | `ACTIVE` or `RETIRED` |
| 29 | `Notes` | string | optional | Explanatory remarks; epistemic labels (`FACT`, `ASSUMPTION`, `PROPOSAL`) |

#### Extension Columns (MAY be present; non-breaking)

| Column | Type | Description |
|---|---|---|
| `EstimateImpactClass` | enum | `BLOCKING`, `ADVISORY`, `INFO`, `TBD` |
| `ConsumerHint` | enum | `TASK`, `TASK_ESTIMATING`, `AGGREGATION`, `EVALUATION`, `RECONCILIATION_LEGACY`, `TBD` |

### 6.3 Canonical Enum Values

**DependencyClass:**
| Value | Meaning |
|---|---|
| `ANCHOR` | Tree edge: connects deliverable to a definition/traceability node |
| `EXECUTION` | DAG edge: information flow, prerequisite, handoff, or constraint |

**AnchorType:**
| Value | Meaning |
|---|---|
| `IMPLEMENTS_NODE` | Parent definition node (exactly one per deliverable) |
| `TRACES_TO_REQUIREMENT` | Requirement trace link (zero or more) |
| `NOT_APPLICABLE` | Used for EXECUTION rows |

**Direction:**
| Value | Meaning |
|---|---|
| `UPSTREAM` | This deliverable requires information FROM the target |
| `DOWNSTREAM` | This deliverable produces information FOR the target |

**DependencyType:**
| Value | Usage | Meaning |
|---|---|---|
| `PREREQUISITE` | Preferred | Required input or approval before work can proceed |
| `INTERFACE` | Preferred | Explicit data/artifact exchange between deliverables |
| `HANDOVER` | Preferred | Output of one deliverable consumed as input to another |
| `CONSTRAINT` | Preferred | Explicit constraint or condition |
| `ENABLES` | Preferred | This deliverable enables downstream work |
| `OTHER` | Preferred | Dependency that does not fit other categories; used for ANCHOR rows |

**TargetType:**
| Value | Meaning |
|---|---|
| `DELIVERABLE` | Another deliverable in the project |
| `PACKAGE` | A package (used in ANCHOR rows) |
| `WBS_NODE` | Work breakdown structure or scope node |
| `REQUIREMENT` | A specific requirement (SOW item, objective, etc.) |
| `DOCUMENT` | An external or reference document |
| `EQUIPMENT` | Physical equipment or asset |
| `EXTERNAL` | External entity (organization, standard, etc.) |
| `UNKNOWN` | Target cannot be confidently resolved |

**Explicitness:**
| Value | Meaning |
|---|---|
| `EXPLICIT` | Dependency is explicitly stated in source text |
| `IMPLICIT` | Dependency is implied but not directly stated |

**SatisfactionStatus:**
| Value | Meaning |
|---|---|
| `TBD` | Not yet assessed |
| `PENDING` | Assessed but not yet satisfied |
| `IN_PROGRESS` | Actively being worked toward satisfaction |
| `SATISFIED` | Dependency has been fulfilled |
| `WAIVED` | Dependency waived by human decision |
| `NOT_APPLICABLE` | Dependency determined to be not applicable |

**Confidence:**
| Value | Meaning |
|---|---|
| `HIGH` | Strong evidence; explicit source reference |
| `MEDIUM` | Reasonable evidence; some interpretation required |
| `LOW` | Weak evidence; significant interpretation or assumption |

**Origin:**
| Value | Meaning |
|---|---|
| `DECLARED` | Human-declared dependency |
| `EXTRACTED` | Agent-extracted from source documents |

**Status:**
| Value | Meaning |
|---|---|
| `ACTIVE` | Dependency is currently observed and relevant |
| `RETIRED` | Dependency was previously observed but is no longer found in source text |

### 6.4 Row Classification

**ANCHOR rows** connect a deliverable to the project's definition tree:
- Exactly one `IMPLEMENTS_NODE` row SHOULD exist per deliverable (connects to parent package/WBS node)
- Zero or more `TRACES_TO_REQUIREMENT` rows (connect to scope items, objectives, requirements)
- `DependencyType` MUST be `OTHER` for ANCHOR rows
- `AnchorType` MUST NOT be `NOT_APPLICABLE` for ANCHOR rows

**EXECUTION rows** capture information flow and constraints:
- `DependencyClass` MUST be `EXECUTION`
- `AnchorType` MUST be `NOT_APPLICABLE`
- `DependencyType` uses the preferred execution enums (`PREREQUISITE`, `INTERFACE`, `HANDOVER`, `CONSTRAINT`, `ENABLES`, `OTHER`)

### 6.5 Provenance Requirements

Every ACTIVE row MUST include:
- `EvidenceFile`: the source document filename (or `location TBD`)
- `SourceRef`: path + heading/section within the evidence file (or `location TBD`)

`EvidenceQuote` SHOULD be provided (max 30 words) for traceability. This section is the enforcement point for `CONTRACT.md` K-PROV-1.

### 6.6 Lifecycle Tracking

Each row tracks two independent lifecycles:

**Extraction lifecycle:**
- `FirstSeen`: date the row was first created
- `LastSeen`: date the row was most recently confirmed by extraction
- `Status`: `ACTIVE` (currently observed) or `RETIRED` (no longer found in source text)

**Closure lifecycle:**
- `RequiredMaturity`: maturity level needed for satisfaction
- `ProposedMaturity`: agent-suggested maturity level
- `SatisfactionStatus`: current satisfaction state

Rows are never deleted. Rows no longer observed in source text are marked `RETIRED`.

### 6.7 Legacy Compatibility

**Direction normalization:**
- `INBOUND` (legacy) → `UPSTREAM` (canonical)
- `OUTBOUND` (legacy) → `DOWNSTREAM` (canonical)

**DependencyType normalization (see §6.3):**
- `COORDINATION` (legacy) → `OTHER` (canonical, used for ANCHOR rows and catch-all)
- `INFORMATION` (legacy) → Interpret context and map to `PREREQUISITE`, `INTERFACE`, `HANDOVER`, `CONSTRAINT`, or `ENABLES` as appropriate
- Project-specific dependency labels such as `ARCHITECTURE_BASIS`, `DOMAIN_MODEL`, `*_PREDECESSOR`, `*_CONTRACT`, or `SERVICE_API` are read-only migration inputs, not v3.1 core enum values. Current registers MUST map them to the canonical `DependencyType` set and preserve the original label in `Notes` or a documented extension column.
- `CANDIDATE` is not a valid `Status`. Candidate/non-gating graph dispositions belong in graph-governance worklists or review packets outside the canonical `Dependencies.csv` / `DependencyEdges.csv` register.

**SchemaVersion handling:**
- If `RegisterSchemaVersion` is missing from an existing file, add it on write and set to `v3.1`

### 6.8 Identity Rules

- `DependencyID` MUST be unique within a single deliverable's register
- `DependencyID` format: `DEP-{PKG}-{DEL}-{SEQ}` (e.g., `DEP-01-01-001`)
- `FromDeliverableID` MUST match the host deliverable's ID
- For `TargetType=DELIVERABLE`: `TargetDeliverableID` MUST contain the target's stable deliverable ID
- For non-deliverable targets: `TargetDeliverableID` MUST be empty; use `TargetRefID` and `TargetName`

---

## 7. `_REFERENCES.md` — Source Document Pointers

### 7.1 Format

```markdown
# References: {DEL-ID} {DeliverableName}

## Applicable References
- {RefName/ID} — {Location: path/URL} — {Relevance: brief description}

## Notes
- {Additional notes or placeholder if none identified}
```

### 7.2 Rules

- References are listed as relative paths (preferred) or absolute paths to source documents.
- Each reference includes a brief relevance statement.
- `_REFERENCES.md` is created by PREPARATION and MAY be updated by human or PROJECT_SETUP.
- TASK+dependency-extract reads `_REFERENCES.md` but MUST NOT modify it.

---

## 8. `_MEMORY.md` — Working Memory

### 8.1 Format

```markdown
# Memory — {DEL-ID}

> Organize by semantic topic, then chronologically within each topic.

## Key Decisions & Human Rulings

## Domain Context

## Open Items

## Proposal History

## Interface & Dependency Notes
```

### 8.2 Rules

- Created by PREPARATION as an empty structured template.
- Used by WORKING_ITEMS and deliverable-local task agents to record working context.
- Sections MAY be added as needed; the above are the minimum schema.
- `MEMORY.md` (without underscore prefix) MAY exist as a compatibility pointer containing: `See _MEMORY.md (canonical deliverable memory).`

---

## 9. Agent Instruction File Structure

All live agent instruction files currently implement the candidate structure in
`WORKFLOW_COMPONENT_STANDARD.md` and are checked by the instruction validator.
That implementation evidence does not ratify the candidate. HELPS_HUMANS is
the applying/maintenance persona, not the constitutional source. `AGENTS.md`
is a distinct authoritative runtime surface (K-AGENTS-1).

### 9.1 Required Header

```markdown
[[DOC:AGENT_INSTRUCTIONS]]
# AGENT INSTRUCTIONS — {AGENT_NAME} ({Brief Descriptor})
AGENT_TYPE: {0|1|2}
```

### 9.2 Required Agent Type Table

```markdown
## Agent Type

| Property | Value |
|---|---|
| **AGENT_TYPE** | TYPE {0|1|2} |
| **AGENT_CLASS** | {PERSONA|TASK} |
| **INTERACTION_SURFACE** | {chat|INIT-TASK|spawned|both} |
| **WRITE_SCOPE** | {scope description} |
| **BLOCKING** | {never|allowed} |
| **PRIMARY_OUTPUTS** | {description} |
```

### 9.3 Required Sections

Every agent instruction file MUST include these section markers:

| Section | Marker | Purpose |
|---|---|---|
| PROTOCOL | `[[BEGIN:PROTOCOL]]` ... `[[END:PROTOCOL]]` | Execution procedure (sequencing, interactions) |
| SPEC | `[[BEGIN:SPEC]]` ... `[[END:SPEC]]` | Validity requirements (pass/fail criteria) |
| STRUCTURE | `[[BEGIN:STRUCTURE]]` ... `[[END:STRUCTURE]]` | Schemas, templates, artifact definitions |
| RATIONALE | `[[BEGIN:RATIONALE]]` ... `[[END:RATIONALE]]` | Interpretation and values (non-normative) |

### 9.4 Precedence Order

When sections conflict, resolution follows:

```
PROTOCOL > SPEC > STRUCTURE > RATIONALE
```

### 9.5 Classification Properties

| Property | Valid Values | Meaning |
|---|---|---|
| `AGENT_TYPE` | `TYPE 0`, `TYPE 1`, `TYPE 2` | Architect / Manager / Specialist |
| `AGENT_CLASS` | `PERSONA`, `TASK` | Interactive session vs. straight-through pipeline |
| `INTERACTION_SURFACE` | `chat`, `INIT-TASK`, `spawned`, `both` | How the agent is invoked |
| `WRITE_SCOPE` | base values: `repo-wide`, `project-level`, `package-level`, `deliverable-local`, `tool-root-only`, `workspace-scaffold-only`, `repo-metadata-only`, `bounded-task-brief`, `none` | What the agent is allowed to write |
| `BLOCKING` | `never`, `allowed` | Whether the agent may pause for human input |

**`WRITE_SCOPE` parameterization.** A `tool-root-only` scope MAY be parameterized to a specific tool root or registered subtree — for example `tool-root-only ({EXECUTION_ROOT}/_Evaluation/<subtree>/)`. The parameterized form satisfies the `AUDIT_GOVERNANCE` registry check via its parent tool root (see §1.2). `bounded-task-brief` is the canonical scope of the `TASK` shell: writes are authorized only by the effective bounded task brief (`AllowedWriteTargets` or an explicitly named boundary), never by `ScopePath`/`DeliverablePath` alone, and always subject to ScopePath containment (§0.2.3).

### 9.6 Naming Convention

Use `AGENT_*` when referring to instruction files (e.g., `AGENT_CHANGE.md`). Use the role name (e.g., `CHANGE`) when referring to the agent itself.

### 9.7 Runtime Metadata Contract (Harness)

Harness runtime metadata parsing uses a split contract:

- **YAML frontmatter** (machine fields consumed by runtime where present): `description`, `subagents`, `tools`, `model`, `max_turns`, `disallowed_tools`, `auto_approve_tools`, `allow_generalist_agent2`, and `dedicated_agent2_approval`.
- **Canonical body header/table**: the `AGENT_TYPE: {0|1|2}` line in the instruction body and the `AGENT_CLASS` value in the Agent Type table.

Subagent registry safety rules:
- The former SDK Agent compatibility bridge is disabled after managed-runtime
  acceptance. The canonical managed runtime permits Agent 0 to launch named
  Agent 1 sessions and Agent 1 to launch valid Agent 2 forms; historical Agent
  tool requests fail closed.
- Agent 1 delegates only Agent 2 forms. `AGENT_CLASS: TASK` remains preferred
  for persistent Agent 2 packages.

Delegation governance rule (fail closed): when subagents are enabled and a Type 1 persona is allowlisted for subagents, runtime injects subagents only if valid governance metadata is present (`contextSealed === true`, `pipelineRunApproved === true`, a non-empty `approvalRef`). The reference MUST cite the applicable human approval record; runtime presence checks are necessary but do not authenticate or create that human act. Missing or invalid governance metadata MUST block subagent injection while allowing the parent turn to continue normally. Deployment-specific harness/runtime API and UI contracts (turn input, attachment handling, selector schemas) are defined in the owning project's runtime docs, not at the framework root.

### 9.8 Managed Multi-Agent Runtime Record

The managed runtime persists one durable record tree per orchestration
run under `{EXECUTION_ROOT}/_Coordination/AgentRuns/<RunID>/`. It contains the
versioned orchestration plan, work graph, instance launch briefs/status/returns,
coordination notices and dispositions, parent updates and acknowledgments,
brief amendments, and final handoff state.

Plans, briefs, returns, notices, dispositions, updates, amendments, and
acknowledgments are immutable/versioned entries. `STATUS.json` and
`HANDOFF_STATE.md` are runtime-owned materialized summaries reconstructed from
those records and may advance as a child or run changes state.

Every work graph records `RunID`, `PlanVersion`, selection authority,
descriptive posture, accepted basis, agent-instance nodes, dependency edges,
concurrency eligibility, read scopes, write ownership, expected returns,
fan-in gates, and human decision points. Every managed instance records its
logical parent, agent role/type, instruction or brief hash, declared context,
tools, writes, output artifacts, and status.

The runtime rejects direct sibling messaging, invalid parent/child type pairs,
undeclared writes, concurrent path overlap (including ancestor containment),
missing seals/approval references, capability inheritance, and fan-in over
missing or invalid returns. Overlapping writes require an accepted predecessor
or one declared integration owner.

---

## 10. Filesystem-Safe Labels

### 10.1 Sanitization Rule

`Sanitize(name)`:
1. Replace any of these characters with `-`: `/`, `\`, `:`, `*`, `?`, `"`, `<`, `>`, `|`
2. Collapse consecutive whitespace to a single space
3. Trim leading/trailing whitespace

### 10.2 Folder Naming

- Package folders: `{PKG-ID}_{Sanitize(PackageName)}/`
- Deliverable folders: `{DEL-ID}_{Sanitize(DeliverableName)}/`
- Canonical (unsanitized) names are recorded in `_CONTEXT.md`.

---

## 11. Snapshot and Pointer Conventions

### 11.1 Snapshot Folders

Task agents that produce outputs to tool roots SHOULD write to timestamped snapshot folders:

```
{TOOL_ROOT}/{SNAPSHOT_LABEL}_{YYYY-MM-DD}_{HHmm}/
```

Snapshot folders are immutable after creation. Reruns create new snapshot folders. This is the enforcement point for `CONTRACT.md` K-SNAP-1.

### 11.2 Pointer Files

`_LATEST.md` is a mutable pointer file that references the most recent snapshot:

```markdown
Latest: {SNAPSHOT_FOLDER_NAME}
Updated: {YYYY-MM-DD}
```

Pointer files MAY be overwritten; snapshots MUST NOT.

---

## 12. Folder Structure Validation Checklist

### 12.1 Valid Execution Root

An execution root is valid when:
- [ ] At least one `PKG-XX_{Label}/` folder exists
- [ ] `_Decomposition/` folder exists and contains at least one decomposition document
- [ ] `INIT.md` exists with session parameters

### 12.2 Valid Package Folder

A package folder is valid when:
- [ ] Named `{PKG-ID}_{PkgLabel}/` with a valid `PKG-XX` identifier
- [ ] Contains `1_Working/` subfolder
- [ ] `0_References/`, `2_Checking/`, and `3_Issued/` subfolders SHOULD exist

### 12.3 Valid Deliverable Folder

A deliverable folder is valid when:
- [ ] Named `{DEL-ID}_{DelLabel}/` with a valid `DEL-XX-YY` identifier
- [ ] Contains `_STATUS.md` with a valid lifecycle state
- [ ] Contains `_CONTEXT.md` with header fields matching the decomposition
- [ ] Contains `_DEPENDENCIES.md`
- [ ] Contains `_REFERENCES.md`

A deliverable folder is **initialized** (state >= `INITIALIZED`) when it
additionally resolves to exactly one valid production format under §2.2:
`SOW_V1`, or `LEGACY_FOUR_DOC` during the authorized transition. New
deliverables must resolve to `SOW_V1`.

A deliverable folder is **dependency-tracked** when it additionally contains:
- [ ] `Dependencies.csv` with valid v3.1 schema headers

---

## 13. `_COORDINATION.md` — Coordination Representation

Located at `{EXECUTION_ROOT}/_Coordination/_COORDINATION.md`.

Records the project's chosen coordination representation:
- **Schedule-first:** Gantt drives sequencing; dependency tracking is active for blocker detection and audit
- **Dependency-tracked:** Dependency graph drives sequencing
- **Hybrid:** Combination of schedule-first and dependency-tracked

The coordination representation is chosen per project instance and recorded once. It does not change the dependency tracking mechanics (which always maintain the full DAG), only how teams use the graph for scheduling.

The coordination root also holds the session control-plane handoff files (`NEXT_INSTANCE_PROMPT.md` and, where used, `NEXT_INSTANCE_STATE.md`); see `AGENT_PROJECT_SETUP.md`.

---

## Deferred to working-root / runtime docs

The prior root SPEC carried desktop-frontend UI navigation and `/api/project/deliverables` response contracts. Those are deployment-specific runtime contracts, not framework-root structures, and are owned by the runtime project's docs (`projects/chirality-app-dev/docs/`). They are intentionally not reproduced here.

---

## 14. Root-Owned Shared Runtime

The root `runtime/` workspace contains versioned contracts, provider-neutral
orchestration, a daemon, a Unix-socket client, a CLI, and safe engine/provider
adapters. It is an independent Node workspace with its own lockfile. Project
applications consume its public packages; private project adapters do not
become generic runtime dependencies.

### 14.1 Local control plane

The packaged Chirality application may run in `--runtime-daemon` mode without
a window. Its only control listener is
`{userData}/runtime/control.sock`. The parent directory is mode `0700`; the
socket and owner/auth records are mode `0600`. Stale-socket recovery verifies
current-user ownership and absence of a live recorded process before removal.

Installation is opt-in through the bundled CLI. The installed macOS
LaunchAgent has label `com.chirality.runtime`, starts at login, restarts after
failure, writes logs and mutable state beneath Chirality user data, and does
not load any local model automatically.

HTTP/1.1 JSON requests and canonical SSE responses cover health, project
registration/status, session create/list/boot/replay/turn/interrupt,
high-level Agent 1 runs, provider credentials, and explicit oMLX model
status/activation. Tokens are hashed at rest, scoped to a client and optional
project, and compared in constant time. Browser code never receives a runtime
credential.

### 14.2 Project manifests and sessions

Each registered checkout supplies `chirality.project.json` with schema
`chirality.project/v1`, a stable project ID and display name, relative
working/instruction/AGENTS/execution references, profile references, enabled
adapter IDs, and an embedded-UI declaration. Registration containment-checks
the resolved paths and records the manifest hash and approval outside the
checkout. Privileged execution stops on manifest drift until re-registration.

Canonical runtime sessions live beneath
`{userData}/runtime/projects/<projectId>/sessions`. A legacy project-local
session may be copied and validated lazily on access, with migration evidence;
the source remains untouched for the migration cycle. JSON/JSONL stays the
runtime evidence format.

### 14.3 Local-model residency

The first managed provider is authenticated literal-loopback oMLX. Discovery
uses `GET /v1/models/status`; explicit transitions use the exact model ID with
`POST /v1/models/{id}/unload` and `POST /v1/models/{id}/load`. Redirects,
embedded URL credentials, remote hosts, and aliases are rejected.

One primary local LLM may be managed at a time. Activation rejects new local
turns, drains active Pi turns for at most ten minutes, and completes the whole
transition within twenty minutes. Drain timeout retains the current model.
Load failure after unload enters `NO_MODEL`. Unknown helper, embedding, and
reranking models are never automatically unloaded. Redacted transition
evidence assigns an epoch referenced by local sessions and AgentRuns.

### 14.4 Initial governed run

`chirality run --project <id> --agent <Agent1Role> --brief-file <path>
--local-model <exact-id>` creates a real Agent 1 session. The exact local model
must already be resident. The run authorizes at most one Pi/oMLX Agent 2 child
with one declared read-only Chirality tool and requires the Agent 1 to review
its return. Missing compliant delegation terminates with
`REQUIRED_DELEGATION_MISSING`. Agent 2 cannot delegate.

The complete initial CLI surface is:

```text
chirality daemon install|start|stop|status|uninstall
chirality project register|list|status
chirality models list|activate
chirality session create|list|replay|turn|interrupt
chirality run --project <id> --agent <role> --brief-file <path>
              [--local-model <exact-id>] [--json]
```

Run requests may also arrive through standard input or a request file. Human
output is the default; `--json` emits newline-delimited canonical events.
Credential values remain Desktop-managed and are neither accepted nor
displayed by this initial CLI.
