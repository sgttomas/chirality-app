# QA Report

## PKG-04 Pavement & Surfacing Estimate

### Snapshot Information

| Field | Value |
|-------|-------|
| Snapshot ID | EST_PKG04_DRAFT_2026-01-28_2350 |
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
| LineID unique | PASS | L001-L029 unique |
| CBS assigned | PASS | All lines have CBS code |
| SourceRef populated | PASS | All lines reference A-### or D-### |

### Arithmetic Reconciliation

| CBS | Detail.csv Sum | Summary.md Total | Variance | Status |
|-----|----------------|------------------|----------|--------|
| E | $62,000 | $62,000 | $0 | PASS |
| MAT | $1,595,000 | $1,595,000 | $0 | PASS |
| CD | $1,790,000 | $1,790,000 | $0 | PASS |
| CI | $340,000 | $340,000 | $0 | PASS |
| PM | $219,000 | $219,000 | $0 | PASS |
| P | $32,000 | $32,000 | $0 | PASS |
| COM | $109,000 | $109,000 | $0 | PASS |
| **BASE TOTAL** | **$4,147,000** | **$4,147,000** | **$0** | **PASS** |

### Coverage Check

| Deliverable | Has Cost Lines | Status |
|-------------|----------------|--------|
| DEL-04.01 | Yes (L001) | Covered |
| DEL-04.02 | Yes (L002) | Covered |
| DEL-04.03 | Yes (L003) | Covered |
| DEL-04.04 | Yes (L004) | Covered |
| Asphalt Paving scope | Yes (L005-L006, L018-L019) | Covered |
| Concrete Paving scope | Yes (L007-L008) | Covered |
| Base Course scope | Yes (L009-L010) | Covered |
| Curb/Gutter scope | Yes (L011-L012) | Covered |
| Sidewalk scope | Yes (L013-L014) | Covered |
| Line Marking scope | Yes (L015-L016) | Covered |
| Site work (grading, survey, testing) | Yes (L017, L020-L022) | Covered |
| Joints/sealants | Yes (L023-L024) | Covered |
| OBJ-8 provisions | Yes (L025) | Covered |
| Indirects | Yes (L026-L029) | Covered |

**Coverage Result:** All 4 deliverables have associated cost lines. All scope elements from decomposition are covered. No uncovered scope.

### Double-Count Check

| Potential Overlap | Lines | Assessment |
|-------------------|-------|------------|
| Asphalt supply vs installation | L005, L006 | Distinct - material supply vs labor |
| Concrete supply vs installation | L007, L008 | Distinct - material vs installation |
| Base material vs placement | L009, L010 | Distinct - material vs placement labor |
| Curb material vs installation | L011, L012 | Distinct - material vs labor |
| Testing in CD vs COM | L020-L021, L029 | L020-L021 are field QC; L029 is final verification |

**Double-Count Result:** No double-counting identified.

### Unknowns List (Top Assumptions by Value)

| Rank | Assumption ID | Description | Amount | % of Base |
|------|---------------|-------------|--------|-----------|
| 1 | A-001 | Asphalt paving (supply + install) | $1,225,000 | 29.5% |
| 2 | A-002 | Concrete paving (supply + install) | $1,100,000 | 26.5% |
| 3 | A-011 | Base course (supply + install) | $495,000 | 11.9% |
| 4 | D-008 | Construction indirects | $340,000 | 8.2% |
| 5 | D-008 | PM/EPCM | $219,000 | 5.3% |
| 6 | A-003 | Curbs and gutters | $200,000 | 4.8% |
| 7 | D-008 | Testing/commissioning | $109,000 | 2.6% |
| 8 | A-012 | Fine grading | $90,000 | 2.2% |
| | | **Top 8 Total** | **$3,778,000** | **91.1%** |

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
| No pavement layout drawings | HIGH | Quantities assumed from area ratios; ±40% uncertainty | Complete DEL-04.01 drawings |
| No geotechnical data | HIGH | Pavement design and base thickness assumed | Coordinate with PKG-02 geotech |
| No traffic loading data | HIGH | Pavement thickness assumed; may be under/over-designed | Obtain traffic study from Owner |
| No vendor quotes | HIGH | All pricing via allowances | Obtain budgetary quotes |
| No rate tables | MEDIUM | Labor rates assumed | Provide project rate library |
| Deliverables in INITIALIZED state | MEDIUM | Scope not finalized | Progress deliverables to IN_PROGRESS |
| Rail crossing details undefined | MEDIUM | Special pavement at PKG-07 interfaces not priced | Coordinate with PKG-07 |

### Mapping Ambiguities

| Deliverable | CBS Assignment | Ambiguity | Resolution |
|-------------|----------------|-----------|------------|
| DEL-04.04 (Records) | E | Could be CD (field QC) or E (documentation) | Assigned to E as document compilation |
| Compaction testing | CD | Could be COM (commissioning) | Assigned to CD as construction QC |
| Survey work | CD | Could be E (design survey) | Assigned to CD as construction control |

### QA Summary

| Category | Status |
|----------|--------|
| Schema compliance | PASS |
| Arithmetic | PASS |
| Coverage | PASS |
| Completeness | FAIL (100% allowances) |
| Overall | WARNINGS |

**Recommendation:** This estimate provides placeholder budget coverage for PKG-04 but requires significant input improvement before use for decision-making. Priority actions:
1. Complete pavement layout drawings (DEL-04.01) with area calculations
2. Complete pavement design calculations (DEL-04.03) with traffic loading and geotechnical data
3. Coordinate with PKG-02 for subgrade preparation handoff criteria
4. Obtain budgetary quotes from paving contractors
5. Confirm OBJ-8 Phase 2 expansion corridor locations with Owner
