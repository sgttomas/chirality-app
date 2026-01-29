# Source Index — PKG-16 Valves & Specialty Equipment

**Snapshot ID:** EST_PKG16_DRAFT_2026-01-28_2347
**Package:** PKG-16 Valves & Specialty Equipment
**Date:** 2026-01-28

---

## Purpose

This index catalogs the information sources searched and used to develop the estimate for PKG-16.

---

## 1. Vendor Quotes and Budgetary Pricing

**Search Results:** None found

**Locations Searched:**
- `/Users/ryan/ai-env/projects/chirality-app/test/execution/PKG-16_Valves_and_Specialty_Equipment/0_References/`
- `/Users/ryan/ai-env/projects/chirality-app/test/execution/_Estimates/_RateTables/`
- `/Users/ryan/ai-env/projects/chirality-app/test/0_References/` (if exists)

**Typical Vendor Quote Sources (not found):**
- Control valve manufacturers (Fisher, Emerson, Valmet, etc.)
- Isolation valve vendors (Velan, Tyco, Crane, etc.)
- Relief valve manufacturers (Crosby, Farris, Leser, etc.)
- Actuator suppliers (Rotork, Bettis, Limitorque, etc.)
- Strainer suppliers

**Decision:** D-016 (no vendor quotes available; proceed with allowances)

---

## 2. Project Rate Tables

**Search Results:** None found

**Locations Searched:**
- `/Users/ryan/ai-env/projects/chirality-app/test/execution/_Estimates/_RateTables/`
- Project execution folder for rate table files

**Typical Rate Table Sources (not found):**
- Valve unit costs by type and size
- Actuator costs by type and size
- Labor rates (installation, hookup, testing)
- Equipment rates (crane, rigging)

**Decision:** D-016 (no rate tables available; proceed with allowances)

---

## 3. Deliverable Engineering Documents

**Search Results:** 5 deliverables found (all INITIALIZED status)

**Documents Read:**

### DEL-16.01: Valve Design Drawing Set
- **Path:** `/Users/ryan/ai-env/projects/chirality-app/test/execution/PKG-16_Valves_and_Specialty_Equipment/1_Working/DEL-16.01_Valve_Design_Drawing_Set/`
- **Status:** INITIALIZED
- **Artifacts:** Valve arrangement drawings, actuator details (anticipated)
- **Quantity Information:** Drawing count anticipated (TBD); valve locations and arrangements TBD pending design

### DEL-16.02: Valve Technical Specification
- **Path:** `/Users/ryan/ai-env/projects/chirality-app/test/execution/PKG-16_Valves_and_Specialty_Equipment/1_Working/DEL-16.02_Valve_Technical_Specification/`
- **Status:** INITIALIZED
- **Artifacts:** Control valve specification, isolation valve specification, relief valve specification
- **Quantity Information:** Valve categories identified (control, isolation, relief, strainers, specialty); specific counts TBD pending P&ID development

### DEL-16.03: Valve Design Calculations
- **Path:** `/Users/ryan/ai-env/projects/chirality-app/test/execution/PKG-16_Valves_and_Specialty_Equipment/1_Working/DEL-16.03_Valve_Design_Calculations/`
- **Status:** INITIALIZED
- **Artifacts:** Control valve sizing, relief valve sizing calculations
- **Quantity Information:** Calculation scope TBD pending valve count and service definition

### DEL-16.04: Valve Data Sheet Package
- **Path:** `/Users/ryan/ai-env/projects/chirality-app/test/execution/PKG-16_Valves_and_Specialty_Equipment/1_Working/DEL-16.04_Valve_Data_Sheet_Package/`
- **Status:** INITIALIZED
- **Artifacts:** Control valve data sheets, isolation valve data sheets, relief valve data sheets
- **Quantity Information:** Datasheet count TBD pending valve count from P&IDs

### DEL-16.05: Valve Installation & Test Records
- **Path:** `/Users/ryan/ai-env/projects/chirality-app/test/execution/PKG-16_Valves_and_Specialty_Equipment/1_Working/DEL-16.05_Valve_Installation_and_Test_Records/`
- **Status:** INITIALIZED
- **Artifacts:** Material certificates, FAT records, set pressure test records
- **Quantity Information:** Test scope TBD pending valve quantities

**Quantity Extraction Results:**
- Deliverable counts: 5/5 deliverables present
- Explicit valve quantities: **None** (all TBD pending P&ID development)
- Material specifications: Stainless steel (316SS/304SS) preferred for product contact; materials TBD
- Environmental conditions: Coastal marine environment (Fraser Surrey Terminal, BC)

---

## 4. Cross-Package References

**Process Package References (P&IDs and Equipment):**
- PKG-10 Railcar Unloading System (32 railcar stations) — provides valve service requirements
- PKG-11 Marine Loading System — provides marine loading arm valve requirements
- PKG-12 Product Transfer & Metering — provides transfer system valve requirements
- PKG-13 Storage Tanks (3 × 15,000 MT tanks) — provides tank valve requirements and relief valve protected equipment data
- PKG-14 Process Piping — provides line list, line sizes, pressure classes for valve sizing

**Status:** P&IDs not available; valve quantities TBD

**Decision:** D-017 (estimate valve quantities based on facility type and typical transload installations)

---

## 5. Employer's Requirements (ER)

**Documents Referenced:**
- Volume 2 Part 1: `/Users/ryan/ai-env/projects/chirality-app/test/Volume_2_Part_1_Employers_Requirements.pdf`
- Volume 2 Part 2: `/Users/ryan/ai-env/projects/chirality-app/test/Volume_2_Part_2_Employers_Requirements.pdf`
- Volume 2 Part 3: `/Users/ryan/ai-env/projects/chirality-app/test/Volume_2_Part_3_Employers_Requirements.pdf`

**Extraction Status:** PDFs available but not extracted for valve-specific requirements

**Typical ER Content (not extracted):**
- Valve specification requirements
- Material requirements for food-grade service
- Testing and commissioning requirements
- Safety requirements (relief valve protection)

**Decision:** D-018 (ER volumes available but not extracted; proceed with typical valve requirements for canola oil transload facilities)

---

## 6. Decomposition Document

**Document:** `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md`

**PKG-16 Scope Extracted:**
- Package label: "Valves & Specialty Equipment"
- Discipline: Mechanical
- Scope description: "Control valves, isolation valves, relief valves, strainers, specialty items"
- Deliverable count: 5 deliverables (DEL-16.01 through DEL-16.05)

**High-Level Project Parameters (relevant to valve quantities):**
- Throughput: 1,000,000 MT/annum
- Storage: 45,000 MT (3 × 15,000 MT tanks)
- Railcar unloading: 32 railcar stations
- Marine loading: ship loading system

**Source:** Decomposition Section 5, PKG-16; Section 1 (Project Overview)

---

## 7. Fallback Typical Model

**Applicability:** HIGH

**Rationale:**
- No vendor quotes available
- No project rate tables available
- No design quantities (valve counts, sizes) available
- P&IDs not developed (valve tagging and service assignment TBD)

**Fallback Model Used:**
- Valve quantity estimation based on facility type (transload facility with 32 railcar stations, 3 storage tanks, marine loading)
- Valve pricing based on typical market rates (BC/Canada)
- Installation costs based on valve count and complexity
- Indirects/services factors per AGENT_ESTIMATING (CI=18%, P=2%, PM=6%, COM=3%)
- Contingency per AGENT_ESTIMATING PCT_BY_BUCKET method with allowance-heavy adjustments

**Source:** AGENT_ESTIMATING fallback model (lines 645-713)

**Decision:** D-016 (use fallback model for all pricing)

---

## Source Priority Summary

| Priority | Source Type | Coverage | Availability |
|----------|-------------|----------|--------------|
| 1 | Vendor quotes | 0% | Not available |
| 2 | Rate tables | 0% | Not available |
| 3 | Historical data | 0% | Not available |
| 4 | Allowances (fallback model) | 100% | Used |

**Result:** 100% allowance-based estimate with LOW confidence

**Recommendation for Next Iteration:**
1. Complete P&IDs (PKG-10, PKG-11, PKG-12, PKG-13) to establish valve counts and service requirements
2. Complete DEL-16.04 valve datasheets to establish valve sizes, types, and specifications
3. Obtain budgetary quotes from valve vendors (control valves, isolation valves, relief valves)
4. Develop project rate tables for valves, actuators, and installation labor
5. Re-run estimate to upgrade from Class 5 to Class 4/3

---

**Source Index Prepared By:** Estimating Agent
**Date:** 2026-01-28
**Status:** Complete (no quotes or rate tables found; proceeding with allowances)
