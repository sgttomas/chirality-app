# Decision Log — EST_DEL-021-02_2026-02-27_0540

| DecisionID | Decision | Rationale | Source |
|---|---|---|---|
| DEC-001 | Used PARAMETRIC basis for all line items | BASIS_OF_ESTIMATE = PARAMETRIC; all price sources are parametric (rates, hours, allowances) | Run brief; Professional_Staff_Rates.csv; Level_of_Effort.csv; Fees_Permits_Insurance.csv |
| DEC-002 | Used Fees_Permits_Insurance.csv FP-01 RecommendedRate ($22,000) for performance bond premium | Contract price is TBD; FP-01 provides a parametric allowance with range $12K–$35K and recommended $22,000 | Fees_Permits_Insurance.csv FP-01 |
| DEC-003 | Used Fees_Permits_Insurance.csv FP-02 RecommendedRate ($17,000) for payment bond premium | Contract price is TBD; FP-02 provides a parametric allowance with range $9K–$28K and recommended $17,000 | Fees_Permits_Insurance.csv FP-02 |
| DEC-004 | Priced bond premiums as LUMP_SUM (Qty=1, Unit=LS) per parametric/allowance convention | Bond premiums are fixed-cost items to the proponent, not unit-rate items | AGENT_ESTIMATING.md STRUCTURE — Allowance/parametric convention |
| DEC-005 | Matched Level_of_Effort.csv rows for DEL-021-02 to Professional_Staff_Rates.csv for hourly rates | 8 roles matched: R-01 (PM), R-02 (CPM), R-03 (Supt), R-05 (HSE), R-06 (QA/QC), R-08 (CE), R-09 (DC), R-25 (CA) | Level_of_Effort.csv; Professional_Staff_Rates.csv |
| DEC-006 | Scope resolution: DEL-021-02 covers only the cost to the proponent (bond premiums + labour) — not the bond face amount or coverage values | Bond face amounts (50% of contract price each) are Owner-facing coverage values, not proponent costs | Datasheet Attributes; Guidance Considerations — Bond Amount Calculation |
| DEC-007 | CBS categories assigned based on role function: Bonding (premiums), Labour — Contract Administration, Labour — Management, Labour — Construction Management, Labour — Construction, Labour — Admin | Consistent with staff role categories in Professional_Staff_Rates.csv | Professional_Staff_Rates.csv Category column |
