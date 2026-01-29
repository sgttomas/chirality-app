# Source Index — PKG-30 Commissioning Estimate

**Snapshot ID:** EST_PKG30_DRAFT_2026-01-29_0014
**Date:** 2026-01-29

This index lists all sources discovered and used for pricing and quantity extraction, organized by priority order per AGENT_ESTIMATING methodology.

---

## 1. Explicit Pricing Sources (Vendor Quotes / Budgets)

**Priority:** HIGHEST

**Status:** None available

**Search Locations:**
- `execution/_Estimates/_RateTables/` — No vendor quotes found
- `execution/PKG-30_Commissioning/1_Working/DEL-*/` — No vendor budgets in deliverable _REFERENCES.md files
- Project workspace root — No commissioning vendor quotes located

**Result:** 0% of estimate priced from vendor quotes

**Impact:** Reliance on rate tables, allowances, and parametric methods

---

## 2. Rate Tables / Cost Libraries

**Priority:** HIGH

**Sources Located:**

### 2.1 Commissioning Labor Rates (Typical BC Market Rates)

**Source Type:** Market research / industry rates

**Content:**
- Commissioning Manager: $135/hr fully burdened
- Commissioning Discipline Leads: $115/hr fully burdened
- Field Commissioning Technicians: $85/hr fully burdened
- QA/QC Inspector: $85/hr fully burdened

**Basis:**
- BC industrial labor market rates for 2026
- Fully burdened: includes base wage, benefits, statutory costs, travel, per diem, contractor markup
- Fraser Surrey location (Lower Mainland BC)
- Consistent with previous package estimates

**Confidence:** MEDIUM

**Usage:** Lines L-013 through L-022, L-028 (commissioning team labor)

**Value:** $1,772,000 (37.9% of base estimate)

**Source Reference:** Assumption A-020; Decision D-014

---

### 2.2 Parametric Indirects and Services Factors

**Source Type:** AGENT_ESTIMATING fallback typical model

**Content:**
- Construction Indirects (CI): ~18% of CD
- Project Management (PM): 6% of (CD + CI + MAT)
- Procurement (P): 2% of MAT
- Commissioning (COM): Not factored; priced directly

**Basis:**
- Fallback typical model for EPC/EPCM projects
- Adjusted for project complexity and coordination requirements

**Confidence:** MEDIUM

**Usage:** Lines L-005 (PM), L-006 (P), L-033 through L-037 (CI parametric components)

**Value:** $619,000 (13.2% of base estimate)

**Source Reference:** Decisions D-010, D-011, D-015; AGENT_ESTIMATING fallback model

---

**Rate Table Summary:**
- Total value priced from rate tables: $703,000 (commissioning labor rates only)
- % of estimate: 15.0%
- Confidence: MEDIUM (labor rates), MEDIUM (parametric factors)

---

## 3. Quantity Sources (Deliverable Datasheets, Specifications, Decomposition)

**Priority:** MEDIUM

**Sources Located:**

### 3.1 Project Decomposition

**Source:** `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md`

**Content Extracted:**
- Section 1.1 (Key Parameters):
  - Throughput: 1,000,000 MT/annum
  - Storage: 45,000 MT (3 × 15,000 MT tanks)
  - Railcar unloading: 32 stations on 2 tracks
  - Product: CSD canola oil
- Section 5 PKG-30: Deliverable definitions (DEL-30.01 through DEL-30.08)
- Section 2 (Project Objectives): OBJ-1 through OBJ-10 supported by commissioning

**Quantities Extracted:**
- 32 railcar stations (explicit) → Line L-029
- 3 storage tanks (explicit) → Line L-030
- 8 deliverables requiring engineering/planning (explicit) → Lines L-001 through L-004

**Usage:** WBS structure, deliverable scope definition, system counts

**Confidence:** HIGH (explicit counts), MEDIUM (scope interpretation)

---

### 3.2 Deliverable Datasheets (DEL-30.01 through DEL-30.08)

**Source:** `/Users/ryan/ai-env/projects/chirality-app/test/execution/PKG-30_Commissioning/1_Working/DEL-*/Datasheet.md`

**Content Extracted:**
- DEL-30.01 Datasheet §Construction: Anticipated artifacts (pre-commissioning procedures, commissioning procedures, start-up procedures) → Lines L-001, L-002, L-003
- DEL-30.02 Datasheet §Construction: Commissioning plan content and schedule → Line L-004
- DEL-30.04 Datasheet §Construction: Commissioning records by discipline (mechanical, electrical, I&C) → Multiple CD lines
- DEL-30.05 Datasheet §Construction: IST scenarios (railcar-to-tank, tank-to-ship, direct rail-to-ship, control integration) → Lines L-040 through L-043
- DEL-30.08 Datasheet: Cathodic protection commissioning scope → Line L-031

**Quantities Extracted:**
- Commissioning procedure types and categories (qualitative) → translated to procedure count assumptions
- IST scenario count (4 explicit scenarios)
- CP commissioning as distinct scope

**Usage:** Scope definition, anticipated artifact lists, commissioning activities breakdown

**Confidence:** LOW-MEDIUM (anticipated artifacts listed, but detailed scope TBD)

---

### 3.3 Deliverable Specifications and Guidance

**Source:** `/Users/ryan/ai-env/projects/chirality-app/test/execution/PKG-30_Commissioning/1_Working/DEL-*/Specification.md` and `Guidance.md`

**Content Extracted:**
- DEL-30.01 Specification §Requirements: Systems coverage (railcar, tanks, transfer, metering, marine, electrical, I&C, fire, security) → commissioning labor scope
- DEL-30.02 Guidance.md §Considerations C-2: System breakdown and commissioning scope detail → commissioning team sizing assumptions
- DEL-30.02 Guidance.md §Principles P-1: Phased commissioning strategy (pre-commissioning, system commissioning, IST, start-up, performance) → duration phasing (A-008)
- DEL-30.02 Guidance.md §C-3: Terminal continuity constraints → duration extension assumptions (A-010)

**Quantities Extracted:**
- Commissioning phases (5 distinct phases) → duration breakdown
- System commissioning coverage scope → labor resource requirements
- Terminal constraint impacts → schedule duration adjustments

**Usage:** Duration assumptions, resource loading, scope boundaries

**Confidence:** LOW-MEDIUM (guidance principles, not detailed requirements)

---

**Quantity Sources Summary:**
- Explicit quantities extracted: 35% (railcar stations, tanks, deliverable counts, IST scenarios)
- Scope-based quantities (translated to assumptions): 65%
- Detailed quantity takeoff: Not performed (procedures and schedules TBD)

---

## 4. Embedded Typical Model (Fallback)

**Priority:** LOWEST (used when no usable pricing sources found)

**Source:** AGENT_ESTIMATING fallback typical model (embedded in agent instructions)

**Content Used:**
- Indirects factors (CI = 18% CD, PM = 6%, P = 2%)
- Contingency baseline percentages by CBS bucket
- Allowance-heavy adjustment (+5% contingency for buckets >80% allowance)

**Usage:**
- Parametric indirects/services allocation: $619k (Lines L-005, L-006, L-033 through L-037)
- Contingency calculation methodology: $1,211k total contingency

**Confidence:** LOW-MEDIUM (fallback model represents typical industry ranges, not project-specific data)

**Justification:** No project-specific indirects budget or detailed resource plan available; fallback model provides reasonable order-of-magnitude estimate

**Source Reference:** Decisions D-010, D-011, D-015, D-018; AGENT_ESTIMATING §STRUCTURE "Fallback Typical Model"

---

## 5. Allowances (Scope TBD / Quantities Unknown)

**Priority:** LOWEST (placeholder values)

**Allowances Created:** 26 line items (60.5% of line count, 71.7% of base cost)

**Allowance Categories:**

### 5.1 Engineering / Planning Allowances
- Commissioning procedures development: $350k (A-003)
- Commissioning plan development: $35k (A-004)
- **Total:** $385k

### 5.2 Consumables and Test Equipment Allowances
- Flushing & cleaning consumables: $85k (A-022)
- Hydrotest water treatment: $95k (A-012)
- Nitrogen purging: $35k (A-022)
- Test equipment rental: $180k (A-022)
- Metering proving equipment: $45k (A-018)
- Misc supplies: $25k (A-022)
- **Total:** $465k

### 5.3 Vendor Commissioning Support Allowances
- Tank instrumentation vendor support: $32k (A-005)
- Metering proving specialist: $75k (A-018)
- Marine loading vendor support: $36k (A-005)
- Control systems vendor support: $32k (A-005)
- Other specialized vendor support: $20k (A-005)
- **Total:** $195k

### 5.4 System-Specific Commissioning Allowances
- Railcar station commissioning (32 stations): $576k (A-014)
- Storage tank commissioning (3 tanks): $195k (A-013)
- Cathodic protection commissioning: $28k (A-023)
- Defect rectification: $75k (A-024)
- **Total:** $874k

### 5.5 Integrated Testing and Performance Allowances
- IST planning & coordination: $45k (A-016)
- IST scenarios (4 scenarios): $155k (A-016)
- Control system integration testing: $41k (A-016)
- Performance test planning & execution: $55k (A-017)
- **Total:** $296k

### 5.6 Temporary Facilities Allowance
- Commissioning temporary facilities: $85k (A-025)
- **Total:** $85k

**Allowances Summary:**
- Total allowance value: $2,300k (49.2% of base estimate; excludes parametric $619k and RATE_TABLE labor $703k that are also assumptions but not classified as "allowances")
- All allowances logged in Assumptions_Log.md with IDs A-001 through A-025
- All allowances traceable to deliverable scope or typical industry values

---

## Pricing Method Distribution Summary

| Method | Base Cost (CAD) | % of Base | Line Count | % of Lines | Confidence |
|--------|-----------------|-----------|------------|------------|------------|
| QUOTE | $0 | 0% | 0 | 0% | N/A |
| RATE_TABLE | $703,000 | 15.0% | 10 | 23.3% | MEDIUM |
| ALLOWANCE | $3,357,000 | 71.7% | 26 | 60.5% | LOW |
| PARAMETRIC | $619,000 | 13.2% | 7 | 16.3% | MEDIUM |
| **Total** | **$4,679,000** | **100%** | **43** | **100%** | **LOW** |

**Notes:**
- ALLOWANCE % includes both explicit allowances ($2,300k) and commissioning labor duration assumptions ($1,057k)
- Commissioning labor priced using RATE_TABLE rates but durations are assumptions → mixed confidence (rates MEDIUM, durations LOW)
- Overall estimate confidence: LOW due to high allowance/assumption reliance

---

## Search Strategy and Coverage

**Search Locations Checked:**
1. ✓ Decomposition file (quantities and scope)
2. ✓ PKG-30 deliverable folders (all 8 deliverables reviewed)
3. ✓ Deliverable Datasheets, Specifications, Guidance, Procedures (read for scope extraction)
4. ✓ `execution/_Estimates/_RateTables/` (no vendor quotes or project rate tables found)
5. ✓ Previous package estimates (for consistency in labor rates and methods)
6. ✓ `_CONFIG.md` (for estimate configuration overrides)

**Coverage Assessment:**
- All deliverables reviewed: 100%
- All available source documents read: 100%
- Vendor quotes available: 0%
- Project-specific rate tables available: 0%
- Fallback to typical industry values: Required for 72% of estimate

---

## Source Quality and Confidence Assessment

| Source Category | Availability | Quality | Confidence Impact |
|-----------------|--------------|---------|-------------------|
| Vendor quotes | None | N/A | Estimate confidence LOW |
| Project rate tables | None | N/A | Reliance on market rates |
| Deliverable scope definitions | Available (INITIALIZED) | Low detail | Scope assumptions required |
| Facility quantities | Available (decomposition) | Explicit | Medium-High confidence on counts |
| Commissioning procedures | Not developed | N/A | Engineering scope is allowance |
| Commissioning schedule | Not available | N/A | Duration is assumption |
| Vendor requirements | Not defined | N/A | Vendor support is allowance |

**Overall Source Quality:** LOW-MEDIUM
- Strengths: Facility quantities (railcar stations, tanks) are explicit and high confidence
- Weaknesses: Commissioning procedures TBD, schedule TBD, vendor requirements TBD, no vendor quotes

**Estimate Maturity Implication:** Class 5 (Conceptual / Order of Magnitude) appropriate for available source quality

---

## Recommended Source Improvements for Next Estimate Iteration

**Priority 1 (HIGH IMPACT):**
1. Develop commissioning procedures (DEL-30.01) to detailed outline level → refine engineering and labor scope
2. Obtain construction/commissioning schedule with system handover dates → refine duration assumptions
3. Obtain vendor quotes for specialized commissioning support (metering proving, tank instrumentation, marine loading) → replace allowances with quotes

**Priority 2 (MEDIUM IMPACT):**
4. Coordinate with equipment packages (PKG-10, PKG-11, PKG-13, PKG-19) for vendor commissioning requirements → refine vendor support scope
5. Obtain test equipment rental quotes → replace equipment rental allowance with quotes
6. Develop detailed commissioning plan (DEL-30.02) with resource loading → refine team size and duration

**Priority 3 (LOW IMPACT):**
7. Confirm terminal operations constraints and work windows with Employer → refine terminal continuity impact
8. Define performance test acceptance criteria (DEL-30.06) → refine performance test scope

**Expected Maturity Improvement:** Implementing Priority 1-2 recommendations would enable Class 4 estimate (-20% to +30% accuracy)

---

**Source Index Prepared By:** Estimating Agent (Automated Pipeline)
**Date:** 2026-01-29
**Status:** Complete

---

**End of Source Index**
