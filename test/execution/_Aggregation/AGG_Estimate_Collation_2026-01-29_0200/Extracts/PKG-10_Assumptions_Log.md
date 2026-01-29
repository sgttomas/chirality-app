# Assumptions Log

## Overview

This log captures all assumptions and allowances made during the estimating process where quantities, rates, or scope elements required assumption due to missing source data.

---

## A-001: Unloading Arm Pricing

**Assumption:** Railcar unloading arms priced at $50,000 CAD per unit (32 units).

**Why Needed:** No vendor quotes or budgetary proposals available for unloading arms.

**Impacted WBS/CBS:** PKG-10 / MAT

**Cost Impact:** $1,600,000 (total for 32 arms); range $1,440,000 - $1,920,000 (±20% based on $45k-60k/unit industry typical range)

**Confidence:** LOW

**Resolution Path:** Obtain budgetary quotes from specialized railcar unloading equipment suppliers (TechnipFMC, OPW, Emco Wheaton, Ultraflow, Civacon).

**Notes:** Articulating bottom-loading arms for food-grade service typically $45k-60k/unit depending on materials (aluminum vs stainless), reach envelope, swivel configuration, and manufacturer. Gravity flow arms are simpler than pump-assisted but still specialized equipment.

---

## A-002: Quick-Connect Coupler Pricing

**Assumption:** Quick-connect couplers priced at $3,000 CAD per unit (32 units).

**Why Needed:** No vendor quotes available; couplers may be integral to arms or separate components.

**Impacted WBS/CBS:** PKG-10 / MAT

**Cost Impact:** $96,000 (total for 32 couplers); range $80,000 - $112,000 (±15% based on $2.5k-3.5k/unit typical)

**Confidence:** LOW

**Resolution Path:** Clarify if couplers are integral to unloading arms (included in arm price) or separate procurement; obtain coupler pricing from suppliers.

**Notes:** Dry-break cam-lock couplers for food-grade service typically $2.5k-3.5k/unit. If integral to arms, eliminate this line and adjust arm pricing accordingly.

---

## A-003: Header Piping Length

**Assumption:** Gravity flow header piping length estimated at 400 linear meters.

**Why Needed:** DEL-10.01 header layout drawings not yet available; piping length required for material and labor estimates.

**Impacted WBS/CBS:** PKG-10 / MAT, CD

**Cost Impact:** $280,000 material + $180,000 labor = $460,000 total; range $368,000 - $552,000 (±20% based on 320-480 lm range)

**Confidence:** LOW-MEDIUM

**Resolution Path:** Provide DEL-10.01 header layout drawings; measure actual piping length from layout.

**Notes:** Estimate based on: 32 stations at ~12m spacing average = ~380m main header run + ~20m for branch connections and routing = 400 lm total. Actual length depends on station spacing (per PKG-07 track layout), header routing path, and elevation changes.

---

## A-004: Spill Containment Pan Quantity and Configuration

**Assumption:** 32 individual spill containment pans (one per unloading station) at $8,000/unit.

**Why Needed:** Containment configuration (individual pans vs grouped zones vs common containment) not yet defined in DEL-10.01.

**Impacted WBS/CBS:** PKG-10 / MAT, CD

**Cost Impact:** $256,000 material + $144,000 labor = $400,000 total; range could vary significantly with configuration

**Confidence:** LOW

**Resolution Path:** Provide DEL-10.01 containment details drawings; verify pan configuration and regulatory compliance per DEL-10.03 calculations.

**Notes:** Individual pans provide localized containment (easier cleanup, isolated spills) but higher cost and installation complexity vs. grouped containment zones. Regulatory requirements (Environment Canada, BC regulations) drive minimum containment volume. Pan pricing assumes fabricated steel pans with drains, ~2m × 3m × 0.3m typical dimensions per station.

---

## A-005: Sump Pump Quantity

**Assumption:** 8 sump pumps for grouped containment drainage (4 pumps per zone × 2 zones).

**Why Needed:** Drainage configuration not yet defined; pump quantity depends on containment zone arrangement from DEL-10.01.

**Impacted WBS/CBS:** PKG-10 / MAT, CD

**Cost Impact:** $48,000 material + $24,000 labor = $72,000 total; range $24,000 - $144,000 (varies with pump count 4-24)

**Confidence:** LOW

**Resolution Path:** Provide DEL-10.01 containment details drawings and DEL-10.03 drainage calculations showing pump quantity and sizing.

**Notes:** Pump quantity options: (a) 32 individual pumps (1 per pan) = highest cost/complexity; (b) grouped zones with 4-8 pumps per zone = balanced approach (assumed); (c) common containment with 1-2 pumps = lowest cost but longest drainage times and higher single-point failure risk.

---

## A-006: Engineering - Design Drawing Set Allowance

**Assumption:** DEL-10.01 Design Drawing Set engineering effort priced at $55,000.

**Why Needed:** No engineering rate table or historical data for drawing production effort.

**Impacted WBS/CBS:** PKG-10 DEL-10.01 / E

**Cost Impact:** $55,000; range $45,000 - $70,000 (±20%)

**Confidence:** LOW

**Resolution Path:** Provide engineering labor rates and estimated drawing production hours; or use historical project data for similar drawing sets.

**Notes:** Estimate based on typical effort for unloading system GA, 32 arm arrangement drawings (may be multiple sheets for clarity), header layout with profile, and containment details. Drawing set is larger than typical due to 32 stations requiring detailed arrangements.

---

## A-007: Engineering - Technical Specification Allowance

**Assumption:** DEL-10.02 Technical Specification engineering effort priced at $18,000.

**Why Needed:** No engineering rate table or historical data for specification development.

**Impacted WBS/CBS:** PKG-10 DEL-10.02 / E

**Cost Impact:** $18,000; range $15,000 - $22,000 (±20%)

**Confidence:** LOW

**Resolution Path:** Provide engineering labor rates and estimated specification development hours.

**Notes:** Specification covers unloading arm requirements, header pipe specification, and containment system specification with materials and workmanship requirements.

---

## A-008: Engineering - Design Calculations Allowance

**Assumption:** DEL-10.03 Design Calculations engineering effort priced at $28,000.

**Why Needed:** No engineering rate table or calculation effort data available.

**Impacted WBS/CBS:** PKG-10 DEL-10.03 / E

**Cost Impact:** $28,000; range $22,000 - $35,000 (±20%)

**Confidence:** LOW

**Resolution Path:** Provide engineering labor rates and estimated calculation hours for header sizing, throughput analysis, and containment volume calculations.

**Notes:** Calculations include header pipe sizing (gravity flow hydraulics for 400 lm system with 32 branches), unloading rate and throughput verification (1,000,000 MT/annum capacity demonstration), and containment volume sizing (regulatory compliance for 32 stations or zones).

---

## A-009: Engineering - Data Sheet Package Allowance

**Assumption:** DEL-10.04 Data Sheet Package engineering effort priced at $22,000.

**Why Needed:** No engineering rate table for data sheet development effort.

**Impacted WBS/CBS:** PKG-10 DEL-10.04 / E

**Cost Impact:** $22,000; range $18,000 - $28,000 (±20%)

**Confidence:** LOW

**Resolution Path:** Provide engineering labor rates and estimated hours for 32 arm data sheets + quick-connect sheets + pump sheets.

**Notes:** Data sheet package includes 32 unloading arm data sheets, quick-connect coupler sheets (may be integral to arm sheets or separate), and sump pump data sheets (8 pumps). Higher effort than typical due to 32 repetitive arm data sheets requiring individualization (tag numbers, locations, P&ID references).

---

## A-010: Engineering - Installation & Test Records Allowance

**Assumption:** DEL-10.05 Installation & Test Records engineering/QA effort priced at $12,000.

**Why Needed:** No QA/documentation rate data available.

**Impacted WBS/CBS:** PKG-10 DEL-10.05 / E

**Cost Impact:** $12,000; range $10,000 - $15,000 (±20%)

**Confidence:** LOW

**Resolution Path:** Provide QA/documentation labor rates and estimated record preparation hours.

**Notes:** Records include FAT records (32 arms), installation records (arms + header + containment + pumps), and hydrostatic test records (header pressure testing).

---

## A-011: Flow Indicator Pricing

**Assumption:** Flow indicators priced at $2,500 CAD per unit (32 units).

**Why Needed:** No vendor quotes for flow indication devices.

**Impacted WBS/CBS:** PKG-10 / MAT

**Cost Impact:** $80,000 (total for 32 indicators); range $64,000 - $96,000 (based on $2k-3k/unit typical)

**Confidence:** LOW

**Resolution Path:** Obtain quotes for local flow indicators suitable for food-grade canola oil service.

**Notes:** Local flow indicators (visual or simple electronic) for operator verification at each station. Custody transfer metering (PKG-12) is separate; these are operational indicators only.

---

## A-012: Atmospheric Venting System Pricing

**Assumption:** Atmospheric venting system (32 connections + routing + flame arrestors) priced at $65,000 total.

**Why Needed:** No vendor quotes or detailed scope for venting system.

**Impacted WBS/CBS:** PKG-10 / MAT

**Cost Impact:** $65,000; range $50,000 - $80,000 (±25%)

**Confidence:** LOW

**Resolution Path:** Verify venting requirements in Employer's Requirements; obtain quotes for vent piping and flame arrestors.

**Notes:** Estimate includes 32 vent connections from railcar unloading points, vent piping/manifold, flame arrestors (safety requirement for atmospheric venting of flammable vapors, though canola oil is non-flammable with flash point >300°C), and supports. Vent routing configuration TBD (individual vents vs. manifold).

---

## A-013: Isolation Valves and Fittings Pricing

**Assumption:** Header isolation valves and fittings priced at $85,000 total.

**Why Needed:** No valve schedule or vendor quotes; valve quantity and sizing TBD per DEL-10.01 and DEL-10.03.

**Impacted WBS/CBS:** PKG-10 / MAT

**Cost Impact:** $85,000; range $65,000 - $110,000 (±30%)

**Confidence:** LOW

**Resolution Path:** Provide DEL-10.01 header layout showing valve locations; obtain valve vendor quotes.

**Notes:** Estimate includes isolation valves at header sections (operational flexibility per OBJ-4), branch isolation valves at station connections (32 branch valves), pipe fittings (elbows, tees, reducers), and pipe supports. Valve sizing per header pipe diameter (8-12 inch per A-003).

---

## A-014: Installation Consumables Pricing

**Assumption:** Installation consumables and fasteners priced at $45,000 total.

**Why Needed:** No detailed material takeoff for welding consumables, fasteners, gaskets, sealants.

**Impacted WBS/CBS:** PKG-10 / MAT

**Cost Impact:** $45,000; range $35,000 - $55,000 (±25%)

**Confidence:** LOW

**Resolution Path:** Develop detailed material takeoff from DEL-10.01 drawings and installation procedures.

**Notes:** Includes welding electrodes/wire for header piping installation (~400 lm of pipe), anchor bolts for arm and pump mounting, gaskets for flanged connections, sealants for containment pan joints, miscellaneous hardware.

---

## A-015: Unloading Arm Installation Labor

**Assumption:** Unloading arm installation labor priced at $8,000 per unit (32 units = $256,000 total).

**Why Needed:** No project labor rates or productivity data; installation scope TBD.

**Impacted WBS/CBS:** PKG-10 / CD

**Cost Impact:** $256,000 total; range $192,000 - $320,000 (±25% based on $6k-10k/unit range)

**Confidence:** LOW

**Resolution Path:** Provide labor rates and installation method statement with estimated hours per arm.

**Notes:** Estimate based on ~70-80 hours per arm @ $110/hr all-in composite rate (includes fitter, helper, supervision markup). Work scope includes: arm mounting to foundation/support, alignment to railcar position, connection to header branch, testing and adjustment.

---

## A-016: Header Piping Installation Labor

**Assumption:** Header piping installation labor priced at $450 per linear meter (400 lm = $180,000 total).

**Why Needed:** No project labor rates or productivity data for piping installation.

**Impacted WBS/CBS:** PKG-10 / CD

**Cost Impact:** $180,000 total; range $140,000 - $220,000 (±25%)

**Confidence:** LOW

**Resolution Path:** Provide labor rates and piping installation productivity rates (hrs/lm by diameter).

**Notes:** Estimate based on ~4-5 hours per linear meter @ $110/hr all-in for 8-12 inch pipe. Work scope includes: pipe welding, support installation, joint preparation, NDE (radiography or ultrasonic per code), pressure testing, coating touch-up.

---

## A-017: Containment Pan Installation Labor

**Assumption:** Containment pan installation labor priced at $4,500 per unit (32 units = $144,000 total).

**Why Needed:** No labor rates or installation method data for containment pan placement.

**Impacted WBS/CBS:** PKG-10 / CD

**Cost Impact:** $144,000 total; range $115,000 - $175,000 (±20%)

**Confidence:** LOW

**Resolution Path:** Provide labor rates and installation method statement with estimated hours per pan.

**Notes:** Estimate based on ~40 hours per pan @ $110/hr all-in. Work scope includes: pan placement and leveling, seal welding for liquid-tight construction, drain connections, leak testing.

---

## A-018: Sump Pump Installation Labor

**Assumption:** Sump pump installation labor priced at $3,000 per unit (8 units = $24,000 total).

**Why Needed:** No labor rates or pump installation data.

**Impacted WBS/CBS:** PKG-10 / CD

**Cost Impact:** $24,000 total; range $18,000 - $30,000 (±25%)

**Confidence:** LOW

**Resolution Path:** Provide labor rates and pump installation hours.

**Notes:** Estimate based on ~25 hours per pump @ $110/hr all-in. Work scope includes: pump mounting/installation, discharge piping connections, electrical rough-in coordination (actual electrical work in PKG-17), level switch installation coordination (PKG-20), functional testing.

---

## A-019: Flow Indicator Installation Labor

**Assumption:** Flow indicator installation labor priced at $1,000 per unit (32 units = $32,000 total).

**Why Needed:** No labor rates or installation data for flow indicators.

**Impacted WBS/CBS:** PKG-10 / CD

**Cost Impact:** $32,000 total; range $25,000 - $40,000 (±25%)

**Confidence:** LOW

**Resolution Path:** Provide labor rates and indicator installation hours.

**Notes:** Estimate based on ~8-10 hours per indicator @ $110/hr all-in. Work scope includes: indicator mounting at each station, piping connections, wiring rough-in coordination (PKG-20 final connections), calibration, functional testing.

---

## A-020: Venting System Installation Labor

**Assumption:** Venting system installation labor priced at $28,000 total (lump sum for 32 vent connections + piping + flame arrestors).

**Why Needed:** No labor rates or venting installation scope detail.

**Impacted WBS/CBS:** PKG-10 / CD

**Cost Impact:** $28,000 total; range $20,000 - $35,000 (±25%)

**Confidence:** LOW

**Resolution Path:** Provide labor rates and venting installation method statement.

**Notes:** Work scope includes: 32 vent connection installations at each station, vent piping/manifold installation, flame arrestor mounting (if required), supports, testing. Vent configuration TBD (individual vents vs manifolded system).

---

## A-021: Setting Out and Survey Labor

**Assumption:** Setting out and survey labor priced at $18,000 total for 32-station layout.

**Why Needed:** No survey crew rates or layout effort data.

**Impacted WBS/CBS:** PKG-10 / CD

**Cost Impact:** $18,000 total; range $15,000 - $22,000 (±20%)

**Confidence:** LOW

**Resolution Path:** Provide survey labor rates and estimated hours for layout and as-built survey.

**Notes:** Work scope includes: initial station layout (32 unloading arm positions relative to track alignment), containment pan layout, header piping layout verification, as-built survey after installation.

---

## A-022: Hydrostatic Testing and Flushing Labor

**Assumption:** Hydrostatic testing and flushing labor priced at $22,000 total.

**Why Needed:** No labor rates or testing scope detail.

**Impacted WBS/CBS:** PKG-10 / CD

**Cost Impact:** $22,000 total; range $18,000 - $28,000 (±25%)

**Confidence:** LOW

**Resolution Path:** Provide labor rates and testing procedure with estimated hours.

**Notes:** Work scope includes: header system hydrostatic pressure test per ASME B31.3 (1.5× design pressure typical), test water fill and drain, flushing for cleanliness (food-grade requirement), drying, preservation for storage or service. Test duration depends on header volume and test procedure.

---

## A-023: Coating Touch-Up and Protection Labor

**Assumption:** Coating touch-up and protection labor priced at $13,000 total.

**Why Needed:** No labor rates or coating scope detail.

**Impacted WBS/CBS:** PKG-10 / CD

**Cost Impact:** $13,000 total; range $10,000 - $16,000 (±25%)

**Confidence:** LOW

**Resolution Path:** Provide coating labor rates and field coating requirements.

**Notes:** Work scope includes: field coating touch-up after installation (welded joints, damaged areas during installation), temporary corrosion protection for equipment during construction, surface preparation per coating spec.

---

## A-024: Unloading Arm FAT and Commissioning

**Assumption:** Unloading arm factory acceptance testing and commissioning priced at $1,800 per unit (32 units = $58,000 total).

**Why Needed:** No commissioning rates or FAT scope detail.

**Impacted WBS/CBS:** PKG-10 / COM

**Cost Impact:** $58,000 total; range $46,000 - $70,000 (±25%)

**Confidence:** LOW

**Resolution Path:** Provide commissioning labor rates and FAT procedures with estimated hours.

**Notes:** Estimate based on ~15 hours per arm @ $120/hr all-in. Work scope includes: factory acceptance testing (functionality, leak testing, swivel operation), site functional testing after installation, operational adjustments.

---

## A-025: System Integration Testing

**Assumption:** System integration testing priced at $28,000 total.

**Why Needed:** No commissioning scope detail or testing procedure available.

**Impacted WBS/CBS:** PKG-10 / COM

**Cost Impact:** $28,000 total; range $20,000 - $35,000 (±25%)

**Confidence:** LOW

**Resolution Path:** Provide commissioning procedures and estimated testing hours for integrated system testing.

**Notes:** Work scope includes: integrated system testing (multiple arms to header to storage), flow verification (gravity flow performance), control logic testing (if automated controls), interface testing with PKG-19 control system and PKG-20 instrumentation.

---

## A-026: Performance Testing and Verification

**Assumption:** Performance testing and verification priced at $22,000 total.

**Why Needed:** No performance testing scope detail available.

**Impacted WBS/CBS:** PKG-10 / COM

**Cost Impact:** $22,000 total; range $18,000 - $28,000 (±25%)

**Confidence:** LOW

**Resolution Path:** Provide performance testing procedures and acceptance criteria from Employer's Requirements.

**Notes:** Work scope includes: throughput verification testing (demonstrate 1,000,000 MT/annum capacity per OBJ-2), containment system testing (leak testing, drainage verification), acceptance testing per ER criteria, performance documentation.

---

## A-027: Final Inspection and Documentation

**Assumption:** Final inspection and commissioning documentation priced at $14,000 total.

**Why Needed:** No commissioning documentation effort data.

**Impacted WBS/CBS:** PKG-10 / COM

**Cost Impact:** $14,000 total; range $10,000 - $18,000 (±30%)

**Confidence:** LOW

**Resolution Path:** Provide commissioning team rates and documentation hours.

**Notes:** Work scope includes: final system inspection, punch list completion, commissioning records preparation, operations and maintenance manual review, handover documentation to Owner.

---

## A-028: Seasonal Constraints

**Assumption:** Year-round construction feasible; winterization may affect unloading operations but not construction schedule.

**Why Needed:** No schedule constraints documented; seasonal impacts on construction productivity not specified.

**Impacted WBS/CBS:** CD, CI (labor productivity and schedule)

**Cost Impact:** Minimal for construction (standard year-round construction assumed); operational winterization costs excluded (operations phase, not construction)

**Confidence:** MEDIUM

**Resolution Path:** Verify construction schedule constraints in project schedule; verify winterization requirements for unloading operations in Employer's Requirements.

**Notes:** Fraser Surrey location allows year-round construction (lower mainland BC climate). Canola oil pour point ~-10°C may require product heating for winter operations, but winterization is operational scope (not construction estimate).

---

## Summary

Total assumptions logged: 28 (A-001 through A-028)

**Assumptions by value impact (HIGH = >$200k; MEDIUM = $50k-200k; LOW = <$50k):**

| Impact Level | Count | Examples |
|--------------|-------|----------|
| HIGH | 3 | A-001 Unloading arms ($1.6M), A-003 Header piping ($460k), A-004 Containment pans ($400k) |
| MEDIUM | 2 | A-016 Header install labor ($180k), A-015 Arm install labor ($256k) |
| LOW | 23 | All other assumptions |

**Assumptions by category:**
- Equipment pricing: 7 assumptions (A-001, A-002, A-011, A-012, A-013)
- Material quantities: 3 assumptions (A-003, A-004, A-005)
- Engineering effort: 5 assumptions (A-006 through A-010)
- Installation labor: 8 assumptions (A-015 through A-023)
- Commissioning: 4 assumptions (A-024 through A-027)
- Site conditions: 1 assumption (A-028)

**Critical assumptions requiring resolution:**
1. **A-001** (Unloading arms $1.6M): Obtain vendor quotes — 32 specialized arms are single largest cost item
2. **A-003** (Header piping 400 lm): Verify from DEL-10.01 layout — material and labor affected
3. **A-004** (32 containment pans): Verify configuration (individual vs grouped) and regulatory requirements
4. **A-005** (8 sump pumps): Verify pump quantity from containment design

All assumptions are placeholders pending better source data (vendor quotes, rate tables, design details, regulatory requirements). Estimate confidence will improve significantly when quotes and design details are available.
