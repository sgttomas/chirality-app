# Estimate Summary — EST_DEL-03-03_2026-02-18_1200

## Deliverable

| Field | Value |
|-------|-------|
| DeliverableID | DEL-03-03 |
| Name | Pavements, Aggregate Yard Areas & Concrete Aprons |
| Package | PKG-003 — Site & Civil Works |
| Scope Items | SOW-0107 (sitework surfacing), SOW-0108 (concrete aprons) |

## Basis of Estimate

| Field | Value |
|-------|-------|
| BASIS_OF_ESTIMATE | RATE_TABLE |
| Primary Rate Source | Paving_Surfacing_Rates.csv (PS-01 through PS-09) |
| Quantity Source | Assumed_Project_Parameters.csv (parametric areas pre-design) |
| Currency | CAD |
| Rounding | DOLLAR |
| Fallback Policy | STRICT (no fallback pricing allowed) |
| Mixed Methods | FALSE (all lines are RATE_TABLE) |

## Estimate Total

| | Amount (CAD) |
|---|---:|
| **DEL-03-03 Total** | **$896,380** |

## Breakdown by CBS Code

| CBS | Description | Amount (CAD) | % of Total | Lines |
|-----|------------|------------:|----------:|------:|
| 03.03.ASP-HD | Heavy duty asphalt (Zone A) + geogrid | $200,000 | 22.3% | 2 |
| 03.03.ASP-LD | Light duty asphalt (Zone B) + geofabric | $208,000 | 23.2% | 2 |
| 03.03.AGG | Aggregate surfacing (Zone C) + geofabric | $390,000 | 43.5% | 3 |
| 03.03.CONC | Concrete (aprons + curb/gutter + sidewalk) | $83,230 | 9.3% | 4 |
| 03.03.MARK | Pavement markings + accessible signage | $3,150 | 0.4% | 2 |
| 03.03.SITE | Bollards | $12,000 | 1.3% | 1 |
| **TOTAL** | | **$896,380** | **100.0%** | **14** |

## Cost Driver Analysis

The three largest cost categories are:

1. **Aggregate surfacing (Zone C) — $390,000 (43.5%):** The largest cost driver is aggregate surfacing for the heavy equipment yard areas at 6,000 m2 x 300mm depth (two lifts at $30/m2 each) plus geofabric separation. The 1.5-acre yard area is the largest surfaced zone on site. This area is a significant cost because heavy equipment yard requires double-depth aggregate.

2. **Light duty asphalt (Zone B) — $208,000 (23.2%):** Parking area at 3,200 m2 at $60/m2 plus geofabric allowance. Driven by the 40-stall parking requirement plus access aisles.

3. **Heavy duty asphalt (Zone A) — $200,000 (22.3%):** Fire apparatus routing at 2,000 m2 at $92/m2 plus geogrid allowance. Despite the smaller area, the higher unit rate for fire-truck-rated pavement makes this a significant cost.

## Key Warnings

1. **QUANTITIES_ASSUMED:** All area quantities are parametric (derived from Assumed_Project_Parameters.csv), not measured from a site plan. Quantities should be updated when DEL-03-01 site plan is complete.

2. **CONCRETE_APRON_DIMENSIONS_TBD:** Apron dimensions (4.88m x 8.0m assumed per door) depend on architectural overhead door locations from PKG-002 and PKG-004 drawings, which are not yet available.

3. **AGGREGATE_DEPTH_TBD:** The 300mm aggregate depth is an assumption from Specification REQ-03-03-05, pending design confirmation from the pavement design report.

4. **GEOSYNTHETICS_CONSERVATIVE:** $62,000 in geosynthetic allowances (L-012, L-013, L-014) may overlap with "includes base prep" notes in PS-01 and PS-02. These lines can be removed if confirmed to be already included.

## Scope Exclusions (per cost ownership rules)

The following items are explicitly NOT in this estimate:
- Subgrade preparation, earthwork, and grading (DEL-03-02)
- Site layout and design (DEL-03-01)
- Underground utility crossings beneath pavement (DEL-03-04)
- Civil design fees (PKG-001 general requirements)
- Building interior floor slabs (PKG-002, PKG-004)
- Stormwater management infrastructure (DEL-03-02)

## Comparison to Parametric Benchmark

PP-23 in Assumed_Project_Parameters.csv estimates total site/civil construction at $1,800,000 (for all of PKG-003). This DEL-03-03 estimate of $896,380 represents approximately 50% of the total site/civil parametric estimate, which appears reasonable given that pavements and surfacing are typically the largest single cost category in site/civil works for an operational facility of this type.
