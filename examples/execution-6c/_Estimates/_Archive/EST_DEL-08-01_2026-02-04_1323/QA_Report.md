# QA Report
## DEL-08-01: DetailedProjectSchedule

---

## Snapshot Identification

| Property | Value |
|----------|-------|
| **Snapshot ID** | EST_DEL-08-01_2026-02-04_1323 |
| **Deliverable** | DEL-08-01 DetailedProjectSchedule |
| **Run Date** | 2026-02-04 |
| **RUN_STATUS** | WARNINGS |

---

## QA Checks Performed

### 1. Currency Consistency

| Check | Result | Notes |
|-------|--------|-------|
| Single currency used | PASS | All amounts in CAD |
| Currency declared in BOE | PASS | CAD specified in BOE.md |
| Currency column populated | PASS | All Detail.csv lines show CAD |

---

### 2. Qty/Unit/UnitRate Presence (Hard Check)

| Check | Result | Notes |
|-------|--------|-------|
| All lines have Qty | PASS | 20/20 lines populated |
| All lines have Unit | PASS | 20/20 lines populated (HR, LS) |
| All lines have UnitRate | PASS | 20/20 lines populated |
| Qty x UnitRate = Amount | PASS | All calculations verified |

---

### 3. Arithmetic Reconciliation (Detail to Summary)

| Check | Result | Notes |
|-------|--------|-------|
| E category total | PASS | Detail: $7,500 = Summary: $7,500 |
| PM category total | PASS | Detail: $3,050 = Summary: $3,050 |
| CONT category total | PASS | Detail: $1,500 = Summary: $1,500 |
| Grand total | PASS | Detail: $12,050 = Summary: $12,050 |

---

### 4. Coverage Check

| Check | Result | Notes |
|-------|--------|-------|
| All deliverables costed | PASS | DEL-08-01 has associated cost lines |
| Scope items addressed | PASS | All 4 anticipated artifacts covered (Gantt, Milestones, Narrative, Assumptions) |
| Requirements addressed | PASS | REQ-SCH-000 through REQ-SCH-012 verification effort included |

---

### 5. Double Count Heuristics

| Check | Result | Notes |
|-------|--------|-------|
| Duplicate line items | PASS | No duplicated scope identified |
| Overlapping activities | PASS | Activities are discrete work packages |

---

### 6. Traceability Check

| Check | Result | Notes |
|-------|--------|-------|
| All lines have SourceRef | PASS | 20/20 lines reference assumption IDs |
| SourceRefs valid | PASS | All A-### and D-### IDs exist in logs |
| Method column populated | PASS | All lines show ALLOWANCE |

---

### 7. Completeness Metrics

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| Lines priced by QUOTE | 0% | N/A | INFO |
| Lines priced by RATE_TABLE | 0% | Preferred | WARNING |
| Lines priced by ALLOWANCE | 100% | <50% preferred | WARNING |
| Deliverables with explicit quantities | 100% | >80% | PASS |
| Confidence Level | LOW-MEDIUM | MEDIUM+ | WARNING |

---

## Mapping Ambiguities

| Item | Ambiguity | Resolution | Decision ID |
|------|-----------|------------|-------------|
| Activity count | Range 50-150 specified | Used midpoint (100) | D-005 |
| RFP Section 7.1.9 | Not accessible | Inferred from decomposition | D-008 |

---

## Unknowns List (Top Assumptions by Value)

| Rank | Assumption ID | Description | Cost Impact (CAD) |
|------|---------------|-------------|-------------------|
| 1 | A-001 | Scheduler rate ($125/hr) | $7,500 |
| 2 | A-002 | Senior PM rate ($150/hr) | $1,650 |
| 3 | A-003 | Technical Lead rate ($140/hr) | $1,400 |
| 4 | A-006 | Duration assignment effort (12 hrs) | $1,500 |
| 5 | A-005/A-007 | WBS/Dependency effort (8 hrs each) | $1,000 each |

---

## Issues and Findings

### Finding 1: No Rate Tables Available

| Severity | WARNING |
|----------|---------|
| **Description** | All pricing based on allowance assumptions due to empty _RateTables/ folder |
| **Impact** | Estimate accuracy depends on market rate assumptions |
| **Recommendation** | Provide firm billing rates for future estimate updates |

---

### Finding 2: RFP Section 7.1.9 Not Accessible

| Severity | WARNING |
|----------|---------|
| **Description** | Primary RFP schedule requirements section marked as "location TBD" |
| **Impact** | Additional effort may be required if RFP specifies different requirements |
| **Recommendation** | Obtain and review RFP Section 7.1.9 before finalizing estimate |

---

### Finding 3: Cross-Deliverable Coordination Complexity

| Severity | INFO |
|----------|------|
| **Description** | 5 deliverable interfaces identified requiring coordination |
| **Impact** | Included in estimate; 10 hours coordination effort |
| **Recommendation** | N/A - standard proposal development practice |

---

## RUN_STATUS Determination

| Status | Rationale |
|--------|-----------|
| **WARNINGS** | Estimate is complete and usable but has material assumptions: (1) 100% ALLOWANCE pricing, (2) RFP requirements partially unknown, (3) labour rates assumed |

---

## Certification

| Check Category | Status |
|----------------|--------|
| Currency Consistency | PASS |
| Qty/Unit/UnitRate Present | PASS |
| Arithmetic Reconciliation | PASS |
| Coverage | PASS |
| Double Count | PASS |
| Traceability | PASS |
| **Overall QA Status** | PASS with WARNINGS |

---

## Document Control

| Property | Value |
|----------|-------|
| **Snapshot ID** | EST_DEL-08-01_2026-02-04_1323 |
| **Created** | 2026-02-04 |
| **Agent** | ESTIMATING (Type 2) |
