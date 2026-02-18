# QA Report: EST_DEL-03-01_2026-02-18_1400

## RUN_STATUS: OK

Totals are meaningful; no critical input gaps. All line items are fully priced with complete provenance.

---

## S1 -- Write Quarantine

- **PASS.** All files written under `_Estimates/EST_DEL-03-01_2026-02-18_1400/` only.
- No files outside the estimating tool root were modified.

## S2 -- Snapshot Created

- **PASS.** Snapshot folder `EST_DEL-03-01_2026-02-18_1400` created under `_Estimates/`.

## S3 -- BASIS_OF_ESTIMATE Validated

- **PASS.** `RATE_TABLE` is a valid enum value.

## S4 -- Required Artifacts Exist

- **PASS.** All required files present:
  - `Run_Context.md`
  - `Summary.md`
  - `QA_Report.md`
  - `Source_Index.md`
  - `Decision_Log.md`
  - `Assumptions_Log.md`
  - `WBS_CBS_Matrix.csv`
  - `Detail.csv` (optional but produced)

## S5 -- Detail Schema Integrity

- **PASS.**
  - `Detail.csv` contains all 14 required columns: LineID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes.
  - Method values: all `RATE_TABLE` -- valid.
  - No ALLOWANCE or PARAMETRIC lines present, so allowance/parametric convention check is N/A.
  - All amounts are whole dollars (ROUNDING=DOLLAR respected).

## S6 -- Provenance Discipline

- **PASS.**
  - 2 of 2 priced rows (100%) have non-TBD SourceRef.
  - Each SourceRef cites both the rate table file + role ID and the LOE file + deliverable/role row.
  - No `location TBD` entries.

### Provenance Completeness

| Metric | Value |
|---|---|
| Total priced rows | 2 |
| Rows with SourceRef | 2 |
| Rows with `location TBD` | 0 |
| Provenance completeness | 100% |

## S7 -- Status Reporting

- **RUN_STATUS = OK** declared above.

## S8 -- Operator Acceptance Checklist

| Criterion | Result |
|---|---|
| RUN_STATUS is OK or bounded WARNINGS | OK |
| Basis-consistency checks pass | PASS -- all lines are RATE_TABLE; matches BASIS_OF_ESTIMATE |
| Provenance completeness reported | 100% |
| Scope coverage explicit | 1 in scope / 0 excluded / 0 blocked |
| No writes outside _Estimates/ | Confirmed |

---

## Coverage

| Metric | Value |
|---|---|
| Deliverables in scope | 1 (DEL-03-01) |
| Deliverables covered (with priced lines) | 1 |
| Deliverables missing | 0 |
| Deliverables blocked | 0 |

## Basis-Consistency Check

| Check | Result |
|---|---|
| BASIS_OF_ESTIMATE | RATE_TABLE |
| Methods in Detail.csv | RATE_TABLE (2 lines) |
| Mixed methods detected | No |
| ALLOW_MIXED_METHODS | FALSE |
| Consistency | PASS |

## Dependency / Blocker Assessment

- Dependencies loaded: 10 ACTIVE rows from Dependencies.csv
- Upstream execution dependencies: 3 (DEL-02-01, DEL-08-01, DEL-02-02)
- All SatisfactionStatus = TBD
- **No blockers to estimating identified.** The upstream dependencies are coordination/sequencing dependencies for deliverable content production, not for pricing inputs. The estimate uses rate tables and LOE estimates that are independent of upstream deliverable completion.

## What to Fix for a Cleaner Rerun

- Nothing required. This is a clean run with no TBDs, no warnings, and full provenance coverage.
- If actual firm rates become available, replace Professional_Staff_Rates.csv and rerun to improve from MARKET to ACTUAL basis.
- If actual tracked effort data becomes available, replace Level_of_Effort.csv hours and rerun.
