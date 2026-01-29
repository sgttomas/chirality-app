# Datasheet: DEL-32.02 Permits

## Identification

| Field | Value |
|-------|-------|
| Deliverable ID | DEL-32.02 |
| Name | Permits |
| Package | PKG-32 Regulatory & Permits |
| Discipline | Project Delivery |
| Type | Permit |
| Responsible | D&B Contractor |
| Status | INITIALIZED |

**Source:** _CONTEXT.md; Decomposition Section 5 (PKG-32 deliverable table)

## Attributes

| Attribute | Value |
|-----------|-------|
| Deliverable Purpose | Defines and substantiates permits in accordance with ER requirements |
| Scope Coverage | Contractor-responsible issued permits only (Employer-responsible permits excluded) |
| Related Deliverable (Upstream) | DEL-32.01 (Permit Applications — applications result in issued permits) |
| Related Deliverables (Downstream) | DEL-32.03 through DEL-32.06 (Compliance Records — evidence of permit condition compliance) |
| Document Type | Issued permit documents (official regulatory authority permits) |
| Format | **TBD** — Authority-issued format (varies by authority; typically PDF or hard copy certificate) |
| Verification Method | See Specification.md Section "Verification" and Procedure.md Section "Verification" |

**Source:** _CONTEXT.md; Decomposition Section 5; **ASSUMPTION** labels as noted

**Key entities:**

| Entity | Description | Specification Ref | Procedure Ref |
|--------|-------------|-------------------|---------------|
| Issued Permit Documents | Official permits issued by regulatory authorities | FR-01, FR-02 | Steps 2, 3 |
| Permit Conditions | Requirements/restrictions imposed by authorities in permits | FR-03, IR-03 | Step 2.2, Step 4 |
| Permit Register | Tracking of issued permits | FR-04 | Step 3 |
| Permit Distribution List | Project team members requiring copies | FR-05 | Step 3.3 |
| Permit Condition Compliance Tracking | System for tracking compliance | IR-03, FR-06 | Step 4 |

## Conditions

**Project Context:**

(Same as DEL-32.01; see DEL-32.01 Datasheet.md for details)

- **Project:** Canola Oil Transload Facility Phase 1, Fraser Surrey Terminal, Surrey, BC
- **Contract:** CAVAN-MIS-2022-342/D&B/2022/022, Design & Build for DP World Fraser Surrey Inc.
- **Facility:** 1,000,000 MT/annum throughput; 45,000 MT storage; 32 railcar stations; marine loading
- (Source: Decomposition Section 1.1)

**Anticipated permit types:**

(Source: Decomposition Section 5, DEL-32.02 — "Building permits, construction permits, environmental permits"; see DEL-32.01 for application types)

- Building permits, construction permits, environmental permits
- VFPA PER approval, DFO Fisheries Act authorization, Transport Canada approvals — **ASSUMPTION**: Based on scope
- Development permits, fire approvals, WorkSafeBC notifications — **TBD**

**Scope boundary:**

- **Contractor-responsible permits only** (Source: Decomposition Section 1.2)
- Employer-responsible permits excluded
- **TBD** — Interface protocol with Employer permits

## Construction

**Deliverable Production:**

This deliverable consists of **official permit documents issued by regulatory authorities**. Production involves:

1. Submitting permit applications (DEL-32.01)
2. Responding to authority RFIs during review
3. Receiving issued permits from authorities
4. Reviewing permit conditions
5. Recording, filing, and distributing permits
6. Initiating compliance tracking

(See Procedure.md for detailed workflow)

**Anticipated artifacts:**
- Building permits, construction permits, environmental permits (Source: Decomposition Section 5, DEL-32.02)

**Production flow:**
- **Inputs:** Permit applications (DEL-32.01); authority review/approval process; RFI responses
- **Outputs:** Issued permit documents; permit conditions requiring compliance tracking (DEL-32.03-32.06)

**Permit characteristics:**
- **Format:** Authority-issued (certificate/letter with seal/signature) — **TBD**: Per authority
- **Content:** Permit number, dates, scope, conditions, authority contact — **TBD**: Varies by authority
- **Legal status:** Official regulatory approval; legally binding with enforceable conditions
- **Validity:** May have expiry dates or deadlines — **TBD**: Per permit

## References

**Primary sources:**
- `_CONTEXT.md`, Decomposition Sections 1.1, 1.2, 3, 5, 6
- Specification.md, Guidance.md, Procedure.md

**Related deliverables:**
- **DEL-32.01 (Permit Applications)** — upstream: applications result in permits
- **DEL-32.03-32.06 (Compliance Records)** — downstream: evidence of permit condition compliance
- **DEL-32.07 (Correspondence Register)** — tracking permit issuance notifications
- **DEL-32.08 (Correspondence Copies)** — copies of issued permits filed

**Standards:**
- Employer's Requirements Volume 2 Parts 1–3 — **location TBD**
- Authority-issued permits and conditions — **TBD**
- ISO 9001:2015 — **ASSUMPTION**: Applicable to document control

**Dependencies:** See `_DEPENDENCIES.md` — **NOT_TRACKED**
