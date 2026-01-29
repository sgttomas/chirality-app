# Datasheet: DEL-23.03 Fire Protection Design Calculations

## Identification

| Field | Value |
|-------|-------|
| Deliverable ID | DEL-23.03 |
| Name | Fire Protection Design Calculations |
| Package | PKG-23 Fire Protection |
| Discipline | Specialty |
| Type | Calculation |
| Responsible | D&B Contractor |
| Status | INITIALIZED |
| Project | Canola Oil Transload Facility — Phase 1 |
| Location | Fraser Surrey Terminal, 11060 Elevator Road, Surrey, BC |

## Attributes

| Attribute | Value | Source |
|-----------|-------|--------|
| Calculation Package Number | **TBD** | **ASSUMPTION**: Per project calculation numbering system (e.g., CALC-23-03 or similar) |
| Calculation Software | Hydraulic analysis software (AFT Fathom, PIPE-FLO, or equivalent) for hydraulic calculations; spreadsheet (Excel) or MathCAD for fire water demand calculations | **ASSUMPTION**: Standard fire protection calculation tools |
| Design Codes/Standards | NFPA 30, NFPA 24, NFPA 11, NFPA 16, NFPA 72 | **ASSUMPTION**: Fire protection design standards |
| Calculation Type | Sizing and verification | Decomposition: provides engineering basis and sizing/verification calculations |
| Revision | Rev 0 (initial issue) | **ASSUMPTION**: Initial design phase |
| Classification | For Design & Construction | Decomposition: DEL-23.03 |
| Calculation Format | Calculation packages with cover sheet, input data, methodology, calculations, results, references | **ASSUMPTION**: Standard calculation package format |
| Calculation Retention | Per project record retention requirements — **TBD** (typically 25+ years for design calculations) | **ASSUMPTION**: Permanent design record |

## Conditions

**Project Context:**

This calculation package provides the engineering basis and sizing/verification calculations for fire protection systems serving a canola oil transload facility with the following conditions:

| Condition | Value | Source |
|-----------|-------|--------|
| Facility Type | CSD Canola Oil Transload | Decomposition Section 1.1 |
| Permitted Throughput | 1,000,000 MT per annum | Decomposition Section 1.1 |
| Storage Capacity | 45,000 MT (3 × 15,000 MT tanks) | Decomposition Section 1.1 |
| Railcar Capacity | 32 unloading stations on 2 tracks | Decomposition Section 1.1 |
| Product Classification | Combustible liquid (Class IIIA per NFPA 30) | **ASSUMPTION**: CSD canola oil flash point typically >93°C (200°F) |
| Operating Temperature Range | -40°C to +40°C ambient | **ASSUMPTION**: Fraser Valley climate, BC |
| Design Life | 25 years minimum | **ASSUMPTION**: Typical industrial facility |

**Calculation Scope:**

| Calculation | Purpose | Source |
|-------------|---------|--------|
| Fire Water Demand Calculation | Determine total fire water demand (flow rate and duration) based on NFPA 30 requirements for combustible liquid storage, transfer operations, and exposure protection | Decomposition: fire water demand calculations (anticipated artifact) and **ASSUMPTION** |
| Hydraulic Calculation | Verify fire water distribution system can deliver required flow and pressure to all hydrants and fire protection equipment; size fire water piping and fire pump (if required) | Decomposition: hydraulic calculations (anticipated artifact) and **ASSUMPTION** |

**Additional Calculations (typical):**

| Calculation | Purpose | Source |
|-------------|---------|--------|
| Tank Foam System Calculations | Size foam concentrate storage, foam proportioning system, and foam discharge devices for storage tank foam systems per NFPA 11/16 | **ASSUMPTION**: Required for combustible liquid storage tanks |
| Marine Loading Foam System Calculations | Size foam system for marine loading arms per NFPA 11/16 | **ASSUMPTION**: Required for marine loading protection |
| Fire Pump Sizing Calculation (if applicable) | Determine fire pump capacity, head, and power requirements to meet fire water demand | **ASSUMPTION**: If fire pump in Contractor scope |
| Fire Alarm System Calculations | Battery capacity calculation per NFPA 72; audibility/visibility coverage calculations | **ASSUMPTION**: Fire alarm system design |

## Construction

**Calculation Package Contents:**

**Fire Water Demand Calculation:**

| Calculation Element | Content | Source/Basis |
|---------------------|---------|--------------|
| Design Basis | Facility description, product properties, fire protection zones, applicable codes (NFPA 30) | **ASSUMPTION**: Standard calculation inputs |
| Input Data | Tank sizes, spacing, diameters; marine loading arm flow rates; railcar unloading area dimensions; building areas; exposure distances | From DEL-23.01 drawings and facility design |
| Methodology | NFPA 30 methodology for combustible liquid facility fire water demand: largest single tank foam system demand + cooling water for exposures + hydrant/monitor streams + marine/rail loading protection | **ASSUMPTION**: NFPA 30 approach for Class IIIA combustible liquids |
| Calculations | Tank foam system demand (gpm, duration); tank cooling demand (gpm); hydrant/monitor demand (gpm, number of streams); marine loading foam demand (gpm); total fire water demand (gpm) and duration (hours) | **ASSUMPTION**: Standard fire water demand calculation components |
| Results | Total fire water demand: **TBD** gpm for **TBD** hours | To be calculated |
| References | NFPA 30, tank manufacturer foam system design, insurance requirements (if applicable) | **ASSUMPTION**: Calculation references |

**Hydraulic Calculation:**

| Calculation Element | Content | Source/Basis |
|---------------------|---------|--------------|
| Design Basis | Fire water distribution system layout, fire water demand | From DEL-23.01 drawings and fire water demand calculation above |
| Input Data | Fire water loop piping layout, pipe lengths, pipe sizes (initial assumption or from drawings), elevation changes, hydrant locations, fire pump characteristics (if applicable) | From DEL-23.01 drawings |
| Methodology | Hydraulic analysis using Hazen-Williams or Darcy-Weisbach equation; analyze fire water loop for most hydraulically remote hydrant/demand point; model fire water system in hydraulic analysis software | **ASSUMPTION**: Standard hydraulic analysis approach |
| Calculations | Pipe friction losses, elevation head, velocity head, pressure at hydrants, fire pump head and flow (if applicable), system curve | **ASSUMPTION**: Hydraulic calculation components |
| Results | Available pressure at hydrants: **TBD** psi at **TBD** gpm (compare to required pressure); pipe sizes verified adequate or adjusted; fire pump capacity: **TBD** gpm at **TBD** psi (if required) | To be calculated |
| References | NFPA 24, hydraulic analysis software user manual, pipe roughness coefficients | **ASSUMPTION**: Calculation references |

**Tank Foam System Calculations:**

| Calculation Element | Content | Source/Basis |
|---------------------|---------|--------------|
| Design Basis | Storage tank sizes, product type, foam system type (fixed chamber or foam maker) | From DEL-23.01 drawings and DEL-23.02 specification |
| Input Data | Tank diameter, foam application rate per NFPA 11/16 (**TBD** gpm/ft²), foam concentrate percentage (3% or 6%), discharge duration (**TBD** minutes, typically 55 minutes for hydrocarbon foams) | From NFPA standards and design criteria |
| Methodology | NFPA 11/16 methodology for tank foam system sizing | **ASSUMPTION**: NFPA standards |
| Calculations | Tank surface area (ft²), foam solution demand (gpm), foam concentrate demand (gpm), foam concentrate storage volume (gallons), foam proportioning system capacity (gpm), foam discharge device capacity (gpm) | **ASSUMPTION**: Standard foam system calculation components |
| Results | Foam concentrate storage: **TBD** gallons; foam proportioning system: **TBD** gpm; foam discharge device: **TBD** gpm | To be calculated |
| References | NFPA 11, NFPA 16, foam equipment manufacturer data | **ASSUMPTION**: Calculation references |

**Fire Pump Sizing Calculation (if applicable):**

| Calculation Element | Content | Source/Basis |
|---------------------|---------|--------------|
| Design Basis | Fire water demand, available water supply pressure | From fire water demand calculation and supply source data |
| Input Data | Total fire water demand (gpm), required pressure at most remote hydrant (psi), available supply pressure (psi), fire pump location elevation | From calculations and site data |
| Methodology | NFPA 20 fire pump sizing methodology | **ASSUMPTION**: NFPA 20 standard |
| Calculations | Fire pump head (ft or psi), fire pump capacity (gpm, typically 150% of demand per NFPA 20), fire pump power (HP or kW), fire pump selection (pump curve) | **ASSUMPTION**: Standard fire pump sizing |
| Results | Fire pump capacity: **TBD** gpm at **TBD** psi (**TBD** HP/kW) | To be calculated |
| References | NFPA 20, fire pump manufacturer pump curves | **ASSUMPTION**: Calculation references |

## References

**Decomposition and Context:**
- Decomposition document: `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md`, Section 5 (PKG-23), DEL-23.03
- Deliverable context: `_CONTEXT.md`

**Applicable Codes and Standards:**
- NFPA 30: Flammable and Combustible Liquids Code — fire water demand basis
- NFPA 24: Installation of Private Fire Service Mains — hydraulic design requirements
- NFPA 20: Installation of Stationary Pumps for Fire Protection — fire pump sizing
- NFPA 11: Low-, Medium-, and High-Expansion Foam — foam system design
- NFPA 16: Installation of Foam-Water Sprinkler and Foam-Water Spray Systems — tank foam systems
- NFPA 72: National Fire Alarm and Signaling Code — fire alarm system calculations

**Cross-References:**
- DEL-23.01: Fire Protection Design Drawing Set — provides system layouts, pipe routing, equipment locations as calculation inputs
- DEL-23.02: Fire Protection Technical Specification — calculation results inform specification performance requirements
- DEL-23.04: Fire Protection Data Sheet Package — equipment data sheets provide equipment characteristics for calculations
- DEL-23.05: Fire Protection Installation & Test Records — testing verifies calculation assumptions and results
