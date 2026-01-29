# QA Report

## PKG-02 Earthworks & Ground Improvement Estimate

### Snapshot Information

| Field | Value |
|-------|-------|
| Snapshot ID | EST_PKG02_DRAFT_2026-01-28_2330 |
| QA Date | 2026-01-28 |
| Run Status | WARNINGS |

### Currency Consistency Check

| Check | Result | Notes |
|-------|--------|-------|
| Single currency used | PASS | All amounts in CAD |
| Currency matches config | PASS | CAD per _CONFIG.md |
| No mixed currencies | PASS | N/A |

### Schema Compliance Check

| Check | Result | Notes |
|-------|--------|-------|
| Qty populated on all lines | PASS | All lines have Qty=1 (LS convention) |
| Unit populated on all lines | PASS | All lines have Unit=LS |
| UnitRate populated on all lines | PASS | All lines have UnitRate=Amount |
| Amount populated on all lines | PASS | All amounts present |
| LineID unique | PASS | L001-L027 unique |
| CBS assigned | PASS | All lines have CBS code |
| SourceRef populated | PASS | All lines reference A-### or D-### |

### Arithmetic Reconciliation

| CBS | Detail.csv Sum | Summary.md Total | Variance | Status |
|-----|----------------|------------------|----------|--------|
| E | $268,500 | $268,500 | $0 | PASS |
| MAT | $1,135,000 | $1,135,000 | $0 | PASS |
| CD | $1,575,000 | $1,575,000 | $0 | PASS |
| CI | $279,000 | $279,000 | $0 | PASS |
| PM | $176,000 | $176,000 | $0 | PASS |
| P | $23,000 | $23,000 | $0 | PASS |
| COM | $88,000 | $88,000 | $0 | PASS |
| **BASE TOTAL** | **$3,544,500** | **$3,544,500** | **$0** | **PASS** |

### Coverage Check

| Deliverable | Has Cost Lines | Status |
|-------------|----------------|--------|
| DEL-02.01 | Yes (L001) | Covered |
| DEL-02.02 | Yes (L002) | Covered |
| DEL-02.03 | Yes (L003) | Covered |
| DEL-02.04 | Yes (L004-L006) | Covered |
| DEL-02.05 | Yes (L007) | Covered |
| DEL-02.06 | Yes (L008) | Covered |
| DEL-02.07 | Yes (L009) | Covered |
| DEL-02.08 | Yes (L010) | Covered |
| DEL-02.09 | Yes (L011) | Covered |
| Construction scope | Yes (L012-L023) | Covered |
| Indirects | Yes (L024-L027) | Covered |

**Coverage Result:** All 9 deliverables have associated cost lines. No uncovered scope.

### Double-Count Check

| Potential Overlap | Lines | Assessment |
|-------------------|-------|------------|
| Fill material vs placement | L014, L015 | Distinct - material supply vs labor |
| Ground improvement mat vs install | L016, L017 | Distinct - material vs installation |
| Survey in geotech vs separate | L004, L007 | Distinct - drilling vs topographic |

**Double-Count Result:** No double-counting identified.

### Unknowns List (Top Assumptions by Value)

| Rank | Assumption ID | Description | Amount | % of Base |
|------|---------------|-------------|--------|-----------|
| 1 | A-017 | Ground improvement installation | $900,000 | 25.4% |
| 2 | A-016 | Ground improvement materials | $600,000 | 16.9% |
| 3 | A-015 | Imported fill material | $375,000 | 10.6% |
| 4 | A-015 | Fill placement & compaction | $250,000 | 7.1% |
| 5 | A-014 | Excavation | $180,000 | 5.1% |
| 6 | A-022 | Geotextile | $160,000 | 4.5% |
| 7 | A-004 | Geotechnical investigation | $100,000 | 2.8% |
| 8 | A-013 | Site stripping | $75,000 | 2.1% |
| | | **Top 8 Total** | **$2,640,000** | **74.5%** |

### Completeness Metrics

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| Lines priced by QUOTE | 0% | >50% | FAIL |
| Lines priced by RATE_TABLE | 0% | >30% | FAIL |
| Lines priced by ALLOWANCE/PARAMETRIC | 100% | <20% | FAIL |
| Deliverables with explicit quantities | 0% | >80% | FAIL |
| Overall confidence | LOW | MED+ | FAIL |

### Known Issues

| Issue | Severity | Impact | Resolution |
|-------|----------|--------|------------|
| No earthwork quantities | HIGH | Cut/fill volumes assumed; ±50% uncertainty | Complete design drawings |
| No geotechnical data | HIGH | Ground improvement scope assumed | Complete geotechnical investigation |
| No vendor quotes | HIGH | All pricing via allowances | Obtain budgetary quotes |
| No rate tables | MEDIUM | Labor rates assumed | Provide project rate library |
| Deliverables in INITIALIZED state | MEDIUM | Scope not finalized | Progress deliverables to IN_PROGRESS |

### Mapping Ambiguities

| Deliverable | CBS Assignment | Ambiguity | Resolution |
|-------------|----------------|-----------|------------|
| DEL-02.06 (Records) | E | Could be CD (field QC) or E (documentation) | Assigned to E as document compilation |
| Ground improvement | CD + MAT | Split between materials and installation | 40% MAT / 60% CD typical split applied |

### QA Summary

| Category | Status |
|----------|--------|
| Schema compliance | PASS |
| Arithmetic | PASS |
| Coverage | PASS |
| Completeness | FAIL (100% allowances) |
| Overall | WARNINGS |

**Recommendation:** This estimate provides placeholder budget coverage for PKG-02 but requires significant input improvement before use for decision-making. Priority actions:
1. Complete geotechnical investigation (DEL-02.04)
2. Complete topographic survey (DEL-02.05)
3. Develop preliminary earthworks design with quantities (DEL-02.01, DEL-02.03)
4. Obtain budgetary quotes for ground improvement and drilling
