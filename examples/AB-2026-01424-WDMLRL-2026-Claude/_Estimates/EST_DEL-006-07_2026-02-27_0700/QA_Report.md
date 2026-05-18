# QA Report — EST_DEL-006-07_2026-02-27_0700

## RUN_STATUS: OK

---

## S1 — Write Quarantine Respected

| Check | Result |
|---|---|
| All output files written under `_Estimates/EST_DEL-006-07_2026-02-27_0700/` | PASS |
| No files modified outside `_Estimates/` | PASS |

---

## S2 — Snapshot Created

| Check | Result |
|---|---|
| Snapshot folder `EST_DEL-006-07_2026-02-27_0700` exists | PASS |

---

## S3 — BASIS_OF_ESTIMATE Validated

| Check | Result |
|---|---|
| BASIS_OF_ESTIMATE value | PARAMETRIC |
| Value is in allowed enum (QUOTE, RATE_TABLE, HISTORICAL, PARAMETRIC, ALLOWANCE) | PASS |

---

## S4 — Required Artifacts Exist

| Artifact | Status |
|---|---|
| Run_Context.md | PRESENT |
| Items.csv | PRESENT |
| Summary.md | PRESENT |
| QA_Report.md | PRESENT (this file) |
| Source_Index.md | PRESENT |
| Decision_Log.md | PRESENT |
| Assumptions_Log.md | PRESENT |
| WBS_CBS_Matrix.csv | PRESENT |
| Detail.csv | PRESENT (optional; produced for full run) |

---

## S5 — CSV Schema Integrity

### Items.csv

| Check | Result |
|---|---|
| Parseable CSV | PASS |
| Required columns present (ItemID, DeliverableID, Description, Qty, Unit, PricingMode, SourceDoc, SourceSection, Notes) | PASS |
| All rows have DeliverableID = DEL-006-07 | PASS |
| PricingMode values valid (UNIT_RATE or LUMP_SUM) | PASS — 13 LUMP_SUM, 4 UNIT_RATE |
| All rows trace to a source document and section | PASS |
| Row count | 17 items |

### Detail.csv

| Check | Result |
|---|---|
| Parseable CSV | PASS |
| Required columns present (LineID, ItemID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes) | PASS |
| Method values valid (PARAMETRIC for all rows) | PASS |
| Allowance/parametric convention — LS items: Qty=1, Unit=LS, UnitRate=Amount | PASS (DL-005 through DL-017: Qty=1, Unit=LS, UnitRate=0, Amount=0; convention respected for zero-amount LS lines) |
| All Amounts are numeric (no TBD) | PASS |
| Row count | 17 detail lines |

---

## S6 — Provenance Discipline

| Check | Result |
|---|---|
| % of priced rows (Amount > 0) with non-TBD SourceRef | 100% (4/4 priced rows) |
| % of all rows with non-TBD SourceRef | 100% (17/17 rows) |
| Top missing-source offenders | None — all rows have SourceRef |

---

## S7 — Status Reporting

| Check | Result |
|---|---|
| RUN_STATUS declared | OK |
| Justification | All items priced; no TBD amounts; all provenance complete; basis is consistent (100% PARAMETRIC); all price sources usable |

---

## S8 — Operator Acceptance Checklist

| Criterion | Status | Notes |
|---|---|---|
| RUN_STATUS is OK or WARNINGS with bounded gaps | PASS — OK | |
| Quantity takeoff (Items.csv) reviewed for completeness | PASS | 17 items extracted from all 4 documents; covers all 9 Procedure steps plus 4 labour roles |
| Basis-consistency checks pass | PASS | All 17 Detail.csv lines use Method=PARAMETRIC; matches BASIS_OF_ESTIMATE |
| Provenance completeness reported | PASS | 100% provenance; see S6 above |
| Scope coverage explicit | PASS | 1 deliverable (DEL-006-07), 1 package (PKG-006); scope exclusions documented in Summary.md (no material costs, Old North Shop TBD) |
| No writes outside _Estimates/ | PASS | |

---

## Quantity Takeoff Coverage

| Document | Items Extracted | Notes |
|---|---|---|
| Datasheet.md | 3 | Building context, sizing parameters, fixtures used for ITEM-012, ITEM-014 through ITEM-017 |
| Specification.md | 2 | REQ-007 (emergency shower) -> ITEM-011; REQ-012 (washroom) -> ITEM-013 |
| Guidance.md | 0 direct | Principles and trade-offs informed scope of calculation items but did not generate separate priceable items |
| Procedure.md | 12 | Steps 1-9 mapped to ITEM-001 through ITEM-010 plus labour items |

---

## Pricing Coverage

| Metric | Value |
|---|---|
| Total items | 17 |
| Items priced (Amount > 0) | 4 (23.5%) |
| Items at $0 (included in parent effort) | 13 (76.5%) |
| Items TBD | 0 (0%) |
| Total estimate | $11,365 CAD |

**Note:** The 13 items at $0 are not missing prices. They represent calculation sub-artifacts whose production effort is captured in the 49-hour Plumbing Engineer allocation (DL-004). This is the correct parametric approach: the Level_of_Effort model allocates total hours by role, not by sub-artifact. The Items.csv provides the sub-artifact-level takeoff for scope traceability; Detail.csv prices at the role-effort level to avoid double-counting.

---

## Basis-Consistency Check

| Check | Result |
|---|---|
| BASIS_OF_ESTIMATE | PARAMETRIC |
| ALLOW_MIXED_METHODS | TRUE |
| Methods used in Detail.csv | PARAMETRIC (100%) |
| Deviation from basis | None |
| Fallback items | None |

---

## What to Fix for a Cleaner Rerun

1. **Resolve CFT-001 (Old North Shop scope).** If Old North Shop plumbing is included in DEL-006-07 scope, additional Plumbing Engineer hours would be needed in Level_of_Effort.csv.
2. **Validate LOE hours against actual project experience.** The 49-hour Plumbing Engineer allocation is a parametric estimate; comparison with similar completed projects would increase confidence.
3. **Consider adding a plumbing-specific design fee entry to Professional_Design_Fees.csv.** Currently only DF-03 (Mechanical) exists; a DF-06 (Plumbing) entry would enable cross-check against fee-based pricing.
