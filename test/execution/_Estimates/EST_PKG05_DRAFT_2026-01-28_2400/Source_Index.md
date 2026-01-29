# Source Index — PKG-05 Concrete Structures Estimate

**Snapshot ID:** EST_PKG05_DRAFT_2026-01-28_2400
**Package Scope:** PKG-05 Concrete Structures
**Date:** 2026-01-28

---

## Source Discovery Summary

This index documents the pricing and quantity sources discovered during estimate preparation.

**Discovery Outcome:** No project-specific pricing sources found. Fallback typical model used per Decision D-005.

---

## 1. Explicit Pricing Sources (Highest Priority)

### 1.1 Vendor Quotes / Budgetary Proposals

| Source Type | Files Found | Status |
|-------------|-------------|--------|
| Concrete supplier quotes | 0 | NOT FOUND |
| Rebar fabricator quotes | 0 | NOT FOUND |
| Formwork system quotes | 0 | NOT FOUND |
| Testing lab quotes | 0 | NOT FOUND |
| Subcontractor proposals | 0 | NOT FOUND |

**Search Locations:**
- `/Users/ryan/ai-env/projects/chirality-app/test/execution/PKG-05_Concrete_Structures/1_Working/*/` — no pricing documents found
- Deliverable `_REFERENCES.md` files — reference only decomposition document

**Impact:** All material and installation costs must use fallback allowances.

---

### 1.2 Historical Project Data

| Source Type | Files Found | Status |
|-------------|-------------|--------|
| Similar project estimates | 0 | NOT FOUND |
| Benchmarking data | 0 | NOT FOUND |
| Cost database extracts | 0 | NOT FOUND |

**Impact:** Cannot benchmark estimate against historical projects.

---

## 2. Rate Tables / Cost Libraries

### 2.1 Project Rate Tables

| Location | Files Found | Status |
|----------|-------------|--------|
| `_Estimates/_RateTables/` | 0 | EMPTY DIRECTORY |

**Search Results:**
- Directory exists but contains no rate table files
- No CSV, XLSX, or MD rate tables found

**Impact:** Must use fallback parametric rates for all line items.

---

### 2.2 Industry Cost Data

| Source Type | Available | Status |
|-------------|-----------|--------|
| RS Means data | No | NOT INTEGRATED |
| Richardson data | No | NOT INTEGRATED |
| Local cost indices | No | NOT FOUND |

**Impact:** Fallback rates based on typical EPC experience rather than published cost data.

---

## 3. Quantity Sources

### 3.1 Deliverable Documents — PKG-05

| Deliverable | Document | Quantities Found | Status |
|-------------|----------|------------------|--------|
| DEL-05.01 | Datasheet.md | Drawing counts (estimated 22 sheets) | PARTIAL |
| DEL-05.01 | Specification.md | No physical quantities | TBD |
| DEL-05.02 | Datasheet.md | Specification counts (3 specs) | PARTIAL |
| DEL-05.03 | Datasheet.md | Calculation scope (5 calc types) | PARTIAL |
| DEL-05.04 | N/A | Record types only | TBD |

**Quantity Extraction Results:**
- **Extracted:** Artifact counts (drawings, specifications, calculations)
- **Not Extracted:** Concrete volumes, rebar weights, formwork areas, thrust block counts

---

### 3.2 Project Parameters — Quantity Derivation Basis

| Parameter | Value | Source |
|-----------|-------|--------|
| Storage capacity | 45,000 MT | Decomposition line 41 |
| Tank count | 3 tanks | Decomposition line 41 |
| Tank capacity (each) | 15,000 MT | Decomposition line 41 |
| Product | CSD canola oil | Decomposition line 43 |
| Product SG (assumed) | 0.92 | Typical canola oil density |
| Tank volume (each) | ~16,300 m³ | Derived (15,000 MT ÷ 0.92) |
| Tank diameter (assumed) | ~32m | Typical API 650 tank for volume |

**Usage:** Parameters used to derive tank foundation and containment wall quantities parametrically (see A-005, A-006).

---

### 3.3 Adjacent Package Inputs

| Package | Input Needed | Available | Status |
|---------|--------------|-----------|--------|
| PKG-02 | Geotechnical parameters | No | TBD — foundation sizing affected |
| PKG-03 | Underground utilities clash | No | TBD — thrust block locations |
| PKG-10 | Equipment loads (railcar unloading) | No | TBD — pad sizing |
| PKG-11 | Equipment loads (marine loading) | No | TBD — pad sizing |
| PKG-13 | Tank anchor/nozzle loads | No | TBD — foundation interface |
| PKG-14 | Pipe thrust loads | No | TBD — thrust block sizing |
| PKG-15 | Pump loads | No | TBD — pad sizing |

**Impact:** Equipment pad and thrust block quantities are highly uncertain without interface inputs.

---

## 4. Fallback Sources Used

### 4.1 Fallback Typical Model (AGENT_ESTIMATING Embedded)

**Applied Components:**

| Component | Application | Reference |
|-----------|-------------|-----------|
| Indirects factors | CI = 18% of CD; PM = 6% of (CD+CI+MAT); P = 2% of MAT | D-006 |
| Contingency rates | 10-25% by CBS with allowance adjustment | D-008 |

---

### 4.2 Parametric Derivations

| Quantity | Derivation Method | Confidence |
|----------|-------------------|------------|
| Tank foundation volume | Ring wall dimensions from typical 32m tank | LOW |
| Containment wall volume | 110% tank volume containment requirement | LOW |
| Equipment pad volume | Typical pad sizes for equipment types | LOW |
| Reinforcing steel | kg/m³ ratios by element type | LOW |
| Formwork area | Wall surface area calculation | LOW |

---

### 4.3 Unit Rate Assumptions (Fallback)

| Item | Unit | Rate (CAD) | Basis |
|------|------|------------|-------|
| Ready-mix concrete (standard) | m³ | $220 | Typical BC Lower Mainland pricing |
| Ready-mix concrete (containment grade) | m³ | $240 | Premium for low-permeability mix |
| Concrete placement (slab/foundations) | m³ | $180 | Typical installation cost |
| Concrete placement (walls) | m³ | $350 | Complex formwork, waterstops |
| Reinforcing steel (fabricated, delivered) | kg | $2.00 | Typical rebar supply pricing |
| Reinforcing steel (installed) | kg | $1.00 | Typical placement cost |
| Formwork (rental + installation) | m² | $90 | Combined rate for wall forms |
| Engineering drawings | sheet | $3,500-$4,500 | Typical structural drafting |
| Specifications | each | $12,000-$20,000 | Typical technical writing |
| Design calculations | package | $10,000-$45,000 | By complexity |

**Source:** Fallback typical model per Decision D-005; typical EPC project experience; BC construction market context.

---

## 5. Source Quality Assessment

### 5.1 Source Availability by Line Item Type

| Line Item Type | Source Type | % of Base Cost | Confidence |
|----------------|-------------|----------------|------------|
| Engineering deliverables | ALLOWANCE | 14% | LOW |
| Materials | ALLOWANCE | 42% | LOW |
| Construction directs | ALLOWANCE | 32% | LOW |
| Indirects (factor-based) | PARAMETRIC | 12% | MED |

---

### 5.2 Recommendations to Improve Source Quality

**Priority 1 — High Impact:**
1. **Obtain concrete supplier budgetary quote** — ready-mix pricing for project location
2. **Obtain rebar fabricator budgetary quote** — fabricated rebar supply pricing
3. **Develop dimensioned QTO** — from DEL-05.01 once developed to 30% maturity

**Priority 2 — Medium Impact:**
4. **Obtain formwork system quote** — rental/purchase options for containment walls
5. **Obtain testing lab quote** — cylinder testing, field testing services
6. **Establish engineering labor rates** — internal rates for design/drafting

**Priority 3 — Interface Inputs:**
7. **Coordinate with PKG-02** — geotechnical parameters for foundation design
8. **Coordinate with PKG-10/11/15** — equipment loads for pad sizing
9. **Coordinate with PKG-14** — piping loads for thrust block sizing

---

## 6. Data Gap Summary

| Gap Category | Gap Description | Impact | Mitigation |
|--------------|-----------------|--------|------------|
| Pricing | No vendor quotes | HIGH | Allowances with wide ranges |
| Quantities | No dimensioned drawings | HIGH | Parametric derivation |
| Geotechnical | Foundation conditions unknown | MED | Assumed ring wall type |
| Interfaces | Equipment loads unknown | MED | Typical equipment pad sizes |
| Schedule | Construction duration unknown | LOW | Factor-based indirects |

---

**Source Index Prepared By:** Estimating Agent
**Date:** 2026-01-28
**Status:** Complete
