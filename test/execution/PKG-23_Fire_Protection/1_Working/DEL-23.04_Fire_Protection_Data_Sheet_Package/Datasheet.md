# Datasheet: DEL-23.04 Fire Protection Data Sheet Package

## Identification

| Field | Value |
|-------|-------|
| Deliverable ID | DEL-23.04 |
| Name | Fire Protection Data Sheet Package |
| Package | PKG-23 Fire Protection |
| Discipline | Specialty |
| Type | Data Sheet |
| Responsible | D&B Contractor |
| Status | INITIALIZED |
| Project | Canola Oil Transload Facility — Phase 1 |
| Location | Fraser Surrey Terminal, 11060 Elevator Road, Surrey, BC |

## Attributes

| Attribute | Value | Source |
|-----------|-------|--------|
| Data Sheet Package Number | **TBD** | **ASSUMPTION**: Per project data sheet numbering system |
| Data Sheet Format | Standard equipment data sheet format (equipment tag, service description, specifications, operating conditions, performance data, materials, accessories, approvals) | **ASSUMPTION**: Industry-standard data sheet format |
| Number of Data Sheets | **TBD** (estimate 10–20 data sheets depending on equipment list) | **ASSUMPTION**: Based on typical fire protection equipment count |
| Revision | Rev 0 (initial issue) | **ASSUMPTION**: Initial design phase |
| Classification | For Design & Construction | Decomposition: DEL-23.04 |
| Data Sheet Source | Combination of design calculations (DEL-23.03), equipment manufacturer data, and engineering specifications (DEL-23.02) | **ASSUMPTION**: Data sheet development sources |
| Data Sheet Retention | Per project record retention requirements — **TBD** (typically 25+ years for equipment records) | **ASSUMPTION**: Permanent equipment record |

## Conditions

**Project Context:**

This data sheet package defines and substantiates fire protection equipment in accordance with Employer's Requirements (ER) for a canola oil transload facility with the following conditions:

| Condition | Value | Source |
|-----------|-------|--------|
| Facility Type | CSD Canola Oil Transload | Decomposition Section 1.1 |
| Permitted Throughput | 1,000,000 MT per annum | Decomposition Section 1.1 |
| Storage Capacity | 45,000 MT (3 × 15,000 MT tanks) | Decomposition Section 1.1 |
| Railcar Capacity | 32 unloading stations on 2 tracks | Decomposition Section 1.1 |
| Product Classification | Combustible liquid (Class IIIA per NFPA 30) | **ASSUMPTION**: CSD canola oil flash point typically >93°C (200°F) |
| Operating Temperature Range | -40°C to +40°C ambient | **ASSUMPTION**: Fraser Valley climate, BC |
| Environmental Classification | Outdoor industrial (marine/coastal corrosive atmosphere) | Site location and **ASSUMPTION** |
| Hazardous Area Classification | Class I, Division 2 (anticipated in loading areas) | **ASSUMPTION**: To be confirmed per facility hazardous area classification study (DEL-30.03) |
| Seismic Requirements | 2020 NBCC seismic provisions for BC | **ASSUMPTION**: BC seismic design requirement |
| Design Life | 25 years minimum | **ASSUMPTION**: Typical industrial equipment design life |

**Data Sheet Package Scope:**

| Data Sheet | Equipment/System | Purpose | Source |
|------------|------------------|---------|--------|
| Fire Hydrant Data Sheets | Fire hydrants (multiple units per facility) | Specify fire hydrant type, model, outlets, accessories, installation requirements | Decomposition: fire hydrant data sheets (anticipated artifact) |
| Fire Alarm Panel Data Sheet | Fire alarm control panel | Specify fire alarm control panel type, capacity, features, I/O, power requirements | Decomposition: fire alarm panel data sheet (anticipated artifact) |

**Additional Data Sheets (typical for comprehensive fire protection system):**

| Data Sheet | Equipment/System | Purpose | Source |
|------------|------------------|---------|--------|
| Fire Pump Data Sheet (if applicable) | Fire pump unit | Specify fire pump type, capacity, head, driver, controller, accessories | **ASSUMPTION**: If fire pump in Contractor scope |
| Foam Proportioning System Data Sheets | Foam proportioning equipment | Specify foam proportioning system type, capacity, accessories | **ASSUMPTION**: Required for combustible liquid tank protection |
| Foam Concentrate Storage Tank Data Sheet | Foam concentrate storage tank | Specify tank capacity, materials, heating/insulation, accessories | **ASSUMPTION**: Foam concentrate storage specification |
| Foam Discharge Device Data Sheets | Tank foam chambers, foam makers, foam monitors | Specify foam discharge devices for tanks and marine loading | **ASSUMPTION**: Tank and marine foam systems |
| Fire Detection Device Data Sheets | Heat detectors, flame detectors | Specify detection device types, models, ratings, approvals | **ASSUMPTION**: Fire detection system equipment |
| Fire Alarm Notification Device Data Sheets | Horns, strobes, horn/strobe combinations | Specify notification device types, models, candela/decibel ratings, approvals | **ASSUMPTION**: Fire alarm notification equipment |
| Fire Water Valve Data Sheets (key valves) | Isolation valves, control valves | Specify valve types, sizes, ratings, operators, accessories | **ASSUMPTION**: Major fire water system valves |
| Fire Protection Pipe Marker/Valve Tag Data | Identification tags and markers | Specify pipe marker and valve tag requirements | **ASSUMPTION**: Fire protection identification |

## Construction

**Data Sheet Content and Format:**

Each equipment data sheet typically includes the following sections (content varies by equipment type):

| Section | Content | Source |
|---------|---------|--------|
| **Equipment Identification** | Equipment tag number, equipment name, service description, quantity | From DEL-23.01 drawings and equipment list |
| **General Specifications** | Equipment type/classification, manufacturer (or "to be determined" if competitive procurement), model number, applicable standards (NFPA, ULC, AWWA, etc.), listings/approvals (UL, ULC, FM) | From DEL-23.02 technical specification and code requirements |
| **Performance Requirements** | Flow rate, pressure, capacity, head, power, or other performance parameters as applicable | From DEL-23.03 design calculations |
| **Operating Conditions** | Design temperature range, ambient conditions, product/service fluid properties (if applicable), operating pressure/temperature, hazardous area classification | From project design basis and site conditions |
| **Physical Characteristics** | Dimensions, weight, materials of construction, coatings/finishes, corrosion protection | From DEL-23.02 specification and manufacturer data |
| **Accessories and Appurtenances** | Required accessories (valves, gauges, controls, heaters, insulation, etc.) | From DEL-23.02 specification and design requirements |
| **Electrical Requirements** | Electrical power supply (voltage, phase, frequency), power consumption, motor data (HP/kW, efficiency), control voltage, hazardous area classification of electrical components | Coordination with PKG-17 Electrical |
| **Control and Instrumentation** | Control system interfaces, I/O requirements, monitoring points, alarm/shutdown functions | Coordination with PKG-19 Control Systems |
| **Installation Requirements** | Mounting, supports, seismic bracing, clearances, access requirements | From DEL-23.02 specification and installation standards |
| **Testing and Commissioning** | Factory testing requirements, site testing requirements, performance verification | From DEL-23.02 specification and DEL-23.05 test requirements |
| **References** | Applicable drawings, specifications, calculations, codes/standards | Cross-references to DEL-23.01, DEL-23.02, DEL-23.03 |
| **Notes** | Special requirements, exceptions, clarifications, assumptions | As needed |
| **Revisions** | Revision history | Document control |

**Example Data Sheet Structure:**

**Fire Hydrant Data Sheet:**

| Data Sheet Section | Typical Content | Source |
|--------------------|----------------|--------|
| Equipment Tag | FH-001, FH-002, ... FH-0XX (multiple hydrants) | Equipment tagging system — **TBD** |
| Equipment Name | Fire Hydrant | Standard nomenclature |
| Service | Fire water supply for facility fire protection | System function |
| Quantity | **TBD** (typically 10–20 hydrants for facility) | From DEL-23.01 hydrant location drawing |
| Type | Dry-barrel fire hydrant | Freeze protection requirement for BC climate |
| Standard | AWWA C502 | Fire hydrant standard |
| Outlets | 2 × 2½" hose outlets, 1 × 4½" pumper outlet (or per local fire department) | **ASSUMPTION**: Standard North American configuration |
| Operating Nut | Pentagon or per local fire department | **ASSUMPTION**: Compatibility with fire department |
| Valve Type | Compression-type main valve, bronze seat | Standard dry-barrel construction |
| Drain Valve | Automatic drain valve | Freeze protection |
| Barrel Material | Ductile iron or cast iron | Standard hydrant materials |
| Coating | Baked enamel or powder coat finish | Corrosion protection |
| Installation | Concrete pad, adjustable extension, valve box for shutoff valve | Installation requirements |
| Operating Pressure | **TBD** psi | From DEL-23.03 hydraulic calculation |
| Flow Rate | **TBD** gpm per hydrant | From DEL-23.03 fire water demand calculation |
| Approval | UL or FM approved (if applicable) | Fire equipment approval |

**Fire Alarm Panel Data Sheet:**

| Data Sheet Section | Typical Content | Source |
|--------------------|----------------|--------|
| Equipment Tag | FACP-001 | Equipment tagging system — **TBD** |
| Equipment Name | Fire Alarm Control Panel | Standard nomenclature |
| Service | Facility fire detection and alarm system | System function |
| Quantity | 1 (or multiple panels if large facility) | From DEL-23.01 fire alarm drawings |
| Type | Addressable fire alarm control panel | Modern industrial system |
| Standard | ULC-S527 (Canadian fire alarm control panel standard) | Canadian standard |
| Capacity | **TBD** addressable points (devices) | Based on device count from DEL-23.01 |
| Detection Device Types | Heat detectors (ULC-S530), flame detectors (ULC-S536), smoke detectors (ULC-S531), manual pull stations (ULC-S528) | From DEL-23.01 and DEL-23.02 |
| Notification Device Types | Horns/strobes (ULC-S525) | From DEL-23.01 and DEL-23.02 |
| Power Supply | 120VAC, 60Hz (or per project electrical system) | Coordination with PKG-17 Electrical |
| Backup Power | Battery backup per NFPA 72 (24-hour standby + 5-minute alarm capacity) | From DEL-23.03 battery calculation |
| Communication | Network-capable for SCADA/DCS integration (Modbus, BACnet, or protocol TBD) | Coordination with PKG-19 Control Systems |
| Enclosure | NEMA 4 (weatherproof) or NEMA 1 (indoor) per location | Environmental protection |
| Listing | ULC-listed | Canadian fire alarm equipment requirement |
| Seismic | Seismic-rated anchorage per NBCC 2020 | BC seismic requirement |

**Fire Pump Data Sheet (if applicable):**

| Data Sheet Section | Typical Content | Source |
|--------------------|----------------|--------|
| Equipment Tag | FP-001 | Equipment tagging system — **TBD** |
| Equipment Name | Fire Pump Unit | Standard nomenclature |
| Service | Fire water supply pressurization | System function |
| Quantity | 1 (or 2 if redundant) | From DEL-23.01 and reliability requirements |
| Type | Horizontal split-case centrifugal pump per NFPA 20 | Fire pump standard |
| Capacity | **TBD** gpm at **TBD** psi (150% of demand per NFPA 20) | From DEL-23.03 fire pump sizing calculation |
| Driver | Electric motor or diesel engine — **TBD** | To be determined based on power reliability and requirements |
| Motor Power | **TBD** HP or kW | From DEL-23.03 calculation |
| Motor Voltage | **TBD** (e.g., 480V, 3-phase, 60Hz) | Coordination with PKG-17 Electrical |
| Controller | Listed fire pump controller per NFPA 20 and ULC-S536 | Fire pump control standard |
| Accessories | Circulation relief valve, pressure relief valve, test header, pressure gauges, flow meter | Per NFPA 20 |
| Listing | UL-listed or FM-approved | Fire pump approval |
| Installation | Fire pump room (if required) or outdoor installation with weather protection | From DEL-23.02 specification |

## References

**Decomposition and Context:**
- Decomposition document: `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md`, Section 5 (PKG-23), DEL-23.04
- Deliverable context: `_CONTEXT.md`

**Applicable Codes and Standards:**
- NFPA 20: Installation of Stationary Pumps for Fire Protection — fire pump standards
- NFPA 72: National Fire Alarm and Signaling Code — fire alarm equipment standards
- AWWA C502: Dry-Barrel Fire Hydrants — fire hydrant standard
- ULC-S527: Control Units for Fire Alarm Systems — Canadian FACP standard
- ULC-S530, S536, S531, S528, S525: Canadian fire alarm device standards

**Cross-References:**
- DEL-23.01: Fire Protection Design Drawing Set — provides equipment locations, quantities, tagging
- DEL-23.02: Fire Protection Technical Specification — provides equipment specifications and material requirements
- DEL-23.03: Fire Protection Design Calculations — provides equipment sizing and performance requirements
- DEL-23.05: Fire Protection Installation & Test Records — testing per data sheet specifications
- PKG-17: Electrical — electrical power supply data
- PKG-19: Control Systems — control system interface data
