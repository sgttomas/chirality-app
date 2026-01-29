# QA Report

## PKG-11 Marine Loading System Estimate

### Snapshot Information

| Field | Value |
|-------|-------|
| Snapshot ID | EST_PKG11_DRAFT_2026-01-28_2359 |
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
| LineID unique | PASS | L001-L028 unique |
| CBS assigned | PASS | All lines have CBS code |
| SourceRef populated | PASS | All lines reference A-### or D-### |

### Arithmetic Reconciliation

| CBS | Detail.csv Sum | Summary.md Total | Variance | Status |
|-----|----------------|------------------|----------|--------|
| E | $125,000 | $125,000 | $0 | PASS |
| MAT | $1,485,000 | $1,485,000 | $0 | PASS |
| CD | $595,000 | $595,000 | $0 | PASS |
| CI | $107,000 | $107,000 | $0 | PASS |
| PM | $119,000 | $119,000 | $0 | PASS |
| P | $30,000 | $30,000 | $0 | PASS |
| COM | $79,000 | $79,000 | $0 | PASS |
| **BASE TOTAL** | **$2,540,000** | **$2,540,000** | **$0** | **PASS** |

### Coverage Check

| Deliverable | Has Cost Lines | Status |
|-------------|----------------|--------|
| DEL-11.01 | Yes (L001) | Covered |
| DEL-11.02 | Yes (L002) | Covered |
| DEL-11.03 | Yes (L003) | Covered |
| DEL-11.04 | Yes (L004) | Covered |
| DEL-11.05 | Yes (L005) | Covered |
| DEL-11.06 | Yes (L006) | Covered |
| Marine Loading Arm scope | Yes (L007, L015) | Covered |
| Double-Walled Pipe scope | Yes (L008, L016) | Covered |
| Leak Detection scope | Yes (L009, L017) | Covered |
| Sump scope | Yes (L010, L018) | Covered |
| Operator Shelter scope | Yes (L011, L019) | Covered |
| Nitrogen Connection scope | Yes (L012, L020) | Covered |
| Pipe Supports scope | Yes (L013, L023) | Covered |
| E&I scope | Yes (L014, L021, L022) | Covered |
| Testing | Yes (L024) | Covered |
| Indirects | Yes (L025-L028) | Covered |

**Coverage Result:** All 6 deliverables have associated cost lines. All scope elements from decomposition are covered. No uncovered scope.

### Double-Count Check

| Potential Overlap | Lines | Assessment |
|-------------------|-------|------------|
| Loading arm supply vs installation | L007, L015 | Distinct - equipment supply vs installation labor |
| Pipe supply vs installation | L008, L016 | Distinct - material supply vs fabrication/installation |
| Leak detection supply vs install | L009, L017 | Distinct - equipment vs installation/wiring |
| E&I materials vs electrical install vs I&C install | L014, L021, L022 | Distinct - materials vs power install vs I&C install |
| Testing in CD vs COM | L024, L028 | L024 is construction QC; L028 is commissioning/acceptance |

**Double-Count Result:** No double-counting identified.

### Unknowns List (Top Assumptions by Value)

| Rank | Assumption ID | Description | Amount | % of Base |
|------|---------------|-------------|--------|-----------|
| 1 | A-001 | Marine loading arm (supply + install) | $1,070,000 | 42.1% |
| 2 | A-002 | Double-walled pipe (supply + install) | $405,000 | 15.9% |
| 3 | A-014 | E&I (supply + install) | $165,000 | 6.5% |
| 4 | A-003 | Leak detection (supply + install) | $120,000 | 4.7% |
| 5 | D-008 | Project Management/EPCM | $119,000 | 4.7% |
| 6 | D-008 | Construction Indirects | $107,000 | 4.2% |
| 7 | A-005 | Operator shelter (supply + install) | $100,000 | 3.9% |
| 8 | A-013 | Pipe supports (supply + install) | $80,000 | 3.1% |
| | | **Top 8 Total** | **$2,166,000** | **85.3%** |

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
| No loading arm OEM quotes | HIGH | Largest cost element (37%) has ±40% uncertainty | Obtain budgetary quotes from marine loading arm OEMs |
| No berth layout drawings | HIGH | Pipe routing assumed at 150 lm; may vary significantly | Complete DEL-11.01 drawings with routing |
| No design vessel data | HIGH | Loading arm envelope calculations cannot be verified | Provide vessel manifold data for DEL-11.03 |
| No leak detection specification | MEDIUM | System scope assumed | Complete DEL-11.02 leak detection requirements |
| Deliverables in INITIALIZED state | MEDIUM | Scope not finalized | Progress deliverables to IN_PROGRESS |
| No rate tables | MEDIUM | Labor rates assumed | Provide project rate library |
| Marine interface undefined | MEDIUM | PKG-08 foundation interface not defined | Coordinate with PKG-08 for foundation requirements |
| Long-lead equipment | MEDIUM | Loading arm lead time (6-12 months) may impact schedule | Early procurement planning |

### Mapping Ambiguities

| Deliverable | CBS Assignment | Ambiguity | Resolution |
|-------------|----------------|-----------|------------|
| DEL-11.05 (Records) | E | Could be CD (construction QC) or E (documentation) | Assigned to E as document compilation |
| Testing (L024) | CD | Could be COM (commissioning) | Assigned to CD as construction QC; COM is separate |
| E&I installation | CD | Could be separate EI bucket | Assigned to CD; no separate EI bucket used |

### QA Summary

| Category | Status |
|----------|--------|
| Schema compliance | PASS |
| Arithmetic | PASS |
| Coverage | PASS |
| Completeness | FAIL (100% allowances) |
| Overall | WARNINGS |

**Recommendation:** This estimate provides placeholder budget coverage for PKG-11 but requires significant input improvement before use for decision-making. Priority actions:
1. Obtain budgetary quotes from marine loading arm OEMs (FMC Technologies, SVT, Emco Wheaton)
2. Complete berth/jetty layout to confirm pipe routing length and loading arm position (DEL-11.01)
3. Obtain design vessel data (manifold heights, beam, positions) for envelope calculations (DEL-11.03)
4. Develop OEM qualification requirements (DEL-11.06) to support early procurement
5. Coordinate with PKG-08 for loading arm foundation requirements
6. Progress deliverables from INITIALIZED to IN_PROGRESS with defined scope
