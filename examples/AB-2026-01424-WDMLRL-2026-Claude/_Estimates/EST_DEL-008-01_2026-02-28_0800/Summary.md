# Summary — EST_DEL-008-01_2026-02-28_0800

## Basis of Estimate

| Field | Value |
|-------|-------|
| **BASIS_OF_ESTIMATE** | PARAMETRIC |
| **CURRENCY** | CAD |
| **FALLBACK_POLICY** | ALLOW_PARAMETRIC |
| **ALLOW_MIXED_METHODS** | TRUE |
| **Method used** | PARAMETRIC (all lines) |

This estimate is a parametric model based on geotechnical investigation subcontractor rates (Geotechnical_Investigation_Rates.csv), professional staff hourly rates (Professional_Staff_Rates.csv), and level-of-effort hours (Level_of_Effort.csv). All 26 detail lines are fully priced with no remaining TBD values.

---

## Totals by Package / Deliverable / CBS

### By Package

| PackageID | Amount (CAD) | Line Count | Notes |
|-----------|-------------|------------|-------|
| PKG-008 | $46,130 | 26 | All lines priced |

### By Deliverable

| DeliverableID | Amount (CAD) | Line Count | Priced Lines | TBD Lines |
|---------------|-------------|------------|-------------|-----------|
| DEL-008-01 | $46,130 | 26 | 26 (100%) | 0 (0%) |

### By CBS

| CBS Category | Amount (CAD) | Line Count | Lines |
|-------------|-------------|------------|-------|
| Professional Services — Management | $1,530 | 2 | L-001 ($990), L-002 ($540) |
| Professional Services — Geotechnical | $20,000 | 11 | L-003 ($3,000), L-004 ($350), L-010 ($5,250), L-013 ($700), L-014 ($0), L-015 ($0), L-016 ($0), L-017 ($0), L-018 ($9,000), L-019 ($350), L-022 ($350) |
| Professional Services — Administration | $0 | 1 | L-021 ($0) — included in PM hours |
| Field Investigation — Mobilization | $6,000 | 1 | L-005 ($6,000) |
| Field Investigation — Drilling | $4,000 | 2 | L-006 ($1,600), L-007 ($2,400) |
| Field Investigation — Monitoring | $2,500 | 1 | L-008 ($2,500) |
| Field Investigation — Sampling | $1,250 | 1 | L-009 ($1,250) |
| Field Investigation — Documentation | $250 | 1 | L-011 ($250) |
| Field Investigation — Restoration | $1,000 | 1 | L-023 ($1,000) |
| Laboratory Testing | $9,600 | 4 | L-012 ($4,500), L-024 ($2,200), L-025 ($1,500), L-026 ($1,400) |
| Professional Services — Geotechnical (P.Eng.) | $1,000 | 1 | L-020 ($1,000) |
| **TOTAL** | **$46,130** | **26** | |

---

## Cost Distribution Summary

| Cost Category | Amount (CAD) | % of Total |
|---------------|-------------|------------|
| Professional Services (Management + Geotech + Admin + P.Eng.) | $22,530 | 48.8% |
| Field Investigation (Mob + Drilling + Monitoring + Sampling + Docs + Restoration) | $15,000 | 32.5% |
| Laboratory Testing | $9,600 | 20.8% |
| **Total** | **$46,130** | **100.0%** |

---

## Priced Amount Summary

**Total priced: $46,130 CAD**

This represents the full parametric estimate for the DEL-008-01 geotechnical investigation including:
- Project management and cost estimating overhead ($1,530)
- Geotechnical subcontractor scope: program development, field supervision, analysis/report, P.Eng. seal ($18,250)
- Project team geotechnical engineer: site access, lab QA review, independent review, owner coordination ($1,750)
- Field investigation: mobilization, drilling, test pits, monitoring well, sampling, documentation, restoration ($15,000)
- Laboratory testing: classification, consolidation, shear, chemical ($9,600)

---

## Resolved TBDs (from Prior Snapshot)

The prior snapshot (EST_DEL-008-01_2026-02-26_2232) had 21 of 23 lines as TBD, with only $1,530 CAD priced. This snapshot resolves all 21 TBD lines and adds 3 new items, bringing the total to $46,130 CAD across 26 lines.

| Resolution Source | Lines Resolved | Description |
|-------------------|---------------|-------------|
| Geotechnical_Investigation_Rates.csv | 14 | GI-01 through GI-15 rates applied to field, lab, and subcontractor professional items |
| Professional_Staff_Rates.csv R-20 + Level_of_Effort.csv | 4 | R-20 at $175/hr for project team items (site access, lab QA, independent review, owner coordination) |
| Bundled in other lines | 3 | L-014, L-015, L-016, L-017 bundled into L-018 (GI-12); L-021 bundled into L-001 (PM) |
| New items (GI-07, GI-08, GI-09) | 3 | Specialized lab tests added: consolidation, shear, chemical analysis |

---

## Key Notes

1. **Subcontractor vs. project team split.** GI rates (Geotechnical_Investigation_Rates.csv) are used for items within the geotechnical subcontractor's scope of work. R-20 at $175/hr is used only for project team activities not covered by the subcontractor (site access coordination, lab QA review, independent review, owner coordination).

2. **Bundled analysis items.** Bearing capacity analysis (L-014), settlement analysis (L-015), service pit characterization (L-016), and deleterious materials assessment (L-017) are priced at $0 individually because they are included in the GI-12 lump-sum report preparation scope ($9,000 in L-018). They are retained as separate line items for traceability to specification requirements.

3. **Confidence levels.** Most field investigation and lab items are rated MED confidence (based on parametric rates with reasonable basis). Professional services items using R-20 hourly rates and GI lump sums are rated LOW confidence (hours are estimated; lump sums have wide ranges in the rate source).

4. **No overhead/markup.** Rates are applied without overhead, profit, or indirect cost multipliers. Actual costs may be higher if markups apply.

5. **Commercially significant output.** This deliverable produces the deleterious materials determination that drives the variable-price foundation mechanism (RFP 4.8.2). The investigation cost ($46,130) is small relative to the foundation pricing adjustment it may trigger.
