# Datasheet: DEL-17.03 Electrical Power Design Calculations

## Identification

| Field | Value |
|-------|-------|
| Deliverable ID | DEL-17.03 |
| Name | Electrical Power Design Calculations |
| Package | PKG-17 Electrical Power Distribution |
| Discipline | Electrical |
| Type | Calculation |
| Responsible | D&B Contractor |
| Status | INITIALIZED |

## Attributes

| Attribute | Value |
|-----------|-------|
| Calculation Number | **TBD** — To be assigned per project calculation numbering system |
| Software Used | **ASSUMPTION**: ETAP, SKM PowerTools, or equivalent electrical analysis software for load flow, short circuit, and protection coordination |
| Design Codes | CEC (CSA C22.1), IEEE Std 141 (Red Book), IEEE Std 242, IEEE Std 80, CSA C68.3 |
| Revision | 0 (Initial issue) |
| Classification | For Construction |
| Calculation Package Contents | Load calculations, short circuit analysis, protection coordination, voltage drop (Source: _CONTEXT.md) |

### Calculation Types and Purposes

**Source**: _CONTEXT.md anticipated artifacts; typical electrical design calculation requirements.

| Calculation Type | Purpose | Methodology/Standard | Software Tool | Specification Reference | Guidance Reference | Procedure Step |
|------------------|---------|----------------------|---------------|------------------------|-------------------|----------------|
| **Load Calculations** | Size transformers, switchgear, MCCs, feeders; determine demand load | IEEE Std 141 Chapter 4, CEC demand factors | Spreadsheet or ETAP/SKM | FR-1 (Specification.md) | Principle 1 (Guidance.md) | Step 2 (Procedure.md) |
| **Short Circuit Analysis** | Determine available fault current at each bus; size circuit breakers and equipment | IEEE Std 141 Chapter 4, ANSI/IEEE C37 series | ETAP/SKM PowerTools | FR-2 (Specification.md) | Principle 2 (Guidance.md) | Step 3 (Procedure.md) |
| **Protection Coordination Study** | Coordinate protective device settings for selective operation | IEEE Std 242, IEEE Std 141 Chapter 5 | ETAP/SKM PowerTools | FR-3 (Specification.md) | Principle 3 (Guidance.md) | Step 4 (Procedure.md) |
| **Voltage Drop Analysis** | Verify cable sizing meets voltage drop limits (3% feeders, 5% total) | CEC Section 8, IEEE Std 141 Chapter 4 | Spreadsheet or ETAP/SKM | FR-4 (Specification.md) | Principle 4 (Guidance.md) | Step 5 (Procedure.md) |
| **Grounding Grid Design** | Design grounding grid to limit step/touch potentials | IEEE Std 80 | ETAP/SKM or specialized grounding software | FR-5 (Specification.md) | Consideration 7 (Guidance.md) | Step 6 (Procedure.md) |
| **Arc Flash Hazard Analysis** (Optional) | Determine incident energy and arc flash boundaries | CSA Z462, IEEE Std 1584 | ETAP/SKM PowerTools | FR-6 (Specification.md) | Consideration 8 (Guidance.md) | Step 7 (Procedure.md) |

**Note**: Arc flash hazard analysis may be included in this deliverable or performed as a separate study — **TBD** (per Employer's Requirements and project scope).

## Conditions

**Design Basis and Context:**

This calculation package provides the engineering basis and sizing/verification calculations for electrical power distribution per Employer's Requirements.

**Project Context** (Source: Decomposition Section 1):
- **Location**: Fraser Surrey Terminal, 11060 Elevator Road, Surrey, BC
- **Facility Type**: Canola oil transload (rail-to-storage-to-ship)
- **Throughput**: 1,000,000 MT per annum (OBJ-2)
- **Key Electrical Loads**:
  - **Railcar Unloading**: 32 railcar positions with unloading pumps, valves, heating
  - **Transfer Pumps**: Multiple large centrifugal pumps for product transfer between tanks and loading system
  - **Marine Loading Pumps**: High-capacity pumps for ship loading via loading arms
  - **Storage Tank Heating**: Circulation pumps and immersion heaters to maintain product temperature
  - **Process Control & Instrumentation**: Control systems, instrumentation, UPS loads
  - **Lighting**: Interior and exterior LED lighting (PKG-18)
  - **HVAC**: Building heating, ventilation, air conditioning
  - **Miscellaneous**: Receptacles, small tools, maintenance equipment

**Electrical System Parameters**:
- **Utility Service**: **TBD** — BC Hydro service voltage (anticipated: 25 kV or 13.8 kV class) and available fault current
- **Distribution Voltage Levels**: MV (25 kV or 13.8 kV), LV (600V for large motors, 480V for process loads, 208V-120V for lighting/small loads)
- **Load Diversity**: Industrial facility with continuous operation but not all loads operate simultaneously — demand factors applied

**Environmental and Operating Conditions**:
- **Ambient Temperature**: **ASSUMPTION**: -20°C to +40°C (coastal BC climate, CSA Climate Zone 2)
- **Operating Hours**: Continuous operation (24/7) — 8760 hours/year
- **Load Factor**: **TBD** — Average load as percentage of peak load (typical industrial: 0.6-0.8)
- **Power Factor**: **ASSUMPTION**: 0.85-0.95 lagging (industrial motor loads); power factor correction may be required
- **Voltage Regulation**: ±5% at point of utilization (per utility requirements and good practice)

**Design Criteria and Assumptions**:
- **Design Life**: 25+ years minimum (per facility operational life expectancy)
- **Future Expansion**: Phase 2 expansion planned (OBJ-8) — calculations shall consider spare capacity (20-25% typical)
- **Reliability**: High reliability required for continuous commercial operation (OBJ-1)
- **Safety**: Calculations support safe design per CEC, CSA Z462, and IEEE standards

## Construction

**Calculation Methodology and Content:**

Anticipated calculation artifacts (Source: _CONTEXT.md and Decomposition DEL-17.03 entry):

### 1. Load Calculations

**Purpose**: Determine connected load, demand load, and transformer/switchgear sizing.

**Methodology** (per IEEE Std 141 Chapter 4):
1. **Connected Load Compilation**: Sum nameplate ratings of all electrical equipment (motors, lighting, HVAC, process loads)
2. **Demand Factor Application**: Apply demand factors to account for non-simultaneous operation (CEC Table 14, IEEE Std 141 Chapter 4)
3. **Load Categories**: Organize loads by voltage level (600V, 480V, 208V-120V) and distribution point (MCC, panel, substation)
4. **Transformer Sizing**: Size transformers based on demand load plus future expansion allowance (typically 20-25% spare capacity)
5. **Power Factor**: Assume motor loads at 0.85-0.90 PF lagging; lighting at 0.95-1.0 PF
6. **Spare Capacity**: Include allowance for future loads (Phase 2 expansion per OBJ-8)

**Typical Load Categories**:
- **Large Motors (>50 HP)**: Pumps (transfer, marine loading, heating circulation) — 600V or 480V
- **Medium Motors (10-50 HP)**: Process equipment, HVAC fans, smaller pumps — 480V
- **Small Motors (<10 HP)**: Mixers, agitators, utility equipment — 480V or 208V
- **Lighting**: LED interior/exterior lighting — 208V-120V (PKG-18 coordination)
- **Receptacles and Small Power**: Tools, maintenance, offices — 120V
- **Control Systems**: Instrumentation power, UPS loads — 120V (PKG-19 coordination)
- **HVAC**: Packaged units, split systems, exhaust fans — 208V or 480V
- **Tank Heating**: Immersion heaters, circulation pumps — 600V or 480V

**Output**:
- Connected load summary (kW, kVA) by voltage level and distribution point
- Demand load calculation with demand factors applied
- Transformer sizing summary (kVA ratings for unit substations and lighting transformers)
- Switchgear and MCC bus sizing (continuous current ratings)

### 2. Short Circuit Analysis

**Purpose**: Determine available fault current at each electrical bus to size circuit breakers, switchgear, and protective devices.

**Methodology** (per IEEE Std 141 Chapter 4, ANSI/IEEE C37 series):
1. **Utility Fault Current**: Obtain available fault current at utility service point from BC Hydro — **TBD** (typical: 25-50 kA for 25 kV service, 40-60 kA for 13.8 kV service)
2. **System Modeling**: Model electrical distribution system in ETAP or SKM PowerTools (utility source, transformers, cables, switchgear, MCCs, motors)
3. **Fault Calculations**: Calculate three-phase and single-line-to-ground fault currents at each bus
4. **Motor Contribution**: Include motor contribution to fault current (typically 4-6 times motor FLA for first few cycles)
5. **X/R Ratio**: Calculate X/R ratio at each bus (affects asymmetrical fault current and DC component)
6. **Equipment Ratings**: Compare calculated fault current against equipment interrupting capacity (AIC or kA rating)

**Output**:
- Fault current summary table (three-phase and line-to-ground fault current in kA RMS symmetrical at each bus)
- X/R ratios
- Equipment short circuit current rating (SCCR) verification
- Protective device interrupting capacity verification

**Typical Fault Current Levels** (ASSUMPTION):
- **MV Switchgear Bus**: 25-40 kA (25 kV system) or 40-63 kA (13.8 kV system) — based on utility source
- **LV Switchgear Bus (Transformer Secondary)**: 30-65 kA depending on transformer size and impedance
- **MCC Bus**: 15-35 kA depending on distance from transformer and cable impedance
- **Load Centers and Panels**: 5-15 kA depending on distance from source

### 3. Protection Coordination Study

**Purpose**: Coordinate protective device settings (circuit breakers, fuses, relays) to ensure selective operation (only faulted circuit is isolated).

**Methodology** (per IEEE Std 242, IEEE Std 141 Chapter 5):
1. **Device Inventory**: Identify all protective devices (utility breaker, MV breaker/relays, LV breaker trip units, MCC motor starters, fuses)
2. **Time-Current Curve (TCC) Plotting**: Plot device characteristics on log-log graph (current vs. time)
3. **Coordination Criteria**: Ensure upstream device operates slower than downstream device by minimum coordination interval (typically 0.2-0.3 seconds for circuit breakers, 0.1 seconds for fuses)
4. **Relay Settings**: Determine relay pickup, time delay, and instantaneous settings for microprocessor relays
5. **Motor Starting**: Verify protective devices do not trip on motor inrush (typically 6 times FLA for 6-10 seconds)
6. **Coordination Verification**: Verify coordination for full range of fault currents (minimum to maximum)

**Output**:
- Time-current coordination curves (TCC plots)
- Relay settings table (pickup, time delay, instantaneous settings for each protective relay)
- Circuit breaker trip unit settings (LSIG settings for electronic trip units)
- Coordination intervals verification
- Motor starting verification

**Coordination Sequence** (typical):
1. **Utility Protective Devices** (BC Hydro reclosers, relays)
2. **MV Switchgear Main Breaker** (incoming service breaker with relay)
3. **MV Feeder Breakers** (transformer primary breakers with relays)
4. **LV Switchgear Main Breaker** (transformer secondary main)
5. **LV Feeder Breakers** (MCC feeders, large load feeders)
6. **MCC Branch Circuit Devices** (motor starters, MCCBs)
7. **Final Branch Devices** (small breakers, fuses)

### 4. Voltage Drop Analysis

**Purpose**: Verify cable sizing provides acceptable voltage drop (maximum 3% for feeders, 5% total per IEEE recommendations).

**Methodology** (per CEC Section 8, IEEE Std 141 Chapter 4):
1. **Cable Data**: Cable size, length, conductor material (copper), installation method (conduit, tray, direct burial)
2. **Load Current**: Calculate load current for each feeder (from load calculations)
3. **Voltage Drop Calculation**: VD = √3 × I × (R cosθ + X sinθ) × L for three-phase circuits; VD = 2 × I × R × L for single-phase circuits
4. **Cumulative Voltage Drop**: Calculate total voltage drop from source to load (feeder + branch circuit)
5. **Verification**: Verify voltage drop ≤ 3% for feeders, ≤ 5% total
6. **Cable Upsizing**: Increase cable size if voltage drop exceeds limits

**Output**:
- Voltage drop summary table (cable circuit, length, current, voltage drop %, cumulative voltage drop %)
- Cable sizing verification (ampacity per CEC, voltage drop per IEEE)
- Recommended cable sizes for each circuit

**Voltage Drop Limits**:
- **Feeders**: 3% maximum (IEEE Std 141 recommendation; CEC permits 5%)
- **Branch Circuits**: 2% maximum (to achieve 5% total)
- **Total (Feeder + Branch)**: 5% maximum

### 5. Grounding Grid Design (Optional/Included)

**Purpose**: Design facility grounding grid to limit step and touch potentials during ground fault conditions (personnel safety).

**Methodology** (per IEEE Std 80):
1. **Soil Resistivity**: Obtain soil resistivity measurements (Ω-m) — **TBD** (field testing required)
2. **Grid Design**: Design grounding grid layout (grid conductors, ground rods, spacing)
3. **Grid Resistance**: Calculate grounding grid resistance (target: < 5 ohms typical)
4. **Fault Current**: Maximum ground fault current (from short circuit analysis)
5. **Step and Touch Potential**: Calculate step and touch potentials during fault
6. **Safety Verification**: Verify potentials below safe limits per IEEE Std 80 (based on fault duration and soil resistivity)

**Output**:
- Grounding grid design (conductor size, spacing, ground rod locations)
- Grid resistance calculation
- Step and touch potential analysis
- Safety verification

**Typical Grounding Grid Design** (ASSUMPTION):
- Grid conductor: Bare copper 2/0 AWG or 4/0 AWG
- Grid spacing: 10-20 m
- Ground rods: 16 mm × 3 m copper-clad steel at grid intersections
- Target grid resistance: < 5 ohms

### 6. Arc Flash Hazard Analysis (Optional)

**Purpose**: Determine arc flash incident energy levels and arc flash boundaries for personnel safety labeling (CSA Z462 requirement).

**Methodology** (per IEEE Std 1584, CSA Z462):
1. **Incident Energy Calculation**: Calculate arc flash incident energy (cal/cm²) at each electrical equipment location based on available fault current, protective device clearing time, and working distance
2. **Arc Flash Boundary**: Determine distance at which incident energy = 1.2 cal/cm² (onset of second-degree burn)
3. **PPE Category**: Determine required personal protective equipment (PPE) category (0-4 per CSA Z462)
4. **Equipment Labeling**: Prepare arc flash labels for each electrical equipment

**Output**:
- Arc flash incident energy summary (cal/cm² at each bus)
- Arc flash boundary distances
- PPE category assignments
- Arc flash label content for equipment

**TBD**: Confirm if arc flash analysis is included in this deliverable or performed separately.

## References

**Primary References**:
- **Decomposition Document**: /Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md (Section 4 — PKG-17, DEL-17.03 entry)
- **_CONTEXT.md**: Deliverable identity and anticipated calculation artifacts
- **Employer's Requirements**: **TBD** — Volume 2 Parts 1-3 (electrical design criteria, load data) — **location TBD**

**Applicable Standards** (Calculation Methodologies):

**Load Calculations**:
- IEEE Std 141 (Red Book) — Chapter 4: Load Characteristics and Diversity Factors
- CEC Table 14 — Demand Factors for Services and Feeders

**Short Circuit Analysis**:
- IEEE Std 141 (Red Book) — Chapter 4: Short Circuit Calculations
- ANSI/IEEE C37 series — Circuit Breaker Ratings and Application

**Protection Coordination**:
- IEEE Std 242 (Buff Book) — Protection and Coordination of Industrial and Commercial Power Systems
- IEEE Std 141 (Red Book) — Chapter 5: Protection

**Voltage Drop**:
- CEC Section 8 — Circuit Loading and Demand Factors
- IEEE Std 141 (Red Book) — Chapter 4: Voltage Drop Calculations

**Grounding**:
- IEEE Std 80 — Guide for Safety in AC Substation Grounding

**Arc Flash**:
- CSA Z462 — Workplace Electrical Safety
- IEEE Std 1584 — Guide for Performing Arc Flash Hazard Calculations

**Software References**:
- ETAP (Electrical Transient Analyzer Program) or SKM PowerTools — electrical analysis software for load flow, short circuit, protection coordination, arc flash

**Additional References**:
- BC Hydro service information — utility fault current, protection requirements — **TBD**
- Equipment manufacturer data — transformer impedances, motor data, cable impedances
- See DEL-17.01 (Electrical Power Design Drawing Set) for single line diagrams, equipment list, cable schedules
- See DEL-17.02 (Electrical Power Technical Specification) for equipment performance requirements
- See DEL-17.04 (Electrical Power Data Sheet Package) for equipment nameplate data

**Cross-references**:
- Dependencies coordinated externally (per _DEPENDENCIES.md — NOT_TRACKED mode)
- Interface with PKG-15 (Pumps and Rotating Equipment) for motor nameplate data
- Interface with PKG-18 (Lighting) for lighting load data
- Interface with PKG-19 (Control & Instrumentation) for control system and UPS load data
