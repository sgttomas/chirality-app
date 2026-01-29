# Source Index

This index lists all sources discovered and used for pricing, quantities, and cost drivers in the PKG-27 Engineering Design estimate.

---

## Source Discovery Summary

| Source Type | Sources Found | Sources Used | Coverage |
|-------------|--------------|--------------|----------|
| Vendor Quotes | 0 | 0 | 0.0% |
| Rate Tables | 0 | 0 | 0.0% |
| Decomposition File | 1 | 1 | 100.0% (scope definition only) |
| Deliverable Folders | 0 | 0 | 0.0% (not yet scaffolded) |
| Parametric/Allowances | — | 27 assumptions | 100.0% (all line items) |

---

## Primary Sources (Scope Definition)

### Source 1: Project Decomposition Document

**File Path:** `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md`

**Type:** Project Scope Document

**Relevant Sections:**
- Line 117: PKG-27 package summary (Engineering Design, 5 deliverables)
- Lines 604-618: PKG-27 detailed scope and deliverables

**Content Used:**
- Package scope: "All engineering design, investigations, studies, HAZOP, Phase 2 feasibility documentation"
- Deliverable definitions:
  - DEL-27.01: Design Basis Documents ("Design basis memorandum, design criteria")
  - DEL-27.02: HAZOP Study Reports
  - DEL-27.03: Phase 2 Expansion Documentation ("Phase 2 general arrangement drawing, Phase 2 engineering memo")
  - DEL-27.04: Design Submission Packages ("30% design package, 60% design package, 90% design package, IFC package")
  - DEL-27.05: Cathodic Protection Design Basis & Design Calculations ("CP design basis, anode layout calculations, current demand calculations, design drawings where applicable")

**How Used:** Scope definition and deliverable enumeration. No quantities or pricing data available from this source.

**Confidence:** HIGH (for scope definition); LOW (no quantity or pricing data)

---

## Vendor Quotes (None Available)

**Search Conducted:**
- Searched deliverable `_REFERENCES.md` files — PKG-27 deliverables not yet scaffolded
- Searched project workspace for files matching: "quote", "proposal", "budget", "quotation", "RFP", "RFQ"
- Searched `execution/_Estimates/_RateTables/` directory
- **Result:** No vendor quotes found

**Impact:** All line items are priced using parametric/allowance methods. Estimate confidence is LOW.

**Recommendation:** Obtain budgetary quotes from:
1. HAZOP facilitator (specialist consultant with HAZOP expertise)
2. Cathodic protection specialist (corrosion engineering sub-consultant)
3. Engineering service providers (discipline-specific design services)

**Where to Add Quotes:**
- Save vendor quotes to project workspace with clear filenames (e.g., `HAZOP_Facilitator_Quote_ABC_Consultants_2026-01.pdf`)
- Reference in deliverable `_REFERENCES.md` files when scaffolded
- Or add to `execution/_Estimates/_RateTables/Vendor_Quotes/` directory

---

## Rate Tables (None Available)

**Search Conducted:**
- Searched `execution/_Estimates/_RateTables/` directory — directory exists but is empty
- Searched project workspace for files matching: "rate", "unit cost", "cost", "pricing", "schedule of rates"
- **Result:** No project-specific rate tables found

**Impact:** All engineering rates are parametric assumptions ($145-$185/hr blended rates) based on industry typical for Greater Vancouver engineering market. Estimate confidence is LOW.

**Recommendation:** Create project-specific engineering rate table with negotiated rates from engineering service providers.

**Suggested Rate Table Format:**

`/Users/ryan/ai-env/projects/chirality-app/test/execution/_Estimates/_RateTables/Engineering_Rates_2026.csv`

```csv
Discipline,Level,HourlyRate_CAD,Notes
Civil,Senior,180,Fully-burdened rate including OH&P
Civil,Intermediate,140,Fully-burdened rate including OH&P
Civil,Junior,105,Fully-burdened rate including OH&P
Mechanical,Senior,185,Fully-burdened rate including OH&P
Mechanical,Intermediate,145,Fully-burdened rate including OH&P
Electrical,Senior,175,Fully-burdened rate including OH&P
Electrical,Intermediate,135,Fully-burdened rate including OH&P
I&C,Senior,180,Fully-burdened rate including OH&P
I&C,Intermediate,140,Fully-burdened rate including OH&P
Marine,Senior,190,Fully-burdened rate including OH&P
Marine,Intermediate,150,Fully-burdened rate including OH&P
HAZOP Facilitator,Specialist,250,External consultant rate
CP Specialist,Specialist,210,Cathodic protection sub-consultant
Project Manager,Senior,165,PM and coordination role
```

---

## Parametric Sources (Industry Benchmarks)

Since no project-specific pricing sources were available, the following parametric sources and benchmarks were used:

### Parametric Source 1: Engineering Hourly Rates (Greater Vancouver Market)

**Source:** Industry typical engineering rates for Greater Vancouver region, British Columbia, January 2026 pricing.

**Benchmarks Used:**
- Senior Engineer (blended, fully-burdened): $165-$185/hr CAD
- HAZOP Facilitator (specialist): $250/hr CAD
- Design Coordination/Compilation (mid-level): $145-$165/hr CAD
- Project Manager (senior): $165/hr CAD

**Basis:** Greater Vancouver engineering market rates for consulting engineering services; fully-burdened rates including salary, benefits, overhead, and profit.

**Confidence:** MED (industry typical but not project-specific)

**Applied To:**
- All Engineering (E) CBS line items (L001-L018)
- PM line items (L019-L020)
- CD line item (L022)
- COM line item (L024)

**Reference:** Assumptions A-024, A-025

---

### Parametric Source 2: Engineering Effort Factors (Typical Design-Build Projects)

**Source:** Industry typical engineering effort factors for design-build projects in British Columbia.

**Benchmarks Used:**
- **Design Basis Document (per discipline):** 200-400 hours
- **HAZOP Facilitation:** 5 days (40 hours) for bulk liquid transload facility
- **HAZOP Engineering Participation:** 40 hours per discipline (5 disciplines)
- **Design Submission Package Compilation:** 500-850 hours (varies by milestone)
- **Phase 2 Concept Design:** 350-450 hours
- **Phase 2 Feasibility Engineering:** 250-350 hours
- **CP Design Basis:** 120-160 hours
- **CP Design Calculations:** 180-220 hours
- **FAT/SAT Design Representative Attendance:** 15 days across project
- **Commissioning Design Support:** 80 hours

**Basis:** Typical engineering effort for design-build EPC projects; adjusted for facility size and complexity (1M MT/a capacity, 45,000 MT storage, 32 railcar stations, marine loading).

**Confidence:** LOW to MED (varies by factor; HAZOP and FAT/SAT attendance are MED confidence; design basis and submission packages are LOW confidence)

**Applied To:**
- DEL-27.01 (Design Basis Documents): A-001 through A-005
- DEL-27.02 (HAZOP Study): A-006 through A-009
- DEL-27.03 (Phase 2 Expansion): A-010, A-011
- DEL-27.04 (Design Submission Packages): A-012 through A-015
- DEL-27.05 (CP Design): A-016 through A-018
- Support Activities: A-019 through A-023

**Reference:** Assumptions A-001 through A-023, A-026, A-027

---

### Parametric Source 3: Indirects and Support Factors (Fallback Model)

**Source:** Fallback Typical Model (embedded in AGENT_ESTIMATING.md, lines 666-673)

**Factors Used:**
- **Project Management (PM):** 11.5% of Engineering (E) base (adjusted from 6% default due to multi-discipline coordination complexity) — Decision D-009
- **Procurement (P):** Allowance for HAZOP logistics — Assumption A-020
- **Construction Directs (CD):** Design representative attendance at FAT/SAT — Assumption A-021
- **Construction Indirects (CI):** Field engineering coordination — Assumption A-022
- **Commissioning (COM):** Design verification support — Assumption A-023

**Basis:** Fallback model provides default factors for indirects when project-specific data is not available. PM factor was adjusted upward (11.5% vs. 6% default) due to PKG-27's high coordination requirements.

**Confidence:** MED (fallback model is based on industry typical but not project-specific)

**Applied To:**
- L019, L020 (PM)
- L021 (P)
- L022 (CD)
- L023 (CI)
- L024 (COM)

**Reference:** Decision D-009; Assumptions A-019 through A-023

---

### Parametric Source 4: Contingency Factors (Fallback Model)

**Source:** Fallback Typical Model (embedded in AGENT_ESTIMATING.md, lines 676-697)

**Factors Used:**
- **Engineering (E):** 10% baseline + 2% allowance-heavy adjustment = 12%
- **Project Management (PM):** 10% baseline + 2% allowance-heavy adjustment = 12%
- **Procurement (P):** 15% baseline + 2% allowance-heavy adjustment = 17%
- **Construction Directs (CD):** 20% (standard)
- **Construction Indirects (CI):** 20% (standard)
- **Commissioning (COM):** 25% (standard)

**Allowance-Heavy Adjustment:** +2% applied to CBS buckets with AllowanceShare >50% per fallback model.

**Basis:** Fallback model contingency defaults; adjusted for allowance-heavy buckets.

**Confidence:** MED (fallback model is based on industry typical)

**Applied To:** All CBS categories

**Reference:** Decision D-011; BOE.md Contingency Methodology section

---

## Deliverable Folders (Not Yet Scaffolded)

**Search Conducted:**
- Searched for PKG-27 deliverable folders under `execution/PKG-27_Engineering_Design/1_Working/`
- **Result:** Deliverable folders not yet created (scaffolding not completed)

**Impact:** No deliverable-specific scope definition, datasheets, specifications, or guidance available. All scope interpretation is based on decomposition only.

**Recommendation:** Scaffold PKG-27 deliverable folders and populate with initial scope definition, then re-run estimate with refined quantities and cost drivers.

**Expected Deliverable Folder Structure:**
```
execution/PKG-27_Engineering_Design/1_Working/
├── DEL-27.01_Design_Basis_Documents/
│   ├── _CONTEXT.md
│   ├── _REFERENCES.md
│   ├── Datasheet.md
│   ├── Specification.md
│   ├── Guidance.md
│   └── Procedure.md
├── DEL-27.02_HAZOP_Study_Reports/
├── DEL-27.03_Phase_2_Expansion_Documentation/
├── DEL-27.04_Design_Submission_Packages/
└── DEL-27.05_Cathodic_Protection_Design_Basis_Design_Calculations/
```

---

## Configuration File

**File Path:** `/Users/ryan/ai-env/projects/chirality-app/test/execution/_Estimates/_CONFIG.md`

**Content Used:**
- Currency: CAD
- Pricing Date: 2026-01 (January 2026)
- Estimate Label: PKG27_DRAFT (updated for this snapshot)
- Rounding: 1000 (nearest $1,000)
- Contingency Method: PCT_BY_BUCKET
- Escalation Mode: NONE
- Include Scopes: Engineering, PM, Procurement, Materials, Construction Directs, Construction Indirects, Commissioning
- Exclude Scopes: Owner's costs, land, financing, permits obtained by Employer

**How Used:** Config file provided default settings for estimate basis, CBS coverage, and methodology.

**Confidence:** HIGH (config file is authoritative for project-level settings)

---

## Source Priority Applied

Per AGENT_ESTIMATING.md (PROTOCOL Function 3 Phase 3.3), pricing sources are applied in priority order:

1. **Vendor Quotes** (highest priority) — 0 sources available
2. **Rate Tables** — 0 sources available
3. **Parametric/Allowances** — Used for all 24 line items (100%)

**Result:** Entire estimate is based on parametric/allowance pricing.

---

## Recommendations for Next Estimate Run

To improve estimate confidence and reduce reliance on parametric/allowance pricing, obtain the following sources:

### High Priority (Target: Upgrade to Class 4 Estimate)

1. **HAZOP Facilitator Quote** — Budgetary quote from specialist consultant with HAZOP expertise (target savings/refinement: ±$20,000)
2. **CP Specialist Quote** — Budgetary quote from cathodic protection sub-consultant (target savings/refinement: ±$30,000)
3. **Engineering Service Provider Quotes** — Quotes from 2-3 engineering firms for design basis documents and design submission package coordination (target savings/refinement: ±$100,000-$200,000)

### Medium Priority (Target: Upgrade to Class 3 Estimate)

4. **Project-Specific Engineering Rate Table** — Negotiate and document engineering hourly rates with selected service providers
5. **Discipline-Specific Engineering Hour Budgets** — Develop detailed hour budgets for design basis documents and design submission packages based on preliminary scope definition
6. **HAZOP Scoping Study** — Conduct preliminary HAZOP scoping session to identify process nodes and confirm participant requirements

### Lower Priority (Target: Continuous Improvement)

7. **Deliverable Folder Scaffolding** — Create deliverable folders and populate with initial scope definition (Datasheets, Specifications, Guidance, Procedures)
8. **Geotechnical/Corrosivity Studies** — Obtain data to refine CP design scope
9. **Design Milestone Schedule** — Confirm 30%/60%/90%/IFC submission dates and drawing count estimates

---

## Source Index Change Log

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-01-29 | Initial source index for EST_PKG27_DRAFT_2026-01-29_0040 |

---

**Source Index Prepared By:** ESTIMATING Agent (Straight-Through Pipeline)
**Date:** 2026-01-29 00:40
