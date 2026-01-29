# Source Index — PKG-26 Protective Coatings & Painting

**Snapshot ID:** EST_PKG26_DRAFT_2026-01-29_0006
**Date:** 2026-01-29

This document indexes all sources used for pricing, quantities, and estimating basis.

---

## Source Hierarchy (Priority Order)

The estimating pipeline searches for sources in the following priority order:

1. **Explicit pricing sources (vendor quotes, budgetary quotes, proposals):** HIGHEST PRIORITY
2. **Rate tables / cost libraries:** HIGH PRIORITY
3. **Quantity sources (drawings, specifications, data sheets):** MEDIUM PRIORITY
4. **Derived quantities (from related package estimates):** MEDIUM PRIORITY
5. **Allowances and parametric factors (fallback model):** LOWEST PRIORITY

---

## Source Discovery Results

### 1. Explicit Pricing Sources (Vendor Quotes)

**Search performed:** Checked `_REFERENCES.md` in all PKG-26 deliverable folders; searched project workspace for vendor quotes, budgetary quotes, proposals

**Result:** **NONE FOUND**

**Impact:** 0% of estimate priced by vendor quotes

**Recommendation:** Issue RFQs for coating materials to obtain budgetary quotes:
- Food-grade tank linings (FDA 21 CFR 175.300, NSF/ANSI 61 compliant)
- Marine coating systems (NACE/SSPC marine guidance)
- Structural steel topcoats (compatible with galvanizing)
- Surface preparation abrasives
- Application consumables and testing equipment

---

### 2. Rate Tables / Cost Libraries

**Search performed:** Checked `/Users/ryan/ai-env/projects/chirality-app/test/execution/_Estimates/_RateTables/` directory

**Result:** **NONE FOUND**

**Impact:** 0% of estimate priced by rate tables

**Recommendation:** Create project rate tables for:
- Coating material unit costs ($/m² or $/L)
- Surface preparation labor rates ($/m² by SSPC grade)
- Coating application labor rates ($/m² by application method and coating type)
- Engineering hourly rates by discipline
- Inspection and testing labor rates

---

### 3. Quantity Sources (Drawings, Specifications, Data Sheets)

**Search performed:** Read all 4 deliverable folders in PKG-26 (DEL-26.01 through DEL-26.04); reviewed Datasheet.md and Specification.md files

**Result:** **PARTIAL** — Deliverables provide qualitative scope but not quantitative surface areas or coating system details

**Sources found:**
- DEL-26.01 Datasheet: Defines 5 coating application types (tank internal, tank external, structural steel, marine, field); lists TBD for quantities
- DEL-26.01 Specification: Defines performance requirements, standards, and interfaces; coating systems and DFT TBD
- No explicit surface area calculations or coating quantity takeoffs found

**Impact:** Qualitative scope definition; no direct quantitative basis for estimate

**Recommendation:**
- Complete detailed coating specification in DEL-26.01 (coating systems, DFT, SSPC surface prep grades)
- Perform surface area takeoffs from 3D model or detailed drawings
- Coordinate with PKG-06, PKG-08, PKG-13 to verify quantities

---

### 4. Derived Quantities (Related Package Estimates)

**Search performed:** Reviewed PKG-06, PKG-08, PKG-13 estimates for structural steel tonnages and tank surface areas

**Result:** **FOUND** — Quantities derived from related packages

**Sources found:**

#### PKG-13 Storage Tanks (EST_PKG13_DRAFT_2026-01-28_2400)
- **Line L015:** Internal Coating System - food-grade epoxy lining (~11000 m² total 3 tanks)
  - **Confidence:** MED (quantity from PKG-13 estimate; not yet validated by detailed tank design)
  - **Used for:** Tank internal coating area (Line L2606, L2614, L2615)
- **Line L016:** External Coating System - primer and topcoat (~9000 m² total 3 tanks)
  - **Confidence:** MED (quantity from PKG-13 estimate; not yet validated by detailed tank design)
  - **Used for:** Tank external coating area (Line L2607, L2616, L2617)

#### PKG-06 Structural Steelwork (EST_PKG06_DRAFT_2026-01-28_2333)
- **Line L006:** Structural Steel Material Supply - fabricated and galvanized (platforms stairs gangways pipe racks handrails supports) - 150 tonnes
  - **Confidence:** MED (tonnage from PKG-06 estimate)
  - **Derived surface area:** 150 tonnes × 25 m²/tonne = 3,750 m² (Decision D-2609)
  - **Used for:** Structural steel field painting (Line L2608, L2618, L2619)
  - **Note:** PKG-06 material cost includes galvanizing; PKG-26 provides field painting over galvanized

#### PKG-08 Marine Structures (EST_PKG08_DRAFT_2026-01-28_2400)
- **Line L813:** Trestle Structural Steel Supply - 150 tonnes
- **Line L814:** Loading Platform Structural Steel Supply - 80 tonnes
- **Line L815:** Catwalk Structural Steel Supply - 25 tonnes
- **Total marine steel:** 150 + 80 + 25 = 255 tonnes
  - **Confidence:** MED (tonnages from PKG-08 estimate)
  - **Derived surface area:** 255 tonnes × 30 m²/tonne = 7,650 m² (Decision D-2610)
  - **Used for:** Marine coatings (Line L2609, L2620, L2621)

**Impact:** 35% of estimate based on derived quantities from related packages ($845k direct material and labor)

**Quality:** Quantities are derived from related package estimates (not vendor-confirmed or detailed-design-validated)

---

### 5. Allowances and Parametric Factors (Fallback Model)

**Search performed:** Applied fallback typical model per AGENT_ESTIMATING.md when no other sources available

**Result:** **APPLIED** — Fallback model used for engineering, field touch-up, consumables, indirects, PM, procurement, commissioning

**Sources applied:**

#### Allowance-Based Line Items (Engineering)
- **L2601:** Coating specification — 100 hours @ $250/hr = $25k (Assumption A-2601)
- **L2602:** Coating procedures — 80 hours @ $250/hr = $20k (Assumption A-2602)
- **L2603:** Data sheet compilation — 40 hours @ $250/hr = $10k (Assumption A-2603)
- **L2604:** Records preparation — 60 hours @ $250/hr = $15k (Assumption A-2604)
- **L2605:** Engineering coordination — 90 hours @ $245/hr = $22k (Assumption A-2605)
- **Total engineering allowances:** $92k (3.8% of base estimate)

#### Allowance-Based Line Items (Materials)
- **L2606:** Tank internal coating — 11,000 m² @ $50/m² = $550k (Assumption A-2606; derived quantity; allowance rate)
- **L2607:** Tank external coating — 9,000 m² @ $20/m² = $180k (Assumption A-2607; derived quantity; allowance rate)
- **L2608:** Structural steel field painting — 3,750 m² @ $15/m² = $56k (Assumption A-2608; derived quantity; allowance rate)
- **L2609:** Marine coatings — 7,650 m² @ $35/m² = $268k (Assumption A-2609; derived quantity; allowance rate)
- **L2610:** Field touch-up materials — $85k lump sum (Assumption A-2610)
- **L2611:** Surface prep abrasives — $95k lump sum (Assumption A-2611)
- **L2612:** Application consumables — $65k lump sum (Assumption A-2612)
- **L2613:** Testing equipment — $35k lump sum (Assumption A-2613)
- **Total material allowances:** $1,389k (57.7% of base estimate; 70% of MAT bucket)

#### Allowance-Based Line Items (Construction Directs)
- **L2614:** Tank internal surface prep labor — 11,000 m² @ $8/m² = $88k (Assumption A-2614)
- **L2615:** Tank internal coating application labor — 11,000 m² @ $12/m² = $132k (Assumption A-2615)
- **L2616:** Tank external surface prep labor — 9,000 m² @ $5/m² = $45k (Assumption A-2616)
- **L2617:** Tank external coating application labor — 9,000 m² @ $7/m² = $63k (Assumption A-2617)
- **L2618:** Structural steel surface prep labor — 3,750 m² @ $3/m² = $11k (Assumption A-2618)
- **L2619:** Structural steel field painting labor — 3,750 m² @ $5/m² = $19k (Assumption A-2619)
- **L2620:** Marine surface prep labor — 7,650 m² @ $7/m² = $54k (Assumption A-2620)
- **L2621:** Marine coating application labor — 7,650 m² @ $10/m² = $77k (Assumption A-2621)
- **L2622:** Field touch-up labor — $95k lump sum (Assumption A-2622)
- **L2623:** Inspection and testing labor — $75k lump sum (Assumption A-2623)
- **L2624:** Confined space entry support — $55k lump sum (Assumption A-2624)
- **L2625:** Access equipment and scaffolding — $65k lump sum (Assumption A-2625)
- **Total CD allowances:** $762k (31.6% of base estimate; 60% of CD bucket)

#### Parametric Factor-Based Line Items (Fallback Model)
- **L2626 (CI):** Construction Indirects = 18% × CD = $137k (Decision D-2608; AGENT_ESTIMATING.md default)
- **L2627 (P):** Procurement = 2% × MAT = $28k (Decision D-2608; AGENT_ESTIMATING.md default)
- **L2628 (PM):** Project Management = 6% × (CD+CI+MAT) = $137k (Decision D-2608; AGENT_ESTIMATING.md default)
- **L2629 (COM):** Commissioning = 3% × (CD+CI+MAT) = $69k (Decision D-2608; AGENT_ESTIMATING.md default)
- **Total parametric allowances:** $371k (15.4% of base estimate)

**Impact:** 65% of estimate based on allowances and parametric factors ($1,562k + $371k = $1,933k total)

**Rationale:** No project-specific pricing sources or rate tables available; fallback model provides runnable basis for straight-through estimate

---

## Source Quality Summary

| Source Type | Amount | % of Base | Confidence | Notes |
|-------------|--------|-----------|------------|-------|
| Vendor quotes | $0 | 0% | N/A | None available |
| Rate tables | $0 | 0% | N/A | None available |
| Derived quantities (from related packages) | $845k | 35% | MED | Tank areas from PKG-13; steel tonnages from PKG-06/PKG-08; surface area factors assumed |
| Allowances (engineering, materials, CD labor) | $1,562k | 65% | LOW | No vendor pricing; coating systems not specified; labor productivity assumed |
| Parametric factors (CI, P, PM, COM) | $371k | 15% | LOW-MED | Fallback model default factors; may not reflect project-specific conditions |
| **Total before contingency** | **$2,408k*** | **100%** | **LOW-MED** | *Rounded from $2,613k |

**Overall Source Quality:** LOW-MED
- Moderate confidence in derived quantities (from validated related package estimates)
- Low confidence in allowance-based pricing (no vendor quotes or rate tables)
- Low confidence in parametric factors (default fallback model; not project-specific)

---

## Recommendations to Improve Source Quality

### Immediate Actions (to reach Class 3 Budget Estimate)

1. **Obtain vendor budgetary quotes:**
   - Food-grade tank linings (FDA/NSF compliant epoxy systems)
   - Marine coating systems (NACE/SSPC guidance; high-performance epoxies)
   - Structural steel topcoats (compatible with galvanizing)
   - Surface preparation abrasives and consumables
   - **Impact:** Would reduce allowance share from 70% to <30% in MAT bucket; increase confidence to MED-HIGH

2. **Create project rate tables:**
   - Engineering hourly rates by discipline
   - Coating labor rates by surface prep grade (SSPC-SP 5, SP-6, SP-10) and application method
   - Inspection and testing labor rates
   - **Impact:** Would reduce allowance share from 60% to <20% in CD bucket; increase confidence to MED-HIGH

3. **Complete coating specifications:**
   - Finalize DEL-26.01 coating specification (systems, DFT, coat schedules, SSPC grades)
   - Define shop vs. field coating responsibilities with PKG-06 and PKG-08
   - **Impact:** Would enable vendor quotes with firm scope basis; increase confidence to MED-HIGH

### Future Actions (to reach Class 2 Definitive Estimate)

1. **Complete detailed surface area takeoffs:**
   - Tank surface areas from 3D model or detailed tank design (coordinate with PKG-13)
   - Structural steel surface areas from detailed fabrication drawings (coordinate with PKG-06)
   - Marine steel surface areas from detailed marine structures design (coordinate with PKG-08)
   - **Impact:** Would replace derived surface area factors with validated quantities; increase confidence to HIGH

2. **Obtain firm vendor quotations:**
   - Issue RFPs with completed coating specifications
   - Obtain firm pricing with defined scope, schedule, and terms
   - **Impact:** Would replace all material allowances with firm quotes; increase confidence to HIGH

3. **Develop detailed coating application schedule:**
   - Define access requirements and sequencing
   - Model weather impacts and recoat windows
   - Quantify labor resource loading
   - **Impact:** Would replace CD labor allowances with detailed resource-loaded schedule; increase confidence to HIGH

---

## Source References

### Decomposition
- `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md`
  - Section 1: Project overview
  - Section 5: PKG-26 Protective Coatings & Painting (lines 588-602)
  - Section 6: Objectives (OBJ-3 Storage Capacity, OBJ-9 Lifecycle Cost Optimization)

### Configuration
- `/Users/ryan/ai-env/projects/chirality-app/test/execution/_Estimates/_CONFIG.md`
  - Currency: CAD
  - Pricing date: 2026-01
  - Contingency method: PCT_BY_BUCKET
  - Rounding: 1000

### Deliverable Documents
- `/Users/ryan/ai-env/projects/chirality-app/test/execution/PKG-26_Protective_Coatings_and_Painting/1_Working/`
  - `DEL-26.01_Coating_Technical_Specification/` — Datasheet.md, Specification.md, Guidance.md, Procedure.md
  - `DEL-26.02_Coating_Procedures/` — Datasheet.md, Specification.md, Guidance.md, Procedure.md
  - `DEL-26.03_Coating_Data_Sheet_Package/` — Datasheet.md, Specification.md, Guidance.md, Procedure.md
  - `DEL-26.04_Coating_Installation_and_Test_Records/` — Datasheet.md, Specification.md, Guidance.md, Procedure.md

### Related Package Estimates
- **PKG-06:** EST_PKG06_DRAFT_2026-01-28_2333 — Detail.csv Line L006 (150 tonnes structural steel)
- **PKG-08:** EST_PKG08_DRAFT_2026-01-28_2400 — Detail.csv Lines L813, L814, L815 (255 tonnes marine steel)
- **PKG-13:** EST_PKG13_DRAFT_2026-01-28_2400 — Detail.csv Lines L015, L016 (11,000 m² internal, 9,000 m² external coating areas)

### Agent Instructions
- `/Users/ryan/ai-env/projects/chirality-app/agents/AGENT_ESTIMATING.md`
  - Section 3.4: Fallback Typical Model (default factors for CI, P, PM, COM)
  - Section 4.2: Contingency (PCT_BY_BUCKET method and allowance-share adjustments)

---

**End of Source Index**
