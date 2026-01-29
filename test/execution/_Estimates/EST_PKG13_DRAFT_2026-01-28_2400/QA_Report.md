# QA Report

## PKG-13 Storage Tanks Estimate

### Snapshot Identification

| Field | Value |
|-------|-------|
| Snapshot ID | EST_PKG13_DRAFT_2026-01-28_2400 |
| Estimate Label | PKG13_DRAFT |
| Date | 2026-01-28 |
| Run Status | WARNINGS |

---

## QA Checks

### Currency Consistency

| Check | Result |
|-------|--------|
| Single currency used | PASS |
| Currency | CAD |
| Mixed currencies | None |
| Conversion applied | N/A |

---

### Required Fields Check

| Check | Result | Notes |
|-------|--------|-------|
| All lines have LineID | PASS | L001-L037 |
| All lines have CBS | PASS | E, MAT, CD, CI, PM, P, COM |
| All lines have WBS_PackageID | PASS | All PKG-13 |
| All lines have WBS_DeliverableID | PASS | DEL-13.xx or N/A |
| All lines have Description | PASS | Descriptive text present |
| All lines have Qty | PASS | All = 1 (LS items) |
| All lines have Unit | PASS | All = LS |
| All lines have UnitRate | PASS | All populated |
| All lines have Amount | PASS | All = UnitRate × Qty |
| All lines have Currency | PASS | All = CAD |
| All lines have Method | PASS | ALLOWANCE or PARAMETRIC |
| All lines have SourceRef | PASS | A-xxx or D-xxx references |
| All lines have Confidence | PASS | LOW or MED |
| All lines have Notes | PASS | Context provided |

---

### Arithmetic Reconciliation

| Check | Detail Amount | Summary Amount | Variance | Result |
|-------|---------------|----------------|----------|--------|
| Engineering (E) | $580,000 | $580,000 | $0 | PASS |
| Materials (MAT) | $11,855,000 | $11,855,000 | $0 | PASS |
| Construction Directs (CD) | $5,100,000 | $5,100,000 | $0 | PASS |
| Construction Indirects (CI) | $918,000 | $918,000 | $0 | PASS |
| Project Management (PM) | $1,020,000 | $1,020,000 | $0 | PASS |
| Procurement (P) | $237,000 | $237,000 | $0 | PASS |
| Commissioning (COM) | $535,000 | $535,000 | $0 | PASS |
| **Base Total** | **$20,245,000** | **$20,245,000** | **$0** | **PASS** |

---

### Coverage Check

| Deliverable | Line Items | Status |
|-------------|------------|--------|
| DEL-13.01 Storage Tank Design Drawing Set | L001 | Covered |
| DEL-13.02 Storage Tank Technical Specification | L002 | Covered |
| DEL-13.03 Storage Tank Design Calculations | L003 | Covered |
| DEL-13.04 Storage Tank Data Sheet Package | L004 | Covered |
| DEL-13.05 Storage Tank Installation & Test Records | L005 | Covered |
| DEL-13.06 Storage Tank Fabrication Quality Documentation Package | L006 | Covered |
| Tank Supply | L007-L009 | Covered (3 tanks) |
| Agitators | L010-L012 | Covered (3 agitators) |
| Overflow Protection | L013 | Covered |
| Water Draw-off | L014 | Covered |
| Coatings | L015-L016 | Covered (internal + external) |
| Appurtenances | L017 | Covered |
| Access Equipment | L018 | Covered |
| Phase 2 Provisions | L019 | Covered |
| Tank Erection | L020-L022 | Covered (3 tanks) |
| Hydrostatic Tests | L023-L025 | Covered (3 tanks) |
| Agitator Installation | L026 | Covered |
| NDE and Inspection | L027 | Covered |
| Installation Items | L028-L032 | Covered |
| Heavy Equipment | L033 | Covered |
| Indirects | L034 | Covered |
| PM/EPCM | L035 | Covered |
| Procurement | L036 | Covered |
| Commissioning | L037 | Covered |

**Coverage Result:** All 6 deliverables have associated line items. All major scope elements covered.

---

### Double Count Check

| Potential Double Count | Assessment |
|------------------------|------------|
| Tank supply vs coating | DISTINCT: Tank supply is steel; coating is separate line items |
| Engineering vs fabrication QA | DISTINCT: DEL-13.06 is documentation; NDE is field inspection |
| Agitator supply vs installation | DISTINCT: Separate line items |
| Appurtenances vs tank supply | DISTINCT: Tank supply is shell/bottom/roof; appurtenances are separate |

**Double Count Result:** No double counts identified.

---

### Mapping Ambiguities

| Item | CBS Assigned | Ambiguity | Resolution |
|------|--------------|-----------|------------|
| Electrical installation | CD | Could be E&I separate bucket | Assigned to CD as field installation work |
| Instrumentation installation | CD | Could be E&I separate bucket | Assigned to CD as field installation support |
| Crane equipment | CD | Could be CI | Assigned to CD as direct erection support |

---

### Completeness Metrics

| Metric | Value | Notes |
|--------|-------|-------|
| Lines priced by QUOTE | 0 (0%) | No vendor quotes available |
| Lines priced by RATE_TABLE | 0 (0%) | No rate tables provided |
| Lines priced by ALLOWANCE | 33 (89%) | Direct scope items |
| Lines priced by PARAMETRIC | 4 (11%) | CI, PM, P, COM factor-based |
| Deliverables with explicit quantities | 0 (0%) | All quantities are assumptions |
| Total line items | 37 | Complete coverage |

---

### Unknowns List (Top Assumptions by Value)

| Rank | Assumption | Item | Cost Impact | Confidence |
|------|------------|------|-------------|------------|
| 1 | A-001 | Tank sizing and weight | $9.6M (supply) + $2.55M (erection) | LOW |
| 2 | A-005 | Steel weight ~420 tonnes/tank | $7,600/tonne fabricated | LOW |
| 3 | A-025 | Crane requirements | $420k | LOW |
| 4 | A-006 | Agitator configuration | $375k (supply) + $95k (install) | LOW |
| 5 | A-009 | Internal coating area | $550k | MEDIUM |
| 6 | A-022 | NDE scope | $280k | MEDIUM |

---

## Known Issues

| Issue | Severity | Impact | Recommended Action |
|-------|----------|--------|-------------------|
| No vendor quotes | HIGH | All pricing is allowance-based | Obtain budgetary quotes from tank fabricators |
| Tank geometry not finalized | HIGH | Steel weight and erection cost uncertain | Complete DEL-13.03 design calculations |
| Agitator selection TBD | MEDIUM | Equipment cost and installation uncertain | Complete agitator selection |
| Seismic design not complete | MEDIUM | May increase tank weight and anchorage | Complete seismic analysis per API 650 App E |
| Foundation interface TBD | MEDIUM | Coordination with PKG-05 required | Define foundation interface requirements |
| Deliverables in INITIALIZED state | MEDIUM | Scope not finalized | Progress deliverables to IN_PROGRESS |

---

## Run Status Assessment

| Criterion | Result |
|-----------|--------|
| All required files produced | PASS |
| Traceability complete | PASS |
| Required fields populated | PASS |
| Arithmetic reconciled | PASS |
| Coverage adequate | PASS |
| Critical gaps exist | YES (no quotes, geometry TBD) |
| Confidence level | LOW |

**Run Status:** WARNINGS

**Rationale:** Estimate is structurally complete but relies entirely on allowances with LOW confidence. No vendor quotes or rate tables. Tank geometry and steel weight are assumptions. Estimate is suitable for early budget purposes only; significant refinement needed before commitment.

---

## Recommendations

1. **Immediate:** Obtain budgetary quotes from API 650 tank fabricators
2. **Immediate:** Complete DEL-13.03 design calculations for tank geometry and steel weight
3. **Near-term:** Obtain agitator quotes from OEM suppliers
4. **Near-term:** Complete seismic analysis for Surrey, BC location
5. **Near-term:** Coordinate with PKG-05 for foundation interface
6. **Ongoing:** Progress deliverables from INITIALIZED to IN_PROGRESS
7. **Next estimate:** Replace allowances with quotes; target >50% quote-based pricing
