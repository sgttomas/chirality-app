# Estimate Summary — DEL-001-02 Architectural Floor Plans

**RunID:** EST_DEL-001-02_2026-02-27_0600
**As Of:** 2026-02-27T06:00:00-07:00
**Basis of Estimate:** PARAMETRIC
**Currency:** CAD
**Scope:** DEL-001-02 (Architectural Floor Plans) within PKG-001 (Architectural Design)

---

## Basis of Estimate Used

- **Method:** PARAMETRIC — Level of Effort (hours by role) multiplied by Professional Staff Rates (CAD/hr).
- **Quantity source:** Level_of_Effort.csv (5 role assignments for DEL-001-02, totalling 130 hours).
- **Rate source:** Professional_Staff_Rates.csv (hourly rates by role, all PARAMETRIC basis, MEDIUM confidence).
- **Fallback:** None required. All 5 priced line items have both quantity and rate evidence from provided sources.
- **Mixed methods:** Not triggered. All priced lines use Method=PARAMETRIC, consistent with BASIS_OF_ESTIMATE.

---

## Totals by Package / Deliverable

| WBS_PackageID | WBS_DeliverableID | Amount (CAD) | Line Count |
|---|---|---|---|
| PKG-001 | DEL-001-02 | **19,200.00** | 5 |

## Totals by CBS

| CBS Category | Amount (CAD) | Line Count |
|---|---|---|
| Management | 1,530.00 | 2 |
| Design | 17,670.00 | 3 |
| **Grand Total** | **19,200.00** | **5** |

## Totals by Role

| Role | Hours | Rate (CAD/hr) | Amount (CAD) |
|---|---|---|---|
| Project Manager (R-01) | 6 | 165.00 | 990.00 |
| Cost Estimator (R-08) | 4 | 135.00 | 540.00 |
| Senior Architect (R-11) | 54 | 180.00 | 9,720.00 |
| Architect (R-12) | 42 | 135.00 | 5,670.00 |
| BIM Technician (R-13) | 24 | 95.00 | 2,280.00 |
| **Total** | **130** | — | **19,200.00** |

---

## Cross-Check: Design Fee Percentage Method

For context, Professional_Design_Fees.csv provides an architectural design fee range of 3.0%–6.0% (recommended 4.5%) of construction value. Using the Parametric_Building_Rates.csv recommended rate of $285/sf for 13,000 sqft:

- Estimated construction value: 13,000 sf x $285/sf = $3,705,000
- Architectural fee at 4.5%: $3,705,000 x 4.5% = $166,725

DEL-001-02 (Architectural Floor Plans) is one of 11 deliverables in PKG-001. The LOE-based estimate of $19,200 for this single deliverable represents approximately 11.5% of the total architectural fee ($166,725), which is consistent with floor plans being a major but not sole drawing set in the package.

---

## Key Warnings and Coverage Gaps

1. **Items with $0 pricing (scope tracked only):** ITM-006 (Code analysis), ITM-007 (Interdisciplinary coordination review), ITM-008 (IFC stamp), and ITM-009 (County approval gate) are scope items identified from the Specification and Procedure documents but are not separately priced — their effort is captured within the professional staff hours (ITM-001 through ITM-005). No additional cost is unaccounted.
2. **Confidence level:** All priced lines carry MEDIUM confidence, consistent with the parametric basis of the staff rates and level-of-effort model.
3. **No direct material or subcontractor costs:** DEL-001-02 is a professional design deliverable (drawing set). All costs are professional labour. No materials, equipment, or subcontractor costs apply.
4. **Rate basis assumptions:** Staff rates are parametric benchmarks for Alberta design-build context. Actual rates may vary by firm.
