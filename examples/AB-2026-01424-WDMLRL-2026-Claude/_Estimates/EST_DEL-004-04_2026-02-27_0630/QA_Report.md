# QA Report — EST_DEL-004-04_2026-02-27_0630

## RUN_STATUS: WARNINGS

**Rationale:** The design professional services LOE is fully priced ($18,810.00 CAD) with complete provenance. However, 7 of 15 line items carry TBD amounts (hardware/material reference items and emergency lighting assessment), and 3 unresolved conflicts (CONF-LT-001, CONF-LT-002, CONF-LT-003) affect scope completeness. Totals are meaningful for the design-fee component but incomplete for the full deliverable cost picture.

---

## S1 — Write Quarantine Respected

| Check | Result |
|---|---|
| All outputs written under `_Estimates/EST_DEL-004-04_2026-02-27_0630/` | PASS |
| No files modified outside `_Estimates/` | PASS |

## S2 — Snapshot Created

| Check | Result |
|---|---|
| Snapshot folder `EST_DEL-004-04_2026-02-27_0630` exists | PASS |

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
| All rows trace to SourceDoc + SourceSection | PASS |
| PricingMode values valid (UNIT_RATE or LUMP_SUM) | PASS |
| Row count | 15 items |

### Detail.csv

| Check | Result |
|---|---|
| Parseable CSV | PASS |
| Required columns present (LineID, ItemID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes) | PASS |
| Method values valid | PASS — all are PARAMETRIC |
| Allowance/parametric convention | PASS — lump-sum items (DL-011 through DL-015) have Qty=1, Unit=LS |
| ItemID traceability to Items.csv | PASS — all 15 ItemIDs match |

## S6 — Provenance Discipline

### Provenance Completeness

| Metric | Value |
|---|---|
| Total Detail.csv rows | 15 |
| Rows with non-TBD SourceRef | 15 (100%) |
| Rows with priced Amount (non-TBD) | 8 of 15 (53%) |
| Rows with TBD Amount | 7 of 15 (47%) |

### Top Missing-Source Offenders

| LineID | Description | Gap |
|---|---|---|
| DL-005 | Main Shop High Bay LED fixtures | No fixture hardware unit cost source |
| DL-006 | Wash Bay High Bay LED fixtures | No fixture hardware unit cost source + fixture specs TBD (CONF-LT-001) |
| DL-007 | Office 8-foot LED strip | No fixture hardware unit cost source |
| DL-008 | Utility Room 8-foot LED strip | No fixture hardware unit cost source |
| DL-009 | Parts/Tool Room 8-foot LED strip | No fixture hardware unit cost source |
| DL-010 | Service Pit/Trench fixtures | Fixture type/count/specs all TBD (CONF-LT-002) + no unit cost source |
| DL-015 | Emergency/exit lighting assessment | Scope applicability TBD (CONF-LT-003) |

**Note:** All TBD items are hardware/material or scope-uncertain items. The 4 design LOE lines (DL-001 through DL-004) accounting for $18,810 are fully provenanced.

## S7 — Status Reporting

| Field | Value |
|---|---|
| RUN_STATUS | **WARNINGS** |
| Rationale | Design professional services total ($18,810) is meaningful and fully provenanced. Material/hardware items are TBD (outside design-fee scope). Three unresolved design conflicts (CONF-LT-001/002/003) affect scope completeness but do not invalidate the design LOE estimate. |

## S8 — Operator Acceptance Checklist

| Criterion | Status | Notes |
|---|---|---|
| RUN_STATUS is OK or WARNINGS with bounded gaps | PASS | WARNINGS — gaps are bounded to hardware items and unresolved conflicts |
| Quantity takeoff (Items.csv) reviewed for completeness | PASS | 15 items extracted from all 4 documents; all lighting zones covered |
| Basis-consistency checks pass | PASS | All priced lines use PARAMETRIC method consistent with BASIS_OF_ESTIMATE |
| Provenance completeness reported | PASS | 100% of rows have SourceRef; 53% have priced amounts |
| Scope coverage explicit | PASS | 1 deliverable (DEL-004-04); included/excluded counts documented |
| No writes outside _Estimates/ | PASS | Verified |

---

## Quantity Takeoff Coverage

| Source Document | Items Extracted | Notes |
|---|---|---|
| Datasheet | 6 items (ITEM-005 through ITEM-010) | All lighting zones covered; hardware reference items |
| Specification | 2 items (ITEM-014, ITEM-015) | P.Eng. stamp requirement; emergency lighting TBD |
| Guidance | 0 direct items | Guidance informed trade-off context but no independently priceable items extracted |
| Procedure | 7 items (ITEM-001 through ITEM-004, ITEM-011 through ITEM-013) | LOE roles + process activities |

| Deliverable | Documents Read | Documents Missing |
|---|---|---|
| DEL-004-04 | 4 of 4 (Datasheet, Specification, Guidance, Procedure) | None |

---

## What to Fix for a Cleaner Rerun

1. **Resolve CONF-LT-001** (wash bay fixture specs) to eliminate TBD on ITEM-006/DL-006.
2. **Resolve CONF-LT-002** (service pit fixture selection) to eliminate TBD on ITEM-010/DL-010.
3. **Resolve CONF-LT-003** (emergency/exit lighting applicability) to eliminate TBD on ITEM-015/DL-015.
4. **Add fixture hardware pricing source** if hardware procurement is to be estimated under this scope (currently outside design-fee scope).
5. **Obtain actual subconsultant quotes** for Electrical Engineer and BIM Technician hours to upgrade from PARAMETRIC to QUOTE basis with higher confidence.
