# QA Report -- EST_DEL-05-03_2026-02-18_1700

## RUN_STATUS: WARNINGS

**Rationale:** Totals are producible and meaningful at parametric level, but material assumptions remain (zone count TBD, no vendor quote, LOW confidence pricing). Estimate is suitable as a proposal-stage placeholder but requires vendor quote replacement before final submission.

---

## S1 -- Write Quarantine Respected

- **Result:** PASS
- **Details:** All files written under `_Estimates/EST_DEL-05-03_2026-02-18_1700/`. No files outside `_Estimates/` were modified.

## S2 -- Snapshot Created

- **Result:** PASS
- **Details:** Snapshot folder `EST_DEL-05-03_2026-02-18_1700` created under `_Estimates/`.

## S3 -- BASIS_OF_ESTIMATE Validated

- **Result:** PASS (with warning)
- **Details:** `QUOTE` is a valid enum value. However, actual pricing method is PARAMETRIC (fallback) because no vendor quote exists. Logged in Decision_Log.md (DEC-RUN-001).

## S4 -- Required Artifacts Exist

- **Result:** PASS
- **Artifacts produced:**
  - [x] Run_Context.md
  - [x] Summary.md
  - [x] QA_Report.md
  - [x] Source_Index.md
  - [x] Decision_Log.md
  - [x] Assumptions_Log.md
  - [x] WBS_CBS_Matrix.csv
  - [x] Detail.csv
  - [x] Blockers.md
  - [x] Risk_Register.md

## S5 -- Detail Schema Integrity

- **Result:** PASS
- **Columns present:** LineID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes (all 14 required columns)
- **Method values:** PARAMETRIC (valid enum)
- **Allowance/parametric convention:** Qty=1, Unit=LS, UnitRate=Amount -- PASS

## S6 -- Provenance Discipline

- **Result:** PASS
- **Provenance completeness:** 1/1 priced rows (100%) have non-TBD SourceRef
- **SourceRef detail:**
  - L-05-03-001: `Optional_Items_Pricing.csv > OPT-06` -- VALID
- **Missing-source offenders:** None

## S7 -- Status Reporting

- **Result:** PASS
- **RUN_STATUS:** WARNINGS
- **Justification:** Totals exist ($45,000 CAD) but:
  - No vendor quote (PARAMETRIC fallback)
  - Zone count is assumed (TBD pending DEL-02-01)
  - LOW confidence across all pricing inputs

---

## Basis-Consistency Check

| Check | Result | Notes |
|---|---|---|
| Declared basis vs actual methods | WARNING | Declared QUOTE; actual PARAMETRIC. Permitted by FALLBACK_POLICY + ALLOW_MIXED_METHODS. |
| Mixed methods present | N/A | Only one method used (PARAMETRIC). |
| Fallback usage logged | PASS | DEC-RUN-001 in Decision_Log.md. |

## Coverage Check

| Metric | Value |
|---|---|
| Deliverables in scope | 1 |
| Deliverables with at least 1 line item | 1 |
| Deliverables missing / blocked | 0 |
| Total line items | 1 |
| Lines with Amount=TBD | 0 |

## Dependency / Blocker Summary

| Metric | Value |
|---|---|
| Total dependencies loaded | 9 (2 ANCHOR + 7 EXECUTION) |
| Upstream blockers affecting estimate | 2 |
| Non-blocking dependencies | 5 |

Upstream blockers:
1. DEP-05-03-003: DEL-02-01 floor plan required for zone count confirmation
2. DEP-05-03-004: DEL-02-06 interface coordination (does not block pricing but blocks detailed scope)

---

## What to Fix for a Cleaner Rerun

1. **Obtain vendor quote** for access control system to replace parametric pricing (OPT-06). This would change Method from PARAMETRIC to QUOTE and likely improve confidence from LOW to MED/HIGH.
2. **Confirm zone count** once DEL-02-01 floor plan is available. If zones exceed 10, add line items using OPT-07 ($3,200/zone). If fewer, consider whether 10-zone base price still applies.
3. **Confirm scope boundary** with DEL-02-06 estimator to ensure no double-counting of conduit, low-voltage power, or network costs at the access control / electrical interface.
4. **Consider breaking into multiple line items** once vendor quote provides component-level detail (equipment, software, wiring, installation, commissioning as separate lines).

---

## Operator Acceptance Checklist (S8)

| Criterion | Status |
|---|---|
| RUN_STATUS is OK or WARNINGS with bounded gaps | PASS (WARNINGS; gaps are clearly identified and bounded) |
| Basis-consistency checks pass or deviations approved | PASS (fallback approved by FALLBACK_POLICY + ALLOW_MIXED_METHODS) |
| Provenance completeness reported | PASS (100% -- 1/1 rows) |
| Scope coverage explicit | PASS (1 in scope; 0 excluded; 0 blocked) |
| No writes outside _Estimates/ | PASS |

**Recommendation:** Snapshot is acceptable for publication as a proposal-stage parametric placeholder. Replace with vendor quote before final pricing submission.
