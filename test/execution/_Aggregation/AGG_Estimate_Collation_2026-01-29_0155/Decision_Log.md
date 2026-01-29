# Aggregated Decision Log


---

## PKG-00

# Decision Log — PKG-00 Site Establishment Estimate

**Snapshot ID:** EST_PKG00_DRAFT_2026-01-28_2315
**Package Scope:** PKG-00 Site Establishment
**Date:** 2026-01-28

---

## D-001: Estimate Scope — Package-Level Estimating

**Decision:** Create separate estimates by package rather than single project-wide estimate.

**Trigger:** Project instructions (INIT.md) specify phased work by package: "Progress one deliverable at a time until all deliverables in that package are complete. Only complete one package at a time."

**Evidence:** `/Users/ryan/ai-env/projects/chirality-app/INIT.md`, lines 3-11.

**Impacted WBS/CBS:** All packages (PKG-00 through PKG-35). This estimate covers PKG-00 only.

**Estimate Impact:** This estimate is a subset of the full project. Indirects, project management, and other cross-package costs are allocated proportionally to PKG-00.

**Override Path:** To create full project estimate, modify scope in `_CONFIG.md` to include all packages.

---

## D-002: Currency Selection — CAD

**Decision:** Use Canadian dollars (CAD) as the estimate currency.

**Trigger:** Default currency selection per AGENT_ESTIMATING protocol (Phase 1.3).

**Evidence:** Project location is Fraser Surrey Terminal, 11060 Elevator Road, Surrey, BC (decomposition Section 1, line 10). Canadian location indicates CAD currency.

**Impacted WBS/CBS:** All line items.

**Estimate Impact:** All costs expressed in CAD. No currency conversion required for Canadian vendors/rates.

**Override Path:** Set `currency` parameter in `_CONFIG.md` if different currency required.

---

## D-003: Pricing Date — January 2026

**Decision:** Use January 2026 as the pricing date ("dollars of" month).

**Trigger:** No explicit pricing date found in deliverable documents. Default to current date per AGENT_ESTIMATING protocol.

**Evidence:** Current date is 2026-01-28. No historical pricing dates referenced in deliverable `_REFERENCES.md` files.

**Impacted WBS/CBS:** All line items.

**Estimate Impact:** Costs represent January 2026 pricing. No escalation applied (escalation_mode = NONE per config).

**Override Path:** Set `pricing_date` parameter in `_CONFIG.md` if different pricing basis required.

---

## D-004: Workspace Paths — Default Paths Used

**Decision:** Use default workspace paths specified in AGENT_ESTIMATING instructions.

**Trigger:** Initialization Phase 1.1 — auto-discovery of project paths.

**Evidence:**
- Project workspace: `/Users/ryan/ai-env/projects/chirality-app/test/`
- Execution root: `/Users/ryan/ai-env/projects/chirality-app/test/execution/`
- Decomposition: `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md`
- Estimates output: `/Users/ryan/ai-env/projects/chirality-app/test/execution/_Estimates/`

All paths verified as accessible.

**Impacted WBS/CBS:** N/A (infrastructure decision).

**Estimate Impact:** None (path selection does not affect cost values).

**Override Path:** Paths can be overridden via conversation if project structure changes.

---

## D-005: Source Priority — No Project-Specific Pricing Sources Found

**Decision:** Use fallback typical model for pricing due to absence of project-specific quotes, budgets, or rate tables.

**Trigger:** Source discovery (Phase 2.2) found no vendor quotes, budgetary proposals, or project rate tables in deliverable `_REFERENCES.md` files or `_Estimates/_RateTables/` directory.

**Evidence:**
- All deliverable `_REFERENCES.md` files state "no references identified yet" or list only the decomposition document
- `_Estimates/_RateTables/` directory is empty (created during initialization)
- No pricing documents discovered in PKG-00 deliverable folders

**Impacted WBS/CBS:** All CBS buckets.

**Estimate Impact:** HIGH — All line items will use fallback allowances or parametric models with LOW confidence ratings. Estimate totals will have wide uncertainty ranges.

**Override Path:** To improve estimate accuracy:
1. Add vendor quotes to deliverable `_REFERENCES.md` files or place quote files in deliverable folders
2. Add rate tables (CSV, XLSX, or MD format) to `_Estimates/_RateTables/` directory
3. Re-run estimate pipeline

---

## D-006: Indirects Model — Factor-Based (No Schedule Data)

**Decision:** Apply indirects using factor-based model rather than time-based model.

**Trigger:** No construction schedule or duration data discovered in deliverable documents.

**Evidence:** Deliverable `Procedure.md` and `Guidance.md` files reference project duration as "multi-year EPC project" and provide example equipment mobilization/demobilization spanning 52 weeks, but no detailed project schedule or critical path was found.

**Impacted WBS/CBS:** Construction Indirects (CI), Project Management (PM), Commissioning (COM).

**Estimate Impact:** Indirects calculated as factors of Construction Directs (CD) and Materials (MAT) using fallback typical model defaults.

**Override Path:** Provide detailed construction schedule to enable time-based indirects calculation (staffing levels × duration).

---

## D-007: Rounding Policy — Nearest $1,000

**Decision:** Round estimate totals to nearest $1,000 CAD.

**Trigger:** Default rounding policy per AGENT_ESTIMATING protocol and `_CONFIG.md` setting.

**Evidence:** `_CONFIG.md`, rounding = 1000.

**Impacted WBS/CBS:** Summary totals only (detail line items retain calculated precision).

**Estimate Impact:** Minimal — rounding affects presentation only, not line item accuracy.

**Override Path:** Modify `rounding` parameter in `_CONFIG.md` (e.g., 10000 for $10k rounding, 100 for $100 rounding).

---

## D-008: Contingency Method — Percentage by Bucket (PCT_BY_BUCKET)

**Decision:** Apply contingency using percentage-by-CBS-bucket method with allowance-heavy adjustment.

**Trigger:** Default contingency method per AGENT_ESTIMATING protocol and `_CONFIG.md` setting.

**Evidence:** `_CONFIG.md`, contingency_method = PCT_BY_BUCKET. Risk-based three-point estimation not feasible without vendor quotes and project-specific risk data.

**Impacted WBS/CBS:** All CBS buckets — contingency calculated separately for E, PM, P, MAT, CD, CI, COM.

**Estimate Impact:** Contingency will be higher for buckets with high allowance share (due to low confidence in fallback pricing).

**Override Path:**
1. Set `contingency_method = RISK_BASED` in `_CONFIG.md` to enable three-point estimation
2. Provide vendor quotes and project-specific risk data to support risk-based model

---

## D-009: Escalation — Not Applied

**Decision:** Do not apply escalation to this estimate.

**Trigger:** Default escalation mode per AGENT_ESTIMATING protocol and `_CONFIG.md` setting (escalation_mode = NONE).

**Evidence:** No cashflow curve or expenditure schedule discovered. Pricing date (2026-01) represents current pricing; no forward escalation required for draft estimate.

**Impacted WBS/CBS:** All line items (escalation = 0%).

**Estimate Impact:** Estimate represents January 2026 dollars without adjustment for future price changes.

**Override Path:**
1. Set `escalation_mode = EXPLICIT` in `_CONFIG.md`
2. Provide construction schedule with cashflow curve to enable escalation calculation

---

## Decision Summary Table

| Decision ID | Topic | Selection | Confidence | Impact Level |
|-------------|-------|-----------|------------|--------------|
| D-001 | Scope | PKG-00 only | HIGH | HIGH |
| D-002 | Currency | CAD | HIGH | MED |
| D-003 | Pricing Date | 2026-01 | MED | MED |
| D-004 | Paths | Defaults | HIGH | NONE |
| D-005 | Sources | Fallback model | LOW | HIGH |
| D-006 | Indirects | Factor-based | MED | MED |
| D-007 | Rounding | $1,000 | HIGH | LOW |
| D-008 | Contingency | PCT_BY_BUCKET | MED | MED |
| D-009 | Escalation | NONE | HIGH | LOW |

---

**Total Decisions Recorded:** 9


---

## PKG-01

# Decision Log — PKG-01 Demolition & Removals Estimate

**Snapshot ID:** EST_PKG01_DRAFT_2026-01-28_2330
**Package Scope:** PKG-01 Demolition & Removals
**Date:** 2026-01-28

---

## D-010: Estimate Scope — PKG-01 Only

**Decision:** Create estimate for PKG-01 Demolition & Removals only.

**Trigger:** Project instructions (INIT.md) specify phased work by package.

**Evidence:** `/Users/ryan/ai-env/projects/chirality-app/INIT.md`, lines 3-6; continuation of package-by-package estimating approach established in D-001 (PKG-00 estimate).

**Impacted WBS/CBS:** PKG-01 (4 deliverables: DEL-01.01 through DEL-01.04).

**Estimate Impact:** This estimate covers only PKG-01 demolition scope. Indirects and PM allocated proportionally.

**Override Path:** To create full project estimate, modify scope in `_CONFIG.md` to include all packages.

---

## D-011: Currency Selection — CAD (Inherited)

**Decision:** Use Canadian dollars (CAD) as the estimate currency.

**Trigger:** Inherited from PKG-00 estimate basis (D-002) and `_CONFIG.md`.

**Evidence:** Project location is Fraser Surrey Terminal, Surrey, BC. `_CONFIG.md` specifies `currency = CAD`.

**Impacted WBS/CBS:** All line items.

**Estimate Impact:** All costs expressed in CAD.

**Override Path:** Set `currency` parameter in `_CONFIG.md`.

---

## D-012: Pricing Date — January 2026 (Inherited)

**Decision:** Use January 2026 as the pricing date.

**Trigger:** Inherited from PKG-00 estimate basis (D-003) and `_CONFIG.md`.

**Evidence:** `_CONFIG.md` specifies `pricing_date = 2026-01`.

**Impacted WBS/CBS:** All line items.

**Estimate Impact:** Costs represent January 2026 pricing.

**Override Path:** Set `pricing_date` parameter in `_CONFIG.md`.

---

## D-013: Source Priority — No Project-Specific Pricing Sources Found

**Decision:** Use fallback typical model for pricing due to absence of project-specific quotes, budgets, or rate tables.

**Trigger:** Source discovery found no vendor quotes, budgetary proposals, or project rate tables in PKG-01 deliverable folders or `_Estimates/_RateTables/` directory.

**Evidence:**
- All PKG-01 deliverable `_REFERENCES.md` files reference only the decomposition document
- `_Estimates/_RateTables/` directory is empty
- No demolition contractor quotes or marine removal quotes discovered

**Impacted WBS/CBS:** All CBS buckets.

**Estimate Impact:** HIGH — All line items will use fallback allowances with LOW confidence. Demolition costs are highly site-specific and require contractor quotes for accuracy.

**Override Path:**
1. Obtain demolition contractor budgetary quotes (Track 6, Dolphin 2)
2. Obtain marine contractor quote for Dolphin 2 marine work
3. Add rate tables or quotes to `_Estimates/_RateTables/` or deliverable folders
4. Re-run estimate pipeline

---

## D-014: Demolition Scope Breakdown — Structure-Based Estimation

**Decision:** Estimate demolition costs by major structure: Track 6 (rail), Dolphin 2 (marine), fencing, salt tent.

**Trigger:** Decomposition PKG-01 scope explicitly identifies these four demolition items with distinct work types requiring different methods and equipment.

**Evidence:** Decomposition PKG-01 scope: "Removal and disposal of existing infrastructure including Track 6, Dolphin 2, fencing, salt tent dismantling, and associated decommissioning."

**Impacted WBS/CBS:** CD (Construction Directs), MAT (Materials for disposal/protection).

**Estimate Impact:** Four separate allowance line items for construction directs, sized based on typical demolition work complexity:
- Track 6: Rail infrastructure (moderate complexity, specialized equipment)
- Dolphin 2: Marine structure (high complexity, marine equipment required)
- Fencing: Simple removal (low complexity)
- Salt tent: Building structure (moderate complexity)

**Override Path:** Provide structure-specific quantities (linear feet of track, pile count for dolphin, linear feet of fencing, tent dimensions) to enable quantity-based pricing.

---

## D-015: Dolphin 2 Marine Demolition — Marine Equipment Requirement

**Decision:** Dolphin 2 demolition requires marine equipment (barge, crane) and is estimated as a marine construction operation with higher unit costs.

**Trigger:** Structure type (marine dolphin) and location require over-water demolition operations.

**Evidence:** DEL-01.03 Datasheet.md specifies Dolphin 2 removal procedure requires "marine equipment mobilization (barge, crane)" and "marine traffic coordination, tide/weather assessment, marine safety zone establishment."

**Impacted WBS/CBS:** CD (Dolphin 2 line item).

**Estimate Impact:** Dolphin 2 allowance sized higher than land-based demolition to account for marine equipment mob/demob, marine crew, weather sensitivity, and marine safety requirements. Confidence is LOW due to lack of marine contractor quote.

**Override Path:** Obtain marine demolition contractor budgetary quote with scope specific to Dolphin 2 structure (pile count, deck area, access conditions).

---

## D-016: Hazardous Materials — Status Unknown

**Decision:** Exclude hazardous materials abatement costs from base estimate; add placeholder allowance for potential contamination.

**Trigger:** Deliverable documents indicate hazardous materials presence is TBD pending survey.

**Evidence:** DEL-01.02 Datasheet.md states "Hazardous materials: TBD (presence and extent of hazardous materials in existing structures to be demolished)." DEL-01.02 Specification R21 addresses special disposal requirements for hazardous materials "if present."

**Impacted WBS/CBS:** CD (potential hazmat abatement), MAT (disposal costs).

**Estimate Impact:** A contingency placeholder is included for potential hazardous materials discovery. If hazmat survey identifies asbestos, lead, or contaminated materials, costs could increase significantly.

**Override Path:** Complete hazardous materials survey prior to estimate finalization. If hazmat present, add abatement costs and licensed hazmat contractor costs.

---

## D-017: Indirects Model — Factor-Based (Inherited)

**Decision:** Apply indirects using factor-based model.

**Trigger:** Inherited from PKG-00 estimate basis (D-006). No schedule data available for time-based calculation.

**Evidence:** No construction schedule with PKG-01 duration. Deliverable Procedure.md documents do not specify demolition duration.

**Impacted WBS/CBS:** CI, PM, P.

**Estimate Impact:** Indirects calculated as factors of CD and MAT per fallback model.

**Override Path:** Provide PKG-01 demolition schedule duration to enable time-based indirects.

---

## D-018: Contingency Method — PCT_BY_BUCKET (Inherited)

**Decision:** Apply contingency using percentage-by-CBS-bucket method with allowance-heavy adjustment.

**Trigger:** Inherited from PKG-00 estimate basis (D-008) and `_CONFIG.md`.

**Evidence:** `_CONFIG.md` specifies `contingency_method = PCT_BY_BUCKET`. 100% of PKG-01 estimate is ALLOWANCE-based, triggering maximum allowance adjustment.

**Impacted WBS/CBS:** All CBS buckets.

**Estimate Impact:** Higher contingency applied due to 100% allowance-based estimate (baseline + 10% allowance adjustment).

**Override Path:** Obtain vendor quotes to reduce allowance share and corresponding contingency.

---

## Decision Summary Table

| Decision ID | Topic | Selection | Confidence | Impact Level |
|-------------|-------|-----------|------------|--------------|
| D-010 | Scope | PKG-01 only | HIGH | HIGH |
| D-011 | Currency | CAD (inherited) | HIGH | MED |
| D-012 | Pricing Date | 2026-01 (inherited) | MED | MED |
| D-013 | Sources | Fallback model | LOW | HIGH |
| D-014 | Structure Breakdown | 4 structures | MED | MED |
| D-015 | Dolphin 2 | Marine equipment | MED | HIGH |
| D-016 | Hazmat | Unknown (excluded) | LOW | HIGH |
| D-017 | Indirects | Factor-based | MED | MED |
| D-018 | Contingency | PCT_BY_BUCKET | MED | MED |

---

**Total Decisions Recorded:** 9


---

## PKG-02

# Decision Log

## PKG-02 Earthworks & Ground Improvement Estimate

| ID | Decision Statement | Trigger | Evidence | Impacted WBS/CBS | Estimate Impact | Override Method |
|----|-------------------|---------|----------|------------------|-----------------|-----------------|
| D-001 | Currency set to CAD | Config default validation | Project location: Surrey, BC, Canada per decomposition Section 1 | All | Currency basis | Update _CONFIG.md currency |
| D-002 | Geotechnical investigation assumed Contractor responsibility | Missing scope clarity | D&B contract type per decomposition; DEL-02.04 scope description | PKG-02 / E, CD | ~$150k investigation allowance | Confirm scope in ER |
| D-003 | Survey work assumed Contractor responsibility | Missing scope clarity | D&B contract type; DEL-02.05 scope description | PKG-02 / E | ~$60k survey allowance | Confirm scope in ER |
| D-004 | Ground improvement assumed required | No geotechnical data | Fraser River delta location typically requires ground improvement | PKG-02 / MAT, CD | ~$1.5M ground improvement allowance | Provide geotechnical data |
| D-005 | Productivity factor set to 1.0 | No site-specific data | BC lower mainland baseline; urban industrial site | CD, CI | Base labor rates | Provide site conditions data |
| D-006 | Standard site access assumed | No access constraints documented | Elevator Road access per project location | CD | No adjustment | Document access restrictions |
| D-007 | Standard work shifts assumed (8-10 hr) | No schedule constraints | Typical D&B construction | CD, CI | Base rates | Provide schedule constraints |
| D-008 | All pricing via allowances | No vendor quotes or rate tables found | Searched _RateTables/ and deliverable references | All | LOW confidence on all lines | Provide quotes and rate tables |
| D-009 | Indirects factors applied from fallback model | No project-specific factors | CI=18%, P=2%, PM=6%, COM=3% per AGENT_ESTIMATING.md | CI, P, PM, COM | ~$700k indirect costs | Provide project factor schedule |
| D-010 | Contingency elevated for allowance-heavy estimate | 100% allowance-based | +10% above baseline per fallback model rules | CONT | ~30% average contingency | Improve pricing basis |
| D-011 | No escalation applied | Config setting | escalation_mode = NONE | All | $0 escalation | Update config if needed |
| D-012 | Site area estimated at 5 hectares | No survey data | Typical for 3-tank farm + rail unloading facility of this scale | PKG-02 / CD | Earthwork quantity basis | Provide survey/layout |
| D-013 | Cut/fill volume estimated at 25,000 m³ | No design quantities | Typical for industrial facility of this scope on delta site | PKG-02 / CD, MAT | Earthwork cost basis | Provide cut/fill takeoff |
| D-014 | Ground improvement area estimated at 3 hectares | No geotechnical design | Tank foundations + pump area likely need improvement | PKG-02 / CD, MAT | Ground improvement cost basis | Provide geotechnical design |


---

## PKG-03

# Decision Log

## Snapshot Identification

| Field | Value |
|-------|-------|
| Snapshot ID | EST_PKG03_DRAFT_2026-01-28_2330 |
| Package | PKG-03 Underground Utilities & Drainage |
| Date | 2026-01-28 |

## Decision Entries

### D-001: Currency Selection

**Decision:** Use CAD (Canadian dollars) for this estimate.

**Trigger:** Currency not explicitly stated in deliverables; required for estimate execution.

**Evidence:**
- Project location is Fraser Surrey Terminal, 11060 Elevator Road, Surrey, BC, Canada (Source: decomposition Section 1)
- Config file `/Users/ryan/ai-env/projects/chirality-app/test/execution/_Estimates/_CONFIG.md` specifies `currency: CAD`

**Impacted WBS/CBS:** All packages and CBS buckets (currency applies to entire estimate)

**Estimate Impact:** All costs expressed in CAD; no currency conversion required

**Override Path:** Modify `_CONFIG.md` if different currency is required

---

### D-002: Pricing Date

**Decision:** Use 2026-01 (January 2026) as pricing date.

**Trigger:** Pricing date required for estimate basis and future escalation reference.

**Evidence:**
- Config file specifies `pricing_date: 2026-01`
- Current date is 2026-01-28 (January 2026)

**Impacted WBS/CBS:** All CBS buckets (pricing date applies to all costs)

**Estimate Impact:** Estimate is in "January 2026 dollars"; no escalation applied (escalation_mode = NONE per config)

**Override Path:** Modify `_CONFIG.md` pricing_date if different pricing basis is required

---

### D-003: Estimate Label

**Decision:** Use `PKG03_DRAFT` as estimate label.

**Trigger:** Estimate label required for snapshot identification and tracking.

**Evidence:**
- Following established pattern from previous packages (PKG00_DRAFT, PKG01_DRAFT, PKG02_DRAFT per _LATEST.md)
- Config file lists `estimate_label: PKG00_DRAFT` (package-specific labels per snapshot)

**Impacted WBS/CBS:** N/A (metadata only)

**Estimate Impact:** None (label is for identification only)

**Override Path:** Provide different label via config or user instruction for next run

---

### D-004: Scope Inclusions

**Decision:** Include Engineering (E), PM, Procurement (P), Materials (MAT), Construction Directs (CD), Construction Indirects (CI), Commissioning (COM).

**Trigger:** CBS scope definition required for estimate coverage.

**Evidence:**
- Config file specifies include scopes list
- PKG-03 scope includes design deliverables (engineering), equipment/materials (procurement, materials), installation (construction), testing (commissioning) per decomposition

**Impacted WBS/CBS:** All CBS buckets except excluded scopes

**Estimate Impact:** Estimate includes full EPC coverage for contractor scope

**Override Path:** Modify `_CONFIG.md` include_scopes/exclude_scopes if different coverage is required

---

### D-005: Scope Exclusions

**Decision:** Exclude Owner's costs, land acquisition, financing costs, permits obtained by Employer.

**Trigger:** Exclusions required for estimate boundary definition.

**Evidence:**
- Config file specifies exclude scopes
- Decomposition Section 1.2 Scope Focus confirms "Contractor's scope of work only. Employer-responsible items (permits obtained by Employer, nitrogen skid supply) are excluded except for interface connections."

**Impacted WBS/CBS:** N/A (exclusions)

**Estimate Impact:** Permits obtained by Employer are not costed; Contractor scope only

**Override Path:** Review decomposition Section 1.2 if scope boundary changes

---

### D-006: Contingency Method

**Decision:** Use `PCT_BY_BUCKET` (percentage by CBS bucket) with allowance-based adjustments.

**Trigger:** Contingency method required for risk reserve calculation.

**Evidence:**
- Config file specifies `contingency_method: PCT_BY_BUCKET`
- Fallback typical model (AGENT_ESTIMATING.md STRUCTURE section) defines baseline contingency percentages by CBS bucket and allowance-heavy adjustments

**Impacted WBS/CBS:** Contingency (CONT) applied to all CBS buckets

**Estimate Impact:** Contingency rates elevated due to 100% allowance-based estimate (see Risk_Register.md for bucket-specific rates)

**Override Path:** Modify `_CONFIG.md` contingency_method to RISK_BASED if risk-based contingency is preferred; provide risk data for risk quantification

---

### D-007: Escalation Mode

**Decision:** Use `NONE` (no escalation).

**Trigger:** Escalation mode required for estimate basis definition.

**Evidence:**
- Config file specifies `escalation_mode: NONE`
- Pricing date is current (2026-01); no escalation required for current pricing

**Impacted WBS/CBS:** N/A (no escalation bucket)

**Estimate Impact:** Estimate total does not include escalation; costs are in current January 2026 dollars

**Override Path:** Modify `_CONFIG.md` escalation_mode to EXPLICIT if escalation is required; provide schedule/cashflow curve and escalation factors

---

### D-008: Pricing Method for All Line Items

**Decision:** Use ALLOWANCE method for all line items due to absence of vendor quotes, rate tables, and explicit quantities.

**Trigger:** No pricing sources or explicit quantities available; pricing method required for estimate execution.

**Evidence:**
- Source Index shows 0 vendor quotes, 0 rate tables
- All deliverables in INITIALIZED status with quantities TBD
- Fallback typical model permits allowance-based pricing when sources are not available (AGENT_ESTIMATING.md STRUCTURE section "Placeholder allowance policy")

**Impacted WBS/CBS:** All CBS buckets (Engineering, Materials, Construction Directs, Construction Indirects, PM, Procurement, Commissioning)

**Estimate Impact:** All line items are lump-sum allowances (Qty=1, Unit=LS, UnitRate=Amount); estimate confidence is LOW

**Override Path:** Provide design quantities from DEL-03.01 drawings and vendor quotes for materials/equipment to enable volume-based and quote-based pricing

---

### D-009: Indirects Model Selection

**Decision:** Use factor-based indirects model (fallback typical model).

**Trigger:** No schedule/duration data available; indirects model required for CI, PM, P, COM pricing.

**Evidence:**
- No schedule or duration data discovered in deliverables
- Fallback typical model (AGENT_ESTIMATING.md STRUCTURE section "Default factors") defines factor-based indirects:
  - Construction Indirects (CI) = 0.18 × Construction Directs (CD)
  - Procurement Services (P) = 0.02 × (MAT + FRT)
  - EPCM/PM = 0.06 × (CD + CI + MAT)
  - Commissioning (COM) = 0.03 × (CD + CI + MAT)

**Impacted WBS/CBS:** CI, PM, P, COM buckets

**Estimate Impact:** Indirects are factor-derived based on directs/materials base costs

**Override Path:** Provide project schedule with durations and resource loading to enable time-based indirects pricing

---

### D-010: WBS → CBS Mapping for PKG-03 Deliverables

**Decision:** Map PKG-03 deliverables to CBS buckets as follows:
- DEL-03.01, 03.02, 03.03, 03.04, 03.06 → Engineering (E)
- DEL-03.05 → Construction Indirects (CI) for QA/QC records capture
- Storm drainage materials → Materials (MAT) + Construction Directs (CD)
- OWS equipment → Materials (MAT) + Construction Directs (CD)
- Duct banks → Materials (MAT) + Construction Directs (CD)
- Trenchless crossings → Construction Directs (CD)

**Trigger:** WBS → CBS mapping required for cost categorization.

**Evidence:**
- DEL-03.01 through DEL-03.04 are design deliverables (Drawing, Specification, Calculation, Data Sheet) → Engineering discipline
- DEL-03.05 is QA/QC records → Construction Indirects
- DEL-03.06 is specialist surveyor report → Engineering
- PKG-03 scope includes materials (pipes, OWS, duct bank materials) → Materials bucket
- PKG-03 scope includes installation (excavation, pipe laying, OWS installation, duct bank construction, trenchless boring) → Construction Directs
- Testing and commissioning (pressure testing, CCTV, OWS performance verification) → included in Commissioning bucket via indirects factor

**Impacted WBS/CBS:** All PKG-03 deliverables mapped to E, MAT, CD, CI buckets

**Estimate Impact:** Cost distribution across CBS buckets reflects engineering-heavy (design) + materials/construction (installation) mix

**Override Path:** Review mapping if deliverable types or CBS bucket definitions change

---

### D-011: Allowance Sizing Approach for PKG-03

**Decision:** Size allowances using engineering judgment based on typical underground utilities scope for canola oil transload facility with key parameters:
- 1,000,000 MT/a throughput (decomposition Project Overview)
- 45,000 MT storage in 3 tanks (decomposition Project Overview)
- 32 railcar unloading stations (decomposition Project Overview)
- Storm drainage for tank farm, railcar unloading area, marine loading platform access
- OWS for spill containment and environmental protection
- Duct banks for electrical/communications infrastructure
- Trenchless crossings for rail tracks and existing utilities

**Trigger:** Allowance amounts required for Detail.csv line items; no vendor quotes or quantities available.

**Evidence:**
- Decomposition Section 1.1 Project Overview provides key parameters
- PKG-03 scope description: "Storm drainage, containment water collection, oil-water separator, underground utility routing, trenchless crossing, outfalls"
- Typical underground utilities scope for industrial facility includes:
  - Storm drainage network (several hundred to 1000+ LM of pipe depending on site area)
  - OWS unit (typically 1-2 units for industrial facility of this scale)
  - Duct banks (several hundred LM of conduit for electrical/comms)
  - Trenchless crossings (5-10 crossings for rail/road/existing utility conflicts)

**Impacted WBS/CBS:** MAT, CD buckets (materials and construction allowances)

**Estimate Impact:** Allowance amounts sized to order-of-magnitude for budgeting purposes; confidence LOW pending design quantities

**Override Path:** Provide design quantities from DEL-03.01 drawings and calculations from DEL-03.03 to replace allowances with volume-based estimates

---

### D-012: Engineering Allowance Sizing for PKG-03

**Decision:** Size engineering allowance based on typical engineering effort for underground utilities package with 6 deliverables (4 design deliverables + 2 record deliverables).

**Trigger:** Engineering cost required for E bucket; no labor hours or rates available.

**Evidence:**
- PKG-03 has 6 deliverables: 1 drawing set, 1 specification, 1 calculation package, 1 data sheet package, 1 installation records, 1 CCTV survey report
- Typical engineering effort for underground utilities includes:
  - Civil engineers (senior, intermediate) for design, calculations, specifications
  - CAD technicians for drawing production
  - QA/QC reviewers for interdisciplinary and independent checks
  - Specialist surveyors for CCTV survey
- Comparable package PKG-02 (9 deliverables, earthworks scope) had Engineering = $268,500 CAD (per _LATEST.md)
- PKG-03 has fewer deliverables (6 vs 9) but includes specialist CCTV survey and OWS environmental engineering

**Impacted WBS/CBS:** E bucket (Engineering)

**Estimate Impact:** Engineering allowance sized based on deliverable count and scope complexity

**Override Path:** Provide engineering labor hours breakdown by discipline and deliverable to enable hour-based engineering estimate

---


---

## PKG-04

# Decision Log

## PKG-04 Pavement & Surfacing Estimate

| ID | Decision Statement | Trigger | Evidence | Impacted WBS/CBS | Estimate Impact | How to Override |
|----|-------------------|---------|----------|------------------|-----------------|-----------------|
| D-001 | Currency set to CAD (Canadian dollars) | Default selection required | Project location: Fraser Surrey Terminal, Surrey, BC, Canada per decomposition Section 1 | All | All amounts | Set `currency` in _CONFIG.md |
| D-002 | Subgrade preparation assumed complete by PKG-02 Earthworks prior to PKG-04 | Scope boundary clarification | Decomposition shows PKG-02 Earthworks & Ground Improvement separate from PKG-04 | PKG-04 / CD | Excludes earthworks costs | Include subgrade if scope changes |
| D-003 | Drainage infrastructure assumed by PKG-03 Underground Utilities | Scope boundary clarification | Decomposition shows PKG-03 Underground Utilities & Drainage separate from PKG-04 | PKG-04 interface | Drainage tie-ins only | Include drainage if scope changes |
| D-004 | Productivity factor set to 1.0 (BC lower mainland baseline) | No site-specific productivity data | Project location in established industrial area | PKG-04 / CD | Labor rates | Provide site-specific productivity factors |
| D-005 | Site access assumed standard via Elevator Road | No access constraints identified | Decomposition Section 1 location description | PKG-04 / CD | No access premiums | Provide access study if constraints exist |
| D-006 | Working hours assumed standard 8-10 hour shifts | No shift schedule provided | Typical industrial construction | PKG-04 / CD, CI | Labor productivity | Provide project schedule/shift requirements |
| D-007 | All pricing via allowances (fallback typical model) | No vendor quotes or rate tables available | Source index search returned no pricing sources | All | 100% allowance basis | Provide vendor quotes or rate tables |
| D-008 | Indirects factors applied per fallback typical model (CI 18%, PM 6%, P 2%, COM 3%) | No project-specific indirects data | Fallback typical model per AGENT_ESTIMATING STRUCTURE | CI, PM, P, COM | $700,000 indirects | Provide project-specific indirects |
| D-009 | Contingency rates elevated due to 100% allowance-based estimate (+10% on direct CBS, +5% on factors) | High uncertainty in allowance-based estimate | Per AGENT_ESTIMATING fallback contingency method | CONT | 27% weighted contingency | Reduce allowance share with quotes |
| D-010 | Escalation mode set to NONE | Default selection | Pricing date is current (January 2026) | All | No escalation | Set `escalation_mode` in _CONFIG.md |
| D-011 | Survey and grade control allowance of $25,000 for layout and verification | No survey scope defined | Required for pavement construction quality | PKG-04 / CD | $25,000 | Provide survey scope/quote |


---

## PKG-05

# Decision Log — PKG-05 Concrete Structures Estimate

**Snapshot ID:** EST_PKG05_DRAFT_2026-01-28_2400
**Package Scope:** PKG-05 Concrete Structures
**Date:** 2026-01-28

---

## D-001: Estimate Scope — Package-Level Estimating

**Decision:** Create separate estimates by package rather than single project-wide estimate.

**Trigger:** Project instructions (INIT.md) specify phased work by package: "Progress one deliverable at a time until all deliverables in that package are complete. Only complete one package at a time."

**Evidence:** `/Users/ryan/ai-env/projects/chirality-app/INIT.md`, lines 3-11.

**Impacted WBS/CBS:** All packages (PKG-00 through PKG-35). This estimate covers PKG-05 only.

**Estimate Impact:** This estimate is a subset of the full project. Indirects, project management, and other cross-package costs are allocated proportionally to PKG-05.

**Override Path:** To create full project estimate, modify scope in `_CONFIG.md` to include all packages.

---

## D-002: Currency Selection — CAD

**Decision:** Use Canadian dollars (CAD) as the estimate currency.

**Trigger:** Default currency selection per AGENT_ESTIMATING protocol (Phase 1.3).

**Evidence:** Project location is Fraser Surrey Terminal, 11060 Elevator Road, Surrey, BC (decomposition Section 1, line 10). Canadian location indicates CAD currency.

**Impacted WBS/CBS:** All line items.

**Estimate Impact:** All costs expressed in CAD. No currency conversion required for Canadian vendors/rates.

**Override Path:** Set `currency` parameter in `_CONFIG.md` if different currency required.

---

## D-003: Pricing Date — January 2026

**Decision:** Use January 2026 as the pricing date ("dollars of" month).

**Trigger:** No explicit pricing date found in deliverable documents. Default to current date per AGENT_ESTIMATING protocol.

**Evidence:** Current date is 2026-01-28. No historical pricing dates referenced in deliverable `_REFERENCES.md` files.

**Impacted WBS/CBS:** All line items.

**Estimate Impact:** Costs represent January 2026 pricing. No escalation applied (escalation_mode = NONE per config).

**Override Path:** Set `pricing_date` parameter in `_CONFIG.md` if different pricing basis required.

---

## D-004: Workspace Paths — Default Paths Used

**Decision:** Use default workspace paths specified in AGENT_ESTIMATING instructions.

**Trigger:** Initialization Phase 1.1 — auto-discovery of project paths.

**Evidence:**
- Project workspace: `/Users/ryan/ai-env/projects/chirality-app/test/`
- Execution root: `/Users/ryan/ai-env/projects/chirality-app/test/execution/`
- Decomposition: `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md`
- Estimates output: `/Users/ryan/ai-env/projects/chirality-app/test/execution/_Estimates/`

All paths verified as accessible.

**Impacted WBS/CBS:** N/A (infrastructure decision).

**Estimate Impact:** None (path selection does not affect cost values).

**Override Path:** Paths can be overridden via conversation if project structure changes.

---

## D-005: Source Priority — No Project-Specific Pricing Sources Found

**Decision:** Use fallback typical model for pricing due to absence of project-specific quotes, budgets, or rate tables.

**Trigger:** Source discovery (Phase 2.2) found no vendor quotes, budgetary proposals, or project rate tables in deliverable `_REFERENCES.md` files or `_Estimates/_RateTables/` directory.

**Evidence:**
- All PKG-05 deliverable `_REFERENCES.md` files list only the decomposition document
- `_Estimates/_RateTables/` directory is empty
- No pricing documents discovered in PKG-05 deliverable folders

**Impacted WBS/CBS:** All CBS buckets.

**Estimate Impact:** HIGH — All line items will use fallback allowances or parametric models with LOW confidence ratings. Estimate totals will have wide uncertainty ranges.

**Override Path:** To improve estimate accuracy:
1. Add vendor quotes for concrete supply, rebar supply, formwork systems
2. Add rate tables (CSV, XLSX, or MD format) to `_Estimates/_RateTables/` directory
3. Re-run estimate pipeline

---

## D-006: Indirects Model — Factor-Based (No Schedule Data)

**Decision:** Apply indirects using factor-based model rather than time-based model.

**Trigger:** No construction schedule or duration data discovered in deliverable documents.

**Evidence:** Deliverable documents reference project duration assumptions but no detailed schedule or critical path was found.

**Impacted WBS/CBS:** Construction Indirects (CI), Project Management (PM).

**Estimate Impact:** Indirects calculated as factors of Construction Directs (CD) and Materials (MAT) using fallback typical model defaults.

**Override Path:** Provide detailed construction schedule to enable time-based indirects calculation (staffing levels × duration).

---

## D-007: Rounding Policy — Nearest $1,000

**Decision:** Round estimate totals to nearest $1,000 CAD.

**Trigger:** Default rounding policy per AGENT_ESTIMATING protocol and `_CONFIG.md` setting.

**Evidence:** `_CONFIG.md`, rounding = 1000.

**Impacted WBS/CBS:** Summary totals only (detail line items retain calculated precision).

**Estimate Impact:** Minimal — rounding affects presentation only, not line item accuracy.

**Override Path:** Modify `rounding` parameter in `_CONFIG.md` (e.g., 10000 for $10k rounding, 100 for $100 rounding).

---

## D-008: Contingency Method — Percentage by Bucket (PCT_BY_BUCKET)

**Decision:** Apply contingency using percentage-by-CBS-bucket method with allowance-heavy adjustment.

**Trigger:** Default contingency method per AGENT_ESTIMATING protocol and `_CONFIG.md` setting.

**Evidence:** `_CONFIG.md`, contingency_method = PCT_BY_BUCKET. Risk-based three-point estimation not feasible without vendor quotes and project-specific risk data.

**Impacted WBS/CBS:** All CBS buckets — contingency calculated separately for E, PM, P, MAT, CD, CI.

**Estimate Impact:** Contingency will be higher for buckets with high allowance share (due to low confidence in fallback pricing).

**Override Path:**
1. Set `contingency_method = RISK_BASED` in `_CONFIG.md` to enable three-point estimation
2. Provide vendor quotes and project-specific risk data to support risk-based model

---

## D-009: Escalation — Not Applied

**Decision:** Do not apply escalation to this estimate.

**Trigger:** Default escalation mode per AGENT_ESTIMATING protocol and `_CONFIG.md` setting (escalation_mode = NONE).

**Evidence:** No cashflow curve or expenditure schedule discovered. Pricing date (2026-01) represents current pricing; no forward escalation required for draft estimate.

**Impacted WBS/CBS:** All line items (escalation = 0%).

**Estimate Impact:** Estimate represents January 2026 dollars without adjustment for future price changes.

**Override Path:**
1. Set `escalation_mode = EXPLICIT` in `_CONFIG.md`
2. Provide construction schedule with cashflow curve to enable escalation calculation

---

## D-010: Concrete Quantity Basis — Parametric from Tank Parameters

**Decision:** Derive concrete quantities parametrically from known tank and facility parameters.

**Trigger:** No detailed quantity takeoffs available. Deliverables specify 3 × 15,000 MT tanks and 45,000 MT total storage but do not provide foundation/wall dimensions.

**Evidence:**
- Decomposition lines 41-42: Storage Capacity 45,000 MT (3 × 15,000 MT tanks)
- DEL-05.01 Datasheet: Tank foundation layouts, containment walls, equipment pads, thrust blocks
- No dimensioned drawings or QTO available

**Impacted WBS/CBS:** Materials (MAT), Construction Directs (CD) for concrete and rebar.

**Estimate Impact:** Concrete and rebar quantities are parametric estimates based on typical tank foundation/containment proportions. Uncertainty ±40%.

**Override Path:** Provide dimensioned drawings or QTO from DEL-05.01 development.

---

## D-011: Tank Foundation Type — Ring Wall Assumed

**Decision:** Assume ring wall foundations for the 15,000 MT storage tanks (most common for large API 650 tanks).

**Trigger:** Foundation type not specified in deliverables. DEL-05.03 references "Tank foundation calculations" and "Foundation sizing (diameter, thickness)" without specifying type.

**Evidence:** Typical industry practice for 15,000 MT API 650 tanks uses ring wall foundations on properly prepared subgrade. Geotechnical conditions assumed adequate (per PKG-02 earthworks).

**Impacted WBS/CBS:** Materials (MAT), Construction Directs (CD) for tank foundations.

**Estimate Impact:** Ring wall foundation is lower cost than full mat foundation. If mat foundations required (poor soils), costs could increase 50-100%.

**Override Path:** Confirm foundation type from DEL-05.03 design calculations once developed.

---

## Decision Summary Table

| Decision ID | Topic | Selection | Confidence | Impact Level |
|-------------|-------|-----------|------------|--------------|
| D-001 | Scope | PKG-05 only | HIGH | HIGH |
| D-002 | Currency | CAD | HIGH | MED |
| D-003 | Pricing Date | 2026-01 | MED | MED |
| D-004 | Paths | Defaults | HIGH | NONE |
| D-005 | Sources | Fallback model | LOW | HIGH |
| D-006 | Indirects | Factor-based | MED | MED |
| D-007 | Rounding | $1,000 | HIGH | LOW |
| D-008 | Contingency | PCT_BY_BUCKET | MED | MED |
| D-009 | Escalation | NONE | HIGH | LOW |
| D-010 | Quantities | Parametric | LOW | HIGH |
| D-011 | Tank Foundation | Ring wall | MED | MED |

---

**Total Decisions Recorded:** 11


---

## PKG-06

# Decision Log

## Snapshot ID
EST_PKG06_DRAFT_2026-01-28_2333

## Purpose
This log records all decisions made by the estimating agent during the straight-through pipeline run for PKG-06 Structural Steelwork.

---

## D-001: Currency Selection

**Decision:** CAD (Canadian dollars)

**Trigger:** No explicit currency override in config; must select single currency for snapshot.

**Evidence:**
- Project location: Fraser Surrey Terminal, Surrey, BC, Canada (decomposition Section 1)
- File: `test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md`

**Impacted WBS/CBS:** All packages and CBS buckets

**Estimate Impact:** All line items priced in CAD; no currency conversion required.

**Override Path:** Specify `currency: USD` (or other) in `execution/_Estimates/_CONFIG.md` if CAD is incorrect.

---

## D-002: Pricing Date

**Decision:** 2026-01 (January 2026 dollars)

**Trigger:** No explicit pricing date in config or source documents.

**Evidence:** Current date (2026-01-28); no historical pricing basis found.

**Impacted WBS/CBS:** All

**Estimate Impact:** Pricing basis is current month; no escalation applied (escalation_mode = NONE).

**Override Path:** Specify `pricing_date: YYYY-MM` in config if different basis is required.

---

## D-003: Estimate Label

**Decision:** PKG06_DRAFT

**Trigger:** No estimate label specified in config.

**Evidence:** Default label convention per AGENT_ESTIMATING.md (Function 1.3).

**Impacted WBS/CBS:** Metadata only (snapshot identification)

**Estimate Impact:** Snapshot labeled as draft; not for procurement or commitment.

**Override Path:** Specify `estimate_label` in config (e.g., `30PCT`, `IFC`, `BUDGET`).

---

## D-004: CBS Inclusions/Exclusions

**Decision:** Include E, PM, P, MAT, CD, CI, COM, CONT; exclude Owner's costs, land, financing, permits obtained by Employer, escalation, taxes.

**Trigger:** No config override; default inclusion/exclusion per AGENT_ESTIMATING.md (Function 1.3).

**Evidence:**
- Decomposition Section 1.2: Contractor scope only; Employer-responsible items excluded except interfaces.
- AGENT_ESTIMATING.md: default `include_scopes` and `exclude_scopes`.

**Impacted WBS/CBS:** All CBS buckets

**Estimate Impact:** Estimate covers full EPC-style D&B scope; excludes owner/financing items.

**Override Path:** Modify config `include_scopes` / `exclude_scopes` if different scope is required.

---

## D-005: WBS → CBS Mapping for PKG-06

**Decision:** Map PKG-06 deliverables to CBS as follows:
- DEL-06.01 (Drawing Set) → E (Engineering & Design)
- DEL-06.02 (Technical Specification) → E
- DEL-06.03 (Design Calculations) → E
- DEL-06.04 (Data Sheet Package) → E
- DEL-06.05 (Installation & Test Records) → E (QA/documentation effort)

Construction/installation scope (not tied to specific deliverables) → CD, MAT, CI

**Trigger:** Deliverable types indicate engineering/design work; construction is implicit in package scope.

**Evidence:**
- Decomposition PKG-06 deliverables (lines 248-252): types are Drawing, Specification, Calculation, Data Sheet, Record
- Package scope (line 242): steel platforms, stairs, gangways, access structures, handrails, pipe supports

**Impacted WBS/CBS:** All PKG-06 deliverables and construction line items

**Estimate Impact:** Engineering effort separated from materials/construction; allows CBS-based contingency.

**Override Path:** N/A (standard WBS→CBS mapping per deliverable type).

---

## D-006: Productivity and Location Factors

**Decision:** Productivity factor = 1.0 (BC lower mainland baseline); no location adjustment applied.

**Trigger:** No project-specific productivity or location data available.

**Evidence:**
- Location: Fraser Surrey Terminal, Surrey, BC (decomposition)
- Assumption: BC lower mainland is baseline productivity region (no remote/offshore adjustment)

**Impacted WBS/CBS:** CD, CI (construction labor productivity)

**Estimate Impact:** Labor hours and indirects computed using standard BC productivity; no uplift or reduction.

**Override Path:** If site-specific productivity data becomes available (remote access, congestion, working hours constraints), adjust labor hour estimates or apply factor in config.

---

## D-007: Geotechnical/Foundation Interface Assumption

**Decision:** Assume structural steel platforms/pipe racks will be supported on concrete foundations provided under PKG-05 (Concrete Structures). Coordination of foundation loads is external (dependency tracking mode = NOT_TRACKED).

**Trigger:** No explicit foundation design information in PKG-06 deliverables.

**Evidence:**
- PKG-06 scope (decomposition): platforms, stairs, gangways, handrails, pipe supports
- PKG-05 scope (decomposition): concrete structures (likely includes foundations)
- `_DEPENDENCIES.md`: NOT_TRACKED

**Impacted WBS/CBS:** PKG-06 MAT, CD (structural steel erection assumes foundations are ready)

**Estimate Impact:** Structural steel estimate does not include foundation costs (those are in PKG-05).

**Override Path:** Confirm foundation responsibility via cross-package coordination (outside estimating agent scope).

---

## D-008: Pricing Basis Selection (All Allowances)

**Decision:** All PKG-06 line items priced via allowances using fallback typical model.

**Trigger:** No vendor quotes or rate tables available; explicit quantities (tonnage, counts) not yet defined in deliverables (TBD status).

**Evidence:**
- Source_Index.md: no quotes, no rate tables, no design drawings with quantities
- Deliverables status: INITIALIZED (quantities TBD pending design)

**Impacted WBS/CBS:** All CBS buckets (E, MAT, CD, CI, PM, P, COM)

**Estimate Impact:** All line items have Method=ALLOWANCE or Method=PARAMETRIC; Confidence=LOW. Contingency percentages elevated per allowance-heavy adjustment (AGENT_ESTIMATING.md, STRUCTURE: Fallback Typical Model).

**Override Path:** Provide structural steel design drawings (with tonnages, counts, sizes), vendor quotes, or project rate tables to replace allowances with quantity-based pricing in next run.

---

## D-009: Indirects/Services Factors (Fallback Model)

**Decision:** Apply factor-based indirects per fallback typical model:
- CI (Construction Indirects) = 0.18 × CD
- P (Procurement Services) = 0.02 × MAT
- PM (EPCM/Project Management) = 0.06 × (CD + CI + MAT)
- COM (Commissioning) = 0.03 × (CD + CI + MAT)

**Trigger:** No time-based schedule or project-specific indirects model available.

**Evidence:** AGENT_ESTIMATING.md, STRUCTURE: Fallback Typical Model (default factors).

**Impacted WBS/CBS:** CI, P, PM, COM

**Estimate Impact:** Indirects/services are parametric (factor-derived); not based on project schedule or org chart.

**Override Path:** Provide project schedule with durations, staffing plan, or project-specific indirects rates in config/rate tables.

---

## D-010: Contingency Method and Percentages

**Decision:** Use PCT_BY_BUCKET method with allowance-heavy adjustment:
- E: 10% base + 10% allowance adjustment = 20%
- MAT: 15% base + 10% allowance adjustment = 25%
- CD: 20% base + 10% allowance adjustment = 30%
- CI: 20% base + 10% allowance adjustment = 30%
- PM: 10% base + 5% (factor-derived adjustment) = 15%
- P: 10% base + 5% (factor-derived adjustment) = 15%
- COM: 25% base + 5% (factor-derived adjustment) = 30%

**Trigger:** contingency_method = PCT_BY_BUCKET (default); all base estimate lines are allowance/parametric (100% allowance share for E, MAT, CD).

**Evidence:**
- AGENT_ESTIMATING.md, STRUCTURE: Fallback Typical Model (contingency defaults and allowance-heavy adjustment formula)
- Source_Index.md: 100% allowance-based estimate

**Impacted WBS/CBS:** All CBS buckets

**Estimate Impact:** Contingency percentages elevated due to low estimate maturity and absence of vendor pricing.

**Override Path:** Provide vendor quotes or detailed design to reduce allowance share and lower contingency %.

---

## D-011: Escalation Mode

**Decision:** escalation_mode = NONE (no escalation applied).

**Trigger:** Default config; pricing date is current (2026-01).

**Evidence:** AGENT_ESTIMATING.md, Function 1.3 (default escalation_mode).

**Impacted WBS/CBS:** All

**Estimate Impact:** Estimate totals are in January 2026 dollars; no adjustment for future expenditure timing.

**Override Path:** Set `escalation_mode: EXPLICIT` in config and provide cashflow curve or escalation factors if escalation is required.

---

## D-012: Structural Steel Tonnage Allowance (Placeholder)

**Decision:** Estimate structural steel fabricated tonnage as 150 tonnes (allowance).

**Trigger:** No design drawings or calculations with explicit tonnage available.

**Evidence:**
- Package scope: platforms, stairs, gangways, pipe racks, handrails, pipe supports (decomposition line 242)
- Assumption: medium-scale industrial facility structural steel package
- Comparable EPC projects: 100-200 tonnes typical for railcar unloading facility access structures

**Impacted WBS/CBS:** MAT (structural steel material), CD (fabrication/erection labor)

**Estimate Impact:** Allowance sizing for MAT and CD line items; actual tonnage may vary significantly when design is complete.

**Override Path:** Provide structural steel design drawings with member sizes/lengths or explicit tonnage estimate from DEL-06.03 calculations.

---

## D-013: Handrail and Grating Allowances

**Decision:** Estimate handrail as 400 linear meters and grating as 800 m² (allowances).

**Trigger:** No design drawings or data sheets with explicit quantities available.

**Evidence:**
- DEL-06.04 scope: gangway data sheets, grating data sheets (decomposition line 251)
- Package scope: access platforms, stairs, gangways (decomposition line 242)
- Assumption: industrial railcar unloading facility with 32 unloading stations requires extensive walkways and grating

**Impacted WBS/CBS:** MAT (handrail/grating supply), CD (installation labor)

**Estimate Impact:** Allowance sizing; actual quantities TBD when design drawings (DEL-06.01) are issued.

**Override Path:** Provide platform/gangway layout drawings showing linear footage of handrails and grating areas.

---

**Decision Log compiled:** 2026-01-28 23:33
**Total Decisions:** 13 (D-001 through D-013)


---

## PKG-07

# Decision Log

## PKG-07 Rail Works Estimate

| ID | Decision Statement | Trigger | Evidence | Impacted WBS/CBS | Estimate Impact | Override Method |
|----|-------------------|---------|----------|------------------|-----------------|-----------------|
| D-001 | Currency set to CAD | Config default validation | Project location: Surrey, BC, Canada per decomposition Section 1 | All | Currency basis | Update _CONFIG.md currency |
| D-002 | Track length estimated at 500m per new track (Tracks 6, 7) | No design drawings available | 32 railcar unloading stations at ~15m/car spacing per project parameters | PKG-07 / CD, MAT | Track cost basis (~1,000m total) | Provide track layout drawings |
| D-003 | Track 5 restoration length estimated at 300m | No design drawings available | Assumed 60% of new track length for partial restoration scope | PKG-07 / CD, MAT | Track 5 cost basis | Provide Track 5 condition assessment |
| D-004 | Ballast volume estimated at 1.5 m³/linear meter | No ballast design available | Typical rail track ballast section depth/width | PKG-07 / MAT, CD | Ballast cost basis (~1,950 m³ total) | Provide ballast design (DEL-07.03) |
| D-005 | End stops count set to 4 units | Engineering assumption | 2 new tracks × 2 ends each (Tracks 6, 7) | PKG-07 / MAT, CD | End stop cost basis | Confirm end stop requirements in ER |
| D-006 | Productivity factor set to 1.0 | No site-specific data | BC lower mainland baseline; rail work at operating terminal | CD, CI | Base labor rates | Provide site access constraints |
| D-007 | Rail work assumed during normal operations | No schedule constraints | Terminal operations coordination per PKG-34 | CD, CI | Base rates; no shutdown premium | Document operational constraints |
| D-008 | All pricing via allowances | No vendor quotes or rate tables found | Searched _RateTables/ and deliverable references | All | LOW confidence on all lines | Provide rail vendor quotes and rate tables |
| D-009 | Indirects factors applied from fallback model | No project-specific factors | CI=18%, P=2%, PM=6%, COM=3% per AGENT_ESTIMATING.md | CI, P, PM, COM | ~$200k indirect costs | Provide project factor schedule |
| D-010 | Contingency elevated for allowance-heavy estimate | 100% allowance-based | +10% above baseline per fallback model rules | CONT | ~30% average contingency | Improve pricing basis |
| D-011 | No escalation applied | Config setting | escalation_mode = NONE | All | $0 escalation | Update config if needed |
| D-012 | Rail type assumed as 115 RE or equivalent | No rail specification available | Typical heavy rail for industrial trackage | PKG-07 / MAT | Rail material cost basis | Provide rail specification (DEL-07.02) |
| D-013 | Track subgrade preparation included in PKG-02 | Scope split assumption | Earthworks package handles subgrade; rail works package handles ballast/track | PKG-07 / Scope | No subgrade cost in PKG-07 | Confirm scope split in ER |
| D-014 | Track drainage assumed in PKG-03 | Scope split assumption | Utilities package handles track drainage; rail works handles ballast only | PKG-07 / Scope | No drainage cost in PKG-07 | Confirm scope split in ER |


---

## PKG-08

# Decision Log — PKG-08 Marine Structures Estimate

**Snapshot ID:** EST_PKG08_DRAFT_2026-01-28_2400
**Date:** 2026-01-28

---

## Purpose

This log records all decisions, defaults, and ambiguous interpretations made during the estimating process for PKG-08 Marine Structures. Each decision is assigned a unique ID (D-###) and is referenced from the Basis of Estimate (BOE) and/or line items in `Detail.csv`.

---

## D-801: Currency Selection

**Decision:** Use CAD (Canadian Dollars) as the currency for this estimate.

**Trigger:** Config parameter `currency` not overridden for PKG-08 specifically; default from `_CONFIG.md` applies.

**Evidence:** Project location is Fraser Surrey Terminal, Surrey, BC, Canada. Config file specifies CAD for prior packages (PKG-00 through PKG-04).

**Impacted WBS/CBS:** All line items (PKG-08)

**Estimate Impact:** Currency basis for all pricing; no currency conversion required.

**How to Override:** Edit `_CONFIG.md` or provide PKG-08-specific config override if different currency is required.

---

## D-802: Pricing Date and Escalation

**Decision:** Use January 2026 as pricing date; escalation_mode = NONE.

**Trigger:** No historical pricing sources found; config specifies escalation_mode = NONE.

**Evidence:** Config file `_CONFIG.md` line 10 specifies `pricing_date = 2026-01` and line 36 specifies `escalation_mode = NONE`.

**Impacted WBS/CBS:** All line items (PKG-08)

**Estimate Impact:** Pricing represents "January 2026 dollars"; no escalation applied to future expenditure.

**How to Override:** Update `_CONFIG.md` with `escalation_mode = EXPLICIT` and provide cashflow curve or escalation factors.

---

## D-803: Pricing Sources — No Quotes or Rate Tables

**Decision:** Proceed with 100% Allowance/Parametric pricing using Fallback Typical Model.

**Trigger:** Source discovery (Protocol Phase 2.2) found no vendor quotes, no rate tables in `_RateTables/`, and no historical project data.

**Evidence:**
- `_RateTables/` directory is empty
- No quotes found in deliverable `_REFERENCES.md` files or workspace
- Deliverables at INITIALIZED state with TBD content

**Impacted WBS/CBS:** All line items (PKG-08)

**Estimate Impact:** All pricing is allowance-based or parametric (factor-based). Confidence = LOW for all line items.

**How to Override:**
1. Obtain vendor budgetary quotes for marine piling, structural steel, and marine contractor services
2. Populate `_RateTables/` with unit rates for marine construction
3. Re-run estimating pipeline

---

## D-804: WBS → CBS Mapping

**Decision:** Map PKG-08 deliverables and physical scope to CBS buckets as follows:

| WBS Element | CBS Bucket | Rationale |
|-------------|------------|-----------|
| DEL-08.01 through DEL-08.11 | E (Engineering) | All deliverables are design/engineering outputs (drawings, calcs, specs, reports) |
| Marine piling supply | MAT (Materials) | Equipment/materials supply |
| Structural steel supply | MAT (Materials) | Equipment/materials supply |
| Abutment materials | MAT (Materials) | Concrete, rebar, formwork |
| Marine hardware | MAT (Materials) | Ladders, platforms, anodes |
| Marine logistics | FRT (Freight) | Barge mobilization, marine transport |
| Pile installation | CD (Construction Directs) | Field labor and equipment |
| Steel erection | CD (Construction Directs) | Field labor and equipment |
| Coatings, NDT | CD (Construction Directs) | Field labor and services |
| Supervision, safety, QA/QC | CI (Construction Indirects) | Field overhead and management |
| EPCM allocation | PM (Project Management) | Project-level management and coordination |
| Vendor coordination | P (Procurement) | Procurement services |
| Load testing, proving | COM (Commissioning) | Testing and acceptance |

**Trigger:** No explicit CBS mapping provided in decomposition or ER; agent must infer mapping based on deliverable types and marine scope.

**Evidence:** Standard EPC CBS structure; marine work typically split into MAT (supply), FRT (marine logistics), CD (installation), CI (supervision).

**Impacted WBS/CBS:** All PKG-08 line items

**Estimate Impact:** Determines which CBS bucket each line item rolls up to; affects contingency application and summary reporting.

**How to Override:** Provide explicit WBS-CBS mapping table in `_CONFIG.md` or decomposition.

---

## D-805: Quantity Takeoff Approach — No Explicit Quantities

**Decision:** Proceed with allowance line items (Qty=1, Unit=LS) sized using fallback model and industry-typical assumptions.

**Trigger:** All deliverables at INITIALIZED state; no explicit quantities in Datasheet.md or Specification.md files (all marked TBD).

**Evidence:**
- Reviewed all 11 deliverable folders under `PKG-08_Marine_Structures/1_Working/`
- All `Datasheet.md` files show TBD for quantities, dimensions, materials
- No design drawings or geotechnical reports available to support QTO

**Impacted WBS/CBS:** MAT, CD line items (piling, steel, installation)

**Estimate Impact:** All quantities are placeholders; actual quantities may vary significantly when design matures.

**How to Override:**
1. Complete marine geotechnical investigation (DEL-08.04) to confirm pile type, size, quantity
2. Develop preliminary design drawings (DEL-08.01) with trestle/platform geometry and steel tonnages
3. Re-run estimating pipeline with updated QTO

**Assumptions Created:** A-812 through A-825

---

## D-806: Allowance Sizing Method

**Decision:** Size allowances using:
1. Comparable engineering line items from PKG-01/PKG-02 estimates, scaled for marine complexity
2. Industry-typical unit rates for marine materials (piling, structural steel with marine-grade corrosion protection)
3. Marine construction rates reflecting specialized marine contractor requirements

**Trigger:** No project-specific pricing sources available; must size allowances to produce runnable estimate.

**Evidence:**
- Prior estimates (PKG-00, PKG-01, PKG-02) used allowance-based pricing successfully
- Marine piling: typical CAD $750-$1,100/tonne installed (including supply, delivery, driving)
- Marine structural steel: typical CAD $4,500-$5,500/tonne installed (including supply, delivery, erection, marine-grade coating)
- Engineering deliverables: scaled from prior packages based on complexity and number of deliverables

**Impacted WBS/CBS:** All ALLOWANCE line items (E, MAT, CD)

**Estimate Impact:** Allowance amounts are industry-typical placeholders; may vary ±50% based on actual project-specific conditions.

**How to Override:** Obtain project-specific vendor quotes or populate `_RateTables/` with verified unit rates.

---

## D-807: Indirects, Management, and Commissioning Factors

**Decision:** Apply Fallback Typical Model factors as follows:

| CBS Bucket | Factor | Base | Calculation |
|------------|--------|------|-------------|
| CI (Construction Indirects) | 18% | CD | $1,830k × 0.18 = $329.4k |
| PM (EPCM/Project Mgmt) | 6% | CD + CI + MAT + FRT | ($1,830k + $329.4k + $2,280k + $175k) × 0.06 = $276.9k |
| P (Procurement Services) | 2% | MAT + FRT | ($2,280k + $175k) × 0.02 = $49.1k |
| COM (Commissioning) | 3% | CD + CI + MAT | ($1,830k + $329.4k + $2,280k) × 0.03 = $133.2k |

**Trigger:** No project-specific indirects data or schedule-based models available.

**Evidence:** Fallback Typical Model (AGENT_ESTIMATING.md lines 666-673) provides default factors for marine/EPC work.

**Impacted WBS/CBS:** CI, PM, P, COM line items

**Estimate Impact:** Indirects and management represent 14.3% of base estimate; commissioning represents 2.4%.

**How to Override:**
1. Provide project-specific indirects model (time-based supervision, temporary facilities, HSE costs)
2. Provide schedule/duration data to support time-based indirects calculation
3. Update `_CONFIG.md` with custom factor overrides

**Justification for Marine Work:**
- 18% CI is appropriate for marine construction (enhanced supervision, marine safety, specialized QA/QC for welding/NDT, tide/weather coordination)
- 6% PM reflects marine engineering coordination across disciplines and interfaces
- 3% COM reflects structural load testing, proof testing, as-built survey requirements

---

## D-808: Contingency Method and Percentage

**Decision:** Apply 25% contingency to base estimate using `PCT_BY_BUCKET` method with allowance-heavy adjustment.

**Trigger:** Config specifies `contingency_method = PCT_BY_BUCKET`; estimate is 92.2% ALLOWANCE/PARAMETRIC.

**Evidence:**
- Fallback model (AGENT_ESTIMATING.md lines 677-690) specifies baseline contingency by CBS plus allowance-heavy adjustment
- Pre-conceptual design maturity (< 5%)
- 100% allowance/parametric pricing (no quotes or rate tables)
- Marine construction complexity and uncertainty

**Impacted WBS/CBS:** All CBS buckets

**Estimate Impact:** Contingency = $1,365,750 (25% of rounded base estimate $5,463,000)

**Contingency Breakdown by CBS:**
- E: 20% (baseline 10% + 10% allowance adjustment)
- MAT: 25% (baseline 15% + 10% allowance adjustment)
- FRT: 25% (baseline 15% + 10% allowance adjustment)
- CD: 30% (baseline 20% + 10% allowance adjustment)
- CI: 20% (baseline 20%; no adjustment for parametric)
- PM: 10% (baseline 10%; no adjustment for parametric)
- P: 10% (baseline 10%; no adjustment for parametric)
- COM: 25% (baseline 25%; no adjustment for parametric)

**How to Override:**
1. Switch to `contingency_method = RISK_BASED` in `_CONFIG.md` and provide risk register with quantified impacts
2. Provide explicit contingency % override in `_CONFIG.md`
3. Reduce allowance share by obtaining quotes/rate tables → lower contingency justified

**Rationale:**
- High contingency reflects pre-conceptual maturity and marine construction uncertainty
- Contingency will reduce as design matures and pricing sources improve

---

## Summary

| Decision ID | Topic | Impact |
|-------------|-------|--------|
| D-801 | Currency = CAD | All line items priced in CAD |
| D-802 | Pricing date = 2026-01, no escalation | January 2026 dollars basis |
| D-803 | No quotes/rate tables → 100% allowance/parametric | Low confidence, all pricing |
| D-804 | WBS → CBS mapping | Line item CBS assignment |
| D-805 | No explicit quantities → allowance line items | All quantities are placeholders |
| D-806 | Allowance sizing using industry-typical rates | All allowance amounts |
| D-807 | Indirects/PM/P/COM factors from fallback model | Parametric line items |
| D-808 | 25% contingency (PCT_BY_BUCKET, allowance-heavy) | Contingency amount |

---

**END OF DECISION LOG**


---

## PKG-09

# Decision Log

## EST_PKG09_DRAFT_2026-01-28_2332

All decisions made during the estimating process for PKG-09 Marine Outfitting.

---

### D-001: Currency Selection

**Decision:** Use CAD (Canadian dollars) as the single currency for this estimate.

**Trigger:** Config did not specify currency; auto-discovery required.

**Evidence:** Project location is Fraser Surrey Terminal, 11060 Elevator Road, Surrey, BC, Canada (decomposition Section 1). All work is performed in Canada.

**Impacted WBS/CBS:** All packages and CBS buckets.

**Estimate Impact:** No conversion required; single-currency estimate reduces complexity and eliminates FX risk.

**How to Override:** Set `currency: USD` (or other) in `_CONFIG.md` if required by contract.

---

### D-002: Marine Structure Interface Assumption

**Decision:** Assume PKG-08 Marine Structures provides structural capacity for fender/bollard mounting.

**Trigger:** PKG-08 deliverables (DEL-08.01, DEL-08.03) are not yet available; interface assumptions required.

**Evidence:** Decomposition Section PKG-09 scope states "Fenders, bollards, ladders, life-saving equipment, existing Berth 10 upgrades and repairs." PKG-08 is responsible for "Marine Structures."

**Impacted WBS/CBS:** PKG-09 installation scope (CD lines L-011 through L-015).

**Estimate Impact:** Scope boundary assumed; no structural capacity upgrades included in PKG-09 estimate.

**How to Override:** Coordinate with PKG-08 outputs (DEL-08.01, DEL-08.03) when available to confirm interface scope.

---

### D-003: Berthing Design Basis

**Decision:** Assume berthing energy and mooring loads will be provided by PKG-08 analyses (DEL-08.06, DEL-08.09).

**Trigger:** No berthing energy calculations or mooring analysis results available.

**Evidence:** Decomposition PKG-08 includes DEL-08.06 (Berthing Energy Calculation), DEL-08.07 (Fender System Deflection Characteristics), DEL-08.08 (Fender Supplier Design Verification), and DEL-08.09 (Mooring Analysis).

**Impacted WBS/CBS:** MAT lines L-006 (fenders) and L-007 (bollards); fender/bollard sizing assumptions.

**Estimate Impact:** Fender and bollard sizing/capacity based on parametric assumptions (Panamax vessel class).

**How to Override:** Update fender/bollard specifications when PKG-08 analyses are complete.

---

### D-004: Productivity Factor

**Decision:** Use productivity factor of 1.0 (BC lower mainland baseline).

**Trigger:** No project-specific productivity data available.

**Evidence:** Location is Surrey, BC, Canada (decomposition Section 1). BC lower mainland is a mature construction market with standard labor availability.

**Impacted WBS/CBS:** CD (Construction Directs) labor rates.

**Estimate Impact:** No productivity adjustment applied; labor rates use baseline values.

**How to Override:** Adjust productivity factor in rate tables if site-specific constraints are identified (e.g., access limitations, concurrent operations).

---

### D-005: Marine Access Method

**Decision:** Assume marine installation via crane barge with water-based access for fenders/bollards.

**Trigger:** No installation method specified; marine work requires access assumptions.

**Evidence:** Marine outfitting typically requires crane barge for positioning/installation of heavy fenders and bollards at waterside locations.

**Impacted WBS/CBS:** CD line L-016 (Marine Crane/Barge Mobilization); installation labor lines L-011, L-012.

**Estimate Impact:** Crane barge mobilization cost of $65,000 included; marine labor rates assume barge-based work.

**How to Override:** Confirm installation method with site logistics plan and PKG-08 marine structure access provisions.

---

### D-006: Working Hours and Constraints

**Decision:** Standard 8-10 hour shifts assumed; marine work subject to tide and weather constraints.

**Trigger:** No project schedule or work hour constraints specified.

**Evidence:** Marine construction typically limited by tides, weather, and vessel traffic. Standard shifts assumed for cost estimating.

**Impacted WBS/CBS:** CD (Construction Directs) labor productivity and CI (Construction Indirects) supervision.

**Estimate Impact:** Labor rates assume standard productivity; no shift premiums or overtime included.

**How to Override:** Adjust rates if compressed schedule or shift work is required (update _CONFIG.md or provide project schedule).

---

### D-007: Pricing Sources Hierarchy

**Decision:** All line items priced via allowances (fallback typical model) due to absence of vendor quotes or project rate tables.

**Trigger:** No vendor quotes or rate tables provided; straight-through estimating requires pricing basis.

**Evidence:** No vendor quotes found; no rate tables in `_RateTables/` directory.

**Impacted WBS/CBS:** All CBS buckets; all MAT and CD line items.

**Estimate Impact:** 100% allowance-based estimate; confidence = LOW; contingency elevated per PCT_BY_BUCKET method.

**How to Override:** Provide vendor budgetary quotes for fenders, bollards, ladders, life-saving equipment. Provide project labor/equipment rate tables in `_RateTables/`.

---

### D-008: Indirects and Services Factors

**Decision:** Apply factor-based indirects model using fallback typical model rates.

**Trigger:** No project-specific indirects model or schedule-based data available.

**Evidence:** Fallback typical model (STRUCTURE section of AGENT_ESTIMATING.md).

**Impacted WBS/CBS:**
- CI (Construction Indirects): 18% of CD
- P (Procurement Services): 2% of MAT
- PM (Project Management / EPCM): 6% of (CD + CI + MAT)
- COM (Commissioning): 3% of (CD + CI + MAT)

**Estimate Impact:**
- CI = $64,000 (18% × $355,000)
- P = $31,000 (2% × $1,534,000)
- PM = $114,000 (6% × $1,953,000)
- COM adjusted to reflect proof load testing scope (see lines L-023 through L-025)

**How to Override:** Provide project-specific indirects rates, schedule-based resource loading, or overhead allocation model in _CONFIG.md or rate tables.

---

### D-009: Contingency Method and Rates

**Decision:** Apply PCT_BY_BUCKET contingency with allowance-heavy adjustment (100% allowance estimate).

**Trigger:** Config specified `contingency_method: PCT_BY_BUCKET`; all line items are allowances.

**Evidence:** Fallback typical model contingency rates (STRUCTURE section) plus allowance adjustment (+10% for buckets with 100% allowance share).

**Impacted WBS/CBS:** All CBS buckets.

**Estimate Impact:**
- E: 20% (10% base + 10% allowance adjustment)
- MAT: 25% (15% base + 10% allowance adjustment)
- CD: 30% (20% base + 10% allowance adjustment)
- CI: 30% (20% base + 10% factor-derived adjustment)
- PM: 15% (10% base + 5% factor-derived adjustment)
- P: 15% (10% base + 5% factor-derived adjustment)
- COM: 30% (25% base + 5% factor-derived adjustment)

**Total Contingency:** $568,000 (25.3% of base)

**How to Override:** Provide vendor quotes to reduce allowance share and lower contingency rates. Alternatively, switch to `contingency_method: RISK_BASED` in _CONFIG.md for three-point estimating.

---

### D-010: Escalation Mode

**Decision:** No escalation applied (escalation_mode = NONE).

**Trigger:** Config default; no schedule or cashflow data available.

**Evidence:** Pricing date is January 2026 (current); no future escalation factors defined.

**Impacted WBS/CBS:** All CBS buckets.

**Estimate Impact:** Estimate is in "January 2026 dollars"; no escalation to future expenditure dates.

**How to Override:** Set `escalation_mode: EXPLICIT` in _CONFIG.md and provide schedule/cashflow curve and escalation factors.

---

## Summary

| Decision ID | Topic | Impact |
|-------------|-------|--------|
| D-001 | Currency = CAD | Single-currency estimate |
| D-002 | PKG-08 interface | Scope boundary assumption |
| D-003 | Berthing design basis | Fender/bollard sizing assumptions |
| D-004 | Productivity factor = 1.0 | No productivity adjustment |
| D-005 | Marine access via crane barge | Installation method assumption |
| D-006 | Standard working hours | No shift premiums |
| D-007 | 100% allowance pricing | Low confidence; high contingency |
| D-008 | Factor-based indirects | Default fallback model |
| D-009 | Contingency = 25.3% of base | Elevated for allowance-heavy estimate |
| D-010 | No escalation | January 2026 dollars |

---

*All decisions are traceable to source documents, config defaults, or fallback typical model per AGENT_ESTIMATING.md PROTOCOL.*

