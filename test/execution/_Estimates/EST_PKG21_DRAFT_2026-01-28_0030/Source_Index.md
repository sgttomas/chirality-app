# Source Index

## PKG-21: Building Structures & Envelope

**Snapshot ID:** EST_PKG21_DRAFT_2026-01-28_0030

---

## Source Discovery Summary

| Category | Sources Found | Sources Used |
|----------|---------------|--------------|
| Vendor Quotes | 0 | 0 |
| Rate Tables | 0 | 0 |
| Deliverable Documents | 6 | 6 |
| Reference Documents | 1 | 1 |
| Parametric/Industry Data | N/A | Primary basis |

---

## Primary Pricing Sources

### Tier 1: Explicit Pricing (None Found)

No vendor quotes, budgetary quotes, or explicit pricing documents were found in the workspace for PKG-21.

**Search Locations:**
- `execution/PKG-21_Building_Structures_and_Envelope/` — No pricing files
- `execution/_Estimates/_RateTables/` — Empty or no building-specific rates
- Deliverable `_REFERENCES.md` files — No pricing references

---

### Tier 2: Rate Tables (None Found)

No project-specific rate tables available for building construction.

**Search Locations:**
- `execution/_Estimates/_RateTables/` — No building rate tables

---

### Tier 3: Quantity Sources (Deliverable Documents)

| Source | Path | Content Used |
|--------|------|--------------|
| DEL-21.01 Datasheet | `PKG-21_.../DEL-21.01_.../Datasheet.md` | Building scope, MCC building assumptions, operator shelter assumptions |
| DEL-21.02 Datasheet | `PKG-21_.../DEL-21.02_.../Datasheet.md` | Specification scope, material categories |
| DEL-21.03 Datasheet | `PKG-21_.../DEL-21.03_.../Datasheet.md` | Calculation scope, structural/foundation assumptions |
| DEL-21.04 Datasheet | `PKG-21_.../DEL-21.04_.../Datasheet.md` | Data sheet scope |
| DEL-21.05 Datasheet | `PKG-21_.../DEL-21.05_.../Datasheet.md` | QA/QC records scope, testing requirements |
| DEL-21.06 Datasheet | `PKG-21_.../DEL-21.06_.../Datasheet.md` | Shop drawing scope |
| DEL-21.01 Specification | `PKG-21_.../DEL-21.01_.../Specification.md` | Building requirements, code references |

---

### Tier 4: Parametric/Industry Data (Primary Basis)

All pricing is based on parametric estimating using industry benchmarks. Sources include:

| Benchmark | Application | Confidence |
|-----------|-------------|------------|
| PEMB industry pricing ($600-$1,200/m²) | MCC building supply | LOW |
| Prefab shelter pricing ($35,000-$65,000/unit) | Operator shelters | LOW |
| Engineering % of construction (8-15%) | Design services | LOW |
| BC union construction rates | Labor pricing | LOW |
| Fallback Typical Model factors | Indirects, PM, contingency | LOW |

**Note:** Parametric data is based on general industry knowledge for industrial building construction in British Columbia. No project-specific validation available.

---

## Reference Documents

### Decomposition Document

| Document | Path | Sections Used |
|----------|------|---------------|
| Canola Oil Transload Facility Decomposition | `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md` | Lines 503-519 (PKG-21 definition), Line 507 (scope), Lines 512-518 (deliverables) |

### Employer's Requirements (Not Accessed)

| Document | Path | Status |
|----------|------|--------|
| ER Volume 2 Part 3: Building Works | `.../test/Volume_2_Part_3_Employers_Requirements.pdf` | NOT ACCESSED per user instruction |

**Note:** ER Volume 2 Part 3 likely contains project-specific building requirements that could improve estimate accuracy. Access requires user authorization.

---

## Source Priority Used

Per AGENT_ESTIMATING.md (Phase 3.3: Price Line Items):

1. **QUOTE** — Not available (0 items)
2. **RATE_TABLE** — Not available (0 items)
3. **ALLOWANCE** — Used for scope-specific items (21 items)
4. **PARAMETRIC** — Used for factor-based items (5 items)

---

## Recommendations for Improved Sources

| Priority | Action | Expected Benefit |
|----------|--------|------------------|
| 1 | Obtain PEMB supplier budget quotes | Replace parametric with QUOTE; reduce MAT contingency |
| 2 | Obtain erection subcontractor budgets | Replace parametric with QUOTE; reduce CD contingency |
| 3 | Obtain prefab shelter supplier quotes | Replace parametric with QUOTE |
| 4 | Access ER Volume 2 Part 3 | Confirm building requirements and features |
| 5 | Add building rate tables to _RateTables/ | Improve consistency across packages |
| 6 | Confirm MCC building size | Reduce primary quantity uncertainty |

---

**Prepared by:** ESTIMATING Agent
**Date:** 2026-01-28
