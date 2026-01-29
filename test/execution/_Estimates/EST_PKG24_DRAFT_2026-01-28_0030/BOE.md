# Basis of Estimate (BoE) — PKG-24 Security Systems

**Snapshot ID:** EST_PKG24_DRAFT_2026-01-28_0030
**Estimate Label:** PKG24_DRAFT
**Package Scope:** PKG-24 Security Systems
**Date:** 2026-01-28
**Prepared By:** Estimating Agent (Automated Pipeline)

---

## Executive Summary

**Total Estimate:** $1,047,000 CAD (rounded, includes contingency)
**Base Estimate:** $834,000 CAD (before contingency)
**Contingency:** $213,000 CAD (26% blended rate)
**Currency:** CAD (Canadian dollars)
**Pricing Date:** January 2026
**Confidence:** LOW (100% allowance/parametric; no vendor quotes; quantities TBD)
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

### 1.2 PKG-24 Scope

**Package Description:** CCTV, access control, integration with Terminal security network

**Deliverables (4 total):**
- DEL-24.01: Security System Design Drawing Set
- DEL-24.02: Security System Technical Specification
- DEL-24.03: Security System Data Sheet Package
- DEL-24.04: Security System Installation & Test Records

**Source:** Decomposition Section 5, PKG-24, lines 556-569

**Key Interfaces:**
- DEC-05: Terminal network interfaces treated as multiple distinct systems (CCTV, access control, communications separate)
- PKG-17 (Electrical Power): Power supply for security equipment
- PKG-23 (Fire Protection): Access control integration with fire alarm/life safety
- PKG-25 (Communications & IT): Network infrastructure backbone
- PKG-29 (Testing): Site acceptance testing procedures
- PKG-30 (Commissioning): System commissioning and Terminal integration

**Objectives Supported:**
- OBJ-1 (Safe & Reliable Operation): Security monitoring supports safety observation
- OBJ-6 (Regulatory Compliance): Privacy and port security compliance

---

## 2. Estimate Scope and Basis

### 2.1 Inclusions

- **Engineering & Design (E):** CCTV layout drawings, access control layout, coverage analysis, system architecture, specifications, datasheets, installation/test support
- **Materials (MAT):** CCTV cameras (fixed and PTZ), NVR, VMS software, access control readers, controllers, software, door hardware, network switches, UPS, cabling, conduit, camera poles
- **Construction Directs (CD):** Camera installation, access control installation, network equipment installation, underground conduit installation, camera pole foundations, testing and commissioning labor
- **Construction Indirects (CI):** Field supervision, QA/QC, HSE, site overhead
- **Project Management (PM):** EPCM allocation, Terminal coordination
- **Procurement (P):** Vendor coordination, expediting, submittal management
- **Commissioning (COM):** Integrated system testing, Terminal integration, performance verification, training support

---

### 2.2 Exclusions

- Owner's costs, land, financing, Employer-obtained permits
- Other packages (PKG-00 through PKG-23, PKG-25 through PKG-35)
- Security operations procedures (Employer responsibility)
- Terminal-wide security master plan upgrades beyond Phase 1 facility interface
- Nitrogen skid security monitoring (skid supplied by Employer per DEC-07)
- Escalation (January 2026 pricing basis)
- Taxes (GST/PST)

**Source:** `_CONFIG.md`; Decision D-005; Decomposition Sections 1.2 and 7 (Decisions)

---

## 3. Pricing Sources and Methods

### 3.1 Source Hierarchy Applied

1. Vendor quotes: 0% (none available)
2. Rate tables: 0% (none available)
3. Allowances: 85.5% ($714k)
4. Parametric factors: 14.5% ($120k - indirects/services)

**Decision:** D-008 (use fallback model)

**Source Index:** See `Source_Index.md`

---

### 3.2 Fallback Model Disclosure

**Primary pricing basis:** Fallback typical model (no project-specific sources)

**Components used:**
- Allowance placeholders for engineering, materials, and construction (A-001 through A-021)
- Indirects factors: CI=18%, P=2%, PM=6%, COM=3% (D-009)
- Contingency baseline by bucket with allowance-heavy adjustment (D-010)

**Transparency:** All uses labeled ALLOWANCE or PARAMETRIC with LOW/MED confidence and traced to assumptions/decisions

**Source:** AGENT_ESTIMATING fallback model, lines 623-691

---

## 4. Currency and Pricing Date

**Currency:** CAD (D-002) — project location Surrey, BC
**Pricing Date:** January 2026 (D-003) — current pricing
**Escalation:** NONE (D-004) — no escalation applied

---

## 5. Estimate Methodology

### 5.1 WBS to CBS Mapping

- Design deliverables (DEL-24.01 through DEL-24.04 engineering support) → Engineering (E)
- Equipment and materials (cameras, NVR, VMS, access control, network, cabling) → Materials (MAT)
- Installation work (mounting, cable pulling, configuration, testing) → Construction Directs (CD)
- Field management and QA/QC → Construction Indirects (CI)
- Vendor coordination and submittals → Procurement (P)
- Project oversight and Terminal coordination → Project Management (PM)
- Integrated testing and handover → Commissioning (COM)

**Source:** WBS_CBS_Matrix.csv; Decision D-006

---

### 5.2 Quantity Extraction

**Extracted from deliverable documents:**
- Deliverable artifact counts (drawings, specs, datasheets, test records)
- Qualitative scope descriptions (CCTV, access control, Terminal integration per DEC-05)
- Environmental requirements (coastal marine; IP66/IP67; IK10; -20°C to +40°C)
- Integration requirements (separate interfaces for CCTV and access control per DEC-05)

**Estimated Quantities (engineering judgment based on facility scope):**
- CCTV fixed cameras: 18 units (coverage for tank farm, railcar unloading, marine loading, perimeter, gates, buildings)
- CCTV PTZ cameras: 3 units (flexible coverage for key monitoring areas)
- Total cameras: 21 units
- Access control card readers: 12 units (site gates, building entrances, restricted areas)
- Controlled doors/gates: 12 locations
- NVR systems: 2 units (redundant configuration)
- Access control controllers: 2 units (distributed architecture)
- Network PoE switches: 4 units
- Camera poles: 8 units (for areas without building/structure mounting)
- Underground conduit routing: 400-700 LM (coordinate with PKG-03)
- Cable (Cat6A): 2000-3000m
- Fiber optic: 500-800m

**Not Extracted (TBD):**
- Exact camera locations and coverage zones (pending DEL-24.01 design)
- Specific equipment models and manufacturers (pending DEL-24.03 submittals)
- Detailed cable routing and lengths (pending coordination with PKG-03, PKG-17, PKG-25)
- Terminal integration protocols and requirements (pending Employer coordination)

**Impact:** Cannot create vendor-specific quotes; forced to use market-average allowances for industrial IP security systems

**Source:** Exploration findings (DEL-24.01 through DEL-24.04 documents); Assumptions A-001 through A-021; typical security system design for 1M MT/a transload facility

---

### 5.3 Pricing Methodology

**Allowance Sizing (equipment and materials):**
- CCTV fixed cameras: $63k (18 units @ $2500-4500/unit avg $3500) — A-002
- CCTV PTZ cameras: $36k (3 units @ $9000-15000/unit avg $12000) — A-003
- NVR system: $30k (2 units @ $12000-18000/unit avg $15000) — A-004
- VMS software: $25k (5-10 user licenses, ONVIF-compliant, Terminal integration) — A-005
- Access control readers: $14.4k (12 units @ $800-1500/unit avg $1200) — A-006
- Access control controllers: $16k (2 units @ $6000-10000/unit avg $8000) — A-007
- Access control software: $18k (3-5 user licenses, Terminal integration per DEC-05) — A-008
- Door hardware: $10k (electric strikes/mag locks, REX, door position switches for 12 doors) — A-009
- Network switches and fiber: $18k (4 PoE switches with accessories) — A-010
- UPS: $8.4k (3 units @ $2000-3500/unit avg $2800) — A-011
- Cabling and conduit materials: $95k (bulk materials for 21 cameras + 12 readers + network) — A-012
- Camera poles: $25.6k (8 poles @ $2500-4000/pole avg $3200) — A-013

**Allowance Sizing (engineering):**
- Engineering design: $123k total (1500-1900 hours @ $140-175/hr blended) — A-001
  - DEL-24.01 drawings: $48k (600-800 hours)
  - DEL-24.02 specification: $32k (400-500 hours)
  - DEL-24.03 datasheet support: $18k (200-250 hours)
  - DEL-24.04 test/commissioning support: $25k (300-350 hours)

**Allowance Sizing (construction directs):**
- Camera installation: $17.85k (21 cameras @ 6-12 hrs/camera, $120-150/hr loaded) — A-014, A-020
- Access control installation: $13.2k (12 doors @ 8-14 hrs/door, $120-150/hr loaded) — A-015, A-020
- Network/central equipment installation: $42k (250-350 hours @ $120-150/hr loaded) — A-016, A-020
- Underground conduit installation: $95k (400-700 LM trenching/boring, coordinate PKG-03) — A-017
- Camera pole foundations: $11.2k (8 poles @ 10-16 hrs/pole, $120-150/hr loaded + concrete) — A-018
- Testing and commissioning labor: $65k (400-550 hours @ $120-150/hr loaded) — A-019, A-021

**Calculated Indirects (factor-based per fallback model):**
- CI = 18% × CD ($244k) = $44k
- P = 2% × MAT ($359k) = $7k
- PM = 6% × (CD+CI+MAT) ($647k) = $37k
- COM = 3% × (CD+CI+MAT) ($647k) = $19k

**Source:** Assumptions_Log.md, Decision_Log.md; typical market rates for BC Lower Mainland industrial security systems

---

## 6. Location and Productivity

**Location:** Fraser Surrey Terminal, Surrey, BC (coastal marine environment)

**Labor Market:** Vancouver/Lower Mainland BC rates (prevailing wage or union rates likely)
**Site Conditions:** Active marine terminal; coastal environment (salt spray, corrosion concerns); Terminal operations continuity constraints per OBJ-5
**Environmental:** IP66/IP67 outdoor equipment ratings; IK10 vandal resistance; corrosion-resistant materials; -20°C to +40°C operating temperature
**Productivity:** Standard EPC productivity with Terminal coordination constraints; phased installation to minimize operational disruption

**Adjustments:** Terminal operational interface and phased installation may reduce productivity 10-20% (reflected in CD/CI contingency)

**Source:** Assumptions A-020, A-021; Risk R-007; Decomposition Section 2 (OBJ-5 Terminal Continuity)

---

## 7. Indirects Model

**Model:** Factor-based (D-004, D-009)

**Rationale:** No construction schedule available; factor-based appropriate for conceptual estimate

| Indirect | Factor | Base | Amount (CAD) |
|----------|--------|------|--------------|
| CI | 18% | CD=$244k | $44,000 |
| P | 2% | MAT=$359k | $7,000 |
| PM | 6% | CD+CI+MAT=$647k | $37,000 |
| COM | 3% | CD+CI+MAT=$647k | $19,000 |

**Source:** AGENT_ESTIMATING fallback factors (lines 643-652)

---

## 8. Contingency Method

**Method:** PCT_BY_BUCKET with allowance-heavy adjustment (D-010)

**Rates Applied:**

| CBS | Base (CAD) | Allowance Share | Baseline Rate | Allowance Adj | Final Rate | Contingency (CAD) |
|-----|------------|-----------------|---------------|---------------|------------|-------------------|
| E | $123,000 | 100% | 10% | +10% | 20% | $24,600 |
| MAT | $359,000 | 100% | 15% | +10% | 25% | $89,750 |
| CD | $244,000 | 100% | 20% | +10% | 30% | $73,200 |
| CI | $44,000 | 100% (factor) | 20% | +10% | 30% | $13,200 |
| P | $7,000 | 100% (factor) | 10% | +5% | 15% | $1,050 |
| PM | $37,000 | 100% (factor) | 10% | +5% | 15% | $5,550 |
| COM | $19,000 | 100% (factor) | 25% | +5% | 30% | $5,700 |

**Total Contingency:** $213,000 CAD (26% blended)

**Rationale:** Elevated rates due to:
- No vendor quotes (equipment pricing uncertainty)
- Quantities based on engineering judgment (scope uncertainty)
- Terminal integration complexity (protocol compatibility, network security)
- Coastal marine environment (equipment ratings, corrosion protection)
- Technology refresh risk (5-7 year equipment lifecycle vs 15-20 year infrastructure)

**Source:** AGENT_ESTIMATING contingency model (lines 653-667); Risk_Register.md

---

## 9. Escalation

**Mode:** NONE (D-004)
**Rationale:** Current pricing (2026-01); no schedule available for escalation calculation
**Exposure:** 3-6% annual escalation over 2-3 year project = potential $50k-$157k addition (see Risk R-008)

---

## 10. Rounding Policy

**Rounding:** Nearest $1,000 CAD (D-007)
**Application:** Summary totals only; Detail.csv retains calculated precision

---

## 11. Completeness Metrics

### Pricing Method Distribution

- ALLOWANCE: 85.5% ($714k)
- PARAMETRIC: 14.5% ($120k - indirects/services factors)
- QUOTE: 0%
- RATE_TABLE: 0%

### Quantity Extraction Success

- Deliverable counts: 100% (4/4)
- Equipment quantities: 0% (engineering judgment estimates only; pending design)
- Installation hours: 0% (allowance estimates only)

---

## 12. Known Gaps

**Critical Gaps:**
1. No vendor quotes or rate tables for security equipment
2. Equipment quantities based on engineering judgment (pending DEL-24.01 coverage design)
3. No Terminal integration specification (protocols, network topology, firewall rules TBD)
4. Employer's Requirements Volume 2 not available (security performance requirements TBD)
5. Construction schedule not available (phasing, Terminal coordination constraints)
6. PKG-17 electrical design not available (power supply routing)
7. PKG-25 communications design not available (network backbone details)
8. Existing Terminal security system documentation not available (integration requirements)

**Impact:** Estimate suitable for conceptual budgeting only; not suitable for procurement or contracting

---

## 13. Key Assumptions Requiring Validation

1. **A-002:** 18 fixed CCTV cameras @ $3500/unit — $63k, 8% of base
2. **A-012:** Cabling and conduit materials bulk allowance — $95k, 11% of base
3. **A-017:** Underground conduit installation (400-700 LM) — $95k, 11% of base
4. **A-019, A-021:** Testing and commissioning labor (400-550 hours) — $65k, 8% of base
5. **A-023:** Terminal integration complexity and protocols per DEC-05 (separate CCTV/access control interfaces)

**Validation Path:**
- Complete DEL-24.01 coverage design with camera counts and locations
- Complete DEL-24.02 specification with equipment performance requirements
- Obtain Employer's Requirements Volume 2 security requirements
- Obtain budgetary quotes from security system integrators
- Coordinate with Terminal IT/security for integration requirements

---

## 14. Supporting Documents

- Decision_Log.md (11 decisions)
- Assumptions_Log.md (23 assumptions)
- Source_Index.md (no pricing sources found)
- Detail.csv (27 line items, all fields populated)
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
4. ✓ Extract quantities (deliverable counts + engineering judgment equipment estimates)
5. ✓ Price line items (allowances + parametric factors)
6. ✓ Apply indirects (factor-based)
7. ✓ QA checks
8. ✓ Risk register + contingency
9. ✓ Publish snapshot

**Human Interaction:** None (straight-through)
**Decisions:** 11 documented
**Assumptions:** 23 documented

---

## 16. Recommended Next Steps

**Immediate (Before Decision-Making):**
1. Complete DEL-24.01 coverage analysis and camera layout with quantities
2. Obtain Employer's Requirements Volume 2 security system requirements
3. Coordinate with Terminal IT/security for integration requirements (protocols, credentials, network topology)
4. Obtain budgetary quotes from security system integrators for equipment packages
5. Clarify fail-safe/fail-secure requirements with PKG-23 fire protection

**Medium-Term:**
6. Develop detailed cable routing coordinated with PKG-03, PKG-17, PKG-25
7. Obtain existing Terminal security system documentation for integration planning
8. Develop project rate tables for security systems installation labor
9. Complete privacy compliance assessment (PIPEDA, signage, data retention)
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
- Coverage design complete with camera quantities and locations
- Equipment specifications and vendor quotes obtained
- Terminal integration requirements defined
- ER Volume 2 security requirements extracted
- PKG-17 electrical and PKG-25 communications coordination complete

---

**Basis of Estimate Prepared By:** Estimating Agent
**Date:** 2026-01-28
**Status:** Complete
**Snapshot:** EST_PKG24_DRAFT_2026-01-28_0030
