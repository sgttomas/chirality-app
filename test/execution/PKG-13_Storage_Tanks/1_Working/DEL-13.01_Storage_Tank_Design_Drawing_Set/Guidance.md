# Guidance: DEL-13.01 Storage Tank Design Drawing Set

## Purpose

This guidance document supports the development of **Storage Tank Design Drawing Set** for **PKG-13 Storage Tanks**.

### Deliverable Role

Defines the design arrangement and details for 3 × 15,000 MT atmospheric storage tanks for CSD canola oil per ER requirements.

This deliverable provides the visual and dimensional definition necessary for:
- Tank fabrication procurement and vendor coordination
- Foundation design and construction (PKG-05)
- Piping design and interface coordination (PKG-14)
- Instrumentation installation (PKG-20)
- Construction planning and execution
- Operations and maintenance planning

**Source:** _CONTEXT.md, Decomposition DEL-13.01

### Project Context

- **Package:** PKG-13 Storage Tanks
- **Discipline:** Mechanical
- **Responsible Party:** D&B Contractor
- **Project Objectives Supported:**
  - OBJ-1: Safe & Reliable Operation — Tank design ensures safe storage and operations (Specification.md FR-01, PR-02, PR-06)
  - OBJ-3: Storage Capacity — Delivers 45,000 MT capacity in 3 × 15,000 MT tanks (Specification.md FR-01; Datasheet.md Tank Configuration)
  - OBJ-8: Future Expandability — Includes Phase 2 connection provisions (Specification.md FR-05; Datasheet.md Phase 2 Connections)

**Source:** Decomposition document, Section 2 (Project Objectives) and Section 6 (Objective Mapping)

---

## Principles

### Design Philosophy

**DP-01: Code Compliance First**
- API 650 is the governing standard for atmospheric storage tank design
- All design decisions shall comply with API 650 requirements and recommendations
- Where multiple design options exist within API 650, select the option that provides the most robust and maintainable solution considering lifecycle costs (OBJ-9)
- **Links to Requirements:** Specification.md PR-01 (Design Standard); Datasheet.md Tank Standard
- **Source:** Decomposition PKG-13 Scope; API 650 standard practice

**DP-02: Safety and Reliability**
- Tank design shall prioritize personnel safety during construction, operation, and maintenance
- Design shall minimize failure modes and provide defense-in-depth (overflow protection per PR-06, overfill prevention, proper venting per API 650 Appendix F)
- Access provisions (ladders, platforms, hatches) shall comply with safety standards (CSA Z259 for fall protection)
- **Links to Requirements:** Specification.md FR-01 (Storage Capacity), PR-02 (Seismic Design), PR-06 (Overflow Protection); Datasheet.md Seismic Requirements, Overflow Protection
- **Source:** OBJ-1 (Safe & Reliable Operation); ASSUMPTION based on safety-first design philosophy

**DP-03: Operability and Maintainability**
- Tank configuration shall facilitate operational needs: filling, mixing (agitators per PR-05), sampling, gauging, cleaning
- Maintenance access shall be provided for all equipment and components requiring routine service (agitators, level instruments, vents)
- Design shall minimize operational complexity and maintenance burden (OBJ-9: Lifecycle Cost Optimization)
- **Links to Requirements:** Specification.md FR-04 (Operational Flexibility), PR-05 (Agitator Performance); Datasheet.md Agitators, Access Provisions
- **Source:** OBJ-1 (Safe & Reliable Operation); OBJ-9 (Lifecycle Cost Optimization)

**DP-04: Interface Management**
- Tank design is one component of an integrated facility — interface coordination is critical
- Nozzle locations, elevations, and orientations must align with piping (PKG-14), instrumentation (PKG-20), and structural design (PKG-05)
- Early and ongoing coordination with adjacent packages required per Specification.md IR-01 through IR-06
- **Links to Requirements:** Specification.md IR-01 (Foundation Interface), IR-02 (Piping Interface), IR-03 (Instrumentation Interface), IR-04 (Fire Protection Interface), IR-05 (Coating Interface), IR-06 (Dyke/Bunding Interface)
- **Source:** Typical multi-discipline design challenges; Procedure.md Step 6 (Interdisciplinary Check)

**DP-05: Future-Proofing**
- Phase 2 expansion provisions shall be clearly identified, protected, and documented per Specification.md FR-05
- Design decisions shall consider potential future modifications and expansion scenarios
- Avoid design choices that preclude or significantly complicate future expansion
- **Links to Requirements:** Specification.md FR-05 (Future Expandability); Datasheet.md Phase 2 Connections
- **Source:** OBJ-8 (Future Expandability); Decomposition PKG-13 Scope (Phase 2 connections)

### API 650 Design Intent

API 650 is a prescriptive standard providing detailed rules for atmospheric storage tank design. Key principles:

**Tank Shell Design:**
- Shell thickness determined by hydrostatic pressure per API 650 Section 5.6 and minimum thickness requirements
- Bottom course thickness typically governs due to maximum liquid head
- Upper courses may be thinner (step-down approach for economy and weight reduction)
- Hydrostatic design basis: ρgh (product specific gravity × tank height × gravity)
- **Links to Requirements:** Specification.md PR-01 (Design Standard); Datasheet.md Shell Plate Thickness
- **Source:** API 650 Section 5 (Design)

**Bottom Design:**
- Bottom plates designed for product weight and foundation support
- Annular bottom plates often required for shell-to-bottom junction reinforcement (higher stress at junction)
- Proper slope for drainage typically 1:120 toward sump or water draw-off per PR-07
- Lap-welded bottom plates per API 650 Section 5.4
- **Links to Requirements:** Specification.md PR-01, PR-07 (Water Draw-off); Datasheet.md Bottom Plate Thickness, Water Draw-off
- **Source:** API 650 Section 5.4 (Bottom Design)

**Roof Design:**
- Roof type selection: cone roof, dome roof, or floating roof
- Cone roof common for non-volatile products like canola oil (low vapor pressure) — **ASSUMPTION**
- Roof loading considerations: dead load, live load, snow load per PR-03, internal pressure/vacuum per API 650 Appendix F
- Cone roof typically self-supporting for smaller diameters; rafter-supported for larger diameters
- **Links to Requirements:** Specification.md PR-03 (Environmental Loads); Datasheet.md Roof Type, Roof Configuration
- **Source:** API 650 Section 5.10 (Roof Design); ASSUMPTION based on product type

**Structural Stability:**
- Wind load resistance: shell stiffness per API 650 Section 5.9, wind girders if required
- Seismic resistance per API 650 Appendix E: base shear, overturning, sloshing (dynamic liquid motion), anchorage
- Foundation settlement tolerance per API 650 Appendix B: maximum differential settlement typically 1:100 over 10 m
- **Links to Requirements:** Specification.md PR-02 (Seismic Design), PR-03 (Environmental Loads), PR-04 (Foundation Performance); Datasheet.md Seismic Requirements, Wind Girders, Stiffening Rings
- **Source:** API 650 Sections 5.9 (Wind), Appendix E (Seismic), Appendix B (Foundations)

**Appurtenances:**
- Nozzles: reinforcement per API 650 Section 5.7 (reinforcement pad area calculation)
- Manholes, handholes, cleanout openings for access (sizes per API 650 Table 5.7a)
- Venting: normal venting for thermal breathing, emergency venting per API 650 Appendix F for fire exposure
- **Links to Requirements:** Specification.md PR-06 (Overflow Protection), PR-07 (Water Draw-off); Datasheet.md Nozzle Schedule, Vent Connections, Overflow Connections
- **Source:** API 650 Sections 5.7 (Appurtenances) and Appendix F (Venting)

---

## Considerations

### Product Characteristics

**Canola Oil Properties (Typical — TBD: Confirm with Product Specification)**
- Specific gravity: ~0.91–0.92 (lighter than water) — **TBD** per Datasheet.md Product Specific Gravity
- Viscosity: Moderate, temperature-dependent (increases at low temperature) — **TBD**
- Flash point: High (typically >200°C) — low fire/explosion risk — **TBD**
- Volatility: Low — atmospheric tank suitable (API 650 appropriate)
- Corrosivity: Generally low — carbon steel tanks acceptable with proper internal coating for product purity — **TBD**

**Design Implications:**
- Atmospheric tank (API 650) is appropriate for canola oil (low volatility, low vapor pressure)
- Internal coating (food-grade epoxy typical) may be required for product purity and corrosion protection — **TBD** per Specification.md IR-05 and PKG-26 coordination
- Heating system may be required if product viscosity increases significantly at low ambient temperature — **TBD** per Datasheet.md Heating System
- Agitation required per PKG-13 Scope and Specification.md PR-05 to prevent settling and maintain product uniformity

**Source:** ASSUMPTION based on typical canola oil properties; requires confirmation with product specification and ER (Volume 2 Part 2)

### Tank Sizing and Configuration

**Capacity Calculation:**
- Nominal capacity: 15,000 MT per tank (Specification.md FR-01)
- Requires product specific gravity to convert MT to volume (m³)
- Example calculation: 15,000 MT ÷ 0.92 SG ≈ 16,304 m³ — **ASSUMPTION pending SG confirmation** per Datasheet.md Product Specific Gravity
- Working capacity typically 90–95% of nominal tank volume to allow freeboard (ullage space for thermal expansion and vapor space)
- **Links to Requirements:** Specification.md FR-01 (Storage Capacity); Datasheet.md Capacity per Tank, Product Specific Gravity
- **Source:** ASSUMPTION based on typical tank design practice; requires DEL-13.03 capacity calculations

**Geometry Selection:**
- Tank diameter and height are design variables optimized for site constraints, cost, and constructability
- Typical diameter-to-height (D/H) ratio: 1:1 to 2:1 for large atmospheric tanks — **ASSUMPTION**
- Site constraints affect selection: available footprint, foundation conditions per DEL-02.04, height restrictions per local zoning
- **TBD** — Site layout, foundation conditions, height restrictions require site survey and ER extraction (Volume 2 Part 2)
- **Links to Requirements:** Specification.md PR-04 (Foundation Performance); Datasheet.md Tank Diameter, Tank Height
- **Source:** ASSUMPTION based on typical tank design optimization; requires DEL-13.03 sizing analysis; informed by Trade-off TD-01 (Diameter vs. Height)

**Multiple Tanks vs. Single Large Tank:**
- Project specifies 3 tanks for operational flexibility and redundancy (OBJ-4: Operational Flexibility)
- Benefits: maintenance isolation (take one tank offline), blending flexibility, independent filling/discharge operations
- Drawback: Higher cost than single large tank, more plot area required
- **Links to Requirements:** Specification.md FR-01 (Storage Capacity), FR-04 (Operational Flexibility); Datasheet.md Number of Tanks
- **Source:** Decomposition Section 1.1 (3 × 15,000 MT tanks); OBJ-4 (Operational Flexibility)

### Site-Specific Design Factors

**Location: Fraser Surrey Terminal, Surrey, BC**

**Seismic Considerations:**
- Surrey, BC is in a moderate-to-high seismic zone (proximity to Cascadia subduction zone)
- API 650 Appendix E seismic design required per Specification.md PR-02 — **ASSUMPTION**
- Site-specific seismic parameters needed: Peak Ground Acceleration (PGA), spectral acceleration Sa(T), site class — **TBD** per Datasheet.md Seismic Parameters
- Seismic design considerations: base shear, overturning moment, liquid sloshing dynamics, anchorage requirements, foundation performance
- Anchorage decision (anchored vs. unanchored) based on API 650 Appendix E overturning analysis — informed by Trade-off TD-04
- **Links to Requirements:** Specification.md PR-02 (Seismic Design), PR-04 (Foundation Performance); Datasheet.md Seismic Requirements, Anchor Chairs
- **Source:** ASSUMPTION based on BC seismicity; requires ER extraction (Volume 2 Part 2) and DEL-13.03 seismic analysis

**Wind Loading:**
- Coastal location (Fraser River estuary) may have elevated wind exposure
- NBC 2020 wind loads for Surrey, BC — **TBD** per Datasheet.md Design Wind Speed
- Wind girders may be required depending on shell stiffness and tank aspect ratio (H/D ratio)
- API 650 Section 5.9 provides wind stability criteria
- **Links to Requirements:** Specification.md PR-03 (Environmental Loads); Datasheet.md Design Wind Speed, Wind Girders
- **Source:** ASSUMPTION based on coastal location; requires ER extraction and DEL-13.03 wind analysis

**Snow Loading:**
- Roof snow load per NBC 2020 for Surrey, BC — **TBD** per Datasheet.md Snow Load
- Roof structural design must account for snow accumulation and potential drifting
- Cone roof slope (typical 1:16 to 1:12) sheds snow but must be designed for accumulation
- **Links to Requirements:** Specification.md PR-03 (Environmental Loads); Datasheet.md Snow Load
- **Source:** ASSUMPTION based on BC climate; requires ER extraction and DEL-13.03 roof design

**Foundation Conditions:**
- Geotechnical report (DEL-02.04) will provide bearing capacity and settlement characteristics
- Foundation type (ring wall, mat, piles) depends on soil conditions — **TBD** per Datasheet.md Foundation Type
- API 650 Appendix B settlement limits apply: maximum differential settlement typically 1:100
- **Links to Requirements:** Specification.md IR-01 (Foundation Interface), PR-04 (Foundation Performance); Datasheet.md Foundation Type, Bearing Capacity
- **Source:** API 650 Appendix B foundation requirements; requires DEL-02.04 coordination; informed by Trade-off TD-03

### Agitator Integration

**Agitator Purpose:**
- Maintain product uniformity and prevent density stratification (temperature or composition gradients)
- Prevent settling of particulates or water accumulation
- Facilitate blending and mixing operations
- **Links to Requirements:** Specification.md PR-05 (Agitator Performance); Datasheet.md Agitators
- **Source:** Decomposition PKG-13 Scope (agitators)

**Agitator Design Considerations:**
- Type selection: Side-entering (most common for large tanks), top-entering, or bottom-mounted — **TBD** per Datasheet.md Agitator Type
- Side-entry agitators: nozzle reinforcement required, structural loads on tank shell (thrust, bending moment, torsion)
- Top-entry agitators: roof support structure required, shaft length consideration
- Mounting details must integrate with tank shell design (nozzle reinforcement per API 650 Section 5.7 if side-entry)
- Access for installation, maintenance, removal (confined space entry considerations)
- **Links to Requirements:** Specification.md PR-05 (Agitator Performance); Datasheet.md Agitator Type, Agitator Drawings
- **Source:** ASSUMPTION based on typical agitator integration; requires DEL-13.02 specification and vendor data (DEL-13.04)

**Coordination:**
- Agitator drawings (anticipated artifact per _CONTEXT.md) must show mounting details, clearances, and structural interface
- Coordinate with DEL-13.04 (agitator data sheets) and agitator vendor for performance verification
- Coordinate with PKG-17 (electrical power) for agitator motor power supply
- **Links to Requirements:** Specification.md PR-05; Datasheet.md Agitator Drawings
- **Source:** _CONTEXT.md (Anticipated Artifacts: agitator drawings)

### Overflow Protection and Water Draw-off

**Overflow Protection:**
- Purpose: Prevent tank overfilling beyond safe capacity (OBJ-1: Safe & Reliable Operation)
- Typical solutions: overflow nozzle at maximum safe fill level, overflow piping to containment dyke or separate collection tank
- Coordinate with PKG-14 (piping) for overflow piping routing and PKG-19 (control systems) for high-level alarms and interlocks
- **Links to Requirements:** Specification.md PR-06 (Overflow Protection); Datasheet.md Overflow Protection, Overflow Connections
- **Source:** Decomposition PKG-13 Scope (overflow protection); typical tank safety features

**Water Draw-off:**
- Purpose: Remove water accumulation from tank bottom (condensation, rainwater ingress, product contamination)
- Canola oil specific gravity (~0.91–0.92) is less than water (1.0), so water settles to tank bottom
- Typical solution: low-point nozzle at tank bottom (sump location) with external valve and drain piping
- May integrate with tank drainage system for maintenance and cleaning
- **Links to Requirements:** Specification.md PR-07 (Water Draw-off); Datasheet.md Water Draw-off, Drain Connections
- **Source:** Decomposition PKG-13 Scope (water draw-off); typical tank appurtenance for low-density products

### Phase 2 Provisions

**Future Expandability:**
- Phase 2 connections shall be designed and installed in Phase 1, capped or blanked per Specification.md FR-05
- Locations and sizes must be coordinated with Phase 2 scope and layout — **TBD** per ER extraction (Volume 2 Part 2)
- Protection during Phase 1 operations: blind flanges, corrosion protection (coating), labeling
- Documentation: Phase 2 connections clearly identified on Tank GAs and nozzle schedules, documented in DEL-31.08 (O&M Manuals)
- **Links to Requirements:** Specification.md FR-05 (Future Expandability); Datasheet.md Phase 2 Connections
- **Source:** Decomposition PKG-13 Scope (Phase 2 connections); OBJ-8 (Future Expandability)

### Interfaces Requiring Early Coordination

**Foundation (PKG-05):**
- Foundation type, size, and anchor bolt layout must be coordinated early in design (Procedure.md Step 2: Preliminary Design)
- Tank loading (dead load, live load, seismic shear, wind overturning moment) provided to foundation designer (DEL-05.01)
- Settlement limits per API 650 Appendix B and monitoring provisions if required
- **Links to Requirements:** Specification.md IR-01 (Foundation Interface), PR-04 (Foundation Performance); Datasheet.md Foundation attributes
- **Source:** Typical tank-foundation interface requirements; Procedure.md Step 6 (IDC with PKG-05)

**Piping (PKG-14):**
- P&ID development drives nozzle schedule (sizes, quantities, locations, services) per Specification.md IR-02
- Nozzle orientations coordinated with piping routing and pipe support locations
- Thermal expansion and flexibility analysis (DEL-14.03) may impose nozzle loads on tank — verify nozzle design accommodates piping loads
- **Links to Requirements:** Specification.md IR-02 (Piping Interface); Datasheet.md Nozzle Schedule, all nozzle attributes
- **Source:** Typical tank-piping interface requirements; Procedure.md Step 6 (IDC with PKG-14)

**Instrumentation (PKG-20):**
- Level instrumentation: type selection (radar, ultrasonic, float, etc.), mounting nozzle size and location, access for calibration
- Temperature instrumentation if heating system provided (TBD per Datasheet.md Heating System)
- Pressure instrumentation for roof space and vent system monitoring
- **Links to Requirements:** Specification.md IR-03 (Instrumentation Interface); Datasheet.md Level Instrumentation, Temperature Instrumentation, Instrumentation Connections
- **Source:** Typical tank instrumentation requirements; Procedure.md Step 6 (IDC with PKG-20)

**Fire Protection (PKG-23):**
- Tank spacing for fire protection access and thermal radiation separation per Specification.md IR-04
- Foam system interfaces if required (foam injection nozzles, foam chambers) — **TBD**
- Fire water connections and monitors — **TBD**
- **Links to Requirements:** Specification.md IR-04 (Fire Protection Interface); Datasheet.md Tank Spacing
- **Source:** ASSUMPTION based on typical fire protection for bulk storage facilities; Procedure.md Step 6 (IDC with PKG-23)

**Coatings (PKG-26):**
- Internal coating selection for product compatibility (food-grade epoxy typical) and corrosion protection per Specification.md IR-05
- External coating for atmospheric corrosion protection and UV resistance
- Surface preparation requirements (blast cleaning grade) impact fabrication sequence and schedule
- **Links to Requirements:** Specification.md IR-05 (Coating Interface); Datasheet.md Coating System (Internal), Coating System (External)
- **Source:** Typical storage tank coating requirements; Procedure.md Step 6 (IDC with PKG-26)

---

## Trade-offs

### Design Decision Trade-offs

**TD-01: Tank Diameter vs. Height**
- **Larger Diameter, Shorter Height:**
  - **Pros:** Lower shell thickness (less hydrostatic head per API 650 Section 5.6), easier roof access for maintenance, lower wind loads, lower seismic overturning moment
  - **Cons:** Larger foundation footprint, more site area required, may conflict with site layout constraints
- **Smaller Diameter, Taller Height:**
  - **Pros:** Smaller foundation footprint, less site area, may fit site constraints better, potentially lower foundation cost
  - **Cons:** Thicker shell plates (higher hydrostatic head), higher wind loads and wind girder requirements, more difficult roof access, higher seismic overturning moment
- **Decision Basis:** Site layout optimization, foundation conditions per DEL-02.04, cost analysis, constructability (crane lift height for shell courses) — **TBD** in DEL-13.03 optimization
- **Links to Requirements:** Specification.md PR-02 (Seismic), PR-03 (Wind), PR-04 (Foundation); Datasheet.md Tank Diameter, Tank Height
- **Source:** ASSUMPTION based on typical tank design optimization; Procedure.md Step 3 (Detailed Design) decision point

**TD-02: Roof Type Selection**
- **Cone Roof (Fixed):**
  - **Pros:** Simple construction, low cost, suitable for low-volatility products like canola oil, well-established design
  - **Cons:** Vapor space subject to atmospheric breathing (venting required per API 650 Appendix F), potential for minor evaporation losses, requires normal and emergency venting
- **Dome Roof (Fixed):**
  - **Pros:** Structurally efficient for larger diameters (self-supporting), no internal columns required, good for snow loads
  - **Cons:** More complex fabrication (curved plates), higher cost than cone roof
- **Floating Roof (Internal or External):**
  - **Pros:** Minimizes vapor space, reduces evaporation losses, suitable for volatile products
  - **Cons:** High cost, complex operation and maintenance, less common for non-volatile products like canola oil, requires deck seals and supports
- **Decision Basis:** Product volatility (low for canola oil favors fixed roof), environmental regulations for VOC emissions, cost — **TBD** per ER extraction (Volume 2 Part 2)
- **Links to Requirements:** Specification.md PR-01 (API 650 design); Datasheet.md Roof Type, Roof Configuration
- **Source:** ASSUMPTION based on typical roof type selection criteria; API 650 Section 5.10

**TD-03: Foundation Type**
- **Ring Wall Foundation:**
  - **Pros:** Economical, suitable for competent soils, commonly used for API 650 tanks, simple construction
  - **Cons:** Requires adequate bearing capacity per DEL-02.04, sensitive to differential settlement (must meet API 650 Appendix B limits)
- **Mat Foundation (Slab):**
  - **Pros:** Distributes load over larger area, reduces settlement risk, suitable for weaker soils, provides solid base for tank bottom
  - **Cons:** Higher cost (more concrete), more complex construction, requires more excavation
- **Pile Foundation:**
  - **Pros:** Suitable for very weak soils or high seismic loads requiring deep foundation, transfers load to competent bearing strata
  - **Cons:** High cost, complex design and construction, less common for atmospheric storage tanks, requires pile driving or drilling
- **Decision Basis:** Geotechnical conditions per DEL-02.04 (bearing capacity, settlement characteristics), seismic loads per DEL-13.03, cost — **TBD**
- **Links to Requirements:** Specification.md IR-01 (Foundation Interface), PR-04 (Foundation Performance); Datasheet.md Foundation Type, Bearing Capacity
- **Source:** ASSUMPTION based on typical foundation type selection; API 650 Appendix B; requires DEL-02.04 coordination

**TD-04: Anchorage for Seismic**
- **Unanchored:**
  - **Pros:** Lower cost, simpler construction, acceptable if API 650 Appendix E overturning criteria are satisfied (tank remains stable without uplift)
  - **Cons:** Subject to uplift and potential shell buckling in severe seismic event, higher seismic acceleration capacity required for stability
- **Anchored:**
  - **Pros:** Resists overturning, suitable for high seismic zones or tall slender tanks, prevents uplift, increased seismic resistance
  - **Cons:** Higher cost (anchor chairs, anchor bolts, foundation design for bolt loads), adds complexity to shell and foundation design
- **Decision Basis:** Seismic analysis per API 650 Appendix E using site-specific seismic parameters (DEL-13.03) — **TBD** per Datasheet.md Seismic Parameters
- **Links to Requirements:** Specification.md PR-02 (Seismic Design); Datasheet.md Seismic Requirements, Anchor Chairs, Foundation Anchor Bolts
- **Source:** API 650 Appendix E seismic design criteria and anchorage requirements

**TD-05: Internal Coating vs. Bare Steel**
- **Internal Coating (Food-Grade Epoxy):**
  - **Pros:** Product purity (prevents contamination from rust or corrosion products), corrosion protection (extends service life), customer requirement for food-grade products (likely)
  - **Cons:** Higher initial cost, coating application requires surface preparation (blast cleaning), coating maintenance and periodic inspection required
- **Bare Carbon Steel:**
  - **Pros:** Lower initial cost, simpler construction (no coating application step)
  - **Cons:** Potential for corrosion (especially if water accumulation occurs), product contamination risk (rust particles), shorter service life, customer acceptance issue for food-grade product
- **Decision Basis:** Product compatibility requirements, ER specification for food-grade storage, lifecycle cost analysis (OBJ-9) — **TBD** per ER extraction (Volume 2 Part 2) and PKG-26 coordination
- **Links to Requirements:** Specification.md FR-02 (Product Compatibility), IR-05 (Coating Interface); Datasheet.md Coating System (Internal)
- **Source:** ASSUMPTION based on typical coating selection for edible oil storage; Procedure.md Step 3 (Detailed Design) decision point

---

## Examples

### Reference Precedents

**Similar Facilities:**
- Bulk liquid storage terminals for edible oils, vegetable oils, biodiesel (similar products and storage requirements)
- API 650 atmospheric storage tanks in similar capacity range (10,000–20,000 m³ per tank)
- **TBD** — Specific precedent projects or lessons learned to be identified during design development

**Industry Best Practices:**
- API 650 standard itself incorporates decades of industry experience and best practices for atmospheric storage tank design
- Tank fabrication and construction per API 653 (tank inspection, repair, alteration, and reconstruction) for future maintenance reference
- **Source:** API 650, API 653 standards

### Typical Drawing Set Content

**Tank General Arrangement (GA):**
- Plan view showing tank diameter, nozzle locations (with nozzle marks), appurtenances (manways, vents, overflow), agitator location
- Elevation view showing tank height, shell courses with thickness callouts, roof slope, ladder/platform locations, foundation interface
- Sections through tank showing internal details (bottom slope, sump configuration), agitator mounting detail reference, roof structure
- Nozzle orientation diagram (polar plot showing nozzle angular positions)
- **Links to Deliverable:** Datasheet.md Anticipated Drawing Set Content — Tank General Arrangements (3)
- **Source:** ASSUMPTION based on typical API 650 tank GA content; Procedure.md Step 4 (CAD Drafting) activity 4.2

**Foundation Drawing:**
- Foundation plan showing ring wall or mat dimensions, anchor bolt locations (if anchored per TD-04), sump/drain details
- Foundation sections and details (reinforcement, anchor bolt chairs if applicable, grout details)
- Anchor bolt chair details (if anchored) showing embedment, loading, bolt size
- Loading diagram for structural designer: dead load, seismic shear, wind overturning moment, tank operating/test loads
- **Links to Deliverable:** Datasheet.md Anticipated Drawing Set Content — Foundation Drawings
- **Source:** ASSUMPTION based on typical tank foundation drawing content; Procedure.md Step 4 activity 4.3

**Nozzle Schedule:**
- Table listing all nozzles with columns: nozzle mark (N1, N2, etc.), size (NPS), rating (Class 150, etc.), orientation (degrees from north), elevation (from tank bottom), service (inlet, outlet, vent, drain, etc.), connection type (flanged, threaded, welded)
- Reinforcement pad details per API 650 Section 5.7 (pad diameter, thickness)
- Flange facing (RF, FF) and bolt hole orientation (straddling or on centerline)
- **Links to Deliverable:** Datasheet.md Anticipated Drawing Set Content — Nozzle Schedules (3)
- **Source:** ASSUMPTION based on typical nozzle schedule content; Procedure.md Step 4 activity 4.4

**Roof Details:**
- Roof framing plan showing rafters, girders, column supports (if rafter-supported per TD-02 and roof diameter), compression ring
- Roof plate layout and seam details (lap-welded or butt-welded per API 650 Section 5.10)
- Manway detail showing cover, davit, access ladder from roof
- Vent nozzle and access hatch details
- Ladder and platform details for roof access (external ladder, landing platform, fall protection provisions per CSA Z259)
- **Links to Deliverable:** Datasheet.md Anticipated Drawing Set Content — Roof Details
- **Source:** ASSUMPTION based on typical API 650 roof detail content; Procedure.md Step 4 activity 4.5

**Agitator Drawing:**
- Agitator mounting nozzle and reinforcement detail (if side-entry) per API 650 Section 5.7
- Agitator support bracket or flange detail showing bolt pattern, sealing, torque requirements
- Clearance diagram showing agitator envelope (impeller diameter, shaft length) and internal clearances (to shell, bottom, opposite agitator)
- Loading diagram for tank designer: thrust load, bending moment, torsion on tank shell at nozzle location
- **Links to Deliverable:** Datasheet.md Anticipated Drawing Set Content — Agitator Drawings
- **Source:** ASSUMPTION based on typical agitator installation drawing content; Procedure.md Step 4 activity 4.6

---

## Cross-Document References

**For entity attributes and data:** See `Datasheet.md`
- Tank Configuration, Product, Capacity → Discussed in "Tank Sizing and Configuration"
- Seismic Design conditions → Discussed in "Seismic Considerations"
- Agitators → Discussed in "Agitator Integration"
- Overflow Protection, Water Draw-off → Discussed in "Overflow Protection and Water Draw-off"
- Phase 2 Connections → Discussed in "Phase 2 Provisions"
- All attributes inform the considerations and trade-offs discussed in this document

**For formal requirements:** See `Specification.md`
- Design Principles (DP-01 through DP-05) → Provide rationale for all functional and performance requirements (FR/PR series)
- API 650 Design Intent sections → Support PR-01 (Design Standard) and provide basis for detailed requirements
- Considerations sections → Inform interface requirements (IR series) and performance requirements (PR series)
- Trade-offs (TD-01 through TD-05) → Support design decision points referenced in requirements

**For production workflow and verification:** See `Procedure.md`
- Design philosophy and principles (DP-01 through DP-05) → Applied in Steps 2-3 (Preliminary and Detailed Design)
- Considerations (Product, Sizing, Site-Specific, Agitator, Interfaces) → Evaluated in Step 3 (Detailed Design Development)
- Trade-offs (TD-01 through TD-05) → Decision points in Step 3 (Detailed Design) and Step 8 (Design Review)
- Interface coordination sections → Implemented in Step 6 (Interdisciplinary Check) with PKG-05, PKG-14, PKG-20, PKG-23, PKG-26
- Examples (Drawing Set Content) → Inform Step 4 (CAD Drafting) drawing production

---

**Document Status:** Pass 3 Complete (2026-01-28) — Design philosophy, API 650 intent, product/site considerations, trade-offs, and examples provided with explicit links to requirements (Specification.md), attributes (Datasheet.md), and workflow (Procedure.md). All TBDs specify information source needed. ASSUMPTIONs labeled with basis and references. Ready for WORKING_ITEMS refinement.

**Last Updated:** 2026-01-28
