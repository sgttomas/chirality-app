# Datasheet: DEL-27.02 HAZOP Study Reports

## Identification

| Field | Value |
|-------|-------|
| Deliverable ID | DEL-27.02 |
| Name | HAZOP Study Reports |
| Package | PKG-27 Engineering Design |
| Discipline | Design |
| Type | Report |
| Responsible | D&B Contractor |
| Status | INITIALIZED |

## Attributes

| Attribute | Value |
|-----------|-------|
| Study Type | Hazard and Operability Study (HAZOP) |
| Study Methodology | Structured HAZOP per IEC 61882 or equivalent — **TBD** |
| Study Scope | All major process systems for Phase 1 canola oil transload facility |
| Report Format | HAZOP worksheets with node descriptions, deviations, causes, consequences, safeguards, recommendations |
| Submission Stages | **TBD** — Align with design submission stages (30%, 60%, 90%, IFC per DEL-27.04) or as standalone milestone |
| HAZOP Team Composition | **TBD** — Multi-discipline team with facilitator, scribe, design leads, operations input |

**Source:** _CONTEXT.md; **ASSUMPTION**: Standard HAZOP methodology per IEC 61882 or equivalent industry practice

## Conditions

**Project Context:**

| Parameter | Value | Source |
|-----------|-------|--------|
| Facility Type | Canola oil transload facility (rail-to-ship) | Decomposition Section 1.1 |
| Product | CSD (Crude Super Degummed) canola oil | Decomposition Section 1.1 |
| Location | Fraser Surrey Terminal, 11060 Elevator Road, Surrey, BC | Decomposition Section 1.1 |
| Permitted Throughput | 1,000,000 MT per annum | Decomposition Section 1.1 (OBJ-2) |
| Storage Capacity | 45,000 MT (3 × 15,000 MT tanks) | Decomposition Section 1.1 (OBJ-3) |
| Railcar Capacity | 32 unloading stations on 2 tracks | Decomposition Section 1.1 |
| Operating Modes | Tank storage operations and direct rail-to-ship transfer | Decomposition Section 2 (OBJ-4) |

**HAZOP Study Scope (Major Systems):**

Systems to be analyzed in HAZOP study (typical scope for canola oil transload facility):

1. **Railcar Unloading System** (PKG-10)
   - 32 railcar unloading stations
   - Unloading pumps, piping, valves
   - Nitrogen blanketing and purge system
   - Spill containment and drainage

2. **Storage Tank System** (PKG-13)
   - 3 × 15,000 MT vertical storage tanks
   - Tank heating/cooling systems (if applicable)
   - Tank venting and pressure/vacuum relief
   - Level instrumentation and overfill protection
   - Secondary containment

3. **Transfer and Process Piping** (PKG-14)
   - Main transfer piping from railcar unloading to tanks
   - Tank-to-tank transfer piping
   - Tank-to-marine loading transfer piping
   - Pump suction and discharge piping
   - Piping relief and drainage systems

4. **Marine Loading System** (PKG-11)
   - Marine loading arms
   - Loading pumps and piping
   - Metering and custody transfer (PKG-12)
   - Emergency shutdown systems
   - Vapor recovery (if applicable)

5. **Pumps and Rotating Equipment** (PKG-15)
   - Unloading pumps
   - Transfer pumps
   - Loading pumps
   - Pump sealing systems

6. **Valves and Specialty Equipment** (PKG-16)
   - Isolation valves
   - Control valves
   - Relief valves
   - Emergency shutdown valves

7. **Electrical Power Distribution** (PKG-17)
   - Power distribution to motor-driven equipment
   - Hazardous area electrical classification
   - Emergency power systems

8. **Control Systems** (PKG-19)
   - Distributed control system (DCS) or PLC
   - Safety instrumented system (SIS)
   - Emergency shutdown (ESD) logic
   - Alarm and interlock systems

9. **Fire Protection and Safety Systems** (PKG-23, PKG-24)
   - Fire detection and suppression systems
   - Gas detection systems (if applicable)
   - Emergency response equipment

**Source:** Decomposition Sections 1.1, 4 (Package Summary); **ASSUMPTION**: Typical HAZOP scope covers all major process systems

**Operating Conditions for HAZOP Analysis:**

- **Normal operations:** Steady-state railcar unloading, tank storage, marine loading at design rates
- **Start-up and shutdown:** System commissioning, planned shutdowns, restart after maintenance
- **Upset conditions:** Equipment failures, operator errors, instrument failures, utility outages
- **Emergency conditions:** Fire, spill, loss of containment, loss of power
- **Maintenance conditions:** Isolation, draining, purging, entry
- **Environmental conditions:** Extreme temperatures, seismic events, high winds, flooding (Fraser River proximity)
- **Operating temperature range:** **TBD** — Canola oil handling temperature (typically near ambient to ~60°C for viscosity control)
- **Operating pressure range:** **TBD** — Typically atmospheric to low pressure (< 150 psig for transfer piping)
- **Product characteristics:** Combustible liquid (flash point ~300°C), food-grade, temperature-sensitive

**Source:** **ASSUMPTION**: Typical operating conditions for canola oil handling facility; **TBD** — Specific operating parameters from design basis (DEL-27.01)

**Hazardous Area Classification:**

- HAZOP study results inform hazardous area classification for electrical equipment
- Expected classifications (preliminary, to be confirmed by HAZOP):
  - **Zone 0/1:** Inside storage tanks, vapor space
  - **Zone 1:** Areas with potential for releases during normal operation (loading arms, pump seals, vent outlets)
  - **Zone 2:** Areas with potential for releases only under abnormal conditions (piping flanges, valve packing)
  - **Non-hazardous:** Areas with no potential for combustible atmosphere
- **TBD** — Detailed hazardous area classification drawings based on HAZOP findings
- **Source:** **ASSUMPTION**: Typical hazardous area classification for combustible liquid handling; coordination with electrical design (PKG-17)

## Construction

**Anticipated Artifacts:**

Per _CONTEXT.md and decomposition DEL-27.02 entry:
- **HAZOP Study Reports** — Comprehensive documentation of HAZOP study process, findings, and recommendations

**HAZOP Report Structure (typical):**

1. **Executive Summary**
   - Study objectives and scope
   - Key findings and high-priority recommendations
   - Summary of hazardous area classification results

2. **Introduction**
   - Project overview
   - HAZOP methodology (IEC 61882 or equivalent)
   - Study objectives

3. **Study Organization**
   - HAZOP team composition and qualifications
   - Study schedule and session dates
   - Node definition and boundaries

4. **Design Basis Review**
   - Process description
   - P&IDs (Piping and Instrumentation Diagrams) reviewed
   - Operating philosophy and design intent
   - Reference to DEL-27.01 (Design Basis Documents)

5. **HAZOP Worksheets**
   - Node-by-node analysis using guidewords (More, Less, No, Reverse, As Well As, Part Of, Other Than, etc.)
   - Deviations from design intent
   - Causes of deviations
   - Consequences (safety, environmental, operational, economic)
   - Existing safeguards
   - Risk ranking (likelihood × consequence)
   - Recommendations for risk reduction
   - Action items assigned with responsibility and target dates

6. **Hazardous Area Classification**
   - Methodology and standards (CEC, API RP 505, IEC 60079, etc.)
   - Source of release identification
   - Zone/division classification by area
   - Hazardous area classification drawings (as appendix or separate deliverable)

7. **Recommendations Summary**
   - All recommendations tabulated with priority, responsibility, target completion
   - Cross-reference to HAZOP worksheet node/deviation
   - Status tracking (for subsequent HAZOP review iterations)

8. **Action Item Tracking**
   - Action item register with owner, description, priority, status, closure evidence
   - Follow-up HAZOP review to verify action item closure

9. **Appendices**
   - HAZOP team qualifications
   - P&IDs (marked-up with HAZOP nodes)
   - Guideword definitions
   - Risk matrix (likelihood × consequence)
   - Reference documents

**Source:** **ASSUMPTION**: Standard HAZOP report structure per IEC 61882 and industry practice; **TBD** — Project-specific HAZOP report template

**HAZOP Study Timing:**

- **Preliminary HAZOP (30-60% design stage):** Identifies major hazards and informs design direction; P&IDs may be preliminary
- **Detailed HAZOP (90% design stage):** Comprehensive analysis of near-final P&IDs; generates final recommendations for design and operational safeguards
- **Pre-commissioning HAZOP review:** Verifies HAZOP action items closed and as-built conditions match HAZOP assumptions
- **Post-startup HAZOP review:** Captures lessons learned from commissioning and early operations (may be out of scope for DEL-27.02 if focused on design phase)

**Source:** **ASSUMPTION**: Multi-stage HAZOP approach aligned with design submission stages (DEL-27.04)

## References

**Primary References:**

- Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md (Sections 1.1, 2, 4, 6)
- _CONTEXT.md (DEL-27.02)
- DEL-27.01: Design Basis Documents (provides design intent, process description, operating philosophy)
- Employer's Requirements Volume 2 Part 1 (General Requirements) — **location TBD**
- Employer's Requirements Volume 2 Part 2 (Civil & Process Mechanical Works) — **location TBD**
- Employer's Requirements Volume 2 Part 3 (Building Works) — **location TBD**
- P&IDs (Piping and Instrumentation Diagrams) for all systems in HAZOP scope — **TBD** — To be developed by discipline engineering teams
- Process flow diagrams (PFDs) — **TBD**
- Equipment datasheets — **TBD**
- Operating procedures (preliminary or draft) — **TBD**

**Applicable Standards and Guidelines:**

- **HAZOP Methodology:**
  - IEC 61882: Hazard and operability studies (HAZOP studies) — Application guide — **location TBD**
  - CCPS (Center for Chemical Process Safety) Guidelines for Hazard Evaluation Procedures — **location TBD**
  - **TBD** — Project-specific HAZOP procedure or Employer's Requirements for HAZOP

- **Hazardous Area Classification:**
  - Canadian Electrical Code (CEC) Part I, Section 18: Hazardous locations — **location TBD**
  - API RP 505: Recommended Practice for Classification of Locations for Electrical Installations at Petroleum Facilities Classified as Class I, Zone 0, Zone 1, and Zone 2 — **location TBD**
  - IEC 60079 series: Explosive atmospheres — **location TBD**
  - **TBD** — Applicable BC or Canadian standards for hazardous area classification

- **Safety and Risk Management:**
  - ISO 31000: Risk management — Guidelines — **location TBD**
  - **TBD** — Employer's risk assessment and management requirements

- **Process Safety:**
  - **TBD** — Applicable CSA or other Canadian process safety standards
  - CCPS Guidelines — **location TBD**

**Cross-References:**

- DEL-27.01: Design Basis Documents (HAZOP uses design basis as foundation; HAZOP findings may trigger design basis updates)
- DEL-27.04: Design Submission Packages (HAZOP reports submitted as part of design packages at appropriate stages)
- DEL-28.01: Independent Design Verification Reports (IDV may review HAZOP study adequacy and recommendation implementation)
- PKG-10 through PKG-26 deliverables (HAZOP findings inform detailed design of all process systems)
- PKG-19: Control Systems (HAZOP identifies SIS requirements, interlocks, alarms)
- PKG-23, PKG-24: Fire Protection and Safety Systems (HAZOP identifies fire scenarios and safety system requirements)
- See `_DEPENDENCIES.md` (NOT_TRACKED — dependencies coordinated externally per _COORDINATION.md)

**Source:** Decomposition Section 3 (Reference Documents); **ASSUMPTION**: Standard HAZOP reference documents and industry guidelines; **location TBD** for all standards
