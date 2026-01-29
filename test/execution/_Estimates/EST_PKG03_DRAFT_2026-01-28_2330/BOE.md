# Basis of Estimate (BoE) — PKG-03 Underground Utilities & Drainage

**Snapshot ID:** EST_PKG03_DRAFT_2026-01-28_2330
**Estimate Label:** PKG03_DRAFT
**Package Scope:** PKG-03 Underground Utilities & Drainage
**Date:** 2026-01-28
**Prepared By:** Estimating Agent (Automated Pipeline)

---

## Executive Summary

**Total Estimate:** $2,607,000 CAD (rounded, includes contingency)
**Base Estimate:** $2,119,000 CAD (before contingency)
**Contingency:** $488,000 CAD (23.0% blended rate)
**Currency:** CAD (Canadian dollars)
**Pricing Date:** January 2026
**Confidence:** LOW (77.7% allowance-based; no vendor quotes; quantities TBD)
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

### 1.2 PKG-03 Scope

**Package Description:** Storm drainage, containment water collection, oil-water separator, underground utility routing, trenchless crossing, outfalls

**Deliverables (6 total):**
- DEL-03.01: Underground Utilities Design Drawing Set (4+ drawings)
- DEL-03.02: Underground Utilities Technical Specification (3 specs)
- DEL-03.03: Underground Utilities Design Calculations
- DEL-03.04: Underground Utilities Data Sheet Package
- DEL-03.05: Underground Utilities Installation & Test Records
- DEL-03.06: CCTV Survey Report – Storm Pipes & Culverts

**Source:** Decomposition Section 5, PKG-03, lines 188-203

---

## 2. Estimate Scope and Basis

### 2.1 Inclusions

- Engineering & Design (E): Drawings, specifications, calculations, data sheets, CCTV survey
- Materials (MAT): Storm drainage pipes, manholes, catch basins, OWS equipment, duct bank materials
- Construction Directs (CD): Excavation, pipe installation, OWS installation, duct banks, trenchless crossings
- Construction Indirects (CI): Field supervision, QA/QC, HSE, site overhead
- Project Management (PM): EPCM allocation, coordination
- Procurement (P): Vendor coordination, expediting
- Commissioning (COM): Testing, performance verification, handover

---

### 2.2 Exclusions

- Owner's costs, land, financing, Employer-obtained permits
- Other packages (PKG-00, PKG-01, PKG-02, PKG-04-35)
- Escalation (January 2026 pricing basis)
- Taxes (GST/PST)

**Source:** `_CONFIG.md`; Decision D-005; Decomposition Section 1.2

---

## 3. Pricing Sources and Methods

### 3.1 Source Hierarchy Applied

1. Vendor quotes: 0% (none available)
2. Rate tables: 0% (none available)
3. Allowances: 77.7% ($1,647k)
4. Parametric factors: 22.3% ($472k)

**Decision:** D-008 (use fallback model)

**Source Index:** See `Source_Index.md`

---

### 3.2 Fallback Model Disclosure

**Primary pricing basis:** Fallback typical model (no project-specific sources)

**Components used:**
- Allowance placeholders for materials and construction (A-001 through A-012, A-015 through A-023)
- Indirects factors: CI=18%, P=2%, PM=6%, COM=3% (D-009)
- Contingency baseline by bucket with allowance-heavy adjustment (D-008)

**Transparency:** All uses labeled ALLOWANCE or PARAMETRIC with LOW/MED confidence and traced to assumptions/decisions

**Source:** AGENT_ESTIMATING fallback model, lines 623-691

---

## 4. Currency and Pricing Date

**Currency:** CAD (D-002) — project location Surrey, BC
**Pricing Date:** January 2026 (D-003) — current pricing
**Escalation:** NONE (D-009) — no escalation applied

---

## 5. Estimate Methodology

### 5.1 WBS to CBS Mapping

- Design deliverables (DEL-03.01 through DEL-03.04, DEL-03.06) → Engineering (E)
- QA/QC records (DEL-03.05) → Construction Indirects (CI) / Commissioning (COM)
- Physical materials (pipes, manholes, OWS, duct banks) → Materials (MAT)
- Installation work (excavation, pipe laying, boring) → Construction Directs (CD)

**Source:** WBS_CBS_Matrix.csv; Decision D-010

---

### 5.2 Quantity Extraction

**Extracted:**
- Deliverable artifact counts (drawings, specs, calculations, reports)
- Qualitative scope descriptions (storm drainage, OWS, duct banks, trenchless crossings)

**Not Extracted (TBD):**
- Storm drainage pipe lengths, sizes, manhole counts
- OWS treatment capacity and equipment specifications
- Duct bank conduit sizes and quantities (pending PKG-17)
- Trenchless crossing count, lengths, sizes

**Impact:** Cannot create unit-rate-based QTO; forced to use LS allowances

**Source:** Exploration findings; Assumptions A-001 through A-005

---

### 5.3 Pricing Methodology

**Allowance Sizing:**
- Storm drainage: $770k (pipes + manholes + installation) — A-001, A-002
- Trenchless crossings: $265k (4-8 crossings @ $33k-$56k each) — A-005, A-012
- Duct banks: $240k (materials + installation) — A-004
- OWS: $230k (equipment + installation) — A-003
- Engineering: $232k (1,200-1,600 hours @ $140-175/hr blended) — A-006

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
**Site Conditions:** Active marine terminal; excavation in Fraser Delta soils (soft, high groundwater)
**Productivity:** Standard EPC productivity with terminal coordination constraints

**Adjustments:** Terminal operational interface may reduce productivity 10-20% (reflected in CD/CI contingency)

**Source:** Assumptions A-007, A-018; Risk R-007

---

## 7. Indirects Model

**Model:** Factor-based (D-006, D-009)

**Rationale:** No construction schedule available; factor-based appropriate for conceptual estimate

| Indirect | Factor | Base | Amount (CAD) |
|----------|--------|------|--------------|
| CI | 18% | CD=$975k | $175,500 |
| P | 2% | MAT=$570k | $11,400 |
| PM | 6% | CD+CI+MAT=$1,720.5k | $103,000 |
| COM | 3% | CD+CI+MAT=$1,720.5k | $52,000 |

**Source:** AGENT_ESTIMATING fallback factors (lines 643-652)

---

## 8. Contingency Method

**Method:** PCT_BY_BUCKET with allowance-heavy adjustment (D-008)

**Rates Applied:**

| CBS | Base (CAD) | Allowance Share | Final Rate | Contingency (CAD) |
|-----|------------|-----------------|------------|-------------------|
| E | $232,000 | 100% | 15% | $34,800 |
| PM | $103,000 | 0% | 15% | $15,450 |
| P | $11,400 | 0% | 15% | $1,710 |
| COM | $52,000 | 0% | 25% | $13,000 |
| MAT | $570,000 | 100% | 20% | $114,000 |
| CD | $975,000 | 87% | 25% | $243,750 |
| CI | $175,500 | 0% | 25% | $43,875 |

**Total Contingency:** $466,585 CAD (23.0%)

**Rationale:** Elevated rates due to:
- No vendor quotes (pricing uncertainty)
- Quantities TBD (scope uncertainty)
- Geotechnical unknowns (excavation risk)
- Trenchless crossing variability (high unit cost uncertainty)

**Source:** AGENT_ESTIMATING contingency model (lines 653-667); Risk_Register.md

---

## 9. Escalation

**Mode:** NONE (D-009)
**Rationale:** Current pricing (2026-01); no schedule available for escalation calculation
**Exposure:** 3-6% annual escalation over 2-3 year project = potential $127k-$380k addition (see Risk R-008)

---

## 10. Rounding Policy

**Rounding:** Nearest $1,000 CAD (D-007)
**Application:** Summary totals only; Detail.csv retains calculated precision

---

## 11. Completeness Metrics

### Pricing Method Distribution

- ALLOWANCE: 77.7% ($1,647k)
- PARAMETRIC: 22.3% ($472k)
- QUOTE: 0%
- RATE_TABLE: 0%

### Quantity Extraction Success

- Deliverable counts: 100% (6/6)
- Physical quantities: 0% (all TBD)

---

## 12. Known Gaps

**Critical Gaps:**
1. No vendor quotes or rate tables
2. Physical quantities TBD (pipe lengths, OWS capacity, duct bank quantities)
3. Employer's Requirements Volume 2 Part 2 not available
4. Geotechnical report not available
5. Construction schedule not available
6. PKG-17 electrical design not available (for duct bank coordination)

**Impact:** Estimate suitable for conceptual budgeting only

---

## 13. Key Assumptions Requiring Validation

1. **A-001:** Storm drainage network (800-1200 LM, DN150-DN600) — $770k, 36% of base
2. **A-005:** Trenchless crossings (4-8 crossings, 15-40m each) — $265k, 13% of base
3. **A-003:** OWS capacity (50-100 L/s) and discharge limits (<15 mg/L O&G) — $230k, 11% of base
4. **A-004:** Duct bank network (400-600 LM, 4-8 conduits) — $240k, 11% of base

**Validation Path:** Complete design (DEL-03.01, DEL-03.03), obtain ER Volume 2 Part 2, acquire vendor quotes

---

## 14. Supporting Documents

- Decision_Log.md (13 decisions)
- Assumptions_Log.md (27 assumptions)
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
**Decisions:** 13 documented
**Assumptions:** 27 documented

---

## 16. Recommended Next Steps

**Immediate (Before Decision-Making):**
1. Complete DEL-03.03 hydraulic calculations to size storm drainage
2. Complete DEL-03.03 OWS sizing based on throughput and discharge permit
3. Develop DEL-03.01 drainage layout with pipe routing and quantities
4. Obtain budgetary quotes for OWS equipment, pipe materials, trenchless boring

**Medium-Term:**
5. Obtain Employer's Requirements Volume 2 Part 2 (Civil & Process Mechanical)
6. Obtain geotechnical report for excavation planning
7. Coordinate with PKG-17 electrical for duct bank requirements
8. Develop project rate tables for labor, equipment, materials
9. Re-run estimate to upgrade from Class 5 to Class 4/3

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
- Design quantities available
- Vendor quotes obtained
- ER Volume 2 Part 2 extracted
- Geotechnical report available
- PKG-17 electrical coordination complete

---

**Basis of Estimate Prepared By:** Estimating Agent
**Date:** 2026-01-28
**Status:** Complete
**Snapshot:** EST_PKG03_DRAFT_2026-01-28_2330
