# QA Report — EST_DEL-03-03_2026-02-18_1200

## RUN_STATUS: WARNINGS

This estimate produces meaningful totals but has material assumptions regarding quantities (pre-design parametric areas) and geosynthetic overlap. The estimate is suitable for budgetary/planning purposes but should be updated when site plan areas are available.

---

## S1 — Write Quarantine Respected

| Check | Result |
|-------|--------|
| All files written under _Estimates/ only | PASS |
| No deliverable files modified | PASS |
| No lifecycle files modified | PASS |
| No decomposition outputs modified | PASS |
| No dependency registers modified | PASS |

## S2 — Snapshot Created

| Check | Result |
|-------|--------|
| Snapshot folder exists | PASS |
| Folder name | EST_DEL-03-03_2026-02-18_1200 |

## S3 — BASIS_OF_ESTIMATE Validated

| Check | Result |
|-------|--------|
| BASIS_OF_ESTIMATE provided | PASS |
| Value = RATE_TABLE | PASS (valid enum) |

## S4 — Required Artifacts Exist

| Artifact | Status |
|----------|--------|
| Run_Context.md | PRESENT |
| Summary.md | PRESENT |
| QA_Report.md | PRESENT (this file) |
| Source_Index.md | PRESENT |
| Decision_Log.md | PRESENT |
| Assumptions_Log.md | PRESENT |
| WBS_CBS_Matrix.csv | PRESENT |
| Detail.csv | PRESENT |
| Blockers.md | PRESENT |

## S5 — Detail Schema Integrity

| Check | Result |
|-------|--------|
| Detail.csv parseable | PASS |
| All 14 required columns present | PASS |
| Column list: LineID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes | PASS |
| Method values valid (all = RATE_TABLE) | PASS |
| No ALLOWANCE or PARAMETRIC convention violations | N/A (no ALLOWANCE or PARAMETRIC method lines) |
| All amounts = Qty x UnitRate (verified) | PASS |
| ROUNDING=DOLLAR applied | PASS |

### Amount Verification (spot checks)

| LineID | Qty | UnitRate | Expected | Actual | Match |
|--------|----:|--------:|--------:|-------:|-------|
| L-001 | 2000 | 92 | 184000 | 184000 | PASS |
| L-002 | 3200 | 60 | 192000 | 192000 | PASS |
| L-003 | 6000 | 30 | 180000 | 180000 | PASS |
| L-005 | 312 | 132 | 41184 | 41184 | PASS |
| L-006 | 78 | 132 | 10296 | 10296 | PASS |

### WBS_CBS_Matrix Totals Verification

| CBS | Sum of Detail Lines | Matrix Amount_Total | Match |
|-----|-------------------:|-------------------:|-------|
| 03.03.ASP-HD | 184000 + 16000 = 200000 | 200000 | PASS |
| 03.03.ASP-LD | 192000 + 16000 = 208000 | 208000 | PASS |
| 03.03.AGG | 180000 + 180000 + 30000 = 390000 | 390000 | PASS |
| 03.03.CONC | 41184 + 10296 + 20500 + 11250 = 83230 | 83230 | PASS |
| 03.03.MARK | 1800 + 1350 = 3150 | 3150 | PASS |
| 03.03.SITE | 12000 | 12000 | PASS |
| **TOTAL** | **896380** | **896380** | **PASS** |

## S6 — Provenance Discipline

| Metric | Value |
|--------|-------|
| Total priced rows | 14 |
| Rows with non-TBD SourceRef | 14 |
| Provenance completeness | **100%** |
| Rows citing rate table + quantity source | 14 |
| Rows with "location TBD" | 0 |

All 14 line items have SourceRef pointing to specific rate table item IDs (PS-01 through PS-09) and quantity assumptions (PP-10, PP-13, PP-14, PP-19, or ASM-### references).

## S7 — Basis Consistency

| Check | Result |
|-------|--------|
| BASIS_OF_ESTIMATE | RATE_TABLE |
| Method values in Detail.csv | All = RATE_TABLE |
| ALLOW_MIXED_METHODS | FALSE |
| Mixed methods detected | NONE |
| Basis consistency | PASS |

Note: The rate table itself contains rates with Basis=PARAMETRIC (meaning the rates were developed parametrically, not from firm quotes). The estimate Method=RATE_TABLE is correct because pricing is derived from the rate table as the basis document. The underlying confidence of the rates is reflected in the MEDIUM confidence assignments.

## S8 — Coverage

| Metric | Count |
|--------|------:|
| Deliverables in SCOPE | 1 |
| Deliverables with estimate lines | 1 |
| Deliverables blocked | 0 |
| Deliverables excluded | 0 |
| Coverage | **100%** |

## Dependency/Blocker Summary

| Metric | Count |
|--------|------:|
| Dependencies loaded | 9 (from Dependencies.csv) |
| Hard blockers | 0 |
| Information gaps (MEDIUM impact) | 3 |
| Information gaps (LOW impact) | 1 |

Information gaps are documented in Blockers.md and mitigated by assumptions (ASM-001 through ASM-016).

## Warnings Detail

| # | Warning ID | Severity | Description | Recommended Action |
|---|-----------|----------|-------------|-------------------|
| 1 | QUANTITIES_ASSUMED | HIGH | All area quantities are parametric (pre-design). No site plan areas measured. | Update quantities when DEL-03-01 site plan is issued. Re-run estimate. |
| 2 | CONCRETE_APRON_DIMENSIONS_TBD | MEDIUM | Apron dimensions assumed at 4.88m x 8.0m per door. Actual depends on PKG-002/PKG-004 architectural. | Update apron quantities when door locations are confirmed. |
| 3 | AGGREGATE_DEPTH_TBD | MEDIUM | 300mm depth is an assumption per Specification REQ-03-03-05. Pavement design report may change this. | Confirm aggregate depth in pavement design report. Adjust L-003/L-004 if depth changes. |
| 4 | GEOSYNTHETICS_CONSERVATIVE | LOW | $62,000 in geosynthetic allowance lines may overlap with rate table "includes base prep" notes. | Confirm with rate table author whether PS-01/PS-02 rates include geosynthetics. Remove L-012/L-013 if confirmed. |
| 5 | RATES_PARAMETRIC_NOT_QUOTED | MEDIUM | All rates from Paving_Surfacing_Rates.csv are parametric (MEDIUM confidence), not firm contractor quotes. | Obtain contractor quotes during procurement phase. |

## What to Fix for a Cleaner Rerun

1. **Provide measured site plan areas** from DEL-03-01 (fire route m2, parking m2, yard m2) to replace parametric quantity assumptions.
2. **Confirm concrete apron dimensions** from PKG-002 and PKG-004 architectural drawings (door locations + swept path analysis).
3. **Confirm aggregate yard depth** from pavement design report (REQ-03-03-05).
4. **Clarify geosynthetic inclusion** in PS-01 and PS-02 rate table entries — are geogrid/geofabric supply+install included in the $92/m2 and $60/m2 rates?
5. **Obtain contractor quotes** to replace parametric rates with firm pricing (would change BASIS_OF_ESTIMATE to QUOTE).

## Operator Acceptance Checklist

| Criterion | Status |
|-----------|--------|
| RUN_STATUS is OK or WARNINGS with bounded gaps | PASS (WARNINGS — 5 warnings, all bounded and actionable) |
| Basis-consistency checks pass | PASS (all RATE_TABLE, no mixed methods) |
| Provenance completeness reported | PASS (100%) |
| Scope coverage explicit | PASS (1/1 deliverable covered; exclusions documented) |
| No writes outside _Estimates/ | PASS |
| **Snapshot publishable** | **YES — suitable for budgetary/planning use** |
