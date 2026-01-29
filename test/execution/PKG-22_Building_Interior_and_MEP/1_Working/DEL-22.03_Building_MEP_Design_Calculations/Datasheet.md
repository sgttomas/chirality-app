# Datasheet: DEL-22.03 Building MEP Design Calculations

## Identification

| Field | Value |
|-------|-------|
| Deliverable ID | DEL-22.03 |
| Name | Building MEP Design Calculations |
| Package | PKG-22 Building Interior & MEP |
| Discipline | Buildings |
| Type | Calculation |
| Responsible | D&B Contractor |
| Status | INITIALIZED |

## Attributes

| Attribute | Value |
|-----------|-------|
| Calculation Number Prefix | **TBD** — Per project calculation numbering system |
| Software Used | **TBD** — **ASSUMPTION**: Carrier HAP or Trane TRACE for HVAC loads; Excel or MathCAD for plumbing sizing |
| Design Codes | NBC 2020, ASHRAE 90.1, ASHRAE 62.1, CSA B64 series (plumbing), NFPA 13 (fire protection) |
| Calculation Format | **TBD** — **ASSUMPTION**: Calculation sheets with inputs, methodology, outputs, and references |
| File Format | **TBD** — **ASSUMPTION**: Native software format + PDF for issue |
| Revision Control | **TBD** — Per project document control procedure |
| Classification | For Construction |

**Source:** Decomposition REVISED_v2.md, DEL-22.03 entry; _CONTEXT.md

## Conditions

**Operating / Environmental Context:**

This deliverable provides the engineering basis and sizing/verification calculations for building MEP systems per Employer's Requirements.

**Source:** Decomposition REVISED_v2.md, DEL-22.03 description

### Design Basis Parameters

| Condition | Value |
|-----------|-------|
| Building Type | MCC building (Motor Control Center building) |
| Location | Fraser Surrey Terminal, Surrey, BC |
| Indoor Design Temperature (Winter) | **TBD** — Per ASHRAE 90.1 and building occupancy type |
| Indoor Design Temperature (Summer) | **TBD** — Per ASHRAE 90.1 and building occupancy type |
| Outdoor Design Temperature (Winter) | **TBD** — Per NBC 2020 climate data for Surrey, BC (ASHRAE climate zone 5) |
| Outdoor Design Temperature (Summer) | **TBD** — Per NBC 2020 climate data for Surrey, BC |
| Building Occupancy Classification | **TBD** — Per NBC 2020 Part 3 (likely Group F - Industrial) |
| Occupancy Load | **TBD** — Number of occupants for ventilation calculations |
| Hazardous Area Classification | **TBD** — Per facility hazardous area study (building interior likely non-hazardous) |
| Seismic Design Category | **TBD** — Per NBC 2020, Site Class for Surrey, BC |
| Design Life | **TBD** — **ASSUMPTION**: 25 years minimum per industrial facility practice |

**Source:** NBC 2020 requirements (location TBD); ASHRAE climate data; consistent with DEL-22.01 Datasheet

### Load and Sizing Parameters

**HVAC Load Components:**
- Building envelope heat loss/gain (walls, roof, windows, doors)
- Internal heat gains (lighting, equipment, occupants)
- Ventilation loads (outdoor air per ASHRAE 62.1)
- Infiltration and exfiltration
- Safety factors and design margins

**Plumbing Sizing Parameters:**
- Fixture unit method per CSA B64 / NBC 2020
- Domestic water demand (hot and cold)
- Peak flow rates and simultaneous use factors
- Pressure requirements at fixtures
- Drainage pipe sizing per fixture units

**Fire Protection Parameters:**
- Sprinkler density and coverage area per NFPA 13
- Hydraulic calculations for pipe sizing
- Available water supply pressure and flow (from PKG-03)
- Hose stream demand

**Source:** ASHRAE Fundamentals, NBC 2020, CSA B64, NFPA 13 (locations TBD)

## Construction

**Materials / Configuration:**

### Anticipated Calculation Artifacts

Per Decomposition REVISED_v2.md, DEL-22.03 anticipated artifacts:

1. **HVAC load calculations** — Heating and cooling load calculations for equipment sizing
2. **Plumbing sizing** — Water supply and drainage pipe sizing calculations

**Source:** Decomposition REVISED_v2.md, DEL-22.03 anticipated artifacts

### Additional Calculations (Inferred from MEP Design Scope)

**ASSUMPTION**: Additional calculations likely required to fully support DEL-22.01 design and DEL-22.02 specifications:

- **Ductwork sizing** — Duct sizing for air distribution per ASHRAE/SMACNA standards
- **Ventilation calculations** — Outdoor air requirements per ASHRAE 62.1
- **Electrical load calculations** — Lighting and power loads for building services (coordinate with PKG-17)
- **Fire protection hydraulic calculations** — Sprinkler system hydraulic calculations per NFPA 13

**Source:** Inferred from DEL-22.01 scope; standard MEP calculation requirements

### Calculation Methodology and Format

**Typical Calculation Package Structure:**

1. **Cover Sheet**
   - Project identification, calculation title, revision history
   - Preparer, checker, approver signatures
   - Summary of results and conclusions

2. **Design Basis**
   - Design criteria and assumptions
   - Reference documents and standards
   - Climate data and operating conditions

3. **Input Data**
   - Building geometry and envelope properties
   - Equipment schedules and internal loads
   - Utility service parameters

4. **Calculations**
   - Methodology description
   - Step-by-step calculations or software input/output
   - Code compliance checks
   - Design margins and safety factors

5. **Results Summary**
   - Equipment sizes and capacities
   - System performance parameters
   - Comparison to design criteria

**Source:** ASSUMPTION: standard engineering calculation format; to be confirmed with project calculation standards

## References

### Project References

- Decomposition: `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md`
- Context: `_CONTEXT.md`
- Dependencies: `_DEPENDENCIES.md` (NOT_TRACKED — dependencies coordinated externally)
- Additional references: See `_REFERENCES.md` and `execution/PKG-22_Building_Interior_and_MEP/0_References/`

### Applicable Standards and Design Codes

**Primary Design Codes:**

- **NBC 2020** — National Building Code of Canada 2020 (building loads, climate data)
- **ABC 2019** — **TBD** — Identify full name and applicability (location TBD)
- **ASHRAE 90.1** — Energy Standard for Buildings (envelope performance, equipment efficiency)
- **ASHRAE 62.1** — Ventilation for Acceptable Indoor Air Quality **TBD** (location TBD)
- **ASHRAE Fundamentals Handbook** — Load calculation methodology

**Plumbing Codes:**

- **CSA B64** series — Plumbing fixture units and pipe sizing **TBD** (location TBD)
- **NBC 2020 Part 7** — Plumbing Services

**Fire Protection Codes:**

- **NFPA 13** — Installation of Sprinkler Systems (hydraulic calculations) **TBD** (location TBD)

**Source:** Applicable MEP design codes per DEL-22.01 and DEL-22.02; specific editions TBD per Employer's Requirements

### Cross-References

**Related Deliverables (within PKG-22):**

- **DEL-22.01** — Building MEP Design Drawing Set (calculations support equipment sizing shown on drawings)
- **DEL-22.02** — Building MEP Technical Specification (calculations verify specified equipment performance)
- **DEL-22.04** — Building MEP Data Sheet Package (calculations establish equipment parameters documented in datasheets)

**Related Deliverables (other packages):**

- **PKG-03** — Site Services (fire water supply pressure and flow for fire protection calculations)
- **PKG-17** — Electrical Power Distribution (electrical load coordination)
- **PKG-19** — Control Systems (HVAC control strategy inputs)
- **PKG-21** — Building Structures & Envelope (building geometry, envelope properties, internal heat gains)

**Source:** PKG-22 deliverable relationships; calculation inputs from upstream packages
