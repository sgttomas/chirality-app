# Decision Log — EST_DEL-021-05_2026-02-27_0834

## Decisions Applied During This Run

| ID | Decision | Rationale | Impact |
|---|---|---|---|
| DEC-001 | Activity-to-role mapping adopted for pricing | Level_of_Effort.csv provides hours by role, not by activity. Each of the 8 role-hour allocations was mapped to the most representative activity item from the 15-item takeoff. | Items.csv has 15 rows; Detail.csv has 8 rows. No pricing information is lost — all hours and rates are accounted for. |
| DEC-002 | All 8 LOE roles included in estimate | All 8 roles listed in Level_of_Effort.csv for DEL-021-05 are included. No roles were excluded. | Full labour coverage. |
| DEC-003 | Fees_Permits_Insurance.csv items excluded from DEL-021-05 scope | FP-01 through FP-05 cover bonding premiums, insurance premiums, and permit fees — these are pre-construction procurement items, not warranty administration costs. | No fee/permit/insurance items priced under DEL-021-05. |
| DEC-004 | WARRANTY_REMEDIATION_COSTS excluded | Actual deficiency rectification costs (materials, trades, subcontractors) are borne by the Contractor per RFP §2.10.7. These are not within the scope of DEL-021-05's administrative deliverable. | Estimate reflects administration cost only. |
| DEC-005 | FALLBACK_POLICY not invoked | All items were priceable using the PARAMETRIC basis. No fallback to ALLOWANCE or other methods was required. | 100% PARAMETRIC consistency. |
| DEC-006 | UPDATE_LATEST_POINTER = FALSE respected | No pointer file was modified. | _LATEST.md unchanged. |
| DEC-007 | Rounding defaulted to NONE | No rounding directive provided; NONE applied per protocol default. | Amounts reflect exact calculations. |
