# QA Report

**RunID:** EST_DEL-004-07_2026-02-27_0141
**Date:** 2026-02-27
**RUN_STATUS: WARNINGS**

---

## S1 — Write Quarantine Respected

**PASS.** All output files written exclusively under `_Estimates/EST_DEL-004-07_2026-02-27_0141/`. No files outside the estimating tool root were modified.

---

## S2 — Snapshot Created

**PASS.** Snapshot folder `EST_DEL-004-07_2026-02-27_0141` created under `_Estimates/`.

---

## S3 — BASIS_OF_ESTIMATE Validated

**PASS.** `BASIS_OF_ESTIMATE = PARAMETRIC` — valid enum value.

---

## S4 — Required Artifacts Exist

**PASS.** All required artifacts produced:

| Artifact | Status |
|---|---|
| Run_Context.md | Created |
| Items.csv | Created |
| Detail.csv | Created |
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

Row count: 10 items. All rows trace to a source document and section.

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
| Qty | Yes | Numeric (4 rows) or TBD (3 rows) |
| Unit | Yes | hr or EA |
| UnitRate | Yes | Numeric (4 rows) or TBD (3 rows) |
| Amount | Yes | Numeric (4 rows) or TBD (3 rows) |
| Currency | Yes | All = CAD |
| Method | Yes | All = PARAMETRIC |
| SourceRef | Yes | Non-empty for all rows |
| Confidence | Yes | MED (4 rows) or LOW (3 rows) |
| Notes | Yes | Non-empty |

Method values: All PARAMETRIC — consistent with BASIS_OF_ESTIMATE. No mixed methods exercised.

Note: Items ITM-008, ITM-009, ITM-010 (coordination review, P.Eng. stamp, construction support) are not separately priced in Detail.csv because their effort is included within the LOE hours of LN-001 and LN-004. This is documented in Items.csv Notes column. No separate Detail.csv lines were created to avoid double-counting.

---

## S6 — Provenance Discipline

**PASS (with gaps).**

| Metric | Value |
|---|---|
| Total Detail.csv rows | 7 |
| Rows with non-TBD SourceRef | 7 (100%) |
| Rows with fully substantiated pricing | 4 (57%) |
| Rows with TBD amounts | 3 (43%) |

### Top Missing-Source Offenders

| LineID | Issue | Remediation |
|---|---|---|
| LN-005 | Camera count, technology, and cable type TBD in Datasheet | Confirm with County at preliminary design (Procedure Step 1) |
| LN-006 | Antenna point count and radio system type TBD in Datasheet | Confirm with County at preliminary design (Procedure Step 1) |
| LN-007 | Additional low-voltage systems (fire alarm, data, access control, intercom) scope TBD | Resolve per Specification REQ-007-08 and REQ-007-09 at preliminary design |

All TBD items have SourceRef pointing to the specific Datasheet or Specification sections that document the gap. No `location TBD` entries without traceable document references.

---

## S7 — Status Reporting

### RUN_STATUS: WARNINGS

**Rationale:** The estimate produces a meaningful total ($18,810.00 CAD) for the confirmed professional design services scope using parametric LOE + rate table pricing. However, three material TBD items remain:

1. Security camera system scope (count, technology) — TBD
2. Radio antenna system scope (count, type) — TBD
3. Additional low-voltage systems (fire alarm, data, access control, intercom) — TBD

These TBDs are inherent to the project's design-build nature (RFP §3.4: "The County only has a concept in mind") and will be resolved at preliminary design. The current LOE allocation (130 hours) includes effort for the two confirmed systems but may be insufficient if additional systems are confirmed.

The estimate does NOT represent a `FAILED_INPUTS` condition because:
- All four price sources are present and usable
- The LOE model provides hours for DEL-004-07 specifically
- The rate table provides rates for all assigned roles
- The TBD items are scope-driven gaps (not pricing-source gaps)

---

## S8 — Operator Acceptance Checklist

| Check | Status | Notes |
|---|---|---|
| RUN_STATUS is OK or WARNINGS with bounded gaps | PASS | WARNINGS — gaps are scope-driven TBDs, clearly bounded and traceable |
| Items.csv reviewed for completeness | PASS | 10 items extracted covering all work activities from all four documents |
| Basis-consistency checks pass | PASS | All priced lines use PARAMETRIC method, matching BASIS_OF_ESTIMATE |
| Provenance completeness reported | PASS | 100% of lines have SourceRef; 57% have priced amounts |
| Scope coverage explicit | PASS | 1 deliverable in scope; all 4 documents read; included/excluded clearly stated |
| No writes outside _Estimates/ | PASS | Write quarantine respected |

---

## What to Fix for a Cleaner Rerun

1. **Resolve camera scope** — Confirm camera count, technology (IP vs. analog), and coverage zones with County. Update Datasheet attributes and rerun.
2. **Resolve radio antenna scope** — Confirm radio system type (VHF/UHF), antenna point count, and in-building coverage approach. Update Datasheet attributes and rerun.
3. **Resolve additional low-voltage systems** — Confirm or exclude fire alarm, data/network, access control, and intercom per REQ-007-08/09. If confirmed, LOE hours will need adjustment.
4. **Resolve Old North Shop scope boundary** — Confirm whether Old North Shop renovation areas include low-voltage scope (CON-007-02). If in scope, LOE hours will need adjustment.
5. **Validate LOE hours** — The 130-hour parametric allocation is a standard drawing-set model. Once scope is confirmed, compare against actual project complexity and adjust if needed.
