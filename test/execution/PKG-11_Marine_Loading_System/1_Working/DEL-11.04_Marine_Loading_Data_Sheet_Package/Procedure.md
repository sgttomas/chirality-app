# Procedure: DEL-11.04 Marine Loading Data Sheet Package

## Purpose

This procedure defines the process for producing and verifying **Marine Loading Data Sheet Package** within **PKG-11 Marine Loading System**.

**Deliverable purpose:** Defines and substantiates marine loading equipment in accordance with Employer's Requirements (ER), providing the procurement basis and technical evaluation criteria for equipment selection and vendor qualification.

**Deliverable type:** Data Sheet
**Responsible party:** D&B Contractor
**Discipline:** Process

## Prerequisites

### Dependencies
- See `_DEPENDENCIES.md` — **NOT_TRACKED**: Dependencies are coordinated externally by humans (see `execution/_Coordination/_COORDINATION.md`)
- Upstream deliverables and input data to be confirmed prior to commencement

### Required Inputs

| Input | Source | Status |
|-------|--------|--------|
| Design requirements | DEL-11.02 Technical Specification | **TBD** |
| Calculated duty points | DEL-11.03 Design Calculations | **TBD** |
| Tag numbers and locations | DEL-11.01 Drawing Set | **TBD** |
| OEM data (loading arm) | DEL-11.06 OEM Qualification | **TBD** |
| Hazardous area classification | PKG-27 | **TBD** |
| Electrical interface requirements | PKG-20 | **TBD** |
| I&C interface requirements | PKG-19 | **TBD** |
| ESD interface requirements | PKG-29 | **TBD** |
| Project datasheet templates | Project standards | **TBD** |

### Reference Materials
- `_REFERENCES.md` — applicable reference document list
- `0_References/` — package reference materials
- Employer's Requirements — **TBD** (specific clause references)
- Applicable codes and standards — **TBD** (confirm per ER and project code register)

### Personnel Requirements
- Qualified Process discipline engineer (datasheet originator)
- Qualified checker (independent of originator)
- Discipline lead / approver
- **ASSUMPTION:** Personnel competency per project quality procedures

## Steps

### Step 1: Define Templates and Register

**Action:** Confirm datasheet templates and create datasheet register.

| Task | Output |
|------|--------|
| Obtain project datasheet templates | Template set |
| Confirm required datasheets per decomposition | Datasheet list |
| Assign tag numbers per project convention | Tag assignments |
| Create datasheet register (tag, title, revision, status) | Datasheet register (draft) |

**Required datasheets (from decomposition):**

| Tag | Title | Equipment |
|-----|-------|-----------|
| **TBD** | Marine Loading Arm Data Sheet | Powered loading arm with ERC |
| **TBD** | Leak Detection System Data Sheet | Annulus/drip tray/sump detection |
| **TBD** | Sump Pump Data Sheet | Containment sump pump |

### Step 2: Populate Design Basis Fields

**Action:** Enter design conditions and requirements from controlled sources.

| Task | Source | Output |
|------|--------|--------|
| Extract design conditions | DEL-11.02 §3 | Design conditions block |
| Extract loading arm requirements | DEL-11.02 §4 | Loading arm design fields |
| Extract leak detection requirements | DEL-11.02 §6 | Leak detection design fields |
| Extract sump pump duty point | DEL-11.03 drainage calc | Sump pump design fields |
| Mark unavailable values as TBD | — | TBD list |

**Hold point:** Confirm design basis values before proceeding to vendor coordination.

### Step 3: Populate Loading Arm Datasheet

**Action:** Complete loading arm datasheet fields.

| Field Category | Source | Status |
|----------------|--------|--------|
| Identification | DEL-11.01, project tagging | **TBD** |
| Design conditions | DEL-11.02 §3 | **TBD** |
| Mechanical (reach, envelope) | DEL-11.03, DEL-11.06 | **TBD** |
| ERC data | DEL-11.02 §4.6, DEL-11.06 | **TBD** |
| Materials | DEL-11.02 §4.4, DEL-11.06 | **TBD** |
| Connections | DEL-11.02 §4.3, DEL-11.06 | **TBD** |
| Controls/I&C | DEL-11.02 §4.7, PKG-19/20 | **TBD** |
| Hazardous area | PKG-27 | **TBD** |
| Vendor data | DEL-11.06 | **TBD** |

### Step 4: Populate Leak Detection Datasheet

**Action:** Complete leak detection system datasheet fields.

| Field Category | Source | Status |
|----------------|--------|--------|
| Identification | DEL-11.01, project tagging | **TBD** |
| Detection philosophy | DEL-11.02 §6.1 | **TBD** |
| Sensor type | DEL-11.02 §6.1, vendor data | **TBD** |
| Zones/coverage | DEL-11.02 §6.2, DEL-11.01 | **TBD** |
| Alarm outputs | DEL-11.02 §6.3 | **TBD** |
| I&C interfaces | PKG-19, PKG-29 | **TBD** |
| Power | PKG-20 | **TBD** |
| Hazardous area | PKG-27 | **TBD** |
| Testing | DEL-11.02 §6.4 | **TBD** |
| Vendor data | Vendor submissions | **TBD** |

### Step 5: Populate Sump Pump Datasheet

**Action:** Complete sump pump datasheet fields.

| Field Category | Source | Status |
|----------------|--------|--------|
| Identification | DEL-11.01, project tagging | **TBD** |
| Design duty | DEL-11.03 drainage calc | **TBD** |
| Operating range | DEL-11.03, vendor curve | **TBD** |
| Construction | DEL-11.02, product compatibility | **TBD** |
| Motor | PKG-20, hazardous area | **TBD** |
| Connections | DEL-11.01, pipe specs | **TBD** |
| Controls | PKG-19, level control | **TBD** |
| Testing | DEL-11.02 §9 | **TBD** |
| Vendor data | Vendor submissions | **TBD** |

### Step 6: Vendor Coordination

**Action:** Request and incorporate vendor data.

| Task | Responsibility | Output |
|------|----------------|--------|
| Issue RFQ/enquiry with preliminary datasheets | Procurement | Enquiry package |
| Receive vendor technical data | Vendor | Vendor data package |
| Review vendor data for compliance | Engineer | Technical evaluation |
| Populate vendor-offered fields | Engineer | Updated datasheets |
| Document vendor data revision/date | Engineer | Revision references |

### Step 7: Consistency Checks

**Action:** Cross-check datasheets against related deliverables.

| Check | Comparison | Record |
|-------|------------|--------|
| Design basis vs. DEL-11.02 | Datasheet values ↔ Specification requirements | Consistency check form |
| Duty points vs. DEL-11.03 | Datasheet values ↔ Calculation outputs | Consistency check form |
| Tags vs. DEL-11.01 | Datasheet tags ↔ Drawing tag list | Cross-reference check |
| Interfaces vs. adjacent packages | Datasheet interfaces ↔ PKG-19/20/29 | Interface check form |

### Step 8: Review and Approval

**Action:** Conduct review and obtain approval.

| Task | Responsibility | Record |
|------|----------------|--------|
| Self-check (units, terminology, completeness) | Originator | Self-check form |
| Independent review | Checker | Review comments |
| Comment resolution | Originator | Comment response |
| Discipline approval | Lead engineer | Approval signature |
| Document control registration | Document controller | Transmittal |

## Verification

**Verification activities (traceability to Specification.md):**

| Verification Method | Requirements Verified | Record |
|---------------------|----------------------|--------|
| Completeness check | DS-001 to DS-006 | Completeness form |
| Consistency check | DS-007, MLA-DS, LDS-DS, SP-DS | Consistency form |
| Cross-reference check | Tags vs. DEL-11.01 | Cross-reference log |
| Vendor data review | Vendor-supplied fields | Technical evaluation |
| Interface check | INT-001 to INT-004 | Interface check form |
| Units/terminology check | QA-002 to QA-004 | Standards check form |

**Acceptance checklist (aligns to Datasheet.md and Specification.md):**

| Criterion | Check | Status |
|-----------|-------|--------|
| Datasheet register provided with tags and revisions | Document review | ☐ |
| Each datasheet includes required fields or marked TBD | Completeness check | ☐ |
| Design basis values consistent with DEL-11.02/11.03 | Consistency check | ☐ |
| Vendor data referenced with revision/date | Traceability check | ☐ |
| Tags consistent with DEL-11.01 drawings | Cross-reference check | ☐ |
| Units and nomenclature per project standards | Standards check | ☐ |
| Independent review completed | Review records | ☐ |

**Sign-off requirements:**

| Role | Responsibility | Signature Block |
|------|----------------|-----------------|
| Originator | Technical content | **TBD** |
| Checker | Independent review | **TBD** |
| Approver | Discipline approval | **TBD** |

**ASSUMPTION:** Sign-off protocol per project quality procedures.

## Records

**Documentation outputs:**
- Marine loading arm data sheet
- Leak detection system data sheet
- Sump pump data sheet
- Datasheet register/index

**Record management:**

| Record | Location | Retention |
|--------|----------|-----------|
| Draft datasheets (working) | `1_Working/` | Until superseded |
| Review packages | `2_Checking/To/` | Per project procedures |
| Issued datasheets | `3_Issued/` | Project archive (**TBD**) |
| Vendor data packages | Document control system | Project archive (**TBD**) |
| Review/check records | Document control system | Project archive (**TBD**) |

**ASSUMPTION:** Electronic records in project document management system.
