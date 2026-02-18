# Estimate Summary -- DEL-01-04 Schedule A Pricing Summary

**RunID:** EST_DEL-01-04_2026-02-18_2359
**Basis of Estimate:** RATE_TABLE (with PARAMETRIC and ALLOWANCE fallback per ALLOW_MIXED_METHODS=TRUE)
**Currency:** CAD
**Rounding:** DOLLAR
**Deliverable:** DEL-01-04 -- Appendix H Schedule A Pricing Summary
**Package:** PKG-001 -- Proposal Compliance, Commercial & Team Qualifications

---

## Schedule A Pricing Structure

### Line 1-1: Base Contract Price

| CBS | Description | Amount (CAD) |
|---|---|---:|
| CON.STR | Structural/Concrete | $896,000 |
| CON.ENV | Building Envelope | $808,000 |
| CON.INT | Interior Architectural | $280,000 |
| CON.MEC | Mechanical Systems | $942,000 |
| CON.ELC | Electrical Systems | $697,000 |
| CON.CIV | Earthwork/Civil | $552,000 |
| CON.PAV | Paving/Surfacing | $651,000 |
| CON.UTL | Underground Utilities | $210,000 |
| CON.EQP | Equipment/Specialty | $1,000,000 |
| CON.GR | General Requirements | $1,291,000 |
| **SUBTOTAL** | **Base Contract (excl. taxes)** | **$7,327,000** |

### Lines 1-2 through 1-7: Additional Options

| Line | Option | Amount (CAD) |
|---|---|---:|
| 1-2 | Option 1 -- Wash Bay | $123,000 |
| 1-3 | Option 2 -- Yard Lighting | $106,000 |
| 1-4 | Option 3 -- Access Control | $45,000 |
| 1-5 | Option 4 -- Security/Cameras | $55,000 |
| 1-6 | Option 5 -- Signage | $34,000 |
| 1-7 | Option 6 -- FF&E (cash allowance) | $20,000 |
| **SUBTOTAL** | **All Options** | **$383,000** |

### Total Construction Pricing Content

| Component | Amount (CAD) |
|---|---:|
| Base Contract (Line 1-1) | $7,327,000 |
| Additional Options (Lines 1-2 to 1-7) | $383,000 |
| **Total Construction Content** | **$7,710,000** |

### Production Cost (Group A -- DEL-01-04 compilation effort)

| Role | Hours | Rate | Amount (CAD) |
|---|---:|---:|---:|
| Senior Estimator (R-18) | 40 | $145/hr | $5,800 |
| Intermediate Estimator (R-19) | 24 | $115/hr | $2,760 |
| Project Manager (R-02) | 8 | $175/hr | $1,400 |
| **SUBTOTAL** | **72 hrs** | | **$9,960** |

### Grand Total (All Groups)

| Group | Amount (CAD) |
|---|---:|
| Group A -- Production costs | $9,960 |
| Group B -- Construction pricing content | $7,710,000 |
| **GRAND TOTAL** | **$7,719,960** |

---

## Parametric Cross-Check

| Benchmark | $/sf | Source | Status |
|---|---:|---|---|
| Base construction / main PSB (18,000 sf) | $407/sf | Computed | PASS -- within PB-04 range ($320-$420) |
| Base construction / total GFA (24,000 sf) | $305/sf | Computed | PASS -- within PB-03 range ($280-$380) |
| Fire station parametric (PB-04) | $370/sf | Parametric_Building_Rates.csv | Benchmark |
| Combined PSB facility parametric (PB-07) | $415/sf | Parametric_Building_Rates.csv | Benchmark |
| PB-04 x 18,000 sf | $6,660,000 | Parametric check | Base ($7,327k) is 10% above PB-04 benchmark -- reasonable given GR inclusion |

**Cross-check assessment:** The base construction estimate of $7,327,000 falls within the expected range when compared to parametric benchmarks. At $407/sf against the main PSB footprint, it is slightly above the PB-04 fire station rate of $370/sf, which is expected because the base includes General Requirements ($1.291M = design fees, bonds, insurance, permits) that are additive to direct construction costs. Stripping GR, the direct construction cost is $6,036,000 / 18,000 sf = $335/sf, which aligns well with the PB-03 institutional rate of $330/sf.

**Gap to PP-25 ($12M):** The bottom-up estimate of $7.327M base is 61% of the PP-25 rough-order-of-magnitude $12M. The gap represents: (a) DB fee/profit margin (typically 8-12%), (b) construction contingency (typically 5-10%), (c) escalation (2-3% over 18-month construction), and (d) PP-25 was acknowledged as LOW confidence / rough order of magnitude. The $12M target price would imply approximately 64% markup over direct costs, which would include ~$870k DB fee (12%) + ~$600k contingency (8%) + ~$220k escalation (3%) + remaining conservatism in PP-25 order-of-magnitude estimate. These commercial decisions (margin, contingency, escalation) are outside the scope of this estimate and belong to the commercial team's pricing strategy.

---

## Key Warnings

1. **Mixed methods active:** Detail.csv contains RATE_TABLE (primary), PARAMETRIC (cold storage PEMB), and ALLOWANCE (workshop equipment, municipal tie-ins, utility connection fees, FF&E) methods.
2. **Fire protection (B-420):** $108,000 at LOW confidence -- sprinkler requirement depends on AHJ determination; may not be required for this occupancy type.
3. **Generator system (B-530):** $150,000 at LOW confidence -- actual cost depends on final load calculations and equipment selection.
4. **Design fees (B-1100):** Computed as percentage of construction scope; includes markup for coordination and management. Individual discipline fee allocations are approximate.
5. **CCIP insurance (B-1130):** $240,000 at LOW confidence -- actual rate depends on project risk profile and insurer.
6. **DB margin, contingency, and escalation NOT included:** This estimate represents direct costs + general requirements. Commercial markup is a business decision outside ESTIMATING scope.
7. **Quantities are parametric estimates** based on Assumed_Project_Parameters.csv and reasonable assumptions for a building of this type and size. Actual quantities will be determined during detailed design.

---

## Blocker Summary

| DependencyID | Target | Issue | Impact |
|---|---|---|---|
| DEP-0104-E001 | DEL-01-05 (Schedule B) | Upstream prerequisite -- Schedule B provides values that populate Schedule A | Schedule A values computed independently from rate tables; reconciliation with Schedule B required |
| DEP-0104-E002 | DEL-01-06 (Pricing Narrative) | Upstream prerequisite -- assumptions must be documented | Assumptions captured in this estimate run; pricing narrative coordination required |
| DEP-0104-E003 | DEL-01-03 (Bonding/Insurance) | Bond and CCIP costs must be calculated | Bond/CCIP costs computed from Fees_Permits_Insurance.csv; DEL-01-03 estimate should reconcile |
| DEP-0104-E004 | RFP Appendix H template | Form template required | Template referenced but not modified by this estimate |

No hard blockers prevent this estimate from being meaningful. All upstream data was available from price sources.
