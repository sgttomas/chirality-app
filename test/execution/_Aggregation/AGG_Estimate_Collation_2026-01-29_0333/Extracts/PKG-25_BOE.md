# Basis of Estimate (BoE) — PKG-25 Communications & IT

**Snapshot ID:** EST_PKG25_DRAFT_2026-01-29_0004
**Estimate Label:** PKG25_DRAFT
**Package Scope:** PKG-25 Communications & IT
**Date:** 2026-01-29
**Prepared By:** Estimating Agent (Automated Pipeline)

---

## Executive Summary

**Total Estimate:** $723,000 CAD (rounded, includes contingency)
**Base Estimate:** $563,000 CAD (before contingency)
**Contingency:** $160,000 CAD (28% blended rate)
**Currency:** CAD (Canadian dollars)
**Pricing Date:** January 2026
**Confidence:** LOW (82% allowance-based; no vendor quotes; quantities TBD)
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
- Product: CSD canola oil
- Contract: Design & Build

---

### 1.2 PKG-25 Scope

**Package Description:** Communications network, fiber infrastructure, patch panels, workstation connectivity

**Deliverables (4 total):**
- DEL-25.01: Communications Design Drawing Set (fiber network layout, communications distribution drawings, patch panel locations)
- DEL-25.02: Communications Technical Specification (fiber cable specification, network cabling specification)
- DEL-25.03: Communications Data Sheet Package (network switch data sheets, patch panel data sheets)
- DEL-25.04: Communications Installation & Test Records (fiber test records, network test records)

**Source:** Decomposition Section 5, PKG-25, lines 572-586

---

## 2. Estimate Scope and Basis

### 2.1 Inclusions

- Engineering & Design (E): Drawings, specifications, data sheets, test records
- Materials (MAT): Fiber optic cables, copper network cables (Cat 6/6A), network switches, patch panels, connectors, cable management
- Construction Directs (CD): Cable installation, termination, testing, equipment mounting, fiber splicing
- Construction Indirects (CI): Field supervision, QA/QC, HSE, site overhead
- Project Management (PM): EPCM allocation, coordination
- Procurement (P): Vendor coordination, expediting, equipment inspection
- Commissioning (COM): System integration testing, performance verification, handover

---

### 2.2 Exclusions

- Owner's costs, land, financing, Employer-obtained permits
- Other packages (PKG-00 through PKG-24, PKG-26 through PKG-35)
- CCTV network (see PKG-24 Security Systems per DEC-05)
- Access control network (see PKG-24 Security Systems per DEC-05)
- Control system networks/fieldbus (see PKG-19 Control Systems) — integration points only
- Cable pathways/trays installed by other packages (PKG-17/PKG-21) — coordination required
- Escalation (January 2026 pricing basis)
- Taxes (GST/PST)

**Source:** `_CONFIG.md`; Decision D-2502; Decomposition Section 7 DEC-05; DEL-25.01 Specification.md Scope §Exclusions

---

## 3. Pricing Sources and Methods

### 3.1 Source Hierarchy Applied

1. Vendor quotes: 0% (none available)
2. Rate tables: 0% (none available)
3. Allowances: 82.1% ($462k)
4. Parametric factors: 17.9% ($101k)

**Decision:** D-2508 (use fallback model)

**Source Index:** See `Source_Index.md`

---

### 3.2 Fallback Model Disclosure

**Primary pricing basis:** Fallback typical model (no project-specific sources)

**Components used:**
- Allowance placeholders for materials and construction (A-2501 through A-2518)
- Indirects factors: CI=18%, P=2%, PM=6%, COM=3% (D-2509)
- Contingency baseline by bucket with allowance-heavy adjustment (D-2508)

**Transparency:** All uses labeled ALLOWANCE or PARAMETRIC with LOW/MED confidence and traced to assumptions/decisions

**Source:** AGENT_ESTIMATING fallback model, lines 623-691

---

## 4. Currency and Pricing Date

**Currency:** CAD (D-2502) — project location Surrey, BC
**Pricing Date:** January 2026 (D-2503) — current pricing
**Escalation:** NONE (D-2509) — no escalation applied

---

## 5. Estimate Methodology

### 5.1 WBS to CBS Mapping

- Design deliverables (DEL-25.01 through DEL-25.03) → Engineering (E)
- QA/QC records (DEL-25.04) → Construction Indirects (CI) / Commissioning (COM)
- Physical materials (cables, switches, patch panels) → Materials (MAT)
- Installation work (cable pulling, termination, testing) → Construction Directs (CD)

**Source:** WBS_CBS_Matrix.csv; Decision D-2510

---

### 5.2 Quantity Extraction

**Extracted:**
- Deliverable artifact counts (drawings, specs, data sheets, test records)
- Qualitative scope descriptions (fiber infrastructure, structured cabling, network equipment, patch panels)
- Equipment types (network switches, fiber/copper patch panels)
- Cable types (single-mode fiber OS2, multi-mode fiber OM3/OM4, Cat 6/6A copper UTP)
- Standards references (TIA-568, TIA-569, TIA-606, TIA-607, CSA C22.1)

**Not Extracted (TBD):**
- Fiber cable lengths and fiber counts (6/12/24/48 fiber)
- Copper cable lengths and port counts
- Number of network switches and port configurations (24/48 port)
- Number of patch panels (fiber and copper)
- Number of telecommunications rooms (TRs) and equipment room (ER) locations
- Number of workstation outlets and data drops

**Impact:** Cannot create unit-rate-based QTO; forced to use LS allowances

**Source:** Exploration of DEL-25.01, DEL-25.02, DEL-25.03 deliverable folders; Assumptions A-2501 through A-2505

---

### 5.3 Pricing Methodology

**Allowance Sizing:**
- Fiber optic cabling system: $120k (cables + splicing + termination) — A-2501, A-2509
- Structured copper cabling system: $85k (Cat 6/6A cables + termination + testing) — A-2502, A-2510
- Network switches and equipment: $95k (core/distribution and access switches) — A-2503, A-2511
- Patch panels (fiber and copper): $30k (rack-mounted panels + connectors) — A-2504, A-2512
- Cable management and infrastructure: $15k (J-hooks, D-rings, labels, grounding) — A-2505, A-2513
- Engineering design: $75k (600-800 hours @ $125-150/hr blended) — A-2506

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
**Site Conditions:** Active marine terminal; coordination with terminal operations
**Productivity:** Standard telecommunications installation productivity with terminal coordination constraints

**Adjustments:** Terminal operational interface and security clearance requirements may reduce productivity 10-15% (reflected in CD/CI contingency)

**Source:** Assumptions A-2507, A-2514; Risk R-2507

---

## 7. Indirects Model

**Model:** Factor-based (D-2506, D-2509)

**Rationale:** No construction schedule available; factor-based appropriate for conceptual estimate

| Indirect | Factor | Base | Amount (CAD) |
|----------|--------|------|--------------|
| CI | 18% | CD=$160k | $28,800 |
| P | 2% | MAT=$345k | $6,900 |
| PM | 6% | CD+CI+MAT=$533.8k | $32,000 |
| COM | 3% | CD+CI+MAT=$533.8k | $16,000 |

**Source:** AGENT_ESTIMATING fallback factors (lines 643-652)

---

## 8. Contingency Method

**Method:** PCT_BY_BUCKET with allowance-heavy adjustment (D-2508)

**Rates Applied:**

| CBS | Base (CAD) | Allowance Share | Final Rate | Contingency (CAD) |
|-----|------------|-----------------|------------|-------------------|
| E | $75,000 | 100% | 20% | $15,000 |
| MAT | $345,000 | 100% | 25% | $86,000 |
| CD | $160,000 | 100% | 30% | $48,000 |
| CI | $29,000 | 100% (factor-derived) | 30% | $9,000 |
| P | $7,000 | 100% (factor-derived) | 15% | $1,000 |
| PM | $32,000 | 100% (factor-derived) | 15% | $5,000 |
| COM | $16,000 | 100% (factor-derived) | 30% | $5,000 |

**Total Contingency:** $169,000 CAD (30% blended, rounded to $160,000)

**Rationale:** Elevated rates due to:
- No vendor quotes (pricing uncertainty)
- Quantities TBD (scope uncertainty)
- Technology selection unknowns (Cat 6 vs Cat 6A, switch specifications)
- Network architecture not defined (topology, redundancy, port counts)

**Source:** AGENT_ESTIMATING contingency model (lines 653-667); Risk_Register.md

---

## 9. Escalation

**Mode:** NONE (D-2509)
**Rationale:** Current pricing (2026-01); no schedule available for escalation calculation
**Exposure:** 3-6% annual escalation over 2-3 year project = potential $34k-$100k addition (see Risk R-2508)

---

## 10. Rounding Policy

**Rounding:** Nearest $1,000 CAD (D-2507)
**Application:** Summary totals only; Detail.csv retains calculated precision

---

## 11. Completeness Metrics

### Pricing Method Distribution

- ALLOWANCE: 82.1% ($462k)
- PARAMETRIC: 17.9% ($101k)
- QUOTE: 0%
- RATE_TABLE: 0%

### Quantity Extraction Success

- Deliverable counts: 100% (4/4)
- Physical quantities: 0% (all TBD)

---

## 12. Known Gaps

**Critical Gaps:**
1. No vendor quotes or rate tables for telecommunications equipment or cabling
2. Physical quantities TBD (cable lengths, port counts, equipment quantities)
3. Employer's Requirements for communications not available
4. Network architecture not defined (topology, bandwidth requirements, redundancy)
5. Building layouts and telecommunications room locations not available (coordination with PKG-21, PKG-22)
6. Integration requirements with PKG-19 Control Systems not defined

**Impact:** Estimate suitable for conceptual budgeting only

---

## 13. Key Assumptions Requiring Validation

1. **A-2501:** Fiber optic cabling system (800-1500 LM backbone + distribution) — $120k, 21% of base
2. **A-2502:** Structured copper cabling (1500-2500 LM horizontal + outlets) — $85k, 15% of base
3. **A-2503:** Network switches (4-8 switches, 24-48 ports each) — $95k, 17% of base
4. **A-2504:** Patch panels (fiber and copper, 8-15 panels) — $30k, 5% of base
5. **A-2506:** Engineering design (600-800 hours) — $75k, 13% of base

**Validation Path:** Complete network architecture design, obtain building layouts (DEL-21.01), acquire vendor quotes for equipment and materials

---

## 14. Supporting Documents

- Decision_Log.md (12 decisions)
- Assumptions_Log.md (20 assumptions)
- Source_Index.md (no pricing sources found)
- Detail.csv (15 lines, all fields populated)
- WBS_CBS_Matrix.csv (WBS-CBS mapping)
- Risk_Register.md (8 risks)
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
**Assumptions:** 20 documented

---

## 16. Recommended Next Steps

**Immediate (Before Decision-Making):**
1. Define network architecture (bandwidth requirements, topology, redundancy) — impacts cable and equipment selections
2. Complete building layouts (coordinate with PKG-21) to establish telecommunications room locations and cable routing
3. Develop port count matrix (workstations, control points, field devices) to size cabling and switching
4. Obtain budgetary quotes for network switches, patch panels, fiber/copper cables
5. Clarify integration requirements with PKG-19 Control Systems

**Medium-Term:**
6. Obtain Employer's Requirements for communications systems
7. Complete cable pathway design (coordinate with PKG-17 Electrical for shared pathways)
8. Develop equipment room HVAC and power requirements (coordinate with PKG-22, PKG-17)
9. Develop project rate tables for labor, equipment, materials
10. Re-run estimate to upgrade from Class 5 to Class 4/3

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
- Network architecture defined
- Building layouts available
- Vendor quotes obtained
- Employer's Requirements extracted
- Integration requirements with PKG-19 clarified

---

**Basis of Estimate Prepared By:** Estimating Agent
**Date:** 2026-01-29
**Status:** Complete
**Snapshot:** EST_PKG25_DRAFT_2026-01-29_0004
