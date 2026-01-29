# Risk Register

## Snapshot Identification

| Field | Value |
|-------|-------|
| Snapshot ID | EST_PKG03_DRAFT_2026-01-28_2330 |
| Package | PKG-03 Underground Utilities & Drainage |
| Date | 2026-01-28 |

## Contingency Summary

| CBS Bucket | Base Cost | Base % | Allowance Adj | Final % | Contingency Amount | Rationale |
|------------|-----------|--------|---------------|---------|-------------------|-----------|
| E | $232,000 | 10% | +10% | 20% | $46,000 | 100% allowance-based engineering hours; no labor hour breakdown |
| MAT | $570,000 | 15% | +10% | 25% | $143,000 | 100% allowance-based materials; no vendor quotes or quantities |
| CD | $975,000 | 20% | +10% | 30% | $293,000 | 100% allowance-based construction; no site-specific productivity data |
| CI | $176,000 | 20% | +10% | 30% | $53,000 | Factor-derived from CD; indirects uncertainty follows CD uncertainty |
| P | $11,000 | 10% | +5% | 15% | $2,000 | Factor-derived; procurement scope typical |
| PM | $103,000 | 10% | +5% | 15% | $15,000 | Factor-derived; PM scope typical |
| COM | $52,000 | 25% | +5% | 30% | $16,000 | Factor-derived; commissioning scope has execution uncertainty |
| **TOTAL** | **$2,119,000** | | | **27%** | **$568,000** | Elevated contingency due to 100% allowance-based estimate |

**Contingency Method:** PCT_BY_BUCKET per config (Decision D-006)

**Allowance Share by Bucket:**
- E: 100% (all engineering lines are ALLOWANCE)
- MAT: 100% (all material lines are ALLOWANCE)
- CD: 100% (all construction lines are ALLOWANCE)
- CI, P, PM, COM: 100% (all factor-derived from allowance bases)

---

## Risk Entries

### R-001: Scope Definition Uncertainty

**Risk Driver:** Scope / Quantity

**Cause → Consequence:**
- All deliverables in INITIALIZED status; no design quantities available
- → Allowance-based estimate may under-represent or over-represent actual scope
- → Estimate may vary -30% to +50% from actual costs when design matures

**Affected Buckets:**
- WBS: All PKG-03 deliverables
- CBS: All buckets (E, MAT, CD, CI, P, PM, COM)

**Suggested Mitigation:**
1. Prioritize DEL-03.01 drawing development to establish storm drainage layout, OWS location, duct bank routing, trenchless crossing details
2. Complete DEL-03.03 calculations to size OWS, drainage pipes, duct bank capacity
3. Re-run estimate when design quantities are available (Class 4 accuracy achievable with 60% design completion)

**Contingency Handling:** Base contingency rates (10-25% by bucket) plus +10% allowance adjustment applied; total 27% contingency

---

### R-002: Storm Drainage Extent Uncertainty

**Risk Driver:** Scope / Quantity

**Cause → Consequence:**
- Storm drainage scope estimated at 800-1200 LM based on typical facility layout (Assumption A-001)
- → If actual drainage area or pipe routing is more extensive (e.g., additional tank farm drainage, railcar unloading area expansion, marine platform runoff), pipe lengths may increase 20-40%
- → Materials (MAT) and construction (CD) costs may increase $100k-$200k

**Affected Buckets:**
- WBS: DEL-03.01, 03.02, 03.05
- CBS: MAT (storm drainage pipe), CD (storm drainage installation)

**Suggested Mitigation:**
1. Develop preliminary site drainage plan showing drainage areas and flow paths
2. Coordinate with PKG-02 site grading to confirm finished grades and drainage flow directions
3. Identify tie-ins to existing terminal storm drainage system (if any)
4. Update estimate when DEL-03.01 preliminary layout is available

**Contingency Handling:** 25% contingency on MAT and 30% on CD partially covers scope growth; monitor during design development

---

### R-003: OWS Sizing and Equipment Selection Uncertainty

**Risk Driver:** Scope / Price

**Cause → Consequence:**
- OWS treatment capacity estimated at 50-100 L/s; separator volume 10-20 m³ (Assumption A-003)
- → If actual runoff volumes or spill containment requirements are higher (e.g., larger contributing drainage area, more stringent regulatory requirements per A-023), OWS capacity may increase 30-50%
- → If more stringent discharge limits exist (e.g., <10 mg/L oil instead of <15 mg/L), enhanced treatment technology may be required (coalescing plates, media filtration)
- → OWS equipment costs may increase $50k-$100k; installation costs may increase $20k-$40k

**Affected Buckets:**
- WBS: DEL-03.02, 03.03, 03.04, 03.05
- CBS: MAT (OWS equipment), CD (OWS installation), COM (OWS performance testing)

**Suggested Mitigation:**
1. Complete DEL-03.03 OWS sizing calculations using peak runoff and spill volumes
2. Obtain environmental discharge permit requirements from Employer
3. Request budgetary quotes from OWS equipment vendors with specified treatment capacity and discharge limits
4. Coordinate with environmental team to confirm regulatory compliance requirements (OBJ-7)

**Contingency Handling:** 25% contingency on MAT OWS equipment allowance provides $34k reserve; monitor OWS sizing as design progresses

---

### R-004: Trenchless Crossing Count and Complexity Uncertainty

**Risk Driver:** Scope / Productivity

**Cause → Consequence:**
- Trenchless crossing count estimated at 4-8 crossings (Assumption A-005)
- → If actual rail track crossings, road crossings, or existing utility conflicts are more numerous or more complex (e.g., longer crossing lengths, larger casing sizes, difficult boring conditions), crossing count or unit costs may increase 30-60%
- → Mobilization for additional crossings adds $25k-$50k per crossing
- → Difficult boring conditions (cobbles, groundwater, existing buried obstructions) may require more expensive boring methods (e.g., microtunneling instead of auger boring)
- → Trenchless crossing costs may increase $100k-$200k

**Affected Buckets:**
- WBS: DEL-03.01, 03.02
- CBS: CD (trenchless boring services)

**Suggested Mitigation:**
1. Develop DEL-03.01 preliminary site plan showing all underground utility routes and crossing locations
2. Conduct utility locates and survey to identify existing buried utilities and potential conflicts
3. Coordinate with rail operator and roadway authorities for crossing permits and requirements
4. Obtain budgetary quotes from trenchless boring contractors for project-specific conditions
5. Consider value engineering alternatives (e.g., open-cut crossings with traffic management if permissible)

**Contingency Handling:** 30% contingency on CD trenchless allowance provides $80k reserve; trenchless crossings are high-risk activity, monitor closely

---

### R-005: Duct Bank Coordination with Electrical (PKG-17)

**Risk Driver:** Interface / Scope

**Cause → Consequence:**
- Duct bank scope estimated at 400-600 LM with 4-8 conduits per bank (Assumption A-004)
- → If PKG-17 electrical design requires more conduits (e.g., more circuits, redundancy, future capacity), conduit count may increase 20-40%
- → If electrical routing changes during design coordination, duct bank routes may change, affecting trench lengths and congestion
- → Duct bank materials and installation costs may increase $40k-$80k

**Affected Buckets:**
- WBS: DEL-03.01, 03.02 (duct bank scope coordination with PKG-17 per Specification IF-1)
- CBS: MAT (duct bank materials), CD (duct bank installation)

**Suggested Mitigation:**
1. Coordinate DEL-03.01 duct bank plan development with PKG-17 electrical design early in design phase
2. Obtain preliminary conduit schedule from PKG-17 electrical engineer
3. Hold coordination meeting to align duct bank routing, pull box locations, and separation requirements
4. Update duct bank estimate when PKG-17 electrical design reaches 30% completion

**Contingency Handling:** 25% contingency on MAT duct bank materials and 30% on CD duct bank installation provides $35k reserve; early coordination critical to manage interface risk

---

### R-006: Site Soil Conditions and Geotechnical Uncertainty

**Risk Driver:** Productivity / Price

**Cause → Consequence:**
- Soil conditions assumed typical Fraser River delta (soft silty soils, high groundwater) (Assumption A-008)
- → If actual soil conditions are worse than assumed (e.g., very soft soils requiring extensive shoring, contaminated soils requiring disposal, buried obstructions, artesian groundwater), excavation support and dewatering costs may increase significantly
- → Shoring/dewatering may add 20-40% to excavation costs instead of assumed 15-25%
- → Contaminated soil disposal may add $50k-$150k if encountered
- → CD costs may increase $100k-$250k

**Affected Buckets:**
- WBS: All construction-related deliverables
- CBS: CD (excavation, shoring, dewatering, backfill)

**Suggested Mitigation:**
1. Complete geotechnical investigation for PKG-03 utility corridors (borings, soil classification, groundwater monitoring)
2. Conduct contamination screening if site history indicates potential contamination
3. Develop excavation support plan based on geotechnical data (shoring design, dewatering design)
4. Include geotechnical allowance or contingency for unexpected conditions
5. Update estimate when geotechnical report is available

**Contingency Handling:** 30% contingency on CD provides $293k reserve; geotechnical unknowns are major risk driver for underground work

---

### R-007: Regulatory and Permitting Requirements Uncertainty

**Risk Driver:** Scope / Schedule

**Cause → Consequence:**
- Environmental protection requirements (OBJ-7) include OWS discharge limits, containment systems, stormwater pollution prevention (Assumptions A-019, A-023)
- → If regulatory requirements are more stringent than assumed (e.g., Metro Vancouver stormwater source control requirements, Fisheries Act fish habitat protection, higher treatment standards), scope may expand
- → Additional erosion/sediment controls, enhanced OWS treatment, outfall diffusers, or monitoring systems may be required
- → Permitting delays may extend schedule and increase indirects (CI, PM)
- → MAT, CD, CI, PM costs may increase $50k-$150k

**Affected Buckets:**
- WBS: DEL-03.02, 03.03, 03.04 (OWS and environmental protection requirements)
- CBS: MAT (additional equipment), CD (additional controls installation), CI (extended duration), PM (permitting coordination)

**Suggested Mitigation:**
1. Obtain environmental discharge permit requirements from Employer early in design phase
2. Extract environmental protection requirements from Employer's Requirements Volume 2 Part 2
3. Engage environmental consultant if specialized expertise is required for permit applications or compliance demonstration
4. Coordinate with Employer and regulatory agencies (Metro Vancouver, BC Ministry of Environment) for permit approvals timeline

**Contingency Handling:** Contingency provides reserve for moderate scope growth; significant regulatory changes may require estimate update and cost review with Employer

---

### R-008: Schedule and Productivity Uncertainty

**Risk Driver:** Productivity / Schedule

**Cause → Consequence:**
- Construction productivity assumed standard for BC Lower Mainland (factor 1.0) (Assumption A-007)
- → If site access restrictions, terminal operations coordination (OBJ-5), or working hour limitations reduce productivity 10-30%, construction duration may extend
- → Seasonal constraints (wet season October-March per A-020) may further reduce productivity or limit work windows
- → CD duration increases → CI and PM costs increase due to extended supervision and management
- → Total project cost may increase $50k-$150k

**Affected Buckets:**
- WBS: All construction-related deliverables
- CBS: CD (direct labor hours increase), CI (extended supervision), PM (extended management)

**Suggested Mitigation:**
1. Develop detailed construction schedule with productivity assumptions documented
2. Coordinate with DP World terminal operations for access windows and working hour restrictions
3. Plan underground utilities installation during dry season (April-September) to minimize wet weather impacts
4. Include schedule float for terminal coordination delays

**Contingency Handling:** 30% contingency on CD and CI provides reserve for moderate productivity reductions; significant schedule delays may require project-level mitigation (acceleration, overtime, additional crews)

---

## Risk Quantification

**Total Base Estimate:** $2,119,000 CAD

**Total Contingency:** $568,000 CAD (27% of base)

**Estimate Total:** $2,687,000 CAD (rounded to $2,690,000)

**Confidence Level:** LOW (Class 5 / Order of Magnitude estimate)

**Expected Range:**
- Low (-30%): $1,880,000 CAD
- Most Likely (base + contingency): $2,690,000 CAD
- High (+50%): $4,000,000 CAD

**Primary Risk Drivers (by impact magnitude):**
1. **Scope definition uncertainty (R-001):** Affects all buckets; -30% to +50% range
2. **Geotechnical and soil conditions (R-006):** Affects CD; potential +$100k-$250k
3. **Trenchless crossing complexity (R-004):** Affects CD; potential +$100k-$200k
4. **Storm drainage extent (R-002):** Affects MAT and CD; potential +$100k-$200k
5. **OWS sizing and regulatory requirements (R-003, R-007):** Affects MAT and CD; potential +$50k-$150k
6. **Schedule and productivity (R-008):** Affects CD, CI, PM; potential +$50k-$150k
7. **Duct bank coordination with PKG-17 (R-005):** Affects MAT and CD; potential +$40k-$80k

**Contingency Allocation by Risk Driver:**
- Scope/quantity risks (R-001, R-002, R-003, R-004, R-005): $480k contingency allocated (84% of total)
- Geotechnical/productivity risks (R-006, R-008): $60k contingency allocated (11% of total)
- Regulatory/schedule risks (R-007, R-008): $28k contingency allocated (5% of total)

**Contingency Adequacy:**
- Current contingency ($568k) provides coverage for **moderate scope growth and moderate execution challenges**
- Contingency may be insufficient if **multiple high-impact risks materialize concurrently** (e.g., extensive trenchless crossings + difficult geotechnical + stringent regulatory requirements)
- Recommend estimate update at 30% design completion to refine scope and contingency

---

## Risk Mitigation Recommendations

| Priority | Action | Owner | Timing | Cost Impact |
|----------|--------|-------|--------|-------------|
| 1 | Complete DEL-03.01 preliminary drawings (30% design) | Civil Engineering | Design Phase Month 1-2 | Enables Class 4 estimate |
| 2 | Complete geotechnical investigation for utility corridors | Geotechnical Consultant | Pre-Construction | Reduces R-006 uncertainty; potential +$50k investigation cost |
| 3 | Obtain OWS equipment budgetary quotes | Procurement | Design Phase Month 2 | Reduces R-003 pricing uncertainty |
| 4 | Coordinate duct bank scope with PKG-17 electrical | Civil + Electrical | Design Phase Month 1 | Reduces R-005 interface risk |
| 5 | Obtain environmental discharge permit requirements | Employer / Environmental | Design Phase Month 1 | Reduces R-007 regulatory uncertainty |
| 6 | Obtain trenchless boring contractor budgetary quotes | Procurement | Design Phase Month 2-3 | Reduces R-004 pricing uncertainty |
| 7 | Develop site logistics and access plan | Construction Management | Pre-Construction | Reduces R-008 productivity uncertainty |
| 8 | Extract design criteria from ER Volume 2 Part 2 | Engineering | Design Phase Month 1 | Reduces A-022 design parameter uncertainty |

---

## Contingency Drawdown Plan (Conceptual)

As design matures and risks are mitigated, contingency may be reallocated or released:

| Design Stage | Expected Contingency % | Rationale |
|--------------|------------------------|-----------|
| Current (INITIALIZED) | 27% | 100% allowance-based; Class 5 accuracy |
| 30% Design | 22-25% | Quantities defined; vendor budgets available; Class 4 accuracy |
| 60% Design | 18-22% | Detailed quantities; firm quotes; geotechnical data; Class 3 accuracy |
| 90% Design / IFC | 12-18% | Final quantities; contracted pricing; site conditions confirmed; Class 2 accuracy |
| Construction | 8-12% | Execution risks only; materials procured; installation rates confirmed |

**Note:** Contingency drawdown assumes successful risk mitigation and no major scope changes. Contingency release requires Employer approval and project-level cost review.

---
