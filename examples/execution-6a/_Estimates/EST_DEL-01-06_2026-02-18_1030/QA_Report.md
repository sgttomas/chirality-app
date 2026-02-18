# QA Report -- EST_DEL-01-06_2026-02-18_1030

## RUN_STATUS: WARNINGS

The run produced meaningful labor totals but material TBDs remain for non-labor site costs.

---

## S1 -- Write Quarantine Respected

**PASS.** All files written exclusively under `_Estimates/EST_DEL-01-06_2026-02-18_1030/`. No deliverable content, lifecycle files, decomposition outputs, or dependency registers were modified.

## S2 -- Snapshot Created

**PASS.** Snapshot folder `EST_DEL-01-06_2026-02-18_1030` created under `_Estimates/`.

## S3 -- BASIS_OF_ESTIMATE Validated

**PASS.** `RATE_TABLE` is a valid enum value.

## S4 -- Required Artifacts Exist

**PASS.** All required artifacts produced:
- Run_Context.md
- Summary.md
- QA_Report.md (this file)
- Source_Index.md
- Decision_Log.md
- Assumptions_Log.md
- WBS_CBS_Matrix.csv
- Detail.csv (recommended; produced)

## S5 -- Detail Schema Integrity

**PASS.**
- Detail.csv contains all 14 required columns: LineID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes.
- Method values: all rows use `RATE_TABLE` (consistent with BASIS_OF_ESTIMATE).
- No ALLOWANCE or PARAMETRIC rows present, so allowance/parametric convention check is N/A.
- TBD amounts are properly flagged with TBD in Qty, UnitRate, and Amount fields.

## S6 -- Provenance Discipline

**PASS (with warnings).**
- 2 of 4 rows (50%) have complete SourceRef pointing to specific files and rows.
- 2 of 4 rows (50%) have SourceRef = `location TBD` (the non-labor items).
- **Top missing-source offenders:**
  1. L-0106-003 (Temporary facilities and fencing) -- no rate table for site facility costs
  2. L-0106-004 (Site cleaning) -- no rate table for cleaning costs

## S7 -- Status Reporting

**RUN_STATUS = WARNINGS**

Rationale: Priced labor totals ($203,700 CAD) are meaningful and fully sourced. However, 2 of 4 line items (representing non-labor site costs) remain TBD due to missing rate table evidence. The total understates the full deliverable cost. Gaps are clearly bounded: only non-labor site general costs are missing.

## Coverage Report

| Metric | Value |
|---|---|
| Deliverables in scope | 1 |
| Deliverables covered (at least 1 priced line) | 1 |
| Deliverables missing | 0 |
| Deliverables blocked | 0 |
| Total line items | 4 |
| Priced line items | 2 |
| TBD line items | 2 |
| Priced total | $203,700 CAD |

## Basis-Consistency Check

**PASS.** All 4 rows use `Method=RATE_TABLE`, consistent with `BASIS_OF_ESTIMATE=RATE_TABLE`. `ALLOW_MIXED_METHODS=FALSE` is respected. No fallback methods were used (STRICT policy: TBD amounts used instead).

## Blocker Summary (from dependency evidence)

- Dependencies.csv loaded: 8 rows (4 ANCHOR, 4 EXECUTION).
- Upstream prerequisites: DEL-01-02 (schedule), DEL-03-01 (site plan) -- these are execution-phase prerequisites, not estimate blockers.
- Upstream interface: DEL-01-03 (H&S plan) -- coordination interface, not estimate blocker.
- No dependency rows include `EstimateImpactClass` hints.
- **Conclusion:** 0 estimate-blocking dependencies identified.

## What to Fix for a Cleaner Rerun

1. **Add non-labor rate evidence.** Provide rate tables or quotes for:
   - Temporary site facilities and fencing (monthly rental rates, or lump sum per project duration)
   - Site cleaning services (daily cleaning rate, or lump sum per project duration)
   Adding these to PRICE_SOURCES would resolve the 2 TBD line items and allow a complete total.

2. **Consider ALLOW_ALLOWANCE or ALLOW_PARAMETRIC fallback.** If non-labor costs can be estimated parametrically (e.g., as a percentage of construction value per PP-24) or from an allowance table, changing FALLBACK_POLICY would allow pricing those items in a rerun.

3. **No other gaps.** Labor pricing is complete and fully sourced. Decomposition alignment is confirmed. Dependencies are loaded with no estimate-blocking issues.
