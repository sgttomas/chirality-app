# QA Report
## DEL-06-01: CommissioningTrainingCloseoutWarrantyNarrative

---

## Snapshot Information

| Property | Value |
|----------|-------|
| **Snapshot ID** | EST_DEL-06-01_2026-02-04_1323 |
| **Created** | 2026-02-04 |
| **RUN_STATUS** | WARNINGS |

---

## QA Checks Summary

| Check | Status | Notes |
|-------|--------|-------|
| Currency consistency | PASS | All line items in CAD |
| Qty/Unit/UnitRate present | PASS | All 17 lines have required fields |
| Arithmetic reconciliation | PASS | Detail.csv sums match Summary.md (within rounding) |
| Coverage check | PASS | DEL-06-01 has associated cost lines |
| Double count check | PASS | No duplicate scope identified |
| Traceability check | PASS | All lines have SourceRef (assumption IDs) |
| Method field populated | PASS | All lines have Method (ALLOWANCE) |
| Confidence field populated | PASS | All lines have Confidence (LOW/MED) |

---

## Currency Consistency

| Check | Result |
|-------|--------|
| **Single currency used** | YES - CAD |
| **Currency field on all lines** | YES - All 17 lines |
| **Foreign currency conversions** | N/A - No foreign currency |

**Status:** PASS

---

## Qty/Unit/UnitRate Validation

| Check | Result |
|-------|--------|
| **Lines with Qty populated** | 17/17 (100%) |
| **Lines with Unit populated** | 17/17 (100%) |
| **Lines with UnitRate populated** | 17/17 (100%) |
| **Lines with Amount populated** | 17/17 (100%) |
| **Qty x UnitRate = Amount** | 17/17 verified |

**Units Used:**
- HR (Hours): 16 lines
- LS (Lump Sum): 1 line (Contingency)

**Status:** PASS

---

## Arithmetic Reconciliation

| Source | E (Engineering) | PM | CONT | Total |
|--------|-----------------|-------|------|-------|
| Detail.csv sum | $7,100.00 | $600.00 | $1,170.00 | $8,870.00 |
| Summary.md | $7,100 | $600 | $1,200 | $8,900 |
| Variance | $0 | $0 | $30 | $30 |

**Variance Explanation:** Summary.md rounds contingency to nearest $100 ($1,170 -> $1,200); total rounded to $8,900

**Status:** PASS (within rounding policy)

---

## Coverage Check

| WBS Item | Has Cost Lines | Status |
|----------|----------------|--------|
| PKG-07/DEL-06-01 | YES (17 lines) | PASS |

**Deliverables Without Cost Lines:** None

**Status:** PASS

---

## Double Count Heuristics

| Potential Overlap | Assessment | Status |
|-------------------|------------|--------|
| Technical Lead support overlapping Commissioning Lead | No overlap - Technical Leads provide input; Commissioning Lead drafts | PASS |
| Proposal Manager overlapping quality review | No overlap - PM oversight is separate from Step 12 quality review | PASS |
| Step-by-step effort overlapping integration | No overlap - Steps 4-8 are drafting; Step 9 is integration | PASS |

**Status:** PASS

---

## Traceability Check

| Check | Result |
|-------|--------|
| **Lines with SourceRef** | 17/17 (100%) |
| **SourceRef types used** | Assumption IDs (A-xxx), Decision IDs (D-xxx) |
| **Lines without source** | 0 |

**Status:** PASS

---

## Completeness Metrics

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| % priced by QUOTE | 0% | N/A | - |
| % priced by RATE_TABLE | 0% | N/A | - |
| % priced by ALLOWANCE | 100% | <50% preferred | WARNING |
| % with explicit quantities | 100% | >90% | PASS |
| Deliverables covered | 100% (1/1) | 100% | PASS |

**Status:** WARNINGS (100% allowance-based pricing)

---

## Unknowns List (Top Assumptions by Value)

| Rank | Assumption ID | Description | Cost Impact (CAD) |
|------|---------------|-------------|-------------------|
| 1 | A-007 | Commissioning narrative development (6 hrs @ $175/hr) | $1,050 |
| 2 | A-005 | RFP/facility context review (5 hrs @ $175/hr) | $875 |
| 3 | A-008 | Training plan development (4 hrs @ $175/hr) | $700 |
| 4 | A-019 | Proposal Manager oversight (4 hrs @ $150/hr) | $600 |
| 5 | Multiple | Steps 6-12 (various, 3 hrs each @ $175/hr) | $525 each |

**Top 5 assumptions represent ~40% of base estimate**

---

## Mapping Ambiguities

| Item | Ambiguity | Resolution | Decision ID |
|------|-----------|------------|-------------|
| CBS assignment | Deliverable spans commissioning (COM) and proposal (E/PM) | Mapped to E/PM (proposal production scope, not execution) | D-004 |
| Commissioning Lead vs. PM | Responsibility per _CONTEXT.md is "Commissioning Lead / PM" | Treated as single role; priced at Commissioning Lead rate | D-007 |

---

## Known Issues

| Issue ID | Description | Severity | Recommendation |
|----------|-------------|----------|----------------|
| QA-001 | 100% allowance-based pricing | WARNING | Provide rate tables for future estimates |
| QA-002 | Effort estimates based on Procedure.md durations, not historical data | WARNING | Track actual effort for calibration |
| QA-003 | RFP requirements not directly verified | WARNING | Verify against actual RFP PDF when accessible |
| QA-004 | Cross-deliverable consistency depends on draft maturity | WARNING | Coordinate early; may require iteration |

---

## Run Status Determination

| Criterion | Assessment |
|-----------|------------|
| Critical failures | None |
| Material assumptions/ambiguities | Yes - 100% allowance-based; RFP not verified |
| Missing inputs | Partial - Rate tables not available; RFP text not accessible |
| Totals meaningful | Yes - Estimate provides reasonable order of magnitude |

**RUN_STATUS:** WARNINGS

**Rationale:** Estimate is complete and internally consistent, but 100% reliance on allowances and unverified RFP requirements warrant WARNINGS status. Totals are meaningful for budgeting purposes but should be refined with rate tables and RFP verification.

---

## Recommendations for Next Run

1. **Provide rate tables** in `_Estimates/_RateTables/` for professional services rates
2. **Verify RFP requirements** against actual PDF text (Sections 7.3.6, 7.3.7, 7.6)
3. **Track actual effort** on this deliverable to calibrate future estimates
4. **Update config** in `_CONFIG.md` with confirmed currency, rounding policy
5. **Refine Technical Lead effort** based on actual scope of technical input needed

---

## Document Control

| Property | Value |
|----------|-------|
| **Created** | 2026-02-04 |
| **Agent** | ESTIMATING (Type 2) |
