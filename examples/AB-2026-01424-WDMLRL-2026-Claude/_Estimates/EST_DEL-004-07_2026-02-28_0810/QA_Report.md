# QA Report

**RunID:** EST_DEL-004-07_2026-02-28_0810
**Date:** 2026-02-28
**RUN_STATUS: WARNINGS**

---

## S1 — Write Quarantine Respected

**PASS.** All output files written exclusively under `_Estimates/EST_DEL-004-07_2026-02-28_0810/`. No files outside the estimating tool root were modified.

---

## S2 — Snapshot Created

**PASS.** Snapshot folder `EST_DEL-004-07_2026-02-28_0810` created under `_Estimates/`.

---

## S3 — BASIS_OF_ESTIMATE Validated

**PASS.** `BASIS_OF_ESTIMATE = PARAMETRIC` — valid enum value.

---

## S4 — Required Artifacts Exist

**PASS.** All required artifacts produced:

| Artifact | Status |
|---|---|
| Run_Context.md | Created |
| Items.csv | Copied from prior snapshot (unchanged) |
| Detail.csv | Created (updated — 2 TBDs resolved) |
| Summary.md | Created |
| QA_Report.md | Created (this file) |
| Source_Index.md | Created |
| Decision_Log.md | Created |
| Assumptions_Log.md | Created |
| WBS_CBS_Matrix.csv | Created |

---

## S5 — CSV Schema Integrity

### Items.csv

**PASS.** Schema validation:

| Column | Present | Valid |
|---|---|---|
| ItemID | Yes | Unique IDs ITM-001 through ITM-010 |
| DeliverableID | Yes | All = DEL-004-07 |
| Description | Yes | Non-empty for all rows |
| Qty | Yes | Numeric or TBD (3 rows TBD) |
| Unit | Yes | Valid units (hr, EA, LS) |
| PricingMode | Yes | UNIT_RATE (4 rows) or LUMP_SUM (6 rows) |
| SourceDoc | Yes | Datasheet, Specification, Procedure |
| SourceSection | Yes | Non-empty for all rows |
| Notes | Yes | Non-empty for all rows |

Row count: 10 items. All rows trace to a source document and section. Items.csv is unchanged from prior snapshot.

### Detail.csv

**PASS.** Schema validation:

| Column | Present | Valid |
|---|---|---|
| LineID | Yes | Unique IDs LN-001 through LN-007 |
| ItemID | Yes | All reference valid Items.csv ItemIDs |
| CBS | Yes | Management or Design |
| WBS_PackageID | Yes | All = PKG-004 |
| WBS_DeliverableID | Yes | All = DEL-004-07 |
| Description | Yes | Non-empty |
| Qty | Yes | Numeric (6 rows) or TBD (1 row) |
| Unit | Yes | hr, LS, or EA |
| UnitRate | Yes | Numeric (6 rows) or TBD (1 row) |
| Amount | Yes | Numeric (6 rows) or TBD (1 row) |
| Currency | Yes | All = CAD |
| Method | Yes | All = PARAMETRIC |
| SourceRef | Yes | Non-empty for all rows |
| Confidence | Yes | MED (6 rows) or LOW (1 row) |
| Notes | Yes | Non-empty |

Method values: All PARAMETRIC — consistent with BASIS_OF_ESTIMATE. No mixed methods exercised.

Note: Items ITM-008, ITM-009, ITM-010 (coordination review, P.Eng. stamp, construction support) are not separately priced in Detail.csv because their effort is included within the LOE hours of LN-001 and LN-004. This is documented in Items.csv Notes column. No separate Detail.csv lines were created to avoid double-counting.

---

## S6 — Provenance Discipline

**PASS (with 1 residual gap).**

| Metric | Value |
|---|---|
| Total Detail.csv rows | 7 |
| Rows with non-TBD SourceRef | 7 (100%) |
| Rows with fully substantiated pricing | 6 (86%) |
| Rows with TBD amounts | 1 (14%) |

### Residual TBD Item

| LineID | Issue | Remediation |
|---|---|---|
| LN-007 | Additional low-voltage systems (fire alarm, data, access control, intercom) scope TBD | Confirm or exclude per Specification REQ-007-08 and REQ-007-09 at preliminary design; pending County confirmation |

### Resolved Since Prior Snapshot

| LineID | Resolution | Decision |
|---|---|---|
| LN-005 | Set to $0 (1 LS) | Design effort in LN-004 engineering hours; camera hardware cost in PKG-015 (DEC-R01) |
| LN-006 | Set to $0 (1 LS) | Design effort in LN-004 engineering hours; antenna hardware cost in PKG-015 (DEC-R02) |

All TBD items have SourceRef pointing to the specific Specification sections that document the gap. No `location TBD` entries without traceable document references.

---

## S7 — Status Reporting

### RUN_STATUS: WARNINGS

**Rationale:** The estimate produces a meaningful total ($18,810.00 CAD) for the confirmed professional design services scope using parametric LOE + rate table pricing. Two previously TBD items (LN-005, LN-006) have been resolved to $0 as hardware reference items with design effort included in LN-004. One material TBD item remains:

1. Additional low-voltage systems (fire alarm, data, access control, intercom) — TBD pending County confirmation

This TBD is inherent to the project's design-build nature (RFP S3.4: "The County only has a concept in mind") and will be resolved at preliminary design. The current LOE allocation (130 hours) includes effort for the two confirmed systems but may be insufficient if additional systems are confirmed.

The estimate does NOT represent a `FAILED_INPUTS` condition because:
- All four price sources are present and usable
- The LOE model provides hours for DEL-004-07 specifically
- The rate table provides rates for all assigned roles
- The single residual TBD is a scope-driven gap (not a pricing-source gap)
- 86% of lines are now priced (improved from 57% in prior snapshot)

---

## S8 — Operator Acceptance Checklist

| Check | Status | Notes |
|---|---|---|
| RUN_STATUS is OK or WARNINGS with bounded gaps | PASS | WARNINGS — 1 residual scope-driven TBD, clearly bounded and traceable |
| Items.csv reviewed for completeness | PASS | 10 items unchanged from prior snapshot |
| Detail.csv TBD resolution | PASS | 2 of 3 TBDs resolved; 1 cannot be resolved without County input |
| Basis-consistency checks pass | PASS | All priced lines use PARAMETRIC method, matching BASIS_OF_ESTIMATE |
| Provenance completeness reported | PASS | 100% of lines have SourceRef; 86% have priced amounts |
| Scope coverage explicit | PASS | 1 deliverable in scope; all 4 documents read; included/excluded clearly stated |
| Arithmetic verification | PASS | LN-001: 6x165=990; LN-002: 4x135=540; LN-003: 36x95=3420; LN-004: 84x165=13860; LN-005: 0; LN-006: 0; Total priced: 18810 |
| No writes outside _Estimates/ | PASS | Write quarantine respected |

---

## What to Fix for a Cleaner Rerun

1. **Resolve additional low-voltage systems scope (LN-007)** — Confirm or exclude fire alarm, data/network, access control, and intercom per REQ-007-08/09. If confirmed, LOE hours will need adjustment and LN-007 can be priced.
2. **Resolve Old North Shop scope boundary** — Confirm whether Old North Shop renovation areas include low-voltage scope (CON-007-02). If in scope, LOE hours will need adjustment.
3. **Validate LOE hours** — The 130-hour parametric allocation is a standard drawing-set model. Once scope is fully confirmed, compare against actual project complexity and adjust if needed.
