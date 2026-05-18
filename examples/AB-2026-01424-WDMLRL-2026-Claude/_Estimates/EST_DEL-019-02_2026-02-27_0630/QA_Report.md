# QA Report — EST_DEL-019-02_2026-02-27_0630

## RUN_STATUS: WARNINGS

**Rationale:** Totals are meaningful and fully priced from parametric sources, but material concerns exist regarding LOE adequacy for a recurring weekly deliverable and missing non-labour cost coverage.

---

## S1 — Write Quarantine Respected

**PASS.** All output files written exclusively under `_Estimates/EST_DEL-019-02_2026-02-27_0630/`. No files outside `_Estimates/` were modified.

## S2 — Snapshot Created

**PASS.** Snapshot folder `EST_DEL-019-02_2026-02-27_0630` created under `_Estimates/`.

## S3 — BASIS_OF_ESTIMATE Validated

**PASS.** `BASIS_OF_ESTIMATE = PARAMETRIC` — valid enum value.

## S4 — Required Artifacts Exist

**PASS.** All required artifacts present:

| Artifact | Status |
|---|---|
| Run_Context.md | Present |
| Items.csv | Present |
| Summary.md | Present |
| QA_Report.md | Present (this file) |
| Source_Index.md | Present |
| Detail.csv | Present (optional; produced) |
| WBS_CBS_Matrix.csv | Present |
| Decision_Log.md | Present |
| Assumptions_Log.md | Present |

## S5 — CSV Schema Integrity

### Items.csv

**PASS.**

| Check | Result |
|---|---|
| Parseable CSV | Yes |
| Required columns present (ItemID, DeliverableID, Description, Qty, Unit, PricingMode, SourceDoc, SourceSection, Notes) | Yes |
| All rows trace to source document and section | Yes — every row cites SourceDoc (Procedure, Specification, or Datasheet) and SourceSection |
| PricingMode values valid | Yes — UNIT_RATE (6 rows), LUMP_SUM (2 rows) |
| Row count | 8 |

### Detail.csv

**PASS.**

| Check | Result |
|---|---|
| Parseable CSV | Yes |
| Required columns present (LineID, ItemID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes) | Yes |
| Method values valid | Yes — all PARAMETRIC (8 rows) |
| Allowance/parametric convention (Qty=1, Unit=LS, UnitRate=Amount for LS items) | Yes — L-019-02-007 and L-019-02-008 use Qty=1, Unit=LS, UnitRate=Amount=0.00 |
| All ItemIDs trace to Items.csv | Yes |
| Row count | 8 |

## S6 — Provenance Discipline

**PASS.**

| Metric | Value |
|---|---|
| Total priced rows (Amount > 0) | 6 |
| Rows with non-TBD SourceRef | 8 / 8 (100%) |
| Provenance completeness | 100% |
| Top missing-source offenders | None |

All SourceRef values cite specific pricing source files and row/section identifiers.

## S7 — Status Reporting

**RUN_STATUS: WARNINGS**

Warnings:

1. **W-001: LOE adequacy concern.** 38 total hours across 6 roles for a weekly recurring deliverable spanning ~39 weeks (April through December 2026). This averages less than 1 hour per role per week. For weekly meetings of 60-90 minutes duration (Datasheet attribute), the total LOE may understate true effort by a significant factor. The estimate uses the values as stated.

2. **W-002: Non-labour costs missing.** No pricing source provides non-labour costs for meeting operations (travel, facilities, technology, printing). For in-person meetings at a rural site (~30km south of Camrose), travel costs could be material.

3. **W-003: LOE source notes are placeholders.** Level_of_Effort.csv notes for all DEL-019-02 rows show "PKG-019 TBD -- TBD", indicating the parametric model has not been fully refined for this package.

4. **W-004: Phase A/D not separately broken out.** The LOE does not distinguish between one-time setup (Phase A), recurring operations (Phase B/C), and closeout (Phase D) effort. Informational line items (L-019-02-007, L-019-02-008) carry $0 amounts.

## S8 — Operator Acceptance Checklist

| Criterion | Status | Notes |
|---|---|---|
| RUN_STATUS is OK or WARNINGS with bounded gaps | WARNINGS — gaps are bounded and described | W-001 through W-004 identified |
| Items.csv reviewed for completeness | 8 items extracted from 4 documents | Covers all procedural phases (A through D) and all 6 LOE roles |
| Basis-consistency checks pass | PASS — all 8 lines use PARAMETRIC | Consistent with BASIS_OF_ESTIMATE |
| Provenance completeness reported | 100% (8/8 SourceRef populated) | No missing-source offenders |
| Scope coverage explicit | 1 deliverable in scope; 1 deliverable estimated | DEL-019-02 fully covered; 4 documents read; no missing documents |
| No writes outside _Estimates/ | PASS | Write quarantine respected |

---

## What to Fix for a Cleaner Rerun

1. **Refine LOE hours for DEL-019-02.** The current LOE appears to understate effort for a weekly recurring deliverable. Consider whether the hours represent per-occurrence or total project values and update Level_of_Effort.csv accordingly.
2. **Break out LOE by project phase.** Separate Phase A (setup), Phase B/C (recurring), and Phase D (closeout) hours to improve traceability and allow scaling by project duration.
3. **Add non-labour cost source.** Provide a pricing source for meeting-related non-labour costs (travel, facilities, technology) or explicitly confirm these are excluded/covered elsewhere.
4. **Resolve "PKG-019 TBD -- TBD" notes.** Update the LOE source notes to reflect the actual package/deliverable grouping rationale.
