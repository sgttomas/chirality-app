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


---

## PKG-10

# Decision Log

## Overview

This log captures all decisions made during the estimating process where the agent selected defaults, resolved ambiguities, or made choices affecting the estimate.

---

## D-001: Currency Selection

**Decision:** Use CAD (Canadian dollars) for all estimate values.

**Trigger:** No explicit currency specified in deliverable documents.

**Evidence:**
- Project location: Fraser Surrey Terminal, Surrey, BC, Canada (decomposition Section 1)
- Canadian project location implies CAD currency

**Impacted WBS/CBS:** All packages and CBS buckets

**Estimate Impact:** None (currency selection; does not change values)

**Override Path:** Set `currency: USD` (or other) in `_CONFIG.md` if different currency required.

---

## D-002: Rail Track Interface Assumption

**Decision:** Assume PKG-07 Rail Works provides track alignment, railcar positioning, and station spacing.

**Trigger:** PKG-07 deliverable details not yet available; station positioning required for unloading arm placement.

**Evidence:**
- Decomposition Section 5: PKG-07 Rail Works scope includes rail infrastructure
- DEL-10.01 Datasheet Section "Construction" references PKG-07 interface for track alignment

**Impacted WBS/CBS:** PKG-10 (all deliverables); affects unloading arm spacing and header routing

**Estimate Impact:** Qualitative — affects design coordination effort; no direct cost impact on this estimate

**Override Path:** Provide PKG-07 track layout drawings (DEL-07.01) for coordination verification.

---

## D-003: Header Discharge Interface Assumption

**Decision:** Assume PKG-14 Process Piping provides downstream piping connection from header discharge point.

**Trigger:** PKG-14 deliverable details not yet available; header discharge connection required for interface definition.

**Evidence:**
- Decomposition Section 5: PKG-14 Process Piping scope includes product transfer piping
- DEL-10.01 Datasheet Section "Construction" references PKG-14 interface for header discharge connection

**Impacted WBS/CBS:** PKG-10 (DEL-10.01, DEL-10.03); affects header terminus design

**Estimate Impact:** Qualitative — affects interface coordination; header piping estimate assumes connection at header terminus only

**Override Path:** Provide PKG-14 process piping layout for interface coordination.

---

## D-004: Productivity Factor Selection

**Decision:** Use productivity factor of 1.0 (baseline) for BC lower mainland.

**Trigger:** No project-specific productivity data available.

**Evidence:**
- Location: Fraser Surrey Terminal, Surrey, BC (major urban area with skilled labor availability)
- BC lower mainland is a major construction market with typical productivity

**Impacted WBS/CBS:** All construction labor (CBS = CD, CI)

**Estimate Impact:** None (baseline productivity factor); changing factor would scale labor costs proportionally

**Override Path:** Provide project productivity assessment or adjust labor rates in rate tables to account for site-specific factors.

---

## D-005: Site Access Assumption

**Decision:** Assume standard construction site access adjacent to rail tracks with no extraordinary access constraints.

**Trigger:** No site access restrictions documented in deliverable documents.

**Evidence:**
- PKG-10 scope is railcar unloading system located at rail track alignment
- DEL-10.01 Datasheet does not mention access restrictions

**Impacted WBS/CBS:** CD (construction labor productivity and mobilization)

**Estimate Impact:** Minimal — standard access assumed; extraordinary access (e.g., work within active rail corridor with frequent train traffic) would increase labor costs

**Override Path:** Provide site access constraints or rail operations coordination requirements if applicable.

---

## D-006: Working Hours Assumption

**Decision:** Assume standard 8-10 hour shifts with minimal constraints.

**Trigger:** No shift restrictions or working hour limitations documented.

**Evidence:**
- Industrial site location with no apparent shift restrictions in deliverable documents
- PKG-10 scope does not reference special working hour requirements

**Impacted WBS/CBS:** CD, CI (labor costs and schedule)

**Estimate Impact:** Minimal — standard shift assumptions; shift work premiums or restricted hours would increase labor costs

**Override Path:** Provide working hour restrictions or shift requirements if applicable (e.g., night work only, rail traffic windows).

---

## D-007: Pricing Basis Selection

**Decision:** Price all line items using allowances (fallback typical model) due to absence of vendor quotes or rate tables.

**Trigger:** No vendor quotes or project rate tables available for PKG-10 scope.

**Evidence:**
- Source search found no quotes, budgetary proposals, or rate tables for unloading arms or related equipment
- `_RateTables/` directory empty (no project rate library)

**Impacted WBS/CBS:** All packages and CBS buckets

**Estimate Impact:** HIGH — all pricing is parametric/allowance-based with LOW confidence; variance likely when actual quotes obtained

**Override Path:**
1. Obtain budgetary quotes from unloading arm suppliers (TechnipFMC, OPW, Emco Wheaton, etc.)
2. Populate `_RateTables/` with project labor rates, equipment rates, material unit costs
3. Re-run estimating pipeline to replace allowances with quote/rate pricing

---

## D-008: Indirects and Services Factors

**Decision:** Apply factor-based indirects and services per fallback typical model.

**Trigger:** No project-specific indirects pricing or time-based model available.

**Evidence:**
- No schedule/duration data available for time-based indirects calculation
- Fallback typical model (AGENT_ESTIMATING Section "Fallback Typical Model") provides default factors

**Factors Applied:**
- CI (Construction Indirects) = 18% × CD
- P (Procurement Services) = 2% × MAT
- PM (EPCM/PM) = 6% × (CD + CI + MAT)

**Impacted WBS/CBS:** CI, P, PM

**Estimate Impact:** MEDIUM — factors are typical industry averages; actual project indirects may vary ±25% depending on schedule, site conditions, project complexity

**Override Path:** Provide project schedule and indirects staffing plan for time-based indirects calculation, or provide indirect cost rates in `_CONFIG.md` to override factors.

---

## D-009: Contingency Rates

**Decision:** Apply elevated contingency rates per PCT_BY_BUCKET method with allowance-heavy adjustments.

**Trigger:** 100% allowance-based estimate with no vendor quotes; specialized equipment with limited pricing data.

**Evidence:**
- All line items priced via allowances (Method = ALLOWANCE or PARAMETRIC)
- Specialized railcar unloading equipment (32 articulating arms) with vendor-specific pricing variation

**Contingency Rates Applied:**
- E: 20% (10% base + 10% allowance adjustment)
- MAT: 25% (15% base + 10% allowance adjustment)
- CD: 30% (20% base + 10% allowance adjustment)
- CI: 30% (20% base + 10% factor-derived adjustment)
- PM: 15% (10% base + 5% factor-derived adjustment)
- P: 15% (10% base + 5% factor-derived adjustment)
- COM: 30% (25% base + 5% allowance adjustment)

**Impacted WBS/CBS:** All CBS buckets (CONT)

**Estimate Impact:** HIGH — contingency totals $996,000 (25.4% of base); reflects estimate uncertainty

**Override Path:** Obtain vendor quotes and rate tables to reduce allowance share and lower contingency rates in next run.

---

## D-010: Escalation Mode

**Decision:** Do not apply escalation (escalation_mode = NONE).

**Trigger:** Config specifies NONE; pricing date is current (January 2026).

**Evidence:**
- `_CONFIG.md` specifies `escalation_mode: NONE`
- Pricing date = 2026-01 (current month)

**Impacted WBS/CBS:** All CBS buckets (no ESC bucket)

**Estimate Impact:** None for current estimate; future project execution may require escalation depending on schedule

**Override Path:** Set `escalation_mode: EXPLICIT` in `_CONFIG.md` and provide schedule/cashflow data for escalation calculation.

---

## D-011: Unloading Arm Type Selection

**Decision:** Assume articulating bottom-loading arms as the unloading arm type.

**Trigger:** Deliverable documents reference "bottom-loading" but specific arm configuration (articulating vs. fixed) not specified.

**Evidence:**
- DEL-10.01 Datasheet Section "Conditions" notes "bottom-loading type **ASSUMPTION**"
- Industry practice: articulating arms are standard for railcar bottom unloading (provides reach flexibility and operator safety)
- Gravity flow requirement (decomposition PKG-10 scope) implies bottom outlet connection

**Impacted WBS/CBS:** MAT (unloading arms), CD (installation labor)

**Estimate Impact:** MEDIUM — articulating arms are higher cost ($45k-60k/unit) than fixed arms; installation labor also higher

**Override Path:** Verify arm type requirements in Employer's Requirements or specify arm configuration in DEL-10.02 specification.

---

## D-012: Header Piping Length Estimate

**Decision:** Estimate 400 lm of header piping for 32-station layout.

**Trigger:** DEL-10.01 header layout drawings not yet available; piping length required for material and labor estimates.

**Evidence:**
- 32 stations with typical spacing of 12-14m on-center (industry standard for railcar unloading facilities)
- Header routing: main header run (~380m for 32 stations) + branch connections (~20m allowance) = ~400 lm total
- Assumption logged as A-003

**Impacted WBS/CBS:** MAT (header piping supply), CD (piping installation labor)

**Estimate Impact:** MEDIUM — header piping is ~$280k material + $180k labor; ±20% variance if actual layout differs

**Override Path:** Provide DEL-10.01 header layout drawings to verify piping length from actual routing.

---

## D-013: Sump Pump Quantity

**Decision:** Estimate 8 sump pumps for grouped containment drainage.

**Trigger:** Containment drainage configuration not yet defined in DEL-10.01; pump quantity required for estimate.

**Evidence:**
- DEL-10.04 Datasheet notes sump pump quantity as "**TBD** per containment design from DEL-10.01"
- Grouped containment zones reduce pump count vs. 32 individual pumps (1 per pan)
- Typical configuration: 4 pumps per zone with 2 zones for 32 stations (4 pumps × 2 zones = 8 total)
- Assumption logged as A-005

**Impacted WBS/CBS:** MAT (sump pumps), CD (pump installation)

**Estimate Impact:** LOW-MEDIUM — sump pumps total ~$48k material + $24k labor; quantity variance from 4 to 16 pumps would affect costs by ±50%

**Override Path:** Provide DEL-10.01 containment details drawings showing drainage configuration and pump locations.

---

## Summary

Total decisions logged: 13 (D-001 through D-013)

**Critical decisions affecting estimate significantly:**
- D-007: All allowance-based pricing (HIGH impact — entire estimate variance)
- D-009: Elevated contingency rates (HIGH impact — $996k contingency)
- D-011: Unloading arm type (MEDIUM impact — ~$1.6M equipment cost)
- D-012: Header piping length (MEDIUM impact — ~$460k header piping total)

**Decision categories:**
- Currency and config: 3 decisions (D-001, D-010, rounding per config)
- Interface assumptions: 2 decisions (D-002, D-003)
- Productivity and site: 3 decisions (D-004, D-005, D-006)
- Pricing methodology: 3 decisions (D-007, D-008, D-009)
- Technical assumptions: 2 decisions (D-011, D-013)

All decisions are recorded for audit trail and can be overridden in subsequent estimate runs by providing better inputs (quotes, rate tables, interface documents, design details).

---

## PKG-11

# Decision Log

## PKG-11 Marine Loading System Estimate

| ID | Decision Statement | Trigger | Evidence | Impacted WBS/CBS | Estimate Impact | How to Override |
|----|-------------------|---------|----------|------------------|-----------------|-----------------|
| D-001 | Currency set to CAD (Canadian dollars) | Default selection required | Project location: Fraser Surrey Terminal, Surrey, BC, Canada per decomposition Section 1 | All | All amounts | Set `currency` in _CONFIG.md |
| D-002 | Marine loading arm assumed as OEM-supplied package with Contractor installation | Procurement approach clarification | Industry standard for specialized marine loading equipment | MAT, CD | Equipment as single procurement; install separate | Confirm procurement strategy |
| D-003 | Loading arm foundation assumed in PKG-08 Marine Structures scope | Scope boundary clarification | Decomposition shows PKG-08 Marine Structures separate from PKG-11 | PKG-11 interface | Foundation excluded from PKG-11 | Include foundation if scope changes |
| D-004 | Productivity factor set to 1.0 (BC lower mainland baseline) | No site-specific productivity data | Project location in established industrial port area | PKG-11 / CD | Labor rates | Provide site-specific productivity factors |
| D-005 | Marine/jetty access assumed with coordination for terminal operations | Working conditions clarification | Active terminal with vessel operations | PKG-11 / CD, CI | Marine access logistics | Provide terminal coordination plan |
| D-006 | Working hours assumed standard 8-10 hour shifts; marine work may require tide windows | No shift schedule provided | Typical marine terminal construction | PKG-11 / CD, CI | Labor productivity | Provide project schedule/shift requirements |
| D-007 | All pricing via allowances (fallback typical model) | No vendor quotes or rate tables available | Source index search returned no pricing sources | All | 100% allowance basis | Provide vendor quotes or rate tables |
| D-008 | Indirects factors applied per fallback typical model (CI 18%, PM 6%, P 2%, COM 4%) | No project-specific indirects data | Fallback typical model per AGENT_ESTIMATING STRUCTURE; COM elevated to 4% for marine loading commissioning complexity | CI, PM, P, COM | $335,000 indirects | Provide project-specific indirects |
| D-009 | Contingency rates elevated due to 100% allowance-based estimate (+10% on direct CBS, +5% on factors) | High uncertainty in allowance-based estimate | Per AGENT_ESTIMATING fallback contingency method | CONT | 25.7% weighted contingency | Reduce allowance share with quotes |
| D-010 | Escalation mode set to NONE | Default selection | Pricing date is current (January 2026) | All | No escalation | Set `escalation_mode` in _CONFIG.md |
| D-011 | Double-walled pipe routing assumed at 150 lm from tank farm to berth | No layout drawings available | Typical routing for marine terminal with tank farm setback | MAT, CD | Pipe quantity basis | Provide DEL-11.01 with actual routing |
| D-012 | Loading arm size assumed 12-16 inch nominal for canola oil throughput | No loading rate specified | 1,000,000 MT/annum OBJ-2 implies ~2,000-4,000 m³/hr loading rate | MAT | Loading arm size/cost | Confirm loading rate from ER |

---

## PKG-12

# Decision Log

## Snapshot Identification

| Field | Value |
|-------|-------|
| Snapshot ID | EST_PKG12_DRAFT_2026-01-28_2341 |
| Estimate Label | PKG12_DRAFT |
| Package | PKG-12 Product Transfer & Metering |
| Date | 2026-01-28 |

---

## D-001: Currency Selection

**Decision:** Use CAD (Canadian dollars) for all estimate values

**Trigger:** Config file specifies CAD; project location is Surrey, BC, Canada

**Evidence:**
- `_CONFIG.md` line 9: `currency | CAD`
- Decomposition line 10: "Location: Fraser Surrey Terminal, 11060 Elevator Road, Surrey, BC"

**Impacted WBS/CBS:** All packages, all CBS buckets

**Estimate Impact:** All costs denominated in CAD; no currency conversion required

**Override Path:** Edit `_CONFIG.md` to change currency parameter

---

## D-002: Pricing Basis Selection (Allowances)

**Decision:** Use allowances for all line items due to absence of vendor quotes and rate tables

**Trigger:** Source discovery found no vendor quotes or project-specific rate tables

**Evidence:**
- Rate table directory search: `test/execution/_Estimates/_RateTables/` — not found
- Deliverable `_REFERENCES.md` files reviewed — no vendor quote references
- Source_Index.md: "Explicit Pricing Sources: None available"

**Impacted WBS/CBS:** All PKG-12 deliverables, all CBS buckets

**Estimate Impact:** All pricing uses fallback typical model; estimate confidence is LOW; cost ranges are wide

**Override Path:** Provide vendor budgetary quotes for custody transfer metering equipment, or populate `_RateTables/` with project-specific labor/equipment/material rates

---

## D-003: Meter Technology Assumption

**Decision:** Assume Coriolis mass flowmeter technology for custody transfer flow meters

**Trigger:** Meter technology not specified in available deliverable documents (deliverables in INITIALIZED state)

**Evidence:**
- DEL-12.02 Datasheet.md line 69: "Technology selection (Coriolis mass flowmeter, ultrasonic flowmeter, turbine flowmeter, positive displacement flowmeter, or other)"
- Typical custody transfer practice: Coriolis offers direct mass measurement, high accuracy (±0.15% typical), integral density measurement, good for viscous products

**Impacted WBS/CBS:** MAT (flow meters), CD (installation)

**Estimate Impact:** Flow meter unit cost ~$150k-250k/unit (Coriolis typical range); higher than turbine (~$30k-80k) or ultrasonic (~$80k-150k), but better accuracy and integrated density

**Override Path:** Confirm meter technology selection in DEL-12.02 specification; adjust flow meter costs if different technology selected

---

## D-004: Proving Method Assumption

**Decision:** Assume portable prover for custody transfer meter proving

**Trigger:** Proving method not specified in available deliverable documents

**Evidence:**
- DEL-12.02 Datasheet.md line 71: "Proving method (in-line prover with sphere or piston, portable prover, master meter, or combination)"
- Typical for dual-service installations (rail + marine): Portable prover provides flexibility to prove both meters without dedicated in-line provers

**Impacted WBS/CBS:** MAT (proving equipment), COM (proving labor)

**Estimate Impact:** Portable prover cost ~$100k-150k; lower than dual in-line provers (~$150k-250k each), higher than master meter approach (~$50k-80k for master meter + periodic external calibration)

**Override Path:** Confirm proving method in DEL-12.02 specification; adjust proving equipment cost if in-line prover or master meter selected

---

## D-005: Labor Rate Assumption

**Decision:** Use $120/hr all-in labor rate for construction direct labor

**Trigger:** No project-specific labor rates available in rate tables

**Evidence:**
- Rate table search: No rate tables found
- Typical BC lower mainland labor rates for industrial/process work: $100-140/hr all-in (direct wage + fringes + burden + contractor markup)

**Impacted WBS/CBS:** CD (construction directs)

**Estimate Impact:** All CD labor priced at $120/hr; actual rates may vary based on trade (pipefitter, instrument tech, electrician, etc.)

**Override Path:** Provide project labor rate table in `_RateTables/` with craft-specific rates

---

## D-006: Metering Point Configuration

**Decision:** Assume separate dedicated meters for rail unloading and marine loading (not shared/manifolded)

**Trigger:** Configuration not explicitly stated; typical custody transfer practice

**Evidence:**
- DEL-12.01 Datasheet.md line 36: "Metering Points: Two primary custody transfer locations: (1) Rail unloading custody transfer; (2) Marine loading custody transfer"
- Typical practice: Separate meters for independent operations and custody transfer integrity

**Impacted WBS/CBS:** MAT (2 flow meters required), E (separate sizing/design for each service)

**Estimate Impact:** Requires 2 flow meters (~$150k-250k each) vs. 1 shared meter; provides operational flexibility and redundancy

**Override Path:** Confirm metering configuration in DEL-12.01 drawings and DEL-12.02 specification

---

## D-007: Indirects and Services Factors

**Decision:** Apply factor-based indirects and services per fallback typical model

**Trigger:** Default estimating method per AGENT_ESTIMATING.md; no project-specific schedule or duration data available

**Evidence:**
- AGENT_ESTIMATING.md lines 665-673: Default factors for CI (18% CD), P (2% MAT), PM (6% CD+CI+MAT), COM (3% CD+CI+MAT)
- No schedule or cashflow data available for time-based indirects model

**Impacted WBS/CBS:** CI, P, PM, COM

**Estimate Impact:**
- CI = 18% of CD = ~$77k
- P = 2% of MAT = ~$54k
- PM = 6% of (CD+CI+MAT) = ~$216k
- COM base (factor) = 3% of (CD+CI+MAT) = ~$108k

**Override Path:** Provide project schedule and duration estimates for time-based indirects calculation, or override factors in `_CONFIG.md`

---

## D-008: Contingency Method (PCT_BY_BUCKET)

**Decision:** Use PCT_BY_BUCKET contingency method with allowance-heavy adjustment

**Trigger:** Config specifies `contingency_method = PCT_BY_BUCKET`; 100% allowance-based estimate

**Evidence:**
- `_CONFIG.md` line 35: `contingency_method | PCT_BY_BUCKET`
- AGENT_ESTIMATING.md lines 676-689: Contingency baseline by CBS + allowance-heavy adjustment (+0.10 for >80% allowance share)

**Impacted WBS/CBS:** All CBS buckets (contingency applied to each)

**Estimate Impact:**
- E: 10% base + 10% allowance adjustment = 20%
- MAT: 15% base + 10% allowance adjustment = 25%
- CD: 20% base + 10% allowance adjustment = 30%
- CI: 20% base + 10% (factor-derived) = 30%
- PM: 10% base + 5% (factor-derived) = 15%
- P: 10% base + 5% (factor-derived) = 15%
- COM: 25% base + 5% (factor-derived) = 30%

**Override Path:** Change `contingency_method` to `RISK_BASED` in `_CONFIG.md`, or provide risk register with quantified risk impacts

---

## D-009: Escalation Mode

**Decision:** No escalation applied (escalation_mode = NONE)

**Trigger:** Config specifies NONE; pricing date is current (2026-01)

**Evidence:**
- `_CONFIG.md` line 36: `escalation_mode | NONE`
- Pricing date 2026-01 is current month

**Impacted WBS/CBS:** All CBS buckets

**Estimate Impact:** Estimate is in January 2026 dollars; no escalation to project midpoint or cashflow-weighted average date

**Override Path:** Change `escalation_mode` to `EXPLICIT` in `_CONFIG.md` and provide escalation factors or schedule/cashflow curve

---

## D-010: Rounding Policy

**Decision:** Round all summary values to nearest $1,000 CAD

**Trigger:** Config specifies rounding = 1000

**Evidence:**
- `_CONFIG.md` line 13: `rounding | 1000`

**Impacted WBS/CBS:** Summary.md totals (Detail.csv line items not rounded)

**Estimate Impact:** Summary totals rounded to $1k; minor differences may appear between Detail.csv sum and Summary.md due to rounding

**Override Path:** Change `rounding` parameter in `_CONFIG.md`

---

## Summary

| Decision Count | 10 |
|----------------|-----|
| Currency/Config Decisions | D-001, D-009, D-010 |
| Pricing Basis Decisions | D-002, D-003, D-004, D-005 |
| Scope/Config Decisions | D-006, D-007, D-008 |

All decisions are recorded with evidence and override path for next run transparency.

---

*Decision log prepared per AGENT_ESTIMATING SPEC requirements. All defaults and ambiguities documented for auditability.*

---

## PKG-13

# Decision Log

## PKG-13 Storage Tanks Estimate

### Snapshot Identification

| Field | Value |
|-------|-------|
| Snapshot ID | EST_PKG13_DRAFT_2026-01-28_2400 |
| Estimate Label | PKG13_DRAFT |
| Date | 2026-01-28 |

---

## Decisions

### D-001: Currency Selection

| Field | Value |
|-------|-------|
| Decision | Use CAD (Canadian dollars) as estimate currency |
| Trigger | Currency not specified in config for this package |
| Evidence | Project location is Fraser Surrey Terminal, Surrey, BC, Canada (decomposition Section 1) |
| Impacted WBS/CBS | All |
| Estimate Impact | All pricing in CAD |
| Override | Set currency in _CONFIG.md if USD or other currency required |

---

### D-002: Tank Supply Method

| Field | Value |
|-------|-------|
| Decision | Assume field-erected tanks by qualified tank fabricator |
| Trigger | Tank erection method not specified |
| Evidence | 15,000 MT capacity (~16,300 m³) typical for field erection; shop-built would be impractical |
| Impacted WBS/CBS | MAT, CD |
| Estimate Impact | Pricing based on field erection with shop-fabricated courses |
| Override | Confirm erection method in DEL-13.02 specification |

---

### D-003: Tank Fabrication Method

| Field | Value |
|-------|-------|
| Decision | Shop-fabricated shell courses with field erection |
| Trigger | Fabrication approach not specified |
| Evidence | Typical practice for large API 650 tanks; quality control advantages |
| Impacted WBS/CBS | MAT, CD |
| Estimate Impact | Included in tank supply and erection allowances |
| Override | Confirm fabrication approach in DEL-13.02 specification |

---

### D-004: Agitator Supply Approach

| Field | Value |
|-------|-------|
| Decision | OEM supply with Contractor installation |
| Trigger | Agitator procurement approach not specified |
| Evidence | Typical for mechanical equipment; vendor design for tank geometry |
| Impacted WBS/CBS | MAT, CD |
| Estimate Impact | Separate supply and installation line items |
| Override | Confirm procurement approach in project execution plan |

---

### D-005: Internal Coating Responsibility

| Field | Value |
|-------|-------|
| Decision | Internal coating by tank vendor as part of tank supply |
| Trigger | Coating responsibility not specified |
| Evidence | Typical for food-grade applications; vendor warranty considerations |
| Impacted WBS/CBS | MAT |
| Estimate Impact | Coating included in MAT allowance |
| Override | Confirm with PKG-26 scope definition |

---

### D-006: External Coating Responsibility

| Field | Value |
|-------|-------|
| Decision | External coating by tank vendor or coating contractor |
| Trigger | Coating responsibility not specified |
| Evidence | Can be tank vendor scope or separate coating contract |
| Impacted WBS/CBS | MAT |
| Estimate Impact | Coating included in MAT allowance |
| Override | Confirm with PKG-26 scope definition |

---

### D-007: Productivity Factor

| Field | Value |
|-------|-------|
| Decision | Use 1.0 productivity factor for BC lower mainland |
| Trigger | Site-specific productivity data not available |
| Evidence | BC lower mainland has adequate skilled labor pool; baseline assumption |
| Impacted WBS/CBS | CD, CI |
| Estimate Impact | Direct and indirect labor costs at baseline rates |
| Override | Adjust if site conditions warrant premium (access, congestion, etc.) |

---

### D-008: Working Hours

| Field | Value |
|-------|-------|
| Decision | Standard 8-10 hour shifts |
| Trigger | Work schedule not specified |
| Evidence | Default for industrial construction in BC |
| Impacted WBS/CBS | CD, CI |
| Estimate Impact | No shift premium included |
| Override | If extended hours or shifts required, adjust labor rates |

---

### D-009: Pricing Basis

| Field | Value |
|-------|-------|
| Decision | All line items priced via allowances (fallback typical model) |
| Trigger | No vendor quotes or rate tables available |
| Evidence | No pricing sources discovered during source indexing |
| Impacted WBS/CBS | All |
| Estimate Impact | All line items marked ALLOWANCE or PARAMETRIC; confidence LOW |
| Override | Provide vendor quotes or rate tables for next estimate run |

---

### D-010: Indirects Factor Method

| Field | Value |
|-------|-------|
| Decision | Use factor-based indirects model (fallback typical) |
| Trigger | Project-specific indirects data not available |
| Evidence | CI=18% of CD, P=2% of MAT, PM=6% of base, COM=3% of base |
| Impacted WBS/CBS | CI, P, PM, COM |
| Estimate Impact | Indirects derived from direct cost base |
| Override | Provide project-specific indirects breakdown or schedule-based model |

---

### D-011: Contingency Rates

| Field | Value |
|-------|-------|
| Decision | Elevated contingency rates due to 100% allowance-based estimate |
| Trigger | No quotes available; all pricing via allowances |
| Evidence | Fallback typical model with AllowanceShare adjustment |
| Impacted WBS/CBS | CONT |
| Estimate Impact | Contingency ~25.9% of base ($5.235M on $20.245M) |
| Override | Reduce contingency as vendor quotes replace allowances |

---

### D-012: Escalation Mode

| Field | Value |
|-------|-------|
| Decision | No escalation applied (NONE mode) |
| Trigger | Config default; pricing date is current |
| Evidence | Pricing date 2026-01 is current month |
| Impacted WBS/CBS | None |
| Estimate Impact | No escalation reserve included |
| Override | Enable EXPLICIT escalation in _CONFIG.md if project schedule extends pricing validity |

---

## Decision Summary

| ID | Decision | Impact |
|----|----------|--------|
| D-001 | CAD currency | All pricing |
| D-002 | Field-erected tanks | MAT/CD split |
| D-003 | Shop-fabricated courses | Quality/cost basis |
| D-004 | OEM agitator supply | Procurement approach |
| D-005 | Tank vendor internal coating | MAT scope |
| D-006 | Tank vendor external coating | MAT scope |
| D-007 | 1.0 productivity factor | Labor rates |
| D-008 | Standard shift hours | No premium |
| D-009 | Allowance-based pricing | LOW confidence |
| D-010 | Factor-based indirects | CI/P/PM/COM |
| D-011 | Elevated contingency | 25.9% reserve |
| D-012 | No escalation | Current pricing |

---

## PKG-14

# Decision Log

## PKG-14 Process Piping Estimate

| ID | Decision Statement | Trigger | Evidence | Impacted WBS/CBS | Estimate Impact | How to Override |
|----|-------------------|---------|----------|------------------|-----------------|-----------------|
| D-001 | Currency set to CAD (Canadian dollars) | Default selection required | Project location: Fraser Surrey Terminal, Surrey, BC, Canada per decomposition Section 1 | All | All amounts | Set `currency` in _CONFIG.md |
| D-002 | Piping assumed to be shop prefabricated with field assembly | Fabrication approach clarification | Industry standard for quality control on large diameter process piping | MAT, CD | Shop vs field labor split | Confirm fabrication strategy in DEL-14.02 |
| D-003 | Welding assumed per ASME B31.3 with coded welders | Welding code clarification | Process piping for petroleum/chemical service | CD | Welder qualification costs | Confirm code requirements in DEL-14.02 |
| D-004 | NDE assumed 100% RT on headers, spot RT on smaller lines | Inspection level clarification | Typical for process headers vs utility piping | CD | NDE costs ~$125,000 | Confirm NDE requirements in DEL-14.02 |
| D-005 | Productivity factor set to 1.0 (BC lower mainland baseline) | No site-specific productivity data | Project location in established industrial port area | PKG-14 / CD | Labor rates | Provide site-specific productivity factors |
| D-006 | Site access assumed via established industrial roads | Access clarification | Fraser Surrey Terminal is operating facility with road access | PKG-14 / CD | Logistics costs | Confirm access restrictions |
| D-007 | Working hours assumed standard 8-10 hour shifts | No shift schedule provided | Typical industrial construction | PKG-14 / CD, CI | Labor productivity | Provide project schedule/shift requirements |
| D-008 | All pricing via allowances (fallback typical model) | No vendor quotes or rate tables available | Source index search returned no pricing sources | All | 100% allowance basis | Provide vendor quotes or rate tables |
| D-009 | Total piping quantity assumed ~1,700 lm across all systems | No P&IDs or piping GAs available | Parametric estimate based on 32 unloading stations, 3 tanks, terminal layout | MAT, CD | Quantity basis for all pipe lines | Complete DEL-14.01 P&IDs and GAs |
| D-010 | Indirects factors applied per fallback typical model (CI 18%, PM 6%, P 2%, COM 3%) | No project-specific indirects data | Fallback typical model per AGENT_ESTIMATING STRUCTURE | CI, PM, P, COM | $835,000 indirects | Provide project-specific indirects |
| D-011 | Contingency rates elevated due to 100% allowance-based estimate (+10% on direct CBS, +5% on factors) | High uncertainty in allowance-based estimate | Per AGENT_ESTIMATING fallback contingency method | CONT | 26.2% weighted contingency | Reduce allowance share with quotes |
| D-012 | Escalation mode set to NONE | Default selection | Pricing date is current (January 2026) | All | No escalation | Set `escalation_mode` in _CONFIG.md |
| D-013 | Rail unloading header sized at 16-20 inch based on 32 station throughput | No hydraulic calculations available | 32 stations × typical 150-200 m³/hr per station = 4,800-6,400 m³/hr total | MAT | Header sizing | Complete DEL-14.03 pipe sizing calculations |
| D-014 | Export piping sized at 12-16 inch based on marine loading rate | No loading rate defined | 1,000,000 MT/annum throughput divided by operating hours | MAT | Export pipe sizing | Confirm loading rate from ER |
| D-015 | Nitrogen distribution assumed 400 lm covering tanks, headers, marine loading | No N2 P&ID available | Blanketing and purge requirements for canola oil service | MAT, CD | N2 system quantity | Complete N2 distribution in DEL-14.01 |


---

## PKG-15

# Decision Log — PKG-15 Pumps & Rotating Equipment Estimate

**Snapshot ID:** EST_PKG15_DRAFT_2026-01-28_2345
**Package:** PKG-15 Pumps & Rotating Equipment
**Estimate Date:** 2026-01-28
**Currency:** CAD
**Pricing Date:** 2026-01

---

## Decision Entries

### D-001: Workspace Paths and Inputs Discovery
**Decision:** Used default workspace paths from Project Instance Paths.
**Trigger:** Standard initialization; no explicit paths provided by human.
**Evidence:**
- Execution root: `/Users/ryan/ai-env/projects/chirality-app/test/execution/`
- Decomposition: `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md`
- Estimates output: `/Users/ryan/ai-env/projects/chirality-app/test/execution/_Estimates/`

**Impact:** Standard paths; no estimate impact.
**How to override:** Provide explicit paths in conversation.

---

### D-002: Currency Selection
**Decision:** Use CAD (Canadian Dollars) as estimate currency.
**Trigger:** Project location in Surrey, BC, Canada; existing _CONFIG.md specifies CAD.
**Evidence:**
- _CONFIG.md line 9: `currency | CAD | Canadian dollars (project location: Surrey, BC)`
- Project location: Fraser Surrey Terminal, Surrey, BC

**Impact:** All costs in CAD; no currency conversion required.
**How to override:** Update _CONFIG.md currency parameter.

---

### D-003: Pricing Date
**Decision:** Use 2026-01 (January 2026) as pricing date.
**Trigger:** Current date is 2026-01-28; _CONFIG.md specifies 2026-01.
**Evidence:**
- _CONFIG.md line 10: `pricing_date | 2026-01 | January 2026 (current date)`
- Current pricing environment

**Impact:** Costs reflect January 2026 pricing (no escalation applied).
**How to override:** Update _CONFIG.md pricing_date parameter.

---

### D-004: Estimate Label
**Decision:** Use estimate label "PKG15_DRAFT"
**Trigger:** Package-specific estimate following established phased approach.
**Evidence:** _CONFIG.md pattern of package-by-package estimates; PKG-00 through PKG-13 completed.

**Impact:** Snapshot labeled as draft estimate for PKG-15.
**How to override:** Update estimate_label in conversation or config.

---

### D-005: Pump Quantities - Parametric Allowance Approach
**Decision:** Use parametric allowances for pump quantities since deliverables show "TBD" for all pump counts.
**Trigger:** Deliverable documents (DEL-15.02, DEL-15.04) list all pump quantities as "TBD" pending DEL-15.03 calculations.
**Evidence:**
- DEL-15.04 Datasheet line 36: "Quantity | **TBD** — One data sheet per pump unit"
- DEL-15.02 Specification lines 27-32: All pump service quantities shown as "**TBD**"
- Exploration agent confirmed: "most pump quantities and capacities marked as TBD"

**Estimated quantities (for budgeting):**
- Railcar unloading transfer pumps: 4 units (2 duty + 2 standby, supporting 32 railcar stations and 1M MT/annum throughput)
- Marine loading pumps: 2 units (1 duty + 1 standby)
- Tank transfer pumps: 2 units (for 3 x 15,000 MT tanks)
- Sump pumps: 6 units (railcar area, marine loading area, tank farm containment)
- **Total: 14 pump units**

**Impacted WBS/CBS:** All PKG-15 deliverables; Materials (MAT), Construction Directs (CD)
**Estimate Impact:** HIGH - pump quantities directly affect equipment cost and installation hours.
**How to override:** Provide finalized pump quantities from DEL-15.03 calculations or ER Part 2.

**Related Assumptions:** A-001, A-002, A-003, A-004

---

### D-006: Pump Sizing and Power Ratings
**Decision:** Use typical sizing ranges for process facility pumps in canola oil service.
**Trigger:** Specific pump capacities and motor power ratings listed as "TBD" in deliverables.
**Evidence:**
- DEL-15.02 lines 76-88: All performance data (flow, head, power) shown as "TBD"
- Facility throughput requirement: 1,000,000 MT/annum
- 32 railcar stations, 3 storage tanks, marine loading capacity

**Estimated sizing:**
- Railcar unloading pumps: 200 m³/hr @ 50m head, 30 kW motors (estimate based on throughput requirements)
- Marine loading pumps: 400 m³/hr @ 40m head, 50 kW motors
- Tank transfer pumps: 150 m³/hr @ 30m head, 15 kW motors
- Sump pumps: 25 m³/hr @ 15m head, 3 kW motors

**Impacted WBS/CBS:** DEL-15.01 through DEL-15.05; Materials (MAT), Electrical (E)
**Estimate Impact:** MEDIUM - affects equipment cost and electrical load.
**How to override:** Provide finalized pump sizing from DEL-15.03 or vendor data.

**Related Assumptions:** A-002, A-005

---

### D-007: API 610 Pump Specification
**Decision:** Assume API 610 centrifugal pumps for all process services; standard industrial pumps for sump service.
**Trigger:** DEL-15.02 specifies API 610 as primary standard; typical for process industry.
**Evidence:**
- DEL-15.02 line 187: "**API 610** (latest edition) — Centrifugal Pumps for Petroleum, Petrochemical and Natural Gas Industries"
- Line 134: "Horizontal or vertical centrifugal pump per API 610"

**Impact:** API 610 compliance increases equipment cost vs. commercial pumps (typically 1.5-2.0× cost multiplier).
**Impacted WBS/CBS:** Materials (MAT)
**Estimate Impact:** MEDIUM - affects unit costs
**How to override:** Confirm API 610 requirement or allow commercial pumps per ER Part 2.

**Related Assumptions:** A-002

---

### D-008: Materials of Construction
**Decision:** Carbon steel/cast iron casings with stainless steel wetted parts for food-grade canola oil service.
**Trigger:** DEL-15.02 identifies canola oil as food-grade product; materials must be food-compatible.
**Evidence:**
- DEL-15.02 line 128: "Canola oil is a food-grade product. Materials in contact with product should be compatible with food-grade service"
- Line 118: Material options include cast iron, ductile iron, carbon steel, stainless steel

**Assumed materials:**
- Casings: Cast iron or carbon steel
- Impellers/wetted parts: 316 stainless steel
- Seal faces: Silicon carbide
- Baseplates: Structural steel

**Impacted WBS/CBS:** Materials (MAT)
**Estimate Impact:** LOW - typical materials for vegetable oil service.
**How to override:** Provide specific material requirements from ER Part 2 or vendor recommendations.

**Related Assumptions:** A-002

---

### D-009: Engineering Effort Distribution
**Decision:** Allocate engineering hours across 5 deliverables using complexity weighting.
**Trigger:** No explicit engineering hours provided in deliverables.
**Evidence:** Standard EPC practice; similar packages (PKG-00, PKG-11) used parametric approach.

**Distribution:**
- DEL-15.01 Design Drawings: 40% (arrangement, foundation interface most complex)
- DEL-15.02 Specification: 25% (procurement specification development)
- DEL-15.03 Calculations: 20% (sizing, NPSH, system curves)
- DEL-15.04 Data Sheets: 10% (vendor data review and approval)
- DEL-15.05 Test Records: 5% (commissioning support and documentation)

**Impacted WBS/CBS:** Engineering (E)
**Estimate Impact:** LOW - distribution methodology, not absolute value.
**How to override:** Provide detailed engineering hour estimates by deliverable.

---

### D-010: Indirects and Management Factors
**Decision:** Apply fallback typical model factors for indirects and project management.
**Trigger:** No project-specific indirects or PM rates found in rate tables or source documents.
**Evidence:** No rate tables in `/Users/ryan/ai-env/projects/chirality-app/test/execution/_Estimates/_RateTables/`

**Factors applied (from AGENT_ESTIMATING.md fallback model):**
- Construction Indirects (CI): 18% of Construction Directs (CD)
- Procurement Services (P): 2% of (MAT + FRT)
- EPCM/PM: 6% of (CD + CI + MAT)
- Commissioning (COM): 3% of (CD + CI + MAT)

**Impacted WBS/CBS:** CI, P, PM, COM buckets
**Estimate Impact:** MEDIUM - affects total project cost by ~25-30%.
**How to override:** Provide project-specific rates in _RateTables/ or update _CONFIG.md.

**Related Assumptions:** A-006, A-007, A-008

---

### D-011: Contingency Method
**Decision:** Use PCT_BY_BUCKET method with allowance-heavy adjustments.
**Trigger:** _CONFIG.md specifies PCT_BY_BUCKET; estimate has high allowance content due to TBD quantities.
**Evidence:**
- _CONFIG.md line 35: `contingency_method | PCT_BY_BUCKET`
- High TBD content increases uncertainty

**Baseline contingency by CBS:**
- Engineering (E): 10%
- Project Management (PM): 10%
- Procurement (P): 10%
- Materials (MAT): 15% + allowance adjustment
- Construction Directs (CD): 20% + allowance adjustment
- Construction Indirects (CI): 20%
- Commissioning (COM): 25%

**Allowance adjustments:**
- If bucket allowance share ≥ 50%: +5%
- If bucket allowance share ≥ 80%: additional +5% (total +10%)

**Impacted WBS/CBS:** All CBS buckets
**Estimate Impact:** HIGH - contingency 20-30% of base cost expected given TBD quantities.
**How to override:** Switch to RISK_BASED method in _CONFIG.md or provide better quantity data.

---

### D-012: Rounding Policy
**Decision:** Round to nearest $1,000 CAD.
**Trigger:** _CONFIG.md specifies rounding = 1000.
**Evidence:** _CONFIG.md line 12: `rounding | 1000 | Round to nearest $1,000`

**Impact:** All summary values rounded to $1,000.
**How to override:** Update _CONFIG.md rounding parameter.

---

### D-013: Escalation Mode
**Decision:** No escalation applied (current dollars).
**Trigger:** _CONFIG.md specifies escalation_mode = NONE.
**Evidence:** _CONFIG.md line 36: `escalation_mode | NONE | No escalation (current pricing)`

**Impact:** Estimate is in January 2026 dollars; no time-phased escalation.
**How to override:** Set escalation_mode = EXPLICIT in _CONFIG.md.

---

### D-014: Installation Labor Productivity
**Decision:** Use standard industrial rates for BC coastal location with skilled trades.
**Trigger:** No project-specific productivity data provided.
**Evidence:** Project location (Fraser Surrey Terminal, Surrey, BC); industrial terminal setting.

**Assumed productivity:**
- Pump setting and alignment: 24 manhours per pump unit (medium-size process pumps)
- Piping connections: included in PKG-14 (Process Piping)
- Electrical connections: included in PKG-17/19 (Electrical)
- Testing and commissioning: 16 manhours per pump unit

**Labor rate:** $95/hr loaded (BC prevailing industrial rate including benefits, burden)

**Impacted WBS/CBS:** Construction Directs (CD)
**Estimate Impact:** MEDIUM
**How to override:** Provide project-specific labor rates and productivity factors.

**Related Assumptions:** A-003

---

### D-015: Commissioning Scope
**Decision:** Commissioning includes FAT witness, installation supervision, performance testing, and documentation.
**Trigger:** DEL-15.05 scope; standard for critical rotating equipment.
**Evidence:** DEL-15.05 anticipated artifacts include FAT records, performance test records, vibration analysis.

**Assumed commissioning effort:**
- FAT witness (vendor shop): 8 hours per major pump (included in travel allowance)
- Installation supervision: included in Construction Indirects
- Performance testing: 16 manhours per pump
- Vibration analysis: 4 manhours per pump
- Documentation: 8 manhours per pump

**Impacted WBS/CBS:** Commissioning (COM)
**Estimate Impact:** LOW - commissioning 3-5% of total.
**How to override:** Provide detailed commissioning plan from DEL-15.05.

**Related Assumptions:** A-009

---

## Summary

**Total Decisions:** 15
**High Impact:** 2 (D-005 pump quantities, D-011 contingency)
**Medium Impact:** 5
**Low Impact:** 8

**Key Uncertainties:**
1. Pump quantities (TBD in all deliverables → parametric allowance used)
2. Pump sizing and power ratings (TBD → typical values assumed)
3. No vendor quotes available (all equipment priced parametrically)
4. Installation labor productivity assumptions

**Next Run Improvements:**
- Finalize pump quantities from DEL-15.03 calculations
- Obtain vendor budgetary quotes for API 610 pumps
- Confirm engineering hours by deliverable
- Validate labor rates and productivity for BC location


---

## PKG-16

# Decision Log — PKG-16 Valves & Specialty Equipment

**Snapshot ID:** EST_PKG16_DRAFT_2026-01-28_2347
**Package:** PKG-16 Valves & Specialty Equipment
**Date:** 2026-01-28

---

## Purpose

This log records all decisions made during the estimating process where ambiguities, missing inputs, or defaults required agent selection of a runnable path forward.

Each decision is traceable to its trigger, evidence (or lack thereof), impacted scope, and override path for the next iteration.

---

## Decision Entries

### D-1601: Workspace Paths (Auto-Discovery)

**Decision:** Use default project paths as defined in AGENT_ESTIMATING.md

**Trigger:** No explicit paths provided by human; using defaults

**Evidence:**
- Execution root: `/Users/ryan/ai-env/projects/chirality-app/test/execution/` (exists, verified)
- Decomposition: `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md` (exists, verified)
- Estimates output: `/Users/ryan/ai-env/projects/chirality-app/test/execution/_Estimates/` (exists, verified)

**Impacted WBS/CBS:** All

**Estimate Impact:** None (paths valid)

**Override:** N/A (paths are correct)

---

### D-1602: Currency Selection

**Decision:** Use **CAD** (Canadian dollars) as estimate currency

**Trigger:** Config file specifies CAD; project location in Surrey, BC, Canada

**Evidence:**
- `_CONFIG.md` line 9: `currency | CAD | Canadian dollars (project location: Surrey, BC)`
- Project location: Fraser Surrey Terminal, 11060 Elevator Road, Surrey, BC
- All prior package estimates (PKG-00 through PKG-14) used CAD

**Impacted WBS/CBS:** All

**Estimate Impact:** All amounts in CAD; no currency conversion required

**Override:** Update `_CONFIG.md` if different currency desired

---

### D-1603: Pricing Date

**Decision:** Use **January 2026** (2026-01) as pricing date

**Trigger:** Config file specifies 2026-01; current date is 2026-01-28

**Evidence:**
- `_CONFIG.md` line 10: `pricing_date | 2026-01 | January 2026 (current date)`
- Current date: 2026-01-28

**Impacted WBS/CBS:** All

**Estimate Impact:** Prices represent January 2026 dollars; no escalation applied (per D-1609)

**Override:** Update `_CONFIG.md` if different pricing date desired

---

### D-1604: Estimate Label

**Decision:** Use **PKG16_DRAFT** as estimate label

**Trigger:** Following established pattern from prior packages

**Evidence:**
- Prior estimates: PKG00_DRAFT, PKG01_DRAFT, PKG03_DRAFT, PKG04_DRAFT, etc.
- This is conceptual/budgeting estimate (no design quantities or vendor quotes)

**Impacted WBS/CBS:** N/A (label only)

**Estimate Impact:** Snapshot ID = EST_PKG16_DRAFT_2026-01-28_2347

**Override:** Provide alternate label in conversation or `_CONFIG.md`

---

### D-1605: Rounding Policy

**Decision:** Round summary totals to nearest **$1,000 CAD**

**Trigger:** Config file specifies rounding = 1000

**Evidence:**
- `_CONFIG.md` line 12: `rounding | 1000 | Round to nearest $1,000`
- Consistent with all prior package estimates

**Impacted WBS/CBS:** Summary only (Detail.csv retains calculated precision)

**Estimate Impact:** Summary totals rounded to nearest $1k; Detail.csv unrounded

**Override:** Update `_CONFIG.md` if different rounding desired

---

### D-1606: Scope Inclusions/Exclusions

**Decision:** Include Engineering, PM, Procurement, Materials, Construction Directs/Indirects, Commissioning; exclude Owner's costs, land, financing, permits

**Trigger:** Config file specifies include/exclude scopes

**Evidence:**
- `_CONFIG.md` lines 16-30: Include scopes E, PM, P, MAT, CD, CI, COM; exclude Owner's costs, land, financing, permits
- Consistent with EPC/Design-Build scope boundary
- Decomposition Section 1.2 (Scope Focus) — Contractor responsible for design, procurement, construction, commissioning

**Impacted WBS/CBS:** All CBS buckets

**Estimate Impact:** Full EPC scope coverage; Owner-supplied items excluded

**Override:** Update `_CONFIG.md` include/exclude lists if scope boundary changes

---

### D-1607: Contingency Method

**Decision:** Use **PCT_BY_BUCKET** with allowance-heavy adjustments

**Trigger:** Config file specifies contingency_method = PCT_BY_BUCKET

**Evidence:**
- `_CONFIG.md` line 35: `contingency_method | PCT_BY_BUCKET | Apply contingency % by CBS bucket`
- AGENT_ESTIMATING fallback model (lines 676-689): baseline contingency + allowance-heavy adjustment

**Impacted WBS/CBS:** All CBS buckets (contingency line)

**Estimate Impact:** Contingency rates 15-30% by CBS bucket depending on allowance share

**Override:** Update `_CONFIG.md` to `RISK_BASED` if three-point estimate desired; provide risk model inputs

---

### D-1608: Indirects Model

**Decision:** Use **factor-based** indirects (CI, P, PM, COM)

**Trigger:** No construction schedule or duration data available

**Evidence:**
- No schedule available in workspace
- AGENT_ESTIMATING protocol (lines 307-320): "factor-based model (default) using the fallback typical model" when schedule unavailable
- Factors: CI=18%, P=2%, PM=6%, COM=3% (AGENT_ESTIMATING lines 666-673)

**Impacted WBS/CBS:** CI, P, PM, COM

**Estimate Impact:**
- CI = 0.18 × CD
- P = 0.02 × MAT
- PM = 0.06 × (CD + CI + MAT)
- COM = 0.03 × (CD + CI + MAT)

**Override:** Provide construction schedule and duration data to enable time-based indirects model

---

### D-1609: Escalation Mode

**Decision:** Use **NONE** (no escalation)

**Trigger:** Config file specifies escalation_mode = NONE

**Evidence:**
- `_CONFIG.md` line 36: `escalation_mode | NONE | No escalation (current pricing)`
- No schedule available for cashflow curve
- January 2026 pricing basis (current)

**Impacted WBS/CBS:** N/A (no escalation line)

**Estimate Impact:** Estimate in current January 2026 dollars; escalation exposure noted in Risk Register

**Override:** Update `_CONFIG.md` to `EXPLICIT` and provide schedule/cashflow data if escalation calculation desired

---

### D-1610: WBS to CBS Mapping

**Decision:** Map PKG-16 deliverables to CBS buckets per deliverable type

**Trigger:** Deliverables span multiple CBS categories (engineering, materials, construction)

**Evidence:**
- DEL-16.01 (drawings) → Engineering (E)
- DEL-16.02 (specifications) → Engineering (E)
- DEL-16.03 (calculations) → Engineering (E)
- DEL-16.04 (datasheets) → Engineering (E)
- DEL-16.05 (test records) → Construction Indirects (CI) and Commissioning (COM)
- Valve equipment → Materials (MAT)
- Valve installation → Construction Directs (CD)

**Impacted WBS/CBS:** All deliverables

**Estimate Impact:** Engineering costs allocated to E; materials to MAT; installation to CD; testing/commissioning to CI/COM

**Override:** N/A (mapping follows deliverable type convention)

---

### D-1611: Valve Quantity Estimation Basis

**Decision:** Estimate valve quantities using **parametric approach** based on facility type and system complexity

**Trigger:** No P&IDs available; no valve lists; no equipment datasheets with valve counts

**Evidence:**
- Deliverable status: All INITIALIZED (no design quantities)
- Facility parameters from decomposition:
  - 32 railcar unloading stations (PKG-10)
  - 3 storage tanks × 15,000 MT each (PKG-13)
  - Marine loading system (PKG-11)
  - Product transfer and metering (PKG-12)
- Typical transload facility valve density (industry experience)

**Impacted WBS/CBS:** MAT, CD (valve quantities drive material and installation costs)

**Estimate Impact:** Valve count estimate:
- Control valves: ~25-35 units (flow, pressure, level control at railcar stations, tanks, loading system)
- Isolation valves: ~120-180 units (manual and automated; line isolation, equipment isolation)
- Relief valves: ~15-25 units (tank relief, pump relief, line thermal relief)
- Strainers: ~15-20 units (pump suction protection, meter protection)
- Total: ~175-260 valves

**Assumption:** A-1601 (valve count parametric)

**Override:** Provide P&IDs with valve counts and service assignments to replace parametric estimate with actual valve list

---

### D-1612: Valve Size Distribution

**Decision:** Estimate valve size distribution using **typical size mix** for transload facility

**Trigger:** No line list available; no pipe sizes defined; no valve datasheets with sizes

**Evidence:**
- Facility type: Canola oil transload with railcar unloading, storage, marine loading
- Typical transload piping: 2" to 12" product lines; 1" to 4" utility/control lines
- Larger isolation valves at tank inlets/outlets (8" to 12")
- Smaller control valves at railcar stations (2" to 4")

**Impacted WBS/CBS:** MAT (valve cost varies significantly with size)

**Estimate Impact:** Size distribution assumption:
- Small (DN50-DN100 / 2"-4"): 60% of valves
- Medium (DN150-DN200 / 6"-8"): 30% of valves
- Large (DN250-DN300 / 10"-12"): 10% of valves

**Assumption:** A-1602 (valve size distribution)

**Override:** Provide piping line list with line sizes to replace size distribution assumption with actual valve sizes

---

### D-1613: Valve Material Selection

**Decision:** Use **stainless steel (316SS)** as baseline for product-contact valves

**Trigger:** Food-grade canola oil service requires cleanable, corrosion-resistant materials

**Evidence:**
- DEL-16.04 Datasheet.md lines 303-314: "Stainless steel (316SS or 304SS) for food-grade cleanliness and corrosion resistance"
- DEL-16.02 Datasheet.md lines 167-176: "Stainless steel (316SS or 304SS) preferred for product-contact materials"
- Coastal marine environment (Fraser Surrey Terminal) requires corrosion-resistant materials
- Food-grade product (canola oil) requires cleanable surfaces

**Impacted WBS/CBS:** MAT (stainless steel valves cost ~2-3× carbon steel)

**Estimate Impact:** Higher material costs vs. carbon steel; lower lifecycle maintenance costs

**Assumption:** A-1603 (material selection)

**Override:** Provide DEL-16.02 specification with actual material selections if different from 316SS baseline

---

### D-1614: Actuator Type Distribution

**Decision:** Estimate actuator distribution as **60% manual, 30% pneumatic, 10% electric**

**Trigger:** No P&IDs with actuation requirements; no control philosophy available

**Evidence:**
- Isolation valves: Typically manual unless ESD or seasonal operation required
- Control valves: Typically pneumatic actuation for modulating control
- Large isolation valves (MOVs): Electric actuation for large sizes (DN200+)
- Typical transload facility actuation mix (industry experience)

**Impacted WBS/CBS:** MAT (actuators add significant cost), CD (automated valves require hookup)

**Estimate Impact:** Actuated valve costs ~3-5× manual valves (actuator + accessories + hookup)

**Assumption:** A-1604 (actuator type distribution)

**Override:** Provide P&IDs with valve actuation requirements or control philosophy document

---

### D-1615: Control Valve Complexity

**Decision:** Estimate control valve complexity as **50% standard globe, 30% ball/butterfly, 20% severe service**

**Trigger:** No valve datasheets with trim types; no sizing calculations available

**Evidence:**
- Standard globe valves: Typical for general flow/pressure control (railcar stations, tank level control)
- Ball/butterfly control valves: Large sizes, on/off with modulation capability
- Severe service: Potential high pressure drop applications (pressure reducing stations)

**Impacted WBS/CBS:** MAT (severe service valves cost ~2-3× standard)

**Estimate Impact:** Weighted average control valve cost reflects complexity mix

**Assumption:** A-1605 (control valve complexity)

**Override:** Provide DEL-16.03 sizing calculations or DEL-16.04 datasheets with valve body styles and trim types

---

### D-1616: Pricing Sources (Fallback Model)

**Decision:** Use **fallback typical model** for all valve pricing (no vendor quotes or rate tables available)

**Trigger:** Source discovery (Source_Index.md) found no vendor quotes or rate tables

**Evidence:**
- Searched `/Users/ryan/ai-env/projects/chirality-app/test/execution/PKG-16_Valves_and_Specialty_Equipment/0_References/` — no vendor quotes
- Searched `/Users/ryan/ai-env/projects/chirality-app/test/execution/_Estimates/_RateTables/` — no rate tables
- All deliverables INITIALIZED status (no design quantities)

**Impacted WBS/CBS:** MAT, CD (all valve material and installation costs)

**Estimate Impact:** 100% allowance-based pricing with LOW confidence; typical market rates for BC/Canada

**Override:** Provide vendor budgetary quotes or populate `_RateTables/` with project-specific valve rates

---

### D-1617: Valve Count Parametric Model

**Decision:** Estimate valve count using **facility-type parametric** approach

**Trigger:** No P&IDs; no valve lists; no equipment datasheets with valve interface counts

**Evidence:**
- 32 railcar unloading stations: ~4-6 valves per station (unloading valve, isolation, drain, sample) → 128-192 valves
- 3 storage tanks: ~10-15 valves per tank (inlet, outlet, relief, drain, gauge, sample) → 30-45 valves
- Marine loading system: ~15-25 valves (loading arm isolation, flow control, relief)
- Product transfer: ~10-15 valves (transfer pumps, meters, manifolds)
- Total range: ~183-277 valves
- Midpoint: ~230 valves

**Impacted WBS/CBS:** MAT (valve count drives material cost), CD (installation cost)

**Estimate Impact:** Parametric valve count = 220 valves (conservative midpoint)
- Control: 30 units (flow, pressure, level control)
- Isolation: 150 units (manual and automated block valves)
- Relief: 20 units (tank, pump, line protection)
- Strainers: 20 units (pump suction, meter protection)

**Assumption:** A-1601 (valve count parametric)

**Override:** Provide P&IDs with actual valve count and service assignments

---

### D-1618: Valve Unit Cost Assumptions

**Decision:** Use **typical BC market rates** for valve pricing (no vendor quotes)

**Trigger:** No vendor quotes or rate tables available

**Evidence:**
- Industry experience: BC/Lower Mainland valve pricing
- Stainless steel valve premium (~2-3× vs. carbon steel)
- Actuator costs: Pneumatic ~$3k-$15k, Electric ~$8k-$40k (size-dependent)
- Control valve positioners: ~$2k-$5k per unit

**Impacted WBS/CBS:** MAT

**Estimate Impact:** Valve allowances sized using typical unit costs:
- Small isolation valve (DN50-100, SS, manual): $800-$2,500 each
- Medium isolation valve (DN150-200, SS, manual): $3,000-$8,000 each
- Large isolation valve (DN250-300, SS, manual): $10,000-$25,000 each
- Control valve (DN50-100, SS, pneumatic, positioner): $8,000-$15,000 each
- Relief valve (API 526, SS): $3,000-$12,000 each (size-dependent)
- Strainer (SS, Y-type or basket): $1,500-$5,000 each

**Assumption:** A-1606 (valve unit costs)

**Override:** Provide vendor budgetary quotes or historical pricing data for BC/Canada market

---

### D-1619: Installation Labor Productivity

**Decision:** Use **typical valve installation productivity** (4-12 hours per valve depending on size and complexity)

**Trigger:** No project-specific installation rates or crew productivity data

**Evidence:**
- Small valves (DN50-100): ~4-6 hours (rigging, bolting, alignment, testing)
- Medium valves (DN150-200): ~8-12 hours
- Large valves (DN250-300): ~16-24 hours
- Actuated valves: +2-4 hours for actuator mounting and hookup
- BC labor rate (all-in with benefits, indirects): ~$85-$110/hr

**Impacted WBS/CBS:** CD

**Estimate Impact:** Installation labor allowances reflect size and actuation complexity

**Assumption:** A-1607 (installation productivity)

**Override:** Provide project labor rate tables and construction management estimate of crew productivity

---

### D-1620: Indirects Factors (CI, P, PM, COM)

**Decision:** Apply factor-based indirects per AGENT_ESTIMATING fallback model

**Trigger:** No construction schedule available; factor-based appropriate for conceptual estimate

**Evidence:**
- AGENT_ESTIMATING lines 666-673: CI=18%, P=2%, PM=6%, COM=3%
- All prior package estimates used same factors
- No schedule or duration data available

**Impacted WBS/CBS:** CI, P, PM, COM

**Estimate Impact:**
- CI = 0.18 × CD (construction supervision, QA/QC, HSE, site overhead)
- P = 0.02 × MAT (procurement, expediting, inspection)
- PM = 0.06 × (CD + CI + MAT) (project management, engineering management, cost/schedule control)
- COM = 0.03 × (CD + CI + MAT) (commissioning, testing per DEL-16.05, handover)

**Override:** Provide construction schedule and duration estimate to enable time-based indirects calculation

---

### D-1621: Contingency Baseline Rates

**Decision:** Apply baseline contingency rates per AGENT_ESTIMATING model with allowance-heavy adjustments

**Trigger:** All pricing is allowance/parametric-based; no vendor quotes

**Evidence:**
- AGENT_ESTIMATING lines 678-689: baseline + allowance-heavy adjustment
- Baseline: E=10%, MAT=15%, CD=20%, CI=20%, P=10%, PM=10%, COM=25%
- Allowance share ≥50%: +5%; ≥80%: +10%
- PKG-16 allowance share: 100% (all allowance/parametric)

**Impacted WBS/CBS:** CONT (contingency)

**Estimate Impact:** Elevated contingency rates:
- E: 20% (baseline 10% + 10% allowance adjustment)
- MAT: 25% (baseline 15% + 10% allowance adjustment)
- CD: 30% (baseline 20% + 10% allowance adjustment)
- CI: 30% (baseline 20% + 10% allowance adjustment)
- P: 15% (baseline 10% + 5% allowance adjustment)
- PM: 15% (baseline 10% + 5% allowance adjustment)
- COM: 35% (baseline 25% + 10% allowance adjustment)

**Override:** Obtain vendor quotes and design quantities to reduce allowance share and lower contingency

---

### D-1622: Control Valve vs Isolation Valve Ratio

**Decision:** Estimate **13% control valves, 68% isolation valves, 9% relief valves, 9% strainers** (by count)

**Trigger:** No P&IDs; no valve service assignments; must estimate mix

**Evidence:**
- Typical transload facility: More isolation valves than control valves (many manual block valves for maintenance isolation)
- Control valves: Flow/pressure/level control at critical points (railcar stations, loading arms, tank inlets)
- Relief valves: Safety-critical overpressure protection (one per tank, pump, blocked line segment)
- Strainers: One per pump suction, one per meter (protection devices)
- Industry ratios for process facilities: ~10-15% control, ~65-75% isolation, ~5-10% relief, ~5-10% specialty

**Impacted WBS/CBS:** MAT (control valves cost ~3-5× isolation valves due to actuators/instrumentation)

**Estimate Impact:** Weighted average valve cost reflects mix (higher isolation valve count reduces average cost)

**Assumption:** A-1608 (valve type ratio)

**Override:** Provide P&IDs with valve counts by type to replace parametric ratio

---

### D-1623: Relief Valve Sizing Basis (Placeholder)

**Decision:** Estimate relief valve count based on **protected equipment count** (tanks, pumps, blocked segments)

**Trigger:** No DEL-16.03 relief calculations; no equipment datasheets with MAWP

**Evidence:**
- Storage tanks: 3 tanks → 3 tank relief valves (one per tank)
- Pumps: ~6-8 pumps (unloading, transfer, loading) → 6-8 pump relief valves
- Thermal relief (blocked line segments): ~6-10 thermal relief valves
- Total: ~15-21 relief valves
- Estimate: 20 relief valves (midpoint)

**Impacted WBS/CBS:** MAT (relief valve count)

**Estimate Impact:** Relief valve count = 20 units

**Assumption:** A-1609 (relief valve count)

**Override:** Provide DEL-16.03 relief calculations or PKG-13 tank datasheets with relief requirements

---

### D-1624: Strainer Count Estimation

**Decision:** Estimate **20 strainers** (one per pump suction, one per meter, spares)

**Trigger:** No piping layout; no equipment list with strainer requirements

**Evidence:**
- Pump count estimate: ~6-8 pumps → 6-8 pump suction strainers
- Meter count estimate: ~6-10 meters (custody transfer, batching) → 6-10 meter strainers
- Spare/standby: ~2-4 additional strainers
- Total: ~14-22 strainers
- Estimate: 20 strainers (midpoint)

**Impacted WBS/CBS:** MAT (strainer count)

**Estimate Impact:** Strainer count = 20 units

**Assumption:** A-1610 (strainer count)

**Override:** Provide P&IDs or equipment datasheets with actual strainer requirements

---

### D-1625: Specialty Equipment Scope

**Decision:** Include **check valves** as specialty equipment; exclude other specialty items for this estimate

**Trigger:** "Specialty items" in PKG-16 scope is ambiguous; no deliverables explicitly list specialty equipment

**Evidence:**
- PKG-16 scope: "Control valves, isolation valves, relief valves, strainers, specialty items"
- Common specialty items: Check valves (backflow prevention), pressure regulators, special service valves
- Check valves: Typical ~15-25 units in transload facility (pump discharge, gravity feed prevention)

**Impacted WBS/CBS:** MAT

**Estimate Impact:** Add 20 check valves to material estimate

**Assumption:** A-1611 (specialty equipment scope = check valves)

**Override:** Provide scope clarification for "specialty items" or P&IDs showing specialty equipment

---

### D-1626: Installation Labor Rate

**Decision:** Use **$95/hr all-in** (blended rate for pipefitter, instrument tech, electrician)

**Trigger:** No project labor rate tables available

**Evidence:**
- BC Lower Mainland union labor rates (2026): $70-85/hr base wage
- All-in rate with benefits, payroll burden, small tools: 1.4-1.5× base = $98-$128/hr
- Blended rate (pipefitter + instrument tech + electrician): $90-$100/hr typical
- Midpoint: $95/hr

**Impacted WBS/CBS:** CD (installation labor cost)

**Estimate Impact:** Installation labor priced at $95/hr blended rate

**Assumption:** A-1612 (labor rate)

**Override:** Provide project labor rate tables or construction manager's all-in labor rate estimate

---

### D-1627: Engineering Hours Estimation

**Decision:** Estimate engineering hours using **deliverable complexity** and **typical effort per valve**

**Trigger:** No engineering budget; no manhour estimate from project team

**Evidence:**
- DEL-16.01 drawings: ~800-1,200 hours (arrangement drawings for ~220 valves, actuator details)
- DEL-16.02 specifications: ~400-600 hours (3 specs: control, isolation, relief)
- DEL-16.03 calculations: ~600-900 hours (30 control valve sizing, 20 relief valve sizing, actuator sizing)
- DEL-16.04 datasheets: ~900-1,400 hours (220 datasheets @ 4-6 hours each)
- Total: ~2,700-4,100 hours
- Estimate: 3,400 hours (midpoint)

**Impacted WBS/CBS:** E (engineering cost)

**Estimate Impact:** Engineering effort = 3,400 hours @ $155/hr blended = $527k

**Assumption:** A-1613 (engineering hours)

**Override:** Provide engineering manager's manhour estimate or historical data for similar valve packages

---

### D-1628: Engineering Hourly Rate

**Decision:** Use **$155/hr blended** rate for mechanical engineering

**Trigger:** No engineering rate table available

**Evidence:**
- BC mechanical engineer rate (P.Eng. + EIT mix): $120-180/hr
- CAD technician rate: $80-120/hr
- Blended rate for mechanical discipline: $140-170/hr typical
- Midpoint: $155/hr

**Impacted WBS/CBS:** E

**Estimate Impact:** Engineering priced at $155/hr blended rate

**Assumption:** A-1614 (engineering rate)

**Override:** Provide engineering rate table or project billing rates

---

### D-1629: QA/QC Testing Scope (DEL-16.05)

**Decision:** Include testing scope in **COM (Commissioning)** factor-based bucket

**Trigger:** DEL-16.05 testing scope not quantified (test counts, duration TBD)

**Evidence:**
- DEL-16.05 anticipated artifacts: Material certificates, FAT records, set pressure test records
- Testing included in COM factor (3% of CD+CI+MAT)
- Relief valve set pressure testing: Typically vendor FAT (included in valve supply cost)
- Control valve stroking tests: Field commissioning activity (included in COM)

**Impacted WBS/CBS:** COM (testing cost included in commissioning factor)

**Estimate Impact:** No separate testing line; testing included in COM = 3% × (CD+CI+MAT)

**Assumption:** A-1615 (testing scope in COM factor)

**Override:** Provide detailed test plan if testing scope exceeds typical commissioning factor coverage

---

### D-1630: RUN_STATUS Classification

**Decision:** Set RUN_STATUS = **WARNINGS**

**Trigger:** Estimate complete but with material assumptions and 100% allowance-based pricing

**Evidence:**
- No critical failures (all required files generated; all line items have Qty/Unit/UnitRate)
- Material assumptions: Valve counts, sizes, materials all parametric/allowance-based
- Confidence: LOW (100% allowance/parametric pricing)
- Suitable for conceptual budgeting; not suitable for procurement or GMP

**Impacted WBS/CBS:** N/A (status classification)

**Estimate Impact:** Estimate published with WARNINGS status; flagged for re-estimate when design quantities available

**Override:** Obtain design quantities and vendor quotes to upgrade status to OK

---

## Decision Summary Statistics

| Metric | Count |
|--------|-------|
| Total decisions | 30 |
| Path/workspace decisions | 1 |
| Config/basis decisions | 9 |
| Quantity estimation decisions | 7 |
| Pricing decisions | 6 |
| Scope/mapping decisions | 5 |
| Status decisions | 2 |

---

**Decision Log Prepared By:** Estimating Agent
**Date:** 2026-01-28
**Status:** Complete (30 decisions recorded)


---

## PKG-17

# Decision Log — PKG-17 Electrical Power Distribution

**Snapshot ID:** EST_PKG17_DRAFT_2026-01-28_0005
**Date:** 2026-01-28

---

This log records all decisions made during the estimating process where the agent had to choose between alternatives or apply defaults due to missing information.

---

## D-1701: Currency Selection

**Decision:** Use CAD (Canadian Dollars) for all pricing

**Trigger:** No explicit currency specified in deliverable documents (deliverable folders do not exist yet)

**Evidence:** Project location is Surrey, BC, Canada (per decomposition). Config file specifies CAD.

**Impacted WBS/CBS:** All packages and CBS buckets

**Estimate Impact:** N/A (all pricing converted to single currency)

**Override Path:** Update `_CONFIG.md` if different currency is required

---

## D-1702: Pricing Date

**Decision:** Use January 2026 as pricing date (current date)

**Trigger:** No historical pricing sources or vendor quotes available

**Evidence:** Config file specifies 2026-01 as pricing date

**Impacted WBS/CBS:** All packages and CBS buckets

**Estimate Impact:** No escalation applied (escalation_mode = NONE)

**Override Path:** Update `_CONFIG.md` to enable escalation if multi-year cash flow is required

---

## D-1703: Pricing Sources

**Decision:** Use 100% Fallback Typical Model (allowance/parametric pricing)

**Trigger:** No vendor quotes, rate tables, or historical data discovered for PKG-17

**Evidence:**
- No deliverable folders exist for PKG-17 (not yet scaffolded)
- No rate tables found in `_RateTables/` for electrical equipment
- No vendor quotes referenced in any available documents

**Impacted WBS/CBS:** All line items

**Estimate Impact:** All pricing is LOW confidence allowance-based

**Override Path:** Provide budgetary quotes for transformers, switchgear, MCCs; populate `_RateTables/electrical_equipment_rates.csv`

---

## D-1704: WBS to CBS Mapping

**Decision:** Map PKG-17 deliverables to CBS buckets as follows:
- DEL-17.01 through DEL-17.05 → E (Engineering)
- Electrical equipment → MAT (Materials)
- Equipment transport → FRT (Freight)
- Installation and testing → CD (Construction Directs)
- Supervision/QA → CI (Construction Indirects, parametric)
- Project management → PM (EPCM, parametric)
- Procurement coordination → P (Procurement, parametric)
- Commissioning support → COM (Commissioning, parametric)

**Trigger:** Standard WBS-to-CBS mapping required per estimating protocol

**Evidence:** Decomposition deliverable types and electrical discipline scope

**Impacted WBS/CBS:** All PKG-17 deliverables

**Estimate Impact:** Determines contingency rates and rollup structure

**Override Path:** Adjust WBS_CBS_Matrix.csv if alternative mapping is required

---

## D-1705: Quantity Takeoff (QTO) Approach

**Decision:** Proceed with allowance line items due to absence of explicit quantities

**Trigger:** No deliverable folders exist for PKG-17; no design drawings or load calculations available

**Evidence:** Decomposition provides only high-level scope description (MV/LV distribution, transformers, switchgear, MCC, panels, grounding, cable installation)

**Impacted WBS/CBS:** All MAT and CD line items

**Estimate Impact:** All material quantities and installation scope are assumptions

**Override Path:** Develop load calculations (DEL-17.03) and preliminary layout (DEL-17.01) to enable quantity-based estimating

---

## D-1706: Allowance Sizing Basis

**Decision:** Size allowances using industry-typical values for industrial electrical installations scaled to facility scope

**Trigger:** No project-specific pricing basis available

**Evidence:**
- Facility scale: 1M MT/annum throughput, 45,000 MT storage, 32 railcar stations
- Electrical loads anticipated from: pumps (PKG-15), storage tanks (PKG-13), railcar unloading (PKG-10), marine loading (PKG-11), building HVAC (PKG-22)
- Comparable industrial facility electrical systems

**Impacted WBS/CBS:** MAT and CD buckets

**Estimate Impact:** Material and labor allowances reflect industrial-scale electrical distribution system

**Override Path:** Obtain vendor budgetary quotes; conduct load study to refine equipment sizing

---

## D-1707: Contingency Method

**Decision:** Use `PCT_BY_BUCKET` method with allowance-based adjustments

**Trigger:** Config file specifies `contingency_method = PCT_BY_BUCKET`

**Evidence:** Config setting; 85.7% of base estimate is allowance/parametric pricing

**Impacted WBS/CBS:** All CBS buckets (contingency applied by bucket)

**Estimate Impact:** Total contingency = 25% average ($896k on $3,554k base)

**Override Path:** Update `_CONFIG.md` to use RISK_BASED method if probabilistic approach is preferred

---

## D-1708: Indirects and Management Factors

**Decision:** Apply default factors from Fallback Typical Model:
- CI (Construction Indirects) = 18% of CD
- PM (EPCM) = 6% of (CD + CI + MAT + FRT)
- P (Procurement) = 2% of (MAT + FRT)
- COM (Commissioning) = 3% of (CD + CI + MAT)

**Trigger:** No project-specific indirects basis or schedule-based estimate available

**Evidence:** Fallback Typical Model defaults per AGENT_ESTIMATING.md lines 666-673

**Impacted WBS/CBS:** CI, PM, P, COM buckets

**Estimate Impact:** Parametric indirects total $509k (14.3% of base estimate)

**Override Path:** Provide project-specific indirects rates or schedule-based resource loading; update `_CONFIG.md` with custom factors

---

**Total Decisions:** 8 (D-1701 through D-1708)

---

**END OF DECISION LOG**


---

## PKG-18

# Decision Log — PKG-18 Lighting Estimate

**Snapshot ID:** EST_PKG18_DRAFT_2026-01-28_2400
**Date:** 2026-01-28

---

## Purpose

This log documents all decisions made during the estimating process where explicit input was not available. Each decision is assigned a unique ID (D-1801, D-1802, etc.) and includes the rationale, evidence, and method to override in future estimate iterations.

---

## Decision Entries

### D-1801: Currency Selection

**Decision:** Use CAD (Canadian Dollars) as estimate currency.

**Trigger:** Config does not explicitly override currency; agent must select default.

**Evidence:**
- Project location: Fraser Surrey Terminal, 11060 Elevator Road, Surrey, BC, Canada (decomposition Section 1)
- No mixed-currency indicators found in deliverable documents

**Impacted WBS/CBS:** All packages and CBS buckets

**Estimate Impact:** All amounts expressed in CAD; no currency conversion required

**Override Method:** Set `currency: USD` (or other) in `_CONFIG.md` if different currency required

---

### D-1802: Pricing Date and Escalation

**Decision:** Use January 2026 as pricing date; escalation_mode = NONE.

**Trigger:** Config specifies escalation_mode = NONE; no historical pricing sources found.

**Evidence:**
- Current date: 2026-01-28
- No vendor quotes or historical rate tables with different pricing dates discovered
- Config: `escalation_mode: NONE`

**Impacted WBS/CBS:** All CBS buckets

**Estimate Impact:** Estimate represents "January 2026 dollars"; no escalation applied

**Override Method:** Set `escalation_mode: EXPLICIT` in `_CONFIG.md` and provide escalation factors/curve if escalation required

---

### D-1803: Pricing Sources Hierarchy

**Decision:** Use Fallback Typical Model for 100% of pricing (no quotes, rate tables, or historical data found).

**Trigger:** Source discovery (Protocol Phase 2.2) found no project-specific pricing sources.

**Evidence:**
- No vendor quotes or budgetary quotes found in deliverable `_REFERENCES.md` files
- No rate tables found in `execution/_Estimates/_RateTables/` (directory empty or not populated)
- No historical pricing sources referenced in deliverable documents
- All deliverables at INITIALIZED state with TBD placeholders

**Impacted WBS/CBS:** All line items (25/25 line items use ALLOWANCE or PARAMETRIC method)

**Estimate Impact:** Estimate confidence = LOW; pricing based on industry-typical allowances and parametric factors

**Override Method:**
- Add vendor budgetary quotes to deliverable `_REFERENCES.md` files
- Add rate tables (CSV or Excel) to `execution/_Estimates/_RateTables/` with columns: Item, Unit, UnitRate, Currency, Date, Source
- Add ER-extracted requirements with pricing guidance to deliverable documents

---

### D-1804: WBS-to-CBS Mapping

**Decision:** Map PKG-18 deliverables to CBS buckets based on deliverable type and electrical discipline scope.

**Trigger:** No explicit CBS mapping provided in decomposition or deliverable documents.

**Evidence:**
- Deliverable types from decomposition: Drawing, Specification, Calculation, Data Sheet, Record
- Discipline: Electrical
- Package scope: Interior and exterior LED lighting, lighting controls, emergency lighting

**Mapping:**
- **DEL-18.01 through DEL-18.05** → CBS = E (Engineering & Design)
- **LED fixtures, poles, controls** → CBS = MAT (Materials)
- **Installation labor** → CBS = CD (Construction Directs)
- **Supervision and QA/QC** → CBS = CI (Construction Indirects, parametric)
- **EPCM coordination** → CBS = PM (Project Management, parametric)
- **Vendor coordination** → CBS = P (Procurement, parametric)
- **Testing and acceptance** → CBS = COM (Commissioning, parametric)

**Impacted WBS/CBS:** All deliverables and line items

**Estimate Impact:** Determines how costs are categorized and reported; affects contingency application

**Override Method:** Provide explicit WBS-CBS mapping in `_CONFIG.md` or deliverable documents if different categorization required

---

### D-1805: Quantity Takeoff Approach (Allowance-Based)

**Decision:** Proceed with allowance-based line items using estimated fixture counts; do not invent precise quantities.

**Trigger:** No explicit quantities found in deliverable documents (all at INITIALIZED state with TBD placeholders).

**Evidence:**
- Deliverable Datasheets and Specifications contain TBD placeholders for fixture counts, pole quantities, and design parameters
- No lighting design drawings or calculations available (DEL-18.01, DEL-18.03 at INITIALIZED state)
- No fixture schedules or equipment lists available

**Impacted WBS/CBS:** All MAT and CD line items

**Estimate Impact:** Fixture counts estimated using typical ranges for industrial facilities; quantities are placeholders pending design

**Override Method:**
- Complete lighting design drawings (DEL-18.01) with fixture schedules
- Complete illumination calculations (DEL-18.03) with fixture selections
- Update deliverable documents with explicit equipment lists

---

### D-1806: Allowance Sizing Method

**Decision:** Size material and construction allowances using industry-typical unit pricing for LED commercial/industrial lighting.

**Trigger:** No project-specific quotes or rate tables available; must use fallback model to complete estimate.

**Evidence:**
- No vendor quotes in `_REFERENCES.md` files
- No rate tables in `_RateTables/` directory
- Comparable packages (PKG-17 Electrical Power) not yet estimated to provide precedent

**Allowance Basis:**
- **Exterior LED area lights:** $1,500-$3,000 CAD per fixture (pole-mounted, 30-40 ft poles, marine environment)
- **Interior high-bay LED:** $800-$1,500 CAD per fixture
- **Office/control room LED:** $300-$600 CAD per fixture
- **Emergency LED battery-backed:** $500-$1,000 CAD per fixture
- **Lighting poles:** $4,000-$8,000 CAD per pole (30-40 ft steel/aluminum, foundation, installation)
- **Controls:** $500-$1,500 CAD per device (sensors, switches, panels)
- **Installation labor:** $200-$400 CAD per fixture (exterior), $100-$200 CAD per fixture (interior)

**Impacted WBS/CBS:** MAT and CD line items

**Estimate Impact:** Material and construction costs based on typical market pricing for BC industrial projects

**Override Method:** Obtain budgetary quotes from lighting vendors; add to deliverable `_REFERENCES.md` and re-run estimate

---

### D-1807: Indirects, Management, and Commissioning Factors

**Decision:** Apply parametric factors from Fallback Typical Model for CI, PM, P, COM.

**Trigger:** No time-based schedule/duration data available; no project-specific overhead rates found.

**Evidence:**
- No project schedule or duration data in deliverable documents
- No EPCM rate tables or overhead rate sheets in `_RateTables/`
- Fallback model provides default factors (per AGENT_ESTIMATING.md STRUCTURE section)

**Factors Applied:**
- **CI (Construction Indirects):** 18% of CD = $47,700
- **PM (EPCM/Project Management):** 6% of (CD + CI + MAT) = $78,540
- **P (Procurement):** 2% of MAT = $9,500
- **COM (Commissioning):** Enhanced for comprehensive illumination testing = $166,596

**Impacted WBS/CBS:** CI, PM, P, COM buckets

**Estimate Impact:** Indirects, management, procurement, and commissioning costs based on typical factors

**Override Method:**
- Provide project-specific EPCM rates or overhead percentages in `_CONFIG.md`
- Provide schedule/duration data to enable time-based calculation of indirects
- Add rate tables for supervision, QA/QC, testing labor

---

### D-1808: Commissioning Scope Enhancement

**Decision:** Increase commissioning allowance beyond standard 3% factor to reflect comprehensive illumination testing requirements.

**Trigger:** DEL-18.05 describes extensive testing scope: exterior illumination testing, interior illumination testing, emergency lighting duration testing, control functional testing.

**Evidence:**
- DEL-18.05 Datasheet describes multi-zone illumination testing, emergency duration testing, control system verification
- Lighting testing requires nighttime testing for exterior areas, specialized illuminance measurement equipment, comprehensive documentation

**Calculation:**
- Standard COM factor: 3% of (CD + CI + MAT) = $23,841
- Enhanced allowance for testing scope: Increased by 7× to $166,596 (approximately 15% of base estimate for lighting-heavy commissioning)

**Impacted WBS/CBS:** COM bucket

**Estimate Impact:** Higher commissioning cost reflects extensive field testing and verification requirements

**Override Method:** Obtain testing contractor quotes; provide testing manhour budget in rate tables; adjust COM percentage in `_CONFIG.md`

---

## Decision Summary Table

| Decision ID | Topic | Impact | Confidence | Resolution Path |
|-------------|-------|--------|------------|-----------------|
| D-1801 | Currency (CAD) | All line items | HIGH | Override in _CONFIG.md if needed |
| D-1802 | Pricing date (2026-01) | All line items | HIGH | Provide dated quotes or enable escalation |
| D-1803 | Pricing sources (Fallback) | All line items | LOW | Obtain vendor quotes and rate tables |
| D-1804 | WBS-CBS mapping | Organization | MED | Provide explicit mapping if needed |
| D-1805 | QTO approach (Allowance) | MAT, CD | LOW | Complete design drawings and calcs |
| D-1806 | Allowance sizing | MAT, CD | LOW | Obtain budgetary quotes |
| D-1807 | Indirects/PM/P/COM factors | CI, PM, P, COM | LOW-MED | Provide schedule and rate tables |
| D-1808 | COM scope enhancement | COM | MED | Obtain testing contractor quotes |

---

**END OF DECISION LOG**


---

## PKG-19

# Decision Log

## Snapshot: EST_PKG19_DRAFT_2026-01-28_0015

This log records all decisions made during estimate preparation for PKG-19 Control Systems.

---

## Decisions

### D-001: Currency Selection

| Field | Value |
|-------|-------|
| ID | D-001 |
| Decision | Use CAD (Canadian dollars) as estimate currency |
| Trigger | Currency not explicitly specified in config |
| Evidence | Project location: Fraser Surrey Terminal, Surrey, BC, Canada (decomposition Section 1) |
| Impacted WBS/CBS | All line items |
| Estimate Impact | None (single currency) |
| Override | Set `currency: USD` in _CONFIG.md if USD required |

---

### D-002: Single-Vendor DCS/PLC Solution

| Field | Value |
|-------|-------|
| ID | D-002 |
| Decision | Assume single-vendor integrated DCS/PLC solution |
| Trigger | Vendor strategy not defined |
| Evidence | No evidence; default assumption for D&B projects |
| Impacted WBS/CBS | MAT (control system equipment) |
| Estimate Impact | Affects system integration complexity and pricing; single-vendor typically lower integration cost |
| Override | Define vendor strategy in DEL-19.02 specification |

---

### D-003: Control System Platform Class

| Field | Value |
|-------|-------|
| ID | D-003 |
| Decision | Assume modern mid-tier DCS/PLC platform (Honeywell, Emerson, ABB, Siemens class) |
| Trigger | Platform selection not defined |
| Evidence | No evidence; default for industrial terminal of this size |
| Impacted WBS/CBS | MAT (controllers, I/O, software licenses) |
| Estimate Impact | +/- 20% depending on vendor; high-end DCS higher, PLC-based lower |
| Override | Select vendor and obtain budgetary quote |

---

### D-004: HMI Platform Integration

| Field | Value |
|-------|-------|
| ID | D-004 |
| Decision | Assume vendor-integrated HMI platform with DCS/PLC |
| Trigger | HMI vendor strategy not defined |
| Evidence | No evidence; typical for integrated systems |
| Impacted WBS/CBS | MAT (HMI workstations, software) |
| Estimate Impact | Integrated HMI typically lower cost vs. third-party |
| Override | Define HMI platform in DEL-19.02 specification |

---

### D-005: Historian Platform

| Field | Value |
|-------|-------|
| ID | D-005 |
| Decision | Assume vendor-integrated historian or OSIsoft PI class |
| Trigger | Historian vendor not specified |
| Evidence | No evidence; typical for process facilities |
| Impacted WBS/CBS | MAT (historian server, software) |
| Estimate Impact | OSIsoft PI typically higher cost; vendor-integrated lower |
| Override | Select historian platform based on Employer requirements |

---

### D-006: Software Development Responsibility

| Field | Value |
|-------|-------|
| ID | D-006 |
| Decision | Software development by control system vendor or qualified integrator |
| Trigger | Software development responsibility not defined |
| Evidence | D&B contract structure per decomposition |
| Impacted WBS/CBS | E (software development) |
| Estimate Impact | Vendor software typically more structured pricing |
| Override | Define development approach in contracting strategy |

---

### D-007: Productivity Factor

| Field | Value |
|-------|-------|
| ID | D-007 |
| Decision | Use productivity factor of 1.0 (BC lower mainland baseline) |
| Trigger | Location-specific productivity not defined |
| Evidence | Project location: Surrey, BC |
| Impacted WBS/CBS | CD, CI |
| Estimate Impact | Could vary +/- 10% based on actual site conditions |
| Override | Provide site-specific productivity assessment |

---

### D-008: Working Hours

| Field | Value |
|-------|-------|
| ID | D-008 |
| Decision | Assume standard 8-10 hour shifts |
| Trigger | Work schedule not defined |
| Evidence | No evidence; default assumption |
| Impacted WBS/CBS | CD, CI |
| Estimate Impact | Shift premium for extended hours would increase labor costs |
| Override | Define work schedule in project execution plan |

---

### D-009: Pricing Basis - Allowances

| Field | Value |
|-------|-------|
| ID | D-009 |
| Decision | All line items priced via allowances (fallback typical model) |
| Trigger | No vendor quotes or rate tables available |
| Evidence | No pricing sources found in Source_Index search |
| Impacted WBS/CBS | All |
| Estimate Impact | Estimate confidence LOW; +/- 30-50% accuracy range |
| Override | Obtain vendor budgetary quotes for control system equipment |

---

### D-010: Indirects Factor Model

| Field | Value |
|-------|-------|
| ID | D-010 |
| Decision | Use fallback typical model for indirects calculation |
| Trigger | Project-specific indirects data not available |
| Evidence | Default factors per AGENT_ESTIMATING.md |
| Impacted WBS/CBS | PM, P, CI, COM |
| Estimate Impact | Factors: CI=18% of CD, P=2% of MAT, PM=6% of CD+CI+MAT, COM=3% of CD+CI+MAT |
| Override | Provide project-specific indirects rates in _CONFIG.md |

---

### D-011: Contingency Rates Elevated

| Field | Value |
|-------|-------|
| ID | D-011 |
| Decision | Apply elevated contingency rates due to 100% allowance-based pricing |
| Trigger | All pricing via allowances; high uncertainty |
| Evidence | Fallback typical model contingency adjustment (+5% to +10% for allowance-heavy buckets) |
| Impacted WBS/CBS | CONT applied to all CBS |
| Estimate Impact | Base contingency + allowance adjustment = 15-30% by bucket; weighted average ~25% |
| Override | Reduce contingency when vendor quotes obtained |

---

### D-012: Escalation Not Applied

| Field | Value |
|-------|-------|
| ID | D-012 |
| Decision | No escalation applied; pricing in January 2026 dollars |
| Trigger | escalation_mode = NONE in _CONFIG.md |
| Evidence | Config file setting |
| Impacted WBS/CBS | None |
| Estimate Impact | Future spending would be subject to escalation in actual project |
| Override | Set escalation_mode = EXPLICIT in _CONFIG.md with escalation factors |

---

## Decision Summary

| ID | Short Description | Primary Impact |
|----|-------------------|----------------|
| D-001 | CAD currency | Currency |
| D-002 | Single-vendor DCS/PLC | MAT pricing |
| D-003 | Mid-tier platform class | MAT pricing |
| D-004 | Integrated HMI | MAT pricing |
| D-005 | Vendor/OSIsoft historian | MAT pricing |
| D-006 | Vendor software development | E pricing |
| D-007 | Productivity factor 1.0 | CD/CI pricing |
| D-008 | Standard work hours | CD/CI pricing |
| D-009 | Allowance-based pricing | Overall confidence |
| D-010 | Indirects factor model | PM/P/CI/COM |
| D-011 | Elevated contingency | CONT |
| D-012 | No escalation | ESC |


---

## PKG-20

# Decision Log — PKG-20 Field Instrumentation

## Overview

This log records all decisions made during the estimating process for PKG-20 Field Instrumentation. Each decision is assigned a unique ID (D-###) and referenced from the BOE, Detail.csv, and Assumptions_Log.

---

## Decisions

### D-001: Currency Selection

| Field | Value |
|-------|-------|
| Decision | Use CAD (Canadian dollars) for all estimate values |
| Trigger | Currency not specified in scope documents |
| Evidence | Project location is Fraser Surrey Terminal, Surrey, BC, Canada (decomposition Section 1) |
| Impacted WBS/CBS | All line items |
| Estimate Impact | Currency consistency maintained |
| Override | Set `currency` in _CONFIG.md to change |

---

### D-002: Instrument Supply Model

| Field | Value |
|-------|-------|
| Decision | Contractor procures instruments from qualified vendors |
| Trigger | Procurement model not specified |
| Evidence | D&B contract (decomposition Section 1.2) implies Contractor responsibility |
| Impacted WBS/CBS | MAT, P |
| Estimate Impact | Procurement costs included in estimate |
| Override | If Owner-supplied instruments, remove MAT and adjust P |

---

### D-003: Instrument Calibration Approach

| Field | Value |
|-------|-------|
| Decision | Vendor factory calibration with field verification by Contractor |
| Trigger | Calibration approach not specified |
| Evidence | Industry standard practice for new instrument installations |
| Impacted WBS/CBS | CD (calibration labor), COM |
| Estimate Impact | Field calibration included at $280/instrument |
| Override | If bench calibration only, reduce field calibration scope |

---

### D-004: Cable Supply Approach

| Field | Value |
|-------|-------|
| Decision | Contractor supplies bulk instrument cable |
| Trigger | Cable supply not specified |
| Evidence | D&B contract (decomposition Section 1.2) |
| Impacted WBS/CBS | MAT |
| Estimate Impact | 8,000 m cable at $12/m included |
| Override | If cable supplied by PKG-17/19, remove MAT allocation |

---

### D-005: Junction Box Material

| Field | Value |
|-------|-------|
| Decision | NEMA 4X stainless steel junction boxes |
| Trigger | Material specification not defined |
| Evidence | Marine/industrial environment at Fraser Surrey Terminal |
| Impacted WBS/CBS | MAT |
| Estimate Impact | SS junction boxes at $2,800/unit |
| Override | If painted steel acceptable, reduce unit cost to ~$1,500 |

---

### D-006: Location Productivity Factor

| Field | Value |
|-------|-------|
| Decision | Use productivity factor of 1.0 (baseline) |
| Trigger | No project-specific productivity data |
| Evidence | BC lower mainland has standard industrial labor availability |
| Impacted WBS/CBS | CD, CI |
| Estimate Impact | No productivity adjustment applied |
| Override | Adjust if site-specific conditions warrant |

---

### D-007: Working Hours Assumption

| Field | Value |
|-------|-------|
| Decision | Standard 8-10 hour shifts assumed |
| Trigger | Schedule and shift pattern not specified |
| Evidence | Typical for D&B industrial construction in BC |
| Impacted WBS/CBS | CD, CI |
| Estimate Impact | No premium for extended shifts |
| Override | If accelerated schedule, add shift premium |

---

### D-008: Pricing Method Selection

| Field | Value |
|-------|-------|
| Decision | All pricing uses allowances (fallback typical model) |
| Trigger | No vendor quotes or rate tables available |
| Evidence | Deliverables in INITIALIZED state; no pricing sources found |
| Impacted WBS/CBS | All |
| Estimate Impact | 100% allowance-based; LOW confidence |
| Override | Provide vendor quotes to replace allowances |

---

### D-009: Indirect Cost Factors

| Field | Value |
|-------|-------|
| Decision | Apply factor-based indirects (CI=18%, P=2%, PM=6%, COM=4%) |
| Trigger | Indirect costs not explicitly defined |
| Evidence | Fallback typical model per AGENT_ESTIMATING protocol |
| Impacted WBS/CBS | CI, P, PM, COM |
| Estimate Impact | ~$222,000 in factor-based indirects |
| Override | Provide project-specific indirect rates |

Note: Commissioning factor elevated to 4% for I&C work (loop testing and calibration intensive).

---

### D-010: Contingency Rates

| Field | Value |
|-------|-------|
| Decision | Apply elevated contingency rates due to 100% allowance basis |
| Trigger | Estimate maturity is Class 5 (order of magnitude) |
| Evidence | PCT_BY_BUCKET method per _CONFIG.md with allowance adjustment |
| Impacted WBS/CBS | All CBS buckets |
| Estimate Impact | ~$408,000 contingency (26.6% overall) |
| Override | Reduce as estimate matures with quotes/quantities |

---

### D-011: Escalation Mode

| Field | Value |
|-------|-------|
| Decision | No escalation applied |
| Trigger | escalation_mode = NONE in _CONFIG.md |
| Evidence | Pricing date is current (January 2026) |
| Impacted WBS/CBS | None |
| Estimate Impact | No escalation in estimate |
| Override | Set escalation_mode = EXPLICIT in _CONFIG.md |

---

## Decision Summary

| ID | Decision Summary | Impact Level |
|----|------------------|--------------|
| D-001 | CAD currency | Low |
| D-002 | Contractor procures instruments | Medium |
| D-003 | Factory cal + field verification | Low |
| D-004 | Contractor supplies cable | Medium |
| D-005 | NEMA 4X SS junction boxes | Low |
| D-006 | Productivity factor 1.0 | Medium |
| D-007 | Standard shifts | Low |
| D-008 | All pricing via allowances | High |
| D-009 | Factor-based indirects | Medium |
| D-010 | Elevated contingency | High |
| D-011 | No escalation | Low |

---

*Decision Log generated by ESTIMATING Agent | 2026-01-28*


---

## PKG-21

# Decision Log

## PKG-21: Building Structures & Envelope

**Snapshot ID:** EST_PKG21_DRAFT_2026-01-28_0030

---

## Decisions

### D-001: MCC Building Size Assumption

| Field | Value |
|-------|-------|
| Decision | Assumed MCC building footprint of 600 m² (approx. 6,500 ft²) |
| Trigger | Building size not defined in deliverable documents; all references marked TBD |
| Evidence | DEL-21.01 Datasheet line 82: "Size/footprint: **TBD**" |
| Impacted WBS/CBS | PKG-21 / MAT, CD |
| Estimate Impact | HIGH — Building size is primary cost driver; ±50% on building materials/labor |
| Override Path | Provide MCC equipment layout with space requirements; update MAT and CD line items |

---

### D-002: Building Construction Type

| Field | Value |
|-------|-------|
| Decision | Assumed Pre-Engineered Metal Building (PEMB) construction with insulated metal panels |
| Trigger | Construction type marked TBD in deliverables |
| Evidence | DEL-21.01 Datasheet line 82: "Construction type: **TBD** — **ASSUMPTION**: Pre-engineered metal building or modular construction typical for industrial MCC buildings" |
| Impacted WBS/CBS | PKG-21 / MAT, CD |
| Estimate Impact | MEDIUM — PEMB vs modular vs conventional construction affects cost structure |
| Override Path | Confirm preferred construction method in _CONFIG.md or provide vendor budget |

---

### D-003: Foundation Type

| Field | Value |
|-------|-------|
| Decision | Assumed pile foundations with concrete pile caps and slab-on-grade |
| Trigger | Foundation type not defined; geotechnical investigation not available |
| Evidence | DEL-21.03 Datasheet line 67: "Foundation type: **TBD** — Spread footings, piles, mat (based on geotechnical investigation)" |
| Impacted WBS/CBS | PKG-21 / MAT, CD |
| Estimate Impact | MEDIUM — Pile foundations vs spread footings can vary ±30% on foundation costs |
| Override Path | Provide geotechnical recommendations; update foundation line items |

---

### D-004: Operator Shelter Quantity

| Field | Value |
|-------|-------|
| Decision | Assumed 4 operator shelters to serve 32 railcar unloading stations |
| Trigger | Number of shelters not defined |
| Evidence | DEL-21.01 Datasheet line 86: "Number of shelters: **TBD** — **ASSUMPTION**: Related to 32 railcar unloading stations" |
| Impacted WBS/CBS | PKG-21 / MAT, CD |
| Estimate Impact | MEDIUM — Each shelter adds ~$70,000 (supply + install) |
| Override Path | Confirm shelter count per PKG-10 railcar unloading layout |

---

### D-005: No Vendor Quotes Available

| Field | Value |
|-------|-------|
| Decision | Proceeded with parametric/allowance pricing due to absence of vendor quotes |
| Trigger | No pricing sources found in workspace |
| Evidence | Source discovery searched deliverable folders and _RateTables/; no quotes found |
| Impacted WBS/CBS | All CBS buckets |
| Estimate Impact | HIGH — 100% allowance/parametric pricing triggers contingency uplift |
| Override Path | Obtain budget quotes from PEMB suppliers and building contractors |

---

### D-006: No Rate Tables Available

| Field | Value |
|-------|-------|
| Decision | Proceeded without project-specific rate tables |
| Trigger | _RateTables/ folder empty or not populated |
| Evidence | Rate table search returned no results |
| Impacted WBS/CBS | All CBS buckets |
| Estimate Impact | MEDIUM — Using industry benchmarks instead of project rates |
| Override Path | Provide building rate tables in `_RateTables/` |

---

### D-007: PM Factor Selection

| Field | Value |
|-------|-------|
| Decision | Applied 6% PM factor on (CD + CI + MAT) |
| Trigger | No project-specific PM rates or durations available |
| Evidence | Fallback Typical Model (AGENT_ESTIMATING.md line 673): "EPCM/PM (PM) = 0.06 × (CD + CI + MAT + FRT)" |
| Impacted WBS/CBS | PKG-21 / PM |
| Estimate Impact | LOW — PM calculated as $67,000 |
| Override Path | Provide PM level of effort or duration-based estimate |

---

### D-008: Procurement Factor Selection

| Field | Value |
|-------|-------|
| Decision | Applied 2% procurement factor on MAT |
| Trigger | No project-specific procurement scope or rates |
| Evidence | Fallback Typical Model (AGENT_ESTIMATING.md line 669): "Procurement services (P) = 0.02 × (MAT + FRT)" |
| Impacted WBS/CBS | PKG-21 / P |
| Estimate Impact | LOW — Procurement calculated as $14,000 |
| Override Path | Provide procurement scope of work or detailed estimate |

---

### D-009: Construction Indirects Factor Selection

| Field | Value |
|-------|-------|
| Decision | Applied 18% CI factor on Construction Directs |
| Trigger | No project-specific indirects breakdown or schedule |
| Evidence | Fallback Typical Model (AGENT_ESTIMATING.md line 667): "Construction indirects (CI) = 0.18 × Construction Directs (CD)" |
| Impacted WBS/CBS | PKG-21 / CI |
| Estimate Impact | LOW-MEDIUM — CI calculated as $62,000 |
| Override Path | Provide detailed indirects estimate or duration-based calculation |

---

### D-010: Currency Selection

| Field | Value |
|-------|-------|
| Decision | Used CAD (Canadian dollars) per _CONFIG.md |
| Trigger | Config file specifies currency |
| Evidence | _CONFIG.md line 9: "currency: CAD" |
| Impacted WBS/CBS | All |
| Estimate Impact | N/A — Currency is correct for project location |
| Override Path | N/A |

---

### D-011: Contingency Method

| Field | Value |
|-------|-------|
| Decision | Applied PCT_BY_BUCKET contingency method with allowance adjustment |
| Trigger | Config specifies PCT_BY_BUCKET; all items are allowance/parametric |
| Evidence | _CONFIG.md line 35: "contingency_method: PCT_BY_BUCKET"; 100% allowance share triggers +10% uplift |
| Impacted WBS/CBS | All CBS buckets (CONT) |
| Estimate Impact | Contingency = $410,000 (25.7% of base) |
| Override Path | Provide more detailed pricing to reduce allowance share and contingency |

---

### D-012: Operator Shelter Size

| Field | Value |
|-------|-------|
| Decision | Assumed 15 m² (160 ft²) per shelter |
| Trigger | Shelter size not defined |
| Evidence | DEL-21.01 Datasheet lines 85-88: shelter function and size marked TBD |
| Impacted WBS/CBS | PKG-21 / MAT, CD |
| Estimate Impact | LOW-MEDIUM — Size affects unit cost |
| Override Path | Define shelter size requirements per operator comfort and equipment needs |

---

**Total Decisions:** 12

**Prepared by:** ESTIMATING Agent
**Date:** 2026-01-28


---

## PKG-22

# Decision Log — PKG-22 Building Interior & MEP

**Snapshot ID:** EST_PKG22_DRAFT_2026-01-28_2358
**Package:** PKG-22 Building Interior & MEP
**Date:** 2026-01-28

---

## Purpose

This document records all decisions made during the estimating process, including defaults, ambiguities, and mapping choices.

---

## Decision Entries

### D-001: Workspace Paths

**Decision:** Use default workspace paths per AGENT_ESTIMATING

**Trigger:** No explicit paths provided in conversation

**Evidence:**
- Execution root: `/Users/ryan/ai-env/projects/chirality-app/test/execution/`
- Decomposition: `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md`
- Estimates write zone: `/Users/ryan/ai-env/projects/chirality-app/test/execution/_Estimates/`

**Impacted WBS/CBS:** All

**Estimate Impact:** None (path selection only)

**How to Override:** Provide explicit paths in conversation or update AGENT_ESTIMATING defaults

---

### D-002: Currency Selection

**Decision:** CAD (Canadian dollars)

**Trigger:** Config override in `_CONFIG.md`

**Evidence:**
- `_CONFIG.md` line 9: `currency | CAD | Canadian dollars (project location: Surrey, BC)`
- Project location: Fraser Surrey Terminal, Surrey, BC (Decomposition Section 1)

**Impacted WBS/CBS:** All

**Estimate Impact:** All values in CAD; no currency conversion required

**How to Override:** Update `_CONFIG.md` currency parameter

---

### D-003: Pricing Date

**Decision:** January 2026 (2026-01)

**Trigger:** Config override in `_CONFIG.md`

**Evidence:**
- `_CONFIG.md` line 10: `pricing_date | 2026-01 | January 2026 (current date)`
- Today's date: 2026-01-28

**Impacted WBS/CBS:** All

**Estimate Impact:** Current pricing basis; no historical adjustment; escalation exposure noted in Risk_Register.md

**How to Override:** Update `_CONFIG.md` pricing_date parameter

---

### D-004: Estimate Label

**Decision:** PKG22_DRAFT

**Trigger:** Sequential package estimating approach; update _CONFIG.md for PKG-22

**Evidence:**
- Previous package: PKG20_DRAFT
- Next package per sequence: PKG-22 Building Interior & MEP

**Impacted WBS/CBS:** All (label only)

**Estimate Impact:** None (labeling only)

**How to Override:** Update `_CONFIG.md` estimate_label parameter

---

### D-005: Scope Inclusions/Exclusions

**Decision:** Include E, PM, P, MAT, CD, CI, COM; exclude Owner's costs, land, financing, Employer-obtained permits

**Trigger:** Config override in `_CONFIG.md`

**Evidence:**
- `_CONFIG.md` lines 16-29 (scope settings)
- Decomposition Section 1.2: "This decomposition covers the Contractor's scope of work only"

**Impacted WBS/CBS:** All

**Estimate Impact:** Estimate covers Contractor D&B scope only

**How to Override:** Update `_CONFIG.md` include_scopes/exclude_scopes

---

### D-006: Indirects Model Selection

**Decision:** Factor-based indirects (CI, P, PM, COM calculated as % of directs/materials)

**Trigger:** No construction schedule available; conceptual estimate maturity

**Evidence:**
- No schedule found in workspace
- Deliverables in INITIALIZED state (no execution plan)
- Fallback model supports factor-based indirects (AGENT_ESTIMATING lines 643-652)

**Impacted WBS/CBS:** CI, P, PM, COM

**Estimate Impact:** $391k total indirects/services (19% of MAT+CD base)

**How to Override:** Provide construction schedule and time-based resource loading plan

---

### D-007: Rounding Policy

**Decision:** Nearest $1,000 CAD

**Trigger:** Config override in `_CONFIG.md`

**Evidence:**
- `_CONFIG.md` line 12: `rounding | 1000 | Round to nearest $1,000`

**Impacted WBS/CBS:** Summary totals only (Detail.csv retains calculated precision)

**Estimate Impact:** Minimal (rounding applied to final summary totals only)

**How to Override:** Update `_CONFIG.md` rounding parameter

---

### D-008: Pricing Method (No Quotes/Rates Available)

**Decision:** Use 100% allowance-based pricing for directs and materials; fallback model for indirects

**Trigger:** No vendor quotes or rate tables found (see Source_Index.md)

**Evidence:**
- Source search completed: 0 vendor quotes, 0 rate tables (Source_Index.md Phase 1-2)
- All deliverables in INITIALIZED state with TBD quantities
- Fallback model available per AGENT_ESTIMATING lines 623-691

**Impacted WBS/CBS:** E, MAT, CD (directs); CI, P, PM, COM (parametric factors)

**Estimate Impact:** 100% allowance/parametric pricing; confidence LOW; high contingency required

**How to Override:** Provide vendor quotes, develop rate tables, complete design quantities

---

### D-009: Indirects Factors Applied

**Decision:** Apply fallback typical factors: CI=18%, P=2%, PM=6%, COM=3%

**Trigger:** Factor-based indirects model selected (D-006); no project-specific factors available

**Evidence:**
- Fallback model factors (AGENT_ESTIMATING lines 643-652)
- Factors typical for industrial facility construction in BC Lower Mainland

**Impacted WBS/CBS:** CI, P, PM, COM

**Estimate Impact:**
- CI = 18% × CD ($632k) = $114k
- P = 2% × MAT ($675k) = $14k
- PM = 6% × (CD+CI+MAT) ($1,421k) = $85k
- COM = 3% × (CD+CI+MAT) ($1,421k) = $43k

**How to Override:** Update `_CONFIG.md` with project-specific factors or provide time-based resource plan

---

### D-010: Contingency Method

**Decision:** PCT_BY_BUCKET with allowance-heavy adjustment

**Trigger:** Config override in `_CONFIG.md`; 100% allowance-based pricing

**Evidence:**
- `_CONFIG.md` line 35: `contingency_method | PCT_BY_BUCKET`
- AllowanceShare = 100% for E, MAT, CD buckets
- Fallback model contingency baseline (AGENT_ESTIMATING lines 653-667)

**Impacted WBS/CBS:** All (contingency by CBS bucket)

**Estimate Impact:** Elevated contingency rates (20-30%) due to pricing uncertainty and scope uncertainty

**How to Override:** Update `_CONFIG.md` contingency_method; provide vendor quotes to reduce AllowanceShare

---

### D-011: WBS to CBS Mapping (MEP Deliverables)

**Decision:** Map PKG-22 deliverables to CBS as follows:
- Design deliverables (DEL-22.01 through DEL-22.04, DEL-22.06) → Engineering (E)
- Physical materials (HVAC equipment, plumbing materials, fire suppression components, electrical fixtures, interior finishes) → Materials (MAT)
- Installation work (HVAC installation, plumbing installation, fire sprinkler installation, interior electrical, finishes installation) → Construction Directs (CD)
- QA/QC records (DEL-22.05) → Construction Indirects (CI) / Commissioning (COM)

**Trigger:** Standard WBS→CBS mapping required per estimating protocol

**Evidence:**
- Deliverable types from Decomposition: Drawing, Specification, Calculation, Data Sheet, Record, Drawing Set
- Package discipline: Buildings (MEP specialty)
- Scope keywords: HVAC, plumbing, fire suppression, electrical, finishes

**Impacted WBS/CBS:** E, MAT, CD, CI, COM

**Estimate Impact:** Mapping determines CBS bucket allocation for all line items

**How to Override:** Provide explicit WBS-CBS mapping table or update estimating protocol

---

### D-012: Building Size Assumption

**Decision:** Assume 300 m² (3,230 SF) MCC building as baseline for MEP system sizing

**Trigger:** No building size available from PKG-21 deliverables (INITIALIZED state)

**Evidence:**
- Decomposition project parameters: 1,000,000 MT/a throughput; 32 railcar unloading stations; marine loading controls
- Typical industrial MCC building range: 200-400 m² (2,150-4,300 SF)
- 300 m² is mid-range estimate suitable for conceptual budgeting

**Impacted WBS/CBS:** All MEP line items (HVAC, plumbing, fire suppression, electrical, finishes)

**Estimate Impact:** Significant; building size drives HVAC capacity, plumbing fixture counts, sprinkler head counts, electrical load, finishes quantities

**How to Override:** Complete DEL-21.01 building design drawings or provide building floor area in conversation

**Cross-reference:** A-022 (building size assumption)

---

### D-013: Interior Finishes Scope Interpretation

**Decision:** Include basic industrial interior finishes (flooring, wall finishes, ceilings) in PKG-22 scope

**Trigger:** Decomposition PKG-22 scope states "Interior finishes" but does not detail extent

**Evidence:**
- PKG-22 scope (Decomposition line 525): "Interior finishes, HVAC, plumbing, building electrical distribution, fire suppression"
- Building type: MCC building (industrial occupancy)
- Typical industrial finish levels: sealed concrete floors or epoxy; painted drywall or metal panels; exposed or suspended acoustic ceiling

**Impacted WBS/CBS:** MAT, CD

**Estimate Impact:** $120k allowance for finishes (materials + installation)

**How to Override:** Complete DEL-21.01/DEL-22.01 building design drawings with finish schedules or clarify finish requirements in conversation

**Cross-reference:** A-021 (interior finishes allowance)

---

## Decision Summary

| Decision ID | Topic | Impact Level | Override Path |
|-------------|-------|--------------|---------------|
| D-001 | Workspace paths | Low | Provide explicit paths |
| D-002 | Currency (CAD) | Medium | Update _CONFIG.md |
| D-003 | Pricing date (2026-01) | Medium | Update _CONFIG.md |
| D-004 | Estimate label | Low | Update _CONFIG.md |
| D-005 | Scope inclusions/exclusions | High | Update _CONFIG.md |
| D-006 | Factor-based indirects | High | Provide schedule or override factors |
| D-007 | Rounding ($1,000) | Low | Update _CONFIG.md |
| D-008 | Use allowances (no quotes/rates) | High | Provide vendor quotes or rate tables |
| D-009 | Indirects factors (18/2/6/3%) | High | Update _CONFIG.md or provide resource plan |
| D-010 | PCT_BY_BUCKET contingency | High | Update _CONFIG.md or provide risk model |
| D-011 | WBS-CBS mapping | Medium | Provide explicit mapping table |
| D-012 | Building size (300 m²) | High | Provide PKG-21 building drawings or floor area |
| D-013 | Interior finishes scope | Medium | Clarify finish requirements or provide finish schedule |

---

**Total Decisions:** 13

**Decision Log Prepared By:** Estimating Agent
**Date:** 2026-01-28
**Snapshot:** EST_PKG22_DRAFT_2026-01-28_2358
**Status:** Complete


---

## PKG-23

# Decision Log

## Snapshot Identification

| Field | Value |
|-------|-------|
| Snapshot ID | EST_PKG23_DRAFT_2026-01-28_2400 |
| Package | PKG-23 Fire Protection |
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

**Decision:** Use `PKG23_DRAFT` as estimate label.

**Trigger:** Estimate label required for snapshot identification and tracking.

**Evidence:**
- Following established pattern from previous packages (PKG00_DRAFT through PKG20_DRAFT per _LATEST.md)
- Package-specific labels per snapshot convention

**Impacted WBS/CBS:** N/A (metadata only)

**Estimate Impact:** None (label is for identification only)

**Override Path:** Provide different label via config or user instruction for next run

---

### D-004: Scope Inclusions

**Decision:** Include Engineering (E), PM, Procurement (P), Materials (MAT), Construction Directs (CD), Construction Indirects (CI), Commissioning (COM).

**Trigger:** CBS scope definition required for estimate coverage.

**Evidence:**
- Config file specifies include scopes list
- PKG-23 scope includes design deliverables (engineering), fire protection equipment (procurement, materials), installation (construction), testing (commissioning) per decomposition

**Impacted WBS/CBS:** All CBS buckets except excluded scopes

**Estimate Impact:** Estimate includes full EPC coverage for contractor scope

**Override Path:** Modify `_CONFIG.md` include_scopes/exclude_scopes if different coverage is required

---

### D-005: Scope Exclusions

**Decision:** Exclude Owner's costs, land acquisition, financing costs, permits obtained by Employer, building sprinkler systems (PKG-22 scope).

**Trigger:** Exclusions required for estimate boundary definition.

**Evidence:**
- Config file specifies exclude scopes
- Decomposition Section 1.2 Scope Focus confirms "Contractor's scope of work only"
- Building fire suppression systems allocated to PKG-22 Building Interior & MEP per decomposition

**Impacted WBS/CBS:** N/A (exclusions)

**Estimate Impact:** Building sprinkler systems not costed in PKG-23; allocated to PKG-22

**Override Path:** Review decomposition if scope boundary changes

---

### D-006: Rounding Policy

**Decision:** Round to nearest $1,000 CAD.

**Trigger:** Rounding policy required per config.

**Evidence:**
- Config file specifies `rounding: 1000`

**Impacted WBS/CBS:** All summary totals

**Estimate Impact:** Summary totals rounded; Detail.csv retains calculated precision

**Override Path:** Modify `_CONFIG.md` rounding if different precision required

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
- DEL-23.03 fire water demand calculations not complete
- Fallback typical model permits allowance-based pricing when sources are not available (AGENT_ESTIMATING.md STRUCTURE section "Placeholder allowance policy")

**Impacted WBS/CBS:** All CBS buckets (Engineering, Materials, Construction Directs, Construction Indirects, PM, Procurement, Commissioning)

**Estimate Impact:** All line items are lump-sum allowances (Qty=1, Unit=LS, UnitRate=Amount); estimate confidence is LOW

**Override Path:** Provide design quantities from DEL-23.01 drawings and DEL-23.03 calculations; obtain vendor quotes for fire protection equipment

---

### D-009: Indirects Model Selection

**Decision:** Use factor-based indirects model (fallback typical model).

**Trigger:** No schedule/duration data available; indirects model required for CI, PM, P, COM pricing.

**Evidence:**
- No schedule or duration data discovered in deliverables
- Fallback typical model (AGENT_ESTIMATING.md STRUCTURE section "Default factors") defines factor-based indirects:
  - Construction Indirects (CI) = 0.18 × Construction Directs (CD)
  - Procurement Services (P) = 0.02 × (MAT)
  - EPCM/PM = 0.06 × (CD + CI + MAT)
  - Commissioning (COM) = 0.03 × (CD + CI + MAT)

**Impacted WBS/CBS:** CI, PM, P, COM buckets

**Estimate Impact:** Indirects are factor-derived based on directs/materials base costs

**Override Path:** Provide project schedule with durations and resource loading to enable time-based indirects pricing

---

### D-010: WBS → CBS Mapping for PKG-23 Deliverables

**Decision:** Map PKG-23 deliverables to CBS buckets as follows:
- DEL-23.01, 23.02, 23.03, 23.04 → Engineering (E)
- DEL-23.05 → Construction Indirects (CI) for QA/QC records capture
- Fire protection equipment (hydrants, FACP, detectors, foam equipment) → Materials (MAT)
- Installation work (fire water loop, hydrants, fire alarm, foam systems) → Construction Directs (CD)

**Trigger:** WBS → CBS mapping required for cost categorization.

**Evidence:**
- DEL-23.01 through DEL-23.04 are design deliverables (Drawing, Specification, Calculation, Data Sheet) → Engineering discipline
- DEL-23.05 is QA/QC records → Construction Indirects
- PKG-23 scope includes fire protection equipment → Materials bucket
- PKG-23 scope includes installation → Construction Directs
- Testing and commissioning (hydrostatic, flow, fire alarm, foam testing) → included in Commissioning bucket via indirects factor

**Impacted WBS/CBS:** All PKG-23 deliverables mapped to E, MAT, CD, CI buckets

**Estimate Impact:** Cost distribution across CBS buckets reflects engineering-heavy (design) + materials/construction (installation) mix

**Override Path:** Review mapping if deliverable types or CBS bucket definitions change

---

### D-011: Fire Pump Exclusion

**Decision:** Exclude fire pump from PKG-23 estimate; assume municipal fire water supply provides adequate pressure.

**Trigger:** Fire pump requirement not confirmed; need to determine if dedicated fire pump is required.

**Evidence:**
- No fire water demand calculation available (DEL-23.03 INITIALIZED)
- No hydraulic analysis available to confirm supply pressure adequacy
- Municipal fire water supply often adequate for industrial facilities in urban areas
- Fire pump may be required if supply pressure is insufficient or if insurance/AHJ requires dedicated pump

**Impacted WBS/CBS:** MAT, CD, CI, COM (fire pump would add $150k-300k to estimate)

**Estimate Impact:** Fire pump cost excluded; estimate may be understated if fire pump required

**Override Path:** Complete DEL-23.03 hydraulic calculations; confirm municipal supply pressure; add fire pump scope if required

---

### D-012: Foam System Inclusion

**Decision:** Include tank foam suppression system for all 3 × 15,000 MT tanks and marine loading foam system in PKG-23 scope.

**Trigger:** Foam system requirement for combustible liquid storage facilities per NFPA 30.

**Evidence:**
- Product is CSD canola oil, Class IIIA combustible liquid per NFPA 30 (flash point >93°C)
- NFPA 30 requires foam suppression for combustible liquid storage tanks above certain thresholds
- DEL-23.01 anticipated artifacts include foam system layout
- DEL-23.02 anticipated artifacts include foam system specification

**Impacted WBS/CBS:** MAT ($425k foam equipment), CD ($150k foam installation)

**Estimate Impact:** Foam system is significant cost driver (~$575k or 27% of base estimate)

**Override Path:** Confirm foam system requirements per NFPA 30 and insurance/AHJ; adjust foam system scope if alternative fire protection approach approved

---

---

## PKG-24 Decisions

**Package:** PKG-24 Security Systems
**Source:** Extracts/PKG-24_Decision_Log.md

PKG-24 includes 11 decisions covering workspace paths, currency, pricing date, escalation mode, scope, WBS/CBS mapping, rounding policy, pricing method, indirects model, contingency method, and Terminal integration scope per DEC-05.

Key decisions:
- **D-005:** Scope inclusions/exclusions (EPC scope, exclude Owner's costs)
- **D-008:** Pricing method - fallback model (allowances + parametric factors)
- **D-010:** Contingency method - PCT_BY_BUCKET with 26% blended rate
- **D-011:** Terminal integration - separate CCTV and access control interfaces per DEC-05

For detailed decision descriptions, see `Extracts/PKG-24_Decision_Log.md`.

**Total Cumulative Decisions:** ~275 (across all packages)

---

**Updated:** 2026-01-29 03:06

---

## PKG-25 Decisions

**Package:** PKG-25 Communications & IT
**Source:** Extracts/PKG-25_Decision_Log.md

PKG-25 includes 12 decisions covering workspace paths, currency, pricing date, scope, indirects method, rounding, contingency, escalation, WBS/CBS mapping, pricing sources, and network architecture assumptions.

Key decisions:
- **D-2505:** Scope exclusions (CCTV/access control to PKG-24 per DEC-05; control systems to PKG-19)
- **D-2506:** Factor-based indirects (CI=18%, P=2%, PM=6%, COM=3%)
- **D-2508:** Contingency method - PCT_BY_BUCKET with 28% blended rate
- **D-2511:** Fallback allowance model (no quotes or rate tables)
- **D-2512:** Network architecture assumptions (4-8 switches, 50-100 data drops)

For detailed decision descriptions, see `Extracts/PKG-25_Decision_Log.md`.

**Total Cumulative Decisions:** ~287 (across all packages)

---

**Updated:** 2026-01-29 03:14

---

## PKG-26 Decisions

**Package:** PKG-26 Protective Coatings & Painting
**Decisions:** 15 (D-2601 through D-2615)

Key decisions cover workspace paths, currency, pricing method, quantity derivation from related packages (PKG-06/08/13), surface area conversion factors, and contingency rates.

**Updated:** 2026-01-29 03:24

---

## PKG-27 Decisions
**Package:** PKG-27 Engineering Design
**Updated:** 2026-01-29 03:33
