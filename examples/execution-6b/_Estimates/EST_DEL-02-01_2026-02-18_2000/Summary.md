# Estimate Summary — DEL-02-01 Architectural Concept Package

**RunID:** EST_DEL-02-01_2026-02-18_2000
**Basis of Estimate:** RATE_TABLE
**Currency:** CAD
**Rounding:** DOLLAR

---

## Basis of Estimate Used

**Method:** RATE_TABLE -- hourly rates from `Professional_Staff_Rates.csv` multiplied by estimated hours from `Level_of_Effort.csv`.

All 4 line items use Method = RATE_TABLE. No fallback methods were applied. No mixed methods.

---

## Total

| Measure | Value |
|---|---|
| **Total Estimated Cost** | **$15,780 CAD** |
| **Total Hours** | **132 hours** |
| **Line Items** | 4 |
| **Provenance Completeness** | 100% (all rows have SourceRef) |

---

## Breakdown by CBS

| CBS | Description | Hours | Amount (CAD) | % of Total |
|---|---|---|---|---|
| LABOR-DESIGN | Architect (Project) + Architect (Intermediate) | 64 | $8,680 | 55.0% |
| LABOR-PRODUCTION | CAD Technician / BIM Operator | 60 | $5,700 | 36.1% |
| LABOR-MGMT | Project Manager | 8 | $1,400 | 8.9% |
| **TOTAL** | | **132** | **$15,780** | **100.0%** |

---

## Breakdown by Role

| RoleID | Role | Hours | Rate (CAD/hr) | Amount (CAD) | % of Total |
|---|---|---|---|---|---|
| R-04 | Architect (Project) | 40 | $145 | $5,800 | 36.8% |
| R-06 | CAD Technician / BIM Operator | 60 | $95 | $5,700 | 36.1% |
| R-05 | Architect (Intermediate) | 24 | $120 | $2,880 | 18.2% |
| R-02 | Project Manager | 8 | $175 | $1,400 | 8.9% |
| **TOTAL** | | **132** | | **$15,780** | **100.0%** |

---

## Key Observations

1. **Highest-effort PKG-002 deliverable.** At 132 hours and $15,780, DEL-02-01 is the most resource-intensive deliverable in the Conceptual Design package due to drawing production requirements (floor plans, elevations, sections, optional renderings).

2. **Drawing production dominates.** CAD/BIM production (60 hours) accounts for 36% of cost but 45% of total hours, reflecting the labor-intensive nature of architectural drawing sets at concept stage.

3. **Design + Production = 91% of cost.** Only 9% of cost ($1,400) is management overhead; the vast majority is direct design and production labor.

4. **Cost ownership boundaries respected.** No civil, structural, mechanical, or electrical hours are included. Those discipline-specific concept costs are carried by DEL-02-02 through DEL-02-05 respectively.

5. **SOW-0009/SOW-0010 multi-mapping acknowledged.** This estimate covers only the architectural portion of these shared scope items. The full PKG-002 concept design cost is the sum of DEL-02-01 through DEL-02-05.

---

## Warnings and Blockers

- **No critical warnings.** All 4 line items are fully priced with RATE_TABLE method and complete provenance.
- **Dependency blockers (for execution, not pricing):** DEL-02-01 has upstream interface dependencies on DEL-02-02, DEL-02-03, DEL-02-04, and DEL-02-05 for discipline input data. These do not affect cost estimation but are noted in `Blockers.md`.
- **Rate confidence:** All rates are MARKET-basis with MEDIUM confidence. Actual firm rates may differ.
- **Hours confidence:** Level of effort is PARAMETRIC-basis. Actual hours depend on design complexity, revision cycles, and client feedback.
