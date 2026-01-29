# Guidance: DEL-12.02 Metering Technical Specification

## Purpose

This guidance document supports the development of the **Metering Technical Specification** for **PKG-12 Product Transfer & Metering**.

DEL-12.02 defines performance, materials, and workmanship requirements for custody transfer metering per Employer's Requirements (Source: Decomposition:357). The deliverable is classified as a **Specification** under the **Process** discipline, produced by the **D&B Contractor**.

### Deliverable Intent

The metering technical specification serves as the contract-aligned technical baseline that drives all downstream PKG-12 deliverables:

- **DEL-12.01 Metering Design Drawing Set** — drawings implement metering arrangements, installation requirements, and proving connections per this specification
- **DEL-12.03 Metering Design Calculations** — calculations verify meter sizing, flow capacity, and performance per this specification
- **DEL-12.04 Metering Data Sheet Package** — data sheets document equipment parameters and specifications per this specification
- **Procurement** — vendor bid packages and purchase orders reference this specification
- **DEL-12.05 Metering Installation & Test Records** — QA records demonstrate compliance with this specification's requirements and acceptance criteria

This specification translates Employer's Requirements into implementable technical requirements that custody transfer metering must satisfy to meet project objectives (OBJ-2 Throughput Capacity and OBJ-10 Custody Transfer Accuracy).

### Downstream Use

The specification serves multiple purposes:
- **Engineering basis** — provides requirements for DEL-12.01 drawings and DEL-12.03 calculations
- **Procurement basis** — defines equipment to be purchased (meters, transmitters, proving equipment)
- **Installation basis** — defines installation requirements (straight-runs, orientation, mounting)
- **Testing basis** — defines FAT, SAT, calibration, and proving requirements
- **Compliance basis** — enables DEL-12.05 records to demonstrate ER compliance
- **Operational basis** — defines proving frequency and operational requirements

## Principles

### Specification Development Rationale

| Principle | Rationale |
|-----------|-----------|
| Contract Alignment | The specification translates Employer's Requirements (ER Vol 2 Part 2) into implementable technical requirements; every specification clause should be traceable to an ER source or labeled TBD/ASSUMPTION (per Specification.md REQ-24) |
| Objective Support | Requirements must protect project objectives: OBJ-2 (1,000,000 MT/a throughput) by ensuring metering does not constrain flow capacity, and OBJ-10 (Custody Transfer Accuracy) by defining accuracy, proving, and uncertainty requirements (Source: Decomposition:781, 789; Specification.md REQ-09, REQ-10) |
| Testability | Every requirement must have a defined verification method (review, inspection, test, certificate) enabling DEL-12.05 compliance demonstration; untestable requirements cannot be verified (Source: Decomposition:360; Specification.md REQ-21) |
| Traceability | All requirements cite sources (ER clauses, applicable standards, or calculations); unknowns marked TBD pending ER review; inferences marked ASSUMPTION with basis (epistemic rule per Specification.md REQ-24) |
| Technology Neutrality (where appropriate) | Avoid over-specifying meter technology unless ER mandates specific technology; specify performance requirements and allow vendors to propose appropriate meter technologies that meet performance criteria |

### Custody Transfer Metering Principles

Custody transfer metering for commercial transactions requires specific attention to measurement quality:

| Principle | Application |
|-----------|-------------|
| Accuracy and Uncertainty | Define accuracy class (e.g., ±0.15%, ±0.25%, TBD from ER) and uncertainty budget appropriate for custody transfer commercial transactions; accuracy affects revenue/cost for both buyer and seller; typical custody transfer accuracy ranges from ±0.15% to ±0.5% depending on product value and transaction volume (ASSUMPTION; TBD verification from ER Vol 2 Part 2 or Measurement Canada requirements) |
| Repeatability | Define repeatability requirements (typically ±0.05% to ±0.1%) that enable consistent measurement over time; poor repeatability leads to disputes even if average accuracy is acceptable; repeatability is critical for proving verification |
| Proving | Define proving methodology (in-line prover, portable prover, or master meter) that enables periodic verification of meter accuracy without removing meter from service; proving frequency depends on regulatory requirements, operational requirements, and meter technology (typical range: quarterly to annually; TBD from ER or Measurement Canada) |
| Compensation | Define temperature, pressure, and density measurement requirements for volume/mass correction; CSD canola oil density and viscosity vary with temperature; accurate compensation is essential for custody transfer measurement; coordinate with meter technology selection (Coriolis mass meters may not require density compensation; volumetric meters typically do) |

### Objective Alignment

| Objective | Specification Guidance |
|-----------|----------------------|
| OBJ-2 Throughput Capacity (1,000,000 MT/a) | Specify flow ranges that accommodate 1,000,000 MT/a without meter constraints (per Specification.md REQ-09); meter sizing must accommodate design flow rates for both rail unloading and marine loading per DEL-12.03 calculations; avoid excessive turndown ratios (e.g., 100:1) that may degrade accuracy at low flows; typical custody transfer meter turndown is 10:1 to 20:1 (ASSUMPTION; verify from selected meter technology) |
| OBJ-10 Custody Transfer Accuracy (Commercial Transactions) | Specify accuracy class, repeatability, proving criteria, and uncertainty budget that satisfy commercial custody transfer requirements (per Specification.md REQ-10); specification must enable DEL-12.05 records to demonstrate compliance; proving requirements must be achievable operationally (e.g., quarterly proving during scheduled maintenance windows vs. online proving during operations) |
| OBJ-6 Regulatory Compliance | Ensure compliance with Measurement Canada and applicable custody transfer regulations; meters used for custody transfer in Canada may require Measurement Canada approval; specification must cite applicable regulations and define compliance requirements (TBD; ER Vol 2 Part 2) |

## Considerations

### Technology Selection Factors

Meter technology selection significantly affects specification content, installation requirements, proving approach, and cost:

| Factor | Consideration |
|--------|---------------|
| Meter Technology Options | **Coriolis mass flowmeter**: Direct mass measurement, high accuracy (±0.10% to ±0.15% typical), minimal straight-run requirements (typically 3D-5D), insensitive to viscosity and density variations, higher cost, higher pressure drop; **Ultrasonic flowmeter**: Volumetric measurement, good accuracy (±0.15% to ±0.5%), moderate straight-run requirements (10D-20D typical), suitable for large pipe sizes, lower pressure drop, moderate cost; **Turbine flowmeter**: Volumetric measurement, good accuracy (±0.15% to ±0.25% when proved), longer straight-run requirements (10D-20D or more), lower cost, moving parts require maintenance; **Positive displacement**: Volumetric measurement, high accuracy (±0.1%), no straight-run requirements, suitable for low flow rates, higher pressure drop, mechanical complexity (ASSUMPTION; typical technology characteristics; actual selection TBD from ER and vendor proposals) |
| Product Properties | CSD canola oil properties affect meter selection: **Viscosity** — vegetable oil viscosity varies with temperature; Coriolis meters handle viscosity variation well; turbine meters may be affected by viscosity; viscosity data TBD from ER Vol 2 Part 2; **Density** — density affects volumetric flow measurement and mass flow calculation; Coriolis meters measure mass directly; ultrasonic and turbine meters measure volume and require density compensation; density vs. temperature data TBD; **Temperature** — operating temperature range affects meter materials, seals, and calibration; temperature measurement is critical for volume/mass compensation; temperature range TBD from ER Vol 2 Part 2; **Corrosivity** — vegetable oils generally non-corrosive; stainless steel or carbon steel construction typically acceptable; food-grade materials may be required (TBD) |
| Flow Range | Rail unloading and marine loading have different flow profiles: **Rail unloading** — multiple railcars unloaded simultaneously or sequentially; flow rate depends on unloading pump capacity and number of cars unloading concurrently; batch measurement may be required for individual car tracking; flow rates TBD from DEL-12.03; **Marine loading** — high flow rates for rapid vessel loading to minimize vessel dwell time; loading rates drive meter sizing; flow rates TBD from DEL-12.03; **Turndown** — ensure selected meter technology can accommodate flow variation from minimum to maximum flow rates for each service without degrading accuracy beyond specification limits |
| Proving Method | Proving approach affects meter technology selection and specification content: **In-line prover (sphere or piston)** — provides continuous proving capability, higher accuracy, suitable for high-value custody transfer, requires significant space and capital cost, suitable for larger pipe sizes (typically 6" and above); **Portable prover** — lower capital cost, suitable for multiple meters, requires operational coordination for proving events, typical for smaller pipe sizes or lower-value transactions; **Master meter** — uses reference meter to prove operational meter, requires calibrated master meter, suitable when in-line or portable provers are impractical; proving method selection TBD from ER Vol 2 Part 2 and operational requirements |

### Service-Specific Considerations

Rail unloading and marine loading have different operational characteristics that affect specification requirements:

| Service | Considerations |
|---------|----------------|
| Rail Unloading Metering | **Multiple railcars** — facility has 32 railcar unloading stations (Decomposition:44); consider whether individual metering for each car or manifold arrangement with single custody transfer meter is used; individual metering provides better tracking but higher capital cost; **Batch vs. totalizing** — individual car tracking may require batch measurement with car identification; totalizing acceptable if only cumulative unloading quantity is needed; **Flow rate variation** — railcar unloading rates depend on pump capacity, number of cars unloading concurrently, and railcar pressure; meter must accommodate flow variation; **Proving during unloading** — consider whether proving can be performed during unloading operations or requires dedicated proving time |
| Marine Loading Metering | **High flow rates** — vessel loading requires high flow rates to minimize vessel dwell time and maximize terminal throughput; loading rates drive meter sizing per DEL-12.03; **Meter range** — meter must accommodate vessel loading profile from start-up (low flow) through peak loading (high flow) to shut-down (low flow); **Proving capacity** — prover must accommodate peak loading rate if online proving during loading is required; **Loading rate control** — meter signal may be used for loading rate control to prevent vessel overflow or loading arm breakaway; coordinate with PKG-19 control system |

### Specification Content Considerations

Key topics that specification must address (per Datasheet.md Construction section):

| Topic | Guidance |
|-------|----------|
| Performance Requirements | Define accuracy, repeatability, turndown clearly per Specification.md REQ-06, REQ-07, REQ-08; cite source (ER clause or custody transfer standard); avoid over-specification that unnecessarily limits technology options or increases cost; typical custody transfer accuracy ±0.15% to ±0.25%, repeatability ±0.05% to ±0.1%, turndown 10:1 to 20:1 (ASSUMPTION; verify from ER) |
| Materials | Specify wetted materials compatible with CSD canola oil per Specification.md REQ-11; consider stainless steel (SS316, SS304) or carbon steel; specify seals and gaskets (e.g., Viton, PTFE); consider food-grade materials if required by product specifications; consider cleaning and inspection requirements for vegetable oil service |
| Installation | Reference manufacturer requirements per Specification.md REQ-13, REQ-14; allow for site-specific adaptation in DEL-12.01 drawings; specify straight-run requirements (e.g., "10D upstream, 5D downstream, or per manufacturer recommendations"); specify orientation (horizontal preferred for most meters; vertical acceptable for some); specify access for proving, calibration, maintenance |
| Proving | Specify method per Specification.md REQ-04, REQ-17; specify frequency per REQ-18 (quarterly, semi-annually, annually, or operational schedule-based); specify acceptance criteria per REQ-19 (e.g., meter factor drift <±0.05%); coordinate with operational procedures (proving during maintenance windows vs. online proving); define prover calibration traceability requirements |
| QA/Documentation | Define deliverables per Specification.md REQ-20, REQ-23 that enable DEL-12.05 compliance demonstration: calibration certificates (traceable to Measurement Canada or NIST), material certificates (MTRs), FAT protocol and results, SAT protocol and results, proving records, as-built documentation; define acceptance criteria per REQ-21 for each testable requirement |

### Interface Considerations (Coordinated Externally)

Dependencies coordinated externally per dependency mode NOT_TRACKED (see `_DEPENDENCIES.md`); interfaces defined in specification per Specification.md REQ-15:

| Interface | Coordination Need |
|-----------|-------------------|
| PKG-14 Process Piping | Piping class (material, pressure rating, temperature rating); isolation valve requirements (upstream, downstream, bypass); piping arrangement (straight-run compliance); proving connections; interface point sizes and orientations; coordinate to ensure straight-run requirements can be met in overall piping layout |
| PKG-17 Electrical Power Distribution | Power supply requirements (voltage, frequency, power consumption; e.g., 120VAC, 240VAC, 480VAC; TBD per selected equipment); area classification compliance (intrinsically safe, explosion-proof, general purpose; TBD per hazardous area classification); cable requirements (power, signal); grounding and bonding |
| PKG-19 Control Systems | Signal integration (4-20 mA analog, pulse, digital communication); communication protocols (Modbus RTU/TCP, HART, Profibus, or other; TBD); HMI requirements (display flow rate, total, density, temperature); data logging and totalizing (batch totals, cumulative totals); alarm and interlock functions (high flow, low flow, meter failure) |
| PKG-20 Field Instrumentation | Transmitter specifications (temperature transmitter: RTD Pt100, ±0.1°C; pressure transmitter: ±0.1% of span; density transmitter if applicable); signal protocols (4-20 mA, HART, digital); junction boxes and cable routing; integration with metering system; coordinate tag numbers between metering specification and instrumentation specification |

**Note:** Dependency mode is NOT_TRACKED; interfaces coordinated externally through IDC process per Procedure.md Step 6.

### Product-Specific Considerations for Canola Oil

CSD (Crude Super Degummed) canola oil has specific properties that may affect metering specification:

- **Viscosity temperature dependence** — vegetable oil viscosity decreases significantly with temperature; viscosity affects meter performance for some technologies (turbine meters sensitive to viscosity; Coriolis insensitive); viscosity data TBD from ER Vol 2 Part 2 or product specifications
- **Density temperature dependence** — canola oil density decreases with temperature; density compensation required for volumetric meters to calculate mass; density vs. temperature data TBD; Coriolis meters measure density directly
- **Temperature range** — product temperature affects fluidity and pumpability; low temperatures may require heat tracing to maintain fluidity; temperature range TBD from ER Vol 2 Part 2; affects meter materials and seal selection
- **Food-grade requirements** — canola oil is food product; food-grade materials and cleanability may be required; materials must not contaminate product; cleanout procedures may be required between product batches (TBD; ER Vol 2 Part 2)
- **Low vapor pressure** — vegetable oils have very low vapor pressure; cavitation unlikely under normal operating conditions (ASSUMPTION; verify from product data)
- **Non-corrosive** — vegetable oils generally non-corrosive; standard carbon steel or stainless steel construction acceptable (ASSUMPTION; verify material compatibility from ER or product specifications)

## Trade-offs

### Competing Design Factors

| Trade-off | Options | Guidance |
|-----------|---------|----------|
| Accuracy vs. Cost | Higher accuracy meters (e.g., ±0.10%) cost significantly more than standard custody transfer meters (e.g., ±0.25%); incremental accuracy improvement has diminishing returns | Specify accuracy appropriate for commercial custody transfer as required by ER or Measurement Canada, not unnecessarily tight; typical custody transfer accuracy ±0.15% to ±0.25% is acceptable for most applications; tighter accuracy (±0.10%) may be justified for very high-value products or large transaction volumes; balance accuracy cost against transaction value and throughput |
| Accuracy vs. Pressure Drop | Some meter technologies (Coriolis) have higher pressure drop than others (ultrasonic); higher pressure drop increases pumping cost and may limit flow capacity | Balance accuracy and pressure drop against system hydraulics per DEL-12.03; for high-flow applications (marine loading), pressure drop may drive meter technology selection; for lower-flow applications (rail unloading), accuracy may take priority; coordinate with process design to ensure available pressure drop accommodates selected meter technology |
| Standardization vs. Optimization | Using identical meter technology for rail unloading and marine loading simplifies procurement (single vendor, volume discount), spares inventory (common spare parts), and maintenance training (single technology) but may not optimize performance for each service | Consider meter technology commonality where feasible to reduce lifecycle cost; however, flow rate differences between rail and marine may require different meter sizes even if same technology; evaluate trade-off between standardization benefits (procurement, spares, training) and service-specific optimization (performance, cost); different meter technologies may be justified if flow characteristics differ significantly |
| Robustness vs. Sensitivity | More sensitive meters (Coriolis, precision turbines) achieve higher accuracy but may be less robust in harsh environments or with contaminated product; simpler meters (basic turbines) are more robust but may have lower accuracy | Consider operational environment and product quality; Fraser Surrey Terminal outdoor installation requires environmental protection (temperature extremes, moisture, corrosion); CSD canola oil is relatively clean product (ASSUMPTION; verify from product specifications); balance sensitivity and robustness based on operational requirements and maintenance capability |
| Proving Frequency vs. Operational Impact | More frequent proving (monthly, quarterly) improves measurement confidence and enables early detection of meter degradation but disrupts operations and increases maintenance cost; less frequent proving (semi-annually, annually) reduces operational impact but increases risk of undetected meter drift | Balance proving frequency against operational requirements and regulatory requirements; Measurement Canada or ER may specify minimum proving frequency; consider operational schedule (proving during scheduled maintenance windows minimizes impact); proving frequency may vary by service (more frequent for higher-value marine loading, less frequent for rail unloading) |
| In-line Prover vs. Portable Prover | In-line prover provides continuous proving capability and higher accuracy but requires significant space, capital cost, and operational complexity; portable prover reduces space and cost but requires operational coordination for proving events and may have lower accuracy | Evaluate prover selection based on service value, operational requirements, and space/cost constraints; in-line prover typical for high-value custody transfer (export loading); portable prover acceptable for lower-value or lower-throughput services (rail unloading); coordinate with DEL-12.01 drawings for space allocation |

### Unresolved Trade-offs (TBD)

The following trade-offs require resolution during specification development based on ER requirements and operational considerations:

- **Specific meter technology selection** (Coriolis vs. ultrasonic vs. turbine vs. positive displacement) — affects accuracy, pressure drop, straight-run requirements, proving approach, and cost; requires ER review and vendor input
- **Proving methodology and frequency** — in-line prover vs. portable prover; monthly vs. quarterly vs. semi-annually vs. annually; requires ER review and Measurement Canada compliance verification
- **Accuracy class requirements** — ±0.10% vs. ±0.15% vs. ±0.25%; requires ER review and cost-benefit analysis
- **Instrumentation approach** — integrated transmitters in meter vs. separate field-mounted transmitters; affects cost, accuracy, and maintenance
- **Area classification** — Division 1 vs. Division 2 vs. non-classified; affects electrical equipment selection and cost; requires ER hazardous area classification drawings
- **Temperature compensation approach** — real-time temperature measurement vs. assumed temperature vs. API temperature correction tables; affects accuracy and complexity

## Examples

### Specification Structure Reference

The anticipated artifacts provide guidance on expected specification structure (Source: Decomposition:357; Datasheet.md Construction section):

| Artifact | Expected Content |
|----------|------------------|
| Custody Transfer Flow Meter Specification | **Scope**: Rail unloading and marine loading services; CSD canola oil product; custody transfer application; **Performance**: Accuracy class (e.g., ±0.15%), repeatability (e.g., ±0.05%), flow range per DEL-12.03, turndown ratio; **Materials**: Body material, wetted parts, seals/gaskets compatible with canola oil; **Installation**: Straight-run requirements, orientation, mounting, instrument taps; **Testing**: FAT requirements, calibration, proving; **Documentation**: Data sheets, certificates, drawings |
| Metering System Specification | **System Overview**: Metering system architecture, integration with process and control systems; **Instrumentation**: Temperature transmitters (RTD Pt100, ±0.1°C), pressure transmitters (±0.1% span), density transmitters if applicable; **Proving System**: Prover type (in-line/portable), prover specifications, proving procedures, acceptance criteria; **Controls Integration**: Signal types (4-20 mA, pulse, digital), communication protocols, HMI requirements, data logging; **Quality Assurance**: Inspection and test plan (ITP), hold points, certificates, compliance matrices |

### Typical Specification Sections (ASSUMPTION)

Based on typical custody transfer metering specifications for similar services:

| Section | Typical Content |
|---------|-----------------|
| 1. Scope | Service description (rail unloading: product receipt from rail tank cars, maximum X cars concurrently; marine loading: product export to vessels, loading rate Y m³/h); product (CSD canola oil, density, viscosity, temperature); custody transfer application (commercial transactions requiring Measurement Canada approval or equivalent); system boundaries (meter inlet to meter outlet; instrumentation; proving connections) |
| 2. Technical Requirements | **Accuracy**: ±0.15% of reading (example; TBD from ER); **Repeatability**: ±0.05% (example; TBD); **Flow range**: Rail unloading 50-500 m³/h (example; TBD from DEL-12.03); Marine loading 200-2000 m³/h (example; TBD from DEL-12.03); **Turndown**: 10:1 minimum; **Materials**: Body SS316L or carbon steel (TBD); wetted parts SS316L; seals Viton or PTFE; **Environmental**: Outdoor installation, temperature range -20°C to +50°C (example; TBD from ER) |
| 3. Installation | **Straight-run**: 10D upstream, 5D downstream minimum (example; actual per manufacturer and meter technology); **Orientation**: Horizontal preferred; vertical acceptable if manufacturer approved; **Mounting**: Supported per manufacturer requirements; isolated from piping stress; **Instrument taps**: Temperature tap within 5D downstream of meter; pressure taps per manufacturer recommendations; **Access**: Clearance for proving equipment connection, meter removal, transmitter calibration |
| 4. Proving | **Method**: In-line sphere prover for marine loading (example; TBD); portable prover for rail unloading (example; TBD); **Frequency**: Quarterly for marine loading, semi-annually for rail unloading (example; TBD from Measurement Canada or ER); **Acceptance**: Meter factor drift within ±0.05% (example; TBD from applicable standard); **Prover calibration**: Traceable to Measurement Canada or NIST; calibration interval 12 months |
| 5. Testing | **FAT**: Witness test at manufacturer facility; verify accuracy, repeatability, functionality; acceptance per accuracy specification; **SAT**: Site installation verification; proving upon installation; acceptance per proving criteria; **Calibration**: Initial calibration certificate from manufacturer; periodic proving per proving frequency; re-calibration if proving fails acceptance |
| 6. Documentation | **Data sheets**: DEL-12.04 metering data sheet package; **Drawings**: DEL-12.01 installation drawings; **Calculations**: DEL-12.03 meter sizing calculations; **Certificates**: Calibration certificates, material certificates, Measurement Canada approval (if applicable); **Test records**: DEL-12.05 FAT, SAT, calibration, proving records; **Manuals**: Operation and maintenance manuals |

### Cross-Package Coordination Examples

Interfaces requiring coordination (per Specification.md REQ-15, REQ-16):

| Interface | Example Coordination Point |
|-----------|----------------------------|
| PKG-14 Process Piping | Metering specification specifies: "Provide meter inlet isolation valve and meter outlet isolation valve per P&ID; valve size and rating per piping specification; provide bypass piping around meter with isolation valves for meter removal without process shutdown; ensure straight-run compliance (minimum 10D upstream clear of fittings, valves, or obstructions)"; Piping designer coordinates to ensure layout meets straight-run requirements |
| PKG-19 Control Systems | Metering specification specifies: "Meter shall provide 4-20 mA flow signal and pulse output for totalizing; communication via Modbus RTU; integrate with DCS for HMI display (flow rate, instantaneous; total, cumulative; temperature; pressure); provide high flow alarm at 105% design flow; provide low flow alarm at 10% design flow"; Control system designer integrates signals per specification |
| PKG-20 Field Instrumentation | Metering specification specifies: "Provide temperature transmitter, RTD Pt100, range 0-100°C, accuracy ±0.1°C, 4-20 mA output with HART; provide pressure transmitter, range 0-10 bar, accuracy ±0.1% span, 4-20 mA output with HART"; Instrumentation designer coordinates transmitter specifications and junction box locations |

## Conflict Table

### Local Conflicts (for Human Ruling)

No conflicts identified from accessible sources at this stage.

| Conflict ID | Conflict | Source A (File § Section) | Source B (File § Section) | Impacted Sections | Proposed Authority | Human Ruling |
|-------------|----------|---------------------------|---------------------------|-------------------|-------------------|--------------|
| — | — | — | — | — | — | TBD |

### Conflict Recording Instructions

When conflicts are discovered during specification development, record them in this table with:
- **Conflict ID:** Sequential identifier (e.g., DEL-12.02-C01)
- **Conflict:** Clear statement of the conflicting requirements or constraints
- **Source A/B:** File path and section reference for each conflicting source (e.g., "ER Vol 2 Part 2 § 5.3.2" or "DEL-12.03 § Calculations Table Row 5")
- **Impacted Sections:** Which sections of DEL-12.02 documents are affected (e.g., "Specification.md REQ-06; Procedure.md Step 3.1")
- **Proposed Authority:** Which source should govern (PROPOSAL label)
- **Human Ruling:** Resolution decision and date (TBD until ruled)

### Potential Conflicts to Monitor

| Potential Conflict | Trigger Condition | Sources to Compare | Impacted Documents |
|--------------------|-------------------|--------------------|--------------------|
| Accuracy vs. cost | ER specifies accuracy tighter than ±0.15% and achievable meter technology significantly exceeds budget | ER Vol 2 Part 2 accuracy clause vs. project budget constraints vs. vendor quotations | Specification.md REQ-06; Procedure.md Step 3.1.1 |
| Proving frequency vs. operational schedule | Measurement Canada requires quarterly proving but operational schedule allows only semi-annual maintenance windows | Measurement Canada regulations vs. facility operational schedule | Specification.md REQ-18; Procedure.md Step 3.4.2 |
| Meter technology vs. process conditions | ER specifies specific meter technology (e.g., Coriolis) but process conditions (high flow rate, low pressure drop available) favor different technology (e.g., ultrasonic) | ER Vol 2 Part 2 technology clause vs. DEL-12.03 hydraulic analysis vs. vendor capabilities | Specification.md REQ-05; Guidance.md § Considerations (Meter technology) |
| In-line prover vs. space allocation | In-line prover required but space allocation per site layout cannot accommodate prover dimensions | Proving requirements (ER or Measurement Canada) vs. DEL-12.01 layout constraints | Specification.md REQ-17; Procedure.md Step 3.4.1 |
| Materials vs. food-grade requirements | Standard materials specified but CSD canola oil requires food-grade certification | ER Vol 2 Part 2 material clauses vs. product specifications vs. food-grade regulations | Specification.md REQ-11; Guidance.md § Product-Specific Considerations |

## Cross-Document Traceability

| Document | Section | Traceability Points |
|----------|---------|---------------------|
| Datasheet.md | § Identification | DEL-12.02 identity referenced in Guidance § Purpose deliverable definition |
| Datasheet.md | § Conditions | Design context (service application, product CSD canola oil, throughput, metering points) driving Guidance § Considerations |
| Datasheet.md | § Construction | Key specification topics informing Guidance § Specification Content Considerations |
| Specification.md | § Scope | System boundaries that Guidance § Purpose downstream use addresses |
| Specification.md | § Requirements | REQ-01 through REQ-24 that Guidance § Principles rationale supports |
| Specification.md | § Standards | Custody transfer standards that Guidance § Considerations standard compliance addresses |
| Procedure.md | § Prerequisites | Inputs that Guidance § Considerations identifies as necessary (ER, standards, design basis, interfaces) |
| Procedure.md | § Step 1 | Basis gathering that Guidance § Principles contract alignment addresses |
| Procedure.md | § Step 3 | Requirements drafting that Guidance § Considerations informs for each topic |
| Procedure.md | § Step 5 | Discipline check that Guidance § Principles (testability, traceability) supports |
| DEL-12.01 | Drawings | Installation requirements from this specification drive DEL-12.01 content per Guidance § Purpose (engineering basis) |
| DEL-12.03 | Calculations | Performance requirements from this specification drive DEL-12.03 verification per Guidance § Purpose (engineering basis) |
| DEL-12.04 | Data Sheets | Equipment parameters per this specification documented in DEL-12.04 per Guidance § Purpose (procurement basis) |
| DEL-12.05 | Test Records | QA requirements from this specification drive DEL-12.05 compliance demonstration per Guidance § Purpose (compliance basis)
