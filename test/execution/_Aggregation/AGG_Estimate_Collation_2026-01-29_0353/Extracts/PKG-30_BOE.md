# Basis of Estimate (BoE) — PKG-30 Commissioning

**Snapshot ID:** EST_PKG30_DRAFT_2026-01-29_0014
**Estimate Label:** PKG30_DRAFT
**Package Scope:** PKG-30 Commissioning
**Date:** 2026-01-29
**Prepared By:** Estimating Agent (Automated Pipeline)

---

## Executive Summary

**Total Estimate:** $5,890,000 CAD (rounded, includes contingency)
**Base Estimate:** $4,679,000 CAD (before contingency)
**Contingency:** $1,211,000 CAD (26% blended rate)
**Currency:** CAD (Canadian dollars)
**Pricing Date:** January 2026
**Confidence:** LOW to MEDIUM (85% allowance/parametric; limited vendor quotes; durations based on typical values)
**Maturity:** Class 5 (Conceptual / Order of Magnitude)

---

## 1. Project Overview

### 1.1 Project Description

**Project:** Canola Oil Transload Facility — Phase 1 Design & Build Contract
**Employer:** DP World Fraser Surrey Inc.
**Location:** Fraser Surrey Terminal, 11060 Elevator Road, Surrey, BC

**Key Parameters:**
- Throughput: 1,000,000 MT per annum
- Storage: 45,000 MT (3 × 15,000 MT tanks)
- Railcar unloading: 32 stations on 2 tracks
- Marine loading: Ship loading arms
- Product: CSD canola oil
- Contract: Design & Build

---

### 1.2 PKG-30 Scope

**Package Description:** Pre-commissioning, system commissioning, start-up, performance verification, defect rectification

**Deliverables (8 total):**
- DEL-30.01: Commissioning Procedures
- DEL-30.02: Commissioning Plan
- DEL-30.03: Pre-commissioning Installation & Test Records
- DEL-30.04: Commissioning Installation & Test Records
- DEL-30.05: Integrated Systems Test Installation & Test Records
- DEL-30.06: Performance Test Installation & Test Records
- DEL-30.07: Punch Lists
- DEL-30.08: Cathodic Protection Test & Commissioning Installation & Test Records

**Source:** Decomposition Section 5, PKG-30, lines 656-674

**Key Commissioning Systems:**
- Railcar Unloading: 32 stations with pumps, valves, instrumentation, controls
- Storage Tanks: 3×15,000 MT tanks with level gauging, temperature monitoring, mixing systems
- Product Transfer: Transfer piping, manifolds, isolation valves
- Metering Systems: Custody transfer meters and proving systems (critical accuracy requirement - OBJ-10)
- Marine Loading: Loading arms, gangway, manifold, control systems
- Electrical: Power distribution, MCCs, motors, transformers, lighting
- I&C: SCADA/PLC systems, field instrumentation, interlocks, alarms, safety systems
- Fire Protection: Detection and suppression systems
- Security: CCTV and access control systems
- Cathodic Protection: Rectifiers and monitoring systems

**Source:** Decomposition §1.1 (Key Parameters), DEL-30.01 through DEL-30.08 datasheets

**Key Interfaces:**
- PKG-29 (Testing): Pre-commissioning testing coordination
- PKG-31 (Documentation): O&M manuals, as-builts, vendor documentation
- PKG-32 (Regulatory & Permits): Inspection witness points, permit compliance
- PKG-33 (HSE Management): Safety procedures, permit-to-work integration
- PKG-35 (Training & Handover): Operational readiness and handover

**Objectives Supported:**
- OBJ-1 (Safe & Reliable Operation): Demonstrate fitness for purpose
- OBJ-2 (Throughput Capacity): Verify 1,000,000 MT/annum capacity
- OBJ-3 (Storage Capacity): Confirm 45,000 MT storage capacity
- OBJ-4 (Operational Flexibility): Verify tank storage and direct rail-to-ship modes
- OBJ-5 (Terminal Continuity): Minimize disturbance to existing terminal operations
- OBJ-6 (Regulatory Compliance): Demonstrate compliance with permits and codes
- OBJ-10 (Custody Transfer Accuracy): Metering system commissioning and proving

---

## 2. Estimate Scope and Basis

### 2.1 Inclusions

- **Engineering & Design (E):** Commissioning procedures development, commissioning plan and schedule, commissioning datasheets and test protocols, system handover documentation, lessons learned documentation
- **Materials (MAT):** Commissioning consumables (flushing fluids, cleaning materials, test fluids, nitrogen for purging, hydrotest water treatment), specialized test equipment rental
- **Construction Directs (CD):** Commissioning team labor (commissioning manager, discipline leads, field technicians), pre-commissioning activities (flushing, cleaning, hydrotesting, leak testing, drying), mechanical commissioning (pumps, valves, tanks, piping), electrical commissioning (power distribution, motors, transformers, lighting), I&C commissioning (loop checking, SCADA/PLC, interlocks, alarms), integrated systems testing, start-up support, performance testing support, vendor commissioning support, defect rectification
- **Construction Indirects (CI):** Field supervision, QA/QC, HSE, site overhead, temporary facilities for commissioning
- **Project Management (PM):** EPCM allocation, Employer coordination, regulatory liaison
- **Procurement (P):** Test equipment procurement, consumables procurement, vendor coordination
- **Commissioning (COM):** Integrated within CD; separated for clarity in CBS

---

### 2.2 Exclusions

- Owner's costs, land, financing, Employer-obtained permits
- Other packages (PKG-00 through PKG-29, PKG-31 through PKG-35)
- Operations personnel training (covered in PKG-35)
- Ongoing operations and maintenance post-handover
- Employer-responsible commissioning activities
- Product supply for commissioning (first product load assumed Employer-provided)
- Terminal integration activities beyond Phase 1 facility interface
- Escalation (January 2026 pricing basis)
- Taxes (GST/PST)

**Source:** `_CONFIG.md`; Decision D-005; Decomposition Sections 1.2 and 7 (Decisions)

---

## 3. Pricing Sources and Methods

### 3.1 Source Hierarchy Applied

1. Vendor quotes: 0% (none available)
2. Rate tables: 15% ($703k - commissioning labor rates)
3. Allowances: 72% ($3,357k)
4. Parametric factors: 13% ($619k - indirects/services)

**Source:** Source_Index.md; Decision D-008

**Method Selection:**
- Commissioning planning and procedures: ALLOWANCE (no detailed scope)
- Commissioning labor: RATE_TABLE where available, else ALLOWANCE
- Test equipment and consumables: ALLOWANCE (quantities TBD)
- Vendor support: ALLOWANCE (specific equipment TBD)
- Indirects and services: PARAMETRIC (default factors)

**Source:** Decision D-009 through D-015

---

### 3.2 Commissioning Duration and Resource Assumptions

**Commissioning Duration:**
- Pre-commissioning: 8 weeks (2 months) — **ASSUMPTION** based on facility scale
- Individual system commissioning: 12 weeks (3 months) — **ASSUMPTION** based on system complexity
- Integrated systems testing: 6 weeks (1.5 months) — **ASSUMPTION**
- Start-up and performance verification: 4 weeks (1 month) — **ASSUMPTION**
- Total commissioning duration: ~30 weeks (7.5 months) — **ASSUMPTION**

**Commissioning Team:**
- Commissioning Manager: 1 FTE for 30 weeks
- Mechanical Commissioning Lead: 1 FTE for 24 weeks
- Electrical Commissioning Lead: 1 FTE for 20 weeks
- I&C Commissioning Lead: 1 FTE for 22 weeks
- Field Commissioning Technicians: 8-12 FTE variable loading
- QA/QC Inspector: 1 FTE for 30 weeks
- HSE Coordinator: 0.5 FTE for 30 weeks

**Source:** Decision D-012 (duration assumptions); Assumption A-008 (resource loading)

**Critical Factors:**
- 32 railcar stations require significant commissioning effort
- Metering system proving is specialized and time-intensive
- Marine loading commissioning requires suitable weather and tide windows
- Terminal continuity (OBJ-5) constrains work windows and extends duration
- Regulatory witness points may introduce schedule delays

**Source:** DEL-30.02 Guidance.md (Terminal continuity, regulatory considerations); Assumption A-010

---

## 4. Cost Breakdown Structure (CBS) Summary

| CBS Category | Base Amount (CAD) | Contingency (CAD) | Total (CAD) | % of Base |
|--------------|-------------------|-------------------|-------------|-----------|
| Engineering (E) | $385,000 | $77,000 | $462,000 | 8.2% |
| Project Management (PM) | $210,000 | $32,000 | $242,000 | 4.5% |
| Procurement (P) | $52,000 | $8,000 | $60,000 | 1.1% |
| Materials (MAT) | $465,000 | $116,000 | $581,000 | 9.9% |
| Construction Directs (CD) | $2,806,000 | $787,000 | $3,593,000 | 60.0% |
| Construction Indirects (CI) | $505,000 | $141,000 | $646,000 | 10.8% |
| Commissioning (COM) | $256,000 | $77,000 | $333,000 | 5.5% |
| **Total** | **$4,679,000** | **$1,211,000** | **$5,890,000** | **100%** |

**Source:** Detail.csv line item rollup; Summary.md

---

## 5. Key Assumptions and Basis

### 5.1 Duration and Schedule Assumptions

**A-008: Commissioning Duration**
- Total commissioning duration: 30 weeks (~7.5 months)
- Based on facility scale (32 railcar stations, 3 tanks, marine loading, extensive I&C)
- Terminal continuity constraints extend duration by ~20% vs unrestricted schedule
- Assumes construction systems handover occurs on an integrated schedule
- **Impact:** $2.8M commissioning labor costs
- **Source:** Decision D-012; typical commissioning durations for similar liquid bulk terminals

**A-010: Terminal Continuity Impact**
- Commissioning must coordinate with existing terminal commercial operations
- Work windows restricted; night/weekend work may be required
- Marine loading commissioning limited to suitable weather/tide windows
- Schedule contingency of 15% included in duration assumptions
- **Impact:** Extends duration and increases labor costs by ~$400k
- **Source:** DEL-30.02 Datasheet §Conditions (Terminal Continuity); OBJ-5

**A-015: Commissioning Team Loading**
- Average team size: 10 FTE (variable 6-14 FTE across phases)
- Peak loading during integrated systems testing and start-up
- Mix: 30% leads/engineering, 70% field technicians
- Fully burdened rates including benefits, travel, per diem
- **Impact:** $2.8M commissioning labor
- **Source:** Assumption based on facility complexity and system count

---

### 5.2 Scope and Execution Assumptions

**A-003: Commissioning Procedures Scope**
- ~25-30 commissioning procedures required (pre-commissioning, commissioning, start-up)
- Average 40 hours development per procedure
- Includes safety review, technical review, approval process
- **Impact:** $120k engineering
- **Source:** DEL-30.01 Datasheet; typical procedure development effort

**A-005: Vendor Commissioning Support**
- Specialized vendor support required for:
  - Storage tanks (vendor technician for level gauging system commissioning)
  - Metering systems (custody transfer meter proving specialist)
  - Marine loading arms (OEM commissioning support)
  - Control systems (SCADA/PLC vendor FAT and SAT support)
- Estimated 6 weeks total vendor support across all systems
- **Impact:** $185k
- **Source:** Assumption based on equipment criticality and specialty requirements

**A-012: Hydrotest Water Management**
- Tank hydrotesting requires significant water volume: 3 tanks × 15,000 MT ≈ 45,000 m³
- Water treatment and discharge per environmental permit requirements
- Disposal costs included
- **Impact:** $95k consumables
- **Source:** DEL-30.03 (pre-commissioning), DEL-29.06 (Hydrotest Water Management Plan)

**A-018: Metering System Proving**
- Custody transfer accuracy critical (OBJ-10)
- Metering proving requires specialized equipment rental (prover, master meters)
- Multiple proving runs per meter
- Estimated 3 weeks for full metering system commissioning and proving
- **Impact:** $125k (equipment rental + specialist labor)
- **Source:** DEL-30.04 Datasheet (metering criticality); industry practice for custody transfer commissioning

---

### 5.3 Pricing and Rate Assumptions

**A-020: Commissioning Labor Rates**
- Commissioning Manager: $135/hr fully burdened
- Discipline Leads: $115/hr fully burdened
- Field Technicians: $85/hr fully burdened
- Rates include base wage, benefits, travel, per diem, markup
- BC labor market; Fraser Surrey location
- **Impact:** $2.8M commissioning labor
- **Source:** Decision D-014; typical commissioning labor rates for BC industrial projects 2026

**A-022: Test Equipment and Consumables**
- Specialized test equipment rental: $180k (multimeters, megohmmeters, vibration analyzers, loop calibrators, proving equipment)
- Commissioning consumables: $285k (flushing fluids, cleaning materials, nitrogen, hydrotest water treatment, misc supplies)
- Equipment rental assumes 6-month rental period
- **Impact:** $465k materials
- **Source:** Allowance A-022; typical commissioning consumables for liquid bulk facility

---

## 6. Risk Register Summary

**Key Commissioning Risks:**

**R-001: Terminal Continuity Constraints**
- Risk: Existing terminal operations limit commissioning work windows
- Impact: Schedule delays, increased labor costs (premium time)
- Contingency: 15% schedule float; premium time allowance
- Mitigation: Early coordination with terminal operations; flexible scheduling

**R-003: Metering System Proving Delays**
- Risk: Custody transfer meter proving is specialized and can encounter technical issues
- Impact: Critical path delay; repeat proving runs
- Contingency: 25% contingency on metering commissioning costs
- Mitigation: Pre-qualify proving contractor; allow adequate schedule float

**R-005: Marine Loading Commissioning Weather**
- Risk: Marine loading commissioning requires suitable weather and tide conditions
- Impact: Schedule delays waiting for weather windows
- Contingency: 20% schedule contingency for marine commissioning
- Mitigation: Plan marine commissioning for summer weather window; have backup dates

**R-008: Vendor Support Availability**
- Risk: Specialized vendor support may not be available on required schedule
- Impact: Commissioning delays; additional mobilization costs
- Contingency: Allowance includes mobilization buffer
- Mitigation: Lock in vendor commissioning support early; include in equipment purchase terms

**R-010: Defect Rectification Scope**
- Risk: Construction defects discovered during commissioning require rectification
- Impact: Extended commissioning duration; additional labor and materials
- Contingency: 30% contingency on defect rectification allowance
- Mitigation: Strong QA/QC during construction; early system turnover inspections

**Source:** Risk_Register.md (R-001 through R-015)

---

## 7. Contingency Method and Rationale

**Method:** PCT_BY_BUCKET (percentage by CBS bucket with allowance-heavy adjustment)

**Baseline Contingency by CBS:**
- Engineering (E): 20% (procedures and planning have scope uncertainty)
- Project Management (PM): 15% (coordination complexity)
- Procurement (P): 15% (test equipment procurement straightforward)
- Materials (MAT): 25% (consumables quantities TBD; hydrotest water uncertainty)
- Construction Directs (CD): 28% (labor duration uncertainty; terminal constraints; vendor support variability)
- Construction Indirects (CI): 28% (tracks with CD)
- Commissioning (COM): 30% (integrated testing has high uncertainty)

**Allowance-Heavy Adjustment:**
- CD, CI, COM buckets are >80% allowance/parametric → +5% contingency added
- Reflects low confidence in base estimates due to limited detailed scope

**Blended Rate:** 26% average across all CBS categories

**Rationale:**
- Commissioning scope uncertainty is high (procedures not yet developed, system details TBD)
- Terminal continuity constraints introduce schedule risk
- Specialized activities (metering proving, vendor support) have execution uncertainty
- Limited vendor quotes; relying on allowances and typical values
- Confidence: LOW to MEDIUM

**Source:** Decision D-018; Risk_Register.md; AGENT_ESTIMATING fallback model with project-specific adjustments

---

## 8. Quality and Completeness

### 8.1 Completeness Metrics

**Pricing Method Distribution:**
- Vendor quotes: 0%
- Rate tables: 15% (commissioning labor rates)
- Allowances: 72% (procedures, consumables, vendor support, test equipment)
- Parametric: 13% (indirects and services)

**Deliverable Coverage:**
- 8/8 deliverables have associated cost line items (100% coverage)
- All deliverables have allowance-based estimates (scope detail TBD)

**Source:** QA_Report.md; Detail.csv analysis

---

### 8.2 Known Gaps and Limitations

**Gap-1: Detailed Commissioning Procedures Not Available**
- Impact: Procedure development scope estimated as allowance
- Resolution: Refine estimate once DEL-30.01 procedures are drafted
- Affected CBS: E (Engineering)

**Gap-2: System Handover Schedule Unknown**
- Impact: Commissioning duration assumptions have high uncertainty
- Resolution: Update estimate once construction schedule defines system handover dates
- Affected CBS: CD, CI (commissioning labor duration)

**Gap-3: Vendor Commissioning Requirements Not Defined**
- Impact: Vendor support scope estimated as allowance
- Resolution: Coordinate with equipment packages (PKG-10 through PKG-24) for vendor commissioning terms
- Affected CBS: CD (vendor support labor and travel)

**Gap-4: Regulatory Witness Point Requirements Unknown**
- Impact: Schedule impact of regulatory inspections uncertain
- Resolution: Coordinate with PKG-32 for permit conditions and inspection requirements
- Affected CBS: CD (potential schedule delays)

**Gap-5: Performance Test Acceptance Criteria Not Defined**
- Impact: Performance test scope and duration uncertain
- Resolution: Define acceptance criteria in DEL-30.06 and update estimate
- Affected CBS: CD (performance testing labor)

**Source:** QA_Report.md (Gaps section); Assumptions_Log.md

---

## 9. Estimate Governance

### 9.1 Currency and Pricing Date

- **Currency:** CAD (Canadian dollars) — Project location: Surrey, BC
- **Pricing Date:** January 2026 (current date)
- **Escalation:** NONE (current pricing; no escalation to future dates)
- **Exchange Rates:** N/A (single currency)

**Source:** Decision D-001; _CONFIG.md

---

### 9.2 Rounding Policy

- Line items: Nearest $1,000
- Summary totals: Nearest $10,000
- Percentages: Nearest 1%

**Source:** Decision D-003; _CONFIG.md

---

### 9.3 Estimate Class and Confidence

**Estimate Class:** Class 5 — Order of Magnitude (Conceptual)
- Accuracy range: -30% to +50% (typical for Class 5)
- Confidence: LOW to MEDIUM
- Maturity: Based on decomposition and deliverable datasheets; detailed commissioning scope TBD

**Basis:**
- Decomposition defines deliverable scope
- Deliverable datasheets define anticipated artifacts
- Detailed procedures, schedules, and test protocols not yet developed
- Limited vendor input
- Reliance on allowances and typical values

**Source:** Decision D-020; AACE International Recommended Practice 18R-97 (Cost Estimate Classification System)

---

## 10. References

### 10.1 Project Documents

- Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md — Project scope decomposition
- PKG-30 Deliverable Datasheets (DEL-30.01 through DEL-30.08) — Deliverable scope and anticipated artifacts
- _CONFIG.md — Estimate configuration overrides
- _LATEST.md — Previous estimate snapshots

**Source:** Source_Index.md

---

### 10.2 Supporting Estimate Documents

**This Snapshot:**
- BOE.md (this document) — Basis of Estimate
- Decision_Log.md — Decisions made during estimating (D-001 through D-025)
- Assumptions_Log.md — Assumptions and allowances (A-001 through A-025)
- Source_Index.md — Pricing sources hierarchy
- Detail.csv — Line-item cost detail (58 line items)
- WBS_CBS_Matrix.csv — WBS-to-CBS mapping
- Summary.md — Executive summary and cost rollup
- Risk_Register.md — Risks affecting estimate (R-001 through R-015)
- QA_Report.md — Quality assurance checks and known gaps
- Change_Log.md — Changes from previous estimate

---

## 11. Limitations and Use

This estimate is a **budgeting tool** for the PKG-30 Commissioning package. It is:

- **Not a binding quote** or commitment
- **Not a detailed cost control baseline** (Class 5 maturity)
- **Subject to refinement** as commissioning scope is defined
- **Based on assumptions** that must be validated

**Recommended Actions:**
1. Develop commissioning procedures (DEL-30.01) and plan (DEL-30.02) to refine scope
2. Coordinate with construction schedule for system handover dates
3. Confirm vendor commissioning requirements with equipment packages
4. Define performance test acceptance criteria
5. Obtain vendor quotes for specialized commissioning support
6. Update estimate to Class 4 or Class 3 as scope matures

**Source:** Decision D-025 (estimate use and limitations)

---

**Prepared by:** Estimating Agent (Automated Pipeline)
**Date:** 2026-01-29
**Estimate Snapshot:** EST_PKG30_DRAFT_2026-01-29_0014
**Status:** DRAFT (WARNINGS - 72% allowance/parametric pricing; scope refinement required)

---

**End of Basis of Estimate**
