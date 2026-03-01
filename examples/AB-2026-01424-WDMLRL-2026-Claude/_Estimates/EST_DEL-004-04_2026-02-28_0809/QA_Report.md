# QA Report — EST_DEL-004-04_2026-02-28_0809

## RUN_STATUS: WARNINGS

**Rationale:** The design professional services LOE is fully priced ($18,810.00 CAD) with complete provenance. Hardware reference items (DL-005 through DL-010) are resolved to $0 with rationale documented in Decision_Log (DEC-R01). However, 1 of 15 line items (DL-015 emergency/exit lighting) carries a TBD amount, and 3 unresolved conflicts (CONF-LT-001, CONF-LT-002, CONF-LT-003) affect scope completeness. The priced total of $18,810 is meaningful and complete for the design-fee component, with 1 residual TBD.

---

## S1 — Write Quarantine Respected

| Check | Result |
|---|---|
| All outputs written under `_Estimates/EST_DEL-004-04_2026-02-28_0809/` | PASS |
| No files modified outside `_Estimates/` | PASS |

## S2 — Snapshot Created

| Check | Result |
|---|---|
| Snapshot folder `EST_DEL-004-04_2026-02-28_0809` exists | PASS |

## S3 — BASIS_OF_ESTIMATE Validated

| Check | Result |
|---|---|
| BASIS_OF_ESTIMATE = PARAMETRIC | PASS (valid enum value) |

## S4 — Required Artifacts Exist

| Artifact | Status |
|---|---|
| Run_Context.md | PASS |
| Items.csv | PASS |
| Summary.md | PASS |
| QA_Report.md | PASS (this file) |
| Source_Index.md | PASS |
| Detail.csv | PASS |
| WBS_CBS_Matrix.csv | PASS |
| Decision_Log.md | PASS |
| Assumptions_Log.md | PASS |

## S5 — CSV Schema Integrity

### Items.csv

| Check | Result |
|---|---|
| Parseable CSV | PASS |
| Required columns present (ItemID, DeliverableID, Description, Qty, Unit, PricingMode, SourceDoc, SourceSection, Notes) | PASS |
| All rows trace to SourceDoc + SourceSection | PASS |
| PricingMode values valid (UNIT_RATE or LUMP_SUM) | PASS |
| Row count | 15 items |
| Unchanged from prior snapshot | PASS (copied as-is) |

### Detail.csv

| Check | Result |
|---|---|
| Parseable CSV | PASS |
| Required columns present (LineID, ItemID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes) | PASS |
| Method values valid | PASS -- all are PARAMETRIC |
| Allowance/parametric convention | PASS -- lump-sum items (DL-010 through DL-015) have Qty=1, Unit=LS |
| ItemID traceability to Items.csv | PASS -- all 15 ItemIDs match |
| TBD resolution | PASS -- 6 of 7 prior TBDs resolved (DL-005 through DL-010 set to $0); 1 residual TBD (DL-015) |

## S6 — Provenance Discipline

### Provenance Completeness

| Metric | Value |
|---|---|
| Total Detail.csv rows | 15 |
| Rows with non-TBD SourceRef | 15 (100%) |
| Rows with priced Amount (non-TBD) | 14 of 15 (93%) |
| Rows with TBD Amount | 1 of 15 (7%) |

### Improvement from Prior Snapshot

| Metric | Prior (0627) | Current (0809) | Delta |
|---|---|---|---|
| Priced rows | 8 of 15 (53%) | 14 of 15 (93%) | +6 rows |
| TBD rows | 7 of 15 (47%) | 1 of 15 (7%) | -6 rows |

### Residual TBD Items

| LineID | Description | Gap |
|---|---|---|
| DL-015 | Emergency/exit lighting assessment | Scope applicability TBD (CONF-LT-003); conditional allowance ~$5,800 noted |

**Note:** All 6 hardware reference TBDs (DL-005 through DL-010) have been resolved to $0 with rationale: hardware cost is in PKG-015 Electrical Installation scope, not PKG-004 design-fee scope. The sole remaining TBD is DL-015 (emergency/exit lighting), which depends on Alberta Building Code review.

## S7 — Status Reporting

| Field | Value |
|---|---|
| RUN_STATUS | **WARNINGS** |
| Rationale | Design professional services total ($18,810) is meaningful and fully provenanced. Hardware reference items resolved to $0 with documented rationale. One residual TBD (DL-015 emergency/exit lighting) depends on code review (CONF-LT-003). Three unresolved design conflicts (CONF-LT-001/002/003) affect scope completeness but do not invalidate the design LOE estimate. |

## S8 — Operator Acceptance Checklist

| Criterion | Status | Notes |
|---|---|---|
| RUN_STATUS is OK or WARNINGS with bounded gaps | PASS | WARNINGS -- 1 bounded TBD (DL-015) with conditional allowance noted |
| Quantity takeoff (Items.csv) reviewed for completeness | PASS | 15 items unchanged from prior snapshot; all lighting zones covered |
| Basis-consistency checks pass | PASS | All priced lines use PARAMETRIC method consistent with BASIS_OF_ESTIMATE |
| Provenance completeness reported | PASS | 100% of rows have SourceRef; 93% have priced amounts (up from 53%) |
| Scope coverage explicit | PASS | 1 deliverable (DEL-004-04); included/excluded counts documented |
| No writes outside _Estimates/ | PASS | Verified |
| Delta from prior snapshot documented | PASS | Run_Context.md and Summary.md document changes |

---

## Quantity Takeoff Coverage

| Source Document | Items Extracted | Notes |
|---|---|---|
| Datasheet | 6 items (ITEM-005 through ITEM-010) | All lighting zones covered; hardware reference items resolved to $0 |
| Specification | 2 items (ITEM-014, ITEM-015) | P.Eng. stamp requirement; emergency lighting TBD |
| Guidance | 0 direct items | Guidance informed trade-off context but no independently priceable items extracted |
| Procedure | 7 items (ITEM-001 through ITEM-004, ITEM-011 through ITEM-013) | LOE roles + process activities |

| Deliverable | Documents Read | Documents Missing |
|---|---|---|
| DEL-004-04 | 4 of 4 (Datasheet, Specification, Guidance, Procedure) | None |

---

## What to Fix for a Cleaner Rerun

1. **Resolve CONF-LT-003** (emergency/exit lighting applicability under Alberta Building Code) to eliminate the sole residual TBD on DL-015.
2. **Resolve CONF-LT-001** (wash bay fixture specs) -- does not affect design-fee total but improves scope clarity.
3. **Resolve CONF-LT-002** (service pit fixture selection) -- does not affect design-fee total but improves scope clarity.
4. **Obtain actual subconsultant quotes** for Electrical Engineer and BIM Technician hours to upgrade from PARAMETRIC to QUOTE basis with higher confidence.
