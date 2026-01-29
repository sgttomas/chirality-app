# Guidance: DEL-12.01 Metering Design Drawing Set

## Purpose

This guidance document supports the development of the **Metering Design Drawing Set** for **PKG-12 Product Transfer & Metering**.

DEL-12.01 defines the design arrangement and details for custody transfer metering per Employer's Requirements (Source: Decomposition:356). The deliverable is classified as a **Drawing** under the **Process** discipline, produced by the **D&B Contractor**.

### Deliverable Intent

The metering design drawings serve as the primary geometric definition for custody transfer metering installations at two critical measurement points in the canola oil transload facility:

1. **Rail unloading** — measuring product received from rail tank cars
2. **Marine loading** — measuring product delivered to liquid bulk carriers for export

These drawings enable construction and commissioning of metering systems that satisfy the project's custody transfer accuracy (OBJ-10) and throughput capacity (OBJ-2) objectives. The drawings provide the spatial, dimensional, and interface information necessary for fabrication, installation, proving, and operation of custody transfer metering equipment.

### Downstream Use

The drawing set serves multiple downstream purposes:
- **Fabrication** — metering skid manufacturers use GAs and details for skid fabrication
- **Installation** — field installation crews use drawings for positioning, alignment, and piping tie-ins
- **Commissioning** — commissioning team uses drawings to verify as-built configuration and proving connections
- **Operations** — operations personnel use drawings to understand meter arrangement and access for maintenance
- **Regulatory approval** — drawings may be submitted to Measurement Canada or other authorities for custody transfer approval (TBD; ER Vol 2 Part 2)

## Principles

### Custody Transfer Measurement Intent

The drawings must make the custody-transfer measurement intent unambiguous and verifiable (ASSUMPTION based on Decomposition:350, 356, 789):

| Principle | Rationale |
|-----------|-----------|
| Meter run geometry clarity | Clear depiction of meter orientation, upstream/downstream straight-run requirements, and flow conditioning (if any) prevents field deviations that affect measurement accuracy; any deviation from design geometry can introduce measurement error |
| Instrument tap locations | Explicit positioning of temperature, pressure, and density (if applicable) measurement points ensures proper flow compensation; inaccurate temperature or pressure measurement degrades custody transfer accuracy |
| Proving connection accessibility | Proving loop/master meter connection points must be clearly detailed to enable periodic verification; proving is essential for maintaining custody transfer accuracy over time |
| Installation precision | Drawings must enable field installation that matches design intent; meter orientation, alignment, and straight-run compliance directly affect measurement performance |

### Objective Alignment

| Objective | Guidance |
|-----------|----------|
| OBJ-2 Throughput Capacity (1,000,000 MT/a) | Ensure meter run arrangements do not introduce unnecessary pressure drop or flow constraints that limit throughput; meter sizing per DEL-12.03 calculations should be reflected in arrangement dimensions; piping geometry should minimize pressure loss while maintaining measurement accuracy (Source: Decomposition:781) |
| OBJ-10 Custody Transfer Accuracy | Drawing clarity prevents undocumented field changes that degrade measurement accuracy; straight-run requirements, meter orientation, flow conditioning, and instrument positions must be explicit and dimensioned; proving connections must be accessible and clearly detailed (Source: Decomposition:789) |
| OBJ-6 Regulatory Compliance | Drawings must support compliance with Measurement Canada and applicable custody transfer regulations; installation must be per approved design to maintain custody transfer approval (ASSUMPTION based on Canadian location) |

### Drawing Content Principles

| Principle | Application |
|-----------|-------------|
| Completeness | Include all decomposition-listed artifacts: metering skid GAs, flow meter installation details, proving connection details; ensure both rail unloading and marine loading services are covered |
| Constructability | Show access for installation, lifting, alignment, and welding; provide clearances for component installation; identify lifting points and rigging provisions |
| Maintainability | Show access for proving, calibration, inspection, and component replacement; ensure proving equipment can be connected without process shutdown if possible; provide access for transmitter calibration and verification |
| Interface clarity | Identify piping tie-ins (PKG-14), electrical/control interfaces (PKG-17, PKG-19, PKG-20), and structural support requirements (PKG-06); dimension interface points to enable coordination |
| Measurement precision | Dimension all geometry critical to measurement accuracy (straight runs, meter orientation, instrument tap positions); specify tolerances where critical (e.g., meter levelness, alignment) |

## Considerations

### Design Factors to Address

| Factor | Consideration |
|--------|---------------|
| Meter technology | Drawing arrangements depend on selected meter type (Coriolis, ultrasonic, turbine, positive displacement, etc.) — coordinate with DEL-12.02 and DEL-12.04; each technology has different installation requirements, straight-run needs, and orientation constraints |
| Straight-run requirements | Different meter technologies have different upstream/downstream straight-run requirements; Coriolis meters typically require shorter straight runs than turbine or ultrasonic meters; verify manufacturer recommendations and reflect in drawings; insufficient straight runs degrade accuracy |
| Flow conditioning | Some meter technologies require flow conditioning (straightening vanes, perforated plates) to achieve specified accuracy; if required per DEL-12.02, flow conditioner position and type must be clearly shown |
| Proving method | Arrangement depends on whether in-line prover, portable prover, or master meter proving is used — coordinate with DEL-12.02; in-line prover requires dedicated piping and isolation; portable prover requires accessible connection points; master meter requires parallel meter run (TBD) |
| Environmental conditions | Outdoor/indoor installation affects enclosure, heat tracing, insulation, and access provisions — confirm from ER Vol 2 Part 2 (TBD); Fraser Surrey Terminal location subject to Pacific Northwest climate (rain, temperature range, seismic) |
| Hazardous area classification | Electrical interface details depend on area classification — coordinate with PKG-17 (TBD; ER Vol 2 Part 2); custody transfer metering may require intrinsically safe or explosion-proof instrumentation |
| Seismic design | Skid anchorage and piping support must accommodate seismic loads — coordinate with PKG-06 for structural support design (TBD; ER Vol 2 Part 1) |
| Product characteristics | CSD canola oil properties (density, viscosity, vapor pressure, temperature) affect meter selection and installation; vegetable oils may require heat tracing to maintain fluidity depending on ambient temperature (TBD; ER Vol 2 Part 2) |

### Service-Specific Considerations

| Service | Considerations |
|---------|----------------|
| Rail Unloading Metering | Multiple railcars may be unloaded simultaneously; consider whether individual metering or manifold with single custody transfer meter is used; railcar unloading rates vary; meter range must accommodate flow variation; proving frequency during unloading operations affects proving connection design |
| Marine Loading Metering | High flow rates for vessel loading (loading rates drive meter sizing per DEL-12.03); meter range must accommodate vessel loading profile; proving during loading may be required; proving connection must not interrupt loading operations; marine loading is the final custody transfer point for export |

### Interface Considerations (Coordinated Externally)

Dependencies coordinated externally per dependency mode NOT_TRACKED (see `_DEPENDENCIES.md`):

| Interface | Coordination Need |
|-----------|-------------------|
| PKG-06 Structural Steelwork | Skid support structure design, elevations, anchor bolt locations; access platforms, stairs, and walkways; seismic bracing; coordinate skid dimensions and loading |
| PKG-14 Process Piping | Piping tie-in locations, elevations, and orientations; isolation valve positions; upstream and downstream piping configuration; coordinate to ensure straight-run requirements are met in overall piping layout |
| PKG-17 Electrical Power Distribution | Power supply routing to metering equipment (meters, transmitters, control panels); coordinate electrical interface points, conduit routing, and hazardous area requirements |
| PKG-19 Control Systems | Signal routing from transmitters to control system; control panel locations; HMI requirements for metering display; coordinate tag numbers, I/O lists, and signal types |
| PKG-20 Field Instrumentation | Transmitter mounting, junction box locations, cable routing; coordinate instrument tag numbers, specifications, and installation details |

### Product-Specific Considerations for Canola Oil

CSD (Crude Super Degummed) canola oil has specific properties that may affect metering design:

- **Viscosity** — vegetable oil viscosity varies with temperature; meter performance may be temperature-dependent (TBD; verify from ER Vol 2 Part 2 or vendor data)
- **Density** — canola oil density affects mass flow calculation; density measurement or compensation may be required for accurate custody transfer (TBD; coordinate with DEL-12.02)
- **Temperature effects** — product temperature affects density and viscosity; temperature measurement is critical for accurate custody transfer; heat tracing may be required to prevent solidification at low ambient temperatures (TBD)
- **Vapor pressure** — low vapor pressure; cavitation unlikely under normal operating conditions (ASSUMPTION; verify from ER Vol 2 Part 2)
- **Corrosivity** — vegetable oils generally non-corrosive; standard carbon steel or stainless steel piping acceptable (TBD; verify material selection from DEL-12.02)

## Trade-offs

### Competing Design Factors

| Trade-off | Options | Guidance |
|-----------|---------|----------|
| Accuracy vs. Pressure Drop | Longer straight runs and flow conditioning improve accuracy but increase pressure drop and footprint; shorter runs reduce footprint and pressure drop but may compromise accuracy | Balance per project hydraulic constraints (DEL-12.03) and accuracy requirements (OBJ-10); custody transfer accuracy is typically the governing criterion; accept additional pressure drop if necessary to meet accuracy requirements |
| Accessibility vs. Footprint | Better access for proving and maintenance requires more space; compact arrangements reduce footprint but may limit access | Prioritize proving access; proving is essential for maintaining custody transfer accuracy over facility lifetime; insufficient access leads to deferred proving and degraded accuracy; allocate adequate space for proving equipment connection |
| Standardization vs. Optimization | Using identical meter technology and arrangements for rail and marine simplifies design, spares inventory, and maintenance training but may not optimize each service; service-specific designs optimize performance but increase complexity | Consider meter technology commonality where feasible to reduce spares and training requirements; however, size each meter run for service-specific flow rates per DEL-12.03; identical technology does not mean identical sizes |
| Integrated vs. Modular Skid | Integrated skid (meter run, instruments, control panel on single skid) simplifies installation but complicates transport and may exceed lifting capacity; modular approach (separate skids) adds field connections but facilitates transport and installation | Consider site access, available lifting capacity, and transportation constraints; Fraser Surrey Terminal location may have crane access limitations; coordinate with PKG-06 for rigging and lifting analysis; field connections add potential leak points but may be necessary for large assemblies |
| In-line vs. Portable Proving | In-line prover provides continuous proving capability and higher accuracy but requires significant space and capital cost; portable prover reduces footprint and cost but requires operational coordination for proving events | Balance capital cost, space constraints, and operational requirements; in-line prover typical for high-value custody transfer (export loading); portable prover may be acceptable for railcar unloading; coordinate with DEL-12.02 proving requirements |

### Unresolved Trade-offs (TBD)

The following trade-offs require resolution during detailed design (inputs from ER Vol 2 Part 2 and DEL-12.02):

- Specific meter technology selection (Coriolis vs. ultrasonic vs. turbine vs. positive displacement) — affects straight-run requirements, proving approach, accuracy, and cost
- Proving methodology (in-line prover vs. portable prover vs. master meter) — affects space allocation, connection details, and capital cost
- Area classification (Division 1 vs. Division 2 vs. non-classified) — affects electrical interface design and equipment selection
- Indoor vs. outdoor installation — affects enclosure design, environmental protection, and access provisions
- Heat tracing requirements — affects piping design, power requirements, and operational complexity

## Examples

### Reference for Drawing Content

The anticipated artifacts provide guidance on expected drawing content (Source: Decomposition:356):

| Artifact | Expected Content |
|----------|------------------|
| Metering Skid GAs | Plan and elevation views showing: meter run(s) with flow direction, associated piping (isolation valves, bypass, proving connections), instruments (flow meters, temperature transmitters, pressure transmitters, density transmitters if applicable), structural supports and skid framing, access provisions (platforms, stairs, walkways), dimensions (overall skid dimensions, meter centerline elevations, critical clearances), tag numbers for all equipment, interface points (piping tie-ins, electrical connections, structural supports) |
| Flow Meter Installation Details | Detailed views showing: meter mounting and orientation (horizontal, vertical, or inclined per manufacturer requirements), straight-run dimensions upstream and downstream with tolerances, flow conditioning devices (if any) with positions, instrument tap positions (temperature, pressure, density) dimensioned from meter, mounting details (flanges, supports, alignment provisions), installation notes (torque requirements, gasket types, alignment tolerances), clearances for removal and maintenance |
| Proving Connection Details | Details showing: prover connection points (locations, elevations, sizes), isolation valves for proving loop, drainage provisions for proving connections, access for proving equipment connection and operation, piping routing for proving loop (if in-line prover), notes on proving procedures and frequency (if available from DEL-12.02) |

### Coordination with Other PKG-12 Deliverables

| Deliverable | Relationship and Coordination Points |
|-------------|--------------------------------------|
| DEL-12.02 Metering Technical Specification | Provides performance requirements (accuracy ±%, repeatability, flow range min/max, operating pressure and temperature, meter technology selection, proving method, calibration frequency); drawings must accommodate all specified requirements; tag numbers must match between specification and drawings |
| DEL-12.03 Metering Design Calculations | Provides sizing basis (flow rates for rail unloading and marine loading, pressure drops, straight-run lengths calculated per meter manufacturer requirements); dimensions in drawings must align with calculated values; any deviation from calculated straight runs requires calculation update |
| DEL-12.04 Metering Data Sheet Package | Provides specific instrument parameters (flow meter size, connection size, transmitter ranges, power requirements, signal types); drawings show physical arrangement of specified equipment; tag numbers, sizes, and connections must match data sheets exactly; vendor dimensional data used for detail drawings |

### Typical Metering Skid GA Content (ASSUMPTION)

A typical metering skid GA for custody transfer service would show:

- **Plan view**: Meter run centerline, isolation valves upstream and downstream, bypass piping (if any), proving connections, instrument locations (plan positions), dimensions (overall skid length and width, meter position along skid), tag numbers
- **Elevation view**: Meter elevation, piping elevations, structural supports, access platform elevation (if any), height clearances, vertical dimensions
- **Notes**: Flow direction, straight-run requirements (e.g., "Minimum 10D upstream, 5D downstream"), proving frequency, installation requirements, interface points
- **Title block**: Drawing title, number, revision, date, originator, checker, approver, project information

## Conflict Table

### Local Conflicts (for Human Ruling)

No conflicts identified from accessible sources at this stage.

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority | Human Ruling |
|-------------|----------|----------|----------|-------------------|-------------------|--------------|
| — | — | — | — | — | — | — |

**Note:** Conflicts discovered during detailed design should be added here with citations and requested human ruling. Potential conflicts that may arise:

- **Accuracy vs. pressure drop conflicts** — if ER specifies both high accuracy and low pressure drop, and these cannot be simultaneously achieved with available meter technology, document conflict with citations from ER Vol 2 Part 2 and vendor data
- **Straight-run conflicts with layout constraints** — if required straight runs per manufacturer exceed available space in facility layout, document conflict with layout drawings and manufacturer requirements
- **Proving method conflicts** — if ER requires in-line prover but space or budget constraints favor portable prover, document conflict with ER clause and project constraints
- **Hazardous area classification conflicts** — if area classification requires expensive explosion-proof equipment but metering budget assumes non-classified area, document conflict with area classification drawings and budget assumptions
