# Datasheet: DEL-29.01 Test Procedures

## Identification

| Field | Value |
|-------|-------|
| Deliverable ID | DEL-29.01 |
| Name | Test Procedures |
| Package | PKG-29 Testing |
| Discipline | T&C |
| Type | Procedure |
| Responsible | D&B Contractor (QA/QC) |
| Status | INITIALIZED |

**Source:** _CONTEXT.md, Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md lines 646

## Attributes

| Attribute | Value |
|-----------|-------|
| Procedure Category | Testing & Commissioning |
| Test Types | Hydrostatic, Electrical, I&C |
| Applicable Systems | Storage tanks, piping, electrical distribution, control systems |
| Applicable Phase | Construction completion through commissioning |
| Procedure Classification | QA/QC Execution Procedures |
| Revision | **TBD** — Initial issue pending development |

**ASSUMPTION:** Test procedures will be developed as equipment and systems are defined during detailed design.

## Conditions

**Operating / Environmental Context:**

Defines the execution method and controls for test to meet safety, quality, and operational requirements. **Source:** Decomposition line 646

**Project Context:**
- Facility: Canola Oil Transload Facility — Phase 1
- Location: Fraser Surrey Terminal, 11060 Elevator Road, Surrey, BC
- Contract Type: Design & Build
- Employer: DP World Fraser Surrey Inc.

**Source:** Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md Section 1

**Testing Environment:**
- Operating temperature range: **TBD** — varies by system under test (cryogenic to ambient to elevated)
- Environmental exposure: Marine terminal environment (corrosive atmosphere)
- Hazardous area classification: **TBD** — **ASSUMPTION**: Class I Div 2 areas for product handling systems (to be confirmed per facility hazardous area study)
- Seismic requirements: **TBD** — As per British Columbia Building Code and project seismic study
- Test medium considerations: Hydrostatic (water), electrical (energized), pneumatic (air/nitrogen) **ASSUMPTION**

**Project Objectives Supported:**
- OBJ-1: Safe & Reliable Operation
- OBJ-10: Custody Transfer Accuracy

**Source:** Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md Section 6 (Objective-to-Deliverable Mapping), lines 780, 789

## Construction

**Materials / Configuration:**

**Test Procedure Types:**

1. **Hydrostatic Test Procedures:**
   - Storage tank hydrostatic testing (3 × 15,000 MT tanks)
   - Process piping pressure testing
   - Loading arm system pressure testing
   - Test medium: Potable water **ASSUMPTION**
   - Test pressure: **TBD** — Per ASME/API standards and design pressure
   - Hold duration: **TBD** — Per applicable codes

2. **Electrical Test Procedures:**
   - Electrical power distribution testing
   - Motor and equipment continuity testing
   - Insulation resistance testing
   - Protection relay testing
   - Grounding system verification
   - Test equipment: **TBD** — Meggers, multimeters, relay test sets

3. **I&C Test Procedures:**
   - Instrument calibration procedures
   - Control loop testing
   - Interlock verification
   - Metering system accuracy verification (custody transfer)
   - Safety system functional testing
   - Test equipment: **TBD** — Calibrators, signal generators, PLCsimulators

**Source:** _CONTEXT.md Anticipated Artifacts; Decomposition line 646

**Procedure Format:**
- Document structure: **TBD** — **ASSUMPTION**: Per project procedure template
- Approval requirements: **TBD** — Multi-discipline review expected
- Witness/hold points: Cross-reference with DEL-29.02 (Inspection and Test Plan With Hold/Witness Points)
- Safety documentation: Job Safety Analysis (JSA) for each test type **ASSUMPTION**

## References

**Decomposition & Context:**
- Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md (Section 5, PKG-29, lines 636-653)
- _CONTEXT.md (deliverable identity and scope)
- _REFERENCES.md (reference materials listing)

**Applicable Standards:**
- ASME B31.3: Process Piping (hydrostatic testing)
- API 650: Welded Tanks for Oil Storage (tank hydrostatic testing)
- API 653: Tank Inspection, Repair, Alteration, and Reconstruction (testing requirements)
- CSA Z662: Oil and Gas Pipeline Systems (pressure testing)
- IEC 62382: Electrical and instrumentation loop check (I&C testing)
- NFPA 70: National Electrical Code (electrical testing)
- IEEE 43: Insulation Resistance Testing
- ASME PCC-1: Guidelines for Pressure Boundary Bolted Flange Joint Assembly
- Employer's Requirements: **location TBD** — Project-specific testing requirements

**Cross-References:**
- DEL-29.02: Inspection and Test Plan With Hold/Witness Points (ITR procedures integration)
- DEL-29.03: Test Installation & Test Records (records resulting from these procedures)
- DEL-29.06: Tank Hydrotest Water Management Plan (water supply, treatment, disposal)
- DEL-13.01-13.06: Storage Tanks (tank design and testing requirements)
- DEL-14.01-14.08: Process Piping (piping design and testing requirements)
- DEL-17.01-17.05: Electrical Power Distribution (electrical system testing)
- DEL-19.01-19.05: Control Systems (I&C testing)
- See `_DEPENDENCIES.md` (NOT_TRACKED — dependencies coordinated externally)

**ASSUMPTION:** Specific clause references from standards will be identified during procedure development when design details are available.
