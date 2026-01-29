# Guidance: DEL-18.02 Lighting Technical Specification

## Purpose

This guidance document supports the development of the **Lighting Technical Specification** for **PKG-18 Lighting** on the Canola Oil Transload Facility project.

**Deliverable Purpose:** Defines performance, materials, and workmanship requirements for lighting per ER requirements. *(Source: _CONTEXT.md, Decomposition DEL-18.02 description)*

**Role in Project:** This technical specification establishes the procurement and installation requirements for lighting equipment, supporting:
- Contractor procurement of lighting fixtures, poles, and controls
- Quality assurance and verification that equipment meets project requirements
- Installation and workmanship standards for construction
- Testing and commissioning activities (DEL-18.05)
- Warranty and lifecycle support

**Deliverable Classification:**
- **Type:** Specification
- **Discipline:** Electrical
- **Responsible Party:** D&B Contractor

## Principles

**Engineering Rationale (Lighting Specifications):**

**P-1: Performance-Based vs. Prescriptive Specifications**
- **Performance-based:** Specify required performance (lumens, efficacy, CRI) and allow multiple manufacturers — provides competition and cost control — **ASSUMPTION**
- **Prescriptive:** Specify exact manufacturers and models — ensures known performance but may limit competition — **ASSUMPTION**
- **Hybrid approach** (typical): Specify performance requirements and list 3+ acceptable manufacturers or "or equal" — balances quality assurance with competition — **ASSUMPTION**

**P-2: LED Technology Justification**
- LED specified in PKG-18 scope *(Source: Decomposition PKG-18 scope)*
- **LED benefits:**
  - Long life (50,000+ hours) reduces maintenance and replacement costs — supports OBJ-9 (Lifecycle Cost Optimization)
  - High efficacy (100-130+ lm/W) reduces energy consumption — reduces operating costs
  - Good color rendering and instant-on capability — improves safety and usability
  - Dimmable and compatible with advanced controls — enables energy-saving control strategies
- **LED considerations:**
  - Higher initial cost than legacy technologies (HID, fluorescent) — justified by lifecycle savings — **ASSUMPTION**
  - Temperature sensitivity — LED output decreases at high temperatures; fixtures must be thermally managed — **ASSUMPTION**
  - Driver quality critical — poor drivers cause flicker, short life, and power quality issues — **ASSUMPTION**

**P-3: Environmental Durability for Marine/Industrial Setting**
- Fraser Surrey Terminal is a marine environment — salt spray, moisture, temperature extremes
- Fixtures require:
  - **IP65+ for exterior** — dust-tight and protected against water jets — **ASSUMPTION**
  - **IP54+ for interior industrial** — protection against dust and splashing water — **ASSUMPTION**
  - **Corrosion-resistant materials and finishes** — marine-grade aluminum, stainless steel, powder-coat finishes — **ASSUMPTION**
  - **UV-stabilized plastics** for outdoor enclosures and lenses — **ASSUMPTION**

**P-4: Emergency Lighting Code Compliance**
- Emergency egress lighting is life-safety-critical per NFPA 101 and CSA C22.1 — **ASSUMPTION**
- Requirements:
  - **Illumination level:** Minimum 10 lux (1 fc) average, 1 lux (0.1 fc) minimum along egress paths — **TBD** *(Code requirements location TBD)* — **ASSUMPTION**
  - **Duration:** 90 minutes minimum — **TBD** — **ASSUMPTION**
  - **Reliability:** Battery backup with self-test capability, or emergency generator supply with automatic transfer — **ASSUMPTION**
- Specification must clearly define emergency lighting equipment and performance to ensure code compliance — **ASSUMPTION**

**P-5: Control System Integration**
- PKG-18 scope includes lighting controls *(Source: Decomposition PKG-18 scope)*
- Controls enable:
  - **Energy savings** — occupancy sensing, daylight harvesting, scheduling reduces energy waste
  - **Operational flexibility** — zoned control allows selective lighting of areas as needed
  - **Integration with facility systems (PKG-19)** — centralized monitoring and control — **TBD**
- Specification must define control equipment, interfaces, and communication protocols to ensure compatibility with facility control architecture — **ASSUMPTION**

**Applicable Standards Context:**

**Electrical Codes:**
- **CSA C22.1** (Canadian Electrical Code) — Governs electrical installations; specifies wiring, grounding, hazardous location requirements — **ASSUMPTION**
- **NBCC 2020** — Building code requirements for emergency lighting, seismic design — **ASSUMPTION**

**Equipment Standards:**
- **CSA C22.2** and **UL** — Product certification standards; fixtures must be certified by recognized testing laboratory (CSA, UL, ETL) — **ASSUMPTION**
- **IEC 60529** — IP rating system for enclosure protection against dust and water — **ASSUMPTION**

**Lighting Performance Standards:**
- **IESNA** — Industry guidance for illumination levels, quality, and design practices — **TBD** *(Edition and location TBD)*
- **IES LM-79, LM-80, TM-21** — LED photometric testing, lumen maintenance testing, and projection standards — **TBD**

**Life Safety:**
- **NFPA 101** (Life Safety Code) — Emergency lighting requirements for egress paths — **ASSUMPTION**

## Considerations

**Factors to Consider During Specification Development:**

**C-1: Balancing Performance and Cost**
- **Higher performance** (higher CRI, better lumen maintenance, tighter tolerances) increases fixture cost
- **Lower performance** reduces cost but may compromise lighting quality, energy efficiency, or life
- **Resolution approach:**
  - Specify performance levels appropriate to application (higher CRI for task areas, standard for general lighting) — **ASSUMPTION**
  - Use lifecycle cost analysis to justify premium fixtures where energy/maintenance savings offset initial cost — **TBD**

**C-2: Manufacturer Qualifications and Availability**
- **Approved manufacturers list** ensures quality but may limit competition and increase cost — **TBD**
- **Performance-based "or equal"** allows broader competition but requires more thorough submittal review — **ASSUMPTION**
- **Sole-source specifications** may be justified for standardization or unique requirements, but require justification and may face procurement challenges — **TBD**
- Consider:
  - Manufacturer reputation and track record — **ASSUMPTION**
  - Product availability and lead times — **TBD**
  - Local service and support — **TBD**
  - Warranty terms and duration — **TBD**

**C-3: Hazardous Area Classification**
- Canola oil transfer and storage may create hazardous areas (Class I Division 1/2 or Zone 0/1/2 per CSA C22.1) — **TBD** *(Hazardous area classification study location TBD)*
- Fixtures in classified areas require:
  - **Explosion-proof or intrinsically safe design** per classification
  - **Certification and labeling** by recognized testing agency for the specific classification
  - **Higher cost** due to specialized construction — **ASSUMPTION**
- Specification must clearly identify which fixtures are in hazardous areas and specify appropriate ratings — **ASSUMPTION**
- Coordinate with hazardous area classification drawings and electrical discipline — **TBD**

**C-4: Seismic and Structural Requirements**
- Surrey, BC is in a seismically active region — **ASSUMPTION**
- NBCC 2020 seismic requirements apply to lighting poles and fixtures — **ASSUMPTION**
- Specification must require:
  - Pole and foundation design for seismic loads (coordinated with civil discipline) — **ASSUMPTION**
  - Building-mounted fixtures adequately braced or designed for seismic accelerations — **ASSUMPTION**
  - Certification or engineering analysis demonstrating seismic compliance — **TBD**

**C-5: Submittal Requirements**
- Well-defined submittals ensure equipment meets specification before procurement and installation
- Typical submittals for lighting:
  - **Product data sheets** showing fixture performance, dimensions, materials — **ASSUMPTION**
  - **Photometric test reports** (IES files, laboratory test data per IES LM-79) — **ASSUMPTION**
  - **Certifications** (CSA, UL, explosion-proof certification for hazardous areas) — **ASSUMPTION**
  - **Shop drawings** for custom poles, integrated systems, or special installations — **TBD**
  - **Samples** (finishes, lens materials) if required for approval — **TBD**
  - **Warranty documentation** — **TBD**
  - **O&M manuals** — **ASSUMPTION**
- Specification must clearly define submittal requirements and review/approval process — **ASSUMPTION**

**C-6: Warranty and Lifecycle Support**
- LED fixtures have long life but drivers and electronics may fail — warranty critical — **ASSUMPTION**
- Typical LED fixture warranties: 5-10 years — **TBD**
- Specification should define:
  - Warranty duration and coverage (fixtures, drivers, finishes) — **TBD**
  - Warranty service process (repair/replace, on-site vs. return-to-factory) — **TBD**
  - Spare parts requirements — **TBD** — **ASSUMPTION**: Minimum 2% spare fixtures, plus spare drivers and critical components

**C-7: Energy Efficiency and Compliance**
- Energy codes or ER requirements may specify maximum lighting power density (LPD) in watts per square meter — **TBD** *(Energy code or ER location TBD)*
- LED efficacy and controls contribute to meeting LPD limits — **ASSUMPTION**
- Specification should require:
  - Minimum fixture efficacy (lumens/watt) — **TBD**
  - Power factor ≥ 0.90 to reduce reactive power — **ASSUMPTION**
  - Low harmonic distortion (THD < 20%) to minimize power quality issues — **ASSUMPTION**

**C-8: Installation and Workmanship Standards**
- Specification must define acceptable installation practices to ensure safety and performance:
  - Installation per manufacturer instructions — **ASSUMPTION**
  - Compliance with CSA C22.1 wiring and grounding requirements — **ASSUMPTION**
  - Installer qualifications (licensed electricians) — **ASSUMPTION**
  - Coordination with other trades (avoid damage to fixtures during construction) — **ASSUMPTION**
  - Protection of fixtures until final acceptance — **TBD**

**C-9: Testing and Commissioning Requirements**
- Specification defines testing requirements; execution and documentation captured in DEL-18.05 — **ASSUMPTION**
- Typical testing:
  - **Illumination level testing** — verify achieved levels match design calculations (DEL-18.03) — **ASSUMPTION**
  - **Emergency lighting duration test** — verify battery backup provides required duration — **ASSUMPTION**
  - **Control system functional testing** — verify sensors, switches, and integration operate correctly — **ASSUMPTION**
  - **Photocell and daylight sensor calibration** — **TBD**

## Trade-offs

**Competing Concerns to Evaluate:**

**T-1: Performance vs. Cost**
- **Higher-performance fixtures** (higher CRI, better optics, tighter beam control) provide better lighting quality but cost more
- **Standard-performance fixtures** meet basic requirements at lower cost
- **Resolution approach:**
  - Specify higher performance for critical task areas (control rooms, maintenance areas)
  - Use standard performance for general area lighting
  - Justify premium fixtures with lifecycle cost analysis where applicable — **TBD**

**T-2: Sole-Source vs. Multi-Source**
- **Sole-source specifications** (one manufacturer) ensure standardization, simplify spares, but limit competition and may increase cost
- **Multi-source specifications** (3+ manufacturers or "or equal") promote competition and cost control but require more submittal review
- **Resolution approach:**
  - Use multi-source with performance-based requirements and approved manufacturers list (if available) — **TBD**
  - Consider standardization with existing Terminal equipment if Employer has preferences — **TBD**

**T-3: Initial Cost vs. Lifecycle Cost**
- **Lower initial cost** fixtures may have shorter life, lower efficacy, higher maintenance
- **Higher initial cost** (premium LED, better drivers) provides longer life, better efficiency, lower lifecycle cost per OBJ-9
- **Resolution approach:**
  - LED already selected in scope for lifecycle benefits *(Source: Decomposition PKG-18 scope)*
  - Use lifecycle cost analysis to justify premium features (higher-efficacy drivers, extended warranties) — **TBD**

**T-4: Prescriptive Details vs. Performance Flexibility**
- **Prescriptive specifications** (exact models, dimensions, configurations) ensure known outcome but limit contractor flexibility and innovation
- **Performance-based specifications** allow contractor to propose cost-effective solutions meeting performance criteria
- **Resolution approach:**
  - Define performance requirements clearly (lumens, CRI, IP rating, efficacy, etc.)
  - Allow multiple manufacturers or "or equal" with submittal approval process — **ASSUMPTION**

**T-5: Submittal Rigor vs. Review Burden**
- **Rigorous submittals** (detailed test data, certifications, calculations) ensure compliance but increase review time and cost
- **Minimal submittals** speed procurement but may allow non-compliant equipment
- **Resolution approach:**
  - Require submittals for critical performance and safety items (photometric data, certifications, hazardous area ratings) — **ASSUMPTION**
  - Use standard product data sheets for commodity items — **ASSUMPTION**
  - Define clear acceptance criteria in specification to streamline review — **ASSUMPTION**

**T-6: Advanced Controls vs. Simplicity**
- **Advanced controls** (networked, addressable, integrated with BMS/SCADA) provide maximum energy savings and operational flexibility but add cost and complexity
- **Simple controls** (manual switches, basic occupancy sensors) are low-cost and reliable but offer limited energy savings
- **Resolution approach:**
  - PKG-18 scope includes lighting controls *(Source: Decomposition PKG-18 scope)*
  - Implement control strategies with proven reliability and positive return on investment — **ASSUMPTION**
  - Coordinate control system architecture with PKG-19 to ensure integration is feasible and cost-effective — **TBD**

**T-7: Standardization vs. Application-Specific Optimization**
- **Standardization** (few fixture types across all applications) simplifies procurement, reduces spares, easier maintenance
- **Application-specific fixtures** (optimized for each area) may provide better performance or efficiency
- **Resolution approach:**
  - Limit fixture types to 3-5 standard models covering majority of applications
  - Use specialized fixtures only where justified by unique requirements (hazardous areas, high-vibration, etc.) — **ASSUMPTION**

## Examples

**Reference Examples and Precedents:**

**E-1: Typical LED Lighting Specification Sections**

**Exterior LED Area Lighting (CSI 26 56 00):**
- Pole-mounted LED fixtures for site and parking areas
- Performance: 15,000-25,000 lumens per fixture, 120 lm/W efficacy, CRI ≥ 70, 4000-5000K CCT — **ASSUMPTION** *(Values TBD per design)*
- Materials: Marine-grade aluminum housing, powder-coat finish, IP65 minimum, IK08 impact rating
- Mounting: Pole-top or arm-mounted, 30-40 ft pole height typical
- Controls: Photocell for dusk-to-dawn operation, optional time-based dimming

**Interior LED High-Bay Lighting (CSI 26 51 00):**
- High-bay LED fixtures for warehouse/process areas
- Performance: 20,000-30,000 lumens per fixture, 130+ lm/W, CRI ≥ 80, 4000-5000K CCT
- Materials: Aluminum housing, tempered glass or polycarbonate lens, IP54 minimum
- Mounting: Pendant or surface-mounted, 20-30 ft mounting height typical
- Controls: Occupancy sensors for unoccupied areas, daylight harvesting if skylights present

**Emergency Lighting (CSI 26 52 00):**
- LED emergency fixtures with integral battery backup
- Performance: Per NFPA 101 (10 lux average, 1 lux minimum, 90-minute duration)
- Battery: Sealed lead-acid or lithium-ion, self-test capability
- Mounting: Wall or ceiling-mounted at exits, corridors, stairwells
- Testing: Monthly 30-second test, annual 90-minute test per code

**Lighting Controls (CSI 26 09 00 or within lighting sections):**
- Occupancy/vacancy sensors: PIR or ultrasonic, adjustable time delay
- Photocells and daylight sensors: 0-10V dimming or relay control
- Networked lighting control panel (if applicable): BACnet or DALI protocol, integration with PKG-19

**E-2: Submittal Requirements Example**

Typical specification language for submittals:
- "Submit product data sheets for all fixture types, showing photometric performance, electrical characteristics, materials, finishes, and certifications."
- "Submit IES photometric test reports per IES LM-79 for all fixture types."
- "Submit certifications (CSA or UL) demonstrating compliance with CSA C22.2 No. 250.0 or equivalent."
- "For fixtures in hazardous locations, submit certification and labeling demonstrating compliance with CSA C22.1 requirements for the specified classification."
- "Submit shop drawings for custom lighting poles showing dimensions, materials, finishes, and foundation interface details."
- "Submit warranty documentation covering minimum 5 years for fixtures and 3 years for drivers." — **TBD**

**E-3: Anticipated Artifacts**

Per decomposition and _CONTEXT.md:
1. **LED lighting specification** — Technical specification covering LED fixtures, poles, supports, performance, materials, installation
2. **Lighting controls specification** — Technical specification for sensors, switches, panels, integration with PKG-19
3. **Emergency lighting specification** — Technical specification for emergency fixtures, battery backup, testing requirements

**E-4: Industry Best Practices**

- **Specify L70 lumen maintenance** (70% output at rated life) rather than L50 — more conservative and ensures acceptable lighting quality over fixture life — **ASSUMPTION**
- **Require LM-79 photometric test data** from independent testing lab — ensures reported performance is accurate — **ASSUMPTION**
- **Use "or equal" provisions** with clear acceptance criteria — promotes competition while ensuring quality — **ASSUMPTION**
- **Define warranty clearly** — specify what is covered (fixtures, drivers, finishes), duration, and service process (on-site repair vs. return-to-factory) — **TBD**
- **Coordinate with electrical and controls early** — lighting loads, circuit requirements, and control interfaces affect electrical and control system design — **ASSUMPTION**

**E-5: Lessons Learned (General)**
- **Avoid over-specifying aesthetics** unless appearance is critical; focus on performance and durability for industrial facilities — **ASSUMPTION**
- **Verify commercial availability** of specified performance levels before finalizing specification — some performance combinations may not be available or only from limited sources — **TBD**
- **Consider maintenance access** when specifying pole heights and mounting methods — very tall poles may require specialized equipment for maintenance — **ASSUMPTION**
- **Plan for spare parts** early — LED fixtures are long-life but drivers can fail; specify spare fixtures and critical components (drivers, sensors) — **TBD**

**References for Examples:**
- Employer's Requirements — **TBD** *(Vol 2 Part 1, Part 2, Part 3 — location TBD)*
- CSI MasterFormat specifications — **TBD** *(If project uses CSI format)*
- Industry standards (IESNA, CSA, UL) — **TBD**
- Manufacturer product data (for reference, not endorsement) — **TBD**
