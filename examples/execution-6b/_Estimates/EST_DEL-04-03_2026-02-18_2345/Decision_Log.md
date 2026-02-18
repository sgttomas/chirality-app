# Decision Log

| DecisionID | Decision | Rationale |
|---|---|---|
| EST-DEC-001 | CBS code assigned as `PROF_SERVICES.ELECTRICAL` for all DEL-04-03 line items. | No explicit CBSHint in decomposition. Deterministic rule applied: deliverables authored by Electrical Engineer are mapped to PROF_SERVICES.ELECTRICAL. Rule documented in Run_Context.md. |
| EST-DEC-002 | Hours sourced from Level_of_Effort.csv (Basis=PARAMETRIC) treated as compatible with BASIS_OF_ESTIMATE=RATE_TABLE. | Level_of_Effort.csv provides quantity (hours) while Professional_Staff_Rates.csv provides the rate. The combination is a rate-table pricing method: Qty x UnitRate = Amount. The LoE hours basis describes how quantities were derived, not the pricing method. |
| EST-DEC-003 | Dependencies treated as production sequencing constraints, not pricing blockers. | Level of effort for a proposal-stage narrative deliverable is determined by scope complexity and discipline effort, not by whether upstream deliverables are complete. The estimate is valid regardless of production sequencing status. |
| EST-DEC-004 | Cost ownership boundaries enforced per brief: solar-ready ELECTRICAL provisions costed in DEL-04-03 only. | Brief explicitly states: "Solar-ready ELECTRICAL provisions -> DEL-04-03 (NOT in DEL-02-05 concept)." This prevents double-counting across the estimate portfolio. |
| EST-DEC-005 | Rounding applied at DOLLAR level per run configuration. | $1,240 is already a whole dollar amount; no rounding adjustment needed. |
