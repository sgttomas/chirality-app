# Guidance: DEL-22.04 Building MEP Data Sheet Package

## Purpose

This guidance document supports the development of **Building MEP Data Sheet Package** for **PKG-22 Building Interior & MEP**.

**Deliverable Purpose:** Defines and substantiates building MEP equipment in accordance with Employer's Requirements.

**Source:** Decomposition REVISED_v2.md, DEL-22.04 entry; _CONTEXT.md

### Role in Project Delivery

Equipment data sheets serve as the detailed technical specification for individual equipment items. They provide:

- **Procurement specification** for equipment purchases and vendor quotations
- **Performance baseline** for equipment acceptance testing and commissioning
- **Technical reference** for operations and maintenance
- **Interface definition** for electrical power, controls, and utility connections
- **Configuration management** for tracking as-built equipment and future replacements

**Deliverable Classification:**
- **Type:** Data Sheet
- **Discipline:** Buildings
- **Responsible Party:** D&B Contractor

**Source:** Standard EPC deliverable purposes; _CONTEXT.md

## Principles

### Purpose and Content of Equipment Data Sheets

**Data Sheet Philosophy:**

Equipment data sheets translate system-level design (from DEL-22.01 drawings and DEL-22.03 calculations) into equipment-specific technical requirements. They serve as the bridge between design intent and physical equipment procurement.

**Key Functions:**
1. **Specify Performance**: Define required capacity, efficiency, operating range
2. **Define Interfaces**: Document electrical, control, utility, and mounting requirements
3. **Establish Quality**: Specify materials, certifications, and manufacturer requirements
4. **Enable Procurement**: Provide clear basis for vendor quotes and purchase orders
5. **Support Commissioning**: Establish acceptance criteria for testing per DEL-22.05

**Source:** ASSUMPTION: standard equipment data sheet purpose

### HVAC Equipment Data Sheet Content

**Critical Parameters for HVAC Equipment:**

- **Capacity**: Heating capacity (kW or MBH), cooling capacity (tons or kW), airflow (CFM or L/s)
- **Efficiency**: EER, SEER, COP, AFUE per ASHRAE 90.1 minimum requirements
- **Operating Conditions**: Indoor/outdoor temperature range, altitude derating (if applicable)
- **Electrical**: Voltage, phase, FLA, MCA, MOCP, disconnect requirements
- **Controls**: BAS integration, control points, communication protocol (Modbus, BACnet, etc.)
- **Physical**: Dimensions, weight, rigging requirements, mounting details
- **Noise**: Sound power level or sound pressure level at specified distance
- **Connections**: Ductwork connections, condensate drain, refrigerant piping (if split system)

**Source:** ASHRAE 90.1; standard HVAC equipment specification practice

### Plumbing Equipment Data Sheet Content

**Critical Parameters for Plumbing Equipment:**

- **Capacity**: Tank volume (liters or gallons), recovery rate (for water heaters), pump flow (GPM or L/s)
- **Pressure**: Operating pressure range, maximum working pressure, pump head (for pumps)
- **Temperature**: Operating temperature range, setpoint (for water heaters)
- **Materials**: Tank material (for corrosion resistance), piping connections material
- **Certifications**: NSF/ANSI approval for potable water contact, CSA B64 compliance
- **Electrical**: Voltage, kW rating (for electric heaters), pump motor HP and electrical
- **Controls**: Temperature controls, pressure switches, monitoring interfaces
- **Physical**: Dimensions, weight, installation clearances
- **Connections**: Inlet/outlet size and type, pressure relief valve, expansion tank (if required)

**Source:** NBC 2020, CSA B64; standard plumbing equipment specification practice

### Fire Protection Equipment Data Sheet Content

**Critical Parameters for Fire Protection Equipment:**

- **Sprinkler Heads**: Type (upright, pendent, sidewall), temperature rating, K-factor, coverage area, finish
- **Sprinkler System Components**: Alarm valve type, flow switch rating, tamper switch, pressure gauges
- **Fire Pumps** (if required): Flow (GPM), head (PSI), driver type (electric motor, diesel engine), controller type
- **Approvals**: UL/FM listing (mandatory for fire protection equipment)
- **Operating Conditions**: Water pressure range, ambient temperature range
- **Electrical** (for fire pumps): Voltage, FLA, dedicated power source requirements, emergency power
- **Performance**: Flow vs. pressure curve (for fire pumps), hydraulic calculation reference

**Source:** NFPA 13; standard fire protection equipment specification practice

### Material Selection for Plumbing

**Potable Water Systems:**

- Materials in contact with potable water must be NSF/ANSI certified
- Copper, stainless steel, or approved plastic (PEX, CPVC) for piping
- Lead-free fittings and valves per Safe Drinking Water Act requirements

**Corrosion Considerations:**

- Surrey, BC location has moderate corrosion environment (coastal proximity)
- Consider corrosion-resistant materials for outdoor installations or marine environments
- Protective coatings or cathodic protection for buried or exposed piping

**Source:** NSF/ANSI standards; NBC 2020; corrosion engineering practice

### Fire Protection Equipment Approvals

**Mandatory Approvals:**

- **UL Listed**: Sprinkler heads, alarm valves, flow switches must be UL listed
- **FM Approved**: Fire pumps and major components should be FM approved
- **CSA Certified**: Equipment used in Canada should have CSA certification

**Why Approvals Matter:**

- Required by NFPA 13 and building codes
- Required by insurance underwriters and fire marshal (AHJ)
- Ensures equipment meets performance and safety standards
- Failure to use listed/approved equipment will result in code compliance issues

**Source:** NFPA 13 requirements; fire protection engineering practice

### Energy Efficiency Requirements

**ASHRAE 90.1 Minimum Efficiency:**

- **HVAC Equipment**: Packaged AC units, heat pumps, furnaces must meet minimum EER, SEER, COP, AFUE per ASHRAE 90.1 equipment tables (varies by size and type)
- **Motors**: Pump and fan motors must meet minimum efficiency per ASHRAE 90.1
- **Lighting**: Fixture efficacy must meet ASHRAE 90.1 requirements (if lighting data sheets included)

**Beyond Code Minimum:**

- **TBD** — Project may have sustainability goals requiring efficiency beyond code minimum (location TBD)
- Higher efficiency reduces operating cost but increases capital cost (lifecycle cost analysis may be required)

**Source:** ASHRAE 90.1 (location TBD); DEL-22.01 Specification PR-03

## Considerations

### Factors to Consider During Development

#### Data Sheets and Drawings Coordination

Data sheets must support DEL-22.01 drawings:

- Equipment tags on data sheets must match tags on drawings
- Equipment locations referenced on data sheets must match drawing locations
- Equipment capacities and sizes on schedules must match data sheet information
- Any discrepancies between data sheets and drawings must be resolved

**Source:** Specification.md IF-01

#### Data Sheets and Specifications Coordination

Data sheets must comply with DEL-22.02 specifications:

- Specified manufacturers and models must be reflected in data sheets
- Performance requirements in specifications must be met by data sheet selections
- Materials and certifications in specifications must be documented in data sheets

**Source:** Specification.md IF-02

#### Calculations and Equipment Selection

Data sheets must reflect DEL-22.03 calculations:

- Equipment capacities must meet or exceed calculated requirements
- Operating conditions must be within calculated ranges
- Design margins (typically 10-15%) from calculations should be reflected in equipment selections

**Source:** Specification.md IF-03; DEL-22.03 calculations

#### Control System Interfaces

**Critical Coordination with PKG-19:**

- Define all control and monitoring points for each equipment (start/stop, status, alarms, analog values)
- Specify communication protocol (hardwired, Modbus RTU, BACnet IP, etc.)
- Define control sequence and interlocks
- Coordinate control power requirements (24VAC, 120VAC, etc.)

**Why This Matters:**

- Inadequate control interface definition leads to field changes and commissioning delays
- Control system contractor (PKG-19) needs this information for control panel design and programming

**Source:** Interface with PKG-19; Specification.md IF-04

#### Electrical Coordination

**Critical Coordination with PKG-17:**

- Define electrical power requirements accurately (voltage, phase, FLA, MCA, MOCP)
- Coordinate equipment locations with electrical power distribution routing
- Define disconnect and starter requirements
- Identify emergency power requirements (fire pumps require emergency power)

**Why This Matters:**

- Electrical engineer (PKG-17) uses this information to size feeders, breakers, and design electrical distribution
- Inaccurate electrical data leads to undersized or oversized electrical infrastructure

**Source:** Interface with PKG-17; Specification.md IF-05

### Vendor Data Validation

**Verifying Vendor-Supplied Data:**

- Confirm data is from current manufacturer literature (not outdated catalogs)
- Verify performance curves show equipment meets required performance at specified conditions
- Check that all required parameters are provided (not marked "TBD" or "to be determined")
- Validate that certifications and approvals are documented (UL, FM, CSA, NSF/ANSI, etc.)
- Compare vendor data to multiple manufacturers to ensure selections are competitive

**Common Vendor Data Issues:**

- Performance data at conditions different from project requirements (requires interpolation or derating)
- Missing electrical data or incomplete control interface information
- Approvals or certifications not documented or expired
- Equipment dimensions do not fit space shown on drawings

**Source:** ASSUMPTION: standard vendor data validation practice; Specification.md PR-01

### Equipment Selection Margins

**Design Margins** (from DEL-22.03 calculations):

- Typical 10-15% margin for equipment sizing beyond peak calculated load
- Margins account for: calculation uncertainties, future load growth, part load operation, degradation over time

**Avoiding Over-Sizing:**

- Excessive margins increase capital cost and may reduce efficiency at typical operating conditions
- Pumps and fans oversized significantly may require VFDs for turndown capability
- Cooling equipment oversized may have poor humidity control at part load

**Right-Sizing Approach:**

- Use calculated peak load from DEL-22.03 plus standard margin (10-15%)
- Consider part-load performance and efficiency
- Document equipment selection margin in data sheet notes

**Source:** Guidance from DEL-22.03; industry standard practice; Specification.md PR-03

### Data Sheet Format Standards

**Standardization Benefits:**

- Consistent format improves readability and reduces errors
- Standardized equipment tagging simplifies coordination across deliverables
- Common terminology and units prevent confusion

**Typical Format Elements:**

- Project header with project name, location, date
- Equipment identification section (tag, service, location)
- Required performance section (capacity, efficiency, conditions)
- Materials and construction section
- Vendor information section (manufacturer, model, data sheet reference)
- Utilities and connections section (electrical, piping, controls)
- Notes and special requirements section

**Source:** ASSUMPTION: standard data sheet format; Specification.md QR-02

### Quality Assurance for Equipment Data

**Review Process:**

1. **Self-Check**: Originator verifies data completeness and accuracy
2. **Technical Review**: Engineer verifies equipment meets design requirements and calculations
3. **Vendor Review**: Vendor data validated against manufacturer literature
4. **Interface Coordination**: Electrical, control, and utility interfaces verified with other packages
5. **Discipline Lead Approval**: Final approval before issue for procurement or construction

**Why Multiple Reviews Matter:**

- Equipment procurement errors are costly to correct (long lead times, change orders)
- Incorrect equipment may not fit space, may not meet performance, or may not integrate with controls
- Multiple eyes catch errors and improve quality

**Source:** ASSUMPTION: standard equipment data sheet quality process; Specification.md QR-01

## Trade-offs

### Competing Concerns to Evaluate

#### Energy Efficiency vs. Equipment Cost

**Decision Point**: Specify high-efficiency equipment vs. code-minimum efficiency

**Trade-off**:
- **High-efficiency equipment**: Lower operating cost (energy savings), but higher capital cost, longer payback period
- **Code-minimum equipment**: Lower capital cost, but higher operating cost, may not align with sustainability goals

**Recommendation**:
- Perform lifecycle cost analysis for major equipment (HVAC units, pumps)
- Consider utility rates, operating hours, and project economic criteria
- **TBD** — Lifecycle cost criteria and discount rate (location TBD)

**Source:** ASHRAE 90.1; Specification.md PR-02; DEL-22.01 Guidance Trade-offs

#### Standardization vs. Optimization

**Decision Point**: Standardize equipment selections vs. optimize each selection

**Trade-off**:
- **Standardization**: Simplifies procurement, reduces spare parts inventory, simplifies training, but may result in over/under-sized equipment for some applications
- **Optimization**: Reduces cost and improves efficiency for each application, but increases procurement complexity and spare parts inventory

**Recommendation**:
- Standardize where practical (lighting fixtures, plumbing fixtures, small fans)
- Optimize major equipment (HVAC units, large pumps, fire pumps)
- Balance standardization with project size and complexity

**Source:** ASSUMPTION: standard design approach

#### Single Source vs. Multiple Approved Manufacturers

**Decision Point**: Specify single manufacturer vs. allow multiple approved manufacturers

**Trade-off**:
- **Single source**: Ensures compatibility and uniformity, simplifies procurement, but reduces competition and may increase cost
- **Multiple manufacturers**: Increases competition and may reduce cost, provides alternatives if lead times are long, but requires more engineering effort to establish equivalency criteria

**Recommendation**:
- **Critical or proprietary equipment**: May require single source (e.g., fire pump with specific controller)
- **Standard equipment**: Allow multiple approved manufacturers with performance-based equivalency criteria
- **TBD** — Project procurement strategy (location TBD)

**Source:** ASSUMPTION: standard procurement approach; DEL-22.02 equipment specification approach

#### Vendor Selection Timing

**Decision Point**: Select specific vendors during design vs. performance-based specification

**Trade-off**:
- **Early vendor selection**: Allows coordination with vendor for detailed design, ensures equipment fits and performs, but commits to vendor before competitive bidding
- **Performance-based spec**: Maintains competition until procurement, may reduce cost, but increases risk that selected equipment may not fit or perform as expected

**Recommendation**:
- **Design phase**: Use performance-based requirements allowing multiple manufacturers
- **Procurement phase**: Vendor selection through competitive bidding
- **Special cases**: Early vendor involvement for long-lead or complex equipment (coordinate with procurement)

**Source:** ASSUMPTION: standard EPC design and procurement approach

## Examples

### Reference Examples and Precedents

**Project-Specific References**:

- **Employer's Requirements** — **TBD** (location TBD; shall provide equipment requirements and preferences)
- **Previous Similar Facilities** — **TBD** — Precedent MEP equipment selections from similar industrial facilities (if available)

**Source:** Employer's Requirements to be provided; industry precedents TBD

### Sample HVAC Equipment Data Sheet (Conceptual)

**Equipment Tag**: HV-001
**Service**: MCC Building Rooftop HVAC Unit
**Location**: Building Roof, Grid A-5

**Required Performance**:
- Cooling Capacity: 10 tons (35 kW) at 35°C outdoor, 24°C indoor
- Heating Capacity: 100 MBH (29 kW) at -10°C outdoor
- Supply Airflow: 4000 CFM (1900 L/s)
- Outdoor Air: 1000 CFM (470 L/s) minimum per ASHRAE 62.1
- Cooling EER: 11.0 minimum (ASHRAE 90.1)
- Heating AFUE: 80% minimum

**Electrical**: 460V / 3Ph / 60Hz, FLA 20A, MCA 25A, MOCP 30A

**Controls**: BACnet IP interface to BAS, provide start/stop, temperature control, status, alarms

**Source:** ASSUMPTION: typical small commercial HVAC unit for MCC building

### Sample Fire Protection Data Sheet (Conceptual)

**Equipment Tag**: FP-SPK-001
**Service**: Standard Coverage Upright Sprinkler
**Location**: MCC Building, typical throughout

**Required Performance**:
- Type: Standard Coverage Upright
- Temperature Rating: 165°F (74°C) Ordinary
- K-Factor: K=5.6 (standard orifice)
- Coverage Area: 130 sf maximum per NFPA 13
- Finish: Chrome plated

**Approvals**: UL Listed for Light/Ordinary Hazard

**Source:** ASSUMPTION: typical sprinkler head specification per NFPA 13

### Anticipated Artifacts (from DEL-22.04)

1. **HVAC equipment datasheets** — Units, fans, accessories
2. **Plumbing equipment datasheets** — Water heaters, pumps, fixtures
3. **Fire suppression system datasheets** — Sprinkler components

**Source:** Decomposition REVISED_v2.md, DEL-22.04 anticipated artifacts

## Conflict Table (for human ruling)

No conflicts identified at this stage. Conflicts will be documented here if contradictions are found between sources during data sheet development.

**Format**:

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority | Human Ruling |
|-------------|----------|----------|----------|-------------------|-------------------|--------------|
| (none yet) | | | | | | |
