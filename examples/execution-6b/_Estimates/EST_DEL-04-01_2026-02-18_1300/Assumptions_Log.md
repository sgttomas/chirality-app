# Assumptions Log

**RunID:** EST_DEL-04-01_2026-02-18_1300

| AssumptionID | Assumption | Source | Impact if Wrong |
|---|---|---|---|
| ASM-001 | Building Science Consultant rate of $165/hr CAD is representative of market rates for this role in Alberta | Professional_Staff_Rates.csv row R-27 (Basis: MARKET, Confidence: MEDIUM) | If actual rate differs, total changes by $12/hr x delta. At 12 hours, a +/- $15/hr variance = +/- $180. |
| ASM-002 | Architect (Project) rate of $145/hr CAD is representative of market rates for this role in Alberta | Professional_Staff_Rates.csv row R-04 (Basis: MARKET, Confidence: MEDIUM) | If actual rate differs, total changes by $4/hr x delta. At 4 hours, a +/- $15/hr variance = +/- $60. |
| ASM-003 | 12 hours is sufficient for the Building Science Consultant to produce the envelope strategy narrative including cross-discipline coordination | Level_of_Effort.csv row DEL-04-01/R-27 (Basis: PARAMETRIC) | If more hours needed (e.g., 16-20 hrs for complex envelope), cost increases by $165/hr per additional hour. |
| ASM-004 | 4 hours is sufficient for the Architect (Project) to provide envelope coordination input | Level_of_Effort.csv row DEL-04-01/R-04 (Basis: PARAMETRIC) | If more hours needed (e.g., 6-8 hrs), cost increases by $145/hr per additional hour. |
| ASM-005 | No additional roles are required to produce this deliverable | Level_of_Effort.csv (only 2 rows for DEL-04-01) | If additional roles needed (e.g., intermediate architect, mechanical input), cost would increase. However, mechanical/electrical coordination is costed in DEL-04-02 and DEL-04-03 respectively. |
| ASM-006 | The estimate covers proposal-stage effort only (producing the narrative for the RFP submission), not detailed design or construction-phase energy modeling | Scope boundary per decomposition: DEL-04-01 is a proposal narrative deliverable | If scope creep occurs into detailed energy modeling, additional hours/roles would be required. |
