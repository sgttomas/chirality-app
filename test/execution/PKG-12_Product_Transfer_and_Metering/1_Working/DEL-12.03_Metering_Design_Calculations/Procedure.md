# Procedure: DEL-12.03 Metering Design Calculations

## Purpose

This procedure defines the process for producing and managing **Metering Design Calculations** within **PKG-12 Product Transfer & Metering**.

### Deliverable Definition

DEL-12.03 provides the engineering basis and sizing/verification calculations for custody transfer metering (Source: Decomposition:358).

| Attribute | Value |
|-----------|-------|
| Deliverable Type | Calculation |
| Discipline | Process |
| Responsible Party | D&B Contractor |
| Service Application | Custody transfer metering for CSD canola oil at rail unloading and marine loading |

### Procedure Scope

This procedure covers the complete lifecycle for producing metering design calculations:

1. **Development** — defining cases, collecting inputs, performing sizing/accuracy/proving calculations
2. **Review and checking** — independent check workflow
3. **Issue and revision management** — document control, approvals, issuance

This procedure applies to all calculation types: flow meter sizing, accuracy/uncertainty analysis, and proving calculations.

## Prerequisites

### Dependencies

| Prerequisite | Status | Notes |
|--------------|--------|-------|
| Dependency Mode | NOT_TRACKED | Dependencies coordinated externally by humans (see `_DEPENDENCIES.md` and `execution/_Coordination/_COORDINATION.md`); coordinate with PKG-14 for flow rates and available pressure, PKG-10/PKG-11 for service requirements |

### Recommended Upstream Inputs

The following inputs should be obtained before commencing calculation development (ASSUMPTION based on typical calculation workflow):

| Input | Source | Purpose | Timing |
|-------|--------|---------|--------|
| Metering Technical Specification | DEL-12.02 | Performance requirements (accuracy, repeatability, turndown), meter technology (if specified), proving method (if specified), flow range requirements | Before Step 2 (Collect Inputs) |
| Employer's Requirements | ER Vol 2 Part 2 | Flow rates, accuracy requirements, operating conditions, fluid properties, proving requirements, regulatory compliance (Measurement Canada) | Before Step 2 (Collect Inputs) |
| Process Design Basis | Design Basis / PKG-14 | Operating pressure and temperature, product properties (CSD canola oil density, viscosity), flow rates if not in ER | Before Step 2 (Collect Inputs) |
| Rail Unloading Flow Rates | DEL-10.03 or design basis | Rail unloading design, normal, min, max flow rates | Before Step 3 (Sizing) |
| Marine Loading Flow Rates | DEL-11.03 or design basis | Marine loading design, normal, min, max flow rates | Before Step 3 (Sizing) |
| Applicable Standards | Standards library | API MPMS (Chapters 4, 5, 11, 13), OIML R117, ISO GUM, Measurement Canada regulations | During Step 2 (Collect Inputs) |
| Vendor Data | Meter vendors (if available) | Manufacturer performance specifications, sizing tools, accuracy curves, pressure drop data | During Step 3-5 (may be iterative with vendor selection) |

### Reference Materials

| Reference | Location | Purpose |
|-----------|----------|---------|
| `_REFERENCES.md` | Deliverable folder | Applicable reference documents; list of ER clauses, standards, project documents |
| `0_References/` | Package directory | Reference materials for PKG-12 (ER excerpts, standards, vendor literature, product data) |
| Employer's Requirements Vol 2 Part 1 | ER document set | General requirements, document control, calculation standards, quality procedures | TBD |
| Employer's Requirements Vol 2 Part 2 | ER document set | Process mechanical requirements, metering requirements, flow rates, operating conditions, fluid properties (CSD canola oil), accuracy requirements, proving requirements, regulatory compliance | TBD |
| Decomposition | Project root | PKG-12 scope (line 350), DEL-12.03 definition (line 358), objective mappings (lines 781, 789), facility parameters (throughput line 41, unloading stations line 44) |
| Specification.md | Deliverable folder | Requirements to be satisfied (REQ-01 through REQ-24); defines calculation scope, methodology requirements, quality requirements |
| Guidance.md | Deliverable folder | Calculation considerations, principles, trade-offs, technology selection factors, sizing factors, uncertainty factors, proving factors, service-specific considerations |
| Datasheet.md | Deliverable folder | Design context, calculation input parameters (all TBD items), anticipated calculation content, calculation report structure |

### Personnel Requirements

| Role | Qualification | Responsibility | Source |
|------|---------------|----------------|--------|
| Originator | Qualified Process discipline engineer with custody transfer metering experience; familiarity with applicable custody transfer standards (API MPMS, OIML R117); calculation and uncertainty analysis experience | Technical content, calculation development, input documentation, assumption documentation, results verification | ASSUMPTION; project quality procedures |
| Checker | Independent Process discipline engineer (not the originator); metering expertise; calculation checking experience | Independent verification of all calculations; re-perform key calculations; verify methodology appropriateness; check unit consistency; verify results reasonableness | ASSUMPTION; project quality procedures |
| Approver | Authorized per project procedures (typically Process Lead or Engineering Manager) | Authorization for issue; confirm calculations satisfy ER requirements and project objectives | TBD; ER Vol 2 Part 1 |

### Tools and Systems

| Tool/System | Purpose | Source |
|-------------|---------|--------|
| Calculation Software | Calculation development (Excel, MathCAD, Python, or specialized metering software) | TBD; declare tool in calculation report per Specification.md REQ-11 |
| Vendor Sizing Tools | Manufacturer-specific meter sizing tools (if available and if vendor selected) | Vendor; optional; results to be verified or used as inputs |
| Document Management System | Calculation storage, revision control, distribution | TBD; ER Vol 2 Part 1 |

## Steps

### Step 1: Define Cases

**Objective:** Identify services and operating scenarios to be analyzed in calculations.

| Action | Description | Output |
|--------|-------------|--------|
| 1.1 | Identify services to be calculated per Specification.md REQ-02: (1) Rail unloading custody transfer metering, (2) Marine loading custody transfer metering | Service identification |
| 1.2 | Define operating scenarios for each service per Guidance.md sizing factors: **Design flow rate** (maximum anticipated flow for sizing), **Normal flow rate** (typical operating flow), **Minimum flow rate** (lowest measurable flow; defines turndown), **Maximum flow rate** (peak flow; meter must handle without damage) | Operating scenario definitions |
| 1.3 | Define product properties to be used: **CSD canola oil density** (at reference temperature and vs. temperature curve), **Viscosity** (at operating temperature and vs. temperature curve), **Vapor pressure** (for cavitation assessment), **Compressibility** (if pressure compensation required) | Product property requirements |
| 1.4 | Define operating conditions: **Temperature range** (ambient and product temperature range), **Pressure range** (operating pressure at meter inlet and outlet), **Environmental conditions** (outdoor installation at Fraser Surrey Terminal; Pacific Northwest climate) | Operating condition definitions |
| 1.5 | Document case definitions in calculation introduction section per Specification.md Documentation section | Calculation introduction with case definitions |

**Output:** Documented calculation cases for rail unloading and marine loading services; operating scenarios defined; product properties identified; operating conditions identified

**Verification:** Case definitions cover both services per Specification.md REQ-02; operating scenarios address design, normal, min, max flows per Guidance.md

---

### Step 2: Collect Inputs

**Objective:** Gather all input data and reference materials necessary for calculations; document inputs with sources per Specification.md REQ-04, REQ-05, REQ-20.

| Action | Description | Output |
|--------|-------------|--------|
| 2.1 | Obtain flow rates from ER Vol 2 Part 2, DEL-10.03 (rail unloading), DEL-11.03 (marine loading), or design basis: rail unloading design/normal/min/max flow rates (m³/h or kg/h; units TBD), marine loading design/normal/min/max flow rates; document source (ER clause number, calculation reference, design basis section) | Flow rate inputs with sources |
| 2.2 | Obtain product properties from ER Vol 2 Part 2, product specifications, or technical literature: CSD canola oil density (g/cm³ at reference temperature and vs. temperature curve), viscosity (cP at operating temperature and vs. temperature curve), vapor pressure, compressibility (if significant); document source; if data unavailable, state assumption with rationale or mark TBD | Product property inputs with sources |
| 2.3 | Obtain operating conditions from ER Vol 2 Part 2 or design basis: operating temperature range (°C), operating pressure range (bar or kPa), environmental conditions (outdoor, temperature extremes, seismic); document source | Operating condition inputs with sources |
| 2.4 | Obtain performance requirements from DEL-12.02 Metering Technical Specification: accuracy requirement (e.g., ±0.15%, ±0.25%; TBD), repeatability requirement (e.g., ±0.05%, ±0.1%; TBD), turndown ratio requirement (e.g., 10:1, 20:1; TBD), proving frequency (quarterly, semi-annually, annually; TBD), proving acceptance criteria (e.g., meter factor drift ±0.05%; TBD); cite DEL-12.02 section numbers | Performance requirement inputs from DEL-12.02 |
| 2.5 | Obtain applicable standards per Specification.md Standards section: API MPMS (Chapters 4, 5, 11, 13 if applicable), OIML R117 (if primary standard for vegetable oil), ISO GUM (general uncertainty framework), Measurement Canada regulations (if applicable); obtain standard copies or access; identify specific standard clauses for methodology | Standard identification and access |
| 2.6 | Document all inputs in input table with columns: Parameter, Value, Units, Source (ER clause, specification section, calculation reference, standard, vendor data, assumption); per Specification.md REQ-04, REQ-20 | Input table in calculation report |
| 2.7 | Document all assumptions in assumption table with columns: Assumption, Rationale, Basis (if any), Impact if incorrect; per Specification.md REQ-05, REQ-20; mark unknowns as TBD with source needed | Assumption table in calculation report |
| 2.8 | Document boundary conditions per Specification.md REQ-14: upstream pressure (from pumps or elevation), downstream pressure (to storage or vessel), flow control philosophy (constant flow, variable flow, batch control), proving method constraints (space availability from DEL-12.01 layout, operational schedule) | Boundary condition documentation |

**Output:** Complete input documentation with sources; assumption documentation with rationale; boundary condition documentation

**Verification:** All inputs documented per Specification.md REQ-04, REQ-20; assumptions stated with rationale per REQ-05; TBD items flagged

---

### Step 3: Perform Flow Meter Sizing

**Objective:** Size flow meters for rail unloading and marine loading services; verify sizing supports OBJ-2 throughput per Specification.md REQ-06, REQ-09, REQ-10.

#### 3.1: Select Meter Technology (if not specified)

| Action | Description |
|--------|-------------|
| 3.1.1 | Review DEL-12.02 specification to determine if meter technology is specified (Coriolis, ultrasonic, turbine, positive displacement, or technology-neutral); if specified, use specified technology; if technology-neutral, select preliminary technology for sizing or perform sizing for multiple technologies for comparison |
| 3.1.2 | Consider factors per Guidance.md technology selection: accuracy (Coriolis ±0.10%-0.15%, ultrasonic ±0.15%-0.5%, turbine ±0.15%-0.25%), pressure drop (Coriolis higher, ultrasonic lower), straight-run requirements (Coriolis 3D-5D, ultrasonic/turbine 10D-20D), viscosity sensitivity (Coriolis insensitive, turbine sensitive), cost, product compatibility |
| 3.1.3 | Document technology selection or preliminary technology for sizing; cite basis (DEL-12.02 specification if specified, or engineering judgment with rationale if technology-neutral) |

#### 3.2: Size Meters for Rail Unloading Service

| Action | Description |
|--------|-------------|
| 3.2.1 | **Input flow rates**: Use rail unloading design flow rate (maximum flow for sizing), normal flow rate, minimum flow rate (for turndown), maximum flow rate (peak flow) from Step 2 |
| 3.2.2 | **Select meter size**: Use manufacturer sizing tool if available (input flow rates, fluid properties, pipe size, allowable pressure drop; tool recommends meter size) or perform first-principles sizing (calculate required meter capacity, select meter size from manufacturer product line); preliminary meter size selection |
| 3.2.3 | **Calculate pressure drop**: Using selected meter size and maximum flow rate, calculate pressure drop across meter; use manufacturer pressure drop data/correlations or Darcy-Weisbach equation if first-principles; verify pressure drop is acceptable (coordinate with PKG-14 for available system pressure; pressure drop should not excessively constrain system) per Specification.md REQ-10 |
| 3.2.4 | **Calculate flow velocity**: Velocity = flow rate / pipe cross-sectional area; verify velocity is within acceptable range (typically 1-5 m/s for liquids; may vary by meter type and application; verify with manufacturer recommendations) |
| 3.2.5 | **Verify turndown ratio**: Turndown = maximum flow / minimum flow; verify turndown ≥ required turndown from DEL-12.02 (e.g., 10:1, 20:1; TBD); verify meter accuracy is maintained across entire turndown range (review manufacturer accuracy curves; some meters have degraded accuracy at low flows) per Specification.md REQ-09 |
| 3.2.6 | **Verify throughput support**: Calculate annual throughput capacity based on meter size and operating schedule; verify supports portion of 1,000,000 MT/a facility throughput allocated to rail unloading service per Specification.md REQ-06 |
| 3.2.7 | **Document sizing**: Record selected meter size, pressure drop, flow velocity, turndown ratio, throughput verification; cite methodology (vendor tool, first-principles, standard) per Specification.md REQ-11 |

#### 3.3: Size Meters for Marine Loading Service

| Action | Description |
|--------|-------------|
| 3.3.1 | Repeat sizing process (Actions 3.2.1 through 3.2.7) for marine loading service using marine loading flow rates from Step 2 |
| 3.3.2 | Note that marine loading typically has higher flow rates than rail unloading; meter size for marine may be larger; verify sizing separately |
| 3.3.3 | Document marine loading meter sizing with same detail as rail unloading |

#### 3.4: Compare Rail and Marine Sizing Results

| Action | Description |
|--------|-------------|
| 3.4.1 | Compare meter sizes, pressure drops, turndown ratios for rail unloading vs. marine loading |
| 3.4.2 | Evaluate opportunities for standardization per Guidance.md trade-offs: if meter sizes are similar, consider using identical technology/model for both services (procurement, spares, training benefits); if flow rates differ significantly, accept different sizes |
| 3.4.3 | Document comparison and standardization considerations |

**Output:** Flow meter sizing calculations for rail unloading and marine loading; selected meter sizes; pressure drops; turndown ratios; throughput verification

**Verification:** Sizing supports OBJ-2 throughput per Specification.md REQ-06; turndown ratios meet requirements per REQ-09; pressure drops acceptable per REQ-10; methodology documented per REQ-11

---

### Step 4: Perform Accuracy / Uncertainty Calculations

**Objective:** Develop uncertainty budget and verify combined uncertainty meets accuracy requirements per Specification.md REQ-07, REQ-12.

#### 4.1: Identify Uncertainty Components

| Action | Description |
|--------|-------------|
| 4.1.1 | Identify all uncertainty components per Guidance.md accuracy/uncertainty factors: (a) Meter base uncertainty (manufacturer specification or selected accuracy class), (b) Temperature measurement uncertainty (transmitter accuracy from DEL-12.02 or assumed), (c) Pressure measurement uncertainty (if applicable), (d) Density uncertainty (measured if Coriolis, assumed or correlated if volumetric meter), (e) Proving uncertainty (prover accuracy; will be calculated in Step 5), (f) Other uncertainties (flow computer, signal conditioning, installation effects) |
| 4.1.2 | Document uncertainty component identification in uncertainty budget table |

#### 4.2: Quantify Individual Uncertainties

| Action | Description |
|--------|-------------|
| 4.2.1 | **Meter base uncertainty**: Obtain from manufacturer specification (e.g., ±0.15% of reading) or selected accuracy class (e.g., OIML R117 accuracy class 0.5 = ±0.5%); note that accuracy may vary with flow rate (review manufacturer accuracy curve); select conservative value or calculate flow-weighted average; document source (manufacturer data sheet, accuracy class standard) |
| 4.2.2 | **Temperature measurement uncertainty**: Obtain transmitter accuracy from DEL-12.02 specification or assume typical value (e.g., RTD Pt100 ±0.1°C; thermocouple ±0.5°C; TBD); calculate impact on density compensation using density-temperature coefficient for canola oil (typical ~0.0007 g/cm³ per °C; ASSUMPTION; TBD from product data); temperature uncertainty contribution = temperature measurement error × density-temperature coefficient / density |
| 4.2.3 | **Pressure measurement uncertainty**: If pressure compensation is required (for volumetric meters if compressibility is significant), obtain transmitter accuracy from DEL-12.02 or assume (e.g., ±0.1% of span); calculate impact on volume/mass using compressibility; if canola oil compressibility is negligible (TBD; verify from product data), pressure compensation may not be required and pressure uncertainty may be omitted |
| 4.2.4 | **Density uncertainty**: If Coriolis meter with integral density measurement, obtain density measurement uncertainty from manufacturer (e.g., ±0.001 g/cm³); if volumetric meter, density uncertainty depends on approach: measured density (online densitometer uncertainty), assumed fixed density (estimate uncertainty range, e.g., ±0.01 g/cm³), calculated from temperature correlation (propagate temperature uncertainty through correlation) |
| 4.2.5 | **Proving uncertainty**: Use prover uncertainty from Step 5 proving calculations (in-line prover typical ±0.02% to ±0.05%, portable prover ±0.05% to ±0.1%, master meter per master meter accuracy) |
| 4.2.6 | **Other uncertainties**: Consider flow computer uncertainty, signal conditioning, installation effects (meter misalignment, piping stress); typically small but include if significant; may assume negligible if not quantifiable |
| 4.2.7 | Document all uncertainty component values with sources in uncertainty budget table per Specification.md REQ-20 |

#### 4.3: Propagate Uncertainties

| Action | Description |
|--------|-------------|
| 4.3.1 | Select uncertainty propagation methodology per Specification.md REQ-12: API MPMS Chapter 13 (root-sum-squares for independent uncertainties), OIML R117 (metering-specific framework), ISO GUM (general framework); cite selected methodology |
| 4.3.2 | Calculate combined standard uncertainty using root-sum-squares (RSS) per API MPMS Chapter 13 or selected methodology: U_combined = sqrt(U_meter² + U_temperature² + U_pressure² + U_density² + U_proving² + U_other²) where each U is standard uncertainty for that component |
| 4.3.3 | Apply coverage factor to obtain expanded uncertainty: U_expanded = k × U_combined; typical coverage factor k=2 for 95% confidence level (per API MPMS Chapter 13 or ISO GUM); document coverage factor and confidence level |
| 4.3.4 | Calculate expanded uncertainty as percentage of reading: U_expanded_% = U_expanded / measured value × 100% |
| 4.3.5 | Document uncertainty propagation methodology, combined standard uncertainty calculation, coverage factor application, expanded uncertainty result per Specification.md REQ-12 |

#### 4.4: Verify Accuracy Requirement Compliance

| Action | Description |
|--------|-------------|
| 4.4.1 | Compare calculated expanded uncertainty to accuracy requirement from DEL-12.02 specification (e.g., if requirement is ±0.15%, expanded uncertainty must be ≤±0.15%) |
| 4.4.2 | Verify compliance for both rail unloading and marine loading services (uncertainties may differ if flow rates, temperatures, or proving methods differ) |
| 4.4.3 | If expanded uncertainty exceeds requirement, identify largest uncertainty contributors from budget; consider mitigation: tighter meter accuracy class, improved temperature/density measurement, better prover, reduced flow rate range (tighter turndown) |
| 4.4.4 | Document verification that expanded uncertainty meets accuracy requirement per Specification.md REQ-07; verify supports OBJ-10 custody transfer accuracy |

**Output:** Uncertainty budget with all components quantified; combined standard uncertainty; expanded uncertainty; verification of accuracy requirement compliance

**Verification:** Uncertainty methodology per recognized standard (API MPMS, OIML R117, ISO GUM) per Specification.md REQ-12; combined uncertainty meets accuracy requirement per REQ-07; supports OBJ-10 per REQ-07

---

### Step 5: Perform Proving Calculations

**Objective:** Define proving methodology, size prover if applicable, define acceptance criteria per Specification.md REQ-07, REQ-13.

#### 5.1: Select Proving Method

| Action | Description |
|--------|-------------|
| 5.1.1 | Review DEL-12.02 specification to determine if proving method is specified (in-line prover, portable prover, master meter); if specified, use specified method; if not specified, select method based on evaluation |
| 5.1.2 | Evaluate proving method options per Guidance.md proving factors: **In-line prover**: higher accuracy (±0.02%-0.05%), continuous proving capability, suitable for high-value custody transfer (marine loading), requires space and capital cost; **Portable prover**: lower cost, flexible (one prover for multiple meters), typical accuracy ±0.05%-0.1%, suitable for rail unloading; **Master meter**: uses calibrated reference meter, suitable when provers impractical; select based on accuracy requirements, operational constraints, space availability, cost |
| 5.1.3 | Document proving method selection with rationale; cite basis (DEL-12.02 if specified, or engineering evaluation per Guidance.md if selection required) per Specification.md REQ-13 |

#### 5.2: Size Prover (if In-Line Prover Selected)

| Action | Description |
|--------|-------------|
| 5.2.1 | If in-line prover is selected, calculate required prover volume: Prover volume = flow rate × proving time / number of proving runs; typical proving time 30-120 seconds (TBD; per API MPMS Chapter 4 or operational requirements); typical number of runs 3-5 for repeatability verification |
| 5.2.2 | Verify prover repeatability can be achieved: prover repeatability depends on prover volume, meter flow rate, pulse resolution, and operational factors; typical in-line prover repeatability ±0.02% to ±0.05%; verify selected prover volume can achieve required repeatability per API MPMS Chapter 4 |
| 5.2.3 | Document prover sizing calculations: prover volume, proving time, number of runs, repeatability; cite methodology (API MPMS Chapter 4 or other) |
| 5.2.4 | If portable prover or master meter is selected, specify prover/master meter capacity and uncertainty; document requirements |

#### 5.3: Define Proving Frequency

| Action | Description |
|--------|-------------|
| 5.3.1 | Identify regulatory requirements for proving frequency from Measurement Canada regulations or ER Vol 2 Part 2 (TBD; typical regulatory requirements quarterly to annually) |
| 5.3.2 | Consider operational requirements: commercial agreements may specify proving frequency, operational confidence needs, service-specific requirements (marine loading may require more frequent proving than rail unloading) |
| 5.3.3 | Coordinate proving frequency with operational schedule: proving during scheduled maintenance windows vs. online proving during operations; operational feasibility |
| 5.3.4 | Define proving frequency with rationale: cite regulatory requirement, commercial requirement, or operational requirement; per Specification.md REQ-13 |

#### 5.4: Define Meter Factor Acceptance Criteria

| Action | Description |
|--------|-------------|
| 5.4.1 | Define meter factor: Meter factor = true volume (from prover) / indicated volume (from meter); ideal meter factor = 1.000; actual meter factor accounts for meter calibration offset |
| 5.4.2 | Define meter factor acceptable range: typical range 0.995 to 1.005 (±0.5%); may be tighter for high-accuracy applications; cite applicable standard (API MPMS Chapter 4, OIML R117, Measurement Canada) |
| 5.4.3 | Define meter factor drift acceptance: define acceptable drift from baseline (initial proving) or previous proving; typical ±0.05% drift limit; if drift exceeds limit, meter requires re-calibration or investigation |
| 5.4.4 | Define proving repeatability requirement: define required repeatability for proving run acceptance (e.g., proving runs must agree within ±0.02% for in-line prover, ±0.05% for portable prover); if repeatability is not achieved, proving is invalid and must be repeated |
| 5.4.5 | Define actions if proving fails: if meter factor is outside acceptable range or drift exceeds limit, define actions (re-prove to verify, re-calibrate meter, investigate cause, replace meter if defective) |
| 5.4.6 | Document meter factor acceptance criteria citing applicable standard per Specification.md REQ-13; cite API MPMS Chapter 4, OIML R117, or Measurement Canada for acceptance criteria basis |

#### 5.5: Document Proving Uncertainty Contribution

| Action | Description |
|--------|-------------|
| 5.5.1 | Document prover uncertainty for use in uncertainty budget (Step 4.2.5): in-line prover uncertainty (typical ±0.02% to ±0.05%), portable prover uncertainty (typical ±0.05% to ±0.1%), master meter uncertainty (per master meter accuracy class) |
| 5.5.2 | Document prover calibration traceability requirement: prover calibration shall be traceable to national metrology institute (Measurement Canada, NIST, or equivalent); calibration interval (typical 12 months or per regulatory requirement) |

**Output:** Proving method selection with rationale; prover sizing (if in-line prover); proving frequency with rationale; meter factor acceptance criteria citing standard; prover uncertainty for uncertainty budget

**Verification:** Proving methodology cites applicable standard per Specification.md REQ-13; proving supports OBJ-10 accuracy per REQ-07

---

### Step 6: Cross-Check with Specification

**Objective:** Verify calculation inputs and results align with DEL-12.02 specification; identify conflicts per Specification.md REQ-08, REQ-15.

| Action | Description | Verification |
|--------|-------------|--------------|
| 6.1 | Review calculation inputs vs. DEL-12.02 specification requirements: verify accuracy requirement used in calculations matches DEL-12.02; verify flow ranges align with DEL-12.02; verify meter technology (if specified in DEL-12.02) matches sizing; verify proving method (if specified in DEL-12.02) matches proving calculations | Input alignment check |
| 6.2 | Review calculation results vs. DEL-12.02 requirements: verify calculated meter sizes can meet specified accuracy; verify calculated pressure drops are acceptable; verify calculated turndown ratios meet specification; verify calculated uncertainty meets accuracy requirement | Results compliance check |
| 6.3 | Identify conflicts or TBDs: if calculation results do not meet specification requirements, identify conflict and document in Guidance.md Conflict Table with citations (calculation result vs. specification clause); if inputs are TBD in DEL-12.02, flag TBD in calculations and note source needed | Conflict identification |
| 6.4 | Update calculations or flag issues: if minor conflicts can be resolved by calculation adjustment (e.g., larger meter size), update calculations; if significant conflicts exist (e.g., specified accuracy cannot be achieved with specified meter technology), flag for human ruling per Guidance.md Conflict Table | Conflict resolution or flagging |

**Output:** Cross-check verification documenting alignment or conflicts with DEL-12.02 specification

**Verification:** Calculation inputs align with DEL-12.02 per Specification.md REQ-08; calculation results meet specification requirements per REQ-15; conflicts flagged

---

### Step 7: Perform Sensitivity Analysis

**Objective:** Evaluate sensitivity of results to key parameters; identify critical assumptions and risks per Specification.md REQ-23, REQ-24.

| Action | Description | Output |
|--------|-------------|--------|
| 7.1 | Identify key parameters for sensitivity analysis per Guidance.md sensitivity topics: flow rate variation (accuracy at min vs. max flow), temperature variation (compensation error at extremes), viscosity variation (impact on meter performance if turbine meter), prover uncertainty (impact on combined uncertainty), density assumption (if volumetric meter without density measurement) | Parameter identification |
| 7.2 | Evaluate flow rate sensitivity per Specification.md REQ-23: calculate accuracy (expanded uncertainty) at minimum flow, normal flow, and maximum flow; verify accuracy is maintained across turndown range; identify if accuracy degrades significantly at low flows (may indicate turndown limitation or need for dual-range metering) | Flow rate sensitivity results |
| 7.3 | Evaluate temperature sensitivity: calculate density correction error at minimum and maximum operating temperatures; assess impact on mass flow uncertainty; identify if temperature compensation uncertainty is significant contributor to combined uncertainty; if temperature range is wide and density-temperature coefficient is large, temperature compensation may be critical | Temperature sensitivity results |
| 7.4 | Evaluate other parameter sensitivities as applicable: viscosity variation impact (for turbine meters), prover uncertainty impact (compare in-line ±0.02% vs. portable ±0.1% on combined uncertainty), density assumption impact (for volumetric meters; calculate mass flow error for ±X% density variation) | Other sensitivity results |
| 7.5 | Identify critical assumptions and parameters per Specification.md REQ-24: document parameters where small variations significantly impact results; document assumptions that if incorrect would significantly affect sizing or accuracy; document risks (e.g., "If actual minimum flow is lower than assumed, meter may not maintain accuracy at low flows; risk: measurement errors at low flow conditions") | Critical assumptions and risks |
| 7.6 | Document sensitivity analysis results in calculation report per Specification.md Documentation section | Sensitivity analysis section in calculation report |

**Output:** Sensitivity analysis results for key parameters; identification of critical assumptions and risks

**Verification:** Sensitivity analysis performed per Specification.md REQ-23; critical assumptions and risks identified per REQ-24

---

### Step 8: Assemble Calculation Report

**Objective:** Compile complete calculation report with all sections per Specification.md Documentation section and Datasheet.md report structure.

| Action | Description | Output |
|--------|-------------|--------|
| 8.1 | Assemble calculation report per structure in Specification.md Documentation section and Datasheet.md Construction section: 1. Purpose and Scope, 2. Inputs and Sources, 3. Assumptions and Boundary Conditions, 4. Methodology, 5. Flow Meter Sizing Calculations, 6. Accuracy/Uncertainty Analysis, 7. Proving Basis, 8. Sensitivity Analysis, 9. Results Summary, 10. Implications for Other Deliverables, 11. References, 12. Revision History, Appendices | Draft calculation report |
| 8.2 | Include executive summary with key results per Specification.md Documentation requirements: selected meter sizes (rail and marine), pressure drops, turndown ratios, combined uncertainties, verification of accuracy compliance, proving method and frequency, acceptance criteria; summary should be traceable to procurement and installation decisions | Executive summary |
| 8.3 | Document implications for other deliverables per Specification.md REQ-16: **DEL-12.01 implications**: Meter sizes to be shown in drawings, straight-run requirements (cite manufacturer or standard; e.g., "10D upstream, 5D downstream"), proving connection requirements (prover type, connection locations, isolation); **DEL-12.02 cross-check**: Verify calculation results meet specification; flag any conflicts requiring specification update; **DEL-12.04 implications**: Flow ranges, accuracy class, pressure drops to be documented in data sheets; **DEL-12.05 implications**: Acceptance criteria for FAT (accuracy verification), SAT (installation verification), proving (meter factor acceptance) | Implications documentation |
| 8.4 | Include references per Specification.md Documentation section: cite all standards applied (API MPMS chapters, OIML R117, ISO GUM, Measurement Canada), project documents (ER Vol 2 Part 2 clauses, DEL-12.02 sections, design basis), vendor data (manufacturer data sheets, sizing tools), technical literature (if assumptions based on published data) | References section |
| 8.5 | Include revision history per Specification.md REQ-19: Revision number (00 for initial), date, description of changes, originator name, checker name, approver name | Revision history |
| 8.6 | Include appendices as needed: Appendix A (detailed calculation sheets), Appendix B (vendor sizing tool outputs if used), Appendix C (uncertainty budget detailed tables), Appendix D (sensitivity analysis detailed results), Appendix E (standard excerpts if referenced) | Appendices |

**Output:** Complete calculation report ready for independent check

**Verification:** Report structure per Specification.md Documentation section; all required sections present per REQ-01; implications for other deliverables documented per REQ-16

---

### Step 9: Independent Check and Issue

**Objective:** Independent engineer checks all calculations; resolve comments; obtain approvals; issue per Specification.md REQ-18.

| Action | Description | Output |
|--------|-------------|--------|
| 9.1 | Independent checker reviews calculation report for completeness per Specification.md Verification Methods: verify all sections present (purpose, inputs, assumptions, methodology, calculations, sensitivity, results, implications, references); verify documentation quality (inputs sourced, assumptions stated, TBDs flagged) | Completeness check |
| 9.2 | Checker verifies inputs per Specification.md REQ-04, REQ-20: verify all inputs documented with sources (ER clauses, specification sections, design basis, vendor data); verify inputs are reasonable (flow rates consistent with facility throughput, product properties reasonable for canola oil); verify assumptions stated with rationale; verify TBDs flagged with source needed | Input verification |
| 9.3 | Checker verifies methodology per Specification.md REQ-11, REQ-12, REQ-13: verify sizing methodology is appropriate (manufacturer tools or first-principles); verify uncertainty methodology cites applicable standard (API MPMS Chapter 13, OIML R117, ISO GUM); verify proving methodology cites standard (API MPMS Chapter 4, OIML R117, Measurement Canada); verify methodology is correctly applied | Methodology verification |
| 9.4 | Checker verifies calculations: re-perform key calculations independently (meter sizing, pressure drop, uncertainty propagation, prover sizing); verify calculation logic is correct; check arithmetic; verify formulas are correct; spot-check calculation results | Calculation verification |
| 9.5 | Checker verifies unit consistency per Specification.md REQ-22: verify units are consistent throughout calculations; verify unit conversions are shown and correct (e.g., m³/h to kg/h using density, bar to kPa, °C to K if needed); verify final results have correct units | Unit consistency check |
| 9.6 | Checker verifies results reasonableness: verify meter sizes are reasonable for flow rates; verify pressure drops are acceptable (not excessive); verify turndown ratios are achievable; verify combined uncertainties are reasonable (not unrealistically tight or loose); verify results support OBJ-2 and OBJ-10 per Specification.md REQ-06, REQ-07 | Results reasonableness check |
| 9.7 | Checker documents check comments: prepare independent check comment list with comment number, calculation section, comment description, severity (critical/major/minor if calculation error; advisory if suggestion for clarity), recommended action | Check comment list |
| 9.8 | Originator and checker coordinate to resolve comments: review comments together, agree on resolutions (correct calculation errors, clarify documentation, revise assumptions), originator implements agreed resolutions, checker verifies resolutions | Comment resolution |
| 9.9 | Checker records independent check completion per Specification.md REQ-18: date, checker name, summary of check (sections reviewed, key items verified), confirmation that all comments are resolved or dispositioned, checker signature confirming calculations are verified | Independent check record |
| 9.10 | Obtain approval signatures per project procedures (TBD; ER Vol 2 Part 1): originator signature (confirming calculation accuracy), checker signature (confirming independent check completion), approver signature (authorizing issue; typically Process Lead or Engineering Manager) | Approval signatures |
| 9.11 | Issue per project document control process (TBD; ER Vol 2 Part 1): submit to document management system, assign document number per project numbering system, assign revision (00 for initial issue), distribute to required recipients (project team, DEL-12.01 drawing originator, DEL-12.04 data sheet originator, procurement if applicable; distribution list TBD) | Document management system entry; distribution |
| 9.12 | Place issued copy in deliverable folder structure: place issued copy in `2_Checking/` for review issue or `3_Issued/` for final issue — per project convention and lifecycle state | Filed issue copy |
| 9.13 | Update deliverable status: if issuing for review, update `_STATUS.md` to CHECKING with note "Issued for Review, Rev 00, Date YYYY-MM-DD"; if issuing final, update `_STATUS.md` to ISSUED with note "Issued, Rev 00, Date YYYY-MM-DD" — record issue date, revision, and issue purpose in status history | Status update |

**Output:** Independently checked calculation report with all comments resolved; check record with checker signature; issued calculation with all approvals; deliverable status updated

**Verification:** Independent check complete per Specification.md REQ-18; check record documents verification; all approval signatures obtained; calculation issued per document control procedures

---

## Verification

### Verification Activities

| Activity | Requirement Verified | Method | Record |
|----------|---------------------|--------|--------|
| Artifact completeness check | REQ-03 | Checklist against Decomposition:358 — verify flow meter sizing, accuracy/uncertainty calculations, proving calculations are present | Document index; Step 8 report assembly |
| Service coverage check | REQ-02 | Verify both rail unloading and marine loading services addressed | Calculation report; Step 1 case definitions |
| Input documentation check | REQ-04, REQ-05, REQ-20 | Verify all inputs documented with sources; assumptions stated with rationale; TBDs flagged | Input table review Step 2.6; assumption table review Step 2.7; check record Step 9.2 |
| Methodology verification | REQ-11, REQ-12, REQ-13 | Verify sizing, uncertainty, and proving methodologies cite applicable standards | Methodology review Step 9.3; standard citations in calculation report |
| Technical correctness check | REQ-06, REQ-07, REQ-09, REQ-10 | Independent checker verifies calculations: re-perform key calculations, verify logic, check arithmetic, verify results | Independent check Step 9.4; check record Step 9.9 |
| Unit consistency check | REQ-22 | Verify units consistent throughout; unit conversions shown and correct | Unit check Step 9.5; check record |
| Objective alignment check | REQ-06, REQ-07 | Verify sizing supports OBJ-2 throughput; verify uncertainty meets OBJ-10 accuracy | Results review Step 9.6; objective verification Step 3.5, Step 4.4 |
| Specification consistency check | REQ-08, REQ-15 | Verify calculation inputs align with DEL-12.02; verify results meet specification | Cross-check Step 6; check record |
| Sensitivity analysis check | REQ-23, REQ-24 | Verify sensitivity analysis performed; critical assumptions identified | Sensitivity review Step 7; check record |
| Downstream implications check | REQ-16 | Verify implications for DEL-12.01, DEL-12.04, DEL-12.05 documented | Implications review Step 8.3; calculation report Section 10 |

### Acceptance Criteria

| Criterion | Verification Method | Source |
|-----------|---------------------|--------|
| All three calculation types present | Document index review; Step 8 | Specification.md REQ-03; Decomposition:358 |
| Both services addressed | Case definition review Step 1; calculation report sections | Specification.md REQ-02 |
| Inputs traceable to sources | Input table review Step 2.6; check record Step 9.2 | Specification.md REQ-04, REQ-20 |
| Assumptions stated with rationale | Assumption table review Step 2.7; check record Step 9.2 | Specification.md REQ-05, REQ-20 |
| Methodology cites standards | Methodology section review; check record Step 9.3 | Specification.md REQ-11, REQ-12, REQ-13 |
| Calculations verified by independent check | Check record Step 9.9 with checker signature | Specification.md REQ-18 |
| Units consistent | Unit check Step 9.5; check record | Specification.md REQ-22 |
| Sizing supports OBJ-2 throughput | Throughput verification Step 3.6; results review Step 9.6 | Specification.md REQ-06 |
| Uncertainty meets OBJ-10 accuracy | Accuracy verification Step 4.4; results review Step 9.6 | Specification.md REQ-07 |
| Results meet DEL-12.02 specification | Cross-check Step 6; check record | Specification.md REQ-08, REQ-15 |
| Sensitivity analysis performed | Sensitivity analysis section review Step 7 | Specification.md REQ-23, REQ-24 |
| Implications documented | Implications section review Step 8.3 | Specification.md REQ-16 |

### Sign-off Requirements

| Role | Responsibility | Verification | Source |
|------|----------------|--------------|--------|
| Originator | Technical content accuracy; input and assumption documentation; calculation correctness | Originator signature on calculation report confirming accuracy | ASSUMPTION; project quality procedures |
| Checker | Independent verification; re-perform calculations; methodology appropriateness; results reasonableness | Checker signature on calculation report and check record confirming verification complete | ASSUMPTION; project quality procedures; Specification.md REQ-18 |
| Approver | Authorization for issue; confirm calculations satisfy ER and project objectives | Approver signature on calculation report authorizing issue | TBD; ER Vol 2 Part 1 |

## Records

### Documentation Outputs

| Output | Description | Source |
|--------|-------------|--------|
| Flow Meter Sizing Calculation | Calculation report section documenting meter size selection for rail unloading and marine loading; includes flow rates, product properties, meter size, pressure drop, turndown, throughput verification | Decomposition:358; Specification.md REQ-03, REQ-06, REQ-09, REQ-10; Step 3 |
| Accuracy / Uncertainty Calculation | Calculation report section documenting uncertainty budget, uncertainty components, propagation methodology, combined uncertainty, accuracy verification | Decomposition:358; Specification.md REQ-03, REQ-07, REQ-12; Step 4 |
| Proving Calculation | Calculation report section documenting proving method, prover sizing, frequency, acceptance criteria | Decomposition:358; Specification.md REQ-03, REQ-07, REQ-13; Step 5 |
| Sensitivity Analysis | Calculation report section documenting parameter sensitivities and critical assumptions | Specification.md REQ-23, REQ-24; Step 7 |
| Independent Check Record | Record documenting independent check completion with checker signature, check comments, resolutions | Specification.md REQ-18; Step 9.9 |

### Record Management

| Attribute | Value | Source |
|-----------|-------|--------|
| Filing Location (Working) | `1_Working/DEL-12.03_Metering_Design_Calculations/` | Current location |
| Filing Location (Review) | `2_Checking/` (for review issue) | Project convention |
| Filing Location (Issued) | `3_Issued/` (for final issue) | Project convention |
| Document Management System | Per project document control procedures (TBD; ER Vol 2 Part 1) | TBD |
| Retention Period | Per project quality procedures; typically life of facility for custody transfer calculations | TBD |
| Format | Electronic files (Excel, MathCAD, PDF, or per project standard); electronic distribution | ASSUMPTION |
| Backup and Version Control | Per project IT procedures; calculation files under version control in document management system | TBD |

### Status Transitions

Status transitions are managed per `_STATUS.md` in the deliverable folder:

| From State | To State | Trigger | Responsible |
|------------|----------|---------|-------------|
| INITIALIZED | IN_PROGRESS | Calculation development commences (Step 1) | Process Engineer (originator) |
| IN_PROGRESS | CHECKING | Calculation submitted for independent check (Step 9) | Process Engineer (originator) |
| CHECKING | IN_PROGRESS | Check comments require revision | Process Engineer (originator) |
| CHECKING | ISSUED | Check complete; approvals obtained; calculation issued (Step 9.13) | Approver |

**Note:** Status state transitions are recorded in `_STATUS.md` with date, state change, and brief description. Detailed issue history is maintained in the document management system.

### Revision Management

| Revision | Purpose | Typical Trigger | Approval Required |
|----------|---------|-----------------|-------------------|
| 00 | Initial issue | First issue for review or for project use | Process Lead or Engineering Manager |
| A, B, C... | Subsequent revisions incorporating review comments or design changes | Review comments received, design basis changes, vendor data updates | Process Lead |
| As-built | Final as-built revision incorporating actual installed equipment | Construction complete; vendor data finalized; as-built verification | As-built process per project procedures (TBD) |

**Note:** Revision numbering convention TBD from ER Vol 2 Part 1 project document control procedures.
