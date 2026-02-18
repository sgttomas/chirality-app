# Decision Log — EST_DEL-02-01_2026-02-18_2000

| DecisionID | Decision | Rationale |
|---|---|---|
| EST-D-001 | CBS codes derived as `LABOR-{Category}` from Professional_Staff_Rates.csv Category column | No project-standard CBS dictionary was provided. Deterministic derivation from rate table categories ensures consistency across estimates. |
| EST-D-002 | All line items use Method = RATE_TABLE despite Level_of_Effort.csv Basis = PARAMETRIC | The hours source (Level_of_Effort.csv) uses parametric modeling to derive hours, but the pricing method is RATE_TABLE (rate x quantity). The declared BASIS_OF_ESTIMATE = RATE_TABLE governs the Method column. The parametric nature of the hours input is documented in Assumptions_Log.md. |
| EST-D-003 | Only architectural roles (R-02, R-04, R-05, R-06) included for DEL-02-01 | Per cost ownership rules in the brief: DEL-02-01 carries architectural drawings + program integration + coordination leadership. Civil, structural, mechanical, and electrical hours belong to DEL-02-02 through DEL-02-05 respectively. |
| EST-D-004 | PM hours (R-02, 8h) included in DEL-02-01 rather than distributed across PKG-002 | Level_of_Effort.csv explicitly allocates 8 PM hours to DEL-02-01 for "coordination oversight; client interface." This is consistent with DEL-02-01 being the highest-effort and coordination-leading deliverable in PKG-002. |
| EST-D-005 | No materials, equipment, or subcontractor line items included | DEL-02-01 is proposal production cost (hours to produce architectural concept drawings). No physical materials or subcontract scope is involved. |
| EST-D-006 | DOLLAR rounding applied; no sub-dollar amounts exist | All amounts are products of integer hours and integer rates, yielding whole-dollar amounts. Rounding has no mathematical effect on this estimate. |
