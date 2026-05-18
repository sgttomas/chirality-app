# Assumptions Log: EST_DEL-05-03_2026-02-18_1430

## Assumptions Active in This Run

| AssumptionID | Assumption | Source | Impact if Wrong | Confidence |
|---|---|---|---|---|
| A-001 | Professional hourly rates are internal DB firm rates (not external consultant fees) | BOE A-01; Professional_Staff_Rates.csv Basis=MARKET | If external consultants used, rates may be higher (potentially +20-50%) | MEDIUM |
| A-002 | PM 12 hours and Estimator Senior 8 hours are adequate for the narrative scope including: allowances, exclusions, addenda impacts, value alternatives (SOW-028), and cross-deliverable coordination with 6+ upstream interfaces | Level_of_Effort.csv (PARAMETRIC basis); BOE Section 4 cost ownership rules | If actual effort exceeds LOE, production cost increases proportionally. 20-30% variance expected per INDEX.md Data Quality Statement. | MEDIUM |
| A-003 | OI-004 (FF&E) will be resolved as $20,000 cash allowance as Additional Option 6 per BOE recommendation | BOE A-04; upstream estimates (DEL-05-01 L-035, DEL-05-02 L-170) | If different FF&E treatment is decided, narrative must be updated. Production effort (hours) unlikely to change materially. | MEDIUM |
| A-004 | Value alternatives analysis (SOW-028) is within PM's scope and does not require separate discipline engineering hours | BOE Section 4 cost ownership rules; Level_of_Effort.csv allocation | If value alternatives require significant engineering analysis (e.g., alternative structural systems), additional discipline hours may be needed | MEDIUM |
| A-005 | Narrative content can be authored within 6-week proposal preparation timeline (PP-04) without schedule pressure premium | Assumed_Project_Parameters.csv PP-04 | If timeline is compressed, parallel work overhead may increase hours | MEDIUM |
| A-006 | Base year 2024 rates apply with no escalation | BOE A-08 | If preparation extends beyond 2024, rates may escalate | MEDIUM |
