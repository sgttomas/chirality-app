# QA Report — EST_DEL-002-11_2026-02-27_0600

## RUN_STATUS: WARNINGS

**Rationale:** Totals are meaningful — all 4 role-based line items are priced from PARAMETRIC sources with full provenance. However, material assumptions and TBDs remain (variable-price scope subject to post-geotech revision; peer reviewer hours embedded rather than explicit; design fee cross-check not possible without construction value). Status is WARNINGS rather than OK.

---

## S1 — Write Quarantine Respected

**PASS.** All files written exclusively under `_Estimates/EST_DEL-002-11_2026-02-27_0600/`. No files outside the estimating tool root were modified.

## S2 — Snapshot Created

**PASS.** Snapshot folder `EST_DEL-002-11_2026-02-27_0600` created under `_Estimates/`.

## S3 — BASIS_OF_ESTIMATE Validated

**PASS.** `BASIS_OF_ESTIMATE = PARAMETRIC` — valid enum value. All 4 Detail.csv lines use `Method=PARAMETRIC`, consistent with basis.

## S4 — Required Artifacts Exist

**PASS.** All required files present:

| File | Status |
|---|---|
| Run_Context.md | Present |
| Items.csv | Present |
| Summary.md | Present |
| QA_Report.md | Present (this file) |
| Source_Index.md | Present |
| Detail.csv | Present (optional but produced) |
| WBS_CBS_Matrix.csv | Present |
| Decision_Log.md | Present |
| Assumptions_Log.md | Present |

## S5 — CSV Schema Integrity

### Items.csv

**PASS.**

- Columns present: ItemID, DeliverableID, Description, Qty, Unit, PricingMode, SourceDoc, SourceSection, Notes
- 14 rows; all rows trace to a source document (Procedure or Specification) and section
- PricingMode values: UNIT_RATE (4 rows), LUMP_SUM (10 rows) — all valid

### Detail.csv

**PASS.**

- Columns present: LineID, ItemID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes
- 4 rows; all Method values = PARAMETRIC — valid
- No ALLOWANCE or PARAMETRIC convention violations (all lines use Qty > 1 with hr units, standard UNIT_RATE pricing)
- All Amount values are computable: Qty x UnitRate = Amount (verified: 6x165=990, 4x135=540, 21x95=1995, 49x170=8330)

## S6 — Provenance Discipline

**PASS.**

- 4 of 4 priced rows (100%) have non-TBD SourceRef values
- All SourceRef values point to specific source files (Level_of_Effort.csv row + Professional_Staff_Rates.csv role ID)
- No "location TBD" entries in Detail.csv
- **Top missing-source offenders:** None

### Provenance Completeness

| Metric | Value |
|---|---|
| Total priced rows | 4 |
| Rows with SourceRef | 4 (100%) |
| Rows with "location TBD" | 0 (0%) |

## S7 — Status Reporting

**PASS.** RUN_STATUS declared as `WARNINGS` (see top of this report). Rationale provided.

### Warning Summary

| Warning ID | Description | Severity |
|---|---|---|
| W-001 | Variable-price scope: foundation design hours may increase post-geotech if conditions differ from assumed normal | MEDIUM |
| W-002 | Peer reviewer hours embedded in R-14 LOE; not broken out separately | LOW |
| W-003 | Design fee cross-check (Professional_Design_Fees.csv DF-02) not possible without construction value base | LOW |
| W-004 | Items ITEM-005 through ITEM-014 are tracking items at $0 — their scope is absorbed in ITEM-001 through ITEM-004 | INFO |

## S8 — Operator Acceptance Checklist

| Check | Status | Notes |
|---|---|---|
| RUN_STATUS is OK or WARNINGS with clearly bounded gaps | PASS | WARNINGS — gaps are bounded and documented |
| Quantity takeoff (Items.csv) reviewed for completeness | PASS | 14 items extracted covering all Procedure phases, Specification requirements, and anticipated artifacts |
| Basis-consistency checks pass | PASS | All 4 Detail.csv lines use PARAMETRIC method; matches BASIS_OF_ESTIMATE |
| Provenance completeness reported | PASS | 100% provenance on all priced lines |
| Scope coverage explicit | PASS | 1 deliverable (DEL-002-11) in scope; exclusions stated in Summary.md (construction costs excluded; geotech excluded) |
| No writes outside _Estimates/ | PASS | Confirmed |

---

## Quantity Takeoff Coverage

| Deliverable | Documents Read | Items Extracted | Priced Items | Tracking Items |
|---|---|---|---|---|
| DEL-002-11 | 4 of 4 (Datasheet, Specification, Guidance, Procedure) | 14 | 4 (ITEM-001 through ITEM-004) | 10 (ITEM-005 through ITEM-014) |

### Missing Documents

None. All four production documents were present and read.

---

## Pricing Coverage

| Metric | Value |
|---|---|
| Total priceable items (role-based) | 4 |
| Items priced | 4 (100%) |
| Items TBD | 0 (0%) |
| Total tracking items (absorbed in role-based) | 10 |
| Total estimated amount | $11,855 CAD |
| Total estimated hours | 80 hr |

---

## What to Fix for a Cleaner Rerun

1. **Resolve construction value for design fee cross-check.** If a construction value estimate for the variable-price foundation scope becomes available, re-run with that value to enable a cross-check against Professional_Design_Fees.csv DF-02 (structural design fee 1.2%–2.5% of construction value).

2. **Break out peer reviewer hours.** If a separate peer reviewer is engaged (as implied by Procedure Step 2.7), their hours should be added to Level_of_Effort.csv as a distinct role (e.g., R-20 Geotechnical Engineer or a senior structural reviewer) for a cleaner LOE breakdown.

3. **Post-geotech re-estimate.** After DEL-008-01 is received, re-run the estimate with updated scope if the geotechnical findings require material changes to the foundation design approach.
