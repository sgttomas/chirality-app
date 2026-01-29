# Specification: DEL-35.05 Defects Liability Installation & Test Records

## Scope

Provides evidence of completion, inspection, and testing for defects liability — documenting defects identified during warranty period after handover (cross-reference DEL-35.03) and their rectification.

*Source: _CONTEXT.md; cross-reference DEL-35.03*

**Anticipated artifacts**: Defect rectification records, warranty claim records

*Source: _CONTEXT.md*

**Defects liability period**: **TBD** per Design & Build Contract (typically 12 months from Taking Over Date)

*Source: **ASSUMPTION** — typical warranty period; specific period TBD per contract*

## Requirements

### Functional Requirements

**FR-01: Defect Notification Records**
Document defect identification (description, location, severity, safety impact), discovery date, reported by, defect category, affected system, operational impact, photographic evidence.

**FR-02: Defect Assessment Records**
Document Contractor assessment (root cause, rectification approach, duration estimate), warranty determination (responsibility), urgency classification, rectification work scope/plan.

**FR-03: Defect Rectification Work Records**
Document work authorization, rectification work performed (date, personnel, activities), materials used, testing performed, photographs (before/during/after), Contractor QA/QC completion certification.

**FR-04: Defect Completion and Acceptance Records**
Document Employer inspection of rectified defect, acceptance testing (if required), Employer acceptance sign-off (defect closed), follow-up actions/monitoring, lessons learned.

**FR-05: Warranty Claim Records**
Document warranty claims (by Employer or by Contractor against OEM/supplier), claim description/justification, claim determination, resolution, claim closure.

**FR-06: Defects Liability Management Records**
Maintain defects liability register (master log of all defects, status, responsibility, target completion), Contractor response time tracking, Employer satisfaction tracking, defects liability period closure report.

*Source: **ASSUMPTION** based on typical defects liability record scope; see Datasheet.md for detailed content*

### Performance Requirements

**PR-01: Responsiveness**
Contractor response times per contract requirements:
- **TBD**: Emergency defects (safety-critical) — immediate response
- **TBD**: Urgent defects (operational impact) — response within [hours/days]
- **TBD**: Routine defects — response within [days/weeks]

**PR-02: Terminal Continuity (OBJ-5)**
Defect rectification minimizes disruption to facility operations per **OBJ-5: Terminal Continuity** — coordinate site access, schedule work during low-activity periods.

*Source: Decomposition Section 2 (OBJ-5)*

**PR-03: Safe and Reliable Operation (OBJ-1)**
Safety-critical defects rectified immediately to maintain **OBJ-1: Safe & Reliable Operation**.

*Source: Decomposition Section 2 (OBJ-1)*

**PR-04: Lifecycle Cost Optimization (OBJ-9)**
Effective defects liability management supports **OBJ-9: Lifecycle Cost Optimization** by rectifying defects before Employer incurs operational costs or system degradation.

*Source: Decomposition Section 2 (OBJ-9), Section 6 (DEL-35.01-35.05 support OBJ-9)*

### Interface Requirements

**IF-01: Handover Integration (DEL-35.03)**
Outstanding defects list from handover (DEL-35.03 punch list) forms initial defects liability workload; Taking Over Date establishes defects liability period commencement.

**IF-02: Training Integration (DEL-35.01, DEL-35.02)**
Training-related defects (if training inadequate or incorrect) addressed during defects liability period; may require training material updates or re-training.

**IF-03: All Project Deliverables**
Defects may relate to any facility system documented in project deliverables; defect rectification may require reference to design documentation, OEM manuals, commissioning records.

*Cross-references: DEL-35.03, DEL-35.01, DEL-35.02, all project deliverables*

### Quality Requirements

**QR-01**: Comply with project Quality Management Plan and contract warranty provisions
**QR-02**: Defect rectification work subject to Contractor QA/QC inspection
**QR-03**: Rectified defects subject to Employer inspection and acceptance
**QR-04**: Defects liability records maintained in defects register (traceability, status tracking)

## Standards

- ISO 9001:2015 (Quality Management — warranty management, customer satisfaction)
- ISO 10002:2018 (Customer Satisfaction — complaints handling)
- Design & Build Contract terms (defects liability provisions)
- **TBD**: Specific contract response time requirements and rectification obligations

## Verification

**VM-01**: Defect rectification completeness (all defects rectified or documented for post-defects-liability resolution)
**VM-02**: Employer acceptance (all rectified defects inspected and accepted by Employer)
**VM-03**: Defects register accuracy (all defects logged, status current, closure documentation complete)
**VM-04**: Contract compliance (response times met, warranty obligations fulfilled)

## Documentation

**Outputs**: Defect notification forms, rectification work orders, completion/test records, Employer acceptance sign-offs, warranty claim records, defects liability register, defects liability period closure report

**Management**: Records filed during defects liability period, compiled at period end, retained per contract (typically 2-3 years post-defects period for dispute resolution)

*See Procedure.md for detailed defects liability management process.*
