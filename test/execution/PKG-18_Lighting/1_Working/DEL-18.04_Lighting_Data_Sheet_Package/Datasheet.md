# Datasheet: DEL-18.04 Lighting Data Sheet Package

## Identification

| Field | Value |
|-------|-------|
| Deliverable ID | DEL-18.04 |
| Name | Lighting Data Sheet Package |
| Package | PKG-18 Lighting |
| Discipline | Electrical |
| Type | Data Sheet |
| Responsible | D&B Contractor |
| Status | INITIALIZED |

## Attributes

| Attribute | Value |
|-----------|-------|
| Package Contents | Light fixture data sheets, Pole data sheets per anticipated artifacts *(Source: _CONTEXT.md, Decomposition)* |
| Data Sheet Format | **TBD** — **ASSUMPTION**: Manufacturer standard product data sheets |
| Equipment Tags | **TBD** — Per lighting drawings (DEL-18.01) fixture schedule |
| Number of Fixture Types | **TBD** — Estimated 3-7 fixture types per typical lighting design |
| Number of Pole Types | **TBD** — Estimated 1-3 pole types for exterior lighting |
| Revision Control | **TBD** — Per project document control procedures |
| Classification | **TBD** — **ASSUMPTION**: For Construction / Procurement |

**Data Sheet Package Scope:**

| Category | Description |
|----------|-------------|
| LED Lighting Fixtures | Product data sheets for all fixture types specified (see Specification) |
| Lighting Poles | Product data sheets for exterior lighting poles and supports |
| Photometric Data | IES files (IESNA LM-63 format) for all fixture types |
| Certifications | CSA, UL, or other certification documents demonstrating compliance with standards |
| Installation Data | Mounting details, wiring diagrams, dimensional drawings |
| Warranty | Manufacturer warranty documentation |

## Conditions

**Operating / Environmental Context:**

This deliverable defines and substantiates lighting in accordance with ER requirements. *(Source: _CONTEXT.md, Decomposition DEL-18.04 description)*

**Project Context:**
- **Location:** Fraser Surrey Terminal, 11060 Elevator Road, Surrey, BC *(Source: Decomposition Section 1)*
- **Facility Type:** Canola Oil Transload Facility *(Source: Decomposition Section 1)*
- **Environment:** Marine terminal with outdoor exposure and industrial process areas

**Equipment Operating Conditions (typical for data sheet specifications):**

| Condition | Value |
|-----------|-------|
| Ambient Temperature Range | **TBD** — **ASSUMPTION**: -20°C to +40°C for Surrey, BC climate; fixtures rated for full output across range |
| Environmental Classification | **TBD** — Marine/industrial environment with moisture, salt spray |
| IP Rating Requirements | **TBD** — **ASSUMPTION**: IP65+ for exterior; IP54+ for interior industrial per Specification (DEL-18.02) |
| Hazardous Area Classification | **TBD** — Fixtures in classified areas require appropriate ratings (Class I Div 1/2 or Zone 0/1/2) |
| Seismic Qualification | **TBD** — Poles and fixtures designed for NBCC 2020 seismic requirements |
| Electrical Supply | **TBD** — **ASSUMPTION**: 120/208V or 347/600V per facility electrical system (PKG-17) |
| Design Life | **TBD** — **ASSUMPTION**: LED fixtures minimum 50,000 hours L70 |

**Performance Requirements (from data sheets to demonstrate):**

| Requirement | Value |
|-------------|-------|
| LED Efficacy | **TBD** — **ASSUMPTION**: Minimum 100-120 lm/W per Specification (DEL-18.02) |
| Lumen Output | **TBD** — Per fixture type and calculations (DEL-18.03) |
| Color Rendering Index (CRI) | **TBD** — **ASSUMPTION**: Minimum 70-80 per Specification |
| Color Temperature (CCT) | **TBD** — **ASSUMPTION**: 4000-5000K per Specification |
| Lumen Maintenance | **TBD** — **ASSUMPTION**: L70 ≥ 50,000 hours per Specification |
| Power Factor | **TBD** — **ASSUMPTION**: Minimum 0.90 per Specification |

## Construction

**Data Sheet Package Contents:**

Anticipated artifacts per decomposition and _CONTEXT.md:
1. **Light fixture data sheets** — Product data for all LED fixture types
2. **Pole data sheets** — Product data for exterior lighting poles and supports

**Typical Data Sheet Package Structure:**

**Section 1: LED Lighting Fixtures**
For each fixture type (per lighting drawings DEL-18.01 and specification DEL-18.02):
- **Product data sheet** showing:
  - Manufacturer, model number, description
  - Photometric performance (lumens, efficacy, distribution type)
  - Electrical characteristics (voltage, wattage, power factor, current)
  - Physical characteristics (dimensions, weight, materials, finish)
  - Environmental ratings (IP rating, operating temperature, corrosion resistance)
  - LED module specifications (CCT, CRI, lumen maintenance L70 hours)
  - Driver specifications (type, efficiency, dimming capability if applicable)
  - Mounting options and hardware
  - Optional accessories
  - Warranty terms
- **Photometric data (IES file)** per IESNA LM-63 format — used in calculations (DEL-18.03)
- **Certifications:** CSA C22.2, UL 1598, or equivalent product certification
- **Installation instructions** or reference to manufacturer installation manual
- **Dimensional drawings** showing fixture dimensions, mounting details, clearances

**Section 2: Lighting Poles**
For each pole type:
- **Product data sheet** showing:
  - Manufacturer, model, description
  - Height and configuration
  - Materials (steel, aluminum, composite) and finish (galvanized, powder-coat)
  - Wind load rating and seismic design compliance
  - Foundation requirements (base plate dimensions, anchor bolt pattern)
  - Mounting hardware for fixtures (arm length, tilt, orientation options)
  - Electrical access (hand hole location, size)
  - Grounding provisions
  - Warranty terms
- **Structural calculations or certification** demonstrating compliance with NBCC 2020 wind and seismic loads — **TBD**
- **Foundation interface details** coordinated with civil discipline (PKG-01, PKG-02, PKG-03)
- **Installation instructions**

**Section 3: Certifications and Compliance Documentation**
- **Product certifications:** CSA C22.2, UL, ETL, or equivalent for all fixtures
- **Photometric test reports:** IES LM-79 laboratory test data (if required for verification)
- **Lumen maintenance data:** IES LM-80 test data and TM-21 projections (if required)
- **Hazardous location certifications:** For fixtures in classified areas (if applicable) — **TBD**
- **Environmental compliance:** RoHS, etc. (if required) — **TBD**

**Section 4: Warranty Documentation**
- Fixture warranty certificates — **TBD** — **ASSUMPTION**: Minimum 5 years for fixtures, 3 years for drivers per Specification
- Pole warranty certificates — **TBD**
- Warranty claim procedures and contacts

**Data Sheet Package Organization:**

| Document Type | Quantity (estimated) | Purpose |
|---------------|----------------------|---------|
| Fixture product data sheets | 3-7 types | One per fixture type on lighting drawings (DEL-18.01) |
| IES photometric files | 3-7 files | One per fixture type; used in calculations (DEL-18.03) |
| Pole product data sheets | 1-3 types | One per pole type |
| Certification documents | 3-10 documents | CSA/UL certifications for fixtures and special equipment |
| Warranty documents | 3-10 documents | Warranty certificates for fixtures and poles |

**Interface Requirements:**

- **Lighting Design Drawings (DEL-18.01)** — Data sheets for fixture types shown on drawings; equipment tags match — **ASSUMPTION**
- **Lighting Technical Specification (DEL-18.02)** — Data sheets demonstrate compliance with specification requirements — **ASSUMPTION**
- **Lighting Design Calculations (DEL-18.03)** — IES photometric files from data sheets used in calculations — **ASSUMPTION**
- **Procurement/Construction** — Data sheets used for equipment procurement and verification — **ASSUMPTION**

## References

**Primary References:**
- Decomposition: `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md` — PKG-18 scope, DEL-18.04 entry
- Context: `_CONTEXT.md` — Deliverable identity and anticipated artifacts
- Specification: `Specification.md` — Requirements for data sheet package
- Guidance: `Guidance.md` — Data sheet selection and review principles
- Procedure: `Procedure.md` — Data sheet procurement and approval process

**Applicable Standards:**
- **CSA C22.2** — Electrical equipment certification standards — **ASSUMPTION**
- **UL 1598** (or CSA equivalent) — Luminaire standards — **TBD**
- **UL 924** (or CSA equivalent) — Emergency lighting equipment — **TBD**
- **IESNA LM-63** — IES photometric data file format — **ASSUMPTION**
- **IES LM-79** — Photometric and electrical testing of SSL products — **TBD**
- **IES LM-80** — Lumen maintenance testing of LED light sources — **TBD**

**Project-Specific References:**
- Employer's Requirements Volume 2 Part 1, Part 2, Part 3 — Equipment requirements and approved manufacturers (if applicable) — **TBD** — Location TBD in `0_References/`
- Approved Manufacturers List (if applicable) — **TBD**

**Cross-References (within PKG-18):**
- DEL-18.01 Lighting Design Drawing Set — Fixture types and tags; data sheets match drawing schedule
- DEL-18.02 Lighting Technical Specification — Data sheets demonstrate compliance with specification performance and material requirements
- DEL-18.03 Lighting Design Calculations — IES photometric files from data sheets used in calculations
- DEL-18.05 Lighting Installation & Test Records — Data sheets referenced during installation and testing
