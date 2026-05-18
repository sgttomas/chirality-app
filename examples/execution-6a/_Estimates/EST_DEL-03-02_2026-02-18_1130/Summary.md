# Estimate Summary: DEL-03-02 Grading, Earthworks, Drainage & Stormwater

## Run Identity

| Field | Value |
|---|---|
| Snapshot | EST_DEL-03-02_2026-02-18_1130 |
| Deliverable | DEL-03-02 -- Grading, Earthworks, Drainage & Stormwater |
| Package | PKG-003 -- Site & Civil Works |
| Basis of Estimate | RATE_TABLE |
| Currency | CAD |
| RUN_STATUS | WARNINGS |

## Estimate Total

| | Amount (CAD) |
|---|---|
| **DEL-03-02 Total** | **$472,062** |

## Totals by CBS Category

| CBS | Description | Amount (CAD) | % of Total | Lines |
|---|---|---|---|---|
| 03-02-EW | Earthworks (Cut/Fill/Pad Prep/Compaction) | $178,038 | 37.7% | 5 |
| 03-02-FIN | Final Grading and Restoration | $110,000 | 23.3% | 1 |
| 03-02-DRN | Drainage and Stormwater | $74,500 | 15.8% | 3 |
| 03-02-CLR | Clearing and Stripping | $32,010 | 6.8% | 2 |
| 03-02-GEO | Geotechnical Services | $32,000 | 6.8% | 1 |
| 03-02-ESC | Erosion and Sediment Control | $22,000 | 4.7% | 1 |
| 03-02-SRV | Construction Survey | $12,000 | 2.5% | 1 |
| 03-02-DSN | Civil Design Fees | $11,514 | 2.4% | 1 |
| **TOTAL** | | **$472,062** | **100.0%** | **15** |

## BasisOfEstimate_Used

All 15 line items are priced using Method=RATE_TABLE, derived from:
- **Earthwork_Civil_Rates.csv** (11 rate items EC-01 through EC-11) -- primary rate source for 14 construction lines
- **Professional_Design_Fees.csv** (DF-02, 2.5% of construction subtotal) -- 1 design fee line
- **Assumed_Project_Parameters.csv** -- quantity basis for area/volume derivations
- **Construction_Labour_Rates.csv** -- cross-reference validation only (not used for pricing)

No fallback methods were used. ALLOW_MIXED_METHODS=FALSE is satisfied.

## Key Quantity Assumptions (Driving Cost Sensitivity)

| Assumption | Assumed Value | Affected Amount | % of Total |
|---|---|---|---|
| Cut volume (ASM-001) | 3,000 m3 | $45,000 | 9.5% |
| Fill import (ASM-002) | 2,000 m3 | $60,000 | 12.7% |
| Pond excavation (ASM-005) | 2,500 m3 | $37,500 | 7.9% |
| Seeding area (ASM-008) | 10,000 m2 | $110,000 | 23.3% |
| **Total assumption-driven** | | **$252,500** | **53.5%** |

Over half of the estimate is driven by quantity assumptions that require resolution through design development and/or quantity takeoff from TPN46 drawings.

## Comparison to Parametric Benchmark

| Benchmark | Value | Source |
|---|---|---|
| PP-23 (parametric site/civil value) | $1,800,000 | Assumed_Project_Parameters.csv |
| DEL-03-02 estimate | $472,062 | This snapshot |
| DEL-03-02 as % of PP-23 | 26.2% | Derived |

DEL-03-02 (earthworks/grading/drainage) at ~26% of total site/civil parametric value is reasonable. The remaining ~74% would be distributed across DEL-03-01 (site plan/layout -- minimal construction cost), DEL-03-03 (pavements/aggregate/aprons -- typically the largest site/civil cost), DEL-03-04 (utilities), and DEL-03-05 (environmental compliance).

## Key Warnings

1. **Cut/fill quantities are assumptions** (Datasheet item B-001). Lines L-003 and L-004 ($105,000 combined, 22% of total) are LOW confidence. Civil engineer must extract quantities from TPN46 or post-award survey.

2. **Stormwater pond sizing criteria TBD** (REQ-3212 / item F-001). Lines L-010 and L-011 ($52,500, 11% of total) are LOW confidence. Design storm return period, pond capacity, and outlet flow rate must be determined per municipal standards.

3. **AEPA Water Act approval PENDING** (external gate). Earthwork near waterway may require additional mitigation not currently priced. Physical mitigation costs would affect DEL-03-02; consultant costs belong to DEL-03-05.

4. **Geotechnical report is 5 years old** (Feb 2021). If conditions have changed, supplemental investigation may add $25,000-$40,000 beyond the $32,000 geotech services line.

## Blockers (from Dependency Analysis)

| Blocker | Description | Estimate Impact |
|---|---|---|
| Cut/fill quantities not extracted | Datasheet B-001; depends on DEL-03-01 site plan | 22% of total at LOW confidence |
| Pond sizing criteria TBD | REQ-3212/F-001; depends on DEL-03-05 approvals | 11% of total at LOW confidence |
