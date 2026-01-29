# Risk Register

## Snapshot Identification

| Field | Value |
|-------|-------|
| Snapshot ID | EST_PKG12_DRAFT_2026-01-28_2341 |
| Estimate Label | PKG12_DRAFT |
| Package | PKG-12 Product Transfer & Metering |
| Date | 2026-01-28 |

---

## R-001: Meter Technology Selection Impact on Cost

**Risk Driver:** Scope / Price

**Cause:** Meter technology not selected in DEL-12.02 specification; Coriolis assumed but ultrasonic, turbine, or positive displacement alternatives possible

**Consequence:** Flow meter costs may vary ±40-60% depending on technology selection

**Cost Range by Technology:**
- Coriolis mass: $150k-250k/unit (assumed in estimate)
- Ultrasonic: $80k-150k/unit (lower cost, requires separate density)
- Turbine: $30k-80k/unit (lowest cost, viscosity-sensitive, lower accuracy)
- Positive displacement: $50k-120k/unit (moderate cost, higher pressure drop)

**Affected Buckets:**
- MAT: $410k (2 meters) could range $260k-500k
- CD: Installation complexity varies by meter type
- COM: Proving requirements vary by meter type

**Suggested Mitigation:**
1. Confirm custody transfer accuracy requirements in ER Vol 2 Part 2
2. Perform technology trade study in DEL-12.02 considering accuracy, cost, product properties (CSD canola oil viscosity), pressure drop, proving requirements
3. Obtain vendor quotes for shortlisted technologies
4. Update estimate after technology selection with vendor budgetary quotes

**Contingency Handling:** MAT contingency 25% provides ~$100k buffer; technology variance could exceed this

---

## R-002: Proving Method Selection Impact on Cost

**Risk Driver:** Scope / Price

**Cause:** Proving method not selected in DEL-12.02; portable prover assumed but in-line provers or master meter alternatives possible

**Consequence:** Proving equipment costs range $60k-400k depending on method

**Cost Range by Proving Method:**
- Portable prover: $100k-150k (assumed in estimate)
- In-line provers (×2, one per service): $300k-500k (higher cost, continuous proving capability)
- Master meter: $50k-80k equipment + periodic calibration (~$10k-20k/year; lifecycle cost consideration)

**Affected Buckets:**
- MAT: Portable prover $120k vs. in-line provers $400k vs. master meter $60k (±$280k swing)
- COM: Proving labor varies (portable prover mobilization vs. in-line prover automated proving vs. master meter external calibration)

**Suggested Mitigation:**
1. Confirm proving frequency requirements in ER Vol 2 Part 2 and Measurement Canada regulations
2. Evaluate proving method options in DEL-12.03 calculations considering accuracy requirements, operational schedule, cost, space constraints
3. Coordinate with operations on proving downtime tolerance
4. Update estimate after proving method selection

**Contingency Handling:** MAT contingency provides ~$180k buffer; proving method swing could exceed this if in-line provers required

---

## R-003: Flow Rate Specification Affects Meter Sizing and Cost

**Risk Driver:** Scope / Quantity

**Cause:** Design flow rates not specified in ER Vol 2 Part 2 or PKG-10/PKG-11; meter sizes estimated parametrically (6" rail, 10" marine)

**Consequence:** Actual meter sizes may differ; larger meters cost more and affect installation complexity

**Meter Size Sensitivity:**
- Rail unloading: 4" meter ~$120k-160k; 6" meter ~$150k-200k; 8" meter ~$180k-220k
- Marine loading: 8" meter ~$180k-220k; 10" meter ~$200k-250k; 12" meter ~$250k-300k

**Affected Buckets:**
- MAT: Meter costs ±20-30% if sizes differ from assumption
- MAT: Piping costs vary with meter size (larger straight-run sections)
- CD: Installation manhours vary with meter size and weight

**Suggested Mitigation:**
1. Obtain design flow rates from ER Vol 2 Part 2 or perform flow calculations in PKG-10/PKG-11
2. Perform meter sizing calculations in DEL-12.03 with defined flow rates and product properties
3. Coordinate with PKG-10 (railcar unloading) and PKG-11 (marine loading) on hydraulics and flow rates
4. Obtain vendor sizing recommendations with budgetary quotes

**Contingency Handling:** MAT contingency 25% provides buffer for sizing variance; extreme sizing changes (e.g., 12" marine meter vs. 10" assumed) could exceed buffer

---

## R-004: Deliverable Scope Expansion During Engineering

**Risk Driver:** Scope

**Cause:** Deliverables currently in INITIALIZED state; engineering progression from INITIALIZED → IN_PROGRESS → CHECKING may reveal additional scope

**Consequence:** Engineering effort (E) and deliverable outputs may increase

**Potential Scope Additions:**
- Additional drawing sheets beyond 3-sheet minimum (DEL-12.01)
- Extended specification content (DEL-12.02)
- Additional calculation complexity (uncertainty analysis, sensitivity studies in DEL-12.03)
- Additional data sheets (proving equipment, flow computers, additional transmitters in DEL-12.04)
- Extended test record scope (periodic proving records, regulatory compliance documentation in DEL-12.05)

**Affected Buckets:**
- E: Engineering deliverables currently $138k; could increase 20-40% if scope expands

**Suggested Mitigation:**
1. Progress deliverables to IN_PROGRESS with defined scope and acceptance criteria
2. Confirm drawing count, specification length, calculation scope, data sheet count in work planning
3. Review ER Vol 2 Part 2 for metering documentation requirements
4. Re-estimate engineering effort after scope is defined

**Contingency Handling:** E contingency 20% provides ~$28k buffer (~20% scope growth); larger scope growth would require additional budget

---

## R-005: Interface Coordination Scope with Adjacent Packages

**Risk Driver:** Interface / Scope

**Cause:** Interfaces with PKG-06 (structural), PKG-14 (piping), PKG-17 (electrical), PKG-19 (controls), PKG-20 (instrumentation) not fully coordinated; dependency mode is NOT_TRACKED

**Consequence:** Installation scope boundary unclear; may affect labor estimate and material scope

**Interface Uncertainties:**
- PKG-06: Metering skid structural design and fabrication scope split unclear
- PKG-14: Meter run piping vs. process piping scope boundary unclear
- PKG-17: Electrical installation scope for metering power supply
- PKG-19: Flow computer vs. control system integration (DCS/PLC totalizing)
- PKG-20: Transmitter installation scope (metering-specific vs. general instrumentation)

**Affected Buckets:**
- MAT: Structural steel, piping, flow computers may shift to/from adjacent packages
- CD: Installation labor scope boundary affects manhour estimate
- E: Interface coordination effort

**Suggested Mitigation:**
1. Establish scope boundaries with adjacent packages per NOT_TRACKED coordination mode
2. Clarify whether metering skid structural design is in PKG-12 or PKG-06
3. Clarify meter run piping scope (PKG-12 straight-runs vs. PKG-14 process piping)
4. Clarify flow computer/totalizer scope (PKG-12 dedicated vs. PKG-19 DCS integration)
5. Update estimate after interface scope is defined

**Contingency Handling:** Contingency across affected CBS buckets provides buffer; significant scope shifts may require re-estimate

---

## R-006: Measurement Canada Regulatory Compliance Costs

**Risk Driver:** Scope / Price

**Cause:** Measurement Canada approval requirements for custody transfer in Canada not specified in ER or deliverables

**Consequence:** Additional costs for meter certification, periodic verification, regulatory documentation, or third-party inspection

**Potential Additional Costs:**
- Measurement Canada meter approval: $10k-30k per meter type
- Periodic verification costs: $5k-15k/year ongoing
- Third-party inspection/witness for proving: $10k-20k
- Regulatory documentation and record-keeping: included in DEL-12.05 estimate

**Affected Buckets:**
- MAT: Meter certification costs
- COM: Periodic verification, third-party witness
- E: Regulatory compliance documentation

**Suggested Mitigation:**
1. Research Measurement Canada Weights and Measures Act requirements for custody transfer of vegetable oil
2. Confirm in ER Vol 2 Part 2 whether Measurement Canada approval is required
3. Coordinate with legal/commercial on custody transfer regulatory compliance strategy
4. Obtain quotes from Measurement Canada-approved meter suppliers
5. Add regulatory compliance line items if required

**Contingency Handling:** COM and MAT contingency provide buffer; significant regulatory costs may require additional allowance

---

## R-007: Installation Labor Productivity and Site Conditions

**Risk Driver:** Productivity / Schedule

**Cause:** Labor productivity assumes standard site conditions; actual site conditions at Fraser Surrey Terminal not assessed

**Consequence:** Installation manhours may increase if site access, laydown, or working conditions are constrained

**Productivity Factors:**
- Site access constraints (terminal operations continuity per OBJ-5)
- Laydown and staging area availability
- Crane/lifting equipment access
- Work permit and hot work requirements
- Working hours restrictions (if terminal operations limit construction hours)
- Weather (Pacific Northwest rain may affect outdoor work productivity)

**Affected Buckets:**
- CD: Installation labor $311k base; productivity factor 0.8 would increase to ~$390k (+$79k)
- CI: Indirects scale with CD; productivity impact propagates

**Suggested Mitigation:**
1. Conduct site visit or obtain site logistics plan
2. Confirm working hours and access constraints with terminal operations
3. Develop detailed installation sequence and logistics plan in Procedure.md
4. Coordinate with PKG-00 (site establishment) on laydown and staging areas
5. Adjust productivity factor if site constraints identified

**Contingency Handling:** CD contingency 30% provides ~$93k buffer for productivity variance; severe constraints may exceed buffer

---

## R-008: Vendor Lead Times and Procurement Schedule

**Risk Driver:** Schedule / Price

**Cause:** Custody transfer flow meters have long lead times (typical 20-32 weeks); schedule constraints may require expediting or affect installation sequence

**Consequence:** Expediting costs, potential schedule delays affecting indirects duration, or installation sequence changes

**Lead Time Estimates (typical):**
- Custody transfer Coriolis flow meters: 20-32 weeks (engineered-to-order with Measurement Canada approval)
- Portable prover: 16-24 weeks
- Transmitters: 8-16 weeks
- Flow computers: 12-20 weeks

**Affected Buckets:**
- MAT: Expediting costs (typically 5-15% premium for accelerated delivery)
- CI: Extended duration if critical path affected
- COM: FAT schedule depends on vendor production schedule

**Suggested Mitigation:**
1. Initiate vendor engagement early (during DEL-12.02 specification development)
2. Obtain lead time confirmation with budgetary quotes
3. Consider procurement strategy: issue inquiry early, or provide performance spec allowing multiple vendors
4. Coordinate procurement schedule with project master schedule
5. Evaluate expediting vs. schedule float trade-off

**Contingency Handling:** Contingency includes schedule buffer; extreme expediting (>15%) may require additional budget

---

## R-009: Accuracy Requirements More Stringent Than Assumed

**Risk Driver:** Scope / Price

**Cause:** Custody transfer accuracy requirement not specified in ER Vol 2 Part 2; assumed ±0.15% typical for vegetable oil custody transfer

**Consequence:** Tighter accuracy (e.g., ±0.10% or better) requires higher-grade meters, more rigorous proving, tighter installation tolerances

**Cost Impact if Accuracy Tightened:**
- Flow meters: High-accuracy Coriolis +10-20% cost premium
- Installation: Tighter tolerances increase labor +10-15%
- Proving: More frequent proving or in-line provers required (+$200k-300k)
- Commissioning: Extended proving runs and uncertainty verification (+20-30%)

**Affected Buckets:**
- MAT: Flow meters, proving equipment
- CD: Installation precision
- COM: Proving and verification

**Suggested Mitigation:**
1. Confirm accuracy requirements in ER Vol 2 Part 2
2. Perform uncertainty budget analysis in DEL-12.03 to verify achievability
3. Obtain vendor quotes with accuracy class specified
4. Evaluate accuracy vs. cost trade-off with stakeholders

**Contingency Handling:** Contingency provides buffer for moderate accuracy tightening; stringent requirements (e.g., ±0.10%) may require budget increase

---

## R-010: Temperature Compensation and Density Measurement Requirements

**Risk Driver:** Scope

**Cause:** Compensation methodology not specified; assumed Coriolis integral density with temperature compensation; pressure compensation may/may not be required

**Consequence:** Compensation scope affects transmitter count, flow computer functionality, accuracy budget

**Compensation Scenarios:**
- **Scenario 1 (assumed):** Coriolis with integral density + temperature transmitters (4 units); pressure compensation not required
- **Scenario 2:** Volumetric meter + separate density measurement + temperature + pressure compensation (adds densitometers ~$30k-60k/unit)
- **Scenario 3:** Mass meter with minimal compensation (if product properties stable; lower transmitter count)

**Affected Buckets:**
- MAT: Transmitter count and type ($24k-34k current; could range $10k-80k)
- E: Calculation complexity in DEL-12.03
- COM: Calibration and proving scope

**Suggested Mitigation:**
1. Confirm compensation requirements in ER Vol 2 Part 2 or industry standards
2. Evaluate product property stability (CSD canola oil density and temperature variation)
3. Perform uncertainty budget in DEL-12.03 to determine required compensation
4. Confirm transmitter count in DEL-12.04

**Contingency Handling:** MAT and COM contingency provide buffer for compensation scope variance

---

## R-011: Integration with Control System (PKG-19) Complexity

**Risk Driver:** Interface / Scope

**Cause:** Metering system integration with control system (PKG-19) not detailed; scope boundary unclear

**Consequence:** Flow computers/totalizers may be PKG-12 scope or integrated in PKG-19 DCS/PLC; affects equipment cost and installation

**Integration Options:**
- **Option 1 (assumed):** Dedicated flow computers in PKG-12 ($36k included)
- **Option 2:** Totalizing integrated in PKG-19 DCS/PLC (flow computers removed from PKG-12; -$36k MAT; scope shifts to PKG-19)
- **Option 3:** Hybrid (basic totalizing in flow computers; advanced data logging in DCS)

**Affected Buckets:**
- MAT: Flow computers $36k may shift to PKG-19
- E: Interface engineering effort
- CD: Installation scope (flow computer mounting, wiring)

**Suggested Mitigation:**
1. Coordinate with PKG-19 on control system architecture and totalizing approach
2. Clarify scope boundary: dedicated flow computers (PKG-12) vs. DCS integration (PKG-19)
3. Confirm in DEL-12.02 specification and PKG-19 control system specification
4. Adjust estimate if flow computers shift to PKG-19 (-$36k MAT from PKG-12, +$36k+ to PKG-19)

**Contingency Handling:** Minor impact on PKG-12 total (~3% of MAT); contingency absorbs variance

---

## R-012: FAT and SAT Scope Not Defined

**Risk Driver:** Scope

**Cause:** Factory acceptance test (FAT) and site acceptance test (SAT) requirements not specified in ER or DEL-12.02

**Consequence:** Testing scope and costs may vary; FAT may not be required (reduces cost ~$32k) or may be more extensive (increases cost)

**Testing Scenarios:**
- **Minimal:** Factory calibration certificate only; no FAT witness; shop SAT only (-$32k FAT, -$10k SAT)
- **Assumed:** FAT at vendor for flow meters + site SAT ($32k FAT, $28k SAT)
- **Comprehensive:** Extended FAT + witnessed SAT + proving witness + third-party inspection (+$20k-40k)

**Affected Buckets:**
- COM: FAT/SAT $60k could range $20k-100k

**Suggested Mitigation:**
1. Confirm FAT/SAT requirements in ER Vol 2 Part 1 (general QA/QC) and ER Vol 2 Part 2 (metering-specific)
2. Define FAT/SAT scope and acceptance criteria in DEL-12.02 specification
3. Determine witness requirements (Employer witness, third-party, Measurement Canada)
4. Obtain FAT/SAT service quotes from vendors

**Contingency Handling:** COM contingency 30% provides ~$36k buffer for testing scope variance

---

## R-013: Metering Skid Structural Design Complexity

**Risk Driver:** Scope / Interface

**Cause:** Metering skid structural design not detailed in DEL-12.01; structural scope boundary with PKG-06 unclear

**Consequence:** Structural steel quantity and fabrication complexity may vary; skid design affects cost and installation

**Structural Scope Scenarios:**
- **Minimal:** Simple pipe supports on existing structures (coordinate with PKG-06; -$20k-30k from PKG-12 MAT)
- **Assumed:** Modular skid-mounted metering with access platforms ($55k structural steel)
- **Comprehensive:** Integrated multi-level skid with extensive platforms, stairs, handrails, weather protection (+$30k-50k)

**Affected Buckets:**
- MAT: Structural steel $55k could range $25k-105k
- CD: Skid assembly and installation labor varies with complexity
- E: Structural design effort (DEL-12.01 or PKG-06)

**Suggested Mitigation:**
1. Develop metering skid GA in DEL-12.01 with structural requirements
2. Coordinate with PKG-06 on structural design scope (who designs/details skid structure)
3. Confirm access and maintenance requirements affecting platform scope
4. Obtain fabrication quotes for metering skid structural steel
5. Clarify scope boundary: is metering skid structure in PKG-12 or PKG-06?

**Contingency Handling:** MAT contingency provides buffer; significant structural scope increase may require adjustment

---

## R-014: Installation Schedule and Site Coordination

**Risk Driver:** Schedule / Productivity

**Cause:** Installation schedule and site coordination with operating terminal not defined; OBJ-5 (minimize disturbance to Terminal operations) may constrain installation

**Consequence:** Work hour restrictions, phasing requirements, or access limitations may increase installation duration and labor cost

**Site Coordination Factors:**
- Terminal operations continuity (OBJ-5)
- Rail siding access during installation
- Marine berth access during installation
- Tie-ins to existing process piping (PKG-14) may require shutdown windows
- Hot work permits and safety coordination
- Concurrent construction activities (other packages)

**Affected Buckets:**
- CD: Installation labor may increase 10-30% if work hours constrained or phasing required
- CI: Indirects duration extends if installation extends
- COM: Commissioning window may be constrained by operations

**Suggested Mitigation:**
1. Develop installation sequence and site logistics plan in Procedure.md
2. Coordinate with terminal operations on access, shutdown windows, work hour restrictions
3. Coordinate with PKG-00 (site establishment) on site logistics and laydown areas
4. Identify critical tie-in windows requiring shutdowns (coordinate with PKG-14)
5. Adjust labor productivity factor if site constraints identified

**Contingency Handling:** CD contingency 30% and CI contingency 30% provide buffer for schedule/productivity variance

---

## R-015: Pressure Drop and System Hydraulics Interaction

**Risk Driver:** Interface / Performance

**Cause:** Meter pressure drop affects system hydraulics (PKG-14); pressure drop not calculated (requires flow rates and meter selection)

**Consequence:** Meter pressure drop may require pump upgrades or piping modifications in PKG-14; affects interface coordination

**Pressure Drop Estimates (typical):**
- Coriolis mass flowmeter: 0.5-2.0 bar pressure drop at design flow (depends on size and flow rate)
- Ultrasonic flowmeter: 0.1-0.5 bar (lower pressure drop)
- Turbine flowmeter: 0.2-1.0 bar
- Positive displacement: 1.0-3.0 bar (highest pressure drop)

**Affected Buckets:**
- PKG-14: May require pump capacity increase or piping size increase (cost impact in PKG-14, not PKG-12)
- PKG-12: Meter technology selection may be constrained by pressure drop budget

**Suggested Mitigation:**
1. Obtain system pressure budget from PKG-14 process piping hydraulics
2. Perform pressure drop calculations in DEL-12.03 for selected meter sizes
3. Coordinate with PKG-14 on acceptable pressure drop for metering
4. Evaluate meter technology considering pressure drop impact (ultrasonic if pressure budget tight)

**Contingency Handling:** No direct cost impact to PKG-12; affects PKG-14 hydraulics and possibly meter technology selection (which is captured in R-001)

---

## R-016: Proving Equipment Mobilization and Access

**Risk Driver:** Logistics / Interface

**Cause:** Portable prover mobilization, setup, and access requirements not defined; proving may require shutdowns or special access

**Consequence:** Proving mobilization costs and proving labor may increase if access is difficult or proving windows are limited

**Proving Logistics Factors:**
- Portable prover transport (size/weight)
- Connection to meters (proving hose routing, access clearances)
- Product handling during proving (displacement, containment, drainage)
- Operational shutdown windows for proving
- Specialist proving technician availability

**Affected Buckets:**
- COM: Initial proving $48k assumes straightforward access; difficult access could add +20-40%

**Suggested Mitigation:**
1. Define proving connection details in DEL-12.01 drawings
2. Confirm proving logistics and access requirements in DEL-12.03 and Procedure.md
3. Coordinate proving schedule with operations (shutdown windows)
4. Clarify product handling during proving (displacement volume, drainage, containment)

**Contingency Handling:** COM contingency 30% provides buffer for proving logistics variance

---

## R-017: Canola Oil Product Properties Affect Meter Performance

**Risk Driver:** Performance / Scope

**Cause:** CSD canola oil properties (viscosity, density, temperature effects) not fully specified; affects meter technology suitability and compensation requirements

**Consequence:** Meter technology or compensation scope may change if product properties differ from assumptions

**Product Property Uncertainties:**
- Viscosity: Assumed ~30-70 cP at 20°C; actual viscosity vs. temperature curve TBD
- Density: Assumed ~0.91-0.92 g/cm³ at 15°C; actual density vs. temperature curve TBD
- Temperature range: Operating temperature range TBD; affects viscosity and density
- Vapor pressure: Assumed very low (typical vegetable oil); cavitation risk low

**Meter Technology Sensitivity:**
- Coriolis: Relatively insensitive to viscosity; suitable for wide viscosity range
- Ultrasonic: Good for low-viscosity products; performance degrades at high viscosity
- Turbine: Viscosity-sensitive; requires viscosity correction or limited to narrow viscosity range
- Positive displacement: Suitable for high viscosity; less sensitive to viscosity variation

**Affected Buckets:**
- MAT: Meter technology selection (affects cost per R-001)
- E: Compensation calculations complexity in DEL-12.03
- COM: Calibration across viscosity range

**Suggested Mitigation:**
1. Obtain CSD canola oil product specifications from ER Vol 2 Part 2 or Employer
2. Confirm operating temperature range and product temperature control strategy
3. Evaluate meter technology suitability in DEL-12.02 based on product properties
4. Confirm viscosity and density compensation requirements in DEL-12.03

**Contingency Handling:** Technology contingency (R-001) addresses meter cost variance; product property variance is a technology selection input

---

## Summary

| Risk Count | 17 |
|------------|-----|
| Scope Risks | R-004, R-005, R-011, R-012, R-013 |
| Price Risks | R-001, R-002, R-003, R-006 |
| Schedule Risks | R-007, R-008, R-014, R-016 |
| Performance/Interface Risks | R-015, R-017 |

### Top Risks by Cost Impact

| Rank | Risk | Potential Cost Impact | Mitigation Priority |
|------|------|---------------------|-------------------|
| 1 | R-002: Proving method (in-line vs. portable) | +$200k-300k if in-line provers required | HIGH — Confirm proving method in DEL-12.02 |
| 2 | R-001: Meter technology (Coriolis vs. alternatives) | ±$100k-200k depending on technology | HIGH — Confirm technology in DEL-12.02; obtain quotes |
| 3 | R-003: Meter sizing (flow rate uncertainty) | ±$50k-100k if sizes differ from assumption | HIGH — Obtain design flow rates; size in DEL-12.03 |
| 4 | R-007: Labor productivity (site constraints) | +$50k-100k if productivity factor <1.0 | MEDIUM — Site assessment; logistics planning |
| 5 | R-013: Metering skid structural complexity | ±$40k-80k depending on skid design | MEDIUM — Develop skid GA; coordinate PKG-06 |

### Contingency Allocation Summary

Base estimate: **$1,426,000**

Contingency by CBS: **$366,000 (25.7% overall)**

| CBS | Base | Contingency $ | Contingency % | Risk Coverage |
|-----|------|---------------|---------------|---------------|
| E | $138k | $28k | 20% | Covers scope expansion (R-004) and interface coordination |
| MAT | $717k | $179k | 25% | Covers meter technology variance (R-001), proving method (R-002), sizing (R-003), regulatory (R-006), structural (R-013) |
| CD | $311k | $93k | 30% | Covers productivity variance (R-007), site coordination (R-014), interface scope (R-005) |
| CI | $56k | $17k | 30% | Scales with CD risks |
| PM | $71k | $11k | 15% | Moderate variance expected for factor-based |
| P | $13k | $2k | 15% | Moderate variance for factor-based |
| COM | $120k | $36k | 30% | Covers FAT/SAT scope variance (R-012), proving logistics (R-016), regulatory compliance (R-006) |

**Contingency adequacy:** 25.7% overall contingency is appropriate for:
- 100% allowance-based estimate (no vendor quotes)
- Deliverables in INITIALIZED state (scope immature)
- Technology and proving method not selected (high-value decisions pending)
- Custody transfer precision requirements (OBJ-10)
- Multiple interface packages (scope boundary uncertainties)

**Contingency may be insufficient if:**
- In-line provers required instead of portable prover (+$200k-300k; exceeds contingency buffer)
- Accuracy requirements significantly tighter than ±0.15% (may require in-line provers or higher-grade equipment)
- Significant site constraints reduce productivity factor below 0.8

**Recommendation:** Re-estimate after meter technology, proving method, and design flow rates are confirmed in DEL-12.02 and DEL-12.03.

---

*Risk register prepared per AGENT_ESTIMATING SPEC requirements. Risks identified, mitigation actions recommended, contingency adequacy assessed.*
