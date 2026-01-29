# Procedure: DEL-12.02 Metering Technical Specification

## Purpose

This procedure defines the process for producing and managing the **Metering Technical Specification** within **PKG-12 Product Transfer & Metering**.

### Deliverable Definition

DEL-12.02 defines performance, materials, and workmanship requirements for custody transfer metering per Employer's Requirements (Source: Decomposition:357).

| Attribute | Value |
|-----------|-------|
| Deliverable Type | Specification |
| Discipline | Process |
| Responsible Party | D&B Contractor |
| Service Application | Custody transfer metering for CSD canola oil at rail unloading and marine loading |

### Procedure Scope

This procedure covers the complete lifecycle for producing the metering technical specification:

1. **Authoring** — gathering basis, defining scope, drafting requirements, adding verification hooks
2. **Review and checking** — discipline check, interdisciplinary check (IDC)
3. **Issue and revision management** — document control, approvals, issuance

This procedure applies to both specification artifacts: (1) Custody Transfer Flow Meter Specification, (2) Metering System Specification.

## Prerequisites

### Dependencies

| Prerequisite | Status | Notes |
|--------------|--------|-------|
| Dependency Mode | NOT_TRACKED | Dependencies coordinated externally by humans (see `_DEPENDENCIES.md` and `execution/_Coordination/_COORDINATION.md`); interfaces with PKG-14, PKG-17, PKG-19, PKG-20 managed through coordination meetings and IDC process |

### Recommended Upstream Inputs

The following inputs should be obtained before commencing specification authoring (ASSUMPTION based on typical specification development workflow):

| Input | Source | Purpose | Timing |
|-------|--------|---------|--------|
| Employer's Requirements | ER Vol 2 Part 2 | Metering requirements, accuracy criteria, flow rates, operating conditions, fluid properties, hazardous area classification, proving requirements, regulatory compliance | Before Step 1 (Gather Basis) |
| Applicable Metering Standards | TBD | Custody transfer measurement standards (API MPMS, OIML R117, Measurement Canada); standard clauses govern accuracy, proving, installation, testing | During Step 1 (Gather Basis) |
| Process Design Basis | PKG-14, Design Basis | Flow rates for rail unloading and marine loading, operating pressure and temperature, product properties (CSD canola oil density, viscosity, pour point, flash point) | Before Step 3 (Draft Requirements) |
| Interface Definitions | PKG-17, PKG-19, PKG-20 | Electrical interface (power supply, area classification), controls interface (signal types, communication protocols, HMI), instrumentation interface (transmitter types, signal protocols) | During Step 3 (Draft Requirements); may be iterative |
| Project Quality Plan | Project Quality | QA requirements, inspection and test procedures, hold points, witness points, nonconformance handling, material traceability | During Step 3 (Draft Requirements for QA section) |

### Reference Materials

| Reference | Location | Purpose |
|-----------|----------|---------|
| `_REFERENCES.md` | Deliverable folder | Applicable reference documents; list of ER clauses, standards, project documents |
| `0_References/` | Package directory | Reference materials for PKG-12 (ER excerpts, standards, vendor literature) |
| Employer's Requirements Vol 2 Part 1 | ER document set | General requirements, document control procedures, quality procedures, design life, seismic requirements, environmental conditions | TBD |
| Employer's Requirements Vol 2 Part 2 | ER document set | Process mechanical requirements, metering technical requirements, accuracy criteria, flow rates, fluid properties (CSD canola oil), operating conditions, hazardous area classification, regulatory compliance | TBD |
| Decomposition | Project root | PKG-12 scope (line 350), DEL-12.02 definition (line 357), objective mappings (lines 781, 789) |
| Specification.md | Deliverable folder | Requirements to be satisfied (REQ-01 through REQ-24); defines what specification must contain |
| Guidance.md | Deliverable folder | Development considerations, principles, trade-offs, technology selection factors, service-specific considerations |
| Datasheet.md | Deliverable folder | Design context, anticipated specification content, key topics |

### Personnel Requirements

| Role | Qualification | Responsibility | Source |
|------|---------------|----------------|--------|
| Originator | Qualified Process discipline engineer with custody transfer metering experience; familiarity with applicable metering standards (API MPMS, OIML R117) and Measurement Canada requirements | Technical content, specification authoring, requirements traceability, coordination with vendors and interfaces | ASSUMPTION; project quality procedures |
| Checker | Independent Process discipline engineer (not the originator); metering expertise | Discipline check for technical correctness, completeness, testability, traceability | ASSUMPTION; project quality procedures |
| IDC Participants | Representatives from interfacing disciplines: Piping (PKG-14), Electrical (PKG-17), Instrumentation (PKG-20), Controls (PKG-19) | Interface review and coordination; verify interface definitions are complete and achievable | ASSUMPTION |
| Approver | Authorized per project procedures (typically Process Lead or Engineering Manager) | Authorization for issue; confirm specification satisfies ER requirements and project objectives | TBD; ER Vol 2 Part 1 |

### Tools and Systems

| Tool/System | Purpose | Source |
|-------------|---------|--------|
| Word Processing Software | Specification authoring (MS Word, Google Docs, or per project standards) | TBD; ER Vol 2 Part 1 |
| Document Management System | Specification storage, revision control, distribution | TBD; ER Vol 2 Part 1 |
| Requirements Management Tool (optional) | Requirements traceability matrix management | TBD; may use spreadsheet if dedicated tool not available |

## Steps

### Step 1: Gather Basis

**Objective:** Collect all basis information and reference materials necessary for specification authoring.

| Action | Description | Output |
|--------|-------------|--------|
| 1.1 | Collect Employer's Requirements clauses related to metering from ER Vol 2 Part 2 (TBD); extract requirements for: accuracy class, flow rates, operating conditions, proving requirements, regulatory compliance (Measurement Canada), documentation submittals | ER clause excerpts; requirement notes |
| 1.2 | Identify applicable custody transfer metering standards: (a) API MPMS if applicable to vegetable oil (TBD; commonly referenced even for non-petroleum liquids), (b) OIML R117 for dynamic measuring systems for liquids other than water (likely primary standard), (c) Measurement Canada regulations for custody transfer in Canada (TBD); obtain standard copies or access | Standard identification list; standard copies |
| 1.3 | Obtain process design basis from PKG-14 or design basis document: flow rates (rail unloading design/normal/min/max; marine loading design/normal/min/max), operating pressure and temperature ranges, product properties (CSD canola oil density vs. temperature, viscosity vs. temperature, pour point, flash point, vapor pressure) | Design basis summary; product property data |
| 1.4 | Review project objectives for specification alignment: OBJ-2 (1,000,000 MT/a throughput) — ensure metering does not constrain flow capacity; OBJ-10 (Custody Transfer Accuracy) — define accuracy and proving requirements | Objective alignment notes |
| 1.5 | Review Guidance.md for design considerations: technology selection factors (Coriolis, ultrasonic, turbine, positive displacement), proving method options (in-line prover, portable prover, master meter), service-specific considerations (rail vs. marine), product-specific considerations (canola oil properties) | Design considerations summary |
| 1.6 | Document specification basis in specification introduction/references section: cite ER clauses, applicable standards, design basis sources | Documented specification basis |

**Output:** Complete basis package documented in specification; basis summary for originator's use

**Verification:** Basis package is complete and traceable to sources; no fabricated or assumed basis without labeling

---

### Step 2: Define Scope

**Objective:** Clearly define specification scope, system boundaries, and artifacts.

| Action | Description | Output |
|--------|-------------|--------|
| 2.1 | Confirm scope covers both rail unloading and marine loading metering services per Decomposition:350, 357 and Specification.md REQ-01 | Scope statement |
| 2.2 | Define system boundaries — what is included in metering scope vs. excluded: **Included**: custody transfer flow meters (rail and marine), metering instrumentation (temperature, pressure, density transmitters), proving system (prover, connections, isolation), integration with control system (signals, data logging), QA documentation (certificates, test records); **Excluded**: control system architecture (PKG-19), general field instrumentation requirements (PKG-20), process piping beyond meter runs (PKG-14), electrical power distribution (PKG-17) | System boundary definition |
| 2.3 | Identify the two specification artifacts per Decomposition:357 and Specification.md REQ-02: (1) Custody Transfer Flow Meter Specification — meter-specific requirements, (2) Metering System Specification — system-level requirements (instrumentation, proving, integration) | Artifact identification |
| 2.4 | Document scope in specification scope section: service description (rail unloading, marine loading), product (CSD canola oil), application (custody transfer commercial transactions), system boundaries (included/excluded) | Specification scope section draft |

**Output:** Defined specification scope documented in specification

**Verification:** Scope aligns with Decomposition:350, 357 and Specification.md REQ-01, REQ-02; system boundaries are clear

---

### Step 3: Draft Requirements

**Objective:** Draft technical requirements for custody transfer metering covering performance, materials, installation, proving, instrumentation, electrical/controls, and QA.

#### 3.1: Performance Requirements

| Action | Description |
|--------|-------------|
| 3.1.1 | Draft accuracy class requirement per Specification.md REQ-06: specify accuracy (e.g., ±0.15%, ±0.25%, or as required by ER Vol 2 Part 2; TBD); cite source (ER clause or custody transfer standard); define uncertainty budget if required by standard; **Example**: "Flow meters shall achieve accuracy of ±0.15% of reading over the specified flow range (Reference: ER Vol 2 Part 2 Clause X.X.X; TBD)" |
| 3.1.2 | Draft repeatability requirement per Specification.md REQ-08: specify repeatability (e.g., ±0.05%, ±0.1%, or as required by ER; TBD); cite source; **Example**: "Flow meters shall achieve repeatability of ±0.05% (Reference: OIML R117 accuracy class 0.5; TBD)" |
| 3.1.3 | Draft turndown ratio requirement per Specification.md REQ-07: specify minimum turndown (e.g., 10:1, 20:1, or as required; TBD); cite source; **Example**: "Flow meters shall provide turndown ratio of at least 10:1 (minimum measurable flow to maximum measurable flow)" |
| 3.1.4 | Draft flow range requirements per Specification.md REQ-09 for each service: (a) Rail unloading: minimum, normal, design, maximum flow rates (TBD from DEL-12.03), (b) Marine loading: minimum, normal, design, maximum flow rates (TBD from DEL-12.03); cite DEL-12.03 calculations; verify flow ranges support OBJ-2 (1,000,000 MT/a throughput) |
| 3.1.5 | Draft meter technology requirements per Specification.md REQ-05: specify meter technology (Coriolis, ultrasonic, turbine, positive displacement, or "technology neutral — performance-based specification allowing vendors to propose suitable technology"); if technology-specific requirements exist in ER, cite ER clause; if technology neutral, define performance criteria that any proposed technology must meet |

#### 3.2: Material Requirements

| Action | Description |
|--------|-------------|
| 3.2.1 | Draft wetted parts material requirements per Specification.md REQ-11: specify materials compatible with CSD canola oil (e.g., body material: SS316L or carbon steel; wetted components: SS316L; seals and gaskets: Viton or PTFE; TBD); cite material compatibility source (ER, vendor data, or industry practice) |
| 3.2.2 | Draft environmental rating requirements per Specification.md REQ-12: specify ratings for outdoor installation at Fraser Surrey Terminal (temperature range -20°C to +50°C example; TBD from ER Vol 2 Part 1), humidity, corrosion resistance (coastal environment), seismic requirements (TBD from ER Vol 2 Part 1) |
| 3.2.3 | Consider food-grade material requirements if applicable to CSD canola oil (TBD; ER Vol 2 Part 2 or product specifications) |

#### 3.3: Installation Requirements

| Action | Description |
|--------|-------------|
| 3.3.1 | Draft straight-run requirements per Specification.md REQ-13: specify upstream and downstream straight-run lengths (e.g., "10D upstream, 5D downstream minimum, or per manufacturer recommendations, whichever is greater"; TBD per selected meter technology); cite manufacturer requirements and applicable standards |
| 3.3.2 | Draft orientation requirements: specify meter orientation (horizontal preferred, vertical acceptable if manufacturer approved, inclined per manufacturer; TBD per meter technology); cite manufacturer requirements |
| 3.3.3 | Draft mounting and support requirements: specify support provisions (meter shall be independently supported per manufacturer requirements; isolation from piping stress; support frequency and type per piping specification PKG-14); cite manufacturer requirements |
| 3.3.4 | Draft instrument tap location requirements per Specification.md REQ-03: specify temperature tap location (within 5D downstream of meter example; TBD per manufacturer), pressure tap locations (upstream and downstream per manufacturer), density tap location if applicable (per manufacturer); cite manufacturer recommendations |
| 3.3.5 | Reference DEL-12.01 drawings per Specification.md REQ-14: "Installation details shown in DEL-12.01 Metering Design Drawing Set; drawings incorporate manufacturer requirements and site-specific conditions" |

#### 3.4: Proving Requirements

| Action | Description |
|--------|-------------|
| 3.4.1 | Draft proving method requirement per Specification.md REQ-04, REQ-17: specify proving method — (a) in-line prover (sphere or piston; specify prover type, capacity, connections), (b) portable prover (specify prover type, connections, operational requirements), (c) master meter (specify master meter type, calibration, parallel arrangement), or (d) combination; cite source (ER requirement, Measurement Canada requirement, or operational selection); coordinate with DEL-12.01 proving connection details |
| 3.4.2 | Draft proving frequency requirement per Specification.md REQ-18: specify proving frequency (e.g., quarterly, semi-annually, annually, after maintenance, or per operational schedule; TBD from ER Vol 2 Part 2 or Measurement Canada); cite source (ER clause, Measurement Canada regulation, or custody transfer standard) |
| 3.4.3 | Draft acceptance criteria for proving per Specification.md REQ-19: specify acceptance criteria (e.g., "Meter factor drift shall be within ±0.05% of previous proving or within ±0.1% of manufacturer's baseline, whichever is tighter"; TBD from applicable standard); cite source (API MPMS Chapter 4, OIML R117, or Measurement Canada) |
| 3.4.4 | Draft prover calibration requirements: specify prover calibration traceability (traceable to Measurement Canada, NIST, or equivalent national metrology institute), calibration interval (e.g., 12 months), calibration method (volumetric calibration, gravimetric calibration, or per applicable standard) |

#### 3.5: Instrumentation Requirements

| Action | Description |
|--------|-------------|
| 3.5.1 | Draft temperature measurement requirements per Specification.md REQ-03: specify transmitter type (RTD Pt100, thermocouple, or per project standard; TBD), range (e.g., 0-100°C; TBD from operating conditions), accuracy (e.g., ±0.1°C; TBD from accuracy budget), signal output (4-20 mA, digital, or per project standard; TBD), communication protocol if applicable (HART, Profibus, or per PKG-19; TBD) |
| 3.5.2 | Draft pressure measurement requirements per Specification.md REQ-03: specify transmitter type (gauge pressure, absolute pressure, differential pressure if required; TBD), range (e.g., 0-10 bar; TBD from operating conditions), accuracy (e.g., ±0.1% of span; TBD from accuracy budget), signal output, communication protocol |
| 3.5.3 | Draft density measurement requirements if applicable per Specification.md REQ-03: if volumetric meter requires density compensation, specify density transmitter type (online densitometer, Coriolis-based density, or laboratory sampling), range (e.g., 0.90-0.94 g/cm³ for canola oil; TBD from product data), accuracy (e.g., ±0.001 g/cm³; TBD from accuracy budget), signal output, communication protocol; if Coriolis meter with integral density measurement, specify density output requirements |

#### 3.6: Electrical and Controls Requirements

| Action | Description |
|--------|-------------|
| 3.6.1 | Draft power supply requirements per Specification.md REQ-15 (electrical interface): specify voltage (120VAC, 240VAC, 480VAC, 24VDC, or per PKG-17; TBD), frequency (50Hz, 60Hz; TBD), power consumption (typical and maximum; TBD from selected equipment), coordinate with PKG-17 electrical power distribution |
| 3.6.2 | Draft signal output requirements per Specification.md REQ-15 (controls interface): specify signal types (4-20 mA analog for flow, temperature, pressure, density; pulse output for totalizing; digital communication; TBD per PKG-19), signal wiring (2-wire, 3-wire, 4-wire; TBD), coordinate with PKG-19 control systems |
| 3.6.3 | Draft communication protocol requirements per Specification.md REQ-15 (controls interface): specify protocol (Modbus RTU, Modbus TCP, HART, Profibus, Foundation Fieldbus, or per PKG-19; TBD), data points (flow rate instantaneous, total cumulative, total batch, temperature, pressure, density, alarms, status; TBD), coordinate with PKG-19 control systems |
| 3.6.4 | Draft HMI requirements: specify display requirements (local display on meter vs. DCS HMI only; TBD), data logging requirements (batch records, cumulative totals, alarm history; TBD), totalizing requirements (cumulative, batch reset, non-resettable grand total; TBD per Measurement Canada if applicable) |
| 3.6.5 | Draft area classification requirements per Specification.md REQ-15 (electrical interface): specify hazardous area classification (Division 1, Division 2, non-classified; TBD from ER Vol 2 Part 2 area classification drawings), equipment certification (CSA, UL, ATEX, IECEx; TBD), installation requirements (intrinsically safe, explosion-proof, general purpose; TBD), coordinate with PKG-17 electrical |

#### 3.7: QA Requirements

| Action | Description |
|--------|-------------|
| 3.7.1 | Draft calibration certificate requirements per Specification.md REQ-20: specify traceability (traceable to Measurement Canada, NIST, or equivalent national metrology institute), calibration points (minimum 5 points across flow range, or per applicable standard; TBD), uncertainty statement (calibration uncertainty shall be documented and shall be ≤1/3 of specified meter accuracy; TBD from standard) |
| 3.7.2 | Draft material certificate requirements per Specification.md REQ-20: specify material test reports (MTRs) for wetted components (body, internals, seals), chemical composition and mechanical properties per material specifications, traceability to heat lot |
| 3.7.3 | Draft factory acceptance test (FAT) requirements per Specification.md REQ-20: specify FAT location (vendor facility), FAT witness (client representative witness optional or mandatory; TBD from project QA plan), FAT scope (flow test at multiple flow rates across range, accuracy verification, functional test of signals and communications, proving if prover included, visual inspection), FAT acceptance criteria (accuracy per specification, signals functional, no visible defects), FAT documentation (test protocol, test results, nonconformance reports if any) |
| 3.7.4 | Draft site acceptance test (SAT) requirements per Specification.md REQ-20: specify SAT scope (installation verification per drawings, proving upon installation, functional test of integrated system, accuracy verification), SAT acceptance criteria (installation per drawings, proving acceptance per proving criteria, system functional), SAT documentation (test protocol, test results, as-built verification) |
| 3.7.5 | Draft inspection and test plan (ITP) requirements per Specification.md REQ-20: specify ITP shall be submitted by vendor; ITP shall identify hold points (mandatory inspection/witness points where work cannot proceed without client approval) and witness points (optional inspection/witness points); typical hold points: material receiving inspection, FAT, shipment release; typical witness points: fabrication inspections, subcomponent tests |

#### 3.8: Documentation Requirements

| Action | Description |
|--------|-------------|
| 3.8.1 | Draft data sheet submittal requirements per Specification.md REQ-23: specify data sheets per DEL-12.04 Metering Data Sheet Package; data sheets shall document flow meter specifications, transmitter specifications, prover specifications; data sheets shall demonstrate compliance with specification requirements |
| 3.8.2 | Draft drawing submittal requirements per Specification.md REQ-23: specify drawings per DEL-12.01 Metering Design Drawing Set; drawings shall show installation details consistent with this specification and manufacturer requirements |
| 3.8.3 | Draft calculation submittal requirements per Specification.md REQ-23: specify calculations per DEL-12.03 Metering Design Calculations; calculations shall verify meter sizing, flow capacity, and performance per this specification |
| 3.8.4 | Draft test record submittal requirements per Specification.md REQ-23: specify test records per DEL-12.05 Metering Installation & Test Records; records shall demonstrate compliance with this specification (calibration certificates, FAT results, SAT results, proving records) |
| 3.8.5 | Draft O&M manual requirements per Specification.md REQ-23: specify operation and maintenance manuals shall be provided; manuals shall include operating instructions, maintenance procedures, troubleshooting, spare parts lists |
| 3.8.6 | Draft as-built documentation requirements per Specification.md REQ-23: specify as-built drawings and data sheets shall be provided upon project completion; as-built documentation shall reflect actual installed configuration |

**Output:** Draft specification with complete technical requirements covering all topics

**Verification:** All Specification.md requirements (REQ-03 through REQ-23) addressed in draft; no critical topics missing

---

### Step 4: Add Verification Hooks

**Objective:** For each requirement, define verification method and acceptance criteria to enable DEL-12.05 compliance demonstration.

| Action | Description | Output |
|--------|-------------|--------|
| 4.1 | For each specification requirement, define verification method per Specification.md REQ-21: **Review** (document review, technical review), **Inspection** (visual inspection, dimensional inspection), **Test** (flow test, accuracy test, functional test, FAT, SAT, proving), **Certificate** (calibration certificate, material certificate, Measurement Canada approval if required), **Calculation** (verification calculation per DEL-12.03) | Verification methods for each requirement |
| 4.2 | Ensure verification methods enable DEL-12.05 compliance demonstration per Specification.md REQ-21: each testable requirement shall have FAT or SAT test method; test results will be recorded in DEL-12.05; certificates will be filed in DEL-12.05; proving records will be compiled in DEL-12.05 | Testability verification |
| 4.3 | Define acceptance criteria for each testable requirement per Specification.md REQ-21: specify pass/fail criteria (e.g., "Accuracy test: meter shall achieve ±0.15% accuracy or better across flow range; Pass if all test points ≤±0.15%; Fail if any test point >±0.15%"); acceptance criteria enable clear compliance determination | Acceptance criteria for testable requirements |
| 4.4 | Add requirements traceability matrix per Specification.md REQ-24: create matrix with columns: Specification Clause, Requirement Description, Source (ER clause, standard clause, or ASSUMPTION), Verification Method, Acceptance Criteria, Related Deliverable (DEL-12.01, DEL-12.03, DEL-12.04, DEL-12.05); map each specification clause to source | Requirements traceability matrix |

**Output:** Specification with verification methods, acceptance criteria, and traceability matrix

**Verification:** Every requirement has verification method per Specification.md REQ-21; traceability matrix complete per REQ-24

---

### Step 5: Discipline Check

**Objective:** Independent Process discipline engineer reviews specification for completeness, technical correctness, and compliance.

| Action | Description | Verification |
|--------|-------------|--------------|
| 5.1 | Checker reviews specification for completeness per Specification.md REQ-02: verify both specification artifacts present (custody transfer flow meter specification, metering system specification); verify all required topics covered per Datasheet.md Construction section (performance, flow range, materials, installation, proving, instrumentation, electrical/controls, QA) | Completeness check |
| 5.2 | Checker reviews for internal consistency: verify requirements are mutually compatible; identify conflicts or contradictions; verify terminology is consistent; verify units are consistent (SI vs. Imperial; TBD per project conventions) | Consistency check |
| 5.3 | Checker reviews for testability per Specification.md REQ-21: verify all requirements are testable (have defined verification method); verify acceptance criteria are clear and measurable; identify untestable requirements for revision | Testability check |
| 5.4 | Checker reviews for alignment with objectives per Specification.md REQ-09, REQ-10: verify flow ranges support OBJ-2 (1,000,000 MT/a throughput); verify accuracy, proving, and uncertainty requirements support OBJ-10 (custody transfer accuracy) | Objective alignment check |
| 5.5 | Checker reviews for standard compliance: verify requirements align with applicable custody transfer standards (API MPMS, OIML R117, Measurement Canada); identify deviations from standard requirements; verify standard citations are correct | Standard compliance check |
| 5.6 | Checker reviews traceability matrix per Specification.md REQ-24: verify all specification clauses are mapped to sources (ER, standards, ASSUMPTION); verify TBD items are flagged with source needed; verify ASSUMPTION items have basis stated | Traceability check |
| 5.7 | Checker documents review comments: prepare discipline check comment list with comment number, specification section, comment description, severity (critical/major/minor), recommended action | Discipline check comment list |
| 5.8 | Originator and checker coordinate to resolve comments: review comments together, agree on resolutions, originator implements agreed resolutions, checker verifies resolutions | Comment resolution |
| 5.9 | Checker records discipline check completion: date, checker name, summary of review, confirmation that all comments are resolved, checker signature | Discipline check record |

**Output:** Discipline-checked specification with all comments resolved; discipline check record

**Verification:** Discipline check record complete; all comments resolved; checker signature confirms completion

---

### Step 6: Interdisciplinary Check (IDC)

**Objective:** Coordinate with interfacing disciplines to verify interface definitions and resolve interface issues.

| Action | Description | Participants |
|--------|-------------|--------------|
| 6.1 | Distribute specification to interfacing discipline leads per Specification.md REQ-16: (a) Piping (PKG-14) — review piping interface requirements (size, rating, isolation, straight-run), (b) Electrical (PKG-17) — review power supply requirements (voltage, frequency, area classification), (c) Instrumentation (PKG-20) — review transmitter specifications (temperature, pressure, density), (d) Controls (PKG-19) — review control integration (signals, protocols, HMI, totalizing); provide sufficient review time (typically 5-10 working days; TBD per project procedures) | IDC distribution to all interfacing disciplines |
| 6.2 | Hold IDC meeting to review interfaces per Specification.md REQ-15: review metering system interfaces (piping connections, electrical power, control/communication signals, instrumentation integration, proving connections); discuss interface requirements and identify any interface issues or conflicts | IDC meeting with all disciplines represented |
| 6.3 | Document IDC comments: prepare IDC comment list with comment number, commenting discipline, specification section, comment description, interface affected, recommended action; **Example comments**: "PKG-14 Piping: Straight-run requirement 10D upstream may conflict with available space in piping layout; coordinate with DEL-12.01 drawings to verify straight-run is achievable"; "PKG-19 Controls: Modbus RTU protocol acceptable; confirm baud rate and register mapping" | IDC comment list |
| 6.4 | Resolve interface comments: coordinate with commenting disciplines to agree on resolutions; update specification as needed to resolve interface issues; verify changes do not create new conflicts; **Example resolutions**: "Coordinated with PKG-14; piping layout revised to provide 10D straight-run; no specification change needed"; "Added specification clause: Modbus RTU, 9600 baud, register mapping per Appendix X" | Comment resolution with interface coordination |
| 6.5 | Confirm interface definitions are complete and coordinated: obtain confirmation from each discipline that their interface comments are resolved and interfaces are acceptable; verify all metering system interfaces defined per Specification.md REQ-15 are coordinated | Interface sign-off from all disciplines |
| 6.6 | Record IDC completion: date, participants (discipline leads who participated), summary of interface review, confirmation that all interface comments are resolved, IDC record with discipline sign-offs | IDC record |

**Output:** IDC-reviewed specification with all interface comments resolved; IDC record with interface sign-offs from participating disciplines

**Verification:** IDC record complete; all participating disciplines confirm interfaces are acceptable; all comments resolved

---

### Step 7: Issue for Review or Construction

**Objective:** Finalize specification, obtain required approvals, and issue per project document control procedures.

| Action | Description | Output |
|--------|-------------|--------|
| 7.1 | Apply final document control metadata per Specification.md documentation requirements: update document number per project numbering system (TBD; ER Vol 2 Part 1), add final revision number (00 for initial issue, or A/B/C for subsequent issues, or 01/02/03 for construction issues; TBD per project convention), add date of issue, add originator name and signature (confirming authoring and discipline check resolution), add checker name and signature (confirming discipline check completion), add approver name and signature (authorizing issue per project procedures; TBD ER Vol 2 Part 1) | Document control metadata complete |
| 7.2 | Obtain required approvals per project procedures (TBD; ER Vol 2 Part 1): Process Lead approval (technical content, alignment with ER requirements), Engineering Manager approval (if required by project procedures), Quality Manager approval (if required for custody transfer specifications), Client approval (if required for review issue; TBD per contract); approval authorities TBD from ER Vol 2 Part 1 | Approval signatures |
| 7.3 | Prepare issue package: assemble complete specification document(s) (custody transfer flow meter specification, metering system specification), include requirements traceability matrix, include discipline check record, include IDC record, prepare transmittal letter or form per project procedures documenting issue purpose and revision | Issue package |
| 7.4 | Issue per project document control process (TBD; ER Vol 2 Part 1): submit to document management system, assign issue status ("Issued for Review" for client review issues, "Issued for Construction" for final construction issues, "Issued for Record" for as-built issues; TBD per project convention), distribute to required recipients per distribution list (client, internal disciplines, vendors if applicable; distribution list TBD) | Document management system entry; distribution |
| 7.5 | Place issue copy in deliverable folder structure: place issued copy in `2_Checking/To/` for review issues (client review or internal review), or place issued copy in `3_Issued/` for construction or as-built issues — per project convention and lifecycle state | Filed issue copy |
| 7.6 | Update deliverable status: if issuing for review, update `_STATUS.md` to CHECKING with note "Issued for Review, Rev 00, Date YYYY-MM-DD"; if issuing for construction, update `_STATUS.md` to ISSUED with note "Issued for Construction, Rev 01, Date YYYY-MM-DD" — record issue date, revision, and issue purpose in status history | Status update |

**Output:** Issued specification with all approvals; issue record in document management system; deliverable status updated

**Verification:** All approval signatures obtained; issue record complete in document management system; specification filed per project conventions; `_STATUS.md` updated

---

## Verification

### Verification Activities

| Activity | Requirement Verified | Method | Record |
|----------|---------------------|--------|--------|
| Artifact completeness check | REQ-02 | Checklist against Decomposition:357 — verify custody transfer flow meter specification and metering system specification are present | Document index; discipline check Step 5.1 |
| Technical content review | REQ-01, REQ-03 through REQ-09, REQ-11 through REQ-19 | Discipline check for technical correctness, completeness, performance alignment | Discipline check record Step 5 |
| Interface review | REQ-15, REQ-16 | IDC with interfacing disciplines (PKG-14, PKG-17, PKG-19, PKG-20) | IDC record Step 6 |
| Traceability review | REQ-24 | Traceability matrix review — verify all specification clauses mapped to sources (ER, standards, ASSUMPTION) | Traceability matrix Step 4.4; discipline check Step 5.6 |
| Testability review | REQ-21 | Verification method check — verify each requirement has defined verification method enabling DEL-12.05 compliance demonstration | Step 4.2; discipline check Step 5.3 |
| Cross-document consistency check | REQ-09, REQ-14, REQ-23 | Verify specification is consistent with DEL-12.01 drawings (installation requirements), DEL-12.03 calculations (flow ranges, sizing), DEL-12.04 data sheets (equipment parameters) | Discipline check Step 5.2 |
| Objective alignment review | REQ-09, REQ-10 | Verify specification supports OBJ-2 (throughput) and OBJ-10 (custody transfer accuracy) | Discipline check Step 5.4 |
| Standard compliance review | REQ-06, REQ-07, REQ-08, REQ-18, REQ-19 | Verify requirements align with applicable custody transfer standards (API MPMS, OIML R117, Measurement Canada) | Discipline check Step 5.5 |

### Acceptance Criteria

| Criterion | Verification Method | Source |
|-----------|---------------------|--------|
| Both specification artifacts present | Document index review; Step 5.1 | Specification.md REQ-02; Decomposition:357 |
| Service coverage | Specification covers both rail unloading and marine loading with service-specific requirements | Specification.md REQ-01; discipline check Step 5.1 |
| Requirements traceable | Traceability matrix complete; all clauses mapped to sources or labeled TBD/ASSUMPTION | Specification.md REQ-24; Step 4.4; discipline check Step 5.6 |
| Requirements testable | Verification methods defined for all requirements; acceptance criteria clear and measurable | Specification.md REQ-21; Step 4.2; discipline check Step 5.3 |
| Interface coverage | All metering system interfaces defined (piping, electrical, controls, instrumentation, proving) and coordinated with interfacing disciplines | Specification.md REQ-15; IDC Step 6 |
| Standard compliance | Requirements align with applicable custody transfer standards; deviations identified and justified | Specification.md Standards section; discipline check Step 5.5 |
| Performance alignment | Specification supports OBJ-2 (throughput) and OBJ-10 (accuracy) | Specification.md REQ-09, REQ-10; discipline check Step 5.4 |
| Check records complete | Discipline check and IDC records complete with all comments resolved | Specification.md REQ-22; Step 5.9; Step 6.6 |

### Sign-off Requirements

| Role | Responsibility | Verification | Source |
|------|----------------|--------------|--------|
| Originator | Technical content accuracy, requirements traceability, comment resolution | Originator signature on specification confirming authoring and discipline check resolution | ASSUMPTION; project quality procedures |
| Checker | Discipline check completion, technical verification, testability confirmation | Checker signature on specification confirming discipline check completion | ASSUMPTION; project quality procedures |
| IDC Participants | Interface coordination, interface acceptance | IDC record with discipline sign-offs confirming interface acceptance | ASSUMPTION; IDC procedure |
| Approver | Authorization for issue, compliance with ER requirements, alignment with project objectives | Approver signature on specification authorizing issue | TBD; ER Vol 2 Part 1 |

## Records

### Documentation Outputs

| Output | Description | Source |
|--------|-------------|--------|
| Custody Transfer Flow Meter Specification | Technical specification document defining performance, materials, installation, and testing requirements for custody transfer flow meters | Decomposition:357; Specification.md REQ-02; Steps 1-3 |
| Metering System Specification | System-level specification document defining instrumentation, proving, control integration, data logging, and QA requirements | Decomposition:357; Specification.md REQ-02; Steps 1-3 |
| Requirements Traceability Matrix | Matrix mapping specification clauses to Employer's Requirements source clauses; identifies TBD and ASSUMPTION items | Specification.md REQ-24; Step 4.4 |
| Discipline Check Record | Record of discipline check with date, checker name, comment list, resolutions, and sign-off | Specification.md REQ-22; Step 5.9 |
| IDC Record | Record of interdisciplinary check with date, participants, interface comment list, resolutions, and discipline sign-offs | Specification.md REQ-22; Step 6.6 |
| Issue Record | Record of specification issue with date, revision, approvals, distribution | Specification.md documentation requirements; Step 7.4 |

### Record Management

| Attribute | Value | Source |
|-----------|-------|--------|
| Filing Location (Working) | `1_Working/DEL-12.02_Metering_Technical_Specification/` | Current location |
| Filing Location (Review) | `2_Checking/To/` (for review issues); `2_Checking/From/` (for returned review comments) | Project convention |
| Filing Location (Issued) | `3_Issued/` (for construction or as-built issues) | Project convention |
| Document Management System | Per project document control procedures (TBD; ER Vol 2 Part 1) | TBD |
| Retention Period | Per project quality procedures; typically life of facility for custody transfer specifications | TBD |
| Format | Electronic files (MS Word, PDF, or per project standard); electronic distribution | ASSUMPTION |
| Backup and Version Control | Per project IT procedures; specification files under version control in document management system | TBD |

### Status Transitions

Status transitions are managed per `_STATUS.md` in the deliverable folder:

| From State | To State | Trigger | Responsible |
|------------|----------|---------|-------------|
| INITIALIZED | IN_PROGRESS | Specification authoring commences (Step 1) | Process Engineer (originator) |
| IN_PROGRESS | CHECKING | Specification submitted for client review (Step 7 for review issue) | Process Engineer (originator) |
| CHECKING | IN_PROGRESS | Review comments received requiring revision | Process Engineer (originator) |
| CHECKING | ISSUED | Approved for construction (Step 7 for construction issue) | Approver |

**Note:** Status state transitions are recorded in `_STATUS.md` with date, state change, and brief description. Detailed issue history is maintained in the document management system.

### Revision Management

| Revision | Purpose | Typical Trigger | Approval Required |
|----------|---------|-----------------|-------------------|
| 00 | Initial issue for client review | First issue to client for review and comment | Process Lead |
| A, B, C... | Subsequent review issues incorporating client comments | Client review comments received and incorporated | Process Lead |
| 01, 02, 03... | Issued for construction | Client approval received; all review comments resolved; ready for procurement and construction | Engineering Manager |
| As-built revisions | Incorporate field changes and as-built verification | Construction complete; vendor data finalized; as-built drawings available | As-built process per project procedures (TBD) |

**Note:** Revision numbering convention TBD from ER Vol 2 Part 1 project document control procedures.
