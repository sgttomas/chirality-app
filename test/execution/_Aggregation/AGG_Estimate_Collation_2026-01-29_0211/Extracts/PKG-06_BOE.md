# Basis of Estimate (BOE)

## Snapshot Identification

| Field | Value |
|-------|-------|
| Snapshot ID | EST_PKG06_DRAFT_2026-01-28_2333 |
| Estimate Label | PKG06_DRAFT |
| Pricing Date | 2026-01 (January 2026 dollars) |
| Currency | CAD |
| Package Scope | PKG-06 Structural Steelwork (5 deliverables) |
| Run Status | WARNINGS |

## Currency & Conversion

- **Currency:** CAD (Canadian dollars)
- **Evidence:** Project location is Fraser Surrey Terminal, Surrey, BC, Canada (decomposition Section 1)
- **Conversion:** None required; single-currency estimate
- **Decision:** D-001 (currency selection)

## Scope Inclusions

This estimate includes the following CBS buckets for PKG-06:

| CBS | Description | Included |
|-----|-------------|----------|
| E | Engineering & Design | Yes |
| PM | Project Management / EPCM | Yes |
| P | Procurement Services | Yes |
| MAT | Equipment & Materials | Yes |
| CD | Construction Directs | Yes |
| CI | Construction Indirects | Yes |
| COM | Commissioning / Testing | Yes |
| CONT | Contingency | Yes |

### Package Scope Detail (PKG-06 Structural Steelwork)

Per decomposition (lines 238-252):
- **Discipline:** Structural
- **Scope:** Steel platforms, stairs, gangways, access structures, handrails, pipe supports
- **Deliverables (5):**
  - DEL-06.01: Structural Steel Design Drawing Set (Drawing)
  - DEL-06.02: Structural Steel Technical Specification (Specification)
  - DEL-06.03: Structural Steel Design Calculations (Calculation)
  - DEL-06.04: Structural Steel Data Sheet Package (Data Sheet)
  - DEL-06.05: Structural Steel Installation & Test Records (Record)

**Anticipated work products:**
- Platform general arrangements, stair drawings, gangway drawings, pipe rack/support drawings, handrail details
- Specifications for structural steel, handrails, and grating
- Structural calculations for platforms, pipe racks, connections
- Data sheets for gangways and grating
- QA/QC records: mill certificates, weld inspection records, galvanizing certificates

## Scope Exclusions

| Exclusion | Rationale |
|-----------|-----------|
| Foundations for platforms/pipe racks | Assumed under PKG-05 Concrete Structures (Decision D-007) |
| Owner's costs | Not in Contractor scope per decomposition Section 1.2 |
| Land acquisition | Not in Contractor scope |
| Financing costs | Not in Contractor scope |
| Permits obtained by Employer | Per decomposition Section 1.2 |
| Escalation | escalation_mode = NONE per config (Decision D-011) |
| Taxes | Excluded from base estimate |

## Contracting Assumptions

| Assumption | Value | Decision Ref |
|------------|-------|--------------|
| Contract type | Design & Build (D&B) | decomposition Section 1 |
| Contractor responsibility | Full design and construction of structural steelwork | decomposition Section 1.2 |
| Fabrication location | Off-site fabrication assumed (shop-fabricated, galvanized, delivered to site) | A-006 |
| Galvanizing | Hot-dip galvanizing assumed for corrosion protection (marine/industrial environment) | A-006, A-013 |
| Foundation coordination | Structural steel assumes foundations provided by others (PKG-05); dependency tracking NOT_TRACKED | D-007 |

## Location / Productivity Assumptions

| Assumption | Value | Decision Ref |
|------------|-------|--------------|
| Location | Fraser Surrey Terminal, 11060 Elevator Road, Surrey, BC | decomposition Section 1 |
| Productivity factor | 1.0 (BC lower mainland baseline) | D-006 |
| Site access | Assumed standard access via Elevator Road; work in active terminal environment may impose constraints | D-006, A-014 |
| Working hours | Standard 8-10 hour shifts assumed | D-006 |
| Crane availability | Mobile crane rental assumed; coordination with other trades may affect erection schedule | A-008 |
| Seasonal constraints | Fraser Surrey Terminal wet season work may affect erection productivity | Risk R-003 |
| Terminal operations continuity | Per decomposition objective OBJ-5 (Terminal Continuity): works must minimize disturbance to existing terminal operations | decomposition Section 2 |

## Pricing Sources Hierarchy

1. **Quotes/Vendor Budgets:** None available
2. **Project Rate Tables:** None provided
3. **Allowances:** All line items priced via allowances (fallback typical model)

**Decision:** D-008 — All pricing uses allowances due to absence of vendor quotes, rate tables, and detailed design drawings.

### Source Discovery Summary

| Source Type | Status | Impact on Estimate |
|-------------|--------|-------------------|
| Vendor quotes (fabrication, galvanizing, handrails, grating, gangways) | None found | All MAT items (56% of base) are allowances |
| Project rate tables (labor, equipment) | None provided | All labor/equipment rates are assumed typical BC rates |
| Design drawings with quantities (tonnage, linear footage, areas, counts) | Not yet available (deliverables INITIALIZED, TBD) | All quantities are allowances |
| Deliverable four-documents | Present for all 5 deliverables | Scope is clear; quantities are not yet defined |

**Reference:** Source_Index.md for full discovery details.

## Indirects Model

**Method:** Factor-based (fallback typical model)

**Rationale:** No project schedule, staffing plan, or time-based indirects model available; factor-based approach used to ensure runnable estimate (Decision D-009).

| Factor | Rate | Base | Formula | Amount (CAD) | Decision Ref |
|--------|------|------|---------|-------------:|--------------|
| Construction Indirects (CI) | 0.18 | CD | 0.18 × $611k | $115,000 | D-009 |
| Procurement Services (P) | 0.02 | MAT | 0.02 × $1,301k | $27,000 | D-009 |
| EPCM/PM | 0.06 | CD + CI + MAT | 0.06 × ($611k + $115k + $1,301k) | $120,000 | D-009 |
| Commissioning (COM) | 0.03 | CD + CI + MAT | 0.03 × ($611k + $115k + $1,301k) | $60,000 | D-009 |

**Construction Indirects (CI) Scope:**
- Field supervision and construction management
- Site overhead and temporary facilities (PKG-06 allocation)
- HSE support and safety programs
- QA/QC coordination and inspection oversight

**Procurement Services (P) Scope:**
- Vendor coordination and expediting
- Material inspection and receiving
- Procurement documentation

**EPCM/PM Scope:**
- Project management (PKG-06 allocation)
- Engineering management and design coordination
- Document control and review
- Interface coordination (foundations, piping, etc.)

**Commissioning (COM) Scope:**
- Load testing and structural verification
- Final inspections and punch list
- Record documentation and as-built reconciliation
- Handover preparation

**Improvement Path:** Provide project schedule with durations, staffing plan, or project-specific indirects rates in config/rate tables to replace factor-based model.

## Contingency Method

**Method:** PCT_BY_BUCKET (percentage by CBS bucket)

**Rationale:** All base estimate line items are allowance/parametric-based (100% allowance share); contingency percentages elevated above baseline to account for estimate immaturity and scope uncertainty (Decision D-010).

| CBS | Base % | Allowance Adjustment | Final % | Rationale |
|-----|--------|---------------------|---------|-----------|
| E | 10% | +10% (100% allowance) | 20% | All engineering effort is allowance-based; no design hours validation |
| MAT | 15% | +10% (100% allowance) | 25% | No vendor quotes; tonnage/quantities are allowances |
| CD | 20% | +10% (100% allowance) | 30% | No productivity data or site-specific validation; all labor allowances |
| CI | 20% | +10% (100% factor-derived) | 30% | Factor-derived from CD base (no schedule validation) |
| PM | 10% | +5% (factor-derived) | 15% | Factor-based (no staffing plan) |
| P | 10% | +5% (factor-derived) | 15% | Factor-based (no procurement plan) |
| COM | 25% | +5% (factor-derived) | 30% | Factor-based (no commissioning plan) |

**Allowance-Heavy Adjustment Formula:**
- If bucket AllowanceShare ≥ 0.50: add +0.05 (5%)
- If bucket AllowanceShare ≥ 0.80: add an additional +0.05 (total +0.10, or 10%)

Where `AllowanceShare = (ALLOWANCE+PARAMETRIC base $) / (bucket base $)`.

For PKG-06, all CBS buckets have 100% allowance/parametric share → maximum adjustment applied.

**Decision:** D-010 — Contingency rates elevated due to 100% allowance-based estimate.

**Total Contingency:** $601,000 (26% of $2,323,000 base estimate)

**Reference:** Risk_Register.md for risk-by-risk contingency justification.

## Escalation Method

- **Mode:** NONE
- **Rationale:** Pricing date is current (January 2026); no escalation applied per config default (Decision D-011)
- **Impact:** Estimate totals are in January 2026 dollars; if work occurs in future years, escalation may be required (see Risk R-007)
- **Override Path:** Set `escalation_mode: EXPLICIT` in config and provide cashflow curve or escalation factors if escalation is required

## Rounding Policy

- **Rounding:** Nearest $1,000 CAD
- **Applied to:** Summary CBS totals, contingency amounts, and final estimate total
- **Rationale:** Estimate maturity (LOW confidence, 100% allowance-based) does not support precision beyond $1,000
- **Decision:** Per _CONFIG.md default (Decision D-002)

## Completeness Metrics

| Metric | Value |
|--------|-------|
| Lines priced by QUOTE | 0% (0 of 21 lines) |
| Lines priced by RATE_TABLE | 0% (0 of 21 lines) |
| Lines priced by ALLOWANCE | 81% (17 of 21 lines) |
| Lines priced by PARAMETRIC | 19% (4 of 21 lines) |
| Deliverables with explicit quantities | 0% (0 of 5 deliverables) |
| Overall confidence | LOW |

### Confidence Assessment by CBS

| CBS | Confidence | Justification |
|-----|------------|---------------|
| E | LOW | All engineering hours are allowances without design scope validation |
| MAT | LOW | No vendor quotes; tonnage and quantities are rough allowances |
| CD | LOW | No productivity data, site-specific rates, or schedule validation |
| CI | LOW | Factor-derived from CD (no independent validation) |
| PM | MED | Factor-based but typical for EPCM allocation at this stage |
| P | MED | Factor-based but typical for procurement services allocation |
| COM | LOW | Factor-based without commissioning plan or test scope |

**Overall Confidence:** LOW (estimate suitable for preliminary budgeting; NOT suitable for procurement or commitment without refinement)

## Known Gaps

| Gap | Impact | Resolution Path |
|-----|--------|-----------------|
| No structural steel tonnage estimate | HIGH — tonnage allowance (150 t) may vary ±50%; affects $900k material cost and $356k erection labor | Provide design drawings (DEL-06.01) with member sizes/lengths or tonnage estimate from calculations (DEL-06.03) |
| No vendor quotes for fabrication/galvanizing | HIGH — $6k/tonne rate is placeholder; may vary $5k-$7.5k/tonne | Obtain budgetary quotes from 3 structural steel fabricators |
| No handrail/grating quantities | MEDIUM — linear/area allowances (400 m, 800 m²) are rough | Provide platform layout drawings showing handrail extents and grating areas |
| No stairs/gangway item list | MEDIUM — count allowance (12 items) is rough | Provide gangway data sheets (DEL-06.04) with item counts, spans, and sizes |
| No project labor rates | MEDIUM — labor rates ($95/hr, $110/hr, etc.) are assumed typical BC rates | Provide project labor rates and equipment rental rates |
| No productivity data | MEDIUM — 25 hrs/tonne erection productivity is typical range | Provide erection productivity assumptions or historical data from execution plan |
| No piping layout for pipe supports | MEDIUM — pipe support allowance ($65k) may be insufficient if piping extents are large | Provide piping general arrangements (process packages) and clarify pipe support responsibility |
| No foundation interface definition | LOW-MEDIUM — coordination risk if foundation loads/schedules not aligned | Confirm foundation scope (PKG-05) and establish interface early |

## Key Estimate Drivers and Sensitivities

### Top 3 Cost Drivers

1. **Structural steel material supply (150 tonnes @ $6k/tonne):** $900,000 (39% of base)
   - Sensitivity: ±50 tonnes → ±$300,000
   - Sensitivity: ±$1k/tonne → ±$150,000

2. **Structural steel erection labor (3,750 hrs @ $95/hr):** $356,000 (15% of base)
   - Sensitivity: ±5 hrs/tonne → ±$71,000
   - Sensitivity: ±$10/hr rate → ±$38,000

3. **Stairs and gangways (12 items @ $15k/item):** $180,000 (8% of base)
   - Sensitivity: ±4 items → ±$60,000
   - Sensitivity: ±$5k/item → ±$60,000

### Tornado Diagram (Conceptual)

If actual values differ from allowances, estimate impact:

| Parameter | Low Case | Base Case | High Case | Range Impact |
|-----------|----------|-----------|-----------|--------------|
| Steel tonnage | 100 t | 150 t | 200 t | ±$600k on MAT+CD |
| Fabrication rate | $5k/t | $6k/t | $7.5k/t | ±$225k on MAT |
| Erection productivity | 20 hrs/t | 25 hrs/t | 35 hrs/t | ±$143k on CD |
| Handrail/grating quantities | -30% | Base | +50% | ±$110k on MAT+CD |
| Stairs/gangways count | 8 items | 12 items | 16 items | ±$60k on MAT |

**Conclusion:** Structural steel tonnage and fabrication rate are the dominant sensitivities; obtaining design drawings and vendor quotes will significantly improve estimate confidence.

## Design Basis and Assumptions Summary

### Structural Steel Scope (Package-Level)

- **Platforms:** Access platforms for railcar unloading stations (32 stations assumed to require platform access)
- **Stairs:** Vertical access between platform levels and grade
- **Gangways:** Elevated walkways connecting platforms or providing access to equipment
- **Pipe racks/supports:** Structural supports for process piping (coordination with process packages)
- **Handrails:** 3-rail galvanized steel handrail system (safety barrier per code)
- **Grating:** Medium-duty industrial grating for platform walking surfaces

### Material Assumptions

- **Steel grade:** CSA G40.21 350W or equivalent (typical structural grade for industrial platforms) — **TBD** pending specification (DEL-06.02)
- **Protective system:** Hot-dip galvanizing (marine/industrial environment corrosion protection) — **TBD** pending specification
- **Handrail:** Galvanized steel, 3-rail system with posts per code — **TBD** pending specification
- **Grating:** Galvanized steel grating, medium-duty industrial rating — **TBD** pending specification and data sheets (DEL-06.04)

### Design Load Assumptions

- **Platform live loads:** Industrial access (per code; likely 4.8 kPa or higher for equipment access) — **TBD** pending calculations (DEL-06.03)
- **Wind/seismic:** Fraser Surrey, BC seismic and wind exposure — **TBD** pending calculations
- **Equipment loads:** Pipe loads, unloading arm reactions (coordination with process packages) — **TBD** pending interface definition

### Construction Assumptions

- **Fabrication:** Off-site shop fabrication assumed (higher quality, lower field labor)
- **Galvanizing:** Off-site hot-dip galvanizing after fabrication
- **Delivery:** Truck delivery to site; laydown area required (see A-014)
- **Erection:** Mobile crane erection; field bolted connections preferred (minimize field welding)
- **Field welding:** Limited field welding anticipated (connections, repairs); weld inspection per CSA W59 or equivalent
- **Site access:** Work in active terminal; coordination with terminal operations required (OBJ-5 Terminal Continuity)

## References

| Document | Description |
|----------|-------------|
| Decision_Log.md | All decisions D-001 through D-013 |
| Assumptions_Log.md | All assumptions A-001 through A-015 |
| Detail.csv | Line item detail with traceability (21 line items) |
| Summary.md | CBS totals and WBS breakdown |
| WBS_CBS_Matrix.csv | WBS × CBS mapping |
| QA_Report.md | Quality checks and completeness metrics |
| Risk_Register.md | Risk factors and contingency basis (8 risk entries) |
| Source_Index.md | Source discovery and quality assessment |
| test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md | PKG-06 scope definition (lines 238-252) |
| test/execution/PKG-06_Structural_Steelwork/1_Working/ | Deliverable folders (DEL-06.01 through DEL-06.05) |

## Estimate Limitations and Disclaimer

**This estimate is a preliminary budgeting tool only and is NOT suitable for:**
- Procurement commitments or purchase orders
- Binding quotations or contractual pricing
- Detailed cost control or cost-loaded schedules
- Tender/bid submission without further refinement

**Limitations:**
1. **No vendor quotes:** All material costs are allowances without vendor validation.
2. **No detailed design:** Structural steel tonnage, handrail/grating quantities, and stair/gangway counts are rough allowances.
3. **No project-specific rates:** Labor and equipment rates are assumed typical BC lower mainland rates without project validation.
4. **No schedule integration:** Indirects and commissioning are factor-based without schedule or staffing plan validation.
5. **No site-specific constraints:** Erection productivity assumes standard access; active terminal constraints not fully assessed.
6. **Dependencies not tracked:** Foundation interface (PKG-05), piping interface (process packages), and other cross-package coordination assumed but not validated.

**Confidence Level:** LOW (estimate maturity is conceptual/allowance-based; suitable for preliminary budgeting and planning)

**Recommended Use:**
- High-level project budgeting and financial planning
- Scope definition and design prioritization (identify areas needing early design effort)
- Risk identification and contingency allocation
- Vendor engagement planning (identify items requiring budgetary quotes)

**Next Steps to Improve Estimate:**
1. Complete structural steel design (DEL-06.01 drawings, DEL-06.03 calculations) to establish tonnages and quantities
2. Obtain vendor budgetary quotes for fabrication, galvanizing, handrails, grating, stairs/gangways
3. Provide project labor rates, productivity assumptions, and equipment rental rates
4. Establish foundation interface (PKG-05 coordination) and piping interface (process packages)
5. Develop erection schedule and site logistics plan to validate productivity assumptions

---

**BOE compiled:** 2026-01-28 23:33
**Estimating Agent:** AGENT_ESTIMATING (straight-through pipeline per AGENT_ESTIMATING.md)
**Agent Version:** 2026-01-28_v3
