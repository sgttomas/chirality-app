# Source Index

## Pricing Sources

| # | Source Path | Source Type | Parsing Notes | Supports |
|---|---|---|---|---|
| S1 | test/execution-6b/_PriceSources/Professional_Staff_Rates.csv | Rate Table | 30 roles with RoleID, hourly rate (CAD), category, confidence. Parsed as CSV with header row. | Unit rates for all professional staff roles |
| S2 | test/execution-6b/_PriceSources/Level_of_Effort.csv | Level of Effort (hours by deliverable and role) | 73 rows; filtered to Execution=6b and DeliverableID=DEL-04-02 yielding 1 row. Parsed as CSV with header row. | Hour quantities per role per deliverable |
| S3 | test/execution-6b/_PriceSources/Assumed_Project_Parameters.csv | Project Parameters | 29 parameters covering duration, area, quantities, financial assumptions. Parsed as CSV with header row. | Context and validation only; not used for direct pricing of DEL-04-02 |

## Non-Pricing Sources

| # | Source Path | Source Type | Role in This Run |
|---|---|---|---|
| N1 | test/execution-6b/_Decomposition/Penhold_PSB_Project_Decomposition_v2.md | Decomposition (v2.3 FINAL) | Package/Deliverable ID validation; scope item traceability; CBS hint derivation |
| N2 | test/execution-6b/PKG-004_Sustainability_and_Energy/1_Working/DEL-04-02_MechanicalEnergyAndSolarReadiness/Dependencies.csv | Dependency Register | Blocker/readiness assessment; 12 dependency rows parsed |

## Source Coverage Assessment

- **DEL-04-02 pricing**: Fully covered by S1 (rates) + S2 (hours). One matching row in Level_of_Effort.csv for DEL-04-02: R-11 (10 hrs).
- **No gaps**: All in-scope line items have both quantity and rate evidence from provided sources.
- **Assumed_Project_Parameters.csv**: Referenced for context (building area, equipment counts, solar orientation constraints) but not used as a direct pricing input for this deliverable.
