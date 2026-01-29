# Source Index — PKG-25 Communications & IT

**Snapshot ID:** EST_PKG25_DRAFT_2026-01-29_0004
**Package:** PKG-25 Communications & IT
**Date:** 2026-01-29

---

## Purpose

This index catalogs all pricing and quantity sources discovered and used in the estimate, organized by priority tier per AGENT_ESTIMATING pricing hierarchy.

---

## Source Discovery Summary

**Search Strategy:**
1. Searched for vendor quotes, budgetary quotes, proposals, PO summaries
2. Searched `_RateTables/` directory for rate tables and cost libraries
3. Searched deliverable folders for quantity data (datasheets, specifications)
4. Applied fallback typical model when no project-specific sources found

**Discovery Result:** Zero project-specific pricing sources found; fallback model applied

---

## Tier 1: Explicit Pricing Sources (Vendor Quotes)

**Priority:** Highest
**Status:** NOT FOUND

### Search Locations

- `/Users/ryan/ai-env/projects/chirality-app/test/execution/_Estimates/_RateTables/` — Not found or empty
- `/Users/ryan/ai-env/projects/chirality-app/test/execution/PKG-25_Communications_and_IT/` — No quotes found
- Workspace search for files matching: `quote`, `proposal`, `budget`, `PO`, `pricing` — Zero results

### Attempted Vendors (Expected Sources)

- Network equipment vendors (Cisco, Juniper, HPE, Aruba, Dell, etc.) — No quotes available
- Structured cabling suppliers (Belden, CommScope, Panduit, Leviton, etc.) — No quotes available
- Telecommunications installers/integrators — No quotes available
- Fiber optic suppliers (Corning, OFS, AFL, etc.) — No quotes available

**Impact:** 0% of estimate priced from quotes (target >60% for Class 3)

**Recommendation:** Solicit budgetary quotes from vendors for:
1. Network switches (specify port counts, PoE capability, Layer 2/3 features)
2. Patch panels (fiber LC/SC; copper Cat 6/6A)
3. Fiber optic cables (OS2 single-mode; OM3/OM4 multi-mode)
4. Structured copper cabling (Cat 6 or Cat 6A; plenum/riser rated)
5. Installation labor (per LM fiber; per LM copper; per outlet)

---

## Tier 2: Rate Tables / Cost Libraries

**Priority:** High
**Status:** NOT FOUND

### Search Locations

- `/Users/ryan/ai-env/projects/chirality-app/test/execution/_Estimates/_RateTables/` — Directory empty or not found
- Workspace search for files matching: `rate`, `unit cost`, `cost library`, `pricing table` — Zero results

### Expected Rate Tables (Not Found)

- Labor rates (telecommunications technicians, fiber splicers, low-voltage electricians, engineers)
- Material unit costs (cable per LM; connectors per each; patch panels per panel)
- Equipment unit costs (switches per port; patch cords per each)
- Installation productivity rates (LM per day; outlets per day; splices per day)

**Impact:** 0% of estimate priced from rate tables (target >25% for Class 3)

**Recommendation:** Develop and populate `_RateTables/` directory with:
1. `Labor_Rates.csv` — Vancouver/Lower Mainland BC labor rates (loaded, by trade)
2. `Fiber_Installation_Rates.csv` — Fiber cable installation rates (per LM by installation type)
3. `Copper_Cabling_Rates.csv` — Structured cabling installation rates (per LM, per outlet, per termination)
4. `Network_Equipment_Rates.csv` — Switch pricing (by port count and feature set)
5. `Materials_Unit_Costs.csv` — Cable, connector, patch panel unit costs

---

## Tier 3: Quantity Sources (Deliverable Documents)

**Priority:** Medium
**Status:** PARTIAL

### Deliverable Documents Reviewed

| Deliverable | Documents Read | Quantities Extracted | Status |
|-------------|----------------|----------------------|--------|
| DEL-25.01 | Specification.md, Datasheet.md | Deliverable types; anticipated artifacts (fiber layout, distribution drawings, patch panel locations) | Qualitative only |
| DEL-25.02 | Specification.md, Datasheet.md | Cable types (OS2 SMF, OM3/OM4 MMF, Cat 6/6A UTP); standards (TIA-568, TIA-569); performance specs | Qualitative only |
| DEL-25.03 | Datasheet.md | Equipment types (network switches, patch panels); anticipated counts (4-8 switches, 8-15 panels) | Range estimates only |
| DEL-25.04 | Not reviewed (test records) | Testing scope (fiber OTDR, copper certification per TIA-568) | Qualitative only |

### Quantities Extracted (Deliverable Counts)

- Design drawings: 4+ drawings (fiber network layout, communications distribution, patch panel locations per DEL-25.01)
- Technical specifications: 2 specs (fiber cable spec, network cabling spec per DEL-25.02)
- Data sheets: 2 categories (network switches, patch panels per DEL-25.03)
- Test records: 2 categories (fiber test records, network test records per DEL-25.04)

**Quantities NOT Extracted (TBD Pending Design):**

- Fiber cable lengths and fiber counts (800-1500 LM estimated range; actual TBD per DEL-25.01 design)
- Copper cable lengths and port counts (1500-2500 LM estimated range; 50-100 outlets estimated; actual TBD per DEL-25.01 design)
- Network switch counts and specifications (4-8 switches estimated; actual TBD per network architecture and DEL-25.03)
- Patch panel counts and port configurations (8-15 panels estimated; actual TBD per DEL-25.01 rack elevations)
- Telecommunications room (TR) locations and counts (2-4 TRs estimated; actual TBD per PKG-21 building layouts)

**Impact:** 100% of deliverables inventoried; 0% of physical quantities extracted (all TBD)

**Recommendation:** Complete design deliverables to extract:
1. Cable schedules from DEL-25.01 (fiber and copper lengths, counts, sizes)
2. Equipment schedules from DEL-25.03 (switch models, port counts, PoE capability)
3. Patch panel schedules from DEL-25.01 (panel types, port counts, rack locations)
4. Telecommunications room layouts from DEL-25.01 and PKG-21 coordination

---

## Tier 4: Fallback Typical Model (Applied)

**Priority:** Lowest (last resort)
**Status:** APPLIED

### Fallback Model Components Used

**Source:** AGENT_ESTIMATING.md lines 623-714 (Fallback Typical Model)

**Indirects Factors (PARAMETRIC):**

| Indirect | Factor Applied | Base | Amount (CAD) | Decision Reference |
|----------|----------------|------|--------------|-------------------|
| CI (Construction Indirects) | 18% of CD | $160,000 | $28,800 | D-2506 |
| P (Procurement) | 2% of MAT | $345,000 | $6,900 | D-2506 |
| PM (Project Management) | 6% of (CD+CI+MAT) | $533,800 | $32,028 | D-2506 |
| COM (Commissioning) | 3% of (CD+CI+MAT) | $533,800 | $16,014 | D-2506 |

**Total Parametric:** $83,742 (18% of base estimate)

**Contingency Model (PCT_BY_BUCKET with Allowance Adjustment):**

| CBS | Baseline Rate | Allowance Share | Adjustment | Final Rate | Decision Reference |
|-----|---------------|-----------------|------------|------------|-------------------|
| E | 10% | 100% | +10% | 20% | D-2508 |
| MAT | 15% | 100% | +10% | 25% | D-2508 |
| CD | 20% | 100% | +10% | 30% | D-2508 |
| CI | 25% | 100% (factor-derived) | +5% | 30% | D-2508 |
| P | 10% | 100% (factor-derived) | +5% | 15% | D-2508 |
| PM | 10% | 100% (factor-derived) | +5% | 15% | D-2508 |
| COM | 25% | 100% (factor-derived) | +5% | 30% | D-2508 |

**Total Contingency:** $168,533 (30% blended rate)

**Allowance Placeholders (ALLOWANCE Method):**

Used to avoid $0 coverage where no quotes or rates available:

| Line Item | Allowance Amount | Assumption Reference | Confidence |
|-----------|------------------|----------------------|------------|
| Fiber optic cabling system | $120,000 | A-2501 | LOW |
| Structured copper cabling system | $85,000 | A-2502 | LOW |
| Network switches and equipment | $95,000 | A-2503 | LOW |
| Patch panels | $30,000 | A-2504 | LOW |
| Cable management and infrastructure | $15,000 | A-2505 | MED |
| Engineering design | $75,000 | A-2506 | MED |
| Network equipment installation | $40,000 | A-2507 | LOW |
| Equipment room/TR setup | $30,000 | A-2515 | LOW |
| Fiber splicing labor | $15,000 | A-2509 | LOW |
| Spare capacity allowance | $5,000 | A-2518 | MED |
| Installation labor (copper) | $35,000 | A-2502 + A-2510 | LOW |
| Installation labor (fiber) | $40,000 | A-2501 + A-2509 | LOW |

**Total Allowances:** $585,000 (before indirects)
**Allowance Share of Base:** 82% (very high; typical for Class 5 with no quotes)

**Transparency:** All fallback model uses are:
- Labeled with Method=ALLOWANCE or Method=PARAMETRIC in Detail.csv
- Referenced to assumption IDs (A-xxxx) or decision IDs (D-xxxx) in SourceRef column
- Confidence marked as LOW or MED (never HIGH for fallback model)
- Disclosed in BOE.md §3.2 and QA_Report.md

---

## Source Summary

| Source Tier | Sources Found | Lines Priced | % of Base | Confidence |
|-------------|---------------|--------------|-----------|------------|
| Tier 1: Vendor Quotes | 0 | 0 | 0% | — |
| Tier 2: Rate Tables | 0 | 0 | 0% | — |
| Tier 3: Quantity Extraction | 4 deliverables (qualitative) | 0 | 0% | — |
| Tier 4: Fallback Model | All components | 15 | 100% | LOW-MED |

**Pricing Method Distribution:**

- QUOTE: 0% ($0)
- RATE_TABLE: 0% ($0)
- ALLOWANCE: 82% ($462,000)
- PARAMETRIC: 18% ($101,742)

**Overall Source Quality:** Very Low (no quotes, no rates, no quantities)

---

## Recommended Next Steps

### High Priority (Immediate)

1. **Obtain Vendor Quotes:**
   - Network equipment (switches, patch panels): Cisco, Juniper, HPE, Aruba, Dell
   - Fiber optic cables and materials: Corning, OFS, AFL, CommScope
   - Structured copper cabling: Belden, Panduit, Leviton, CommScope
   - Installation labor: Local telecommunications contractors

2. **Develop Rate Tables:**
   - Labor rates from local union agreements or market surveys
   - Material unit costs from distributor pricing
   - Equipment unit costs from vendor catalogs or online pricing

### Medium Priority (Design Phase)

3. **Complete Quantity Takeoff:**
   - DEL-25.01 cable schedules (fiber and copper lengths, counts)
   - DEL-25.03 equipment schedules (switch models, specifications)
   - DEL-25.01 rack elevations (patch panel counts and configurations)
   - Building layouts from PKG-21 (TR locations, cable routing)

4. **Validate Assumptions:**
   - Network architecture (bandwidth, topology, redundancy)
   - Technology selections (Cat 6 vs Cat 6A, fiber grades, PoE requirements)
   - Site access constraints (security clearances, work hours)

### Long-Term (Estimate Maturity Upgrade)

5. **Re-Run Estimate:**
   - Replace allowances with unit-rate pricing
   - Upgrade from Class 5 to Class 4 or Class 3
   - Reduce contingency as uncertainty decreases
   - Apply escalation if project schedule available

---

**Source Index Prepared By:** Estimating Agent
**Date:** 2026-01-29
**Status:** Complete
**Sources Found:** 0 pricing sources (fallback model applied)
