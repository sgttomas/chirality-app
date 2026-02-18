# QA Report: EST_DEL-05-06_2026-02-18_1900

## RUN_STATUS: WARNINGS

**Rationale:** All line items are priced with traceable source references and all deliverables in scope are covered. Status is WARNINGS (not OK) because:
1. The method classification required an explicit decision to treat PARAMETRIC-labeled source data as QUOTE-equivalent (DEC-EST-001).
2. No vendor-specific quote exists; pricing is based on retail/parametric midpoints.
3. Price range exposure exists (min $13,800 to max $24,100 vs estimate $18,600).

---

## S1 -- Write Quarantine

- **Status:** PASS
- All files written under `_Estimates/EST_DEL-05-06_2026-02-18_1900/` only.
- No project truth files modified.

## S2 -- Snapshot Created

- **Status:** PASS
- Snapshot folder: `EST_DEL-05-06_2026-02-18_1900`

## S3 -- BASIS_OF_ESTIMATE Validated

- **Status:** PASS
- `BASIS_OF_ESTIMATE = QUOTE` -- valid enum value.

## S4 -- Required Artifacts Exist

- **Status:** PASS
- Run_Context.md: present
- Summary.md: present
- QA_Report.md: present (this file)
- Source_Index.md: present
- Decision_Log.md: present
- Assumptions_Log.md: present
- WBS_CBS_Matrix.csv: present
- Detail.csv: present (optional but produced)

## S5 -- Detail Schema Integrity

- **Status:** PASS
- Detail.csv contains all 14 required columns: LineID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes.
- All `Method` values = `QUOTE` (valid enum).
- Line L-0506-06 (installation) uses Qty=1, Unit=LS, UnitRate=Amount (allowance/parametric convention respected for lump-sum items).
- 6 rows total; all parseable.

## S6 -- Provenance Discipline

- **Status:** PASS
- Provenance completeness: **100%** (6/6 rows have non-TBD SourceRef).
- All SourceRef values point to Optional_Items_Pricing.csv with specific row IDs (OPT-12 through OPT-17).
- No `location TBD` entries.

## S7 -- Basis-Consistency Check

- **Status:** PASS (with logged decision)
- `BASIS_OF_ESTIMATE = QUOTE`; all `Method` values = `QUOTE`.
- `ALLOW_MIXED_METHODS = FALSE`; no mixed methods present.
- **Note:** Source data self-labels as `PARAMETRIC`. The brief explicitly authorizes treating retail appliance pricing as quote-equivalent. This is logged as DEC-EST-001.

## Blocker Analysis (from dependency evidence)

- **Dependency rows analyzed:** 10 (from Dependencies.csv)
- **Blockers to estimating:** 0
- **Key interfaces confirmed:**
  - DEL-02-05 / DEL-02-06 provide base building rough-in (upstream; does not affect appliance pricing)
  - DEL-05-07 boundary is clear (FF&E excluded from DEL-05-06)
  - Owner option election (DEP-05-06-009) is a constraint on implementation, not on estimating

## Coverage Summary

| Metric | Value |
|---|---|
| Deliverables in scope | 1 |
| Deliverables covered | 1 |
| Deliverables blocked | 0 |
| Line items produced | 6 |
| Rows with Amount = TBD | 0 |
| Provenance completeness | 100% |

## What to Fix for a Cleaner Rerun

1. **Obtain actual vendor quotes** for appliances to move from retail-parametric to true vendor quote basis. This would resolve the method-classification decision and improve confidence from MEDIUM to HIGH.
2. **Confirm stove/oven fuel type** (electric vs gas) to resolve whether a gas service connection cost should be included.
3. **Confirm delivery cost treatment** -- whether delivery is included in equipment prices or should be separately itemized.
4. **Confirm sales tax treatment** -- whether GST/PST should be included in the estimate or is handled at the contract level.
5. **Narrow price ranges** -- current min/max spread is $10,300 ($13,800 to $24,100). Vendor quotes would narrow this considerably.
