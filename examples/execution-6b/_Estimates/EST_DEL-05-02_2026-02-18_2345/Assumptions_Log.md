# Assumptions_Log.md -- EST_DEL-05-02_2026-02-18_2345

| AssumptionID | Assumption | Source | Impact if Wrong |
|---|---|---|---|
| ASM-001 | The structural durability narrative is authored entirely by the Structural Engineer (Senior) with no supporting production roles required | Level_of_Effort.csv assigns only R-09 to DEL-05-02 | If intermediate structural engineer or CAD support is needed, hours and cost would increase. At R-10 rate ($125/hr), each additional hour adds $125. |
| ASM-002 | 8 hours is sufficient for the structural durability narrative scope (corrosion, freeze-thaw, foundation, slab, inspection access) | Level_of_Effort.csv row DEL-05-02/R-09 = 8 hr; Basis = PARAMETRIC | If the narrative requires deeper technical analysis or additional coordination cycles, hours could increase. Each additional senior structural hour adds $155. |
| ASM-003 | The R-09 hourly rate of $155/hr CAD reflects the actual rate for the structural engineer on this project | Professional_Staff_Rates.csv row R-09; Basis = MARKET; Confidence = MEDIUM | If the actual contracted rate differs from the MARKET assumption, the amount changes proportionally. A $10/hr variance on 8 hours = $80 impact. |
| ASM-004 | No additional geotechnical investigation is required to inform the structural durability narrative | DEC-013 in Decomposition; Level_of_Effort.csv does not include R-29 (Geotechnical Engineer) hours for DEL-05-02 | If the existing 2021 geotech report is deemed insufficient for durability claims, additional geotechnical review hours would be needed (R-29 at $155/hr). |
