# SPEC — Physical Structures and Mechanics

This document is the authoritative specification for the physical structures, file formats, schemas, and layout conventions used in the Chirality filesystem-as-state project execution system.

All agents, tools, and governance documents reference this specification. Where an agent instruction file defines a format inline, this document is the canonical version; agent instructions MUST conform.

**Normative keywords:** MUST, MUST NOT, SHOULD, SHOULD NOT, MAY follow the conventions defined in `AGENT_HELPS_HUMANS.md`.

---

## 1. Execution Root Layout

An execution instance is a self-contained project workspace rooted at `{EXECUTION_ROOT}/`. The execution root contains packages (work partitions) and tool roots (derived/operational outputs).

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
├── _Decomposition/                  # Project decomposition document(s)
│   └── _Archive/
├── _Estimates/                      # Cost estimate snapshots
├── _Reconciliation/                 # Reconciliation reports, closure analysis
├── _Archive/                        # Baseline snapshots with checksums
├── _Scripts/                        # Deployment and analysis scripts
└── _Sources/                        # Shared source/reference documents
```

### 1.1 Package Folders

**Naming:** `{PKG-ID}_{PkgLabel}/` where `PKG-ID` follows the `PKG-XX` format and `PkgLabel` is a filesystem-safe version of the package name (see Section 10).

**Required subfolders:**

| Subfolder | Purpose |
|-----------|---------|
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

Tool roots are project-level directories for derived outputs. Each tool root is isolated from source truth (deliverable folders).

| Tool Root | Purpose | Typical Writer |
|-----------|---------|----------------|
| `_Aggregation/` | Aggregation snapshots and templates | AGGREGATION agent |
| `_Change/` | Change management records | CHANGE agent |
| `_Coordination/` | Coordination representation | ORCHESTRATOR |
| `_Decomposition/` | Project decomposition document(s) | PROJECT_DECOMP agent |
| `_Estimates/` | Cost estimate snapshots | ESTIMATING agent |
| `_Reconciliation/` | Reconciliation reports, closure analysis | RECONCILIATION agent |
| `_Archive/` | Baseline snapshots with checksums | Human / CHANGE agent |
| `_Scripts/` | Deployment and analysis scripts | Human / tooling |
| `_Sources/` | Shared source/reference documents | Human |

---

## 2. Deliverable Folder Layout

Each deliverable occupies a folder at:

```
{EXECUTION_ROOT}/{PKG-ID}_{PkgLabel}/1_Working/{DEL-ID}_{DelLabel}/
```

### 2.1 File Inventory

| File | Presence | Created By | Purpose |
|------|----------|------------|---------|
| `_STATUS.md` | MUST | PREPARATION | Lifecycle state and history |
| `_CONTEXT.md` | MUST | PREPARATION | Identity, decomposition pointer, traceability |
| `_DEPENDENCIES.md` | MUST | PREPARATION | Dependency summary (human declarations + agent extractions) |
| `_REFERENCES.md` | MUST | PREPARATION | Source document pointers |
| `Datasheet.md` | MUST | 4_DOCUMENTS | Key parameters and structured metadata |
| `Specification.md` | MUST | 4_DOCUMENTS | Technical requirements and scope definition |
| `Guidance.md` | MUST | 4_DOCUMENTS | Design guidance, rationale, and best practices |
| `Procedure.md` | MUST | 4_DOCUMENTS | Step-by-step execution workflow |
| `Dependencies.csv` | SHOULD | DEPENDENCIES | Structured dependency register (v3.1 schema) |
| `_MEMORY.md` | SHOULD | PREPARATION | Working memory (shared by WORKING_ITEMS and TASK agents) |
| `_SEMANTIC.md` | MAY | CHIRALITY_FRAMEWORK | Semantic lens with derivation work |
| `_SEMANTIC_LENSING.md` | MAY | CHIRALITY_LENS | Semantic analysis narrative |
| `MEMORY.md` | MAY | PREPARATION | Compatibility pointer to `_MEMORY.md` |

**Minimum viable fileset (PREPARATION):** `_STATUS.md`, `_CONTEXT.md`, `_DEPENDENCIES.md`, `_REFERENCES.md`, `_SEMANTIC.md` (placeholder).

**Document kit (4_DOCUMENTS):** `Datasheet.md`, `Specification.md`, `Guidance.md`, `Procedure.md`.

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

### 3.2 Valid Lifecycle States

```
OPEN → INITIALIZED → SEMANTIC_READY → IN_PROGRESS → CHECKING → ISSUED
```

| State | Meaning | Typical Trigger |
|-------|---------|-----------------|
| `OPEN` | Folder exists, no content yet | PREPARATION creates folder |
| `INITIALIZED` | Draft documents generated | 4_DOCUMENTS completes document kit |
| `SEMANTIC_READY` | Semantic lens generated | CHIRALITY_FRAMEWORK writes `_SEMANTIC.md` |
| `IN_PROGRESS` | Active human + agent work | Human or WORKING_ITEMS begins work |
| `CHECKING` | Under review | Human moves to review |
| `ISSUED` | Released | Human approves and issues |

### 3.3 Transition Rules

| Transition | Authorized Actor |
|------------|-----------------|
| `→ OPEN` | PREPARATION |
| `OPEN → INITIALIZED` | 4_DOCUMENTS |
| `INITIALIZED → SEMANTIC_READY` | CHIRALITY_FRAMEWORK |
| `INITIALIZED → IN_PROGRESS` | Human, WORKING_ITEMS (when semantic step is skipped) |
| `SEMANTIC_READY → IN_PROGRESS` | Human, WORKING_ITEMS |
| `IN_PROGRESS → CHECKING` | Human |
| `CHECKING → ISSUED` | Human |

**Invariant:** `_STATUS.md` is the authoritative lifecycle indicator. No other file determines deliverable state.

**Stage gates** (30/60/90/IFC, etc.) are human-managed milestones and are NOT lifecycle states. They are tracked separately in coordination records.

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

**Human-owned sections** (PREPARATION creates; human/ORCHESTRATOR maintains):
- Dependency Tracking Mode
- Declared Upstream
- Declared Downstream

**Agent-owned sections** (DEPENDENCIES agent populates):
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
|------|---------|
| `NOT_TRACKED` | Dependencies coordinated externally by humans |
| `DECLARED` | Human-declared upstream/downstream only; no agent extraction |
| `TRACKED` | Full agent extraction via DEPENDENCIES agent; `Dependencies.csv` present |

---

## 6. Dependencies.csv — Structured Dependency Register (v3.1)

### 6.1 Schema Version

The `RegisterSchemaVersion` column MUST be present in every row and set to `v3.1`.

### 6.2 Column Specification

#### Core Columns (MUST be present)

| # | Column | Type | Required | Description |
|---|--------|------|----------|-------------|
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
|--------|------|-------------|
| `EstimateImpactClass` | enum | `BLOCKING`, `ADVISORY`, `INFO`, `TBD` |
| `ConsumerHint` | enum | `TASK`, `TASK_ESTIMATING`, `AGGREGATION`, `RECONCILIATION`, `TBD` |

### 6.3 Canonical Enum Values

**DependencyClass:**
| Value | Meaning |
|-------|---------|
| `ANCHOR` | Tree edge: connects deliverable to a definition/traceability node |
| `EXECUTION` | DAG edge: information flow, prerequisite, handoff, or constraint |

**AnchorType:**
| Value | Meaning |
|-------|---------|
| `IMPLEMENTS_NODE` | Parent definition node (exactly one per deliverable) |
| `TRACES_TO_REQUIREMENT` | Requirement trace link (zero or more) |
| `NOT_APPLICABLE` | Used for EXECUTION rows |

**Direction:**
| Value | Meaning |
|-------|---------|
| `UPSTREAM` | This deliverable requires information FROM the target |
| `DOWNSTREAM` | This deliverable produces information FOR the target |

**DependencyType:**
| Value | Usage | Meaning |
|-------|-------|---------|
| `PREREQUISITE` | Preferred | Required input or approval before work can proceed |
| `INTERFACE` | Preferred | Explicit data/artifact exchange between deliverables |
| `HANDOVER` | Preferred | Output of one deliverable consumed as input to another |
| `CONSTRAINT` | Preferred | Explicit constraint or condition |
| `ENABLES` | Preferred | This deliverable enables downstream work |
| `OTHER` | Preferred | Dependency that does not fit other categories; used for ANCHOR rows |
| `COORDINATION` | Legacy | Do not emit in new extractions |
| `INFORMATION` | Legacy | Do not emit in new extractions |

**TargetType:**
| Value | Meaning |
|-------|---------|
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
|-------|---------|
| `EXPLICIT` | Dependency is explicitly stated in source text |
| `IMPLICIT` | Dependency is implied but not directly stated |

**SatisfactionStatus:**
| Value | Meaning |
|-------|---------|
| `TBD` | Not yet assessed |
| `PENDING` | Assessed but not yet satisfied |
| `IN_PROGRESS` | Actively being worked toward satisfaction |
| `SATISFIED` | Dependency has been fulfilled |
| `WAIVED` | Dependency waived by human decision |
| `NOT_APPLICABLE` | Dependency determined to be not applicable |

**Confidence:**
| Value | Meaning |
|-------|---------|
| `HIGH` | Strong evidence; explicit source reference |
| `MEDIUM` | Reasonable evidence; some interpretation required |
| `LOW` | Weak evidence; significant interpretation or assumption |

**Origin:**
| Value | Meaning |
|-------|---------|
| `DECLARED` | Human-declared dependency |
| `EXTRACTED` | Agent-extracted from source documents |

**Status:**
| Value | Meaning |
|-------|---------|
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

`EvidenceQuote` SHOULD be provided (max 30 words) for traceability.

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

- `Direction`: `INBOUND` normalizes to `UPSTREAM`; `OUTBOUND` normalizes to `DOWNSTREAM`
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
- `_REFERENCES.md` is created by PREPARATION and MAY be updated by human or ORCHESTRATOR.
- DEPENDENCIES agent reads `_REFERENCES.md` but MUST NOT modify it.

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
- Used by WORKING_ITEMS and TASK agents to record working context.
- Sections MAY be added as needed; the above are the minimum schema.
- `MEMORY.md` (without underscore prefix) MAY exist as a compatibility pointer containing: `See _MEMORY.md (canonical deliverable memory).`

---

## 9. Agent Instruction File Structure

All agent instruction files (`AGENT_*.md`) MUST follow the structure defined by `AGENT_HELPS_HUMANS.md`.

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
|---------|--------|---------|
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
|----------|-------------|---------|
| `AGENT_TYPE` | `TYPE 0`, `TYPE 1`, `TYPE 2` | Architect / Manager / Specialist |
| `AGENT_CLASS` | `PERSONA`, `TASK` | Interactive session vs. straight-through pipeline |
| `INTERACTION_SURFACE` | `chat`, `INIT-TASK`, `spawned`, `both` | How the agent is invoked |
| `WRITE_SCOPE` | `repo-wide`, `deliverable-local`, `tool-root-only`, `workspace-scaffold-only`, `repo-metadata-only`, `none` | What the agent is allowed to write |
| `BLOCKING` | `never`, `allowed` | Whether the agent may pause for human input |

### 9.6 Naming Convention

Use `AGENT_*` when referring to instruction files (e.g., `AGENT_CHANGE.md`). Use the role name (e.g., `CHANGE`) when referring to the agent itself.

### 9.7 Runtime Metadata Contract (Harness)

Harness runtime metadata parsing uses a split contract:

- **YAML frontmatter** (machine fields consumed by runtime where present):
  - `description`
  - `subagents`
  - `tools`
  - `model`
  - `max_turns`
  - `disallowed_tools`
  - `auto_approve_tools`
- **Canonical body header/table**:
  - `AGENT_TYPE: {0|1|2}` line in the instruction body
  - `AGENT_CLASS` value in the Agent Type table

Subagent registry safety rules:

- Delegated subagents MUST declare `AGENT_TYPE: 2` in the body header.
- `AGENT_CLASS: TASK` is preferred and validated as a warning-level rule (non-blocking).

Delegation governance rule (fail closed):

- When `CHIRALITY_ENABLE_SUBAGENTS === "true"` and a Type 1 persona is allowlisted for subagents, runtime injects subagents only if `opts.subagentGovernance` is present and valid:
  - `contextSealed === true`
  - `pipelineRunApproved === true`
  - `approvalRef` is a non-empty string
  - `approvedBy` is optional
- Missing/invalid governance metadata MUST block subagent injection while allowing the parent turn to continue normally.

### 9.8 Harness Turn Input Contract

Harness runtime accepts a turn options object (`opts`) on session boot and turn execution APIs.

- `POST /api/harness/turn` accepts `opts` and applies runtime option mapping.
- `POST /api/harness/session/boot` accepts `opts`; bootstrap policy remains authoritative for bootstrap-only constraints.
- `POST /api/harness/turn` also accepts optional `attachments` as an array of absolute filesystem path strings.

Attachment handling rules:

- The UI sends attachment paths only; server-side runtime classifies and reads files.
- Client-supplied attachment metadata (name/mime/type) is non-authoritative and MUST NOT be trusted for execution.
- A turn MAY omit text when attachments are present (`message.trim() === ""` with non-empty `attachments`).
- Resolver validation is server-side and enforces:
  - supported extensions (`.png`, `.jpg`, `.jpeg`, `.gif`, `.webp`, `.pdf`, `.txt`, `.md`, `.csv`)
  - `stats.isFile()` check — directories, symlinks, and special files are rejected
  - per-file size limit (10 MB)
  - total per-turn raw-byte budget (18 MB raw, which yields ~24 MB after base64 encoding)
- Partial attachment failure is non-fatal when the turn still has executable content:
  - if at least one attachment resolves (or user text exists), runtime proceeds and prepends a warning text block to the user content.
  - if all attachments fail and user text is empty, the request is rejected (`400`).

Prompt mode selection:

- No attachments: runtime uses SDK `query({ prompt: string })`.
- Attachments present: runtime builds multimodal content blocks and uses SDK `query({ prompt: AsyncIterable<SDKUserMessage> })`.

UI attachment state rules:

- UI stores `Attachment[]` (path, display name, client-classified mime/type) for preview purposes only; server reclassifies.
- On send failure, UI rolls back the optimistic user message and streaming placeholder, preserving the draft text and attachment selections for retry.
- Session rehydration validates attachment shape — malformed records are silently dropped; valid records are restored.

UI contract rules:

- UI MAY expose any subset of supported `opts` fields.
- Omitted fields MUST follow runtime fallback chains (persona defaults, global defaults, and runtime defaults).
- UI visibility of a field MUST NOT be interpreted as runtime authorization.

Key fallback examples:

- Model: `opts.model` → global model (instruction root) → runtime default.
- Tools: `opts.tools` → persona `tools` frontmatter → runtime preset.
- Max turns: `opts.maxTurns` → persona `max_turns` frontmatter → runtime default.

Governance visibility and enforcement:

- UI MAY present delegation governance fields for operator use.
- Runtime gate/seal logic remains authoritative.
- Supplying `opts.subagentGovernance` does not guarantee delegation; all runtime gates MUST still pass.

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

Snapshot folders are immutable after creation. Reruns create new snapshot folders.

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

A deliverable folder is **initialized** (state >= `INITIALIZED`) when it additionally contains:
- [ ] `Datasheet.md`
- [ ] `Specification.md`
- [ ] `Guidance.md`
- [ ] `Procedure.md`

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

---

## 14. UI Navigation and Selector Contract

This section defines deterministic frontend behavior for matrix launch routing and work mode selectors.

### 14.1 PORTAL Matrix Routing

Matrix rows map to destination views as follows:

| Matrix Row | Destination View |
|------------|------------------|
| `NORMATIVE` | `WORKBENCH` |
| `OPERATIVE` | `PIPELINE` |
| `EVALUATIVE` | `WORKBENCH` |

Matrix columns are shared labels: `GUIDING`, `APPLYING`, `JUDGING`, `REVIEWING`.

### 14.2 WORKBENCH Selector Scope

WORKBENCH persona selector is limited to the NORMATIVE + EVALUATIVE matrix agents:

- `HELP`
- `ORCHESTRATE`
- `WORKING_ITEMS`
- `AGGREGATE`
- `AGENTS`
- `DEPENDENCIES`
- `CHANGE`
- `RECONCILING`

OPERATIVE matrix entries MUST route to PIPELINE, not WORKBENCH.

### 14.3 PIPELINE Selector Schema

PIPELINE uses category-driven selectors:

1. `Category`: one of `DECOMP*`, `PREP*`, `TASK*`, `AUDIT*`
2. `Type`: category-specific static options (including disabled placeholders)
3. TASK-only split controls:
   - `Task Agent` (static task options)
   - `Scope Mode` (`DELIVERABLES` or `KNOWLEDGE_TYPES`)
   - `Scope` (dynamic list based on mode)
   - `Target Deliverable` (required when scope mode is `KNOWLEDGE_TYPES`)

### 14.4 Disabled Option Behavior

Requested but unsupported variants MUST be shown and disabled:

- Visible to operators (no silent omission)
- Non-selectable
- Labeled as coming soon (or equivalent disabled hint)

### 14.5 Stale Selection Reset Rules

Frontend state MUST clear invalid/stale selections when:

- Project root changes
- Deliverable scan results no longer include the selected deliverable key
- Knowledge decomposition marker is absent while knowledge-type scope is selected
- Knowledge type no longer resolves to available target deliverables

---

## 15. `/api/project/deliverables` Response Contract Extension

The deliverables endpoint continues to return `deliverables[]` and is extended with knowledge-scope metadata.

### 15.1 Response Shape

```json
{
  "deliverables": [
    {
      "id": "DEL-01-01",
      "name": "Deliverable Name",
      "pkg": "PKG-01_PackageLabel",
      "status": "open",
      "path": "/abs/path/to/deliverable"
    }
  ],
  "knowledgeDecomposition": {
    "enabled": false,
    "markerFile": null
  },
  "knowledgeTypes": [
    {
      "id": "datasheet",
      "label": "Datasheet",
      "matchingDeliverableKeys": ["PKG-01_PackageLabel::DEL-01-01"]
    }
  ]
}
```

### 15.2 `knowledgeDecomposition`

| Field | Type | Meaning |
|-------|------|---------|
| `enabled` | boolean | `true` only when a knowledge decomposition marker is found in decomposition docs |
| `markerFile` | string \| null | Path (or filename) of the first marker-bearing decomposition file; `null` when none found |

### 15.3 `knowledgeTypes[]`

Each element represents a canonical knowledge-type bucket observed across scanned deliverables.

| Field | Type | Meaning |
|-------|------|---------|
| `id` | string | Stable key for the knowledge type (e.g., `datasheet`) |
| `label` | string | Human-readable label (e.g., `Datasheet`) |
| `matchingDeliverableKeys` | string[] | Deliverable composite keys in `pkg::id` format where this type is present |

Knowledge types SHOULD be derived from canonical deliverable file classes:

- Datasheet
- Specification
- Guidance
- Procedure
- Dependencies
- References
- Context
- Status
- Semantic
- Memory

When `knowledgeDecomposition.enabled=false`, clients MUST NOT present knowledge-type scope as an active selection mode.

---

EOF
