# Source Index — PKG-00 Site Establishment Estimate

**Snapshot ID:** EST_PKG00_DRAFT_2026-01-28_2315
**Package Scope:** PKG-00 Site Establishment
**Date:** 2026-01-28

---

## Source Discovery Summary

This index catalogs all pricing and quantity sources discovered during the estimate preparation phase, listed in priority order per AGENT_ESTIMATING protocol (Phase 2.2).

**Priority hierarchy:**
1. Explicit pricing sources (quotes, budgets, proposals)
2. Rate tables / cost libraries
3. Quantity sources (datasheets, specifications, procedures)
4. Embedded fallback model

---

## 1. Explicit Pricing Sources (Highest Priority)

**Status:** **NONE FOUND**

**Search performed:**
- Checked all deliverable `_REFERENCES.md` files in PKG-00 (DEL-00.01 through DEL-00.08)
- Searched for vendor quotes, budgetary quotes, proposals, budget sheets, PO summaries
- Checked deliverable folders for pricing documents

**Findings:**
- All deliverable `_REFERENCES.md` files state "no references identified yet" or list only the decomposition document
- No vendor quotes or pricing documents discovered in any deliverable folder
- No budgetary proposals or cost estimates found

**Impact:** Cannot price line items using project-specific vendor quotes. Must proceed to next source priority level.

**Resolution path:** Add vendor quotes to deliverable folders and reference in `_REFERENCES.md` files, then re-run estimate.

---

## 2. Rate Tables / Cost Libraries

**Status:** **NONE FOUND**

**Search performed:**
- Checked `_Estimates/_RateTables/` directory
- Searched workspace for files matching patterns: `rate`, `unit cost`, `cost`, `estimate`, `pricing`
- Checked deliverable folders for cost libraries

**Findings:**
- `_Estimates/_RateTables/` directory exists but is empty (created during initialization)
- No rate table files (CSV, XLSX, MD) discovered in workspace
- No historical project cost data or cost libraries found

**Impact:** Cannot price line items using project rate tables. Must proceed to next source priority level.

**Resolution path:** Add rate tables to `_Estimates/_RateTables/` directory in CSV or XLSX format with columns: Description, Unit, UnitRate, Currency, Date. Then re-run estimate.

---

## 3. Quantity Sources

**Status:** **FOUND** — Deliverable documents provide qualitative scope descriptions

**Search performed:**
- Read all PKG-00 deliverable documents (Datasheet.md, Specification.md, Guidance.md, Procedure.md)
- Extracted quantities, counts, sizes, and execution drivers

**Findings:**

### DEL-00.01: Site Establishment Design Drawing Set
- **Quantities:** 4 drawings (site layout, compound layout, temp facilities location, traffic management)
- **Source:** `_CONTEXT.md`, decomposition Section 5, line 141
- **Cost drivers:** CAD drafting effort, review/approval cycles, coordination with DEL-00.02 and DEL-00.03

### DEL-00.02: Site Establishment Technical Specification
- **Quantities:** 2 specifications (temporary facilities, temporary utilities)
- **Source:** `_CONTEXT.md`, decomposition Section 5, line 142
- **Scope elements:** Modular offices, storage, security fencing, gates, electrical service, water supply, sanitary sewer, drainage, telecommunications
- **Cost drivers:** Specification writing effort, material selection, workmanship standards, utility tie-in coordination

### DEL-00.03: Site Establishment Procedures
- **Quantities:** 3 procedures (traffic management plan, site access procedure, mobilization procedure)
- **Source:** `_CONTEXT.md`, decomposition Section 5, line 143
- **Cost drivers:** Procedure development effort, gate staffing requirements, traffic control, security coordination

### DEL-00.04: Contractor's Equipment Schedule
- **Quantities:** 2 documents (equipment list, mobilization/demobilization schedule)
- **Source:** `_CONTEXT.md`, decomposition Section 5, line 144
- **Example equipment:** Tower crane (50-ton, 52 weeks), excavators (2 units), concrete pump
- **Cost drivers:** Equipment rental costs, mobilization/demobilization, laydown space

### DEL-00.05: Road Access Configuration and Security Process Submission
- **Quantities:** 3 plans (road access configuration, security process, gate control procedures)
- **Source:** `_CONTEXT.md`, decomposition Section 5, line 145
- **Cost drivers:** Security gate implementation, staffing, access control system, authority approvals

### DEL-00.06: Pre-Works Road Condition Survey Report
- **Quantities:** 2 documents (baseline survey report, photo log)
- **Source:** `_CONTEXT.md`, decomposition Section 5, line 146
- **Cost drivers:** Surveyor field time, photo documentation (systematic intervals), report compilation

### DEL-00.07: Post-Works Road Condition Survey Report
- **Quantities:** 3 documents (post-construction survey, photo log, deficiency closeout)
- **Source:** `_CONTEXT.md`, decomposition Section 5, line 147
- **Cost drivers:** Survey execution, deficiency remediation, restoration coordination, authority sign-off

### DEL-00.08: Temporary Water Supply Installation Details
- **Quantities:** 3 drawings (water routing plan/profile, connection details, backflow prevention details)
- **Source:** `_CONTEXT.md`, decomposition Section 5, line 148
- **Scope elements:** Pipe sizing/routing (example: 50mm HDPE main, 25mm branches), backflow preventer (RPZ or DCVA), freeze protection
- **Cost drivers:** Drawing production, pipe materials, backflow device, utility provider approval, installation labor

**Impact:** Quantities are primarily **deliverable counts** (number of drawings, specifications, procedures, reports) rather than physical construction quantities. Physical quantities (e.g., linear feet of fencing, square feet of laydown area, number of office trailers) are marked as "TBD" in deliverable documents.

**Limitation:** Cannot create detailed quantity takeoffs for physical site establishment elements without additional input from Employer's Requirements.

**Resolution path:** Obtain Employer's Requirements (Volume 2 Part 1) to extract specific quantities for temporary facilities, fencing, laydown areas, utilities, etc.

---

## 4. Embedded Fallback Model

**Status:** **ACTIVE** (primary pricing basis)

**Trigger:** No project-specific pricing sources or rate tables found (Sections 1-2 above).

**Application:** Per AGENT_ESTIMATING STRUCTURE section (Fallback Typical Model), the fallback model will be used to:
- Provide placeholder allowances for deliverables without explicit quantities
- Apply default factors for indirects, project management, and commissioning
- Apply default contingency percentages by CBS bucket

**Method:**
- Line items priced using fallback model will be marked as `Method=ALLOWANCE` or `Method=PARAMETRIC`
- Confidence will be set to `LOW`
- Source reference will cite applicable Decision Log entry (e.g., `SourceRef=D-005`)

**Fallback Model Components:**

### Indirects Factors (from AGENT_ESTIMATING):
- Construction Indirects (CI) = 18% of Construction Directs (CD)
- Procurement (P) = 2% of (MAT + FRT)
- Commissioning (COM) = 3% of (CD + CI + MAT)
- EPCM/PM (PM) = 6% of (CD + CI + MAT + FRT)

### Contingency Baseline % (from AGENT_ESTIMATING):
- Engineering (E), PM, Procurement (P): 10%
- Materials (MAT), Freight (FRT): 15%
- Construction Directs (CD), Construction Indirects (CI): 20%
- Commissioning (COM): 25%
- **Adjustment:** +5% if bucket allowance share ≥ 50%; +10% if ≥ 80%

**Disclosure:** All uses of fallback model are explicitly documented in Decision_Log.md (D-005, D-006, D-008) and will be flagged in QA_Report.md.

---

## Source Selection Decision

**Decision Reference:** D-005 (Decision_Log.md)

**Primary Basis:** Fallback typical model (no project-specific sources available)

**Confidence:** LOW

**Recommendation:** Acquire vendor quotes and/or develop project rate tables to replace fallback allowances in next estimate iteration.

---

## Deliverables Inventory — Source Coverage

| Deliverable ID | Name | Quantities Found | Pricing Found | Coverage Status |
|----------------|------|------------------|---------------|-----------------|
| DEL-00.01 | Site Establishment Design Drawing Set | 4 drawings | None | Fallback |
| DEL-00.02 | Site Establishment Technical Specification | 2 specifications | None | Fallback |
| DEL-00.03 | Site Establishment Procedures | 3 procedures | None | Fallback |
| DEL-00.04 | Contractor's Equipment Schedule | 2 documents | None | Fallback |
| DEL-00.05 | Road Access Configuration & Security Process | 3 plans | None | Fallback |
| DEL-00.06 | Pre-Works Road Condition Survey Report | 2 documents | None | Fallback |
| DEL-00.07 | Post-Works Road Condition Survey Report | 3 documents | None | Fallback |
| DEL-00.08 | Temporary Water Supply Installation Details | 3 drawings | None | Fallback |

**Total Deliverables:** 8
**With Explicit Quotes:** 0 (0%)
**With Rate Table Pricing:** 0 (0%)
**With Fallback Pricing:** 8 (100%)

---

## Next Steps to Improve Source Coverage

1. **Obtain Employer's Requirements** (Volume 2 Part 1: General Requirements) to extract specific site establishment criteria
2. **Request vendor budgetary quotes** for:
   - Modular office trailers and welfare facilities
   - Security fencing and gates
   - Temporary electrical service and distribution
   - Temporary water supply installation
   - Road condition survey services
   - Traffic control equipment and signage
3. **Develop project rate tables** for:
   - Engineering labor rates (CAD drafting, specification writing, design review)
   - Construction labor rates (installers, equipment operators)
   - Equipment rental rates (cranes, excavators, pumps)
   - Material unit costs (fencing, pipe, electrical, signage)
4. **Add rate tables** to `_Estimates/_RateTables/` directory in standardized format

---

**Source Index Prepared By:** Estimating Agent
**Date:** 2026-01-28
**Status:** Complete (ready for pricing phase)
