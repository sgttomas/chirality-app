# Procedure: DEL-11.05 Marine Loading Installation & Test Records

## Purpose

This procedure defines the process for producing and managing **Marine Loading Installation & Test Records** within **PKG-11 Marine Loading System**.

**Deliverable purpose:** Provides evidence of completion, inspection, and testing for the marine loading system, demonstrating compliance with specification requirements and readiness for operation.

**Deliverable type:** Record
**Responsible party:** D&B Contractor (QA/QC)
**Discipline:** Process

## Prerequisites

### Dependencies
- See `_DEPENDENCIES.md` — **NOT_TRACKED**: Dependencies are coordinated externally by humans (see `execution/_Coordination/_COORDINATION.md`)
- Upstream deliverables and input data to be confirmed prior to commencement

### Required Inputs

| Input | Source | Status |
|-------|--------|--------|
| IFC drawings (as-installed reference) | DEL-11.01 Drawing Set | **TBD** |
| Technical specification (acceptance criteria) | DEL-11.02 §9 | **TBD** |
| Equipment datasheets (tag/duty reference) | DEL-11.04 | **TBD** |
| OEM FAT procedures | DEL-11.06 OEM Qualification | **TBD** |
| Project ITP | Project QA/QC | **TBD** |
| ITR templates | Project QA/QC | **TBD** |
| Calibration certificates | Test equipment | **TBD** |

### Reference Materials
- `_REFERENCES.md` — applicable reference document list
- `0_References/` — package reference materials
- Employer's Requirements — **TBD** (specific clause references)
- Applicable codes and standards — **TBD** (confirm per ER and project code register)

### Personnel Requirements
- QA/QC coordinator (records management)
- Process discipline engineer (technical review)
- Qualified inspectors (installation verification)
- Commissioning engineer (functional testing)
- **ASSUMPTION:** Personnel competency per project quality procedures

## Steps

### Step 1: Define Records Index

**Action:** Create records register listing required record types and equipment.

| Task | Output |
|------|--------|
| Review project ITP for PKG-11 hold points | Hold point list |
| Identify required FAT records | FAT record list |
| Identify required installation records | Installation record list |
| Identify required commissioning records | Commissioning record list |
| Create records index with IDs and status | Records index (draft) |

**Required records (from decomposition and project ITP):**

| Category | Record ID | Description | Status |
|----------|-----------|-------------|--------|
| FAT | **TBD** | Loading arm FAT report | Pending |
| FAT | **TBD** | ERC FAT record | Pending |
| FAT | **TBD** | Leak detection FAT | Pending |
| FAT | **TBD** | Sump pump FAT | Pending |
| Installation | **TBD** | Mechanical completion checklist | Pending |
| Installation | **TBD** | Pipe installation checklist | Pending |
| Installation | **TBD** | Instrument installation checklist | Pending |
| Installation | **TBD** | As-installed verification | Pending |
| Commissioning | **TBD** | Loading arm functional test | Pending |
| Commissioning | **TBD** | ERC functional test | Pending |
| Commissioning | **TBD** | Leak detection loop test | Pending |
| Commissioning | **TBD** | ESD integration test | Pending |

### Step 2: Prepare Templates and Procedures

**Action:** Confirm ITR templates and test procedures.

| Task | Source | Output |
|------|--------|--------|
| Obtain project ITR templates | Project QA/QC | Template set |
| Confirm FAT procedures with OEM | DEL-11.06 | FAT procedure list |
| Confirm commissioning procedures | DEL-11.02 §9 | Test procedure list |
| Identify witness/hold points | Project ITP | Witness requirements |
| Confirm acceptance criteria | DEL-11.02, ER | Acceptance criteria list |

### Step 3: Collect FAT Records

**Action:** Obtain FAT records from OEM and vendors.

| Task | Responsibility | Output |
|------|----------------|--------|
| Witness FAT at OEM facility (if required) | QA/Inspector | Witness notes |
| Obtain FAT report package from OEM | Procurement | FAT package |
| Review FAT records for completeness | QA/Engineer | Review notes |
| Verify acceptance criteria met | Engineer | Technical evaluation |
| Obtain calibration certificates | OEM | Calibration certs |
| Log FAT records in index | QA | Updated index |

**FAT record content checklist:**
- [ ] Loading arm functional test (envelope, controls)
- [ ] ERC activation test (release force, valve closure, reset)
- [ ] Leak detection sensor calibration and response
- [ ] Sump pump performance curve
- [ ] Witness signatures (Contractor, Employer as required)

### Step 4: Collect Installation Records

**Action:** Generate installation records during construction.

| Task | Responsibility | Output |
|------|----------------|--------|
| Complete mechanical completion checklists | Inspector | MC checklists |
| Complete pipe installation checklists | Inspector | Pipe checklists |
| Complete instrument installation checklists | Inspector | Instrument checklists |
| Perform as-installed verification | Inspector/Engineer | As-installed records |
| Obtain inspector sign-offs | QA | Signed records |
| Log installation records in index | QA | Updated index |

**Installation record content checklist:**
- [ ] Loading arm installation (alignment, foundation bolting, torques)
- [ ] Double-walled pipe (supports, welds, expansion provisions)
- [ ] Leak detection devices (mounting, wiring, tagging)
- [ ] Sump pump (alignment, connections, motor check)
- [ ] As-installed verification against IFC drawings

### Step 5: Collect Commissioning Records

**Action:** Generate commissioning records during testing.

| Task | Responsibility | Output |
|------|----------------|--------|
| Execute loading arm functional test | Commissioning | Test record |
| Execute ERC functional test | Commissioning | Test record |
| Execute leak detection loop tests | Commissioning/I&C | Loop test records |
| Execute ESD integration test | Commissioning/SIS | Integration test record |
| Obtain witness signatures | QA | Signed records |
| Log commissioning records in index | QA | Updated index |

**Commissioning record content checklist:**
- [ ] Loading arm slew/luff operation and position feedback
- [ ] ERC manual activation and auto-release simulation
- [ ] Leak detection simulated leak response
- [ ] Leak detection alarm and ESD trip verification
- [ ] Sump pump level control and run/stop
- [ ] ESD integration (trip signals, interlocks)

### Step 6: Quality Check

**Action:** Verify completeness and quality of records package.

| Check | Criteria | Record |
|-------|----------|--------|
| Completeness vs. index | All required records present | Completeness check |
| Signature verification | All required signatures obtained | Signature check |
| Acceptance criteria referenced | Each record traces to criteria | Traceability check |
| Calibration certificates current | Certificates valid during test period | Calibration check |
| As-installed matches IFC | Deviations documented | Cross-reference check |

### Step 7: Resolve Gaps and NCRs

**Action:** Address missing records and nonconformances.

| Task | Responsibility | Output |
|------|----------------|--------|
| Identify missing records | QA | Gap list |
| Obtain missing records or document reason | QA/Engineer | Updated records |
| Document nonconformances on NCR | QA | NCR register |
| Obtain NCR disposition | Engineering | Closed NCRs |
| Update punch list | QA | Punch list status |
| Track to closure | QA | Closure evidence |

### Step 8: Compile Submission Package

**Action:** Assemble final records package for turnover.

| Task | Responsibility | Output |
|------|----------------|--------|
| Compile all records per index | QA | Records package |
| Include calibration certificates | QA | Certificates file |
| Include NCR register and closures | QA | NCR file |
| Include punch list status | QA | Punch list file |
| Format per project requirements | QA | Formatted package |
| Submit for review/acceptance | QA | Transmittal |

## Verification

**Verification activities (traceability to Specification.md):**

| Verification Method | Requirements Verified | Record |
|---------------------|----------------------|--------|
| Completeness check | ITR-001 to ITR-007 | Completeness form |
| Traceability check | ITR-003, ITR-004 | Traceability log |
| Signature check | FAT-005, INS-006, COM-008 | Signature log |
| Cross-reference check | INS-004 | As-installed log |
| Calibration check | QA-001 | Calibration log |
| NCR review | QA-002 | NCR register |

**Acceptance checklist (aligns to Datasheet.md and Specification.md):**

| Criterion | Check | Status |
|-----------|-------|--------|
| Records index complete | All records listed | ☐ |
| Each record traceable to acceptance criteria | Traceability check | ☐ |
| Required signatures obtained | Signature check | ☐ |
| Calibration certificates current | Calibration check | ☐ |
| NCRs documented and dispositioned | NCR review | ☐ |
| Punch list items closed or accepted | Punch list review | ☐ |

**Sign-off requirements:**

| Role | Responsibility | Signature Block |
|------|----------------|-----------------|
| QA Coordinator | Records compilation | **TBD** |
| Process Engineer | Technical review | **TBD** |
| QA Manager | Package approval | **TBD** |

**ASSUMPTION:** Sign-off protocol per project quality procedures.

## Records

**Documentation outputs:**
- FAT records package
- Installation records package
- Commissioning test records
- Records index/register
- Calibration certificates file
- NCR register and closures

**Record management:**

| Record | Location | Retention |
|--------|----------|-----------|
| Working records (drafts) | `1_Working/` | Until superseded |
| Review packages | `2_Checking/To/` | Per project procedures |
| Issued records package | `3_Issued/` | Project archive (**TBD**) |
| NCR register | Document control system | Project archive (**TBD**) |
| Calibration certificates | Document control system | Per instrument lifecycle |

**ASSUMPTION:** Electronic records in project document management system.
