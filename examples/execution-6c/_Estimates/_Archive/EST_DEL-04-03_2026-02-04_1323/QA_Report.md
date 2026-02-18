# QA Report
## DEL-04-03: Communications and Reporting Plan Estimate

---

## Snapshot Identification

| Property | Value |
|----------|-------|
| **Snapshot ID** | EST_DEL-04-03_2026-02-04_1323 |
| **Deliverable** | DEL-04-03 Communications and Reporting Plan |
| **RUN_STATUS** | WARNINGS |

---

## QA Check Results

### 1. Currency Consistency

| Check | Status |
|-------|--------|
| **Single currency used** | PASS |
| **Currency** | CAD |
| **All line items in CAD** | PASS (21 of 21 lines) |
| **No mixed currencies** | PASS |

---

### 2. Qty/Unit/UnitRate Completeness

| Check | Status |
|-------|--------|
| **All lines have Qty** | PASS (21 of 21) |
| **All lines have Unit** | PASS (21 of 21) |
| **All lines have UnitRate** | PASS (21 of 21) |
| **All lines have Amount** | PASS (21 of 21) |

**Line Item Validation:**
- Lines L-001 through L-020: HR or LS units with valid Qty, UnitRate, Amount
- Line L-021 (Contingency): LS unit with Qty=1, UnitRate=Amount

---

### 3. Arithmetic Reconciliation

| Check | Value |
|-------|-------|
| **Detail.csv sum** | CAD 9,920 |
| **Summary.md total** | CAD 9,920 |
| **Variance** | CAD 0 |
| **Status** | PASS |

**CBS Bucket Reconciliation:**

| CBS | Detail.csv Sum | Summary.md | Variance | Status |
|-----|----------------|------------|----------|--------|
| E | CAD 7,720 | CAD 7,720 | CAD 0 | PASS |
| PM | CAD 900 | CAD 900 | CAD 0 | PASS |
| CONT | CAD 1,300 | CAD 1,300 | CAD 0 | PASS |
| **Total** | **CAD 9,920** | **CAD 9,920** | **CAD 0** | **PASS** |

---

### 4. Coverage Check

| Check | Status |
|-------|--------|
| **Deliverables with cost lines** | 1 of 1 (100%) |
| **DEL-04-03 coverage** | PASS (21 line items) |
| **Missing deliverable costs** | None |

---

### 5. Double Count Heuristics

| Check | Status |
|-------|--------|
| **Duplicate descriptions** | None detected |
| **Overlapping scope indicators** | None detected |
| **Status** | PASS |

---

### 6. Unknowns List (Top Assumptions by Value)

| Rank | Assumption ID | Description | Cost Impact (CAD) |
|------|---------------|-------------|-------------------|
| 1 | A-002 | Construction Manager rate CAD 140/hr | 6,720 |
| 2 | A-001 | Proposal Manager rate CAD 150/hr | 900 |
| 3 | A-003 | Project Controls Specialist rate CAD 100/hr | 1,000 |
| 4 | A-006 | Meeting cadence definition effort 8 hours | 1,120 |
| 5 | A-005 | Roles/responsibilities effort 6 hours | 840 |

**Top 5 assumptions account for CAD 10,580 of potential impact (>100% of base when rate changes considered).**

---

### 7. Completeness Metrics

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| **Lines priced by QUOTE** | 0% | N/A | N/A |
| **Lines priced by RATE_TABLE** | 0% | >50% | WARNING |
| **Lines priced by ALLOWANCE** | 100% | <50% | WARNING |
| **Deliverables with explicit quantities** | 100% | 100% | PASS |

---

### 8. Traceability Check

| Check | Status |
|-------|--------|
| **All lines have SourceRef** | PASS (21 of 21) |
| **All lines have Confidence** | PASS (21 of 21) |
| **All lines have CBS** | PASS (21 of 21) |
| **All lines have WBS_PackageID** | PASS (21 of 21) |
| **All lines have WBS_DeliverableID** | PASS (21 of 21) |

---

### 9. Decision Coverage

| Check | Status |
|-------|--------|
| **Currency decision** | D-001 documented |
| **Pricing method decision** | D-002 documented |
| **Rate assignment decision** | D-003 documented |
| **Contingency decision** | D-004 documented |
| **CBS mapping decision** | D-005 documented |
| **Total decisions** | 8 documented |

---

### 10. Mapping Ambiguities

| Item | Issue | Resolution | Decision ID |
|------|-------|------------|-------------|
| CBS assignment | Plan Document could be E or PM | Mapped primarily to E (development work); PM for review/oversight | D-005 |
| Responsible party rate | _CONTEXT.md says Construction Manager; rate not provided | Used CAD 140/hr allowance | D-003 |

---

## Warnings and Issues

### WARNINGS

| ID | Category | Description | Impact | Recommendation |
|----|----------|-------------|--------|----------------|
| W-001 | Pricing Method | 100% of lines priced by ALLOWANCE | Confidence LOW-MEDIUM | Provide rate tables in _RateTables/ for future estimates |
| W-002 | Rate Tables | No rate tables available | Unable to validate rate assumptions | Populate _RateTables/ with project rates |
| W-003 | Historical Data | No historical effort data for calibration | Effort estimates are parametric | Track actual effort for calibration |

### CRITICAL ISSUES

None identified.

---

## Run Status Determination

| Criterion | Status |
|-----------|--------|
| **All line items have Qty/Unit/UnitRate** | PASS |
| **Arithmetic reconciliation** | PASS |
| **Currency consistency** | PASS |
| **Coverage complete** | PASS |
| **Rate tables available** | FAIL (0 of 1) |
| **ALLOWANCE percentage < 50%** | FAIL (100% ALLOWANCE) |

**RUN_STATUS: WARNINGS**

Rationale: Estimate is structurally valid and complete, but 100% ALLOWANCE-based pricing without rate table validation. Confidence is LOW-MEDIUM. Recommend providing rate tables for next estimate iteration.

---

## Document Control

| Property | Value |
|----------|-------|
| **Created** | 2026-02-04 |
| **Agent** | ESTIMATING (Type 2) |
| **Snapshot** | EST_DEL-04-03_2026-02-04_1323 |
