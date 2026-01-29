# Specification: DEL-31.02 As-Built Design Drawing Set

## Scope

This specification defines the requirements for **As-Built Design Drawing Set** within **PKG-31 Documentation & Deliverables**.

**Purpose:**
Defines and substantiates as-built drawings in accordance with Employer's Requirements (ER) and VFPA standards, documenting the facility as actually constructed.

**Source:** Decomposition DEL-31.02 (line 687)

**Scope Inclusions:**

The As-Built Design Drawing Set shall include:
- Final as-constructed drawings from all project disciplines (Civil, Structural, Mechanical, Process, Electrical, I&C, Marine, Buildings, Fire Protection)
- Construction markups and field changes incorporated into Record Drawings baseline (DEL-31.01)
- Actual field dimensions, locations, elevations, and configurations verified by survey and field measurement
- All approved design changes, RFIs, field orders, and construction change notices reflected
- Updated drawing registers and indices

**Scope Exclusions:**

- Record Design Drawings (covered under DEL-31.01) — as-builts supersede but do not replace record drawings
- Construction shop drawings (contractor submittals, not part of final facility documentation)
- Vendor drawings (covered under DEL-31.05, unless incorporated by reference into as-builts)
- Temporary works drawings (not part of permanent facility documentation)

**Source:** **ASSUMPTION** based on as-built documentation scope; distinction from Record Drawings per industry practice

**Anticipated deliverable artifacts:**
- As-built drawings (all disciplines) per VFPA standards

**Source:** _CONTEXT.md; Decomposition line 687

## Requirements

### Functional Requirements

**FR-01: As-Built Completeness**
- The As-Built Design Drawing Set shall include all final as-constructed drawings for the Canola Oil Transload Facility Phase 1 Works
- All disciplines identified in Section 4 of the Decomposition (Packages and Deliverables) shall be represented
- **Source:** Decomposition Section 4; **ASSUMPTION** based on project scope
- **Rationale:** See Guidance.md (Principle 1: Accurate Construction Record)
- **Verification:** See Procedure.md (Step 1.1: Prepare As-Built Drawing Register; Step 6: Final Completeness Verification)

**FR-02: Field Verification**
- All as-built drawings shall be verified against actual field conditions through field surveys, measurements, and inspections
- As-built drawings shall accurately represent the constructed facility dimensions, locations, elevations, and configurations
- **Source:** **ASSUMPTION** per as-built documentation requirements; **TBD** — specific field verification requirements per Employer's Requirements
- **Rationale:** See Guidance.md (Principle 1: Accurate Construction Record; Principle 2: Field-Verified Accuracy)
- **Verification:** See Procedure.md (Step 3: Field Measurement and Verification; Step 5.3: Field Verification Sign-Off)

**FR-03: Construction Change Integration**
- All approved design changes, RFIs, field orders, and construction change notices shall be incorporated into as-built drawings
- Change documentation shall be traceable to source records (RFI log, change order register, etc.)
- **Source:** **ASSUMPTION** per configuration management requirements; **TBD** — change documentation requirements per project procedures
- **Rationale:** See Guidance.md (Principle 3: Configuration Integrity; Considerations: Change Documentation Integration)
- **Verification:** See Procedure.md (Step 2: Collect and Review Construction Markups and Changes; Step 4.3: Change Documentation Cross-Check)

**FR-04: VFPA Standards Compliance**
- All as-built drawings shall comply with VFPA (Vancouver Fraser Port Authority) drawing standards and requirements
- **Source:** Decomposition DEL-31.02 (line 687); Employer's Requirements — **TBD** — **location TBD**
- **Rationale:** See Guidance.md (Principle 4: Standardization and Regulatory Compliance; Considerations: VFPA Standards Compliance)
- **Verification:** See Procedure.md (Step 4.4: VFPA Standards Compliance Check)

**FR-05: Baseline from Record Drawings**
- As-built drawings shall be produced using Record Design Drawings (DEL-31.01) as the baseline
- As-built updates shall be clearly distinguishable from original record design information
- **Source:** Datasheet (Attributes: Baseline); **ASSUMPTION** per as-built documentation workflow
- **Rationale:** See Guidance.md (Principle 5: Continuity with Design Baseline; Considerations: Record Drawing Baseline)
- **Verification:** See Procedure.md (Step 1.2: Obtain Record Drawings Baseline)

### Performance Requirements

**PR-01: Drawing Accuracy and Precision**
- As-built drawings shall accurately represent field conditions within acceptable tolerances
- **TBD** — Specific dimensional accuracy tolerances per Employer's Requirements or VFPA standards (e.g., ±6mm for critical dimensions, ±50mm for general arrangement)
- **Source:** **ASSUMPTION** per typical as-built accuracy requirements; **TBD** — project-specific tolerances
- **Rationale:** See Guidance.md (Principle 2: Field-Verified Accuracy)
- **Verification:** See Procedure.md (Step 3.2: Survey and Measurement; Step 6: Final Completeness Verification)

**PR-02: Drawing Format Standards**
- Drawing format, symbology, line weights, text sizes, and annotation standards shall comply with VFPA requirements
- As-built changes shall be clearly indicated per project standards (e.g., revision clouds, change notes, color coding)
- **Source:** Datasheet (Construction: Drawing Standards and Conventions); **TBD** — as-built markup conventions per project procedures
- **Rationale:** See Guidance.md (Principle 4: Standardization and Regulatory Compliance)
- **Verification:** See Procedure.md (Step 4.4: VFPA Standards Compliance Check; Step 5: Technical Review and QA)

**PR-03: Timeliness**
- As-built drawings shall be completed and issued within the schedule requirements of the contract
- **TBD** — Specific schedule milestones for as-built drawing completion (e.g., within 90 days of substantial completion, or per contract requirements)
- **Source:** **ASSUMPTION** per contract closeout requirements; **TBD** — specific schedule per Employer's Requirements or contract
- **Rationale:** See Guidance.md (Considerations: Schedule and Resourcing)
- **Verification:** See Procedure.md (Step 1.3: Develop As-Built Production Schedule)

### Interface Requirements

**IR-01: Record Drawings Interface**
- As-built drawings shall be produced from Record Design Drawing Set (DEL-31.01) as the baseline
- Coordination with design team to understand design intent and changes
- **Source:** FR-05; Datasheet (Attributes: Baseline)
- **Rationale:** See Guidance.md (Principle 5: Continuity with Design Baseline)
- **Verification:** See Procedure.md (Step 1.2: Obtain Record Drawings Baseline)

**IR-02: Construction Team Interface**
- Construction field personnel shall provide marked-up drawings, field measurement data, and change documentation
- Coordination with construction management to track and document field changes
- **Source:** **ASSUMPTION** per construction documentation workflow; cross-reference construction installation & test records (DEL-04.04 through DEL-26.04 as applicable)
- **Rationale:** See Guidance.md (Considerations: Construction Team Coordination)
- **Verification:** See Procedure.md (Step 2: Collect and Review Construction Markups and Changes)

**IR-03: Commissioning Records Interface**
- As-built drawings shall be cross-checked against commissioning test records and acceptance documentation (PKG-30) to confirm final operating configurations
- **Source:** **ASSUMPTION** per commissioning closeout; cross-reference PKG-30 (Commissioning)
- **Rationale:** See Guidance.md (Considerations: Commissioning Records Cross-Check)
- **Verification:** See Procedure.md (Step 3.3: Cross-Check with Commissioning Records)

**IR-04: Operations & Maintenance Interface**
- As-built drawings shall serve as primary reference for operation manuals (DEL-31.03) and maintenance manuals (DEL-31.04)
- As-built drawings shall be suitable for use by operations and maintenance personnel
- **Source:** **ASSUMPTION** per OBJ-9 (Lifecycle Cost Optimization, Decomposition line 788); Datasheet (Conditions: Purpose and Context)
- **Rationale:** See Guidance.md (Principle 6: Operability and Maintainability Support)
- **Verification:** See Procedure.md (Step 7: Handover to Operations)

**IR-05: Asset Hierarchy Interface**
- Equipment tags and identifiers on as-built drawings shall align with Asset Hierarchy (DEL-31.06)
- **Source:** **ASSUMPTION** per asset management integration; cross-reference DEL-31.06 (Decomposition line 692)
- **Rationale:** See Guidance.md (Considerations: Asset Management Integration)
- **Verification:** See Procedure.md (Step 4.5: Asset Tag Verification)

**IR-06: Regulatory Handover Interface**
- As-built drawings shall be suitable for submission to regulatory authorities for project closeout and acceptance
- **Source:** **ASSUMPTION** per regulatory compliance requirements; cross-reference PKG-32 (Regulatory & Permits)
- **Rationale:** See Guidance.md (Principle 4: Standardization and Regulatory Compliance)
- **Verification:** See Procedure.md (Step 5.4: Regulatory Submittal Readiness Check)

### Quality Requirements

**QR-01: Quality Management System Compliance**
- All work shall comply with the project Quality Management Plan
- **Source:** **ASSUMPTION** per ISO 9001 requirements

**QR-02: As-Built Drawing Checking and Review**
- All as-built drawings shall undergo technical checking and independent review prior to approval
- Checker and reviewer qualifications shall meet project requirements
- Field verification sign-offs shall be obtained
- **Source:** **ASSUMPTION** per engineering quality assurance practice
- **Rationale:** See Guidance.md (Considerations: Quality Assurance and Checking)
- **Verification:** See Procedure.md (Step 5: Technical Review and QA)

**QR-03: As-Built Drawing Approval Authority**
- As-built drawings shall be approved by authorized personnel per project procedures
- Approval signatures and dates shall be recorded on drawing title blocks
- **Source:** **ASSUMPTION** per document control practice
- **Verification:** See Procedure.md (Step 5.5: Final Approval)

**QR-04: Audit Trail and Traceability**
- Complete audit trail of construction changes, field verifications, reviews, and approvals shall be maintained
- As-built changes traceable to source documentation (RFIs, field orders, change notices, field measurements)
- **Source:** **ASSUMPTION** per quality management and traceability requirements; FR-03
- **Rationale:** See Guidance.md (Principle 3: Configuration Integrity)
- **Verification:** See Procedure.md (Step 4.3: Change Documentation Cross-Check; Step 6: Final Completeness Verification)

### Safety and Regulatory Requirements

**SR-01: Safe & Reliable Operation Support**
- As-built drawings shall support OBJ-1 (Safe & Reliable Operation) by accurately documenting as-constructed safety systems, emergency response features, and operational configurations
- **Source:** Decomposition Section 2, OBJ-1 (line 59); Objective Mapping (line 780)
- **Verification:** See Procedure.md (Step 3: Field Measurement and Verification; Step 6: Final Completeness Verification)

**SR-02: Regulatory Compliance**
- As-built drawings shall comply with all applicable codes, standards, and regulatory requirements
- **Source:** OBJ-6 (Regulatory Compliance, Decomposition line 64); **TBD** — specific code/standard references per Employer's Requirements

### Lifecycle and Maintenance Requirements

**LR-01: Lifecycle Cost Optimization**
- As-built drawings shall support OBJ-9 (Lifecycle Cost Optimization) by providing accurate documentation for operations, maintenance, modifications, and future expansions
- **Source:** Decomposition Section 2, OBJ-9 (line 67); Objective Mapping (line 788)
- **Rationale:** See Guidance.md (Principle 6: Operability and Maintainability Support)
- **Verification:** See Procedure.md (Step 7: Handover to Operations)

**LR-02: Future Expandability Documentation**
- As-built drawings shall document as-constructed provisions for Phase 2 expansion per OBJ-8
- **Source:** OBJ-8 (Future Expandability, Decomposition line 66)
- **Verification:** See Procedure.md (Step 6: Final Completeness Verification)

## Standards

**Applicable codes and standards (Project Delivery discipline):**

- **VFPA (Vancouver Fraser Port Authority) Drawing Standards** — **TBD** — **location TBD**
- **ISO 9001:2015** — Quality Management Systems
- **ISO 14001** — Environmental Management Systems
- **ISO 45001** — Occupational Health and Safety Management Systems
- **CAD Standards** — **TBD** — Project-specific CAD standards and as-built markup conventions
- **Employer's Requirements** — Volumes 2 Part 1, 2, 3 (project-specific requirements) — **TBD** — **location TBD**

**Source:** **ASSUMPTION** per Project Delivery discipline context

**Additional applicable standards (discipline-specific):**
- Each discipline's as-built drawings shall comply with discipline-specific codes and standards as identified in respective package specifications (PKG-04 through PKG-26)
- **Source:** **ASSUMPTION** based on multi-discipline project scope

## Verification

**Verification methods for As-Built Drawing Set deliverables:**

1. **Field Verification and Measurement** (Step 3)
   - Physical field surveys and measurements to confirm as-constructed dimensions, locations, elevations
   - Visual inspection to verify configurations and installations
   - **Acceptance Criterion:** As-built drawings match field conditions within specified tolerances

2. **Change Documentation Cross-Check** (Step 4.3)
   - Verify all RFIs, field orders, design changes, and construction change notices are incorporated
   - Traceability to source documents confirmed
   - **Acceptance Criterion:** All approved changes reflected in as-built drawings; traceability documented

3. **Completeness Check** (Step 6)
   - Verification that all required as-built drawings are included
   - Cross-check against as-built drawing register and deliverable requirements
   - **Acceptance Criterion:** As-built drawing register 100% complete; no missing drawings

4. **Format and Standards Compliance** (Step 4.4)
   - Review for compliance with VFPA drawing standards
   - Check symbology, annotations, title blocks, scales, coordinate systems, as-built markup conventions
   - **Acceptance Criterion:** Full compliance with VFPA standards and project as-built conventions confirmed

5. **Technical Review and QA** (Step 5)
   - Independent technical review by qualified checker
   - Verification of as-built accuracy, completeness, and compliance
   - **Acceptance Criterion:** Checker sign-off obtained; no unresolved technical issues

6. **Stakeholder Review and Acceptance** (Step 5.5, Step 7)
   - Internal review (D&B Contractor team)
   - Employer review and acceptance
   - Regulatory authority review (as required for project closeout)
   - **Acceptance Criterion:** All stakeholder comments addressed; required approvals obtained

**Overall Acceptance Criteria:**
- All construction changes and field conditions accurately incorporated
- Field verification sign-offs obtained for all as-built drawings
- Technical review and checker sign-offs obtained
- As-built drawings issued with "As-Built" or "Final" status
- Compliance with VFPA standards confirmed
- Employer acceptance obtained
- As-built drawing register complete and accurate

**Source:** **ASSUMPTION** per as-built documentation quality requirements; **TBD** — specific acceptance criteria per Employer's Requirements

## Documentation

**Required documentation outputs:**

1. **As-Built Drawings:**
   - Electronic format (CAD native files and PDF)
   - Hard copy sets (if required)
   - **Source:** Datasheet (Construction: Deliverable Format)

2. **As-Built Drawing Register:**
   - Comprehensive list of all as-built drawings with drawing numbers, titles, revisions, as-built completion dates
   - **Source:** **ASSUMPTION** per document control requirements

3. **Field Verification Records:**
   - Survey data, field measurement logs, inspection records
   - Sign-offs from field personnel confirming as-built accuracy
   - **Source:** **ASSUMPTION** per field verification requirements

4. **Change Documentation Package:**
   - Compilation of RFIs, field orders, design changes, construction change notices incorporated into as-builts
   - Cross-reference table linking changes to affected drawings
   - **Source:** FR-03; QR-04

5. **As-Built Transmittals:**
   - Transmittal records for all as-built drawing submissions and approvals
   - **Source:** **ASSUMPTION** per document control practice

**Documentation requirements:**

- All documents shall comply with project document control procedures
- Revision control per project numbering system — **TBD**
- Format: **ASSUMPTION**: Per project document management requirements and VFPA standards
- Electronic records managed in project document management system — **TBD** — **location TBD**
- Retention requirements: **TBD** — Per Employer's Requirements and regulatory requirements (typically for facility design life plus additional years per records retention policy)

**Filing and Archiving:**
- Working documents in `1_Working/` folder
- Review packages in `2_Checking/To/` (during review)
- Issued as-built documents in `3_Issued/` (upon approval and handover)
- **Source:** README.md (Section: "How to use the framework")
