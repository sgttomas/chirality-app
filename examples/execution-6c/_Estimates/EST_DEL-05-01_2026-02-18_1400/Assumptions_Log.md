# Assumptions Log: EST_DEL-05-01_2026-02-18_1400

| AssumptionID | Assumption | Source | Impact if Wrong | Confidence |
|---|---|---|---|---|
| A-001 | Main PSB building footprint is 18,000 sf (ground floor) per PP-05 | Assumed_Project_Parameters.csv PP-05 | If building is larger/smaller, all per-sf rates scale proportionally. +/-10% area = +/-$300-500k on building scope. | MEDIUM |
| A-002 | Cold storage building is 6,000 sf (60x100 ft) per PP-07 | Assumed_Project_Parameters.csv PP-07 (CONFIRMED) | Low risk; confirmed dimension. | HIGH |
| A-003 | Developed site area is 4.5 acres per PP-10 | Assumed_Project_Parameters.csv PP-10 | If site layout requires more development, civil costs increase. +/-1 acre = +/-$200-300k. | MEDIUM |
| A-004 | Main PSB split is approximately 40% office/admin (7,200 sf) and 60% apparatus/shop bays (10,800 sf) | Derived from functional program (4 fire bays + 4 PW bays + office/admin) | If split is different, MEP and interior costs shift (office areas cost more per sf than bays). | MEDIUM |
| A-005 | 8 overhead doors at 16x16 ft for main building (4 fire + 4 PW) per PP-13 and Addendum 03 | Assumed_Project_Parameters.csv PP-13 (DERIVED from CONFIRMED inputs) | Low risk; quantity is confirmed. | HIGH |
| A-006 | General requirements at 15% of base construction is appropriate for a DB municipal project | Industry standard range 12-18%; midpoint used | If actual GR is at 18% end, adds $261k to estimate. | MEDIUM |
| A-007 | Design fees at 9% blended rate of base construction is appropriate | Professional_Design_Fees.csv ranges + industry standard for DB | If actual fee is 12%, adds $261k. If 7%, reduces by $174k. | MEDIUM |
| A-008 | Bond premium rates: performance 1.5%, L&M 1.0% per FP-01/FP-02 | Fees_Permits_Insurance.csv market estimates | Actual quotes may vary by +/-25%. Impact: +/-$55k on bond line. | MEDIUM |
| A-009 | CCIP insurance at 2.0% per FP-03 | Fees_Permits_Insurance.csv market estimate | Rate depends on project risk profile and insurer. Range 1.5-2.5%. Impact: +/-$44k. | LOW |
| A-010 | Building permit fee at 0.75% of construction value per FP-06 | Fees_Permits_Insurance.csv; Penhold fee schedule TBD | Municipal fee schedules vary. Impact: +/-$22k. | LOW |
| A-011 | OI-004 resolved as $20,000 FF&E cash allowance on Additional Option 6 | BOE Section 4 recommendation; OPT-18 | If FF&E scope is expanded or moved to base cost, Schedule A structure changes. Low dollar impact at $20k. | HIGH |
| A-012 | GST rate is 5% (Alberta has no PST) | Current federal GST rate | Low risk; GST rate is stable. | HIGH |
| A-013 | No escalation applied (base year 2024) per BOE A-08 | BOE Assumptions Section | If construction extends beyond 2024, 3-5% annual escalation would add $300-500k per year. | MEDIUM |
| A-014 | Addenda 01-03 fully integrated per decomposition | Decomposition Section 4 | Addenda are confirmed integrated. | HIGH |
| A-015 | Pickled sand storage building excluded from base scope per Addendum 03 (CHG-003) | Addendum 03 | Low risk; confirmed excluded. | HIGH |
| A-016 | Fire protection sprinkler system included at $6/sf (MS-05) | Mechanical_System_Rates.csv MS-05 | May not be required by AHJ; if excluded, saves $108k. MS-05 confidence is LOW. | LOW |
| A-017 | Breathing air compressor system included at $55k (MS-08/EQ-08) | Equipment_Pricing.csv EQ-08 | Specialized system; actual pricing could vary significantly. | LOW |
| A-018 | Yard lighting assumes 12 poles per PP-20 | Assumed_Project_Parameters.csv PP-20 (ASSUMPTION; LOW confidence) | If more or fewer poles needed, Option 2 price changes proportionally (~$7,500 per pole). | LOW |
| A-019 | Utility tie-in allowance of $35,000 per UU-12 covers all services | Underground_Utility_Rates.csv UU-12 (ALLOWANCE) | Highly variable; depends on stub locations. Could range $25k-$50k per UU-12 range. | LOW |
| A-020 | Non-illuminated signage for Option 5 ($12k) rather than illuminated ($22k) | Decision D-006; Owner branding guidelines PENDING | If illuminated elected, adds $10k. | LOW |
