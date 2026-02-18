# Assumptions Log -- EST_DEL-03-03_2026-02-18_2300

| AssumptionID | Assumption | Source / Basis | Impact if Wrong |
|---|---|---|---|
| ASM-001 | The Level of Effort for DEL-03-03 is 10 hours of Structural Engineer (Senior) time, as stated in Level_of_Effort.csv | Level_of_Effort.csv row: DEL-03-03, R-09, 10 hr, Basis=PARAMETRIC | If actual effort differs, the total cost scales linearly at $155/hr. A +/- 4 hour variance would represent +/- $620. |
| ASM-002 | The hourly rate for Structural Engineer (Senior) is $155 CAD, as stated in Professional_Staff_Rates.csv | Professional_Staff_Rates.csv row R-09, $155/hr, Basis=MARKET, Confidence=MEDIUM | Rate is market-based with MEDIUM confidence. Actual negotiated rate may vary. |
| ASM-003 | No additional roles contribute to DEL-03-03 beyond R-09 | Level_of_Effort.csv contains only one row for DEL-03-03 | If a Structural Engineer (Intermediate) or other supporting role is needed, additional hours at their respective rate would increase total cost. |
| ASM-004 | The scope of DEL-03-03 as described in the decomposition (system selection rationale, expansion provisions, foundation approach, load path narrative) is stable and will not expand | Decomposition v2.3 FINAL, Section 9, DEL-03-03 description | Scope expansion (e.g., additional analysis for complex foundation conditions, expanded expansion narrative) could increase hours. |
