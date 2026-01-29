# Datasheet: DEL-17.05 Electrical Power Installation & Test Records

## Identification

| Field | Value |
|-------|-------|
| Deliverable ID | DEL-17.05 |
| Name | Electrical Power Installation & Test Records |
| Package | PKG-17 Electrical Power Distribution |
| Discipline | Electrical |
| Type | Record |
| Responsible | D&B Contractor (QA/QC) |
| Status | INITIALIZED |

## Attributes

| Attribute | Value |
|-----------|-------|
| Record Package Contents | FAT records, insulation test records, protection relay test records (Source: _CONTEXT.md) |
| Number of Test Records | **TBD** — Based on installed equipment (anticipated: 2-3 transformers FATs, 1-2 switchgear FATs, 4-8 MCC FATs, field insulation tests per equipment, relay tests per protective device) |
| Retention Period | Permanent (life of facility) — required for regulatory compliance, warranty, future modifications |
| Revision | 0 (Initial issue as-built records) |
| Classification | Project Record / As-Built |

### Test Record Types and Purposes

| Test Record Type | Equipment/System Tested | Purpose | Test Standard |
|------------------|-------------------------|---------|---------------|
| **Factory Acceptance Test (FAT) Records** | Transformers, switchgear, MCCs (major equipment) | Verify equipment performance at factory before shipment | CSA C88/C802, C22.2 No. 31/254, IEEE C57/C37 |
| **Insulation Resistance (Megger) Test Records** | All electrical equipment and cables | Verify insulation integrity before energization | CEC, IEEE Std 43 |
| **High-Potential (Hi-Pot) Test Records** | MV cables, MV equipment | Verify dielectric strength of insulation | CEC, IEEE Std 400 |
| **Protection Relay Test Records** | MV switchgear protective relays, LV trip units | Verify relay operation and settings per coordination study | IEEE C37.90, manufacturer procedures |
| **Circuit Breaker Operation Test Records** | MV and LV circuit breakers | Verify mechanical and electrical operation | IEEE C37.09, C37.50 |
| **Ground Resistance Test Records** | Grounding grid, ground rods | Verify grounding system resistance meets design (< 5 ohms typical) | IEEE Std 81 |
| **Load Test/Energization Records** | Distribution system (transformers, feeders, MCCs) | Verify system operates under load, voltage regulation acceptable | Project commissioning procedures |
| **Commissioning Test Summary** | Complete electrical distribution system | Overall system acceptance and turnover | Project commissioning plan |

**Source**: _CONTEXT.md (anticipated artifacts); typical electrical commissioning test requirements per CEC, IEEE, CSA standards.

## Conditions

**Testing Context and Requirements:**

This record package provides evidence of completion, inspection, and testing for electrical power distribution per Employer's Requirements, CEC, and IEEE standards.

**Project Context** (Source: Decomposition Section 1):
- **Location**: Fraser Surrey Terminal, 11060 Elevator Road, Surrey, BC
- **Facility Type**: Canola oil transload (continuous industrial operation)
- **Key Equipment to be Tested**: Transformers (unit substations, dry-type), MV switchgear, LV switchgear, MCCs (4-8 lineups), power cables (MV and LV), grounding system, protective relays

**Testing Objectives**:
- **Safety**: Verify electrical installations meet CEC safety requirements for personnel and equipment protection (OBJ-1)
- **Regulatory Compliance**: Satisfy BC Safety Authority inspection and permit closeout requirements (OBJ-6)
- **Performance Verification**: Confirm equipment operates per specifications and design calculations (OBJ-1, OBJ-2)
- **Warranty Baseline**: Establish equipment performance baseline for warranty claims and future troubleshooting

**Test Conditions**:
- **Factory Tests (FAT)**: Performed at manufacturer facility under controlled conditions per applicable standards
- **Field Tests**: Performed at installation site; ambient conditions may affect test results (temperature, humidity corrections applied where applicable)
- **Acceptance Criteria**: Per specifications (DEL-17.02), manufacturer recommendations, and applicable test standards (CEC, IEEE, CSA)

## Construction

**Test Record Content by Type:**

### 1. Factory Acceptance Test (FAT) Records

**Transformers** (CSA C88 / C802 routine tests):
- **Resistance Measurement**: Winding resistance (DC) to verify connections and detect winding faults
- **Polarity Test**: Verify transformer polarity and phase relationships correct
- **Voltage Ratio Test**: Verify turns ratio matches nameplate for all tap positions
- **No-Load Loss Test**: Measure core losses (excitation current and power at rated voltage, no load)
- **Impedance / Load Loss Test**: Measure transformer impedance (%) and winding losses at rated current
- **Applied Voltage (Dielectric) Test**: Apply test voltage to windings to verify insulation strength (per CSA C88/C802)
- **Induced Voltage Test**: Overvoltage test at increased frequency to verify inter-turn insulation
- **Test Results**: Pass/Fail for each test; deviations from standards noted; test engineer signature and date

**Switchgear** (CSA C22.2 No. 31 / IEEE C37 tests):
- **High-Potential (Dielectric) Test**: Apply test voltage to buses, breakers, and compartments to verify insulation (per CSA C22.2 No. 31)
- **Primary Current Injection Test**: Inject test current through circuit to verify protection relay operation and current transformer (CT) accuracy
- **Protective Relay Functional Test**: Verify relay settings, pickup, timing, and trip functions per manufacturer procedures
- **Control Circuit Functional Test**: Verify breaker control (open/close), interlocks, and indication lights operate correctly
- **Mechanical Operation Test**: Operate breakers multiple times to verify mechanical integrity and smooth operation
- **Insulation Resistance Test**: Megger test of insulation (min 1000 MΩ typical for MV equipment)

**Motor Control Centers (MCCs)** (CSA C22.2 No. 254 tests):
- **High-Potential (Dielectric) Test**: Apply test voltage to buses and starters
- **Control Circuit Functional Test**: Verify motor starter operation (start/stop), overload operation, control interlocks
- **Mechanical Operation Test**: Cycle contactors and disconnect switches
- **Insulation Resistance Test**: Megger test of bus and starter insulation

**FAT Record Format**:
- Test report header: Equipment tag, manufacturer, model, serial number, test date, test location, test engineer
- Test procedures: Standards followed, test equipment used, test setup
- Test results: Table of tests performed, acceptance criteria, actual results, pass/fail
- Test certificates: Signatures (manufacturer test engineer, witness if applicable)
- Photographs: Equipment under test (if applicable)

### 2. Insulation Resistance (Megger) Test Records

**Purpose**: Verify insulation integrity of equipment and cables before energization (detect moisture, contamination, damage)

**Equipment Tested**:
- Transformers (winding-to-winding, winding-to-ground)
- Switchgear and MCC (bus-to-ground, circuit-to-ground)
- Power cables (conductor-to-ground, conductor-to-conductor)
- Motors (winding-to-ground) — coordinated with PKG-15

**Test Method** (per IEEE Std 43):
- Apply DC test voltage (500V or 1000V for equipment up to 1 kV; 1000V or 2500V for MV equipment)
- Measure insulation resistance in MegaOhms (MΩ)
- Apply temperature correction if ambient temperature significantly different from standard (40°C)

**Acceptance Criteria**:
- **New Equipment**: Minimum insulation resistance per IEEE Std 43 (typically > 1000 MΩ for new MV equipment; > 100 MΩ for LV equipment)
- **Cables**: Minimum per manufacturer and IEEE Std 400 (varies by voltage and cable length)
- **Pass**: Insulation resistance ≥ minimum; **Fail**: Insulation resistance < minimum (investigate cause — moisture, contamination, damage)

**Test Record Format**:
- Equipment/cable identification (tag number, circuit ID)
- Test voltage applied, test duration
- Insulation resistance measured (MΩ), temperature at time of test
- Acceptance criteria, pass/fail
- Test equipment used (Megger make/model, calibration date)
- Tester signature and date

### 3. High-Potential (Hi-Pot) Test Records

**Purpose**: Verify dielectric strength of MV cable and equipment insulation (more severe test than Megger; applies higher voltage)

**Equipment Tested**:
- MV power cables (after installation, before energization)
- MV switchgear and transformers (if not already tested at factory)

**Test Method** (per IEEE Std 400, CEC Section 12):
- Apply AC or DC test voltage significantly above operating voltage (per IEEE Std 400 recommendations)
- Typical: 60-80% of factory test voltage for cables (to avoid over-stressing insulation in field)
- Hold voltage for specified duration (1-5 minutes typical)
- Monitor leakage current (excessive leakage indicates insulation weakness)

**Acceptance Criteria**:
- No flashover or breakdown during test
- Leakage current within acceptable limits (per IEEE Std 400 and manufacturer guidance)
- **Pass**: Withstands test voltage for specified duration; **Fail**: Flashover, breakdown, or excessive leakage (investigate and repair)

**Test Record Format**:
- Cable/equipment identification (circuit ID, tag number)
- Test voltage applied, test duration
- Leakage current measured
- Pass/fail
- Test equipment used (Hi-Pot tester make/model, calibration date)
- Tester signature and date

### 4. Protection Relay Test Records

**Purpose**: Verify protective relay operation and settings match protection coordination study (DEL-17.03)

**Relays Tested**:
- MV switchgear protective relays (microprocessor-based: 50/51, 50/51G, 27/59, etc.)
- LV switchgear and MCC electronic trip units (LSIG settings)

**Test Method** (per IEEE C37.90, manufacturer procedures):
- **Primary Injection Test**: Inject test current through CT primary circuit; verify relay pickup and timing at multiple current levels
- **Secondary Injection Test**: Inject test current directly into relay; verify relay pickup, timing, and instantaneous functions
- **Settings Verification**: Verify relay settings match coordination study (pickup current, time dial, instantaneous setpoint)
- **Functional Test**: Verify relay operates correctly and trips breaker

**Test Record Format**:
- Relay identification (tag number, relay type/model, function — e.g., 50/51)
- Settings (per coordination study): Pickup, time dial, instantaneous
- Test results: Pickup current measured, trip time measured at multiple test currents (compare to expected per TCC)
- Pass/fail (pickup and timing within tolerance — typically ±5% for pickup, ±10% for timing)
- Test equipment used (relay test set make/model, calibration date)
- Tester signature and date

### 5. Circuit Breaker Operation Test Records

**Purpose**: Verify circuit breaker mechanical and electrical operation

**Breakers Tested**: MV circuit breakers (VCBs), LV circuit breakers (ICCBs, MCCBs, LVPCBs)

**Test Method** (per IEEE C37.09, C37.50):
- **Mechanical Operation**: Operate breaker (open/close) multiple times; verify smooth operation, no binding
- **Timing Test**: Measure breaker operating time (close time, open time, contact travel time) — compare to manufacturer specifications
- **Contact Resistance Test**: Measure resistance across closed contacts (low resistance indicates good contact; high resistance indicates contact wear/burning)

**Test Record Format**:
- Breaker identification (tag number, location, breaker type/rating)
- Operating time measured (close time, open time)
- Contact resistance measured
- Pass/fail (operation smooth, timing within spec, resistance acceptable)
- Tester signature and date

### 6. Ground Resistance Test Records

**Purpose**: Verify facility grounding system resistance meets design target (< 5 ohms typical)

**Test Method** (per IEEE Std 81):
- **Fall-of-Potential Method**: Most common; uses test instrument with current and potential electrodes driven into ground at specified distances
- Measure ground grid resistance (ohms)

**Acceptance Criteria**:
- Ground resistance ≤ design target (< 5 ohms typical; lower is better)
- **Pass**: Resistance meets target; **Fail**: Resistance exceeds target (may require additional ground rods or grid enhancement)

**Test Record Format**:
- Grounding system identification (main grounding grid, equipment ground, etc.)
- Ground resistance measured (ohms)
- Acceptance criteria, pass/fail
- Test equipment used (ground resistance tester make/model, calibration date)
- Test date, weather conditions (soil moisture affects resistance), tester signature

### 7. Load Test / Energization Records

**Purpose**: Verify electrical distribution system operates correctly under actual load conditions

**Test Activities**:
- **Initial Energization**: Energize transformers, switchgear, and feeders in sequence; verify no faults, alarms, or abnormal conditions
- **No-Load Voltage Verification**: Measure voltage at each distribution level with no load; verify within tolerance (±5% typical)
- **Load Test**: Energize loads incrementally (MCCs, motors, lighting); measure voltage and current at each step; verify voltage regulation acceptable (voltage drop < 5% at full load)
- **Load Balance**: Verify three-phase load balance (current imbalance < 10% desirable)

**Test Record Format**:
- System/circuit tested (transformer, switchgear, MCC, feeder)
- Voltage measured (no-load and full-load), current measured
- Load applied (description, kW/kVA)
- Voltage regulation (voltage drop %), pass/fail
- Tester signature and date

### 8. Commissioning Test Summary

**Purpose**: Overall system acceptance and turnover documentation

**Content**:
- List of all tests performed (FAT, field tests, functional tests)
- Test results summary (pass/fail for each system/equipment)
- Deficiencies identified and resolved (punch list items)
- System acceptance sign-off (contractor, engineer, Employer, BC Safety Authority inspector if required)
- Turnover date and documentation (as-built drawings, O&M manuals, test records)

## References

**Primary References**:
- **Decomposition Document**: /Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md (Section 4 — PKG-17, DEL-17.05 entry)
- **_CONTEXT.md**: Deliverable identity and anticipated test record artifacts
- **Employer's Requirements**: **TBD** — Volume 2 Parts 1-3 (testing and commissioning requirements) — **location TBD**

**Test Standards**:
- **CEC (CSA C22.1)**: General installation and testing requirements
- **CSA C88, C802**: Transformer factory tests
- **CSA C22.2 No. 31, No. 254**: Switchgear and MCC factory tests
- **IEEE C37.09, C37.50**: Circuit breaker testing
- **IEEE C37.90**: Protective relay testing
- **IEEE Std 43**: Insulation resistance testing (rotating machinery — applicable to equipment)
- **IEEE Std 81**: Ground resistance testing
- **IEEE Std 400**: MV cable testing (Hi-Pot, insulation)

**Supporting Deliverables**:
- **DEL-17.01** (Electrical Power Design Drawing Set): Equipment to be tested per drawings and schedules
- **DEL-17.02** (Electrical Power Technical Specification): Test requirements and acceptance criteria per specifications
- **DEL-17.03** (Electrical Power Design Calculations): Protection coordination settings for relay tests
- **DEL-17.04** (Electrical Power Data Sheet Package): FAT records from manufacturer (included in this deliverable)

**Cross-references**:
- Dependencies coordinated externally (per _DEPENDENCIES.md — NOT_TRACKED mode)
- Interface with PKG-15 (Pumps and Rotating Equipment) for motor testing
- BC Safety Authority: Test records required for electrical permit inspection and closeout
