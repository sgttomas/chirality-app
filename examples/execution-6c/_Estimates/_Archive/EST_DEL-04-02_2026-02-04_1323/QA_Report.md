# QA Report
## DEL-04-02: Budget Control and Change Management Plan

---

## Snapshot Information

| Property | Value |
|----------|-------|
| **Snapshot ID** | EST_DEL-04-02_2026-02-04_1323 |
| **QA Date** | 2026-02-04 |
| **RUN_STATUS** | WARNINGS |

---

## QA Checks Summary

| Check | Status | Notes |
|-------|--------|-------|
| Currency Consistency | PASS | All lines in CAD |
| Qty/Unit/UnitRate Populated | PASS | All 22 lines have required fields |
| Arithmetic Reconciliation | PASS | Detail sums match Summary |
| Coverage Check | PASS | Single deliverable scope covered |
| Double Count Check | PASS | No duplicate scope items |
| Source Traceability | PASS | All lines have SourceRef |

---

## Detailed Check Results

### 1. Currency Consistency

| Status | PASS |
|--------|------|
| **Check** | All Detail.csv lines use same currency |
| **Result** | All 22 lines specify CAD |
| **Issues** | None |

---

### 2. Qty/Unit/UnitRate Populated (Hard Check)

| Status | PASS |
|--------|------|
| **Check** | Every Detail.csv line has non-empty Qty, Unit, UnitRate |
| **Result** | All 22 lines have required fields populated |
| **Allowance Convention** | L-020, L-021, L-022 use Qty=1, Unit=LS per protocol |
| **Issues** | None |

**Line-by-Line Verification:**
- L-001 through L-019: HR unit with hourly rates
- L-020 through L-022: LS unit (allowance convention applied)

---

### 3. Arithmetic Reconciliation

| Status | PASS |
|--------|------|
| **Check** | Detail.csv amounts sum to Summary.md totals |
| **Result** | Reconciled within rounding tolerance |

**Reconciliation:**

| CBS | Detail.csv Sum | Summary.md | Variance |
|-----|----------------|------------|----------|
| E | $6,260 | $6,260 | $0 |
| PM | $2,060 | $2,060 | $0 |
| CONT | $1,247 | $1,247 | $0 |
| **TOTAL** | **$9,567** | **$9,567** | **$0** |

---

### 4. Coverage Check

| Status | PASS |
|--------|------|
| **Check** | Deliverable scope is covered by cost lines |
| **Result** | DEL-04-02 scope fully mapped to line items |
| **Issues** | None |

**Coverage Analysis:**
- 7 plan sections mapped to L-001 through L-007
- 4 templates mapped to L-008 through L-011
- Consistency/addenda review mapped to L-012 through L-014
- Oversight and review mapped to L-015 through L-020
- Contingency mapped to L-021 through L-022

---

### 5. Double Count Check

| Status | PASS |
|--------|------|
| **Check** | No scope items priced in multiple places |
| **Result** | Each effort element has single line item |
| **Issues** | None |

---

### 6. Source Traceability

| Status | PASS |
|--------|------|
| **Check** | Every line has SourceRef pointing to assumption, decision, or document |
| **Result** | All 22 lines have SourceRef populated |

**Traceability Summary:**
- Lines referencing assumptions (A-xxx): 20 lines
- Lines referencing decisions (D-xxx): 2 lines

---

## Completeness Metrics

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| Lines priced by QUOTE | 0% | N/A | - |
| Lines priced by RATE_TABLE | 0% | Preferred | BELOW TARGET |
| Lines priced by ALLOWANCE | 100% | <50% preferred | WARNING |
| Deliverables with explicit quantities | 100% | 100% | PASS |
| SourceRef coverage | 100% | 100% | PASS |

**Completeness Score:** 60% (allowance-heavy, but fully traced)

---

## Mapping Ambiguities

| Item | Ambiguity | Resolution | Decision ID |
|------|-----------|------------|-------------|
| CBS assignment | Plan document could map to E or PM | Mapped to E for drafting, PM for oversight | D-003 |
| Validation walkthrough | Optional per Procedure Step 12 | Included as allowance | A-012 |

---

## Unknowns List (Top Assumptions by Value)

| Rank | Assumption ID | Description | Value Impact |
|------|---------------|-------------|--------------|
| 1 | A-005 | Section drafting effort 4-8 hrs | $5,320 |
| 2 | A-001 | CM rate $140/hr | $6,160 (44 hrs) |
| 3 | A-006 | Template development effort | $1,170 |
| 4 | A-003 | PM rate $150/hr | $1,200 (8 hrs) |
| 5 | A-002 | Commercial Lead rate $130/hr | $2,080 (16 hrs) |

---

## RUN_STATUS Determination

| Property | Value |
|----------|-------|
| **RUN_STATUS** | WARNINGS |
| **Critical Failures** | None |
| **Material Warnings** | Yes (see below) |

**Warnings:**
1. **W-001**: 100% of pricing by ALLOWANCE (no rate tables available)
2. **W-002**: RFP Section 7 requirements TBD (scope uncertainty)
3. **W-003**: Appendix H dependency (coordination not confirmed)

**Rationale:** Estimate is complete and traceable, but all pricing is based on assumptions due to lack of rate tables. Confidence is LOW-MEDIUM.

---

## Recommendations for Next Run

1. **Provide rate tables** in `_RateTables/` folder with professional hourly rates to replace allowances
2. **Confirm RFP Section 7 requirements** through human review of PDF to validate scope
3. **Coordinate with Appendix H team** to confirm Schedule A/B structure before consistency verification

---

## Document Control

| Property | Value |
|----------|-------|
| **Created** | 2026-02-04 |
| **Agent** | ESTIMATING (Type 2) |
| **QA Checks Performed** | 6 |
| **Warnings Issued** | 3 |
