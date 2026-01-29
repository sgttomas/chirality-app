# Guidance: DEL-12.04 Metering Data Sheet Package

## Purpose

This guidance document supports the development of the **Metering Data Sheet Package** for **PKG-12 Product Transfer & Metering**.

DEL-12.04 defines and substantiates metering in accordance with Employer's Requirements (Source: Decomposition:359). The deliverable is classified as a **Data Sheet** under the **Process** discipline, produced by the **D&B Contractor**.

### Deliverable Intent

The metering data sheet package serves as the structured, auditable single source of truth for equipment and instrument parameters throughout the project lifecycle:

- **Design phase** — data sheets consolidate requirements from ER, DEL-12.02 specification, and DEL-12.03 calculations into structured equipment definitions
- **Procurement phase** — data sheets provide equipment specifications for vendor bid packages and purchase orders
- **Installation phase** — data sheets provide equipment parameters for DEL-12.01 drawings and field installation
- **Testing phase** — data sheets provide acceptance criteria for DEL-12.05 test records (FAT, SAT, calibration, proving)
- **Operations phase** — data sheets provide reference parameters for operation, maintenance, and proving

These data sheets link specification requirements (DEL-12.02) and calculation results (DEL-12.03) to physical equipment, ensuring procurement and installation align with design intent.

### Downstream Use

Data sheets are used by:
- **Engineering** — DEL-12.01 drawings show equipment per data sheet specifications; tag numbers must match
- **Procurement** — vendor bid packages include data sheets as procurement specifications; vendor proposals are compared to data sheet requirements
- **Vendors** — vendor certified data is incorporated into data sheets; vendor data sheets are attached or referenced
- **Installation** — field installation verifies equipment matches data sheet parameters
- **Testing** — DEL-12.05 test records verify equipment per data sheet specifications (FAT, SAT, calibration)
- **Operations** — data sheets provide reference for operation, maintenance, troubleshooting, and spare parts

## Principles

### Data Sheet Development Rationale

| Principle | Rationale |
|-----------|-----------|
| Single Source of Truth | Data sheets consolidate equipment parameters from multiple sources (ER requirements, DEL-12.02 specification, DEL-12.03 calculations, vendor data) into one auditable, structured record; avoids conflicts from multiple sources; provides clear reference for all project phases (per Specification.md REQ-05, REQ-06) |
| Traceability | Each critical field should indicate its verification basis (per Specification.md REQ-10): "ER Vol 2 Part 2 Clause X.X.X" for ER-derived requirements, "DEL-12.02 Section Y" for specification requirements, "DEL-12.03 Calculation" for calculated values, "Vendor Certified Data" for manufacturer parameters, "ASSUMPTION" for inferred values, "TBD" for unknowns; traceability enables audit and verification; supports DEL-12.05 compliance demonstration |
| Consistency | Parameters must be consistent across all PKG-12 deliverables (per Specification.md REQ-04, REQ-05, REQ-06): tag numbers consistent with P&IDs and DEL-12.01 drawings (REQ-04), performance consistent with DEL-12.02 specification (REQ-05), sizing consistent with DEL-12.03 calculations (REQ-06); inconsistencies create confusion and rework; cross-checks during data sheet development identify and resolve conflicts |
| No Invention | Unknown values marked TBD with source needed; do not assume parameters without basis and labeling (per Specification.md REQ-12); assumed values can lead to procurement errors or equipment that does not meet requirements; TBD items flag gaps for resolution before procurement |

### Custody Transfer Data Sheet Principles

Data sheets for custody transfer service require specific attention to measurement quality parameters:

| Principle | Application |
|-----------|-------------|
| Accuracy Capture | Custody transfer accuracy class and uncertainty must be explicitly documented for commercial and regulatory compliance (per Specification.md REQ-07); accuracy class per DEL-12.02 specification (e.g., ±0.15%, ±0.25%; TBD); expanded uncertainty per DEL-12.03 uncertainty budget; accuracy is critical for commercial transactions (affects revenue/cost for buyer and seller); Measurement Canada approval may require specific accuracy documentation |
| Calibration Traceability | Calibration requirements enable DEL-12.05 records to demonstrate measurement traceability (per Specification.md REQ-11); calibration range, calibration traceability (traceable to Measurement Canada, NIST, or equivalent national metrology institute), calibration interval (per Measurement Canada regulations or DEL-12.02); traceability is essential for custody transfer approval and commercial confidence |
| Proving Fields | Proving-related parameters support custody transfer verification over time: proving method (in-line prover, portable prover, master meter; from DEL-12.02), proving frequency (quarterly, semi-annually, annually; from DEL-12.02 or Measurement Canada), meter factor range (acceptable range; e.g., 0.995-1.005; from DEL-12.03), meter factor drift limit (e.g., ±0.05%; from DEL-12.03), proving acceptance criteria (from DEL-12.03); proving maintains measurement accuracy over facility lifetime |

### Objective Alignment

| Objective | Data Sheet Guidance |
|-----------|---------------------|
| OBJ-2 Throughput Capacity (1,000,000 MT/a) | Data sheets must specify equipment rated for design flow rates supporting 1,000,000 MT/a throughput (per Specification.md REQ-08): flow meter data sheets document flow ranges from DEL-12.03 calculations (design flow rates for rail unloading and marine loading); transmitter data sheets document measurement ranges adequate for operating conditions; equipment capacity must not constrain facility throughput (Source: Decomposition:781) |
| OBJ-10 Custody Transfer Accuracy (Commercial Transactions) | Data sheets must capture accuracy class, calibration requirements, proving requirements, and traceability fields for custody transfer compliance (per Specification.md REQ-07, REQ-11): accuracy class per DEL-12.02 specification; expanded uncertainty per DEL-12.03 uncertainty budget; calibration traceability requirements; proving method, frequency, and acceptance criteria; data sheets enable DEL-12.05 test records to demonstrate measurement accuracy and traceability (Source: Decomposition:789) |

## Considerations

### Data Sheet Content Considerations

Factors affecting data sheet development:

| Factor | Consideration |
|--------|---------------|
| Service Differentiation | Rail unloading and marine loading have different flow profiles and operating conditions (per Specification.md REQ-02): **Rail unloading** — batch operation (railcar unloading events), multiple railcars (32 unloading stations per Decomposition:44; may unload multiple cars concurrently or sequentially), flow variations during batch (high initial rate, decreasing as car empties), lower flow rates than marine loading (typical railcar unloading 50-100 m³/h per car; ASSUMPTION); **Marine loading** — continuous high flow rates (vessel loading 500-2000 m³/h; ASSUMPTION), extended operation periods (loading duration depends on vessel size), high-value export transactions requiring tight accuracy; data sheets should capture service-specific conditions (flow ranges, operating modes, operational considerations) |
| Vendor Data Timing | Vendor-certified data may not be available at initial data sheet issue (per Guidance.md data sheet timing): **Inquiry stage** — data sheets include functional requirements, performance targets, TBD for vendor-specific parameters; used for vendor RFQ; **Order stage** — vendor-confirmed parameters incorporated; manufacturer and model identified; data sheets updated with vendor bid data; **Delivery stage** — final vendor-certified data incorporated; serial numbers added; data sheets finalized with as-ordered equipment; establish placeholder structure at inquiry stage; update progressively as vendor data becomes available; use revision control to track vendor data incorporation |
| Interface Fields | Capture electrical, controls, and communications interface data even when coordination is external (per Specification.md REQ-03, REQ-13): power supply requirements (for PKG-17 electrical load calculations), signal types and protocols (for PKG-19 control system I/O), communication parameters (for PKG-19 network configuration), area classification (for PKG-17 electrical design); interface fields enable coordinated design even though dependency mode is NOT_TRACKED |
| Calibration Fields | Include comprehensive calibration and proving fields per Specification.md REQ-11: calibration range (flow range over which meter is calibrated), calibration traceability (traceable to national standards), calibration interval (per Measurement Canada or operational schedule), certificates required (calibration certificate, material certificates), proving method and frequency (for flow meters), meter factor limits (for flow meters), proving acceptance criteria; calibration fields enable DEL-12.05 test records to demonstrate compliance and traceability |

### Flow Meter Data Sheet Considerations

Flow meter data sheets are the core custody transfer equipment documentation:

| Field | Guidance |
|-------|----------|
| Flow Range | Specify normal, design, minimum, maximum flow rates for each service per Specification.md REQ-08; flow ranges from DEL-12.03 sizing calculations; normal flow = typical operating flow rate (most common); design flow = maximum for sizing purposes; minimum flow = lowest measurable flow with specified accuracy (defines turndown); maximum flow = peak flow meter must handle; ensure flow ranges support 1,000,000 MT/a facility throughput (OBJ-2) |
| Accuracy Class | Custody transfer accuracy class per applicable standard per Specification.md REQ-07; cite accuracy class from DEL-12.02 specification (e.g., "±0.15% per OIML R117 accuracy class 0.5" or "±0.25% per API MPMS"); document expanded uncertainty from DEL-12.03 uncertainty budget (e.g., "Combined expanded uncertainty ±0.14% at 95% confidence per DEL-12.03"); accuracy critical for OBJ-10 custody transfer compliance |
| Materials | Wetted materials compatible with CSD canola oil per Specification.md REQ-05; specify body material (SS316L, carbon steel, or other from DEL-12.02), internals material (SS316L typical for food products), seals and gaskets (Viton, PTFE, or other compatible with vegetable oil); material selection affects corrosion resistance, cleanability, product contamination; food-grade materials may be required (TBD from ER or product specifications) |
| Process Connections | Size, rating, face type for piping integration per Specification.md REQ-03; connection size from DEL-12.03 (meter line size); flange rating (ANSI 150#, 300#, PN10, PN16, or other; TBD from DEL-12.02 or PKG-14 piping specification); flange facing (RF raised face, FF flat face, RTJ ring type joint; TBD); coordinate with PKG-14 piping for connection compatibility |
| Electrical | Power supply, signal outputs, communications protocol per Specification.md REQ-03, REQ-13; power supply from PKG-17 (voltage: 120VAC, 240VAC, 24VDC, or other; frequency: 50Hz, 60Hz; power consumption: watts; TBD); signal outputs to PKG-19 (4-20 mA analog for flow/density/temperature, pulse for totalizing, digital communication; TBD); communication protocol from PKG-19 (Modbus RTU/TCP, HART, Profibus, Foundation Fieldbus, or other; TBD); area classification from ER (Division 1 requires intrinsically safe or explosion-proof; Division 2 allows non-incendive or explosion-proof; non-classified allows general purpose; TBD) |
| Proving | Prover connection requirements, meter factor acceptance criteria per Specification.md REQ-11; proving method from DEL-12.02 (in-line prover, portable prover, master meter; TBD); prover connection type and size (flanged, threaded, quick-disconnect; TBD); meter factor range from DEL-12.03 (acceptable range: e.g., 0.995-1.005); meter factor drift limit from DEL-12.03 (e.g., ±0.05% from baseline); proving acceptance criteria from DEL-12.03 (proving repeatability, meter factor limits); proving frequency from DEL-12.02 (quarterly, semi-annually, annually; TBD) |

### Transmitter Data Sheet Considerations

Transmitter data sheets document instrumentation for custody transfer compensation:

| Field | Guidance |
|-------|----------|
| Measurement Range | Range appropriate for operating conditions per Specification.md REQ-02, REQ-03; **Temperature transmitters**: range from minimum to maximum operating temperature (e.g., 0-100°C, -20-80°C; TBD from ER Vol 2 Part 2 operating conditions); range should include normal operating temperature ±margin; **Pressure transmitters** (if applicable): range from minimum to maximum operating pressure (e.g., 0-10 bar, 0-150 psi; TBD from ER or PKG-14 piping); overpressure rating should exceed maximum pressure excursions |
| Accuracy | Accuracy class for custody transfer compensation per Specification.md REQ-05; transmitter accuracy contributes to combined measurement uncertainty per DEL-12.03; **Temperature**: typical RTD Pt100 accuracy Class A ±(0.15 + 0.002×T)°C or better (e.g., ±0.1°C; TBD from DEL-12.02); temperature accuracy affects density compensation uncertainty; **Pressure**: typical pressure transmitter accuracy ±0.1% of span or better (TBD from DEL-12.02); pressure accuracy affects volume correction (if applicable) |
| Signal Output | 4-20 mA, HART, or other per control system requirements per Specification.md REQ-13; signal type from PKG-19 control system requirements (4-20 mA analog standard; HART digital communication overlaid on 4-20 mA for diagnostics and configuration; pure digital protocols: Modbus, Profibus, Foundation Fieldbus; TBD); 2-wire vs. 4-wire (2-wire loop-powered typical for 4-20 mA; 4-wire separately powered typical for higher-accuracy transmitters) |
| Area Classification | Certifications for hazardous area per Specification.md REQ-13; area classification from ER Vol 2 Part 2 hazardous area classification drawings (TBD); **Division 1**: requires intrinsically safe (IS) or explosion-proof (XP) transmitters with appropriate certifications (CSA, UL, ATEX, IECEx); **Division 2**: allows non-incendive or explosion-proof; **Non-classified**: general purpose transmitters acceptable; certifications affect cost and availability |
| Calibration | Calibration range and certificate requirements per Specification.md REQ-11; calibration range typically same as measurement range; calibration traceability to national standards (Measurement Canada, NIST, or equivalent national metrology institute); calibration interval (typical 12-24 months for transmitters; may be specified in ER or project QA plan; TBD); calibration certificates required for custody transfer traceability |

### Service-Specific Considerations

| Service | Data Sheet Considerations |
|---------|---------------------------|
| Rail Unloading | **Batch operation**: Railcar unloading is batch operation; each car is separate custody transfer transaction; flow meter may require batch totalizing capability (cumulative total per car; reset between cars); coordinate with PKG-19 control system for batch control; **Flow variations**: Unloading flow rate varies during batch (high initial flow as railcar is pressurized, decreasing flow as car empties and pressure drops); meter must maintain accuracy across flow variation per turndown specification; **Multiple meters**: If 32 unloading stations have individual custody transfer meters (vs. manifold with single meter), 32 flow meter data sheets required (ASSUMPTION; TBD from system configuration); alternatively, if manifold arrangement with single custody transfer meter, single flow meter data sheet for rail unloading (TBD from DEL-12.01 arrangement) |
| Marine Loading | **Continuous high flow rates**: Vessel loading requires sustained high flow rates; flow meter sized for peak marine loading flow rate (typically higher than rail unloading); **Extended operation**: Loading duration depends on vessel size (hours to days for large vessels); meter reliability critical; **High-value export**: Marine loading is final custody transfer point for export transactions; accuracy is critical for commercial settlement; in-line prover may be specified for higher accuracy verification; more stringent calibration and proving requirements may apply |

### Data Sheet Timing Considerations

Data sheet development progresses through project phases (per Guidance.md in Pass 1; expanded here):

| Stage | Data Sheet Status | Actions | Verification Basis |
|-------|-------------------|---------|-------------------|
| **Inquiry / RFQ Stage** | Functional requirements and performance targets; TBD for vendor-specific parameters | Populate data sheets with: ER requirements, DEL-12.02 specification requirements, DEL-12.03 calculation results, design basis parameters; mark vendor-specific fields TBD (manufacturer, model, serial number, vendor-certified dimensions, vendor-certified performance); issue data sheets as procurement specifications | Verification basis: "ER Vol 2 Part 2 Clause X", "DEL-12.02 Section Y", "DEL-12.03 Calculation", "TBD — vendor to provide" |
| **Order / Purchase Stage** | Vendor-confirmed parameters; manufacturer and model identified | Incorporate vendor bid data: manufacturer name, model number, vendor-confirmed performance (accuracy, flow range, pressure drop), vendor-confirmed dimensions (length, weight, connections), vendor-confirmed electrical (power, signals); compare vendor bid data to data sheet requirements (verify vendor meets or exceeds requirements); issue purchase order referencing data sheet requirements and vendor-confirmed parameters | Verification basis: "Vendor Bid Data — [Vendor] Proposal [Ref]", "Vendor Certified — [Vendor] Data Sheet [Ref]" |
| **Delivery / Installation Stage** | Final certified data incorporated; as-ordered equipment documented | Incorporate vendor final certified data: serial numbers, final calibration certificates, actual as-manufactured dimensions and weights, material certificates (MTRs), test certificates (FAT results), Measurement Canada approval certificate (if applicable); update data sheets to reflect as-ordered and as-delivered equipment; issue final data sheets for DEL-12.05 installation and test records | Verification basis: "Vendor Certified Data — [Vendor] Certificate [Ref]", "Calibration Certificate [Number]", "Measurement Canada Approval [Number]" |

## Trade-offs

### Competing Design Factors

| Trade-off | Options | Guidance |
|-----------|---------|----------|
| Standardization vs. Service-Specific Optimization | Using identical flow meters for rail unloading and marine loading (same manufacturer, model, meter type) simplifies procurement (single vendor, volume discount), spares inventory (common spare parts), and maintenance training (single technology); service-specific meters (different technologies or sizes for rail vs. marine) optimize performance for each service flow profile and accuracy requirements | Consider meter technology commonality where feasible to reduce lifecycle cost (procurement, spares, training); coordinate with DEL-12.03 sizing — different flow ranges for rail and marine likely require different meter sizes even if same technology; evaluate whether identical technology with different sizes provides adequate standardization benefits vs. fully optimized service-specific designs; data sheets document selected approach |
| Accuracy vs. Cost | Higher accuracy flow meters and transmitters cost significantly more than standard instruments; incremental accuracy improvement has diminishing returns beyond certain point | Specify accuracy appropriate for custody transfer as required by ER or Measurement Canada, not unnecessarily tight (per Guidance.md in DEL-12.02); typical custody transfer accuracy ±0.15% to ±0.25% is acceptable for most vegetable oil applications; tighter accuracy (±0.10%) may be justified for very high-value export transactions; data sheets document specified accuracy per DEL-12.02; avoid gold-plating |
| Vendor Lock-in vs. Flexibility | Specifying specific vendor and model provides certainty (performance guaranteed, delivery schedule known, spares availability clear) but creates vendor lock-in and limits competition; generic functional specifications allow competitive bidding and vendor flexibility but may introduce uncertainty in performance and delivery | Use functional specifications with acceptable manufacturers list (approved vendors who meet requirements); allow vendors to propose equipment meeting data sheet requirements; data sheets initially have TBD for manufacturer/model; vendor selection during procurement incorporates certified data into data sheets; maintains competition while ensuring requirements are met |
| Detail Level | Highly detailed data sheets (extensive field coverage, tight tolerances) provide clear procurement specifications but may be difficult to populate if ER or vendor data is limited; less detailed data sheets are easier to complete but may not provide sufficient procurement guidance | Balance detail level based on available information and procurement needs: populate fields where information is available from ER, DEL-12.02, DEL-12.03; mark TBD for fields requiring vendor data; use verification basis column to indicate source of each parameter; detailed fields for critical custody transfer parameters (accuracy, flow range, calibration); less detail for non-critical parameters if data unavailable |

### Cross-Package Interface Considerations

Data sheets capture interface parameters for coordination with other packages (per Specification.md REQ-03, REQ-13):

| Interface | Data Sheet Fields for Coordination |
|-----------|-------------------------------------|
| PKG-14 Process Piping | **P&ID reference**: Identify P&ID drawing number and tag number for cross-reference; **Process connections**: Flange size, rating, facing must match piping specification; **Line sizes**: Meter line size from DEL-12.03 must match piping line size; **Straight-run requirements**: Document straight-run requirements (e.g., "10D upstream, 5D downstream") for piping layout coordination; piping layout must provide straight runs per data sheet requirements |
| PKG-17 Electrical Power Distribution | **Power supply**: Document voltage, frequency, power consumption for electrical load calculations; **Area classification**: Document area classification (Division 1, Division 2, non-classified) for electrical equipment selection; **Electrical certification**: Document required certifications (CSA, UL) for equipment procurement |
| PKG-19 Control Systems | **Signal outputs**: Document signal types (4-20 mA, pulse, digital), signal ranges (e.g., 4 mA = 0 flow, 20 mA = max flow), totalizer pulse weight (e.g., 1 pulse = 1 liter); **Communication protocol**: Document protocol (Modbus RTU/TCP, HART, Profibus) and parameters (baud rate, node address, register map) for control system integration; **Data logging**: Document data points for logging (flow instantaneous, total cumulative, total batch, density, temperature, pressure, alarms); **HMI**: Document display requirements (local display on meter vs. DCS HMI only) |
| PKG-20 Field Instrumentation | **Transmitter specifications**: If metering transmitters are within PKG-20 scope (vs. this deliverable), coordinate transmitter data sheets; **Signal protocols**: Coordinate signal types and protocols between metering data sheets and PKG-20 instrumentation specification; **Junction boxes**: Document junction box requirements for transmitter termination and cable routing |

## Examples

### Data Sheet Content Reference

The anticipated artifacts provide guidance on expected content (Source: Decomposition:359):

| Artifact | Expected Content |
|----------|------------------|
| Flow Meter Data Sheet — Rail Unloading | **Identification**: Tag number (e.g., FT-1201), service "Rail Unloading Custody Transfer", P&ID reference; **Process**: CSD canola oil, flow range 50-500 m³/h (example; TBD from DEL-12.03), temperature 10-40°C (example; TBD), pressure 2-8 bar (example; TBD); **Performance**: Coriolis mass flowmeter (example; TBD from DEL-12.02), accuracy ±0.15%, repeatability ±0.05%, turndown 20:1, expanded uncertainty ±0.14% (from DEL-12.03); **Materials**: Body SS316L, seals Viton; **Electrical**: 120VAC power, 4-20 mA flow output, pulse totalizer, Modbus RTU; **Physical**: 6" meter (example; TBD from DEL-12.03), 6" 150# RF flanges, 1200 mm length, 150 kg weight; **Proving**: Portable prover, quarterly, meter factor 0.995-1.005; **Vendor**: [TBD], Model [TBD] |
| Flow Meter Data Sheet — Marine Loading | Similar structure as rail unloading; higher flow range (e.g., 200-2000 m³/h; example; TBD from DEL-12.03); larger meter size (e.g., 10" or 12"; TBD from DEL-12.03); may have in-line prover instead of portable (TBD from DEL-12.02) |
| Temperature Transmitter Data Sheet | Tag number (e.g., TT-1201), service "Rail Unloading Metering Temperature Compensation", RTD Pt100 Class A, range 0-100°C, accuracy ±0.1°C, 4-20 mA output with HART, calibration traceable to Measurement Canada |
| Pressure Transmitter Data Sheet | Tag number (e.g., PT-1201), service "Rail Unloading Metering Pressure Compensation" (if applicable), range 0-10 bar, accuracy ±0.1% span, 4-20 mA output with HART, calibration traceable to Measurement Canada |

### Field Verification Basis Examples

Examples of verification basis documentation per Specification.md REQ-10 (ASSUMPTION; specific sources TBD):

| Field | Value | Verification Basis |
|-------|-------|-------------------|
| Accuracy Class | ±0.15% | DEL-12.02 Metering Technical Specification Section 4.2 |
| Flow Range | 50-500 m³/h | DEL-12.03 Metering Design Calculations Section 5.1 |
| Wetted Materials | Body SS316L, seals Viton | DEL-12.02 Specification Section 4.5 |
| Signal Output | 4-20 mA + Modbus RTU | PKG-19 Control System Specification Section 3.2 (TBD) |
| Calibration Traceability | Traceable to Measurement Canada | ER Vol 2 Part 2 Clause 7.3.2 (example; TBD) |
| Meter Size | 6" (150 mm) | DEL-12.03 Calculation Section 5.1 Table 3 |
| Manufacturer | [Vendor Name] | Vendor Certified Data — [Vendor] Data Sheet [Document #] |
| Serial Number | [Serial #] | Equipment nameplate; TBD until delivery |

## Conflict Table

### Local Conflicts (for Human Ruling)

No conflicts identified from accessible sources at this stage.

| Conflict ID | Conflict | Source A (File § Section) | Source B (File § Section) | Impacted Sections | Proposed Authority | Human Ruling |
|-------------|----------|---------------------------|---------------------------|-------------------|-------------------|--------------|
| — | — | — | — | — | — | TBD |

### Conflict Recording Instructions

When conflicts are discovered during data sheet development, record them in this table with:
- **Conflict ID:** Sequential identifier (e.g., DEL-12.04-C01)
- **Conflict:** Clear statement of the conflicting requirements or data
- **Source A/B:** File path and section reference for each conflicting source (e.g., "DEL-12.02 Specification.md REQ-07" or "Vendor Data Sheet [Vendor] [Doc#]")
- **Impacted Sections:** Which data sheet fields or documents are affected
- **Proposed Authority:** Which source should govern (PROPOSAL label)
- **Human Ruling:** Resolution decision and date (TBD until ruled)

### Potential Conflicts to Monitor

| Potential Conflict | Trigger Condition | Sources to Compare | Impacted Documents |
|--------------------|-------------------|--------------------|--------------------|
| Specification accuracy vs. vendor capability | DEL-12.02 specifies accuracy ±0.15% but vendor certified data shows achievable accuracy ±0.20% | DEL-12.02 Specification.md § Requirements (accuracy) vs. Vendor certified data sheet | Datasheet.md Construction § Flow Meter Data Sheet Fields (Performance); Specification.md REQ-05 |
| Calculation flow range vs. vendor range | DEL-12.03 calculates required flow range 50-500 m³/h but vendor standard meter has range 100-1000 m³/h | DEL-12.03 Calculation results vs. Vendor certified data sheet | Datasheet.md Construction § Flow Meter Data Sheet Fields (Process Conditions, Performance); Specification.md REQ-06 |
| ER material vs. vendor standard | ER requires SS316L but vendor standard model uses SS304 | ER Vol 2 Part 2 material clause vs. Vendor certified data sheet | Datasheet.md Construction § Flow Meter Data Sheet Fields (Materials); Specification.md REQ-05 |
| Tag numbering convention | P&IDs (PKG-14) use different tag numbering convention than data sheets | PKG-14 P&IDs vs. Project tag numbering system | Datasheet.md Construction § Flow Meter Data Sheet Fields (Identification); Specification.md REQ-04 |
| Electrical interface mismatch | Data sheet power supply or signal output differs from PKG-17/PKG-19 interface specifications | Data sheet electrical fields vs. PKG-17/19 interface specifications | Datasheet.md Construction § Flow Meter Data Sheet Fields (Electrical/Controls); Specification.md REQ-13 |

## Cross-Document Traceability

| Document | Section | Traceability Points |
|----------|---------|---------------------|
| Datasheet.md | § Identification | DEL-12.04 identity referenced in Guidance § Purpose deliverable definition |
| Datasheet.md | § Conditions | Design context (services, product, throughput) driving Guidance § Considerations |
| Datasheet.md | § Construction | Data sheet field categories informing Guidance § Flow Meter Data Sheet Considerations and § Transmitter Data Sheet Considerations |
| Specification.md | § Scope | Inclusions that Guidance § Purpose downstream use addresses |
| Specification.md | § Requirements | REQ-01 through REQ-17 that Guidance § Principles rationale supports |
| Specification.md | § Documentation | Field requirements that Guidance § Considerations informs |
| Procedure.md | § Prerequisites | Inputs that Guidance § Data Sheet Timing Considerations identifies (DEL-12.02, DEL-12.03, ER, P&IDs, vendor data) |
| Procedure.md | § Step 3 | Design basis population that Guidance § Flow Meter/Transmitter Considerations informs |
| Procedure.md | § Step 4 | Vendor data incorporation per Guidance § Data Sheet Timing Considerations (inquiry/order/delivery stages) |
| Procedure.md | § Step 5 | Cross-check that Guidance § Cross-Package Interface Considerations informs |
| DEL-12.01 | Drawings | Data sheet tag numbers, sizes, orientations shown in drawings per Guidance § Purpose (engineering downstream use) |
| DEL-12.02 | Specification | Performance requirements per Guidance § Flow Meter Data Sheet Considerations (accuracy, materials, proving) |
| DEL-12.03 | Calculations | Sizing parameters per Guidance § Flow Meter Data Sheet Considerations (flow range, meter size, pressure drop, uncertainty) |
| DEL-12.05 | Test Records | Calibration/proving fields per Guidance § Custody Transfer Data Sheet Principles (calibration traceability, proving fields) enable DEL-12.05 compliance
