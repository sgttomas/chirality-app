# QA Report -- EST_DEL-06-02_2026-02-18_1800

## RUN_STATUS: OK

All inputs resolved; all line items priced with full provenance; no critical gaps.

---

## S1 -- Write Quarantine

| Check | Result |
|---|---|
| All writes under `_Estimates/`? | PASS |
| Any project truth files modified? | NO -- PASS |

## S2 -- Snapshot Created

| Check | Result |
|---|---|
| Snapshot folder exists? | PASS (`EST_DEL-06-02_2026-02-18_1800/`) |

## S3 -- BASIS_OF_ESTIMATE Validated

| Check | Result |
|---|---|
| Value provided? | YES: `RATE_TABLE` |
| Valid enum? | PASS (one of: QUOTE, RATE_TABLE, HISTORICAL, PARAMETRIC, ALLOWANCE) |

## S4 -- Required Artifacts Exist

| Artifact | Status |
|---|---|
| `Run_Context.md` | PRESENT |
| `Summary.md` | PRESENT |
| `QA_Report.md` | PRESENT (this file) |
| `Source_Index.md` | PRESENT |
| `Decision_Log.md` | PRESENT |
| `Assumptions_Log.md` | PRESENT |
| `WBS_CBS_Matrix.csv` | PRESENT |
| `Detail.csv` | PRESENT (optional; included) |
| `Blockers.md` | PRESENT (optional; included) |

## S5 -- Detail Schema Integrity

| Check | Result |
|---|---|
| `Detail.csv` parseable? | PASS |
| All required columns present? | PASS (LineID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes) |
| `Method` values valid? | PASS (all = RATE_TABLE) |
| Allowance/parametric convention? | N/A (no ALLOWANCE or PARAMETRIC method rows) |
| Row count | 2 |

### Arithmetic Verification

| LineID | Qty | UnitRate | Expected | Actual | Match |
|---|---:|---:|---:|---:|---|
| L-0602-01 | 10 | 165 | 1650 | 1650 | PASS |
| L-0602-02 | 4 | 175 | 700 | 700 | PASS |
| **Total** | | | **2350** | **2350** | **PASS** |

## S6 -- Provenance Discipline

| Metric | Value |
|---|---|
| Rows with non-TBD SourceRef | 2/2 (100%) |
| Rows with `location TBD` | 0 |
| Top missing-source offenders | None |

## S7 -- Status Reporting

| Field | Value |
|---|---|
| **RUN_STATUS** | **OK** |
| Rationale | All line items priced from basis evidence; no TBDs; no critical input gaps; provenance 100% |

## S8 -- Operator Acceptance Checklist

| Check | Result |
|---|---|
| RUN_STATUS is OK or bounded WARNINGS? | PASS (OK) |
| Basis-consistency checks pass? | PASS (all methods = RATE_TABLE = BASIS_OF_ESTIMATE) |
| Provenance completeness reported? | PASS (100%) |
| Scope coverage explicit? | PASS (1 included, 0 excluded, 0 blocked) |
| No writes outside `_Estimates/`? | PASS |
| **Snapshot publishable?** | **YES** |

## Basis-Consistency Detail

| Method in Detail.csv | Count | Matches BASIS_OF_ESTIMATE? |
|---|---:|---|
| RATE_TABLE | 2 | YES |
| Other | 0 | N/A |

## Coverage

| Metric | Value |
|---|---|
| Deliverables in scope | 1 (DEL-06-02) |
| Deliverables covered (priced) | 1 |
| Deliverables missing/blocked | 0 |

## What to Fix for a Cleaner Rerun

Nothing. This run produced a complete, consistent estimate with full provenance.
