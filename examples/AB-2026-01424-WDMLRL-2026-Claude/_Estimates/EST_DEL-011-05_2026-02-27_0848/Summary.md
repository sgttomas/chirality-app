# Estimate Summary — DEL-011-05 Wash Bay Enclosure

**RunID:** EST_DEL-011-05_2026-02-27_0848
**Date:** 2026-02-27
**Basis of Estimate:** PARAMETRIC
**Currency:** CAD
**RUN_STATUS:** WARNINGS

---

## Basis of Estimate Used

- **Primary method:** PARAMETRIC — unit rates and parametric models from project-specific rate tables (Structural_Concrete_Rates.csv, Building_Envelope_Rates.csv, Construction_Labour_Rates.csv, Professional_Staff_Rates.csv, Level_of_Effort.csv).
- **Fallback method:** ALLOWANCE — used for items where parametric rates exist but quantities or specifications are TBD (embedded steel plates, overhead door, gantry provisions).
- **Mixed methods:** YES (ALLOW_MIXED_METHODS=TRUE). 20 of 24 lines are PARAMETRIC; 4 lines are ALLOWANCE.
- **Fallback policy:** ALLOW_PARAMETRIC — items without direct rate evidence were estimated using parametric derivations from comparable items and documented in Decision_Log.md.

---

## Totals by CBS

| CBS | Amount (CAD) | Line Count | % of Total |
|---|---|---|---|
| 01-General | $10,040 | 5 | 6.9% |
| 03-Concrete | $43,895 | 8 | 30.2% |
| 05-Structural | $12,500 | 2 | 8.6% |
| 07-Envelope | $55,706 | 6 | 38.4% |
| 08-Doors | $21,916 | 2 | 15.1% |
| 16-Electrical | $1,200 | 1 | 0.8% |
| **TOTAL** | **$145,257** | **24** | **100%** |

---

## Totals by Package / Deliverable

| WBS_PackageID | WBS_DeliverableID | Amount (CAD) | Line Count |
|---|---|---|---|
| PKG-011 | DEL-011-05 | $145,257 | 24 |

---

## Key Warnings and Coverage Gaps

1. **Multiple TBD attributes** — Steel plate dimensions/grade (B-001), wall construction material (B-003), overhead door height (A-001), wash bay clear ceiling height (C-001), and floor drainage slope (F-002) are all TBD pending IFC drawings. These affect quantity and rate confidence.

2. **Steel plate scope ownership conflict (C-01)** — The wash bay floor steel plate may also be addressed in DEL-011-02 (Steel Plate Floor Embedments). This estimate includes wash bay steel plates under DEL-011-05 per SOW-0027a. Risk of double-counting exists if DEL-011-02 also includes them.

3. **Gantry provisions are conditional ($5,000)** — Line L-015 is included based on the ASSUMPTION that the gantry shown in App B is confirmed. If the Owner does not confirm the gantry, this line should be removed, reducing the total by $5,000.

4. **Overhead door is an ALLOWANCE ($19,000)** — The 24 ft overhead door is priced using Building_Envelope_Rates.csv BE-03 at the recommended rate. Door height is TBD, and motorized operation is assumed. Actual procurement pricing could vary significantly ($14,000 to $24,000 range).

5. **Wall material is ASSUMED as insulated metal panels** — If the Architect/Structural Engineer specifies concrete tilt-up or CMU walls instead, the wall cost (currently $26,280 for 146 m2 at $180/m2) would increase significantly (concrete wall rate is $420/m2 per SC-06, which would yield ~$61,320).

6. **Labour hours are parametric estimates** — Construction labour quantities (concrete: 120 hr, walls: 160 hr, roof: 80 hr, door: 40 hr) are derived from parametric benchmarks, not from a detailed crew-day analysis. Actual hours depend on site conditions and crew productivity.

---

## Scope Coverage

- **Included:** 1 deliverable (DEL-011-05) with 24 priced line items covering concrete floor, walls, roof, overhead door, embedded steel plates, mezzanine provisions, gantry provisions, drainage coordination, electrical coordination, inspections, professional staff, and documentation.
- **Excluded (by scope):** Drainage infrastructure (DEL-018-05), electrical installation (DEL-015-02/04), mezzanine framing (DEL-011-07), foundation (DEL-010-01), plumbing (DEL-014-04/06), mechanical/ventilation (DEL-013 package).
- **Documents read:** 4/4 (Datasheet, Specification, Guidance, Procedure) + _CONTEXT.md.
