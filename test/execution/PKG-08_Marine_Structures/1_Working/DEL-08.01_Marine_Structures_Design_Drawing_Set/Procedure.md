# Procedure: DEL-08.01 Marine Structures Design Drawing Set

## Purpose

This procedure defines a **repeatable production workflow** for the Marine Structures Design Drawing Set deliverable. It describes the steps to produce the drawing set from initial setup through final issue, including verification steps aligned to the Specification requirements.

**Deliverable intent (source-anchored):** Defines the design arrangement and details for marine structures per ER requirements. *(Source: Decomposition line 281 + `_CONTEXT.md`; specific ER clause locations TBD)*

**Package scope context (source-anchored):** PKG-08 covers piling, access trestle, loading platform structure, catwalk, and abutments. *(Source: Decomposition line 275)*

---

## Prerequisites

### Dependencies

**Dependency tracking mode:** NOT_TRACKED *(per `_DEPENDENCIES.md`)*

Dependencies are coordinated externally by humans (see `test/execution/_Coordination/_COORDINATION.md`).

**Note:** Even though dependencies are NOT_TRACKED, the following upstream deliverables and inputs are anticipated to be required before this deliverable can be finalized. Coordination of timing and availability is managed externally:

- **DEL-08.04 Marine Geotechnical Report** — provides geotechnical parameters (pile capacity, soil layering) and bathymetric survey results (seabed levels, obstructions) required for piling layout and elevation design
- **DEL-08.03 Marine Structures Design Calculations** — provides engineering basis and sizing to support drawing content
- **DEL-09.01 Marine Outfitting Design Drawing Set** — provides fender/bollard/ladder interface details affecting platform/trestle drawings
- **DEL-11.01 Marine Loading Design Drawing Set** — provides loading arm and operator shelter interface details affecting platform drawings
- **Civil/Structural Works deliverables** — provide abutment tie-in details and landside access interface details
- **ER clauses extraction** — ER Vol 2 Parts 1-2 clauses applicable to marine structures must be identified
- **Project document control procedures and CAD standards** — required to establish drawing numbering, revision scheme, title block template, layer naming, etc.

### Inputs / References (TBD)

The following inputs/references are **TBD** and must be available before drawing production can commence:

| Input / Reference | Required For | Status |
|---|---|---|
| Employer's Requirements clauses for marine structures | R-002 compliance; code/standard identification | **TBD** *(ER Vol 2 Parts 1-2 PDFs available; clause extraction pending)* |
| Project document control requirements | R-003 compliance; drawing numbering, revision scheme, title block | **TBD** *(location in ER or project procedures TBD)* |
| Project CAD/BIM standards | Drawing setup; layer naming; coordinate system; sheet templates | **TBD** *(location in ER or project procedures TBD)* |
| Project survey control basis | R-005 compliance; coordinate system and vertical datum | **TBD** *(required for marine structures positioning and elevation control)* |
| Design basis inputs (from various sources) | Drawing content | **TBD** *(vessel data, environmental loads, geotechnical results, equipment loads/envelopes)* |

---

## Procedure Steps (Production Workflow)

These steps are a **PROPOSAL** pending confirmation against ER and project QA/QC procedures. Actual workflow may vary based on project-specific requirements and practices.

### Step 1: Setup and Planning

**Objective:** Establish drawing framework and confirm scope coverage.

**Actions:**
1. Review `Specification.md` R-001 to confirm minimum required drawing artifacts:
   - Piling layout
   - Trestle general arrangement (GA)
   - Platform GA
   - Catwalk drawings
   - Abutment drawings
2. Review PKG-08 scope (Decomposition line 275) to confirm all scope elements covered: piling, access trestle, loading platform structure, catwalk, abutments
3. Develop preliminary drawing list/index with proposed drawing numbers, titles, and scope coverage
4. Confirm drawing numbering scheme and title block template per project CAD standard *(TBD)*
5. Set up CAD/BIM environment per project CAD standard (layer naming, coordinate system, sheet templates) *(TBD)*

**Verification:**
- Drawing list covers all scope elements per R-001
- Drawing numbering scheme complies with project document control requirements *(TBD from R-003)*

**Outputs:**
- Preliminary drawing list/index
- CAD/BIM environment set up and ready

**Sources:**
- `Specification.md` R-001, R-003
- `Guidance.md` § Scope Coverage Checklist
- Project CAD standard *(TBD)*

---

### Step 2: ER Requirements Capture and Code/Standard Identification

**Objective:** Identify and document all applicable ER requirements and codes/standards for marine structures.

**Actions:**
1. Review ER Vol 2 Parts 1-2 to identify clauses applicable to marine structures *(TBD)*
2. Extract ER requirements for marine structures drawings (content, standards, approvals, submittals) *(TBD)*
3. Identify codes/standards required by ER (likely: CSA S6, CSA S16, API, ISO marine standards) *(TBD)*
4. Document ER requirements and codes/standards in a requirements matrix or compliance checklist
5. Update drawing general notes to reference applicable codes/standards

**Verification:**
- All applicable ER clauses identified and documented
- Codes/standards identified and noted on drawings or in general notes
- Requirements matrix/checklist prepared for compliance tracking

**Outputs:**
- ER requirements matrix or compliance checklist
- Codes/standards list for drawing general notes

**Sources:**
- `Specification.md` R-002
- `Guidance.md` § Requirement Rationale Map, R-002
- ER Vol 2 Parts 1-2 PDFs *(TBD)*

---

### Step 3: Interface Coordination and Design Basis Confirmation

**Objective:** Confirm interface details and design basis inputs required for drawing content.

**Actions:**
1. Review `Guidance.md` § Interface Coordination Checklist to identify required interfaces
2. Coordinate with interfacing disciplines/packages to obtain interface information:
   - PKG-09 Marine Outfitting: fender/bollard/ladder locations, loads, mounting details *(TBD)*
   - PKG-11 Marine Loading System: loading arm location, envelope, support details; operator shelter location/loads *(TBD)*
   - Civil/Structural Works: abutment tie-in details, landside access, utilities penetrations *(TBD)*
3. Obtain design basis inputs from upstream deliverables:
   - DEL-08.04 Marine Geotechnical Report: geotechnical parameters, bathymetric survey *(TBD)*
   - DEL-08.03 Marine Structures Design Calculations: structural sizing, pile capacity *(TBD)*
   - DEL-08.06 Berthing Energy Calculation Report: berthing loads *(TBD if required)*
   - ER or other sources: vessel characteristics, environmental loads, design water levels *(TBD)*
4. Document interface agreements and design basis inputs in design basis memorandum or interface register
5. Update `Guidance.md` § Interface Coordination Checklist with coordination status

**Verification:**
- All interfaces identified in `Guidance.md` checklist are addressed (confirmed or marked TBD with coordination plan)
- Design basis inputs required for drawing content are available or documented as TBD
- Interface agreements documented and traceable

**Outputs:**
- Interface coordination register or meeting minutes
- Design basis memorandum or inputs summary
- Updated `Guidance.md` § Interface Coordination Checklist

**Sources:**
- `Specification.md` R-004
- `Guidance.md` § Interface Coordination Checklist, § Requirement Rationale Map R-004
- Interface coordination meetings with PKG-09, PKG-11, civil/structural leads
- DEL-08.03, DEL-08.04, DEL-08.06 (upstream deliverables) *(TBD)*

---

### Step 4: Draft Drawings

**Objective:** Produce initial draft drawings to satisfy `Specification.md` R-001 scope coverage and R-005 technical content requirements.

**Actions:**
1. Draft **Piling Layout** drawing(s):
   - Show pile locations in plan with coordinates
   - Show pile elevations (top-of-pile, cut-off, tip) referenced to project vertical datum *(TBD)*
   - Include pile schedule with pile type, size, material, capacity (from DEL-08.03 calculations) *(TBD)*
   - Note geotechnical parameters or reference DEL-08.04 Marine Geotechnical Report
2. Draft **Trestle GA** drawing(s):
   - Show trestle plan, elevation, and key sections
   - Show structural framing and member sizes (from DEL-08.03 calculations) *(TBD)*
   - Dimension key spans, clearances, and elevations
   - Show abutment connections and landside interface (coordinate with civil/structural) *(TBD)*
3. Draft **Platform GA** drawing(s):
   - Show platform plan, elevation, and key sections
   - Show structural framing and member sizes (from DEL-08.03 calculations) *(TBD)*
   - Show equipment support locations and envelopes (loading arm, operator shelter, fenders, bollards) *(TBD from PKG-09, PKG-11)*
   - Dimension key dimensions, clearances, and elevations
   - Show access provisions (stairs, ladders, catwalks)
4. Draft **Catwalk** drawing(s):
   - Show catwalk layout in plan and elevation
   - Show support details and connection to platform/trestle
   - Show handrail and safety details (height, spacing, materials)
   - Dimension key dimensions and clearances
5. Draft **Abutment** drawing(s):
   - Show abutment plan, elevation, and sections
   - Show tie-in details to landside structures (coordinate with civil/structural) *(TBD)*
   - Show connection details to trestle
   - Dimension key dimensions and elevations
6. For all drawings, include per `Specification.md` R-005:
   - Coordinate system and vertical datum reference
   - Key dimensions and elevations
   - Materials notes or reference to DEL-08.02 Marine Structures Technical Specification
   - General notes (codes/standards, tolerances, welding/fabrication standards, inspection requirements) *(TBD)*
   - Legends and symbols as required
7. Mark TBD items explicitly on drawings where information is not yet available (e.g., interface details, final elevations, equipment envelopes)

**Verification:**
- All scope elements per `Specification.md` R-001 are covered
- Technical content per `Specification.md` R-005 is included
- TBD items are clearly marked with notes

**Outputs:**
- Draft drawing set (piling layout, trestle GA, platform GA, catwalk drawings, abutment drawings)

**Sources:**
- `Specification.md` R-001, R-005
- `Guidance.md` § Scope Coverage Checklist, § Requirement Rationale Map R-005
- DEL-08.02 Marine Structures Technical Specification *(for materials/specs cross-reference)*
- DEL-08.03 Marine Structures Design Calculations *(for sizing/member sizes)*
- DEL-08.04 Marine Geotechnical Report *(for geotechnical parameters, bathymetric survey)*
- Interface coordination results from Step 3

---

### Step 5: Originator Self-Check

**Objective:** Verify compliance with `Specification.md` requirements R-001 through R-005 before submittal for review.

**Actions:**
1. Review drawings against `Specification.md` requirement verification map:
   - **R-001:** Confirm all required drawing artifacts present; drawing list/index complete
   - **R-002:** Confirm ER requirements addressed; codes/standards noted
   - **R-003:** Confirm drawing numbering, revision status, title blocks comply with project document control
   - **R-004:** Confirm interfaces shown/noted; coordination status documented
   - **R-005:** Confirm technical content adequate (coordinate system, dimensions, materials, notes, legends)
2. Check cross-document consistency with related deliverables:
   - Cross-check with DEL-08.02 Specification for materials/specs consistency
   - Cross-check with DEL-08.03 Calculations for sizing/capacity consistency
   - Cross-check with DEL-08.04 Geotechnical Report for geotechnical parameters consistency
3. Check for internal drawing consistency:
   - Dimensions and elevations consistent across plan/elevation/section views
   - Cross-references between drawings correct
   - Symbols and abbreviations consistent and defined in legends
4. Document self-check results in self-check checklist or markup set

**Verification:**
- Self-check checklist completed
- All non-conformances corrected or documented as TBD with resolution plan

**Outputs:**
- Self-check checklist or markup set
- Corrected draft drawings

**Sources:**
- `Specification.md` § Requirement Verification Map
- `Guidance.md` § Scope Coverage Checklist, § Interface Coordination Checklist

---

### Step 6: Interdisciplinary Coordination (IDC) Check

**Objective:** Coordinate with interfacing disciplines to verify interface compatibility and resolve interface issues.

**Actions:**
1. Distribute draft drawings to interfacing disciplines/packages for IDC review:
   - PKG-09 Marine Outfitting (for fender/bollard/ladder interfaces)
   - PKG-11 Marine Loading System (for loading arm/operator shelter interfaces)
   - Civil/Structural Works (for abutment tie-ins, landside access, utilities)
   - Other disciplines as required (electrical, instrumentation, process, etc.)
2. Hold IDC coordination meeting(s) to review interface comments and resolve issues
3. Collect IDC comments and document resolutions in IDC comment register
4. Update drawings to incorporate IDC comment resolutions
5. Update `Guidance.md` § Interface Coordination Checklist with final coordination status

**Verification:**
- All IDC comments collected and documented
- All IDC comments resolved or dispositioned with agreement of interfacing disciplines
- Interface Coordination Checklist updated

**Outputs:**
- IDC comment register with resolutions
- Updated drawings incorporating IDC resolutions
- Updated `Guidance.md` § Interface Coordination Checklist

**Sources:**
- `Specification.md` R-004
- `Guidance.md` § Interface Coordination Checklist, § Requirement Rationale Map R-004
- IDC coordination meetings with interfacing disciplines

---

### Step 7: Discipline Check / Independent Check

**Objective:** Obtain senior engineer or independent checker review for technical adequacy and code compliance.

**Actions:**
1. Submit drawings for discipline check (senior marine engineer or discipline lead review):
   - Verify technical adequacy and completeness
   - Verify compliance with codes/standards
   - Verify compliance with ER requirements
   - Verify constructability and operability
2. If required by project, submit drawings for independent check:
   - Independent checker (not involved in design) reviews drawings for compliance with ER, codes, and project procedures
3. Collect discipline check and/or independent check comments
4. Resolve comments and update drawings
5. Obtain discipline check and/or independent check sign-off

**Verification:**
- Discipline check and/or independent check completed
- All comments resolved or dispositioned
- Sign-offs obtained

**Outputs:**
- Discipline check and/or independent check comment register with resolutions
- Updated drawings incorporating check resolutions
- Check sign-off records

**Sources:**
- `Specification.md` § Verification and Acceptance
- Project QA/QC procedures *(TBD)*
- ER requirements for review/approval *(TBD)*

---

### Step 8: Prepare for Issue

**Objective:** Finalize drawings and prepare drawing package for issue.

**Actions:**
1. Update drawing register/index with final drawing numbers, titles, revisions, dates
2. Update drawing title blocks:
   - Set revision status to issue revision (e.g., "0" for first issue) per project document control *(TBD)*
   - Set issue status (e.g., "Issued for Construction", "Issued for Approval") per project requirements *(TBD)*
   - Obtain required approvals and signatures on title blocks per project procedures *(TBD)*
   - Update date to issue date
3. Verify all drawings in package are at same revision and issue status
4. Prepare drawing transmittal or cover letter per project document control *(TBD)*
5. Assemble issue package:
   - Drawing register/index
   - All drawings in drawing set
   - Drawing transmittal or cover letter
   - Supporting documentation if required (calculations summary, compliance matrix, etc.) *(TBD)*
6. Perform final QA check of issue package (correct drawings, correct revision, complete package)

**Verification:**
- Drawing register/index complete and accurate
- All drawings at correct revision and issue status
- Title blocks complete with required approvals
- Issue package complete and correct

**Outputs:**
- Final drawing register/index
- Final drawing set ready for issue
- Drawing transmittal or cover letter
- Issue package assembled

**Sources:**
- `Specification.md` R-003, § Documentation / Deliverable Outputs
- Project document control procedures *(TBD)*

---

### Step 9: Issue and Archive

**Objective:** Issue drawing package to Employer (or other recipient) and archive issue records.

**Actions:**
1. Issue drawing package per project document control procedures:
   - Submit to Employer via project document management system or transmittal *(TBD)*
   - Obtain issue receipt or acknowledgment *(TBD)*
2. Copy issued drawing package to `test/execution/PKG-08_Marine_Structures/3_Issued/` folder:
   - Include drawing set, drawing register, transmittal, and any supporting documentation
   - Name files with deliverable ID, revision, and date (e.g., `DEL-08.01_Rev0_2026-01-28.pdf`)
3. Update `_STATUS.md` to ISSUED with issue date and revision in history entry
4. Archive working files and review records:
   - Self-check records
   - IDC comment register
   - Discipline check / independent check records
   - Approval records
   - Store in project archive per project records management procedures *(TBD)*

**Verification:**
- Drawing package issued and receipt confirmed
- Issued package copied to `3_Issued/` folder
- `_STATUS.md` updated to ISSUED
- Records archived

**Outputs:**
- Issued drawing package (in project document management system and `3_Issued/` folder)
- Updated `_STATUS.md`
- Archived working files and review records

**Sources:**
- Project document control procedures *(TBD)*
- Project records management procedures *(TBD)*

---

## Requirement Coverage Map

This table maps each `Specification.md` requirement to the procedure step(s) that address it and the expected verification evidence:

| Spec ID | Requirement | Covered by Step(s) | Expected Output / Evidence |
|---|---|---|---|
| R-001 | Drawing set coverage (minimum artifacts and scope elements) | Step 1 (setup/planning), Step 4 (draft drawings), Step 5 (self-check) | Drawing list/index showing all required artifacts; drawings covering all scope elements |
| R-002 | ER-driven requirements capture | Step 2 (ER requirements capture), Step 5 (self-check), Step 7 (discipline check) | ER requirements matrix/checklist; codes/standards noted on drawings; compliance verified |
| R-003 | Document control / metadata | Step 1 (setup/planning), Step 8 (prepare for issue), Step 9 (issue/archive) | Drawing numbering, revision, title blocks compliant; drawing register/index complete |
| R-004 | Interface coordination | Step 3 (interface coordination), Step 6 (IDC check), Step 5 (self-check) | Interface coordination register; IDC comment register with resolutions; interfaces shown/noted on drawings |
| R-005 | Technical content and notation | Step 4 (draft drawings), Step 5 (self-check), Step 7 (discipline check) | Drawings include coordinate system, dimensions, materials, notes, legends; technical content verified adequate |

---

## Verification Summary

Verification/acceptance criteria are **TBD** pending ER and project QA/QC procedures. The following verification approach is **PROPOSED** based on standard EPC practice:

| Verification Activity | Performed In Step | Acceptance Criteria |
|---|---|---|
| Originator self-check | Step 5 | Self-check checklist completed; all Specification requirements verified met or TBD documented |
| Interdisciplinary coordination check | Step 6 | All IDC comments collected, resolved, and dispositioned with interfacing discipline agreement |
| Discipline check | Step 7 | Senior engineer or discipline lead verifies technical adequacy, code compliance, ER compliance, constructability |
| Independent check (if required) | Step 7 | Independent checker verifies compliance with ER, codes, project procedures |
| Approval for issue | Step 8 | Authorized approver signs title blocks; drawing package complete and ready for issue |

**Final acceptance:** Drawing package issued per Step 9 with all required approvals and verifications complete.

---

## Records

### Minimum Expected Deliverable Outputs (per Specification.md)

Per `Specification.md` R-001 and Decomposition line 281:

- Piling layout
- Trestle general arrangement (GA)
- Platform general arrangement (GA)
- Catwalk drawings
- Abutment drawings

### Associated Records (TBD)

Records to retain with the drawing set package or in project archive:

- Drawing register / transmittal — **TBD** *(format and archival location TBD from project document control and records management procedures)*
- Review/IDC markups and dispositions — **TBD**
- Self-check records — **TBD**
- Discipline check / independent check records — **TBD**
- Approval records and sign-offs — **TBD**
- ER requirements matrix / compliance checklist — **TBD**
- Interface coordination register — **TBD**

---

## Sources

- `test/execution/PKG-08_Marine_Structures/1_Working/DEL-08.01_Marine_Structures_Design_Drawing_Set/_CONTEXT.md`
- `test/execution/PKG-08_Marine_Structures/1_Working/DEL-08.01_Marine_Structures_Design_Drawing_Set/_DEPENDENCIES.md`
- `test/execution/PKG-08_Marine_Structures/1_Working/DEL-08.01_Marine_Structures_Design_Drawing_Set/Specification.md`
- `test/execution/PKG-08_Marine_Structures/1_Working/DEL-08.01_Marine_Structures_Design_Drawing_Set/Guidance.md`
- `test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md` (lines 271-291: PKG-08 scope statement at line 275; deliverables table; DEL-08.01 at line 281)
- `test/Volume_2_Part_1_Employers_Requirements.pdf` *(present in repo; content not extracted here; clause locations TBD)*
- `test/Volume_2_Part_2_Employers_Requirements.pdf` *(present in repo; content not extracted here; clause locations TBD)*
- Standard EPC practice for drawing production workflow, QA/QC, and document control
