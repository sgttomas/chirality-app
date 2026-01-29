# Decision Log — PKG-26 Protective Coatings & Painting

**Snapshot ID:** EST_PKG26_DRAFT_2026-01-29_0006
**Date:** 2026-01-29

This log captures all decisions made during the estimating process where choices were required due to missing inputs, ambiguities, or conflicts.

---

## Decision Entries

### D-2601: Currency Selection

**Decision:** Use CAD (Canadian dollars) for all costs

**Trigger:** No explicit currency specified in deliverable documents

**Evidence:**
- Project location: Surrey, BC, Canada (Decomposition Section 1)
- _CONFIG.md specifies CAD as project currency
- All previous package estimates use CAD

**Impacted WBS/CBS:** All line items

**Estimate Impact:** Qualitative — establishes pricing basis; no exchange rate conversions needed

**Override Path:** Update `_CONFIG.md` if different currency required

**Source:** _CONFIG.md; Decomposition Section 1; BOE precedent

---

### D-2602: Pricing Date

**Decision:** Use January 2026 as pricing date ("dollars of" month)

**Trigger:** No explicit pricing date in deliverable documents

**Evidence:**
- Current date: 2026-01-29
- _CONFIG.md specifies pricing_date = 2026-01
- Consistent with other package estimates

**Impacted WBS/CBS:** All line items

**Estimate Impact:** Establishes escalation baseline; no escalation applied per _CONFIG.md

**Override Path:** Update `_CONFIG.md` pricing_date if different date required

**Source:** _CONFIG.md; current date

---

### D-2603: Estimate Label

**Decision:** Use "PKG26_DRAFT" as estimate label

**Trigger:** Standard labeling convention for package-level estimates

**Evidence:**
- Previous package estimates use "PKG##_DRAFT" format (PKG00_DRAFT through PKG20_DRAFT)
- Decomposition identifies this as PKG-26

**Impacted WBS/CBS:** Snapshot identification only

**Estimate Impact:** None (labeling only)

**Override Path:** Update _CONFIG.md estimate_label if different label needed

**Source:** _CONFIG.md precedent; Decomposition PKG-26

---

### D-2604: Rounding Policy

**Decision:** Round to nearest $1,000

**Trigger:** Standard project rounding policy

**Evidence:**
- _CONFIG.md specifies rounding = 1000
- Consistent with all previous package estimates
- Appropriate for Class 4-5 estimate maturity

**Impacted WBS/CBS:** Summary totals only; detail lines not rounded

**Estimate Impact:** $205k reduction in total (from $3,161k to $3,051k after contingency); rounding down to avoid false precision

**Override Path:** Update _CONFIG.md rounding parameter

**Source:** _CONFIG.md; AGENT_ESTIMATING.md rounding policy

---

### D-2605: Scope Inclusions

**Decision:** Include Engineering, PM, Procurement, Materials, Construction Directs/Indirects, and Commissioning

**Trigger:** _CONFIG.md defines include_scopes

**Evidence:**
- _CONFIG.md include_scopes: E, PM, P, MAT, CD, CI, COM
- Decomposition confirms PKG-26 scope covers specification, procedures, data sheets, records, and coating execution
- Design & Build contract (D&B Contractor responsible for all phases)

**Impacted WBS/CBS:** All CBS buckets

**Estimate Impact:** Full EPC-style estimate; excludes Owner's costs, land, financing per _CONFIG.md

**Override Path:** Update _CONFIG.md include_scopes or exclude_scopes

**Source:** _CONFIG.md; Decomposition PKG-26; contract type

---

### D-2606: Contingency Method

**Decision:** Use PCT_BY_BUCKET (percentage by CBS bucket) method

**Trigger:** _CONFIG.md specifies contingency_method

**Evidence:**
- _CONFIG.md contingency_method = PCT_BY_BUCKET
- Consistent with all previous package estimates
- Allows adjustment for allowance-heavy buckets per AGENT_ESTIMATING.md

**Impacted WBS/CBS:** CONT (contingency) bucket; all CBS buckets receive contingency allocation

**Estimate Impact:** 27% blended contingency rate ($643k); varies by bucket based on allowance share

**Override Path:** Update _CONFIG.md contingency_method to RISK_BASED if preferred

**Source:** _CONFIG.md; AGENT_ESTIMATING.md Section 4.2

---

### D-2607: Escalation Mode

**Decision:** No escalation applied (escalation_mode = NONE)

**Trigger:** _CONFIG.md specifies escalation_mode

**Evidence:**
- _CONFIG.md escalation_mode = NONE
- All costs in January 2026 pricing basis
- Consistent with all previous package estimates

**Impacted WBS/CBS:** All line items (no escalation bucket)

**Estimate Impact:** No escalation adjustment; estimate represents current pricing only

**Override Path:** Update _CONFIG.md escalation_mode to EXPLICIT; provide escalation factors and schedule

**Source:** _CONFIG.md; AGENT_ESTIMATING.md Section 4.3

---

### D-2608: Fallback Model Application

**Decision:** Use fallback typical model for indirects, procurement, PM, and commissioning factors

**Trigger:** No project-specific rate tables or factor schedules available

**Evidence:**
- No rate tables found in _RateTables/ directory
- No project-specific indirects/PM percentages in deliverable documents
- AGENT_ESTIMATING.md provides default factors for straight-through execution

**Impacted WBS/CBS:** CI, P, PM, COM (parametric line items)

**Estimate Impact:**
- CI = 18% × CD = $137k
- P = 2% × MAT = $28k
- PM = 6% × (CD+CI+MAT) = $137k
- COM = 3% × (CD+CI+MAT) = $69k
- Total parametric cost: $371k (15% of base estimate)

**Override Path:**
- Add project-specific rate tables to _RateTables/
- Update _CONFIG.md with explicit factor overrides
- Provide project-specific indirects/PM/COM estimates

**Source:** AGENT_ESTIMATING.md default factors (Section 3.4 Fallback Model)

**Confidence:** LOW (default factors may not reflect project-specific conditions; marine project may require higher indirects for HSE/logistics)

---

### D-2609: Structural Steel Surface Area Factor

**Decision:** Use 25 m² surface area per tonne for structural steel

**Trigger:** Structural steel surface area not explicitly defined; needed to estimate field painting quantities

**Evidence:**
- PKG-06 estimate provides tonnage (150 tonnes) but not surface area
- Industry typical range: 20-30 m²/tonne for fabricated structural steel depending on complexity
- 25 m²/tonne is mid-range assumption for platforms, stairs, gangways, handrails, pipe racks (typical PKG-06 scope)
- Higher complexity (grating, handrails, intricate connections) increases surface area per tonne

**Impacted WBS/CBS:** MAT (L2608), CD (L2618, L2619) for structural steel field painting

**Estimate Impact:**
- Structural steel surface area: 150 tonnes × 25 m²/tonne = 3,750 m²
- Field painting cost: 3,750 m² × $15/m² = $56k material + $30k labor = $86k
- If factor is 20 m²/t: 3,000 m² → $69k (−$17k or −20%)
- If factor is 30 m²/t: 4,500 m² → $103k (+$17k or +20%)

**Override Path:**
- Complete detailed surface area takeoff from PKG-06 drawings or 3D model
- Obtain fabricator-provided surface area data
- Update Detail.csv L2608 quantity when actual surface area is known

**Source:** Industry typical factors; engineering judgment

**Confidence:** LOW (±20% range; actual surface area depends on component mix and fabrication details)

---

### D-2610: Marine Steel Surface Area Factor

**Decision:** Use 30 m² surface area per tonne for marine structural steel

**Trigger:** Marine steel surface area not explicitly defined; needed to estimate marine coating quantities

**Evidence:**
- PKG-08 estimate provides tonnages (trestle 150t, loading platform 80t, catwalk 25t; total 255t) but not surface area
- Industry typical range: 25-35 m²/tonne for marine structures
- 30 m²/tonne is mid-range assumption; marine structures typically have higher surface area per tonne than land-based structures due to:
  - Increased exposure surface (all sides exposed to marine environment)
  - Complex marine details (splash zone transitions, corrosion protection interfaces)
  - Marine access platforms and safety features

**Impacted WBS/CBS:** MAT (L2609), CD (L2620, L2621) for marine coatings

**Estimate Impact:**
- Marine steel surface area: 255 tonnes × 30 m²/tonne = 7,650 m²
- Marine coating cost: 7,650 m² × $35/m² = $268k material + $130k labor = $398k
- If factor is 25 m²/t: 6,375 m² → $332k (−$66k or −17%)
- If factor is 35 m²/t: 8,925 m² → $464k (+$66k or +17%)

**Override Path:**
- Complete detailed surface area takeoff from PKG-08 drawings or 3D model
- Obtain fabricator-provided surface area data
- Update Detail.csv L2609 quantity when actual surface area is known

**Source:** Industry typical factors; marine engineering judgment

**Confidence:** LOW (±17% range; actual surface area depends on marine structure configuration and exposure zone definition)

---

### D-2611: Contingency Rate Adjustments for Allowance Share

**Decision:** Increase contingency rates for buckets with high allowance share (≥50%)

**Trigger:** AGENT_ESTIMATING.md specifies contingency adjustment rules for allowance-heavy buckets

**Evidence:**
- E bucket: 100% allowance share → base 10% + 10% adjustment = 20%
- MAT bucket: 70% allowance share → base 15% + 5% adjustment = 20%
- CD bucket: 60% allowance share → base 20% + 5% adjustment = 25%
- Allowance-heavy buckets have higher uncertainty and should carry higher contingency

**Impacted WBS/CBS:** E, MAT, CD contingency calculations

**Estimate Impact:**
- E contingency increased from $9.2k (10%) to $18.4k (20%): +$9.2k
- MAT contingency increased from $208k (15%) to $278k (20%): +$70k
- CD contingency increased from $152k (20%) to $190k (25%): +$38k
- Total contingency increase: +$117k (22% increase in contingency)

**Override Path:** If project-specific pricing or rate tables are added and allowance share drops below thresholds, contingency rates will automatically adjust in next estimate iteration

**Source:** AGENT_ESTIMATING.md Section 4.2 (Contingency default PCT_BY_BUCKET); Assumptions_Log.md

**Confidence:** MED (adjustment methodology per agent instructions; rates appropriate for allowance-based estimate)

---

### D-2612: Tank Coating Area Sources

**Decision:** Use tank coating areas from PKG-13 estimate (11,000 m² internal, 9,000 m² external)

**Trigger:** Tank surface areas not explicitly calculated in PKG-26 deliverable documents; PKG-13 estimate provides quantities

**Evidence:**
- PKG-13 estimate Detail.csv Line L015: "Internal Coating System - food-grade epoxy lining (~11000 m2 total 3 tanks)"
- PKG-13 estimate Detail.csv Line L016: "External Coating System - primer and topcoat (~9000 m2 total 3 tanks)"
- Tank configuration: 3 × 15,000 MT storage tanks (Decomposition Section 1)
- PKG-13 estimate provides validated quantity basis (EST_PKG13_DRAFT_2026-01-28_2400)

**Impacted WBS/CBS:** MAT (L2606, L2607), CD (L2614, L2615, L2616, L2617) for tank coatings

**Estimate Impact:**
- Tank internal coating: 11,000 m² basis for $770k estimate
- Tank external coating: 9,000 m² basis for $288k estimate
- Total tank coating cost: $1,058k (44% of base estimate)

**Override Path:**
- Complete detailed tank surface area calculations from tank design drawings or 3D model
- Verify with PKG-13 tank design deliverables (DEL-13.01 through DEL-13.06)
- Update Detail.csv L2606, L2607, L2614-L2617 quantities when actual surface areas are known

**Source:** PKG-13 estimate (EST_PKG13_DRAFT_2026-01-28_2400) Detail.csv L015, L016

**Confidence:** MED (quantities from related package estimate; not yet validated by detailed tank design)

---

### D-2613: Structural Steel Tonnage Source

**Decision:** Use structural steel tonnage from PKG-06 estimate (150 tonnes)

**Trigger:** Structural steel quantities not explicitly defined in PKG-26 deliverable documents; PKG-06 estimate provides tonnage

**Evidence:**
- PKG-06 estimate Detail.csv Line L006: "Structural Steel Material Supply - fabricated and galvanized (platforms stairs gangways pipe racks handrails supports)" at 150 tonnes
- PKG-06 scope includes platforms, stairs, gangways, pipe racks, handrails, supports (Decomposition PKG-06)
- PKG-06 estimate note: "150 tonnes (D-012) at $6k/tonne fabricated/galvanized"
- Galvanizing provided in PKG-06 material cost; PKG-26 provides field painting over galvanized

**Impacted WBS/CBS:** MAT (L2608), CD (L2618, L2619) for structural steel field painting

**Estimate Impact:**
- Structural steel surface area: 150 tonnes × 25 m²/tonne = 3,750 m² (per D-2609)
- Field painting cost: $86k (4% of base estimate)

**Override Path:**
- Verify with PKG-06 structural steel deliverables (DEL-06.01 through DEL-06.05)
- Update tonnage when PKG-06 design is finalized

**Source:** PKG-06 estimate (EST_PKG06_DRAFT_2026-01-28_2333) Detail.csv L006; Decision D-012 from PKG-06

**Confidence:** MED (tonnage from related package estimate; galvanizing noted as included in PKG-06)

---

### D-2614: Marine Steel Tonnage Source

**Decision:** Use marine steel tonnages from PKG-08 estimate (255 tonnes total: trestle 150t, platform 80t, catwalk 25t)

**Trigger:** Marine steel quantities not explicitly defined in PKG-26 deliverable documents; PKG-08 estimate provides tonnages

**Evidence:**
- PKG-08 estimate Detail.csv Line L813: "Trestle Structural Steel Supply" at 150 tonnes
- PKG-08 estimate Detail.csv Line L814: "Loading Platform Structural Steel Supply" at 80 tonnes
- PKG-08 estimate Detail.csv Line L815: "Catwalk Structural Steel Supply" at 25 tonnes
- Total marine steel: 150 + 80 + 25 = 255 tonnes
- PKG-08 notes indicate "marine-grade corrosion protection required" (implies coatings coordination with PKG-26)

**Impacted WBS/CBS:** MAT (L2609), CD (L2620, L2621) for marine coatings

**Estimate Impact:**
- Marine steel surface area: 255 tonnes × 30 m²/tonne = 7,650 m² (per D-2610)
- Marine coating cost: $398k (17% of base estimate)

**Override Path:**
- Verify with PKG-08 marine structures deliverables (DEL-08.01 through DEL-08.10)
- Update tonnage when PKG-08 design is finalized
- Coordinate coating system selection with PKG-08 design requirements

**Source:** PKG-08 estimate (EST_PKG08_DRAFT_2026-01-28_2400) Detail.csv L813, L814, L815

**Confidence:** MED (tonnages from related package estimate; marine coating requirements noted in PKG-08)

---

### D-2615: Engineering Hours Allocation

**Decision:** Allocate engineering hours per deliverable based on complexity and coordination requirements

**Trigger:** No project-specific engineering hour budgets; allowance-based estimate required

**Evidence:**
- DEL-26.01 (Specification): 100 hours × $250/hr = $25k (most complex; 5 coating types; performance requirements; standards coordination)
- DEL-26.02 (Procedures): 80 hours × $250/hr = $20k (surface prep, application, inspection, testing procedures for 5 coating types)
- DEL-26.03 (Data Sheets): 40 hours × $250/hr = $10k (compilation and organization; manufacturer data sheet review)
- DEL-26.04 (Records): 60 hours × $250/hr = $15k (QA/QC templates; inspection records; acceptance testing)
- Engineering Coordination: 90 hours × $245/hr = $22k (PKG-06, PKG-08, PKG-13, PKG-27, PKG-30, PKG-33 interfaces)
- Total: ~370 hours; $92k

**Impacted WBS/CBS:** E (L2601, L2602, L2603, L2604, L2605)

**Estimate Impact:** Engineering = $92k (3.8% of base estimate); 100% allowance-based; no vendor data sheets available

**Override Path:**
- Complete DEL-26.01 through DEL-26.04 and track actual hours
- Update engineering estimates based on actual effort in future iterations

**Source:** Allowance-based; engineering judgment; similar deliverable estimates from other packages

**Confidence:** LOW (no project-specific precedent; high variability depending on coordination complexity and regulatory requirements)

---

**Total Decisions:** 15 (D-2601 through D-2615)

**Decision Impact Summary:**
- Currency, pricing date, rounding: Establishes estimate basis; standard project conventions
- Scope, contingency, escalation: Per _CONFIG.md; consistent with other packages
- Fallback model: Indirects/PM/COM factors due to lack of project-specific data; $371k impact (15% of base)
- Quantity derivation: Tank areas from PKG-13; steel tonnages from PKG-06/PKG-08; surface area factors assumed; $1,541k impact (64% of base)
- Contingency adjustments: Allowance-heavy buckets receive higher contingency; +$117k contingency
- Engineering allocation: Allowance-based; $92k estimate (3.8% of base)

---

**End of Decision Log**
