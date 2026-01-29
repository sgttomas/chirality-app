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

| Attribute | Value | Specification § | Guidance § | Procedure Step |
|-----------|-------|-----------------|------------|----------------|
| Study Type | Hazard and Operability Study (HAZOP) | FR-1 | Principles §1 | Step 2.1 |
| Study Methodology | Structured HAZOP per IEC 61882 or equivalent — **TBD** | QR-1 | Principles §1, §2 | Step 1.4, Step 2.1 |
| Study Scope | All major process systems for Phase 1 canola oil transload facility | FR-1 | Considerations (HAZOP Scope) | Step 1.1 |
| Report Format | HAZOP worksheets with node descriptions, deviations, causes, consequences, safeguards, recommendations | QR-2, Documentation | Examples §1, §2 | Step 3.1 |
| Submission Stages | **TBD** — Align with design submission stages (30%, 60%, 90%, IFC per DEL-27.04) or as standalone milestone | QR-4 | Considerations (Timing) | Steps 4.2, 6.1 |
| HAZOP Team Composition | **TBD** — Multi-discipline team with facilitator, scribe, design leads, operations input | FR-2 | Principles §2 | Step 1.2 |

**Source:** _CONTEXT.md; **ASSUMPTION**: Standard HAZOP methodology per IEC 61882 or equivalent industry practice

## Conditions

**Project Context:**

| Parameter | Value | Source | Specification § | Guidance § |
|-----------|-------|--------|-----------------|------------|
| Facility Type | Canola oil transload facility (rail-to-ship) | Decomposition Section 1.1 | Scope | Purpose |
| Product | CSD (Crude Super Degummed) canola oil | Decomposition Section 1.1 | PR-3 | Considerations (Product) |
| Location | Fraser Surrey Terminal, 11060 Elevator Road, Surrey, BC | Decomposition Section 1.1 | PR-4 | Considerations (Location) |
| Permitted Throughput | 1,000,000 MT per annum | Decomposition Section 1.1 (OBJ-2) | PR-2 | Considerations (Operational) |
| Storage Capacity | 45,000 MT (3 × 15,000 MT tanks) | Decomposition Section 1.1 (OBJ-3) | PR-2 | Examples §2 |
| Railcar Capacity | 32 unloading stations on 2 tracks | Decomposition Section 1.1 | PR-2 | Examples §1 |
| Operating Modes | Tank storage operations and direct rail-to-ship transfer | Decomposition Section 2 (OBJ-4) | PR-2 | Considerations (Operational) |

**HAZOP Study Scope (Major Systems):**

Systems to be analyzed in HAZOP study (typical scope for canola oil transload facility):

| System | Package Reference | Key HAZOP Focus Areas | Specification § |
|--------|-------------------|----------------------|-----------------|
| Railcar Unloading System | PKG-10 | 32 stations, unloading pumps, piping, nitrogen, spill containment | PR-1, PR-2, IR-2 |
| Storage Tank System | PKG-13 | 3 × 15,000 MT tanks, heating/cooling, venting, overfill protection, containment | PR-1, PR-3, IR-2 |
| Transfer and Process Piping | PKG-14 | Main transfer piping, pump suction/discharge, relief and drainage | PR-1, IR-2 |
| Marine Loading System | PKG-11 | Loading arms, loading pumps, metering (PKG-12), ESD, vapor recovery | PR-1, PR-3, IR-2 |
| Pumps and Rotating Equipment | PKG-15 | Unloading, transfer, loading pumps, sealing systems | PR-1, IR-2 |
| Valves and Specialty Equipment | PKG-16 | Isolation, control, relief, ESD valves | PR-1, IR-2 |
| Electrical Power Distribution | PKG-17 | Power to motor-driven equipment, hazardous area classification, emergency power | FR-4, IR-4 |
| Control Systems | PKG-19 | DCS/PLC, SIS, ESD logic, alarms and interlocks | IR-3 |
| Fire Protection and Safety | PKG-23, PKG-24 | Fire detection/suppression, gas detection, emergency response | IR-5 |

**Source:** Decomposition Sections 1.1, 4 (Package Summary); **ASSUMPTION**: Typical HAZOP scope covers all major process systems

**Operating Conditions for HAZOP Analysis:**

| Condition Type | Description | Specification § | Guidance § |
|----------------|-------------|-----------------|------------|
| Normal operations | Steady-state railcar unloading, tank storage, marine loading at design rates | PR-2 | Principles §3 |
| Start-up and shutdown | System commissioning, planned shutdowns, restart after maintenance | PR-2 | Principles §9 |
| Upset conditions | Equipment failures, operator errors, instrument failures, utility outages | PR-1 | Principles §4, §5 |
| Emergency conditions | Fire, spill, loss of containment, loss of power | PR-1, PR-3 | Principles §7, §8 |
| Maintenance conditions | Isolation, draining, purging, entry | PR-2 | Principles §9 |
| Environmental conditions | Extreme temperatures, seismic events, high winds, flooding (Fraser River) | PR-4 | Considerations (Location) |

- Operating temperature range: **TBD** — Canola oil handling temperature (typically near ambient to ~60°C for viscosity control)
- Operating pressure range: **TBD** — Typically atmospheric to low pressure (< 150 psig for transfer piping)
- Product characteristics: Combustible liquid (flash point ~300°C), food-grade, temperature-sensitive

**Source:** **ASSUMPTION**: Typical operating conditions for canola oil handling facility; **TBD** — Specific operating parameters from design basis (DEL-27.01)

**Hazardous Area Classification:**

| Zone | Typical Locations | Classification Basis | Specification § | Guidance § |
|------|-------------------|---------------------|-----------------|------------|
| Zone 0/1 | Inside storage tanks, vapor space | Continuous/frequent release potential | FR-4, IR-4 | Principles §10, §11 |
| Zone 1 | Loading arms, pump seals, vent outlets | Normal operation releases | FR-4, IR-4 | Examples §3 |
| Zone 2 | Piping flanges, valve packing | Abnormal condition releases only | FR-4, IR-4 | Examples §3 |
| Non-hazardous | Areas with no combustible atmosphere potential | No credible release scenarios | FR-4, IR-4 | Principles §11 |

- **TBD** — Detailed hazardous area classification drawings based on HAZOP findings
- **Source:** **ASSUMPTION**: Typical hazardous area classification for combustible liquid handling; coordination with electrical design (PKG-17)

## Construction

**Anticipated Artifacts:**

Per _CONTEXT.md and decomposition DEL-27.02 entry:
- **HAZOP Study Reports** — Comprehensive documentation of HAZOP study process, findings, and recommendations (see Specification § Documentation; Guidance § Examples; Procedure Step 3.1)

**HAZOP Report Structure (typical):**

| Section | Content | Specification § | Guidance § | Procedure Step |
|---------|---------|-----------------|------------|----------------|
| Executive Summary | Objectives, key findings, high-priority recommendations, hazardous area summary | Documentation | — | Step 3.1 |
| Introduction | Project overview, methodology (IEC 61882), objectives | QR-1 | Principles §1 | Step 3.1 |
| Study Organization | Team composition/qualifications, schedule, node definitions | FR-2 | Principles §2 | Step 1.2, 1.4 |
| Design Basis Review | Process description, P&IDs, operating philosophy, reference to DEL-27.01 | FR-3, IR-1 | Principles §3 | Step 3.1 |
| HAZOP Worksheets | Node-by-node analysis with guidewords, deviations, causes, consequences, safeguards, risk ranking, recommendations | FR-1, FR-5 | Examples §1, §2 | Step 2.1 |
| Hazardous Area Classification | Methodology, source identification, zone classification, drawings | FR-4 | Principles §10, §11; Examples §3 | Step 2.2 |
| Recommendations Summary | Tabulated with priority, responsibility, target dates, cross-references | FR-6 | Examples §4 | Step 3.1 |
| Action Item Tracking | Register with owner, status, closure evidence | FR-6, VM-5 | Examples §4 | Steps 5.1-5.3 |
| Appendices | Team qualifications, P&IDs, guideword definitions, risk matrix, references | QR-2 | — | Step 3.1 |

**HAZOP Study Timing:**

| Stage | Design Maturity | Purpose | Specification § | Guidance § |
|-------|-----------------|---------|-----------------|------------|
| Preliminary HAZOP | 30-60% design | Identifies major hazards, informs design direction | QR-4 | Considerations (30-60% Stage) |
| Detailed HAZOP | 90% design | Comprehensive analysis of near-final P&IDs, final recommendations | QR-4 | Considerations (90% Stage) |
| Pre-commissioning review | As-built | Verifies action items closed, as-built matches HAZOP assumptions | QR-4 | Considerations (Pre-Commissioning) |
| Post-startup review | Post-startup | Captures lessons learned from commissioning/operations — **TBD** if in scope | QR-4 | Considerations (Post-Startup) |

**Source:** **ASSUMPTION**: Multi-stage HAZOP approach aligned with design submission stages (DEL-27.04)

## References

**Primary References:**

| Reference | Description | Status | Specification § |
|-----------|-------------|--------|-----------------|
| Decomposition | Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md (Sections 1.1, 2, 4, 6) | Available | All |
| _CONTEXT.md | DEL-27.02 deliverable context | Available | Scope |
| DEL-27.01 | Design Basis Documents — design intent, process description, operating philosophy | Required | FR-3, IR-1 |
| Employer's Requirements Vol 2 (all parts) | Project-specific requirements | **location TBD** | RC-2 |
| P&IDs | Piping and Instrumentation Diagrams for all systems | **TBD** — To be developed | FR-1, FR-3 |
| PFDs, equipment datasheets, operating procedures | Supporting design documents | **TBD** | FR-1, FR-3 |

**Applicable Standards and Guidelines:**

| Standard | Description | Status | Specification § |
|----------|-------------|--------|-----------------|
| IEC 61882 | HAZOP studies — Application guide | **location TBD** | QR-1, RC-3 |
| CCPS Guidelines | Hazard Evaluation Procedures | **location TBD** | QR-1, RC-3 |
| CEC Part I, Section 18 | Hazardous locations | **location TBD** | FR-4, RC-3 |
| API RP 505 | Hazardous area classification for petroleum facilities | **location TBD** | FR-4, RC-3 |
| IEC 60079 series | Explosive atmospheres | **location TBD** | FR-4, RC-3 |
| ISO 31000 | Risk management — Guidelines | **location TBD** | FR-5, RC-3 |
| IEC 61508/61511 | Functional safety (SIS design) | **location TBD** | IR-3 |

**Cross-References to Related Deliverables:**

| Deliverable | Relationship | Interface Type | Specification § |
|-------------|--------------|----------------|-----------------|
| DEL-27.01 | Design Basis Documents | HAZOP foundation; HAZOP may trigger updates | IR-1 |
| DEL-27.04 | Design Submission Packages | Submission timing and requirements | QR-4, RC-2 |
| DEL-28.01 | Independent Design Verification Reports | IDV may review HAZOP adequacy | IR-7, VM-6 |
| PKG-10 through PKG-26 | Detailed engineering deliverables | HAZOP recommendations inform design | IR-2 |
| PKG-19 | Control Systems | SIS requirements, interlocks, alarms | IR-3 |
| PKG-17 | Electrical Power Distribution | Hazardous area classification | IR-4 |
| PKG-23, PKG-24 | Fire Protection and Safety Systems | Fire scenarios, safety systems | IR-5 |
| _DEPENDENCIES.md | Dependency tracking | NOT_TRACKED — dependencies coordinated externally | — |

**Source:** Decomposition Section 3 (Reference Documents); **ASSUMPTION**: Standard HAZOP reference documents and industry guidelines; **location TBD** for all standards

---

**Cross-Document Verification (Pass 3):**
- Terminology verified consistent with Specification.md, Guidance.md, Procedure.md
- Project parameters (1,000,000 MT/annum, 45,000 MT storage, 3 × 15,000 MT tanks, 32 railcar stations) verified consistent across all documents
- HAZOP scope systems verified consistent with Specification § FR-1 and Guidance § Considerations
- Submission stages aligned with DEL-27.04 verified consistent across all documents
- Cross-references to DEL-27.01, DEL-27.04, DEL-28.01, PKG-10 through PKG-26 verified consistent across all documents
- Hazardous area classification methodology (CEC, API RP 505, IEC 60079) verified consistent across all documents
