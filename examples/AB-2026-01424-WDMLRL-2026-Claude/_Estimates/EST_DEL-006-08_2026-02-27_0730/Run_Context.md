# Run Context — EST_DEL-006-08_2026-02-27_0730

| Field | Value |
|-------|-------|
| **RunID** | EST_DEL-006-08_2026-02-27_0730 |
| **AsOf** | 2026-02-27T07:30:00-07:00 |
| **Scope** | DEL-006-08 |
| **ScopeResolvedSummary** | 1 deliverable (DEL-006-08 Plumbing Specification) in 1 package (PKG-006 Plumbing Design) |
| **BASIS_OF_ESTIMATE** | PARAMETRIC |
| **CURRENCY** | CAD |
| **PRICE_SOURCES** | 1. Professional_Staff_Rates.csv  2. Level_of_Effort.csv  3. Assumed_Project_Parameters.csv  4. Professional_Design_Fees.csv |
| **DECOMPOSITION_PATH** | _Decomposition/WDMLRL_Decomposition_Claude.md |
| **FALLBACK_POLICY** | ALLOW_PARAMETRIC |
| **ALLOW_MIXED_METHODS** | TRUE |
| **UPDATE_LATEST_POINTER** | FALSE |
| **Rounding** | NONE (default) |
| **OUTPUT_LABEL** | DEL-006-08 |
| **Warnings** | None |

## Resolved Paths

- **ESTIMATES_ROOT:** `{RUN_ROOT}/_Estimates/`
- **DELIVERABLE_PATH:** `PKG-006_Plumbing Design/1_Working/DEL-006-08_Specification/`
- **Documents read:**
  - `_CONTEXT.md` — present
  - `Datasheet.md` — present
  - `Specification.md` — present
  - `Guidance.md` — present
  - `Procedure.md` — present

## Pricing Source Resolution

| Source File | Type | Status |
|------------|------|--------|
| Professional_Staff_Rates.csv | Rate table (hourly rates by role) | Usable — 25 roles with CAD hourly rates |
| Level_of_Effort.csv | Parametric LOE (hours by deliverable and role) | Usable — DEL-006-08 rows found (4 role assignments) |
| Assumed_Project_Parameters.csv | Parametric parameters | Usable — 19 parameters including facility dimensions, equipment counts |
| Professional_Design_Fees.csv | Parametric fee percentages | Informational — percentage-based fee model (not directly used for DEL-level pricing; LOE approach preferred) |

## Defaults Applied

- `ROUNDING`: NONE (protocol default)
- `UPDATE_LATEST_POINTER`: FALSE (as specified)
- CBS codes: assigned based on deliverable type and content categories
