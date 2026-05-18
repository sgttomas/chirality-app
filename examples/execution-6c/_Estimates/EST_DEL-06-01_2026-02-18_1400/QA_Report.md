# QA Report — EST_DEL-06-01_2026-02-18_1400

## RUN_STATUS: OK

Totals are meaningful; no critical input gaps. All line items are priced from rate table + level-of-effort sources with full provenance.

---

## 1. Schema Validity (Detail.csv)

| Check | Result | Notes |
|-------|--------|-------|
| All required columns present | PASS | LineID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes |
| Method values valid | PASS | All rows: RATE_TABLE (allowed enum value) |
| Allowance/parametric convention | N/A | No ALLOWANCE or PARAMETRIC method rows |
| Amount = Qty x UnitRate | PASS | L-001: 16 x 140 = 2,240; L-002: 6 x 175 = 1,050 |
| Currency consistent | PASS | All rows: CAD |
| Rounding applied | PASS | DOLLAR rounding; all amounts are whole dollars |

## 2. Coverage

| Metric | Value |
|--------|-------|
| Deliverables in scope | 1 (DEL-06-01) |
| Deliverables with line items | 1 (DEL-06-01) |
| Deliverables blocked | 0 |
| Deliverables with $0 or TBD | 0 |
| Line items produced | 2 |
| Total estimated | $3,290 CAD |

## 3. Provenance Completeness

| Metric | Value |
|--------|-------|
| Total priced rows | 2 |
| Rows with non-TBD SourceRef | 2 |
| Provenance completeness | **100%** |
| Top missing-source offenders | None |

## 4. Basis Consistency

| Check | Result | Notes |
|-------|--------|-------|
| BASIS_OF_ESTIMATE declared | RATE_TABLE | Valid enum |
| Method values match basis | PASS | All 2 rows: Method=RATE_TABLE |
| ALLOW_MIXED_METHODS | FALSE | No mixed methods detected |
| FALLBACK_POLICY | STRICT | No fallback needed; all items priced from basis evidence |
| Fallback rows | 0 | None |

## 5. Dependency / Blocker Assessment

| Metric | Value |
|--------|-------|
| Dependencies.csv found | YES |
| Total ACTIVE dependency rows | 16 |
| Upstream EXECUTION dependencies | 8 (7 deliverables + 1 document) |
| Downstream EXECUTION dependencies | 2 |
| Estimation blockers from dependencies | 0 |

**Dependency note:** DEL-06-01 has 7 upstream deliverable interfaces (DEL-01-01, DEL-08-01, DEL-04-01, DEL-07-02, DEL-03-01, DEL-03-02, DEL-09-01) and 1 document prerequisite (Addendum 03). These are production dependencies (needed to write the deliverable) but do NOT block estimation of production cost. The hours required to produce DEL-06-01 are independent of upstream deliverable completion status.

## 6. Decomposition Alignment

| Check | Result | Notes |
|-------|--------|-------|
| DEL-06-01 found in decomposition | PASS | Decomposition Section 8: DEL-06-01_CommissioningTrainingCloseoutWarrantyNarrative |
| Package mapping correct | PASS | PKG-07 (Commissioning, Closeout & Warranty) |
| Scope item mapping | PASS | SOW-022 |
| Tier classification | T3 | Per BOE Section 4 |

## 7. Reasonableness Checks

| Check | Result | Notes |
|-------|--------|-------|
| Total hours (22) within expected range | PASS | BOE notes "Commissioning lead/PM hours" as cost drivers; 22 hours for consolidated narrative covering 5 sub-topics (commissioning, training, closeout, deficiencies, warranty) is reasonable for a proposal narrative |
| Cx Lead hours (16) vs PM hours (6) ratio | PASS | ~2.7:1 ratio; appropriate — Cx lead does specialist writing, PM provides coordination input |
| Comparison to BOE characterization | PASS | BOE Section 4 PKG-07 identifies Commissioning Lead and PM as primary roles; LOE matches |
| Cost per page equivalent | INFO | At ~$3,290 for a consolidated narrative, comparable to other T3 narratives (DEL-04-03 at $1,690 for simpler scope) |

## 8. What to Fix for a Cleaner Rerun

Nothing. This run is clean.

- All inputs resolved successfully
- All line items priced with full provenance
- Basis consistency maintained
- Decomposition alignment confirmed
- No TBD amounts

---

## Operator Acceptance Checklist

- [x] RUN_STATUS is OK
- [x] Basis-consistency checks pass (all RATE_TABLE, no mixed methods)
- [x] Provenance completeness reported (100%)
- [x] Scope coverage explicit (1/1 deliverable estimated, 0 blocked, 0 excluded)
- [x] No writes outside _Estimates/

---

**END OF QA REPORT**
