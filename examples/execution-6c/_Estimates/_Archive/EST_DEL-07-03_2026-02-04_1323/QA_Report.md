# QA Report

## Snapshot Identification

| Property | Value |
|----------|-------|
| **Snapshot ID** | EST_DEL-07-03_2026-02-04_1323 |
| **Deliverable** | DEL-07-03 Appendix I - Subtrade and Consultant List |
| **QA Date** | 2026-02-04 |
| **RUN_STATUS** | WARNINGS |

---

## QA Checks

### Check 1: Currency Consistency

| Check | Result |
|-------|--------|
| **Description** | All line items use consistent currency |
| **Status** | PASS |
| **Evidence** | All 13 line items in Detail.csv have Currency = CAD |
| **Notes** | No currency mixing detected |

---

### Check 2: Qty/Unit/UnitRate Presence (Hard Check)

| Check | Result |
|-------|--------|
| **Description** | Every line item has non-empty Qty, Unit, and UnitRate fields |
| **Status** | PASS |
| **Evidence** | All 13 line items have: Qty = 1, Unit = LS, UnitRate = Amount |
| **Notes** | Allowance convention applied correctly (Qty=1, Unit=LS, UnitRate=Amount) |

---

### Check 3: Arithmetic Reconciliation

| Check | Result |
|-------|--------|
| **Description** | Detail.csv sum matches Summary.md base estimate |
| **Status** | PASS |
| **Evidence** | Sum of Detail.csv Amount column = CAD 4,450; Summary.md Base Estimate = CAD 4,450 |
| **Variance** | CAD 0 |
| **Notes** | Perfect reconciliation |

---

### Check 4: Coverage Check

| Check | Result |
|-------|--------|
| **Description** | All deliverable scope areas have associated cost lines |
| **Status** | PASS |
| **Evidence** | All 10 Procedure steps mapped to at least one line item |
| **Coverage Mapping** | |

| Procedure Step | Line Items |
|----------------|------------|
| Step 1: Template Acquisition | L-001 |
| Step 1b: Commitment Policy | Included in L-001 |
| Step 2: Scope Checklist | L-002 |
| Step 3: Team Identification | L-003, L-004, L-005, L-006 |
| Step 4: Cost Breakdown Cross-Check | L-007 |
| Step 5: Addenda Compliance | L-008 |
| Step 6: Cross-Deliverable Check | L-009 |
| Step 7: Formatting | L-010 |
| Step 8: Quality Review | L-011 |
| Step 9: PDF Integration | L-012 |
| Step 10: Compliance Matrix | L-013 |

---

### Check 5: Double Count Heuristics

| Check | Result |
|-------|--------|
| **Description** | Check for same scope priced in multiple places |
| **Status** | PASS |
| **Evidence** | Each line item maps to distinct Procedure step; no overlap detected |
| **Notes** | Line items are mutually exclusive by activity |

---

### Check 6: Traceability

| Check | Result |
|-------|--------|
| **Description** | Every line item has SourceRef populated |
| **Status** | PASS |
| **Evidence** | All 13 line items have SourceRef pointing to Assumption IDs (A-006 through A-018) |
| **Notes** | All sources traceable to Assumptions_Log.md |

---

### Check 7: Method Distribution

| Check | Result |
|-------|--------|
| **Description** | Document pricing method distribution |
| **Status** | WARNING |
| **Evidence** | 100% ALLOWANCE (13/13 line items) |
| **Notes** | No quotes or rate tables available; all pricing is assumption-based |

---

### Check 8: Confidence Distribution

| Check | Result |
|-------|--------|
| **Description** | Document confidence level distribution |
| **Status** | WARNING |
| **Evidence** | 13 line items: 13 LOW confidence (100%) |
| **Notes** | Low confidence due to lack of rate tables and historical data |

---

## Completeness Metrics

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| % Lines with Qty/Unit/UnitRate | 100% | 100% | PASS |
| % Lines priced by QUOTE | 0% | - | INFO |
| % Lines priced by RATE_TABLE | 0% | - | INFO |
| % Lines priced by ALLOWANCE | 100% | <50% | WARNING |
| % Lines with SourceRef | 100% | 100% | PASS |
| % Lines with LOW confidence | 100% | <30% | WARNING |
| Deliverable coverage | 100% | 100% | PASS |
| Arithmetic reconciliation variance | 0% | 0% | PASS |

---

## Mapping Ambiguities

| Ambiguity ID | Description | Resolution |
|--------------|-------------|------------|
| MA-001 | CBS classification could be "E" (Engineering) or "PM" (Project Management) for proposal preparation | Assigned to "E" per D-007; PM also acceptable |

---

## Unknowns List (Top Assumptions by Value)

| Rank | Assumption ID | Description | Impact (CAD) |
|------|---------------|-------------|--------------|
| 1 | A-001 | PM labor rate CAD 150/hr | 2,850 |
| 2 | A-002 | Admin labor rate CAD 85/hr | 1,445 |
| 3 | A-003 | Total effort 36 hours | 4,450 (base) |
| 4 | A-008 | Design consultant identification effort | 600 |
| 5 | A-009 | Construction subtrade identification effort | 510 |

---

## Known Issues

| Issue ID | Description | Severity | Mitigation |
|----------|-------------|----------|------------|
| KI-001 | No rate tables available | Medium | Provide rates to `_RateTables/` |
| KI-002 | No historical data for calibration | Medium | Track actuals on this proposal |
| KI-003 | 100% allowance-based pricing | Medium | Accept 15% contingency coverage |

---

## RUN_STATUS Determination

| Criterion | Status |
|-----------|--------|
| Critical failures (missing required fields) | None |
| Material assumptions/ambiguities | Yes (100% allowance pricing) |
| Inputs missing such that totals not meaningful | No (totals are meaningful) |

**RUN_STATUS: WARNINGS**

Rationale: Estimate is complete and arithmetically correct, but 100% reliance on allowances with LOW confidence creates material uncertainty. Totals are meaningful for budgeting purposes but should be refined with actual rate tables when available.

---

## Recommendations

1. **Priority 1:** Provide labor rate tables to `_Estimates/_RateTables/` for future estimates
2. **Priority 2:** Track actual hours on DEL-07-03 to calibrate future estimates
3. **Priority 3:** Confirm team size (number of firms to list) to refine effort estimates
4. **Priority 4:** If proposal preparation cost is material, obtain quotes from proposal services vendors
