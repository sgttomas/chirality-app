# Procedure: DEL-32.02 Permits

## Purpose

This procedure defines the process for **receiving, reviewing, recording, and managing issued Permits** within **PKG-32 Regulatory & Permits**.

**Deliverable purpose:** Defines and substantiates permits in accordance with ER requirements. (Source: _CONTEXT.md; Decomposition Section 5; Datasheet.md)

**Deliverable type:** Permit (issued regulatory documents)
**Responsible party:** D&B Contractor

**Procedure scope:** This procedure covers:
1. Receiving issued permits from regulatory authorities
2. Reviewing permit content and conditions
3. Recording permits in permit register
4. Distributing permits to project team
5. Initiating permit condition compliance tracking

## Prerequisites

### Dependencies

**Dependency tracking mode:** NOT_TRACKED (Source: _DEPENDENCIES.md)

**Upstream deliverables:**
- **DEL-32.01 (Permit Applications)** — permit applications result in issued permits (Source: Specification.md IR-01; Datasheet.md References)
- Application review and authority approval process (external to Contractor)

### Reference Materials

- **Permit register** (initiated in DEL-32.01) — to be updated with issued permit details
- **Employer's Requirements** Volume 2 Parts 1–3 — **location TBD**
- **Project Quality Management Plan** — **TBD**
- **Permit distribution list** — **TBD** (defines who receives copies of each permit type)

### Personnel Requirements

- **Permit Coordinator** (or Project Delivery Lead) — responsible for permit receipt, review, recording, distribution, and compliance tracking initiation — **TBD**: Define qualifications
- **QA/QC Manager** — responsible for permit condition compliance tracking oversight — **TBD**: Define qualifications
- **Discipline Leads** — responsible for technical review of permit content and discipline-specific compliance — **TBD**: Define qualifications

## Steps

### Step 1: Monitor for Permit Issuance

**Objective:** Track permit application status and anticipate permit issuance.

**Activities:**

1.1. **Monitor Application Status** — Track status of pending permit applications in permit register (initiated in DEL-32.01).
1.2. **Follow Up with Authorities** — If permit issuance is delayed or approaching anticipated approval date, contact authority to confirm status.
1.3. **Receive Issuance Notification** — Authority notifies Contractor of permit issuance (via email, phone, or mail).

**Output:** Awareness of pending permit issuance

---

### Step 2: Receive and Review Issued Permit

**Objective:** Receive issued permit from authority and conduct initial review.

(Implements Specification.md FR-01, FR-02, FR-03)

**Activities:**

**2.1. Receive Permit and Confirm Receipt**

- Receive issued permit from authority (electronic or hard copy)
- Confirm receipt with authority (reply to email, sign delivery receipt, etc.)
- **Implements:** Specification.md FR-01

**2.2. Review Permit Content and Conditions**

Conduct initial review of issued permit:

- **Accuracy check:** Verify project information (name, location, applicant, owner) matches application
- **Completeness check:** Verify all applied-for approvals are included in permit
- **Condition identification:** Identify and extract all permit conditions
- **Condition classification:** Classify conditions by type (see Guidance.md Section "Considerations — Permit Condition Types"):
  - Pre-construction conditions (must be satisfied before work starts)
  - During-construction conditions (ongoing compliance during construction)
  - Post-construction conditions (required after construction completion)
  - Operational conditions (ongoing compliance during facility operation)
- **Implements:** Specification.md FR-02, FR-03
- **Rationale:** See Guidance.md Section "Principles" #2 — permit conditions are legally binding and must be identified and tracked

**2.3. Log Permit Receipt in Correspondence Register**

- Log permit receipt in DEL-32.07 (Authority & Stakeholder Correspondence Register)
- Include: authority name, permit number, issue date, conditions summary
- **Implements:** Specification.md IR-02

**Outputs:**
- Issued permit received
- Initial permit review complete (accuracy, completeness, conditions identified and classified)
- Permit receipt logged in DEL-32.07

**Verification:** Accuracy and completeness verified; all conditions identified (see Specification.md Verification table)

---

### Step 3: Record and Distribute Issued Permit

**Objective:** Record permit in permit register, file in project records, and distribute to project team.

(Implements Specification.md FR-04, FR-05, QR-01)

**Activities:**

**3.1. Update Permit Register**

Update permit register (initiated in DEL-32.01) with issued permit details:
- Permit number
- Issue date
- Issuing authority
- Expiry date (if applicable)
- Permit conditions summary
- Compliance tracking status (to be updated in Step 4)
- **Implements:** Specification.md FR-04

**3.2. Log in Correspondence Register**

- Ensure permit issuance is logged in DEL-32.07 (completed in Step 2.3; verify entry complete)
- **Implements:** Specification.md IR-02

**3.3. Distribute Permit to Project Team**

Distribute permit to distribution list (see Guidance.md Section "Considerations — Distribution and Communication"):
- Project Manager
- Discipline Leads (relevant to permit scope)
- Construction Manager
- QA/QC Manager
- HSE Manager (if health, safety, or environmental conditions)
- Other stakeholders per project communication plan
- **Implements:** Specification.md FR-05

**3.4. File Permit in Project Records**

- File copy of issued permit in DEL-32.08 (Authority & Stakeholder Correspondence Copies)
- File in project document management system per project document control procedures
- **Implements:** Specification.md QR-01, IR-02

**Outputs:**
- Permit register updated
- Correspondence register updated
- Permit distributed to project team
- Permit filed in project records (DEL-32.08)

**Verification:** Permit register and correspondence register updated; distribution complete; permit filed (see Specification.md Verification table)

---

### Step 4: Initiate Permit Condition Compliance Tracking

**Objective:** Assign permit conditions to compliance tracking deliverables and initiate compliance tracking.

(Implements Specification.md FR-06, IR-03)

**Activities:**

**4.1. Assign Conditions to Compliance Deliverables**

Assign each permit condition to the appropriate compliance records deliverable (see Guidance.md Section "Considerations — Relationship to Compliance Records"):

| Compliance Deliverable | Conditions Assigned |
|------------------------|---------------------|
| **DEL-32.03 (VFPA PER Compliance)** | VFPA Project and Environmental Review approval conditions |
| **DEL-32.04 (DFO Compliance)** | DFO Fisheries Act authorization conditions |
| **DEL-32.05 (Transport Canada Compliance)** | Transport Canada approval conditions |
| **DEL-32.06 (Code Compliance)** | Building permits, fire permits, environmental permits, other code compliance conditions |

**4.2. Initiate Compliance Tracking**

For each permit condition:
- Create compliance tracking entry in applicable compliance deliverable (DEL-32.03-32.06)
- Identify responsible party for compliance demonstration
- Identify compliance verification method (inspection, test, documentation submittal, etc.)
- Establish compliance schedule (when condition must be satisfied)
- **Implements:** Specification.md FR-06, IR-03
- **Rationale:** See Guidance.md Section "Principles" #2 — permit conditions are legally binding; compliance must be demonstrated

**4.3. Communicate Pre-Construction Conditions**

If permit includes pre-construction conditions (conditions that must be satisfied before construction starts):
- Highlight pre-construction conditions to Project Manager and Construction Manager
- Ensure pre-construction conditions are satisfied before construction commencement
- See Guidance.md Section "Considerations — Permit Condition Types" — pre-construction conditions

**Outputs:**
- All permit conditions assigned to compliance deliverables (DEL-32.03-32.06)
- Compliance tracking initiated for each condition
- Pre-construction conditions communicated to project team

**Verification:** All conditions assigned; compliance tracking entries created; responsible parties identified (see Specification.md Verification table; Specification.md PR-02 — 100% of conditions tracked)

---

## Verification

**Overall verification activities:**

(See Specification.md Section "Verification"; see Guidance.md for rationale)

| Verification Activity | Acceptance Criteria | Responsible Party | Specification Ref | Step Ref |
|-----------------------|---------------------|-------------------|-------------------|----------|
| Permit receipt confirmed | Receipt confirmation obtained | Permit Coordinator | FR-01 | Step 2.1 |
| Permit accuracy verified | Permit content matches application; no discrepancies | Permit Coordinator / Reviewer | FR-02 | Step 2.2 |
| Permit conditions identified | All conditions identified and classified by type | Permit Coordinator / QA/QC Manager | FR-03 | Step 2.2 |
| Permit recorded | Permit register updated with issued permit details | Permit Coordinator | FR-04 | Step 3.1 |
| Permit distributed | Distribution complete; recipients confirmed | Permit Coordinator | FR-05 | Step 3.3 |
| Compliance tracking initiated | All conditions assigned to DEL-32.03-32.06 | QA/QC Manager | FR-06, IR-03 | Step 4 |

**Sign-off requirements:** **TBD** — per project quality procedures

## Records

**Documentation outputs:**

**Primary outputs:**
- **Building permits, construction permits, environmental permits** (Source: Decomposition Section 5; Datasheet.md Construction) — issued regulatory authority permits

**Related outputs:**
- **Updated permit register** — tracking of issued permits (extension of DEL-32.01 permit register) (Step 3.1; Specification.md FR-04)
- **Correspondence register entries** — logged in DEL-32.07 (Steps 2.3, 3.2; Specification.md IR-02)
- **Permit copies filed** — filed in DEL-32.08 (Step 3.4; Specification.md IR-02)
- **Compliance tracking entries** — created in DEL-32.03-32.06 (Step 4; Specification.md IR-03)

**Record management:**
- **Storage location:** Issued permits filed in DEL-32.08 (Correspondence Copies); tracked in permit register; logged in DEL-32.07 (Correspondence Register)
- **Document control:** Per project document control procedures — **TBD**
- **Retention requirements:** **TBD** — per contract and regulatory requirements (typically project duration + post-construction period + X years)

**Relationship to other deliverables:**
- **DEL-32.01 (Permit Applications)** → **DEL-32.02 (Permits)** — applications result in issued permits (Specification.md IR-01; Step 2)
- **DEL-32.02 (Permits)** → **DEL-32.03-32.06 (Compliance Records)** — permit conditions tracked and demonstrated (Specification.md IR-03; Step 4)
- **DEL-32.02 (Permits)** → tracked in **DEL-32.07 (Correspondence Register)** — permit receipt logged (Specification.md IR-02; Steps 2.3, 3.2)
- **DEL-32.02 (Permits)** → filed in **DEL-32.08 (Correspondence Copies)** — permit copies filed (Specification.md IR-02; Step 3.4)
