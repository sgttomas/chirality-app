# Datasheet: DEL-11.05 Marine Loading Installation & Test Records

## Identification

| Field | Value |
|-------|-------|
| Deliverable ID | DEL-11.05 |
| Name | Marine Loading Installation & Test Records |
| Package | PKG-11 Marine Loading System |
| Discipline | Process |
| Type | Record |
| Responsible | D&B Contractor (QA/QC) |
| Status | INITIALIZED |

## Objectives Mapping

This deliverable contributes to the following project objectives (per decomposition Section 6):
- **OBJ-1 Safe & Reliable Operation** — records verify safety-critical systems (ERC, leak detection, ESD) function as designed
- **OBJ-2 Throughput Capacity (1,000,000 MT/annum)** — records verify equipment meets design capacity
- **OBJ-4 Operational Flexibility** — records verify operating envelope meets specification
- **OBJ-7 Environmental Protection** — records verify leak detection and containment systems are functional

## Attributes

| Attribute | Value |
|-----------|-------|
| Records index / MDR register | **TBD** — list of records with IDs, equipment tags, dates, status |
| Record categories | FAT / installation / functional testing / commissioning |
| Witness/hold points | **TBD** — per ER and project ITP |
| Retention period | **TBD** — per project document control |
| Revision | **TBD** |
| Classification | **TBD** |

## Conditions

**Operating / Environmental Context:**

Provides evidence of completion, inspection, and testing for the marine loading system, demonstrating compliance with specification requirements and readiness for operation.

**Record generation context:**
- FAT records generated at OEM facility prior to shipment
- Installation records generated during construction phase
- Leak detection test records generated during commissioning
- All records subject to project QA/QC procedures

## Construction

**Record package contents (from decomposition):**

| Record Category | Equipment/System | Test Scope |
|-----------------|-----------------|------------|
| FAT records | Loading arm, ERC, leak detection | OEM functional tests, calibration, certification |
| Installation records | All PKG-11 equipment | Mechanical completion, alignment, as-installed verification |
| Leak detection test records | Annulus, drip trays, sumps | Functional tests, alarm/ESD verification |

**Detailed record types:**

### FAT Records

| Record | Equipment | Content |
|--------|-----------|---------|
| Loading arm FAT report | Marine loading arm | Functional test, envelope verification, ERC activation test |
| ERC FAT record | Emergency release coupling | Release force test, valve closure test, reset verification |
| Leak detection FAT | Leak detection sensors | Calibration, response time, alarm output verification |
| Sump pump FAT | Sump pump | Performance curve verification, motor test |

### Installation Records

| Record | Equipment/Scope | Content |
|--------|-----------------|---------|
| Mechanical completion checklist | Loading arm installation | Alignment, foundation bolting, connection torques |
| Pipe installation checklist | Double-walled pipe | Support installation, expansion provisions, weld inspection |
| Instrument installation checklist | Leak detection devices | Mounting, wiring, tag verification |
| As-installed verification | All equipment | Comparison to IFC drawings |

### Commissioning / Functional Test Records

| Record | System | Content |
|--------|--------|---------|
| Loading arm functional test | Loading arm | Slew/luff operation, position feedback, controls |
| ERC functional test | ERC | Manual activation, auto-release simulation |
| Leak detection loop test | Leak detection | Simulated leak response, alarm verification, ESD trip |
| Sump pump functional test | Sump pump | Level control, run/stop, discharge verification |
| ESD integration test | ESD interface | Trip signals, interlock verification |

## Interfaces (Coordination Items)

Dependencies are coordinated externally (NOT_TRACKED). Records shall capture interface verification:

| Interface | Adjacent Package/Deliverable | Record Type |
|-----------|------------------------------|-------------|
| Electrical energization | PKG-20 | Installation / pre-energization check |
| I&C loop checks | PKG-19 | Leak detection loop test |
| ESD integration | PKG-29 | ESD integration test |
| Drainage completion | PKG-03 | Installation checklist |
| Marine structure readiness | PKG-08 | Installation checklist |

## Cross-Document Links

| Document | Link Point |
|----------|------------|
| Datasheet.md (this file) | Record attributes and content structure |
| Specification.md (DEL-11.05) | Record package requirements and acceptance criteria |
| Guidance.md (DEL-11.05) | Engineering rationale for records development |
| Procedure.md (DEL-11.05) | Record collection workflow and verification |
| DEL-11.01 Drawing Set | As-installed verification reference |
| DEL-11.02 Technical Specification | Acceptance criteria source (§9 FAB requirements) |
| DEL-11.04 Data Sheet Package | Tag/duty reference for equipment records |
| DEL-11.06 OEM Qualification | FAT procedures and OEM documentation |

## Deliverable Acceptance (Minimum)

| Acceptance Criterion | Verification Method | Reference |
|---------------------|---------------------|-----------|
| Records index provided with IDs, dates, status | Document review | Specification.md §Requirements |
| Each record includes equipment tag and procedure reference | Completeness check | Specification.md §Requirements |
| Acceptance criteria referenced for each test | Traceability check | Specification.md §Requirements |
| Required signatures and witnesses obtained | Signature check | Specification.md §Quality |
| Calibration certificates included where required | Document review | Specification.md §Quality |
| NCRs/deficiencies documented and dispositioned | NCR review | Specification.md §Quality |

## References

- `_REFERENCES.md` — applicable reference document list
- `0_References/` — package reference materials
- Decomposition: `test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md` (PKG-11 / DEL-11.05)
- Employer's Requirements: **TBD** (clause references pending extraction)
- Applicable standards: **TBD** (confirm per ER and project code register)
- `_DEPENDENCIES.md` — NOT_TRACKED (dependencies coordinated externally)

---

**Pass 3 Enrichment Notes (Final Quality Check):**
- Verified cross-document consistency: 3 record categories (FAT, installation, commissioning) aligned across Datasheet §Construction, Specification requirements, Procedure §Steps 3-5
- Verified record types: FAT (4 records), Installation (4 records), Commissioning (5 records) = 13 record types total
- Verified objectives mapping (OBJ-1, OBJ-2, OBJ-4, OBJ-7) consistent with Guidance.md §Purpose
- Verified Interfaces table (5 interfaces) traces to Specification §Interface Requirements (INT-001 to INT-004)
- Verified Cross-Document Links (8 links) include all PKG-11 deliverables with correct relationships
- Verified Deliverable Acceptance (6 criteria) aligns with Specification §Verification (6 criteria) and Procedure §Verification checklist (6 items)
- Confirmed record generation context: FAT (OEM), Installation (construction), Commissioning (testing) phases correctly described
- Confirmed terminology consistency: FAT, MC (mechanical completion), loop test, ESD integration consistent with DEL-11.02 §9
- All TBDs and ASSUMPTIONs retained with proper labeling
- Pass 3 complete — document ready for WORKING_ITEMS session
