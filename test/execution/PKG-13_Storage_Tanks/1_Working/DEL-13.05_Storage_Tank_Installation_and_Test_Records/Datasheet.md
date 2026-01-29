# Datasheet: DEL-13.05 Storage Tank Installation & Test Records

## Identification

| Field | Value |
|-------|-------|
| **Deliverable ID** | DEL-13.05 |
| **Deliverable Name** | Storage Tank Installation & Test Records |
| **Package** | PKG-13 Storage Tanks |
| **Discipline** | Mechanical |
| **Type** | Record |
| **Responsible Party** | D&B Contractor (QA/QC) |
| **Status** | INITIALIZED |

**Source:** `_CONTEXT.md`

---

## Attributes

### Record Package Configuration

| Attribute | Value | Source |
|-----------|-------|--------|
| **Number of Tanks** | 3 | Decomposition Section 1.1 (3 × 15,000 MT tanks) |
| **Record Package Scope** | Material certificates, weld maps, NDE reports, hydrostatic test records | _CONTEXT.md (Anticipated Artifacts) |
| **Package Format** | **TBD** — Per project document management requirements (likely PDF dossier or indexed folder) | |
| **Retention Period** | **TBD** — Requires ER extraction (typically facility lifetime for as-built quality records) | |
| **Record Classification** | Quality Records — Evidence of compliance with API 650 and project specifications | ASSUMPTION: Based on record purpose |

### Material Certificates

| Attribute | Value | Source |
|-----------|-------|--------|
| **Certificate Types** | Mill Test Reports (MTRs) for shell, bottom, roof plates; material certifications for nozzles, structural steel, bolts | API 650 requirements and typical tank material documentation |
| **Quantity (Per Tank)** | **TBD** — Depends on number of material heats used in fabrication | |
| **Total Quantity (3 Tanks)** | **TBD** — Estimated 50-100 MTRs for all plates and materials (ASSUMPTION) | |
| **Content Requirements** | Material grade, heat number, chemical composition, mechanical properties, test results, certifier signature | API 650 Section 2.2 material requirements |
| **Traceability** | Each certificate shall be traceable to specific tank components per weld map | API 650 and typical QA practice |
| **Certifier** | Material supplier or material testing laboratory | Typical material certification practice |
| **Standards Compliance** | ASTM material standards (e.g., ASTM A36, A283, A572 for shell plates — **TBD**) | API 650 material specifications |

### Weld Maps

| Attribute | Value | Source |
|-----------|-------|--------|
| **Weld Map Scope** | Shell welds (vertical and horizontal), bottom-to-shell weld, roof welds, nozzle welds, structural attachment welds | API 650 welding requirements |
| **Quantity** | 3 weld maps (one per tank) | One weld map per tank (typical practice) |
| **Content Requirements** | Weld joint identification, weld procedure (WPS number), welder ID, weld date, NDE results reference | API 650 Section 8 and CSA W59 welding documentation |
| **Format** | Drawing showing all weld joints with identification numbers and NDE reference numbers | Typical weld map format |
| **Traceability** | Each weld joint traceable to NDE report and welder qualification record | API 650 and CSA W59 QA requirements |
| **Revision Control** | As-built weld maps updated to reflect repair welds and field modifications | Typical as-built documentation practice |

### NDE Reports (Non-Destructive Examination)

| Attribute | Value | Source |
|-----------|-------|--------|
| **NDE Methods** | Radiographic testing (RT), ultrasonic testing (UT), magnetic particle testing (MT), vacuum box testing | API 650 Section 8 NDE requirements |
| **NDE Extent** | Per API 650 requirements: Full or spot examination of shell welds, full examination of bottom-to-shell weld | API 650 Section 8.1 |
| **Quantity (Per Tank)** | **TBD** — Depends on number of welds and NDE extent (estimated 20-50 NDE reports per tank) | |
| **Total Quantity (3 Tanks)** | **TBD** — Estimated 60-150 NDE reports for all tanks (ASSUMPTION) | |
| **Content Requirements** | NDE method, procedure reference, weld joint ID, acceptance criteria, results, defects identified, repair actions, examiner signature | API 650 Section 8 and typical NDE report format |
| **Acceptance Criteria** | Per API 650 Section 8 and project specification (DEL-13.02) | API 650 |
| **NDE Technician Qualification** | Certified per ASNT SNT-TC-1A or ISO 9712 | Typical NDE technician certification requirements |
| **NDE Report Certification** | NDE Level II or Level III examiner signature | Typical NDE certification practice |

### Hydrostatic Test Records

| Attribute | Value | Source |
|-----------|-------|--------|
| **Test Scope** | Hydrostatic test of each completed tank per API 650 | API 650 Section 7.4 |
| **Quantity** | 3 hydrostatic test records (one per tank) | One test per tank |
| **Test Pressure** | **TBD** — Per API 650 requirements (typically shell design height + additional head) | API 650 Section 7.4.1 |
| **Test Duration** | Minimum 24 hours hold time (typical per API 650) | API 650 Section 7.4.3 |
| **Test Water Source** | **TBD** — Requires coordination with DEL-29.06 (Tank Hydrotest Water Management Plan) | |
| **Test Water Disposal** | **TBD** — Requires coordination with DEL-29.07 and DEL-29.08 | |
| **Content Requirements** | Tank tag, test date, test pressure, duration, water source, settlement measurements, leak detection results, acceptance, inspector signature | API 650 Section 7.4 and typical hydrotest documentation |
| **Settlement Measurements** | Foundation settlement measured before, during, and after test | API 650 Section 7.4.4 |
| **Inspection** | Visual inspection for leaks, distortion, structural issues during and after test | API 650 Section 7.4.5 |
| **Acceptance Criteria** | No leaks, settlement within API 650 limits, no visible distortion or damage | API 650 Section 7.4 |
| **Witness Requirements** | **TBD** — Client witness required per ER (hold point in ITP — DEL-29.02) | |

---

## Conditions

### Record Generation Timing

| Condition | Value | Source |
|-----------|-------|--------|
| **Material Certificates** | Obtained from suppliers during procurement; compiled before fabrication | Typical procurement and QA workflow |
| **Weld Maps** | Created during fabrication; updated as-built after completion | Typical fabrication QA workflow |
| **NDE Reports** | Generated during fabrication as welds are examined; finalized after repairs | API 650 and typical NDE workflow |
| **Hydrostatic Test Records** | Generated after tank erection is complete and before commissioning | API 650 Section 7.4 timing |

### Inspection and Test Plan (ITP) Hold/Witness Points

| Condition | Value | Source |
|-----------|-------|--------|
| **Material Receiving Inspection** | **TBD** — Hold or witness point per ITP (DEL-29.02) | |
| **Weld Inspection (In-Process)** | **TBD** — Witness point per ITP (DEL-29.02) | |
| **NDE Inspection** | **TBD** — Hold or witness point per ITP (DEL-29.02) | |
| **Hydrostatic Test** | **TBD** — Hold point per ITP (DEL-29.02); typically requires client witness | |

**Source:** Typical ITP hold/witness point requirements for storage tanks

### Record Retention and Archive

| Condition | Value | Source |
|-----------|-------|--------|
| **Retention Period** | **TBD** — Requires ER extraction (typically facility lifetime) | |
| **Archive Format** | **TBD** — Electronic and/or hard copy per project document control procedures | |
| **Archive Location** | **TBD** — Project document management system and/or client archive | |
| **Accessibility** | Records shall be accessible for future maintenance, repair, and regulatory inspections | Typical facility record management requirements |

---

## Construction

### Record Production Workflow

| Item | Description | Source |
|------|-------------|--------|
| **Material Certificates** | Supplier provides MTRs with material shipment; QA reviews and accepts; QA compiles into dossier | Typical material procurement QA workflow |
| **Weld Maps** | Fabricator produces preliminary weld map from design drawings; updates during fabrication with welder IDs and weld dates; finalizes as-built after completion | Typical fabrication QA workflow |
| **NDE Reports** | NDE technician performs examination per procedure; generates report; QA reviews and accepts; repairs performed if defects found; re-examination after repairs | API 650 and typical NDE workflow |
| **Hydrostatic Test Records** | Installation contractor performs hydrotest per procedure; inspector witnesses and documents; settlement measured; visual inspection performed; test record completed and signed | API 650 Section 7.4 and typical testing workflow |

### Record Organization

| Document Category | Organization | Source |
|-------------------|--------------|--------|
| **Tank-Specific Records** | Organized by tank (TK-101 dossier, TK-102 dossier, TK-103 dossier) | Typical record organization practice |
| **Material Certificates** | Organized by heat number or material type within each tank dossier | Typical material traceability practice |
| **Weld Maps** | One weld map per tank, with cross-references to NDE reports | Typical weld documentation practice |
| **NDE Reports** | Organized by weld joint ID or NDE report number within each tank dossier | Typical NDE documentation practice |
| **Hydrostatic Test Records** | One hydrotest record per tank in each tank dossier | Typical testing documentation practice |

### Record Validation and Acceptance

| Item | Description | Source |
|------|-------------|--------|
| **Material Certificate Review** | QA engineer reviews MTRs for completeness, material grade compliance, test results within specification limits | Typical material acceptance process |
| **Weld Map Review** | QA engineer reviews weld map for completeness, traceability to NDE reports, welder qualification verification | Typical weld documentation review process |
| **NDE Report Review** | QA engineer reviews NDE reports for acceptance criteria compliance, examiner qualification, defect disposition | API 650 and typical NDE review process |
| **Hydrostatic Test Record Review** | QA engineer and client inspector review hydrotest record for test pressure, duration, settlement, acceptance criteria compliance | API 650 and typical hydrotest acceptance process |
| **Final Dossier Compilation** | QA engineer compiles all records into tank dossier, indexes, reviews for completeness, submits for client acceptance | Typical as-built documentation process |

---

## References

### Source Documents

1. `_CONTEXT.md` — Deliverable identity, description, anticipated artifacts
2. Decomposition document (`/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md`):
   - Section 1.1 (Project Overview — Key Parameters): Storage capacity (3 × 15,000 MT tanks)
   - Section 5, PKG-13: Scope (API 650 tanks)
   - Section 5, DEL-13.05: Description and anticipated artifacts
3. `_REFERENCES.md` — Reference index (ER PDFs location TBD)

### Expected Reference Documents (TBD — ER Extraction Pending)

1. Volume 2 Part 2: Employer's Requirements - Civil & Process Mechanical Works — **Location TBD**
2. API 650: Welded Tanks for Oil Storage — **Location TBD** (Section 2.2 Materials, Section 7.4 Hydrostatic Testing, Section 8 Welding)
3. CSA W59: Welded Steel Construction (Metal Arc Welding) — **Location TBD** (ASSUMPTION: applicable for welding requirements)
4. ASNT SNT-TC-1A or ISO 9712: NDE Personnel Qualification and Certification — **Location TBD** (ASSUMPTION)
5. ASTM material standards for tank plates — **Location TBD**

### Related Deliverables

| Deliverable | Relationship |
|-------------|-------------|
| DEL-13.01: Storage Tank Design Drawing Set | Design drawings provide basis for material take-offs and weld map development |
| DEL-13.02: Storage Tank Technical Specification | Specification defines material requirements, NDE requirements, testing requirements |
| DEL-13.03: Storage Tank Design Calculations | Calculations define hydrotest pressure and settlement limits |
| DEL-13.04: Storage Tank Data Sheet Package | Data sheets identify tank tags and configuration referenced in records |
| DEL-13.06: Storage Tank Fabrication Quality Documentation Package | Fabrication quality documentation (WPS/PQR/WPQ, shop inspection) supplements installation and test records |
| DEL-29.02: Inspection and Test Plan With Hold/Witness Points | ITP defines hold/witness points for material inspection, NDE, and hydrostatic test |
| DEL-29.06: Tank Hydrotest Water Management Plan | Hydrotest water management plan defines water source, treatment, and disposal for hydrostatic tests |
| DEL-29.07: Hydrotest Water Treatment & Discharge Testing Results | Hydrotest water disposal records supplement hydrotest records |
| DEL-29.08: Hydrotest Water Disposal Installation & Test Records | Hydrotest water disposal records supplement hydrotest records |

---

## Cross-Document References

**For detailed requirements:** See `Specification.md`
- FR-01: Material Certificate Requirements → Material Certificates attributes
- FR-02: Weld Map Requirements → Weld Maps attributes
- FR-03: NDE Report Requirements → NDE Reports attributes
- FR-04: Hydrostatic Test Record Requirements → Hydrostatic Test Records attributes
- QR-01 through QR-04: Quality and compliance requirements for each record type

**For record generation rationale:** See `Guidance.md`
- DP-01: Quality Evidence Philosophy → Record purpose and value
- DP-02: Traceability → Material and weld traceability principles
- DP-03: API 650 Compliance Documentation → Standards compliance requirements
- Trade-offs → Record detail level, documentation format decisions

**For record production workflow:** See `Procedure.md`
- Steps 1-4 → Produce material certificates, weld maps, NDE reports, hydrotest records documented here
- Step 5 → Compile and validate record package
- Step 6 → Submit record package for acceptance

---

**Document Status:** Pass 3 (Final) — Enrichment complete. Cross-document consistency verified. All TBDs marked for ER extraction and execution planning. ASSUMPTIONs labeled. Ready for WORKING_ITEMS refinement.

**Last Updated:** 2026-01-28
