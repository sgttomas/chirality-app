# Assumptions Log — EST_DEL-01-05_2026-02-18_0000

| AssumptionID | Assumption | Source / Basis | Impact if Wrong | Affected Lines |
|---|---|---|---|---|
| ASM-001 | Construction duration is 18 months (NTP to Substantial Performance) | Assumed_Project_Parameters.csv PP-01; Confidence=MEDIUM | If duration is shorter or longer, PM and Admin hours would scale proportionally. A 12-month duration could reduce hours by ~33%; a 24-month duration could increase by ~33%. | L-01, L-02 |
| ASM-002 | Meetings are biweekly (approximately 36 meetings over 18 months) | Level_of_Effort.csv Notes for DEL-01-05 R-02: "Biweekly meetings (2h x 36 = 72h)" | If meeting frequency changes to weekly, PM meeting hours would approximately double (72h -> 144h). If monthly, hours would halve. | L-01 |
| ASM-003 | Meeting duration is 2 hours per meeting | Level_of_Effort.csv Notes for DEL-01-05 R-02 | Longer or shorter meetings directly affect PM hours. | L-01 |
| ASM-004 | Change control admin effort is 18 hours over full project duration | Level_of_Effort.csv Notes for DEL-01-05 R-02: "change control admin (18h)" | If the project has higher change order volume than typical, admin hours could increase. | L-01 |
| ASM-005 | Admin/document control hours (50h) cover minutes, RFI log, submittal tracking, and change order documentation for the full project duration | Level_of_Effort.csv DEL-01-05 R-24 (50h) | If documentation volume is higher than anticipated (e.g., complex project with many RFIs), hours could be insufficient. | L-02 |
| ASM-006 | Rates are market-based and appropriate for Alberta professional services (2026) | Professional_Staff_Rates.csv Basis=MARKET; Confidence=MEDIUM | If actual market rates differ, total cost would scale proportionally. | L-01, L-02 |
| ASM-007 | No document management system (DMS) costs are included; it is assumed the DB uses existing internal systems or the cost is carried elsewhere | DEC-EST-003 (Decision Log) | If DMS licensing/setup costs are expected in this deliverable, total could increase. Amount is TBD. | N/A |
| ASM-008 | No overhead, burden, or profit is included in the bare labour rates | DEC-EST-004 (Decision Log); Professional_Staff_Rates.csv provides bare rates only | If burdened rates are required, total cost could increase by 30-100% depending on the multiplier. | L-01, L-02 |
