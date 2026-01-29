# Procedure: DEL-17.05 Electrical Power Installation & Test Records

## Purpose

This procedure defines the process for producing and managing **Electrical Power Installation & Test Records** within **PKG-17 Electrical Power Distribution**.

**Deliverable Purpose**: Provides evidence of completion, inspection, and testing for electrical power.

**Deliverable Type**: Record
**Responsible Party**: D&B Contractor (QA/QC)
**Discipline**: Electrical

## Prerequisites

**Dependencies** (NOT_TRACKED): Equipment installed per drawings (DEL-17.01) and specifications (DEL-17.02); FAT records received from manufacturers

**Reference Materials**: Test standards (CEC, IEEE, CSA), equipment manuals, protection coordination study (DEL-17.03), commissioning plan

**Personnel**: Qualified electrical technicians/engineers (test performers), relay technicians (for relay testing), P.Eng. (test record review and approval), BC Safety Authority inspector (for inspection witness)

## Steps

### Step 1: Factory Acceptance Test (FAT) Coordination
- Schedule FAT at manufacturer facilities (transformers, switchgear, MCCs)
- Determine if Owner or engineer will witness FAT (optional)
- Receive FAT reports from manufacturers (part of equipment submittal — DEL-17.04)
- Review FAT reports for compliance with specifications; flag any test failures or deviations

### Step 2: Pre-Energization Field Testing

**Step 2a: Visual Inspection**
- Inspect installed equipment: Verify equipment installed per drawings, verify proper clearances (CEC Section 2), verify grounding connections, verify labels/nameplates
- Document inspection results (checklist or inspection report)

**Step 2b: Insulation Resistance (Megger) Tests**
- Perform Megger tests on all equipment and cables before energization
- Test voltage: 500-1000V for LV equipment/cables; 1000-2500V for MV equipment/cables (per equipment manual)
- Measure and record insulation resistance (MΩ)
- Compare to acceptance criteria (IEEE Std 43); flag failures for investigation
- Document test results (test forms with equipment ID, test voltage, resistance measured, pass/fail)

**Step 2c: High-Potential (Hi-Pot) Tests**
- Perform Hi-Pot tests on MV cables and equipment (per IEEE Std 400)
- Test voltage: 60-80% of factory test voltage (consult IEEE Std 400 and equipment manual)
- Apply voltage for specified duration (1-5 minutes); monitor leakage current
- Pass = No flashover/breakdown; Fail = Flashover or excessive leakage
- Document test results (test forms with equipment/cable ID, test voltage, leakage current, pass/fail)

**Step 2d: Ground Resistance Test**
- Perform ground resistance test on facility grounding grid (per IEEE Std 81)
- Measure ground resistance (ohms) using fall-of-potential method
- Compare to design target (< 5 ohms typical)
- Document test results (test form with resistance measured, pass/fail)

### Step 3: Protection Relay and Circuit Breaker Testing

**Step 3a: Protection Relay Testing**
- Perform relay tests on MV switchgear protective relays and LV trip units
- Verify relay settings match protection coordination study (DEL-17.03)
- Perform pickup and timing tests using relay test set (primary or secondary injection)
- Verify relay operates correctly and trips breaker
- Document test results (test forms with relay ID, settings, pickup/timing measured, pass/fail)

**Step 3b: Circuit Breaker Operation Testing**
- Perform breaker operation tests (mechanical operation, timing, contact resistance)
- Verify breaker operates smoothly (no binding or unusual noise)
- Measure breaker operating time and contact resistance
- Compare to manufacturer specifications
- Document test results (test forms with breaker ID, operation observed, timing/resistance measured, pass/fail)

### Step 4: System Energization and Load Testing

**Step 4a: Initial Energization (No Load)**
- Coordinate with BC Safety Authority for rough-in inspection (before energization) — **TBD**
- Energize transformers, switchgear, and feeders in sequence (follow energization plan)
- Monitor for faults, alarms, or abnormal conditions (unusual noise, overheating)
- Measure no-load voltages at each distribution level; verify within tolerance (±5%)
- Document energization results (energization checklist, voltage measurements)

**Step 4b: Load Testing**
- Energize loads incrementally (MCCs, motors, lighting)
- Measure voltage and current at each step
- Verify voltage regulation acceptable (voltage drop < 5% at full load)
- Verify three-phase load balance (current imbalance < 10%)
- Document load test results (load test forms with voltages/currents measured, load applied)

### Step 5: Test Record Compilation and Review

**Step 5a: Compile Test Records**
- Collect all test records (FAT, Megger, Hi-Pot, relay tests, breaker tests, ground resistance, load tests)
- Organize records by equipment type or system
- Create test record package with table of contents and equipment index

**Step 5b: Test Record Review**
- Review test records for completeness (all required tests performed and documented)
- Verify all test results meet acceptance criteria (all tests PASS)
- Verify test equipment calibration valid
- Verify test records signed by test performers
- Flag any incomplete or failed tests for resolution

**Step 5c: Test Record Approval**
- Electrical engineer (P.Eng.) reviews and approves test record package
- Sign/seal commissioning test summary (overall system acceptance)

### Step 6: Final Inspection and System Turnover

**Step 6a: BC Safety Authority Final Inspection**
- Coordinate with BC Safety Authority for final electrical inspection
- Inspector reviews test records and performs site inspection
- Inspector approves electrical installation (permit closeout)

**Step 6b: System Turnover to Owner**
- Prepare turnover documentation package: As-built drawings (DEL-17.01 as-built), specifications (DEL-17.02), calculations (DEL-17.03), data sheets (DEL-17.04), test records (DEL-17.05), O&M manuals
- Conduct turnover meeting with Owner (system walkthrough, documentation review)
- Obtain Owner acceptance sign-off
- Deliver turnover documentation package to Owner

### Step 7: As-Built Test Record Retention

- File final test records in 3_Issued/ folder (as-built designation)
- Retain test records permanently (life of facility) per project record retention requirements
- Provide copies to Owner for operations and maintenance use

## Verification

**Verification Activities**:
- Visual inspection before energization
- Pre-energization insulation tests (Megger, Hi-Pot)
- Protection relay and breaker functional tests
- Load tests and voltage regulation verification
- Test record completeness review
- BC Safety Authority inspection

**Sign-Off Requirements**:
- Test performers sign test records
- Electrical engineer (P.Eng.) approves test record package and commissioning summary
- BC Safety Authority inspector approves final electrical installation
- Owner signs turnover acceptance

## Records

**Documentation Outputs** (Source: _CONTEXT.md):
- FAT records (transformers, switchgear, MCCs)
- Insulation resistance test records (Megger)
- High-potential test records (Hi-Pot)
- Protection relay test records
- Circuit breaker operation test records
- Ground resistance test records
- Load test / energization records
- Commissioning test summary

**Record Management**:
- Test records compiled in 2_Checking/ during testing and review
- Approved test records filed in 3_Issued/ (as-built designation) upon system turnover
- Permanent retention (life of facility)
- Copies delivered to Owner

**Interfaces**:
- DEL-17.02 (Specifications): Test requirements and acceptance criteria
- DEL-17.03 (Calculations): Relay settings for testing
- DEL-17.04 (Data Sheets): FAT records from manufacturers
- BC Safety Authority: Inspection and permit closeout
