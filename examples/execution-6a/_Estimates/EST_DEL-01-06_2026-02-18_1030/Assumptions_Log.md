# Assumptions Log -- EST_DEL-01-06_2026-02-18_1030

## Active Assumptions

| AssumptionID | Description | Source | Impact | Risk if Wrong |
|---|---|---|---|---|
| ASM-0106-001 | Construction duration is 18 months (NTP to Substantial Performance). This drives the Site Superintendent's 1,440-hour estimate. | Assumed_Project_Parameters.csv PP-01 (Confidence: MEDIUM) | HIGH -- a 1-month change in duration shifts Site Superintendent cost by approximately $23,400 CAD (4.33 wk x 40 hr/wk x 0.8 utilization x $135/hr). | Schedule extension or compression would proportionally change the single largest line item. |
| ASM-0106-002 | Site Superintendent utilization is 80% of full-time equivalent (40 hrs/wk). | Level_of_Effort.csv DEL-01-06/R-16 notes | MEDIUM -- 20% reduction from gross hours accounts for non-productive time, weather days, and administrative overhead. | If full-time (100%) is required, add ~360 hours ($48,600 CAD). If utilization is lower (e.g., 60%), reduce by ~360 hours. |
| ASM-0106-003 | Construction Manager visits are periodic at approximately 3.5 hours per week over the construction duration. | Level_of_Effort.csv DEL-01-06/R-15 notes | LOW -- this is a small portion of total cost ($9,300 of $203,700). | Minimal financial impact even if doubled. |
| ASM-0106-004 | Hourly rates in Professional_Staff_Rates.csv are current market rates for Alberta and appropriate for this project. | Professional_Staff_Rates.csv (Basis: MARKET; Confidence: MEDIUM) | MEDIUM -- rates are the unit price basis for all labor. | Rate escalation or regional premium could shift total; $10/hr change on Site Superintendent = $14,400 CAD impact. |
| ASM-0106-005 | Non-labor site costs (temporary facilities, fencing, cleaning) are material cost drivers that are not yet quantifiable from available sources. | Brief cost drivers field; Datasheet.md attributes | UNKNOWN -- amounts are TBD; could range from minor ($10,000-$20,000) to significant ($50,000+) depending on site logistics complexity and duration. | Understatement of total DEL-01-06 cost until these are priced. |
