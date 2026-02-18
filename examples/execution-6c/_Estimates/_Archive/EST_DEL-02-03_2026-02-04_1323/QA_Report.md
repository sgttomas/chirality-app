# QA Report

## Snapshot: EST_DEL-02-03_2026-02-04_1323

This report documents quality assurance checks performed on the estimate and identifies any issues or warnings.

---

## Run Status: WARNINGS

The estimate completed successfully with warnings. All required artifacts were generated, but the estimate is based entirely on allowances due to missing rate tables.

---

## QA Checks Performed

### 1. Currency Consistency
| Check | Result | Notes |
|-------|--------|-------|
| All line items in same currency | PASS | All lines use CAD |
| Currency matches task specification | PASS | CAD specified in task brief |
| No mixed currencies | PASS | Single currency throughout |

### 2. Qty/Unit/UnitRate Completeness
| Check | Result | Notes |
|-------|--------|-------|
| All lines have Qty | PASS | 12/12 lines |
| All lines have Unit | PASS | 12/12 lines (HR or LS) |
| All lines have UnitRate | PASS | 12/12 lines |
| All lines have Amount | PASS | 12/12 lines |
| Lump sum lines use Qty=1, Unit=LS | PASS | Lines L-011, L-012 |

### 3. Arithmetic Reconciliation
| Check | Result | Notes |
|-------|--------|-------|
| Detail.csv sum | $12,120 | Sum of all Amount fields |
| Summary.md total | $12,000 | Rounded per policy |
| Variance | $120 | Within rounding tolerance |
| Reconciliation Status | PASS | Variance < 2% |

### 4. Coverage Check
| Check | Result | Notes |
|-------|--------|-------|
| Deliverable has cost lines | PASS | DEL-02-03 covered |
| All Procedure steps costed | PASS | Steps 1-9 mapped to line items |
| All mandatory requirements addressed | PASS | REQ-001 through REQ-008 covered |

### 5. Double Count Heuristics
| Check | Result | Notes |
|-------|--------|-------|
| Overlapping scope items | PASS | No duplicate scope detected |
| Duplicate line items | PASS | Each activity distinct |

### 6. Traceability Check
| Check | Result | Notes |
|-------|--------|-------|
| All lines have SourceRef | PASS | 12/12 lines reference assumptions or decisions |
| All lines have Method | PASS | 12/12 lines (all ALLOWANCE) |
| All lines have Confidence | PASS | 12/12 lines (LOW or MED) |

---

## Completeness Metrics

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| % Lines priced by QUOTE | 0% | N/A | N/A (no quotes expected) |
| % Lines priced by RATE_TABLE | 0% | >50% preferred | WARNING |
| % Lines priced by ALLOWANCE | 100% | <50% preferred | WARNING |
| % Deliverables with explicit quantities | 0% | N/A | N/A (effort-based) |
| Assumptions logged | 8 | All documented | PASS |
| Decisions logged | 6 | All documented | PASS |
| Risks identified | 5 | Adequate coverage | PASS |

---

## Warnings

### W-001: 100% Allowance-Based Pricing
| Warning ID | W-001 |
|------------|-------|
| **Issue** | All line items priced using allowances; no rate tables available |
| **Impact** | Moderate uncertainty in estimate accuracy (+/- 20-30%) |
| **Recommendation** | Provide rate tables in `_Estimates/_RateTables/` for future estimates |
| **Resolution** | Acceptable for current estimate; logged in Assumptions_Log.md |

### W-002: Optional Scope Items Included
| Warning ID | W-002 |
|------------|-------|
| **Issue** | Graphics/diagram scope (L-007, L-008) is optional per Specification.md |
| **Impact** | $1,800 CAD may be reduced or eliminated based on proposal strategy |
| **Recommendation** | Confirm diagram scope with Proposal Manager before production |
| **Resolution** | Logged in Decision_Log.md (D-005); Risk_Register.md (R-004) |

### W-003: Upstream Deliverable Dependencies
| Warning ID | W-003 |
|------------|-------|
| **Issue** | Narrative requires coordination with DEL-02-01, DEL-02-02, DEL-06-01, DEL-09-02 |
| **Impact** | Coordination effort may increase if upstream deliverables are delayed or unavailable |
| **Recommendation** | Proceed with assumptions; flag TBD items in narrative |
| **Resolution** | Logged in Risk_Register.md (R-002) |

---

## Unknowns List (Top Assumptions by Value)

| Rank | Assumption | Cost Impact | Confidence |
|------|------------|-------------|------------|
| 1 | A-006: Narrative production effort (28 hours) | $4,620 | LOW-MED |
| 2 | A-007: Graphics production effort (20 hours) | $1,800 | LOW |
| 3 | A-008: Overhead factor (15%) | $1,320 | MED |
| 4 | A-001: Lead Architect rate ($165/hr) | $4,620 | MED |
| 5 | A-002: Sustainability Specialist rate ($150/hr) | $900 | MED |

---

## Mapping Ambiguities

| Ambiguity | Resolution | Decision ID |
|-----------|------------|-------------|
| CBS classification for narrative document | Assigned to E (Engineering & Design) | D-003 |
| Diagram scope (optional vs. required) | Included as optional with allowance | D-005 |

---

## Estimate Validity Summary

| Requirement | Status |
|-------------|--------|
| Snapshot folder exists | PASS |
| BOE.md present and complete | PASS |
| Decision_Log.md present | PASS |
| Detail.csv with all required fields | PASS |
| Qty/Unit/UnitRate on all lines | PASS |
| Summary.md totals reconcile | PASS |
| Assumptions_Log.md present | PASS |
| Risk_Register.md present | PASS |
| QA_Report.md present | PASS |
| No deliverable edits | PASS |

**Overall Validity: VALID (with WARNINGS)**

---

## Document History
- 2026-02-04 1323 - Initial QA report created (ESTIMATING Agent)
