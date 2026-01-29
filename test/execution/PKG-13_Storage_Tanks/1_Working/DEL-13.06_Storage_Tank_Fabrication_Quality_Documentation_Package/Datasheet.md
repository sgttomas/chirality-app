# Datasheet: DEL-13.06 Storage Tank Fabrication Quality Documentation Package

## Identification

| Field | Value |
|-------|-------|
| **Deliverable ID** | DEL-13.06 |
| **Deliverable Name** | Storage Tank Fabrication Quality Documentation Package |
| **Package** | PKG-13 Storage Tanks |
| **Discipline** | Mechanical |
| **Type** | Document Package |
| **Responsible Party** | D&B Contractor |
| **Status** | INITIALIZED |

**Source:** `_CONTEXT.md`

---

## Attributes

### Document Package Configuration

| Attribute | Value | Source |
|-----------|-------|--------|
| **Number of Tanks** | 3 | Decomposition Section 1.1 (3 × 15,000 MT tanks) |
| **Package Scope** | Shop inspection reports, MTRs, impact test results, NDE reports, WPS/PQR/WPQ, weld inspection records | _CONTEXT.md (Anticipated Artifacts) |
| **Package Purpose** | Demonstrate fabricator qualification and fabrication quality compliance with API 650 and CSA W59 | ASSUMPTION: Based on typical fabrication quality documentation purpose |
| **Package Format** | **TBD** — Per project document management requirements (likely indexed PDF dossier) | |
| **Retention Period** | **TBD** — Requires ER extraction (typically facility lifetime for fabrication quality records) | |

### Shop Inspection Reports

| Attribute | Value | Source |
|-----------|-------|--------|
| **Report Scope** | Third-party or D&B Contractor QA inspection of fabricator's shop during tank fabrication | Typical shop inspection practice for API 650 tanks |
| **Inspection Frequency** | **TBD** — Daily, weekly, or milestone-based inspection per ITP (DEL-29.02) | |
| **Quantity** | **TBD** — Depends on fabrication duration and inspection frequency (estimated 10-30 reports per tank) | |
| **Content Requirements** | Date, inspector name, fabrication activities observed, conformance observations, non-conformances identified, corrective actions, sign-off | Typical shop inspection report format |
| **Inspector Qualification** | **TBD** — Requires ER extraction (typically CWB certified welding inspector or equivalent) | |

### Material Test Reports (MTRs)

| Attribute | Value | Source |
|-----------|-------|--------|
| **Scope** | Mill Test Reports for all pressure-retaining and structural materials | API 650 Section 2.2 material requirements |
| **Quantity** | **TBD** — Estimated 50-100 MTRs total for 3 tanks | |
| **Content** | Material specification, heat number, chemical composition, mechanical properties, test results, certifier signature | Standard MTR format |
| **Note** | MTRs are also part of DEL-13.05 (Installation & Test Records); included in fabrication quality package for fabricator qualification documentation | Typical documentation practice (MTRs appear in multiple deliverables) |

### Impact Test Results

| Attribute | Value | Source |
|-----------|-------|--------|
| **Scope** | Charpy V-notch impact test results for materials requiring low-temperature toughness verification | API 650 Section 2.2.11 (if applicable) |
| **Applicability** | **TBD** — Required if tank operates below -29°C or if specified by ER for seismic design | API 650 Section 2.2.11; API 650 Appendix E seismic requirements |
| **Quantity** | **TBD** — Depends on material specification and operating temperature (3-5 tests per heat for applicable materials) | |
| **Content Requirements** | Material heat number, test temperature, test specimen orientation, impact energy values (3 specimens per test), acceptance criteria, test lab certification | ASTM A370 impact test reporting requirements |
| **Acceptance Criteria** | **TBD** — Per API 650 Section 2.2.11 or project specification (DEL-13.02) | |

### NDE Reports (Fabrication)

| Attribute | Value | Source |
|-----------|-------|--------|
| **Scope** | Non-Destructive Examination reports generated during shop fabrication | API 650 Section 8 NDE requirements |
| **Quantity** | **TBD** — Estimated 60-150 NDE reports total for 3 tanks | |
| **Content** | NDE method, procedure, weld joint ID, acceptance criteria, results, technician certification, sign-off | Standard NDE report format |
| **Note** | NDE reports are also part of DEL-13.05 (Installation & Test Records); included in fabrication quality package to demonstrate fabrication process quality control | Typical documentation practice (NDE reports appear in multiple deliverables) |

### Welding Procedure Specifications (WPS)

| Attribute | Value | Source |
|-----------|-------|--------|
| **Scope** | Qualified welding procedures for all weld types used in tank fabrication | API 650 Section 8.2 / CSA W59 Section 5 welding procedure requirements |
| **Quantity** | **TBD** — Estimated 3-10 WPS depending on material types, thicknesses, joint configurations, welding processes | |
| **Content Requirements** | Base metal specification and thickness range, filler metal specification, welding process (SMAW, GMAW, FCAW, SAW), joint design, preheat/interpass temperature, heat input, post-weld heat treatment (if applicable), qualification reference (PQR number) | API 650 Section 8.2 / CSA W59 Section 5.1 |
| **Qualification Standard** | API 650 Section 8.2 and/or CSA W59 Section 5 | Decomposition PKG-13 Scope (API 650); ASSUMPTION (CSA W59 for Canadian project) |
| **WPS Approval** | **TBD** — Requires D&B Contractor review and approval before use; may require client review per ER | |

### Procedure Qualification Records (PQR)

| Attribute | Value | Source |
|-----------|-------|--------|
| **Scope** | Test results demonstrating welding procedure adequacy (qualification test welds) | API 650 Section 8.2 / CSA W59 Section 5 procedure qualification requirements |
| **Quantity** | **TBD** — One PQR per WPS (estimated 3-10 PQRs) | |
| **Content Requirements** | Test coupon description, welding parameters actually used, test results (visual, NDE, bend tests, tensile tests, impact tests if required), acceptance criteria, test lab certification, test date and witness | API 650 Section 8.2.4 / CSA W59 Section 5.2 |
| **Test Requirements** | Minimum tests: Visual examination, radiographic or ultrasonic examination, tensile test, guided bend test (side or face bends); impact tests if low-temperature service | API 650 Section 8.2.4 / CSA W59 Section 5.2 |
| **PQR Certification** | **TBD** — PQR certified by qualified welding engineer or CWB testing facility | |

### Welder Qualification Records (WPQ)

| Attribute | Value | Source |
|-----------|-------|--------|
| **Scope** | Test results demonstrating individual welder skill and qualification | API 650 Section 8.2.5 / CSA W59 Section 6 welder qualification requirements |
| **Quantity** | **TBD** — One WPQ per welder per qualified process and position (estimated 5-20 welders, 10-40 WPQs total) | |
| **Content Requirements** | Welder name and identification, welding process qualified, material type and thickness qualified, joint type and position qualified, test coupon configuration, test results (visual, NDE, bend test), test date and witness | API 650 Section 8.2.5 / CSA W59 Section 6 |
| **Test Requirements** | Visual examination, radiographic or ultrasonic examination, guided bend test | API 650 Section 8.2.5 / CSA W59 Section 6.2 |
| **Qualification Validity** | WPQ remains valid as long as welder is actively welding similar work; re-qualification required after 6-month absence or if weld quality is questionable | API 650 Section 8.2.5 / CSA W59 Section 6.4 |

### Weld Inspection Records

| Attribute | Value | Source |
|-----------|-------|--------|
| **Scope** | In-process weld inspection records documenting visual inspection and acceptance of welds during fabrication | API 650 Section 8 / CSA W59 Section 12 inspection requirements |
| **Quantity** | **TBD** — Depends on inspection frequency and number of welds (may be included in shop inspection reports) | |
| **Content Requirements** | Weld joint ID, visual inspection criteria (undercut, porosity, spatter, profile), acceptance/rejection, inspector signature, date | API 650 Section 8 / CSA W59 Section 12 visual inspection requirements |
| **Note** | Weld inspection records may be combined with shop inspection reports or documented separately on weld traveler forms | Typical fabrication QA practice |

---

## Conditions

### Fabricator Qualification and Selection

| Condition | Value | Source |
|-----------|-------|--------|
| **Fabricator Qualification Requirements** | **TBD** — Fabricator shall be qualified per API 650 requirements or equivalent; may require CSA W47.1 certification for welding | API 650 fabricator requirements; ASSUMPTION (CSA W47.1 for Canadian project) |
| **Fabricator Selection Timing** | Fabricator shall be selected and qualified before fabrication documentation package is finalized | Typical procurement sequence |
| **Shop Audit** | **TBD** — D&B Contractor or third-party may audit fabricator shop before fabrication begins to verify quality systems | Typical fabricator qualification process |

### Documentation Package Submission Timing

| Condition | Value | Source |
|-----------|-------|--------|
| **Pre-Fabrication Submission** | WPS/PQR/WPQ submitted and approved before fabrication begins | API 650 and typical QA workflow (procedures qualified before production welding) |
| **During-Fabrication Submission** | Shop inspection reports, MTRs, impact test results, NDE reports submitted progressively during fabrication | Typical fabrication QA workflow |
| **Post-Fabrication Submission** | Complete fabrication quality documentation package compiled and submitted after fabrication complete | Typical final documentation workflow |

### Document Package Retention and Archive

| Condition | Value | Source |
|-----------|-------|--------|
| **Retention Period** | **TBD** — Requires ER extraction (typically facility lifetime) | |
| **Archive Format** | **TBD** — Electronic and/or hard copy per project document control procedures | |
| **Archive Location** | **TBD** — Project document management system and/or client archive | |

---

## Construction

### Document Package Production Workflow

| Item | Description | Source |
|------|-------------|--------|
| **WPS/PQR/WPQ Development** | Fabricator develops and qualifies welding procedures and welders; submits WPS/PQR/WPQ to D&B Contractor for review and approval | Typical welding qualification workflow |
| **Shop Inspection** | D&B Contractor QA or third-party inspector conducts shop inspections; generates shop inspection reports | Typical shop inspection workflow |
| **Material Certificate Collection** | Fabricator receives MTRs from material suppliers; provides copies to D&B Contractor QA | Typical material procurement and traceability workflow |
| **Impact Testing** | If required, material supplier or independent test lab performs impact tests; provides impact test results | Typical impact testing workflow (if applicable) |
| **NDE Examination** | Fabricator's NDE technician or third-party NDE service performs examinations; generates NDE reports | API 650 NDE workflow |
| **Weld Inspection** | Fabricator's or D&B Contractor's welding inspector performs in-process visual inspections; documents on shop inspection reports or weld traveler forms | Typical in-process inspection workflow |

### Document Package Organization

| Document Category | Organization | Source |
|-------------------|--------------|--------|
| **Package-Level Documents** | WPS, PQR, WPQ organized in separate section (applicable to all tanks) | Typical documentation organization |
| **Tank-Specific Documents** | Shop inspection reports, MTRs, impact test results, NDE reports, weld inspection records organized by tank | Typical documentation organization |
| **Index** | Comprehensive index cross-referencing all documents in package | Typical document package practice |

### Document Package Validation

| Item | Description | Source |
|------|-------------|--------|
| **WPS/PQR/WPQ Review** | D&B Contractor welding engineer reviews WPS/PQR/WPQ for compliance with API 650/CSA W59 and project specification (DEL-13.02) | Typical welding procedure approval process |
| **Shop Inspection Report Review** | D&B Contractor QA manager reviews shop inspection reports for completeness and conformance tracking | Typical QA review process |
| **Material Certificate Review** | D&B Contractor QA engineer reviews MTRs for material specification compliance | Typical material acceptance process |
| **Impact Test Result Review** | D&B Contractor QA engineer reviews impact test results for acceptance criteria compliance (if applicable) | Typical impact test review process |
| **NDE Report Review** | D&B Contractor QA engineer reviews NDE reports for acceptance criteria compliance and technician qualification | Typical NDE review process |
| **Final Package Compilation** | D&B Contractor QA compiles all documents into fabrication quality documentation package, indexes, reviews for completeness | Typical documentation compilation process |

---

## References

### Source Documents

1. `_CONTEXT.md` — Deliverable identity, description, anticipated artifacts
2. Decomposition document (`/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md`):
   - Section 1.1 (Project Overview — Key Parameters): Storage capacity (3 × 15,000 MT tanks)
   - Section 5, PKG-13: Scope (API 650 tanks)
   - Section 5, DEL-13.06: Description and anticipated artifacts
3. `_REFERENCES.md` — Reference index (ER PDFs location TBD)

### Expected Reference Documents (TBD — ER Extraction Pending)

1. Volume 2 Part 2: Employer's Requirements - Civil & Process Mechanical Works — **Location TBD**
2. API 650: Welded Tanks for Oil Storage — **Location TBD** (Section 2.2 Materials, Section 8 Welding)
3. CSA W59: Welded Steel Construction (Metal Arc Welding) — **Location TBD** (ASSUMPTION: applicable for Canadian project)
4. CSA W47.1: Certification of Companies for Fusion Welding of Steel — **Location TBD** (ASSUMPTION: fabricator certification requirement)
5. ASTM A370: Standard Test Methods and Definitions for Mechanical Testing of Steel Products — **Location TBD** (impact testing methods)
6. ASNT SNT-TC-1A or ISO 9712: NDE Personnel Qualification and Certification — **Location TBD**

### Related Deliverables

| Deliverable | Relationship |
|-------------|-------------|
| DEL-13.01: Storage Tank Design Drawing Set | Design drawings provide basis for fabrication and inspection |
| DEL-13.02: Storage Tank Technical Specification | Specification defines material requirements, welding requirements, fabrication quality requirements |
| DEL-13.03: Storage Tank Design Calculations | Calculations define design basis and performance requirements |
| DEL-13.04: Storage Tank Data Sheet Package | Data sheets reference fabrication quality documentation |
| DEL-13.05: Storage Tank Installation & Test Records | Installation and test records reference WPS/PQR/WPQ and include MTRs and NDE reports (overlap between deliverables) |
| DEL-29.02: Inspection and Test Plan With Hold/Witness Points | ITP defines hold/witness points for welding procedure approval, welder qualification, shop inspections |

---

## Cross-Document References

**For detailed requirements:** See `Specification.md`
- FR-01: WPS/PQR/WPQ Requirements → WPS, PQR, WPQ attributes
- FR-02: Shop Inspection Requirements → Shop Inspection Reports attributes
- FR-03: Material Documentation Requirements → MTRs, Impact Test Results attributes
- FR-04: NDE Documentation Requirements → NDE Reports attributes
- FR-05: Weld Inspection Requirements → Weld Inspection Records attributes

**For fabrication quality documentation rationale:** See `Guidance.md`
- DP-01: Fabricator Qualification Philosophy → Package purpose and value
- DP-02: Welding Procedure Qualification → WPS/PQR/WPQ principles
- DP-03: API 650 and CSA W59 Compliance Documentation → Standards compliance requirements
- Trade-offs → Documentation depth, third-party vs. self-inspection decisions

**For document package production workflow:** See `Procedure.md`
- Steps 1-6 → Produce WPS/PQR/WPQ, shop inspection reports, material documentation, NDE documentation, weld inspection records documented here
- Step 7 → Compile and validate document package
- Step 8 → Submit for approval and archive

---

**Document Status:** Pass 3 (Final) — Enrichment complete. Cross-document consistency verified. All TBDs marked for ER extraction and execution planning. ASSUMPTIONs labeled. Ready for WORKING_ITEMS refinement.

**Last Updated:** 2026-01-28
