---
name: estimate-snapshot
description: Generate an immutable, provenance-first estimate snapshot for a bounded scope of deliverables and/or packages, writing quarantined artifacts under the estimating tool root. Use for automated estimate runs driven by a validated BASIS_OF_ESTIMATE enum and local pricing sources.
compatibility: Chirality TASK; invoked for estimate snapshot generation (tool-root-only writes under _Estimates/)
allowed-tools: python3 tools/validation/validate_enum.py:*, bash tools/scaffolding/create_snapshot_folder.sh:*, bash tools/scaffolding/update_latest_pointer.sh:*
metadata:
  chirality-skill-version: "1"
  chirality-task-profile: NONE
---

# SKILL — estimate-snapshot

## Purpose

Produce an immutable estimate snapshot under the estimating tool root for a bounded scope of deliverables and/or packages. Each run writes a NEW, timestamped snapshot folder with provenance-first line items, a WBS×CBS rollup matrix, QA reporting, and run context logs.

The skill does **not** author a narrative Basis of Estimate. Instead, it requires a validated `BASIS_OF_ESTIMATE` enum as an explicit input and uses that value to drive default behaviors, method tagging, and QA consistency checks.

## Suitable agent shells

- `TASK` in generic shell mode (no profile)

## Inputs

### Required

- `ScopePath` — `{EXECUTION_ROOT}`
- `TaskSkill` — `estimate-snapshot`
- `AllowedWriteTargets` — `["{EXECUTION_ROOT}/_Estimates/"]` (tool-root-only)
- `RuntimeOverrides.SCOPE` — deliverable IDs and/or package IDs to estimate (or path glob)
- `RuntimeOverrides.BASIS_OF_ESTIMATE` — one of: `QUOTE | RATE_TABLE | HISTORICAL | PARAMETRIC | ALLOWANCE`
- `RuntimeOverrides.CURRENCY` — ISO-like code (e.g., `USD`, `CAD`) or project-defined currency token
- `RuntimeOverrides.ESTIMATES_ROOT` — `{EXECUTION_ROOT}/_Estimates/` (must already exist)

### Recommended

- `RuntimeOverrides.DECOMPOSITION_PATH` — absolute path to the latest decomposition markdown. If absent, attempt to locate most recent under `{EXECUTION_ROOT}/_Decomposition/`. If still missing, log `[WARNING] MISSING_DECOMPOSITION` and proceed with degraded ID/path validation.
- `RuntimeOverrides.DEPENDENCY_SOURCES` — `AUTO` (default) or explicit paths to dependency registers/snapshots
- `RuntimeOverrides.PRICE_SOURCES` — list of local files/folders containing basis evidence (quotes, rate tables, historical datasets, parametric models, allowance tables)

### Optional

- `RuntimeOverrides.OUTPUT_LABEL` — short label for snapshot naming (default: `AUTO`)
- `RuntimeOverrides.UPDATE_LATEST_POINTER` — `FALSE` (default) | `TRUE`
- `RuntimeOverrides.FALLBACK_POLICY` — `STRICT` (default) | `ALLOW_ALLOWANCE` | `ALLOW_PARAMETRIC`
- `RuntimeOverrides.ALLOW_MIXED_METHODS` — `FALSE` (default) | `TRUE`
- `RuntimeOverrides.ROUNDING` — `NONE` (default) | `CENT` | `DOLLAR` | project-defined
- `RuntimeOverrides.RUN_TIMESTAMP` — optional ISO timestamp; else generated at runtime

## Runtime overrides

| Key | Meaning | Default | Allowed values |
|---|---|---|---|
| `SCOPE` | Deliverable IDs, package IDs, or path glob | **Required** | Non-empty |
| `BASIS_OF_ESTIMATE` | Validated estimate basis enum | **Required** | `QUOTE`, `RATE_TABLE`, `HISTORICAL`, `PARAMETRIC`, `ALLOWANCE` |
| `CURRENCY` | Currency code | **Required** | ISO code or project-defined token |
| `ESTIMATES_ROOT` | Tool root path | **Required** | Must already exist |
| `DECOMPOSITION_PATH` | Decomposition markdown path | auto-locate | Valid file path |
| `DEPENDENCY_SOURCES` | Dependency evidence sources | `AUTO` | `AUTO` or explicit paths |
| `PRICE_SOURCES` | Basis evidence sources | None | List of local paths |
| `OUTPUT_LABEL` | Snapshot naming label | `AUTO` | Short identifier |
| `UPDATE_LATEST_POINTER` | Update `_LATEST.md` pointer | `FALSE` | `TRUE` or `FALSE` |
| `FALLBACK_POLICY` | Method fallback policy | `STRICT` | `STRICT`, `ALLOW_ALLOWANCE`, `ALLOW_PARAMETRIC` |
| `ALLOW_MIXED_METHODS` | Permit mixed `Method` values in Detail.csv | `FALSE` | `TRUE` or `FALSE` |
| `ROUNDING` | Amount rounding | `NONE` | `NONE`, `CENT`, `DOLLAR`, project-defined |

## Read boundary

Reads are limited to:

- `DECOMPOSITION_PATH` (when provided or auto-located)
- `{deliverable}/Dependencies.csv` for each in-scope deliverable (when `DEPENDENCY_SOURCES=AUTO`)
- Explicit paths provided in `DEPENDENCY_SOURCES`
- Explicit paths provided in `PRICE_SOURCES` (quotes, rate tables, historical datasets, parametric models, allowance tables)
- Decomposition and deliverable metadata needed to resolve IDs

The skill must NOT fetch from the internet. Only local inputs.

## Write boundary

Writes are limited to the snapshot folder under `{ESTIMATES_ROOT}`:

- `{ESTIMATES_ROOT}/EST_{OUTPUT_LABEL}_{YYYY-MM-DD}_{HHMM}/` (new folder each run)
- Optionally `{ESTIMATES_ROOT}/_LATEST.md` pointer (only when `UPDATE_LATEST_POINTER=TRUE`)

No writes outside `ESTIMATES_ROOT`. No modification of project truth (deliverable content, lifecycle files, decomposition outputs, dependency registers).

## Tool usage

### Preferred tools

- `tools/validation/validate_enum.py` — validate `BASIS_OF_ESTIMATE` at Step 0 (halt with `FAILED_INPUTS` if invalid)
- `tools/scaffolding/create_snapshot_folder.sh` — create the immutable snapshot folder with canonical naming
- `tools/scaffolding/update_latest_pointer.sh` — update `_LATEST.md` pointer only when `UPDATE_LATEST_POINTER=TRUE`

### Disallowed behavior

- No writes outside `{ESTIMATES_ROOT}`
- No modification of any file in deliverable folders, decomposition outputs, dependency registers, or lifecycle files
- No overwriting an existing snapshot folder
- No internet fetching (only local `PRICE_SOURCES`)
- No treating prior snapshots under `_Estimates/` as pricing sources unless explicitly included in `PRICE_SOURCES`

## Method

### Step 0 — Resolve tool root + create snapshot folder

1. Resolve tool root to `{ESTIMATES_ROOT}` (or `{EXECUTION_ROOT}/_Estimates/`).
2. Validate the brief enum: `python3 tools/validation/validate_enum.py BASIS_OF_ESTIMATE {BASIS_OF_ESTIMATE}`. If invalid or missing, halt with `RUN_STATUS=FAILED_INPUTS`.
3. Create the immutable snapshot folder: `bash tools/scaffolding/create_snapshot_folder.sh {ESTIMATES_ROOT} EST {OUTPUT_LABEL}`.
4. If `UPDATE_LATEST_POINTER=TRUE`, run `bash tools/scaffolding/update_latest_pointer.sh {ESTIMATES_ROOT} {snapshot_folder_name}`. If `FALSE`, do not modify pointer files.

### Step 1 — Load decomposition (stable IDs + scope mapping)

1. Read `DECOMPOSITION_PATH` if provided or auto-locate under `{EXECUTION_ROOT}/_Decomposition/`.
2. Extract Package IDs, Deliverable IDs, labels, and optional hints (`CBSHint`, `EstimateMethodHint`, `StageHint`, `ContextEnvelope`) if present. Do not invent hints.
3. If decomposition is missing, record `[WARNING] MISSING_DECOMPOSITION` in QA and `Run_Context.md` and proceed best-effort.

### Step 2 — Enumerate work items from `SCOPE`

1. Expand `SCOPE` into a concrete deliverable list.
2. Produce `Scope_Resolved.csv` (or a `Run_Context.md` section) listing `DeliverableID`, `PackageID` (if known), `Path` (if known), `InScope=TRUE|FALSE`, and notes.

### Step 3 — Load dependency evidence (readiness + blockers)

1. If `DEPENDENCY_SOURCES=AUTO`, read each in-scope deliverable's `Dependencies.csv` if present.
2. Use dependency evidence to identify prerequisites and information gaps that block meaningful estimating. If `EstimateImpactClass` is present, use it as a hint only.
3. Emit `Blockers.md` (or `blocker_report.csv`) listing unresolved inputs by deliverable with evidence references.
4. Dependencies are NOT pricing evidence — they inform readiness only.

### Step 4 — Load pricing sources (basis evidence)

1. Index each entry in `PRICE_SOURCES` into `Source_Index.md` with source path, source type (quote, rate table, historical, parametric, allowance), parsing notes, and what it can/cannot support.
2. If `PRICE_SOURCES` is empty or unusable, do not guess prices — produce `TBD` amounts with `FAILED_INPUTS` or `WARNINGS` per SPEC.
3. Avoid recursive ingestion: do NOT treat prior `_Estimates/` snapshots as pricing sources unless explicitly listed in `PRICE_SOURCES`.

### Step 5 — Generate estimate detail (automated)

For each in-scope deliverable:

1. Propose line items (minimum one row per deliverable in `Detail.csv` unless blocked).
2. Assign `WBS_PackageID` and `WBS_DeliverableID` from decomposition when available; otherwise best-effort from scope resolution. Assign `CBS` from explicit `CBSHint`, else a deterministic rule documented in `Run_Context.md`, else `TBD`.
3. Price per `BASIS_OF_ESTIMATE` using only `PRICE_SOURCES` evidence:
   - `QUOTE` → `Method=QUOTE`
   - `RATE_TABLE` → `Method=RATE_TABLE`
   - `HISTORICAL` → `Method=HISTORICAL`
   - `PARAMETRIC` → `Method=PARAMETRIC`
   - `ALLOWANCE` → `Method=ALLOWANCE`
4. Enforce `ALLOW_MIXED_METHODS` and `FALLBACK_POLICY`. If fallback is not allowed and basis evidence is missing, set `Amount=TBD` and log a QA warning.
5. Populate provenance on every row:
   - `SourceRef` points to a file + section/row ID, OR to an entry in `Decision_Log.md` / `Assumptions_Log.md`.
   - If unknown, use `location TBD` and flag in QA.
6. Apply the allowance/parametric convention when applicable: `Qty=1`, `Unit=LS`, `UnitRate=Amount`.

### Step 6 — Produce rollups + matrices

1. Produce `WBS_CBS_Matrix.csv` with totals by `WBS_PackageID`, `WBS_DeliverableID`, `CBS`, `Currency`.
2. Produce `Summary.md` with: basis + run config (`BasisOfEstimate_Used` block), totals by package/deliverable/CBS, and key warnings + blockers.

### Step 7 — QA + logs

1. Produce `QA_Report.md` including:
   - schema validity (Detail.csv columns + enum validation)
   - coverage (deliverables covered, missing, blocked)
   - provenance completeness (% rows with non-TBD `SourceRef`)
   - basis-consistency checks (method mix vs `BASIS_OF_ESTIMATE`)
   - blocker counts (from dependency evidence when available)
   - "what to fix for a cleaner rerun"
   - a declared `RUN_STATUS`: `OK` | `WARNINGS` | `FAILED_INPUTS`
2. Produce logs:
   - `Decision_Log.md` — defaults applied, fallback uses, scope-resolution decisions
   - `Assumptions_Log.md` — explicit assumptions with IDs
   - `Risk_Register.md` — optional, only if risks are explicit or implied by missing inputs
   - `Change_Log.md` — what changed vs a referenced prior snapshot

## Outputs

### Required snapshot artifacts

- `Run_Context.md` (brief inputs + resolved defaults + chosen paths)
- `Summary.md`
- `QA_Report.md`
- `Source_Index.md`
- `Decision_Log.md`
- `Assumptions_Log.md`
- `WBS_CBS_Matrix.csv`

### Conditional/optional snapshot artifacts

- `Detail.csv` (recommended; required for full runs where pricing sources support meaningful totals)
- `Scope_Resolved.csv` (when scope expansion is non-trivial)
- `blocker_report.csv` or `Blockers.md` (when dependencies are used)
- `Risk_Register.md`
- `Change_Log.md`
- `Run_Brief.md` (verbatim brief text if provided by invoker; recommended for audit)

`BOE.md` is NOT required by default. If the invoker explicitly requests a narrative BOE, the skill MAY emit `BOE.md`, but it must be derived from run inputs and sources only (no invention).

### Canonical `Detail.csv` schema (when emitted)

Mandatory columns: `LineID`, `CBS`, `WBS_PackageID`, `WBS_DeliverableID`, `Description`, `Qty`, `Unit`, `UnitRate`, `Amount`, `Currency`, `Method`, `SourceRef`, `Confidence`, `Notes`.

- `Method` ∈ `{QUOTE, RATE_TABLE, HISTORICAL, ALLOWANCE, PARAMETRIC}`
- `Confidence` ∈ `{LOW, MEDIUM, HIGH}` (see QA_CHECKS for confidence rules)
- Allowance/parametric convention: `Qty=1`, `Unit=LS`, `UnitRate=Amount`

### `WBS_CBS_Matrix.csv` (minimum columns)

`WBS_PackageID`, `WBS_DeliverableID`, `CBS`, `Currency`, `Amount_Total`, `LineCount`, `ProvenanceCompletenessPct` (optional), `Notes` (optional)

### `Run_Context.md` (minimum fields)

`RunID`, `AsOf`, `Scope`, `ScopeResolvedSummary`, `BASIS_OF_ESTIMATE`, `CURRENCY`, `PRICE_SOURCES`, `DECOMPOSITION_PATH`, `DEPENDENCY_SOURCES`, `FALLBACK_POLICY`, `ALLOW_MIXED_METHODS`, `UPDATE_LATEST_POINTER`, `Rounding`, `Warnings`

## Non-negotiable constraints

- **BASIS_OF_ESTIMATE enum discipline.** Value must be exactly one of `QUOTE`, `RATE_TABLE`, `HISTORICAL`, `PARAMETRIC`, `ALLOWANCE`. Any other value is `FAILED_INPUTS` (fail-fast at Step 0).
- **Snapshot immutability.** Each run writes a NEW snapshot folder under `{ESTIMATES_ROOT}`. Never overwrite an existing snapshot folder.
- **Write quarantine (tool-root-only).** Write ONLY under `{ESTIMATES_ROOT}`. Never modify deliverable content, `_STATUS.md` or other lifecycle files, decomposition outputs, or dependency registers.
- **Provenance-first.** Every priced row in `Detail.csv` MUST carry a `SourceRef` (file + section/row ID, or an entry in `Decision_Log.md`/`Assumptions_Log.md`) OR explicitly `location TBD` with a QA warning. Every row also carries `Method` and `Confidence`.
- **No invention.** If a quantity, rate, currency, scope boundary, or dependency claim cannot be substantiated by provided sources, record `TBD` and surface it in QA. Do not guess.
- **Confidence rules.** Human-confirmed and vendor-quoted values earn `HIGH`. Parametric values are `MEDIUM` or `LOW`. Never assign `HIGH` to values derived from a parametric model or allowance table.
- **Dependencies are not pricing evidence.** Dependency registers inform readiness/blockers only. Unit rates must come from `PRICE_SOURCES`.
- **Avoid recursive ingestion.** Do not treat prior `_Estimates/` snapshots as pricing sources unless explicitly listed in `PRICE_SOURCES`.
- **Deterministic outputs.** Given identical inputs (scope + sources + brief), artifacts should be stable apart from timestamps and ordering normalizations.

## QA expectations

- `BASIS_OF_ESTIMATE` was validated by `validate_enum.py` before any writes occurred.
- A new snapshot folder exists (even if the run is blocked by missing inputs).
- Required artifacts exist: `Run_Context.md`, `Summary.md`, `QA_Report.md`, `Source_Index.md`.
- When `Detail.csv` exists: schema is intact, `Method` values valid, allowance/parametric convention respected.
- Every priced row has a `SourceRef` or `location TBD`. Provenance completeness percentage is reported in QA.
- Method mix is consistent with `BASIS_OF_ESTIMATE` unless `ALLOW_MIXED_METHODS=TRUE` or a `FALLBACK_POLICY` deviation is explicitly logged.
- `QA_Report.md` declares a `RUN_STATUS`: `OK` | `WARNINGS` | `FAILED_INPUTS`.
- No files outside `{ESTIMATES_ROOT}` were modified.
