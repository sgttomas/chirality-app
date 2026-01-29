# Specification: DEL-29.02 Inspection and Test Plan With Hold/Witness Points

## Scope

This specification defines the requirements for **Inspection and Test Plan With Hold/Witness Points** within **PKG-29 Testing**.

**Purpose:** Defines the planned approach and controls for inspection and test plan with hold/witness points to meet ER requirements. **Source:** Decomposition line 647

**Deliverable Type:** Plan
**Responsible Party:** D&B Contractor (QA/QC)
**Source:** _CONTEXT.md

### Inclusions

This deliverable encompasses:
1. **Inspection and Test Plan (ITP) with hold/witness points** — Comprehensive matrix of all inspection and test activities with Employer hold/witness designations
2. **Inspection matrix** — Summary document showing inspection categories and distribution

**Source:** _CONTEXT.md Anticipated Artifacts, Decomposition line 647

The ITP shall cover inspection and testing activities across all project phases:
- Design phase reviews and approvals
- Procurement and vendor surveillance
- Shop fabrication and FAT
- Construction installation and field inspection
- Testing activities (hydrostatic, electrical, I&C)
- Commissioning and performance verification

**ASSUMPTION:** Scope encompasses full project lifecycle per typical D&B project quality requirements

### Exclusions

The following are excluded from this deliverable:
- Detailed test procedures — covered by DEL-29.01 (Test Procedures)
- Actual test records and inspection reports — covered by DEL-29.03 through DEL-29.08
- Project Quality Management Plan — covered by DEL-00.03 **ASSUMPTION**
- Non-conformance tracking system — covered by project quality procedures (not a specific deliverable)

**ASSUMPTION:** Exclusions based on PKG-29 and PKG-00 deliverable boundaries

## Requirements

### Functional Requirements

**FR-1: Comprehensive Coverage**

The ITP shall identify and document:
- All equipment, systems, and work activities requiring inspection or testing
- All code-mandated inspection hold points (pressure tests, concrete pours, etc.)
- All Employer-required hold and witness points per Employer's Requirements **location TBD**
- All third-party inspection requirements (insurance, regulatory authorities)

**Source:** General ITP practice; ASME B31.3, API 650, AWS D1.1 (inspection requirements) **ASSUMPTION**

**FR-2: Hold and Witness Point Designations**

The ITP shall clearly designate each inspection activity as:
- **Hold Point (H):** Work cannot proceed without Employer release
- **Witness Point (W):** Employer may observe; work may proceed if witness not available per prior agreement
- **Review Point (R):** Document review without physical inspection **ASSUMPTION**
- **Contractor Verification:** No Employer presence required

**Definitions:**
- Hold point: A mandatory stop point where the Contractor shall not proceed without formal release from the Employer or designated representative
- Witness point: A planned observation point where the Employer may observe work; if the Employer does not attend after proper notification, work may proceed (subject to prior agreement and project procedures)

**TBD:** Specific hold/witness point definitions and release authority per Employer's Requirements **location TBD** and project Quality Management Plan **location TBD**

**FR-3: Inspection Criteria and Acceptance Standards**

For each inspection activity, the ITP shall specify:
- Applicable specification or drawing reference
- Acceptance criteria or reference standard (code section, specification clause, etc.)
- Required documentation (test reports, certifications, photographs)

**Source:** ISO 9001 (documented quality requirements), typical EPC ITP content **ASSUMPTION**

**FR-4: Notification and Scheduling**

The ITP shall define:
- Minimum advance notification period for hold/witness points (e.g., 48 hours, 72 hours)
- Notification method and contact information
- Response time for Employer release or witness availability
- Procedure for rescheduling inspections

**TBD:** Specific notification requirements per Employer's Requirements **location TBD**

**FR-5: Status Tracking and Documentation**

The ITP shall include provisions for tracking:
- Date inspection performed
- Inspector name and qualification
- Employer representative (if witnessed)
- Inspection result (pass/fail)
- Non-conformance reference (if applicable)
- Completion sign-off

**Source:** General ITP tracking practice **ASSUMPTION**

### Performance Requirements

**PR-1: Completeness and Accuracy**

- ITP shall cover 100% of code-required inspections
- ITP shall cover 100% of Employer-specified hold/witness points
- ITP shall be updated to reflect design changes, scope additions, and lessons learned
- ITP revisions shall be coordinated with Employer and incorporated prior to affected work

**Source:** Project quality requirements **ASSUMPTION**

**PR-2: Timing and Coordination**

- Initial ITP shall be submitted for Employer review within **TBD** days of contract award or per project schedule milestone
- ITP updates shall be submitted for Employer review **TBD** days prior to affected work
- Final ITP shall be issued prior to start of construction activities
- ITP shall be progressively updated as design matures and construction progresses

**TBD:** Specific timing requirements per project execution plan or Employer's Requirements **location TBD**

**PR-3: Integration with Test Procedures**

- ITP hold/witness designations shall be incorporated into test procedures per DEL-29.01
- Test procedure steps shall reference ITP activity numbers for traceability
- ITP updates shall be coordinated with test procedure revisions

**Source:** Cross-reference to DEL-29.01 (Test Procedures), Specification FR-3

### Interface Requirements

**IR-1: Upstream Design Deliverable Interfaces**

ITP content is derived from:
- Design drawings (all disciplines) — identify equipment and systems to inspect
- Design specifications (all disciplines) — provide inspection criteria and acceptance standards
- Design calculations — identify code-required inspections (pressure tests, structural verifications)
- Equipment vendor documents — identify FAT requirements and inspection hold points

**ASSUMPTION:** Design maturity required before ITP can be finalized; interim ITPs may be issued as design progresses

**IR-2: Downstream Testing and Records Interfaces**

ITP provides input to:
- DEL-29.01 (Test Procedures) — hold/witness points are implemented in procedures
- DEL-29.03 (Test Installation & Test Records) — ITP activity numbers used for record traceability
- DEL-29.04 (FAT Records) — ITP defines FAT witness requirements
- DEL-29.05 (SAT Records) — ITP defines SAT witness requirements
- All package installation and test records — ITP defines inspection requirements

**Source:** PKG-29 deliverable relationships, Decomposition lines 646-653

**IR-3: Coordination with Employer and Third Parties**

ITP shall accommodate:
- Employer witness and hold point preferences
- Third-party inspector requirements (insurance surveyors, regulatory authorities)
- Sub-contractor and vendor quality plans
- Schedule constraints and mobilization logistics

**TBD:** Specific third-party inspection requirements

### Quality Requirements

**QR-1: ITP Development and Approval**

- ITP shall be developed by qualified QA/QC personnel
- ITP shall undergo multi-discipline review (Engineering, Construction, HSE, Procurement)
- ITP shall be submitted to Employer for review and acceptance prior to use
- Employer comments shall be addressed and incorporated prior to final issue

**Source:** Typical D&B contract quality requirements **ASSUMPTION**

**QR-2: ITP Maintenance and Revision Control**

- ITP shall be maintained as a controlled document per project document control procedures
- Revisions shall be clearly marked and tracked
- Current ITP revision shall be distributed to all required parties
- Superseded revisions shall be archived but not used for work

**Source:** ISO 9001, general document control practice **ASSUMPTION**

**QR-3: Competency of Inspectors**

- ITP shall specify minimum qualification requirements for inspectors (Contractor QC and Employer representative)
- Inspector qualifications shall be verified prior to performing inspections
- Qualification records shall be maintained

**TBD:** Specific inspector qualification requirements per project Quality Management Plan **location TBD**

## Standards

### Applicable Codes and Standards

**Quality Management:**
- ISO 9001: Quality Management Systems **ASSUMPTION**
- Project Quality Management Plan: **location TBD**
- Employer's Requirements: **location TBD** (quality requirements, hold/witness points)

**Discipline-Specific Inspection Standards:**

**Civil/Structural:**
- ACI 318: Building Code Requirements for Structural Concrete (inspection)
- ACI 301: Specifications for Structural Concrete (inspection requirements)
- AWS D1.1: Structural Welding Code — Steel (welding inspection)
- CSA W59: Welded Steel Construction (Metal Structures) **ASSUMPTION for Canadian project**

**Mechanical/Process:**
- ASME B31.3: Process Piping (inspection and examination)
- API 650: Welded Tanks for Oil Storage (inspection requirements)
- API 653: Tank Inspection, Repair, Alteration, and Reconstruction
- ASME Section V: Nondestructive Examination
- ASME Section VIII: Pressure Vessels (inspection)

**Marine:**
- PIANC: Guidelines for Marina and Port Design (inspection considerations)
- Local maritime authority requirements **TBD**

**Electrical:**
- NFPA 70: National Electrical Code (installation inspection)
- NETA: Standards for Electrical Testing (acceptance testing)

**I&C:**
- IEC 62382: Electrical and instrumentation loop check
- ISA: Instrumentation standards (calibration and loop testing)

**Nondestructive Testing:**
- ASME Section V: Nondestructive Examination
- ASTM E165 / E709 / E1417: Liquid Penetrant Testing
- ASTM E94 / E747 / E1742: Radiographic Testing
- ASTM E164 / E587 / E2001: Ultrasonic Testing

**Coatings:**
- NACE/SSPC: Surface Preparation and Coatings Application Standards
- ISO 12944: Paints and Varnishes — Corrosion Protection

**Source:** Typical EPC project inspection standards based on project scope per Decomposition Sections 4-5

## Verification

### Verification Methods

**VM-1: Completeness Review**
- Verify ITP covers all equipment, systems, and work activities identified in design deliverables
- Verify ITP covers all code-mandated inspection points
- Verify ITP addresses all Employer-specified hold/witness requirements
- Checklist review against package deliverables (PKG-01 through PKG-36)

**VM-2: Multi-Discipline Review**
- Engineering review: Verify inspection criteria align with design specifications
- Construction review: Verify inspection sequence and logistics are practical
- QA/QC review: Verify ITP meets project quality plan requirements
- HSE review: Verify inspection activities address safety considerations
- Procurement review: Verify vendor/supplier inspection requirements are included

**VM-3: Employer Review and Acceptance**
- Submit ITP to Employer for review
- Conduct ITP review meeting to discuss hold/witness points and notification requirements
- Address Employer comments and resubmit if necessary
- Obtain Employer formal acceptance

**Source:** Typical D&B project review process **ASSUMPTION**

**VM-4: Integration Check**
- Verify ITP activity numbers are correctly referenced in test procedures (DEL-29.01)
- Verify test record forms (DEL-29.03) include fields for ITP activity number and hold/witness sign-off
- Verify sub-contractor and vendor quality plans align with ITP requirements

### Acceptance Criteria

**AC-1: Completeness**
- ITP covers all required inspection activities (100% of code-required and Employer-specified inspections)
- ITP includes all required information fields (item, activity, criteria, hold/witness, notification, documentation)
- Inspection matrix provides complete summary of ITP content

**AC-2: Adequacy**
- Inspection criteria are clear, measurable, and traceable to design specifications or codes
- Hold/witness designations are appropriate for risk and contractual requirements
- Notification periods allow adequate time for Employer planning

**AC-3: Approval Status**
- Multi-discipline reviews completed and comments addressed
- Employer has reviewed and accepted the ITP
- ITP is issued as a controlled document

**TBD:** Specific acceptance criteria per Employer's Requirements and project Quality Management Plan **location TBD**

## Documentation

### Required Deliverable Outputs

**Primary Deliverable: Inspection and Test Plan (ITP) with Hold/Witness Points**

**ITP Document Structure:**
- Cover page: Project name, document number, revision, date, approval signatures
- Table of contents (if ITP is multi-volume)
- Introduction: Purpose, scope, definitions, responsibilities
- ITP Matrix: Tabular listing of all inspection activities with hold/witness designations
  - May be organized by package, discipline, system, or phase
  - Typically 100s to 1000s of line items for a project of this scale
- Notification and Release Procedures: How to notify Employer, how hold points are released
- References: Applicable drawings, specifications, standards
- Appendices: Sample inspection forms, contact lists, revision log

**TBD:** Specific ITP format, organization, and template per Employer's Requirements **location TBD** or project standards

**Secondary Deliverable: Inspection Matrix**

**Inspection Matrix Content:**
- Summary table showing inspection categories by discipline or phase
- Count or percentage of hold/witness/review/Contractor-only inspections by category
- May include bar charts or other visualizations
- Used for high-level planning and communication with Employer

**ASSUMPTION:** Inspection matrix format to be determined based on project needs and Employer preferences

### Documentation Format and Control

- Document format: **TBD** — Typically spreadsheet (Excel) for ITP matrix, PDF for issued/archived copies
- Document numbering: **TBD** — Per project numbering system (e.g., COTF-QC-PLN-29.02-001)
- Revision control: Per project document control procedures **location TBD**
- Distribution: **TBD** — QA/QC, Engineering, Construction, Commissioning, HSE, Employer, Third-party inspectors
- Update frequency: Progressive updates as design matures and construction progresses; major revisions at project milestones (e.g., IFC design, start of construction, start of testing)
- Retention: Permanent project record

### Integration with Other Documentation

- Test procedures (DEL-29.01): ITP activity numbers and hold/witness designations incorporated
- Test records (DEL-29.03-29.08): Record forms include ITP activity number for traceability
- Project schedule: ITP activities may be linked to schedule milestones for notification and planning
- Non-conformance reports: NCRs reference ITP activity number if inspection fails

**ASSUMPTION:** Integration methods based on typical EPC project document coordination practices

---

## Cross-Document Linkage

| Document | Key Sections | Relationship |
|----------|--------------|--------------|
| Datasheet.md | §Attributes, §Construction, §References | Captures ITP structure, column definitions, and cross-references |
| Guidance.md | §Principles, §Considerations, §Trade-offs, §Examples | Provides rationale for requirements and practical implementation examples |
| Procedure.md | §Steps 1-9, §Verification | Defines process for implementing these requirements |

**Requirement-to-Guidance Traceability:**
- FR-1 (Comprehensive Coverage) → Guidance §Considerations Items 1-2 (Scope, Code Requirements)
- FR-2 (Hold/Witness Designations) → Guidance §Principles (Hold Point vs. Witness Point Philosophy)
- FR-3 (Acceptance Criteria) → Guidance §Examples (ITP Matrix Entry examples)
- FR-4 (Notification/Scheduling) → Guidance §Examples (Notification Procedure)
- FR-5 (Status Tracking) → Guidance §Examples (ITP Structure)
- PR-3 (Test Procedure Integration) → Cross-reference DEL-29.01 Specification FR-3

**Requirement-to-Procedure Traceability:**
- FR-1 (Coverage) → Procedure Step 2 (Identify Inspection Activities)
- FR-2 (Designations) → Procedure Step 3 (Assign Hold/Witness Designations)
- FR-3 (Criteria) → Procedure Step 4 (Define Acceptance Criteria)
- FR-4, FR-5 (Notification, Tracking) → Procedure Steps 4, 9
- QR-1 (Development/Approval) → Procedure Steps 6-8
- QR-2 (Maintenance) → Procedure Step 9
