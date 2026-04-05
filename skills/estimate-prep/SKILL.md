---
name: estimate-prep
description: Generates estimation input package (pricing library, LOE, project parameters, BOE) via two-phase run with PHASE=SCAFFOLD|BOE modes and a human gate between invocations.
compatibility: Chirality TASK; two-phase invocation pattern (human gate BETWEEN runs, not inside); writes to tool root _EstimatePrep/
metadata:
  chirality-skill-version: "1"
  chirality-task-profile: NONE
---

# SKILL — estimate-prep

## Purpose

Generate the complete input package consumed by ESTIMATING agents: pricing libraries, effort matrices, project parameter assumptions, and the Basis of Estimate (BOE).

This skill runs in two phases, invoked separately with a human gate between:

1. **SCAFFOLD** — generates a parametric pricing baseline + a BOE scaffold for human review.
2. **BOE** — consumes the approved scaffold + dependency evidence to produce the full `BASIS_OF_ESTIMATE.md` with tier sequencing, cost ownership rules, and aggregation strategy.

Each invocation runs exactly ONE phase, selected by the `PHASE` brief parameter. The human gate is external: a human reviews SCAFFOLD output, then re-invokes the skill with `PHASE=BOE`.

**Non-goal:** this skill MUST NOT compute or publish project totals, bid prices, or line-item estimates. It prepares inputs; ESTIMATING produces estimates.

## Suitable agent shells

- `TASK` (generic shell mode, no profile)

## Phase parameter — single-run discipline

The `PHASE` parameter determines which pipeline executes. A single invocation runs exactly one phase:

| PHASE | Input expectation | Primary output |
|---|---|---|
| `SCAFFOLD` | Decomposition + source documents + project context (+ optional `HUMAN_PRICING` if `MODE=ENRICH`) | Pricing library CSVs + `PriceSources/INDEX.md` + `Scaffold/BOE_Scaffold.md` |
| `BOE` | Approved `SCAFFOLD_PATH` + dependency evidence | Full `BASIS_OF_ESTIMATE.md` + `Tier_Analysis.md` |

**Critical invariant:** a single run MUST NOT span both phases — the human gate between them is a non-negotiable decision point. If a brief requests both phases in one run, halt with `FAILED_INPUTS`.

## Inputs

### Common (both phases)

Required:
- `EXECUTION_ROOT` — root of the current execution/workspace
- `PHASE` — `SCAFFOLD` | `BOE` (validated enum; invalid = `FAILED_INPUTS`)
- `DECOMPOSITION_PATH` — path to the latest decomposition markdown (PROJECT_DECOMP or SOFTWARE_DECOMP)
- `SOURCE_DOCUMENTS` — path(s) to source documents (RFP, addenda, specs, reference reports)
- `CURRENCY` — ISO-like code (e.g., `USD`, `CAD`)
- `PROJECT_CONTEXT` — structured block (`Location`, `BaseYear`, `ProjectType`, `ProcurementModel`; `EstimatedValue` optional; `AdditionalContext` optional)

Optional:
- `OUTPUT_LABEL` — short label for snapshot naming (default `AUTO`)
- `SECONDARY_SOURCES` — path(s) to secondary reference documents
- `CANONICAL_PRICESOURCES_ROOT` — path to canonical pricing library (e.g., `{EXECUTION_ROOT}/_PriceSources/`) used for schema discovery and/or as ENRICH input
- `SCHEMA_MODE` — `AUTO_FROM_CANONICAL` (default) | `DEFAULT_COMPAT`
- `EXPORT_BUNDLE` — `MANIFEST_ONLY` (default) | `MANIFEST_AND_PACKAGE`

### SCAFFOLD-specific

- `MODE` — `BOOTSTRAP` (default) | `ENRICH`
- `PRIOR_SNAPSHOT` — required if `MODE=ENRICH` (or use `CANONICAL_PRICESOURCES_ROOT`)
- `HUMAN_PRICING` — path(s) to human-provided pricing (quotes, rate tables, historical data, vendor proposals)
- `RATE_SCOPE` — `PRODUCTION_ONLY` (default) | `PRODUCTION_AND_CONSTRUCTION`
- `DISCIPLINE_HINTS` — override/supplement discipline detection from decomposition

### BOE-specific

Required:
- `SCAFFOLD_PATH` — path to approved SCAFFOLD snapshot (may have been modified by human after Phase SCAFFOLD)

Optional:
- `DEPENDENCY_SOURCES` — `AUTO` (default; reads per-deliverable `Dependencies.csv`) or explicit path(s) to dependency registers
- `EVALUATION_CRITERIA` — path to or structured block of evaluation criteria with point allocations
- `AGGREGATION_HINTS` — human-specified aggregation preferences

All resolved defaults and chosen paths MUST be recorded in the snapshot `Run_Context.md`.

## Runtime overrides

| Key | Meaning | Default | Allowed values |
|---|---|---|---|
| `PHASE` | Which pipeline to run | **Required** | `SCAFFOLD`, `BOE` |
| `MODE` | SCAFFOLD only: baseline vs enrichment | `BOOTSTRAP` | `BOOTSTRAP`, `ENRICH` |
| `RATE_SCOPE` | SCAFFOLD only: which rate files to generate | `PRODUCTION_ONLY` | `PRODUCTION_ONLY`, `PRODUCTION_AND_CONSTRUCTION` |
| `SCHEMA_MODE` | Whether to auto-match canonical file headers | `AUTO_FROM_CANONICAL` | `AUTO_FROM_CANONICAL`, `DEFAULT_COMPAT` |
| `EXPORT_BUNDLE` | Manifest-only vs manifest + copy-ready package | `MANIFEST_ONLY` | `MANIFEST_ONLY`, `MANIFEST_AND_PACKAGE` |
| `DEPENDENCY_SOURCES` | BOE only: dependency source policy | `AUTO` | `AUTO` or explicit path(s) |
| `OUTPUT_LABEL` | Label for snapshot folder naming | `AUTO` | free-form short token |

## Tool usage

- The `allowed-tools` frontmatter field is intentionally omitted. The skill dispatches several utility scripts under `tools/` (enum validation, snapshot scaffolding, INDEX generation) but their invocation is guided operationally, not enforced through the TASK-consumed allowed-tools contract.
- Preferred utility scripts (invoked by the agent during the run when available):
  - `tools/validation/validate_enum.py` — validates `PHASE` input.
  - `tools/scaffolding/scaffold_tool_root.sh` — creates `_EstimatePrep/` tool root.
  - `tools/scaffolding/create_snapshot_folder.sh` — creates immutable snapshot folder.
  - `tools/reporting/generate_index_md.sh` — generates file inventory portion of `INDEX.md`.
- Reasoning + file-write operations generate the content (CSVs, scaffold, BOE) based on the canonical schemas in the Schema Annex.

Disallowed behavior:
- No writes outside `{EXECUTION_ROOT}/_EstimatePrep/`.
- No overwriting prior snapshots.
- No modification of `_PriceSources/`, `_Estimates/`, deliverable folders, decomposition outputs, or dependency registers.
- No recursive ingestion of prior `_EstimatePrep/` outputs unless explicitly provided as `PRIOR_SNAPSHOT` / `SCAFFOLD_PATH`.

## Phase SCAFFOLD — method

1. **Resolve tool root + create snapshot folder.** Validate `PHASE` enum; bootstrap `_EstimatePrep/`; create `EPREP_SCAFFOLD_{LABEL}_{DATE}_{TIME}/`.
2. **Load decomposition.** Extract Package IDs, Deliverable IDs, scope items, disciplines, owner roles, variant hints.
3. **Load source documents.** Extract project name, location, owner, timeline, submission requirements, scope boundaries, referenced standards, constraints. Record `TBD` for items not found.
4. **Determine canonical schemas.** If `SCHEMA_MODE=AUTO_FROM_CANONICAL` and `CANONICAL_PRICESOURCES_ROOT` has a matching file, use its header exactly; otherwise use the Schema Annex (see `SCHEMA_ANNEX.md` for the 9 schema families).
5. **Generate `Professional_Staff_Rates.csv`** (Family 4). Default `Confidence=MEDIUM`, `Basis=PARAMETRIC`. ENRICH mode overlays human rates and logs each override.
6. **Generate `Level_of_Effort.csv`** (Family 9). Default `Basis=PARAMETRIC`. No `Confidence` column — provenance is `Basis` alone.
7. **Generate `Assumed_Project_Parameters.csv`** (Family 8). Uses `Source` column (not `Basis`); canonical enum: `ASSUMPTION`, `DESIGN_BASIS`, `CONFIRMED`, `DERIVED`, `PARAMETRIC`.
8. **Generate additional rate tables (conditional).** If `RATE_SCOPE=PRODUCTION_AND_CONSTRUCTION`, generate all applicable Family 1-7 files matching exact canonical schemas.
9. **Generate `PriceSources/INDEX.md`** with the 7 required sections: header block, data quality statement (HIGH/MEDIUM/LOW definitions), file inventory, PS-ID to file mapping, ESTIMATING run configuration (DEL-to-PKG mapping + per-package `PRICE_SOURCES` list + usage guidance), open issues, gaps. Full section contract: see `INDEX_MD_CONTRACT.md`.
10. **Generate `Scaffold/BOE_Scaffold.md`.** Per-deliverable table (DEL-ID, name, package, default basis, fallback policy, mixed-method flag, substance, cost drivers, roles), package cost ownership hints, SOW multi-mapping warnings. Marked `DRAFT — requires human review`.
11. **QA + handoff artifacts.** Produce `Confidence_Summary.md`, `QA_Report.md` with `RUN_STATUS`, `Decision_Log.md`, `Assumptions_Log.md`, `Source_Index.md`, `Override_Log.csv` (ENRICH only), `Conflicts.csv` (when needed), `Publish_Manifest.md` (always).

## Phase BOE — method

1. **Resolve tool root + create snapshot folder.** Create `EPREP_BOE_{LABEL}_{DATE}_{TIME}/`.
2. **Load approved scaffold.** Read `SCAFFOLD_PATH`; diff against original scaffold if identifiable; log human modifications in `Decision_Log.md`.
3. **Load decomposition + dependencies.** Read `DEPENDENCY_SOURCES` (or `AUTO` for per-deliverable `Dependencies.csv`); build dependency DAG; detect cycles.
4. **Derive tier sequencing.** Assign tiers via topological layering (T0, T1, ...); identify sequential chains and parallelization opportunities; output `Tier_Analysis.md`.
5. **Generate per-deliverable estimation plan.** Tier assignment, basis/fallback/mixed-method from approved scaffold, substance and cost drivers, required price sources; package-level cost ownership rules.
6. **Generate dependency-informed run sequence.** Tiers in order + within-tier parallelism + sequential chains + gates.
7. **Generate aggregation strategy.** Rollups: deliverables to packages to project totals; add evaluation-weight views if `EVALUATION_CRITERIA` provided.
8. **Generate missing/weak PRICE_SOURCES register.** Identify and prioritize low-confidence items impacting the plan.
9. **Compile assumptions and constraints log.** Merge scaffold assumptions + BOE derivations with IDs and impact-if-wrong.
10. **Compile full `BASIS_OF_ESTIMATE.md`.** Follow canonical BOE structure if one exists; otherwise use the 10-section set: Purpose, Project Context, Estimation Scope, Estimation Strategy, Per-Deliverable Plan, Dependency-Informed Run Sequence, Missing/Weak PRICE_SOURCES, Aggregation Strategy, Assumptions Log, Document Control. Full section contract + handoff artifact contracts: see `BOE_STRUCTURE.md`.
11. **QA + handoff artifacts.** `QA_Report.md` with `RUN_STATUS`, `Decision_Log.md`, `Assumptions_Log.md`, `Source_Index.md`, `Conflicts.csv` (if cycles or contradictions), `Publish_Manifest.md` (always).

## Outputs

### SCAFFOLD snapshot

```
{EXECUTION_ROOT}/_EstimatePrep/EPREP_SCAFFOLD_{LABEL}_{DATE}_{TIME}/
  Run_Context.md
  PriceSources/
    [pricing library CSVs per RATE_SCOPE]
    INDEX.md
  Scaffold/
    BOE_Scaffold.md
    Package_Analysis.md
  Confidence_Summary.md
  QA_Report.md
  Decision_Log.md
  Assumptions_Log.md
  Source_Index.md
  Override_Log.csv          (ENRICH mode only)
  Conflicts.csv             (when needed)
  Publish_Manifest.md
  Publish_Package/          (optional; if EXPORT_BUNDLE=MANIFEST_AND_PACKAGE)
```

### BOE snapshot

```
{EXECUTION_ROOT}/_EstimatePrep/EPREP_BOE_{LABEL}_{DATE}_{TIME}/
  Run_Context.md
  BASIS_OF_ESTIMATE.md
  Tier_Analysis.md
  QA_Report.md
  Decision_Log.md
  Assumptions_Log.md
  Source_Index.md
  Conflicts.csv             (when needed)
  Publish_Manifest.md
  Publish_Package/          (optional)
```

## Non-negotiable constraints

- **Write quarantine.** Write ONLY under `{EXECUTION_ROOT}/_EstimatePrep/`. Never modify `_PriceSources/`, `_Estimates/`, deliverable folders, decomposition outputs, or dependency registers. Publishing to canonical locations is a separate, human-approved step handled by the invoker.
- **Snapshots are immutable.** Each run writes a new snapshot folder; never overwrite prior snapshots.
- **Phase separation.** SCAFFOLD and BOE are distinct invocations. A single run MUST NOT span both phases — the human gate between them is a non-negotiable decision point.
- **Provenance tracking is mandatory.** Every generated value carries provenance appropriate to its schema family: `Basis` + `Confidence` for Families 1-7; `Source` + `Confidence` for Family 8; `Basis` alone (no `Confidence`) for Family 9. Do not add columns that do not exist in the canonical schema for a given file.
- **Parametric defaults are not human confirmation.** Parametric values MUST be labeled `PARAMETRIC` with `MEDIUM` or `LOW` confidence, never `HIGH`. Only human-confirmed, vendor-quoted, or directly source-document-derived values earn `HIGH`.
- **No silent overrides.** When ENRICH mode overlays human data on a baseline, every override MUST be logged in `Override_Log.csv` (what changed, from what, to what, confidence change).
- **Conflicts are surfaced.** If two sources disagree or schema mismatches exist, produce `Conflicts.csv`; do not silently pick a winner.
- **Dependencies are read-only inputs.** Dependency registers inform tier sequencing in Phase BOE but are never modified by this skill.
- **No recursive ingestion.** Do not treat prior `_EstimatePrep/` outputs as "market evidence" unless explicitly provided as `PRIOR_SNAPSHOT` / `SCAFFOLD_PATH`.
- **CSV schema integrity.** Every generated CSV MUST match the exact column names and order specified by its schema family (or by the canonical file discovered via `AUTO_FROM_CANONICAL`). No invented columns.

## Human decision rights (must remain human)

This skill may propose, but MUST NOT decide:

- Accepting / issuing the BOE strategy and publishing it to canonical locations.
- Rulings on conflicts (two quotes disagree, scope overlaps, contradictory dependency assertions).
- Approving any override that would change a `HIGH`-confidence value.
- Scope boundary decisions (in/out; base vs option vs alternate).
- Any irreversible publication action (git commit/push; copy into `_PriceSources/`).

Human rulings SHOULD be recorded in the scaffold/BOE artifacts (or in a separate decision log maintained by the invoker).

## QA expectations

See `QA_CHECKS.md` for the full invariant + quality gate set. Summary:

- `RUN_STATUS` declared in `QA_Report.md` (`OK` | `WARNINGS` | `FAILED_INPUTS`).
- Snapshot folder created for every run (including failures).
- No writes outside `_EstimatePrep/`.
- CSV schemas match the canonical Schema Annex exactly.
- Provenance complete per schema family.
- `Publish_Manifest.md` exists and references the run outputs.
- Phase-specific required artifacts present (see `QA_CHECKS.md`).

## Companion documents

This skill's detailed contracts live in adjacent companion files. Consult these when implementing:

- **`SCHEMA_ANNEX.md`** — 9 canonical CSV schema families covering 18 files in `_PriceSources/`; `Basis`/`Source`/`Confidence` enum references; `Override_Log.csv` and `Conflicts.csv` schemas. Hardened against the on-disk canonical library as of 2026-02-18.
- **`BOE_STRUCTURE.md`** — `BOE_Scaffold.md` contract (Phase SCAFFOLD), `BASIS_OF_ESTIMATE.md` 10-section contract (Phase BOE), `Run_Context.md` minimum fields, `Publish_Manifest.md` handoff contract.
- **`INDEX_MD_CONTRACT.md`** — 7-section `PriceSources/INDEX.md` contract including the ESTIMATING run configuration block.
