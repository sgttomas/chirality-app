# Run Context — EST_DEL-001-10_2026-02-27_0600

| Field | Value |
|---|---|
| **RunID** | EST_DEL-001-10_2026-02-27_0600 |
| **AsOf** | 2026-02-27T06:00:00-07:00 |
| **Scope** | DEL-001-10 |
| **ScopeResolvedSummary** | 1 deliverable (DEL-001-10 Old North Shop Renovation Plans) in PKG-001 Architectural Design |
| **BASIS_OF_ESTIMATE** | PARAMETRIC |
| **CURRENCY** | CAD |
| **PRICE_SOURCES** | 1. Professional_Staff_Rates.csv; 2. Level_of_Effort.csv; 3. Assumed_Project_Parameters.csv; 4. Professional_Design_Fees.csv; 5. Parametric_Building_Rates.csv |
| **DECOMPOSITION_PATH** | _Decomposition/WDMLRL_Decomposition_Claude.md |
| **FALLBACK_POLICY** | ALLOW_PARAMETRIC |
| **ALLOW_MIXED_METHODS** | TRUE |
| **UPDATE_LATEST_POINTER** | FALSE |
| **OUTPUT_LABEL** | DEL-001-10 |
| **Rounding** | NONE (default) |
| **DELIVERABLE_PATH** | PKG-001_Architectural Design/1_Working/DEL-001-10_Renovation-Plans |
| **Warnings** | None |

## Resolved Defaults

- `ROUNDING`: NONE (not specified in brief; using default)
- `RUN_TIMESTAMP`: 2026-02-27T06:00:00-07:00 (provided in brief)
- All four deliverable documents (Datasheet.md, Specification.md, Guidance.md, Procedure.md) found and read successfully for DEL-001-10.
- `_CONTEXT.md` read for deliverable identification metadata.

## Price Source Resolution

| # | File | Type | Status |
|---|---|---|---|
| 1 | Professional_Staff_Rates.csv | Rate table (25 roles with hourly rates in CAD) | Usable — provides hourly rates for all roles |
| 2 | Level_of_Effort.csv | Parametric LOE model (hours per deliverable per role) | Usable — provides DEL-001-10 rows (5 roles, 130 total hours) |
| 3 | Assumed_Project_Parameters.csv | Project parameters (18 parameters) | Usable — provides project context and facility parameters |
| 4 | Professional_Design_Fees.csv | Fee percentage model (5 disciplines) | Usable — alternative fee-based pricing approach (not primary for this deliverable) |
| 5 | Parametric_Building_Rates.csv | Building rate model (2 items) | Usable — overall building cross-check (not primary for design deliverable) |
