# Procedure: DEL-07.01 Rail Works Design Drawing Set

**Enrichment Status:** Pass 3 Complete (3-pass enrichment: Initial draft, Cross-reference enrichment, Final reconciliation)

## Purpose

This Procedure defines the workflow to **produce and control** the Rail Works Design Drawing Set (DEL-07.01) that establishes the arrangement and detailing for PKG-07 rail works at the Canola Oil Transload Facility.

**Scope of this Procedure:**
- Production workflow: How to develop the drawing set from inputs to draft to checked deliverable
- Verification workflow: How to verify the drawing set satisfies Specification requirements
- Records workflow: What documentation must be maintained to demonstrate compliance

**What this Procedure accomplishes:**
- Operationalizes Specification.md requirements into actionable steps
- Defines quality checkpoints and verification activities
- Ensures traceability through inputs/assumptions register and supporting records

(Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:259, :265)

## Prerequisites

### Dependencies and Coordination

| Prerequisite Category | Requirement | Verification | Cross-Reference |
|-----------------------|-------------|--------------|-----------------|
| **Dependency coordination** | Dependencies coordinated externally by humans (NOT_TRACKED mode; see `_DEPENDENCIES.md`); confirm required inputs and interface expectations before starting | Review coordination records; confirm inputs available | Specification.md: Requirements IR-02; Guidance.md: Considerations (Coordination and Dependencies) |
| **Interface confirmation** | Identify interface points with adjacent packages (civil, process); confirm coordination approach | Coordination meeting notes or external workflow confirmation | Specification.md: Requirements IR-01; Datasheet.md: Conditions (Interface boundaries) |

### Reference Materials

| Reference | Purpose | Status | Cross-Reference |
|-----------|---------|--------|-----------------|
| Employer's Requirements Vol 2 Pt 1 | Document control, drawing standards, QA procedures | Available (clauses **TBD**) | Specification.md: Standards (Drawing standards, Document control, QA/QC procedures) |
| Employer's Requirements Vol 2 Pt 2 | Rail/civil works requirements, design criteria | Available (clauses **TBD**) | Specification.md: Standards (Rail/track design); Datasheet.md: Conditions (Design Criteria) |
| DEL-07.02 (if available) | Rail Works Technical Specification (materials/workmanship) | **TBD** — may not be available at initial draft stage | Specification.md: Requirements PR-01, FR-03; Steps 5 (consistency check) |
| DEL-07.03 (if available) | Rail Works Design Calculations (design basis/sizing) | **TBD** — may not be available at initial draft stage | Specification.md: Requirements PR-02, QR-03, FR-03; Steps 3, 5 (assumptions/consistency check) |

(Source: test/Volume_2_Part_1_Employers_Requirements.pdf; test/Volume_2_Part_2_Employers_Requirements.pdf, clauses TBD; test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:47, :266-267)

### Scope Confirmation

| Scope Element | Confirmation Required | Cross-Reference |
|---------------|----------------------|-----------------|
| **Rail works scope** | Confirm Tracks 6 & 7 (new works), Track 5 (restoration/modifications), ballast, end stops | Datasheet.md: Conditions (Context & Scope); Specification.md: Scope |
| **Anticipated artifacts** | Confirm drawing set shall include track layout plans, rail profiles, ballast sections, end stop details | Datasheet.md: Content (Anticipated Artifacts); Specification.md: Scope (Anticipated Artifacts) |
| **Deliverable purpose** | Confirm drawings define design arrangement and details per ER requirements | Specification.md: Scope; Guidance.md: Purpose |

(Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:259, :265)

## Steps

### Step 1: Scope and Sheet List Confirmation

**Action:**
- Review deliverable scope per Specification.md: Scope and Datasheet.md: Conditions (Context & Scope)
- Confirm minimum anticipated artifacts per decomposition and Datasheet.md: Content
- Develop preliminary sheet list identifying sheets needed to represent track layouts, profiles, ballast sections, end stop details

**Outputs:**
- Preliminary sheet list (drawing sheet index)

**Verification:**
- Sheet list covers all anticipated artifacts (Specification.md: Requirements FR-01; Verification)

**Cross-Reference:**
- Datasheet.md: Content (Anticipated Artifacts); Specification.md: Scope (Anticipated Artifacts); Guidance.md: Examples

(Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:265)

---

### Step 2: Input Gathering and Coordination

**Action:**
- Gather required inputs from project coordination workflow:
  - Survey data / base plans
  - Existing track information (Track 5 as-built or design data)
  - Site constraints and interface requirements
- Confirm interface expectations with adjacent packages per external coordination workflow (NOT_TRACKED dependency mode)
- Record any missing inputs as **TBD** in inputs/assumptions register (Step 3)

**Outputs:**
- Input data package (survey, existing conditions, constraints)
- Coordination records (meeting notes, interface confirmations)

**Verification:**
- Required inputs identified and obtained (or noted as **TBD**)
- Interface coordination confirmed per external workflow

**Cross-Reference:**
- Prerequisites (Reference Materials, Dependencies and Coordination); Specification.md: Requirements IR-01, IR-02; Guidance.md: Considerations (Coordination and Dependencies)

---

### Step 3: Inputs/Assumptions Register Creation

**Action:**
- Create an inputs/assumptions register documenting:
  - What inputs were used (survey, existing track data, constraints)
  - What inputs remain **TBD** (to be obtained or confirmed)
  - What design assumptions were made (e.g., preliminary geometry, ballast depth basis)
- For each assumption, note:
  - Assumption description
  - Basis (e.g., "per DEL-07.03 calculation XX," "engineering judgment pending survey," etc.)
  - Whether traceable to DEL-07.03 or tagged **ASSUMPTION**
- Ensure register supports cross-checks against DEL-07.02 and DEL-07.03 (Steps 5)

**Outputs:**
- Inputs/assumptions register (maintained throughout drawing development)

**Verification:**
- All assumptions documented and traceable or tagged (Specification.md: Requirements QR-03)

**Cross-Reference:**
- Specification.md: Requirements QR-03 (assumption traceability); Guidance.md: Principles (Assumption transparency), Considerations (Drawing Content and Clarity), Trade-offs (Assumption visibility)

(Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:267)

---

### Step 4: Draft Drawing Production

**Action:**
- Produce draft drawings for each anticipated artifact:
  - **Track layout plans:** Plan view showing Tracks 5, 6, 7 arrangement, alignment, limits of work, interface callouts (Specification.md: Requirements FR-04)
  - **Rail profiles:** Longitudinal profiles showing rail elevations, vertical geometry, critical elevations (Specification.md: Requirements FR-05)
  - **Ballast sections:** Cross-sections showing ballast depth, material zones, sub-base details (Specification.md: Requirements FR-06)
  - **End stop details:** Detail drawings of end stop configuration, anchoring, clearances (Specification.md: Requirements FR-07)
- Include notes differentiating new works (Tracks 6/7) vs restoration (Track 5) with limits-of-work notation (Specification.md: Requirements FR-02)
- Note design assumptions explicitly on drawings (traceable to inputs/assumptions register from Step 3)
- Cross-reference material/workmanship notes to DEL-07.02 (when available)

**Outputs:**
- Draft drawing set (all anticipated artifacts)

**Verification:**
- All anticipated artifacts produced (Specification.md: Requirements FR-01)
- Limits-of-work notation clear and complete (Specification.md: Requirements FR-02)
- Assumptions noted on drawings (Specification.md: Requirements QR-03)

**Cross-Reference:**
- Datasheet.md: Content (Anticipated Artifacts, Additional Drawing Content Requirements); Specification.md: Requirements (Functional); Guidance.md: Examples, Considerations (Scope and Limits of Work, Drawing Content and Clarity)

(Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:265)

---

### Step 5: Consistency Cross-Checks

**Action:**
- Cross-check drawing content consistency with DEL-07.02 (Rail Works Technical Specification) once available:
  - Verify material/workmanship notes align with technical specification
  - Resolve any conflicts; update inputs/assumptions register if changes required
  - Document cross-check results
- Cross-check drawing content consistency with DEL-07.03 (Rail Works Design Calculations) once available:
  - Verify design loads, geometry, and assumptions align with calculation basis
  - Trace drawing assumptions to specific calculations (update inputs/assumptions register)
  - Resolve any conflicts; document cross-check results
- If DEL-07.02 or DEL-07.03 not yet available, note cross-checks as **TBD** for future iteration

**Outputs:**
- Cross-check notes / consistency verification records
- Updated inputs/assumptions register (tracing drawing assumptions to DEL-07.03)

**Verification:**
- No unresolved conflicts with DEL-07.02 or DEL-07.03 (Specification.md: Requirements FR-03, PR-01, PR-02)
- Assumptions traceable to DEL-07.03 or tagged **ASSUMPTION** (Specification.md: Requirements QR-03)

**Cross-Reference:**
- Datasheet.md: References (Related Deliverables); Specification.md: Requirements FR-03, PR-01, PR-02, QR-03; Verification (Performance, Quality); Guidance.md: Considerations (Coordination and Dependencies)

(Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:266-267)

---

### Step 6: QA/QC Checks and Document Control Application

**Action:**
- Perform checks per project QA/QC process (to be confirmed from ER requirements):
  - Self-check (drafter review)
  - Discipline check (structural engineer review)
  - Interface / IDC check (coordination with adjacent disciplines)
- Review drawing checklists for completeness, clarity, constructability
- Resolve review comments; update drawings and inputs/assumptions register as needed
- Apply document control rules:
  - Assign drawing numbers per project numbering scheme (**TBD**)
  - Populate title blocks with revision, issue status, metadata
  - Prepare issue transmittal

**Outputs:**
- Drawing checklists (self-check, discipline check, IDC check)
- Review comment logs and responses
- Updated drawing set with document control metadata applied
- Issue transmittal / document control submission record

**Verification:**
- QA/QC checks completed per ER requirements (Specification.md: Requirements QR-02)
- Document control rules applied (Specification.md: Requirements QR-01)
- All review comments resolved or carried forward with approval

**Cross-Reference:**
- Datasheet.md: Attributes (Drawing Set Metadata); Specification.md: Requirements QR-01, QR-02; Standards (Document control, QA/QC procedures); Verification (Quality, constructability/clarity check)

(Source: test/Volume_2_Part_1_Employers_Requirements.pdf, clauses TBD)

---

### Step 7: Package and Issue

**Action:**
- Package drawing set for submission through document control:
  - Final drawing set (all sheets with metadata and document control applied)
  - Drawing sheet index (sheet list)
  - Inputs/assumptions register
  - Drawing checklists and review comment logs
  - Issue transmittal
- Submit per project document control workflow
- Retain all check records and supporting documentation per ER requirements

**Outputs:**
- Issued drawing package (transmitted to recipient per document control workflow)
- Retained records (checklists, cross-checks, inputs/assumptions register, transmittals)

**Verification:**
- Drawing package complete and transmitted per document control workflow
- Records retained per ER requirements

**Cross-Reference:**
- Specification.md: Documentation; Verification-to-Records Mapping; Records section below

(Source: test/Volume_2_Part_1_Employers_Requirements.pdf, clauses TBD)

## Verification

Verification activities are integrated throughout the Procedure steps. Summary of verification checkpoints:

| Verification Checkpoint | Performed In | Verification Method | Acceptance Criterion | Cross-Reference |
|------------------------|--------------|---------------------|---------------------|-----------------|
| **Scope and completeness** | Step 1 | Sheet list review against anticipated artifacts | All anticipated artifacts covered in sheet list | Specification.md: Requirements FR-01; Verification |
| **Interface coordination** | Step 2 | Coordination records review | Interface expectations confirmed per external workflow | Specification.md: Requirements IR-01, IR-02; Verification |
| **Assumption traceability** | Step 3 | Inputs/assumptions register review | All assumptions documented and traceable or tagged **ASSUMPTION** | Specification.md: Requirements QR-03; Verification |
| **Draft content completeness** | Step 4 | Draft drawing review against requirements | All anticipated artifacts produced; limits-of-work notation clear | Specification.md: Requirements FR-01, FR-02, FR-04 to FR-07; Verification |
| **Consistency (DEL-07.02)** | Step 5 | Cross-check against technical specification | No unresolved conflicts with materials/workmanship requirements | Specification.md: Requirements FR-03, PR-01; Verification |
| **Consistency (DEL-07.03)** | Step 5 | Cross-check against design calculations | No unresolved conflicts; assumptions traced to calculations | Specification.md: Requirements FR-03, PR-02, QR-03; Verification |
| **QA/QC checks** | Step 6 | Drawing checklists (self, discipline, IDC) | All checks completed; review comments resolved | Specification.md: Requirements QR-02; Verification |
| **Document control compliance** | Step 6 | Document control metadata review | Drawing numbers, revisions, metadata populated per ER requirements | Specification.md: Requirements QR-01; Verification |
| **Package completeness** | Step 7 | Submission package review | Drawing package complete with all supporting records | Specification.md: Documentation; Verification-to-Records Mapping |

**Overall acceptance:**
- All verification checkpoints satisfied per Specification.md: Verification (Acceptance Criteria)
- All **TBD** items resolved or explicitly carried forward with approval
- All **ASSUMPTION** items traced or tagged and approved

(Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:265, :266-267; test/Volume_2_Part_1_Employers_Requirements.pdf, clauses TBD)

## Records

### Primary Deliverable Outputs

| Record | Description | Generated In | Cross-Reference |
|--------|-------------|--------------|-----------------|
| Track layout plans | Plan view drawings showing track arrangement for Tracks 5, 6, 7 | Step 4 | Datasheet.md: Content; Specification.md: Scope (Anticipated Artifacts); Guidance.md: Examples |
| Rail profiles | Longitudinal profile drawings showing rail elevations and geometry | Step 4 | Datasheet.md: Content; Specification.md: Scope (Anticipated Artifacts); Guidance.md: Examples |
| Ballast sections | Cross-section drawings showing ballast details | Step 4 | Datasheet.md: Content; Specification.md: Scope (Anticipated Artifacts); Guidance.md: Examples |
| End stop details | Detail drawings of end stop configuration and anchoring | Step 4 | Datasheet.md: Content; Specification.md: Scope (Anticipated Artifacts); Guidance.md: Examples |

(Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:265)

### Supporting Documentation Records

| Record | Description | Generated In | Retention | Cross-Reference |
|--------|-------------|--------------|-----------|-----------------|
| Drawing sheet index | Sheet list identifying all drawings in the set | Step 1, updated through Step 4 | Retained with deliverable package | Specification.md: Verification-to-Records Mapping |
| Inputs/assumptions register | Register documenting inputs used, inputs **TBD**, assumptions made, and assumption traceability | Step 3, updated in Steps 4, 5 | Retained with deliverable package | Specification.md: Requirements QR-03; Verification-to-Records Mapping |
| Coordination records | Meeting notes, interface confirmations, external coordination evidence | Step 2 | Retained per project records management | Specification.md: Requirements IR-02; Verification-to-Records Mapping |
| Cross-check notes | Consistency verification records vs DEL-07.02 and DEL-07.03 | Step 5 | Retained with deliverable package | Specification.md: Verification-to-Records Mapping |
| Drawing checklists | Self-check, discipline check, IDC check checklists | Step 6 | Retained per ER QA requirements (clauses **TBD**) | Specification.md: Requirements QR-02; Verification-to-Records Mapping |
| Review comment logs | Review comments and responses | Step 6 | Retained per ER QA requirements (clauses **TBD**) | Specification.md: Verification-to-Records Mapping |
| Issue transmittals | Document control submission records | Step 7 | Retained per ER document control requirements (clauses **TBD**) | Specification.md: Requirements QR-01; Verification-to-Records Mapping |

(Source: test/Volume_2_Part_1_Employers_Requirements.pdf, clauses TBD)

## Cross-Document Notes

### Procedure ↔ Specification

| Procedure Section | Specification Section | Relationship |
|-------------------|----------------------|--------------|
| Steps 1-7 (all steps) | Requirements (all categories) | Procedure steps operationalize Specification requirements into actionable workflow |
| Verification (summary table) | Verification (methods and criteria) | Procedure verification checkpoints implement Specification verification methods |
| Records | Documentation, Verification-to-Records Mapping | Procedure records satisfy Specification documentation requirements and provide verification evidence |

### Procedure ↔ Datasheet

| Procedure Section | Datasheet Section | Relationship |
|-------------------|-------------------|--------------|
| Prerequisites (Scope Confirmation) | Conditions (Context & Scope), Content (Anticipated Artifacts) | Prerequisites ensure scope alignment with Datasheet scope and content definitions |
| Steps 1, 4 | Content (Anticipated Artifacts, Additional Drawing Content Requirements) | Steps produce artifacts and content defined in Datasheet |
| Steps 6 (document control) | Attributes (Drawing Set Metadata) | Step 6 populates metadata attributes defined in Datasheet |
| Records (Primary Deliverable Outputs) | Content (Anticipated Artifacts) | Records produced match anticipated artifacts listed in Datasheet |

### Procedure ↔ Guidance

| Procedure Section | Guidance Section | Relationship |
|-------------------|------------------|--------------|
| Prerequisites (Dependencies and Coordination) | Considerations (Coordination and Dependencies) | Prerequisites align with coordination guidance |
| Steps 3 (inputs/assumptions register) | Principles (Assumption transparency), Trade-offs (Assumption visibility) | Step 3 implements assumption transparency principle from Guidance |
| Steps 4 (draft production) | Examples, Considerations (Drawing Content and Clarity) | Step 4 applies examples and content/clarity considerations from Guidance |
| Steps 5 (cross-checks) | Considerations (Coordination and Dependencies) | Step 5 implements cross-check coordination guidance |
| Verification (all checkpoints) | Principles, Considerations, Trade-offs | Verification applies engineering judgment informed by Guidance |
