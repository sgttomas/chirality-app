# Decision Log -- EST_DEL-06-02_2026-02-18_1800

| DecisionID | Decision | Rationale |
|---|---|---|
| EST-DEC-001 | CBS assigned as `DESIGN_MANAGEMENT` for all DEL-06-02 line items | No explicit CBSHint in decomposition. DEL-06-02 describes design management activities (milestone planning, coordination, QA/QC checkpoint definition) under PKG-006 Delivery Plan. Both contributing roles (Design Manager, Project Manager) are management-category. DESIGN_MANAGEMENT is the most descriptive CBS code for this scope. |
| EST-DEC-002 | Hours sourced from Level_of_Effort.csv (PARAMETRIC basis) used as quantities; rates sourced from Professional_Staff_Rates.csv (MARKET basis) | Brief instructs: use Level_of_Effort.csv for hours by role, Professional_Staff_Rates.csv for rates. Both sources are explicit PRICE_SOURCES. The combination (hours x rate) constitutes a RATE_TABLE method per protocol. |
| EST-DEC-003 | Rounding applied at DOLLAR level per brief | ROUNDING=DOLLAR. Both line items compute to whole-dollar amounts naturally (10x165=1650, 4x175=700), so no rounding adjustment was needed. |
| EST-DEC-004 | Confidence set to MED for all lines | Hours basis is PARAMETRIC (medium confidence); rate basis is MARKET (medium confidence). Combined confidence = MED. |
| EST-DEC-005 | Assumed_Project_Parameters.csv indexed but not used for pricing | This file provides contextual project parameters (durations, areas, quantities). None are directly relevant to pricing DEL-06-02 (a narrative deliverable). Indexed in Source_Index.md for completeness. |
