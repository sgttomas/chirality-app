# Procedure: DEL-12.01 Metering Design Drawing Set

## Purpose

This procedure defines the process for producing and managing the **Metering Design Drawing Set** within **PKG-12 Product Transfer & Metering**.

### Deliverable Definition

DEL-12.01 defines the design arrangement and details for custody transfer metering per Employer's Requirements (Source: Decomposition:356).

| Attribute | Value |
|-----------|-------|
| Deliverable Type | Drawing |
| Discipline | Process |
| Responsible Party | D&B Contractor |
| Service Application | Custody transfer metering for CSD canola oil at rail unloading and marine loading |

### Procedure Scope

This procedure covers the complete lifecycle for producing the metering design drawing set:

1. **Production** — creating the drawing set from initial scope definition through detailed design
2. **Review and checking** — self-check, independent check (IC), and interdisciplinary check (IDC)
3. **Issue and revision management** — document control, approvals, and issuance

This procedure applies to all drawing types within the deliverable: metering skid GAs, flow meter installation details, and proving connection details.

## Prerequisites

### Dependencies

| Prerequisite | Status | Notes |
|--------------|--------|-------|
| Dependency Mode | NOT_TRACKED | Dependencies coordinated externally by humans (see `_DEPENDENCIES.md` and `execution/_Coordination/_COORDINATION.md`); interfaces with PKG-06, PKG-14, PKG-17, PKG-19, PKG-20 managed through coordination meetings and IDC process |

### Recommended Upstream Inputs

The following inputs should be obtained before commencing drawing production (ASSUMPTION based on typical drawing production workflow):

| Input | Source | Purpose | Timing |
|-------|--------|---------|--------|
| Metering Technical Specification | DEL-12.02 | Performance requirements, meter technology selection, proving method, accuracy requirements, operating conditions | Before Step 3 (Draft Drawings) |
| Metering Design Calculations | DEL-12.03 | Sizing basis (flow rates, pressure drops), straight-run lengths, meter selection verification | Before Step 3 (Draft Drawings) |
| Metering Data Sheet Package | DEL-12.04 | Specific instrument parameters (sizes, connections, dimensions), tag numbers, vendor data | During Step 3 (Draft Drawings); vendor data may be iterative |
| P&IDs | PKG-14 | Process context, line numbers, valve positions, instrument positions, interface points | Before Step 3 (Draft Drawings) |
| Vendor Data | Equipment suppliers | Manufacturer installation requirements, dimensional data, straight-run requirements, mounting details | During Step 3 (Draft Drawings); obtained after equipment selection |
| Layout Drawings | PKG-14 or site planning | Overall facility layout, available space for metering skids, elevation constraints | Before Step 3 (Draft Drawings) |
| Structural Support Design | PKG-06 | Skid support elevations, anchor bolt patterns, seismic requirements | During Step 3 (Draft Drawings); may be iterative with metering drawings |

### Reference Materials

| Reference | Location | Purpose |
|-----------|----------|---------|
| `_REFERENCES.md` | Deliverable folder | Applicable reference documents |
| `0_References/` | Package directory | Reference materials for PKG-12 |
| Employer's Requirements Vol 2 Part 1 | ER document set | General requirements, drawing standards, document control procedures, CAD standards, quality procedures | TBD |
| Employer's Requirements Vol 2 Part 2 | ER document set | Process mechanical requirements, metering technical requirements, operating conditions, fluid properties, hazardous area classification | TBD |
| Decomposition | Project root | PKG-12 scope (line 350), DEL-12.01 definition (line 356), objective mappings (lines 781, 789) |
| Specification.md | Deliverable folder | Requirements to be satisfied (REQ-01 through REQ-18) |
| Guidance.md | Deliverable folder | Design considerations, principles, trade-offs |
| Datasheet.md | Deliverable folder | Design context, anticipated drawing content, conditions |

### Personnel Requirements

| Role | Qualification | Responsibility | Source |
|------|---------------|----------------|--------|
| Originator | Qualified Process discipline engineer with custody transfer metering experience | Technical content, drawing production, self-check completion | ASSUMPTION; project quality procedures |
| Checker | Independent Process discipline engineer (not the originator) | Independent check for technical correctness, constructability, maintainability | ASSUMPTION; project quality procedures |
| IDC Participants | Representatives from interfacing disciplines: Piping (PKG-14), Structural (PKG-06), Electrical (PKG-17), Instrumentation (PKG-20), Controls (PKG-19) | Interface review and coordination | ASSUMPTION |
| Approver | Authorized per project procedures (typically Process Lead or Engineering Manager) | Authorization for issue | TBD; ER Vol 2 Part 1 |

### Tools and Systems

| Tool/System | Purpose | Source |
|-------------|---------|--------|
| CAD Software | Drawing production per project CAD standards | TBD; ER Vol 2 Part 1 |
| Document Management System | Drawing storage, revision control, distribution | TBD; ER Vol 2 Part 1 |
| Calculation Software | Verify straight-run calculations if needed | DEL-12.03 |

## Steps

### Step 1: Confirm Scope and Drawing List

**Objective:** Establish the scope of the drawing set and create a drawing list identifying all sheets to be produced.

| Action | Description | Output |
|--------|-------------|--------|
| 1.1 | Review PKG-12 scope definition (Decomposition line 350): "Custody transfer flow meters (rail unloading and marine loading), metering instrumentation" | Scope understanding |
| 1.2 | Review DEL-12.01 definition (Decomposition line 356): "Defines the design arrangement and details for metering per ER requirements" | Deliverable understanding |
| 1.3 | Confirm minimum artifact set per Specification.md REQ-02: (a) Metering skid GAs, (b) Flow meter installation details, (c) Proving connection details | Artifact checklist |
| 1.4 | Determine number of sheets required: consider separate sheets for rail unloading vs. marine loading services, plan vs. elevation views, different detail scales | Sheet count estimate |
| 1.5 | Prepare preliminary drawing list / sheet index with: drawing numbers (TBD per project numbering system), drawing titles, sheet descriptions, anticipated scales | Preliminary drawing list |
| 1.6 | Obtain drawing number assignments per project document control procedures (TBD; ER Vol 2 Part 1) | Assigned drawing numbers |
| 1.7 | Finalize drawing list and obtain approval from Process Lead or Engineering Manager | Approved drawing list |

**Output:** Approved drawing list with assigned drawing numbers, titles, and sheet descriptions

**Verification:** Drawing list includes all decomposition-listed artifacts (Specification.md REQ-02)

---

### Step 2: Collect Inputs

**Objective:** Gather all necessary input information and reference materials before commencing drawing production.

| Action | Description | Verification |
|--------|-------------|--------------|
| 2.1 | Obtain latest metering specification (DEL-12.02) — review for: performance requirements (accuracy, repeatability, flow range), meter technology selection (Coriolis, ultrasonic, turbine, etc.), proving method (in-line prover, portable prover, master meter), operating conditions (pressure, temperature, flow rates) | Check document revision and approval status |
| 2.2 | Obtain metering design calculations (DEL-12.03) — extract: meter sizing basis (rail unloading flow rates, marine loading flow rates), straight-run requirements (upstream and downstream lengths per meter technology), pressure drop calculations, proving requirements | Verify calculations are complete and checked |
| 2.3 | Obtain metering data sheets (DEL-12.04) — extract: specific instrument parameters (flow meter size, connection size and type, transmitter types and ranges, tag numbers), dimensional data (meter length, weight, connection orientations), power requirements (for electrical interface) | Verify data sheets match specification and calculations |
| 2.4 | Obtain relevant P&IDs (PKG-14) — identify: process context (upstream and downstream of metering points), line numbers and sizes, valve positions (isolation, control, bypass), instrument positions, interface points with metering skids | Verify P&IDs are current revision |
| 2.5 | Obtain vendor data if available — review: manufacturer installation requirements (straight-run requirements, orientation constraints, mounting recommendations), dimensional drawings (meter outline, connection locations), installation manuals (torque requirements, gasket specifications, alignment tolerances) | Verify vendor data matches selected equipment per DEL-12.04 |
| 2.6 | Obtain project drafting standards (TBD; ER Vol 2 Part 1) — review: CAD standards (layers, line weights, text styles, dimensioning), title block format, revision control procedures, sheet size and scale conventions | Confirm latest revision of drafting standards |
| 2.7 | Obtain layout drawings and elevation constraints — identify: available space for metering skids at rail unloading and marine loading locations, elevation constraints (pipe rack elevations, access platform elevations), interface locations (piping tie-ins, electrical connections, structural supports) | Coordinate with PKG-14 and site planning |
| 2.8 | Review Guidance.md — note: design principles, considerations (meter technology, straight-run, proving method, environmental conditions), trade-offs (accuracy vs. pressure drop, accessibility vs. footprint, in-line vs. portable proving) | Understand design intent and factors |

**Output:** Complete input package sufficient for drawing production; input register documenting all collected inputs with revision/date information

**Verification:** All prerequisite inputs obtained and current; any missing inputs identified and flagged for resolution

---

### Step 3: Draft Drawings

**Objective:** Produce draft drawings showing metering arrangements and details per requirements.

#### 3.1: Produce Metering Skid GA(s)

| Action | Description |
|--------|-------------|
| 3.1.1 | Create plan view(s) showing: meter run centerline and orientation, upstream and downstream piping with straight-run dimensions, isolation valves (upstream, downstream, bypass), proving connections, instruments (flow meter, temperature transmitters, pressure transmitters, density transmitters if applicable) with tag numbers per DEL-12.04, structural supports and skid framing, overall skid dimensions (length, width), interface points (piping tie-ins to PKG-14, electrical connections, structural support points) |
| 3.1.2 | Create elevation view(s) showing: meter elevation and mounting, piping elevations, structural supports and skid framing, access provisions (platforms, stairs, walkways if required), height clearances (for installation, operation, maintenance), vertical dimensions |
| 3.1.3 | Add general notes: flow direction arrows, straight-run requirements (e.g., "Minimum 10D upstream, 5D downstream per vendor requirements"), proving frequency (if specified in DEL-12.02), installation notes (alignment tolerances, torque requirements), interface notes (piping tie-in sizes and elevations, electrical power requirements) |
| 3.1.4 | Apply tag numbers consistent with: P&IDs (PKG-14), metering specification (DEL-12.02), data sheets (DEL-12.04) — verify tag number consistency per Specification.md REQ-04 |
| 3.1.5 | Dimension all critical geometry: overall skid dimensions, meter positions along skid, straight-run lengths (upstream and downstream), interface point locations (piping tie-ins, electrical connections, structural anchor points), clearances (for access, removal, proving equipment connection) |
| 3.1.6 | Prepare separate GAs for rail unloading and marine loading if arrangements differ significantly; otherwise show both services on same drawing set with clear identification |

#### 3.2: Produce Flow Meter Installation Details

| Action | Description |
|--------|-------------|
| 3.2.1 | Create detail view(s) showing: meter orientation (horizontal, vertical, or inclined per manufacturer requirements and DEL-12.02), meter mounting arrangement (flange connections, support locations, alignment provisions), upstream straight-run dimension with tolerance (e.g., "10D ± 0.5D"), downstream straight-run dimension with tolerance (e.g., "5D ± 0.5D"), flow conditioning devices if any (straightening vanes, perforated plates) with positions dimensioned from meter inlet |
| 3.2.2 | Show instrument tap locations: temperature transmitter tap (position along meter run, distance from meter per manufacturer requirements), pressure transmitter taps (upstream and downstream positions if differential pressure is measured), density transmitter tap if applicable (position and installation details) — dimension all tap positions from meter centerline or flange face |
| 3.2.3 | Detail mounting provisions: flange details (size, rating, facing per DEL-12.02), support locations and types (pipe supports, skid mounting), alignment requirements (levelness tolerance, pipe alignment tolerance per manufacturer), anchor points (if meter requires specific anchoring) |
| 3.2.4 | Add installation notes: torque requirements for flange bolts, gasket type and material, alignment tolerances (e.g., "Meter shall be level within ±0.5°"), installation sequence, cleanliness requirements (if applicable for custody transfer service) |
| 3.2.5 | Show clearances for: meter removal (bolt circle clearance for flange separation), transmitter access (for calibration and maintenance), proving equipment connection (if portable prover connections are on meter body) |

#### 3.3: Produce Proving Connection Details

| Action | Description |
|--------|-------------|
| 3.3.1 | Detail proving connection arrangement per proving method specified in DEL-12.02: (a) If in-line prover: show prover loop piping, isolation valves, sphere launcher/receiver if applicable, drain points, connection to meter run; (b) If portable prover: show prover connection points, isolation valves, quick-disconnect fittings (if used), drain points, access for portable prover equipment; (c) If master meter: show master meter installation, parallel piping arrangement, isolation and diverter valves |
| 3.3.2 | Show isolation valve arrangement: valves to isolate proving loop from process, valve sizes and types per DEL-12.02, valve positions (open/closed) during normal operation vs. proving operation, valve tag numbers per P&IDs |
| 3.3.3 | Detail drainage provisions: drain points for proving loop, drain valve sizes and connections, drain routing (to drain system or containment), notes on proving loop drainage procedure |
| 3.3.4 | Show access provisions: access for portable prover connection (if applicable), clearance for proving equipment operation, access platforms or walkways if required for proving activities, lifting provisions if proving equipment is heavy |
| 3.3.5 | Add proving notes: proving frequency (if specified in DEL-12.02, e.g., "Prove meter quarterly or after maintenance"), proving procedure reference (if procedure is defined separately), proving connection size and type, prover type and model (if specified) |

#### 3.4: Apply Standard Drawing Elements

| Action | Description |
|--------|-------------|
| 3.4.1 | Apply project title block per project standards (TBD; ER Vol 2 Part 1): project name and number, drawing title, drawing number, revision (00 for initial), date, originator name and signature block, checker signature block, approver signature block |
| 3.4.2 | Add drawing border, sheet size per project standards (typically A1 or A0 for GAs, A3 or A2 for details) |
| 3.4.3 | Apply CAD standards: correct layers for different element types, line weights per project standards, text heights per project standards, dimensioning style per project standards |
| 3.4.4 | Add legend if needed: symbol legend (valves, instruments, equipment), abbreviation list, notes section |
| 3.4.5 | Add reference notes: reference to metering specification (DEL-12.02 document number), reference to P&IDs (document numbers), reference to vendor data (if specific vendor installation drawings are referenced) |

**Output:** Draft drawing set ready for self-check; drawings include metering skid GAs, flow meter installation details, proving connection details

**Verification:** All decomposition-listed artifacts present (Specification.md REQ-02); tag numbers consistent with DEL-12.04 and P&IDs; dimensions consistent with DEL-12.03 calculations

---

### Step 4: Self-Check

**Objective:** Originator reviews own work for completeness, accuracy, and compliance with requirements before submitting for independent check.

| Action | Description | Checklist Item |
|--------|-------------|----------------|
| 4.1 | Verify all decomposition-listed artifacts are present: (a) Metering skid GAs — rail unloading and marine loading, (b) Flow meter installation details, (c) Proving connection details | ✓ REQ-02 per Specification.md |
| 4.2 | Verify drawing content aligns with Specification.md requirements: REQ-01 (depicts custody transfer at rail unloading and marine loading), REQ-03 (sufficient detail for construction and commissioning), REQ-05 (supports 1,000,000 MT/a throughput per OBJ-2), REQ-06 (supports custody transfer accuracy per OBJ-10), REQ-16/17/18 (content requirements for GAs, installation details, proving details) | ✓ Requirements verification |
| 4.3 | Verify consistency with related deliverables: tag numbers match DEL-12.04 data sheets and P&IDs (REQ-04), straight-run dimensions match DEL-12.03 calculations (REQ-07), meter technology and proving method match DEL-12.02 specification | ✓ Cross-document consistency |
| 4.4 | Verify interface points are identified per REQ-09: piping tie-ins to PKG-14 (sizes, elevations, orientations), instrument connections to PKG-20 (tag numbers, signal types), electrical power to PKG-17 (power requirements, connection points), control/communications to PKG-19 (signal routing), structural supports to PKG-06 (anchor points, loads), access/maintenance provisions, proving connections | ✓ Interface coverage |
| 4.5 | Check CAD standards and document control compliance (REQ-08, REQ-13, REQ-15): drawing numbering per project system, CAD layering and line weights per standards, title block complete with project information, revision control (revision 00 for initial issue), originator information in title block | ✓ Document control compliance |
| 4.6 | Check dimensions and tolerances: all critical dimensions shown (straight runs, overall dimensions, interface points, clearances), tolerances specified where critical (meter alignment, straight-run lengths), dimension consistency (no conflicting dimensions), units clearly indicated | ✓ Dimensional accuracy |
| 4.7 | Check notes and callouts: all equipment tagged with numbers matching DEL-12.04 and P&IDs, material callouts reference DEL-12.02 specification, installation notes are clear and complete, interface notes identify coordination with other packages | ✓ Notes completeness |
| 4.8 | Review against Guidance.md principles: custody transfer measurement intent is clear (meter geometry, straight runs, instrument taps, proving connections unambiguous), constructability (access for installation, lifting, welding), maintainability (access for proving, calibration, inspection, component replacement), measurement precision (all geometry critical to accuracy is dimensioned) | ✓ Design principles |
| 4.9 | Record self-check completion: date, items checked, comments or issues identified, resolution of issues | Self-check record |

**Output:** Self-checked drawings; self-check record documenting completion and any issues resolved

**Verification:** Self-check record complete; all checklist items verified; any issues identified during self-check are resolved before proceeding to IC

---

### Step 5: Independent Check (IC)

**Objective:** Independent Process discipline engineer reviews drawings for technical correctness, constructability, and maintainability.

| Action | Description | Verification |
|--------|-------------|--------------|
| 5.1 | Independent checker reviews drawings for technical correctness: meter technology selection appropriate for service (per DEL-12.02), meter sizing adequate for flow rates (per DEL-12.03), straight-run lengths comply with manufacturer requirements, instrument tap positions comply with manufacturer recommendations, proving arrangement suitable for specified proving method | Technical correctness |
| 5.2 | Verify custody-transfer measurement intent is clear per Guidance.md principles: meter run geometry unambiguous (orientation, alignment, straight runs clearly dimensioned), instrument tap locations explicit (temperature, pressure, density if applicable), proving connections accessible and clearly detailed, installation precision requirements specified (alignment tolerances, levelness) | Measurement intent clarity |
| 5.3 | Verify constructability: access for installation (clearance for flange assembly, bolt access), lifting provisions adequate (lifting points shown, rigging clearances), alignment provisions shown (support locations, adjustment provisions), welding access if field welds are required (adequate clearance for welding equipment) | Constructability |
| 5.4 | Verify maintainability: access for proving (portable prover connection access, in-line prover operation access), access for calibration and inspection (transmitter access, meter access for internal inspection), component removal clearances (meter removal, transmitter removal, valve removal), maintenance notes provided (proving frequency, calibration requirements) | Maintainability |
| 5.5 | Verify compliance with objectives: OBJ-2 (throughput capacity): meter arrangements do not constrain flow, pressure drop acceptable per DEL-12.03; OBJ-10 (custody transfer accuracy): design supports accurate measurement, straight runs adequate, proving accessible | Objective compliance |
| 5.6 | Check for errors or omissions: missing dimensions, missing tag numbers, inconsistent callouts, conflicts between plan and elevation views, missing notes or specifications | Error check |
| 5.7 | Document check comments: prepare IC comment list with: comment number, drawing sheet number, comment description, severity (critical / major / minor), recommended action | IC comment list |
| 5.8 | Coordinate with originator to resolve comments: review comments with originator, agree on resolutions, verify originator implements agreed resolutions | Comment resolution |
| 5.9 | Record IC completion: date, checker name, summary of review, confirmation that all comments are resolved | IC record |

**Output:** IC-reviewed drawings with all comments resolved; IC record

**Verification:** IC record complete; IC comment list shows all comments resolved; checker signature on drawings confirming IC completion

---

### Step 6: Interdisciplinary Check (IDC)

**Objective:** Coordinate with interfacing disciplines to verify interface compatibility and resolve interface issues.

| Action | Description | Participants |
|--------|-------------|--------------|
| 6.1 | Distribute drawings to interfacing discipline leads: Piping (PKG-14), Structural (PKG-06), Electrical (PKG-17), Instrumentation (PKG-20), Controls (PKG-19) — provide sufficient review time (typically 5-10 working days; TBD per project procedures) | IDC distribution |
| 6.2 | Hold IDC meeting to review interfaces: review piping tie-ins with PKG-14 (sizes, elevations, orientations match piping layout), review structural supports with PKG-06 (skid support elevations, anchor bolt patterns, loads, seismic requirements), review electrical interfaces with PKG-17 (power supply routing, hazardous area requirements), review instrumentation interfaces with PKG-20 (transmitter specifications, junction box locations, cable routing), review control interfaces with PKG-19 (signal types, I/O assignments, HMI requirements) | IDC meeting with all disciplines |
| 6.3 | Document IDC comments: prepare IDC comment list with: comment number, commenting discipline, drawing sheet number, comment description, interface affected, recommended action | IDC comment list |
| 6.4 | Resolve interface comments: coordinate with commenting disciplines to agree on resolutions, update drawings as needed to resolve interface issues, verify changes do not create new conflicts | Comment resolution with coordination |
| 6.5 | Confirm interface coordination is complete: obtain confirmation from each discipline that their interface comments are resolved, verify no outstanding interface issues | Interface sign-off |
| 6.6 | Record IDC completion: date, participants (discipline leads who participated), summary of interface review, confirmation that all interface comments are resolved | IDC record |

**Output:** IDC-reviewed drawings with all interface comments resolved; IDC record with interface sign-offs from participating disciplines

**Verification:** IDC record complete; all participating disciplines confirm interfaces are acceptable; IDC comment list shows all comments resolved

---

### Step 7: Issue for Review or Construction

**Objective:** Finalize drawings, obtain required approvals, and issue per project document control procedures.

| Action | Description | Output |
|--------|-------------|--------|
| 7.1 | Apply final document control metadata: update title block with final revision number (00 for initial issue, or A, B, C for subsequent revisions), add date of issue, add originator signature (confirming self-check completion), add checker signature (confirming IC completion), add approver signature (authorizing issue per project procedures; TBD ER Vol 2 Part 1) | Title block completion |
| 7.2 | Obtain required approvals per project procedures: Process Lead approval (technical content), Engineering Manager approval (if required by project procedures), Quality Manager approval (if required for custody transfer drawings) — approval authorities TBD from ER Vol 2 Part 1 | Approval signatures |
| 7.3 | Prepare issue package: assemble complete drawing set (all sheets), include drawing list / sheet index, include check records (self-check, IC, IDC records), prepare transmittal letter or form per project procedures | Issue package |
| 7.4 | Issue per project document control process: submit to document management system (TBD), assign issue status (e.g., "Issued for Review", "Issued for Construction", "Issued for Record"), distribute to required recipients per distribution list (TBD) | Document management system entry |
| 7.5 | Place review package in deliverable folder structure: place issued copy in `2_Checking/To/` for review issues, or place issued copy in `3_Issued/` for final/construction issues — per project convention and lifecycle state | Filed issue package |
| 7.6 | Update deliverable status: if issuing for review, update `_STATUS.md` to CHECKING; if issuing for construction, update `_STATUS.md` to ISSUED — record issue date, revision, and issue purpose in status history | Status update |

**Output:** Issued drawing set with all approvals; issue record in document management system; deliverable status updated

**Verification:** All approval signatures obtained; issue record complete in document management system; drawings filed per project conventions; `_STATUS.md` updated

---

## Verification

### Verification Activities

| Activity | Requirement Verified | Method | Record |
|----------|---------------------|--------|--------|
| Artifact completeness check | REQ-02 | Checklist against Decomposition:356 — verify metering skid GAs, flow meter installation details, proving connection details are present | Drawing list; self-check record Step 4.1 |
| Technical review | REQ-01, REQ-03, REQ-05, REQ-06, REQ-07, REQ-16, REQ-17, REQ-18 | Discipline review for technical correctness, custody transfer intent, dimensional accuracy | Self-check record Step 4.2; IC record Step 5.1, 5.2 |
| Cross-document consistency check | REQ-04, REQ-07 | Verify tag numbers match DEL-12.04 and P&IDs; verify dimensions match DEL-12.03 calculations; verify meter technology and proving method match DEL-12.02 | Self-check record Step 4.3 |
| Interface review | REQ-09, REQ-10 | IDC with interfacing disciplines (PKG-06, PKG-14, PKG-17, PKG-19, PKG-20) | IDC record Step 6; IDC comment list and resolution |
| Document control check | REQ-08, REQ-13, REQ-15 | Verify drawing numbering, CAD standards, title block, revision control per project procedures | Self-check record Step 4.5; document control review at issue Step 7.1 |
| Check completion review | REQ-12 | Verify self-check, IC, and IDC records are complete and all comments resolved | Check records; issue package Step 7.3 |
| Constructability review | REQ-03 | Verify sufficient detail for construction, access for installation, lifting provisions | IC record Step 5.3 |
| Maintainability review | REQ-03 | Verify access for proving, calibration, inspection, component replacement | IC record Step 5.4 |

### Acceptance Criteria

| Criterion | Verification Method | Source |
|-----------|---------------------|--------|
| All three artifact types present covering both services | Drawing list review; Step 4.1 checklist | Specification.md REQ-02; Decomposition:356 |
| Technical accuracy | IC record confirms technical correctness | Specification.md REQ-01, REQ-05, REQ-06, REQ-07; IC record Step 5.1, 5.2 |
| Cross-document consistency | Self-check confirms tag numbers, dimensions, specifications match related deliverables | Specification.md REQ-04, REQ-07; self-check Step 4.3 |
| Interface coverage and coordination | IDC record confirms all interfaces identified and coordinated | Specification.md REQ-09, REQ-10; IDC record Step 6 |
| Document control compliance | Document control check confirms numbering, title blocks, revisions comply with project procedures | Specification.md REQ-08, REQ-13, REQ-15; self-check Step 4.5; issue Step 7.1 |
| Check records complete | Issue package includes complete self-check, IC, IDC records with all comments resolved | Specification.md REQ-12; issue Step 7.3 |
| Custody transfer intent clear | IC confirms measurement intent is unambiguous per Guidance.md principles | Specification.md REQ-06; Guidance.md principles; IC record Step 5.2 |
| Constructability and maintainability | IC confirms adequate access and clearances for installation, operation, maintenance | Specification.md REQ-03; IC record Step 5.3, 5.4 |

### Sign-off Requirements

| Role | Responsibility | Verification | Source |
|------|----------------|--------------|--------|
| Originator | Technical content accuracy, self-check completion | Originator signature in title block | ASSUMPTION; project quality procedures |
| Checker | IC completion, technical verification, check record | Checker signature in title block | ASSUMPTION; project quality procedures |
| Approver | Authorization for issue, compliance with project requirements | Approver signature in title block | TBD; ER Vol 2 Part 1 |
| IDC Participants | Interface coordination, interface acceptance | IDC record with discipline sign-offs | ASSUMPTION; IDC procedure |

## Records

### Documentation Outputs

| Output | Description | Source |
|--------|-------------|--------|
| Metering Skid GAs | General arrangement drawing(s) for rail unloading and marine loading metering skids showing plan and elevation views with dimensions, tag numbers, and interface points | Decomposition:356; Specification.md REQ-16; Step 3.1 |
| Flow Meter Installation Details | Installation detail drawing(s) for custody transfer flow meters showing orientation, straight-run dimensions, instrument taps, and mounting details | Decomposition:356; Specification.md REQ-17; Step 3.2 |
| Proving Connection Details | Proving connection detail drawing(s) showing prover connections, isolation, drainage, and access | Decomposition:356; Specification.md REQ-18; Step 3.3 |
| Drawing List / Sheet Index | Index of all drawing sheets with drawing numbers, titles, revisions, and descriptions | Specification.md Documentation section; Step 1.5 |
| Self-Check Record | Record of originator self-check with date, items checked, comments, and resolutions | Step 4.9 |
| IC Record | Record of independent check with date, checker name, comments, and resolutions | Step 5.9 |
| IDC Record | Record of interdisciplinary check with date, participants, interface comments, and resolutions | Step 6.6 |
| Issue Record | Record of drawing issue with date, revision, approvals, distribution | Step 7.4 |

### Record Management

| Attribute | Value | Source |
|-----------|-------|--------|
| Filing Location (Working) | `1_Working/DEL-12.01_Metering_Design_Drawing_Set/` | Current location |
| Filing Location (Review) | `2_Checking/To/` (for review issues); `2_Checking/From/` (for returned review comments) | Project convention |
| Filing Location (Issued) | `3_Issued/` (for final/construction issues) | Project convention |
| Document Management System | Per project document control procedures (TBD; ER Vol 2 Part 1) | TBD |
| Retention Period | Per project quality procedures; typically life of facility for custody transfer drawings | TBD |
| Format | Electronic files in CAD format (DWG, DGN, or per project standard); PDF for distribution | ASSUMPTION |
| Backup and Version Control | Per project IT procedures; CAD files under version control in document management system | TBD |

### Status Transitions

Status transitions are managed per `_STATUS.md` in the deliverable folder:

| From State | To State | Trigger | Responsible |
|------------|----------|---------|-------------|
| INITIALIZED | IN_PROGRESS | Drawing production commences (Step 3) | Process Engineer (originator) |
| IN_PROGRESS | CHECKING | Drawing set submitted for review (Step 7 for review issue) | Process Engineer (originator) |
| CHECKING | IN_PROGRESS | Review comments received requiring revision | Process Engineer (originator) |
| CHECKING | ISSUED | Approved for construction (Step 7 for construction issue) | Approver |

**Note:** Status state transitions are recorded in `_STATUS.md` with date, state change, and brief description. Detailed issue history is maintained in the document management system.

### Revision Management

| Revision | Purpose | Typical Trigger | Approval Required |
|----------|---------|-----------------|-------------------|
| 00 | Initial issue for review | First issue to client or for internal review | Process Lead |
| A, B, C... | Subsequent issues incorporating review comments | Review comments received and incorporated | Process Lead |
| 01, 02, 03... | Issued for construction | Approved for construction; all review comments resolved | Engineering Manager |
| As-built revisions | Incorporate field changes | Construction complete; as-built markups received | As-built process per project procedures (TBD) |

**Note:** Revision numbering convention TBD from ER Vol 2 Part 1 project document control procedures.
