# Estimate Summary

## Snapshot Identification

| Field | Value |
|-------|-------|
| Snapshot ID | EST_PKG06_DRAFT_2026-01-28_2333 |
| Estimate Label | PKG06_DRAFT |
| Package Scope | PKG-06 Structural Steelwork (5 deliverables) |
| Pricing Date | 2026-01 (January 2026 dollars) |
| Currency | CAD |
| Run Status | WARNINGS |

## Base Estimate by CBS

| CBS | Description | Base Amount (CAD) | Contingency % | Contingency (CAD) | Total (CAD) |
|-----|-------------|------------------:|-------------:|------------------:|------------:|
| E | Engineering & Design | $89,000 | 20% | $17,800 | $106,800 |
| PM | Project Management / EPCM | $120,000 | 15% | $18,000 | $138,000 |
| P | Procurement Services | $27,000 | 15% | $4,100 | $31,100 |
| MAT | Equipment & Materials | $1,301,000 | 25% | $325,300 | $1,626,300 |
| CD | Construction Directs | $611,000 | 30% | $183,300 | $794,300 |
| CI | Construction Indirects | $115,000 | 30% | $34,500 | $149,500 |
| COM | Commissioning / Testing | $60,000 | 30% | $18,000 | $78,000 |
| **Subtotal** | | **$2,323,000** | | **$601,000** | **$2,924,000** |

*(Rounded to nearest $1,000)*

## Total Estimate

| Line | Amount (CAD) |
|------|-------------:|
| **Base Estimate** | $2,323,000 |
| **Contingency** | $601,000 |
| **Total Estimate** | **$2,924,000** |

## Estimate Breakdown by WBS

| Deliverable ID | Deliverable Name | Base Amount (CAD) |
|----------------|------------------|------------------:|
| DEL-06.01 | Structural Steel Design Drawing Set | $45,000 |
| DEL-06.02 | Structural Steel Technical Specification | $12,000 |
| DEL-06.03 | Structural Steel Design Calculations | $18,000 |
| DEL-06.04 | Structural Steel Data Sheet Package | $6,000 |
| DEL-06.05 | Structural Steel Installation & Test Records | $8,000 |
| N/A | Construction/Materials (package scope, not deliverable-specific) | $2,234,000 |
| **Total Base** | | **$2,323,000** |

## Key Quantities and Drivers

| Item | Quantity | Unit | Unit Rate (CAD) | Basis |
|------|----------|------|----------------:|-------|
| Structural steel (fabricated/galvanized) | 150 | tonne | $6,000/tonne | Allowance (D-012, A-006) |
| Steel erection labor | 3,750 | hrs | $95/hr | Allowance (25 hrs/tonne, A-007) |
| Handrail | 400 | m | $220/m installed | Allowance (D-013, A-009) |
| Grating | 800 | m² | $180/m² installed | Allowance (D-013, A-010) |
| Stairs and gangways | 12 | EA | $15,000/item | Allowance (A-011) |

## Cost Distribution

**By CBS Category:**
- Materials (MAT): 56% of base estimate
- Construction Directs (CD): 26% of base estimate
- Construction Indirects (CI): 5% of base estimate
- Project Management (PM): 5% of base estimate
- Engineering (E): 4% of base estimate
- Commissioning (COM): 3% of base estimate
- Procurement (P): 1% of base estimate

**By Pricing Method:**
- Allowances: 81% of base estimate ($1,880,000)
- Parametric (factor-derived): 19% of base estimate ($443,000)
- Quotes: 0%
- Rate Tables: 0%

## Completeness Metrics

| Metric | Value |
|--------|-------|
| Lines priced by QUOTE | 0% (0 of 21 lines) |
| Lines priced by RATE_TABLE | 0% (0 of 21 lines) |
| Lines priced by ALLOWANCE | 81% (17 of 21 lines) |
| Lines priced by PARAMETRIC | 19% (4 of 21 lines) |
| Deliverables with explicit quantities | 0% (0 of 5 deliverables) |
| Overall Confidence | LOW |

## Top Cost Drivers (Descending)

| Rank | Description | Amount (CAD) | % of Base |
|------|-------------|-------------:|----------:|
| 1 | Structural steel material supply (150 tonnes fabricated/galvanized) | $900,000 | 39% |
| 2 | Structural steel erection labor (3,750 hrs) | $356,000 | 15% |
| 3 | Stairs and gangways (12 items pre-fabricated) | $180,000 | 8% |
| 4 | Crane & equipment for steel erection | $120,000 | 5% |
| 5 | EPCM / Project Management (factor-based) | $120,000 | 5% |
| 6 | Construction Indirects (factor-based) | $115,000 | 5% |
| 7 | Grating supply (800 m²) | $96,000 | 4% |
| 8 | Pipe supports and racks | $65,000 | 3% |
| 9 | Commissioning & testing (factor-based) | $60,000 | 3% |
| 10 | Handrail supply (400 m) | $60,000 | 3% |

## Known Gaps and Warnings

| Gap | Impact on Estimate | Resolution Required |
|-----|-------------------|---------------------|
| No structural steel tonnage from design | High — tonnage allowance (150 t) may be ±50% | Provide design drawings (DEL-06.01) with member sizes or tonnage estimate |
| No vendor quotes for fabrication/galvanizing | High — $6k/tonne rate is placeholder | Obtain budgetary quotes from steel fabricators |
| No handrail/grating quantities | Medium — linear/area allowances are rough | Provide platform layout drawings showing handrail extents and grating areas |
| No stairs/gangway item list | Medium — count allowance (12 items) is rough | Provide gangway data sheets (DEL-06.04) with item counts and sizes |
| No labor productivity data | Medium — 25 hrs/tonne is typical range | Provide erection productivity assumptions or historical data |
| No project rate tables | Medium — labor/equipment rates are assumed | Provide project labor rates and equipment rental rates |

## Exclusions

- Foundation costs (assumed under PKG-05 Concrete Structures)
- Owner's costs, land, financing
- Permits obtained by Employer
- Escalation (pricing date = 2026-01; no escalation applied)
- Taxes

## Notes

- **Estimate maturity:** LOW (100% allowance/parametric-based; no vendor quotes or detailed design)
- **Contingency:** Elevated percentages (20-30%) applied due to allowance-heavy estimate
- **Rounding:** All CBS totals rounded to nearest $1,000
- **Recommended next steps:** Obtain structural steel design drawings (tonnage, counts), vendor quotes, and project rate tables to improve estimate confidence

---

**Summary compiled:** 2026-01-28 23:33
**Detail Reference:** Detail.csv (21 line items)
**Traceability:** Decision_Log.md (D-001 to D-013), Assumptions_Log.md (A-001 to A-015)
