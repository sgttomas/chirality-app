# QA Report

## PKG-14 Process Piping Estimate

### Snapshot Information

| Field | Value |
|-------|-------|
| Snapshot ID | EST_PKG14_DRAFT_2026-01-28_2400 |
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
| LineID unique | PASS | L001-L036 unique |
| CBS assigned | PASS | All lines have CBS code |
| SourceRef populated | PASS | All lines reference A-### or D-### |

### Arithmetic Reconciliation

| CBS | Detail.csv Sum | Summary.md Total | Variance | Status |
|-----|----------------|------------------|----------|--------|
| E | $515,000 | $515,000 | $0 | PASS |
| MAT | $2,125,000 | $2,125,000 | $0 | PASS |
| CD | $1,975,000 | $1,975,000 | $0 | PASS |
| CI | $359,000 | $359,000 | $0 | PASS |
| PM | $298,000 | $298,000 | $0 | PASS |
| P | $42,000 | $42,000 | $0 | PASS |
| COM | $136,000 | $136,000 | $0 | PASS |
| **BASE TOTAL** | **$5,450,000** | **$5,450,000** | **$0** | **PASS** |

### Coverage Check

| Deliverable | Has Cost Lines | Status |
|-------------|----------------|--------|
| DEL-14.01 | Yes (L001) | Covered |
| DEL-14.02 | Yes (L002) | Covered |
| DEL-14.03 | Yes (L003) | Covered |
| DEL-14.04 | Yes (L004) | Covered |
| DEL-14.05 | Yes (L005) | Covered |
| DEL-14.06 | Yes (L006) | Covered |
| DEL-14.07 | Yes (L007) | Covered |
| DEL-14.08 | Yes (L008) | Covered |
| Rail Unloading Header scope | Yes (L009, L010, L021, L022) | Covered |
| Tank Farm Piping scope | Yes (L011, L012, L023) | Covered |
| Export Piping scope | Yes (L013, L024) | Covered |
| Recycle Piping scope | Yes (L014, L025) | Covered |
| Nitrogen Distribution scope | Yes (L015, L026) | Covered |
| Small Bore Utility scope | Yes (L016, L027) | Covered |
| Pipe Supports scope | Yes (L017, L028) | Covered |
| Insulation/Heat Trace scope | Yes (L018, L029) | Covered |
| Testing/NDE scope | Yes (L030, L031) | Covered |
| Gaskets/Bolting/Expansion | Yes (L019, L020) | Covered |
| Specialty Work | Yes (L032) | Covered |
| Indirects | Yes (L033-L036) | Covered |

**Coverage Result:** All 8 deliverables have associated cost lines. All scope elements from decomposition are covered. No uncovered scope.

### Double-Count Check

| Potential Overlap | Lines | Assessment |
|-------------------|-------|------------|
| Header supply vs installation | L009-L010, L021-L022 | Distinct - material supply vs fabrication/installation labor |
| Pipe supply vs installation (all systems) | L011-L016, L023-L027 | Distinct - material vs labor |
| Insulation supply vs install | L018, L029 | Distinct - material vs labor |
| Testing in CD vs COM | L030-L031, L036 | L030-L031 is construction hydro/NDE; L036 is commissioning flushing |
| Supports supply vs install | L017, L028 | Distinct - fabricated steel vs installation |
| Gaskets/bolts vs piping | L019 vs pipe lines | Distinct - small fittings vs main pipe |

**Double-Count Result:** No double-counting identified.

### Unknowns List (Top Assumptions by Value)

| Rank | Assumption ID | Description | Amount | % of Base |
|------|---------------|-------------|--------|-----------|
| 1 | A-001 | Rail unloading header system | $815,000 | 15.0% |
| 2 | A-003 | Export piping system | $770,000 | 14.1% |
| 3 | A-002 | Tank farm piping | $650,000 | 11.9% |
| 4 | A-008 | Insulation & heat trace | $430,000 | 7.9% |
| 5 | A-007 | Pipe supports | $360,000 | 6.6% |
| 6 | D-010 | Construction Indirects | $359,000 | 6.6% |
| 7 | D-010 | Project Management/EPCM | $298,000 | 5.5% |
| 8 | A-005 | Nitrogen distribution | $280,000 | 5.1% |
| | | **Top 8 Total** | **$3,962,000** | **72.7%** |

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
| No P&IDs or piping GAs | HIGH | Quantities are parametric estimates; ±30% variance possible | Complete DEL-14.01 P&IDs and GAs |
| No line list | HIGH | Pipe sizes and materials assumed | Complete DEL-14.04 line list |
| No stress analysis | HIGH | Support quantities and expansion provisions uncertain | Complete DEL-14.03 stress analysis |
| No transient studies | HIGH | Surge protection requirements unknown | Complete DEL-14.06, DEL-14.07 |
| No hydraulic calculations | MEDIUM | Header and export pipe sizes assumed | Complete DEL-14.03 sizing calculations |
| No pipe material quotes | MEDIUM | Large diameter pipe pricing uncertain | Obtain supplier quotes |
| Multiple interface packages | MEDIUM | PKG-10, PKG-11, PKG-13, PKG-15, PKG-16 interfaces undefined | Coordinate interface definitions |
| Deliverables in INITIALIZED state | MEDIUM | Scope not finalized | Progress deliverables to IN_PROGRESS |
| No rate tables | MEDIUM | Labor rates assumed | Provide project rate library |
| Insulation scope uncertain | MEDIUM | May not need all lines insulated | Confirm insulation requirements |

### Mapping Ambiguities

| Deliverable | CBS Assignment | Ambiguity | Resolution |
|-------------|----------------|-----------|------------|
| DEL-14.05 (Records) | E | Could be CD (construction QC) or E (documentation) | Assigned to E as document compilation |
| DEL-14.06/07 (Transient) | E | Could be separate specialist bucket | Assigned to E as engineering studies |
| Testing (L030-L031) | CD | Could be COM (commissioning) | Assigned to CD as construction QC; COM is system commissioning |
| Pipe supports (L017, L028) | Separate from MAT, CD | Could be combined with structural steel | Assigned to MAT/CD per PKG-14 scope |

### QA Summary

| Category | Status |
|----------|--------|
| Schema compliance | PASS |
| Arithmetic | PASS |
| Coverage | PASS |
| Completeness | FAIL (100% allowances) |
| Overall | WARNINGS |

**Recommendation:** This estimate provides placeholder budget coverage for PKG-14 but requires significant input improvement before use for decision-making. Priority actions:
1. Complete P&IDs and piping GAs (DEL-14.01) to establish routing and quantities
2. Develop line list (DEL-14.04) with sizes, materials, and service conditions
3. Complete stress analysis (DEL-14.03) to confirm expansion provisions and supports
4. Complete transient studies (DEL-14.06, DEL-14.07) to identify surge protection needs
5. Coordinate interfaces with PKG-10 (headers), PKG-11 (export), PKG-13 (tanks), PKG-15 (pumps)
6. Obtain budgetary quotes from pipe suppliers for large diameter material
7. Progress deliverables from INITIALIZED to IN_PROGRESS with defined scope
