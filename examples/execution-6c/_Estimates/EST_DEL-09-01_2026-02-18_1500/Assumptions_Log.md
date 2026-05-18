# Assumptions Log

## Run: EST_DEL-09-01_2026-02-18_1500

---

| AssumptionID | Assumption | Source | Impact if Wrong |
|---|---|---|---|
| ASM-001 | Professional hourly rates in Professional_Staff_Rates.csv are representative of the actual DB firm's internal rates for Alberta 2024. | Professional_Staff_Rates.csv (Basis=MARKET, Confidence=MEDIUM, accuracy +/-20-30%) | Estimate could be off by 20-30% on unit rates. Rates are market-based parametric; actual firm rates may differ. |
| ASM-002 | Level of effort hours in Level_of_Effort.csv for DEL-09-01 (22 total hours across 3 roles) are representative of actual effort required to produce a risk register + quality management plan for this proposal scope. | Level_of_Effort.csv (Basis=PARAMETRIC, rows for DEL-09-01) | If actual effort differs significantly (e.g., more risk categories require analysis, or QMP requires more detailed procedures), hours could increase. LOE notes indicate ~4h PM time added for embedded QMP. |
| ASM-003 | The 6-week proposal preparation timeline (PP-04) is sufficient for all deliverable production including DEL-09-01. | Assumed_Project_Parameters.csv#PP-04 | If timeline is compressed, overtime or additional resources may be needed, increasing cost. Not directly priced but provides context for LOE reasonableness. |
| ASM-004 | No external specialist (e.g., environmental consultant, geotechnical engineer) hours are needed for DEL-09-01 risk register production; the PM + Quality Lead + CM team is sufficient to identify and document risks using available reference reports. | Level_of_Effort.csv (only 3 roles allocated to DEL-09-01) | If specialist input is needed for risk identification (e.g., R-28 Environmental Consultant or R-29 Geotechnical Engineer), additional hours and cost would apply. Currently these specialists are allocated to DEL-09-02 instead. |
