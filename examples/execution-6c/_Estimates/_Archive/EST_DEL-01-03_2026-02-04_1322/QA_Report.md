# QA Report

## Snapshot Identification

| Property | Value |
|----------|-------|
| **Snapshot ID** | EST_DEL-01-03_2026-02-04_1322 |
| **Deliverable** | DEL-01-03 BondingAndInsuranceEvidence |
| **QA Date** | 2026-02-04 |
| **Run Status** | WARNINGS |

---

## QA Checks

### Check 1: Currency Consistency

| Property | Result |
|----------|--------|
| **Check** | All line items in same currency |
| **Status** | PASS |
| **Details** | All 11 line items in CAD |

---

### Check 2: Qty/Unit/UnitRate Completeness

| Property | Result |
|----------|--------|
| **Check** | Every line has non-empty Qty, Unit, UnitRate |
| **Status** | PASS |
| **Details** | All 11 line items have Qty, Unit, UnitRate populated |

**Line Item Verification:**

| LineID | Qty | Unit | UnitRate | Status |
|--------|-----|------|----------|--------|
| L-001 | 4 | HR | 150 | OK |
| L-002 | 8 | HR | 150 | OK |
| L-003 | 4 | HR | 150 | OK |
| L-004 | 4 | HR | 150 | OK |
| L-005 | 4 | HR | 150 | OK |
| L-006 | 4 | HR | 150 | OK |
| L-007 | 4 | HR | 175 | OK |
| L-008 | 1 | LS | 500 | OK |
| L-009 | 1 | LS | 300 | OK |
| L-010 | 2 | HR | 100 | OK |
| L-100 | 1 | LS | 870 | OK |

---

### Check 3: Arithmetic Reconciliation

| Property | Result |
|----------|--------|
| **Check** | Detail.csv sums match Summary.md totals |
| **Status** | PASS |
| **Details** | See reconciliation below |

**Reconciliation:**

| Calculation | Amount (CAD) |
|-------------|--------------|
| Sum of L-001 through L-010 (Base) | 5,900 |
| Summary.md Base Subtotal | 5,900 |
| **Base Match** | PASS |
| L-100 (Contingency) | 870 |
| Summary.md Contingency | 870 |
| **Contingency Match** | PASS |
| Total (Base + Contingency) | 6,770 |
| Summary.md Total | 6,770 |
| **Total Match** | PASS |

---

### Check 4: Coverage Check

| Property | Result |
|----------|--------|
| **Check** | All deliverables in scope have associated cost lines |
| **Status** | PASS |
| **Details** | DEL-01-03 is the only deliverable in scope; all line items map to DEL-01-03 |

---

### Check 5: Double Count Heuristics

| Property | Result |
|----------|--------|
| **Check** | No duplicate scope priced in multiple places |
| **Status** | PASS |
| **Details** | Each procedure step mapped to unique line item(s); no overlapping scope identified |

---

### Check 6: SourceRef Completeness

| Property | Result |
|----------|--------|
| **Check** | Every line has SourceRef (assumption ID, decision ID, or file reference) |
| **Status** | PASS |
| **Details** | All 11 line items have SourceRef mapped to Assumptions_Log or Decision_Log entries |

---

### Check 7: CBS Assignment

| Property | Result |
|----------|--------|
| **Check** | Every line has valid CBS code |
| **Status** | PASS |
| **Details** | CBS codes used: PM (8 lines), E (1 line), P (2 lines), CONT (1 line) - all valid |

---

### Check 8: Mapping Ambiguities

| Property | Result |
|----------|--------|
| **Check** | WBS-to-CBS mapping issues identified and documented |
| **Status** | PASS (no ambiguities) |
| **Details** | DEL-01-03 clearly maps to PM (Proposal Management) based on _CONTEXT.md discipline and responsible party fields |

---

## Completeness Metrics

| Metric | Value |
|--------|-------|
| **% of lines priced by QUOTE** | 0% (0/11) |
| **% of lines priced by RATE_TABLE** | 0% (0/11) |
| **% of lines priced by ALLOWANCE** | 100% (11/11) |
| **% of deliverables with explicit quantities** | 0% (no material quantities; effort-based) |

---

## Unknowns List (Top Assumptions/Allowances by Value)

| Rank | Item | Value (CAD) | Assumption ID | Confidence |
|------|------|-------------|---------------|------------|
| 1 | Surety Coordination (8 hrs) | 1,200 | A-004 | MED |
| 2 | Contingency | 870 | D-004 | MED |
| 3 | Estimator Support (4 hrs) | 700 | A-009 | MED |
| 4 | RFP Requirements Extraction (4 hrs) | 600 | A-003 | MED |
| 5 | Bond Cost Statement (4 hrs) | 600 | A-005 | MED |
| 6 | Insurance Summary (4 hrs) | 600 | A-006 | LOW |
| 7 | Package Assembly (4 hrs) | 600 | A-007 | MED |
| 8 | Final QC (4 hrs) | 600 | A-008 | MED |
| 9 | Surety Processing Fee | 500 | A-010 | LOW |
| 10 | Insurance Broker Fee | 300 | A-011 | LOW |

---

## Known Issues

| Issue ID | Description | Severity | Resolution Path |
|----------|-------------|----------|-----------------|
| QA-001 | RFP Section 5.3.1 requirements not extracted (TBD items in deliverable documents) | WARNING | Extract RFP requirements when PDF accessible; update estimate |
| QA-002 | All line items are allowances (no quotes or rate tables) | WARNING | Provide rate tables or obtain quotes for improved accuracy |
| QA-003 | Insurance scope conditional ("as required") | INFO | Clarify RFP requirements; may reduce or eliminate L-004, L-009 |
| QA-004 | Surety relationship status unknown | INFO | Confirm with Proposal Manager; may affect L-002 effort |

---

## Run Status Determination

| Criteria | Status |
|----------|--------|
| Critical failures | None |
| Material assumptions/ambiguities | Yes (TBD items, 100% allowance-based) |
| Arithmetic reconciliation | PASS |
| Completeness | PASS |

**RUN_STATUS: WARNINGS**

Estimate is valid and complete but has material assumptions due to TBD items in source documents and 100% allowance-based pricing.

---

## Recommendations for Next Run

1. **Extract RFP Section 5.3.1** - Resolve TBD items in deliverable documents; update estimate with actual requirements
2. **Provide Rate Tables** - Add professional services rate table to `_RateTables/` for improved pricing accuracy
3. **Confirm Surety Status** - Verify surety relationship status (existing vs. new) to refine coordination effort estimate
4. **Clarify Insurance Scope** - Determine if insurance approach summary is required; adjust estimate accordingly
