# Procedure: DEL-05.02 Concrete Structures Technical Specification

## Purpose

Draft, review, and control the **Concrete Structures Technical Specification** for PKG-05, ensuring the specification:
- Defines performance, materials, and workmanship requirements per Employer's Requirements
- Supports construction quality and QA/QC verification
- Maintains consistency with design drawings (DEL-05.01), design calculations (DEL-05.03), and enables generation of installation & test records (DEL-05.04)
- Meets project document control and quality management requirements
(Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:233; Specification.md: Scope.)

## Prerequisites

### P-01: Dependencies (Coordinated Externally — NOT_TRACKED Mode)

Dependencies are coordinated externally by humans (see `_DEPENDENCIES.md` and `execution/_Coordination/_COORDINATION.md`). Confirm inputs from related deliverables to ensure specification consistency:

**Drawing set inputs (from DEL-05.01):**
- Drawing notes and details (material properties, cover requirements, tolerances)
- General notes (concrete strength by element type, exposure class terminology, finish designations)
- Typical details (joint details, embedment details, reinforcement details)
- Coordinate specification terminology with drawing terminology for consistency

**Design calculation inputs (from DEL-05.03):**
- Concrete strength requirements by element type (tank foundations, containment walls, equipment pads, thrust blocks)
- Material property assumptions (concrete modulus, unit weight, Poisson's ratio)
- Design parameters (cover requirements, seismic detailing requirements)
- Coordinate specification values with calculation assumptions

**Installation & test records interface (to DEL-05.04):**
- Ensure specification inspection/testing requirements enable record generation (pour records, cylinder test results, rebar inspection records)
- Provide clear acceptance criteria and documentation requirements
- Define hold points and verification methods

**Interdisciplinary interface inputs (TBD pending IDC):**
- Equipment anchor bolt requirements (PKG-10, PKG-11, PKG-13, PKG-15)
- Pipe sleeve and penetration requirements (PKG-14)
- Electrical embedment requirements (PKG-17)
- Instrumentation penetration requirements (PKG-20)
- Drainage penetration requirements (PKG-03)

(Source: `_DEPENDENCIES.md`; test/execution/_Coordination/_COORDINATION.md; test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:232; test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:234; test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:235; Specification.md: IR-01; Specification.md: IR-02.)

### P-02: Reference Materials

**Employer's Requirements (clause locations TBD):**
- Volume 2 Part 1: General Requirements (document control, QA/QC requirements, quality management)
- Volume 2 Part 2: Civil & Process Mechanical Works (concrete requirements, durability requirements, materials requirements, inspection/testing requirements)
- Volume 2 Part 3: Building Works (if applicable to PKG-05 scope)
(Source: execution/PKG-05_Concrete_Structures/0_References/_REFERENCE_INDEX.md; test/Volume_2_Part_1_Employers_Requirements.pdf, location TBD; test/Volume_2_Part_2_Employers_Requirements.pdf, location TBD.)

**Design basis documents (TBD):**
- Project design basis memorandum
- Geotechnical investigation report (from PKG-02) — bearing capacity, soil properties
- Environmental exposure assessment (freeze-thaw, marine exposure, sulfates, chlorides)
- Seismic design parameters
- Load combinations and design standards

**Applicable codes and standards (TBD extraction from ERs):**
- Concrete materials and testing standard (likely CSA A23.1)
- Concrete design standard (likely CSA A23.3)
- Reinforcing steel standard (likely CSA G30.18)
- Building code (likely BC Building Code / NBCC)
- Quality assurance standards
- Testing standards (ASTM or CSA)

(Source: Specification.md: Standards; Datasheet.md: Attributes.)

### P-03: Scope Baseline

Confirm PKG-05 scope and anticipated specification artifacts:
- **Package scope:** Foundations, containment walls, equipment pads, thrust blocks, ground liner system
- **Anticipated artifacts:** Concrete specification, reinforcement specification, formwork specification
- **Project objectives:** OBJ-3 (Storage Capacity 45,000 MT), OBJ-7 (Environmental Protection)
- **Project context:** Canola Oil Transload Facility Phase 1, Fraser Surrey Terminal, Surrey, BC
(Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:226; test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:233; test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:782; test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:786; Datasheet.md: Conditions.)

### P-04: Document Control Conventions

Project document control requirements (TBD until conventions are established):
- Document numbering system
- Revision tracking and issue status management
- Approval workflow and signature requirements
- Distribution and access control
- Electronic submission requirements and formats
- Template or format standards for technical specifications
(Source: test/Volume_2_Part_1_Employers_Requirements.pdf, location TBD; Datasheet.md: Attributes; Specification.md: QR-01.)

## Steps

### Step 1: Confirm Scope and Objectives

**Actions:**
1. Review decomposition scope for PKG-05 (foundations, containment walls, equipment pads, thrust blocks, ground liner system).
2. Review anticipated specification artifacts (concrete, reinforcement, formwork).
3. Review project objectives (OBJ-3 Storage Capacity, OBJ-7 Environmental Protection) and identify how specification requirements support these objectives.
4. Identify scope boundaries (Contractor scope only; exclude Employer-responsible items except interfaces).
5. Create specification outline covering concrete, reinforcement, and formwork sections.

**Outputs:**
- Specification outline with section structure for concrete, reinforcement, and formwork
- Objectives mapping (identify durability and containment requirements that support OBJ-3 and OBJ-7)
- Scope boundary documentation

**Verification:**
- Specification outline covers all Specification FR-01 requirements (concrete, reinforcement, formwork)
- Objectives mapping aligns with Datasheet conditions (OBJ-3 and OBJ-7)
- Scope boundaries are clear and align with contractor responsibilities

(Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:226; test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:233; test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:782; test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:786; Specification.md: FR-01; Datasheet.md: Conditions; Guidance.md: P-02.)

### Step 2: Extract and Document Governing Requirements

**Actions:**
1. Identify governing Employer's Requirements clauses for concrete (materials, durability, inspection/testing).
2. Extract specific requirements from Volume 2 Part 2 concrete section:
   - Concrete strength requirements by element type
   - Durability/exposure requirements (exposure classes, w/c ratio limits, air entrainment, cover)
   - Material requirements (cement type, aggregate specifications, admixtures)
   - Quality control requirements (testing frequencies, acceptance criteria, sampling procedures)
   - Special requirements for containment structures (joints, waterstops, liner interfaces)
3. Extract document control and QA/QC requirements from Volume 2 Part 1.
4. Identify applicable codes and standards referenced in Employer's Requirements.
5. Document requirements extraction in a traceability matrix (requirement → ER source → specification section).
6. Flag any unconfirmed requirements or standards as **TBD** with source citation.
7. Apply Guidance Principle P-04 (Evidence-Based Standards).

**Outputs:**
- Requirements traceability matrix (Employer's Requirements → specification requirements)
- Extracted durability/exposure requirements
- Extracted material and quality control requirements
- Applicable codes and standards list
- TBD list for missing or unconfirmed requirements

**Verification:**
- All specification requirements are traceable to Employer's Requirements or project design basis
- Durability requirements address BC coastal environment (freeze-thaw, marine exposure if applicable)
- Containment requirements support OBJ-7 Environmental Protection
- Standards are sourced from ERs (not invented or assumed without citation)

(Source: test/Volume_2_Part_2_Employers_Requirements.pdf, location TBD; test/Volume_2_Part_1_Employers_Requirements.pdf, location TBD; Specification.md: FR-03; Specification.md: Standards; Guidance.md: P-02; Guidance.md: P-04.)

### Step 3: Draft Concrete Specification Section

**Actions:**
1. Draft concrete specification section following Specification requirements FR-02 through FR-06:
   - Materials (cement, aggregates, water, admixtures, certifications)
   - Mix design (strength requirements, durability requirements, exposure classes, proportioning)
   - Delivery and placement (delivery requirements, placement procedures, consolidation, joints)
   - Finishing and curing (finishing requirements, curing methods, protection, seasonal requirements)
   - Quality control (testing frequencies, acceptance criteria, sampling procedures, defect repair)
2. Organize content by exposure class (durability-first framing per Guidance P-02).
3. Use "shall" statements with measurable acceptance criteria and verification methods (Guidance P-01).
4. Emphasize containment-related requirements (joints, waterstops, liner interfaces) per Guidance P-03.
5. Address BC coastal environment requirements (freeze-thaw, marine exposure, seasonal construction) per Guidance C-05.
6. Ensure requirements enable generation of DEL-05.04 pour records and cylinder test results per Specification FR-06.
7. Coordinate with DEL-05.01 drawing notes for terminology consistency per Guidance P-05.

**Outputs:**
- Concrete specification section draft covering materials, mix design, placement, finishing, curing, and quality control
- Exposure class definitions and durability requirements
- Testing frequencies and acceptance criteria
- Hold points and inspection requirements
- Special requirements for containment structures

**Verification:**
- Concrete specification covers all Specification FR-02 through FR-06 requirements
- Durability requirements are organized by exposure class (Guidance P-02)
- Requirements have clear acceptance criteria and verification methods (Guidance P-01)
- Containment requirements support OBJ-7 (Guidance P-03)
- Requirements enable DEL-05.04 record generation (Specification FR-06)

(Source: Specification.md: FR-02 through FR-06; Guidance.md: P-01; Guidance.md: P-02; Guidance.md: P-03; Guidance.md: C-05; Datasheet.md: Construction.)

### Step 4: Draft Reinforcement Specification Section

**Actions:**
1. Draft reinforcement specification section following Specification requirements FR-07 through FR-09:
   - Materials (reinforcing steel grades/types, certifications, epoxy coating if required, storage/protection)
   - Fabrication (bending tolerances, cutting, threading, bar marking)
   - Placement (tolerances for cover/spacing/location, support requirements, lap splices, mechanical couplers, welding if applicable)
   - Inspection (placement inspection, cover verification, hold points, acceptance criteria)
2. Use "shall" statements with measurable tolerances and verification methods (Guidance P-01).
3. Address constructability (reinforcement congestion, bar sizes/spacing) per Guidance C-03.
4. Specify hold points before concrete placement (Guidance C-04).
5. Ensure requirements enable generation of DEL-05.04 rebar inspection records per Specification FR-09.
6. Coordinate with DEL-05.01 reinforcement drawings for consistency (bar marks, lap splice requirements).

**Outputs:**
- Reinforcement specification section draft covering materials, fabrication, placement, and inspection
- Placement tolerances and support requirements
- Lap splice and mechanical coupler requirements
- Hold points and inspection procedures
- Acceptance criteria for reinforcement placement

**Verification:**
- Reinforcement specification covers all Specification FR-07 through FR-09 requirements
- Requirements have clear tolerances and verification methods (Guidance P-01)
- Constructability is considered (reinforcement congestion, bar placement) (Guidance C-03)
- Hold points are explicit and actionable (Guidance C-04)
- Requirements enable DEL-05.04 record generation (Specification FR-09)

(Source: Specification.md: FR-07 through FR-09; Guidance.md: P-01; Guidance.md: C-03; Guidance.md: C-04; Datasheet.md: Construction.)

### Step 5: Draft Formwork Specification Section

**Actions:**
1. Draft formwork specification section following Specification requirements FR-10 through FR-12:
   - Materials and design (formwork materials, design requirements, coatings/release agents, cleaning/reuse)
   - Tolerances and finishes (dimensional tolerances, surface finish requirements by element type, chamfers/features, acceptance criteria)
   - Embedded items and removal (embedded item installation, coordinate with other disciplines, formwork removal procedures/timing, re-shoring, inspection hold points)
2. Use "shall" statements with measurable tolerances and verification methods (Guidance P-01).
3. Coordinate embedded item requirements with interdisciplinary interfaces per Prerequisite P-01 (PKG-14, PKG-17, PKG-20, etc.).
4. Balance tolerance tightness with constructability per Guidance Trade-off T-03.
5. Specify hold points for formwork inspection before concrete placement (Guidance C-04).
6. Coordinate with DEL-05.01 drawing finish designations for consistency (Guidance P-05).

**Outputs:**
- Formwork specification section draft covering materials, tolerances, finishes, embedded items, and removal
- Dimensional tolerances and surface finish requirements
- Embedded item installation requirements and coordination notes
- Formwork removal procedures and timing
- Hold points and inspection requirements

**Verification:**
- Formwork specification covers all Specification FR-10 through FR-12 requirements
- Tolerances are feasible and appropriate to interface requirements (Guidance T-03)
- Embedded item requirements coordinate with other disciplines (Specification IR-02, Guidance C-02)
- Hold points are explicit and actionable (Guidance C-04)
- Finish designations are consistent with DEL-05.01 (Guidance P-05)

(Source: Specification.md: FR-10 through FR-12; Guidance.md: P-01; Guidance.md: P-05; Guidance.md: C-02; Guidance.md: C-04; Guidance.md: T-03; Datasheet.md: Construction.)

### Step 6: Add Quality Control and Documentation Requirements

**Actions:**
1. Add comprehensive quality control section covering:
   - Inspection frequencies, hold points, and acceptance criteria for concrete, reinforcement, and formwork (Specification QR-02)
   - Testing frequencies and acceptance criteria for concrete quality control (Specification FR-06)
   - Documentation requirements for inspections and tests (enable DEL-05.04 record generation)
   - Non-conformance reporting and corrective action procedures
   - Retention of QA/QC records
2. Specify concrete testing requirements:
   - Slump testing (frequency, acceptance range)
   - Air content testing (frequency, acceptance range for freeze-thaw protection)
   - Concrete temperature testing (frequency, limits for hot/cold weather)
   - Cylinder sampling (frequency, handling/curing procedures, testing ages, acceptance criteria)
3. Specify reinforcement inspection requirements:
   - Placement inspection (cover, spacing, lap splices, support, cleanliness)
   - Hold point before concrete placement (Guidance C-04)
   - Documentation requirements (rebar inspection records for DEL-05.04)
4. Specify formwork inspection requirements:
   - Form inspection before concrete placement (dimensions, cleanliness, release agent, embedded items)
   - Hold point before concrete placement (Guidance C-04)
   - Documentation requirements
5. Coordinate inspection terminology with DEL-05.01 and DEL-05.04 for consistency (Guidance P-05).
6. Apply Guidance Principle P-01 (clear acceptance criteria and verification methods).
7. Consider Trade-off T-04 (inspection frequency vs schedule/cost) when specifying frequencies.

**Outputs:**
- Quality control section covering inspection and testing requirements
- Testing frequencies and acceptance criteria for concrete
- Inspection requirements and hold points for reinforcement and formwork
- Documentation requirements that enable DEL-05.04 record generation
- Non-conformance and corrective action procedures

**Verification:**
- Quality control requirements cover all Specification QR-02 and FR-06, FR-09 requirements
- Requirements enable generation of DEL-05.04 records (pour records, cylinder test results, rebar inspection records)
- Hold points are explicit and tied to acceptance criteria (Guidance P-01, Guidance C-04)
- Terminology is consistent with DEL-05.01 and DEL-05.04 (Guidance P-05)
- Testing/inspection frequencies are appropriate to project quality priorities (Guidance T-04)

(Source: Specification.md: FR-06; Specification.md: FR-09; Specification.md: QR-02; test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:235; Guidance.md: P-01; Guidance.md: P-05; Guidance.md: C-04; Guidance.md: T-04.)

### Step 7: Conduct Reviews and Incorporate Comments

**Actions:**
1. **Originator self-check:** Review specification for completeness, accuracy, consistency, and traceability to Employer's Requirements.
   - Verify all anticipated artifacts are present (concrete, reinforcement, formwork) per Specification FR-01
   - Verify all requirements are traceable to Employer's Requirements or design basis (Step 2 traceability matrix)
   - Verify requirements have clear acceptance criteria and verification methods (Guidance P-01)
   - Verify terminology is consistent within specification and with DEL-05.01 (Guidance P-05)
   - Verify document control metadata matches Datasheet (Specification QR-01)

2. **Independent/peer review:** Technical review by independent reviewer (not the originator).
   - Review technical adequacy of requirements (durability, materials, workmanship)
   - Review alignment with applicable codes and standards (Specification Standards)
   - Review constructability of specified requirements (Guidance C-03)
   - Review consistency with DEL-05.01 and DEL-05.03 (Specification IR-01)
   - Document review comments and required actions

3. **Interdisciplinary check (IDC):** Coordinate with related deliverables to verify consistency.
   - DEL-05.01: Verify specification terminology and values align with drawing notes
   - DEL-05.03: Verify material properties and strengths align with calculation assumptions
   - DEL-05.04: Verify inspection/testing requirements enable record generation
   - Interdisciplinary packages: Verify embedded item and interface requirements align (PKG-14, PKG-17, PKG-20, etc.)
   - Document IDC comments and required actions

4. **QA review:** Quality assurance review per project QA/QC requirements (**TBD** specific checklists).
   - Review compliance with Employer's Requirements
   - Review document control compliance (numbering, revision, approvals)
   - Review completeness of quality control requirements
   - Document QA review findings and required actions

5. **Incorporate comments:** Address all review and IDC comments.
   - Update specification to incorporate accepted comments
   - Document comment resolution (accept, reject with justification, or carry forward as TBD)
   - Re-review specification if significant changes are made

**Outputs:**
- Originator check report with findings and resolutions
- Peer review report with comments and resolutions
- IDC comment log with actions and closures
- QA review report with findings and resolutions
- Updated specification incorporating review comments
- Comment resolution log

**Verification:**
- All Specification requirements (FR-01 through QR-03) are verified by reviews
- All interfaces with related deliverables (DEL-05.01, DEL-05.03, DEL-05.04) are verified by IDC
- All review comments are addressed and documented
- Specification is consistent and traceable to Employer's Requirements

(Source: Specification.md: FR-01; Specification.md: IR-01; Specification.md: QR-01; test/Volume_2_Part_1_Employers_Requirements.pdf, location TBD; Guidance.md: P-01; Guidance.md: P-05.)

### Step 8: Finalize and Issue Specification

**Actions:**
1. Finalize specification document and update revision status per project document control.
2. Apply document control metadata (document number, revision, approval signatures, issue date).
3. Generate issue copies per project requirements (PDF, editable format **TBD**).
4. Assemble issue package:
   - Specification document (concrete, reinforcement, formwork sections)
   - Supporting documentation (inspection/testing plan, QC checklists/templates if applicable **TBD**)
5. Assemble QA/QC records:
   - Originator check records
   - Peer review records
   - IDC records and comment log
   - QA review records
   - Comment resolution log
   - Requirements traceability matrix
6. Update Datasheet metadata (document number, revision, status).
7. Submit issue package per project document control process (electronic submission requirements **TBD**).
8. Update `_STATUS.md` to next lifecycle state per project process (e.g., IN_PROGRESS → CHECKING → ISSUED).

**Outputs:**
- Issued specification document (PDF and editable format)
- Supporting documentation (inspection/testing plan, QC checklists if applicable)
- QA/QC records package
- Requirements traceability matrix
- Updated Datasheet and `_STATUS.md`

**Verification:**
- Specification document is complete and includes all required sections (concrete, reinforcement, formwork)
- Document control metadata is complete and consistent with Datasheet
- All required QA/QC records are assembled and complete
- Issue package meets project document control and submission requirements
- `_STATUS.md` lifecycle state is updated appropriately

(Source: Specification.md: Documentation; Datasheet.md: Attributes; test/Volume_2_Part_1_Employers_Requirements.pdf, location TBD.)

## Verification

### Completeness Verification (Maps to Specification Verification)

**Specification artifacts present and complete:**
- Concrete specification section (materials, mix design, placement, finishing, curing, quality control) — Specification FR-02 through FR-06
- Reinforcement specification section (materials, fabrication, placement, inspection) — Specification FR-07 through FR-09
- Formwork specification section (materials, tolerances, finishes, embedded items, removal) — Specification FR-10 through FR-12

**Verification method:** Review specification content against Specification FR-01 and Datasheet Construction artifacts. Confirm each anticipated artifact is present and includes requirements, acceptance criteria, and verification methods. (Source: Specification.md: FR-01; Datasheet.md: Construction; Procedure Step 1.)

### Alignment Verification (Maps to Specification Verification)

**Cross-deliverable consistency:**
- Specification terminology and values align with DEL-05.01 (drawing notes, general notes, finish designations) — Specification IR-01, QR-03
- Material properties and strengths align with DEL-05.03 (calculation assumptions) — Specification IR-01
- Inspection/testing requirements enable generation of DEL-05.04 (pour records, cylinder test results, rebar inspection records) — Specification IR-01

**Verification method:** Conduct IDC process (Step 7.3) to confirm alignment with DEL-05.01, DEL-05.03, and DEL-05.04. Document alignment verification in IDC comment log. (Source: Specification.md: IR-01; Specification.md: QR-03; Procedure Step 7.3.)

### Requirements Traceability Verification (Maps to Specification Verification)

**Traceability to source:**
- All specification requirements are traceable to Employer's Requirements or project design basis (Step 2 traceability matrix)
- Durability requirements address BC coastal environment (freeze-thaw, marine exposure if applicable) — Specification FR-03, PR-01
- Containment requirements support OBJ-7 Environmental Protection — Specification PR-03
- Equipment interface requirements support construction and installation quality — Specification PR-02

**Verification method:** Review requirements traceability matrix (Step 2 output) to verify each requirement has source citation. Review requirements content against Employer's Requirements extracts. (Source: Specification.md: FR-03; Specification.md: PR-01; Specification.md: PR-02; Specification.md: PR-03; Procedure Step 2.)

### Quality Verification (Maps to Specification Verification)

**Quality and consistency:**
- Terminology is consistent within specification and with DEL-05.01 and DEL-05.04 — Specification QR-03
- Requirements have clear acceptance criteria and verification methods — Guidance P-01
- Document control metadata matches Datasheet — Specification QR-01
- Peer/QA reviews are complete with findings addressed — Specification Verification

**Verification method:** Originator check (Step 7.1), peer review (Step 7.2), and QA review (Step 7.4) confirm quality and consistency. Review comment resolution log confirms all findings are addressed. (Source: Specification.md: QR-01; Specification.md: QR-03; Datasheet.md: Attributes; Guidance.md: P-01; Procedure Steps 7.1, 7.2, 7.4.)

## Records

**Specification document deliverables:**
- Concrete specification section (materials, placement, curing, durability, quality control)
- Reinforcement specification section (materials, fabrication, placement, inspection)
- Formwork specification section (materials, tolerances, finishes, embedded items, removal)
(Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:233; Datasheet.md: Construction.)

**Supporting documentation:**
- Inspection and testing plan (frequencies, hold points, acceptance criteria) — may be included in specification or issued separately (**TBD**)
- Quality control checklists and forms (templates for DEL-05.04 records) — may be included or issued separately (**TBD**)
- Material certification requirements and templates
(Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:235; Specification.md: Documentation.)

**QA/QC records:**
- Requirements traceability matrix (Employer's Requirements → specification requirements)
- Originator check records (checklist, findings, resolutions)
- Peer review records (reviewer name, date, comments, resolutions)
- IDC records (deliverables coordinated, comments, closures)
- QA review records (findings, resolutions)
- Review comment/response log
- Check evidence per project QA/QC requirements (**TBD** specific forms/checklists)
(Source: test/Volume_2_Part_1_Employers_Requirements.pdf, location TBD; Specification.md: Documentation; Procedure Steps 2, 7.)

**Project records:**
- Issued specification document files (PDF and editable format)
- Document transmittal and submission records
- Updated Datasheet metadata
- Updated `_STATUS.md` lifecycle state
(Source: Specification.md: Documentation; Procedure Step 8.)

## Cross-Document Notes

- **Specification:** This Procedure's steps (Steps 1-8) and verifications demonstrate compliance with all Specification requirements (FR-01 through QR-03). Each Specification requirement is addressed by one or more Procedure steps and verified by corresponding verification checks. (Source: Specification.md: Requirements; Specification.md: Verification.)
- **Guidance:** Use Guidance Principles (P-01 through P-05), Considerations (C-01 through C-05), Trade-offs (T-01 through T-04), and Examples (E-01 through E-03) to inform how specification requirements are written. Guidance informs how to execute Steps 3, 4, 5, and 6 effectively. (Source: Guidance.md: Principles; Guidance.md: Considerations; Guidance.md: Trade-offs; Guidance.md: Examples.)
- **Datasheet:** Datasheet Construction section lists the anticipated artifacts that Steps 1, 3, 4, and 5 must produce. Datasheet Attributes define the metadata requirements that Steps 7 and 8 must implement. Datasheet Cross-Document Points identify the linkages this Procedure must maintain. (Source: Datasheet.md: Construction; Datasheet.md: Attributes; Datasheet.md: Cross-Document Points.)
