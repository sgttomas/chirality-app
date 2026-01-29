# Guidance: DEL-32.02 Permits

## Purpose

This guidance document supports **Permits** for **PKG-32 Regulatory & Permits**.

**Deliverable purpose:** Defines and substantiates permits in accordance with ER requirements. (Source: _CONTEXT.md; Decomposition Section 5; Datasheet.md)

**Deliverable classification:**
- **Type:** Permit (issued regulatory documents)
- **Discipline:** Project Delivery
- **Responsible party:** D&B Contractor
- (Source: _CONTEXT.md; Datasheet.md Identification)

**Objective alignment:** Supports **OBJ-6: Regulatory Compliance** — "The Works comply with all permits, codes, and authority requirements." (Source: Decomposition Section 6)

## Principles

### 1. Timely Permit Receipt (supports Specification.md FR-01)

Issued permits enable construction commencement. Timely receipt, acknowledgment, and review are critical to avoid construction delays.

- Receipt must be confirmed with issuing authority
- Permits must be reviewed promptly (see Specification.md PR-01)
- See Procedure.md Step 2 for receipt and review process

### 2. Permit Condition Management (supports Specification.md FR-03, FR-06)

Permit conditions are legally binding requirements. Non-compliance can result in stop-work orders, fines, or permit revocation.

- All conditions must be identified and classified (pre-construction, during-construction, post-construction, operational)
- Conditions must be assigned to compliance tracking deliverables (DEL-32.03-32.06)
- Compliance must be demonstrated and documented
- See "Considerations — Permit Condition Types" below
- See Procedure.md Steps 2.2 and 4 for condition identification and tracking initiation

### 3. Record Management (supports Specification.md FR-04, QR-01)

Permits are official regulatory documents requiring proper recordkeeping:

- Permits must be filed in project records (DEL-32.08)
- Permit status must be tracked in permit register (extension of DEL-32.01 register)
- Permits must be readily retrievable for inspections and audits
- See Procedure.md Step 3 for recording and filing process

## Considerations

### Permit Condition Types

(Supports Specification.md FR-03; see Datasheet.md Attributes — "Permit Conditions")

**Pre-construction conditions:**
- Must be satisfied before construction work begins
- Examples: Submit additional plans, obtain additional approvals, provide insurance certificates, pay fees
- **Impact:** Construction cannot commence until pre-construction conditions are satisfied
- **Tracking:** Assign to DEL-32.03-32.06; verify completion before construction start

**During-construction conditions:**
- Ongoing compliance requirements during construction
- Examples: Environmental monitoring, erosion control, noise limits, work hour restrictions, inspection notifications
- **Impact:** Non-compliance during construction can result in stop-work orders
- **Tracking:** Assign to DEL-32.03-32.06; ongoing monitoring and documentation required

**Post-construction conditions:**
- Required after construction completion
- Examples: Submit as-built drawings, remove temporary works, restore disturbed areas, final inspections
- **Impact:** Permit closure and final acceptance may be contingent on post-construction condition compliance
- **Tracking:** Assign to DEL-32.03-32.06; complete before permit closeout

**Operational conditions:**
- Ongoing compliance requirements during facility operation
- Examples: Annual inspections, maintenance records, operational limits, reporting requirements
- **Impact:** Non-compliance during operation can result in operational restrictions or permit suspension
- **Tracking:** Assign to DEL-32.03-32.06; establish operational compliance protocols; typically transfer to facility operations team at handover

### Relationship to DEL-32.01 (Permit Applications)

(Supports Specification.md IR-01; see Datasheet.md References)

DEL-32.02 (Permits) is the direct result of DEL-32.01 (Permit Applications):

- Application submitted (DEL-32.01) → Authority review → Permit issued (DEL-32.02)
- Permit register tracks full lifecycle: application submission, review status, permit issuance
- Application-to-permit relationship must be clear for auditing and compliance verification

**Coordination:** Link each issued permit (DEL-32.02) to its application (DEL-32.01) in permit register

### Relationship to Compliance Records (DEL-32.03-32.06)

(Supports Specification.md IR-03; see Datasheet.md References)

Issued permits (DEL-32.02) contain conditions that must be tracked and demonstrated through compliance records:

| Compliance Deliverable | Permit Conditions Tracked |
|------------------------|---------------------------|
| DEL-32.03 (VFPA PER Compliance) | VFPA Project and Environmental Review approval conditions |
| DEL-32.04 (DFO Compliance) | DFO Fisheries Act authorization conditions |
| DEL-32.05 (Transport Canada Compliance) | Transport Canada approval conditions |
| DEL-32.06 (Code Compliance) | Building permits, fire permits, environmental permits, and other code compliance conditions |

**Coordination:** Upon permit receipt, extract conditions and assign to appropriate compliance deliverable; initiate compliance tracking (see Procedure.md Step 4)

### Distribution and Communication

(Supports Specification.md FR-05; see Datasheet.md Attributes — "Permit Distribution List")

Relevant team members must be aware of issued permits and conditions:

- **Project Manager** — overall project compliance and schedule impacts
- **Discipline Leads** — discipline-specific permit requirements and conditions
- **Construction Manager** — construction phase compliance (during-construction conditions)
- **QA/QC Manager** — compliance tracking and verification
- **HSE Manager** — health, safety, and environmental conditions
- **Other stakeholders** — as defined in project communication plan

**Consideration:** Tailor distribution to permit scope; not all permits require distribution to all team members

### Coordination with DEL-32.01 (Permit Register Continuity)

(Supports Specification.md FR-04; see Datasheet.md Attributes — "Permit Register")

The permit register initiated in DEL-32.01 (Permit Applications) is continued and updated in DEL-32.02 (Permits):

- Application phase: Track application submission, RFIs, review status
- Issuance phase: Update register with permit number, issue date, expiry date, conditions summary
- Compliance phase: Track compliance status for each condition (linked to DEL-32.03-32.06)

**Register continuity ensures:** Complete audit trail from application through issuance to compliance demonstration

## Trade-offs

### Immediate Construction Start vs Comprehensive Permit Review

**Trade-off:** Start construction immediately upon permit receipt (faster) vs conduct thorough permit review to identify all conditions before construction starts (slower but reduces compliance risk).

**Considerations:**
- Unidentified permit conditions discovered during construction can cause delays, rework, or stop-work orders
- Thorough pre-construction permit review identifies all requirements upfront
- Some permits allow construction start for certain scopes while other conditions are being satisfied

**Guidance:**
- Conduct rapid initial review to identify pre-construction conditions (Procedure.md Step 2.2)
- Verify all pre-construction conditions are satisfied before construction start
- Conduct comprehensive permit review concurrently to identify all during-construction, post-construction, and operational conditions
- Prioritize review thoroughness over speed to avoid mid-construction surprises

### Centralized vs Distributed Permit Management

**Trade-off:** Centralized permit management (single permit coordinator manages all permits) vs distributed management (discipline leads manage their own permits).

**Considerations:**
- **Centralized:** Better consistency, easier tracking, clear accountability; but single point of failure, potential bottleneck
- **Distributed:** Discipline expertise applied to permit management, reduced bottleneck; but coordination challenges, potential gaps

**Guidance:**
- Use **centralized permit coordinator** for permit receipt, recording, and compliance tracking initiation (Procedure.md Steps 2, 3, 4)
- Use **distributed discipline leads** for technical permit review and discipline-specific compliance execution
- Best of both: Centralized coordination with distributed technical expertise

## Examples

### Permit Content Example (Conceptual)

**Typical issued permit document:**

1. **Header Information**
   - Permit number: [AUTHORITY-TYPE-YEAR-NUMBER]
   - Issue date: [DATE]
   - Expiry date (if applicable): [DATE]
   - Issuing authority: [AUTHORITY NAME]

2. **Project Information**
   - Project name: Canola Oil Transload Facility Phase 1
   - Project location: Fraser Surrey Terminal, 11060 Elevator Road, Surrey, BC
   - Applicant: [CONTRACTOR NAME]
   - Owner: DP World Fraser Surrey Inc.

3. **Approved Scope**
   - Description of approved works per application

4. **Permit Conditions** (variable by permit type and authority)
   - Pre-construction conditions (if any)
   - During-construction conditions (if any)
   - Post-construction conditions (if any)
   - Operational conditions (if applicable)

5. **Authority Contact Information**
   - Inspector name and contact
   - Authority office address and phone

6. **Signatures and Seal**
   - Authorized signatory
   - Official authority seal/stamp

**Note:** Actual permit format varies by authority. Some permits are brief (single-page certificate); others are multi-page documents with detailed conditions.

### Permit Condition Examples

**Pre-construction condition example:**
- "Prior to commencement of marine works, the Contractor shall submit a Marine Construction Management Plan to DFO for approval."
- **Classification:** Pre-construction (work cannot start until condition satisfied)
- **Compliance tracking:** Assign to DEL-32.04 (DFO Compliance); prepare and submit plan; obtain DFO approval; file approval in compliance records

**During-construction condition example:**
- "During pile driving operations, underwater noise monitoring shall be conducted in accordance with the approved Environmental Management Plan. Monitoring results shall be submitted to VFPA monthly."
- **Classification:** During-construction (ongoing compliance during specific construction activity)
- **Compliance tracking:** Assign to DEL-32.03 (VFPA PER Compliance); establish monitoring protocol; conduct monitoring; submit monthly reports; file reports in compliance records

**Post-construction condition example:**
- "Within 30 days of construction completion, as-built drawings shall be submitted to the City of Surrey Building Department."
- **Classification:** Post-construction (required after construction completion)
- **Compliance tracking:** Assign to DEL-32.06 (Code Compliance); prepare as-built drawings; submit to authority; obtain confirmation; file in compliance records

**Operational condition example:**
- "The facility fire protection system shall be inspected annually by a qualified fire protection professional. Inspection reports shall be retained on-site and made available to the Fire Department upon request."
- **Classification:** Operational (ongoing requirement during facility operation)
- **Compliance tracking:** Assign to DEL-32.06 (Code Compliance); establish operational inspection protocol; transfer requirement to facility operations team at handover; ensure inspection schedule and recordkeeping procedures are in place
