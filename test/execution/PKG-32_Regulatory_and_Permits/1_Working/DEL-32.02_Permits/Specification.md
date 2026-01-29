# Specification: DEL-32.02 Permits

## Scope

This specification defines the requirements for **Permits** within **PKG-32 Regulatory & Permits**.

**Purpose:** Defines and substantiates permits in accordance with ER requirements. (Source: _CONTEXT.md; Decomposition Section 5)

**Coverage:** Contractor-responsible issued permits only. Employer-responsible permits excluded. (Source: Decomposition Section 1.2; Datasheet.md Conditions)

**Anticipated artifacts:**
- Building permits, construction permits, environmental permits (Source: Decomposition Section 5; Datasheet.md Construction)

**Relationship to project objectives:**
- **OBJ-6: Regulatory Compliance** — "The Works comply with all permits, codes, and authority requirements" (Source: Decomposition Section 6)

**Downstream use:**
- Issued permits include conditions that must be demonstrated through compliance records (DEL-32.03 through DEL-32.06)

## Requirements

### Functional Requirements

**FR-01: Permit Receipt**
- The Contractor shall receive and acknowledge receipt of all issued permits from regulatory authorities
- (See Datasheet.md Attributes — "Issued Permit Documents" entity)
- **Source:** **ASSUMPTION** — standard project management requirement
- **Rationale:** See Guidance.md Section "Principles" #1 — timely permit receipt enables construction commencement
- **Verification:** Procedure.md Step 2 (Receive and Acknowledge Permit)

**FR-02: Permit Review**
- Each issued permit shall be reviewed for:
  - Accuracy (project information, scope, approval dates)
  - Completeness (all applied-for approvals included)
  - Conditions imposed by the authority
- **Source:** **ASSUMPTION** — regulatory compliance and risk management requirement
- **Rationale:** See Guidance.md Section "Principles" #2 — permit conditions must be understood and tracked
- **Verification:** Procedure.md Step 2.2 (Review Permit Content and Conditions)

**FR-03: Permit Condition Identification and Classification**
- Permit conditions shall be identified, extracted, and classified by type:
  - Pre-construction conditions (must be satisfied before work starts)
  - During-construction conditions (ongoing compliance during construction)
  - Post-construction conditions (required after construction completion)
  - Operational conditions (ongoing compliance during facility operation)
- (See Datasheet.md Attributes — "Permit Conditions" entity)
- **Source:** **ASSUMPTION** — compliance tracking requirement
- **Rationale:** See Guidance.md Section "Considerations — Permit Condition Types" — different condition types require different compliance approaches
- **Verification:** Procedure.md Step 2.2 (Review Permit Content and Conditions)

**FR-04: Permit Recording**
- All issued permits shall be recorded in the permit register (extension of DEL-32.01 permit register)
- Recording shall include: permit number, issue date, issuing authority, expiry date (if applicable), permit conditions summary, compliance tracking status
- (See Datasheet.md Attributes — "Permit Register" entity)
- **Source:** **ASSUMPTION** — project management and compliance tracking requirement
- **Rationale:** See Guidance.md Section "Considerations — Coordination with DEL-32.01" — permit register tracks full lifecycle from application to issuance to compliance
- **Verification:** Procedure.md Step 3 (Record Permit in Permit Register)

**FR-05: Permit Distribution**
- Issued permits shall be distributed to relevant project team members:
  - Project Manager
  - Discipline leads (relevant to permit scope)
  - Construction Manager
  - QA/QC Manager (for compliance tracking)
  - Other stakeholders as defined in distribution list
- (See Datasheet.md Attributes — "Permit Distribution List" entity)
- **Source:** **ASSUMPTION** — project communication and compliance requirement
- **Rationale:** See Guidance.md Section "Considerations — Distribution and Communication" — relevant team members must be aware of permits and conditions
- **Verification:** Procedure.md Step 3.3 (Distribute Permit to Project Team)

**FR-06: Compliance Tracking Initiation**
- Upon permit receipt, compliance tracking shall be initiated for all permit conditions
- Compliance tracking shall be documented in the applicable compliance records deliverable (DEL-32.03 through DEL-32.06)
- (See Datasheet.md Attributes — "Permit Condition Compliance Tracking" entity)
- **Source:** **ASSUMPTION** — regulatory compliance requirement
- **Rationale:** See Guidance.md Section "Principles" #2 — permit conditions are legally binding and must be tracked and demonstrated
- **Verification:** Procedure.md Step 4 (Initiate Permit Condition Compliance Tracking)

### Performance Requirements

**PR-01: Permit Review Timeliness**
- Permits shall be reviewed within [X] business days of receipt to enable timely construction commencement and compliance tracking initiation
- **Source:** **TBD** (project schedule and ER requirements)
- **Acceptance criteria:** **TBD** — review completed within [X] days of receipt
- **Verification:** Procedure.md Step 2; tracking in permit register

**PR-02: Compliance Tracking Completeness**
- All permit conditions shall be identified and tracked; no conditions shall be overlooked
- **Source:** **ASSUMPTION** — regulatory compliance requirement
- **Acceptance criteria:** 100% of permit conditions identified and assigned to compliance tracking deliverables (DEL-32.03-32.06)
- **Verification:** Procedure.md Step 4; compliance records deliverables

### Interface Requirements

**IR-01: DEL-32.01 (Permit Applications)**
- Issued permits (DEL-32.02) result from permit applications (DEL-32.01)
- Application-to-permit relationship shall be tracked in permit register
- (See Datasheet.md Attributes; Datasheet.md References)
- **Source:** **ASSUMPTION** — logical workflow sequence
- **Rationale:** See Guidance.md Section "Considerations — Relationship to DEL-32.01"
- **Coordination:** Ensure application (DEL-32.01) and issued permit (DEL-32.02) are linked in permit register
- **Verification:** Procedure.md Section "Prerequisites" and Step 3 (permit register updated)

**IR-02: DEL-32.07 (Correspondence Register) and DEL-32.08 (Correspondence Copies)**
- Permit issuance notifications and issued permit copies shall be logged in correspondence register (DEL-32.07) and filed in correspondence copies (DEL-32.08)
- (See Datasheet.md References)
- **Source:** **ASSUMPTION** — project recordkeeping requirement
- **Coordination:** Ensure permit receipt is logged and permit copy is filed
- **Verification:** Procedure.md Steps 2.3, 3.2, 3.4

**IR-03: DEL-32.03 through DEL-32.06 (Compliance Records)**
- Permit conditions identified in issued permits (DEL-32.02) shall be tracked and demonstrated through compliance records:
  - DEL-32.03 (VFPA PER Compliance Records) — VFPA PER approval conditions
  - DEL-32.04 (DFO Compliance Records) — DFO Fisheries Act authorization conditions
  - DEL-32.05 (Transport Canada Compliance Records) — Transport Canada approval conditions
  - DEL-32.06 (Code Compliance Records) — Building code and other permit conditions
- (See Datasheet.md Attributes — "Permit Condition Compliance Tracking"; Datasheet.md References)
- **Source:** **ASSUMPTION** — regulatory compliance requirement
- **Rationale:** See Guidance.md Section "Principles" #2 and Section "Considerations — Relationship to Compliance Records"
- **Coordination:** Assign each permit condition to appropriate compliance records deliverable; initiate tracking upon permit receipt
- **Verification:** Procedure.md Step 4 (Initiate Compliance Tracking)

### Quality Requirements

**QR-01: Permit Document Control**
- All issued permits shall be managed per project document control procedures
- Permits shall be filed, stored, and retrievable per project requirements
- **Source:** **ASSUMPTION** — project quality management requirement
- **Verification:** Procedure.md Step 3.4 (File Permit in Project Records) and Section "Records"

**QR-02: Permit Accuracy Verification**
- Each issued permit shall be verified for accuracy (project information, scope, dates match application)
- **Source:** **ASSUMPTION** — quality assurance requirement
- **Verification:** Procedure.md Step 2.2 (Review Permit Content and Conditions) — accuracy check

## Standards

**Project Delivery and Quality Management:**
- ISO 9001:2015 (Quality Management Systems) — **ASSUMPTION**: Applicable to project delivery processes
- **TBD** — Project Quality Management Plan

**Regulatory Requirements:**
(See Datasheet.md Conditions — anticipated permit types; see DEL-32.01 Specification.md for detailed authority requirements)

- Authority-issued permits and permit conditions — **TBD** (specific to each permit)

**Project-Specific Requirements:**
- Employer's Requirements Volume 2 Parts 1–3 — **location TBD** (Source: Decomposition Section 3)

## Verification

**Verification methods:**

(See Datasheet.md Attributes — "Verification Method"; see Guidance.md for rationale; see Procedure.md for detailed activities)

| Verification Activity | Method | Responsible Party | Acceptance Criteria | Procedure Ref |
|----------------------|--------|-------------------|---------------------|---------------|
| Permit receipt confirmed | Receipt acknowledgment to authority | **TBD** (Permit Coordinator) | Receipt confirmation obtained | Step 2.1 |
| Permit accuracy verified | Review against application | **TBD** (Permit Coordinator / Reviewer) | Permit content matches application; no discrepancies | Step 2.2 |
| Permit conditions identified | Extract and classify conditions | **TBD** (Permit Coordinator / QA/QC Manager) | All conditions identified and classified by type | Step 2.2 |
| Permit recorded | Update permit register | **TBD** (Permit Coordinator) | Permit register updated with issued permit details | Step 3 |
| Permit distributed | Distribute to distribution list | **TBD** (Permit Coordinator) | Distribution complete; recipients confirmed | Step 3.3 |
| Compliance tracking initiated | Assign conditions to compliance deliverables | **TBD** (QA/QC Manager) | All conditions assigned to DEL-32.03-32.06 | Step 4 |

**Sign-off requirements:** **TBD** — per project quality procedures

## Documentation

**Required documentation outputs:**
- Building permits, construction permits, environmental permits (Source: Decomposition Section 5; Datasheet.md Construction)

**Permit documentation format:**
- Authority-issued format (varies by authority) — **TBD**
- Typically: official certificate or letter with authority seal/signature, permit number, issue/expiry dates, project scope, permit conditions

**Document control:**
- Storage location: Filed in project records per Procedure.md Section "Records"
- Copies: Filed in DEL-32.08 (Correspondence Copies); logged in DEL-32.07 (Correspondence Register)
- Retention requirements: **TBD** — per contract and regulatory requirements (typically project duration + post-construction period)
