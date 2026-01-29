# Procedure: DEL-10.03 Railcar Unloading Design Calculations

## Purpose

This procedure defines the process for **producing and managing** the **Railcar Unloading Design Calculations** within **PKG-10 Railcar Unloading System**.

**Scope of Procedure:**
- Development of design calculations for railcar unloading system (header pipe sizing, unloading rate/throughput verification, containment volume calculations)
- Independent calculation check and approval workflow
- Documentation, issue, and communication of results to other deliverables

**Deliverable Type:** Calculation (Engineering Design Calculations)
**Responsible Party:** D&B Contractor
**Discipline:** Process
**Status:** INITIALIZED

**Dual-Use Nature:**
- This procedure primarily describes how to **produce** the calculation deliverable (design calculations for sizing and verification)
- The produced calculations will be **used by** design team (equipment sizing for DEL-10.01 drawings and DEL-10.02 specifications), procurement team (equipment capacity basis), regulatory authorities (permit review — containment compliance), QA/QC team (construction verification), and future engineering (basis for modifications/expansions)

## Prerequisites

### Dependencies

**Dependency Tracking Mode:** NOT_TRACKED — dependencies coordinated externally by humans (see `_DEPENDENCIES.md` and `execution/_Coordination/_COORDINATION.md`)

**Upstream Inputs (typical sequence — may be iterative with some deliverables):**

| Input | Source | Status | Required Information | Use in This Procedure | Specification Link |
|-------|--------|--------|---------------------|----------------------|--------------------|
| Project design basis and performance requirements | Employer's Requirements Vol 2 Parts 1, 2; Decomposition | **TBD** | Throughput capacity (1,000,000 MT/annum confirmed), operating schedule (**TBD** — hours per year, shift patterns, seasonal variations), performance criteria (unloading rate targets **TBD**, margin requirements **TBD**), acceptance criteria (how to demonstrate compliance) | Step 2 (design basis inputs — primary source for calculation requirements and criteria) | Specification.md IN-01 (design basis parameters from ER and decomposition) |
| Product properties | Product data sheets; Employer; product supplier | **TBD** | Canola oil properties: density (value and temperature dependence), viscosity (value and temperature dependence — critical for flow calculations), operating temperature range (affects density and viscosity), other properties (pour point for winterization, flash point for safety classification) | Step 2 (product properties inputs — density for mass-volume conversions, viscosity for flow/pressure drop calculations, temperature effects critical for accurate results) | Specification.md IN-02 (product properties with temperature dependence required) |
| Preliminary layout and geometry | DEL-10.01 Design Drawing Set (preliminary or approved drawings) | **TBD** | Header routing (path from stations to discharge connection), header elevations (profile showing elevations at key points for hydraulic gradient), slopes (actual slopes from profile — minimum 1:100 for drainage), station spacing (distance between 32 stations), branch connection configuration (swept vs. abrupt branches — affects pressure drop); If DEL-10.01 not available: site survey data, conceptual layout assumptions | Step 2 (geometry inputs for header sizing — header length, elevations, slopes critical for gravity flow calculations); May be iterative: preliminary calc sizes header → DEL-10.01 draws layout → final calc verifies layout | Specification.md IN-03 (geometry from DEL-10.01 or assumptions); Datasheet.md §Conditions (geometry inputs) |
| Equipment data | DEL-10.04 Data Sheet Package; vendor data | **TBD** | Unloading arm flow capacity (vendor Q-H curve or flow rate at design head — critical for unloading rate calculations), arm pressure drop (pressure loss through arm and quick-connect at design flow rate — affects header sizing), valve/fitting pressure drop (loss coefficients or pressure drop data for isolation valves, air release valves, fittings, branch connections), sump pump data if sizing pumps (pump curves for flow rate and head) | Step 2 (equipment data inputs for flow/pressure drop calculations); May be iterative: calc determines sizing requirements → DEL-10.04 specifies equipment → final calc verifies with actual equipment data | Specification.md IN-04 (equipment data from DEL-10.04 or vendor data) |
| Regulatory requirements for containment | Environmental regulations (federal, provincial, municipal); Employer's Requirements | **TBD** | Applicable regulations (Environment Canada Code of Practice, BC environmental regulations, Surrey municipal bylaws — identify which regulations apply to this project), containment volume formula or criteria (from regulations — typically 110% of largest vessel or 100% + freeboard + rainfall allowance), worst-case spill scenario definition (per regulations — typically single largest source), rainfall allowance criteria if required (design storm criteria), freeboard requirements (minimum freeboard height), drainage time requirements if specified | Step 2 (regulatory requirements inputs for containment volume calculation — critical for compliance demonstration) | Specification.md IN-05 (regulatory requirements documented); PF-03 (regulatory compliance verification) |

**ASSUMPTION:** Dependencies managed through project schedule, stage gates, and human coordination. Calculations may be iterative with DEL-10.01 (geometry) and DEL-10.04 (equipment data) — preliminary calculations with assumptions, refined calculations when inputs available. If upstream inputs not available when calculations needed: proceed with reasonable assumptions (document all assumptions with justification; mark results as preliminary pending input verification; update calculations when inputs become available and issue revised calculations if results change significantly).

### Reference Materials

| Reference | Location | Purpose | Document Link | Specification Link |
|-----------|----------|---------|---------------|--------------------|
| Decomposition | `test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md` | PKG-10 scope; DEL-10.03 definition; objectives (OBJ-1, OBJ-2, OBJ-4, OBJ-7); project parameters (32 stations, 1,000,000 MT/annum) | Datasheet.md §References; Guidance.md §Principles (objective alignment) | Specification.md IN-01 (design basis from decomposition) |
| Employer's Requirements Vol 2 Pt 1, 2, 3 | `test/Volume_2_Part_{1,2,3}_Employers_Requirements.pdf` | Design basis (throughput, operating schedule), performance criteria, regulatory references, QA requirements for calculations | Specification.md IN-01, IN-05; Datasheet.md §References | Specification.md IN-01 (design basis from ER); Step 2 (ER inputs) |
| Specification.md | This deliverable folder | Requirements for calculations (calculation topics FN-01/02/03, performance criteria PF-01/02/03, input requirements IN-01 through IN-05, quality requirements QA-01 through QA-05) | Bidirectional link (all steps verify against Specification.md) | — |
| Guidance.md | This deliverable folder | Calculation principles, considerations, methods, trade-offs, typical calculation flows (step-by-step templates for execution) | Bidirectional link (Step 4 applies Guidance) | — |
| Datasheet.md | This deliverable folder | Design parameters, calculation scope, anticipated artifacts, metadata requirements | Bidirectional link (Steps 2, 4, 6 use Datasheet) | — |
| DEL-10.01 | `execution/PKG-10_Railcar_Unloading_System/1_Working/DEL-10.01_*/` | Geometry inputs (header routing, elevations, slopes, spacing); Calculation results used in drawings (pipe sizes, containment dimensions) | Datasheet.md §References; Step 2 (geometry inputs) | Specification.md IN-03 (geometry from DEL-10.01); relationship documented in Specification.md §Documentation |
| DEL-10.02 | `execution/PKG-10_Railcar_Unloading_System/1_Working/DEL-10.02_*/` | Performance requirements to verify (calculations demonstrate compliance with DEL-10.02 performance requirements); Calculation results inform specification requirements | Datasheet.md §References; Step 6 (results to DEL-10.02) | Specification.md (calculations verify DEL-10.02 requirements); relationship documented |
| DEL-10.04 | `execution/PKG-10_Railcar_Unloading_System/1_Working/DEL-10.04_*/` | Equipment data inputs (arm flow capacity, valve/fitting data, pump data); Calculation results drive equipment sizing in data sheets | Datasheet.md §References; Step 2 (equipment data inputs) | Specification.md IN-04 (equipment data from DEL-10.04); relationship documented |
| DEL-10.05 | `execution/PKG-10_Railcar_Unloading_System/1_Working/DEL-10.05_*/` | Installation/test records may verify calculation predictions during commissioning (e.g., flow rate testing verifies calculated flow rates) | Downstream relationship | (Downstream deliverable — DEL-10.05 verifies design during commissioning) |
| Applicable codes, standards, references | **TBD** — per Specification.md §Standards | Calculation methods, design criteria, acceptance criteria | Specification.md §Standards; Datasheet.md §Construction | Specification.md §Standards (all codes/standards/references listed) |

### Personnel Requirements

| Role | Qualification | Responsibility | Verification | Specification Link |
|------|---------------|----------------|--------------|-------------------|
| Calculation Author | Process discipline; hydraulic analysis experience; knowledge of applicable codes/standards and calculation methods; **TBD** years experience or professional registration (P.Eng. in BC for engineering calculations) | Calculation development (Steps 1–4): scope definition, input gathering, assumption documentation, calculation execution, results documentation | Author sign-off on calculations (originator signature on calculation cover page) | Specification.md QA-02 (author metadata) |
| Checker | Process discipline; independent from author; calculation checking experience; knowledge of applicable codes/standards and calculation methods; **TBD** years experience or professional registration | Independent calculation check (Step 5): verify inputs, assumptions, methods, arithmetic, software outputs, results vs. criteria, documentation completeness; checker sign-off | Checker sign-off (checker signature on calculation cover page); checker comments/stamps if issues identified | Specification.md QA-01 (independent check requirement) |
| Discipline Lead | Process discipline; approval authority; **TBD** years experience and professional registration | Calculation approval (Step 6): review for technical adequacy, results acceptable, checker comments resolved, appropriateness for use | Approval sign-off (approver signature on calculation cover page) | Specification.md QA-05 (approval requirement — inferred from quality requirements) |
| Document Controller | Document control procedures knowledge | Issue and transmittal (Step 6): calculation numbering, transmittal preparation, distribution | Transmittal record; document register entry | Specification.md QA-02 (document control — metadata and issue) |

**ASSUMPTION:** Personnel competency requirements per project quality procedures and professional registration requirements (P.Eng. in BC for engineering calculations or Engineer-in-Training under P.Eng. supervision). Design calculations are engineering documents requiring appropriate professional oversight and seal if required by regulations.

### Tools and Resources

| Tool/Resource | Purpose | Specification Link | Use in Procedure |
|---------------|---------|-------------------|------------------|
| Spreadsheet software (Excel, Google Sheets, or similar) | Calculation execution (throughput analysis, pipe sizing, containment volume — spreadsheet adequate for these calculations); data organization; results presentation | Specification.md QA-04 (software verification — identify software used); Datasheet.md §Attributes (software used **TBD**) | Step 4 (execute calculations in spreadsheet — adequate for hand calculations with organized presentation; verify inputs, formulas, results) |
| Hydraulic analysis software (AFT Fathom, PIPENET, PIPESIM, or similar) | **If detailed hydraulic model required:** Comprehensive header system modeling (all branches, fittings, valves, elevations); detailed hydraulic profile and pressure distribution; **TBD** — determine if needed per Guidance.md §Trade-offs (calculation complexity trade-off) | Specification.md QA-04 (software verification if software used — verify software appropriate, inputs correct, outputs verified); Datasheet.md §Attributes (software used **TBD**) | Step 4b (header sizing with software if detailed model used — build model, verify inputs, run analysis, verify outputs, document results) |
| Hand calculation tools (calculator, MathCAD, or similar) | Simple calculations or verification calculations (first-principles calculations, order-of-magnitude checks, spot-checks of software results) | Specification.md QA-03 (calculation methods documented) | Step 4 (hand calculations for simpler analysis or verification; Step 5 checker may use hand calcs for spot-checking software results) |
| Hydraulic reference handbooks | Calculation methods and data (Cameron Hydraulic Data, Crane TP-410, Perry's Handbook — friction factors, loss coefficients, flow equations) | Specification.md §Standards (hydraulic references listed); Datasheet.md §Construction (methods reference standard handbooks) | Step 4 (use handbooks for friction factors, loss coefficients, equations; cite references in calculations) |
| Code and standard references | Design criteria and methods (ASME B31.3 for piping design basis, environmental regulations for containment, industry standards for design guidance) | Specification.md §Standards (all codes/standards listed) | Step 2 (obtain design criteria from codes), Step 4 (apply code requirements in calculations; cite codes for methods and criteria) |
| Project document numbering system | Calculation number assignment | Datasheet.md §Attributes (calculation number **TBD**) | Step 6 (finalize calculation number before issue) |
| Document management system | Calculation storage, revision control, transmittal | Specification.md QA-02 (document control) | Step 6 (issue and filing) |

## Steps

### Step 1: Define Calculation Basis and Scope

**Objective:** Establish calculation scope, required calculation topics, inputs, methods, and acceptance criteria before execution.

**Actions:**

1. **Review Specification.md §Scope** for required calculations (3 calculation topics per Datasheet.md §Construction):
   - Header pipe sizing (FN-01 requirement)
   - Unloading rate calculations (FN-02 requirement)
   - Containment volume calculations (FN-03 requirement)

2. **Review Datasheet.md §Conditions** for design parameters and calculation inputs:
   - Throughput capacity (1,000,000 MT/annum)
   - Number of stations (32)
   - Product (canola oil — obtain properties)
   - Unloading method (gravity flow)
   - Other parameters **TBD** (operating schedule, unloading rate per station, simultaneous operations, etc.)

3. **Review Guidance.md for calculation principles, considerations, and typical calculation flows:**
   - Engineering calculation principles (transparency, reproducibility, conservatism, traceability, accuracy — Guidance.md §Principles)
   - Calculation-specific considerations (header sizing factors, unloading rate factors, containment factors — Guidance.md §Considerations)
   - Typical calculation flows (step-by-step templates for each calculation topic — Guidance.md §Examples)
   - Trade-offs requiring decisions (simultaneous operations assumption, design margins, containment sizing approach, calculation complexity — Guidance.md §Trade-offs)

4. **Confirm calculation list and acceptance criteria** with discipline lead:

   | Calculation Topic | Purpose | Acceptance Criterion | Spec Requirement | Datasheet Link |
   |-------------------|---------|---------------------|------------------|----------------|
   | **Header Pipe Sizing** | Size gravity flow header for required capacity | Header capacity ≥ design throughput + margin (**TBD** margin — typically 10–25%); velocity within limits (**TBD** — typically 1.5–3 m/s); slope achievable with layout; gravity flow viable (head ≥ pressure drop) | Specification.md FN-01, PF-01 | Datasheet.md §Construction; §Verification (acceptance criteria table) |
   | **Unloading Rate / Throughput** | Verify throughput capacity achievable with 32 stations | Calculated annual throughput ≥ 1,000,000 MT/annum (preferably with margin — e.g., ≥ 1,100,000 MT/annum for 10% margin); 32 stations adequate (required simultaneous + margin ≤ 32); unloading time per railcar acceptable (**TBD** per ER or operations plan) | Specification.md FN-02, PF-02 | Datasheet.md §Construction; §Verification (acceptance criteria table) |
   | **Containment Volume** | Size containment per regulatory requirements; demonstrate compliance | Calculated containment volume ≥ regulatory requirement (**TBD** — Environment Canada, BC regulations; typically 110% of largest vessel or 100% + freeboard + rainfall allowance); regulatory compliance demonstrated (cite regulation, show compliance) | Specification.md FN-03, PF-03 | Datasheet.md §Construction; §Verification (acceptance criteria table) |

5. **Identify input sources** per Datasheet.md §Construction and Specification.md IN-01 through IN-05:
   - Design basis: ER Vol 2, Decomposition (throughput, operating parameters)
   - Product properties: Product data sheets **TBD** (density, viscosity, temperature effects)
   - Geometry: DEL-10.01 drawings **TBD** (header routing, elevations, slopes, spacing) or preliminary layout assumptions
   - Equipment data: DEL-10.04 data sheets **TBD** or vendor data (arm flow capacity, valve/fitting losses, pump data)
   - Regulatory requirements: Environmental regulations **TBD** (containment volume requirements)

6. **Determine calculation methods** per Guidance.md §Considerations and §Examples:
   - Header sizing: Gravity flow hydraulics — Manning equation (open channel) or Darcy-Weisbach (full pipe flow with slope); select method based on header configuration **TBD**; use hydraulic references (Cameron, Crane) for friction factors and loss coefficients
   - Unloading rate: Mass balance and flow rate analysis — annual capacity ÷ operating hours = required hourly rate; required rate ÷ flow per station = simultaneous stations needed; verify 32 stations adequate
   - Containment volume: Regulatory formula (per applicable regulations **TBD** — typically 110% of largest source or 100% + freeboard + rainfall); worst-case scenario analysis (largest credible spill — one railcar typical)

7. **Confirm scope, inputs, methods, and acceptance criteria with discipline lead:**
   - Review calculation scope (verify 3 calculation topics address all sizing requirements for PKG-10)
   - Confirm input sources identified (verify sources appropriate and available or obtainable)
   - Confirm methods appropriate (verify methods suitable for application per Guidance.md §Trade-offs — simplified vs. detailed approach)
   - Confirm acceptance criteria clear (verify pass/fail criteria defined for each calculation — results comparison to criteria documented in Step 4)
   - Obtain discipline lead sign-off on calculation basis (confirms scope, methods, criteria approved before execution)

**Output:** Approved calculation scope and basis (calculation list, input sources, methods, acceptance criteria); filed in `1_Working/` deliverable folder.

**Verification:** Discipline lead sign-off on calculation basis (confirms calculation approach approved; provides basis for execution in Steps 2–4).

---

### Step 2: Gather and Document Inputs

**Objective:** Collect all calculation inputs from appropriate sources and document in calculation input summary with sources cited (Specification.md IN-01 through IN-05 requirements).

**Actions:**

1. **Gather design basis parameters** from ER and project design basis (Specification.md IN-01):
   - Annual throughput capacity: 1,000,000 MT/annum (Decomposition §1; README; OBJ-2)
   - Operating schedule: **TBD** — operating hours per year (obtain from ER Vol 2 **TBD** or assume reasonable value — e.g., 8,000 hr/yr for ~22 hr/day with downtime allowance; document source or assumption)
   - Number of stations: 32 (Decomposition §1; README; DEL-10.01 Datasheet)
   - Design margins: **TBD** — margin on throughput capacity, header capacity, containment volume (obtain from ER or project design basis **TBD**, or assume industry-typical margins 10–25% with justification per Guidance.md §Trade-offs)
   - Performance criteria: **TBD** — specific criteria from ER (e.g., unloading rate targets, unloading time limits, pressure limits)

2. **Obtain product properties** with temperature dependence (Specification.md IN-02):
   - **TBD** — Obtain canola oil product data sheets from Employer, product supplier, or industry references
   - Density: Value at reference temperature (e.g., 920 kg/m³ at 15°C); temperature dependence (e.g., -0.7 kg/m³ per °C or density-temperature curve); range (910–930 kg/m³ typical)
   - Viscosity (kinematic): Value at reference temperature (e.g., 60–80 cSt at 20°C); temperature dependence (viscosity-temperature curve critical — viscosity varies significantly with temperature; e.g., 80 cSt at 20°C, 30 cSt at 40°C); range for seasonal operations
   - Operating temperature range: **TBD** — temperature during unloading (ambient for unheated, heated temperature if winterization; affects viscosity and flow rate significantly)
   - Other properties: Pour point (~-10°C typical — winterization consideration), flash point (>300°C typical — safety classification)
   - **If product data not available:** Use typical canola oil properties from industry references (mark as assumption; cite reference — e.g., "AOCS Lipid Library, canola oil properties"; note uncertainty; verify when product data available; assess impact on results — if viscosity assumption significantly affects results, flag for verification)

3. **Obtain layout geometry** from DEL-10.01 or preliminary layout (Specification.md IN-03):
   - **If DEL-10.01 available:** Extract geometry from drawings (Header Layout for header routing, profile for elevations/slopes, GA for station spacing)
   - Header length: Measure total pipe run from DEL-10.01 Header Layout (from first station inlet to discharge connection outlet; account for routing path)
   - Elevations: Extract from DEL-10.01 profile views (header elevations at key points — inlet at first station, outlet at discharge connection, intermediate high/low points for hydraulic gradient and air release valve locations)
   - Slopes: Calculate from elevations and horizontal distances (verify slopes ≥ minimum 1:100 for drainage; use actual slopes from layout for calculations)
   - Station spacing: Measure from DEL-10.01 GA (distance between 32 stations — affects branch connection configuration and header sizing)
   - Branch connections: Note configuration from DEL-10.01 Header Layout (swept vs. abrupt branches — affects pressure loss; swept branches lower loss)
   - **If DEL-10.01 not available (preliminary calculations):** Use conceptual layout assumptions (assume header routing based on site constraints and track layout from PKG-07 if available; assume minimum slope 1:100; assume typical station spacing 15m; mark all geometry as assumptions; note calculations preliminary pending DEL-10.01 layout; verify and recalculate when DEL-10.01 available; coordinate with DEL-10.01 design team for iteration — preliminary calc provides sizing for layout, layout provides geometry for final calc)

4. **Obtain equipment data** from DEL-10.04 or vendor data (Specification.md IN-04):
   - Unloading arm flow capacity: **TBD** — vendor Q-H curve (flow rate vs. head for specific arm model — preferred; most accurate) or typical flow rate (50–200 m³/hr for gravity unloading arms — industry typical; less accurate; mark as assumption)
   - Arm pressure drop: **TBD** — pressure drop through arm and quick-connect at design flow rate (from vendor data or estimate from typical values — e.g., 0.5–2.0 m head loss for arm+coupler; affects total system pressure drop)
   - Valve/fitting pressure drop: Loss coefficients K or pressure drop data for isolation valves (K ~0.1–0.2 for full-bore gate/ball valves), air release valves, fittings (elbows K ~0.9, tees K ~1.8 for through-flow, branch connections K ~1.0–2.0 depending on geometry), from vendor data or standard references (Cameron, Crane — loss coefficient tables)
   - Sump pump data if sizing pumps: **TBD** — pump curves (Q-H curve for sump pump; or size pump for required flow rate and head)
   - **If equipment data not available:** Use typical values from industry practice or vendor catalogs with assumption (mark assumptions; note uncertainty; verify when equipment data available; assess impact — if arm flow rate assumption significantly affects throughput results, flag for verification when DEL-10.04 or vendor data available)

5. **Identify regulatory requirements** for containment (Specification.md IN-05):
   - **TBD** — Obtain applicable environmental regulations (Environment Canada Environmental Code of Practice for Storage Tank Systems, BC environmental regulations, Surrey/Fraser Surrey municipal bylaws)
   - Extract containment volume requirements from regulations:
     - Containment volume formula or criteria (typically 110% of largest vessel, or 100% + freeboard + rainfall allowance — verify specific requirement in regulations; note regulation edition and section)
     - Worst-case spill scenario definition (typically single largest source — verify regulatory definition; adapt for railcar unloading context)
     - Rainfall allowance requirements (if regulations require stormwater capacity — obtain design storm criteria: intensity, duration, return period)
     - Freeboard requirements (minimum freeboard above design liquid level — typically 150–300mm or percentage of depth)
     - Drainage time requirements if specified (time to evacuate containment — typically 4–24 hours if specified)
   - **If regulations not available:** Contact regulatory authorities for guidance (federal — Environment Canada; provincial — BC Ministry of Environment; municipal — Surrey; request containment calculation requirements); or use industry-standard approach with assumption (110% of largest vessel + standard freeboard — mark as assumption pending regulatory confirmation; flag for verification)

6. **Document all inputs in calculation input summary** (table or organized section in calculation report):

   | Input Category | Parameter | Value | Source | Status |
   |----------------|-----------|-------|--------|--------|
   | Design Basis | Annual throughput | 1,000,000 MT/annum | Decomposition §1; ER Vol 2 **TBD** | Confirmed |
   | Design Basis | Operating hours/year | **TBD** (e.g., 8,000 hr/yr assumed) | ER Vol 2 **TBD** or assumption | **TBD** / Assumed |
   | Design Basis | Number of stations | 32 | Decomposition §1; DEL-10.01 | Confirmed |
   | Design Basis | Design margin | **TBD** (e.g., 15–20% assumed) | ER or assumption per Guidance.md | **TBD** / Assumed |
   | Product | Density | **TBD** (920 kg/m³ at 15°C assumed) | Product data **TBD** or industry ref | **TBD** / Assumed |
   | Product | Viscosity | **TBD** (60–80 cSt at 20°C assumed) | Product data **TBD** or industry ref | **TBD** / Assumed |
   | Product | Temperature | **TBD** (operating temp range) | ER Vol 2 **TBD** or assumption | **TBD** / Assumed |
   | Geometry | Header length | **TBD** (from DEL-10.01 or assumed) | DEL-10.01 **TBD** or assumption | **TBD** / Assumed |
   | Geometry | Elevations | **TBD** (from DEL-10.01 or assumed) | DEL-10.01 **TBD** or assumption | **TBD** / Assumed |
   | Geometry | Slopes | **TBD** (from DEL-10.01 or 1:100 assumed) | DEL-10.01 **TBD** or assumption | **TBD** / Assumed |
   | Equipment | Arm flow capacity | **TBD** (from DEL-10.04/vendor or assumed) | DEL-10.04 **TBD** or vendor data/assumption | **TBD** / Assumed |
   | Equipment | Valve/fitting losses | **TBD** (from vendor or standard tables) | Vendor data **TBD** or Cameron/Crane | **TBD** / From tables |
   | Regulatory | Containment formula | **TBD** (110% of largest vessel assumed typical) | Regulations **TBD** or assumption | **TBD** / Assumed |
   | Regulatory | Worst-case spill | **TBD** (one railcar ~100–150 m³ assumed) | Regulations **TBD** or assumption | **TBD** / Assumed |
   | (etc.) | (etc.) | (etc.) | (etc.) | (etc.) |

   **Note:** Mark all inputs as "Confirmed" (from reliable source), "TBD" (to be obtained from specified source), or "Assumed" (assumption used pending data availability — document assumption and justification in Step 3). Inputs marked "TBD" or "Assumed" require verification when data available (update calculations if values change significantly).

**Output:** Approved calculation scope and basis (calculation list, acceptance criteria, input sources identified); documented input summary (preliminary — values **TBD** until gathered); filed in `1_Working/` deliverable folder.

**Verification:** Discipline lead sign-off on calculation basis (confirms scope, acceptance criteria, approach approved).

---

### Step 3: Document Assumptions

**Objective:** Record and justify all calculation assumptions clearly for transparency and verification (Specification.md FN-04 requirement — assumptions documented with justification).

**Actions:**

1. **Identify assumptions required** where inputs are incomplete or uncertain:
   - Review input summary from Step 2 (identify inputs marked "TBD" or "Assumed")
   - Identify where assumptions needed for calculation execution (parameters not yet available from ER, product data, DEL-10.01, DEL-10.04, or regulations)
   - Determine if calculation can proceed with assumptions or if inputs critical and must be obtained before proceeding (for critical inputs affecting results significantly: obtain inputs before proceeding; for non-critical inputs: reasonable assumptions acceptable — mark assumptions and verify later)

2. **Document each assumption with justification** (create assumption log — table format in calculation or separate assumption section):

   | Assumption No. | Assumption | Basis / Justification | Impact on Results | Verification Required | Specification Link |
   |----------------|------------|----------------------|-------------------|----------------------|--------------------|
   | A-1 | Simultaneous operations = **TBD** stations (e.g., 12 stations assumed for realistic operations) | Based on: industry practice for similar terminals (typical simultaneity **TBD** %), operating schedule analysis (if 8,000 hr/yr operating with **TBD** hr unloading time per railcar, calculate turnover rate and required simultaneous operations), operational flexibility per OBJ-4 (not all 32 stations operate continuously — some down for maintenance, railcar delays, etc.); conservative with margin (design for 12 × 1.25 = 15 stations equivalent capacity — 25% margin provides operational flexibility) | **Critical assumption** affecting header sizing (simultaneous operations directly determines required header capacity — higher simultaneous operations requires larger header; assumption affects pipe size, cost, and capacity verification); affects throughput verification (demonstrates 32 stations adequate for required simultaneous operations) | **Yes** — verify with ER operating scenario requirements **TBD** or Employer operations planning when available; perform sensitivity analysis varying simultaneous operations ±20–50% to demonstrate design robust; recalculate if actual requirement significantly different from assumption | Specification.md PF-01 (header capacity depends on simultaneous operations); PF-02 (throughput verification depends on simultaneous operations); Datasheet.md §Conditions (simultaneous operations parameter **TBD** — critical design parameter) |
   | A-2 | Product density = 920 kg/m³ at 15°C | Based on: typical canola oil density per industry references (e.g., AOCS Lipid Library — canola oil density range 910–930 kg/m³ at 15°C; 920 kg/m³ is mid-range value); conservative for mass-volume conversions (mid-range value appropriate — not overly conservative or optimistic); temperature dependence -0.7 kg/m³ per °C per industry data | Moderate impact on mass-volume conversions (affects throughput mass calculations — MT to m³ conversions; ±1% variation in density causes ±1% variation in volumetric flow rates and volumes); low impact on sizing (header size driven by volumetric flow rate, relatively insensitive to density; containment volume driven by spill volume, moderate sensitivity to density if mass-based requirement) | **Moderate priority** — verify with product data sheets when available (obtain actual canola oil density from Employer or product supplier; update calculations if density differs by >2–3% from assumed value — recalculate if significant impact on results) | Specification.md IN-02 (product density input); Datasheet.md §Conditions (product density parameter **TBD**) |
   | A-3 | Product viscosity = 70 cSt at 20°C (kinematic viscosity) | Based on: typical canola oil viscosity per industry references (range 60–80 cSt at 20°C; 70 cSt is mid-range); temperature dependence per industry viscosity-temperature curves (viscosity ~30 cSt at 40°C, ~150 cSt at 0°C — strong temperature dependence for vegetable oils); conservative for flow calculations (mid-range viscosity at typical temperature) | **Significant impact** on flow rate and pressure drop calculations (viscosity directly affects friction factor, pressure drop, flow rate for gravity flow; factor of 2 variation in viscosity causes significant variation in flow rate and pressure drop — e.g., winter operations at 0°C with viscosity ~150 cSt would have much lower flow rate than summer operations at 40°C with viscosity ~30 cSt; affects header sizing, unloading rate, simultaneousoperations requirement) | **High priority** — verify with product data sheets when available (obtain actual canola oil viscosity-temperature curve from Employer or product supplier; critical for accurate flow calculations); verify operating temperature range (if wide temperature range, analyze flow at minimum and maximum temperatures — verify system performs adequately at both extremes; may require winterization if flow rate unacceptable at low temperature); recalculate if viscosity differs significantly from assumed value or if operating temperature significantly different | Specification.md IN-02 (product viscosity input — critical for flow calculations); Datasheet.md §Conditions (product viscosity parameter **TBD** — critical parameter) |
   | A-4 | Operating temperature range = 5°C to 30°C (seasonal ambient temperature range for unheated operations) | Based on: Fraser Surrey climate (outdoor facility; product at ambient temperature if no heating; typical ambient range for Fraser Valley, BC); winterization **TBD** (if heated for winter operations, temperature range different — e.g., 10°C to 40°C for heated product); affects viscosity significantly (temperature determines viscosity for flow calculations — lower temperature = higher viscosity = lower flow rate) | **Significant impact** on flow rate calculations (temperature affects viscosity; viscosity affects flow rate; if temperature range wide, flow rate varies significantly across range — verify system performs at minimum temperature worst case); may affect winterization requirement (if flow rate unacceptable at low temperature, winterization — heating — may be required; coordinate with DEL-10.02 specifications and DEL-10.01 details if heating required) | **High priority** — verify operating temperature range with ER **TBD** or Employer operations planning; determine if winterization (heating) required for year-round operations; analyze flow rates at temperature extremes if wide range; coordinate winterization requirements with DEL-10.01, DEL-10.02 if heating needed | Specification.md IN-02 (temperature range input); Datasheet.md §Conditions (operating temperature range parameter **TBD**) |
   | A-5 | Header minimum slope = 1:100 for drainage (if preliminary — geometry from DEL-10.01 not yet available) | Based on: industry practice for gravity drainage (minimum 1:100 slope typical for reliable drainage of liquid piping; steeper slopes acceptable and improve drainage); DEL-10.01 design intent (gravity flow header requires slopes for drainage — assume minimum slope if actual layout not yet available; verify when DEL-10.01 available) | Moderate impact on header sizing (slope affects flow capacity — steeper slopes increase capacity for given pipe size; shallower slopes reduce capacity requiring larger pipe; if actual slope from DEL-10.01 different from assumed 1:100, recalculate capacity — if actual slope shallower than 1:100, header may need to be larger; if actual slope steeper, header may be smaller or have more capacity margin) | **Moderate priority** — verify actual slopes when DEL-10.01 layout available (measure slopes from DEL-10.01 profile views; recalculate header capacity with actual slopes; verify capacity still adequate — if actual slopes shallower than assumed, may need larger header; coordinate with DEL-10.01 if slopes cannot achieve required capacity) | Specification.md IN-03 (geometry — slopes from DEL-10.01 or assumptions); Datasheet.md §Conditions (slope parameter) |
| A-6 | Unloading rate per station = **TBD** m³/hr (e.g., 100 m³/hr assumed for gravity unloading with typical arm and railcar head) | Based on: vendor data for unloading arms **TBD** (if available — use vendor Q-H curve at typical railcar head ~3m; preferred method), or industry typical values (50–200 m³/hr for gravity unloading arms depending on arm design, railcar head, product viscosity, piping configuration), or first-principles calculation (calculate gravity flow from railcar through arm to header using Bernoulli equation — requires assumptions about arm geometry, restrictions); mid-range value used if uncertain (100 m³/hr reasonable for typical gravity unloading — conservative for demonstrating 32 stations adequate; if actual rate higher, fewer simultaneous stations needed; if actual rate lower, more simultaneous stations needed but 32 stations likely still adequate with margin) | **Significant impact** on simultaneous operations requirement (flow rate per station directly determines how many stations must operate simultaneously to achieve throughput — lower flow rate requires more simultaneous operations; higher flow rate requires fewer simultaneous operations); affects unloading time (unloading time per railcar = railcar capacity ÷ flow rate — lower flow rate increases unloading time; verify unloading time acceptable); moderate impact on header sizing (header flow = simultaneous operations × flow per station — if simultaneous operations and flow per station both assumed, combined assumption affects header sizing) | **High priority** — verify with vendor data when DEL-10.04 or vendor proposals available (obtain actual arm flow capacity from vendor Q-H curves or vendor test data; recalculate with actual flow rates; verify simultaneous operations requirement still within 32 stations; verify unloading time acceptable); if actual flow rate significantly different from assumption, recalculate throughput and header sizing; coordinate with DEL-10.04 for arm selection (ensure selected arms meet flow rate requirements from this calculation) | Specification.md IN-04 (arm flow capacity input); PF-02 (unloading rate verification depends on flow per station); Datasheet.md §Conditions (unloading rate per station parameter **TBD** — critical) |
   | A-7 | Railcar capacity = 100 m³ per car (typical North American tank car) | Based on: industry typical tank car capacity for liquid bulk (range 80–120 m³; 100 m³ mid-range and common size); railcar fleet data **TBD** (actual railcar types serving facility from PKG-07 or Employer — verify when available); conservative for containment (if using largest railcar for worst-case spill, 100 m³ may be conservative — actual railcars may be smaller; or may be non-conservative if larger cars used — verify actual fleet); conservative for unloading time (if calculating unloading time, 100 m³ capacity with assumed flow rate gives reasonable unloading time estimate) | Moderate impact on containment volume (railcar capacity typically determines worst-case spill volume — if actual railcar larger than assumed, containment may be undersized; if smaller, containment oversized with margin); low impact on unloading time (affects calculated unloading time — larger cars take longer; verify time acceptable); low impact on throughput (throughput driven by flow rate and operating hours, not railcar size — railcar size affects individual car unloading time but not annual throughput assuming adequate railcars available) | **Moderate priority** — verify with railcar fleet data from PKG-07 or Employer (identify actual railcar types serving facility — tank car models and capacities; use largest railcar for worst-case spill in containment calculation — conservative); update containment calculation if actual railcar capacity significantly larger than 100 m³ (ensures containment adequate for largest railcar); verify unloading time acceptable with actual railcar size | Specification.md IN-04 (railcar data input); PF-03 (worst-case spill volume depends on railcar capacity); Datasheet.md §Conditions (railcar capacity parameter **TBD**) |
   | A-8 | **TBD** — Other assumptions as required (e.g., roughness coefficient for pipe friction, loss coefficients for fittings if vendor data not available, freeboard height if regulation not specific, rainfall criteria if regulation not specific, drainage time if regulation not specific, pump efficiency if sizing pumps, etc.) | Basis and justification for each assumption (industry practice, code guidance, conservative approach, etc.) | Impact on results (note if critical assumption affecting results significantly or if low-impact assumption) | Verification required? (yes for critical assumptions; optional for low-impact assumptions) | Specification.md reference (which specification requirement relates to assumption) |

   **For each assumption:** Document assumption clearly (what is assumed — value, parameter, scenario), justify assumption (why this value reasonable — industry practice, code guidance, conservative approach, typical value, etc.), note impact on results (how assumption affects calculation results — significant impact or low impact), flag verification requirement if critical (assumptions with significant impact on sizing or compliance require verification when data available — mark for verification; low-impact assumptions may not require verification).

3. **Flag assumptions requiring confirmation** for future verification:
   - Critical assumptions (significant impact on sizing or compliance): simultaneous operations, product viscosity, operating schedule, unloading rate per station, railcar capacity for containment, regulatory requirements
   - Moderate priority assumptions: product density, slopes if preliminary, header geometry if preliminary, design margins if assumed
   - Low priority assumptions (low impact on results): minor fitting loss coefficients, roughness coefficients if using standard values, other minor parameters

4. **Apply Guidance.md considerations for conservative assumptions** (Guidance.md §Principles — conservatism principle; Guidance.md §Conservatism Guidelines):
   - For throughput: Use conservative assumptions (lower operating hours requires higher rate — conservative for equipment sizing; lower flow per station requires more simultaneous operations — conservative for verifying 32 stations adequate)
   - For header sizing: Use conservative assumptions (higher viscosity requires larger pipe — conservative; higher roughness requires larger pipe — conservative; higher simultaneous operations requires larger pipe — conservative)
   - For containment: Use conservative assumptions (larger railcar capacity requires larger containment — conservative for compliance; higher rainfall if uncertain — conservative; higher freeboard if uncertain — conservative)
   - Document conservatism in assumption justification (note where conservative approach used to address uncertainty; provides confidence in design adequacy even if assumptions prove slightly optimistic)

**Output:** Documented assumption log (table or assumption section in calculation report listing all assumptions with justification, impact assessment, and verification requirements); filed in calculation package.

**Verification:** Assumption review by checker in Step 5 (checker verifies assumptions reasonable, justified, appropriately conservative, impacts understood).

---

### Step 4: Execute Calculations

**Objective:** Perform calculations per Specification.md requirements using documented inputs (Step 2) and assumptions (Step 3), following typical calculation flows from Guidance.md §Examples.

**Actions:**

Execute 3 calculation topics per calculation scope (Step 1). For each calculation: document purpose, inputs, assumptions, method, step-by-step calculations, results summary, conclusions per calculation report structure (Datasheet.md §Construction).

---

#### **Step 4a: Unloading Rate / Throughput Calculations**

**Objective:** Verify 1,000,000 MT/annum throughput achievable with 32 stations; determine required simultaneous operations; calculate unloading time per railcar (Specification.md FN-02, PF-02).

**Calculation Steps (follow Guidance.md §Examples — Unloading Rate Calculation Flow):**

1. **Calculate required throughput rate:**
   - Annual capacity: 1,000,000 MT/annum (from design basis)
   - Operating hours per year: **TBD** (e.g., 8,000 hr/yr from ER or assumed per Step 2/3 — document value and source/assumption)
   - Required hourly rate (mass): 1,000,000 MT/annum ÷ 8,000 hr/yr = 125 MT/hr (example calculation — actual value per operating hours used)
   - Required hourly rate (volumetric): Convert mass rate to volumetric using product density: 125 MT/hr ÷ 0.920 MT/m³ = 136 m³/hr (example — actual calculation uses values from Steps 2/3)

2. **Determine flow rate per station:**
   - Obtain from equipment data (Step 2): Arm flow capacity **TBD** (e.g., 100 m³/hr assumed or from vendor data — document value and source)
   - Or calculate from first principles if vendor data not available: Gravity flow from railcar through arm (use Bernoulli equation or orifice flow equations; requires assumptions about arm geometry, restrictions, railcar head — document calculation method and assumptions; less accurate than vendor data)
   - Account for head variation if significant (railcar head decreases as unloading progresses — full railcar ~3–4m head, empty railcar ~0.5–1m head; flow rate varies with head; use average head or time-averaged flow rate for unloading time calculation; verify with vendor Q-H curve if available)

3. **Determine number of simultaneous stations needed:**
   - Minimum simultaneous stations: Required hourly volumetric rate ÷ flow per station = minimum simultaneous stations for average throughput (e.g., 136 m³/hr ÷ 100 m³/hr per station = 1.36 stations — round up to 2 stations minimum for average throughput in this example; actual calculation uses values from above)
   - Add design margin per Step 3 assumptions: Margin **TBD** (e.g., 25% margin assumed per Guidance.md conservatism guidelines — provides operational flexibility per OBJ-4 and accommodates peak periods, uncertainties); Design simultaneous operations = minimum × (1 + margin) = 2 × 1.25 = 2.5 — round up to 3 stations for design (example — actual calculation uses assumed margin)
   - Or design for realistic operations scenario: If operating scenario known from ER or operations planning (e.g., typical operations have 8–12 stations unloading simultaneously due to railcar arrival patterns, shift schedules, etc.), use realistic scenario + margin rather than strict minimum (results in more realistic simultaneous operations requirement — e.g., 12 stations typical → design for 12 × 1.15 = 14 stations — provides margin for variations)

4. **Verify total capacity exceeds requirement:**
   - Calculate annual throughput capacity with design assumptions: Design simultaneous operations × flow per station × operating hours per year = annual throughput capacity (e.g., 3 stations × 100 m³/hr × 8,000 hr/yr = 2,400,000 m³/yr = 2,400,000 m³/yr × 0.920 MT/m³ = 2,208,000 MT/yr in this simplified example — actual calculation shows capacity significantly exceeds 1,000,000 MT/annum minimum; demonstrates adequate capacity and large margin)
   - Verify capacity ≥ 1,000,000 MT/annum + margin: Compare calculated capacity to requirement (in above example: 2,208,000 MT/yr >> 1,000,000 MT/yr — demonstrates capacity exceeds requirement with large margin of ~120%; pass)
   - Verify 32 stations adequate: Compare required design simultaneous operations to available 32 stations (in above example: 3 design simultaneous stations << 32 available stations — demonstrates 32 stations more than adequate; large reserve capacity for operational flexibility, future expansion, peak demands; pass)

5. **Calculate unloading time per railcar:**
   - Unloading time: Railcar capacity ÷ flow rate per station = unloading time (e.g., 100 m³ per railcar ÷ 100 m³/hr flow rate = 1.0 hour = 60 minutes unloading time in this example; actual calculation uses values from above)
   - Verify unloading time acceptable: Compare calculated unloading time to ER requirement **TBD** or operations plan (typical acceptable unloading time 30–90 minutes; faster unloading better for operations but may require larger arms or higher pressure; verify time meets requirements or adjust design if needed)
   - Account for connection/disconnection time if total cycle time specified (railcar total cycle time = unloading time + connection time + disconnection time + positioning time + delays — if ER specifies total cycle time rather than just unloading time, verify total cycle time acceptable)

6. **Perform sensitivity analysis** (verify design robust to assumption variations — recommended per Guidance.md §Trade-offs):
   - Vary key assumptions: Operating hours (±10–20% variation — e.g., 6,400–9,600 hr/yr if 8,000 hr/yr assumed), flow rate per station (±20–30% variation — e.g., 70–130 m³/hr if 100 m³/hr assumed), simultaneous operations (±20–50% variation — e.g., 2–5 stations if 3 stations design in example)
   - Recalculate throughput capacity for each variation: Verify capacity still ≥ 1,000,000 MT/annum under variations (demonstrates design robust even if assumptions prove optimistic or operating conditions vary)
   - Document sensitivity results: Show throughput capacity for range of assumptions (e.g., "Throughput capacity ranges from 1,200,000 to 3,000,000 MT/yr for ±20% variations in key assumptions; all scenarios exceed 1,000,000 MT/yr requirement — design robust")

7. **Document results and comparison to acceptance criteria:**
   - Results summary table: Required hourly rate, flow rate per station, required simultaneous operations (minimum and design with margin), calculated annual throughput capacity, unloading time per railcar, comparison to 32 available stations
   - Acceptance criterion comparison: Calculated throughput ≥ 1,000,000 MT/annum (pass/fail); 32 stations adequate for required simultaneous + margin (pass/fail); unloading time acceptable (pass/fail)
   - Conclusions: "Throughput capacity of 1,000,000 MT/annum achievable with 32 unloading stations operating by gravity flow. Design basis: [state key assumptions]. Design simultaneous operations = [X] stations provides [Y%] margin for operational flexibility. Unloading time per railcar = [Z] minutes is acceptable per [ER requirement or operations plan]. Design meets OBJ-2 throughput capacity objective."

**Output:** Unloading rate / throughput calculation documented in calculation package (inputs, assumptions, step-by-step calculations, results, conclusions).

**Traceability to Specification:**
- FN-02: Unloading rate calculation performed ✓
- PF-02: Throughput ≥ 1,000,000 MT/annum verified (acceptance criterion met — pass/fail documented)
- IN-01, IN-02, IN-04: Inputs documented (design basis, product properties, equipment data)

---

#### **Step 4b: Header Pipe Sizing Calculations**

**Objective:** Size gravity flow header pipe for required capacity with design margin; verify velocity, slope, pressure drop (Specification.md FN-01, PF-01).

**Calculation Steps (follow Guidance.md §Examples — Header Sizing Calculation Flow):**

1. **Determine design flow rate** (from unloading rate calculation Step 4a):
   - Design simultaneous operations × flow per station = design flow rate (e.g., from Step 4a example: 3 stations × 100 m³/hr = 300 m³/hr design flow rate for header)
   - Or apply margin directly: Required hourly rate × (1 + margin) = design flow rate (e.g., 136 m³/hr required × 1.25 margin = 170 m³/hr design flow — alternative approach if not using simultaneous operations basis)
   - Document design flow rate value and basis (from unloading rate calc or margin on required rate)

2. **Select pipe material and determine roughness:**
   - Pipe material: From DEL-10.02 material selection **TBD** (carbon steel or stainless steel per Guidance.md §Trade-offs and DEL-10.02 material trade-off decision)
   - Roughness coefficient: ε (absolute roughness) or n (Manning roughness) depending on method:
     - For Darcy-Weisbach (pipe flow): ε = 0.045mm (carbon steel new commercial pipe), ε = 0.015–0.045mm (stainless steel depending on finish), or higher if aged/fouled pipe (conservatively use higher roughness — e.g., ε = 0.090mm for aged carbon steel)
     - For Manning (open channel): n = 0.012–0.015 (steel channel depending on condition)
   - Document material and roughness (cite source — code, handbook, or standard values)

3. **Determine available slope/head** (from DEL-10.01 or assumptions):
   - Slope: From DEL-10.01 Header Layout profile (measure actual slopes) or assumed minimum 1:100 (per Step 3 assumption if preliminary)
   - Head (elevation difference): From DEL-10.01 elevations (elevation at first station inlet − elevation at discharge connection outlet = total available head for gravity flow)
   - Horizontal distance: Header length from DEL-10.01 or assumed based on station spacing and routing (e.g., 32 stations × 15m spacing + routing allowance = ~500–600m total length — order of magnitude estimate if preliminary)
   - Verify slope = head ÷ horizontal distance (check consistency — if slope and head both from DEL-10.01, should be consistent; if one assumed, calculate the other for consistency)

4. **Size pipe for required capacity with margin** (iterative calculation — try pipe sizes until capacity adequate):
   - Select sizing method: Darcy-Weisbach for full pipe flow (preferred for viscous fluids like canola oil — accounts for viscosity effects on friction factor) or Manning for open channel flow (if header partially full with free surface — verify flow regime from header configuration)
   - **For Darcy-Weisbach method:**
     - Assume pipe diameter (start with reasonable initial guess — e.g., 6" or 8" or 10" depending on flow rate magnitude)
     - Calculate flow velocity: V = Q / A (flow rate ÷ pipe area)
     - Calculate Reynolds number: Re = ρ × V × D / μ (density × velocity × diameter ÷ dynamic viscosity; determines flow regime and friction factor; convert kinematic viscosity from Step 2 to dynamic viscosity: μ = ν × ρ)
     - Calculate friction factor: f from Moody diagram or Colebrook-White equation using Re and ε/D (relative roughness)
     - Calculate friction pressure drop: ΔP_friction = f × (L/D) × (ρ × V²/2) (Darcy-Weisbach equation)
     - Add fitting/valve losses: ΔP_fittings = Σ(K × ρ × V²/2) for all fittings, valves, branches (use loss coefficients from Step 2 or standard tables)
     - Add elevation change: ΔP_elevation = ρ × g × Δz (positive for flow up, negative for flow down — gravity flow header typically flows down providing driving head)
     - Total pressure drop: ΔP_total = ΔP_friction + ΔP_fittings + ΔP_elevation
     - Available gravity head: ΔP_available = ρ × g × (elevation at inlet − elevation at outlet) (gravity driving force)
     - Verify gravity flow viable: ΔP_available ≥ ΔP_total (if not, increase pipe diameter to reduce losses or increase slope if possible)
     - Verify capacity: If ΔP_available >> ΔP_total (significant excess head), pipe may be oversized — consider smaller pipe if velocity still acceptable and slope adequate; If ΔP_available ≈ ΔP_total (marginal), pipe size appropriate; If ΔP_available < ΔP_total (insufficient head), pipe too small or slope inadequate — increase pipe size or slope
     - Iterate until pipe size provides required capacity at acceptable velocity and gravity flow viable
   - **For Manning method (if open channel flow):**
     - Manning equation: Q = (1/n) × A × R^(2/3) × S^(1/2) (flow rate = function of roughness, area, hydraulic radius, slope)
     - Iterate pipe diameter until Q ≥ design flow rate + margin
   - Select standard pipe size: Round up to next standard pipe size (per ASME B16.5 or pipe manufacturer standard sizes — e.g., if calculated diameter = 7.5", select 8" standard pipe)
   - Calculate wall thickness: Per ASME B31.3 pressure design + corrosion allowance (low pressure for gravity flow but code-compliant wall thickness required; standard wall thickness typically adequate — verify with code)

5. **Verify velocity within acceptable range** (Specification.md PF-01 requirement):
   - Calculate final velocity: V = Q / A (design flow rate + margin ÷ selected pipe area)
   - Check minimum velocity: V ≥ V_min (**TBD** — typically 0.5–1.0 m/s for drainage and self-cleaning; verify velocity adequate for drainage; if too low, consider smaller pipe or steeper slope)
   - Check maximum velocity: V ≤ V_max (**TBD** — typically 1.5–3.0 m/s for vegetable oils to prevent erosion; verify with ASME B31.3 or industry practice for canola oil in selected pipe material; stainless steel more erosion-resistant allows higher velocity; carbon steel may require lower velocity limit)
   - If velocity out of range: Adjust pipe size (increase for too-high velocity, decrease for too-low velocity if capacity still adequate) or adjust slope if possible (steeper slope increases velocity and capacity; shallower slope decreases velocity)

6. **Calculate pressure drop and verify gravity flow viable:**
   - Total pressure drop: Calculate per method above (friction + fittings + elevation change)
   - Available gravity head: ρ × g × elevation difference (driving force for gravity flow)
   - Verify ΔP_available ≥ ΔP_total: If yes, gravity flow viable (adequate head for flow without pumping — fundamental requirement met); If no, revise design (increase pipe size to reduce losses, increase slope to increase available head, or reconsider gravity flow viability — may need pumping if gravity head insufficient, though pumping at unloading stations contradicts decomposition scope — coordinate with design team if gravity flow not viable)

7. **Confirm slope achievable with layout:**
   - Required slope: Calculate minimum slope required to achieve capacity (from above calculations — slope is input, but verify slope adequate for capacity; if capacity inadequate at available slope, calculate required slope: rearrange Manning or Darcy-Weisbach to solve for slope given Q, D, other parameters)
   - Available slope: From DEL-10.01 layout (actual slopes from profile) or from site elevations (elevation difference ÷ horizontal distance = available slope)
   - Verify required ≤ available: If required slope ≤ available slope from DEL-10.01, layout is adequate (slope sufficient for calculated capacity); If required slope > available slope, layout needs adjustment (coordinate with DEL-10.01 to increase slope — raise inlet or lower outlet elevations if possible — or increase pipe size to achieve capacity at available slope)

8. **Document results:**
   - **Results summary table:**
     - Design flow rate: [X] m³/hr
     - Selected pipe size: [Y]" (DN[Z]mm) standard pipe
     - Wall thickness: [W]mm per ASME B31.3
     - Calculated flow velocity: [V] m/s (verify within [V_min] to [V_max] range)
     - Slope: [S] (e.g., 1:100 = 1%) from DEL-10.01 or assumed
     - Pressure drop: [ΔP] kPa (friction + fittings + elevation)
     - Available gravity head: [H] kPa (from elevation difference)
     - Margin: [M]% (capacity margin = (header capacity − required throughput) / required throughput × 100%)
   - **Acceptance criterion verification:**
     - Header capacity ≥ design throughput + margin? Yes/No (pass/fail) — demonstrate capacity adequate
     - Velocity within acceptable range? Yes/No (pass/fail)
     - Slope achievable with layout? Yes/No (pass/fail)
     - Gravity flow viable (head ≥ pressure drop)? Yes/No (pass/fail)
   - **Conclusions:** "Gravity flow header sized at [X]" diameter with [S] slope provides capacity of [C] m³/hr, which exceeds design requirement of [R] m³/hr by [M]% margin. Flow velocity [V] m/s is within acceptable range. Gravity flow viable with available head. Header sizing meets requirements."

**Output:** Header pipe sizing calculation documented (inputs, assumptions, method, step-by-step calculations with intermediate results, results summary, conclusions, acceptance criterion verification).

**Traceability to Specification:**
- FN-01: Header pipe sizing calculation performed ✓
- PF-01: Header capacity ≥ design + margin verified ✓ (pass/fail documented)

---

#### **Step 4c: Containment Volume Calculations**

**Objective:** Size spill containment pans and sumps per regulatory requirements; demonstrate regulatory compliance (Specification.md FN-03, PF-03).

**Calculation Steps (follow Guidance.md §Examples — Containment Calculation Flow):**

1. **Identify regulatory requirements** (from Step 2 regulatory inputs):
   - Applicable regulations: **TBD** (Environment Canada Code of Practice, BC regulations, Surrey bylaws — document specific regulations applicable to this project; cite regulation name, edition, section)
   - Containment volume formula: **TBD** (extract from regulations — typically 110% of largest vessel, or 100% + freeboard + rainfall allowance; document formula and cite regulation section)
   - Worst-case spill scenario: **TBD** (per regulations — typically single largest source; adapt for railcar unloading context — one railcar typical)
   - Rainfall allowance requirement: **TBD** (if required — design storm criteria; if not required, document why exempted)
   - Freeboard requirement: **TBD** (minimum freeboard above design liquid level — from regulations or engineering practice; typical 150–300mm)

2. **Determine worst-case spill volume:**
   - Identify potential spill sources: One railcar full capacity (if railcar connection fails or ruptures — largest volume at any single station), header section volume between isolation valves (if header ruptures — volume of pipe segment; calculate from pipe size per Step 4b and section length per DEL-10.01), other sources **TBD** (pump rupture if large pumps — typically small; arm rupture — small volume in arm; unlikely controlling)
   - Calculate volume for each source:
     - One railcar: Railcar capacity **TBD** (e.g., 100 m³ from Step 2/3 assumptions or railcar data from PKG-07)
     - Header section: π/4 × D² × L (pipe internal diameter from Step 4b × section length between isolation valves from DEL-10.01 — e.g., 8" diameter × 50m section = ~0.2² × π/4 × 50 = ~1.6 m³ — typically much smaller than one railcar)
     - Other sources: Calculate if applicable
   - Select worst-case: Largest volume among sources (typically one railcar capacity ~100 m³ is controlling — significantly larger than header section or other sources)
   - Document worst-case selection and justification: "Worst-case spill scenario = one full railcar capacity = [100] m³. Rationale: Largest single source at any station; significantly larger than header section volume (~1.6 m³ per [calculation]) or other sources. Conservative assumption: largest railcar capacity used if fleet has range of sizes."

3. **Add rainfall allowance** if applicable (if regulations require — verify in Step 2):
   - **If rainfall allowance required by regulations:**
     - Design storm criteria: **TBD** (e.g., 24-hour rainfall, 1-in-25-year return period, or per regulation)
     - Rainfall intensity/amount: **TBD** (obtain from climate data for Fraser Surrey, BC — e.g., Environment Canada climate normals; 24-hour design storm rainfall amount — e.g., 50–100mm typical for Fraser Valley depending on return period)
     - Containment pan area: From DEL-10.01 Containment Details (measure pan area from drawings) or assume based on railcar footprint and access allowances (e.g., ~20–40 m² per station for under-track containment pan — order of magnitude)
     - Rainfall volume: Rainfall amount (mm) × pan area (m²) ÷ 1000 = rainfall volume (m³) (e.g., 75mm rain × 30 m² pan = 2.25 m³ rainfall volume)
   - **If rainfall allowance not required:** Document exemption (e.g., "Rainfall allowance not required per [regulation] due to covered containment" — verify containment covered per DEL-10.01 design; or "Rainfall allowance not required per [regulation] Section X exemption for [reason]")

4. **Add freeboard:**
   - Freeboard height: **TBD** (from regulations or engineering practice — typical 150–300mm; e.g., 200mm = 0.2m assumed)
   - Freeboard volume: Freeboard height × pan area = freeboard volume (e.g., 0.2m × 30 m² = 6 m³)
   - Or include freeboard in total depth calculation below (freeboard as additional depth above liquid depth)

5. **Calculate total required containment volume:**
   - **If regulatory formula is additive:** Total required volume = worst-case spill volume + rainfall volume (if applicable) + freeboard volume (e.g., 100 m³ spill + 2.25 m³ rain + 6 m³ freeboard = 108.25 m³ total required)
   - **If regulatory formula is percentage:** Total required volume = 110% × worst-case spill volume (or per regulation — e.g., 110% × 100 m³ = 110 m³; then add rainfall and freeboard if required in addition to 110%, or if 110% includes freeboard — verify regulatory formula interpretation)
   - Apply most stringent requirement if multiple formulas (if multiple regulations apply with different formulas, satisfy all — use largest required volume)

6. **Compare to pan sizing from DEL-10.01 layout:**
   - Obtain pan dimensions from DEL-10.01 Containment Details (if available — length, width, depth of containment pans)
   - Calculate pan volume: Length × width × depth (liquid depth, not including freeboard) = pan volume (verify volume ≥ required volume from above)
   - **If individual pans per station:** Each pan volume ≥ required volume per station (verify each of 32 pans provides ≥ 108.25 m³ in example — or per calculated requirement)
   - **If common containment system:** Total system volume ≥ required volume for applicable scenario (if common system for all 32 stations: verify total volume ≥ worst-case spill — typically one railcar, not all 32 simultaneously unless regulations require; verify regulatory interpretation for common containment — see Guidance.md §Considerations for multiple spill scenario discussion)
   - **If DEL-10.01 not available (preliminary):** Calculate required pan dimensions (assume reasonable pan footprint — e.g., 5m × 6m = 30 m² per railcar footprint and access; calculate required depth: required volume ÷ pan area = liquid depth; add freeboard to get total pan depth; verify depth practical — typically 0.5–2.0m total depth for constructibility; if depth excessive, increase pan area to reduce depth)

7. **Verify regulatory compliance:**
   - Compliance statement: "Containment volume provided = [X] m³ ≥ regulatory requirement = [Y] m³ per [regulation citation — name, edition, section]. Design complies with [regulation name]."
   - Cite specific regulation: Include regulation name, edition/version, specific section or clause defining containment requirement (e.g., "Per Environment Canada Environmental Code of Practice for Aboveground and Underground Storage Tank Systems, 2nd Edition (2003), Section 4.2.1, secondary containment volume shall be 110% of largest tank volume. Containment volume provided = [X] m³ = 110% × [railcar capacity] m³. Complies with Code of Practice Section 4.2.1.")
   - If exceeding regulatory minimum: Note margin (e.g., "Containment volume provided = 120 m³ exceeds regulatory requirement = 110 m³ by 9% margin — provides additional environmental protection")

8. **Size sump and pump** (for containment drainage):
   - **Sump sizing:**
     - Drainage requirement: Sump must accommodate drainage from containment pans (pan volume drains to sump via gravity)
     - Pump cycling: Sump volume = pump flow rate × pump run time between start/stop cycles (typical 5–15 minutes run time for reasonable pump cycling — not continuous operation; e.g., if pump flow rate 10 m³/hr, sump volume = 10 m³/hr × 10 min ÷ 60 min/hr = 1.67 m³ for 10-minute cycling)
     - High-level alarm offset: Add volume for high-level alarm above pump stop level (typical 200–500mm or per alarm requirements)
     - Total sump volume: Pump cycling volume + alarm offset volume = total sump volume
   - **Pump capacity sizing:**
     - Drainage time requirement: **TBD** (from regulations or operations requirements — typical 4–24 hours; faster drainage better for environmental protection and operations recovery but requires larger pump; verify requirement)
     - Required pump flow rate: Containment volume ÷ drainage time = minimum pump flow rate (e.g., 108 m³ ÷ 24 hr = 4.5 m³/hr minimum)
     - Add design margin: Pump flow rate = minimum × (1 + margin) — typical 10–25% margin for pump degradation, reliability (e.g., 4.5 m³/hr × 1.20 = 5.4 m³/hr design pump capacity)
     - Pump head: Sump depth + discharge piping elevation and friction losses + discharge pressure (if pumping to process system or drain system — coordinate with DEL-10.01 and PKG-14 for discharge piping configuration and elevation)
     - Select pump: Size pump for required flow rate and head (refer to DEL-10.04 for pump selection or specify requirements for pump procurement)

9. **Document results and comparison to acceptance criteria:**
   - **Results summary table:**
     - Worst-case spill volume: [X] m³ (one railcar capacity or other controlling scenario)
     - Rainfall allowance: [Y] m³ (if applicable) or N/A (if exempted — state reason)
     - Freeboard: [Z] m³ (freeboard height × pan area)
     - Total required containment volume: [X + Y + Z] m³
     - Containment volume provided: [V] m³ (from DEL-10.01 pan sizing or calculated pan dimensions)
     - Regulatory requirement: [R] m³ (per [regulation citation])
     - Sump volume: [S] m³
     - Pump capacity: [P] m³/hr at [H] m head
   - **Acceptance criterion verification:**
     - Containment volume provided ≥ regulatory requirement? Yes/No (pass/fail)
     - Regulatory compliance demonstrated? Yes/No (citation provided, compliance shown)
   - **Conclusions:** "Spill containment volume of [V] m³ meets regulatory requirement of [R] m³ per [regulation citation]. Worst-case spill scenario (one railcar capacity [X] m³) analyzed with rainfall allowance [Y] m³ (if applicable) and freeboard [Z] m³. Design complies with [regulation name] and OBJ-7 environmental protection objective. Sump pump sized at [P] m³/hr provides drainage within [T] hours."

**Output:** Containment volume calculation documented (inputs including regulatory requirements, assumptions, method, step-by-step calculations, results summary with regulatory compliance statement and citation, conclusions, regulatory requirement excerpts in appendices).

**Traceability to Specification:**
- FN-03: Containment volume calculation performed ✓
- PF-03: Regulatory compliance verified ✓ (containment volume ≥ regulatory requirement; pass/fail documented with citation)
- IN-05: Regulatory requirements documented ✓ (regulations identified, formula extracted, cited in calculation)

---

### Step 5: Independent Check

**Objective:** Verify calculation accuracy, completeness, and compliance through independent check by qualified checker (Specification.md QA-01 requirement).

**Actions:**

1. **Issue calculation package to independent checker:**
   - Assign checker (must be independent from calculation author per Specification.md QA-01 — different person; qualified per §Personnel Requirements)
   - Provide checker with complete calculation package:
     - All 3 calculation documents (Header Sizing, Unloading Rate, Containment Volume)
     - Specification.md (requirements to verify)
     - Guidance.md (principles and considerations to verify)
     - Datasheet.md (design parameters and calculation scope)
     - Input sources (ER excerpts, product data sheets, DEL-10.01 drawings if available, DEL-10.04 data sheets if available, regulations for containment)
     - Reference materials (codes, standards, handbooks used in calculations)

2. **Checker reviews calculations** against all requirements (comprehensive check per Specification.md §Verification):

   **a) Input accuracy and sources (Specification.md IN-01 through IN-05; Procedure.md Step 2 verification):**
   - Verify all inputs documented with sources (check input summary — all parameters have values and sources cited)
   - Verify sources appropriate (ER for design basis, product data for properties, DEL-10.01 for geometry, DEL-10.04 for equipment, regulations for containment — verify sources per IN requirements)
   - Verify input values reasonable (order-of-magnitude check — values realistic for application; e.g., density ~920 kg/m³ reasonable for vegetable oil, viscosity ~70 cSt reasonable for canola oil at ~20°C, throughput 1,000,000 MT/annum per decomposition, etc.)
   - Verify input values current (if values from ER or other deliverables, verify latest version used; if assumptions, verify marked as assumptions and flagged for verification)
   - Note any input errors or questionable values (document in checker comments for author resolution)

   **b) Assumption validity and conservatism (Specification.md FN-04; Procedure.md Step 3 verification):**
   - Verify all assumptions documented with justification (check assumption log — all assumptions listed with basis/justification, impact assessment, verification requirements)
   - Verify assumptions reasonable (assumptions based on industry practice, code guidance, conservative approach, or other sound engineering basis — not arbitrary or overly optimistic)
   - Verify assumptions appropriately conservative per Guidance.md §Conservatism Guidelines (conservative assumptions where uncertainty significant — reduces risk of under-capacity or non-compliance; avoid excessive conservatism — uneconomical over-design)
   - Verify critical assumptions flagged for verification (assumptions with significant impact on results marked for verification when data available — e.g., simultaneous operations, product viscosity, unloading rate per station, regulatory requirements)
   - Verify assumption impact understood (assumptions with significant impact identified; assumptions with low impact noted; impact assessment reasonable)
   - Note any questionable assumptions (assumptions not well-justified, assumptions too optimistic or too conservative, assumptions with unclear impact — document in checker comments)

   **c) Method appropriateness and correctness (Specification.md QA-03; Procedure.md Step 4 verification):**
   - Verify methods suitable for application (methods appropriate for calculation purpose — gravity flow hydraulics for header sizing, mass balance for throughput, regulatory formula for containment; not overly complex or overly simplified per Guidance.md §Trade-offs calculation complexity consideration)
   - Verify methods correctly applied (equations correct — check equation forms against references cited; variables defined correctly; units consistent throughout; sign conventions correct — e.g., pressure drop sign, elevation change sign)
   - Verify methods cited with references (codes, standards, handbooks cited — e.g., "Darcy-Weisbach equation per ASME B31.3 Appendix A" or "Manning equation per Open Channel Hydraulics, Chow"; verify citations correct — correct reference, correct section/page/equation)
   - Verify method logic sound (calculation flow logical from inputs to results; intermediate steps make sense; no gaps in logic; assumptions clearly stated where used in methods)
   - Note any method errors or inappropriate methods (equation errors, incorrect method selection, missing steps, logic errors — document in checker comments)

   **d) Arithmetic accuracy (verify all calculations step-by-step):**
   - Check arithmetic: Verify all numerical calculations correct (use calculator or spreadsheet to spot-check calculations; verify critical calculations in detail; may use sampling for extensive calculations — check representative sample thoroughly, scan remainder for obvious errors)
   - Check unit conversions: Verify all unit conversions correct (e.g., MT to m³ using density, cSt to m²/s for kinematic viscosity, mm to m for dimensions, kPa to m of head for pressure conversions — verify conversion factors correct; verify units cancel properly in equations)
   - Check intermediate results: Verify intermediate results reasonable (order-of-magnitude check — do intermediate values make sense? e.g., Reynolds number ~10⁴ to 10⁶ for turbulent pipe flow typical; friction factor 0.015–0.030 for turbulent flow in steel pipe typical; velocity 1–3 m/s per velocity limits; pressure drop fraction of available head for viable gravity flow)
   - Verify final results: Check final result calculations (verify results calculated correctly from intermediate results; verify results have correct units; verify results compared to acceptance criteria correctly)
   - Note any arithmetic errors (calculation errors, unit conversion errors, transcription errors — document for correction)

   **e) Software output verification (Specification.md QA-04) if software used:**
   - Verify software appropriate for application (hydraulic analysis software suitable for pipe flow calculations if used — e.g., AFT Fathom appropriate for header sizing; spreadsheet appropriate for throughput and containment calculations)
   - Verify software inputs correct (if software used — e.g., hydraulic model in AFT Fathom: verify geometry input correctly — pipe lengths, diameters, elevations; verify properties input correctly — density, viscosity; verify operating conditions input correctly — flow rate, temperature; check for input errors or typos)
   - Verify software outputs reasonable (spot-check software results with hand calculations or alternative methods; verify results order-of-magnitude reasonable; check for obvious software errors or modeling errors — e.g., unrealistic pressures, flow reversals, negative heads)
   - Verify software output documented (software output files, screenshots, or printouts included in calculation appendices per Specification.md QA-04; verify outputs traceable — can match reported results to software outputs)
   - Note any software issues (incorrect inputs, unreasonable outputs, undocumented outputs, software not appropriate for application — document for resolution)

   **f) Results vs. acceptance criteria (Specification.md PF-01, PF-02, PF-03; Procedure.md Step 1 acceptance criteria verification):**
   - **Header sizing:** Verify header capacity ≥ design throughput + margin (check results summary — capacity calculated, margin calculated, compared to requirement; pass/fail clearly stated); verify velocity within limits (V_min ≤ V ≤ V_max); verify slope achievable; verify gravity flow viable (head ≥ pressure drop)
   - **Unloading rate:** Verify calculated throughput ≥ 1,000,000 MT/annum (check results summary — annual throughput calculated, compared to 1,000,000 MT/annum; pass/fail clearly stated; preferably with margin e.g., ≥ 1,100,000 MT/annum); verify 32 stations adequate (required simultaneous + margin ≤ 32); verify unloading time acceptable
   - **Containment volume:** Verify calculated/provided volume ≥ regulatory requirement (check results summary — containment volume, regulatory requirement, comparison, pass/fail, regulatory compliance statement with citation); verify worst-case scenario reasonable; verify regulatory formula correctly applied
   - Verify all acceptance criteria met (all calculations pass acceptance criteria — if any fail, calculations must be revised in coordination with design team; design changes may be required to achieve acceptable results)
   - Note any failures or marginal results (results not meeting acceptance criteria or barely meeting criteria — document for resolution or design revision)

   **g) Documentation completeness (Specification.md FN-04; reproducibility per QA-01):**
   - Verify all required sections present (cover, purpose, inputs, assumptions, methods, calculations, results, conclusions, appendices per Datasheet.md §Construction calculation report structure)
   - Verify documentation complete (all inputs documented, all assumptions documented, all methods documented, all results documented; no gaps or missing information)
   - Verify documentation clear (calculations presented clearly; step-by-step calculations easy to follow; results summarized; conclusions clear; another engineer can understand and verify calculations from documented information — reproducibility test)
   - Verify metadata complete (calculation number, title, revision, date, author, checker, approver per Datasheet.md §Attributes — cover page has all metadata; verify author name present; checker and approver names to be added after check/approval)
   - Note any documentation gaps or unclear presentation (missing sections, unclear methods, insufficient detail for verification, missing metadata — document for completion)

3. **Document checker review findings:**
   - **If no issues found:** Checker stamps/signs calculations as checked and acceptable (stamp each page or provide summary checker sign-off sheet; signature on cover page in checker signature block; date of check)
   - **If issues found:** Checker documents comments (comment list or marked-up calculations — redline corrections or comments; comment severity: error — must correct, question — clarify or verify, suggestion — optional improvement)
   - Prepare checker comment list (if comments issued): Comment number, page/section reference, comment description, severity, suggested resolution (e.g., "Comment C-1: Page 5, Header Sizing. Error: Velocity calculation uses wrong pipe diameter (used 6" instead of 8" selected size). Recalculate velocity with correct diameter.")

4. **Resolve checker comments** (author addresses all comments):
   - Author reviews checker comments (review comment list and marked-up calculations)
   - Resolve all errors and questions (correct errors — arithmetic errors, method errors, input errors; clarify questions — provide additional justification, correct misunderstandings, verify values)
   - Address suggestions as appropriate (consider improvement suggestions; implement if beneficial and within scope)
   - Update calculations with corrections (incorporate corrections into calculation package; recalculate as needed if errors affect results; verify results still meet acceptance criteria after corrections)
   - Respond to checker on comment dispositions (comment response log: comment number, disposition — corrected/clarified/accepted/rejected, explanation if rejected or modified differently than suggested)

5. **Obtain checker sign-off** (after comments resolved):
   - Reissue corrected calculations to checker (if significant corrections — checker reviews corrections and verifies issues resolved)
   - Checker verifies all critical issues resolved (errors corrected, questions clarified, results recalculated if needed)
   - Checker signs off on calculations (checker signature on cover page in checker signature block; date of final check; confirms independent check complete and calculations acceptable for issue)
   - File checker sign-off and comment resolution record in `1_Working/` (maintain record of check process — original comments, resolutions, final checker sign-off)

**Output:** Checked calculation package with checker sign-off; all checker comments resolved; ready for discipline lead approval (Step 6).

**Verification:** Checker sign-off (Specification.md QA-01) confirming independent check performed and calculations acceptable; checker comment resolution record if comments issued.

---

### Step 6: Approval and Issue

**Objective:** Obtain discipline lead approval and issue calculation package; communicate results to other deliverables for incorporation (DEL-10.01, DEL-10.02, DEL-10.04).

**Actions:**

1. **Submit checked calculation package for discipline lead approval:**
   - Provide discipline lead with complete approval package:
     - Calculation package (all 3 calculations with checker sign-off)
     - Calculation basis (approved scope from Step 1)
     - Checker comment resolution record (if comments issued — shows all comments resolved)
     - Supporting deliverables for reference (DEL-10.01 drawings if available, DEL-10.02 specification, input sources)

2. **Discipline lead reviews calculations for:**
   - **Technical completeness:** All required calculations performed (3 calculation topics per scope); all inputs, assumptions, methods, results documented; documentation complete per calculation report structure
   - **Results acceptable:** All acceptance criteria met (header capacity adequate with margin, throughput ≥ 1,000,000 MT/annum, containment volume ≥ regulatory requirement); results reasonable (engineering judgment — results make sense for application; comparison to industry practice or similar facilities if available)
   - **Checker comments resolved:** All checker comments addressed (errors corrected, questions clarified, issues resolved; checker sign-off obtained)
   - **Appropriateness for use:** Calculations suitable for intended use (sizing basis for DEL-10.01 drawings and DEL-10.02 specifications; procurement basis; regulatory submittals; OBJ-1, OBJ-2, OBJ-7 verification)

3. **Obtain discipline lead approval sign-off:**
   - Discipline lead signs approval on calculation cover page (approver signature block; date of approval)
   - Approval confirms calculations approved for issue (technical adequacy confirmed, results acceptable, appropriateness confirmed)
   - File approval record in `1_Working/`

4. **Finalize document metadata** (Datasheet.md §Attributes):
   - Finalize calculation number(s): Coordinate with document control for number assignment per project numbering procedure **TBD** (may be single package number or individual numbers for each calculation topic)
   - Set revision: Initial issue (0 or A per convention **TBD**)
   - Set issue date: Current date (date of approval or issue)
   - Verify all sign-offs present: Author (calculation author signature/date on cover), checker (checker signature/date from Step 5), approver (discipline lead signature/date from this step)
   - Verify software documented: Software name, version, license noted per QA-04 if software used (e.g., "AFT Fathom v12.0, License #XXXX" or "Microsoft Excel 365")
   - Verify design code cited: Codes and standards listed (ASME B31.3, hydraulic references, environmental regulations — per §Standards)
   - Set classification: Per project requirements **TBD**

5. **Prepare transmittal** per project document control procedure **TBD**:
   - Transmittal form or cover letter (list calculations being issued: calculation numbers, titles, revisions, dates)
   - Identify recipients: Employer (for review/approval), design team (DEL-10.01, DEL-10.02, DEL-10.04 — for incorporation of results), procurement team (for equipment sizing basis), regulatory authorities (for permit submittals if required), document control (for distribution)
   - Transmittal purpose: "Issued for Design" (if for incorporation into drawings/specifications), "Issued for Construction" (if IFC stage), "Issued for Regulatory Review" (if for permits), or other purpose per project convention
   - Obtain document controller sign-off on transmittal

6. **Issue calculation package:**
   - Submit to document control for distribution (per transmittal recipients)
   - Document control distributes per project distribution matrix
   - Document control updates document register (record calculation numbers, titles, revisions, issue date, distribution)

7. **Communicate results to other deliverables** for incorporation (critical for design integration):
   - **To DEL-10.01 (Design Drawing Set):**
     - Header pipe sizes: Communicate selected pipe size and wall thickness from header sizing calculation (DEL-10.01 Header Layout to show pipe sizes per calculations)
     - Slopes: Confirm slopes from calculation (verify DEL-10.01 slopes match calculation assumptions; if iterative, verify actual slopes from DEL-10.01 layout result in adequate capacity per recalculation)
     - Containment dimensions: Communicate required containment volume and resulting pan dimensions from containment calculation (DEL-10.01 Containment Details to show pan dimensions providing required volume per calculations)
     - Coordinate design: If calculation results require design changes (pipe size larger than assumed in preliminary DEL-10.01, containment deeper than shown on preliminary drawings, etc.), coordinate with DEL-10.01 design team for layout updates
   - **To DEL-10.02 (Technical Specification):**
     - Performance requirements: Communicate calculated capacities as basis for specification performance requirements (header flow capacity from header sizing, unloading rate from throughput calc, containment volume from containment calc — DEL-10.02 performance requirements based on calculation results)
     - Verify specification requirements achievable: Confirm equipment specified in DEL-10.02 meets performance requirements from calculations (arm flow capacity adequate per throughput calc, header size adequate per header sizing calc, containment volume adequate per containment calc)
   - **To DEL-10.04 (Data Sheet Package):**
     - Equipment sizing requirements: Communicate equipment capacity requirements from calculations (unloading arm flow capacity from throughput calc, sump pump capacity from containment calc — DEL-10.04 data sheets specify equipment meeting calculated requirements)
     - Coordinate equipment selection: If iterative, verify selected equipment data from DEL-10.04 matches calculation assumptions (if equipment data changes, recalculate to verify with actual equipment; update calculations if results change)
   - **Documentation:** Document results communication (memo, transmittal, or email to other deliverable leads noting calculation results and coordination requirements; maintain record of coordination in `1_Working/` folder)

8. **File records** per §Records below:
   - Working records in `1_Working/`: calculation basis (Step 1), input summary (Step 2), assumption log (Step 3), draft calculations (Step 4), checker comments and resolution (Step 5), approval sign-off, transmittal record, results communication record
   - Issued calculations in `3_Issued/`: final issued calculation package (all 3 calculations with all sign-offs — author, checker, approver)

9. **Update deliverable status:**
   - **Note:** Status updates are human-managed per project workflow (see `_STATUS.md`)
   - This procedure does not automatically update status
   - **Typical status progression:** OPEN → INITIALIZED (after Pass 1 draft) → IN_PROGRESS (during Steps 1–5) → CHECKING (during Step 5 independent check) → ISSUED (after Step 6 issue)

**Output:** Issued calculation package (all 3 calculations with sign-offs); results communicated to other deliverables for integration; transmittal record; document register updated.

**Verification:**
- Discipline lead approval sign-off (confirms calculations approved for issue — technical adequacy, results acceptable, completeness verified)
- Document controller confirmation of issue (transmittal acknowledgment, distribution confirmation)
- Results communication record (documents coordination with DEL-10.01, DEL-10.02, DEL-10.04 for design integration)

**Note for Subsequent Revisions:**
- Calculations may require revision if inputs change (ER requirements clarified, product data obtained, DEL-10.01 layout finalized, DEL-10.04 equipment data finalized — if inputs change significantly from assumptions, recalculate)
- Revision process similar (Steps 2–6 as applicable with updated inputs; document what changed in revision; update revision history on cover page; maintain previous revision for traceability)
- Coordinate revisions with other deliverables (if calculation results change significantly, coordinate with DEL-10.01, DEL-10.02, DEL-10.04 to update their content accordingly — ensure design remains integrated)

---

## Verification

**Verification Summary:**

| Step | Verification Activity | Responsible | Record | Specification Link | Datasheet Link |
|------|----------------------|-------------|--------|--------------------|--------------------|
| 1 | Scope/basis approval | Discipline lead | Approved calculation basis with sign-off | Specification.md FN-01, FN-02, FN-03 (calculation topics); PF-01, PF-02, PF-03 (acceptance criteria) | Datasheet.md §Construction (calculation scope); §Verification (acceptance criteria table) |
| 2 | Input documentation | Calculation author | Input summary with sources (in calculation package) | Specification.md IN-01 through IN-05 (all input requirements) | Datasheet.md §Conditions (input parameters); §Construction (inputs summary in each calculation) |
| 3 | Assumption documentation | Calculation author | Assumption log with justification (in calculation package) | Specification.md FN-04 (assumptions documented); Guidance.md conservatism guidelines | Datasheet.md §Construction (assumptions in calculation report structure) |
| 4 | Calculation execution and completion | Calculation author | Draft calculation package (all 3 calculations documented) | Specification.md FN-01, FN-02, FN-03 (all calculation topics completed); PF-01, PF-02, PF-03 (results meet acceptance criteria) | Datasheet.md §Construction (all 3 calculation documents completed) |
| 5 | Independent check | Checker (independent from author) | Checker sign-off; checker comment resolution record if comments issued | Specification.md QA-01 (independent check requirement); QA-03, QA-04 (method and software verification) | — |
| 6 | Discipline lead approval | Discipline lead | Approval sign-off on calculation cover page(s) | Specification.md (overall quality and technical adequacy — inferred from quality requirements) | — |
| 6 | Issue confirmation | Document controller | Transmittal record; document register entry | Specification.md QA-02 (document control — metadata and issue) | Datasheet.md §Attributes (issue metadata) |
| 6 | Results communication | Calculation author / discipline lead | Results communication record (coordination with DEL-10.01, DEL-10.02, DEL-10.04) | Specification.md FN-05 (traceability — results support design decisions in other deliverables); Datasheet.md §Construction (downstream use for each calculation documented) | Datasheet.md §Construction (downstream use); §References (related deliverables) |

**Requirement Verification Matrix (Comprehensive Traceability to Specification.md):**

| Req ID | Requirement Summary | Verification Step(s) | Verification Method | Record | Guidance Link | Datasheet Link |
|--------|---------------------|---------------------|---------------------|--------|---------------|----------------|
| FN-01 | Header pipe sizing calculation | 4b, 5 | Calculation execution; independent check (verify calculation performed per method; verify results reasonable; verify documentation complete) | Header Pipe Sizing Calculation document; checker sign-off | Guidance.md §Considerations (header sizing factors); §Examples (header sizing flow) | Datasheet.md §Construction (Header Sizing topic) |
| FN-02 | Unloading rate calculation | 4a, 5 | Calculation execution; independent check (verify throughput calculation performed; verify results ≥ 1,000,000 MT/annum) | Unloading Rate Calculation document; checker sign-off | Guidance.md §Considerations (unloading rate factors); §Examples (unloading rate flow) | Datasheet.md §Construction (Unloading Rate topic) |
| FN-03 | Containment volume calculation | 4c, 5 | Calculation execution; independent check (verify containment calculation performed; verify regulatory compliance) | Containment Volume Calculation document; checker sign-off | Guidance.md §Considerations (containment factors); §Examples (containment flow) | Datasheet.md §Construction (Containment Volume topic) |
| FN-04 | Document inputs/assumptions/methods | 2, 3, 4, 5 | Documentation review by checker (verify all inputs, assumptions, methods documented per requirement); reproducibility verification (checker can reproduce results from documentation) | Input summary, assumption log, method documentation in calculations; checker sign-off | Guidance.md §Principles (transparency, reproducibility, documentation) | Datasheet.md §Construction (calculation report structure includes all documentation) |
| FN-05 | Traceability to design basis and ER | 2, 5, 6 | Document review (verify inputs traced to sources — ER, decomposition, other deliverables); results communication (verify results linked to downstream use — DEL-10.01, DEL-10.02, DEL-10.04) | Input summary with sources, results communication record; checker verification of traceability | Guidance.md §Principles (traceability principle) | Datasheet.md §References (sources); §Construction (downstream use for each calculation) |
| FN-06 | Additional calculation requirements | 1, 2, 4, 5 | **TBD** — per ER requirements (identify in Step 1; execute in Steps 2–4; verify in Step 5) | **TBD** | — | — |
| PF-01 | Header capacity ≥ design + margin | 4b, 5 | Calculation results review (verify header capacity calculated; verify capacity ≥ design throughput + margin; verify pass/fail clearly stated in results summary) | Header sizing calculation results summary; acceptance criterion verification; checker sign-off | Guidance.md §Considerations (header sizing — margin); §Trade-offs (margin magnitude) | Datasheet.md §Verification (acceptance criterion: capacity > design + margin) |
| PF-02 | Throughput ≥ 1,000,000 MT/annum | 4a, 5 | Calculation results review (verify throughput calculated; verify ≥ 1,000,000 MT/annum with margin; verify pass/fail) | Unloading rate calculation results summary; acceptance criterion verification; checker sign-off | Guidance.md §Principles (OBJ-2); §Considerations (throughput basis); §Conservatism | Datasheet.md §Verification (acceptance criterion: ≥ 1,000,000 MT/annum) |
| PF-03 | Containment ≥ regulatory requirement | 4c, 5 | Calculation results review (verify containment volume calculated; verify ≥ regulatory requirement with citation; verify compliance demonstrated; verify pass/fail) | Containment calculation results summary; regulatory compliance statement; checker sign-off | Guidance.md §Principles (OBJ-7); §Considerations (regulatory basis); §Conservatism | Datasheet.md §Verification (acceptance criterion: ≥ regulatory requirement) |
| PF-04 | Additional performance criteria | 1, 4, 5 | **TBD** — per ER requirements | **TBD** | — | — |
| IN-01 to IN-05 | All input requirements | 2, 5 | Input review by checker (verify all inputs documented with sources per IN-01 through IN-05 requirements; verify sources appropriate; verify values reasonable) | Input summary in calculations with sources; checker verification of inputs | Guidance.md §Principles (complete inputs); §Considerations (input categories) | Datasheet.md §Conditions (all input parameters) |
| QA-01 | Independent check performed | 5 | Checker sign-off (confirms independent check performed per comprehensive verification process in Step 5); checker comment resolution if comments issued | Checker sign-off; checker comments and resolution record | Guidance.md §Principles (reproducibility enables checking) | — |
| QA-02 | Metadata complete | 6 | Document check (verify all metadata fields populated per Datasheet.md §Attributes); document control review | Calculation cover pages with complete metadata; transmittal | Guidance.md §Principles (documentation) | Datasheet.md §Attributes (all metadata fields) |
| QA-03 | Methods documented and reproducible | 4, 5 | Method review by checker (verify methods documented with citations; verify methods appropriate; verify calculations reproducible — checker can verify results from documented methods) | Method documentation in calculations; checker sign-off on method verification | Guidance.md §Principles (transparency, reproducibility); §Considerations (appropriate methods) | Datasheet.md §Construction (method documentation in calculation report structure) |
| QA-04 | Software verification if used | 4, 5 | Software verification by checker (verify software appropriate; verify inputs correct; verify outputs reasonable and documented) | Software documentation in calculations; software outputs in appendices; checker verification | Guidance.md §Principles (accuracy — software must be appropriate) | Datasheet.md §Attributes (software used); §Construction (software outputs in appendices) |
| QA-05 | Additional quality requirements | 1, 5, 6 | **TBD** — per ER requirements | **TBD** | — | — |

---

## Records

**Documentation Outputs (Deliverable Artifacts — the calculations produced by this procedure):**

| Record | Description | Filing Location | Specification Link | Datasheet Link | Guidance Link |
|--------|-------------|-----------------|--------------------|--------------------|---------------|
| **Header Pipe Sizing Calculation** | Complete calculation document (cover with metadata and sign-offs, purpose/scope, design basis inputs, assumptions, method, step-by-step calculations, results summary, conclusions, appendices) | `3_Issued/` (issued calculation); `1_Working/` (working drafts) | Specification.md FN-01, PF-01 (header sizing requirement); §Documentation | Datasheet.md §Construction (Header Pipe Sizing Calculation described); §Verification (acceptance criteria) | Guidance.md §Considerations (header sizing factors); §Examples (typical calculation flow) |
| **Unloading Rate / Throughput Calculation** | Complete calculation document (cover with metadata and sign-offs, purpose/scope, design basis inputs, assumptions, method, step-by-step calculations, results summary demonstrating ≥ 1,000,000 MT/annum, conclusions, appendices) | `3_Issued/` (issued calculation); `1_Working/` (working drafts) | Specification.md FN-02, PF-02 (unloading rate requirement); §Documentation | Datasheet.md §Construction (Unloading Rate Calculation described); §Verification (acceptance criteria) | Guidance.md §Considerations (unloading rate factors); §Examples (typical calculation flow) |
| **Containment Volume Calculation** | Complete calculation document (cover with metadata and sign-offs, purpose/scope, design basis inputs including regulatory requirements, assumptions, method, step-by-step calculations, results summary with regulatory compliance statement and citation, conclusions, appendices including regulatory excerpts) | `3_Issued/` (issued calculation); `1_Working/` (working drafts) | Specification.md FN-03, PF-03 (containment volume requirement and regulatory compliance); §Documentation | Datasheet.md §Construction (Containment Volume Calculation described); §Verification (acceptance criteria) | Guidance.md §Considerations (containment volume factors); §Examples (typical calculation flow) |

**Production Records (Supporting Documentation — records of calculation development process):**

| Record | Description | Filing Location | Purpose | Specification Link |
|--------|-------------|-----------------|---------|-------------------|
| Approved calculation basis | Calculation scope, input sources, methods, acceptance criteria with discipline lead sign-off (from Step 1) | `1_Working/` | Step 1 output; documents calculation approach approval before execution; basis for calculation development | Specification.md FN-01 through FN-03 (scope), PF-01 through PF-03 (acceptance criteria) |
| Input summary | Documented inputs with sources and status (confirmed/TBD/assumed) from Step 2; preliminary version updated during execution | `1_Working/` (separate or incorporated in final calculations) | Step 2 output; documents input gathering process; inputs incorporated into final calculations | Specification.md IN-01 through IN-05 (all input requirements) |
| Assumption log | Documented assumptions with justification, impact, verification requirements from Step 3; incorporated into final calculations | `1_Working/` (separate or incorporated in final calculations) | Step 3 output; documents all assumptions for transparency; assumptions incorporated into final calculations | Specification.md FN-04 (assumptions documented) |
| Checker comments and resolution | Checker comment list or marked-up calculations (if comments issued); comment resolution record showing disposition of all comments | `1_Working/` | Step 5 output if comments issued; demonstrates checking process and issue resolution; quality record | Specification.md QA-01 (independent check process) |
| Approval sign-off | Discipline lead approval signature on calculation cover pages | `1_Working/` or on issued calculations (cover pages) | Step 6 output; demonstrates calculations approved for issue | Specification.md (approval — inferred from quality requirements) |
| Transmittal record | Issue transmittal form/letter with distribution record | `1_Working/` | Step 6 output; documents calculation issue (what issued, when, to whom) | Specification.md QA-02 (document control) |
| Results communication record | Memo, email, or coordination record documenting results communication to DEL-10.01, DEL-10.02, DEL-10.04 (from Step 6 Item 7) | `1_Working/` | Step 6 output; documents design integration and coordination; ensures calculation results incorporated in other deliverables | Specification.md FN-05 (traceability — results support design decisions in other deliverables) |

**Record Management:**

| Location | Purpose | Contents | Access |
|----------|---------|----------|--------|
| `1_Working/` | Active working location for deliverable; all production records and working drafts | All production records listed above; working drafts of calculations (multiple iterations during development and checking); input data files (product data, regulations, etc.); reference materials (code excerpts, handbook pages, etc.); coordination correspondence | Discipline team access (calculation author, checker, discipline lead) |
| `2_Checking/To/` | Review packages during formal review cycles (if required per project convention for Employer review at stage gates) | Review copies of calculations submitted for Employer review at 30%, 60%, 90% stages; Employer review comments; review responses | Review team access (Employer, contractor review team) |
| `3_Issued/` | Issued calculations (final approved versions) | Final issued calculation package (all 3 calculations with all sign-offs — author, checker, approver); organized by revision if multiple issues | Project-wide access (design team, procurement team, construction contractors, regulatory authorities, Employer, QA/QC team) |

**Retention Requirements:**
- **TBD** — per project document control procedure and regulatory requirements
- **ASSUMPTION:** Electronic records maintained in project document management system with backup and archival (daily backup, offsite archival, long-term retention for professional liability protection)
- **ASSUMPTION:** Design calculations retained for project design life and beyond (typically permanent retention or 25–30+ years minimum; design calculations may be needed for future modifications, expansions, incident investigations, litigation — long-term retention protects engineer and contractor)
- **ASSUMPTION:** Issued calculations retained permanently; working records retained for duration of design and construction phase minimum (may be archived after project completion but retain for reference)

**Traceability:**
- All records linked to deliverable ID (DEL-10.03) per Datasheet.md §Identification
- Calculation numbers traceable to approved calculation basis (Step 1 scope definition)
- Revisions traceable through revision history on calculation cover pages and document register
- Inputs traceable to sources (ER, decomposition, DEL-10.01, DEL-10.04, product data, regulations — all sources cited in input summary)
- Results traceable to downstream deliverables (header sizing results used in DEL-10.01 and DEL-10.02; unloading rate results used in DEL-10.02 and DEL-10.04; containment results used in DEL-10.01 and DEL-10.02 — traceability through results communication record and cross-references in other deliverables)

**Pass 3 Final Verification:** All procedure steps aligned with Specification requirements, Guidance principles, and Datasheet attributes; comprehensive step-by-step calculation execution guidance provided for all 3 calculation topics; all cross-references bidirectional and verified; all TBDs and ASSUMPTIONs properly marked and sourced; terminology consistent across all four documents; verification matrix complete; acceptance criteria clearly defined and linked to verification steps; results communication process to other deliverables documented for design integration.
