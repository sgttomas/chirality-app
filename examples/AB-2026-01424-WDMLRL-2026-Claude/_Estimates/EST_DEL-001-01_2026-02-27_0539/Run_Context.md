# Run Context — EST_DEL-001-01_2026-02-27_0539

| Field | Value |
|---|---|
| **RunID** | EST_DEL-001-01_2026-02-27_0539 |
| **AsOf** | 2026-02-27T05:39:00Z |
| **Scope** | DEL-001-01 (Preliminary Architectural Design) |
| **ScopeResolvedSummary** | 1 deliverable; 1 package (PKG-001 Architectural Design) |
| **BASIS_OF_ESTIMATE** | PARAMETRIC |
| **CURRENCY** | CAD |
| **PRICE_SOURCES** | Professional_Staff_Rates.csv, Level_of_Effort.csv, Assumed_Project_Parameters.csv, Professional_Design_Fees.csv, Parametric_Building_Rates.csv |
| **DECOMPOSITION_PATH** | _Decomposition/WDMLRL_Decomposition_Claude.md |
| **FALLBACK_POLICY** | ALLOW_PARAMETRIC |
| **ALLOW_MIXED_METHODS** | TRUE |
| **UPDATE_LATEST_POINTER** | FALSE |
| **Rounding** | NONE |
| **Warnings** | None |

## Resolved Paths

- **RUN_ROOT:** `/Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude`
- **ESTIMATES_ROOT:** `/Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/_Estimates`
- **Deliverable Folder:** `PKG-001_Architectural Design/1_Working/DEL-001-01_Preliminary-Design`
- **Documents Read:** Datasheet.md, Specification.md, Guidance.md, Procedure.md, _CONTEXT.md

## Price Sources Resolved

| Source File | Type | Notes |
|---|---|---|
| Professional_Staff_Rates.csv | Rate Table | 25 roles with CAD hourly rates; Basis=PARAMETRIC, Confidence=MEDIUM |
| Level_of_Effort.csv | Parametric Model | Hours by role per deliverable; DEL-001-01 has 5 role entries totalling 70 hrs |
| Assumed_Project_Parameters.csv | Reference Parameters | 19 parameters; building ~13,000 sqft, 35 ft ceiling, 2x5T cranes, etc. |
| Professional_Design_Fees.csv | Parametric Model | Fee percentages by discipline as % of construction value; useful for cross-check |
| Parametric_Building_Rates.csv | Parametric Model | $/sf rates for industrial building and wash bay premium |
