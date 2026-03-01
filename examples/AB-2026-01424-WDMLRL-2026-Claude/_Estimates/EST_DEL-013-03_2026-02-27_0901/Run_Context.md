# Run Context — EST_DEL-013-03_2026-02-27_0901

| Field | Value |
|---|---|
| **RunID** | EST_DEL-013-03_2026-02-27_0901 |
| **AsOf** | 2026-02-27T09:01Z |
| **Scope** | DEL-013-03 |
| **ScopeResolvedSummary** | 1 deliverable (DEL-013-03: Forced-Air Makeup System) in PKG-013 |
| **BASIS_OF_ESTIMATE** | PARAMETRIC |
| **CURRENCY** | CAD |
| **PRICE_SOURCES** | Professional_Staff_Rates.csv, Level_of_Effort.csv, Assumed_Project_Parameters.csv, Mechanical_System_Rates.csv, Construction_Labour_Rates.csv, Equipment_Pricing.csv |
| **DECOMPOSITION_PATH** | {RUN_ROOT}/_Decomposition/WDMLRL_Decomposition_Claude.md |
| **FALLBACK_POLICY** | ALLOW_PARAMETRIC |
| **ALLOW_MIXED_METHODS** | TRUE |
| **UPDATE_LATEST_POINTER** | FALSE |
| **Rounding** | NONE (default) |
| **OUTPUT_LABEL** | DEL-013-03 |
| **DELIVERABLE_PATH** | {RUN_ROOT}/PKG-013_Mechanical & HVAC Installation/1_Working/DEL-013-03_Makeup-Air |

## Resolved Paths

- RUN_ROOT: /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude
- ESTIMATES_ROOT: {RUN_ROOT}/_Estimates
- Snapshot: {ESTIMATES_ROOT}/EST_DEL-013-03_2026-02-27_0901/

## Deliverable Identity (from _CONTEXT.md)

- **Deliverable ID**: DEL-013-03
- **Title**: Forced-Air Makeup System
- **Package**: PKG-013 — Mechanical & HVAC Installation
- **Type**: Mechanical & HVAC Installation
- **SOW Reference**: SOW-0037
- **Responsible Party**: Mechanical Contractor

## Documents Read

| Document | Status |
|---|---|
| _CONTEXT.md | READ |
| Datasheet.md | READ |
| Specification.md | READ |
| Guidance.md | READ |
| Procedure.md | READ |
| Decomposition | READ (DEL-013-03 confirmed in PKG-013, SOW-0037) |

## Warnings

- W-01: MUA supply airflow rate is TBD (BLOCKING per Datasheet) -- equipment sizing not finalized; unit cost based on parametric allowance range.
- W-02: Design outdoor air temperature TBD -- heating capacity sizing not independently verifiable.
- W-03: MUA make/model TBD -- equipment cost is parametric estimate from Mechanical_System_Rates.csv (MS-02).
- W-04: Ductwork routing, quantity, and distribution point count TBD -- ductwork cost is parametric per floor area from Mechanical_System_Rates.csv (MS-06).
- W-05: Fire/smoke damper quantity and locations TBD -- estimated as parametric allowance.
- W-06: Supply ductwork insulation type/thickness TBD -- estimated as parametric percentage of ductwork cost.
