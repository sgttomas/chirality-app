# Procedure: DEL-26.02 Coating Procedures

## Purpose

This procedure document serves a dual purpose for **DEL-26.02 Coating Procedures**:

1. **Production:** Defines the process for producing coating procedure documents (surface preparation procedures and coating application procedures)
2. **Operation/Use:** Provides general guidance for executing coating procedures during construction/fabrication

**Deliverable type:** Procedure
**Responsible party:** D&B Contractor
**Deliverable output:** Surface preparation procedures and coating application procedures that implement DEL-26.01 (Coating Technical Specification)

**Source:** `_CONTEXT.md`; Decomposition DEL-26.02; 4_DOCUMENTS agent instructions (Procedure is dual-use and recursive)

**Note on recursive structure:** This deliverable produces procedures (anticipated artifacts), and this Procedure.md describes both how to produce those procedures AND how to use them. This is the intended recursive/dual-use structure for Procedure-type deliverables.

## PART A: PRODUCING COATING PROCEDURES

### Purpose

Define the process for producing surface preparation procedures and coating application procedures that implement DEL-26.01 requirements.

### Prerequisites

**Dependency tracking mode:** NOT_TRACKED
**Note:** Dependencies are coordinated externally by humans per project schedule and stage gates (see `execution/_Coordination/_COORDINATION.md`).

**Source:** `_DEPENDENCIES.md`

**Upstream deliverables and inputs (typical sequence — verify with project schedule):**

- **DEL-26.01** (Coating Technical Specification) — Coating systems, surface preparation standards (SSPC), DFT requirements, application environmental limits (PR-6), inspection requirements (QR-1), acceptance criteria
  - **Source:** Primary upstream deliverable; procedures implement DEL-26.01 requirements

- **DEL-26.03** (Coating Data Sheet Package) — Manufacturer data sheets for coating products (application requirements, pot life, mixing, environmental limits, cure times, recoat windows)
  - **Source:** Specification.md (IR-2)

- **PKG-13** (Storage Tanks) — Tank design (access provisions, internal appurtenances affecting coating application)
  - **Source:** For tank internal coating procedures

- **PKG-06** (Structural Steelwork) — Shop vs. field fabrication strategy
  - **Source:** For structural steel coating procedures

- **PKG-33** (HSE Management) — Project HSE procedures (confined space entry, hot work permits, respiratory protection, fall protection, environmental controls)
  - **Source:** Specification.md (IR-4); safety coordination

**ASSUMPTION:** Typical upstream dependencies for coating procedure development — confirm with project coordination.

### Reference Materials

**Required references:**

- **DEL-26.01** (Coating Technical Specification) — Requirements to be implemented by procedures
- **DEL-26.03** (Coating Data Sheet Package) — Manufacturer data sheets with product-specific application guidance
- **DEL-26.04** (Coating Installation & Test Records) — Record templates to be used by procedures
- **SSPC standards:** SP-1, SP-3, SP-5, SP-6, SP-10, SP-11 (surface preparation); PA-2, PA-17 (inspection); VIS-1 (visual standard)
- **ASTM standards:** D3359 (adhesion), D4417 (surface profile)
- **PKG-33 HSE procedures:** Confined space entry, hot work, respiratory protection, fall protection
- **Project Quality Management Plan:** Quality procedures and documentation requirements
- **Project procedure template:** **TBD** — Project-specific procedure format

**Source:** Specification.md (Standards section); Datasheet.md (References)

### Personnel Requirements

**Procedure author:**
- Qualified Coatings Engineer or Specialist
- Experience with protective coating application and inspection
- Familiarity with SSPC standards and coating application practice
- **ASSUMPTION:** Qualifications per project staffing plan

**Reviewers:**
- Coatings discipline lead (technical review)
- QA/QC reviewer (compliance with DEL-26.01, standards, quality procedures)
- HSE reviewer (safety review — JSA/HAZOP)
- Interdisciplinary reviewers (PKG-13 for tank internals, PKG-06 for structural steel, PKG-33 for HSE coordination)

**Approver:**
- Coatings discipline lead or designated authority

**Procedure users (for operational use):**
- Coating applicators and blasters (qualified per DEL-26.01 QR-3 or industry certification)
- Coating inspectors (NACE/AMPP Coating Inspector Level 2 or equivalent recommended)
- Confined space attendants (for tank internal coating)

**Source:** **ASSUMPTION** — Typical project quality procedures; Specification.md (QR-2 Competency and Training)

### Tools and Resources

- Project document management system
- Procedure template (project standard format) — **TBD**
- SSPC and ASTM standards library
- Manufacturer data sheets (DEL-26.03)
- Record templates (DEL-26.04)
- Job safety analysis (JSA) or HAZOP template for safety review

## Steps (Producing Coating Procedures)

### Step 1: Define Procedure Scope and Structure

**Objective:** Determine how many procedures are needed and what each procedure will cover.

**Activities:**

1.1. **Review DEL-26.01 requirements:**
- Identify all coating applications from DEL-26.01:
  - Tank internal coatings (food-grade, confined space)
  - Tank external coatings (atmospheric corrosion protection)
  - Structural steel coatings (shop and field)
  - Marine coatings (immersion, splash, atmospheric zones)
  - Field touch-up and repair
- Identify all surface preparation methods required:
  - Solvent cleaning (SSPC-SP 1)
  - Power tool cleaning (SSPC-SP 3, SP-11)
  - Abrasive blast cleaning (SSPC-SP 5, SP-6, SP-10)

1.2. **Determine procedure organization:**
- Decision: Generic procedures (one procedure for all applications) vs. application-specific procedures (separate procedure for each application)
- Recommendation per Guidance.md (Trade-offs): Application-specific procedures for usability and error reduction
- Proposed procedure set:
  - **Surface Preparation Procedures:**
    - Surface Preparation for Tank Internals (SSPC-SP 10 or SP-5, confined space)
    - Surface Preparation for Tank Externals and Structural Steel (SSPC-SP 6 or SP-10)
    - Surface Preparation for Marine Structures (SSPC-SP 10)
    - Solvent Cleaning (SSPC-SP 1, prerequisite for all blasting)
    - Power Tool Cleaning for Touch-Up and Repair (SSPC-SP 3, SP-11)
  - **Coating Application Procedures:**
    - Coating Application for Tank Internals (Food-Grade Coatings, confined space, holiday detection)
    - Coating Application for Tank Externals and Structural Steel (Multi-Coat Systems)
    - Coating Application for Marine Structures and Loading Equipment
    - Field Touch-Up and Repair

1.3. **Establish procedure structure:**
- Use consistent structure for all procedures (per Specification.md QR-1 Procedure Content Requirements):
  1. Purpose (what the procedure accomplishes)
  2. Scope (what applications/areas the procedure covers)
  3. Prerequisites (required conditions before starting)
  4. Equipment and Materials (tools, equipment, materials required)
  5. Safety and PPE (safety precautions, PPE requirements, permits required)
  6. Steps (detailed step-by-step instructions)
  7. Quality Control and Hold Points (inspection points, acceptance criteria)
  8. Documentation (records to be completed, forms from DEL-26.04)
  9. References (DEL-26.01, standards, data sheets, HSE procedures)

**Deliverable from Step 1:** Procedure scope definition and structure outline

**Source:** Guidance.md (Trade-offs — Generic vs. Application-Specific); Specification.md (QR-1)

### Step 2: Develop Surface Preparation Procedures

**Objective:** Write detailed surface preparation procedures for each application.

**Activities:**

2.1. **For each surface preparation procedure:**

**Purpose and Scope:**
- Define what surface preparation standard is achieved (SSPC-SP X)
- Define what application the procedure applies to (tank internals, structural steel, etc.)

**Prerequisites:**
- Surfaces accessible and ready for preparation
- Confined space entry permit (if applicable — tank internals)
- Equipment and materials available
- Personnel trained and competent
- Environmental conditions acceptable (no rain, temperature within limits)

**Equipment and Materials:**
- Abrasive blast equipment (blast pot, vacuum blast system for confined space)
- Abrasive (type and size per profile requirement from DEL-26.01 or manufacturer data sheet)
- Power tools (grinders, wire brushes for power tool cleaning)
- Solvents (for solvent cleaning SSPC-SP 1)
- Air supply (compressor, hoses)
- Ventilation equipment (for confined space)
- Lighting (for confined space or indoor work)
- PPE (supplied air respirator for blasting, hearing protection, eye protection, protective clothing)

**Safety and PPE:**
- Confined space entry permit and controls (if applicable)
- Respiratory protection (supplied air for blasting, especially confined space)
- Hearing protection (blast noise levels typically > 85 dBA)
- Fall protection (if elevated work)
- Dust control and containment
- Air monitoring (confined space: oxygen, LEL, toxics)
- Attendant (confined space)
- Rescue equipment (confined space)
- **Source:** Guidance.md (Worker Safety); PKG-33 HSE procedures

**Steps (example for abrasive blast cleaning):**
1. Inspect surfaces for oil, grease, and contaminants; perform solvent cleaning (SSPC-SP 1) if needed
2. Set up containment (tarpaulins, enclosures) for dust and abrasive control
3. Set up ventilation (if confined space or enclosed area)
4. Verify air monitoring and confined space entry controls active (if applicable)
5. Set up blast equipment and verify functionality
6. Perform abrasive blast cleaning to specified SSPC standard (SP-5, SP-6, or SP-10)
   - Maintain proper blast angle, distance, and overlap
   - Achieve uniform surface cleanliness and profile
7. Remove blast abrasive and dust (vacuum or sweep)
8. **HOLD POINT:** Notify inspector for surface preparation inspection

**Quality Control and Hold Points:**
- **Hold point:** Surface preparation inspection before coating application (mandatory)
- **Inspection:** Visual inspection per SSPC-VIS 1 (compare to specified SSPC-SP standard)
- **Profile measurement:** Measure surface profile per ASTM D4417 (target per DEL-26.01 or manufacturer data sheet)
- **Acceptance criteria:**
  - Surface cleanliness: Specified SSPC-SP standard achieved (visual confirmation per SSPC-VIS 1)
  - Surface profile: Within specified range (per DEL-26.01 requirements or manufacturer data sheet)
- **Non-conformance:** Re-blast areas not meeting acceptance criteria; re-inspect

**Documentation:**
- Complete Surface Preparation Record (form per DEL-26.04):
  - Date and time
  - Environmental conditions (temperature, humidity, wind, precipitation)
  - Abrasive type and size
  - Surface cleanliness verification (SSPC-SP standard achieved)
  - Surface profile measurement
  - Inspector name and signature
  - Acceptance for coating application (yes/no)

**References:**
- DEL-26.01 Coating Technical Specification (surface prep requirements, acceptance criteria)
- SSPC-SP standards (SP-1, SP-3, SP-5, SP-6, SP-10, SP-11)
- SSPC-VIS 1 Visual Standard
- ASTM D4417 Surface Profile Measurement
- Confined Space Entry Procedure (PKG-33, if applicable)

2.2. **Repeat for each surface preparation procedure** (tank internals, tank externals/structural steel, marine structures, solvent cleaning, power tool cleaning)

**Deliverable from Step 2:** Draft surface preparation procedures

**Source:** Datasheet.md (Surface Preparation Procedures); Guidance.md (Examples — Procedure Structure)

### Step 3: Develop Coating Application Procedures

**Objective:** Write detailed coating application procedures for each application.

**Activities:**

3.1. **For each coating application procedure:**

**Purpose and Scope:**
- Define what coating system is applied (per DEL-26.01)
- Define what application the procedure applies to (tank internals, structural steel, etc.)

**Prerequisites:**
- Surface preparation complete and accepted (surface prep hold point passed)
- Confined space entry permit (if applicable — tank internals)
- Equipment and materials available
- Coating materials conditioned to application temperature
- Personnel trained and competent
- Environmental conditions acceptable (temperature, humidity, dew point per DEL-26.01 PR-6 and manufacturer data sheet)

**Equipment and Materials:**
- Coating materials (primer, intermediate, topcoat per DEL-26.01 coating system)
- Mixing equipment (paddle mixer, drill)
- Application equipment:
  - Spray equipment (airless spray, conventional spray, plural component spray per coating type)
  - Brushes and rollers (for touch-up or areas unsuitable for spray)
- Environmental monitoring equipment (thermometer, hygrometer, dew point meter, surface temperature probe)
- DFT measurement equipment (magnetic gage per SSPC-PA 2)
- WFT measurement equipment (wet film thickness gage)
- Holiday detection equipment (low-voltage wet sponge or high-voltage holiday detector, if immersion service)
- Adhesion test equipment (ASTM D3359 cross-hatch kit)
- Ventilation equipment (for confined space or VOC control)
- Lighting (for confined space or indoor work)
- PPE (respiratory protection per coating type and ventilation, eye protection, protective clothing, gloves)

**Safety and PPE:**
- Confined space entry permit and controls (if applicable)
- Respiratory protection:
  - Organic vapor respirator (half-mask or full-face) for solvent-based coatings with adequate ventilation
  - Supplied air respiratory protection for confined space or high-exposure areas
- Fire prevention (flammable coatings):
  - Eliminate ignition sources
  - Fire extinguishers readily available
  - Hot work permit (if any hot work nearby)
- Fall protection (if elevated work)
- Ventilation (natural or mechanical for VOC control and respiratory protection)
- Air monitoring (confined space: oxygen, LEL, solvent vapors)
- Attendant (confined space)
- **Source:** Guidance.md (Worker Safety); DEL-26.01 (PR-6 Application Conditions); PKG-33 HSE procedures

**Steps (example for multi-coat spray application):**

0. **Pre-Application:**
   1. Verify surface preparation accepted (hold point passed)
   2. Verify environmental conditions acceptable:
      - Measure ambient temperature, relative humidity, surface temperature
      - Calculate dew point
      - Verify surface temperature ≥ dew point + 3°C (minimum)
      - Verify ambient temperature within manufacturer limits (typically 10–32°C)
      - Verify relative humidity ≤ 85% RH (or per manufacturer limit)
   3. Verify no precipitation forecast during application and cure period
   4. If environmental conditions not acceptable: delay coating application and re-check conditions
   5. Verify coating materials conditioned to application temperature (per manufacturer data sheet)
   6. Mix coating materials per manufacturer data sheet (mixing ratio, pot life, induction time)
   7. Record batch/lot numbers for each coating component

1. **Primer Application:**
   1. Apply primer coat by spray (or brush/roller for small areas) per manufacturer data sheet
   2. Monitor wet film thickness (WFT) during application to control dry film thickness (DFT)
      - Target WFT = Target DFT ÷ % Solids (per manufacturer data sheet)
   3. Achieve uniform coverage with no misses, runs, or sags
   4. Allow primer to cure per manufacturer data sheet (minimum cure time before intermediate coat)
   5. Measure DFT per SSPC-PA 2 at specified frequency (**TBD** — e.g., grid pattern 100 ft² areas for structural steel; 100% for tank internals)
   6. Verify DFT meets DEL-26.01 requirements (minimum DFT per coating system)
   7. **HOLD POINT (if specified):** Notify inspector for primer DFT verification before intermediate coat

2. **Intermediate Coat Application:**
   1. Verify primer cure time and recoat window per manufacturer data sheet (within maximum recoat window)
   2. Apply intermediate coat by spray (or brush/roller) per manufacturer data sheet
   3. Monitor WFT during application
   4. Achieve uniform coverage
   5. Allow intermediate coat to cure per manufacturer data sheet
   6. Measure DFT per SSPC-PA 2
   7. **HOLD POINT (if specified):** Notify inspector for intermediate DFT verification before topcoat

3. **Topcoat Application:**
   1. Verify intermediate cure time and recoat window
   2. Apply topcoat by spray (or brush/roller) per manufacturer data sheet
   3. Monitor WFT during application
   4. Achieve uniform coverage
   5. Allow topcoat to cure per manufacturer data sheet (cure time before final inspection and handling)
   6. Measure total DFT per SSPC-PA 2
   7. Verify total DFT meets DEL-26.01 requirements

4. **Post-Application (before final acceptance):**
   1. Allow final cure per manufacturer data sheet (full cure before service or final acceptance)
   2. Perform final visual inspection for defects (runs, sags, pinholes, contamination, color uniformity)
   3. Perform adhesion testing per ASTM D3359 at specified frequency (**TBD** — e.g., one test per 1000 ft² for structural steel; multiple tests for tank internals)
      - Acceptance: Rating 4B or 5B (or per DEL-26.01 requirement)
   4. Perform holiday detection (if immersion service — tank internals, marine immersion zones):
      - Low-voltage wet sponge (for DFT < 20 mils) or high-voltage holiday detector (for DFT > 20 mils)
      - Frequency: 100% coverage for immersion service
      - Mark detected holidays for repair
   5. Repair detected holidays or defects:
      - Surface prep repair area (power tool clean or spot blast)
      - Re-apply coating to repair area
      - Re-inspect repair area (DFT, holiday detection)
   6. **HOLD POINT (Final Acceptance):** Notify inspector for final acceptance inspection

**Quality Control and Hold Points:**

- **Hold point (Pre-Application):** Surface prep acceptance (before coating application starts)
- **Hold point (Primer, if specified):** Primer DFT verification (before intermediate coat)
- **Hold point (Intermediate, if specified):** Intermediate DFT verification (before topcoat)
- **Hold point (Final Acceptance, mandatory):** Final inspection and testing (DFT, adhesion, holiday detection, visual inspection) before final acceptance

**Acceptance criteria (Final):**
- Total DFT meets DEL-26.01 requirements (minimum DFT per coating system, per location)
- Adhesion test rating ≥ 4B (or per DEL-26.01 requirement)
- No holidays detected (for immersion service) or holidays repaired and re-inspected
- Visual inspection: No defects (runs, sags, pinholes, contamination, color variation exceeding acceptance limits)

**Non-conformance:**
- Areas not meeting DFT requirements: Apply additional coating to achieve specified DFT; re-inspect
- Adhesion test failures: Investigate cause (surface prep inadequate, contamination, out-of-spec application); remove coating and re-apply; re-test
- Holidays (immersion service): Repair per repair procedure; re-inspect with holiday detector

**Documentation:**

- Complete Coating Application Record (form per DEL-26.04):
  - Date and time of application
  - Environmental conditions (temperature, humidity, dew point, surface temperature, wind)
  - Coating material batch/lot numbers
  - WFT measurements during application
  - Cure times (primer, intermediate, topcoat)
  - Recoat windows (verify within limits)
- Complete DFT Measurement Record (form per DEL-26.04):
  - DFT measurements per location (grid or 100% coverage per application)
  - Acceptance (yes/no) per DEL-26.01 criteria
- Complete Adhesion Test Record (form per DEL-26.04):
  - Adhesion test locations
  - Test results (rating per ASTM D3359)
  - Acceptance (yes/no)
- Complete Holiday Detection Record (form per DEL-26.04, if immersion service):
  - Holiday detection method (low-voltage or high-voltage)
  - Holidays detected and repaired
  - Re-inspection results
- Inspector name and signature for each hold point and final acceptance

**References:**
- DEL-26.01 Coating Technical Specification (coating systems, DFT requirements, environmental limits, acceptance criteria)
- Manufacturer data sheets (DEL-26.03) for coating products (pot life, mixing, environmental limits, cure times, recoat windows)
- SSPC-PA 2 (DFT measurement)
- ASTM D3359 (adhesion testing)
- Confined Space Entry Procedure (PKG-33, if applicable)
- DEL-26.04 record templates

3.2. **Repeat for each coating application procedure** (tank internals, tank externals/structural steel, marine coatings, field touch-up)

**Deliverable from Step 3:** Draft coating application procedures

**Source:** Datasheet.md (Coating Application Procedures); Guidance.md (Application Quality Control); Specification.md (PR-4 DFT, PR-6 Application Conditions, QR-1 Inspection and Testing)

### Step 4: Technical Review and Interdisciplinary Coordination

**Objective:** Ensure procedures are technically accurate, complete, and coordinated with related disciplines and HSE.

**Activities:**

4.1. **Coatings discipline self-check:**
- Verify all procedures implement DEL-26.01 requirements (coating systems, surface prep standards, DFT, acceptance criteria)
- Verify all procedures reference manufacturer data sheets (DEL-26.03) correctly
- Verify all procedures use record templates from DEL-26.04
- Check internal consistency (no contradictions between procedures)

4.2. **Interdisciplinary review:**
- **PKG-13 (Storage Tanks):** Review tank internal coating procedures for coordination with tank design (access, internal appurtenances, confined space entry)
- **PKG-06 (Structural Steelwork):** Review structural steel coating procedures for coordination with shop vs. field responsibilities
- **PKG-08/09/11 (Marine):** Review marine coating procedures for coordination with marine structure design (exposure zones)
- **PKG-30 (Commissioning):** Review tank internal coating procedures for coordination with commissioning acceptance and food-grade cleanliness verification
- Collect comments and address coordination issues

4.3. **QA/QC review:**
- Verify procedures comply with DEL-26.01 requirements
- Verify hold points and acceptance criteria align with DEL-26.01
- Verify record requirements align with DEL-26.04
- Verify procedure content meets project quality procedures (Specification.md QR-1)

**Deliverable from Step 4:** Reviewed procedures with comment register

**Source:** Specification.md (Verification — Document Review)

### Step 5: Safety Review (JSA/HAZOP)

**Objective:** Verify procedures include adequate safety controls and comply with project HSE requirements.

**Activities:**

5.1. **Perform Job Safety Analysis (JSA) or HAZOP for each procedure:**
- Identify hazards for each step (confined space hazards, respiratory hazards, fall hazards, fire hazards, etc.)
- Verify controls are defined for each hazard (PPE, permits, ventilation, air monitoring, attendant, rescue equipment)
- Verify PPE requirements are specified
- Verify permit requirements are identified (confined space entry, hot work)

5.2. **Coordinate with PKG-33 (HSE Management):**
- Verify coating procedures comply with project HSE procedures (confined space entry, hot work, respiratory protection, fall protection, environmental controls)
- Align procedure safety requirements with PKG-33 procedures
- Resolve any conflicts or gaps

5.3. **Document safety review findings:**
- Record hazards identified, controls verified, and any procedure revisions needed
- Update procedures to address safety review findings

**Deliverable from Step 5:** Safety-reviewed procedures with JSA/HAZOP documentation

**Source:** Specification.md (Verification — Safety Review); Guidance.md (Worker Safety)

### Step 6: Walkthrough / Tabletop Review

**Objective:** Verify procedures are complete, logical, and executable.

**Activities:**

6.1. **Conduct walkthrough with personnel who will execute procedures:**
- Coating applicators, blasters, inspectors
- Walk through each procedure step-by-step
- Identify missing steps, unclear instructions, impractical requirements, or safety concerns

6.2. **Document walkthrough findings:**
- Record comments and recommended procedure revisions
- Update procedures to address walkthrough findings

6.3. **Consider trial run (if practical and warranted):**
- For critical procedures (tank internal coating) or novel methods, consider performing a trial run on representative surfaces
- Verify procedure is executable in actual field conditions
- Document trial run findings and update procedures accordingly
- **Note:** Trial run may not be practical for all procedures; prioritize for high-risk or critical applications

**Deliverable from Step 6:** Walkthrough-reviewed procedures (and trial run results, if applicable)

**Source:** Specification.md (Verification — Walkthrough / Tabletop Review, Trial Run)

### Step 7: Finalize and Approve Procedures

**Objective:** Finalize procedures for use in construction/fabrication.

**Activities:**

7.1. **Incorporate all review comments:**
- Technical review (Step 4)
- Safety review (Step 5)
- Walkthrough review (Step 6)
- Trial run findings (if applicable)

7.2. **Final quality check:**
- Verify all review comments addressed
- Verify procedure format complies with project procedure template
- Verify all cross-references are correct (DEL-26.01, DEL-26.03, DEL-26.04, PKG-33)
- Verify signature/approval blocks complete

7.3. **Obtain approval:**
- Submit procedures to Coatings discipline lead (or designated approver) for approval
- Obtain approval signatures per project quality procedures

7.4. **Issue procedures:**
- Update procedure status to "Issued" or equivalent per project lifecycle
- Place issued copies in `3_Issued/` folder (per project convention)
- Distribute procedures to users (coating applicators, inspectors, QA/QC, HSE personnel)
- Notify downstream deliverable owners (DEL-26.04 records coordinator)

7.5. **Update deliverable status:**
- Update `_STATUS.md` to reflect issuance (if applicable per lifecycle state)
- Record issue date and revision

**Deliverable from Step 7:** Issued coating procedures ready for use in construction/fabrication

**Source:** Specification.md (Documentation section)

### Step 8: Procedure Training and Competency Verification

**Objective:** Ensure personnel are competent to execute procedures.

**Activities:**

8.1. **Conduct procedure training:**
- Review procedures with coating applicators, blasters, and inspectors before use
- Emphasize critical steps, hold points, safety requirements, and documentation requirements
- Hands-on training for complex procedures (confined space entry + blasting/coating, specialized equipment)

8.2. **Verify personnel competency:**
- Verify personnel qualifications (industry certifications, training, experience):
  - Coating applicators: NACE/AMPP or SSPC certification (or equivalent) — **TBD**
  - Coating inspectors: NACE/AMPP Coating Inspector Level 2 (or equivalent) — **TBD**
  - Confined space attendants: Confined space entry training per WorkSafeBC and PKG-33
- Conduct competency assessment (verify understanding of critical steps, hold points, safety requirements)
- Document training and competency verification

8.3. **Issue procedures to trained personnel:**
- Provide issued procedures to trained and competent personnel
- Ensure procedures are accessible at point of use (job site, shop)

**Deliverable from Step 8:** Trained and competent personnel ready to execute coating procedures

**Source:** Specification.md (QR-2 Competency and Training); Guidance.md (Training and Competency)

### Step 9: Procedure Maintenance and Revision (Ongoing)

**Objective:** Maintain procedure currency and effectiveness through construction phase.

**Activities:**

9.1. **Monitor procedure execution:**
- Collect feedback from procedure users (applicators, inspectors)
- Monitor non-conformances and procedure-related issues
- Identify procedure improvements or clarifications needed

9.2. **Revise procedures as needed:**
- Update procedures per project change control procedures
- Update revision number and re-issue updated procedures
- Notify users of procedure revisions and conduct re-training if needed

9.3. **Maintain traceability:**
- Maintain revision history with dates and descriptions of changes
- Document rationale for procedure changes

**Source:** **ASSUMPTION** — Typical procedure maintenance during construction phase

---

## PART B: USING/OPERATING COATING PROCEDURES (General Guidance)

### Purpose

Provide general guidance for executing coating procedures (surface preparation and coating application) during construction/fabrication.

**Note:** This section provides overarching guidance for procedure execution. The specific procedures produced per Part A (above) contain detailed step-by-step instructions for each surface preparation and coating application task.

### Prerequisites (General for All Coating Work)

Before starting any coating work:

1. **Procedure availability:**
   - Issued procedures available and accessible at point of use
   - Personnel trained on procedures and competent to execute

2. **Permits and approvals:**
   - Confined space entry permit obtained (if applicable — tank internals)
   - Hot work permit obtained (if applicable — any hot work nearby)
   - Work authorization per project procedures

3. **Equipment and materials:**
   - All required equipment functional and calibrated (if applicable — DFT gages, environmental monitoring equipment)
   - All required materials available and conditioned (coating materials at application temperature, abrasive sufficient quantity)

4. **Environmental conditions:**
   - Weather forecast acceptable (no precipitation during application and cure)
   - Environmental conditions within limits (temperature, humidity, dew point per DEL-26.01 PR-6 and manufacturer data sheet)

5. **Safety:**
   - All safety controls in place (confined space controls, ventilation, air monitoring, attendant, rescue equipment, PPE)
   - Personnel briefed on hazards and safety requirements (toolbox talk or equivalent)

### General Execution Steps

**Step 1: Pre-Work Preparation**
- Review procedure for the specific task (surface preparation or coating application)
- Verify prerequisites complete (permits, equipment, materials, environmental conditions, safety controls)
- Brief crew on work scope, critical steps, hold points, and safety requirements
- Set up work area (containment, ventilation, lighting, access)

**Step 2: Execute Procedure**
- Follow procedure steps in sequence
- Monitor quality during work (WFT for coating application, surface cleanliness for surface prep)
- Monitor environmental conditions during work (temperature, humidity, dew point)
- Monitor safety during work (air quality for confined space, PPE compliance)
- Complete documentation during work (record environmental conditions, batch/lot numbers, WFT measurements)

**Step 3: Hold Points**
- Stop work at each hold point defined in procedure
- Notify inspector for hold point inspection
- Do not proceed beyond hold point until acceptance obtained
- If non-conformance identified at hold point: address non-conformance (rework, repair) and re-inspect

**Step 4: Documentation**
- Complete all required records per procedure (surface prep records, application records, DFT records, adhesion test records, holiday detection records)
- Use record templates from DEL-26.04
- Obtain inspector signatures at hold points and final acceptance
- Submit completed records to QA/QC or records coordinator per project procedures

**Step 5: Final Acceptance**
- After final cure (per manufacturer data sheet), request final acceptance inspection
- Inspector performs final visual inspection, DFT verification, adhesion testing, holiday detection (if immersion service)
- If final acceptance achieved: work complete; submit final records
- If non-conformance identified: address non-conformance (rework, repair) and request re-inspection

### Quality Control (General Principles)

- **In-process quality control:** Monitor quality during work (WFT, visual inspection) to prevent defects from progressing
- **Hold point inspections:** Stop work at hold points for acceptance inspection before proceeding (prevents non-conforming work)
- **Final acceptance inspection:** Comprehensive inspection and testing after final cure (DFT, adhesion, holiday detection, visual inspection) before final acceptance
- **Non-conformance handling:** Address non-conformances promptly (rework, repair per procedure); re-inspect after rework
- **Traceability:** Complete all required records to provide traceability (what was done, when, under what conditions, who inspected and accepted)

**Source:** DEL-26.01 (QR-1 Inspection and Testing); Specification.md (PR-1 Inspection and Hold Points)

### Safety (General Principles)

- **Confined space entry (tank internals):**
  - Obtain confined space entry permit before entry
  - Verify air monitoring (oxygen ≥ 19.5%, LEL < 10%, no toxic gases)
  - Maintain continuous ventilation during work
  - Station attendant outside confined space (continuous communication with workers inside)
  - Verify rescue equipment ready
  - **Source:** PKG-33 Confined Space Entry Procedure; Guidance.md (Worker Safety)

- **Respiratory protection:**
  - Use respiratory protection per procedure requirements:
    - Supplied air for abrasive blasting and confined space coating
    - Organic vapor respirator (minimum) for solvent-based coatings with adequate ventilation
  - Verify respirator fit-tested and personnel trained per respiratory protection program
  - **Source:** PKG-33 Respiratory Protection Program; WorkSafeBC

- **Fall protection:**
  - Use fall protection per project fall protection procedures for elevated work (platforms, scaffolds, tanks)
  - **Source:** PKG-33 Fall Protection Procedure

- **Fire prevention (flammable coatings):**
  - Eliminate ignition sources (no smoking, no hot work, no sparking tools)
  - Verify fire extinguishers readily available
  - Ensure adequate ventilation to prevent flammable vapor accumulation
  - **Source:** PKG-33 Fire Prevention Procedure; manufacturer data sheets

- **Stop work authority:**
  - Any worker has authority to stop work if unsafe conditions identified
  - Report unsafe conditions to supervisor and HSE personnel
  - Do not resume work until unsafe conditions corrected

**Source:** PKG-33 (HSE Management); WorkSafeBC regulations

### Environmental Compliance

- **VOC emissions:**
  - Minimize VOC emissions per project environmental plan (use low-VOC coatings where practical, control ventilation exhaust)
  - Comply with provincial/federal VOC regulations
  - **Source:** Project Environmental Management Plan; Guidance.md (Regulatory Context)

- **Waste disposal:**
  - Dispose of blast abrasive, coating waste, solvent waste per project environmental plan and regulations
  - Use designated waste containers and disposal methods
  - **Source:** Project Environmental Management Plan

## Verification (Producing and Using Coating Procedures)

### Deliverable Acceptance Criteria (Producing Procedures)

**The Coating Procedures deliverable is acceptable when:**

- ✓ All anticipated artifacts produced per Decomposition DEL-26.02:
  - Surface preparation procedures (covering all SSPC standards required by DEL-26.01)
  - Coating application procedures (covering all coating types specified by DEL-26.01)
- ✓ All procedures implement DEL-26.01 requirements (coating systems, surface prep standards, DFT, acceptance criteria)
- ✓ All procedures include required content per Specification.md QR-1 (purpose, scope, prerequisites, equipment, safety, steps, QC, documentation, references)
- ✓ All safety controls defined (confined space, respiratory protection, fall protection, hot work, ventilation)
- ✓ All inspection hold points and acceptance criteria defined and aligned with DEL-26.01
- ✓ All documentation requirements defined and aligned with DEL-26.04
- ✓ All reviews complete (technical, interdisciplinary, QA/QC, safety per Steps 4-5)
- ✓ Walkthrough or tabletop review complete with findings addressed (Step 6)
- ✓ Safety review (JSA/HAZOP) complete with findings addressed (Step 5)
- ✓ Trial run complete (if applicable) with findings addressed (Step 6)
- ✓ Personnel training and competency verification complete (Step 8)
- ✓ Procedures approved by authorized personnel (Step 7)
- ✓ Procedures issued and distributed per project document control procedures (Step 7)

**Source:** Specification.md (Verification — Acceptance Criteria)

### Operational Success Criteria (Using Procedures)

**Coating work is successful when:**

- ✓ All procedures followed as written (no unauthorized deviations)
- ✓ All hold point inspections performed and acceptance obtained before proceeding
- ✓ Final acceptance inspection passed (DFT, adhesion, holiday detection, visual inspection per DEL-26.01 acceptance criteria)
- ✓ All required records completed and submitted (surface prep, application, DFT, adhesion, holiday detection per DEL-26.04)
- ✓ No safety incidents (confined space incidents, respiratory exposures, falls, fires)
- ✓ Environmental compliance maintained (VOC emissions, waste disposal)

## Records

### Documentation Outputs (Producing Procedures)

**Primary deliverables:**
- Surface preparation procedures (multiple procedures by application — see Step 1)
- Coating application procedures (multiple procedures by application — see Step 1)

**Supporting documentation:**
- Technical review comment register and disposition (Step 4)
- Safety review (JSA/HAZOP) documentation (Step 5)
- Walkthrough review findings and disposition (Step 6)
- Trial run results (if applicable, Step 6)
- Training and competency verification records (Step 8)

**Source:** Decomposition DEL-26.02 anticipated artifacts; Specification.md (Documentation section)

### Documentation Outputs (Using Procedures)

**Records generated during coating work (filed in DEL-26.04):**
- Surface preparation records (environmental conditions, inspection results, surface profile)
- Coating application records (environmental conditions, batch/lot numbers, cure times)
- DFT measurement records (DFT readings, acceptance)
- Adhesion test records (test results, acceptance)
- Holiday detection records (for immersion service)

**Source:** Datasheet.md (Documentation and Records); DEL-26.04 (Coating Installation & Test Records)

### Record Management

**Filing locations:**
- **Procedure documents (produced):** `1_Working/DEL-26.02_Coating_Procedures/` (working), `3_Issued/` (issued procedures)
- **Coating work records (generated during use):** DEL-26.04 folder structure per project record management procedures

**Retention requirements:** Per project record retention requirements — **TBD**

**Source:** README.md (project filesystem structure); **ASSUMPTION** — Standard record management

### Cross-Document Consistency Check

**Verify consistency with related deliverables:**

- **Datasheet.md:** Procedure types and applications match Datasheet content
- **Specification.md:** Procedures implement Specification requirements
- **Guidance.md:** Procedures reflect Guidance principles and considerations
- **DEL-26.01 (Coating Technical Specification):** Procedures implement DEL-26.01 requirements (coating systems, surface prep, DFT, acceptance criteria)
- **DEL-26.03 (Coating Data Sheet Package):** Procedures reference manufacturer data sheets correctly
- **DEL-26.04 (Coating Installation & Test Records):** Procedures use DEL-26.04 record templates

**Source:** 4_DOCUMENTS agent instructions (cross-document consistency requirement)

---

## Cross-Document Verification Summary

| Procedure Step | Specification § | Datasheet § | Guidance § | Output/Reference |
|----------------|-----------------|-------------|------------|------------------|
| Step 1 (Scope/Structure) | QR-1, Scope | Attributes, Coverage Scope | Trade-offs (Generic vs. Specific) | Procedure outline |
| Step 2 (Surface Prep) | FR-1, PR-1, IR-1 | Surface Preparation Procedures | Surface Preparation Quality | Draft procedures |
| Step 3 (Coating Application) | FR-2, FR-3, PR-2, PR-3, PR-4 | Coating Application Procedures | Application Quality Control | Draft procedures |
| Step 4 (Technical Review) | Verification (Document Review) | Cross-references | Coordination Points | Comment register |
| Step 5 (Safety Review) | FR-4, IR-4, IR-5 | Conditions (Safety) | Worker Safety | JSA/HAZOP |
| Step 6 (Walkthrough) | Verification (Walkthrough) | — | Trade-offs (Verification) | Review findings |
| Step 7 (Finalize/Approve) | Documentation | Attributes | — | Issued procedures |
| Step 8 (Training) | QR-2 | — | Training and Competency | Training records |
| Step 9 (Maintenance) | — | — | — | Revised procedures |
| Part B (General Execution) | PR-1, PR-2, PR-4 | Inspection and Acceptance | Application Quality Control | Work records → DEL-26.04 |

**Verification status:** Pass 3 complete — Procedure steps traceable to Specification requirements and Guidance principles.

**Downstream deliverable notification checklist:**
- [ ] DEL-26.04 (Coating Installation & Test Records) — Receives record templates and documentation requirements
