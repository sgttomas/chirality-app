# QA Report — EST_DEL-021-04_2026-02-28_0802

**RUN_STATUS: OK**

---

## Schema Validity

### Items.csv

| Check | Result |
|---|---|
| File parseable | PASS |
| Required columns present (ItemID, DeliverableID, Description, Qty, Unit, PricingMode, SourceDoc, SourceSection, Notes) | PASS |
| All rows have DeliverableID = DEL-021-04 | PASS |
| PricingMode values valid (UNIT_RATE or LUMP_SUM) | PASS |
| Lump-sum convention (Qty=1, Unit=LS) | PASS — applied to ITEM-001 through ITEM-005 |
| SourceDoc values valid (Specification, Procedure) | PASS |
| No TBD quantities in Items.csv | PASS — all quantities determined from Level_of_Effort.csv or set to 1 for lump-sum |
| Total items | 13 |

### Detail.csv

| Check | Result |
|---|---|
| File parseable | PASS |
| Required columns present (LineID, ItemID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes) | PASS |
| ItemID references valid (each maps to Items.csv) | PASS |
| Method values valid (PARAMETRIC) | PASS |
| Allowance/parametric convention (Qty=1, Unit=LS, UnitRate=Amount for LS items) | PASS — applied to L-001 through L-004; L-005 resolved to Qty=1, Unit=LS, UnitRate=0, Amount=0 |
| Currency consistent | PASS — all CAD |
| TBD amounts flagged | PASS — 0 lines have Amount=TBD (L-005 resolved to $0 in this snapshot) |
| Amount arithmetic check | PASS — all lines: Amount = Qty x UnitRate |
| Total lines | 13 |

---

## TBD Resolution

| LineID | ItemID | Description | Prior Status | Current Status | Resolution |
|---|---|---|---|---|---|
| L-005 | ITEM-005 | Contract administration procedures document preparation | TBD | Resolved ($0) | Labour effort captured in ITEM-006 through ITEM-013; no separate non-labour cost identified. Set to $0 per DEC-R01. |

**TBDs remaining: 0**

---

## Quantity Takeoff Coverage

| Deliverable | Items Extracted | Documents Read | Documents Missing |
|---|---|---|---|
| DEL-021-04 | 13 | 4 of 4 (Datasheet, Specification, Guidance, Procedure) | None |

**Coverage assessment:** All four production documents were read. Priceable items were extracted from:
- Procedure: 12 items — 4 non-labour items from specific procedural steps (CCDC form, legal review, execution meeting, distribution) + 8 labour lines by role aligned to procedural steps
- Specification: 1 item (REQ-021-04-23 contract administration procedures)
- Datasheet: Reviewed for contract package composition; individual components (bonds, insurance, forms) are priced under their respective deliverables (DEL-021-02, DEL-021-03); no separate priceable items extracted to avoid double-counting
- Guidance: Reviewed for trade-offs and context; informed assumptions but no discrete priceable items extracted

---

## Pricing Coverage

| Metric | Value |
|---|---|
| Total items | 13 |
| Items priced | 13 |
| Items TBD | 0 |
| Pricing coverage | 100% |

---

## Provenance Completeness

| Metric | Value |
|---|---|
| Lines with SourceRef | 13 of 13 (100%) |
| Lines with "location TBD" | 0 of 13 (0%) |

All 8 labour lines have traceable SourceRef pointing to specific rows in Professional_Staff_Rates.csv and Level_of_Effort.csv. The 4 non-labour priced lines (L-001 through L-004) reference parametric estimates documented in the Assumptions_Log.md. L-005 references Decision_Log DEC-R01.

---

## Basis-Consistency Checks

| Check | Result |
|---|---|
| BASIS_OF_ESTIMATE | PARAMETRIC |
| Method values in Detail.csv | All PARAMETRIC |
| ALLOW_MIXED_METHODS | TRUE (allowed but not needed; all lines are PARAMETRIC) |
| FALLBACK_POLICY | ALLOW_PARAMETRIC — applied; non-labour items priced as parametric allowances |
| Basis consistency | PASS — no method mix violations |

---

## Scope Coverage

| Metric | Value |
|---|---|
| Deliverables in scope | 1 (DEL-021-04) |
| Deliverables estimated | 1 |
| SOW items mapped | SOW-0104 (CCDC 14-2013 contract execution) |
| SOW items covered by line items | SOW-0104 maps to the full set of contract execution activities (ITEM-001 through ITEM-013) |
| Excluded from scope | Bonds (DEL-021-02); insurance premiums (DEL-021-03); construction work itself (PKG-001 through PKG-018); warranty period administration (DEL-021-05); foundation price negotiation deferred costs |

---

## Warnings Summary

| # | Severity | Description |
|---|---|---|
| W-001 | MODERATE | Legal counsel review fee ($5,000) is a parametric allowance — no legal rate data in price sources; actual cost depends on counsel selection and contract complexity |
| W-002 | LOW | CCDC 14-2013 form purchase ($500) is a parametric estimate — actual cost depends on format and vendor |
| W-003 | MODERATE | Foundation price negotiation (Procedure Step 6) is deferred and not costed — additional PM, legal, and estimating effort will be needed when geotechnical report is received |
| W-004 | LOW | Supplementary Conditions negotiation effort not separately costed — if modifications to CCDC 14-2013 are needed, additional legal and PM time may be required |
| W-005 | LOW | Execution meeting and distribution costs are nominal parametric allowances ($500 + $300) — may understate actual costs if travel or extensive distribution is required |

---

## Change from Prior Snapshot

| Metric | Prior (2026-02-27_0547) | Current (2026-02-28_0802) |
|---|---|---|
| RUN_STATUS | WARNINGS | OK |
| TBD count | 1 | 0 |
| Pricing coverage | 92.3% | 100% |
| Provenance completeness | 92.3% | 100% |
| Total amount | $14,260 | $14,260 |
| Resolution | -- | L-005 TBD resolved to $0 (DEC-R01) |

---

## What to Fix for a Cleaner Rerun

1. **Add legal counsel rate data** — Provide external counsel hourly rate and estimated review hours to replace the $5,000 parametric allowance with a calculated amount.
2. **Confirm CCDC 14-2013 form cost** — Obtain actual purchase price from CCDC or legal counsel to replace the $500 parametric estimate.
3. **Estimate foundation negotiation costs** — Once geotechnical report is available, add a separate cost item for the deferred Step 6 negotiation effort.
4. **Clarify Supplementary Conditions scope** — If CCDC 14-2013 modifications are anticipated, add cost for additional legal and PM time.
5. **Refine meeting/distribution logistics** — Once execution format (physical vs. electronic per Guidance D-001) and distribution list are confirmed, update logistics and distribution costs.
