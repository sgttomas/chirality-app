# Specification: DEL-32.01 Permit Applications

## Scope

This specification defines the requirements for **Permit Applications** within **PKG-32 Regulatory & Permits**.

**Purpose:** Provides project management/control documentation for permit applications required by the Employer's Requirements (ERs). (Source: _CONTEXT.md; Decomposition Section 5; Datasheet.md Attributes)

**Coverage:** Contractor-responsible permit applications only. Employer-responsible permits are excluded. (Source: Decomposition Section 1.2 — scope boundary; Datasheet.md Conditions)

**Anticipated deliverable artifacts:**
- Contractor permit applications (Source: Decomposition Section 5, DEL-32.01 row; Datasheet.md Construction)

**Relationship to project objectives:**
- **OBJ-6: Regulatory Compliance** — "The Works comply with all permits, codes, and authority requirements" (Source: Decomposition Section 6, objective mapping; Datasheet.md References)

**Downstream use:**
- Permit applications (DEL-32.01) are submitted to regulatory authorities to obtain issued permits (DEL-32.02)
- Issued permits include conditions that must be demonstrated through compliance records (DEL-32.03 through DEL-32.06)
- See Guidance.md Section "Principles" for regulatory compliance framework context

## Requirements

### Functional Requirements

**FR-01: Permit Identification and Planning**
- The Contractor shall identify all permits required for the Works based on the Employer's Requirements and applicable regulations
- The Contractor shall develop a permit register listing all Contractor-responsible permits (see Datasheet.md Attributes — "Permit Register" entity)
- The Contractor shall develop a permit acquisition schedule integrated into the project schedule (see Datasheet.md Attributes — "Permit Acquisition Schedule" entity)
- **Source:** **ASSUMPTION** — standard D&B contract requirement; **location TBD** (Employer's Requirements Volume 2 Part 1)
- **Rationale:** See Guidance.md Section "Principles" #1 (Early identification and planning) — regulatory approval timelines can be lengthy and must be factored into project schedule
- **Verification:** Procedure.md Step 1 (Permit Identification and Planning); permit register cross-checked against ER requirements and regulatory authority requirements

**FR-02: Application Preparation**
- Each permit application shall be prepared in accordance with the applicable authority's requirements and application forms (see Datasheet.md Attributes — "Authority Application Forms" entity)
- Applications shall include all required supporting documentation as specified by the authority (see FR-03)
- **Source:** **ASSUMPTION** — regulatory compliance requirement; **TBD** (authority-specific requirements)
- **Rationale:** See Guidance.md Section "Principles" #4 (Authority-specific requirements) — each regulatory authority has its own application forms, supporting documentation requirements, review processes, and approval timelines
- **Verification:** Procedure.md Step 2 (Application Preparation); application completeness check against authority checklists

**FR-03: Supporting Documentation**
- Permit applications shall include all required supporting documentation, including:
  - **Design drawings** (as-applicable from PKG-04 through PKG-26) — site plans, civil, structural, process, electrical, fire protection, environmental control
  - **Technical specifications** (as-applicable from discipline packages)
  - **Calculations and design rationale** (as-applicable) — structural, fire protection, environmental
  - **Environmental assessments and studies** — **TBD**
  - **Geotechnical reports** (PKG-02, PKG-03) — **TBD**: Confirm requirement per permit type
  - **Hazard assessments and safety studies** — **TBD**
  - **Operational information** — process descriptions, operating procedures, emergency response plans (as applicable) — **TBD**
  - **Other authority-required documentation** — **TBD**
- (See Datasheet.md Attributes — "Supporting Documentation" entity; Datasheet.md Construction — production inputs)
- **Source:** **ASSUMPTION** — typical permit application requirements; **TBD** (authority-specific requirements)
- **Rationale:** See Guidance.md Section "Considerations — Supporting Documentation Requirements" for typical documentation types and Guidance.md Section "Considerations — Design Maturity Requirements" for design maturity considerations
- **Verification:** Procedure.md Step 2.2 (Compile Supporting Documentation); document checklist per authority requirements

**FR-04: Contractor-Employer Interface**
- Permit applications shall be submitted to Employer for review prior to authority submission (if required by contract)
- (See Datasheet.md Attributes — "Employer Review Process" entity; Datasheet.md Conditions — scope boundary and interface protocol)
- **Source:** **TBD** (Employer's Requirements — location TBD)
- **Rationale:** See Guidance.md Section "Principles" #6 (Employer coordination) — Employer may require review/approval of permit applications before authority submission; this review step must be planned into schedule
- **Verification:** Procedure.md Step 4 (Employer Review); Employer review/approval record

**FR-05: Authority Submission**
- Permit applications shall be submitted to the applicable regulatory authorities with all required fees and documentation
- (See Datasheet.md Attributes — "Authority Submission" entity)
- **Source:** **ASSUMPTION** — standard regulatory requirement
- **Rationale:** See Guidance.md Section "Principles" #2 (Scope boundary clarity) and #4 (Authority-specific requirements)
- **Verification:** Procedure.md Step 5 (Authority Submission); submission receipts and tracking (see FR-06 and IR-04)

**FR-06: Application Tracking**
- The status of each permit application shall be tracked from submission through approval/issuance
- Tracking shall be documented in the permit register and correspondence register (DEL-32.07)
- (See Datasheet.md Attributes — "Application Tracking" entity)
- **Source:** **ASSUMPTION** — project management requirement
- **Rationale:** See Guidance.md Section "Principles" #7 (Tracking and follow-up) — permit application status must be actively tracked to ensure timely follow-up on authority requests and approvals
- **Verification:** Procedure.md Step 6 (Application Tracking and Follow-Up); correspondence register (DEL-32.07) updated; issued permits recorded in DEL-32.02

### Performance Requirements

**PR-01: Completeness and Accuracy**
- All permit applications shall be complete and accurate to minimize authority requests for additional information (RFIs) and resubmissions
- **Source:** **ASSUMPTION** — project efficiency and schedule requirement
- **Rationale:** See Guidance.md Section "Principles" #3 (Completeness and accuracy) — incomplete or inaccurate applications result in authority RFIs and resubmissions, which delay permit issuance and impact project schedule; and Guidance.md Section "Trade-offs — Completeness vs Schedule Pressure"
- **Acceptance criteria:** **TBD** — target: fewer than [X] authority RFIs per application
- **Verification:** Procedure.md Step 3 (Internal Review) — technical accuracy review, completeness check, regulatory compliance check

**PR-02: Schedule Compliance**
- Permit applications shall be submitted in accordance with the project permit acquisition schedule (see FR-01 — permit acquisition schedule)
- **Source:** **TBD** (project schedule and Employer's Requirements — location TBD)
- **Rationale:** See Guidance.md Section "Considerations — Schedule and Critical Path" — permit approval timelines vary widely (2 weeks to 12+ months); long-lead permits must be identified early and submitted as soon as design maturity allows
- **Acceptance criteria:** **TBD** — application submission dates per project schedule
- **Verification:** Procedure.md Step 1.7 (Develop Permit Acquisition Schedule) and Step 5 (Authority Submission); schedule compliance tracking

### Interface Requirements

**IR-01: Discipline Design Packages**
- Permit applications shall interface with design deliverables from applicable discipline packages (PKG-01 through PKG-31)
- Design information (drawings, specifications, calculations) shall flow from discipline packages to permit applications
- (See Datasheet.md Construction — production inputs; see Datasheet.md References — related discipline packages)
- **Source:** **ASSUMPTION** — design-build workflow
- **Rationale:** See Guidance.md Section "Principles" #5 (Integrated design basis) — permit applications rely on design information from multiple discipline packages; design must be sufficiently mature before applications can be prepared; and Guidance.md Section "Considerations — Design Maturity Requirements"
- **Coordination:** **TBD** — define information handoff protocol and design maturity thresholds for each permit type; see Guidance.md Section "Trade-offs — Application Timing vs Design Maturity"
- **Verification:** Procedure.md Step 2.2 (Compile Supporting Documentation) — coordinate with discipline package leads

**IR-02: Employer-Responsible Permits**
- The Contractor shall coordinate with the Employer regarding Employer-responsible permits to ensure scope boundary clarity and interface requirements
- (See Datasheet.md Conditions — scope boundary)
- **Source:** Decomposition Section 1.2 (scope boundary)
- **Rationale:** See Guidance.md Section "Principles" #2 (Scope boundary clarity) — Contractor is responsible only for Contractor-responsible permits; Employer-responsible permits are excluded; and Guidance.md Section "Considerations — Employer-Contractor Interface"
- **Coordination:** **TBD** — define interface protocol and communication requirements
- **Verification:** Procedure.md Step 1.5 (Clarify Scope Boundary) — document Contractor vs Employer permit responsibilities

**IR-03: DEL-32.02 (Permits)**
- Permit applications (DEL-32.01) result in issued permits (DEL-32.02)
- Application-to-permit relationship shall be tracked in permit register
- (See Datasheet.md Attributes — Related Deliverable; see Datasheet.md References — related deliverables)
- **Source:** **ASSUMPTION** — logical workflow sequence
- **Rationale:** See Guidance.md Section "Considerations — Coordination with Related Deliverables"
- **Coordination:** Track application-to-permit relationship; ensure issued permits are recorded in DEL-32.02
- **Verification:** Procedure.md Step 6.4 (Receive Issued Permit) — record issued permit in DEL-32.02

**IR-04: DEL-32.07 (Correspondence Register)**
- All authority correspondence related to permit applications shall be tracked in the correspondence register (DEL-32.07)
- This includes: application submissions, authority RFIs, Contractor responses, and permit issuance notifications
- (See Datasheet.md Attributes — "Application Tracking" entity; see Datasheet.md References — related deliverables)
- **Source:** **ASSUMPTION** — project management requirement
- **Rationale:** See Guidance.md Section "Principles" #7 (Tracking and follow-up) and Guidance.md Section "Considerations — Coordination with Related Deliverables"
- **Coordination:** Ensure submission records, RFIs, responses, and approvals are logged in DEL-32.07 and copies filed in DEL-32.08
- **Verification:** Procedure.md Steps 5.5, 6.2, 6.4 (Record in Correspondence Register) — log submissions, RFIs, and approvals

### Quality Requirements

**QR-01: Document Control**
- All permit applications shall be managed per the project document control procedures
- Document numbering, revision control, and storage shall comply with project procedures
- **Source:** **ASSUMPTION** — project quality management requirement
- **Rationale:** See Guidance.md Section "Principles" — quality management framework; ISO 9001:2015 applicable to project delivery processes
- **Verification:** Procedure.md Section "Records — Record management" — document control per project procedures — **TBD** (define document numbering and revision control system)

**QR-02: Technical Review**
- Permit applications shall undergo technical review by qualified personnel prior to Employer submission and/or authority submission
- Review shall verify technical accuracy and consistency with design deliverables
- (See Datasheet.md Attributes — "Internal Review Process" entity)
- **Source:** **ASSUMPTION** — quality assurance requirement
- **Rationale:** See Guidance.md Section "Principles" #3 (Completeness and accuracy) and Guidance.md Section "Trade-offs — Completeness vs Schedule Pressure" — thorough internal review before submission reduces authority RFI risk
- **Verification:** Procedure.md Step 3.1 (Technical Accuracy Review) — discipline lead(s) review application package; review sign-offs — **TBD** (define review protocol and qualifications)

**QR-03: Regulatory Compliance Check**
- Each permit application shall be checked for compliance with the applicable authority's requirements and the Employer's Requirements
- (See Datasheet.md Attributes — "Internal Review Process" entity)
- **Source:** **ASSUMPTION** — regulatory compliance requirement
- **Rationale:** See Guidance.md Section "Principles" #4 (Authority-specific requirements) — each authority has specific requirements; applications must be compliant
- **Verification:** Procedure.md Step 3.3 (Regulatory Compliance Check) — regulatory specialist (or designated reviewer) reviews for authority compliance; compliance checklist — **TBD**

## Standards

**Applicable codes and standards:**

**Project Delivery and Quality Management:**
- **ISO 9001:2015 (Quality Management Systems)** — **ASSUMPTION**: Likely applicable to project delivery processes and document control (see Datasheet.md References)
- **TBD** — Project Quality Management Plan reference

**Regulatory and Jurisdictional Requirements:**

(See Datasheet.md Conditions — Key regulatory authorities; see Guidance.md Section "Considerations — Regulatory Authority Identification" for detailed authority descriptions)

- **TBD** — Vancouver Fraser Port Authority (VFPA) Project and Environmental Review (PER) process requirements
- **TBD** — Department of Fisheries and Oceans (DFO) permit requirements (Fisheries Act)
- **TBD** — Transport Canada regulatory requirements (rail and marine interface)
- **TBD** — City of Surrey / Fraser Valley Regional District building and development permit requirements
- **TBD** — Provincial environmental permit requirements (BC Ministry of Environment)
- **TBD** — Federal environmental assessment requirements (if applicable)
- **TBD** — WorkSafeBC occupational health and safety requirements
- **TBD** — Fire authority requirements (Surrey Fire Service or applicable authority)

**Project-Specific Requirements:**

(See Datasheet.md References; Decomposition Section 3)

- **Employer's Requirements Volume 2 Part 1 (General Requirements)** — **location TBD**
- **Employer's Requirements Volume 2 Part 2 (Civil & Process Mechanical Works)** — **location TBD**
- **Employer's Requirements Volume 2 Part 3 (Building Works)** — **location TBD**

## Verification

**Verification methods for permit application documents:**

(See Datasheet.md Attributes — "Verification Method"; see Guidance.md for verification rationale; see Procedure.md for detailed verification activities)

| Verification Activity | Method | Responsible Party | Acceptance Criteria | Procedure Ref |
|----------------------|--------|-------------------|---------------------|---------------|
| Technical accuracy review | Document review against design deliverables | **TBD** (Contractor discipline lead) | Technical content consistent with design | Step 3.1 |
| Completeness check | Checklist against authority requirements | **TBD** (Contractor project delivery lead) | All required sections and attachments included | Steps 2.5, 3.2 |
| Regulatory compliance check | Review against authority application requirements | **TBD** (Contractor regulatory specialist) | Application format and content compliant | Step 3.3 |
| Employer review (if required) | Submittal to Employer per contract | **TBD** | Employer approval/comments received | Step 4 |
| Authority submission | Submit to regulatory authority with fees | **TBD** (Contractor project delivery lead) | Submission receipt obtained | Step 5 |
| Tracking and follow-up | Monitor application status | **TBD** (Contractor project delivery lead) | Status updates recorded in DEL-32.07 | Step 6 |

**Sign-off requirements:**
- **TBD** — Originator, checker, approver per project quality procedures (see Procedure.md Section "Verification")

## Documentation

**Required documentation outputs:**
- Contractor permit applications (Source: Decomposition Section 5, DEL-32.01 row; Datasheet.md Construction)

**Anticipated permit application types (based on facility scope):**

(See Datasheet.md Conditions — Key regulatory authorities; see Guidance.md Section "Considerations — Regulatory Authority Identification")

- **TBD** — VFPA Project and Environmental Review (PER) application
- **TBD** — DFO Fisheries Act authorization application (marine works)
- **TBD** — Transport Canada approvals (rail/marine interface)
- **TBD** — Building permits (City of Surrey or applicable authority)
- **TBD** — Development permits (local authority)
- **TBD** — Environmental discharge permits (provincial/federal)
- **TBD** — Occupational health and safety notifications/approvals (WorkSafeBC)
- **TBD** — Fire department approvals (Surrey Fire Service or applicable authority)
- **TBD** — Other authority-required permits and approvals

**Documentation format and structure:**

(See Datasheet.md Construction — document structure; see Guidance.md Section "Examples — Document Structure Example" for typical application package structure; see Procedure.md Step 2 for assembly process)

- Application cover letters — **TBD** (Procedure Step 2.4)
- Completed authority application forms — **TBD** (authority-specific) (Procedure Step 2.3)
- Technical drawings and specifications (cross-referenced to discipline packages) — **TBD** (Procedure Step 2.2)
- Supporting calculations and reports — **TBD** (Procedure Step 2.2)
- Environmental documentation — **TBD** (Procedure Step 2.2)
- Fee payment records — **TBD** (Procedure Step 5.2)

**Document control:**
- Document numbering system: **TBD** — per project document control procedures (see QR-01)
- Revision control: **TBD** — per project document control procedures (see QR-01)
- Storage location: `2_Checking/` (during review) → submitted to Employer/authority → tracking in DEL-32.07 (IR-04) → copies in DEL-32.08
- Retention requirements: **TBD** — per contract and regulatory requirements (see Procedure.md Section "Records")
