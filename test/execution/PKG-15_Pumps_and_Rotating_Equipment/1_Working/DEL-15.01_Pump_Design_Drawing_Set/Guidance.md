# Guidance: DEL-15.01 Pump Design Drawing Set

## Purpose

This guidance document supports the development of the **Pump Design Drawing Set** for **PKG-15 Pumps & Rotating Equipment** within the Canola Oil Transload Facility project.

**Deliverable purpose:** Defines the design arrangement and details for pumps per ER requirements.

**Source:** `_CONTEXT.md` (description), decomposition DEL-15.01 entry

### Role in Project Delivery

The Pump Design Drawing Set serves as:

1. **Foundation for procurement** — Provides arrangement and interface data for equipment procurement (supports DEL-15.04 Data Sheet Package)
2. **Basis for construction** — Defines installation requirements for foundation work (PKG-05), structural supports (PKG-06), and piping interfaces (DEL-14.01)
3. **Coordination tool** — Ensures interdisciplinary alignment between mechanical, structural, electrical, and I&C disciplines
4. **Verification baseline** — Provides as-designed reference for installation verification (DEL-15.05)

**Source:** Standard engineering documentation hierarchy and purpose

### Contribution to Project Objectives

This deliverable directly supports:

- **OBJ-1 (Safe & Reliable Operation):** Proper pump arrangement, access, and clearances ensure safe operation and maintenance
- **OBJ-2 (Throughput Capacity):** Correct pump sizing and arrangement enable 1,000,000 MT/annum facility throughput
- **OBJ-4 (Operational Flexibility):** Pump configuration supports both tank storage and direct rail-to-ship transfer modes
- **OBJ-7 (Environmental Protection):** Drawing coordination with containment systems ensures spill prevention and leak detection
- **OBJ-9 (Lifecycle Cost Optimization):** Proper access and maintainability provisions reduce future maintenance costs

**Source:** Decomposition Section 2 (Objectives), Section 6 (Objective-Deliverable Mapping for PKG-15)

## Principles

### Engineering Rationale for Pump Design Drawings

#### Principle 1: Equipment-Centric Design Coordination

Pump design drawings serve as the central coordination point between:

- **Equipment design** (internal to pump vendor) ← **boundary** → **Installation design** (Contractor responsibility)
- Pump arrangement drawings bridge vendor-supplied outline drawings with site-specific installation requirements
- Foundation and piping interface drawings translate vendor nozzle data into constructible details

**Source:** Standard EPC engineering practice; API 610 Section 6 (installation) defines Contractor installation responsibilities separate from vendor equipment design

#### Principle 2: "Design for Maintainability"

Per API 610 Section 6.1.1, adequate clearances must be provided for:

- Coupling removal and replacement
- Impeller extraction
- Seal maintenance and replacement
- Instrument calibration and replacement
- Lubrication system service

**Typical clearances:**
- **Coupling end:** Minimum 1.5× coupling length for spacer removal
- **Seal area:** Adequate access for seal cartridge removal (typically 0.5m minimum)
- **Instrument connections:** Clear access for technician with tools (0.75m typical)
- **All-around clearance:** Minimum 1.0m for general access and egress

**Source:** API 610 Section 6.1.1 (installation clearances); ASME B30.20 (rigging clearances); WorkSafeBC (safe access requirements)

**Trade-off:** Increased clearances improve maintainability but increase plot space requirements and potential piping run lengths (impacting NPSH and capital cost)

#### Principle 3: Foundation Design Independence

API 610 Section 6.1 requires:

- Foundations designed for pump and driver loads plus dynamic loads (vibration, seismic, thermal)
- Foundation natural frequency ≥ 2× pump operating frequency (to avoid resonance)
- Foundation mass typically 3–5× equipment mass (rule of thumb for dynamic isolation)

Foundation drawings must show:

- Anchor bolt embedment and spacing per ACI 318 / CSA A23.3
- Grout pad thickness (typical: 25–75mm) for alignment adjustment
- Concrete strength (typical: 25–35 MPa for pump foundations)

**Source:** API 610 Section 6.1.4 (foundations and grouting); ACI 351.3R (Foundations for Dynamic Equipment)

#### Principle 4: Piping Interface Load Management

Per API 610 Section 4.2.9 and Section 6.2:

- Piping loads on pump nozzles must not exceed vendor-specified allowable loads
- Piping must be independently supported — **piping weight and thermal expansion shall not be carried by the pump**
- First piping support typically located within 1–2 pipe diameters from pump nozzle
- Expansion loops or flexible joints may be required for thermal growth accommodation

**Common failure mode:** Excessive piping loads cause shaft misalignment, bearing overload, and seal failure

**Source:** API 610 Section 4.2.9 (nozzle loads), Section 6.2 (piping installation); ASME B31.3 (piping flexibility analysis)

#### Principle 5: Seismic and Vibration Considerations

For seismic zones (NBC 2015 applies in BC):

- Anchor bolts must resist both static and seismic overturning moments
- Flexible piping connections near pump may be required (but must not compromise piping support independence)
- Elevated pumps require additional seismic bracing of support structures

For vibration control (API 610 Section 6.9):

- Pump operating speeds typically 1,000–3,600 RPM (50/60 Hz motor-driven)
- Foundation natural frequency must avoid resonance with operating frequency and harmonics
- Vibration acceptance criteria per ISO 10816 or API 610 Figure 15

**Source:** API 610 Section 6.9 (vibration); NBC 2015 (seismic design); ISO 10816 (vibration severity)

### Applicable Standards Context

#### API 610 — Centrifugal Pumps for Petroleum, Petrochemical and Natural Gas Industries

**Scope:** Covers minimum requirements for centrifugal pumps for use in petroleum, heavy-duty chemical, and gas industry services.

**Relevant sections for drawing development:**
- **Section 4:** Design requirements (nozzles, baseplates, couplings)
- **Section 5:** Materials and welding
- **Section 6:** Installation, operation, and testing

**Application to canola oil service:** API 610 applies directly; canola oil is a low-viscosity, non-corrosive hydrocarbon service (similar to light petroleum products). Material selection for food-grade service may require additional considerations (consult ER Part 2).

**Source:** API 610 scope and application

#### ASME B31.3 — Process Piping

**Relevance:** Governs piping interface requirements, including:
- Flange ratings and material selection
- Allowable piping loads on equipment nozzles (coordinate with API 610 Section 4.2.9)
- Piping flexibility analysis requirements

**Source:** ASME B31.3 scope

#### NBC 2015 and CSA A23.3 — Structural and Foundation Design

**Relevance:** Governs foundation design for seismic and gravity loads in British Columbia.

**Key requirements:**
- Seismic design per NBC 2015 (site class, seismic hazard, importance factor)
- Concrete design per CSA A23.3 (strength, reinforcement, durability)
- Anchor bolt design per CAN/CSA-S6 or ACI 318 Appendix D

**Source:** NBC 2015, CSA A23.3 (applicable codes for BC)

## Considerations

### Factors to Consider During Drawing Development

#### Site and Layout Constraints

1. **Plot space availability**
   - Fraser Surrey Terminal is an active operating terminal (OBJ-5: minimize disturbance)
   - Pump locations constrained by existing infrastructure, tankage, and marine loading facilities
   - Underground utilities and existing foundations may limit equipment placement
   - **Action:** Coordinate with site survey, civil drawings (PKG-01–PKG-04), and existing facility as-builts

2. **Access and egress**
   - WorkSafeBC requires safe access to all equipment requiring maintenance
   - Consider: walkways, platforms, ladders, guardrails (coordinate with PKG-06 structural steel)
   - Elevated pumps require fall protection and safe access provisions
   - **Action:** Ensure 1.0m minimum clearance for egress; 0.75m for routine access

3. **Environmental exposure**
   - Coastal/marine environment (Fraser River terminal location)
   - Consider: corrosion protection (coatings, material upgrade), weather protection (rain shields for motors)
   - Drainage provisions to prevent standing water around pumps (coordinate with PKG-03)
   - **Action:** Coordinate with PKG-32 Coatings and PKG-33 Corrosion Protection

**Source:** OBJ-5 (terminal continuity), WorkSafeBC regulations, site conditions (decomposition Section 1)

#### Pump Service-Specific Considerations

1. **Railcar unloading pumps**
   - Located near railcar unloading stations (32 stations per project context)
   - May require multiple pumps or duty/standby configuration for reliability
   - Suction from railcar; discharge to storage tanks or marine loading system
   - NPSH consideration: Railcar liquid level varies during unloading (affects available NPSH)
   - **Action:** Coordinate pump location with DEL-10.01 (Railcar Unloading System Design) and DEL-15.03 (NPSH calculations)

2. **Marine loading pumps**
   - Located near marine loading arms (Berth 10 area)
   - Suction from storage tanks; discharge to marine loading arms
   - High flow rate and pressure for efficient ship loading
   - Redundancy for operational flexibility (OBJ-4)
   - **Action:** Coordinate with DEL-11.01–11.06 (Marine Loading System) and DEL-08 (Marine Structures)

3. **Sump pumps**
   - Located at low points in containment areas and sumps
   - Service: spill recovery, rainwater drainage, leak collection
   - Supports OBJ-7 (Environmental Protection)
   - May require explosion-proof motors if located in hazardous areas
   - **Action:** Coordinate with PKG-03 (Drainage), hazardous area classification study, and environmental requirements

4. **Transfer pumps (if applicable)**
   - Tank-to-tank transfer or recirculation service
   - Lower duty cycle than unloading/loading pumps
   - May share piping infrastructure with other pump systems
   - **Action:** Confirm requirements from process design and DEL-12 (Product Transfer & Metering)

**Source:** DEL-15.02 anticipated artifacts (pump types); project objectives; typical pump service characteristics

#### Interdisciplinary Coordination Requirements

| Discipline | Coordination Item | Timing |
|------------|-------------------|--------|
| **Process (PKG-10, 11, 12)** | Flow rates, pressures, system curves, NPSH available | Early (basis of design) |
| **Civil (PKG-03, 04, 05)** | Foundation locations, anchor bolt embedment, grout pad details | Mid (detailed design) |
| **Structural (PKG-06)** | Support steel for elevated pumps, platform access, stairs/ladders | Mid (detailed design) |
| **Piping (PKG-14)** | Nozzle loads, piping routing, support locations, thermal expansion | Continuous (iterative) |
| **Electrical (PKG-19, 20)** | Motor sizes, power supply routing, conduit entries, control interfaces | Mid (detailed design) |
| **I&C (PKG-29, 30)** | Instrument connections, transmitter mounting, local indication | Late (detailed design) |
| **Coatings (PKG-32)** | Surface preparation, coating systems for corrosion protection | Late (detailed design) |

**Source:** Standard interdisciplinary coordination requirements; dependencies inferred from typical pump installation scope

**Coordination mechanism:** `_DEPENDENCIES.md` indicates NOT_TRACKED — formal coordination managed by humans via project coordination meetings, IDC reviews, and model coordination (if 3D model used).

#### Constructability Factors

1. **Installation sequence**
   - Typical sequence: Foundation → Anchor bolt installation → Baseplate set and level → Grout → Equipment set → Alignment → Piping tie-in
   - Consider: Foundation curing time (minimum 7 days before equipment set), grouting sequence
   - **Action:** Ensure foundation drawings show adequate anchor bolt sleeves for adjustment; grout access provisions

2. **Equipment delivery and rigging**
   - Large pumps may require crane access for installation
   - Consider: laydown area, rigging path, overhead obstructions
   - Lifting lugs on pump/motor must be adequate for rigging loads (coordinate with vendor)
   - **Action:** Show rigging clearances on arrangement drawings; confirm site access with construction team

3. **Modularization potential**
   - Some pumps may be pre-assembled on baseplates with piping spool pieces (off-site assembly)
   - Reduces field labor and weather exposure; improves quality control
   - **Trade-off:** Larger modules require heavier rigging and may limit installation window
   - **Action:** Evaluate modularization feasibility with construction and vendor input

**Source:** Typical construction sequencing and best practices; API 610 Section 6 (installation procedures)

#### Operability and Maintainability Factors

1. **Routine maintenance access**
   - Lubrication points must be accessible from grade or platform (no ladders for routine tasks)
   - Instrument valves and sample points accessible for operators
   - Seal flush connections and drain points at safe, accessible locations
   - **Action:** Show access clearances per API 610 Section 6.1.1; coordinate with O&M manuals (DEL-27.04)

2. **Major maintenance requirements**
   - Impeller/seal replacement typically requires pump disassembly (coupling removal, bearing housing separation)
   - Motor removal may require overhead lifting or equipment relocation
   - Consider: permanent davit or monorail for heavy component lifting (coordinate with PKG-06)
   - **Action:** Ensure coupling end clearance ≥ 1.5× coupling length; show laydown space for disassembled components

3. **Spare parts strategy**
   - Standardization of pump models reduces spare parts inventory
   - Common baseplates and foundation designs reduce engineering/construction effort for future additions (OBJ-8: expandability)
   - **Trade-off:** Standardization may not optimize each pump for specific duty (cost vs. performance)
   - **Action:** Coordinate with procurement and O&M planning (DEL-27.05 Maintenance Plan)

**Source:** API 610 Section 6.1.1 (maintenance clearances); OBJ-9 (lifecycle cost optimization)

## Trade-offs

### Competing Concerns to Evaluate

#### Trade-off 1: Horizontal vs. Vertical Pump Configuration

| Factor | Horizontal Pump | Vertical Pump |
|--------|-----------------|---------------|
| **Footprint** | Larger (motor and pump on same level) | Smaller (motor above pump) |
| **NPSH available** | Requires adequate suction head | Can use sump configuration (better NPSH) |
| **Maintenance** | Easier coupling/seal access (grade level) | More difficult (elevated motor) |
| **Cost** | Typically lower capital cost | Higher capital cost |
| **Seismic** | Lower center of gravity (better seismic) | Higher center of gravity (more seismic load) |

**Guidance:** Horizontal configuration preferred for most process pumps unless NPSH is severely limited or plot space is constrained.

**Source:** API 610 (covers both configurations); industry practice

#### Trade-off 2: Individual Foundations vs. Common Baseplate

| Factor | Individual Foundations | Common Baseplate/Skid |
|--------|------------------------|----------------------|
| **Flexibility** | Each pump independently located and aligned | Pumps pre-aligned on common baseplate |
| **Field labor** | Higher (individual alignment and grouting) | Lower (pre-aligned, single grout operation) |
| **Constructability** | Slower (sequential installation) | Faster (modular installation) |
| **Vibration isolation** | Better (independent foundations) | Potentially worse (shared foundation transmits vibration) |
| **Cost** | Lower material cost; higher labor cost | Higher material cost; lower labor cost |

**Guidance:** Common baseplate preferred for small pumps in close proximity (e.g., duty/standby pairs); individual foundations preferred for large pumps or when vibration isolation is critical.

**Source:** API 610 Section 6.1 (foundation design); modular construction best practices

#### Trade-off 3: Indoor vs. Outdoor Installation

| Factor | Indoor (Enclosed Building) | Outdoor (Weather-Exposed) |
|--------|---------------------------|--------------------------|
| **Environmental protection** | Protected from rain, snow, corrosion | Exposed to weather; requires weatherproof motors and corrosion protection |
| **Ventilation** | Requires building HVAC for heat removal | Natural ventilation |
| **Noise control** | Easier to implement building insulation | Requires individual equipment silencing |
| **Capital cost** | Higher (building cost) | Lower (no building) |
| **Maintenance comfort** | Better for O&M personnel (weather-protected) | Worse (exposed to elements) |

**Guidance:** Outdoor installation typical for industrial facilities unless specific requirements dictate indoor (e.g., freeze protection, noise limits, hazardous area ventilation).

**Source:** API 610 (applies to both); project climate and site conditions

**Project context:** Fraser Surrey Terminal, BC — mild coastal climate suggests outdoor installation feasible with appropriate corrosion protection (coordinate with PKG-32 Coatings).

#### Trade-off 4: Fixed-Speed vs. Variable-Speed Pumps

| Factor | Fixed-Speed (Direct Motor) | Variable-Speed (VFD-Controlled) |
|--------|---------------------------|--------------------------------|
| **Operational flexibility** | Limited (throttle valve control only) | High (flow control via speed) |
| **Energy efficiency** | Lower (throttling losses at low flow) | Higher (reduced speed = reduced power) |
| **Capital cost** | Lower (no VFD) | Higher (VFD cost) |
| **Reliability** | Higher (simpler system) | Lower (VFD adds failure mode) |
| **Electrical infrastructure** | Simpler (direct motor starter) | More complex (VFD, harmonics, cabling) |

**Guidance:** VFD justification depends on:
- Operating profile (frequent flow variation favors VFD)
- Energy cost and operating hours (high utilization favors VFD)
- Operational flexibility needs (OBJ-4 may favor VFD for marine loading/railcar unloading variable rates)

**Decision:** **TBD** — Requires operating profile analysis and lifecycle cost evaluation (coordinate with Electrical and Process disciplines).

**Source:** Industry practice; OBJ-9 (lifecycle cost optimization)

## Examples

### Reference Examples and Precedents

#### Example 1: Typical Horizontal Centrifugal Pump Arrangement

**Configuration:**
- Horizontal, single-stage, end-suction centrifugal pump
- Motor: 75 kW, 1,800 RPM, 460V 3-phase
- Foundation: Reinforced concrete, 1,200mm × 800mm × 600mm deep
- Baseplate: Fabricated steel, 2,000mm × 1,000mm
- Piping: 150mm (6") suction, 100mm (4") discharge

**Arrangement features:**
- Coupling end clearance: 1,500mm (1.5× coupling length)
- Motor terminal box oriented away from piping for conduit access
- Suction strainer with drain valve and isolation valves
- Discharge pressure gauge and check valve

**Lessons learned:**
- Adequate clearance at coupling end critical for maintenance
- Piping flexibility analysis confirmed allowable nozzle loads not exceeded
- Foundation natural frequency >2× operating frequency (verified by calculation)

**Source:** Industry example; typical API 610 pump installation

#### Example 2: Vertical Sump Pump Installation

**Configuration:**
- Vertical, single-stage, sump pump
- Motor: 15 kW, 1,200 RPM, 460V 3-phase, explosion-proof (Class I, Div 2)
- Foundation: Concrete sump with pump mounting flange
- Discharge: 75mm (3") to above-grade discharge header

**Arrangement features:**
- Motor mounted on sump cover plate (grade level)
- Pump column extends into sump (4m depth)
- Discharge elbow at grade with flexible coupling (seismic isolation)
- Access ladder into sump for inspection (confined space entry procedures apply)

**Lessons learned:**
- Explosion-proof motor required due to hazardous area classification near sump
- Confined space entry procedures add complexity to maintenance (coordinate with safety plan)
- Sump pump eliminates NPSH concerns but requires deeper excavation

**Source:** Industry example; typical sump pump installation per API 610

#### Example 3: Marine Terminal Loading Pump (Precedent)

**Similar facility precedents:**
- **Vancouver Wharves (North Vancouver, BC):** Multi-commodity terminal with vegetable oil handling
- **Richardson International (Vancouver):** Canola crushing facility with oil storage and loading
- **Cargill (Alberta):** Canola processing with rail and truck loading

**Common design features observed:**
- High-capacity centrifugal pumps (500–1,500 m³/hr typical for marine loading)
- Duty/standby configuration for operational flexibility (OBJ-4)
- Outdoor installation with weatherproof motors and corrosion-resistant coatings
- Elevated pumps on structural steel platforms for NPSH and piping routing

**Relevance to project:**
- Fraser Surrey Terminal location similar marine/coastal environment
- 1,000,000 MT/annum throughput requires high-capacity, reliable pumping systems
- Operational flexibility (tank storage + direct rail-to-ship) similar to precedent facilities

**Source:** Industry knowledge; publicly available facility information

**Action:** Verify ER Part 2 for specific precedent references or design standards preferred by Employer.

### Anticipated Artifacts for Reference

From `_CONTEXT.md`, the following artifacts are anticipated for DEL-15.01:

1. **Pump arrangement drawings**
   - Overall layout showing all pumps in facility
   - Individual pump elevations and plan views
   - Clearance envelopes and access requirements

2. **Pump foundation details**
   - Foundation plan and sections
   - Anchor bolt details and schedules
   - Grout pad and baseplate details

3. **Piping interface drawings**
   - Pump nozzle schedule
   - Isometric views of pump connections
   - Flange and gasket details

**Source:** `_CONTEXT.md` (anticipated artifacts)

---

**Document Status:** ENRICHED (Pass 1)
**Enrichment Date:** 2026-01-28
**Agent:** 4_DOCUMENTS enrichment cycle

**Cross-References:**
- Datasheet.md — Equipment attributes and operating conditions
- Specification.md — Requirements for drawing content and verification
- Procedure.md — Process for producing and verifying drawings
- DEL-15.02 — Pump Technical Specification (performance requirements feed into arrangement)
- DEL-15.03 — Pump Design Calculations (NPSH, sizing verification)
- DEL-15.04 — Pump Data Sheet Package (vendor outline drawings input to arrangement)
- DEL-15.05 — Pump Installation & Test Records (installation verification uses these drawings)
