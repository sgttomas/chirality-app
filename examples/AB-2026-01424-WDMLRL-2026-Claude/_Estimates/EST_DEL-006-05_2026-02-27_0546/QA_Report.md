# QA Report — EST_DEL-006-05_2026-02-27_0546

## RUN_STATUS: OK

Totals are meaningful; no critical input gaps. All line items are priced with full provenance.

---

## S1 — Write Quarantine Respected

| Check | Result |
|---|---|
| All outputs written under `_Estimates/EST_DEL-006-05_2026-02-27_0546/` | PASS |
| No files modified outside `_Estimates/` | PASS |

## S2 — Snapshot Created

| Check | Result |
|---|---|
| Snapshot folder exists | PASS |
| Folder name follows convention `EST_{LABEL}_{DATE}_{TIME}` | PASS |

## S3 — BASIS_OF_ESTIMATE Validated

| Check | Result |
|---|---|
| BASIS_OF_ESTIMATE = PARAMETRIC | PASS (valid enum value) |
| All Detail.csv Method values consistent with basis | PASS (all 4 lines = PARAMETRIC) |

## S4 — Required Artifacts Exist

| Artifact | Status |
|---|---|
| Run_Context.md | PASS |
| Items.csv | PASS |
| Summary.md | PASS |
| QA_Report.md | PASS (this file) |
| Source_Index.md | PASS |
| Detail.csv | PASS (optional; produced) |
| WBS_CBS_Matrix.csv | PASS |
| Decision_Log.md | PASS |
| Assumptions_Log.md | PASS |

## S5 — CSV Schema Integrity

### Items.csv

| Check | Result |
|---|---|
| Parseable CSV | PASS |
| Required columns present (ItemID, DeliverableID, Description, Qty, Unit, PricingMode, SourceDoc, SourceSection, Notes) | PASS |
| All rows trace to source document and section | PASS (4/4 rows) |
| PricingMode values valid (UNIT_RATE or LUMP_SUM) | PASS (all 4 rows = UNIT_RATE) |
| Row count | 4 |

### Detail.csv

| Check | Result |
|---|---|
| Parseable CSV | PASS |
| Required columns present (LineID, ItemID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes) | PASS |
| Method values valid (PARAMETRIC for all) | PASS |
| Allowance/parametric convention (Qty=1, Unit=LS, UnitRate=Amount) | N/A — all items are UNIT_RATE with actual quantities |
| All ItemIDs trace to Items.csv | PASS (ITEM-001 through ITEM-004) |
| Row count | 4 |

### Arithmetic Verification

| LineID | Qty | UnitRate | Expected Amount | Actual Amount | Check |
|---|---|---|---|---|---|
| LN-001 | 49 | 160 | 7,840 | 7,840 | PASS |
| LN-002 | 21 | 95 | 1,995 | 1,995 | PASS |
| LN-003 | 6 | 165 | 990 | 990 | PASS |
| LN-004 | 4 | 135 | 540 | 540 | PASS |
| **TOTAL** | | | **11,365** | **11,365** | **PASS** |

## S6 — Provenance Discipline

| Metric | Value |
|---|---|
| Total priced rows | 4 |
| Rows with non-TBD SourceRef | 4 |
| Provenance completeness | 100% |
| Rows with TBD SourceRef | 0 |
| Top missing-source offenders | None |

All SourceRef entries point to specific rows in Level_of_Effort.csv (for hours) cross-referenced with Professional_Staff_Rates.csv (for hourly rates).

## S7 — Status Reporting

| Field | Value |
|---|---|
| RUN_STATUS | OK |
| Rationale | All 4 line items priced; no TBD amounts; 100% provenance completeness; basis consistency is clean (all PARAMETRIC) |

## S8 — Operator Acceptance Checklist

| Check | Status | Notes |
|---|---|---|
| RUN_STATUS is OK or WARNINGS | OK | No material gaps |
| Items.csv reviewed for completeness | 4 items identified from 4 documents | Design labour deliverable; scope is professional services only |
| Basis-consistency checks pass | PASS | All lines PARAMETRIC; matches BASIS_OF_ESTIMATE |
| Provenance completeness reported | 100% | No gaps |
| Scope coverage explicit | 1 deliverable (DEL-006-05) in scope; 0 excluded | Single-deliverable run |
| No writes outside _Estimates/ | Confirmed | PASS |

## Quantity Takeoff Coverage

| Document | Items Extracted | Notes |
|---|---|---|
| Datasheet.md | Context for scope | Tank attributes, conditions, construction elements informed item scoping |
| Specification.md | Context for scope | Requirements REQ-001 through REQ-010 confirmed drawing set scope |
| Guidance.md | Context for scope | Principles confirmed holding-tank-only scope; trade-offs and coordination dependencies noted |
| Procedure.md | Primary extraction source | Steps 1-7 defined the work activities mapped to labour roles |
| Level_of_Effort.csv | 4 rows (R-01, R-08, R-13, R-18) | Direct quantity source for hours per role |

## Pricing Coverage

| Metric | Value |
|---|---|
| Total items in Items.csv | 4 |
| Items priced (non-TBD Amount) | 4 |
| Items with TBD Amount | 0 |
| Pricing coverage | 100% |

## What to Fix for a Cleaner Rerun

Nothing required. This run completed cleanly with full coverage. For future refinement:

1. If actual plumbing engineer fee proposals or quotes become available, a rerun with BASIS_OF_ESTIMATE=QUOTE would replace parametric estimates with firm pricing.
2. The construction cost for the physical septic system (tank procurement, excavation, installation, existing tank removal) is not within the scope of this design deliverable estimate. Those costs should be estimated under DEL-014-02 / PKG-014 with appropriate construction rate sources.
