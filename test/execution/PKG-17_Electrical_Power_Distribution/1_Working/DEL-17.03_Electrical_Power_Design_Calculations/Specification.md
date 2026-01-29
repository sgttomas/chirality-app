# Specification: DEL-17.03 Electrical Power Design Calculations

## Scope

This specification defines the requirements for **Electrical Power Design Calculations** within **PKG-17 Electrical Power Distribution**.

**Purpose** (Source: Decomposition DEL-17.03 entry): Provides the engineering basis and sizing/verification calculations for electrical power.

**Anticipated deliverable artifacts** (Source: _CONTEXT.md):
- Load calculations
- Short circuit analysis
- Protection coordination
- Voltage drop

**Project Context**: Canola oil transload facility, 1,000,000 MT/a throughput (OBJ-2), requiring comprehensive electrical system analysis to support equipment sizing and safe operation (OBJ-1).

## Requirements

### Functional Requirements

**FR-1: Load Calculations**
- Calculate connected load and demand load for all electrical equipment
- Apply appropriate demand factors per CEC Table 14 and IEEE Std 141
- Size transformers, switchgear, and MCCs based on demand load plus spare capacity (20-25% for Phase 2 expansion per OBJ-8)
- Organize loads by voltage level and distribution point
- **Rationale**: See Guidance.md — Principle 1 (Load Diversity and Demand Factors)

**FR-2: Short Circuit Analysis**
- Calculate three-phase and line-to-ground fault currents at each bus
- Include utility source contribution and motor contributions
- Determine X/R ratios
- Verify equipment ratings (interrupting capacity, withstand ratings) exceed calculated fault currents
- **Rationale**: See Guidance.md — Principle 2 (Fault Current Determination)

**FR-3: Protection Coordination Study**
- Coordinate all protective devices (relays, breakers, fuses) for selective operation
- Plot time-current coordination curves (TCC)
- Determine relay settings (pickup, time delay, instantaneous)
- Verify coordination intervals meet minimum requirements (0.2-0.3 sec for breakers)
- Verify devices do not trip on motor starting inrush
- **Rationale**: See Guidance.md — Principle 3 (Selective Coordination)

**FR-4: Voltage Drop Analysis**
- Calculate voltage drop for all feeders and branch circuits
- Verify voltage drop ≤ 3% for feeders, ≤ 5% total per IEEE Std 141
- Verify cable sizing meets both ampacity (CEC) and voltage drop requirements
- **Rationale**: See Guidance.md — Principle 4 (Voltage Regulation)

**FR-5: Grounding Grid Design** (if included)
- Design grounding grid per IEEE Std 80
- Calculate grid resistance (target < 5 ohms)
- Verify step and touch potentials within safe limits
- **TBD**: Confirm if grounding calculations included in this deliverable or separate

**FR-6: Arc Flash Hazard Analysis** (if included)
- Calculate arc flash incident energy per IEEE Std 1584 and CSA Z462
- Determine arc flash boundaries and PPE categories
- Provide arc flash label information
- **TBD**: Confirm if arc flash study included in this deliverable or separate

### Performance Requirements

**PR-1: Calculation Accuracy and Methodology**
- All calculations shall use recognized methodologies (IEEE Std 141, IEEE Std 242, IEEE Std 80, CSA Z462)
- Calculation software (ETAP, SKM PowerTools) shall be industry-recognized and validated
- Hand calculations acceptable for simple circuits; software required for complex systems
- **Source**: Professional engineering practice; CEC and IEEE standards

**PR-2: Design Conservatism and Safety Margins**
- Equipment ratings shall exceed calculated requirements (safety margins):
  - Transformers: 20-25% spare capacity for future loads (OBJ-8)
  - Circuit breakers: Interrupting capacity ≥ 125% of calculated fault current (typical practice)
  - Cables: Sized for both ampacity and voltage drop with appropriate derating factors
- **Source**: OBJ-1 (Safe & Reliable Operation); IEEE Std 141 recommended practices

**PR-3: Code and Standards Compliance**
- Calculations shall demonstrate compliance with CEC (CSA C22.1)
- Equipment sizing shall meet IEEE and CSA standard requirements
- Protection coordination shall comply with IEEE Std 242
- **Source**: OBJ-6 (Regulatory Compliance); BC Safety Authority requirements

**PR-4: Consistency with Drawings and Specifications**
- Calculations shall be consistent with equipment shown on drawings (DEL-17.01)
- Equipment ratings in calculations shall match specifications (DEL-17.02)
- Cable sizes in calculations shall match cable schedules (DEL-17.01)
- **Verification**: Cross-check required per Procedure.md Step 7

### Quality Requirements

**QR-1: Calculation Format and Documentation**
- Each calculation shall include: Title, calculation number, date, revision, originator, checker
- Design basis and assumptions clearly stated
- Input data sources identified and referenced
- Calculations legible and organized (logical flow)
- Results and conclusions clearly stated
- **Source**: Professional engineering practice; project quality standards

**QR-2: Independent Check**
- All calculations shall undergo independent check by qualified checker (not originator)
- Checker shall verify: Methodology, input data, arithmetic, results, conclusions
- Check method: Independent calculation (preferred) or detailed review of original
- **Source**: Project quality management plan; professional engineering practice
- **Rationale**: See Guidance.md — Principle 5 (Independent Verification)

**QR-3: Software Verification**
- Software calculations shall include: Software name/version, input file, output file, model verification
- Model verification: Verify system model matches actual electrical system (single line diagram)
- Hand calculation spot-check: Verify software results with hand calculation for representative cases
- **Source**: Software validation best practices; professional engineering standards

**QR-4: Calculation Revisions**
- Calculation revisions shall be documented (revision history, description of changes)
- Superseded calculations shall be retained (filed or archived)
- Current approved calculations shall be clearly identified
- **Source**: Project document control procedures

## Standards

**Primary Standards** (Calculation Methodologies):

| Standard | Title | Application |
|----------|-------|-------------|
| **IEEE Std 141 (Red Book)** | Recommended Practice for Electric Power Distribution for Industrial Plants | Load calculations, short circuit analysis, voltage drop, overall system design guidance |
| **IEEE Std 242 (Buff Book)** | Recommended Practice for Protection and Coordination | Protection coordination study, relay settings, TCC plotting |
| **IEEE Std 80** | Guide for Safety in AC Substation Grounding | Grounding grid design, step/touch potential calculations |
| **IEEE Std 1584** | Guide for Performing Arc Flash Hazard Calculations | Arc flash incident energy calculations |
| **CSA Z462** | Workplace Electrical Safety | Arc flash hazard analysis, PPE categories, safety boundaries |
| **CEC (CSA C22.1)** | Canadian Electrical Code | Demand factors (Table 14), ampacity tables, voltage drop limits |
| **CSA C68.3** | Cable — 5 kV to 46 kV | MV cable ampacity and characteristics |
| **ANSI/IEEE C37 series** | Switchgear, Circuit Breakers, Relays | Equipment ratings, interrupting capacity, relay application |

**Software Tools** (Industry-Recognized):
- **ETAP** (Electrical Transient Analyzer Program) — Comprehensive power system analysis
- **SKM PowerTools** — Power systems analysis including load flow, short circuit, coordination, arc flash
- **Microsoft Excel** or equivalent — Load summaries, simple voltage drop calculations
- **AutoCAD Electrical** or similar — One-line diagram preparation (interface with analysis software)

**Additional Standards**:
- **TBD**: Employer's Requirements (project-specific calculation requirements) — **location TBD**

## Verification

**Verification Methods for Calculation Deliverables**:

| Verification Activity | Method | Acceptance Criteria | Responsibility |
|-----------------------|--------|---------------------|----------------|
| **Input Data Verification** | Review input data sources (motor nameplates, utility data, manufacturer data) | All input data traceable to source; assumptions documented | Calculation originator |
| **Methodology Verification** | Verify calculation method consistent with applicable standard (IEEE, CEC) | Methodology per recognized standard; appropriate for application | Checker + P.Eng. |
| **Independent Check Calculation** | Checker performs independent calculation or detailed review | Results agree within acceptable tolerance (±5% typical); conclusions valid | Independent checker (P.Eng. or senior engineer) |
| **Software Output Verification** | Verify software model matches one-line diagram; spot-check results with hand calculation | Model correct; software results reasonable | Checker |
| **Code Compliance Check** | Verify calculations demonstrate compliance with CEC, IEEE, CSA requirements | All code requirements met and documented | Checker + P.Eng. |
| **Cross-Document Consistency** | Verify calculations consistent with drawings (DEL-17.01) and specifications (DEL-17.02) | Equipment ratings and cable sizes consistent | Checker / coordination review |
| **Sensitivity Analysis** (if required) | Vary key parameters (load diversity, fault current, cable length) to assess design robustness | Design adequate for reasonable parameter variations | Originator + Checker |

**Acceptance Criteria**:
- All verification activities completed and signed off
- No outstanding calculation errors or design issues
- Calculations approved by discipline lead (P.Eng.)
- Calculations consistent with approved drawings and specifications
- **TBD**: Specific approval protocol per project quality procedures

## Documentation

**Required Documentation Outputs** (Source: _CONTEXT.md anticipated artifacts):

### 1. Load Calculations
- **Content**: Connected load summary, demand factors, demand load, transformer/switchgear sizing
- **Format**: Tabular summary (Excel or calculation software output) with narrative explanation
- **Typical Sections**: Load categories, connected load by voltage level, demand factors applied, demand load summary, transformer sizing, switchgear/MCC sizing

### 2. Short Circuit Analysis
- **Content**: System model, fault current calculations (3-phase and L-G), X/R ratios, equipment rating verification
- **Format**: Software output (ETAP or SKM) with one-line diagram and fault current table
- **Typical Sections**: System modeling assumptions, fault current summary table (kA at each bus), X/R ratios, equipment SCCR verification

### 3. Protection Coordination Study
- **Content**: Protective device inventory, time-current curves (TCC plots), relay settings, coordination verification
- **Format**: Software output (ETAP or SKM) with TCC plots and relay settings table
- **Typical Sections**: Device inventory, TCC plots (log-log scale), relay settings table, coordination intervals, motor starting verification

### 4. Voltage Drop Analysis
- **Content**: Cable data, load currents, voltage drop calculations, cumulative voltage drop, cable sizing verification
- **Format**: Tabular summary (Excel or calculation software) with voltage drop table
- **Typical Sections**: Cable circuit list, cable data (size, length, installation method), load current, voltage drop (%), cumulative voltage drop (%), verification against limits

### 5. Grounding Grid Design (if included)
- **Content**: Soil resistivity, grid design, grid resistance, step/touch potential analysis
- **Format**: Hand calculation or specialized software output with grounding plan sketch

### 6. Arc Flash Hazard Analysis (if included)
- **Content**: Incident energy calculations, arc flash boundaries, PPE categories, label information
- **Format**: Software output (ETAP or SKM) with arc flash summary table and label templates

**Documentation Requirements**:
- All calculations shall comply with project document control procedures
- Revision control per project calculation numbering system — **TBD**
- Format: **ASSUMPTION**: PDF (for issued calculations) and native software files (ETAP, SKM, Excel) for revisions
- Electronic files managed in project document management system — **TBD**

**Deliverable Maturity Stages**:
- **Preliminary (30% Design)**: Preliminary load estimates, approximate transformer sizing
- **Interim (60% Design)**: Detailed load calculations, short circuit analysis, preliminary coordination
- **Final (90% / IFC)**: Final calculations supporting equipment procurement and construction
- **As-Built**: Calculations updated to reflect actual equipment installed (if significant deviations)

**Cross-References**:
- **Datasheet.md**: Calculation types, methodologies, and software tools
- **Guidance.md**: Engineering rationale for calculation approaches, design conservatism, and trade-offs
- **Procedure.md**: Step-by-step process for performing, checking, and approving calculations
- **DEL-17.01** (Electrical Power Design Drawing Set): Calculations support equipment shown on drawings
- **DEL-17.02** (Electrical Power Technical Specification): Calculations determine equipment ratings specified
- **DEL-17.04** (Electrical Power Data Sheet Package): Calculations verified against actual equipment data
