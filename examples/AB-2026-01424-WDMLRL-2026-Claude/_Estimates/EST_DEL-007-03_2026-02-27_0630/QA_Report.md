# QA Report — EST_DEL-007-03_2026-02-27_0630

## RUN_STATUS: OK

---

## 1. Schema Validity

### Items.csv

| Check | Result |
|---|---|
| File exists and is parseable | PASS |
| Required columns present (ItemID, DeliverableID, Description, Qty, Unit, PricingMode, SourceDoc, SourceSection, Notes) | PASS |
| All PricingMode values valid (UNIT_RATE or LUMP_SUM) | PASS — all 8 rows are UNIT_RATE |
| All rows trace to a source document and section | PASS — all rows reference Procedure.md with specific step/section |
| No TBD quantities | PASS — all Qty values are numeric |

### Detail.csv

| Check | Result |
|---|---|
| File exists and is parseable | PASS |
| Required columns present (LineID, ItemID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes) | PASS |
| All Method values valid (QUOTE, RATE_TABLE, HISTORICAL, ALLOWANCE, PARAMETRIC) | PASS — all 8 rows are PARAMETRIC |
| Allowance/parametric convention check | N/A — all items are UNIT_RATE (hr-based); convention applies to lump-sum parametric items |
| Amount = Qty x UnitRate for all rows | PASS |

### WBS_CBS_Matrix.csv

| Check | Result |
|---|---|
| File exists and is parseable | PASS |
| Required columns present | PASS |
| TOTAL row matches sum of detail rows | PASS — Management ($1,530) + Design ($9,450) = $10,980 |

---

## 2. Quantity Takeoff Coverage

| Metric | Value |
|---|---|
| Deliverables in scope | 1 (DEL-007-03) |
| Items extracted | 8 |
| Documents read | 5 (_CONTEXT.md, Datasheet.md, Specification.md, Guidance.md, Procedure.md) |
| Missing documents | 0 |
| Items with TBD quantities | 0 |

**Assessment:** Full coverage of the professional design services scope. Items map to the Procedure.md workflow steps and the Level_of_Effort.csv role allocations.

**Note:** The quantity takeoff is limited to professional services (labour hours). Physical deliverable attributes (plant species, quantities, areas) are TBD in the source documents and would require separate material/construction pricing if in scope.

---

## 3. Pricing Coverage

| Metric | Value |
|---|---|
| Total items in Items.csv | 8 |
| Items priced in Detail.csv | 8 |
| Items with TBD Amount | 0 |
| Pricing coverage | 100% (8/8) |

---

## 4. Provenance Completeness

| Metric | Value |
|---|---|
| Total rows in Detail.csv | 8 |
| Rows with non-TBD SourceRef | 8 |
| Rows with TBD SourceRef | 0 |
| Provenance completeness | 100% (8/8) |

**Top missing-source offenders:** None. All rows have complete source references pointing to Professional_Staff_Rates.csv (rate) and Level_of_Effort.csv (hours).

---

## 5. Basis-Consistency Checks

| Check | Result |
|---|---|
| BASIS_OF_ESTIMATE | PARAMETRIC |
| Method values in Detail.csv | All PARAMETRIC (8/8) |
| Mixed methods used | No |
| ALLOW_MIXED_METHODS setting | TRUE (but not exercised) |
| FALLBACK_POLICY | ALLOW_PARAMETRIC (not exercised — no fallback needed) |
| Basis consistency | PASS — 100% PARAMETRIC, consistent with BASIS_OF_ESTIMATE |

---

## 6. Scope Coverage

| Metric | Value |
|---|---|
| Scope requested | DEL-007-03 |
| Deliverables included | 1 (DEL-007-03 Planting & Restoration Plans) |
| Deliverables excluded | 0 |
| Packages covered | 1 (PKG-007) |
| Exclusion reasons | N/A |

---

## 7. Write Quarantine Check

| Check | Result |
|---|---|
| All output files written under _Estimates/ | PASS |
| No project truth files modified | PASS |
| No deliverable content files modified | PASS |
| No lifecycle files modified | PASS |
| No decomposition files modified | PASS |

---

## 8. Warnings and Recommendations

### Warnings

| ID | Severity | Description |
|---|---|---|
| W-001 | LOW | Landscape Architect sub-allocation (ASM-002) is an estimating assumption. The 70 hr total is sourced; the split across Steps 1-6 is not. |
| W-002 | LOW | Non-labour costs (materials, travel, printing, external assessments) are not included (ASM-004). If these are in scope, additional pricing sources are needed. |
| W-003 | INFO | CONF-007-03-001 (P.Eng. vs. RLA stamp) is unresolved. Potential minor cost impact if P.Eng. co-signature is required. |
| W-004 | INFO | Source documents contain numerous TBD attributes (plant species, soil data, hardiness zone). This does not affect the professional services estimate but signals the deliverable is at an early design stage. |

### What to Fix for a Cleaner Rerun

1. **Resolve LA sub-allocation:** If actual hour distribution across procedure steps is known, update Level_of_Effort.csv with per-step rows for DEL-007-03 R-19.
2. **Add non-labour costs:** If material, travel, or external assessment costs are in scope, provide pricing sources (quotes, historical data, or allowance tables).
3. **Add landscape design fee to Professional_Design_Fees.csv:** If a fee-based cross-check is desired, add a landscape discipline row (e.g., DF-06 Landscape).
4. **Resolve open conflicts:** CONF-007-03-001 (stamp type) and CONF-007-03-002 (restoration phasing vs. deadline) may affect scope/cost.

---

## 9. Operator Acceptance Checklist (S8)

| Criterion | Status |
|---|---|
| RUN_STATUS is OK or WARNINGS with bounded gaps | PASS — OK |
| Items.csv reviewed for completeness | PASS — 8 items covering all procedure steps and LOE roles |
| Basis-consistency checks pass | PASS — 100% PARAMETRIC |
| Provenance completeness reported and top gaps actionable | PASS — 100% provenance; no gaps |
| Scope coverage explicit | PASS — 1 deliverable, 1 package, 0 exclusions |
| No writes outside _Estimates/ | PASS |
