# Assumptions Log -- EST_DEL-07-01_2026-02-18_1700

| AssumptionID | Assumption | Source | Impact if Wrong |
|---|---|---|---|
| ASM-001 | Hourly rates in Professional_Staff_Rates.csv are representative of actual blended rates the firm would charge for this proposal effort | Professional_Staff_Rates.csv (Basis=MARKET, Confidence=MEDIUM) | If actual rates differ, the total will scale linearly; +/- 15% rate variance = +/- $384 on total |
| ASM-002 | Hours in Level_of_Effort.csv for DEL-07-01 (12 hrs CM, 4 hrs PM = 16 hrs total) are a reasonable estimate of the effort to produce the construction methodology narrative | Level_of_Effort.csv (Basis=PARAMETRIC) | If actual effort differs, the total will scale; a 50% overrun would add $1,280 |
| ASM-003 | The construction methodology narrative is a standalone proposal section; no additional roles (e.g., Safety Officer, Scheduler, Proposal Writer) contribute hours to DEL-07-01 specifically | Level_of_Effort.csv (only R-15 and R-02 rows present for DEL-07-01) | If additional roles are needed, the estimate would increase; a Proposal Writer (R-22 at $105/hr) for 4 hrs editing would add $420 |
| ASM-004 | No printing, reproduction, or external review costs are included; this estimate covers professional labor hours only | Brief context (proposal production cost estimate = hours to write) | If printing/binding or external review is required, those costs would be additional |
