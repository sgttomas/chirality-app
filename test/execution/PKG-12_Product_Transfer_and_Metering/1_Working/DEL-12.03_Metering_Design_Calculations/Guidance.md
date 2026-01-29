# Guidance: DEL-12.03 Metering Design Calculations

## Purpose

This guidance document supports the development of **Metering Design Calculations** for **PKG-12 Product Transfer & Metering**.

DEL-12.03 provides the engineering basis and sizing/verification calculations for custody transfer metering (Source: Decomposition:358). The deliverable is classified as a **Calculation** under the **Process** discipline, produced by the **D&B Contractor**.

### Deliverable Intent

The metering design calculations serve as the engineering foundation for the entire PKG-12 metering deliverable set:

- **Engineering basis for meter selection** — calculations demonstrate selected meter technology, size, and configuration meet project requirements
- **Accuracy verification** — uncertainty analysis confirms custody transfer accuracy requirements are achievable
- **Proving methodology** — calculations define proving approach and acceptance criteria
- **Downstream deliverable support** — calculation results drive DEL-12.01 drawings (meter sizes, straight-runs, proving connections), DEL-12.04 data sheets (flow ranges, accuracy class), and DEL-12.05 test records (acceptance criteria)

These calculations demonstrate that the metering design can meet project objectives (OBJ-2 Throughput Capacity and OBJ-10 Custody Transfer Accuracy) and provide the technical justification for procurement and installation decisions.

### Downstream Use

The calculation results are used by:
- **Engineering** — DEL-12.01 drawings incorporate meter sizes, straight-run requirements, proving connections from calculations
- **Procurement** — vendor bid packages specify meter sizes, flow ranges, accuracy requirements from calculations
- **Data sheets** — DEL-12.04 data sheets document parameters validated by calculations
- **Testing** — DEL-12.05 test records use acceptance criteria from calculations (accuracy verification, proving acceptance)
- **Operations** — proving procedures and acceptance criteria from calculations guide ongoing operational verification

## Principles

### Calculation Development Rationale

| Principle | Rationale |
|-----------|-----------|
| Objective Demonstration | Calculations must demonstrate metering design meets OBJ-2 (1,000,000 MT/a throughput without flow constraints) and OBJ-10 (custody transfer accuracy with defined uncertainty) (Source: Decomposition:781, 789; Specification.md REQ-06, REQ-07); calculations are the primary evidence that objectives can be achieved |
| Traceability | All inputs, assumptions, and methods must be clearly stated with sources to support review, audit, and future reference (per Specification.md REQ-04, REQ-05); traceability enables verification that calculations are based on correct requirements and enables future updates when requirements change |
| Auditability | Calculation structure should enable independent check (Specification.md REQ-18) and future reference; clear documentation of methodology and assumptions enables checker to verify correctness and enables future engineers to understand basis |
| No Invention | Where ER clauses or design basis are unavailable, mark requirements as TBD with source needed rather than assuming values (per Specification.md REQ-05); assumed values can lead to incorrect sizing or performance shortfalls; TBD items flag gaps for resolution |
| Standard-Based Methodology | Use recognized custody transfer standards (API MPMS, OIML R117, ISO GUM, Measurement Canada) for methodology (per Specification.md REQ-11, REQ-12, REQ-13); standard-based approach ensures calculations follow industry best practices and are defensible to client and regulators |

### Calculation Methodology Principles

| Principle | Application |
|-----------|-------------|
| Flow Meter Sizing | Size meters to accommodate design flow range with appropriate margin; consider turndown ratio (accuracy across flow range from minimum to maximum), pressure drop (impact on system hydraulics), and product properties (viscosity, density affect meter performance); verify sizing supports OBJ-2 throughput (per Specification.md REQ-06, REQ-09, REQ-10) |
| Uncertainty Analysis | Apply recognized uncertainty methodology (API MPMS Chapter 13, OIML R117, ISO GUM) for custody transfer uncertainty budgeting (per Specification.md REQ-12); identify all uncertainty components (meter, temperature, pressure, density, proving), quantify individual uncertainties, propagate uncertainties using root-sum-squares or Monte Carlo, verify combined uncertainty meets accuracy requirement (per Specification.md REQ-07) |
| Proving Basis | Select proving method appropriate for custody transfer requirements (in-line prover for high-accuracy applications, portable prover for flexibility, master meter for specific applications); define acceptance criteria per applicable standard (API MPMS Chapter 4, OIML R117, Measurement Canada); proving methodology must be operationally feasible and cost-effective (per Specification.md REQ-13) |

### Objective Alignment

| Objective | Calculation Guidance |
|-----------|---------------------|
| OBJ-2 Throughput Capacity (1,000,000 MT/a) | Demonstrate meter sizing accommodates 1,000,000 MT/a throughput without excessive constraints (per Specification.md REQ-06): verify meter flow capacity accommodates design flow rates for rail unloading (facility has 32 unloading stations per Decomposition:44; cumulative flow rate depends on number of cars unloading concurrently) and marine loading (high flow rates for rapid vessel loading); verify meter pressure drop does not excessively constrain system hydraulics (coordinate with PKG-14 piping hydraulics); verify meter turndown ratio accommodates flow variations from start-up to peak flow without accuracy degradation |
| OBJ-10 Custody Transfer Accuracy (Commercial Transactions) | Demonstrate uncertainty budget meets custody transfer requirements (per Specification.md REQ-07): develop uncertainty budget per applicable standard (API MPMS Chapter 13, OIML R117, or other; TBD from ER and DEL-12.02); calculate combined expanded uncertainty; verify combined uncertainty meets accuracy requirement from DEL-12.02 specification (e.g., ±0.15%, ±0.25%; TBD); define proving methodology and acceptance criteria that maintain accuracy over time; proving frequency and acceptance criteria must be achievable operationally |

## Considerations

### Sizing Calculation Factors

Factors affecting flow meter sizing (per Specification.md REQ-06, REQ-09, REQ-10, REQ-11):

| Factor | Consideration |
|--------|---------------|
| Flow Range | **Design flow rate**: Maximum anticipated flow rate for each service (rail unloading, marine loading); drives meter size selection; **Normal flow rate**: Typical operating flow rate; meter should have good accuracy at normal flow; **Minimum flow rate**: Lowest measurable flow rate; defines turndown requirement; **Maximum flow rate**: Peak flow rate; meter must handle without damage or excessive pressure drop; TBD from ER Vol 2 Part 2, DEL-12.02, or design basis |
| Product Properties | **CSD canola oil density**: Affects volumetric/mass conversion; typical canola oil density ~0.91-0.92 g/cm³ at 15°C (ASSUMPTION; TBD from ER Vol 2 Part 2 or product specs); density varies with temperature (requires compensation or measurement); **Viscosity**: Affects meter technology selection and performance; typical canola oil viscosity ~30-70 cP at 20°C, decreases with temperature (ASSUMPTION; TBD); Coriolis meters insensitive to viscosity; turbine meters affected by viscosity; **Temperature**: Product temperature affects density and viscosity; temperature range TBD from ER Vol 2 Part 2 |
| Pressure Drop | **Meter pressure drop**: Calculate pressure drop at maximum flow rate; different meter technologies have different pressure drops (Coriolis typically higher, ultrasonic lower); **System impact**: Pressure drop must not excessively constrain system hydraulics; coordinate with PKG-14 piping hydraulics to ensure available pressure accommodates metering pressure drop; **Pump capacity**: Excessive pressure drop may require larger pumps or limit flow capacity |
| Turndown Ratio | **Definition**: Ratio of maximum measurable flow to minimum measurable flow while maintaining specified accuracy; **Requirement**: Typical custody transfer meters 10:1 to 20:1 turndown (ASSUMPTION; TBD from DEL-12.02); Coriolis meters may achieve 50:1 or higher; **Verification**: Calculate accuracy at minimum flow, normal flow, and maximum flow; verify accuracy remains within specification across entire range; **Low-flow accuracy**: Some meters have degraded accuracy at low flows; verify minimum flow is within meter's accurate range |
| Meter Technology | **Coriolis mass flowmeter**: Direct mass measurement; high accuracy (±0.10% to ±0.15%); minimal straight-run (3D-5D); insensitive to viscosity; higher cost and pressure drop; **Ultrasonic flowmeter**: Volumetric measurement; good accuracy (±0.15% to ±0.5%); moderate straight-run (10D-20D); suitable for large sizes; lower pressure drop; **Turbine flowmeter**: Volumetric measurement; good accuracy (±0.15% to ±0.25% when proved); longer straight-run (10D-20D or more); viscosity-sensitive; moving parts require maintenance; **Positive displacement**: Volumetric measurement; high accuracy (±0.1%); no straight-run requirement; suitable for low flows; higher pressure drop; mechanical complexity; **Selection**: May be specified in DEL-12.02 or left open for vendor proposal; calculations should address selected or assumed technology |

### Accuracy / Uncertainty Calculation Factors

Factors affecting uncertainty analysis (per Specification.md REQ-07, REQ-12):

| Factor | Consideration |
|--------|---------------|
| Meter Base Uncertainty | **Source**: Manufacturer specification or selected accuracy class (e.g., OIML R117 accuracy class 0.5 = ±0.5%); **Varies with flow rate**: Meters typically have tighter accuracy at higher flow rates; accuracy may degrade at low flows; verify accuracy across entire turndown range; **Repeatability**: Meter repeatability (typically ±0.05% to ±0.1%) is separate from accuracy; both contribute to uncertainty |
| Temperature Compensation Uncertainty | **Temperature measurement**: Temperature transmitter accuracy (e.g., RTD Pt100 ±0.1°C; TBD from DEL-12.02); **Temperature effect on density**: Canola oil density decreases with temperature; typical coefficient ~0.0007 g/cm³ per °C (ASSUMPTION; TBD from product data); **Compensation calculation**: Temperature correction applied to convert measured volume at flowing temperature to standard reference temperature (e.g., 15°C); error in temperature measurement propagates to final result; **Uncertainty contribution**: Calculate uncertainty contribution from temperature measurement error and density-temperature correlation uncertainty |
| Pressure Compensation Uncertainty | **Pressure measurement**: Pressure transmitter accuracy (e.g., ±0.1% of span; TBD from DEL-12.02); **Pressure effect**: Vegetable oils relatively incompressible; pressure compensation may be negligible (TBD; verify from product compressibility data); **Applicable for volumetric meters**: Coriolis mass meters do not require pressure compensation; ultrasonic and turbine volumetric meters may require pressure compensation if compressibility is significant |
| Density Compensation Uncertainty | **Coriolis meters**: Measure density directly; density measurement uncertainty per manufacturer specification (e.g., ±0.001 g/cm³); **Volumetric meters**: Require density input for mass calculation; density may be measured (online densitometer), assumed (fixed value with uncertainty), or calculated (temperature-compensated correlation); **Uncertainty contribution**: Density uncertainty propagates directly to mass flow uncertainty for volumetric meters |
| Proving Uncertainty | **Prover uncertainty**: In-line prover uncertainty (typical ±0.02% to ±0.05%); portable prover uncertainty (typical ±0.05% to ±0.1%); master meter uncertainty (depends on master meter accuracy class); **Proving as reference**: Proving establishes meter factor; prover uncertainty contributes to overall measurement uncertainty; **Traceability**: Prover calibration traceability to national standards (Measurement Canada, NIST) affects prover uncertainty |
| Combined Uncertainty Propagation | **Methodology**: API MPMS Chapter 13 prescribes root-sum-squares (RSS) for combining independent uncertainties: U_combined = sqrt(U1² + U2² + U3² + ...); ISO GUM provides general framework; OIML R117 provides metering-specific approach; **Coverage factor**: Apply coverage factor (typically k=2 for 95% confidence level) to combined standard uncertainty to obtain expanded uncertainty: U_expanded = k × U_combined; **Result verification**: Verify expanded uncertainty meets accuracy requirement from DEL-12.02 (e.g., if requirement is ±0.15%, expanded uncertainty must be ≤±0.15%) |

### Proving Calculation Factors

Factors affecting proving methodology and calculations (per Specification.md REQ-13):

| Factor | Consideration |
|--------|---------------|
| Proving Method Selection | **In-line prover (sphere or piston)**: Provides continuous proving capability; higher accuracy (typical ±0.02% to ±0.05%); suitable for high-value custody transfer (marine loading export); requires significant space and capital cost; requires operational expertise; **Portable prover**: Lower capital cost; flexible (one prover can prove multiple meters); requires operational coordination for proving events; typical accuracy ±0.05% to ±0.1%; suitable for lower-volume services (rail unloading); **Master meter**: Uses calibrated reference meter to prove operational meter; requires maintaining master meter calibration; suitable when provers are impractical; **Selection criteria**: Accuracy requirements (OBJ-10), operational constraints (proving frequency, operational impact), space availability (coordinate with DEL-12.01 drawings), cost (capital and operational) |
| Prover Sizing | **In-line prover volume**: Calculate required prover displacement volume based on meter flow rate and proving procedure; typical proving time 30-120 seconds (TBD; per API MPMS Chapter 4 or operational requirements); prover volume = flow rate × proving time / number of proving runs; **Prover repeatability**: In-line prover must achieve specified repeatability (typical ±0.02% to ±0.05%); repeatability depends on prover volume, meter flow rate, pulse resolution, and operational factors; **Portable prover capacity**: Specify portable prover volume adequate for meter proving; typical portable provers 50-500 liters |
| Proving Frequency | **Regulatory requirements**: Measurement Canada or other regulatory authority may specify minimum proving frequency (TBD; verify from Measurement Canada regulations or ER Vol 2 Part 2); typical regulatory requirements quarterly to annually; **Operational requirements**: Proving frequency may be driven by commercial agreements (buyer/seller requirements) or operational confidence needs; **Proving schedule**: Coordinate proving frequency with operational schedule (proving during maintenance windows vs. online proving during operations); **Service-specific**: Marine loading (high-value export) may require more frequent proving than rail unloading |
| Acceptance Criteria | **Meter factor definition**: Meter factor = true volume (from prover) / indicated volume (from meter); ideal meter factor = 1.000; actual meter factor accounts for meter calibration offset; **Meter factor limits**: Define acceptable range for meter factor (e.g., 0.995 to 1.005); **Meter factor drift**: Define acceptable drift from baseline or previous proving (e.g., ±0.05%); if drift exceeds limit, meter requires re-calibration or replacement; **Proving repeatability**: Define required repeatability for proving run acceptance (e.g., ±0.02% for in-line prover, ±0.05% for portable prover); **Standard basis**: Cite API MPMS Chapter 4, OIML R117, or Measurement Canada for acceptance criteria |

### Service-Specific Considerations

Rail unloading and marine loading have different operational characteristics affecting calculations:

| Service | Considerations |
|---------|----------------|
| Rail Unloading Metering | **Multiple railcars**: Facility has 32 unloading stations (Decomposition:44); consider whether individual metering for each station or manifold with single custody transfer meter; individual metering provides car-by-car tracking but higher capital cost; manifold with single custody transfer meter reduces cost but requires operational coordination; **Batch operation**: Railcar unloading is batch operation; each car is a separate custody transfer transaction; meter may require batch totalizing capability; **Flow variation**: Unloading flow rate varies during batch (high initial rate, decreasing as railcar empties); meter must maintain accuracy across flow variation; **Proving during unloading**: Consider whether proving can be performed during unloading operations or requires dedicated proving time between batches |
| Marine Loading Metering | **High flow rates**: Vessel loading requires high flow rates to minimize vessel dwell time and maximize terminal throughput; loading rates drive meter sizing; typical bulk vessel loading 500-2000 m³/h for vegetable oil (ASSUMPTION; TBD from ER or DEL-11.03 marine loading calculations); **Continuous operation during loading**: Vessel loading is continuous operation (start-up, steady-state loading, shut-down); meter must accommodate flow profile from low flow (start-up) to peak flow (steady-state) to low flow (shut-down); **Proving capacity**: If online proving during loading is required, prover must accommodate peak loading rate; alternatively, proving may be performed before or after loading; **Loading rate control**: Meter signal may be used for loading rate control to prevent vessel overflow or loading arm breakaway (coordinate with PKG-19 controls); **High-value export**: Marine loading is final custody transfer point for export; accuracy is critical for commercial transactions; in-line prover may be justified for higher accuracy |

### Sensitivity Analysis Topics

Sensitivity analysis identifies parameters where small variations significantly impact results (per Specification.md REQ-23, REQ-24):

| Parameter | Sensitivity Check |
|-----------|-------------------|
| Flow Rate Variation | **Purpose**: Verify accuracy is maintained across turndown range from minimum to maximum flow; **Method**: Calculate accuracy (expanded uncertainty) at minimum flow, normal flow, and maximum flow; identify if accuracy degrades at low flows; **Risk**: If accuracy degrades significantly at low flows, minimum measurable flow may need to be increased or meter technology reconsidered |
| Temperature Variation | **Purpose**: Assess temperature compensation error at temperature extremes; **Method**: Calculate density correction error at minimum and maximum operating temperatures; assess impact on final mass flow uncertainty; **Risk**: If temperature range is wide and density-temperature coefficient is large, temperature compensation uncertainty may be significant contributor to combined uncertainty |
| Viscosity Variation | **Purpose**: Assess impact of viscosity variation on meter performance (relevant for turbine meters; less relevant for Coriolis); **Method**: Review manufacturer specifications for viscosity effects; assess if viscosity variation affects meter accuracy or pressure drop; **Risk**: Turbine meters may have degraded accuracy or increased pressure drop at high viscosity; Coriolis meters generally insensitive |
| Prover Volume/Uncertainty | **Purpose**: Assess impact of prover selection on combined uncertainty; **Method**: Calculate combined uncertainty with different prover accuracies (in-line ±0.02% vs. portable ±0.1%); assess if prover uncertainty is significant contributor; **Risk**: If prover uncertainty is large relative to meter uncertainty, overall custody transfer accuracy may not meet requirement; may justify in-line prover over portable prover |
| Density Assumption | **Purpose**: Assess impact of assumed density on mass flow accuracy (for volumetric meters without density measurement); **Method**: Calculate mass flow error for ±X% density variation; assess if density uncertainty is acceptable or if density measurement is required; **Risk**: If density varies significantly and is not measured, mass flow uncertainty may exceed requirement; may require online density measurement |

## Trade-offs

### Competing Design Factors

| Trade-off | Options | Guidance |
|-----------|---------|----------|
| Meter Size vs. Accuracy at Low Flows | Larger meters handle higher design flow rates but may have degraded accuracy at low flows (turndown limitation); smaller meters have better low-flow accuracy but may not accommodate peak flows | Size for expected flow range; verify accuracy across entire turndown from minimum to maximum flow; if single meter cannot achieve required accuracy across range, consider dual-range metering (parallel meters for different flow ranges) or accept reduced accuracy at flow extremes |
| Accuracy vs. Pressure Drop | Some meter technologies (Coriolis) achieve higher accuracy but have higher pressure drop; other technologies (ultrasonic) have lower pressure drop but may have lower accuracy | Balance accuracy requirement (OBJ-10) against system hydraulic constraints; coordinate with PKG-14 piping hydraulics to verify available pressure drop accommodates meter selection; if pressure drop is critical constraint, may accept lower accuracy or larger meter size to reduce pressure drop |
| Proving Method vs. Cost and Complexity | In-line provers provide higher accuracy and continuous proving capability but require significant capital cost, space, and operational expertise; portable provers are lower cost and flexible but have lower accuracy and require operational coordination | Evaluate based on accuracy requirements, operational requirements, space constraints, and budget; in-line prover typical for high-value custody transfer (marine loading export); portable prover acceptable for rail unloading if accuracy requirement is less stringent; master meter option if provers are impractical |
| Conservative Assumptions vs. Over-Sizing | Using conservative assumptions (high safety factors, worst-case conditions) reduces risk but may lead to unnecessary over-sizing and cost; using realistic assumptions optimizes sizing but requires confidence in input data | Use realistic inputs based on best available data; document assumptions clearly; perform sensitivity analysis to assess impact of assumption variations; conservative assumptions justified where uncertainty is high or consequences of under-sizing are severe; over-sizing has cost penalty and may degrade low-flow accuracy |
| Standardization vs. Service-Specific Optimization | Using identical meter technology and sizes for rail unloading and marine loading simplifies procurement (single vendor, volume discount), spares inventory (common parts), and maintenance training (single technology) but may not optimize performance for each service | Evaluate standardization benefits (procurement, spares, training, lifecycle cost) vs. service-specific optimization (performance, cost for each service); different flow ranges for rail and marine likely require different meter sizes even if same technology; technology commonality where feasible is beneficial; accept different sizes where required by flow rates |

### Unresolved Trade-offs (TBD)

The following trade-offs require resolution during calculation development based on ER requirements, DEL-12.02 specification, and operational considerations:

- **Specific meter technology selection** (Coriolis vs. ultrasonic vs. turbine vs. positive displacement) — requires ER review, DEL-12.02 specification review, and vendor input; affects accuracy, pressure drop, straight-run, proving, and cost; may be technology-neutral specification allowing vendor proposals
- **Proving methodology and frequency** (in-line prover vs. portable prover; monthly vs. quarterly vs. semi-annually vs. annually) — requires ER review, Measurement Canada compliance verification, and operational input; affects capital cost, operational complexity, and accuracy confidence
- **Accuracy class requirements** (±0.10% vs. ±0.15% vs. ±0.25%) — requires ER review and cost-benefit analysis; tighter accuracy increases cost; accuracy should be appropriate for transaction value and throughput
- **Flow rate assumptions** — rail unloading and marine loading design flow rates TBD from ER Vol 2 Part 2 or DEL-10.03/DEL-11.03 calculations; flow rates are critical sizing inputs
- **Product property data** (density vs. temperature, viscosity vs. temperature) — TBD from ER Vol 2 Part 2 or product specifications; affects temperature compensation and meter technology selection

## Examples

### Calculation Content Reference

The anticipated artifacts provide guidance on expected calculation content (Source: Decomposition:358; Datasheet.md Construction section):

| Artifact | Expected Content |
|----------|------------------|
| Flow Meter Sizing | **Inputs**: Flow rates (design, normal, min, max) for rail unloading and marine loading; product properties (density, viscosity at operating temperature); operating pressure and temperature; **Calculations**: Meter technology selection (if not specified), meter size calculation based on flow range, pressure drop calculation at maximum flow using Darcy-Weisbach or manufacturer correlations, velocity calculation, turndown ratio verification (max flow / min flow; verify ≥ required turndown); **Results**: Selected meter sizes for rail and marine services, pressure drops, flow velocities, turndown ratios; verification that sizing supports OBJ-2 (1,000,000 MT/a throughput) |
| Accuracy / Uncertainty Calculations | **Uncertainty budget**: Table listing all uncertainty components with values and sources; **Components**: Meter base uncertainty (from manufacturer or accuracy class), temperature measurement uncertainty (transmitter accuracy), pressure measurement uncertainty (if applicable), density uncertainty (measured or assumed), proving uncertainty (prover accuracy); **Propagation**: Combine uncertainties using RSS per API MPMS Chapter 13 or OIML R117; calculate combined standard uncertainty; apply coverage factor k=2 for 95% confidence; calculate expanded uncertainty; **Results**: Combined expanded uncertainties for rail unloading and marine loading; verification that uncertainties meet accuracy requirements per DEL-12.02 and support OBJ-10 |
| Proving Calculations | **Method selection**: Rationale for selected proving method (in-line prover, portable prover, master meter) considering accuracy, cost, space, operational factors; **Prover sizing** (if in-line): Required prover volume calculation based on flow rate and proving time; prover repeatability requirement; **Proving frequency**: Rationale for proving frequency (regulatory requirement, operational requirement, or commercial requirement); **Acceptance criteria**: Meter factor limits (e.g., 0.995-1.005), meter factor drift limits (e.g., ±0.05% from baseline), proving repeatability requirement (e.g., ±0.02%); cite standard (API MPMS Chapter 4, OIML R117, Measurement Canada) |

### Typical Calculation Workflow

Recommended calculation workflow (per Procedure.md Steps):

| Step | Description | Key Outputs |
|------|-------------|-------------|
| 1. Define Cases | Identify services (rail unloading, marine loading); define operating scenarios (design, normal, min, max flow); define product properties; define temperature and pressure ranges | Case definitions |
| 2. Collect Inputs | Obtain flow rates from ER or design basis; obtain product properties from ER or product specs; obtain accuracy requirements from DEL-12.02; obtain applicable standards; document all inputs with sources; state assumptions with rationale | Input table; assumption list |
| 3. Size Meters | Select meter technology (if not specified in DEL-12.02); calculate meter size for each service based on flow range and product properties; calculate pressure drop at max flow; verify turndown ratio; verify sizing supports OBJ-2 throughput | Meter sizes; pressure drops; turndown ratios |
| 4. Uncertainty Analysis | Identify uncertainty components; quantify individual uncertainties from manufacturer specs, transmitter specs, prover specs; apply uncertainty propagation (RSS); calculate combined standard uncertainty; apply coverage factor; calculate expanded uncertainty; verify meets accuracy requirement | Uncertainty budget; combined uncertainties; verification of OBJ-10 |
| 5. Proving Basis | Select proving method; size prover if in-line prover; define proving frequency and rationale; define meter factor acceptance criteria citing standard | Proving method; prover size; frequency; acceptance criteria |
| 6. Cross-Check | Verify calculation inputs align with DEL-12.02 specification; verify results meet specification requirements; flag conflicts or TBDs | Cross-check verification; conflict identification |
| 7. Sensitivity | Perform sensitivity analysis for key parameters (flow rate, temperature, viscosity, prover uncertainty); identify critical assumptions and risks | Sensitivity analysis results; risk identification |
| 8. Document | Assemble calculation report with all sections; include executive summary with key results; document implications for DEL-12.01, DEL-12.04, DEL-12.05 | Calculation report |
| 9. Check and Issue | Independent checker verifies calculations; resolve comments; obtain approvals; issue per document control | Checked and issued calculation |

## Conflict Table

### Local Conflicts (for Human Ruling)

No conflicts identified from accessible sources at this stage.

| Conflict ID | Conflict | Source A (File § Section) | Source B (File § Section) | Impacted Sections | Proposed Authority | Human Ruling |
|-------------|----------|---------------------------|---------------------------|-------------------|-------------------|--------------|
| — | — | — | — | — | — | TBD |

### Conflict Recording Instructions

When conflicts are discovered during calculation development, record them in this table with:
- **Conflict ID:** Sequential identifier (e.g., DEL-12.03-C01)
- **Conflict:** Clear statement of the conflicting requirements or constraints
- **Source A/B:** File path and section reference for each conflicting source (e.g., "ER Vol 2 Part 2 § 5.3.2" or "DEL-12.02 Specification.md REQ-06")
- **Impacted Sections:** Which sections of DEL-12.03 documents or calculation report are affected
- **Proposed Authority:** Which source should govern (PROPOSAL label)
- **Human Ruling:** Resolution decision and date (TBD until ruled)

### Potential Conflicts to Monitor

| Potential Conflict | Trigger Condition | Sources to Compare | Impacted Documents |
|--------------------|-------------------|--------------------|--------------------|
| Accuracy requirement vs. achievable uncertainty | ER or DEL-12.02 specifies accuracy tighter than achievable uncertainty with selected meter technology and proving method | DEL-12.02 Specification.md § Requirements (accuracy) vs. DEL-12.03 uncertainty budget calculation results | Specification.md REQ-07; Procedure.md Step 4.4 |
| Flow rate vs. meter capacity | Design flow rate from ER exceeds selected meter's maximum capacity | ER Vol 2 Part 2 flow rate requirements vs. manufacturer meter capacity data | Specification.md REQ-06; Procedure.md Step 3.2 |
| Pressure drop vs. available pressure | Calculated meter pressure drop exceeds available system pressure from PKG-14 piping hydraulics | DEL-12.03 calculated pressure drop vs. PKG-14 available pressure allocation | Specification.md REQ-10/17; Procedure.md Step 3.2.3 |
| Proving frequency vs. operational schedule | Measurement Canada or ER requires quarterly proving but operational schedule allows only semi-annual maintenance windows | Measurement Canada regulations or ER Vol 2 Part 2 vs. facility operational schedule | Specification.md REQ-13; Procedure.md Step 5.3 |
| Meter technology vs. product compatibility | Selected or specified meter technology has limitations with canola oil properties | DEL-12.02 meter technology requirement vs. manufacturer compatibility statements vs. product property data | Guidance.md § Considerations (Meter Technology); Procedure.md Step 3.1 |

## Cross-Document Traceability

| Document | Section | Traceability Points |
|----------|---------|---------------------|
| Datasheet.md | § Identification | DEL-12.03 identity referenced in Guidance § Purpose deliverable definition |
| Datasheet.md | § Conditions | Design context (services, product, throughput) driving Guidance § Considerations; calculation input parameters matching Guidance § Sizing/Accuracy/Proving Calculation Factors |
| Datasheet.md | § Construction | Anticipated calculation content informing Guidance § Examples; calculation methodology matching Guidance § Methodology Principles |
| Specification.md | § Scope | Inclusions/exclusions that Guidance § Purpose downstream use addresses |
| Specification.md | § Requirements | REQ-01 through REQ-24 that Guidance § Principles rationale supports; REQ-06/07 objective alignment per Guidance § Objective Alignment |
| Specification.md | § Standards | Custody transfer standards informing Guidance § Methodology Principles (API MPMS, OIML R117, ISO GUM) |
| Specification.md | § Verification | Verification methods aligned with Guidance § Principles (auditability) |
| Procedure.md | § Prerequisites | Inputs that Guidance § Considerations identifies (DEL-12.02, ER, standards, vendor data) |
| Procedure.md | § Step 1 | Case definition per Guidance § Service-Specific Considerations |
| Procedure.md | § Step 2 | Input collection per Guidance § Considerations (product properties, operating conditions) |
| Procedure.md | § Step 3 | Sizing per Guidance § Sizing Calculation Factors and § Methodology Principles |
| Procedure.md | § Step 4 | Uncertainty analysis per Guidance § Accuracy/Uncertainty Calculation Factors and § Methodology Principles |
| Procedure.md | § Step 5 | Proving per Guidance § Proving Calculation Factors and § Methodology Principles |
| Procedure.md | § Step 7 | Sensitivity analysis per Guidance § Sensitivity Analysis Topics |
| Procedure.md | § Step 9 | Independent check per Guidance § Principles (auditability) |
| DEL-12.01 | Drawings | Drawings implement calculation results per Guidance § Purpose (downstream use) — meter sizes, straight-runs, proving connections |
| DEL-12.02 | Specification | Specification provides performance requirements per Guidance § Considerations — accuracy, turndown, flow range as calculation inputs |
| DEL-12.04 | Data Sheets | Data sheets document calculation-validated parameters per Guidance § Purpose (downstream use) — sizes, flow ranges, accuracy class |
| DEL-12.05 | Test Records | Test records use calculation-derived acceptance criteria per Guidance § Purpose (downstream use) — FAT/SAT accuracy, proving criteria
