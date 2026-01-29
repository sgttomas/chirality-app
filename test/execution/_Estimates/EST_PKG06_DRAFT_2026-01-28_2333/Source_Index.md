# Source Index

## Snapshot ID
EST_PKG06_DRAFT_2026-01-28_2333

## Discovery Summary

This index lists the sources discovered and evaluated for pricing and quantity extraction for PKG-06 Structural Steelwork.

## Priority 1: Explicit Pricing Sources (Vendor Quotes / Budgets)

**Status:** None found.

No vendor quotes, budgetary proposals, or purchase order summaries were discovered for structural steel fabrication, gangways, grating, handrails, or installation.

## Priority 2: Rate Tables / Cost Libraries

**Status:** None provided.

Searched locations:
- `execution/_Estimates/_RateTables/` — empty
- No project-specific rate tables found in workspace

## Priority 3: Quantity Sources (Deliverable Documents)

**Status:** Deliverable folders present; limited explicit quantities.

| Deliverable ID | Folder Path | Four Docs Present | Quantity Sources |
|----------------|-------------|-------------------|------------------|
| DEL-06.01 | execution/PKG-06_Structural_Steelwork/1_Working/DEL-06.01_Structural_Steel_Design_Drawing_Set | Yes | Drawing set scope defined (platforms, stairs, gangways, pipe racks, handrails); no drawing counts or tonnage yet |
| DEL-06.02 | execution/PKG-06_Structural_Steelwork/1_Working/DEL-06.02_Structural_Steel_Technical_Specification | Yes | Specification sections identified (structural steel, handrails, grating); no quantities |
| DEL-06.03 | execution/PKG-06_Structural_Steelwork/1_Working/DEL-06.03_Structural_Steel_Design_Calculations | Yes | Design calculations scope defined; no tonnage or member counts |
| DEL-06.04 | execution/PKG-06_Structural_Steelwork/1_Working/DEL-06.04_Structural_Steel_Data_Sheet_Package | Yes | Data sheet artifacts identified (gangways, grating); no item counts or sizes |
| DEL-06.05 | execution/PKG-06_Structural_Steelwork/1_Working/DEL-06.05_Structural_Steel_Installation_and_Test_Records | Yes | Record types identified (mill certs, weld inspection, galvanizing certs); no quantity basis |

**Key observations:**
- Deliverable scope is clear: platforms, stairs, gangways, access structures, handrails, pipe supports
- No explicit tonnages, item counts, or sizes provided in current documents
- Documents are in INITIALIZED state; quantities are TBD pending design drawings/calculations

## Priority 4: Fallback Typical Model (Used)

**Status:** Applied for all line items.

Given the absence of vendor quotes, rate tables, and explicit quantities, all cost line items are priced using allowances derived from the fallback typical model (AGENT_ESTIMATING.md: STRUCTURE, Fallback Typical Model).

**Decision Reference:** D-008 (pricing basis selection)

## Source Quality Assessment

| Source Type | Availability | Quality | Confidence Impact |
|-------------|--------------|---------|-------------------|
| Vendor quotes | None | N/A | LOW confidence for all items |
| Rate tables | None | N/A | LOW confidence for all items |
| Explicit quantities (design drawings) | Not yet available (TBD) | N/A | Unable to price by quantity × unit rate |
| Parametric/allowance fallback | Available | Placeholder only | LOW confidence (allowance-based) |

## Recommendations for Next Run

To improve estimate confidence in future iterations, provide:

1. **Structural steel fabrication drawings** showing:
   - Platform/pipe rack steel tonnage (or member sizes/lengths for takeoff)
   - Stair/gangway counts, spans, and sizes
   - Handrail linear footage by type
   - Grating areas by type and loading

2. **Vendor budgetary quotes** for:
   - Structural steel supply ($/tonne or $/kg delivered)
   - Fabrication ($/tonne fabricated)
   - Galvanizing/protective treatment ($/tonne or $/m²)
   - Handrail/grating supply and installation ($/m or $/m²)

3. **Project rate tables** including:
   - Steel erection labor productivity (hrs/tonne)
   - Labor rates ($/hr by trade)
   - Equipment rates (crane, welding, access equipment)

---

**Index compiled:** 2026-01-28 23:33
**Decision Reference:** D-001 through D-008 (see Decision_Log.md)
