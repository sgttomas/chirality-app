# Summary — EST_DEL-004-09_2026-02-27_0141

## Basis of Estimate

| Field | Value |
|---|---|
| BASIS_OF_ESTIMATE | PARAMETRIC |
| Method Used | Level-of-effort hours (from Level_of_Effort.csv) multiplied by staff hourly rates (from Professional_Staff_Rates.csv) |
| Currency | CAD |
| Fallback Policy | ALLOW_PARAMETRIC |
| Mixed Methods | TRUE (allowed) — all lines priced as PARAMETRIC in this run |

## Totals by Deliverable

| WBS_DeliverableID | Name | Amount (CAD) | Line Count |
|---|---|---|---|
| DEL-004-09 | Electrical Specification | **10,170.00** | 4 |

## Totals by CBS

| CBS | Amount (CAD) | Line Count | Description |
|---|---|---|---|
| Design-Management | 1,530.00 | 2 | Project Manager + Cost Estimator |
| Design-Production | 1,710.00 | 1 | BIM Technician (specification support and figure preparation) |
| Design-Engineering | 6,930.00 | 1 | Electrical Engineer (lead specification authoring) |
| **TOTAL** | **10,170.00** | **4** | |

## Totals by Package

| WBS_PackageID | Amount (CAD) |
|---|---|
| PKG-004 | **10,170.00** |

## Effort Summary

| Role | Hours | Rate (CAD/hr) | Amount (CAD) |
|---|---|---|---|
| Project Manager (R-01) | 6 | 165.00 | 990.00 |
| Cost Estimator (R-08) | 4 | 135.00 | 540.00 |
| BIM Technician (R-13) | 18 | 95.00 | 1,710.00 |
| Electrical Engineer (R-16) | 42 | 165.00 | 6,930.00 |
| **Total** | **70** | — | **10,170.00** |

## Key Observations

1. **Scope:** DEL-004-09 is the Electrical Specification governing SOW-0014 (complete final electrical design). It is a written design specification document — not a field installation procedure or construction deliverable. The estimate covers professional design labour only; no material or construction costs are included.
2. **Comprehensive specification scope:** The specification covers 27 requirements (REQ-001 through REQ-027) spanning three-phase power, lighting (26 fixtures across 5 space types), receptacles (5 circuit types), dedicated equipment circuits (cranes, compressor, fire hose pump, pressure washer, overhead doors), exhaust fans, low-voltage systems (security cameras, radio antenna), grounding/bonding, emergency lighting, lighting control, voltage drop, and wiring methods.
3. **Labour composition:** The Electrical Engineer accounts for 68.1% of the total cost (42 of 70 hours). This is consistent with a specification-authoring deliverable where the engineer performs source review, requirements extraction, utility coordination, discipline coordination, design calculations, specification drafting, QA review, and permit coordination.
4. **BIM Technician:** 18 hours allocated for specification support, representing 25.7% of total hours. This covers figure preparation, cross-referencing between specification and drawing deliverables, and format/layout support.
5. **Management overhead:** PM (6h) + Cost Estimator (4h) = 10h combined (14.3% of total), which is a light management touch consistent with a specification deliverable within a larger design package.
6. **No TBD pricing:** All 4 priced lines have complete rates and quantities from the price sources. 100% pricing coverage.

## Warnings and Coverage Gaps

- **No material/construction costs:** This deliverable is design-only. Items 5–36 in Items.csv represent design scope verification lines (electrical systems and specification activities the engineer must address) but are priced through the labour effort in Items 1–4. They are not separately costed.
- **Numerous TBD inputs in the specification:** The Electrical Specification identifies multiple TBD items (crane specs, exhaust fan data, camera system, antenna system, utility confirmation, code editions) that require resolution before the specification can be finalized for IFC. These TBDs do not affect the design labour estimate but represent technical risks to the deliverable schedule.
- **Five hold points (HOLD-01 through HOLD-05):** The Procedure identifies 5 interdisciplinary hold points that must be released before corresponding design elements can be finalized. Delays in hold-point release could extend the schedule and potentially increase hours, though the parametric LOE allocation accounts for typical coordination effort.
- **Professional Design Fees cross-check:** DF-04 in Professional_Design_Fees.csv suggests electrical design fees of 1.0%–2.2% of construction value. Without a confirmed construction value, this cross-check cannot be completed. If construction value is estimated at ~$2M–$3M, the full electrical design package (PKG-004, all deliverables DEL-004-01 through DEL-004-09) would be $20K–$66K. The DEL-004-09 specification at $10,170 represents one deliverable of nine in PKG-004, which is directionally consistent.
