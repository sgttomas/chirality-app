# Decision Log -- EST_DEL-02-02_2026-02-18_2100

| DecisionID | Decision | Rationale |
|---|---|---|
| EST-D-001 | CBS codes assigned by role category: Design -> CBS-200, Production -> CBS-210 | No `CBSHint` present in decomposition for DEL-02-02. Deterministic mapping from `Professional_Staff_Rates.csv` `Category` column. Civil Engineer (Senior) and Civil Engineer (Intermediate) are both `Category=Design` -> CBS-200. CAD Technician / BIM Operator is `Category=Production` -> CBS-210. |
| EST-D-002 | Method set to RATE_TABLE for all 3 line items despite Level_of_Effort.csv showing `Basis=PARAMETRIC` | The LoE table's `Basis` column describes how the *hours* were estimated (parametric judgment). The estimate snapshot's `Method` column describes how the *price* is computed: hours (quantity) multiplied by hourly rate from the rate table. This is a RATE_TABLE method per the AGENT_ESTIMATING protocol. `ALLOW_MIXED_METHODS=FALSE` is satisfied. |
| EST-D-003 | No fallback pricing applied | All 3 line items for DEL-02-02 have both quantity evidence (Level_of_Effort.csv) and rate evidence (Professional_Staff_Rates.csv). `FALLBACK_POLICY=STRICT` was not triggered. |
| EST-D-004 | Dependency register used for blocker assessment only, not for pricing evidence | Per AGENT_ESTIMATING invariant: "Dependencies are not pricing evidence." The 20 dependency rows inform readiness/sequencing (e.g., DEL-02-01 prerequisite) but no amounts are derived from dependency data. |
| EST-D-005 | Rounding confirmed as no-op for this deliverable | All three line items produce exact integer amounts (24x155=3720, 16x125=2000, 16x95=1520). ROUNDING=DOLLAR has no effect. |
