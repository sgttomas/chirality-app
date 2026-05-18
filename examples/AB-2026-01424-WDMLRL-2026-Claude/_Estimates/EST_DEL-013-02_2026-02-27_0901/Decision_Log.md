# Decision Log — EST_DEL-013-02_2026-02-27_0901

| DecisionID | Decision | Rationale | Impact |
|---|---|---|---|
| D-001 | Used MS-03 ALLOWANCE rate ($13,500) for equipment despite BASIS_OF_ESTIMATE=PARAMETRIC | ALLOW_MIXED_METHODS=TRUE; MS-03 is the only rate source for this equipment class; FALLBACK_POLICY=ALLOW_PARAMETRIC permits this | Method=ALLOWANCE for L-001; flagged in QA |
| D-002 | Allocated 35% of whole-building ductwork cost to DEL-013-02 air exchanger distribution | Air exchanger provides general supply/return ventilation but shares distribution infrastructure with heating (DEL-013-01) and makeup air (DEL-013-03); 35% reflects proportional share for ventilation distribution | L-005 amount = $25,368; sensitivity noted in Summary W-002 |
| D-003 | Estimated HVAC trade labour at 80 hours for ductwork installation | Parametric basis: 2 sheet metal tradespeople x 5 working days x 8 hrs/day for a single-deliverable ductwork scope in a ~13,000 sqft building | L-023 amount = $7,296 |
| D-004 | Estimated general labourer at 24 hours | Parametric basis: 1 labourer x 3 working days x 8 hrs/day for site support during mechanical installation | L-024 amount = $1,562.40 |
| D-005 | Included fire stopping (L-007) despite requirement being TBD | Prudent to include per standard code practice; amount is small ($700) and removable if wall fire ratings do not trigger requirement | L-007 amount = $700 |
| D-006 | Included vibration isolation (L-008) despite requirement being TBD per Specification REQ-016 | Standard practice for large industrial HRV/ERV; Specification REQ-016 flags it as likely required | L-008 amount = $2,000 |
| D-007 | Used commissioning agent (R-23) and controls specialist (R-24) rates for commissioning line | Professional_Staff_Rates.csv provides these rates; 16 hrs Cx agent + 8 hrs controls specialist is parametric estimate for single-system commissioning | L-013 amount = $3,800 |
| D-008 | Did not include training (Procedure Step 5.4) as a separate priced line | Training requirement is TBD per Procedure; included implicitly in closeout documentation allowance (L-016) | No separate line; noted in Assumptions |
| D-009 | Did not include warranty registration as a separate priced line | Warranty registration (Procedure Step 5.5) is administrative; cost is negligible and included in closeout allowance | No separate line |
| D-010 | UPDATE_LATEST_POINTER=FALSE — did not modify pointer files | Per run brief instruction | No pointer file created or modified |
