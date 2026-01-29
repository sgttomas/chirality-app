# QA Report

## PKG-07 Rail Works Estimate

### Snapshot Information

| Field | Value |
|-------|-------|
| Snapshot ID | EST_PKG07_DRAFT_2026-01-28_2332 |
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
| LineID unique | PASS | L001-L023 unique |
| CBS assigned | PASS | All lines have CBS code |
| SourceRef populated | PASS | All lines reference A-### or D-### |

### Arithmetic Reconciliation

| CBS | Detail.csv Sum | Summary.md Total | Variance | Status |
|-----|----------------|------------------|----------|--------|
| E | $45,000 | $45,000 | $0 | PASS |
| MAT | $898,000 | $898,000 | $0 | PASS |
| CD | $468,000 | $468,000 | $0 | PASS |
| CI | $84,000 | $84,000 | $0 | PASS |
| PM | $87,000 | $87,000 | $0 | PASS |
| P | $18,000 | $18,000 | $0 | PASS |
| COM | $44,000 | $44,000 | $0 | PASS |
| **BASE TOTAL** | **$1,644,000** | **$1,644,000** | **$0** | **PASS** |

### Coverage Check

| Deliverable | Has Cost Lines | Status |
|-------------|----------------|--------|
| DEL-07.01 | Yes (L001) | Covered |
| DEL-07.02 | Yes (L002) | Covered |
| DEL-07.03 | Yes (L003) | Covered |
| DEL-07.04 | Yes (L004) | Covered |
| Construction scope | Yes (L011-L019) | Covered |
| Materials scope | Yes (L005-L010) | Covered |
| Indirects | Yes (L020-L023) | Covered |

**Coverage Result:** All 4 deliverables have associated cost lines. No uncovered scope.

### Double-Count Check

| Potential Overlap | Lines | Assessment |
|-------------------|-------|------------|
| Rail supply vs installation | L005-L006, L011-L012 | Distinct - material supply vs labor |
| Ballast supply vs placement | L009, L013 | Distinct - material vs labor |
| End stops material vs install | L010, L014 | Distinct - equipment vs installation |
| Survey in testing vs standalone | L015, L016 | Distinct - alignment survey vs geometry testing |

**Double-Count Result:** No double-counting identified.

### Unknowns List (Top Assumptions by Value)

| Rank | Assumption ID | Description | Amount | % of Base |
|------|---------------|-------------|--------|-----------|
| 1 | A-005 | Rail supply - new tracks | $350,000 | 21.3% |
| 2 | A-011 | Track ties/sleepers | $195,000 | 11.9% |
| 3 | A-009 | Ballast material | $117,000 | 7.1% |
| 4 | A-007 | Rail supply - Track 5 | $105,000 | 6.4% |
| 5 | A-008 | Rail restoration labor | $75,000 | 4.6% |
| 6 | A-012 | Fasteners & hardware | $91,000 | 5.5% |
| 7 | A-010 | Ballast placement | $78,000 | 4.7% |
| 8 | A-013 | End stops | $60,000 | 3.6% |
| | | **Top 8 Total** | **$1,266,000** | **77.0%** |

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
| No track layout design | HIGH | Track lengths assumed; ±30% uncertainty | Complete design drawings (DEL-07.01) |
| No Track 5 condition assessment | HIGH | Restoration scope unknown | Complete Track 5 survey and condition report |
| No vendor quotes | HIGH | All pricing via allowances | Obtain budgetary quotes for rail and materials |
| No rate tables | MEDIUM | Labor rates assumed | Provide project rate library |
| Deliverables in INITIALIZED state | MEDIUM | Scope not finalized | Progress deliverables to IN_PROGRESS |
| Scope boundaries unclear | MEDIUM | Interface with PKG-02/03/17/34 assumed | Confirm scope splits in ER |
| No rail specification | MEDIUM | Rail type and grade assumed | Develop specification (DEL-07.02) |

### Mapping Ambiguities

| Deliverable | CBS Assignment | Ambiguity | Resolution |
|-------------|----------------|-----------|------------|
| DEL-07.04 (Records) | E | Could be CD (field QC) or E (documentation) | Assigned to E as document compilation |
| Track installation | CD | Could include some MAT components | Split explicitly: rail/ties/fasteners = MAT; labor = CD |
| End stops | MAT + CD | Mixed material and installation | Split: $10k/unit MAT, $5k/unit CD |

### QA Summary

| Category | Status |
|----------|--------|
| Schema compliance | PASS |
| Arithmetic | PASS |
| Coverage | PASS |
| Completeness | FAIL (100% allowances) |
| Overall | WARNINGS |

**Recommendation:** This estimate provides placeholder budget coverage for PKG-07 but requires significant input improvement before use for decision-making. Priority actions:
1. Complete track layout design with actual track lengths (DEL-07.01)
2. Complete track geometry and ballast calculations (DEL-07.03)
3. Develop technical specification for rail type and materials (DEL-07.02)
4. Obtain budgetary quotes for rail supply and specialty rail contractors
5. Confirm scope boundaries with adjacent packages
