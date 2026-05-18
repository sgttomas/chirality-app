# Specification — DEL-008-03 Construction Survey

**Document Type:** Specification (normative)
**Deliverable:** DEL-008-03 Construction Survey
**Package:** PKG-008 Geotechnical Investigation & Surveying
**Project:** 2026 Design Build — West Dried Meat Lake Regional Landfill Maintenance Shop Addition
**Revision:** Pass 3 — 2026-02-26

---

## Scope

### What This Specification Covers

This specification governs the Construction Survey (DEL-008-03) for the West Dried Meat Lake Regional Landfill (WDMLRL) Maintenance Shop Addition. It defines the requirements for the field survey work that establishes control, positions, grades, and alignment enabling construction of the addition at SW 14–44–21–W4, near Ferintosh, Alberta.

The construction survey covers:
- Establishment and documentation of horizontal and vertical control network for the construction site
- Layout and alignment survey translating IFC drawings to the field
- Grade establishment supporting slab-on-grade, site grading, and drainage design
- Construction staking for all major building elements and site features
- Field verification of constructed positions against design intent
- Progress survey updates throughout the construction phase
- Preparation of field documentation and survey records

**Source:** _CONTEXT.md (Scope, Description); WDMLRL_Decomposition_Claude.md §3 (SOW-0003); RFP §3.3.2

### What This Specification Excludes

- Geotechnical investigation scope (DEL-008-01)
- Preliminary survey scope (DEL-008-02)
- As-built survey scope (DEL-008-04)
- Foundation design calculations (DEL-002-11, PKG-002)
- Civil grading design (PKG-005)
- Construction execution of any element (PKG-010 through PKG-018)

---

## Requirements

### REQ-008-03-01: Survey Must Derive from Preliminary Survey Control

The construction survey shall use the control points, benchmarks, and baseline data established by DEL-008-02 (Preliminary Site Survey) as its primary horizontal and vertical reference. All survey work shall be performed on the geodetic datum, map projection, and vertical datum established by DEL-008-02 (TBD — see Datasheet Key Site Information; **ASSUMPTION**: NAD83(CSRS), UTM Zone 12N, CGVD2013 per standard Alberta practice).

**Rationale:** Continuity of control between preliminary and construction survey is necessary to ensure design-to-field traceability. A declared coordinate reference system is fundamental to the authoritative standing of all spatial data in this deliverable. [Lensing items E-001, B-003]
**Source:** _DEPENDENCIES.md (upstream: DEL-008-02); _REFERENCES.md (Related Deliverables); Surveyor / DEL-008-02 (**location TBD** for datum confirmation)
**Verification:** Surveyor shall document control point provenance in field notes, including the geodetic datum, projection, and vertical datum used.

### REQ-008-03-02: IFC Drawings Required Before Staking

Construction staking shall not commence until P.Eng.-stamped Issued for Construction (IFC) drawings are available for the element being staked.

**Rationale:** RFP §3.3.2 requires all IFC drawings to be signed and stamped by a professional engineer licensed in Alberta. Staking from unapproved drawings creates rework risk.
**Source:** RFP §3.3.2; WDMLRL_Decomposition_Claude.md §3 (SOW-0018)
**Verification:** Surveyor shall record the drawing revision/stamp reference for each staking activity.

### REQ-008-03-03: Layout and Alignment for All Major Building Elements

The construction survey shall lay out and stake the following elements consistent with the IFC drawings:

| Element | Source Requirement |
|---------|-------------------|
| Building footprint and column grid | RFP §3.1, §3.4; Appendix B (Shop) |
| Two drive-through repair bays (24 ft wide bays per conceptual drawing) | RFP §3.1; WDMLRL_Decomposition_Claude.md SOW-0025 |
| Enclosed wash bay (single bay, motor scraper-sized) | RFP §3.4; WDMLRL_Decomposition_Claude.md SOW-0027a |
| Service pit / trench location and grade | RFP §3.4; WDMLRL_Decomposition_Claude.md SOW-0028 |
| Foundation extents | RFP §3.4; WDMLRL_Decomposition_Claude.md SOW-0023 |
| Cistern location and invert grades | RFP §3.4; WDMLRL_Decomposition_Claude.md SOW-0041 |
| Cement pads (per conceptual drawings) | Appendix B (Shop); WDMLRL_Decomposition_Claude.md SOW-0078 |
| Gravel driving surface alignment and grades | RFP §3.3.2, §3.4; WDMLRL_Decomposition_Claude.md SOW-0077 |
| Mud sump (exterior, wash bay) | RFP §3.4; WDMLRL_Decomposition_Claude.md SOW-0027b |
| Utility corridors (gas, electrical, communications tie-in) | RFP §3.3.2; WDMLRL_Decomposition_Claude.md SOW-0080–0082 |
| Septic holding tank location | RFP §3.4; WDMLRL_Decomposition_Claude.md SOW-0043 |

**Note:** Exact bay dimensions, pad dimensions, and invert elevations are subject to IFC drawings; the conceptual dimensions above are from Appendix B and RFP §3.4 and shall be superseded by IFC drawings when available.

**Source:** RFP §3.1, §3.3.2, §3.4; Appendix B (Shop); WDMLRL_Decomposition_Claude.md §3 (SOW-0003, SOW-0022–0031, SOW-0041–0043, SOW-0075–0079)
**Verification:** Field staking records shall reference the IFC drawing sheet and revision for each element.

### REQ-008-03-04: Grade Establishment Supporting Positive Drainage

The construction survey shall establish grade control consistent with the civil grading design, such that:
- Positive drainage is directed away from the building and site features
- Drainage conditions of neighbouring properties are not altered

**Discrepancy resolution:** Discrepancies between survey grade control and the civil grading design shall be reported to the civil design engineer and construction manager. The Construction Manager shall have authority to accept, reject, or require remediation of discrepancies, in consultation with the civil design engineer. Work in the affected area shall not proceed until the discrepancy is resolved and the resolution is documented. **ASSUMPTION**: Construction Manager holds resolution authority per the CCDC 14-2013 contract structure; this should be confirmed. [Lensing item X-004]

**Source:** RFP §3.4; WDMLRL_Decomposition_Claude.md §3 (SOW-0020, SOW-0021); CCDC 14-2013 (**location TBD** for dispute resolution authority)
**Verification:** Grade control points shall be compared against civil grading design elevations; discrepancy reports shall document the measured vs. design values, the resolution authority's decision, and the corrective action taken (if any).

### REQ-008-03-05: Grade Control for Topsoil Stripping Surfaces

The construction survey shall establish reference grades for all driving surfaces subject to topsoil stripping, to enable the contractor to achieve correct subgrade elevations prior to gravel surfacing.

**Source:** RFP §3.3.2 (strip topsoil from all driving surfaces); WDMLRL_Decomposition_Claude.md §3 (SOW-0075)
**Note:** County is responsible for bulk cut and fill; surveyor provides grade references only.
**Verification:** Subgrade grades verified by survey before gravel placement.

### REQ-008-03-06: Field Verification During Construction

The Surveyor shall conduct field verification checks to confirm that constructed elements (foundations, slabs, walls, pads) are positioned and graded within the tolerances established in the Construction Survey Plan.

**Accuracy Tolerances:** TBD — specific horizontal and vertical construction survey tolerances shall be defined by the licensed Surveyor consistent with Alberta survey practice standards and the precision required by the structural and civil design. No specific tolerance is stated in the RFP or decomposition. [Lensing item A-001: this TBD is a critical gap; prescriptive direction is incomplete without defined tolerances]

**Normative obligation:** The Construction Survey Plan shall define the accuracy tolerances to be applied. The tolerances in the Construction Survey Plan constitute the pass/fail criteria for all field verification checks under this requirement. The Surveyor holds professional discretion to set tolerances consistent with Alberta survey practice, but the Construction Survey Plan must be produced and approved before field verification checks are assessed as pass/fail. [Lensing items A-002, C-001, X-001: closes the circular reference where tolerances depend on a plan that was not itself required]

**Source:** _CONTEXT.md (Scope — "Field verification and documentation"); SOW-0003; Licensed Surveyor / Alberta survey practice standards (**location TBD**)
**Verification:** Verification check records shall be retained as field documentation; records shall reference the tolerance values from the approved Construction Survey Plan and include explicit pass/fail determination for each checked element.

### REQ-008-03-06a: Construction Survey Plan Required Before Field Work

The Surveyor shall prepare a Construction Survey Plan (as described in Procedure Step A3) defining the control network, survey methodology, accuracy tolerances, and milestone schedule. The Construction Survey Plan shall be reviewed and approved by the Design-Builder and/or Construction Manager before field survey work commences. Field staking and verification activities shall not proceed without an approved Construction Survey Plan.

**Rationale:** REQ-008-03-06 delegates tolerance definition to the Construction Survey Plan, and Procedure Step A3 describes creating it, but without a requirement mandating its production and approval the obligation chain is broken. This requirement closes that gap. [Lensing item F-001]
**Source:** Specification REQ-008-03-06; Procedure Step A3; Design-Builder / Construction Manager (**ASSUMPTION**: approval authority inferred from contract structure)
**Verification:** Approved Construction Survey Plan on file before first field staking activity; approval record retained.

### REQ-008-03-07: Progress Survey Updates

The Surveyor shall perform periodic progress surveys during the construction phase to verify positional compliance of ongoing work with the IFC drawings.

**Frequency:** TBD — to be established in the Construction Survey Plan or construction schedule. [Lensing item F-004: terminology normalized]
**Source:** _CONTEXT.md (Scope — "Progress survey updates"); MEMORY.md
**Verification:** Progress survey records shall be filed and made available to the construction manager.

### REQ-008-03-08: Field Documentation and Records

All survey field notes, control point records, staking records, grade sheets, and verification checks shall be documented and retained.

**Minimum content for field verification records:** Each field verification record shall include, at minimum: date of verification, surveyor name and license number, instrument(s) used, IFC drawing reference (sheet number and revision), element being verified, measured values (position and/or elevation), design values, tolerance applied, and pass/fail determination. **ASSUMPTION**: minimum content list is based on standard construction survey record practice; the Surveyor may supplement with additional fields as required by Alberta professional standards. [Lensing item E-003]

**Source:** _CONTEXT.md (Scope — "Field verification and documentation"); Licensed Surveyor / Alberta survey practice standards (**location TBD**)
**Verification:** Documentation package available for review upon request; records reviewed for completeness against the minimum content requirements above.

### REQ-008-03-08a: Survey Record Retention

All survey records produced under REQ-008-03-08 shall be retained for a period consistent with the contract guarantee period (RFP §2.10) and applicable Alberta professional surveying obligations (Alberta Land Surveyors Act, RSA 2000, c. A-31.5).

**Retention period:** TBD — to be confirmed based on the CCDC 14-2013 guarantee period terms and Alberta Land Surveyors' professional record retention requirements. **ASSUMPTION**: the contract guarantee period (RFP §2.10) implies a minimum retention period equal to the guarantee duration, and professional obligations may require longer retention.
**Rationale:** REQ-008-03-08 requires documentation but does not address how long records must be kept. The guarantee period may impose an implied retention need for defect-resolution purposes. [Lensing item C-002]
**Source:** RFP §2.10 (guarantee period); CCDC 14-2013 (**location TBD** for specific retention clauses); Alberta Land Surveyors Act (**location TBD**)
**Verification:** Retention policy documented in the Construction Survey Plan or separate records management plan.

### REQ-008-03-08b: Control Point Data Chain-of-Custody

The Surveyor shall maintain a documented chain-of-custody for control point data, covering:
- Receipt of control data from DEL-008-02 (Preliminary Site Survey): date received, source surveyor, data format, and datum confirmation
- Any modifications to the control network during construction survey work: date, reason, new coordinates, and verification check results
- Transfer of control data to DEL-008-04 (As-Built Survey): date transferred, recipient, data format, and datum confirmation

**Rationale:** Provenance documentation for control data supports audit traceability and ensures that any spatial discrepancy can be traced to its origin. [Lensing item E-004]
**Source:** Specification REQ-008-03-01 (control from DEL-008-02); Procedure Steps A1, D3; _DEPENDENCIES.md (upstream/downstream); Surveyor (**ASSUMPTION**: chain-of-custody documentation is standard professional practice)
**Verification:** Chain-of-custody record reviewed as part of the documentation package (REQ-008-03-08).

### REQ-008-03-09: Completion Deadline

All construction survey activities required to support construction completion must be completed such that construction can complete on or before December 31, 2026.

**Source:** RFP §3.1 (bold statement: "All Work pertaining to the Design Build of West Dried Meat Lake Regional Landfill Maintenance Shop Addition must be completed on or before December 31, 2026."); WDMLRL_Decomposition_Claude.md §5 (OBJ-002)
**Verification:** Survey activity milestones shall be identified in the Construction Survey Plan and tracked against the construction schedule (PKG-019). The Surveyor shall report survey schedule status to the Construction Manager at intervals defined in the Construction Survey Plan. Deviations from the planned survey schedule shall be reported promptly with an assessment of impact on the construction critical path. [Lensing item D-001: strengthens the previously vague verification approach]

### REQ-008-03-10: Coordination with County Project Manager

Survey activities, inspection requests, and scheduling shall be coordinated through the County project manager.

**Source:** RFP §3.1, §3.3.2 (submit all inspection requests; County representative present at all inspections; provide copies of inspection reports)
**Verification:** Communication records maintained.

---

## Standards

The following standards and regulatory frameworks are expected to govern construction survey practice for this deliverable. Specific clause-level requirements are TBD pending confirmation of the applicable standard suite with the licensed Surveyor. [Lensing items A-003, F-002: compliance determination cannot be performed until the Surveyor confirms the applicable standards and specific clause-level requirements. The ASSUMPTION tags below should be resolved to confirmed applicability or removed once the Surveyor reviews this section.]

| Standard / Framework | Status | Source |
|---------------------|--------|--------|
| Alberta Land Surveyors Act (RSA 2000, c. A-31.5) | ASSUMPTION: likely applicable — construction survey in Alberta performed under professional surveying obligations | location TBD |
| Alberta Survey Standards and professional practice requirements | ASSUMPTION: likely applicable — specific accuracy and documentation standards for construction surveys in Alberta | location TBD |
| CCDC 14–2013 Design-Build Stipulated Price Contract (general conditions) | Applicable — contract form governing the project; Surveyor is a subcontractor under the Design-Builder | RFP §2.7; WDMLRL_Decomposition_Claude.md §5 (OBJ-006) |
| Alberta OH&S and Prime Contractor obligations | Applicable — Surveyor working on site is subject to the Prime Contractor's OH&S framework | RFP §2.15; WDMLRL_Decomposition_Claude.md §3 (SOW-0083) |
| Alberta building codes and regulations (general) | Applicable by reference — the survey must support compliance with applicable building codes | RFP §3.3.2; WDMLRL_Decomposition_Claude.md §3 (SOW-0008) |

---

## Verification

| Requirement | Verification Approach |
|-------------|----------------------|
| REQ-008-03-01: Control from DEL-008-02 | Review field notes for control point provenance documentation |
| REQ-008-03-02: IFC drawings before staking | Review staking records for drawing reference entries |
| REQ-008-03-03: Layout and alignment completeness | Cross-check staking records against IFC drawing element list |
| REQ-008-03-04: Positive drainage grades | Compare survey grade control points with civil grading design; review report of discrepancies |
| REQ-008-03-05: Subgrade grades for driving surfaces | Review grade sheets before gravel placement |
| REQ-008-03-06: Field verification checks | Review verification check records; compare to tolerances in approved Construction Survey Plan; confirm each record includes pass/fail determination |
| REQ-008-03-06a: Construction Survey Plan required | Confirm approved Construction Survey Plan on file before first field staking activity; verify approval record exists |
| REQ-008-03-07: Progress survey updates | Review progress survey records; confirm frequency matches schedule |
| REQ-008-03-08: Field documentation | Documentation package review; verify records meet minimum content requirements |
| REQ-008-03-08a: Record retention | Confirm retention policy documented in Construction Survey Plan or records management plan |
| REQ-008-03-08b: Control point chain-of-custody | Review chain-of-custody record for control data receipt (DEL-008-02), modifications, and transfer (DEL-008-04) |
| REQ-008-03-09: Completion deadline | Track survey milestones against construction schedule per Construction Survey Plan; review schedule status reports |
| REQ-008-03-10: Coordination | Review communication records with County project manager |

---

## Documentation

The following artifacts are anticipated from the construction survey. The specific format and detail level shall be as agreed between the Surveyor and the Design-Builder/Construction Manager.

| Artifact | Description |
|----------|-------------|
| Construction Survey Plan | Describes the control network, methodology, accuracy targets, and schedule for survey activities |
| Field Notes | Raw field survey observations and measurements |
| Control Network Documentation | Description and coordinates of all established control points and benchmarks |
| Staking Records | Records of each staking activity, referencing the IFC drawing element |
| Grade Sheets | Cut-and-fill tables or grade control records for site grading and pavement areas |
| Field Verification Records | Checks of constructed elements against design positions/grades |
| Progress Survey Records | Periodic survey records through construction |
| Construction Survey Report | Summary report (if required by construction manager or County) |

**Source:** _CONTEXT.md (Anticipated artifacts — field documentation); standard construction survey practice (ASSUMPTION for artifact names and formats not explicitly stated in RFP)
