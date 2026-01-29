# QA Report

## Snapshot: EST_PKG19_DRAFT_2026-01-28_0015

This report documents quality assurance checks performed on the PKG-19 Control Systems estimate.

---

## Check Summary

| Check | Status | Notes |
|-------|--------|-------|
| Currency consistency | PASS | All line items in CAD |
| Qty/Unit/UnitRate present | PASS | All 30 line items have required fields |
| Arithmetic reconciliation | PASS | Detail sums match Summary |
| Coverage check | PASS | All 5 deliverables have associated costs |
| Double count check | PASS | No duplicates identified |
| Traceability | PASS | All lines have SourceRef (A-### or D-###) |

---

## Detailed Checks

### 1. Currency Consistency

| Check | Result |
|-------|--------|
| Single currency? | Yes — CAD |
| All amounts in CAD? | Yes |
| Conversion required? | No |

**Status:** PASS

---

### 2. Qty/Unit/UnitRate Present

| Check | Result |
|-------|--------|
| Total line items | 30 |
| Lines with Qty | 30 (100%) |
| Lines with Unit | 30 (100%) |
| Lines with UnitRate | 30 (100%) |
| Lines with Amount | 30 (100%) |

**Status:** PASS

---

### 3. Arithmetic Reconciliation

| CBS | Detail.csv Sum | Summary.md | Variance |
|-----|----------------|------------|----------|
| E | $240,000 | $240,000 | $0 |
| PM | $120,000 | $120,000 | $0 |
| P | $18,000 | $18,000 | $0 |
| MAT | $920,000 | $920,000 | $0 |
| CD | $380,000 | $380,000 | $0 |
| CI | $68,000 | $68,000 | $0 |
| COM | $55,000 | $55,000 | $0 |
| **Base Total** | **$1,801,000** | **$1,801,000** | **$0** |

**Status:** PASS

---

### 4. Coverage Check

| Deliverable | Line Items | Cost Allocated | Status |
|-------------|------------|----------------|--------|
| DEL-19.01 | L-001, L-002 | $60,000 | Covered |
| DEL-19.02 | L-003, L-004 | $40,000 | Covered |
| DEL-19.03 | L-005 | $20,000 | Covered |
| DEL-19.04 | L-006, L-007, L-008 | $120,000 | Covered |
| DEL-19.05 | L-026 | $32,000 | Covered |
| Package-level | L-009 through L-030 (excl above) | $1,529,000 | Covered |

**Status:** PASS — All 5 deliverables have associated costs

---

### 5. Double Count Check

| Potential Overlap | Analysis | Status |
|-------------------|----------|--------|
| Engineering vs. Software | E includes design (DEL-19.01-03) and software (DEL-19.04); distinct scope | OK |
| MAT vs. CD | Materials are supply; CD is installation; distinct | OK |
| PM vs. E | PM is management; E is technical; distinct | OK |
| COM vs. CD | COM is FAT/SAT/commissioning; CD is installation; distinct | OK |

**Status:** PASS — No double counting identified

---

### 6. Traceability Check

| Method | Line Count | % of Total |
|--------|------------|------------|
| QUOTE | 0 | 0% |
| RATE_TABLE | 0 | 0% |
| ALLOWANCE | 26 | 87% |
| PARAMETRIC | 4 | 13% |
| **Total** | **30** | **100%** |

All line items have SourceRef:
- ALLOWANCE items reference A-### assumptions
- PARAMETRIC items reference D-### decisions

**Status:** PASS

---

## Completeness Metrics

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| Lines priced by QUOTE | 0% | >50% for Class 3 | Below target (Class 5) |
| Lines priced by RATE_TABLE | 0% | >25% | Below target |
| Lines priced by ALLOWANCE/PARAMETRIC | 100% | <25% for Class 3 | Above target (Class 5) |
| Deliverables with explicit quantities | 0% | >75% | Below target |
| Decisions documented | 12 | All | Complete |
| Assumptions documented | 22 | All | Complete |
| Risks documented | 10 | All material | Complete |

**Overall Estimate Class:** Class 5 (Order of Magnitude)

**Accuracy Range:** -30% to +50% (typical for Class 5)

---

## Mapping Ambiguities

| Item | Ambiguity | Resolution | Decision Ref |
|------|-----------|------------|--------------|
| I/O count | Count not defined | Used 600-800 estimate based on facility scope | A-006 |
| Network architecture | Not designed | Used typical terminal configuration | A-009, A-010 |
| HMI screen count | Not defined | Used 40-60 screens based on facility | A-012 |

---

## Unknowns List (Top Assumptions by Value)

| Rank | Assumption | Value Impact | Confidence |
|------|------------|--------------|------------|
| 1 | DCS/PLC controllers (A-003) | $180,000 | MEDIUM |
| 2 | I/O modules (A-007) | $120,000 | LOW |
| 3 | Control cabinets (A-011) | $184,000 | LOW |
| 4 | Fiber optic infrastructure (A-010) | $160,000 | LOW |
| 5 | Software development (A-018) | $120,000 | LOW |
| 6 | Software licenses (A-019) | $100,000 | LOW |

---

## RUN_STATUS Determination

| Criterion | Value | Impact on Status |
|-----------|-------|------------------|
| Critical failures | 0 | OK |
| Missing required files | 0 | OK |
| Arithmetic errors | 0 | OK |
| Coverage gaps | 0 | OK |
| Material assumptions | 22 | WARNINGS |
| Allowance-heavy pricing | 100% | WARNINGS |

**RUN_STATUS:** WARNINGS

**Reason:** Estimate is complete and passes all technical checks, but is 100% allowance-based with numerous material assumptions. Estimate confidence is LOW. Suitable for early planning/budgeting only.

---

## Recommendations

1. **Obtain vendor budgetary quotes** for DCS/PLC system to reduce MAT uncertainty
2. **Complete PKG-20 instrumentation design** to firm up I/O count
3. **Complete control narratives** to define software development scope
4. **Confirm SIS requirements** from HAZOP to identify potential scope additions
5. **Define historian requirements** (tag count, retention, platform) with Employer
6. **Complete network architecture design** to firm up infrastructure scope

---

## QA Certification

| Field | Value |
|-------|-------|
| QA performed by | ESTIMATING Agent |
| Date | 2026-01-28 |
| Snapshot ID | EST_PKG19_DRAFT_2026-01-28_0015 |
| RUN_STATUS | WARNINGS |
| Recommendation | Suitable for early budgeting; refine with vendor quotes |
