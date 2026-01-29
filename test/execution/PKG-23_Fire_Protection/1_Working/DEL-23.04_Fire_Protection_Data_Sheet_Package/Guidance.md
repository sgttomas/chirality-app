# Guidance: DEL-23.04 Fire Protection Data Sheet Package

## Purpose

This guidance document supports the development of **Fire Protection Data Sheet Package** for **PKG-23 Fire Protection** within the Canola Oil Transload Facility — Phase 1 Design & Build project.

**Deliverable Purpose:**

Defines and substantiates fire protection equipment in accordance with Employer's Requirements (ER), providing equipment data sheets that:
- Document equipment specifications and performance requirements
- Facilitate equipment procurement and vendor selection
- Support interdisciplinary coordination (electrical, I&C, structural)
- Provide equipment information for installation and commissioning
- Create permanent equipment records for operations and maintenance
- Source: Decomposition DEL-23.04 description and **ASSUMPTION** regarding data sheet purpose

**Project Context:**
- **Project:** Canola Oil Transload Facility — Phase 1, Fraser Surrey Terminal, Surrey, BC
- **Deliverable Classification:** Data Sheet deliverable under Specialty discipline
- **Responsible Party:** D&B Contractor
- **Source:** Decomposition Section 1.1 and DEL-23.04 context

**Objective Alignment:**

This deliverable supports **OBJ-1: Safe & Reliable Operation** — data sheets ensure fire protection equipment is properly specified and meets performance requirements.
- Source: Decomposition Section 2 (Project Objectives) and Section 6 (Objective-to-Deliverable Mapping)

## Principles

**Equipment Data Sheet Principles:**

**P-1: Data Sheets as Equipment Specifications**
- Equipment data sheets are detailed specifications for individual pieces of equipment or equipment types
- Data sheets bridge the gap between design drawings/specifications and procurement/installation
- Data sheets provide equipment-specific information not practical to include on drawings or in general specifications
- Source: **ASSUMPTION**: Data sheet function in design-build
- Application: Data sheets supplement drawings and specifications with detailed equipment information

**P-2: Design Basis Traceability**
- Data sheet specifications and performance requirements must be traceable to design calculations and technical specifications
- Equipment sizing based on design calculations (DEL-23.03)
- Equipment specifications based on technical specification (DEL-23.02) and codes/standards
- Source: **ASSUMPTION**: Data sheet development basis
- Application: Cross-reference data sheets to calculations and specifications

**P-3: Interdisciplinary Coordination**
- Equipment data sheets are key interdisciplinary coordination documents
- Electrical team needs electrical load data from data sheets
- I&C team needs control system interface data from data sheets
- Structural team needs equipment load data from data sheets
- Source: **ASSUMPTION**: Data sheet coordination role
- Application: Data sheets include interface data for other disciplines

**P-4: Procurement Support**
- Data sheets facilitate equipment procurement by providing clear specifications for vendors
- Data sheets should allow for competitive procurement (performance specs or "or approved equal") where appropriate
- Data sheets define acceptance criteria for vendor submittals
- Source: **ASSUMPTION**: Data sheet procurement function
- Application: Write data sheets to enable vendor quotations and submittals

**P-5: Operations and Maintenance Record**
- Data sheets become permanent equipment records for facility operations and maintenance
- Data sheets provide equipment information needed for spare parts, maintenance, and future modifications
- Source: **ASSUMPTION**: Data sheet O&M function
- Application: Include information useful for long-term equipment management

**P-6: Consistency Across Documents**
- Equipment tags, specifications, and performance requirements must be consistent across data sheets, drawings, specifications, and calculations
- Inconsistencies cause confusion and errors during procurement and construction
- Source: **ASSUMPTION**: Document set consistency principle
- Application: Cross-check data sheets with other design documents

## Considerations

**Data Sheet Development Considerations:**

**C-1: Equipment List Development**
- Develop comprehensive equipment list from fire protection drawings (DEL-23.01)
- Determine which equipment requires data sheets (typically major equipment: pumps, panels, tanks; not minor components: valves, fittings unless critical)
- Equipment list should be coordinated with equipment tagging system
- Source: **ASSUMPTION**: Equipment list development
- Impact: Data sheet scope definition

**C-2: Equipment Tagging System**
- Consistent equipment tagging system critical for data sheet organization and cross-referencing
- Equipment tags on data sheets must match tags on drawings
- Tagging system typically hierarchical (e.g., FH-001 for Fire Hydrant #1, FACP-001 for Fire Alarm Control Panel #1)
- Source: **ASSUMPTION**: Equipment tagging practice
- Impact: Equipment identification and cross-referencing

**C-3: Data Sheet Template Selection**
- Use standard data sheet templates for consistency and efficiency
- Templates vary by equipment type (pump data sheet, panel data sheet, valve data sheet, etc.)
- Project may have standard data sheet templates; otherwise use industry-standard formats
- Source: **ASSUMPTION**: Data sheet template use
- Impact: Data sheet format and efficiency

**C-4: Equipment Specifications: Performance vs. Prescriptive**
- Balance between performance specifications (specify what equipment must do) and prescriptive specifications (specify exact equipment)
- Performance specifications allow competitive procurement but require more vendor evaluation
- Prescriptive specifications (manufacturer/model specified) provide certainty but may limit competition
- Design-build projects typically use hybrid approach
- Source: **ASSUMPTION**: Specification approach for data sheets
- Impact: Data sheet content and procurement approach

**C-5: Electrical Interface Data**
- Fire protection equipment requires electrical power (fire pump, fire alarm panel, detection devices, notification devices)
- Data sheets must provide electrical load data for electrical design team: voltage, phase, frequency, power consumption (kW or HP), motor data, control voltage
- Coordinate early with electrical team on data format and requirements
- Source: **ASSUMPTION**: Electrical coordination requirement
- Impact: Electrical load data on data sheets; coordination with PKG-17

**C-6: Control System Interface Data**
- Fire alarm system typically integrates with facility SCADA/DCS
- Fire pump may have status/alarm monitoring
- Data sheets must provide control system interface data: I/O requirements (digital/analog inputs/outputs), communication protocols (Modbus, BACnet, etc.), monitoring/alarm points
- Coordinate early with I&C team on interface requirements
- Source: **ASSUMPTION**: Control system coordination requirement
- Impact: I&C interface data on data sheets; coordination with PKG-19

**C-7: Equipment Load Data for Structural Design**
- Equipment requires structural supports, foundations, or anchorage
- Data sheets must provide equipment load data for structural team: weight (operating and empty), seismic loads, footprint, anchor bolt pattern
- Coordinate with structural team on data requirements
- Source: **ASSUMPTION**: Structural coordination requirement
- Impact: Equipment load data on data sheets; coordination with PKG-06

**C-8: Equipment Availability and Lead Times**
- Specified equipment must be commercially available within project schedule
- Long-lead equipment (fire pump, foam equipment, fire alarm panel) may require early procurement
- Consider equipment lead times when specifying equipment and developing procurement schedule
- Source: **ASSUMPTION**: Procurement schedule consideration
- Impact: Equipment selection and procurement planning

**C-9: Vendor Data Integration**
- Data sheets initially prepared based on design calculations and specifications (design intent data sheets)
- During procurement, vendor-proposed equipment data integrated into data sheets or vendor submittals reviewed against data sheet requirements
- Final "as-purchased" data sheets reflect actual equipment selected
- Source: **ASSUMPTION**: Data sheet evolution through design and procurement
- Impact: Data sheet revision process

**C-10: Freeze Protection Requirements**
- BC climate requires freeze protection for fire protection equipment
- Fire pump room (if applicable) must be heated
- Foam concentrate storage tank must be heated/insulated
- Fire hydrants must be dry-barrel type
- Data sheets must specify freeze protection requirements
- Source: **ASSUMPTION**: BC climate consideration
- Impact: Freeze protection specifications on data sheets

**C-11: Corrosion Protection for Marine Environment**
- Marine terminal environment requires enhanced corrosion protection
- Equipment coatings/materials must be suitable for marine/coastal atmosphere
- Data sheets must specify corrosion protection requirements (materials, coatings)
- Source: **ASSUMPTION**: Marine environment consideration
- Impact: Corrosion protection specifications on data sheets

**C-12: Seismic Requirements**
- BC seismic zone requires seismic design for equipment anchorage and supports
- Data sheets must note seismic requirements and provide seismic load data
- Coordinate with structural team on seismic anchorage design
- Source: **ASSUMPTION**: BC seismic requirement
- Impact: Seismic design notes and load data on data sheets

## Trade-offs

**T-1: Level of Detail on Data Sheets**
- **Option A:** Highly detailed data sheets (extensive specifications, all accessories listed) — clearer for vendors, longer to develop, less flexibility
- **Option B:** Performance-focused data sheets (key performance requirements, vendors fill in details) — faster to develop, more vendor responsibility, requires good submittal review
- **Trade-off:** Development effort vs. vendor responsibility vs. procurement risk
- **Recommendation:** Moderate detail level — specify critical requirements and performance, allow vendor to propose details subject to approval
- Source: **ASSUMPTION**: Data sheet detail level trade-off

**T-2: Manufacturer-Specific vs. Performance-Based**
- **Option A:** Specify manufacturer and model (e.g., "XYZ Brand Model 123") — ensures specific equipment, limits competition
- **Option B:** Performance-based with "or approved equal" — promotes competition, requires more evaluation
- **Trade-off:** Competition/cost vs. design certainty
- **Recommendation:** Performance-based with "or approved equal" for most equipment; manufacturer-specific only where compatibility or unique features required
- Source: **ASSUMPTION**: Equipment specification approach trade-off

**T-3: Data Sheet Template Standardization**
- **Option A:** Standardized templates for all equipment types — consistent format, easier to manage
- **Option B:** Custom data sheets for each equipment type — tailored content, more flexibility, inconsistent format
- **Trade-off:** Consistency vs. customization
- **Recommendation:** Standardized templates with flexibility to add custom sections as needed
- Source: **ASSUMPTION**: Template standardization trade-off

**T-4: Data Sheet Organization**
- **Option A:** Single data sheet package document — all data sheets in one file, easier to issue
- **Option B:** Separate data sheets (one file per equipment or equipment type) — modular, easier to revise individual sheets, more files to manage
- **Trade-off:** Document management vs. modularity
- **Recommendation:** Separate data sheets for major equipment; grouped data sheets for minor equipment (e.g., all hydrants in one data sheet document)
- Source: **ASSUMPTION**: Data sheet organization trade-off

## Examples

**E-1: Employer's Requirements**
- Refer to Employer's Requirements Volume 2 Parts 1–3 for project-specific equipment requirements
- Location: `/Users/ryan/ai-env/projects/chirality-app/test/Volume_2_Part_{1,2,3}_Employers_Requirements.pdf`
- **Note:** Per INIT.md instruction, do not attempt to read ER files at this stage; reference them as inputs for future working sessions
- Source: Decomposition Section 3 (Reference Documents)

**E-2: Equipment Manufacturer Data Sheets**
- Equipment manufacturers provide product data sheets with specifications, performance curves, dimensions, weights, accessories
- Manufacturer data sheets used as input to develop project data sheets or as basis for submittal review
- Source: **ASSUMPTION**: Manufacturer data as input

**E-3: Industry-Standard Data Sheet Templates**
- Various industry organizations and companies publish data sheet templates for common equipment types
- Templates provide standard format and content guidance
- Source: **ASSUMPTION**: Industry templates available

**E-4: Anticipated Data Sheet Artifacts**
- Fire hydrant data sheets — specify hydrant type, outlets, accessories
- Fire alarm panel data sheet — specify panel capacity, devices, power, communication
- Source: Decomposition DEL-23.04 anticipated artifacts

**E-5: Related Data Sheet Examples (from other disciplines)**
- Pump data sheets (process pumps, transfer pumps) from other packages provide examples of pump data sheet format
- Electrical equipment data sheets (MCCs, switchgear) from PKG-17 provide examples of electrical equipment data sheets
- Source: **ASSUMPTION**: Interdisciplinary examples

## Conflict Table (for human ruling)

No conflicts identified at this stage of document development.

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority | Human Ruling |
|-------------|----------|----------|----------|-------------------|-------------------|--------------|
| *(none at INITIALIZED state)* | | | | | | |

**Note:** Conflicts that arise during data sheet development (e.g., conflicting specifications from different sources, interface data mismatches between disciplines) will be documented here for human ruling.
