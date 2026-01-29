# Source Index

## Snapshot: EST_PKG19_DRAFT_2026-01-28_0015

This index documents pricing and quantity sources discovered for PKG-19 Control Systems estimate.

---

## Source Discovery Results

### 1. Explicit Pricing Sources (Highest Priority)

| Source Type | Files Found | Status |
|-------------|-------------|--------|
| Vendor quotes | 0 | NOT FOUND |
| Budgetary proposals | 0 | NOT FOUND |
| Purchase orders | 0 | NOT FOUND |
| Budget sheets | 0 | NOT FOUND |

**Result:** No explicit pricing sources found for control systems.

---

### 2. Rate Tables / Cost Libraries

| Location Searched | Files Found | Status |
|-------------------|-------------|--------|
| `_Estimates/_RateTables/` | 0 | NOT FOUND |
| Workspace `*rate*` files | 0 | NOT FOUND |
| Workspace `*cost*` files | 0 | NOT FOUND |
| Workspace `*pricing*` files | 0 | NOT FOUND |

**Result:** No rate tables or cost libraries found.

---

### 3. Quantity Sources

| Source | Location | Content | Used For |
|--------|----------|---------|----------|
| Decomposition | `/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md` | PKG-19 scope description | System scope definition |
| DEL-19.01 Datasheet | `PKG-19.../DEL-19.01.../Datasheet.md` | System attributes, capacity parameters | I/O drivers, facility scope |
| DEL-19.02 Specification | `PKG-19.../DEL-19.02.../Specification.md` | Functional requirements, performance criteria | System requirements |
| DEL-19.03 Datasheet | `PKG-19.../DEL-19.03.../Datasheet.md` | Equipment categories | Equipment list structure |
| DEL-19.04 Datasheet | `PKG-19.../DEL-19.04.../Datasheet.md` | Software scope | Software scope definition |

**Result:** Quantity sources found but contain **TBD** values; quantities estimated parametrically.

---

### 4. Fallback Typical Model (Used)

Due to absence of explicit pricing sources, the **Fallback Typical Model** was applied per AGENT_ESTIMATING.md STRUCTURE section.

| Application | Method | Confidence |
|-------------|--------|------------|
| DCS/PLC system pricing | ALLOWANCE | LOW |
| I/O module pricing | ALLOWANCE | LOW |
| HMI workstation pricing | ALLOWANCE | LOW |
| Network equipment pricing | ALLOWANCE | LOW |
| Engineering effort | ALLOWANCE | LOW |
| Indirects factors | PARAMETRIC (fallback model) | LOW |
| Contingency factors | PARAMETRIC (fallback model) | LOW |

---

## Reference Documents

### Project Documents

| Document | Path | Content Used |
|----------|------|--------------|
| Decomposition | `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md` | PKG-19 scope, deliverables, objectives |
| _CONFIG.md | `/Users/ryan/ai-env/projects/chirality-app/test/execution/_Estimates/_CONFIG.md` | Currency (CAD), pricing date, rounding |
| _LATEST.md | `/Users/ryan/ai-env/projects/chirality-app/test/execution/_Estimates/_LATEST.md` | Previous estimate reference |

### Deliverable Documents

| Document | Path | Content Used |
|----------|------|--------------|
| DEL-19.01 Datasheet | `.../DEL-19.01.../Datasheet.md` | System scope, capacity parameters |
| DEL-19.02 Specification | `.../DEL-19.02.../Specification.md` | Requirements basis |
| DEL-19.03 Datasheet | `.../DEL-19.03.../Datasheet.md` | Equipment categories |
| DEL-19.04 Datasheet | `.../DEL-19.04.../Datasheet.md` | Software scope |

---

## Pricing Source Priority Applied

Per AGENT_ESTIMATING.md PROTOCOL Phase 3.3:

1. **QUOTE** — Not available (0 line items)
2. **RATE_TABLE** — Not available (0 line items)
3. **ALLOWANCE** — Used for all material line items (26 line items)
4. **PARAMETRIC** — Used for derived costs (4 line items: PM, P, CI from fallback factors)

---

## Recommendations to Improve Pricing Basis

| Action | Impact | Priority |
|--------|--------|----------|
| Obtain DCS/PLC vendor budgetary quotes | Firm up 50% of MAT cost | HIGH |
| Obtain historian vendor pricing | Firm up historian costs | MEDIUM |
| Complete I/O list (PKG-20) | Firm up I/O module count | HIGH |
| Add control system rate tables to `_RateTables/` | Enable RATE_TABLE pricing | MEDIUM |

---

## Source Files Created This Run

| File | Purpose |
|------|---------|
| BOE.md | Basis of Estimate |
| Summary.md | Executive summary |
| Detail.csv | Line item detail |
| Decision_Log.md | Decision record |
| Assumptions_Log.md | Assumption record |
| Risk_Register.md | Risk record |
| QA_Report.md | Quality checks |
| Source_Index.md | This file |
| WBS_CBS_Matrix.csv | WBS-CBS mapping |
