# Datasheet: DEL-22.04 Building MEP Data Sheet Package

## Identification

| Field | Value |
|-------|-------|
| Deliverable ID | DEL-22.04 |
| Name | Building MEP Data Sheet Package |
| Package | PKG-22 Building Interior & MEP |
| Discipline | Buildings |
| Type | Data Sheet |
| Responsible | D&B Contractor |
| Status | INITIALIZED |

## Attributes

| Attribute | Value |
|-----------|-------|
| Data Sheet Number Prefix | **TBD** — Per project data sheet numbering system |
| Data Sheet Format | **TBD** — **ASSUMPTION**: Standardized forms per project data sheet templates |
| File Format | **TBD** — **ASSUMPTION**: Excel or PDF forms |
| Revision Control | **TBD** — Per project document control procedure |
| Classification | For Construction |
| Equipment Tag Prefix | **TBD** — Per project equipment tagging system (e.g., HV- for HVAC, P- for plumbing, FP- for fire protection) |

**Source:** Decomposition REVISED_v2.md, DEL-22.04 entry; _CONTEXT.md

## Conditions

**Operating / Environmental Context:**

This deliverable defines and substantiates building MEP equipment in accordance with Employer's Requirements.

**Source:** Decomposition REVISED_v2.md, DEL-22.04 description

### Purpose and Use

| Purpose | Description |
|---------|-------------|
| Equipment Specification | Defines required performance, capacity, and features for MEP equipment |
| Procurement Guidance | Provides technical basis for vendor quotations and equipment procurement |
| Performance Baseline | Establishes acceptance criteria for vendor-supplied equipment |
| Operations Reference | Documents installed equipment parameters for future operations and maintenance |

**Source:** ASSUMPTION: standard equipment data sheet purposes in EPC projects

### Applicable System Context

Per Decomposition PKG-22 scope and DEL-22.01/22.02, this data sheet package addresses:

| MEP System | Equipment Types |
|------------|----------------|
| HVAC | Rooftop units, split systems, air handling units, exhaust fans, ductwork accessories |
| Plumbing | Water heaters, pumps, pressure boosters, backflow preventers, fixtures |
| Fire Suppression | Fire pumps (if required), sprinkler heads, alarm valves, flow switches, tamper switches |
| Electrical Building Services | Lighting fixtures, panels, transformers (coordinate with PKG-17) |

**Source:** Decomposition REVISED_v2.md, PKG-22 scope; DEL-22.01 anticipated artifacts

### Environmental Context (for Equipment Selection)

| Condition | Value |
|-----------|-------|
| Building Type | MCC building (Motor Control Center building) and other facility buildings |
| Location | Fraser Surrey Terminal, Surrey, BC (marine/industrial environment) |
| Indoor Operating Temperature | **TBD** — Per ASHRAE 90.1 and building occupancy type |
| Outdoor Operating Temperature Range | **TBD** — Per NBC 2020 climate data for Surrey, BC (winter: ~-10°C, summer: ~+30°C typical) |
| Humidity | **TBD** — Indoor humidity control requirements per building function |
| Hazardous Area Classification | **TBD** — Per facility hazardous area study (building interior likely non-hazardous, but verify for equipment ratings) |
| Seismic Design Category | **TBD** — Per NBC 2020, Site Class for Surrey, BC (equipment seismic certification may be required) |
| Design Life | **TBD** — **ASSUMPTION**: 25 years minimum per industrial facility practice |
| Corrosion Environment | Moderate (coastal proximity at Fraser River / Strait of Georgia) — equipment materials and coatings may require corrosion resistance |

**Source:** NBC 2020 requirements (location TBD); Decomposition project location; consistent with DEL-22.01/22.03 Datasheets

## Construction

**Materials / Configuration:**

### Anticipated Data Sheet Artifacts

Per Decomposition REVISED_v2.md, DEL-22.04 anticipated artifacts:

1. **HVAC equipment datasheets** — Heating, ventilation, and air conditioning units and accessories
2. **Plumbing equipment datasheets** — Plumbing fixtures, water heaters, pumps, and accessories
3. **Fire suppression system datasheets** — Sprinkler system components and equipment

**Source:** Decomposition REVISED_v2.md, DEL-22.04 anticipated artifacts

### Typical Data Sheet Content Structure

**ASSUMPTION**: Standard equipment data sheet format to be confirmed with project data sheet templates:

Each equipment data sheet typically includes:

1. **Identification**
   - Equipment tag number
   - Service description
   - Location
   - Equipment type and classification

2. **Required Performance**
   - Capacity (heating/cooling, flow, pressure, etc.)
   - Operating conditions (temperature, pressure, flow)
   - Efficiency requirements (per ASHRAE 90.1 or project criteria)
   - Control requirements (interface to PKG-19)

3. **Materials and Construction**
   - Materials of construction (for corrosion resistance, durability)
   - Pressure ratings and temperature ratings
   - Certifications required (UL, FM, CSA, etc.)

4. **Vendor Information**
   - Proposed manufacturer and model
   - Vendor data sheet reference
   - Performance curves (pumps, fans)
   - Submittal status

5. **Utilities and Connections**
   - Electrical power requirements (voltage, phase, FLA, MCA)
   - Water connections (size, pressure)
   - Control and monitoring interfaces
   - Mounting and support requirements

6. **Notes and Special Requirements**
   - Installation requirements
   - Testing and commissioning requirements
   - Spare parts recommendations
   - Warranty requirements

**Source:** ASSUMPTION: standard equipment data sheet structure; industry practice

### Equipment Types and Typical Data Sheets

**HVAC Equipment Data Sheets**:
- Packaged rooftop HVAC units (heating, cooling, ventilation)
- Split system air conditioners (if applicable)
- Exhaust fans (for ventilation and equipment cooling)
- Unit heaters (if applicable for warehouse/garage areas)
- Ductwork accessories (dampers, diffusers, grilles)

**Plumbing Equipment Data Sheets**:
- Electric or gas water heaters (if required)
- Domestic water pumps or boosters (if required for pressure)
- Backflow preventers (for potable water protection)
- Plumbing fixtures (water closets, lavatories, sinks, safety showers)
- Mixing valves and controls

**Fire Suppression Equipment Data Sheets**:
- Fire pumps (if required; coordinate with PKG-03 for water supply adequacy)
- Sprinkler heads (type, temperature rating, coverage)
- Alarm valves and control valves
- Flow switches and tamper switches
- Fire department connections

**Source:** Inferred from DEL-22.01 scope; standard MEP equipment types

## References

### Project References

- Decomposition: `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md`
- Context: `_CONTEXT.md`
- Dependencies: `_DEPENDENCIES.md` (NOT_TRACKED — dependencies coordinated externally)
- Additional references: See `_REFERENCES.md` and `execution/PKG-22_Building_Interior_and_MEP/0_References/`

### Applicable Standards and Equipment Codes

**Equipment Standards and Certifications:**

- **UL** (Underwriters Laboratories) — Equipment safety certifications (HVAC, electrical, fire protection)
- **FM** (Factory Mutual) — Fire protection equipment approvals
- **CSA** (Canadian Standards Association) — Equipment standards and certifications for Canada
- **ASHRAE 90.1** — Equipment efficiency requirements (HVAC equipment, lighting)
- **NFPA 13** — Fire protection equipment requirements (sprinkler heads, control valves)
- **CSA B64** series — Plumbing fixture standards
- **CEC** — Canadian Electrical Code (equipment electrical ratings)

**Source:** Applicable equipment standards per industry practice; specific editions TBD per DEL-22.02 and Employer's Requirements

### Cross-References

**Related Deliverables (within PKG-22):**

- **DEL-22.01** — Building MEP Design Drawing Set (data sheets document equipment shown on drawings)
- **DEL-22.02** — Building MEP Technical Specification (data sheets detail items specified in specifications)
- **DEL-22.03** — Building MEP Design Calculations (calculations establish equipment capacities documented in data sheets)
- **DEL-22.05** — Building MEP Installation and Test Records (testing verifies equipment performs per data sheet requirements)
- **DEL-22.06** — Building MEP Shop Design Drawing Set (shop drawings provide fabrication details for equipment documented in data sheets)

**Related Deliverables (other packages):**

- **PKG-03** — Site Services (utility service parameters for equipment connections: fire water, domestic water, sanitary sewer)
- **PKG-17** — Electrical Power Distribution (electrical power requirements for MEP equipment)
- **PKG-19** — Control Systems (control and monitoring interfaces for HVAC equipment)
- **PKG-21** — Building Structures & Envelope (equipment locations, support requirements, architectural coordination)

**Source:** PKG-22 deliverable relationships; equipment data coordination with upstream and downstream packages
