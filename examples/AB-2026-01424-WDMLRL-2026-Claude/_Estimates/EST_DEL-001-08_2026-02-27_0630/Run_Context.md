# Run Context — EST_DEL-001-08_2026-02-27_0630

| Field | Value |
|---|---|
| **RunID** | EST_DEL-001-08_2026-02-27_0630 |
| **AsOf** | 2026-02-27T06:30:00-07:00 |
| **Scope** | DEL-001-08 |
| **ScopeResolvedSummary** | 1 deliverable (Finish Schedule), 1 package (PKG-001 Architectural Design) |
| **BASIS_OF_ESTIMATE** | PARAMETRIC |
| **CURRENCY** | CAD |
| **PRICE_SOURCES** | Professional_Staff_Rates.csv, Level_of_Effort.csv, Assumed_Project_Parameters.csv, Professional_Design_Fees.csv, Parametric_Building_Rates.csv |
| **DECOMPOSITION_PATH** | _Decomposition/WDMLRL_Decomposition_Claude.md |
| **FALLBACK_POLICY** | ALLOW_PARAMETRIC |
| **ALLOW_MIXED_METHODS** | TRUE |
| **UPDATE_LATEST_POINTER** | FALSE |
| **Rounding** | NONE (default) |
| **OUTPUT_LABEL** | DEL-001-08 |

## Resolved Price Sources

| # | Path | Type | Notes |
|---|---|---|---|
| 1 | PriceSources/Professional_Staff_Rates.csv | PARAMETRIC | 25 roles with hourly rates in CAD |
| 2 | PriceSources/Level_of_Effort.csv | PARAMETRIC | Estimated hours by role per deliverable |
| 3 | PriceSources/Assumed_Project_Parameters.csv | PARAMETRIC | 18 project parameters (areas, capacities, schedule) |
| 4 | PriceSources/Professional_Design_Fees.csv | PARAMETRIC | Design fee percentages by discipline |
| 5 | PriceSources/Parametric_Building_Rates.csv | PARAMETRIC | Building cost rates per sf |

## Scope Resolution

- **Deliverable:** DEL-001-08 Finish Schedule
- **Package:** PKG-001 Architectural Design
- **Discipline:** Architect
- **Type:** Schedule
- **SOW coverage:** SOW-0011
- **Documents read:** _CONTEXT.md, Datasheet.md, Specification.md, Guidance.md, Procedure.md (all 4 production documents present)

## Warnings

- None. All four production documents present and readable. All five price sources loaded successfully.
