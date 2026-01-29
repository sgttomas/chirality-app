# Guidance: DEL-20.01 Instrumentation Design Drawing Set

## Purpose

This guidance document supports the development of the **Instrumentation Design Drawing Set** for **PKG-20 Field Instrumentation** on the Canola Oil Transload Facility Phase 1 project.

**Deliverable Objective:**

Defines the design arrangement and details for instrumentation per ER requirements.

**Source:** Decomposition document `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md`, DEL-20.01 (line 496)

**Deliverable Classification:**
- **Type:** Drawing
- **Discipline:** I&C
- **Responsible:** D&B Contractor
- **Project Phase:** Design & Build

**Source:** `_CONTEXT.md` and Decomposition PKG-20 scope

**Downstream Use:**

This drawing set will be used by:
- Construction contractors for field installation of instruments and cables
- Commissioning engineers for loop verification and system checkout
- Operations personnel for maintenance access and troubleshooting reference
- As-built documentation for facility lifecycle management

**Source:** **ASSUMPTION** based on typical drawing deliverable lifecycle use

## Principles

### Cross-Document Context

This Guidance document provides the engineering rationale and decision-making context for requirements defined in Specification.md. Key linkages:

- **Specification FR-1 to FR-6 (Functional Requirements)** — Principles below explain why these requirements exist
- **Specification PR-1 to PR-3 (Performance Requirements)** — Considerations section addresses factors affecting performance
- **Specification INT-1, INT-2 (Interface Requirements)** — Trade-offs section explores interface coordination strategies
- **Datasheet Attributes** — Examples section illustrates how attribute values are applied in practice

See Procedure.md for the step-by-step process to implement these requirements.

### Engineering Rationale (I&C Discipline)

**Principle 1: Instrumentation Serves Process Safety and Control**

Field instrumentation provides the "eyes and ears" of the facility control system:
- **Measurement** — Accurate sensing of process variables (level, pressure, temperature, flow)
- **Control** — Input signals for automated control loops and operator displays
- **Safety** — Critical measurements for alarm generation and safety interlocks
- **Custody transfer** — Accurate metering for product quantity verification

For a canola oil transload facility, instrumentation integrity directly impacts:
- Safe railcar unloading operations (overfill prevention, leak detection)
- Accurate product custody transfer during ship loading (commercial accountability)
- Storage tank monitoring (level, temperature for product quality)
- Environmental protection (spill detection, containment verification)

**Source:** **ASSUMPTION** based on I&C discipline fundamentals and decomposition project context (Section 1.1)

**Principle 2: Design for Harsh Marine Environment**

Fraser Surrey Terminal is a coastal marine facility. Instrumentation design must address:
- **Corrosion** — Salt air, moisture, temperature cycling
- **Weathering** — Outdoor exposure, UV degradation, rain intrusion
- **Environmental ratings** — NEMA/IP ratings appropriate for marine service
- **Material selection** — Stainless steel, marine-grade coatings, sealed enclosures

**Source:** **ASSUMPTION** based on project location (Fraser Surrey Terminal, Surrey, BC per Decomposition Section 1.1) and typical marine terminal conditions

**Principle 3: Hazardous Area Compliance**

Canola oil is a combustible liquid. Instrumentation in hazardous areas must be:
- **Classified per CEC/NEC** — Division/Zone classification appropriate to vapor release potential
- **Intrinsically safe or explosion-proof** — Electrical protection method suitable for classification
- **Properly sealed** — Cable entries, conduit seals per CSA C22.1 requirements

**Source:** **ASSUMPTION** based on canola oil combustibility and CSA C22.1 applicability (Canadian jurisdiction); **TBD**: Facility hazardous area classification study results

**Principle 4: Accessibility for Installation and Maintenance**

Instrument locations shall consider:
- **Installation access** — Adequate clearance for field installation (pipe cutting, welding, termination)
- **Maintenance access** — Safe access for calibration, repair, replacement (platforms, ladders, fall protection)
- **Operational visibility** — Local indicators visible from operator access points where applicable

**Source:** **ASSUMPTION** based on good engineering practice and operability considerations

**Principle 5: Interdisciplinary Coordination**

Instrumentation design is inherently cross-disciplinary:
- **Process** — P&IDs define what to measure and where
- **Piping** — Instrument connection points, taps, isolation valves
- **Structural** — Mounting supports, cable tray routing, junction box locations
- **Electrical** — Power supply, hazardous area classification, grounding
- **Control Systems** — Signal types, I/O allocation, network architecture

Drawing coordination is critical to avoid field conflicts and rework.

**Source:** **ASSUMPTION** based on typical EPC interdisciplinary integration requirements

### Applicable Standards Context

**ISA 5.1 — Instrumentation Symbols and Identification**
- Provides standard symbology for P&IDs and instrumentation drawings
- Defines tagging conventions (loop identification, instrument function codes)
- **Application:** Ensures consistent instrument identification across project documentation

**ISA 84 / IEC 61511 — Functional Safety**
- Governs design of safety instrumented systems (SIS)
- Requires safety integrity level (SIL) verification for safety functions
- **Application:** **TBD** — Applicability depends on whether facility includes SIS (e.g., overfill prevention, emergency shutdown)

**CSA C22.1 — Canadian Electrical Code**
- Governs electrical installations in Canadian jurisdiction (BC)
- Section 18: Hazardous locations (explosive atmospheres)
- **Application:** Mandatory for hazardous area instrument installations at Fraser Surrey Terminal

**API 554 — Process Instrumentation and Control**
- Oil and gas industry standard for instrumentation design and installation
- Covers instrument selection, installation practices, maintenance considerations
- **Application:** **ASSUMPTION** — Good practice reference for liquid bulk terminal instrumentation

**Source:** Standards list from existing Datasheet.md; applicability based on **ASSUMPTION** of typical I&C practice and Canadian regulatory context

## Considerations

### Project-Specific Considerations

**Facility Type: Canola Oil Transload**
- **Product characteristics:** CSD canola oil — viscosity, temperature sensitivity, material compatibility
- **Custody transfer:** High-accuracy flow metering required for commercial transactions (export loading)
- **Storage monitoring:** Tank level and temperature instrumentation for 3 × 15,000 MT tanks
- **Railcar unloading:** Instrumentation for 32 unloading stations (level monitoring, flow control)

**Source:** Decomposition Section 1.1 Key Parameters (lines 38-44)

**Location: Marine Terminal**
- **Environmental exposure:** Corrosive marine atmosphere, rain, fog, temperature range
- **Access constraints:** Working around active terminal operations (OBJ-5: Terminal Continuity)
- **Seismic considerations:** BC seismic zone requires instrument mounting and support design
- **Regulatory jurisdiction:** Provincial (BC), Federal (Transport Canada for marine operations), Municipal (Surrey)

**Source:** Decomposition Section 1.1 (Location); OBJ-5 (line 62); **ASSUMPTION** based on Canadian regulatory framework

**Design & Build Delivery**
- **Constructor input:** Early involvement of construction team can improve buildability
- **Procurement integration:** Drawing details must support equipment procurement (mounting requirements)
- **Fast-track potential:** Phased drawing release may be required to support construction schedule

**Source:** Decomposition project title "Design & Build Contract" (line 4); **ASSUMPTION** based on typical D&B execution approach

### Technical Considerations

**Instrument Selection and Sizing**
- Coordinate with DEL-20.03 (Instrumentation Design Calculations) for sizing basis
- Coordinate with DEL-20.04 (Instrumentation Data Sheet Package) for equipment data
- Consider instrument turndown, accuracy, response time for process control needs

**Source:** Cross-reference to PKG-20 deliverables (lines 498-499)

**Cable Routing and Infrastructure**
- Underground duct banks for long runs (railcar unloading area to control building)
- Cable trays for above-ground routing (tank farm, loading platform)
- Conduit for final connections and hazardous area sealing
- Coordinate with PKG-23 (Electrical Infrastructure) for routing infrastructure

**Source:** **ASSUMPTION** based on typical terminal electrical infrastructure; cross-reference to PKG-23 per package structure

**Junction Box Locations**
- Minimize cable lengths from field instruments to termination points
- Group instruments by area for efficient junction box utilization
- Provide adequate junction box sizing for future expansion (OBJ-8: Future Expandability)
- Environmental ratings (NEMA 4X typical for marine environment)

**Source:** **ASSUMPTION** based on typical I&C design practice; OBJ-8 reference (line 65)

**Power Supply Coordination**
- Instrument power requirements (24 VDC, 120 VAC typical)
- Coordinate with PKG-17 (Electrical Power Distribution) for instrument power panels
- Uninterruptible power supply (UPS) for critical instrumentation (**TBD**: criticality assessment)

**Source:** **ASSUMPTION** based on typical instrument power requirements; cross-reference to PKG-17 per package structure

**Hazardous Area Strategy**
- Intrinsically safe (IS) barriers in safe area, simple apparatus in field (lower installation cost)
- Explosion-proof enclosures in field (simpler wiring, higher equipment cost)
- Purged/pressurized enclosures for analyzer shelters or complex devices
- **TBD**: Strategy to be confirmed based on facility hazardous area classification and project preferences

**Source:** **ASSUMPTION** based on typical hazardous area design options per CSA C22.1

### Coordination Considerations

**Upstream Dependencies** (typical coordination required):
- P&IDs and instrument index (defines what to draw)
- Process flow diagrams and heat & material balances (design basis for instrument sizing)
- Equipment layouts and plot plans (spatial constraints for instrument placement)
- Piping isometrics and arrangements (instrument connection points)
- Hazardous area classification drawings (instrument electrical protection requirements)
- Control system architecture (I/O allocation, signal types, network topology)

**Downstream Impacts** (who uses these drawings):
- Equipment procurement (instrument mounting dimensions, connection sizes)
- Piping fabrication (instrument taps, valve requirements)
- Electrical installation (cable pulling, terminations, junction box population)
- Commissioning (loop identification, test procedure development)
- Operations training (facility familiarization, instrument location reference)

**Source:** **ASSUMPTION** based on typical EPC workflow and deliverable interfaces

**Interdisciplinary Coordination** (IDC process):
- Issue drawings for IDC review to affected disciplines
- Resolve comments and incorporate feedback
- Obtain sign-offs before proceeding to next design phase
- **TBD**: Project-specific IDC procedures and timing

**Source:** **ASSUMPTION** based on typical EPC interdisciplinary coordination process

### Quality and Verification Considerations

**Design Review Stages**
- 30% review: Concept and major equipment locations
- 60% review: Detailed layouts and cable routing
- 90% review: Final details and specifications
- IFC review: Issued for Construction (ready for field installation)

**Source:** **ASSUMPTION** based on typical EPC design review gates; **TBD**: Project-specific review stages per Employer's Requirements

**Verification Activities**
- Self-check: Originator reviews own work for completeness and accuracy
- Independent check: Peer review by qualified I&C engineer (different from originator)
- IDC: Interdisciplinary coordination with piping, electrical, structural, control systems
- QA audit: Compliance check against project quality procedures and CAD standards

**Source:** **ASSUMPTION** based on typical EPC quality assurance requirements

**Common Drawing Errors to Avoid**
- Instrument tag number mismatches with P&IDs
- Instrument locations conflicting with piping or equipment
- Inadequate maintenance clearances
- Cable routes not coordinated with cable tray/duct bank layout
- Missing hazardous area sealing details
- Inconsistent symbology or drafting standards

**Source:** **ASSUMPTION** based on typical I&C drawing errors and lessons learned

## Trade-offs

### Design Trade-offs

**Trade-off 1: Intrinsically Safe vs. Explosion-Proof**

| Aspect | Intrinsically Safe (IS) | Explosion-Proof (XP) |
|--------|-------------------------|----------------------|
| Field devices | Simple (lower cost) | Complex (higher cost) |
| Wiring cost | Higher (special IS cable, separation) | Lower (standard cable) |
| Flexibility | Lower (energy limits restrict device types) | Higher (most devices compatible) |
| Maintenance | Requires IS barrier checks | Requires enclosure integrity checks |
| Typical choice | Large field instrument populations | Individual complex devices |

**Recommendation:** **TBD** — To be determined based on facility hazardous area classification extent, project budget, and maintenance philosophy.

**Source:** **ASSUMPTION** based on typical hazardous area design trade-offs per CSA C22.1 and industry practice

**Trade-off 2: Central vs. Distributed Junction Boxes**

| Aspect | Central JBs (fewer, larger) | Distributed JBs (more, smaller) |
|--------|------------------------------|----------------------------------|
| Cable length | Longer field cable runs | Shorter field cable runs |
| JB cost | Lower (fewer enclosures) | Higher (more enclosures) |
| Maintenance access | Concentrated at few locations | Spread across facility |
| Future flexibility | Less flexible (fixed termination point) | More flexible (local termination) |
| Typical choice | Compact facility areas | Large, distributed areas (tank farm) |

**Recommendation:** **ASSUMPTION** — Distributed approach likely appropriate for 32 railcar stations spread over rail tracks; central approach may suit compact areas like control building.

**Source:** **ASSUMPTION** based on facility layout considerations and typical I&C design practice

**Trade-off 3: Detail Drawing Depth**

| Aspect | Minimal Details (Reference Mnfr) | Extensive Details (Fully Specified) |
|--------|-----------------------------------|--------------------------------------|
| Engineering effort | Lower (faster to produce) | Higher (more drawing time) |
| Constructor clarity | Requires manufacturer coordination | Self-contained installation guidance |
| Flexibility | Allows field adaptation | Prescriptive (less flexibility) |
| Risk | Field interpretation issues | Over-specification constraints |
| Typical choice | Experienced contractors, standard products | Complex installations, critical instruments |

**Recommendation:** **ASSUMPTION** — Balance approach: provide typical details for standard installations; reference manufacturer for specialized equipment (e.g., custody transfer meters).

**Source:** **ASSUMPTION** based on typical EPC drawing detail philosophy and design-build risk allocation

**Trade-off 4: Drawing Release Strategy**

| Aspect | Single IFC Release | Phased Release (by area/system) |
|--------|--------------------|---------------------------------|
| Design completeness | Full coordination achieved | Partial coordination per phase |
| Construction start | Later (await full design) | Earlier (fast-track) |
| Change risk | Lower (stable design) | Higher (interface changes) |
| Schedule | Longer design phase | Compressed overall schedule |
| Typical choice | Complex, highly integrated facilities | Fast-track, modular construction |

**Recommendation:** **TBD** — To be determined based on project schedule constraints and Employer priorities (OBJ-5: Terminal Continuity may favor fast-track approach to minimize terminal disruption).

**Source:** **ASSUMPTION** based on typical EPC phasing strategies; OBJ-5 reference (Decomposition line 62)

### Cost vs. Performance Trade-offs

**Instrument Redundancy**
- Single instruments: Lower cost, single-point failure risk
- Redundant instruments: Higher cost, improved reliability (supports OBJ-1: Safe & Reliable Operation)
- **TBD**: Criticality assessment and redundancy requirements per Employer's Requirements

**Source:** OBJ-1 reference (Decomposition line 58)

**Instrumentation Density**
- Minimal instrumentation: Lower capital cost, reduced operational visibility
- Comprehensive instrumentation: Higher capital cost, improved process control and troubleshooting
- **TBD**: Instrumentation philosophy per Employer's Requirements (balance cost vs. operational needs)

**Source:** **ASSUMPTION** based on typical capital vs. operational cost trade-offs

**Cable Infrastructure**
- Direct burial: Lower initial cost, difficult to modify/expand
- Duct banks and trays: Higher initial cost, easier future expansion (supports OBJ-8: Future Expandability)
- **TBD**: Infrastructure strategy per project execution plan

**Source:** OBJ-8 reference (Decomposition line 65)

## Examples

### Reference Examples and Precedents

**Industry Precedents:**
- Similar liquid bulk terminals (vegetable oil, petroleum products)
- Marine loading/unloading facilities with custody transfer metering
- Railcar unloading operations with multiple parallel stations

**TBD** — Specific precedent project references to be identified and reviewed for lessons learned.

**Source:** **ASSUMPTION** — Typical approach for EPC projects to leverage industry precedents

### Drawing Types (Typical Content)

**Example 1: Instrument Location Plan**
- Base drawing: Equipment layout or piping plan
- Overlaid content: Instrument tag numbers, locations (dimensioned from reference points)
- Typical scale: 1:100 or 1:50 for detailed areas
- Typical information: Instrument type, elevation (EL), access notes

**Example 2: Instrument Installation Detail**
- Typical detail: Level transmitter mounting on tank nozzle
- Content: Mounting flange, isolation valve, drain/vent, tubing/cable connection
- References: Manufacturer installation drawing, material specification

**Example 3: Cable Schedule**
- Tabular format: Columns for cable tag, from/to, cable type, length, routing, termination
- Typical grouping: By area, by junction box, by cable type
- Integration: Links to instrument list (from tag) and I/O list (to tag)

**Source:** **ASSUMPTION** based on typical I&C drawing content and formats

### Project-Specific Examples

**Anticipated Drawing Applications:**

**Railcar Unloading Stations (32 stations)**
- Instrument location plan showing unloading pit instrumentation layout
- Level switches for unloading pit sump monitoring
- Flow instruments on unloading headers
- Pressure instruments for pump performance monitoring
- Cable routing from rail track area to control building

**Source:** Decomposition Key Parameters — 32 railcar unloading stations (line 43); **ASSUMPTION** on typical railcar unloading instrumentation requirements

**Storage Tanks (3 × 15,000 MT)**
- Tank instrumentation layout: level transmitters (top-mounted or side-mounted), temperature elements (multiple elevations)
- Installation details for tank roof/shell penetrations
- Cable routing from tank farm to control building
- Hazardous area considerations (tank vapor space classification)

**Source:** Decomposition Key Parameters — 45,000 MT storage capacity in 3 tanks (line 40); **ASSUMPTION** on typical storage tank instrumentation

**Marine Loading Platform**
- Loading arm instrumentation (emergency shutdown valves, position switches)
- Custody transfer metering (Coriolis or turbine meters, transmitters, proving connection)
- Cable routing to control system and metering computer
- Marine environment considerations (corrosion protection, weatherproofing)

**Source:** Decomposition Project Overview — "transfers from rail tank cars to liquid bulk carriers for export" (line 34); **ASSUMPTION** on typical marine loading instrumentation requirements; coordinate with PKG-11 (Marine Loading System) per decomposition (lines 240-252)

### Lessons Learned (Typical Issues)

**Issue 1: Inadequate Maintenance Clearances**
- Problem: Instrument located in confined space without adequate access for calibration/removal
- Solution: Review instrument locations with maintenance personnel; provide platform access where needed

**Issue 2: Cable Route Not Constructible**
- Problem: Drawing shows cable route through area with no cable tray or duct bank infrastructure
- Solution: Early coordination with electrical infrastructure design (PKG-23)

**Issue 3: Hazardous Area Sealing Omitted**
- Problem: Conduit seals not shown on installation details for hazardous area instruments
- Solution: Develop standard details for hazardous area installations per CSA C22.1; include on all applicable drawings

**Source:** **ASSUMPTION** based on typical I&C drawing lessons learned and common field issues

**Note:** Project-specific lessons learned to be captured during design and construction phases for continuous improvement.

## Project Objective Alignment

This deliverable supports the following project objectives:

**OBJ-1: Safe & Reliable Operation**
- Proper instrumentation design and installation is fundamental to safe facility operations
- Clear, accurate drawings reduce installation errors and improve system reliability
- As-built documentation supports ongoing maintenance and troubleshooting

**Source:** Decomposition Section 6 Objective-to-Deliverable Mapping — PKG-20 supports OBJ-1 (line 780)

**Secondary Objective Support:**
- **OBJ-6: Regulatory Compliance** — Drawings demonstrate compliance with electrical code (CSA C22.1) and safety standards
- **OBJ-7: Environmental Protection** — Proper instrumentation enables leak detection and spill prevention monitoring
- **OBJ-10: Custody Transfer Accuracy** — Installation details support accurate metering system installation

**Source:** **ASSUMPTION** based on instrumentation role in facility operations and regulatory compliance
