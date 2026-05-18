# Source Index

## Pricing Sources

| # | Source Path | Source Type | Parsing Notes | Supports |
|---|---|---|---|---|
| S1 | test/execution-6b/_PriceSources/Professional_Staff_Rates.csv | Rate Table | 30 roles with RoleID, hourly rate (CAD), category, confidence. Parsed as CSV with header row. | Unit rates for all professional staff roles |
| S2 | test/execution-6b/_PriceSources/Level_of_Effort.csv | Level of Effort (hours by deliverable and role) | 73 rows; filtered to Execution=6b and DeliverableID=DEL-02-04 yielding 2 rows. Parsed as CSV with header row. | Hour quantities per role per deliverable |
| S3 | test/execution-6b/_PriceSources/Assumed_Project_Parameters.csv | Project Parameters | 29 parameters covering duration, area, quantities, financial assumptions. Parsed as CSV with header row. | Context and validation only; not used for direct pricing of DEL-02-04 |

## Non-Pricing Sources

| # | Source Path | Source Type | Role in This Run |
|---|---|---|---|
| N1 | test/execution-6b/_Decomposition/Penhold_PSB_Project_Decomposition_v2.md | Decomposition (v2.3 FINAL) | Package/Deliverable ID validation; scope item traceability; CBS hint derivation |
| N2 | test/execution-6b/PKG-002_Conceptual_Design/1_Working/DEL-02-04_MechanicalConceptNarrative/Dependencies.csv | Dependency Register | Blocker/readiness assessment; 13 dependency rows parsed |

## Source Coverage Assessment

- **DEL-02-04 pricing**: Fully covered by S1 (rates) + S2 (hours). Two matching rows in Level_of_Effort.csv for DEL-02-04: R-11 (16 hrs) and R-12 (8 hrs).
- **No gaps**: All in-scope line items have both quantity and rate evidence from provided sources.
- **Assumed_Project_Parameters.csv**: Referenced for context (building area, bay counts, equipment quantities) but not used as a direct pricing input for this deliverable.
