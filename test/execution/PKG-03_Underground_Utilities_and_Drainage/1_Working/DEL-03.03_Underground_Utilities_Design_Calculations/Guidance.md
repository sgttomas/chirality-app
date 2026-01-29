# Guidance: DEL-03.03 Underground Utilities Design Calculations

## Purpose

Provide decision-making context and engineering rationale for developing the Underground Utilities Design Calculations package for PKG-03, ensuring that storm drainage hydraulics, OWS sizing, duct bank capacity analysis, and trenchless crossing structural calculations reflect project objectives and support downstream design deliverables (DEL-03.01 Drawing Set and DEL-03.02 Technical Specification).

**Why this deliverable matters:**
- Calculations provide the quantitative engineering basis that validates design decisions documented in drawings and specifications; without rigorous calculations, design claims cannot be verified and regulatory approval may be jeopardized (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:210).
- Environmental protection calculations (OWS sizing, drainage capacity) directly support **OBJ-7 Environmental Protection** by demonstrating containment and treatment adequacy; calculation conservatism and clarity affect permitting outcomes and regulatory compliance verification (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:786; Specification §FR-2 environmental protection performance verification requirement).
- Calculation documentation creates permanent engineering record for future design modifications, troubleshooting, and operations; clear methodology and assumptions documentation enables future engineers to understand design basis and make informed changes (rationale for Specification §QR-2 calculation methodology documentation requirement; supports Datasheet §Conditions operational context).

## Principles

**P-1: Hydraulic Performance and Capacity Verification**
- Storm drainage calculations must demonstrate that pipe network can convey design storm runoff without surcharging or flooding critical areas; hydraulic grade line analysis verifies adequate freeboard and prevents system overtopping.
- **Application:** Develop runoff calculations using rational method or hydrograph analysis appropriate to drainage area size and time of concentration; size pipes to maintain velocities within acceptable range (minimum velocity for self-cleaning, maximum velocity to prevent erosion); verify hydraulic grade lines remain below ground surface or inlet elevations; confirm outfall discharge rates comply with municipal limits or environmental permits.
- **Rationale:** Undersized drainage systems cause operational flooding, property damage, and environmental contamination from runoff bypassing treatment systems; oversized systems waste capital and increase excavation/construction costs; hydraulic grade line analysis identifies bottlenecks and verifies adequate capacity margins (supports Specification §FR-1 comprehensive hydraulic analysis requirement and §PR-1 hydraulic performance requirement).
- **Cross-reference:** Datasheet §Construction storm drainage calculations content describes runoff calculation, pipe sizing, hydraulic grade line analysis; Procedure §4.1 implements storm drainage calculation development; Specification §FR-1 and §PR-1 establish hydraulic performance requirements.

**P-2: Environmental Protection Performance Verification**
- OWS sizing calculations must demonstrate separator capacity to treat peak runoff flows, provide adequate retention time for oil separation and solids settling, and meet discharge water quality limits to support **OBJ-7 Environmental Protection**.
- **Application:** Determine contributing drainage area from site layout and flow path analysis; calculate peak runoff using rational method or hydrograph appropriate to drainage area characteristics; size separator volume for oil storage capacity, solids settling volume, and water retention volume based on treatment performance targets; verify retention time meets minimum duration for oil/water separation efficiency; confirm discharge rate and quality comply with environmental permit limits.
- **Rationale:** Undersized OWS leads to treatment bypass, environmental permit violations, and potential facility shutdown; oversized OWS increases capital cost and footprint without commensurate environmental benefit; retention time verification ensures separator achieves target oil removal efficiency under peak flow conditions; discharge limit confirmation demonstrates regulatory compliance (supports Specification §FR-2 environmental protection performance verification requirement and §PR-2 facility throughput and containment support).
- **Cross-reference:** Datasheet §Construction OWS sizing content describes contributing area, peak flow, separator volume, retention time calculations; Procedure §4.2 and §5 implement OWS sizing and environmental protection calculations; Specification §FR-2 and §PR-2 establish environmental protection requirements; Example 2 below provides OWS sizing methodology guidance.

**P-3: Calculation Assumptions and Data Source Traceability**
- All calculation inputs, assumptions, and data sources must be explicitly documented with references to source documents, data extraction dates, and assumption justifications to support independent verification and future design modifications.
- **Application:** Calculation input summary shall identify all design criteria sources (civil design brief, Employer's Requirements Volume 2 Part 2, geotechnical report, site survey, rainfall IDF curves) with document IDs, revision numbers, and data extraction dates; document all assumptions (runoff coefficients, pipe roughness values, soil properties, load factors) with justification or reference to applicable standards; flag conservative assumptions taken due to data uncertainty and identify future validation requirements.
- **Rationale:** Undocumented assumptions create verification difficulties, increase review time, and may lead to design errors if assumptions are not validated; missing data source references prevent traceability and make future updates difficult when design criteria change; clear assumption documentation enables reviewers to assess calculation conservatism and identify areas requiring validation (supports Specification §QR-2 calculation methodology documentation requirement).
- **Cross-reference:** Datasheet §Attributes "Design Criteria Sources" and §Construction input data summary content; Procedure §2.2 input data collection and §4.5 methodology documentation; Specification §QR-2 methodology documentation requirement; Consideration C-1 and C-2 below address design criteria availability and ER extraction.

**P-4: Coordination with Design Drawings and Specifications**
- Calculation results (pipe sizes, slopes, hydraulic parameters, OWS capacity, duct bank configuration, structural capacities) must align with design drawings (DEL-03.01) and specifications (DEL-03.02) to ensure consistency across deliverables and enable construction without conflicts.
- **Application:** Review DEL-03.01 Drawing Set for pipe alignments, invert elevations, slopes, OWS location, duct bank routing before finalizing calculations; verify calculation pipe sizes and slopes match drawing annotations; cross-reference calculation OWS capacity to drawing capacity annotations and DEL-03.04 data sheet equipment specifications; coordinate duct bank fill factor calculations with PKG-17 electrical cable schedules; update drawings and specifications when calculation results change during design iterations.
- **Rationale:** Inconsistencies between calculations, drawings, and specifications create construction conflicts, increase RFI volume, delay construction, and may lead to field redesign; early coordination prevents rework and ensures all deliverables reflect same design basis; calculation-drawing-specification alignment is critical checkpoint during design review (supports Specification §IF-1 coordination with related deliverables requirement).
- **Cross-reference:** Datasheet §References lists DEL-03.01/02/04 linkages; Procedure §2.1 input data collection from related deliverables and §7.2 interdisciplinary coordination check; Specification §IF-1 coordination with related deliverables; Consideration C-4 below addresses QA coordination.

## Considerations

**C-1: Design Criteria Availability and Data Gaps**
- Design calculations require multiple input data sources (civil design brief, geotechnical report, Employer's Requirements, rainfall IDF curves, site survey); data availability varies during design development phases; calculations may proceed with conservative assumptions when data is incomplete, but assumptions must be flagged for future validation.
- **Impact on deliverable:** Initial calculations may use conservative assumptions (higher rainfall intensities, lower soil bearing capacities, increased load factors) when civil design brief or geotechnical data is not finalized; calculation revisions will be required when actual design criteria become available; assumption tracking in calculation notes enables efficient revision when data gaps are closed.
- **Recommended approach:** Identify all required input data during calculation planning (Procedure §Prerequisites); obtain available data from approved sources; document conservative assumptions for missing data with justification and future validation requirements; flag calculations requiring revision when specific data becomes available; coordinate with design team to prioritize data acquisition for critical design decisions.
- **Cross-reference:** Specification §PR-3 design life and environmental conditions (lists design parameters as TBD from ER and civil design brief); Principle P-3 calculation assumptions and data source traceability; Procedure §2.2 input data collection (identifies data sources and collection process).

**C-2: Employer's Requirements Extraction and Interpretation**
- Employer's Requirements Volume 2 Part 2 contains civil design criteria, storm drainage standards, OWS performance requirements, structural loading criteria; specific clauses and values must be extracted and interpreted for calculation inputs; extraction requires engineering judgment to identify applicable requirements and resolve ambiguities.
- **Impact on deliverable:** Design storm return period, hydraulic capacity factors, OWS treatment efficiency targets, structural load factors, seismic design parameters are TBD pending ER extraction; calculation methodology may vary depending on ER requirements (e.g., rational method vs hydrograph analysis for runoff calculation); ER interpretation affects calculation conservatism and compliance demonstration.
- **Recommended approach:** Review ER Volume 2 Part 2 civil sections during calculation planning; extract applicable design criteria and document in calculation input summary with ER clause references; clarify ambiguous requirements with Employer or design team; use conservative interpretation when requirements allow multiple approaches; document interpretation rationale in calculation notes.
- **Cross-reference:** Specification §Standards governing standards (ER Volume 2 Part 2 is authoritative source); Datasheet §Conditions and §Attributes list design criteria as TBD from ER; Principle P-3 emphasizes data source traceability; Procedure §Prerequisites lists ER as required reference material.

**C-3: Calculation Structure and Scope Boundaries**
- Calculation package scope must align with DEL-03.03 decomposition scope (storm drainage, OWS, duct banks, trenchless crossings for PKG-03); avoid scope creep into adjacent package calculations (e.g., detailed electrical cable sizing in PKG-17, process piping hydraulics in PKG-14, building foundation design in PKG-05).
- **Impact on deliverable:** Clear scope boundaries prevent duplication of effort and maintain traceability to decomposition; duct bank calculations verify conduit capacity only (fill factors, spacing) while detailed electrical cable sizing is in PKG-17; calculation organization structure (sections matching anticipated artifacts per Specification §Scope) supports scope control.
- **Recommended approach:** Review decomposition scope and anticipated artifacts during calculation planning (Procedure §1 scope review); organize calculation package into sections matching Specification §Scope anticipated calculation types; identify interface calculations requiring coordination with adjacent packages (e.g., duct bank fill factors coordinate with PKG-17 cable schedules); document scope boundaries and coordination requirements in calculation introduction.
- **Cross-reference:** Specification §Scope lists anticipated calculation types and exclusions; Datasheet §Construction calculation package organization structure; Procedure §3.2 establish calculation section structure; Trade-off T-4 addresses duct bank calculation coordination with PKG-17.

**C-4: QA Sign-offs and Coordination with Installation Records**
- Calculation review and approval (preparer, checker, approver signatures per Specification §QR-1) creates traceable QA record; calculation results and margins inform installation testing and commissioning documented in DEL-03.05 Installation and Test Records; coordination ensures test acceptance criteria align with design performance.
- **Impact on deliverable:** Calculation review signatures document that hydraulic performance, OWS sizing, structural capacities have been verified before construction; calculation margins (e.g., OWS retention time safety factor, trenchless crossing load factors) provide basis for installation tolerance acceptance; calculation results (design flows, pressures, capacities) become test targets for commissioning.
- **Recommended approach:** Follow calculation review workflow per Procedure §Verification (self-check, interdisciplinary check, independent check); document review comments and resolutions in calculation review log; coordinate with DEL-03.05 development team to ensure test procedures reflect calculation performance targets and acceptance margins; provide calculation summary table for test procedure reference.
- **Cross-reference:** Specification §Verification describes review process; Specification §QR-1 compliance with Quality Management Plan; Specification §IF-1 coordination with DEL-03.05; Principle P-4 coordination with design deliverables; Procedure §7 verification activities and §Records QA documentation.

**C-5: Engineering Record and Future Reference**
- Calculation package serves as permanent engineering record documenting design basis, methodology, and performance verification; future design modifications, troubleshooting, and operations maintenance decisions rely on calculation documentation; clear methodology and assumptions enable future engineers to understand design rationale and make informed changes.
- **Impact on deliverable:** Calculation methodology documentation (Specification §QR-2) must balance sufficient detail for verification with clarity for future reference; calculation organization and summary tables should enable quick review of key results without requiring detailed review of all analysis steps; calculation appendices (software output files, manufacturer data) preserve supporting information for future validation.
- **Recommended approach:** Structure calculation package with executive summary table showing key results (pipe sizes, flows, capacities, margins); document methodology clearly with governing equations, standards references, and software tools identified; include calculation flowchart or methodology overview for complex analyses; preserve software model files and output reports in calculation appendices; issue calculation package into document control system for archival and future retrieval (Procedure §8).
- **Cross-reference:** Specification §QR-2 calculation methodology documentation; Datasheet §Conditions operational context (permanent record for operations and future modifications); Principle P-3 calculation assumptions and data source traceability; Procedure §Records calculation deliverables preservation.

## Trade-offs

**T-1: Calculation Detail vs Conservative Assumptions**
- **Trade-off:** Detailed calculations with refined input data and rigorous analysis methods increase accuracy and may reduce conservatism, but require more time and data; conservative assumptions and simplified methods enable faster calculation with adequate safety margins, but may result in oversized systems and increased capital cost.
- **Considerations:**
  - Detailed hydraulic modeling (e.g., HEC-RAS dynamic routing) vs simplified rational method for runoff calculation; detailed modeling improves accuracy for large drainage areas or complex flow paths but requires more time and software validation.
  - Refined OWS sizing with computational fluid dynamics (CFD) analysis vs empirical sizing equations; CFD may optimize separator volume but requires specialized expertise and longer analysis time.
  - When design criteria data is uncertain (e.g., soil properties pending geotechnical investigation), conservative assumptions enable calculation to proceed while design development continues; calculation revision required when refined data becomes available.
- **Recommended approach:** Use simplified methods with conservative assumptions for initial design calculations to support early drawing and specification development; refine calculations with detailed analysis when design criteria data becomes available and design is maturing for construction issue; document assumption conservatism in calculation notes to inform future refinement decisions; coordinate calculation detail level with project schedule and design phase requirements.
- **Cross-reference:** Consideration C-1 design criteria availability and data gaps; Principle P-3 calculation assumptions documentation; Specification §PR-1 and §PR-2 performance requirements establish adequacy criteria regardless of calculation method.

**T-2: OWS Sizing Methodology Selection**
- **Trade-off:** OWS sizing methodology selection affects separator volume, footprint, and capital cost; empirical sizing equations (e.g., API separator sizing) are simple and widely accepted, but conservative; detailed analysis (CFD, pilot testing) may optimize volume but requires more time and expense.
- **Considerations:**
  - Empirical sizing equations are code-compliant and widely used for typical oil-water separation applications; conservative sizing provides safety margin for flow variability and ensures regulatory compliance.
  - Detailed CFD analysis or pilot testing may reduce separator volume by 20-30% compared to empirical sizing, reducing capital cost and footprint; analysis cost and schedule impact must be weighed against capital savings.
  - Environmental permit requirements may specify minimum retention time or treatment performance regardless of sizing methodology; permit compliance is non-negotiable and affects methodology selection.
- **Recommended approach:** Use empirical sizing equations (API separator sizing or equivalent) for initial OWS sizing to support drawing layout and early cost estimates; evaluate detailed analysis only if separator footprint or cost is critical constraint; ensure sizing methodology demonstrates compliance with environmental permit requirements; document methodology selection rationale in calculation notes.
- **Cross-reference:** Principle P-2 environmental protection performance verification; Specification §FR-2 environmental protection performance verification requirement; Example 2 below provides OWS sizing methodology guidance.

**T-3: Trenchless Crossing Calculation Conservatism**
- **Trade-off:** Trenchless crossing structural calculations involve uncertainty in boring conditions (soil properties, groundwater, obstructions); conservative load factors and assumptions increase structural capacity margins but may require larger/heavier casing pipes and increase cost; refined analysis with detailed geotechnical data may optimize design but requires more investigation and analysis time.
- **Considerations:**
  - Boring conditions are difficult to predict accurately; soil variability, unexpected obstructions, and groundwater fluctuations create uncertainty in earth pressure and jacking force predictions.
  - Conservative assumptions (higher earth pressure coefficients, increased surcharge loads, reduced soil strength) provide safety margin for boring uncertainty; conservatism increases casing pipe size and wall thickness, affecting cost.
  - Detailed geotechnical investigation along crossing alignment may reduce uncertainty and enable refined analysis; investigation cost and schedule impact must be weighed against structural cost savings.
- **Recommended approach:** Use conservative load factors and soil strength assumptions for initial trenchless crossing structural calculations given boring condition uncertainty; document conservatism in calculation notes; evaluate detailed geotechnical investigation for critical or expensive crossings where refined analysis may yield significant cost savings; coordinate with geotechnical engineer on boring condition assumptions.
- **Cross-reference:** Principle P-1 structural performance verification; Specification §PR-1 structural performance requirement; Datasheet §Construction trenchless crossing calculations content; Example 4 below provides crossing structural analysis guidance.

**T-4: Duct Bank Capacity Analysis Coordination with Electrical**
- **Trade-off:** Duct bank capacity calculations overlap with PKG-17 electrical cable sizing analysis; civil duct bank calculations verify conduit fill factors and physical capacity, while electrical calculations determine cable sizes and loading; coordination boundary and calculation responsibility must be clearly defined to avoid duplication or gaps.
- **Considerations:**
  - Conduit fill factor requirements are defined by electrical codes (e.g., NEC/CEC conduit fill tables); civil duct bank calculations verify conduit sizes accommodate electrical cable schedules from PKG-17 within fill factor limits.
  - Electrical cable sizing and loading calculations (voltage drop, ampacity, short circuit) are PKG-17 responsibility; civil calculations assume cable schedules from PKG-17 as input.
  - Pull box spacing calculations depend on cable pulling tension limits; coordination with PKG-17 required to establish pulling tension criteria.
- **Recommended approach:** Civil duct bank calculations verify conduit fill factors using cable schedules from PKG-17 as input; verify conduit spacing, trench width, and pull box locations based on civil constructability and utility separation requirements; coordinate with PKG-17 for cable schedule input data and pulling tension criteria; document coordination boundary in calculation notes; cross-reference PKG-17 deliverables for detailed electrical analysis.
- **Cross-reference:** Principle P-4 coordination with design deliverables; Specification §FR-3 coordination with electrical infrastructure; Specification §IF-2 coordination with PKG-17; Consideration C-3 calculation scope boundaries; Example 3 below provides duct bank capacity analysis guidance.

## Examples

**Example 1: Storm Drainage Hydraulic Calculation Structure**

**Scenario:** Develop hydraulic calculations for storm drainage network serving facility roadways and paved areas; demonstrate compliance with design storm event and verify pipe capacities.

**Recommended calculation structure:**
1. **Input data summary:** Design storm return period (TBD from ER Volume 2 Part 2, assume 25-year for initial calculation); rainfall IDF curves (source: Metro Vancouver or local jurisdiction); runoff coefficients (source: civil design standards for pavement, landscaped areas); pipe roughness coefficients (Manning's n values from pipe material specifications in DEL-03.02); site grading and drainage area delineation (from DEL-03.01 Drawing Set and PKG-02 site grading plans).

2. **Drainage area delineation:** Identify contributing drainage areas for each inlet/catch basin; calculate drainage area sizes; determine flow paths and time of concentration; document drainage area assumptions and sketches.

3. **Runoff calculation:** Apply rational method (Q = CiA) for drainage areas < 80 hectares; calculate peak runoff for each inlet based on rainfall intensity for time of concentration, runoff coefficient, and drainage area; summarize results in runoff calculation table.

4. **Pipe sizing and hydraulic analysis:** Size storm drain pipes for calculated flows; verify pipe velocities within acceptable range (minimum 0.6 m/s for self-cleaning, maximum 3-5 m/s to prevent erosion); develop hydraulic grade line analysis using hydraulic modeling software (e.g., StormCAD) or step-backwater calculation method; verify hydraulic grade lines remain below inlet elevations and ground surface.

5. **Results summary table:** Tabulate pipe sizes, slopes, flows, velocities, hydraulic grade lines for each pipe segment; identify any capacity deficiencies or design revisions required; cross-reference drawing sheet numbers for each pipe segment.

6. **Appendices:** Include software model setup description, model output files, drainage area sketches, rainfall IDF curves reference.

**Application to DEL-03.03:** This calculation structure demonstrates hydraulic performance verification (Principle P-1) and provides traceable engineering basis for storm drainage design in DEL-03.01 Drawing Set and DEL-03.02 Technical Specification; calculation results (pipe sizes, slopes) must match drawing annotations per coordination requirement (Principle P-4).

**Cross-reference:** Datasheet §Construction storm drainage calculations content; Specification §FR-1 comprehensive hydraulic analysis; Procedure §4.1 develop storm drainage hydraulic calculations.

**Example 2: OWS Sizing Methodology**

**Scenario:** Size oil-water separator for facility drainage area subject to canola oil spills; demonstrate adequate treatment capacity, retention time, and discharge compliance to support OBJ-7 Environmental Protection.

**Recommended sizing methodology:**
1. **Contributing drainage area determination:** Identify paved areas and process areas draining to OWS; calculate contributing area size; determine runoff characteristics (runoff coefficient, time of concentration).

2. **Peak runoff flow rate calculation:** Calculate peak runoff using rational method for design storm event (TBD from ER Volume 2 Part 2 or environmental permit requirements); consider both rainfall runoff and potential process spill scenarios; use conservative assumption for peak flow (e.g., maximum of storm runoff or spill release rate).

3. **Separator volume sizing:** Apply empirical sizing equation (e.g., API separator sizing equation or manufacturer sizing guidelines) based on peak flow rate and target treatment performance; size separator for three volume components:
   - Oil storage volume: Capacity to store separated oil between maintenance intervals (assume oil layer thickness and maintenance frequency).
   - Solids settling volume: Capacity for sediment accumulation between cleaning intervals.
   - Water retention volume: Active treatment volume based on retention time requirement.

4. **Retention time verification:** Calculate retention time (separator volume / peak flow rate); verify retention time meets minimum duration for oil/water separation efficiency (typical minimum 10-20 minutes depending on oil characteristics and treatment target); adjust separator volume if retention time is insufficient.

5. **Discharge rate and quality limits confirmation:** Verify discharge rate complies with outfall capacity or environmental permit limits; confirm treatment performance (oil removal efficiency) meets discharge water quality limits (e.g., <15 mg/L oil & grease for typical environmental permits); document permit requirement references.

6. **Results summary:** Tabulate separator volume, retention time, treatment capacity, discharge rate/quality; cross-reference DEL-03.04 Data Sheet Package for equipment specifications; note any conservative assumptions requiring validation.

**Application to DEL-03.03:** This sizing methodology demonstrates environmental protection performance verification (Principle P-2) and supports OBJ-7 compliance; calculation results inform OWS layout in DEL-03.01 Drawing Set and performance requirements in DEL-03.02 Technical Specification.

**Cross-reference:** Datasheet §Construction OWS sizing content; Specification §FR-2 environmental protection performance verification; Procedure §4.2 develop OWS sizing calculations and §5 environmental protection calculations; Trade-off T-2 OWS sizing methodology selection.

**Example 3: Duct Bank Fill Factor Analysis**

**Scenario:** Verify duct bank conduit capacity for electrical cables; coordinate with PKG-17 cable schedules; demonstrate compliance with electrical code fill factor limits.

**Recommended analysis approach:**
1. **Conduit schedule input:** Obtain cable schedule from PKG-17 showing cable sizes (conductor size, insulation type, overall diameter), cable quantities, and conduit assignments; document PKG-17 deliverable reference and coordination date.

2. **Conduit fill area calculation:** For each conduit, calculate total cable cross-sectional area (sum of individual cable areas based on cable diameters from cable schedule or manufacturer data); calculate conduit internal area (based on conduit size from DEL-03.01 Drawing Set and conduit ID from manufacturer data).

3. **Fill factor verification:** Calculate fill factor (total cable area / conduit internal area); verify fill factor complies with electrical code limits (e.g., NEC/CEC Table 1 allows 40% fill for 3+ cables in conduit); identify any conduits exceeding fill limits requiring upsizing.

4. **Pull box spacing calculation:** Verify pull box spacing based on cable pulling tension limits (coordinate with PKG-17 for maximum pulling tension criteria); calculate cumulative pulling angles and straight lengths between pull boxes; verify pull box locations shown in DEL-03.01 Drawing Set comply with maximum spacing.

5. **Results summary table:** Tabulate conduit sizes, cable quantities, fill factors, pull box spacings; flag any fill factor exceedances or pull box spacing deficiencies; provide coordination notes for PKG-17 (e.g., "Conduit C-3 fill factor 45% exceeds 40% limit; upsize conduit to 100mm or reduce cable quantity").

**Application to DEL-03.03:** This analysis demonstrates coordination with electrical infrastructure (Principle P-4) and verifies duct bank capacity supports electrical system requirements; simplified fill factor check supplements detailed electrical cable analysis in PKG-17 (Trade-off T-4 coordination boundary).

**Cross-reference:** Datasheet §Construction duct bank capacity content; Specification §FR-3 coordination with electrical infrastructure; Specification §IF-2 coordination with PKG-17; Procedure §4.3 develop duct bank capacity calculations; Trade-off T-4 duct bank calculation coordination.

**Example 4: Trenchless Crossing Structural Analysis**

**Scenario:** Verify casing pipe structural capacity for trenchless crossing beneath existing roadway; demonstrate adequate strength for earth pressure, surcharge loading, and jacking forces.

**Recommended analysis approach:**
1. **Input data collection:** Obtain geotechnical parameters (soil unit weight, internal friction angle, cohesion) from geotechnical report; identify roadway surcharge load (vehicle load or pavement weight); determine crossing depth and length from DEL-03.01 Drawing Set; identify casing pipe size and material from DEL-03.02 Technical Specification.

2. **Earth pressure calculation:** Calculate vertical earth pressure on casing pipe (overburden soil pressure = soil unit weight × depth); apply surcharge load (roadway live load or pavement dead load); use conservative earth pressure coefficient (e.g., at-rest or increased value to account for boring disturbance).

3. **Casing pipe structural analysis:** Model casing pipe as beam on elastic foundation or use ring deflection analysis; apply earth pressure and surcharge loads; calculate bending moments, deflections, and stresses; verify against allowable limits per pipe material standard (e.g., ASTM steel pipe allowable stresses, deflection limits).

4. **Jacking force calculation:** Estimate jacking force based on pipe-soil friction (friction coefficient × normal force from earth pressure) and face resistance for boring method; verify jacking force within thrust capacity of jacking equipment and pipe crushing strength.

5. **Settlement and differential movement analysis:** Estimate settlement potential from soil consolidation or boring disturbance; verify carrier pipe support and annular space accommodate anticipated settlements without pipe overstress; document monitoring requirements if settlement risk is significant.

6. **Results summary:** Tabulate loading conditions, structural capacities, utilization ratios (actual/allowable); document conservatism in assumptions (e.g., "At-rest earth pressure coefficient 0.5 used; conservative compared to typical active pressure 0.3"); note any validation requirements (e.g., "Verify jacking force with boring contractor based on selected equipment").

**Application to DEL-03.03:** This analysis demonstrates structural performance verification (Principle P-1) with conservative assumptions appropriate for boring condition uncertainty (Trade-off T-3); calculation results support casing pipe selection in DEL-03.02 Technical Specification and crossing detail design in DEL-03.01 Drawing Set.

**Cross-reference:** Datasheet §Construction trenchless crossing calculations content; Specification §PR-1 structural performance requirement; Procedure §4.4 develop trenchless crossing structural calculations; Trade-off T-3 trenchless crossing calculation conservatism.

## Cross-Document Linkages

**Guidance ↔ Datasheet:**
- Guidance §Purpose "why this deliverable matters" → Datasheet §Conditions operational context (calculations validate design and support regulatory approval)
- Guidance §P-1 hydraulic performance and capacity verification → Datasheet §Construction storm drainage calculations content
- Guidance §P-2 environmental protection performance verification → Datasheet §Conditions OBJ-7 environmental protection emphasis + Datasheet §Construction OWS sizing content
- Guidance §P-3 calculation assumptions and data source traceability → Datasheet §Attributes "Design Criteria Sources" + Datasheet §Construction input data summary content
- Guidance §P-4 coordination with design drawings and specifications → Datasheet §References lists DEL-03.01/02/04/05 linkages
- Guidance §C-1 design criteria availability → Datasheet §Attributes and §Conditions list design criteria as TBD
- Guidance §C-3 calculation structure and scope boundaries → Datasheet §Construction calculation package organization structure
- Guidance §C-5 engineering record and future reference → Datasheet §Conditions operational context (permanent record for operations and future modifications)
- Guidance §Example 1 storm drainage calculation structure → Datasheet §Construction storm drainage calculations content
- Guidance §Example 2 OWS sizing methodology → Datasheet §Construction OWS sizing content
- Guidance §Example 3 duct bank fill factor analysis → Datasheet §Construction duct bank capacity content
- Guidance §Example 4 trenchless crossing structural analysis → Datasheet §Construction trenchless crossing calculations content

**Guidance ↔ Specification:**
- Guidance §P-1 hydraulic performance and capacity verification principle → Specification §FR-1 comprehensive hydraulic analysis requirement + §PR-1 hydraulic performance requirement
- Guidance §P-2 environmental protection performance verification principle → Specification §FR-2 environmental protection performance verification requirement + §PR-2 facility throughput and containment support
- Guidance §P-3 calculation assumptions and data source traceability principle → Specification §QR-2 calculation methodology documentation requirement
- Guidance §P-4 coordination with design drawings and specifications principle → Specification §IF-1 coordination with related deliverables
- Guidance §C-1 design criteria availability consideration → Specification §PR-3 design life and environmental conditions (lists parameters as TBD)
- Guidance §C-2 ER extraction and interpretation consideration → Specification §Standards governing standards (ER Volume 2 Part 2 as authoritative source)
- Guidance §C-3 calculation structure and scope boundaries consideration → Specification §Scope anticipated calculation types and exclusions
- Guidance §C-4 QA sign-offs and coordination with installation records → Specification §Verification design review process + §IF-1 coordination with DEL-03.05
- Guidance §C-5 engineering record and future reference consideration → Specification §QR-2 calculation methodology documentation requirement
- Guidance §T-1 calculation detail vs conservative assumptions trade-off → Specification §PR-1/PR-2 performance requirements (adequacy criteria regardless of method)
- Guidance §T-2 OWS sizing methodology selection trade-off → Specification §FR-2 environmental protection performance verification
- Guidance §T-3 trenchless crossing calculation conservatism trade-off → Specification §PR-1 structural performance requirement
- Guidance §T-4 duct bank calculation coordination trade-off → Specification §FR-3 coordination with electrical infrastructure + §IF-2 coordination with PKG-17

**Guidance ↔ Procedure:**
- Guidance §Purpose "why this deliverable matters" → Procedure §Purpose calculation production and QA purposes
- Guidance §P-1 hydraulic performance verification → Procedure §4.1 develop storm drainage hydraulic calculations
- Guidance §P-2 environmental protection performance verification → Procedure §4.2 develop OWS sizing calculations + §5 environmental protection calculations
- Guidance §P-3 calculation assumptions and data source traceability → Procedure §2.2 input data collection + §4.5 document calculation methodology
- Guidance §P-4 coordination with design drawings and specifications → Procedure §2.1 input data collection from related deliverables + §7.2 interdisciplinary coordination check
- Guidance §C-1 design criteria availability → Procedure §Prerequisites lists civil design brief, geotechnical report, ER as required references
- Guidance §C-2 ER extraction and interpretation → Procedure §Prerequisites lists ER Volume 2 Part 2 as required reference material
- Guidance §C-3 calculation structure and scope boundaries → Procedure §1 scope review + §3.2 establish calculation section structure
- Guidance §C-4 QA sign-offs and coordination with installation records → Procedure §Verification self-check/interdisciplinary/independent + §Records QA documentation
- Guidance §C-5 engineering record and future reference → Procedure §8 issue into document control system + §Records calculation deliverables preservation
- Guidance §Example 1 storm drainage calculation structure → Procedure §4.1 storm drainage calculation development steps
- Guidance §Example 2 OWS sizing methodology → Procedure §4.2 OWS sizing calculation development steps
- Guidance §Example 3 duct bank fill factor analysis → Procedure §4.3 duct bank capacity calculation development steps
- Guidance §Example 4 trenchless crossing structural analysis → Procedure §4.4 trenchless crossing calculation development steps

**Principles Linked to Requirements and Procedures:**
- P-1 hydraulic performance verification → Specification FR-1 comprehensive hydraulic analysis → Procedure §4.1 storm drainage calculations → Procedure §7.3.2 hydraulic performance validation
- P-2 environmental protection performance verification → Specification FR-2 environmental protection verification → Procedure §4.2 OWS sizing + §5 environmental calculations → Procedure §7.3.3 OWS compliance verification
- P-3 calculation assumptions traceability → Specification QR-2 methodology documentation → Procedure §4.5 methodology documentation → Procedure §7.1.4 methodology completeness check
- P-4 coordination with design deliverables → Specification IF-1 coordination with related deliverables → Procedure §2.1 input data collection + §7.2 interdisciplinary check → Procedure §7.2 coordination verification

(All Guidance principles have clear linkages to Specification requirements and Procedure implementation.)

## Pass 3 Final Notes

**Pass 3 Reconciliation Completed:**
- All cross-document linkages verified bidirectional: Guidance principles/considerations/examples reference Datasheet attributes/conditions/construction, Specification requirements, and Procedure steps; corresponding back-references confirmed in those documents.
- Principles linked to requirements and procedures: All four principles (P-1 through P-4) map to Specification functional/performance/interface/quality requirements and Procedure implementation steps; traceability matrix documented above.
- Entity coverage check: All major calculation types and themes appear consistently across all four documents (see Datasheet §Cross-Document Linkages entity coverage check).
- Terminology consistency verified: Key terms used consistently across all four documents (see Specification §Cross-Document Linkages terminology consistency check).
- Examples provide implementation guidance: All four examples demonstrate application of principles and provide concrete calculation structure/methodology guidance referenced by Datasheet construction content and Procedure steps.
- No conflicts detected between documents; all rationale, requirements, and implementation steps align.

**Document Maturity:**
- This Guidance, along with Datasheet, Specification, and Procedure, has completed three enrichment passes (Pass 1 initial generation, Pass 2 cross-reference and detail enrichment, Pass 3 final reconciliation).
- Documents are ready for WORKING_ITEMS sessions where human engineer will refine, validate, and populate TBD items as design development proceeds.
- All four documents provide coherent, traceable, and consistent foundation for DEL-03.03 Underground Utilities Design Calculations production.
