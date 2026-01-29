# Specification: DEL-26.02 Coating Procedures

## Scope

This specification defines requirements for coating execution procedures (surface preparation and coating application) that implement the coating technical specification (DEL-26.01) for the Canola Oil Transload Facility at Fraser Surrey Terminal, Surrey, BC.

**Source:** Decomposition DEL-26.02 description; Datasheet.md

**Relationship to DEL-26.01:**
- DEL-26.01 (Coating Technical Specification) defines WHAT coating systems, performance requirements, and acceptance criteria
- DEL-26.02 (Coating Procedures — this deliverable) defines HOW to execute surface preparation and coating application to meet DEL-26.01 requirements
- **Source:** Decomposition deliverable structure; DEL-26.01 (IR-4)

### Inclusions

This specification covers procedure requirements for:

- **Surface preparation procedures:** Methods to achieve SSPC surface preparation standards specified in DEL-26.01
- **Coating application procedures:** Methods to apply coating systems specified in DEL-26.01 within environmental limits and quality controls

**Applications:** Tank internals, tank externals, structural steel, marine structures, field painting (all coating types per DEL-26.01)

**Source:** Decomposition DEL-26.02; Datasheet.md (Construction)

### Exclusions

- Material specifications (defined in DEL-26.01, supported by DEL-26.03)
- Inspection and test record templates (defined in DEL-26.04)
- **TBD** — Other exclusions to be confirmed

## Requirements

### Functional Requirements

**FR-1: Surface Preparation Compliance**
- Surface preparation procedures shall define methods to achieve the surface cleanliness and profile standards specified in DEL-26.01 (PR-5)
- Procedures shall address all surface preparation methods required:
  - Solvent cleaning (SSPC-SP 1)
  - Power tool cleaning (SSPC-SP 3, SP-11)
  - Abrasive blast cleaning (SSPC-SP 5, SP-6, SP-10)
- **Source:** DEL-26.01 (PR-5 Surface Preparation); Datasheet.md (Surface Preparation Procedures)
- **Rationale:** See Guidance.md (Surface Preparation Quality)
- **Verification:** See Procedure.md; walkthrough review per Verification section

**FR-2: Coating Application Compliance**
- Coating application procedures shall define methods to apply coating systems specified in DEL-26.01 to achieve specified dry film thickness (DFT) and quality standards
- Procedures shall address application methods:
  - Spray application (airless, conventional, plural component)
  - Brush and roller application (touch-up, small areas)
- **Source:** DEL-26.01 (PR-4 DFT, PR-6 Application Conditions); Datasheet.md (Coating Application Procedures)
- **Rationale:** See Guidance.md (Application Quality Control)
- **Verification:** See Procedure.md; trial run or walkthrough per Verification section

**FR-3: Environmental Controls**
- Procedures shall define methods to monitor and control environmental conditions during coating application to meet manufacturer requirements and DEL-26.01 (PR-6):
  - Ambient temperature (min/max per manufacturer)
  - Relative humidity (typically ≤ 85% RH)
  - Surface temperature (min 3°C above dew point)
  - Wind conditions (spray application limits)
- **Source:** DEL-26.01 (PR-6 Application Conditions); Datasheet.md (Environmental Monitoring and Control)
- **Rationale:** See Guidance.md (Environmental Sensitivity)
- **Verification:** See Procedure.md; include environmental monitoring steps

**FR-4: Safety and HSE Compliance**
- Procedures shall define safety controls and personal protective equipment (PPE) for coating operations:
  - Confined space entry (tank internals)
  - Respiratory protection (blasting, coating application)
  - Fall protection (elevated work)
  - Fire prevention (flammable coatings)
  - Ventilation (VOC control)
  - Hot work permits (as applicable)
- **Source:** **ASSUMPTION** — WorkSafeBC requirements and PKG-33 (HSE Management); Datasheet.md (Safety and Environmental Controls)
- **Rationale:** See Guidance.md (Worker Safety)
- **Verification:** Safety review (JSA/HAZOP) per Verification section

### Performance Requirements

**PR-1: Inspection and Hold Points**
- Procedures shall define inspection hold points and acceptance criteria at critical stages:
  - **Surface preparation hold point:** Surface cleanliness and profile verification before coating application
  - **Inter-coat hold points:** DFT and cure time verification between coats
  - **Final acceptance hold point:** DFT, adhesion, holiday detection (if applicable), and visual inspection before final acceptance
- Acceptance criteria shall reference DEL-26.01 requirements
- **Source:** DEL-26.01 (QR-1 Inspection and Testing); Datasheet.md (Inspection and Acceptance)
- **Rationale:** Hold points prevent non-conforming work from progressing
- **Verification:** See Procedure.md; verify hold points defined in procedures

**PR-2: Documentation and Record Keeping**
- Procedures shall define documentation requirements during surface preparation and coating application:
  - Surface preparation records (environmental conditions, cleanliness acceptance, profile measurement)
  - Application records (environmental conditions, batch/lot numbers, WFT/DFT measurements, cure times)
  - Inspection records (DFT, adhesion, holiday detection, visual inspection)
- Record formats per DEL-26.04
- **Source:** DEL-26.01 (QR-2 Documentation); Datasheet.md (Documentation and Records)
- **Rationale:** Documentation provides traceability and evidence of compliance
- **Verification:** See Procedure.md; verify documentation steps included

**PR-3: Material Handling and Storage**
- Procedures shall define coating material handling requirements:
  - Storage conditions (temperature control per manufacturer)
  - Material mixing (pot life, induction time, mixing ratios per manufacturer data sheet)
  - Batch/lot number tracking
  - Waste disposal per project environmental plan
- **Source:** **ASSUMPTION** — Manufacturer data sheets (DEL-26.03); Datasheet.md (Material Handling)
- **Rationale:** Proper material handling ensures coating performance
- **Verification:** See Procedure.md; verify material handling steps included

**PR-4: Quality Control Steps**
- Procedures shall define quality control steps during application:
  - Wet film thickness (WFT) measurement to control DFT
  - DFT measurement frequency and acceptance per DEL-26.01 and SSPC-PA 2
  - Visual inspection for defects (runs, sags, holidays, contamination)
  - Inter-coat timing verification (minimum/maximum recoat windows per manufacturer)
  - Cure time before handling or service
- **Source:** DEL-26.01 (QR-1); Datasheet.md (Quality Control During Application)
- **Rationale:** In-process quality control prevents defects
- **Verification:** See Procedure.md; verify QC steps included

### Interface Requirements

**IR-1: Specification Compliance (DEL-26.01)**
- All procedures shall implement the requirements specified in DEL-26.01 (Coating Technical Specification)
- Procedures shall reference DEL-26.01 for coating system requirements, surface preparation standards, DFT requirements, and acceptance criteria
- **Source:** Decomposition deliverable relationships; DEL-26.01 (IR-4)
- **Rationale:** DEL-26.01 defines requirements; this deliverable defines implementation methods
- **Verification:** See Procedure.md; cross-check procedures against DEL-26.01 requirements

**IR-2: Material Data Sheets (DEL-26.03)**
- Procedures shall reference manufacturer data sheets for specific coating products (surface preparation requirements, application requirements, environmental limits, cure times, pot life, mixing ratios)
- Manufacturer data sheets provided in DEL-26.03
- **Source:** Datasheet.md (References — Manufacturer data sheets)
- **Rationale:** Procedures must be compatible with manufacturer recommendations
- **Verification:** See Procedure.md; verify manufacturer data sheet references

**IR-3: Records and Documentation (DEL-26.04)**
- Procedures shall use record templates defined in DEL-26.04 (Coating Installation & Test Records)
- Procedures shall define what records are generated and when
- **Source:** Datasheet.md (Cross-references — DEL-26.04)
- **Rationale:** Consistent record keeping per project standards
- **Verification:** See Procedure.md; verify record templates referenced

**IR-4: HSE Procedures (PKG-33)**
- Coating procedures shall be consistent with project HSE procedures:
  - Confined space entry procedures
  - Hot work permit procedures
  - Respiratory protection program
  - Fall protection procedures
  - Environmental controls (VOC management, waste disposal)
- **Source:** Datasheet.md (Cross-references — PKG-33); **ASSUMPTION**
- **Rationale:** Coating work must comply with project HSE requirements
- **Verification:** See Procedure.md; HSE review and coordination

**IR-5: Confined Space Coordination (Tank Internals)**
- Tank internal coating procedures shall coordinate with confined space entry requirements (access, ventilation, emergency procedures)
- Coordinate with PKG-13 (tank design) and PKG-30 (commissioning)
- **Source:** Datasheet.md (Hazardous Area and Safety Context — Confined space entry)
- **Rationale:** Tank internal coating requires confined space entry protocols
- **Verification:** See Procedure.md; confined space entry coordination

### Quality Requirements

**QR-1: Procedure Content Requirements**
- Each procedure shall include:
  - **Purpose:** What the procedure accomplishes
  - **Scope:** What applications/areas the procedure covers
  - **Prerequisites:** Required conditions before starting (upstream work complete, materials available, environmental conditions acceptable)
  - **Equipment and materials:** Tools, equipment, and materials required
  - **Safety and PPE:** Safety precautions, PPE requirements, permits required
  - **Steps:** Detailed step-by-step instructions
  - **Quality control:** Inspection points, hold points, acceptance criteria
  - **Documentation:** Records to be completed
  - **References:** Related specifications (DEL-26.01), data sheets (DEL-26.03), record forms (DEL-26.04)
- **Source:** **ASSUMPTION** — Standard procedure format; Guidance.md (Procedure Structure)
- **Rationale:** Consistent procedure format ensures usability
- **Verification:** See Procedure.md; verify procedure content checklist

**QR-2: Competency and Training**
- Procedures shall identify required personnel qualifications:
  - Coating applicators: **TBD** — Industry certification or equivalent (e.g., NACE/AMPP, SSPC)
  - Coating inspectors: **TBD** — NACE/AMPP Coating Inspector Level 2 or equivalent recommended
  - Confined space attendants (tank internals): Per confined space entry training
- Procedures shall be reviewed during training and competency verification
- **Source:** DEL-26.01 (QR-3 Workmanship); **ASSUMPTION**
- **Rationale:** Qualified personnel ensure procedure execution quality
- **Verification:** See Procedure.md; competency verification

**QR-3: Procedure Verification and Approval**
- Procedures shall be verified before use:
  - Walkthrough or tabletop review
  - Safety review (Job Safety Analysis / JSA or HAZOP as applicable)
  - Trial run (where practical)
- Procedures shall be approved by authorized personnel before issuance
- **Source:** Specification Verification section; **ASSUMPTION** — Standard procedure approval process
- **Rationale:** Verification prevents procedural errors and safety hazards
- **Verification:** See Procedure.md; procedure approval workflow

## Standards

**Applicable codes and standards:**

### Primary Standards (Referenced by Procedures)

**SSPC — The Society for Protective Coatings**
- Surface preparation standards (SP series): SP-1, SP-3, SP-5, SP-6, SP-10, SP-11
- Application/inspection standards (PA series): PA-2, PA-17
- Visual standards: VIS-1
- **Source:** DEL-26.01 (Standards section); Datasheet.md (Applicable Standards)

**NACE/AMPP — NACE International (now part of AMPP)**
- Coating inspector certification and training standards
- Corrosion control best practices
- **Source:** DEL-26.01 (Standards section)

**ISO 12944 — Paints and varnishes — Corrosion protection of steel structures**
- Part 4: Types of surface and surface preparation (guidance)
- **Source:** DEL-26.01 (Standards section)

**ASTM Standards**
- ASTM D3359: Adhesion testing (cross-hatch tape test)
- ASTM D4417: Surface profile measurement
- **Source:** DEL-26.01 (Standards section)

**Manufacturer Data Sheets**
- Product data sheets for coating materials specified in DEL-26.01
- Surface preparation requirements, application instructions, environmental limits, cure times, pot life
- **Source:** DEL-26.03 (Coating Data Sheet Package)

### Safety and Environmental Standards

**WorkSafeBC Regulations**
- Confined space entry
- Respiratory protection
- Fall protection
- Hot work
- **Source:** Datasheet.md (Cross-references — PKG-33)

**Project HSE Procedures (PKG-33)**
- Project-specific HSE procedures and work permit systems
- **Source:** Datasheet.md (Cross-references — PKG-33)

**VOC Regulations**
- Provincial and federal air quality regulations
- **Source:** DEL-26.01 (Guidance — Regulatory Context)

### Project-Specific Requirements

**DEL-26.01 (Coating Technical Specification)**
- Primary upstream requirement defining coating systems, surface preparation standards, DFT requirements, acceptance criteria
- **Source:** Decomposition deliverable relationships

**Project Quality Management Plan**
- Quality procedures and documentation requirements
- **Source:** **ASSUMPTION**

**Project Document Control Procedures**
- Document numbering, revision control, distribution
- **Source:** **ASSUMPTION**

## Verification

**Verification methods:**

### Document Review

**Technical review:**
- Coatings discipline lead review for technical accuracy and completeness
- Verify all coating types from DEL-26.01 are covered by procedures
- Verify all SSPC surface preparation standards from DEL-26.01 are addressed
- Verify all safety and environmental controls are included

**Interdisciplinary review:**
- **PKG-13 (Storage Tanks):** Tank internal coating procedures (access, confined space)
- **PKG-06 (Structural Steelwork):** Shop vs. field coordination
- **PKG-33 (HSE Management):** Safety procedures (confined space, hot work, respiratory protection, fall protection)
- **PKG-30 (Commissioning):** Tank internal coating acceptance procedures

**QA/QC review:**
- Verify procedures reference DEL-26.01 requirements correctly
- Verify hold points and acceptance criteria align with DEL-26.01
- Verify record requirements align with DEL-26.04

### Procedure Walkthrough / Tabletop Review

**Purpose:** Verify procedures are complete, logical, and executable

**Method:**
- Walk through each procedure step-by-step with personnel who will execute the procedure
- Identify missing steps, unclear instructions, safety hazards, or impractical requirements
- Revise procedures based on walkthrough findings

**Source:** **ASSUMPTION** — Standard procedure verification method

### Safety Review

**Purpose:** Verify procedures include adequate safety controls and comply with project HSE requirements

**Method:**
- Job Safety Analysis (JSA) or HAZOP review for each procedure
- Identify hazards and verify controls are defined
- Verify PPE requirements are specified
- Verify permit requirements (confined space, hot work) are identified
- Coordinate with PKG-33 (HSE Management) for HSE procedure compliance

**Source:** **ASSUMPTION** — Standard safety review; Datasheet.md (Cross-references — PKG-33)

### Trial Run (Where Practical)

**Purpose:** Verify procedures are executable in actual field conditions

**Method:**
- Perform trial run of procedures (or portions of procedures) on representative surfaces
- Verify steps are clear and achievable
- Verify quality control steps are effective
- Verify environmental monitoring and controls are adequate
- Revise procedures based on trial run findings

**Source:** **ASSUMPTION** — Best practice for critical or novel procedures

**Note:** Trial runs may not be practical for all procedures but should be considered for:
- Tank internal coating procedures (complex confined space work)
- Novel application methods or materials
- Procedures with high safety risk

### Competency Verification

**Purpose:** Verify personnel are competent to execute procedures

**Method:**
- Review personnel qualifications (certifications, training, experience)
- Conduct procedure training and competency assessment
- Verify understanding of critical steps, hold points, and safety requirements

**Source:** **ASSUMPTION** — Standard competency verification

### Acceptance Criteria

**Coating procedures are acceptable when:**

- ✓ All anticipated artifacts produced per Decomposition DEL-26.02:
  - Surface preparation procedures (covering all SSPC standards required by DEL-26.01)
  - Coating application procedures (covering all coating types specified by DEL-26.01)
- ✓ All procedures implement DEL-26.01 requirements (coating systems, surface prep standards, DFT, acceptance criteria)
- ✓ All procedures include required content (purpose, scope, prerequisites, equipment, safety, steps, QC, documentation, references)
- ✓ All safety controls defined (confined space, respiratory protection, fall protection, hot work, ventilation)
- ✓ All inspection hold points and acceptance criteria defined and aligned with DEL-26.01
- ✓ All documentation requirements defined and aligned with DEL-26.04
- ✓ All reviews complete (technical, interdisciplinary, QA/QC, safety)
- ✓ Walkthrough or tabletop review complete with findings addressed
- ✓ Safety review (JSA/HAZOP) complete with findings addressed
- ✓ Trial run complete (if applicable) with findings addressed
- ✓ Personnel competency verification complete
- ✓ Procedures approved by authorized personnel
- ✓ Procedures issued and distributed per project document control procedures

**Source:** Procedure.md (Verification — Deliverable Acceptance Criteria)

## Documentation

**Required documentation outputs:**

This deliverable shall produce the following procedure documents:

### 1. Surface Preparation Procedures

**Content:**
- **Purpose and scope:** Surface preparation to meet DEL-26.01 standards
- **Applications:** Tank internals, tank externals, structural steel, marine structures (per DEL-26.01 coating types)
- **Methods:**
  - Solvent cleaning (SSPC-SP 1)
  - Power tool cleaning (SSPC-SP 3, SP-11)
  - Abrasive blast cleaning (SSPC-SP 5, SP-6, SP-10)
- **Equipment and materials:** Blast equipment, abrasives, power tools, solvents
- **Safety and PPE:** Respiratory protection, hearing protection, fall protection, confined space entry, dust control
- **Steps:** Detailed step-by-step instructions for each surface preparation method
- **Quality control and hold points:** Surface cleanliness and profile inspection, acceptance criteria per DEL-26.01
- **Documentation:** Surface preparation records (DEL-26.04)
- **References:** DEL-26.01 (surface prep standards), SSPC standards, manufacturer data sheets (DEL-26.03)

**Source:** Decomposition DEL-26.02 anticipated artifacts; Datasheet.md (Surface Preparation Procedures)

### 2. Coating Application Procedures

**Content:**
- **Purpose and scope:** Coating application to meet DEL-26.01 requirements
- **Applications:** Tank internal coatings, tank external coatings, structural steel coatings, marine coatings, field painting (per DEL-26.01 coating types)
- **Methods:**
  - Spray application (airless, conventional, plural component)
  - Brush and roller application (touch-up, small areas)
- **Equipment and materials:** Spray equipment, coating materials, mixing equipment, environmental monitoring equipment
- **Safety and PPE:** Respiratory protection, fire prevention, confined space entry, ventilation, fall protection
- **Environmental monitoring and control:** Temperature, humidity, dew point, surface temperature, wind (limits per DEL-26.01 PR-6)
- **Material handling:** Storage, mixing, pot life, batch tracking, waste disposal
- **Steps:** Detailed step-by-step instructions for coating application (each coating type)
- **Quality control and hold points:** WFT/DFT measurement, visual inspection, inter-coat timing, cure time, acceptance criteria per DEL-26.01
- **Final inspection and testing:** DFT, adhesion, holiday detection (immersion service), visual inspection
- **Documentation:** Application records, DFT records, adhesion test records, holiday detection records (DEL-26.04)
- **References:** DEL-26.01 (coating systems, DFT requirements, acceptance criteria), manufacturer data sheets (DEL-26.03), SSPC-PA 2, ASTM D3359

**Source:** Decomposition DEL-26.02 anticipated artifacts; Datasheet.md (Coating Application Procedures)

### Documentation Format

**Document numbering:** **TBD** — per project document control procedures
**Revision control:** Per project document management system
**Format standard:** **TBD** — project procedure template
**Review and approval records:** Per project quality procedures

**Metadata requirements:**
- Deliverable ID: DEL-26.02
- Procedure number(s): **TBD**
- Revision history with dates and descriptions
- Originator, reviewer, approver signatures and dates

**Source:** **ASSUMPTION** — Standard procedure documentation

### Document Relationships

**Implements:**
- **DEL-26.01** (Coating Technical Specification) — These procedures implement DEL-26.01 requirements

**References:**
- **DEL-26.03** (Coating Data Sheet Package) — Manufacturer data sheets for coating products
- **DEL-26.04** (Coating Installation & Test Records) — Record templates used by these procedures
- **PKG-33** (HSE Management) — Safety procedures (confined space entry, hot work, respiratory protection, fall protection)

**Produces (when executed):**
- Surface preparation records (filed in DEL-26.04)
- Coating application records (filed in DEL-26.04)
- Inspection and test records (filed in DEL-26.04)

**Source:** Decomposition Section 5 (package and deliverable structure); Datasheet.md (Cross-references)

**Distribution:**
- Coating applicators and supervisors (procedure users)
- QA/QC inspectors (for inspection procedures and hold points)
- HSE personnel (for safety review)
- DEL-26.04 records coordinator (for record keeping)
- Related discipline leads (PKG-13, PKG-06, PKG-33)

**Source:** **ASSUMPTION** — Typical procedure distribution
