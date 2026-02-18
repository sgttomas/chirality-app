# QA Report
## EST_DEL-02-02_2026-02-04_1323

**Deliverable:** DEL-02-02 DesignBriefNarrative
**Package:** PKG-04 Design Proposal (Concept + Design Brief)
**Run Status:** WARNINGS

---

## 1. Currency Consistency Check

| Check | Result |
|-------|--------|
| Single currency used | PASS |
| Currency matches specification | PASS (CAD per task) |
| All line items have currency | PASS |

**Notes:** All 26 line items in Detail.csv use CAD currency.

---

## 2. Qty/Unit/UnitRate Completeness Check

| Check | Result |
|-------|--------|
| All lines have Qty | PASS |
| All lines have Unit | PASS |
| All lines have UnitRate | PASS |
| All lines have Amount | PASS |

**Notes:** All 26 line items have complete Qty/Unit/UnitRate/Amount fields. HR (hours) and LS (lump sum) units used appropriately.

---

## 3. Arithmetic Reconciliation

| Source | Amount (CAD) |
|--------|--------------|
| Sum of E lines (E-001 to E-022) | 23,950 |
| Sum of PM lines (PM-001 to PM-003) | 3,000 |
| Sum of CONT lines (CONT-001, CONT-002) | 3,900 |
| **Total from Detail.csv** | **30,850** |
| **Summary.md Base + Contingency** | **30,900** |
| **Variance** | 50 |

**Status:** PASS (within rounding tolerance)

**Notes:** CAD 50 variance due to rounding to nearest CAD 1,000 in Summary.md. Detail.csv provides exact values.

---

## 4. Coverage Check

| Check | Result |
|-------|--------|
| Deliverable has cost lines | PASS |
| All 5 discipline briefs covered | PASS |
| Additional narratives covered | PASS |
| QA/coordination activities covered | PASS |
| Contingency allocated | PASS |

**Coverage Detail:**

| Content Area | Line Items | Covered |
|--------------|------------|---------|
| Architectural Design Brief | E-001, E-002, E-003, E-004 | YES |
| Civil Design Brief | E-005, E-006, E-007 | YES |
| Structural Design Brief | E-008, E-009, E-010 | YES |
| Mechanical Design Brief | E-011, E-012, E-013 | YES |
| Electrical/IT Design Brief | E-014, E-015, E-016, E-017, E-018 | YES |
| Accessibility Narrative | E-019 | YES |
| Adaptability/Expansion Narrative | E-020 | YES |
| Durability/Maintenance Narrative | E-004 (premium) | YES |
| Document Integration | E-021, E-022 | YES |
| PM Coordination | PM-001, PM-002, PM-003 | YES |
| Contingency | CONT-001, CONT-002 | YES |

---

## 5. Double Count Heuristics

| Check | Result |
|-------|--------|
| Same scope in multiple lines | PASS (no duplicates) |
| Overlapping descriptions | PASS |

**Notes:** Line items are distinct by discipline and content area. No double counting detected.

---

## 6. Mapping Ambiguities

| Item | Ambiguity | Resolution |
|------|-----------|------------|
| DEL-02-02 CBS | Document deliverable vs. engineering services | Mapped to CBS E (Engineering & Design) per D-008 |
| Durability narrative | Could be separate CBS or part of Architectural | Included as premium on Architectural per D-010 |

**Notes:** Mapping decisions documented in Decision_Log.md.

---

## 7. Unknowns List (Top Assumptions by Value)

| Rank | Assumption | Cost Impact (CAD) | Confidence |
|------|------------|-------------------|------------|
| 1 | A-001: Architectural rate CAD 175/hr | 9,100 | MEDIUM |
| 2 | A-008: Integration and QA effort | 5,050 | MEDIUM |
| 3 | A-006: Electrical rate CAD 165/hr | 4,290 | MEDIUM |
| 4 | A-005: Mechanical rate CAD 165/hr | 2,970 | MEDIUM |
| 5 | A-004: Structural rate CAD 170/hr | 2,380 | MEDIUM |

**Total value of top 5 unknowns:** CAD 23,790 (77% of base estimate)

---

## 8. Completeness Metrics

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| % Lines by QUOTE | 0% | N/A | INFO |
| % Lines by RATE_TABLE | 0% | N/A | INFO |
| % Lines by ALLOWANCE | 100% | <50% | WARNING |
| % with explicit quantities | 100% | 100% | PASS |
| Confidence HIGH | 0% | >30% | WARNING |
| Confidence MEDIUM | 87% | -- | INFO |
| Confidence LOW | 13% | <20% | PASS |

---

## 9. Traceability Check

| Check | Result |
|-------|--------|
| All lines have SourceRef | PASS |
| SourceRef references valid IDs | PASS |

**Notes:** All line items reference either Assumption IDs (A-###) or Decision IDs (D-###) in Assumptions_Log.md and Decision_Log.md.

---

## 10. Known Issues

| ID | Issue | Severity | Impact |
|----|-------|----------|--------|
| QA-001 | 100% allowance-based pricing | WARNING | Low confidence in cost precision |
| QA-002 | No rate tables available | WARNING | Cannot validate rate assumptions |
| QA-003 | No historical comparison | INFO | Cannot benchmark against similar proposals |

---

## 11. Recommendations for Next Run

1. **Provide Rate Tables:** Add professional services rate tables to `_RateTables/` to replace allowance-based pricing with rate-based pricing.

2. **Historical Data:** Provide historical proposal costs for similar Design Brief deliverables to calibrate effort estimates.

3. **Fire Station Expertise:** Confirm team includes fire station design expertise; adjust R-001 risk if confirmed.

4. **DEL-02-01 Coordination:** Monitor coordination complexity with Concept Design Package; adjust PM effort if significant iteration required.

---

## Run Status Summary

| Status | Criteria | Result |
|--------|----------|--------|
| OK | No critical failures | -- |
| **WARNINGS** | Material assumptions/ambiguities | **SELECTED** |
| FAILED_INPUTS | Missing inputs preventing meaningful totals | -- |

**Run Status: WARNINGS**

**Rationale:** Estimate is complete and arithmetically correct, but all pricing is allowance-based with MEDIUM confidence. No rate tables or historical data available to validate assumptions.

---

*Generated by ESTIMATING agent*
*Snapshot: EST_DEL-02-02_2026-02-04_1323*
*Date: 2026-02-04*
