# Estimate Summary — EST_DEL-012-03_2026-02-27_0630

## Basis of Estimate

| Field | Value |
|---|---|
| BASIS_OF_ESTIMATE | PARAMETRIC |
| CURRENCY | CAD |
| FALLBACK_POLICY | ALLOW_PARAMETRIC |
| ALLOW_MIXED_METHODS | TRUE |
| Scope | DEL-012-03 — Office Space (PKG-012 Interior Construction & Fit-Out) |
| Run Timestamp | 2026-02-27T06:30:00-07:00 |

**Method Summary:** 22 of 23 lines priced as PARAMETRIC; 1 line (DL-018 millwork) priced as ALLOWANCE. Mixed methods permitted per ALLOW_MIXED_METHODS=TRUE.

---

## Total by Package / Deliverable

| WBS Package | Deliverable | Total (CAD) |
|---|---|---|
| PKG-012 | DEL-012-03 — Office Space | **$37,247.40** |

## Total by CBS

| CBS Category | Total (CAD) | Line Count |
|---|---|---|
| Management | $2,340.00 | 3 |
| Construction | $34,907.40 | 20 |
| **Grand Total** | **$37,247.40** | **23** |

## Breakdown by Major Category

| Category | Amount (CAD) | % of Total |
|---|---|---|
| Professional staff (PM, CPM, Supt, Estimator, QA/QC, HSE) | $5,590.00 | 15.0% |
| Interior finishes — partitions (material) | $4,500.00 | 12.1% |
| Interior finishes — ceiling (material + install) | $2,000.00 | 5.4% |
| Interior finishes — flooring (material + install) | $1,750.00 | 4.7% |
| Interior finishes — paint | $900.00 | 2.4% |
| Millwork allowance | $11,000.00 | 29.5% |
| Door — supply and install | $1,200.00 | 3.2% |
| Electrical (receptacles + lighting + data) | $1,890.00 | 5.1% |
| HVAC coordination allowance | $750.00 | 2.0% |
| Accessibility features | $500.00 | 1.3% |
| Safety / life safety features | $800.00 | 2.1% |
| Construction trade labour (carpenter, drywaller, painter, flooring) | $5,846.60 | 15.7% |
| Inspection / deficiency correction | $520.80 | 1.4% |
| **Total** | **$37,247.40** | **100.0%** |

---

## Key Warnings and Coverage Gaps

1. **Office floor area is assumed (25 m2 / ~269 sq ft).** This is a critical driver for partition, ceiling, flooring, and paint quantities. The actual area is TBD pending IFC architectural drawings. Quantity sensitivity: +/- 50% area change would shift area-dependent items by approximately +/- $4,575.

2. **Millwork allowance ($11,000) represents 29.5% of the total.** This is the single largest line item and is sourced from the Interior_Architectural_Rates.csv allowance (IA-05) at LOW confidence. If the office does not require casework (e.g., no kitchenette counter or built-in shelving), this line should be removed, reducing the total to approximately $26,247.

3. **Scope boundary between PKG-012 and PKG-015 is unresolved (CONF-001).** Electrical receptacle, lighting, and data outlet items (DL-012, DL-013, DL-014; total $1,890) are included in this estimate per _CONTEXT.md scope. If these are ultimately assigned to PKG-015, they should be removed from this estimate.

4. **Multiple finish specifications are TBD** pending IFC design (flooring type, ceiling type, drywall finish level, door type/hardware). Actual costs may vary from parametric rates once specifications are confirmed.

5. **No contingency or escalation is included.** This estimate reflects base parametric costs only.

6. **All confidence ratings are MEDIUM or LOW.** No HIGH-confidence lines exist. This is consistent with a pre-IFC, conceptual-stage parametric estimate.

---

## Provenance

- 23 of 23 Detail.csv lines (100%) have a non-TBD SourceRef.
- All price sources are local CSV files provided in PRICE_SOURCES.
- All quantities are derived from deliverable documents or assumed parametrically (documented in Assumptions_Log.md).
