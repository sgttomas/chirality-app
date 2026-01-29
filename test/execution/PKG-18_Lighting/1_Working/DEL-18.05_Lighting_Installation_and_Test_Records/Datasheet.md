# Datasheet: DEL-18.05 Lighting Installation & Test Records

## Identification

| Field | Value |
|-------|-------|
| Deliverable ID | DEL-18.05 |
| Name | Lighting Installation & Test Records |
| Package | PKG-18 Lighting |
| Discipline | Electrical |
| Type | Record |
| Responsible | D&B Contractor (QA/QC) |
| Status | INITIALIZED |

## Attributes

| Attribute | Value |
|-----------|-------|
| Record Package Contents | Illumination test records per anticipated artifacts *(Source: _CONTEXT.md, Decomposition)* |
| Record Format | **TBD** — **ASSUMPTION**: Standardized test forms with signatures and data |
| Record Categories | Installation records, Functional test records, Illumination test records, Emergency lighting test records — **ASSUMPTION** |
| Retention Period | **TBD** — **ASSUMPTION**: Permanent retention as project closeout documentation |
| Quality Classification | **TBD** — **ASSUMPTION**: QA/QC records per project Quality Management Plan |

**Testing and Commissioning Scope:**

| Test Category | Description |
|---------------|-------------|
| Installation Inspection | Verification of proper installation, mounting, wiring, grounding per drawings and specifications |
| Illumination Level Testing | Field measurement of illuminance levels to verify compliance with design calculations (DEL-18.03) |
| Emergency Lighting Testing | Duration testing and illuminance verification for emergency egress lighting per NFPA 101 |
| Control System Functional Testing | Verification of lighting controls operation (sensors, switches, integration with PKG-19) |
| Final Acceptance | Punch list completion and final acceptance sign-off |

## Conditions

**Operating / Environmental Context:**

This deliverable provides evidence of completion, inspection, and testing for lighting. *(Source: _CONTEXT.md, Decomposition DEL-18.05 description)*

**Project Context:**
- **Location:** Fraser Surrey Terminal, 11060 Elevator Road, Surrey, BC *(Source: Decomposition Section 1)*
- **Facility Type:** Canola Oil Transload Facility *(Source: Decomposition Section 1)*
- **Testing Environment:** Marine terminal with outdoor and indoor testing conditions

**Testing Conditions:**

| Parameter | Value |
|-----------|-------|
| Testing Phase | Commissioning phase after installation completion |
| Test Participants | Contractor QA/QC, Electrical Engineer, Commissioning Agent (if applicable), Employer representative — **TBD** |
| Test Equipment | Illuminance meters (lux meters), multimeters, stopwatches for emergency duration tests — **TBD** |
| Test Standards | IESNA measurement procedures, NFPA 101 emergency lighting test requirements — **TBD** |
| Weather Conditions | Exterior testing conducted at night in dry conditions — **ASSUMPTION** |
| Acceptance Criteria | Measured illuminance ≥ 80% of calculated values typical; emergency lighting meets NFPA 101 minimums — **TBD** — **ASSUMPTION** |

## Construction

**Installation & Test Records Package Contents:**

Anticipated artifacts per decomposition and _CONTEXT.md:
1. **Illumination test records** — Field illuminance measurements for exterior and interior areas

**Typical Records Package Structure:**

**Section 1: Installation Inspection Records**
- **Fixture installation checklists:** Verify each fixture properly mounted, aligned, secure per manufacturer instructions and drawings (DEL-18.01)
- **Pole installation inspections:** Verify poles plumb, properly grouted/anchored, grounding connections per specifications
- **Wiring and circuiting verification:** Verify circuit assignments match drawings, proper wire sizes per CSA C22.1, grounding and bonding complete
- **As-built markups:** Document any deviations from design drawings for incorporation into as-builts
- **Installation photographs:** Photographs of installed fixtures, poles, control panels for record

**Section 2: Illumination Test Records**
- **Test plan:** Define test locations, grid, equipment, procedures per Specification and Procedure
- **Exterior illumination tests:**
  - Measurement locations on site plan (grid or key points)
  - Measured illuminance values (lux or fc)
  - Comparison to calculated values from DEL-18.03
  - Pass/fail determination per acceptance criteria
- **Interior illumination tests:**
  - Measurement locations on floor plans
  - Measured illuminance values
  - Comparison to calculated values from DEL-18.03
  - Pass/fail determination
- **Test equipment calibration certificates:** Illuminance meters calibrated within 12 months — **TBD** — **ASSUMPTION**
- **Environmental conditions during testing:** Date, time (night for exterior), weather, temperature — **ASSUMPTION**
- **Signatures:** Tested by (contractor), Witnessed by (Employer/commissioning agent) — **TBD**

**Section 3: Emergency Lighting Test Records**
- **Emergency illuminance testing:**
  - Measurement of illuminance levels along egress paths under emergency power
  - Verification of minimum 10 lux average, 1 lux minimum per NFPA 101 — **TBD** — **ASSUMPTION**
- **Duration testing:**
  - Disconnect normal power; verify emergency lights activate
  - Measure battery backup duration (minimum 90 minutes per NFPA 101) — **TBD** — **ASSUMPTION**
  - Record time to failure or end of test
- **Self-test verification:** For fixtures with self-test capability, verify monthly and annual self-tests function correctly — **TBD**

**Section 4: Control System Functional Test Records**
- **Occupancy sensors:** Verify on/off operation, time delays adjustable and functional
- **Photocells:** Verify dusk-to-dawn operation or daylight harvesting functionality
- **Manual controls:** Verify switches, contactors operate correctly
- **Integration with facility controls (PKG-19):** Verify communication, monitoring, remote control functions — **TBD**
- **Control zone verification:** Verify control zones match design and operate independently as intended

**Section 5: Punch List and Final Acceptance**
- **Punch list:** Document deficiencies found during testing (non-compliant illuminance, damaged fixtures, control malfunctions)
- **Punch list resolution:** Document corrective actions and re-testing
- **Final acceptance certificate:** Final sign-off that lighting system is complete, tested, and compliant — **TBD**
- **Training records:** Document owner/operator training on lighting system operation and maintenance — **TBD**
- **O&M manual delivery:** Confirm operation and maintenance manuals delivered — **TBD**

**Interface Requirements:**

- **Lighting Design Drawings (DEL-18.01)** — Installation verified against drawings; test locations based on calculation grids
- **Lighting Technical Specification (DEL-18.02)** — Installation and testing per specification requirements
- **Lighting Design Calculations (DEL-18.03)** — Measured illuminance compared to calculated values
- **Lighting Data Sheet Package (DEL-18.04)** — Installed equipment verified against approved data sheets
- **Construction QA/QC Program** — Testing performed per project QA/QC procedures — **TBD**

## References

**Primary References:**
- Decomposition: `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md` — PKG-18 scope, DEL-18.05 entry
- Context: `_CONTEXT.md` — Deliverable identity and anticipated artifacts
- Specification: `Specification.md` — Testing requirements and acceptance criteria
- Guidance: `Guidance.md` — Testing principles and best practices
- Procedure: `Procedure.md` — Detailed testing and commissioning procedures

**Applicable Standards:**
- **IESNA Lighting Handbook** — Illuminance measurement procedures — **TBD** *(Edition TBD)*
- **NFPA 101** (Life Safety Code) — Emergency lighting testing requirements — **ASSUMPTION**
- **CSA C22.1** (Canadian Electrical Code) — Installation and testing requirements — **ASSUMPTION**

**Project-Specific References:**
- Employer's Requirements Volume 2 Part 1, Part 2, Part 3 — Testing and commissioning requirements — **TBD**
- Project Quality Management Plan — QA/QC procedures for testing and inspection — **TBD**
- Project Commissioning Plan — Commissioning procedures and acceptance criteria — **TBD**

**Cross-References (within PKG-18):**
- DEL-18.01 Lighting Design Drawing Set — Installation verified against drawings
- DEL-18.02 Lighting Technical Specification — Testing per specification requirements
- DEL-18.03 Lighting Design Calculations — Measured values compared to calculated values
- DEL-18.04 Lighting Data Sheet Package — Equipment verified against approved data sheets
