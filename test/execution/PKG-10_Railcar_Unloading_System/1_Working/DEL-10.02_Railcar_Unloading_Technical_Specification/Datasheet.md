# Datasheet: DEL-10.02 Railcar Unloading Technical Specification

## Identification

| Field | Value |
|-------|-------|
| Deliverable ID | DEL-10.02 |
| Name | Railcar Unloading Technical Specification |
| Package | PKG-10 Railcar Unloading System |
| Discipline | Process |
| Type | Specification |
| Responsible | D&B Contractor |
| Status | INITIALIZED |

## Attributes

| Attribute | Value | Procedure Link |
|-----------|-------|----------------|
| Document Number | **TBD** — per project document numbering procedure | Procedure.md Step 6 |
| Specification Type | Technical Specification (Equipment & Systems Performance, Materials, Workmanship) | Specification.md §Scope |
| Revision | **TBD** — per project document control procedure (initial issue: 0 or A per convention) | Procedure.md Step 6 |
| Applicable Standards | **TBD** — see Specification.md §Standards (ASME B31.3, CSA codes, API standards, food-grade standards, AWS welding) | Specification.md §Standards; Procedure.md Step 3 |
| Classification | **TBD** — per project security/confidentiality requirements | Procedure.md Step 6 |
| Compliance Matrix | Required — ER traceability matrix mapping specification requirements to ER clauses (**TBD** format per project or ER requirements) | Specification.md QA-01; Procedure.md Step 2 |

## Conditions

**Operating / Environmental Context:**

The Railcar Unloading Technical Specification defines performance, materials, and workmanship requirements for the railcar unloading system serving the Canola Oil Transload Facility at Fraser Surrey Terminal, 11060 Elevator Road, Surrey, BC. The facility has a permitted throughput of 1,000,000 MT/annum with 32 railcar unloading stations operating by gravity flow to a common header system. (**Source:** decomposition §1 Project Overview; README §Project snapshot; Specification.md §Scope)

**PKG-10 Scope Elements Covered by This Specification:**

| Element | Specification Section | Quantity/Description | Cross-Reference | Specification Link |
|---------|----------------------|---------------------|-----------------|-------------------|
| Unloading arms | Unloading Arm Specification | 32 units (bottom-loading type **ASSUMPTION**) | DEL-10.04 (Data Sheets); DEL-10.01 (Arm Arrangement drawings) | Specification.md FN-01, PF-02 |
| Quick-connects | Unloading Arm Specification | 32 quick-connect couplers (dry-break type typical) | DEL-10.04 (Data Sheets); DEL-10.01 (Arm Arrangement drawings) | Specification.md FN-01, MT-04 |
| Gravity flow header | Header Pipe Specification | Single header system with 32 branch connections | DEL-10.03 (Calculations — header sizing); DEL-10.01 (Header Layout drawings) | Specification.md FN-01, PF-03 |
| Spill containment pans | Containment System Specification | 32 individual pans **PROPOSAL** or combined system **TBD** | DEL-10.03 (Calculations — containment volume); DEL-10.01 (Containment Details drawings) | Specification.md FN-01, PF-04 |
| Collection system | Containment System Specification | Sumps, drains, sump pumps per containment design | DEL-10.01 (Containment Details drawings) | Specification.md FN-01, MT-03 |
| Atmospheric venting | Unloading Arm Specification | 32 vent connections from railcars (to atmosphere or vapor recovery **TBD**) | DEL-10.01 (GA and Arm Arrangement drawings) | Specification.md FN-01 |
| Flow indicators | Instrumentation Requirements (within Unloading Arm Specification) | 32 local flow indicators (one per station) | DEL-10.04 (Data Sheets); PKG-20 (Field Instrumentation coordination) | Specification.md FN-01, IF-04 |

**Design Parameters (Specification Basis):**

| Parameter | Value | Source | Guidance Link | Specification Link |
|-----------|-------|--------|---------------|-------------------|
| Number of unloading stations | 32 | Decomposition §1; README; DEL-10.01 Datasheet | Guidance.md §Considerations (throughput) | Specification.md FN-05 |
| Annual throughput capacity | 1,000,000 MT/annum | Decomposition §1; §2 OBJ-2; README | Guidance.md §Principles (OBJ-2) | Specification.md PF-01 |
| Product | Canola oil (food-grade vegetable oil; viscosity 30–60 cP @ 20°C; density ~0.92 kg/L; pour point -10°C typical) | Decomposition §1; product data **TBD** | Guidance.md §Considerations (product properties) | Specification.md MT-01 (food-grade compatibility) |
| Unloading method | Gravity flow from railcars to header (no pumping at unloading stations) | Decomposition §5 PKG-10; DEL-10.01 Guidance | Guidance.md §Principles (gravity flow) | Specification.md FN-05, PF-03 |
| Operating temperature range | **TBD** — per product properties and winterization requirements (canola oil pour point -10°C; may require heating for winter operations) | ER Vol 2 clauses **TBD**; product data | Guidance.md §Considerations (product properties, site conditions) | Specification.md PF-02 (temperature range) |
| Ambient temperature range | **TBD** — Fraser Surrey climate data (design range -15°C to +35°C typical for outdoor installations) | Site climate data **TBD**; BC climate normals | Guidance.md §Considerations (site conditions) | Specification.md MT-02, MT-03 (material selection for climate) |
| Hazardous area classification | **TBD** — per HAC study (Class I Div 2 or Zone 2 typical for edible oil handling) | ER Vol 2 clauses **TBD**; HAC study deliverable | Guidance.md §Considerations (site conditions) | Specification.md IF-03 (electrical coordination) |
| Seismic requirements | **TBD** — per BC Building Code / site-specific seismic criteria (Fraser Surrey in seismic zone) | BC Building Code clauses **TBD**; PKG-02 geotechnical study | Guidance.md §Considerations (site conditions) | Specification.md IF-02 (structural coordination) |
| Design life | **TBD** — per Employer's Requirements (typical: 25–30 years for permanent facilities) | ER Vol 2 clauses **TBD** | Guidance.md §Principles (design life consideration) | Specification.md MT-02, WK-02 (long-term durability) |
| Unloading rate per station | **TBD** — per ER requirements and DEL-10.03 throughput analysis (affects arm sizing, header sizing) | ER Vol 2 clauses **TBD**; DEL-10.03 calculations | Guidance.md §Considerations (throughput) | Specification.md PF-02, PF-05 |
| Simultaneous operations | **TBD** — number of stations operating simultaneously to achieve throughput (affects header sizing) | DEL-10.03 throughput analysis; ER Vol 2 clauses **TBD** | Guidance.md §Considerations (throughput) | Specification.md PF-01, PF-03 |

## Construction

**Specification Document Structure (Anticipated Artifacts per Decomposition §5 DEL-10.02):**

| Section | Content | Drawing Reference | Calculation Reference | Procedure Step | Guidance Link |
|---------|---------|-------------------|----------------------|----------------|---------------|
| **Unloading Arm Specification** | Performance requirements: flow rate, pressure rating, temperature range, operational envelope (reach, rotation, vertical travel); Material requirements: product contact materials (food-grade compatible), structural materials, seal materials; Workmanship requirements: fabrication, assembly, testing, painting/coating | DEL-10.01 Arm Arrangement (arm positions, clearances, connections) | DEL-10.03 (flow rates, pressure drop) | Procedure.md Step 3 (draft content) | Guidance.md §Considerations (material selection — unloading arms), §Workmanship (testing) |
| **Containment System Specification** | Performance requirements: containment volume (per largest credible spill), drainage time, structural load capacity; Material requirements: pan materials (corrosion-resistant, liquid-tight), drain materials, sump materials, pump materials (product-compatible); Workmanship requirements: welding (liquid-tight construction), surface preparation, testing (leak testing) | DEL-10.01 Containment Details (pan arrangement, sumps, drains) | DEL-10.03 (containment volume, sump sizing) | Procedure.md Step 3 (draft content) | Guidance.md §Considerations (material selection — containment), §Workmanship (welding, testing) |
| **Header Pipe Specification** | Performance requirements: flow capacity (per DEL-10.03), pressure rating, drainage (gravity flow with minimum slopes), air release; Material requirements: pipe materials (carbon steel or stainless steel **TBD**), valve materials, fitting materials, support materials; Workmanship requirements: welding per code, pipe support installation, pressure testing, surface preparation/coating | DEL-10.01 Header Layout (pipe routing, sizes, slopes, valves) | DEL-10.03 (header sizing, hydraulic analysis, pressure drop) | Procedure.md Step 3 (draft content) | Guidance.md §Considerations (material selection — header piping), §Workmanship (welding, testing) |
| **Compliance Matrix** (Appendix or separate document) | ER clause mapping: each ER requirement mapped to specification section addressing it; traceability from ER to specification and vice versa; status tracking (addressed, TBD, not applicable) | — | — | Procedure.md Step 2 (ER clause identification) | Guidance.md §Principles (traceability) |

**Material Requirements Overview (Detailed Requirements in Specification Sections):**

| Component | Material Requirement | Rationale | Specification Link | Guidance Link |
|-----------|---------------------|-----------|--------------------|--------------------|
| Unloading arms (product contact) | **TBD** — food-grade compatible material (stainless steel SS316 or SS304 typical; aluminum alloy acceptable if food-grade certified) | Product contact; food-grade requirement; corrosion resistance; OBJ-7 environmental protection | Specification.md MT-01 (food-grade compatibility) | Guidance.md §Considerations (material selection), §Trade-offs (arm material — aluminum vs. stainless) |
| Quick-connects (seals and gaskets) | **TBD** — food-grade compatible seal materials (EPDM, Viton, or PTFE typical for canola oil; verify compatibility) | Product contact; leak prevention; food-grade requirement; temperature compatibility | Specification.md MT-04 (seal compatibility) | Guidance.md §Considerations (material selection — quick-connects) |
| Header piping (product contact) | **TBD** — carbon steel ASTM A53 Grade B (acceptable for canola oil with internal coating or cathodic protection) or stainless steel SS304/SS316 (higher cost but better corrosion resistance and food-grade compatibility) | Product compatibility; cost consideration; corrosion resistance; food-grade consideration | Specification.md MT-02 (pipe materials) | Guidance.md §Trade-offs (header material — carbon steel vs. stainless) |
| Containment pans (environmental protection) | **TBD** — coated carbon steel (epoxy or polyurethane coating for corrosion protection) or stainless steel SS304 (no coating required; easier cleaning) | Environmental protection (OBJ-7); corrosion resistance (outdoor exposure); liquid-tight construction; cleanability | Specification.md MT-03 (containment materials) | Guidance.md §Considerations (material selection — containment) |
| Sump pumps (wetted parts) | **TBD** — product-compatible materials for wetted parts (stainless steel or coated cast iron; seals compatible with canola oil) | Product recovery; corrosion resistance; reliability | Specification.md MT-03 (pump materials) | Guidance.md §Considerations (material selection — containment) |
| Pipe supports and structural components | **TBD** — structural steel (painted or galvanized for corrosion protection in outdoor environment) | Structural capacity; corrosion resistance; cost; standard availability | Specification.md MT-02 (support materials) | Guidance.md §Considerations (site conditions — outdoor exposure) |

**Workmanship Requirements Overview (Detailed Requirements in Specification Sections):**

| Aspect | Requirement | Standard/Code | Specification Link | Guidance Link |
|--------|-------------|---------------|--------------------|--------------------|
| Welding (piping and pressure equipment) | **TBD** — welding per applicable code (ASME B31.3 for process piping, AWS D1.1 for structural); welder qualification per code; welding procedure specifications (WPS) required; NDE per code (radiography, ultrasonic, or visual per joint type and service) | ASME B31.3 **TBD**; AWS D1.1 **TBD**; ASME Section IX **TBD** | Specification.md WK-01 (welding requirements) | Guidance.md §Workmanship (welding) |
| Surface finish (product contact surfaces) | **TBD** — food-grade contact surfaces: smooth finish (mill finish acceptable for stainless; 125 RMS or better for critical surfaces); no crevices or pockets that trap product; cleanable surface | Food-grade industry standards **TBD**; 3-A Sanitary Standards **TBD** (if applicable) | Specification.md WK-02 (surface finish) | Guidance.md §Workmanship (surface finish) |
| Cleanliness (pre-commissioning) | **TBD** — pre-commissioning cleaning: removal of mill scale, welding debris, construction debris; flushing with cleaning solution (detergent or solvent **TBD**); final rinse with clean water; drying; preservation for storage | Project cleaning procedure **TBD**; vendor recommendations | Specification.md WK-03 (cleanliness) | Guidance.md §Workmanship (cleanliness) |
| Testing (pressure and leak testing) | **TBD** — pressure testing: hydrostatic test per ASME B31.3 (1.5× design pressure typical; hold time per code); leak testing: soap solution or other method at connections and flanges; functional testing: operational testing of arms, valves, pumps | ASME B31.3 **TBD**; manufacturer test procedures **TBD** | Specification.md WK-04 (testing requirements) | Guidance.md §Workmanship (testing) |
| Painting and coating (non-product contact) | **TBD** — surface preparation: SSPC-SP standards **TBD**; coating system: primer + finish coat(s) suitable for outdoor exposure and chemical environment; coating thickness per specification; touch-up after installation | SSPC standards **TBD**; coating manufacturer specifications **TBD** | Specification.md WK-02, MT-03 (coating requirements) | Guidance.md §Considerations (site conditions — outdoor exposure) |

## References

| Reference | Location | Relevance | Document Link | Specification Link |
|-----------|----------|-----------|---------------|--------------------|
| Decomposition | `test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md` | PKG-10 scope (§5); DEL-10.02 definition; objective mapping (§6: OBJ-1, OBJ-2, OBJ-4, OBJ-7) | All sections; bidirectional link | Specification.md §Scope (scope definition) |
| Employer's Requirements Vol 2 Pt 1 | `test/Volume_2_Part_1_Employers_Requirements.pdf` | Performance/material requirements (**TBD** clauses — to be identified in Procedure.md Step 2) | Procedure.md Step 2 (ER clause identification) | Specification.md §Requirements (ER requirements drive specifications) |
| Employer's Requirements Vol 2 Pt 2 | `test/Volume_2_Part_2_Employers_Requirements.pdf` | Technical requirements (**TBD** clauses — standards, codes, technical criteria) | Procedure.md Step 2 (ER clause identification) | Specification.md §Standards (applicable standards from ER) |
| Employer's Requirements Vol 2 Pt 3 | `test/Volume_2_Part_3_Employers_Requirements.pdf` | Quality/workmanship requirements (**TBD** clauses — QA/QC, testing, documentation) | Procedure.md Step 2 (ER clause identification) | Specification.md WK-xx (workmanship requirements from ER) |
| DEL-10.01 | `execution/PKG-10_Railcar_Unloading_System/1_Working/DEL-10.01_*/` | Design Drawing Set (equipment arrangement, layout, interfaces) — drawings show physical implementation of requirements specified in this document | All sections (specifications drive drawing content; drawings show physical arrangement) | Specification.md §Scope (drawings reference) |
| DEL-10.03 | `execution/PKG-10_Railcar_Unloading_System/1_Working/DEL-10.03_*/` | Design Calculations (sizing basis, performance verification) — calculations provide sizing and capacity basis for specifications | §Construction (calculations support specification requirements) | Specification.md PF-01, PF-03, PF-04 (performance requirements verified by calculations) |
| DEL-10.04 | `execution/PKG-10_Railcar_Unloading_System/1_Working/DEL-10.04_*/` | Data Sheet Package (equipment specifications, vendor data) — data sheets implement this technical specification for specific equipment items | §Construction (data sheets implement specifications for individual equipment) | Specification.md FN-01 (scope elements detailed in data sheets) |
| DEL-10.05 | `execution/PKG-10_Railcar_Unloading_System/1_Working/DEL-10.05_*/` | Installation & Test Records (verification of compliance) — installation and test records demonstrate compliance with workmanship and testing requirements | §Construction (installation and testing per specifications) | Specification.md WK-04 (testing requirements verified in DEL-10.05) |
| Specification.md | This deliverable folder | Requirements for this deliverable (functional, performance, material, workmanship, interface, quality requirements) | All sections; bidirectional link | — |
| Guidance.md | This deliverable folder | Design intent, principles, considerations, trade-offs | All sections; bidirectional link | — |
| Procedure.md | This deliverable folder | Production workflow, ER clause identification, review/approval process | All sections; bidirectional link | — |
| _DEPENDENCIES.md | This deliverable folder | NOT_TRACKED — dependencies coordinated externally per project schedule | Procedure.md §Prerequisites (dependency tracking mode) | — |

**Note:** Specific Employer's Requirements clause references to be populated during specification development (Procedure.md Step 2 — ER clause identification). Compliance matrix will map all ER clauses to specification sections.

**Pass 3 Verification:** All references bidirectionally linked; all TBDs marked and sourced; all ASSUMPTIONs and PROPOSALs labeled; cross-references to all related PKG-10 deliverables verified.
