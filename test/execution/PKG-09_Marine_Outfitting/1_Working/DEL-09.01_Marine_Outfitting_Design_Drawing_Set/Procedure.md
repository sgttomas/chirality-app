# Procedure: DEL-09.01 Marine Outfitting Design Drawing Set

## Purpose

This procedure defines the process for producing and verifying **Marine Outfitting Design Drawing Set** within **PKG-09 Marine Outfitting**.

**Decomposition definition (authoritative):** Defines the design arrangement and details for marine outfitting per Employer's Requirements. (**Source:** Decomposition, DEL-09.01 row)

**Deliverable type:** Drawing
**Responsible party:** D&B Contractor

**Scope:** This procedure covers the production process from scope confirmation through issue preparation, including design development, checking, interdisciplinary coordination, and verification activities.

## Prerequisites

### Dependencies

Dependencies are coordinated externally (NOT_TRACKED). See `_DEPENDENCIES.md` and `execution/_Coordination/_COORDINATION.md`.

**Typical upstream inputs (confirm availability and maturity prior to commencement):**

| Input | Source | Required For | Specification § | Guidance § |
|-------|--------|--------------|-----------------|------------|
| Marine structure design basis and geometry | PKG-08 (DEL-08.01, DEL-08.03) | Fender/bollard interface locations, structural supports | SPEC § 3.1 | Guidance § Principles (Fenders, Bollards) |
| Berthing energy calculation results | DEL-08.06 | Fender selection and sizing basis | SPEC § 1.1 | Guidance § Principles (Fenders) |
| Fender system deflection characteristics | DEL-08.07 | Fender performance data (reaction force vs deflection) | SPEC § 1.1 | Guidance § Principles (Fenders) |
| Fender supplier design verification | DEL-08.08 | Fender suitability confirmation | SPEC § 1.1 | Guidance § Principles (Fenders) |
| Mooring analysis results | DEL-08.09 | Bollard capacities and locations | SPEC § 1.2 | Guidance § Principles (Bollards) |
| Employer's Requirements | Employer | All scope items, materials, standards, acceptance criteria | SPEC § Standards | — |
| Site survey / as-built for Berth 10 | Survey | Existing works scope and tie-in constraints | SPEC § 1.5 | Guidance § Considerations (Existing Works) |
| Vendor data (fenders, bollards, ladders) | Vendor/Supplier | Installation details, fixing requirements, product specifications | SPEC § 1.1, 1.2, 1.3 | — |

### Reference Materials

- See `_REFERENCES.md` for applicable reference documents.
- See `0_References/` in package directory (`test/execution/PKG-09_Marine_Outfitting/0_References/`) for reference materials and reference index.
- Employer's Requirements (Vol 2 Part 1–3) — **TBD** (clauses applicable to marine outfitting to be extracted during design development).
- Applicable codes and standards — **TBD** (as specified by Employer's Requirements and approvals; see `Specification.md § Standards` for assumed standards list).

### Personnel Requirements

| Role | Requirement |
|------|-------------|
| Originator (Lead Designer) | Qualified Marine discipline personnel with experience in marine terminal design and marine outfitting — **TBD** (qualifications per project quality plan) |
| Checker/Reviewer | Checker qualifications — **TBD** (independent of originator; qualified in Marine discipline or relevant experience) |
| IDC participants | Representatives from interfacing disciplines (PKG-08 Marine Structures, PKG-11 Marine Loading, Process/Mechanical, others as applicable) |
| Approver | **TBD** — per project authority matrix (typically Marine discipline lead or Package Manager) |

**ASSUMPTION:** Personnel competency and authority per project quality procedures and authority matrix.

### Tools and Resources

| Tool/Resource | Purpose | Status |
|---------------|---------|--------|
| CAD/BIM software | Drawing production | **TBD** — project-standard software (e.g., AutoCAD, MicroStation, Revit) |
| Project document control system | Document numbering, revision control, transmittal | **TBD** — system to be established |
| Project CAD standard | Line weights, layers, annotation, title blocks, sheet templates | **TBD** — standard to be established |
| Site coordinate system and datum | Setting-out and coordination with PKG-08 | **TBD** — coordinate system to be confirmed with survey/PKG-08 |

## Steps

### Step 1: Confirm Scope

**Objective:** Establish the drawing list and confirm scope boundaries.

**Actions:**
1. Review PKG-09 scope items and DEL-09.01 anticipated artifacts from the decomposition:
   - Fender arrangement drawings
   - Bollard installation details
   - Ladder details
2. Review `Datasheet.md` Content Checklist for minimum drawing content requirements.
3. Review Employer's Requirements for additional drawings needed beyond the decomposition list (e.g., life-saving equipment details, Berth 10 repair details, equipment schedules).
4. Review `Specification.md § 1` (Content Requirements) to confirm all required content items.
5. Confirm interface scope boundaries with PKG-08 Marine Structures (where does structural design end and outfitting begin?).
6. Document any scope clarifications or additional items identified.
7. Prepare preliminary drawing list with sheet titles and anticipated content.

**Inputs:** Decomposition, `Datasheet.md`, `Specification.md`, Employer's Requirements.
**Outputs:** Confirmed drawing list; scope clarification notes (if any).
**Verification:** Drawing list addresses all `Datasheet.md` Content Checklist items and `Specification.md § 1` requirements.

### Step 2: Gather Inputs

**Objective:** Collect all design inputs required for drawing development.

**Actions:**
1. Collect design inputs per Prerequisites table above:
   - Request PKG-08 interface information (marine structure geometry, structural capacities, connection details)
   - Obtain berthing energy analysis results (DEL-08.06) and fender system data (DEL-08.07, DEL-08.08)
   - Obtain mooring analysis results (DEL-08.09)
   - Obtain site survey/as-built data for existing Berth 10 works
2. Extract applicable clauses from Employer's Requirements related to:
   - Fender system performance requirements
   - Bollard capacity and spacing requirements
   - Ladder and access design standards
   - Life-saving equipment requirements
   - Materials and corrosion protection requirements
   - Quality assurance and testing requirements
3. Obtain vendor data for selected fender, bollard, and ladder systems (if pre-selected; otherwise identify selection criteria).
4. Log missing inputs as **TBD** with action owners and target dates.
5. Establish input register to track receipt and maturity of inputs.

**Inputs:** Decomposition, `_REFERENCES.md`, Prerequisites list.
**Outputs:** Input register / status log; extracted ER clauses; vendor data (as available); missing inputs log with action owners.
**Verification:** Input register is complete and reviewed with Project Manager or Package Lead; missing inputs have action owners assigned.

### Step 3: Develop Arrangement

**Objective:** Produce preliminary layout(s) for marine outfitting elements.

**Actions:**
1. Establish base drawing(s) using PKG-08 marine structure geometry (plan, elevations, sections as needed).
2. Develop preliminary fender arrangement:
   - Position fenders based on berthing energy analysis inputs (DEL-08.06) and fender deflection characteristics (DEL-08.07)
   - Ensure fender coverage across design vessel envelope (consider vessel length, beam, tidal range)
   - Coordinate fender reaction forces with PKG-08 structural capacity
   - Identify fender mounting locations and structural interface points
3. Develop preliminary bollard arrangement:
   - Position bollards based on mooring analysis inputs (DEL-08.09)
   - Ensure bollard coverage for mooring line geometry and operational requirements
   - Coordinate bollard locations with operational access and deck layout
   - Identify bollard foundation locations and structural interface points
4. Develop preliminary ladder arrangement:
   - Position ladders to provide access per operational and emergency egress requirements (coordinate with operational stakeholders if possible)
   - Ensure compliance with safety codes (cage requirements, rest platforms, toe clearance)
   - Coordinate ladder attachment points with PKG-08 structural supports
5. Identify preliminary locations for life-saving equipment (coverage and accessibility).
6. Identify existing Berth 10 repair/upgrade extents based on survey/as-built data and ER requirements.
7. Conduct preliminary interface check with PKG-08 Marine Structures (informal coordination; formal IDC occurs in Step 6).

**Inputs:** PKG-08 geometry (DEL-08.01), berthing energy analysis (DEL-08.06), fender data (DEL-08.07, DEL-08.08), mooring analysis (DEL-08.09), ER requirements, survey/as-built data.
**Outputs:** Preliminary arrangement drawings (plan, elevations, sections as needed); interface coordination notes.
**Verification:** Preliminary arrangement addresses all `Specification.md § 1.1–1.5` content requirements; interfaces to PKG-08 identified.

### Step 4: Detailing

**Objective:** Add installation details, notes, and schedules to complete drawings.

**Actions:**
1. Add fender installation details:
   - Fender type, size, performance characteristics (rated energy absorption, reaction force)
   - Anchorage and mounting details (connection types, fastener specifications, load transfer)
   - Interface details to supporting structure (coordinate with PKG-08)
   - Fender schedule (if multiple fender types/sizes)
2. Add bollard installation details:
   - Bollard type, capacity (rated bollard pull in kN or tonnes)
   - Foundation/anchor details (base plate, anchor bolts, embedment, grouting)
   - Interface details to supporting structure (coordinate with PKG-08)
   - Proof load provisions (if required by ER/codes)
   - Bollard schedule (if multiple bollard types/capacities)
3. Add ladder installation details:
   - Ladder type, materials, dimensions
   - Safety features (cages, rest platforms, toe clearance)
   - Structural attachments (fixing types, capacities)
   - Ladder schedule (if multiple ladder types/locations)
4. Add life-saving equipment details:
   - Equipment types, mounting details
   - Equipment schedule (types, quantities, locations)
5. Add existing Berth 10 repair/upgrade details:
   - Distinguish existing vs new work (line types, hatching, notation)
   - Interface details between existing and new elements
   - Demolition/repair extents and tie-in constraints
6. Add general notes and specifications:
   - Materials and corrosion protection requirements (coordinate with PKG-08)
   - Installation notes (torque requirements, welding specifications, grouting, tolerances)
   - Reference notes linking to technical specifications (DEL-09.02) and other relevant documents
7. Add dimensions, coordinates (setting-out), and annotation per CAD standards.
8. Apply CAD/drafting standards (line weights, layers, title blocks, revision blocks) per project CAD standard.

**Inputs:** Preliminary arrangement drawings (Step 3 outputs), vendor data, ER requirements, PKG-08 interface details, project CAD standard.
**Outputs:** Detailed drawings ready for self-check; equipment schedules; general notes.
**Verification:** All `Datasheet.md` Content Checklist items addressed; all `Specification.md § 1.1–1.6` requirements met; drawings comply with `Specification.md § 2` drafting requirements.

### Step 5: Self-Check

**Objective:** Verify completeness, consistency, and compliance before circulating for IDC/independent check.

**Actions:**
1. Verify coverage against `Datasheet.md` Content Checklist — all items addressed (either resolved or noted as TBD with action owner).
2. Verify compliance with `Specification.md § 1` requirements — all content requirements met or TBD noted with justification.
3. Verify internal drawing consistency:
   - Dimensions sum correctly; coordinates consistent across views
   - References (detail callouts, section cuts) are correct and complete
   - Schedules match drawing content (no missing or extra items)
4. Verify CAD/drafting standards compliance per `Specification.md § 2`:
   - Line weights, layers, annotation per project CAD standard
   - Title blocks, revision blocks, sheet numbering per project document control
   - Units, coordinate system, datums consistent with site survey and PKG-08
5. Verify cross-document consistency:
   - Drawing content aligns with `Specification.md` requirements
   - Design intent aligns with `Guidance.md` principles and considerations
6. Document self-check completion (self-check record/sign-off per project procedures).

**Inputs:** Detailed drawings (Step 4 outputs), `Datasheet.md`, `Specification.md`, `Guidance.md`, project CAD standard.
**Outputs:** Self-check record; self-check comments (if any) resolved; drawings ready for IDC.
**Verification:** Self-check completed and documented; all issues resolved or noted as TBD with action owners.

### Step 6: Interdisciplinary Check (IDC)

**Objective:** Coordinate interfaces and resolve conflicts with other disciplines/packages.

**Actions:**
1. Circulate drawings for IDC to interfacing disciplines (per `Specification.md § 3`):
   - **PKG-08 Marine Structures (mandatory):** Fender/bollard interfaces, structural loads, connection details, structural capacity verification
   - **PKG-11 Marine Loading (if applicable):** Safety zones around loading arms, access clearances
   - **PKG-10 Railcar Unloading (if applicable):** Access clearances, safety zones
   - **Process/Mechanical (if applicable):** Access requirements, operational constraints
   - **Other disciplines as applicable:** Electrical (lighting, grounding), instrumentation, etc.
2. Define IDC scope and focus areas in transmittal (e.g., "Please review fender/bollard interfaces to marine structure; confirm structural capacity for fender reaction forces").
3. Receive and log IDC comments.
4. Review comments with IDC participants and resolve (accept, reject with justification, or negotiate alternative solution).
5. Update drawings to incorporate IDC comment resolutions.
6. Document IDC completion and comment resolution (IDC record, comment resolution log per project procedures).
7. Obtain IDC sign-off from participating disciplines.

**Inputs:** Drawings (Step 5 outputs), `Specification.md § 3` interface requirements.
**Outputs:** IDC record; comment resolution log; updated drawings incorporating IDC resolutions; IDC sign-off.
**Verification:** All IDC comments resolved and documented; interfaces coordinated; no unresolved conflicts.
**TBD:** IDC workflow and sign-off requirements per project procedures.

### Step 7: Independent Check

**Objective:** Verify technical accuracy, code compliance, and ER compliance by independent checker.

**Actions:**
1. Assign independent checker (qualified in Marine discipline; independent of originator per project quality procedures).
2. Provide checker with:
   - Drawings (IDC-resolved version)
   - `Specification.md` (requirements)
   - `Guidance.md` (design rationale)
   - `Datasheet.md` (content checklist)
   - ER requirements and applicable codes/standards
   - Design inputs (berthing energy analysis, mooring analysis, vendor data, etc.)
3. Checker performs independent check per `Specification.md § 4` check criteria:
   - **Technical accuracy:** Design is technically sound; calculations/analyses support design decisions; vendor data correctly applied
   - **ER compliance:** All ER requirements addressed; no deviations without justification
   - **Code compliance:** Fender/bollard design complies with applicable marine/port codes; ladder design complies with safety codes; life-saving equipment complies with regulatory requirements
   - **Completeness:** All `Datasheet.md` Content Checklist items and `Specification.md § 1` requirements addressed
   - **Constructability:** Design is buildable; installation details are clear and complete
4. Receive and log checker comments.
5. Review comments with checker and resolve (accept, reject with justification, or negotiate alternative solution).
6. Update drawings to incorporate checker comment resolutions.
7. Obtain checker sign-off (acceptance that design meets requirements and is ready for issue).

**Inputs:** Drawings (Step 6 outputs), all design inputs and references, `Datasheet.md`, `Specification.md`, `Guidance.md`, ER requirements, codes/standards.
**Outputs:** Checker comments; comment resolution log; updated drawings incorporating checker resolutions; checker sign-off.
**Verification:** Checker sign-off obtained; all checker comments resolved and documented.
**TBD:** Independent check acceptance criteria and sign-off requirements per project quality procedures.

### Step 8: Issue Preparation

**Objective:** Prepare drawing package for issue (review/approval or construction).

**Actions:**
1. Apply final document control:
   - Assign drawing numbers per project numbering system (if not already assigned)
   - Apply revision designations per project revision scheme (e.g., Rev 0 for first issue, Rev A/B/C for subsequent revisions)
   - Update title blocks and revision blocks
2. Prepare issue package per `Specification.md § Documentation`:
   - **Format:** PDF for review/approval; native CAD files for construction (per project requirements)
   - **Transmittal:** Prepare transmittal cover sheet listing drawing numbers, titles, revisions, purpose of issue (e.g., "For Review," "For Approval," "For Construction")
3. Prepare issue records:
   - Self-check record (Step 5)
   - IDC record and comment resolution log (Step 6)
   - Checker sign-off and comment resolution log (Step 7)
4. Update `_STATUS.md` when ready for CHECKING or ISSUED state:
   - **CHECKING:** Drawings issued for review/approval (placed in `2_Checking/To/`)
   - **ISSUED:** Drawings approved and issued for construction (placed in `3_Issued/`)
5. Archive previous revisions (if applicable) per project records management procedures.

**Inputs:** Drawings (Step 7 outputs), all check/sign-off records, project document control procedures.
**Outputs:** Issue-ready drawing package; transmittal; updated `_STATUS.md`; archived records.
**Verification:** Drawing package is complete and complies with project document control requirements; `_STATUS.md` updated correctly.
**TBD:** Project document control procedures and issue protocols.

## Verification

**Summary of verification activities performed throughout this procedure:**

| Activity | Step | Criteria | Sign-off |
|----------|------|----------|----------|
| Scope confirmation | Step 1 | Drawing list addresses all `Datasheet.md` Content Checklist items and `Specification.md § 1` requirements | Originator |
| Input completeness | Step 2 | All required inputs received or TBD with action owners | Originator / Package Lead |
| Arrangement adequacy | Step 3 | Preliminary arrangement addresses all content requirements; interfaces identified | Originator |
| Detailing completeness | Step 4 | All details, notes, schedules complete per `Specification.md § 1, 2` | Originator |
| Self-check | Step 5 | Completeness, consistency, CAD standards compliance | Originator |
| Interdisciplinary check (IDC) | Step 6 | Interface coordination; no conflicts with other disciplines | IDC participants |
| Independent check | Step 7 | Technical accuracy, ER compliance, code compliance, completeness | Checker |
| Issue readiness | Step 8 | Drawing package complete and complies with document control requirements | Approver |

**Sign-off requirements (per project quality procedures):**

| Role | Signature | Purpose |
|------|-----------|---------|
| Originator | Required | Confirms self-check completed; design meets requirements |
| IDC participants | Required | Confirms interfaces coordinated; no unresolved conflicts |
| Checker | Required | Confirms independent check completed; design is technically acceptable |
| Approver | Required | Authorizes issue for intended purpose (review/approval/construction) |

**ASSUMPTION:** Sign-off protocol and authority matrix per project quality procedures.

## Records

**Documentation outputs (per `Specification.md § Documentation` and `Datasheet.md`):**
- Fender arrangement drawings
- Bollard installation details
- Ladder details
- (Additional drawings as required by ER to fully define PKG-09 scope)

**Record management:**

| Record | Location | Retention | Purpose |
|--------|----------|-----------|---------|
| Draft drawings (in progress) | `1_Working/` | Per project procedures | Working files during development |
| Review package | `2_Checking/To/` | Per project procedures | Issue for review/approval |
| Issued drawings | `3_Issued/` | Per project procedures | Final issue for construction; as-built record |
| Self-check record | Deliverable folder or project QA system | Per project procedures | Evidence of self-check completion |
| IDC record and comment resolution log | Deliverable folder or project QA system | Per project procedures | Evidence of interface coordination |
| Checker sign-off and comment resolution log | Deliverable folder or project QA system | Per project procedures | Evidence of independent check |
| Input register / status log | Deliverable folder | Per project procedures | Tracking of design inputs |

**ASSUMPTION:** Electronic records managed in project document management system with appropriate access controls and backup/retention protocols.

**Cross-reference:** See `Datasheet.md § References` for related documents.
