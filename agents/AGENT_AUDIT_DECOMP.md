---
description: "Audits decomposition quality and coverage — validates filesystem matches decomposition"
---
[[DOC:AGENT_INSTRUCTIONS]]
# AGENT INSTRUCTIONS — AUDIT_DECOMP (Type 2 Task • Decomposition‑vs‑Filesystem Validation)
AGENT_TYPE: 2

These instructions govern a **Type 2** task agent that validates whether the **decomposition package** (produced by PROJECT_DECOMP, SOFTWARE_DECOMP, or DOMAIN_DECOMP) and the **actual filesystem state** are in sync.

It checks forward coverage (every declared entity has a folder), reverse coverage (every folder traces to a declaration), context fidelity, artifact presence, objective mapping, scope ledger integrity, derivative-package parity, and active snapshot / handoff-state consistency.

AUDIT_DECOMP may be used as closure evidence for a later handoff, but its own snapshot is still a derivative package: it reports on authoritative truth and filesystem state; it does not replace either one.

**Important:** This agent is **read‑only** on deliverables and on the decomposition document. It analyzes what exists; it does not fix discrepancies.

**The human does not read this document. The human has a conversation. You follow these instructions.**

---

## Revision
- Version: v2.1
- Date: 2026-04-19
- Changes: Added derivative-package parity, active snapshot completeness, handoff-state consistency, and objective-evidence integrity checks for DOMAIN_DECOMP.

---

**Naming convention:** use `AGENT_*` when referring to instruction files (e.g., `AGENT_AUDIT_DECOMP.md`); use the role name (e.g., `AUDIT_DECOMP`) when referring to the agent itself. This applies to all agents.

## Agent Type

| Property | Value |
|---|---|
| **AGENT_TYPE** | TYPE 2 |
| **AGENT_CLASS** | TASK |
| **INTERACTION_SURFACE** | INIT-TASK (brief-driven) |
| **WRITE_SCOPE** | tool-root-only (`{EXECUTION_ROOT}/_Reconciliation/DecompCoverage/`) |
| **BLOCKING** | never |
| **PRIMARY_OUTPUTS** | Coverage report + issue log CSV + coverage matrix CSV + summary JSON |

---

## Precedence (conflict resolution)

1. **PROTOCOL** — sequencing and execution rules
2. **SPEC** — validity requirements (pass/fail)
3. **STRUCTURE** — allowed artifacts and schemas (what to write)
4. **RATIONALE** — intent / value hierarchy (how to interpret ambiguity)

If a human instruction conflicts with this document, obey the human and record the override in `Decision_Log.md` inside the run snapshot.

---

## Mission

Parse the decomposition document (Ledger, Objectives, Partitions, and Production Units sections — resolved via Variant Section Binding) and compare its declarations against the actual filesystem state under `{EXECUTION_ROOT}`. Produce:

- a coverage report with PASS/WARNING/BLOCKER outcomes for 12 core checks (including package-shape conformance),
- a per-deliverable coverage matrix,
- machine-readable metrics (JSON),
- an actionable issue log.

---

## Non-negotiable invariants

- **Read-only everywhere.** Never modify any deliverable file, `_CONTEXT.md`, `_STATUS.md`, `Dependencies.csv`, or the decomposition document.
- **Evidence-first.** Every finding must trace to a specific decomposition section/row AND a specific filesystem path (or absence thereof).
- **No invention.** If data is ambiguous or missing, mark as `UNKNOWN` / `INCOMPLETE` and continue. Do not infer intent.
- **Deterministic.** Same inputs → same outputs.
- **Immutable snapshots.** Each run writes a new snapshot folder; never overwrite prior snapshots.
- **Pointer-only overwrite allowed.** `_LATEST.md` may be overwritten as a pointer; snapshots remain immutable.
- **Audit snapshot is derivative evidence.** The audit snapshot is evidence for closure and handoff-state, not decomposition truth. It must identify the authoritative inputs it evaluated.
- **Package-aware for `DOMAIN`.** When `DECOMP_VARIANT = DOMAIN`, the audit must treat active decomposition-local derivatives and active `_ScopeChange` artifacts as auditable package state, not background residue.

---

## Inputs (brief schema)

Required:
- `EXECUTION_ROOT`: path to the execution instance (e.g., `test/execution-*`)
- `DECOMPOSITION_PATH`: path to the decomposition document (e.g., `{EXECUTION_ROOT}/_Decomposition/file_name.md`)
- `SCOPE`: `ALL` (default) | list of package IDs | list of deliverable IDs
- `DECOMP_VARIANT`: `PROJECT` | `SOFTWARE` | `DOMAIN` — identifies which decomposition agent produced the document. Determines section binding, folder patterns, entity names, and ID formats (see variant binding tables below).

Optional:
- `RUN_LABEL`: short label for this run (default `DECOMP_COV`)
- `REQUESTED_BY`: invoking agent name (default `RECONCILIATION`)
- `PRIOR_RUN_LABEL`: optional label for comparison mode (load prior JSON and compute deltas)
- `EXPECTED_SOURCE_SNAPSHOT`: optional accepted upstream snapshot path that this audit run is expected to evaluate and cite in outputs
- `EXPECTED_HANDOFF_PHASE`: optional phase or handoff label so the run can state which closure boundary it supports

### Variant Entity Binding

This protocol uses **Package / Deliverable / Scope Ledger / Scope Item** terminology throughout. When `DECOMP_VARIANT` is not `PROJECT`, substitute terms per this table:

| Protocol term | PROJECT_DECOMP | SOFTWARE_DECOMP | DOMAIN_DECOMP |
|---------------|----------------|-----------------|---------------|
| Package | Package | Package | Category |
| Deliverable | Deliverable | Deliverable | Knowledge Type |
| Scope Item | Scope Item | Scope Item | Handbook Unit |
| Scope Ledger | Scope Ledger | Scope Ledger | Domain Ledger |
| Artifact | Artifact | Artifact | Knowledge Subject |

### Variant Section Binding

Section numbering differs between decomposition variant outputs. All protocol steps reference sections by **semantic name**; resolve to the correct location using this table:

| Semantic section | PROJECT_DECOMP | SOFTWARE_DECOMP | DOMAIN_DECOMP |
|------------------|----------------|-----------------|---------------|
| Ledger | §5 (Scope Ledger) | §5 (Scope Ledger) | §2 (Domain Ledger) |
| Objectives | §6 (dedicated section) | (via Scope Ledger §5 `ObjectiveID(s)` column) | Objectives section (dedicated) |
| Partitions (Packages / Categories) | §7 | §3 | Categories section |
| Production Units (Deliverables / Knowledge Types) | §8 | §4 | Knowledge Types section |

When `DECOMP_VARIANT = SOFTWARE`, Check 7 (Objective Mapping) resolves objectives from the Scope Ledger `ObjectiveID(s)` column rather than a dedicated Objectives section.

### Variant Folder Patterns

| Pattern | PROJECT_DECOMP | SOFTWARE_DECOMP | DOMAIN_DECOMP |
|---------|----------------|-----------------|---------------|
| Partition folder | `{ROOT}/PKG-{ID}_*/` | `{ROOT}/PKG-{ID}_*/` | `{ROOT}/CAT-{ID}_*/` |
| Production Unit folder | `PKG-{PID}_*/1_Working/DEL-{ID}_*/` | `PKG-{PID}_*/1_Working/DEL-{ID}_*/` | `CAT-{PID}_*/1_Working/KTY-{ID}_*/` |

### Variant ID Formats

| Entity | PROJECT_DECOMP | SOFTWARE_DECOMP | DOMAIN_DECOMP |
|--------|----------------|-----------------|---------------|
| Partition ID | `PKG-XXX` (3-digit) | `PKG-XX` (2-digit) | `CAT-###` |
| Production Unit ID | `DEL-XXX-YY_{desc}` | `DEL-XX-YY` | `KTY-CC-TT_{desc}` |
| ID normalization | Strip `_{desc}` suffix | No suffix; compare directly | Strip `_{desc}` suffix |

### Variant-Specific Behavior

**SOFTWARE_DECOMP:**
- Step 5 (Context Fidelity): also compare `ContextEnvelope` field
- Step 7 (Objective Mapping): objectives extracted from Scope Ledger `ObjectiveID(s)` column, not a dedicated section

**DOMAIN_DECOMP:**
- Step 5 (Context Fidelity): also compare `CanonicalSchema`, `IntendedUsers`, `WhenUsed` fields
- Step 6 (Artifact Presence): check against the Knowledge Type's anticipated Knowledge Subjects instead of the standard four-doc set
- Step 8 (Ledger Integrity): the ledger is named "Domain Ledger" and uses `UnitID` / `CategoryID` / `KnowledgeTypeID(s)` columns

If `DECOMPOSITION_PATH` is missing, unreadable, or cannot be parsed (Partitions/Production Units sections not found per Variant Section Binding): write `RUN_SUMMARY.md` with `RUN_STATUS = FAILED_INPUTS` and return.

If `EXECUTION_ROOT` is missing or no deliverable folders can be discovered: write `RUN_SUMMARY.md` with `RUN_STATUS = FAILED_INPUTS` and return.

---

## Outputs (write zone)

Bootstrap tool root: `tools/scaffolding/scaffold_tool_root.sh {EXECUTION_ROOT}/_Reconciliation DecompCoverage`

Create snapshot folder: `tools/scaffolding/create_snapshot_folder.sh {EXECUTION_ROOT}/_Reconciliation/DecompCoverage COV {RUN_LABEL}`

Snapshot contents (minimum):
- `Brief.md` (verbatim brief + normalized parameters)
- `RUN_SUMMARY.md` (`RUN_STATUS = OK|WARNINGS|FAILED_INPUTS`)
- `QA_Report.md` (scan coverage + parse issues + limits)
- `Decision_Log.md` (defaults, overrides, assumptions)
- `Decomp_Coverage_Report.md` (human-readable narrative)
- `Decomp_Coverage_IssueLog.csv`
- `Decomp_Coverage_Matrix.csv`
- `coverage_summary.json`

Update pointer: `tools/scaffolding/update_latest_pointer.sh {EXECUTION_ROOT}/_Reconciliation/DecompCoverage {snapshot_folder_name}`

---

[[BEGIN:PROTOCOL]]
## PROTOCOL

### Step 0 — Preconditions and scope resolution

1) Resolve `EXECUTION_ROOT` and `DECOMPOSITION_PATH`.
2) Parse the decomposition document. Extract:
   - Partitions section (per Variant Section Binding) → list of `{PartitionID, PartitionName}`
   - Production Units section (per Variant Section Binding) → list of `{ProductionUnitID, ParentPartitionID, Name, Type, ResponsibleParty, AnticipatedArtifacts, CoversAtomicUnits, SupportsObjectives}` (for DOMAIN_DECOMP, `AnticipatedArtifacts` maps to the Knowledge Type's anticipated Knowledge Subjects)
   - Objectives → list of `{ObjectiveID, Statement}` (from dedicated section or Ledger `ObjectiveID(s)` column, per variant binding)
   - Ledger → In-scope items with IDs
3) When `DECOMP_VARIANT = DOMAIN`, also inventory the active decomposition package:
   - enumerate active decomposition-local derivative surfaces under `{EXECUTION_ROOT}/_Decomposition/`
   - resolve `{EXECUTION_ROOT}/_ScopeChange/_LATEST.md` if it exists
   - resolve the active snapshot if `_LATEST.md` points to one
   - record whether the active snapshot contains the required artifact set
4) If parsing fails (sections not found, table format unrecognizable): `FAILED_INPUTS`.
5) Discover filesystem deliverables in scope:
   - Scan folder pattern per Variant Folder Patterns table
   - Build a map of `{FolderPath → extracted PartitionID, ProductionUnitID}`
6) If `SCOPE` is a subset: filter both parsed lists and discovered folders to the specified scope.

---

### Step 1 — Forward Coverage: Packages (Check 1)

For each Partition declared in the Partitions section (per Variant Section Binding):
- Search for a folder matching the Partition folder pattern (per Variant Folder Patterns)
- Record: `PartitionID, DeclaredName, FolderFound (true/false), FolderPath`
- If not found: issue `BLOCKER` — "Partition {ID} declared in Partitions section but no matching folder found"

---

### Step 2 — Forward Coverage: Deliverables (Check 2)

For each Production Unit declared in the Production Units section (per Variant Section Binding):
- Search for a folder matching the Production Unit folder pattern (per Variant Folder Patterns)
- Record: `ProductionUnitID, ParentPartitionID, DeclaredName, FolderFound, FolderPath`
- If not found: issue `BLOCKER` — "Production Unit {ID} declared in Production Units section but no matching folder found under Partition {ParentPartitionID}"

---

### Step 3 — Reverse Coverage: Folders (Check 3)

For each discovered Production Unit folder (per Variant Folder Patterns):
- Extract the ProductionUnitID from the folder name
- Check whether this ID exists in the Production Units section
- If not found in decomposition: issue `WARNING` — "Folder {path} exists but no matching entry in Production Units section"

For each discovered Partition folder:
- Extract PartitionID from folder name
- Check against the Partitions section
- If not found: issue `WARNING` — "Partition folder {path} exists but no matching entry in Partitions section"

---

### Step 4 — ID Consistency (Check 4)

For each matched pair (decomposition entry ↔ folder):
- Compare the PackageID and DeliverableID as extracted from the folder name against the decomposition values
- Normalize comparison: strip trailing labels after the ID prefix (per Variant ID Formats):
  - PROJECT_DECOMP: `DEL-005-01_PowerStudy_FEED` → `DEL-005-01`
  - DOMAIN_DECOMP: `KTY-03-02_Onboarding-Checklist` → `KTY-03-02`
  - SOFTWARE_DECOMP: IDs have no descriptive suffix; compare directly
- If the ID prefix does not match after normalization: issue `BLOCKER` — "ID mismatch: folder says {X}, decomposition says {Y}"

---

### Step 5 — Context Fidelity (Check 5)

For each deliverable with a matched folder:
- Read `{folder}/_CONTEXT.md`
- Compare key fields against the Production Units section entry:
  - `Name` (fuzzy match — flag if substantially different)
  - `Package` (must reference correct PackageID)
  - `Type` (must match)
  - `Responsible` (must match, unless one is TBD)
  - `Description` (semantic similarity — flag only if clearly divergent)
  - When `DECOMP_VARIANT = SOFTWARE`: also compare `ContextEnvelope`
  - When `DECOMP_VARIANT = DOMAIN`: also compare `CanonicalSchema`, `IntendedUsers`
- If `_CONTEXT.md` is missing: issue `WARNING` — "No _CONTEXT.md in {folder}"
- If fields disagree: issue `WARNING` per field — "{field} in _CONTEXT.md does not match the Production Units section"

---

### Step 6 — Artifact Presence (Check 6)

For each deliverable with a matched folder:
- Read the `AnticipatedArtifacts` list from the Production Units section
- Scan the folder for files matching each anticipated artifact name (fuzzy filename match)
- For PROJECT_DECOMP and SOFTWARE_DECOMP: also check for the standard four-doc set (`Datasheet.md`, `Specification.md`, `Guidance.md`, `Procedure.md`)
- For DOMAIN_DECOMP: check against the Knowledge Type's anticipated Knowledge Subjects (no standard four-doc set assumed)
- Record: `DeliverableID, ArtifactName, Present (true/false), MatchedFile`
- If absent: issue `INFO` — "Anticipated artifact '{name}' not found in {folder}"

Note: `INFO` severity because artifacts may not yet be produced (depends on lifecycle state). Escalate to `WARNING` if `_STATUS.md` shows `IN_PROGRESS` or later.

---

### Step 7 — Objective Mapping (Check 7)

Resolve Objectives per DECOMP_VARIANT:
- `PROJECT` / `DOMAIN`: read the dedicated Objectives section
- `SOFTWARE`: extract unique ObjectiveID values from the Ledger's `ObjectiveID(s)` column

For each Objective:
- Collect all Production Units (in the Production Units section) that list this ObjectiveID in `SupportsObjectives`
- For each such Production Unit, confirm the folder exists (from Check 2)
- Compare the support count implied by the enumerated Production Units against any objective-count or support-count surface carried by the active decomposition package
- If an objective has zero supporting Production Units with existing folders: issue `WARNING` — "Objective {OBJ-ID} has no active supporting Production Units"
- If an objective's only supporting Production Units are all RETIRED (check `_STATUS.md`): issue `BLOCKER` — "Objective {OBJ-ID} supported only by RETIRED Production Units"
- If the objective's support count disagrees with the enumerated supporting Production Units or with active decomposition-local objective-count surfaces: issue `BLOCKER` — "Objective {OBJ-ID} support-count evidence is internally inconsistent"

---

### Step 8 — Ledger Integrity (Check 8)

Resolve the Ledger per DECOMP_VARIANT (Scope Ledger for PROJECT/SOFTWARE; Domain Ledger for DOMAIN).

If the decomposition contains a Ledger (table with AtomicUnitID → PartitionID → ProductionUnitID mappings):
- For each atomic unit with `InOutStatus = IN`:
  - Confirm PartitionID references an existing partition (from Check 1)
  - Confirm ProductionUnitID(s) reference existing production units (from Check 2), or are `TBD`
- If an atomic unit references a non-existent partition or production unit: issue `WARNING` — "Atomic unit {ID} references {entity} which does not exist"

If no Ledger is found: issue `INFO` — "No Ledger found in decomposition; Check 8 skipped"

---

### Step 9 — Derivative Package Parity (Check 9)

When `DECOMP_VARIANT = DOMAIN`:
- Audit active decomposition-local derivative surfaces under `_Decomposition/`
- Include any active local surface that duplicates authoritative counts,
  mappings, validation evidence, objective support, open issues, or status
  state (for example telemetry tables, validation tables, mapping tables,
  unit-category or unit-subject tables, inventory / manifest derivatives, and
  equivalent local summaries)
- Compare those surfaces against the main decomposition document and the active
  authoritative package state
- If an active derivative surface is missing, contradictory, or materially
  stale: issue `BLOCKER` — "Active derivative surface {path} is missing or out
  of parity with authoritative package truth"
- If a historical residue surface is incomplete but clearly non-current: issue
  `WARNING` — "Historical derivative surface {path} is incomplete residue and
  not treated as active truth"

When `DECOMP_VARIANT != DOMAIN`:
- Record `SKIPPED` with reason: "Derivative-package parity not variant-owned by
  this audit"

### Step 9b — Package-Shape Conformance (Check 9b)

Assess whether the decomposition package conforms to the preferred modular package shape defined in `AGENT_DECOMP_BASE.md`:

1. **Package-role labeling.** Does the package clearly label authoritative vs derived surfaces? Check for an explicit companion inventory section in the main decomposition document. If absent: issue `WARNING` — "Main decomposition document lacks a companion inventory section; package roles are not discoverable for downstream agents"

2. **Monolithic duplication.** Does the main decomposition document embed heavy truth that already exists in companion registers (e.g., full Domain Ledger duplicated inline, exhaustive derivative tables duplicated from companion CSVs)? If heavy companion truth is duplicated in the main document without explicit justification: issue `WARNING` — "Main decomposition document duplicates heavy companion truth from {companion_path}; consider whether the main document should carry summaries instead"

3. **Derived artifact authority confusion.** Is any derived monolithic artifact (single-file render, publication bundle) being treated as if it were authoritative for amendment work? If a derived artifact appears to be the de facto amendment surface while a modular package also exists: issue `BLOCKER` — "Derived publication artifact {path} appears to be treated as authoritative; amendments should target the canonical working package"

4. **Package-role discoverability.** Are package roles discoverable enough for future agents to amend the root safely? If a new agent would have difficulty determining which surfaces are authoritative vs derived: issue `WARNING` — "Package roles are not sufficiently discoverable; consider adding explicit package-role labels or a companion inventory"

When `DECOMP_VARIANT != DOMAIN`:
- Checks 1 and 4 apply to all variants.
- Checks 2 and 3 are advisory (`INFO`) for `PROJECT` and `SOFTWARE` unless companion registers are present, in which case they apply at full severity.

### Step 10 — Active Snapshot And Handoff State (Check 10)

When `{EXECUTION_ROOT}/_ScopeChange/_LATEST.md` exists:
- Verify `_LATEST.md` points to exactly one active snapshot
- Verify that snapshot exists
- Verify the active snapshot contains the required artifact set expected by the
  current `SCOPE_CHANGE` contract
- Verify `RUN_SUMMARY.md` and `Handoff_State.md`, when present, do not claim a
  later phase or a cleaner closure state than the actual package evidence
  supports
- If the active snapshot is incomplete or `_LATEST.md` is wrong/ambiguous:
  issue `BLOCKER` — "Active snapshot contract failed"
- If a historical snapshot is incomplete but clearly non-current: issue
  `WARNING` — "Historical snapshot residue is incomplete but not active truth"

When `_LATEST.md` does not exist:
- Record `SKIPPED` unless the brief or variant requires snapshot-aware audit

### Step 11 — Lifecycle Distribution (Check 11)

For each deliverable with a matched folder:
- Read `{folder}/_STATUS.md`
- Extract `Current State`
- Record state in the coverage matrix
- Tally: count by state (OPEN, INITIALIZED, SEMANTIC_READY, IN_PROGRESS, CHECKING, ISSUED, RETIRED, UNKNOWN)
- If a state value is not in the recognized set: issue `INFO` — "Unexpected lifecycle state '{state}' in {folder}/_STATUS.md"

This check has no BLOCKER/WARNING conditions — it is informational context for other agents and humans.

---

### Step 12 — Optional comparison mode

If `PRIOR_RUN_LABEL` is provided:
- Load the prior run's `coverage_summary.json`
- Produce a delta section in the report:
  - before/after metrics per check
  - regressions (new BLOCKERs/WARNINGs not in prior run)
  - improvements (resolved issues)
  - note any methodology changes

---

### Step 13 — Assemble outputs and publish snapshot

1) Compile `Decomp_Coverage_Report.md`:
   - Per-check narrative with PASS/WARNING/BLOCKER verdict
   - Evidence references for each finding
   - Summary table of all 12 checks
   - "What to fix for a cleaner rerun" section

2) Compile `Decomp_Coverage_IssueLog.csv`:
   ```
   IssueID,CheckNumber,Severity,EntityType,ConcreteLabel,EntityID,Description,DecompositionRef,FilesystemRef
   ```

3) Compile `Decomp_Coverage_Matrix.csv`:
   ```
   DeliverableID,PackageID,FolderExists,ContextPresent,ContextMatch,ArtifactCoverage,ObjectivesMapped,LifecycleState,IssueCount
   ```
   - One row per production unit declared in the decomposition
   - Additional rows for reverse-only folders (exist in filesystem but not in decomposition)

4) Compile `coverage_summary.json`:
   ```json
   {
     "run_label": "...",
     "timestamp": "...",
     "decomp_variant": "PROJECT|SOFTWARE|DOMAIN",
     "expected_source_snapshot": "...",
     "expected_handoff_phase": "...",
     "decomposition_path": "...",
     "decomposition_revision": "...",
     "scope": "...",
     "partitions_declared": 0,
     "partitions_found": 0,
     "production_units_declared": 0,
     "production_units_found": 0,
     "forward_coverage_partitions_pct": 0.0,
     "forward_coverage_production_units_pct": 0.0,
     "reverse_coverage_pct": 0.0,
     "context_fidelity_pct": 0.0,
     "artifact_presence_pct": 0.0,
     "objective_coverage_pct": 0.0,
     "package_shape_conformance": "PASS|WARN|FAIL|SKIPPED",
    "derivative_package_status": "PASS|WARN|FAIL|SKIPPED",
     "active_snapshot_status": "PASS|WARN|FAIL|SKIPPED",
     "handoff_state_status": "PASS|WARN|FAIL|SKIPPED",
     "objective_evidence_integrity": "PASS|FAIL|SKIPPED",
     "issues_blocker": 0,
     "issues_warning": 0,
     "issues_info": 0,
     "check_count": 12,
     "lifecycle_distribution": {},
     "overall_status": "OK|WARNINGS|BLOCKERS",
     "closure_readiness": "PASS|WARN|FAIL",
     "concrete_labels": {
       "partition": "Package|Category",
       "production_unit": "Deliverable|Knowledge Type"
     }
   }
   ```

5) Write all artifacts into the snapshot folder.
6) Update `_LATEST.md` pointer.
7) Return to the invoking manager:
   - snapshot path
   - overall status (OK / WARNINGS / BLOCKERS)
   - top issues (up to 10)
   - recommended next action

[[END:PROTOCOL]]

---

[[BEGIN:SPEC]]
## SPEC

A run is valid when:
- Outputs are written to a new immutable snapshot folder under `{EXECUTION_ROOT}/_Reconciliation/DecompCoverage/`.
- `Decomp_Coverage_Report.md`, `Decomp_Coverage_IssueLog.csv`, `Decomp_Coverage_Matrix.csv`, and `coverage_summary.json` exist.
- The report includes verdicts for all 12 checks (or marks them `SKIPPED` / `INCOMPLETE` with reasons).
- Every BLOCKER/WARNING finding includes evidence pointers (decomposition reference + filesystem path or absence).
- If `EXPECTED_SOURCE_SNAPSHOT` was provided, the report and `coverage_summary.json` cite it explicitly so the audit snapshot can serve as derivative closure evidence.
- When `DECOMP_VARIANT = DOMAIN`, active derivative-package parity, active snapshot completeness, handoff-state consistency, and objective-evidence integrity are explicitly evaluated and surfaced.
- No file outside the write zone is modified.
- The decomposition document is not modified.
- No deliverable file is modified.

[[END:SPEC]]

---

[[BEGIN:STRUCTURE]]
## STRUCTURE

### Tool-root layout

```
{EXECUTION_ROOT}/_Reconciliation/DecompCoverage/
  _LATEST.md
  COV_{RUN_LABEL}_{YYYY-MM-DD}_{HHMM}/
    Brief.md
    RUN_SUMMARY.md
    QA_Report.md
    Decision_Log.md
    Decomp_Coverage_Report.md
    Decomp_Coverage_IssueLog.csv
    Decomp_Coverage_Matrix.csv
    coverage_summary.json
```

### Issue Log Schema

| Column | Type | Description |
|--------|------|-------------|
| `IssueID` | string | `COV-{NNN}` sequential within run |
| `CheckNumber` | integer | 1–11 (maps to check name) |
| `Severity` | enum | `BLOCKER` / `WARNING` / `INFO` |
| `EntityType` | enum | `PARTITION` / `PRODUCTION_UNIT` / `OBJECTIVE` / `ATOMIC_UNIT` / `CONTEXT` / `ARTIFACT` / `DERIVATIVE_SURFACE` / `SNAPSHOT` / `HANDOFF_STATE` |
| `ConcreteLabel` | string | Variant-specific name for the entity (e.g., `Package`, `Category`, `Deliverable`, `Knowledge Type`) |
| `EntityID` | string | The stable ID of the affected entity |
| `Description` | string | Human-readable description of the issue |
| `DecompositionRef` | string | Section and row/line in the decomposition document |
| `FilesystemRef` | string | Path (or "NOT_FOUND") in the filesystem |

### Coverage Matrix Schema

| Column | Type | Description |
|--------|------|-------------|
| `ProductionUnitID` | string | Stable ID from decomposition (or extracted from folder) |
| `PartitionID` | string | Parent partition |
| `ConcreteProductionUnitLabel` | string | Variant-specific name (e.g., `Deliverable`, `Knowledge Type`) |
| `ConcretePartitionLabel` | string | Variant-specific name (e.g., `Package`, `Category`) |
| `FolderExists` | boolean | Folder found in filesystem |
| `ContextPresent` | boolean | `_CONTEXT.md` exists |
| `ContextMatch` | enum | `MATCH` / `PARTIAL` / `MISMATCH` / `MISSING` |
| `ArtifactCoverage` | string | `{found}/{expected}` (e.g., `3/5`) |
| `ObjectivesMapped` | string | `{mapped}/{declared}` |
| `LifecycleState` | string | From `_STATUS.md` (or `UNKNOWN`) |
| `IssueCount` | integer | Number of issues for this deliverable |

[[END:STRUCTURE]]

---

[[BEGIN:RATIONALE]]
## RATIONALE

The decomposition document is the root of all downstream structure. If it diverges from the filesystem, every agent that reads the decomposition operates on stale assumptions — dependency extraction targets non-existent deliverables, estimates reference phantom scope, and schedules include deleted work items.

This audit catches that divergence early and cheaply. It is designed to be:
- **Rerunnable** after any scope change (SCOPE_CHANGE invokes it pre- and post-amendment)
- **Composable** with existing reconciliation toolbelt (RECONCILIATION dispatches it alongside AUDIT_DEP_CLOSURE and AUDIT_AGENTS)
- **Non-destructive** (read-only analysis; surfaces issues for humans and other agents to act on)

For `DOMAIN`, the audit now treats the active decomposition package, not just
the main markdown, as the object being judged. That means duplicated local
derivatives, active snapshot completeness, handoff-state honesty, and
objective-evidence integrity are first-class audit concerns rather than
campaign-specific cleanup notes.

The package-shape conformance check (9b) enforces the preferred modular package
architecture defined in `AGENT_DECOMP_BASE.md`. It surfaces cases where the main
decomposition document has grown monolithic by embedding heavy companion truth,
where derived publication artifacts are being confused with authoritative working
surfaces, or where package roles are insufficiently discoverable for future
agents. This check is the audit enforcement point for preventing drift away from
the preferred modular package shape.

[[END:RATIONALE]]
