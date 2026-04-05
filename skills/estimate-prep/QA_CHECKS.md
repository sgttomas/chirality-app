# QA_CHECKS — estimate-prep

Invariants and quality gates. These apply to **both** phases unless explicitly marked `SCAFFOLD only` or `BOE only`.

## Universal invariants (both phases)

| # | Check | Validation |
|---|---|---|
| S1 | Write quarantine respected | No files created or modified outside `{EXECUTION_ROOT}/_EstimatePrep/` |
| S2 | Snapshot created | A new snapshot folder exists for the run, even if the run fails |
| S3 | Phase validated | `PHASE` is present and equals `SCAFFOLD` or `BOE`; invalid/missing = `RUN_STATUS=FAILED_INPUTS` |
| S3b | Single phase per run | Run did not span both phases; human gate between SCAFFOLD and BOE preserved |
| S10 | Status reporting | `QA_Report.md` declares `RUN_STATUS` = `OK` \| `WARNINGS` \| `FAILED_INPUTS` |
| S11 | Handoff artifacts | `Publish_Manifest.md` exists and references the run outputs |

## Required artifacts per phase

### SCAFFOLD — required files

| Artifact | Required |
|---|---|
| `Run_Context.md` | Yes |
| `QA_Report.md` | Yes |
| `Source_Index.md` | Yes |
| `Confidence_Summary.md` | Yes |
| `PriceSources/INDEX.md` | Yes |
| `Scaffold/BOE_Scaffold.md` | Yes |
| At least one pricing CSV appropriate to `RATE_SCOPE` | Yes |
| `Publish_Manifest.md` | Yes |
| `Override_Log.csv` | If `MODE=ENRICH` |
| `Conflicts.csv` | If conflicts detected |
| `Publish_Package/` | If `EXPORT_BUNDLE=MANIFEST_AND_PACKAGE` |

### BOE — required files

| Artifact | Required |
|---|---|
| `Run_Context.md` | Yes |
| `QA_Report.md` | Yes |
| `Source_Index.md` | Yes |
| `BASIS_OF_ESTIMATE.md` | Yes |
| `Tier_Analysis.md` | Yes |
| `Decision_Log.md` | Yes |
| `Assumptions_Log.md` | Yes |
| `Publish_Manifest.md` | Yes |
| `Conflicts.csv` | If dependency cycles or contradictions detected |
| `Publish_Package/` | If `EXPORT_BUNDLE=MANIFEST_AND_PACKAGE` |

## CSV schema integrity (SCAFFOLD only)

| # | Check | Requirement |
|---|---|---|
| S5a | Column names + order | Every generated CSV matches the canonical schema family (or the canonical file discovered via `AUTO_FROM_CANONICAL`) exactly — no invented columns |
| S5b | Key fields non-empty | No empty `ItemID`, `ParameterID`, `RoleID`, `TradeID`, or `DeliverableID` values |
| S5c | Recommended within range | For files with min/max/recommended columns, `RecommendedRate` (or `RecommendedPrice` / `RecommendedPercent`) MUST fall within `[Min, Max]` unless `Notes` provides explicit justification |
| S5d | No column additions | No columns may be added beyond what the canonical schema specifies |

## Provenance tracking (SCAFFOLD only; schema-family-aware)

| # | Check | Requirement |
|---|---|---|
| S6a | Rate/pricing files (Families 1-7) | Every row has non-empty `Basis` (canonical enum or ENRICH addition) and non-empty `Confidence` (`HIGH`, `MEDIUM`, `LOW`, `N/A`) |
| S6b | Project parameters (Family 8) | Every row has non-empty `Source` (canonical enum) and non-empty `Confidence` |
| S6c | Level of effort (Family 9) | Every row has non-empty `Basis`. **No `Confidence` column exists; do not require or generate one** |
| S6d | Parametric defaults | Parametric values carry `Confidence=MEDIUM` or `LOW` with `Basis=PARAMETRIC`, never `HIGH` |
| S6e | `HIGH` confidence discipline | `HIGH` confidence values are traceable to a vendor quote, human confirmation, or source document — not to parametric defaults |

### Canonical enum reference

| Context | Column | Canonical values | ENRICH additions |
|---|---|---|---|
| Rate/pricing files (Families 1-7) | `Basis` | `MARKET`, `PARAMETRIC`, `ALLOWANCE`, `N/A` | `QUOTE`, `HUMAN_PROVIDED`, `HUMAN_CONFIRMED` |
| Project parameters (Family 8) | `Source` | `ASSUMPTION`, `DESIGN_BASIS`, `CONFIRMED`, `DERIVED`, `PARAMETRIC` | `HUMAN_PROVIDED` |
| Level of effort (Family 9) | `Basis` | `PARAMETRIC` | `MARKET`, `HUMAN_PROVIDED` |

Values outside these enums require explicit justification in Notes or are treated as `FAILED_INPUTS`.

## Override logging (SCAFFOLD + MODE=ENRICH only)

| # | Check | Requirement |
|---|---|---|
| S7a | Override log exists | `Override_Log.csv` is present in the snapshot |
| S7b | Coverage complete | Every overridden value is recorded in `Override_Log.csv` |
| S7c | Columns present | `OverrideID`, `File`, `Key`, `Field`, `PriorValue`, `PriorConfidence`, `PriorBasis` (or `PriorSource`), `NewValue`, `NewConfidence`, `NewBasis` (or `NewSource`), `HumanSource`, `Notes` |
| S7d | No silent `HIGH` upgrades | Overrides that change a `HIGH`-confidence value require human-source documentation |

## BOE completeness (BOE only)

| # | Check | Requirement |
|---|---|---|
| S8a | Deliverable coverage | Every deliverable in the decomposition appears in the per-deliverable estimation plan |
| S8b | Cost ownership rules | Cost ownership rules exist for every package with multi-deliverable scope overlap |
| S8c | Run sequence produced | Canonical run sequence (tiers + within-tier parallelism + chains + gates) is present |
| S8d | Aggregation strategy | Rollups from deliverables to packages to project totals are defined |
| S8e | BOE sections present | If no canonical BOE format exists, the generated BOE includes all 10 required sections |

## Tier sequencing validity (BOE only)

| # | Check | Requirement |
|---|---|---|
| S9a | Tier assignment | Every deliverable is assigned a tier (T0, T1, ...) |
| S9b | Dependency consistency | Tier assignments are consistent with the dependency DAG |
| S9c | Cycle detection | Cycles are detected and reported in `QA_Report.md` AND `Conflicts.csv` |
| S9d | Dependencies unmodified | Dependency registers are read-only inputs; no modifications |

## Conflict surfacing (both phases)

- Conflicts MUST be surfaced in `Conflicts.csv`, not silently resolved.
- Conflict triggers:
  - Two or more human sources disagree for the same key
  - Canonical schema discovery fails / mismatches
  - Required inputs imply contradictory interpretations
  - Dependency cycles (BOE only)
- `Conflicts.csv` columns: `ConflictID`, `Key`, `Description`, `Contenders`, `ProposedAuthority` (optional PROPOSAL), `HumanRuling` (TBD until decided), `Notes`.
- `HumanRuling` remains `TBD` in every generated row — the skill does not fill this field.

## Human decision rights (both phases)

The skill MUST NOT unilaterally decide any of the following. If any arise, flag them and halt the relevant step:

- Accept or issue the BOE strategy / publish to canonical locations
- Resolve conflicts between disagreeing sources
- Approve overrides that would change a `HIGH`-confidence value
- Make scope boundary decisions (in/out; base vs option vs alternate)
- Execute any irreversible publication action (git commit/push; copy into `_PriceSources/`)

Any such decisions surfaced during a run are recorded as proposals in the relevant log (`Decision_Log.md`, `Conflicts.csv`) with `HumanRuling=TBD`.

## Failure reporting

| Status | Condition |
|---|---|
| `FAILED_INPUTS` | `PHASE` missing/invalid, required inputs missing, required inputs malformed, or single-run-spans-both-phases detected |
| `WARNINGS` | Run completed with surfaced conflicts, low-confidence items requiring attention, partial coverage, or schema discovery warnings |
| `OK` | Run completed with no warnings, no conflicts, and all required artifacts present |

`QA_Report.md` MUST declare exactly one `RUN_STATUS` value.

## Success case — SCAFFOLD

A clean SCAFFOLD run reports:

- `RUN_STATUS=OK`
- Snapshot folder path
- Pricing files generated (file count + row counts)
- Confidence distribution summary
- BOE scaffold file path
- `Publish_Manifest.md` present
- No conflicts, no overrides requiring human ruling (or explicit statement of none)

## Success case — BOE

A clean BOE run reports:

- `RUN_STATUS=OK`
- Snapshot folder path
- Deliverable count + tier distribution
- Cycle detection result (none, or listed)
- `BASIS_OF_ESTIMATE.md` path
- `Publish_Manifest.md` present
- Human modifications between scaffold snapshots logged in `Decision_Log.md`

## Evidence and logs required per run

| Log | Purpose |
|---|---|
| `Run_Context.md` | All resolved defaults, chosen paths, phase, mode |
| `Decision_Log.md` | Defaults applied, methods used, human modifications logged |
| `Assumptions_Log.md` | Explicit assumptions with IDs and impact-if-wrong |
| `Source_Index.md` | Source document index |
| `Confidence_Summary.md` (SCAFFOLD) | Per-file confidence distribution |
| `Override_Log.csv` (SCAFFOLD + ENRICH) | Every override with before/after |
| `Conflicts.csv` (when needed) | Unresolved conflicts with proposed authority (human ruling TBD) |
