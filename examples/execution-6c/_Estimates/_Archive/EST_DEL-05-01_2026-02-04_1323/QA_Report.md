# QA Report

## Snapshot: EST_DEL-05-01_2026-02-04_1323

---

## Run Status: WARNINGS

The estimate completed successfully but has significant warnings due to 100% allowance-based pricing.

---

## QA Checks Performed

### 1. Currency Consistency

| Check | Result | Notes |
|-------|--------|-------|
| Single currency used | PASS | All values in CAD |
| Currency declared in BOE | PASS | CAD documented |
| Conversion assumptions | N/A | No currency conversions required |

### 2. Qty/Unit/UnitRate Completeness

| Check | Result | Notes |
|-------|--------|-------|
| All lines have Qty | PASS | 25/25 lines have Qty populated |
| All lines have Unit | PASS | 25/25 lines have Unit populated |
| All lines have UnitRate | PASS | 25/25 lines have UnitRate populated |
| All lines have Amount | PASS | 25/25 lines have Amount populated |
| Qty x UnitRate = Amount | PASS | Verified for all lines |

### 3. Arithmetic Reconciliation (Detail to Summary)

| Check | Result | Notes |
|-------|--------|-------|
| Detail.csv base total matches Summary.md | PASS | $10,356,000 CAD |
| Detail.csv options total matches Summary.md | PASS | $430,000 CAD |
| Sum of CBS categories matches total | PASS | Categories sum to total |

**Detailed Reconciliation:**

| Category | Detail.csv Sum | Summary.md Value | Match |
|----------|----------------|------------------|-------|
| Engineering & Design (E) | $528,000 | $528,000 | YES |
| Project Management (PM) | $240,000 | $240,000 | YES |
| Construction Directs (CD) | $7,310,000 | $7,310,000 | YES |
| Construction Indirects (CI) | $584,000 | $584,000 | YES |
| Bonding (MAT) | $150,000 | $150,000 | YES |
| Commissioning (COM) | $146,000 | $146,000 | YES |
| Contingency (CONT) | $1,398,000 | $1,398,000 | YES |
| **Base Total** | **$10,356,000** | **$10,356,000** | **YES** |
| Options Total | $430,000 | $430,000 | YES |

### 4. Coverage Check

| Check | Result | Notes |
|-------|--------|-------|
| All Schedule A lines addressed | PASS | 7 lines (1-1 through 1-7) covered |
| Base contract scope covered | PASS | All OSR requirements addressed |
| Addendum 03 requirements covered | PASS | All added requirements included |
| Scope exclusions documented | PASS | Pickled sand building excluded |

### 5. Double Count Heuristics

| Check | Result | Notes |
|-------|--------|-------|
| Generator not in base + options | PASS | Generator in base only (required by Addendum 03) |
| Appliances in Option 6 only | PASS | Not in base |
| Access control vs security distinct | PASS | Options 3 and 4 have separate scopes |

### 6. Traceability Check

| Check | Result | Notes |
|-------|--------|-------|
| All lines have SourceRef | PASS | 25/25 lines have assumption or decision ID |
| All allowances logged | PASS | A-001 through A-025 documented |
| All decisions logged | PASS | D-001 through D-011 documented |

---

## Completeness Metrics

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| % Lines priced by QUOTE | 0% | >50% preferred | WARNING |
| % Lines priced by RATE_TABLE | 0% | >30% preferred | WARNING |
| % Lines priced by ALLOWANCE | 100% | <30% preferred | WARNING |
| % Deliverables with quantities | 20% | >70% preferred | WARNING |
| Assumptions count | 24 | <10 preferred | WARNING |
| Decisions count | 11 | <5 preferred | ACCEPTABLE |
| Coverage | 100% | 100% required | PASS |

---

## Unknowns List (Top Assumptions by Value)

| Rank | Assumption ID | Description | Cost Impact | Confidence |
|------|---------------|-------------|-------------|------------|
| 1 | A-002 | Main building unit cost ($350/SF) | $5,250,000 | LOW |
| 2 | A-001 | Main building area (15,000 SF) | Drives $5,250,000 | LOW |
| 3 | A-005 | Site development cost ($75K/AC) | $900,000 | LOW |
| 4 | A-004 | Cold storage cost ($100/SF) | $600,000 | LOW |
| 5 | A-006 | Service tie-in allowance | $150,000 | LOW |

---

## Mapping Ambiguities

| Item | Ambiguity | Resolution | Decision ID |
|------|-----------|------------|-------------|
| Monthly monitoring fee | Schedule A vs Schedule B treatment unclear | Excluded from Schedule A per Guidance Conflict-02 | D-010 |
| FF&E | Not a named option but permitted as additional | Excluded from base and options per Addendum 03 s1.18 | N/A |
| Service tie-ins | Allowance vs firm pricing decision | Allowance approach selected per Addendum 03 permission | D-011 |

---

## Known Issues

| Issue ID | Description | Impact | Recommended Action |
|----------|-------------|--------|-------------------|
| QA-001 | 100% allowance-based pricing | HIGH - Low estimate confidence (-30%/+50% accuracy) | Obtain subcontractor pricing before final submission |
| QA-002 | Building area estimated | HIGH - Area drives 50%+ of cost | Develop design concept to confirm area |
| QA-003 | No site survey available | MEDIUM - Site conditions unknown | Request geotech report if available |
| QA-004 | No Schedule B to reconcile | MEDIUM - Cannot verify A-B match | Complete DEL-05-02 before finalizing |
| QA-005 | Tax calculation assumptions | LOW - GST rate may vary | Confirm GST rate at submission |

---

## Validation Against Specification Requirements

| Spec Requirement | Status | Notes |
|------------------|--------|-------|
| All 7 pricing lines completed (R-01.2) | SUPPORTED | Lines 1-1 through 1-7 all have values |
| Taxes shown separately (R-02.5) | SUPPORTED | GST calculated separately in Summary |
| Reconciliation to Schedule B (R-03.1, R-03.2) | PENDING | Schedule B (DEL-05-02) not yet complete |
| Addenda reflected (R-04.2) | SUPPORTED | All Addendum 03 requirements priced |
| Scope exclusions applied (R-06.1) | SUPPORTED | Pickled sand building excluded |
| Options priced correctly (R-07.1-R-07.4) | SUPPORTED | All option requirements addressed |

---

## QA Summary

| Category | Pass | Fail | Warning | Pending |
|----------|------|------|---------|---------|
| Schema compliance | 6 | 0 | 0 | 0 |
| Arithmetic | 3 | 0 | 0 | 0 |
| Coverage | 4 | 0 | 0 | 0 |
| Traceability | 3 | 0 | 0 | 0 |
| Completeness metrics | 1 | 0 | 5 | 0 |
| External reconciliation | 0 | 0 | 0 | 1 |
| **Total** | **17** | **0** | **5** | **1** |

---

## QA Disposition

**Status:** WARNINGS

**Rationale:** Estimate is structurally complete and arithmetically correct, but confidence is LOW due to 100% allowance-based pricing. All required artifacts are present. Estimate should be used for budgeting/proposal development only, with the understanding that significant refinement is required before final pricing submission.

**Recommended Actions Before Submission:**
1. Complete DEL-05-02 (Schedule B) and verify A-B reconciliation
2. Obtain subcontractor budget pricing for major cost items
3. Develop design concept to confirm building area
4. Validate unit cost benchmarks against recent Alberta projects
5. Confirm current GST rate

---

*QA Report generated: 2026-02-04*
*Snapshot: EST_DEL-05-01_2026-02-04_1323*
