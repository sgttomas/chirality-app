# Source Index — PKG-01 Demolition & Removals Estimate

**Snapshot ID:** EST_PKG01_DRAFT_2026-01-28_2330
**Package Scope:** PKG-01 Demolition & Removals
**Date:** 2026-01-28

---

## Source Discovery Summary

| Source Type | Count Found | Status |
|-------------|-------------|--------|
| Vendor Quotes | 0 | None discovered |
| Budgetary Proposals | 0 | None discovered |
| Rate Tables | 0 | `_RateTables/` empty |
| Historical Data | 0 | None discovered |
| Deliverable Documents | 16 | 4 deliverables × 4 docs |

**Overall Pricing Basis:** Fallback Typical Model (100% allowance-based)

---

## 1. Explicit Pricing Sources (Highest Priority)

### Status: NONE FOUND

No vendor quotes, budgetary quotes, proposals, or budget sheets were discovered in:
- PKG-01 deliverable folders (`1_Working/DEL-01.*/`)
- Deliverable `_REFERENCES.md` files
- `_Estimates/_RateTables/` directory

**Recommended Sources to Obtain:**
1. **Demolition contractor budgetary quote** — for Track 6 rail removal and general site demolition
2. **Marine contractor budgetary quote** — for Dolphin 2 marine structure removal (barge, crane, marine crew)
3. **Hazardous materials survey and abatement quote** — if survey identifies asbestos, lead, or contaminated materials
4. **Disposal facility quotes** — for demolition waste disposal (concrete, steel, rail materials)

---

## 2. Rate Tables / Cost Libraries

### Status: NONE FOUND

Searched locations:
- `_Estimates/_RateTables/` — directory exists but is empty
- PKG-01 deliverable folders — no rate tables discovered

**Recommended Rate Tables:**
1. **Civil demolition rates** — $/LF rail track, $/SF structure, $/LF fencing
2. **Marine demolition rates** — $/ea pile removal, $/SF marine deck
3. **Disposal rates** — $/ton concrete disposal, $/ton steel recycling, $/ton rail material

---

## 3. Quantity Sources (Deliverable Documents)

### DEL-01.01 Demolition Design Drawing Set

| Document | Quantity Data Found | Confidence |
|----------|---------------------|------------|
| Datasheet.md | Demolition scope items listed (Track 6, Dolphin 2, fencing, salt tent) | MED |
| Specification.md | Drawing types listed (demolition plans, sequence drawings, disposal plans) | MED |
| Guidance.md | No explicit quantities | LOW |
| Procedure.md | No explicit quantities | LOW |

**Quantities Extracted:** None explicit. Demolition scope items identified qualitatively.

**Missing Quantities (Critical for Pricing):**
- Track 6: Linear feet of track, number of ties, ballast volume
- Dolphin 2: Number of piles, deck area, structural weight
- Fencing: Linear feet, fence type/height
- Salt tent: Building footprint, structure type, foundation type

### DEL-01.02 Demolition Technical Specification

| Document | Quantity Data Found | Confidence |
|----------|---------------------|------------|
| Datasheet.md | Specification sections listed | MED |
| Specification.md | Requirements defined (no quantities) | MED |
| Guidance.md | No explicit quantities | LOW |
| Procedure.md | No explicit quantities | LOW |

**Quantities Extracted:** None explicit.

### DEL-01.03 Demolition Procedures

| Document | Quantity Data Found | Confidence |
|----------|---------------------|------------|
| Datasheet.md | Procedure types listed | MED |
| Specification.md | Requirements for procedures | MED |
| Guidance.md | No explicit quantities | LOW |
| Procedure.md | No explicit quantities | LOW |

**Quantities Extracted:** None explicit. Procedure scope confirms 4+ separate procedures required.

### DEL-01.04 Demolition Installation & Test Records

| Document | Quantity Data Found | Confidence |
|----------|---------------------|------------|
| Datasheet.md | Record types listed | MED |
| Specification.md | Record requirements defined | MED |
| Guidance.md | No explicit quantities | LOW |
| Procedure.md | No explicit quantities | LOW |

**Quantities Extracted:** None explicit.

---

## 4. Fallback Typical Model (Applied)

Due to absence of project-specific pricing sources (D-013), the following fallback basis is applied:

### Engineering Allowances
- Drawing production: Based on typical civil demolition drawing effort
- Specification writing: Based on typical specification development hours
- Procedure development: Based on typical HSE procedure development effort
- QA/QC documentation: Based on typical record preparation effort

### Construction Directs Allowances
- **Track 6 demolition:** Allowance sized for rail infrastructure removal (moderate complexity)
- **Dolphin 2 demolition:** Allowance sized for marine structure removal (high complexity, marine equipment)
- **Fencing removal:** Allowance sized for simple fencing removal (low complexity)
- **Salt tent demolition:** Allowance sized for building structure removal (moderate complexity)

### Indirects Factors
- CI = 18% of CD (per D-017, fallback model)
- PM = 6% of (CD + CI + MAT) (per D-017, fallback model)
- P = 2% of MAT (per D-017, fallback model)

All fallback model applications are recorded in Assumptions_Log.md with A-### identifiers.

---

## 5. Reference Documents (Not Pricing Sources)

The following documents provide context but not pricing data:

| Document | Location | Use |
|----------|----------|-----|
| Decomposition | `/Users/ryan/.../Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md` | Scope definition |
| ER Vol 2 Part 1 | `/Users/ryan/.../Volume_2_Part_1_Employers_Requirements.pdf` | Requirements (not read for estimate) |
| ER Vol 2 Part 2 | `/Users/ryan/.../Volume_2_Part_2_Employers_Requirements.pdf` | Requirements (not read for estimate) |
| ER Vol 2 Part 3 | `/Users/ryan/.../Volume_2_Part_3_Employers_Requirements.pdf` | Requirements (not read for estimate) |

---

## Source Discovery Actions Taken

1. Read all 4 deliverable `_CONTEXT.md` files — scope confirmed
2. Read all 4 deliverable `Datasheet.md` files — no explicit quantities
3. Read all 4 deliverable `Specification.md` files — no explicit quantities
4. Checked `_Estimates/_RateTables/` — empty
5. Checked deliverable `_REFERENCES.md` files — no pricing references

---

**Source Discovery Complete.**

**Pricing Basis:** 100% Fallback Typical Model (Allowance/Parametric)
**Confidence:** LOW
**Action Required:** Obtain vendor quotes and site-specific quantities to improve estimate accuracy.
