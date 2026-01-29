# Datasheet: DEL-35.05 Defects Liability Installation & Test Records

## Identification

| Field | Value |
|-------|-------|
| Deliverable ID | DEL-35.05 |
| Name | Defects Liability Installation & Test Records |
| Package | PKG-35 Training & Handover |
| Discipline | Project Delivery |
| Type | Record |
| Responsible | D&B Contractor (QA/QC) |
| Status | INITIALIZED |
| Project | Canola Oil Transload Facility — Phase 1 |
| Location | Fraser Surrey Terminal, 11060 Elevator Road, Surrey, BC |

*Source: _CONTEXT.md, Decomposition Section 5 (PKG-35)*

## Attributes

| Attribute | Value |
|-----------|-------|
| Record Purpose | Provides evidence of completion, inspection, and testing for defects liability — documenting defects identified during warranty period and their rectification |
| Record Category | Defects Liability (Warranty) Records |
| Defects Liability Period | **TBD** — Per Design & Build Contract (typically 12 months from Taking Over) |
| Period Commencement | Taking Over Date (cross-reference DEL-35.03) |
| Scope | All defects identified during defects liability period requiring Contractor rectification per contract warranty provisions |
| Record Format | **ASSUMPTION**: Defect notification forms, rectification work orders, completion/test records, Employer acceptance sign-offs |
| Record Number | **TBD** — Per project record management numbering system |
| Retention Period | **TBD** — **ASSUMPTION**: Minimum end of defects liability period plus dispute resolution period (typically 2-3 years post-defects period) |
| Classification | **ASSUMPTION**: Contractor Confidential / Client Proprietary |

*Source: **ASSUMPTION** based on typical Design & Build defects liability provisions; specific terms TBD per contract*

## Conditions

**Defects Liability Context:**

Defects liability records document defects discovered during the warranty period after handover (cross-reference DEL-35.03) and their rectification:
- **Defects liability period**: **TBD** (typically 12 months from Taking Over Date)
- **Defect definition**: Deficiencies in design, materials, or workmanship that manifest during defects liability period
- **Contractor responsibility**: Rectify defects at no cost to Employer (per contract warranty)
- **Exclusions**: Damage from Employer operations, misuse, or modifications (typically not Contractor responsibility)

*Source: **ASSUMPTION** — typical defects liability provisions; cross-reference DEL-35.03 Taking Over Certificate*

**Facility Context**: Canola oil transload facility (1,000,000 MT/annum, 45,000 MT storage) in operation during defects liability period

*Source: Decomposition Section 1.1 (Project Overview)*

**Operational Context During Defects Liability:**
- Facility is operational under Employer control
- Contractor access requires coordination with Employer operations (minimize disruption per **OBJ-5: Terminal Continuity**)
- Defect rectification must maintain facility safety (per **OBJ-1: Safe & Reliable Operation**)
- Defect rectification scheduling balances urgency vs. operational disruption

*Source: Decomposition Section 2 (OBJ-1, OBJ-5)*

**Outstanding Defects from Handover:**
- Outstanding defects list (punch list) from handover (cross-reference DEL-35.03) forms initial defects liability workload
- New defects may be discovered during operations

*Source: Cross-reference DEL-35.03 (Outstanding Defects List)*

## Construction

**Defects Liability Record Deliverables:**

Per _CONTEXT.md anticipated artifacts:
- **Defect rectification records**: Documentation of defects identified, rectification work performed, and completion verification
- **Warranty claim records**: Records of warranty claims, determinations, and resolutions

*Source: _CONTEXT.md (Anticipated Artifacts)*

**ASSUMPTION: Defect rectification records shall include:**

**1. Defect Notification Records**
- Defect identification (description, location, severity, safety impact)
- Discovery date and reported by (Employer notification to Contractor)
- Defect category (design deficiency, material defect, workmanship defect, equipment failure)
- Affected system/equipment
- Impact on operations (downtime, reduced capacity, safety hazard)
- Photographic evidence of defect

**2. Defect Assessment Records**
- Contractor assessment (root cause, rectification approach, estimated duration)
- Warranty determination (Contractor responsibility vs. Employer responsibility vs. OEM warranty)
- Urgency classification (immediate, urgent, routine)
- Rectification work scope and plan
- Required materials, equipment, personnel

**3. Defect Rectification Work Records**
- Work authorization (Employer approval for site access, work permit if required)
- Rectification work performed (date, personnel, activities)
- Materials used (replacement parts, consumables)
- Testing performed (functional test, performance test, safety test)
- Photographs (before/during/after rectification)
- Work completion certification (Contractor QA/QC sign-off)

**4. Defect Completion and Acceptance Records**
- Employer inspection of rectified defect
- Acceptance testing (if required)
- Employer acceptance sign-off (defect closed)
- Any follow-up actions or monitoring required
- Lessons learned (if significant defect)

**5. Warranty Claim Records**
- Warranty claim filed (by Employer against Contractor, or by Contractor against OEM/supplier)
- Claim description and justification
- Claim determination (accepted, rejected, disputed)
- Resolution (rectification by responsible party, negotiated settlement, dispute resolution)
- Claim closure documentation

**Defects Liability Management:**
- Defects liability register (master log of all defects, status, responsibility, target completion)
- Contractor response time tracking (per contract response/rectification time requirements)
- Employer satisfaction tracking (disputes, complaints, escalations)
- Defects liability period closure report (summary of defects rectified, outstanding items at period end)

*Source: **ASSUMPTION** — typical defects liability record content*

**Communication and Coordination:**
- Defect notification process (Employer to Contractor)
- Site access coordination (Contractor access to operational facility)
- Work scheduling (minimize operational disruption)
- Emergency response (safety-critical defects requiring immediate rectification)

*Source: **ASSUMPTION** — operational coordination during defects liability period*

## References

**Decomposition References:**
- Decomposition file: `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md` (Section 5, PKG-35, DEL-35.05)
- Project objectives: Decomposition Section 2 (OBJ-1: Safe & Reliable Operation, OBJ-5: Terminal Continuity, OBJ-9: Lifecycle Cost Optimization)
- Objective-to-deliverable mapping: Decomposition Section 6 (DEL-35.01–DEL-35.05 support OBJ-9)

**Reference Documents:**
- See `_REFERENCES.md` for applicable reference documents
- Design & Build Contract — **TBD**: Defects liability (warranty) clauses, response time requirements, rectification obligations
- Employer's Requirements Volume 2 Part 1, 2, 3 — **TBD**: Warranty requirements

**Cross-References:**
- **DEL-35.03 (Handover Documentation)**: Taking Over Certificate establishes defects liability period commencement; outstanding defects list from handover
- **Training deliverables (DEL-35.01, DEL-35.02)**: Training-related defects (if training inadequate) may be addressed during defects liability
- **All project deliverables**: Defects may relate to any facility system documented in project deliverables

**Applicable Standards:**
- **ASSUMPTION**: ISO 9001 (Quality Management — warranty management, customer satisfaction)
- **ASSUMPTION**: ISO 10002 (Customer Satisfaction — complaints handling)
- Design & Build Contract terms (defects liability provisions)

**Dependencies:**
- See `_DEPENDENCIES.md` (NOT_TRACKED — dependencies coordinated externally)
- **ASSUMPTION**: Defects liability records depend on:
  - Handover completion (DEL-35.03)
  - Facility operations commencement
  - Defect discovery during operations

*Source: Package scope and logical dependencies*
