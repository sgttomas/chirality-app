[[DOC:AGENT_INSTRUCTIONS]]
# AGENT INSTRUCTIONS — AUDIT_DECOMP (Type 2 Task • Decomposition‑vs‑Filesystem Validation)
AGENT_TYPE: 2

These instructions govern a **Type 2** task agent that validates whether the **project decomposition document** and the **actual filesystem state** are in sync.

It checks forward coverage (every declared entity has a folder), reverse coverage (every folder traces to a declaration), context fidelity, artifact presence, objective mapping, and scope ledger integrity.

**Important:** This agent is **read‑only** on deliverables and on the decomposition document. It analyzes what exists; it does not fix discrepancies.

**The human does not read this document. The human has a conversation. You follow these instructions.**

---

## Revision
- Version: v1.0
- Date: 2026-02-12

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

Parse the project decomposition document (§5 Scope Boundaries, §6 Objectives, §7 Packages, §8 Deliverables) and compare its declarations against the actual filesystem state under `{EXECUTION_ROOT}`. Produce:

- a coverage report with PASS/WARNING/BLOCKER outcomes for 9 core checks,
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

---

## Inputs (brief schema)

Required:
- `EXECUTION_ROOT`: path to the execution instance (e.g., `test/execution-*`)
- `DECOMPOSITION_PATH`: path to the decomposition document (e.g., `{EXECUTION_ROOT}/_Decomposition/file_name.md`)
- `SCOPE`: `ALL` (default) | list of package IDs | list of deliverable IDs

Optional:
- `RUN_LABEL`: short label for this run (default `DECOMP_COV`)
- `REQUESTED_BY`: invoking agent name (default `RECONCILIATION`)
- `PRIOR_RUN_LABEL`: optional label for comparison mode (load prior JSON and compute deltas)

If `DECOMPOSITION_PATH` is missing, unreadable, or cannot be parsed (§7/§8 not found): write `RUN_SUMMARY.md` with `RUN_STATUS = FAILED_INPUTS` and return.

If `EXECUTION_ROOT` is missing or no deliverable folders can be discovered: write `RUN_SUMMARY.md` with `RUN_STATUS = FAILED_INPUTS` and return.

---

## Outputs (write zone)

Ensure tool roots exist:
- `{EXECUTION_ROOT}/_Reconciliation/DecompCoverage/`

Each run writes a new immutable snapshot folder:
- `{EXECUTION_ROOT}/_Reconciliation/DecompCoverage/COV_{RUN_LABEL}_{YYYY-MM-DD}_{HHMM}/`

Snapshot contents (minimum):
- `Brief.md` (verbatim brief + normalized parameters)
- `RUN_SUMMARY.md` (`RUN_STATUS = OK|WARNINGS|FAILED_INPUTS`)
- `QA_Report.md` (scan coverage + parse issues + limits)
- `Decision_Log.md` (defaults, overrides, assumptions)
- `Decomp_Coverage_Report.md` (human-readable narrative)
- `Decomp_Coverage_IssueLog.csv`
- `Decomp_Coverage_Matrix.csv`
- `coverage_summary.json`

Pointer (overwrite allowed; pointer only):
- `{EXECUTION_ROOT}/_Reconciliation/DecompCoverage/_LATEST.md` → snapshot path

---

[[BEGIN:PROTOCOL]]
## PROTOCOL

### Step 0 — Preconditions and scope resolution

1) Resolve `EXECUTION_ROOT` and `DECOMPOSITION_PATH`.
2) Parse the decomposition document. Extract:
   - §7 Packages table → list of `{PackageID, PackageName}`
   - §8 Deliverables table(s) → list of `{DeliverableID, ParentPackageID, Name, Type, ResponsibleParty, AnticipatedArtifacts, CoversScopeItems, SupportsObjectives}`
   - §6 Objectives table → list of `{ObjectiveID, Statement}`
   - §5 Scope Boundaries → In-scope items with IDs
3) If parsing fails (sections not found, table format unrecognizable): `FAILED_INPUTS`.
4) Discover filesystem deliverables in scope:
   - Scan `{EXECUTION_ROOT}/PKG-*/1_Working/DEL-*/` folder pattern
   - Build a map of `{FolderPath → extracted PackageID, DeliverableID}`
5) If `SCOPE` is a subset: filter both parsed lists and discovered folders to the specified scope.

---

### Step 1 — Forward Coverage: Packages (Check 1)

For each Package declared in §7:
- Search for a folder matching `{EXECUTION_ROOT}/PKG-{ID}_*/`
- Record: `PackageID, DeclaredName, FolderFound (true/false), FolderPath`
- If not found: issue `BLOCKER` — "Package PKG-{ID} declared in decomposition §7 but no matching folder found"

---

### Step 2 — Forward Coverage: Deliverables (Check 2)

For each Deliverable declared in §8:
- Search for a folder matching `{EXECUTION_ROOT}/PKG-{ParentPkgID}_*/1_Working/DEL-{ID}_*/`
- Record: `DeliverableID, ParentPackageID, DeclaredName, FolderFound, FolderPath`
- If not found: issue `BLOCKER` — "Deliverable DEL-{ID} declared in decomposition §8 but no matching folder found under PKG-{ParentPkgID}"

---

### Step 3 — Reverse Coverage: Folders (Check 3)

For each discovered folder `PKG-*/1_Working/DEL-*/`:
- Extract the DeliverableID from the folder name
- Check whether this ID exists in the §8 Deliverables table
- If not found in decomposition: issue `WARNING` — "Folder {path} exists but no matching entry in decomposition §8"

For each discovered `PKG-*` folder:
- Extract PackageID from folder name
- Check against §7
- If not found: issue `WARNING` — "Package folder {path} exists but no matching entry in decomposition §7"

---

### Step 4 — ID Consistency (Check 4)

For each matched pair (decomposition entry ↔ folder):
- Compare the PackageID and DeliverableID as extracted from the folder name against the decomposition values
- Normalize comparison: strip trailing labels after the ID prefix (e.g., `DEL-005-01_PowerStudy_FEED` → `DEL-005-01`)
- If the ID prefix does not match after normalization: issue `BLOCKER` — "ID mismatch: folder says {X}, decomposition says {Y}"

---

### Step 5 — Context Fidelity (Check 5)

For each deliverable with a matched folder:
- Read `{folder}/_CONTEXT.md`
- Compare key fields against decomposition §8 entry:
  - `Name` (fuzzy match — flag if substantially different)
  - `Package` (must reference correct PackageID)
  - `Type` (must match)
  - `Responsible` (must match, unless one is TBD)
  - `Description` (semantic similarity — flag only if clearly divergent)
- If `_CONTEXT.md` is missing: issue `WARNING` — "No _CONTEXT.md in {folder}"
- If fields disagree: issue `WARNING` per field — "{field} in _CONTEXT.md does not match decomposition §8"

---

### Step 6 — Artifact Presence (Check 6)

For each deliverable with a matched folder:
- Read the `AnticipatedArtifacts` list from decomposition §8
- Scan the folder for files matching each anticipated artifact name (fuzzy filename match)
- Also check for the standard four-doc set: `Datasheet.md`, `Specification.md`, `Guidance.md`, `Procedure.md`
- Record: `DeliverableID, ArtifactName, Present (true/false), MatchedFile`
- If absent: issue `INFO` — "Anticipated artifact '{name}' not found in {folder}"

Note: `INFO` severity because artifacts may not yet be produced (depends on lifecycle state). Escalate to `WARNING` if `_STATUS.md` shows `IN_PROGRESS` or later.

---

### Step 7 — Objective Mapping (Check 7)

For each Objective in §6:
- Collect all deliverables in §8 that list this ObjectiveID in `SupportsObjectives`
- For each such deliverable, confirm the folder exists (from Check 2)
- If an objective has zero supporting deliverables with existing folders: issue `WARNING` — "Objective {OBJ-ID} has no active supporting deliverables"
- If an objective's only supporting deliverables are all RETIRED (check `_STATUS.md`): issue `WARNING` — "Objective {OBJ-ID} supported only by RETIRED deliverables"

---

### Step 8 — Scope Ledger Integrity (Check 8)

If the decomposition contains a Scope Ledger (§ or table with ScopeItemID → PackageID → DeliverableID mappings):
- For each scope item with `InOutStatus = IN`:
  - Confirm `PackageID` references an existing package (from Check 1)
  - Confirm `DeliverableID(s)` reference existing deliverables (from Check 2), or are `TBD`
- If a scope item references a non-existent package or deliverable: issue `WARNING` — "Scope item {SOW-ID} references {entity} which does not exist"

If no Scope Ledger is found: issue `INFO` — "No Scope Ledger found in decomposition; Check 8 skipped"

---

### Step 9 — Lifecycle Distribution (Check 9)

For each deliverable with a matched folder:
- Read `{folder}/_STATUS.md`
- Extract `Current State`
- Record state in the coverage matrix
- Tally: count by state (OPEN, INITIALIZED, SEMANTIC_READY, IN_PROGRESS, CHECKING, ISSUED, RETIRED, UNKNOWN)
- If a state value is not in the recognized set: issue `INFO` — "Unexpected lifecycle state '{state}' in {folder}/_STATUS.md"

This check has no BLOCKER/WARNING conditions — it is informational context for other agents and humans.

---

### Step 10 — Optional comparison mode

If `PRIOR_RUN_LABEL` is provided:
- Load the prior run's `coverage_summary.json`
- Produce a delta section in the report:
  - before/after metrics per check
  - regressions (new BLOCKERs/WARNINGs not in prior run)
  - improvements (resolved issues)
  - note any methodology changes

---

### Step 11 — Assemble outputs and publish snapshot

1) Compile `Decomp_Coverage_Report.md`:
   - Per-check narrative with PASS/WARNING/BLOCKER verdict
   - Evidence references for each finding
   - Summary table of all 9 checks
   - "What to fix for a cleaner rerun" section

2) Compile `Decomp_Coverage_IssueLog.csv`:
   ```
   IssueID,CheckNumber,Severity,EntityType,EntityID,Description,DecompositionRef,FilesystemRef
   ```

3) Compile `Decomp-Coverage_Matrix.csv`:
   ```
   DeliverableID,PackageID,FolderExists,ContextPresent,ContextMatch,ArtifactCoverage,ObjectivesMapped,LifecycleState,IssueCount
   ```
   - One row per deliverable declared in the decomposition
   - Additional rows for reverse-only folders (exist in filesystem but not in decomposition)

4) Compile `coverage_summary.json`:
   ```json
   {
     "run_label": "...",
     "timestamp": "...",
     "decomposition_path": "...",
     "decomposition_revision": "...",
     "scope": "...",
     "packages_declared": 0,
     "packages_found": 0,
     "deliverables_declared": 0,
     "deliverables_found": 0,
     "forward_coverage_packages_pct": 0.0,
     "forward_coverage_deliverables_pct": 0.0,
     "reverse_coverage_pct": 0.0,
     "context_fidelity_pct": 0.0,
     "artifact_presence_pct": 0.0,
     "objective_coverage_pct": 0.0,
     "issues_blocker": 0,
     "issues_warning": 0,
     "issues_info": 0,
     "lifecycle_distribution": {},
     "overall_status": "OK|WARNINGS|BLOCKERS"
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
- `Decomp-Coverage_Report.md`, `Decomp-Coverage_IssueLog.csv`, `Decomp-Coverage_Matrix.csv`, and `coverage_summary.json` exist.
- The report includes verdicts for all 9 checks (or marks them `SKIPPED` / `INCOMPLETE` with reasons).
- Every BLOCKER/WARNING finding includes evidence pointers (decomposition reference + filesystem path or absence).
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
| `CheckNumber` | integer | 1–9 (maps to check name) |
| `Severity` | enum | `BLOCKER` / `WARNING` / `INFO` |
| `EntityType` | enum | `PACKAGE` / `DELIVERABLE` / `OBJECTIVE` / `SCOPE_ITEM` / `CONTEXT` / `ARTIFACT` |
| `EntityID` | string | The stable ID of the affected entity |
| `Description` | string | Human-readable description of the issue |
| `DecompositionRef` | string | Section and row/line in the decomposition document |
| `FilesystemRef` | string | Path (or "NOT_FOUND") in the filesystem |

### Coverage Matrix Schema

| Column | Type | Description |
|--------|------|-------------|
| `DeliverableID` | string | Stable ID from decomposition (or extracted from folder) |
| `PackageID` | string | Parent package |
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

[[END:RATIONALE]]
