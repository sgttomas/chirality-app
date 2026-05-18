# Assumptions Log

**RunID:** EST_DEL-02-03_2026-02-18_2100

| AssumptionID | Assumption | Source / Basis | Impact if Wrong |
|---|---|---|---|
| ASM-001 | Level of effort hours (16 Sr + 8 Int = 24 total) are sufficient to produce a complete structural concept narrative for a combined Fire Hall + Public Works + Cold Storage facility | Level_of_Effort.csv (PARAMETRIC basis, MEDIUM confidence) | If actual effort exceeds 24 hours, the estimate understates cost. A 50% overrun would add $1,740 CAD. |
| ASM-002 | Hourly rates ($155 Sr, $125 Int) reflect market rates for Alberta structural engineering professionals on a municipal Design-Build proposal | Professional_Staff_Rates.csv (MARKET basis, MEDIUM confidence) | If firm-specific rates differ by +/-15%, total impact is +/-$522. |
| ASM-003 | No additional disciplines (e.g., geotechnical engineer, CAD technician) are required to produce this narrative deliverable | Level_of_Effort.csv scoping -- only R-09 and R-10 rows exist for DEL-02-03 | If geotech or CAD support hours are needed, they are not captured here. Geotechnical review is separately captured under DEL-10-02. |
| ASM-004 | The structural concept narrative is a text-only deliverable (no drawings); CAD/BIM hours are not included | Decomposition: DEL-02-03 Type = "Design / Narrative"; no anticipated drawing artifacts | If sketches or structural diagrams are required, CAD technician hours (R-06 @ $95/hr) would need to be added. |
| ASM-005 | Foundation approach is based solely on the existing 2021 geotechnical report (per DEC-013); no additional geotechnical investigation costs are included | Decomposition DEC-013; Dependencies.csv DEP-02-03-E007 | If additional investigation is later required, a separate cost item would be needed (not in this deliverable's scope). |
