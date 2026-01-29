# Procedure: DEL-10.02 Railcar Unloading Technical Specification

## Purpose

This procedure defines the process for **producing and managing** the **Railcar Unloading Technical Specification** within **PKG-10 Railcar Unloading System**.

**Scope of Procedure:**
- Development of technical specification for railcar unloading equipment and systems (performance, materials, workmanship requirements)
- Creation of compliance/traceability matrix mapping specification to Employer's Requirements
- Technical review, IDC coordination, approval, and issue workflow
- Document control and records management

**Deliverable Type:** Specification (Technical Specification)
**Responsible Party:** D&B Contractor
**Discipline:** Process
**Status:** INITIALIZED

**Dual-Use Nature:**
- This procedure primarily describes how to **produce** the technical specification deliverable (specification document defining requirements for equipment and systems)
- The produced technical specification will be **used by** procurement team (equipment procurement), vendors/manufacturers (equipment design and fabrication), construction contractors (installation standards), and QA/QC team (inspection and testing criteria)

## Prerequisites

### Dependencies

**Dependency Tracking Mode:** NOT_TRACKED — dependencies coordinated externally by humans (see `_DEPENDENCIES.md` and `execution/_Coordination/_COORDINATION.md`)

**Upstream Inputs (typical sequence — coordinate via project schedule and stage gates):**

| Input | Source | Status | Required Information | Use in This Procedure | Specification Link |
|-------|--------|--------|---------------------|----------------------|--------------------|
| Project design basis and requirements | Employer's Requirements Vol 2 Parts 1–3 | **TBD** | Performance requirements, material requirements, workmanship requirements, standards and codes, interface requirements, quality requirements specific to railcar unloading system | Step 2 (ER clause identification — primary source for specification requirements); all steps (ER requirements drive specification content) | Specification.md §Requirements (all requirements traceable to ER); Datasheet.md §References (ER listed as baseline source) |
| Equipment sizing basis and performance analysis | DEL-10.03 Design Calculations | **TBD** | Header pipe sizing (pipe diameters, wall thickness, pressure ratings), hydraulic analysis (flow capacity, pressure drop, slopes), containment volume calculations (pan sizing, sump sizing), throughput analysis (verify 1,000,000 MT/annum with 32 stations; simultaneous operations requirement **TBD**), equipment loads (for structural coordination) | Step 3 (performance requirements based on DEL-10.03 calculations — header capacity, containment volume, unloading rates, equipment loads); verification that performance requirements are achievable | Specification.md PF-01, PF-03, PF-04 (performance requirements based on calculations); IF-02 (equipment loads from calculations) |
| Layout and physical arrangement | DEL-10.01 Design Drawing Set | **TBD** | Equipment arrangement (32 station layout, header routing, containment arrangement), interface points (structural supports, electrical connections, instrumentation, piping connections), space constraints (clearances, access requirements) | Step 3 (specification requirements account for physical arrangement — arm reach envelopes per layout, header routing per layout, containment configuration per layout); Step 5 (IDC coordination uses DEL-10.01 drawings to verify interface alignment) | Specification.md IF-01 through IF-06 (interface requirements coordinate with DEL-10.01 arrangement); Datasheet.md §Construction (specification sections reference DEL-10.01 drawings) |
| Applicable codes and standards | Regulatory (BC Building Code, environmental regulations); industry codes (ASME B31.3, CSA codes, API standards, food-grade standards, AWS, SSPC) | **TBD** | Code requirements: material requirements per code, design requirements per code, fabrication requirements per code, testing requirements per code; standard requirements: performance standards, material standards, workmanship standards | Step 3 (specification requirements per applicable codes and standards — code-compliant materials, welding per code, testing per code); Step 4 (code compliance verification during technical review) | Specification.md §Standards (all applicable codes and standards listed); MT-02, WK-01, WK-04 (requirements per code) |

**ASSUMPTION:** Dependencies managed through project schedule, stage gates (30% / 60% / 90% / IFC), and human coordination. Upstream deliverables to be available per project milestone plan. If upstream inputs not available when needed: proceed with specification development using reasonable assumptions (document all assumptions; mark requirements TBD where inputs required); update specification when inputs become available (issue revised specification with updated requirements).

### Reference Materials

| Reference | Location | Purpose | Document Link | Specification Link |
|-----------|----------|---------|---------------|--------------------|
| Decomposition | `test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md` | PKG-10 scope (§5 — scope elements, deliverable definitions); DEL-10.02 definition; objective mapping (§6: OBJ-1, OBJ-2, OBJ-4, OBJ-7) | Datasheet.md §References (decomposition as primary scope source); Guidance.md §Principles (objective alignment) | Specification.md §Scope (scope from decomposition) |
| Employer's Requirements Vol 2 Pt 1 | `test/Volume_2_Part_1_Employers_Requirements.pdf` | Performance/material requirements (clauses **TBD** — primary source for project-specific requirements; to be identified and mapped in Step 2) | Specification.md §Requirements; Datasheet.md §Conditions | Specification.md §Requirements (ER requirements drive specifications); Step 2 (ER clause identification) |
| Employer's Requirements Vol 2 Pt 2 | `test/Volume_2_Part_2_Employers_Requirements.pdf` | Technical requirements (clauses **TBD** — standards, codes, technical criteria, equipment requirements) | Specification.md §Standards; Datasheet.md §Conditions | Specification.md §Standards (applicable standards from ER); Step 2 (ER clause identification) |
| Employer's Requirements Vol 2 Pt 3 | `test/Volume_2_Part_3_Employers_Requirements.pdf` | Quality/workmanship requirements (clauses **TBD** — QA/QC procedures, testing requirements, documentation requirements, submittal requirements) | Specification.md WK-xx, QA-xx; Datasheet.md §Attributes | Specification.md WK-xx (workmanship requirements from ER); Step 2 (ER clause identification) |
| Specification.md | This deliverable folder | Requirements for this deliverable (functional, performance, material, workmanship, interface, quality requirements that this procedure must satisfy) | Bidirectional link (all steps verify against Specification.md requirements) | All procedure steps (requirements verification) |
| Guidance.md | This deliverable folder | Design principles, considerations, trade-offs, examples (guide specification development per principles) | Bidirectional link (Step 3 applies Guidance principles and considerations) | All procedure steps (guidance application) |
| Datasheet.md | This deliverable folder | Document attributes, scope elements, anticipated artifacts (specification structure and content basis) | Bidirectional link (Steps 1, 3, 6 use Datasheet for document structure and metadata) | All procedure steps (datasheet defines scope and structure) |
| DEL-10.01 | `execution/PKG-10_Railcar_Unloading_System/1_Working/DEL-10.01_*/` | Design Drawing Set (equipment arrangement, layout, interfaces) — specification requirements drive drawing content; drawings show physical implementation | Datasheet.md §References; Step 3 (specification requirements coordinate with DEL-10.01 arrangement) | Specification.md §Scope (drawings reference); IF-01 through IF-06 (interface requirements shown on DEL-10.01 drawings) |
| DEL-10.03 | `execution/PKG-10_Railcar_Unloading_System/1_Working/DEL-10.03_*/` | Design Calculations (sizing basis, performance verification) — calculations provide basis for specification performance requirements | Datasheet.md §References; §Prerequisites (DEL-10.03 as upstream input) | Specification.md PF-01, PF-03, PF-04 (performance requirements from calculations); Step 3 (incorporate DEL-10.03 results) |
| DEL-10.04 | `execution/PKG-10_Railcar_Unloading_System/1_Working/DEL-10.04_*/` | Data Sheet Package (equipment specifications) — data sheets implement this technical specification for individual equipment items | Datasheet.md §References; downstream relationship | Specification.md FN-01 (scope elements detailed in data sheets); downstream (data sheets follow specification) |
| DEL-10.05 | `execution/PKG-10_Railcar_Unloading_System/1_Working/DEL-10.05_*/` | Installation & Test Records (verification of compliance) — installation and test records demonstrate compliance with workmanship and testing requirements | Datasheet.md §References; downstream relationship | Specification.md WK-04 (testing requirements verified in DEL-10.05); downstream (installation/test records verify specification compliance) |
| Applicable codes/standards | **TBD** — per Specification.md §Standards | Code compliance (ASME B31.3, CSA codes, API standards, food-grade standards, AWS, SSPC, BC Building Code, environmental regulations) | Specification.md §Standards (all codes listed) | Step 3 (requirements per codes); Step 4 (code compliance verification) |

### Personnel Requirements

| Role | Qualification | Responsibility | Verification | Specification Link |
|------|---------------|----------------|--------------|-------------------|
| Specification Author | Process discipline; specification writing experience; knowledge of applicable codes/standards; **TBD** years experience or professional registration (P.Eng. in BC for engineering specifications) | Specification development (Steps 1–3): outline development, ER clause identification, content drafting, compliance matrix development | Author sign-off on specification | Specification.md QA-02 (author metadata) |
| Technical Reviewer | Process discipline; independent from author; specification review experience; knowledge of applicable codes/standards; **TBD** years experience or professional registration | Technical review (Step 4): verify technical adequacy, code compliance, completeness, clarity, consistency, verifiability; review compliance matrix; document review comments | Reviewer sign-off; review comment resolution record | Specification.md QA-03 (technical review requirement) |
| Discipline Lead | Process discipline; approval authority; **TBD** years experience and professional registration | Specification approval (Step 6): review for technical completeness, ER compliance, IDC coordination completeness, appropriateness for use | Approval sign-off | Specification.md QA-05 (approval requirement) |
| IDC Coordinator | Multi-discipline coordination experience; understanding of all discipline scopes and interfaces | Interface coordination (Step 5): organize IDC meetings, track interface issues, coordinate conflict resolution, obtain sign-offs from interface disciplines | IDC sign-off sheet (all interface disciplines signed) | Specification.md QA-04 (IDC review requirement) |
| Document Controller | Document control procedures knowledge; project document management system familiarity | Issue and transmittal (Step 6): document numbering, transmittal preparation, distribution, document register updates | Transmittal record; document register entry | Specification.md §Documentation (document control requirements) |

**ASSUMPTION:** Personnel competency requirements per project quality procedures and professional registration requirements (e.g., P.Eng. in BC for engineering specifications, or Engineer-in-Training under supervision of P.Eng.). Technical Specification is an engineering document requiring appropriate professional oversight.

### Tools and Resources

| Tool/Resource | Purpose | Use in Procedure |
|---------------|---------|------------------|
| Word processing or document authoring software | Specification document preparation (MS Word, LaTeX, or other per project standard **TBD**) | Step 3 (draft specification content) |
| Spreadsheet or database software | Compliance matrix development (Excel, database, or other per project standard **TBD**) | Step 2 (ER clause identification and matrix development), Step 4 (matrix review) |
| Project document numbering system | Specification document number assignment | Step 6 (finalize document number) |
| Document management system | Specification storage, revision control, transmittal, distribution | Step 6 (issue and filing) |
| Code and standard references | Code compliance verification (ASME B31.3, CSA codes, food-grade standards, AWS, SSPC, etc.) | Step 3 (requirements per codes), Step 4 (code compliance review) |
| ER clause database or index | **If available** — searchable index of ER clauses for efficient clause identification | Step 2 (ER clause identification) |

## Steps

### Step 1: Confirm Scope and Develop Outline

**Objective:** Establish specification structure based on PKG-10 scope and anticipated artifacts (3 specification sections per Datasheet.md §Construction).

**Actions:**

1. **Review Specification.md §Scope** for deliverable scope and exclusions:
   - Confirm PKG-10 scope elements to be specified: (1) unloading arms, (2) quick-connects, (3) gravity flow header, (4) spill containment pans, (5) collection system, (6) atmospheric venting, (7) flow indicators (Specification.md FN-01)
   - Confirm anticipated specification sections: Unloading Arm Specification, Containment System Specification, Header Pipe Specification (Specification.md FN-04; Datasheet.md §Construction)
   - Note exclusions: downstream piping (PKG-14), electrical power (PKG-17), detailed instrumentation specs (PKG-20), control systems (PKG-21 if applicable), structural design (PKG-05/PKG-06), rail track (PKG-07) — these are interface items only in this specification

2. **Review Datasheet.md §Construction** for anticipated artifacts and scope elements:
   - 3 specification sections covering all 7 PKG-10 scope elements
   - Compliance matrix required (Datasheet.md §Attributes)

3. **Review Guidance.md for specification content principles** (Guidance.md §Principles and §Examples):
   - Performance-based requirements (specify outcomes, not prescriptive designs)
   - Material compatibility (food-grade for product contact)
   - Code compliance (reference applicable codes)
   - Verifiability (all requirements testable/verifiable)
   - Traceability (compliance matrix to ER)
   - Typical specification structure (10 sections per Guidance.md §Examples — adapt as needed)

4. **Develop specification outline** (adapt typical structure from Guidance.md §Examples):

   **Section 1: Scope**
   - 1.1 General (PKG-10 scope elements covered, 32 stations, gravity flow operation)
   - 1.2 Inclusions (equipment and systems within specification scope)
   - 1.3 Exclusions (equipment and systems outside specification scope — covered by other packages)
   - 1.4 Applicable Standards and Codes (list from Specification.md §Standards)

   **Section 2: References**
   - 2.1 Codes and Standards (ASME B31.3, food-grade standards, AWS, etc.)
   - 2.2 Project Documents (DEL-10.01 drawings, DEL-10.03 calculations, DEL-10.04 data sheets)
   - 2.3 Employer's Requirements (Vol 2 Parts 1–3 with clause references)

   **Section 3: Definitions and Abbreviations**
   - 3.1 Definitions (technical terms: "gravity flow," "dry-break coupler," "food-grade," "largest credible spill," etc.)
   - 3.2 Abbreviations (NDE, WPS, IDC, ER, etc.)

   **Section 4: General Requirements**
   - 4.1 Codes and Standards Compliance (all equipment shall comply with applicable codes)
   - 4.2 Food-Grade Requirements (all product contact materials and surfaces food-grade compatible)
   - 4.3 Submittal Requirements (shop drawings, product data, test reports, certifications — general submittal requirements; specific submittals in Section 9)
   - 4.4 Quality Assurance (inspection, testing, documentation — general QA requirements; specific requirements in Section 8)

   **Section 5: Unloading Arm Specification** (covers unloading arms, quick-connects, atmospheric venting, flow indicators)
   - 5.1 Performance Requirements (flow rate, pressure rating, temperature range, operational envelope)
   - 5.2 Material Requirements (product contact materials, structural materials, seal materials)
   - 5.3 Workmanship Requirements (fabrication, assembly, testing, painting/coating)
   - 5.4 Interface Requirements (railcar connection, structural supports, instrumentation)

   **Section 6: Containment System Specification** (covers spill containment pans, sumps, drains, sump pumps)
   - 6.1 Performance Requirements (containment volume, drainage time, structural capacity)
   - 6.2 Material Requirements (pan materials, drain materials, sump materials, pump materials)
   - 6.3 Workmanship Requirements (welding — liquid-tight construction, surface preparation, leak testing)
   - 6.4 Interface Requirements (structural supports, electrical power for pumps, instrumentation for level switches)

   **Section 7: Header Pipe Specification** (covers gravity flow header, valves, fittings, supports)
   - 7.1 Performance Requirements (flow capacity, pressure rating, drainage capability, air release)
   - 7.2 Material Requirements (pipe materials, valve materials, fitting materials, support materials)
   - 7.3 Workmanship Requirements (welding per code, pipe support installation, pressure testing, surface preparation/coating)
   - 7.4 Interface Requirements (downstream piping connection, structural supports)

   **Section 8: Quality Assurance and Testing**
   - 8.1 Inspection Requirements (weld inspection, surface inspection, coating inspection, dimensional inspection)
   - 8.2 Non-Destructive Examination (NDE methods, extent, acceptance criteria per code)
   - 8.3 Pressure Testing (hydrostatic test per ASME B31.3, test pressure, hold time, test medium, witnessing)
   - 8.4 Leak Testing (soap solution or other method at all connections, flanges, seals)
   - 8.5 Functional Testing (operational testing of arms, valves, pumps per manufacturer requirements)
   - 8.6 Acceptance Criteria (pass/fail criteria for all inspections and tests)
   - 8.7 Test Records (documentation requirements per DEL-10.05)

   **Section 9: Submittals and Documentation**
   - 9.1 Submittal Requirements (shop drawings for approval, product data, test reports, material certifications, as-built data, O&M manuals)
   - 9.2 Submittal Schedule (submittal timing and approval process)
   - 9.3 Data Sheets (32 unloading arm data sheets, pump data sheets, instrument data sheets — refer to DEL-10.04)

   **Section 10: Appendices**
   - Appendix A: Compliance Matrix (ER clause to specification section mapping — see Step 2 for matrix development)
   - Appendix B: Reference Drawings (list drawings from DEL-10.01 referenced in specification)
   - Other appendices as needed

5. **Review outline with discipline lead:**
   - Verify outline covers all scope elements (all 7 PKG-10 scope elements addressed in appropriate sections)
   - Verify outline structure appropriate for project and ER requirements (may need to adapt structure if ER specifies format **TBD**)
   - Confirm section organization logical and complete

6. **Obtain discipline lead sign-off on approved outline:**
   - Document outline approval (written approval or email confirmation)
   - File approved outline in `1_Working/` deliverable folder

**Output:** Approved specification outline; filed in `1_Working/` deliverable folder.

**Verification:** Discipline lead sign-off on outline (confirms specification structure appropriate and complete).

**Traceability to Specification:**
- Specification.md FN-04: Anticipated artifacts (3 specification sections) addressed in approved outline (Sections 5, 6, 7)
- Specification.md FN-01, FN-02, FN-03: All scope elements have performance, material, workmanship requirements in outline structure

---

### Step 2: Identify Employer's Requirements Clauses and Develop Compliance Matrix

**Objective:** Map Employer's Requirements clauses to specification sections for traceability (Specification.md QA-01 — compliance matrix required).

**Actions:**

1. **Review Employer's Requirements Vol 2 Parts 1, 2, and 3:**
   - **TBD** — Systematic review of all three ER volumes
   - Identify clauses applicable to PKG-10 scope (railcar unloading system, equipment, materials, installation, testing)
   - Extract requirements from each applicable ER clause (performance criteria, material requirements, workmanship standards, testing requirements, quality requirements, interface requirements)

2. **Categorize ER clauses** by requirement type and specification section:

   | ER Clause Category | Specification Section(s) | Example Requirements (to be populated from actual ER clauses) |
   |-------------------|-------------------------|--------------------------------------------------------------|
   | Unloading system performance | Section 5 (Unloading Arms), Section 7 (Header Pipe) | Flow rates, unloading time, throughput capacity, simultaneous operations |
   | Equipment specifications | Section 5 (Unloading Arms) | Arm type, capacity, materials, operational envelope, quick-connect type |
   | Containment requirements | Section 6 (Containment System) | Containment volume, regulatory compliance, materials, testing |
   | Material requirements | Sections 5, 6, 7 (Materials subsections) | Food-grade materials, product compatibility, corrosion resistance, certifications |
   | Workmanship standards | Sections 5, 6, 7 (Workmanship subsections), Section 8 (QA/Testing) | Welding per code, surface finish, cleaning, testing per code |
   | Interface requirements | Sections 5, 6, 7 (Interface subsections) | Coordination with other packages, load requirements, connection requirements |
   | Quality/documentation | Section 8 (QA/Testing), Section 9 (Submittals) | QA/QC procedures, testing requirements, submittal requirements, documentation |

3. **Create preliminary compliance matrix** mapping ER clauses to specification sections:

   **Matrix Format (table or spreadsheet per project convention **TBD**):**

   | ER Volume | ER Clause | ER Requirement Summary | Specification Section | Compliance Status | Notes |
   |-----------|-----------|------------------------|----------------------|------------------|-------|
   | Vol 2 Pt 1 | **TBD** | (Performance requirement — e.g., unloading rate) | Section 5.1 or 7.1 | Addressed / TBD / N/A | (Notes if TBD or N/A with justification) |
   | Vol 2 Pt 1 | **TBD** | (Material requirement — e.g., food-grade materials) | Section 5.2, 6.2, 7.2 | Addressed / TBD / N/A | (Notes) |
   | Vol 2 Pt 2 | **TBD** | (Standard/code requirement — e.g., ASME B31.3 compliance) | Section 1.4, 7.3 | Addressed / TBD / N/A | (Notes) |
   | Vol 2 Pt 3 | **TBD** | (QA requirement — e.g., welding inspection) | Section 8.1, 8.2 | Addressed / TBD / N/A | (Notes) |
   | (etc.) | (etc.) | (etc.) | (etc.) | (etc.) | (etc.) |

   **Compliance Status Definitions:**
   - **Addressed:** ER requirement addressed in specified section of this specification
   - **TBD:** ER requirement identified but specification section not yet developed (to be addressed during Step 3 content drafting)
   - **N/A (Not Applicable):** ER requirement not applicable to PKG-10 scope (justify why not applicable)

4. **Document any missing or unclear requirements as TBD:**
   - If ER clause unclear or ambiguous: document question, mark TBD, request clarification from Employer if needed
   - If ER clause conflicts with code/standard: document conflict, mark TBD, request ruling (see Guidance.md Conflict Table)
   - If ER clause requires information not yet available (e.g., vendor data): mark TBD, note required information and source

5. **Obtain technical reviewer confirmation** of ER clause identification:
   - Technical reviewer reviews preliminary compliance matrix for completeness (all applicable ER clauses identified)
   - Reviewer verifies clause categorization appropriate (ER clauses mapped to correct specification sections)
   - Reviewer identifies any missed ER clauses (systematic review to ensure no ER requirements overlooked)
   - Document reviewer confirmation (sign-off or email confirmation)

**Output:** Preliminary compliance matrix with ER clause mapping; filed in `1_Working/` deliverable folder (matrix will be updated during Step 3 content drafting and finalized in Step 6).

**Verification:** Technical reviewer confirmation of ER clause identification; preliminary matrix completeness verified.

**Note:** Compliance matrix is a living document during specification development. Update matrix as specification content is drafted (Step 3) and reviewed (Step 4). Final matrix issued with specification (Step 6).

---

### Step 3: Draft Specification Content

**Objective:** Develop specification content addressing all requirements from Specification.md, using approved outline from Step 1 and ER clauses from Step 2.

**Actions:**

1. **Draft specification content per approved outline** (Step 1), incorporating requirements from multiple sources:

   **a) Draft Section 1: Scope**
   - 1.1 General: PKG-10 scope elements (7 elements), 32 stations, 1,000,000 MT/annum throughput, gravity flow operation, canola oil product
   - 1.2 Inclusions: All PKG-10 scope elements per Specification.md §Scope
   - 1.3 Exclusions: Scope items excluded per Specification.md §Scope (downstream piping, electrical design, instrumentation design, control systems, structural design, rail track)
   - 1.4 Applicable Standards and Codes: List from Specification.md §Standards (ASME B31.3, CSA codes, food-grade standards, AWS, SSPC, BC Building Code, environmental regulations — all **TBD** with specific clause/section references)

   **b) Draft Section 2: References**
   - List all codes, standards, regulations, and project documents referenced in specification
   - Include clause/section numbers where specific clauses referenced (e.g., "ASME B31.3-20XX, Chapter III Pressure Design")
   - Reference DEL-10.01 (drawings), DEL-10.03 (calculations), DEL-10.04 (data sheets), DEL-10.05 (installation/test records)
   - Reference Employer's Requirements Vol 2 Parts 1–3 (with clause mapping from Step 2 compliance matrix)

   **c) Draft Section 3: Definitions and Abbreviations**
   - Define technical terms used in specification (standardize terminology per cross-document consistency)
   - Define abbreviations (NDE, WPS, IDC, ER, HAC, SPCC, etc.)

   **d) Draft Section 4: General Requirements** (applicable to all PKG-10 components):
   - 4.1 Codes and Standards Compliance: All equipment and systems shall comply with applicable codes and standards listed in Section 1.4
   - 4.2 Food-Grade Requirements: All product contact materials and surfaces shall be food-grade compatible with canola oil (per MT-01); food-grade certification required where specified; comply with applicable food-grade standards **TBD**
   - 4.3 Submittal Requirements: General submittal requirements (shop drawings for approval, product data, test procedures, test reports, material certifications, as-built data, O&M manuals); submittal timing and approval process (specific submittals detailed in Section 9)
   - 4.4 Quality Assurance: General QA requirements (inspection by qualified inspectors, testing per code and specification, documentation per DEL-10.05, non-conformance handling **TBD**)

   **e) Draft Section 5: Unloading Arm Specification** (comprehensive requirements for unloading arms, quick-connects, atmospheric venting, flow indicators):

   **5.1 Performance Requirements (per Specification.md PF-02 and ER requirements **TBD**):**
   - Flow rate: **TBD** — minimum flow rate per arm to support unloading time target (typical 50–200 m³/hr for gravity unloading; actual rate from DEL-10.03 analysis and ER requirements)
   - Operating pressure: Atmospheric to **TBD** kPa (low-pressure gravity unloading; specify maximum pressure arm must withstand)
   - Operating temperature: **TBD** — product temperature range (canola oil ambient to heated temperature if winterization required; typical 0°C to +50°C or as required)
   - Ambient temperature: **TBD** — outdoor installation, Fraser Surrey climate (-15°C to +35°C typical design range)
   - Operational envelope: Reach (horizontal reach **TBD** per DEL-10.01 arrangement — typically 3–5m to accommodate railcar positioning tolerance ±500mm), Rotation (**TBD** degrees — typically 180° or more for positioning), Vertical travel (**TBD** — accommodate railcar height variations)
   - Quick-connect performance: Dry-break function (drip-free disconnection; minimize product spillage), connection/disconnection force (**TBD** — ergonomic for operators, typically <50 lbf or <225 N for manual operation), leak-tight connection (no leakage during operation or disconnection)
   - Atmospheric venting: Vent capacity **TBD** — accommodate vapor displacement during unloading (prevent vacuum or overpressure in railcar); vent routing per DEL-10.01 drawings
   - Flow indication: Flow range **TBD** (0–200 m³/hr typical for gravity unloading or per DEL-10.03 flow rates); accuracy **TBD** (±2% to ±5% typical for local indication); local indication visible to operator

   **5.2 Material Requirements (per Specification.md MT-01, MT-04 and ER requirements **TBD**):**
   - Product contact materials: Stainless steel SS304 or SS316 preferred **PROPOSAL** (see Guidance.md §Trade-offs for aluminum alternative); food-grade certified; compatible with canola oil (verify compatibility with product properties — temperature, viscosity, chemical composition)
   - Quick-connect body: Stainless steel or aluminum (compatible with arm material selection)
   - Quick-connect seals: EPDM, Viton (FKM), PTFE, or approved food-grade elastomer; compatible with canola oil and temperature range **TBD**; food-grade certified
   - Structural materials: Stainless steel, aluminum, or coated carbon steel (non-product contact structural components; corrosion-resistant for outdoor exposure)
   - Paint/coating: **TBD** — coating system for non-product contact surfaces (surface preparation per SSPC-SP **TBD**; coating system suitable for outdoor exposure and chemical environment)

   **5.3 Workmanship Requirements (per Specification.md WK-01, WK-02, WK-04 and ER requirements **TBD**):**
   - Fabrication: Per manufacturer standards and applicable codes; welding per ASME Section IX (WPS and welder qualification required); weld quality per code acceptance criteria
   - Assembly: Per manufacturer procedures; seal installation per manufacturer requirements (proper seating, torque requirements); verify operational envelope (test full range of motion before shipment)
   - Surface finish: Product contact surfaces smooth (mill finish acceptable for stainless; 125 RMS or better where specified); no crevices, pockets, or dead legs; cleanable surfaces
   - Testing: Factory acceptance test (FAT) per manufacturer procedures (operational test — full range of motion, locking mechanisms, quick-connect operation; leak test at quick-connect); witness FAT if specified **TBD**; document results
   - Painting/coating: Surface preparation per SSPC-SP **TBD** (non-product contact surfaces); coating system per Section 5.2; coating thickness per manufacturer specification; touch-up after installation
   - Cleanliness: Pre-commissioning cleaning per WK-03 (remove mill scale, fabrication debris, preservatives); cleaning procedure **TBD**; verification before shipment

   **5.4 Interface Requirements (per Specification.md IF-01, IF-04):**
   - Railcar connection (IF-01): Quick-connect compatible with standard railcar bottom outlet (typically 3" or 4" API bottom outlet); verify railcar fleet compatibility with PKG-07
   - Structural supports (IF-02): Arm loads for structural design (static, operational, dynamic, seismic — **TBD** from vendor data or calculations); anchor bolt requirements; coordinate with PKG-05
   - Instrumentation (IF-04): Flow indicator specifications (flow range, accuracy, signal output if required — coordinate with PKG-20); mounting and process connection details

   **f) Draft Section 6: Containment System Specification** (comprehensive requirements for containment pans, sumps, drains, sump pumps):

   **6.1 Performance Requirements (per Specification.md PF-04 and ER requirements **TBD**):**
   - Containment volume: Per DEL-10.03 calculations (largest credible spill — typically one railcar capacity ~100–150 m³ per station or per regulatory requirements **TBD**); verify against regulatory minimums (110% of largest vessel typical or 100% + freeboard)
   - Drainage time: **TBD** — sump pump capacity to evacuate containment within acceptable time (regulatory requirement or operational requirement **TBD**; typical 4–24 hours depending on regulations)
   - Structural capacity: Contain liquid load (full containment volume — heavy when full; calculate load from volume and product density); contain equipment loads (sump pump weight, access loads if personnel access required); seismic loads per BC Building Code **TBD**
   - Sump capacity: **TBD** — sump volume per DEL-10.03 calculations (account for drainage from pans, pump cycling, high-level alarm offset)
   - Pump capacity: **TBD** — sump pump flow rate to achieve required drainage time; pump head per sump depth and discharge piping (coordinate with PKG-14 if sump discharge to process system or separate drainage system)

   **6.2 Material Requirements (per Specification.md MT-03 and ER requirements **TBD**):**
   - Containment pan materials: Coated carbon steel (epoxy or polyurethane coating) **PROPOSAL** or stainless steel SS304 preferred alternative (see Guidance.md §Trade-offs for material selection trade-off); corrosion-resistant; liquid-tight construction (welded, no bolted joints at liquid boundary); cleanable surfaces
   - Drain materials: Stainless steel, PVC, or HDPE (compatible with canola oil and outdoor environment; sized per drainage requirements)
   - Sump materials: Coated carbon steel or stainless steel (same considerations as containment pans; liquid-tight construction)
   - Sump pump materials: Wetted parts stainless steel or coated cast iron (compatible with canola oil and outdoor/wet environment); seals compatible with canola oil per MT-04; motor suitable for outdoor installation and area classification **TBD** (TEFC enclosure typical; rated for classified area or located in unclassified area)

   **6.3 Workmanship Requirements (per Specification.md WK-01, WK-04 and ER requirements **TBD**):**
   - Welding: Per ASME B31.3 or AWS D1.1 (containment pans and sumps — structural or pressure boundary welding per applicable code); WPS and welder qualification required; full penetration welds for liquid-tight construction; weld inspection and NDE per code (visual minimum; RT or UT if required by code or service criticality)
   - Surface preparation: For coated steel: surface preparation per SSPC-SP **TBD** (blast cleaning for coating adhesion); For stainless: mill finish acceptable (no coating required)
   - Coating application: If coated steel: coating system per Section 6.2 (primer + finish coats); coating thickness per manufacturer specification; application per manufacturer requirements (environmental conditions, surface conditions); coating inspection (visual, thickness measurement)
   - Leak testing: All containment pans and sumps shall be leak tested before installation (fill with water, observe for leaks for 24 hours minimum or per specification **TBD**; no leakage acceptable; repair leaks and retest); document test results
   - Sump pump installation: Install per manufacturer requirements; verify mounting secure; verify suction screen installed and clear; verify discharge piping connected and supported

   **6.4 Interface Requirements (per Specification.md IF-02, IF-03, IF-04):**
   - Structural supports (IF-02): Containment and sump loads for structural design (liquid load, equipment loads, seismic loads — **TBD** from DEL-10.03 or design analysis); coordinate with PKG-05 for support design
   - Electrical power (IF-03): Sump pump electrical requirements (voltage, power, motor type suitable for outdoor and area classification **TBD**); control interface (manual/automatic via level switches); coordinate with PKG-17
   - Instrumentation (IF-04): Level switch specifications for sumps (type, set points — high alarm, pump start/stop; electrical rating; area classification compatible); coordinate with PKG-20

   **g) Draft Section 7: Header Pipe Specification** (comprehensive requirements for gravity flow header, valves, fittings, supports):

   **7.1 Performance Requirements (per Specification.md PF-03 and ER requirements **TBD**):**
   - Flow capacity: Per DEL-10.03 calculations (header sized for simultaneous operations **TBD**; typically 200–500 m³/hr or per throughput analysis); verify capacity adequate for 1,000,000 MT/annum throughput
   - Pressure rating: **TBD** — design pressure per service (low-pressure gravity flow; atmospheric to +X kPa maximum pressure; account for static head, pressure drop, surge if applicable)
   - Drainage capability: Complete drainage for cleaning/maintenance (minimum 1:100 slope per DEL-10.01 Header Layout; low-point drains if required); no stagnant zones or dead legs
   - Air release: Automatic air release valves at high points (prevent vapor lock; maintain gravity flow); air release valve sizing **TBD** per vent capacity requirements
   - Isolation valves: Isolation valves at strategic locations for operational flexibility (station isolation, section isolation, header isolation for maintenance — per OBJ-4); valve type, size, operator per service

   **7.2 Material Requirements (per Specification.md MT-02 and ER requirements **TBD**):**
   - Pipe material: Stainless steel SS304 or SS316 preferred **PROPOSAL** (see Guidance.md §Trade-offs for carbon steel alternative); material per ASME B31.3 (material selection for service, temperature, pressure); pipe wall thickness per code (pressure design + corrosion allowance); food-grade compatible for product contact
   - Valve materials: Body and wetted parts compatible with header pipe material (stainless or carbon steel per pipe material selection); seals compatible with canola oil and temperature range (per MT-04); valve type per service (isolation valves: gate or ball valve — full bore for pigging capability if required; air release valves: automatic air release type)
   - Fitting materials: Compatible with pipe material (same material to avoid galvanic corrosion); fittings per code (ASME B16.9 for wrought fittings, ASME B16.5 for flanges)
   - Pipe support materials: Structural steel (painted or galvanized for outdoor exposure); support design per code (ASME B31.3 support spacing, loads); coordinate with PKG-05/PKG-06 for support installation

   **7.3 Workmanship Requirements (per Specification.md WK-01, WK-04 and ER requirements **TBD**):**
   - Welding: Per ASME B31.3 Section 328 (welding requirements); WPS required for all production welding (qualified per ASME Section IX); welder qualification per ASME Section IX; NDE per code (extent and method per service and code requirements — visual, RT, UT, MT, or PT per joint type and service class); weld acceptance criteria per code; weld repairs per code (if defects found, repair per qualified repair procedure, re-examine)
   - Pipe support installation: Supports installed per DEL-10.01 Header Layout (locations coordinated with PKG-05/PKG-06); support types per design (guide, anchor, slide); installation per code (welding, bolting, alignment); allow for thermal expansion if applicable (expansion loops, sliding supports, or expansion joints)
   - Pressure testing: Hydrostatic test per ASME B31.3 (test pressure = 1.5× design pressure or per code; hold time per code — typically 10 minutes minimum; test medium water with corrosion inhibitor if extended duration; drain and dry after test; inspector witness required; document test results including pressure gauge calibration, test duration, pressure readings, any leaks/defects, repairs, retest)
   - Leak testing: Soap solution or other leak detection method at all connections, flanges, valves, fittings (during or after pressure test; verify no leakage; document results)
   - Surface preparation and coating: Non-product contact external surfaces: surface preparation per SSPC-SP **TBD** (blast cleaning); coating system per Section 7.2 (primer + finish coats suitable for outdoor exposure and chemical environment); coating thickness per manufacturer specification (verify with coating thickness gauge); application per manufacturer requirements (temperature, humidity, surface conditions); field touch-up after installation, welding, damage; coating inspection (visual, thickness measurement, adhesion testing if required)

   **7.4 Interface Requirements (per Specification.md IF-02, IF-05):**
   - Structural supports (IF-02): Header pipe loads for structural design (pipe weight, product weight when full, insulation weight if applicable, thermal expansion forces, seismic loads per BC Building Code **TBD**); pipe support types and locations per design (coordinate with PKG-05/PKG-06)
   - Downstream piping connection (IF-05): Header discharge connection specifications (size per header pipe size from DEL-10.03 — typically 6" to 12" or larger **TBD**; pressure rating per design pressure — ANSI 150# or 300# **TBD**; flange type/rating per ASME B16.5); isolation valve at connection point (valve type: gate or ball valve full bore; size per header size; operator: manual typical **TBD**; responsibility boundary: PKG-10 provides valve, PKG-14 connects downstream); material compatibility with downstream piping (same material preferred; coordinate with PKG-14 to avoid galvanic corrosion)

   **h) Draft Section 8: Quality Assurance and Testing** (comprehensive QA, inspection, and testing requirements per Specification.md WK-xx and QA-xx):
   - 8.1 Inspection Requirements: Weld inspection (visual inspection of all welds; NDE per code and Section 5.3, 6.3, 7.3); surface inspection (product contact surfaces per food-grade requirements; coating inspection for painted/coated surfaces); dimensional inspection (verify dimensions per drawings DEL-10.01 and data sheets DEL-10.04; verify clearances and fits)
   - 8.2 Non-Destructive Examination: NDE methods (RT, UT, MT, PT per code and service); NDE extent (percentage of welds examined per code — may be spot examination or 100% depending on service class and code); NDE procedures (qualified procedures per code; qualified NDE technicians); acceptance criteria per code (workmanship standards for each NDE method); NDE reports documenting examinations, results, accept/reject, repairs
   - 8.3 Pressure Testing: Hydrostatic test per ASME B31.3 and Section 7.3 (test pressure 1.5× design pressure; hold time per code; test medium water; inspector witness; test records)
   - 8.4 Leak Testing: Leak test per Section 5.3, 6.3, 7.3 (soap solution or other method; all connections, flanges, seals; no leakage acceptable; document results)
   - 8.5 Functional Testing: Unloading arms (operational test per Section 5.3 — full range of motion, locking mechanisms, quick-connect operation; witness FAT if specified **TBD**); sump pumps (pump performance test per manufacturer — flow rate, head, controls; witness test if specified **TBD**); valves (stroke test — open/close operation, seating; verify no leakage past seat)
   - 8.6 Acceptance Criteria: All inspections and tests shall meet acceptance criteria specified in relevant sections (5.3, 6.3, 7.3, 8.1–8.5); deficiencies shall be corrected and re-inspected/retested; final acceptance by inspector/reviewer sign-off
   - 8.7 Test Records: All inspections and tests shall be documented per DEL-10.05 (test records, inspection reports, NDE reports, certifications, witness sign-offs); records submitted for approval before equipment installation or system commissioning

   **i) Draft Section 9: Submittals and Documentation** (submittal requirements per Specification.md QA-xx and ER **TBD**):
   - 9.1 Submittal Requirements: Shop drawings (equipment fabrication drawings, assembly drawings — submit for approval before fabrication); product data (manufacturer catalog data, technical data sheets, performance curves — submit for information or approval per specification **TBD**); test procedures (pressure test procedures, NDE procedures, functional test procedures — submit for review before testing); test reports (pressure test reports, NDE reports, functional test reports — submit after testing for acceptance); material certifications (mill test reports, material certificates, food-grade certifications — submit with test reports); as-built data (final as-installed dimensions, configurations — submit for DEL-10.04 data sheets); O&M manuals (operation and maintenance manuals for all equipment — submit before commissioning)
   - 9.2 Submittal Schedule: Submittal timing coordinated with procurement and construction schedule (shop drawings early for approval before fabrication; test reports during fabrication/installation; as-built data and O&M manuals before commissioning)
   - 9.3 Data Sheets: 32 unloading arm data sheets per DEL-10.04 (implement this specification for individual arms); sump pump data sheets per DEL-10.04 (if pumps included); flow indicator data sheets (coordinate with PKG-20 or include in DEL-10.04 **TBD**)

   **j) Draft Section 10: Appendices:**
   - Appendix A: Compliance Matrix (ER clause to specification section mapping from Step 2; update during content drafting; finalize in Step 6)
   - Appendix B: Reference Drawings (list drawings from DEL-10.01 referenced in specification sections — GA, Arm Arrangement, Header Layout, Containment Details)
   - Other appendices as needed (e.g., typical details, standard data sheet formats, test report templates)

2. **Apply Guidance.md principles and considerations** (verify specification content aligns with guidance):
   - **Performance-based requirements:** Specify outcomes (flow rate, pressure rating) rather than prescriptive designs (allow vendor solutions); clear acceptance criteria for all performance requirements
   - **Material compatibility:** All product contact materials food-grade compatible (MT-01); verify compatibility with canola oil product properties (Guidance.md §Considerations — product properties)
   - **Code compliance:** All requirements reference applicable codes (ASME B31.3, AWS, food-grade standards, environmental regulations); code-compliant design, fabrication, testing
   - **Verifiability:** All requirements verifiable by inspection, test, calculation, or certification (specify verification method for each requirement)
   - **Traceability:** Compliance matrix maps all ER clauses to specification sections (QA-01)
   - **Apply design considerations:** Product properties (viscosity, temperature, food-grade), throughput (32 stations, 1,000,000 MT/annum), gravity flow (slopes, air release), environmental protection (containment volume, leak-tight construction), site conditions (climate, seismic, HAC), operational flexibility (isolation provisions)
   - **Apply material selection considerations:** Unloading arms (aluminum or stainless — trade-off per Guidance.md §Trade-offs), quick-connects (seals compatible with product), header piping (carbon steel or stainless — trade-off per Guidance.md §Trade-offs), containment (coated steel or stainless — trade-off per Guidance.md §Trade-offs)
   - **Apply workmanship considerations:** Welding per code, surface finish for food-grade, cleanliness pre-commissioning, testing comprehensive (pressure, leak, functional)

3. **Incorporate DEL-10.03 calculation results** for performance requirements:
   - Header sizing (pipe sizes, pressure ratings from hydraulic calculations) → Section 7.1 performance requirements
   - Containment volume (pan sizing, sump sizing from spill volume calculations) → Section 6.1 performance requirements
   - Throughput analysis (verify 32 stations achieve 1,000,000 MT/annum; simultaneous operations required **TBD**) → Section 5.1 and overall performance requirements
   - Equipment loads (for structural coordination) → Sections 5.4, 6.4, 7.4 interface requirements with PKG-05

4. **Reference DEL-10.01 drawings** for physical arrangement and interfaces:
   - Arm arrangement from DEL-10.01 → Section 5.1 operational envelope requirements (reach, rotation based on arrangement)
   - Header layout from DEL-10.01 → Section 7.1 performance requirements (routing, slopes, valves based on layout)
   - Containment arrangement from DEL-10.01 → Section 6.1 performance requirements (configuration based on arrangement)
   - Interface points from DEL-10.01 → Sections 5.4, 6.4, 7.4 interface requirements (interface locations and details per drawings)

5. **Populate document metadata** per Datasheet.md §Attributes:
   - Document number: **TBD** — per project document numbering procedure (coordinate with document control)
   - Document title: "Railcar Unloading Technical Specification" or per project naming convention **TBD**
   - Revision: Initial issue (0 or A per convention **TBD**)
   - Date: Specification preparation date (updated on each revision)
   - Author: Specification author name
   - Document header/footer: Project name, location, client, contractor, document number, revision, date (per project template **TBD**)
   - Classification: Per project requirements **TBD**

6. **Apply cross-references** throughout specification (ensure traceability):
   - Reference to Employer's Requirements (cite ER clauses where requirements derived from ER — use compliance matrix for comprehensive mapping)
   - Reference to codes and standards (cite specific code sections where requirements derived from code — e.g., "per ASME B31.3 Section 328.4")
   - Reference to DEL-10.01 drawings (cite drawing numbers where arrangement or details referenced — e.g., "per DEL-10.01 Dwg **TBD**-GA-001")
   - Reference to DEL-10.03 calculations (cite calculation numbers where sizing or performance based on calculations — e.g., "header size per DEL-10.03 Calculation **TBD**")
   - Reference to DEL-10.04 data sheets (note that data sheets implement specification for individual equipment)
   - Reference to DEL-10.05 installation/test records (note that installation and testing per specification requirements documented in DEL-10.05)
   - Internal cross-references within specification (e.g., "seal materials per Section 5.2" when referenced in another section)

7. **Update compliance matrix** (Step 2 preliminary matrix) as specification content is drafted:
   - As each specification section is drafted, verify ER clauses addressed (mark "Addressed" in compliance matrix)
   - If ER clause cannot be addressed yet (missing information), mark "TBD" with note explaining what's needed
   - If ER clause not applicable to PKG-10, mark "N/A" with justification
   - Maintain matrix current with specification content

**Output:** Draft Technical Specification (all 10 sections drafted per outline) and updated compliance matrix; ready for technical review (Step 4).

**Traceability to Specification.md Requirements (verify all requirements addressed in specification content):**

| Requirement | Specification Section(s) | Content Verification | Status after Step 3 |
|-------------|-------------------------|---------------------|---------------------|
| FN-01: Performance requirements for all scope elements | Sections 5.1, 6.1, 7.1 (Performance subsections) | All 7 PKG-10 scope elements have performance requirements specified | ✓ Draft complete |
| FN-02: Material requirements for all scope elements | Sections 5.2, 6.2, 7.2 (Material subsections) | All scope elements have material requirements with food-grade compatibility | ✓ Draft complete |
| FN-03: Workmanship requirements for all scope elements | Sections 5.3, 6.3, 7.3 (Workmanship subsections), Section 8 (QA/Testing) | All scope elements have fabrication, installation, testing requirements | ✓ Draft complete |
| FN-04: Anticipated artifacts (3 specification sections) | Sections 5, 6, 7 | 3 specification sections drafted per approved outline | ✓ Draft complete |
| FN-05: 32 stations, gravity flow | Sections 5.1, 7.1 | Requirements support 32 stations with gravity flow operation | ✓ Draft complete |
| FN-06: Food-grade compatibility | Sections 4.2 (General), 5.2, 6.2, 7.2 (Materials), 5.3, 6.3 (Workmanship — surface finish) | Food-grade requirements specified for all product contact materials and surfaces | ✓ Draft complete |
| PF-01 through PF-06: Performance requirements | Sections 5.1, 6.1, 7.1 (Performance subsections) | Performance requirements from DEL-10.03 calculations and ER **TBD** | Draft complete; verify with DEL-10.03 |
| MT-01 through MT-05: Material requirements | Sections 5.2, 6.2, 7.2 (Material subsections) | Material requirements specified; trade-offs identified for human ruling | Draft complete; trade-offs require ruling |
| WK-01 through WK-05: Workmanship requirements | Sections 5.3, 6.3, 7.3 (Workmanship subsections), Section 8 (QA/Testing) | Workmanship requirements per code and industry practice | ✓ Draft complete |
| IF-01 through IF-06: Interface requirements | Sections 5.4, 6.4, 7.4 (Interface subsections) | Interface requirements defined; prepare for IDC (Step 5) | Draft complete; ready for IDC |
| QA-01: Compliance matrix | Appendix A | Matrix developed in Step 2; updated during Step 3; to be finalized in Step 6 | ✓ Draft complete; requires review/finalization |

---

### Step 4: Technical Review

**Objective:** Verify specification completeness, technical accuracy, code compliance, and verifiability through independent technical review.

**Actions:**

1. **Issue draft specification and compliance matrix for technical review:**
   - Assign technical reviewer (must be independent from specification author per Specification.md QA-03)
   - Provide reviewer with complete review package:
     - Draft Technical Specification (all 10 sections)
     - Compliance Matrix (Appendix A showing ER clause mapping)
     - Specification.md (requirements to be verified)
     - Guidance.md (principles and considerations to be verified)
     - Datasheet.md (scope elements and attributes to be verified)
     - DEL-10.03 calculations (performance requirements basis — verify specification requirements consistent with calculations)
     - DEL-10.01 drawings (arrangement basis — verify specification requirements consistent with layout)
     - Applicable codes and standards (for code compliance verification)
     - Employer's Requirements Vol 2 (for ER compliance verification)

2. **Technical reviewer checks specification against all requirements** (per Specification.md §Verification):

   **a) Specification.md requirements verification:**
   - **FN-01 through FN-07:** Functional requirements
     - Verify all 7 PKG-10 scope elements have specified performance, material, workmanship requirements (check Sections 5, 6, 7 for completeness)
     - Verify 3 anticipated specification sections included (Unloading Arm, Containment System, Header Pipe — Sections 5, 6, 7)
     - Verify 32 stations and gravity flow operation addressed in requirements (Sections 5.1, 7.1)
     - Verify food-grade compatibility requirements specified for all product contact (Sections 4.2, 5.2, 6.2, 7.2)
   - **PF-01 through PF-06:** Performance requirements
     - Verify throughput capacity requirements (1,000,000 MT/annum) addressed (Section 5.1, 7.1; cross-check with DEL-10.03 throughput analysis)
     - Verify header performance requirements based on DEL-10.03 calculations (flow capacity, pressure drop, drainage — verify specification Section 7.1 consistent with DEL-10.03 header sizing)
     - Verify containment performance requirements based on DEL-10.03 calculations (containment volume, sump sizing — verify specification Section 6.1 consistent with DEL-10.03 containment calculations)
     - Verify unloading arm performance requirements realistic and achievable (flow rate, pressure, temperature, operational envelope — cross-check with vendor literature or industry precedents if available)
   - **MT-01 through MT-05:** Material requirements
     - Verify food-grade materials specified for product contact (all product contact materials — arms, quick-connects, header piping, pump wetted parts)
     - Verify material selections appropriate for service (canola oil compatibility, temperature compatibility, outdoor exposure, corrosion resistance)
     - Verify material selections code-compliant (materials per ASME B31.3 for piping, per applicable codes for other equipment)
     - Verify seal materials compatible with product and temperature (verify seal material selections per product compatibility data)
   - **WK-01 through WK-05:** Workmanship requirements
     - Verify welding requirements per applicable codes (ASME B31.3, AWS D1.1, ASME Section IX — verify requirements correctly cited and applied)
     - Verify surface finish requirements appropriate for food-grade service (smooth finishes, no crevices, cleanable surfaces)
     - Verify cleanliness requirements adequate for food-grade commissioning (cleaning procedures, verification methods)
     - Verify testing requirements per code and adequate for verification (pressure testing per code, leak testing comprehensive, functional testing per manufacturer requirements)
   - **IF-01 through IF-06:** Interface requirements
     - Verify interface requirements identified for all interfaces (PKG-05, PKG-07, PKG-14, PKG-17, PKG-20, others as applicable)
     - Verify interface requirements clear and complete (loads, connection details, coordination requirements specified)
     - Prepare for IDC (Step 5) — verify interface requirements ready for coordination with other disciplines
   - **QA-01 through QA-06:** Quality requirements
     - Verify compliance matrix complete (all ER clauses mapped to specification sections — review matrix for gaps or omissions)
     - Verify document metadata complete per Datasheet.md §Attributes
     - (QA-03 is this step — technical review being performed)
     - Verify specification ready for IDC review (interface requirements complete — Step 5 preparation)

   **b) Guidance.md principles verification:**
   - Verify **performance-based requirements** principle applied: requirements specify outcomes (flow rate, capacity, envelope) rather than prescriptive designs (except where code requires specific approach); allows vendor flexibility and optimization
   - Verify **material compatibility** principle applied: all product contact materials food-grade compatible with canola oil; compatibility verified or specified for verification
   - Verify **code compliance** principle applied: all requirements reference applicable codes (ASME B31.3, AWS, food-grade standards, etc.); code-compliant design and construction specified
   - Verify **verifiability** principle applied: all requirements have verification method specified (inspection, testing, calculation, certification); no unverifiable subjective requirements
   - Verify **traceability** principle applied: compliance matrix maps ER to specification; requirements traceable to sources

   **c) Code and standard compliance:**
   - Verify material requirements per ASME B31.3 (piping materials per code material selection tables; verify code compliance)
   - Verify welding requirements per ASME B31.3, AWS D1.1, ASME Section IX (welding procedures, welder qualification, NDE, acceptance criteria per code)
   - Verify testing requirements per ASME B31.3 (pressure testing per code requirements; verify test pressure, hold time, test medium, witnessing per code)
   - Verify food-grade requirements per applicable food-grade standards **TBD** (material certifications, surface finish requirements, cleanliness requirements per standards)
   - Verify coating requirements per SSPC standards **TBD** (surface preparation, coating application, inspection per standards)

   **d) Completeness and consistency:**
   - Verify all PKG-10 scope elements addressed (check each of 7 scope elements has requirements in appropriate sections)
   - Verify specification sections complete (all subsections per outline drafted; no missing sections)
   - Verify requirements internally consistent (no contradictions within specification; same values throughout; consistent terminology)
   - Verify cross-document consistency (specification consistent with Datasheet, Guidance, Procedure; consistent with DEL-10.01 drawings and DEL-10.03 calculations)

   **e) Clarity and verifiability:**
   - Verify requirements clear and unambiguous (specific values where applicable; objective criteria; no vague terms like "adequate" or "suitable" without defining criteria)
   - Verify requirements verifiable (inspection method, test method, calculation method, or certification method specified for each requirement)
   - Verify acceptance criteria clear (pass/fail criteria specified for all inspections and tests)

3. **Reviewer documents review comments:**
   - Review comments identify issues: errors (technical errors, code compliance errors, requirement gaps), omissions (missing requirements, missing scope elements, missing verification methods), clarifications (unclear requirements, ambiguous language, missing criteria), suggestions (improvements, optimization, alternative approaches)
   - Comment list or review report (comment number, section reference, comment description, severity — error/omission/clarification/suggestion)

4. **Verify compliance matrix completeness:**
   - Reviewer checks that all ER clauses identified in Step 2 are addressed in specification (each ER clause mapped to specification section; all ER clauses status "Addressed" or justified "TBD" or "N/A")
   - Reviewer verifies no ER requirements overlooked (systematic review of ER volumes to ensure comprehensive coverage)
   - Reviewer verifies matrix format appropriate **TBD** (if ER specifies matrix format, verify compliance; otherwise use project standard format)

5. **Resolve review comments:**
   - Specification author reviews technical reviewer comments
   - Resolve all "errors" and "omissions" comments (correct technical errors, add missing requirements, fill gaps)
   - Address "clarifications" and "suggestions" as appropriate (clarify unclear requirements, add missing criteria, consider improvement suggestions)
   - Update specification with agreed changes (incorporate corrections, additions, clarifications)
   - Update compliance matrix if review identifies additional ER clauses or gaps in ER coverage
   - Respond to reviewer on disposition of each comment (comment response log: comment number, disposition — accepted/revised/rejected, explanation if rejected or revised differently)

6. **Update specification and compliance matrix:**
   - Incorporate all agreed changes into specification document (revised specification ready for IDC Step 5)
   - Update compliance matrix with any changes from technical review (additional ER clauses, revised section mappings, status updates)
   - Update document metadata (revision date, author, reviewer)

**Output:** Technically reviewed specification with all review comments resolved; updated compliance matrix; ready for IDC (Step 5).

**Verification:** Technical reviewer sign-off (Specification.md QA-03) confirming technical review complete and critical issues resolved; review comment resolution record filed.

---

### Step 5: Interdisciplinary Coordination (IDC)

**Objective:** Coordinate interface requirements with adjacent disciplines per Specification.md IF-xx requirements (IF-01 through IF-06) to ensure specification alignment across disciplines.

**Actions:**

1. **Prepare for IDC:**
   - Issue specification for IDC review (provide copies to all interface disciplines)
   - Prepare interface coordination list identifying specific interface requirements in specification (extract interface requirements from Sections 5.4, 6.4, 7.4 and list for each discipline)
   - Schedule IDC meeting or distributed review (coordinate with IDC Coordinator)
   - Distribute specification and interface list in advance (allow review time — typically 1–2 weeks)

2. **Conduct IDC review** for each interface (per Specification.md IF-01 through IF-06; refer to Guidance.md §Interface Considerations):

   **IF-01: Rail track alignment and railcar positioning (PKG-07 Rail Works)**
   - **Specification Section:** Section 5.4 (Unloading Arm interface requirements)
   - **Coordination Actions:**
     - Review arm specifications with PKG-07: verify arm reach envelope accommodates track geometry (station spacing, track curvature per PKG-07 track layout)
     - Confirm railcar positioning tolerance (verify arm reach accommodates positioning variation ±500mm typical or per PKG-07 railcar positioning specification)
     - Verify quick-connect specifications compatible with railcar bottom outlets (verify connection size, type, coupler configuration compatible with expected railcar fleet — coordinate with PKG-07 for railcar specifications or historical railcar data)
   - **Resolution:** Document agreements; update specification if changes required; obtain PKG-07 sign-off on interface

   **IF-02: Structural supports and foundations (PKG-05 Concrete Structures / PKG-06 Structural Steelwork)**
   - **Specification Sections:** Sections 5.4, 6.4, 7.4 (Interface requirements in all sections — equipment loads)
   - **Coordination Actions:**
     - Review equipment load requirements with PKG-05/PKG-06: verify loads specified in specification adequate and correct (arm loads, header pipe loads, containment loads — static, operational, seismic)
     - Coordinate anchor/connection details: base plate requirements, anchor bolt size/type/embedment, connection design for load transfer
     - Coordinate seismic requirements: verify seismic design criteria consistent between process and structural disciplines (BC Building Code criteria, site-specific seismic parameters from PKG-02 geotechnical study **TBD**)
     - Coordinate thermal expansion: if header piping has significant thermal expansion (temperature variations or long pipe runs), coordinate expansion provisions (expansion loops, expansion joints, sliding supports) with pipe support design
   - **Resolution:** Document load values and connection details; update specification if load values revised; obtain PKG-05/PKG-06 sign-off on interface

   **IF-03: Electrical power for sump pumps (PKG-17 Electrical)**
   - **Specification Section:** Section 6.4 (Containment System interface requirements)
   - **Coordination Actions:**
     - Review sump pump electrical requirements with PKG-17: verify voltage, power, motor type specified in specification align with PKG-17 electrical design (voltage available, load capacity)
     - Coordinate control requirements: manual/automatic pump operation (coordinate control interface with level switches if automatic; verify control voltage and logic with PKG-17 and PKG-21 if applicable)
     - Coordinate hazardous area classification compatibility: verify pump motor specifications suitable for area classification (motor rated for classified area **TBD** or located in unclassified area; coordinate with PKG-17 HAC design)
   - **Resolution:** Document electrical requirements and control interface; update specification if electrical requirements revised; obtain PKG-17 sign-off on interface

   **IF-04: Instrumentation (flow indicators and level switches) (PKG-20 Field Instrumentation)**
   - **Specification Sections:** Section 5.4 (flow indicators), Section 6.4 (level switches)
   - **Coordination Actions:**
     - Review flow indicator specifications with PKG-20: verify flow range, accuracy, indication type, signal output (if remote indication required **TBD**) align with PKG-20 instrumentation design and project I&C standards
     - Review level switch specifications with PKG-20: verify level switch type, set points (high alarm, pump start/stop), electrical rating, area classification compatibility align with PKG-20 design
     - Coordinate installation requirements: process connection size/type, mounting details, cable/conduit routing (coordinate with PKG-20 for installation standards)
   - **Resolution:** Document instrument specifications and installation requirements; update specification if instrument requirements revised; obtain PKG-20 sign-off on interface

   **IF-05: Downstream process piping (PKG-14 Process Piping)**
   - **Specification Section:** Section 7.4 (Header Pipe interface requirements)
   - **Coordination Actions:**
     - Review header discharge connection requirements with PKG-14: verify connection size, pressure rating, flange type/rating specified in specification match PKG-14 piping design at connection point
     - Coordinate isolation valve at connection point: verify valve type, size, operator specified in specification align with PKG-14 expectations; clarify responsibility boundary (PKG-10 provides isolation valve, PKG-14 connects downstream of valve — confirm boundary with PKG-14)
     - Coordinate material compatibility: verify header pipe material compatible with downstream piping material (same material preferred to avoid galvanic corrosion; coordinate with PKG-14 piping material selection; if dissimilar metals required, specify insulating gaskets or other galvanic corrosion prevention)
   - **Resolution:** Document connection requirements and responsibility boundary; update specification if connection details revised; obtain PKG-14 sign-off on interface

   **IF-06: Other interfaces as identified**
   - **Specification Sections:** Various (as applicable)
   - **Coordination Actions:** Coordinate any additional interfaces identified during ER review (Step 2) or technical review (Step 4) — e.g., control systems PKG-21 if automated control, fire protection if applicable, utilities if required
   - **Resolution:** Document additional interface requirements; update specification as needed; obtain sign-offs from additional disciplines

3. **IDC meeting / comment resolution:**
   - Conduct IDC meeting or distributed review (all interface disciplines review specification and provide comments)
   - Document interface agreements and action items (IDC meeting minutes or interface coordination record)
   - Document conflicts requiring resolution (if interface conflicts identified between PKG-10 specification and other discipline specifications or designs)
   - Assign responsibilities for conflict resolution (typically discipline leads; may require project management decision if conflict cannot be resolved at technical level)
   - Agree on schedule for conflict resolution and re-review if needed

4. **Incorporate agreed changes:**
   - Update specification per IDC agreements (incorporate agreed changes to interface requirements; clarify interface details; resolve conflicts per agreed approach)
   - Update cross-references if other discipline deliverable numbers are known (e.g., reference PKG-05 foundation drawing number if known)
   - Mark interfaces as "coordinated" in specification (note in interface sections: "Coordinated with PKG-XX" or per project convention)

5. **Obtain IDC sign-offs:**
   - Prepare IDC sign-off sheet listing all interface disciplines and their sign-off status:
     - IF-01: PKG-07 Rail Works (arm reach and railcar compatibility)
     - IF-02: PKG-05 Concrete Structures / PKG-06 Structural Steelwork (equipment loads and connection details)
     - IF-03: PKG-17 Electrical (pump power and HAC compatibility)
     - IF-04: PKG-20 Field Instrumentation (flow indicators and level switches)
     - IF-05: PKG-14 Process Piping (header discharge connection and material compatibility)
     - IF-06: Others as identified
   - Circulate IDC sign-off sheet to all interface disciplines (obtain signatures or email confirmations)
   - File IDC sign-off sheet in `1_Working/` deliverable folder (retain as record of interface coordination per Specification.md QA-04)

**Output:** IDC-coordinated specification with all interface requirements coordinated and signed off by all affected disciplines.

**Verification:** IDC sign-off sheet with signatures from all interface disciplines (Specification.md QA-04).

**Conflict Escalation:** If interface conflicts cannot be resolved at IDC level (technical disagreement, cost impact requiring management decision, schedule conflict): escalate to project management with conflict description, affected disciplines, technical analysis, and recommendation; obtain ruling; incorporate ruling into specification; re-circulate for IDC sign-off if ruling affects other disciplines.

---

### Step 6: Approval and Issue

**Objective:** Obtain discipline lead approval and issue specification with compliance matrix.

**Actions:**

1. **Submit specification and compliance matrix for discipline lead approval:**
   - Provide discipline lead with complete approval package:
     - Technical Specification (all sections; incorporating technical review and IDC changes)
     - Compliance Matrix (Appendix A; final version mapping all ER clauses)
     - Technical reviewer sign-off (from Step 4)
     - IDC sign-off sheet (from Step 5)
     - Review comment resolution record (from Step 4)
     - Supporting deliverables: DEL-10.03 calculations, DEL-10.01 drawings (for reference)

2. **Discipline lead reviews specification for:**
   - **Technical completeness:** All PKG-10 scope elements addressed with performance, material, workmanship requirements; all anticipated specification sections complete; no gaps or omissions
   - **ER compliance:** Compliance matrix demonstrates all ER requirements addressed (all ER clauses mapped to specification sections; status "Addressed" or justified "TBD"/"N/A"); specification requirements satisfy ER requirements
   - **Code compliance:** Specification requirements comply with applicable codes and standards (ASME B31.3, food-grade standards, AWS, SSPC, BC Building Code, environmental regulations)
   - **IDC coordination completeness:** All interface requirements coordinated through IDC (IDC sign-off sheet shows all interface disciplines signed; interface conflicts resolved)
   - **Appropriateness for use:** Specification suitable for intended use (procurement of equipment meeting requirements; fabrication and installation per requirements; testing and verification per requirements); specification clarity adequate for vendors and contractors

3. **Obtain discipline lead approval sign-off:**
   - Discipline lead signs approval on specification (signature on approval page or separate approval sheet per project convention)
   - Approval sign-off confirms specification approved for issue (technical adequacy confirmed, ER compliance confirmed, IDC coordination confirmed, ready for use)
   - File approval record in `1_Working/`

4. **Finalize document metadata** (Datasheet.md §Attributes):
   - Finalize document number (coordinate with document control for number assignment per project numbering procedure **TBD**)
   - Set revision to initial issue (0 or A per project convention **TBD**)
   - Set issue date (current date — date of approval or issue)
   - Verify all sign-offs present: author (specification author signature/date), reviewer (technical reviewer signature/date from Step 4), approver (discipline lead signature/date from this step)
   - Verify classification set per project requirements **TBD**
   - Verify document header/footer complete (project name, location, document number, revision, date per template **TBD**)

5. **Finalize compliance matrix** (Appendix A):
   - Review matrix for completeness (all ER clauses addressed; no gaps)
   - Update any "TBD" items (if resolved during specification development; otherwise maintain TBD with note on required information)
   - Verify matrix format appropriate (per ER requirements **TBD** or project standard)
   - Include matrix as Appendix A of specification or issue as separate document per project convention **TBD**

6. **Prepare transmittal** per project document control procedure:
   - **TBD** — Transmittal form or cover letter format per project
   - List specification document being issued: document number, title, revision, date
   - Include compliance matrix in transmittal (as appendix or separate document)
   - Identify recipients: Employer (DP World Fraser Surrey Inc.), procurement team (for equipment procurement), construction contractor (for installation standards), other disciplines for coordination (PKG-05, PKG-07, PKG-14, PKG-17, PKG-20), document control (for distribution)
   - Include transmittal purpose (e.g., "Issued for Procurement and Construction" at IFC stage, "Issued for Review" at earlier stage, "Issued for Information" if coordination only)
   - Obtain document controller sign-off on transmittal

7. **Issue specification:**
   - Submit specification and transmittal to document control for distribution
   - Document control distributes per project distribution matrix (all recipients per transmittal)
   - Document control updates document register (record document number, title, revision, issue date, distribution, transmittal number)

8. **File records** per §Records below:
   - Working records in `1_Working/`: approved outline (Step 1), preliminary compliance matrix (Step 2), draft specification (Step 3), technical review sign-off and comments (Step 4), IDC sign-off sheet (Step 5), approval sign-off (this step), transmittal record
   - Review package in `2_Checking/To/` if required per project convention (for formal Employer reviews at stage gates)
   - Issued specification in `3_Issued/`: final issued specification with compliance matrix (PDF or Word per project requirements **TBD**)

9. **Update deliverable status:**
   - **Note:** Status updates are human-managed per project workflow and lifecycle (see `_STATUS.md`)
   - This procedure does not automatically update status
   - **Typical status progression:** OPEN → INITIALIZED (after Pass 1 draft by 4_DOCUMENTS agent) → IN_PROGRESS (during Steps 1–5) → CHECKING (during Step 4 technical review) → ISSUED (after Step 6 issue)

**Output:** Issued Technical Specification with compliance matrix; transmittal record; document register updated.

**Verification:**
- Discipline lead approval sign-off (Specification.md QA-05)
- Document controller confirmation of issue (transmittal acknowledgment)
- Updated document register (confirms specification registered in project document management system)

**Note for Subsequent Revisions:**
- Subsequent specification revisions follow similar process (Steps 2–6 as applicable) with revision control:
  - Update compliance matrix if new ER clauses identified or requirements change
  - Mark revisions with revision tracking (revision history table in specification document; highlight changes or provide revision summary)
  - Update revision number (increment revision per project convention: Rev 0 → Rev 1, or Rev A → Rev B)
  - Maintain previous revision files (archive for traceability; do not overwrite previous revisions)
  - Re-issue with transmittal noting revision and changes

---

## Verification

**Verification Summary:**

| Step | Verification Activity | Responsible | Record | Specification Link | Datasheet Link |
|------|----------------------|-------------|--------|--------------------|--------------------|
| 1 | Outline approval | Discipline lead | Approved outline with sign-off | Specification.md FN-04 (anticipated artifacts requirement) | Datasheet.md §Construction (specification sections structure) |
| 2 | ER clause identification and preliminary compliance matrix | Technical reviewer | Preliminary compliance matrix with reviewer confirmation | Specification.md QA-01 (compliance matrix required) | Datasheet.md §Attributes (compliance matrix required) |
| 3 | Draft specification completion | Specification author | Draft specification (all 10 sections complete) | Specification.md FN-01 through FN-06 (all functional requirements), PF-xx, MT-xx, WK-xx (all requirements) | Datasheet.md §Construction (all specification sections completed) |
| 4 | Technical review | Technical reviewer (independent) | Technical reviewer sign-off; review comment resolution record | Specification.md QA-03 (technical review requirement) | — |
| 5 | IDC coordination | IDC coordinator / multi-discipline team | IDC sign-off sheet (all interface disciplines signed) | Specification.md IF-01 through IF-06 (all interface requirements); QA-04 (IDC sign-off required) | Datasheet.md §Conditions (interface elements) |
| 6 | Discipline lead approval | Discipline lead | Approval sign-off | Specification.md QA-05 (approval requirement) | — |
| 6 | Issue confirmation | Document controller | Transmittal record; document register entry | Specification.md §Documentation (document control requirements) | Datasheet.md §Attributes (issue metadata) |

**Requirement Verification Matrix (Traceability to Specification.md — comprehensive verification):**

| Req ID | Requirement Summary | Verification Step(s) | Verification Method | Record | Guidance Link |
|--------|---------------------|---------------------|---------------------|--------|---------------|
| FN-01 | Performance requirements for all scope elements | 3, 4 | Technical review (verify all elements addressed); specification sections 5.1, 6.1, 7.1 | Draft specification; review sign-off | Guidance.md §Principles (performance-based requirements) |
| FN-02 | Material requirements for all scope elements | 3, 4 | Material review (verify all elements addressed; food-grade compliance); specification sections 5.2, 6.2, 7.2 | Draft specification; review sign-off | Guidance.md §Principles (material compatibility); §Considerations (material selection) |
| FN-03 | Workmanship requirements for all scope elements | 3, 4 | Technical review (verify all elements addressed; code compliance); specification sections 5.3, 6.3, 7.3, 8 | Draft specification; review sign-off | Guidance.md §Workmanship (all aspects) |
| FN-04 | Anticipated artifacts (3 specification sections) | 1, 3 | Document check (verify outline approved, sections drafted); specification Sections 5, 6, 7 | Approved outline; draft specification | Guidance.md §Examples (typical specification structure) |
| FN-05 | 32 stations, gravity flow | 3, 4 | Technical review (verify requirements support 32 stations and gravity flow); specification Sections 5.1, 7.1 | Draft specification; review sign-off | Guidance.md §Principles (gravity flow design) |
| FN-06 | Food-grade compatibility | 3, 4 | Material review (verify food-grade requirements for all product contact); specification Section 4.2, 5.2, 6.2, 7.2 | Draft specification; review sign-off; material certifications | Guidance.md §Principles (material compatibility — food-grade) |
| FN-07 | Additional ER requirements | 2, 3, 4 | ER clause review (identify in Step 2); technical review (verify addressed in Step 3) | Compliance matrix; draft specification; review sign-off | — |
| PF-01 | Throughput capacity (1,000,000 MT/annum) | 3, 4 | Calculation review (DEL-10.03 throughput analysis); technical review | DEL-10.03; draft specification; review sign-off | Guidance.md §Principles (OBJ-2); §Considerations (throughput) |
| PF-02 | Arm performance requirements | 3, 4 | Technical review; calculation verification (DEL-10.03 flow analysis **TBD**); vendor data review **TBD** | Draft specification; DEL-10.03; review sign-off | Guidance.md §Considerations (material selection — arms) |
| PF-03 | Header performance requirements | 3, 4 | Calculation verification (DEL-10.03 header sizing, hydraulic analysis); technical review | DEL-10.03; draft specification; review sign-off | Guidance.md §Principles (gravity flow); §Considerations (header design) |
| PF-04 | Containment performance requirements | 3, 4 | Calculation verification (DEL-10.03 containment volume); technical review | DEL-10.03; draft specification; review sign-off | Guidance.md §Principles (OBJ-7 environmental protection); §Considerations (containment volume) |
| PF-05 | Unloading rate per station | 2, 3, 4 | ER clause review; calculation verification; technical review | Compliance matrix; DEL-10.03; review sign-off | Guidance.md §Considerations (throughput) |
| PF-06 | Additional performance requirements | 2, 3, 4 | ER clause review; technical review | Compliance matrix; review sign-off | — |
| MT-01 | Food-grade product contact materials | 3, 4 | Material review; compatibility verification; certification requirements | Draft specification; review sign-off; material certifications | Guidance.md §Principles (material compatibility); §Considerations (material selection for all components) |
| MT-02 | Piping materials per code | 3, 4 | Code compliance review (ASME B31.3); material specification review | Draft specification; review sign-off; code compliance check | Guidance.md §Trade-offs (header material selection); §Principles (code compliance) |
| MT-03 | Containment materials environmental resistance | 3, 4 | Material specification review; environmental compatibility verification | Draft specification; review sign-off | Guidance.md §Considerations (material selection — containment); §Trade-offs (containment material) |
| MT-04 | Seal materials product compatibility | 3, 4 | Material compatibility verification (supplier data or testing); temperature rating verification | Draft specification; review sign-off; material compatibility data | Guidance.md §Considerations (material selection — quick-connects, seals) |
| MT-05 | Additional material requirements | 2, 3, 4 | ER clause review; material review | Compliance matrix; review sign-off | — |
| WK-01 | Welding per code | 3, 4 | Code compliance review (ASME B31.3, AWS D1.1, ASME Section IX); technical review | Draft specification; review sign-off; code compliance check | Guidance.md §Workmanship (welding per code) |
| WK-02 | Food-grade surface finish | 3, 4 | Technical review; food-grade standards review **TBD** | Draft specification; review sign-off | Guidance.md §Workmanship (surface finish) |
| WK-03 | Pre-commissioning cleaning | 3, 4 | Technical review; cleaning procedure review | Draft specification; review sign-off | Guidance.md §Workmanship (cleanliness) |
| WK-04 | Testing per code | 3, 4 | Code compliance review (ASME B31.3 testing requirements); technical review | Draft specification; review sign-off; code compliance check | Guidance.md §Workmanship (testing per code) |
| WK-05 | Additional workmanship requirements | 2, 3, 4 | ER clause review; technical review | Compliance matrix; review sign-off | — |
| IF-01 | Rail track/railcar interface | 5 | IDC review with PKG-07 | IDC sign-off sheet (PKG-07 signed) | Guidance.md §Interface Considerations (PKG-07) |
| IF-02 | Structural supports interface | 5 | IDC review with PKG-05/PKG-06 | IDC sign-off sheet (PKG-05/PKG-06 signed) | Guidance.md §Interface Considerations (PKG-05) |
| IF-03 | Electrical interface | 5 | IDC review with PKG-17 | IDC sign-off sheet (PKG-17 signed) | Guidance.md §Interface Considerations (PKG-17) |
| IF-04 | Instrumentation interface | 5 | IDC review with PKG-20 | IDC sign-off sheet (PKG-20 signed) | Guidance.md §Interface Considerations (PKG-20) |
| IF-05 | Process piping interface | 5 | IDC review with PKG-14 | IDC sign-off sheet (PKG-14 signed) | Guidance.md §Interface Considerations (PKG-14) |
| IF-06 | Other interfaces | 5 | IDC review as identified | IDC sign-off sheet | — |
| QA-01 | Compliance matrix | 2, 4, 6 | Matrix completeness review (all ER clauses mapped); technical review; final verification | Compliance matrix; review sign-off | Guidance.md §Principles (traceability) |
| QA-02 | Document metadata complete | 6 | Document check (all metadata fields populated per Datasheet.md §Attributes) | Specification with complete metadata | Guidance.md §Principles (completeness) |
| QA-03 | Technical review | 4 | Technical reviewer sign-off | Technical review sign-off; comment resolution record | Guidance.md §Principles (all principles verified in technical review) |
| QA-04 | IDC review | 5 | IDC sign-off sheet (all interface disciplines) | IDC sign-off sheet | Guidance.md §Principles (coordination principle) |
| QA-05 | Discipline lead approval | 6 | Approval sign-off | Approval sign-off (this step) | Guidance.md §Principles (completeness verified by approval) |
| QA-06 | Additional quality requirements | 2, 3, 4, 6 | ER clause review; technical review; compliance verification | Compliance matrix; review sign-off | — |

**Output:** Issued Technical Specification with compliance matrix; all sign-offs obtained (author, reviewer, approver); transmittal record; document register updated.

**Verification:**
- Discipline lead approval sign-off (Specification.md QA-05) confirming specification approved for issue
- Document controller confirmation of issue (transmittal acknowledgment, distribution confirmation)
- Updated document register (confirms specification registered in project document management system)

---

## Records

**Documentation Outputs (Deliverable Artifacts — the specification produced by this procedure):**

| Record | Description | Filing Location | Specification Link | Datasheet Link | Guidance Link |
|--------|-------------|-----------------|--------------------|--------------------|---------------|
| **Technical Specification Document** | Complete technical specification (Sections 1–10) defining performance, material, workmanship requirements for all PKG-10 scope elements | `3_Issued/` (issued specification); `1_Working/` (working drafts and revisions) | Specification.md §Documentation (specification document listed); all requirements implemented in specification | Datasheet.md §Construction (3 specification sections: Unloading Arm, Containment System, Header Pipe) | Guidance.md §Examples (typical specification structure) |
| **Compliance Matrix** (Appendix A or separate document) | Traceability matrix mapping Employer's Requirements clauses to specification sections (ER clause, requirement summary, specification section, compliance status, notes) | `3_Issued/` (issued with specification or as separate document); `1_Working/` (preliminary and updated versions during development) | Specification.md QA-01 (compliance matrix requirement); §Documentation (compliance matrix listed) | Datasheet.md §Attributes (compliance matrix required) | Guidance.md §Principles (traceability principle — matrix demonstrates ER compliance) |

**Production Records (Supporting Documentation — records of specification development process):**

| Record | Description | Filing Location | Purpose | Specification Link |
|--------|-------------|-----------------|---------|-------------------|
| Approved specification outline | Specification structure outline with discipline lead sign-off (from Step 1) | `1_Working/` | Step 1 output; documents specification structure approval; basis for content development | Specification.md FN-04 (anticipated artifacts basis) |
| Preliminary compliance matrix | ER clause to specification section mapping developed in Step 2 (preliminary version before content drafting) | `1_Working/` | Step 2 output; ER clause identification record; updated during Step 3 and finalized in Step 6 | Specification.md QA-01 (compliance matrix development) |
| Technical review sign-off and comments | Technical reviewer sign-off and review comment list/report (from Step 4) | `1_Working/` | Step 4 output; demonstrates independent technical review performed per QA-03; documents review findings and comment resolution | Specification.md QA-03 (technical review requirement) |
| Review comment resolution record | Comment response log (comment number, disposition, explanation) from Step 4 comment resolution | `1_Working/` | Step 4 output; documents how review comments addressed; demonstrates issue resolution | Specification.md QA-03 (review process) |
| IDC sign-off sheet | Interface coordination record with signatures from all interface disciplines (PKG-05, PKG-07, PKG-14, PKG-17, PKG-20, others) from Step 5 | `1_Working/` | Step 5 output; demonstrates interface coordination per QA-04; verifies interface requirements coordinated with all affected disciplines | Specification.md QA-04 (IDC requirement); IF-01 through IF-06 (all interface requirements) |
| Discipline lead approval sign-off | Approval sign-off from Step 6 (signature on specification approval page or separate approval sheet) | `1_Working/` or on issued specification | Step 6 output; demonstrates specification approved for issue per QA-05; confirms technical adequacy, ER compliance, IDC coordination, appropriateness for use | Specification.md QA-05 (approval requirement) |
| Transmittal record | Issue transmittal form/letter with distribution record and acknowledgments from Step 6 | `1_Working/` or per document control procedures | Step 6 output; documents specification issue (what issued, when, to whom, for what purpose); distribution confirmation | Specification.md §Documentation (transmittal requirement) |

**Record Management:**

| Location | Purpose | Contents | Access |
|----------|---------|----------|--------|
| `1_Working/` | Active working location for deliverable; all production records and working drafts | All production records listed above; working drafts of specification (multiple iterations during development); preliminary compliance matrix; review records; IDC records; approval records; transmittal record; correspondence related to deliverable | Discipline team access (specification author, technical reviewer, discipline lead, IDC coordinator) |
| `2_Checking/To/` | Review packages during formal Employer review cycles (if required per project convention) | Review copies of specification submitted for Employer review at stage gates (30%, 60%, 90%); Employer review comments; review responses | Review team access (Employer, contractor review team, discipline leads) |
| `3_Issued/` | Issued specification (final approved version) | Final issued Technical Specification with compliance matrix (PDF or Word per project requirements **TBD**); organized by revision (subdirectories for Rev 0, Rev 1, etc., or Rev A, Rev B, etc.); transmittal record with issued specification | Project-wide access (all disciplines, procurement team, construction contractors, vendors, Employer, QA/QC team) |

**Retention Requirements:**
- **TBD** — per project document control procedure and regulatory requirements
- **ASSUMPTION:** Electronic records maintained in project document management system with backup and archival per IT procedures (daily backup, offsite archival, disaster recovery)
- **ASSUMPTION:** Minimum retention period aligned with project design life (25–30 years typical per Datasheet.md §Conditions design life **TBD**) and regulatory requirements (building code, environmental regulations, food safety regulations may require specific retention periods)
- **ASSUMPTION:** Issued specifications retained permanently for project record; working records retained for duration of design and construction phase minimum (may be archived after project completion per document retention policy)

**Traceability:**
- All records linked to deliverable ID (DEL-10.02) per Datasheet.md §Identification
- Specification document number traceable to approved outline (Step 1) and project document numbering system
- Revisions traceable through revision history in specification document and document register (each revision documented with number, date, description, author)
- ER requirements traceable through compliance matrix (each ER clause mapped to specification section; bidirectional traceability ER ↔ specification)
- Interfaces traceable through IDC sign-off sheet linking to other package deliverables (PKG-05, PKG-07, PKG-14, PKG-17, PKG-20)
- Requirements traceable through verification matrix (each requirement linked to verification step, method, record)

**Pass 3 Final Verification:** All procedure steps aligned with Specification requirements, Guidance principles, and Datasheet attributes; all cross-references bidirectional and verified; all TBDs and ASSUMPTIONs properly marked and sourced; terminology consistent across all four documents (Datasheet, Specification, Guidance, Procedure); verification matrix complete and comprehensive; compliance matrix development process fully described.
