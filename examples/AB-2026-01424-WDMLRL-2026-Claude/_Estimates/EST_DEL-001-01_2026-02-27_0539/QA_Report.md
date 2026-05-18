# QA Report — EST_DEL-001-01_2026-02-27_0539

**RUN_STATUS: OK**

---

## S1 — Write Quarantine Respected

**PASS.** All files written exclusively under `_Estimates/EST_DEL-001-01_2026-02-27_0539/`. No files outside the estimating tool root were modified.

---

## S2 — Snapshot Created

**PASS.** Snapshot folder `EST_DEL-001-01_2026-02-27_0539` created under `_Estimates/`.

---

## S3 — BASIS_OF_ESTIMATE Validated

**PASS.** `BASIS_OF_ESTIMATE = PARAMETRIC` — valid enum value.

---

## S4 — Required Artifacts Exist

**PASS.** All required artifacts present:

| Artifact | Status |
|---|---|
| Run_Context.md | Present |
| Items.csv | Present |
| Detail.csv | Present |
| Summary.md | Present |
| QA_Report.md | Present (this file) |
| Source_Index.md | Present |
| Decision_Log.md | Present |
| Assumptions_Log.md | Present |
| WBS_CBS_Matrix.csv | Present |

---

## S5 — CSV Schema Integrity

### Items.csv

**PASS.**

| Check | Result |
|---|---|
| Parseable CSV | Yes |
| Required columns present (ItemID, DeliverableID, Description, Qty, Unit, PricingMode, SourceDoc, SourceSection, Notes) | Yes — all 9 columns present |
| Row count | 5 rows |
| All rows trace to source document and section | Yes |
| PricingMode values valid (UNIT_RATE or LUMP_SUM) | Yes — all 5 rows use UNIT_RATE |
| Qty values | All numeric (6, 4, 27, 21, 12 hours) |
| TBD quantities | 0 |

### Detail.csv

**PASS.**

| Check | Result |
|---|---|
| Parseable CSV | Yes |
| Required columns present (LineID, ItemID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes) | Yes — all 15 columns present |
| Row count | 5 rows |
| Method values valid | Yes — all 5 rows use PARAMETRIC |
| Allowance/parametric convention | N/A — all items are UNIT_RATE with hr quantities; no LS items |
| Amount = Qty x UnitRate verified | L-001: 6 x 165 = 990 (PASS); L-002: 4 x 135 = 540 (PASS); L-003: 27 x 180 = 4860 (PASS); L-004: 21 x 135 = 2835 (PASS); L-005: 12 x 95 = 1140 (PASS) |
| Sum of amounts | 990 + 540 + 4860 + 2835 + 1140 = 10,365 CAD (PASS) |

---

## S6 — Provenance Discipline

**PASS.**

| Metric | Value |
|---|---|
| Total priced rows | 5 |
| Rows with non-TBD SourceRef | 5 (100%) |
| Rows with TBD SourceRef | 0 (0%) |
| Provenance completeness | 100% |

All 5 SourceRef entries reference specific source file + role ID combinations from Professional_Staff_Rates.csv and Level_of_Effort.csv.

**Top missing-source offenders:** None.

---

## S7 — Status Reporting

**RUN_STATUS: OK**

Totals are meaningful. No critical input gaps. All items are priced with full provenance.

---

## S8 — Operator Acceptance Checklist

| Check | Status | Notes |
|---|---|---|
| RUN_STATUS is OK or WARNINGS | OK | No critical gaps |
| Items.csv reviewed for completeness | PASS | 5 items cover all roles from Level_of_Effort.csv for DEL-001-01 |
| Basis-consistency checks pass | PASS | All 5 lines use PARAMETRIC method, matching BASIS_OF_ESTIMATE |
| Provenance completeness reported | 100% | All rows have non-TBD SourceRef |
| Scope coverage explicit | PASS | 1 deliverable (DEL-001-01) in scope; 1 deliverable estimated; 0 excluded |
| No writes outside _Estimates/ | PASS | Verified |

---

## Quantity Takeoff Coverage

| Deliverable | Documents Available | Documents Missing | Items Extracted |
|---|---|---|---|
| DEL-001-01 | Datasheet.md, Specification.md, Guidance.md, Procedure.md | None | 5 |

All four documents were read. Items are professional staff labour hours for the preliminary design phase. No material or equipment items were identified as priceable for this deliverable (DEL-001-01 is a Design Presentation, not a construction deliverable).

---

## Pricing Coverage

| Metric | Value |
|---|---|
| Total items in Items.csv | 5 |
| Items priced in Detail.csv | 5 (100%) |
| Items with TBD amount | 0 (0%) |
| Pricing coverage | 100% |

---

## Basis-Consistency Checks

| Method | Count | % of Lines | Consistent with BASIS_OF_ESTIMATE? |
|---|---|---|---|
| PARAMETRIC | 5 | 100% | Yes |

No mixed methods. All lines are consistent with the declared BASIS_OF_ESTIMATE (PARAMETRIC).

---

## Parametric Cross-Check

Using Professional_Design_Fees.csv and Parametric_Building_Rates.csv as reasonableness checks:

- Construction value estimate: 13,000 sf x $285/sf = $3,705,000 CAD
- Total architectural fee at recommended 4.5%: $166,725 CAD
- DEL-001-01 estimate ($10,365) = 6.2% of total architectural fee
- This is reasonable for a single preliminary design presentation deliverable (1 of 11 deliverables in PKG-001)

---

## What to Fix for a Cleaner Rerun

Nothing required. The run completed with full pricing, full provenance, and no TBD items. Confidence could be improved from MEDIUM to HIGH by:

1. Obtaining firm hourly rate quotes from the design team (replacing parametric rate assumptions)
2. Developing activity-level time estimates (replacing parametric LOE model)
