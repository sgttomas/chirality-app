# Guidance: DEL-05.03 Concrete Structures Design Calculations

## Purpose

- Guide development of the **Concrete Structures Design Calculations** so they substantiate foundations, containment walls, and seismic design basis for PKG-05. (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:234.)
- Ensure calculations support project objectives (OBJ-3 Storage Capacity 45,000 MT, OBJ-7 Environmental Protection) through appropriate design verification and containment analysis. (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:782; test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:786; test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:41-42.)
- Provide calculation approach that supports constructability, quality verification, and long-term facility performance. (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:58.)

## Principles

**P-01: Traceability and Reproducibility**
Clearly state assumptions, inputs, load cases, and governing requirements so an independent checker can reproduce results:
- All inputs shall have source citations (Employer's Requirements, geotechnical reports, equipment data sheets, etc.)
- All assumptions shall be explicitly stated and justified (or flagged as TBD for future resolution)
- All code references shall cite specific clause numbers (e.g., "per CSA A23.3 Cl. 8.4.2")
- All calculation steps shall be documented or software input/output files retained
- Results shall be summarized in tables for easy verification
- Checker shall be able to verify key results independently without extensive reverse-engineering
(Source: test/Volume_2_Part_1_Employers_Requirements.pdf, location TBD; Specification.md: QR-03; Procedure.md: Steps.)

**P-02: Containment Sensitivity (OBJ-7 Environmental Protection)**
Treat containment wall serviceability as a critical performance consideration:
- **Crack control:** Analyze crack widths under service loads and verify against containment integrity limits (typically more stringent than general structural limits)
- **Joint design:** Evaluate construction joints, control joints, and expansion joints for leakage potential; provide detailing recommendations
- **Leakage pathways:** Consider penetrations, waterstop interfaces, liner connections as potential leakage paths
- **Serviceability load cases:** Include hydrostatic pressure scenarios (full containment, partial containment, product spillage)
- **Long-term durability:** Consider creep, shrinkage, and temperature effects on crack development over facility lifetime
- **TBD:** Specific crack width limits and serviceability criteria from Employer's Requirements
(Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:226; test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:786; Specification.md: FR-04; Specification.md: PR-01.)

**P-03: Evidence-Based Code Application**
Do not assert specific code clauses without accessible sources; flag governing codes/clauses as **TBD** until extracted from Employer's Requirements:
- Reference specific code sections only when confirmed from Employer's Requirements
- Do not invent code requirements based on assumption or general knowledge
- Flag unconfirmed code requirements as **TBD** and note they require extraction from ERs
- When codes are confirmed, ensure they are current and applicable to BC location
- Justify any departures from code requirements with engineering rationale
(Source: test/Volume_2_Part_2_Employers_Requirements.pdf, location TBD; Specification.md: Standards; Datasheet.md: Attributes.)

**P-04: Design Optimization Balance**
Balance design optimization with constructability and risk management:
- Optimize element sizing for material efficiency while maintaining constructability (avoid excessive reinforcement congestion)
- Use engineering judgment to avoid over-conservatism that adds cost without significant safety benefit
- Document optimization decisions and trade-offs (e.g., deeper foundation vs more reinforcement)
- Consider lifecycle costs in optimization (initial cost vs maintenance, durability)
- Maintain adequate design margins for uncertainty in assumptions (especially where inputs are TBD)
(Source: Specification.md: PR-03; Procedure.md: Steps.)

**P-05: Consistency Across Deliverables**
Ensure calculation assumptions and results are consistent with drawings (DEL-05.01) and specifications (DEL-05.02):
- Material properties (concrete strength, modulus) shall match DEL-05.02 specification values
- Element dimensions (foundation thickness, wall height, pad size) shall match DEL-05.01 drawing dimensions
- Reinforcement quantities calculated shall be feasible for the element size shown on drawings
- Cover requirements assumed in calculations shall match DEL-05.02 specification cover requirements
- Coordinate with drawing and specification development during iterative design process
(Source: Specification.md: IR-01; test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:232; test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:233.)

## Considerations

**C-01: Input Data Requirements (Dependencies Coordinated Externally)**
Multiple inputs are required for calculations (dependencies coordinated externally per NOT_TRACKED mode):
- **Geotechnical parameters (from PKG-02 DEL-02.04):**
  - Bearing capacity (allowable bearing pressure, ultimate bearing capacity factors)
  - Settlement parameters (compression indices, consolidation parameters)
  - Soil properties (unit weight, friction angle, cohesion, passive pressure coefficients)
  - Groundwater levels and seasonal variations
  - Soil-structure interaction parameters (subgrade modulus, lateral earth pressure coefficients)
- **Equipment loads (from PKG-10, PKG-11, PKG-13, PKG-15):**
  - Dead loads (equipment weight, piping weight, insulation, platforms)
  - Live loads (maintenance loads, access loads)
  - Operating loads (product weight for 45,000 MT storage, dynamic loads, vibration)
  - Thermal loads (temperature differentials, expansion/contraction)
  - Seismic loads (equipment seismic response factors, amplification)
- **Piping loads (from PKG-14):**
  - Pipe support loads (dead, operating, thermal, seismic)
  - Thrust loads for thrust block design (pressure thrust, thermal thrust)
  - Anchor loads and moments
- **Design basis documents:**
  - Seismic design parameters (spectral accelerations, site class, importance factors)
  - Load combinations and load factors
  - Material properties and design strengths
  - Serviceability limits (crack widths, settlement, deflection)

**Coordination approach:**
- Request inputs early in design process
- Document assumptions for missing inputs and flag as TBD
- Maintain assumptions register and update calculations when inputs are confirmed
- Conduct sensitivity analysis for critical uncertain inputs
(Source: `_DEPENDENCIES.md`; test/execution/_Coordination/_COORDINATION.md; Specification.md: FR-02; Specification.md: IR-01; Procedure.md: Prerequisites.)

**C-02: Serviceability Criteria Importance**
Serviceability often governs concrete design for operational facilities:
- **Foundation settlement:** May govern foundation sizing more than bearing capacity (especially for large tank foundations)
- **Differential settlement:** Critical for equipment alignment, piping connections, tank levelness
- **Crack control:** Critical for containment walls (OBJ-7), affects durability for all elements
- **Deflection:** May govern for equipment pads supporting sensitive equipment
- **Vibration:** May govern for pads supporting rotating equipment
- **TBD:** Specific serviceability limits from Employer's Requirements (settlement tolerances, crack width limits, vibration criteria)
(Source: Specification.md: PR-01; test/Volume_2_Part_2_Employers_Requirements.pdf, location TBD.)

**C-03: Seismic Design Importance**
BC location requires thorough seismic design:
- **Seismic zone:** BC is in moderate to high seismic zone; seismic loads may govern design
- **Importance factors:** Storage facility with environmental containment likely has elevated importance factors
- **Soil-structure interaction:** Soft soils (if present) may amplify seismic response
- **Liquid storage:** Sloshing and hydrodynamic effects for tank foundations (coordinate with PKG-13 tank design)
- **Containment integrity:** Seismic loads must not compromise containment integrity (OBJ-7)
- **Ductile detailing:** Identify where ductile detailing is required vs capacity-protected elements
- **TBD:** Specific seismic design parameters from Employer's Requirements and geotechnical investigation (site class, spectral accelerations)
(Source: Specification.md: FR-05; Specification.md: PR-02; Datasheet.md: Conditions; test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:10.)

**C-04: Methodology Selection**
Select calculation methodology appropriate to element type and complexity:
- **Hand calculations:** Appropriate for simple elements (small equipment pads, thrust blocks, preliminary sizing)
- **Spreadsheets:** Appropriate for repetitive calculations (multiple equipment pads, parametric studies)
- **Finite element analysis (FEM):** Appropriate for complex elements (large tank foundations, containment walls with complex loading, soil-structure interaction)
- **Software validation:** If using software, verify software is validated for intended application and results are checked for reasonableness
- **Document methodology selection:** Justify methodology choice and note limitations/assumptions
- **ASSUMPTION:** Methodology selection per standard structural engineering practice; specific software TBD per Contractor standards
(Source: Specification.md: FR-06; Datasheet.md: Attributes; Procedure.md: Steps.)

**C-05: Assumption Management**
Many inputs will be TBD early in design; manage assumptions systematically:
- **Assumptions register:** Maintain a register of all provisional assumptions with impact assessment
- **Conservative assumptions:** Use conservative values where inputs are uncertain (balance risk vs cost)
- **Assumption tracking:** Flag assumptions in calculations clearly and track resolution
- **Sensitivity analysis:** For critical assumptions, perform sensitivity analysis to understand impact
- **Update trigger:** Define when calculations must be updated (e.g., when actual loads exceed assumed loads by X%)
- **Communication:** Communicate assumptions to drawing and specification development so they are aligned
(Source: Specification.md: FR-02; Specification.md: IR-02; Procedure.md: Steps; Procedure.md: Prerequisites.)

## Trade-offs

**T-01: Conservatism vs Constructability**
Conservative design (larger sections, more reinforcement) reduces structural risk but can create construction challenges:
- **Issue:** Overly conservative sections may create reinforcement congestion, formwork complexity, or excessive concrete volumes
- **Risk reduction:** Conservative design provides margin for uncertainties, load increases, future modifications
- **Cost/schedule impact:** Larger sections increase material cost, formwork cost, and potentially construction duration
- **Balance approach:** Use appropriate safety factors per code; avoid adding extra conservatism unless justified by uncertainty or future loads
- **Optimization:** Optimize sections for reinforcement placement (avoid congestion while meeting strength/serviceability requirements)
(Source: Specification.md: PR-03; Guidance.md: P-04.)

**T-02: Modeling Detail vs Schedule**
Detailed analysis (3D FEM, soil-structure interaction, nonlinear analysis) improves accuracy but adds time and cost:
- **Detailed analysis benefits:** More accurate results, better understanding of behavior, may allow optimization
- **Detailed analysis costs:** Requires specialized software, more engineering time, longer review/verification time
- **When detailed analysis is warranted:** Large/complex structures, critical elements (containment walls), elements where simple methods are very conservative
- **When simple methods suffice:** Small/repetitive elements, preliminary design, elements with ample design margin
- **Decision criteria:** Consider element importance, cost impact of conservatism, schedule constraints, available tools/expertise
(Source: Guidance.md: C-04.)

**T-03: Design Maturity vs Drawing Issue Timing**
Calculations mature iteratively; coordinate with drawing and specification issue timing:
- **Early calculations (preliminary):** Support early drawing issue and procurement but may require later revisions
- **Mature calculations (final):** Fully verified with all inputs confirmed, support final drawings, minimize revisions
- **Issue:** Early drawing issue supports schedule but may require design changes; late issue ensures accuracy but delays construction
- **Approach:** Issue calculations and drawings in stages aligned with input maturity (e.g., foundation calcs when geotech complete, equipment pad calcs when equipment data available)
- **Revision management:** Plan for calculation and drawing revisions as design matures; track revision impacts on construction
(Source: Specification.md: IR-01; Procedure.md: Steps.)

**T-04: Standardization vs Optimization**
Standardized designs (e.g., all equipment pads same size) simplify construction but may not be most cost-effective:
- **Standardization benefits:** Simplified drawings, repetitive formwork, reduced design effort, reduced potential for errors
- **Optimization benefits:** Material savings, reduced foundation volumes, potentially faster construction (less material placement)
- **When to standardize:** Multiple similar elements, modest cost difference, construction efficiency gain
- **When to optimize:** Large elements with significant cost difference, critical elements requiring precise sizing
- **Balance:** Standardize small elements (e.g., pump pads), optimize large elements (e.g., tank foundations)

## Examples

**E-01: Calculation Package Organization (Example Structure)**
Expected calculation set organization:
1. **Calculation Package Cover and Index**
   - Cover sheet with project info, calculation package title, revision, approvals
   - Calculation index listing all calculations by element type

2. **Design Basis Section**
   - Design basis statement (Employer's Requirements, applicable codes)
   - Input data register (loads, geotech, materials, code parameters)
   - Assumptions register (provisional parameters, TBD items)
   - Load combination summary

3. **Foundation Calculations**
   - Tank foundation calculations (3 tanks × calculation set each)
   - Equipment pad calculations (by equipment type or grouped if similar)
   - Building foundation calculations (if in scope)
   - Thrust block calculations (by location or grouped if similar)

4. **Containment Wall Calculations**
   - Structural design calculations (earth pressure, hydrostatic, sizing, reinforcement)
   - Serviceability calculations (crack control, joint design)
   - Seismic calculations (dynamic earth pressure, stability)

5. **Seismic Analysis**
   - Seismic design basis (zone, site class, spectral values, importance factors)
   - Seismic methodology description
   - Element-specific seismic analysis (foundations, walls, pads, thrust blocks)

6. **Results Summary and Recommendations**
   - Results summary tables (element sizes, reinforcement quantities, demand/capacity ratios)
   - Design verification statement
   - Recommendations for drawings and specifications

7. **Independent Check Records**
   - Checker comments and resolutions
   - Checker sign-off

(Source: Datasheet.md: Construction; Specification.md: Documentation.)

**E-02: Calculation Traceability Example (Good Practice)**

**Good calculation (traceable, reproducible):**
- "Tank foundation design loads:
  - Dead load (tank + structure): 500 kN (per PKG-13 tank data sheet, Rev B)
  - Product storage load (15,000 MT at 0.92 specific gravity): 135,450 kN (per decomposition §1.2)
  - Live load (maintenance): 10 kN (per NBCC Table 4.1.5.3, assembly areas)
  - Seismic load: Calculated per CSA A23.3 Cl. 21.2 using Ie = 1.3 (storage facility importance)
  - Load combination (governing): 1.0D + 1.0L + 1.0E per NBCC Load Combination 4
  - Total factored load: 147,123 kN
  - Required bearing area (allowable bearing pressure 150 kPa per geotech report): 981 m²
  - Foundation diameter selected: 35 m (area = 962 m², within 2% of required, acceptable)"

**Poor calculation (not traceable):**
- "Tank foundation: Need 35m diameter foundation." (Where did loads come from? What is bearing capacity? How was size determined?)

(Source: Guidance.md: P-01; Specification.md: QR-03.)

**E-03: Containment Wall Serviceability Example (OBJ-7 Focus)**

**Good serviceability analysis:**
- "Containment wall crack control analysis (OBJ-7 Environmental Protection):
  - Wall dimensions: 3.5 m height, 300 mm thickness
  - Service load case: Earth pressure + hydrostatic (full containment scenario)
  - Maximum flexural stress: 2.8 MPa (service loads, uncracked section)
  - Expected crack width: Calculated per CSA A23.3 Cl. 10.6 = 0.18 mm
  - Allowable crack width for liquid containment: 0.30 mm (per Employer's Req Vol 2 Part 2 § TBD)
  - Result: Crack width 0.18 mm < 0.30 mm allowable — ACCEPTABLE
  - Recommendation: Waterstops required at construction joints per DEL-05.01 drawing notes; crack control reinforcement per DEL-05.02 specification Cl. X.X"

(Source: Guidance.md: P-02; Specification.md: FR-04; Specification.md: PR-01.)

## Local Conflict Table

No conflicts identified from accessible sources. Governing design criteria and code clauses pending extraction from Employer's Requirements. (Source: test/Volume_2_Part_2_Employers_Requirements.pdf, location TBD.)

## Cross-Document Notes

- **Specification:** This guidance informs how `Specification.md` requirements (FR-01 through QR-03) are implemented in calculations. Each Principle and Consideration should support corresponding Specification requirements. (Source: Specification.md: Requirements.)
- **Procedure:** `Procedure.md` defines how calculations are developed, checked, and controlled (Steps 1-6). Considerations noted here (input coordination, methodology selection, assumption management) should be addressed in Procedure steps. (Source: Procedure.md: Steps; Procedure.md: Verification.)
- **Datasheet:** Datasheet Construction section lists the calculation artifacts (foundations, containment walls, seismic) that these Principles and Considerations guide. Ensure calculation content aligns with Datasheet construction breakdown. (Source: Datasheet.md: Construction.)
- **Related Deliverables:** Calculations should maintain consistency with:
  - DEL-05.01 element dimensions and reinforcement details (Guidance P-05)
  - DEL-05.02 material properties and specification values (Guidance P-05)
