# Source Index

## Snapshot Identification

| Field | Value |
|-------|-------|
| Snapshot ID | EST_PKG03_DRAFT_2026-01-28_2330 |
| Package | PKG-03 Underground Utilities & Drainage |
| Date | 2026-01-28 |

## Source Discovery Summary

| Source Type | Count | Priority | Notes |
|-------------|-------|----------|-------|
| Explicit pricing sources | 0 | Highest | No vendor quotes or budgetary proposals available |
| Rate tables | 0 | High | No project rate tables found in _RateTables/ |
| Quantity sources | 6 | Medium | All 6 deliverables in INITIALIZED status; quantities TBD |
| Fallback typical model | Used | Fallback | Applied for all line items |

## Deliverables Inventory (PKG-03)

All deliverables located under `/Users/ryan/ai-env/projects/chirality-app/test/execution/PKG-03_Underground_Utilities_and_Drainage/1_Working/`:

| Deliverable ID | Name | Type | Status | 4-Doc Set | Quantities Available |
|----------------|------|------|--------|-----------|---------------------|
| DEL-03.01 | Underground Utilities Design Drawing Set | Drawing | INITIALIZED | Complete | TBD (awaiting design development) |
| DEL-03.02 | Underground Utilities Technical Specification | Specification | INITIALIZED | Complete | TBD (awaiting design development) |
| DEL-03.03 | Underground Utilities Design Calculations | Calculation | INITIALIZED | Complete | TBD (awaiting calculation execution) |
| DEL-03.04 | Underground Utilities Data Sheet Package | Data Sheet | INITIALIZED | Complete | TBD (awaiting equipment selection) |
| DEL-03.05 | Underground Utilities Installation & Test Records | Record | INITIALIZED | Complete | TBD (construction phase deliverable) |
| DEL-03.06 | CCTV Survey Report – Storm Pipes & Culverts | Report | INITIALIZED | Complete | TBD (post-installation deliverable) |

## Pricing Source Details

### 1. Explicit Pricing Sources (None Available)

No vendor quotes, budgetary proposals, or purchase orders found for PKG-03 scope.

**Decision:** D-008 — All pricing uses allowances due to absence of vendor quotes or rate tables.

### 2. Rate Tables (None Available)

No project-specific rate tables found in `/Users/ryan/ai-env/projects/chirality-app/test/execution/_Estimates/_RateTables/`.

**Decision:** D-009 — Indirects and services priced via factor-based fallback model.

### 3. Quantity Sources (6 Deliverables)

All PKG-03 deliverables provide scope definition and anticipated artifacts but contain TBD placeholders for specific quantities:

- **DEL-03.01 Datasheet** describes storm drainage system, OWS layout, duct banks, trenchless crossings but pipe lengths/sizes/counts are TBD pending design development.
- **DEL-03.02 Datasheet** describes material specifications and performance requirements but material quantities are TBD pending drawing takeoff.
- **DEL-03.03 Datasheet** describes calculation types (hydraulic, OWS sizing, duct bank capacity, trenchless structural) but specific design parameters and results are TBD pending calculation execution.
- **DEL-03.04 Datasheet** describes equipment data sheets (OWS, pipes, instrumentation, pumps) but equipment counts and capacities are TBD pending equipment selection.
- **DEL-03.05 Datasheet** describes testing scope (pressure testing, CCTV, as-built survey, OWS performance verification) but test quantities are TBD pending construction planning.
- **DEL-03.06 Datasheet** describes CCTV survey report scope but pipe lengths and inspection extent are TBD pending as-built conditions.

### 4. Fallback Typical Model (Applied)

Since no explicit pricing sources, rate tables, or explicit quantities are available, all line items are priced using the fallback typical model defined in AGENT_ESTIMATING.md STRUCTURE section.

**Method:** ALLOWANCE (lump-sum allowances sized based on typical scope for underground utilities package)

**Confidence:** LOW (all allowances pending design quantities and vendor pricing)

**Decision:** D-010 — Allowance sizing uses engineering judgment based on typical underground utilities scope for canola oil transload facility (storm drainage for 45,000 MT storage + railcar unloading areas, OWS for containment, duct banks for electrical/comms, trenchless crossings for rail/road crossings).

## Reference Documents Reviewed

| Document | Path | Content Used |
|----------|------|--------------|
| Decomposition | /Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md | PKG-03 scope definition, deliverables list, objectives mapping |
| DEL-03.01 Datasheet | PKG-03_Underground_Utilities_and_Drainage/1_Working/DEL-03.01.../Datasheet.md | Storm drainage, OWS, duct banks, trenchless crossings scope |
| DEL-03.01 Specification | PKG-03_Underground_Utilities_and_Drainage/1_Working/DEL-03.01.../Specification.md | Drawing set requirements and artifacts |
| DEL-03.02 Datasheet | PKG-03_Underground_Utilities_and_Drainage/1_Working/DEL-03.02.../Datasheet.md | Material and performance specifications scope |
| DEL-03.03 Datasheet | PKG-03_Underground_Utilities_and_Drainage/1_Working/DEL-03.03.../Datasheet.md | Calculation types and analysis scope |
| DEL-03.04 Datasheet | PKG-03_Underground_Utilities_and_Drainage/1_Working/DEL-03.04.../Datasheet.md | Equipment data sheets scope (OWS, pipes, instrumentation) |
| DEL-03.05 Datasheet | PKG-03_Underground_Utilities_and_Drainage/1_Working/DEL-03.05.../Datasheet.md | Installation and test records scope |
| DEL-03.06 Datasheet | PKG-03_Underground_Utilities_and_Drainage/1_Working/DEL-03.06.../Datasheet.md | CCTV survey report scope |
| Config | /Users/ryan/ai-env/projects/chirality-app/test/execution/_Estimates/_CONFIG.md | Currency, pricing date, contingency method, rounding |

## Known Gaps

| Gap | Impact | Resolution Path |
|-----|--------|-----------------|
| No storm drainage quantities (pipe lengths, sizes, manhole counts) | Unable to price storm drainage by volume | Provide design drawings (DEL-03.01) with quantity takeoff |
| No OWS sizing (treatment capacity, separator volume, instrumentation count) | Unable to price OWS equipment by specifications | Provide design calculations (DEL-03.03) and equipment selection (DEL-03.04) |
| No duct bank quantities (conduit lengths, sizes, pull box counts) | Unable to price duct banks by volume | Provide duct bank plans with conduit schedules |
| No trenchless crossing quantities (crossing count, lengths, casing sizes) | Unable to price trenchless work by crossing | Provide trenchless crossing drawings and boring specifications |
| No vendor quotes | All equipment/materials as allowances | Obtain budgetary quotes for OWS, pipes, manholes, duct bank materials |
| No rate tables | Labor and equipment rates assumed | Provide project rate library |
| No site-specific constraints | Installation productivity assumed standard | Provide site logistics plan, access constraints, working hour restrictions |

## Next Run Improvements

To improve estimate accuracy for PKG-03 in the next iteration:

1. **Provide design quantities:** Complete DEL-03.01 drawings with pipe sizes, lengths, manhole counts, OWS location and size, duct bank conduit schedules, trenchless crossing details.
2. **Provide OWS sizing:** Complete DEL-03.03 calculations with OWS treatment capacity, separator volume, retention time, instrumentation requirements.
3. **Provide equipment selection:** Complete DEL-03.04 data sheets with OWS equipment specifications, pipe material selections, instrumentation models.
4. **Obtain vendor quotes:** Request budgetary quotes for OWS equipment, pipe materials, manholes/catch basins, duct bank materials, trenchless boring services.
5. **Add rate tables:** Populate `_RateTables/` with project labor rates, equipment rates, material unit costs for civil/underground work.
6. **Clarify site constraints:** Provide site logistics plan with access restrictions, working hours, seasonal constraints, traffic management requirements.
