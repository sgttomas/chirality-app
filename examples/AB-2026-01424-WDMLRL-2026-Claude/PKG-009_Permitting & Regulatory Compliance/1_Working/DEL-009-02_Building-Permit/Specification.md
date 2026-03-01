# Specification
## DEL-009-02 | Building Permit Application & Approval

---

## Scope

### In Scope

This deliverable covers the full lifecycle of the building permit for the WDMLRL Maintenance Shop Addition project:

- Preparation and assembly of the building permit application package for submission to Camrose County (R-01, §3.3.2; SOW-0006)
- Coordination with the Camrose County building authority throughout the review and approval process
- Receipt and documentation of the issued building permit
- Recording and tracking of all permit conditions and requirements
- Coordination of inspections required under the building permit (with County representative presence per SOW-0084, SOW-0085)
- Provision of copies of completed inspection reports to the County (SOW-0085)

### Out of Scope

- Payment of building permit fees — County responsibility (R-01, §3.3.1; SOW-0202)
- Development permit — addressed by DEL-009-01
- Safety Code permits — addressed by DEL-009-03
- Detailed code compliance tracking register — addressed by DEL-009-04 (Code Compliance Register & Inspection Log)
- Brushing, clearing, bulk cut and fill (County forces — R-01, §3.3.1)

---

## Requirements

### REQ-009-02-01: Permit Obligation
**Statement:** The Design-Builder shall obtain a building permit from Camrose County for the WDMLRL Maintenance Shop Addition.
**Source:** R-01, §3.3.2; SOW-0006
**Priority:** Mandatory

### REQ-009-02-02: Sequential Predecessor
**Statement:** The building permit application shall not be submitted until the Development Permit (DEL-009-01) has been obtained from Camrose County.
**Source:** _DEPENDENCIES.md (declared upstream dependency — DEL-009-01 is a critical sequential predecessor); _CONTEXT.md
**Priority:** Mandatory gate

### REQ-009-02-03: IFC Drawing Completeness
**Statement:** The building permit application package shall include complete IFC drawings signed and stamped by a professional engineer licensed to practice in the Province of Alberta, covering the following required design disciplines: architectural, structural, mechanical/HVAC, electrical, civil/site grading, and plumbing. (Lensing ref: C-002 — disciplines enumerated for specificity; cross-reference Procedure Phase 2 Step 4 and Datasheet Attributes.)
**Source:** R-01, §3.3.2; SOW-0018; Procedure.md Phase 2 Step 4 (discipline list)
**Priority:** Mandatory

### REQ-009-02-04: Code Compliance — Building Codes
**Statement:** The building design submitted with the permit application shall adhere to all applicable Alberta building codes and regulations.
**Source:** R-01, §3.3.2; SOW-0008
**Priority:** Mandatory

### REQ-009-02-05: Code Compliance — Safety Codes
**Statement:** The building design shall adhere to all applicable Alberta Safety Codes.
**Source:** R-01, §3.3.2; SOW-0009
**Priority:** Mandatory

### REQ-009-02-06: Inspection Request Submission
**Statement:** The Design-Builder shall submit all inspection requests required under the building permit.
**Source:** R-01, §3.3.2; SOW-0084
**Priority:** Mandatory

### REQ-009-02-07: County Representative at Inspections
**Statement:** The County project representative must be present at all inspections conducted under the building permit.
**Source:** R-01, §3.3.2; SOW-0084
**Priority:** Mandatory
**Note:** Coordination of County representative availability is a shared responsibility between Proponent and County; Proponent provides notice and coordinates timing. (Lensing ref: C-001 — Priority field added for consistency with other requirements.)

### REQ-009-02-08: Inspection Reports to County
**Statement:** Copies of all completed inspection reports shall be provided to the County.
**Source:** R-01, §3.3.2; SOW-0085
**Priority:** Mandatory

### REQ-009-02-09: Permit Conditions Incorporation
**Statement:** All conditions and requirements attached to the issued building permit shall be documented and incorporated into construction procedures and the Code Compliance Register (DEL-009-04).
**Source:** _CONTEXT.md (Success Criteria); _DEPENDENCIES.md (downstream — DEL-009-04)
**Priority:** Mandatory
**Note:** ASSUMPTION — specific mechanism for incorporation into construction procedures is not prescribed in sources; standard industry practice is to attach permit conditions to the site instructions and construction quality control program.

### REQ-009-02-10: Construction Commencement Gate
**Statement:** Construction shall not commence until the building permit has been issued and is in effect.
**Source:** _DEPENDENCIES.md (downstream dependency — Construction Phase is blocked by this deliverable); _CONTEXT.md
**Priority:** Mandatory gate

### REQ-009-02-11: Project Completion Deadline
**Statement:** The building permit must be obtained in sufficient time to allow all construction, commissioning, and closeout work to be completed on or before December 31, 2026.
**Source:** R-01, §3.1; SOW-0091
**Priority:** Mandatory schedule constraint

---

## Standards

| Standard / Code | Applicability | Accessibility |
|-----------------|---------------|---------------|
| Alberta Safety Codes Act (RSA 2000, c S-1) | Governing statute for Safety Codes in Alberta — building permit is issued under this framework | ASSUMPTION: likely applicable; specific text not reproduced in accessible sources — **blocking TBD: confirm exact citation and current amendments with Camrose County building authority or Alberta Municipal Affairs** (Lensing ref: F-001) |
| Alberta Building Code (current edition) | Prescribes minimum standards for building design and construction in Alberta | ASSUMPTION: likely applicable; specific edition not cited in accessible sources — **blocking TBD: confirm specific edition (e.g., ABC 2019 or later) with Camrose County building authority** (Lensing ref: F-001) |
| Camrose County Land Use Bylaw | Governs development and building permit requirements within the County | TBD — specific bylaw number and requirements not provided in accessible sources |
| CCDC 14-2013 | Design-Build Stipulated Price Contract form — contractual framework for the project | R-01, §2.7; SOW-0104 |
| Alberta OH&S Legislation | Prime Contractor obligations (SOW-0083); relevant to site inspection conditions | R-01, §2.15 |
| Accessibility standards | TBD — Applicable accessibility standards for a ~13,000 sq ft commercial/industrial structure in Alberta not yet enumerated. Confirm with building authority. (Lensing ref: B-002) | TBD — _REFERENCES.md lists as TBD |
| Fire safety requirements | TBD — Fire safety requirements for a concrete commercial/industrial structure with hazardous activities (welding, equipment fueling) not yet enumerated. Confirm with building authority. (Lensing ref: B-002) | TBD — _REFERENCES.md lists as TBD |
| Environmental / heritage overlays | TBD — Confirm whether environmental assessment, heritage overlay, or other municipal/provincial regulatory overlays apply to this site (SW 14-44-21-W4, Camrose County). For a new 13,000 sq ft structure on County land, additional regulatory checks (wetland, environmental, heritage) may apply. **Proposed authority: Camrose County planning department; Alberta Environment** (Lensing ref: F-002) | TBD — not addressed in accessible sources |

---

## Verification

| Requirement | Verification Approach |
|-------------|----------------------|
| REQ-009-02-01: Permit Obligation | Verify by receipt of issued building permit document from Camrose County |
| REQ-009-02-02: Sequential Predecessor | Verify that DEL-009-01 approval is documented before application is submitted |
| REQ-009-02-03: IFC Drawing Completeness | Verify that application package includes P.Eng.-stamped IFC drawings for all six enumerated disciplines (architectural, structural, mechanical/HVAC, electrical, civil/site grading, plumbing); check stamps and signatures against discipline checklist |
| REQ-009-02-04: Code Compliance — Building Codes | (a) Pre-submission: conduct explicit code compliance review of design documentation against applicable Alberta Building Code provisions prior to application submission. (b) Post-submission: verify by permit issuance (building authority confirms compliance). (Lensing ref: A-003 — pre-submission compliance check added to avoid circular reliance on permit issuance alone) |
| REQ-009-02-05: Code Compliance — Safety Codes | (a) Pre-submission: conduct explicit Safety Code compliance review of design documentation prior to application submission. (b) Post-submission: verify by permit issuance and Safety Code permit approvals (DEL-009-03). (Lensing ref: A-003 — pre-submission compliance check added to avoid circular reliance on permit issuance alone) |
| REQ-009-02-06: Inspection Request Submission | Verify by reviewing inspection request records and submission log in DEL-009-04 |
| REQ-009-02-07: County Representative at Inspections | Verify by signed inspection attendance records or inspection report sign-off by County representative |
| REQ-009-02-08: Inspection Reports to County | Verify by delivery receipt or acknowledgement from County; record in DEL-009-04 |
| REQ-009-02-09: Permit Conditions Incorporation | Verify by reviewing DEL-009-04 Code Compliance Register — all permit conditions entered and assigned |
| REQ-009-02-10: Construction Commencement Gate | Verify by checking that construction mobilization did not precede permit issuance date |
| REQ-009-02-11: Project Completion Deadline | Verify by defined schedule monitoring checkpoints: (a) establish target application submission date derived from required construction start date minus estimated authority processing time (TBD); (b) monitor at weekly project meetings (SOW-0086) with explicit escalation trigger if permit not received by [TBD — target date minus 2-week buffer]; (c) verify permit acquisition date against project schedule critical path. (Lensing ref: X-003 — specific monitoring mechanism replaces generic statement) |

### Anticipated Mandatory Inspection Stages

The following inspection stages are anticipated based on the building type (concrete commercial/industrial structure, ~13,000 sq ft). **All stages are TBD pending confirmation by Camrose County building authority upon permit issuance.** (Lensing ref: D-001)

| Inspection Stage | Typical Trigger | Status |
|------------------|----------------|--------|
| Foundation / footings | Prior to backfill | TBD — confirm with authority |
| Framing / structural | After structural frame erection | TBD — confirm with authority |
| Mechanical rough-in | Before concealment of mechanical systems | TBD — confirm with authority |
| Electrical rough-in | Before concealment of electrical systems | TBD — confirm with authority |
| Plumbing rough-in | Before concealment of plumbing systems | TBD — confirm with authority |
| Insulation / vapour barrier | Before concealment of insulation | TBD — confirm with authority |
| Final inspection | At substantial completion of construction | TBD — confirm with authority |

---

## Documentation

### Required Artifacts (Anticipated)

| Artifact | Description | Source |
|----------|-------------|--------|
| Building Permit Application Form | Completed application form(s) as prescribed by Camrose County building authority | R-01, §3.3.2; TBD (form sourced from authority) |
| IFC Drawing Set (all disciplines) | Stamped and signed IFC drawings — architectural, structural, mechanical, electrical, civil, plumbing | R-01, §3.3.2; SOW-0018 |
| Site Grading Plan | Required as part of application — must account for positive drainage and not alter neighboring properties | R-01, §3.3.2; SOW-0015, SOW-0020, SOW-0021 |
| Issued Building Permit | Official permit document issued by Camrose County | SOW-0006 |
| Permit Conditions Summary | Documented list of all conditions attached to issued permit | _CONTEXT.md (Success Criteria) |
| Inspection Submission Records | Log of all inspection requests submitted | R-01, §3.3.2; SOW-0084 |
| Completed Inspection Reports | Copies of all inspection reports from inspections conducted under permit | R-01, §3.3.2; SOW-0085 |
| Permit Conditions in DEL-009-04 | Permit conditions entered into Code Compliance Register (DEL-009-04) | _DEPENDENCIES.md (downstream) |
| Pre-submission Code Compliance Review | Record of pre-submission review confirming design documentation compliance with applicable Alberta Building Code and Safety Codes (Lensing ref: A-003) | REQ-009-02-04, REQ-009-02-05; Procedure Step 7 |
