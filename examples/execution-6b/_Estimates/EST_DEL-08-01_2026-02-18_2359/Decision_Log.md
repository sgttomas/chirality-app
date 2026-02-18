# Decision Log -- EST_DEL-08-01_2026-02-18_2359

| DecisionID | Decision | Rationale |
|---|---|---|
| EST-D-001 | CBS code `CX` assigned to Commissioning Lead (R-21) labor | R-21 is categorized as `Construction` in Professional_Staff_Rates.csv; mapped to `CX` (commissioning) CBS since the work is commissioning-specific labor within a commissioning deliverable |
| EST-D-002 | CBS code `MGMT` assigned to Project Manager (R-02) labor | R-02 is categorized as `Management` in Professional_Staff_Rates.csv; mapped to `MGMT` CBS |
| EST-D-003 | All line items priced as RATE_TABLE (no fallback used) | Both DEL-08-01 rows in Level_of_Effort.csv have matching rates in Professional_Staff_Rates.csv; STRICT fallback policy is satisfied; no mixed methods needed |
| EST-D-004 | Assumed_Project_Parameters.csv reviewed but not used for pricing | DEL-08-01 is a narrative deliverable; its cost is entirely labor-driven. No area, quantity, or duration parameters from Assumed_Project_Parameters.csv affect the line item pricing |
| EST-D-005 | Rounding applied at DOLLAR level to amounts | Per brief ROUNDING=DOLLAR; both amounts ($1,400 and $700) are already whole dollars so no rounding adjustment was needed |
| EST-D-006 | Dependencies assessed as non-blocking for estimating | 15 dependency rows loaded; all are coordination interfaces, traceability anchors, or content prerequisites that do not affect labor hours or rates |
