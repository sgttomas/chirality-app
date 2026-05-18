# Estimate Summary -- DEL-02-05 Mechanical, Plumbing, Ventilation & Exhaust

## Run Identity

- **RunID:** EST_DEL-02-05_2026-02-18_1400
- **Date:** 2026-02-18
- **Scope:** DEL-02-05 (PKG-002)
- **Basis:** RATE_TABLE
- **Currency:** CAD
- **Rounding:** DOLLAR

## BasisOfEstimate_Used

All line items are priced using structured rate tables from the project price sources. The primary source is `Mechanical_System_Rates.csv` providing per-sf and per-unit rates for HVAC, plumbing, exhaust, and equipment. Labour rates from `Construction_Labour_Rates.csv` support lump-sum commissioning and rough-in items. Design fees are derived from `Professional_Design_Fees.csv` at 2.5% of mechanical construction cost.

## Total Estimate

| Description | Amount (CAD) |
|-------------|-------------|
| **DEL-02-05 Total** | **$1,014,095** |

## Totals by CBS Category

| CBS | Description | Amount (CAD) | Lines | % of Total |
|-----|-------------|-------------|-------|------------|
| 23-HVAC | HVAC systems | $435,200 | 3 | 42.9% |
| 23-PLMB | Plumbing systems | $163,600 | 4 | 16.1% |
| 23-EXHS | Exhaust and ventilation | $144,000 | 2 | 14.2% |
| 23-FPRT | Fire protection (conditional) | $108,000 | 1 | 10.7% |
| 23-CTRL | Building automation | $72,000 | 1 | 7.1% |
| 23-EQUP | Mechanical equipment | $49,000 | 3 | 4.8% |
| 23-MECH-DESIGN | Mechanical design fees | $24,295 | 1 | 2.4% |
| 23-COMM | Commissioning labour | $18,000 | 1 | 1.8% |
| **Total** | | **$1,014,095** | **16** | **100.0%** |

## Key Metrics

- **Mechanical cost per sf (main PSB):** $54/sf ($971,800 construction / 18,000 sf, excluding design fees and commissioning)
- **Line items:** 16
- **Provenance completeness:** 100% (16/16 rows have SourceRef)
- **TBD amounts:** 0
- **Method consistency:** 100% RATE_TABLE (16/16 lines)

## Key Warnings and Risks

1. **Fire protection (L-12, $108,000):** Conditional on AHJ requirement. May not be required for this occupancy classification. Rated LOW confidence. If removed, total drops to $906,095.
2. **Area zoning assumption (ASM-01):** The 18,000 sf building footprint is split into 6,400 sf apparatus bays / 6,400 sf PW bays / 5,200 sf institutional. Actual design layout may shift these proportions.
3. **Rate-table source metadata note:** Price source CSVs carry `Basis=PARAMETRIC` in their metadata, but are structured as tabular rates and are treated as rate-table entries for this run (DEC-01).
4. **Sump rough-in excluded:** Only sump assemblies + plumbing connections are priced here. Slab rough-in (floor penetrations, embedded piping) is owned by DEL-02-04.
5. **Compressed air excluded:** Per cost ownership rules, compressed air equipment is owned by DEL-02-02; not priced here.

## Blockers from Dependency Analysis

- **DEP-0205-E08:** Compressed air scope boundary (CON-M-01) remains unresolved between DEL-02-05 and DEL-02-02. No pricing impact on this estimate because compressed air is excluded per brief, but the boundary should be confirmed.
- **DEP-0205-E11:** PW bay count (assumed 4 per PP-12, CONFIRMED) constrains sump quantity. If bay count changes, L-09 sump quantity must be revised.
- **DEP-0205-E12:** Applicable code editions not confirmed with AHJ. Fire protection requirement (L-12) is conditional.
