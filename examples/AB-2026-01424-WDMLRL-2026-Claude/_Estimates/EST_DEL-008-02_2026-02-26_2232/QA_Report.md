# QA Report — EST_DEL-008-02_2026-02-26_2232

## RUN_STATUS: WARNINGS

**Rationale:** Totals are meaningful and internally consistent, but material assumptions remain regarding Surveyor hours (parametric, not sourced from LOE) and scope exclusions (equipment, travel, subconsultant, materials). The estimate is suitable as a planning-level professional services labour estimate but requires validation for budget commitment.

---

## S1 — Write Quarantine Respected

**PASS.** All output files written under `_Estimates/EST_DEL-008-02_2026-02-26_2232/`. No files outside `_Estimates/` were modified.

## S2 — Snapshot Created

**PASS.** Snapshot folder `EST_DEL-008-02_2026-02-26_2232` created under `_Estimates/`.

## S3 — BASIS_OF_ESTIMATE Validated

**PASS.** `BASIS_OF_ESTIMATE = PARAMETRIC` is a valid enum value.

## S4 — Required Artifacts Exist

**PASS.** All required artifacts produced:

| Artifact | Status |
|---|---|
| Run_Context.md | Present |
| Items.csv | Present |
| Summary.md | Present |
| QA_Report.md | Present (this file) |
| Source_Index.md | Present |
| Detail.csv | Present |
| WBS_CBS_Matrix.csv | Present |
| Decision_Log.md | Present |
| Assumptions_Log.md | Present |

## S5 — CSV Schema Integrity

### Items.csv

**PASS.**

| Check | Result |
|---|---|
| Parseable CSV | Yes |
| Required columns present (ItemID, DeliverableID, Description, Qty, Unit, PricingMode, SourceDoc, SourceSection, Notes) | Yes |
| All rows trace to a source document and section | Yes (13/13) |
| PricingMode values valid (UNIT_RATE or LUMP_SUM) | Yes |
| Row count | 13 items |

### Detail.csv

**PASS.**

| Check | Result |
|---|---|
| Parseable CSV | Yes |
| Required columns present (LineID, ItemID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes) | Yes |
| Method values valid | Yes — all PARAMETRIC |
| Allowance/parametric convention for LS items | LUMP_SUM items: Qty=1 convention not used; instead hours are used as Qty with UNIT_RATE pricing. This is acceptable because the parametric model uses hourly rates rather than lump-sum amounts. |
| Row count | 13 lines |
| All ItemIDs in Detail.csv exist in Items.csv | Yes (13/13) |

## S6 — Provenance Discipline

**PASS (with notes).**

| Metric | Value |
|---|---|
| Total priced rows | 13 |
| Rows with non-TBD SourceRef | 13 (100%) |
| Rows with `location TBD` SourceRef | 0 |
| Provenance completeness | 100% |

**Note:** While all SourceRefs are populated, 11 of 13 lines (DL-001 through DL-009, DL-012, DL-013) reference parametric estimates for Surveyor hours that are not sourced from the Level_of_Effort.csv. The SourceRef correctly identifies this as "parametric estimate of effort." Only DL-010 (PM) and DL-011 (Cost Estimator) have hours directly sourced from Level_of_Effort.csv.

### Top Missing-Source Offenders

None — all lines have SourceRef populated. The key provenance gap is that Surveyor hour quantities are agent-estimated, not externally sourced.

## S7 — Basis-Consistency Checks

**PASS.**

| Check | Result |
|---|---|
| BASIS_OF_ESTIMATE | PARAMETRIC |
| Methods used in Detail.csv | PARAMETRIC (13/13 lines) |
| Mixed methods present | No — 100% PARAMETRIC |
| ALLOW_MIXED_METHODS | TRUE (not triggered) |
| FALLBACK_POLICY | ALLOW_PARAMETRIC (used for Surveyor hours where LOE was TBD) |

## Quantity Takeoff Coverage

| Metric | Value |
|---|---|
| Deliverables in scope | 1 (DEL-008-02) |
| Documents read | 4 of 4 (Datasheet, Specification, Guidance, Procedure) |
| Missing documents | 0 |
| Items extracted | 13 |
| Items with TBD quantities | 0 (all quantities resolved parametrically) |

## Pricing Coverage

| Metric | Value |
|---|---|
| Total items in Items.csv | 13 |
| Items priced (Amount > 0 or Amount = 0 with justification) | 13 |
| Items with TBD Amount | 0 |
| Pricing coverage | 100% |

## Scope Coverage

| Category | Included | Excluded / Not Estimated |
|---|---|---|
| Professional staff labour (Surveyor) | Yes — 90 hr parametric | |
| Professional staff labour (PM) | Yes — 6 hr from LOE | |
| Professional staff labour (Cost Estimator) | Yes — 4 hr from LOE | |
| Survey equipment costs | | Not included — no equipment rate source provided |
| Travel / mileage / per diem | | Not included — no travel rate source provided |
| ALS subconsultant fees | | Not included — boundary scope TBD |
| Survey monument materials | | Not included — no material rate source provided |
| Printing / plotting | | Not included — nominal |
| Insurance / bonding | | Not included — project-level cost |

---

## What to Fix for a Cleaner Rerun

1. **Provide Surveyor (R-21) hours in Level_of_Effort.csv for DEL-008-02.** The current LOE entry has TBD notes. A licensed surveyor should validate the 90-hour parametric estimate or provide their own estimate by activity.

2. **Resolve boundary survey scope decision.** Confirm with Owner whether a full legal ALS boundary survey is required (affects hours and may require a subconsultant line).

3. **Add equipment and travel rate sources** if the estimate should cover more than professional labour.

4. **Add a crew size parameter** to Assumed_Project_Parameters.csv or Level_of_Effort.csv to resolve the single-person vs. two-person crew assumption.

5. **Resolve TBD Datasheet attributes** (datum, coordinate system, accuracy class, mapping scale, control point count) to confirm scope does not expand beyond current assumptions.
