# QA Report -- EST_DEL-05-05_2026-02-18_1800

## RUN_STATUS: WARNINGS

Totals exist but are provisional. Material TBDs and assumptions remain due to missing branding guidelines and unresolved illumination decision.

---

## S1 -- Write Quarantine Respected

**PASS.** All files written under `_Estimates/EST_DEL-05-05_2026-02-18_1800/`. No files outside `_Estimates/` were modified.

## S2 -- Snapshot Created

**PASS.** Snapshot folder `EST_DEL-05-05_2026-02-18_1800` exists.

## S3 -- BASIS_OF_ESTIMATE Validated

**PASS.** `BASIS_OF_ESTIMATE=QUOTE` is a valid enum value. Fallback to ALLOWANCE is authorized by `FALLBACK_POLICY=ALLOW_ALLOWANCE` and logged in Decision_Log.md (DEC-EST-001).

## S4 -- Required Artifacts Exist

**PASS.** All required files present:
- [x] Run_Context.md
- [x] Summary.md
- [x] QA_Report.md
- [x] Source_Index.md
- [x] Decision_Log.md
- [x] Assumptions_Log.md
- [x] WBS_CBS_Matrix.csv

Additional files emitted:
- [x] Detail.csv
- [x] Blockers.md
- [x] Risk_Register.md

## S5 -- Detail Schema Integrity

**PASS.**
- Detail.csv contains all 14 required columns: LineID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes.
- Method values: `ALLOWANCE` (valid enum).
- Allowance convention: Qty=1, Unit=LS, UnitRate=Amount. **PASS** for both rows.
- 2 rows total.

## S6 -- Provenance Discipline

**PASS.**
- 2/2 priced rows (100%) have non-TBD SourceRef values.
  - L-05-05-01: `Optional_Items_Pricing.csv > OPT-10 (RecommendedPrice)`
  - L-05-05-02: `Optional_Items_Pricing.csv > OPT-11 (RecommendedPrice)`
- Provenance completeness: **100%**.
- No missing-source offenders.

## S7 -- Status Reporting

**RUN_STATUS = WARNINGS.** Justification:
- Totals exist ($12,000 non-illuminated primary; $22,000 illuminated alternate).
- Material TBDs remain:
  - Town branding guidelines PENDING (DEP-05-05-007) -- cannot finalize design.
  - Illumination decision TBD -- $10,000 delta between scenarios.
  - Sign quantity assumed as 1 -- may need to scale.
- All pricing is allowance-grade (LOW confidence) due to fallback from QUOTE.
- Does not meet `OK` because critical input gaps exist.
- Does not meet `FAILED_INPUTS` because meaningful (if provisional) totals are produced using authorized fallback.

## Basis-Consistency Checks

| Check | Result |
|---|---|
| Declared BASIS_OF_ESTIMATE | QUOTE |
| Actual methods used | ALLOWANCE (100% of rows) |
| ALLOW_MIXED_METHODS | TRUE |
| FALLBACK_POLICY | ALLOW_ALLOWANCE |
| Deviation authorized? | YES -- DEC-EST-001 |
| **Result** | **PASS (deviation is logged and authorized)** |

## Coverage

| Metric | Value |
|---|---|
| Deliverables in scope | 1 (DEL-05-05) |
| Deliverables covered with pricing | 1 |
| Deliverables missing | 0 |
| Deliverables blocked | 0 (pricing produced via fallback; design is blocked on branding guidelines) |
| Line items produced | 2 (1 primary + 1 alternate) |

## Blocker Counts (from Dependency Evidence)

| Blocker Type | Count | Details |
|---|---|---|
| External constraint (PENDING) | 1 | DEP-05-05-007: Town branding guidelines |
| Upstream deliverable (TBD) | 3 | DEP-05-05-004 (DEL-02-01), DEP-05-05-005 (DEL-02-04), DEP-05-05-006 (DEL-02-06, conditional) |

## What to Fix for a Cleaner Rerun

1. **Obtain Town branding guidelines** from the Owner. This resolves DEP-05-05-007 and enables design-specific vendor quoting.
2. **Resolve illumination decision** (illuminated vs non-illuminated). This collapses the two scenarios into one and removes the $10,000 uncertainty band.
3. **Obtain vendor quote** for signage fabrication and installation. This would allow pricing at Method=QUOTE (the declared basis) instead of ALLOWANCE fallback.
4. **Confirm sign quantity** (1 or more) once branding guidelines and building exterior concept are available.
5. **Verify electrical circuit cost** is carried by DEL-02-06 during aggregation/reconciliation (ASM-EST-005).
