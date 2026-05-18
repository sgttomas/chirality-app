# Decision Log

**RunID:** EST_DEL-06-01_2026-02-18_1600

---

| DecisionID | Decision | Rationale |
|---|---|---|
| EST-D-001 | CBS code `MGMT` assigned to both line items based on role Category = "Management" in Professional_Staff_Rates.csv | Deterministic mapping rule: CBS derived from rate table Category column. Both R-02 (Project Manager) and R-03 (Design Manager) have Category = "Management". No explicit CBSHint was present in the decomposition. Rule documented in Run_Context.md. |
| EST-D-002 | Hours sourced from Level_of_Effort.csv treated as quantities (Qty) for RATE_TABLE method | Level_of_Effort.csv provides "EstimatedHours" with Basis = "PARAMETRIC". These are used as the quantity input; the rate table provides the unit rate. Combined, this constitutes a RATE_TABLE estimate method where Qty and UnitRate are from separate but complementary sources. |
| EST-D-003 | No fallback method applied | FALLBACK_POLICY = STRICT. All line items had complete pricing inputs (hours and rates available for both roles). No fallback was needed. |
| EST-D-004 | Rounding applied at DOLLAR level | ROUNDING = DOLLAR per run brief. Both line items produce whole-dollar amounts (1650, 700), so rounding had no effect on this run. |
| EST-D-005 | Assumed_Project_Parameters.csv was indexed but not used for pricing | This source provides project-level parameters (durations, areas, quantities, financial estimates) that do not directly contribute to DEL-06-01 line-item pricing. It was indexed in Source_Index.md for completeness and potential cross-check use. |
