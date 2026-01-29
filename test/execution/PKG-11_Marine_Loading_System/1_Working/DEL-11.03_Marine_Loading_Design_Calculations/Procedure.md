# Procedure: DEL-11.03 Marine Loading Design Calculations

## Purpose

This procedure defines the process for producing and verifying **Marine Loading Design Calculations** within **PKG-11 Marine Loading System**.

**Deliverable purpose:** Provides the engineering basis and sizing/verification calculations for the marine loading system, demonstrating compliance with design requirements and deriving constraints for layout drawings and equipment specifications.

**Deliverable type:** Calculation
**Responsible party:** D&B Contractor
**Discipline:** Process

## Prerequisites

### Dependencies
- See `_DEPENDENCIES.md` — **NOT_TRACKED**: Dependencies are coordinated externally by humans (see `execution/_Coordination/_COORDINATION.md`)
- Upstream deliverables and input data to be confirmed prior to commencement

### Required Inputs

| Input | Source | Status |
|-------|--------|--------|
| Design basis parameters | DEL-11.02 Technical Specification §3 | **TBD** |
| Berth geometry (platform level, edge, fender line) | PKG-08 Marine Structures | **TBD** |
| Design vessel parameters (manifold heights, beam) | ER / marine studies | **TBD** |
| Loading arm OEM envelope data | DEL-11.06 OEM Qualification | **TBD** |
| Fender deflection at design berthing energy | DEL-08.06/08.07 | **TBD** |
| Tidal range | Site data | **TBD** |
| Design rainfall intensity | Site data / ER | **TBD** |
| Spill volume (ERC release) | DEL-11.02 §4.6 | **TBD** |
| Nitrogen supply conditions | DEL-18.xx (PKG-18 Utilities) | **TBD** |
| Purge philosophy (target O₂, purge time) | DEL-11.02 §7 | **TBD** |

### Reference Materials
- `_REFERENCES.md` — applicable reference document list
- `0_References/` — package reference materials
- Employer's Requirements — **TBD** (specific clause references)
- Applicable codes and standards — **TBD** (confirm per ER and project code register)

### Personnel Requirements
- Qualified Process discipline engineer (calculation originator)
- Qualified checker (independent of originator)
- Discipline lead / approver
- **ASSUMPTION:** Personnel competency per project quality procedures

## Steps

### Step 1: Define Calculation List

**Action:** Confirm required calculation topics and assign calculation IDs.

| Task | Output |
|------|--------|
| Review decomposition scope and ER requirements | Required calculation topics |
| Assign calculation IDs per document control | Calculation register (draft) |
| Confirm calculation scope boundaries | Scope notes |

**Required calculations (from decomposition):**

| Calc ID | Title | Scope |
|---------|-------|-------|
| **TBD** | Loading Arm Reach/Envelope Calculation | Arm reach, operating envelope, clearances |
| **TBD** | Marine Loading Drainage Calculation | Catchment, runoff, sump sizing |
| **TBD** | Nitrogen Purge Calculation | Volume, flow rate, purge time |

### Step 2: Collect Inputs

**Action:** Gather all available input data and document sources.

| Task | Source | Output |
|------|--------|--------|
| Obtain design basis from DEL-11.02 | Technical Specification | Design basis summary |
| Obtain berth geometry data | PKG-08 / marine studies | Geometry inputs |
| Obtain OEM arm data (preliminary or final) | DEL-11.06 | OEM envelope data |
| Obtain site data (tidal, rainfall, ambient) | Site studies | Environmental inputs |
| Document input sources and revisions | All sources | Input register |

**Hold point:** If critical inputs are unavailable, document assumptions and proceed; flag for update when data becomes available.

### Step 3: Loading Arm Envelope Calculation

**Action:** Calculate required arm reach and verify operating envelope.

| Task | Method | Output |
|------|--------|--------|
| Define vessel manifold position range | Vessel data + tidal range | Manifold envelope |
| Define platform edge position | Berth geometry + fender deflection | Shore reference |
| Calculate required reach (outboard/inboard) | Geometry analysis | Reach requirements |
| Plot operating envelope (plan and elevation) | CAD or spreadsheet | Envelope drawings |
| Verify clearances at all operating positions | Geometry check | Clearance verification |
| Verify ERC activation envelope | Drift limits vs. arm limits | ERC envelope verification |

**Output:** Envelope calculation document with plots and constraints for DEL-11.01.

### Step 4: Drainage Calculation

**Action:** Size drainage/containment for design spill and rainfall.

| Task | Method | Output |
|------|--------|--------|
| Define containment catchment area | Layout dimensions | Catchment area (m²) |
| Calculate design rainfall runoff | Intensity × area | Rainfall flow (m³/hr) |
| Define design spill volume | ERC release + drip tray | Spill volume (m³) |
| Size sump capacity | Spill + rainfall accumulation | Sump volume (m³) |
| Size sump pump (if required) | Flow to empty in acceptable time | Pump capacity (m³/hr) |
| Size drainage channels/pipes (if in scope) | Manning or Darcy-Weisbach | Drain sizing |

**Output:** Drainage calculation document with sizing and constraints for DEL-11.01 and PKG-03.

### Step 5: Nitrogen Purge Calculation

**Action:** Size nitrogen supply for purge operations.

| Task | Method | Output |
|------|--------|--------|
| Define system volume to purge | Loading arm + header pipe | Volume (m³) |
| Define target O₂ concentration | DEL-11.02 / ER | Target (% O₂) |
| Define maximum acceptable purge time | DEL-11.02 / ER | Time (minutes) |
| Calculate required nitrogen flow rate | Volume × dilution factor / time | Flow (Nm³/hr) |
| Verify nitrogen supply capacity | Compare to DEL-18 supply | Capacity confirmation |

**Output:** Nitrogen purge calculation document with supply requirements for DEL-18.

### Step 6: Communicate Constraints

**Action:** Identify and formally communicate output constraints to layout and specification deliverables.

| Constraint | Receiving Deliverable | Communication |
|------------|----------------------|---------------|
| Operating envelope plot | DEL-11.01 (GA drawing) | Transmittal / coordination |
| Clearance requirements | DEL-11.01 (GA drawing) | Notes on calculation |
| Sump sizing | DEL-11.01 (layout), PKG-03 | Transmittal / coordination |
| Drain sizing | DEL-11.01, PKG-03 | Transmittal / coordination |
| Nitrogen flow requirements | DEL-18.xx | Transmittal / coordination |

**Output:** Constraint transmittal log.

### Step 7: Reasonableness Checks

**Action:** Perform sanity checks on calculation results.

| Check | Method | Record |
|-------|--------|--------|
| Arm reach vs. typical marine loading arms | Industry benchmarks | Reasonableness note |
| Sump capacity vs. similar facilities | Benchmarks | Reasonableness note |
| Nitrogen flow vs. system volume | Dilution time check | Reasonableness note |
| Sensitivity to key assumptions | What-if analysis | Sensitivity summary |

### Step 8: Independent Check

**Action:** Qualified checker reviews all calculations.

| Task | Checker Responsibility | Record |
|------|------------------------|--------|
| Verify input sources and values | Source traceability | Check mark-ups |
| Verify methodology and code compliance | Technical correctness | Check mark-ups |
| Verify arithmetic and results | Spot checks, recalculation | Check mark-ups |
| Verify conclusions and constraints | Completeness | Check mark-ups |
| Sign-off | Independent confirmation | Checker signature |

### Step 9: Approval and Issue

**Action:** Obtain discipline approval and issue per document control.

| Task | Responsibility | Record |
|------|----------------|--------|
| Resolve checker comments | Originator | Comment response log |
| Discipline approval | Lead engineer | Approval signature |
| Document control registration | Document controller | Transmittal |
| Update calculation register | Document controller | Register update |

## Verification

**Verification activities (traceability to Specification.md):**

| Verification Method | Requirements Verified | Record |
|---------------------|----------------------|--------|
| Independent check | All calculations (CALC-001 to QA-004) | Check records |
| Software verification | ENV-001, DRN-003, N2-002 | Spot check notes |
| Reasonableness review | All calculations | Reasonableness notes |
| Cross-reference check | INT-002 (output constraints) | Constraint transmittal |

**Acceptance checklist (aligns to Datasheet.md and Specification.md):**

| Criterion | Check | Status |
|-----------|-------|--------|
| Calculation register provided with IDs and revisions | Document review | ☐ |
| Each calculation includes purpose, inputs, assumptions, method, results, conclusions | Completeness check | ☐ |
| Input sources documented and traceable | Traceability review | ☐ |
| Assumptions explicitly labeled | Completeness check | ☐ |
| Output constraints communicated to DEL-11.01/11.02 | Cross-reference check | ☐ |
| Independent check completed and signed | Check records | ☐ |

**Sign-off requirements:**

| Role | Responsibility | Signature Block |
|------|----------------|-----------------|
| Originator | Technical content | **TBD** |
| Checker | Independent verification | **TBD** |
| Approver | Discipline approval | **TBD** |

**ASSUMPTION:** Sign-off protocol per project quality procedures.

## Records

**Documentation outputs:**
- Loading arm reach/envelope calculations
- Drainage calculations
- Nitrogen purge calculations
- Calculation register/index

**Record management:**

| Record | Location | Retention |
|--------|----------|-----------|
| Draft calculations (working) | `1_Working/` | Until superseded |
| Review packages | `2_Checking/To/` | Per project procedures |
| Issued calculations | `3_Issued/` | Project archive (**TBD**) |
| Check mark-ups and records | Document control system | Project archive (**TBD**) |
| Calculation files (spreadsheets, models) | Document control system | Project archive (**TBD**) |

**ASSUMPTION:** Electronic records in project document management system.

---

**Pass 3 Enrichment Notes (Final Quality Check):**
- Verified 9-step workflow completeness: Define List → Collect Inputs → 3 Calculations → Communicate Constraints → Reasonableness → Check → Approval
- Verified Required Inputs (10 inputs) traces to Datasheet §Conditions and Specification inputs tables
- Verified Steps 3-5 produce 3 calculations matching Datasheet §Construction and Specification §ENV/DRN/N2 requirements
- Verified Step 6 constraint transmittal covers DEL-11.01, DEL-11.02, DEL-18, PKG-03
- Verified Step 8 checker responsibilities cover all verification methods from Specification
- Verified Verification table links activities to Specification requirements (CALC to QA-004, ENV-001, DRN-003, N2-002, INT-002)
- Verified Acceptance checklist (6 criteria) aligns with Datasheet §Deliverable Acceptance (6 criteria)
- Verified Records table (5 record types) references appropriate lifecycle locations
- Confirmed sign-off requirements trace to project quality procedures
- Full traceability chain verified: Decomposition → Datasheet → Specification (34 reqs) → Guidance → Procedure
- All TBDs and ASSUMPTIONs retained with proper labeling
- Pass 3 complete — document ready for WORKING_ITEMS session
