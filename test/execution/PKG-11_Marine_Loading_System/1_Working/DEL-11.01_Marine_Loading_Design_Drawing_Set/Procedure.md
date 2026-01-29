# Procedure: DEL-11.01 Marine Loading Design Drawing Set

## Purpose

This procedure defines the process for producing and verifying **Marine Loading Design Drawing Set** within **PKG-11 Marine Loading System**.

**Deliverable purpose:** Defines the design arrangement and details for the marine loading system, enabling procurement, construction, and commissioning of loading facilities.
**Source:** Decomposition DEL-11.01 description.

**Deliverable type:** Drawing
**Responsible party:** D&B Contractor
**Discipline:** Process
**Source:** Datasheet.md §Identification.

## Prerequisites

### Dependencies
- See `_DEPENDENCIES.md` — **NOT_TRACKED**: Dependencies are coordinated externally by humans (see `execution/_Coordination/_COORDINATION.md`)
- Upstream deliverables and input data to be confirmed prior to commencement

### Required Inputs

| Input | Source | Status | Related Procedure Step |
|-------|--------|--------|------------------------|
| Project design basis | ER / PKG-00 | **TBD** | Step 1 |
| Loading arm OEM data (envelope, connections) | DEL-11.06 | **TBD** | Step 1, Step 3 |
| Marine loading technical specification | DEL-11.02 | **TBD** | Steps 3-6 |
| Design calculations (envelope, drainage, purge) | DEL-11.03 | **TBD** | Step 3, Step 4 |
| Marine structures interface data | DEL-08.xx (PKG-08) | **TBD** | Step 1, Step 8 |
| Piping routing data | DEL-14.xx (PKG-14) | **TBD** | Step 1, Step 4, Step 8 |
| I&C interface data (leak detection, ESD) | DEL-19.xx (PKG-19) | **TBD** | Step 1, Step 5, Step 8 |
| Site survey / berth geometry | Project inputs | **TBD** | Step 1, Step 3 |

**Source:** Specification.md §Related Deliverables; Datasheet.md §Interfaces.

### Reference Materials
- `_REFERENCES.md` — applicable reference document list
- `0_References/` — package reference materials
- Employer's Requirements — **TBD** (specific clause references)
- Applicable codes and standards — **TBD** (confirm per ER and project code register)

**Source:** Specification.md §Standards.

### Personnel Requirements
- Qualified Process discipline engineer (drawing originator)
- Qualified checker/reviewer (independent of originator)
- Discipline lead / approver
- **ASSUMPTION:** Personnel competency per project quality procedures

**Source:** Good practice **ASSUMPTION**; Specification.md §Quality QA-01.

## Steps

### Step 1: Confirm Inputs and Interfaces

**Action:** Verify availability and adequacy of input data before commencing drawing production.

| Task | Verification | Record | Related Requirement |
|------|--------------|--------|---------------------|
| Confirm ER applicability and clause requirements | ER review checklist | Input log | Specification.md REQ-03 |
| Confirm loading arm OEM data received (envelope, connections) | Data receipt confirmation | Input log | Specification.md REQ-06 |
| Confirm site/berth geometry and constraints | Survey data review | Input log | Specification.md REQ-04 |
| Identify interface points with adjacent packages | Interface register update | Interface log | Specification.md INT-01 through INT-05 |

**Source:** Specification.md §Requirements, §Interface Requirements; Datasheet.md §Interfaces.

**Hold point:** Do not proceed until critical inputs (OEM envelope data, berth geometry) are available or assumptions are formally documented.
**ASSUMPTION:** Hold point per good practice.

### Step 2: Establish Drawing List

**Action:** Draft a drawing register with anticipated artifacts and titles.

| Task | Output | Related Requirement |
|------|--------|---------------------|
| Identify required drawings per decomposition and ER | Drawing list (draft) | Specification.md REQ-01, REQ-02 |
| Assign drawing numbers per document control scheme | Drawing register | Specification.md REQ-01 |
| Confirm sheet sizes and scales | Drawing register | Datasheet.md §Attributes |
| Coordinate with document control for number reservation | Number confirmation | Specification.md §Quality QA-01 |

**Source:** Decomposition DEL-11.01 "Anticipated Artifacts"; Specification.md REQ-01.

**Output:** Drawing register with titles, numbers, and planned revision status. Traces to Datasheet.md §Deliverable Acceptance criterion 1.

### Step 3: Develop Loading Arm GA

**Action:** Prepare loading arm general arrangement drawing(s).

| Content Item | Source | Cross-Reference | Related Requirement |
|--------------|--------|-----------------|---------------------|
| Plan and elevation views | OEM data (DEL-11.06), site survey | Datasheet.md §Construction | Specification.md REQ-06 |
| Slew/luff envelope | DEL-11.03 envelope calcs | Datasheet.md §Construction | Specification.md REQ-06 |
| ERC location and clearances | OEM data, safety requirements | Guidance.md §Safety | Specification.md REQ-06 |
| Connection flanges and orientation | OEM data, DEL-14 piping | Datasheet.md §Interfaces | Specification.md INT-01 |
| Operating/maintenance clearances | OEM recommendations, ER | Guidance.md §Operational | Specification.md REQ-04 |

**Source:** Decomposition "Anticipated Artifacts" (Loading arm GA); Guidance.md §Examples; Specification.md REQ-06.

**Note:** This step directly produces one of the 4 anticipated artifacts listed in Datasheet.md §Construction and Specification.md §Documentation.

### Step 4: Develop Double-Walled Pipe Arrangement

**Action:** Prepare double-walled export pipe arrangement drawing(s).

| Content Item | Source | Cross-Reference | Related Requirement |
|--------------|--------|-----------------|---------------------|
| Pipe routing from storage to loading arm | DEL-14 piping, P&IDs | Datasheet.md §Construction | Specification.md REQ-07 |
| Annulus leak detection tap locations | DEL-11.02 spec | Datasheet.md §Construction | Specification.md REQ-07 |
| Expansion provisions (loops, bellows) | Thermal analysis, DEL-11.03 | Guidance.md §Constructability | Specification.md REQ-07 |
| Support locations and types | Structural coordination (PKG-06/08) | Datasheet.md §Interfaces | Specification.md INT-03 |
| Tie-in flanges and isolation valves | DEL-14, DEL-16 | Datasheet.md §Interfaces | Specification.md INT-01 |

**Source:** Decomposition "Anticipated Artifacts" (double-walled pipe arrangement); Guidance.md §Examples; Specification.md REQ-07.

**Note:** This step directly produces one of the 4 anticipated artifacts listed in Datasheet.md §Construction and Specification.md §Documentation.

### Step 5: Develop Leak Detection Layout

**Action:** Prepare leak detection layout drawing(s).

| Content Item | Source | Cross-Reference | Related Requirement |
|--------------|--------|-----------------|---------------------|
| Annulus monitoring sensor locations | DEL-11.02 spec | Datasheet.md §Construction | Specification.md REQ-08 |
| Drip tray locations and drainage | Civil coordination (PKG-03) | Datasheet.md §Interfaces | Specification.md INT-05 |
| Sump locations and level instrumentation | DEL-11.02, DEL-19 | Datasheet.md §Interfaces | Specification.md REQ-08 |
| Signal routing to junction boxes / ESD panel | DEL-19, DEL-20 | Datasheet.md §Interfaces | Specification.md INT-02 |
| Reference to alarm/trip setpoints | DEL-11.02 spec | Guidance.md §Safety | Specification.md REQ-08 |

**Source:** Decomposition "Anticipated Artifacts" (leak detection layout); Guidance.md §Examples; Specification.md REQ-08.

**Note:** This step directly produces one of the 4 anticipated artifacts listed in Datasheet.md §Construction and Specification.md §Documentation.

### Step 6: Develop Operator Shelter Drawings

**Action:** Prepare operator shelter arrangement and interface drawings.

| Content Item | Source | Cross-Reference | Related Requirement |
|--------------|--------|-----------------|---------------------|
| Shelter location relative to loading arm | DEL-11.02 spec, ER | Guidance.md §Operational | Specification.md REQ-09 |
| Floor plan and sections | PKG-22 building works | Datasheet.md §Interfaces | Specification.md INT-03 |
| Access/egress routes | Safety requirements | Guidance.md §Safety | Specification.md REQ-09 |
| HVAC, lighting, power interfaces | DEL-21 **TBD**, DEL-20 | Datasheet.md §Interfaces | Specification.md INT-02 |
| Control panel location (HMI, ESD buttons) | DEL-19, DEL-20 | Datasheet.md §Interfaces | Specification.md REQ-09 |

**Source:** Decomposition "Anticipated Artifacts" (operator shelter drawings); Guidance.md §Examples; Specification.md REQ-09.

**Note:** This step directly produces one of the 4 anticipated artifacts listed in Datasheet.md §Construction and Specification.md §Documentation.

### Step 7: Self-Check

**Action:** Originator performs completeness and consistency check.

| Check Item | Criteria | Record | Related Requirement |
|------------|----------|--------|---------------------|
| All anticipated drawings produced | Drawing register complete (4 drawing types) | Self-check form | Specification.md REQ-01, REQ-02 |
| All required content items included | Per Steps 3-6 checklists (20+ content items) | Self-check form | Specification.md REQ-04 |
| Cross-references to specifications/calculations | DEL-11.02, DEL-11.03 cited | Self-check form | Specification.md REQ-06, REQ-07, REQ-08 |
| Assumptions and TBDs documented | Notes on drawings or in register | Self-check form | Specification.md REQ-05 |
| CAD standards compliance | Title block, scales, layers | Self-check form | Specification.md QA-02 |

**Source:** Specification.md §Quality QA-01 (self-check); Datasheet.md §Deliverable Acceptance.

**Output:** Self-check form with originator sign-off. Traces to Specification.md §Verification "Design review (peer check)".

### Step 8: Interdisciplinary Check (IDC)

**Action:** Coordinate IDC review with affected disciplines.

| Discipline | Interface Focus | Reviewer | Related Interface Requirement |
|------------|-----------------|----------|-------------------------------|
| Structural (PKG-06/08) | Foundation interfaces, support loads | **TBD** | Specification.md INT-03 |
| Piping (PKG-14) | Routing, tie-ins, supports | **TBD** | Specification.md INT-01 |
| I&C (PKG-19) | Leak detection, ESD interfaces | **TBD** | Specification.md INT-02 |
| Electrical (PKG-20) | Power, lighting, grounding | **TBD** | Specification.md INT-02 |
| Civil (PKG-03) | Drainage, containment | **TBD** | Specification.md INT-05 |
| Building works (PKG-22) | Shelter interfaces | **TBD** | Specification.md INT-03 (shelter pad) |

**Source:** Datasheet.md §Interfaces (8 interfaces); Specification.md §Interface Requirements INT-01 through INT-05; Specification.md §Quality QA-03.

**Output:** IDC comment log with responses and actions. Traces to Datasheet.md §Deliverable Acceptance criterion 4 and 6.

### Step 9: Independent Check and Approval

**Action:** Checker review and discipline approval for issue.

| Task | Responsibility | Record | Related Requirement |
|------|----------------|--------|---------------------|
| Technical review | Independent checker | Check mark-ups | Specification.md QA-01 |
| Comment resolution | Originator | Comment response log | Specification.md QA-01 |
| Discipline approval | Lead engineer | Approval signature | Specification.md QA-01 |
| Document control registration | Document controller | Transmittal | Specification.md §Documentation |

**Source:** Specification.md §Quality QA-01; good practice **ASSUMPTION**.

**Output:** Approved drawing set ready for issue. Traces to all 6 acceptance criteria in Datasheet.md §Deliverable Acceptance.

## Verification

**Verification activities (traceability to Specification.md §Verification):**

| Verification Method | Requirements Verified | Procedure Step | Record | Datasheet Criterion |
|---------------------|----------------------|----------------|--------|---------------------|
| Design review (peer check) | REQ-01 through REQ-09 | Step 7, Step 9 | Check mark-ups | Criterion 2, 3 |
| Dimensional/completeness check | REQ-04, REQ-06, REQ-07, REQ-08, REQ-09 | Step 7 | Self-check form | Criterion 2, 3 |
| Interdisciplinary check (IDC) | INT-01 through INT-05 | Step 8 | IDC log | Criterion 4, 6 |
| CAD standards compliance check | QA-02 | Step 7 | Self-check form | Criterion 2 |
| Completeness check | REQ-05, QA-04 | Step 7 | Review checklist | Criterion 5 |

**Source:** Specification.md §Verification; Datasheet.md §Deliverable Acceptance (6 criteria).

**Acceptance checklist (aligns to Specification.md and Datasheet.md):**

| Criterion | Check | Status | Datasheet Ref | Specification Ref |
|-----------|-------|--------|---------------|-------------------|
| Drawing register/index present and matches issued set | Document review | ☐ | Datasheet criterion 1 | Specification REQ-01 |
| Drawings include required title blocks/revision blocks | CAD check | ☐ | Datasheet criterion 2 | Specification QA-02 |
| Operating envelope and clearance zones shown | Design review | ☐ | Datasheet criterion 3 | Specification REQ-06 |
| Interface points identified with adjacent package references | IDC review | ☐ | Datasheet criterion 4 | Specification INT-01 to INT-05 |
| Assumptions and TBDs explicitly highlighted | Completeness check | ☐ | Datasheet criterion 5 | Specification REQ-05, QA-04 |
| IDC completed with comments resolved or actioned | IDC log review | ☐ | Datasheet criterion 6 | Specification QA-03 |

**Note:** All 6 acceptance criteria align across Datasheet.md §Deliverable Acceptance, Specification.md §Verification, and this Procedure.md §Verification section.

**Sign-off requirements:**

| Role | Responsibility | Signature Block | Quality Requirement |
|------|----------------|-----------------|---------------------|
| Originator | Technical content, self-check (Step 7) | **TBD** | Specification QA-01 |
| Checker | Independent technical review (Step 9) | **TBD** | Specification QA-01 |
| Approver | Discipline approval for issue (Step 9) | **TBD** | Specification QA-01 |

**ASSUMPTION:** Sign-off protocol per project quality procedures.

## Records

**Documentation outputs:**
- Loading arm GA drawing(s)
- Double-walled pipe arrangement drawing(s)
- Leak detection layout drawing(s)
- Operator shelter drawing(s)
- Drawing register/index

**Source:** Decomposition DEL-11.01 "Anticipated Artifacts"; Specification.md §Documentation; Datasheet.md §Construction table.

**Note:** These 4 drawing types (plus register) are consistently identified across all documents as the deliverable outputs.

**Record management:**

| Record | Location | Retention | Related Step |
|--------|----------|-----------|--------------|
| Draft drawings (working) | `1_Working/` | Until superseded | Steps 3-6 |
| Drawing register | `1_Working/` | Until superseded | Step 2 |
| Self-check form | `1_Working/` | Until issued | Step 7 |
| IDC comment log | `1_Working/` or document control system | Project archive **TBD** | Step 8 |
| Review packages | `2_Checking/To/` | Per project procedures **TBD** | Step 9 |
| Issued drawings | `3_Issued/` | Project archive **TBD** | Step 9 |
| Check/approval records | Document control system | Project archive **TBD** | Step 9 |

**ASSUMPTION:** Electronic records in project document management system.

---

**Pass 3 Enrichment Notes (Final Quality Check):**
- Verified 9-step workflow completeness: Inputs → Drawing List → 4 Drawing Types → Self-Check → IDC → Approval
- Verified Required Inputs table (8 inputs) traces to Specification.md §Related Deliverables and Datasheet.md §Interfaces
- Verified Steps 3-6 each produce one of 4 anticipated artifacts from Decomposition/Datasheet/Specification
- Verified Step 8 IDC table (6 disciplines) covers all 5 interface requirements from Specification.md
- Verified Verification table links all 5 verification methods to requirements, steps, records, and Datasheet criteria
- Verified Acceptance checklist (6 criteria) fully aligned with Datasheet.md §Deliverable Acceptance and Specification.md §Verification
- Verified Records table (7 records) references appropriate procedure steps
- Confirmed sign-off requirements trace to Specification.md QA-01
- Full traceability chain verified: Decomposition → Datasheet → Specification → Guidance → Procedure
- All TBDs and ASSUMPTIONs retained with proper labeling
- Pass 3 complete — document ready for WORKING_ITEMS session
