# Summary — EST_DEL-008-01_2026-02-26_2232

## Basis of Estimate

| Field | Value |
|-------|-------|
| **BASIS_OF_ESTIMATE** | PARAMETRIC |
| **CURRENCY** | CAD |
| **FALLBACK_POLICY** | ALLOW_PARAMETRIC |
| **ALLOW_MIXED_METHODS** | TRUE |
| **Method used** | PARAMETRIC (all lines) |

The estimate is a parametric model based on professional staff hourly rates and level-of-effort hours. The provided price sources cover only a small fraction of the deliverable's cost scope: project management and cost estimating hours. The major cost drivers for a geotechnical investigation (drilling, laboratory testing, geotechnical engineer time, mobilization) are not quantified in the available sources.

---

## Totals by Package / Deliverable / CBS

### By Package

| PackageID | Amount (CAD) | Line Count | Notes |
|-----------|-------------|------------|-------|
| PKG-008 | 1,530 + TBD | 23 | Only management overhead priced |

### By Deliverable

| DeliverableID | Amount (CAD) | Line Count | Priced Lines | TBD Lines |
|---------------|-------------|------------|-------------|-----------|
| DEL-008-01 | 1,530 + TBD | 23 | 2 (8.7%) | 21 (91.3%) |

### By CBS

| CBS Category | Amount (CAD) | Line Count |
|-------------|-------------|------------|
| Professional Services — Management | 1,530 | 2 |
| Professional Services — Geotechnical | TBD | 11 |
| Professional Services — Administration | TBD | 1 |
| Field Investigation — Mobilization | TBD | 1 |
| Field Investigation — Drilling | TBD | 2 |
| Field Investigation — Monitoring | TBD | 1 |
| Field Investigation — Sampling | TBD | 1 |
| Field Investigation — Documentation | TBD | 1 |
| Field Investigation — Restoration | TBD | 1 |
| Laboratory Testing | TBD | 1 |
| **TOTAL** | **1,530 + TBD** | **23** |

---

## Priced Amount Summary

**Total priced: $1,530 CAD** (Project Manager 6 hr x $165 = $990; Cost Estimator 4 hr x $135 = $540)

This represents management overhead only. The substantive cost of the geotechnical investigation (field work, laboratory testing, geotechnical engineering, report preparation) remains TBD.

---

## Key Warnings and Coverage Gaps

1. **Critical gap — Geotechnical Engineer hours not in Level_of_Effort.csv.** The LoE file provides only PM and Cost Estimator hours for DEL-008-01. No hours are allocated for the Geotechnical Engineer (R-20), who is the responsible party and performs the majority of the work.

2. **Critical gap — No field investigation or laboratory rates.** The price sources contain only professional staff hourly rates. Drill rig, drilling crew, sampling equipment, lab testing, and mobilization costs are not covered. These are typically the largest cost components of a geotechnical investigation.

3. **Quantity uncertainty.** Most quantities in Items.csv are TBD. The deliverable documents correctly note that borehole count, depth, test program, and lab testing scope are to be determined by the Geotechnical Engineer based on site conditions. This is appropriate for design-stage scoping but prevents pricing.

4. **Commercially significant output.** This deliverable produces the "deleterious materials" determination that drives the variable-price foundation mechanism (RFP §4.8.2). The investigation cost itself is small relative to the foundation pricing adjustment it may trigger.

5. **For a meaningful estimate,** the following are needed:
   - Geotechnical Engineer level-of-effort hours (investigation program development, field supervision, analysis, report preparation)
   - Geotechnical drilling subcontractor quote or parametric rates (per borehole, per metre)
   - Laboratory testing unit costs
   - Mobilization/demobilization lump sum or rate
