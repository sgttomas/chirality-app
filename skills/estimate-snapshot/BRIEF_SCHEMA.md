# estimate-snapshot — Brief Schema

Use this skill with a generic TASK shell (no profile).

## Required fields

| Field | Value | Notes |
|---|---|---|
| `ScopePath` | `{EXECUTION_ROOT}` | Top-level execution root |
| `TaskSkill` | `estimate-snapshot` | Must match skill folder name |
| `AllowedWriteTargets` | `["{EXECUTION_ROOT}/_Estimates/"]` | Tool-root-only writes |
| `RuntimeOverrides.SCOPE` | Deliverable IDs, package IDs, or path glob | Non-empty |
| `RuntimeOverrides.BASIS_OF_ESTIMATE` | Enum value | `QUOTE`, `RATE_TABLE`, `HISTORICAL`, `PARAMETRIC`, or `ALLOWANCE` |
| `RuntimeOverrides.CURRENCY` | ISO code or project token | e.g., `USD`, `CAD` |
| `RuntimeOverrides.ESTIMATES_ROOT` | `{EXECUTION_ROOT}/_Estimates/` | Must already exist |

## Recommended fields

| Field | Default | Notes |
|---|---|---|
| `RuntimeOverrides.DECOMPOSITION_PATH` | auto-locate | Absolute path to decomposition markdown; auto-locates under `{EXECUTION_ROOT}/_Decomposition/` if absent; logs `MISSING_DECOMPOSITION` warning if not found |
| `RuntimeOverrides.DEPENDENCY_SOURCES` | `AUTO` | `AUTO` reads each in-scope deliverable's `Dependencies.csv`; or explicit paths |
| `RuntimeOverrides.PRICE_SOURCES` | none | List of local files/folders with basis evidence (quotes, rate tables, historical datasets, parametric models, allowance tables) |

## Optional fields

| Field | Default | Allowed values |
|---|---|---|
| `RuntimeOverrides.OUTPUT_LABEL` | `AUTO` | Short identifier used in snapshot naming |
| `RuntimeOverrides.UPDATE_LATEST_POINTER` | `FALSE` | `TRUE` or `FALSE` |
| `RuntimeOverrides.FALLBACK_POLICY` | `STRICT` | `STRICT`, `ALLOW_ALLOWANCE`, `ALLOW_PARAMETRIC` |
| `RuntimeOverrides.ALLOW_MIXED_METHODS` | `FALSE` | `TRUE` or `FALSE` |
| `RuntimeOverrides.ROUNDING` | `NONE` | `NONE`, `CENT`, `DOLLAR`, project-defined |
| `RuntimeOverrides.RUN_TIMESTAMP` | runtime-generated | ISO timestamp |

## TaskProfile

`NONE` — this skill runs in generic TASK shell mode without a profile.

## Example brief

```markdown
PURPOSE: Generate estimate snapshot for Package 02 deliverables (parametric model)
RequestedBy: ORCHESTRATOR
ScopePath: {EXECUTION_ROOT}
TaskSkill: estimate-snapshot

AllowedWriteTargets:
  - "{EXECUTION_ROOT}/_Estimates/"

RuntimeOverrides:
  SCOPE: DEL-02.01,DEL-02.02,DEL-02.03
  BASIS_OF_ESTIMATE: PARAMETRIC
  CURRENCY: USD
  ESTIMATES_ROOT: "{EXECUTION_ROOT}/_Estimates/"
  DECOMPOSITION_PATH: /abs/path/to/_Decomposition/Decomp_2026-03-15.md
  DEPENDENCY_SOURCES: AUTO
  PRICE_SOURCES:
    - /abs/path/to/models/parametric_cost_model_v2.csv
    - /abs/path/to/rate_tables/labor_rates_2026.csv
  OUTPUT_LABEL: PKG-02_Parametric
  UPDATE_LATEST_POINTER: FALSE
  FALLBACK_POLICY: STRICT
  ALLOW_MIXED_METHODS: FALSE
  ROUNDING: DOLLAR
```

## Read boundary

The skill reads only:

- `DECOMPOSITION_PATH` (when provided or auto-located)
- `{deliverable}/Dependencies.csv` for each in-scope deliverable (when `DEPENDENCY_SOURCES=AUTO`)
- Explicit paths in `DEPENDENCY_SOURCES`
- Explicit paths in `PRICE_SOURCES`
- Decomposition/deliverable metadata needed to resolve IDs

The skill must NOT fetch from the internet. Local inputs only.

## Write boundary

The skill writes only:

- `{ESTIMATES_ROOT}/EST_{OUTPUT_LABEL}_{YYYY-MM-DD}_{HHMM}/` (new immutable folder each run)
- `{ESTIMATES_ROOT}/_LATEST.md` pointer (only when `UPDATE_LATEST_POINTER=TRUE`)

`ESTIMATES_ROOT` must already exist. The skill does not create the tool root itself.

## BASIS_OF_ESTIMATE enum (validated at Step 0)

| Value | Meaning | Source type |
|---|---|---|
| `QUOTE` | Vendor-quoted prices | Explicit quote lines from vendor documents |
| `RATE_TABLE` | Rates from published tables | Labor/material/equipment rate tables |
| `HISTORICAL` | Prior cost data with normalization | Historical project datasets |
| `PARAMETRIC` | Approved parametric model | Cost model formulas + parameters |
| `ALLOWANCE` | Allowance tables/budgets | Allowance tables |

Invalid or missing values cause `RUN_STATUS=FAILED_INPUTS` (fail-fast at Step 0).

## Notes

- `OUTPUT_LABEL` should be short and stable across reruns (e.g., `PKG-02`, `DEL-001-01`) — the timestamp makes each snapshot unique.
- `UPDATE_LATEST_POINTER=TRUE` is only safe when the invoker has authorized pointer updates; the default is `FALSE`.
- `PRICE_SOURCES` are the only authoritative pricing inputs; dependencies are not pricing evidence.
- Do not pass `BOE.md` authoring as an expectation — the skill does not author a narrative BOE by default.
