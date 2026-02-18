# QA Report

## Snapshot Identification

| Attribute | Value |
|---|---|
| **Snapshot ID** | EST_DEL-05-03_2026-02-04_1323 |
| **Deliverable** | DEL-05-03 Pricing Narrative and Assumptions |
| **QA Date** | 2026-02-04 |
| **RUN_STATUS** | WARNINGS |

---

## Mandatory Checks

### Currency Consistency

| Check | Result | Notes |
|---|---|---|
| Single currency used | PASS | All amounts in CAD |
| Currency column populated | PASS | All 14 line items have Currency = CAD |
| No mixed currencies | PASS | N/A (single currency snapshot) |

---

### Qty/Unit/UnitRate Presence (Hard Check)

| Check | Result | Notes |
|---|---|---|
| Qty populated on all lines | PASS | All 14 lines have Qty = 1 |
| Unit populated on all lines | PASS | All 14 lines have Unit = LS |
| UnitRate populated on all lines | PASS | All 14 lines have UnitRate values |
| Amount = Qty x UnitRate | PASS | All lines verified (Qty=1, Unit=LS, UnitRate=Amount) |

**Note:** All line items use allowance convention (Qty=1, Unit=LS, UnitRate=Amount) per AGENT_ESTIMATING STRUCTURE requirements.

---

### Arithmetic Reconciliation

| Check | Result | Notes |
|---|---|---|
| Detail.csv sum matches Summary.md | PASS | Detail total = $12,650; Summary total = $12,650 |
| CBS subtotals reconcile | PASS | E = $8,600; PM = $4,400; CONT = $1,650 (total in Summary confirmed) |
| Contingency calculation correct | PASS | 15% x $11,000 base = $1,650 |

**Reconciliation Detail:**
- Sum of L-001 through L-013 (base): $500 + $1,200 + $800 + $600 + $1,000 + $1,500 + $800 + $1,200 + $1,000 + $1,200 + $800 + $1,000 + $400 = $11,000
- L-100 (contingency): $1,650
- Total: $12,650

---

### Coverage Check

| Check | Result | Notes |
|---|---|---|
| WBS coverage | PASS | DEL-05-03 covered; no other deliverables in scope |
| CBS coverage | PASS | E (Engineering), PM (Project Management), CONT (Contingency) all represented |
| Missing deliverables | N/A | Single-deliverable estimate |

---

### Double Count Check

| Check | Result | Notes |
|---|---|---|
| Duplicate scope detection | PASS | No duplicate descriptions or overlapping scope detected |
| Cross-reference integrity | PASS | Each line item maps to distinct narrative section or activity |

---

## Completeness Metrics

### Pricing Method Distribution

| Method | Line Count | Amount | % of Total |
|---|---|---|---|
| QUOTE | 0 | $0 | 0% |
| RATE_TABLE | 0 | $0 | 0% |
| HISTORICAL | 0 | $0 | 0% |
| ALLOWANCE | 14 | $12,650 | 100% |
| PARAMETRIC | 0 | $0 | 0% |

**Assessment:** 100% allowance-based pricing indicates LOW confidence. Rate tables or historical data needed to improve accuracy.

---

### Confidence Distribution

| Confidence | Line Count | Amount | % of Total |
|---|---|---|---|
| HIGH | 0 | $0 | 0% |
| MED | 0 | $0 | 0% |
| LOW | 14 | $12,650 | 100% |

**Assessment:** 100% LOW confidence. All pricing based on professional judgment without rate tables or quotes.

---

### Quantity Extraction

| Check | Result | Notes |
|---|---|---|
| Explicit quantities extracted | PARTIAL | Narrative sections quantifiable (8 sections); effort per section estimated |
| Quantities derived from documents | YES | Datasheet Content Structure provides section breakdown |
| Parametric quantities | NO | Hours-based effort estimates for professional services |

**Deliverables with Explicit Quantities:** 30% (section count known; effort uncertain)

---

## Mapping Ambiguities

| Item | Ambiguity | Resolution | Decision ID |
|---|---|---|---|
| Professional services CBS | Could be E (Engineering) or PM (Project Management) | Split: document production → E; coordination/review → PM | D-003 |
| Value alternatives scope | Optional per source documents; unclear if included | Assumed minimal; priced as allowance | A-003 |

---

## Unknowns List (Top Assumptions/Allowances by Value)

| Rank | Item | Amount | Type | Notes |
|---|---|---|---|---|
| 1 | L-100 Contingency | $1,650 | CONT | 15% of base; accounts for allowance-based pricing risk |
| 2 | L-006 Additional Options (Section 6) | $1,500 | ALLOWANCE | 6 options to document; scope uncertain |
| 3 | L-002 Addenda Integration (Section 2) | $1,200 | ALLOWANCE | 3 addenda; impacts well-documented |
| 4 | L-008 Pricing Assumptions (Section 8) | $1,200 | ALLOWANCE | Multiple TBD items in source documents |
| 5 | L-010 Cross-Reference to Related Deliverables | $1,200 | ALLOWANCE | Depends on deliverable availability |

---

## Issues and Warnings

### Critical Issues

None identified.

### Warnings

| ID | Warning | Impact | Recommendation |
|---|---|---|---|
| W-001 | No rate tables available | All pricing LOW confidence | Provide rate tables in _RateTables/ |
| W-002 | Multiple TBD items in source documents | Effort estimates uncertain | Resolve TBD items before production |
| W-003 | 100% allowance-based pricing | Actual costs may vary +/- 30% | Track actuals; update for future estimates |
| W-004 | Cross-deliverable dependencies unknown | Cross-reference effort may need adjustment | Confirm related deliverable status |

---

## RUN_STATUS Determination

| Status | Criteria | Result |
|---|---|---|
| OK | No critical failures; estimates meaningful | NOT MET |
| WARNINGS | Material assumptions/ambiguities exist | **MET** |
| FAILED_INPUTS | Inputs missing; totals not meaningful | NOT MET |

**RUN_STATUS: WARNINGS**

**Rationale:**
- All mandatory checks pass (currency, Qty/Unit/UnitRate, arithmetic)
- Coverage is complete for single-deliverable scope
- However, 100% allowance-based pricing and multiple TBD items in source documents create material uncertainty
- Estimate is usable for budgeting but should be validated with rate tables and resolved TBD items

---

## Recommendations for Next Run

1. **Provide rate tables** for professional services (estimator, commercial lead, proposal manager hourly rates)
2. **Resolve TBD items** in Datasheet.md and Specification.md before next estimate run
3. **Track actual effort** during DEL-05-03 production to calibrate future estimates
4. **Confirm cross-deliverable status** to validate effort assumptions for L-009 and L-010
5. **Update _CONFIG.md** with project-specific parameters if defaults are not appropriate

---

**QA Completed:** 2026-02-04 13:23
**QA Agent:** ESTIMATING (Type 2)
