# audit-decomp — method

## Method

### Step 0 — Preconditions and scope resolution

1) Resolve `EXECUTION_ROOT` and `DECOMPOSITION_PATH`.
2) Parse the decomposition document. Extract:
   - Partitions section (per Variant Section Binding) → list of `{PartitionID, PartitionName}`
   - Production Units section (per Variant Section Binding) → list of `{ProductionUnitID, ParentPartitionID, Name, Type, ResponsibleParty, AnticipatedArtifacts, CoversAtomicUnits, SupportsObjectives}` (for WORKING_ITEMS (workflow: domain-decomp), `AnticipatedArtifacts` maps to the Knowledge Type's anticipated Knowledge Subjects)
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
  - WORKING_ITEMS (workflow: project-decomp): `DEL-005-01_PowerStudy_FEED` → `DEL-005-01`
  - WORKING_ITEMS (workflow: domain-decomp): `KTY-03-02_Onboarding-Checklist` → `KTY-03-02`
  - WORKING_ITEMS (workflow: software-decomp): IDs have no descriptive suffix; compare directly
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
- For WORKING_ITEMS (workflow: project-decomp) and WORKING_ITEMS (workflow: software-decomp): resolve `SOW_V1`, transitional
  `LEGACY_FOUR_DOC`, authorized isolated `MIGRATION_DUAL`, or a fail-closed
  invalid/ambiguous state. Validate the selected contract; both formats
  without exact migration authority are ambiguous and nonconformant.
- For WORKING_ITEMS (workflow: domain-decomp): check against the Knowledge Type's anticipated Knowledge Subjects (no standard four-doc set assumed)
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

Assess whether the decomposition package conforms to the preferred modular package shape defined in `docs/DECOMPOSITION_STANDARD.md`:

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
  current `WORKING_ITEMS (workflow: scope-change)` contract
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
   ProductionUnitID,PartitionID,ConcreteProductionUnitLabel,ConcretePartitionLabel,FolderExists,ContextPresent,ContextMatch,ArtifactCoverage,ObjectivesMapped,LifecycleState,IssueCount
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
     "repository_topology": {
       "packages": 0,
       "deliverables": 0,
       "objectives": 0,
       "scope_items": 0,
       "ledger_rows": 0
     },
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
     "deliverables_without_objective_mapping": 0,
     "in_ledger_rows_without_objective_mapping": 0,
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

   **`repository_topology` (optional).** Whole-decomposition totals, independent
   of what this run audited: `packages`, `deliverables`, `objectives`,
   `scope_items`, and `ledger_rows` counted across the entire decomposition
   document. It is the denominator context for the scoped metrics beside it —
   `partitions_declared` and `production_units_declared` count only the audited
   `scope`, so a scoped run reports (for example) 3 partitions and 15 production
   units against a repository of 10 packages and 51 deliverables. Omit the
   object when the run does not measure whole-repository totals; never restate
   scoped counts in it.

   **`closure_readiness` is a three-way verdict**, not a lifecycle or handoff
   state. Emit exactly `PASS`, `WARN`, or `FAIL`. A phase name such as
   `READY_FOR_IMPLEMENTATION_HANDOFF` is not a valid value: readiness to hand
   off is a lifecycle judgement recorded by the invoking manager, and writing it
   here both leaves the verdict unstated and lets a run carrying warnings read
   as ready.

5) Write all artifacts into the snapshot folder.
6) Update `_LATEST.md` pointer.
7) Return to the invoking manager:
   - snapshot path
   - overall status (OK / WARNINGS / BLOCKERS)
   - top issues (up to 10)
   - recommended next action

---
