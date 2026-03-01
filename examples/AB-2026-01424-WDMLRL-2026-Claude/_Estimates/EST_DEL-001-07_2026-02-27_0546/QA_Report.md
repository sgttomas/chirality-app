# QA Report — EST_DEL-001-07_2026-02-27_0546

**RUN_STATUS: OK**

---

## S1 — Write Quarantine Respected

**PASS.** All output files are written exclusively under `_Estimates/EST_DEL-001-07_2026-02-27_0546/`. No files outside the estimating tool root were modified.

---

## S2 — Snapshot Created

**PASS.** Snapshot folder `EST_DEL-001-07_2026-02-27_0546` created under `_Estimates/`.

---

## S3 — BASIS_OF_ESTIMATE Validated

**PASS.** `BASIS_OF_ESTIMATE = PARAMETRIC` is a valid enum value (one of: QUOTE, RATE_TABLE, HISTORICAL, PARAMETRIC, ALLOWANCE).

---

## S4 — Required Artifacts Exist

**PASS.** All required artifacts are present:

| Artifact | Status |
|---|---|
| Run_Context.md | Present |
| Items.csv | Present |
| Detail.csv | Present |
| Summary.md | Present |
| QA_Report.md | Present (this file) |
| Source_Index.md | Present |
| WBS_CBS_Matrix.csv | Present |
| Decision_Log.md | Present |
| Assumptions_Log.md | Present |

---

## S5 — CSV Schema Integrity

### Items.csv

**PASS.**

- **Columns present:** ItemID, DeliverableID, Description, Qty, Unit, PricingMode, SourceDoc, SourceSection, Notes (all 9 required columns)
- **Row count:** 5 items
- **PricingMode values:** All UNIT_RATE (valid)
- **Source traceability:** All 5 rows reference Procedure as SourceDoc with specific step references in SourceSection
- **Qty values:** All numeric (no TBD entries)

### Detail.csv

**PASS.**

- **Columns present:** LineID, ItemID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes (all 15 required columns)
- **Row count:** 5 lines
- **Method values:** All PARAMETRIC (valid; consistent with BASIS_OF_ESTIMATE)
- **Amount values:** All numeric (no TBD entries)
- **Arithmetic check:** All Amount = Qty x UnitRate (verified for all 5 lines)
  - L-001: 6 x 165 = 990
  - L-002: 4 x 135 = 540
  - L-003: 18 x 180 = 3,240
  - L-004: 14 x 135 = 1,890
  - L-005: 8 x 95 = 760
- **Total:** 990 + 540 + 3,240 + 1,890 + 760 = $7,420 CAD

---

## S6 — Provenance Discipline

**PASS.**

- **Provenance completeness:** 5/5 rows (100%) have non-TBD SourceRef values
- **All SourceRef entries** reference both the rate source (Professional_Staff_Rates.csv with RoleID) and the hours source (Level_of_Effort.csv with DeliverableID/RoleID)
- **No missing-source offenders.**

---

## S7 — Status Reporting

**RUN_STATUS: OK**

Totals are meaningful. No critical input gaps. All 5 line items are priced using the primary PARAMETRIC method with full provenance. No TBD amounts remain.

---

## Quantity Takeoff Coverage

| Deliverable | Documents Available | Documents Read | Items Extracted | Notes |
|---|---|---|---|---|
| DEL-001-07 | 4 of 4 | 4 of 4 | 5 | All four documents present and read: Datasheet.md, Specification.md, Guidance.md, Procedure.md |

- **Missing documents:** None
- **Item extraction approach:** DEL-001-07 is a design-phase schedule deliverable. Items represent professional services effort (staff hours by role) to produce the schedule, not the physical door/window units themselves. The physical doors and windows would be priced as construction items in construction packages (PKG-011, PKG-012, PKG-017).

---

## Pricing Coverage

| Metric | Value |
|---|---|
| Total items in Items.csv | 5 |
| Items priced (non-TBD Amount) | 5 |
| Items with TBD Amount | 0 |
| **Pricing coverage** | **100%** |

---

## Basis-Consistency Check

| Metric | Value |
|---|---|
| BASIS_OF_ESTIMATE | PARAMETRIC |
| ALLOW_MIXED_METHODS | TRUE |
| Method values in Detail.csv | PARAMETRIC (5/5) |
| Non-basis methods used | None |
| Fallback methods used | None |
| **Basis consistency** | **100% consistent** |

---

## What to Fix for a Cleaner Rerun

No fixes required. This run produced a complete, consistent estimate with full provenance coverage.

Potential improvements for future iterations:
1. **Activity-level LOE build-up:** Replace parametric hours-by-deliverable-type with hours estimated per procedure step (e.g., Step 1 Code Analysis = X hrs Senior Architect, Step 2 Owner Confirmation = Y hrs PM). This would increase confidence from MEDIUM to HIGH.
2. **Firm rate quotes:** Replace parametric staff rates with firm quotes from the project team's professional services agreements for HIGH confidence.
3. **Scope refinement:** The Datasheet identifies 12+ door openings and conditional window requirements. A more refined estimate could adjust hours based on the actual complexity of the code analysis and the number of coordination interfaces required.
