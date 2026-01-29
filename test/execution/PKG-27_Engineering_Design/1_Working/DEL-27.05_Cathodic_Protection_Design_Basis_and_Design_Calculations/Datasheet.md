# Datasheet: DEL-27.05 Cathodic Protection Design Basis & Design Calculations

## Identification

| Field | Value |
|-------|-------|
| Deliverable ID | DEL-27.05 |
| Name | Cathodic Protection Design Basis & Design Calculations |
| Package | PKG-27 Engineering Design |
| Discipline | Design |
| Type | Calculation |
| Responsible | D&B Contractor (CP Specialist) |
| Status | INITIALIZED |

## Attributes

| Attribute | Value |
|-----------|-------|
| CP System Type | Impressed Current Cathodic Protection (ICCP) or Sacrificial Anode (Galvanic) — **TBD** |
| Structures Protected | Storage tanks, buried piping, marine structures (piles, sheet piles, loading platform) |
| Design Life | **TBD** — Typical 25-30 years for ICCP; 20-25 years for sacrificial anodes |
| Soil/Water Resistivity | **TBD** — From site investigation (critical design parameter) |
| Current Density Criteria | Per NACE SP0169 or CSA Z662 — **TBD** |
| Calculation Software | Hand calculations or specialized CP software — **TBD** |

**Source:** _CONTEXT.md; **ASSUMPTION**: Standard CP design for industrial facility with buried/marine structures

## Conditions

**Project Context:**

| Parameter | Value | Source |
|-----------|-------|--------|
| Facility Type | Canola oil transload facility (rail-to-ship) | Decomposition Section 1.1 |
| Location | Fraser Surrey Terminal (marine/waterfront) | Decomposition Section 1.1 |
| Structures Requiring CP | Storage tanks, buried piping, marine structures | **ASSUMPTION** |
| Environmental Conditions | Marine/waterfront, saline environment, corrosive soil/water | Decomposition Section 1.1; **ASSUMPTION** |

**Corrosion Environment:**

Fraser Surrey Terminal is marine waterfront environment on Fraser River:
- **Soil conditions:** Waterfront soils likely brackish, conductive, corrosive — **TBD** from geotechnical investigation
- **Water conditions:** Brackish water (mix of fresh and salt water), conductive, corrosive to steel structures
- **Atmospheric conditions:** Marine atmosphere, salt spray, high humidity — corrosive to above-ground steel
- **Stray current:** Potential for stray current interference from rail systems, other facilities — **TBD**

**Cathodic protection typically required for:**
1. **Underground Storage Tanks (3 × 15,000 MT):** Tank bottoms in contact with soil (if not on concrete pad with liner)
2. **Buried Piping:** Underground transfer piping, fire water piping, utilities
3. **Marine Structures:** Steel sheet piling, pipe piles, loading platform structures submerged or in splash zone
4. **Steel Foundations:** Embedded steel foundations for equipment, pipe racks (if applicable)

**Source:** Decomposition Section 1.1; **ASSUMPTION**: Typical CP scope for marine transload facility; **TBD** — Specific structures requiring CP from corrosion assessment

**Design Parameters (to be determined from site investigation and codes):**

- **Soil resistivity:** **TBD** — Ω-cm (critical for buried structures CP design)
- **Water resistivity:** **TBD** — Ω-cm (critical for marine structures CP design)
- **Current density requirements:** **TBD** — mA/m² per NACE SP0169 or CSA Z662 (varies by structure type, coating quality, environment)
- **Structure surface areas:** **TBD** — m² (from structural/piping drawings)
- **Coating efficiency:** **TBD** — % (assumed coating efficiency affects current demand; 90-95% typical for new well-coated structures)
- **Design life:** **TBD** — years (drives anode sizing for sacrificial systems or rectifier sizing for ICCP)

**Source:** **ASSUMPTION**: Standard CP design parameters; **TBD** — Specific values from site data and design codes

## Construction

**Anticipated Artifacts:**

Per _CONTEXT.md and decomposition DEL-27.05 entry:
1. **CP Design Basis** — Document establishing CP system requirements, design criteria, methodology
2. **Anode Layout Calculations** — Sizing and spacing of anodes (sacrificial or impressed current)
3. **Current Demand Calculations** — Total protection current required for all structures
4. **Design Drawings** (where applicable) — Anode locations, rectifier locations, connections, test stations

**CP Design Basis (typical content):**
- Structures to be protected (inventory)
- Corrosion environment assessment (soil/water resistivity, stray current, coatings)
- CP criteria (potential requirements per NACE SP0169 or CSA Z662)
- CP system selection (ICCP vs. sacrificial anodes; rationale)
- Design life
- Current density assumptions
- Coating assumptions
- Design methodology and standards
- Maintenance and monitoring requirements

**Current Demand Calculations (typical methodology):**
- Determine protected surface area for each structure (from drawings)
- Apply current density per structure type and coating quality
- Calculate total current demand: I = Surface Area × Current Density × (1 - Coating Efficiency)
- Include design margin (typical 20-50%) for uncertainties and coating degradation over time

**Anode Layout Calculations:**

For **ICCP (Impressed Current):**
- Size rectifier capacity based on total current demand + margin
- Determine anode bed configuration (deep well, distributed, etc.)
- Calculate anode resistance to soil/water (depends on resistivity, anode geometry)
- Verify voltage output adequate to drive required current
- Layout anodes for uniform current distribution

For **Sacrificial Anodes (Galvanic):**
- Select anode material (zinc, magnesium, aluminum alloys) based on environment
- Calculate anode current output capacity (depends on anode-to-structure potential difference, anode resistance, circuit resistance)
- Size anodes for design life: Anode Mass = (Current Demand × Design Life × 8760 hr/year) / (Utilization Factor × Capacity)
- Determine number and spacing of anodes for uniform distribution
- Verify anode output adequate to meet protection criteria

**Design Drawings (typical):**
- Anode locations on site plan (buried anodes, marine anodes on underwater structures)
- Rectifier locations (for ICCP)
- Cable routing (anode cables, structure bonds)
- Test station locations (for monitoring CP effectiveness)
- Connection details

**Source:** **ASSUMPTION**: Standard CP calculation methodology per NACE, CSA Z662, and industry practice; **TBD** — Specific calculations from CP specialist

## References

**Primary References:**

- Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md
- _CONTEXT.md (DEL-27.05)
- Site geotechnical investigation report (soil resistivity data) — **location TBD**
- Site environmental assessment (water quality, stray current survey) — **location TBD**
- Structural drawings (tank foundations, piles, sheet piles) — **TBD** (from PKG-05, PKG-06, PKG-08)
- Piping drawings (buried piping routes, materials) — **TBD** (from PKG-14)
- Coating specifications (tank, piping, marine structures) — **TBD**

**Applicable Standards and Codes:**

- **NACE SP0169:** Control of External Corrosion on Underground or Submerged Metallic Piping Systems — **location TBD**
- **NACE TM0497:** Measurement Techniques Related to Criteria for Cathodic Protection on Underground or Submerged Metallic Piping Systems — **location TBD**
- **CSA Z662:** Oil and Gas Pipeline Systems (includes CP requirements) — **location TBD**
- **NACE SP0176:** Corrosion Control of Steel Fixed Offshore Platforms Associated with Petroleum Production (for marine structures if applicable) — **location TBD**
- **DNV RP-B401:** Cathodic Protection Design (for marine structures) — **location TBD**
- **ISO 15589 series:** Petroleum and natural gas industries — Cathodic protection — **location TBD**
- **TBD** — Canadian or BC-specific codes for cathodic protection

**Cross-References:**

- PKG-05: Concrete Structures (storage tank foundations)
- PKG-08: Marine Structures (piles, sheet piles, loading platforms requiring CP)
- PKG-13: Storage Tanks (tank bottom CP requirements)
- PKG-14: Process Piping (buried piping CP requirements)
- DEL-27.01: Design Basis Documents (corrosion protection philosophy)
- See `_DEPENDENCIES.md` (NOT_TRACKED — dependencies coordinated externally)

**Source:** **ASSUMPTION**: Standard CP design references and codes; **TBD** — Specific code editions and data sources
