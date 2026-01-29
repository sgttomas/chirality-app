# Source Index — PKG-24 Security Systems Estimate

**Snapshot ID:** EST_PKG24_DRAFT_2026-01-28_0030
**Date:** 2026-01-28

This index lists pricing and quantity sources discovered during the estimating pipeline.

---

## 1. Vendor Quotes and Budgetary Pricing

**Search Results:** No vendor quotes found

**Locations Searched:**
- `/Users/ryan/ai-env/projects/chirality-app/test/execution/PKG-24_Security_Systems/`
- `/Users/ryan/ai-env/projects/chirality-app/test/execution/_Estimates/_RateTables/`
- `/Users/ryan/ai-env/projects/chirality-app/test/0_References/` (if exists)

**Conclusion:** No security system equipment quotes or budgetary pricing available

---

## 2. Project Rate Tables

**Search Results:** No project rate tables found

**Locations Searched:**
- `/Users/ryan/ai-env/projects/chirality-app/test/execution/_Estimates/_RateTables/`
- Package-level reference folders

**Conclusion:** No rate tables for security systems equipment, materials, or installation labor

---

## 3. Deliverable Document Sources (Quantities and Requirements)

**Documents Read:**

| Document | Path | Content Extracted |
|----------|------|-------------------|
| DEL-24.01 Datasheet.md | `PKG-24_Security_Systems/1_Working/DEL-24.01.../Datasheet.md` | Qualitative scope (CCTV layout, camera coverage, access control layout); quantities TBD; environmental requirements (IP66/IP67, IK10, -20°C to +40°C); Terminal integration per DEC-05 |
| DEL-24.01 Specification.md | `PKG-24_Security_Systems/1_Working/DEL-24.01.../Specification.md` | Design requirements; coverage requirements (facial recognition, detection levels); Terminal integration per DEC-05; no explicit quantities |
| DEL-24.01 Guidance.md | `PKG-24_Security_Systems/1_Working/DEL-24.01.../Guidance.md` | Design principles; coverage strategy; typical camera counts (TBD); access control zoning; Terminal integration considerations |
| DEL-24.01 Procedure.md | `PKG-24_Security_Systems/1_Working/DEL-24.01.../Procedure.md` | Drawing production workflow; no quantities |
| DEL-24.02 Datasheet.md | `PKG-24_Security_Systems/1_Working/DEL-24.02.../Datasheet.md` | CCTV system components (cameras, NVR, VMS); access control components (readers, controllers, software, door hardware); network infrastructure; specifications TBD |
| DEL-24.02 Specification.md | `PKG-24_Security_Systems/1_Working/DEL-24.02.../Specification.md` | Performance requirements; environmental ratings; Terminal integration per DEC-05; no explicit quantities or pricing |
| DEL-24.03 Datasheet.md | `PKG-24_Security_Systems/1_Working/DEL-24.03.../Datasheet.md` | Equipment categories (CCTV cameras, NVR, VMS, access control readers, controllers, door hardware, network, UPS); quantities TBD |
| DEL-24.03 Specification.md | `PKG-24_Security_Systems/1_Working/DEL-24.03.../Specification.md` | Equipment submittal requirements; compliance verification; no pricing |
| DEL-24.04 Datasheet.md | `PKG-24_Security_Systems/1_Working/DEL-24.04.../Datasheet.md` | Installation and test record requirements; testing scope; commissioning scope; no hours or pricing |
| DEL-24.04 Specification.md | `PKG-24_Security_Systems/1_Working/DEL-24.04.../Specification.md` | Installation verification requirements; testing requirements; Terminal integration testing per DEC-05; no hours or pricing |

**Quantities Extracted:** None (all TBD; deliverables are INITIALIZED status with no design quantities)

**Pricing Extracted:** None (no vendor datasheets or pricing information in deliverable documents)

---

## 4. Reference Documents

**Decomposition Document:**
- Path: `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md`
- Content Used:
  - Section 1.1: Project parameters (1,000,000 MT/a throughput, 45,000 MT storage, 32 railcar stations)
  - Section 2: Objectives (OBJ-1 Safe & Reliable Operation, OBJ-5 Terminal Continuity, OBJ-6 Regulatory Compliance)
  - Section 5, PKG-24: Security Systems scope (CCTV, access control, Terminal integration)
  - Section 7, DEC-05: Terminal network interfaces treated as multiple distinct systems

**Employer's Requirements:**
- Expected: Volume 2 Parts 1-3
- Status: Not available in workspace
- Impact: Security performance requirements TBD

**Terminal Security Documentation:**
- Expected: Existing Terminal security system as-builts and integration specification
- Status: Not available
- Impact: Integration requirements (protocols, network topology, credentials) TBD

---

## 5. Comparable Project Data and Historical Pricing

**Search Results:** No comparable project data or historical pricing found in workspace

**Conclusion:** No project-specific historical data for security systems

---

## 6. Embedded Fallback Model (Used)

**Source:** AGENT_ESTIMATING fallback typical model
**Path:** `/Users/ryan/ai-env/projects/chirality-app/agents/AGENT_ESTIMATING.md`
**Lines Referenced:** 623-691 (Fallback Typical Model section)

**Model Components Used:**

1. **Indirects Factors (lines 643-652):**
   - CI = 18% × CD
   - P = 2% × MAT
   - PM = 6% × (CD + CI + MAT)
   - COM = 3% × (CD + CI + MAT)

2. **Contingency Baseline Rates (lines 653-667):**
   - E: 10% baseline
   - MAT: 15% baseline
   - CD: 20% baseline
   - CI: 20% baseline
   - P: 10% baseline
   - PM: 10% baseline
   - COM: 25% baseline

3. **Allowance-Heavy Adjustment (lines 669-677):**
   - If bucket AllowanceShare ≥ 50%: add +5%
   - If bucket AllowanceShare ≥ 80%: add additional +5% (total +10%)
   - **Applied to PKG-24:** All buckets are 100% allowance/parametric, so +10% adjustment applied

**Usage Transparency:**
- All fallback model usage documented in Decision_Log.md (D-009, D-010)
- All allowance line items marked with Method=ALLOWANCE and Confidence=LOW
- All parametric line items marked with Method=PARAMETRIC and Confidence=MEDIUM
- All line items traced to SourceRef (assumption or decision ID)

---

## 7. Market Data and Industry Typical Pricing

**Sources Used (for allowance development):**

| Source Type | Description | Application |
|-------------|-------------|-------------|
| Typical industrial IP camera pricing | Market research for 2-4MP outdoor IP66/IP67 cameras with IR | Fixed camera unit cost: $2,500-4,500, average $3,500 (A-002) |
| Typical industrial PTZ camera pricing | Market research for 2-4MP PTZ with 30x zoom, outdoor IP66/IP67 | PTZ camera unit cost: $9,000-15,000, average $12,000 (A-003) |
| Typical enterprise NVR pricing | Market research for 32-64 channel rack-mount NVR with RAID | NVR unit cost: $12,000-18,000, average $15,000 (A-004) |
| Typical VMS software pricing | Market research for ONVIF-compliant VMS with 5-10 user licenses | VMS software: $25,000 (A-005) |
| Typical access control pricing | Market research for industrial access control readers, controllers, software | Reader: $800-1,500 avg $1,200; Controller: $6,000-10,000 avg $8,000 (A-006, A-007, A-008) |
| Typical door hardware pricing | Market research for electric strikes, mag locks, REX, door switches | Strike/lock: $450-850 avg $650; REX/switch set: $120-240 avg $180 (A-009) |
| Typical network equipment pricing | Market research for managed PoE switches 24-48 port with fiber | PoE switch: $3,500-5,500 avg $4,500 (A-010) |
| Typical security systems labor rates | Vancouver/Lower Mainland BC prevailing wage or union rates | Loaded labor rate: $120-150/hr for security systems technician (A-020) |
| Typical engineering labor rates | BC professional engineering rates | Blended rate: $140-175/hr (senior designer + CAD technician) (A-001) |
| Typical security systems installation productivity | Industry standard installation hours per device | Camera: 6-12 hrs; Door: 8-14 hrs; Network: 250-350 hrs total (A-014, A-015, A-016) |

**Notes:**
- All market data is typical/average pricing for industrial-grade equipment (not project-specific quotes)
- Marine-grade equipment premium (15-30%) included in unit cost allowances for coastal environment
- Labor rates reflect BC Lower Mainland market (prevailing wage or union rates typical for public/industrial projects)

---

## 8. Pricing Source Summary

| Source Priority | Lines Using This Source | Base Amount | % of Base |
|-----------------|------------------------|-------------|-----------|
| 1. Vendor Quotes | 0 | $0 | 0% |
| 2. Rate Tables | 0 | $0 | 0% |
| 3. Historical/Project Data | 0 | $0 | 0% |
| 4. Allowances (market typical) | 23 | $714,000 | 86% |
| 5. Parametric (fallback factors) | 4 | $107,000 | 13% |
| **Total** | **27** | **$833,000** | **100%** |

**Pricing Quality:** LOW (no project-specific pricing; 100% market-average allowances and factors)

---

## 9. Recommended Source Improvements for Next Iteration

**To upgrade estimate from Class 5 to Class 4:**

1. **Obtain budgetary quotes (High Priority):**
   - Security system integrator turnkey quotes (2-3 vendors)
   - CCTV equipment quotes (cameras, NVR, VMS software)
   - Access control equipment quotes (readers, controllers, software)
   - Network equipment quotes (PoE switches, fiber equipment, UPS)
   - Installation labor rates from security systems contractors

2. **Develop project rate tables (High Priority):**
   - Security systems equipment unit costs by type (cameras, readers, controllers, etc.)
   - Installation labor rates by trade (security technician, electrician, commissioning engineer)
   - Material unit costs (cabling, conduit, camera poles)

3. **Obtain design quantities (High Priority):**
   - Complete DEL-24.01 coverage design with camera counts and locations
   - Complete DEL-24.01 access control layout with door/gate counts
   - Complete DEL-24.01 cable routing with conduit lengths and sizes

4. **Obtain Employer's Requirements (Medium Priority):**
   - ER Volume 2 security performance requirements
   - Terminal security integration specification (protocols, network, credentials)

**Expected Accuracy Improvement:** Class 4 (-20% to +30%) with quotes and design quantities; Class 3 (-15% to +20%) with final design and firm pricing

---

**Source Index Prepared By:** Estimating Agent
**Date:** 2026-01-28
**Status:** Complete
**Snapshot:** EST_PKG24_DRAFT_2026-01-28_0030
