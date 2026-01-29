# Specification: DEL-18.01 Lighting Design Drawing Set

## Scope

This specification defines the requirements for the **Lighting Design Drawing Set** within **PKG-18 Lighting** for the Canola Oil Transload Facility at Fraser Surrey Terminal.

**Purpose:** Defines the design arrangement and details for lighting per ER requirements. *(Source: _CONTEXT.md, Decomposition DEL-18.01 description)*

**Package Scope:** Interior and exterior LED lighting, lighting controls, emergency lighting. *(Source: Decomposition PKG-18 scope)*

**Deliverable Artifacts:**
- Exterior lighting layout
- Interior lighting layout
- Emergency lighting layout

*(Source: _CONTEXT.md, Decomposition DEL-18.01 anticipated artifacts)*

**Inclusions:**
- Lighting fixture locations and mounting details
- Lighting pole locations and foundations (coordination with civil)
- Lighting circuits and panel assignments
- Lighting control zones and devices
- Emergency lighting and egress lighting systems
- Photometric overlays (as applicable, referencing DEL-18.03)
- Fixture schedules and equipment lists
- Installation details and typical assemblies

**Exclusions:**
- Electrical power distribution equipment (see PKG-17)
- Control system logic and programming (see PKG-19)
- Structural design of buildings (see PKG-21)
- Civil foundations design (civil to provide support; lighting to coordinate)

## Requirements

### Functional Requirements

**FR-1: Lighting Coverage**
- Drawings shall show complete lighting coverage for all exterior and interior areas requiring illumination per ER requirements — **TBD** *(Source ER location TBD)*
- Emergency lighting shall cover all egress paths and safety-critical areas per NFPA 101 and CSA C22.1 requirements — **ASSUMPTION** *(Typical code requirement)*

**FR-2: Fixture Selection and Layout**
- Fixture types, quantities, and locations shall be based on illumination calculations (DEL-18.03) to achieve required illuminance levels — **TBD** *(Source: ER requirements location TBD)*
- Fixture mounting heights and orientations shall be clearly indicated — **ASSUMPTION** *(Standard drawing practice)*

**FR-3: Circuiting and Controls**
- Drawings shall show lighting circuits, panel assignments, and control zones — **ASSUMPTION** *(Typical lighting drawing content)*
- Control devices (switches, sensors, contactors) shall be located and identified — **ASSUMPTION** *(Standard practice)*

**FR-4: Emergency Lighting**
- Emergency lighting systems shall be shown on separate layout or clearly distinguished from normal lighting — **ASSUMPTION** *(Standard practice for clarity)*
- Emergency power sources and transfer mechanisms shall be indicated or referenced — **TBD**

### Performance Requirements

**PR-1: Illumination Levels**
- Lighting design shall achieve minimum illuminance levels per:
  - Employer's Requirements — **TBD** *(ER location TBD)*
  - IESNA Lighting Handbook — **TBD** *(Standard reference location TBD)*
  - CSA C22.1 requirements for specific area types — **ASSUMPTION**

**PR-2: Uniformity and Glare Control**
- Lighting layout shall provide uniform illumination with uniformity ratios per **TBD** *(ER or industry standards)*
- Glare control measures shall be incorporated per IESNA guidelines — **TBD** *(Reference location TBD)*

**PR-3: Energy Efficiency**
- LED technology as specified in PKG-18 scope *(Source: Decomposition PKG-18 scope)*
- Lighting power density shall comply with **TBD** *(Energy code requirements - location TBD)*

**PR-4: Drawing Accuracy and Completeness**
- Drawings shall be dimensionally accurate and coordinated with architectural, structural, and civil drawings
- All fixtures, poles, and equipment shall be located with coordinates or dimensions — **ASSUMPTION** *(Standard drawing requirement)*

### Interface Requirements

**IR-1: Architectural Coordination**
- Interior lighting layouts shall be coordinated with building floor plans, ceiling plans, and reflected ceiling plans (PKG-21, PKG-22) — **ASSUMPTION**
- Fixture mounting locations shall avoid conflicts with HVAC, fire protection, and structure

**IR-2: Electrical Power Distribution**
- Lighting panel locations, feeder sizes, and circuit breaker assignments shall be coordinated with electrical power distribution drawings (PKG-17) — **ASSUMPTION**

**IR-3: Civil and Site Coordination**
- Exterior lighting pole locations and foundations shall be coordinated with site grading, paving, and underground utilities (PKG-01, PKG-02, PKG-03) — **ASSUMPTION**

**IR-4: Control Systems Integration**
- Lighting control interfaces and integration points with facility control systems (PKG-19) shall be identified — **ASSUMPTION**

**IR-5: Fire Protection and Life Safety**
- Emergency lighting shall be coordinated with fire alarm system (PKG-23) and egress routes per building code — **ASSUMPTION**

### Quality Requirements

**QR-1: Design Standards**
- All drawings shall comply with:
  - Project CAD standards — **TBD** *(Location TBD)*
  - Project drawing format and title block standards — **TBD**
  - CSA drafting symbols for electrical installations — **ASSUMPTION**

**QR-2: Checking and Coordination**
- Drawings shall undergo:
  - Self-check by originator
  - Interdisciplinary check (IDC) with affected disciplines
  - Independent peer check by qualified electrical engineer
  - Design review per project Quality Management Plan — **TBD** *(QMP location TBD)*

**QR-3: Revision Control**
- Drawing revisions shall be controlled per project document control procedures — **TBD** *(Procedure location TBD)*
- Revision clouds and descriptions shall be provided for all changes — **ASSUMPTION** *(Standard practice)*

**QR-4: Deliverable Format**
- Drawings shall be issued in:
  - Native CAD format — **TBD** *(Format to be confirmed)*
  - PDF format for review and approval — **ASSUMPTION**
  - Plot size per project standards — **TBD**

## Standards

**Applicable Codes and Standards (Electrical Discipline):**

**Primary Codes:**
- **CSA C22.1** (Canadian Electrical Code) — Governing electrical code for installations in Canada — **ASSUMPTION**
- **NBCC 2020** (National Building Code of Canada) — Building code requirements including seismic and structural — **ASSUMPTION**

**Lighting Standards:**
- **IESNA Lighting Handbook** — Illumination design criteria and calculation methods — **TBD** *(Edition and location TBD)*
- **NFPA 101** (Life Safety Code) — Emergency lighting and egress requirements — **ASSUMPTION**
- **CSA C22.2** — Electrical equipment certification standards — **ASSUMPTION**

**Design and Drafting Standards:**
- **CSA Z32** — Electrical and Electronics Diagrams — **TBD** *(If applicable, location TBD)*
- Project CAD Manual — **TBD** *(Location TBD)*
- Project Drawing Standards — **TBD** *(Location TBD)*

**Additional Standards:**
- **IEEE C2** (National Electrical Safety Code) — **ASSUMPTION** *(May apply to exterior installations)*
- **CSA Z462** — Workplace Electrical Safety — **ASSUMPTION** *(May inform maintenance access considerations)*
- **Employer's Requirements** — Project-specific requirements — **TBD** *(Vol 2 Part 1, Part 2, Part 3 — location TBD)*

**Industry Standards:**
- **IES RP-33** — Lighting for Exterior Environments — **TBD** *(If applicable, location TBD)*
- **IES RP-1** — Office Lighting — **TBD** *(If applicable for interior spaces)*

## Verification

**Verification Methods for Drawing Deliverables:**

**V-1: Design Review (Peer Check)**
- Independent review by qualified electrical engineer not involved in original design
- Verification of compliance with codes, standards, and ER requirements
- Review of calculations supporting the design (DEL-18.03) — **ASSUMPTION**

**V-2: Dimensional Verification**
- Check dimensions, coordinates, and spatial relationships
- Verify fixture locations are physically achievable and accessible — **ASSUMPTION**

**V-3: Interdisciplinary Check (IDC)**
- Coordination check with:
  - Architectural (PKG-21, PKG-22)
  - Structural (for mounting supports)
  - Civil (PKG-01, PKG-02, PKG-03 for exterior poles and foundations)
  - Electrical power (PKG-17)
  - Controls (PKG-19)
  - Fire protection (PKG-23)
- Clash detection using 3D models if available — **TBD**

**V-4: CAD Standards Compliance Check**
- Verify compliance with project CAD layer standards, symbology, text styles
- Check title block completeness and accuracy
- Validate file naming and organization — **TBD** *(Per project standards)*

**V-5: Calculation Cross-Check**
- Verify lighting layout matches illumination calculations (DEL-18.03)
- Confirm fixture counts and types match those specified in calculations — **ASSUMPTION**

**V-6: Specification Coordination**
- Verify fixture types on drawings match technical specification (DEL-18.02) and data sheets (DEL-18.04) — **ASSUMPTION**

**Acceptance Criteria:**
- All review comments closed or dispositioned
- No open IDC issues
- Calculations support design — **TBD**
- Compliance with codes and standards verified — **TBD**
- Drawings approved by discipline lead and project engineering manager — **TBD** *(Approval matrix per QMP)*

## Documentation

**Required Documentation Outputs:**

Per decomposition and _CONTEXT.md:
1. **Exterior lighting layout** — Site lighting plan
2. **Interior lighting layout** — Building lighting plans
3. **Emergency lighting layout** — Emergency egress lighting

**Supporting Documentation:**
- Lighting fixture schedule
- Lighting panel schedule (or reference to electrical schedules)
- Pole schedule (for exterior poles)
- Details and typical sections — **TBD**
- General notes and legend — **ASSUMPTION**

**Documentation Control:**
- All drawings shall be managed per project document control procedures — **TBD** *(Procedure location TBD)*
- Drawing numbering system per project standards — **TBD**
- Revision tracking and distribution per project procedures — **TBD**

**Issuance and Approval:**
- Review issue to `2_Checking/To/` for review
- Approved issue to `3_Issued/` upon acceptance — **ASSUMPTION** *(Per project workflow)*
- Retention requirements per project records management plan — **TBD**

**Electronic File Management:**
- Native CAD files stored in project document management system — **TBD** *(System and location TBD)*
- PDF copies for distribution and record — **ASSUMPTION**
- Metadata and attributes per project requirements — **TBD**
