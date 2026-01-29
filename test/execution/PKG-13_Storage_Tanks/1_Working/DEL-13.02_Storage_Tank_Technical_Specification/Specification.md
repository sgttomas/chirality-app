# Specification: DEL-13.02 Storage Tank Technical Specification

## Scope

This specification defines the requirements for producing **Storage Tank Technical Specification** within **PKG-13 Storage Tanks**.

### Deliverable Description

Defines performance, materials, and workmanship requirements for storage tank per ER requirements.

**Source:** _CONTEXT.md, Decomposition document DEL-13.02

### Coverage

**This deliverable shall produce three specification documents:**

1. **API 650 Tank Specification** — Performance, materials, fabrication, testing, and quality requirements for 3 × 15,000 MT atmospheric storage tanks
2. **Agitator Specification** — Performance, materials, and installation requirements for tank agitators (3 units)
3. **Tank Appurtenance Specification** — Requirements for overflow protection, water draw-off, nozzles, manholes, vents, and Phase 2 connections

**Source:** _CONTEXT.md (Anticipated Artifacts)

**Included in API 650 Tank Specification:**
- Tank design basis and performance requirements
- Material specifications for shell, bottom, roof, nozzles, structural elements
- Fabrication standards and workmanship requirements
- Welding procedures and qualifications
- Quality control and inspection requirements
- Testing requirements (hydrostatic, leak, settlement)
- Surface preparation and coating specifications (coordinate with PKG-26)
- Installation and erection requirements
- Documentation and record requirements

**Included in Agitator Specification:**
- Agitator type, capacity, and performance requirements
- Motor and drive specifications
- Materials and construction standards
- Mounting and support requirements
- Installation and alignment requirements
- Testing and commissioning requirements
- Maintenance and spare parts requirements

**Included in Tank Appurtenance Specification:**
- Overflow protection system requirements
- Water draw-off system requirements
- Nozzle specifications (sizes, ratings, materials, connections)
- Manhole and access opening requirements
- Vent and pressure relief requirements
- Instrumentation connections and supports
- Phase 2 connection provisions
- Ladders, platforms, handrails, access equipment

**Source:** ASSUMPTION based on typical tank specification scope and Datasheet.md

**Excluded:**
- Detailed design calculations (covered by DEL-13.03 Design Calculations)
- Detailed design drawings (covered by DEL-13.01 Design Drawing Set)
- Vendor equipment data sheets (covered by DEL-13.04 Data Sheet Package)
- Construction execution procedures (covered by construction management, not this deliverable — **ASSUMPTION**)
- Operations and maintenance manuals (separate deliverable, not this specification — **ASSUMPTION**)

**Source:** ASSUMPTION based on typical responsibility splits and decomposition package structure

---

## Requirements

### Functional Requirements

**FR-01: Specification Completeness**
- The specification shall address all aspects necessary for tank procurement, fabrication, installation, and testing
- All performance requirements, materials, workmanship standards, and quality requirements shall be clearly specified
- No critical requirements shall be left undefined or ambiguous
- **Source:** Specification best practice; OBJ-1 (Safe & Reliable Operation)

**FR-02: Alignment with Design**
- The specification shall be consistent with and support the tank design shown in DEL-13.01 (Design Drawing Set)
- Materials specified shall be suitable for the design conditions (temperature, pressure, seismic, etc.)
- Fabrication requirements shall be achievable with the design configuration
- **Source:** Design-specification consistency requirement

**FR-03: Alignment with Calculations**
- The specification shall reference and be supported by DEL-13.03 (Design Calculations)
- Material specifications shall satisfy design calculation assumptions
- Performance requirements shall be verified by calculations
- **Source:** Calculation-specification consistency requirement

**FR-04: Procurement Support**
- The specification shall provide sufficient information for procurement activities:
  - Vendor bidding and proposal evaluation
  - Vendor equipment selection and submittal preparation
  - Contract technical requirements
- **Source:** ASSUMPTION based on typical EPC procurement workflow

**FR-05: Quality Assurance Integration**
- The specification shall define quality control and inspection requirements aligned with project QA/QC plan
- Hold points and witness points for inspections shall be identified
- Acceptance criteria shall be clearly stated
- **Source:** ASSUMPTION based on typical quality management requirements; OBJ-1 (Safe & Reliable Operation)

### Content Requirements

**CR-01: API 650 Tank Specification Content**

The API 650 Tank Specification shall include the following sections (minimum):

| Section | Content | Source |
|---------|---------|--------|
| **1. Scope** | Defines what the specification covers and excludes | Standard specification format |
| **2. References** | Lists applicable codes, standards, and reference documents (API 650, NBC 2020, etc.) | Datasheet.md Primary Standards |
| **3. Definitions** | Defines technical terms and abbreviations used | Standard specification format |
| **4. Design Basis** | Tank capacity, product, operating conditions, environmental loads, design life | Datasheet.md Conditions section; DEL-13.03 calculations |
| **5. Materials** | Shell, bottom, roof, nozzle, structural materials with specifications and grades | Datasheet.md Material Categories; API 650 material requirements |
| **6. Design Requirements** | Tank geometry, shell thickness, roof type, foundation interface, seismic design per API 650 | DEL-13.01 drawings; DEL-13.03 calculations; API 650 |
| **7. Fabrication** | Fabrication methods, tolerances, workmanship standards per API 650 | API 650 fabrication requirements |
| **8. Welding** | Welding procedures, qualifications (WPS/PQR/WPQ), inspection per API 650 and CSA W59 | Datasheet.md Quality and Compliance; API 650; CSA W59 |
| **9. Inspection and Testing** | In-process inspection, NDE, hydrostatic testing, leak testing per API 650 | API 650 inspection and testing requirements |
| **10. Surface Preparation and Coating** | Surface prep standards, coating systems (internal and external) per PKG-26 | Coordination with PKG-26; **TBD** |
| **11. Installation** | Erection methods, field welding, alignment, final inspection | API 650 erection requirements; **TBD** |
| **12. Documentation** | Required submittals, test reports, certifications, as-built records | DEL-13.05, DEL-13.06 requirements |

**Source:** ASSUMPTION based on typical API 650 tank specification structure; API 650 standard content

**CR-02: Agitator Specification Content**

The Agitator Specification shall include:
- Performance requirements: Mixing duty, power, speed, torque — **TBD** (vendor data or process requirements)
- Type selection: Side-entering, top-entering, or bottom-mounted — **TBD** (design selection)
- Motor and drive: Power, voltage, enclosure type, VFD if required — **TBD**
- Materials: Wetted parts material compatibility with canola oil — **TBD**
- Mounting: Interface with tank shell, structural loads, reinforcement requirements
- Testing: Factory acceptance test, site performance test — **TBD**

**Source:** ASSUMPTION based on typical agitator specification content; Datasheet.md (agitators required)

**CR-03: Tank Appurtenance Specification Content**

The Tank Appurtenance Specification shall include:
- Overflow protection: Type, capacity, piping interface — **TBD** (ER extraction)
- Water draw-off: Nozzle size, valve type, piping interface — **TBD**
- Nozzles: Schedule referencing DEL-13.01 (nozzle schedules), material specs, reinforcement per API 650
- Manholes and access openings: Size, quantity, gasket type per API 650
- Venting: Normal venting and emergency venting per API 650 Appendix F — **TBD**
- Instrumentation connections: Nozzles for level, temperature, pressure instruments (coordinate with PKG-20)
- Phase 2 connections: Size, location, blanking/capping method — **TBD** (ER extraction for Phase 2 scope)
- Access equipment: Ladders, platforms, handrails per safety codes — **TBD**

**Source:** ASSUMPTION based on typical tank appurtenance requirements; Decomposition PKG-13 Scope

### Performance Requirements

**PR-01: Standard Compliance**
- The specification shall require compliance with API 650 as the primary design and fabrication standard
- Edition and addenda of API 650 shall be specified — **TBD** (ER extraction)
- Where the specification imposes requirements beyond API 650, those requirements shall be clearly identified
- **Source:** Decomposition PKG-13 Scope (API 650); specification best practice

**PR-02: Material Suitability**
- Specified materials shall be suitable for CSD canola oil service
- Material compatibility with product and operating temperature shall be verified
- Brittle fracture considerations per API 650 Appendix D shall be addressed if minimum operating temperature is low — **TBD**
- **Source:** API 650 material requirements; product compatibility

**PR-03: Fabricator Qualification**
- The specification shall require fabricator qualification per CSA W47.1 or equivalent — **ASSUMPTION**
- Fabricator's quality management system shall comply with ISO 9001 or equivalent — **TBD**
- **Source:** ASSUMPTION based on Canadian location and quality requirements

**PR-04: Welding Quality**
- Welding procedures (WPS) shall be qualified per CSA W59 and API 650
- Welders shall be qualified per CSA W47.1 or API 650 requirements
- Weld inspection and NDE requirements per API 650 Section 8
- **Source:** Datasheet.md Quality and Compliance; API 650; CSA W59

**PR-05: Testing Requirements**
- Hydrostatic test per API 650 Section 7 shall be specified
- Test duration, water source, drainage, and acceptance criteria shall be defined
- Agitator performance testing and acceptance criteria shall be specified — **TBD**
- **Source:** API 650 Section 7; typical agitator testing requirements

### Interface Requirements

**IR-01: Coordination with Design Drawings**
- The specification shall reference DEL-13.01 (Design Drawing Set) for tank geometry, nozzle schedule, and details
- Any conflicts between specification and drawings shall be resolved and documented
- **Source:** Typical design-specification coordination requirement

**IR-02: Coordination with Calculations**
- The specification shall reference DEL-13.03 (Design Calculations) for design basis verification
- Material properties and allowable stresses shall be consistent with calculation assumptions
- **Source:** Typical calculation-specification coordination requirement

**IR-03: Coordination with Coatings Package**
- The specification shall coordinate with PKG-26 (Protective Coatings & Painting) for:
  - Surface preparation standards
  - Internal coating system selection and application
  - External coating system selection and application
  - Coating inspection and testing requirements
- **TBD** — Specific coating requirements require PKG-26 coordination
- **Source:** Typical tank coating coordination requirement

**IR-04: Coordination with Piping Package**
- Nozzle specifications shall coordinate with PKG-14 (Process Piping) for:
  - Nozzle sizes and ratings
  - Connection types (flanged, threaded, etc.)
  - Piping interface loads (thermal expansion, vibration, etc.)
- **Source:** Typical tank-piping interface coordination

**IR-05: Coordination with Instrumentation Package**
- Instrumentation connection specifications shall coordinate with PKG-20 (Field Instrumentation) for:
  - Instrument nozzle sizes and types
  - Mounting provisions for level, temperature, pressure instruments
  - Access for installation and maintenance
- **Source:** Typical tank-instrumentation interface coordination

### Documentation Requirements

**DR-01: Specification Format**
- Specifications shall follow project specification format and template — **TBD** (project standards)
- Numbering system per project document control procedures — **TBD**
- **Source:** ASSUMPTION based on typical project documentation requirements

**DR-02: Specification Clarity**
- Requirements shall be stated clearly and unambiguously using "shall" for mandatory requirements
- Optional requirements shall be identified using "should" or "may"
- Informational content shall be clearly distinguished from requirements
- **Source:** Specification best practice (imperative mood for requirements)

**DR-03: Reference Completeness**
- All referenced codes, standards, and documents shall be listed with edition and date
- References to other project deliverables shall include deliverable ID
- **Source:** Specification best practice

---

## Standards

### Primary Standards

| Standard | Title | Application |
|----------|-------|-------------|
| **API 650** | Welded Tanks for Oil Storage | Primary tank design, fabrication, inspection, testing standard |
| **API 653** | Tank Inspection, Repair, Alteration, and Reconstruction | Referenced for future maintenance |
| **CSA W59** | Welded Steel Construction (Metal Arc Welding) | Welding requirements for Canadian location |

### Supporting Standards

| Standard | Title | Application |
|----------|-------|-------------|
| **ASME B31.3** | Process Piping | Nozzle connections and piping interfaces |
| **CSA B51** | Boiler, Pressure Vessel and Pressure Piping Code | Potential application to agitators |
| **CSA G40.21** | Structural Quality Steel | Structural steel material specifications |
| **CSA W47.1** | Certification of Companies for Fusion Welding of Steel | Fabricator qualification |
| **NBC 2020** | National Building Code of Canada | Environmental loads (wind, snow, seismic) |
| **ISO 9001** | Quality Management Systems | Fabricator quality management (ASSUMPTION) |

**Source:** Datasheet.md Primary Standards; ASSUMPTION for supporting standards

### Employer's Requirements

- Volume 2 Part 1: Employer's Requirements - General Requirements — **Location TBD**
- Volume 2 Part 2: Employer's Requirements - Civil & Process Mechanical Works — **Location TBD**
- **TBD** — Specific ER clauses applicable to storage tank specifications require extraction

---

## Verification

### Specification Review Process

**V-01: Technical Review**
- Mechanical discipline lead reviews specification for technical accuracy and completeness
- Verify alignment with API 650 and applicable standards
- Verify material selections are appropriate for service
- **TBD** — Review checklist per project quality procedures

**V-02: Interdisciplinary Review (IDR)**
- Affected disciplines review specification for interface coordination:
  - Civil/Structural (PKG-05): Foundation interface, loading
  - Process/Piping (PKG-14): Nozzle specifications, piping interfaces
  - Electrical/I&C (PKG-20): Instrumentation interfaces
  - Coatings (PKG-26): Coating specifications
- IDR comments logged, resolved, and closed out
- **Source:** Typical specification review process

**V-03: Compliance Matrix Verification**
- Verify all ER requirements are addressed in specification
- Compliance matrix tracks ER clause to specification section mapping
- **TBD** — Compliance matrix format and maintenance per project procedures
- **Source:** ASSUMPTION based on typical ER compliance verification

**V-04: Calculation Cross-Check**
- Verify specification requirements are supported by DEL-13.03 (Design Calculations)
- Material specifications and design parameters match calculation assumptions
- **Source:** Typical calculation-specification coordination

**V-05: Employer Review**
- Specification submitted to Employer for review and comment — **TBD** (submission schedule and process)
- Employer comments resolved or incorporated
- **Source:** ASSUMPTION based on typical design-build review workflow

### Acceptance Criteria

**AC-01: Completeness**
- All three specification documents produced (API 650 Tank, Agitator, Tank Appurtenances)
- All required sections present and complete
- No critical TBDs remaining at time of final issue

**AC-02: Technical Accuracy**
- Requirements are technically sound and achievable
- Compliance with API 650 and applicable standards verified
- Material selections appropriate for service

**AC-03: Consistency**
- Specification consistent with design drawings (DEL-13.01)
- Specification consistent with design calculations (DEL-13.03)
- No internal contradictions within specification

**AC-04: Clarity**
- Requirements stated clearly using imperative mood ("shall")
- No ambiguous or conflicting requirements
- References complete and accurate

**AC-05: Approval**
- Technical review completed and signed off
- IDR completed and all comments resolved
- Discipline lead approval obtained
- Employer review completed (if required) — **TBD**

**Source:** ASSUMPTION based on typical specification acceptance criteria

---

## Documentation

### Required Specification Outputs

| Specification Document | Description | Format |
|------------------------|-------------|--------|
| **API 650 Tank Specification** | Performance, materials, fabrication, testing requirements for tanks | **TBD** — Project specification format |
| **Agitator Specification** | Performance, materials, installation requirements for agitators | **TBD** — Project specification format |
| **Tank Appurtenance Specification** | Requirements for overflow, water draw-off, nozzles, appurtenances | **TBD** — Project specification format |

**Source:** _CONTEXT.md (Anticipated Artifacts)

### Specification Management

**DM-01: Document Control**
- All specifications managed per project document control procedures
- Electronic master copies maintained in project document management system
- **TBD** — Document management system and procedures

**DM-02: Issuance**
- Specifications issued for review: Filed in `2_Checking/To/` with transmittal
- Specifications issued for procurement/construction: Filed in `3_Issued/` with issue record
- **TBD** — Issuance workflow and approval matrix

**DM-03: Revision Management**
- Revisions tracked with revision table and change bars
- Revision history maintained in specification document
- Superseded revisions archived per project retention policy
- **TBD** — Revision conventions per project procedures

**Source:** ASSUMPTION based on typical project document management

---

---

## Cross-Document References

**See Datasheet.md:** Standards, materials, quality context → Referenced in CR-01, PR-01 through PR-05
**See Guidance.md:** Principles (DP series), considerations, trade-offs → Support content and performance requirements
**See Procedure.md:** Steps 2-4 produce the specification documents per requirements here; Steps 5-8 verify compliance

---

**Document Status:** Pass 3 (Final) — Enrichment complete. Requirements for producing three specification documents defined. Cross-document consistency verified. Ready for WORKING_ITEMS refinement.

**Last Updated:** 2026-01-28
