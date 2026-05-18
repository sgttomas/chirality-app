# QA Report — EST_DEL-011-01_2026-02-27_0845

## RUN_STATUS: WARNINGS

**Rationale:** Totals are meaningful and cover the full scope of DEL-011-01 Concrete Superstructure. However, material TBDs remain in structural system type, concrete strength, roof system, mezzanine loads, and geotechnical conditions. These TBDs are bounded and quantified in warnings.

---

## S1 -- Write Quarantine Respected

| Check | Result |
|---|---|
| All files written under `_Estimates/EST_DEL-011-01_2026-02-27_0845/` | PASS |
| No files modified outside `_Estimates/` | PASS |

---

## S2 -- Snapshot Created

| Check | Result |
|---|---|
| Snapshot folder `EST_DEL-011-01_2026-02-27_0845` exists | PASS |

---

## S3 -- BASIS_OF_ESTIMATE Validated

| Check | Result |
|---|---|
| `BASIS_OF_ESTIMATE = PARAMETRIC` | PASS (valid enum) |

---

## S4 -- Required Artifacts Exist

| Artifact | Status |
|---|---|
| `Run_Context.md` | PRESENT |
| `Items.csv` | PRESENT |
| `Summary.md` | PRESENT |
| `QA_Report.md` | PRESENT (this file) |
| `Source_Index.md` | PRESENT |
| `Detail.csv` | PRESENT |
| `WBS_CBS_Matrix.csv` | PRESENT |
| `Decision_Log.md` | PRESENT |
| `Assumptions_Log.md` | PRESENT |

---

## S5 -- CSV Schema Integrity

### Items.csv

| Check | Result |
|---|---|
| Parseable CSV | PASS |
| Required columns present (ItemID, DeliverableID, Description, Qty, Unit, PricingMode, SourceDoc, SourceSection, Notes) | PASS |
| All PricingMode values valid (UNIT_RATE or LUMP_SUM) | PASS |
| Every row traces to SourceDoc and SourceSection | PASS |
| No TBD quantities (all items have numeric Qty) | PASS |
| Row count | 33 items |

### Detail.csv

| Check | Result |
|---|---|
| Parseable CSV | PASS |
| Required columns present (LineID, ItemID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes) | PASS |
| All Method values valid (PARAMETRIC or ALLOWANCE) | PASS |
| Allowance/parametric convention respected (Qty=1, Unit=LS, UnitRate=Amount for LS items) | PASS |
| All ItemIDs in Detail.csv trace to Items.csv | PASS |
| Row count | 33 lines |

---

## S6 -- Provenance Discipline

| Metric | Value |
|---|---|
| Total priced lines | 33 |
| Lines with non-TBD SourceRef | 33 (100%) |
| Lines with `location TBD` SourceRef | 0 |
| **Provenance completeness** | **100%** |

All 33 lines have a SourceRef pointing to a specific pricing source file and item ID, or to a derivation note with source context.

### Top Missing-Source Offenders

None. All lines have provenance.

---

## S7 -- Pricing Coverage

| Metric | Value |
|---|---|
| Items extracted (Items.csv) | 33 |
| Items priced (Detail.csv with Amount != TBD) | 33 |
| Items with TBD Amount | 0 |
| **Pricing coverage** | **100%** |

---

## S8 -- Basis-Consistency Checks

| Check | Result |
|---|---|
| Primary basis: PARAMETRIC | 30 lines ($2,238,902 / 98.9%) |
| Fallback: ALLOWANCE | 3 lines ($25,000 / 1.1%) |
| ALLOW_MIXED_METHODS = TRUE | PASS -- mixed methods permitted |
| FALLBACK_POLICY = ALLOW_PARAMETRIC | PASS -- ALLOWANCE items logged in Decision_Log |
| Deviations from primary basis | 3 ALLOWANCE items (L-003 steel plates, L-017 cistern provisions, L-021 cold weather) -- all logged |

---

## Quantity Takeoff Coverage

| Deliverable | Documents Read | Missing Documents | Items Extracted |
|---|---|---|---|
| DEL-011-01 | Datasheet.md, Specification.md, Guidance.md, Procedure.md | None | 33 |

All four production documents were available and read. No missing documents.

### Scope Coverage

| Element from Datasheet/Specification | Covered in Items.csv | Notes |
|---|---|---|
| Concrete structural frame (walls/columns) | ITM-007 | Covered |
| Concrete floor slab | ITM-001 | Covered |
| Thickened slab edge / grade beam | ITM-002 | Covered |
| Steel plate embedments | ITM-003 | Covered |
| Service pit/trench | ITM-004 | Covered |
| Mezzanine structure | ITM-005 | Covered |
| Mezzanine stair | ITM-006 | Covered |
| Crane runway supports | ITM-008 | Covered |
| Roof structure | ITM-009 | Covered |
| OH door structural openings (repair bays) | ITM-010 | Covered |
| OH door structural opening (wash bay) | ITM-011 | Covered |
| Entrance/exit doors | ITM-012 | Covered |
| Building envelope -- wall panels | ITM-013 | Covered |
| Building envelope -- roof panels | ITM-014 | Covered |
| Flashing/trim/sealants | ITM-015 | Covered |
| Windows | ITM-016 | Covered |
| Cistern structural provisions | ITM-017 | Covered |
| Reinforcing steel (rebar) | ITM-018 | Covered |
| Formwork | ITM-019 | Covered |
| Concrete testing/QA | ITM-020 | Covered |
| Cold-weather provisions | ITM-021 | Covered |
| Professional staff (6 roles) | ITM-022 to ITM-027 | Covered |
| Construction labour (4 trades) | ITM-028 to ITM-031 | Covered |
| Equipment | ITM-032 | Covered |
| Survey/as-built | ITM-033 | Covered |

### Excluded Items (correctly excluded per scope)

- Foundation construction (DEL-010-01 / PKG-010)
- Crane supply and installation (DEL-016-01 / PKG-016)
- Interior fit-out (PKG-012)
- MEP rough-in (PKG-013, PKG-014, PKG-015)
- Wash bay structural enclosure (DEL-011-05 per SOW-0027a)
- OH door supply/install (DEL-011-03, DEL-011-05)
- Cistern supply/install (DEL-014-01)

---

## Confidence Distribution

| Confidence | Lines | Amount (CAD) | % of Total |
|---|---|---|---|
| MED | 30 | $2,238,902.00 | 98.9% |
| LOW | 3 | $25,000.00 | 1.1% |
| HIGH | 0 | $0.00 | 0.0% |

---

## What to Fix for a Cleaner Rerun

1. **Confirm structural system type** (CIP vs. tilt-up vs. precast) -- this would refine the structural frame unit rate ($420/m2 baseline) and could change the total by +/-20%.
2. **Confirm concrete f'c** from DEL-002-10 -- higher strength concrete increases unit rates.
3. **Confirm roof system** -- steel deck/bar joist vs. concrete roof changes the $175K roof line.
4. **Obtain mezzanine design live load** from DEL-002-10 -- refines mezzanine pricing.
5. **Obtain geotechnical report** (DEL-008-01) -- may affect slab thickness and grade beam sizing.
6. **Confirm steel plate embedment count** from DEL-002-08 design -- currently estimated at 20 EA.
7. **Confirm overhead door sizes** from DEL-001-07 door schedule -- refines structural opening costs.
8. **Confirm window glazing area** from architectural design -- currently estimated at 20 m2.
9. **Elevate ALLOWANCE items** (L-003, L-017, L-021) to PARAMETRIC with specific rates when design details are available.
10. **Confirm entrance/exit door count** -- currently assumed at 4 EA based on typical shop layout.

---

## Operator Acceptance Checklist (S8)

| Criterion | Status |
|---|---|
| RUN_STATUS is OK or WARNINGS with bounded gaps | WARNINGS -- all gaps are identified, bounded, and actionable |
| Quantity takeoff reviewed for completeness | 33 items covering all scope elements; no missing scope |
| Basis-consistency checks pass or deviations approved/logged | 3 ALLOWANCE deviations logged in Decision_Log.md; per ALLOW_MIXED_METHODS=TRUE |
| Provenance completeness reported | 100% of lines have SourceRef |
| Scope coverage explicit | Inclusions and exclusions documented above |
| No writes outside _Estimates/ | Confirmed |
