# Guidance: DEL-18.01 Lighting Design Drawing Set

## Purpose

This guidance document supports the development of the **Lighting Design Drawing Set** for **PKG-18 Lighting** on the Canola Oil Transload Facility project.

**Deliverable Purpose:** Defines the design arrangement and details for lighting per ER requirements. *(Source: _CONTEXT.md, Decomposition DEL-18.01 description)*

**Role in Project:** This drawing set provides the graphical representation and spatial arrangement of the facility lighting systems, supporting:
- Construction installation of lighting fixtures and infrastructure
- Coordination with other disciplines (architectural, electrical, civil, controls)
- Verification that lighting design meets illumination requirements
- Commissioning and testing activities (DEL-18.05)
- Operations and maintenance reference

**Deliverable Classification:**
- **Type:** Drawing
- **Discipline:** Electrical
- **Responsible Party:** D&B Contractor

## Principles

**Engineering Rationale (Lighting Design):**

**P-1: Lighting Levels and Quality**
- Illumination design shall provide safe, effective task lighting while minimizing energy consumption
- Lighting levels based on activity type, safety requirements, and applicable codes (IESNA, CSA C22.1, ER requirements) — **TBD** *(ER location TBD)*
- Uniformity ratios considered to avoid dark spots and excessive contrast — **ASSUMPTION** *(Good engineering practice)*

**P-2: LED Technology Selection**
- PKG-18 scope specifies LED lighting *(Source: Decomposition PKG-18 scope)*
- LED provides: long life (reduced maintenance), energy efficiency, good color rendering, instant-on capability
- LED suitable for marine/industrial environment with appropriate IP ratings — **ASSUMPTION**

**P-3: Emergency Lighting Principles**
- Emergency lighting ensures safe egress during power failure per NFPA 101 and CSA C22.1 — **ASSUMPTION**
- Emergency lighting powered by emergency power source (battery backup, generator, or UPS) — **TBD** *(System configuration to be confirmed)*
- Minimum illumination levels and duration per code requirements — **TBD**

**P-4: Lighting Controls**
- PKG-18 scope includes lighting controls *(Source: Decomposition PKG-18 scope)*
- Controls provide energy savings (occupancy sensing, daylight harvesting, scheduling) and operational flexibility — **ASSUMPTION**
- Integration with facility control systems (PKG-19) for centralized monitoring and control — **ASSUMPTION**

**P-5: Maintainability and Access**
- Fixture locations selected for safe access during lamp replacement and maintenance
- Exterior pole-mounted fixtures: consider pole height, climbing safety, and ground-level access — **ASSUMPTION**
- Interior fixtures: coordinate with ceiling grid, access panels, and maintenance clearances — **ASSUMPTION**

**Applicable Standards Context:**

**Electrical Codes:**
- **CSA C22.1** (Canadian Electrical Code) — Governs electrical installations in Canada; specifies wiring methods, grounding, hazardous locations — **ASSUMPTION**
- **NBCC 2020** — Building code requirements for egress lighting, seismic design of poles and supports — **ASSUMPTION**

**Lighting Design Standards:**
- **IESNA Lighting Handbook** — Industry reference for illuminance levels, calculation methods, quality metrics — **TBD** *(Edition and location TBD)*
- **IES Recommended Practices** — Guidance for specific applications (exterior, industrial, etc.) — **TBD**

**Life Safety:**
- **NFPA 101** (Life Safety Code) — Emergency egress lighting requirements — **ASSUMPTION**

**Drawing Standards:**
- Project CAD standards define layer naming, symbology, text styles, and file organization — **TBD** *(Location TBD)*
- CSA Z32 or similar standards for electrical diagram symbols — **TBD**

## Considerations

**Factors to Consider During Drawing Development:**

**C-1: Site and Environmental Factors**
- **Marine environment:** Salt spray, moisture, corrosion potential — select fixtures with appropriate IP rating and corrosion-resistant materials — **ASSUMPTION**
- **Outdoor temperature range:** Surrey, BC climate (-20°C to +40°C approximate) — verify fixture operating temperature range — **ASSUMPTION** *(Range TBD)*
- **Wind loading:** Pole-mounted fixtures subject to wind forces per NBCC — coordinate structural design with civil/structural disciplines — **ASSUMPTION**
- **Seismic:** Surrey, BC is seismically active region — pole foundations and mounting to meet NBCC seismic requirements — **ASSUMPTION**

**C-2: Hazardous Area Classification**
- Canola oil transfer and storage may create hazardous areas (flammable vapor zones) — **TBD** *(Hazardous area classification study location TBD)*
- Lighting in hazardous areas requires explosion-proof or intrinsically safe fixtures per CSA C22.1 and classification drawings — **TBD**
- Coordinate fixture selection with hazardous area boundaries (typically shown on electrical area classification drawings) — **ASSUMPTION**

**C-3: Coordination with Other Disciplines**
- **Architectural (PKG-21, PKG-22):** Building layouts, ceiling types, finishes — interior fixture types must be compatible with ceiling system
- **Civil (PKG-01, PKG-02, PKG-03):** Site grading, paving, underground utilities — exterior pole locations must avoid conflicts and provide proper drainage around foundations
- **Electrical Power (PKG-17):** Panel locations, feeder routing, circuit capacities — lighting circuits must tie into available panel capacity
- **Controls (PKG-19):** Control system architecture — lighting controls interface with SCADA or BMS as applicable — **TBD**
- **Fire Protection (PKG-23):** Sprinkler heads, fire alarm devices — maintain required clearances and avoid obstructions

**C-4: Operational and Maintenance Considerations**
- **Access for maintenance:** Pole heights and fixture mounting locations should allow safe maintenance access (aerial lifts, catwalks, ladders)
- **Spare parts standardization:** Minimize fixture types to reduce spare parts inventory — **ASSUMPTION** *(Good practice)*
- **Control zoning:** Organize lighting circuits by operational area to allow selective switching and reduce energy waste — **ASSUMPTION**
- **Future flexibility:** Consider future expansion per OBJ-8 (Future Expandability) — **TBD** *(Not explicitly tied to PKG-18 in objective mapping, but general consideration)*

**C-5: Security and Safety**
- **Perimeter security lighting:** Adequate illumination for CCTV cameras (PKG-28) and security personnel — **TBD** *(ER requirements location TBD)*
- **Process safety:** Lighting levels in operational areas sufficient for safe equipment operation and emergency response — **ASSUMPTION**
- **Egress lighting:** Clear visibility of exit paths, signage, and obstacles during emergency conditions per NFPA 101 — **ASSUMPTION**

**C-6: Energy Efficiency and Sustainability**
- **Lighting power density:** Minimize watts per square meter while meeting illumination requirements — **TBD** *(Energy code or ER requirements)*
- **Controls for energy savings:** Occupancy sensors, daylight harvesting, time scheduling — **ASSUMPTION** *(Enabled by PKG-18 scope including controls)*
- **Lifecycle cost:** LED initial cost higher but lower lifecycle cost due to long life and low energy consumption per OBJ-9 (Lifecycle Cost Optimization) — **ASSUMPTION** *(Not explicitly tied to PKG-18 in objective mapping)*

**C-7: Regulatory and Permitting**
- Lighting design shall comply with all applicable codes, permits, and authority requirements per OBJ-6 (Regulatory Compliance) — **ASSUMPTION**
- **TBD** — Local authority requirements (City of Surrey, Port Authority, etc.)

## Trade-offs

**Competing Concerns to Evaluate:**

**T-1: Illumination Level vs. Energy Consumption**
- **Higher illumination** improves visibility and safety but increases energy cost and fixture count
- **Lower illumination** reduces energy and capital cost but may compromise safety or task performance
- **Resolution approach:** Use task-specific illumination levels per IESNA; avoid over-lighting; use controls to reduce energy when not needed — **ASSUMPTION**

**T-2: Pole Height vs. Coverage vs. Cost**
- **Taller poles** provide wider coverage (fewer poles required), but higher cost, more difficult maintenance, greater wind loading
- **Shorter poles** easier to maintain and install, but require more poles for same coverage, potentially more visual clutter
- **Resolution approach:** Optimize pole height based on photometric analysis (DEL-18.03), maintenance access constraints, and site aesthetics — **ASSUMPTION**

**T-3: Fixture Standardization vs. Optimization**
- **Standardized fixtures** reduce spare parts inventory, simplify procurement, reduce lifecycle cost
- **Optimized fixtures** tailored to specific areas may provide better performance or lower energy use
- **Resolution approach:** Limit fixture types to 3-5 standard models covering majority of applications; use special fixtures only where justified — **ASSUMPTION**

**T-4: Initial Cost vs. Lifecycle Cost**
- **Lower initial cost** may use cheaper fixtures with shorter life, higher energy consumption, or more frequent maintenance
- **Higher initial cost** (LED, high-efficiency) provides long-term savings in energy and maintenance per OBJ-9
- **Resolution approach:** LED technology already selected in PKG-18 scope; lifecycle cost analysis to justify premium features if needed — **TBD** *(Analysis location TBD)*

**T-5: Aesthetics vs. Function**
- **Architectural lighting** enhances appearance but may add cost and complexity
- **Functional lighting only** meets safety and operational needs at lower cost
- **Resolution approach:** Balance per ER requirements and stakeholder input — **TBD** *(ER requirements location TBD)*

**T-6: Control Complexity vs. Energy Savings**
- **Advanced controls** (occupancy, daylight, scheduling) provide significant energy savings but add cost, complexity, and maintenance burden
- **Simple controls** (manual switches, contactors) are low-cost and reliable but miss energy-saving opportunities
- **Resolution approach:** PKG-18 scope includes lighting controls; implement control strategies with proven reliability and positive ROI — **ASSUMPTION**

**T-7: Emergency Lighting Extent vs. Cost**
- **Comprehensive emergency lighting** covers all areas but increases cost and complexity
- **Code-minimum emergency lighting** covers egress paths only, lower cost, but may leave operational areas dark during outages
- **Resolution approach:** Meet NFPA 101 and CSA C22.1 code minimums for egress; extend to safety-critical operational areas per ER requirements — **TBD** *(ER location TBD)*

## Examples

**Reference Examples and Precedents:**

**E-1: Typical Lighting Layouts**
- **Exterior site lighting:** Pole-mounted area lights on 30-40 ft poles, spacing per photometric analysis, circuiting by operational zone — **ASSUMPTION** *(Industry practice)*
- **Interior warehouse/process:** High-bay LED fixtures on building structure, typical spacing 20-30 ft, controlled by zone — **ASSUMPTION** *(Industry practice)*
- **Emergency egress:** Wall-mounted emergency lights with battery backup at exit doors, along corridors, at stairwells per NFPA 101 — **ASSUMPTION**

**E-2: Drawing Conventions**
- Fixture symbols per CSA Z32 or project CAD standards — **TBD** *(Standards location TBD)*
- Circuiting shown with dashed lines connecting fixtures to panels
- Control devices (switches, sensors) shown with standard symbols and connected to controlled fixtures — **ASSUMPTION**
- Photometric overlay contours showing illuminance levels (footcandles or lux) as reference from DEL-18.03 — **ASSUMPTION**

**E-3: Anticipated Artifacts**

Per decomposition and _CONTEXT.md:
1. **Exterior lighting layout** — Site plan showing:
   - Exterior area lighting poles and fixtures
   - Building-mounted wall packs and canopy lights
   - Perimeter security lighting
   - Roadway and parking area lighting
   - Circuiting and panel assignments

2. **Interior lighting layout** — Building plans showing:
   - High-bay or linear LED fixtures in process/warehouse areas
   - Office and control room lighting
   - Utility and maintenance area lighting
   - Circuiting and control zones

3. **Emergency lighting layout** — Plan showing:
   - Emergency egress lighting along exit paths
   - Emergency battery-backed fixtures
   - Emergency power sources and circuits
   - Compliance with NFPA 101 requirements

**E-4: Industry Best Practices**
- **Pole foundation coordination:** Civil provides foundation design; lighting provides pole loads and mounting details — **ASSUMPTION**
- **Interdisciplinary checking:** Lighting drawings checked against architectural, civil, and electrical power drawings before issue — **ASSUMPTION**
- **As-built documentation:** Lighting as-builts critical for future maintenance and modifications — **ASSUMPTION** *(To be captured in DEL-18.05 installation records)*

**E-5: Lessons Learned (General)**
- **Early coordination** with hazardous area classification prevents rework when lighting in classified areas discovered late — **ASSUMPTION**
- **Control zoning** aligned with operational areas improves usability and energy savings — **ASSUMPTION**
- **Fixture access** for maintenance often overlooked in initial design; verify maintenance access during design reviews — **ASSUMPTION**

**References for Examples:**
- Employer's Requirements — **TBD** *(Vol 2 Part 1, Part 2, Part 3 — location TBD)*
- IESNA Lighting Handbook — **TBD** *(Location TBD)*
- Industry precedent and best practice examples — **TBD**
- Lessons learned from similar facilities — **TBD**
