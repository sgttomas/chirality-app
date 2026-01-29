# Procedure: DEL-30.08 Cathodic Protection Test & Commissioning Installation & Test Records

## Purpose

Defines the process for executing and documenting **Cathodic Protection (CP) Commissioning** for the Canola Oil Transload Facility.

**Context:** Provides evidence of completion, inspection, and testing for cathodic protection test & commissioning.

**Source:** Decomposition §5 PKG-30, DEL-30.08

## Prerequisites

**Dependencies:** NOT_TRACKED mode — See `_DEPENDENCIES.md`

**Upstream Requirements:**
- DEL-30.01 Commissioning Procedures — CP commissioning procedures
- DEL-30.02 Commissioning Plan — CP commissioning schedule
- CP system design documents (PKG-03, PKG-08, PKG-14) — CP design basis and criteria
- CP system installation complete (anodes, rectifiers, test stations, wiring)
- Coating installation complete and cured (where applicable)
- Backfill complete (for buried structures)

**Personnel:**
- CP specialist (NACE certified or equivalent)
- Commissioning engineer
- Corrosion engineer (review and acceptance)
- QC inspector
- Regulatory authority representative (if required)

**Tools:**
- High-impedance voltmeter (for potential measurements)
- Reference electrodes (copper-copper sulfate for soil, silver-silver chloride for seawater)
- Interruption equipment (for CP-off potential measurement)
- Multimeter (for continuity and resistance measurements)
- GPS (for test station location documentation)
- Camera (for documentation photos)
- CP commissioning test forms — **TBD**

**Source:** NACE SP0169; **ASSUMPTION: likely applicable**; DEL-30.01, DEL-30.02

## Steps

**Step 1: Review CP System Design**
- Review CP design documents from PKG-03, PKG-08, PKG-14
- Understand protected structures, CP system type (galvanic, impressed current, hybrid)
- Review design criteria: Protective potential targets, current requirements
- Identify test station locations from design drawings
- Review CP commissioning procedure from DEL-30.01

**Step 2: Conduct Pre-Commissioning Electrical Tests**

**Test 2.1: Anode-to-Structure Continuity**
- Measure electrical continuity from each anode (or anode bed) to protected structure
- Verify continuity within acceptable limits (low resistance)
- Document continuity test results

**Test 2.2: Structure Electrical Isolation**
- Verify protected structure electrically isolated from foreign structures (other piping, grounding systems, etc.)
- Measure structure-to-foreign-structure resistance (should be high, >10 kΩ typical)
- Document isolation verification

**Test 2.3: Stray Current Survey**
- Conduct stray current survey to detect interference sources
- Measure structure potentials at multiple locations
- Identify any stray current effects
- Document stray current conditions

**Test 2.4: Short Circuit Detection**
- Test for short circuits in CP system (anode to structure shorts, coating holidays)
- Document any shorts and resolve before proceeding

**Step 3: Energize CP System and Commission Rectifier**

**For Impressed Current CP Systems:**
- Energize rectifier per manufacturer instructions
- Set initial output per design requirements (voltage, current)
- Adjust tap settings as needed
- Verify output stable under load
- Test automatic controls (if applicable)
- Verify safety features (overcurrent protection, lightning arrestor)
- Document rectifier settings and output

**For Galvanic Anode Systems:**
- Verify anodes connected and providing protective current
- Measure anode-to-structure potential and current output
- Document galvanic system operation

**Step 4: Conduct Baseline Potential Survey**

**Survey 4.1: CP-Off Potentials (Native Potentials)**
- Interrupt CP system (turn off rectifier or disconnect anodes temporarily)
- Allow depolarization (wait time per NACE SP0169, typically 1-10 seconds)
- Measure structure-to-electrolyte potentials at all test stations
- Use consistent reference electrode type (CSE for soil, Ag/AgCl for seawater)
- Document CP-off potentials (native structure potentials)

**Survey 4.2: CP-On Potentials (Protected Potentials)**
- Re-energize CP system
- Allow polarization to stabilize (wait time varies, 24 hours to several days typical)
- Measure structure-to-electrolyte potentials at all test stations
- Document CP-on potentials (protected potentials with CP active)

**Survey 4.3: Polarization Verification**
- Calculate polarization shift: (CP-on potential) - (CP-off potential)
- Verify polarization shift meets criteria (typically 100 mV minimum)
- Verify CP-on potentials meet protective criteria (typically -850 mV vs. CSE or more negative)
- Document protective criteria achieved

**Survey 4.4: Potential Profile Mapping**
- Map potential profile along protected structures
- Identify any areas with inadequate protection (insufficient negative potential)
- If inadequate: Adjust rectifier output, add supplemental anodes, investigate coating defects
- Re-survey after adjustments

**Step 5: Verify CP System Performance**
- Verify all protected structures achieve protective potentials
- Verify current distribution adequate
- Verify no adverse effects (coating damage, stray current interference with other systems)
- Verify rectifier output stable and within design capacity
- Document CP system performance verification

**Step 6: Document Non-Conformances and Resolutions**
- If protective criteria not achieved: Document non-conformance
- Investigate root cause (inadequate current, coating defects, electrical shorts, stray current interference)
- Implement corrective action (adjust rectifier, repair coating, add anodes, mitigate interference)
- Re-test after correction
- Document resolution and acceptance

**Step 7: Obtain Sign-offs and Acceptance**
- CP specialist reviews commissioning test sheets and signs
- Commissioning engineer reviews and signs
- Corrosion engineer reviews baseline data and provides acceptance
- QC inspector verifies and signs
- Regulatory authority witnesses and accepts (if required) — **TBD**

**Step 8: Submit CP Commissioning Records**
- Compile all CP commissioning records:
  - Pre-commissioning electrical tests
  - Rectifier commissioning and settings
  - Baseline potential survey (CP-off and CP-on potentials)
  - Potential profile maps
  - Protective criteria verification
  - Acceptance certificates
- Submit to document control
- File in `3_Issued/DEL-30.08/`
- Provide baseline data to operations for ongoing CP monitoring program

**Source:** NACE SP0169; **ASSUMPTION: likely applicable**; **ASSUMPTION** — CP commissioning process

## Verification

- CP pre-commissioning electrical tests complete
- Rectifier commissioned and settings documented
- Baseline potential survey complete (CP-off and CP-on)
- Protective criteria achieved on all structures
- Sign-offs obtained
- Acceptance achieved

**Source:** Specification.md

## Records

**Outputs:**
- CP commissioning test sheets (electrical tests, energization, performance)
- Rectifier settings records (settings, output verification)
- Baseline potential survey data (CP-off, CP-on, polarization verification)
- Potential profile maps
- Acceptance records (CP specialist, corrosion engineer, regulatory authority)

**Management:**
- Filed in `3_Issued/DEL-30.08/`
- Baseline data provided to operations for ongoing CP monitoring
- Retention: **TBD** — Permanent project records (lifecycle baseline)

**Source:** Decomposition §5 DEL-30.08

---

## Document Cross-References

- **← Datasheet / Specification / Guidance:** Procedure implements CP commissioning requirements
- CP commissioning records provide baseline for ongoing CP monitoring (PKG-31 O&M Manuals)
- Supports long-term facility integrity (OBJ-1) and lifecycle cost optimization (OBJ-9)
