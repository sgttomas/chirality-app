# Procedure: DEL-23.03 Fire Protection Design Calculations

## Purpose

This procedure defines the process for **producing** the **Fire Protection Design Calculations** within **PKG-23 Fire Protection** for the Canola Oil Transload Facility — Phase 1 Design & Build project.

**Scope of This Procedure:**

This procedure covers the workflow for developing, checking, and issuing fire protection design calculations per project quality and engineering standards.

**Deliverable Information:**
- **Deliverable ID:** DEL-23.03
- **Deliverable Type:** Calculation
- **Responsible Party:** D&B Contractor
- **Discipline:** Specialty (Fire Protection)
- **Source:** Decomposition DEL-23.03 and `_CONTEXT.md`

## Prerequisites

### Dependencies

**Dependency Tracking Mode:**
- **Mode:** NOT_TRACKED (Source: `_DEPENDENCIES.md`)
- **Coordination:** Dependencies coordinated externally by humans

**Upstream Dependencies (typical inputs for calculations):**

| Input | Source | Purpose | Status |
|-------|--------|---------|--------|
| Fire protection design drawings (preliminary or final) | DEL-23.01 | System layouts, pipe routing, tank locations, equipment locations for calculations | **TBD** — coordinate with design team |
| Facility design data | Various sources | Tank sizes, product properties, facility layout, operational data | **TBD** — from facility design |
| Fire water supply data | Employer or utility | Available flow and pressure from fire water source | **TBD** — obtain from Employer or municipal utility |
| Fire protection design basis | Internal or project documents | Design criteria, performance requirements, codes/standards | **TBD** — establish early in design |
| Equipment data (preliminary) | DEL-23.04 or vendors | Fire pump curves, foam equipment data (may be iterative) | **TBD** — coordinate with equipment selection |
| Employer's Requirements | Employer | Project-specific calculation requirements and criteria | **TBD** |

### Reference Materials

**Required References:**
- Employer's Requirements Volume 2 Parts 1–3 (**TBD**)
- NFPA 30: Flammable and Combustible Liquids Code (**TBD**)
- NFPA 24: Installation of Private Fire Service Mains (**TBD**)
- NFPA 20: Installation of Stationary Pumps for Fire Protection (**TBD** — if fire pump required)
- NFPA 11: Low-, Medium-, and High-Expansion Foam (**TBD**)
- NFPA 16: Installation of Foam-Water Sprinkler and Foam-Water Spray Systems (**TBD**)
- NFPA 72: National Fire Alarm and Signaling Code (**TBD**)
- NBCC 2020, BCFC (**TBD**)
- Hydraulic analysis software user manual (**TBD**)
- Fire equipment manufacturer technical data (**TBD**)

### Personnel Requirements

| Role | Qualifications | Source |
|------|----------------|--------|
| Fire Protection Engineer / Calculation Engineer | P.Eng. licensed in Canada, fire protection or mechanical discipline, experience with NFPA codes and fire protection calculations | **ASSUMPTION**: Professional engineering requirement |
| Calculation Checker | P.Eng., independent from originator, calculation review experience | **ASSUMPTION**: Engineering quality control |
| Discipline Lead / Approver | Senior P.Eng., authority to approve calculations for use in design | **ASSUMPTION**: Engineering approval authority |

### Tools and Software

| Tool | Purpose | Source |
|------|---------|--------|
| Hydraulic analysis software (AFT Fathom, PIPE-FLO, AutoSPRINK, or equivalent) | Fire water system hydraulic network analysis | **ASSUMPTION**: Standard hydraulic calculation tool |
| Spreadsheet software (Microsoft Excel, MathCAD, or equivalent) | Fire water demand calculations, foam system calculations, general calculations | **ASSUMPTION**: General calculation tool |
| Fire alarm design software (if applicable) | Fire alarm coverage analysis, battery capacity calculations | **ASSUMPTION**: Specialized tool (if used) |

## Steps

### Step 1: Planning and Setup

**1.1 Review Calculation Scope and Requirements**
- Review deliverable scope (`_CONTEXT.md`, Specification.md, Guidance.md)
- Review Employer's Requirements for fire protection calculation requirements and design criteria
- Review applicable codes (NFPA 30, NFPA 24, NFPA 20, NFPA 11, NFPA 16, NFPA 72)
- **Output:** Understanding of calculation scope and requirements

**1.2 Obtain Input Data**
- Obtain facility design data (tank sizes, spacing, facility layout, operational data) from facility design team
- Obtain fire water supply data (available flow/pressure) from Employer or municipal utility (coordinate with civil/utilities team)
- Obtain preliminary fire protection drawings (DEL-23.01) for system layouts and dimensions
- Obtain product properties (flash point, density, viscosity) from process engineering or product specifications
- **TBD:** Input data sources and availability
- **Output:** Calculation input data package

**1.3 Establish Calculation List and Numbering**
- Develop list of calculations required:
  - Fire water demand calculation
  - Hydraulic calculation
  - Tank foam system calculations (for each tank or representative tanks)
  - Marine loading foam system calculation
  - Fire pump sizing calculation (if applicable)
  - Fire alarm battery capacity calculation
  - Fire alarm coverage analysis (if required)
- Assign calculation numbers per project numbering system — **TBD**
- **Output:** Calculation list with assigned numbers

**1.4 Set Up Calculation Tools**
- Set up hydraulic analysis software with project model (fire water loop network)
- Set up spreadsheet templates or MathCAD templates for calculations
- Verify software versions and validation status
- **Output:** Calculation tools ready for use

### Step 2: Fire Water Demand Calculation

**2.1 Define Fire Protection Zones and Fire Scenarios**
- Identify fire protection zones (tank farm, marine loading, railcar unloading, pump house, buildings)
- Identify credible fire scenarios per NFPA 30 (largest single tank fire, marine loading fire, rail loading fire, exposure fires)
- Determine worst-case scenario for fire water demand (typically largest tank fire + exposures)
- **Output:** Fire scenario definition and worst-case determination

**2.2 Calculate Tank Foam System Demand**
- For largest tank (or each tank if varies significantly):
  - Tank diameter and surface area (ft²)
  - Foam application rate per NFPA 11/16 (gpm/ft²) — based on product classification and foam type
  - Foam solution demand (gpm) = surface area × application rate
  - Foam concentrate percentage (3% or 6%) and foam concentrate demand (gpm)
  - Discharge duration (typically 55 minutes for hydrocarbon foams) — per NFPA 11/16
  - Foam concentrate storage volume (gallons) = concentrate demand × duration
- **Calculation Basis:** NFPA 11, NFPA 16, tank dimensions from DEL-23.01
- **Output:** Tank foam system demand (gpm, duration, concentrate volume)

**2.3 Calculate Cooling Water Demand**
- Determine adjacent tanks requiring cooling per NFPA 30 (tanks within exposure distance)
- Cooling water application rate per NFPA 30 (gpm/ft² of tank surface area)
- Total cooling demand (gpm) = sum of cooling demands for exposed tanks
- **Calculation Basis:** NFPA 30, tank locations and spacing from DEL-23.01
- **Output:** Cooling water demand (gpm)

**2.4 Calculate Hydrant/Monitor Demand**
- Number of hydrant streams required per NFPA 30 or risk assessment (typically 2–4 streams)
- Flow rate per hydrant stream (typically 250–500 gpm per stream)
- Total hydrant demand (gpm) = number of streams × flow per stream
- **Calculation Basis:** NFPA 30, facility size and risk
- **Output:** Hydrant/monitor demand (gpm)

**2.5 Calculate Marine/Rail Loading Demand (if simultaneous)**
- Determine if marine or rail loading fire protection demand is simultaneous with tank fire (depends on risk assessment and operational procedures)
- Marine loading foam demand (gpm) if applicable
- Rail loading protection demand (gpm) if applicable
- **Calculation Basis:** NFPA 30, operational procedures, risk assessment
- **Output:** Marine/rail loading demand (gpm) — if simultaneous

**2.6 Calculate Total Fire Water Demand**
- Total fire water demand (gpm) = tank foam demand + cooling demand + hydrant demand + marine/rail demand (if simultaneous)
- Fire water duration (hours) = longest demand duration (typically foam discharge duration)
- Total fire water volume (gallons) = total demand (gpm) × duration (minutes)
- **Output:** Total fire water demand summary

**2.7 Document Fire Water Demand Calculation**
- Prepare calculation package:
  - Cover sheet with calculation title, number, engineer, date
  - Design basis and fire scenario description
  - Input data (tank sizes, foam rates, codes, assumptions)
  - Calculation steps (foam demand, cooling demand, hydrant demand, total)
  - Results and conclusions
  - References
- **Output:** Fire water demand calculation package (draft)

### Step 3: Hydraulic Calculation

**3.1 Develop Fire Water System Model**
- Build hydraulic network model in hydraulic analysis software:
  - Fire water loop piping layout from DEL-23.01 drawings
  - Pipe segments (lengths, diameters, materials)
  - Hydrant nodes
  - Fire pump (if applicable)
  - Water supply source (flow/pressure characteristics)
  - Elevation changes
- Input pipe roughness (Hazen-Williams C-factor) — use conservative values (e.g., C=120 for steel, C=140 for ductile iron)
- **Output:** Hydraulic network model

**3.2 Define Demand Scenarios**
- Set up demand scenarios in hydraulic model:
  - Most hydraulically remote hydrant at required flow rate (from fire water demand calculation)
  - Multiple hydrants flowing if required by demand calculation
  - Tank foam system demand nodes (if modeled)
- Define acceptance criteria: minimum residual pressure at demand points (typically 20 psi minimum per NFPA 24, or higher per NFPA 30/design criteria)
- **Output:** Demand scenarios defined in model

**3.3 Run Hydraulic Analysis**
- Run hydraulic analysis for demand scenarios
- Analyze results:
  - Pressure at each node (hydrants, demand points)
  - Flow in each pipe segment
  - Velocity in pipes (check for excessive velocity >15 fps)
  - Fire pump operating point (if applicable)
- Identify any deficiencies (low pressure, undersized pipes, excessive velocity)
- **Output:** Hydraulic analysis results

**3.4 Adjust Pipe Sizes or Fire Pump Capacity (if needed)**
- If pressures inadequate or velocities excessive, adjust design:
  - Increase pipe sizes in critical segments
  - Increase fire pump capacity/head (if fire pump used)
  - Adjust fire water loop configuration
- Re-run hydraulic analysis with adjustments
- Iterate until all acceptance criteria met
- **Output:** Optimized fire water system design

**3.5 Perform Sensitivity Analysis (optional)**
- Vary key parameters to assess design robustness:
  - Pipe roughness (vary C-factor)
  - Demand scenarios (vary flow rates, number of streams)
  - Fire water loop with one section out of service
- Verify design adequate under variations
- **Output:** Sensitivity analysis results (if performed)

**3.6 Document Hydraulic Calculation**
- Prepare calculation package:
  - Cover sheet
  - Design basis and hydraulic model description
  - Input data (pipe layout, sizes, roughness, elevations, demand)
  - Hydraulic analysis methodology
  - Results (pressures, flows, velocities, system curve)
  - Conclusions and design recommendations (pipe sizes, fire pump capacity)
  - References
  - Appendix: Hydraulic software output (network diagram, results tables, system curve plot)
- **Output:** Hydraulic calculation package (draft)

### Step 4: Foam System Calculations

**4.1 Tank Foam System Calculations**
- For each storage tank (or representative tanks):
  - Calculate foam solution demand (gpm) — from Step 2.2 above
  - Calculate foam concentrate storage volume (gallons) — from Step 2.2 above
  - Calculate foam proportioning system capacity (gpm) — typically equals foam solution demand
  - Calculate foam discharge device capacity (gpm) — typically equals foam solution demand / number of devices
  - Select foam discharge device type (fixed foam chamber, foam maker, Type II/III outlet) and size per NFPA 11/16
- **Output:** Tank foam system sizing calculation for each tank

**4.2 Marine Loading Foam System Calculation (if applicable)**
- Calculate foam demand for marine loading arms per NFPA 11/16
- Size foam system components (foam storage, proportioning, discharge nozzles/monitors)
- **Output:** Marine loading foam system sizing calculation

**4.3 Document Foam System Calculations**
- Prepare calculation package(s):
  - Cover sheet
  - Design basis
  - Input data (tank sizes, foam rates, foam concentrate properties)
  - Calculation steps
  - Results (foam storage volume, proportioning capacity, discharge device sizing)
  - References
- **Output:** Foam system calculation packages (draft)

### Step 5: Fire Pump Sizing Calculation (if applicable)

**5.1 Determine Fire Pump Requirements**
- Total fire water demand (gpm) from Step 2.6
- Required pressure at most remote hydrant (from hydraulic analysis Step 3.3)
- Available supply pressure (from water supply source data)
- Fire pump head (psi or ft) = required pressure – available supply pressure + losses + safety margin
- **Output:** Fire pump head and flow requirements

**5.2 Size Fire Pump per NFPA 20**
- Fire pump capacity = 150% of demand per NFPA 20 (or 100% if justified)
- Fire pump rated head at 150% flow
- Fire pump power (HP or kW) based on pump efficiency and head
- **Output:** Fire pump sizing

**5.3 Select Fire Pump from Manufacturer Curves**
- Review fire pump manufacturer pump curves
- Select pump model that meets capacity and head requirements
- Verify pump curve meets system demand curve (pump curve above system curve at all flow rates)
- **Output:** Fire pump selection

**5.4 Document Fire Pump Sizing Calculation**
- Prepare calculation package:
  - Cover sheet
  - Design basis
  - Input data (demand, pressures, supply characteristics)
  - Calculation steps (pump head, capacity, power)
  - Pump selection and pump curve
  - References
  - Appendix: Manufacturer pump curves
- **Output:** Fire pump sizing calculation package (draft)

### Step 6: Fire Alarm System Calculations (if applicable)

**6.1 Fire Alarm Battery Capacity Calculation**
- Determine fire alarm system load (standby current, alarm current) from equipment data sheets
- Calculate battery capacity per NFPA 72: standby for 24 hours + alarm for 5 minutes (or per project requirements)
- Size battery (amp-hours)
- **Output:** Fire alarm battery sizing calculation

**6.2 Fire Alarm Coverage Analysis (if required)**
- Perform audibility coverage analysis (horn decibel levels at distances)
- Perform visibility coverage analysis (strobe candela and spacing per NFPA 72)
- Verify code-compliant coverage
- **Output:** Fire alarm coverage analysis (if performed)

**6.3 Document Fire Alarm Calculations**
- Prepare calculation package(s)
- **Output:** Fire alarm calculation packages (draft)

### Step 7: Calculation Checking and Review

**7.1 Self-Check**
- Engineer performing calculations reviews for:
  - Completeness (all required calculations performed)
  - Accuracy (arithmetic correct, formulas correct)
  - Units consistent
  - Input data sources cited
  - Assumptions identified
  - Results reasonable (order of magnitude check, comparison to similar facilities)
- **Output:** Self-checked calculations, self-check notes

**7.2 Calculation Verification (as applicable)**
- Complex or critical calculations verified using:
  - Hand calculation for simplified case
  - Alternative software or method
  - Comparison to published data or design charts
- **Output:** Verification calculations or comparison documentation

**7.3 Independent Check**
- Qualified independent checker (P.Eng., not the originator) reviews calculations for:
  - Methodology correct and appropriate
  - Input data correct and from valid sources
  - Calculations correct (spot-check arithmetic, verify formulas)
  - Results reasonable and conclusions sound
  - Documentation complete and clear
  - Code compliance
- Checker documents review comments
- **Output:** Independent check comments

**7.4 Resolve Check Comments**
- Originator reviews check comments and incorporates corrections
- Coordinate with checker to resolve disagreements
- Update calculations
- **Output:** Revised calculations with check comments resolved

**7.5 Checker Sign-off**
- Checker verifies comments resolved satisfactorily
- Checker signs calculation packages to indicate independent check complete
- **Output:** Checker sign-off (**TBD:** sign-off format per project)

### Step 8: Cross-Document Coordination

**8.1 Update Drawings with Calculation Results**
- Provide calculation results to drawing team (DEL-23.01):
  - Fire water pipe sizes
  - Fire pump capacity and head (if applicable)
  - Foam system equipment sizes
  - Performance requirements
- Verify drawings updated with calculation results
- **Output:** Coordinated drawings and calculations

**8.2 Update Specifications with Calculation Results**
- Provide calculation results to specification team (DEL-23.02):
  - Fire water demand (gpm, duration)
  - Fire water pressure requirements
  - Fire pump specifications (if applicable)
  - Foam system performance requirements
- Verify specifications updated with calculation results
- **Output:** Coordinated specifications and calculations

**8.3 Update Data Sheets with Calculation Results**
- Provide calculation results to data sheet team (DEL-23.04):
  - Equipment sizing and performance requirements
- Verify data sheets consistent with calculations
- **Output:** Coordinated data sheets and calculations

**8.4 Cross-Document Consistency Check**
- Verify consistency between calculations, drawings, specifications, and data sheets
- Resolve any inconsistencies
- **Output:** Consistent document set

### Step 9: Approval and Issue

**9.1 Discipline Lead Approval**
- Discipline lead reviews calculations for overall adequacy and consistency with project requirements
- Discipline lead approves calculations for use in design
- **Output:** Discipline lead approval (**TBD:** approval format per project)

**9.2 P.Eng. Seal (if required)**
- Professional Engineer seals and signs calculation packages if required by jurisdiction or Employer
- **TBD:** P.Eng. seal requirement
- **Output:** Sealed calculation packages (if required)

**9.3 Issue Calculations**
- Finalize calculation packages with all sign-offs and approvals
- Assign final revision number (**TBD:** per project revision system)
- Issue calculations via project document management system or per document control procedures
- **TBD:** Distribution list and issue procedures
- **Output:** Issued calculations, transmittal record

**9.4 Update Deliverable Status**
- Update `_STATUS.md` to reflect deliverable lifecycle state:
  - INITIALIZED → IN_PROGRESS (when calculation work commences)
  - IN_PROGRESS → CHECKING (when calculations issued for formal review)
  - CHECKING → ISSUED (when calculations formally issued)
- Copy issued calculations to `3_Issued/` folder per framework conventions
- **Output:** Updated `_STATUS.md`, issued calculations archived in `3_Issued/`

### Step 10: Calculation Revisions

**10.1 Revise Calculations (if changes required)**
- If design changes require calculation updates, revise calculations following steps 2–9 above
- Document revision description in calculation revision history
- Increment revision number per project system
- Re-perform independent check of revised calculations
- **TBD:** Revision approval authority and change control process
- **Output:** Revised calculations

## Verification

**Verification Activities:**

| Activity | Performed By | Acceptance Criteria | Source |
|----------|--------------|---------------------|--------|
| **Self-Check** | Calculation engineer | Calculations complete, accurate, correct methodology, units consistent | **ASSUMPTION**: Engineering practice |
| **Calculation Verification** | Engineer or checker | Complex calculations verified by alternative method or hand calculation | **ASSUMPTION**: Engineering verification practice |
| **Independent Check** | Qualified checker (P.Eng.) | Methodology correct, inputs correct, calculations correct, results reasonable, documentation complete, checker sign-off | **ASSUMPTION**: Engineering quality control |
| **Cross-Document Consistency Check** | Originator or coordination lead | Calculations consistent with drawings, specifications, data sheets | **ASSUMPTION**: Document coordination |
| **Code Compliance Verification** | Checker or code reviewer | Calculations comply with NFPA codes and other applicable standards | **ASSUMPTION**: Code compliance requirement |
| **Testing Verification (post-construction)** | Testing team | Field test results (flow test, pump test) compared to calculated values, assumptions validated | **ASSUMPTION**: Testing verification |

**Sign-off Requirements:**

| Sign-off | Role | Meaning | Source |
|----------|------|---------|--------|
| Engineer Sign-off | Calculation engineer (P.Eng.) | Engineer certifies calculations performed correctly to best of their knowledge | **ASSUMPTION**: Engineering responsibility |
| Checker Sign-off | Independent checker (P.Eng.) | Checker certifies independent check performed and calculations satisfactory | **ASSUMPTION**: Engineering quality control |
| Approver Sign-off | Discipline lead or designated approver (P.Eng.) | Approver authorizes calculations for use in design | **ASSUMPTION**: Approval authority |
| P.Eng. Seal | Professional Engineer (P.Eng.) | Professional engineer seals calculations (if required by jurisdiction or Employer) | **ASSUMPTION**: Professional engineering requirement |

**TBD:** Specific sign-off format and location per project quality procedures

## Records

**Documentation Outputs:**

| Record | Content | Purpose | Location | Source |
|--------|---------|---------|----------|--------|
| **Fire Water Demand Calculation** | Design basis, fire scenarios, foam demand, cooling demand, hydrant demand, total demand, references | Determine fire water requirements for facility | Working: `1_Working/DEL-23.03/` <br> Issued: `3_Issued/` | Decomposition: anticipated artifact |
| **Hydraulic Calculation** | Design basis, hydraulic model, input data, hydraulic analysis, results (pressures, flows), pipe sizing, fire pump sizing, references | Verify fire water system capacity and size equipment | Working: `1_Working/DEL-23.03/` <br> Issued: `3_Issued/` | Decomposition: anticipated artifact |
| **Tank Foam System Calculations** | Design basis, tank sizes, foam demands, foam storage sizing, proportioning sizing, discharge device sizing, references | Size tank foam systems | Working: `1_Working/DEL-23.03/` <br> Issued: `3_Issued/` | **ASSUMPTION**: Required calculations |
| **Marine Loading Foam Calculation** | Design basis, foam demand, foam system sizing, references | Size marine loading foam system | Working: `1_Working/DEL-23.03/` <br> Issued: `3_Issued/` | **ASSUMPTION**: Required calculations |
| **Fire Pump Sizing Calculation** | Design basis, demand, pressures, pump head/capacity, pump selection, references | Size and select fire pump | Working: `1_Working/DEL-23.03/` <br> Issued: `3_Issued/` | **ASSUMPTION**: If fire pump required |
| **Fire Alarm Calculations** | Battery capacity calculation, coverage analysis | Size fire alarm battery and verify coverage | Working: `1_Working/DEL-23.03/` <br> Issued: `3_Issued/` | **ASSUMPTION**: Fire alarm calculations |
| **Calculation Register** | List of calculations with numbers, revisions, dates | Tracking and document control | Project DMS — **TBD** | **ASSUMPTION**: Document control |
| **Independent Check Records** | Check comments, resolutions, checker sign-off | Quality record | `1_Working/DEL-23.03/` or project quality folder — **TBD** | **ASSUMPTION**: Quality record |
| **Calculation Verification Records** | Verification calculations, comparisons | Verification record | `1_Working/DEL-23.03/` | **ASSUMPTION**: Verification documentation |

**Record Management:**
- All records managed per project document control procedures — **TBD**
- Electronic calculation files (Excel, MathCAD, hydraulic software files) retained in addition to PDF packages
- Record retention per project retention schedule — **TBD** (typically 25+ years for design calculations)

**Deliverable Lifecycle and Folder Structure:**

| Lifecycle State | Folder Location | Purpose | Source |
|----------------|-----------------|---------|--------|
| INITIALIZED, IN_PROGRESS | `1_Working/DEL-23.03/` | Active working location | Framework conventions |
| CHECKING | `2_Checking/To/` (copy for review) | Review package location; working files remain in `1_Working/` | Framework conventions |
| ISSUED | `3_Issued/` (copy of issued calculations) | Issued calculation archive; working files remain in `1_Working/` | Framework conventions |

**Related Records from Other Deliverables:**

| Deliverable | Related Records | Relationship | Source |
|-------------|----------------|--------------|--------|
| DEL-23.01 | Fire Protection Design Drawing Set | Drawings provide layout data for calculations; calculation results (pipe sizes, equipment capacities) appear on drawings | Decomposition PKG-23 |
| DEL-23.02 | Fire Protection Technical Specification | Calculation results define specification performance requirements (flow rates, pressures, capacities) | Decomposition PKG-23 |
| DEL-23.04 | Fire Protection Data Sheet Package | Calculation results size equipment (data sheets); equipment data from data sheets used as calculation inputs | Decomposition PKG-23 |
| DEL-23.05 | Fire Protection Installation & Test Records | Field test results verify calculation assumptions and results (flow test, pump test) | Decomposition PKG-23 |
