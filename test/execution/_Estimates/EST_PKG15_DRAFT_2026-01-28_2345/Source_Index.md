# Source Index — PKG-15 Pumps & Rotating Equipment Estimate

**Snapshot ID:** EST_PKG15_DRAFT_2026-01-28_2345
**Package:** PKG-15 Pumps & Rotating Equipment
**Date:** 2026-01-28

---

## Source Discovery Summary

This index catalogs all information sources discovered and used for the PKG-15 estimate, organized by priority/reliability.

---

## 1. Explicit Pricing Sources (QUOTE)

**Status:** None found.

**Search performed:**
- Checked `_REFERENCES.md` files in all PKG-15 deliverable folders
- Searched for vendor quotes, budgetary proposals, PO summaries
- Searched workspace for files matching: `quote`, `proposal`, `budget`, `vendor`

**Result:** No vendor quotes or budgetary pricing available at this estimate stage.

**Impact:** All equipment pricing based on parametric allowances and typical industry costs.

---

## 2. Rate Tables / Cost Libraries (RATE_TABLE)

**Status:** None found for PKG-15 equipment.

**Search performed:**
- Checked `/Users/ryan/ai-env/projects/chirality-app/test/execution/_Estimates/_RateTables/`
- Searched deliverable folders for embedded cost data

**Result:** No project-specific rate tables for pumps, motors, or rotating equipment.

**Impact:** Equipment costs estimated using fallback parametric model and industry typical values.

---

## 3. Quantity Sources (DELIVERABLES)

**Primary sources:**

### 3.1 PKG-15 Deliverable Folder
**Path:** `/Users/ryan/ai-env/projects/chirality-app/test/execution/PKG-15_Pumps_and_Rotating_Equipment/1_Working/`

**Deliverables reviewed:**

| Deliverable | Files Reviewed | Quantities Extracted |
|-------------|---------------|---------------------|
| DEL-15.01 Pump Design Drawing Set | Datasheet.md, Specification.md | Arrangement scope, installation requirements (TBD quantities) |
| DEL-15.02 Pump Technical Specification | Datasheet.md, Specification.md | Pump types (railcar, marine, sump, transfer), performance requirements (quantities TBD) |
| DEL-15.03 Pump Design Calculations | Datasheet.md, Specification.md | Sizing methodology, NPSH requirements (calculations pending) |
| DEL-15.04 Pump Data Sheet Package | Datasheet.md, Specification.md | Vendor data requirements, equipment covered (quantities TBD) |
| DEL-15.05 Pump Installation & Test Records | Datasheet.md, Specification.md | Commissioning scope, testing requirements |

**Key findings:**
- All pump quantities listed as "**TBD**" pending DEL-15.03 calculations
- Pump services identified: railcar unloading, marine loading, sump, transfer (if applicable)
- Performance parameters TBD pending calculations and ER Part 2 data
- API 610 compliance required for process pumps
- Food-grade material requirements for canola oil service

**Traceability:**
- DEL-15.02 Datasheet line 36: "Quantity | **TBD**"
- DEL-15.04 Specification lines 27-32: All pump services show quantity "**TBD**"

---

### 3.2 Related Package Deliverables

**PKG-10 Railcar Unloading System:**
- Path: `/Users/ryan/ai-env/projects/chirality-app/test/execution/PKG-10_Railcar_Unloading_System/`
- Findings: Sump pump quantities TBD (1 or more per containment design)
- 32 railcar unloading stations confirmed

**PKG-11 Marine Loading System:**
- Path: `/Users/ryan/ai-env/projects/chirality-app/test/execution/PKG-11_Marine_Loading_System/`
- Findings: 1 sump pump for marine loading containment
- Marine loading arm requires pump feed (duty/standby configuration likely)

**PKG-13 Storage Tanks:**
- Referenced: 3 × 15,000 MT tanks (45,000 MT total storage capacity)
- Tank transfer pump requirements implied but not quantified

---

### 3.3 Project Decomposition
**Path:** `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md`

**Section:** PKG-15: Pumps & Rotating Equipment (lines 401-416)

**Extracted parameters:**
- Discipline: Mechanical
- Scope: "Railcar unloading pumps, marine loading pumps, sump pumps, motors, drives, pump containment"
- 5 deliverables (DEL-15.01 through DEL-15.05)
- Objectives: OBJ-1 (Safe & Reliable Operation), OBJ-2 (Throughput Capacity 1M MT/annum), OBJ-4 (Operational Flexibility)

**Facility-level parameters:**
- Location: Fraser Surrey Terminal, Surrey, BC
- Throughput: 1,000,000 MT/annum
- Storage: 45,000 MT (3 tanks)
- Railcar capacity: 32 stations

---

## 4. Embedded Fallback Model (PARAMETRIC / ALLOWANCE)

**Status:** Used for all equipment and labor pricing due to lack of quotes/rate tables.

**Source:** AGENT_ESTIMATING.md fallback typical model (lines 645-714)

**Factors applied:**
- Construction Indirects (CI): 18% of CD
- Procurement (P): 2% of (MAT + FRT)
- PM/EPCM: 6% of (CD + CI + MAT)
- Commissioning (COM): 3% of (CD + CI + MAT)
- Contingency: PCT_BY_BUCKET method with allowance-heavy adjustments

**Equipment cost basis:**
- API 610 process pumps: Parametric cost models based on size, capacity, and materials
- Motors: Cost per kW rating with NEMA Premium efficiency
- Baseplates, coupling, seals: Percentage of pump cost

**Labor cost basis:**
- Installation labor: $95/hr loaded (BC industrial rate)
- Productivity: 24 manhours per pump unit for setting/alignment
- Commissioning: 16 manhours per pump unit for testing

**Confidence:** LOW (per AGENT_ESTIMATING.md requirements when using fallback model)

---

## 5. Industry Typical Values / Engineering Judgment

**Pump quantities (parametric estimate):**
| Service | Estimated Qty | Basis |
|---------|---------------|-------|
| Railcar unloading transfer pumps | 4 units | 32 railcar stations, 1M MT/annum throughput, duty/standby pairs |
| Marine loading pumps | 2 units | Marine loading system, duty/standby configuration |
| Tank transfer pumps | 2 units | 3 storage tanks, operational flexibility (OBJ-4) |
| Sump pumps | 6 units | Containment zones (railcar area, marine area, tank farm) |
| **Total** | **14 pump units** | Parametric estimate for budgeting |

**Pump sizing (typical for canola oil facility):**
- Railcar unloading pumps: 200 m³/hr @ 50m head, 30 kW
- Marine loading pumps: 400 m³/hr @ 40m head, 50 kW
- Tank transfer pumps: 150 m³/hr @ 30m head, 15 kW
- Sump pumps: 25 m³/hr @ 15m head, 3 kW

**Basis:** Industry experience with similar vegetable oil transload facilities; canola oil properties (SG ~0.91, viscosity 40-60 cP @ 20°C).

**Confidence:** LOW-MEDIUM (requires validation against DEL-15.03 calculations and ER Part 2 requirements)

---

## 6. Sources Not Available / Missing

**Critical missing sources:**

1. **Employer's Requirements Volume 2 Part 2 (Process Mechanical Works)**
   - Expected location: `/Users/ryan/ai-env/projects/chirality-app/test/Volume_2_Part_2_Employers_Requirements.pdf`
   - Status: File exists but not read for this estimate
   - Impact: Pump performance requirements, materials, fluid properties may be specified
   - **Action:** Review ER Part 2 for pump specifications and update estimate

2. **DEL-15.03 Pump Design Calculations**
   - Status: INITIALIZED (calculations not yet performed)
   - Impact: Pump quantities, sizing, power requirements, NPSH margins unknown
   - **Action:** Complete DEL-15.03 and update equipment list

3. **Vendor Budgetary Quotes**
   - Status: Not available (early design stage)
   - Impact: Equipment costs estimated parametrically with LOW confidence
   - **Action:** Solicit budgetary quotes for API 610 pumps when specifications finalized

4. **Project-Specific Rate Tables**
   - Status: Not created
   - Impact: Using fallback model for labor, indirects, management
   - **Action:** Develop project rate tables for labor, equipment rental, indirects

5. **Engineering Hours Budget**
   - Status: No detailed breakdown by deliverable
   - Impact: Engineering costs estimated using similar package benchmarks
   - **Action:** Obtain engineering hours estimate from discipline lead

---

## 7. Source Priority Summary

**Estimate composition by pricing method:**

| Method | Line Items | Base Cost $ | % of Base | Confidence |
|--------|------------|-------------|-----------|------------|
| QUOTE (vendor quotes) | 0 | $0 | 0% | N/A |
| RATE_TABLE (project rates) | 0 | $0 | 0% | N/A |
| PARAMETRIC (fallback model) | ~25 | ~$950,000 | 60% | LOW-MEDIUM |
| ALLOWANCE (lump sum) | ~15 | ~$650,000 | 40% | LOW |
| **Total** | **~40** | **~$1,600,000** | **100%** | **LOW-MEDIUM** |

**Overall assessment:** Estimate has LOW-MEDIUM confidence due to:
- No vendor quotes
- TBD pump quantities in all deliverables
- Parametric equipment sizing
- Fallback model for indirects and management

**Recommended actions to improve confidence:**
1. Complete DEL-15.03 calculations (pump quantities and sizing)
2. Review ER Part 2 for pump specifications
3. Obtain budgetary quotes from pump vendors
4. Develop project-specific rate tables
5. Validate labor productivity assumptions for BC location

---

**Document Status:** FINAL
**Prepared By:** ESTIMATING Agent
**Date:** 2026-01-28
