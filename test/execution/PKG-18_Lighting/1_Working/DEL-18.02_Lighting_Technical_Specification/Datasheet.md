# Datasheet: DEL-18.02 Lighting Technical Specification

## Identification

| Field | Value |
|-------|-------|
| Deliverable ID | DEL-18.02 |
| Name | Lighting Technical Specification |
| Package | PKG-18 Lighting |
| Discipline | Electrical |
| Type | Specification |
| Responsible | D&B Contractor |
| Status | INITIALIZED |

## Attributes

| Attribute | Value |
|-----------|-------|
| Document Number | **TBD** — Per project specification numbering system |
| Specification Format | **TBD** — **ASSUMPTION**: CSI MasterFormat or project specification template |
| Specification Sections | LED lighting, lighting controls, emergency lighting per anticipated artifacts *(Source: _CONTEXT.md, Decomposition)* |
| Revision Control | **TBD** — Per project document control procedures |
| Document Format | **TBD** — **ASSUMPTION**: MS Word or PDF |
| Classification | **TBD** — **ASSUMPTION**: For Construction |
| Organization Standard | **TBD** — **ASSUMPTION**: CSI MasterFormat Division 26 (Electrical) typical for lighting specifications |

**Specification Content Attributes:**

| Attribute | Value |
|-----------|-------|
| Lighting Technology | LED per PKG-18 scope *(Source: Decomposition PKG-18 scope)* |
| Equipment Categories Covered | LED fixtures, lighting controls, emergency lighting, poles and supports per PKG-18 scope |
| Performance Basis | Illumination levels, efficacy, color rendering, control functionality per ER requirements — **TBD** *(ER location TBD)* |
| Material Requirements | Corrosion resistance, IP ratings, seismic qualifications — **ASSUMPTION** *(For marine/industrial environment)* |
| Workmanship Standards | Installation per manufacturer instructions and CSA C22.1 — **ASSUMPTION** |
| Testing and Commissioning | Illumination testing, functional testing per DEL-18.05 — **ASSUMPTION** |

## Conditions

**Operating / Environmental Context:**

This specification defines performance, materials, and workmanship requirements for lighting per ER requirements. *(Source: _CONTEXT.md, Decomposition DEL-18.02 description)*

**Project Context:**
- **Location:** Fraser Surrey Terminal, 11060 Elevator Road, Surrey, BC *(Source: Decomposition Section 1)*
- **Facility Type:** Canola Oil Transload Facility *(Source: Decomposition Section 1)*
- **Environment:** Marine terminal with outdoor exposure and industrial process areas

**Equipment Operating Conditions:**

| Condition | Value |
|-----------|-------|
| Ambient Temperature Range | **TBD** — **ASSUMPTION**: -20°C to +40°C typical for Surrey, BC climate; fixtures shall be rated for full output across this range |
| Environmental Exposure | Marine/industrial environment with moisture, salt spray, dust — **ASSUMPTION**: Fixtures require IP65+ for outdoor, IP54+ for indoor industrial areas — **TBD** |
| Hazardous Area Classification | **TBD** — Some areas may be classified per canola oil vapor zones; fixtures in classified areas require appropriate ratings (Class I Division 1/2 or Zone 0/1/2 per CSA C22.1) |
| Seismic Qualification | **TBD** — **ASSUMPTION**: Fixtures and supports designed for NBCC 2020 seismic requirements for Surrey, BC |
| Electrical Supply | **TBD** — **ASSUMPTION**: 120/208V or 347/600V 3-phase per facility electrical system (PKG-17) |
| Emergency Power | **TBD** — Emergency lighting powered by battery backup, generator, or UPS system |
| Design Life | **TBD** — **ASSUMPTION**: LED fixtures minimum 50,000 hours L70 rating; controls minimum 10-year life |

**Performance Requirements:**

| Requirement | Value |
|-------------|-------|
| LED Efficacy | **TBD** — **ASSUMPTION**: Minimum 100-120 lumens/watt for area lighting; higher for specialized fixtures |
| Color Rendering Index (CRI) | **TBD** — **ASSUMPTION**: Minimum CRI 70 for exterior; CRI 80+ for interior task areas |
| Color Temperature | **TBD** — **ASSUMPTION**: 4000-5000K typical for industrial/exterior; adjustable per area requirements |
| Lumen Maintenance | **TBD** — **ASSUMPTION**: L70 > 50,000 hours (70% lumen output after 50,000 hours) |
| Power Factor | **TBD** — **ASSUMPTION**: Minimum 0.90 for LED drivers |
| Harmonic Distortion | **TBD** — **ASSUMPTION**: THD < 20% per CSA C22.2 or IEEE standards |

## Construction

**Specification Structure:**

Anticipated artifacts per decomposition and _CONTEXT.md:
1. **LED lighting specification** — Performance, materials, and workmanship for LED fixtures and poles
2. **Lighting controls specification** — Control devices, sensors, panels, and integration requirements
3. **Emergency lighting specification** — Emergency and egress lighting fixtures, battery backup, and testing

**Typical Specification Sections (CSI MasterFormat Division 26 — Electrical):**

**For LED Lighting:**
- **TBD** — Section 26 50 00: Lighting (general)
- **TBD** — Section 26 51 00: Interior Lighting
- **TBD** — Section 26 56 00: Exterior Lighting
- **TBD** — Section 26 57 00: LED Lighting

**For Lighting Controls:**
- **TBD** — Section 26 09 00: Instrumentation and Control for Electrical Systems (if controls integrated with PKG-19)
- **TBD** — Section 26 51 00 or 26 56 00: Lighting controls as sub-section

**For Emergency Lighting:**
- **TBD** — Section 26 52 00: Emergency Lighting
- **TBD** — Battery backup systems, exit signs, egress lighting

**Specification Content Elements (typical for equipment specifications):**

**Part 1 — General:**
- Scope and related sections
- References to codes and standards (CSA C22.1, CSA C22.2, IESNA, NFPA 101, NBCC, ER)
- Submittals (product data, shop drawings, samples, test reports, O&M manuals)
- Quality assurance (manufacturer qualifications, testing requirements, certifications)
- Delivery, storage, and handling
- Warranty requirements — **TBD**

**Part 2 — Products:**
- Manufacturers (approved manufacturers list or performance-based) — **TBD**
- LED fixtures (types, performance, materials, finishes, mounting)
- LED drivers and power supplies
- Lighting poles and supports
- Lighting controls (sensors, switches, contactors, panels, software)
- Emergency lighting fixtures and battery backup systems
- Accessories and spare parts

**Part 3 — Execution:**
- Installation requirements and procedures
- Coordination with other work (electrical, civil, architectural)
- Wiring and circuiting per drawings (DEL-18.01)
- Testing and commissioning requirements (reference DEL-18.05)
- Demonstration and training

**Interface Requirements:**

- **Electrical power distribution (PKG-17)** — Supply voltages, panel capacities, circuit protection coordination
- **Control systems (PKG-19)** — Control system interfaces, communication protocols, integration points
- **Lighting design drawings (DEL-18.01)** — Fixture types, quantities, and locations match drawings
- **Lighting calculations (DEL-18.03)** — Performance requirements based on calculation results
- **Lighting data sheets (DEL-18.04)** — Equipment data sheets support specifications
- **Building construction (PKG-21, PKG-22)** — Mounting surfaces, structural supports, ceiling compatibility
- **Civil works (PKG-01, PKG-02, PKG-03)** — Pole foundations, underground conduit and wiring

## References

**Primary References:**
- Decomposition: `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md` — PKG-18 scope, DEL-18.02 entry
- Context: `_CONTEXT.md` — Deliverable identity and anticipated artifacts
- Dependencies: `_DEPENDENCIES.md` — NOT_TRACKED (dependencies coordinated externally)
- Specification: `Specification.md` — Requirements for this technical specification
- Guidance: `Guidance.md` — Principles for specification development
- Procedure: `Procedure.md` — Process for producing the specification

**Applicable Standards:**
- **CSA C22.1** (Canadian Electrical Code) — Electrical installation requirements — **ASSUMPTION**
- **CSA C22.2 No. 250.0** — LED equipment certification — **TBD** *(Specific part number TBD)*
- **UL 1598** or **CSA equivalent** — Luminaire standards — **TBD**
- **UL 924** or **CSA equivalent** — Emergency lighting equipment — **TBD**
- **IESNA** — Lighting design and performance standards — **TBD** *(Specific IES publications TBD)*
- **NFPA 101** (Life Safety Code) — Emergency lighting requirements — **ASSUMPTION**
- **NBCC 2020** — Building code requirements — **ASSUMPTION**
- **IEC 60529** — IP rating system — **ASSUMPTION** *(Referenced for enclosure protection)*

**Project-Specific References:**
- Employer's Requirements Volume 2 Part 1, Part 2, Part 3 — **TBD** — Location TBD in `0_References/`
- Project Specification Template — **TBD** *(Location and format TBD)*
- Approved Manufacturers List — **TBD** *(If applicable)*
- Project Quality Management Plan — **TBD**

**Cross-References (within PKG-18):**
- DEL-18.01 Lighting Design Drawing Set — Fixture locations, types, quantities (specification shall match drawings)
- DEL-18.03 Lighting Design Calculations — Performance basis for specification requirements
- DEL-18.04 Lighting Data Sheet Package — Equipment data sheets demonstrating compliance with specification
- DEL-18.05 Lighting Installation & Test Records — Testing and commissioning requirements specified here, executed and recorded in DEL-18.05
