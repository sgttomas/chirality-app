# BRIEF_SCHEMA — estimate-prep

This skill runs in exactly ONE phase per invocation, selected by the `PHASE` brief parameter. The human gate is external: a human reviews `SCAFFOLD` output, then re-invokes with `PHASE=BOE`.

## PHASE parameter (required, both phases)

| Value | Meaning |
|---|---|
| `SCAFFOLD` | Generate parametric pricing baseline + BOE scaffold for human review |
| `BOE` | Consume approved scaffold + dependency evidence; produce full `BASIS_OF_ESTIMATE.md` |

Any other value produces `RUN_STATUS=FAILED_INPUTS`. A single run MUST NOT span both phases.

## Common required fields (both phases)

| Field | Type / values | Notes |
|---|---|---|
| `TaskSkill` | `estimate-prep` | Must match skill folder name |
| `PHASE` | `SCAFFOLD` \| `BOE` | Validated enum |
| `EXECUTION_ROOT` | Absolute path | Root of current execution/workspace |
| `DECOMPOSITION_PATH` | Absolute path | Latest decomposition markdown (PROJECT_DECOMP or SOFTWARE_DECOMP) |
| `SOURCE_DOCUMENTS` | Path or list of paths | RFP, addenda, specs, reference reports |
| `CURRENCY` | ISO-like code | e.g., `USD`, `CAD` |
| `PROJECT_CONTEXT` | Structured block | See block schema below |

### `PROJECT_CONTEXT` block

| Sub-field | Required | Example |
|---|---|---|
| `Location` | Yes | `Alberta, Canada — Penhold/Red Deer` |
| `BaseYear` | Yes | `2024` |
| `ProjectType` | Yes | `Municipal Public Services Building` |
| `ProcurementModel` | Yes | `Design-Build`, `Design-Bid-Build`, `CM at Risk` |
| `EstimatedValue` | No | `$12M-$15M CAD` |
| `AdditionalContext` | No | `LEED target`, `phased construction`, `occupied renovation` |

## Common optional fields (both phases)

| Field | Default | Allowed values |
|---|---|---|
| `OUTPUT_LABEL` | `AUTO` | Short label for snapshot folder naming |
| `SECONDARY_SOURCES` | — | Path(s) to secondary reference documents |
| `CANONICAL_PRICESOURCES_ROOT` | — | Path to existing canonical pricing library (e.g., `{EXECUTION_ROOT}/_PriceSources/`) |
| `SCHEMA_MODE` | `AUTO_FROM_CANONICAL` | `AUTO_FROM_CANONICAL`, `DEFAULT_COMPAT` |
| `EXPORT_BUNDLE` | `MANIFEST_ONLY` | `MANIFEST_ONLY`, `MANIFEST_AND_PACKAGE` |

## PHASE=SCAFFOLD — additional fields

### Optional (SCAFFOLD)

| Field | Default | Notes |
|---|---|---|
| `MODE` | `BOOTSTRAP` | `BOOTSTRAP` or `ENRICH` |
| `PRIOR_SNAPSHOT` | — | **Required if `MODE=ENRICH`** (unless `CANONICAL_PRICESOURCES_ROOT` is provided instead) |
| `HUMAN_PRICING` | — | Path(s) to human-provided pricing: quotes, rate tables, historical data, vendor proposals (CSV, markdown, PDF, structured text) |
| `RATE_SCOPE` | `PRODUCTION_ONLY` | `PRODUCTION_ONLY` or `PRODUCTION_AND_CONSTRUCTION` |
| `DISCIPLINE_HINTS` | — | Override or supplement discipline detection from decomposition |

## PHASE=BOE — additional fields

### Required (BOE)

| Field | Notes |
|---|---|
| `SCAFFOLD_PATH` | Path to approved SCAFFOLD snapshot (may have been modified by human after Phase SCAFFOLD) |

### Optional (BOE)

| Field | Default | Notes |
|---|---|---|
| `DEPENDENCY_SOURCES` | `AUTO` | `AUTO` (reads per-deliverable `Dependencies.csv`) or explicit path(s) |
| `EVALUATION_CRITERIA` | — | Path to or structured block of evaluation criteria with point allocations |
| `AGGREGATION_HINTS` | — | Human-specified aggregation preferences |

## Write boundary (both phases)

- Write target: `{EXECUTION_ROOT}/_EstimatePrep/` and nothing outside it.
- Each run creates a new immutable snapshot folder:
  - SCAFFOLD: `EPREP_SCAFFOLD_{LABEL}_{DATE}_{TIME}/`
  - BOE: `EPREP_BOE_{LABEL}_{DATE}_{TIME}/`

The brief SHOULD declare:

```yaml
AllowedWriteTargets:
  - "{EXECUTION_ROOT}/_EstimatePrep/"
```

## Example brief — PHASE=SCAFFOLD (BOOTSTRAP)

```markdown
PURPOSE: Generate parametric pricing baseline + BOE scaffold for Penhold MSB proposal
RequestedBy: ORCHESTRATOR
ScopePath: {EXECUTION_ROOT}
TaskSkill: estimate-prep

AllowedWriteTargets:
  - "{EXECUTION_ROOT}/_EstimatePrep/"

RuntimeOverrides:
  PHASE: SCAFFOLD
  MODE: BOOTSTRAP
  EXECUTION_ROOT: /abs/path/to/Penhold_MSB_Proposal
  DECOMPOSITION_PATH: /abs/path/to/Penhold_MSB_Proposal/_Decomposition/LATEST.md
  SOURCE_DOCUMENTS:
    - /abs/path/to/RFP.pdf
    - /abs/path/to/Addendum_01.pdf
  CURRENCY: CAD
  PROJECT_CONTEXT:
    Location: "Alberta, Canada — Penhold/Red Deer"
    BaseYear: 2024
    ProjectType: "Municipal Public Services Building"
    ProcurementModel: "Design-Build"
    EstimatedValue: "$12M-$15M CAD"
  RATE_SCOPE: PRODUCTION_AND_CONSTRUCTION
  SCHEMA_MODE: AUTO_FROM_CANONICAL
  CANONICAL_PRICESOURCES_ROOT: "{EXECUTION_ROOT}/_PriceSources/"
  EXPORT_BUNDLE: MANIFEST_ONLY
  OUTPUT_LABEL: "Penhold_MSB"
```

## Example brief — PHASE=SCAFFOLD (ENRICH)

```markdown
PURPOSE: Enrich SCAFFOLD snapshot with vendor quotes received since last run
RequestedBy: ESTIMATING_LEAD
TaskSkill: estimate-prep

AllowedWriteTargets:
  - "{EXECUTION_ROOT}/_EstimatePrep/"

RuntimeOverrides:
  PHASE: SCAFFOLD
  MODE: ENRICH
  EXECUTION_ROOT: /abs/path/to/Penhold_MSB_Proposal
  PRIOR_SNAPSHOT: "{EXECUTION_ROOT}/_EstimatePrep/EPREP_SCAFFOLD_Penhold_MSB_2024-03-15_0930/"
  DECOMPOSITION_PATH: /abs/path/to/Penhold_MSB_Proposal/_Decomposition/LATEST.md
  SOURCE_DOCUMENTS:
    - /abs/path/to/RFP.pdf
  HUMAN_PRICING:
    - /abs/path/to/quotes/mechanical_quote_acme.pdf
    - /abs/path/to/quotes/electrical_rates_q1_2024.csv
  CURRENCY: CAD
  PROJECT_CONTEXT:
    Location: "Alberta, Canada — Penhold/Red Deer"
    BaseYear: 2024
    ProjectType: "Municipal Public Services Building"
    ProcurementModel: "Design-Build"
  RATE_SCOPE: PRODUCTION_AND_CONSTRUCTION
  OUTPUT_LABEL: "Penhold_MSB_v2"
```

## Example brief — PHASE=BOE

```markdown
PURPOSE: Generate full BASIS_OF_ESTIMATE.md from approved SCAFFOLD snapshot
RequestedBy: ESTIMATING_LEAD
TaskSkill: estimate-prep

AllowedWriteTargets:
  - "{EXECUTION_ROOT}/_EstimatePrep/"

RuntimeOverrides:
  PHASE: BOE
  EXECUTION_ROOT: /abs/path/to/Penhold_MSB_Proposal
  SCAFFOLD_PATH: "{EXECUTION_ROOT}/_EstimatePrep/EPREP_SCAFFOLD_Penhold_MSB_v2_2024-03-22_1430/"
  DECOMPOSITION_PATH: /abs/path/to/Penhold_MSB_Proposal/_Decomposition/LATEST.md
  SOURCE_DOCUMENTS:
    - /abs/path/to/RFP.pdf
  CURRENCY: CAD
  PROJECT_CONTEXT:
    Location: "Alberta, Canada — Penhold/Red Deer"
    BaseYear: 2024
    ProjectType: "Municipal Public Services Building"
    ProcurementModel: "Design-Build"
  DEPENDENCY_SOURCES: AUTO
  EVALUATION_CRITERIA: /abs/path/to/RFP_Section5_Evaluation.md
  EXPORT_BUNDLE: MANIFEST_AND_PACKAGE
  OUTPUT_LABEL: "Penhold_MSB_BOE_v1"
```

## Notes

- `SCHEMA_MODE=AUTO_FROM_CANONICAL` + `CANONICAL_PRICESOURCES_ROOT` produces output CSVs whose headers match the canonical library exactly. Prefer this mode when a canonical `_PriceSources/` library exists.
- `EXPORT_BUNDLE=MANIFEST_AND_PACKAGE` writes an additional `Publish_Package/` subfolder inside the snapshot — this is still inside the write quarantine; human publication to canonical locations remains a separate approved step.
- All resolved defaults and chosen paths are recorded in the snapshot `Run_Context.md`.
- `PROJECT_CONTEXT` can be inlined in the brief (as shown) or provided as a path to a structured file — consult the invoker's brief conventions.
