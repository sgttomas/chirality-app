# Estimate Summary — EST_DEL-011-04_2026-02-27_0949

## Basis of Estimate

| Field | Value |
|---|---|
| **BASIS_OF_ESTIMATE** | PARAMETRIC |
| **CURRENCY** | CAD |
| **FALLBACK_POLICY** | ALLOW_PARAMETRIC |
| **ALLOW_MIXED_METHODS** | TRUE |
| **Scope** | DEL-011-04 — Entrance/Exit Doors (PKG-011 Building Structure & Envelope) |
| **Run** | EST_DEL-011-04_2026-02-27_0949 |

The estimate is derived parametrically from rate tables (Building_Envelope_Rates.csv, Construction_Labour_Rates.csv, Professional_Staff_Rates.csv) and the Level_of_Effort.csv model. Door quantity (3 EA) is assumed based on parametric reasoning for a ~13,000 sqft industrial maintenance shop in Alberta (see ASM-001). One line item (L-014 fire-rated door allowance) uses the ALLOWANCE method per FALLBACK_POLICY = ALLOW_PARAMETRIC and ALLOW_MIXED_METHODS = TRUE.

---

## Totals by CBS

| CBS | Amount (CAD) | Line Count | % of Total |
|---|---|---|---|
| Materials | $7,761.20 | 5 | 44.5% |
| Labour | $3,264.30 | 7 | 18.7% |
| Professional Services | $6,400.00 | 2 | 36.7% |
| **TOTAL** | **$17,425.50** | **14** | **100.0%** |

## Totals by Package / Deliverable

| Package | Deliverable | Amount (CAD) |
|---|---|---|
| PKG-011 | DEL-011-04 Entrance/Exit Doors | $17,425.50 |

---

## Key Warnings and Coverage Gaps

| ID | Warning | Impact |
|---|---|---|
| W-001 | Door quantity assumed at 3 EA (TBD in Datasheet). Actual count depends on IFC Architectural drawings (DEL-001-07). | Quantity may vary from 2 to 5+; estimate scales linearly on quantity-driven items (L-001 through L-006). |
| W-002 | Door material, dimensions, hardware specification, fire rating, glazing, and insulation are all TBD pending DEL-001-07 / DEL-001-11. | Unit rates may change when specifications are confirmed. Current pricing uses generic insulated steel man-door rate. |
| W-003 | Fire-rated door allowance ($1,500) is speculative — compartmentation design TBD. | May be $0 if no fire compartmentation affects pedestrian doors, or higher if multiple doors require fire rating. |
| W-004 | Professional staff LOE ($5,590) represents 32% of total — significant for a relatively small material scope. This is typical for a design-build delivery model with PM/Supt/QA overhead. | LOE is fixed per Level_of_Effort.csv model regardless of door count. |

---

## Pricing Coverage

- **Items priced:** 14 / 14 (100%)
- **Items with TBD amount:** 0 / 14 (0%)
- **Provenance completeness:** 14 / 14 lines have SourceRef (100%)
- **Method mix:** 13 PARAMETRIC + 1 ALLOWANCE (consistent with ALLOW_MIXED_METHODS = TRUE)

---

## Sensitivity Notes

The estimate is most sensitive to:
1. **Door quantity** (ASM-001): each additional door adds approximately $2,500-$2,800 in material + labour.
2. **Fire-rating requirement** (ASM-005): if multiple doors require fire rating, the allowance could increase significantly.
3. **Door specification** (material, size, hardware grade): the BE-04 rate ($1,300/EA) assumes a standard insulated steel man-door; premium specifications (e.g., stainless steel, oversized, blast-rated) would be materially higher.
