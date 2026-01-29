# Guidance: DEL-05.01 Concrete Structures Design Drawing Set

## Purpose

- Guide production of the **Concrete Structures Design Drawing Set** so it expresses the intended arrangement and details for concrete works in PKG-05. (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:232.)
- Emphasize drawing clarity for containment-related features and interfaces that support storage capacity (OBJ-3: 45,000 MT) and environmental protection (OBJ-7) objectives. (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:782; test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:786; test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:41-42.)
- Ensure drawings facilitate safe, efficient construction and provide clear verification points for QA/QC inspection. (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:58.)

## Principles

**P-01: Scope Fidelity**
Keep drawings aligned to PKG-05 scope (foundations, containment walls, equipment pads, thrust blocks, ground liner system); avoid adding unrelated building/MEP details. Clearly identify scope boundaries and interfaces with adjacent packages (PKG-08 Marine, PKG-21 Buildings). (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:226; Specification.md: Scope.)

**P-02: Containment Clarity (Environmental Protection Focus)**
Where concrete elements form part of secondary containment or support liner systems, detail joints/penetrations/interfaces clearly to reduce environmental risk and rework:
- Tank farm containment walls must clearly show joint details, waterstops, and liner interfaces
- Penetrations through containment walls must be sealed and detailed to prevent leakage pathways
- Construction notes should emphasize quality control for containment performance (relates to OBJ-7)
- Detail typical joints (construction, control, expansion) to ensure consistency and quality
(Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:786; test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:226; Specification.md: PR-02.)

**P-03: Traceability to Design Basis**
Reinforcement presentation and general notes should be consistent with:
- DEL-05.02 (Technical Specification) — concrete materials, reinforcement specifications, quality requirements
- DEL-05.03 (Design Calculations) — foundation sizing, wall design, seismic analysis, bearing capacity
- As these deliverables mature, ensure drawing notes reflect calculation results and specification requirements
(Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:233; test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:234; Specification.md: QR-03.)

**P-04: Evidence-Based Code Reference**
Do not assert governing codes/clauses unless sourced from Employer's Requirements or an accessible referenced standard; otherwise flag as **TBD**. When codes are confirmed:
- Reference specific code sections in drawing notes (e.g., "per CSA A23.3 Cl. X.X")
- Note code-driven requirements clearly (e.g., seismic detailing, exposure class requirements)
- Ensure code references are consistent across all drawings and with Specification Standards section
(Source: test/Volume_2_Part_1_Employers_Requirements.pdf, location TBD; test/Volume_2_Part_2_Employers_Requirements.pdf, location TBD; Specification.md: Standards.)

**P-05: Interface Visibility**
Explicitly identify interfaces and coordination requirements:
- Embedded items for other disciplines (anchor bolts, sleeves, blockouts)
- Hold points for interface verification before concrete placement
- Coordination notes referencing other discipline drawings
- Interface elevations and connection details
- This supports safe, coordinated construction and reduces RFIs/rework
(Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:49; Specification.md: IR-02; Datasheet.md: Construction.)

## Considerations

**C-01: Required Inputs (Dependencies Coordinated Externally)**
The following inputs affect foundations and pads (dependencies coordinated externally per NOT_TRACKED mode — see `_DEPENDENCIES.md`):
- **Geotechnical parameters:** Bearing capacity, settlement tolerances, soil properties, groundwater levels (from PKG-02 geotechnical reports)
- **Equipment loads:** Dead loads, live loads, operating loads, seismic loads (from PKG-10, PKG-11, PKG-13, PKG-15 equipment vendors/designers)
- **Tank interface loads:** Tank nozzle loads, anchor bolt loads, settlement tolerances (from PKG-13 storage tank design)
- **Piping support loads:** Pipe support locations and loads, thrust block requirements (from PKG-14 piping design)
- **Underground utility constraints:** Clash avoidance with drainage, duct banks, underground piping (from PKG-03)
- **Building foundation interfaces:** Control room, pump house, and other building foundations (from PKG-21/PKG-22)

**Coordination strategy:** Hold layout freeze points until critical inputs are received. Document assumptions clearly when inputs are not yet available. Maintain assumption register and update drawings when inputs are confirmed. (Source: `_DEPENDENCIES.md`; test/execution/_Coordination/_COORDINATION.md; Procedure.md: Prerequisites.)

**C-02: Constructability**
Ensure reinforcement congestion, pour sequencing, and formwork access are considered in detailing:
- **Reinforcement congestion:** Minimize congestion at beam-column joints, wall intersections, and dense anchor bolt layouts through careful detailing and sequencing
- **Pour sequencing:** Note critical pour sequences on drawings (e.g., foundation base before walls, construction joint locations)
- **Formwork access:** Ensure formwork can be installed and removed safely; note where special formwork or construction sequencing is required
- **Construction joints:** Locate construction joints for structural and construction efficiency; detail shear keys, dowels, or surface preparation as required
- **Cold weather / hot weather:** Consider seasonal construction constraints for BC location (freeze-thaw exposure, curing requirements)

**ASSUMPTION:** Standard constructability considerations for concrete drawings; specific project constraints TBD from Employer's Requirements and Contractor's construction plan. (Source: Specification.md: PR-03.)

**C-03: Durability and Exposure**
Confirm concrete durability requirements from Employer's Requirements and reflect them in notes/details:
- **Exposure classes:** Freeze-thaw exposure (likely for BC location), de-icing salts (if applicable), sulfates (from soil), chlorides (marine environment proximity)
- **Cover requirements:** Minimum cover by exposure zone and structural element type
- **Water-cement ratio limits:** Durability-driven w/c ratio limits by exposure class
- **Air entrainment:** Air content requirements for freeze-thaw protection
- **Concrete strength:** Compressive strength by element type and exposure class
- **Curing requirements:** Curing duration and methods by exposure class

**TBD:** Specific exposure class assignments and durability requirements from Employer's Requirements Volume 2 Part 2 concrete section. (Source: test/Volume_2_Part_2_Employers_Requirements.pdf, location TBD; Datasheet.md: Conditions; Specification.md: PR-01.)

**C-04: Interface Identification**
Explicitly call out sleeves, blockouts, embeds, and interface hold points for other disciplines:
- **Electrical:** Conduit sleeves through foundations and walls (PKG-17)
- **Piping:** Pipe sleeves through containment walls, thrust block interfaces (PKG-14)
- **Instrumentation:** Instrument penetrations and mounting provisions (PKG-20)
- **Equipment:** Anchor bolt embedments, grout pockets, equipment mounting interfaces (PKG-10, PKG-11, PKG-13, PKG-15)
- **Drainage:** Drainage penetrations through containment walls, sumps (PKG-03)
- **Marine:** Interface with marine structures if applicable (PKG-08)

**TBD:** Complete interface list and coordination matrix pending interdisciplinary coordination (IDC) inputs. (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:49; Specification.md: IR-01; Specification.md: IR-02.)

**C-05: Seismic Considerations**
Concrete structures must be designed and detailed for seismic loads appropriate to BC location:
- **Seismic design parameters:** Seismic zone, site class, importance factors, R values (**TBD** from design basis)
- **Detailing requirements:** Seismic detailing for ductile behavior (confinement, lap splices, anchorage)
- **Foundation performance:** Allowable settlement and differential settlement under seismic loads
- **Containment integrity:** Ensure containment walls maintain integrity under seismic loads (critical for OBJ-7)

**TBD:** Specific seismic design parameters and detailing requirements from Employer's Requirements and applicable seismic code. (Source: Datasheet.md: Conditions; Specification.md: PR-01.)

## Trade-offs

**T-01: Detail Level vs Schedule**
Adding more typical details reduces RFIs and improves construction quality but increases drafting effort and review duration:
- **Approach:** Use a drawing list/typical details strategy to balance detail and efficiency
- **Recommendation:** Develop comprehensive typical details for repetitive elements (standard joints, standard embedments, standard reinforcement) and reference them on layout drawings
- **ASSUMPTION:** This is standard structural drawing practice; specific project drafting standards TBD

**T-02: Optimization vs Standardization**
Standardized details aid repeatability and construction efficiency, but site-specific loads/settlement may require bespoke elements:
- **Approach:** Use standardized details where conditions are similar (equipment pads, typical foundations) and custom details where required (tank foundations, containment walls)
- **Consideration:** Balance between optimization (cost, material efficiency) and standardization (construction efficiency, quality control)
- **TBD:** Specific optimization opportunities until design basis and loads are confirmed

**T-03: Concrete Thickness/Cover Decisions vs Constructability**
Durability-driven cover requirements may increase section sizes and reinforcement congestion:
- **Issue:** Higher exposure classes require greater cover, which increases section thickness and may create reinforcement congestion
- **Consideration:** Balance durability requirements (long-term performance) with constructability (reinforcement placement, concrete consolidation)
- **Mitigation:** Use larger bar spacing, reduce bar sizes, or increase section dimensions where congestion is unavoidable
- **TBD:** Specific cover and exposure requirements from Employer's Requirements concrete section

**T-04: Design Maturity vs Drawing Issue Timing**
Early drawing issue supports construction schedule but may require revisions as design basis matures:
- **Issue:** Drawings issued before design calculations are complete may require significant revisions
- **Consideration:** Balance early issue (support procurement, early construction) with design maturity (reduce revisions, avoid rework)
- **Approach:** Issue drawings in stages aligned with design maturity (e.g., foundation drawings before wall drawings, preliminary drawings before final)
- **Coordination:** Align drawing issue with DEL-05.02 (Technical Specification) and DEL-05.03 (Design Calculations) maturity

## Examples

**E-01: Suggested Sheet Grouping (Example Only; TBD per Project Drafting Standards)**
- **General sheets:** Drawing list, general notes, legend, abbreviations, typical details index
- **Foundation sheets:** Tank foundation plans, equipment pad foundation plans, building foundation plans, thrust block layouts, foundation sections and details
- **Containment wall sheets:** Containment wall plans, wall sections, joint details, waterstop details, liner interface details, penetration details
- **Reinforcement sheets:** Reinforcement plans by area/element, bar bending schedules, reinforcement sections and details
- **Typical details sheets:** Typical joint details, typical embedment details, typical reinforcement details

**ASSUMPTION:** Typical structural concrete drawing set organization; specific project organization TBD. (Source: Datasheet.md: Construction.)

**E-02: Drawing Content Example — Tank Foundation Plan**
A tank foundation plan drawing should show:
- Foundation layout with tank centerlines and anchor bolt circle
- Foundation dimensions (diameter, thickness, edge details)
- Elevation datum and finished floor elevations
- Reinforcement callouts (reference to bar bending schedule)
- Anchor bolt layout (coordinate with PKG-13 tank design)
- Interface notes (liner termination, drainage, grounding)
- General notes (concrete strength, cover, curing, pour sequence)
- Section cut lines referencing foundation sections

**E-03: Drawing Content Example — Containment Wall Section**
A containment wall section drawing should show:
- Wall height, thickness, and length
- Foundation connection detail
- Joint details at regular intervals (construction joints, control joints)
- Waterstop details at joints (coordinate with ground liner)
- Reinforcement callouts (vertical, horizontal, at joints)
- Penetration sleeves and sealing details
- Liner termination and attachment details
- General notes (concrete exposure class, cover, joint spacing, curing)

## Conflict Table (for human ruling)

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority | Human Ruling |
|-------------|----------|----------|----------|-------------------|-------------------|--------------|
| — | No conflicts identified from accessible sources | — | — | — | — | — |

**Note:** Employer's Requirements clause extraction pending for final verification. If conflicts are identified during ER review, they should be added to this table for human ruling. Key areas requiring ER confirmation:
- Design codes and standards (CSA A23.1/A23.3 assumed for BC location — **ASSUMPTION**)
- Seismic design parameters (site class, importance factors, R values — **TBD**)
- Exposure class assignments (freeze-thaw, sulfates, chlorides — **TBD**)
- Document control and QA/QC requirements (drawing numbering, checking process — **TBD**)

(Source: test/Volume_2_Part_2_Employers_Requirements.pdf, location TBD.)

## Guidance-to-Specification Traceability

| Guidance § | Supporting Specification Requirements |
|------------|---------------------------------------|
| P-01 Scope Fidelity | FR-01 Artifact Coverage, Scope section |
| P-02 Containment Clarity | FR-03 Containment Wall Details, PR-02 Containment Performance |
| P-03 Traceability to Design Basis | QR-03 Technical Consistency, PR-01 Design Basis Alignment |
| P-04 Evidence-Based Code Reference | Standards section, QR-01 Document Control |
| P-05 Interface Visibility | IR-02 Interface Identification, FR-04 Equipment Pad Details |
| C-01 Required Inputs | IR-01 Dependency Coordination, Prerequisites |
| C-02 Constructability | PR-03 Constructability, FR-05 Reinforcement Presentation |
| C-03 Durability and Exposure | PR-01 Design Basis Alignment |
| C-04 Interface Identification | IR-01, IR-02 Interface Requirements |
| C-05 Seismic Considerations | PR-01 Design Basis Alignment |
| T-01 through T-04 | Trade-offs inform engineering judgment within requirements |
| E-01 through E-03 | Examples support FR-01 through FR-06 implementation |

## Cross-Document Notes

- **Specification:** Use `Specification.md` as the checklist for what must be present and how it will be verified. Each Principle (§P-01 through §P-05) and Consideration (§C-01 through §C-05) supports corresponding Specification requirements per the Guidance-to-Specification Traceability table above. (Source: Specification.md: Requirements; Specification.md: Requirements Traceability Matrix.)
- **Procedure:** `Procedure.md` describes how to develop/check/release the drawing set (Steps 1-7) and what evidence is retained (§Records). Considerations §C-01 through §C-05 are addressed in `Procedure.md` §P-01 Prerequisites and Steps 2-4. (Source: Procedure.md: Prerequisites; Procedure.md: Steps; Procedure.md: Records.)
- **Datasheet:** `Datasheet.md` §Construction lists the anticipated artifacts that Principles §P-01 through §P-05 and Considerations §C-01 through §C-05 guide. Ensure drawing content aligns with §Construction breakdown. (Source: Datasheet.md: Construction; Datasheet.md: Cross-Document Traceability.)
