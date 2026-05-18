# QA Report — EST_DEL-008-01_2026-02-28_0800

## RUN_STATUS: OK

All 26 line items are fully priced with no remaining TBD values. Total estimate: $46,130 CAD. All artifacts pass schema and provenance checks. This is a re-run that resolves all 21 TBD lines from the prior snapshot (EST_DEL-008-01_2026-02-26_2232) and adds 3 new specialized lab test items.

---

## S1 — Write Quarantine Respected

**PASS.** All outputs written to `_Estimates/EST_DEL-008-01_2026-02-28_0800/`. No files outside `_Estimates/` were modified.

## S2 — Snapshot Created

**PASS.** Snapshot folder `EST_DEL-008-01_2026-02-28_0800` created under `_Estimates/`.

## S3 — BASIS_OF_ESTIMATE Validated

**PASS.** `BASIS_OF_ESTIMATE = PARAMETRIC` — valid enum value. All 26 detail lines use Method = PARAMETRIC, consistent with the declared basis.

## S4 — Required Artifacts Exist

**PASS.** All required files produced:

| File | Status |
|------|--------|
| Run_Context.md | Created |
| Items.csv | Created (26 rows) |
| Detail.csv | Created (26 rows) |
| Summary.md | Created |
| QA_Report.md | Created (this file) |
| Source_Index.md | Created |
| Decision_Log.md | Created (11 decisions) |
| Assumptions_Log.md | Created (13 assumptions) |
| WBS_CBS_Matrix.csv | Created (11 CBS categories + total) |

## S5 — CSV Schema Integrity

### Items.csv

**PASS.**

| Check | Result |
|-------|--------|
| Parseable CSV | Yes |
| Required columns present (ItemID, DeliverableID, Description, Qty, Unit, PricingMode, SourceDoc, SourceSection, Notes) | Yes — all 9 columns present |
| PricingMode values valid | Yes — all values are UNIT_RATE or LUMP_SUM |
| Every row traces to SourceDoc and SourceSection | Yes |
| Row count | 26 |
| Items with Qty = TBD | 0 of 26 (0%) |

### Detail.csv

**PASS.**

| Check | Result |
|-------|--------|
| Parseable CSV | Yes |
| Required columns present (LineID, ItemID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes) | Yes — all 15 columns present |
| Method values valid | Yes — all 26 values are PARAMETRIC |
| Allowance/parametric convention respected | N/A — no ALLOWANCE lines; lump-sum PARAMETRIC lines have Qty=1, Unit=LS where applicable |
| ItemID traceability | All 26 Detail lines map to a valid Items.csv ItemID |
| Row count | 26 |
| Lines with Amount = TBD | 0 of 26 (0%) |
| Lines with Amount = 0 | 5 of 26 — L-014, L-015, L-016, L-017 (bundled into L-018 GI-12 report), L-021 (bundled into L-001 PM) |
| Amount sum check | $46,130 CAD (verified: matches Summary.md total) |

## S6 — Provenance Discipline

| Metric | Value |
|--------|-------|
| Lines with non-TBD SourceRef | 26 of 26 (100%) |
| Lines with SourceRef = "location TBD" | 0 of 26 (0%) |

**PASS.** Every line item has a complete SourceRef tracing to a specific file and row/rate identifier. All GI-rate references point to Geotechnical_Investigation_Rates.csv with specific GI-XX identifiers. All staff rate references point to Professional_Staff_Rates.csv with specific R-XX identifiers plus Level_of_Effort.csv for hours.

## S7 — TBD Assessment

| Metric | Value |
|--------|-------|
| TBD quantities in Items.csv | 0 |
| TBD rates in Detail.csv | 0 |
| TBD amounts in Detail.csv | 0 |

**PASS.** No TBD values remain in the estimate. All quantities, rates, and amounts are resolved.

## S8 — Pricing Coverage

| CBS Category | Lines | Priced | Coverage |
|---|---|---|---|
| Professional Services — Management | 2 | 2 | 100% |
| Professional Services — Geotechnical | 11 | 11 | 100% (5 lines at $0 are intentionally bundled) |
| Professional Services — Administration | 1 | 1 | 100% ($0; bundled in PM hours) |
| Field Investigation — Mobilization | 1 | 1 | 100% |
| Field Investigation — Drilling | 2 | 2 | 100% |
| Field Investigation — Monitoring | 1 | 1 | 100% |
| Field Investigation — Sampling | 1 | 1 | 100% |
| Field Investigation — Documentation | 1 | 1 | 100% |
| Field Investigation — Restoration | 1 | 1 | 100% |
| Laboratory Testing | 4 | 4 | 100% |

**Overall pricing coverage: 26 of 26 items (100%) are fully priced.**

## S9 — Confidence Distribution

| Confidence Level | Line Count | Amount (CAD) | % of Total |
|---|---|---|---|
| MED | 8 | $16,530 | 35.8% |
| LOW | 18 | $29,600 | 64.2% |

Note: Majority of estimate value is LOW confidence due to parametric subcontractor rates (GI lump sums and R-20 hourly allocations). MED confidence items are those with both rate and quantity sourced from established data (PM/Cost Estimator hours from LoE, drilling/sampling unit rates from GI).

## S10 — Status Reporting

**RUN_STATUS = OK**

Rationale: All 26 line items are fully priced with traceable sources. No TBD values remain. The total of $46,130 CAD represents a complete parametric estimate for the DEL-008-01 geotechnical investigation. All prior-snapshot warnings (W-001 missing LoE hours, W-002 missing GI rates) are resolved.

## S11 — Operator Acceptance Checklist

| Criterion | Status | Notes |
|-----------|--------|-------|
| RUN_STATUS is OK | OK | All items priced; no TBDs |
| Quantity takeoff (Items.csv) reviewed for completeness | 26 items (23 original + 3 new lab test types) | Coverage is thorough for the deliverable scope |
| Basis-consistency checks pass | PASS — all lines use PARAMETRIC | Consistent with BASIS_OF_ESTIMATE |
| Provenance completeness reported | 100% non-TBD SourceRef | All lines fully sourced |
| Scope coverage explicit | 1 deliverable, 1 package | DEL-008-01 fully scoped within PKG-008 |
| No writes outside _Estimates/ | PASS | Verified |
| Prior-snapshot TBDs resolved | 21 of 21 resolved + 3 new items added | $1,530 priced in prior snapshot increased to $46,130 |
