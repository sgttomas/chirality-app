# Source Index — PKG-08 Marine Structures Estimate

**Snapshot ID:** EST_PKG08_DRAFT_2026-01-28_2400
**Date:** 2026-01-28

---

## Purpose

This index lists all sources discovered and used (or not used) during the estimating process for PKG-08 Marine Structures, organized by priority per Protocol Phase 2.2.

---

## 1. Explicit Pricing Sources (Highest Priority)

**Status:** None found

### Vendor Quotes
- **Searched:** Deliverable `_REFERENCES.md` files, workspace `/Users/ryan/ai-env/projects/chirality-app/test/execution/PKG-08_Marine_Structures/`
- **Found:** None
- **Usage:** Not used

### Budgetary Quotes
- **Searched:** Workspace and prior estimate folders
- **Found:** None
- **Usage:** Not used

### Proposals / Budget Sheets
- **Searched:** Workspace
- **Found:** None
- **Usage:** Not used

### PO Summaries
- **Searched:** Workspace
- **Found:** None
- **Usage:** Not used

---

## 2. Rate Tables / Cost Libraries

**Status:** None found

### Project Rate Tables
- **Searched:** `/Users/ryan/ai-env/projects/chirality-app/test/execution/_Estimates/_RateTables/`
- **Found:** Empty directory (no rate tables)
- **Usage:** Not used

### Industry Rate Tables
- **Searched:** Workspace
- **Found:** None
- **Usage:** Not used

### Unit Cost Libraries
- **Searched:** Workspace
- **Found:** None
- **Usage:** Not used

---

## 3. Quantity Sources

**Status:** No explicit quantities available

### Deliverable Datasheets
- **Searched:** All 11 deliverable folders under `PKG-08_Marine_Structures/1_Working/`
  - DEL-08.01 through DEL-08.11 `Datasheet.md` files
- **Found:** All datasheets at INITIALIZED state; all quantities marked TBD
- **Usage:** Reviewed for scope understanding; no quantities extracted

### Deliverable Specifications
- **Searched:** All 11 deliverable folders `Specification.md` files
- **Found:** All specifications at INITIALIZED state; requirements TBD pending ER extraction
- **Usage:** Reviewed for scope understanding; no quantities extracted

### Deliverable Guidance/Procedures
- **Searched:** All 11 deliverable folders `Guidance.md` and `Procedure.md` files
- **Found:** Process and methodology content; no quantities
- **Usage:** Reviewed for understanding engineering effort; no quantities extracted

---

## 4. Design Basis Documents

**Status:** Referenced but not yet extracted

### Employer's Requirements (ER)
- **Location:**
  - `/Users/ryan/ai-env/projects/chirality-app/test/Volume_2_Part_1_Employers_Requirements.pdf`
  - `/Users/ryan/ai-env/projects/chirality-app/test/Volume_2_Part_2_Employers_Requirements.pdf`
  - `/Users/ryan/ai-env/projects/chirality-app/test/Volume_2_Part_3_Employers_Requirements.pdf`
- **Status:** Present in repo; content not extracted; clause locations TBD
- **Usage:** Not used (ER extraction required to obtain design requirements, vessel data, environmental data, codes/standards)

### Project Decomposition
- **Location:** `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md`
- **Status:** Reviewed
- **Usage:** Used for PKG-08 scope definition (lines 275-291), deliverable list (11 deliverables), anticipated artifacts
- **Reference:** Decomposition defines scope as "piling, access trestle, loading platform structure, catwalk, abutments"

### Deliverable _CONTEXT.md Files
- **Location:** Each deliverable folder under `PKG-08_Marine_Structures/1_Working/`
- **Status:** Reviewed (11 deliverables)
- **Usage:** Used for deliverable identity, parent package, lifecycle state verification

---

## 5. Prior Estimates (Reference)

**Status:** Reviewed for pricing patterns

### PKG-00 Site Establishment
- **Location:** `/Users/ryan/ai-env/projects/chirality-app/test/execution/_Estimates/EST_PKG00_DRAFT_2026-01-28_2315/`
- **Usage:** Reviewed for engineering deliverable allowance sizing patterns

### PKG-01 Demolition & Removals
- **Location:** `/Users/ryan/ai-env/projects/chirality-app/test/execution/_Estimates/EST_PKG01_DRAFT_2026-01-28_2330/`
- **Usage:** Reviewed for:
  - Engineering deliverable allowance sizing (drawings, specs, procedures, records)
  - Construction directs allowance sizing patterns
  - Indirects/PM/P factors (18% CI, 6% PM, 2% P)
  - Contingency methodology (25% for high-allowance packages)
  - Detail.csv format and BOE structure

### PKG-02 Earthworks & Ground Improvement
- **Location:** `/Users/ryan/ai-env/projects/chirality-app/test/execution/_Estimates/EST_PKG02_DRAFT_2026-01-28_2330/`
- **Usage:** Reviewed for civil/geotechnical deliverable allowance sizing

---

## 6. Fallback Typical Model (Used)

**Status:** Used for 100% of pricing

### Fallback Model Source
- **Location:** AGENT_ESTIMATING.md (Fallback Typical Model, lines 645-714)
- **Usage:** Used for:
  - Indirects/services factors (CI=18%, PM=6%, P=2%, COM=3%)
  - Contingency method (PCT_BY_BUCKET with allowance-heavy adjustment)
  - Allowance sizing guidance (placeholder allowances when no explicit quantities)

### Industry-Typical Rates (Embedded Knowledge)
- **Source:** Marine construction industry-typical unit rates (embedded in agent knowledge)
- **Usage:** Used for allowance sizing:
  - Marine piling supply: ~$850/tonne FOB
  - Marine structural steel fabricated: ~$4,500-$5,625/tonne FOB with marine-grade coatings
  - Marine piling installation: ~$13,000/pile installed (including marine crane/barge, driving, testing)
  - Marine steel erection: ~$2,800-$3,400/tonne installed (including marine crane/barge, welding/bolting)
  - Concrete abutments: ~$1,200/m³ materials (concrete, rebar, formwork)

**Confidence:** LOW (industry-typical rates, not project-specific)

---

## 7. Configuration

### Estimate Config
- **Location:** `/Users/ryan/ai-env/projects/chirality-app/test/execution/_Estimates/_CONFIG.md`
- **Status:** Reviewed
- **Usage:** Used for:
  - Currency: CAD
  - Pricing date: 2026-01
  - Rounding: 1000 (nearest $1,000)
  - Contingency method: PCT_BY_BUCKET
  - Escalation mode: NONE
  - Include scopes: E, PM, P, MAT, CD, CI, COM
  - Exclude scopes: Owner's costs, land, financing, permits (Employer-responsible)

---

## 8. Sources Not Available (Gaps)

The following sources would significantly improve estimate accuracy but are not available:

1. **Marine geotechnical investigation report** (DEL-08.04)
   - Required for: Pile type, size, quantity, embedment depth, capacity

2. **Design drawings** (DEL-08.01)
   - Required for: Trestle/platform geometry, steel tonnages, pile layout

3. **Design vessel characteristics and berthing/mooring data**
   - Required for: Berthing energy, mooring loads, structural loading

4. **Marine environmental data** (wind, current, wave, water levels, seismic)
   - Required for: Environmental design loads, current assessment

5. **Equipment loads from PKG-09 and PKG-11**
   - Required for: Fender/bollard reactions, loading arm loads, equipment support design

6. **Vendor budgetary quotes**
   - Required for: Marine piling supply, structural steel supply, marine contractor installation

7. **Project-specific rate tables**
   - Required for: Unit rates for marine construction labor, equipment, materials

---

## 9. Pricing Source Summary

| Source Type | Priority | Available | Usage | % of Estimate |
|-------------|----------|-----------|-------|---------------|
| Vendor Quotes | 1 | No | Not used | 0% |
| Rate Tables | 2 | No | Not used | 0% |
| Historical Data | 3 | No | Not used | 0% |
| Fallback Model | 4 | Yes | Used | 100% |

**Conclusion:** No project-specific pricing sources available. Estimate is 100% Allowance/Parametric based on Fallback Typical Model and industry-typical unit rates.

**Recommendation:** Prioritize obtaining vendor budgetary quotes and populating `_RateTables/` to improve pricing accuracy in next estimate iteration.

---

**END OF SOURCE INDEX**
