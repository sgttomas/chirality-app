# Guidance: DEL-29.01 Test Procedures

## Purpose

This guidance document supports the development of **Test Procedures** for **PKG-29 Testing**.

**Deliverable Purpose:** Defines the execution method and controls for test to meet safety, quality, and operational requirements. **Source:** Decomposition line 646

**Deliverable Classification:**
- Type: Procedure
- Discipline: T&C (Testing & Commissioning)
- Responsible Party: D&B Contractor (QA/QC)

**Source:** _CONTEXT.md

## Principles

### Engineering Rationale for Test Procedures

**Testing Philosophy:**

Test procedures serve multiple critical functions in EPC project execution:

1. **Safety Assurance:** Systematic verification that equipment and systems can be operated safely without risk to personnel, property, or environment

2. **Quality Verification:** Confirmation that installed work complies with design requirements, codes, and specifications

3. **Functional Demonstration:** Proof that systems perform as intended under specified conditions

4. **Documentation of Conformance:** Creation of objective evidence for regulatory compliance, insurance, and asset lifecycle management

5. **Risk Mitigation:** Early identification of defects, non-conformances, or design issues prior to commissioning and operation

**Source:** General testing and commissioning principles per IEC 62382, ASME B31.3, API 650 **ASSUMPTION**

### Discipline-Specific Principles

**Hydrostatic Testing Principles:**
- Hydrostatic testing verifies pressure boundary integrity before introduction of hazardous materials
- Test pressure typically 1.25-1.5× design pressure (code-dependent) to provide margin of safety
- Test medium (water) provides visual indication of leaks without fire/toxicity hazards
- Hold duration ensures leak detection and stress relaxation
- Post-test inspection confirms no permanent deformation or damage

**Source:** ASME B31.3, API 650, CSA Z662 **location TBD**

**Electrical Testing Principles:**
- Sequential testing from component level to system level reduces risk
- De-energized testing (continuity, insulation resistance) precedes energized testing
- Protection system verification ensures safe equipment operation and fault clearing
- Grounding verification is fundamental to personnel safety

**Source:** NFPA 70, IEEE 43 **location TBD**

**I&C Testing Principles:**
- Calibration ensures measurement accuracy for process control and custody transfer
- Loop testing verifies end-to-end signal path integrity
- Functional testing demonstrates correct response to process conditions
- Safety system testing follows IEC 61511 proof test requirements for SIL achievement

**Source:** IEC 62382, IEC 61511 **location TBD**

### Project-Specific Context

**Project Objectives Alignment:**

This deliverable directly supports:
- **OBJ-1: Safe & Reliable Operation** — Testing verifies systems are safe and ready for operation
- **OBJ-10: Custody Transfer Accuracy** — Metering calibration ensures accurate product measurement

**Source:** Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md Section 6, lines 780, 789

**Facility Considerations:**
- Marine terminal environment requires attention to corrosion protection and weatherproofing
- CSD canola oil product requires clean, contamination-free systems (hydrostatic test water quality)
- High throughput capacity (1,000,000 MT/a) demands reliable equipment performance
- Large storage capacity (3 × 15,000 MT tanks) requires rigorous tank integrity verification

**Source:** Decomposition Section 1 (Project Context)

## Considerations

### Factors to Consider During Test Procedure Development

**1. Timing and Sequencing**
- Test procedures must align with construction schedule and system completion
- Some tests are prerequisites for subsequent work (e.g., piping hydrotest before insulation)
- Coordination with commissioning schedule (PKG-30) to ensure smooth handover
- Weather considerations for outdoor testing (temperature effects on hydrostatic testing) **ASSUMPTION**

**2. Resource Requirements**
- Test equipment availability and calibration status
- Personnel qualifications and certifications (pressure testers, electricians, instrument technicians)
- Test utilities (water supply, electrical power, compressed air/nitrogen)
- Test medium disposal (especially hydrostatic test water — see DEL-29.06)

**3. Safety and Environmental Hazards**
- Pressure hazards during hydrostatic testing (stored energy, sudden release)
- Electrical hazards during energization (arc flash, electrocution)
- Fall hazards when accessing elevated equipment during testing
- Confined space entry during tank inspections
- Water discharge environmental compliance (DEL-29.07, DEL-29.08)

**ASSUMPTION:** Typical EPC project testing hazards

**4. Hold and Witness Point Coordination**
- Integration with DEL-29.02 (Inspection and Test Plan With Hold/Witness Points)
- Employer witness requirements for critical tests
- Third-party inspection requirements (insurance, regulatory authorities)
- Notification and scheduling requirements for witnessed tests

**Source:** Cross-reference to DEL-29.02, Decomposition line 647

**5. Documentation and Records**
- Test data recording requirements (pressures, durations, results)
- Photographic documentation requirements
- Non-conformance reporting and resolution
- Test records that feed into DEL-29.03, DEL-29.04, DEL-29.05

**Source:** Cross-references to DEL-29.03-29.05

**6. Acceptance Criteria Definition**
- Code-mandated acceptance criteria (e.g., API 650 pressure drop limits)
- Project-specific acceptance criteria from Employer's Requirements **location TBD**
- Pass/fail criteria that are objective and measurable
- Disposition of non-conformances (repair, re-test, accept with deviation)

**7. Custody Transfer Metering Considerations**
- Enhanced accuracy requirements for fiscal metering (OBJ-10)
- Regulatory compliance for metered quantities (Weights and Measures Canada) **ASSUMPTION**
- Witness requirements for metering system calibration
- Traceability of calibration standards

**Source:** Project Objective OBJ-10, Decomposition line 789

## Trade-offs

### Competing Concerns During Test Procedure Development

**1. Conservatism vs. Practicality**

- **Trade-off:** Overly conservative test requirements may be impractical or create unnecessary risk (e.g., excessive test pressures), while insufficient rigor may fail to detect problems
- **Consideration:** Follow code-mandated test pressures and hold durations; avoid arbitrary increases unless justified by risk assessment
- **Recommendation:** Use code minimum requirements as baseline; increase rigor only where specific risks warrant it **ASSUMPTION**

**2. Comprehensive Testing vs. Schedule Pressure**

- **Trade-off:** Thorough testing takes time and may delay commissioning; rushing tests increases risk of undetected defects
- **Consideration:** Testing is not optional for code-required verification; shortcuts create liability
- **Recommendation:** Build adequate testing time into schedule; prioritize critical path testing; allow for contingency re-testing

**3. Centralized vs. Distributed Testing**

- **Trade-off:** System-level testing (e.g., entire piping system at once) is efficient but makes leak identification difficult; component-level testing is thorough but time-consuming
- **Consideration:** Balance depends on system complexity and criticality
- **Recommendation:** Test in logical boundaries that allow leak isolation while minimizing repetitive setup **ASSUMPTION**

**4. Prescriptive vs. Performance-Based Procedures**

- **Trade-off:** Highly prescriptive procedures reduce variability but may not adapt to field conditions; performance-based procedures allow flexibility but require more skilled personnel
- **Consideration:** Complexity of test and personnel competency level
- **Recommendation:** Use prescriptive step-by-step procedures for complex or hazardous tests; allow some flexibility for routine tests **ASSUMPTION**

**5. Automated vs. Manual Testing**

- **Trade-off:** Automated test sequences (especially for I&C) are repeatable and reduce human error but require setup time and software validation; manual testing is flexible but dependent on operator skill
- **Consideration:** System complexity, repeatability requirements, and available tools
- **Recommendation:** Automate repetitive tests (e.g., instrument loop checks); use manual testing where engineering judgment is needed **ASSUMPTION**

## Examples

### Reference Examples and Precedents

**1. Hydrostatic Testing Examples**

**Storage Tank Hydrostatic Test:**
- Fill tank with clean water to design capacity plus test height (API 650 Annex I)
- Hold for minimum 24 hours (typical per API 650)
- Monitor for leakage at shell seams, bottom plates, nozzles, roof penetrations
- Monitor for shell deformation or settlement
- Post-test: Drain, dry, internal inspection for water damage or coating defects
- **TBD** — Specific acceptance criteria per tank design and Employer's Requirements

**Source:** API 650 **location TBD**

**Piping Hydrostatic Test:**
- Isolate test section with blind flanges or closed valves
- Fill with water and vent air completely
- Pressurize to 1.5× design pressure (typical per ASME B31.3)
- Hold for minimum 10 minutes (B31.3) or longer per project requirements
- Inspect all joints, flanges, welds visually during hold period
- Acceptance: No visible leakage, no pressure drop exceeding code allowance
- **TBD** — Specific test sections and pressure values per piping design

**Source:** ASME B31.3 **location TBD**

**2. Electrical Testing Examples**

**Motor Insulation Resistance Test:**
- De-energize and lock out motor circuit
- Disconnect motor leads from starter
- Connect megohmmeter (typically 500V or 1000V DC)
- Measure insulation resistance between phases and to ground
- Acceptance: Typically >1 MΩ (IEEE 43 provides temperature-corrected values)
- Record results and compare to manufacturer's data and previous tests
- **TBD** — Specific acceptance criteria per equipment and project standards

**Source:** IEEE 43 **location TBD**

**Protection Relay Functional Test:**
- Use relay test set to inject simulated fault currents
- Verify relay trips at correct setpoints
- Verify correct timing (instantaneous, time-delay)
- Verify correct output contacts operate (trip circuit, alarm)
- Acceptance: Relay performance within ±5% of settings (typical) **ASSUMPTION**
- **TBD** — Specific relay settings per electrical coordination study

**3. I&C Testing Examples**

**Instrument Calibration (Example: Pressure Transmitter):**
- Remove transmitter from service (isolate, depressurize)
- Connect calibration standard (dead-weight tester or precision pressure source)
- Apply 0%, 25%, 50%, 75%, 100% of instrument range
- Verify output signal (4-20 mA) corresponds to applied pressure within tolerance
- Adjust zero and span if necessary
- Perform ascending and descending calibration to check hysteresis
- Acceptance: ±0.5% of span (typical for process instruments) or per specification
- **TBD** — Specific accuracy requirements per instrument specification

**Source:** IEC 62382, ISA practices **ASSUMPTION**

**Control Loop Functional Test:**
- Simulate process input (e.g., pressure) at field instrument
- Verify signal transmission to control system (PLC/DCS)
- Verify control system displays correct value and engineering units
- Verify control output to final control element (valve, damper)
- Verify final control element responds correctly (stroke test)
- Test both manual and automatic control modes
- Test alarm setpoints and annunciation
- **TBD** — Specific loop configurations per control system design

**Source:** IEC 62382 **location TBD**

**4. Integration with Other PKG-29 Deliverables**

- **DEL-29.02** (Inspection and Test Plan): Test procedures implement the hold/witness points defined in ITP
- **DEL-29.03** (Test Records): Test procedures include data sheets/forms that become test records
- **DEL-29.04** (FAT Records): FAT procedures are subset of test procedures executed at vendor facilities
- **DEL-29.05** (SAT Records): SAT procedures verify integrated system performance on site
- **DEL-29.06** (Tank Hydrotest Water Management Plan): Tank test procedures reference water management requirements
- **DEL-29.07, 29.08**: Test procedures specify water quality testing and disposal documentation

**Source:** PKG-29 deliverable relationships, Decomposition lines 646-653

### Lessons Learned and Best Practices

**Best Practice 1:** Involve operations and maintenance personnel in test procedure review — they provide valuable input on operability and future maintainability **ASSUMPTION**

**Best Practice 2:** Conduct pre-test meetings with all participants to review procedure, roles, hazards, and emergency response

**Best Practice 3:** Use checklists and hold points within procedures to ensure critical steps are not skipped

**Best Practice 4:** Build in time for "dry runs" or walkthrough of complex test procedures before execution

**Best Practice 5:** Document all deviations from procedure in real-time (don't rely on memory for post-test documentation)

**Best Practice 6:** Have spare parts and repair materials available during testing (gaskets, bolts, fittings) to minimize downtime for minor leaks

**Best Practice 7:** For hydrostatic testing, allow adequate time for filling (especially large tanks) and for water temperature stabilization

**Source:** General EPC industry practice **ASSUMPTION**

## Conflict Table (for human ruling)

No conflicts identified during document development. If conflicts arise during test procedure execution or integration with other deliverables, they shall be documented here for resolution.

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority | Human Ruling |
|-------------|----------|----------|----------|-------------------|-------------------|--------------|
| — | — | — | — | — | — | **TBD** |
