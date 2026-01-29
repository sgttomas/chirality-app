# Datasheet: DEL-10.01 Railcar Unloading Design Drawing Set

## Identification

| Field | Value |
|-------|-------|
| Deliverable ID | DEL-10.01 |
| Name | Railcar Unloading Design Drawing Set |
| Package | PKG-10 Railcar Unloading System |
| Discipline | Process |
| Type | Drawing |
| Responsible | D&B Contractor |
| Status | INITIALIZED |

## Attributes

| Attribute | Value | Procedure Link |
|-----------|-------|----------------|
| Drawing Number Series | **TBD** — per project document numbering procedure | Procedure.md Step 1, Step 6 |
| Total Sheet Count | **TBD** — minimum 4 sheets (GA, arrangements, header layout, containment details) per anticipated artifacts; actual count per design complexity | Procedure.md Step 1 |
| Sheet Size | **TBD** — per project CAD standard (typical: ANSI D or ISO A1 for GA/arrangements; ANSI C or ISO A3 for details) | Specification.md QA-01; Procedure.md Step 2 |
| Scale | **TBD** — varies by sheet type: GA 1:100 or 1:200; arrangements 1:50 or 1:25; header layout 1:50 or 1:100; details 1:20 to 1:50 as required for clarity | Specification.md QA-01; Guidance.md §Examples |
| CAD Standard | **TBD** — per Employer's Requirements / contractor CAD procedures (line weights, layers, symbols, title block format) | Specification.md §Standards, QA-01; Procedure.md Step 2, Step 5 |
| Revision Control | **TBD** — per project document control procedure (revision numbering system, revision clouds, revision history in title block) | Procedure.md Step 6; Specification.md QA-02 |
| Classification | **TBD** — per project security/confidentiality requirements (e.g., Proprietary, For Internal Use, Unclassified) | Procedure.md Step 6 |

## Conditions

**Operating / Environmental Context:**

The Railcar Unloading Design Drawing Set defines the design arrangement and details for the railcar unloading system serving the Canola Oil Transload Facility at Fraser Surrey Terminal, 11060 Elevator Road, Surrey, BC. The facility has a permitted throughput of 1,000,000 MT/annum with 32 railcar unloading stations capable of simultaneous operations. (**Source:** decomposition §1 Project Overview; README §Project snapshot; Specification.md PF-01)

**PKG-10 Scope Elements (from decomposition §5 Package Descriptions — PKG-10):**

| Element | Quantity/Description | Drawing Coverage | Specification Link | Guidance Link |
|---------|---------------------|------------------|--------------------|--------------------|
| Unloading arms | 32 unloading arm assemblies (bottom-loading type **ASSUMPTION**) | Unloading arm arrangement drawings | Specification.md FN-03 | Guidance.md §Trade-offs |
| Quick-connects | Coupler assemblies for railcar connection (32 connections) | Unloading arm arrangement details | Specification.md FN-03 | Guidance.md §Principles |
| Gravity flow header | Collection header from unloading stations to storage (single system with branch connections) | Header pipe layout drawings | Specification.md FN-04, PF-04 | Guidance.md §Principles (gravity flow design) |
| Spill containment pans | Under-track containment for each station (32 individual pans **PROPOSAL** or combined system **TBD**) | Containment details drawings | Specification.md FN-05, PF-03 | Guidance.md §Trade-offs |
| Collection system | Sumps, drains, sump pumps for spill recovery | Containment details drawings | Specification.md FN-05 | Guidance.md §Considerations |
| Atmospheric venting | Vent connections and routing from railcars (32 vent connections) | GA and arrangement drawings | Specification.md FN-01 | Guidance.md §Principles |
| Flow indicators | Local flow indication devices at each station (32 indicators) | GA and arrangement drawings | Specification.md FN-01; IF-04 | Guidance.md §Principles |

**Environmental and Design Conditions:**

| Parameter | Value | Source | Guidance Link | Procedure Link |
|-----------|-------|--------|---------------|----------------|
| Operating temperature range | **TBD** — per product properties and site climate (canola oil pour point typically -10°C; winterization may be required) | ER Vol 2 clauses **TBD** | Guidance.md §Considerations (product properties, site conditions) | Procedure.md Step 2 (design development) |
| Ambient temperature range | **TBD** — Fraser Surrey climate data (typical: -15°C to +35°C design range) | Site climate data **TBD**; BC climate normals | Guidance.md §Considerations | Procedure.md Step 2 |
| Environmental classification | **TBD** — per site classification study (outdoor, weather-exposed installation) | ER Vol 2 clauses **TBD** | — | Procedure.md Step 2 |
| Hazardous area classification | **TBD** — per Employer's Requirements / HAC study (expect Class I Div 2 or Zone 2 typical for edible oil handling) | ER Vol 2 clauses **TBD**; HAC study deliverable | Specification.md §Standards; Guidance.md §Considerations | Procedure.md Step 2 (show classification zones on GA) |
| Seismic requirements | **TBD** — per BC Building Code / site-specific criteria (Fraser Surrey in seismic zone; expect Site Class and seismic parameters per geotechnical study) | BC Building Code clauses **TBD**; geotechnical study (PKG-02) | Specification.md §Standards; Guidance.md §Considerations | Procedure.md Step 4 (IDC with PKG-05 structural) |
| Design life | **TBD** — per Employer's Requirements (typical: 25–30 years for permanent facilities; affects material selection and corrosion allowances) | ER Vol 2 clauses **TBD** | Guidance.md §Principles | Procedure.md Step 2 |
| Product handled | Canola oil (food-grade vegetable oil; viscosity 30–60 cP @ 20°C typical; density ~0.92 kg/L) | Decomposition §1; product properties **TBD** | Guidance.md §Considerations (product properties) | Procedure.md Step 2 (affects header sizing) |
| Throughput capacity | 1,000,000 MT/annum utilizing 32 unloading stations (simultaneous operations capability **TBD**) | Decomposition §1; §2 OBJ-2; Specification.md PF-01 | Guidance.md §Principles (OBJ-2); Guidance.md §Considerations | Procedure.md Step 2; DEL-10.03 (throughput analysis) |

## Construction

**Drawing Set Composition (Anticipated Artifacts per Decomposition §5 DEL-10.01):**

| Drawing Type | Content | Cross-Reference | Procedure Step | Guidance Link |
|--------------|---------|-----------------|----------------|----------------|
| Unloading System GA | Overall layout showing 32 unloading positions, header routing, containment areas, equipment locations, interface points with adjacent disciplines | Specification.md §Scope, §Documentation; Procedure.md Step 2; Guidance.md §Examples | Procedure.md Step 2 (production) | Guidance.md §Examples (typical scale 1:100 or 1:200) |
| Unloading Arm Arrangement | Arm positions, clearances, quick-connect details, reach envelopes for each of 32 stations, railcar coupling interface, operator access platforms | Specification.md FN-03, IF-01; DEL-10.04 (Data Sheets — arm specifications); Guidance.md §Principles; Procedure.md Step 2 | Procedure.md Step 2 (production), Step 4 (IDC) | Guidance.md §Examples (typical scale 1:50 or 1:25; may require multiple sheets for 32 stations) |
| Header Pipe Layout | Gravity flow header routing, pipe sizes (per DEL-10.03 calculations), slopes (minimum 1:100 for gravity drainage), connection points, branch connections from each of 32 stations, isolation valves (operational flexibility per OBJ-4), air release provisions at high points | DEL-10.03 (Calculations — header sizing, hydraulic profile); PKG-14 (Process Piping interface at discharge connection); Specification.md FN-04, PF-04, IF-05; Guidance.md §Principles (gravity flow design) | Procedure.md Step 2 (production), Step 4 (IDC with PKG-14) | Guidance.md §Examples (typical scale 1:50 or 1:100) |
| Containment Details | Spill containment pans (32 individual or combined system per Guidance.md §Trade-offs), collection sumps, drain routing, sump pump locations, containment volume verification (reference to DEL-10.03 calculations) | Specification.md FN-05, PF-03; DEL-10.03 (Calculations — containment volume per largest credible spill); DEL-10.02 (Tech Spec — containment requirements) | Procedure.md Step 2 (production), Step 4 (IDC with PKG-05, PKG-17, PKG-20) | Guidance.md §Examples (typical scale 1:20 or 1:50); Guidance.md §Trade-offs (individual vs. common containment) |

**Interface Elements (to be shown on drawings per Specification.md IF-01 through IF-06):**

| Interface | Discipline/Package | Drawing | Specification Req | Procedure Step | Coordination Need |
|-----------|-------------------|---------|-------------------|----------------|-------------------|
| Rail track alignment and railcar positions | PKG-07 Rail Works | GA, Arm Arrangement | IF-01 | Step 4 (IDC) | Station positions relative to track centerline; clearances to track; track curvature effects on station spacing; railcar positioning tolerance |
| Civil/structural supports and foundations | PKG-05 Concrete Structures / PKG-06 Structural Steelwork | All drawings | IF-02 | Step 4 (IDC) | Foundation locations and elevations for unloading arms; pipe support locations and loads; containment structure supports; seismic design coordination |
| Electrical connections for sump pumps, area lighting | PKG-17 Electrical | Containment Details, GA | IF-03 | Step 4 (IDC) | Sump pump power supply and cable routing; area lighting requirements; hazardous area classification boundaries (if shown on GA) |
| Instrumentation connections for flow indicators, level switches, temperature elements | PKG-20 Field Instrumentation | GA, Arm Arrangement, Containment Details | IF-04 | Step 4 (IDC) | Flow indicator locations and mounting at each of 32 stations; sump level switch locations; temperature element locations (**if required for winterization**) |
| Process piping connections downstream of header | PKG-14 Process Piping | Header Pipe Layout | IF-05 | Step 4 (IDC) | Header discharge connection size, location, elevation; coordinate with downstream piping layout to storage tanks; isolation valve locations |

**ASSUMPTION:** Interface coordination will be performed through IDC process per Procedure.md Step 4, with interface points clearly marked on drawings for multi-discipline review and sign-off (Specification.md QA-04).

## References

| Reference | Location | Relevance | Document Link |
|-----------|----------|-----------|---------------|
| Decomposition | `test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md` | PKG-10 scope (§5); DEL-10.01 definition; objective mapping (§6: OBJ-1 Safe Operation, OBJ-2 Throughput, OBJ-4 Operational Flexibility, OBJ-7 Environmental Protection) | Guidance.md §Principles (objective alignment) |
| Employer's Requirements Vol 2 Pt 1 | `test/Volume_2_Part_1_Employers_Requirements.pdf` | Clauses **TBD** — unloading system requirements, standards, interfaces, performance criteria | Specification.md §Requirements, §Standards |
| Employer's Requirements Vol 2 Pt 2 | `test/Volume_2_Part_2_Employers_Requirements.pdf` | Clauses **TBD** — technical specifications, design criteria, equipment requirements | Specification.md §Requirements; Procedure.md §Prerequisites |
| Employer's Requirements Vol 2 Pt 3 | `test/Volume_2_Part_3_Employers_Requirements.pdf` | Clauses **TBD** — quality requirements, document control, CAD standards | Specification.md QA-xx; Procedure.md Steps 5, 6 |
| Specification.md | This deliverable folder | Requirements driving drawing content (functional, performance, interface, quality) | All sections; bidirectional link |
| Guidance.md | This deliverable folder | Design intent, principles, considerations, trade-off analysis | All sections; bidirectional link |
| Procedure.md | This deliverable folder | Production workflow, verification, IDC process, records management | All sections; bidirectional link |
| DEL-10.02 | `execution/PKG-10_Railcar_Unloading_System/1_Working/DEL-10.02_*/Specification.md` | Technical Specification for unloading system (performance requirements, materials, equipment specifications) | Specification.md §Requirements; Procedure.md Step 2 (design basis) |
| DEL-10.03 | `execution/PKG-10_Railcar_Unloading_System/1_Working/DEL-10.03_*/` | Design Calculations (header sizing, hydraulic profile, containment volume, throughput analysis) | §Construction (Header Pipe Layout, Containment Details); Procedure.md Step 2 (verify calculations) |
| DEL-10.04 | `execution/PKG-10_Railcar_Unloading_System/1_Working/DEL-10.04_*/` | Data Sheet Package (32 unloading arm data sheets, equipment specifications, vendor information) | §Construction (Arm Arrangement drawings); Procedure.md Step 2 (equipment details) |
| _DEPENDENCIES.md | This deliverable folder | NOT_TRACKED — dependencies coordinated externally per project schedule and stage gates | Procedure.md §Prerequisites (dependency tracking mode) |

**Note:** Specific Employer's Requirements clause references to be populated during detailed design phase when ER content is reviewed (Procedure.md Step 2). Mark drawing notes with ER clause references where applicable for traceability.

**Pass 3 Verification:** All references bidirectionally linked; all TBDs marked and sourced; all ASSUMPTIONs and PROPOSALs labeled.
