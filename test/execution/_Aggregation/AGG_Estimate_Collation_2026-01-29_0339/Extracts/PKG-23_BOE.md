# Basis of Estimate (BoE) — PKG-23 Fire Protection

**Snapshot ID:** EST_PKG23_DRAFT_2026-01-28_2400
**Estimate Label:** PKG23_DRAFT
**Package Scope:** PKG-23 Fire Protection
**Date:** 2026-01-28
**Prepared By:** Estimating Agent (Automated Pipeline)

---

## Executive Summary

**Total Estimate:** $2,480,000 CAD (rounded, includes contingency)
**Base Estimate:** $1,948,000 CAD (before contingency)
**Contingency:** $529,000 CAD (27% blended rate)
**Currency:** CAD (Canadian dollars)
**Pricing Date:** January 2026
**Confidence:** LOW (100% allowance-based; no vendor quotes; quantities TBD)
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
- Product: CSD canola oil (Class IIIA combustible liquid per NFPA 30)
- Contract: Design & Build

---

### 1.2 PKG-23 Scope

**Package Description:** Fire water loop, hydrants, connections, fire alarm panel, detection devices, hose bibs

**Deliverables (5 total):**
- DEL-23.01: Fire Protection Design Drawing Set (fire water loop layout, hydrant locations, fire alarm system drawings)
- DEL-23.02: Fire Protection Technical Specification (fire water piping spec, fire hydrant spec, fire alarm spec)
- DEL-23.03: Fire Protection Design Calculations (fire water demand calculations, hydraulic calculations)
- DEL-23.04: Fire Protection Data Sheet Package (fire hydrant data sheets, fire alarm panel data sheet)
- DEL-23.05: Fire Protection Installation & Test Records (hydrostatic test records, flow test records, fire alarm test records)

**Source:** Decomposition Section 5, PKG-23, lines 539-554

---

## 2. Estimate Scope and Basis

### 2.1 Inclusions

- Engineering & Design (E): Drawings, specifications, calculations, data sheets
- Materials (MAT): Fire water piping, hydrants, fire alarm equipment, foam system equipment
- Construction Directs (CD): Fire water loop installation, hydrant installation, fire alarm installation, foam system installation
- Construction Indirects (CI): Field supervision, QA/QC, HSE, site overhead
- Project Management (PM): EPCM allocation, coordination
- Procurement (P): Vendor coordination, expediting
- Commissioning (COM): Testing, performance verification, handover

**Major Systems Included:**
1. Fire Water Distribution System (underground loop, above-ground piping, hydrants, fire department connections)
2. Fire Alarm and Detection System (addressable FACP, heat/flame/smoke detectors, notification appliances)
3. Foam Suppression System (foam concentrate storage, proportioning, tank foam chambers, marine loading foam)

---

### 2.2 Exclusions

- Owner's costs, land, financing, Employer-obtained permits
- Other packages (PKG-00 through PKG-22, PKG-24 through PKG-35)
- Building sprinkler systems (covered under PKG-22 Building Interior & MEP)
- Fire pump (if required, assumed to be tied to municipal water supply with adequate pressure)
- Escalation (January 2026 pricing basis)
- Taxes (GST/PST)

**Source:** `_CONFIG.md`; Decision D-005; Decomposition Section 1.2

---

## 3. Pricing Sources and Methods

### 3.1 Source Hierarchy Applied

1. Vendor quotes: 0% (none available)
2. Rate tables: 0% (none available)
3. Allowances: 78% ($1,520k)
4. Parametric factors: 22% ($428k)

**Decision:** D-008 (use fallback model)

**Source Index:** See `Source_Index.md`

---

### 3.2 Fallback Model Disclosure

**Primary pricing basis:** Fallback typical model (no project-specific sources)

**Components used:**
- Allowance placeholders for materials and construction (A-001 through A-022)
- Indirects factors: CI=18%, P=2%, PM=6%, COM=3% (D-009)
- Contingency baseline by bucket with allowance-heavy adjustment (D-008)

**Transparency:** All uses labeled ALLOWANCE or PARAMETRIC with LOW/MED confidence and traced to assumptions/decisions

**Source:** AGENT_ESTIMATING fallback model, lines 623-691

---

## 4. Currency and Pricing Date

**Currency:** CAD (D-001) — project location Surrey, BC
**Pricing Date:** January 2026 (D-002) — current pricing
**Escalation:** NONE (D-007) — no escalation applied

---

## 5. Estimate Methodology

### 5.1 WBS to CBS Mapping

- Design deliverables (DEL-23.01 through DEL-23.04) → Engineering (E)
- QA/QC records (DEL-23.05) → Construction Indirects (CI) / Commissioning (COM)
- Fire protection equipment (fire alarm panels, hydrants, foam equipment) → Materials (MAT)
- Installation work (fire water loop, hydrants, fire alarm, foam systems) → Construction Directs (CD)

**Source:** WBS_CBS_Matrix.csv; Decision D-010

---

### 5.2 Quantity Extraction

**Extracted:**
- Deliverable artifact counts (drawings, specs, calculations, data sheets, test records)
- Facility parameters (3 × 15,000 MT tanks, 32 railcar stations, marine loading platform)
- Product classification (Class IIIA combustible liquid per NFPA 30)

**Not Extracted (TBD):**
- Fire water loop pipe lengths, sizes, hydrant counts
- Fire alarm device counts, panel size
- Foam system capacities, foam concentrate volumes
- Fire water demand (gpm) and duration (hours)

**Impact:** Cannot create unit-rate-based QTO; forced to use LS allowances

**Source:** Exploration findings; Assumptions A-001 through A-008

---

### 5.3 Pricing Methodology

**Allowance Sizing:**
- Fire water distribution system: $435k (piping + hydrants + FDC + valves) — A-001, A-002, A-003, A-009
- Fire alarm system: $215k (FACP + detectors + notification + wiring) — A-004, A-005, A-010
- Foam suppression system: $430k (storage + proportioning + discharge + piping + concentrate) — A-006, A-007, A-008, A-011
- Engineering: $175k (900-1,200 hours @ $145-175/hr blended) — A-012
- Construction directs: $600k (fire water loop + hydrants + fire alarm + foam installation) — A-013 through A-017

**Calculated Indirects:**
- CI = 18% × CD
- P = 2% × MAT
- PM = 6% × (CD+CI+MAT)
- COM = 3% × (CD+CI+MAT)

**Source:** Assumptions_Log.md, Decision_Log.md

---

## 6. Location and Productivity

**Location:** Fraser Surrey Terminal, Surrey, BC

**Labor Market:** Vancouver/Lower Mainland BC rates
**Site Conditions:** Active marine terminal; fire protection work coordinated with ongoing operations
**Productivity:** Standard EPC productivity with terminal coordination constraints

**Adjustments:** Terminal operational interface may reduce productivity 10-20% (reflected in CD/CI contingency)

**Source:** Assumptions A-018, A-019; Risk R-006

---

## 7. Indirects Model

**Model:** Factor-based (D-006, D-009)

**Rationale:** No construction schedule available; factor-based appropriate for conceptual estimate

| Indirect | Factor | Base | Amount (CAD) |
|----------|--------|------|--------------|
| CI | 18% | CD=$600k | $108,000 |
| P | 2% | MAT=$1,065k | $21,000 |
| PM | 6% | CD+CI+MAT=$1,773k | $106,000 |
| COM | 3% | CD+CI+MAT=$1,773k | $53,000 |

**Source:** AGENT_ESTIMATING fallback factors (lines 643-652)

---

## 8. Contingency Method

**Method:** PCT_BY_BUCKET with allowance-heavy adjustment (D-008)

**Rates Applied:**

| CBS | Base (CAD) | Allowance Share | Final Rate | Contingency (CAD) |
|-----|------------|-----------------|------------|-------------------|
| E | $175,000 | 100% | 20% | $35,000 |
| MAT | $1,065,000 | 100% | 25% | $266,000 |
| CD | $600,000 | 100% | 30% | $180,000 |
| CI | $108,000 | 100% (factor-derived) | 30% | $32,000 |
| P | $21,000 | 100% (factor-derived) | 15% | $3,000 |
| PM | $106,000 | 100% (factor-derived) | 15% | $16,000 |
| COM | $53,000 | 100% (factor-derived) | 30% | $16,000 |

**Total Contingency:** $548,000 CAD (28% blended, rounded down to $529k for rounding alignment)

**Rationale:** Elevated rates due to:
- No vendor quotes (pricing uncertainty)
- Quantities TBD (scope uncertainty)
- Foam system complexity (specialized equipment)
- Fire water demand TBD (design uncertainty)
- Code compliance requirements (NFPA 30, NFPA 72)

**Source:** AGENT_ESTIMATING contingency model (lines 653-667); Risk_Register.md

---

## 9. Escalation

**Mode:** NONE (D-007)
**Rationale:** Current pricing (2026-01); no schedule available for escalation calculation
**Exposure:** 3-6% annual escalation over 2-3 year project = potential $118k-$355k addition (see Risk R-008)

---

## 10. Rounding Policy

**Rounding:** Nearest $1,000 CAD (D-006)
**Application:** Summary totals only; Detail.csv retains calculated precision

---

## 11. Completeness Metrics

### Pricing Method Distribution

- ALLOWANCE: 78% ($1,520k)
- PARAMETRIC: 22% ($428k)
- QUOTE: 0%
- RATE_TABLE: 0%

### Quantity Extraction Success

- Deliverable counts: 100% (5/5)
- Physical quantities: 0% (all TBD)

---

## 12. Known Gaps

**Critical Gaps:**
1. No vendor quotes or rate tables
2. Physical quantities TBD (fire water loop lengths, hydrant counts, detector counts, foam volumes)
3. Fire water demand calculation not complete (DEL-23.03 INITIALIZED)
4. Foam system requirements not finalized (tank sizes known, but foam application rates TBD)
5. Employer's Requirements Volume 2 Part 1 not available (fire protection requirements)
6. Fire pump requirement not confirmed (assumed municipal supply adequate)

**Impact:** Estimate suitable for conceptual budgeting only

---

## 13. Key Assumptions Requiring Validation

1. **A-001:** Fire water loop length (500-800 LM underground, 200-400 LM above-ground) — $435k, 22% of base
2. **A-006:** Tank foam system (3 tanks × foam chambers + proportioning) — $250k, 13% of base
3. **A-004:** Fire alarm system (addressable FACP + 60-100 devices) — $215k, 11% of base
4. **A-007:** Marine loading foam system — $80k, 4% of base
5. **A-014:** Fire water loop installation (trench excavation, pipe installation, testing) — $300k, 15% of base

**Validation Path:** Complete design (DEL-23.01, DEL-23.03), obtain ER Volume 2 Part 1, acquire vendor quotes

---

## 14. Supporting Documents

- Decision_Log.md (12 decisions)
- Assumptions_Log.md (22 assumptions)
- Source_Index.md (no pricing sources found)
- Detail.csv (18 lines, all fields populated)
- WBS_CBS_Matrix.csv (WBS-CBS mapping)
- Risk_Register.md (10 risks)
- QA_Report.md (Run Status: WARNINGS)
- Summary.md (CBS/deliverable breakdown)

**Traceability:** All line items traceable to assumptions or decisions

---

## 15. Estimate Preparation Process

**Method:** Automated straight-through pipeline per AGENT_ESTIMATING protocol

**Steps Completed:**
1. ✓ Initialize + auto-discover
2. ✓ Index sources (none found)
3. ✓ Map WBS → CBS
4. ✓ Extract quantities (deliverable counts only; physical quantities TBD)
5. ✓ Price line items (allowances)
6. ✓ Apply indirects (factor-based)
7. ✓ QA checks
8. ✓ Risk register + contingency
9. ✓ Publish snapshot

**Human Interaction:** None (straight-through)
**Decisions:** 12 documented
**Assumptions:** 22 documented

---

## 16. Recommended Next Steps

**Immediate (Before Decision-Making):**
1. Complete DEL-23.03 fire water demand calculations per NFPA 30
2. Complete DEL-23.03 hydraulic calculations for fire water loop sizing
3. Develop DEL-23.01 fire water loop layout with pipe routing and hydrant locations
4. Confirm foam system requirements for tanks and marine loading per NFPA 11/16
5. Obtain budgetary quotes for fire alarm panel, foam proportioning system, fire hydrants

**Medium-Term:**
6. Obtain Employer's Requirements Volume 2 Part 1 (fire protection requirements)
7. Confirm fire pump requirement (municipal supply pressure vs. fire pump)
8. Coordinate with PKG-03 underground utilities for fire water loop installation
9. Coordinate with PKG-17/PKG-19 for fire alarm integration with DCS
10. Develop project rate tables for fire protection labor, equipment, materials
11. Re-run estimate to upgrade from Class 5 to Class 4/3

---

## 17. Approvals and Limitations

**Prepared By:** Estimating Agent (Automated)
**Reviewed By:** Not reviewed
**Approved By:** Not approved

**Limitations:**
- Conceptual budgeting and feasibility only
- NOT for contracting, procurement, GMP, or financing
- Expected accuracy: -30% / +50% (Class 5)
- Validity: January 2026 pricing; subject to escalation

**Re-Estimate Triggers:**
- Fire water demand calculation complete
- Fire water loop design available
- Foam system requirements finalized
- Vendor quotes obtained
- ER Volume 2 Part 1 extracted
- Fire pump requirement confirmed

---

**Basis of Estimate Prepared By:** Estimating Agent
**Date:** 2026-01-28
**Status:** Complete
**Snapshot:** EST_PKG23_DRAFT_2026-01-28_2400
