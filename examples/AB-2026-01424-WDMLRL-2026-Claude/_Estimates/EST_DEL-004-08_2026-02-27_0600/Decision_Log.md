# Decision Log — EST_DEL-004-08_2026-02-27_0600

| DecisionID | Decision | Rationale | Impact |
|---|---|---|---|
| DEC-001 | Pricing model: role-based LOE x hourly rate (not fee-percentage model) | Level_of_Effort.csv provides explicit hour allocations per role for DEL-004-08. This is more precise than the percentage-of-construction-value approach in Professional_Design_Fees.csv. The LOE model is directly traceable to the PARAMETRIC basis. | Primary pricing method; $13,050 total |
| DEC-002 | Technical scope items (ITEM-001 to ITEM-026) mapped to role-based effort lines rather than individually priced | The parametric LOE model allocates hours by role, not by calculation section. Attempting to sub-allocate hours across 24+ technical items without an allocation model would introduce fabricated precision. The role-hour lines fully cover all technical scope. | Detail.csv has 4 priced lines instead of 30; avoids double-counting |
| DEC-003 | CBS categories set to LABOUR-MGMT and LABOUR-DESIGN | No material, equipment, or subcontract costs are applicable to a professional calculation package. CBS categories reflect the nature of the work: management labour (PM, Cost Estimator) and design labour (Electrical Engineer, BIM Technician). | WBS_CBS_Matrix reflects 2 CBS categories |
| DEC-004 | Professional_Design_Fees.csv used as cross-check only, not primary pricing | Fee-percentage model (DF-04: 1.6% of construction value) requires a construction value input not available in PRICE_SOURCES. LOE-based model is self-contained and directly supported by the two primary pricing sources. Fee model provides reasonableness validation only. | No impact on totals; noted in Summary.md |
| DEC-005 | Scope resolved to single deliverable DEL-004-08 only | SCOPE parameter specifies DEL-004-08. No package-level rollup or multi-deliverable aggregation required. | 1 deliverable estimated |
| DEC-006 | FALLBACK_POLICY = ALLOW_PARAMETRIC: not invoked | All items were priceable via primary PARAMETRIC method. No fallback to allowance was needed. | No impact |
| DEC-007 | UPDATE_LATEST_POINTER = FALSE: no pointer file modified | Per brief instruction. | No _LATEST.md file created or modified |
| DEC-008 | Rounding = NONE (default) | No rounding instruction provided in brief. Amounts reported at full cent precision. | Amounts show 2 decimal places |
