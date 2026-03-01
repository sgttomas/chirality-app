# QA Report — EST_DEL-016-01_2026-02-27_0133

## RUN_STATUS: WARNINGS

**Rationale:** Totals are meaningful and the estimate provides a reasonable parametric/allowance basis for budgeting. However, material TBDs and assumptions remain, particularly: (a) equipment pricing is LOW confidence with a wide range, (b) multiple design parameters are TBD, (c) potential supply+install overlap between EQ-01 allowance and separate installation labour lines, and (d) 1 line item (anti-collision) is fully TBD.

---

## 1. Schema Validity

### Items.csv

| Check | Result |
|-------|--------|
| File exists and parseable | PASS |
| Required columns present (ItemID, DeliverableID, Description, Qty, Unit, PricingMode, SourceDoc, SourceSection, Notes) | PASS |
| PricingMode values valid (UNIT_RATE or LUMP_SUM) | PASS |
| All rows trace to a source document and section | PASS |
| Row count | 16 items |

### Detail.csv

| Check | Result |
|-------|--------|
| File exists and parseable | PASS |
| Required columns present (LineID, ItemID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes) | PASS |
| Method values valid (QUOTE, RATE_TABLE, HISTORICAL, ALLOWANCE, PARAMETRIC) | PASS — 2 ALLOWANCE, 19 PARAMETRIC, 1 TBD (DL-021) |
| Allowance/parametric convention respected (Qty=1, Unit=LS, UnitRate=Amount for lump-sum) | PASS (where applicable) |
| Row count | 22 lines |

---

## 2. Quantity Takeoff Coverage

| Metric | Value |
|--------|-------|
| Deliverables in scope | 1 (DEL-016-01) |
| Documents read | 5 of 5 |
| Missing documents | 0 |
| Items extracted | 16 |
| Items per source document | Datasheet: 4, Specification: 2, Procedure: 8, Guidance: 0 (referenced via Specification/Procedure), _CONTEXT: 0 (identity only) |

**Assessment:** Quantity takeoff is comprehensive. All major cost categories identified from the four documents are represented: equipment procurement (2 crane units), installation labour (ironworker, labourer, electrician), commissioning activities (functional test, load test, AHJ inspection, owner demo), professional staff (6 roles from Level_of_Effort.csv), procurement management, documentation, and freight.

---

## 3. Pricing Coverage

| Metric | Value |
|--------|-------|
| Total detail lines | 22 |
| Priced lines (Amount is numeric) | 21 (95.5%) |
| TBD lines | 1 (4.5%) |
| TBD line items | DL-021: Anti-collision system (depends on runway configuration TBD) |

---

## 4. Provenance Completeness

| Metric | Value |
|--------|-------|
| Lines with non-TBD SourceRef | 22 of 22 (100%) |
| Lines with "location TBD" SourceRef | 1 (DL-021 — anti-collision system, correctly flagged) |

**Top missing-source offenders:** None. All lines have a SourceRef. DL-021 references "location TBD" which is correct given the item itself is TBD.

---

## 5. Basis-Consistency Checks

| Check | Result |
|-------|--------|
| BASIS_OF_ESTIMATE | PARAMETRIC |
| ALLOW_MIXED_METHODS | TRUE |
| Methods used | PARAMETRIC (19 lines), ALLOWANCE (2 lines — DL-001, DL-002), TBD (1 line — DL-021) |
| Basis consistency | PASS — ALLOW_MIXED_METHODS=TRUE permits ALLOWANCE fallback; FALLBACK_POLICY=ALLOW_PARAMETRIC permits parametric pricing |
| ALLOWANCE usage justified | YES — Equipment_Pricing.csv EQ-01 provides the only available crane pricing basis; no quotes or rate tables exist for the equipment |

---

## 6. Scope Coverage

| Check | Result |
|-------|--------|
| Deliverables included | DEL-016-01 (1 of 1 in scope) |
| Deliverables excluded | None |
| Items with TBD quantity | 1 (ITM-016-01-015: anti-collision system) |
| Known exclusions per Specification | Crane runway (PKG-011/DEL-002-07), electrical feeder (PKG-015/DEL-015-04), operator training (OPS-001), maintenance scheduling (MAINT-001) — all correctly out of scope |

---

## 7. Warnings Register

| ID | Severity | Description |
|----|----------|-------------|
| W-001 | HIGH | Equipment pricing (EQ-01) is LOW confidence with $120k–$280k range per unit. Total equipment cost could vary by $320,000. |
| W-002 | HIGH | Multiple TBD design parameters (crane span, hook height, duty class, standards) mean procurement spec is incomplete. |
| W-003 | MEDIUM | Construction labour hours are parametric assumptions, not based on specific crane model or site conditions. |
| W-004 | MEDIUM | Anti-collision system (DL-021) is fully TBD — depends on runway configuration decision. |
| W-005 | MEDIUM | Potential supply+install overlap: EQ-01 is "supply + install" but separate installation labour lines are also priced. See Decision DEC-002. |
| W-006 | LOW | No contingency, management reserve, or escalation applied. Typically applied at package/project rollup level. |

---

## 8. What to Fix for a Cleaner Rerun

1. **Obtain crane supplier quotes.** Replace the ALLOWANCE basis (EQ-01) with actual QUOTE pricing from qualified suppliers. This will resolve W-001 and significantly improve estimate confidence.

2. **Resolve TBD design parameters.** Confirm crane span, hook height, duty class, applicable standards, and voltage/amperage. This feeds into both a more accurate specification for quotation and better labour hour estimates.

3. **Confirm runway configuration.** Determine whether cranes will operate on shared or independent runways. This resolves the anti-collision TBD (W-004) and refines structural cost allocation.

4. **Clarify supply+install overlap.** When quotes are obtained, confirm whether the crane supplier's price includes installation labour or only equipment supply. Adjust DL-003 through DL-007 accordingly to eliminate any double-counting risk (W-005).

5. **Add contingency at rollup level.** When this estimate is rolled up into the PKG-016 or project-level estimate, apply an appropriate contingency percentage reflecting the LOW confidence on equipment pricing.

---

## Operator Acceptance Checklist (S8)

| Check | Status |
|-------|--------|
| RUN_STATUS is OK or WARNINGS with bounded gaps | PASS — WARNINGS with clearly identified and bounded gaps |
| Items.csv reviewed for completeness | PASS — 16 items covering all major cost categories |
| Basis-consistency checks pass | PASS — mixed methods authorized and justified |
| Provenance completeness reported | PASS — 100% SourceRef coverage |
| Scope coverage explicit | PASS — 1/1 deliverable, exclusions documented |
| No writes outside _Estimates/ | PASS |
