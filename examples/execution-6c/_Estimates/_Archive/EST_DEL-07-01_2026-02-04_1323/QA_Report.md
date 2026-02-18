# QA Report

## Estimate Identification

| Property | Value |
|----------|-------|
| **Snapshot ID** | EST_DEL-07-01_2026-02-04_1323 |
| **Deliverable** | DEL-07-01 Design-Build Firm Experience Profile |
| **QA Date** | 2026-02-04 |
| **RUN_STATUS** | WARNINGS |

---

## Mandatory Checks

### Currency Consistency
| Check | Status | Notes |
|-------|--------|-------|
| All line items use same currency | PASS | All amounts in CAD |
| Currency matches BOE declaration | PASS | BOE declares CAD |
| No mixed currencies | PASS | Single currency throughout |

### Qty/Unit/UnitRate Completeness
| Check | Status | Notes |
|-------|--------|-------|
| All lines have Qty populated | PASS | 17 lines, all with Qty |
| All lines have Unit populated | PASS | HR or LS for all lines |
| All lines have UnitRate populated | PASS | Rates derived from assumptions |
| All lines have Amount calculated | PASS | Qty x UnitRate = Amount verified |

### Arithmetic Reconciliation
| Check | Status | Notes |
|-------|--------|-------|
| Detail.csv sum = Summary total | PASS | $11,280 CAD |
| Base estimate reconciles | PASS | $9,400 CAD |
| Contingency calculation correct | PASS | $9,400 x 20% = $1,880 CAD |

### Traceability
| Check | Status | Notes |
|-------|--------|-------|
| All lines have SourceRef | PASS | References to assumptions and procedure steps |
| All assumptions logged | PASS | 12 assumptions in Assumptions_Log.md |
| All decisions logged | PASS | 9 decisions in Decision_Log.md |

---

## Coverage Check

### Deliverable Coverage
| Deliverable | Cost Lines | Status |
|-------------|------------|--------|
| DEL-07-01 | 17 | COVERED |

### WBS Coverage
| Package | Deliverables Covered | Status |
|---------|---------------------|--------|
| PKG-03 | DEL-07-01 | PARTIAL (1 of 3 deliverables in package) |

*Note: This estimate covers only DEL-07-01. DEL-07-02 and DEL-07-03 require separate estimates.*

---

## Double-Count Heuristics
| Check | Status | Notes |
|-------|--------|-------|
| No scope priced in multiple lines | PASS | Each activity is distinct |
| No overlap with other deliverable estimates | PASS | DEL-07-01 scope isolated |
| Cross-deliverable coordination (DEL-07-02/03) | PASS | Coordination cost attributed to DEL-07-01 only |

---

## Unknowns List (Top Assumptions by Value)

| Rank | Assumption ID | Description | Cost Impact (CAD) |
|------|---------------|-------------|-------------------|
| 1 | A-005 | Document drafting effort (20 hrs PM) | $3,000 |
| 2 | A-009 | Technical review effort (8 hrs Sr PM) | $1,600 |
| 3 | A-006 | Data collection effort (8 hrs Admin) | $800 |
| 4 | A-007 | Reference coordination (4 hrs PM) | $600 |
| 5 | A-010 | Executive review (2 hrs Executive) | $600 |

**Total assumption-driven cost:** $9,400 CAD (100% of base estimate)

---

## Completeness Metrics

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| % lines priced by QUOTE | 0% | >50% preferred | FAIL |
| % lines priced by RATE_TABLE | 0% | >25% preferred | FAIL |
| % lines priced by ALLOWANCE | 100% | <25% preferred | FAIL |
| % lines with LOW confidence | 65% | <20% preferred | FAIL |
| % lines with MED confidence | 35% | >60% preferred | PARTIAL |
| % lines with HIGH confidence | 0% | >20% preferred | FAIL |

**Overall Completeness Rating:** LOW

---

## Mapping Ambiguities

| Item | Description | Resolution |
|------|-------------|------------|
| CBS Assignment | DEL-07-01 is qualifications document; mapped to E (Engineering) and PM (Project Management) | D-008 recorded; PM overhead set to 0% per D-005 |
| Labor Rate Basis | No rate tables available; used assumed market rates | A-001 through A-004 recorded |
| Effort Estimates | No historical proposal data; effort based on procedure step analysis | A-005 through A-010 recorded |

---

## Input Gaps Identified

| Gap | Severity | Impact on Estimate |
|-----|----------|-------------------|
| RFP Section 7.1.6 not accessible | HIGH | Cannot verify content requirements; scope uncertainty |
| OSR (Appendix A) not accessible | HIGH | Cannot verify tailoring requirements |
| Firm project database not provided | HIGH | Cannot verify data availability |
| Rate tables not available | MEDIUM | All pricing uses allowances |
| Historical proposal cost data not available | MEDIUM | Effort estimates are assumptions |

---

## RUN_STATUS Determination

| Criteria | Assessment |
|----------|------------|
| Snapshot folder exists | PASS |
| BOE.md complete | PASS |
| Decision_Log.md complete | PASS |
| Detail.csv valid schema | PASS |
| All lines have Qty/Unit/UnitRate | PASS |
| Summary reconciles to Detail | PASS |
| Assumptions explicit | PASS |
| Risk/contingency documented | PASS |
| Critical inputs missing | YES (RFP, OSR, firm data) |

**RUN_STATUS: WARNINGS**

Rationale: Estimate is structurally complete and passes all schema checks, but is 100% allowance-based due to missing inputs (rate tables, quotes, RFP access). Confidence is LOW. Estimate is suitable for budgeting purposes but should be refined when inputs become available.

---

## Recommendations for Next Run

1. **Provide rate tables:** Add ProposalLaborRates.csv to _RateTables/ with firm-specific fully-loaded rates
2. **Obtain RFP access:** Review Section 7.1.6 to verify content requirements and refine scope
3. **Verify firm data:** Confirm project database availability and comparable project inventory
4. **Historical data:** If available, provide past proposal effort data for similar deliverables
5. **Reference verification:** Pre-identify and contact references before next estimate iteration

---

**QA Report Status:** Complete for snapshot EST_DEL-07-01_2026-02-04_1323
