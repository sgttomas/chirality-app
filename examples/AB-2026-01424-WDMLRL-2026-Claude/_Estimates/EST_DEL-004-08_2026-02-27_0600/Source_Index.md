# Source Index — EST_DEL-004-08_2026-02-27_0600

## Pricing Sources

| # | Source File | Source Type | Parsing Notes | Supports |
|---|---|---|---|---|
| PS-01 | _EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Staff_Rates.csv | PARAMETRIC (rate table) | 25 roles with CAD hourly rates; all PARAMETRIC basis, MEDIUM confidence. Key roles for this deliverable: R-01 (PM, $165/hr), R-08 (Cost Estimator, $135/hr), R-13 (BIM Technician, $95/hr), R-16 (Electrical Engineer, $165/hr). | Unit rate pricing for all labour line items |
| PS-02 | _EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Level_of_Effort.csv | PARAMETRIC (effort model) | Multi-deliverable LOE table. DEL-004-08 rows: R-01 6h, R-08 4h, R-13 24h, R-16 56h. Total 90 hours. All PARAMETRIC basis. | Quantity (hours) for each role per deliverable |
| PS-03 | _EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Assumed_Project_Parameters.csv | PARAMETRIC (parameters) | 19 parameters; key for this deliverable: PP-10 (floor area ~13,000 sqft), PP-11 (ceiling height 35 ft), PP-12 (2 overhead cranes), PP-13 (5 ton crane capacity), PP-17 (currency CAD). | Context and scope parameters for reasonableness checks |
| PS-04 | _EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Design_Fees.csv | PARAMETRIC (fee model) | 5 discipline fee percentages. DF-04 Electrical: 1.0%–2.2% of construction value, recommended 1.6%. Not used directly for this estimate (LOE-based pricing preferred) but available as cross-check. | Cross-check only; not primary pricing basis for this run |

## Deliverable Documents Read

| Document | Path | Items Extracted |
|---|---|---|
| _CONTEXT.md | PKG-004_Electrical Design/1_Working/DEL-004-08_Calculation-Package/_CONTEXT.md | Deliverable identification, package, discipline, type |
| Datasheet.md | PKG-004_Electrical Design/1_Working/DEL-004-08_Calculation-Package/Datasheet.md | Building parameters, lighting attributes, receptacle types, equipment circuits, crane data gaps, low-voltage systems, conditions |
| Specification.md | PKG-004_Electrical Design/1_Working/DEL-004-08_Calculation-Package/Specification.md | 24 requirements (REQ-004-08-01 through REQ-004-08-24), verification methods, standards |
| Guidance.md | PKG-004_Electrical Design/1_Working/DEL-004-08_Calculation-Package/Guidance.md | Design principles, trade-offs, considerations, conflict table (5 conflicts) |
| Procedure.md | PKG-004_Electrical Design/1_Working/DEL-004-08_Calculation-Package/Procedure.md | 10 production steps + Step 9A, prerequisites, verification checks, records |

## Decomposition Reference

| Document | Path | Usage |
|---|---|---|
| WDMLRL_Decomposition_Claude.md | _Decomposition/WDMLRL_Decomposition_Claude.md | WBS traceability: PKG-004 (Electrical Design), DEL-004-08 (Electrical Calculation Package), SOW-0014, OBJ-003, OBJ-005 |
