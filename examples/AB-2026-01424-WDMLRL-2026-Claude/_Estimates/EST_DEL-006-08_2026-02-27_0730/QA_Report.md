# QA Report — EST_DEL-006-08_2026-02-27_0730

## RUN_STATUS: OK

**Justification:** All 4 priced line items have complete quantity and rate data from parametric pricing sources. No TBD amounts. No critical input gaps. Totals are meaningful. Basis-consistency checks pass (all lines use PARAMETRIC method, consistent with BASIS_OF_ESTIMATE=PARAMETRIC). Provenance is 100% complete.

---

## S1 — Write Quarantine Respected

| Check | Result |
|-------|--------|
| All output files written under `_Estimates/EST_DEL-006-08_2026-02-27_0730/` | PASS |
| No files outside `_Estimates/` modified | PASS |
| No deliverable working files modified | PASS |
| No lifecycle files modified | PASS |
| No decomposition outputs modified | PASS |

## S2 — Snapshot Created

| Check | Result |
|-------|--------|
| Snapshot folder `EST_DEL-006-08_2026-02-27_0730` exists | PASS |

## S3 — BASIS_OF_ESTIMATE Validated

| Check | Result |
|-------|--------|
| `BASIS_OF_ESTIMATE` present | PASS |
| Value `PARAMETRIC` is valid enum | PASS |

## S4 — Required Artifacts Exist

| Artifact | Status |
|----------|--------|
| `Run_Context.md` | PRESENT |
| `Items.csv` | PRESENT |
| `Summary.md` | PRESENT |
| `QA_Report.md` | PRESENT (this file) |
| `Source_Index.md` | PRESENT |
| `Detail.csv` | PRESENT (optional; produced) |
| `WBS_CBS_Matrix.csv` | PRESENT |
| `Decision_Log.md` | PRESENT |
| `Assumptions_Log.md` | PRESENT |

## S5 — CSV Schema Integrity

### Items.csv

| Check | Result |
|-------|--------|
| Parseable CSV | PASS |
| Required columns present (ItemID, DeliverableID, Description, Qty, Unit, PricingMode, SourceDoc, SourceSection, Notes) | PASS |
| All rows trace to a source document | PASS |
| All rows trace to a source section | PASS |
| PricingMode values valid (UNIT_RATE or LUMP_SUM) | PASS |
| Row count | 20 items |
| Items with Qty=TBD | 0 |

### Detail.csv

| Check | Result |
|-------|--------|
| Parseable CSV | PASS |
| Required columns present (LineID, ItemID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes) | PASS |
| Method values valid (all PARAMETRIC) | PASS |
| Allowance/parametric convention (Qty=1, Unit=LS, UnitRate=Amount for LS items) | PASS — LS items with $0 amount correctly set Qty=1, Unit=LS, UnitRate=0, Amount=0 |
| Row count | 20 lines |
| Lines with Amount=TBD | 0 |

## S6 — Provenance Discipline

| Metric | Value |
|--------|-------|
| Rows with non-TBD SourceRef | 20 / 20 (100%) |
| Rows with `location TBD` SourceRef | 0 |
| Provenance completeness | 100% |
| Top missing-source offenders | None |

## S7 — Status Reporting

| Field | Value |
|-------|-------|
| **RUN_STATUS** | **OK** |
| Totals meaningful | Yes — $11,365.00 CAD |
| Critical input gaps | None |
| Material TBDs | None in priced lines |
| Material assumptions | Documented in Assumptions_Log.md |

## Quantity Takeoff Coverage

| Check | Result |
|-------|--------|
| Documents read for DEL-006-08 | 5/5 (_CONTEXT.md, Datasheet.md, Specification.md, Guidance.md, Procedure.md) |
| Missing documents | None |
| Items extracted | 20 (4 role-level + 16 activity/content-level) |
| Deliverables with missing documents | 0 |

## Pricing Coverage

| Metric | Value |
|--------|-------|
| Items priced (Amount > 0) | 4 / 20 |
| Items at $0 (effort included in role LOE) | 16 / 20 |
| Items with Amount=TBD | 0 / 20 |
| Pricing coverage explanation | 4 role-level items carry the full cost; 16 activity items are $0 because their effort is embedded within the role-level LOE allocations. This is by design — the LOE pricing source provides hours per role, not per activity. |

## Basis-Consistency Checks

| Check | Result |
|-------|--------|
| BASIS_OF_ESTIMATE | PARAMETRIC |
| Method values in Detail.csv | All PARAMETRIC |
| Mixed methods used | No |
| Fallback used | No |
| Basis-consistency | PASS |

## S8 — Operator Acceptance Checklist

| Criterion | Status |
|-----------|--------|
| RUN_STATUS is OK or WARNINGS with clearly bounded gaps | PASS (OK) |
| Quantity takeoff (Items.csv) reviewed for completeness | PASS — 20 items covering all 5 procedure phases and all specification content sections |
| Basis-consistency checks pass | PASS — 100% PARAMETRIC |
| Provenance completeness reported and top gaps actionable | PASS — 100% provenance; no gaps |
| Scope coverage explicit | PASS — 1 deliverable, 1 package, included/excluded documented in Summary.md |
| No writes outside _Estimates/ | PASS |

## What to Fix for a Cleaner Rerun

1. **Activity-level LOE breakdown.** If per-activity hours were available in Level_of_Effort.csv (breaking the 49 Plumbing Engineer hours into Phase 1, 2, 3, 4, 5 components), the estimate would have more granular pricing.
2. **Subconsultant rates.** Current rates are parametric (MEDIUM confidence). Actual subconsultant fee proposals would upgrade confidence to HIGH.
3. **Construction cost cross-reference.** This estimate covers design effort only. A companion estimate for PKG-014 (Plumbing & Water Systems Installation) would provide construction costs for the physical systems specified in DEL-006-08.
