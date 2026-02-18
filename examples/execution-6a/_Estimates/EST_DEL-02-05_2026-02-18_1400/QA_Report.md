# QA Report -- DEL-02-05 Estimate

## RUN_STATUS: OK

The estimate is meaningful with well-sourced totals. All line items have rate-table evidence. One conditional item (fire protection) carries LOW confidence but is clearly flagged.

---

## S1 -- Write Quarantine

- **PASS.** All files written under `_Estimates/EST_DEL-02-05_2026-02-18_1400/` only.
- No project truth files modified.

## S2 -- Snapshot Created

- **PASS.** Snapshot folder `EST_DEL-02-05_2026-02-18_1400` created.

## S3 -- BASIS_OF_ESTIMATE Validated

- **PASS.** `RATE_TABLE` is a valid enum value.
- Note: Source CSV metadata labels rates as `PARAMETRIC`; agent treats structured tabular rates as rate-table entries. Logged as DEC-01.

## S4 -- Required Artifacts

- **PASS.** All required files present:
  - `Run_Context.md`
  - `Summary.md`
  - `QA_Report.md`
  - `Source_Index.md`
  - `Decision_Log.md`
  - `Assumptions_Log.md`
  - `WBS_CBS_Matrix.csv`
  - `Detail.csv` (recommended; produced)

## S5 -- Detail Schema Integrity

- **PASS.** `Detail.csv` contains all 14 required columns.
- **PASS.** All 16 `Method` values are `RATE_TABLE` (valid enum).
- **PASS.** Lump-sum items (L-13, L-14, L-15, L-16) use `Qty=1, Unit=LS, UnitRate=Amount` convention where applicable. Note: L-15 and L-16 are lump-sum RATE_TABLE items (not ALLOWANCE/PARAMETRIC), so the LS convention is applied for consistency.

## S6 -- Provenance Discipline

- **PASS.** 16 of 16 priced rows (100%) have non-TBD `SourceRef`.
- **Missing-source offenders:** None.

## S7 -- Status Reporting

- **RUN_STATUS: OK**
- Totals are meaningful; no critical input gaps.
- One LOW-confidence item (fire protection, $108,000) is clearly bounded and separately identifiable.

## S8 -- Operator Acceptance Checklist

| Check | Status | Notes |
|-------|--------|-------|
| RUN_STATUS OK or bounded WARNINGS | OK | All totals meaningful |
| Basis-consistency | PASS | 100% RATE_TABLE; no mixed methods |
| Provenance completeness | 100% | 16/16 rows sourced |
| Scope coverage | 1/1 deliverable covered | DEL-02-05 fully priced |
| Excluded items documented | Yes | 5 exclusions per cost ownership |
| No writes outside _Estimates/ | PASS | Quarantine respected |

---

## Coverage Analysis

| Metric | Value |
|--------|-------|
| Deliverables in scope | 1 |
| Deliverables covered | 1 |
| Deliverables missing | 0 |
| Deliverables blocked | 0 |
| Line items produced | 16 |
| Lines with TBD Amount | 0 |
| Lines with TBD SourceRef | 0 |

## Basis-Consistency Check

| Method | Count | % |
|--------|-------|---|
| RATE_TABLE | 16 | 100% |
| Other | 0 | 0% |

**PASS.** No mixed methods; consistent with `BASIS_OF_ESTIMATE=RATE_TABLE` and `ALLOW_MIXED_METHODS=FALSE`.

## Blocker Summary (from dependency evidence)

| DependencyID | Type | Impact on Estimate | Status |
|-------------|------|-------------------|--------|
| DEP-0205-E08 | INTERFACE | Compressed air scope boundary -- no pricing impact (excluded per brief) | Information only |
| DEP-0205-E11 | CONSTRAINT | PW bay count affects sump qty -- assumed 4 per PP-12 (CONFIRMED) | Mitigated by confirmed parameter |
| DEP-0205-E12 | CONSTRAINT | AHJ code confirmation pending -- fire protection conditional | Flagged; LOW confidence on L-12 |

## What to Fix for a Cleaner Rerun

1. **Confirm fire protection requirement** with AHJ. If not required, remove L-12 and re-run. If required, upgrade L-12 confidence to MED.
2. **Resolve compressed air scope boundary** (CON-M-01) between DEL-02-05 and DEL-02-02. Currently excluded per brief; confirm this is correct.
3. **Validate area zoning split** (ASM-01) against actual architectural layout when available from DEL-02-01.
4. **Confirm kitchen/laundry rough-in scope** (L-13) aligns with DEL-05-06 boundary expectations.
