# Assumptions Log -- EST_DEL-01-01_2026-02-18_1400

| AssumptionID | Assumption | Source | Impact if Wrong |
|---|---|---|---|
| EST-ASM-001 | The 8 hours allocated to R-22 for DEL-01-01 in Level_of_Effort.csv are sufficient for full compliance matrix production, RFP section mapping, and addenda integration checklist. | Level_of_Effort.csv row DEL-01-01/R-22 (Basis=PARAMETRIC) | If hours are insufficient, the estimate understates cost. The LoE basis is PARAMETRIC (not CONFIRMED), so this is an estimate-grade allocation. |
| EST-ASM-002 | The $105/hr rate for R-22 (Proposal Coordinator / Writer) is representative of the actual cost for this role. | Professional_Staff_Rates.csv row R-22 (Basis=MARKET, Confidence=MEDIUM) | If actual rate differs, the line item amount changes proportionally. MEDIUM confidence means +/-15-25% variance is plausible. |
| EST-ASM-003 | No other roles contribute billable hours to DEL-01-01. | Level_of_Effort.csv has exactly one row for DEL-01-01 | If a reviewer (e.g., PM) spends time on compliance review that is not captured in LoE, the estimate understates cost. The brief assigns compliance checking exclusively to DEL-01-01 scope. |
