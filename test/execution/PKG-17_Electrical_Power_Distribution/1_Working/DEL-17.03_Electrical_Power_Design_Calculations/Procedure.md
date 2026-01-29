# Procedure: DEL-17.03 Electrical Power Design Calculations

## Purpose

This procedure defines the process for producing and managing **Electrical Power Design Calculations** within **PKG-17 Electrical Power Distribution**.

**Deliverable Purpose** (Source: Decomposition DEL-17.03 entry): Provides the engineering basis and sizing/verification calculations for electrical power.

**Deliverable Type**: Calculation
**Responsible Party**: D&B Contractor
**Discipline**: Electrical

## Prerequisites

### Dependencies

**Per _DEPENDENCIES.md**: NOT_TRACKED — Dependencies coordinated externally by humans.

**Typical upstream dependencies**:
- Equipment list and motor data (from process engineering and mechanical packages)
- Utility service information (BC Hydro voltage class and fault current)
- Preliminary single line diagrams (DEL-17.01 — developed concurrently)
- Project design criteria and load requirements (Employer's Requirements)

### Reference Materials

**Required references**:
- **Employer's Requirements**: **TBD** — Volume 2 Parts 1-3 (electrical load data, design criteria)
- **Decomposition Document**: Section 4 — PKG-17, DEL-17.03 entry
- **Calculation Standards**: IEEE Std 141, IEEE Std 242, IEEE Std 80, CEC, CSA Z462

**Supporting deliverables**:
- DEL-17.01 (Design Drawing Set) — single line diagrams, cable schedules
- DEL-17.02 (Technical Specification) — equipment performance criteria
- Motor and equipment data from mechanical/process packages

### Personnel Requirements

**Calculation Originator**: P.Eng. or senior electrical engineer/designer; proficient in electrical analysis software (ETAP/SKM)
**Checker**: Independent P.Eng. or senior engineer (not originator); qualified to perform independent check calculations
**Approver**: P.Eng. (discipline lead); authority to approve calculations for construction

## Steps

### Step 1: Input Data Collection

**Objective**: Gather all data required for calculations.

**Activities**:
1.1. **Electrical Load Data**:
     - Motor list (HP, voltage, FLA, starting method) from mechanical/process packages
     - Lighting load (watts) from PKG-18
     - HVAC load from mechanical
     - Control system and UPS loads from PKG-19
     - Receptacle and miscellaneous loads (estimate based on building areas)
1.2. **Utility Data** (from BC Hydro coordination):
     - Service voltage (25 kV or 13.8 kV)
     - Available fault current at service point
     - Utility protection requirements (reclosing, coordination)
1.3. **Equipment Data**:
     - Transformer impedances (manufacturer data or standard values)
     - Cable impedances (from CEC/IEEE tables or manufacturer data)
     - Circuit breaker and protective device characteristics (time-current curves)
1.4. **Site Data**:
     - Cable lengths (from preliminary site plan and building layouts)
     - Ambient temperature (climate data)
     - Soil resistivity (for grounding calculations — geotechnical data or field measurements)
1.5. **Design Criteria**:
     - Voltage drop limits (3% feeder, 5% total per IEEE)
     - Spare capacity requirements (20-25% typical)
     - Power factor assumptions (0.85-0.90 for motors)

**Output**: Input data summary with sources identified; TBDs documented.

### Step 2: Load Calculations

**Objective**: Calculate connected load, demand load, and transformer/switchgear sizing.

**Activities**:
2.1. **Organize Loads**:
     - Group loads by voltage level (600V, 480V, 208V-120V)
     - Group loads by distribution point (substation, MCC, panel)
2.2. **Calculate Connected Load**:
     - Sum nameplate ratings for each load category
     - Motors: HP × 0.746 kW/HP / PF (or use FLA × voltage × √3 for kVA)
     - Lighting: watts from lighting design
     - HVAC, receptacles: nameplate or estimated loads
2.3. **Apply Demand Factors**:
     - Use CEC Table 14 or IEEE Std 141 Chapter 4 guidance
     - Document demand factor assumptions (typical: 0.7-0.85 for industrial motor loads)
2.4. **Calculate Demand Load**:
     - Demand Load (kVA) = Connected Load (kVA) × Demand Factor
2.5. **Size Transformers**:
     - Add spare capacity (20-25% for future expansion)
     - Select standard transformer sizes (1000 kVA, 1500 kVA, 2000 kVA, etc.)
2.6. **Size Switchgear and MCC Buses**:
     - Calculate continuous current: I = kVA / (√3 × kV)
     - Select standard bus ratings (1200A, 1600A, 2000A, etc.)

**Output**: Load calculation summary (Excel spreadsheet or similar) showing connected load, demand factors, demand load, and equipment sizing.

**Verification**: Cross-check motor data against mechanical packages; verify demand factors are reasonable.

### Step 3: Short Circuit Analysis

**Objective**: Calculate fault currents to verify equipment ratings.

**Activities**:
3.1. **Build System Model** (in ETAP or SKM):
     - Model utility source (voltage, fault current from Step 1.2)
     - Model transformers (kVA, impedance)
     - Model cables (size, length, impedance)
     - Model switchgear and MCC buses
     - Model motors (contribute to fault current)
3.2. **Run Short Circuit Analysis**:
     - Calculate 3-phase fault current at each bus
     - Calculate line-to-ground fault current at each bus
     - Calculate X/R ratios
3.3. **Verify Equipment Ratings**:
     - Compare calculated fault current vs. equipment SCCR (short circuit current rating)
     - Verify circuit breaker interrupting capacity ≥ 125% of calculated fault current
     - Flag any equipment with inadequate ratings
3.4. **Document Results**:
     - Fault current summary table (bus name, 3-phase fault kA, L-G fault kA, X/R)
     - Equipment rating verification table

**Output**: Short circuit analysis report (ETAP/SKM output) with fault current table and equipment verification.

**Verification**: Spot-check results with hand calculation for one bus; verify system model matches single line diagram.

### Step 4: Protection Coordination Study

**Objective**: Coordinate protective devices for selective operation.

**Activities**:
4.1. **Compile Protective Device Data**:
     - Circuit breaker time-current curves (from manufacturer data)
     - Fuse time-current curves
     - Protective relay characteristics (51, 50, 50/51, etc.)
4.2. **Plot Time-Current Curves** (in ETAP or SKM):
     - Plot all devices on log-log TCC graph
     - Plot in sequence from load to source
4.3. **Adjust Settings for Coordination**:
     - Set relay pickups and time delays to achieve minimum coordination interval (0.2-0.3 sec)
     - Verify devices do not trip on motor starting inrush
     - Iterate settings until coordination achieved
4.4. **Document Relay Settings**:
     - Relay settings table (device, pickup, time dial, instantaneous)
     - Coordination verification notes

**Output**: Protection coordination study report (ETAP/SKM output) with TCC plots and relay settings table.

**Verification**: Verify coordination intervals at all current levels; verify motor starting coordination.

### Step 5: Voltage Drop Analysis

**Objective**: Verify cable sizing meets voltage drop limits.

**Activities**:
5.1. **List All Feeders and Branch Circuits**:
     - Circuit ID, voltage, load current, cable size, length
5.2. **Calculate Voltage Drop**:
     - Use formula: VD = √3 × I × (R cosθ + X sinθ) × L for 3-phase
     - Obtain R and X from CEC/IEEE tables or cable data
     - Use power factor from load calculations
5.3. **Calculate Cumulative Voltage Drop**:
     - Sum feeder and branch circuit voltage drops
5.4. **Verify Against Limits**:
     - Feeder VD ≤ 3%, Total VD ≤ 5%
     - Flag circuits exceeding limits
5.5. **Upsize Cables if Required**:
     - Increase cable size for circuits exceeding voltage drop limits
     - Recalculate voltage drop with larger cable

**Output**: Voltage drop summary table (Excel or similar) showing circuit, cable size, length, current, VD%, cumulative VD%.

**Verification**: Spot-check calculations; verify cable sizes meet both ampacity (CEC) and voltage drop.

### Step 6: Grounding Grid Design (if included)

**Objective**: Design grounding grid per IEEE Std 80.

**Activities** (high-level):
6.1. Obtain soil resistivity data
6.2. Design grid layout (conductor size, spacing, ground rods)
6.3. Calculate grid resistance
6.4. Calculate step and touch potentials during fault
6.5. Verify potentials within safe limits (IEEE Std 80 criteria)

**Output**: Grounding calculation report with grid design and safety verification.

**TBD**: Confirm if grounding calculations included in this deliverable.

### Step 7: Arc Flash Hazard Analysis (if included)

**Objective**: Calculate arc flash incident energy per CSA Z462.

**Activities** (high-level):
7.1. Calculate incident energy at each electrical equipment location (using ETAP/SKM)
7.2. Determine arc flash boundaries
7.3. Assign PPE categories
7.4. Prepare arc flash label content

**Output**: Arc flash hazard analysis report with incident energy table and label templates.

**TBD**: Confirm if arc flash analysis included in this deliverable.

### Step 8: Calculation Documentation and Formatting

**Objective**: Organize and format calculations for review.

**Activities**:
8.1. **Title Page**: Calculation title, number, date, revision, originator, checker, approver
8.2. **Table of Contents**: List of calculation sections
8.3. **Design Basis**: Assumptions, criteria, codes/standards
8.4. **Input Data Summary**: Sources of input data
8.5. **Calculations**: Organized by type (load, short circuit, coordination, voltage drop)
8.6. **Results and Conclusions**: Summary of key results; equipment sizing recommendations
8.7. **Appendices**: Software output files, manufacturer data, reference documents

**Output**: Complete calculation package ready for independent check.

### Step 9: Independent Check

**Objective**: Verify calculations are correct and complete.

**Check Method Options**:
- **Independent Calculation** (preferred): Checker performs parallel calculation using same inputs
- **Detailed Review**: Checker reviews original calculation line-by-line

**Check Scope**:
- Verify methodology appropriate (IEEE/CEC standards)
- Verify input data correct and traceable to sources
- Verify arithmetic and software calculations correct
- Verify results reasonable and conclusions valid
- Verify compliance with codes and standards

**Output**: Check comments (if any); checker sign-off when check complete.

**Resolution**: Originator addresses check comments; checker verifies resolutions.

### Step 10: Approval and Issue

**Objective**: Discipline lead approves calculations for use in design.

**Approval Process**:
10.1. Discipline lead (P.Eng.) reviews checked calculations
10.2. Verify calculations support design (equipment sizing, protection, safety)
10.3. Approve calculations (sign/seal if required)
10.4. Update calculation status to "Approved" or "Issued for Construction"
10.5. File issued calculations in 3_Issued/ folder

**Output**: Approved calculation package.

### Step 11: Calculation Updates and Revisions

**Objective**: Maintain calculations current as design evolves.

**Revision Triggers**:
- Load changes (equipment added, sizes changed)
- Equipment changes (transformer sizes, breaker ratings)
- Utility data updates (fault current)
- Design changes affecting electrical system

**Revision Process**:
11.1. Identify sections affected by changes
11.2. Update affected calculations
11.3. Re-check revised calculations (independent check)
11.4. Re-approve revised calculations
11.5. Update revision history (describe changes)
11.6. Issue revised calculations (increment revision number)

**Output**: Revised calculation package (Rev A, Rev B, etc.).

## Verification

**Verification Activities Summary**:

| Activity | Method | Acceptance Criteria | Responsibility |
|----------|--------|---------------------|----------------|
| **Input Data Check** | Verify data sources | All input data traceable; assumptions documented | Originator |
| **Methodology Check** | Review methodology | Per IEEE/CEC standards | Checker |
| **Independent Check** | Independent calc or detailed review | Results agree (±5%); conclusions valid | Checker (P.Eng.) |
| **Software Verification** | Model verification, hand calc spot-check | Model correct; results reasonable | Checker |
| **Code Compliance** | Verify compliance with CEC, IEEE | All requirements met | Checker + P.Eng. |
| **Cross-Document Check** | Compare with drawings/specs | Consistent equipment sizing | Checker |

**Sign-Off Requirements**:
- Originator: Initials/date (calculation complete)
- Checker: Initials/date (independent check complete)
- Approver (P.Eng.): Signature/date (approved for construction)

## Records

**Documentation Outputs** (Source: _CONTEXT.md):
1. Load calculations
2. Short circuit analysis
3. Protection coordination study
4. Voltage drop analysis
5. Grounding grid design (if included)
6. Arc flash hazard analysis (if included)

**Record Management**:

**During Development (1_Working/)**:
- Working calculation files (ETAP, SKM, Excel)
- Draft calculation reports

**During Review (2_Checking/)**:
- Calculations submitted for check in 2_Checking/To/
- Check comments in 2_Checking/From/

**Upon Approval (3_Issued/)**:
- Approved calculations (PDF format for distribution, native files for future revisions)
- Calculation register (tracking calculation numbers, revisions, status)

**Retention**: Per project document control procedures and professional engineering requirements.

**Interfaces**:
- DEL-17.01 (Drawings): Calculations support equipment shown on drawings
- DEL-17.02 (Specifications): Calculations determine equipment ratings
- DEL-17.04 (Data Sheets): Calculations verified against actual equipment
