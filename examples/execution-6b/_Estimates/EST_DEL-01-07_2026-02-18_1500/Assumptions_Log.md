# Assumptions Log — EST_DEL-01-07_2026-02-18_1500

| AssumptionID | Assumption | Source | Impact if Wrong |
|---|---|---|---|
| ASM-001 | Hourly rates in Professional_Staff_Rates.csv are representative of actual project costs for the proposal team | Professional_Staff_Rates.csv (Basis=MARKET, Confidence=MEDIUM) | If actual rates differ, total will scale linearly. A +/-20% rate variance on R-22 ($105/hr) changes total by +/-$336. |
| ASM-002 | Level-of-effort hours in Level_of_Effort.csv are a reasonable estimate for the firm experience profile deliverable | Level_of_Effort.csv (Basis=PARAMETRIC, Confidence implied MEDIUM) | If actual hours differ, total will scale linearly. The 16-hour writer allocation assumes a standard firm profile with 4-6 project summaries. More projects or deeper research could add 4-8 hours. |
| ASM-003 | The firm experience profile is a standalone narrative document (not requiring significant graphic design, photography, or external production services) | Decomposition DEL-01-07 description; RFP Section 7.1.6 | If external production (graphic layout, professional photography of past projects) is required, an additional cost category would be needed. |
| ASM-004 | No travel or site visits to past project locations are required for the firm experience profile | Implied by proposal-stage scope | If reference site visits are needed, travel costs would be additional. |
