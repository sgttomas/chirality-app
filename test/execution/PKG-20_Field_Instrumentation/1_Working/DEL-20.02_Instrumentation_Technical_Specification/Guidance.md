# Guidance: DEL-20.02 Instrumentation Technical Specification

## Purpose

This guidance document supports the development of the **Instrumentation Technical Specification** for **PKG-20 Field Instrumentation** on the Canola Oil Transload Facility Phase 1 project.

**Deliverable Objective:**

Defines performance, materials, and workmanship requirements for instrumentation per ER requirements.

**Source:** Decomposition document `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md`, DEL-20.02 (line 497)

**Deliverable Classification:**
- **Type:** Specification
- **Discipline:** I&C
- **Responsible:** D&B Contractor

**Downstream Use:**

This technical specification will be used by:
- Equipment procurement teams for instrument purchase specifications
- Vendors/manufacturers for equipment quotations and proposal preparation
- Construction contractors for installation workmanship standards
- Quality assurance personnel for inspection and acceptance criteria
- Commissioning engineers for calibration and testing requirements

**Source:** **ASSUMPTION** based on typical specification deliverable lifecycle use

## Principles

### Cross-Document Context

This Guidance document provides the engineering rationale and decision-making context for requirements defined in Specification.md. Key linkages:

- **Specification FR-1 to FR-5 (Functional Requirements)** — Principles below explain why these requirements exist
- **Specification PR-1 to PR-5 (Performance Requirements)** — Considerations section addresses factors affecting performance selection
- **Specification INT-1 to INT-4 (Interface Requirements)** — Trade-offs section explores interface coordination strategies
- **Datasheet Construction section** — Detailed scope and technology options for level, pressure, temperature instruments

See Procedure.md for the step-by-step process to develop and issue these specifications.

### Engineering Rationale (I&C Discipline)

**Principle 1: Specifications Define "What," Not "How"**

A technical specification defines:
- **Performance requirements:** What the instrument must measure (range, accuracy, response time)
- **Material requirements:** What materials are acceptable (corrosion resistance, environmental durability)
- **Workmanship requirements:** What quality standards apply (installation methods, testing protocols)

A technical specification does NOT prescribe:
- Specific vendor products (unless single-source justified)
- Detailed design (that's the vendor's responsibility)
- Installation locations (that's in DEL-20.01 drawings)

**Why this matters:** Performance-based specifications allow:
- Competitive bidding (multiple vendors can propose compliant solutions)
- Innovation (vendors can offer better technologies)
- Design-build flexibility (contractor can optimize based on procurement and construction constraints)

**Source:** **ASSUMPTION** based on EPC specification philosophy and design-build procurement strategy

**Principle 2: Right Instrument for the Application**

Instrument selection is application-driven:
- **Custody transfer metering:** High accuracy (±0.15% typical), certified measurement, audit trail
- **Process control:** Moderate accuracy (±0.5-1%), fast response, reliable repeatability
- **Safety alarms/interlocks:** Fail-safe design, redundancy (if SIL-rated), independent from control
- **Monitoring/indication:** Lower accuracy acceptable (±2-5%), cost-effective

**Source:** **ASSUMPTION** based on ISA 84, API 554, and typical measurement system design hierarchy

Specification must define fit-for-purpose requirements without over-specifying (cost) or under-specifying (performance failure).

**Principle 3: Environmental Durability for Marine Terminal**

Fraser Surrey Terminal is a harsh outdoor coastal environment:
- **Corrosion:** Salt air accelerates corrosion of carbon steel, aluminum, and even stainless steel (pitting)
- **Temperature cycling:** Daily and seasonal temperature variations cause thermal stress and condensation
- **UV exposure:** Plastics and coatings degrade over time from sunlight
- **Rain intrusion:** Water ingress into enclosures causes electrical failures

Specification must require:
- Marine-grade materials (316 stainless steel, marine aluminum, epoxy coatings)
- Weatherproof enclosures (NEMA 4X / IP66 minimum with drain provisions)
- UV-resistant components (cables, gaskets, windows)
- Condensation management (heaters, drain holes, desiccants where applicable)

**Source:** Project location (Fraser Surrey Terminal, BC coast); **ASSUMPTION** based on typical marine terminal environmental design requirements

**Principle 4: Hazardous Area Safety**

Canola oil is combustible (flash point typically >200°C):
- **Hazardous area classification:** Likely Class I, Division 2 or Zone 2 in areas with potential vapor release (tank roofs, pump seals, loading arms)
- **Electrical safety:** Instruments in hazardous areas must be certified for explosive atmospheres (CSA/UL)
- **Installation integrity:** Field wiring, conduit seals, and cable glands must maintain electrical protection

Specification must define:
- Certification requirements (CSA Class I, Div 2 or IECEx Zone 2)
- Protection method (intrinsically safe, explosion-proof, non-incendive)
- Temperature class (T3 or T4 typical for canola oil)
- Installation workmanship per CSA C22.1 Section 18

**Source:** CSA C22.1; **ASSUMPTION** based on canola oil properties; **TBD**: Facility-specific hazardous area classification

**Principle 5: Lifecycle Cost vs. Capital Cost**

Instrument selection involves cost trade-offs:
- **Capital cost:** Purchase price (dominates initial project budget)
- **Installation cost:** Labor and materials for field installation
- **Calibration cost:** Initial calibration and periodic recalibration over facility life
- **Maintenance cost:** Spare parts, repairs, wear item replacement
- **Downtime cost:** Lost revenue during instrument failures

OBJ-9 (Lifecycle Cost Optimization) requires considering total cost of ownership, not just purchase price.

**Examples:**
- Radar level transmitters: Higher capital cost, but no moving parts (lower maintenance)
- Float-and-tape gauges: Lower capital cost, but require periodic wire replacement and calibration
- Redundant instruments: Higher capital cost, but reduced downtime risk for critical measurements

**Source:** Decomposition Section 2, OBJ-9 (line 66); **ASSUMPTION** based on typical lifecycle cost analysis

### Applicable Standards Context

**ISA 5.1 — Instrumentation Symbols and Identification**
- Defines instrument tagging conventions (tag numbers, function codes)
- **Application:** Ensures consistent identification across P&IDs, specifications, data sheets, drawings

**ISA 84 / IEC 61511 — Functional Safety**
- Governs design of safety instrumented systems (SIS) and safety instrumented functions (SIF)
- **Application:** If overfill protection or emergency shutdown functions are safety-rated (SIL 1/2/3)
- **Key concept:** Safety instruments must be independent, fail-safe, and verified for target SIL

**API 554 — Process Instrumentation and Control**
- Oil and gas industry standard for instrumentation good practice
- Covers instrument selection, installation, calibration, maintenance
- **Application:** Good practice reference for bulk liquid terminal (canola oil is similar to petroleum products in handling)

**API 2350 — Overfill Protection for Storage Tanks**
- Specifies requirements for independent overfill protection systems
- **Application:** 3 × 15,000 MT tanks require overfill prevention (regulatory and safety requirement)
- **Key requirement:** Independent high level alarm and automatic shutdown (separate from process control)

**CSA C22.1 — Canadian Electrical Code**
- Governs electrical installations in Canada (BC jurisdiction)
- Section 18: Hazardous locations (explosive atmospheres)
- **Application:** Mandatory compliance for instrumentation wiring and equipment in hazardous areas

**Source:** Standards list from Datasheet.md and Specification.md; applicability based on **ASSUMPTION** of typical I&C practice and Canadian regulatory context

## Considerations

### Project-Specific Considerations

**Facility Type: Canola Oil Transload**

CSD canola oil characteristics affect instrumentation specification:
- **Viscosity:** Temperature-dependent (thick when cold, thin when warm) — affects level measurement technology (radar preferred over ultrasonic)
- **Vapor pressure:** Low vapor pressure (minimal vapor space) — affects hazardous area classification extent
- **Density:** Approximately 0.92 kg/L — affects level-to-volume conversion and tank gauging accuracy
- **Conductivity:** Non-conductive (dielectric) — guided wave radar requires coaxial probe (not single rod)
- **Food-grade product:** Wetted materials must be food-grade compatible (stainless steel, not carbon steel)

**Source:** **ASSUMPTION** based on canola oil properties; **TBD**: Specific product data from Employer's Requirements or process design

**Throughput and Storage Scale**

- **1,000,000 MT/annum throughput:** High-volume operations require reliable, low-maintenance instruments
- **32 railcar unloading stations:** Large number of unloading points requires standardization (reduce spare parts inventory)
- **3 × 15,000 MT storage tanks:** Large tanks (approximately 16,000 m³ each) require accurate level measurement for inventory and overfill protection

**Source:** Decomposition Section 1.1 Key Parameters (lines 38-44)

**Design-Build Delivery**

- Contractor has flexibility to select instrument vendors and technologies (within specification limits)
- Early procurement may be advantageous (long-lead instruments for custody transfer metering)
- Standardization across similar applications reduces engineering effort and construction/commissioning efficiency

**Source:** Decomposition project type "Design & Build" (line 4); **ASSUMPTION** based on typical D&B execution

### Technical Considerations (By Instrument Type)

**Level Instruments**

**Technology Selection Factors:**
- **Radar (non-contact):** Best for viscous fluids, independent of product properties, no moving parts (low maintenance) — higher cost
- **Guided wave radar (contact):** Reliable, good for interface detection, unaffected by vapor/foam — requires clean product (canola oil is suitable)
- **Float-and-tape:** Mechanical simplicity, visual indication — requires periodic maintenance (wire replacement)
- **Ultrasonic (non-contact):** Lower cost — not suitable for viscous fluids or temperature variations (speed of sound changes)
- **Level switches:** Float, tuning fork, capacitance, or vibrating rod for alarm points — simple, reliable, cost-effective

**Accuracy Considerations:**
- **Tank gauging:** ±3 mm typical for custody transfer / inventory accuracy
- **Process control:** ±1-2% of span adequate for pump control
- **Alarm/interlock:** Repeatability more important than absolute accuracy

**Source:** **ASSUMPTION** based on ISA, API, and typical level measurement technology characteristics

**Pressure Instruments**

**Technology Selection Factors:**
- **Pressure transmitters (4-20 mA + HART):** Industry standard for process control and monitoring
- **Differential pressure transmitters:** Used for filter monitoring, flow measurement (orifice plate), pump performance
- **Pressure gauges (local):** Visual indication for field operators, mechanical backup — require isolation valve for replacement
- **Pressure switches:** Simple on/off output for alarms/interlocks — mechanical or electronic

**Accuracy Considerations:**
- **Process control:** ±0.5% of span typical
- **Safety alarms:** ±1% acceptable if setpoints have adequate margin
- **Custody transfer (if pressure-based flow):** ±0.25% or better (coordinate with PKG-12 metering)

**Range Selection:**
- Select range to keep normal operating point at 30-70% of span (optimal transmitter accuracy)
- Overpressure rating should be ≥ 2× range or piping system MAWP (whichever is greater)

**Source:** **ASSUMPTION** based on ISA, API 554, and typical pressure measurement practice

**Temperature Instruments**

**Technology Selection Factors:**
- **RTDs (Pt100 / Pt1000):** High accuracy (±0.1-0.5°C), stable over time, good for product temperature monitoring
- **Thermocouples (K-type typical):** Lower accuracy (±1-2°C), faster response, suitable for equipment protection (bearing temperature)
- **Thermistors:** High sensitivity, narrow range — niche applications
- **Temperature switches:** Mechanical (bimetal) or electronic for alarm points

**Thermowell Considerations:**
- Required for process immersion (allows element replacement without process shutdown)
- Material: 316 stainless steel typical for canola oil service
- Wake frequency calculation required for high-velocity piping (per ASME PTC 19.3)
- Insertion length: 1/3 pipe diameter typical (trade-off between response time and structural stress)

**Source:** **ASSUMPTION** based on ISA, ASME PTC 19.3, and typical temperature measurement practice

### Coordination Considerations

**Process Engineering Coordination**

Specification must align with:
- P&IDs (instrument tag numbers, function codes, service descriptions)
- Process data sheets (operating pressures, temperatures, flow rates — defines instrument ranges)
- Control philosophy (control loop requirements — defines transmitter accuracy and response time)

**Procurement Coordination**

Specification must support:
- Competitive bidding (multiple vendors can meet specification)
- Data sheet templates (DEL-20.04) that match specification requirements
- Vendor quote evaluation (specification provides acceptance criteria)

**Construction Coordination**

Specification workmanship requirements must be:
- Constructible (field contractors can execute)
- Verifiable (inspection and testing can confirm compliance)
- Consistent with other specifications (piping, electrical, structural)

**Source:** **ASSUMPTION** based on typical EPC coordination workflow

### Quality and Verification Considerations

**Design Verification**

- Calculations (DEL-20.03) verify instrument ranges, accuracies, and sizing are adequate for application
- Independent check ensures specification is technically correct and complete

**Procurement Verification**

- Vendor data sheets (DEL-20.04) are reviewed against specification (bid evaluation and shop drawing review)
- Factory acceptance testing (FAT) may be required for complex or critical instruments (custody transfer meters)

**Installation Verification**

- QA/QC inspection verifies field installation per specification workmanship requirements
- Site acceptance testing (SAT) verifies instrument calibration and performance (DEL-20.05 records)

**Source:** **ASSUMPTION** based on typical EPC quality assurance workflow; cross-references to other PKG-20 deliverables

## Trade-offs

### Technology Trade-offs

**Trade-off 1: Contact vs. Non-Contact Level Measurement**

| Aspect | Contact (Guided Wave Radar, Float) | Non-Contact (Radar, Ultrasonic) |
|--------|-------------------------------------|----------------------------------|
| Installation | Requires tank penetration | Mounts on nozzle or flange (cleaner installation) |
| Maintenance | In-tank maintenance (tank outage) | External maintenance (no tank entry) |
| Product buildup | Probe coating can affect performance (canola oil is clean — low risk) | No coating issues |
| Vapor/foam | Unaffected (probe penetrates) | Radar unaffected; ultrasonic struggles with foam |
| Accuracy | Excellent (±3 mm typical) | Radar excellent; ultrasonic moderate |
| Cost | Moderate | Radar higher; ultrasonic lower |

**Recommendation:** Radar preferred for large storage tanks (3 × 15,000 MT) for maintenance-free operation and accuracy; guided wave radar acceptable for process vessels; float-and-tape as mechanical backup for tanks.

**Source:** **ASSUMPTION** based on typical level measurement technology comparison and canola oil application

**Trade-off 2: Intrinsically Safe vs. Explosion-Proof**

| Aspect | Intrinsically Safe (IS) | Explosion-Proof (XP) |
|--------|-------------------------|----------------------|
| Field device cost | Lower (simple device) | Higher (certified enclosure) |
| Control room cost | Higher (IS barriers, isolated power supplies) | Lower (standard wiring) |
| Wiring complexity | Higher (cable separation, grounding, capacitance limits) | Lower (standard cable) |
| Flexibility | Limited (energy limits restrict device types) | Higher (most devices compatible) |
| Typical use | Large populations of simple sensors (transmitters, switches) | Complex devices (analyzers, cameras) |

**Recommendation:** IS preferred for field transmitters and switches (large population in PKG-20); XP for complex devices if needed.

**Source:** **ASSUMPTION** based on CSA C22.1 and typical hazardous area design strategies

### Performance vs. Cost Trade-offs

**Trade-off 3: Accuracy vs. Cost**

Higher accuracy instruments cost more (purchase, calibration, maintenance):
- **Custody transfer:** High accuracy required (regulatory, commercial) — cost justified
- **Process control:** Moderate accuracy adequate — balance cost vs. control performance
- **Monitoring/indication:** Lower accuracy acceptable — minimize cost

**Recommendation:** Specify fit-for-purpose accuracy (don't over-specify). Use DEL-20.03 calculations to verify adequacy.

**Trade-off 4: Redundancy vs. Availability**

Single instruments are lower cost but create single-point failure risk:
- **Critical measurements:** Redundancy may be justified (tank overfill protection, emergency shutdown)
- **Non-critical measurements:** Single instrument with spare parts inventory is cost-effective

**Recommendation:** **TBD** — Criticality assessment and redundancy strategy per Employer's Requirements and safety analysis. OBJ-1 (Safe & Reliable Operation) may justify redundancy for critical instruments.

**Source:** Decomposition OBJ-1 (line 58)

### Specification Detail Trade-offs

**Trade-off 5: Prescriptive vs. Performance-Based**

| Aspect | Prescriptive (Brand/Model Specified) | Performance-Based (Requirements Only) |
|--------|---------------------------------------|---------------------------------------|
| Vendor competition | Limited (single source or "or equal") | Open (multiple vendors can bid) |
| Engineering control | High (known solution) | Lower (vendor proposes solution) |
| Innovation | Limited (locked to specified product) | Higher (vendors offer latest technology) |
| Risk | Lower (proven solution) | Higher (unproven vendor solutions) |
| Typical use | Proven applications, Owner preference | Competitive procurement, cost optimization |

**Recommendation:** Performance-based preferred for Design & Build (contractor flexibility, competitive procurement); prescriptive only if Employer has strong preference or proven solution requirement.

**Source:** **ASSUMPTION** based on design-build procurement philosophy

**Trade-off 6: Detail Level**

Specification detail level affects engineering effort and flexibility:
- **Highly detailed:** More engineering effort, prescriptive requirements, less contractor flexibility
- **Less detailed:** Faster engineering, more contractor responsibility for detailed design, requires robust acceptance criteria

**Recommendation:** Balance appropriate to deliverable maturity. For IFC (Issued for Construction), sufficient detail for procurement and installation; avoid excessive detail that constrains contractor unnecessarily.

**Source:** **ASSUMPTION** based on typical EPC specification philosophy for design-build projects

## Examples

### Reference Examples and Precedents

**Industry Precedents:**

Similar instrumentation applications:
- Vegetable oil terminals (soybean oil, palm oil, canola oil)
- Petroleum product terminals (similar handling, different hazardous area extent)
- Chemical bulk liquid terminals (instrumentation technologies overlap)

**TBD** — Specific precedent project references to be identified and reviewed for lessons learned.

**Source:** **ASSUMPTION** — Typical approach for EPC projects to leverage industry precedents

### Specification Content Examples

**Example 1: Level Transmitter Performance Requirement**

```
Level transmitters for storage tank service shall meet the following performance requirements:
- Measurement range: 0 to [TBD] meters (tank height)
- Accuracy: ±3 mm or ±0.01% of range, whichever is greater
- Repeatability: ±1 mm
- Operating temperature: -30°C to +60°C ambient; -10°C to +80°C process
- Output: 4-20 mA with HART digital communication
- Update rate: 1 second maximum
- Tank penetration: Top-mounted via 6" or 8" nozzle (coordinate with tank design)
```

**Example 2: Material Requirement**

```
Wetted parts for instruments in canola oil service shall be constructed of:
- 316 or 316L stainless steel (ASTM A316 or equivalent)
- Hastelloy C (for superior corrosion resistance, if specified)
- Acceptable elastomers: PTFE, EPDM, Viton (food-grade)
- NOT acceptable: Carbon steel, brass, aluminum (wetted parts)
```

**Example 3: Workmanship Requirement**

```
Instrument installation shall comply with the following workmanship requirements:
- Impulse piping shall be sloped 1:12 minimum (rising to transmitter for gas service, falling to transmitter for liquid service)
- Impulse piping supports shall be provided at 1.5 m intervals maximum
- Block-and-bleed valves shall be provided for pressure transmitter isolation and calibration
- Condensate pots or vapor traps shall be provided where process conditions create condensation or vaporization in impulse lines
- Installation shall comply with manufacturer recommendations and API 554 good practice
```

**Source:** **ASSUMPTION** based on typical specification language and ISA/API instrumentation installation practices

### Project-Specific Examples

**Anticipated Specification Applications:**

**Storage Tanks (3 × 15,000 MT)**

Level instrumentation specification shall address:
- **Primary level:** Radar level transmitter (continuous measurement for inventory and control)
- **Backup level:** Float-and-tape gauge (mechanical, local indication)
- **High level alarm:** Independent radar level switch or second transmitter (API 2350 overfill protection)
- **Temperature:** Multi-point RTDs (stratification monitoring, viscosity correlation)

**Railcar Unloading (32 Stations)**

Instrumentation specification shall address:
- **Unloading pit level:** Level switches (high level alarm, pump interlock)
- **Flow indication:** Flow transmitters or switches (verification of unloading flow)
- **Pressure monitoring:** Pressure transmitters on unloading headers (pump performance, system pressure)

**Marine Loading**

Instrumentation specification shall address:
- **Loading arm pressure:** Pressure transmitters (loading rate control, high pressure alarm)
- **Loading arm position:** Position switches (arm movement interlock)
- **Product temperature:** RTD (custody transfer temperature correction)

**Source:** **ASSUMPTION** based on facility scope (decomposition Key Parameters lines 38-44) and typical bulk liquid terminal instrumentation applications

### Lessons Learned (Typical Issues)

**Issue 1: Over-Specification**

Problem: Specifying tighter accuracy than required increases cost unnecessarily
Solution: Use DEL-20.03 calculations to verify fit-for-purpose accuracy; specify only what's needed

**Issue 2: Inadequate Environmental Rating**

Problem: Indoor-rated instruments installed outdoors fail prematurely from weather exposure
Solution: Specify NEMA 4X / IP66 minimum for all outdoor instruments; require corrosion-resistant materials for coastal environment

**Issue 3: Incompatible Hazardous Area Certification**

Problem: Instruments certified to European standards (ATEX) may not be acceptable in Canada (CSA required)
Solution: Specify CSA or UL certification explicitly; verify vendor certification during data sheet review (DEL-20.04)

**Issue 4: Specification vs. Data Sheet Mismatch**

Problem: Vendor data sheets don't clearly demonstrate specification compliance (difficult bid evaluation)
Solution: Coordinate specification requirements with data sheet templates (DEL-20.04) to ensure vendor submittals address all requirements

**Source:** **ASSUMPTION** based on typical instrumentation specification and procurement lessons learned

## Project Objective Alignment

This deliverable supports the following project objectives:

**OBJ-1: Safe & Reliable Operation**

Proper specification of instrument performance, materials, and workmanship ensures:
- Accurate measurement for process control and safety
- Reliable equipment suitable for marine terminal environment
- Compliance with electrical codes and safety standards (hazardous areas)

**Source:** Decomposition Section 6 Objective-to-Deliverable Mapping — PKG-20 supports OBJ-1 (line 780)

**Secondary Objective Support:**

- **OBJ-6: Regulatory Compliance** — Specifications ensure compliance with CSA C22.1 (electrical code), API 2350 (overfill protection), and other regulatory requirements
- **OBJ-9: Lifecycle Cost Optimization** — Fit-for-purpose specifications balance capital cost with maintenance cost and reliability (total cost of ownership)
- **OBJ-10: Custody Transfer Accuracy** — Specifications support accurate product metering (coordinate with PKG-12 metering systems)

**Source:** **ASSUMPTION** based on instrumentation specification's role in facility safety, compliance, cost optimization, and commercial accountability

## Cross-Document Traceability

This Guidance document provides engineering rationale and decision context for DEL-20.02. The following documents provide complementary information:

| Document | Purpose | Key Linkages |
|----------|---------|--------------|
| Datasheet.md | Factual identification, attributes, conditions, references | Conditions § provides project context for Principles; Construction § details instrument types for Technical Considerations |
| Specification.md | Requirements and verification criteria | FR-1 to FR-5 implement Principles; PR-1 to PR-5 implement Performance Considerations; Standards § implements Standards Context |
| Procedure.md | Production workflow and verification steps | Steps 1-5 implement Principles and Considerations; Verification implements Quality Considerations |

**Guidance-to-Specification Mapping:**

| Guidance Section | Specification Section | Rationale Provided |
|------------------|----------------------|-------------------|
| Principle 1 | Scope | Specifications define "what" not "how" |
| Principle 2 | FR-1 | Right instrument for application |
| Principle 3 | PR-2 | Environmental durability for marine terminal |
| Principle 4 | PR-3 | Hazardous area safety requirements |
| Principle 5 | PR-5 | Lifecycle cost vs. capital cost |
| Trade-off 1 | FR-2 | Contact vs. non-contact level measurement |
| Trade-off 2 | PR-3 | Intrinsically safe vs. explosion-proof |
| Trade-off 3-4 | PR-1 | Accuracy vs. cost and redundancy decisions |
| Trade-off 5-6 | Scope | Prescriptive vs. performance-based specifications |
| Level Instruments | FR-2 | Level technology selection factors |
| Pressure Instruments | FR-3 | Pressure technology selection factors |
| Temperature Instruments | FR-4 | Temperature technology selection factors |
