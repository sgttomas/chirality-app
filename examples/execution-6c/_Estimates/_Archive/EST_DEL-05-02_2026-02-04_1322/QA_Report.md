# QA Report

## Snapshot Information

| Field | Value |
|-------|-------|
| **Snapshot ID** | EST_DEL-05-02_2026-02-04_1322 |
| **Deliverable** | DEL-05-02 AppendixH ScheduleB CostBreakdown |
| **QA Date** | 2026-02-04 |
| **RUN_STATUS** | WARNINGS |

---

## QA Checks Performed

### 1. Currency Consistency
| Check | Result | Notes |
|-------|--------|-------|
| Single currency used | PASS | All amounts in CAD |
| Currency documented in BOE | PASS | Currency = CAD per D-006 |
| No mixed currency line items | PASS | All Detail.csv Currency = CAD |

### 2. Qty/Unit/UnitRate Completeness (Hard Check)
| Check | Result | Notes |
|-------|--------|-------|
| All lines have Qty | PASS | 25 lines, all have Qty populated |
| All lines have Unit | PASS | 25 lines, all have Unit (LS or YR) |
| All lines have UnitRate | PASS | 25 lines, all have UnitRate = Amount for LS items |
| Allowance convention followed | PASS | All allowances: Qty=1, Unit=LS, UnitRate=Amount |

### 3. Arithmetic Reconciliation
| Check | Result | Notes |
|-------|--------|-------|
| Detail.csv sums correctly | PASS | Sum of amounts verified |
| Summary.md matches Detail.csv | PASS | Within rounding tolerance ($1,000) |
| Category subtotals correct | PASS | GR=$450K, B=$5.2M, SW=$1.225M verified |

**Reconciliation Detail:**
- General Requirements (L-001 to L-004): $200K + $75K + $100K + $75K = $450,000
- Building (L-005 to L-012): $600K + $900K + $800K + $600K + $900K + $600K + $400K + $400K = $5,200,000
- Sitework (L-013 to L-017): $300K + $400K + $350K + $100K + $75K = $1,225,000
- Contingency (L-018): $598,000
- Options Capital (L-019 to L-022, L-024, L-025): $75K + $50K + $40K + $60K + $25K + $30K = $280,000
- Option 4 Monitoring (L-023): $6,000/year
- **Base Scope Total**: $7,473,000
- **Grand Total (Capital)**: $7,753,000

### 4. Coverage Check
| Check | Result | Notes |
|-------|--------|-------|
| All cost categories present | PASS | GR, Building, Sitework, Options, Contingency |
| Additional Options 1-6 present | PASS | 6 options with separate line items |
| Option 4 monitoring separated | PASS | L-023 is separate line for monitoring fee (R-004) |
| Pickled sand building excluded | PASS | No line item for pickled sand storage (R-007) |

### 5. Double Count Heuristics
| Check | Result | Notes |
|-------|--------|-------|
| No duplicate scope | PASS | Each scope element appears once |
| No overlapping descriptions | PASS | Line items have distinct scope descriptions |

### 6. Unknowns List (Top Assumptions by Value)
| Rank | Assumption | Value Impact | Confidence |
|------|------------|--------------|------------|
| 1 | A-008: Building area 20,000 SF | $5,200,000 (building cost) | LOW |
| 2 | A-009: 12-acre site development | $1,225,000 (sitework cost) | HIGH |
| 3 | A-006: 10% design contingency | $598,000 | MED |
| 4 | A-007: 10% GR factor | $450,000 | MED |
| 5 | A-010: Service tie-in allowance | $400,000 | MED |

---

## Completeness Metrics

| Metric | Value | Assessment |
|--------|-------|------------|
| % of lines priced by QUOTE | 0% | No vendor quotes |
| % of lines priced by RATE_TABLE | 0% | No rate tables |
| % of lines priced by ALLOWANCE/PARAMETRIC | 100% | All allowance-based |
| % of deliverables with explicit quantities | 0% | Quantities TBD (DEL-02-01 pending) |
| Line items with HIGH confidence | 0 | None |
| Line items with MED confidence | 0 | None |
| Line items with LOW confidence | 25 | All |
| Total line items | 25 | Complete set |

---

## Mapping Ambiguities

| Item | CBS Assignment | Ambiguity | Resolution |
|------|----------------|-----------|------------|
| Fire apparatus exhaust | Building (B) - Fire Protection | Could be Mechanical or Fire Protection | Assigned to Fire Protection per Datasheet.md assumption |
| Emergency generator | Building (B) - Electrical | Could be separate equipment line | Included in Electrical per Datasheet.md assumption |
| Bay sumps | Building (B) - Mechanical | Could be Plumbing or Specialties | Included in Mechanical per Datasheet.md assumption |
| Solar-ready provisions | Building (B) - Electrical | Could be separate line | Included in Electrical per Datasheet.md assumption |

---

## Known Issues

| Issue ID | Description | Severity | Impact |
|----------|-------------|----------|--------|
| QA-001 | All pricing based on allowances; no firm pricing data | HIGH | LOW confidence in all estimates |
| QA-002 | Building area not confirmed; 20,000 SF is assumption | HIGH | Could vary +/- 30% |
| QA-003 | No Appendix H template obtained | MED | Line item structure may not match actual template |
| QA-004 | DEL-02-01 not complete | HIGH | Quantities and systems TBD |
| QA-005 | No rate tables provided | MED | Cannot validate unit rates |
| QA-006 | Additional Options scope not detailed | MED | Option costs are rough allowances |

---

## RUN_STATUS Determination

| Status | Criteria | Assessment |
|--------|----------|------------|
| OK | No critical failures | Not met |
| WARNINGS | Material assumptions/ambiguities exist | **MET** |
| FAILED_INPUTS | Inputs missing such that totals not meaningful | Not met (totals are directionally useful) |

**Final RUN_STATUS: WARNINGS**

**Rationale:**
- Estimate is complete and mathematically valid
- All required line items present
- All QA checks pass
- However, 100% allowance-based pricing with LOW confidence
- Material assumptions exist (building area, site scope, options)
- Estimate provides order-of-magnitude basis but requires refinement

---

## Recommendations

1. **Obtain DEL-02-01 Concept Design** to update building area and system assumptions
2. **Obtain Appendix H template** to confirm line item structure matches RFP requirements
3. **Provide rate tables** to improve pricing confidence
4. **Clarify Additional Options scope** with Design Lead
5. **Complete site survey** to validate sitework assumptions
6. **Update estimate** when design progresses to reduce contingency requirements

---

## Document Information

| Field | Value |
|-------|-------|
| Created | 2026-02-04 |
| QA Checks | 6 categories, 15 individual checks |
| Known Issues | 6 |
