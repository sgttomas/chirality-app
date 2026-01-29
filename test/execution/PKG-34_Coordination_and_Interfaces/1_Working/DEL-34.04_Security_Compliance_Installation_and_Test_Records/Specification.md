# Specification: DEL-34.04 Security Compliance Installation & Test Records

## Scope

This specification defines the requirements for **Security Compliance Installation & Test Records** within **PKG-34 Coordination & Interfaces**.

**Purpose:** Provides evidence of security compliance for construction at secure port facility (per Decomposition line 752, `_CONTEXT.md`).

**Objective alignment:** Supports OBJ-5 "Terminal Continuity" — maintaining secure facility operations during construction (Decomposition lines 63, 784).

**Anticipated deliverable artifacts:** CBSA/TC security compliance records

**Inclusions:** Personnel security clearances, site access control, security incidents, regulatory compliance (CBSA, Transport Canada MTSR)

**Exclusions:** Physical security systems design (fencing, cameras, gates) — covered by discipline packages

## Requirements

### Functional Requirements

**FR-1: Personnel Security Clearances**
- All construction personnel requiring restricted area access shall obtain security clearances from CBSA/Transport Canada per facility security requirements
- Security clearance applications submitted with adequate lead time (4-8 weeks typical)
- Clearance records maintained (personnel roster, approvals, expiry dates, renewals)
- **Source:** **ASSUMPTION**: CBSA restricted area access requirements; Transport Canada MTSR

**FR-2: Site Access Control**
- Site access badges issued to authorized personnel only (with valid security clearance)
- Visitor logs maintained (name, company, purpose, escort, time in/out)
- Vehicle access permits for authorized vehicles
- Restricted area access logged and authorized
- Lost/stolen badges reported and deactivated immediately
- **Source:** **ASSUMPTION**: Port facility access control best practice per ISO 45001

**FR-3: Security Incident Reporting**
- All security incidents reported and investigated (unauthorized access, security breaches, threats)
- Incidents reported to CBSA, Transport Canada, law enforcement as required
- Investigation findings and corrective actions documented
- **Source:** **ASSUMPTION**: Security incident management per MTSR and CBSA requirements

**FR-4: Regulatory Compliance**
- Compliance with Fraser Surrey Terminal Facility Security Plan (approved by Transport Canada)
- Compliance with CBSA border security requirements
- MARSEC level awareness and response procedures
- Regulatory inspections and audits documented
- **Source:** **ASSUMPTION**: Transport Canada MTSR; CBSA border security regulations

### Performance Requirements

**PR-1: Clearance Timeliness**
- Security clearance applications submitted early (minimum 6 weeks before required site access) — **TBD**
- Clearances valid for personnel duration on project
- Renewals processed before expiry
- **Source:** **ASSUMPTION**: Clearance processing timeline

**PR-2: Access Control Accuracy**
- 100% compliance: no unauthorized access to restricted areas
- Badge issuance only to personnel with valid clearances
- Visitor logs complete and accurate
- **Source:** **ASSUMPTION**: Security compliance requirement

**PR-3: Incident Response**
- Security incidents reported immediately (within 1 hour for significant incidents)
- CBSA/TC notified per regulatory requirements
- Investigation completed within required timeframe — **TBD**
- **Source:** **ASSUMPTION**: Security incident response requirement

### Interface Requirements

**IR-1: Facility Security Plan Compliance**
- Construction activities comply with Fraser Surrey Terminal Facility Security Plan
- Security coordinator liaison with Terminal security management
- **TBD** — Specific requirements per Facility Security Plan — **location TBD**
- **Source:** Transport Canada MTSR requirement for facility security plans

**IR-2: General Coordination Integration**
- Security topics discussed in coordination meetings (DEL-34.01) as needed
- Security incidents escalated per project procedures
- **Source:** Relation to DEL-34.01

### Quality Requirements

**QR-1: Confidentiality**
- Security records classified as Confidential/Security Sensitive
- Controlled access per CBSA/TC requirements
- Secure storage with encryption and access logging
- **Source:** **ASSUMPTION**: Security information protection requirement

**QR-2: Record Retention**
- Security clearance records retained per CBSA/TC requirements (typically 7+ years) — **TBD**
- Secure archival with controlled access
- **Source:** **ASSUMPTION**: CBSA/TC record retention requirements

## Standards

**Applicable regulations:**
- **CBSA:** Border security regulations, restricted area access
- **Transport Canada:** Marine Transportation Security Regulations (MTSR), Facility Security Plans
- **ISO 9001, ISO 45001** — Document control, site access control, incident reporting
- **Employer's Requirements** — **TBD** — **location TBD**

## Verification

**Verification:** Completeness check (all personnel have valid clearances); accuracy verification (access logs, incident reports); regulatory compliance (CBSA/TC inspections passed)

**Acceptance criteria:** All personnel cleared; no unauthorized access; security incidents properly reported and investigated; CBSA/TC compliance maintained

**Sign-off:** Originator: D&B Contractor security coordinator; Reviewer: Project manager; Approver: **TBD**; Regulatory acknowledgment: CBSA, Transport Canada (as applicable)

## Documentation

**Required outputs:** CBSA/TC security compliance records (personnel clearances, access control, incidents, inspections)

**Documentation requirements:** Confidential classification; secure storage; retention per CBSA/TC (typically 7+ years); controlled distribution

**Cross-references:** See Datasheet.md, Guidance.md, Procedure.md
