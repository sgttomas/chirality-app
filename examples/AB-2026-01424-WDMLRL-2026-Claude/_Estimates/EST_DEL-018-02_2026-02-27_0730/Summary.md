# Estimate Summary — DEL-018-02: Site Grading & Landscaping

**RunID:** EST_DEL-018-02_2026-02-27_0730
**As Of:** 2026-02-27T07:30:00-07:00
**Currency:** CAD

---

## Basis of Estimate

| Field | Value |
|-------|-------|
| **BASIS_OF_ESTIMATE** | PARAMETRIC |
| **Method Mix** | 100% PARAMETRIC (23 of 23 lines) |
| **Fallback Used** | Yes — ALLOW_PARAMETRIC applied to lump-sum allowance items where scope is TBD pending upstream design |
| **Mixed Methods** | FALSE (single method: PARAMETRIC) |

---

## Total by Deliverable

| WBS_DeliverableID | Deliverable Name | Amount (CAD) | Line Count |
|-------------------|------------------|-------------|------------|
| DEL-018-02 | Site Grading & Landscaping | $121,442.00 | 23 |

---

## Total by CBS (Cost Breakdown Structure)

| CBS | Amount (CAD) | Line Count | % of Total |
|-----|-------------|------------|------------|
| Professional Services | $8,590.00 | 8 | 7.1% |
| Earthworks | $56,500.00 | 5 | 46.5% |
| Construction Labour | $14,852.00 | 2 | 12.2% |
| Construction — Site Services | $13,500.00 | 5 | 11.1% |
| Quality Assurance | $5,000.00 | 1 | 4.1% |
| Landscaping | $23,000.00 | 2 | 18.9% |
| **TOTAL** | **$121,442.00** | **23** | **100.0%** |

---

## Total by Package

| WBS_PackageID | Package Name | Amount (CAD) |
|---------------|-------------|-------------|
| PKG-018 | Sitework & Civil Construction | $121,442.00 |

---

## Key Warnings and Coverage Gaps

### Critical TBDs Affecting Estimate Accuracy

1. **Grading area quantity (m2) is parametric.** No explicit grading area is stated in the deliverable documents. The 2,500 m2 estimate is derived parametrically from the building footprint (PP-10: ~13,000 sqft = ~1,208 m2) plus assumed surrounding lot area (~2x building footprint for the expansion lot). The actual area will be defined by the IFC civil grading plan (DEL-005-02).

2. **Landscape scope is entirely TBD.** The $23,000 landscaping allowance (18.9% of total) is a parametric placeholder. Species, areas, quantities, and methods are all pending landscape architect design (DEL-007-02, DEL-007-03). This is the largest single source of estimate uncertainty.

3. **Compaction acceptance criteria are TBD.** The compaction testing allowance ($5,000) and compaction unit rate ($4.00/m2) are based on typical construction standards. Actual requirements depend on civil specification DEL-005-07.

4. **Granular fill volume is parametric.** The 500 m3 fill quantity assumes 200mm average depth over 2,500 m2. County supplies the aggregate; the $12,500 covers placement labour only. Actual fill volumes depend on the civil grading plan.

5. **Fine grading tolerances are TBD.** Tolerances pending civil specification DEL-005-07 may affect labour intensity and rework risk.

### Scope Exclusions (per Datasheet / Specification)

- Brushing/clearing: County forces
- Bulk cut and fill: County forces
- Aggregate supply: County
- Civil grading design: PKG-005
- Landscape architectural design: PKG-007
- Topsoil stripping: DEL-018-01 (separate deliverable)

### Confidence Assessment

| Category | Confidence | Rationale |
|----------|-----------|-----------|
| Professional staff hours | MED | Based on Level_of_Effort.csv parametric model |
| Earthworks unit rates | MED | Based on Earthwork_Civil_Rates.csv parametric rates; area is estimated |
| Construction labour hours | MED | Parametric estimate; typical for site of this scale |
| Lump-sum allowances | LOW | Scope TBD pending upstream design deliverables |
| Landscaping | LOW | Entirely dependent on landscape design not yet issued |
| **Overall** | **LOW-MED** | Material TBDs in grading area and landscape scope drive overall uncertainty |
