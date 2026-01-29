# Guidance: DEL-22.03 Building MEP Design Calculations

## Purpose

This guidance document supports the development of **Building MEP Design Calculations** for **PKG-22 Building Interior & MEP**.

**Deliverable Purpose:** Provides the engineering basis and sizing/verification calculations for building MEP per Employer's Requirements.

**Source:** Decomposition REVISED_v2.md, DEL-22.03 entry; _CONTEXT.md

### Role in Project Delivery

These calculations serve as the technical foundation for MEP design. They provide:

- **Equipment sizing justification** for selections shown in DEL-22.01 drawings and DEL-22.04 datasheets
- **Code compliance demonstration** for NBC 2020, ASHRAE, NFPA 13, and other applicable standards
- **Design basis documentation** for future modifications and operations
- **Quality assurance** through independent verification of design assumptions and results
- **Professional liability protection** by demonstrating due diligence and professional standard of care

**Deliverable Classification:**
- **Type:** Calculation
- **Discipline:** Buildings
- **Responsible Party:** D&B Contractor

**Source:** Standard EPC deliverable purposes; _CONTEXT.md

## Principles

### Purpose and Role of Design Calculations

**Engineering Foundation:**

Design calculations translate design requirements (from Employer's Requirements and codes) into specific equipment sizes and system parameters. They provide the technical justification that bridges conceptual requirements to physical design.

**Source:** ASSUMPTION: standard engineering calculation purpose

### HVAC Load Calculation Principles

**Climate Context**: Surrey, BC (ASHRAE Climate Zone 5) requires heating for winter conditions and potentially cooling for internal heat loads from electrical equipment in MCC building.

**Load Components:**

1. **Envelope Loads**: Heat transfer through walls, roof, windows, doors based on construction materials and climate
2. **Internal Gains**: Heat from lighting, equipment (MCC electrical equipment can be significant), occupants
3. **Ventilation Loads**: Energy required to condition outdoor air per ASHRAE 62.1
4. **Infiltration**: Uncontrolled air leakage through building envelope

**Calculation Methodology** (per ASHRAE Fundamentals):
- **Heating Load**: Peak heating capacity during design winter conditions
- **Cooling Load**: Peak cooling capacity considering solar gains, internal loads, and outdoor air
- **Diversity Factors**: Recognition that not all loads occur simultaneously
- **Design Margins**: Typical 10-15% margin for equipment selection

**Source:** ASHRAE Fundamentals Handbook; ASHRAE 90.1; industry standard practice

### Plumbing Sizing Principles

**Fixture Unit Method** (per CSA B64 / NBC 2020):

- Assigns fixture units to each plumbing fixture based on water demand
- Sums fixture units for pipe sections
- Uses lookup tables to determine pipe size for combined fixture units
- Accounts for simultaneous use probability (diversity)

**Key Considerations:**
- **Pressure Requirements**: Minimum pressure at fixtures (typically 200-275 kPa)
- **Pressure Losses**: Friction losses in piping, fittings, valves, elevation changes
- **Available Supply Pressure**: From site water main (coordinate with PKG-03)
- **Peak Demand**: Simultaneous use factors based on building type and fixture count

**Drainage Sizing:**
- Based on drainage fixture units per NBC 2020 / CSA B64
- Slope requirements for gravity drainage (minimum 1-2% slope)
- Vent sizing for proper trap operation

**Source:** NBC 2020, CSA B64 standards; standard plumbing design methodology

### Fire Protection Calculation Principles

**NFPA 13 Hydraulic Calculation Method:**

Fire sprinkler systems require hydraulic calculations to verify adequate water supply pressure and flow can support the most hydraulically demanding sprinkler zone (design area).

**Calculation Process:**
1. **Identify Design Area**: Most hydraulically remote area requiring highest pressure
2. **Sprinkler Demand**: Number of sprinklers × flow per sprinkler (based on density and coverage area)
3. **Pipe Friction Losses**: Hazen-Williams equation for pressure loss through piping network
4. **Elevation Losses**: Pressure loss/gain due to elevation changes
5. **Required Pressure at Source**: Sum of sprinkler discharge pressure + all losses
6. **Hose Stream Demand**: Additional flow for fire department connections

**Comparison to Available Supply**: Calculated demand must be less than available water supply from PKG-03 site fire water system.

**Source:** NFPA 13 requirements; standard fire protection hydraulic calculation methodology

### Calculation Methodology Standards

**Recognized Methods:**

- **Code-Prescribed Methods**: Use methods explicitly described in applicable codes (NBC 2020, ASHRAE, NFPA 13)
- **Industry Standard Methods**: Use methods published by recognized authorities (ASHRAE, SMACNA, etc.)
- **Software Calculations**: Use validated software with documented methodology
- **First Principles**: Use fundamental physics and engineering principles with clear derivations

**Source:** Standard engineering calculation practice

### Code Compliance Through Calculations

Calculations demonstrate code compliance by:

- **NBC 2020**: Using prescribed load tables, climate data, fixture unit tables
- **ASHRAE 90.1**: Demonstrating equipment efficiency meets minimum requirements
- **ASHRAE 62.1**: Calculating required ventilation rates and demonstrating system provides adequate outdoor air
- **NFPA 13**: Following prescribed hydraulic calculation methodology and demonstrating adequate water supply

**Source:** Applicable codes and standards

## Considerations

### Factors to Consider During Development

#### Design Basis Establishment

**Critical Inputs** (see Datasheet.md, Design Basis Parameters):

- Building geometry and envelope properties (from PKG-21)
- Indoor design conditions (temperature, humidity, air quality requirements)
- Outdoor design conditions (from NBC 2020 climate data for Surrey, BC)
- Occupancy and internal loads (lighting, equipment, people)
- Utility service parameters (from PKG-03)

**Source:** Datasheet.md; standard calculation inputs

#### Interface Coordination

**Critical Interfaces** (see Specification.md, Interface Requirements):

1. **PKG-03 (Site Services)**:
   - Fire water supply pressure and flow availability
   - Domestic water supply parameters
   - Sanitary sewer invert elevations

2. **PKG-21 (Building Structures & Envelope)**:
   - Building geometry and floor plans
   - Envelope construction and thermal properties
   - Internal heat loads from architectural/electrical layouts

3. **PKG-17 (Electrical Power Distribution)**:
   - Electrical loads for HVAC equipment (coordination)
   - Internal heat gains from electrical equipment

4. **PKG-19 (Control Systems)**:
   - Control strategy affecting ventilation and equipment operation

**Coordination Method**: Dependencies tracked externally (NOT_TRACKED mode per `_DEPENDENCIES.md`). Coordinate through design meetings and interface registers.

**Source:** Package scope interfaces; Specification.md IF-04

#### Calculations and Drawings Coordination

Calculations must support DEL-22.01 drawings:

- Equipment sizes on drawings must match calculation results
- System capacities shown on schedules must be consistent with calculations
- Design notes on drawings should reference supporting calculations
- Any deviations between calculations and drawings must be resolved

**Source:** Specification.md IF-01; DEL-22.01 Specification QR-06

#### Calculations and Specifications Coordination

Calculations must verify DEL-22.02 specifications:

- Equipment performance requirements specified must be achievable per calculations
- Material selections must be adequate for calculated conditions (pressure, temperature, flow)
- Installation requirements must support calculated system performance

**Source:** Specification.md IF-02; DEL-22.02 Specification IF-02

#### Calculations and Equipment Selection

Calculations establish parameters for DEL-22.04 equipment datasheets:

- Calculated equipment capacities become datasheet "required" parameters
- Vendor-provided equipment must meet or exceed calculated requirements
- Operating conditions (pressure, temperature, flow) must be within equipment capabilities

**Source:** Specification.md IF-03

### Calculation Documentation Standards

**Traceability Requirements:**

Every calculation should answer:
1. **What is being calculated?** (clear objective and scope)
2. **Why is it needed?** (reference to design requirement or code)
3. **What method is used?** (reference to code, standard, or recognized methodology)
4. **What are the inputs?** (data with sources cited)
5. **What are the assumptions?** (documented with justification)
6. **What are the results?** (clear summary)
7. **Who prepared, checked, and approved?** (signatures and dates)

**Source:** ASSUMPTION: standard calculation documentation best practices

### Quality Assurance for Calculations

**Independent Check Process:**

- Checker must be qualified engineer not involved in original calculation preparation
- Checker verifies: methodology selection, input data, assumptions, calculation steps, results reasonableness
- Checker does not simply "approve" but actively verifies and challenges assumptions
- Checker comments must be resolved and documented

**Why Independent Check Matters:**
- Catches errors before design is issued for construction
- Provides professional liability protection
- Demonstrates due diligence and quality assurance
- Required by most project quality management plans

**Source:** ASSUMPTION: standard engineering quality assurance; Specification.md QR-01

## Trade-offs

### Competing Concerns to Evaluate

#### Design Margins vs. Equipment Cost

**Decision Point**: How much margin to include in equipment sizing beyond calculated peak load

**Trade-off**:
- **Larger margins** (15-20% or more): Provide more operational flexibility, accommodate future changes, reduce risk of undersizing, but increase capital cost and may reduce equipment efficiency at typical part-load operation
- **Smaller margins** (5-10%): Reduce capital cost, improve part-load efficiency, but provide less flexibility and higher risk if loads were underestimated

**Recommendation**:
- **Critical systems** (e.g., MCC building cooling for equipment protection): Use conservative margins (15-20%)
- **Non-critical systems** (e.g., comfort cooling for break rooms): Use standard margins (10-15%)
- **TBD** — Project-specific margin requirements per Employer's Requirements (location TBD)

**Source:** ASSUMPTION: standard design margin practice; specific requirements TBD

#### Calculation Detail vs. Schedule

**Decision Point**: Level of calculation detail and refinement vs. time available

**Trade-off**:
- **Detailed calculations**: More accurate results, better optimization, stronger code compliance documentation, but require more engineering time
- **Simplified calculations**: Faster completion, conservative results, but may result in oversized equipment and higher cost

**Recommendation**: Balance detail with project phase:
- **Preliminary Design (30%)**: Use simplified methods, conservative assumptions, parametric analysis
- **Detailed Design (60%)**: Refine calculations with better input data, reduce conservatism
- **Final Design (IFC)**: Complete all detailed calculations with verified inputs

**Source:** ASSUMPTION: standard design phase approach

#### Software vs. Hand Calculations

**Decision Point**: Use calculation software vs. manual calculation methods

**Trade-off**:
- **Software calculations**: Faster for complex problems, can model more variables, produce professional reports, but require software validation, licensing costs, and user training
- **Hand calculations**: More transparent, easier to check, no software licensing, but time-consuming for complex problems and more prone to arithmetic errors

**Recommendation**:
- **HVAC loads**: Use recognized software (Carrier HAP, Trane TRACE) for heating/cooling load calculations
- **Fire protection hydraulics**: Use NFPA 13 approved software (HydraCAD, AutoSPRINK)
- **Plumbing sizing**: Can use Excel or hand calculations (fixture unit method is straightforward)
- **All software**: Require validation documentation and spot-check of results

**Source:** ASSUMPTION: industry standard practice; Specification.md (Calculation Software Standards)

#### Standardization vs. Optimization

**Decision Point**: Use standardized pipe/duct sizes and equipment selections vs. optimize each element

**Trade-off**:
- **Standardization**: Simplifies calculations, reduces design time, simplifies procurement and spare parts, but may result in suboptimal sizing
- **Optimization**: Reduces material cost, improves energy efficiency, but increases calculation effort and complexity

**Recommendation**:
- **Major equipment** (HVAC units, pumps, tanks): Optimize sizing based on detailed calculations
- **Distribution systems** (pipes, ducts): Use standardized sizes and velocity criteria
- **Small components** (fittings, valves, diffusers): Use standard selections from manufacturer catalogs

**Source:** ASSUMPTION: standard design approach balancing cost and complexity

## Examples

### Reference Examples and Precedents

**Project-Specific References**:

- **Employer's Requirements** — **TBD** (location TBD; shall provide calculation criteria and acceptance requirements)
- **Previous Similar Facilities** — **TBD** — Precedent canola oil or industrial facility MEP calculations (if available)

**Source:** Employer's Requirements to be provided; industry precedents TBD

### HVAC Load Calculation Example (Conceptual)

**Typical MCC Building Cooling Load Components:**

1. **Envelope Gains**: Walls, roof, windows (moderate due to industrial construction, limited windows)
2. **Solar Gains**: Through glazing (minimal if limited windows)
3. **Internal Gains from MCC Equipment**: Significant heat dissipation from electrical switchgear, VFDs, transformers (can be 1-5% of electrical load as heat)
4. **Lighting Gains**: LED lighting (moderate density for industrial space)
5. **Occupant Gains**: Low occupancy (electrical equipment room, occasional maintenance)
6. **Ventilation Gains**: Outdoor air to condition (per ASHRAE 62.1)

**Result**: Cooling load likely dominated by MCC equipment heat dissipation and ventilation loads. Heating load likely moderate (Surrey, BC has mild winters but requires heating for comfort).

**Source:** ASSUMPTION: typical MCC building load characteristics; actual loads TBD by detailed calculation

### Plumbing Sizing Example (Conceptual)

**Typical MCC Building Plumbing:**

- **Fixtures**: Washrooms (water closets, lavatories), break room sink, janitor sink, safety shower (if required), hose bibbs
- **Fixture Units**: Total fixture units per NBC 2020 / CSA B64 (typically 10-30 FU for small industrial building)
- **Pipe Sizing**: Cold water main sized for peak demand with diversity (typically 25-40 mm for small building)
- **Hot Water**: If required, size for peak demand with recovery rate
- **Drainage**: Size per drainage fixture units and slope requirements

**Source:** ASSUMPTION: typical small industrial building plumbing; actual sizing TBD by detailed calculation

### Fire Protection Hydraulic Calculation Example (Conceptual)

**Typical MCC Building Sprinkler System:**

- **Occupancy Classification**: Ordinary Hazard Group 1 or 2 per NFPA 13 (electrical equipment storage/operation)
- **Design Density**: 0.15-0.20 gpm/sf per NFPA 13
- **Design Area**: 1500 sf (typical for OH1/OH2)
- **Sprinkler Spacing**: 10-15 ft spacing (typical for standard coverage)
- **Calculated Demand**: ~250-400 gpm at required pressure
- **Hose Stream**: +250 gpm for 30-60 minutes per NFPA 13
- **Available Supply**: Coordinate with PKG-03 site fire water system

**Source:** ASSUMPTION: typical industrial building fire protection; actual requirements TBD per NFPA 13 and AHJ

### Anticipated Artifacts (from DEL-22.03)

1. **HVAC load calculations** — Heating and cooling loads, equipment sizing
2. **Plumbing sizing** — Water supply and drainage pipe sizing

**Source:** Decomposition REVISED_v2.md, DEL-22.03 anticipated artifacts

## Conflict Table (for human ruling)

No conflicts identified at this stage. Conflicts will be documented here if contradictions are found between sources during calculation development.

**Format**:

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority | Human Ruling |
|-------------|----------|----------|----------|-------------------|-------------------|--------------|
| (none yet) | | | | | | |
