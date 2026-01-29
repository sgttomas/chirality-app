# Specification: DEL-10.01 Railcar Unloading Design Drawing Set

## Scope

This specification defines the requirements for the **Railcar Unloading Design Drawing Set** within **PKG-10 Railcar Unloading System**.

**Purpose:** Defines the design arrangement and details for railcar unloading per ER requirements, supporting the facility's 1,000,000 MT/annum throughput capacity with 32 railcar unloading stations capable of simultaneous operations. (**Source:** decomposition §5 PKG-10; Datasheet.md §Conditions; Guidance.md §Purpose)

**PKG-10 Scope Elements to be Depicted:**

| Element | Description | Quantity | Drawing Type | Datasheet Link | Guidance Link |
|---------|-------------|----------|--------------|----------------|---------------|
| Unloading arms | Railcar connection assemblies (bottom-loading type **ASSUMPTION**) | 32 | Arm arrangement | Datasheet.md §Construction | Guidance.md §Trade-offs (arm type selection) |
| Quick-connects | Coupler assemblies for railcar connection | 32 | Arm arrangement details | Datasheet.md §Construction | Guidance.md §Principles |
| Gravity flow header | Collection header from unloading stations to storage (single system with branch connections) | 1 system | Header pipe layout | Datasheet.md §Construction | Guidance.md §Principles (gravity flow design) |
| Spill containment pans | Under-track containment for each station (32 individual **PROPOSAL** or combined system **TBD**) | 32 or combined | Containment details | Datasheet.md §Construction | Guidance.md §Trade-offs (containment approach) |
| Collection system | Sumps, drains, sump pumps for spill recovery | Per containment design | Containment details | Datasheet.md §Construction | Guidance.md §Considerations |
| Atmospheric venting | Vent connections and routing from railcars | 32 connections | GA and arrangements | Datasheet.md §Construction | Guidance.md §Principles |
| Flow indicators | Local flow indication devices at each station | 32 | GA and arrangements | Datasheet.md §Construction | Guidance.md §Principles |

(**Source:** Decomposition §5 PKG-10 scope description; Datasheet.md §Conditions)

**Anticipated Drawing Set (per Datasheet.md §Construction):**

1. **Unloading System GA** — overall facility layout (32 stations, header routing, containment, equipment locations)
2. **Unloading Arm Arrangement** — 32-station arm positions and details (may require multiple sheets for clarity)
3. **Header Pipe Layout** — gravity flow header routing, sizing, slopes, connections
4. **Containment Details** — spill containment and collection system

**Inclusions:**
- All PKG-10 scope elements as identified in decomposition (FN-01)
- Interface points with adjacent disciplines: PKG-05 (structural), PKG-07 (rail), PKG-14 (piping), PKG-17 (electrical), PKG-20 (instrumentation) per IF-01 through IF-06
- Equipment arrangement, clearances, and access provisions per Guidance.md §Principles
- Containment system layout per environmental protection objective (OBJ-7)
- Piping header routing and slopes (gravity flow design per Guidance.md §Principles)
- Drawing metadata per Datasheet.md §Attributes and QA-02

**Exclusions:**
- Detailed fabrication drawings for vendor-supplied equipment (covered by DEL-10.04 Data Sheets and vendor documentation)
- Piping downstream of header discharge connection to storage tanks (covered by PKG-14 Process Piping — interface at IF-05)
- Electrical schematics and wiring diagrams (covered by PKG-17 Electrical — interface at IF-03)
- Instrumentation loop diagrams and control schematics (covered by PKG-20 Field Instrumentation / PKG-21 Control Systems — interface at IF-04)
- Rail track design and construction (covered by PKG-07 Rail Works — interface at IF-01)
- Structural design of foundations and supports (covered by PKG-05 Concrete Structures / PKG-06 Structural Steelwork — interface at IF-02)

## Requirements

### Functional Requirements

| Req ID | Requirement | Source | Verification | Datasheet Link | Procedure Link | Guidance Link |
|--------|-------------|--------|--------------|----------------|----------------|---------------|
| FN-01 | The Drawing Set shall depict all PKG-10 scope elements identified in the decomposition: (1) unloading arms, (2) quick-connects, (3) gravity flow header, (4) spill containment pans, (5) collection system, (6) atmospheric venting, (7) flow indicators | Decomposition §5 PKG-10; Datasheet.md §Conditions | Design review; document check | Datasheet.md §Conditions (all 7 elements listed) | Procedure.md Steps 2, 3, 5 | Guidance.md §Principles (all elements addressed) |
| FN-02 | The Drawing Set shall include the anticipated artifacts: unloading system GA, unloading arm arrangement, header pipe layout, containment details | Decomposition §5 DEL-10.01; Datasheet.md §Construction | Document check against approved drawing list | Datasheet.md §Construction (4 drawing types listed) | Procedure.md Step 1 (drawing list), Step 3 (completeness check) | Guidance.md §Examples (4 drawing types described) |
| FN-03 | Drawings shall show 32 unloading arm positions corresponding to railcar unloading stations with clearances, reach envelopes, and railcar coupling interface | Decomposition §1 (32 stations); README; Datasheet.md §Conditions | Design review; dimensional check | Datasheet.md §Conditions (32 arms quantity) | Procedure.md Step 2 (arm arrangement production), Step 3 (dimensional check) | Guidance.md §Considerations (32-station layout factors) |
| FN-04 | Drawings shall show gravity flow header routing with pipe sizes (per DEL-10.03), slopes (minimum 1:100 for drainage), connection points, branch connections from each of 32 stations, isolation valves, and air release provisions at high points | Decomposition §5 PKG-10; Guidance.md §Principles (gravity flow design) | Design review; calculation check (DEL-10.03) | Datasheet.md §Construction (Header Pipe Layout content) | Procedure.md Step 2 (header layout production) | Guidance.md §Principles (gravity flow principle), §Considerations (header design factors) |
| FN-05 | Drawings shall show spill containment arrangement (pans, sumps) and collection system (drains, sump pumps) with containment volume verification (reference to DEL-10.03 calculations) | Decomposition §5 PKG-10; Guidance.md §Principles (spill containment); OBJ-7 (environmental protection) | Design review; calculation check (DEL-10.03 containment volume) | Datasheet.md §Construction (Containment Details content) | Procedure.md Step 2 (containment details production) | Guidance.md §Principles (spill containment principle), §Trade-offs (containment approach) |
| FN-06 | **TBD** — Additional functional requirements per Employer's Requirements (e.g., accessibility provisions, maintenance access, safety features, emergency provisions) | ER Vol 2 clauses **TBD** | **TBD** — design review per ER requirements | — | — | — |

### Performance Requirements

| Req ID | Requirement | Source | Verification | Guidance Link | Procedure Link | Datasheet Link |
|--------|-------------|--------|--------------|---------------|----------------|----------------|
| PF-01 | Drawings shall support design for 1,000,000 MT/annum throughput capacity utilizing 32 unloading stations (simultaneous operations capability **TBD**) | Decomposition §1, §2 OBJ-2; Datasheet.md §Conditions | Design review; throughput analysis (DEL-10.03) | Guidance.md §Principles (OBJ-2 objective alignment), §Considerations (simultaneous operations) | Procedure.md Step 2 (design development per throughput requirement) | Datasheet.md §Conditions (throughput capacity parameter) |
| PF-02 | **TBD** — Unloading rate requirements per station (e.g., flow rate per arm, unloading time per railcar) per Employer's Requirements | ER Vol 2 clauses **TBD** | Calculation verification (DEL-10.03 — flow analysis) | Guidance.md §Considerations (design factors) | Procedure.md Step 2 (design per performance requirements) | — |
| PF-03 | **TBD** — Containment volume requirements per ER / regulatory requirements (e.g., largest credible spill scenario — typically one railcar capacity or header section volume) | ER Vol 2 clauses **TBD**; regulatory codes **TBD** (e.g., Environment Canada SPCC) | Calculation verification (DEL-10.03 — containment volume) | Guidance.md §Principles (OBJ-7), §Considerations (containment volume), §Examples (regulatory guidance) | Procedure.md Step 2 (containment details per calculations) | Datasheet.md §Construction (Containment Details) |
| PF-04 | **TBD** — Header sizing and hydraulic performance (sufficient capacity for simultaneous unloading operations; gravity flow with adequate slopes; minimize pressure drop) | DEL-10.03 (header sizing calculations); ER Vol 2 clauses **TBD** | Calculation verification (DEL-10.03 — hydraulic analysis) | Guidance.md §Principles (gravity flow design), §Considerations (header design factors) | Procedure.md Step 2 (header layout per calculations) | Datasheet.md §Construction (Header Pipe Layout) |

### Interface Requirements

| Req ID | Requirement | Source | Verification | Datasheet Link | Procedure Link | Guidance Link |
|--------|-------------|--------|--------------|----------------|----------------|---------------|
| IF-01 | Drawings shall show interface with rail track alignment and railcar positions (PKG-07 Rail Works) including station spacing (14–18m centers typical), clearances to track, track curvature effects, and railcar positioning tolerance | Decomposition; Datasheet.md §Construction (interfaces); Guidance.md §Considerations (32-station layout) | IDC review with PKG-07 | Datasheet.md §Construction (interface table) | Procedure.md Step 4 (IDC with PKG-07) | Guidance.md §Considerations (railcar interface factors), §Interface Considerations (PKG-07 coordination needs) |
| IF-02 | Drawings shall show structural support interfaces (PKG-05 Concrete Structures / PKG-06 Structural Steelwork) including foundation locations and elevations for unloading arms, pipe support points and loads, containment structure supports, and seismic design coordination | Decomposition; Datasheet.md §Construction (interfaces); Guidance.md §Considerations (site conditions — seismic) | IDC review with PKG-05/PKG-06 | Datasheet.md §Construction (interface table) | Procedure.md Step 4 (IDC with PKG-05/PKG-06) | Guidance.md §Interface Considerations (structural coordination needs) |
| IF-03 | Drawings shall show electrical interface points for sump pumps, area lighting, and other electrical loads (PKG-17 Electrical) including power supply locations, cable routing, and hazardous area classification boundaries | Decomposition; Datasheet.md §Construction (interfaces); Datasheet.md §Conditions (HAC **TBD**) | IDC review with PKG-17 | Datasheet.md §Construction (interface table), §Conditions (HAC parameter) | Procedure.md Step 4 (IDC with PKG-17); Step 2 (show classification zones on GA) | Guidance.md §Interface Considerations (electrical coordination needs) |
| IF-04 | Drawings shall show instrumentation interface points for flow indicators (32 locations), level switches (sump locations), and temperature elements (**if required for winterization**) (PKG-20 Field Instrumentation) | Decomposition; Datasheet.md §Construction (interfaces) | IDC review with PKG-20 | Datasheet.md §Construction (interface table) | Procedure.md Step 4 (IDC with PKG-20) | Guidance.md §Interface Considerations (instrumentation coordination needs) |
| IF-05 | Drawings shall show process piping connection to downstream header and storage system (PKG-14 Process Piping) including connection size, location, elevation, and isolation valve coordination | Decomposition; Datasheet.md §Construction (interfaces) | IDC review with PKG-14 | Datasheet.md §Construction (interface table) | Procedure.md Step 4 (IDC with PKG-14) | Guidance.md §Interface Considerations (piping coordination needs) |
| IF-06 | **TBD** — Additional interface requirements per Employer's Requirements (e.g., fire protection systems, utilities, site access routes, security systems) | ER Vol 2 clauses **TBD** | IDC review with applicable disciplines | — | Procedure.md Step 4 (IDC as identified) | — |

**Note:** Dependencies coordinated externally (see `_DEPENDENCIES.md` — NOT_TRACKED). Interface coordination performed through IDC process per Procedure.md Step 4 with sign-off from all affected disciplines (QA-04).

### Quality Requirements

| Req ID | Requirement | Source | Verification | Datasheet Link | Procedure Link | Guidance Link |
|--------|-------------|--------|--------------|----------------|----------------|---------------|
| QA-01 | Drawings shall be produced to project CAD standard including sheet size, scale, line weights, text styles, layering, symbology, and title block format | **TBD** — ER/contractor CAD standard; Datasheet.md §Attributes | CAD compliance check (independent check) | Datasheet.md §Attributes (CAD standard, sheet size, scale) | Procedure.md Steps 2 (CAD standard application), 5 (CAD compliance check) | Guidance.md §Principles (drawing development — clarity principle) |
| QA-02 | Drawing metadata shall include fields per Datasheet.md §Attributes: drawing number, drawing title, sheet size, scale, revision, date, originator, checker, approver, classification | Datasheet.md §Attributes; cross-document consistency | Document check (self-check and independent check) | Datasheet.md §Attributes (all metadata fields listed) | Procedure.md Steps 2 (metadata population), 3 (metadata check), 6 (finalize metadata) | Guidance.md §Documentation Considerations (drawing metadata) |
| QA-03 | Drawings shall be subject to independent check by qualified checker (separate from originator) prior to issue, covering technical adequacy, code compliance, dimensional accuracy, and cross-references | **ASSUMPTION** — typical D&B quality procedure | Checker sign-off; comment resolution record | — | Procedure.md Step 5 (independent check process) | Guidance.md §Principles (drawing development — completeness, consistency) |
| QA-04 | Drawings shall be subject to IDC review where interfaces exist (IF-01 through IF-06) with sign-offs from all affected disciplines | **ASSUMPTION** — typical D&B coordination procedure; Datasheet.md §Construction (interfaces) | IDC sign-off sheet (all interface disciplines) | Datasheet.md §Construction (interface table) | Procedure.md Step 4 (IDC process) | Guidance.md §Principles (drawing development — coordination principle) |
| QA-05 | Drawings shall be subject to discipline lead approval prior to issue, confirming technical adequacy, ER compliance, and completeness | **ASSUMPTION** — typical D&B approval procedure | Approval sign-off | — | Procedure.md Step 5 (approval process) | Guidance.md §Principles (drawing development — completeness) |
| QA-06 | **TBD** — Additional quality requirements per Employer's Requirements (e.g., third-party review, regulatory approvals, certification requirements) | ER Vol 2 clauses **TBD** | **TBD** | — | **TBD** | — |

## Standards

**Applicable Standards (to be confirmed per Employer's Requirements):**

| Standard | Application | Source | Datasheet Link | Procedure Link |
|----------|-------------|--------|----------------|----------------|
| **TBD** — Project CAD Standard | Drawing production, formatting, symbology, title block, layers, line weights | ER Vol 2 **TBD** / contractor CAD procedures | Datasheet.md §Attributes (CAD standard) | Procedure.md Step 2 (CAD standard application), Step 5 (CAD compliance check) |
| **TBD** — CSA B51 | Pressure equipment design (if applicable to unloading arms or header system) | ER Vol 2 **TBD** | Datasheet.md §Conditions (design standards) | Procedure.md §Prerequisites (applicable standards) |
| **TBD** — ASME B31.3 | Process piping design (gravity flow header and connections) | ER Vol 2 **TBD**; DEL-10.03 (piping calculations) | Datasheet.md §Construction (Header Pipe Layout); Datasheet.md §Conditions (design standards) | Procedure.md §Prerequisites (applicable standards); Guidance.md §Examples (header design references) |
| **TBD** — BC Building Code | Structural and site requirements (seismic design, foundations, site conditions) | Regulatory; ER Vol 2 **TBD** | Datasheet.md §Conditions (seismic requirements parameter) | Procedure.md §Prerequisites (applicable standards); Procedure.md Step 4 (IDC with PKG-05 structural) |
| **TBD** — Environmental regulations | Containment requirements, spill prevention and control (SPCC) | Regulatory (Environment Canada, BC regulations); ER Vol 2 **TBD** | Datasheet.md §Conditions (environmental classification); Datasheet.md §Construction (Containment Details) | Procedure.md §Prerequisites (applicable standards); Guidance.md §Examples (containment design — regulatory guidance) |
| **TBD** — Hazardous area classification standard | Area classification for electrical/instrumentation (Class/Div or Zone system) | ER Vol 2 **TBD**; HAC study deliverable | Datasheet.md §Conditions (HAC parameter) | Procedure.md Step 2 (show classification zones on GA); Procedure.md Step 4 (IDC with PKG-17 electrical) |

**Baseline Source Documents:**

| Document | Location | Relevance | Datasheet Link |
|----------|----------|-----------|----------------|
| Canola Oil Transload Facility Decomposition | `test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md` | PKG-10 scope; DEL-10.01 definition; objectives (OBJ-1, OBJ-2, OBJ-4, OBJ-7) | Datasheet.md §References |
| Employer's Requirements Vol 2 Pt 1 | `test/Volume_2_Part_1_Employers_Requirements.pdf` | Project requirements (clauses **TBD** — to be reviewed during design development per Procedure.md Step 2) | Datasheet.md §References |
| Employer's Requirements Vol 2 Pt 2 | `test/Volume_2_Part_2_Employers_Requirements.pdf` | Technical specifications (clauses **TBD** — to be reviewed during design development) | Datasheet.md §References |
| Employer's Requirements Vol 2 Pt 3 | `test/Volume_2_Part_3_Employers_Requirements.pdf` | Quality and documentation requirements (clauses **TBD** — CAD standard, document control) | Datasheet.md §References |

## Verification

**Verification Matrix:**

| Req Category | Requirements | Verification Method | Responsible | Procedure Link | Record | Guidance Link |
|--------------|--------------|---------------------|-------------|----------------|--------|---------------|
| Functional (FN-xx) | FN-01 through FN-06 | Design review against decomposition scope and ER; document check for completeness | Discipline lead / design engineer / checker | Procedure.md Steps 2 (design development), 3 (self-check), 5 (independent check) | Review record; checker sign-off; drawings | Guidance.md §Principles (design principles address functional requirements) |
| Performance (PF-xx) | PF-01 through PF-04 | Design review; calculation verification (DEL-10.03 — throughput analysis, header sizing, containment volume) | Discipline lead / design engineer / checker | Procedure.md Steps 2 (design per calculations), 3 (check calculations), 5 (independent check); DEL-10.03 verification | Calculation package (DEL-10.03); review record; checker sign-off | Guidance.md §Considerations (design factors address performance requirements) |
| Interface (IF-xx) | IF-01 through IF-06 | IDC review with adjacent disciplines (PKG-05, PKG-07, PKG-14, PKG-17, PKG-20, others) | IDC coordinator / multi-discipline team | Procedure.md Step 4 (IDC process) | IDC sign-off sheet (all interface disciplines signed) | Guidance.md §Interface Considerations (coordination needs for all interfaces) |
| Quality (QA-xx) | QA-01 through QA-06 | Document check; CAD compliance check; independent check; IDC review; approval | Checker / discipline lead / document control | Procedure.md Steps 3 (self-check), 4 (IDC), 5 (independent check and approval), 6 (issue checks) | Self-check record; checker sign-off; approval sign-off; transmittal | Guidance.md §Principles (drawing development principles support quality requirements) |

**Acceptance Criteria:**

1. All functional requirements (FN-01 through FN-06) addressed on issued drawings with clear depiction of all 7 PKG-10 scope elements
2. All performance requirements (PF-01 through PF-04) verified by design review and supporting calculations (DEL-10.03 — header sizing, throughput analysis, containment volume)
3. All interface requirements (IF-01 through IF-06) coordinated through IDC and signed off by all affected disciplines (PKG-05, PKG-07, PKG-14, PKG-17, PKG-20, others as identified)
4. All quality requirements (QA-01 through QA-06) verified through checks and approvals
5. Drawing metadata complete per Datasheet.md §Attributes (drawing number, revision, dates, sign-offs)
6. Independent checker sign-off obtained (QA-03)
7. Discipline lead approval sign-off obtained (QA-05)
8. **TBD** — Additional acceptance criteria per Employer's Requirements

**Non-Conformance Handling:**
- Drawing errors or omissions identified during checking (Step 5) to be corrected before approval
- Interface conflicts identified during IDC (Step 4) to be resolved through multi-discipline coordination; escalate to project management if resolution cannot be achieved at IDC level
- **TBD** — Non-conformance procedure per project quality plan

## Documentation

**Required Documentation Outputs (per Datasheet.md §Construction):**

| Document | Description | Drawing Type | Datasheet Link | Procedure Step | Guidance Link |
|----------|-------------|--------------|----------------|----------------|---------------|
| Unloading System GA | Overall facility layout showing 32 stations, header routing, containment areas, equipment locations | General arrangement | Datasheet.md §Construction (GA content description) | Procedure.md Step 2 (GA production) | Guidance.md §Examples (GA typical content and scale) |
| Unloading Arm Arrangement | 32-station arm positions, clearances, quick-connect details, reach envelopes (may require multiple sheets) | Arrangement drawings | Datasheet.md §Construction (Arm Arrangement content description) | Procedure.md Step 2 (arrangement production) | Guidance.md §Examples (Arm Arrangement typical content and scale) |
| Header Pipe Layout | Gravity flow header routing, pipe sizes, slopes (minimum 1:100), connections, isolation valves | Piping layout | Datasheet.md §Construction (Header Layout content description) | Procedure.md Step 2 (header layout production) | Guidance.md §Examples (Header Layout typical content and scale) |
| Containment Details | Spill containment pans (32 individual or combined), collection sumps, drain routing, sump pump locations | Detail drawings | Datasheet.md §Construction (Containment Details content description) | Procedure.md Step 2 (containment details production) | Guidance.md §Examples (Containment Details typical content and scale) |

**Document Control Requirements:**

| Requirement | Detail | Source | Procedure Link | Datasheet Link |
|-------------|--------|--------|----------------|----------------|
| Drawing numbering | Per project document numbering procedure (**TBD**); number assignment in Procedure.md Step 1 | ER/contractor document control procedures | Procedure.md Steps 1 (number assignment), 6 (finalize numbers) | Datasheet.md §Attributes (drawing number series **TBD**) |
| Revision control | Per project document control procedure (**TBD**); revision numbering system, revision clouds, revision history in title block | ER/contractor document control procedures | Procedure.md Step 6 (revision management) | Datasheet.md §Attributes (revision control **TBD**) |
| Title block format | Per project CAD standard (**TBD**); include all metadata per Datasheet.md §Attributes | CAD standard | Procedure.md Steps 2 (title block population), 5 (title block check), 6 (finalize title block) | Datasheet.md §Attributes (all metadata fields listed) |
| Transmittal | Per project document control procedure (**TBD**); transmittal form/letter with distribution record required | ER/contractor document control procedures | Procedure.md Step 6 (transmittal process) | — |
| Filing locations | Working: `1_Working/`; Review: `2_Checking/To/`; Issued: `3_Issued/` per framework convention | Framework convention | Procedure.md §Records (filing locations) | — |
| Electronic format | **TBD** — PDF, native CAD, or both per project requirements | ER/contractor document control procedures | Procedure.md Step 6 (convert to issue format) | — |
| Retention | **TBD** — per project document control procedure and regulatory requirements (minimum aligned with project design life) | ER/contractor document control procedures; regulatory requirements | Procedure.md §Records (retention requirements) | Datasheet.md §Conditions (design life parameter **TBD**) |

**Traceability to Other Deliverables:**

| Related Deliverable | Relationship | Interface | Procedure Link |
|---------------------|--------------|-----------|----------------|
| DEL-10.02 (Technical Specification) | Technical requirements for equipment and system performance drive drawing content | Drawings implement specification requirements | Procedure.md §Prerequisites (design basis); Step 2 (design development) |
| DEL-10.03 (Design Calculations) | Header sizing, hydraulic analysis, containment volume calculations provide basis for drawing content | Drawings reflect calculated sizes and capacities | Procedure.md §Prerequisites (equipment sizing); Step 2 (verify calculations) |
| DEL-10.04 (Data Sheet Package) | Equipment data sheets for 32 unloading arms and associated equipment provide dimensions and specifications | Drawings show equipment per data sheet specifications | Procedure.md §Prerequisites (equipment data sheets); Step 2 (arm arrangement per data sheets) |
| DEL-10.05 (Installation and Test Records) | Installation procedures and acceptance testing reference drawings for as-installed configuration | Drawings provide basis for installation and testing | (Downstream deliverable — not a prerequisite for this deliverable) |
| PKG-14 (Process Piping) | Downstream piping from header discharge to storage tanks interfaces at header connection | Interface at header discharge connection (IF-05) | Procedure.md Step 4 (IDC with PKG-14) |
| PKG-07 (Rail Works) | Rail track alignment and railcar positions interface with station layout | Interface at station locations relative to track (IF-01) | Procedure.md Step 4 (IDC with PKG-07) |
| PKG-05 (Concrete Structures) | Foundations and structural supports interface with equipment and piping | Interface at support locations (IF-02) | Procedure.md Step 4 (IDC with PKG-05) |

**Pass 3 Verification:** All requirements traceable to Datasheet, Guidance, and Procedure; all cross-references bidirectional; all TBDs and ASSUMPTIONs properly marked; terminology consistent across all documents.
