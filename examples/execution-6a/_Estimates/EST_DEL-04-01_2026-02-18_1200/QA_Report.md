# QA Report — EST_DEL-04-01_2026-02-18_1200

## RUN_STATUS: OK

---

## S1 -- Write Quarantine

| Check | Result |
|---|---|
| All files written under _Estimates/ only | PASS |
| No deliverable content files modified | PASS |
| No lifecycle files modified | PASS |
| No decomposition outputs modified | PASS |
| No dependency registers modified | PASS |

## S2 -- Snapshot Created

| Check | Result |
|---|---|
| Snapshot folder exists | PASS (EST_DEL-04-01_2026-02-18_1200/) |

## S3 -- BASIS_OF_ESTIMATE Validated

| Check | Result |
|---|---|
| BASIS_OF_ESTIMATE provided | PASS (PARAMETRIC) |
| Value is valid enum | PASS (PARAMETRIC is one of: QUOTE, RATE_TABLE, HISTORICAL, PARAMETRIC, ALLOWANCE) |

## S4 -- Required Artifacts Exist

| Artifact | Status |
|---|---|
| Run_Context.md | PRESENT |
| Summary.md | PRESENT |
| QA_Report.md | PRESENT (this file) |
| Source_Index.md | PRESENT |
| Decision_Log.md | PRESENT |
| Assumptions_Log.md | PRESENT |
| WBS_CBS_Matrix.csv | PRESENT |
| Detail.csv | PRESENT (optional but recommended; produced) |

## S5 -- Detail Schema Integrity

| Check | Result |
|---|---|
| Detail.csv parseable | PASS (2 data rows + header) |
| Required columns present | PASS (LineID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes) |
| Method values valid | PASS (PARAMETRIC, ALLOWANCE -- both are valid enum values) |
| Parametric convention (Qty=1, Unit=LS, UnitRate=Amount) | PASS (L-0401-01: Qty=1, Unit=LS, UnitRate=192000, Amount=192000) |
| Allowance convention (Qty=1, Unit=LS, UnitRate=Amount) | PASS (L-0401-02: Qty=1, Unit=LS, UnitRate=10000, Amount=10000) |

## S6 -- Provenance Discipline

| Metric | Value |
|---|---|
| Total priced rows | 2 |
| Rows with substantive SourceRef | 1 (L-0401-01: Parametric_Building_Rates.csv PB-01) |
| Rows with fallback SourceRef (Assumptions_Log reference) | 1 (L-0401-02: ASM-003) |
| Rows with "location TBD" | 0 |
| Provenance completeness | 50% (1 of 2 rows has direct source; 1 uses assumption reference) |

### Top Missing-Source Offenders

| LineID | Amount | SourceRef | Issue |
|---|---|---|---|
| L-0401-02 | $10,000 | Assumptions_Log.md ASM-003 | No explicit design fee rate in PRICE_SOURCES; priced as allowance per FALLBACK_POLICY |

## S7 -- Status Reporting

| Field | Value |
|---|---|
| RUN_STATUS | OK |
| Justification | Primary shell cost ($192,000, 95% of total) is supported by PB-01 parametric evidence with MEDIUM confidence. Design allowance ($10,000, 5% of total) is a bounded gap with LOW confidence but small dollar impact. Total of $202,000 is meaningful and within expected range. |

## Basis-Consistency Checks

| Check | Result |
|---|---|
| Primary method matches BASIS_OF_ESTIMATE (PARAMETRIC) | PASS (L-0401-01 is PARAMETRIC) |
| Mixed methods present | YES (L-0401-02 is ALLOWANCE) |
| ALLOW_MIXED_METHODS = TRUE | PASS (mixed methods are explicitly permitted) |
| Fallback uses logged | PASS (DEC-RUN-004 in Decision_Log.md) |

## Coverage

| Metric | Value |
|---|---|
| Deliverables in scope | 1 (DEL-04-01) |
| Deliverables covered (at least one priced line) | 1 |
| Deliverables missing | 0 |
| Deliverables blocked | 0 |

## Blocker Summary

| Metric | Value |
|---|---|
| Dependencies parsed | 14 |
| Hard estimating blockers | 0 |
| Design-phase prerequisites (informational) | 4 (DEP-04-01-E001 through E004; these are upstream information needs for design, not for parametric pricing) |

## Cross-Checks Performed

| Check | Result | Status |
|---|---|---|
| PB-01 range check ($168,000 - $210,000) | $192,000 is within range | PASS |
| PB-02 turnkey comparison | Shell ($192,000) = 67% of turnkey ($288,000) | REASONABLE |
| PP-22 rough parametric | DEL-04-01 + design ($202,000) = 70% of PP-22 ($290,000) | REASONABLE |

## What to Fix for a Cleaner Rerun

1. **Design fee source:** Add an explicit design/engineering fee rate table to PRICE_SOURCES to eliminate the ALLOWANCE fallback on L-0401-02.
2. **Rate currency year:** Confirm whether PB-01 rates are 2024 or 2025 base year and whether escalation is needed for 2026 construction.
3. **No other issues identified.** The estimate is clean and well-supported for a single-deliverable parametric run.

## S8 -- Operator Acceptance Checklist

| Criterion | Status |
|---|---|
| RUN_STATUS is OK or WARNINGS with bounded gaps | PASS (OK) |
| Basis-consistency checks pass | PASS |
| Provenance completeness reported | PASS (50%; gap is bounded and small-dollar) |
| Scope coverage explicit | PASS (1/1 deliverable covered) |
| No writes outside _Estimates/ | PASS |
| **Snapshot is good enough to publish** | **YES** |
