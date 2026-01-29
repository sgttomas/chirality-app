# Specification: DEL-11.01 Marine Loading Design Drawing Set

## Scope

This specification defines the requirements for **Marine Loading Design Drawing Set** within **PKG-11 Marine Loading System**.

**Purpose:** Defines the design arrangement and details for the marine loading system per Employer's Requirements (ER), enabling procurement, construction, and commissioning of the loading facilities.
**Source:** Decomposition DEL-11.01 description.

**Package scope (PKG-11):**
- Powered loading arm (articulated boom with powered slew/luff)
- Emergency release coupling (ERC)
- Double-walled export pipe
- Leak detection system
- Nitrogen supply provisions
- Operator shelter

**Source:** Decomposition PKG-11 scope statement.

**Anticipated deliverable artifacts:**
- Loading arm general arrangement (GA) drawing(s)
- Double-walled export pipe arrangement drawing(s)
- Leak detection layout drawing(s)
- Operator shelter drawing(s)

**Source:** Decomposition DEL-11.01 "Anticipated Artifacts" field.

**Objectives served (per decomposition Section 6):**
- OBJ-1 Safe & Reliable Operation
- OBJ-2 Throughput Capacity (1,000,000 MT/annum)
- OBJ-4 Operational Flexibility
- OBJ-7 Environmental Protection

**Source:** Datasheet.md §Objectives Mapping.

## Related Deliverables (PKG-11)

| Deliverable | Relationship | Status |
|-------------|--------------|--------|
| DEL-11.02 Marine Loading Technical Specification | System requirements governing drawing content | **TBD** |
| DEL-11.03 Marine Loading Design Calculations | Envelope, drainage, purge calculations supporting dimensions | **TBD** |
| DEL-11.04 Marine Loading Data Sheet Package | Equipment datasheets cross-referenced on drawings | **TBD** |
| DEL-11.05 Marine Loading Installation & Test Records | Installation/commissioning records referencing drawings | **TBD** |
| DEL-11.06 Marine Loading Arm OEM Qualification Package | Vendor GA and envelope data as drawing inputs | **TBD** |

**Source:** Decomposition PKG-11 deliverable table.

## Requirements

### Drawing Set Requirements

| Req ID | Requirement | Source | Verification |
|--------|-------------|--------|--------------|
| REQ-01 | Provide a drawing register/index identifying all drawings (titles, numbers, revision, status) | Decomposition / project standards **ASSUMPTION** | Document review per Procedure.md §Step 2 |
| REQ-02 | Drawings shall clearly identify all PKG-11 scope components: powered loading arm, ERC, double-walled pipe, leak detection, nitrogen supply, operator shelter | Decomposition PKG-11 scope | Design review per Procedure.md §Step 7 |
| REQ-03 | Drawings shall be suitable to support procurement, installation, and commissioning planning | ER **TBD** / good practice **ASSUMPTION** | Design review per Procedure.md §Step 9 |
| REQ-04 | Each drawing shall include key dimensions, elevations, operating envelope, access/maintenance clearances, and interface/tie-in identification | ER **TBD** / good practice **ASSUMPTION** | Dimensional check per Procedure.md §Verification |
| REQ-05 | Drawing notes shall identify assumptions and TBD items requiring resolution | Project QA standards **TBD** | Completeness check per Procedure.md §Step 7 |
| REQ-06 | Loading arm GA shall show slew/luff envelope, ERC location, and connection flanges | DEL-11.06 OEM data / DEL-11.03 calcs | Design review per Procedure.md §Step 3 |
| REQ-07 | Double-walled pipe arrangement shall show routing, annulus leak detection taps, and expansion provisions | DEL-11.02 spec / DEL-14 interfaces | Design review per Procedure.md §Step 4 |
| REQ-08 | Leak detection layout shall show sensor locations, signal routing, and reference to alarm/trip setpoints | DEL-11.02 spec / DEL-19 I&C | Design review per Procedure.md §Step 5 |
| REQ-09 | Operator shelter drawings shall show location, access/egress, and interface to loading arm controls | DEL-11.02 spec / PKG-22 | Design review per Procedure.md §Step 6 |

**Note:** All requirements trace to verification activities in Procedure.md and acceptance criteria in Datasheet.md §Deliverable Acceptance.

### Interface Requirements

| Req ID | Requirement | Adjacent Deliverable | Verification |
|--------|-------------|---------------------|--------------|
| INT-01 | Identify interface points for metering/custody transfer tie-ins | DEL-12.xx (PKG-12 Product Transfer & Metering) | IDC review per Procedure.md §Step 8 |
| INT-02 | Identify electrical/instrumentation interfaces for leak detection and ESD/alarm signals | DEL-19.xx (PKG-19 Control Systems), DEL-20.xx (PKG-20 **TBD**) | IDC review per Procedure.md §Step 8 |
| INT-03 | Identify civil/structural interfaces (loading arm foundation, shelter pad, pipe supports) | DEL-08.xx (PKG-08 Marine Structures), PKG-06 Structural Steelwork | IDC review per Procedure.md §Step 8 |
| INT-04 | Identify utilities interfaces (nitrogen supply point) | **TBD** — nitrogen supply package not explicitly defined in decomposition | IDC review per Procedure.md §Step 8 |
| INT-05 | Identify spill containment/drainage interfaces (secondary containment, sumps) | DEL-03.xx (PKG-03 Underground Utilities & Drainage) | IDC review per Procedure.md §Step 8 |

**Note:** Dependency tracking is NOT_TRACKED; interfaces are coordinated externally per `_DEPENDENCIES.md` and `execution/_Coordination/_COORDINATION.md`.

### Quality Requirements

| Req ID | Requirement | Source | Verification |
|--------|-------------|--------|--------------|
| QA-01 | All drawings shall comply with project QA/QC procedures (originator self-check and independent check) | Project QA procedures **TBD** | Check records per Procedure.md §Step 7, §Step 9 |
| QA-02 | Drawings shall conform to project CAD/drafting standards and title block conventions | Project CAD standards **TBD** | CAD compliance check per Procedure.md §Step 7 |
| QA-03 | Interdisciplinary check (IDC) required prior to issue | Project IDC procedure **TBD** | IDC sign-off per Procedure.md §Step 8 |
| QA-04 | All interface items shall be coordinated with adjacent packages prior to IFC issue | Project coordination procedure **TBD** | IDC records per Procedure.md §Step 8 |

## Standards

| Standard | Applicability | Status |
|----------|---------------|--------|
| Employer's Requirements (ER) | Baseline contract requirements | Clause references **TBD** |
| Project CAD/drafting standards | Drawing format and conventions | **TBD** |
| ASME B31.3 (or equivalent) | Piping shown on drawings | **TBD** — confirm per ER |
| API 2610 | Terminal piping design | **TBD** — confirm per ER |
| NFPA 30 | Flammable liquids handling | **TBD** — confirm per ER |
| CSA/NBC | Building code (operator shelter) | **TBD** — confirm per ER |
| OCIMF guidelines | Marine loading arms **ASSUMPTION** | **TBD** — confirm per ER |

**Note:** Standards list aligns with Guidance.md §Principles and references Datasheet.md §References.

## Verification

**Verification methods for Drawing deliverables:**

| Method | Description | Applies To | Record Reference |
|--------|-------------|------------|------------------|
| Design review (peer check) | Technical content review by qualified engineer | REQ-01 through REQ-09 | Procedure.md §Step 9 |
| Dimensional/completeness check | Verification of dimensions and coverage against inputs | REQ-04, REQ-06, REQ-07 | Procedure.md §Verification |
| Interdisciplinary check (IDC) | Cross-discipline coordination review | INT-01 through INT-05 | Procedure.md §Step 8 |
| CAD standards compliance check | Verification of drawing format and conventions | QA-02 | Procedure.md §Step 7 |
| Completeness check | Verification of TBD/assumption closure | REQ-05, QA-04 | Procedure.md §Step 7, §Verification |

**Acceptance criteria (traceability to Datasheet.md §Deliverable Acceptance):**
- Drawing register present and matches drawing set (Datasheet criterion 1)
- No unresolved clashes at identified interfaces (or clashes logged with actions) (Datasheet criterion 4)
- All assumptions and TBDs either closed or explicitly highlighted for action (Datasheet criterion 5)
- IDC sign-off obtained (Datasheet criterion 6)
- Title blocks, scales, key notes present per CAD standards (Datasheet criterion 2)
- Operating envelope and clearances shown (Datasheet criterion 3)

**Verification traceability:**
- Verification activities executed and recorded per `Procedure.md` (DEL-11.01) §Steps and §Verification
- Acceptance criteria align with `Datasheet.md` §Deliverable Acceptance
- Verification methods trace to Procedure.md steps as noted in table above

## Documentation

**Required documentation outputs:**
- Loading arm general arrangement (GA) drawing(s)
- Double-walled export pipe arrangement drawing(s)
- Leak detection layout drawing(s)
- Operator shelter drawing(s)
- Drawing register/index

**Source:** Decomposition DEL-11.01 "Anticipated Artifacts" and §Requirements REQ-01.

**Documentation requirements:**
- All documents shall comply with project document control procedures **TBD**
- Revision control per project numbering system — **TBD**
- Native CAD and PDF formats — **TBD** **ASSUMPTION**
- Filing per Procedure.md §Records

**Cross-reference:** Datasheet.md §Construction table, Procedure.md §Records.

---

**Pass 2/3 Enrichment Notes:**
- Enhanced traceability between requirements and Procedure.md verification steps
- Added Record Reference column to verification methods table
- Expanded acceptance criteria to explicitly link each Datasheet criterion
- Added OCIMF guidelines to Standards table (referenced in Guidance.md)
- Clarified nitrogen supply interface INT-04 with TBD note (package not explicit in decomposition)
- Added cross-references to source documents for all major sections
- All TBDs and ASSUMPTIONs preserved from Pass 1
