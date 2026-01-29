# Specification: DEL-15.02 Pump Technical Specification

## Scope

This specification defines the requirements for the **Pump Technical Specification** within **PKG-15 Pumps & Rotating Equipment** for the Canola Oil Transload Facility at Fraser Surrey Terminal, Surrey, BC.

**Deliverable scope:** Defines performance, materials, and workmanship requirements for pumps per ER requirements.

**Source:** `_CONTEXT.md` (description), decomposition DEL-15.02 entry

### Purpose and Application

The Pump Technical Specification shall:

1. **Define procurement requirements** for pump equipment vendors
2. **Establish performance criteria** for pump selection and sizing (flow, head, NPSH, efficiency)
3. **Specify materials and construction** requirements per API 610 and applicable codes
4. **Define quality and testing** requirements for vendor shop testing and field commissioning
5. **Support equipment evaluation** during vendor proposal review and selection

**Source:** Standard purpose of technical specifications in EPC procurement process

### Equipment Covered

The specification shall cover the following pump services:

| Pump Service | Specification Document | Quantity | Typical Duty |
|-------------|------------------------|----------|--------------|
| **Railcar Unloading Pumps** | Railcar unloading pump specification | **TBD** | Transfer from railcars to storage or marine loading |
| **Marine Loading Pumps** | Marine loading pump specification | **TBD** | Transfer from storage to marine loading arms |
| **Sump Pumps** | Sump pump specification | **TBD** | Spill recovery, drainage, leak collection |
| **Transfer Pumps (if applicable)** | **TBD** — Specification to be developed if required | **TBD** | Tank-to-tank transfer or recirculation |

**Source:** `_CONTEXT.md` (anticipated artifacts); pump quantities TBD per DEL-15.03 (sizing calculations) and system design

### Included

- Performance requirements (flow, head, NPSH, efficiency, power)
- Design requirements (pump type, stages, materials, seal type, coupling, baseplate)
- Driver requirements (motor size, speed, voltage, enclosure, efficiency)
- Fabrication and materials requirements (codes, materials, welding, NDT)
- Testing requirements (shop test, performance test, vibration test)
- Documentation requirements (vendor drawings, data sheets, manuals, certifications)
- Quality assurance requirements (quality plan, inspection, test points)

**Source:** Standard content of pump technical specifications per API 610 Section 1 (scope)

### Excluded

- Installation design (covered under DEL-15.01 Pump Design Drawing Set)
- Foundation design (covered under PKG-05 Concrete Structures)
- Piping system design (covered under DEL-14 Process Piping)
- Electrical power distribution (covered under PKG-19/20 Electrical packages)
- Control system design (covered under PKG-29/30 I&C packages)
- Commissioning procedures (covered under DEL-15.05 Installation & Test Records)

**Source:** Decomposition Section 1.2 (Scope Focus: Contractor scope only); typical EPC discipline boundaries

## Requirements

### Functional Requirements

#### FR-1: Support Project Objectives

The pump specifications shall define equipment requirements to achieve:

- **OBJ-1 (Safe & Reliable Operation):** Reliable pump design per API 610; adequate seal systems; compliance with safety codes
- **OBJ-2 (Throughput Capacity):** Pump capacity and system design to support 1,000,000 MT/annum facility throughput
- **OBJ-4 (Operational Flexibility):** Pump configuration to accommodate tank storage and direct rail-to-ship transfer modes
- **OBJ-7 (Environmental Protection):** Seal systems to prevent leaks; materials compatible with containment requirements
- **OBJ-9 (Lifecycle Cost Optimization):** Energy-efficient pumps; maintainable design; standardization where feasible

**Source:** Decomposition Section 2 (Objectives), Section 6 (Objective-Deliverable Mapping for PKG-15)

#### FR-2: Define Pump Performance Requirements

For each pump service, the specification shall define:

| Requirement | Description | Data Source |
|-------------|-------------|-------------|
| **Rated Flow** | Normal operating flow rate (m³/hr or L/s) | DEL-15.03 (sizing calculations), process design |
| **Rated Head** | Total dynamic head at rated flow (m or kPa) | DEL-15.03 (system head curve) |
| **NPSH Available** | Net positive suction head available at pump suction (m) | DEL-15.03 (NPSH calculations) |
| **NPSH Required** | Vendor to provide; must be less than NPSH available with margin | Vendor data (per API 610) |
| **Minimum Flow** | Minimum continuous stable flow (to prevent recirculation) | API 610 recommendations; vendor data |
| **Maximum Flow** | Maximum flow at end of curve (typically 120% rated) | Per API 610 performance criteria |
| **Fluid Properties** | Specific gravity, viscosity, temperature, vapor pressure | ER Part 2 (process data) |
| **Operating Speed** | Pump rotational speed (RPM) — typically motor synchronous speed | Vendor proposal (optimized for duty) |

**Source:** API 610 Section 3 (hydraulic performance); data sources identified from typical pump design workflow

### Performance Requirements

#### PR-1: Hydraulic Performance Criteria (per API 610 Section 3)

| Criterion | Requirement |
|-----------|-------------|
| **Performance tolerance** | Per ISO 9906 Grade 2: Flow ±7%, Head ±5%, Efficiency (not guaranteed below stated value) |
| **NPSH margin** | NPSH available shall exceed NPSH required by minimum 0.5m (or per API 610 recommendations) |
| **Minimum continuous stable flow** | Vendor to define; pump shall operate continuously at any flow above this limit without damage |
| **Preferred operating region** | Between 70% and 120% of rated flow (per API 610) |
| **Shutoff head** | Maximum head at zero flow; shall not exceed 140% of rated head (to prevent over-pressure) |
| **Power at rated flow** | Vendor to provide; motor shall have adequate margin (typically 115% of pump BHP at rated flow) |

**Source:** API 610 Section 3.1 (performance requirements); ISO 9906 (hydraulic performance testing)

#### PR-2: Mechanical Performance Criteria (per API 610)

| Criterion | Requirement |
|-----------|-------------|
| **Vibration** | Per API 610 Figure 15 or ISO 10816 (Zone A or B limits depending on size and speed) |
| **Seal leakage** | Per API 682: visible vapor OK, liquid drips not acceptable (typical for single seal) |
| **Bearing temperature** | Per API 610 Section 5.3: Bearing temperature rise shall not exceed 50°C above ambient |
| **Coupling alignment** | Per API 610 Section 6.3: Alignment per manufacturer recommendations (dial indicator or laser) |
| **Noise level** | **TBD** — Per WorkSafeBC limits (typically 85 dBA at 1m for continuous exposure) |

**Source:** API 610 Sections 5.3 (bearings), 6.9 (vibration), Figure 15 (vibration limits); API 682 (seal performance)

### Interface Requirements

#### IF-1: Piping Interface

Specification shall define:

- **Suction and discharge nozzle sizes** (based on piping velocity criteria: typically 1–3 m/s suction, 2–4 m/s discharge)
- **Flange ratings** per ASME B16.5 (Class 150, 300, or as required by system pressure)
- **Flange facing** (raised face, flat face, RTJ per piping specification)
- **Nozzle orientation** (horizontal, vertical, or as required by layout) — coordinate with DEL-15.01
- **Allowable nozzle loads** per API 610 Section 4.2.9 (vendor to provide; piping design to comply per ASME B31.3)

**Source:** API 610 Section 4.2 (nozzles); ASME B16.5 (flange standards); coordinate with DEL-14 (piping design)

#### IF-2: Foundation and Mounting Interface

Specification shall define:

- **Baseplate type** (fabricated steel, common baseplate for pump and motor)
- **Foundation loads** (static and dynamic) — vendor to provide for foundation design (PKG-05)
- **Anchor bolt requirements** (number, size, material) — vendor to provide; structural to design embedment
- **Grouting requirements** per API 610 Section 6.1.4 (non-shrink grout, minimum thickness 25mm)

**Source:** API 610 Section 4.1 (baseplates), Section 6.1.4 (grouting); coordinate with DEL-15.01 (arrangement) and PKG-05 (foundations)

### Quality Requirements

#### QR-1: Design and Fabrication Quality

- All pumps shall comply with API 610 design requirements (latest edition per ER)
- Fabrication per API 610 Section 4 (materials, welding, NDT)
- Welding per ASME Section IX (qualified procedures and welders)
- Materials per ASTM specifications and API 610 Annex G
- Vendor quality plan per API 610 Section 8.1 (quality assurance requirements)

**Source:** API 610 Sections 4 (design and fabrication) and 8 (quality assurance)

#### QR-2: Inspection and Testing Requirements

**Shop testing (per API 610 Section 7):**

| Test | Requirement | Acceptance Criteria |
|------|-------------|---------------------|
| **Hydrostatic test** | 1.5× design pressure (minimum) | No leaks, no visible distortion |
| **Performance test** | At rated flow and 2 additional points (70%, 120% of rated) | Within ISO 9906 Grade 2 tolerances |
| **Vibration test** | During performance test | Per API 610 Figure 15 or ISO 10816 |
| **NPSH test** | **TBD** — Required if critical NPSH service | NPSH required verified per API 610 Section 7.4 |
| **Seal test** | Seal system operation during performance test | No visible liquid leakage per API 682 |

**Source:** API 610 Section 7 (shop tests); ISO 9906 (performance test); API 682 (seal test)

## Standards

### Primary Standards

- **API 610** (latest edition) — Centrifugal Pumps for Petroleum, Petrochemical and Natural Gas Industries
- **API 682** (latest edition) — Pumps—Shaft Sealing Systems for Centrifugal and Rotary Pumps
- **ASME B31.3** — Process Piping (nozzle loads, flange requirements)
- **ASME B16.5** — Pipe Flanges and Flanged Fittings
- **ISO 9906** — Rotodynamic Pumps—Hydraulic Performance Acceptance Tests
- **ISO 10816** — Mechanical Vibration—Evaluation of Machine Vibration
- **NEMA MG 1** or **IEC 60034** — Rotating Electrical Machines (motor standards)

**Source:** Primary industry standards for centrifugal pump procurement

### Canadian Codes

- **NBC 2015** — National Building Code of Canada (seismic anchorage)
- **CSA B51** — Boiler, Pressure Vessel, and Pressure Piping Code
- **CSA C22.1** — Canadian Electrical Code
- **WorkSafeBC** — Occupational Health and Safety Regulation

**Source:** Applicable Canadian codes for BC industrial facilities

## Verification

### Specification Development Verification

| Requirement Category | Verification Method | Acceptance Criteria |
|---------------------|---------------------|---------------------|
| **Performance requirements** | Review against DEL-15.03 (calculations) | Flow, head, NPSH values match sizing calculations |
| **Material requirements** | Review against ER Part 2 and API 610 | Materials appropriate for CSD canola oil service |
| **Interface requirements** | IDC review with piping, electrical, I&C disciplines | Interfaces coordinated and consistent |
| **Code compliance** | Independent check by qualified engineer | Compliance with API 610, API 682, and applicable codes verified |
| **Completeness** | Specification checklist review | All required sections included |

**Source:** Standard specification development verification process

### Vendor Proposal Evaluation Verification

Specification shall define evaluation criteria for vendor proposals:

| Evaluation Criterion | Requirement | Weight |
|---------------------|-------------|--------|
| **Technical compliance** | Pump meets performance requirements | High |
| **Code compliance** | Pump complies with API 610 and applicable standards | High |
| **Quality** | Vendor quality plan and past performance acceptable | Medium |
| **Delivery schedule** | Delivery meets project schedule requirements | Medium |
| **Price** | Competitive pricing within budget | Medium |

**Source:** Typical vendor proposal evaluation criteria

## Documentation

### Specification Document Deliverables

The following specification documents shall be produced:

1. **Railcar Unloading Pump Specification** — Performance, materials, and testing requirements for railcar unloading service
2. **Marine Loading Pump Specification** — Performance, materials, and testing requirements for marine loading service
3. **Sump Pump Specification** — Performance, materials, and testing requirements for sump/drainage service

**Source:** `_CONTEXT.md` (anticipated artifacts)

### Vendor Documentation Requirements

Vendor shall provide:

- **Outline drawings** (general arrangement, nozzle schedule, weights)
- **Cross-sectional drawings** (pump internals)
- **Performance curves** (head-flow-efficiency-power-NPSH)
- **Foundation loads** (static and dynamic)
- **Data sheets** (equipment technical data)
- **O&M manuals** (operation, maintenance, troubleshooting, spare parts)
- **Material certifications** (material test reports)
- **Test reports** (hydrostatic, performance, vibration)

**Source:** API 610 Section 8.2 (technical data); typical vendor deliverables

---

**Document Status:** ENRICHED (Pass 1)
**Enrichment Date:** 2026-01-28
**Agent:** 4_DOCUMENTS enrichment cycle

**Cross-References:**
- Datasheet.md — Equipment attributes, materials, operating conditions
- Guidance.md — Design principles, material selection rationale, trade-offs
- Procedure.md — Specification development process and verification steps
- DEL-15.01 — Pump Design Drawing Set
- DEL-15.03 — Pump Design Calculations
- DEL-15.04 — Pump Data Sheet Package
- DEL-15.05 — Pump Installation & Test Records
