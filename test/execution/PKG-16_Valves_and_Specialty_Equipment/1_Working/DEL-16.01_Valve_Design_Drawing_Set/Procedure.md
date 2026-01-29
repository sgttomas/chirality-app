# Procedure: DEL-16.01 Valve Design Drawing Set

## Purpose

This procedure defines the process for producing and managing **Valve Design Drawing Set** within **PKG-16 Valves & Specialty Equipment**.

**Deliverable Purpose:** Defines the design arrangement and details for valves per ER requirements for the Canola Oil Transload Facility.

**Source:** `_CONTEXT.md`

**Deliverable Type:** Drawing
**Responsible Party:** D&B Contractor
**Discipline:** Mechanical

**Scope:** This procedure covers the production of valve arrangement drawings and actuator detail drawings from initial design concept through IFC (Issued for Construction) issue.

## Prerequisites

### Dependencies

**Dependency Tracking Mode:** NOT_TRACKED
- Dependencies are coordinated externally by humans (see `execution/_Coordination/_COORDINATION.md`)
- Upstream deliverables and input data to be confirmed prior to commencement

**Source:** `_DEPENDENCIES.md`

**Typical Upstream Inputs (advisory only — not formally tracked):**
- Process design (P&IDs, line list) — defines valve service, size, type
- Valve sizing calculations (DEL-16.03) — provides valve size, pressure class, Cv/Kv
- Piping design (DEL-14.01) — provides piping layout and valve interface points
- Instrumentation design (DEL-20.01) — defines control valve instrumentation requirements
- Structural design (DEL-06.01) — provides support structure for large valves
- HAZOP study (DEL-27.02) — defines safety-critical valve fail-safe modes

**Source:** Inputs inferred from multi-discipline nature of valve design; specific coordination TBD

### Reference Materials

**Required References:**
- See `_REFERENCES.md` for applicable reference documents
- See `0_References/` in package directory for reference materials

**Key References (to be obtained):**
- Employer's Requirements (Volume 2 Parts 1–3) — **TBD**
- Project CAD Standards Manual — **TBD**
- Project Drawing Numbering System — **TBD**
- Project Engineering Standards — **TBD**
- Applicable codes and standards (see Specification.md, Section "Standards")

**Source:** Reference requirements inferred from deliverable type; `_REFERENCES.md` indicates no references identified yet

**Vendor Data (as available):**
- Valve vendor outline drawings (post-procurement)
- Actuator vendor certified drawings (post-procurement)

### Personnel Requirements

**Qualifications:**
- **Design Engineer:** Mechanical engineer with experience in valve selection and arrangement for process facilities
- **CAD Designer:** Proficient in project CAD software (AutoCAD, MicroStation, or as specified)
- **Checker:** Senior mechanical engineer (not the originator), qualified to review valve designs
- **Discipline Lead:** Professional Engineer (P.Eng.) authorized to approve mechanical drawings

**Source:** Typical personnel requirements for mechanical drawing production; specific qualifications TBD per project quality procedures

**Competency Requirements:**
- Familiarity with applicable valve standards (API 600, API 526, ISA-75)
- Understanding of valve actuator types and sizing
- Knowledge of process piping and piping stress considerations
- **ASSUMPTION:** Personnel competency per project quality procedures

## Steps

### Step 1: Design Inputs Review

**Action:** Review and confirm design inputs are sufficient to commence valve arrangement design.

**Inputs to Review:**
- P&IDs (valve service, tag numbers, fail-safe modes)
- Line list (valve line size, pressure class, service)
- Valve sizing calculations (DEL-16.03) — valve type, size, Cv/Kv
- Piping layout drawings (DEL-14.01) — valve interface locations
- Control valve requirements (DEL-20.01, DEL-19.01) — instrumentation and control interfaces
- HAZOP recommendations (DEL-27.02) — safety-critical valve requirements

**Verification:**
- Confirm all valves shown on P&IDs have corresponding sizing calculations
- Confirm valve types and sizes are consistent with piping design
- Identify any missing inputs and issue RFI (Request for Information) to responsible discipline

**Source:** Typical design input review process for valve arrangement drawings

### Step 2: Valve Arrangement Layout

**Action:** Develop valve arrangement drawings showing valve locations, orientations, and interfaces.

**Drawing Content:**
- **Valve Location:** Show valve position on plan and elevation views; reference to grid lines or equipment
- **Valve Orientation:** Show valve stem orientation (vertical, horizontal); critical for operator access and actuator mounting
- **Tag Identification:** Label each valve with tag number per P&ID
- **Piping Interface:** Show piping connection size, flanged rating, and centerline elevation
- **Actuator Indication:** Show actuator type (pneumatic, electric, manual) and orientation
- **Access Requirements:** Show platforms, ladders, or access provisions for valve operation and maintenance
- **Support Requirements:** Indicate structural support points for large or heavy valves

**CAD Standards:**
- Use project CAD software and standards — **TBD**
- Apply correct layers, line weights, and symbol libraries per project CAD manual — **TBD**
- Maintain drawing scale appropriate to level of detail (typically 1:50 or 1:100 for arrangement)

**Coordination:**
- Coordinate valve locations with piping designer to ensure piping flexibility and stress compliance
- Coordinate valve access with structural/architectural designer (platforms, stairs)
- Coordinate actuator clearances with adjacent equipment and cable trays

**Source:** Typical valve arrangement drawing content; CAD standards TBD pending project CAD manual

### Step 3: Actuator Detail Development

**Action:** Develop actuator detail drawings showing typical mounting arrangements for pneumatic, electric, and manual actuators.

**Detail Drawing Content:**
- **Actuator Type:** Pneumatic cylinder, electric motor operator, manual handwheel/gearbox
- **Mounting Arrangement:** Bracket, yoke, or direct-mount configuration
- **Interface Dimensions:** Valve-to-actuator interface dimensions (ISO 5211 for quarter-turn, MSS-SP-91 for linear)
- **Torque/Thrust Basis:** Reference to valve sizing calculation (DEL-16.03) for actuator sizing basis
- **Control Interfaces:** For automated valves, show solenoid valves, positioners, limit switches, terminal boxes
- **Manual Override:** For automated valves, show manual override handwheel or declutching mechanism
- **Failure Mode Indication:** Label fail-safe mode (FC = Fail Closed, FO = Fail Open, FL = Fail Last)

**Typical Details Required:**
- Pneumatic actuator on ball valve (quarter-turn, spring-return, fail-closed)
- Pneumatic actuator on butterfly valve (quarter-turn, double-acting)
- Electric actuator on gate valve (linear, motor-driven, fail-as-is)
- Manual gearbox on large gate valve (high torque, handwheel operated)

**Source:** Typical actuator detail requirements for process facilities; specific details TBD based on valve types used

### Step 4: Self-Check

**Action:** Originator performs self-check of drawings for completeness, accuracy, and compliance (see Specification.md — Verification section for verification methods).

**Self-Check Items:**
- **Completeness:** All valves from P&IDs are shown on arrangement drawings (see Specification.md — Functional Requirements for required drawing content)
- **Accuracy:** Valve sizes, types, and tag numbers match P&ID and line list (see Datasheet.md — Attributes for valve categories covered)
- **Consistency:** Valve data consistent with DEL-16.03 (sizing calculations) and DEL-16.04 (datasheets) (see Datasheet.md — Construction for materials and configuration)
- **CAD Standards:** Drawing complies with project CAD standards (layers, line weights, symbols, title block) (see Specification.md — Quality Requirements for CAD standards)
- **Clarity:** Drawing is clear and unambiguous; adequate notes and callouts provided (see Guidance.md — Principles for design philosophy to be communicated)
- **Interfaces:** Piping interfaces dimensionally correct; no clashes with adjacent equipment or structure (see Specification.md — Interface Requirements for multi-discipline coordination)

**Documentation:**
- Complete self-check checklist (if project provides standard form) — **TBD**
- Correct any errors or omissions identified during self-check
- Prepare drawing for interdisciplinary check

**Source:** Typical engineering self-check process; checklist TBD per project quality procedures

### Step 5: Interdisciplinary Check (IDC)

**Action:** Coordinate drawing with other disciplines to verify interfaces and resolve conflicts.

**Disciplines to Coordinate:**
1. **Piping (DEL-14.01):** Verify valve-to-piping interface; piping flexibility and stress compliance
2. **Instrumentation (DEL-20.01):** Verify control valve instrumentation (positioners, transmitters, limit switches)
3. **Electrical (DEL-17.01):** Verify electric actuator power supply and conduit routing
4. **Control Systems (DEL-19.01):** Verify control valve interface to DCS/PLC (control signals, hardwired interlocks)
5. **Structural (DEL-06.01):** Verify structural support for large valves; platform and access provisions
6. **Civil (as applicable):** Verify valve foundation requirements (for very large ground-mounted valves)

**IDC Process:**
- Distribute drawing for IDC via project document management system — **TBD**
- Allow review period (typically 5–10 working days) — **TBD**
- Collect IDC comments via project comment management system — **TBD**
- Categorize comments per project convention (e.g., Category A = must resolve, Category B = incorporate if possible, Category C = noted)
- Resolve Category A comments; respond to Category B/C comments
- Update drawing and reissue if significant changes result from IDC

**Source:** Typical IDC process for multi-discipline projects; specific procedures TBD per project quality plan

### Step 6: Independent Check

**Action:** Qualified checker (not the originator) performs independent technical review.

**Independent Check Items:**
- **Technical Correctness:** Valve selections appropriate for service (pressure, temperature, fluid compatibility)
- **Code Compliance:** Valve design complies with applicable codes (API, ASME, CSA B51)
- **Dimensional Accuracy:** Dimensions and elevations are correct and consistent with piping design
- **Calculations Consistency:** Valve sizes consistent with sizing calculations (DEL-16.03)
- **Constructability:** Valve arrangement is constructible; adequate rigging and installation clearances
- **Operability:** Valve operation and maintenance access is adequate
- **Safety:** Relief valve discharge is safe; ESD valves are accessible; fail-safe modes are appropriate

**Checker Markups:**
- Checker annotates drawing with comments using redline/markup tools
- Originator addresses checker comments and updates drawing
- Checker verifies comment resolution and signs/stamps drawing as "Checked"

**Source:** Typical independent check process; specific requirements TBD per project quality procedures

### Step 7: Design Review (for Critical Valves)

**Action:** For safety-critical valves, perform design review with discipline lead and safety/process engineer.

**Critical Valves Requiring Design Review:**
- Pressure relief valves (PRVs)
- Emergency shutdown (ESD) valves
- High-pressure or high-temperature service valves
- Valves identified as safety-critical in HAZOP (DEL-27.02)

**Design Review Items:**
- Relief valve sizing basis and set pressure verification
- Relief valve discharge routing (safe discharge location)
- ESD valve fail-safe mode and closure time
- Compliance with HAZOP recommendations
- Adequacy of isolation for safe maintenance

**Documentation:**
- Document design review meeting minutes — **TBD**
- Obtain design review sign-off from discipline lead

**Source:** Typical design review requirements for safety-critical equipment; specific requirements TBD pending project safety procedures and HAZOP

### Step 8: Approval and Issue

**Action:** Obtain approval signatures and issue drawing per project procedures.

**Approval Signatories:**
- **Originator:** Design engineer who prepared the drawing
- **Checker:** Independent checker who reviewed the drawing
- **Approver:** Discipline lead (P.Eng.) authorized to approve mechanical drawings

**Drawing Issue:**
- Assign drawing number per project drawing register — **TBD**
- Assign revision code (Rev 0 or A for initial issue; increment per project convention) — **TBD**
- Update drawing title block with approval signatures and issue date
- Issue drawing via project document management system — **TBD**
- Update drawing register/index

**Issue Purpose Codes (typical):**
- **IFC (Issued for Construction):** Drawing approved for construction
- **IFA (Issued for Approval):** Drawing issued to Employer or Authority for approval
- **IFR (Issued for Review):** Drawing issued for review/comment (30%, 60%, 90% submittals)

**Source:** Typical drawing issue process; specific codes and procedures TBD per project document control procedures

### Step 9: Vendor Drawing Incorporation (Post-Procurement)

**Action:** After valve procurement, incorporate vendor-specific drawings into design.

**Vendor Drawing Review:**
- Receive valve vendor certified outline drawings and actuator vendor drawings
- Review vendor drawings for compliance with project specification (DEL-16.02) and datasheet (DEL-16.04)
- Verify vendor dimensions match design assumptions (envelope dimensions, connection sizes, weights)
- Identify any discrepancies and resolve via vendor query or design adjustment

**Drawing Update:**
- Update valve arrangement drawings with vendor-specific dimensions (or issue addendum drawing)
- Update actuator details with vendor mounting arrangement (if different from generic detail)
- Reissue drawing with revision increment (e.g., Rev 1 or B)
- Note revision (e.g., "Revised per Vendor XYZ Drawing 12345")

**Source:** Typical vendor drawing incorporation process for EPC projects; specific process TBD per project execution plan

## Verification

**Verification activities for Drawing deliverables:**

### Design Self-Check (Step 4)
- Originator reviews for completeness, accuracy, and CAD standards compliance
- Sign-off: Originator initials and dates drawing title block "Designed By" field — **TBD**

### Interdisciplinary Check (Step 5)
- Multi-discipline coordination to verify interfaces
- Sign-off: IDC complete when Category A comments resolved and drawing updated

### Independent Check (Step 6)
- Qualified checker performs technical review
- Sign-off: Checker signs and stamps drawing title block "Checked By" field — **TBD**

### Design Review (Step 7, for critical valves)
- Discipline lead and safety/process engineer review safety-critical valves
- Sign-off: Design review meeting minutes signed by attendees — **TBD**

### Approval (Step 8)
- Discipline lead (P.Eng.) approves drawing for issue
- Sign-off: Approver signs and stamps drawing title block "Approved By" field with P.Eng. seal — **TBD**

**Acceptance Criteria:**
- All verification steps completed per project quality procedures
- Zero unresolved Category A IDC comments
- Checker and approver signatures obtained
- Drawing complies with CAD standards (passes project CAD file check) — **TBD**
- Drawing number assigned and registered in project drawing register

**Source:** Verification activities typical for engineering drawings; specific sign-off requirements TBD per project quality procedures and authority matrix

## Records

**Documentation outputs:**

### Primary Deliverables
- **Valve arrangement drawings:** Multiple sheets showing valve locations on plan, elevation, and section views
- **Actuator detail drawings:** Typical mounting details for each actuator type used in the project

### Supporting Records
- **Drawing register/index:** List of all valve arrangement and actuator detail drawings with numbers, titles, and revision status
- **IDC comment/response log:** Record of interdisciplinary comments and resolutions
- **Design review minutes:** For safety-critical valves (PRVs, ESDs)
- **Checker markup set:** Redline/markup set showing checker comments and resolutions
- **Vendor drawing submittal/review log:** Record of vendor drawings received and reviewed

**Record Management:**

**During Development (Working Status):**
- Working files maintained in `1_Working/` folder in deliverable directory
- Native CAD files (DWG, DGN, etc.) and PDF markups
- **Source:** Folder structure per README.md Section "What lives where"

**During Review (CHECKING Status):**
- Review package placed in `2_Checking/To/` folder
- Include cover transmittal, drawing index, and PDF set
- Track review comments and responses
- **Source:** Recommended convention per README.md Section 6 (Review and issue)

**Upon Issue (ISSUED Status):**
- Issued drawings placed in `3_Issued/` folder
- Include native CAD files and PDF
- Archive superseded revisions (older issues)
- Update project drawing register
- **Source:** Recommended convention per README.md Section 6 (Review and issue)

**Retention Requirements:**
- Retention period: **TBD** — **ASSUMPTION:** Project life + 25 years typical for design documents
- Archival format: **TBD** — **ASSUMPTION:** PDF/A for long-term preservation, plus native CAD files for future modifications
- Backup and disaster recovery: **TBD** — Per project IT/document management procedures

**Electronic Document Management:**
- **ASSUMPTION:** Electronic records managed in project document management system (e.g., Aconex, ProjectWise, SharePoint, or equivalent)
- Document control procedures: **TBD** — Per project document control plan
- Access permissions: **TBD** — Per project data security requirements

**Source:** Record management practices typical for EPC projects; specific requirements TBD per project procedures

## Revision History and Configuration Management

**Drawing Revisions:**
- Initial issue: Rev 0 (or Rev A) — **TBD** per project convention
- Subsequent revisions: Incremental (Rev 1, 2, 3... or Rev B, C, D...) — **TBD**
- Revision description noted in title block revision table
- Revision clouds and triangles mark changed areas per project CAD standards — **TBD**

**Configuration Control:**
- Drawing supersedes previous revision upon issue
- Prior revision archived but retained for record
- Drawing register maintains current and superseded revision status
- No working from superseded drawings (CAD file management controls) — **TBD**

**Source:** Configuration management typical for engineering drawings; specific procedures TBD per project document control plan
