# Run Context — EST_DEL-013-02_2026-02-27_0901

| Field | Value |
|---|---|
| **RunID** | EST_DEL-013-02_2026-02-27_0901 |
| **AsOf** | 2026-02-27T09:01Z |
| **Scope** | DEL-013-02 |
| **ScopeResolvedSummary** | 1 deliverable (DEL-013-02: High-Volume Air Exchanger), 1 package (PKG-013) |
| **BASIS_OF_ESTIMATE** | PARAMETRIC |
| **CURRENCY** | CAD |
| **PRICE_SOURCES** | Professional_Staff_Rates.csv, Level_of_Effort.csv, Assumed_Project_Parameters.csv, Mechanical_System_Rates.csv, Construction_Labour_Rates.csv, Equipment_Pricing.csv |
| **DECOMPOSITION_PATH** | {RUN_ROOT}/_Decomposition/WDMLRL_Decomposition_Claude.md |
| **FALLBACK_POLICY** | ALLOW_PARAMETRIC |
| **ALLOW_MIXED_METHODS** | TRUE |
| **UPDATE_LATEST_POINTER** | FALSE |
| **Rounding** | NONE (default) |
| **OUTPUT_LABEL** | DEL-013-02 |
| **DELIVERABLE_PATH** | {RUN_ROOT}/PKG-013_Mechanical & HVAC Installation/1_Working/DEL-013-02_Air-Exchanger |

## Resolved Paths

- **RUN_ROOT:** /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude
- **ESTIMATES_ROOT:** {RUN_ROOT}/_Estimates/
- **Snapshot Folder:** {ESTIMATES_ROOT}/EST_DEL-013-02_2026-02-27_0901/
- **Price Sources Root:** {RUN_ROOT}/_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/

## Documents Read

| Document | Status |
|---|---|
| _CONTEXT.md | READ |
| Datasheet.md | READ |
| Specification.md | READ |
| Guidance.md | READ |
| Procedure.md | READ |
| Decomposition | READ (filtered for DEL-013-02 / PKG-013) |

## Warnings

- W-001: Air exchange capacity (CFM) is TBD pending Mechanical Engineer design — equipment unit pricing used as ALLOWANCE from Mechanical_System_Rates.csv (MS-03).
- W-002: Ductwork quantities (m2 floor area served) are ASSUMED at 13,000 sq ft from project parameters; actual ductwork scope TBD pending HVAC design (DEL-003-02, DEL-003-03).
- W-003: Several specification requirements are TBD pending Mechanical Engineer design (heat recovery efficiency target, acoustic criteria, vibration isolation spec, cold-climate minimum design temp). Pricing uses parametric/allowance basis where applicable.
- W-004: Electrical scope boundary between PKG-013 and PKG-015 is TBD (Guidance Conflict Table C-002). Power connection labour included as minimal allowance only.
