# QA Report — EST_DEL-015-02_2026-02-27_0848

## RUN_STATUS: WARNINGS

**Rationale:** Totals are meaningful and all 29 line items are priced (no TBD amounts). However, material assumptions remain for several line items where price sources lack direct rates (8-foot LED linear fixtures, mounting hardware, branch circuit wiring, switching/controls). Multiple design parameters are TBD pending IFC drawings, which may materially change quantities or rates upon resolution.

---

## S1 — Write Quarantine Respected

**PASS.** All outputs written exclusively under `_Estimates/EST_DEL-015-02_2026-02-27_0848/`. No files outside the estimating tool root were modified.

---

## S2 — Snapshot Created

**PASS.** Snapshot folder `EST_DEL-015-02_2026-02-27_0848` created under `_Estimates/`.

---

## S3 — BASIS_OF_ESTIMATE Validated

**PASS.** `BASIS_OF_ESTIMATE = PARAMETRIC` is a valid enum value.

---

## S4 — Required Artifacts Exist

**PASS.** All required files present:

| File | Status |
|---|---|
| Run_Context.md | Present |
| Items.csv | Present |
| Summary.md | Present |
| QA_Report.md | Present (this file) |
| Source_Index.md | Present |
| Decision_Log.md | Present |
| Assumptions_Log.md | Present |
| WBS_CBS_Matrix.csv | Present |
| Detail.csv | Present (optional; produced) |
| Risk_Register.md | Present (optional; produced) |

---

## S5 — CSV Schema Integrity

### Items.csv

**PASS.** 29 rows parsed successfully.

| Check | Result |
|---|---|
| Required columns present | PASS (ItemID, DeliverableID, Description, Qty, Unit, PricingMode, SourceDoc, SourceSection, Notes) |
| All ItemIDs unique | PASS (ITM-001 through ITM-029) |
| All DeliverableIDs = DEL-015-02 | PASS |
| PricingMode values valid | PASS (UNIT_RATE: 26 rows; LUMP_SUM: 3 rows) |
| Lump-sum convention (Qty=1, Unit=LS) | PASS (ITM-009, ITM-010, ITM-011, ITM-012, ITM-013 all have Qty=1, Unit=LS) |
| All rows have SourceDoc | PASS (Datasheet: 8; Specification: 7; Procedure: 14) |
| All rows have SourceSection | PASS |
| Qty values: TBD count | 0 (all numeric) |

### Detail.csv

**PASS.** 29 rows parsed successfully.

| Check | Result |
|---|---|
| Required columns present | PASS (LineID, ItemID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes) |
| All LineIDs unique | PASS (DL-001 through DL-029) |
| All ItemIDs trace to Items.csv | PASS |
| Method values valid | PASS (PARAMETRIC: 28; ALLOWANCE: 1) |
| Allowance convention (DL-012: Qty=1, Unit=LS, UnitRate=Amount) | PASS |
| Currency consistency | PASS (all CAD) |
| Amount = TBD count | 0 |

---

## S6 — Provenance Discipline

**PASS (with note).**

| Metric | Value |
|---|---|
| Total priced rows | 29 |
| Rows with full SourceRef | 28 (96.6%) |
| Rows with partial/assumption SourceRef | 1 (3.4%) |
| Rows with `location TBD` | 0 |

### Top Missing-Source Offenders

| LineID | Description | Issue |
|---|---|---|
| DL-012 | Switching/controls devices and installation | SourceRef points to Assumptions_Log A-007 (allowance basis); no rate table or parametric model available because controls strategy is TBD per Spec REQ-L-14 |

All other 28 lines reference specific rate table entries (Electrical_System_Rates.csv, Construction_Labour_Rates.csv, Professional_Staff_Rates.csv, Level_of_Effort.csv) or documented parametric assumptions with IDs.

---

## S7 — Status Reporting

**RUN_STATUS: WARNINGS**

Summary of warning conditions:
1. 1 of 29 lines priced as ALLOWANCE (DL-012: switching/controls) with LOW confidence
2. 7 lines rely on parametric assumptions not backed by provided rate tables (DL-002 through DL-011, DL-013)
3. Multiple design parameters TBD pending IFC drawings (see Datasheet §Unresolved Design Parameters Register)
4. Emergency/exit lighting scope unresolved and excluded
5. Ceiling fan coordination interface unresolved

---

## Quantity Takeoff Coverage

| Deliverable | Documents Read | Documents Missing | Items Extracted |
|---|---|---|---|
| DEL-015-02 | 4 of 4 (Datasheet, Specification, Guidance, Procedure) | 0 | 29 |

### Item Extraction by Source Document

| SourceDoc | Item Count |
|---|---|
| Datasheet | 8 (fixtures, mounting hardware) |
| Specification | 7 (professional staff oversight, general requirements) |
| Procedure | 14 (labour activities, equipment, coordination) |
| Guidance | 0 (informs assumptions; no direct priceable items) |

---

## Pricing Coverage

| Metric | Value |
|---|---|
| Items priced | 29 of 29 (100%) |
| Items TBD | 0 |
| Lines PARAMETRIC | 28 (96.6%) |
| Lines ALLOWANCE | 1 (3.4%) |

---

## Basis-Consistency Checks

| Check | Result |
|---|---|
| BASIS_OF_ESTIMATE = PARAMETRIC | PASS |
| ALLOW_MIXED_METHODS = TRUE | Applied; 1 ALLOWANCE line permitted |
| FALLBACK_POLICY = ALLOW_PARAMETRIC | Applied; parametric assumptions used for items without direct rate table entries |
| Method mix: PARAMETRIC dominant | PASS (28 of 29 = 96.6%) |
| ALLOWANCE line logged in Decision_Log | PASS (D-009, D-011) |

---

## What to Fix for a Cleaner Rerun

1. **Add 8-foot LED linear fixture rate** to Electrical_System_Rates.csv to eliminate A-003 assumption
2. **Add mounting hardware rates** to Electrical_System_Rates.csv to eliminate A-004, A-005 assumptions
3. **Add branch circuit wiring rates** (per-fixture or per-metre) to eliminate A-006 assumption
4. **Resolve switching/controls strategy** (Owner decision per REQ-L-14) to replace ALLOWANCE DL-012 with PARAMETRIC pricing
5. **Add aerial platform rental rate** to price sources to eliminate A-008 assumption
6. **Resolve emergency/exit lighting scope** (Owner + AHJ per REQ-L-15) to either include or formally exclude from estimate
7. **Resolve ceiling fan ownership** (CONF-L-03) to eliminate coordination risk RSK-005
8. **Obtain IFC drawings** to replace TBD design parameters with confirmed values (fixture models, conduit types, panel assignments, circuit breaker sizes)

---

## Operator Acceptance Checklist (S8)

| Check | Status |
|---|---|
| RUN_STATUS is OK or WARNINGS with bounded gaps | PASS (WARNINGS; gaps are clearly identified and bounded) |
| Items.csv reviewed for completeness | 29 items extracted from 4 documents; all 5 lighting zones covered |
| Basis-consistency checks pass | PASS (28 PARAMETRIC + 1 ALLOWANCE; mix explicitly authorized) |
| Provenance completeness reported | 96.6%; 1 offender identified (DL-012) |
| Scope coverage explicit | 1 deliverable (DEL-015-02); exclusions documented (emergency lighting, Old North Shop, ceiling fans) |
| No writes outside _Estimates/ | CONFIRMED |
