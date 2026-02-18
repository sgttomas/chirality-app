# Decision Log: EST_DEL-01-03_2026-02-18_1500

| DecisionID | Decision | Rationale | Source |
|---|---|---|---|
| D-001 | Use base construction value ($9,863,000) from DEL-05-01 as contract value basis for bond/insurance percentage calculations | BOE cost ownership rules state bond premium = percentage of contract price; DEL-05-01 Schedule A provides the most current base construction figure excluding GST and Additional Options | EST_DEL-05-01_2026-02-18_1400/Summary.md; BOE Section 4 PKG-01 |
| D-002 | Exclude GST and Additional Options from the bond/insurance percentage basis | Standard bonding practice in Alberta applies bond premiums to base construction value before tax; options are separate scope | Industry standard; Fees_Permits_Insurance.csv notes |
| D-003 | Apply ALLOWANCE method for bond/insurance premium lines (6 of 9 lines) | Premium rates from Fees_Permits_Insurance.csv are percentage-based market estimates, not firm quotes; FALLBACK_POLICY=ALLOW_ALLOWANCE authorizes this | BOE Section 4 PKG-01 table; brief FALLBACK_POLICY |
| D-004 | Carry surety broker fee ($3,500) as a separate line item rather than embedding in bond premium | FP-19 notes fee "sometimes embedded in bond premium"; separating provides transparency for AGGREGATION | Fees_Permits_Insurance.csv FP-19 Notes field |
| D-005 | Use recommended (midpoint) rates from Fees_Permits_Insurance.csv rather than min or max | Recommended rates represent the pricing source author's best estimate; deviating would require external justification not available | Fees_Permits_Insurance.csv RecommendedRate column |
| D-006 | Classify CBS as MGMT/LEGAL/ADMIN for production lines and BOND/INS for premium lines | Deterministic CBS mapping rule documented in Run_Context.md; separates production effort from premium costs for AGGREGATION clarity | Run_Context.md CBS mapping rule |
