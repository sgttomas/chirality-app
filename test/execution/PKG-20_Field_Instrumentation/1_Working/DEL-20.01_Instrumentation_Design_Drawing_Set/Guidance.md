# Guidance: DEL-20.01 Instrumentation Design Drawing Set

## Purpose

This guidance document supports the development of the **Instrumentation Design Drawing Set** for **PKG-20 Field Instrumentation** on the Canola Oil Transload Facility Phase 1 project.

**Deliverable Objective:**

Defines the design arrangement and details for instrumentation per ER requirements.

**Source:** Decomposition document `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md`, DEL-20.01 (line 496)

**Deliverable Classification:**

| Field | Value | Datasheet § | Specification § |
|-------|-------|-------------|-----------------|
| Type | Drawing | Identification | Scope |
| Discipline | I&C | Identification | Scope |
| Responsible | D&B Contractor | Identification | Scope |
| Project Phase | Design & Build | Identification | Scope |

**Source:** `_CONTEXT.md` and Decomposition PKG-20 scope

**Downstream Use:**

This drawing set will be used by:

| User | Purpose | Specification § | Procedure Step |
|------|---------|-----------------|----------------|
| Construction contractors | Field installation of instruments and cables | INT-2 | 5.2 |
| Commissioning engineers | Loop verification and system checkout | INT-2 | 6.2 |
| Operations personnel | Maintenance access and troubleshooting reference | INT-2 | Records |
| As-built documentation | Facility lifecycle management | QR-4 | 6.2 |

**Source:** **ASSUMPTION** based on typical drawing deliverable lifecycle use

## Principles

### Cross-Document Context

This Guidance document provides the engineering rationale and decision-making context for requirements defined in Specification.md. Key linkages:

| Specification Section | Guidance Section | Relationship |
|----------------------|------------------|--------------|
| FR-1 to FR-6 (Functional Requirements) | Principles, Examples | Principles explain why these requirements exist |
| PR-1 to PR-3 (Performance Requirements) | Considerations | Factors affecting performance decisions |
| INT-1, INT-2 (Interface Requirements) | Trade-offs, Coordination Considerations | Interface coordination strategies |
| Standards | Standards Context | Rationale for standards applicability |
| QR-1 to QR-4 (Quality Requirements) | Quality Considerations | Quality verification approach |

**Datasheet § Attributes** — Examples section illustrates how attribute values are applied in practice.

See Procedure.md for the step-by-step process to implement these requirements.

### Engineering Rationale (I&C Discipline)

**Principle 1: Instrumentation Serves Process Safety and Control**

Field instrumentation provides the "eyes and ears" of the facility control system:

| Function | Description | Specification § | Procedure Step |
|----------|-------------|-----------------|----------------|
| Measurement | Accurate sensing of process variables (level, pressure, temperature, flow) | FR-6 | 2.1 |
| Control | Input signals for automated control loops and operator displays | FR-6, INT-1 | 3.3 |
| Safety | Critical measurements for alarm generation and safety interlocks | FR-6, Standards | 3.2 |
| Custody transfer | Accurate metering for product quantity verification | FR-6 | 3.1 |

For a canola oil transload facility, instrumentation integrity directly impacts:
- Safe railcar unloading operations (overfill prevention, leak detection)
- Accurate product custody transfer during ship loading (commercial accountability)
- Storage tank monitoring (level, temperature for product quality)
- Environmental protection (spill detection, containment verification)

**Source:** **ASSUMPTION** based on I&C discipline fundamentals and decomposition project context (Section 1.1)

**Principle 2: Design for Harsh Marine Environment**

Fraser Surrey Terminal is a coastal marine facility. Instrumentation design must address:

| Environmental Factor | Design Response | Specification § | Datasheet § |
|---------------------|-----------------|-----------------|-------------|
| Corrosion | Salt air, moisture, temperature cycling — use corrosion-resistant materials | FR-6 | Conditions |
| Weathering | Outdoor exposure, UV degradation, rain intrusion — use appropriate enclosures | FR-3 | Conditions |
| Environmental ratings | NEMA/IP ratings appropriate for marine service | FR-3, PR-1 | Attributes |
| Material selection | Stainless steel, marine-grade coatings, sealed enclosures | FR-3 | Installation Requirements |

**Source:** **ASSUMPTION** based on project location (Fraser Surrey Terminal, Surrey, BC per Decomposition Section 1.1) and typical marine terminal conditions

**Principle 3: Hazardous Area Compliance**

Canola oil is a combustible liquid. Instrumentation in hazardous areas must be:

| Requirement | Description | Specification § | Procedure Step |
|-------------|-------------|-----------------|----------------|
| Classification | Classified per CEC/NEC — Division/Zone classification appropriate to vapor release potential | Standards | 1.1 |
| Protection method | Intrinsically safe or explosion-proof — electrical protection method suitable for classification | FR-3, Standards | 3.2 |
| Sealing | Properly sealed — cable entries, conduit seals per CSA C22.1 requirements | FR-3, Standards | 3.2 |

**Source:** **ASSUMPTION** based on canola oil combustibility and CSA C22.1 applicability (Canadian jurisdiction); **TBD**: Facility hazardous area classification study results

**Principle 4: Accessibility for Installation and Maintenance**

Instrument locations shall consider:

| Access Requirement | Description | Specification § | Procedure Step |
|-------------------|-------------|-----------------|----------------|
| Installation access | Adequate clearance for field installation (pipe cutting, welding, termination) | FR-2 | 2.1 |
| Maintenance access | Safe access for calibration, repair, replacement (platforms, ladders, fall protection) | FR-2 | 2.1 |
| Operational visibility | Local indicators visible from operator access points where applicable | FR-2 | 2.1 |

**Source:** **ASSUMPTION** based on good engineering practice and operability considerations

**Principle 5: Interdisciplinary Coordination**

Instrumentation design is inherently cross-disciplinary:

| Discipline | Coordination Need | Specification § | Procedure Step |
|------------|-------------------|-----------------|----------------|
| Process | P&IDs define what to measure and where | FR-5, INT-1 | 1.1 |
| Piping | Instrument connection points, taps, isolation valves | FR-5, INT-1 | 2.1 |
| Structural | Mounting supports, cable tray routing, junction box locations | FR-5, INT-1 | 2.1 |
| Electrical | Power supply, hazardous area classification, grounding | INT-1 | 3.2 |
| Control Systems | Signal types, I/O allocation, network architecture | INT-1 | 3.3 |

Drawing coordination is critical to avoid field conflicts and rework.

**Source:** **ASSUMPTION** based on typical EPC interdisciplinary integration requirements

### Applicable Standards Context

**ISA 5.1 — Instrumentation Symbols and Identification**

| Aspect | Description | Specification § | Procedure Step |
|--------|-------------|-----------------|----------------|
| Symbology | Provides standard symbology for P&IDs and instrumentation drawings | PR-2, Standards | 3.1 |
| Tagging | Defines tagging conventions (loop identification, instrument function codes) | FR-2, Standards | 3.1 |
| Application | Ensures consistent instrument identification across project documentation | PR-2 | 3.1 |

**ISA 84 / IEC 61511 — Functional Safety**

| Aspect | Description | Specification § | Procedure Step |
|--------|-------------|-----------------|----------------|
| SIS design | Governs design of safety instrumented systems (SIS) | Standards | 3.2 |
| SIL verification | Requires safety integrity level (SIL) verification for safety functions | Standards | 4.1 |
| Application | **TBD** — Applicability depends on whether facility includes SIS (e.g., overfill prevention, emergency shutdown) | Standards | 1.1 |

**CSA C22.1 — Canadian Electrical Code**

| Aspect | Description | Specification § | Procedure Step |
|--------|-------------|-----------------|----------------|
| Jurisdiction | Governs electrical installations in Canadian jurisdiction (BC) | Standards | 1.1 |
| Section 18 | Hazardous locations (explosive atmospheres) | Standards | 3.2 |
| Application | Mandatory for hazardous area instrument installations at Fraser Surrey Terminal | Standards | 3.2 |

**API 554 — Process Instrumentation and Control**

| Aspect | Description | Specification § | Procedure Step |
|--------|-------------|-----------------|----------------|
| Industry standard | Oil and gas industry standard for instrumentation design and installation | Standards | 1.3 |
| Coverage | Covers instrument selection, installation practices, maintenance considerations | Standards | 3.2 |
| Application | **ASSUMPTION** — Good practice reference for liquid bulk terminal instrumentation | Standards | 1.3 |

**Source:** Standards list from Datasheet.md References; Specification.md Standards section; applicability based on **ASSUMPTION** of typical I&C practice and Canadian regulatory context

## Considerations

### Project-Specific Considerations

**Facility Type: Canola Oil Transload**

| Consideration | Description | Specification § | Datasheet § |
|---------------|-------------|-----------------|-------------|
| Product characteristics | CSD canola oil — viscosity, temperature sensitivity, material compatibility | FR-6 | Conditions |
| Custody transfer | High-accuracy flow metering required for commercial transactions (export loading) | FR-6 | Key Project Parameters |
| Storage monitoring | Tank level and temperature instrumentation for 3 × 15,000 MT tanks | FR-6 | Key Project Parameters |
| Railcar unloading | Instrumentation for 32 unloading stations (level monitoring, flow control) | FR-6 | Key Project Parameters |

**Source:** Decomposition Section 1.1 Key Parameters (lines 38-44)

**Location: Marine Terminal**

| Consideration | Description | Specification § | Datasheet § |
|---------------|-------------|-----------------|-------------|
| Environmental exposure | Corrosive marine atmosphere, rain, fog, temperature range | FR-6 | Conditions |
| Access constraints | Working around active terminal operations (OBJ-5: Terminal Continuity) | — | — |
| Seismic considerations | BC seismic zone requires instrument mounting and support design | Standards | Conditions |
| Regulatory jurisdiction | Provincial (BC), Federal (Transport Canada for marine operations), Municipal (Surrey) | Standards | — |

**Source:** Decomposition Section 1.1 (Location); OBJ-5 (line 62); **ASSUMPTION** based on Canadian regulatory framework

**Design & Build Delivery**

| Consideration | Description | Specification § | Procedure Step |
|---------------|-------------|-----------------|----------------|
| Constructor input | Early involvement of construction team can improve buildability | — | 2.1 |
| Procurement integration | Drawing details must support equipment procurement (mounting requirements) | FR-1 | 5.2 |
| Fast-track potential | Phased drawing release may be required to support construction schedule | — | Trade-off 4 |

**Source:** Decomposition project title "Design & Build Contract" (line 4); **ASSUMPTION** based on typical D&B execution approach

### Technical Considerations

**Instrument Selection and Sizing**

| Consideration | Coordination | Specification § | Procedure Step |
|---------------|--------------|-----------------|----------------|
| Sizing basis | Coordinate with DEL-20.03 (Instrumentation Design Calculations) | INT-2 | 1.1 |
| Equipment data | Coordinate with DEL-20.04 (Instrumentation Data Sheet Package) | INT-2 | 3.2 |
| Performance | Consider instrument turndown, accuracy, response time for process control needs | FR-6 | 1.1 |

**Source:** Cross-reference to PKG-20 deliverables (lines 498-499)

**Cable Routing and Infrastructure**

| Infrastructure | Application | Specification § | Procedure Step |
|----------------|-------------|-----------------|----------------|
| Underground duct banks | Long runs (railcar unloading area to control building) | FR-4, INT-1 | 2.2 |
| Cable trays | Above-ground routing (tank farm, loading platform) | FR-4, INT-1 | 2.2 |
| Conduit | Final connections and hazardous area sealing | FR-4, INT-1 | 3.3 |
| Coordination | Coordinate with PKG-23 (Electrical Infrastructure) for routing infrastructure | INT-1 | 2.2 |

**Source:** **ASSUMPTION** based on typical terminal electrical infrastructure; cross-reference to PKG-23 per package structure

**Junction Box Locations**

| Consideration | Description | Specification § | Procedure Step |
|---------------|-------------|-----------------|----------------|
| Cable lengths | Minimize cable lengths from field instruments to termination points | FR-4 | 2.2 |
| Grouping | Group instruments by area for efficient junction box utilization | FR-4 | 2.2 |
| Future expansion | Provide adequate junction box sizing for future expansion (OBJ-8: Future Expandability) | — | 2.2 |
| Environmental ratings | NEMA 4X typical for marine environment | FR-3 | 3.2 |

**Source:** **ASSUMPTION** based on typical I&C design practice; OBJ-8 reference (line 65)

**Power Supply Coordination**

| Consideration | Description | Specification § | Procedure Step |
|---------------|-------------|-----------------|----------------|
| Power requirements | Instrument power requirements (24 VDC, 120 VAC typical) | INT-1 | 3.2 |
| Power panels | Coordinate with PKG-17 (Electrical Power Distribution) for instrument power panels | INT-1 | 3.2 |
| UPS | Uninterruptible power supply (UPS) for critical instrumentation (**TBD**: criticality assessment) | INT-1 | 3.2 |

**Source:** **ASSUMPTION** based on typical instrument power requirements; cross-reference to PKG-17 per package structure

**Hazardous Area Strategy**

| Strategy | Description | Pros | Cons |
|----------|-------------|------|------|
| Intrinsically safe (IS) | Barriers in safe area, simple apparatus in field | Lower installation cost | Energy limits restrict device types |
| Explosion-proof (XP) | Enclosures in field | Simpler wiring, most devices compatible | Higher equipment cost |
| Purged/pressurized | Enclosures for analyzer shelters or complex devices | Protects complex equipment | Higher maintenance, air supply required |

**TBD**: Strategy to be confirmed based on facility hazardous area classification and project preferences

**Source:** **ASSUMPTION** based on typical hazardous area design options per CSA C22.1

### Coordination Considerations

**Upstream Dependencies** (typical coordination required):

| Input | Source | Purpose | Specification § | Procedure Step |
|-------|--------|---------|-----------------|----------------|
| P&IDs and instrument index | Process Engineering | Defines what to draw | FR-5, INT-2 | 1.1 |
| Process flow diagrams and heat & material balances | Process Engineering | Design basis for instrument sizing | INT-2 | 1.1 |
| Equipment layouts and plot plans | Layout | Spatial constraints for instrument placement | FR-5, INT-2 | 2.1 |
| Piping isometrics and arrangements | PKG-14 | Instrument connection points | FR-5, INT-2 | 2.1 |
| Hazardous area classification drawings | PKG-17 | Instrument electrical protection requirements | FR-3, INT-2 | 1.1 |
| Control system architecture | PKG-22 | I/O allocation, signal types, network topology | INT-1, INT-2 | 3.3 |

**Downstream Impacts** (who uses these drawings):

| User | Purpose | Specification § | Procedure Step |
|------|---------|-----------------|----------------|
| Equipment procurement | Instrument mounting dimensions, connection sizes | FR-1, INT-2 | 5.2 |
| Piping fabrication | Instrument taps, valve requirements | INT-2 | 5.2 |
| Electrical installation | Cable pulling, terminations, junction box population | INT-2 | 5.2 |
| Commissioning | Loop identification, test procedure development | INT-2 | 6.2 |
| Operations training | Facility familiarization, instrument location reference | INT-2 | Records |

**Source:** **ASSUMPTION** based on typical EPC workflow and deliverable interfaces

**Interdisciplinary Coordination** (IDC process):

| Activity | Description | Specification § | Procedure Step |
|----------|-------------|-----------------|----------------|
| Issue for IDC | Issue drawings for IDC review to affected disciplines | QR-1 | 2.4, 3.4, 4.4 |
| Comment resolution | Resolve comments and incorporate feedback | QR-1 | 4.4 |
| Sign-offs | Obtain sign-offs before proceeding to next design phase | QR-1 | 4.4 |

**TBD**: Project-specific IDC procedures and timing

**Source:** **ASSUMPTION** based on typical EPC interdisciplinary coordination process

### Quality and Verification Considerations

**Design Review Stages**

| Stage | Completeness | Purpose | Specification § | Procedure Step |
|-------|--------------|---------|-----------------|----------------|
| 30% review | Concept | Major equipment locations | QR-1 | 2.4 |
| 60% review | Detailed | Detailed layouts and cable routing | QR-1 | 3.4 |
| 90% review | Final | Final details and specifications | QR-1 | 4.5 |
| IFC review | Issued | Ready for field installation | QR-1 | 5.1 |

**Source:** **ASSUMPTION** based on typical EPC design review gates; **TBD**: Project-specific review stages per Employer's Requirements

**Verification Activities**

| Activity | Performer | Purpose | Specification § | Procedure Step |
|----------|-----------|---------|-----------------|----------------|
| Self-check | Originator | Reviews own work for completeness and accuracy | QR-1 | 4.2 |
| Independent check | Peer reviewer | Peer review by qualified I&C engineer (different from originator) | QR-1 | 4.3 |
| IDC | Affected disciplines | Interdisciplinary coordination with piping, electrical, structural, control systems | QR-1 | 4.4 |
| QA audit | QA | Compliance check against project quality procedures and CAD standards | QR-3 | 4.1 |

**Source:** **ASSUMPTION** based on typical EPC quality assurance requirements

**Common Drawing Errors to Avoid**

| Error | Prevention | Specification § | Procedure Step |
|-------|------------|-----------------|----------------|
| Instrument tag number mismatches with P&IDs | Cross-check with instrument list | FR-2, Verification | 4.2 |
| Instrument locations conflicting with piping or equipment | IDC coordination | FR-5, QR-1 | 4.4 |
| Inadequate maintenance clearances | Review with maintenance/operations | FR-2 | 2.1 |
| Cable routes not coordinated with cable tray/duct bank layout | Coordinate with PKG-23 | FR-4, INT-1 | 2.2 |
| Missing hazardous area sealing details | Standard details per CSA C22.1 | FR-3, Standards | 3.2 |
| Inconsistent symbology or drafting standards | CAD standards audit | PR-2, QR-3 | 4.1 |

**Source:** **ASSUMPTION** based on typical I&C drawing errors and lessons learned

## Trade-offs

### Design Trade-offs

**Trade-off 1: Intrinsically Safe vs. Explosion-Proof**

| Aspect | Intrinsically Safe (IS) | Explosion-Proof (XP) | Specification § | Procedure Step |
|--------|-------------------------|----------------------|-----------------|----------------|
| Field devices | Simple (lower cost) | Complex (higher cost) | FR-3, Standards | 3.2 |
| Wiring cost | Higher (special IS cable, separation) | Lower (standard cable) | FR-4 | 3.3 |
| Flexibility | Lower (energy limits restrict device types) | Higher (most devices compatible) | — | 1.1 |
| Maintenance | Requires IS barrier checks | Requires enclosure integrity checks | — | — |
| Typical choice | Large field instrument populations | Individual complex devices | — | 1.1 |

**Recommendation:** **TBD** — To be determined based on facility hazardous area classification extent, project budget, and maintenance philosophy.

**Source:** **ASSUMPTION** based on typical hazardous area design trade-offs per CSA C22.1 and industry practice

**Trade-off 2: Central vs. Distributed Junction Boxes**

| Aspect | Central JBs (fewer, larger) | Distributed JBs (more, smaller) | Specification § | Procedure Step |
|--------|------------------------------|----------------------------------|-----------------|----------------|
| Cable length | Longer field cable runs | Shorter field cable runs | FR-4 | 2.2 |
| JB cost | Lower (fewer enclosures) | Higher (more enclosures) | — | 2.2 |
| Maintenance access | Concentrated at few locations | Spread across facility | — | — |
| Future flexibility | Less flexible (fixed termination point) | More flexible (local termination) | — | 2.2 |
| Typical choice | Compact facility areas | Large, distributed areas (tank farm) | — | 2.2 |

**Recommendation:** **ASSUMPTION** — Distributed approach likely appropriate for 32 railcar stations spread over rail tracks; central approach may suit compact areas like control building.

**Source:** **ASSUMPTION** based on facility layout considerations and typical I&C design practice

**Trade-off 3: Detail Drawing Depth**

| Aspect | Minimal Details (Reference Mnfr) | Extensive Details (Fully Specified) | Specification § | Procedure Step |
|--------|-----------------------------------|--------------------------------------|-----------------|----------------|
| Engineering effort | Lower (faster to produce) | Higher (more drawing time) | — | 3.1, 3.2 |
| Constructor clarity | Requires manufacturer coordination | Self-contained installation guidance | FR-1 | 3.2 |
| Flexibility | Allows field adaptation | Prescriptive (less flexibility) | — | — |
| Risk | Field interpretation issues | Over-specification constraints | — | — |
| Typical choice | Experienced contractors, standard products | Complex installations, critical instruments | — | 3.2 |

**Recommendation:** **ASSUMPTION** — Balance approach: provide typical details for standard installations; reference manufacturer for specialized equipment (e.g., custody transfer meters).

**Source:** **ASSUMPTION** based on typical EPC drawing detail philosophy and design-build risk allocation

**Trade-off 4: Drawing Release Strategy**

| Aspect | Single IFC Release | Phased Release (by area/system) | Specification § | Procedure Step |
|--------|--------------------|---------------------------------|-----------------|----------------|
| Design completeness | Full coordination achieved | Partial coordination per phase | PR-3 | 5.2 |
| Construction start | Later (await full design) | Earlier (fast-track) | — | 5.2 |
| Change risk | Lower (stable design) | Higher (interface changes) | QR-2 | 6.1 |
| Schedule | Longer design phase | Compressed overall schedule | — | 5.2 |
| Typical choice | Complex, highly integrated facilities | Fast-track, modular construction | — | — |

**Recommendation:** **TBD** — To be determined based on project schedule constraints and Employer priorities (OBJ-5: Terminal Continuity may favor fast-track approach to minimize terminal disruption).

**Source:** **ASSUMPTION** based on typical EPC phasing strategies; OBJ-5 reference (Decomposition line 62)

### Cost vs. Performance Trade-offs

**Instrument Redundancy**

| Aspect | Description | Specification § | Related Objective |
|--------|-------------|-----------------|-------------------|
| Single instruments | Lower cost, single-point failure risk | — | — |
| Redundant instruments | Higher cost, improved reliability | — | OBJ-1: Safe & Reliable Operation |
| **TBD** | Criticality assessment and redundancy requirements per Employer's Requirements | — | — |

**Source:** OBJ-1 reference (Decomposition line 58)

**Instrumentation Density**

| Aspect | Description | Specification § | Related Objective |
|--------|-------------|-----------------|-------------------|
| Minimal instrumentation | Lower capital cost, reduced operational visibility | — | — |
| Comprehensive instrumentation | Higher capital cost, improved process control and troubleshooting | FR-6 | OBJ-1 |
| **TBD** | Instrumentation philosophy per Employer's Requirements (balance cost vs. operational needs) | — | — |

**Source:** **ASSUMPTION** based on typical capital vs. operational cost trade-offs

**Cable Infrastructure**

| Aspect | Description | Specification § | Related Objective |
|--------|-------------|-----------------|-------------------|
| Direct burial | Lower initial cost, difficult to modify/expand | FR-4 | — |
| Duct banks and trays | Higher initial cost, easier future expansion | FR-4, INT-1 | OBJ-8: Future Expandability |
| **TBD** | Infrastructure strategy per project execution plan | — | — |

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

| Element | Description | Specification § | Procedure Step |
|---------|-------------|-----------------|----------------|
| Base drawing | Equipment layout or piping plan | FR-2 | 3.1 |
| Overlaid content | Instrument tag numbers, locations (dimensioned from reference points) | FR-2 | 3.1 |
| Typical scale | 1:100 or 1:50 for detailed areas | PR-1 | 3.1 |
| Typical information | Instrument type, elevation (EL), access notes | FR-2 | 3.1 |

**Example 2: Instrument Installation Detail**

| Element | Description | Specification § | Procedure Step |
|---------|-------------|-----------------|----------------|
| Typical detail | Level transmitter mounting on tank nozzle | FR-3 | 3.2 |
| Content | Mounting flange, isolation valve, drain/vent, tubing/cable connection | FR-3 | 3.2 |
| References | Manufacturer installation drawing, material specification | FR-3 | 3.2 |

**Example 3: Cable Schedule**

| Element | Description | Specification § | Procedure Step |
|---------|-------------|-----------------|----------------|
| Format | Tabular format | FR-4 | 3.3 |
| Columns | Cable tag, from/to, cable type, length, routing, termination | FR-4 | 3.3 |
| Typical grouping | By area, by junction box, by cable type | FR-4 | 3.3 |
| Integration | Links to instrument list (from tag) and I/O list (to tag) | FR-4, INT-1 | 3.3 |

**Source:** **ASSUMPTION** based on typical I&C drawing content and formats

### Project-Specific Examples

**Anticipated Drawing Applications:**

**Railcar Unloading Stations (32 stations)**

| Application | Description | Specification § | Datasheet § |
|-------------|-------------|-----------------|-------------|
| Location plan | Instrument location plan showing unloading pit instrumentation layout | FR-2, FR-6 | Key Project Parameters |
| Level switches | Unloading pit sump monitoring | FR-6 | Instrumentation Types |
| Flow instruments | On unloading headers | FR-6 | Instrumentation Types |
| Pressure instruments | Pump performance monitoring | FR-6 | Instrumentation Types |
| Cable routing | Rail track area to control building | FR-4 | Installation Requirements |

**Source:** Decomposition Key Parameters — 32 railcar unloading stations (line 43); **ASSUMPTION** on typical railcar unloading instrumentation requirements

**Storage Tanks (3 × 15,000 MT)**

| Application | Description | Specification § | Datasheet § |
|-------------|-------------|-----------------|-------------|
| Tank instrumentation layout | Level transmitters (top-mounted or side-mounted), temperature elements (multiple elevations) | FR-6 | Key Project Parameters |
| Installation details | Tank roof/shell penetrations | FR-3 | Installation Requirements |
| Cable routing | Tank farm to control building | FR-4 | Installation Requirements |
| Hazardous area | Tank vapor space classification | FR-3, Standards | Conditions |

**Source:** Decomposition Key Parameters — 45,000 MT storage capacity in 3 tanks (line 40); **ASSUMPTION** on typical storage tank instrumentation

**Marine Loading Platform**

| Application | Description | Specification § | Datasheet § |
|-------------|-------------|-----------------|-------------|
| Loading arm instrumentation | Emergency shutdown valves, position switches | FR-6 | Instrumentation Types |
| Custody transfer metering | Coriolis or turbine meters, transmitters, proving connection | FR-6 | Key Project Parameters |
| Cable routing | To control system and metering computer | FR-4 | Installation Requirements |
| Marine environment | Corrosion protection, weatherproofing | FR-6 | Conditions |

**Source:** Decomposition Project Overview — "transfers from rail tank cars to liquid bulk carriers for export" (line 34); **ASSUMPTION** on typical marine loading instrumentation requirements; coordinate with PKG-11 (Marine Loading System) per decomposition (lines 240-252)

### Lessons Learned (Typical Issues)

| Issue | Problem | Solution | Specification § | Procedure Step |
|-------|---------|----------|-----------------|----------------|
| Inadequate Maintenance Clearances | Instrument located in confined space without adequate access for calibration/removal | Review instrument locations with maintenance personnel; provide platform access where needed | FR-2 | 2.1 |
| Cable Route Not Constructible | Drawing shows cable route through area with no cable tray or duct bank infrastructure | Early coordination with electrical infrastructure design (PKG-23) | FR-4, INT-1 | 2.2 |
| Hazardous Area Sealing Omitted | Conduit seals not shown on installation details for hazardous area instruments | Develop standard details for hazardous area installations per CSA C22.1; include on all applicable drawings | FR-3, Standards | 3.2 |

**Source:** **ASSUMPTION** based on typical I&C drawing lessons learned and common field issues

**Note:** Project-specific lessons learned to be captured during design and construction phases for continuous improvement.

## Project Objective Alignment

This deliverable supports the following project objectives:

| Objective | Description | How Supported | Specification § |
|-----------|-------------|---------------|-----------------|
| OBJ-1 | Safe & Reliable Operation | Proper instrumentation design and installation is fundamental to safe facility operations; clear, accurate drawings reduce installation errors and improve system reliability; as-built documentation supports ongoing maintenance and troubleshooting | FR-1 to FR-6, QR-1 to QR-4 |
| OBJ-6 | Regulatory Compliance | Drawings demonstrate compliance with electrical code (CSA C22.1) and safety standards | Standards, QR-3 |
| OBJ-7 | Environmental Protection | Proper instrumentation enables leak detection and spill prevention monitoring | FR-6 |
| OBJ-10 | Custody Transfer Accuracy | Installation details support accurate metering system installation | FR-6, INT-1 |

**Source:** Decomposition Section 6 Objective-to-Deliverable Mapping — PKG-20 supports OBJ-1 (line 780); secondary objectives based on **ASSUMPTION** regarding instrumentation role in facility operations and regulatory compliance

## Cross-Document Traceability

This Guidance document provides engineering rationale and decision context for DEL-20.01. The following documents provide complementary information:

| Document | Purpose | Key Linkages |
|----------|---------|--------------|
| Datasheet.md | Factual identification, attributes, conditions, references | Conditions § provides project context for Principles; References § lists standards for Standards Context |
| Specification.md | Requirements and verification criteria | FR-1 to FR-6 implement Principles; INT-1 to INT-2 implement Coordination Considerations; Standards § implements Standards Context |
| Procedure.md | Production workflow and verification steps | Steps 1-6 implement Principles and Considerations; Verification section implements Quality Considerations |

**Guidance-to-Specification Mapping:**

| Guidance Section | Specification Section | Rationale Provided |
|------------------|----------------------|-------------------|
| Principle 1 | FR-6 | Instrumentation serves safety and control functions |
| Principle 2 | FR-3, FR-6, Standards | Marine environment drives material and protection requirements |
| Principle 3 | FR-3, Standards | Hazardous area compliance is mandatory |
| Principle 4 | FR-2 | Accessibility is essential for installation and maintenance |
| Principle 5 | FR-5, INT-1 | Coordination prevents conflicts and rework |
| Trade-offs 1-4 | Various | Design decisions affecting cost, schedule, performance |
| Examples 1-3 | FR-2, FR-3, FR-4 | Illustrate typical drawing content and format |
