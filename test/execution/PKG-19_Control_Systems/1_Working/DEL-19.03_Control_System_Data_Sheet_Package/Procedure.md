# Procedure: DEL-19.03 Control System Data Sheet Package

## Purpose

This procedure defines the process for reviewing and approving **Control System Data Sheet Package** within **PKG-19 Control Systems**.

**Deliverable purpose:** Defines and substantiates control system in accordance with ER requirements.

**Source:** `_CONTEXT.md`

**Deliverable type:** Data Sheet (Vendor Submittal Package)
**Responsible party:** D&B Contractor (review); Vendor (submittal)
**Discipline:** I&C

This procedure guides the I&C team through the vendor data sheet review and approval process, ensuring equipment compliance with DEL-19.02 (Control System Technical Specification) before procurement and fabrication.

## Prerequisites

### Dependencies

**Dependency tracking mode:** NOT_TRACKED — Dependencies are coordinated externally by humans (see `execution/_Coordination/_COORDINATION.md` and `_DEPENDENCIES.md`)

**Upstream deliverables** (required before data sheet review):
- **DEL-19.02:** Control System Technical Specification (approved) — compliance basis for review
- **Vendor Selection:** Control system vendor selected and contract awarded
- **Submittal Schedule:** Project submittal schedule established with vendor

**Source:** Typical submittal review workflow dependencies

### Reference Materials

**Required reference documents:**
- DEL-19.02 (Control System Technical Specification) — approved version
- DEL-19.01 (Control System Design Drawing Set) — for equipment arrangement context
- Vendor contract and scope of work
- Project submittal procedures — **TBD**
- Applicable codes and standards (IEC 61131-3, ISA 84, CSA C22.1, API 554, ISA/IEC 62443)

**Available reference materials:** See `_REFERENCES.md` and `0_References/` in package directory

### Personnel Requirements

**Qualified personnel:**
- **Reviewer:** I&C engineer with control system equipment review experience — **ASSUMPTION**: Per project staffing plan
- **Interdisciplinary Reviewers:** Electrical engineer (PKG-17), instrumentation engineer (PKG-20), safety engineer (PKG-23) as applicable
- **Approver:** I&C discipline lead or authorized representative — **TBD**

**Competency requirements:**
- Familiarity with DCS/PLC, HMI, and historian technologies
- Understanding of DEL-19.02 specification requirements
- Ability to evaluate vendor data sheets for compliance
- Knowledge of applicable codes and standards

**Source:** **ASSUMPTION**: Standard reviewer competency requirements; specific qualifications TBD per project quality procedures

### Tools and Resources

- DEL-19.02 specification (reference document)
- Compliance matrix template — **TBD** — **ASSUMPTION**: Excel or equivalent
- Submittal review comment form/template — **TBD**
- Access to project document management system — **TBD**

## Steps

### Step 1: Receive and Log Vendor Submittal

**Objective:** Log vendor submittal and distribute to reviewers

**Activities:**
1. Vendor submits data sheet package per submittal schedule
2. Document control receives submittal and logs:
   - Submittal number
   - Submittal description (DEL-19.03 Control System Data Sheets)
   - Date received
   - Vendor name and contact
3. Document control distributes submittal to I&C reviewer (primary) and interdisciplinary reviewers (as applicable)
4. Document control sets review due date per project procedures — **TBD** — **ASSUMPTION**: 10-15 business days

**Outputs:**
- Submittal log entry
- Submittal distributed to reviewers

**Verification:** Submittal logged and distributed

**Source:** Standard document control submittal logging procedure

### Step 2: Preliminary Completeness Check

**Objective:** Verify submittal is complete before detailed technical review

**Activities:**
1. Reviewer performs quick completeness check:
   - All required data sheets present (DCS/PLC, HMI, historian, network equipment)?
   - Compliance matrix included?
   - Certifications included (or noted as "to follow")?
   - Data sheets legible and in English?
2. If incomplete, return to vendor with "Revise and Resubmit" status and list of missing items
3. If complete, proceed to Step 3

**Outputs:**
- Completeness check result (complete / incomplete)
- If incomplete: Review comment requesting missing items

**Verification:** Submittal completeness confirmed

**Source:** Standard submittal completeness check practice

### Step 3: Technical Review Against DEL-19.02 Specification

**Objective:** Perform detailed technical review for compliance with DEL-19.02

**Activities:**
1. Reviewer reads vendor compliance matrix to understand vendor's compliance claims
2. Reviewer verifies compliance matrix accuracy by cross-referencing data sheets:
   - Verify each DEL-19.02 requirement listed in matrix
   - Verify data sheet references are accurate (correct page numbers, sections)
   - Verify compliance status is correct (do not trust vendor's "complies" without verification)
3. Reviewer performs detailed technical review per Specification.md criteria (RAC-01 through RAC-05):

   **RAC-01: Functional and Performance Compliance**
   - Review against FR-01 through FR-08 (functional requirements in DEL-19.02)
   - Review against PR-01 through PR-04 (performance requirements in DEL-19.02)
   - Check critical parameters: scan time, I/O capacity, network bandwidth, alarm response time, data retention, etc.

   **RAC-02: Interface Compatibility**
   - Review against IR-01 through IR-05 (interface requirements in DEL-19.02)
   - Verify I/O compatibility with field instrumentation (PKG-20)
   - Verify power compatibility with electrical distribution (PKG-17)
   - Verify safety interface compatibility (PKG-23)
   - Verify communication protocol compatibility

   **RAC-03: Materials and Environmental Compliance**
   - Review against MR-01 through MR-05 (materials/workmanship requirements in DEL-19.02)
   - Verify environmental ratings (temperature, humidity, vibration, EMI)
   - Verify hazardous area ratings (if applicable per PKG-30)
   - Verify equipment quality (new, current manufacture, established manufacturer)

   **RAC-04: Standards and Codes Compliance**
   - Verify certifications (UL, CSA, CE, ATEX/IECEx)
   - Verify compliance with IEC 61131-3 (programming languages)
   - Verify compliance with ISA/IEC 62443 (cybersecurity, if specified)
   - Verify compliance with other applicable standards

   **RAC-05: Lifecycle Support**
   - Review warranty provisions
   - Review software support commitments
   - Review spare parts availability commitments

4. Identify deviations, deficiencies, or missing information
5. Prepare review comments with status for each issue:
   - **Approve:** Equipment fully complies, no issues
   - **Approve as Noted:** Equipment complies with minor notes/clarifications required
   - **Revise and Resubmit:** Equipment does not comply or significant issues require vendor action

**Outputs:**
- Technical review notes
- Review comment draft

**Verification:** All DEL-19.02 requirements reviewed

**Source:** Specification.md review criteria (RAC-01 through RAC-05)

### Step 4: Interdisciplinary Check (if required)

**Objective:** Coordinate with interfacing disciplines to verify compatibility

**Activities:**
1. Distribute data sheets to interdisciplinary reviewers:
   - **Electrical (PKG-17):** Review power requirements, UPS compatibility, grounding
   - **Field Instrumentation (PKG-20):** Review I/O compatibility, communication protocols, signal types
   - **Safety Systems (PKG-23):** Review safety interface compatibility, SIS separation (if applicable)
2. Receive and consolidate interdisciplinary review comments
3. Incorporate interdisciplinary comments into overall review comment package

**Outputs:**
- Interdisciplinary review comments (from PKG-17, PKG-20, PKG-23)
- Consolidated review comments

**Verification:** Interdisciplinary reviewers sign-off or provide comments

**Source:** Standard interdisciplinary check (IDC) practice

### Step 5: Employer Review (if required)

**Objective:** Obtain Employer review and comments (if contractually required)

**Activities:**
1. Prepare Employer review package:
   - Vendor data sheets
   - Contractor preliminary review comments (if sharing with Employer)
   - Compliance matrix
2. Submit to Employer per contract requirements
3. Receive Employer review comments
4. Consolidate Employer comments with Contractor comments

**Outputs:**
- Employer review comments (if applicable)
- Consolidated review comments (Contractor + Employer)

**Verification:** Employer review complete (if required)

**Source:** **ASSUMPTION**: Typical D&B contract Employer review process; specific requirements TBD per contract

### Step 6: Finalize Review Comments and Issue to Vendor

**Objective:** Finalize and issue consolidated review comments to vendor

**Activities:**
1. Consolidate all review comments (technical, interdisciplinary, Employer)
2. Assign overall submittal status:
   - **Approved:** No issues, vendor authorized to proceed
   - **Approved as Noted:** Minor notes, vendor authorized to proceed with noted clarifications/confirmations
   - **Revise and Resubmit:** Significant issues, vendor must address and resubmit
3. I&C discipline lead reviews and approves review comments (before issuing to vendor)
4. Document control issues review comments to vendor
5. Request resubmittal if status is "Revise and Resubmit" with vendor response due date

**Outputs:**
- Finalized review comments
- Submittal status (Approved / Approved as Noted / Revise and Resubmit)
- Review comments issued to vendor

**Verification:** I&C discipline lead approval of review comments; document control issuance

**Source:** Standard submittal review comment issuance procedure

### Step 7: Review Resubmittal (if applicable)

**Objective:** Review vendor resubmittal to verify comments addressed

**Activities:**
1. Receive vendor resubmittal (if "Revise and Resubmit" status was issued)
2. Verify vendor addressed all review comments:
   - Check vendor's response to each comment
   - Verify revised data sheets (if equipment changed)
   - Verify additional information provided (if missing information)
3. If all comments addressed satisfactorily: Approve
4. If comments not adequately addressed: Issue additional review comments or request clarification
5. Iterate until acceptable

**Outputs:**
- Resubmittal review notes
- Final approval or additional review comments

**Verification:** All comments adequately addressed

**Source:** Standard resubmittal review process

### Step 8: Final Approval and Authorization to Proceed

**Objective:** Issue final approval for procurement and fabrication

**Activities:**
1. I&C discipline lead issues final approval:
   - Approve data sheet package
   - Authorize vendor to proceed with equipment procurement and fabrication
2. Document control logs approval and issues to vendor and project team
3. Update submittal log with final approval status and date

**Outputs:**
- Final approval letter/transmittal to vendor
- Submittal log updated (status: Approved; date: YYYY-MM-DD)

**Verification:** Final approval issued and logged

**Source:** Standard approval and authorization process

### Step 9: Records Management and Filing

**Objective:** File approved data sheets and maintain records

**Activities:**
1. File approved data sheets in `3_Issued/` folder (copy of vendor submittal with approval)
2. Upload approved data sheets to project document management system
3. File review comment records (all iterations)
4. Update `_STATUS.md` to reflect completion (when appropriate per lifecycle: INITIALIZED → IN_PROGRESS during review, → CHECKING when under review, → ISSUED when approved)
5. Retain records per project retention schedule — **TBD**

**Outputs:**
- Approved data sheets filed in `3_Issued/`
- Review records filed
- Document management system updated
- `_STATUS.md` updated (when appropriate)

**Verification:** Records filed and document management system updated

**Source:** Standard records management practice

## Verification

### Verification Activities Summary

| Step | Verification Activity | Verifier |
|------|----------------------|----------|
| 1 | Submittal logged and distributed | Document control |
| 2 | Completeness check | I&C reviewer |
| 3 | Technical review against DEL-19.02 | I&C reviewer |
| 4 | Interdisciplinary check | PKG-17, PKG-20, PKG-23 reviewers |
| 5 | Employer review (if required) | Employer |
| 6 | Review comments finalization | I&C discipline lead |
| 7 | Resubmittal review (if applicable) | I&C reviewer |
| 8 | Final approval | I&C discipline lead |
| 9 | Records filing | Document control |

**Source:** Specification.md verification methods

### Acceptance Criteria (from Specification.md)

See `Specification.md` Verification section for full acceptance criteria (AC-01, AC-02, AC-03). Summary below:

**AC-01 — Submittal Completeness:**
- All required data sheets submitted (DCS/PLC, HMI, historian)
- Compliance matrix complete
- All certifications provided

**AC-02 — Technical Adequacy:**
- Equipment meets or exceeds all DEL-19.02 requirements
- No unacceptable deviations

**AC-03 — Approval for Procurement:**
- I&C discipline lead approval issued
- Employer approval issued (if required)

### Review Turnaround Targets

- Contractor review: **TBD** — **ASSUMPTION**: 10-15 business days from receipt to comment issuance
- Employer review (if required): **TBD** per contract
- Vendor resubmittal: **TBD** — **ASSUMPTION**: 5-10 business days

**Source:** **ASSUMPTION**: Typical review schedule; specific targets TBD per project procedures

## Records

### Documentation Outputs (from Specification.md and `_CONTEXT.md`)

**Primary deliverable artifacts:**
1. Approved DCS/PLC data sheets
2. Approved HMI data sheets
3. Approved historian data sheets (server data sheets)
4. Approved network equipment data sheets

**Supporting records:**
- Submittal log
- Compliance matrix (vendor-prepared, reviewed)
- Review comment records (all iterations)
- Interdisciplinary review comments
- Employer review comments (if applicable)
- Approval records (I&C discipline lead, Employer)

### Record Management

**Filing locations:**
- Working files: `1_Working/DEL-19.03_Control_System_Data_Sheet_Package/`
- Checking copies: `2_Checking/To/` (during review phase) → `2_Checking/From/` (returned with comments to vendor)
- Issued copies: `3_Issued/` (final approved data sheets with approval date/rev in filename)

**Document management system:**
- All approved data sheets uploaded to project DMS — **TBD** — DMS path and conventions
- Revision control per project procedures — **TBD**

**Retention requirements:**
- Retention per project records retention schedule — **TBD**
- **ASSUMPTION**: Electronic records retained for life of facility plus regulatory retention period

**Source:** Typical engineering records management practice; specific requirements TBD per project procedures

### Lifecycle State Management

**`_STATUS.md` transitions** (when appropriate per project lifecycle):
- `OPEN` → `INITIALIZED` (initial drafts generated)
- `INITIALIZED` → `IN_PROGRESS` (vendor submittals received, review underway)
- `IN_PROGRESS` → `CHECKING` (under formal review)
- `CHECKING` → `IN_PROGRESS` (if resubmittal required) or → `ISSUED` (if approved)
- `ISSUED` (final state for this phase)

**Note:** Status transitions are human-managed decisions; this procedure describes when transitions are typical, but does not automatically change status.

**Source:** Framework lifecycle model per `AGENTS.md`
