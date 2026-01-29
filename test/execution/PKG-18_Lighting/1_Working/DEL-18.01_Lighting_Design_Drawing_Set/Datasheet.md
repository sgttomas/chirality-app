# Datasheet: DEL-18.01 Lighting Design Drawing Set

## Identification

| Field | Value |
|-------|-------|
| Deliverable ID | DEL-18.01 |
| Name | Lighting Design Drawing Set |
| Package | PKG-18 Lighting |
| Discipline | Electrical |
| Type | Drawing |
| Responsible | D&B Contractor |
| Status | INITIALIZED |

## Attributes

| Attribute | Value |
|-----------|-------|
| Drawing Number Prefix | **TBD** — Per project drawing numbering system |
| Sheet Size | **TBD** — **ASSUMPTION**: ANSI D or ISO A1 typical for facility layouts |
| Scale | **TBD** — **ASSUMPTION**: 1:100 or 1:200 for site plans; 1:50 for details |
| CAD Software | **TBD** — **ASSUMPTION**: AutoCAD or Revit per project CAD manual (see Procedure Step 4) |
| Drawing Format | **TBD** — **ASSUMPTION**: PDF and native CAD format (see Specification Documentation section) |
| Revision Control | **TBD** — Per project document control procedures (see Procedure Step 9) |
| Classification | **TBD** — **ASSUMPTION**: For Construction |
| Coordinate System | **TBD** — **ASSUMPTION**: Project datum per site survey (PKG-01); required for exterior pole locations (see Procedure Step 1) |
| Drawing Symbology | **TBD** — **ASSUMPTION**: CSA Z32 or project standard symbols (see Specification Standards section) |

**Lighting System Attributes:**

| Attribute | Value |
|-----------|-------|
| Lighting Technology | LED per PKG-18 scope *(Source: Decomposition PKG-18 scope)* — See Guidance P-2 for rationale |
| Lighting Zones | Exterior, Interior, Emergency per anticipated artifacts *(Source: _CONTEXT.md, Decomposition)* — See Procedure Step 1 for zone identification |
| Control System | Lighting controls included per PKG-18 scope *(Source: Decomposition PKG-18 scope)* — See Guidance P-4 for control principles |
| Power Supply Voltage | **TBD** — **ASSUMPTION**: 120/208V or 347/600V per facility electrical system (PKG-17) |
| Emergency Power Source | **TBD** — Emergency lighting supplied by emergency power system (battery, generator, or UPS) — See Guidance P-3 |
| Illumination Calculation Software | **TBD** — **ASSUMPTION**: AGi32, DIALux, or similar per Procedure Step 3 |

## Conditions

**Operating / Environmental Context:**

This drawing set defines the design arrangement and details for lighting per ER requirements. *(Source: _CONTEXT.md, Decomposition DEL-18.01 description)*

**Project Context:**
- **Location:** Fraser Surrey Terminal, 11060 Elevator Road, Surrey, BC *(Source: Decomposition Section 1)*
- **Facility Type:** Canola Oil Transload Facility *(Source: Decomposition Section 1)*
- **Environment:** Marine terminal with outdoor exposure and industrial process areas — See Guidance C-1 for environmental considerations

**Design Conditions:**

| Condition | Value |
|-----------|-------|
| Operating Temperature Range | **TBD** — **ASSUMPTION**: -20°C to +40°C typical for Surrey, BC climate (see Guidance C-1) |
| Environmental Classification | **TBD** — Marine/industrial environment with potential exposure to moisture, salt spray (see Guidance C-1) |
| Hazardous Area Classification | **TBD** — To be confirmed per facility hazardous area classification study (anticipated in PKG-17 or PKG-24); affects fixture selection per Guidance C-2 and Specification IR-4 |
| Seismic Requirements | **TBD** — **ASSUMPTION**: Per NBCC 2020 for Surrey, BC location (see Guidance C-1) |
| Wind Loading | **TBD** — For exterior pole-mounted fixtures per NBCC 2020 (see Guidance C-1) |
| Design Life | **TBD** — **ASSUMPTION**: 25+ years typical for LED systems |

**Illumination Requirements:**

| Area Type | Illumination Level | Reference |
|-----------|-------------------|-----------|
| Exterior Process Areas | **TBD** | ER requirements, CSA C22.1, IESNA — See Specification PR-1 |
| Interior Areas | **TBD** | ER requirements, CSA C22.1, IESNA — See Specification PR-1 |
| Emergency Egress Paths | **TBD** | NFPA 101, CSA C22.1 — See Specification FR-4 and Guidance P-3 |
| Security/Perimeter | **TBD** | ER requirements — See Guidance C-5 |

## Construction

**Drawing Set Components:**

Anticipated artifacts per decomposition and _CONTEXT.md:
1. **Exterior lighting layout** — Site lighting plan showing exterior fixtures, poles, circuiting (see Guidance E-3.1)
2. **Interior lighting layout** — Building lighting plans showing interior fixtures, controls (see Guidance E-3.2)
3. **Emergency lighting layout** — Emergency and egress lighting systems (see Guidance E-3.3)

**Additional Drawing Requirements (typical for lighting design sets):**

- **TBD** — Lighting fixture schedules and specifications (referenced in Procedure Step 4)
- **TBD** — Pole foundation details (coordination interface per Guidance E-4)
- **TBD** — Lighting control diagrams (per Specification FR-3)
- **TBD** — One-line diagrams showing lighting panel feeders
- **TBD** — Details and typical installations
- **TBD** — Photometric analysis overlays (may reference DEL-18.03 calculations per Procedure Step 3)

**Drawing Production:**

| Aspect | Requirement |
|--------|-------------|
| Software | **TBD** — Per project CAD standards (see Procedure Step 4) |
| Layer Standards | **TBD** — Per project CAD layer naming convention (see Specification QR-1 and Procedure Step 4) |
| Title Block | **TBD** — Per project drawing template (see Procedure Step 4) |
| Symbol Library | **TBD** — **ASSUMPTION**: CSA Z32 or project standard symbols (see Specification Standards section) |
| Annotations | **TBD** — Text height and style per project standards (see Specification QR-1) |

**Interface Requirements:**

The following interfaces are critical and detailed in Specification IR sections and Guidance C-3:

- **Architectural drawings** — Building layouts for interior lighting (PKG-21, PKG-22) — See Specification IR-1 and Procedure Step 6
- **Electrical power distribution** — Panel locations and circuits (PKG-17) — See Specification IR-2 and Procedure Step 1
- **Site civil drawings** — Grading, underground utilities for exterior lighting (PKG-01, PKG-02, PKG-03) — See Specification IR-3 and Procedure Step 6
- **Control systems** — Integration with facility controls (PKG-19) — See Specification IR-4 and Procedure Step 1
- **Fire protection** — Emergency lighting coordination (PKG-23) — See Specification IR-5 and Procedure Step 6

## References

**Primary References:**
- Decomposition: `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md` — PKG-18 scope, DEL-18.01 entry
- Context: `_CONTEXT.md` — Deliverable identity and anticipated artifacts
- Dependencies: `_DEPENDENCIES.md` — NOT_TRACKED (dependencies coordinated externally)
- Specification: `Specification.md` — Requirements for this drawing set
- Guidance: `Guidance.md` — Design principles and considerations
- Procedure: `Procedure.md` — Production and management process

**Applicable Standards:**
- CSA C22.1 (Canadian Electrical Code) — **ASSUMPTION**: Governing electrical code for Canada (see Specification Standards section)
- CSA C22.2 — **ASSUMPTION**: Electrical equipment standards
- CSA Z32 — **TBD**: Electrical and Electronics Diagrams (see Specification Standards section)
- IESNA Lighting Handbook — **TBD** — **ASSUMPTION**: Industry standard for illumination design (see Specification Standards section)
- NFPA 101 (Life Safety Code) — **ASSUMPTION**: Emergency lighting requirements (see Specification FR-4)
- NBCC 2020 (National Building Code of Canada) — **ASSUMPTION**: Structural and seismic requirements for poles

**Project-Specific References:**
- Employer's Requirements Volume 2 Part 1, Part 2, Part 3 — **TBD** — Location TBD in `0_References/` (see Procedure Step 1)
- Project CAD Standards Manual — **TBD** (referenced in Specification QR-1 and Procedure Step 4)
- Project Design Basis — **TBD** (if applicable)
- Site survey and as-built drawings — **TBD** (see Procedure Step 1)
- Hazardous area classification drawings — **TBD** (see Procedure Step 1 and Guidance C-2)

**Cross-References (within PKG-18):**
- DEL-18.02 Lighting Technical Specification — Performance requirements (see Specification and Procedure)
- DEL-18.03 Lighting Design Calculations — Illumination analysis (see Procedure Step 3 and Specification V-5)
- DEL-18.04 Lighting Data Sheet Package — Equipment specifications (see Specification V-6)
- DEL-18.05 Lighting Installation & Test Records — Installation verification (referenced in Procedure Records section)
