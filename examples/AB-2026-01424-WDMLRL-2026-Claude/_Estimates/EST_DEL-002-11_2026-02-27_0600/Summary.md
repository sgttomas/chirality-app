# Summary — EST_DEL-002-11_2026-02-27_0600

## Basis of Estimate Used

| Field | Value |
|---|---|
| BASIS_OF_ESTIMATE | PARAMETRIC |
| Method applied | PARAMETRIC for all 4 priced lines |
| Pricing model | Hours (from Level_of_Effort.csv) x Hourly Rates (from Professional_Staff_Rates.csv) |
| Currency | CAD |
| Fallback used | No — all items priced from primary PARAMETRIC sources |
| Mixed methods | No — all lines are PARAMETRIC |

## Totals by Package / Deliverable

| WBS_PackageID | WBS_DeliverableID | Amount (CAD) | Lines | Hours |
|---|---|---|---|---|
| PKG-002 | DEL-002-11 | **$11,855** | 4 | 80 |

## Totals by CBS

| CBS | Amount (CAD) | Lines |
|---|---|---|
| Professional Services — Management | $1,530 | 2 |
| Professional Services — Design | $10,325 | 2 |
| **TOTAL** | **$11,855** | **4** |

## Totals by Role

| Role | Hours | Rate (CAD/hr) | Amount (CAD) | % of Total |
|---|---|---|---|---|
| R-14 Structural Engineer | 49 | $170 | $8,330 | 70.3% |
| R-13 BIM Technician | 21 | $95 | $1,995 | 16.8% |
| R-01 Project Manager | 6 | $165 | $990 | 8.4% |
| R-08 Cost Estimator | 4 | $135 | $540 | 4.6% |
| **TOTAL** | **80** | — | **$11,855** | **100%** |

## Key Warnings and Coverage Gaps

1. **Scope is professional design services only.** DEL-002-11 is a design package deliverable. The estimate covers professional engineering, drafting, management, and estimating hours. Foundation construction costs (SOW-0023, DEL-010-01, PKG-010) are explicitly excluded.

2. **Variable-price nature.** The foundation design is subject to re-pricing post-geotechnical investigation (RFP §4.8.2). The hours estimated here are for the proposal-phase design on assumed normal ground conditions. If geotechnical findings require significant redesign, additional engineering hours may be needed. This risk is flagged in Risk_Register.md.

3. **Peer review hours are embedded.** The LOE for R-14 Structural Engineer (49 hr) is assumed to include time for peer review coordination (Procedure Step 2.7). A separate peer reviewer's hours are not broken out in Level_of_Effort.csv. See Assumptions_Log.md ASM-003.

4. **Geotechnical Engineer hours not included.** DEL-002-11 does not include geotechnical investigation (DEL-008-01, PKG-008). However, the Structural Engineer's coordination with the geotechnical report is included within the R-14 hours.

5. **Design fee cross-check.** Professional_Design_Fees.csv suggests structural design fees of 1.2%–2.5% of construction value (recommended 1.8%). Without a construction value for the variable-price foundation scope, this cross-check cannot be completed numerically. See Decision_Log.md DEC-002.

6. **Artifact-level items (ITEM-005 through ITEM-014) are tracking items only.** These are listed in Items.csv for completeness and traceability to Specification/Procedure requirements, but their cost is absorbed within the four role-based line items (ITEM-001 through ITEM-004). They carry $0 in Detail.csv and are not priced separately.
