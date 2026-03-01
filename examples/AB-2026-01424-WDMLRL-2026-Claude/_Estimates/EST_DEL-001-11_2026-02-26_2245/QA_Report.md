# QA_Report — EST_DEL-001-11_2026-02-26_2245

## RUN_STATUS: WARNINGS

**Rationale:** Priced totals are meaningful for the LOE-based professional services scope ($10,365 CAD across 70 hours / 5 roles). However, 3 of 11 line items remain TBD (existing conditions survey, P.Eng./AAAL stamp fees, building permit fees), representing material cost gaps that prevent a complete deliverable cost.

---

## S1 — Write Quarantine Respected

| Check | Result |
|---|---|
| All outputs under `_Estimates/` | PASS |
| No modification to deliverable files | PASS |
| No modification to lifecycle files | PASS |
| No modification to decomposition | PASS |

## S2 — Snapshot Created

| Check | Result |
|---|---|
| Snapshot folder exists | PASS — `EST_DEL-001-11_2026-02-26_2245/` |

## S3 — BASIS_OF_ESTIMATE Validated

| Check | Result |
|---|---|
| `BASIS_OF_ESTIMATE` = `PARAMETRIC` | PASS — valid enum value |

## S4 — Required Artifacts Exist

| Artifact | Status |
|---|---|
| Run_Context.md | PASS |
| Items.csv | PASS |
| Summary.md | PASS |
| QA_Report.md | PASS (this file) |
| Source_Index.md | PASS |
| Detail.csv | PASS (optional; produced) |
| WBS_CBS_Matrix.csv | PASS |
| Decision_Log.md | PASS |
| Assumptions_Log.md | PASS |

## S5 — CSV Schema Integrity

### Items.csv

| Check | Result |
|---|---|
| Parseable CSV | PASS |
| Required columns present (ItemID, DeliverableID, Description, Qty, Unit, PricingMode, SourceDoc, SourceSection, Notes) | PASS |
| All rows trace to source document and section | PASS |
| PricingMode values valid (UNIT_RATE or LUMP_SUM) | PASS — 5 UNIT_RATE, 6 LUMP_SUM |
| Row count | 11 items |

### Detail.csv

| Check | Result |
|---|---|
| Parseable CSV | PASS |
| Required columns present (LineID, ItemID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes) | PASS |
| Method values valid | PASS — all PARAMETRIC |
| Allowance/parametric convention (Qty=1, Unit=LS, UnitRate=Amount for LS items) | PASS for priced LS items (DL-007 through DL-009 at $0); TBD items (DL-006, DL-010, DL-011) use Qty=1, Unit=LS, UnitRate=TBD, Amount=TBD |
| Row count | 11 lines |

## S6 — Provenance Discipline

| Metric | Value |
|---|---|
| Total rows in Detail.csv | 11 |
| Rows with substantive SourceRef | 8 (73%) |
| Rows with `location TBD` SourceRef | 3 (27%) |
| Provenance completeness | 73% |

### Top Missing-Source Offenders

| LineID | Description | Gap Reason |
|---|---|---|
| DL-006 | Existing conditions survey — Old North Shop | No survey cost data in price sources |
| DL-010 | P.Eng. stamp / AAAL review fees | No professional stamp fee data in price sources |
| DL-011 | Building permit application — Camrose County | No permit fee data in price sources; OI-003 open |

## S7 — Status Reporting

| Field | Value |
|---|---|
| RUN_STATUS | WARNINGS |
| Justification | 73% provenance completeness; 3 TBD items with no pricing basis; priced total ($10,365) is meaningful but incomplete |

## S8 — Operator Acceptance Checklist

| Check | Status | Notes |
|---|---|---|
| RUN_STATUS is OK or WARNINGS with bounded gaps | PASS | WARNINGS; gaps are bounded (3 specific items) |
| Quantity takeoff (Items.csv) reviewed for completeness | PASS | 11 items covering all Procedure steps and Specification requirements |
| Basis-consistency checks pass | PASS | All methods = PARAMETRIC; consistent with BASIS_OF_ESTIMATE |
| Provenance completeness reported | PASS | 73% with top gaps listed |
| Scope coverage explicit | PASS | 1 deliverable (DEL-001-11); 5 LOE roles; 6 additional activity items |
| No writes outside _Estimates/ | PASS | Confirmed |

---

## Pricing Coverage

| Category | Count | Percentage |
|---|---|---|
| Priced (Amount != TBD) | 8 | 73% |
| TBD (Amount = TBD) | 3 | 27% |
| Total | 11 | 100% |

## Quantity Takeoff Coverage

| Source Document | Items Extracted | Notes |
|---|---|---|
| Datasheet | 0 direct (attributes inform context) | Datasheet attributes inform specification scope but do not generate separate priceable items for the specification deliverable |
| Specification | 3 items (ITEM-007, ITEM-010, ITEM-011) | Code review, stamp fees, permit fees identified from requirements/standards/verification |
| Guidance | 0 direct (informs context) | Guidance trade-offs and considerations inform specification scope |
| Procedure | 8 items (ITEM-001 through ITEM-006, ITEM-008, ITEM-009) | Work steps generate effort-based priceable items |

## What to Fix for a Cleaner Rerun

1. **Obtain survey cost data** — Add a pricing source (quote or allowance) for the Old North Shop existing conditions survey (ITEM-006).
2. **Obtain P.Eng./AAAL fee data** — Add professional stamp and registration fee data to price sources (ITEM-010).
3. **Resolve OI-003** — Confirm building permit fee amount and payment responsibility (Owner vs. Proponent) with Camrose County (ITEM-011).
4. **Replace parametric rates with contracted rates** — When actual contracted staff rates are available, update `Professional_Staff_Rates.csv` to move from MEDIUM to HIGH confidence.
