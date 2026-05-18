# QA Report — EST_DEL-01-05_2026-02-18_0000

## RUN_STATUS: WARNINGS

**Rationale:** Totals are meaningful and fully priced from source evidence. However, the brief identifies "document control system costs" as a cost driver for this deliverable, and no pricing source provides DMS/software cost data. Under STRICT fallback policy, this item is not priced. The labour estimate is complete.

---

## S1 — Write Quarantine

- **PASS.** All output files written under `_Estimates/EST_DEL-01-05_2026-02-18_0000/`. No files outside `_Estimates/` were modified.

## S2 — Snapshot Created

- **PASS.** Snapshot folder `EST_DEL-01-05_2026-02-18_0000` created.

## S3 — BASIS_OF_ESTIMATE Validated

- **PASS.** `RATE_TABLE` is a valid enum value.

## S4 — Required Artifacts Exist

- **PASS.** All required artifacts produced:
  - Run_Context.md
  - Summary.md
  - QA_Report.md (this file)
  - Source_Index.md
  - Decision_Log.md
  - Assumptions_Log.md
  - WBS_CBS_Matrix.csv
  - Detail.csv (recommended; produced)

## S5 — Detail Schema Integrity

- **PASS.**
  - Detail.csv contains all 14 required columns: LineID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes.
  - All `Method` values are `RATE_TABLE` (valid).
  - No allowance/parametric lines present; convention check not applicable.
  - Amounts verified: L-01: 90 x 175 = 15,750; L-02: 50 x 80 = 4,000. Total: 19,750.

## S6 — Provenance Discipline

- **PASS.**
  - 2/2 priced rows (100%) have non-TBD `SourceRef` values.
  - Each SourceRef cites both the rate file (Professional_Staff_Rates.csv with RoleID) and the hours file (Level_of_Effort.csv with DeliverableID + RoleID).
  - No `location TBD` entries.

## S7 — Status Reporting

- **RUN_STATUS: WARNINGS**
  - See rationale at top of report.

## S8 — Operator Acceptance Checklist

| Check | Result |
|---|---|
| RUN_STATUS is OK or WARNINGS with bounded gaps | WARNINGS: gap is specifically "document control system costs" noted in brief but absent from PRICE_SOURCES |
| Basis-consistency checks pass | PASS: all Method values = RATE_TABLE; matches BASIS_OF_ESTIMATE; no mixed methods |
| Provenance completeness reported | PASS: 100% (2/2 rows) |
| Scope coverage explicit | PASS: 1 deliverable in scope, 1 estimated, 0 excluded, 0 blocked |
| No writes outside _Estimates/ | PASS |

---

## Coverage Report

| Metric | Value |
|---|---|
| Deliverables in scope | 1 |
| Deliverables estimated | 1 |
| Deliverables blocked | 0 |
| Total line items | 2 |
| Total hours | 140 |
| Total amount (CAD) | $19,750 |

## Basis-Consistency Check

| Metric | Value |
|---|---|
| BASIS_OF_ESTIMATE | RATE_TABLE |
| Lines with Method=RATE_TABLE | 2 (100%) |
| Lines with other Methods | 0 (0%) |
| ALLOW_MIXED_METHODS | FALSE |
| **Result** | PASS |

## Provenance Completeness

| Metric | Value |
|---|---|
| Total priced rows | 2 |
| Rows with SourceRef | 2 (100%) |
| Rows with `location TBD` | 0 |
| **Result** | PASS |

## Blocker Analysis (from dependency evidence)

| Metric | Value |
|---|---|
| Total dependencies (DEL-01-05) | 11 |
| ANCHOR edges | 4 |
| EXECUTION edges | 7 |
| Upstream blockers to estimating | 0 (all upstream deps are execution prerequisites, not cost-information gaps) |
| Downstream handovers | 1 (DEL-01-07) |

## What to Fix for a Cleaner Rerun

1. **Document control system costs:** If DMS licensing, setup, or SaaS subscription costs should be carried in DEL-01-05, add a pricing source (quote or rate table entry) for document management software. Without this, the line cannot be priced under STRICT fallback policy.
2. **Overhead/markup:** Current amounts are bare labour cost only. If burdened rates or markup factors are required, provide an overhead rate table or multiplier in PRICE_SOURCES.
3. **LOE Basis field:** The Level_of_Effort.csv records Basis=PARAMETRIC for all rows, but this run uses BASIS_OF_ESTIMATE=RATE_TABLE. The hours are treated as given quantities priced at rate-table rates. If the LOE hours themselves require parametric validation, that is outside this run's scope.
