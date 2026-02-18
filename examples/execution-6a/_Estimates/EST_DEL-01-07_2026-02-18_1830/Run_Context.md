# Run Context -- EST_DEL-01-07_2026-02-18_1830

## Run Identity

| Field | Value |
|---|---|
| RunID | EST_DEL-01-07_2026-02-18_1830 |
| AsOf | 2026-02-18T18:30:00-07:00 |
| Agent | ESTIMATING (Type 2) |

## Brief Inputs (as provided)

| Parameter | Value |
|---|---|
| SCOPE | DEL-01-07 |
| RUN_ROOT | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6a |
| ESTIMATES_ROOT | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6a/_Estimates/ |
| BASIS_OF_ESTIMATE | RATE_TABLE |
| CURRENCY | CAD |
| OUTPUT_LABEL | DEL-01-07 |
| UPDATE_LATEST_POINTER | FALSE |
| ALLOW_MIXED_METHODS | FALSE |
| FALLBACK_POLICY | STRICT |
| ROUNDING | DOLLAR |

## Resolved Paths

| Input | Resolved Path | Status |
|---|---|---|
| DECOMPOSITION_PATH | _Decomposition/Penhold_PSB_Project_Decomposition_FINAL_v1.0_PHASE7.md | FOUND |
| DEPENDENCY_SOURCES | AUTO -- read DEL-01-07/Dependencies.csv | FOUND (14 rows) |
| PRICE_SOURCES[1] | _PriceSources/Professional_Staff_Rates.csv | FOUND (31 roles) |
| PRICE_SOURCES[2] | _PriceSources/Level_of_Effort.csv | FOUND (18 rows; 3 rows for DEL-01-07) |
| PRICE_SOURCES[3] | _PriceSources/Assumed_Project_Parameters.csv | FOUND (29 parameters) |

## Scope Resolution Summary

| Metric | Value |
|---|---|
| Deliverables in SCOPE | 1 (DEL-01-07) |
| Deliverables resolved | 1 |
| Deliverables priced | 1 |
| Deliverables blocked | 0 |
| Deliverables skipped | 0 |

## CBS Mapping Rule

CBS codes are assigned based on a deterministic mapping from Role Category in Professional_Staff_Rates.csv:

| Role Category | CBS Code | Description |
|---|---|---|
| Construction | CBS-0107-CX | Commissioning and closeout labor (construction-phase roles) |
| Management | CBS-0107-MGT | Management and coordination labor |
| Administrative | CBS-0107-ADM | Administrative and document control labor |

This rule is specific to DEL-01-07 which covers commissioning coordination, closeout administration, and warranty management under PKG-001.

## Cost Ownership Note (CRITICAL)

DEL-01-07 covers OVERALL commissioning coordination and closeout administration ONLY. System-specific commissioning labor (mechanical balancing, electrical testing, etc.) is carried in the respective PKG-002 discipline deliverables and is NOT included here. All line items in this estimate reflect project-level Cx coordination, training delivery, as-built/O&M assembly, deficiency management, and warranty administration.

## Warnings

- None.
