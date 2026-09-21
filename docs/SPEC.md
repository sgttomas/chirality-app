# SPEC — Physical Structures and Mechanics

> PROSPECTIVE EXACT POST-IMAGE — NOT APPLIED. The runtime migration authority contract controls the named successor clauses only after its actual owner acceptance and effective propagation. Prior ratification remains the basis for unaffected requirements; historical product completion/ownership statements are prospectively superseded as specified below. No product gate, release or Root retirement is declared complete by these draft bytes.

> **Status: RATIFIED — owner ratification 2026-07-11 (`CONTRACT.md` / K-AUTH-1).** Owner direction of record (2026-07-11, in-session, Ryan Tufts): "You can now take all the `docs/` out of the DRAFT state, making them authoritative." This document is accepted root governance in full. Provenance: it re-established the monorepo-root governance layer (root `docs/` was hollowed out during the four-repo merge; see `plans/monorepo_root_governance_and_path_anchoring_2026-06-15.md`), authored from the prior root canon (`.archive/SPEC.md`), preserving the established §1–§13 numbering and schemas, and adding the **Root Model and Path Anchoring** convention (§0.2–§0.3) plus reconciliations to the live agent surface. **Ratification history:** per D-GOV-05 (`docs/governance_harness/_DECISIONS/D-GOV-05_minimal_governance_basis.md`, ruled by owner 2026-07-01), K-WRITE-2 path containment (§0.2.3) was ratified first as part of the minimal harness basis; the 2026-07-11 full ratification subsumes that partial basis.

This document is the authoritative specification for the physical structures, file formats, schemas, and layout conventions of the filesystem-as-state agent operating system contained in Chirality Root.

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

Chirality supports separately scoped Root governance/instruction changes, explicitly governed in-tree v1 projects, registered external v2 projects/domains and desktop-selected working folders. Root governance is not a continuing product working root after accepted retirement. Instruction reads and write containment follow the chosen deployment dialect.

### 0.2.1 `REPO_ROOT` — the active checkout

`REPO_ROOT` is the root of the active git checkout, resolved as:

```sh
REPO_ROOT="$(git rev-parse --show-toplevel)"
```

`REPO_ROOT` MUST be resolved at session start and never hard-coded. In a linked **git worktree**, `git rev-parse --show-toplevel` returns *that worktree's* root — so a worktree is a fully isolated checkout, and every path derived from `REPO_ROOT` re-anchors to it automatically. This is the mechanism that makes worktree-based isolation safe.

`REPO_ROOT` is the active writable Git checkout. Root governance instruction changes act on the repository only under separate explicit scope/M2 authority. Product WORKING_ROOT remains the selected project directory; external projects use their own checkout with disjoint runtime-declared instructions.

`INSTRUCTION_ROOT` is the runtime-declared, read-only home of the **shared instruction surface** (`AGENTS.md`, `CLAUDE.md`, `agents/`, `workflows/`, `tools/`, root `docs/`, `init/`, `.github/workflows/`) — the release-managed agent operating system (see `DIRECTIVE.md` §2.6). The runtime resolves it from `CHIRALITY_INSTRUCTION_ROOT`; a V2 project registration fails if it is missing, unreadable, or overlaps the working root. `CLAUDE.md` imports `AGENTS.md` without adding another instruction layer. The instruction surface is read-mostly: changing it is a repo-wide governance action, not ordinary working-root execution.

### 0.2.2 `WORKING_ROOT` — the active workspace

`WORKING_ROOT` is the selected project or domain workspace, explicitly governed in-tree project, or desktop-selected folder. It contains governed product truth and remains subject to ScopePath containment. Historical Root product execution is retained evidence after accepted retirement; Root governance maintenance uses separately authorized repository scopes.

- `WORKING_ROOT` MUST resolve to an absolute path under the active writable `REPO_ROOT`.
- One `INSTRUCTION_ROOT` serves **many** working repositories without per-workspace instruction drift.
- Project writes MUST remain within the selected WORKING_ROOT. Explicit in-tree v1 instruction references may resolve outside it, but never grant instruction writes. External v2 instruction roots MUST be physically disjoint. Root instruction changes require independently owner-authorized M2/G4 tranches; containment itself grants no authority.

### 0.2.3 ScopePath containment (binding)

Every `ScopePath` and every `AllowedWriteTarget` (see `AGENT_WORKFLOW_RUNTIME.md`) MUST:

1. normalize to an absolute path, and
2. resolve **under `WORKING_ROOT`**, which is itself contained by the active checkout returned by `git rev-parse --show-toplevel`.

A `ScopePath` or write target that resolves outside the selected working root — including a sibling pack, the instruction root, a symlink escape, or `..` traversal — MUST be rejected (`SCOPE_OUTSIDE_WORKTREE` or `WRITE_TARGET_OUTSIDE_WORKTREE`); the task stops rather than writing. This is the deterministic backstop that prevents a run from writing into another checkout or pack. This rule is bound as `CONTRACT.md` invariant **K-WRITE-2**.

### 0.2.4 Path reference discipline

- **Instruction-surface references** (to `agents/`, `workflows/`, `tools/`, root `docs/`, `AGENTS.md`) resolve **`INSTRUCTION_ROOT`-relative**.
- **Working-root references** (to `{EXECUTION_ROOT}`, tool roots, deliverables, `_Coordination/`, decomposition state) resolve **`WORKING_ROOT`-relative**.
- Instruction, coordination, and plan files MUST NOT embed machine-absolute paths (e.g. `/Users/<name>/...`). Absolute paths are permitted only in run records and evidence artifacts, where they record what actually happened and are never re-executed.

---

## 0.3 Path Token Registry

Agent instructions and workflows reference roots through `{*_ROOT}` tokens. Each token resolves against exactly one anchor. Projects and domains MAY bind additional workspace-local tokens, but every such token MUST resolve under `WORKING_ROOT`.

| Token | Anchor | Resolves to |
|---|---|---|
| `{REPO_ROOT}` | self | `git rev-parse --show-toplevel` (the active checkout) |
| `{INSTRUCTION_ROOT}` | runtime-declared | the shared instruction surface; the Chirality checkout, packaged app resources, or the separately governed repository instruction root |
| `{WORKING_ROOT}` | `REPO_ROOT`-relative | the selected project/domain pack or user-selected folder; Root governance maintenance is separately scoped and is not project product execution |
| `{EXECUTION_ROOT}` | `WORKING_ROOT`-relative | the execution instance root (project-defined; often `WORKING_ROOT` or `WORKING_ROOT/execution`) |
| `{COORDINATION_ROOT}` | `EXECUTION_ROOT`-relative | `{EXECUTION_ROOT}/_Coordination/` |
| `{DECOMP_ROOT}` / `{DECOMPOSITION_ROOT}` | `EXECUTION_ROOT`-relative | `{EXECUTION_ROOT}/_Decomposition/` (or a domain pack's `_Decomposition/`) |
| `{AGGREGATION_ROOT}` | tool-root-relative | `{EXECUTION_ROOT}/_Aggregation/` |
| `{EVALUATION_ROOT}` | tool-root-relative | `{EXECUTION_ROOT}/_Evaluation/` |
| `{RECONCILIATION_ROOT}` | tool-root-relative | `{EXECUTION_ROOT}/_Reconciliation/` |
| `{ESTIMATES_ROOT}` | tool-root-relative | `{EXECUTION_ROOT}/_Estimates/` |
| `{SOURCE_AUDIT_ROOT}`, `{ASSETS_ROOT}`, `{PUBLICATION_ROOT}`, `{RESEARCH_ROOT}`, `{PLANNING_ROOT}`, `{RUN_ROOT}`, `{CONTEXT_ROOT}` | `WORKING_ROOT`-relative | domain/workspace-local roots bound by the owning role/workflow; MUST resolve under `WORKING_ROOT` |
| `{WORKFLOW_ROOT}` | `INSTRUCTION_ROOT`-relative | `{INSTRUCTION_ROOT}/workflows/<name>/` |
| `{SKILL_ROOT}` | historical adapter token | Historical briefs retain their recorded binding; the migration adapter maps a selected legacy package to `{WORKFLOW_ROOT}` without granting writes. |
| `{TOOL_ROOT}` | context-dependent | `{INSTRUCTION_ROOT}/tools/` when referring to the deterministic tool layer; a project tool root (`{EXECUTION_ROOT}/_<Name>/`) when referring to a derived-output root (see §1.2) |

The token vocabulary above is the registry; an agent that introduces a new `{*_ROOT}` token MUST declare its anchor in the applicable runtime or workflow contract and keep it consistent with this table.

---

## 1. Execution Root Layout

An execution instance is a self-contained project workspace rooted at `{EXECUTION_ROOT}/` (which resolves `WORKING_ROOT`-relative; see §0.2–0.3). The execution root contains packages (work partitions) and tool roots (derived/operational outputs). After effective retirement, `REPO_ROOT/execution` retains Root governance coordination and historical product evidence only. It is not eligible for new active Root package/deliverable materialization. Source IDs remain reserved; accepted retirement maps exclude them from active product selection.

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

The `_Archive/` subfolders above are **local working state, not tracked repo content**: the repository ignore policy excludes every `_Archive/` path ("Archives are historical/local, not canonical repo content"), so these folders exist in a working checkout but are not under version control, and nothing canonical may live only in an `_Archive/`.

### 1.2 Tool Roots

Tool roots are workspace-level directories for derived outputs, resolved `{EXECUTION_ROOT}`-relative. Each tool root is isolated from source truth (deliverable folders). A tool-root path is the canonical write destination for `tool-root-only` agents (see §9.5); `AUDIT_GOVERNANCE` validates that every agent's `WRITE_SCOPE` references a registered tool root and that every tool root has at least one writer.

| Tool Root | Purpose | Typical Writer |
|---|---|---|
| `_Aggregation/` | Aggregation snapshots and templates | AGGREGATION |
| `_Change/` | Change management records | CHANGE |
| `_Coordination/` | Coordination representation | PROJECT_SETUP |
| `_Decomposition/` | Project/domain decomposition document(s) and companions | WORKING_ITEMS with `project-decomp`, `software-decomp`, or `domain-decomp` |
| `_Estimates/` | Cost estimate snapshots | TASK + estimate workflows |
| `_Evaluation/` | Current evaluation reports plus structural, dependency, epistemic, governance, agent, coherence, and review snapshots | EVALUATION / EVALUATION_* / REVIEW / AUDIT_* |
| `_Reconciliation/` | Calibrated deliverable-corpus concordance runs and historical immutable generic-audit artifacts | RECONCILIATION |
| `_Schedule/` | Schedule snapshots generated from the dependency graph | PROJECT_SETUP scheduling workflow |
| `_ScopeChange/` | Change-impact assessments and decomposition amendment snapshots | WORKING_ITEMS with `scope-change` |
| `_Sources/` | Shared source/reference documents | Human / source-extraction pipelines |
| `_LocalIndexes/` | Derived source-catalog and retrieval snapshots (domain packs) | WORKING_ITEMS with `domain-decomp` / retrieval tools |
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

## 9. Agent Instruction and Workflow Structure

Prospective replacement under D-GOV-41; incompatible consumers remain behind
the adoption hold in `AGENT_WORKFLOW_RUNTIME.md`.

### 9.1 Role files

The four durable instruction files are `AGENT_HELP_HUMAN.md`,
`AGENT_HELPS_HUMANS.md`, `AGENT_WORKING_ITEMS.md`, and `AGENT_TASK.md`, under
`agents/`. Each contains a role title and exactly these level-two sections:
PROTOCOL, SPEC, STRUCTURE, RATIONALE. Their content is characteristic conduct,
standards of judgment, relationships/forms of contribution, and purpose of the
role, respectively. Interpretation follows that order. Rationale grants no
permission.

### 9.2 Runtime configuration

`agents/registry.json` carries role type, entry and delegation eligibility,
instruction path, capability ceilings, and scope ceiling. The schema and
selection contract are defined in `AGENT_WORKFLOW_RUNTIME.md`. These fields are
not duplicated in role prose. A run's brief supplies concrete context, tools,
write targets, outputs, and acceptance checks.

### 9.3 Workflow files

A discoverable workflow is an immediate `workflows/<name>/` directory containing
`WORKFLOW.md`. Its name matches the directory; its description supports explicit
lookup. Method structure and supporting resources follow the undertaking.
Optional `execution.json` provides compatible roles and tool restrictions.
`Workflow` is the canonical selection field; the adapter handles historical
`TaskSkill` inputs. Routine context loads only selected workflow resources.

### 9.4 Permissions and path binding

The host, role, workflow, and brief jointly bound effective permissions.
Capability-name restrictions and command/scope expressions intersect at their
own layers. Paths resolve against declared working, instruction, and tool roots;
real-path containment rejects escape. `ScopePath` or `DeliverablePath` alone
never grants writes. The authorized brief names writable targets explicitly.

### 9.5 Scope and construction compatibility

Scope ceilings retain `repo-wide`, `project-level`, `package-level`,
`deliverable-local`, `tool-root-only`, `workspace-scaffold-only`,
`repo-metadata-only`, `bounded-task-brief`, and `none` where applicable to runtime
configuration or historical contracts. A tool-root-only ceiling may name a
registered subtree. Every actual write remains bounded by the run brief and
§0.2.3. WORKING_ITEMS may coordinate any explicitly authorized bounded
undertaking, including package/deliverable assignments governed by their own
contracts. Type 2 construction is TASK or an ephemeral bounded executor.

### 9.6 Naming

Use `AGENT_<ROLE>.md` for a role's instruction file, the role name for the actor,
and `Workflow: <name>` for its selected method. Historical actor names remain
unchanged in recorded evidence. Their replacements are in the disposition ledger.

### 9.7 Delegation and adoption

The two executable delegation classes in D-GOV-35 remain available. Managed
children use actual child sessions, sealed context, approved pipeline authority,
explicit scopes, and durable evidence. A recorded approval reference does not
create or authenticate a human act. Native descendants retain their actual
host boundary; role non-delegation may be instruction-asserted. Loading a
workflow changes neither role nor authority.

Consumers of old prose metadata remain on their accepted source basis until
their owning loops adopt the replacement registry and workflow interfaces.
Runtime service API details remain with the owning project.

### 9.8 Multi-agent run record

Record versioned plans, work graphs, launch briefs, actual instance parentage,
source hashes, scopes, notices, amendments, returns, and handoff state under
`{EXECUTION_ROOT}/_Coordination/AgentRuns/<RunID>/` when the owning workflow uses
that record root. Distinguish runtime-persisted records from an authorized
agent's factual transcription of native execution. Read-only callers return
records to an authorized writer.

Graphs name dependencies, concurrent write ownership, expected returns, and
human decisions. Coordinate through the parent. Overlapping writes require
serialization or one integration owner. An executed child is required for an
execution claim; a brief alone is insufficient. State actual enforcement limits
and validate combined results before accepting fan-in.

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

The coordination root also holds the session control-plane handoff files (`NEXT_INSTANCE_PROMPT.md` and, where used, `NEXT_INSTANCE_STATE.md`); see `workflows/project-setup/WORKFLOW.md`.

---

## Deferred to working-root / runtime docs

The prior root SPEC carried desktop-frontend UI navigation and `/api/project/deliverables` response contracts. Those are deployment-specific runtime contracts, not framework-root structures, and are owned by the runtime project's docs (`projects/chirality-app-dev/docs/`). They are intentionally not reproduced here.

---

## 14. Shared Runtime Product and Governance Boundary

The `projects/chirality-runtime/` project owns versioned contracts, provider-neutral
orchestration, the Runtime service, a Unix-socket client, a CLI, and safe
engine/provider adapters. It is an independent Node workspace with its own
lockfile. Project applications consume its public packages; private project
adapters do not become generic runtime dependencies. The service composition
stays independent of Electron and Next so a later Chirality application can
run it as its own sidecar (D-GOV-43 A2 supplement).

### 14.1 Application-owned Runtime service and Codex child

The Chirality App starts one Runtime service as a child process at launch,
owns it for the life of the App instance, and stops it deliberately on quit.
There is no per-user LaunchAgent, installer, or headless daemon mode. The
service reports readiness with one ready line on its standard output; the App
waits for that line before routing any request. If the service exits
unexpectedly the App restarts it with bounded backoff and shows the outage;
it never presents unexpected termination as completion.

The service's only control listener is one Unix-domain socket beneath the
application user-data directory, with a `0700` parent directory and a `0600`
socket. Stale-socket recovery verifies current-user ownership and absence of a
live recorded process before removal. The App issues a per-launch client
token, stored under user data and private to the application, and presents it
on every request; the token is not exposed to the renderer. No second socket
and no TCP listener exist under any configuration. The service's HTTP/1.1
JSON and SSE routes cover health, project registration and status, thread
create, list, resume, turn, interrupt, and server-request answers, and
Codex-managed login and logout.

The service owns the stock, version-pinned `codex app-server` child from the
official `@openai/codex` distribution, launched over stdio against Chirality's
effective Codex home, which shares the user's configuration, skills, plugins,
MCP definitions, instruction caches, and sessions store by reference and
keeps `auth.json` and the models cache private. The service forwards the
complete notification and server-request stream; every server request
receives an answer, and an unfamiliar request receives an explicit error
response rather than silence.

Execution, observation, interruption, and shutdown are distinct. The Runtime
owns the active turn. The renderer observes it through loopback HTTP and SSE
served by the in-process Next server; a renderer subscription that drops does
not stop the turn, and reopening recovers current state, missed activity, and
outstanding decisions without re-sending the prompt or executing twice.
Explicit Stop is the interrupt. Quit stops the owned Runtime and Codex
processes deliberately and leaves an accurate continuation record; no
unattended execution after quit is promised.

The App keeps a thread index keyed by Codex thread id in its operational
user-data state (title, project, role, plan revisions, workflow selections,
evidence pointers). On relaunch the App resumes an indexed thread through
`thread/resume`; the sidebar shows the App's index, not every thread in the
shared store.

### 14.2 Project manifests and sessions

Each registered checkout supplies `chirality.project.json`. Schema
`chirality.project/v1` remains supported for in-tree manifests with relative
working and instruction references. Schema `chirality.project/v2` declares
`instructionRoot: {"mode":"runtime"}` so an external writable checkout can
consume the read-only `CHIRALITY_INSTRUCTION_ROOT`. V2 registration requires
that root to be readable and disjoint from the working root. Both schemas carry
a stable project ID and display name, execution and profile references, enabled
adapter IDs, and an embedded-UI declaration. Registration containment-checks
the resolved paths and records the manifest hash and approval outside the
checkout. Privileged execution stops on manifest drift until re-registration.

Threads are ordinary Codex threads in the shared Codex sessions store of
Chirality's effective home; the App keeps its own index and metadata keyed by
Codex thread id under user data (§14.1). Both are operational,
non-authoritative state. Daemon-era session records beneath
`{userData}/runtime/projects/<projectId>/sessions` are preserved unchanged in
place as a readable archive; no import is a release prerequisite, and their
continuation as Codex threads is not promised. Chirality evidence required by
a governing workflow is written to checkout-contained project evidence in
JSON/JSONL.

### 14.3 Local-model residency (retired)

Retired by D-GOV-43 item 13. Local models, when taken up, are Codex model
providers. The prior text is preserved in git history.

### 14.4 Initial governed run (retired)

Retired to history with the daemon CLI it described (D-GOV-43 items 7 and
13, as applied by the A2 tranche). The prior text is preserved in git history.

## Prospective Root execution registration successor

Root execution/ hosts governance coordination, successor assurance records and historical product evidence. It is not eligible for new active Root PKG/DEL materialization after effective product retirement. Ordinary project execution roots retain SPEC's package/deliverable and lifecycle contracts. Product retirement is tracked in the accepted archive/disposition register and excluded from active scanners; no source directory is deleted and IDs remain reserved.


### Root historical-product mode — migration-specific extension

After the exact transfer/retirement act, a Root adapter may declare governance-only mode only with the accepted 53-carrier/104-scope/six-parent disposition register and 46 control references. RETIRED is a migration-specific historical Root registration value, never an active project lifecycle value. No source file is deleted. Root active scanners reject these historical carriers as dispatch targets and reject new Root product materialization. Ordinary project lifecycle and ScopePath checks remain unchanged. Governance/instruction tool invocations require explicit authorized repository scopes and their own containment contract; this extension grants no project write escape and no implicit WORKING_ROOT=REPO_ROOT fallback. Successor G0–G3 must enforce this contract before the mode becomes usable; G4 remains mandatory on its instruction surfaces.
