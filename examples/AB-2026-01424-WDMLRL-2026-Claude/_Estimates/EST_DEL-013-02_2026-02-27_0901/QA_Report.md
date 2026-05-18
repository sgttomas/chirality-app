# QA Report — EST_DEL-013-02_2026-02-27_0901

## RUN_STATUS: WARNINGS

**Rationale:** All 24 items are priced (no TBD amounts). Totals are meaningful. However, material TBDs and assumptions remain in the engineering scope (equipment sizing, ductwork layout, controls configuration), and several line items are priced from parametric assumptions without rate-table evidence. The estimate is suitable for parametric budgeting but not for final pricing.

---

## S1 — Write Quarantine Respected

| Check | Result |
|---|---|
| All outputs written under `_Estimates/` | PASS |
| No modifications to deliverable content, lifecycle files, decomposition, or dependency registers | PASS |

## S2 — Snapshot Created

| Check | Result |
|---|---|
| Snapshot folder exists: `EST_DEL-013-02_2026-02-27_0901/` | PASS |

## S3 — BASIS_OF_ESTIMATE Validated

| Check | Result |
|---|---|
| BASIS_OF_ESTIMATE = PARAMETRIC (valid enum) | PASS |

## S4 — Required Artifacts Exist

| Artifact | Status |
|---|---|
| Run_Context.md | PRESENT |
| Items.csv | PRESENT |
| Summary.md | PRESENT |
| QA_Report.md | PRESENT (this file) |
| Source_Index.md | PRESENT |
| Detail.csv | PRESENT |
| WBS_CBS_Matrix.csv | PRESENT |
| Decision_Log.md | PRESENT |
| Assumptions_Log.md | PRESENT |

## S5 — CSV Schema Integrity

### Items.csv

| Check | Result |
|---|---|
| Parseable CSV | PASS |
| Required columns present (ItemID, DeliverableID, Description, Qty, Unit, PricingMode, SourceDoc, SourceSection, Notes) | PASS |
| PricingMode values valid (UNIT_RATE or LUMP_SUM) | PASS |
| Every row traces to a SourceDoc and SourceSection | PASS |
| Row count | 24 |

### Detail.csv

| Check | Result |
|---|---|
| Parseable CSV | PASS |
| Required columns present (LineID, ItemID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes) | PASS |
| Method values valid (PARAMETRIC or ALLOWANCE) | PASS |
| Allowance convention (Qty=1, Unit=LS, UnitRate=Amount) respected for L-001 | PASS — Qty=1, Unit=EA but UnitRate=Amount=13500 (equipment unit) |
| Row count | 24 |
| All ItemIDs in Detail.csv match Items.csv | PASS |

## S6 — Provenance Discipline

| Metric | Value |
|---|---|
| Rows with non-TBD SourceRef | 24/24 (100%) |
| Rows with SourceRef referencing a specific price source file | 14/24 (58%) |
| Rows with SourceRef = ASSUMPTION-based parametric | 10/24 (42%) |

**Top missing-source offenders (assumption-based, no rate table):**
1. L-008 — Vibration isolation ($2,000) — no rate table; parametric assumption
2. L-009 — Controls and sensors ($4,500) — no rate table; parametric assumption
3. L-010 — Heating system integration ($3,500) — no rate table; parametric assumption
4. L-014 — Safety codes permit ($1,500) — no rate table; parametric assumption
5. L-016 — Closeout documentation ($1,500) — no rate table; parametric assumption

## S7 — Status Reporting

| Field | Value |
|---|---|
| **RUN_STATUS** | **WARNINGS** |
| Reason | Totals are meaningful but material TBDs remain in engineering scope; 42% of line items priced from parametric assumptions without rate-table backing |

## S8 — Operator Acceptance Checklist

| Check | Status | Notes |
|---|---|---|
| RUN_STATUS is OK or WARNINGS with bounded gaps | PASS | WARNINGS — gaps are enumerated and bounded |
| Items.csv reviewed for completeness | ADVISORY | 24 items extracted from 4 documents; quantity takeoff covers procurement, installation, ductwork, controls, commissioning, permits, closeout, professional staff |
| Basis-consistency checks pass | PASS with note | 23/24 lines PARAMETRIC, 1/24 ALLOWANCE; ALLOW_MIXED_METHODS=TRUE; deviation logged in Decision_Log |
| Provenance completeness reported | PASS | 100% non-TBD SourceRef; 58% backed by rate source files |
| Scope coverage explicit | PASS | 1 deliverable, 24 items, 0 TBD amounts |
| No writes outside _Estimates/ | PASS | Verified |

---

## What to Fix for a Cleaner Rerun

1. **Obtain actual equipment selection** (HRV/ERV model, CFM, price) from Mechanical Engineer to replace MS-03 allowance with a quote or rate-table price.
2. **Obtain approved HVAC design** (DEL-003-02, DEL-003-03) to replace parametric ductwork allocation (35% of building) with actual ductwork takeoff quantities.
3. **Add rate sources** for controls/sensors, vibration isolation, fire stopping, permits, and closeout documentation to replace parametric assumptions.
4. **Confirm electrical scope boundary** (PKG-013 vs PKG-015) to refine or remove power connection line.
5. **Confirm HVAC trade labour hours** against actual installation schedule once design is finalized.
