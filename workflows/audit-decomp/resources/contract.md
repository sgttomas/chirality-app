# audit-decomp — contract

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
- **Deterministic.** Deterministic inventories and explicit semantic judgments.
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
- `REQUESTED_BY`: invoking agent name (default `WORKING_ITEMS`)
- `PRIOR_RUN_LABEL`: optional label for comparison mode (load prior JSON and compute deltas)
- `EXPECTED_SOURCE_SNAPSHOT`: optional accepted upstream snapshot path that this audit run is expected to evaluate and cite in outputs
- `EXPECTED_HANDOFF_PHASE`: optional phase or handoff label so the run can state which closure boundary it supports

### Variant Entity Binding

This protocol uses **Package / Deliverable / Scope Ledger / Scope Item** terminology throughout. When `DECOMP_VARIANT` is not `PROJECT`, substitute terms per this table:

| Protocol term | WORKING_ITEMS (workflow: project-decomp) | WORKING_ITEMS (workflow: software-decomp) | WORKING_ITEMS (workflow: domain-decomp) |
|---------------|----------------|-----------------|---------------|
| Package | Package | Package | Category |
| Deliverable | Deliverable | Deliverable | Knowledge Type |
| Scope Item | Scope Item | Scope Item | Handbook Unit |
| Scope Ledger | Scope Ledger | Scope Ledger | Domain Ledger |
| Artifact | Artifact | Artifact | Knowledge Subject |

### Variant Section Binding

Section numbering differs between decomposition variant outputs. All protocol steps reference sections by **semantic name**. Resolve to the correct location as follows.

Bind by heading text, never by section number. Section numbers differ between
variants, differ between documents of the same variant, and drift as documents
are amended.

To resolve a semantic section, collect the document's `##` headings and
normalize each one: strip the `## ` marker, strip a leading section number of
the form `N.` or `NA.` (digits, optional letter suffix, period, trailing
space — e.g. `10A.`), trim, and case-fold. Normalize the target text the same
way. Then match in rank order, stopping at the first rank that yields a hit:
exact, then prefix, then substring. If a rank yields more than one hit, take
the earliest heading in the document and report the ambiguity. Only when no
rank yields any hit is the binding unresolved: stop and report it. Never
resolve by position.

| Semantic section | WORKING_ITEMS (workflow: project-decomp) heading | WORKING_ITEMS (workflow: software-decomp) heading | WORKING_ITEMS (workflow: domain-decomp) heading |
|------------------|------------------------|-------------------------|-----------------------|
| Ledger | `Scope Ledger` | `Scope Ledger` | `Domain Ledger` |
| Objectives | `Objectives` | `Objectives`, or the `ObjectiveID(s)` column of `Scope Ledger` where the variant embeds mapping in the ledger | `Objectives` |
| Partitions (Packages / Categories) | `Packages` | `Packages` | `Categories` |
| Production Units (Deliverables / Knowledge Types) | `Deliverables` | `Deliverables` | `Knowledge Types` |

When `DECOMP_VARIANT = SOFTWARE`, Check 7 (Objective Mapping) resolves objectives from the Scope Ledger `ObjectiveID(s)` column rather than a dedicated Objectives section; the ledger column is authoritative for Check 7 even where the document also carries a dedicated `Objectives` heading.

### Variant Folder Patterns

| Pattern | WORKING_ITEMS (workflow: project-decomp) | WORKING_ITEMS (workflow: software-decomp) | WORKING_ITEMS (workflow: domain-decomp) |
|---------|----------------|-----------------|---------------|
| Partition folder | `{ROOT}/PKG-{ID}_*/` | `{ROOT}/PKG-{ID}_*/` | `{ROOT}/CAT-{ID}_*/` |
| Production Unit folder | `PKG-{PID}_*/1_Working/DEL-{ID}_*/` | `PKG-{PID}_*/1_Working/DEL-{ID}_*/` | `CAT-{PID}_*/1_Working/KTY-{ID}_*/` |

### Variant ID Formats

| Entity | WORKING_ITEMS (workflow: project-decomp) | WORKING_ITEMS (workflow: software-decomp) | WORKING_ITEMS (workflow: domain-decomp) |
|--------|----------------|-----------------|---------------|
| Partition ID | `PKG-XXX` (3-digit) | `PKG-XX` (2-digit) | `CAT-###` |
| Production Unit ID | `DEL-XXX-YY_{desc}` | `DEL-XX-YY` | `KTY-CC-TT_{desc}` |
| ID normalization | Strip `_{desc}` suffix | No suffix; compare directly | Strip `_{desc}` suffix |

### Variant-Specific Behavior

**WORKING_ITEMS (workflow: software-decomp):**
- Step 5 (Context Fidelity): also compare `ContextEnvelope` field
- Step 7 (Objective Mapping): objectives extracted from Scope Ledger `ObjectiveID(s)` column, not a dedicated section

**WORKING_ITEMS (workflow: domain-decomp):**
- Step 5 (Context Fidelity): also compare `CanonicalSchema`, `IntendedUsers`, `WhenUsed` fields
- Step 6 (Artifact Presence): check against the Knowledge Type's anticipated Knowledge Subjects instead of the standard four-doc set
- Step 8 (Ledger Integrity): the ledger is named "Domain Ledger" and uses `UnitID` / `CategoryID` / `KnowledgeTypeID(s)` columns

If `DECOMPOSITION_PATH` is missing, unreadable, or cannot be parsed (Partitions/Production Units sections not found per Variant Section Binding): write `RUN_SUMMARY.md` with `RUN_STATUS = FAILED_INPUTS` and return.

If `EXECUTION_ROOT` is missing or no deliverable folders can be discovered: write `RUN_SUMMARY.md` with `RUN_STATUS = FAILED_INPUTS` and return.

---

## Outputs (write zone)

Bootstrap tool root: `tools/scaffolding/scaffold_tool_root.sh {EXECUTION_ROOT}/_Evaluation DecompCoverage`

Create snapshot folder: `tools/scaffolding/create_snapshot_folder.sh {EXECUTION_ROOT}/_Evaluation/DecompCoverage COV {RUN_LABEL}`

Snapshot contents (minimum):
- `Brief.md` (verbatim brief + normalized parameters)
- `RUN_SUMMARY.md` (`RUN_STATUS = OK|WARNINGS|FAILED_INPUTS`)
- `QA_Report.md` (scan coverage + parse issues + limits)
- `Decision_Log.md` (defaults, overrides, assumptions)
- `Decomp_Coverage_Report.md` (human-readable narrative)
- `Decomp_Coverage_IssueLog.csv`
- `Decomp_Coverage_Matrix.csv`
- `coverage_summary.json`

Update pointer: `tools/scaffolding/update_latest_pointer.sh {EXECUTION_ROOT}/_Evaluation/DecompCoverage {snapshot_folder_name}`

---

## Validity

A run is valid when:
- Outputs are written to a new immutable snapshot folder under `{EXECUTION_ROOT}/_Evaluation/DecompCoverage/`.
- `Decomp_Coverage_Report.md`, `Decomp_Coverage_IssueLog.csv`, `Decomp_Coverage_Matrix.csv`, and `coverage_summary.json` exist.
- The report includes verdicts for all 12 checks (or marks them `SKIPPED` / `INCOMPLETE` with reasons).
- Every BLOCKER/WARNING finding includes evidence pointers (decomposition reference + filesystem path or absence).
- If `EXPECTED_SOURCE_SNAPSHOT` was provided, the report and `coverage_summary.json` cite it explicitly so the audit snapshot can serve as derivative closure evidence.
- When `DECOMP_VARIANT = DOMAIN`, active derivative-package parity, active snapshot completeness, handoff-state consistency, and objective-evidence integrity are explicitly evaluated and surfaced.
- No file outside the write zone is modified.
- The decomposition document is not modified.
- No deliverable file is modified.

---

## Artifacts and schemas

### Tool-root layout

```
{EXECUTION_ROOT}/_Evaluation/DecompCoverage/
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
| `CheckNumber` | string | One of `1`–`9`, `9b`, `10`, `11` (maps to check name). Not an integer: check `9b` is a lettered sub-check. Any value outside this set is invalid |
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

---
