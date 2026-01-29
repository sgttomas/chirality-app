# Datasheet: DEL-12.03 Metering Design Calculations

## Identification

| Field | Value |
|-------|-------|
| Deliverable ID | DEL-12.03 |
| Name | Metering Design Calculations |
| Package | PKG-12 Product Transfer & Metering |
| Discipline | Process |
| Type | Calculation |
| Responsible | D&B Contractor |
| Status | INITIALIZED |

## Attributes

| Attribute | Value |
|-----------|-------|
| Calculation Number | To be issued per project numbering system (TBD; Source: ER Vol 2 Part 1, location TBD) |
| Software/Tool | TBD — calculation method and tools to be declared in calculation report; may include vendor sizing tools, spreadsheet calculations, hand calculations, or specialized software (e.g., for uncertainty propagation per ISO GUM or API MPMS Chapter 13) |
| Design Code / Standard Basis | TBD — custody transfer metering standards and ER clauses (Source: ER Vol 2 Part 2, location TBD); likely includes API MPMS (Chapter 4 Proving, Chapter 5 Metering, Chapter 13 Statistical Aspects), OIML R117 (uncertainty methodology), Measurement Canada regulations |
| Revision | 00 (initial issue) |
| Classification | Process — Custody Transfer Metering Calculations |
| Estimated Length | 30-50 pages including inputs, methodology, calculations, sensitivity analysis, results summary, and appendices (ASSUMPTION based on typical custody transfer metering calculation packages) |

## Conditions

### Design Context

| Condition | Value / Description | Source |
|-----------|---------------------|--------|
| Service Application | Custody transfer metering for CSD canola oil at rail unloading and marine loading transfer points | Decomposition:350 |
| Product | CSD (Crude Super Degummed) canola oil | Decomposition:43 |
| Design Throughput | 1,000,000 MT per annum (permitted) | Decomposition:41 |
| Metering Points | Two primary custody transfer locations: (1) Rail unloading — measuring product received from rail tank cars; (2) Marine loading — measuring product delivered to liquid bulk carriers for export | Decomposition:350 |

### Calculation Input Parameters (TBD)

All input parameters TBD from ER Vol 2 Part 2, DEL-12.02 specification, or design basis documents; calculations shall document sources for all inputs per Specification.md REQ-01, REQ-11:

| Parameter | Value | Source |
|-----------|-------|--------|
| **Product Properties** |
| Product Density (at reference temperature) | TBD (typical canola oil: ~0.91-0.92 g/cm³ at 15°C; ASSUMPTION) | ER Vol 2 Part 2, location TBD; or product specifications |
| Product Density vs. Temperature Curve | TBD; required for volume/mass conversion and compensation calculations | ER Vol 2 Part 2, location TBD; or product specifications |
| Product Viscosity (at operating temperature) | TBD (typical canola oil: ~30-70 cP at 20°C, decreases with temperature; ASSUMPTION) | ER Vol 2 Part 2, location TBD; or product specifications |
| Product Viscosity vs. Temperature Curve | TBD; affects meter technology selection and performance | ER Vol 2 Part 2, location TBD; or product specifications |
| Product Vapor Pressure | TBD; affects cavitation risk (vegetable oils have very low vapor pressure; cavitation unlikely; ASSUMPTION) | ER Vol 2 Part 2, location TBD; or product specifications |
| **Operating Conditions** |
| Operating Temperature Range | TBD (e.g., 5°C to 40°C ambient; product temperature may be controlled; ASSUMPTION) | ER Vol 2 Part 2, location TBD |
| Operating Pressure Range | TBD (e.g., 2-10 bar; depends on pump discharge pressure and piping elevation; ASSUMPTION) | ER Vol 2 Part 2, location TBD; or PKG-14 piping hydraulics |
| **Rail Unloading Service** |
| Rail Unloading Flow Rate (design) | TBD (depends on number of cars unloading concurrently, pump capacity, railcar capacity; facility has 32 unloading stations per Decomposition:44; typical railcar unloading rate 50-100 m³/h per car; ASSUMPTION) | ER Vol 2 Part 2, location TBD; or DEL-10.03 railcar unloading calculations |
| Rail Unloading Flow Rate (normal) | TBD (typical operation flow rate) | ER Vol 2 Part 2, location TBD |
| Rail Unloading Flow Rate (minimum) | TBD (minimum measurable flow; affects turndown requirement and low-flow accuracy) | ER Vol 2 Part 2, location TBD |
| Rail Unloading Flow Rate (maximum) | TBD (peak unloading flow rate; affects meter sizing and pressure drop) | ER Vol 2 Part 2, location TBD |
| **Marine Loading Service** |
| Marine Loading Flow Rate (design) | TBD (depends on vessel loading capacity and desired loading time; typical bulk vessel loading rates 500-2000 m³/h for vegetable oil; ASSUMPTION) | ER Vol 2 Part 2, location TBD; or DEL-11.03 marine loading calculations |
| Marine Loading Flow Rate (normal) | TBD (typical loading flow rate) | ER Vol 2 Part 2, location TBD |
| Marine Loading Flow Rate (minimum) | TBD (minimum loading flow; start-up and shut-down rates) | ER Vol 2 Part 2, location TBD |
| Marine Loading Flow Rate (maximum) | TBD (peak loading rate; affects meter sizing) | ER Vol 2 Part 2, location TBD |
| **Performance Requirements** |
| Accuracy Requirement (custody transfer) | TBD (e.g., ±0.15%, ±0.25%, or per ER; typical custody transfer accuracy for vegetable oils ±0.15% to ±0.5%; ASSUMPTION) | ER Vol 2 Part 2, location TBD; or DEL-12.02 specification |
| Repeatability Requirement | TBD (e.g., ±0.05%, ±0.1%; typically tighter than accuracy; ASSUMPTION) | ER Vol 2 Part 2, location TBD; or DEL-12.02 specification |
| Turndown Ratio Requirement | TBD (minimum turndown ratio; typical custody transfer meters 10:1 to 20:1; ASSUMPTION) | ER Vol 2 Part 2, location TBD; or DEL-12.02 specification |
| Proving Frequency | TBD (e.g., quarterly, semi-annually, annually; depends on Measurement Canada requirements and operational schedule; ASSUMPTION) | ER Vol 2 Part 2, location TBD; or Measurement Canada regulations |
| Proving Acceptance Criteria | TBD (e.g., meter factor drift within ±0.05%; per applicable standard; ASSUMPTION) | API MPMS Chapter 4, OIML R117, or Measurement Canada; TBD |

### Objective Alignment

| Objective | Relevance to This Deliverable |
|-----------|-------------------------------|
| OBJ-2 Throughput Capacity (1,000,000 MT/a) | Calculations must demonstrate meter sizing supports 1,000,000 MT/a throughput without flow constraints; flow rates for rail unloading and marine loading must accommodate design throughput; meter pressure drop must not excessively constrain system hydraulics (Source: Decomposition:781; Specification.md REQ-04) |
| OBJ-10 Custody Transfer Accuracy | Calculations must demonstrate accuracy and uncertainty budget meets custody transfer requirements; uncertainty analysis shall verify combined expanded uncertainty meets specified accuracy class; proving methodology and acceptance criteria shall be defined to maintain accuracy over time (Source: Decomposition:789; Specification.md REQ-05) |

## Construction

### Anticipated Calculation Content

| Calculation Type | Description | Source |
|------------------|-------------|--------|
| Flow Meter Sizing | Meter size selection based on flow range, product properties (density, viscosity), pressure drop calculation, turndown ratio verification; separate sizing for rail unloading and marine loading services; selection of meter technology (Coriolis, ultrasonic, turbine, positive displacement, or per DEL-12.02) | Decomposition:358; Specification.md REQ-04, REQ-07 |
| Accuracy / Uncertainty Calculations | Uncertainty budget development per applicable standard (API MPMS Chapter 13, OIML R117, ISO GUM, or other; TBD); identification of uncertainty components (meter base uncertainty, temperature measurement, pressure measurement, density measurement/compensation, proving uncertainty); uncertainty propagation methodology; combined expanded uncertainty calculation; verification that combined uncertainty meets accuracy requirement per DEL-12.02 | Decomposition:358; Specification.md REQ-05, REQ-06 |
| Proving Calculations | Proving method selection basis (in-line prover, portable prover, master meter; per DEL-12.02); prover sizing if in-line prover (prover displacement volume, repeatability requirements); proving repeatability requirements per applicable standard; meter factor acceptance criteria (e.g., drift limits); proving frequency rationale (regulatory requirements, operational considerations) | Decomposition:358; Specification.md REQ-05 |

### Calculation Methodology

Expected calculation approaches (ASSUMPTION; specific methodology TBD based on selected meter technology and applicable standards):

| Topic | Expected Approach |
|-------|-------------------|
| **Sizing Methodology** | **Manufacturer selection tools**: Vendor sizing software if meter technology is selected (Coriolis, ultrasonic, turbine manufacturers provide sizing tools based on flow rate, fluid properties, pipe size, allowable pressure drop); **First-principles calculation**: Calculate Reynolds number, velocity, pressure drop using Darcy-Weisbach or manufacturer-specific pressure drop correlations; verify flow velocity is within acceptable range (typically 1-5 m/s for liquids; varies by meter type); verify turndown ratio (ratio of maximum to minimum flow rate) meets requirement and meter maintains accuracy across range |
| **Accuracy/Uncertainty Methodology** | **Uncertainty budget per API MPMS Chapter 13** (if applicable): Identify all uncertainty components (Type A: statistical; Type B: systematic); quantify individual uncertainties (standard uncertainty for each component); combine uncertainties using root-sum-squares (RSS) method or Monte Carlo simulation; calculate combined standard uncertainty; apply coverage factor (typically k=2 for 95% confidence level) to obtain expanded uncertainty; **OIML R117 uncertainty methodology** (if applicable): Follow OIML approach for dynamic measuring systems; **ISO GUM (Guide to the Expression of Uncertainty in Measurement)** (general framework): Applicable if specific metering standard does not prescribe methodology |
| **Proving Methodology** | **In-line prover sizing** (if selected): Calculate required prover volume based on meter flow rate and proving duration; verify prover repeatability meets requirement (typically ±0.02% to ±0.05%); calculate proving time at different flow rates; **Portable prover sizing** (if selected): Specify portable prover capacity and uncertainty; define proving procedure and frequency; **Master meter** (if selected): Specify master meter uncertainty and calibration interval; **Acceptance criteria**: Define meter factor limits (e.g., meter factor drift <±0.05% from baseline or previous proving); cite source standard (API MPMS Chapter 4, OIML R117, or Measurement Canada) |

### Calculation Report Structure

Expected calculation report structure per Specification.md Documentation section (ASSUMPTION; project standards may vary):

| Section | Content |
|---------|---------|
| 1. Purpose and Scope | Calculation objectives: size custody transfer meters for rail unloading and marine loading, verify accuracy/uncertainty, define proving methodology; services covered (rail unloading, marine loading); CSD canola oil product; custody transfer application requiring Measurement Canada approval or equivalent |
| 2. Inputs and Sources | **ER requirements**: Flow rates, operating conditions, accuracy requirements, regulatory requirements (cite ER Vol 2 Part 2 clause numbers); **DEL-12.02 specification requirements**: Performance specifications, meter technology (if specified), proving method; **Product properties**: CSD canola oil density, viscosity, temperature (cite source: ER, product specs, or literature); **Standards and codes**: API MPMS (chapters), OIML R117, Measurement Canada (cite clause numbers); **Vendor data**: Manufacturer specifications (if available; cite vendor and document number) |
| 3. Assumptions and Boundary Conditions | **Assumptions**: List all assumptions with rationale (e.g., "Product temperature assumed 20°C ±10°C based on ambient conditions; actual temperature may vary; temperature compensation will be provided per DEL-12.02"); **Boundary conditions**: Upstream and downstream pressure conditions, flow control philosophy (constant flow vs. variable flow), proving method constraints (space availability, operational schedule) |
| 4. Methodology | **Sizing methodology**: Manufacturer selection tools or first-principles approach; pressure drop calculation method; turndown verification approach; **Uncertainty methodology**: Uncertainty budget framework (API MPMS Chapter 13, OIML R117, ISO GUM; specify which); uncertainty propagation method (RSS, Monte Carlo, other); coverage factor and confidence level; **Proving methodology**: Prover sizing approach (if applicable), acceptance criteria basis (cite standard) |
| 5. Flow Meter Sizing Calculations | **Rail unloading metering**: Flow rates (design, normal, min, max), product properties at operating conditions, preliminary meter technology selection (if not specified in DEL-12.02), meter size calculation, pressure drop calculation at maximum flow, turndown ratio verification, results summary (selected meter size, pressure drop, turndown); **Marine loading metering**: Same structure as rail unloading; **Results comparison**: Compare rail and marine sizing; evaluate commonality opportunities |
| 6. Accuracy / Uncertainty Analysis | **Uncertainty budget**: List all uncertainty components with values and sources; **Uncertainty components**: (a) Meter base uncertainty (from manufacturer specification or selected accuracy class), (b) Temperature measurement uncertainty (transmitter accuracy, installation effects), (c) Pressure measurement uncertainty (transmitter accuracy), (d) Density uncertainty (measured density if Coriolis, assumed density or correlation if volumetric meter), (e) Proving uncertainty (prover uncertainty contribution), (f) Other uncertainties (flow computer, signal conditioning, other); **Uncertainty propagation**: Combine individual uncertainties per methodology; calculate combined standard uncertainty; apply coverage factor to obtain expanded uncertainty; **Results**: Combined expanded uncertainty for rail unloading and marine loading; compare to accuracy requirement from DEL-12.02; verify compliance |
| 7. Proving Basis | **Proving method selection**: Rationale for selected proving method (in-line prover, portable prover, master meter); consider accuracy requirements, operational constraints, space availability, cost; **Prover sizing** (if in-line prover): Calculate prover volume, repeatability, proving time; **Proving frequency**: Rationale for proving frequency (Measurement Canada requirement, ER requirement, operational schedule); **Acceptance criteria**: Define meter factor limits (e.g., ±0.05% drift); cite source standard; define actions if proving fails (re-prove, re-calibrate, replace meter) |
| 8. Sensitivity Analysis | **Key parameter sensitivities**: (a) Flow rate: Accuracy at minimum vs. maximum flow (verify turndown), (b) Temperature: Temperature compensation error at temperature extremes, (c) Viscosity: Impact on meter performance (relevant for turbine meters; less relevant for Coriolis), (d) Proving uncertainty: Impact of prover accuracy on combined uncertainty; **Results**: Identify critical parameters; document sensitivity to assumptions; highlight risk areas |
| 9. Results Summary | **Meter sizing**: Selected meter sizes for rail unloading and marine loading; pressure drops; turndown ratios; **Accuracy/uncertainty**: Combined expanded uncertainties for rail and marine services; compliance with accuracy requirements; **Proving**: Selected proving method, frequency, acceptance criteria; **Conclusions**: Confirm metering design meets OBJ-2 (throughput) and OBJ-10 (accuracy) |
| 10. Implications for Other Deliverables | **DEL-12.01 Drawings**: Meter sizes, straight-run requirements (from manufacturer or standard), proving connection requirements; **DEL-12.02 Specification**: Verify calculated performance aligns with specification; identify any conflicts or TBDs requiring specification update; **DEL-12.04 Data Sheets**: Meter sizes, flow ranges, accuracy class, proving requirements to be captured in data sheets; **DEL-12.05 Test Records**: Acceptance criteria for FAT, SAT, proving derived from calculations |
| 11. References | **Standards and codes**: API MPMS (chapter numbers), OIML R117, Measurement Canada, ISO GUM; **Project documents**: ER Vol 2 Part 2 (clause numbers), DEL-12.02 specification, design basis; **Vendor data**: Manufacturer specifications, sizing tools; **Technical literature**: If assumptions based on published data |
| Appendices | **Appendix A**: Detailed calculation sheets (hand calculations, spreadsheet printouts); **Appendix B**: Vendor sizing tool outputs (if used); **Appendix C**: Uncertainty budget detailed tables; **Appendix D**: Sensitivity analysis detailed results; **Appendix E**: Code excerpts or standard clauses (if referenced) |

## References

### Primary Sources

| Reference | Content | Location |
|-----------|---------|----------|
| Decomposition | PKG-12 scope definition, DEL-12.03 definition, objective mappings, facility parameters (throughput, unloading stations) | Lines 41, 44, 350, 358, 781, 789 |
| ER Vol 2 Part 1 | General requirements, document control, calculation standards | TBD |
| ER Vol 2 Part 2 | Process mechanical requirements, metering requirements, flow rates, operating conditions, fluid properties (CSD canola oil), accuracy requirements, proving requirements, regulatory compliance (Measurement Canada) | TBD |

### Related Deliverables (PKG-12)

| Deliverable | Relationship |
|-------------|--------------|
| DEL-12.01 Metering Design Drawing Set | Drawings implement arrangement based on calculation results; meter sizes, straight-run requirements, and proving connections from calculations shall be shown in drawings; coordinate to ensure drawings reflect calculated meter sizes and installation requirements |
| DEL-12.02 Metering Technical Specification | Specification provides performance requirements (accuracy, repeatability, turndown, flow ranges); calculations verify that metering design meets specification requirements; if calculations identify conflicts or performance shortfalls, specification may require revision; calculations shall cite specification requirements as inputs |
| DEL-12.04 Metering Data Sheet Package | Data sheets capture specific parameters validated by calculations; meter sizes, flow ranges, accuracy class, pressure drops calculated in DEL-12.03 shall be documented in DEL-12.04 data sheets; data sheets demonstrate compliance with calculated requirements |
| DEL-12.05 Metering Installation & Test Records | Test records demonstrate compliance with calculation-derived acceptance criteria; FAT and SAT acceptance criteria from calculations (accuracy, flow range, pressure drop) shall be verified in DEL-12.05 records; proving acceptance criteria from DEL-12.03 shall be used for ongoing proving verification |

### Applicable Standards (TBD — ASSUMPTION)

The following standards may be applicable to custody transfer metering calculations; specific applicability TBD from ER Vol 2 Part 2 and DEL-12.02 specification:

| Standard | Description | Potential Applicability |
|----------|-------------|------------------------|
| API MPMS Chapter 4 (Proving Systems) | Proving system design, prover sizing, proving procedures, acceptance criteria for meter proving | Applicable if API MPMS is governing standard for custody transfer; provides methodology for prover sizing and proving acceptance criteria |
| API MPMS Chapter 5 (Metering) | Metering system design, meter installation requirements, straight-run requirements, accuracy requirements | Applicable if API MPMS is governing standard; provides meter sizing and installation guidance |
| API MPMS Chapter 11 (Physical Properties) | Fluid physical properties, temperature correction, density, viscosity | Applicable for temperature and density compensation calculations |
| API MPMS Chapter 13 (Statistical Aspects) | Uncertainty analysis methodology, uncertainty propagation, statistical treatment of measurement data | Applicable for uncertainty budget development; comprehensive framework for custody transfer uncertainty analysis |
| OIML R117 (Dynamic Measuring Systems for Liquids Other Than Water) | Accuracy classes, uncertainty methodology, installation requirements, proving requirements for liquid measuring systems | Likely primary standard for vegetable oil custody transfer; provides accuracy classes (0.3, 0.5, 1.0, 1.5, 2.5) and uncertainty framework |
| ISO GUM (Guide to the Expression of Uncertainty in Measurement) | General uncertainty analysis framework, Type A and Type B uncertainties, uncertainty propagation, coverage factors | General uncertainty methodology applicable if metering-specific standard (API MPMS, OIML R117) does not prescribe approach |
| Measurement Canada (Weights and Measures Act and Regulations) | Canadian regulatory requirements for custody transfer measurement; meter approval requirements, proving requirements, periodic verification | Applicable for custody transfer in Canada; meters may require Measurement Canada approval; specific calculation requirements TBD |
| ISO 4185 (Measurement of Liquid Flow in Closed Conduits — Weighing and Volumetric Methods) | Reference methods for flowmeter calibration and proving | May be applicable for proving system design |

**Note:** Standard applicability and specific clauses to be confirmed from ER Vol 2 Part 2 and DEL-12.02 specification. Calculations shall cite specific standard clauses for methodology and acceptance criteria.

## Cross-Document Traceability

| Document | Section | Link Points |
|----------|---------|-------------|
| Specification.md | § Scope | Defines inclusions (flow meter sizing, accuracy/uncertainty calculations, proving calculations) and exclusions (vendor-specific sizing, control logic, piping hydraulics beyond metering) |
| Specification.md | § Requirements | REQ-01 through REQ-24: functional (REQ-01-05 documentation and coverage), performance (REQ-06-10 throughput and accuracy), methodology (REQ-11-13 standard-based), interface (REQ-14-17 boundary conditions and consistency), quality (REQ-18-22 checking and control), sensitivity (REQ-23-24 analysis) |
| Specification.md | § Standards | Governing references (ER Vol 2 Part 1/2) and custody transfer standards (API MPMS Chapters 4/5/11/13, OIML R117, ISO GUM, Measurement Canada, ISO 4185) |
| Specification.md | § Verification | Methods (document review, technical review, cross-document check, independent check, sensitivity review, standard compliance) and acceptance criteria |
| Specification.md | § Documentation | Calculation report structure matching Construction section (11 sections + appendices); documentation requirements (summary, input documentation, methodology, unit consistency) |
| Guidance.md | § Purpose | Calculations provide engineering basis for meter selection, accuracy verification, proving methodology; drive DEL-12.01, DEL-12.04, DEL-12.05 |
| Guidance.md | § Principles | Development rationale (objective demonstration REQ-06/07, traceability REQ-04, auditability REQ-18, no invention REQ-05, standard-based REQ-11/12/13); methodology principles (sizing REQ-06/09/10, uncertainty REQ-07/12, proving REQ-07/13) |
| Guidance.md | § Considerations | Sizing factors (flow range, product properties, pressure drop, turndown, meter technology per REQ-06/09/10/11); accuracy/uncertainty factors (meter, temperature, pressure, density, proving uncertainty per REQ-07/12); proving factors (method, size, frequency, criteria per REQ-13); service-specific (rail 32 stations, marine high flow per REQ-02) |
| Guidance.md | § Trade-offs | Competing factors: meter size vs. low-flow accuracy, accuracy vs. pressure drop, proving method vs. cost, conservative vs. realistic assumptions, standardization vs. optimization |
| Procedure.md | § Step 1 | Define cases for rail and marine services per REQ-02 |
| Procedure.md | § Step 2 | Collect inputs from ER, DEL-12.02, design basis per REQ-04/05/20 |
| Procedure.md | § Step 3 | Flow meter sizing per REQ-06/09/10/11 |
| Procedure.md | § Step 4 | Accuracy/uncertainty calculations per REQ-07/12 |
| Procedure.md | § Step 5 | Proving calculations per REQ-07/13 |
| Procedure.md | § Step 6 | Cross-check with DEL-12.02 per REQ-08/15 |
| Procedure.md | § Step 7 | Sensitivity analysis per REQ-23/24 |
| Procedure.md | § Step 8 | Assemble calculation report per REQ-01/16/19/20 |
| Procedure.md | § Step 9 | Independent check and issue per REQ-18/22 |
| DEL-12.01 | Drawings | Meter sizes, straight-run requirements, proving connections from calculations per Construction section implications |
| DEL-12.02 | Specification | Performance requirements (accuracy, turndown, flow range) as calculation inputs per Conditions section |
| DEL-12.04 | Data Sheets | Parameters validated by calculations (sizes, flow ranges, accuracy) per Construction section implications |
| DEL-12.05 | Test Records | Acceptance criteria from calculations (FAT/SAT accuracy, proving criteria) per Construction section implications
