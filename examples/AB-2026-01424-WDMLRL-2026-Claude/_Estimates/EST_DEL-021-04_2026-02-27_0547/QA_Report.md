# QA Report — EST_DEL-021-04_2026-02-27_0547

**RUN_STATUS: WARNINGS**

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
| Allowance/parametric convention (Qty=1, Unit=LS, UnitRate=Amount for LS items) | PASS — applied to L-001 through L-004; L-005 is TBD |
| Currency consistent | PASS — all CAD |
| TBD amounts flagged | PASS — 1 line (L-005) has Amount=TBD |
| Total lines | 13 |

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
| Items priced | 12 |
| Items TBD | 1 |
| Pricing coverage | 92.3% |

### TBD Items (top missing-source offenders)

| LineID | ItemID | Description | Reason |
|---|---|---|---|
| L-005 | ITEM-005 | Contract administration procedures document preparation | Labour effort already captured in role-based lines (ITEM-006 through ITEM-013); no external facilitation costs identified in price sources. Set TBD pending confirmation of whether any external costs apply. |

---

## Provenance Completeness

| Metric | Value |
|---|---|
| Lines with SourceRef | 12 of 13 (92.3%) |
| Lines with "location TBD" | 1 of 13 (7.7%) |

All 8 labour lines have traceable SourceRef pointing to specific rows in Professional_Staff_Rates.csv and Level_of_Effort.csv. The 4 non-labour priced lines (L-001 through L-004) reference parametric estimates documented in the Assumptions_Log.md. One line (L-005) has "location TBD".

---

## Basis-Consistency Checks

| Check | Result |
|---|---|
| BASIS_OF_ESTIMATE | PARAMETRIC |
| Method values in Detail.csv | All PARAMETRIC |
| ALLOW_MIXED_METHODS | TRUE (allowed but not needed; all lines are PARAMETRIC) |
| FALLBACK_POLICY | ALLOW_PARAMETRIC — applied; non-labour items priced as parametric allowances; 1 line remains TBD |
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
| W-003 | LOW | ITEM-005 (contract admin procedures) is TBD — labour already captured in role-based hours; any external facilitation cost is unpriced |
| W-004 | MODERATE | Foundation price negotiation (Procedure Step 6) is deferred and not costed — additional PM, legal, and estimating effort will be needed when geotechnical report is received |
| W-005 | LOW | Supplementary Conditions negotiation effort not separately costed — if modifications to CCDC 14-2013 are needed, additional legal and PM time may be required |
| W-006 | LOW | Execution meeting and distribution costs are nominal parametric allowances ($500 + $300) — may understate actual costs if travel or extensive distribution is required |

---

## What to Fix for a Cleaner Rerun

1. **Add legal counsel rate data** — Provide external counsel hourly rate and estimated review hours to replace the $5,000 parametric allowance with a calculated amount.
2. **Confirm CCDC 14-2013 form cost** — Obtain actual purchase price from CCDC or legal counsel to replace the $500 parametric estimate.
3. **Estimate foundation negotiation costs** — Once geotechnical report is available, add a separate cost item for the deferred Step 6 negotiation effort.
4. **Clarify Supplementary Conditions scope** — If CCDC 14-2013 modifications are anticipated, add cost for additional legal and PM time.
5. **Confirm contract administration procedures approach** — Determine whether external facilitation or consulting support is needed (resolves ITEM-005 TBD).
6. **Refine meeting/distribution logistics** — Once execution format (physical vs. electronic per Guidance D-001) and distribution list are confirmed, update logistics and distribution costs.
