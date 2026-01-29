# Procedure: DEL-13.01 Storage Tank Design Drawing Set

## Purpose

This procedure defines the process for producing and managing **Storage Tank Design Drawing Set** within **PKG-13 Storage Tanks**.

### Scope of This Procedure

This procedure describes:
1. **Production workflow** — How to develop the tank design drawings from requirements through approval
2. **Quality control** — How to verify drawing accuracy, completeness, and coordination
3. **Document management** — How to issue, revise, and archive the drawings

**Deliverable type:** Drawing
**Responsible party:** D&B Contractor
**Discipline:** Mechanical

**Source:** _CONTEXT.md

---

## Prerequisites

### Dependencies

**Dependency tracking mode:** NOT_TRACKED — Dependencies are coordinated externally by humans (see `execution/_Coordination/_COORDINATION.md`)

**Source:** `_DEPENDENCIES.md`

**Upstream deliverables and input data (typical sequence — TBD: Confirm in project schedule):**
- DEL-27.01 or equivalent: Design Basis Memorandum or Design Criteria — **TBD**
- DEL-02.04: Geotechnical Reports — Foundation bearing capacity and settlement analysis required for Step 2 (Preliminary Design) foundation selection
- Process design information: Tank capacity requirements (15,000 MT per tank), product properties (CSD canola oil specific gravity, temperature range), throughput (1,000,000 MT/annum) — **TBD**
- P&IDs or Process Flow Diagrams — Nozzle requirements and services required for Step 2 (Preliminary Design) and Step 3 (Detailed Design) nozzle schedule development
- Site survey and layout — Tank locations, spacing, elevation datums required for Step 2 (Preliminary Design) — **TBD**
- **Source:** ASSUMPTION based on typical design workflow; requires project schedule coordination

### Reference Materials

**Required references for Step 1 (Design Initiation) and ongoing:**
- Volume 2 Part 1: Employer's Requirements - General Requirements — **Location TBD**
- Volume 2 Part 2: Employer's Requirements - Civil & Process Mechanical Works — **Location TBD**
- API 650: Welded Tanks for Oil Storage — **Location TBD** (required for all design steps)
- API 650 Appendix E: Seismic Design of Storage Tanks — **Location TBD** (required for Step 2 and Step 3)
- API 650 Appendix F: Atmospheric and Low-Pressure Storage Tank Venting — **Location TBD** (required for Step 3 vent design)
- NBC 2020: National Building Code of Canada — **Location TBD** (required for Step 3 wind, snow, seismic loads)
- Project CAD Manual and Drawing Standards — **Location TBD** (required for Step 4: CAD Drafting)
- Project Document Control Procedures — **Location TBD** (required for Steps 10-11: Issuance and Revision Management)

**Source:** Specification.md Standards section; `_REFERENCES.md`

**Related deliverables for coordination (Step 6: Interdisciplinary Check):**
- DEL-13.02: Storage Tank Technical Specification (material and performance requirements)
- DEL-13.03: Storage Tank Design Calculations (sizing, structural, seismic basis for drawings)
- DEL-13.04: Storage Tank Data Sheet Package (tank and agitator data sheets for reference)
- DEL-05.01: Concrete Structures Design Drawing Set (foundation interface coordination)
- DEL-14.01: Process Piping Design Drawing Set (nozzle interface and P&ID alignment)
- DEL-20.01: Field Instrumentation drawings (instrumentation interface coordination)
- PKG-23 Fire Protection drawings (tank spacing and fire protection interface)
- PKG-26 Coating specifications (coating system coordination)

**Source:** Datasheet.md References section; Specification.md Interface Requirements

### Personnel Requirements

**Roles and qualifications:**
- **Design Engineer (Originator):** Professional Engineer (P.Eng.) or Engineer-in-Training under P.Eng. supervision, with API 650 tank design experience — **TBD** per project quality plan
- **Checker (Independent):** Professional Engineer (P.Eng.) independent of originator, minimum same qualifications as originator, API 650 experience
- **Discipline Lead (Approver):** Professional Engineer (P.Eng.) with tank design and multi-discipline project experience
- **CAD Technician (if applicable):** Qualified in project CAD standards and tank drawing production

**Source:** ASSUMPTION based on typical engineering project personnel requirements; requires project quality plan confirmation

### Tools and Systems

**Required software/systems:**
- CAD software per project standards (e.g., AutoCAD, MicroStation) — **TBD** per project CAD manual
- Project document management system (e.g., ProjectWise, SharePoint) — **TBD** per project document control procedures
- Calculation software if used for nozzle reinforcement calculations, seismic analysis — **TBD** (e.g., PV Elite, STAAD)

**Source:** ASSUMPTION based on typical design tools

---

## Steps

### Step 1: Design Initiation and Planning

**Activities:**
1.1. Review Employer's Requirements (ER Volume 2 Parts 1 and 2) for storage tank requirements per Specification.md FR-01 through FR-05
1.2. Review design basis, criteria, and project-specific constraints (site location, seismic zone, environmental loads)
1.3. Confirm tank capacity (3 × 15,000 MT), product properties (CSD canola oil), and operating conditions per Datasheet.md Tank Configuration
1.4. Identify applicable codes and standards (API 650, API 650 Appendices E and F, NBC 2020) per Specification.md Standards section
1.5. Develop design schedule and resource plan (coordinate with project schedule)
1.6. Identify coordination requirements with adjacent disciplines per Specification.md IR-01 through IR-06 and Guidance.md Interface sections

**Inputs:**
- Employer's Requirements (ER Volume 2 Parts 1 and 2) — **TBD**
- Design Basis Memorandum (DEL-27.01 or equivalent) — **TBD**
- Project scope and objectives (Decomposition document Sections 1 and 2)
- Datasheet.md (Tank Configuration, Product, Capacity)
- Specification.md (all requirements sections)
- Guidance.md (Design Philosophy DP-01 through DP-05)

**Outputs:**
- Design work plan with schedule and milestones
- Coordination register identifying interfaces with PKG-05, PKG-14, PKG-20, PKG-23, PKG-26

**Responsibility:** Design Engineer (Mechanical Lead)

**Verification:** Design work plan reviewed and approved by Discipline Lead

**Source:** ASSUMPTION based on typical design initiation process; informed by Guidance.md Design Philosophy

---

### Step 2: Preliminary Design and Sizing

**Activities:**
2.1. Develop preliminary tank sizing based on capacity requirements (15,000 MT per tank) and product specific gravity (TBD per Datasheet.md) per Guidance.md Tank Sizing and Configuration
2.2. Select preliminary tank diameter and height optimizing D/H ratio per Guidance.md Trade-off TD-01 (Diameter vs. Height)
2.3. Perform preliminary shell thickness calculations per API 650 Section 5.6 (hydrostatic design)
2.4. Select roof type (cone, dome, floating) based on product properties (low volatility canola oil) and ER requirements per Guidance.md Trade-off TD-02 (Roof Type Selection) — **TBD**
2.5. Identify foundation type (ring wall, mat, piles) and preliminary sizing per Guidance.md Trade-off TD-03 (Foundation Type) based on geotechnical report DEL-02.04 — **TBD**
2.6. Develop preliminary nozzle schedule based on P&IDs and process requirements (inlet, outlet, vent, drain, overflow, water draw-off, instrumentation) per Specification.md IR-02
2.7. Coordinate with DEL-13.03 (Design Calculations) — provide sizing basis and assumptions, receive preliminary calculation results

**Inputs:**
- Tank capacity: 3 × 15,000 MT (Datasheet.md Tank Configuration)
- Product properties: CSD canola oil specific gravity, temperature range — **TBD** per Datasheet.md Product Specific Gravity
- Geotechnical report (DEL-02.04) for foundation bearing capacity — **TBD**
- P&IDs or process requirements for nozzle schedule — **TBD**
- Specification.md FR-01 (Storage Capacity), PR-01 (API 650 Design Standard)
- Guidance.md Tank Sizing and Configuration, Trade-offs TD-01, TD-02, TD-03

**Outputs:**
- Preliminary tank sizing (diameter, height, shell thickness, roof type, foundation type)
- Preliminary nozzle schedule (nozzle quantities, sizes, services)
- Preliminary foundation requirements (type, loading, anchor bolt requirements if seismic anchorage needed per Guidance.md Trade-off TD-04)

**Responsibility:** Design Engineer

**Verification:** Self-check calculations, peer review of sizing logic, coordination with DEL-13.03

**Source:** ASSUMPTION based on typical tank design workflow; Guidance.md Considerations section; Specification.md PR-01, PR-02

---

### Step 3: Detailed Design Development

**Activities:**
3.1. Finalize tank geometry and shell plate layout (number of courses, thickness per course) based on DEL-13.03 calculations per API 650 Section 5.6
3.2. Complete nozzle schedule with all details: sizes, ratings (Class 150, etc.), orientations (degrees from north), elevations (from tank bottom), services, connection types per Specification.md IR-02 and Datasheet.md Nozzle Schedule
3.3. Design roof structure (rafters, girders, columns if required for rafter-supported roof) per API 650 Section 5.10 and Guidance.md Roof Design
3.4. Design appurtenances per PKG-13 Scope and Specification.md PR-05, PR-06, PR-07:
    - Overflow protection (overflow nozzle location, size) per Guidance.md Overflow Protection
    - Water draw-off (low-point drain nozzle) per Guidance.md Water Draw-off
    - Agitator mounts (nozzle reinforcement, loading provisions) per Guidance.md Agitator Integration
    - Phase 2 connections (identify locations, sizes, protection) per Specification.md FR-05 and Guidance.md Phase 2 Provisions
3.5. Develop foundation interface details (anchor bolt layout if required per TD-04, foundation loading diagram, grout details) per Specification.md IR-01 and Guidance.md Foundation Interface
3.6. Design access provisions (ladders per CSA Z259, platforms, manways per API 650 Table 5.7a) per Datasheet.md Access Provisions
3.7. Coordinate interfaces with adjacent disciplines per Specification.md IR-01 through IR-06:
    - PKG-05 (foundation loads, anchor bolts, dyke/bunding) per Guidance.md Foundation and Dyke/Bunding Interface
    - PKG-14 (nozzle schedule alignment with P&IDs, piping routing) per Guidance.md Piping Interface
    - PKG-20 (instrumentation nozzles, mounting provisions) per Guidance.md Instrumentation Interface
    - PKG-23 (tank spacing for fire protection) per Guidance.md Fire Protection Interface
    - PKG-26 (coating system selection, surface preparation) per Guidance.md Coatings Interface
3.8. Reference design calculations (DEL-13.03) to support all design decisions per Specification.md V-03

**Inputs:**
- Preliminary design from Step 2
- DEL-13.03: Design Calculations (finalized or in progress) for shell thickness, roof design, seismic analysis, wind analysis
- Coordination inputs from PKG-05, PKG-14, PKG-20, PKG-23, PKG-26 per Specification.md Interface Requirements
- Specification.md all requirements sections (FR, PR, IR)
- Guidance.md all considerations and trade-off sections

**Outputs:**
- Finalized tank design ready for CAD drafting:
  - Tank geometry (diameter, height, shell courses) per Datasheet.md Tank Geometry
  - Complete nozzle schedule per Datasheet.md Nozzle Schedule
  - Roof structure details per Datasheet.md Roof Details
  - Foundation interface details per Datasheet.md Foundation Drawings
  - Agitator mounting details per Datasheet.md Agitator Drawings
- Coordination records (IDC comments received and resolved, interface agreements)

**Responsibility:** Design Engineer

**Verification:** Design review meeting per Step 8, interdisciplinary check (IDC) per Step 6 with affected disciplines

**Source:** ASSUMPTION based on typical detailed design process; Specification.md Interface Requirements IR-01 through IR-06; Guidance.md all sections

---

### Step 4: CAD Drafting

**Activities:**
4.1. Prepare CAD drawings per project CAD standards (layers, line weights, symbology, text styles) per Specification.md DR-01 — **TBD** per project CAD manual
4.2. Produce Tank General Arrangements (3 drawings, one per tank) per Datasheet.md Anticipated Drawing Set Content and Guidance.md Examples:
    - Plan view with tank diameter, nozzle locations (with nozzle marks N1, N2, etc.), appurtenances
    - Elevation view with shell courses (with thickness callouts), roof slope, ladder/platform locations, foundation interface elevation
    - Sections showing internal details (bottom slope toward sump, agitator mounting reference), roof structure
    - Nozzle orientation diagram (polar plot)
4.3. Produce Foundation Drawings per Datasheet.md and Guidance.md Examples:
    - Foundation plan with anchor bolt layout (if anchored per Guidance.md TD-04), dimensions, sump/drain details
    - Foundation sections and details (reinforcement references, anchor bolt chairs if applicable)
    - Loading diagrams (dead load, seismic shear, wind overturning moment) for PKG-05 coordination
4.4. Produce Nozzle Schedules (3 schedules, one per tank) per Datasheet.md and Guidance.md Examples:
    - Nozzle table with columns: mark, size, rating, orientation, elevation, service, connection type
    - Nozzle detail drawings (reinforcement pad per API 650 Section 5.7, flange details)
4.5. Produce Roof Details per Datasheet.md and Guidance.md Examples:
    - Roof framing plan (rafters, girders, columns if applicable, compression ring)
    - Roof structure details (rafter connections, support details)
    - Access details (manway with davit, ladder to roof, vent nozzle details, access hatch)
4.6. Produce Agitator Drawings per Datasheet.md and Guidance.md Examples:
    - Agitator mounting details (nozzle reinforcement if side-entry, support bracket/flange)
    - Clearance diagram (agitator envelope, internal clearances to shell/bottom/other agitators)
    - Loading diagram (thrust, moment, torsion on tank shell for DEL-13.03 verification)
4.7. Add dimensions, notes, and annotations per CAD standards and API 650 requirements
4.8. Complete title block (drawing title, number, revision, date), revision block, and drawing metadata per Specification.md DR-02, DR-03 — **TBD** per project document control procedures

**Inputs:**
- Finalized design from Step 3 (all geometry, nozzle schedule, roof structure, foundation interface, agitator mounting)
- Project CAD standards — **TBD** per project CAD manual
- Drawing templates and title block — **TBD** per project standards

**Outputs:**
- Draft CAD drawings (all anticipated drawing types per _CONTEXT.md Anticipated Artifacts):
  - Tank GAs (3)
  - Foundation Drawings (TBD quantity)
  - Nozzle Schedules (3)
  - Roof Details (TBD quantity)
  - Agitator Drawings (TBD quantity)
- **Links to Datasheet:** All attributes documented in Datasheet.md are now shown on drawings

**Responsibility:** Design Engineer and/or CAD Technician

**Verification:** Self-check per Step 5 against design intent, calculation reference, CAD standards

**Source:** _CONTEXT.md (Anticipated Artifacts); Specification.md Drawing Standards DR-01, DR-02, DR-03; Guidance.md Examples section

---

### Step 5: Self-Check

**Activities per Specification.md V-01:**
5.1. Originator reviews drawings for completeness per Specification.md AC-01 (Acceptance Criteria: Completeness):
    - All required drawing types produced per _CONTEXT.md (Tank GAs, Foundation Drawings, Nozzle Schedules, Roof Details, Agitator Drawings)
    - All required views, sections, and details present per Guidance.md Examples
    - All dimensions provided and no missing annotations
5.2. Verify accuracy per Specification.md AC-02 (Acceptance Criteria: Accuracy):
    - Dimensions match design calculations (DEL-13.03) for shell thickness, tank height, diameter, nozzle elevations
    - Nozzle schedule matches P&IDs and process requirements
    - Foundation interface matches DEL-13.03 foundation loads and anchor bolt requirements
5.3. Verify CAD standards compliance per Specification.md AC-04 (Acceptance Criteria: Standards Compliance):
    - Layers, line weights, symbols, text per project CAD standards — **TBD** per project CAD manual
    - Drawing format, title block, revision block correct per project standards
5.4. Document self-check with checklist or review record — **TBD** per project quality procedures

**Inputs:**
- Draft drawings from Step 4
- DEL-13.03 (Design Calculations) for dimensional verification
- P&IDs for nozzle schedule verification
- Self-check checklist — **TBD** per project quality procedures
- Specification.md Acceptance Criteria AC-01, AC-02, AC-04

**Outputs:**
- Self-checked drawings with any corrections made
- Self-check record (checklist completed, issues corrected)

**Responsibility:** Originator (Design Engineer or CAD Technician)

**Verification:** Self-check record filed per project quality procedures

**Source:** Specification.md Verification section V-01 (Self-Check); ASSUMPTION based on typical engineering QA/QC

---

### Step 6: Interdisciplinary Check (IDC)

**Activities per Specification.md V-02:**
6.1. Distribute drawings to affected disciplines for IDC review per Specification.md IR-01 through IR-06:
    - Civil/Structural (PKG-05): Foundation interface, tank loading (dead, seismic, wind), anchor bolt layout, dyke/bunding coordination
    - Process/Piping (PKG-14): Nozzle schedule verification against P&IDs, piping interface coordination, nozzle orientations for piping routing
    - Electrical/I&C (PKG-20): Instrumentation nozzles (level, temperature, pressure), access for installation and maintenance
    - Fire Protection (PKG-23): Tank spacing for fire protection access, foam system interfaces if applicable
    - Coatings (PKG-26): Surface preparation requirements, coating system interfaces
6.2. Receive and log IDC comments in IDC comments log
6.3. Resolve comments by coordination (interface meetings) or drawing revision
6.4. Document IDC completion with sign-offs from all affected disciplines per Specification.md AC-03 (Acceptance Criteria: Coordination)

**Inputs:**
- Self-checked drawings from Step 5
- IDC distribution list — **TBD** per project quality procedures
- Specification.md Interface Requirements IR-01 through IR-06
- Guidance.md Interface coordination sections

**Outputs:**
- IDC comments log (comments received, originator responses, resolutions)
- Revised drawings incorporating IDC comment resolutions
- IDC sign-off record (sign-offs from PKG-05, PKG-14, PKG-20, PKG-23, PKG-26)

**Responsibility:** Design Engineer (coordinates IDC process); Discipline Leads from affected packages (provide IDC comments and sign-offs)

**Verification:** IDC sign-off record verifies Specification.md AC-03 (Coordination) is satisfied

**Source:** Specification.md Verification section V-02 (Interdisciplinary Check); Guidance.md Interface coordination sections

---

### Step 7: Independent Check

**Activities per Specification.md V-03:**
7.1. Assign independent checker (qualified P.Eng., independent of originator, API 650 experience) — **TBD** per project quality procedures
7.2. Checker reviews drawings for per Specification.md AC-02 and AC-04:
    - Design basis and criteria compliance (ER requirements, API 650, NBC 2020)
    - Calculation reference verification (verify design shown is supported by DEL-13.03 calculations)
    - Dimensional accuracy and interface coordination (foundation, nozzles, agitators)
    - Code compliance (API 650 shell thickness, nozzle reinforcement, roof design, seismic anchorage if required)
    - Completeness and clarity (all information necessary for fabrication and construction is provided)
7.3. Checker provides comments and recommendations in checker comments log
7.4. Originator resolves checker comments by drawing revision or technical justification
7.5. Checker signs off when satisfied (checker sign-off) per Specification.md AC-05 (Approval)

**Inputs:**
- IDC-resolved drawings from Step 6
- DEL-13.03: Design Calculations for calculation reference verification
- API 650, NBC 2020 standards for code compliance verification
- Checking checklist — **TBD** per project quality procedures
- Specification.md all requirements sections (FR, PR, IR, DR)

**Outputs:**
- Checker comments log (comments, originator responses, resolutions)
- Revised drawings incorporating checker comments
- Checker sign-off record

**Responsibility:** Independent Checker (qualified P.Eng.); Design Engineer (resolves checker comments)

**Verification:** Checker sign-off verifies Specification.md AC-02 (Accuracy) and AC-04 (Standards Compliance) are satisfied

**Source:** Specification.md Verification section V-03 (Independent Check); typical engineering QA/QC workflow

---

### Step 8: Design Review (if required)

**Activities per Specification.md V-04:**
8.1. Conduct formal design review meeting for major design decisions and interfaces
8.2. Participants: Mechanical Lead, Civil/Structural Lead, Process Lead, I&C Lead, Project Manager, QA/QC — **TBD** per project quality procedures
8.3. Review key design decisions per Guidance.md Trade-offs:
    - Tank sizing (diameter, height, D/H ratio per Guidance.md TD-01)
    - Roof type selection (cone, dome, floating per Guidance.md TD-02)
    - Foundation type selection (ring wall, mat, piles per Guidance.md TD-03)
    - Seismic anchorage decision (anchored vs. unanchored per Guidance.md TD-04)
    - Coating selection (internal food-grade coating per Guidance.md TD-05)
    - Phase 2 provisions (locations, sizes, protection per Specification.md FR-05)
8.4. Review interface coordination status (status of IDC comments from PKG-05, PKG-14, PKG-20, PKG-23, PKG-26)
8.5. Document design review minutes and action items
8.6. Close action items before proceeding to approval per Step 9

**Inputs:**
- Checked drawings from Step 7 (independent check completed)
- DEL-13.03 (Design Calculations) for design basis review
- Design review agenda — **TBD** per project quality procedures
- Specification.md all requirements sections
- Guidance.md Design Philosophy, Considerations, Trade-offs

**Outputs:**
- Design review minutes (decisions made, action items assigned)
- Action item log (action items, responsible parties, due dates, closure status)
- Revised drawings if required by design review action items

**Responsibility:** Discipline Lead (Mechanical Lead chairs review); Design Engineer (presents design and responds to review comments)

**Verification:** Design review minutes and closed action items verify major design decisions reviewed and approved

**Source:** Specification.md Verification section V-04 (Design Review); ASSUMPTION based on typical design review process for major facilities; Guidance.md Trade-offs section

---

### Step 9: Discipline Lead Approval

**Activities:**
9.1. Discipline Lead (Mechanical Lead, P.Eng.) reviews final drawings
9.2. Verify all checks completed and signed off per Specification.md AC-05 (Approval):
    - Self-check completed (Step 5)
    - IDC completed with all discipline sign-offs (Step 6)
    - Independent check completed with checker sign-off (Step 7)
    - Design review completed if required (Step 8)
9.3. Verify drawings ready for issue per project quality standards and Specification.md Acceptance Criteria AC-01 through AC-04
9.4. Approve drawings for issue: sign and stamp (P.Eng. stamp) per professional engineering requirements
9.5. Update drawing status in revision block (e.g., "Issued for Review" or "Issued for Construction") and date

**Inputs:**
- Fully checked and reviewed drawings from Steps 5–8
- Self-check record, IDC sign-off record, checker sign-off record, design review minutes (if applicable)
- Approval checklist — **TBD** per project quality procedures
- Specification.md AC-05 (Approval)

**Outputs:**
- Approved drawings ready for issuance (P.Eng. signed and stamped)
- Approval record (discipline lead approval documented in project records)

**Responsibility:** Discipline Lead (P.Eng., Mechanical Lead)

**Verification:** P.Eng. signature and stamp on drawings verifies approval

**Source:** ASSUMPTION based on typical engineering approval workflow and professional engineering requirements

---

### Step 10: Issuance for Review or Construction

**Activities per Specification.md DM-02 (Issuance):**
10.1. Prepare transmittal package:
    - Cover letter or transmittal form per project document control procedures — **TBD**
    - Drawing list with drawing numbers, titles, revisions, issue purpose
    - Purpose of issue identified (e.g., "Issued for Review", "Issued for Construction", "Issued for Information")
10.2. If issuing for **Review** (Client review, Authority Having Jurisdiction review, peer review):
    - File copies in deliverable folder `2_Checking/To/` with transmittal per Specification.md DM-02
    - Track review comments and responses in review comments log
    - Revise drawings based on review comments (return to Step 5 or appropriate verification step)
    - Re-issue when comments resolved (repeat Step 10)
10.3. If issuing for **Construction** (final approved issue for fabrication and construction):
    - File copies in deliverable folder `3_Issued/` with issue record per Specification.md DM-02
    - Update project document register with drawing numbers, titles, revisions, issue date
    - Distribute to construction team, tank fabricator, and relevant stakeholders per distribution list
10.4. Manage in project document management system per project document control procedures — **TBD** per Specification.md DM-01

**Inputs:**
- Approved drawings from Step 9
- Transmittal template — **TBD** per project document control procedures
- Distribution list — **TBD** per project procedures

**Outputs:**
- Issued drawing package (electronic and/or hardcopy per project requirements):
  - Tank General Arrangements (3)
  - Foundation Drawings
  - Nozzle Schedules (3)
  - Roof Details
  - Agitator Drawings
- Transmittal record (issue date, purpose, distribution list, recipient acknowledgments)
- Document register update (drawing numbers and issue status recorded)

**Responsibility:** Document Control; Design Engineer (prepares transmittal package)

**Verification:** Transmittal record and document register entry verify issuance completed

**Source:** Specification.md Documentation section DM-02 (Issuance); typical document control workflow

---

### Step 11: Revision Management (as required)

**Activities per Specification.md DM-03 (Revision Management):**
11.1. If revisions required after initial issue (design change, construction RFI, field modification):
    - Initiate revision per project change control procedures — **TBD**
    - Document reason for revision (change notice number, RFI number, description of change)
    - Mark revisions on drawings with revision clouds, revision triangles, and revision description in revision block
    - Update revision block with revision letter/number (A, B, C or R1, R2, R3), date, description
11.2. Repeat verification steps as appropriate based on revision significance — **TBD** per project quality procedures:
    - Minor revisions (dimensional corrections, note clarifications): Self-check (Step 5) and discipline lead approval (Step 9) may suffice
    - Major revisions (design changes affecting interfaces, structural changes, new nozzles): Full IDC (Step 6) and independent check (Step 7) may be required
11.3. Re-issue revised drawings per Step 10 (Issuance)
11.4. Archive superseded revisions per project retention policy per Specification.md DM-04 (Archive and Retention) — **TBD**

**Inputs:**
- Request for revision (design change notice, construction RFI, field query, etc.)
- Current issued drawings (latest revision from `3_Issued/` folder)
- Change control procedures — **TBD** per project procedures
- Specification.md DM-03 (Revision Management)

**Outputs:**
- Revised drawings (with revision clouds, triangles, updated revision block)
- Revision record and justification (change notice, RFI response, revision description)
- Re-issued drawings replacing previous revision

**Responsibility:** Design Engineer (prepares revision); Discipline Lead (approves revision)

**Verification:** Revision record documents reason for revision and approval; revised drawings filed per Specification.md DM-04

**Source:** Specification.md Documentation section DM-03 (Revision Management); typical engineering change control workflow

---

## Verification

### Verification Summary

The following verification activities are embedded in the procedure steps per Specification.md Verification section:

| Verification Activity | Step | Responsibility | Acceptance Criteria (Specification.md) |
|----------------------|------|----------------|----------------------------------------|
| **Self-Check** | Step 5 | Originator | AC-01 (Completeness), AC-02 (Accuracy), AC-04 (Standards Compliance) |
| **Interdisciplinary Check (IDC)** | Step 6 | Affected disciplines (PKG-05, PKG-14, PKG-20, PKG-23, PKG-26) | AC-03 (Coordination) — no unresolved interface conflicts |
| **Independent Check** | Step 7 | Independent checker (P.Eng.) | AC-02 (Accuracy), AC-04 (Standards Compliance) — design basis and code compliance verified |
| **Design Review** | Step 8 | Discipline leads, project team | Major design decisions reviewed and approved (tank sizing, roof type, foundation, seismic, Phase 2) |
| **Discipline Lead Approval** | Step 9 | Discipline Lead (P.Eng.) | AC-05 (Approval) — all checks complete, P.Eng. signed and stamped |

**Source:** Specification.md Verification section V-01 through V-05; typical engineering QA/QC workflow

### Acceptance Criteria (from Specification.md)

**AC-01: Completeness**
- All anticipated drawing types produced per _CONTEXT.md:
  - Tank General Arrangements (3)
  - Foundation Drawings (TBD quantity)
  - Nozzle Schedules (3)
  - Roof Details (TBD quantity)
  - Agitator Drawings (TBD quantity)
- All required views, sections, and details provided per Guidance.md Examples
- All dimensions, notes, and annotations complete (no TBD placeholders on issued drawings)

**AC-02: Accuracy**
- Dimensions and interface points verified against design calculations (DEL-13.03) per Step 5 and Step 7
- Design complies with API 650 (shell thickness per Section 5.6, nozzle reinforcement per Section 5.7, roof design per Section 5.10, seismic per Appendix E if applicable) and NBC 2020
- Nozzle schedule aligns with P&IDs and piping design (PKG-14) per Step 6 IDC
- Foundation interface aligns with structural design (PKG-05) per Step 6 IDC

**AC-03: Coordination**
- Interfaces with adjacent disciplines coordinated and verified per Specification.md IR-01 through IR-06:
  - PKG-05 (foundation) coordination verified in Step 6 IDC
  - PKG-14 (piping) coordination verified in Step 6 IDC
  - PKG-20 (instrumentation) coordination verified in Step 6 IDC
  - PKG-23 (fire protection) coordination verified in Step 6 IDC
  - PKG-26 (coatings) coordination verified in Step 6 IDC
- IDC comments resolved with no unresolved interface conflicts per Step 6

**AC-04: Standards Compliance**
- CAD standards compliance verified per Step 5 (self-check) and Specification.md DR-01
- Drawing format and numbering per project standards verified per Step 5 and Specification.md DR-02, DR-03
- Technical content complies with API 650 and referenced standards verified per Step 7 (independent check) and Specification.md PR-01

**AC-05: Approval**
- All required checks completed and signed off: self-check (Step 5), IDC (Step 6), independent check (Step 7), design review if required (Step 8)
- Discipline lead approval obtained (P.Eng. stamp) per Step 9
- **TBD** — Client review and approval requirements per ER (Volume 2 Part 2)

**Source:** Specification.md Section: Verification — Acceptance Criteria AC-01 through AC-05

---

## Records

### Documentation Outputs (Deliverable Artifacts)

The following documentation outputs are produced by this procedure per _CONTEXT.md Anticipated Artifacts:

| Output | Description | Quantity | Location |
|--------|-------------|----------|----------|
| **Tank General Arrangements** | Overall tank configuration, dimensions, nozzle locations, elevations, one GA per tank | 3 | `2_Checking/To/` (if issued for review) or `3_Issued/` (if issued for construction) per lifecycle state |
| **Foundation Drawings** | Foundation plan, sections, anchor bolt layout, loading diagrams | **TBD** | `2_Checking/To/` or `3_Issued/` per lifecycle state |
| **Nozzle Schedules** | Nozzle table with size, rating, orientation, elevation, service, connection type, one schedule per tank | 3 | `2_Checking/To/` or `3_Issued/` per lifecycle state |
| **Roof Details** | Roof framing, structure, access, venting details | **TBD** | `2_Checking/To/` or `3_Issued/` per lifecycle state |
| **Agitator Drawings** | Agitator mounting, support, clearances, loading | **TBD** | `2_Checking/To/` or `3_Issued/` per lifecycle state |

**Source:** _CONTEXT.md (Anticipated Artifacts); Datasheet.md Anticipated Drawing Set Content

### Process Records (Quality Records)

The following process records are produced to demonstrate compliance with quality procedures:

| Record | Description | Retention |
|--------|-------------|-----------|
| **Self-Check Record** | Originator self-check completed per Step 5, checklist or review log | **TBD** per project quality plan |
| **IDC Comments Log** | Interdisciplinary check comments and resolutions per Step 6 | **TBD** per project quality plan |
| **IDC Sign-off Record** | Sign-offs from PKG-05, PKG-14, PKG-20, PKG-23, PKG-26 per Step 6 | **TBD** per project quality plan |
| **Checker Comments Log** | Independent checker comments and resolutions per Step 7 | **TBD** per project quality plan |
| **Checker Sign-off** | Independent checker approval per Step 7 | **TBD** per project quality plan |
| **Design Review Minutes** | Design review meeting minutes and action items per Step 8 | **TBD** per project quality plan |
| **Approval Record** | Discipline lead approval and P.Eng. stamp per Step 9 | **TBD** per project quality plan (permanent record) |
| **Transmittal Record** | Issuance transmittal and distribution record per Step 10 | **TBD** per project quality plan |
| **Revision Record** | Revision history and justification per Step 11 | **TBD** per project quality plan |

**Source:** ASSUMPTION based on typical engineering project QA/QC records; project quality plan defines retention requirements

### Record Management

**Filing and Archive per Specification.md DM-04 (Archive and Retention):**
- Working files maintained in deliverable folder `1_Working/` during development (Steps 1-9)
- Review copies filed in `2_Checking/To/` when issued for review (Step 10.2)
- Approved copies filed in `3_Issued/` when issued for construction (Step 10.3)
- Superseded revisions archived per project retention policy — **TBD** (Step 11.4)

**Electronic Document Management per Specification.md DM-01 (Document Control):**
- Master copies maintained in project document management system — **TBD** per project document control procedures
- Access control and version control per project procedures — **TBD**

**Retention per Specification.md DM-04:**
- Final as-built drawings retained for facility lifecycle (permanent record)
- Interim revisions and working files retention per project procedures — **TBD**

**Source:** Specification.md Documentation section DM-01, DM-04; ASSUMPTION based on typical project document management and retention practices

---

## Cross-Document References

**For entity attributes and design data:** See `Datasheet.md`
- Step 1 (Design Initiation) → Review Datasheet.md Tank Configuration, Product, Capacity
- Step 2 (Preliminary Design) → Develop preliminary sizing for all Datasheet.md Tank Geometry and Foundation attributes
- Step 3 (Detailed Design) → Finalize design for all Datasheet.md attributes (Geometry, Foundation, Internals, Nozzles)
- Step 4 (CAD Drafting) → Produce drawings documenting all Datasheet.md attributes and Anticipated Drawing Set Content

**For requirements to be met:** See `Specification.md`
- Step 1 (Design Initiation) → Review Specification.md all requirements sections (FR, PR, IR, DR)
- Step 2 (Preliminary Design) → Apply Specification.md FR-01 (Capacity), PR-01 (API 650), PR-02 (Seismic)
- Step 3 (Detailed Design) → Develop design to meet all Specification.md requirements (FR-01 through FR-05, PR-01 through PR-07, IR-01 through IR-06)
- Steps 5-8 (Verification) → Verify compliance with Specification.md requirements and Acceptance Criteria AC-01 through AC-05
- Step 6 (IDC) → Verify Specification.md Interface Requirements IR-01 through IR-06 with affected disciplines
- Step 7 (Independent Check) → Verify Specification.md PR-01 (API 650 compliance), AC-02 (Accuracy), AC-04 (Standards Compliance)
- Step 9 (Approval) → Verify Specification.md AC-05 (Approval) criteria satisfied

**For design rationale and guidance:** See `Guidance.md`
- Step 1 (Design Initiation) → Apply Guidance.md Design Philosophy DP-01 through DP-05
- Step 2 (Preliminary Design) → Apply Guidance.md Tank Sizing and Configuration, Trade-offs TD-01, TD-02, TD-03, TD-04
- Step 3 (Detailed Design) → Apply Guidance.md API 650 Design Intent, all Considerations sections (Product, Sizing, Site-Specific, Agitator, Overflow/Water Draw-off, Phase 2, Interfaces), all Trade-offs TD-01 through TD-05
- Step 4 (CAD Drafting) → Reference Guidance.md Examples section for drawing content and layout
- Step 6 (IDC) → Implement Guidance.md Interface coordination sections (Foundation, Piping, Instrumentation, Fire Protection, Coatings)
- Step 8 (Design Review) → Review Guidance.md Design Philosophy, Considerations, and Trade-offs decision points

---

**Document Status:** Pass 3 Complete (2026-01-28) — Production workflow detailed with 11 steps from initiation through revision management. All verification activities aligned with Specification.md requirements and Acceptance Criteria. All steps linked to Datasheet.md attributes, Specification.md requirements, and Guidance.md rationale. TBDs specify information source needed. ASSUMPTIONs labeled with basis. Ready for WORKING_ITEMS refinement.

**Last Updated:** 2026-01-28
