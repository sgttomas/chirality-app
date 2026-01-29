# Datasheet: DEL-29.02 Inspection and Test Plan With Hold/Witness Points

## Identification

| Field | Value |
|-------|-------|
| Deliverable ID | DEL-29.02 |
| Name | Inspection and Test Plan With Hold/Witness Points |
| Package | PKG-29 Testing |
| Discipline | T&C |
| Type | Plan |
| Responsible | D&B Contractor (QA/QC) |
| Status | INITIALIZED |

**Source:** _CONTEXT.md, Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md line 647

## Attributes

| Attribute | Value |
|-----------|-------|
| Plan Type | Inspection and Test Plan (ITP) |
| Document Format | Matrix/Tabular with hold/witness designations |
| Coverage Scope | All project systems and equipment requiring inspection/testing |
| Applicable Phase | Design, Procurement, Fabrication, Construction, Testing, Commissioning |
| Hold Point Definition | Mandatory stop — work cannot proceed without release |
| Witness Point Definition | Optional observation — work may proceed if witness unavailable (per agreement) **ASSUMPTION** |
| Revision Frequency | Progressive updates as design and construction progress |

**Source:** _CONTEXT.md; general ITP practice **ASSUMPTION**

**ASSUMPTION:** Hold/witness point definitions follow typical EPC project conventions; specific definitions to be confirmed per Employer's Requirements **location TBD**

## Conditions

**Operating / Environmental Context:**

Defines the planned approach and controls for inspection and test plan with hold/witness points to meet ER requirements. **Source:** Decomposition line 647

**Project Context:**
- Facility: Canola Oil Transload Facility — Phase 1
- Location: Fraser Surrey Terminal, 11060 Elevator Road, Surrey, BC
- Contract Type: Design & Build
- Employer: DP World Fraser Surrey Inc.

**Source:** Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md Section 1

**ITP Application Context:**

The Inspection and Test Plan serves as the master quality control document that:
1. Identifies all inspection and test activities across the project lifecycle
2. Designates which activities require Employer hold or witness
3. Defines inspection criteria and acceptance standards
4. Establishes notification and documentation requirements
5. Provides traceability from construction through commissioning

**Project Objectives Supported:**
- OBJ-1: Safe & Reliable Operation (quality verification ensures safety)
- OBJ-6: Regulatory Compliance (inspection evidence for authority approvals)

**Source:** Project Objectives, Decomposition Section 2 (lines 58-67); Section 6 Objective Mapping (line 780, 787)

**Inspection Phases:**

The ITP covers inspection and testing activities during:
- **Design Phase:** Design reviews, calculations checks, drawing approvals
- **Procurement Phase:** Vendor document reviews, FAT requirements
- **Fabrication Phase:** Shop fabrication inspections, material certifications, NDT
- **Construction Phase:** Installation inspections, field welding, concrete placement, coatings
- **Testing Phase:** Hydrostatic tests, electrical tests, I&C calibration (cross-ref DEL-29.01)
- **Commissioning Phase:** Pre-commissioning, commissioning, performance testing (cross-ref PKG-30)

**ASSUMPTION:** Phase breakdown based on typical D&B project lifecycle

## Construction

**ITP Structure and Content:**

### Primary Deliverable: Inspection and Test Plan (ITP) with Hold/Witness Points

**Typical ITP Matrix Columns:**
1. **Item/System:** Equipment tag, system, or work package identifier
2. **Description:** Brief description of item or activity
3. **Specification/Drawing Reference:** Governing technical documents
4. **Inspection/Test Activity:** What is being inspected or tested
5. **Acceptance Criteria:** Pass/fail criteria or reference standard
6. **Responsible Party:** Who performs the inspection (Contractor QC, Engineer, etc.)
7. **Hold/Witness Designation:**
   - **H** = Hold point (mandatory stop for Employer release)
   - **W** = Witness point (Employer may observe)
   - **R** = Review point (document review by Employer) **ASSUMPTION**
   - **Blank** = Contractor verification only
8. **Notification Requirements:** Advance notice period for Employer (e.g., 48 hours)
9. **Documentation Requirements:** Required records (test reports, certifications, photos)
10. **Status Tracking:** Date performed, inspected by, accepted by

**Source:** Typical ITP format used in EPC projects **ASSUMPTION**

**TBD:** Specific ITP format and column structure per Employer's Requirements **location TBD** or project Quality Management Plan **location TBD**

### Secondary Deliverable: Inspection Matrix

**Inspection Matrix Purpose:**
- Simplified summary of ITP showing high-level inspection categories
- Maps inspection activities to project deliverables or work packages
- Provides overview of hold/witness point distribution by discipline or phase
- May be used for early project planning and Employer coordination

**ASSUMPTION:** Inspection matrix is a summary/visualization tool derived from detailed ITP

**Inspection Categories (Typical):**

**By Discipline:**
- Civil: Earthworks, concrete, paving, drainage
- Structural: Steel fabrication, erection, welding, fireproofing
- Marine: Marine structures, fenders, mooring, loading arms
- Mechanical: Piping, tanks, equipment installation, pressure testing
- Electrical: Electrical equipment, cable installation, terminations, testing
- I&C: Instrument installation, calibration, loop checks
- Architectural: Buildings, cladding, roofing, finishes

**By Inspection Type:**
- Material receiving inspections (mill certs, test reports)
- Fabrication inspections (dimensional, welding, NDT)
- Installation inspections (alignment, torque, grounding)
- Testing inspections (pressure tests, electrical tests, calibration)
- Commissioning inspections (functional tests, performance verification)

**Source:** Project package structure PKG-01 through PKG-36 per Decomposition Section 4; typical EPC inspection taxonomy **ASSUMPTION**

## References

**Decomposition & Context:**
- Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md (Section 5, PKG-29, lines 636-653)
- _CONTEXT.md (deliverable identity and scope)
- _REFERENCES.md (reference materials listing)

**Applicable Standards and References:**

**Quality Management:**
- ISO 9001: Quality Management Systems **ASSUMPTION**
- Project Quality Management Plan: **location TBD**
- Employer's Requirements: **location TBD** — Hold/witness point requirements

**Industry Standards for Inspection:**
- ASME B31.3: Process Piping (inspection requirements)
- API 650: Welded Tanks for Oil Storage (inspection and examination)
- AWS D1.1: Structural Welding Code (welding inspection)
- NACE/SSPC: Coatings inspection standards
- ASME Section V: Nondestructive Examination
- ACI 318: Building Code Requirements for Structural Concrete (inspection)

**Source:** Anticipated inspection scope based on project deliverables and typical EPC standards

**Cross-References to Other Deliverables:**

**Upstream (Input) Deliverables:**
- All design deliverables (PKG-04 through PKG-28) — provide basis for inspection criteria
- DEL-00.03: Quality Management Plan — governs ITP requirements **ASSUMPTION**
- DEL-00.04: HSE Management Plan — safety requirements for inspection activities **ASSUMPTION**

**Downstream (Output) Deliverables:**
- DEL-29.01: Test Procedures — implement the hold/witness points defined in ITP
- DEL-29.03: Test Installation & Test Records — document results of ITP activities
- DEL-29.04: FAT Installation & Test Records — factory inspection records per ITP
- DEL-29.05: SAT Installation & Test Records — site inspection records per ITP
- All package-specific installation and test records (DEL-*.04 or DEL-*.05 per package)

**Lateral (Coordination) Deliverables:**
- PKG-30 (Commissioning): ITP transitions into commissioning inspection activities
- All construction packages: ITP defines inspection requirements for each work package

**ASSUMPTION:** Cross-package coordination based on typical D&B project information flow

**Third-Party Inspection References:**
- Insurance surveyor requirements: **TBD**
- Regulatory authority requirements (Transport Canada, local fire marshal, etc.): **TBD**
- Classification society requirements (if applicable for marine structures): **TBD**

See `_DEPENDENCIES.md` (NOT_TRACKED — dependencies coordinated externally)
