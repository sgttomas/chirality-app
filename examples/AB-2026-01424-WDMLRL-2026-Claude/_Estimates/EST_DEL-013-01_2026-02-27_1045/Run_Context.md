# Run_Context — EST_DEL-013-01_2026-02-27_1045

| Field | Value |
|---|---|
| **RunID** | EST_DEL-013-01_2026-02-27_1045 |
| **AsOf** | 2026-02-27T10:45:00-07:00 |
| **Scope** | DEL-013-01 |
| **ScopeResolvedSummary** | 1 deliverable (DEL-013-01: High-Recovery Heating System) in PKG-013 (Mechanical & HVAC Installation) |
| **BASIS_OF_ESTIMATE** | PARAMETRIC |
| **CURRENCY** | CAD |
| **PRICE_SOURCES** | Professional_Staff_Rates.csv, Level_of_Effort.csv, Assumed_Project_Parameters.csv, Mechanical_System_Rates.csv, Construction_Labour_Rates.csv, Equipment_Pricing.csv |
| **DECOMPOSITION_PATH** | _Decomposition/WDMLRL_Decomposition_Claude.md |
| **FALLBACK_POLICY** | ALLOW_PARAMETRIC |
| **ALLOW_MIXED_METHODS** | TRUE |
| **UPDATE_LATEST_POINTER** | FALSE |
| **OUTPUT_LABEL** | DEL-013-01 |
| **Rounding** | NONE (default) |

## Resolved Paths

- **RUN_ROOT:** /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude
- **ESTIMATES_ROOT:** /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/_Estimates
- **DELIVERABLE_PATH:** PKG-013_Mechanical & HVAC Installation/1_Working/DEL-013-01_Heating-System

## Documents Read

| Document | Status |
|---|---|
| _CONTEXT.md | Read |
| Datasheet.md | Read |
| Specification.md | Read |
| Guidance.md | Read |
| Procedure.md | Read |
| Decomposition | Read (PKG-013 / DEL-013-01 sections) |

## Warnings

- W-001: Heating capacity (BTU/h or kW) is TBD pending DEL-003-06 Mechanical Calculation Package. Equipment pricing relies on parametric/allowance rates from Mechanical_System_Rates.csv.
- W-002: Fuel/energy source not formally confirmed (ASSUMPTION: natural gas). Affects pricing of gas connections and gas fitter labour.
- W-003: Equipment type (radiant vs. forced-air vs. hydronic) is TBD pending DEL-003-07 Mechanical Specification. Pricing uses generic high-recovery unit heater allowance.
- W-004: BMS communication protocol TBD. Controls integration priced as parametric allowance.
- W-005: Ductwork quantity derived parametrically from building floor area (approx. 13,000 sq ft / 1,208 m2). Actual quantity TBD pending mechanical drawings.
