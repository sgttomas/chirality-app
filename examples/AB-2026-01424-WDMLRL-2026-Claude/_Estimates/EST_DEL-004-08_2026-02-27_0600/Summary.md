# Summary — EST_DEL-004-08_2026-02-27_0600

## Basis of Estimate

| Field | Value |
|---|---|
| **BASIS_OF_ESTIMATE** | PARAMETRIC |
| **Method** | Role-based level-of-effort (hours) x professional staff hourly rates |
| **Currency** | CAD |
| **Scope** | DEL-004-08 — Electrical Calculation Package |
| **Package** | PKG-004 — Electrical Design |
| **Pricing Model** | 4 roles from Level_of_Effort.csv, priced at rates from Professional_Staff_Rates.csv |

## Totals by Deliverable

| WBS_DeliverableID | Deliverable Name | Amount (CAD) |
|---|---|---|
| DEL-004-08 | Electrical Calculation Package | $13,050.00 |

## Totals by CBS

| CBS | Description | Amount (CAD) | % of Total |
|---|---|---|---|
| LABOUR-MGMT | Management (PM + Cost Estimator) | $1,530.00 | 11.7% |
| LABOUR-DESIGN | Design (Electrical Engineer + BIM Technician) | $11,520.00 | 88.3% |
| **TOTAL** | | **$13,050.00** | **100.0%** |

## Totals by Role

| RoleID | Role | Hours | Rate (CAD/hr) | Amount (CAD) | % of Total |
|---|---|---|---|---|---|
| R-01 | Project Manager | 6 | $165.00 | $990.00 | 7.6% |
| R-08 | Cost Estimator | 4 | $135.00 | $540.00 | 4.1% |
| R-13 | BIM Technician | 24 | $95.00 | $2,280.00 | 17.5% |
| R-16 | Electrical Engineer | 56 | $165.00 | $9,240.00 | 70.8% |
| **TOTAL** | | **90** | | **$13,050.00** | **100.0%** |

## Key Warnings and Coverage Gaps

1. **All pricing is PARAMETRIC.** Rates are from the Professional_Staff_Rates.csv (MEDIUM confidence). Hours are from Level_of_Effort.csv (PARAMETRIC basis). No quotes or historical data were used.

2. **Technical scope items (ITEM-001 through ITEM-026) are not independently priced.** The 24 technical calculation items extracted from Specification and Procedure are scope descriptors that map to the engineering effort captured in the 4 role-based line items (ITEM-027 through ITEM-030). The parametric model does not allocate hours to individual calculation sections.

3. **Multiple TBD data items exist in the deliverable scope:**
   - Crane manufacturer electrical data (FLA, voltage, phases) — affects ITEM-009
   - County welding equipment specifications — affects ITEM-008
   - Exhaust fan count and motor data from PKG-003 — affects ITEM-013
   - CEC edition adopted by Alberta — affects ITEM-015, ITEM-016
   - Service voltage confirmation from utility — affects ITEM-001
   These TBDs do not change the estimated professional effort (LOE-based), but they represent technical risks that could require additional effort if scope changes upon data receipt.

4. **No disbursements, overhead, or profit markup included.** This estimate covers professional labour hours only. Software licenses, printing, travel, and other disbursements are not included.

5. **Cross-check against fee-based model:** Professional_Design_Fees.csv suggests electrical design fee of 1.6% of construction value. At this rate, the $13,050 for the calculation package alone would imply a construction value baseline of ~$815,625 attributable to electrical systems, which is within a plausible range for a 13,000 sqft industrial maintenance shop. This provides a rough reasonableness check.

## Scope Coverage

| Category | Count |
|---|---|
| Deliverables in scope | 1 |
| Deliverables estimated | 1 |
| Items in takeoff (Items.csv) | 30 |
| Items with pricing (Detail.csv) | 4 (role-based lines covering all scope items) |
| Items with TBD pricing | 0 |
| Provenance completeness | 100% (all Detail.csv rows have SourceRef) |
