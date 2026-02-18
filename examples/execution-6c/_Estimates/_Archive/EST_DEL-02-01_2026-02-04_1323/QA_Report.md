# QA Report

## Snapshot Identification

| Property | Value |
|----------|-------|
| **Snapshot ID** | EST_DEL-02-01_2026-02-04_1323 |
| **Deliverable** | DEL-02-01 ConceptDesignPackage |
| **RUN_STATUS** | WARNINGS |

---

## QA Checks Summary

| Check | Status | Notes |
|-------|--------|-------|
| Currency Consistency | PASS | All amounts in CAD |
| Qty/Unit/UnitRate Present | PASS | All 16 lines have required fields |
| Arithmetic Reconciliation | PASS | Detail sum ($43,700) = Summary total |
| Coverage Check | PASS | Single deliverable fully covered |
| Double Count Check | PASS | No duplicate scope identified |
| Contingency Explicit | PASS | L-016 contingency line present |
| Traceability | PASS | All lines have SourceRef |

---

## Detailed QA Checks

### 1. Currency Consistency

| Check | Result |
|-------|--------|
| Single currency used | YES (CAD) |
| Currency column populated | YES (all 16 lines) |
| Mixed currency | NO |

**Status:** PASS

---

### 2. Qty/Unit/UnitRate Present (Hard Check)

| LineID | Qty | Unit | UnitRate | Amount | Check |
|--------|-----|------|----------|--------|-------|
| L-001 | 1 | LS | 4500 | 4500 | PASS |
| L-002 | 1 | LS | 8000 | 8000 | PASS |
| L-003 | 1 | LS | 3500 | 3500 | PASS |
| L-004 | 1 | LS | 2500 | 2500 | PASS |
| L-005 | 1 | LS | 3000 | 3000 | PASS |
| L-006 | 1 | LS | 2500 | 2500 | PASS |
| L-007 | 1 | LS | 1500 | 1500 | PASS |
| L-008 | 1 | LS | 2000 | 2000 | PASS |
| L-009 | 1 | LS | 1500 | 1500 | PASS |
| L-010 | 1 | LS | 2000 | 2000 | PASS |
| L-011 | 1 | LS | 1500 | 1500 | PASS |
| L-012 | 1 | LS | 1500 | 1500 | PASS |
| L-013 | 1 | LS | 1000 | 1000 | PASS |
| L-014 | 1 | LS | 500 | 500 | PASS |
| L-015 | 1 | LS | 2000 | 2000 | PASS |
| L-016 | 1 | LS | 5700 | 5700 | PASS |

**Status:** PASS - All lines have Qty/Unit/UnitRate populated per SPEC requirement

---

### 3. Arithmetic Reconciliation

| Calculation | Result |
|-------------|--------|
| Detail.csv line sum | $43,700 |
| Summary.md total | $43,700 |
| Variance | $0 |

**Status:** PASS

---

### 4. Coverage Check

| WBS Element | Line Count | Amount | Coverage |
|-------------|------------|--------|----------|
| PKG-04/DEL-02-01 | 16 | $43,700 | 100% |

**Status:** PASS - Deliverable fully covered

---

### 5. Double Count Heuristics

| Check | Result |
|-------|--------|
| Duplicate descriptions | None found |
| Overlapping scope | None identified |
| Same CBS/WBS duplication | None (unique line items) |

**Status:** PASS

---

### 6. Traceability Check

| LineID | Method | SourceRef | Status |
|--------|--------|-----------|--------|
| L-001 | ALLOWANCE | A-007 | PASS |
| L-002 | ALLOWANCE | A-008 | PASS |
| L-003 | ALLOWANCE | A-009 | PASS |
| L-004 | ALLOWANCE | A-010 | PASS |
| L-005 | ALLOWANCE | A-011 | PASS |
| L-006 | ALLOWANCE | A-012 | PASS |
| L-007 | ALLOWANCE | A-013 | PASS |
| L-008 | ALLOWANCE | A-014 | PASS |
| L-009 | ALLOWANCE | A-015 | PASS |
| L-010 | ALLOWANCE | A-016 | PASS |
| L-011 | ALLOWANCE | A-017 | PASS |
| L-012 | ALLOWANCE | A-018 | PASS |
| L-013 | ALLOWANCE | A-019 | PASS |
| L-014 | ALLOWANCE | A-020 | PASS |
| L-015 | ALLOWANCE | A-021 | PASS |
| L-016 | ALLOWANCE | D-004 | PASS |

**Status:** PASS - All lines have SourceRef to assumption or decision

---

## Completeness Metrics

| Metric | Value |
|--------|-------|
| % Lines Priced by QUOTE | 0% |
| % Lines Priced by RATE_TABLE | 0% |
| % Lines Priced by ALLOWANCE | 100% |
| % Deliverables with Explicit Quantities | 100% |

---

## Mapping Ambiguities

| Item | Ambiguity | Resolution | Decision ID |
|------|-----------|------------|-------------|
| CBS Assignment | Design deliverable could map to E only or E + PM | Mapped primarily to E with PM for management | D-003 |

---

## Unknowns List (Top Assumptions by Value)

| Rank | Assumption ID | Description | Value Impact |
|------|---------------|-------------|--------------|
| 1 | A-008 | Floor plans allowance | $8,000 |
| 2 | D-004 | Contingency rate (15%) | $5,700 |
| 3 | A-007 | Site concept plan allowance | $4,500 |
| 4 | A-009 | Massing study allowance | $3,500 |
| 5 | A-011 | Elevations allowance | $3,000 |

---

## Issues and Warnings

### WARNINGS

| Issue ID | Description | Impact | Resolution |
|----------|-------------|--------|------------|
| W-001 | 100% allowance-based pricing | Confidence affected; actual costs may vary | Provide rate tables for next iteration |
| W-002 | Appendix B location TBD (Blocking Conflict C-002) | Program fit verification incomplete | Obtain Appendix B immediately |
| W-003 | Town setbacks TBD (Blocking Conflict A-003) | Site concept may require rework | Obtain Town bylaws |
| W-004 | Code edition ASSUMPTION | Code compliance may need revision | Confirm code edition |

### BLOCKING ISSUES

None - estimate can be published with WARNINGS status.

---

## RUN_STATUS Determination

| Criteria | Status |
|----------|--------|
| Critical failures | NONE |
| Material assumptions | YES (100% allowance-based) |
| Known TBDs in inputs | YES (Appendix B, setbacks, code) |
| Totals meaningful | YES |

**RUN_STATUS: WARNINGS**

Rationale: Estimate is complete and arithmetic is valid, but material assumptions exist due to 100% allowance-based pricing and multiple TBDs in source documents.

---

## Document Control

| Property | Value |
|----------|-------|
| **Created** | 2026-02-04 |
| **Author** | ESTIMATING Agent (Type 2) |

---

**END OF QA REPORT**
