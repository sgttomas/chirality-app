# Decision Log -- EST_DEL-10-01_2026-02-18_1900

| Decision ID | Decision | Rationale |
|---|---|---|
| EST-DEC-001 | CBS codes assigned as PROF-PM and PROF-CM based on role category + role abbreviation | No explicit CBSHint in decomposition. Deterministic rule: "PROF" prefix (professional services labor) + role abbreviation (PM, CM). Documented in Run_Context.md. |
| EST-DEC-002 | Assumed_Project_Parameters.csv not used for direct pricing | This file provides project-level parameters (areas, quantities, durations) that do not apply to DEL-10-01 proposal production costing. Referenced for context only. |
| EST-DEC-003 | All amounts rounded to nearest dollar per ROUNDING=DOLLAR | Both computed amounts (1750, 620) are already whole dollars; no rounding adjustment was necessary. |
| EST-DEC-004 | No fallback method applied | FALLBACK_POLICY=STRICT. All line items have basis evidence from Level_of_Effort.csv (hours) and Professional_Staff_Rates.csv (rates). No TBD amounts needed. |
| EST-DEC-005 | Dependency evidence used for readiness/blocker analysis only | Per invariant "Dependencies are not pricing evidence." DEP-10-01-003 through DEP-10-01-012 inform content readiness but do not affect pricing. |
