# Procedure: DEL-23.04 Fire Protection Data Sheet Package

## Purpose

This procedure defines the process for **producing** the **Fire Protection Data Sheet Package** within **PKG-23 Fire Protection** for the Canola Oil Transload Facility — Phase 1 Design & Build project.

**Scope of This Procedure:**

This procedure covers the workflow for developing, coordinating, and issuing fire protection equipment data sheets per project quality and document control requirements.

**Deliverable Information:**
- **Deliverable ID:** DEL-23.04
- **Deliverable Type:** Data Sheet
- **Responsible Party:** D&B Contractor
- **Discipline:** Specialty (Fire Protection)
- **Source:** Decomposition DEL-23.04 and `_CONTEXT.md`

## Prerequisites

### Dependencies

**Dependency Tracking Mode:**
- **Mode:** NOT_TRACKED (Source: `_DEPENDENCIES.md`)
- **Coordination:** Dependencies coordinated externally by humans

**Upstream Dependencies (typical inputs for data sheets):**

| Input | Source | Purpose | Status |
|-------|--------|---------|--------|
| Fire protection design drawings | DEL-23.01 | Equipment list, equipment tags, equipment locations, quantities | **TBD** — coordinate with design team |
| Fire protection technical specification | DEL-23.02 | Equipment specifications, material requirements, standards | **TBD** — coordinate with specification writer |
| Fire protection design calculations | DEL-23.03 | Equipment sizing and performance requirements (flow, pressure, capacity, power) | **TBD** — coordinate with calculation engineer |
| Equipment tagging system | Project standards | Consistent equipment tagging across data sheets and drawings | **TBD** — obtain project tagging system |
| Equipment manufacturer data | Vendors | Product data sheets, performance curves, dimensions, weights (for vendor equipment or similar) | **TBD** — obtain from vendors or prior projects |
| Employer's Requirements | Employer | Project-specific equipment requirements | **TBD** |

### Reference Materials

**Required References:**
- Employer's Requirements Volume 2 Parts 1–3 (**TBD**)
- NFPA 20, NFPA 72, NFPA 11, NFPA 16 (**TBD**)
- AWWA C502, ULC-S527, ULC-S530, ULC-S536, ULC-S531, ULC-S528, ULC-S525 (**TBD**)
- Equipment manufacturer product data sheets and catalogs (**TBD**)
- Project data sheet templates (if available) — **TBD**

### Personnel Requirements

| Role | Qualifications | Source |
|------|----------------|--------|
| Fire Protection Engineer | P.Eng., fire protection or mechanical discipline, equipment specification experience | **ASSUMPTION**: Professional engineering requirement |
| Interdisciplinary Coordinators | Electrical, I&C, structural engineers for interface coordination | **ASSUMPTION**: Interdisciplinary coordination |
| Procurement/Construction Input | Procurement and construction team members for equipment availability and constructability review | **ASSUMPTION**: Design-build collaboration |

### Tools and Software

| Tool | Purpose | Source |
|------|---------|--------|
| Data sheet template software (MS Word, Excel, or specialized software) | Data sheet preparation | **ASSUMPTION**: Document preparation tool |
| Equipment selection software or catalogs (if applicable) | Equipment selection and sizing | **ASSUMPTION**: Equipment selection tool |

## Steps

### Step 1: Planning and Setup

**1.1 Review Data Sheet Scope and Requirements**
- Review deliverable scope (`_CONTEXT.md`, Specification.md, Guidance.md)
- Review Employer's Requirements for equipment requirements
- Review DEL-23.01 (drawings), DEL-23.02 (specification), DEL-23.03 (calculations) for data sheet inputs
- **Output:** Understanding of data sheet scope and requirements

**1.2 Develop Equipment List**
- Extract equipment list from fire protection drawings (DEL-23.01)
- Determine which equipment requires data sheets:
  - Major equipment: fire pump, fire alarm panel, foam proportioning systems, foam storage tank (data sheets required)
  - Repetitive equipment: fire hydrants (one or more data sheets)
  - Minor equipment: valves, fittings (data sheets typically not required unless critical)
- Verify equipment tags match equipment tagging system
- **Output:** Equipment list with equipment tags

**1.3 Obtain Data Sheet Templates**
- Obtain project data sheet templates (if available) or develop templates
- Templates needed by equipment type: pump data sheet, panel data sheet, tank data sheet, hydrant data sheet, detection device data sheet, etc.
- **TBD:** Project data sheet templates
- **Output:** Data sheet templates ready for use

**1.4 Assign Data Sheet Numbers**
- Assign data sheet numbers per project numbering system
- Typical numbering: DS-FP-001 (Data Sheet Fire Protection #1) or similar — **TBD**
- **Output:** Data sheet list with assigned numbers

### Step 2: Data Sheet Development (Design Intent Data Sheets)

For each equipment or equipment type, develop data sheet following subsections below:

**2.1 Fire Hydrant Data Sheets**
- **Equipment Identification:**
  - Equipment tags: FH-001, FH-002, ... FH-0XX (**TBD:** quantity from DEL-23.01)
  - Equipment name: Fire Hydrant
  - Service: Fire water supply for facility fire protection
- **General Specifications:**
  - Type: Dry-barrel fire hydrant (freeze protection for BC climate)
  - Standard: AWWA C502
  - Outlets: 2 × 2½" hose outlets, 1 × 4½" pumper outlet (or per local fire department) — coordinate with fire department
  - Operating nut: Pentagon or per fire department
  - Valve: Compression-type main valve, bronze seat
  - Drain valve: Automatic drain valve
  - Materials: Ductile iron or cast iron barrel
  - Coating: Baked enamel or powder coat (corrosion protection for marine environment)
- **Performance Requirements:**
  - Operating pressure: **TBD** psi (from DEL-23.03 hydraulic calculation)
  - Flow rate: **TBD** gpm per hydrant (from DEL-23.03 fire water demand calculation)
- **Installation:**
  - Concrete pad, adjustable extension, valve box for shutoff valve
  - Installation per NFPA 24 and AWWA C502
- **Approval:**
  - UL or FM approved (if applicable)
- **References:**
  - DEL-23.01 (hydrant locations), DEL-23.02 (specification), DEL-23.03 (hydraulic calculation)
- **Output:** Fire hydrant data sheet(s) (draft)

**2.2 Fire Alarm Panel Data Sheet**
- **Equipment Identification:**
  - Equipment tag: FACP-001 (**TBD:** tagging system)
  - Equipment name: Fire Alarm Control Panel
  - Service: Facility fire detection and alarm system
  - Quantity: 1 (or more if large facility)
- **General Specifications:**
  - Type: Addressable fire alarm control panel
  - Standard: ULC-S527 (Canadian standard)
  - Capacity: **TBD** addressable points (based on device count from DEL-23.01)
  - Detection devices: Heat detectors (ULC-S530), flame detectors (ULC-S536), smoke detectors (ULC-S531), manual pull stations (ULC-S528)
  - Notification devices: Horns/strobes (ULC-S525)
  - Listing: ULC-listed
- **Performance Requirements:**
  - Capacity adequate for all detection and notification devices shown on DEL-23.01 plus spare capacity (**TBD:** spare % per project standards)
- **Electrical Requirements:**
  - Power supply: 120VAC, 60Hz (or per project electrical system) — coordinate with PKG-17
  - Backup power: Battery backup per NFPA 72 (24-hour standby + 5-minute alarm capacity from DEL-23.03 calculation)
  - Battery size: **TBD** amp-hours (from DEL-23.03)
- **Control and Instrumentation:**
  - Communication: Network-capable for SCADA/DCS integration — coordinate with PKG-19
  - Protocol: Modbus, BACnet, or **TBD** — coordinate with PKG-19
  - I/O: **TBD** based on integration requirements — coordinate with PKG-19
- **Physical Characteristics:**
  - Enclosure: NEMA 4 (weatherproof) or NEMA 1 (indoor) per location
  - Mounting: Wall-mounted or floor-mounted enclosure
  - Seismic: Seismic-rated anchorage per NBCC 2020
- **References:**
  - DEL-23.01 (fire alarm system drawings), DEL-23.02 (specification), DEL-23.03 (battery calculation)
- **Output:** Fire alarm panel data sheet (draft)

**2.3 Fire Pump Data Sheet (if applicable)**
- **Equipment Identification:**
  - Equipment tag: FP-001
  - Equipment name: Fire Pump Unit
  - Service: Fire water supply pressurization
  - Quantity: 1 (or 2 if redundant)
- **General Specifications:**
  - Type: Horizontal split-case centrifugal pump per NFPA 20
  - Listing: UL-listed or FM-approved
- **Performance Requirements:**
  - Capacity: **TBD** gpm at **TBD** psi (from DEL-23.03 fire pump sizing calculation)
  - Note: Capacity per NFPA 20 (typically 150% of demand at rated pressure)
- **Driver:**
  - Type: Electric motor or diesel engine — **TBD** (to be determined based on power reliability and requirements)
  - Power: **TBD** HP or kW (from DEL-23.03 calculation)
- **Electrical Requirements (if electric motor):**
  - Motor voltage: **TBD** (e.g., 480V, 3-phase, 60Hz) — coordinate with PKG-17
  - Starter: Listed fire pump controller per NFPA 20 and ULC-S536
  - Emergency power: **TBD** — coordinate with PKG-17 on emergency power availability
- **Accessories:**
  - Circulation relief valve, pressure relief valve, test header, pressure gauges, flow meter per NFPA 20
- **Installation:**
  - Fire pump room (if required) or outdoor installation with weather protection
  - Foundation and anchorage per NFPA 20 and seismic requirements
- **References:**
  - DEL-23.01 (fire pump location), DEL-23.02 (specification), DEL-23.03 (pump sizing calculation)
- **Output:** Fire pump data sheet (draft) — if fire pump in Contractor scope

**2.4 Foam Proportioning System Data Sheets**
- Equipment tags, specifications, capacities (from DEL-23.03 foam system calculations)
- **Output:** Foam system data sheets (draft)

**2.5 Foam Concentrate Storage Tank Data Sheet**
- Equipment tag, capacity (from DEL-23.03), materials, heating/insulation for freeze protection
- **Output:** Foam storage tank data sheet (draft)

**2.6 Foam Discharge Device Data Sheets**
- Equipment tags, types (foam chambers, foam makers, monitors), capacities
- **Output:** Foam discharge device data sheets (draft)

**2.7 Fire Detection Device Data Sheets (if individual data sheets required)**
- Heat detectors, flame detectors: types, standards (ULC), ratings, coverage
- **Output:** Detection device data sheets (draft) — or may be covered in fire alarm panel data sheet

**2.8 Fire Alarm Notification Device Data Sheets (if individual data sheets required)**
- Horns, strobes: types, standards (ULC-S525), candela/decibel ratings
- **Output:** Notification device data sheets (draft) — or may be covered in fire alarm panel data sheet

### Step 3: Interdisciplinary Coordination

**3.1 Electrical Coordination (with PKG-17)**
- Provide electrical load data from data sheets to electrical team:
  - Fire pump motor power, voltage, phase, frequency
  - Fire alarm panel power requirements, battery load
  - Detection and notification device power consumption
- Receive from electrical team:
  - Confirmation of available power supply (voltage, capacity)
  - Electrical disconnect and circuit protection sizing
- Update data sheets with coordinated electrical data
- **Output:** Coordinated electrical data on data sheets

**3.2 Control System Coordination (with PKG-19)**
- Provide control system interface data from data sheets to I&C team:
  - Fire alarm panel communication protocol, I/O requirements
  - Fire pump status/alarm monitoring requirements
- Receive from I&C team:
  - SCADA/DCS interface specifications
  - I/O assignments
  - Communication protocol details
- Update data sheets with coordinated I&C data
- **Output:** Coordinated I&C data on data sheets

**3.3 Structural Coordination (with PKG-06)**
- Provide equipment load data from data sheets to structural team:
  - Fire pump weight (operating and empty), footprint, anchor bolt pattern
  - Foam storage tank weight (full and empty), footprint
  - Fire alarm panel weight (if significant)
- Structural team uses load data for foundation/support design
- **Output:** Equipment load data provided to structural team

**3.4 Procurement/Constructability Review**
- Procurement team reviews data sheets for equipment specifications, availability, lead times
- Construction team reviews data sheets for constructability, installation requirements
- Resolve procurement/constructability comments
- **Output:** Procurement/constructability-reviewed data sheets

### Step 4: Data Sheet Review and Checking

**4.1 Self-Check**
- Engineer reviews data sheets for completeness, accuracy, consistency with design documents (drawings, specifications, calculations)
- Verify equipment tags match drawings
- Verify specifications match technical specification (DEL-23.02)
- Verify performance requirements match calculations (DEL-23.03)
- **Output:** Self-checked data sheets, self-check notes

**4.2 Cross-Document Consistency Check**
- Cross-check data sheets with:
  - DEL-23.01 (drawings): equipment tags, locations, quantities
  - DEL-23.02 (specification): equipment specifications, materials, standards
  - DEL-23.03 (calculations): performance requirements, sizing
- Resolve any inconsistencies
- **Output:** Consistency-checked data sheets, consistency check log

**4.3 Interdisciplinary Check (IDC)**
- Electrical, I&C, structural, procurement teams review data sheets for interface coordination and completeness
- IDC comments tracked and resolved
- **Output:** IDC-reviewed data sheets, IDC comment log

**4.4 Independent Review**
- Qualified reviewer (independent from originator) reviews data sheets for technical correctness, completeness, standards compliance
- Reviewer documents review comments
- **Output:** Independent review comments

**4.5 Resolve Review Comments**
- Originator reviews and incorporates corrections
- Coordinate with reviewer to resolve disagreements
- Update data sheets
- **Output:** Revised data sheets with review comments resolved

**4.6 Reviewer Sign-off**
- Reviewer verifies comments resolved satisfactorily and signs off
- **Output:** Reviewer sign-off (**TBD:** sign-off format per project)

### Step 5: Approval and Issue

**5.1 Discipline Lead Approval**
- Discipline lead reviews data sheets for overall adequacy and consistency with project requirements
- Discipline lead approves data sheets for issue
- **Output:** Discipline lead approval (**TBD:** approval format per project)

**5.2 Issue Data Sheets (Design Intent Issue)**
- Finalize data sheets with all sign-offs and approvals
- Assign final revision number (Rev 0 for initial issue) — **TBD** per project revision system
- Generate PDF from source files (Word/Excel)
- Issue data sheets via project document management system or per document control procedures
- **TBD:** Distribution list (typically: design team, procurement, construction, Employer)
- **Output:** Issued data sheets (design intent), transmittal record

**5.3 Update Deliverable Status**
- Update `_STATUS.md` to reflect deliverable lifecycle state:
  - INITIALIZED → IN_PROGRESS (when data sheet work commences)
  - IN_PROGRESS → CHECKING (when data sheets issued for formal review)
  - CHECKING → ISSUED (when data sheets formally issued)
- Copy issued data sheets to `3_Issued/` folder per framework conventions
- **Output:** Updated `_STATUS.md`, issued data sheets archived in `3_Issued/`

### Step 6: Procurement Phase (Vendor Submittals)

**6.1 Vendor Equipment Submittals**
- During procurement, vendors submit equipment submittals (product data sheets, drawings) for proposed equipment
- Procurement team and engineering team review submittals against data sheet requirements
- Verify vendor-proposed equipment meets data sheet specifications and performance requirements
- **Output:** Submittal review and approval/comments

**6.2 Update Data Sheets (As-Purchased) — Optional**
- After equipment procurement, optionally update data sheets with as-purchased equipment information (actual manufacturer, model, performance, dimensions)
- "As-purchased" data sheets reflect actual equipment selected
- Issue revised data sheets (Rev 1 or As-Purchased revision)
- **TBD:** As-purchased data sheet requirement per project
- **Output:** As-purchased data sheets (if required)

### Step 7: Data Sheet Revisions

**7.1 Revise Data Sheets (if changes required)**
- If design changes or procurement changes require data sheet updates, revise data sheets following steps 2–5 above
- Document revision description in data sheet revision history
- Increment revision number per project system
- Re-perform review and approval steps
- **TBD:** Revision approval authority and change control process
- **Output:** Revised data sheets

## Verification

**Verification Activities:**

| Activity | Performed By | Acceptance Criteria | Source |
|----------|--------------|---------------------|--------|
| **Self-Check** | Data sheet engineer | Data sheets complete, accurate, consistent with design documents | **ASSUMPTION**: Engineering practice |
| **Cross-Document Consistency Check** | Engineer or coordination lead | Data sheets consistent with drawings, specifications, calculations | **ASSUMPTION**: Document coordination |
| **Interdisciplinary Check** | Electrical, I&C, structural, procurement teams | Interface data correct, IDC comments resolved | **ASSUMPTION**: Interdisciplinary coordination |
| **Independent Review** | Qualified reviewer | Data sheets technically correct, complete, standards-compliant, reviewer sign-off | **ASSUMPTION**: Quality control |
| **Procurement/Constructability Review** | Procurement and construction teams | Equipment available, constructible, procurement comments resolved | **ASSUMPTION**: Design-build review |
| **Vendor Submittal Review (during procurement)** | Engineering and procurement teams | Vendor-proposed equipment meets data sheet requirements | **ASSUMPTION**: Procurement verification |

**Sign-off Requirements:**

| Sign-off | Role | Meaning | Source |
|----------|------|---------|--------|
| Engineer Sign-off | Data sheet engineer | Engineer certifies data sheets accurate and complete | **ASSUMPTION**: Engineering responsibility |
| Reviewer Sign-off | Independent reviewer | Reviewer certifies data sheets reviewed and satisfactory | **ASSUMPTION**: Quality control |
| Approver Sign-off | Discipline lead | Approver authorizes data sheets for issue | **ASSUMPTION**: Approval authority |

**TBD:** Specific sign-off format and location per project quality procedures

## Records

**Documentation Outputs:**

| Record | Content | Purpose | Location | Source |
|--------|---------|---------|----------|--------|
| **Fire Hydrant Data Sheets** | Fire hydrant specifications (type, outlets, materials, performance) | Specify fire hydrants for procurement and installation | Working: `1_Working/DEL-23.04/` <br> Issued: `3_Issued/` | Decomposition: anticipated artifact |
| **Fire Alarm Panel Data Sheet** | Fire alarm control panel specifications (type, capacity, devices, power, communication) | Specify fire alarm panel for procurement and installation | Working: `1_Working/DEL-23.04/` <br> Issued: `3_Issued/` | Decomposition: anticipated artifact |
| **Fire Pump Data Sheet** | Fire pump specifications (type, capacity, driver, accessories) | Specify fire pump for procurement and installation | Working: `1_Working/DEL-23.04/` <br> Issued: `3_Issued/` | **ASSUMPTION**: If fire pump required |
| **Foam System Equipment Data Sheets** | Foam proportioning systems, storage tank, discharge devices specifications | Specify foam equipment for procurement and installation | Working: `1_Working/DEL-23.04/` <br> Issued: `3_Issued/` | **ASSUMPTION**: Foam system equipment |
| **Fire Detection/Notification Device Data Sheets** | Detection and notification device specifications | Specify fire alarm devices for procurement and installation | Working: `1_Working/DEL-23.04/` <br> Issued: `3_Issued/` | **ASSUMPTION**: Fire alarm devices |
| **Equipment List** | List of all equipment with tags and data sheet references | Equipment tracking | Project coordination folder — **TBD** | **ASSUMPTION**: Equipment list |
| **IDC Comment Log** | Interdisciplinary check comments and resolutions | Coordination record | `1_Working/DEL-23.04/` or project coordination folder — **TBD** | **ASSUMPTION**: IDC record |
| **Review Records** | Independent review comments, resolutions, sign-offs | Quality record | `1_Working/DEL-23.04/` or project quality folder — **TBD** | **ASSUMPTION**: Quality record |
| **Vendor Submittals** | Vendor equipment submittals and review comments | Procurement record | Project procurement folder — **TBD** | **ASSUMPTION**: Procurement record |

**Record Management:**
- All records managed per project document control procedures — **TBD**
- Electronic data sheet files (Word/Excel source files) retained in addition to PDFs
- Record retention per project retention requirements — **TBD** (typically 25+ years for equipment records)

**Deliverable Lifecycle and Folder Structure:**

| Lifecycle State | Folder Location | Purpose | Source |
|----------------|-----------------|---------|--------|
| INITIALIZED, IN_PROGRESS | `1_Working/DEL-23.04/` | Active working location | Framework conventions |
| CHECKING | `2_Checking/To/` (copy for review) | Review package location; working files remain in `1_Working/` | Framework conventions |
| ISSUED | `3_Issued/` (copy of issued data sheets) | Issued data sheet archive; working files remain in `1_Working/` | Framework conventions |

**Related Records from Other Deliverables:**

| Deliverable | Related Records | Relationship | Source |
|-------------|----------------|--------------|--------|
| DEL-23.01 | Fire Protection Design Drawing Set | Provides equipment list, tags, locations for data sheets | Decomposition PKG-23 |
| DEL-23.02 | Fire Protection Technical Specification | Provides equipment specifications that inform data sheets | Decomposition PKG-23 |
| DEL-23.03 | Fire Protection Design Calculations | Provides equipment sizing and performance requirements for data sheets | Decomposition PKG-23 |
| DEL-23.05 | Fire Protection Installation & Test Records | Testing per data sheet specifications; as-built data verification | Decomposition PKG-23 |
